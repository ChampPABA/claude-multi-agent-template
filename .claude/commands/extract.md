# /extract - Extract Design System from Website (Component-Level)

You are an expert design systems engineer with deep knowledge of CSS, animations, and UX patterns.

Your task is to extract comprehensive design data from a website and save it as reusable YAML files with component-level detail.

---

## 📖 Usage

```bash
/extract <URL>

Arguments:
  URL              Required. Website URL to extract from

Examples:
  /extract https://airbnb.com
  /extract https://blackbird.com
  /extract https://linear.app
```

---

## 🎯 Mission

Extract ALL design data from a website and save to `design-system/extracted/{site-name}/`:
- `data.yaml` - Complete 17-section design data + animations
- `analysis.md` - Psychology & design philosophy analysis
- `screenshots/` - Component screenshots (default + hover/focus states)

**Key Principles:**
1. **Component-Level Detail**: Extract every component type with all states
2. **Animation Capture**: Before/after screenshots for all interactive states
3. **17 Sections Mandatory**: Template-based extraction (fallback if not found)
4. **Reusable**: Output can be used by multiple projects

---

## 🔍 STEP 0: Parse Input & Setup

```javascript
// Parse URL
const input = args[0];
if (!input) {
  return error('URL required. Usage: /extract https://airbnb.com');
}

// Normalize URL
let url = input.trim();
if (!url.startsWith('http://') && !url.startsWith('https://')) {
  url = 'https://' + url;
}

// Auto-detect site name
const siteName = new URL(url).hostname
  .replace('www.', '')
  .replace(/\.[^.]+$/, ''); // Remove TLD
// e.g., "airbnb.com" → "airbnb"

// Check if already extracted
const extractedPath = `design-system/extracted/${siteName}`;
if (exists(extractedPath + '/data.yaml')) {
  const existingData = YAML.parse(Read(extractedPath + '/data.yaml'));
  const extractedDate = existingData.meta.extracted_at;

  const response = await AskUserQuestion({
    questions: [{
      question: `Site "${siteName}" was already extracted on ${extractedDate}. Re-extract?`,
      header: "Re-extract?",
      multiSelect: false,
      options: [
        { label: "Yes, re-extract", description: "Overwrite previous data" },
        { label: "No, cancel", description: "Keep existing data" }
      ]
    }]
  });

  if (response.answers["Re-extract?"] === "No, cancel") {
    return output('Extraction cancelled. Existing data preserved.');
  }
}

// Create directories
Bash: mkdir -p design-system/extracted/${siteName}/screenshots
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

```javascript
// Navigate
await mcp__chrome-devtools__navigate_page({ url });

// Smart wait
try {
  const snapshot = await mcp__chrome-devtools__take_snapshot({ verbose: false });

  // Find main heading
  const headings = snapshot.split('\n')
    .filter(line => line.includes('[heading]'))
    .slice(0, 3);

  if (headings.length > 0) {
    const mainText = headings[0].split('"')[1]; // Extract text

    await mcp__chrome-devtools__wait_for({
      text: mainText,
      timeout: 15000
    });
  } else {
    // Fallback: fixed wait
    await sleep(5000);
  }
} catch {
  await sleep(5000);
}

// Verify loaded
const readyState = await mcp__chrome-devtools__evaluate_script({
  function: '() => document.readyState'
});

if (readyState !== 'complete') {
  await sleep(3000);
}
```

**Report:**
```
✅ Page loaded successfully

🔄 Extracting CSS data (17 sections)...
```

---

## STEP 2: Extract CSS Data (17 Sections in Parallel)

Run all extraction scripts in parallel for speed:

```javascript
const extractionPromises = [
  extractColors(),
  extractTypography(),
  extractShadows(),
  extractSpacing(),
  extractButtons(),
  extractCards(),
  extractInputs(),
  extractAnimations()
];

