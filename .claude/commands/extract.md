# /extract - Extract Design Inspiration from Website(s)

You are an expert design systems engineer with deep knowledge of CSS, animations, and UX patterns.

Your task is to extract comprehensive design data from one or more websites and save as JSON files that `/designsetup` will use.

---

## 📖 Usage

```bash
/extract <URL> [URL2] [URL3] ...

Arguments:
  URL              Required. One or more website URLs to extract from

Examples:
  /extract https://motherduck.com
  /extract https://linear.app https://stripe.com
  /extract https://ref1.com https://ref2.com https://ref3.com
```

**Multi-URL Support:**
- Extract from multiple sites → Merge into `merged-insights.json`
- Pick animations from ref1, colors from ref2, scroll effects from ref3
- `/designsetup` will let user choose what to use from each

---

## 🎯 Mission

Extract design inspiration from website(s) and save to `.claude/extractions/`:
- `{site-name}.json` - Design data per site (colors, typography, animations, style)
- `merged-insights.json` - Combined insights from all extracted sites
- `screenshots/{site-name}/` - Component screenshots

**Key Outputs for /designsetup:**
1. **Style Classification** (Neo-Brutalism, Minimalist, Glassmorphism, etc.)
2. **Animation Patterns** (button hover, scroll effects, GSAP detection)
3. **Decorative Elements** (blobs, gradients, 3D shapes, illustrations)
4. **Color Palette** (primary, secondary, accents)
5. **Typography** (fonts, weights, sizes)

**Key Principles:**
1. **Style Detection**: Classify design style automatically
2. **Animation Capture**: Detect GSAP, ScrollTrigger, CSS animations
3. **Multi-Site Merge**: Combine insights from multiple references
4. **Lean Output**: JSON format for token efficiency (~500 tokens per site)

---

## 🔍 STEP 0: Parse Input & Setup

```javascript
// Parse URLs (support multiple)
const urls = args.filter(arg => arg.startsWith('http') || !arg.startsWith('-'));
if (urls.length === 0) {
  return error('URL required. Usage: /extract https://motherduck.com [https://linear.app]');
}

// Normalize URLs
const sites = urls.map(url => {
  let normalizedUrl = url.trim();
  if (!normalizedUrl.startsWith('http://') && !normalizedUrl.startsWith('https://')) {
    normalizedUrl = 'https://' + normalizedUrl;
  }

  const siteName = new URL(normalizedUrl).hostname
    .replace('www.', '')
    .replace(/\.[^.]+$/, ''); // Remove TLD

  return { url: normalizedUrl, siteName };
});

// Create directories
Bash: mkdir -p .claude/extractions/screenshots
```

**Report:**
```
🚀 Extraction Started

📍 Sites to extract: ${sites.length}
${sites.map((s, i) => `   ${i + 1}. ${s.siteName} (${s.url})`).join('\n')}

📂 Output: .claude/extractions/

⏳ Processing sites...
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

🔄 Detecting style, scroll animations, and decorative elements...
```

---

## STEP 2.5: Detect Design Style & Animation Libraries (NEW!)

