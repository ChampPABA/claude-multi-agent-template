# Typography System

> **Purpose:** Consistent type hierarchy, readability, and typographic rhythm

---

## Type Scale (5-Level Hierarchy)

**Core Principle:** Use a modular scale for harmonious font sizes

### Standard Type Scale

| Level | Token | Size (rem) | Pixels | Use Case |
|-------|-------|------------|--------|----------|
| **H1** | `text-4xl` | 2.5rem | 40px | Hero titles, landing page headers |
| **H2** | `text-3xl` | 2rem | 32px | Page titles, section headers |
| **H3** | `text-2xl` | 1.5rem | 24px | Subsection titles, card headers |
| **Body** | `text-base` | 1rem | 16px | Paragraphs, content, buttons |
| **Small** | `text-sm` | 0.875rem | 14px | Labels, captions, metadata |

### Extended Scale (for flexibility)

```css
:root {
  /* Tiny */
  --text-xs: 0.75rem;    /* 12px - Fine print, badges */

  /* Small */
  --text-sm: 0.875rem;   /* 14px - Labels, captions */

  /* Base */
  --text-base: 1rem;     /* 16px - Body text */

  /* Medium */
  --text-lg: 1.125rem;   /* 18px - Emphasized body text */

  /* Large */
  --text-xl: 1.25rem;    /* 20px - Small headings */
  --text-2xl: 1.5rem;    /* 24px - H3 */
  --text-3xl: 2rem;      /* 32px - H2 */
  --text-4xl: 2.5rem;    /* 40px - H1 */

  /* Extra Large */
  --text-5xl: 3rem;      /* 48px - Hero (desktop) */
  --text-6xl: 3.75rem;   /* 60px - Display (marketing) */
}
```

---

## Font Weights

**Standard Weights:**

| Weight | Value | Use Case |
|--------|-------|----------|
| **Light** | 300 | Rarely used (decorative only) |
| **Regular** | 400 | Body text, paragraphs |
| **Medium** | 500 | Emphasized text, labels |
| **Semibold** | 600 | Buttons, important labels |
| **Bold** | 700 | Headings (H1-H3), strong emphasis |
| **Extrabold** | 800 | Hero titles (rare) |

**Implementation:**
```css
:root {
  --font-weight-light: 300;
  --font-weight-regular: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;
  --font-weight-extrabold: 800;
}
```

**Usage Guidelines:**
- ✅ Body text: Regular (400)
- ✅ Headings: Bold (700)
- ✅ Buttons: Semibold (600) or Medium (500)
- ✅ Labels: Medium (500)
- ❌ Avoid Light (300) for body text (low readability)
- ❌ Avoid Extrabold (800) except for hero titles

---

## Line Height (Leading)

**Rule:** Tighter for headings, looser for body text

### Standard Line Heights

| Element Type | Line Height | Ratio | Use Case |
|--------------|-------------|-------|----------|
| **Headings** | 1.2 | Tight | Visual impact, hierarchy |
| **Headings** | 1.3 | Medium | Balance (alternative) |
| **Body Text** | 1.5 | Comfortable | Readability, long-form |
| **Body Text** | 1.6 | Loose | Extra comfort (rare) |
| **Small Text** | 1.4 | Compact | Labels, captions |
| **Code** | 1.7 | Extra space | Technical content |

**Implementation:**
```css
:root {
  --leading-tight: 1.2;      /* Headings */
  --leading-snug: 1.3;       /* Headings (alternative) */
  --leading-normal: 1.5;     /* Body text */
  --leading-relaxed: 1.6;    /* Body text (loose) */
  --leading-loose: 1.7;      /* Code blocks */
}

h1, h2, h3 {
  line-height: var(--leading-tight);
}

p, li {
  line-height: var(--leading-normal);
}

code, pre {
  line-height: var(--leading-loose);
}
```

**Why This Matters:**
- Tight line height (1.2): Headings feel "punchy" and impactful
- Normal line height (1.5): Body text is comfortable to read
- Loose line height (1.7): Code is easier to scan

---

## Letter Spacing (Tracking)

**Rule:** Looser for uppercase, tighter for display text

