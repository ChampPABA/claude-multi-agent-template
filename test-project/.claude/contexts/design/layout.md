# Layout Patterns

> **Purpose:** Common layout structures and alignment strategies

---

## Core Layout Principles

1. **Box Model First** - Understand all elements as boxes (see `box-thinking.md`)
2. **Flex for 1D** - Use flexbox for single-axis layouts (rows or columns)
3. **Grid for 2D** - Use CSS Grid for multi-axis layouts (rows AND columns)
4. **Responsive by Default** - Design mobile-first, enhance for larger screens

---

## Common Layout Patterns

### 1. Stack (Vertical)

**Use for:** Form fields, article content, vertical lists

```css
.stack {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-4);  /* 16px */
}

/* Variants */
.stack-tight {
  gap: var(--spacing-2);  /* 8px */
}

.stack-loose {
  gap: var(--spacing-8);  /* 32px */
}
```

**HTML:**
```html
<div class="stack">
  <div>Item 1</div>
  <div>Item 2</div>
  <div>Item 3</div>
</div>
```

---

### 2. Inline (Horizontal)

**Use for:** Button groups, breadcrumbs, navigation

```css
.inline {
  display: flex;
  flex-direction: row;
  gap: var(--spacing-4);  /* 16px */
  align-items: center;  /* Vertical centering */
}

/* Variants */
.inline-start {
  justify-content: flex-start;  /* Left-aligned */
}

.inline-center {
  justify-content: center;  /* Centered */
}

.inline-end {
  justify-content: flex-end;  /* Right-aligned */
}

.inline-between {
  justify-content: space-between;  /* Space between items */
}
```

---

### 3. Sidebar Layout

**Use for:** Dashboard, admin panels, documentation

```css
.sidebar-layout {
  display: grid;
  grid-template-columns: 250px 1fr;  /* Fixed sidebar + fluid main */
  gap: var(--spacing-6);  /* 24px */
  min-height: 100vh;
}

@media (max-width: 768px) {
  .sidebar-layout {
    grid-template-columns: 1fr;  /* Stack on mobile */
  }
}
```

**HTML:**
```html
<div class="sidebar-layout">
  <aside class="sidebar">Sidebar</aside>
  <main class="main-content">Main Content</main>
</div>
```

---

### 4. Holy Grail Layout

**Use for:** Classic web pages (header, sidebar, content, footer)

```css
.holy-grail {
  display: grid;
  grid-template-areas:
    "header header header"
    "sidebar main aside"
    "footer footer footer";
  grid-template-columns: 200px 1fr 200px;
  grid-template-rows: auto 1fr auto;
  min-height: 100vh;
  gap: var(--spacing-4);
}

.header { grid-area: header; }
.sidebar { grid-area: sidebar; }
.main { grid-area: main; }
.aside { grid-area: aside; }
.footer { grid-area: footer; }

@media (max-width: 1024px) {
  .holy-grail {
    grid-template-areas:
      "header"
      "main"
      "sidebar"
      "aside"
      "footer";
    grid-template-columns: 1fr;
  }
}
```

---

### 5. Card Grid

**Use for:** Product listings, portfolios, image galleries

```css
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: var(--spacing-6);  /* 24px */
}

/* Auto-fill: Creates as many columns as fit */
/* minmax(300px, 1fr): Min 300px, max equal width */
```

**Responsive Behavior:**
- Mobile: 1 column
- Tablet: 2 columns
- Desktop: 3-4 columns (auto-adjusts)

---

### 6. Center Element

**Use for:** Modals, empty states, landing hero sections

```css
/* Flexbox method */
.center-flex {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
}

/* Grid method */
.center-grid {
  display: grid;
  place-items: center;  /* Shorthand for center both axes */
  min-height: 100vh;
}

/* Absolute positioning (legacy) */
.center-absolute {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
```

---

### 7. Header with Navigation

**Use for:** Site headers, app nav bars

```css
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-4) var(--spacing-6);
  background: white;
  box-shadow: var(--shadow-sm);
}

.nav {
  display: flex;
  gap: var(--spacing-6);
}

@media (max-width: 768px) {
  .nav {
    display: none;  /* Hide on mobile (use hamburger menu) */
  }
}
```

---

### 8. Container (Max-Width)

**Use for:** Constraining content width for readability

```css
.container {
  max-width: 1280px;  /* Desktop max width */
  margin-left: auto;
  margin-right: auto;
  padding-left: var(--spacing-6);  /* 24px */
  padding-right: var(--spacing-6);
}

/* Variants */
.container-narrow {
  max-width: 768px;  /* Blog posts, forms */
}

.container-wide {
  max-width: 1536px;  /* Dashboards, wide layouts */
}
```

