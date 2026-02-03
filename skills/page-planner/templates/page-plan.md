# Page Plan: [Page Name]

> Generated from: [list of context files]
> Change ID: ${changeId}

## 1. Component Plan

### 🔄 Reuse Components (Found in codebase)

[For each found component]
- **[ComponentName]**
  - Path: `[path]`
  - Usage: `<ComponentName prop="value" />`
  - Notes: [Any notes about usage]

### ✅ Create New Components

#### Shared Components (reusable across pages)

[Components that will be used in multiple pages]
- **[ComponentName]**
  - Purpose: [description]
  - Will be used in: [list pages]
  - Store at: `/components/[category]/[ComponentName].tsx`

#### Page-Specific Components (used only here)

[Components for this page only]
- **[ComponentName]**
  - Purpose: [description]
  - Compose with: [other components]
  - Store at: `/app/[page]/[ComponentName].tsx`

---

## 2. Page Structure

```tsx
<Layout>
  <ComponentA />  {/* Reuse */}
  <ComponentB />  {/* New shared */}
  <ComponentC />  {/* New specific */}
</Layout>
```

---

## 2.5. 📐 Layout Wireframe (Visual Blueprint)

> **Purpose:** Visual representation of page layout for user review BEFORE implementation

### Desktop View (>1024px)

```
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
```

### Tablet View (768-1023px)

```
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
```

### Mobile View (<768px)

```
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
```

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

> **Source:** `design-system/data.yaml` (animation tokens)

### Animation Principles

**From data.yaml:**
- **Durations:** 150ms (quick), 300ms (normal), 500ms (slow)
- **Easing:** ease-in-out (default)
- **Properties:** GPU-accelerated ONLY (transform, opacity)

### Button Animations

**Primary CTA:**
- Hover: `transition-all duration-150 hover:scale-105 hover:shadow-lg`
- Active: `active:scale-95`
- Loading: `disabled:opacity-70`

**Secondary:**
- Hover: `transition-colors duration-150 hover:bg-secondary/80`

### Card Animations

**Feature Card:**
- Hover: `transition-shadow duration-300 hover:shadow-xl`
- Border glow (optional): `hover:border-primary/50`

**Interactive Card:**
- Hover + Active: `cursor-pointer transition-shadow duration-300 hover:shadow-xl active:scale-98`

### Input Animations

**Focus:**
- `transition-all duration-200 focus:ring-2 focus:ring-primary focus:border-primary`

### Navigation Animations

**Desktop Menu:**
- `transition-colors duration-150 hover:bg-accent`

**Mobile Sidebar (Framer Motion):**
- Initial: `x: "-100%"`
- Animate: `x: 0`
- Transition: `duration: 0.3, ease: [0.4, 0, 0.2, 1]`

### Performance Guidelines

**GPU-accelerated (preferred):**
- transform, opacity, filter

**Avoid:**
- width, height, top, left, margin

---

## 2.7. 🔄 UI States Definition

### State Categories

| State | When | Visual | Accessibility |
|-------|------|--------|---------------|
| **Empty** | No data exists | Illustration + CTA | `role="status"` |
| **Loading** | Fetching data | Skeleton/Spinner | `aria-busy="true"` |
| **Success** | Action completed | Checkmark + message | `aria-live="polite"` |
| **Error** | Something failed | Error message + retry | `role="alert"` |
| **Disabled** | Not available | Muted + explanation | `aria-disabled="true"` |

### [Component] States

**Empty State:**
- Visual: [description]
- Message: "[friendly message]"
- CTA: [action]

**Loading State:**
- Type: Skeleton / Spinner
- Min duration: 300ms

**Success State:**
- Visual: [checkmark/animation]
- Message: "[confirmation]"
- Auto-dismiss: [yes/no, duration]

**Error State:**
- Visual: [error icon]
- Message: "[specific error]"
- Recovery: [retry action]

**Disabled State:**
- Visual: [muted style]
- Reason: "[why disabled]"

---

## 3. 📦 Assets to Prepare (Performance-Optimized)

### Images

- [ ] **[filename].webp** (1920x1080)
  - Source: [original file]
  - Sizes: 768w, 1024w, 1920w
  - Loading: lazy / eager
  - Alt: "[descriptive text]"
  - Place: /public/images/
  - Purpose: [description]

### Icons

- [ ] **[icon-name].svg** (24x24 viewBox)
  - Format: SVG
  - Optimization: SVGO
  - Place: /public/icons/
  - Style: Match data.yaml colors

---

## 4. Design Notes

**Design System Files:**
- Tokens: `design-system/data.yaml`
- Summary: `design-system/README.md`

**Key Tokens:**
- Primary color: [from data.yaml]
- Font family: [from data.yaml]
- Spacing scale: [from data.yaml]

---

## 5. Implementation Notes

### Component Imports (Reference)

```tsx
// Reuse
[import statements for reused components]

// Component library (shadcn/ui)
[import statements]

// New (to be created)
[import statements with comments]
```

---

## Next Steps

1. ✅ Review layout wireframe & component plan
2. ✅ Prepare assets (images, icons) per checklist
3. ✅ Run `/csetup ${changeId}` for research & content strategy
4. ✅ Run `/cdev ${changeId}` to implement
