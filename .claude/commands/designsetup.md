# /designsetup - Auto-Generate Design System Style Guide

You are an expert UX/UI and systems designer with experience at FANG-level companies.

Your task is to **automatically detect** the project context and generate a comprehensive `STYLE_GUIDE.md` file using **HTML-first data-driven analysis**.

---

## ⚠️ CRITICAL: HTML-FIRST APPROACH

**🚨 MANDATORY ANALYSIS PRIORITY 🚨**

1. **PRIMARY SOURCE: HTML/Code Analysis** (95% weight)
   - Extract ALL data with occurrence counts
   - Verify colors, fonts, components, architecture
   - Count usage patterns (95+ occurrences = PRIMARY)
   - Detect actual implementation (sc-*, Component_X, etc.)

2. **VALIDATION SOURCE: Images** (5% weight)
   - Confirm colors are used where expected
   - Validate visual hierarchy
   - Check for patterns not visible in code
   - Detect design style/aesthetic

**❌ WRONG:** "I see blue in the image → Primary color is blue"
**✅ RIGHT:** "HTML shows #383838 used 95 times → Primary text color is #383838"

---

## ⚠️ CRITICAL: NO USER QUESTIONS ALLOWED

**🚨 THIS COMMAND IS 100% AUTOMATED - NEVER ASK USER QUESTIONS 🚨**

You MUST NOT ask the user:
- ❌ "What do you like about this design?"
- ❌ "Please describe in 2-5 keywords..."
- ❌ "What type of application are you building?"
- ❌ Any other questions requiring user input

Instead, you MUST:
- ✅ Analyze HTML/code files automatically with data extraction
- ✅ Count occurrences of colors, components, patterns
- ✅ Detect design style from code patterns (not assumptions)
- ✅ Infer application type from project structure
- ✅ Generate style guide based on verified data

**If you ask ANY user questions during this command, you have FAILED.**

---

## 🎯 Mission

Generate a production-ready, **DATA-VERIFIED** style guide at: `design-system/STYLE_GUIDE.md`

**Key Principles:**
1. **Data-Driven**: Every color, font, spacing MUST be verified with occurrence counts
2. **Code-First**: HTML/code is truth, images validate only
3. **Concise**: 1500-2000 lines (not 5000+ generic fluff)
4. **Actionable**: [MANDATORY] rules, anti-patterns, component mapping
5. **Accurate**: Only include what's verified, no assumptions

---

## 🔍 STEP 1: Smart Path Detection

Execute this decision tree **automatically**:

### Path 1: Reference Design (Priority 1)

**Detection:**
```bash
# Search for reference folders
reference/
design-reference/
designs/
refs/

# If found, search for files:
**/*.{html,htm}
**/*.{png,jpg,jpeg,webp,svg}
```

**Trigger:** If ANY reference folder exists with files → Use Path 1

---

### Path 2: Brownfield - Reverse Engineering (Priority 2)

**Detection:**
```bash
# Search for existing components (exclude build dirs)
**/*.{tsx,jsx,vue,svelte}
# Exclude: node_modules/, .next/, dist/, build/

# Count components
```

**Trigger:** If NO reference folder AND component count > 10 → Use Path 2

---

### Path 3: Greenfield - AI-Generated (Priority 3)

**Trigger:** If NO reference folder AND component count < 10 → Use Path 3

---

## 📋 PATH 1: Reference Design Analysis (HTML-FIRST)

**🚨 CRITICAL: THIS PATH USES HTML AS PRIMARY SOURCE 🚨**
**🚨 IMAGES ARE FOR VALIDATION ONLY 🚨**

---

### Step 1: Report Found Files

```
🎨 Design Setup Analysis

✅ Found reference design:
   📁 reference/motherduck.html (4.1 MB)
   🖼️ reference/screenshot.png (1.2 MB)

🔄 Starting HTML-first data extraction...
```

---

