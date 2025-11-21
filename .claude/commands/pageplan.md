# /pageplan - Page Structure & Content Planning

**Purpose:** Generate a detailed page plan for UI implementation, including component reuse strategy, content draft, and asset checklist.

**Usage:**
```bash
# With context files
/pageplan @proposal.md @prd.md @project_brief.md

# Current change only (uses proposal.md in openspec/changes/)
/pageplan

# Specify change ID
/pageplan landing-page
```

---

## What This Command Does

1. **Reads User-Specified Context:**
   - Only reads files that user mentions with `@` prefix
   - Always reads `openspec/changes/{change-id}/proposal.md` (if exists)
   - **Always reads `design-system/STYLE_TOKENS.json`** (lightweight, ~500 tokens) ✅
   - Validates `design-system/STYLE_GUIDE.md` exists (doesn't load full content)

2. **Searches Existing Components:**
   - Glob: `**/{Navbar,Footer,Sidebar,Header}*.{tsx,jsx,vue}`
   - Grep: Common UI patterns
   - Builds reuse vs new component list

3. **Generates page-plan.md:**
   - Component plan (reuse vs new)
   - Page structure (layout composition)
   - Content draft (AI-generated from PRD)
   - Asset checklist (user must prepare)
   - Rationale (why this structure)

4. **Outputs to:** `openspec/changes/{change-id}/page-plan.md`

---

## Implementation Instructions

### STEP 1: Detect Change Context

```typescript
// Detect current change ID
const changesDir = 'openspec/changes/'
const changeId = detectCurrentChange() // or from command arg

if (!changeId) {
  error("No active change found. Run after OpenSpec generates proposal.md")
  return
}

const outputPath = `openspec/changes/${changeId}/page-plan.md`
```

### STEP 2: Read Context Files

```typescript
// Only read files user specified with @
const userFiles = extractMentionedFiles(userMessage) // @prd.md, @brief.md

// Always read (if exists)
const proposalPath = `openspec/changes/${changeId}/proposal.md`
const tokensPath = `design-system/STYLE_TOKENS.json` // 🆕 Lightweight tokens
const styleGuidePath = `design-system/STYLE_GUIDE.md` // Validate only, don't load

const contextFiles = [
  ...userFiles,
  proposalPath
].filter(fileExists)

// Read all context
let context = contextFiles.map(readFile).join('\n\n---\n\n')

// 🆕 Extract individual content for buyer avatar analysis (STEP 3.5)
let proposalContent = ''
let briefContent = ''
let tasksContent = ''

// Read proposal separately if exists
if (fileExists(proposalPath)) {
  proposalContent = Read(proposalPath)
}

// Read tasks.md if exists (for marketing page detection)
const tasksPath = `openspec/changes/${changeId}/tasks.md`
if (fileExists(tasksPath)) {
  tasksContent = Read(tasksPath)
}

// Extract brief from user files
const briefFile = userFiles.find(f => f.toLowerCase().includes('brief'))
if (briefFile && fileExists(briefFile)) {
  briefContent = Read(briefFile)
}

// 🆕 Load design tokens (lightweight)
if (fileExists(tokensPath)) {
  const tokens = JSON.parse(Read(tokensPath))
  context += `\n\n---\n\n# Design Tokens (STYLE_TOKENS.json)\n\n`
  context += `Primary Color: ${tokens.tokens.colors.primary.DEFAULT}\n`
  context += `Spacing Scale: ${tokens.tokens.spacing.scale.join(', ')}px\n`
  context += `Component Library: ${tokens.component_library.name}\n`
  context += `Shadows: ${Object.keys(tokens.tokens.shadows).join(', ')}\n`
}

// Validate STYLE_GUIDE.md exists (don't load!)
const hasStyleGuide = fileExists(styleGuidePath)
if (!hasStyleGuide) {
  warn(`⚠️ No STYLE_GUIDE.md found - run /designsetup first`)
}

