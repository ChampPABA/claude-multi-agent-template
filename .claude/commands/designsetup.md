# /designsetup - Auto-Generate Design System from Live Website

You are an expert UX/UI and systems designer with experience at FANG-level companies.

Your task is to generate a comprehensive `STYLE_GUIDE.md` file using **Chrome DevTools MCP** to extract accurate computed styles from live websites or localhost.

---

## 📖 Usage

**Three modes of operation:**

```bash
# Mode 1: Live Website (Reference Design)
/designsetup https://motherduck.com

# Mode 2: Localhost (Brownfield - Reverse Engineering)
/designsetup localhost:3000
/designsetup http://localhost:5173

# Mode 3: Interactive (Greenfield - AI-Generated)
/designsetup
```

**Detection Logic:**
- If URL starts with `https://` → **Path 1** (Live Website)
- If URL contains `localhost` → **Path 2** (Localhost)
- If NO URL provided → **Path 3** (Interactive Greenfield)

---

## 🎯 Mission

Generate a production-ready style guide at: `design-system/STYLE_GUIDE.md`

**Key Principles:**
1. **Data-Driven**: Every color, font, spacing MUST be extracted from computed styles
2. **Accurate**: Use Chrome DevTools MCP for 98% accuracy (vs 75% HTML parsing)
3. **Concise**: 1500-2000 lines (not 5000+ generic fluff)
4. **Actionable**: [MANDATORY] rules, anti-patterns, component mapping
5. **Comprehensive**: All 17 sections included

---

## 🔍 STEP 0: Detect Mode from URL Parameter

**Parse user input to determine which path to use:**

```javascript
const input = userInput.trim();

if (input.startsWith('https://')) {
  // Path 1: Live Website
  mode = 'live-website';
  url = input;
} else if (input.includes('localhost') || input.startsWith('http://localhost')) {
  // Path 2: Localhost (Brownfield)
  mode = 'localhost';
  url = input.startsWith('http') ? input : `http://${input}`;
} else if (input === '' || input === '/designsetup') {
  // Path 3: Interactive Greenfield
  mode = 'interactive';
  url = null;
} else {
  // Invalid input
  error('Invalid URL format. Use: https://, localhost:PORT, or no URL');
}
```

**Report to user:**
```
🔍 Mode Detected: [mode]
📍 URL: [url or "Interactive mode"]

🚀 Starting design extraction...
```

---

## 📋 PATH 1: Live Website Analysis (Chrome DevTools MCP)

**Use Chrome DevTools MCP to extract accurate computed styles from live website.**

---

### Step 1: Open Website in Chrome

```javascript
// 1. Create new page
mcp__chrome-devtools__new_page({
  url: userProvidedUrl  // e.g., "https://motherduck.com"
})

// 2. Wait for page load (critical!)
// Try to detect main heading or fallback to timeout
try {
  // Take quick snapshot to find main content
  const snapshot = mcp__chrome-devtools__take_snapshot({ verbose: false });
  const mainHeading = detectMainHeading(snapshot); // Find first h1 text

  mcp__chrome-devtools__wait_for({
    text: mainHeading,
    timeout: 15000
  });
} catch {
  // Fallback: just wait 5 seconds
  await sleep(5000);
}

// 3. Take initial snapshot
mcp__chrome-devtools__take_snapshot({
  verbose: true
})
```

**Report:**
```
🎨 Design Extraction Started

🌐 Opening: https://motherduck.com
⏳ Waiting for page load...
✅ Page loaded successfully
📸 Snapshot taken

🔄 Extracting design tokens...
```

---

### Step 2: Extract Design Tokens

**Use `evaluate_script` to extract CSS Variables, Colors, Typography, Spacing, and Effects.**

#### A. CSS Variables
- Loop through `document.documentElement` computed styles
- Find all properties starting with `--`
- Return object with variable names and values

#### B. Color Palette (RGB → HEX)
- Extract from all elements: `backgroundColor`, `color`, `borderColor`, `boxShadow`
- Filter out transparent/default values
- Convert RGB to HEX using helper function: `rgb(59, 130, 246)` → `#3B82F6`
- Group by usage: backgrounds, texts, borders, accents

#### C. Typography System
- Query text elements: `h1-h6, p, span, a, button`
- Extract: `fontFamily`, `fontSize`, `fontWeight`, `lineHeight`
- Sort font sizes numerically
- Return unique values only

#### D. Spacing System
- Extract from all elements: `padding`, `margin`, `gap`
- Split compound values: `"16px 24px"` → `["16px", "24px"]`
- Filter out `0px` values
- Sort numerically
- Detect grid pattern (multiples of 4 or 8)

#### E. Visual Effects
- Extract: `boxShadow`, `transition`, `borderRadius`, `animation`
- Filter out default values (`none`, `all 0s ease 0s`)
- Return unique values only

**Report Progress:**
```
✅ Design Tokens Extracted!

📊 Summary:
   - CSS Variables: 24 found
   - Colors: 8 unique colors
     • Backgrounds: 3 colors
     • Text: 2 colors
     • Borders: 2 colors
     • Accents: 1 color
   - Typography: 2 font families, 4 weights, 6 sizes
   - Spacing: 12 unique values (8px grid detected)
   - Effects: 4 shadows, 8 transitions, 3 border radii
```

