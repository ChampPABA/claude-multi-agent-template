# Color Theory - Complete Professional Guide

> **Purpose:** Universal color system principles for any project
> **Audience:** Designers, developers, design system maintainers

---

## Table of Contents

1. [Color Palette Structure](#color-palette-structure)
2. [The 60-30-10 Rule](#the-60-30-10-rule)
3. [Shade Generation](#shade-generation)
4. [Color Harmony](#color-harmony)
5. [Accessibility](#accessibility)
6. [Implementation Patterns](#implementation-patterns)
7. [Best Practices](#best-practices)

---

## Color Palette Structure

### 1. Primary Color (30% of interface)

**Definition & Psychology:**
- The most prominent brand color (NOT the most-used)
- Creates visual emphasis and brand recognition
- Typically 1-2 colors maximum

**Common Psychology:**
| Color | Conveys |
|-------|---------|
| Blue | Trust, professionalism, calm, authority |
| Green | Growth, health, eco-friendly, success |
| Red | Energy, urgency, passion, excitement |
| Purple | Luxury, creativity, premium, wisdom |
| Orange | Friendly, cheerful, affordable, playful |
| Yellow | Optimism, attention, caution, warmth |

**Usage Guidelines:**
- ✅ Headers, navigation bars
- ✅ Primary action buttons
- ✅ Active navigation states
- ✅ Progress indicators
- ✅ Links in body text
- ❌ Large background areas (use neutrals)
- ❌ Body text (low contrast)

---

### 2. Secondary/Accent Color (10% of interface)

**Definition:**
- Harmonious color derived from color wheel relationships
- Complements primary color (warm vs cool balance)
- Used sparingly for emphasis

**Deriving from Primary:**
| Primary | Suggested Secondary |
|---------|-------------------|
| Blue | Orange, Gold, Coral |
| Green | Red, Pink, Purple |
| Red | Green, Teal, Blue-Green |
| Purple | Yellow, Gold, Lime |

**Usage Guidelines:**
- ✅ Call-to-action buttons (Start, Begin, Continue)
- ✅ Important highlights
- ✅ Premium feature badges
- ✅ Success states
- ✅ Hover states for special actions
- ❌ Overuse (should be rare, 10% rule)

---

### 3. Neutral Colors (60% of interface)

**Definition:**
- Whites, grays, blacks in 8-10 shades
- Foundation for text, backgrounds, borders
- Most screens are primarily composed of these colors

**Standard Gray Scale:**
```css
/* Backgrounds */
gray-50:  rgb(249, 250, 251)  /* Lightest backgrounds, hover states */
gray-100: rgb(243, 244, 246)  /* Page backgrounds */
gray-200: rgb(229, 231, 235)  /* Card backgrounds, subtle borders */
gray-300: rgb(209, 213, 219)  /* Borders, dividers */
gray-400: rgb(156, 163, 175)  /* Disabled states, placeholders */

/* Text */
gray-500: rgb(107, 114, 128)  /* Muted text, secondary labels */
gray-600: rgb(75, 85, 99)     /* Body text (dark mode) */
gray-700: rgb(55, 65, 81)     /* Body text (light mode) */
gray-800: rgb(31, 41, 55)     /* Headings, important text */
gray-900: rgb(17, 24, 39)     /* Primary headings, emphasis */
```

**Usage Map:**
| Shade | Use Case | Example |
|-------|----------|---------|
| 50-100 | Page backgrounds, hover states | `bg-gray-50` |
| 200-300 | Card backgrounds, borders | `bg-gray-200 border-gray-300` |
| 400-500 | Disabled states, placeholders | `text-gray-400` |
| 600-700 | Body text, secondary headings | `text-gray-700` |
| 800-900 | Primary headings, important text | `text-gray-900` |

---

### 4. Semantic Colors (Status communication)

**Definition:**
- Colors with universal meaning for user feedback
- Must be consistent across all interfaces
- Should pass WCAG contrast ratios

**Standard Semantic Palette:**

```css
/* Success (Green) */
--success-50: rgb(240, 253, 244)   /* Backgrounds */
--success-500: rgb(34, 197, 94)    /* Base color */
--success-700: rgb(21, 128, 61)    /* Text on light backgrounds */

/* Warning (Amber) */
--warning-50: rgb(255, 251, 235)   /* Backgrounds */
--warning-500: rgb(245, 158, 11)   /* Base color */
--warning-700: rgb(180, 83, 9)     /* Text */

/* Info (Blue) */
--info-50: rgb(239, 246, 255)      /* Backgrounds */
--info-500: rgb(59, 130, 246)      /* Base color */
--info-700: rgb(29, 78, 216)       /* Text */

/* Error/Destructive (Red) */
--error-50: rgb(254, 242, 242)     /* Backgrounds */
--error-500: rgb(239, 68, 68)      /* Base color */
--error-700: rgb(185, 28, 28)      /* Text */
```

**Usage Rules:**
| Color | Meaning | Use Cases | Don't Use For |
|-------|---------|-----------|---------------|
| Green | Success, Positive | Confirmations, completed states, "saved" | Money (use semantic context), navigation |
| Amber | Warning, Caution | Alerts requiring attention, non-critical warnings | Errors (use red), highlights |
| Blue | Info, Neutral | Informational messages, tips, helper text | Primary actions, links |
| Red | Error, Destructive | Failed states, validation errors, delete confirmations | Emphasis, required fields |

**Critical Rule:**
- Use **true red** for errors UNLESS red is your primary color
- If red is primary, use **orange** (`#F97316`) for errors instead

---

## The 60-30-10 Rule

### Visual Balance Formula

**Rule Definition:**
- **60%** Dominant color (Neutrals - backgrounds, text)
- **30%** Secondary color (Primary brand color - headers, actions)
- **10%** Accent color (Secondary brand + semantic colors)

### Why This Works

**Psychological Basis:**
- **60%**: Creates visual calm and foundation
- **30%**: Establishes brand identity without overwhelming
- **10%**: Draws attention to important elements

**Example Application:**

```
Landing Page:
├─ 60% White background, gray text (Neutrals)
├─ 30% Blue headers, navigation, primary buttons (Primary)
└─ 10% Orange CTAs, gold badges, green success (Accent)

Dashboard:
├─ 60% Light gray backgrounds, dark text (Neutrals)
├─ 30% Purple sidebar, active states (Primary)
└─ 10% Yellow highlights, red errors (Accent)
```

### Common Mistakes

**❌ Wrong:**
```css
/* Too much accent color (50% primary, 50% accent) */
background: linear-gradient(blue, orange);
```

**✅ Correct:**
```css
/* Proper balance (60% neutral, 30% primary, 10% accent) */
body { background: white; }         /* 60% */
header { background: blue; }        /* 30% */
.cta { background: orange; }        /* 10% */
```

---

## Shade Generation

### 9-Shade Scale (Industry Standard)

**Naming Convention:**
- 50, 100, 200, 300, 400, 500, 600, 700, 800, 900
- 500 = Base color
- Lower numbers = Lighter (toward white)
- Higher numbers = Darker (toward black)

### Generation Methods

**Method 1: HSL Manipulation (Recommended)**

```javascript
// Starting with base color (500)
const base = { h: 220, s: 70%, l: 50% };  // Blue

// Lightness scale
const shades = {
  50:  { ...base, l: 95% },  // Lightest
  100: { ...base, l: 90% },
  200: { ...base, l: 80% },
  300: { ...base, l: 70% },
  400: { ...base, l: 60% },
  500: { ...base, l: 50% },  // Base
  600: { ...base, l: 40% },
  700: { ...base, l: 30% },
  800: { ...base, l: 20% },
  900: { ...base, l: 10% }   // Darkest
};
```

**Method 2: Online Tools**
- **Tailwind Shades Generator**: https://www.tints.dev/
- **Coolors Palette**: https://coolors.co/
- **Adobe Color**: https://color.adobe.com/

**Usage Rules:**
| Shade | Background | Text | Borders |
|-------|------------|------|---------|
| 50-100 | ✅ Light backgrounds | ❌ Too light | ❌ Too faint |
| 200-300 | ✅ Cards, hover states | ❌ Low contrast | ✅ Subtle borders |
| 400-500 | ✅ Buttons, badges | ✅ On white background | ✅ Default borders |
| 600-700 | ⚠️ Dark backgrounds | ✅ Body text | ⚠️ Too heavy |
| 800-900 | ⚠️ Very dark backgrounds | ✅ Headings | ❌ Too dark |

---

## Color Harmony

### 1. Monochromatic (Safest)

**Definition:** Variations of a single hue (different lightness/saturation)

**Example:**
```css
Primary: Blue (H: 220)
├─ Light blue: hsl(220, 70%, 80%)
├─ Base blue: hsl(220, 70%, 50%)
└─ Dark blue: hsl(220, 70%, 20%)
```

**When to Use:**
- Minimalist designs
- Professional/corporate sites
- When starting out (easiest to get right)

**Pros/Cons:**
- ✅ Always harmonious
- ✅ Consistent mood
- ❌ Can be boring
- ❌ Limited visual interest

---

### 2. Complementary (High Contrast)

**Definition:** Opposite colors on color wheel (180° apart)

**Examples:**
- Blue (#0000FF) + Orange (#FFA500)
- Red (#FF0000) + Green (#00FF00)
- Purple (#800080) + Yellow (#FFFF00)

**When to Use:**
- CTAs that need to "pop"
- Attention-grabbing designs
- Sports brands, energetic sites

**Pros/Cons:**
- ✅ High visual impact
- ✅ Clear hierarchy
- ❌ Can be jarring if overused
- ❌ Requires careful balance (60-30-10 rule)

---

### 3. Analogous (Cohesive)

**Definition:** Adjacent colors on color wheel (30° apart)

**Examples:**
- Blue + Blue-Green + Green
- Orange + Red-Orange + Red
- Purple + Blue-Purple + Blue

**When to Use:**
- Nature-inspired designs
- Calm, cohesive aesthetics
- Gradients and subtle transitions

**Pros/Cons:**
- ✅ Naturally harmonious
- ✅ Smooth gradients
- ❌ Low contrast (harder to create hierarchy)
- ❌ Can lack "pop"

---

### 4. Triadic (Vibrant)

**Definition:** 3 colors evenly spaced on color wheel (120° apart)

**Examples:**
- Red + Yellow + Blue (primary colors)
- Orange + Green + Purple (secondary colors)

**When to Use:**
- Playful brands
- Children's products
- Creative portfolios

**Pros/Cons:**
- ✅ Vibrant and balanced
- ✅ Visual variety
- ❌ Hard to execute well
- ❌ Can look chaotic

---

## Accessibility

### WCAG Contrast Ratios

**Minimum Requirements:**

| Text Type | WCAG AA | WCAG AAA |
|-----------|---------|----------|
| Normal text (<18pt) | 4.5:1 | 7:1 |
| Large text (≥18pt or ≥14pt bold) | 3:1 | 4.5:1 |
| UI components (buttons, inputs) | 3:1 | N/A |

### Testing Contrast

**Tools:**
- **WebAIM Contrast Checker**: https://webaim.org/resources/contrastchecker/
- **Contrast Ratio**: https://contrast-ratio.com/
- **Chrome DevTools**: Lighthouse audit

**Example:**
```css
/* ✅ PASS - 7.5:1 contrast */
background: white; /* #FFFFFF */
color: black;      /* #000000 */

/* ✅ PASS - 4.6:1 contrast */
background: blue;  /* #0000FF */
color: white;      /* #FFFFFF */

/* ❌ FAIL - 2.1:1 contrast */
background: gray;  /* #CCCCCC */
color: white;      /* #FFFFFF */
```

### Color Blindness Considerations

**Types:**
- **Protanopia** (Red-blind): 1% of men
- **Deuteranopia** (Green-blind): 1% of men
- **Tritanopia** (Blue-blind): 0.01% of population
- **Achromatopsia** (Total color blind): 0.003%

**Design Solutions:**
- ✅ Use icons + text (not just color)
- ✅ Use patterns/textures
- ✅ Ensure sufficient contrast
- ❌ Don't rely on red/green alone
- ❌ Don't use only color to convey meaning

**Testing Tools:**
- **Color Oracle**: Free color blindness simulator
- **Stark Plugin**: Figma/Sketch plugin
- **Chrome DevTools**: Vision deficiency emulation

---

## Implementation Patterns

### CSS Custom Properties

```css
/* Define in :root */
:root {
  /* Primary */
  --primary-50: rgb(236, 242, 249);
  --primary-500: rgb(15, 42, 74);
  --primary-900: rgb(3, 8, 15);

  /* Semantic tokens */
  --color-background: var(--neutral-50);
  --color-text: var(--neutral-900);
  --color-primary: var(--primary-500);
  --color-success: var(--success-500);
}

/* Use in components */
.button {
  background: var(--color-primary);
  color: white;
}

.alert-success {
  background: var(--success-50);
  color: var(--success-700);
  border: 1px solid var(--success-500);
}
```

### Dark Mode Support

```css
/* Light mode (default) */
:root {
  --color-background: white;
  --color-text: rgb(17, 24, 39);      /* gray-900 */
  --color-primary: rgb(59, 130, 246);  /* blue-500 */
}

/* Dark mode */
.dark {
  --color-background: rgb(17, 24, 39); /* gray-900 */
  --color-text: white;
  --color-primary: rgb(147, 197, 253); /* blue-300 (lighter for dark backgrounds) */
}

/* Inversion Rule: */
/* Light primary becomes light background in dark mode */
/* Dark primary becomes lighter shade for dark backgrounds */
```

---

## Best Practices

### DO:
- ✅ Use 60-30-10 rule for balance
- ✅ Generate full 9-shade scale for each brand color
- ✅ Test contrast ratios (min 4.5:1)
- ✅ Use semantic colors consistently
- ✅ Define colors once (CSS custom properties)
- ✅ Test for color blindness
- ✅ Use color harmony principles

### DON'T:
- ❌ Use too many colors (max 3-4 brand colors)
- ❌ Rely on color alone to convey meaning
- ❌ Use pure black (#000) for text (too harsh)
- ❌ Hardcode color values everywhere
- ❌ Skip accessibility checks
- ❌ Ignore color psychology
- ❌ Use color without purpose

---

## Quick Reference

**Color Palette Checklist:**
- [ ] Primary color (30%) - Brand identity
- [ ] Secondary/accent (10%) - Emphasis
- [ ] Neutrals (60%) - Backgrounds, text
- [ ] Semantic colors - Success, warning, info, error
- [ ] 9-shade scale for each brand color
- [ ] WCAG AA contrast (4.5:1 min)
- [ ] Color blindness tested
- [ ] Dark mode support (if needed)

**Color Harmony Quick Guide:**
- **Safe**: Monochromatic (1 hue, multiple shades)
- **Balanced**: Complementary (opposite colors, 60-30-10)
- **Cohesive**: Analogous (adjacent colors, smooth)
- **Vibrant**: Triadic (3 evenly spaced, playful)

---

**💡 Remember:** Color is communication. Choose intentionally, apply consistently!
