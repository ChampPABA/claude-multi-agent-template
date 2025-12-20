# /pageplan - Visual Page Planning

**Purpose:** Generate a visual page plan for UI implementation - component strategy, layout wireframes, animation blueprint, and asset checklist.

> **Note:** Content strategy and conversion copy are handled by `/csetup` (Adaptive Depth Research).
> This command focuses on **visual structure** only.

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
   - Always reads `openspec/changes/{change-id}/tasks.md` (for page type detection)
   - **Always reads `openspec/changes/{change-id}/.claude/phases.md`** (if exists - for phase info) ✅ NEW v2.6.0
   - **Always reads `design-system/data.yaml`** (design tokens + psychology, ~500 tokens) ✅

2. **Searches Existing Components:**
   - Glob: `**/{Navbar,Footer,Sidebar,Header}*.{tsx,jsx,vue}`
   - Grep: Common UI patterns
   - Builds reuse vs new component list

3. **Generates page-plan.md:**
   - Component plan (reuse vs new)
   - Page structure (layout composition)
   - Layout wireframe (ASCII art for Desktop/Tablet/Mobile)
   - Animation blueprint (hover, focus, transition patterns)
   - Asset checklist (images, icons to prepare)

4. **Outputs to:** `openspec/changes/{change-id}/page-plan.md`

> **Content & Conversion Strategy** → Handled by `/csetup` in `research-checklist.md`

---

## Implementation Instructions

### STEP 1: Detect Change Context

1. Determine the change ID:
   - Check if user provided a change ID as command argument
   - If not provided, search for the active change in `openspec/changes/`
   - Look for the most recently modified change directory

**If no change ID found:**
```
❌ No active change found. Run after OpenSpec generates proposal.md
```
→ STOP

2. Set the output path:
   - Output file: `openspec/changes/{changeId}/page-plan.md`

→ Continue to STEP 2

### STEP 2: Read Context Files

1. Extract user-mentioned files:
   - Scan the user message for files mentioned with `@` prefix
   - Example: `@prd.md`, `@brief.md`, `@project_brief.md`
   - Store these as user files list

2. Define required file paths:
   - Proposal: `openspec/changes/{changeId}/proposal.md`
   - Tasks: `openspec/changes/{changeId}/tasks.md`
   - Phases: `openspec/changes/{changeId}/.claude/phases.md`
   - Design tokens: `design-system/data.yaml`

3. Build context files list:
   - Start with user-mentioned files
   - Add proposal.md path
   - Filter to only files that exist on disk

4. Read all context files:
   - Read each file in the context files list
   - Join content with separator: `\n\n---\n\n`
   - Store as base context

5. Read proposal.md separately (if exists):
   - Used for individual analysis later
   - Store as `proposalContent`

6. Read tasks.md (if exists):
   - Used for page type detection (marketing vs dashboard)
   - Store as `tasksContent`

7. Read phases.md (if exists):
   - Check path: `openspec/changes/{changeId}/.claude/phases.md`
   - Store as `phasesContent`

**If phases.md found:**
```
✅ phases.md Found - reading phase information
```
- Search for UI phase keywords: `uxui-frontend`, `frontend-mockup`, `Frontend Mockup`
- Count matches and report: `- UI phases detected: {count}`

**If phases.md NOT found:**
```
ℹ️ phases.md not found - run /csetup first if you want phase-aware planning
```

8. Extract brief content:
   - Search user files for filename containing "brief"
   - If found and exists, read it
   - Store as `briefContent`

9. Load design tokens from data.yaml (if exists):
   - Read `design-system/data.yaml`
   - Parse as YAML
   - Extract key design information:
     - Primary color: `tokens.colors.primary.DEFAULT`
     - Spacing scale: `tokens.spacing.scale` (array)
     - Component library: `component_library.name`
     - Shadows: Object keys from `tokens.shadows`
   - Append to context with header: `# Design Tokens (data.yaml)`
   - Include extracted values in readable format

**If data.yaml NOT found:**
```
⚠️ No data.yaml found - run /designsetup first
```

**Context size estimate:** ~1.5K tokens (data.yaml is lightweight)

→ Continue to STEP 3

### STEP 3: Search Existing Components

1. Define search patterns for common shared components:
   - Navbar/Navigation: `**/{Navbar,Navigation}*.{tsx,jsx,vue}`
   - Footer: `**/{Footer}*.{tsx,jsx,vue}`
   - Sidebar/Drawer: `**/{Sidebar,Drawer}*.{tsx,jsx,vue}`
   - Header: `**/{Header}*.{tsx,jsx,vue}`

2. For each search pattern:
   - Run glob search to find matching files
   - If matches found (length > 0):
     - Extract component name from the first match file path
     - Store component information:
       - `name`: Component name (e.g., "Navbar")
       - `path`: Full file path
       - `exports`: Use grep to find exported functions/components
   - Add to found components list

3. Build the found components list:
   - Each entry contains: name, path, exports
   - This list will be used to generate the "Reuse Components" section