---

### Step 3: Extract Component Styles

**Use `evaluate_script` with `querySelector` to extract styles from common components:**

**Component Selectors:**
- **Buttons:** `button[class*="primary"]`, `.btn-primary`, `[class*="Button--primary"]`
- **Cards:** `[class*="card"]`, `.card`, `[class*="Card"]`
- **Typography:** `h1`, `h2`, `h3`, `p`
- **Inputs:** `input[type="text"]`, `input[type="email"]`
- **Navigation:** `nav`, `nav a`

**Extract Properties:**
- Layout: `display`, `gap`, `padding`, `margin`
- Colors: `backgroundColor`, `color`, `border`
- Typography: `fontSize`, `fontWeight`, `fontFamily`, `lineHeight`
- Effects: `borderRadius`, `boxShadow`, `transition`

**Report:**
```
✅ Component Styles Extracted!

📦 Components Found:
   - Buttons: Primary, Secondary
   - Cards: Base card style
   - Typography: h1, h2, h3, p
   - Inputs: Text input
   - Navigation: Nav bar, Links
```

---

### Step 4: Test Interactive States & Responsive

**Test hover/focus states and responsive breakpoints:**

#### A. Interactive States
1. **Button Hover:** Use `hover({ uid })` + wait 300ms + extract styles
   - Properties: `backgroundColor`, `color`, `transform`, `boxShadow`
2. **Input Focus:** Use `click({ uid })` + wait 200ms + extract styles
   - Properties: `outline`, `borderColor`, `boxShadow`

#### B. Responsive Breakpoints
1. **Mobile (375px):** Resize + wait 500ms + extract nav/h1/container styles
2. **Tablet (768px):** Resize + wait 500ms + extract same
3. **Desktop (1440px):** Resize + wait 500ms + extract same

**Report:**
```
✅ Interactive & Responsive Testing Complete!

🎭 Interactive States:
   - Button Hover: backgroundColor changes, transform scale(1.05)
   - Input Focus: borderColor blue, boxShadow glow

📱 Responsive Breakpoints:
   - Mobile (375px): Nav hidden, h1 24px, padding 16px
   - Tablet (768px): Nav visible, h1 32px, padding 24px
   - Desktop (1440px): Nav expanded, h1 48px, padding 40px
```

---

### Step 5: Screenshots & Final Report

**Take screenshots using `take_screenshot`:**
- Full page: `{ fullPage: true, format: "png" }`
- Hero section: Find uid from snapshot + `{ uid: heroUid }`
- Primary button: `{ uid: buttonUid }`

**Final Report:**
```
✅ Extraction Complete!

📊 Full Summary:
   - CSS Variables: 24 found
   - Colors: 8 unique (3 bg, 2 text, 2 border, 1 accent)
   - Typography: 2 families, 4 weights, 6 sizes
   - Spacing: 12 values (8px grid)
   - Effects: 4 shadows, 8 transitions, 3 radii
   - Components: 10 styles extracted
   - Interactive: Hover/Focus captured
   - Responsive: 3 breakpoints tested
   - Screenshots: 3 images saved

🔄 Proceeding to pondering phase...
```

---

### Step 6: Pondering Phase

**Wrap analysis in `<pondering>` tags:**