### Step 1.5: Deep HTML Analysis (DATA EXTRACTION)

**🚨 THIS IS THE MOST CRITICAL STEP - EXTRACT ALL DATA 🚨**

**Before analyzing images, you MUST extract comprehensive data from HTML:**

#### A. Extract ALL Colors with Occurrence Counts

```bash
# 1. Extract ALL hex colors with counts
grep -oE "#[0-9A-Fa-f]{6}" file.html | sort | uniq -c | sort -rn

# Expected output format:
#   95 #383838  ← PRIMARY! (most used)
#    5 #F4EFEA
#    4 #16AA98
#    2 #FF7169

# 2. Separate SVG fills from CSS backgrounds
grep -oE 'fill="#[0-9A-Fa-f]{6}"' file.html | sort | uniq -c | sort -rn
grep -oE 'background[:-].*#[0-9A-Fa-f]{6}' file.html | sort | uniq -c | sort -rn

# 3. Extract RGB colors and convert to hex
grep -oE "rgb\([0-9]+,\s*[0-9]+,\s*[0-9]+\)" file.html | sort | uniq -c | sort -rn
# Convert rgb(111, 194, 255) → #6FC2FF
```

**Report format:**
```
📊 Color Analysis (VERIFIED from HTML)

Top Colors by Occurrence:
1. #383838 (Dark Gray) - 95+ uses
   - Context: SVG fills, stroke, text color
   - Usage: Primary text, icons, borders
   - Verified: fill="#383838", stroke="#383838"

2. #16AA98 (Teal) - 4 uses
   - Context: SVG decorative shapes
   - Usage: Accent elements
   - Verified: fill="#16AA98"

3. #F4EFEA (Cream) - 5 uses
   - Context: SVG background shapes
   - Usage: Light backgrounds
   - Verified: fill="#F4EFEA"

4. #FF7169 (Red) - 2 uses
   - Context: Alert/error indicators
   - Usage: Error states
   - Verified: fill="#FF7169"

5. #6FC2FF (Blue) - 10+ uses
   - Context: background-color styles
   - Usage: Section backgrounds
   - Verified: background-color:rgb(111,194,255)

⚠️ Color Classification:
- Text/Icons: #383838 (PRIMARY - 95+ uses)
- Backgrounds: #6FC2FF (hero sections)
- Accents: #16AA98, #F4EFEA, #FF7169
```

#### B. Detect Component Architecture

```bash
# 1. Find component structure
grep -oE 'data-component-id="[^"]*"' file.html | sort | uniq

# Expected output:
# Component_1
# Component_2
# ...
# Component_16

# 2. Detect styled-components pattern
grep -oE 'className="sc-[a-z0-9-]+ [a-zA-Z]+"' file.html | head -20

# Expected output:
# className="sc-c5701267-0 eRMixW"
# className="sc-70d2e32a-0 dEvzxj"

# 3. Detect Tailwind vs CSS-in-JS
grep -E "className=\"(flex|grid|p-|m-|text-|bg-)" file.html | wc -l
# If > 50: Likely Tailwind
# If = 0: Likely styled-components or vanilla CSS
```

**Report format:**
```
🏗️ Architecture Analysis (VERIFIED)

✅ Detected: styled-components (CSS-in-JS)
   - Pattern: className="sc-[hash]-[index] [name]"
   - Examples: sc-c5701267-0, sc-70d2e32a-0

✅ Component Naming: Component_X pattern
   - Found: Component_1 through Component_16
   - Hierarchical: Component_X_Y, Component_X_Y_Z

❌ Tailwind CSS: NOT detected (0 utility classes found)
```

#### C. Extract Typography Data

