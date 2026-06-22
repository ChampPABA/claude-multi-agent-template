# Output Format: data.yaml

Schema for the extracted design data. The consumer is **impeccable** — but it never reads this file mechanically. A human hands the extraction to an impeccable session, where **Claude reads it as conversation material** to author two files:

- `psychology` → **`/impeccable init`** authors **PRODUCT.md** (register, brand, audience, why-it-works).
- the design tokens → **`/impeccable document`** authors **DESIGN.md** (colors, typography, elevation, components, motion).

So "good extraction" = "lets impeccable author a sharp PRODUCT.md + DESIGN.md," **not** "all 20 boxes ticked." That single fact sets the priority below.

**The split (every section):** computable CSS/DOM signal → **structured YAML**; holistic look/feel that needs an eye → **screenshot + one-line `visual_description`/`visual_notes`**.

## Section tiers

Spend extraction effort in proportion to what the consumer digests.

**CORE (9) — impeccable eats these directly. Extract thoroughly; this is the point.**

| # | Section | Feeds |
|---|---------|-------|
| 1 | `psychology` (top-level block) | init → PRODUCT.md (brand, register, audience) |
| 2 | `color_palette` | document → DESIGN.md Colors |
| 3 | `typography` | document → DESIGN.md Typography |
| 4 | `spacing_system` | document → DESIGN.md (Overview/Components) |
| 5 | `component_styles` (+ states) | document → DESIGN.md Components |
| 6 | `shadows_elevation` | document → DESIGN.md Elevation |
| 7 | `border_radius` | document → DESIGN.md `rounded` |
| 8 | `motion` (`feel` + `libraries`) | document → DESIGN.md motion guidance |
| 9 | `page_composition` (`section_sequence` + `nav` + `hero`) | craft/brand — "why this site looks different with identical tokens" |

