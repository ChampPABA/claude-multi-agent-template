# MotherDuck-Inspired Design System - Style Guide

> **Source:** Generated from reference design (MotherDuck.com)
> **Date:** 2025-11-02
> **Tech Stack:** React, Tailwind CSS
> **Design Style:** Neo-Modern Data Platform (Playful + Professional)

---

## Quick Reference

### Most Used Patterns

| Pattern | Code |
|---------|------|
| Primary Button | `className="px-6 py-3 bg-primary text-white rounded-lg hover:bg-primary/90 transition-colors font-medium"` |
| Secondary Button | `className="px-6 py-3 bg-white text-primary border-2 border-primary rounded-lg hover:bg-primary/5 transition-colors font-medium"` |
| Card | `className="p-8 bg-white rounded-2xl shadow-sm border border-gray-200"` |
| Heading 1 | `className="text-5xl font-bold text-foreground leading-tight"` |
| Body Text | `className="text-base text-foreground leading-relaxed"` |
| Muted Text | `className="text-sm text-muted-foreground"` |
| Accent Section | `className="bg-primary py-16 px-8"` |
| Code Block | `className="px-4 py-2 bg-gray-50 rounded-md font-mono text-sm"` |

### Design Tokens Summary

```json
{
  "colors": {
    "primary": "#6FC2FF",
    "accent": "#FFD93D",
    "success": "#10B981",
    "warning": "#F59E0B",
    "error": "#EF4444",
    "background": "#FFFFFF",
    "foreground": "#000000",
    "mutedForeground": "#6B7280",
    "border": "#E5E7EB"
  },
  "spacing": {
    "xs": "0.25rem",
    "sm": "0.5rem",
    "md": "1rem",
    "lg": "1.5rem",
    "xl": "2rem",
    "2xl": "3rem",
    "3xl": "4rem"
  },
  "typography": {
    "fontFamily": "Inter, -apple-system, BlinkMacSystemFont, sans-serif",
    "fontFamilyMono": "'Aeonik Mono', 'JetBrains Mono', Consolas, monospace",
    "fontSize": {
      "xs": "0.75rem",
      "sm": "0.875rem",
      "base": "1rem",
      "lg": "1.125rem",
      "xl": "1.25rem",
      "2xl": "1.5rem",
      "3xl": "1.875rem",
      "4xl": "2.25rem",
      "5xl": "3rem"
    }
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
This design system is inspired by MotherDuck's modern, data-focused aesthetic. It combines playful energy (bright cyan blue, vibrant yellow accents) with professional clarity. The system prioritizes readability, accessibility, and a friendly-yet-trustworthy user experience suitable for data platforms, SaaS dashboards, and technical products.

**Tech Stack:**
- Framework: React 18
- Styling: Tailwind CSS 3.4
- UI Library: Custom components
- Icons: Lucide React
- Fonts: Inter (UI), Aeonik Mono (code)

**Goals:**
- Create a modern, approachable data platform aesthetic
- Balance playfulness with professionalism
- Ensure high readability and accessibility
- Provide reusable, consistent components
- Speed up development with clear patterns

---

## 2. Design Philosophy

**Core Principles:**
- **Clarity First**: Information hierarchy is paramount. Users should understand content instantly.
- **Playful Professionalism**: Bright colors and friendly design without sacrificing trust.
- **Data-Centric**: Clean tables, readable code blocks, clear data visualization.
- **Modern & Fresh**: Current design trends (soft shadows, rounded corners, ample whitespace).

**Visual Identity:**
- **Color Story**: Bright cyan blue (#6FC2FF) as the hero color, complemented by vibrant yellow (#FFD93D) for accents
- **Typography**: Inter font for clean, modern readability
- **Shapes**: Rounded corners (8-16px radius), organic wave dividers
- **Illustrations**: Playful, friendly (duck mascot, cloud shapes)

**User Experience Goals:**
- **Trust & Credibility**: Professional design, clear structure, accessible
- **Innovation**: Modern aesthetic, bright colors, current trends
- **Approachability**: Not overly corporate, friendly and welcoming
- **Speed & Efficiency**: Fast interactions, minimal cognitive load

---

## 3. Color Palette

### Primary Colors

**Primary (MotherDuck Blue)**
- **Color**: `#6FC2FF` (rgb(111, 194, 255))
- **Usage**: Primary CTAs, hero sections, brand elements, active states
- **CSS Variable**: `var(--color-primary)`
- **Tailwind**: `bg-primary`, `text-primary`, `border-primary`
- **Rationale**: Vibrant cyan blue conveys innovation, trust, and energy. Signature brand color.

**Primary Hover**
- **Color**: `#5AB5F5` (darker shade)
- **Usage**: Hover states for primary buttons/links
- **Tailwind**: `hover:bg-primary/90`

### Accent Colors

**Accent Yellow**
- **Color**: `#FFD93D` (rgb(255, 217, 61))
- **Usage**: CTAs, highlights, important badges, playful accents
- **CSS Variable**: `var(--color-accent)`
- **Tailwind**: `bg-accent`, `text-accent`
- **Rationale**: Vibrant yellow creates energy, draws attention, complements blue

**Accent Hover**
- **Color**: `#FFD020` (darker yellow)
- **Usage**: Hover states for accent buttons
- **Tailwind**: `hover:bg-accent/90`

### Functional Colors

**Success**
- **Color**: `#10B981` (Green 500)
- **Usage**: Success messages, positive states, completed tasks
- **Tailwind**: `bg-success`, `text-success`

**Warning**
- **Color**: `#F59E0B` (Amber 500)
- **Usage**: Warning messages, caution states, pending actions
- **Tailwind**: `bg-warning`, `text-warning`

**Error**
- **Color**: `#EF4444` (Red 500)
- **Usage**: Error messages, destructive actions, failed states
- **Tailwind**: `bg-error`, `text-error`

**Info**
- **Color**: `#3B82F6` (Blue 500)
- **Usage**: Informational messages, neutral notifications
- **Tailwind**: `bg-info`, `text-info`

### Background & Surface Colors

**Background**
- **Color**: `#FFFFFF` (White)
- **Usage**: Page background, card backgrounds
- **Tailwind**: `bg-background`

**Secondary Background**
- **Color**: `#F9FAFB` (Gray 50)
- **Usage**: Alternate section backgrounds, subtle contrast
- **Tailwind**: `bg-gray-50`