```bash
# 1. Find all font families
grep -oE 'font-family:[^;"\)]*' file.html | sort | uniq -c | sort -rn

# 2. Find font weights
grep -oE 'fontWeight="[0-9]+"' file.html | sort | uniq -c | sort -rn

# Expected output:
#   45 fontWeight="400"
#    5 fontWeight="500"
#    2 fontWeight="600"

# 3. Find font sizes (if explicitly set)
grep -oE 'fontSize="[0-9]+px"' file.html | sort | uniq -c
grep -oE 'font-size:[^;"\)]*' file.html | sort | uniq -c
```

**Report format:**
```
✍️ Typography Analysis (VERIFIED)

Font Family:
- Primary: System fonts (Inter, -apple-system, BlinkMacSystemFont)
  NOT custom web fonts (no @import or <link> found)

Font Weights:
- 400 (Regular): 45 uses ← PRIMARY body text
- 500 (Medium): 5 uses
- 600 (Semibold): 2 uses
⚠️ Only 3 weights used - minimalist approach

Font Sizes: (Inferred from component structure)
- Likely range: 14px - 32px
- No explicit fontSize attributes found
```

#### D. Detect Shadows & Borders

```bash
# 1. Check for box-shadow
grep -i "box-shadow" file.html | wc -l

# 2. Check for Tailwind shadow utilities
grep -oE "shadow-(sm|md|lg|xl|2xl|none)" file.html | sort | uniq -c

# 3. Check for border-radius
grep -oE "border-radius:[^;\"]*" file.html | sort | uniq -c
grep -oE "rounded-[a-z0-9]+" file.html | sort | uniq -c

# 4. Check SVG strokes (alternative to shadows)
grep -oE 'stroke="#[0-9A-Fa-f]{6}"' file.html | sort | uniq -c
grep -oE 'strokeWidth="[0-9.]+"' file.html | sort | uniq -c
```

**Report format:**
```
🎨 Visual Effects Analysis (VERIFIED)

Shadows:
❌ box-shadow: 0 instances found
❌ Tailwind shadows: 0 instances found
✅ Design uses STROKE-BASED elevation instead

SVG Strokes (Alternative to shadows):
- stroke="#383838": 30+ instances
- strokeWidth="1": 15 instances
- strokeWidth="2": 8 instances
⚠️ Design prefers sharp strokes over soft shadows

Border Radius:
❌ No rounded-[x] classes found
❌ No border-radius CSS found
✅ Design uses SHARP CORNERS (0px radius)
```

#### E. Component Pattern Extraction

```bash
# 1. Map component hierarchy
grep -A 5 'data-component-id="Component_' file.html | head -100

# 2. Extract button patterns
grep -B 2 -A 2 "START FREE\|LOG IN\|READ MORE" file.html

# 3. Extract card patterns
grep -B 3 -A 3 "sc-.*Card\|card\|Card" file.html | head -50

# 4. Find navigation patterns
grep -B 5 -A 5 "<nav\|navigation" file.html
```

**Report format:**
```
🧩 Component Mapping (VERIFIED)

Component_1: Eyebrow/Banner
- Purpose: Hero announcement
- Pattern: Text + link with icon
- Found at: Line 450

Component_2: Navigation Bar
- Purpose: Header menu
- Pattern: Hamburger + links
- Found at: Line 520

Component_4: Hero Section
- Purpose: Main hero with video
- Pattern: Video background + decorative SVG shapes
- Colors used: #6FC2FF (background), #383838 (text)
- Found at: Line 680

[... map all 16 components ...]

Interaction Patterns:
- Links: className="sc-2f7a5bd-1 kUDpUT"
- Buttons: Styled as links (no <button> elements)
- CTAs: "START FREE", "LOG IN" (all uppercase)
```

---

### Step 2: Image Validation (CONFIRM FINDINGS)

**Now that HTML data is extracted, use images to VALIDATE:**

**Read the screenshot/image and check:**

1. **Color Validation:**
   - "Is #383838 used for text/icons?" → Confirm visually ✓
   - "Is #6FC2FF used for hero background?" → Confirm visually ✓
   - "Are decorative shapes using #16AA98?" → Confirm visually ✓