**SUPPLEMENTARY (11) — reference only. Capture if cheap (you're already on the page), never the focus. Fine to leave `detected: false`.**

`border_styles` · `imagery` · `iconography` · `responsive_reflow` · `form_patterns` · `feedback_states` · `loading_states` · `accessibility` · `metadata` · `css_custom_properties` · `screenshots`

> Why supplementary: impeccable recreates these freshly from its own rules — it has its own a11y pass (`harden`/`audit`), its own responsive build, its own form/empty-state handling. The inspiration's exact `responsive_reflow` or `keyboard_focus_order` rarely survives into the consumer's output, so don't burn the extraction budget there.

**Coverage denominator stays 20** (CORE + SUPPLEMENTARY). `screenshots` is always captured (vision needs it). `psychology` is a top-level block, not counted in the 20.

**Signpost the tiers in the emitted file.** Add `# === CORE ===` / `# === SUPPLEMENTARY ===` comment dividers in the output `data.yaml` so the downstream reader (impeccable's Claude) sees at a glance which blocks to digest first. This is intentional and worth the two comment lines.

---

## File structure (read before writing)

`meta`, `psychology`, and **all 20 sections are top-level (root) keys — siblings of each other.** The 2-space indentation in the example fragments below is illustrative YAML only; do **not** nest the sections under `meta` or `psychology`. Correct shape:

```yaml
meta: { ... }
psychology: { ... }
color_palette: { ... }
typography: { ... }
# ...every section a root-level key, no wrapper
```

## File Location

```
design-system/extracted/{site-name}/data.yaml
design-system/extracted/{site-name}/screenshots/   # ~8-10 reference-only images
```

```yaml
# Design Extraction: {siteName}
meta:
  site_name: "airbnb"
  url: "https://airbnb.com"
  extracted_at: "2026-06-22T15:30:00Z"
  extractor_version: "3.1.0"
  coverage: { total_sections: 20, detected_sections: 18, percentage: 90, missing: ["responsive_reflow", "metadata"] }  # missing REQUIRED
```

---

# CORE sections

## psychology — the most important block (→ init / PRODUCT.md)

This is what makes impeccable's PRODUCT.md good instead of generic. Vision-filled from screenshots + the token signal. Be specific and grounded, not adjective-salad.

```yaml
psychology:
  style_classification: "Modern SaaS"        # see style-detection.md
  brand_personality: ["professional", "minimal"]   # bold|professional|playful|minimal|technical|elegant|creative|warm
  emotions_evoked:
    - { emotion: "Trust", reason: "Clean typography and ample whitespace" }
  target_audience:
    primary: { description: "Young professionals", age_range: "25-40", tech_savvy: "high" }
  visual_principles:
    - { name: "Hierarchy", description: "Clear hierarchy through size and weight" }
  why_it_works:
    - "Large hero images create emotional connection"   # → DESIGN.md Do's and Don'ts
  design_philosophy:
    core_belief: "Design should feel human and approachable"
    key_principles: ["Simplicity over complexity"]
  motion_narrative: "Standard-paced, scroll-scrubbed, staggered reveals — calm and premium"  # mirror motion.feel.summary
```

## color_palette (multi-theme) — → DESIGN.md Colors

Multi-theme is **live-site detection** (toggle `[data-theme]`/`.dark`/`prefers-color-scheme`, re-read computed styles, diff). Always emit the default theme; emit `themes` only when a second is found on the page.

```yaml
  color_palette:
    detected: true
    default_theme: "light"
    primary:      [{ hex: "#FF5A5F", rgb: "rgb(255,90,95)", usage: "brand-primary", count: 23 }]
    text_colors:  [{ hex: "#484848", usage: "body-text", count: 156 }]
    border_colors:[{ hex: "#EBEBEB", usage: "divider", count: 45 }]
    themes:                          # ONLY when a second theme detected live
      detection: "data-theme"        # data-theme | class-dark | prefers-color-scheme
      dark: { background: "#0B0B0C", text: "#EDEDED", primary: "#FF5A5F" }
```

## typography (named scale) — → DESIGN.md Typography

```yaml
  typography:
    detected: true
    fonts: ["Circular", "Cereal", "-apple-system"]
    weights: ["400", "500", "600", "700", "800"]      # include odd weights (510/590) if variable
    sizes: ["12px", "14px", "16px", "18px", "22px", "26px", "32px"]
    scale:
      source: "derived"             # tokens (from --text-* vars) | derived
      ratio: 1.25                    # median size_n / size_n-1 when derived
      named: { h1: "32px", h2: "22px", body: "16px", small: "14px" }   # when --text-* vars exist
    h1:   [{ text: "Find places to stay", fontSize: "32px", fontWeight: "800", fontFamily: "Circular, sans-serif" }]
    body: [{ fontSize: "16px", fontWeight: "400", lineHeight: "1.5" }]
```

## spacing_system

```yaml
  spacing_system:
    detected: true
    grid_base: 8                                  # detect 4 vs 8
    common_values: [8, 16, 24, 32, 48, 64]
    paddings: ["8px", "16px", "24px"]
    gaps: ["8px", "16px", "24px"]
```

## component_styles (+ states) — → DESIGN.md Components

States expand to the standard subset: `default`, `hover`, `focus`, `active`, `disabled`, `error`/`invalid`. Capture from stylesheet rules (`:active`/`:disabled`/`:invalid`) + `aria-disabled`/`aria-invalid` + the runtime hover/focus diffs (STEP 3). impeccable's button/card/input authoring leans on these directly.

```yaml
  component_styles:
    detected: true
    buttons:
      - id: "button-0"
        text: "Search"
        backgroundColor: "rgb(255,90,95)"
        color: "rgb(255,255,255)"
        padding: "14px 24px"
        borderRadius: "8px"
        fontSize: "16px"
        fontWeight: "600"
        transition: "all 0.2s ease"
        states:
          hover:    { background: "rgb(230,80,85)", boxShadow: "0 2px 8px rgba(255,90,95,0.3)" }
          focus:    { outline: "2px solid #0070F3", outlineOffset: "2px" }
          active:   { transform: "scale(0.98)" }
          disabled: { opacity: "0.5", cursor: "not-allowed", source: "aria-disabled" }
    cards:
      - id: "card-0"
        backgroundColor: "rgb(255,255,255)"
        padding: "16px"
        borderRadius: "12px"
        boxShadow: "0 2px 8px rgba(0,0,0,0.1)"
        states: { hover: { boxShadow: "0 4px 16px rgba(0,0,0,0.15)", transform: "translateY(-2px)" } }
    inputs:
      - id: "input-0"
        type: "text"
        height: "48px"
        borderRadius: "8px"
        border: "1px solid #EBEBEB"
        states: { focus: { border: "1px solid #FF5A5F" }, invalid: { border: "1px solid #ef4444", source: ":invalid" } }
```

## shadows_elevation — → DESIGN.md Elevation

```yaml
  shadows_elevation:
    detected: true
    named:                           # from --shadow-* vars, else infer sm/md/lg by spread
      source: "inferred"            # tokens | inferred
      sm: "0 1px 2px rgba(0,0,0,0.08)"
      md: "0 2px 8px rgba(0,0,0,0.1)"
      lg: "0 8px 28px rgba(0,0,0,0.15)"
    values: ["0 1px 2px rgba(0,0,0,0.08)", "0 4px 16px rgba(0,0,0,0.12)"]   # raw set as found
```

## border_radius — → DESIGN.md `rounded`

```yaml
  border_radius:
    detected: true
    values: ["4px", "8px", "12px", "16px", "24px", "50%"]   # include 9999px pills, 50% circles
```

## motion — `feel` + `libraries` are CORE (→ DESIGN.md motion)

What impeccable needs from motion is narrow: **how it feels** (pacing/easing/choreography) and **what stack produces it** (GSAP? Lenis? Framer?) so it reaches for the same tools. The deep introspection (`native` counts, `runtime.sampled_motion`, `scroll_triggers` vars, `view_transitions`) is recreation-only detail → SUPPLEMENTARY; emit compactly or skip. `feel` is grounded in Apple HIG + Material 3.

```yaml
  motion:
    detected: true
    feel:                               # CORE — the one block impeccable digests
      pacing: "standard"                # 0-120 instant | 120-220 snappy | 220-350 standard | 350-600 deliberate | >600 cinematic
      easing: "emphasized-decelerate"
      choreography: "staggered, 80ms interval"
      scroll_coupling: "scrubbed-to-scroll"   # scrubbed-to-scroll | trigger-once
      cinematic: false
      summary: "Standard-paced, scroll-scrubbed, staggered reveals"
    libraries:                          # CORE — names + load tell impeccable the stack to reach for
      - { name: "gsap",  detected: true, load: "global",  scrolltriggers: 6 }
      - { name: "lenis", detected: true, load: "global" }
    # --- below = SUPPLEMENTARY: emit only if cheap; never block on it ---
    runtime:
      scroll_hijack: { detected: true, library: "lenis", sampling_method: "lenis.scrollTo(immediate)" }
      sampled_motion:                   # opacity/transform diffed across scroll % — reference
        - { selector: "h1.hero-title", scroll_progress: { "0%": { opacity: 0, y: 40 }, "25%": { opacity: 1, y: 0 } }, inferred: "fade-up over first 25%" }
    captured_frames:                    # index into screenshots/ for the motion vision-diff
      - { id: "hero-load", file: "screenshots/motion-hero-0ms.png" }
      - { id: "hero-intro", file: "screenshots/motion-hero-600ms.png" }
```

## page_composition (`section_sequence` + `nav` + `hero`) — → craft/brand

The high-value fields are `section_sequence` (reading-order anatomy) and `nav.behavior` — they capture why two sites with identical tokens look completely different. `layout_metrics` folds in the old `layout_patterns`.

```yaml
  page_composition:
    detected: true
    nav:
      behavior: "transparent-to-solid"   # solid | sticky-solid | transparent | transparent-to-solid | overlay
      backdrop_blur: true
      logo_position: "left"
      mobile_menu: "overlay"
      evidence: { bg_alpha_top: 0.0, bg_alpha_scrolled: 0.95, position: "sticky" }   # sampled scrollY 0 vs 400, 200ms wait
    hero:
      layout: "split"                     # centered | split | full-bleed | stacked
      min_height_vh: 86
      headline_fontsize: "64px"
      cta_count: 2
      background: "image"                 # solid | gradient | image | video | mesh | canvas
    section_sequence:                     # reading order — the high-value field
      - { order: 1, type: "header", note: "sticky nav, transparent over hero" }
      - { order: 2, type: "hero", subtype: "split", note: "left headline+CTA, right product shot" }
      - { order: 3, type: "logo-strip", note: "6 logos, uniform row" }       # grid/flex row 40-120px, high img density, no text
      - { order: 4, type: "feature-grid", note: "3-up icon+title+text" }
      - { order: 5, type: "bento-grid", note: "varying col/row span" }
      - { order: 6, type: "testimonial", note: "quote + avatar + name" }
      - { order: 7, type: "pricing", note: "3 tiers" }
      - { order: 8, type: "faq", note: "accordion" }                          # 4-layer check: <details> | aria-expanded | structural | click-test
      - { order: 9, type: "cta-band" }
      - { order: 10, type: "footer" }
    layout_metrics:
      container_width: "1280px"
      grid_columns: 12
      breakpoints: [{ name: "mobile", max_width: "744px" }, { name: "desktop", min_width: "1128px" }]
    visual_notes:                         # vision-filled; emit raw score, let vision label
      airiness_score: 0.38                # raw whitespace ratio — do NOT hard-bucket
      density_label: "balanced"           # airy | balanced | dense — vision assigns from screenshot
```

---

# SUPPLEMENTARY sections

Compact schema. Capture only what falls out cheaply from passes you're already running. Don't add extraction steps for these.

```yaml
  border_styles:        { detected: true, widths: ["1px", "2px"], colors: ["#EBEBEB", "#DDDDDD"] }

  imagery:              # treatment = computable; visual_description = vision-filled. Sample by role, cap ~12.
    detected: true
    dominant_mediums: ["photography", "svg-illustration"]   # img|svg|video|background-image|canvas|lottie
    images:
      - { role: "hero", medium: "photography",
          treatment: { object_fit: "cover", aspect_ratio: "16/9", full_bleed: true, overlay: "linear-gradient(...rgba(0,0,0,0.5))" },
          visual_description: "editorial lifestyle photo, warm grade, people present" }
    # duotone has no single reliable signal → if claimed, flag inferred: true

  iconography:          { detected: true, system: "inline-svg", count: 24, common_sizes: ["16px","20px","24px"], style: "outline" }
                        # system: inline-svg | icon-font | img-based | sprite

  responsive_reflow:    # mechanical viewport diff; recreation-only for the consumer
    detected: true
    viewports: [375, 768, 1024, 1440]
    nav_collapse_breakpoint: 1024
    sections: [{ id: "feature-grid", reflow: { grid_columns: { "375": 1, "768": 2, "1024": 3 } } }]

  form_patterns:        { detected: true, forms: [{ type: "newsletter", fields: ["email"], layout: "inline" }] }
                        # type: newsletter|login|signup|contact|search ; layout: inline|stacked|grid

  feedback_states:      { detected: true, error: { color: "#ef4444" }, success: { color: "#22c55e" }, warning: { color: "#f59e0b" },
                          toast_pattern: { detected: true, library: "sonner", position: "top-right" } }

  loading_states:       { detected: true, patterns: [{ type: "spinner", keyframe: "spin" }, { type: "skeleton", properties: "shimmer gradient" }] }

  accessibility:        # impeccable runs its own a11y pass — this is reference
    detected: true
    semantic_html: ["nav", "main", "footer", "header", "section"]
    contrast_ratios: [{ pair: "primary-text on background", ratio: 15.3, wcag_aa: true }]

  metadata:             { detected: true, favicon: "present", og_image: "present", theme_color: "#FF5A5F", manifest: "present" }
                        # refs only — never downloaded (no-asset constraint)

  css_custom_properties:
    grouped:            # raw vars by prefix — useful token reference
      colors:  { --color-primary: "#FF5A5F", --color-background: "#ffffff" }
      spacing: { --space-1: "4px", --space-2: "8px" }
      fonts:   { --font-sans: "'Inter', sans-serif" }
    # tier classification (primitive/semantic/component via var() DAG) is a community convention, not W3C —
    # over-engineered for the consumer. Add `tiers` only if explicitly asked; the grouped view is enough.

  screenshots:          # ALWAYS captured — vision references these (see STEP 4)
    detected: true
    files:
      - { id: "full-page", file: "screenshots/full-page.png", shows: "overall composition + color story" }
      - { id: "hero",      file: "screenshots/hero.png",      shows: "above-the-fold" }
      - { id: "nav-top",   file: "screenshots/nav-top.png",   shows: "nav transparent over hero" }      # if transparent-to-solid
      - { id: "nav-scrolled", file: "screenshots/nav-scrolled.png", shows: "nav solid after scroll" }
```

---

## Coverage rules

- `coverage.total_sections` = **20** (CORE 9 + SUPPLEMENTARY 11). `screenshots` always counts as detected; `psychology` is not in the 20.
- A CORE section left `detected: false` is a real miss — re-check before accepting it. A SUPPLEMENTARY `detected: false` is fine.
- `coverage.missing` is **required** — list every undetected section name.
- `coverage.percentage` = `detected_sections / total_sections * 100`.