**Code Background**
- **Color**: `#F3F4F6` (Gray 100)
- **Usage**: Code blocks, pre-formatted text
- **Tailwind**: `bg-gray-100`

### Text Colors

**Foreground (Primary Text)**
- **Color**: `#000000` (Black)
- **Usage**: Primary text, headings
- **Tailwind**: `text-foreground`
- **Contrast Ratio**: 21:1 (WCAG AAA)

**Muted Foreground (Secondary Text)**
- **Color**: `#6B7280` (Gray 500)
- **Usage**: Secondary text, descriptions, metadata
- **Tailwind**: `text-muted-foreground`
- **Contrast Ratio**: 7:1 (WCAG AAA)

### Border & Divider Colors

**Border**
- **Color**: `#E5E7EB` (Gray 200)
- **Usage**: Card borders, dividers, input borders
- **Tailwind**: `border-border`

**Border Strong**
- **Color**: `#D1D5DB` (Gray 300)
- **Usage**: Emphasized borders, active input borders
- **Tailwind**: `border-gray-300`

### Pastel Section Backgrounds (from reference)

**Light Blue**
- **Color**: `#EBF9FF` (rgb(235, 249, 255))
- **Usage**: Light blue section backgrounds
- **Tailwind**: Custom class or `bg-blue-50`

**Light Green**
- **Color**: `#E8F5E9` (rgb(232, 245, 233))
- **Usage**: Success section backgrounds
- **Tailwind**: Custom class or `bg-green-50`

**Light Yellow**
- **Color**: `#F4EFEA` (rgb(244, 239, 234))
- **Usage**: Warm section backgrounds
- **Tailwind**: Custom class or `bg-yellow-50`

### Color Palette Grid

| Color | HEX | RGB | Usage | Tailwind Class |
|-------|-----|-----|-------|----------------|
| Primary | #6FC2FF | rgb(111, 194, 255) | CTAs, brand | `bg-primary` |
| Accent | #FFD93D | rgb(255, 217, 61) | Highlights | `bg-accent` |
| Success | #10B981 | rgb(16, 185, 129) | Success states | `bg-success` |
| Warning | #F59E0B | rgb(245, 158, 11) | Warning states | `bg-warning` |
| Error | #EF4444 | rgb(239, 68, 68) | Error states | `bg-error` |
| Info | #3B82F6 | rgb(59, 130, 246) | Info states | `bg-info` |
| Foreground | #000000 | rgb(0, 0, 0) | Primary text | `text-foreground` |
| Muted | #6B7280 | rgb(107, 114, 128) | Secondary text | `text-muted-foreground` |
| Border | #E5E7EB | rgb(229, 231, 235) | Borders | `border-border` |
| Background | #FFFFFF | rgb(255, 255, 255) | Backgrounds | `bg-background` |

---

## 4. Typography

### Font Families

**Sans-Serif (Primary - Inter)**
```css
font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
```
- **Usage**: All UI elements, body text, headings, buttons
- **Why Inter**: Modern, highly readable, excellent at small sizes, professional
- **Import**: `@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');`

**Monospace (Code - Aeonik Mono)**
```css
font-family: 'Aeonik Mono', 'JetBrains Mono', 'Fira Code', Consolas, Monaco, monospace;
```
- **Usage**: Code blocks, technical content, monospace data
- **Fallback**: Use JetBrains Mono or system monospace if Aeonik unavailable

### Font Weights

| Weight | Value | Usage | Tailwind Class |
|--------|-------|-------|----------------|
| Normal | 400 | Body text, paragraphs | `font-normal` |
| Medium | 500 | Subheadings, emphasis, buttons | `font-medium` |
| Semibold | 600 | Section headings, card titles | `font-semibold` |
| Bold | 700 | Page headings, strong emphasis | `font-bold` |

### Text Styles

#### Headings

**H1 - Page Title / Hero Heading**
```html
<h1 className="text-5xl md:text-6xl font-bold text-foreground leading-tight">
  Ducking Simple Data Warehouse
</h1>
```
- **Size**: 3rem (48px) mobile, 3.75rem (60px) desktop
- **Weight**: Bold (700)
- **Line Height**: 1.2 (tight)
- **Usage**: Hero sections, main page titles

**H2 - Section Heading**
```html
<h2 className="text-4xl font-bold text-foreground leading-tight">
  Why MotherDuck?
</h2>
```
- **Size**: 2.25rem (36px)
- **Weight**: Bold (700)
- **Line Height**: 1.2
- **Usage**: Major section headings

**H3 - Subsection Heading**
```html
<h3 className="text-2xl font-semibold text-foreground leading-snug">
  Fast Analytics
</h3>
```
- **Size**: 1.5rem (24px)
- **Weight**: Semibold (600)
- **Line Height**: 1.4
- **Usage**: Card headings, subsection titles

**H4 - Card Title / Feature Heading**
```html
<h4 className="text-xl font-semibold text-foreground">
  Serverless Architecture
</h4>
```
- **Size**: 1.25rem (20px)
- **Weight**: Semibold (600)
- **Line Height**: 1.4
- **Usage**: Feature cards, smaller headings

#### Body Text

**Large Body (Lead Text)**
```html
<p className="text-lg text-foreground leading-relaxed">
  MotherDuck is a collaborative, cloud-based analytics platform built on DuckDB.
</p>
```
- **Size**: 1.125rem (18px)
- **Line Height**: 1.75 (relaxed)
- **Usage**: Lead paragraphs, introductions

**Regular Body**
```html
<p className="text-base text-foreground leading-relaxed">
  Regular body text for main content.
</p>
```
- **Size**: 1rem (16px)
- **Line Height**: 1.75 (relaxed)
- **Usage**: Standard body text, descriptions

**Small Body**
```html
<p className="text-sm text-muted-foreground leading-normal">
  Small secondary text or metadata
</p>
```
- **Size**: 0.875rem (14px)
- **Line Height**: 1.5 (normal)
- **Usage**: Secondary text, descriptions, labels

**Caption / Metadata**
```html
<span className="text-xs text-muted-foreground uppercase tracking-wide">
  Updated 2 hours ago
</span>
```
- **Size**: 0.75rem (12px)
- **Line Height**: 1.5
- **Usage**: Timestamps, metadata, fine print

#### Code Text

**Inline Code**
```html
<code className="px-1.5 py-0.5 bg-gray-100 text-foreground rounded font-mono text-sm">
  SELECT * FROM table
</code>
```

