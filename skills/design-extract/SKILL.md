---
name: design-extract
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
| Animations | @keyframes, transitions, hover/focus states |
| Psychology | Style classification, emotions, target audience |

## Output

```
design-system/extracted/{site-name}/
├── data.yaml           # Complete 17-section design data
└── screenshots/
    ├── full-page.png   # Full page capture
    ├── button-0-default.png
    ├── button-0-hover.png
    └── ...
```

## Workflow

```
1. Navigate → Open URL in browser
2. Extract  → CSS data (colors, typography, spacing, components)
3. Capture  → Interactive states (hover, focus screenshots)
4. Analyze  → AI psychology analysis
5. Generate → data.yaml with 17 sections
```

## Detailed Documentation

| Reference | Use When |
|-----------|----------|
| [references/extraction-steps.md](references/extraction-steps.md) | Full step-by-step extraction process |
| [references/output-format.md](references/output-format.md) | data.yaml schema and sections |
| [references/style-detection.md](references/style-detection.md) | Design style classification |
| [references/error-handling.md](references/error-handling.md) | Handling failures gracefully |

## Next Steps After Extraction

```bash
# Extract more reference sites (optional)
/extract https://linear.app

# Generate final design system
/designsetup @prd.md
# → Merges all extracted data
# → Outputs: design-system/data.yaml
```
