# Interactive Workflow (3-Round Loop)

## STEP 0: Discovery

1. Glob `design-system/extracted/*/data.yaml`
   - If empty → stop: "No extracted data. Run `/extract https://site.com` first."
2. Parse each YAML → store as map: `site_name → data`
3. If user provided `@context-files` → read each, store content

Report to user: "Found N extracted sites: [names]. Starting analysis..."

---

## STEP 1: Context Analysis

### With context files

AI analyzes context to identify:

| Field | What to Extract |
|-------|-----------------|
| target_audience | Age range, demographics, tech level |
| desired_brand_personality | Pick 2-4 from: bold, professional, playful, minimal, technical, elegant, creative, warm |
| product_type | SaaS, E-commerce, Marketing, Internal Tool, Portfolio |
| market_position | How product differentiates |

### Without context (fallback)

Ask user via AskUserQuestion:

1. **Product Type**: SaaS / E-commerce / Marketing / Internal Tool / Portfolio
2. **Target Audience**: Developers / Enterprise / Consumers / Gen Z / Mixed
3. **Brand Personality** (pick 2-4): bold / professional / playful / minimal / technical / elegant / creative / warm

---

## STEP 2: Interactive Selection Loop

### 2.1: Style Selection

For each extracted site, calculate Match Score and present:

```
Option [A]: [style_classification] ⭐ RECOMMENDED
Source: [site_name]
Match Score: [score]%
Feel: [design_philosophy.core_belief]
Colors: [top 3 primary hex swatches]
Animations: [library names or "CSS only"]
```

**Match Score Calculation:**

```
base = meta.coverage.percentage (from extract)

For each tag in extract's psychology.brand_personality:
  if tag appears in user's desired_brand_personality → base += 15

Cap at 100
```

Highest score gets ⭐ RECOMMENDED.

**User options:**
- Select A/B/C → store as **primary site**
- "Mix" or "Custom" → get feedback on what to adjust, increment round, loop back

### 2.2: Animation Selection (Multi-select)

Merge animations from ALL extracted sites into one list. Group by category:

| Category | Source |
|----------|--------|
| Libraries | `animations_transitions.libraries[]` from all sites |
| Scroll patterns | `scroll_animations.patterns[]` from all sites |
| Component hovers | `animations.{component}.description` from all sites |
| Keyframes | `animations_transitions.keyframes[].name` from all sites |

Display numbered list with source site noted. User multi-selects.

If no animations found across any site → tell user, skip this round.

### 2.3: Theme & Decorative Direction

AI recommends 3-4 themes based on selected style + context:

```
Theme [A]: [Name]
Description: [what it evokes]
✅ USE: [decorative elements to include]
❌ AVOID: [elements that clash]
Icons: [Lucide icon suggestions]
Why: [why this matches the project]
```

**User options:**
- Select A/B/C → store theme
- "No Theme" → use abstract/geometric defaults
- "Custom" → user describes their own theme direction

### 2.4: Confirmation

Display summary of all selections:
- Style: [name] from [site]
- Animations: [N patterns selected]
- Theme: [name] with USE/AVOID

Ask user:
- **"Generate"** → exit loop, proceed to STEP 3
- **"Adjust"** → increment round, loop back to 2.1
- **"Start Over"** → reset round to 1, loop back

### 2.5: Max Rounds

After 3 rounds without confirming → force decision:
- "Generate" with current selections
- "Cancel" → exit without generating
