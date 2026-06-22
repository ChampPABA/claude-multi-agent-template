# Extract Skill — Completeness Research & Proposal

**Why:** extract is now the single gateway capturing design inspiration from reference sites (flow: `extract → impeccable`, designsetup/pageplan removed). Its quality determines downstream output. Current skill is strong at token/component level but shallow on "overall look" dimensions.

**Scope:** what extract should capture to be complete for general use, where output may feed another (vision-capable) AI. All additions are **descriptions + screenshots** — no asset download (constraint validated as correct, not a gap).

**Downstream lens:** the consumer is a vision-capable AI. Give it **structured YAML for computable facts** (precise, reusable) + **rich screenshots + concise prose for holistic look/feel** (what it can see). See §6.

---

## §0. Feedback validated against code

| Feedback | In code | Status |
|---|---|---|
| 1. Imagery style shallow | `icons_imagery` = icon system/count/size/outline only; `bg_media` counts videos/gifs/lottie | gap |
| 2. Section composition shallow | `layout_patterns` = container_width/grid_columns/breakpoints only | gap |
| 3. One screenshot only | STEP 4: "One screenshot is enough" | gap |
| 4. Runtime motion invisible | `animation_libraries` = `{name, modules}` — knows "has GSAP", not "what it does" | tech limit, **mostly closable** — re-verified (NotebookLM, 88 sources) |
| 5. Don't download assets | skill already captures descriptions only | keep |

---

## §1. Imagery (NEW dimension)

**✅ Grounded via V1** (~85 sources): [research/V1-imagery.md]. The draft below was largely confirmed — treatment signals are computable from CSS, the DOM-vs-visual split holds, and bounded sampling by role is the right approach. **One correction:** duotone has **no single reliable detection signal** — it is heuristic-only (multiple techniques: SVG `feColorMatrix`, overlay+blend, etc.; see §1.2).

Today the tool knows "N images / N svgs" but not their **style** or **treatment**.

### 1.1 Style taxonomy (medium = computable; subject = visual)

| Style | Decision rule |
|---|---|
| Photography — editorial | `<img>`/`<picture>` raster, people/scenes, aspirational |
| Photography — product | raster, single object, clean/neutral bg |
| Photography — lifestyle | raster, in-context use |
| Illustration — flat | inline `<svg>`/raster, single-tone fills, no shading |
| Illustration — hand-drawn | svg/raster, irregular stroke |
| Illustration — isometric | svg/raster, 30° projection |
| Illustration — line-art | svg, stroke-only |
| 3D render | raster, soft shading/reflections; or `<canvas>` (Three.js) |
| Gradient / mesh | `background-image: linear/radial/conic-gradient` or `mesh-gradient` |
| Abstract / geometric | svg/raster shapes, blobs |
| Icon-as-hero | oversized inline `<svg>` as primary visual |
| Video / film | `<video>` / `<source>` / cinemagraph |

**Medium is computable from DOM** (`img` vs `svg` vs `video` vs `background-image` vs `canvas` vs `lottie-player`). **Subject/style is visual** (photo vs illustration, editorial vs product, color grade, mood) — filled from screenshot by vision.

### 1.2 Treatment / framing dimensions (all computable from CSS)

| Dimension | CSS/HTML signal |
|---|---|
| Fit / crop | `object-fit` (cover/contain/fill/none/scale-down) |
| Aspect ratio | `aspect-ratio`, or computed w/h |
| Corner radius | `border-radius` on image/container (0 sharp, large rounded, 50%/9999 circle/pill) |
| Mask / clip | `mask-image`/`-webkit-mask-image`, `clip-path` (polygon/blob/circle) |
| Filters | `filter`: grayscale, sepia, blur, brightness, contrast, saturate, hue-rotate |
| Backdrop | `backdrop-filter` |
| Blend | `mix-blend-mode`, `background-blend-mode` |
| Duotone | **no single reliable signal (V1)** — heuristic only: check SVG `feColorMatrix`, OR overlay element + `mix-blend-mode`; flag as inferred, not certain |
| Borders / ring | `border`, `outline`, ring `box-shadow` (`0 0 0 Npx`) |
| Full-bleed | width 100vw, or wider than content max-width, negative margins |
| Overlay | abs-positioned `::before/::after` with bg+opacity, or `linear-gradient` overlay on bg-image |
| Grain / texture | bg-image noise data-uri, or blend overlay |

### 1.3 Computable vs visual split

- **Computable (DOM/CSS):** medium, object-fit, aspect-ratio, radius, mask, clip-path, filter, blend, border, overlay presence, full-bleed.
- **Visual (screenshot):** photo-vs-illustration, editorial/product/lifestyle, warm/cool/neutral grade, mood, people present, illustration sub-style, 3D-vs-flat. → one-line `visual_description`.

### 1.4 Sampling (bounded — don't capture all images)