```xml
<pondering>
# Design Analysis (Chrome DevTools Extraction)

## Extraction Results

### CSS Variables
- [List all --var-name: value pairs found]
- Primary color variable: --color-primary
- Spacing scale: --spacing-[size]

### Color Palette (EXTRACTED from computed styles)
- Background Colors:
  - Primary: #FFFFFF (white)
  - Secondary: #F9FAFB (light gray)
  - Accent: #3B82F6 (blue)

- Text Colors:
  - Primary: #111827 (dark)
  - Secondary: #6B7280 (gray)

- Border Colors:
  - Default: #E5E7EB (light gray)
  - Focus: #3B82F6 (blue)

### Typography (EXTRACTED)
- Font Families:
  - Primary: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif
  - Monospace: "Fira Code", Consolas, Monaco, monospace (if found)

- Font Weights:
  - Regular: 400 (most common)
  - Medium: 500
  - Semibold: 600
  - Bold: 700

- Font Sizes (6-level scale detected):
  - xs: 12px
  - sm: 14px
  - base: 16px
  - lg: 18px
  - xl: 20px
  - 2xl: 24px
  - 3xl: 30px
  - 4xl: 36px

### Spacing System (EXTRACTED)
- Grid: 8px base detected (values divisible by 8)
- Common values: 8px, 16px, 24px, 32px, 40px, 48px, 64px
- Likely using: 0.5rem, 1rem, 1.5rem, 2rem, 2.5rem, 3rem, 4rem

### Visual Effects (EXTRACTED)
- Shadows (4 levels detected):
  - sm: 0 1px 2px rgba(0,0,0,0.05)
  - md: 0 4px 6px rgba(0,0,0,0.07)
  - lg: 0 10px 15px rgba(0,0,0,0.1)
  - xl: 0 20px 25px rgba(0,0,0,0.15)

- Border Radius (3 sizes):
  - sm: 4px
  - md: 8px
  - lg: 12px

- Transitions:
  - Duration: 200ms, 300ms (most common)
  - Timing: ease, ease-in-out

### Component Styles (EXTRACTED)
- Button (Primary):
  - Background: #3B82F6
  - Color: #FFFFFF
  - Padding: 12px 24px
  - Border Radius: 8px
  - Hover: Background darken to #2563EB

- Card:
  - Background: #FFFFFF
  - Border: 1px solid #E5E7EB
  - Border Radius: 12px
  - Padding: 24px
  - Shadow: 0 1px 3px rgba(0,0,0,0.1)

### Architecture Detection
- Tailwind CSS: [Check for utility class patterns in class names]
- styled-components: [Check for sc-* pattern]
- CSS Modules: [Check for _[hash] pattern]
- Vanilla CSS: [Check for semantic class names]

### Responsive Behavior
- Mobile (375px): Compact layout, smaller text, reduced padding
- Tablet (768px): Medium layout, standard text, comfortable padding
- Desktop (1440px): Spacious layout, larger text, generous padding

## Design Philosophy (INFERRED)

**Core Principles:**
- Clean, modern, professional aesthetic
- 8px spacing grid for consistency
- Limited color palette (8 colors max)
- Subtle shadows and transitions
- Accessibility-focused (high contrast ratios)

**Visual Identity:**
- [Describe overall design style: Minimalist, Modern, Neo-Brutalism, etc.]
- [Describe mood: Professional, Playful, Technical, Friendly, etc.]
- [Key visual patterns: Rounded corners, Bold borders, Soft shadows, etc.]

## Technical Stack

**Detected Framework:**
- [Tailwind CSS / styled-components / CSS Modules / Vanilla CSS]
- Class pattern: [Describe pattern found]
- Component structure: [Describe organization]

**Not Using:**
- [List frameworks NOT detected]

## Accessibility

**Contrast Ratios:**
- Text on background: [Calculate ratio] (WCAG [AA/AAA])
- Links: [Calculate ratio]
- Buttons: [Calculate ratio]

**Focus States:**
- Visible outline detected: [Yes/No]
- Focus ring color: [Color]

## Key Patterns Summary

1. **Colors**: 8-color palette (minimal, focused)
2. **Typography**: 2 families, 4 weights, 8 sizes
3. **Spacing**: 8px grid (0.5rem to 4rem)
4. **Effects**: 4 shadow levels, 3 border radii
5. **Components**: 10+ component styles extracted
6. **Interactive**: Smooth transitions (200-300ms)
7. **Responsive**: 3 breakpoints (mobile, tablet, desktop)
</pondering>
```

---

## 📋 PATH 2: Localhost Analysis (Brownfield)

**Use Chrome DevTools MCP on localhost + scan codebase for inconsistencies.**

---

### Step 1: Validate Localhost URL

```javascript
const url = userProvidedUrl; // e.g., "localhost:3000" or "http://localhost:5173"
const normalizedUrl = url.startsWith('http') ? url : `http://${url}`;

// Try to connect
try {
  const response = await fetch(normalizedUrl);
  if (!response.ok) {
    throw new Error('Server not responding');
  }
} catch (error) {
  // Server not running
  reportError(`
❌ Cannot connect to ${normalizedUrl}

Please start your dev server first:
  • npm run dev
  • npm start
  • yarn dev

Then run /designsetup again.
  `);
  return;
}
```

**Report:**
```
✅ Localhost server detected!

🌐 URL: http://localhost:3000
🔌 Status: Running
🚀 Starting extraction...
```

---

### Step 2: Extract from Localhost

**Use same extraction as Path 1 (Steps 1-6):**
1. Open page with `mcp__chrome-devtools__new_page`
2. Extract CSS Variables, Colors, Typography, Spacing, Effects
3. Extract Component Styles
4. Test Interactive States & Responsive
5. Take Screenshots
6. Pondering Phase

---

### Step 3: Scan Codebase (Additional Analysis)

**Detect architecture and find component files:**

```bash
# 1. Detect architecture
Grep pattern: 'className=' in src/

# Patterns to detect:
# - Tailwind: className="flex p-4 bg-blue-500"
# - styled-components: className="sc-abc123-0 xyz"
# - CSS Modules: className={styles.button}

# 2. Find all component files
Glob: src/**/*.{tsx,jsx,vue,svelte}

# 3. Map components
# Create mapping: ComponentName → File Path → Extracted Styles
```

**Report:**
```
📊 Codebase Analysis

🏗️ Architecture Detected: Tailwind CSS
   - Utility classes found in 95% of components
   - tailwind.config.js found
   - postcss.config.js found

📁 Components Found: 24 files
   • src/components/Button.tsx
   • src/components/Card.tsx
   • src/components/Input.tsx
   • [... 21 more ...]

🔍 Component Mapping:
   Button.tsx → .btn-primary (extracted styles: bg-blue-500, px-4, py-2)
   Card.tsx → .card (extracted styles: bg-white, rounded-lg, shadow-md)
   [... mapping for all components ...]