const [
  colors,
  typography,
  shadows,
  spacing,
  buttons,
  cards,
  inputs,
  animations
] = await Promise.all(extractionPromises);
```

### 2.1: Extract Colors

```javascript
async function extractColors() {
  return await mcp__chrome-devtools__evaluate_script({
    function: `() => {
      const allElements = document.querySelectorAll('*');
      const colors = {
        backgrounds: new Set(),
        texts: new Set(),
        borders: new Set()
      };

      allElements.forEach(el => {
        const s = window.getComputedStyle(el);
        if (s.backgroundColor && s.backgroundColor !== 'rgba(0, 0, 0, 0)') {
          colors.backgrounds.add(s.backgroundColor);
        }
        if (s.color) colors.texts.add(s.color);
        if (s.borderColor && s.borderColor !== 'rgba(0, 0, 0, 0)') {
          colors.borders.add(s.borderColor);
        }
      });

      // Convert RGB to HEX
      const rgbToHex = (rgb) => {
        const match = rgb.match(/\\d+/g);
        if (!match) return rgb;
        const hex = match.slice(0, 3).map(x => {
          const h = parseInt(x).toString(16);
          return h.length === 1 ? '0' + h : h;
        });
        return '#' + hex.join('').toUpperCase();
      };

      return {
        backgrounds: Array.from(colors.backgrounds).slice(0, 30).map(c => ({
          rgb: c,
          hex: rgbToHex(c)
        })),
        texts: Array.from(colors.texts).slice(0, 20).map(c => ({
          rgb: c,
          hex: rgbToHex(c)
        })),
        borders: Array.from(colors.borders).slice(0, 15).map(c => ({
          rgb: c,
          hex: rgbToHex(c)
        }))
      };
    }`
  });
}
```

### 2.2: Extract Typography

```javascript
async function extractTypography() {
  return await mcp__chrome-devtools__evaluate_script({
    function: `() => {
      const fonts = new Set();
      const weights = new Set();
      const sizes = new Set();

      const typography = {
        h1: [],
        h2: [],
        h3: [],
        body: []
      };

      // Headings
      ['h1', 'h2', 'h3'].forEach(tag => {
        Array.from(document.querySelectorAll(tag)).slice(0, 3).forEach(el => {
          const s = window.getComputedStyle(el);
          typography[tag].push({
            text: el.textContent.trim().substring(0, 50),
            fontSize: s.fontSize,
            fontWeight: s.fontWeight,
            fontFamily: s.fontFamily,
            lineHeight: s.lineHeight,
            letterSpacing: s.letterSpacing,
            textTransform: s.textTransform,
            color: s.color
          });
          fonts.add(s.fontFamily);
          weights.add(s.fontWeight);
          sizes.add(s.fontSize);
        });
      });

      // Body text
      Array.from(document.querySelectorAll('p, div, span')).slice(0, 20).forEach(el => {
        const s = window.getComputedStyle(el);
        if (el.textContent.trim().length > 20) {
          typography.body.push({
            fontSize: s.fontSize,
            fontWeight: s.fontWeight,
            lineHeight: s.lineHeight,
            fontFamily: s.fontFamily,
            color: s.color
          });
          fonts.add(s.fontFamily);
          weights.add(s.fontWeight);
          sizes.add(s.fontSize);
        }
      });

      return {
        ...typography,
        allFonts: Array.from(fonts),
        allWeights: Array.from(weights).sort((a, b) => parseInt(a) - parseInt(b)),
        allSizes: Array.from(sizes).sort((a, b) => parseFloat(a) - parseFloat(b))
      };
    }`
  });
}
```

### 2.3: Extract Shadows & Effects

```javascript
async function extractShadows() {
  return await mcp__chrome-devtools__evaluate_script({
    function: `() => {
      const allElements = document.querySelectorAll('*');
      const effects = {
        shadows: new Set(),
        borderRadii: new Set(),
        borderWidths: new Set()
      };

      allElements.forEach(el => {
        const s = window.getComputedStyle(el);
        if (s.boxShadow && s.boxShadow !== 'none') {
          effects.shadows.add(s.boxShadow);
        }
        if (s.borderRadius && s.borderRadius !== '0px') {
          effects.borderRadii.add(s.borderRadius);
        }
        if (s.borderWidth && s.borderWidth !== '0px') {
          effects.borderWidths.add(s.borderWidth);
        }
      });

      return {
        shadows: Array.from(effects.shadows).slice(0, 15),
        borderRadii: Array.from(effects.borderRadii).slice(0, 15),
        borderWidths: Array.from(effects.borderWidths).slice(0, 10)
      };
    }`
  });
}
```

### 2.4: Extract Spacing

```javascript
async function extractSpacing() {
  return await mcp__chrome-devtools__evaluate_script({
    function: `() => {
      const spacing = {
        paddings: new Set(),
        margins: new Set(),
        gaps: new Set()
      };

      Array.from(document.querySelectorAll('*')).slice(0, 100).forEach(el => {
        const s = window.getComputedStyle(el);

        // Padding
        if (s.padding && s.padding !== '0px') {
          [s.padding, s.paddingTop, s.paddingRight, s.paddingBottom, s.paddingLeft]
            .forEach(v => spacing.paddings.add(v));
        }

        // Margin
        if (s.margin && s.margin !== '0px') {
          [s.marginTop, s.marginBottom].forEach(v => {
            if (v && v !== '0px' && v !== 'auto') spacing.margins.add(v);
          });
        }

        // Gap
        if (s.gap && s.gap !== 'normal' && s.gap !== '0px') {
          spacing.gaps.add(s.gap);
        }
      });

      // Detect grid pattern
      const allValues = [
        ...spacing.paddings,
        ...spacing.margins,
        ...spacing.gaps
      ]
        .map(v => parseFloat(v))
        .filter(v => !isNaN(v) && v > 0)
        .sort((a, b) => a - b);

      // Find GCD (grid base)
      const gcd = (a, b) => b === 0 ? a : gcd(b, a % b);
      const gridBase = allValues.length > 1
        ? allValues.reduce((acc, val) => gcd(acc, val), allValues[0])
        : 8;

      return {
        paddings: Array.from(spacing.paddings).slice(0, 20),
        margins: Array.from(spacing.margins).slice(0, 20),
        gaps: Array.from(spacing.gaps).slice(0, 10),
        detectedGrid: Math.round(gridBase) || 8,
        commonValues: [...new Set(allValues)].slice(0, 15)
      };
    }`
  });
}
```

### 2.5-2.7: Extract Components

```javascript
async function extractButtons() {
  return await mcp__chrome-devtools__evaluate_script({
    function: `() => {
      return Array.from(document.querySelectorAll('button, a[role="button"], .btn, [class*="button"], [class*="Button"]'))
        .slice(0, 10)
        .map((btn, i) => {
          btn.setAttribute('data-extract-id', 'button-' + i);
          const s = window.getComputedStyle(btn);
          return {
            id: 'button-' + i,
            text: btn.textContent.trim().substring(0, 30),
            backgroundColor: s.backgroundColor,
            color: s.color,
            padding: s.padding,
            paddingTop: s.paddingTop,
            paddingRight: s.paddingRight,
            paddingBottom: s.paddingBottom,
            paddingLeft: s.paddingLeft,
            border: s.border,
            borderWidth: s.borderWidth,
            borderColor: s.borderColor,
            borderRadius: s.borderRadius,
            fontSize: s.fontSize,
            fontWeight: s.fontWeight,
            textTransform: s.textTransform,
            letterSpacing: s.letterSpacing,
            boxShadow: s.boxShadow,
            transition: s.transition
          };
        });
    }`
  });
}