// Total context: ~1.5K tokens (vs 5K+ if loading full STYLE_GUIDE.md)
```

### STEP 3: Search Existing Components

```typescript
// Search for common shared components
const searchPatterns = [
  '**/{Navbar,Navigation}*.{tsx,jsx,vue}',
  '**/{Footer}*.{tsx,jsx,vue}',
  '**/{Sidebar,Drawer}*.{tsx,jsx,vue}',
  '**/{Header}*.{tsx,jsx,vue}',
]

const foundComponents = []
for (const pattern of searchPatterns) {
  const matches = glob(pattern)
  if (matches.length > 0) {
    foundComponents.push({
      name: extractComponentName(matches[0]),
      path: matches[0],
      exports: grepExports(matches[0])
    })
  }
}
```

### STEP 3.5: Buyer Avatar Analysis (NEW - Conversion Optimization)

> **Purpose:** Extract buyer psychology to generate conversion-optimized copy (inspired by Eugene Schwartz framework)

```typescript
// Only analyze if this is a marketing/landing page
const isMarketingPage = tasksContent.toLowerCase().match(/(landing|marketing|homepage|product page|sales)/i)

let buyerAvatar = null

if (isMarketingPage && (proposalContent || briefContent)) {
  output(`
🎯 Detecting marketing page - analyzing buyer psychology...
  `)

  const avatarPrompt = `
You are a conversion copywriter analyzing a product to understand the target buyer.

Context:
${proposalContent || ''}
${briefContent || ''}

Task: Extract buyer psychology using Eugene Schwartz's market awareness framework.

Return JSON:
{
  "demographics": {
    "age_range": "string",
    "job_role": "string",
    "description": "string"
  },
  "psychographics": {
    "top_pain_points": ["string", "string", "string"],
    "secret_desires": "string (what they truly want beyond features)",
    "decision_triggers": "string (what makes them buy NOW)",
    "dominant_emotion": "fear" | "aspiration" | "frustration" | "urgency"
  },
  "market_awareness": "unaware" | "problem_aware" | "solution_aware" | "product_aware" | "most_aware",
  "messaging_tone": "B2B" | "B2C",
  "messaging_strategy": {
    "hero_hook": "string (pain-based headline angle)",
    "value_prop_focus": "string (primary benefit to emphasize)",
    "cta_angle": "string (decision trigger for CTA)"
  }
}

If insufficient context, return { "has_context": false }
  `

  buyerAvatar = await LLM({
    prompt: avatarPrompt,
    response_format: 'json',
    temperature: 0.3
  })

  if (buyerAvatar.has_context === false) {
    warn(`⚠️ Insufficient context for buyer avatar - will generate generic copy`)
    buyerAvatar = null
  } else {
    output(`
✅ Buyer Avatar Analyzed:
   - Pain Points: ${buyerAvatar.psychographics.top_pain_points.slice(0, 2).join(', ')}
   - Market Awareness: ${buyerAvatar.market_awareness}
   - Tone: ${buyerAvatar.messaging_tone}
    `)
  }
} else {
  output(`
ℹ️ Non-marketing page detected - skipping buyer avatar analysis
  `)
}
```

---

### STEP 4: Analyze & Generate Plan (ENHANCED with Conversion Copy)

Based on context + found components + buyer avatar (if available), generate:

```markdown
# Page Plan: [Page Name]
> Generated from: [list of context files]
> Change ID: ${changeId}

## 1. Component Plan