```javascript
async function detectStyleAndAnimations() {
  return await mcp__chrome-devtools__evaluate_script({
    function: `() => {
      const result = {
        style: { detected: null, confidence: 0, characteristics: [] },
        animationLibraries: [],
        scrollAnimations: [],
        decorativeElements: []
      };

      // ========== DETECT ANIMATION LIBRARIES ==========

      // Check for GSAP
      if (window.gsap || window.TweenMax || window.TweenLite) {
        result.animationLibraries.push({
          name: 'GSAP',
          version: window.gsap?.version || 'unknown',
          detected: true
        });
      }

      // Check for ScrollTrigger
      if (window.ScrollTrigger) {
        result.animationLibraries.push({
          name: 'ScrollTrigger',
          version: window.ScrollTrigger?.version || 'unknown',
          detected: true,
          instances: document.querySelectorAll('[data-scroll], [data-gsap]').length
        });
      }

      // Check for Framer Motion (React)
      if (document.querySelector('[data-framer-appear-id], [data-projection-id]')) {
        result.animationLibraries.push({
          name: 'Framer Motion',
          detected: true
        });
      }

      // Check for Lottie
      if (window.lottie || document.querySelector('lottie-player, [data-lottie]')) {
        result.animationLibraries.push({
          name: 'Lottie',
          detected: true
        });
      }

      // Check for AOS (Animate on Scroll)
      if (window.AOS || document.querySelector('[data-aos]')) {
        result.animationLibraries.push({
          name: 'AOS',
          detected: true,
          instances: document.querySelectorAll('[data-aos]').length
        });
      }

      // ========== DETECT SCROLL ANIMATIONS ==========

      // Find elements with scroll-triggered classes or attributes
      const scrollElements = document.querySelectorAll(
        '[data-scroll], [data-aos], [data-gsap], [data-animate], ' +
        '[class*="scroll-"], [class*="animate-on-scroll"], ' +
        '[class*="fade-in"], [class*="slide-"]'
      );

      scrollElements.forEach(el => {
        const classes = el.className;
        const dataAttrs = Object.keys(el.dataset || {});

        result.scrollAnimations.push({
          type: detectScrollAnimationType(classes, dataAttrs),
          trigger: el.dataset.aos || el.dataset.scroll || 'scroll',
          element: el.tagName.toLowerCase() + (el.className ? '.' + el.className.split(' ')[0] : '')
        });
      });

      // Detect sticky/pinned sections (common in GSAP sites)
      document.querySelectorAll('[class*="sticky"], [class*="pinned"], [style*="position: sticky"]')
        .forEach(el => {
          result.scrollAnimations.push({
            type: 'sticky-section',
            element: el.tagName.toLowerCase()
          });
        });

      function detectScrollAnimationType(classes, dataAttrs) {
        if (classes.includes('stack') || dataAttrs.includes('stack')) return 'stacking-cards';
        if (classes.includes('parallax') || dataAttrs.includes('parallax')) return 'parallax';
        if (classes.includes('fade')) return 'fade-in';
        if (classes.includes('slide')) return 'slide-in';
        if (classes.includes('scale')) return 'scale-in';
        return 'custom-scroll';
      }

      // ========== DETECT DECORATIVE ELEMENTS ==========

      const svgs = document.querySelectorAll('svg:not([class*="icon"]):not([width="24"]):not([width="16"])');
      svgs.forEach(svg => {
        const viewBox = svg.getAttribute('viewBox');
        const width = parseInt(svg.getAttribute('width') || '0');
        const height = parseInt(svg.getAttribute('height') || '0');

        // Large SVGs are likely decorative
        if (width > 100 || height > 100 || (viewBox && parseInt(viewBox.split(' ')[2]) > 100)) {
          const paths = svg.querySelectorAll('path, circle, ellipse');
          const isBlob = Array.from(paths).some(p => {
            const d = p.getAttribute('d') || '';
            return d.includes('C') && d.length > 200; // Curved paths = likely blob
          });

          result.decorativeElements.push({
            type: isBlob ? 'blob' : 'svg-decoration',
            size: { width, height },
            colors: extractSvgColors(svg)
          });
        }
      });

      // Detect gradient backgrounds
      document.querySelectorAll('*').forEach(el => {
        const bg = window.getComputedStyle(el).backgroundImage;
        if (bg && bg.includes('gradient')) {
          result.decorativeElements.push({
            type: 'gradient',
            value: bg.substring(0, 100) + '...'
          });
        }
      });

      // Detect 3D elements
      document.querySelectorAll('[class*="3d"], [style*="perspective"], [style*="rotateX"], [style*="rotateY"]')
        .forEach(el => {
          result.decorativeElements.push({
            type: '3d-element',
            element: el.tagName.toLowerCase()
          });
        });

      function extractSvgColors(svg) {
        const colors = new Set();
        svg.querySelectorAll('[fill], [stroke]').forEach(el => {
          const fill = el.getAttribute('fill');
          const stroke = el.getAttribute('stroke');
          if (fill && fill !== 'none') colors.add(fill);
          if (stroke && stroke !== 'none') colors.add(stroke);
        });
        return Array.from(colors).slice(0, 5);
      }

      // ========== DETECT DESIGN STYLE ==========

      const allElements = document.querySelectorAll('*');
      const styleIndicators = {
        neoBrutalism: 0,
        minimalist: 0,
        glassmorphism: 0,
        neumorphism: 0,
        modernSaas: 0,
        playful: 0
      };

      allElements.forEach(el => {
        const s = window.getComputedStyle(el);

        // Neo-Brutalism indicators
        if (s.borderWidth && parseInt(s.borderWidth) >= 2) styleIndicators.neoBrutalism += 2;
        if (s.boxShadow && s.boxShadow.includes('0px 0px 0px') || !s.boxShadow.includes('blur')) {
          styleIndicators.neoBrutalism += 1; // Solid shadows
        }
        if (s.borderRadius && parseInt(s.borderRadius) >= 8 && parseInt(s.borderRadius) <= 16) {
          styleIndicators.neoBrutalism += 1;
        }

        // Minimalist indicators
        if (s.borderWidth === '0px' || s.borderWidth === '1px') styleIndicators.minimalist += 0.5;
        if (!s.boxShadow || s.boxShadow === 'none') styleIndicators.minimalist += 0.5;

        // Glassmorphism indicators
        if (s.backdropFilter && s.backdropFilter !== 'none') styleIndicators.glassmorphism += 3;
        if (s.backgroundColor && s.backgroundColor.includes('rgba') && parseFloat(s.backgroundColor.split(',')[3]) < 0.8) {
          styleIndicators.glassmorphism += 1;
        }

        // Neumorphism indicators
        if (s.boxShadow && s.boxShadow.includes('inset')) styleIndicators.neumorphism += 2;

        // Modern SaaS indicators
        if (s.boxShadow && s.boxShadow.includes('rgba') && s.boxShadow.includes('blur')) {
          styleIndicators.modernSaas += 1;
        }
        if (parseInt(s.borderRadius) >= 12) styleIndicators.modernSaas += 0.5;

        // Playful indicators
        if (s.borderRadius && parseInt(s.borderRadius) >= 24) styleIndicators.playful += 1;
        if (s.transform && s.transform !== 'none') styleIndicators.playful += 0.5;
      });

      // Determine style
      const maxStyle = Object.entries(styleIndicators)
        .sort((a, b) => b[1] - a[1])[0];

      const styleDescriptions = {
        neoBrutalism: {
          name: 'Neo-Brutalism',
          characteristics: ['Bold borders (2-4px)', 'Solid shadows (no blur)', 'High contrast', 'Chunky rounded corners'],
          feel: 'Bold, energetic, playful'
        },
        minimalist: {
          name: 'Minimalist',
          characteristics: ['Clean lines', 'Subtle or no shadows', 'Lots of whitespace', 'Simple typography'],
          feel: 'Clean, professional, trustworthy'
        },
        glassmorphism: {
          name: 'Glassmorphism',
          characteristics: ['Frosted glass effect', 'Backdrop blur', 'Semi-transparent backgrounds', 'Layered depth'],
          feel: 'Modern, premium, tech-forward'
        },
        neumorphism: {
          name: 'Neumorphism',
          characteristics: ['Soft inset shadows', 'Extruded elements', 'Monochromatic palette'],
          feel: 'Soft, touchable, futuristic'
        },
        modernSaas: {
          name: 'Modern SaaS',
          characteristics: ['Soft shadows with blur', 'Rounded corners', 'Gradient accents', 'Card-based layout'],
          feel: 'Professional, friendly, reliable'
        },
        playful: {
          name: 'Playful/Creative',
          characteristics: ['Large border radius', 'Animations', 'Bright colors', 'Asymmetric layouts'],
          feel: 'Fun, creative, approachable'
        }
      };

      result.style = {
        detected: styleDescriptions[maxStyle[0]].name,
        confidence: Math.min(Math.round((maxStyle[1] / 50) * 100), 100),
        characteristics: styleDescriptions[maxStyle[0]].characteristics,
        feel: styleDescriptions[maxStyle[0]].feel,
        scores: styleIndicators
      };

      return result;
    }`
  });
}

const styleData = await detectStyleAndAnimations();
```