Categorize by role, cap per role, total ~12–15:
- Hero/primary (largest in first viewport), card thumbnails (3–5), avatars (circular small), decorative bg (`background-image` on large sections), OG/social (`meta[property="og:image"]`).

### 1.5 Proposed YAML

```yaml
imagery:
  detected: true
  sampling: { scanned: 47, categorized: 12, capped: true }
  dominant_mediums: ["photography", "svg-illustration"]
  treatments:                       # aggregate of detected CSS treatments
    object_fit: { cover: 18, contain: 3 }
    aspect_ratios: ["16/9", "4/5", "1/1", "3/2"]
    corner_radius: { values: ["0px", "8px", "12px", "50%"], dominant: "12px" }
    masks: { clip_path: 4, webkit_mask: 1 }
    filters: { grayscale: 2, brightness: 1 }
    blend_modes: ["multiply", "overlay"]
    overlays: { gradient: 7, solid: 2 }
    full_bleed: 3
  images:                           # bounded sample
    - role: "hero"
      medium: "photography"
      treatment:                     # computable
        object_fit: "cover"
        aspect_ratio: "16/9"
        corner_radius: "0px"
        full_bleed: true
        overlay: "linear-gradient(180deg, transparent 0%, rgba(0,0,0,0.5) 100%)"
      visual_description: "editorial lifestyle photo, warm grade, people present"  # vision-filled
    - role: "card-thumbnail"
      medium: "svg-illustration"
      treatment: { aspect_ratio: "1/1", corner_radius: "12px" }
      visual_description: "flat illustration, single accent color"
  og_image: "present"                # detected via meta, value not stored
```

**Key:** split each entry into `treatment` (computable, precise) + `visual_description` (vision-filled). Downstream reads treatment for fidelity, screenshot for style.

---

## §2. Page composition (NEW dimension)

**✅ Grounded via V2** (~50 effective / 181 imported): [research/V2-composition.md]. The draft's overall anatomy approach holds, but **7 specific detection claims were wrong/unverified** — corrections below override the draft where they conflict.

**Corrections to the §2 draft (from V2):**
1. **Hero min-height: ≥80vh, not 60vh.** The draft's `60vh` is **unverified**; full-bleed hero subtype cites `>= 80vh`.
2. **Logo-strip signal is NOT `filter:grayscale`.** Not cited anywhere. Use instead: grid/flex row, height `40–120px`, high img/SVG density, uniform dimensions, zero text nodes.
3. **FAQ detection needs a 4-layer check**, not just `<details>`. Native `<details>` is sufficient-but-not-necessary (modern accordions are JS divs): add structural + `aria-expanded` + behavioral click-test (click trigger → `aria-expanded` flips, height → scrollHeight).
4. **Glass = `backdrop-filter: blur()` AND semi-transparent bg-color.** Draft checked only the former (incomplete).
5. **Bento: add `grid-auto-flow: dense`** as a third signal, but mark weak-alone (false positives on uniform grids).
6. **Nav scroll-sampling: add a 200ms transition-wait** between `scrollY=0` and `scrollY=400` reads (transition must settle).
7. **Airy/dense AR thresholds (0.45/0.20) are provisional.** Formula is cited but bucket-cutoffs aren't empirically validated → **emit raw scores, let the vision pass assign labels.**

**Supported as-is (V2):** transparent-to-solid alpha-sampling (scrollY=0 vs 400, thresholds `<0.2` / `>0.8`), all 6 hero subtypes, feature-grid uniformity check, footer positional rule, sticky validation via programmatic scroll.

Today captures grid **metrics**, not page **anatomy**.

### 2.1 Anatomy vocabulary + detection signals

| Section | Detection signal |
|---|---|
| Header/nav | `<header>`, first `<nav>`, top of page |
| Hero | first large section after header; largest font-size text; min-height ≥ 60vh |
| Hero subtypes | centered / split (grid/flex 2-col) / full-bleed-image / video-bg / product / stat |
| Logo strip | row of `<img>` with `filter:grayscale` or low opacity |
| Feature grid | grid of cards: icon + title + text |
| Bento grid | grid with varying col-span/row-span / grid-template-areas |
| Testimonial | quote + avatar + name pattern |
| Pricing | cards with price regex + feature list + CTA |
| CTA band | full-width, single heading + button, contrasting bg |
| FAQ | `<details>` or `[aria-expanded]` accordion |
| Footer | `<footer>` |

**Method:** walk top-level sections in document order (direct children of main/body), classify each by semantic tag + heading level/font-size + layout (grid cols, flex direction) + content signatures (price regex, avatar+name, details, logo row).

### 2.2 Section sequencing (the high-value field)

Ordered list of `{order, type, note}` in reading order. This is what makes two sites "feel" different with identical tokens.

### 2.3 Nav treatment (often the most memorable thing about a site)