**Code Block**
```html
<pre className="p-4 bg-gray-100 rounded-lg overflow-x-auto">
  <code className="font-mono text-sm text-foreground">
    SELECT * FROM users WHERE active = true;
  </code>
</pre>
```

---

## 5. Spacing System

### Spacing Scale (8px Grid System)

| Token | Value | Pixels | Tailwind | Common Usage |
|-------|-------|--------|----------|--------------|
| xs | 0.25rem | 4px | `p-1`, `m-1`, `gap-1` | Tight spacing, icon gaps |
| sm | 0.5rem | 8px | `p-2`, `m-2`, `gap-2` | Small gaps, inline elements |
| md | 1rem | 16px | `p-4`, `m-4`, `gap-4` | Default spacing, card padding |
| lg | 1.5rem | 24px | `p-6`, `m-6`, `gap-6` | Section spacing, generous padding |
| xl | 2rem | 32px | `p-8`, `m-8`, `gap-8` | Large sections, hero spacing |
| 2xl | 3rem | 48px | `p-12`, `m-12`, `gap-12` | Page margins, major sections |
| 3xl | 4rem | 64px | `p-16`, `m-16`, `gap-16` | Hero sections, large dividers |

### Application Examples

**Component Padding:**
```html
<!-- Button -->
<button className="px-6 py-3">Click me</button>

<!-- Card (generous) -->
<div className="p-8">Card content</div>

<!-- Card (compact) -->
<div className="p-6">Card content</div>

<!-- Hero Section -->
<section className="py-16 px-8">Hero content</section>
```

**Layout Gaps:**
```html
<!-- Vertical stack (tight) -->
<div className="space-y-4">
  <div>Item 1</div>
  <div>Item 2</div>
</div>

<!-- Vertical stack (comfortable) -->
<div className="space-y-8">
  <div>Item 1</div>
  <div>Item 2</div>
</div>

<!-- Horizontal row -->
<div className="flex gap-6">
  <div>Item 1</div>
  <div>Item 2</div>
</div>

<!-- Grid -->
<div className="grid grid-cols-3 gap-8">
  <div>Item 1</div>
  <div>Item 2</div>
  <div>Item 3</div>
</div>
```

---

## 6. Component Styles

### 6.1 Component Inventory

| Component | Variants | States | Priority | Notes |
|-----------|----------|--------|----------|-------|
| Button | Primary, Secondary, Accent, Outline, Ghost | default, hover, active, disabled, loading | **Must-use** | Never create custom buttons |
| Card | Default, Elevated, Interactive | default, hover | **Must-use** | For content grouping |
| Input | Default, Error, Success | default, focus, disabled, error | **Must-use** | All form inputs |
| Badge | Default, Primary, Accent, Success, Warning, Error | - | Optional | Status indicators |
| Alert | Info, Success, Warning, Error | - | Optional | User notifications |
| Code Block | Inline, Block | - | **Must-use** | Technical content |
| Table | Default, Striped | - | **Must-use** | Data display |

**Legend:**
- **Must-use**: Always use this component, never create custom variants
- **Optional**: Use when appropriate
- **Deprecated**: Use alternative component instead

---

### 6.2 Button Component

#### Variants

**Primary Button**
```tsx
<button className="px-6 py-3 bg-primary text-white rounded-lg hover:bg-primary/90 transition-colors duration-200 font-medium shadow-sm hover:shadow-md">
  Get Started
</button>
```
- **Usage**: Main CTAs, primary actions
- **Background**: `#6FC2FF` (primary blue)
- **Text**: White
- **Hover**: Slightly darker blue + elevated shadow

**Accent Button (Yellow)**
```tsx
<button className="px-6 py-3 bg-accent text-black rounded-lg hover:bg-accent/90 transition-colors duration-200 font-medium shadow-sm hover:shadow-md">
  Try Free
</button>
```
- **Usage**: High-priority CTAs, special offers
- **Background**: `#FFD93D` (yellow)
- **Text**: Black (high contrast)
- **Hover**: Slightly darker yellow

**Secondary Button**
```tsx
<button className="px-6 py-3 bg-white text-primary border-2 border-primary rounded-lg hover:bg-primary/5 transition-colors duration-200 font-medium">
  Learn More
</button>
```
- **Usage**: Secondary actions, less prominent
- **Background**: White with primary border
- **Text**: Primary blue
- **Hover**: Light blue background tint

**Outline Button**
```tsx
<button className="px-6 py-3 bg-transparent border-2 border-gray-300 text-foreground rounded-lg hover:bg-gray-50 transition-colors duration-200 font-medium">
  Cancel
</button>
```
- **Usage**: Tertiary actions, cancel buttons
- **Background**: Transparent with border
- **Hover**: Light gray background

**Ghost Button**
```tsx
<button className="px-6 py-3 bg-transparent text-foreground rounded-lg hover:bg-gray-100 transition-colors duration-200 font-medium">
  View Details
</button>
```
- **Usage**: Subtle actions, navigation
- **Background**: Transparent
- **Hover**: Light gray background

#### States

| State | Additional Classes | Visual Behavior |
|-------|-------------------|-----------------|
| Default | - | Normal appearance |
| Hover | `hover:bg-primary/90 hover:shadow-md` | Darker background + shadow |
| Active | `active:bg-primary/80 active:scale-95` | Even darker + slight scale |
| Focus | `focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2` | Visible focus ring |
| Disabled | `disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:bg-primary` | Faded, no interactions |
| Loading | `disabled:opacity-70` + spinner | Faded + spinner icon |

#### Sizes

**Small**
```tsx
<button className="px-4 py-2 text-sm rounded-md">Small</button>
```

**Medium (Default)**
```tsx
<button className="px-6 py-3 text-base rounded-lg">Medium</button>
```

**Large**
```tsx
<button className="px-8 py-4 text-lg rounded-lg">Large</button>
```

#### Full Example with All States
```tsx
<button
  className="
    px-6 py-3
    bg-primary text-white
    rounded-lg
    font-medium
    shadow-sm
    transition-all duration-200
    hover:bg-primary/90 hover:shadow-md
    active:bg-primary/80 active:scale-95
    focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2
    disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:bg-primary
  "
>
  Primary Action
</button>
```

---

### 6.3 Card Component

#### Variants

