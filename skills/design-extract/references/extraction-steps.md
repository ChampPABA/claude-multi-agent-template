# Extraction Steps

Output target: **20-section `data.yaml`** + ~8–10 reference-only screenshots. See [output-format.md](output-format.md).

**Effort allocation (read this first).** The consumer (impeccable) digests a narrow CORE: `psychology` + the design tokens (color/type/spacing/components/shadows/radius/motion-feel/page-composition). Extract that thoroughly — it is the whole point. Everything else is SUPPLEMENTARY: capture it only when it falls out cheaply from a pass you're already running, and never let it block or slow the CORE. The tier table is in [output-format.md](output-format.md#section-tiers); supplementary items are flagged inline below.

agent-browser commands used here: `open`, `eval <js>` (run JS, return JSON), `set viewport <w> <h>`, `set media [dark|light]`, `screenshot [selector] [path]`. All custom JS is written dynamically per site — no hardcoded scripts.

---

## STEP 0: Parse Input & Setup

1. Validate URL — if missing, error: "URL required. Usage: /extract https://airbnb.com"
2. Normalize — trim whitespace, add `https://` if missing
3. Extract site name — remove `www.` and TLD (e.g., `www.airbnb.com` → `airbnb`)
4. Check existing — if `design-system/extracted/{siteName}/data.yaml` exists, ask user to re-extract or keep
5. Create dirs: `mkdir -p design-system/extracted/{siteName}/screenshots`

---

## STEP 1: Open page → capture intro motion → multi-theme → trigger lazy content

```bash
agent-browser open {url}
```

Wait for page load. If redirect occurs, verify final URL is the intended site.

**1a. Capture intro motion FIRST — before any scroll (CRITICAL ordering).**
Native `document.getAnimations()` returns CSS `@keyframes` + CSS transitions + WAAPI `element.animate()` animations. **Finished animations are auto-discarded** unless `fill: forwards|both` or `Animation.persist()` — so intro/load animations vanish within ~1s and BEFORE the lazy-scroll pass below. Capture them immediately:

- At load **t+0, +300, +600ms**, call `document.getAnimations()`; for each, record `animationName`/`id`, `currentTime`, `effect.getTiming()` (duration/easing/delay), and `timeline` constructor name → split **DocumentTimeline** (time-driven) vs **ScrollTimeline**/**ViewTimeline** (scroll-driven). `persist()` any candidate you want to re-read later.
- This feeds `motion.native.getanimations_count` + `motion.native.by_timeline`. Guard with feature-detect + try/catch.
- Also screenshot the hero viewport now (`motion-hero-0ms.png`) and again at +600ms (`motion-hero-600ms.png`) for the motion vision-diff.

**1b. Multi-theme detection.**
Detect whether a second theme exists: `[data-theme]` attribute, `.dark`/`.light` class on `html`/`body`, or `prefers-color-scheme` response. If found, capture a palette per theme by toggling and re-reading computed styles, then diff:
- attribute/class themes: set `documentElement.dataset.theme = "dark"` (or toggle the class), re-read key computed colors, revert.
- media-query themes: `agent-browser set media dark` → re-read → `agent-browser set media light`.
- This is **live-site detection** — NOT a W3C token-set mechanism (§4). Feeds `color_palette.themes`.

**1c. Trigger lazy content.**
Scroll to bottom and back to top. Many sites lazy-load CSS/content on scroll; this ensures stylesheets, images, and components are present before STEP 2. (Do this AFTER 1a — scrolling can finish/discard intro animations.)

---

## STEP 2: Extract data (4 focused calls)

Split extraction into focused calls rather than 1 mega call — each clear scope produces more thorough extraction. ~80–120 lines of focused JS per call beats 200+ trying to do everything.

**Resilience (all calls):** wrap each category in try/catch — on failure continue and return partial data. Skip cross-origin stylesheets that throw SecurityError.

### Call 1: Visual styles + imagery (via getComputedStyle)

Sample top 50–100 visible elements. Return as JSON.

| # | Key | What to Extract |
|---|-----|-----------------|
| 1 | `colors` | backgroundColor, color, borderColor → RGB to HEX + frequency. Skip transparent. Keep near-black variants (dark-mode shades matter). |
| 2 | `typography` | fontSize, fontWeight, fontFamily, lineHeight, letterSpacing on h1–h6 + p + button + a + span. Unique fonts (incl. variable), all weights (incl. 510/590), full size scale. Derive `scale.ratio` (median size_n/size_n-1); if `--text-*` vars exist, emit `scale.named`. |
| 3 | `shadows` | All boxShadow values. Include offset (`4px 4px 0px` = neo-brutalist), layered, ring (`0 0 0 Npx`). A single offset shadow still counts. Infer named `sm/md/lg` by spread, or read `--shadow-*`. |
| 4 | `spacing` | padding, margin, gap. Detect grid base (4/8px). Skip "auto". |
| 5 | `borders` | borderRadius (incl. 9999px pills, 50% circles), borderWidth (1px vs 2–3px), borderColor. |
| 6 | `components` | Query buttons (`button, a[role=button], .btn, [class*=button]`), cards (`[class*=card], article`), inputs (`input, textarea, select`). Add `data-extract-id`. Capture computed styles + transition properties. |
| 7 | `imagery` | **NEW (§1).** For `img`/`picture`/`svg`/`video`/`background-image`/`canvas`/`lottie-player`: record **medium** (computable from element type) + **treatment** (all computable from CSS): `object-fit`, `aspect-ratio` (or computed w/h), `border-radius`, `mask-image`/`clip-path`, `filter`, `backdrop-filter`, `mix-blend-mode`, border/ring, full-bleed (≥100vw or wider than content max-width), overlay (abs `::before/::after` + bg/opacity, or gradient over bg-image). **Duotone = heuristic only** (check SVG `feColorMatrix` OR overlay+blend) → flag `inferred: true`, never certain. Aggregate treatments; sample bounded ~12–15 by role (hero, card-thumbnail 3–5, avatars, decorative bg, og). Leave `visual_description` empty for STEP 5. |

### Call 2: Stylesheet analysis + component states (via document.styleSheets)

Parse all accessible stylesheets. Return as JSON.

| # | Key | What to Extract |
|---|-----|-----------------|
| 8 | `keyframes` | All `CSSKeyframesRule` — name + full CSS text. Include library-specific (Toastify__, swiper-, sonner-). |
| 9 | `transitions` | transition, duration, timing-function, property from elements. Flag signature easing (custom cubic-bezier = intent). |
| 10 | `css_animations` | animationName/Duration/Delay/IterationCount/TimingFunction. Also `animation-timeline`, `animation-range`, `scroll-timeline-name`, `view-timeline-name` (scroll-driven, §3.3 — flag Firefox-partial). |
| 11 | `state_rules` | **EXPANDED (§8 / gap C).** Rules with `:hover`, `:focus`/`:focus-visible`/`:focus-within`, **`:active`, `:disabled`, `:invalid`** selectors — extract property changes per state. Also `[aria-disabled]`/`[aria-invalid]` styling. Map into `component_styles.<c>.states`. Custom cursor/scroll-snap/modal = out of scope. |
| 12 | `loading_patterns` | See "Detecting loading & feedback states" below. |
| 13 | `feedback_patterns` | See "Detecting loading & feedback states" below. |
| 14 | `css_custom_props` | All `--*` props on `:root`, `html`, `body`, `[data-theme]`, `document.documentElement`. Group by prefix (`grouped`) — this is the useful part. **Tier classification (§4) is SUPPLEMENTARY** — walking the `var()` DAG to label primitive/semantic/component is a community convention impeccable doesn't consume; emit `tiers` only if explicitly asked. The flat `grouped` view is enough. |

### Call 3: DOM structure + page composition + motion introspection (via querySelectorAll)

Query the live DOM. Return as JSON.

| # | Key | What to Extract |
|---|-----|-----------------|
| 15 | `iconography` | `svg` count + viewBox sizes, `[class*=icon]`, `i[class*=fa]`, icon `<img>`. System: inline-svg / icon-font (@font-face icon name) / img-based / sprite. (Renamed from icons_imagery.) |
| 16 | `forms` | `form`, `input`, `select`, `textarea`, `label`. Types (newsletter/search/login/contact), layout, validation attrs. |
| 17 | `accessibility` | **SUPPLEMENTARY** (impeccable runs its own a11y pass). Cheap parts worth keeping: semantic tags present (nav/main/footer/header/section) + contrast on the primary text/bg pair. Skip the `keyboard_focus_order` tab-sequence walk unless asked — it almost never survives into the consumer's output. |
| 18 | `page_composition` | **NEW (§2).** Walk top-level sections in document order (direct children of main/body). Classify each by semantic tag + heading level/font-size + layout (grid cols, flex dir) + content signatures → `section_sequence` `{order, type, subtype, note}`. Detect: hero (first large section, min-height ≥80vh for full-bleed subtype), logo-strip (grid/flex row 40–120px, high img/svg density, **zero text nodes** — NOT grayscale-filter), feature-grid (icon+title+text uniform), bento (grid-template-areas OR varying span OR `grid-auto-flow:dense` weak-alone), testimonial (quote+avatar+name), pricing (price regex + features + CTA), **FAQ 4-layer check** (`<details>` OR `[aria-expanded]` OR structural OR click-test: click trigger → `aria-expanded` flips + height→scrollHeight), cta-band, footer. |
| 18b | `layout_metrics` | **Folded from old `layout_patterns`.** Read base layout into `page_composition.layout_metrics`: `container_width` (max-width on main containers), `grid_columns` (cols on the primary grid), `breakpoints` (parse media-query min/max-width from accessible stylesheets). Don't drop these — they were the old top-level `layout`. |
| 19 | `nav_treatment` | **NEW (§2.3).** Read header `position` (sticky/fixed, top:0). Sample `getComputedStyle` backgroundColor **alpha** + boxShadow + backdropFilter at `scrollY=0` then `scrollY=400` **with a 200ms transition-wait between reads**. Classify behavior (solid / sticky-solid / transparent / transparent-to-solid / overlay; alpha `<0.2` vs `>0.8`). Detect glass = `backdrop-filter: blur()` **AND** semi-transparent bg. Logo position (flex order), mega-menu (large dropdown panels), mobile menu (hamburger + hidden menu). Emit `evidence`. |
| 20 | `motion_libraries` | **§3.4.** `script[src]` + DOM for gsap, framer-motion, lottie, anime.js, three.js, rive, spline. Best-effort introspection (feature-detect + try/catch): GSAP global → `window.ScrollTrigger.getAll()` (per instance: start/end/trigger/pin/scrub/vars); Lottie → `lottie-player.getLottie()` (totalFrames/frameRate/duration/loop); Framer Motion/bundled GSAP → mark `introspected:false, reason:module-scoped`. Record `load: global|bundled` per lib. |
| 21 | `view_transitions` | **§3.3.** Detect `document.startViewTransition` presence + `::view-transition*` usage. Emit `motion.native.view_transitions`. |
| 22 | `toast_libraries` | DOM footprint of toast libs (containers injected on load): `[class*=Toastify]`, `[data-sonner-toaster]`, `.swal2-container`, `[class*=notistack]`, `.notyf`, `[class*=hot-toast]`, `[data-headlessui-state]`. Report which present. |

### Call 4: Responsive reflow (via set viewport + diff) — SUPPLEMENTARY

Mechanical but costs 4 viewport switches, and `responsive_reflow` is recreation-only — impeccable builds its own responsive behavior and rarely consumes the inspiration's exact breakpoints. **Run this only when responsive behavior is specifically part of what you're studying; otherwise skip it and mark `responsive_reflow: { detected: false }`.** When you do run it:

1. For each viewport in **[375, 768, 1024, 1440]**: `agent-browser set viewport {w} 900`, then `eval` to read per top-level section (reuse the `page_composition` section ids): `grid-template-columns` (count), `flex-direction`, `display`, `visibility`, `order`.
2. Diff across viewports → emit `responsive_reflow.sections[].reflow` only for properties that change.
3. Detect `nav_collapse_breakpoint` — the viewport at/below which nav switches to hamburger.
4. Restore viewport to 1440 (or original) when done.

### Detecting loading & feedback states

Class-name matching alone fails on Tailwind / CSS-in-JS. Use 3 layers:

**Layer 1 — Stylesheet selector matching:** selectors containing `error`, `success`, `warning`, `alert`, `toast`, `notification`, `loading`, `skeleton`, `spinner`, `shimmer`, `pulse`.

**Layer 2 — CSS property patterns (framework-agnostic):**
- Error: red-range colors (#ef4444, #dc2626, #f87171…) on border/background
- Success: green-range (#22c55e, #16a34a, #4ade80); Warning: amber (#f59e0b, #d97706, #fbbf24)
- Spinners: `@keyframes` named/containing spin/rotate, or `transform: rotate(360deg)`/`1turn`
- Skeletons: `linear-gradient` + `background-size` animation, or shimmer/pulse keyframes

**Layer 3 — DOM/library footprint:** Toastify `[class*=Toastify]`; Sonner `[data-sonner-toast]`; react-hot-toast `[data-hot-toast]`; SweetAlert2 `.swal2-popup`; Notistack `[class*=notistack]`; Notyf `.notyf`; HeadlessUI `[data-headlessui-state]`; generic `[data-state]`/`[data-status]`.

---

## STEP 3: Interactive states + motion sampling (SINGLE-purpose JS calls)

**3a. Toast trigger** — if a toast library was detected (Call 3 `toast_libraries`), trigger it to force CSS to load: Sonner `window.toast?.('test')`; Toastify `window.Toastify?.({text:'test',duration:100}).showToast()`. Wait 200ms, capture newly loaded toast-related stylesheet rules, dismiss immediately. If the global fn doesn't exist, skip (module-scoped).

**3b. Hover/focus/active diffs** — loop `data-extract-id` elements: capture default → `dispatchEvent(new MouseEvent('mouseenter'))` → wait transition (fallback 300ms) → capture → `mouseleave`; `element.focus()` → capture outline/box-shadow/border → `blur()`. Record diffs into `component_styles.<c>.states`. Skip on failure, no retry.

**3c. Contrast ratios** — luminance ratio for primary text/background pairs. Flag WCAG AA (<4.5:1) and AAA (<7:1).

**3d. Scroll-hijack-aware motion sampling (§3.5 — CRITICAL).**
1. **Detect hijack FIRST:** `window.lenis`, `[data-lenis]`, `window.locomotive`, `[data-scroll-container]`.
2. **If present → drive the library instance** (e.g. `window.lenis.scrollTo(pos, { immediate: true })`), **NOT `window.scrollTo`** (native scrollY stays 0 on hijacked sites). If GSAP present, `ScrollTrigger.refresh()` after each move so pins revert + bounds recalc.
3. **If absent → `window.scrollTo` is fine.**
4. At **0/25/50/75/100%** scroll, record per candidate `opacity`, `transform` (decompose matrix → translate/scale/rotate), `getBoundingClientRect`. Diff → reconstruct motion → `motion.runtime.sampled_motion`.
5. Candidates: scroll-animation attrs, near ScrollTriggers, in hero, or present in `getAnimations()`.
6. Set `motion.runtime.scroll_hijack` accordingly (library + sampling_method).

---

## STEP 4: Screenshots (~8–10, reference-only)

Copyright-safe references for the vision-capable downstream. Use `agent-browser screenshot [selector] [path]`:

| Screenshot | How |
|---|---|
| `full-page.png` | `screenshot --full` — overall composition + color story |
| `hero.png` | viewport screenshot at top — most memorable |
| `section-*.png` (2–3) | selector screenshots of hero / one feature-or-bento / one testimonial-or-CTA |
| `nav-top.png` + `nav-scrolled.png` | nav at scrollY=0 vs after scroll — only if `transparent-to-solid` |
| motion frames (2–4) | from STEP 1a (`motion-hero-0ms`, `motion-hero-600ms`) + 1 mid-scroll (`motion-scroll-50.png`) |

Index every file in the `screenshots` section (+ motion frames also in `motion.captured_frames`).

---

## STEP 5: Vision analysis (psychology + visual descriptions)

Analyze screenshots + extracted data. Vision fills what CSS/DOM cannot (§6 split).

| Field | What to Analyze |
|-------|-----------------|
| `psychology.*` | style_classification (see [style-detection.md](style-detection.md)), brand_personality (2–4 tags), emotions_evoked, target_audience, visual_principles, why_it_works, design_philosophy |
| `psychology.motion_narrative` | one-line motion feel (mirror `motion.feel.summary`) |
| `imagery.images[].visual_description` | photo-vs-illustration, editorial/product/lifestyle, color grade/mood, people present, 3D-vs-flat |
| `motion.feel.*` | pacing/easing/choreography/scroll_coupling/scale from sampled motion + frames (grounded vocab, §3.7) |
| `page_composition.visual_notes` | emit **raw** `airiness_score`; let vision assign `density_label`/`symmetry` from the screenshot (thresholds provisional, V2 — do NOT hard-bucket) |

---

## STEP 6: Generate data.yaml

1. Read `metadata` (favicon/OG/theme-color/manifest/apple-touch-icon from `meta`/`link` tags — refs only, no download).
2. Map all extracted data to the **20 output sections** (see [output-format.md](output-format.md)).
3. Motion contract: always emit the CORE — `feel` (the one block impeccable digests) + `libraries` (names + `load`, so it knows the stack) + `captured_frames`. `native` counts, `runtime.sampled_motion`, and `scroll_triggers` vars are SUPPLEMENTARY — emit them compactly only if they fell out cheaply (e.g. `scroll_triggers` only when GSAP is global). `feel` can be read from STEP 1a `getAnimations()` + frames + libraries without the full 5-point sample.
4. Compute coverage: `total_sections: 20`, `detected_sections`, `percentage`, and **required** `coverage.missing` (every undetected section).
5. Write to `design-system/extracted/{siteName}/data.yaml`.

---

## STEP 7: Final Report

Display: coverage %, psychology status, screenshot count + paths, output path, next step (`/impeccable`).
