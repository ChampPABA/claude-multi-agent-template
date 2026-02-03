# /extract - Extract Design System from Website

You are an expert design systems engineer with deep knowledge of CSS, animations, and UX patterns.

Your task is to extract comprehensive design data from a website and save it as a complete YAML file with psychology analysis.

---

## 📖 Usage

```bash
/extract <URL>

Arguments:
  URL              Required. Website URL to extract from

Examples:
  /extract https://airbnb.com
  /extract https://linear.app
  /extract https://stripe.com
```

---

## 🎯 Mission

Extract ALL design data from a website and save to `design-system/extracted/{site-name}/`:
- `data.yaml` - Complete 17-section design data + psychology analysis + animations
- `screenshots/` - Component screenshots (default + hover/focus states)

**Key Principles:**
1. **17 Sections Complete**: Colors with usage, typography with sizes, components with animations
2. **Psychology Included**: Target audience, emotions evoked, why it works
3. **Component-Level Detail**: Every component type with all states
4. **Animation Capture**: Before/after for all interactive states

---

## 🔍 STEP 0: Parse Input & Setup

### 0.1: Validate and Normalize URL

1. Check if URL argument is provided
   - If missing, return error: "URL required. Usage: /extract https://airbnb.com"
2. Trim whitespace from URL
3. Add "https://" prefix if URL doesn't start with "http://" or "https://"
4. Parse hostname and auto-detect site name:
   - Remove "www." prefix if present
   - Remove top-level domain (TLD) to get clean site name
   - Example: "www.airbnb.com" → "airbnb"

### 0.2: Check for Existing Extraction

1. Build path: `design-system/extracted/{siteName}/data.yaml`
2. If file exists:
   - Read existing YAML file
   - Extract `meta.extracted_at` field
   - Ask user via AskUserQuestion:
     - Question: "Site '{siteName}' was already extracted on {extractedDate}. Re-extract?"
     - Options: "Yes, re-extract" (overwrite) or "No, cancel" (keep existing)
   - If user chooses "No, cancel", exit with message: "Extraction cancelled. Existing data preserved."

### 0.3: Create Output Directories

Use Bash to create directory structure:
```bash
mkdir -p design-system/extracted/{siteName}/screenshots
```

**Report:**
```
🚀 Extraction Started

📍 URL: ${url}
📁 Site: ${siteName}
📂 Output: design-system/extracted/${siteName}/

⏳ Navigating to site...
```

---

## STEP 1: Navigate & Wait

### 1.1: Navigate to URL

Use agent-browser to navigate to the target URL:
```bash
agent-browser open {url}
```

### 1.2: Smart Wait for Page Load

1. Take DOM snapshot (verbose: false) to analyze page structure
2. From snapshot, find heading elements (filter lines containing `[heading]`)
3. If headings found:
   - Extract text from first heading
   - Use agent-browser wait_for to wait for that text (timeout: 15000ms)
   - This ensures the main content is loaded
4. If no headings found or wait fails:
   - Fallback to sleep 5000ms

### 1.3: Verify Document Ready

1. Evaluate script to check document.readyState
2. If not "complete", sleep additional 3000ms to ensure full page load

**Report:**
```
✅ Page loaded successfully

🔄 Extracting CSS data (17 sections)...
```

---

## STEP 2: Extract CSS Data (17 Sections in Parallel)

Run all extraction evaluations in parallel for speed. Use agent-browser `evaluate_script` for each extraction function below.

**Parallel Execution Strategy:**
- Execute all 8 extraction functions concurrently
- Collect results: colors, typography, shadows, spacing, buttons, cards, inputs, animations
- Non-critical failures should not block other extractions (use fallback empty arrays)

### 2.1: Extract Colors

Use agent-browser to evaluate script that:

1. **Query all elements**: `document.querySelectorAll('*')`
2. **For each element**, extract using `window.getComputedStyle()`:
   - Background color (skip transparent: `rgba(0, 0, 0, 0)`)
   - Text color
   - Border color (skip transparent)
3. **Convert RGB to HEX**: Parse RGB values and convert to uppercase hex format
4. **Detect usage context** based on element tag/class:
   - Background usage: button-bg, nav-bg, card-bg, hero-bg, page-bg, surface
   - Text usage: heading, link, button-text, muted-text, body-text
   - Border usage: input-border, card-border, divider