### 🔄 Reuse Components (Found in codebase)
[For each found component]
- **[ComponentName]**
  - Path: \`[path]\`
  - Usage: \`<ComponentName prop="value" />\`
  - Notes: [Any notes about usage]

### ✅ Create New Components

#### Shared Components (reusable across pages)
[Components that will be used in multiple pages]
- **[ComponentName]**
  - Purpose: [description]
  - Will be used in: [list pages]
  - Store at: \`/components/[category]/[ComponentName].tsx\`

#### Page-Specific Components (used only here)
[Components for this page only]
- **[ComponentName]**
  - Purpose: [description]
  - Compose with: [other components]
  - Store at: \`/app/[page]/[ComponentName].tsx\`

## 2. Page Structure

\`\`\`tsx
<Layout>
  <ComponentA />  {/* Reuse */}
  <ComponentB />  {/* New shared */}
  <ComponentC />  {/* New specific */}
</Layout>
\`\`\`

## 2.5. 📐 Layout Wireframe (Visual Blueprint)

> **Purpose:** Visual representation of page layout for user review BEFORE implementation

### Desktop View (>1024px)
\`\`\`
┌────────────────────────────────────────────────────┐
│ [Logo]        [Nav Menu]           [CTA Button]   │  ← Navbar (h-16, sticky)
├────────────────────────────────────────────────────┤
│                                                    │
│                  Hero Section                      │  ← Full viewport (h-screen)
│              [Large Headline]                      │     Background image
│            [Subheadline text]                      │     Centered content
│              [Primary CTA]                         │
│                                                    │
├────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │  Card 1  │  │  Card 2  │  │  Card 3  │        │  ← Feature Grid
│  │  [Icon]  │  │  [Icon]  │  │  [Icon]  │        │     (grid-cols-3, gap-6)
│  │  Title   │  │  Title   │  │  Title   │        │     Container: max-w-7xl
│  │  Desc    │  │  Desc    │  │  Desc    │        │     Padding: py-24
│  └──────────┘  └──────────┘  └──────────┘        │
├────────────────────────────────────────────────────┤
│ [Footer Links]              [Social Icons]        │  ← Footer (h-20)
└────────────────────────────────────────────────────┘
\`\`\`

### Tablet View (768-1023px)
\`\`\`
┌──────────────────────────────┐
│ [Logo]   [Nav]      [☰]     │  ← Navbar (collapsed nav)
├──────────────────────────────┤
│         Hero Section         │  ← h-[600px]
│       [Headline]             │     Same layout, smaller
│       [CTA]                  │
├──────────────────────────────┤
│  ┌──────────┐ ┌──────────┐  │
│  │  Card 1  │ │  Card 2  │  │  ← Feature Grid
│  └──────────┘ └──────────┘  │     (grid-cols-2, gap-4)
│  ┌──────────┐               │
│  │  Card 3  │               │
│  └──────────┘               │
├──────────────────────────────┤
│ Footer (stacked)             │
└──────────────────────────────┘
\`\`\`

### Mobile View (<768px)
\`\`\`
┌────────────────┐
│ [Logo]    [☰] │  ← Navbar (hamburger)
├────────────────┤
│   Hero         │  ← h-[500px]
│  [Headline]    │     Smaller text
│  [CTA]         │     Full-width button
├────────────────┤
│ ┌────────────┐ │
│ │   Card 1   │ │  ← Feature Grid
│ │   [Icon]   │ │     (grid-cols-1, gap-4)
│ │   Title    │ │     Full-width cards
│ └────────────┘ │
│ ┌────────────┐ │
│ │   Card 2   │ │
│ └────────────┘ │
│ ┌────────────┐ │
│ │   Card 3   │ │
│ └────────────┘ │
├────────────────┤
│ Footer         │
│ (stacked)      │
└────────────────┘
\`\`\`

### Spacing & Sizing Details

**Containers:**
- Hero: Full viewport height (h-screen desktop, h-[600px] tablet, h-[500px] mobile)
- Features: max-w-7xl, px-6, py-24 (desktop) → py-16 (tablet) → py-12 (mobile)
- Cards: Equal height, p-6 (desktop) → p-4 (mobile)

**Grid Breakpoints:**
- Desktop (>1024px): 3 columns (grid-cols-3)
- Tablet (768-1023px): 2 columns (grid-cols-2)
- Mobile (<768px): 1 column (grid-cols-1)

**Gaps:**
- Section gaps: gap-24 (desktop) → gap-16 (tablet) → gap-12 (mobile)
- Card gaps: gap-6 (desktop) → gap-4 (mobile)

### Responsive Behavior

| Element | Desktop | Tablet | Mobile |
|---------|---------|--------|--------|
| **Navbar** | Full menu | Collapsed | Hamburger |
| **Hero** | h-screen | h-[600px] | h-[500px] |
| **Feature Grid** | 3 cols | 2 cols | 1 col (stack) |
| **Cards** | Side-by-side | Wrap to 2 cols | Full-width stack |
| **Footer** | Horizontal | Stacked | Stacked |

---

## 2.6. 🎬 Animation Blueprint (Micro-interactions)

> **Purpose:** Define animation strategy BEFORE implementation to ensure consistency and polish
> **Source:** `design-system/STYLE_TOKENS.json` (animation tokens)
> **Philosophy:** Match Flow Engineer Step 3 - Design animations systematically, not randomly

### Animation Principles

**From STYLE_TOKENS.json:**
- **Durations:** 150ms (quick), 300ms (normal), 500ms (slow)
- **Easing:** ease-in-out (default), cubic-bezier for custom
- **Properties:** GPU-accelerated ONLY (transform, opacity) - NOT width, height, top, left
- **Consistency:** Same component type = same animation pattern

---

### Button Animations

#### Primary CTA Button
**Hover State:**
- Properties: `transform` (scale 1.05) + `box-shadow` (md → lg)
- Duration: 150ms (fast, responsive feel)
- Easing: ease-in-out
- Code: `transition-all duration-150 hover:scale-105 hover:shadow-lg`

**Active State:**
- Properties: `transform` (scale 0.95)
- Duration: 100ms (immediate feedback)
- Code: `active:scale-95`

**Loading State:**
- Properties: `opacity` (text → 70%), spinner fade-in
- Duration: 300ms
- Code: `disabled:opacity-70` + spinner component

**Full Example:**
```tsx
<button className="px-6 py-3 bg-primary text-primary-foreground rounded-md
  transition-all duration-150
  hover:scale-105 hover:shadow-lg
  active:scale-95
  disabled:opacity-70">
  Get Started