→ Continue to STEP 4

### STEP 4: Analyze & Generate Plan

Based on context + found components, generate:

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
> **Source:** `design-system/data.yaml` (animation tokens)
> **Philosophy:** Match Flow Engineer Step 3 - Design animations systematically, not randomly

### Animation Principles

**From data.yaml:**
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
Primary CTA button should include these Tailwind classes:
- Base styles: `px-6 py-3 bg-primary text-primary-foreground rounded-md`
- Transition: `transition-all duration-150`
- Hover effects: `hover:scale-105 hover:shadow-lg`
- Active state: `active:scale-95`
- Disabled state: `disabled:opacity-70`
- Button text: "Get Started" (or context-appropriate CTA)

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
Feature/product card container should include:
- Base styles: `p-6 bg-card border border-border rounded-lg`
- Transition: `transition-shadow duration-300`
- Hover effects: `hover:shadow-xl hover:border-primary/50`
- Content: Card content elements go inside container

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
Text input field should include:
- Base styles: `w-full px-3 py-2 border border-input rounded-md`
- Transition: `transition-all duration-200`
- Focus effects: `focus:ring-2 focus:ring-primary focus:border-primary`
- Placeholder styling: `placeholder:text-muted-foreground`

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
Mobile sidebar with slide-in animation:
- Component: motion.div wrapper
- Initial state: `x: "-100%"` (off-screen left)
- Animate state: `x: 0` (slide to visible position)
- Exit state: `x: "-100%"` (slide back off-screen)
- Transition settings: `duration: 0.3`, `ease: [0.4, 0, 0.2, 1]`
- Content: Sidebar navigation elements inside wrapper

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

### Performance Guidelines

**GPU-accelerated (preferred):**
- `transform` (translate, scale, rotate)
- `opacity`
- `filter` (blur, brightness)

**Avoid for animations (CPU-intensive):**
- `width`, `height` (causes layout recalculation)
- `top`, `left`, `margin` (use `transform` instead)
- `font-size` (causes text reflow)

**Example:**
Wrong approach (causes reflow):
- Using `className="hover:w-full hover:h-auto"` triggers layout recalculation
- CPU-intensive, janky on mobile

Correct approach (GPU-accelerated):
- Use `className="hover:scale-105 transform"` instead
- Smooth 60fps animations on all devices

---

### Animation Consistency Checklist

**Before implementing components:**
- [ ] All buttons use scale + shadow pattern (150ms)
- [ ] All cards use shadow elevation pattern (300ms)
- [ ] All inputs use ring pattern (200ms)
- [ ] All durations from data.yaml (150/300/500ms)
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

**Inspiration:** Based on extracted animations from reference sites + data.yaml

---

## 2.7. 🔄 UI States Definition

> **Purpose:** Define ALL possible states for each interactive component BEFORE implementation
> **Source:** Based on UX best practices and accessibility requirements
> **Philosophy:** Users should NEVER see a blank screen or unexplained error

### Why Define States Upfront?

1. **Prevents blank screens** - Empty state planned from start
2. **Better UX** - Loading indicators reduce perceived wait time
3. **Accessibility** - Screen readers need proper ARIA attributes
4. **Consistency** - Same state patterns across all components

---

### State Categories

For each interactive component/page section, define:

| State | When | Visual | Accessibility |
|-------|------|--------|---------------|
| **Empty** | No data exists | Illustration + CTA | `role="status"` |
| **Loading** | Fetching data | Skeleton/Spinner | `aria-busy="true"` |
| **Success** | Action completed | Checkmark + message | `aria-live="polite"` |
| **Error** | Something failed | Error message + retry | `role="alert"` |
| **Disabled** | Not available | Muted + explanation | `aria-disabled="true"` |

---

### State Definitions Per Component

#### [Component Name] States

**Empty State:**
- Visual: [Illustration description]
- Message: "[Friendly message explaining empty state]"
- CTA: [Button text and action]
- Example: "No notes yet. Start your first reflection!"

**Loading State:**
- Type: Skeleton / Spinner / Progress bar
- Min duration: 300ms (prevent flash)
- Placement: [Where loading indicator appears]

**Success State:**
- Visual: [Checkmark, animation, color]
- Message: "[Confirmation message]"
- Auto-dismiss: Yes/No (if yes, after X seconds)
- Next action: [Suggested next step]

**Error State:**
- Visual: [Error icon, border color]
- Message: "[Specific error description]"
- Recovery: [Retry button, help text]
- Inline vs Banner: [Where error appears]

**Disabled State:**
- Visual: [Opacity, cursor style]
- Reason: "[Why it's disabled]"
- When enabled: [Condition to enable]

---

### Example: Note List Component

