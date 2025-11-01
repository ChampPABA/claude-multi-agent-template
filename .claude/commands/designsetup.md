# Design System Setup

You are helping the user set up a project-specific design system from a reference website.

---

## CRITICAL: Check Current Project

First, determine which project we're setting up:

Read: `.claude/contexts/domain/index.md`

Extract the current project name from the file.

If no project is configured:
```
❌ No project configured.

Please run `/psetup` first to set up your project structure.
```

Stop execution.

Set: `PROJECT_NAME = {extracted name}`

---

## STEP 1: Locate Reference Materials

### Check for reference folder

Look for reference files in: `reference/` folder

Expected files:
- `*.html` (from SingleFile Extension) - **Required**
- `*.png` or `*.jpg` (screenshot) - **Optional but recommended**

### Case 1: Files exist in reference/

If `.html` files found:

List files found:
```
✅ Found reference materials:
   - {filename}.html
   {- {filename}.png (if screenshot exists)}

Ready to extract design system.
```

Continue to STEP 2.

### Case 2: No files found

If no `.html` files in reference/:

```
❌ No reference files found in reference/ folder.

To set up a design system, you need a reference website.

**How to capture reference:**

1. **Install SingleFile Extension:**
   - Chrome: https://chrome.google.com/webstore/detail/singlefile/
   - Firefox: https://addons.mozilla.org/firefox/addon/single-file/

2. **Capture website:**
   - Navigate to your inspiration website (e.g., linear.app, stripe.com)
   - Right-click → "Save page with SingleFile"
   - Save to: `reference/{sitename}.html`

3. **Capture screenshot (Recommended):**
   - Take full-page screenshot
   - Save to: `reference/{sitename}.png`

   Screenshot improves extraction quality by providing visual context.

4. **Run again:**
   ```
   /designsetup @reference/
   ```

**Alternative:**
If you don't have a reference website, the uxui-frontend agent will use default design foundations from `.claude/contexts/design/`.
```

Stop execution.

---

## STEP 2: Read Reference Files

### Read HTML file

Read the HTML file content.

If file is very large (>50,000 lines):
```
⚠️  Large HTML file detected.

This may take a moment to process. Please wait...
```

### Check for screenshot

Check if screenshot exists with same base name:
- If HTML: `reference/motherduck.html`
- Look for: `reference/motherduck.png` OR `reference/motherduck.jpg`

If screenshot found:
```
✅ Screenshot found: {filename}.png

I'll use both HTML (exact values) and screenshot (visual context) for best accuracy.
```

If screenshot NOT found:
```
⚠️  No screenshot found.

Extraction will be HTML-only. This is still accurate for exact values but lacks visual context.

💡 Tip: Add a screenshot with the same filename for better results:
   - reference/{basename}.png
```

---

## STEP 3: Extract Design System

### Phase 1: Visual Analysis (if screenshot available)

If screenshot exists, view it first:

```
<pondering>
Visual Analysis of {filename}:

Overall Aesthetic:
- Style: [modern/minimal/bold/playful/professional]
- Mood: [clean/energetic/trustworthy/creative]
- Density: [spacious/balanced/compact]

Visual Hierarchy:
- What stands out most: [headings/colors/images/whitespace]
- Primary focus: [content/navigation/CTAs]

Color Impressions:
- Dominant colors: [describe what you see]
- Background: [light/dark/colored]
- Accents: [where bright colors appear]

Spacing Feel:
- Overall: [generous/moderate/tight]
- Whitespace: [lots/balanced/minimal]
- Component padding: [large/medium/small]

Typography Impression:
- Headings: [bold/thin/serif/sans-serif]
- Body text: [readable/small/large]
- Hierarchy: [clear/subtle]

Component Style:
- Buttons: [flat/elevated/outlined/filled]
- Cards: [bordered/shadowed/flat]
- Corners: [sharp/rounded/very rounded]
</pondering>
```

This gives visual context before extracting exact values.

### Phase 2: Extract from HTML

Parse the HTML systematically:

**A) Extract Colors**

Search for all color values in HTML:
- Look for: `color:`, `background:`, `background-color:`, `border-color:`
- Formats: hex (#6366f1), rgb(99,102,241), hsl(239,84%,67%)
- In: inline styles, `<style>` tags, style attributes

Categorize colors by frequency and usage:

```javascript
// Pseudo-logic for color extraction

colors = {
  backgrounds: [],
  texts: [],
  borders: [],
  accents: []
}

// Find all color values
allColors = extractAllColors(html)

// Count frequency
colorFrequency = countFrequency(allColors)

// Sort by frequency
sortedColors = sortByFrequency(colorFrequency)

// Identify primary (most common non-neutral)
primary = findMostCommonNonNeutral(sortedColors)

// Identify neutrals (grays, blacks, whites)
neutrals = findNeutrals(sortedColors)

// Identify functional (reds, greens, yellows)
functional = findFunctional(sortedColors)
```

**B) Extract Typography**