</button>
```

#### Secondary Button
**Hover State:**
- Properties: `background-color` shift, `border-color` shift
- Duration: 150ms
- Code: `transition-colors duration-150 hover:bg-secondary/80`

---

### Card Animations

#### Feature Card / Product Card
**Hover State:**
- Properties: `box-shadow` elevation (sm → xl)
- Duration: 300ms (smooth, elegant)
- Easing: ease-in-out
- Code: `transition-shadow duration-300 hover:shadow-xl`

**Border Glow (Optional):**
- Properties: `border-color` subtle shift
- Duration: 300ms
- Code: `hover:border-primary/50`

**Full Example:**
```tsx
<div className="p-6 bg-card border border-border rounded-lg
  transition-shadow duration-300
  hover:shadow-xl hover:border-primary/50">
  {/* Card content */}
</div>
```

#### Interactive Card (Clickable)
**Hover State:**
- Same as feature card + cursor pointer
- Code: `cursor-pointer transition-shadow duration-300 hover:shadow-xl`

**Active State:**
- Properties: `transform` (scale 0.98) - subtle press feedback
- Duration: 100ms
- Code: `active:scale-98`

---

### Input & Form Animations

#### Text Input / Select / Combobox
**Focus State:**
- Properties: `box-shadow` (ring-2 appears), `border-color` shift
- Duration: 200ms (balanced - not too fast, not slow)
- Easing: ease-in-out
- Code: `transition-all duration-200 focus:ring-2 focus:ring-primary focus:border-primary`

**Error State:**
- Properties: `border-color` (→ destructive), optional shake
- Duration: 300ms
- Code: `border-destructive` (static) or `animate-shake` (if shake defined)

**Full Example:**
```tsx
<input className="w-full px-3 py-2 border border-input rounded-md
  transition-all duration-200
  focus:ring-2 focus:ring-primary focus:border-primary
  placeholder:text-muted-foreground" />