```css
:root {
  --tracking-tighter: -0.05em;  /* Large headings */
  --tracking-tight: -0.025em;   /* H1-H3 */
  --tracking-normal: 0;         /* Body text */
  --tracking-wide: 0.025em;     /* Uppercase, small text */
  --tracking-wider: 0.05em;     /* ALL CAPS */
  --tracking-widest: 0.1em;     /* Extreme emphasis */
}

h1 {
  letter-spacing: var(--tracking-tighter);  /* -0.05em */
}

.label-uppercase {
  text-transform: uppercase;
  letter-spacing: var(--tracking-wide);     /* 0.025em */
}

.all-caps {
  text-transform: uppercase;
  letter-spacing: var(--tracking-wider);    /* 0.05em */
}
```

**When to Use:**
- ✅ Tighter tracking: Large headings (H1, Hero)
- ✅ Wider tracking: Uppercase text, labels
- ✅ Normal tracking: Body text, paragraphs
- ❌ Avoid tight tracking on small text (hard to read)

---

## Font Families

### System Font Stack (Recommended)

**Advantages:**
- ✅ No web font loading (instant render)
- ✅ Native OS appearance
- ✅ Optimal performance
- ✅ Familiar to users

**Implementation:**
```css
:root {
  /* Sans-serif (default) */
  --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI",
               Roboto, "Helvetica Neue", Arial, sans-serif;

  /* Monospace (code) */
  --font-mono: ui-monospace, "Cascadia Code", "Source Code Pro",
               Menlo, Monaco, "Courier New", monospace;

  /* Serif (optional) */
  --font-serif: ui-serif, Georgia, Cambria, "Times New Roman",
                Times, serif;
}

body {
  font-family: var(--font-sans);
}

code, pre {
  font-family: var(--font-mono);
}
```

### Web Fonts (Optional)

**Popular Choices:**
- **Inter**: Modern, versatile, excellent readability
- **Roboto**: Clean, professional, Google's default
- **Poppins**: Geometric, friendly, modern
- **Open Sans**: Humanist, neutral, widely used
- **Lato**: Semi-rounded, approachable

**Implementation (Google Fonts):**
```html
<!-- In <head> -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
```

```css
:root {
  --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}
```

**⚠️ Performance Considerations:**
- Use `font-display: swap` to avoid FOIT (Flash of Invisible Text)
- Limit to 3-4 weights (e.g., 400, 500, 600, 700)
- Consider variable fonts (fewer requests)

---

## Typographic Hierarchy

### Complete Heading System

```css
h1 {
  font-size: var(--text-4xl);        /* 40px */
  font-weight: var(--font-weight-bold);  /* 700 */
  line-height: var(--leading-tight);    /* 1.2 */
  letter-spacing: var(--tracking-tighter); /* -0.05em */
  margin-bottom: var(--spacing-6);      /* 24px */
}

h2 {
  font-size: var(--text-3xl);        /* 32px */
  font-weight: var(--font-weight-bold);  /* 700 */
  line-height: var(--leading-tight);    /* 1.2 */
  letter-spacing: var(--tracking-tight);   /* -0.025em */
  margin-bottom: var(--spacing-4);      /* 16px */
}

h3 {
  font-size: var(--text-2xl);        /* 24px */
  font-weight: var(--font-weight-semibold); /* 600 */
  line-height: var(--leading-snug);     /* 1.3 */
  margin-bottom: var(--spacing-4);      /* 16px */
}

p {
  font-size: var(--text-base);       /* 16px */
  font-weight: var(--font-weight-regular); /* 400 */
  line-height: var(--leading-normal);   /* 1.5 */
  margin-bottom: var(--spacing-4);      /* 16px */
}

small {
  font-size: var(--text-sm);         /* 14px */
  font-weight: var(--font-weight-regular); /* 400 */
  line-height: var(--leading-normal);   /* 1.5 */
}
```

---

## Responsive Typography

### Mobile-First Scaling

```css
/* Mobile (default) */
h1 {
  font-size: 2rem;  /* 32px */
}

h2 {
  font-size: 1.5rem;  /* 24px */
}

/* Tablet (640px+) */
@media (min-width: 640px) {
  h1 {
    font-size: 2.25rem;  /* 36px */
  }

  h2 {
    font-size: 1.75rem;  /* 28px */
  }
}

/* Desktop (1024px+) */
@media (min-width: 1024px) {
  h1 {
    font-size: 2.5rem;  /* 40px */
  }

  h2 {
    font-size: 2rem;  /* 32px */
  }
}
```

**Scaling Pattern:**
- Mobile: 80% of desktop size
- Tablet: 90% of desktop size
- Desktop: 100% (base size)