2. **Visual Style Detection:**
   - Sharp corners or rounded? → Sharp (confirms CSS analysis) ✓
   - Shadows or strokes? → Strokes (confirms no box-shadow) ✓
   - Minimalist or complex? → Minimalist (3 font weights) ✓

3. **Design Aesthetic Classification:**
   - **Neo-Brutalism?** Check: Bold borders (❌), solid shadows (❌)
   - **Minimalist?** Check: Clean, limited palette (✅), sharp corners (✅)
   - **Modern Professional?** Check: Clean layout (✅), professional colors (✅)
   - **Data-Focused?** Check: Clean typography (✅), no distractions (✅)

**Report format:**
```
✅ Image Validation Complete

Visual Confirmation:
- #383838 for text/icons: ✓ Confirmed
- #6FC2FF for backgrounds: ✓ Confirmed (hero sections)
- Sharp corners (no rounding): ✓ Confirmed
- Stroke-based elevation: ✓ Confirmed (no shadows visible)
- Minimalist design: ✓ Confirmed

🎨 Design Style Detected: Modern Data Platform (Minimalist)

Key Characteristics:
- Aesthetic: Clean, professional, data-focused
- Color Palette: 4 core colors (minimal)
- Typography: System fonts, 3 weights only
- Borders: Sharp corners (0px radius)
- Elevation: Stroke-based (no shadows)
- Components: 16 hierarchical components
```

---

### Step 3: Pondering Phase

Wrap analysis in `<pondering>` tags:

```xml
<pondering>
# Design Analysis (Data-Verified)

## HTML Analysis Results
- Primary Color: #383838 (95+ uses in SVG fills, text)
- Background Colors: #6FC2FF (hero sections), white (default)
- Accent Colors: #16AA98 (teal), #F4EFEA (cream), #FF7169 (red)
- Architecture: styled-components (sc-* pattern)
- Components: Component_1 through Component_16
- Typography: System fonts, weights 400/500 only
- Shadows: NONE (stroke-based design)
- Border Radius: NONE (sharp corners)

## Visual Validation (from image)
- Colors used as expected: ✓
- Sharp corners confirmed: ✓
- No shadows visible: ✓
- Minimalist aesthetic: ✓

## Core Philosophy
- Clarity First: Limited palette, clean hierarchy
- Data-Focused: Professional, no distractions
- Modern Minimalism: Sharp edges, subtle accents
- Stroke-based Definition: Uses borders instead of shadows

## Technical Implementation
- CSS-in-JS: styled-components with auto-generated class names
- Component Hierarchy: Parent → Child → Grandchild (Component_X_Y_Z)
- No Framework CSS: Not Tailwind, not Bootstrap
- Manual Styling: All styles defined in components

## User Experience
- Trust & Professionalism: Clean, consistent
- Efficiency: Fast loading, minimal CSS
- Clarity: High contrast (#383838 on white = 12:1 ratio)
- Accessibility: WCAG AAA compliant contrast

## Key Patterns Identified
Colors (VERIFIED):
- Text: #383838 (95+ uses) ← PRIMARY
- Background: #6FC2FF (10+ uses), white (default)
- Accents: #16AA98 (4), #F4EFEA (5), #FF7169 (2)

Typography (VERIFIED):
- Fonts: System stack (Inter implied, not imported)
- Weights: 400 (primary), 500 (emphasis) only
- Sizes: Inferred 14-32px range

Spacing (INFERRED from structure):
- Likely 8px grid (padding values divisible by 8)
- Generous spacing (64px sections observed)

Components (VERIFIED):
- 16 mapped components (Component_1 to Component_16)
- Hierarchical naming (Component_X_Y_Z for nesting)
- No duplicate patterns
</pondering>
```

---

### Step 4: Generate STYLE_GUIDE.md (DATA-DRIVEN)

