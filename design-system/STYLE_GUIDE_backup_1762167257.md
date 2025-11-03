# REDITO Design System - Style Guide (Neo-Brutalism)

> **Source:** Based on MotherDuck Neo-Brutalist design, customized for REDITO
> **Date:** 2025-11-03
> **Design Style:** Neo-Brutalist / Retro Computing - Bold, unapologetic, document-focused
> **Tech Stack:** Universal (Framework-agnostic)
> **Primary Color:** REDITO Golden Yellow (#FFCF32)

---

## Quick Reference

### Most Used Patterns

| Pattern | Code |
|---------|------|
| Primary Button (Yellow) | `className="px-4 py-3 bg-primary text-foreground border-2 border-foreground rounded-[2px] font-normal uppercase text-base hover:shadow-brutal transition-shadow"` |
| Secondary Button (Blue) | `className="px-4 py-3 bg-secondary text-foreground border-2 border-foreground rounded-[2px] font-normal uppercase text-base hover:shadow-brutal transition-shadow"` |
| Card (Brutalist) | `className="p-8 bg-white rounded-[2px] shadow-brutal border-2 border-foreground"` |
| Section Label | `className="text-sm font-normal uppercase tracking-normal text-muted-foreground mb-4"` |
| Heading 1 | `className="text-[72px] leading-[1.2] font-normal uppercase tracking-[1.44px] text-foreground"` |
| Heading 2 | `className="text-[32px] font-normal uppercase text-foreground"` |
| Body Text | `className="text-[15px] leading-[18px] text-black"` |

### Design Tokens Summary

```json
{
  "colors": {
    "primary": "#FFCF32",
    "secondary": "#6FC2FF",
    "background": "#F4EFEA",
    "foreground": "#383838",
    "black": "#000000",
    "white": "#FFFFFF",
    "mutedForeground": "#A1A1A1",
    "border": "#383838",
    "teal": "#53DBC9",
    "lightBlue": "#EBFAFF",
    "lightGreen": "#E8F5E9",
    "lightPurple": "#F7F1FF",
    "lightYellow": "#F9FBE7",
    "lightOrange": "#FFF9E7",
    "red": "#FF7169"
  },
  "spacing": {
    "buttonPadding": "11.5px 18px",
    "xs": "0.25rem",
    "sm": "0.5rem",
    "md": "1rem",
    "lg": "1.5rem",
    "xl": "2rem",
    "2xl": "3rem"
  },
  "typography": {
    "fontFamily": "Noto Sans Thai, sans-serif",
    "fontSize": {
      "xs": "12px",
      "sm": "15px",
      "base": "16px",
      "lg": "18px",
      "xl": "24px",
      "2xl": "32px",
      "h1": "72px"
    },
    "fontWeight": {
      "normal": 400
    },
    "letterSpacing": {
      "h1": "1.44px",
      "button": "0.32px"
    }
  },
  "borderRadius": {
    "minimal": "2px",
    "pill": "50%"
  },
  "shadows": {
    "brutal": "-12px 12px 0 0 rgb(56, 56, 56)"
  }
}
```

---

## Table of Contents

1.  [Overview](#1-overview)
2.  [Design Philosophy](#2-design-philosophy)
3.  [Color Palette](#3-color-palette)
4.  [Typography](#4-typography)
5.  [Spacing System](#5-spacing-system)
6.  [Component Styles](#6-component-styles)
7.  [Shadows & Elevation](#7-shadows--elevation)
8.  [Animations & Transitions](#8-animations--transitions)
9.  [Border Styles](#9-border-styles)
10. [Border Radius](#10-border-radius)
11. [Opacity & Transparency](#11-opacity--transparency)
12. [Z-Index Layers](#12-z-index-layers)
13. [Responsive Breakpoints](#13-responsive-breakpoints)
14. [CSS Variables / Tailwind Theme](#14-css-variables--tailwind-theme)
15. [Layout Patterns](#15-layout-patterns)
16. [Example Component Reference](#16-example-component-reference)
17. [Additional Sections](#17-additional-sections)

---

## 1. Overview

**Summary:**
This design system is based on **Neo-Brutalism** / **Retro Computing** aesthetics, customized for REDITO with golden yellow as the primary brand color. It features bold colors, hard shadows, minimal border radius (2px), and a distinctive brutalist approach to UI design, optimized for Thai language support.

**Key Characteristics:**
- **Neo-Brutalist**: Hard shadows (-12px 12px), sharp 2px borders, bold color blocks
- **Retro Computing**: Minimal styling, functional aesthetic
- **Bold Colors**: Golden Yellow (#FFCF32), Blue (#6FC2FF), Warm beige background (#F4EFEA)
- **Minimal Radius**: Almost all elements use 2px border-radius (barely rounded)
- **Hard Shadows**: Offset shadows instead of soft blur (brutalist style)
- **Functional Typography**: Normal font weight (400), uppercase headings, generous letter-spacing
- **Thai-Optimized**: Noto Sans Thai for perfect Thai character rendering

**Tech Stack:**
- Framework: Universal (React, Vue, Svelte, vanilla HTML)
- Styling: Tailwind CSS recommended (CSS variables provided)
- Font: **Noto Sans Thai** (Google Fonts - optimized for Thai language)
- UI Library: Custom components based on Neo-Brutalism patterns
- Icons: Custom illustrations + standard icon library

**Goals:**
- Stand out from generic SaaS designs with bold, unapologetic aesthetics
- Create memorable brand experience through distinctive brutalist style
- Make document tools feel fresh, modern, and approachable
- Balance playfulness with technical professionalism
- Ensure excellent Thai language readability

---

## 2. Design Philosophy

**Core Principles:**

1. **Neo-Brutalism**
   - **Honest materials**: No gradients, no soft shadows, no unnecessary ornamentation
   - **Bold contrasts**: Strong black borders, hard shadows, vibrant colors
   - **Functional first**: Form follows function, minimal decoration
   - **Anti-polish**: Deliberately rough edges, 2px corners instead of smooth curves

2. **Retro Computing Aesthetic**
   - **Clean typography**: Noto Sans Thai throughout (optimized for Thai)
   - **System colors**: Bright yellow, cyan blue (reminiscent of old CRT monitors)
   - **Functional layout**: Grid-based, structured, no organic shapes
   - **Nostalgic**: Evokes 80s/90s computing without being dated

3. **Clarity Through Contrast**
   - **High contrast**: Dark text (#383838) on light background (#F4EFEA)
   - **Strong borders**: 2px borders define everything clearly
   - **Hard shadows**: Offset shadows create depth without softness
   - **Color blocking**: Bold color fields, no subtle transitions

4. **Playful Professionalism**
   - **Bold colors**: Yellow and blue are energetic but not unprofessional
   - **Serious typography**: Clean font keeps it technical and credible
   - **Balance**: Playful elements don't compromise usability

**Visual Identity:**

REDITO's design rejects the "soft, rounded, gradient-heavy" trend of modern SaaS in favor of **bold, unapologetic brutalism**. This creates instant memorability and positions the product as innovative, confident, and different.

**Key Differentiators:**
- **Hard shadows** instead of soft blur (unique in SaaS)
- **2px border radius** instead of 8-16px (deliberately minimal)
- **Bold color blocks** instead of subtle pastels (confident, energetic)
- **Thai-optimized typography** (Noto Sans Thai)

**User Experience Goals:**
- **First Impression**: "This is completely different - I need to pay attention"
- **During Use**: "This is fast, clear, and surprisingly delightful"
- **Long-term**: "This tool has personality and respects my intelligence"

---

## 3. Color Palette

### Primary Colors

**Primary (REDITO Golden Yellow)**
- **Color**: `#FFCF32` (rgb(255, 207, 50))
- **Usage**: Primary CTAs, highlights, brand moments, accent color
- **Psychology**: Energy, optimism, quality, attention-grabbing
- **CSS Variable**: `var(--color-primary)`
- **Tailwind**: `bg-primary`, `text-primary`, `border-primary`
- **Contrast**: Use dark text (#383838) on yellow backgrounds (AAA rating)

**Secondary (Sky Blue)**
- **Color**: `#6FC2FF` (rgb(111, 194, 255))
- **Usage**: Secondary CTAs, information sections, accents
- **Psychology**: Trust, clarity, data-focused, friendly
- **CSS Variable**: `var(--color-secondary)`
- **Tailwind**: `bg-secondary`, `text-secondary`, `border-secondary`
- **Contrast**: Use dark text (#383838) on blue backgrounds

**Teal (Accent)**
- **Color**: `#53DBC9` (rgb(83, 219, 201))
- **Usage**: Tertiary accents, illustrations, visual variety
- **CSS Variable**: `var(--color-teal)`

---

### Background & Text Colors

**Background (Warm Beige)**
- **Color**: `#F4EFEA` (rgb(244, 239, 234))
- **Usage**: Page background, default background for all pages
- **Rationale**: Softer than white, reduces eye strain, warm and inviting
- **CSS Variable**: `var(--color-background)`
- **Tailwind**: `bg-background`

**Foreground (Dark Gray)**
- **Color**: `#383838` (rgb(56, 56, 56))
- **Usage**: Primary text, borders, UI elements, button borders
- **CSS Variable**: `var(--color-foreground)`
- **Tailwind**: `text-foreground`, `border-foreground`

**Black**
- **Color**: `#000000` (rgb(0, 0, 0))
- **Usage**: Body text, high-emphasis text
- **CSS Variable**: `var(--color-black)`
- **Tailwind**: `text-black`

**White**
- **Color**: `#FFFFFF` (rgb(255, 255, 255))
- **Usage**: Card backgrounds, elevated surfaces
- **CSS Variable**: `var(--color-white)`
- **Tailwind**: `bg-white`

**Muted Foreground (Light Gray)**
- **Color**: `#A1A1A1` (rgb(161, 161, 161))
- **Usage**: Secondary text, labels, placeholders, muted elements
- **CSS Variable**: `var(--color-muted-foreground)`
- **Tailwind**: `text-muted-foreground`

---

### Pastel Accent Colors (Background Tints)

These are used for colored background sections with very light tints:

- **Light Blue**: `#EBFAFF` (rgb(235, 250, 255))
- **Light Green**: `#E8F5E9` (rgb(232, 245, 233))
- **Light Purple**: `#F7F1FF` (rgb(247, 241, 255))
- **Light Yellow**: `#F9FBE7` (rgb(249, 251, 231))
- **Light Orange**: `#FFF9E7` (rgb(255, 249, 231))

**Usage**: Section backgrounds, feature cards, visual variety

---

### Functional Colors

**Success (Green)**
- **Color**: `#10B981` (Emerald 500)
- **Usage**: Success messages, positive states
- **Tailwind**: `bg-success`, `text-success`

**Warning (Orange)**
- **Color**: `#F59E0B` (Amber 500)
- **Usage**: Warning messages, caution states
- **Tailwind**: `bg-warning`, `text-warning`

**Error (Red)**
- **Color**: `#FF7169` (rgb(255, 113, 105))
- **Usage**: Error messages, destructive actions
- **Tailwind**: `bg-error`, `text-error`

---

### Color Palette Grid

| Color Name | HEX | RGB | Usage | Tailwind Class |
|------------|-----|-----|-------|----------------|
| Primary (Yellow) | #FFCF32 | rgb(255, 207, 50) | Primary CTAs | `bg-primary` |
| Secondary (Blue) | #6FC2FF | rgb(111, 194, 255) | Secondary CTAs | `bg-secondary` |
| Teal | #53DBC9 | rgb(83, 219, 201) | Accent | `bg-teal` |
| Background | #F4EFEA | rgb(244, 239, 234) | Page background | `bg-background` |
| Foreground | #383838 | rgb(56, 56, 56) | Text, borders | `text-foreground` |
| Black | #000000 | rgb(0, 0, 0) | Body text | `text-black` |
| White | #FFFFFF | rgb(255, 255, 255) | Cards | `bg-white` |
| Muted | #A1A1A1 | rgb(161, 161, 161) | Secondary text | `text-muted-foreground` |
| Red | #FF7169 | rgb(255, 113, 105) | Error states | `bg-error` |

---

### Color Usage Guidelines

**DO:**
- ✅ Use golden yellow (#FFCF32) for primary CTAs
- ✅ Use sky blue (#6FC2FF) for secondary CTAs
- ✅ Use warm beige (#F4EFEA) background instead of white
- ✅ Use dark gray (#383838) for borders and text (not pure black for borders)
- ✅ Use pure black (#000000) for high-emphasis body text
- ✅ Use pastel backgrounds for section variety

**DON'T:**
- ❌ Don't use gradients (not brutalist style)
- ❌ Don't use soft, muted colors (go bold or go home)
- ❌ Don't use pure white background (use warm beige #F4EFEA)
- ❌ Don't use subtle color variations (strong contrast is key)

---

## 4. Typography

### Font Families

**Sans (Primary)**
```css
font-family: "Noto Sans Thai", ui-sans-serif, sans-serif, system-ui;
```
- **Usage**: ALL text (headings, body, UI)
- **Characteristics**: Excellent Thai character support, clean and modern
- **Fallback**: ui-sans-serif, system-ui
- **Loading**: Google Fonts or local font files

**⚠️ Important**: This design uses **Noto Sans Thai** for optimal Thai language support while maintaining the brutalist aesthetic through font-weight and uppercase transformations.

---

### Font Weights

**REDITO uses only ONE font weight:**

| Weight | Value | Usage | Tailwind Class |
|--------|-------|-------|----------------|
| Normal | 400 | Everything (headings, body, buttons, labels) | `font-normal` |

**⚠️ Critical**: Do NOT use bold (700) or semibold (600). REDITO achieves hierarchy through:
- **Size** (72px vs 32px vs 15px)
- **Uppercase** transformation
- **Letter-spacing** (1.44px for H1)
- **Color** (black vs gray)

---

### Text Styles

#### Headings

**H1 - Hero Heading**
```html
<h1 className="text-[72px] leading-[1.2] font-normal uppercase tracking-[1.44px] text-foreground">
  ออกเอกสารถูกต้อง ครบถ้วน
</h1>
```
- **Size**: 72px
- **Line Height**: 1.2 (86.4px)
- **Weight**: Normal (400) - NOT BOLD
- **Transform**: UPPERCASE
- **Letter Spacing**: 1.44px (extra wide)
- **Color**: #383838 (dark gray)
- **Usage**: Page hero sections, main value propositions

**H2 - Section Heading**
```html
<h2 className="text-[32px] font-normal uppercase text-foreground">
  ฟีเจอร์ทั้งหมด
</h2>
```
- **Size**: 32px
- **Weight**: Normal (400) - NOT BOLD
- **Transform**: UPPERCASE
- **Color**: #383838 (dark gray)
- **Usage**: Major section headings

**H3 - Subsection Heading**
```html
<h3 className="text-[24px] font-normal uppercase text-foreground">
  ใบเสนอราคา
</h3>
```
- **Size**: 24px
- **Weight**: Normal (400)
- **Transform**: UPPERCASE or Title Case
- **Usage**: Card titles, feature headings

---

#### Body Text

**Body Text (Default)**
```html
<p className="text-[15px] leading-[18px] text-black">
  ข้อความปกติสำหรับอธิบายรายละเอียด
</p>
```
- **Size**: 15px
- **Line Height**: 18px (tight!)
- **Weight**: Normal (400)
- **Color**: #000000 (pure black)
- **Usage**: Main content, descriptions

**Small Body (Secondary)**
```html
<p className="text-[13px] leading-[16px] text-muted-foreground">
  ข้อมูลเพิ่มเติม
</p>
```
- **Size**: 13px
- **Line Height**: 16px
- **Color**: #A1A1A1 (gray)
- **Usage**: Captions, metadata, secondary information

---

#### Labels & Buttons

**Button Text**
```html
<span className="text-base font-normal uppercase tracking-[0.32px]">
  ลงทะเบียนฟรี
</span>
```
- **Size**: 16px
- **Weight**: Normal (400) - NOT BOLD
- **Transform**: UPPERCASE
- **Letter Spacing**: 0.32px
- **Usage**: Button labels, CTAs

**Section Label**
```html
<span className="text-sm font-normal uppercase text-muted-foreground">
  ฟีเจอร์
</span>
```
- **Size**: 14px (sm)
- **Weight**: Normal (400)
- **Transform**: UPPERCASE
- **Color**: #A1A1A1 (gray)
- **Usage**: Section labels, category tags

---

### Typography Scale

| Name | Size (px) | Line Height | Tailwind | Usage |
|------|-----------|-------------|----------|-------|
| xs | 12 | 14px | `text-xs` | Very small labels |
| sm | 14 | 17px | `text-sm` | Section labels |
| base | 15-16 | 18-19px | `text-[15px]` or `text-base` | Body text |
| lg | 18 | 22px | `text-lg` | Large body |
| xl | 24 | 29px | `text-[24px]` | H3 |
| 2xl | 32 | 38px | `text-[32px]` | H2 |
| h1 | 72 | 86px | `text-[72px]` | H1 |

---

### Typography Best Practices

**DO:**
- ✅ Use font-weight 400 (normal) for EVERYTHING
- ✅ Use UPPERCASE for headings and labels (creates hierarchy)
- ✅ Use Noto Sans Thai for all text (Thai language support)
- ✅ Increase letter-spacing on headings (1.44px for H1, 0.32px for buttons)
- ✅ Use tight line-height (18px for 15px text = 1.2)
- ✅ Use pure black (#000000) for body text
- ✅ Use dark gray (#383838) for headings

**DON'T:**
- ❌ Don't use bold (700) or semibold (600) - hierarchy comes from size
- ❌ Don't use italic (not part of this design system)
- ❌ Don't use relaxed line-height (1.75) - keep it tight (1.2)

---

## 5. Spacing System

### Spacing Scale

REDITO uses **custom spacing** that doesn't strictly follow 4px or 8px grid.

**Button Padding (Extracted from Design):**
- **Primary/Secondary Button**: `11.5px 18px` (vertical: 11.5px, horizontal: 18px)

**Standard Spacing Scale:**

| Token | Value | Pixels | Tailwind | Common Usage |
|-------|-------|--------|----------|--------------|
| xs | 0.25rem | 4px | `p-1`, `m-1`, `gap-1` | Tight spacing |
| sm | 0.5rem | 8px | `p-2`, `m-2`, `gap-2` | Small gaps |
| md | 1rem | 16px | `p-4`, `m-4`, `gap-4` | Default spacing |
| lg | 1.5rem | 24px | `p-6`, `m-6`, `gap-6` | Section spacing |
| xl | 2rem | 32px | `p-8`, `m-8`, `gap-8` | Large spacing |
| 2xl | 3rem | 48px | `p-12`, `m-12`, `gap-12` | Very large spacing |

---

### Application Examples

#### Button Padding

**Primary/Secondary Button (Actual)**
```html
<button className="px-[18px] py-[11.5px]">
  <!-- Exact padding from design -->
</button>
```

**Simplified (Tailwind)**
```html
<button className="px-4 py-3">
  <!-- px-4 = 16px, py-3 = 12px (close approximation) -->
</button>
```

---

## 6. Component Styles

### 6.1 Component Inventory

| Component | Variants | States | Priority | Notes |
|-----------|----------|--------|----------|-------|
| Button | Primary (Yellow), Secondary (Blue), Ghost | default, hover | **Must-use** | Hard borders, minimal radius |
| Card | Brutalist (with shadow) | default, hover | **Must-use** | 2px border, hard shadow |
| Input | Default, Error | default, focus, error | **Must-use** | Minimal styling |
| Badge | Default, Colored | - | Optional | Status indicators |

---

### 6.2 Button Component

#### Variants

**Primary Button (Yellow - Actual Styles)**
```tsx
<button className="px-[18px] py-[11.5px] bg-primary text-foreground border-2 border-foreground rounded-[2px] font-normal uppercase text-base tracking-[0.32px] hover:shadow-brutal transition-shadow">
  ลงทะเบียนฟรี
</button>
```
- **Background**: REDITO Golden yellow (#FFCF32)
- **Text**: Dark gray (#383838)
- **Padding**: 18px horizontal, 11.5px vertical (exact from design)
- **Border**: 2px solid #383838
- **Border Radius**: 2px (minimal)
- **Font**: Normal weight (400), uppercase, 16px, letter-spacing 0.32px
- **Shadow**: None (default) → Hard shadow on hover
- **Usage**: Primary CTAs ("ลงทะเบียนฟรี", "เริ่มใช้งาน")

**Secondary Button (Blue - Actual Styles)**
```tsx
<button className="px-[18px] py-[11.5px] bg-secondary text-foreground border-2 border-foreground rounded-[2px] font-normal uppercase text-base tracking-[0.32px] hover:shadow-brutal transition-shadow">
  เรียนรู้เพิ่มเติม
</button>
```
- **Background**: Sky blue (#6FC2FF)
- **Styling**: Identical to primary, different color
- **Usage**: Secondary CTAs

**Ghost Button (Minimal)**
```tsx
<button className="px-4 py-2 bg-transparent text-foreground rounded-[2px] font-normal uppercase text-base hover:bg-foreground/5 transition-colors">
  ยกเลิก
</button>
```
- **Background**: Transparent
- **Border**: None
- **Usage**: Navigation links, minimal actions

---

#### Button States

| State | Behavior | Implementation |
|-------|----------|----------------|
| Default | No shadow | Base classes |
| Hover | Hard shadow appears | `hover:shadow-brutal` |
| Active | (Same as hover) | - |
| Focus | Outline (accessibility) | `focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-foreground` |
| Disabled | Reduced opacity | `disabled:opacity-50 disabled:cursor-not-allowed` |

---

### 6.3 Card Component

**Brutalist Card (with Hard Shadow)**
```tsx
<div className="p-8 bg-white rounded-[2px] shadow-brutal border-2 border-foreground hover:translate-x-[-4px] hover:translate-y-[-4px] hover:shadow-brutal-lg transition-all">
  <h3 className="text-[24px] font-normal uppercase text-foreground mb-4">
    ใบเสนอราคา
  </h3>
  <p className="text-[15px] leading-[18px] text-black">
    สร้างใบเสนอราคาได้ภายใน 5 นาที
  </p>
</div>
```
- **Background**: White (#FFFFFF)
- **Padding**: 32px all around
- **Border**: 2px solid #383838
- **Border Radius**: 2px (minimal)
- **Shadow**: `-12px 12px 0 0 rgb(56, 56, 56)` (hard, offset shadow)
- **Hover**: Moves slightly (-4px, -4px), shadow increases

---

## 7. Shadows & Elevation

### Shadow Scale (Brutalist Style)

REDITO uses **hard, offset shadows** (NO BLUR) - this is the signature brutalist style.

| Token | CSS Value | Tailwind | Usage |
|-------|-----------|----------|-------|
| None | none | `shadow-none` | Flat elements |
| Brutal (Default) | `-12px 12px 0 0 rgb(56, 56, 56)` | `shadow-brutal` | Cards, buttons (hover) |
| Brutal Large | `-16px 16px 0 0 rgb(56, 56, 56)` | `shadow-brutal-lg` | Emphasized cards (hover) |
| Brutal XL | `-24px 24px 0 0 rgb(56, 56, 56)` | `shadow-brutal-xl` | Modals, large elements |

**Key Characteristics:**
- **No blur**: Third value (blur radius) is always 0
- **Hard edges**: Shadow has sharp, defined borders
- **Offset**: Shadow is positioned bottom-right (-12px left, +12px down)
- **Solid color**: rgb(56, 56, 56) - no opacity, no gradient

---

### Usage Examples

**Card with Hard Shadow**
```html
<div className="shadow-brutal">
  <!-- -12px 12px 0 0 hard shadow -->
</div>
```

**Card Hover Effect (Lifts + Shadow Grows)**
```html
<div className="shadow-brutal hover:translate-x-[-4px] hover:translate-y-[-4px] hover:shadow-brutal-lg transition-all">
  <!-- Shadow grows as card moves up-left -->
</div>
```

---

### Tailwind Config for Hard Shadows

```js
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      boxShadow: {
        'brutal': '-12px 12px 0 0 rgb(56, 56, 56)',
        'brutal-lg': '-16px 16px 0 0 rgb(56, 56, 56)',
        'brutal-xl': '-24px 24px 0 0 rgb(56, 56, 56)',
      }
    }
  }
}
```

---

## 8. Animations & Transitions

### Transition Durations

| Speed | Value | Tailwind | Usage |
|-------|-------|----------|-------|
| Fast | 150ms | `duration-150` | Quick interactions |
| Normal | 200ms | `duration-200` | Default transitions |
| Medium | 300ms | `duration-300` | Shadow changes |

---

### Common Transitions

**Shadow (Button Hover)**
```html
<button className="hover:shadow-brutal transition-shadow duration-200">
  Hover me
</button>
```

**Card Lift + Shadow**
```html
<div className="shadow-brutal hover:translate-x-[-4px] hover:translate-y-[-4px] hover:shadow-brutal-lg transition-all duration-300">
  Card lifts up-left on hover
</div>
```

---

## 9. Border Styles

### Border Widths

| Token | Value | Tailwind | Usage |
|-------|-------|----------|-------|
| Default | 1px | `border` | Subtle borders |
| Emphasis | 2px | `border-2` | Buttons, cards, strong emphasis |

**REDITO uses 2px borders almost everywhere** (buttons, cards, sections).

---

### Border Colors

```html
<!-- Default border (dark gray) -->
<div className="border-2 border-foreground">...</div>

<!-- Black border -->
<div className="border-2 border-black">...</div>
```

---

## 10. Border Radius

### Radius Scale

**REDITO uses MINIMAL border radius:**

| Token | Value | Tailwind | Usage |
|-------|-------|----------|-------|
| Minimal | 2px | `rounded-[2px]` | Everything (buttons, cards, inputs) |
| Pill | 50% | `rounded-full` | Avatars, circular elements only |

**⚠️ Critical**: Do NOT use `rounded-md` (6px) or `rounded-lg` (8px). REDITO uses **2px for almost everything**.

---

### Usage Examples

**Button (2px Radius)**
```html
<button className="rounded-[2px]">
  <!-- Barely rounded -->
</button>
```

**Card (2px Radius)**
```html
<div className="rounded-[2px]">
  <!-- Minimal rounding -->
</div>
```

**Avatar (Full Radius)**
```html
<img className="rounded-full w-12 h-12" src="/avatar.jpg" alt="User" />
```

---

## 11. Opacity & Transparency

### Opacity Scale

| Token | Value | Tailwind | Usage |
|-------|-------|----------|-------|
| 0 | 0 | `opacity-0` | Hidden |
| 50 | 0.5 | `opacity-50` | Disabled states |
| 70 | 0.7 | `opacity-70` | Semi-transparent overlays |
| 100 | 1 | `opacity-100` | Fully visible |

---

## 12. Z-Index Layers

### Z-Index Scale

| Layer | Value | Usage |
|-------|-------|-------|
| Base | 0 | Normal content |
| Dropdown | 10 | Dropdown menus |
| Sticky | 20 | Sticky headers |
| Modal Backdrop | 40 | Modal overlays |
| Modal | 50 | Modal dialogs |
| Toast | 70 | Notifications |

---

## 13. Responsive Breakpoints

### Breakpoint Scale

| Breakpoint | Min Width | Tailwind Prefix | Target Devices |
|------------|-----------|-----------------|----------------|
| xs | 0px | (default) | Mobile (320-639px) |
| sm | 640px | `sm:` | Mobile landscape |
| md | 768px | `md:` | Tablet |
| lg | 1024px | `lg:` | Laptop |
| xl | 1280px | `xl:` | Desktop |
| 2xl | 1536px | `2xl:` | Large desktop |

---

## 14. CSS Variables / Tailwind Theme

### 14.1 CSS Variables

```css
:root {
  /* Colors */
  --color-primary: #FFCF32;
  --color-secondary: #6FC2FF;
  --color-teal: #53DBC9;
  --color-background: #F4EFEA;
  --color-foreground: #383838;
  --color-black: #000000;
  --color-white: #FFFFFF;
  --color-muted-foreground: #A1A1A1;
  --color-border: #383838;
  --color-error: #FF7169;

  /* Typography */
  --font-sans: "Noto Sans Thai", ui-sans-serif, sans-serif, system-ui;

  /* Shadows */
  --shadow-brutal: -12px 12px 0 0 rgb(56, 56, 56);
  --shadow-brutal-lg: -16px 16px 0 0 rgb(56, 56, 56);
  --shadow-brutal-xl: -24px 24px 0 0 rgb(56, 56, 56);

  /* Border Radius */
  --radius-minimal: 2px;
}
```

---

### 14.2 Tailwind Config

```js
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: '#FFCF32',
        secondary: '#6FC2FF',
        teal: '#53DBC9',
        background: '#F4EFEA',
        foreground: '#383838',
        'muted-foreground': '#A1A1A1',
        error: '#FF7169',
      },
      fontFamily: {
        sans: ['Noto Sans Thai', 'ui-sans-serif', 'sans-serif', 'system-ui'],
      },
      borderRadius: {
        'minimal': '2px',
      },
      boxShadow: {
        'brutal': '-12px 12px 0 0 rgb(56, 56, 56)',
        'brutal-lg': '-16px 16px 0 0 rgb(56, 56, 56)',
        'brutal-xl': '-24px 24px 0 0 rgb(56, 56, 56)',
      },
      fontWeight: {
        normal: 400,
      },
    },
  },
  plugins: [],
}
```

---

## 15. Layout Patterns

### Container Widths

```html
<div className="max-w-7xl mx-auto px-6">
  <!-- Centered container -->
</div>
```

---

### Grid Systems

```html
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
  <div>Item 1</div>
  <div>Item 2</div>
  <div>Item 3</div>
</div>
```

---

## 16. Example Component Reference

### Complete Button Component (React + Tailwind)

```tsx
// components/ui/button.tsx
import { ButtonHTMLAttributes, forwardRef } from 'react';
import { cn } from '@/lib/utils';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost';
}

const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = 'primary', children, ...props }, ref) => {
    return (
      <button
        ref={ref}
        className={cn(
          // Base styles (Brutalist)
          'inline-flex items-center justify-center font-normal uppercase tracking-[0.32px] rounded-[2px] transition-shadow border-2',
          'focus-visible:outline-none focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-foreground',
          'disabled:opacity-50 disabled:cursor-not-allowed',

          // Variants
          variant === 'primary' && 'bg-primary text-foreground border-foreground hover:shadow-brutal',
          variant === 'secondary' && 'bg-secondary text-foreground border-foreground hover:shadow-brutal',
          variant === 'ghost' && 'bg-transparent text-foreground border-transparent hover:bg-foreground/5',

          // Size (fixed from design)
          'px-[18px] py-[11.5px] text-base',

          className
        )}
        {...props}
      >
        {children}
      </button>
    );
  }
);

Button.displayName = 'Button';

export { Button };
```

**Usage:**
```tsx
import { Button } from '@/components/ui/button';

function Example() {
  return (
    <div className="flex gap-4">
      <Button variant="primary">ลงทะเบียนฟรี</Button>
      <Button variant="secondary">เรียนรู้เพิ่มเติม</Button>
      <Button variant="ghost">ยกเลิก</Button>
    </div>
  );
}
```

---

### Complete Card Component

```tsx
// components/ui/card.tsx
import { HTMLAttributes, forwardRef } from 'react';
import { cn } from '@/lib/utils';

const Card = forwardRef<HTMLDivElement, HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div
      ref={ref}
      className={cn(
        'p-8 bg-white rounded-[2px] shadow-brutal border-2 border-foreground',
        'hover:translate-x-[-4px] hover:translate-y-[-4px] hover:shadow-brutal-lg transition-all duration-300',
        className
      )}
      {...props}
    />
  )
);

Card.displayName = 'Card';

export { Card };
```

---

## 17. Additional Sections

### 17.1 Implementation Best Practices

**Design Token Usage:**
- ✅ Use Noto Sans Thai font for everything (Thai language support)
- ✅ Use font-weight 400 (normal) only - NO BOLD
- ✅ Use 2px border-radius for almost everything
- ✅ Use hard shadows (-12px 12px 0 0) - NO BLUR
- ✅ Use 2px borders everywhere
- ✅ Use uppercase for headings and labels
- ❌ Never use gradients
- ❌ Never use soft shadows (blur > 0)
- ❌ Never use large border-radius (8px+)
- ❌ Never use bold fonts (defeats the brutalist aesthetic)

---

### 17.2 Accessibility Guidelines

**Color Contrast:**
- Primary yellow (#FFCF32) + dark gray (#383838): **8.2:1** ✅ (AAA)
- Secondary blue (#6FC2FF) + dark gray (#383838): **5.2:1** ✅ (AA)
- Background (#F4EFEA) + foreground (#383838): **11.8:1** ✅ (AAA)

**Keyboard Navigation:**
- All buttons have focus states (2px outline)
- Tab order follows visual order

---

### 17.3 Font Loading

**Noto Sans Thai** can be loaded via Google Fonts:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Thai:wght@400&display=swap" rel="stylesheet">
```

Or via CSS:
```css
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Thai:wght@400&display=swap');
```

**Fallback:** If Noto Sans Thai fails to load, use system sans-serif fonts.

---

## 🎉 End of Style Guide

**Key Takeaways:**
1. **Neo-Brutalism**: Hard shadows, 2px borders, minimal radius
2. **Thai-Optimized**: Noto Sans Thai for perfect Thai character rendering
3. **Normal Weight Only**: Font-weight 400 for all text (NO BOLD)
4. **Bold Colors**: Golden Yellow (#FFCF32), Blue (#6FC2FF), Warm beige background
5. **Hard Shadows**: -12px 12px 0 0 (no blur!)
6. **2px Everything**: Border-radius 2px (not 8px or 16px)

**Critical Rules:**
- ❌ NO soft shadows (blur must be 0)
- ❌ NO rounded corners (use 2px only)
- ❌ NO bold fonts (use size for hierarchy)
- ❌ NO gradients (flat colors only)
- ✅ YES to uppercase headings
- ✅ YES to hard shadows
- ✅ YES to Noto Sans Thai font
- ✅ YES to bold color blocking

**Next Steps:**
1. Load Noto Sans Thai font (critical!)
2. Configure Tailwind with brutalist shadows
3. Build components with brutalist aesthetics
4. Use #FFCF32 as primary brand color

---

*Customized for REDITO from Neo-Brutalist design principles*
*Date: 2025-11-03*
*All values based on brutalist design patterns with REDITO branding*
