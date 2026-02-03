# Page Planner Skill

Generate visual page plans for UI implementation - component strategy, layout wireframes, animation blueprints.

## Triggers

- "/pageplan [@context-files...]"
- "plan page layout"
- "create page wireframe"
- "วางแผนหน้าเว็บ"

## Quick Usage

```bash
# With context files
/pageplan @proposal.md @prd.md

# Current change only
/pageplan

# Specify change ID
/pageplan landing-page
```

## What Gets Generated

`openspec/changes/{change-id}/page-plan.md` containing:

| Section | Content |
|---------|---------|
| Component Plan | Reuse vs new components |
| Page Structure | Layout composition (TSX) |
| Layout Wireframe | ASCII art (Desktop/Tablet/Mobile) |
| Animation Blueprint | Hover, focus, transition patterns |
| UI States | Empty, loading, success, error states |
| Asset Checklist | Images, icons to prepare |

## Input Sources

| Source | Purpose |
|--------|---------|
| `@context-files` | User-provided requirements |
| `proposal.md` | Change description |
| `tasks.md` | Page type detection |
| `phases.md` | Phase information |
| `design-system/data.yaml` | Design tokens |

## Workflow

```
1. Detect Change → Find active change or use provided ID
2. Read Context → Load all input sources
3. Search Components → Find existing reusable components
4. Generate Plan → Component plan, wireframes, animations
5. Write Output → page-plan.md
```

## Output Sections

### 1. Component Plan
- Reuse: Found components with paths and usage
- New Shared: Components for multiple pages
- New Specific: Page-only components

### 2. Layout Wireframe
ASCII art for Desktop, Tablet, Mobile views with:
- Container sizes
- Grid breakpoints
- Spacing details

### 3. Animation Blueprint
From data.yaml tokens:
- Button animations (scale + shadow)
- Card animations (shadow elevation)
- Input animations (ring focus)
- Navigation animations
- Performance guidelines

### 4. UI States
For each component:
- Empty state
- Loading state
- Success state
- Error state
- Disabled state

### 5. Asset Checklist
- Images (WebP, responsive sizes)
- Icons (SVG preferred)
- Performance notes

## Detailed Documentation

| Reference | Use When |
|-----------|----------|
| [references/generation-steps.md](references/generation-steps.md) | Full step-by-step process |
| [references/wireframe-patterns.md](references/wireframe-patterns.md) | Layout wireframe examples |
| [references/animation-patterns.md](references/animation-patterns.md) | Animation blueprint guide |
| [templates/page-plan.md](templates/page-plan.md) | Output template |

## Integration

```
/designsetup → /pageplan → /csetup → /cdev
     ↓             ↓           ↓         ↓
 data.yaml    page-plan.md  research  uxui-frontend
              (visual)      checklist  reads both
```

**Separation:**
- `/pageplan` = Visual (layout, components, animations)
- `/csetup` = Research (best practices, content strategy)
