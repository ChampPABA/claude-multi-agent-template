# Interactive Workflow (3-Round Loop)

## Overview

The design setup uses a 3-round interactive loop where users can adjust and refine until satisfied (or max 3 rounds reached).

---

## STEP 0: Discovery & Validation

### 0.1: Find Extracted Data

Search for: `design-system/extracted/*/data.yaml`

**If no files found:** Stop with error, instruct to run `/extract` first.

### 0.2: Load Extracted Data

For each extracted site:
1. Extract site name from path
2. Parse YAML content
3. Store in memory (map site name → data)

### 0.3: Load Context Files (Optional)

If user provided `@context-files`:
1. Remove `@` prefix
2. Read file content
3. Store with filename as key

### 0.4: Report Discovery

Display found sites, context files, and start analysis message.

---

## STEP 1: Context Analysis

### 1.1: AI Analysis (if context files provided)

Analyze context files to identify:
- `target_audience`: age_range, demographics, tech_savvy
- `brand_personality`: bold, professional, playful, minimal, technical
- `product_type`: SaaS, E-commerce, Marketing, Internal Tool
- `market_position`: differentiation strategy
- `design_preferences`: any mentioned preferences

### 1.2: Interactive Questions (fallback)

If no context or analysis insufficient, ask:

1. **Product Type**: SaaS Dashboard / E-commerce / Marketing Site / Internal Tool
2. **Target Audience**: Gen Z / Millennials / Enterprise / Developers
3. **Brand Personality** (multi-select): Bold / Professional / Playful / Minimal

---

## STEP 2: Interactive Selection Loop

### 2.1: Style Selection

For each extracted site, display:
```
Option [Letter]: [Style Name] [⭐ RECOMMENDED if highest score]
Source: [site name]
Match Score: [score]%

📝 Characteristics: [list]
🎭 Feel: [description]
🎨 Colors: [primary colors]
🎬 Animations: [available animations]
📜 Scroll Patterns: [patterns]
🖼️ Decorative Elements: [elements]
```

**Match Score Calculation:**
- Base = confidence from extraction
- +15 if brand includes "bold" and style is Neo-Brutalism/Playful
- +15 if brand includes "professional" and style is Minimalist/Modern SaaS
- +15 if brand includes "playful" and style is Playful/Creative
- +15 if brand includes "minimal" and style is Minimalist
- Cap at 100

**User Options:**
- Select A, B, C... → Store as selectedStyle
- Select "Mix/Custom" → Get feedback, increment round, loop back

### 2.2: Animation Selection (Multi-select)

Collect all available animations from extracted sites:
- Animation libraries (GSAP, Framer Motion, etc.)
- Scroll patterns (parallax, fade-in, stacking-cards)
- Component animations (button hover, card hover)

Display numbered list, user selects multiple.

### 2.3: Theme Selection

AI recommends 3-4 themes based on project context:
```
Theme [Letter]: [Name]
📝 Description: [description]
🎭 Feeling: [feeling]
✅ USE: [decorative elements]
❌ AVOID: [elements to avoid]
🎯 Icons: [Lucide suggestions]
💡 Why: [match reason]
```

**User Options:**
- Select A, B, C... → Store theme
- Select "No Theme" → Use abstract/geometric
- Select "Custom" → Input custom theme description

### 2.4: Confirmation

Display summary and ask:
- "Yes, Generate" → Exit loop, proceed to generation
- "Adjust" → Increment round, loop back
- "Start Over" → Reset round to 1, loop back

### 2.5: Max Rounds

After 3 rounds, force decision:
- "Yes" → Generate with current settings
- "Cancel" → Exit without generating

---

## Loop Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     START (Round 1)                          │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  Style Selection → Animation Selection → Theme Selection     │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                       Confirmation                           │
│  ┌─────────┐  ┌─────────┐  ┌─────────────┐                  │
│  │   Yes   │  │ Adjust  │  │ Start Over  │                  │
│  └────┬────┘  └────┬────┘  └──────┬──────┘                  │
│       │            │              │                          │
│       ↓            ↓              ↓                          │
│   Generate     Round++        Round=1                        │
│    Files      (max 3)        (restart)                       │
└─────────────────────────────────────────────────────────────┘
```
