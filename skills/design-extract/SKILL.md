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

## Quick Usage

```bash
/extract https://airbnb.com
/extract https://linear.app
```

## What Gets Extracted

| Category | Details |
|----------|---------|
| Colors | Backgrounds, text, borders with usage context |
| Typography | Fonts, weights, sizes, line heights |
| Spacing | Grid base detection, padding/margin values |
| Components | Buttons, cards, inputs with animations |
| Shadows | Box shadows, elevation levels |
| Animations | @keyframes, transitions, libraries (GSAP/Framer/Lottie), scroll animations |
| Icons | SVG system, icon fonts, sizing patterns |
| Loading | Spinners, skeletons, shimmer from stylesheets |
| Accessibility | Focus states, ARIA, contrast ratios, semantic HTML |
| Forms | Newsletter, search, login form patterns |
| Feedback | Error/success/warning states, toast systems |
| Psychology | Style classification, brand personality tags, emotions, target audience |
| CSS Variables | Custom properties from :root/html/body (design tokens) |

## Output

```
design-system/extracted/{site-name}/
├── data.yaml           # Complete 17-section design data
└── screenshots/
    ├── full-page.png   # Full page capture
    └── component.png   # Key component state (optional)
```

## Workflow

```
1. Open       → agent-browser open URL + scroll (trigger lazy CSS)
2. Extract    → 3 focused JS calls:
                 Call 1: Visual styles (getComputedStyle)
                 Call 2: Stylesheet analysis (document.styleSheets)
                 Call 3: DOM structure (querySelectorAll)
3. Interact   → 1 JS call (toast trigger + hover + focus + contrast)
4. Screenshot → 1 full-page capture
5. Analyze    → AI psychology analysis
6. Generate   → data.yaml with 17 sections
```

**Performance:** 3 focused extract calls give better coverage than 1 mega call because Claude gives full attention to each scope. ~8 tool calls total. Claude writes JS dynamically per site — no hardcoded scripts.

## References

| File | Content |
|------|---------|
| [extraction-steps.md](references/extraction-steps.md) | Step-by-step process |
| [output-format.md](references/output-format.md) | data.yaml schema |
| [style-detection.md](references/style-detection.md) | Design style classification |
| [error-handling.md](references/error-handling.md) | Error handling & fallbacks |

## Next Steps After Extraction

```bash
# Extract more reference sites (optional)
/extract https://linear.app

# Generate final design system
/designsetup @prd.md
# → Merges all extracted data
# → Outputs: design-system/data.yaml
```