async function extractCards() {
  return await mcp__chrome-devtools__evaluate_script({
    function: `() => {
      const selectors = [
        '[class*="card"]', '[class*="Card"]',
        'article', 'section',
        '[class*="box"]', '[class*="Box"]'
      ];

      return Array.from(document.querySelectorAll(selectors.join(', ')))
        .slice(0, 10)
        .map((card, i) => {
          card.setAttribute('data-extract-id', 'card-' + i);
          const s = window.getComputedStyle(card);
          return {
            id: 'card-' + i,
            className: card.className,
            backgroundColor: s.backgroundColor,
            padding: s.padding,
            border: s.border,
            borderRadius: s.borderRadius,
            boxShadow: s.boxShadow,
            transition: s.transition
          };
        });
    }`
  });
}

async function extractInputs() {
  return await mcp__chrome-devtools__evaluate_script({
    function: `() => {
      return Array.from(document.querySelectorAll('input[type="text"], input[type="email"], input[type="password"], textarea'))
        .slice(0, 5)
        .map((input, i) => {
          input.setAttribute('data-extract-id', 'input-' + i);
          const s = window.getComputedStyle(input);
          return {
            id: 'input-' + i,
            type: input.type || 'textarea',
            height: s.height,
            padding: s.padding,
            border: s.border,
            borderRadius: s.borderRadius,
            fontSize: s.fontSize,
            backgroundColor: s.backgroundColor,
            transition: s.transition
          };
        });
    }`
  });
}
```

### 2.8: Extract Animations (@keyframes + transitions)

```javascript
async function extractAnimations() {
  return await mcp__chrome-devtools__evaluate_script({
    function: `() => {
      const keyframes = [];
      const transitions = [];

      // Extract @keyframes
      Array.from(document.styleSheets).forEach(sheet => {
        try {
          Array.from(sheet.cssRules || []).forEach(rule => {
            if (rule.type === CSSRule.KEYFRAMES_RULE) {
              keyframes.push({
                name: rule.name,
                css: rule.cssText
              });
            }
          });
        } catch(e) {
          // CORS - skip
        }
      });

      // Extract elements with transitions
      Array.from(document.querySelectorAll('*')).slice(0, 50).forEach(el => {
        const s = window.getComputedStyle(el);
        if (s.transition && s.transition !== 'all 0s ease 0s') {
          transitions.push({
            selector: el.className || el.tagName,
            transition: s.transition,
            transitionDuration: s.transitionDuration,
            transitionTimingFunction: s.transitionTimingFunction,
            transitionProperty: s.transitionProperty
          });
        }
      });

      return { keyframes, transitions };
    }`
  });
}
```

**Report:**
```
✅ CSS Data Extracted!

