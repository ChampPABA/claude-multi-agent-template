# Shadow System

> **Purpose:** Consistent elevation and depth hierarchy using shadows

---

## 3-Tier Shadow System

**Core Principle:** Use shadows to indicate elevation, not decoration

**Visual Hierarchy:**
- **Level 1** (Subtle): Barely noticeable, resting state
- **Level 2** (Medium): Elevated, interactive elements
- **Level 3** (Large): Floating, top-layer elements

---

## Shadow Definitions

### Level 1: Subtle (sm)

**Use Cases:**
- Cards at rest
- Input fields
- Buttons (default state)
- List items
- Table rows

**Definition:**
```css
--shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
```

**Breakdown:**
- `0` - No horizontal offset (shadow directly below)
- `1px` - 1px vertical offset (slight drop)
- `2px` - 2px blur radius (soft edge)
- `0` - No spread
- `rgb(0 0 0 / 0.05)` - 5% opacity black (very subtle)

**Example:**
```css
.card {
  box-shadow: var(--shadow-sm);
}

.input {
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--color-border);
}
```

---

### Level 2: Medium (md)

**Use Cases:**
- Dropdowns
- Modals
- Popovers
- Buttons (hover state)
- Cards (hover state)
- Tooltips

**Definition:**
```css
--shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1),
             0 2px 4px -2px rgb(0 0 0 / 0.1);
```

**Breakdown:**
- **First shadow** (main depth):
  - `0 4px 6px -1px` - 4px down, 6px blur, -1px spread (tighter shadow)
  - `rgb(0 0 0 / 0.1)` - 10% opacity
- **Second shadow** (subtle edge):
  - `0 2px 4px -2px` - 2px down, 4px blur, -2px spread (soft edge)
  - `rgb(0 0 0 / 0.1)` - 10% opacity

**Example:**
```css
.dropdown {
  box-shadow: var(--shadow-md);
}

.card:hover {
  box-shadow: var(--shadow-md);
  transition: box-shadow 0.2s ease;
}

.button:hover {
  box-shadow: var(--shadow-md);
}
```

---

### Level 3: Large (lg)

**Use Cases:**
- Full-screen modals
- Overlays
- Mega menus
- Sticky headers
- Notification panels
- Slide-out drawers

**Definition:**
```css
--shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1),
             0 4px 6px -4px rgb(0 0 0 / 0.1);
```

**Breakdown:**
- **First shadow** (main depth):
  - `0 10px 15px -3px` - 10px down, 15px blur, -3px spread
  - `rgb(0 0 0 / 0.1)` - 10% opacity
- **Second shadow** (soft edge):
  - `0 4px 6px -4px` - 4px down, 6px blur, -4px spread
  - `rgb(0 0 0 / 0.1)` - 10% opacity

**Example:**
```css
.modal {
  box-shadow: var(--shadow-lg);
}

.mega-menu {
  box-shadow: var(--shadow-lg);
}

.drawer {
  box-shadow: var(--shadow-lg);
}
```

---

## Optional: Extended Shadow Scale

**For projects needing more granularity:**

```css
/* Extra Subtle (xs) */
--shadow-xs: 0 1px 1px 0 rgb(0 0 0 / 0.03);

/* Subtle (sm) - Standard */
--shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);

/* Medium (md) - Standard */
--shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1),
             0 2px 4px -2px rgb(0 0 0 / 0.1);

/* Large (lg) - Standard */
--shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1),
             0 4px 6px -4px rgb(0 0 0 / 0.1);

/* Extra Large (xl) */
--shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1),
             0 8px 10px -6px rgb(0 0 0 / 0.1);

/* 2XL (maximum elevation) */
--shadow-2xl: 0 25px 50px -12px rgb(0 0 0 / 0.25);
```

---

## Shadow Usage Patterns

### Interactive Elements

**Elevation on Hover:**
```css
.card {
  box-shadow: var(--shadow-sm);
  transition: box-shadow 0.2s ease;
}

.card:hover {
  box-shadow: var(--shadow-md);
}

.card:active {
  box-shadow: var(--shadow-sm);  /* Return to base on click */
}
```

**Buttons:**
```css
.button {
  box-shadow: var(--shadow-sm);
}

.button:hover {
  box-shadow: var(--shadow-md);
}

.button:active {
  box-shadow: none;  /* Pressed down, no elevation */
}
```

---

### Layering

**Z-Index + Shadow Coordination:**

```css
/* Base layer (z-index: 1) */
.content {
  z-index: 1;
  box-shadow: var(--shadow-sm);
}

/* Elevated layer (z-index: 10) */
.dropdown {
  z-index: 10;
  box-shadow: var(--shadow-md);
}

/* Top layer (z-index: 100) */
.modal {
  z-index: 100;
  box-shadow: var(--shadow-lg);
}

/* Notification layer (z-index: 1000) */
.toast {
  z-index: 1000;
  box-shadow: var(--shadow-lg);
}
```

**Rule:** Higher z-index = Larger shadow

---

### Navigation

**Sticky Headers:**
```css
.header {
  position: sticky;
  top: 0;
  box-shadow: none;  /* No shadow when at top */
  transition: box-shadow 0.2s ease;
}

.header.scrolled {
  box-shadow: var(--shadow-md);  /* Add shadow when scrolling */
}
```

**Dropdowns:**
```css
.dropdown-menu {
  position: absolute;
  top: 100%;
  box-shadow: var(--shadow-md);
  border-radius: var(--spacing-2);
}
```

---

## Color Variations

### Subtle Color Shadows