```

---

### Navigation Animations

#### Desktop Menu Hover
**Menu Item Hover:**
- Properties: `background-color` subtle shift
- Duration: 150ms
- Code: `transition-colors duration-150 hover:bg-accent`

#### Mobile Menu (Slide-in)
**Hamburger → Sidebar:**
- Properties: `transform` (translateX -100% → 0)
- Duration: 300ms
- Easing: cubic-bezier(0.4, 0, 0.2, 1)
- Library: Framer Motion or Tailwind transition

**Example (Framer Motion):**
```tsx
<motion.div
  initial={{ x: "-100%" }}
  animate={{ x: 0 }}
  exit={{ x: "-100%" }}
  transition={{ duration: 0.3, ease: [0.4, 0, 0.2, 1] }}>
  {/* Sidebar content */}
</motion.div>
```

---

### Icon Animations

#### Chevron / Arrow (Dropdown)
**Expand/Collapse:**
- Properties: `transform` (rotate 0deg → 180deg)
- Duration: 200ms
- Code: `transition-transform duration-200 [data-state=open]:rotate-180`

#### Loading Spinner
**Continuous Rotation:**
- Properties: `transform` (rotate 360deg)
- Duration: 1000ms (1s per rotation)
- Easing: linear (consistent speed)
- Code: `animate-spin` (Tailwind utility)

---

### Modal / Dialog Animations

#### Modal Entrance
**Background Overlay:**
- Properties: `opacity` (0 → 100%)
- Duration: 200ms
- Code: `transition-opacity duration-200`

**Dialog Content:**
- Properties: `opacity` + `transform` (scale 0.95 → 1)
- Duration: 300ms
- Easing: ease-in-out
- Library: Framer Motion or Radix UI (built-in)

---

### Performance Rules (CRITICAL!)

**✅ DO USE (GPU-accelerated):**
- `transform` (translate, scale, rotate)
- `opacity`
- `filter` (blur, brightness)

**❌ DON'T USE (CPU-intensive, causes reflow):**
- `width`, `height` (causes layout recalculation)
- `top`, `left`, `margin` (use `transform` instead)
- `font-size` (causes text reflow)

**Example:**
```tsx
// ❌ WRONG (causes reflow)
className="hover:w-full hover:h-auto"

// ✅ CORRECT (GPU-accelerated)
className="hover:scale-105 transform"
```

---

### Animation Consistency Checklist

**Before implementing components:**
- [ ] All buttons use scale + shadow pattern (150ms)
- [ ] All cards use shadow elevation pattern (300ms)
- [ ] All inputs use ring pattern (200ms)
- [ ] All durations from STYLE_TOKENS.json (150/300/500ms)
- [ ] All properties GPU-accelerated (transform, opacity)
- [ ] No random durations (e.g., 200ms, 400ms) unless intentional
- [ ] Tested on mobile (animations not janky)

---

### Design Rationale

**Why these patterns?**
1. **Scale + Shadow (Buttons):** Creates depth, signals interactivity
2. **Shadow Elevation (Cards):** Subtle, elegant, matches Material Design
3. **Ring (Inputs):** Clear focus indicator, accessibility compliant
4. **Short Durations (150-300ms):** Feels responsive, not sluggish
5. **GPU Properties:** 60fps smooth animations, no jank

**Inspiration:** Based on extracted animations from reference sites + STYLE_TOKENS.json

---

## 3. 🎯 Target Audience & Conversion Strategy (if marketing page)

${buyerAvatar ? `
> **Auto-generated from buyer avatar analysis (Eugene Schwartz framework)**