📊 Summary:
   - Colors: ${colors.backgrounds.length} backgrounds, ${colors.texts.length} texts, ${colors.borders.length} borders
   - Typography: ${typography.allFonts.length} fonts, ${typography.allWeights.length} weights
   - Shadows: ${shadows.shadows.length} unique values
   - Spacing: ${spacing.detectedGrid}px grid detected
   - Buttons: ${buttons.length} extracted
   - Cards: ${cards.length} extracted
   - Inputs: ${inputs.length} extracted
   - Animations: ${animations.keyframes.length} @keyframes, ${animations.transitions.length} transitions

🔄 Extracting component animations (hover/focus states)...
```

---

## STEP 3: Extract Component Animations (Interactive States)

For each component, capture before/after states:

```javascript
const componentAnimations = {};

// Buttons
for (let i = 0; i < Math.min(buttons.length, 3); i++) {
  const btnId = `button-${i}`;

  // Screenshot: Default state
  await mcp__chrome-devtools__evaluate_script({
    function: `() => {
      const el = document.querySelector('[data-extract-id="${btnId}"]');
      if (el) el.scrollIntoView({ block: 'center' });
    }`
  });
  await sleep(500);

  await mcp__chrome-devtools__take_screenshot({
    filePath: `design-system/extracted/${siteName}/screenshots/${btnId}-default.png`
  });

  // Get default computed styles
  const defaultStyle = await mcp__chrome-devtools__evaluate_script({
    function: `() => {
      const el = document.querySelector('[data-extract-id="${btnId}"]');
      if (!el) return null;
      const s = window.getComputedStyle(el);
      return {
        background: s.backgroundColor,
        color: s.color,
        border: s.border,
        borderRadius: s.borderRadius,
        boxShadow: s.boxShadow,
        transform: s.transform,
        opacity: s.opacity
      };
    }`
  });

  // Trigger hover
  await mcp__chrome-devtools__evaluate_script({
    function: `() => {
      const el = document.querySelector('[data-extract-id="${btnId}"]');
      if (el) el.dispatchEvent(new MouseEvent('mouseenter', { bubbles: true }));
    }`
  });
  await sleep(500); // Wait for transition

  // Screenshot: Hover state
  await mcp__chrome-devtools__take_screenshot({
    filePath: `design-system/extracted/${siteName}/screenshots/${btnId}-hover.png`
  });

  // Get hover computed styles
  const hoverStyle = await mcp__chrome-devtools__evaluate_script({
    function: `() => {
      const el = document.querySelector('[data-extract-id="${btnId}"]');
      if (!el) return null;
      const s = window.getComputedStyle(el);
      return {
        background: s.backgroundColor,
        color: s.color,
        border: s.border,
        borderRadius: s.borderRadius,
        boxShadow: s.boxShadow,
        transform: s.transform,
        opacity: s.opacity
      };
    }`
  });

  // Remove hover
  await mcp__chrome-devtools__evaluate_script({
    function: `() => {
      const el = document.querySelector('[data-extract-id="${btnId}"]');
      if (el) el.dispatchEvent(new MouseEvent('mouseleave'));
    }`
  });

  // Calculate changes
  componentAnimations[btnId] = {
    type: 'button',
    states: {
      default: defaultStyle,
      hover: hoverStyle
    },
    changes: {
      background_changed: defaultStyle.background !== hoverStyle.background,
      shadow_changed: defaultStyle.boxShadow !== hoverStyle.boxShadow,
      transform_changed: defaultStyle.transform !== hoverStyle.transform,
      border_changed: defaultStyle.border !== hoverStyle.border
    },
    transition: buttons[i].transition,
    description: generateDescription(defaultStyle, hoverStyle)
  };
}