**Optimal Reading Widths:**
- Text content: 65-75 characters per line (~768px)
- Dashboard: 1280-1536px
- Full-width: No max-width (use sparingly)

---

## Alignment Strategies

### Flexbox Alignment

**Main Axis (justify-content):**
```css
.flex-start { justify-content: flex-start; }    /* Left/Top */
.flex-center { justify-content: center; }       /* Center */
.flex-end { justify-content: flex-end; }        /* Right/Bottom */
.flex-between { justify-content: space-between; } /* Space between */
.flex-around { justify-content: space-around; }  /* Space around */
```

**Cross Axis (align-items):**
```css
.items-start { align-items: flex-start; }   /* Top/Left */
.items-center { align-items: center; }      /* Center */
.items-end { align-items: flex-end; }       /* Bottom/Right */
.items-stretch { align-items: stretch; }    /* Stretch to fill */
```

### Grid Alignment

```css
/* Place items (both axes) */
.place-center { place-items: center; }
.place-start { place-items: start; }
.place-end { place-items: end; }

/* Justify/align individual item */
.justify-self-center { justify-self: center; }
.align-self-center { align-self: center; }
```

---

## Z-Index Layering

**Standard Z-Index Scale:**

```css
:root {
  --z-base: 1;          /* Base content */
  --z-dropdown: 10;     /* Dropdowns, popovers */
  --z-sticky: 20;       /* Sticky headers */
  --z-modal-backdrop: 100;  /* Modal overlays */
  --z-modal: 110;       /* Modal content */
  --z-popover: 200;     /* Tooltips, toasts */
  --z-notification: 1000;   /* Notifications (top layer) */
}
```

**Usage:**
```css
.content { z-index: var(--z-base); }
.dropdown { z-index: var(--z-dropdown); }
.modal-backdrop { z-index: var(--z-modal-backdrop); }
.modal { z-index: var(--z-modal); }
.toast { z-index: var(--z-notification); }
```

---

## Aspect Ratios

**Use for:** Images, videos, cards with consistent proportions

```css
/* Modern approach (aspect-ratio property) */
.aspect-square { aspect-ratio: 1 / 1; }    /* 1:1 */
.aspect-video { aspect-ratio: 16 / 9; }    /* 16:9 */
.aspect-portrait { aspect-ratio: 3 / 4; }  /* 3:4 */

/* Legacy approach (padding-bottom hack) */
.aspect-ratio-16-9 {
  position: relative;
  padding-bottom: 56.25%;  /* 9/16 = 0.5625 */
}

.aspect-ratio-16-9 > * {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
```

---

## Best Practices

### DO:
- ✅ Use flexbox for 1D layouts
- ✅ Use grid for 2D layouts
- ✅ Design mobile-first (stack by default)
- ✅ Use semantic HTML (header, main, aside, footer)
- ✅ Constrain content width for readability
- ✅ Use CSS custom properties for spacing
- ✅ Test on all screen sizes

### DON'T:
- ❌ Use floats for layouts (legacy technique)
- ❌ Use fixed pixel widths (not responsive)
- ❌ Nest too many layout containers (keep it flat)
- ❌ Forget semantic HTML
- ❌ Use arbitrary z-index values (100, 9999)
- ❌ Overcomplicate layouts (KISS principle)

---

## Quick Reference

**Layout Techniques:**
| Pattern | Technique | Use Case |
|---------|-----------|----------|
| Stack | Flexbox (column) | Vertical lists, forms |
| Inline | Flexbox (row) | Horizontal groups, nav |
| Sidebar | Grid (2 columns) | Admin panels, docs |
| Card Grid | Grid (auto-fill) | Products, galleries |
| Center | Flexbox/Grid | Modals, empty states |

**Container Widths:**
| Type | Max Width | Use Case |
|------|-----------|----------|
| Narrow | 768px | Blog posts, forms |
| Default | 1280px | Standard pages |
| Wide | 1536px | Dashboards |
| Full | none | Landing pages |

**Z-Index Layers:**
| Layer | Z-Index | Element Type |
|-------|---------|--------------|
| Base | 1 | Content |
| Dropdown | 10 | Dropdowns, popovers |
| Modal | 100-110 | Modals, overlays |
| Notification | 1000 | Toasts, alerts |

---

**💡 Remember:** Good layout is invisible. Users should focus on content, not structure!