### Buyer Profile

**Demographics:**
- Age Range: ${buyerAvatar.demographics.age_range}
- Job Role: ${buyerAvatar.demographics.job_role}
- Description: ${buyerAvatar.demographics.description}

**Psychographics:**
- **Top Pain Points:**
  ${buyerAvatar.psychographics.top_pain_points.map(p => `- ${p}`).join('\n  ')}
- **Secret Desires:** ${buyerAvatar.psychographics.secret_desires}
- **Decision Triggers:** ${buyerAvatar.psychographics.decision_triggers}
- **Dominant Emotion:** ${buyerAvatar.psychographics.dominant_emotion}

**Market Awareness:** ${buyerAvatar.market_awareness}
- Messaging should be: ${getAwarenessGuidance(buyerAvatar.market_awareness)}

**Messaging Tone:** ${buyerAvatar.messaging_tone} ${buyerAvatar.messaging_tone === 'B2B' ? '(Logic + ROI + Authority)' : '(Emotion + Transformation + Identity)'}

---

### Conversion Framework

**Hero Section Strategy:**
- **Hook Angle:** ${buyerAvatar.messaging_strategy.hero_hook}
- **Value Prop Focus:** ${buyerAvatar.messaging_strategy.value_prop_focus}
- **CTA Angle:** ${buyerAvatar.messaging_strategy.cta_angle}

**Content Guidelines:**
- Lead with pain point (not features)
- Feature → Benefit → Emotional payoff translation
- Use ${buyerAvatar.psychographics.dominant_emotion}-based triggers
- Social proof with specific results (not generic testimonials)

---
` : `
> Skipped (non-marketing page)

`}

## 4. 📦 Assets to Prepare (Performance-Optimized)

> **Performance Note:** Follow image optimization best practices for faster load times and better SEO.
> See: `.claude/contexts/patterns/performance-optimization.md`

### Images (Apply Performance Checklist)

**For each image, provide:**

- [ ] **filename.webp** (1920x1080)
      → **Source:** filename.jpg (compress to WebP, quality 85%)
      → **Responsive sizes:** 768w, 1024w, 1920w (generate 3 sizes for responsive)
      → **Loading strategy:**
         - `loading="lazy"` (if below fold - most images)
         - `loading="eager"` (if hero/above fold - rare)
      → **Alt text:** Descriptive alt text for accessibility
      → **Place at:** `/public/images/`
      → **Purpose:** [description - where used on page]
      → **Estimated size:** ~80KB WebP (was ~450KB JPEG) = **-82% reduction**
      → **LCP impact:** Hero images affect LCP score - optimize first!

**Example:**
```
- [ ] **hero-background.webp** (1920x1080)
      → Source: hero-background.jpg (compress via TinyPNG/Squoosh)
      → Sizes: hero-768.webp, hero-1024.webp, hero-1920.webp
      → Loading: eager (hero image, above fold)
      → Alt: "Students taking TOEIC exam in modern classroom"
      → Place: /public/images/
      → Purpose: Hero section background
      → Size: 85KB WebP (was 520KB JPEG) = -84%
```

### Icons

**Preferred format:** SVG (scalable, tiny file size)

- [ ] **[icon-name].svg** (24x24 viewBox)
      → **Format:** SVG (preferred) or PNG sprite (if 10+ icons)
      → **Optimization:** Remove unnecessary metadata (use SVGO)
      → **Place at:** `/public/icons/` or inline in component
      → **Style:** Match STYLE_GUIDE colors
      → **Estimated size:** 1-3KB per icon

**If using 10+ icons:** Consider SVG sprite sheet (combine → 1 HTTP request)

### Other Assets
- [ ] **Fonts:** Use `font-display: swap` to prevent FOIT (Flash of Invisible Text)
- [ ] **Videos:** Use lazy loading, provide poster image
- [ ] **Third-party scripts:** Load async/defer when possible

---

## 5. 📝 Content Draft (${buyerAvatar ? 'Conversion-Optimized' : 'AI-Generated'})

${buyerAvatar ? `
> **Generated using buyer avatar insights for conversion optimization**

