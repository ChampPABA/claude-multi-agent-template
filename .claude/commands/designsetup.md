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

**Output:** Comprehensive 17-section style guide (1500-2000 lines) based on extracted data.

**Requirements:**
- Mark all computed style data with **[EXTRACTED]**
- Include source indicators (CSS variables, getComputedStyle, etc.)
- Use actual component selectors from extraction
- Include [MANDATORY] rules to prevent anti-patterns
- Match detected CSS architecture

**Structure (17 sections):**

```markdown
# [Project Name] Design System - Style Guide

> **Source:** [Live Website / Localhost / AI-Generated]
> **Date:** [Current date]
> **Architecture:** [Detected CSS framework]
> **Design Style:** [Auto-detected or user-selected style]

---

## Quick Reference
Design Tokens JSON with all extracted values: colors, typography, spacing, effects

## 1. Overview
Tech stack, detected architecture, class patterns, icons

## 2. Design Philosophy
Core principles (2-3), visual identity, aesthetic description

## 3. Color Palette (EXTRACTED)
Primary, text, background, border colors with:
- HEX values (RGB → HEX conversion)
- Usage context
- Contrast ratios (WCAG)
- Extraction method noted
- Color usage summary table

## 4. Typography (EXTRACTED)
Font families, weights (400/500/600/700), sizes table (xs-4xl) with line heights

## 5. Spacing System (EXTRACTED)
Grid base (4px or 8px), spacing scale table (1-16 with px/rem), mark primary value

## 6. Component Styles (EXTRACTED)
For each: Button, Card, Input, Badge, etc.
- Extracted CSS with actual selectors
- Hover/focus states
- Code examples (Tailwind + styled-components)

## 7. Shadows & Elevation (EXTRACTED)
4 levels (sm/md/lg/xl) with CSS values, usage context

## 8. Animations & Transitions (EXTRACTED)
Durations (150ms/200ms/300ms), timing functions, common patterns

## 9. Border Styles (EXTRACTED)
Widths (1px/2px), colors (default/focus/error)

## 10. Border Radius (EXTRACTED)
Size table (sm/md/lg/full), usage examples

## 11. Responsive Breakpoints (EXTRACTED)
Breakpoint values, responsive patterns per device

## 12. Dark Mode (if detected)
CSS Variables pattern with example

## 13. Anti-Patterns & [MANDATORY] Rules
Critical rules for:
- Colors: ❌ hardcoded → ✅ theme tokens
- Spacing: ❌ arbitrary → ✅ scale
- Typography: ❌ arbitrary sizes → ✅ type scale
- Components: ❌ duplicates → ✅ reuse

## 14. Accessibility Guidelines
Contrast ratios (WCAG AAA), focus states, keyboard navigation

## 15. Code Examples
Button, Card, Input components (Tailwind + styled-components examples)

## 16. Verification Checklist
10-point checklist before implementing components

## 17. Additional Resources
Design tokens JSON, component library links, Figma files

---

## 🎉 End of Style Guide
Generated by, source, method, date
```

---

## 🎯 Success Criteria

Verify before reporting:

1. **Data Quality:** All values extracted via getComputedStyle (RGB → HEX)
2. **Guide Length:** 1500-2000 lines (concise, data-focused)
3. **Actionability:** [MANDATORY] rules + anti-patterns included
4. **Accuracy:** Chrome DevTools MCP used, interactive states tested

---

## 📢 Final Output

```
✅ Design Setup Complete!

📁 Generated: design-system/STYLE_GUIDE.md ([line count] lines)

📊 Extraction Summary:
   - Colors extracted: [count] unique colors
   - Primary color: [HEX] ✓ EXTRACTED
   - Architecture: [framework] ✓ DETECTED
   - Components: [count] styles extracted
   - Font weights: 4 (400, 500, 600, 700) ✓ EXTRACTED
   - Shadows: 4 levels ✓ EXTRACTED
   - Border radius: 3 sizes ✓ EXTRACTED

🎨 Design Style: [style]

🔍 Extraction Method:
   ✅ Chrome DevTools MCP (computed styles)
   ✅ Screenshots taken ([count] images)
   ✅ Interactive states tested (hover, focus)
   ✅ Responsive breakpoints tested ([count] sizes)
   ✅ Data-driven (no assumptions)

💡 Next Steps:
   1. Review: design-system/STYLE_GUIDE.md
   2. Run /psetup (if needed)
   3. Start development: /csetup {change-id}

🚀 Ready for production!
```

---

**Now execute the detected path based on user input.**