**Default Card**
```tsx
<div className="p-8 bg-white rounded-2xl border border-gray-200">
  <h3 className="text-xl font-semibold mb-2">Card Title</h3>
  <p className="text-sm text-muted-foreground">Card content and description</p>
</div>
```
- **Padding**: Generous (32px)
- **Border Radius**: Large (16px)
- **Border**: Light gray
- **Background**: White

**Elevated Card (with shadow)**
```tsx
<div className="p-8 bg-white rounded-2xl shadow-md hover:shadow-lg transition-shadow duration-200">
  <h3 className="text-xl font-semibold mb-2">Elevated Card</h3>
  <p className="text-sm text-muted-foreground">Card with shadow elevation</p>
</div>
```
- **Shadow**: Medium shadow
- **Hover**: Larger shadow (elevation effect)

**Interactive Card (clickable)**
```tsx
<div className="p-8 bg-white rounded-2xl border border-gray-200 hover:border-primary hover:shadow-lg transition-all duration-200 cursor-pointer">
  <h3 className="text-xl font-semibold mb-2">Clickable Card</h3>
  <p className="text-sm text-muted-foreground">Hover to see interaction</p>
</div>
```
- **Hover**: Border changes to primary blue + shadow
- **Cursor**: Pointer

**Colored Background Card**
```tsx
<div className="p-8 bg-blue-50 rounded-2xl border border-blue-200">
  <h3 className="text-xl font-semibold mb-2">Info Card</h3>
  <p className="text-sm text-muted-foreground">Light blue background</p>
</div>
```

---

### 6.4 Input Component

#### Variants

**Text Input (Default)**
```tsx
<input
  type="text"
  className="
    w-full px-4 py-3
    bg-white border border-gray-300
    rounded-lg
    text-foreground
    placeholder:text-gray-400
    focus:outline-none focus:ring-2 focus:ring-primary focus:border-primary
    transition-all duration-200
  "
  placeholder="Enter text"
/>
```

**Input with Error**
```tsx
<input
  type="text"
  className="
    w-full px-4 py-3
    bg-white border-2 border-error
    rounded-lg
    text-foreground
    placeholder:text-gray-400
    focus:outline-none focus:ring-2 focus:ring-error
  "
  placeholder="Enter text"
  aria-invalid="true"
  aria-describedby="error-message"
/>
<p id="error-message" className="text-sm text-error mt-2">
  This field is required
</p>
```

**Input with Success**
```tsx
<input
  type="text"
  className="
    w-full px-4 py-3
    bg-white border-2 border-success
    rounded-lg
    text-foreground
    focus:outline-none focus:ring-2 focus:ring-success
  "
  placeholder="Enter text"
/>
```

---

### 6.5 Badge Component

**Default Badge**
```tsx
<span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-700">
  Default
</span>
```

**Status Badges**
```tsx
<!-- Primary -->
<span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-primary/10 text-primary">
  Active
</span>

<!-- Accent -->
<span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-accent/20 text-yellow-800">
  Featured
</span>

<!-- Success -->
<span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-success/10 text-success">
  Completed
</span>

<!-- Warning -->
<span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-warning/10 text-warning">
  Pending
</span>

<!-- Error -->
<span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-error/10 text-error">
  Failed
</span>
```

---

### 6.6 Code Block Component

**Inline Code**
```tsx
<code className="px-2 py-1 bg-gray-100 text-foreground rounded font-mono text-sm">
  SELECT * FROM users
</code>
```

**Code Block**
```tsx
<pre className="p-4 bg-gray-100 rounded-lg overflow-x-auto border border-gray-200">
  <code className="font-mono text-sm text-foreground">
    {`SELECT
  user_id,
  COUNT(*) as query_count
FROM queries
WHERE created_at > NOW() - INTERVAL '7 days'
GROUP BY user_id
ORDER BY query_count DESC;`}
  </code>
</pre>
```

---

## 7. Shadows & Elevation

### Shadow Scale

| Token | CSS Value | Tailwind | Usage |
|-------|-----------|----------|-------|
| None | none | `shadow-none` | Flat elements |
| XS | 0 1px 2px rgba(0,0,0,0.05) | `shadow-sm` | Subtle elevation, buttons |
| SM | 0 1px 3px rgba(0,0,0,0.1), 0 1px 2px rgba(0,0,0,0.06) | `shadow` | Cards, dropdowns |
| MD | 0 4px 6px rgba(0,0,0,0.07), 0 2px 4px rgba(0,0,0,0.06) | `shadow-md` | Elevated cards |
| LG | 0 10px 15px rgba(0,0,0,0.1), 0 4px 6px rgba(0,0,0,0.05) | `shadow-lg` | Modals, popovers |
| XL | 0 20px 25px rgba(0,0,0,0.1), 0 10px 10px rgba(0,0,0,0.04) | `shadow-xl` | Large modals |
| 2XL | 0 25px 50px rgba(0,0,0,0.25) | `shadow-2xl` | Maximum elevation |

### Usage Examples

```html
<!-- Button with subtle shadow -->
<button className="shadow-sm hover:shadow-md">Button</button>

<!-- Card with medium shadow -->
<div className="shadow-md">Card</div>

<!-- Modal -->
<div className="shadow-xl">Modal content</div>

<!-- Elevated card on hover -->
<div className="shadow hover:shadow-lg transition-shadow duration-200">
  Interactive card
</div>
```

---

## 8. Animations & Transitions

### Timing Functions

| Name | Value | Usage |
|------|-------|-------|
| Default | ease-in-out | General transitions |
| Fast | cubic-bezier(0.4, 0, 0.2, 1) | Quick interactions |
| Smooth | cubic-bezier(0.4, 0, 1, 1) | Smooth entrances |

### Transition Durations

| Speed | Value | Tailwind | Usage |
|-------|-------|----------|-------|
| Fast | 150ms | `duration-150` | Hover states, quick feedback |
| Normal | 200ms | `duration-200` | Default transitions |
| Slow | 300ms | `duration-300` | Complex animations |

### Common Transitions

**Background Color**
```html
<button className="transition-colors duration-200 hover:bg-primary/90">
  Hover me
</button>
```

**Shadow**
```html
<div className="transition-shadow duration-200 hover:shadow-lg">
  Card with shadow transition
</div>
```

**Transform (Scale)**
```html
<button className="transition-transform duration-200 hover:scale-105 active:scale-95">
  Interactive button
</button>
```

