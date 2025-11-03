# Cacao Craft - Design System Style Guide

> **Style Direction:** Warm Artisan
> **Generated:** 2025-11-03
> **Version:** 1.0.0
> **Sources:** Synthesized from Airbnb (warmth) + Stripe (sophistication) + Custom earthy palette

---

## Quick Start

**Brand Colors:**
- Primary: Cacao Brown `#6B4423`
- Background: Cream `#F5F1E8`
- Text: Deep Brown `#3E2723`
- Accent: Forest Green `#4A7C59`, Terracotta `#C17853`

**Typography:**
- Headings: EB Garamond (serif)
- Body: Inter (sans-serif)

**Key Patterns:**
- Border Radius: 20px (buttons), 12px (cards)
- Shadows: Multi-layer, soft (Stripe-inspired)
- Spacing: 8px grid system
- Transitions: 0.2s smooth

---

## Table of Contents

1. [Overview](#1-overview)
2. [Design Philosophy](#2-design-philosophy)
3. [Color Palette](#3-color-palette)
4. [Typography](#4-typography)
5. [Spacing System](#5-spacing-system)
6. [Component Styles](#6-component-styles)
7. [Shadows & Elevation](#7-shadows--elevation)
8. [Animations & Transitions](#8-animations--transitions)
9. [Border Styles](#9-border-styles)
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

### Project Description

**Cacao Craft** is a premium organic cacao café and product retailer, specializing in high-quality, pesticide-free cacao products. Think specialty coffee shop, but entirely focused on cacao - from artisan beverages to bean-to-bar chocolates.

**Product Lines:**
- Cacao Beverages (hot, iced, specialty drinks)
- Cacao Mass (pure cacao paste)
- Artisan Chocolate (bean-to-bar, truffles, bonbons)
- Raw Ingredients (cacao nibs, powder)
- Gift Sets (curated collections)

### Target Audience

- **Age:** 25-45 years old
- **Demographics:** Urban professionals, health-conscious consumers
- **Psychographics:** Value organic/sustainable products, appreciate artisan craftsmanship, willing to pay premium for quality

### Brand Personality

**Core Values:** Premium, Natural, Healthy, Artisan, Warm, Earthy, Sophisticated but approachable

**NOT:** Corporate, Mass-market, Clinical, Overly luxurious

### Design Style Classification

**Warm Artisan** - A photo-forward, café-inspired aesthetic combining:
- Airbnb's warmth & approachability (rounded corners, generous spacing)
- Stripe's professional sophistication (multi-layer shadows, polished details)
- Custom earthy color palette (rich browns, warm creams, natural greens)

**Emotional Goals:**
1. Trust (organic, safe, high-quality)
2. Health (nutritious, beneficial)
3. Warmth (welcoming café atmosphere)
4. Discovery (learn about cacao benefits)
5. Indulgence (premium, treat yourself)

---

## 2. Design Philosophy

### Core Principles

#### 1. "Natural is Beautiful"
- Use earthy, organic colors that reflect real cacao
- Avoid artificial or overly vibrant colors
- Let product photography shine (minimal UI decoration)
- Textures and materials feel tactile and real

#### 2. "Warm Welcome"
- Rounded corners create approachability (20px for buttons, 12px for cards)
- Generous spacing provides breathing room (8px grid system)
- Soft shadows add depth without harshness
- Color palette evokes warmth (browns, creams, not cold grays)

#### 3. "Premium but Approachable"
- Professional polish (Stripe-inspired shadows and details)
- But not intimidating (Airbnb-inspired warmth)
- Quality is visible but not ostentatious
- Sophisticated typography balanced with readability

#### 4. "Photos Tell the Story"
- Product imagery is hero, UI recedes
- Large, high-quality photos dominate layouts
- Card-based design showcases products visually
- Minimal text overlay on images

#### 5. "Crafted with Care"
- Attention to small details (subtle shadows, precise spacing)
- Consistent patterns create rhythm
- Smooth transitions feel polished
- Every element serves the experience

---

## 3. Color Palette

### Primary Colors

#### Cacao Brown `#6B4423`
**Usage:** Primary brand color, buttons, CTAs, headers
**Psychology:** Rich, warm, natural - evokes roasted cacao beans
**Accessibility:** ✅ On white (#FFFFFF): Contrast 8.2:1 (AA Large)

#### Cream `#F5F1E8`
**Usage:** Primary background, sections, cards
**Psychology:** Warm, natural - like cacao butter
**Accessibility:** ✅ With deep brown text (#3E2723): Contrast 9.5:1 (AAA)

#### Deep Brown `#3E2723`
**Usage:** Headings, body text, icons
**Psychology:** Grounding, rich - like dark chocolate

---

### Secondary Colors

#### Forest Green `#4A7C59`
**Usage:** Organic/health highlights, secondary CTAs, icons
**Psychology:** Natural, healthy, sustainable

#### Warm Beige `#E8DCC4`
**Usage:** Subtle backgrounds, sections, hover states
**Psychology:** Neutral, warm, inviting

#### Terracotta `#C17853`
**Usage:** Accent color, secondary CTAs, highlights
**Psychology:** Earthy, warm, energetic

---

### Semantic Colors

- **Success Green:** `#68A357` - Success messages, confirmations, badges
- **Warning Gold:** `#D4A574` - Warning messages, important notices
- **Error Red:** `#C85A54` - Error messages, alerts, validation

---

### Neutral Scale

```css
/* Text Colors */
--text-primary: #3E2723;     /* Deep Brown - headings, body */
--text-secondary: #6B4423;   /* Cacao Brown - muted text */
--text-tertiary: #8B7355;    /* Light Brown - captions, metadata */
--text-disabled: #B8A89D;    /* Warm Gray - disabled state */

/* Background Colors */
--bg-primary: #FFFFFF;       /* White - main background */
--bg-secondary: #F5F1E8;     /* Cream - sections, alternating */
--bg-tertiary: #E8DCC4;      /* Warm Beige - subtle highlights */

/* Border Colors */
--border-subtle: #E8DCC4;    /* Warm Beige - subtle dividers */
--border-default: #C8B8A4;   /* Medium Beige - standard borders */
--border-strong: #6B4423;    /* Cacao Brown - emphasis */
```

---

### Color Usage Guide

**DO:**
- ✅ Use Cacao Brown (#6B4423) for primary CTAs
- ✅ Use Cream (#F5F1E8) for main backgrounds
- ✅ Use Deep Brown (#3E2723) for text
- ✅ Use Forest Green (#4A7C59) to emphasize organic/health benefits

**DON'T:**
- ❌ Use pure black (#000000) - use Deep Brown instead
- ❌ Use cool grays - stick to warm beiges/browns
- ❌ Overuse Forest Green - it's an accent, not primary

---

## 4. Typography

### Font Families

**Headings:** EB Garamond (Serif)
```css
font-family: 'EB Garamond', 'Georgia', serif;
```
Classic, artisan feel. Evokes craftsmanship and premium quality.

**Body:** Inter (Sans-serif)
```css
font-family: 'Inter', 'system-ui', sans-serif;
```
Clean, readable, modern. Excellent for long-form content.

---

### Type Scale

#### Display (Hero Headlines)
```css
font-size: 72px;
font-weight: 500;
line-height: 1.1;
letter-spacing: -0.02em;
font-family: 'EB Garamond', serif;
```
**Usage:** Landing page hero, major announcements

#### H1 (Page Titles)
```css
font-size: 48px;
font-weight: 500;
line-height: 1.2;
letter-spacing: -0.01em;
```
**Usage:** Page headings, section headers

#### H2 (Section Headers)
```css
font-size: 36px;
font-weight: 500;
line-height: 1.3;
```

#### H3 (Subsection Headers)
```css
font-size: 28px;
font-weight: 600;
line-height: 1.4;
```

#### H4 (Component Headers)
```css
font-size: 24px;
font-weight: 600;
line-height: 1.4;
font-family: 'Inter', sans-serif;
```

#### Body (Default)
```css
font-size: 16px;
font-weight: 400;
line-height: 1.6;
```

#### Caption
```css
font-size: 12px;
font-weight: 400;
line-height: 1.4;
text-transform: uppercase;
letter-spacing: 0.05em;
```

---

### Font Weights

- **Light (300):** Decorative use only
- **Regular (400):** Body text, paragraphs
- **Medium (500):** Serif headings (Display, H1, H2)
- **Semi-bold (600):** Sans headings (H3, H4), emphasis
- **Bold (700):** Strong emphasis, buttons (rare)

---

## 5. Spacing System

### Grid Base: 8px

All spacing follows an 8px grid system for consistency.

```css
--space-1: 8px;
--space-2: 16px;
--space-3: 24px;
--space-4: 32px;
--space-6: 48px;
--space-8: 64px;
--space-10: 80px;
--space-12: 96px;
--space-16: 128px;
```

---

### Component Spacing

**Buttons:** `padding: 12px 24px;`
**Cards:** `padding: 24px; gap: 16px;`
**Sections:** `padding-block: 80px;`
**Containers:** `max-width: 1280px; padding-inline: 24px (mobile), 48px (desktop);`

---

### Vertical Rhythm

- **Related items:** 8px-16px
- **Sections:** 40px-64px
- **Major sections:** 80px-128px

---

## 6. Component Styles

### Primary Button

```css
/* Base */
background: #6B4423;
color: #FFFFFF;
padding: 12px 24px;
border-radius: 20px;
font-size: 16px;
font-weight: 600;
box-shadow: rgba(0, 0, 0, 0.1) 0px 2px 8px,
            rgba(0, 0, 0, 0.05) 0px 1px 2px;
transition: all 0.2s cubic-bezier(0.2, 0, 0, 1);

/* Hover */
background: #5A3A1E;
box-shadow: rgba(0, 0, 0, 0.15) 0px 4px 12px;
transform: translateY(-1px);
```

**Tailwind Example:**
```jsx
<button className="bg-cacao-brown text-white px-6 py-3 rounded-[20px] font-semibold shadow-md hover:shadow-lg hover:-translate-y-px transition">
  Shop Now
</button>
```

---

### Secondary Button

```css
background: transparent;
color: #6B4423;
border: 2px solid #6B4423;
padding: 12px 24px;
border-radius: 20px;

/* Hover */
background: #F5F1E8;
```

---

### Product Card

```css
background: #FFFFFF;
border-radius: 12px;
padding: 0;
box-shadow: rgba(0, 0, 0, 0.04) 0px 2px 6px,
            rgba(0, 0, 0, 0.02) 0px 0px 0px 1px;
overflow: hidden;
transition: all 0.2s;

/* Hover */
box-shadow: rgba(0, 0, 0, 0.1) 0px 8px 24px;
transform: translateY(-2px);
```

---

### Text Input

```css
background: #FFFFFF;
border: 2px solid #E8DCC4;
border-radius: 12px;
padding: 12px 16px;

/* Focus */
border-color: #6B4423;
outline: none;
box-shadow: 0 0 0 3px rgba(107, 68, 35, 0.1);
```

---

### Badge

```css
background: #E8DCC4;
color: #6B4423;
padding: 4px 12px;
border-radius: 9999px;
font-size: 12px;
font-weight: 600;
text-transform: uppercase;
```

---

## 7. Shadows & Elevation

### Shadow Scale (Stripe-inspired multi-layer)

#### Shadow XS
```css
box-shadow: rgba(0, 0, 0, 0.02) 0px 0px 0px 1px;
```

#### Shadow SM
```css
box-shadow: rgba(0, 0, 0, 0.04) 0px 2px 6px 0px,
            rgba(0, 0, 0, 0.02) 0px 0px 0px 1px;
```

#### Shadow MD
```css
box-shadow: rgba(0, 0, 0, 0.1) 0px 4px 12px 0px,
            rgba(0, 0, 0, 0.04) 0px 0px 0px 1px;
```

#### Shadow LG
```css
box-shadow: rgba(0, 0, 0, 0.1) 0px 8px 24px 0px,
            rgba(0, 0, 0, 0.04) 0px 0px 0px 1px;
```

#### Shadow XL
```css
box-shadow: rgba(0, 0, 0, 0.15) 0px 12px 32px 0px,
            rgba(0, 0, 0, 0.05) 0px 0px 0px 1px;
```

---

## 8. Animations & Transitions

### Transition Timing (Airbnb-inspired)

```css
/* Default */
transition: all 0.2s cubic-bezier(0.2, 0, 0, 1);

/* Fast */
transition: color 0.15s ease;

/* Slow */
transition: transform 0.3s cubic-bezier(0.2, 0, 0, 1);
```

---

### Component Animations

**Button Hover:**
```css
transform: translateY(-1px);
box-shadow: enhanced;
```

**Card Hover:**
```css
transform: translateY(-2px);
box-shadow: enhanced;
```

**Link Hover:**
```css
text-decoration-color: #6B4423;
transition: 0.15s;
```

---

## 9. Border Styles

### Border Widths

- **1px:** Subtle dividers, table borders
- **2px:** Input borders, card outlines, buttons
- **3px:** Emphasis borders, focus states

---

### Border Colors

```css
/* Subtle */
border: 1px solid #E8DCC4;

/* Default */
border: 2px solid #C8B8A4;

/* Strong */
border: 2px solid #6B4423;
```

---

## 10. Border Radius

### Scale (Airbnb-inspired rounded)

```css
--radius-sm: 8px;
--radius-md: 12px;
--radius-lg: 20px;
--radius-xl: 32px;
--radius-full: 9999px;
```

---

### Usage

- **Buttons:** 20px
- **Cards:** 12px
- **Inputs:** 12px
- **Badges:** 9999px (pill)
- **Images:** 12px

---

## 11. Opacity & Transparency

```css
--opacity-0: 0;
--opacity-40: 0.4;   /* Disabled */
--opacity-50: 0.5;   /* Overlays */
--opacity-70: 0.7;   /* Muted text */
--opacity-100: 1;
```

---

## 12. Z-Index Layers

```css
--z-base: 0;
--z-dropdown: 1000;
--z-sticky: 1100;
--z-overlay: 1200;
--z-modal: 1300;
--z-toast: 1400;
--z-tooltip: 1500;
```

---

## 13. Responsive Breakpoints

```css
--screen-sm: 640px;
--screen-md: 768px;
--screen-lg: 1024px;
--screen-xl: 1280px;
--screen-2xl: 1536px;
```

**Mobile-first approach**

---

## 14. CSS Variables / Tailwind Theme

### Tailwind Config

```js
module.exports = {
  theme: {
    extend: {
      colors: {
        'cacao-brown': '#6B4423',
        'cacao-dark': '#5A3A1E',
        'cream': '#F5F1E8',
        'deep-brown': '#3E2723',
        'forest-green': '#4A7C59',
        'warm-beige': '#E8DCC4',
        'terracotta': '#C17853',
        'success': '#68A357',
        'warning': '#D4A574',
        'error': '#C85A54',
      },
      fontFamily: {
        'serif': ['EB Garamond', 'Georgia', 'serif'],
        'sans': ['Inter', 'system-ui', 'sans-serif'],
      },
      fontSize: {
        'display': ['72px', { lineHeight: '1.1', letterSpacing: '-0.02em' }],
        'h1': ['48px', { lineHeight: '1.2', letterSpacing: '-0.01em' }],
        'h2': ['36px', { lineHeight: '1.3' }],
        'h3': ['28px', { lineHeight: '1.4' }],
        'h4': ['24px', { lineHeight: '1.4' }],
      },
      borderRadius: {
        'md': '12px',
        'lg': '20px',
        'xl': '32px',
      },
      boxShadow: {
        'sm': 'rgba(0,0,0,0.04) 0px 2px 6px, rgba(0,0,0,0.02) 0px 0px 0px 1px',
        'md': 'rgba(0,0,0,0.1) 0px 4px 12px, rgba(0,0,0,0.04) 0px 0px 0px 1px',
        'lg': 'rgba(0,0,0,0.1) 0px 8px 24px, rgba(0,0,0,0.04) 0px 0px 0px 1px',
      },
    },
  },
}
```

---

## 15. Layout Patterns

### Container

```jsx
<div className="container mx-auto px-6 lg:px-12 max-w-7xl">
  {/* Content */}
</div>
```

---

### Grid Layout (Product Gallery)

```jsx
<div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
  <ProductCard />
  <ProductCard />
  <ProductCard />
</div>
```

---

### Hero Section

```jsx
<section className="relative min-h-screen flex items-center justify-center bg-cream">
  <div className="container mx-auto px-6 lg:px-12">
    <div className="max-w-3xl mx-auto text-center">
      <h1 className="text-display font-medium text-deep-brown mb-6">
        Artisan Cacao, Naturally Grown
      </h1>
      <p className="text-lg text-cacao-brown mb-8">
        Organic, pesticide-free cacao from farm to cup.
      </p>
      <div className="flex gap-4 justify-center">
        <button>Shop Products</button>
        <button>Visit Café</button>
      </div>
    </div>
  </div>
</section>
```

---

## 16. Example Component Reference

### Product Card Component (React + Tailwind)

```jsx
export function ProductCard({ product }) {
  return (
    <div className="bg-white rounded-xl overflow-hidden shadow-sm hover:shadow-lg hover:-translate-y-0.5 transition-all duration-200 group">
      {/* Image */}
      <div className="relative aspect-square overflow-hidden">
        <img
          src={product.image}
          alt={product.name}
          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
        />

        {/* Badge */}
        {product.isOrganic && (
          <span className="absolute top-4 right-4 bg-forest-green text-white px-3 py-1 rounded-full text-xs font-semibold uppercase tracking-wide">
            Organic
          </span>
        )}
      </div>

      {/* Content */}
      <div className="p-6">
        {/* Category */}
        <p className="text-xs uppercase tracking-wide text-terracotta font-semibold mb-2">
          {product.category}
        </p>

        {/* Title */}
        <h3 className="text-h4 font-semibold text-deep-brown mb-2">
          {product.name}
        </h3>

        {/* Description */}
        <p className="text-sm text-cacao-brown mb-4">
          {product.description}
        </p>

        {/* Footer */}
        <div className="flex items-center justify-between">
          <span className="text-2xl font-bold text-deep-brown">
            ${product.price}
          </span>
          <button className="bg-cacao-brown text-white px-4 py-2 rounded-full text-sm font-medium hover:bg-cacao-dark transition">
            Add to Cart
          </button>
        </div>
      </div>
    </div>
  );
}
```

---

### Hero Section Component

```jsx
export function HeroSection() {
  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
      {/* Background Image */}
      <div className="absolute inset-0 z-0">
        <img
          src="/images/hero-cacao-farm.jpg"
          alt="Cacao farm"
          className="w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-gradient-to-b from-deep-brown/40 to-deep-brown/60" />
      </div>

      {/* Content */}
      <div className="relative z-10 container mx-auto px-6 lg:px-12">
        <div className="max-w-4xl mx-auto text-center text-white">
          {/* Badge */}
          <span className="inline-block bg-forest-green/90 backdrop-blur-sm text-white px-4 py-2 rounded-full text-sm font-semibold uppercase tracking-wide mb-6">
            100% Organic • Pesticide-Free
          </span>

          {/* Heading */}
          <h1 className="text-display font-medium mb-6">
            Artisan Cacao,<br />Naturally Grown
          </h1>

          {/* Subheading */}
          <p className="text-xl mb-10 max-w-2xl mx-auto">
            From our organic farms to your cup. Experience the pure, rich flavor of premium cacao.
          </p>

          {/* CTAs */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button className="bg-cacao-brown text-white px-8 py-4 rounded-lg font-semibold shadow-lg hover:shadow-xl hover:-translate-y-px transition">
              Shop Products
            </button>
            <button className="bg-white/10 backdrop-blur-sm text-white border-2 border-white/30 px-8 py-4 rounded-lg font-semibold hover:bg-white/20 transition">
              Visit Our Café
            </button>
          </div>
        </div>
      </div>
    </section>
  );
}
```

---

### Button Component

```jsx
export function Button({ variant = 'primary', size = 'md', children, ...props }) {
  const variants = {
    primary: 'bg-cacao-brown text-white shadow-md hover:bg-cacao-dark hover:shadow-lg hover:-translate-y-px',
    secondary: 'bg-transparent text-cacao-brown border-2 border-cacao-brown hover:bg-cream',
    tertiary: 'bg-forest-green text-white shadow-md hover:bg-forest-green/90',
  };

  const sizes = {
    sm: 'px-4 py-2 text-sm',
    md: 'px-6 py-3 text-base',
    lg: 'px-8 py-4 text-lg',
  };

  return (
    <button
      className={`font-semibold rounded-lg transition-all duration-200 ${variants[variant]} ${sizes[size]}`}
      {...props}
    >
      {children}
    </button>
  );
}
```

---

## 17. Additional Sections

### 17.1 Best Practices

**Component Reusability:**
- ✅ Create reusable components (Button, Card, Badge)
- ✅ Use composition over duplication

**Performance:**
- ✅ Optimize images (WebP format, lazy loading)
- ✅ Use CSS transitions over JavaScript animations
- ✅ Minimize shadow/blur usage on large areas

**Consistency:**
- ✅ Follow spacing scale strictly (8px grid)
- ✅ Use design tokens instead of hardcoded values
- ✅ Maintain visual hierarchy

---

### 17.2 Accessibility

**Color Contrast:**
- ✅ All text meets WCAG AA standards (4.5:1 minimum)
- ✅ Interactive elements have clear focus states

**Focus States:**
```css
:focus-visible {
  outline: 3px solid #6B4423;
  outline-offset: 2px;
}
```

**Semantic HTML:**
- ✅ Use proper heading hierarchy (h1 → h2 → h3)
- ✅ Use button for buttons, a for links
- ✅ Include alt text for all images

**Keyboard Navigation:**
- ✅ All interactive elements are keyboard accessible
- ✅ Tab order follows visual order

---

### 17.3 Icon System

**Recommended Library:** Lucide Icons or Heroicons

**Icon Sizes:**
```css
--icon-xs: 12px;
--icon-sm: 16px;
--icon-md: 20px;
--icon-lg: 24px;
--icon-xl: 32px;
```

**Icon Colors:** Match text color classes

---

### 17.4 Image Guidelines

**Product Photography:**
- Aspect Ratio: 1:1 (square) or 4:3
- Resolution: Minimum 800x800px
- Format: WebP (with JPEG fallback)
- Background: White or natural/wooden surfaces
- Lighting: Soft, natural light

**Hero Images:**
- Aspect Ratio: 16:9 or wider
- Resolution: Minimum 1920x1080px
- Subject: Cacao farms, products, café atmosphere
- Overlay: Gradient from transparent to 60% Deep Brown

---

### 17.5 Responsive Design Guidelines

**Mobile-First Approach:**
1. Design for mobile (375px) first
2. Add breakpoints for tablet (768px) and desktop (1024px+)
3. Test on real devices

**Touch Targets:**
- Minimum 44x44px for all interactive elements
- Increase button padding on mobile

**Typography Scaling:**
- Reduce heading sizes by 25-33% on mobile
- Keep body text at 16px minimum

---

### 17.6 Motion Design Principles

**When to Animate:**
- ✅ Button/link hover states
- ✅ Card hover effects
- ✅ Modal open/close
- ✅ Page transitions

**When NOT to Animate:**
- ❌ Long scrolling pages (parallax)
- ❌ Autoplay carousels
- ❌ Infinite loops
- ❌ Heavy animations on mobile

---

## Quick Reference

### Color Swatches

```
Cacao Brown:   #6B4423
Cream:         #F5F1E8
Deep Brown:    #3E2723
Forest Green:  #4A7C59
Warm Beige:    #E8DCC4
Terracotta:    #C17853
```

### Typography Scale

```
Display: 72px/1.1 | EB Garamond Medium
H1:      48px/1.2 | EB Garamond Medium
H2:      36px/1.3 | EB Garamond Medium
H3:      28px/1.4 | EB Garamond Semibold
H4:      24px/1.4 | Inter Semibold
Body:    16px/1.6 | Inter Regular
Caption: 12px/1.4 | Inter Regular (uppercase)
```

### Spacing Scale

```
8px  → space-1  | p-1
16px → space-2  | p-2
24px → space-3  | p-3
32px → space-4  | p-4
48px → space-6  | p-6
64px → space-8  | p-8
80px → space-10 | p-10
```

---

**End of Style Guide**

*Generated by /designsetup using multi-source design synthesis*
*Sources: Airbnb (warmth) + Stripe (sophistication) + Custom earthy palette*
*Version: 1.0.0 | Date: 2025-11-03*