```

---

### Step 4: Detect Inconsistencies

**Compare codebase with extracted styles:**

```javascript
// Find inconsistencies:
// 1. Hardcoded colors vs theme colors
// 2. Duplicate component styles
// 3. Unused colors in config
// 4. Inconsistent spacing (not following 8px grid)

const inconsistencies = {
  duplicateStyles: [],
  unusedColors: [],
  hardcodedValues: [],
  namingInconsistencies: []
};

// Example detection logic:
// - Find all bg-blue-* classes, count variants
// - Compare with tailwind.config.js colors
// - Flag if > 3 blue variants used
```

**Report:**
```
⚠️ Inconsistencies Detected:

1. **Duplicate Button Styles (4 variants)**
   • src/components/Button.tsx: bg-blue-500
   • src/components/PrimaryButton.tsx: bg-blue-600
   • src/pages/Home.tsx (inline): bg-primary
   • src/pages/About.tsx (inline): bg-[#3b82f6]

   💡 Recommendation: Consolidate into single Button component

2. **Unused Colors in Config (3 colors)**
   • colors.yellow.500: Defined but never used
   • colors.pink.400: Defined but never used
   • colors.purple.700: Defined but never used

   💡 Recommendation: Remove from tailwind.config.js

3. **Hardcoded Values (8 instances)**
   • margin-left: 17px (not on 8px grid)
   • padding: 13px (not on 8px grid)

   💡 Recommendation: Use spacing scale (p-3, p-4)

4. **Naming Inconsistencies (2 patterns)**
   • Some components: PascalCase (Button.tsx)
   • Other components: kebab-case (nav-bar.tsx)

   💡 Recommendation: Standardize to PascalCase
```

---

### Step 5: Generate Style Guide with Cleanup Notes

**Include all extracted data + inconsistencies + refactoring suggestions:**

```markdown
## ⚠️ Current State Analysis (Brownfield)

**Project:** [Auto-detected from package.json name]
**Architecture:** Tailwind CSS
**Components:** 24 files analyzed

### Inconsistencies Found

[... Include full inconsistency report from Step 4 ...]

### Refactoring Opportunities

1. **Component Consolidation**
   - Merge 4 button variants → single Button component with variants prop
   - Merge 3 card variants → single Card component
   - Estimated time saved: 30 minutes

2. **Color Cleanup**
   - Remove 3 unused colors from config
   - Replace hardcoded blues with theme color
   - Estimated bundle size reduction: 2KB

3. **Spacing Standardization**
   - Replace 8 hardcoded values with spacing scale
   - Use Tailwind spacing utilities (p-4, m-6)
   - Improves consistency across app

4. **Naming Standardization**
   - Rename 12 files to PascalCase
   - Update imports (can be automated)
   - Improves code clarity
```

---

## 📋 PATH 3: Interactive Greenfield

**🚨 ALLOWS USER QUESTIONS for greenfield projects! 🚨**

**When no URL is provided, enter interactive mode to gather requirements.**

---

### Step 1: Ask User Questions

**Use `AskUserQuestion` tool with 4 questions:**

1. **Application Type** (header: "App Type")
   - Options: SaaS Dashboard, Marketing Website, E-commerce Store, Documentation Site, Admin Panel

2. **Design Style** (header: "Design Style")
   - Options: Minimalist, Neo-Brutalism, Modern Professional, Glassmorphism

3. **Primary Color** (header: "Primary Color")
   - Options: Blue (#3B82F6), Green (#10B981), Purple (#8B5CF6), Orange (#F59E0B)

4. **CSS Stack** (header: "CSS Stack")
   - Options: Tailwind CSS, styled-components, CSS Modules, Vanilla CSS

---

### Step 2: Process User Answers

```javascript
const answers = {
  appType: "SaaS Dashboard",
  designStyle: "Modern Professional",
  primaryColor: "Blue",
  cssStack: "Tailwind CSS"
};

// Map to design tokens
const designConfig = {
  colors: {
    primary: answers.primaryColor === "Blue" ? "#3B82F6" :
             answers.primaryColor === "Green" ? "#10B981" :
             answers.primaryColor === "Purple" ? "#8B5CF6" : "#F59E0B"
  },
  style: answers.designStyle,
  appType: answers.appType,
  framework: answers.cssStack
};
```

**Report:**
```
✅ Requirements Gathered!

📋 Configuration:
   - Application Type: SaaS Dashboard
   - Design Style: Modern Professional
   - Primary Color: Blue (#3B82F6)
   - CSS Stack: Tailwind CSS

🎨 Generating AI-based style guide...
```

---

### Step 3: Generate AI-Based Style Guide

**Use modern best practices based on user answers:**

**Generation Rules:**

1. **Color Palette:** Primary + 5 shades, Gray scale (10 levels), Semantic colors (success/warning/error)
2. **Typography Scale:** Base size varies by app type (SaaS: 14px, Marketing: 16px, E-commerce: 15px)
3. **Spacing System:** 8px grid (4px to 64px), maps to 0.25rem to 4rem
4. **Component Styles:** Vary by design style (Minimalist, Neo-Brutalism, Modern Professional, Glassmorphism)
5. **Code Examples:** Tailored to CSS stack (Tailwind, styled-components, CSS Modules, Vanilla)

---

### Step 4: Output Complete Style Guide

**Report:**
```
✅ Style Guide Generated (Greenfield)!

📁 design-system/STYLE_GUIDE.md (1,650 lines)

📊 Generated Configuration:
   - Application: SaaS Dashboard
   - Style: Modern Professional
   - Primary Color: Blue (#3B82F6)
   - Stack: Tailwind CSS

🎨 Included Features:
   - 8-color palette (primary + shades)
   - Gray scale (10 levels)
   - Semantic colors (success, warning, error)
   - Type scale (6 levels, 14px base)
   - 8px spacing grid (9 levels)
   - 12 component styles (Button, Card, Input, Badge, etc.)
   - 4 shadow levels
   - 3 border radius sizes (4px, 8px, 12px)
   - Responsive breakpoints (sm: 640px, md: 768px, lg: 1024px)
   - Dark mode support (CSS variables)
   - Accessibility guidelines (WCAG AAA)
   - 15 code examples (Tailwind syntax)

🚀 Ready for greenfield development!

💡 Next Steps:
   1. Review guide: design-system/STYLE_GUIDE.md
   2. Run /psetup (if needed)
   3. Start building: /csetup feature-name
```

---

## 📝 Generate STYLE_GUIDE.md

**Generate a concise (1500-2000 lines), data-verified style guide.**

**Key Requirements:**
1. **[EXTRACTED]** markers for all computed style data
2. **Source indicators** (CSS variables, computed styles, etc.)
3. **Actual component selectors** (button.primary, not generic)
4. **Anti-patterns section** with [MANDATORY] rules
5. **Architecture-specific** (auto-detected framework)

**Example Structure:**

```markdown
# [Project Name] Design System - Style Guide

> **Source:** Generated from [live website / localhost / AI]
> **Date:** [Current date]
> **Architecture:** [Tailwind CSS / styled-components / CSS Modules / Vanilla CSS]
> **Design Style:** [Minimalist / Neo-Brutalism / Modern Professional / Glassmorphism]

---

## Quick Reference

### Design Tokens (EXTRACTED from computed styles)

```json
{
  "colors": {
    "primary": "#3B82F6",
    "primaryDark": "#2563EB",
    "textPrimary": "#111827",
    "textSecondary": "#6B7280",
    "background": "#FFFFFF",
    "backgroundSecondary": "#F9FAFB",
    "border": "#E5E7EB",
    "borderFocus": "#3B82F6"
  },
  "typography": {
    "fontFamily": "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
    "fontSizes": {
      "xs": "12px",
      "sm": "14px",
      "base": "16px",
      "lg": "18px",
      "xl": "20px",
      "2xl": "24px"
    },
    "fontWeights": {
      "normal": 400,
      "medium": 500,
      "semibold": 600,
      "bold": 700
    }
  },
  "spacing": {
    "1": "4px",
    "2": "8px",
    "3": "12px",
    "4": "16px",
    "6": "24px",
    "8": "32px",
    "10": "40px",
    "12": "48px",
    "16": "64px"
  },
  "effects": {
    "shadows": {
      "sm": "0 1px 2px rgba(0, 0, 0, 0.05)",
      "md": "0 4px 6px rgba(0, 0, 0, 0.07)",
      "lg": "0 10px 15px rgba(0, 0, 0, 0.1)",
      "xl": "0 20px 25px rgba(0, 0, 0, 0.15)"
    },
    "borderRadius": {
      "sm": "4px",
      "md": "8px",
      "lg": "12px"
    },
    "transitions": {
      "fast": "150ms ease",
      "base": "200ms ease",
      "slow": "300ms ease"
    }
  }
}
```

---

## 1. Overview (EXTRACTED Architecture)

**Tech Stack:**
- Framework: React (or detected framework)
- Styling: **[Tailwind CSS / styled-components / CSS Modules]** ✓ EXTRACTED
- Class Pattern: [Detected pattern] ✓ EXTRACTED
- Component Structure: [Detected organization] ✓ EXTRACTED
- Icons: [SVG / Icon library detected] ✓ EXTRACTED

**NOT Using:**
- ❌ [Frameworks NOT detected]

---

## 2. Design Philosophy

**Core Principles:**
- **[Inferred from extraction]**
- **[Based on design style]**
- **[Accessibility focus]**

**Visual Identity:**
- [Describe aesthetic]
- [Describe mood]
- [Key visual patterns]

---

## 3. Color Palette (EXTRACTED from computed styles)

### Primary Colors

**Primary (EXTRACTED from button styles)**
- **Color**: `#3B82F6` (Blue)
- **Usage**: Primary actions, links, focus states
- **Extracted**: getComputedStyle(button).backgroundColor → rgb(59, 130, 246) → #3B82F6
- **Contrast**: 4.5:1 on white (WCAG AA) ✓
- **Context**: Buttons, links, active states

**Primary Dark (EXTRACTED from hover states)**
- **Color**: `#2563EB`
- **Usage**: Hover states, pressed buttons
- **Extracted**: button:hover backgroundColor
- **Context**: Interactive element hover

### Text Colors

**Text Primary (EXTRACTED from body/headings)**
- **Color**: `#111827` (Near Black)
- **Usage**: Main text, headings
- **Extracted**: getComputedStyle(p).color → rgb(17, 24, 39) → #111827
- **Contrast**: 16:1 on white (WCAG AAA) ✓
- **Context**: All body text, headings

**Text Secondary (EXTRACTED from metadata text)**
- **Color**: `#6B7280` (Gray)
- **Usage**: Secondary text, descriptions, metadata
- **Extracted**: getComputedStyle(span.meta).color
- **Contrast**: 7:1 on white (WCAG AAA) ✓

### Background Colors

**Background Primary (EXTRACTED from body)**
- **Color**: `#FFFFFF` (White)
- **Usage**: Page background, card backgrounds
- **Extracted**: getComputedStyle(body).backgroundColor

**Background Secondary (EXTRACTED from sections)**
- **Color**: `#F9FAFB` (Light Gray)
- **Usage**: Alternate sections, subtle backgrounds
- **Extracted**: getComputedStyle(section).backgroundColor

### Color Usage Summary

| Color | Hex | Usage | Contrast |
|-------|-----|-------|----------|
| Primary | #3B82F6 | Actions, links | 4.5:1 (AA) |
| Text Primary | #111827 | Body text | 16:1 (AAA) |
| Text Secondary | #6B7280 | Metadata | 7:1 (AAA) |
| Background | #FFFFFF | Page bg | - |
| Border | #E5E7EB | Dividers | - |

---

## 4. Typography (EXTRACTED)

### Font Families

**Sans-Serif (Primary)**
```css
font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
```
- **Usage**: All UI text (headings, body, buttons)
- **Extracted**: getComputedStyle(body).fontFamily
- **Why**: Modern, readable, system fallbacks

**Monospace (Code)**
```css
font-family: "Fira Code", Consolas, Monaco, "Courier New", monospace;
```
- **Usage**: Code blocks, technical content
- **Extracted**: getComputedStyle(code).fontFamily

### Font Weights (EXTRACTED)

| Weight | Value | Usage |
|--------|-------|-------|
| Normal | 400 | Body text, paragraphs ← PRIMARY |
| Medium | 500 | UI labels, nav links |
| Semibold | 600 | Headings, emphasis |
| Bold | 700 | Strong emphasis, CTAs |

### Font Sizes (EXTRACTED, sorted)

| Size | Value | Usage | Line Height |
|------|-------|-------|-------------|
| xs | 12px | Fine print, captions | 16px (1.33) |
| sm | 14px | Small text, labels | 20px (1.43) |
| base | 16px | Body text ← PRIMARY | 24px (1.5) |
| lg | 18px | Lead paragraphs | 28px (1.56) |
| xl | 20px | Subheadings | 28px (1.4) |
| 2xl | 24px | Section headings | 32px (1.33) |
| 3xl | 30px | Page headings | 36px (1.2) |
| 4xl | 36px | Hero headings | 40px (1.11) |

---

## 5. Spacing System (EXTRACTED)

**Grid: 8px base detected** (all values divisible by 4 or 8)

| Size | Pixels | Rem | Usage |
|------|--------|-----|-------|
| 1 | 4px | 0.25rem | Fine spacing |
| 2 | 8px | 0.5rem | Icon gaps |
| 3 | 12px | 0.75rem | Compact padding |
| 4 | 16px | 1rem | Standard padding ← PRIMARY |
| 6 | 24px | 1.5rem | Comfortable padding |
| 8 | 32px | 2rem | Section spacing |
| 10 | 40px | 2.5rem | Large gaps |
| 12 | 48px | 3rem | Section dividers |
| 16 | 64px | 4rem | Page sections |

---

## 6. Component Styles (EXTRACTED)

### Buttons

**Primary Button (EXTRACTED)**
```css
/* Extracted from: button.primary, .btn-primary */
background-color: #3B82F6;
color: #FFFFFF;
padding: 12px 24px; /* py-3 px-6 */
border-radius: 8px; /* rounded-lg */
font-size: 16px;
font-weight: 500;
transition: background-color 200ms ease;

/* Hover state (EXTRACTED) */
&:hover {
  background-color: #2563EB;
  transform: translateY(-1px);
}

/* Focus state (EXTRACTED) */
&:focus {
  outline: 2px solid #3B82F6;
  outline-offset: 2px;
}
```

**Code Example (Tailwind):**
```tsx
<button className="px-6 py-3 bg-primary text-white rounded-lg font-medium hover:bg-primary-dark transition">
  Click me
</button>
```

**Code Example (styled-components):**
```tsx
const Button = styled.button`
  padding: 12px 24px;
  background-color: var(--color-primary);
  color: white;
  border-radius: 8px;
  font-weight: 500;
  transition: background-color 200ms ease;

  &:hover {
    background-color: var(--color-primary-dark);
  }
`;
```

### Cards

**Card (EXTRACTED)**
```css
/* Extracted from: .card, [class*="Card"] */
background-color: #FFFFFF;
border: 1px solid #E5E7EB;
border-radius: 12px;
padding: 24px;
box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
```

**Code Example (Tailwind):**
```tsx
<div className="bg-white border border-gray-200 rounded-xl p-6 shadow-sm">
  <h3 className="text-lg font-semibold mb-2">Card Title</h3>
  <p className="text-gray-600">Card content...</p>
</div>
```

### Inputs

**Text Input (EXTRACTED)**
```css
/* Extracted from: input[type="text"] */
padding: 12px 16px;
border: 1px solid #E5E7EB;
border-radius: 8px;
font-size: 16px;
transition: border-color 200ms ease;

/* Focus state (EXTRACTED) */
&:focus {
  border-color: #3B82F6;
  outline: none;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}
```

---

## 7. Shadows & Elevation (EXTRACTED)

**Shadow Levels:**

```css
/* sm (EXTRACTED from cards) */
box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);

/* md (EXTRACTED from buttons) */
box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);

/* lg (EXTRACTED from modals) */
box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1);

/* xl (EXTRACTED from popovers) */
box-shadow: 0 20px 25px rgba(0, 0, 0, 0.15);
```

---

## 8. Animations & Transitions (EXTRACTED)

**Transition Durations:**
- Fast: 150ms (small changes, hover states)
- Base: 200ms (standard transitions) ← PRIMARY
- Slow: 300ms (complex animations)

**Timing Functions:**
- ease: Default (most common)
- ease-in-out: Smooth start/end
- ease-out: Smooth end

**Common Patterns:**
```css
/* Button hover */
transition: background-color 200ms ease;

/* Input focus */
transition: border-color 200ms ease, box-shadow 200ms ease;

/* Card hover */
transition: transform 200ms ease, box-shadow 200ms ease;
```

---

## 9. Border Styles (EXTRACTED)

**Border Widths:**
- 1px: Default borders (cards, inputs)
- 2px: Emphasis borders (focused elements)

**Border Colors:**
- Default: #E5E7EB (light gray)
- Focus: #3B82F6 (primary)
- Error: #EF4444 (red)

---

## 10. Border Radius (EXTRACTED)

| Size | Value | Usage |
|------|-------|-------|
| sm | 4px | Small elements, badges |
| md | 8px | Buttons, inputs ← PRIMARY |
| lg | 12px | Cards, modals |
| full | 9999px | Pills, avatars |

---

## 11. Responsive Breakpoints (EXTRACTED)

```css
/* Tailwind default breakpoints (detected) */
sm: 640px   /* Tablet portrait */
md: 768px   /* Tablet landscape */
lg: 1024px  /* Desktop */
xl: 1280px  /* Large desktop */
2xl: 1536px /* Extra large */
```

**Responsive Patterns (EXTRACTED):**
- Mobile (< 640px): Stack vertically, reduced padding
- Tablet (640px - 1024px): 2-column layouts, comfortable spacing
- Desktop (> 1024px): Multi-column layouts, generous spacing

---

## 12. Dark Mode (if detected)

**CSS Variables Pattern:**
```css
:root {
  --color-background: #FFFFFF;
  --color-text: #111827;
}

.dark {
  --color-background: #111827;
  --color-text: #F9FAFB;
}
```

---

## 13. Anti-Patterns & [MANDATORY] Rules

### 🚨 CRITICAL IMPLEMENTATION RULES

**[MANDATORY] Color Usage:**
```
❌ DO NOT hardcode colors (e.g., #3B82F6 inline)
✅ ALWAYS use theme tokens (bg-primary, text-primary)
❌ DO NOT create new colors without design approval
✅ ALWAYS use extracted palette (8 colors max)
```

**[MANDATORY] Spacing:**
```
❌ DO NOT use arbitrary spacing (p-[17px])
✅ ALWAYS use spacing scale (p-4, m-6)
❌ DO NOT break 8px grid (padding: 13px)
✅ ALWAYS use multiples of 4 or 8
```

**[MANDATORY] Typography:**
```
❌ DO NOT use arbitrary font sizes (text-[15px])
✅ ALWAYS use type scale (text-sm, text-base)
❌ DO NOT exceed 4 font weights
✅ ALWAYS use: 400, 500, 600, 700 only
```

**[MANDATORY] Components:**
```
❌ DO NOT create duplicate components
✅ ALWAYS search existing components first
❌ DO NOT hardcode component styles inline
✅ ALWAYS extract to reusable components
```

---

## 14. Accessibility Guidelines

**Contrast Ratios (WCAG AAA):**
- Body text: Minimum 7:1 ratio
- Large text (18px+): Minimum 4.5:1 ratio
- UI components: Minimum 3:1 ratio

**Focus States:**
- Always visible outline (2px solid)
- Offset from element (2px)
- High contrast color (primary)

**Keyboard Navigation:**
- All interactive elements focusable
- Logical tab order
- Focus trap in modals

---

## 15. Code Examples

### Button Component

**Tailwind CSS:**
```tsx
// Primary Button
<button className="px-6 py-3 bg-primary text-white rounded-lg font-medium hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2 transition">
  Click me
</button>

// Secondary Button
<button className="px-6 py-3 bg-white text-primary border border-primary rounded-lg font-medium hover:bg-gray-50 transition">
  Click me
</button>
```

**styled-components:**
```tsx
import styled from 'styled-components';

const Button = styled.button<{ variant?: 'primary' | 'secondary' }>`
  padding: 12px 24px;
  font-weight: 500;
  border-radius: 8px;
  transition: all 200ms ease;

  ${props => props.variant === 'primary' && `
    background-color: var(--color-primary);
    color: white;

    &:hover {
      background-color: var(--color-primary-dark);
    }
  `}

  ${props => props.variant === 'secondary' && `
    background-color: white;
    color: var(--color-primary);
    border: 1px solid var(--color-primary);

    &:hover {
      background-color: var(--color-gray-50);
    }
  `}
`;

export default Button;
```

### Card Component

**Tailwind CSS:**
```tsx
<div className="bg-white border border-gray-200 rounded-xl p-6 shadow-sm hover:shadow-md transition">
  <h3 className="text-lg font-semibold text-gray-900 mb-2">
    Card Title
  </h3>
  <p className="text-gray-600">
    Card description text goes here...
  </p>
</div>
```

**styled-components:**
```tsx
const Card = styled.div`
  background-color: white;
  border: 1px solid var(--color-border);
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: box-shadow 200ms ease;

  &:hover {
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
  }
`;
```

---

## 16. Verification Checklist

Before implementing any component, verify:

- [ ] Colors match extracted palette (no hardcoded colors)
- [ ] Using detected framework ([Tailwind / styled-components / etc.])
- [ ] Spacing follows 8px grid (multiples of 4 or 8)
- [ ] Font sizes use type scale (xs, sm, base, lg, etc.)
- [ ] Font weights: 400, 500, 600, or 700 only
- [ ] Border radius: 4px, 8px, or 12px only
- [ ] Shadows: sm, md, lg, or xl only
- [ ] Transitions: 150ms, 200ms, or 300ms
- [ ] Contrast ratios meet WCAG AAA
- [ ] Focus states visible and accessible

---

## 17. Additional Resources

**Design Tokens (JSON):**
See "Quick Reference" section above for complete JSON export.

**Component Library:**
[If detected: Link to Storybook / component docs]

**Figma/Design Files:**
[If provided by user]

---

## 🎉 End of Style Guide

**Generated by:** Claude Code /designsetup
**Source:** [Live Website / Localhost / AI-Generated]
**Date:** [Current date]
**Method:** Chrome DevTools MCP (computed styles extraction)

---

*This guide is CONCISE (1500-2000 lines) but COMPREHENSIVE because:*
- ✅ Every claim extracted from computed styles (not guessed)
- ✅ Architecture detected from actual code patterns
- ✅ Component examples match detected framework
- ✅ Anti-patterns section prevents mistakes
- ✅ [MANDATORY] rules enforce consistency
- ✅ Accessibility guidelines included
- ✅ Verification checklist provided
```

---

## 🎯 Success Criteria

**Before reporting success, VERIFY:**

1. **Data Quality:**
   - [ ] All colors extracted from computed styles (RGB → HEX)
   - [ ] Architecture detected from class patterns
   - [ ] Component styles match actual selectors
   - [ ] Font weights extracted from getComputedStyle
   - [ ] Shadows/border-radius extracted accurately

2. **Guide Length:**
   - [ ] 1500-2000 lines (concise, not 5000+ fluff)
   - [ ] Focused on extracted data only
   - [ ] No generic filler content

3. **Actionability:**
   - [ ] [MANDATORY] rules included
   - [ ] Anti-patterns section present
   - [ ] Code examples match architecture
   - [ ] Verification checklist provided

4. **Accuracy:**
   - [ ] Chrome DevTools MCP used for extraction
   - [ ] Screenshots taken for reference
   - [ ] No assumptions without extraction
   - [ ] Interactive states tested (hover, focus)
   - [ ] Responsive breakpoints tested

---

## 📢 Final Output

```
✅ Design Setup Complete!

📁 Generated: design-system/STYLE_GUIDE.md (1,850 lines)

📊 Extraction Summary:
   - Colors extracted: 8 unique colors
   - Primary color: #3B82F6 ✓ EXTRACTED
   - Architecture: Tailwind CSS ✓ DETECTED
   - Components: 12 styles extracted
   - Font weights: 4 (400, 500, 600, 700) ✓ EXTRACTED
   - Shadows: 4 levels ✓ EXTRACTED
   - Border radius: 3 sizes (4px, 8px, 12px) ✓ EXTRACTED

🎨 Design Style: Modern Professional

🔍 Extraction Method:
   ✅ Chrome DevTools MCP (computed styles)
   ✅ Screenshots taken (3 images)
   ✅ Interactive states tested (hover, focus)
   ✅ Responsive breakpoints tested (3 sizes)
   ✅ Data-driven (no assumptions)

🎯 Guide Quality:
   ✅ Concise: 1,850 lines (not 5,000+)
   ✅ Accurate: All claims extracted
   ✅ Actionable: [MANDATORY] rules included
   ✅ Architecture-specific: [Framework] examples

💡 Next Steps:
   1. Review guide at design-system/STYLE_GUIDE.md
   2. Run /psetup (if needed)
   3. Start development: /csetup {change-id}
   4. Agents will auto-discover this style guide

🚀 Ready for production!
```

---

**Now execute the detected path based on user input.**