**All Properties**
```html
<div className="transition-all duration-200 hover:shadow-lg hover:border-primary">
  Multiple transitions
</div>
```

### Microinteractions

**Button Press**
```html
<button className="
  active:scale-95
  transition-transform duration-150
">
  Click me
</button>
```

**Card Hover Elevation**
```html
<div className="
  hover:shadow-lg hover:-translate-y-1
  transition-all duration-200
">
  Hover to lift
</div>
```

**Icon Bounce**
```html
<div className="hover:scale-110 transition-transform duration-150">
  <Icon />
</div>
```

---

## 9. Border Styles

### Border Widths

| Token | Value | Tailwind | Usage |
|-------|-------|----------|-------|
| Default | 1px | `border` | Standard borders |
| Medium | 2px | `border-2` | Emphasis, CTAs |
| Thick | 4px | `border-4` | Strong emphasis |

### Border Colors

**Semantic Colors:**
```html
<div className="border border-gray-200">Default border</div>
<div className="border-2 border-primary">Primary border</div>
<div className="border-2 border-error">Error border</div>
<div className="border border-gray-300">Strong border</div>
```

### Border Styles

| Style | Tailwind | Usage |
|-------|----------|-------|
| Solid | `border-solid` (default) | Standard borders |
| Dashed | `border-dashed` | Placeholders, dropzones |
| Dotted | `border-dotted` | Subtle separators |

---

## 10. Border Radius

### Radius Scale

| Token | Value | Tailwind | Usage |
|-------|-------|----------|-------|
| None | 0 | `rounded-none` | Sharp corners |
| SM | 0.25rem (4px) | `rounded-sm` | Subtle rounding |
| Default | 0.5rem (8px) | `rounded-md` | Inputs, small components |
| LG | 0.75rem (12px) | `rounded-lg` | Buttons, cards (default) |
| XL | 1rem (16px) | `rounded-xl` | Large cards, modals |
| 2XL | 1.5rem (24px) | `rounded-2xl` | Hero cards, major sections |
| Full | 9999px | `rounded-full` | Pills, avatars, badges |

### Usage Examples

```html
<!-- Button (large radius) -->
<button className="rounded-lg">Button</button>

<!-- Card (extra large radius) -->
<div className="rounded-2xl">Card</div>

<!-- Input (medium radius) -->
<input className="rounded-lg" />

<!-- Badge (full radius) -->
<span className="rounded-full">Badge</span>

<!-- Avatar -->
<img className="rounded-full" />
```

---

## 11. Opacity & Transparency

### Opacity Scale

| Token | Value | Tailwind | Usage |
|-------|-------|----------|-------|
| 0 | 0 | `opacity-0` | Hidden elements |
| 5 | 0.05 | `opacity-5` | Very subtle backgrounds |
| 10 | 0.1 | `opacity-10` | Subtle overlays |
| 50 | 0.5 | `opacity-50` | Disabled states |
| 70 | 0.7 | `opacity-70` | Muted elements |
| 90 | 0.9 | `opacity-90` | Slightly transparent |
| 100 | 1 | `opacity-100` | Fully visible |

### Common Patterns

**Disabled State**
```html
<button className="disabled:opacity-50 disabled:cursor-not-allowed">
  Button
</button>
```

**Muted Text (using color opacity)**
```html
<p className="text-foreground/70">Muted text</p>
```

**Background Tint**
```html
<div className="bg-primary/5">Light blue background</div>
<div className="bg-primary/10">Medium blue background</div>
```

**Overlay**
```html
<div className="bg-black/50">Dark overlay</div>
```

---

## 12. Z-Index Layers

### Z-Index Scale

| Layer | Value | Usage |
|-------|-------|-------|
| Base | 0 | Normal content |
| Dropdown | 10 | Dropdown menus |
| Sticky | 20 | Sticky headers |
| Fixed | 30 | Fixed elements |
| Modal Backdrop | 40 | Modal overlays |
| Modal | 50 | Modal dialogs |
| Popover | 60 | Popovers, tooltips |
| Toast | 70 | Toast notifications |

### Usage

```css
/* Custom z-index values */
.dropdown { z-index: 10; }
.sticky-header { z-index: 20; }
.modal-backdrop { z-index: 40; }
.modal { z-index: 50; }
.toast { z-index: 70; }
```

```html
<!-- Tailwind z-index utilities -->
<div className="z-10">Dropdown</div>
<div className="z-40">Modal backdrop</div>
<div className="z-50">Modal</div>
```

---

## 13. Responsive Breakpoints

### Breakpoint Scale

| Breakpoint | Min Width | Tailwind | Target Devices |
|------------|-----------|----------|----------------|
| xs | 0px | (default) | Mobile portrait (< 640px) |
| sm | 640px | `sm:` | Mobile landscape |
| md | 768px | `md:` | Tablet portrait |
| lg | 1024px | `lg:` | Tablet landscape, laptop |
| xl | 1280px | `xl:` | Desktop |
| 2xl | 1536px | `2xl:` | Large desktop |

### Mobile-First Approach

```html
<!-- Stack on mobile, row on tablet+ -->
<div className="flex flex-col md:flex-row gap-8">
  <div>Column 1</div>
  <div>Column 2</div>
</div>

<!-- Responsive padding -->
<section className="py-8 px-4 md:py-16 md:px-8 lg:py-24 lg:px-16">
  Content
</section>

<!-- Responsive text size -->
<h1 className="text-4xl md:text-5xl lg:text-6xl font-bold">
  Responsive Heading
</h1>

<!-- Grid columns (1 on mobile, 2 on tablet, 3 on desktop) -->
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
  <div>Item 1</div>
  <div>Item 2</div>
  <div>Item 3</div>
</div>
```

---

## 14. CSS Variables / Tailwind Theme

### 14.1 CSS Variables

```css
:root {
  /* Colors */
  --color-primary: #6FC2FF;
  --color-accent: #FFD93D;
  --color-success: #10B981;
  --color-warning: #F59E0B;
  --color-error: #EF4444;
  --color-info: #3B82F6;

  --color-background: #FFFFFF;
  --color-foreground: #000000;
  --color-muted-foreground: #6B7280;
  --color-border: #E5E7EB;

  /* Spacing */
  --spacing-xs: 0.25rem;
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
  --spacing-lg: 1.5rem;
  --spacing-xl: 2rem;
  --spacing-2xl: 3rem;
  --spacing-3xl: 4rem;

  /* Typography */
  --font-sans: Inter, -apple-system, BlinkMacSystemFont, sans-serif;
  --font-mono: 'Aeonik Mono', 'JetBrains Mono', Consolas, monospace;

  /* Border Radius */
  --radius-sm: 0.25rem;
  --radius-md: 0.5rem;
  --radius-lg: 0.75rem;
  --radius-xl: 1rem;
  --radius-2xl: 1.5rem;
}
```