**Report:**
```
✅ Style & Animations Detected!

🎨 Design Style: ${styleData.style.detected} (${styleData.style.confidence}% confidence)
   Characteristics: ${styleData.style.characteristics.join(', ')}
   Feel: ${styleData.style.feel}

📚 Animation Libraries:
${styleData.animationLibraries.map(lib => `   ✅ ${lib.name} ${lib.version || ''}`).join('\n') || '   (none detected)'}

🎬 Scroll Animations: ${styleData.scrollAnimations.length} detected
${styleData.scrollAnimations.slice(0, 5).map(a => `   - ${a.type}`).join('\n')}

🖼️ Decorative Elements: ${styleData.decorativeElements.length} found
${styleData.decorativeElements.slice(0, 5).map(d => `   - ${d.type}`).join('\n')}

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
await Bash: mkdir -p .claude/extractions/screenshots/${siteName}

// Try fullpage
try {
  await mcp__chrome-devtools__take_screenshot({
    fullPage: true,
    format: 'png',
    filePath: `.claude/extractions/screenshots/${siteName}/full-page.png`
  });
} catch {
  // Fallback: viewport only
  await mcp__chrome-devtools__take_screenshot({
    fullPage: false,
    format: 'png',
    filePath: `.claude/extractions/screenshots/${siteName}/viewport.png`
  });
}
```