5. **Count frequency** of each color (how many times used)
6. **Sort by count** (most used first) and take top 20 per category

**Output format:**
```yaml
colors:
  backgrounds:
    - hex: "#FFFFFF"
      rgb: "rgb(255, 255, 255)"
      usage: "page-bg"
      count: 45
  texts:
    - hex: "#000000"
      usage: "body-text"
      count: 32
  borders:
    - hex: "#E5E7EB"
      usage: "divider"
      count: 12
```

### 2.2: Extract Typography

Use agent-browser to evaluate script that:

1. **Extract heading styles** (h1, h2, h3):
   - Query first 3 instances of each heading tag
   - For each, extract using `window.getComputedStyle()`:
     - Sample text (first 50 characters)
     - fontSize, fontWeight, fontFamily
     - lineHeight, letterSpacing, textTransform
     - color
2. **Extract body text styles** (p, div, span):
   - Query first 20 elements with text content > 20 characters
   - Extract: fontSize, fontWeight, lineHeight, fontFamily, color
3. **Collect unique values**:
   - All font families used
   - All font weights (sorted numerically)
   - All font sizes (sorted by value)

**Output format:**
```yaml
typography:
  h1:
    - text: "Welcome to our site"
      fontSize: "48px"
      fontWeight: "700"
      fontFamily: "Inter, sans-serif"
  h2:
    - fontSize: "32px"
      fontWeight: "600"
  body:
    - fontSize: "16px"
      fontWeight: "400"
      lineHeight: "1.5"
  allFonts: ["Inter", "Roboto"]
  allWeights: ["400", "500", "600", "700"]
  allSizes: ["14px", "16px", "24px", "32px", "48px"]
```

### 2.3: Extract Shadows & Effects

Use agent-browser to evaluate script that:

1. **Query all elements**: `document.querySelectorAll('*')`
2. **For each element**, extract using `window.getComputedStyle()`:
   - boxShadow (skip "none")
   - borderRadius (skip "0px")
   - borderWidth (skip "0px")
3. **Collect unique values** using Set to avoid duplicates
4. **Limit results**:
   - Top 15 unique box shadows
   - Top 15 unique border radii
   - Top 10 unique border widths

**Output format:**
```yaml
shadows:
  - "0 1px 3px rgba(0, 0, 0, 0.1)"
  - "0 4px 6px rgba(0, 0, 0, 0.1)"
borderRadii:
  - "4px"
  - "8px"
  - "12px"
borderWidths:
  - "1px"
  - "2px"
```

### 2.4: Extract Spacing

Use agent-browser to evaluate script that:

1. **Query first 100 elements** for spacing analysis
2. **For each element**, extract using `window.getComputedStyle()`:
   - Padding (all sides: top, right, bottom, left, shorthand) - skip "0px"
   - Margin (top, bottom only) - skip "0px" and "auto"
   - Gap (flexbox/grid) - skip "normal" and "0px"
3. **Detect spacing grid pattern**:
   - Parse all spacing values to numbers
   - Calculate Greatest Common Divisor (GCD) to find base unit
   - Common pattern: 4px or 8px base grid
   - Fallback to 8px if pattern unclear
4. **Limit results**:
   - Top 20 unique padding values
   - Top 20 unique margin values
   - Top 10 unique gap values
   - Top 15 most common spacing values overall

**Output format:**
```yaml
spacing:
  detectedGrid: 8
  paddings: ["8px", "16px", "24px", "32px"]
  margins: ["8px", "16px", "24px"]
  gaps: ["8px", "16px"]
  commonValues: [8, 16, 24, 32, 40, 48]
```

### 2.5: Extract Buttons

Use agent-browser to evaluate script that:

1. **Query button elements** with selectors:
   - `button`, `a[role="button"]`
   - `.btn`, `[class*="button"]`, `[class*="Button"]`
2. **Take first 10 buttons** found
3. **For each button**:
   - Add `data-extract-id` attribute (e.g., "button-0", "button-1")
   - Extract using `window.getComputedStyle()`:
     - Text content (first 30 characters)
     - backgroundColor, color, padding
     - border, borderRadius
     - fontSize, fontWeight
     - boxShadow, transition

**Why add data-extract-id**: Enables later re-querying for hover/focus state extraction.

### 2.6: Extract Cards

