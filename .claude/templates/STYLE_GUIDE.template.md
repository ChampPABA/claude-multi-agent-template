# {PROJECT_NAME} Design System

> **Reference Source:** {REFERENCE_URL or "Custom Reference"}
> **Generated:** {DATE}
> **Method:** {HTML + Screenshot / HTML only}
> **Extraction Confidence:** {High / Medium}
> **Last Updated:** {DATE}

---

## 📸 Reference Materials

### Source Files
- **HTML Reference:** [`./reference.html`](./reference.html)
- **Screenshot:** [`./reference-screenshot.png`](./reference-screenshot.png) {IF_EXISTS}

### Metadata
- **Captured:** {DATE}
- **Page State:** {e.g., "Landing page", "Dashboard view", "Logged in state"}
- **Viewport:** {e.g., "Desktop 1920x1080"}

{IF_SCREENSHOT_EXISTS}
### Visual Reference
View `reference-screenshot.png` for visual context and aesthetic direction.
{END_IF}

---

## 🎯 Design Philosophy

{IF_SCREENSHOT_ANALYZED}
This design embodies **{AESTHETIC_STYLE}** with an emphasis on **{KEY_CHARACTERISTICS}**.

**Visual Characteristics:**
- {CHARACTERISTIC_1}
- {CHARACTERISTIC_2}
- {CHARACTERISTIC_3}
- {CHARACTERISTIC_4}

**Design Principles:**
1. {PRINCIPLE_1}
2. {PRINCIPLE_2}
3. {PRINCIPLE_3}
4. {PRINCIPLE_4}
{ELSE}
Design philosophy extracted from code patterns and structure. Review and refine based on project goals.
{END_IF}

---

## 🎨 Color Palette

### Extraction Notes
```
Method: {CSS parsing from HTML}
Colors found: {TOTAL_COLORS_COUNT}
Screenshot validation: {✓ Validated / Not available}
```

### Primary Colors

**Brand Primary**
- **Hex:** `{PRIMARY_HEX}`
- **RGB:** `rgb({PRIMARY_RGB})`
- **HSL:** `hsl({PRIMARY_HSL})`
- **Usage:** {USAGE_DESCRIPTION}
- **Frequency:** Found in {COUNT} instances
{IF_SCREENSHOT}
- **Visual Context:** {WHERE_USED_DESCRIPTION}
{END_IF}
- **Contrast Ratio:** {RATIO}:1 on white {WCAG_LEVEL}

**Brand Secondary**
- **Hex:** `{SECONDARY_HEX}`
- **RGB:** `rgb({SECONDARY_RGB})`
- **Usage:** {USAGE_DESCRIPTION}
- **Frequency:** Found in {COUNT} instances

### Neutral Colors

**Background Colors**

