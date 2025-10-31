# Design System Hub

> 🎯 **Purpose**: Design Principal Index - Guide all design decisions with proper context

---

## 🧠 Design Decision Framework

**Before ANY design recommendation, ask:**

1. **What type of decision?**
   - Color/Palette
   - Layout/Spacing
   - Depth/Shadows
   - Typography
   - Component Structure
   - Box Relationships

2. **What context?**
   - Project-specific design tokens (see `@/.claude/contexts/domain/[project]/design-tokens.md`)
   - Universal design principles (this directory)

3. **What's the user goal?**
   - Usability (Can users complete tasks easily?)
   - Accessibility (Can ALL users access content?)
   - Aesthetics (Does it look professional and trustworthy?)

**Then route to:**
- **Color** → See `color-theory.md` for harmony, contrast, accessibility
- **Layout** → See `layout.md` + `box-thinking.md` for structure and flow
- **Depth** → See `shadows.md` for elevation and layering
- **Typography** → See `typography.md` for hierarchy and readability
- **Spacing** → See `spacing.md` for consistent gaps and rhythm
- **Responsive** → See `responsive.md` for behavior across devices
- **Accessibility** → See `accessibility.md` for WCAG compliance

---

## 📦 Box Thinking Framework

**Core Principle:** Every element is a box. Understand box relationships before writing code.

### Box Analysis Method

> "Before building or improving this layout, take a step back and observe **every element on the screen** — navigation, headers, cards, buttons, sidebars, text blocks — everything that occupies space. Imagine **each of them as a box** and describe how they relate to one another: which boxes contain others, how they align, and how space flows between them."

### Box Relationship Patterns

- **Container Boxes**: What contains what (hierarchy)
- **Adjacent Boxes**: Side-by-side relationships
- **Nested Boxes**: Parent-child relationships
- **Space Flow**: How space flows between boxes
- **Alignment Logic**: How boxes position relative to each other

### Box Behavior in Responsive Context

> "Now, describe how this layout behaves when the screen or container changes size. Think in terms of movement, proportion, and flow, not pixels. Which sections move above or below others? Which expand, and which step back?"

**Box Movement Patterns:**
- **Stacking**: Horizontal → Vertical arrangement
- **Merging**: Multiple boxes → Single unified box
- **Prioritizing**: Important boxes maintain prominence
- **Compressing**: Boxes shrink but maintain relationships
- **Reorganizing**: Smart rules for box rearrangement

**See `box-thinking.md` for complete framework.**

---

## 🎨 Universal Design Principles

### Color System

**60-30-10 Rule** (Industry standard for balanced color distribution)
- **60% Dominant**: Neutral colors (backgrounds, text) - Creates calm foundation
- **30% Secondary**: Supporting colors (secondary brand color, muted tones)
- **10% Accent**: Primary brand color for emphasis (CTAs, highlights)

**Color Harmony Types:**
- **Monochromatic**: Variations of single hue (most harmonious)
- **Complementary**: Opposite colors on color wheel (high contrast)
- **Analogous**: Adjacent colors (cohesive, natural)
- **Triadic**: 3 colors evenly spaced (vibrant, balanced)

**Accessibility Requirements:**
- Text on background: Minimum 4.5:1 contrast (WCAG AA)
- Large text (18pt+): Minimum 3:1 contrast
- UI components: Minimum 3:1 contrast

**See `color-theory.md` for complete color system.**

---

### Spacing System

**Base Unit Approach:**
```css
--spacing: 0.25rem;  /* 4px - Base spacing unit */
```

**Scale (Multiples of base):**
- `1x` (0.25rem / 4px) - Tiny gaps
- `2x` (0.5rem / 8px) - Small gaps
- `3x` (0.75rem / 12px) - Medium gaps
- `4x` (1rem / 16px) - Default gaps
- `6x` (1.5rem / 24px) - Large gaps
- `8x` (2rem / 32px) - XL gaps
- `12x` (3rem / 48px) - XXL gaps

**See `spacing.md` for complete spacing system.**

---

### Shadow System

**3-Tier Elevation:**