Use agent-browser to evaluate script that:

1. **Query card-like elements** with selectors:
   - `[class*="card"]`, `[class*="Card"]`
   - `article`, `section`
   - `[class*="box"]`, `[class*="Box"]`
2. **Take first 10 cards** found
3. **For each card**:
   - Add `data-extract-id` attribute (e.g., "card-0", "card-1")
   - Extract className for reference
   - Extract using `window.getComputedStyle()`:
     - backgroundColor, padding
     - border, borderRadius
     - boxShadow, transition

### 2.7: Extract Input Fields

Use agent-browser to evaluate script that:

1. **Query input elements** with selectors:
   - `input[type="text"]`, `input[type="email"]`, `input[type="password"]`
   - `textarea`
2. **Take first 5 inputs** found
3. **For each input**:
   - Add `data-extract-id` attribute (e.g., "input-0", "input-1")
   - Extract type (text/email/password/textarea)
   - Extract using `window.getComputedStyle()`:
     - height, padding
     - border, borderRadius
     - fontSize, backgroundColor
     - transition

### 2.8: Extract Animations

Use agent-browser to evaluate script that:

1. **Extract CSS @keyframes animations**:
   - Loop through all document.styleSheets
   - For each stylesheet, check cssRules
   - Find rules with type `CSSRule.KEYFRAMES_RULE`
   - Extract: animation name and full CSS text
   - Handle CORS errors gracefully (skip external stylesheets)

2. **Extract CSS transitions**:
   - Query first 50 elements
   - For each, extract using `window.getComputedStyle()`:
     - transition property
     - transitionDuration
     - transitionTimingFunction
   - Skip default value: "all 0s ease 0s"
   - Record element className or tagName for reference

**Output format:**
```yaml
animations:
  keyframes:
    - name: "fadeIn"
      css: "@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }"
  transitions:
    - selector: "button"
      transition: "all 0.3s ease"
      transitionDuration: "0.3s"
      transitionTimingFunction: "ease"
```

**Report:**
```
✅ CSS Data Extracted!

📊 Summary:
   - Colors: ${colors.backgrounds.length} backgrounds, ${colors.texts.length} texts
   - Typography: ${typography.allFonts.length} fonts, ${typography.allWeights.length} weights
   - Shadows: ${shadows.shadows.length} unique values
   - Spacing: ${spacing.detectedGrid}px grid detected
   - Buttons: ${buttons.length} extracted
   - Cards: ${cards.length} extracted
   - Inputs: ${inputs.length} extracted
   - Animations: ${animations.keyframes.length} @keyframes

🔄 Extracting component animations (hover/focus states)...
```

---

## STEP 3: Extract Component Animations (Interactive States)

For each component type, capture default and hover states to understand animations.

### 3.1: Button Hover States

For the **first 3 buttons** (to limit execution time):

1. **Find element by data-extract-id** (e.g., "button-0")
2. **Scroll element into view** (block: center) for visibility
3. **Wait 500ms** for scroll animation
4. **Take screenshot** of default state
   - Save to: `design-system/extracted/{siteName}/screenshots/{btnId}-default.png`
5. **Capture default computed styles**:
   - backgroundColor, color, boxShadow, transform
6. **Trigger hover state**:
   - Dispatch `MouseEvent('mouseenter', { bubbles: true })` to element
7. **Wait 500ms** for transition to complete
8. **Take screenshot** of hover state
   - Save to: `design-system/extracted/{siteName}/screenshots/{btnId}-hover.png`
9. **Capture hover computed styles**:
   - backgroundColor, color, boxShadow, transform
10. **Remove hover state**:
    - Dispatch `MouseEvent('mouseleave')` to element
11. **Compare states** and generate description:
    - If boxShadow changed → "Shadow changes"
    - If transform changed → "Transform changes"
    - If background changed → "Background changes"
    - Join changes with " + " or return "No visible changes"

### 3.2: Card Hover States

Repeat same process for **first 3 cards** with `data-extract-id="card-{i}"`.

### 3.3: Input Focus States

Similar process for **first 3 inputs** but use:
- Focus event instead of hover: `dispatchEvent(new FocusEvent('focus'))`
- Blur event to remove: `dispatchEvent(new FocusEvent('blur'))`
- Screenshot names: `{inputId}-default.png`, `{inputId}-focus.png`