### Hero Section

**Headline (Pain Hook):**
"[${buyerAvatar.messaging_strategy.hero_hook}]"

_Strategy: Lead with biggest pain point from avatar analysis_
_Length: 8-12 words, emotional trigger: ${buyerAvatar.psychographics.dominant_emotion}_

**Subheadline (Promise + Benefit):**
"[Focus on ${buyerAvatar.messaging_strategy.value_prop_focus}]"

_Strategy: Concrete benefit + emotional payoff_
_Length: 15-25 words_

**CTA (Decision Trigger):**
"[${buyerAvatar.messaging_strategy.cta_angle}]"

_Strategy: Action verb + outcome/time-based urgency_
_Example: "See Results in 5 Minutes" or "Start Your Free Trial"_

---

### Value Proposition Section

**How to Structure:**
For each feature, translate to buyer language:

**Feature 1: [Technical feature name]**
- **What User Gets:** [Practical benefit]
- **Emotional Payoff:** [How it makes them feel - addresses pain point: ${buyerAvatar.psychographics.top_pain_points[0]}]
- **Copy:** "[Benefit-first description, NOT feature dump]"

**Example:**
❌ Bad: "Advanced analytics dashboard with real-time data"
✅ Good: "See exactly where projects are stuck—before your boss asks" (addresses pain: missed deadlines)

---

### Social Proof & Trust Section

**Strategy:** Use ${buyerAvatar.messaging_tone === 'B2B' ? 'logic-based proof (ROI, case studies, metrics)' : 'emotional proof (transformations, identity, belonging)'}

**Testimonial Template:**
- Before state (pain point): "${buyerAvatar.psychographics.top_pain_points[0]}"
- After state (resolution): "[Specific result]"
- Attribution: [Name, Company/Role]

**Risk Reversal:**
- Address objection: "${buyerAvatar.psychographics.decision_triggers}"
- Offer: [Free trial / Money-back guarantee / No credit card required]

---

### Call-to-Action (Final)

**CTA Copy:** "[Repeat hero CTA or variation]"
**Supporting Text:** "[Reinforce ${buyerAvatar.messaging_strategy.value_prop_focus}]"
**Urgency (optional):** ${buyerAvatar.psychographics.dominant_emotion === 'urgency' ? '[Add time-based urgency]' : '[Social proof count or limited offer]'}

` : `
> **Standard AI-generated content (non-marketing page)**

### [Section Name]

**[Element Type]:** "[Content]"
_([length] chars - based on [source])_

[Repeat for all content elements]
`}

---

**Instructions for User:**
1. Review content above
2. Edit tone, length, messaging as needed
3. Prepare assets per checklist
4. When ready, run: \`/csetup ${changeId}\`

---

## 6. Design Notes

**Design System Files:**
- Tokens (lightweight): \`design-system/STYLE_TOKENS.json\`
- Full guide (reference): \`design-system/STYLE_GUIDE.md\`

**Key Design Tokens:**
- Primary color: [from STYLE_TOKENS.json]
- Font family: [from STYLE_TOKENS.json]
- Spacing scale: [from STYLE_TOKENS.json]
- Component library: [from STYLE_TOKENS.json]
- Shadows: [from STYLE_TOKENS.json]

**Agent Instructions:**
- uxui-frontend MUST read STYLE_TOKENS.json in STEP 0.5
- Use theme tokens (text-foreground/70), NOT hardcoded colors
- Use spacing scale (p-4, p-6), NOT arbitrary values (p-5)

## 7. Implementation Notes

### Component Imports (Reference)
\`\`\`tsx
// Reuse
[import statements for reused components]

// shadcn/ui or component library
[import statements]

// New (to be created)
[import statements with comments]
\`\`\`

---

## Next Steps
1. ✅ Review & edit content draft
2. ✅ Prepare assets (images, icons)
3. ✅ Run \`/csetup ${changeId}\` when ready
4. ✅ Run \`/cdev ${changeId}\` to implement
```