**Generate a concise (1500-2000 lines), data-verified style guide.**

**Key Requirements:**
1. **[VERIFIED]** markers for all data-backed claims
2. **Occurrence counts** for colors, patterns
3. **Actual component names** (Component_1, not "Hero")
4. **Anti-patterns section** with [MANDATORY] rules
5. **Architecture-specific** (styled-components, not Tailwind)

**Example Structure:**

```markdown
# MotherDuck-Inspired Design System - Style Guide

> **Source:** Generated from reference design (data-driven HTML analysis)
> **Date:** 2025-11-02
> **Architecture:** styled-components (CSS-in-JS)
> **Design Style:** Modern Data Platform (Minimalist)

---

## Quick Reference

### Design Tokens (VERIFIED with occurrence counts)

```json
{
  "colors": {
    "textPrimary": "#383838",      // 95+ uses (SVG fills, text)
    "accentTeal": "#16AA98",       // 4 uses (decorative)
    "accentCream": "#F4EFEA",      // 5 uses (backgrounds)
    "accentRed": "#FF7169",        // 2 uses (alerts)
    "backgroundHero": "#6FC2FF",   // 10+ uses (hero sections)
    "backgroundDefault": "#FFFFFF"
  },
  "typography": {
    "fontFamily": "system-ui, -apple-system, BlinkMacSystemFont, sans-serif",
    "fontWeights": {
      "regular": 400,    // 45 uses ← PRIMARY
      "medium": 500      // 5 uses
    }
  },
  "effects": {
    "shadows": "NONE",              // 0 box-shadow found
    "borderRadius": "0px",          // Sharp corners (0 rounded-* found)
    "elevation": "stroke-based"     // Uses SVG strokes instead
  }
}
```

---

## 1. Overview (VERIFIED Architecture)

**Tech Stack:**
- Framework: React (implied from JSX)
- Styling: **styled-components** (CSS-in-JS) ✓ VERIFIED
- Class Pattern: `sc-[hash]-[index] [name]` ✓ VERIFIED
- Component Naming: `Component_X`, `Component_X_Y`, `Component_X_Y_Z` ✓ VERIFIED
- Icons: SVG-based (inline, fill="#383838") ✓ VERIFIED

**NOT Using:**
- ❌ Tailwind CSS (0 utility classes found)
- ❌ CSS Modules
- ❌ Sass/SCSS
- ❌ Inline styles (uses className pattern)

---

## 2. Design Philosophy

**Core Principles:**
- **Clarity First**: Limited 4-color palette, high contrast (12:1 ratio)
- **Minimal Complexity**: 3 font weights max, no shadows, sharp corners
- **Data-Focused**: Professional aesthetic, no visual distractions
- **Stroke-Based Definition**: Uses borders/strokes instead of shadows

**Visual Identity:**
- Clean, professional, technical (not playful)
- Sharp corners (no rounding)
- High contrast black text on white
- Subtle accent colors (teal, cream, red)

---

## 3. Color Palette (VERIFIED with occurrence counts)

### Text & Icon Colors

**Primary Text (VERIFIED - 95+ occurrences)**
- **Color**: `#383838` (Dark Gray)
- **Usage**: Main text color, SVG fills, SVG strokes, borders
- **Verified**: `fill="#383838"` (60+ times), `stroke="#383838"` (30+ times)
- **Contrast**: 12:1 ratio on white (WCAG AAA) ✓
- **Context**: Used in Component_1-16, all icon SVGs

**White Text (for dark backgrounds)**
- **Color**: `#FFFFFF`
- **Usage**: Text on #6FC2FF backgrounds
- **Verified**: Visible in hero sections

### Background Colors

**Hero Background (VERIFIED - 10+ occurrences)**
- **Color**: `#6FC2FF` (Bright Cyan Blue)
- **Usage**: Hero section backgrounds, highlighted sections
- **Verified**: `background-color:rgb(111,194,255)` ✓
- **RGB**: rgb(111, 194, 255)
- **Context**: Component_4 (hero), other feature sections

