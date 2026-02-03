# Extraction Steps

Complete step-by-step guide for extracting design data from a website.

---

## STEP 0: Parse Input & Setup

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
   - Ask user: "Site '{siteName}' was already extracted on {extractedDate}. Re-extract?"
   - If user chooses "No", exit with message: "Extraction cancelled. Existing data preserved."

### 0.3: Create Output Directories

```bash
mkdir -p design-system/extracted/{siteName}/screenshots
```

---

## STEP 1: Navigate & Wait

### 1.1: Navigate to URL

Use agent-browser to navigate to the target URL:
```bash
agent-browser open {url}
```

### 1.2: Smart Wait for Page Load

1. Take DOM snapshot to analyze page structure
2. Find heading elements
3. If headings found:
   - Wait for first heading text (timeout: 15000ms)
4. If no headings found:
   - Fallback to sleep 5000ms

### 1.3: Verify Document Ready

1. Check document.readyState
2. If not "complete", sleep additional 3000ms

---

## STEP 2: Extract CSS Data (8 Parallel Extractions)

Run all extractions in parallel for speed.

### 2.1: Extract Colors

Extract from all elements using `window.getComputedStyle()`:
- Background colors (skip transparent)
- Text colors
- Border colors

Convert RGB to HEX, detect usage context, count frequency.

Output: `colors.backgrounds`, `colors.texts`, `colors.borders`

### 2.2: Extract Typography

Extract heading styles (h1, h2, h3) and body text:
- fontSize, fontWeight, fontFamily
- lineHeight, letterSpacing

Collect unique fonts, weights, sizes.

### 2.3: Extract Shadows & Effects

- boxShadow values (skip "none")
- borderRadius values (skip "0px")
- borderWidth values

### 2.4: Extract Spacing

- Padding values
- Margin values (skip "auto")
- Gap values

Detect spacing grid pattern (usually 4px or 8px base).

### 2.5: Extract Buttons

Query: `button`, `a[role="button"]`, `.btn`, `[class*="button"]`

For each button:
- Add `data-extract-id` attribute
- Extract styles: backgroundColor, color, padding, borderRadius, transition

### 2.6: Extract Cards

Query: `[class*="card"]`, `article`, `section`

Extract: backgroundColor, padding, border, boxShadow, transition

### 2.7: Extract Input Fields

Query: `input[type="text"]`, `textarea`, etc.

Extract: height, padding, border, borderRadius, transition

### 2.8: Extract Animations

1. CSS @keyframes from stylesheets
2. Transition properties from elements

---

## STEP 3: Extract Component Animations

For buttons, cards, and inputs:

1. Find element by data-extract-id
2. Scroll into view
3. Screenshot default state
4. Capture default computed styles
5. Trigger hover/focus event
6. Wait for transition (500ms)
7. Screenshot hover/focus state
8. Capture new computed styles
9. Remove hover/focus event
10. Compare and describe changes

---

## STEP 4: Full-Page Screenshot

1. Try full-page screenshot first
2. If fails, fallback to viewport-only
3. Save to `screenshots/full-page.png` or `screenshots/viewport.png`

---

## STEP 5: AI Psychology Analysis

Using the screenshot and extracted data, analyze:

1. **style_classification**: Neo-Brutalism, Minimalist, Glassmorphism, etc.
2. **emotions_evoked**: What feelings the design triggers
3. **target_audience**: Who this design appeals to
4. **visual_principles**: Key design patterns observed
5. **why_it_works**: Strategic design decisions
6. **design_philosophy**: Underlying beliefs

---

## STEP 6: Generate data.yaml

1. Calculate coverage metrics (X/17 sections)
2. Build YAML with all extracted data
3. Include psychology analysis
4. Write to `design-system/extracted/{siteName}/data.yaml`

→ See [output-format.md](output-format.md) for complete schema

---

## STEP 7: Final Report

Display extraction summary:
- Coverage percentage
- Design tokens extracted
- Psychology analysis status
- Screenshot count
- Output file paths
- Next steps