**Store results** in componentAnimations object with structure:
```yaml
componentAnimations:
  button-0:
    type: "button"
    description: "Shadow changes + Background changes"
    transition: "all 0.3s ease"
    states:
      default:
        background: "rgb(59, 130, 246)"
        boxShadow: "none"
      hover:
        background: "rgb(37, 99, 235)"
        boxShadow: "0 4px 6px rgba(0, 0, 0, 0.1)"
```

---

## STEP 4: Full-Page Screenshot

### 4.1: Ensure Screenshot Directory Exists

```bash
mkdir -p design-system/extracted/{siteName}/screenshots
```

### 4.2: Capture Full-Page Screenshot

Use agent-browser to take screenshot:

1. **First attempt**: Full-page screenshot
   ```bash
   agent-browser screenshot --full design-system/extracted/{siteName}/screenshots/full-page.png
   ```

2. **If full-page fails**: Fallback to viewport-only
   - Parameters: `fullPage: false`, `format: 'png'`
   - Save to: `design-system/extracted/{siteName}/screenshots/viewport.png`

**Why fallback**: Some sites have infinite scroll or very long pages that cause full-page screenshots to fail.

---

## STEP 5: AI Psychology Analysis

### 5.1: Determine Screenshot Path

Check which screenshot exists:
- Prefer: `design-system/extracted/{siteName}/screenshots/full-page.png`
- Fallback: `design-system/extracted/{siteName}/screenshots/viewport.png`

### 5.2: Read Screenshot

Use Read tool to load the screenshot image for visual analysis.

### 5.3: Generate Psychology Analysis Prompt

Create analysis request with:

**Context provided:**
- The screenshot (visual attachment)
- Extracted CSS colors data (JSON formatted)
- Extracted typography fonts (JSON formatted)

**Request UX/UI psychology insights in YAML format covering:**

1. **style_classification**: Design style (Neo-Brutalism, Minimalist, Glassmorphism, Modern SaaS, etc.)

2. **emotions_evoked**: List of emotions with reasons
   - emotion: What feeling the design triggers
   - reason: Specific design elements causing this emotion

3. **target_audience**: Who this design appeals to
   - primary: Main user demographic (description, age_range, tech_savvy)
   - secondary: Secondary users (if applicable)

4. **visual_principles**: Key design patterns observed
   - name: Principle name
   - description: How it's applied

5. **why_it_works**: Strategic design decisions
   - List of business/psychological reasons the design is effective

6. **design_philosophy**: Underlying beliefs
   - core_belief: Central design philosophy
   - key_principles: List of guiding principles

**Instruction**: Be specific with examples from the visual.

### 5.4: Extract YAML Response

Parse the LLM response to extract the YAML block (between triple backticks).

---

## STEP 6: Generate data.yaml (17 Sections + Psychology)

### 6.1: Calculate Coverage Metrics

Count how many of the 17 standard sections were successfully detected:
- Overview, Color Palette, Typography, Spacing System, Component Styles
- Shadows/Elevation, Animations/Transitions, Border Radius, Border Styles
- Layout Patterns, etc.

Calculate percentage: `(detectedSections / 17) * 100`

### 6.2: Build YAML Structure

Construct comprehensive YAML file with these sections:

**Header Comments:**
```yaml
# Design Extraction: {siteName}
# Extracted: {ISO timestamp}
# URL: {url}
```

**Meta Section:**
```yaml
meta:
  site_name: {siteName}
  url: {url}
  extracted_at: {ISO timestamp}
  extractor_version: "2.1.0"
  coverage:
    total_sections: 17
    detected_sections: {count}
    percentage: {percentage}
```

**Psychology Section:**
Insert the psychology YAML from Step 5.4