**Default Background**
- **Color**: `#FFFFFF` (White)
- **Usage**: Page background, card backgrounds
- **Verified**: Browser default ✓

### Accent Colors

**Accent Teal (VERIFIED - 4 occurrences)**
- **Color**: `#16AA98`
- **Usage**: Decorative SVG shapes, accent elements
- **Verified**: `fill="#16AA98"` ✓
- **Context**: Component_4 decorative shapes

**Accent Cream (VERIFIED - 5 occurrences)**
- **Color**: `#F4EFEA`
- **Usage**: Light background tints, SVG shapes
- **Verified**: `fill="#F4EFEA"` ✓
- **Context**: Component_4, light sections

**Accent Red (VERIFIED - 2 occurrences)**
- **Color**: `#FF7169`
- **Usage**: Error/alert states
- **Verified**: `fill="#FF7169"` ✓
- **Context**: Component_13 (alert indicators)

### Color Usage Summary

| Color | Hex | Occurrences | Primary Usage |
|-------|-----|-------------|---------------|
| Dark Gray | #383838 | 95+ | Text, icons, strokes ← **PRIMARY** |
| Bright Blue | #6FC2FF | 10+ | Hero backgrounds |
| Teal | #16AA98 | 4 | Decorative accents |
| Cream | #F4EFEA | 5 | Light backgrounds |
| Red | #FF7169 | 2 | Alerts/errors |
| White | #FFFFFF | Default | Page background |

---

## 4. Typography (VERIFIED)

### Font Families

**Sans-Serif (Primary)**
```css
font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
```
- **Usage**: All text (headings, body, UI)
- **Why System Fonts**: No custom font imports detected
- **Verified**: No @import or <link rel="stylesheet"> for web fonts ✓

### Font Weights (VERIFIED with counts)

| Weight | Value | Occurrences | Usage |
|--------|-------|-------------|-------|
| Regular | 400 | 45+ | Body text, paragraphs ← **PRIMARY** |
| Medium | 500-600 | 5-7 | Headings, emphasis |

**⚠️ CRITICAL:** Only 2-3 font weights used (minimalist approach)

### Font Sizes (INFERRED from structure)

Explicit font sizes not found in HTML attributes, likely defined in styled-components theme:

| Size | Estimated | Usage |
|------|-----------|-------|
| Small | 14px | Secondary text, metadata |
| Base | 16px | Body text |
| Large | 18px | Lead paragraphs |
| XL | 24px | Subheadings |
| 2XL | 32px | Section headings |

---

## 5. Component Architecture (VERIFIED)

### Component Mapping

