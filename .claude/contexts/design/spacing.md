# Spacing System

> **Purpose:** Consistent spacing scale for layouts, components, and rhythm

---

## Base Unit Approach

**Core Principle:** All spacing should be multiples of a base unit for consistency

```css
--spacing: 0.25rem;  /* 4px - Base spacing unit (at default 16px root font size) */
```

**Why 0.25rem (4px)?**
- ✅ Divisible by 2, 4, 8 (common design ratios)
- ✅ Works with 8px grid systems (common in Figma, Sketch)
- ✅ Small enough for fine-tuning
- ✅ Large enough to be visually meaningful

---

## Spacing Scale

### Standard Scale (Multiples of Base)

| Token | Value | Pixels | Common Use Case |
|-------|-------|--------|-----------------|
| `spacing-1` | 0.25rem | 4px | Tiny gaps (icon padding, tight spacing) |
| `spacing-2` | 0.5rem | 8px | Small gaps (button padding, input padding) |
| `spacing-3` | 0.75rem | 12px | Medium gaps (card padding, list items) |
| `spacing-4` | 1rem | 16px | Default gaps (section spacing, form fields) |
| `spacing-5` | 1.25rem | 20px | Between default and large |
| `spacing-6` | 1.5rem | 24px | Large gaps (component spacing, cards) |
| `spacing-8` | 2rem | 32px | XL gaps (section margins, page headers) |
| `spacing-10` | 2.5rem | 40px | XXL gaps (major sections) |
| `spacing-12` | 3rem | 48px | XXXL gaps (page margins, hero sections) |
| `spacing-16` | 4rem | 64px | Huge gaps (full section spacing) |
| `spacing-20` | 5rem | 80px | Extra huge (landing page sections) |
| `spacing-24` | 6rem | 96px | Maximum (hero padding, page dividers) |

### Implementation

```css
:root {
  /* Base unit */
  --spacing-base: 0.25rem;

  /* Scale */
  --spacing-1: calc(var(--spacing-base) * 1);   /* 0.25rem / 4px */
  --spacing-2: calc(var(--spacing-base) * 2);   /* 0.5rem / 8px */
  --spacing-3: calc(var(--spacing-base) * 3);   /* 0.75rem / 12px */
  --spacing-4: calc(var(--spacing-base) * 4);   /* 1rem / 16px */
  --spacing-5: calc(var(--spacing-base) * 5);   /* 1.25rem / 20px */
  --spacing-6: calc(var(--spacing-base) * 6);   /* 1.5rem / 24px */
  --spacing-8: calc(var(--spacing-base) * 8);   /* 2rem / 32px */
  --spacing-10: calc(var(--spacing-base) * 10); /* 2.5rem / 40px */
  --spacing-12: calc(var(--spacing-base) * 12); /* 3rem / 48px */
  --spacing-16: calc(var(--spacing-base) * 16); /* 4rem / 64px */
  --spacing-20: calc(var(--spacing-base) * 20); /* 5rem / 80px */
  --spacing-24: calc(var(--spacing-base) * 24); /* 6rem / 96px */
}
```

---

## Usage Patterns

### Component Padding

**Buttons:**
```css
/* Small button */
.btn-sm {
  padding: var(--spacing-1) var(--spacing-3);  /* 4px 12px */
}

/* Default button */
.btn {
  padding: var(--spacing-2) var(--spacing-4);  /* 8px 16px */
}

/* Large button */
.btn-lg {
  padding: var(--spacing-3) var(--spacing-6);  /* 12px 24px */
}
```

**Cards:**
```css
.card {
  padding: var(--spacing-6);  /* 24px */
}

.card-compact {
  padding: var(--spacing-4);  /* 16px */
}

.card-spacious {
  padding: var(--spacing-8);  /* 32px */
}
```

**Inputs:**
```css
.input {
  padding: var(--spacing-2) var(--spacing-3);  /* 8px 12px */
}

.input-large {
  padding: var(--spacing-3) var(--spacing-4);  /* 12px 16px */
}
```

---

### Component Gaps (Spacing Between Elements)

**Stack (Vertical Spacing):**
```css
/* Tight stack (list items) */
.stack-tight > * + * {
  margin-top: var(--spacing-2);  /* 8px */
}

/* Default stack (form fields) */
.stack > * + * {
  margin-top: var(--spacing-4);  /* 16px */
}

/* Loose stack (sections) */
.stack-loose > * + * {
  margin-top: var(--spacing-8);  /* 32px */
}
```

**Inline (Horizontal Spacing):**
```css
/* Tight inline (breadcrumbs) */
.inline-tight > * + * {
  margin-left: var(--spacing-2);  /* 8px */
}

/* Default inline (button groups) */
.inline > * + * {
  margin-left: var(--spacing-4);  /* 16px */
}

/* Loose inline (navigation items) */
.inline-loose > * + * {
  margin-left: var(--spacing-6);  /* 24px */
}
```

**Grid Gaps:**
```css
/* Tight grid (image galleries) */
.grid-tight {
  gap: var(--spacing-2);  /* 8px */
}

/* Default grid (product listings) */
.grid {
  gap: var(--spacing-4);  /* 16px */
}

/* Loose grid (feature cards) */
.grid-loose {
  gap: var(--spacing-8);  /* 32px */
}
```

---

### Layout Spacing

**Page Margins:**
```css
/* Mobile (small screens) */
.page-container {
  padding: var(--spacing-4);  /* 16px */
}

/* Tablet */
@media (min-width: 640px) {
  .page-container {
    padding: var(--spacing-6);  /* 24px */
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .page-container {
    padding: var(--spacing-8);  /* 32px */
  }
}
```