**Primary Background**
- **Hex:** `{BG_PRIMARY_HEX}` (e.g., #ffffff)
- **Usage:** Main content areas, cards

**Secondary Background**
- **Hex:** `{BG_SECONDARY_HEX}` (e.g., #f8fafc)
- **Usage:** Subtle differentiation, sidebars, sections

**Tertiary Background**
- **Hex:** `{BG_TERTIARY_HEX}` (e.g., #f1f5f9)
- **Usage:** Hover states, disabled backgrounds

**Text Colors**

**Primary Text**
- **Hex:** `{TEXT_PRIMARY_HEX}` (e.g., #0f172a)
- **Usage:** Headings, important content
- **Contrast Ratio:** {RATIO}:1 on white {WCAG_LEVEL}

**Secondary Text**
- **Hex:** `{TEXT_SECONDARY_HEX}` (e.g., #64748b)
- **Usage:** Descriptions, metadata, captions
- **Contrast Ratio:** {RATIO}:1 on white {WCAG_LEVEL}

**Muted Text**
- **Hex:** `{TEXT_MUTED_HEX}` (e.g., #94a3b8)
- **Usage:** Placeholders, disabled text
- **Contrast Ratio:** {RATIO}:1 on white {WCAG_LEVEL}

**Border Colors**

**Default Border**
- **Hex:** `{BORDER_DEFAULT_HEX}` (e.g., #e2e8f0)
- **Usage:** Standard borders, dividers

**Subtle Border**
- **Hex:** `{BORDER_SUBTLE_HEX}` (e.g., #f1f5f9)
- **Usage:** Very light separation

### Functional Colors

**Success**
- **Hex:** `{SUCCESS_HEX}` (e.g., #10b981)
- **Usage:** Success messages, positive indicators, checkmarks

**Error / Danger**
- **Hex:** `{ERROR_HEX}` (e.g., #ef4444)
- **Usage:** Error messages, destructive actions, validation errors

**Warning**
- **Hex:** `{WARNING_HEX}` (e.g., #f59e0b)
- **Usage:** Warning messages, cautionary states

**Info**
- **Hex:** `{INFO_HEX}` (e.g., #3b82f6)
- **Usage:** Informational messages, tips, highlights

### Color Usage Guidelines

**Do's:**
- ✅ Use primary color for CTAs and important actions
- ✅ Use secondary for supporting elements
- ✅ Maintain consistent functional color meanings
- ✅ Use neutral colors for hierarchy (primary > secondary > muted)

**Don'ts:**
- ❌ Don't use functional colors decoratively (red ≠ brand color)
- ❌ Don't mix color meanings (success should always be green)
- ❌ Don't use colors with insufficient contrast
- ❌ Don't introduce arbitrary colors outside this palette

---

## ✍️ Typography

### Extraction Notes
```
Primary font: {FONT_FAMILY}
Total sizes found: {COUNT}
Weights found: {WEIGHTS}
```

### Font Stack

**Primary Font Family**
```css
font-family: {FONT_FAMILY};
/* Example: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif */
```

**Loading:**
```html
<!-- If using Google Fonts -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family={FONT_NAME}:wght@400;500;600;700&display=swap" rel="stylesheet">
```

**Or with Fontsource (recommended):**
```bash
npm install @fontsource/{font-name}
```

### Type Scale

**Display Large (Hero)**
```css
font-size: {SIZE_1}px;      /* e.g., 48px or 3rem */
font-weight: {WEIGHT};       /* e.g., 700 */
line-height: {LINE_HEIGHT};  /* e.g., 1.1 */
letter-spacing: {TRACKING};  /* e.g., -0.02em */
```
- **Usage:** Hero headings, landing page titles
- **Frequency:** {COUNT} instances

**Heading 1 (H1)**
```css
font-size: {SIZE_2}px;       /* e.g., 32px or 2rem */
font-weight: {WEIGHT};       /* e.g., 700 */
line-height: {LINE_HEIGHT};  /* e.g., 1.2 */
letter-spacing: {TRACKING};  /* e.g., -0.01em */
```
- **Usage:** Page titles, main headings

**Heading 2 (H2)**
```css
font-size: {SIZE_3}px;       /* e.g., 24px or 1.5rem */
font-weight: {WEIGHT};       /* e.g., 600 */
line-height: {LINE_HEIGHT};  /* e.g., 1.3 */
```
- **Usage:** Section headings

**Heading 3 (H3)**
```css
font-size: {SIZE_4}px;       /* e.g., 20px or 1.25rem */
font-weight: {WEIGHT};       /* e.g., 600 */
line-height: {LINE_HEIGHT};  /* e.g., 1.4 */
```
- **Usage:** Subsection headings, card titles

**Body Large**
```css
font-size: {SIZE_5}px;       /* e.g., 16px or 1rem */
font-weight: {WEIGHT};       /* e.g., 400 */
line-height: {LINE_HEIGHT};  /* e.g., 1.6 */
```
- **Usage:** Large paragraphs, important body content

**Body Regular (Base)**
```css
font-size: {SIZE_6}px;       /* e.g., 14px or 0.875rem */
font-weight: {WEIGHT};       /* e.g., 400 */
line-height: {LINE_HEIGHT};  /* e.g., 1.5 */
```
- **Usage:** Default body text, descriptions, most content

**Body Small**
```css
font-size: {SIZE_7}px;       /* e.g., 12px or 0.75rem */
font-weight: {WEIGHT};       /* e.g., 500 */
line-height: {LINE_HEIGHT};  /* e.g., 1.4 */
letter-spacing: {TRACKING};  /* e.g., 0.01em - slightly wider for readability */
```
- **Usage:** Captions, timestamps, metadata, labels

### Font Weight Usage

- **700 (Bold):** Display text, H1 only
- **600 (Semibold):** H2, H3, important UI elements
- **500 (Medium):** Small text, labels, subtle emphasis
- **400 (Regular):** Body text, default weight

### Typography Guidelines

**Letter Spacing:**
- Large text (>20px): Use tight tracking (`-0.01em` to `-0.02em`)
- Small text (<14px): Use wider tracking (`0.01em` to `0.02em`)
- Default: `0` (normal)

**Line Height:**
- Headings: 1.1 - 1.3 (tight, improves visual impact)
- Body text: 1.5 - 1.6 (comfortable reading)
- Small text: 1.4 (balance between compact and readable)

---

## 📏 Spacing System

### Extraction Notes
```
Analysis: {COUNT} spacing values analyzed
Base unit detected: {BASE_UNIT}px
Verification: All values are multiples of {BASE_UNIT}
{IF_SCREENSHOT}
Visual validation: ✓ Grid structure confirmed in screenshot
{END_IF}
```

### Base Unit
- **Base:** `{BASE_UNIT}px` (e.g., 8px or 4px)
- **Rationale:** {RATIONALE - e.g., "Divisible by 2 and 4, scales well across devices"}

### Spacing Scale

| Token | Value | Rem | Usage | Tailwind |
|-------|-------|-----|-------|----------|
| `xs` | {VALUE_1}px | {REM_1}rem | Tight spacing, icon gaps | `space-x-1` or `gap-1` |
| `sm` | {VALUE_2}px | {REM_2}rem | Default element spacing | `space-x-2` or `gap-2` |
| `md` | {VALUE_3}px | {REM_3}rem | Card padding, moderate spacing | `p-4` or `gap-4` |
| `lg` | {VALUE_4}px | {REM_4}rem | Section spacing, large padding | `p-6` or `gap-6` |
| `xl` | {VALUE_5}px | {REM_5}rem | Page margins, major sections | `p-8` or `gap-8` |
| `2xl` | {VALUE_6}px | {REM_6}rem | Large section separation | `p-10` or `gap-10` |
| `3xl` | {VALUE_7}px | {REM_7}rem | Hero spacing, dramatic separation | `p-12` or `gap-12` |

### Application Examples

**Component Internal Spacing:**
```tsx
// Card component
<div className="p-md">           {/* 24px padding */}
  <h3 className="mb-sm">         {/* 16px margin-bottom */}
    Card Title
  </h3>
  <p className="text-sm">
    Description text
  </p>
</div>
```

**Layout Spacing:**
```tsx
// Page layout
<section className="space-y-lg">  {/* 32px vertical gap */}
  <Header />
  <Content />
  <Footer />
</section>
```

**Grid/Flex Gaps:**
```tsx
// Component grid
<div className="grid grid-cols-3 gap-md">  {/* 24px gap */}
  <Card />
  <Card />
  <Card />
</div>
```

### Spacing Guidelines

**Do's:**
- ✅ Use spacing scale values consistently
- ✅ Stack spacing using the scale (don't mix arbitrary values)
- ✅ Use larger spacing for major sections, smaller for related elements
- ✅ Maintain visual rhythm by repeating spacing values

**Don'ts:**
- ❌ Don't use arbitrary spacing (e.g., `p-5` if 5 is not in scale)
- ❌ Don't mix spacing systems (stick to one base unit)
- ❌ Don't use pixel values in code (use Tailwind classes or CSS variables)

---

## 🧩 Component Styles

### Button

{IF_SCREENSHOT}
**Visual Reference:** See `reference-screenshot.png` for button styles in context.
{END_IF}

#### Primary Button
```tsx
<button className="
  px-{PADDING_X} py-{PADDING_Y}     // Padding: {Xpx} horizontal, {Ypx} vertical
  bg-[{PRIMARY_COLOR}]              // Background: {color name}
  text-white                        // Text color
  font-semibold                     // Weight: 600
  text-sm                           // Size: 14px
  rounded-{RADIUS}                  // Border radius: {value}px
  shadow-sm                         // Shadow: subtle elevation
  hover:bg-[{PRIMARY_HOVER}]        // Hover: darker shade
  active:scale-[0.98]               // Active: slight press effect
  transition-all duration-150       // Smooth transitions
  disabled:opacity-50               // Disabled state
  disabled:cursor-not-allowed
">
  Button Text
</button>
```

**Specifications:**
- **Height:** {HEIGHT}px (auto from padding)
- **Min-width:** {MIN_WIDTH}px
- **Border radius:** {RADIUS}px
- **Shadow:** `{SHADOW_VALUE}`
- **Hover shadow:** `{HOVER_SHADOW_VALUE}`
- **Transition:** `all 150ms ease`

#### Secondary Button
```tsx
<button className="
  px-{PADDING_X} py-{PADDING_Y}
  bg-white
  text-{TEXT_COLOR}
  font-medium
  text-sm
  rounded-{RADIUS}
  border border-{BORDER_COLOR}
  hover:bg-{HOVER_BG}
  transition-colors
">
  Cancel
</button>
```

#### Ghost / Tertiary Button
```tsx
<button className="
  px-{PADDING_X} py-{PADDING_Y}
  bg-transparent
  text-{TEXT_COLOR}
  font-medium
  text-sm
  hover:bg-{HOVER_BG}
  transition-colors
">
  Text Button
</button>
```

---

### Card

```tsx
<div className="
  p-{PADDING}                    // Padding: {value}px
  bg-white
  border border-{BORDER_COLOR}
  rounded-{RADIUS}
  shadow-{SHADOW_LEVEL}          // Elevation level
  hover:shadow-{HOVER_SHADOW}    // Hover effect (if interactive)
  transition-shadow
">
  <h3 className="text-lg font-semibold mb-2">
    Card Title
  </h3>
  <p className="text-sm text-{MUTED_COLOR}">
    Card description or content
  </p>
</div>
```

---

### Input Field

```tsx
<input
  type="text"
  className="
    w-full
    px-{PADDING_X} py-{PADDING_Y}
    bg-white
    border border-{BORDER_COLOR}
    rounded-{RADIUS}
    text-sm
    placeholder:text-{PLACEHOLDER_COLOR}
    focus:outline-none
    focus:ring-2
    focus:ring-{FOCUS_COLOR}
    focus:border-transparent
    transition-all
  "
  placeholder="Enter text..."
/>
```

---

## 🎭 Shadows & Elevation

### Extraction Notes
```
Shadow values found: {COUNT}
Usage: {MINIMAL / MODERATE / PROMINENT}
```

### Shadow Scale

**None / Flat**
```css
box-shadow: none;
```
- **Usage:** Flat designs, bordered elements
- **Tailwind:** `shadow-none`

**Elevation 1 (Subtle)**
```css
box-shadow: {SHADOW_1_VALUE};
/* Example: 0 1px 2px rgba(0, 0, 0, 0.05) */
```
- **Usage:** Buttons, small cards, subtle lift
- **Tailwind:** `shadow-sm`
- **Frequency:** {COUNT} instances

**Elevation 2 (Medium)**
```css
box-shadow: {SHADOW_2_VALUE};
/* Example: 0 4px 6px rgba(0, 0, 0, 0.07) */
```
- **Usage:** Cards, dropdowns, popovers
- **Tailwind:** `shadow-md`
- **Frequency:** {COUNT} instances

**Elevation 3 (High)**
```css
box-shadow: {SHADOW_3_VALUE};
/* Example: 0 10px 15px rgba(0, 0, 0, 0.1) */
```
- **Usage:** Modals, dialogs, floating elements
- **Tailwind:** `shadow-lg`
- **Frequency:** {COUNT} instances

**Elevation 4 (Dramatic)**
```css
box-shadow: {SHADOW_4_VALUE};
/* Example: 0 20px 25px rgba(0, 0, 0, 0.15) */
```
- **Usage:** Large modals, hero elements
- **Tailwind:** `shadow-xl`
- **Frequency:** {COUNT} instances

### Elevation Guidelines

{IF_SCREENSHOT}
**Visual Philosophy:** {DESCRIPTION - e.g., "Minimal shadows, prefers flat design with borders"}
{END_IF}

**Do's:**
- ✅ Use elevation to establish hierarchy
- ✅ Higher elevation = more important / closer to user
- ✅ Use consistent shadows across similar components
- ✅ Combine with z-index for proper layering

**Don'ts:**
- ❌ Don't stack multiple shadow levels on one element
- ❌ Don't use shadows AND heavy borders (choose one)
- ❌ Don't use elevation 4 for common UI (reserve for modals)

---

## 🔲 Border Styles

### Border Widths
- **Default:** `{WIDTH}px` (e.g., 1px)
- **Thick:** `{WIDTH_2}px` (e.g., 2px) - for emphasis
- **None:** `0px` - borderless

### Border Colors
- **Default:** `{BORDER_DEFAULT}` - Standard borders, dividers
- **Subtle:** `{BORDER_SUBTLE}` - Very light separation
- **Strong:** `{BORDER_STRONG}` - Emphasized borders
- **Focus:** `{BORDER_FOCUS}` - Active/focus states

### Border Radius

| Token | Value | Usage | Tailwind |
|-------|-------|-------|----------|
| `none` | `0px` | Sharp corners | `rounded-none` |
| `sm` | `{RADIUS_SM}px` | Subtle rounding | `rounded-sm` |
| `md` | `{RADIUS_MD}px` | Default rounding | `rounded-md` |
| `lg` | `{RADIUS_LG}px` | Prominent rounding | `rounded-lg` |
| `xl` | `{RADIUS_XL}px` | Very rounded | `rounded-xl` |
| `full` | `9999px` | Pills, circles | `rounded-full` |

**Most Common:** `{MOST_COMMON_RADIUS}` ({MOST_COMMON_RADIUS_VALUE}px)

---

## ⚡ Animations & Transitions

### Transition Timings

**Fast (Micro-interactions)**
```css
transition: all 150ms ease;
```
- **Usage:** Hover effects, button presses, small UI changes

**Medium (Default)**
```css
transition: all 250ms ease-in-out;
```
- **Usage:** Dropdowns, tooltips, accordion expansion

**Slow (Dramatic Effects)**
```css
transition: all 350ms ease-in-out;
```
- **Usage:** Page transitions, modal appearances, large movements

### Common Transitions

**Colors/Backgrounds:**
```css
transition: background-color 150ms ease, color 150ms ease;
```

**Shadows:**
```css
transition: box-shadow 200ms ease;
```

**Transforms:**
```css
transition: transform 200ms ease;
```

**Opacity:**
```css
transition: opacity 250ms ease-in-out;
```

### Easing Functions
- **`ease`:** Default, smooth acceleration and deceleration
- **`ease-in-out`:** Gradual start and end
- **`ease-out`:** Quick start, slow end (preferred for UI)
- **`ease-in`:** Slow start, quick end (less common)

---

## 📱 Responsive Breakpoints

### Breakpoint Values

```css
/* Mobile first approach */
sm: 640px   /* Small devices (landscape phones) */
md: 768px   /* Tablets */
lg: 1024px  /* Desktops */
xl: 1280px  /* Large desktops */
2xl: 1536px /* Extra large screens */
```

### Container Max-widths

```css
max-width: {CONTAINER_MAX}px;  /* e.g., 1200px or 1280px */
```

### Responsive Patterns

**Spacing:**
```tsx
<div className="p-4 md:p-6 lg:p-8">
  {/* Padding increases with screen size */}
</div>
```

**Typography:**
```tsx
<h1 className="text-2xl md:text-3xl lg:text-4xl">
  {/* Font size scales up */}
</h1>
```

**Layout:**
```tsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  {/* Columns increase with screen size */}
</div>
```

---

## 🎨 CSS Variables / Tailwind Theme

### CSS Custom Properties

If using vanilla CSS or CSS-in-JS:

```css
:root {
  /* Colors */
  --color-primary: {PRIMARY_HEX};
  --color-secondary: {SECONDARY_HEX};
  --color-bg-primary: {BG_PRIMARY_HEX};
  --color-text-primary: {TEXT_PRIMARY_HEX};

  /* Spacing */
  --spacing-xs: {XS_VALUE}px;
  --spacing-sm: {SM_VALUE}px;
  --spacing-md: {MD_VALUE}px;

  /* Border radius */
  --radius-sm: {RADIUS_SM}px;
  --radius-md: {RADIUS_MD}px;

  /* Shadows */
  --shadow-sm: {SHADOW_SM_VALUE};
  --shadow-md: {SHADOW_MD_VALUE};
}
```

### Tailwind Configuration

If using Tailwind CSS, extend the theme:

```js
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: '{PRIMARY_HEX}',
        secondary: '{SECONDARY_HEX}',
        // ... rest of colors
      },
      fontFamily: {
        sans: ['{FONT_NAME}', 'system-ui', 'sans-serif'],
      },
      spacing: {
        // Custom spacing if needed
      },
      borderRadius: {
        // Custom radius if needed
      },
      boxShadow: {
        // Custom shadows if needed
      },
    },
  },
}
```

---

## 🔧 Implementation Guidelines

### For Developers

**When creating new components:**

1. **Colors:** Use exact hex values from Color Palette
2. **Spacing:** Use spacing scale (avoid arbitrary values)
3. **Typography:** Match font sizes, weights from Typography section
4. **Components:** Reference Component Styles for patterns
5. **Shadows:** Use defined elevation levels
6. **Borders:** Use defined radius values

**Priority:**
```
STYLE_GUIDE.md > best-practices/ > generic design contexts
```

This file is the single source of truth for design.

### For Designers

**When designing new screens:**

1. **Refer to screenshot** (if available) for visual direction
2. **Extract exact values** from this guide
3. **Maintain consistency** with existing patterns
4. **Document new patterns** if creating novel components

### Code Examples

**Good:**
```tsx
// Uses STYLE_GUIDE values
<button className="bg-[#6366f1] px-4 py-2 rounded-md shadow-sm">
  Sign In
</button>
```

**Bad:**
```tsx
// Arbitrary values not in STYLE_GUIDE
<button className="bg-[#5555ff] px-5 py-3 rounded-lg shadow-md">
  Sign In
</button>
```

---

## 📋 Component Checklist

Before submitting a new component, verify:

- [ ] **Colors** match palette (no arbitrary colors)
- [ ] **Spacing** uses scale (no arbitrary px values like p-5, p-7)
- [ ] **Typography** matches styles (correct weights, sizes)
- [ ] **Shadows** match elevation levels
- [ ] **Border radius** matches defined values
- [ ] **Responsive** behavior follows patterns
- [ ] **Accessibility** contrast ratios meet WCAG AA
- [ ] **Consistency** with existing components

---

## 🔄 Updating This Guide

### When to Update

- Reference design changes significantly
- New components establish new patterns
- User feedback identifies gaps or errors
- Design system evolves

### How to Update

1. **Re-run extraction:**
   ```bash
   /designsetup @reference/
   ```

2. **Review changes:**
   - Compare new STYLE_GUIDE with old
   - Identify breaking changes
   - Document migration path

3. **Update components:**
   - Refactor existing components if needed
   - Update documentation
   - Notify team

### Version History

- **v1.0.0** ({DATE}): Initial design system from {REFERENCE_NAME}

---

## 🚨 Troubleshooting

### Colors look different than expected

**Cause:** Monitor calibration, screenshot compression, browser rendering

**Solution:**
- Trust HTML hex values (ground truth)
- Check on multiple devices
- Verify in browser DevTools

### Spacing feels off

**Cause:** Base unit incorrect, rounding errors

**Solution:**
- Verify base unit calculation
- Check actual component implementations
- Reference screenshot for visual validation

### Font rendering differs

**Cause:** Font not loaded, browser differences, fallback fonts

**Solution:**
- Ensure font files loaded correctly
- Check font-weight availability
- Test across browsers

### Components look inconsistent

**Cause:** Not following STYLE_GUIDE, using arbitrary values

**Solution:**
- Review component code
- Compare against STYLE_GUIDE values
- Refactor to match specifications

---

## 📚 Resources

### Reference Materials
- **Original site:** {REFERENCE_URL}
- **HTML source:** [`./reference.html`](./reference.html)
- **Screenshot:** [`./reference-screenshot.png`](./reference-screenshot.png)

### Tools
- **Color contrast checker:** https://webaim.org/resources/contrastchecker/
- **Type scale calculator:** https://type-scale.com/
- **Spacing calculator:** https://spacing.land/

### Further Reading
- **Design system principles:** https://www.designsystems.com/
- **Tailwind CSS docs:** https://tailwindcss.com/docs
- **WCAG guidelines:** https://www.w3.org/WAI/WCAG21/quickref/

---

**Last updated:** {DATE}
**Maintained by:** {TEAM/PROJECT_NAME}
**Questions?** Refer to this document first, then consult the design team.