| Component ID | Purpose | Verified Pattern |
|--------------|---------|------------------|
| Component_1 | Eyebrow/Banner | Text + link + icon |
| Component_2 | Navigation Bar | Hamburger menu + links |
| Component_3 | Main Navigation | Nav links + CTA |
| Component_4 | Hero Section | Video + decorative shapes (uses #6FC2FF, #16AA98) |
| Component_5 | Feature Section | Image + text content |
| Component_12 | Testimonials | Quote cards with icons |
| Component_13 | Carousel | Swiper-based carousel (contains #FF7169 alerts) |
| Component_16 | Footer | Links + copyright |

**Total Components:** 16 (Component_1 through Component_16) ✓ VERIFIED

### Class Name Pattern (VERIFIED)

```jsx
// styled-components pattern
<div
  data-component-id="Component_4"
  className="sc-c5701267-0 eRMixW"
>
  {/* content */}
</div>
```

**Pattern:** `sc-[8-char-hash]-[index] [readable-name]`

---

## 6. Visual Effects (VERIFIED)

### Shadows

**Finding:** ❌ **NO SHADOWS** (0 box-shadow detected)

```bash
# Verified with:
grep -i "box-shadow" file.html | wc -l
# Result: 0
```

**Alternative:** Design uses **stroke-based elevation**

### SVG Strokes (Shadow Alternative)

```
stroke="#383838": 30+ instances
strokeWidth="1": 15 instances
strokeWidth="2": 8 instances
```

**Usage:** SVG elements use strokes for definition instead of shadows

### Border Radius

**Finding:** ❌ **NO ROUNDING** (0 border-radius detected)

```bash
# Verified with:
grep -oE "rounded-[a-z]+" file.html | wc -l
# Result: 0
```

**All corners are SHARP (0px radius)** ✓ VERIFIED

---

## 7. Anti-Patterns & [MANDATORY] Rules

### 🚨 CRITICAL IMPLEMENTATION RULES

**[MANDATORY] Color Usage:**
```
❌ DO NOT use #6FC2FF for text (it's a background color)
✅ ALWAYS use #383838 for text, icons, SVG fills
❌ DO NOT create new colors (stick to verified 4-color palette)
✅ ALWAYS verify color usage with occurrence counts
```

**[MANDATORY] Architecture:**
```
❌ DO NOT use Tailwind classes (bg-blue-500, text-gray-700)
✅ ALWAYS use styled-components pattern (sc-*)
❌ DO NOT use inline styles
✅ ALWAYS use className pattern
```

**[MANDATORY] Visual Effects:**
```
❌ DO NOT add box-shadow (design uses strokes)
❌ DO NOT add border-radius (design uses sharp corners)
✅ ALWAYS use stroke="#383838" for SVG outlines
✅ ALWAYS use strokeWidth="1" or "2" only
```

**[MANDATORY] Typography:**
```
❌ DO NOT use fontWeight 700+ (not in design)
✅ ALWAYS use fontWeight 400 or 500-600 only
❌ DO NOT import custom fonts (use system stack)
✅ ALWAYS use system-ui font family
```

**[MANDATORY] Component Naming:**
```
❌ DO NOT create components outside Component_X pattern
✅ ALWAYS follow Component_X, Component_X_Y hierarchy
❌ DO NOT duplicate components
✅ ALWAYS check existing Component_1-16 first
```

---

## 8. Code Examples (styled-components)

### Button Component (styled-components)

```tsx
// ❌ WRONG (Tailwind)
<button className="px-4 py-2 bg-primary text-white rounded-lg">
  Click me
</button>

// ✅ CORRECT (styled-components)
import styled from 'styled-components';

const StyledButton = styled.button`
  padding: 16px 24px;
  background-color: transparent;
  color: #383838;
  border: 1px solid #383838;
  border-radius: 0; /* Sharp corners */
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;

  &:hover {
    background-color: rgba(56, 56, 56, 0.05);
  }
`;

<StyledButton>Click me</StyledButton>
```

### SVG Icon (Verified Pattern)

```tsx
// ✅ CORRECT (matches reference design)
<svg
  fill="none"
  viewBox="0 0 20 20"
  xmlns="http://www.w3.org/2000/svg"
>
  <path
    fill="#383838"     // ← ALWAYS use #383838
    d="M17.5 8.125..."
  />
</svg>
```

---

## 9. Verification Checklist

Before implementing any component, verify:

- [ ] Colors match verified palette (#383838, #6FC2FF, #16AA98, #F4EFEA, #FF7169)
- [ ] Using styled-components (not Tailwind)
- [ ] Component naming follows Component_X pattern
- [ ] NO box-shadow used
- [ ] NO border-radius used (sharp corners only)
- [ ] Font weights: 400 or 500 only
- [ ] SVG fills/strokes use #383838
- [ ] System fonts (no custom font imports)

---

## 🎉 End of Style Guide

**Key Takeaways:**
1. **4-color palette** (minimal, verified)
2. **styled-components architecture** (not Tailwind)
3. **Sharp corners, no shadows** (stroke-based design)
4. **System fonts, 2 weights** (400, 500)
5. **16 components mapped** (Component_1-16)
6. **Data-driven** (every claim verified with counts)

**File Location:** `design-system/STYLE_GUIDE.md`

---

*Generated by Claude Code Multi-Agent System (Data-Driven Analysis)*
*Source: HTML occurrence counting + image validation*
*Last updated: 2025-11-02*
```

**This guide is CONCISE (1500-2000 lines) but POWERFUL because:**
- ✅ Every color verified with occurrence counts
- ✅ Architecture detected from actual code patterns
- ✅ Component names match actual implementation
- ✅ Anti-patterns section prevents mistakes
- ✅ [MANDATORY] rules enforce consistency

---

## 📋 PATH 2: Brownfield - Reverse Engineering

(Same HTML-first approach as Path 1, but analyzing existing codebase instead of reference folder)

**Steps:**
1. Scan codebase for components
2. Extract colors with `grep -oE` + occurrence counts
3. Detect architecture (Tailwind vs styled-components vs CSS modules)
4. Map components with actual file names
5. Generate style guide reflecting CURRENT state with ⚠️ inconsistencies flagged

---

## 📋 PATH 3: Greenfield - AI-Generated

(Same structure, but auto-detect application type from package.json, folder structure)

**Auto-detection logic:**
- Check `package.json` keywords
- Check folder structure (`dashboard/`, `admin/`, `docs/`)
- Default to **SaaS Dashboard** if unclear
- Generate modern best-practice guide

---

## 🎯 Success Criteria

**Before reporting success, VERIFY:**

1. **Data Quality:**
   - [ ] All colors have occurrence counts (e.g., "95+ uses")
   - [ ] Architecture detected from code patterns
   - [ ] Component names match actual implementation
   - [ ] Font weights verified with counts
   - [ ] Shadows/border-radius checked (not assumed)

2. **Guide Length:**
   - [ ] 1500-2000 lines (concise, not 5000+ fluff)
   - [ ] Focused on verified data only
   - [ ] No generic filler content

3. **Actionability:**
   - [ ] [MANDATORY] rules included
   - [ ] Anti-patterns section present
   - [ ] Code examples match architecture
   - [ ] Verification checklist provided

4. **Accuracy:**
   - [ ] HTML analyzed BEFORE images
   - [ ] Images used for validation only
   - [ ] No assumptions without verification
   - [ ] Occurrence counts for all major patterns

---

## 📢 Final Output

```
✅ Design Setup Complete!

📁 Generated: design-system/STYLE_GUIDE.md (1,850 lines)

📊 Data Verification Summary:
   - Colors analyzed: 6 unique colors
   - Primary color: #383838 (95+ uses) ✓ VERIFIED
   - Architecture: styled-components ✓ VERIFIED
   - Components mapped: 16 (Component_1-16) ✓ VERIFIED
   - Font weights: 2 (400, 500) ✓ VERIFIED
   - Shadows: 0 (stroke-based design) ✓ VERIFIED
   - Border radius: 0px (sharp corners) ✓ VERIFIED

🎨 Design Style Detected: Modern Data Platform (Minimalist)

🔍 Analysis Method:
   ✅ HTML-first (95% weight)
   ✅ Image validation (5% weight)
   ✅ Data-driven (occurrence counts)
   ✅ Zero assumptions

🎯 Guide Quality:
   ✅ Concise: 1,850 lines (not 5,000+)
   ✅ Accurate: All claims verified
   ✅ Actionable: [MANDATORY] rules included
   ✅ Architecture-specific: styled-components examples

💡 Next Steps:
   1. Review guide at design-system/STYLE_GUIDE.md
   2. Run /psetup (if needed)
   3. Start development: /csetup {change-id}
   4. Agents will auto-discover this style guide

🚀 Ready for production!
```

---

**Now execute Path 1 with HTML-first analysis.**
