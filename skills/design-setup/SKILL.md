# Design Setup Skill

Interactive design system setup with theme selection and AI recommendations.

## Triggers

- "/designsetup [@context-files...]"
- "setup design system"
- "create design system from extracted sites"
- "สร้าง design system"

## Prerequisites

Must have extracted at least 1 site first:
```bash
/extract https://airbnb.com
```

## Quick Usage

```bash
# With context files
/designsetup @prd.md @project.md

# Without context (interactive mode)
/designsetup
```

## Output Files

| File | Purpose | Audience |
|------|---------|----------|
| `design-system/data.yaml` | Design tokens (~300 lines) | Agents |
| `design-system/README.md` | Human-readable guide (~100 lines) | Humans |
| `design-system/patterns/*.md` | Code patterns | Agents |

## 3-Round Interactive Process

```
Round 1: Style Selection
├── Present extracted styles with Match Scores
├── User selects (or "Mix/Custom" for adjustments)
└── AI calculates fit based on brand personality

Round 2: Animation Selection
├── Show all available animations from references
├── User multi-selects desired patterns
└── Include scroll animations, hover effects

Round 3: Theme & Decorative Direction
├── AI recommends 3-4 themes based on project
├── Each theme has USE and AVOID elements
└── User selects or creates custom theme

Confirmation → Generate Files
```

## What Gets Generated

### data.yaml (For Agents)
- Style classification + feel
- Colors (primary, secondary, semantic)
- Typography (fonts, weights, sizes)
- Spacing (grid base, scale)
- Animations (durations, easing, patterns)
- Theme direction (use/avoid elements)
- Psychology (emotions, target audience)

### README.md (For Humans)
- Overview and characteristics
- Color palette guide
- Typography guide
- Spacing system
- Theme direction
- Critical rules

### patterns/*.md (For Agents)
- `buttons.md` - Button variants and sizes
- `cards.md` - Card variants
- `forms.md` - Form elements
- `scroll-animations.md` - Scroll patterns
- `decorations.md` - Decorative elements

## Detailed Documentation

| Reference | Use When |
|-----------|----------|
| [references/interactive-workflow.md](references/interactive-workflow.md) | Understanding the 3-round loop |
| [references/generation-steps.md](references/generation-steps.md) | File generation process |
| [references/data-yaml-schema.md](references/data-yaml-schema.md) | data.yaml structure |
| [references/error-handling.md](references/error-handling.md) | Handling failures |

## Next Steps After Setup

```bash
# Plan pages (reads data.yaml)
/pageplan @prd.md

# Setup development workflow
/csetup {change-id}

# Start development (agents read data.yaml)
/cdev {change-id}
```