**Level 1: Subtle** (Cards, Inputs)
```css
--shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
```

**Level 2: Medium** (Dropdowns, Modals)
```css
--shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1),
             0 2px 4px -2px rgb(0 0 0 / 0.1);
```

**Level 3: Large** (Overlays, Popovers)
```css
--shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1),
             0 4px 6px -4px rgb(0 0 0 / 0.1);
```

**See `shadows.md` for complete shadow system.**

---

### Typography Hierarchy

**5-Level System:**

1. **H1** (Display) - 2.5rem (40px) - Hero titles
2. **H2** (Headline) - 2rem (32px) - Section titles
3. **H3** (Title) - 1.5rem (24px) - Subsection titles
4. **Body** (Text) - 1rem (16px) - Paragraphs, content
5. **Small** (Caption) - 0.875rem (14px) - Labels, metadata

**Line Height Rules:**
- Headings: 1.2-1.3 (tight for impact)
- Body text: 1.5-1.6 (comfortable reading)
- Small text: 1.4-1.5 (legible but compact)

**See `typography.md` for complete typography system.**

---

### Responsive Behavior

**3-Tier Breakpoint System:**

```css
/* Mobile-first approach */
--breakpoint-sm: 640px;   /* Tablets */
--breakpoint-md: 768px;   /* Small laptops */
--breakpoint-lg: 1024px;  /* Desktops */
```

**Layout Flow Rules:**
- Mobile (< 640px): Stack all boxes vertically
- Tablet (640-1024px): Partial side-by-side, smart stacking
- Desktop (> 1024px): Full multi-column layouts

**See `responsive.md` for complete responsive patterns.**

---

## 🔍 When to Use Each File

| Need | File | Purpose |
|------|------|---------|
| Choose colors for new feature | `color-theory.md` | Color harmony, contrast, accessibility |
| Set spacing between elements | `spacing.md` | Consistent gaps, rhythm, whitespace |
| Add shadows to cards/modals | `shadows.md` | Elevation, depth, layering |
| Define text hierarchy | `typography.md` | Font sizes, weights, line heights |
| Plan component layout | `layout.md` + `box-thinking.md` | Box structure, alignment |
| Make responsive design | `responsive.md` | Breakpoints, movement patterns |
| Ensure accessibility | `accessibility.md` | WCAG compliance, keyboard nav |

---

## 🎯 Quick Start Checklist

**For every new UI component:**

- [ ] **Box Structure** - Identify all boxes and their relationships
- [ ] **Color** - Apply 60-30-10 rule, check contrast (4.5:1 min)
- [ ] **Spacing** - Use multiples of base unit (0.25rem)
- [ ] **Typography** - Follow 5-level hierarchy
- [ ] **Shadows** - Use 3-tier elevation system
- [ ] **Responsive** - Test all 3 breakpoints (mobile, tablet, desktop)
- [ ] **Accessibility** - Keyboard navigation, screen reader support

---

## 📖 Design System Files

```
design/
├── index.md (this file)      # Design hub and decision framework
├── color-theory.md           # Color harmony, contrast, accessibility
├── spacing.md                # Spacing scale, rhythm, whitespace
├── shadows.md                # 3-tier shadow system
├── typography.md             # Font hierarchy, sizes, weights
├── layout.md                 # Layout patterns, alignment
├── responsive.md             # Breakpoints, responsive behavior
├── box-thinking.md           # Box analysis framework
└── accessibility.md          # WCAG compliance, a11y patterns
```

---

## 🔗 Project-Specific Design

**Universal principles (this directory) + Project tokens (domain folder)**

**Project design tokens go in:**
```
.claude/contexts/domain/[project-name]/design-tokens.md
```

**Example:**
```css
/* domain/ecommerce/design-tokens.md */
--primary: #3B82F6;        /* Blue - Trust */
--secondary: #10B981;      /* Green - Success */
--accent: #F59E0B;         /* Amber - Urgency */
```

**How agents use this:**
1. Load universal principles (design/)
2. Load project tokens (domain/[project]/)
3. Apply principles with project colors

---

**💡 Remember: Think in boxes, design with purpose, implement with consistency!**