**For Brand Emphasis:**
```css
/* Primary color shadow (blue brand) */
.button-primary:hover {
  box-shadow: 0 4px 6px -1px rgb(59 130 246 / 0.2),
              0 2px 4px -2px rgb(59 130 246 / 0.1);
}

/* Success shadow (green) */
.alert-success {
  box-shadow: 0 1px 2px 0 rgb(34 197 94 / 0.1);
  border-left: 4px solid rgb(34 197 94);
}

/* Error shadow (red) */
.alert-error {
  box-shadow: 0 1px 2px 0 rgb(239 68 68 / 0.1);
  border-left: 4px solid rgb(239 68 68);
}
```

**When to Use:**
- ✅ Highlighting important CTAs
- ✅ Status indicators (success, warning, error)
- ✅ Premium/special features
- ❌ Standard UI elements (use neutral shadows)
- ❌ Overuse (loses emphasis)

---

## Inner Shadows

**Definition:** Shadows inside elements (inset)

**Use Cases:**
- Input fields (focused state)
- Pressed buttons
- Recessed areas

```css
/* Input focus state */
.input:focus {
  outline: none;
  box-shadow: inset 0 1px 2px 0 rgb(0 0 0 / 0.05),
              0 0 0 3px rgb(59 130 246 / 0.2);  /* Focus ring */
}

/* Pressed button */
.button:active {
  box-shadow: inset 0 2px 4px 0 rgb(0 0 0 / 0.1);
}

/* Well/recessed area */
.well {
  box-shadow: inset 0 2px 4px 0 rgb(0 0 0 / 0.06);
  background: var(--color-muted);
}
```

---

## Dark Mode Shadows

**Principle:** Lighter shadows on dark backgrounds

```css
/* Light mode (default) */
:root {
  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);
}

/* Dark mode */
.dark {
  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.5);   /* Stronger contrast */
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.7);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.9);
}
```

**Alternative (White Highlights):**
```css
.dark {
  /* Use subtle white glow instead of black shadow */
  --shadow-sm: 0 1px 2px 0 rgb(255 255 255 / 0.05);
  --shadow-md: 0 4px 6px -1px rgb(255 255 255 / 0.1);
}
```

---

## Performance Considerations

### Shadow vs Border

**Shadow (Better):**
```css
/* Smooth, doesn't affect layout */
.card {
  box-shadow: var(--shadow-sm);
}
```

**Border (Alternative):**
```css
/* Affects layout (adds 1px to dimensions) */
.card {
  border: 1px solid var(--color-border);
}
```

**Hybrid Approach:**
```css
/* Combine subtle shadow + border for definition */
.card {
  box-shadow: var(--shadow-sm);
  border: 1px solid rgb(0 0 0 / 0.05);
}
```

---

### Transition Performance

**Smooth Transitions:**
```css
.card {
  box-shadow: var(--shadow-sm);
  transition: box-shadow 0.2s ease;  /* Fast, smooth */
}

.card:hover {
  box-shadow: var(--shadow-md);
}
```

**Avoid:**
```css
/* ❌ Too slow (feels laggy) */
.card {
  transition: box-shadow 0.5s ease;
}

/* ❌ Multiple properties (can cause jank) */
.card {
  transition: all 0.2s ease;  /* Use specific properties */
}
```

---

## Best Practices

### DO:
- ✅ Use 3-tier system (sm, md, lg)
- ✅ Coordinate shadows with z-index
- ✅ Add shadows on hover for interactivity
- ✅ Use subtle shadows for resting states
- ✅ Increase shadow opacity in dark mode
- ✅ Transition shadows smoothly (0.2s)
- ✅ Use neutral black shadows (rgb(0 0 0))

### DON'T:
- ❌ Use more than 3-4 shadow levels
- ❌ Apply shadows to every element
- ❌ Use harsh shadows (too dark)
- ❌ Mix shadow and border on same edge
- ❌ Forget dark mode adjustments
- ❌ Use slow transitions (> 0.3s)
- ❌ Apply shadows to text (use text-shadow)

---

## Common Patterns

### Card System
```css
.card {
  background: white;
  border-radius: var(--spacing-2);
  padding: var(--spacing-6);
  box-shadow: var(--shadow-sm);
  transition: box-shadow 0.2s ease;
}

.card:hover {
  box-shadow: var(--shadow-md);
}

.card-elevated {
  box-shadow: var(--shadow-md);
}
```

### Modal System
```css
.modal-overlay {
  background: rgb(0 0 0 / 0.5);  /* 50% opacity overlay */
}

.modal-content {
  background: white;
  border-radius: var(--spacing-2);
  padding: var(--spacing-8);
  box-shadow: var(--shadow-lg);
}
```

### Dropdown System
```css
.dropdown-trigger {
  box-shadow: var(--shadow-sm);
}

.dropdown-menu {
  position: absolute;
  background: white;
  border-radius: var(--spacing-2);
  padding: var(--spacing-2);
  box-shadow: var(--shadow-md);
  min-width: 200px;
}
```

---

## Quick Reference

**Shadow Levels:**
| Level | Size | Use Case |
|-------|------|----------|
| `shadow-sm` | Subtle | Cards, inputs, buttons (rest) |
| `shadow-md` | Medium | Dropdowns, modals, hovers |
| `shadow-lg` | Large | Overlays, mega menus, drawers |

**Elevation + Z-Index:**
| Z-Index | Shadow | Element Type |
|---------|--------|--------------|
| 1 | `shadow-sm` | Base content |
| 10 | `shadow-md` | Dropdowns, popovers |
| 100 | `shadow-lg` | Modals, overlays |
| 1000 | `shadow-lg` | Toasts, notifications |

**Dark Mode:**
| Mode | Opacity Multiplier |
|------|-------------------|
| Light | 1x (0.05, 0.1) |
| Dark | 5-10x (0.5, 0.7, 0.9) |

---

**💡 Remember:** Shadows indicate elevation. Use them to guide user attention!