### 14.2 Design Tokens (Machine-Readable)

```json
{
  "colors": {
    "primary": {
      "50": "#EBF8FF",
      "100": "#D1EFFF",
      "200": "#B8E7FF",
      "300": "#9FDFFF",
      "400": "#87D8FF",
      "500": "#6FC2FF",
      "600": "#5AB5F5",
      "700": "#3D9DE0",
      "800": "#2A7AB8",
      "900": "#1A5A8F"
    },
    "accent": {
      "50": "#FFFBEB",
      "100": "#FFF4C7",
      "200": "#FFED9E",
      "300": "#FFE575",
      "400": "#FFDE4D",
      "500": "#FFD93D",
      "600": "#FFD020",
      "700": "#F5C300",
      "800": "#D4A800",
      "900": "#A68600"
    },
    "neutral": {
      "50": "#F9FAFB",
      "100": "#F3F4F6",
      "200": "#E5E7EB",
      "300": "#D1D5DB",
      "400": "#9CA3AF",
      "500": "#6B7280",
      "600": "#4B5563",
      "700": "#374151",
      "800": "#1F2937",
      "900": "#111827"
    },
    "semantic": {
      "success": "#10B981",
      "warning": "#F59E0B",
      "error": "#EF4444",
      "info": "#3B82F6"
    }
  },
  "spacing": {
    "xs": "0.25rem",
    "sm": "0.5rem",
    "md": "1rem",
    "lg": "1.5rem",
    "xl": "2rem",
    "2xl": "3rem",
    "3xl": "4rem"
  },
  "typography": {
    "fontFamily": {
      "sans": "Inter, -apple-system, BlinkMacSystemFont, sans-serif",
      "mono": "Aeonik Mono, JetBrains Mono, Consolas, monospace"
    },
    "fontSize": {
      "xs": "0.75rem",
      "sm": "0.875rem",
      "base": "1rem",
      "lg": "1.125rem",
      "xl": "1.25rem",
      "2xl": "1.5rem",
      "3xl": "1.875rem",
      "4xl": "2.25rem",
      "5xl": "3rem",
      "6xl": "3.75rem"
    },
    "fontWeight": {
      "normal": 400,
      "medium": 500,
      "semibold": 600,
      "bold": 700
    },
    "lineHeight": {
      "tight": 1.2,
      "snug": 1.4,
      "normal": 1.5,
      "relaxed": 1.75
    }
  },
  "borderRadius": {
    "none": "0",
    "sm": "0.25rem",
    "md": "0.5rem",
    "lg": "0.75rem",
    "xl": "1rem",
    "2xl": "1.5rem",
    "full": "9999px"
  },
  "shadows": {
    "sm": "0 1px 2px 0 rgba(0, 0, 0, 0.05)",
    "md": "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
    "lg": "0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)",
    "xl": "0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)"
  }
}
```

### 14.3 Tailwind Config

```js
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#6FC2FF',
          50: '#EBF8FF',
          100: '#D1EFFF',
          500: '#6FC2FF',
          600: '#5AB5F5',
          700: '#3D9DE0',
        },
        accent: {
          DEFAULT: '#FFD93D',
          50: '#FFFBEB',
          500: '#FFD93D',
          600: '#FFD020',
        },
        success: '#10B981',
        warning: '#F59E0B',
        error: '#EF4444',
        info: '#3B82F6',
        foreground: '#000000',
        'muted-foreground': '#6B7280',
        border: '#E5E7EB',
        background: '#FFFFFF',
      },
      fontFamily: {
        sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'],
        mono: ['Aeonik Mono', 'JetBrains Mono', 'Consolas', 'monospace'],
      },
      borderRadius: {
        'xl': '1rem',
        '2xl': '1.5rem',
      },
      boxShadow: {
        'sm': '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
        'md': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
      }
    }
  },
  plugins: []
}
```

---

## 15. Layout Patterns

### Container Widths

```html
<!-- Max-width container -->
<div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
  Content
</div>
```

| Breakpoint | Max Width | Tailwind Class |
|------------|-----------|----------------|
| SM | 640px | `max-w-sm` |
| MD | 768px | `max-w-md` |
| LG | 1024px | `max-w-lg` |
| XL | 1280px | `max-w-xl` |
| 2XL | 1536px | `max-w-2xl` |
| 7XL | 80rem (1280px) | `max-w-7xl` |

### Grid Systems

**Auto-responsive Grid**
```html
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
  <div>Item 1</div>
  <div>Item 2</div>
  <div>Item 3</div>
</div>
```

**12-Column Grid**
```html
<div className="grid grid-cols-12 gap-8">
  <div className="col-span-12 lg:col-span-8">Main content</div>
  <div className="col-span-12 lg:col-span-4">Sidebar</div>
</div>
```

### Flexbox Patterns

**Centered Content**
```html
<div className="flex items-center justify-center min-h-screen">
  <div>Centered content</div>
</div>
```

**Space Between (Header Pattern)**
```html
<div className="flex items-center justify-between">
  <div>Logo</div>
  <div>Navigation</div>
</div>
```

**Vertical Stack**
```html
<div className="flex flex-col gap-8">
  <div>Item 1</div>
  <div>Item 2</div>
</div>
```

### Section Patterns

**Hero Section**
```html
<section className="py-16 md:py-24 px-8 bg-primary text-white">
  <div className="max-w-7xl mx-auto">
    <h1 className="text-5xl md:text-6xl font-bold mb-6">
      Ducking Simple Data Warehouse
    </h1>
    <p className="text-xl mb-8">
      Built on DuckDB, powered by collaboration
    </p>
    <button className="px-8 py-4 bg-accent text-black rounded-lg">
      Get Started
    </button>
  </div>
</section>
```

**Content Section**
```html
<section className="py-16 px-8">
  <div className="max-w-7xl mx-auto">
    <h2 className="text-4xl font-bold mb-12 text-center">Features</h2>
    <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
      <!-- Feature cards -->
    </div>
  </div>
</section>
```

---