Search for font-related CSS:
- `font-family:` → font stack
- `font-size:` → all sizes used
- `font-weight:` → weights (400, 500, 600, 700)
- `line-height:` → line heights
- `letter-spacing:` → tracking

Identify patterns:
```javascript
// Collect all font sizes
fontSizes = extractAllFontSizes(html)

// Detect scale (e.g., 12, 14, 16, 20, 24, 32, 48)
typeScale = detectScale(fontSizes)

// Find most common font family
primaryFont = mostCommonFont(html)

// Map sizes to usage
sizeUsage = {
  '48px': 'Headings H1',
  '32px': 'Headings H2',
  '16px': 'Body text',
  '14px': 'Small text',
  '12px': 'Captions'
}
```

**C) Extract Spacing**

Search for spacing values:
- `padding:`, `margin:`, `gap:`
- Collect all numeric values

Detect base unit:
```javascript
// Collect all spacing values
spacingValues = extractAllSpacing(html)

// Find greatest common divisor
baseUnit = findGCD(spacingValues)
// e.g., [8, 16, 24, 32] → GCD = 8

// Build scale
scale = spacingValues.map(v => v / baseUnit).sort().unique()
// [1, 2, 3, 4] → [8px, 16px, 24px, 32px]
```

**D) Extract Shadows**

Search for `box-shadow:` values:
```css
box-shadow: 0 1px 3px rgba(0,0,0,0.1);
box-shadow: 0 4px 6px rgba(0,0,0,0.1);
box-shadow: 0 10px 15px rgba(0,0,0,0.1);
```

Group by intensity (light/medium/heavy).

**E) Extract Border Radius**

Search for `border-radius:` values:
```css
border-radius: 6px;
border-radius: 8px;
border-radius: 12px;
```

Identify common values.

**F) Extract Component Patterns**

Search for common components:
- Buttons: Find elements with button classes/tags
- Cards: Find card-like containers
- Inputs: Find form inputs
- Navigation: Find nav elements

Extract their styling patterns.

---

## STEP 4: Cross-Validate (if screenshot available)

If screenshot was analyzed:

Compare visual impressions with extracted values:

```
Cross-Validation:

Colors:
- Extracted primary: #6366f1 (Indigo)
- Visual impression: Blue/purple accent color
- Match: ✓ Consistent

Spacing:
- Extracted base: 8px
- Visual impression: Generous whitespace
- Match: ✓ Consistent (8px allows for spacious layouts)

Typography:
- Extracted font: Inter, sans-serif
- Visual impression: Clean sans-serif
- Match: ✓ Consistent

Shadows:
- Extracted: Subtle (0-4px blur)
- Visual impression: Minimal elevation
- Match: ✓ Consistent

Conflicts: None detected
```

If conflicts found:
```
⚠️  Potential Conflict Detected:

HTML: Primary color #6366f1
Screenshot: Appears more purple (#8b5cf6)

Resolution: Using HTML value #6366f1 (exact)
Note: Screenshot may have color calibration differences
```

---

## STEP 5: Generate STYLE_GUIDE.md

Use the template and fill with extracted values:

Create comprehensive style guide at:
`.claude/contexts/domain/{PROJECT_NAME}/STYLE_GUIDE.md`

Include:
1. Header with metadata
2. Reference materials section
3. Design philosophy (from visual analysis)
4. Color palette (extracted + usage)
5. Typography (extracted scale)
6. Spacing system (base unit + scale)
7. Component styles (extracted patterns)
8. Shadows & elevation
9. Border radius
10. Implementation notes
11. Usage guidelines

---

## STEP 6: Save Reference Materials

Copy reference files to project:

From: `reference/{filename}.html`
To: `.claude/contexts/domain/{PROJECT_NAME}/reference.html`

If screenshot exists:
From: `reference/{filename}.png`
To: `.claude/contexts/domain/{PROJECT_NAME}/reference-screenshot.png`

This preserves the reference within the project structure.

---

## STEP 7: Update Project Registry

Update: `.claude/contexts/domain/{PROJECT_NAME}/README.md`

Add or update the Design System section:

```markdown
## Design System
- **Status:** ✓ Configured
- **Reference:** {extracted from filename or URL if found}
- **Method:** Reference extraction (HTML + Screenshot / HTML only)
- **Last Updated:** {current date}
- **Files:**
  - [STYLE_GUIDE.md](./STYLE_GUIDE.md)
  - [reference.html](./reference.html)
  - [reference-screenshot.png](./reference-screenshot.png) {if exists}
```

---

## STEP 8: Report to User

Provide comprehensive summary:

```
✅ Design System Setup Complete!

📁 **Files Created:**
   .claude/contexts/domain/{PROJECT_NAME}/
   ├── STYLE_GUIDE.md (comprehensive design system)
   ├── reference.html (source HTML)
   └── reference-screenshot.png (visual reference) {if exists}

🎨 **Extracted Design System:**

   **Colors:**
   - Primary: {hex} ({name})
   - Secondary: {hex} ({name})
   - Neutral colors: {count} shades
   - Functional colors: Success, Error, Warning

   **Typography:**
   - Font family: {font-family}
   - Type scale: {count} sizes ({smallest}px - {largest}px)
   - Weights: {weights}

   **Spacing:**
   - Base unit: {base}px
   - Scale: {scale values}
   - System: {base}-based grid

   **Components:**
   - Patterns documented: {count}
   - Buttons, Cards, Inputs, etc.

   **Shadows:**
   - Elevation levels: {count}
   - Style: {subtle/moderate/prominent}

   **Border Radius:**
   - Values: {values}
   - Style: {sharp/rounded/very rounded}

{If screenshot used:}
📸 **Visual Analysis:**
   - Aesthetic: {aesthetic description}
   - Style: {style keywords}
   - Design Philosophy: {philosophy summary}

{If HTML only:}
⚠️  **Note:** Extracted from HTML only. Consider adding a screenshot for visual context.

🔍 **Quality:**
   - Extraction confidence: {High/Medium}
   - Values: Exact (from HTML CSS)
   - Context: {Visual (screenshot) / Technical only (HTML)}

🚀 **Next Steps:**

   1. **Review STYLE_GUIDE.md**
      - Check extracted values match your expectations
      - Refine if needed (you can edit STYLE_GUIDE.md directly)

   2. **Start Building UI:**
      - Run: `/csetup {change-id}` to plan your first feature
      - Run: `/cdev {change-id}` to start implementation
      - uxui-frontend agent will automatically use STYLE_GUIDE.md

   3. **All Future Components:**
      - Will follow this design system automatically
      - Consistent UI guaranteed
      - No more guessing colors/spacing!

💡 **Tips:**
   - STYLE_GUIDE.md is your single source of truth
   - uxui-frontend agent reads this automatically
   - Update STYLE_GUIDE.md if design evolves
   - Re-run /designsetup to refresh from new reference

---

Design system is now ready! Start building with confidence. 🎉
```

---

## Error Handling

### Error: HTML parsing fails

```
❌ Could not parse HTML file.

Possible issues:
- File is corrupted
- Not a valid HTML file
- Extremely large file (>100MB)

Solutions:
1. Re-capture with SingleFile Extension
2. Try a different page from the reference site
3. Check that file saved correctly
```

### Error: No CSS found

```
⚠️  No CSS found in HTML file.

The HTML appears to be a skeleton without styling.

Possible reasons:
- SingleFile didn't capture external CSS
- Styles are loaded via JavaScript
- Page uses inline styles only

Solutions:
1. Re-capture ensuring "Save CSS" is enabled
2. Try capturing after page fully loads
3. Use browser DevTools to check if CSS loaded
```

### Error: Very minimal CSS

```
⚠️  Limited CSS detected.

Only {count} style rules found. This may not be enough for a complete design system.

Options:
1. Continue with extracted values (partial system)
2. Capture a different page with more UI elements
3. Use default design system (fallback to foundations)

Proceed? (y/n)
```

---

## Usage Examples

### Example 1: Reference in folder

```bash
# User has: reference/motherduck.html

/designsetup @reference/

→ Auto-detects motherduck.html
→ Extracts design system
→ Creates STYLE_GUIDE.md
```

### Example 2: With screenshot

```bash
# User has:
# - reference/linear.html
# - reference/linear.png

/designsetup @reference/

→ Detects both files
→ Uses HTML for exact values
→ Uses screenshot for visual context
→ High-quality STYLE_GUIDE.md
```

### Example 3: Multiple references

```bash
# User has:
# - reference/stripe.html
# - reference/linear.html

/designsetup @reference/

→ Lists both files
→ Asks: "Which reference to use? (stripe/linear)"
→ User selects
→ Proceeds with selected
```

---

## Notes

**This command implements Mode 1 (Reference extraction) only.**

**Why lean approach:**
- Covers 95% of use cases
- Simple, predictable
- High quality output
- Easy to maintain

**If no reference available:**
- Skip /designsetup
- uxui-frontend agent will fall back to:
  1. Existing components (brownfield)
  2. Foundation contexts (design/spacing.md, etc.)

**Future enhancements (if needed):**
- Mode 2: Extract from existing code (--from-code)
- Mode 3: Analyze mockups (--from-openspec)
- For now: Keep it lean and simple
