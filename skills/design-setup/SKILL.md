---
name: designsetup
description: Interactive design system setup with theme selection and AI recommendations. Use when user wants to create a design system, set up design tokens, generate data.yaml from extracted sites, or says /designsetup. Requires extracted site data from /extract first. Also triggers on "setup design system", "create design system", "สร้าง design system", or any request to merge extracted designs into a unified system.
allowed-tools: Read, Write, Glob, AskUserQuestion
---

# Design Setup Skill

Create a unified design system from extracted site data via 3-round interactive loop.

## Triggers

- "/designsetup [@context-files...]"
- "setup design system"
- "create design system from extracted sites"
- "สร้าง design system"

## Prerequisites

At least 1 extracted site: `design-system/extracted/*/data.yaml`
If none found → stop, instruct user to run `/extract https://site.com` first.

## Quick Usage

```bash
/designsetup @prd.md @project.md    # With context
/designsetup                         # Interactive mode
```

## Input

| Source | Path | Required |
|--------|------|----------|
| Extracted sites | `design-system/extracted/*/data.yaml` | Yes (1+) |
| Context files | `@prd.md`, `@project.md`, etc. | No |
| User decisions | 3 rounds via AskUserQuestion | Yes |

## Output

All files write to `design-system/` at project root (create if not exists):

```
design-system/
├── data.yaml              # ~250 lines, curated design tokens (15 sections)
├── README.md              # ~100 lines, human-readable guide
└── patterns/
    ├── buttons.md         # 80-120 lines, variants + sizes + states
    ├── cards.md           # 80-120 lines, variants + hover effects
    ├── forms.md           # 80-120 lines, inputs + validation states
    ├── decorations.md     # 80-120 lines, theme decorative elements
    └── scroll-animations.md  # ONLY if scroll animations detected
```

Do NOT create files inside `design-system/extracted/` — that directory belongs to `/extract`.

## Workflow

```
STEP 0: Discovery
  → Glob extracted sites, load YAML, load context files
  → Report: found N sites, M context files

STEP 1: Context Analysis
  → With context files: AI infers target audience + desired brand personality
  → Without context: AskUserQuestion (product type, audience, personality)

STEP 2: Interactive Loop (max 3 rounds)
  → Round 1: Style Selection (match score using brand_personality)
  → Round 2: Animation Selection (merged from all sites)
  → Round 3: Theme & Decorative Direction (AI recommends)
  → Confirm → Generate | Adjust → loop | Cancel → exit
  → See references/interactive-workflow.md

STEP 3: Generate Files
  → Map extract fields → curated tokens (see references/extract-mapping.md)
  → Merge multi-site data using primary site strategy
  → Write data.yaml, README.md, patterns/*.md
  → See references/output-schema.md

STEP 4: Final Report
  → Display: files created, style, theme, next steps
```

## Error Handling

| Error | Action |
|-------|--------|
| No extracted data found | Stop. Tell user: run `/extract https://site.com` first |
| User cancels at any point | Stop. Preserve existing extracted data |
| 3 rounds reached without confirm | Force decision: Generate or Cancel |

All other errors (write fails, invalid YAML, missing context files) → handle with standard error recovery. Skip invalid sites, warn, continue with valid ones.

## References

| File | Read When |
|------|-----------|
| [interactive-workflow.md](references/interactive-workflow.md) | Entering STEP 2 (3-round selection loop) |
| [extract-mapping.md](references/extract-mapping.md) | Entering STEP 3 (mapping extract → output) |
| [output-schema.md](references/output-schema.md) | Entering STEP 3 (writing data.yaml) |

## Next Steps After Setup

```bash
/pageplan landing-page    # Plan pages (reads data.yaml automatically)
```