**Design Tokens Sections:**
```yaml
sections:
  overview:
    detected: true
    style: {from psychology.style_classification}
    tech_stack: Framework-agnostic

  color_palette:
    detected: true
    primary:
      - hex: {top 5 background colors}
        rgb: {rgb value}
        usage: {usage context}
    text_colors:
      - hex: {top 5 text colors}
        usage: {usage context}
    border_colors:
      - hex: {top 3 border colors}
        usage: {usage context}

  typography:
    detected: true
    fonts: [{top 3 font families}]
    weights: [{all weights, sorted}]
    sizes: [{all sizes, sorted}]

  spacing_system:
    detected: true
    grid_base: {detectedGrid}
    common_values: [{spacing values}]

  component_styles:
    detected: true
    buttons:
      - id: {button-0}
        text: {button text}
        backgroundColor: {color}
        color: {text color}
        padding: {padding}
        borderRadius: {radius}
        transition: {transition}
        hover_animation: {description from Step 3}
    cards:
      - {similar structure}
    inputs:
      - {similar structure}

  shadows_elevation:
    detected: true
    values: [{top 5 shadow values}]

  animations_transitions:
    detected: true
    keyframes:
      - name: {animation name}
    transitions:
      - duration: {duration}
        timing: {timing function}

  border_radius:
    detected: true
    values: [{top 8 radius values}]

  border_styles:
    detected: true
    widths: [{border widths}]

  layout_patterns:
    detected: true
    container_width: "1280px"
    grid_columns: 12
```

**Component Animations (Detailed):**
```yaml
animations:
  button-0:
    type: "button"
    description: {from Step 3}
    transition: {transition value}
    states:
      default:
        background: {color}
        boxShadow: {shadow}
      hover:
        background: {color}
        boxShadow: {shadow}
  card-0:
    {similar structure}
```

### 6.3: Write File

Use Write tool to save the YAML content to:
```
design-system/extracted/{siteName}/data.yaml
```

---

## STEP 7: Final Report

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ EXTRACTION COMPLETE: ${siteName}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Coverage: ${countDetectedSections()}/17 sections

🎨 Design Tokens:
   ✅ Colors: ${colors.backgrounds.length} backgrounds (with usage)
   ✅ Typography: ${typography.allFonts.length} fonts
   ✅ Spacing: ${spacing.detectedGrid}px grid detected
   ✅ Components: ${buttons.length} buttons, ${cards.length} cards
   ✅ Shadows: ${shadows.shadows.length} unique values
   ✅ Animations: ${animations.keyframes.length} @keyframes

🧠 Psychology Analysis:
   ✅ Style classification
   ✅ Emotions evoked
   ✅ Target audience
   ✅ Visual principles
   ✅ Why it works

📸 Screenshots: ${Object.keys(componentAnimations).length * 2 + 1} captured

📁 Output:
   ✓ design-system/extracted/${siteName}/data.yaml
   ✓ design-system/extracted/${siteName}/screenshots/

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 Next Steps:

1. Extract more references (optional):
   /extract https://linear.app

2. Generate design system:
   /designsetup @prd.md

   → Will read: design-system/extracted/*/data.yaml
   → Will merge: Psychology + Tokens + Animations
   → Will output: design-system/data.yaml (final)

3. Review extracted data:
   cat design-system/extracted/${siteName}/data.yaml

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Error Handling

### Critical Errors (Stop Execution)

**Navigation failures** - If agent-browser navigation fails:
1. Catch the error from `agent-browser open`
2. Return error message:
   ```
   ❌ Failed to load URL: {url}

   Error: {error.message}

   Check:
   - Is the URL accessible?
   - Is agent-browser installed? (npm install -g agent-browser)
   - Did you run `agent-browser install` to get Chromium?
   ```
3. Stop execution (cannot proceed without page loaded)

### Non-Critical Errors (Continue with Fallbacks)

**Extraction failures** - If individual extraction steps fail:
1. Log warning message (e.g., "Color extraction failed: {error.message}")
2. Use fallback empty data:
   - Colors: `{ backgrounds: [], texts: [], borders: [] }`
   - Typography: `{ h1: [], h2: [], h3: [], body: [], allFonts: [], allWeights: [], allSizes: [] }`
   - Shadows: `{ shadows: [], borderRadii: [], borderWidths: [] }`
   - Components: `[]` (empty array)
3. Continue with other extractions (parallel execution means one failure doesn't block others)
4. Final YAML will mark section as `detected: false` if no data extracted

**Screenshot failures**:
- Full-page screenshot fails → Fallback to viewport screenshot
- Component screenshot fails → Skip that component, continue with others
- Psychology analysis screenshot missing → Use viewport screenshot as fallback

**YAML generation**:
- Missing data sections → Mark `detected: false` in YAML
- Invalid data → Use empty defaults, note in coverage percentage

---

**Now execute the extraction.**