\`\`\`
📝 Note List States:

Empty:
  Visual: Notebook illustration (aria-hidden="true")
  Message: "No reflections yet"
  CTA: "Start Writing" → opens editor

Loading:
  Type: Skeleton (3 note cards)
  Duration: min 300ms
  ARIA: aria-busy="true", aria-label="Loading notes"

Success (after save):
  Visual: Green checkmark toast
  Message: "Note saved!"
  Auto-dismiss: 3 seconds
  ARIA: role="status", aria-live="polite"

Error (failed to load):
  Visual: Red banner at top
  Message: "Unable to load notes. Check your connection."
  CTA: "Retry" button
  ARIA: role="alert"

Disabled (offline mode):
  Visual: Muted colors, no hover effects
  Message: "You're offline. Notes will sync when connected."
\`\`\`

---

### State Checklist

**Before implementing each component:**

- [ ] Empty state has friendly message + CTA
- [ ] Loading uses skeleton (content) or spinner (actions)
- [ ] Loading shows for minimum 300ms
- [ ] Success confirms action clearly
- [ ] Error explains what went wrong
- [ ] Error provides recovery action (retry/help)
- [ ] Disabled explains WHY
- [ ] All states have proper ARIA attributes
- [ ] Transitions between states are smooth (200ms)
- [ ] Reduced motion respected for transitions

---

## 3. 📦 Assets to Prepare (Performance-Optimized)

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
      → **Style:** Match data.yaml colors
      → **Estimated size:** 1-3KB per icon

**If using 10+ icons:** Consider SVG sprite sheet (combine → 1 HTTP request)

### Other Assets
- [ ] **Fonts:** Use `font-display: swap` to prevent FOIT (Flash of Invisible Text)
- [ ] **Videos:** Use lazy loading, provide poster image
- [ ] **Third-party scripts:** Load async/defer when possible

---

## 4. Design Notes

**Design System Files:**
- Tokens + Psychology: \`design-system/data.yaml\` (agent reads this)
- Human summary: \`design-system/README.md\` (for humans)

**Key Design Tokens:**
- Primary color: [from data.yaml]
- Font family: [from data.yaml]
- Spacing scale: [from data.yaml]
- Component library: [from data.yaml]
- Shadows: [from data.yaml]

**Agent Instructions:**
- uxui-frontend reads data.yaml in STEP 0.5
- Use theme tokens (text-foreground/70) for theme-awareness
- Use spacing scale (p-4, p-6) for consistency

## 5. Implementation Notes

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
1. ✅ Review layout wireframe & component plan
2. ✅ Prepare assets (images, icons) per checklist
3. ✅ Run \`/csetup ${changeId}\` for research & content strategy
4. ✅ Run \`/cdev ${changeId}\` to implement
```

### STEP 5: Write Output & Report

1. Write the page plan file:
   - Path: `openspec/changes/{changeId}/page-plan.md`
   - Content: The generated page plan from STEP 4

2. Count summary metrics:
   - Found components: Count of reusable components found
   - New shared components: Count of new shared components to create
   - New specific components: Count of page-specific components to create
   - Assets needed: Count of images/icons in checklist
   - Content sections: Count of content sections generated

3. Report to user:

```
✅ Page plan generated!

📄 Output: openspec/changes/{changeId}/page-plan.md

📊 Summary:
- Found components: {count} (reuse)
- New shared: {count}
- New specific: {count}
- Assets needed: {count}
- Content sections: {count}

📝 Next Steps:
1. Review content in page-plan.md
2. Edit as needed (tone, messaging)
3. Prepare assets per checklist
4. Run: /csetup {changeId}
```

→ Done

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

## Error Handling

1. **No change ID found:**
   - Error: "No active change. Run after OpenSpec generates proposal."

2. **No @mentions and no proposal.md:**
   - Error: "No context files provided. Use: /pageplan @prd.md"

3. **No UI work detected:**
   - Warning: "This change appears to be backend/API work. /pageplan is for UI tasks."
   - Ask: "Continue anyway? (Y/N)"

4. **data.yaml missing:**
   - Warning: "No data.yaml found. Run /designsetup first for best results."
   - Continue: Use general design principles as fallback

---

## Implementation Priority

**Critical:**
- ✅ Read user-specified files only
- ✅ Search existing components
- ✅ Generate component reuse plan
- ✅ Generate layout wireframe
- ✅ Generate animation blueprint

**Nice to have:**
- Asset checklist detail level
- Auto-detect UI vs backend tasks
- Suggest component classification

---

## Integration with Multi-Agent Flow

```
/designsetup → /pageplan → /csetup → /cdev
     ↓             ↓            ↓         ↓
  data.yaml   page-plan.md  research   uxui-frontend
  patterns/     (visual)      -checklist reads both
  README.md                 (content)
```

**Separation of Concerns:**
- `/pageplan` = **Visual** (layout, components, animations, assets)
- `/csetup` = **Research** (best practices, content strategy, UX principles)

**Agent behavior:**
- `uxui-frontend`: Reads page-plan.md (visual) + research-checklist.md (content)
- `frontend`: May read page-plan.md for component locations
- Other agents: Ignore page-plan.md (not relevant)

---

**END OF COMMAND SPECIFICATION**