| Pattern | Detection |
|---|---|
| sticky/pinned | `position: sticky/fixed`, top:0 |
| transparent-over-hero | computed bg alpha at scrollY=0 |
| solid | bg alpha full at top |
| transparent→solid-on-scroll | alpha 0 at top, ~1 after scroll |
| glass | `backdrop-filter: blur(...)` |
| center-logo vs left-logo | logo element position in nav flex |
| mega-menu | large dropdown panels |
| mobile overlay | hamburger button + hidden menu |

**Method:** read header position; sample `getComputedStyle` backgroundColor alpha + boxShadow + backdropFilter at scrollY=0 and scrollY=400; compare → classify.

### 2.4 Hero composition

`layout` (centered/split/full-bleed/stacked), headline font-size + weight, CTA count, `background` type (solid/gradient/image/video/mesh/canvas).

### 2.5 Proposed YAML

```yaml
page_composition:
  detected: true
  nav:
    behavior: "transparent-to-solid-on-scroll"   # solid | sticky-solid | transparent | transparent-to-solid | overlay
    backdrop_blur: true
    logo_position: "left"
    mega_menu: false
    mobile_menu: "overlay"
    evidence: { bg_alpha_top: 0.0, bg_alpha_scrolled: 0.95, position: "sticky" }
  hero:
    layout: "split"            # centered | split | full-bleed | stacked
    headline_fontsize: "64px"
    headline_weight: "700"
    cta_count: 2
    background: "image"        # solid | gradient | image | video | mesh | canvas
  section_sequence:            # reading order — the high-value field
    - { order: 1, type: "header", note: "sticky nav, transparent over hero" }
    - { order: 2, type: "hero", subtype: "split", note: "left headline+CTA, right product shot" }
    - { order: 3, type: "logo-strip", note: "6 grayscale logos" }
    - { order: 4, type: "feature-grid", note: "3-up icon+title+text" }
    - { order: 5, type: "cta-band", note: "full-width contrasting bg" }
    - { order: 6, type: "footer" }
  layout_metrics:              # existing layout_patterns fields folded here
    container_width: "1280px"
    grid_columns: 12
    breakpoints: [...]
  visual_notes:                # vision-filled
    density: "airy"            # airy | balanced | dense
    symmetry: "symmetric"
```