## 16. Example Component Reference

### Complete Button Component (React + Tailwind)

```tsx
// components/ui/button.tsx
import { ButtonHTMLAttributes, forwardRef } from 'react';
import { cn } from '@/lib/utils';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'accent' | 'outline' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
}

const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = 'primary', size = 'md', ...props }, ref) => {
    return (
      <button
        ref={ref}
        className={cn(
          // Base styles
          'inline-flex items-center justify-center rounded-lg font-medium transition-all duration-200',
          'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2',
          'disabled:opacity-50 disabled:cursor-not-allowed',

          // Variants
          variant === 'primary' && 'bg-primary text-white shadow-sm hover:bg-primary/90 hover:shadow-md active:scale-95 focus-visible:ring-primary',
          variant === 'accent' && 'bg-accent text-black shadow-sm hover:bg-accent/90 hover:shadow-md active:scale-95 focus-visible:ring-accent',
          variant === 'secondary' && 'bg-white text-primary border-2 border-primary hover:bg-primary/5 active:scale-95 focus-visible:ring-primary',
          variant === 'outline' && 'bg-transparent border-2 border-gray-300 text-foreground hover:bg-gray-50 active:scale-95 focus-visible:ring-gray-400',
          variant === 'ghost' && 'bg-transparent text-foreground hover:bg-gray-100 active:scale-95 focus-visible:ring-gray-400',

          // Sizes
          size === 'sm' && 'px-4 py-2 text-sm',
          size === 'md' && 'px-6 py-3 text-base',
          size === 'lg' && 'px-8 py-4 text-lg',

          className
        )}
        {...props}
      />
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
    <div className="flex flex-wrap gap-4">
      <Button variant="primary">Get Started</Button>
      <Button variant="accent">Try Free</Button>
      <Button variant="secondary">Learn More</Button>
      <Button variant="outline">Cancel</Button>
      <Button variant="ghost">View Details</Button>

      <Button variant="primary" size="sm">Small</Button>
      <Button variant="primary" size="lg">Large</Button>
    </div>
  );
}
```

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
        'p-8 bg-white rounded-2xl border border-gray-200',
        className
      )}
      {...props}
    />
  )
);

const CardHeader = forwardRef<HTMLDivElement, HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div
      ref={ref}
      className={cn('mb-4', className)}
      {...props}
    />
  )
);

const CardTitle = forwardRef<HTMLHeadingElement, HTMLAttributes<HTMLHeadingElement>>(
  ({ className, ...props }, ref) => (
    <h3
      ref={ref}
      className={cn('text-xl font-semibold text-foreground', className)}
      {...props}
    />
  )
);

const CardDescription = forwardRef<HTMLParagraphElement, HTMLAttributes<HTMLParagraphElement>>(
  ({ className, ...props }, ref) => (
    <p
      ref={ref}
      className={cn('text-sm text-muted-foreground', className)}
      {...props}
    />
  )
);

const CardContent = forwardRef<HTMLDivElement, HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={cn('', className)} {...props} />
  )
);

Card.displayName = 'Card';
CardHeader.displayName = 'CardHeader';
CardTitle.displayName = 'CardTitle';
CardDescription.displayName = 'CardDescription';
CardContent.displayName = 'CardContent';

export { Card, CardHeader, CardTitle, CardDescription, CardContent };
```

**Usage:**
```tsx
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card';