### STEP 5: Write Output & Report

```typescript
// Write page-plan.md
writeFile(outputPath, pagePlanContent)

// Report to user
console.log(`
✅ Page plan generated!

📄 Output: ${outputPath}

📊 Summary:
- Found components: ${foundComponents.length} (reuse)
- New shared: ${newSharedComponents.length}
- New specific: ${newSpecificComponents.length}
- Assets needed: ${assetsCount}
- Content sections: ${contentSections.length}

📝 Next Steps:
1. Review content in ${outputPath}
2. Edit as needed (tone, messaging)
3. Prepare assets per checklist
4. Run: /csetup ${changeId}
`)
```

---

## Example Scenarios

### Scenario 1: Landing Page (First page)
```bash
User: /pageplan @prd.md @project_brief.md

Result:
- Found components: 0 (empty project)
- New shared: Navbar, Footer (will reuse later)
- New specific: HeroSection, FeatureGrid
- Content: Headlines, descriptions from PRD
```

### Scenario 2: Dashboard (Has existing components)
```bash
User: /pageplan @prd.md

Result:
- Found components: Navbar ✅, Footer ✅
- New shared: Sidebar (for dashboard/profile/admin)
- New specific: DashboardStats, ActivityTimeline
- Content: Dashboard-specific text
```

### Scenario 3: Backend API (No UI)
```bash
User: /pageplan

Result:
- Error: "This change doesn't involve UI work. Skip /pageplan."
- OR: Detect from proposal.md and auto-skip
```

---

## Helper Functions

### getAwarenessGuidance()
```typescript
// Provide messaging guidance based on Eugene Schwartz's market awareness stages
function getAwarenessGuidance(stage: string): string {
  const guidance = {
    'unaware': 'Educate about the problem first (they don\'t know they have it)',
    'problem_aware': 'Agitate the pain, present your solution as THE answer',
    'solution_aware': 'Differentiate - why YOUR solution vs alternatives',
    'product_aware': 'Overcome objections, provide social proof, reduce risk',
    'most_aware': 'Make the offer irresistible, urgency-based CTAs'
  }
  return guidance[stage] || 'Focus on benefits and clear CTAs'
}
```

---

## Error Handling

1. **No change ID found:**
   - Error: "No active change. Run after OpenSpec generates proposal."

2. **No @mentions and no proposal.md:**
   - Error: "No context files provided. Use: /pageplan @prd.md"

3. **No UI work detected:**
   - Warning: "This change appears to be backend/API work. /pageplan is for UI tasks."
   - Ask: "Continue anyway? (Y/N)"

4. **STYLE_GUIDE.md missing:**
   - Warning: "No STYLE_GUIDE.md found. Run /designsetup first for best results."
   - Continue: Use general design principles as fallback

---

## Implementation Priority

**Critical:**
- ✅ Read user-specified files only
- ✅ Search existing components
- ✅ Generate component reuse plan
- ✅ Generate content draft from PRD

**Nice to have:**
- Asset checklist detail level
- Auto-detect UI vs backend tasks
- Suggest component classification

---

## Integration with Multi-Agent Flow

```
tasks.md → /pageplan → page-plan.md → /csetup → /cdev
              ↓            ↓              ↓         ↓
           Search       User review   Phases   uxui-frontend
           components   & edit                  reads plan
                                                 skips search
```

**Agent behavior:**
- `uxui-frontend`: Reads page-plan.md in STEP 0, skips component search (STEP 3)
- `frontend`: May read page-plan.md for component locations
- Other agents: Ignore page-plan.md (not relevant)

---

**END OF COMMAND SPECIFICATION**