---

## STEP 5: Generate Site JSON (Lean Format)

Generate a lean JSON file per site (~500 tokens):

```javascript
const siteData = {
  meta: {
    site_name: siteName,
    url: url,
    extracted_at: new Date().toISOString(),
    extractor_version: '3.0.0'
  },

  // ========== STYLE (from STEP 2.5) ==========
  style: {
    detected: styleData.style.detected,
    confidence: styleData.style.confidence,
    characteristics: styleData.style.characteristics,
    feel: styleData.style.feel
  },

  // ========== ANIMATION LIBRARIES ==========
  animation_libraries: styleData.animationLibraries,

  // ========== SCROLL ANIMATIONS ==========
  scroll_animations: {
    detected: styleData.scrollAnimations.length > 0,
    patterns: [...new Set(styleData.scrollAnimations.map(a => a.type))],
    count: styleData.scrollAnimations.length
  },

  // ========== DECORATIVE ELEMENTS ==========
  decorative_elements: {
    types: [...new Set(styleData.decorativeElements.map(d => d.type))],
    has_blobs: styleData.decorativeElements.some(d => d.type === 'blob'),
    has_gradients: styleData.decorativeElements.some(d => d.type === 'gradient'),
    has_3d: styleData.decorativeElements.some(d => d.type === '3d-element')
  },

  // ========== COLORS (Simplified) ==========
  colors: {
    primary: colors.backgrounds.slice(0, 3).map(c => c.hex),
    text: colors.texts.slice(0, 3).map(c => c.hex),
    accent: colors.borders.slice(0, 2).map(c => c.hex)
  },

  // ========== TYPOGRAPHY (Simplified) ==========
  typography: {
    fonts: typography.allFonts.slice(0, 3),
    weights: typography.allWeights,
    heading_style: typography.h1[0] ? {
      fontSize: typography.h1[0].fontSize,
      fontWeight: typography.h1[0].fontWeight
    } : null
  },

  // ========== COMPONENT ANIMATIONS ==========
  component_animations: {
    button_hover: componentAnimations['button-0']?.description || 'none',
    card_hover: componentAnimations['card-0']?.description || 'none',
    input_focus: componentAnimations['input-0']?.description || 'none'
  },

  // ========== SPACING ==========
  spacing: {
    grid_base: spacing.detectedGrid,
    common: spacing.commonValues.slice(0, 8)
  },

  // ========== SHADOWS ==========
  shadows: shadows.shadows.slice(0, 5),

  // ========== BORDER RADIUS ==========
  border_radius: shadows.borderRadii.slice(0, 5)
};

// Write site-specific JSON
Write(`.claude/extractions/${siteName}.json`, JSON.stringify(siteData, null, 2));
```

**Report:**
```
✅ Site Data Extracted: ${siteName}

🎨 Style: ${siteData.style.detected} (${siteData.style.confidence}% confidence)
📚 Animation Libraries: ${siteData.animation_libraries.map(l => l.name).join(', ') || 'none'}
🎬 Scroll Animations: ${siteData.scroll_animations.patterns.join(', ') || 'none'}
🖼️ Decorative: ${siteData.decorative_elements.types.join(', ') || 'none'}

📁 Saved: .claude/extractions/${siteName}.json
```

---

## STEP 6: Merge Multiple Sites (If Multi-URL)

If extracting from multiple sites, merge insights:

```javascript
// Only run if multiple sites
if (sites.length > 1) {
  const allSiteData = sites.map(site => {
    const data = JSON.parse(Read(`.claude/extractions/${site.siteName}.json`));
    return { siteName: site.siteName, ...data };
  });

  const mergedInsights = {
    meta: {
      generated_at: new Date().toISOString(),
      sites_count: sites.length,
      sites: sites.map(s => s.siteName)
    },

    // ========== STYLES FROM ALL SITES ==========
    styles: allSiteData.map(site => ({
      site: site.siteName,
      style: site.style.detected,
      confidence: site.style.confidence,
      characteristics: site.style.characteristics,
      feel: site.style.feel
    })),

    // ========== ANIMATION LIBRARIES (Combined) ==========
    animation_libraries: [...new Set(
      allSiteData.flatMap(site => site.animation_libraries.map(l => l.name))
    )].map(name => {
      const sources = allSiteData
        .filter(site => site.animation_libraries.some(l => l.name === name))
        .map(site => site.siteName);
      return { name, sources };
    }),

    // ========== SCROLL ANIMATIONS (Combined) ==========
    scroll_animations: [...new Set(
      allSiteData.flatMap(site => site.scroll_animations.patterns)
    )].map(pattern => {
      const sources = allSiteData
        .filter(site => site.scroll_animations.patterns.includes(pattern))
        .map(site => site.siteName);
      return { pattern, sources };
    }),

    // ========== DECORATIVE ELEMENTS (Combined) ==========
    decorative_elements: [...new Set(
      allSiteData.flatMap(site => site.decorative_elements.types)
    )].map(type => {
      const sources = allSiteData
        .filter(site => site.decorative_elements.types.includes(type))
        .map(site => site.siteName);
      return { type, sources };
    }),

    // ========== COMPONENT ANIMATIONS (Combined) ==========
    component_animations: {
      button_hover: allSiteData.map(site => ({
        site: site.siteName,
        animation: site.component_animations.button_hover
      })),
      card_hover: allSiteData.map(site => ({
        site: site.siteName,
        animation: site.component_animations.card_hover
      }))
    },

    // ========== COLORS (All Options) ==========
    color_palettes: allSiteData.map(site => ({
      site: site.siteName,
      primary: site.colors.primary,
      text: site.colors.text
    })),

    // ========== TYPOGRAPHY (All Options) ==========
    typography_options: allSiteData.map(site => ({
      site: site.siteName,
      fonts: site.typography.fonts
    }))
  };

  Write('.claude/extractions/merged-insights.json', JSON.stringify(mergedInsights, null, 2));
}
```

**Report (Multi-Site):**
```
✅ Merged Insights Generated!

📊 Combined from ${sites.length} sites:
${sites.map(s => `   - ${s.siteName}`).join('\n')}

🎨 Styles found:
${mergedInsights.styles.map(s => `   - ${s.style} (${s.site})`).join('\n')}

📚 Animation Libraries:
${mergedInsights.animation_libraries.map(l => `   - ${l.name} (from: ${l.sources.join(', ')})`).join('\n')}

🎬 Scroll Patterns:
${mergedInsights.scroll_animations.map(a => `   - ${a.pattern} (from: ${a.sources.join(', ')})`).join('\n')}

📁 Saved: .claude/extractions/merged-insights.json
```

---

## STEP 7: Final Report

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ EXTRACTION COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Sites Extracted: ${sites.length}
${sites.map(s => `
┌─ ${s.siteName} ─────────────────────────────────────────┐
│ 🎨 Style: ${siteData.style.detected} (${siteData.style.confidence}%)
│ 📚 Libraries: ${siteData.animation_libraries.map(l => l.name).join(', ') || 'none'}
│ 🎬 Scroll: ${siteData.scroll_animations.patterns.join(', ') || 'none'}
│ 🖼️ Decorative: ${siteData.decorative_elements.types.join(', ') || 'none'}
│ 📁 File: .claude/extractions/${s.siteName}.json
└─────────────────────────────────────────────────────────┘
`).join('')}

${sites.length > 1 ? `
📋 Merged Insights: .claude/extractions/merged-insights.json
   → Use this in /designsetup to pick features from each site
` : ''}

📸 Screenshots: .claude/extractions/screenshots/
   ${sites.map(s => `- ${s.siteName}/full-page.png`).join('\n   ')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 Next Steps:

1. Extract more references (optional):
   /extract https://another-site.com

2. Generate design system:
   /designsetup

   → Will read: .claude/extractions/*.json
   → Will ask you to pick: style, animations, theme
   → Will output: design-system/tokens.json

3. Review extracted data:
   Read .claude/extractions/${sites[0].siteName}.json

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