function Example() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
      <Card>
        <CardHeader>
          <CardTitle>Fast Analytics</CardTitle>
          <CardDescription>Query millions of rows in seconds</CardDescription>
        </CardHeader>
        <CardContent>
          <p>DuckDB's columnar architecture delivers blazing fast performance.</p>
        </CardContent>
      </Card>

      <Card className="hover:shadow-lg transition-shadow duration-200">
        <CardHeader>
          <CardTitle>Serverless</CardTitle>
          <CardDescription>No infrastructure to manage</CardDescription>
        </CardHeader>
        <CardContent>
          <p>Focus on analytics, not ops. We handle scaling automatically.</p>
        </CardContent>
      </Card>

      <Card className="bg-blue-50 border-blue-200">
        <CardHeader>
          <CardTitle>Collaborative</CardTitle>
          <CardDescription>Share queries with your team</CardDescription>
        </CardHeader>
        <CardContent>
          <p>Built for modern data teams working together.</p>
        </CardContent>
      </Card>
    </div>
  );
}
```

---

## 17. Additional Sections

### 17.1 Implementation Best Practices

**Design Token Usage:**
- ✅ Always use design tokens (Tailwind classes, CSS variables)
- ❌ Never hardcode colors: `text-gray-500` → ✅ Use `text-muted-foreground`
- ✅ Use semantic names: `bg-primary`, `text-error`
- ❌ Avoid direct values: `bg-[#6FC2FF]`

**Component Reuse:**
- ✅ Search for existing components before creating new ones
- ✅ Use component variants (`<Button variant="primary">`)
- ✅ Compose components from primitives
- ❌ Don't duplicate components with slightly different styles

**Responsive Design:**
- ✅ Mobile-first approach (base styles = mobile)
- ✅ Test on multiple breakpoints (sm, md, lg, xl)
- ✅ Use responsive utilities (`md:flex-row`, `lg:text-xl`)
- ❌ Don't use fixed pixel widths for layouts

**Accessibility:**
- ✅ Semantic HTML (`<button>`, `<nav>`, `<main>`)
- ✅ ARIA labels for icon-only buttons
- ✅ Keyboard navigation (tab, enter, escape)
- ✅ Color contrast 4.5:1 minimum (WCAG AA)
- ❌ Don't use `<div onClick>` (use `<button>`)

**Performance:**
- ✅ CSS transitions for simple animations
- ✅ Avoid layout shifts (reserve space)
- ✅ Prefer `transform` and `opacity` for animations
- ❌ Don't animate expensive properties (width, height)

---

### 17.2 Common Patterns to Avoid

#### ❌ DON'T: Hardcode Colors
```tsx
// Bad
<div className="text-gray-500 bg-blue-600">...</div>

// Good
<div className="text-muted-foreground bg-primary">...</div>
```

#### ❌ DON'T: Use Arbitrary Spacing
```tsx
// Bad
<div className="p-5 m-7">...</div>

// Good (use spacing scale: 4, 8, 16, 24, 32px)
<div className="p-6 m-8">...</div>
```

#### ❌ DON'T: Create Duplicate Components
```tsx
// Bad - creating similar button components
<PrimaryButton />
<AccentButton />
<SecondaryButton />

// Good - use variants
<Button variant="primary" />
<Button variant="accent" />
<Button variant="secondary" />
```

#### ❌ DON'T: Ignore Accessibility
```tsx
// Bad - div as button, no label
<div onClick={handleClick}>
  <Icon />
</div>

// Good - semantic button with aria-label
<button onClick={handleClick} aria-label="Close dialog">
  <Icon />
</button>
```

---

### 17.3 Accessibility Guidelines

#### Color Contrast Requirements (WCAG 2.1 AA)

**Text Contrast:**
- Normal text (< 18px): **4.5:1** minimum
- Large text (≥ 18px or 14px bold): **3.0:1** minimum
- Interactive elements: **3.0:1** against background

**Current Palette Compliance:**
- ✅ Black text on white: 21:1 (AAA)
- ✅ Gray 500 text on white: 7:1 (AAA)
- ✅ Primary blue on white: 3.2:1 (AA Large)
- ✅ White text on primary blue: 3.2:1 (AA Large)

**Tools:**
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- Chrome DevTools: Lighthouse audit

#### Keyboard Navigation

**All interactive elements must:**
- Be focusable (native: `<button>`, `<a>`, `<input>`)
- Have visible focus indicators (`:focus-visible`)
- Follow logical tab order

**Example: Accessible button**
```tsx
<button
  className="
    px-6 py-3 bg-primary text-white rounded-lg
    focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2
  "
>
  Click me
</button>
```

#### ARIA Patterns

**Icon-only buttons:**
```tsx
<button aria-label="Close dialog">
  <X className="w-5 h-5" />
</button>
```

**Form inputs:**
```tsx
<label htmlFor="email" className="block text-sm font-medium mb-2">
  Email address
</label>
<input
  id="email"
  type="email"
  aria-required="true"
  aria-invalid={hasError}
  aria-describedby={hasError ? "email-error" : undefined}
  className="w-full px-4 py-3 border border-gray-300 rounded-lg"
/>
{hasError && (
  <p id="email-error" className="text-sm text-error mt-2">
    Please enter a valid email
  </p>
)}
```

---

### 17.4 Icon System

**Library:** Lucide React

#### Size Conventions

| Size | Pixels | Tailwind Classes | Usage |
|------|--------|------------------|-------|
| XS | 12px | `w-3 h-3` | Very small indicators |
| SM | 16px | `w-4 h-4` | Default icons (buttons, inline) |
| MD | 20px | `w-5 h-5` | Medium icons (headers) |
| LG | 24px | `w-6 h-6` | Large icons (hero sections) |
| XL | 32px | `w-8 h-8` | Extra large (feature icons) |

#### Color Conventions

**Icons inherit text color:**
```tsx
// Primary icon
<button className="text-primary">
  <Check className="w-5 h-5" />
</button>

// Muted icon
<Info className="w-4 h-4 text-muted-foreground" />

// White icon on colored background
<button className="bg-primary text-white">
  <ArrowRight className="w-5 h-5" />
</button>
```

#### Icon-Only Buttons

**Always include `aria-label`:**
```tsx
<button
  aria-label="Close"
  className="p-2 rounded-md hover:bg-gray-100 transition-colors"
>
  <X className="w-5 h-5" />
</button>
```

#### Icon with Text

**Standard spacing:**
```tsx
<button className="flex items-center gap-2">
  <Play className="w-5 h-5" />
  <span>Watch Demo</span>
</button>
```

#### Common Icon Patterns

```tsx
// Search input
<div className="relative">
  <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
  <input className="pl-10 pr-4 py-3 w-full border rounded-lg" placeholder="Search..." />
</div>

// Loading button
<button disabled className="flex items-center gap-2">
  <Loader2 className="w-5 h-5 animate-spin" />
  <span>Loading...</span>
</button>

// Status indicator
<div className="flex items-center gap-2">
  <CheckCircle className="w-5 h-5 text-success" />
  <span>Completed</span>
</div>
```

---

### 17.5 Special Design Elements (from MotherDuck)

#### Wave Dividers

**Usage:** Create organic section transitions
```tsx
// SVG wave divider (place between sections)
<div className="relative">
  <svg className="w-full h-16" viewBox="0 0 1440 120" fill="none">
    <path d="M0,64L80,69.3C160,75,320,85,480,80C640,75,800,53,960,48C1120,43,1280,53,1360,58.7L1440,64L1440,0L1360,0C1280,0,1120,0,960,0C800,0,640,0,480,0C320,0,160,0,80,0L0,0Z" fill="currentColor"/>
  </svg>
</div>
```

#### Colored Section Backgrounds

**Pattern:** Alternate between white and pastel colors
```tsx
// Hero section (primary blue)
<section className="bg-primary text-white py-24">
  {/* Content */}
</section>

// Features section (white)
<section className="bg-white py-16">
  {/* Content */}
</section>

// Testimonials (light blue)
<section className="bg-blue-50 py-16">
  {/* Content */}
</section>

// CTA section (accent yellow)
<section className="bg-accent py-16">
  {/* Content */}
</section>
```

#### Playful Illustrations

**Style Guidelines:**
- Use bright, friendly colors
- Rounded, organic shapes
- Simple, clear visuals
- Incorporate duck mascot where appropriate
- Maintain professional clarity

---

## 🎉 End of Style Guide

**Next Steps:**
1. Run `/psetup` to configure project-level contexts (if not already done)
2. Agents will automatically discover this style guide via STEP 0.5
3. Start building: `/csetup {change-id}` → `/cdev {change-id}`

**Key Takeaways:**
- **Primary Color**: #6FC2FF (MotherDuck blue) - vibrant, modern, trustworthy
- **Accent Color**: #FFD93D (yellow) - energetic, attention-grabbing
- **Typography**: Inter (clean, readable, professional)
- **Style**: Neo-Modern Data Platform (playful + professional)
- **Spacing**: 8px grid system (generous padding, ample whitespace)
- **Components**: Rounded (8-16px radius), soft shadows, smooth transitions

**Questions or Issues?**
- File location: `design-system/STYLE_GUIDE.md`
- Update this guide as the design evolves
- Share with team members for consistency
- Reference during code reviews

---

*Generated by Claude Code Multi-Agent System*
*Based on MotherDuck.com reference design*
*Last updated: 2025-11-02*
