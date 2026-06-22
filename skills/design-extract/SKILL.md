---
name: extract
description: Extract comprehensive design system data from any website using agent-browser
allowed-tools: Bash(agent-browser:*), Read, Write, Glob
---

# Design Extract Skill

Extract comprehensive design system data from any website.

## Triggers

- "extract design from [URL]"
- "ดึง design จาก [URL]"
- "/extract [URL]"
- "analyze design of [URL]"

## Requirements

- agent-browser CLI (`npm install -g agent-browser && agent-browser install`)
- Uses: `open`, `eval <js>`, `set viewport`, `set media`, `screenshot [selector] [path]`

## Quick Usage

```bash
/extract https://airbnb.com
/extract https://linear.app
```

## What Gets Extracted

Output feeds a **vision-capable downstream** (impeccable): computable facts → structured YAML; holistic look/feel → screenshots + one-line prose.

**Extract for the consumer, not for completeness.** impeccable never reads `data.yaml` mechanically — Claude reads it in the impeccable conversation to author PRODUCT.md (from `psychology`) + DESIGN.md (from tokens). So a **CORE** tier gets full effort (`psychology` + color/type/spacing/components/shadows/radius/`motion.feel`+`libraries`/`page_composition`); a **SUPPLEMENTARY** tier (responsive_reflow, accessibility, metadata, token-tiers, form/feedback/loading, view-transitions, toast-libs) is captured only when it's cheap. Tier table + rationale: [output-format.md](references/output-format.md#section-tiers).

| Category | Details |
|----------|---------|
| Colors | Backgrounds, text, borders + usage; **multi-theme** (light/dark via live toggle) |
| Typography | Fonts, weights, sizes, line heights, **named scale/ratio** |
| Spacing | Grid base detection, padding/margin values |
| Components | Buttons, cards, inputs + **states** (hover/focus/active/disabled/error + keyboard-focus order) |
| Shadows | Box shadows, **named elevation levels** |
| Page composition | **NEW** — section sequence, hero anatomy, nav treatment (transparent→solid) |
| Imagery | **NEW** — medium + treatment (object-fit/aspect/radius/mask/filter/blend/overlay) + visual description |
| Iconography | SVG system, icon fonts, sizing patterns |
| Motion | **Consolidated** — native `getAnimations()` + timeline split, scroll-driven, libraries (GSAP/Framer/Lottie), hijack-aware sampling, grounded feel |
| Responsive reflow | **NEW** — per-section grid/flex/order across 4 viewports + nav→hamburger breakpoint |
| Loading | Spinners, skeletons, shimmer from stylesheets |
| Accessibility | Focus states, ARIA, contrast ratios, semantic HTML |
| Forms | Newsletter, search, login form patterns |
| Feedback | Error/success/warning states, toast systems |
| Metadata | **NEW** — favicon/OG/theme-color/manifest refs (not downloaded) |
| Psychology | Style classification, brand personality, emotions, audience, motion narrative |
| CSS Variables | Custom properties + **tier classification** (primitive/semantic/component via `var()` DAG) |

**Constraint:** descriptions + screenshots only — **no asset download** (images/fonts/videos). Copyright-safe.

## Output

```
design-system/extracted/{site-name}/
├── data.yaml           # Complete 20-section design data
└── screenshots/        # ~8-10 reference-only captures
    ├── full-page.png   # overall composition + color story
    ├── hero.png        # above-the-fold
    ├── section-*.png    # feature/bento + testimonial/CTA close-ups
    ├── nav-top.png / nav-scrolled.png   # if transparent→solid nav
    └── motion-*.png    # hero load t+0/+600ms + mid-scroll frames
```

## Workflow

```
1. Open       → open URL → capture intro motion (getAnimations, BEFORE scroll)
                → multi-theme toggle → scroll to trigger lazy CSS
2. Extract    → 4 focused JS calls:
                 Call 1: Visual styles + imagery (getComputedStyle)
                 Call 2: Stylesheet analysis + component states (document.styleSheets)
                 Call 3: DOM + page composition + motion introspection (querySelectorAll)
                 Call 4: Responsive reflow (set viewport × 4 + diff)
3. Interact   → toast trigger + hover/focus/active + contrast
                + scroll-hijack-aware motion sampling (Lenis/Locomotive-safe)
4. Screenshot → ~8-10 reference captures (hero, sections, nav states, motion frames)
5. Analyze    → vision: psychology + imagery/motion visual descriptions
6. Generate   → data.yaml with 20 sections (+ coverage.missing)
```

**Performance:** focused extract calls give better coverage than 1 mega call — Claude gives full attention to each scope. Claude writes JS dynamically per site — no hardcoded scripts.

**Motion ordering (critical):** intro/load animations are auto-discarded unless `fill:forwards|both` — capture `getAnimations()` in STEP 1 **before** the lazy-scroll pass destroys them.

## References

| File | Content |
|------|---------|
| [extraction-steps.md](references/extraction-steps.md) | Step-by-step process (STEP 0–7) |
| [output-format.md](references/output-format.md) | data.yaml schema (20 sections) |
| [style-detection.md](references/style-detection.md) | Design style classification |
| [error-handling.md](references/error-handling.md) | Error handling & fallbacks |

Detection methods are grounded in research archived under [`archive/`](archive/README.md) (`RESEARCH-completeness.md` + `research/V{1,2,4,5}-*.md`) — provenance only, **not read at runtime**. The `§`-numbers in the reference files are shorthand labels, not pointers to read those files during a run.

## Next Steps After Extraction

extract produces **inspiration/reference** (`data.yaml` + screenshots) from sites you admire — one or many. It is NOT an impeccable input file; it is **conversation material** that impeccable (run inside Claude Code) digests to author its own `PRODUCT.md` + `DESIGN.md`, then builds.

```
1. /extract each reference site   → design-system/extracted/{site}/data.yaml + screenshots/  (repeat for many)
2. Open an impeccable session, hand it the extracted references as inspiration:
     /impeccable init      → reads brand/feel from the references → writes PRODUCT.md
     /impeccable document  → reads tokens (color/type/spacing/components) → writes DESIGN.md (+ sidecar)
3. impeccable builds components / pages from PRODUCT.md + DESIGN.md
```

**Why data.yaml is the right output:** impeccable's `context.mjs` auto-loads only `PRODUCT.md` + `DESIGN.md`. But extract's output is never meant to be auto-loaded — it is read by Claude *in the impeccable conversation* to inform the `init`/`document` authoring. So the rich, computable `data.yaml` (tokens for `document`) + `psychology` block (brand for `init`) + screenshots (visual feel) is exactly the digest source needed. No separate `PRODUCT.md`/`tokens.json` emission required — that authoring is impeccable's job, kept in sync with its own current format rules.
