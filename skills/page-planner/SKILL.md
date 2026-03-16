---
name: pageplan
description: >
  Generate page plans for UI — section strategy, content direction, user flow, layout wireframe, and component inventory.
  Make sure to use this skill when the user wants to plan a page before building it.
  Triggers on "/pageplan", "plan page", "วางแผนหน้า", "what should this page have",
  "plan landing page", "plan dashboard", "ออกแบบหน้า", or any request to architect
  a page before implementation. Works with or without design-system/data.yaml.
allowed-tools: Read, Write, Glob, Grep, AskUserQuestion
---

# Page Planner Skill

Plan what a page needs before implementation — decide sections, content direction, user flow, and components based on the specific project context.

## Triggers

- "/pageplan {page-name}"
- "/pageplan {page-name} @extra-context.md"
- "plan landing page for [project]"
- "วางแผนหน้า dashboard"
- "what should the pricing page have?"
- "ออกแบบหน้า checkout"

## Quick Usage

```bash
/pageplan landing-page
/pageplan dashboard @requirements.md
/pageplan checkout
```

## Input

| Source | Path | Required |
|--------|------|----------|
| Page name | From user prompt | Yes |
| Design system | `design-system/data.yaml` | No (auto-read if exists) |
| Extra context | `@files` from user prompt | No |
| Existing components | Codebase scan (auto) | No |
| Extracted sites | `design-system/extracted/*/data.yaml` | No |

If `design-system/data.yaml` exists → auto-read for project context, audience, brand personality, design tokens.
If not found → plan based on user prompt and codebase context. Suggest `/designsetup` for richer output.

## Output

```
design-system/{page-name}/
└── page-plan.md
```

## Workflow

```
STEP 0: Gather Context
  → Read design-system/data.yaml if exists
  → Read @context files if provided
  → Glob design-system/extracted/*/data.yaml for reference site structure
  → Glob codebase for existing components (Navbar, Footer, Button, Card, etc.)
  → Report: data.yaml found (yes/no), N components found, M extracted sites

STEP 1: Understand the Page
  → Analyze: what is this page for? who uses it? what action should they take?
  → Consider project context from data.yaml metadata (audience, brand, industry)
  → If unclear → AskUserQuestion to clarify goal and audience
  → Do NOT follow a generic template — think from this specific context

STEP 2: Generate Page Plan
  → Decide sections based on page goal, audience, and context
  → Plan content direction aligned with brand and audience
  → Map user flow through the page
  → Generate layout wireframe for human review
  → Identify components to reuse vs create
  → Write page-plan.md

STEP 3: Report
  → Display: sections planned, components (reuse vs new), output path
  → Suggest: "Review page-plan.md, then ask an agent to build it"
```

## Output Sections

page-plan.md contains:

### 1. Page Strategy
- Page goal (what should happen when someone visits this page?)
- Target audience (who, what do they need, what concerns do they have?)
- Approach (how does this page achieve its goal for this audience?)

Every decision below flows from this strategy.

### 2. Section Plan (ordered top to bottom)

Decide what sections this specific page needs. Do NOT use a generic template.

Think from the context:
- What does the audience need to see first?
- What builds trust or reduces friction?
- What drives them toward the goal?
- What objections or questions do they have?
- What's the logical flow of information?

For each section:
- Name and purpose (WHY this section exists on THIS page)
- What it must contain
- Recommended approach with reasoning

### 3. Content Direction
- Headline approach per section (pain-point / benefit / curiosity / question — depends on audience awareness level)
- CTA copy direction (what action, what value proposition)
- Tone alignment with brand personality
- Key messages to convey

NOT final copy — direction and reasoning for the copywriter or agent.

### 4. User Flow
- What does the user see first → what do they do → where do they go?
- Click/interaction paths (button → modal → form → success)
- If multi-step: what each step contains and why in that order
- Edge cases: what if they don't convert? what catches them?
- Mobile-specific flow differences if relevant

### 5. Layout Wireframe

ASCII art showing this page's specific layout. Generate based on the sections decided above.

Include Desktop, Tablet, and Mobile views:
- How sections stack and reflow
- Grid columns and breakpoint behavior
- Key element positions (CTA, navigation, sidebar)
- Spacing annotations

Purpose: human reviews and approves the layout before implementation.

### 6. Component Plan
- Reuse: existing components found in codebase with file paths
- New: components to create with suggested file paths and purpose
- For each component: what it contains and how it relates to sections above

## Context-Driven Planning

The key principle: every page is different even if the type is the same.

A landing page for a medical camp for high school students is completely different from a landing page for a B2B SaaS product. The sections, order, content approach, and flow should all reflect the specific context — not a predefined template.

To plan well:
1. Start with WHO visits and WHY
2. Decide WHAT they need to see to take action
3. Arrange sections in the order that builds toward that action
4. Only then think about HOW (layout, components)

Use knowledge of marketing frameworks (AIDA, PAS, storytelling), UX patterns, and industry best practices — but apply them based on context, not by default.

## Error Handling

| Error | Action |
|-------|--------|
| No data.yaml | Continue without design context. Note in report |
| Page name not provided | AskUserQuestion: "What page do you want to plan?" |
| Unclear goal or audience | AskUserQuestion to clarify before planning |

## Integration

```
/extract → /designsetup → /pageplan → build using page-plan.md + data.yaml
                              ↑
                     reads data.yaml automatically
                     (no need to re-attach PRD/brief)
```