// Cards (same pattern)
for (let i = 0; i < Math.min(cards.length, 3); i++) {
  // ... same process for cards ...
}

// Inputs (focus state)
for (let i = 0; i < Math.min(inputs.length, 3); i++) {
  // ... same process with 'focus' event instead of 'mouseenter' ...
}

function generateDescription(defaultStyle, hoverStyle) {
  const changes = [];

  if (defaultStyle.boxShadow !== hoverStyle.boxShadow) {
    if (defaultStyle.boxShadow === 'none' && hoverStyle.boxShadow !== 'none') {
      changes.push('Shadow appears');
    } else if (defaultStyle.boxShadow !== 'none' && hoverStyle.boxShadow !== 'none') {
      changes.push('Shadow changes');
    }
  }

  if (defaultStyle.transform !== hoverStyle.transform) {
    if (hoverStyle.transform.includes('scale')) {
      changes.push('Scales up');
    }
    if (hoverStyle.transform.includes('translateY')) {
      changes.push('Moves up');
    }
  }

  if (defaultStyle.background !== hoverStyle.background) {
    changes.push('Background changes');
  }

  return changes.length > 0 ? changes.join(' + ') : 'No visible changes';
}
```

**Report:**
```
✅ Component Animations Extracted!

📸 Screenshots captured:
   - ${Object.keys(componentAnimations).length} components
   - ${Object.keys(componentAnimations).length * 2} screenshots (default + hover/focus)

🔄 Capturing full-page screenshot...
```

---

## STEP 4: Full-Page Screenshot

```javascript
// Create temp directory
await Bash: mkdir -p design-system/extracted/${siteName}/screenshots