---

## Text Color & Contrast

### Standard Text Colors

```css
:root {
  /* Light mode */
  --text-primary: rgb(17, 24, 39);      /* gray-900 - Headings */
  --text-secondary: rgb(55, 65, 81);    /* gray-700 - Body text */
  --text-tertiary: rgb(107, 114, 128);  /* gray-500 - Muted text */
  --text-disabled: rgb(156, 163, 175);  /* gray-400 - Disabled */
}

.dark {
  /* Dark mode */
  --text-primary: rgb(255, 255, 255);   /* White - Headings */
  --text-secondary: rgb(229, 231, 235); /* gray-200 - Body */
  --text-tertiary: rgb(156, 163, 175);  /* gray-400 - Muted */
  --text-disabled: rgb(75, 85, 99);     /* gray-600 - Disabled */
}
```

**WCAG Contrast Requirements:**
| Text Size | WCAG AA | WCAG AAA |
|-----------|---------|----------|
| Normal text (<18pt) | 4.5:1 | 7:1 |
| Large text (≥18pt) | 3:1 | 4.5:1 |

---

## Common Patterns

### Article/Blog Post

```css
.prose {
  max-width: 65ch;  /* Optimal reading width */
  font-size: var(--text-base);
  line-height: var(--leading-relaxed);  /* 1.6 - Extra comfort */
  color: var(--text-secondary);
}

.prose h1 {
  margin-top: var(--spacing-12);
  margin-bottom: var(--spacing-6);
}

.prose h2 {
  margin-top: var(--spacing-8);
  margin-bottom: var(--spacing-4);
}

.prose p {
  margin-bottom: var(--spacing-4);
}

.prose strong {
  font-weight: var(--font-weight-semibold);
  color: var(--text-primary);
}
```

### Button Text

```css
.button {
  font-size: var(--text-base);        /* 16px */
  font-weight: var(--font-weight-semibold);  /* 600 */
  line-height: 1;                     /* Tight for buttons */
  letter-spacing: var(--tracking-normal);
}

.button-sm {
  font-size: var(--text-sm);          /* 14px */
  font-weight: var(--font-weight-medium);     /* 500 */
}
```

### Labels & Form Fields

```css
.label {
  font-size: var(--text-sm);          /* 14px */
  font-weight: var(--font-weight-medium);     /* 500 */
  line-height: var(--leading-normal);  /* 1.5 */
  color: var(--text-primary);
  margin-bottom: var(--spacing-2);     /* 8px */
}

.input {
  font-size: var(--text-base);        /* 16px - iOS zoom prevention */
  font-weight: var(--font-weight-regular);    /* 400 */
  line-height: var(--leading-normal);  /* 1.5 */
}
```

---

## Best Practices

### DO:
- ✅ Use modular scale (1.25x or 1.5x ratio)
- ✅ Limit to 3-4 font sizes for simplicity
- ✅ Use relative units (rem, em) for scalability
- ✅ Test readability on mobile devices
- ✅ Ensure 4.5:1 contrast for body text
- ✅ Use system fonts for performance
- ✅ Match line height to font size (smaller = tighter)

### DON'T:
- ❌ Use more than 2 font families
- ❌ Use pixel units for font sizes
- ❌ Set font-size < 16px on inputs (iOS zoom)
- ❌ Use low-contrast text (fails accessibility)
- ❌ Use light font weights for body text
- ❌ Forget responsive scaling
- ❌ Use excessive letter spacing on body text

---

## Quick Reference

**Type Scale:**
| Element | Size | Weight | Line Height |
|---------|------|--------|-------------|
| H1 | 40px (2.5rem) | Bold (700) | 1.2 |
| H2 | 32px (2rem) | Bold (700) | 1.2 |
| H3 | 24px (1.5rem) | Semibold (600) | 1.3 |
| Body | 16px (1rem) | Regular (400) | 1.5 |
| Small | 14px (0.875rem) | Regular (400) | 1.5 |

**Font Weights:**
- Body text: 400 (Regular)
- Labels: 500 (Medium)
- Buttons: 600 (Semibold)
- Headings: 700 (Bold)

**Line Heights:**
- Headings: 1.2-1.3
- Body text: 1.5-1.6
- Small text: 1.4-1.5

---

**💡 Remember:** Good typography is invisible. It should aid readability, not distract!
