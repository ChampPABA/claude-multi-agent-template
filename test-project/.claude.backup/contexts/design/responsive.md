# Responsive Design

> **Purpose:** Adaptive layouts that work across all screen sizes

---

## Mobile-First Philosophy

**Core Principle:** Design for mobile, enhance for desktop

**Why Mobile-First?**
- ✅ Forces prioritization of essential content
- ✅ Better performance (load only what's needed)
- ✅ Easier to scale up than down
- ✅ Matches user behavior (60%+ mobile traffic)

**Implementation:**
```css
/* ✅ Mobile-first (recommended) */
.element {
  /* Mobile styles (default) */
  width: 100%;
}

@media (min-width: 640px) {
  .element {
    /* Tablet styles */
    width: 50%;
  }
}

@media (min-width: 1024px) {
  .element {
    /* Desktop styles */
    width: 33.333%;
  }
}

/* ❌ Desktop-first (avoid) */
.element {
  width: 33.333%;  /* Desktop default */
}

@media (max-width: 1023px) {
  .element {
    width: 50%;  /* Tablet override */
  }
}

@media (max-width: 639px) {
  .element {
    width: 100%;  /* Mobile override */
  }
}
```

---

## Breakpoint System

### 3-Tier Standard Breakpoints

| Tier | Min Width | Target Devices | Common Resolutions |
|------|-----------|----------------|-------------------|
| **Mobile** | < 640px | Phones | 375px, 414px |
| **Tablet** | 640px - 1024px | Tablets, small laptops | 768px, 834px, 1024px |
| **Desktop** | > 1024px | Laptops, desktops | 1280px, 1440px, 1920px |

**Implementation:**
```css
:root {
  --breakpoint-sm: 640px;   /* Tablets */
  --breakpoint-md: 768px;   /* Small laptops */
  --breakpoint-lg: 1024px;  /* Desktops */
  --breakpoint-xl: 1280px;  /* Large desktops */
  --breakpoint-2xl: 1536px; /* Extra large */
}

/* Usage */
@media (min-width: 640px) { /* Tablet+ */ }
@media (min-width: 1024px) { /* Desktop+ */ }
```

---

### Extended Breakpoints (Optional)

**For projects needing more granularity:**

| Size | Min Width | Use Case |
|------|-----------|----------|
| xs | < 480px | Small phones |
| sm | 640px | Tablets |
| md | 768px | Small laptops |
| lg | 1024px | Desktops |
| xl | 1280px | Large desktops |
| 2xl | 1536px | Extra large screens |

---

## Responsive Box Movement

**Core Concept:** Describe layouts in terms of box behavior, not pixels

### Stacking Pattern

**Desktop (Horizontal) → Mobile (Vertical)**

```css
/* Desktop: Side-by-side */
.container {
  display: flex;
  gap: var(--spacing-6);
}

/* Mobile: Stacked */
@media (max-width: 639px) {
  .container {
    flex-direction: column;
  }
}
```

**Visual:**
```
Desktop (> 1024px):
┌────────────┬────────────┐
│ Sidebar    │ Main       │
└────────────┴────────────┘

Mobile (< 640px):
┌────────────┐
│ Main       │
├────────────┤
│ Sidebar    │
└────────────┘
```

---

### Merging Pattern

**Multiple Boxes → Single Unified Box**

```css
/* Desktop: 3 columns */
.grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--spacing-6);
}

/* Tablet: 2 columns */
@media (max-width: 1023px) {
  .grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* Mobile: 1 column */
@media (max-width: 639px) {
  .grid {
    grid-template-columns: 1fr;
  }
}
```

---

### Prioritizing Pattern

**Important Content First, Secondary Content Hidden/Moved**

```css
/* Desktop: Show all */
.header {
  display: flex;
  justify-content: space-between;
}

.nav {
  display: flex;
  gap: var(--spacing-6);
}

/* Mobile: Hide nav, show hamburger */
@media (max-width: 767px) {
  .nav {
    display: none;  /* Hidden by default */
  }

  .nav.open {
    display: flex;
    flex-direction: column;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100vh;
    background: white;
    padding: var(--spacing-6);
  }

  .hamburger {
    display: block;  /* Visible on mobile */
  }
}
```

---

### Compressing Pattern

**Boxes Shrink, Maintain Relationships**

```css
/* Desktop: Generous spacing */
.section {
  padding: var(--spacing-12);  /* 48px */
}

/* Tablet: Medium spacing */
@media (max-width: 1023px) {
  .section {
    padding: var(--spacing-8);  /* 32px */
  }
}

/* Mobile: Compact spacing */
@media (max-width: 639px) {
  .section {
    padding: var(--spacing-4);  /* 16px */
  }
}
```

**Scaling Pattern:** 2x (desktop) → 1.5x (tablet) → 1x (mobile)

---

## Responsive Typography

### Fluid Font Sizes

**Method 1: Breakpoint-Based (Simple)**

```css
/* Mobile */
h1 {
  font-size: 2rem;  /* 32px */
}

/* Tablet */
@media (min-width: 640px) {
  h1 {
    font-size: 2.25rem;  /* 36px */
  }
}

/* Desktop */
@media (min-width: 1024px) {
  h1 {
    font-size: 2.5rem;  /* 40px */
  }
}
```

**Method 2: clamp() Function (Fluid)**

```css
h1 {
  /* min, preferred (scales with viewport), max */
  font-size: clamp(2rem, 4vw, 2.5rem);
  /* 32px minimum, scales between, 40px maximum */
}

h2 {
  font-size: clamp(1.5rem, 3vw, 2rem);
}

p {
  font-size: clamp(1rem, 1.5vw, 1.125rem);
}
```

**Benefits of clamp():**
- ✅ Smoothly scales between breakpoints
- ✅ No media queries needed
- ✅ Better user experience (no jumps)

---

## Responsive Images

### Techniques

**1. Fluid Images (Default)**
```css
img {
  max-width: 100%;
  height: auto;
  display: block;
}
```

**2. Picture Element (Art Direction)**
```html
<picture>
  <!-- Desktop -->
  <source media="(min-width: 1024px)" srcset="hero-desktop.jpg">

  <!-- Tablet -->
  <source media="(min-width: 640px)" srcset="hero-tablet.jpg">

  <!-- Mobile (default) -->
  <img src="hero-mobile.jpg" alt="Hero">
</picture>
```

**3. srcset (Resolution Switching)**
```html
<img
  srcset="image-small.jpg 480w,
          image-medium.jpg 768w,
          image-large.jpg 1200w"
  sizes="(max-width: 640px) 100vw,
         (max-width: 1024px) 50vw,
         33vw"
  src="image-medium.jpg"
  alt="Responsive image"
>
```

**4. Background Images**
```css
.hero {
  background-image: url('hero-mobile.jpg');
  background-size: cover;
  background-position: center;
}

@media (min-width: 640px) {
  .hero {
    background-image: url('hero-tablet.jpg');
  }
}

@media (min-width: 1024px) {
  .hero {
    background-image: url('hero-desktop.jpg');
  }
}
```

---

## Container Queries (Modern)

**Use Case:** Component-specific responsive behavior (not viewport-based)

```css
/* Define container */
.card-container {
  container-type: inline-size;
  container-name: card;
}

/* Query container (not viewport) */
@container card (min-width: 400px) {
  .card {
    display: grid;
    grid-template-columns: 200px 1fr;
  }
}

@container card (max-width: 399px) {
  .card {
    display: block;
  }
}
```

**Benefits:**
- ✅ Component adapts to parent width, not viewport
- ✅ Better for reusable components
- ✅ More predictable behavior

**Browser Support:** Modern browsers (2023+)

---

## Touch & Hover Interactions

### Touch Targets

**Minimum Size:** 44x44px (Apple HIG, WCAG 2.1)

```css
.button {
  min-width: 44px;
  min-height: 44px;
  padding: var(--spacing-2) var(--spacing-4);
}

.icon-button {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
}
```

### Hover vs Touch

**Detect Hover Capability:**
```css
/* Desktop (has hover) */
@media (hover: hover) {
  .button:hover {
    background: var(--color-primary-dark);
  }
}

/* Touch devices (no hover) */
@media (hover: none) {
  .button:active {
    background: var(--color-primary-dark);
  }
}
```

---

## Performance Optimization

### Viewport Meta Tag

**Essential for Mobile:**
```html
<meta name="viewport" content="width=device-width, initial-scale=1">
```

**Without this:** Mobile browsers zoom out to fit desktop layout
**With this:** Mobile browsers render at device width

### Reduce Reflows

**Bad:**
```css
/* Causes layout recalculation */
@media (max-width: 767px) {
  .element {
    width: calc(100% - 20px);  /* Reflow */
    margin-left: 10px;         /* Reflow */
  }
}
```

**Good:**
```css
/* GPU-accelerated properties */
@media (max-width: 767px) {
  .element {
    transform: translateX(10px);  /* No reflow */
    opacity: 0.8;                  /* No reflow */
  }
}
```

---

## Testing Checklist

### Device Testing

**Critical Devices:**
- [ ] iPhone SE (375px) - Smallest modern phone
- [ ] iPhone 14 (390px) - Standard phone
- [ ] iPad (768px) - Tablet
- [ ] iPad Pro (1024px) - Large tablet
- [ ] Desktop (1280px) - Standard desktop
- [ ] Desktop (1920px) - Large desktop

**Browser Testing:**
- [ ] Chrome (mobile + desktop)
- [ ] Safari (iOS + macOS)
- [ ] Firefox
- [ ] Edge

### Visual Testing

**Check for:**
- [ ] Text readability (min 16px on mobile)
- [ ] Touch targets (min 44x44px)
- [ ] Horizontal scrolling (should never happen)
- [ ] Image scaling (proper aspect ratios)
- [ ] Spacing consistency
- [ ] Navigation usability
- [ ] Form field usability

---

## Best Practices

### DO:
- ✅ Design mobile-first (default styles for mobile)
- ✅ Use relative units (rem, em, %, vw, vh)
- ✅ Test on real devices (not just DevTools)
- ✅ Use 3-tier breakpoints (mobile, tablet, desktop)
- ✅ Prioritize essential content on mobile
- ✅ Use touch-friendly targets (min 44x44px)
- ✅ Optimize images for each breakpoint

### DON'T:
- ❌ Use fixed pixel widths
- ❌ Design desktop-first (harder to simplify)
- ❌ Test only in DevTools (real devices behave differently)
- ❌ Use too many breakpoints (3-4 is enough)
- ❌ Hide important content on mobile
- ❌ Use hover-only interactions on touch devices
- ❌ Serve desktop images to mobile

---

## Quick Reference

**Breakpoints:**
| Size | Min Width | Target |
|------|-----------|--------|
| sm | 640px | Tablets |
| md | 768px | Small laptops |
| lg | 1024px | Desktops |
| xl | 1280px | Large desktops |

**Box Movement Patterns:**
| Pattern | Desktop | Mobile |
|---------|---------|--------|
| Stacking | Horizontal | Vertical |
| Merging | 3 columns | 1 column |
| Prioritizing | Show all | Show essential |
| Compressing | 48px spacing | 16px spacing |

**Touch Targets:**
- Minimum: 44x44px
- Spacing: 8px between targets
- Common: 48x48px (generous)

---

**💡 Remember:** Think in terms of box behavior (stack, merge, prioritize), not pixels!