// Try fullpage
try {
  await mcp__chrome-devtools__take_screenshot({
    fullPage: true,
    format: 'png',
    filePath: `design-system/extracted/${siteName}/screenshots/full-page.png`
  });
} catch {
  // Fallback: viewport only
  await mcp__chrome-devtools__take_screenshot({
    fullPage: false,
    format: 'png',
    filePath: `design-system/extracted/${siteName}/screenshots/viewport.png`
  });
}
```

---

## STEP 5: AI Psychology Analysis

Read screenshot and analyze:

```javascript
const screenshotPath = exists(`design-system/extracted/${siteName}/screenshots/full-page.png`)
  ? `design-system/extracted/${siteName}/screenshots/full-page.png`
  : `design-system/extracted/${siteName}/screenshots/viewport.png`;

const screenshot = Read(screenshotPath);

const analysisPrompt = `
You are a UX/UI design psychologist and systems architect.

Analyze this website's design and provide deep psychology insights.

Visual Screenshot: [attached]

Extracted CSS Data:
- Colors: ${JSON.stringify(colors, null, 2)}
- Typography: ${JSON.stringify(typography, null, 2)}
- Shadows: ${JSON.stringify(shadows, null, 2)}
- Spacing: ${JSON.stringify(spacing, null, 2)}
- Button Styles: ${JSON.stringify(buttons.slice(0, 2), null, 2)}
- Card Styles: ${JSON.stringify(cards.slice(0, 2), null, 2)}

Component Animations:
${Object.entries(componentAnimations).slice(0, 3).map(([id, anim]) =>
  `- ${id}: ${anim.description}`
).join('\n')}

Wrap your analysis in <pondering> tags and include:

1. **Design Style Classification** (Neo-Brutalism, Minimalist, Modern SaaS, etc.)
2. **Visual Principles** (what design principles are used?)
3. **Psychology** (what emotions does it evoke? why?)
4. **Target Audience** (who is this for?)
5. **Key Differentiators** (how is it different from typical sites?)
6. **Design Philosophy** (core beliefs that guide this design)

Be specific with examples from the CSS data.
`;

const analysis = await LLM({
  prompt: analysisPrompt,
  images: [screenshot]
});

Write(`design-system/extracted/${siteName}/analysis.md`, analysis);
```

**Report:**
```
✅ Psychology Analysis Complete!

🧠 Design style detected from analysis
📁 Saved: analysis.md

🔄 Generating final YAML output...
```

---

## STEP 6: Generate data.yaml (17 Sections)

```javascript
const yamlData = {
  meta: {
    site_name: siteName,
    url: url,
    extracted_at: new Date().toISOString(),
    extractor_version: '2.0.0',
    coverage: {
      total_sections: 17,
      detected_sections: 15, // Count how many have detected: true
      percentage: Math.round((15 / 17) * 100)
    }
  },

  sections: {
    overview: {
      detected: true,
      style: 'Auto-detected from analysis',
      tech_stack: 'Framework-agnostic'
    },

    design_philosophy: {
      detected: true,
      from_analysis: true
    },

    color_palette: {
      detected: true,
      primary: colors.backgrounds.slice(0, 5),
      secondary: colors.backgrounds.slice(5, 10),
      text_colors: colors.texts,
      border_colors: colors.borders
    },

    typography: {
      detected: true,
      fonts: typography.allFonts,
      weights: typography.allWeights,
      sizes: typography.allSizes,
      h1: typography.h1,
      h2: typography.h2,
      h3: typography.h3,
      body: typography.body
    },

    spacing_system: {
      detected: true,
      grid_base: spacing.detectedGrid,
      paddings: spacing.paddings,
      margins: spacing.margins,
      gaps: spacing.gaps,
      common_values: spacing.commonValues
    },

    component_styles: {
      detected: true,
      buttons: buttons.map((btn, i) => ({
        ...btn,
        animation: componentAnimations[`button-${i}`] || null
      })),
      cards: cards.map((card, i) => ({
        ...card,
        animation: componentAnimations[`card-${i}`] || null
      })),
      inputs: inputs.map((input, i) => ({
        ...input,
        animation: componentAnimations[`input-${i}`] || null
      }))
    },

    shadows_elevation: {
      detected: true,
      values: shadows.shadows
    },

    animations_transitions: {
      detected: true,
      keyframes: animations.keyframes,
      transitions: animations.transitions
    },

    border_styles: {
      detected: true,
      widths: shadows.borderWidths
    },

    border_radius: {
      detected: true,
      values: shadows.borderRadii
    },

    opacity_transparency: {
      detected: true,
      values: [0.5, 0.7, 0.9] // Standard
    },

    z_index_layers: {
      detected: false,
      fallback: 'standard'
    },

    responsive_breakpoints: {
      detected: false,
      fallback: 'standard'
    },

    css_variables: {
      generated: true
    },

    layout_patterns: {
      detected: true,
      container_width: '1280px',
      grid_columns: 12
    },

    example_components: {
      generated: true
    },

    additional_sections: {
      accessibility: { detected: true },
      best_practices: { generated: true }
    }
  },

  animations: componentAnimations
};