**Key:** `section_sequence` + `nav.behavior` are the two fields that capture "why this site looks different" (Champ's point #2).

---

## §3. Motion / cinematic (EXPANDED dimension) — re-verified via NotebookLM deep research (88 sources)

**Headline:** runtime motion is **mostly recoverable**, but the tool depends on the source. The first draft of this section underweighted the native `getAnimations()` path, missed CSS scroll-driven animations + View Transitions entirely, proposed a sampling method that **breaks on Lenis/Locomotive sites**, and **invented** the feel thresholds. All corrected below.

### 3.1 The recovery split

| Motion source | How to capture | Confidence |
|---|---|---|
| CSS `@keyframes`, transitions, WAAPI `element.animate()` | `document/Element.getAnimations()` | high |
| CSS scroll-driven (`animation-timeline: scroll()/view()`) | computed styles + `Animation.timeline` type | high |
| View Transitions | `document.activeViewTransition` / `::view-transition*` | medium |
| GSAP (global/UMD) | `window.ScrollTrigger.getAll()` | high |
| GSAP (ES-module), Framer Motion, Rive, Spline | empirical sampling | medium |
| Lottie (`lottie-player`) | `el.getLottie()` | high |

### 3.2 Native CSS/WAAPI introspection — the primary path (was underweighted)

`document.getAnimations()` / `Element.getAnimations()` return native `Animation` objects. They **DO include** CSS `@keyframes`, CSS transitions, WAAPI `element.animate()`. They **DO NOT include GSAP** — GSAP runs its own `requestAnimationFrame` engine and never creates native `Animation` objects (confirmed). `Element.getAnimations()` supports `{ subtree: true }` and `{ pseudoElement }`.

- **Scroll-driven split:** inspect each `Animation.timeline` — `ScrollTimeline`/`ViewTimeline` = scroll-driven, `DocumentTimeline` = time-driven. Cleanly separates the two without reading CSS.
- **Finished-animation caveat:** completed animations are auto-discarded unless `fill: forwards|both` or `Animation.persist()`. Intro animations may be gone by query time → **sample early (load t+0/+300/+600ms)** or `persist()` candidates.
- **Support:** baseline since 2020 (Chrome 84, FF 75, Safari 13.1). Safe.

### 3.3 CSS scroll-driven animations + View Transitions (NEW — entirely missing before)

Standards-based motion with **no JS** — increasingly common, invisible to the old schema.

- **Scroll-driven:** detect via computed styles — `animation-timeline`, `animation-range` (+`-start`/`-end`), `scroll-timeline-name`, `view-timeline-name`. (Legacy `@scroll-timeline` at-rule is deprecated/unsupported.) Support: Chrome/Edge 115+, Safari 18+, **Firefox partial (flag-gated)** — flag it in output.
- **View Transitions API:** detect via `document.activeViewTransition` (non-null = transitioning), monkey-patch `document.startViewTransition` to log SPA transitions, or `::view-transition*` pseudo-elements during capture.

### 3.4 Library introspection (best-effort)

| Lib | Method | Readable |
|---|---|---|
| **GSAP** (global/UMD) | `window.ScrollTrigger.getAll()` | per instance: `.animation`, `.start`, `.end`, `.trigger`, `.pin`, `.vars` (config incl. `scrub`, `toggleActions`), `.progress`, `.direction`, `.isActive` |
| **GSAP** (ES-module, `window.gsap` undefined) | `element._gsap` private cache / `gsap.getProperty(target, prop)` | internal, **not API-guaranteed** (underscore-prefixed) — best-effort, flag it |
| **Lottie** (`lottie-player`) | `el.getLottie()` | `totalFrames`, `frameRate`, `duration`, `autoplay`, `loop` |
| **Framer Motion / Motion** | none reachable | module-scoped, React-internal → sampling only |
| **anime.js** | `window.anime.running` | active tweens, transient |

Record `load: global|bundled` per library so downstream knows feasibility.

### 3.5 Empirical sampling — now scroll-hijack-aware (critical fix)

**The first draft's `window.scrollTo` sampling breaks on Lenis/Locomotive sites:** they hijack scroll (`preventDefault` + `translate3d`/rAF loop), so native `scrollY` stays 0 and CSS scroll-driven animations never fire; they also desync GSAP ScrollTrigger bounds ("synchronicity collisions").

Corrected protocol:
1. **Detect hijack first** (`window.lenis`, `[data-lenis]`, `window.locomotive`, `[data-scroll-container]`).
2. **If present → drive the library instance directly** (e.g. `window.lenis.scrollTo(pos, { immediate: true })`), NOT `window.scrollTo`. Then `ScrollTrigger.refresh()` (if GSAP) so pinned elements revert + bounds recalc.
3. **If absent → `window.scrollTo` is fine.**
4. At 0/25/50/75/100% scroll and load t+0/+300/+600ms, record per candidate: `opacity`, `transform` (matrix → translate/scale/rotate), `getBoundingClientRect`. Diff → reconstruct motion.
5. Candidates: scroll-animation attrs, near `ScrollTrigger`s, in hero, or appearing in `getAnimations()`.

This covers module-scoped libs (Framer Motion, bundled GSAP) AND hijacked-scroll sites — the two cases naive sampling misses.

### 3.6 Frame capture (vision diff)

Viewport/region at the same scroll positions + load ticks → before/after pairs so a vision model SEES what moved. Bounded ~4–6 frames (hero load + 2–3 scroll positions + 1 section close-up).

### 3.7 Motion-feel vocabulary (CORRECTED — grounded; was fabricated)

| pacing | ms range | source |
|---|---|---|
| Instant | 0–120 ms | Apple `--duration-instant` 100ms (micro-interactions); Material "Short" 50–200ms |
| Snappy | 120–220 ms | Apple `--duration-fast` 200ms (hover/focus) |
| Standard | 220–350 ms | Apple `--duration-normal` 300ms; Material "Medium" 250–400ms |
| Deliberate | 350–600 ms | Apple `--duration-slow` 500ms (complex); Material "Long" 450–600ms |
| Cinematic | >600 ms | Material "Extra-long" 700–1000ms (ambient only) |

Easing → match Material 3 named curves (Emphasized, Emphasized-decelerate, Standard) + detect overshoot (cubic-bezier control-point y > 1 ≈ spring/bouncy). Choreography: constant delay offset between elements → stagger interval. Scroll-coupling: element progress ∝ scroll progress → scrubbed-to-scroll, else trigger-once. Scale: micro (hover/press) vs scene (section transition / pinned).

### 3.8 Proposed YAML (consolidated `motion`)

```yaml
motion:
  native:                      # 3.2/3.3 — WAAPI + standards-based (primary)
    getanimations_count: 34
    by_timeline: { document: 28, scroll: 4, view: 2 }   # Animation.timeline split
    scroll_driven: { detected: true, props: ["animation-timeline", "animation-range"], firefox_flag_needed: true }
    view_transitions: { detected: false }
    persist_caveat: "finished anims discarded unless fill:forwards|both — sampled early"
  libraries:                   # 3.4 — best-effort
    - { name: "gsap", detected: true, load: "global", introspected: true, scrolltriggers: 6 }
    - { name: "framer-motion", detected: true, load: "bundled", introspected: false, reason: "module-scoped" }
    - { name: "lottie", detected: true, players: 2, player_meta: [{ totalFrames: 120, frameRate: 30, duration: 4.0, loop: true }] }
  runtime:                     # 3.4/3.5
    scroll_triggers:           # from ScrollTrigger.getAll()
      - { trigger: "section.hero", start: "top 80%", end: "bottom 20%", scrub: true, pin: false, animation: { duration: 1.0, ease: "power2.out", stagger: 0.1 } }
    scroll_hijack:             # critical 3.5 detection
      detected: true
      library: "lenis"
      sampling_method: "lenis.scrollTo(immediate) + ScrollTrigger.refresh()"   # NOT window.scrollTo
    sampled_motion:
      - selector: "h1.hero-title"
        scroll_progress: { "0%": { opacity: 0, y: 40 }, "25%": { opacity: 1, y: 0 } }
        inferred: "fade-up over first 25% of scroll"
  feel:                        # 3.7 — grounded
    pacing: "standard"         # 0-120 instant | 120-220 snappy | 220-350 standard | 350-600 deliberate | >600 cinematic
    easing: "emphasized-decelerate"
    choreography: "staggered, 80ms interval"
    scroll_coupling: "scrubbed-to-scroll"
    scale: "scene"
    cinematic: false
    summary: "Standard-paced, scroll-scrubbed, staggered reveals"
  captured_frames:
    - { id: "hero-load", file: "screenshots/motion-hero-0ms.png" }
    - { id: "hero-intro", file: "screenshots/motion-hero-600ms.png" }
    - { id: "scroll-50", file: "screenshots/motion-scroll-50.png" }
```

**Key:** native `getAnimations()` (+timeline-type split) is the primary reliable path for CSS/WAAPI/scroll-driven; library introspection covers global GSAP + Lottie; hijack-aware empirical sampling covers the rest (Framer Motion, bundled GSAP, Lenis sites); feel-summary is now grounded in Apple HIG + Material 3.

**Scope note (from prior decision):** since downstream (impeccable) regenerates motion, the high-value output is likely `feel` + `sampled_motion` + `captured_frames`, not the precise `scroll_triggers` vars — those are cheap to collect when GSAP is global but are optional. (See §9 Q4.)

---

## §4. Token-tier completeness (grounded via V5 — corrected)

**✅ Grounded:** [research/V5-token-tiers.md]. Two claims in the original draft were **overclaims** and are corrected here:

1. **The primitive → semantic → component tier split is a COMMUNITY CONVENTION, not W3C-mandated.** The W3C Design Tokens Format Module (stable: **2025.10 Final Community Group Report, 28 Oct 2025**) standardizes token *types* (`$type`: color/dimension/duration/shadow/transition/asset/…), the `$type`/`$value` structure, and alias references `{group.token}` + `$extensions` — but it does **not** prescribe a tier taxonomy. Treat tiers as a useful heuristic, not spec compliance.
2. **The W3C format has NO native multi-theme / `$themes` mechanism.** There is no spec-endorsed multi-set construct for dark mode. So "multi-theme sets" must be detected on the **live site**, not modeled as a W3C token feature.

**Corrected recommendations:**

| Concern | Grounded recommendation |
|---|---|
| **Tier classification** (convention, not spec) | Walk the `var()` reference graph from `css_custom_properties` — modeled as a **DAG** (vertices = custom props, edges = `var()` refs). Classify by graph position: leaves (raw values) ≈ primitive; mid nodes (role-named, e.g. `--color-brand`) ≈ semantic; nodes consumed by a component scope (`--button-bg`) ≈ component. Emit as a heuristic with confidence. |
| **Multi-theme / dark mode** (live-site detection, no spec mechanism) | Detect on the rendered page: `[data-theme]`, `.dark`/`.light` classes, `prefers-color-scheme`. To capture a per-theme palette: toggle the attribute/class (or flip the media query), re-read computed styles, diff. Many SaaS sites have dark mode currently invisible to extract. |
| **Motion as first-class token** | Consolidate scattered motion blocks → one `motion` section (§3). Named duration/easing tokens when `--motion-*`/`--ease-*` vars exist (community convention; the W3C `transition`/`duration` types can represent them). |
| **Elevation / typography scales** | Named shadow levels (sm/md/lg) and named type scale (`--text-h1`) when vars reveal them; else derive a ratio. |
| **Asset references** | W3C `asset` token type is the spec-endorsed "reference without downloading" — store icon/logo refs (name + role), not files. Aligns with the no-asset constraint AND the standard. |

**Net:** tier classification + multi-theme detection are still worth doing — but as **heuristics on the live DOM/CSS**, justified by community practice and recreation value, not by claiming W3C mandates them.

---

## §5. Screenshot strategy (cross-cutting — Champ's point #3)

Current: 1 full-page. Expand to ~8–10, all reference use (copyright-safe):

| Screenshot | Why |
|---|---|
| Full-page (keep) | overall composition + color story |
| Viewport hero (above-the-fold at load) | most important, what people remember |
| Section close-ups (2–3) | hero, one feature/bento, one testimonial/CTA — feed style/treatment/imagery |
| Motion frames (2–4) | hero load t+0 vs t+600ms; one scroll-position pair — feed motion-feel |
| Nav states (1) | nav at top (transparent) vs scrolled (solid), if transparent-to-solid |

impeccable is vision-capable → targeted images improve reconstruction. Cheap relative to their signal.

---

## §6. Structured vs visual split (downstream design principle)

| Computable → structured YAML | Holistic → screenshot + prose |
|---|---|
| colors, type sizes, spacing, radii, shadows, easings, object-fit, aspect-ratio, grid columns, section order, sticky positioning, scroll-coupling | photo vs illustration, color grade/mood, density/airiness, style classification, brand personality, motion feel, "premium vs playful" |

**Rule:** if a fact has a CSS/DOM signal → structured. If it needs a human eye → screenshot + one-line `visual_description`. Every new section follows this split.

---

## §7. Schema consolidation flags (clarity only, not feature cuts)

| Current | Issue | Recommendation |
|---|---|---|
| `animations_transitions` + top-level `animations:` + `animation_libraries` | motion in 3 places | consolidate into one `motion` (§3.6); per-component states move under `component_styles.<c>.states` |
| `layout_patterns` (metrics only) | no anatomy | fold metrics into `page_composition.layout_metrics` (§2.5) |
| `icons_imagery` (icons + imagery conflated) | two different concerns | split: `iconography` (icons) + new `imagery` (§1.5) |
| `css_custom_properties` (flat) | no tiers | keep + use to populate semantic-tier view (§4) |

---

## §8. Concrete proposal — extract skill changes

**Scope: VISUAL-ONLY (decided).** extract captures computable visual structure + holistic screenshots for a vision-capable downstream (impeccable). The 5 recreation-only dimensions V4 surfaced (§11) are **excluded from structured extraction** — they are already-covered, non-visual, or screenshot-carried (see §11 disposition). Principle §6: computable → YAML; holistic → screenshot + prose.

**Target data.yaml: ~20 sections** (from 17):

NEW: `imagery`, `page_composition`, `responsive_reflow` (gap B), `motion` (consolidated), `iconography` (renamed), `metadata` (opt, small: favicon/OG/theme-color/manifest refs), `screenshots` (index).
EXPANDED: `color_palette` (multi-theme via live `[data-theme]`/`.dark`/`prefers-color-scheme` toggle — NOT a W3C token set, per §4), `typography` (named scale/ratio), `shadows_elevation` (named levels), `css_custom_properties` (tier classification via `var()` DAG — heuristic, convention not spec, per §4), `component_styles.<c>.states` (expand to active/disabled/error + keyboard-focus order — gap C standard subset).
FOLDED/RENAMED: `layout_patterns`→`page_composition.layout_metrics`, `animations_transitions`/`animations`/`animation_libraries`→`motion`, `icons_imagery`→`iconography`. (`theme_sets`/`design_tokens_tiers` from the earlier draft are NOT separate sections — §4 grounded that multi-theme is live-detection and tiers are css_custom_properties classification.)

**Extraction-step changes:**

| Step | Change |
|---|---|
| STEP 1 | detect multi-theme; toggle `[data-theme]`/`.dark`/`prefers-color-scheme` to capture a palette per theme (live-site detection — no W3C set mechanism) |
| STEP 2 Call 1 | add imagery treatment extraction (object-fit/aspect-ratio/radius/mask/filter/blend/overlay on img/svg/video/background-image); duotone flagged heuristic-only |
| STEP 2 Call 2 | expand component states: capture `:active`/`:disabled`/`:invalid` stylesheet rules + `aria-disabled` + keyboard-focus (focusable tab order). Custom cursor/scroll-snap/modal = out of scope. |
| STEP 2 Call 3 | section-walk for `page_composition` (classify top-level sections in order) + nav treatment sampling (transparent-to-solid alpha-sample with 200ms transition-wait) |
| STEP 2 Call 4 | **responsive_reflow** — emulate 3–5 viewports (375/768/1024/1440px via Playwright `setViewportSize`), per top-level section diff grid-cols/flex-direction/display/visibility/order + detect nav→hamburger breakpoint. Mechanical/deterministic — no research needed. |
| STEP 2/3 | native `document.getAnimations()` (+ `Animation.timeline` split: Document/Scroll/View) + scroll-driven (`animation-timeline`) + View Transitions + library introspection (`window.gsap`/`ScrollTrigger.getAll`/`lottie-player.getLottie`); all guarded by feature-detect + try/catch. **Output is LEAN** (§9.4): emit `feel`+`sampled_motion`+`captured_frames` always; `scroll_triggers` only when GSAP is global. |
| STEP 3 | **scroll-hijack-aware** sampling — detect Lenis/Locomotive first; if present, drive the library instance (NOT `window.scrollTo`) + `ScrollTrigger.refresh()`; record opacity/transform/bounds at 0/25/50/75/100% scroll + load t+0/+300/+600ms |
| STEP 4 | expand screenshots → hero viewport, 2–3 section close-ups, nav top-vs-scrolled, 2–4 motion frames (~8–10 total, reference-only) |
| STEP 5 | motion-feel + imagery `visual_description` (vision on screenshots); emit raw airiness/density scores (labels via vision, thresholds provisional per V2) |
| STEP 6 | read `metadata` (favicon/OG/theme-color/manifest from meta/link tags) + bump coverage section count + `coverage.missing` |

---

## §9. Decisions (RESOLVED)

1. **Where does this output go? → Update the extract skill DIRECTLY** (implement the §8 changes in `data.yaml`). No separate `reference-pack/`. Rationale: extract is the single gateway; §6 already co-locates structured YAML + screenshots + prose in one `data.yaml`; a second artifact fragments the source of truth and forces downstream (impeccable) to read two files. Leanness comes from **bounding** each new section (imagery ≤15 samples, motion-feel is a summary, composition is one sequence), not from forking files.
2. **Coverage scope → implement ALL verified sections.** No deferral — token-tier (§4) ships once grounded. Every new section is bounded by design.
3. **Screenshot budget → ~8–10, reference-only** (copyright-safe). Cheap relative to their signal for a vision-capable downstream.
4. **Motion scope → LEAN contract + opportunistic.**
   - **Always emit:** `feel` + `sampled_motion` + `captured_frames`.
   - **Emit `scroll_triggers` (precise GSAP vars) ONLY when GSAP is global** and `ScrollTrigger.getAll()` makes introspection free; omit otherwise.
   - No information loss on the cheap path; no wasted sampling on the expensive path. (Runtime sampling cost question folded into this — sample only the bounded frame set, not exhaustive.)

---

## §10. Status — what's done / verified / not

| Work item | State | Grounding |
|---|---|---|
| Feedback validated against code (5 pts, §0) | ✅ done | code |
| §3 Motion re-verified + corrected | ✅ done | **grounded** (NotebookLM, 88 sources) |
| §1 Imagery | ✅ done | **grounded** (V1, ~85 sources) → [research/V1-imagery.md] |
| §2 Page composition | ✅ done | **grounded** (V2, ~50 effective / 181 imported) → [research/V2-composition.md] |
| §4 Token-tier / themes | ✅ done | **grounded** (V5, ~108 sources) → [research/V5-token-tiers.md] |
| §5 Screenshot strategy | ⚠️ drafted | reasoning (cross-cutting, low-risk) |
| Completeness audit (any missing dimension?) | ✅ done | **grounded** (V4, ~60–80 unique / 118 imported) → §11 |
| Skill implementation (SKILL.md + steps + output-format) | ❌ not started | — |

**Legend:** *grounded* = backed by external sources; *reasoning* = my analysis, may contain wrong claims (motion proved this). The ⚠️ rows for §1/§2/§4 are now lifted to ✅ grounded via the V1/V2/V5 deep-research runs; §5 stays reasoning (cross-cutting strategy, not a detection-method claim).

---

## §11. Completeness audit — is every design dimension covered?

**✅ VERIFIED via V4 deep research** (~60–80 unique sources / 118 imported). The audit is no longer reasoning — V4 confirmed it against W3C Design Tokens, design-reference/moodboard tools, and design-to-code extractors.

**Verdict: PARTIAL.** The 13-dimension map below covers **Foundations + Componentry** well, but is **not exhaustive for *recreation*** — V4 surfaced recreation-only dimensions a visual audit omits (see "New dimensions" below).

Full dimension map of "what makes a reference site look the way it does":

| # | Dimension | Extract now | After proposal | Still missing? |
|---|---|---|---|---|
| 1 | Color palette + usage | strong | + multi-theme (§4) | dark-mode sets |
| 2 | Typography (fonts/weights/sizes) | strong | + named scale/ratio | type scale as tokens |
| 3 | Spacing system | strong | — | — |
| 4 | Layout grid (container/cols/breakpoints) | metrics | + composition (§2) | reflow behavior (B) |
| 5 | Components + states | strong | — | press/active/modal (C) |
| 6 | Shadows/elevation | strong | + named tiers | — |
| 7 | Borders/radius | strong | — | — |
| 8 | Motion | partial | verified (§3) | — |
| 9 | Imagery style/treatment | icons only | §1 | — |
| 10 | Icons | ok | — | — |
| 11 | Loading/feedback/forms/a11y | strong | — | — |
| 12 | Psychology/brand | present | — | — |
| 13 | CSS custom properties | present | + tier classification (§4) | semantic tiers |

**Gap verdicts (VERIFIED via V4):**

| Gap | V4 verdict | Action |
|---|---|---|
| **A. Logo / wordmark treatment** | **NOT a real standard gap.** Standard completeness checklists do not require it; only individual design systems (e.g. GitLab Pajamas) document lockup rules. | **DOWNGRADE to optional/bonus** — not a required dimension. |
| **B. Responsive reflow behavior** | **REAL gap.** Canonical "Breakpoints & Adaptation" explicitly requires "Layout configuration maps" specifying when multi-column elements stack; breakpoints alone are insufficient. | **KEEP and promote.** |
| **C. Interaction states beyond hover/focus** | **PARTIAL.** Standard requires active/disabled/error states + keyboard-focus order; custom cursor / scroll-snap / modal-drawer are NOT named by the standard. | Capture the **standard subset** (active/disabled/error + keyboard-focus) — mostly overlaps existing "components + states". Custom cursor/scroll-snap/modal = **optional, out of scope** for completeness. |
| **D. Voice / copy style** | **Content, not visual design** — correctly excluded from a *visual* audit, but it is the **#1 recreation-only dimension**. | **Champ's judgment call** — flag clearly; default exclude from extract (visual), acknowledge as recreation gap. |
| E. Information-hierarchy depth | partly in §2 | make explicit in §2 (section_sequence + heading depth). |

**New dimensions V4 surfaced — DISPOSITION DECIDED (visual-only scope, §8):**

| # | Dimension | Disposition | Reason |
|---|---|---|---|
| 1 | IA / sequencing | **Already covered** — §2 `section_sequence` | not new |
| 2 | Dynamic slots / data-binding | **Excluded** | functional/implementation, not visual |
| 3 | Asset / SVG performance | **Excluded** | bundling is a perf detail, not look |
| 4 | Metadata / social ("invisible UI") | **Included (small)** — `metadata` section: favicon/OG/theme-color/manifest refs from meta/link tags | cheap DOM read, mild brand value |
| 5 | Voice / copy / tone (= gap D) | **Excluded from structured** — carried by screenshots | content not visual; vision-capable downstream sees it in screenshots (§6) |

Net: extract stays **visual-only** for structured YAML. No V6 needed — these are either covered, non-visual, or screenshot-carried.

---

## §12. Verification status + V3 re-plan

**V1 / V2 / V4 / V5 — ✅ DONE** (NotebookLM deep research, all grounded; findings folded into §1/§2/§4/§11 above, detail files in `research/`).

| # | Status | Result |
|---|---|---|
| V4 completeness | ✅ done | Audit = PARTIAL; A not a gap, B real, C partial, D content; 5 recreation dims surfaced (§11). |
| V1 imagery | ✅ done | Treatment signals computable; duotone = heuristic (no single signal); DOM-vs-visual split; bounded sampling (§1). |
| V2 composition | ✅ done | 7 corrections to draft (hero 80vh not 60vh, logo-strip signal, FAQ 4-layer check, glass = blur+semi-transparent, bento `grid-auto-flow:dense`, nav 200ms wait, AR thresholds provisional) (§2). |
| V5 token-tier | ✅ done | Tier split = convention not spec; W3C has no native multi-theme; spec stable 2025.10; classify via var() DAG (§4). |

**V3 — SKIPPED (decided): dimensions kept, research dropped.**

The original V3 was broad A/B/C detection research. Decision: **skip the research, handle the dimensions directly in §8 design.** Rationale — the fabrication risk that justified V1/V2/V4/V5 (and sank the first motion draft) does **not** apply here:

| Scope | Detection | Fabrication risk | Verdict |
|---|---|---|---|
| Gap A (logo/lockup) | — | — | **Dropped** (not a standard gap, §11). |
| Gap B (responsive reflow) | emulate 3–5 viewports → diff grid/flex/visibility/order per section + nav→hamburger breakpoint | **Low** — deterministic DOM diff, no subjective thresholds | **In §8** (STEP 2 Call 4). No research. |
| Gap C (interaction subset) | `:active`/`:disabled`/`:invalid` rules + `aria-disabled` + focusable tab order | **Very low** — standard pseudo-classes/aria; overlaps existing component states | **In §8** (STEP 2 Call 2). No research. |

Contrast with motion (subjective feel thresholds + hidden `getAnimations()` API → high fabrication risk → research essential). If a specific detection proves ambiguous during skill-writing, do a **targeted** mini-research then (lazy, first-rung-that-holds).

**5 recreation dimensions — DECIDED visual-only** (§11): no V6. extract stays visual; metadata is the only addition (small).

**Research phase: CLOSED.** All detection methods in §1/§2/§3/§4 are grounded; §8 is a complete, decided spec. Next step is implementation (`/skill-creator`), on hold per Champ.

**Operational lesson (for any future research run):** the CLI is `notebooklm` v0.7.2; `jq` is NOT installed in this env (parse JSON with `python3`); delete syntax is `notebooklm delete -n <id> -y` (not `notebooklm notebook delete`); `export NOTEBOOKLM_HOME` does not persist across Bash calls — set it inline per command and pass `-n <id>`/`--notebook <id>` explicitly; deep research jobs may report `failed` status yet still import 80–190 sources (ask against them anyway).