**Section Spacing:**
```css
/* Between page sections */
.section {
  margin-bottom: var(--spacing-12);  /* 48px */
}

@media (min-width: 1024px) {
  .section {
    margin-bottom: var(--spacing-16);  /* 64px */
  }
}
```

**Component Spacing:**
```css
/* Between components in a section */
.component {
  margin-bottom: var(--spacing-6);  /* 24px */
}
```

---

## Vertical Rhythm

**Definition:** Consistent vertical spacing creates visual harmony

### Line Height + Margin System

```css
/* Typography with rhythm */
p {
  margin-bottom: var(--spacing-4);  /* 16px */
  line-height: 1.5;  /* 24px at 16px font size */
}

h1 {
  margin-bottom: var(--spacing-6);  /* 24px */
  line-height: 1.2;  /* 48px at 40px font size */
}

h2 {
  margin-bottom: var(--spacing-4);  /* 16px */
  line-height: 1.3;  /* 41.6px at 32px font size */
}
```

**Rule:** Margin-bottom should be a multiple of base unit (4px)

---

## White Space

**Principle:** White space (negative space) is as important as content

### Content Density Levels

**Tight (Compact):**
```css
/* Use for: Data tables, dashboards, dense information */
.container-tight {
  padding: var(--spacing-2);  /* 8px */
  gap: var(--spacing-2);      /* 8px */
}
```

**Default (Balanced):**
```css
/* Use for: Standard pages, forms, articles */
.container {
  padding: var(--spacing-4);  /* 16px */
  gap: var(--spacing-4);      /* 16px */
}
```

**Loose (Spacious):**
```css
/* Use for: Landing pages, marketing content, hero sections */
.container-loose {
  padding: var(--spacing-8);  /* 32px */
  gap: var(--spacing-8);      /* 32px */
}
```

---

## Responsive Spacing

### Mobile-First Scaling

```css
/* Mobile (default) */
.section {
  padding: var(--spacing-4);      /* 16px */
  margin-bottom: var(--spacing-8); /* 32px */
}

/* Tablet (640px+) */
@media (min-width: 640px) {
  .section {
    padding: var(--spacing-6);       /* 24px */
    margin-bottom: var(--spacing-12); /* 48px */
  }
}

/* Desktop (1024px+) */
@media (min-width: 1024px) {
  .section {
    padding: var(--spacing-8);       /* 32px */
    margin-bottom: var(--spacing-16); /* 64px */
  }
}
```

**Pattern:** Increase spacing ~1.5-2x per breakpoint

---

## Common Spacing Patterns

### Navigation

```css
/* Header padding */
.header {
  padding: var(--spacing-4) var(--spacing-6);  /* 16px 24px */
}

/* Navigation item spacing */
.nav-item + .nav-item {
  margin-left: var(--spacing-6);  /* 24px */
}
```

### Forms

```css
/* Label to input */
.form-field label {
  margin-bottom: var(--spacing-2);  /* 8px */
}

/* Between form fields */
.form-field + .form-field {
  margin-top: var(--spacing-4);  /* 16px */
}

/* Form groups */
.form-group + .form-group {
  margin-top: var(--spacing-8);  /* 32px */
}
```

### Cards

```css
.card {
  padding: var(--spacing-6);                   /* 24px */
  border-radius: var(--spacing-2);             /* 8px */
}

.card-header {
  margin-bottom: var(--spacing-4);             /* 16px */
  padding-bottom: var(--spacing-4);            /* 16px */
  border-bottom: 1px solid var(--color-border);
}

.card-body {
  padding: var(--spacing-4) 0;                 /* 16px 0 */
}

.card-footer {
  margin-top: var(--spacing-4);                /* 16px */
  padding-top: var(--spacing-4);               /* 16px */
  border-top: 1px solid var(--color-border);
}
```

---

## Best Practices

### DO:
- ✅ Use spacing scale values only (no arbitrary values)
- ✅ Maintain consistent gaps in similar contexts
- ✅ Scale spacing up for larger screens
- ✅ Use generous white space for readability
- ✅ Align spacing with vertical rhythm
- ✅ Test spacing on all screen sizes

### DON'T:
- ❌ Use arbitrary spacing values (e.g., `padding: 13px`)
- ❌ Mix different spacing systems
- ❌ Overcrowd content (too little spacing)
- ❌ Use excessive spacing (too much empty space)
- ❌ Forget to scale spacing responsively
- ❌ Inconsistent spacing for similar elements

---

## Quick Reference

**Component Padding:**
| Component | Padding |
|-----------|---------|
| Button (small) | `spacing-1` `spacing-3` (4px 12px) |
| Button (default) | `spacing-2` `spacing-4` (8px 16px) |
| Button (large) | `spacing-3` `spacing-6` (12px 24px) |
| Input | `spacing-2` `spacing-3` (8px 12px) |
| Card | `spacing-6` (24px) |

**Component Gaps:**
| Context | Gap |
|---------|-----|
| List items | `spacing-2` (8px) |
| Form fields | `spacing-4` (16px) |
| Cards in grid | `spacing-4` to `spacing-6` (16-24px) |
| Page sections | `spacing-12` to `spacing-16` (48-64px) |

**Responsive Scale:**
| Breakpoint | Multiplier |
|------------|------------|
| Mobile (< 640px) | 1x (base) |
| Tablet (640-1024px) | 1.5x |
| Desktop (> 1024px) | 2x |

---

**💡 Remember:** Consistent spacing creates visual rhythm and improves readability!