const yamlContent = YAML.stringify(yamlData, null, 2);
Write(`design-system/extracted/${siteName}/data.yaml`, yamlContent);
```

---

## STEP 7: Final Report

```
✅ Extraction Complete: ${siteName}

📊 Coverage: ${yamlData.meta.coverage.detected_sections}/17 sections (${yamlData.meta.coverage.percentage}%)
   ✅ Colors (${colors.backgrounds.length + colors.texts.length + colors.borders.length} total)
   ✅ Typography (${typography.allFonts.length} fonts, ${typography.allWeights.length} weights)
   ✅ Spacing (${spacing.detectedGrid}px grid detected)
   ✅ Components (${buttons.length} buttons, ${cards.length} cards, ${inputs.length} inputs)
   ✅ Shadows (${shadows.shadows.length} unique values)
   ✅ Animations (${animations.keyframes.length} @keyframes, ${animations.transitions.length} transitions)
   ${yamlData.sections.z_index_layers.detected ? '✅' : '❌'} Z-index
   ${yamlData.sections.responsive_breakpoints.detected ? '✅' : '❌'} Breakpoints

📸 Screenshots: ${Object.keys(componentAnimations).length * 2 + 1} captured
   - full-page.png (or viewport.png)
   - ${Object.keys(componentAnimations).length} components × 2 states

📁 Output:
   ✓ design-system/extracted/${siteName}/data.yaml
   ✓ design-system/extracted/${siteName}/analysis.md
   ✓ design-system/extracted/${siteName}/screenshots/ (${Object.keys(componentAnimations).length * 2 + 1} files)

⏱️ Time: ${Date.now() - startTime}ms

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 Next Steps:

1. Extract more sites:
   /extract https://blackbird.com
   /extract https://linear.app

2. Generate style guide:
   /designsetup @prd.md @project.md

3. Or review extracted data:
   cat design-system/extracted/${siteName}/analysis.md
```

---

## Error Handling

```javascript
try {
  await mcp__chrome-devtools__navigate_page({ url });
} catch (error) {
  return error(`
    ❌ Failed to load URL: ${url}

    Error: ${error.message}

    Check:
    - Is the URL accessible?
    - Is Chrome DevTools MCP running?
    - Try with --verbose for details
  `);
}

// Extraction failures are non-critical
try {
  const colors = await extractColors();
} catch (error) {
  console.warn('Color extraction failed:', error.message);
  colors = { backgrounds: [], texts: [], borders: [] };
}

// Screenshot failures are non-critical
try {
  await takeScreenshot();
} catch (error) {
  console.warn('Screenshot failed, continuing...');
}
```

---

**Now execute the extraction.**
