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
    const mainText = headings[0].split('"')[1];

    await mcp__chrome-devtools__wait_for({
      text: mainText,
      timeout: 15000
    });
  } else {
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

### 2.1: Extract Colors (with usage detection)

```javascript
async function extractColors() {
  return await mcp__chrome-devtools__evaluate_script({
    function: `() => {
      const allElements = document.querySelectorAll('*');
      const colorMap = {
        backgrounds: new Map(),
        texts: new Map(),
        borders: new Map()
      };

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

      // Detect usage based on element context
      const detectUsage = (el, type) => {
        const tag = el.tagName.toLowerCase();
        const classes = el.className || '';

        if (type === 'background') {
          if (tag === 'button' || classes.includes('btn') || classes.includes('button')) return 'button-bg';
          if (tag === 'nav' || classes.includes('nav') || classes.includes('header')) return 'nav-bg';
          if (classes.includes('card') || classes.includes('box')) return 'card-bg';
          if (classes.includes('hero') || classes.includes('banner')) return 'hero-bg';
          if (tag === 'body' || classes.includes('main')) return 'page-bg';
          return 'surface';
        }

        if (type === 'text') {
          if (tag.match(/^h[1-6]$/)) return 'heading';
          if (tag === 'a') return 'link';
          if (tag === 'button') return 'button-text';
          if (classes.includes('muted') || classes.includes('secondary')) return 'muted-text';
          return 'body-text';
        }

        if (type === 'border') {
          if (tag === 'input' || tag === 'textarea') return 'input-border';
          if (classes.includes('card')) return 'card-border';
          return 'divider';
        }

        return 'general';
      };

      allElements.forEach(el => {
        const s = window.getComputedStyle(el);

        if (s.backgroundColor && s.backgroundColor !== 'rgba(0, 0, 0, 0)') {
          const hex = rgbToHex(s.backgroundColor);
          if (!colorMap.backgrounds.has(hex)) {
            colorMap.backgrounds.set(hex, {
              rgb: s.backgroundColor,
              hex: hex,
              usage: detectUsage(el, 'background'),
              count: 1
            });
          } else {
            colorMap.backgrounds.get(hex).count++;
          }
        }

        if (s.color) {
          const hex = rgbToHex(s.color);
          if (!colorMap.texts.has(hex)) {
            colorMap.texts.set(hex, {
              rgb: s.color,
              hex: hex,
              usage: detectUsage(el, 'text'),
              count: 1
            });
          } else {
            colorMap.texts.get(hex).count++;
          }
        }

        if (s.borderColor && s.borderColor !== 'rgba(0, 0, 0, 0)') {
          const hex = rgbToHex(s.borderColor);
          if (!colorMap.borders.has(hex)) {
            colorMap.borders.set(hex, {
              rgb: s.borderColor,
              hex: hex,
              usage: detectUsage(el, 'border'),
              count: 1
            });
          } else {
            colorMap.borders.get(hex).count++;
          }
        }
      });

      // Sort by count (most used first)
      const sortByCount = (map) => Array.from(map.values())
        .sort((a, b) => b.count - a.count)
        .slice(0, 20);

      return {
        backgrounds: sortByCount(colorMap.backgrounds),
        texts: sortByCount(colorMap.texts),
        borders: sortByCount(colorMap.borders)
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

        if (s.padding && s.padding !== '0px') {
          [s.padding, s.paddingTop, s.paddingRight, s.paddingBottom, s.paddingLeft]
            .forEach(v => spacing.paddings.add(v));
        }

        if (s.margin && s.margin !== '0px') {
          [s.marginTop, s.marginBottom].forEach(v => {
            if (v && v !== '0px' && v !== 'auto') spacing.margins.add(v);
          });
        }

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
            border: s.border,
            borderRadius: s.borderRadius,
            fontSize: s.fontSize,
            fontWeight: s.fontWeight,
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

### 2.8: Extract Animations

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
            transitionTimingFunction: s.transitionTimingFunction
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

For each component, capture before/after states:

```javascript
const componentAnimations = {};

// Buttons
for (let i = 0; i < Math.min(buttons.length, 3); i++) {
  const btnId = `button-${i}`;

  // Scroll into view
  await mcp__chrome-devtools__evaluate_script({
    function: `() => {
      const el = document.querySelector('[data-extract-id="${btnId}"]');
      if (el) el.scrollIntoView({ block: 'center' });
    }`
  });
  await sleep(500);

  // Screenshot: Default state
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
        boxShadow: s.boxShadow,
        transform: s.transform
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
  await sleep(500);

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
        boxShadow: s.boxShadow,
        transform: s.transform
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

  // Generate description
  const changes = [];
  if (defaultStyle.boxShadow !== hoverStyle.boxShadow) changes.push('Shadow changes');
  if (defaultStyle.transform !== hoverStyle.transform) changes.push('Transform changes');
  if (defaultStyle.background !== hoverStyle.background) changes.push('Background changes');

  componentAnimations[btnId] = {
    type: 'button',
    states: { default: defaultStyle, hover: hoverStyle },
    transition: buttons[i].transition,
    description: changes.length > 0 ? changes.join(' + ') : 'No visible changes'
  };
}

// Repeat for cards and inputs...
```

---

## STEP 4: Full-Page Screenshot

```javascript
await Bash: mkdir -p design-system/extracted/${siteName}/screenshots

try {
  await mcp__chrome-devtools__take_screenshot({
    fullPage: true,
    format: 'png',
    filePath: `design-system/extracted/${siteName}/screenshots/full-page.png`
  });
} catch {
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
You are a UX/UI design psychologist.

Analyze this website's design and provide insights in YAML format.

Visual Screenshot: [attached]

Extracted CSS Data:
- Colors: ${JSON.stringify(colors, null, 2)}
- Typography: ${JSON.stringify(typography.allFonts, null, 2)}

Return YAML format:

\`\`\`yaml
psychology:
  style_classification: # e.g., Neo-Brutalism, Minimalist, Modern SaaS

  emotions_evoked:
    - emotion: Trust
      reason: "Soft rounded corners reduce anxiety"
    - emotion: Adventure
      reason: "Vibrant colors suggest excitement"

  target_audience:
    primary:
      description: "Travelers seeking unique accommodations"
      age_range: "25-45"
      tech_savvy: high
    secondary:
      description: "Hosts listing their properties"

  visual_principles:
    - name: "Photo-First Design"
      description: "Large images dominate, UI recedes"
    - name: "Soft & Approachable"
      description: "Rounded corners, light grays feel warm"

  why_it_works:
    - "Marketplace requires trust → Clear info, ratings, soft design"
    - "Travel is emotional → Photo-first, inspirational imagery"

  design_philosophy:
    core_belief: "Let the content shine"
    key_principles:
      - "Photography is hero"
      - "Consistency builds trust"
      - "Subtle brand presence"
\`\`\`

Be specific with examples from the visual.
`;

const psychologyYaml = await LLM({
  prompt: analysisPrompt,
  images: [screenshot]
});
```

---

## STEP 6: Generate data.yaml (17 Sections + Psychology)

```javascript
const yamlContent = `# Design Extraction: ${siteName}
# Extracted: ${new Date().toISOString()}
# URL: ${url}

meta:
  site_name: ${siteName}
  url: ${url}
  extracted_at: ${new Date().toISOString()}
  extractor_version: "2.1.0"
  coverage:
    total_sections: 17
    detected_sections: ${countDetectedSections()}
    percentage: ${Math.round((countDetectedSections() / 17) * 100)}

# ============================================
# PSYCHOLOGY & ANALYSIS
# ============================================

${psychologyYaml}

# ============================================
# DESIGN TOKENS
# ============================================

sections:
  overview:
    detected: true
    style: "${detectStyle()}"
    tech_stack: Framework-agnostic

  color_palette:
    detected: true
    primary:
${colors.backgrounds.slice(0, 5).map(c => `      - hex: "${c.hex}"
        rgb: "${c.rgb}"
        usage: "${c.usage}"`).join('\n')}

    text_colors:
${colors.texts.slice(0, 5).map(c => `      - hex: "${c.hex}"
        usage: "${c.usage}"`).join('\n')}

    border_colors:
${colors.borders.slice(0, 3).map(c => `      - hex: "${c.hex}"
        usage: "${c.usage}"`).join('\n')}

  typography:
    detected: true
    fonts:
${typography.allFonts.slice(0, 3).map(f => `      - "${f}"`).join('\n')}
    weights: [${typography.allWeights.join(', ')}]
    sizes: [${typography.allSizes.join(', ')}]

  spacing_system:
    detected: true
    grid_base: ${spacing.detectedGrid}
    common_values: [${spacing.commonValues.join(', ')}]

  component_styles:
    detected: true
    buttons:
${buttons.slice(0, 3).map(btn => `      - id: "${btn.id}"
        text: "${btn.text}"
        backgroundColor: "${btn.backgroundColor}"
        color: "${btn.color}"
        padding: "${btn.padding}"
        borderRadius: "${btn.borderRadius}"
        transition: "${btn.transition}"
        hover_animation: "${componentAnimations[btn.id]?.description || 'none'}"`).join('\n')}

    cards:
${cards.slice(0, 3).map(card => `      - id: "${card.id}"
        backgroundColor: "${card.backgroundColor}"
        padding: "${card.padding}"
        borderRadius: "${card.borderRadius}"
        boxShadow: "${card.boxShadow}"
        hover_animation: "${componentAnimations[card.id]?.description || 'none'}"`).join('\n')}

  shadows_elevation:
    detected: true
    values:
${shadows.shadows.slice(0, 5).map(s => `      - "${s}"`).join('\n')}

  animations_transitions:
    detected: true
    keyframes:
${animations.keyframes.slice(0, 5).map(k => `      - name: "${k.name}"`).join('\n')}
    transitions:
${animations.transitions.slice(0, 5).map(t => `      - duration: "${t.transitionDuration}"
        timing: "${t.transitionTimingFunction}"`).join('\n')}

  border_radius:
    detected: true
    values: [${shadows.borderRadii.slice(0, 8).join(', ')}]

  border_styles:
    detected: true
    widths: [${shadows.borderWidths.join(', ')}]

  layout_patterns:
    detected: true
    container_width: "1280px"
    grid_columns: 12

# ============================================
# COMPONENT ANIMATIONS (DETAILED)
# ============================================

animations:
${Object.entries(componentAnimations).map(([id, anim]) => `  ${id}:
    type: "${anim.type}"
    description: "${anim.description}"
    transition: "${anim.transition}"
    states:
      default:
        background: "${anim.states.default?.background || 'none'}"
        boxShadow: "${anim.states.default?.boxShadow || 'none'}"
      hover:
        background: "${anim.states.hover?.background || 'none'}"
        boxShadow: "${anim.states.hover?.boxShadow || 'none'}"`).join('\n')}
`;

Write(`design-system/extracted/${siteName}/data.yaml`, yamlContent);
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
  `);
}

// Extraction failures are non-critical
try {
  const colors = await extractColors();
} catch (error) {
  console.warn('Color extraction failed:', error.message);
  colors = { backgrounds: [], texts: [], borders: [] };
}
```

---

**Now execute the extraction.**
