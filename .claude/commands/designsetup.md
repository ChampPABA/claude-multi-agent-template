# /designsetup - Auto-Generate Design System from Live Website

You are an expert UX/UI and systems designer with experience at FANG-level companies.

Your task is to generate a comprehensive `STYLE_GUIDE.md` file using **Chrome DevTools MCP** to extract accurate computed styles from live websites, local HTML files, or localhost.

---

## 📖 Usage

**Three modes of operation:**

```bash
# Mode 1: Live Website (Reference Design)
/designsetup https://motherduck.com

# Mode 1b: Local HTML File
/designsetup E:/designs/reference.html
/designsetup /Users/me/designs/index.html

# Mode 2: Localhost (Brownfield - Reverse Engineering)
/designsetup localhost:3000
/designsetup http://localhost:5173

# Mode 3: Interactive (Greenfield - AI-Generated)
/designsetup
```

**Detection Logic:**
- If starts with `https://` or `http://` → **Path 1** (Live Website)
- If file path (starts with `/`, `C:/`, `E:/`) → **Path 1** (Local HTML File, convert to `file:///`)
- If contains `localhost` → **Path 2** (Localhost)
- If NO argument → **Path 3** (Interactive Greenfield)

---

## 🎯 Mission

Generate a production-ready style guide at: `design-system/STYLE_GUIDE.md`

**Key Principles:**
1. **CSS First**: Extract CSS via DevTools BEFORE screenshot analysis
2. **Screenshot Validates**: Use screenshot to validate CSS findings and identify design style
3. **Data-Driven**: Every color, font, spacing from computed styles (98% accuracy)
4. **LLM Analyzes**: AI determines design style from screenshot (no user questions for Path 1)
5. **Comprehensive**: All 17 sections, 1500-2000 lines

**Critical Flow:**
```
DevTools (CSS data) → Screenshot (validate + style detection) → Pondering → Generate
```

---

## 🔍 STEP 0: Detect Mode from Input

**Parse user input:**

```javascript
const input = userInput.trim();

if (input.startsWith('https://') || input.startsWith('http://')) {
  // Path 1: Live Website
  mode = 'live-website';
  url = input;
} else if (input.match(/^[A-Z]:/i) || input.startsWith('/')) {
  // Path 1: Local HTML File
  mode = 'local-html';
  url = input.startsWith('file:///') ? input : 'file:///' + input.replace(/\\/g, '/');
} else if (input.includes('localhost') || input.startsWith('http://localhost')) {
  // Path 2: Localhost (Brownfield)
  mode = 'localhost';
  url = input.startsWith('http') ? input : `http://${input}`;
} else if (input === '' || input === '/designsetup') {
  // Path 3: Interactive Greenfield
  mode = 'interactive';
  url = null;
} else {
  error('Invalid input. Use: https://, file path, localhost:PORT, or no argument');
}
```

**Report:**
```
🔍 Mode Detected: [mode]
📍 URL: [url or "Interactive mode"]

🚀 Starting design extraction...
```

---

## 📋 PATH 1: Reference Design Analysis (Chrome DevTools)

**Use Chrome DevTools MCP to extract CSS from live website or local HTML file.**

---

### Step 1: Navigate to URL

```javascript
// Open page with Chrome DevTools
mcp__chrome-devtools__navigate_page({
  url: normalizedUrl  // e.g., "https://motherduck.com" or "file:///E:/designs/index.html"
})

// Wait for load
try {
  const snapshot = mcp__chrome-devtools__take_snapshot({ verbose: false });
  const mainText = detectMainContent(snapshot);

  mcp__chrome-devtools__wait_for({
    text: mainText,
    timeout: 15000
  });
} catch {
  await sleep(5000); // Fallback
}
```

**Report:**
```
🎨 Design Extraction Started

🌐 Opening: [URL]
⏳ Waiting for page load...
✅ Page loaded successfully

🔄 Extracting CSS data (Source of Truth)...
```

---

### Step 2: Extract CSS Data (Source of Truth)

**Run 5-6 `evaluate_script` calls to extract ALL CSS data FIRST (before screenshot):**

#### Call #1: All Unique Colors

```javascript
mcp__chrome-devtools__evaluate_script({
  function: `() => {
    const allElements = document.querySelectorAll('*');
    const bgColors = new Set();
    const textColors = new Set();
    const borderColors = new Set();

    allElements.forEach(el => {
      const s = window.getComputedStyle(el);
      if (s.backgroundColor && s.backgroundColor !== 'rgba(0, 0, 0, 0)') {
        bgColors.add(s.backgroundColor);
      }
      if (s.color) {
        textColors.add(s.color);
      }
      if (s.borderColor && s.borderColor !== 'rgba(0, 0, 0, 0)') {
        borderColors.add(s.borderColor);
      }
    });

    return {
      backgrounds: Array.from(bgColors).slice(0, 30),
      texts: Array.from(textColors).slice(0, 20),
      borders: Array.from(borderColors).slice(0, 15)
    };
  }`
})
```

#### Call #2: All Effects (shadows, radius, borders)

```javascript
mcp__chrome-devtools__evaluate_script({
  function: `() => {
    const allElements = document.querySelectorAll('*');
    const shadows = new Set();
    const borderRadii = new Set();
    const borderWidths = new Set();

    allElements.forEach(el => {
      const s = window.getComputedStyle(el);
      if (s.boxShadow && s.boxShadow !== 'none') {
        shadows.add(s.boxShadow);
      }
      if (s.borderRadius && s.borderRadius !== '0px') {
        borderRadii.add(s.borderRadius);
      }
      if (s.borderWidth && s.borderWidth !== '0px') {
        borderWidths.add(s.borderWidth);
      }
    });

    return {
      shadows: Array.from(shadows).slice(0, 15),
      borderRadii: Array.from(borderRadii).slice(0, 15),
      borderWidths: Array.from(borderWidths).slice(0, 10)
    };
  }`
})
```

#### Call #3: Typography Details

```javascript
mcp__chrome-devtools__evaluate_script({
  function: `() => {
    return {
      h1: Array.from(document.querySelectorAll('h1')).slice(0, 3).map(h => {
        const s = window.getComputedStyle(h);
        return {
          text: h.textContent.trim().substring(0, 50),
          fontSize: s.fontSize,
          fontWeight: s.fontWeight,
          fontFamily: s.fontFamily,
          lineHeight: s.lineHeight,
          letterSpacing: s.letterSpacing,
          textTransform: s.textTransform,
          color: s.color
        };
      }),
      h2: Array.from(document.querySelectorAll('h2')).slice(0, 3).map(h => {
        const s = window.getComputedStyle(h);
        return {
          text: h.textContent.trim().substring(0, 50),
          fontSize: s.fontSize,
          fontWeight: s.fontWeight,
          fontFamily: s.fontFamily,
          textTransform: s.textTransform,
          color: s.color
        };
      }),
      body: Array.from(document.querySelectorAll('p')).slice(0, 5).map(p => {
        const s = window.getComputedStyle(p);
        return {
          fontSize: s.fontSize,
          lineHeight: s.lineHeight,
          fontFamily: s.fontFamily,
          color: s.color
        };
      })
    };
  }`
})
```

#### Call #4: Primary CTA Buttons

```javascript
mcp__chrome-devtools__evaluate_script({
  function: `() => {
    const ctaButtons = Array.from(document.querySelectorAll('a, button'))
      .filter(el => {
        const text = el.textContent.trim().toUpperCase();
        return text.includes('FREE') || text.includes('START') ||
               text.includes('TRY') || text.includes('DEMO') ||
               text.includes('SIGN UP') || text.includes('GET') ||
               text.includes('BUY') || text.includes('LEARN');
      });

    return ctaButtons.slice(0, 5).map(btn => {
      const s = window.getComputedStyle(btn);
      return {
        text: btn.textContent.trim(),
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
        boxShadow: s.boxShadow
      };
    });
  }`
})
```

#### Call #5: Card/Container Styles

```javascript
mcp__chrome-devtools__evaluate_script({
  function: `() => {
    const selectors = [
      '[class*="card"]', '[class*="Card"]',
      '[class*="container"]', '[class*="Container"]',
      '[class*="box"]', '[class*="Box"]'
    ];

    const cards = Array.from(document.querySelectorAll(selectors.join(', ')))
      .slice(0, 10);

    return cards.map(card => {
      const s = window.getComputedStyle(card);
      return {
        className: card.className,
        backgroundColor: s.backgroundColor,
        padding: s.padding,
        border: s.border,
        borderRadius: s.borderRadius,
        boxShadow: s.boxShadow
      };
    });
  }`
})
```

#### Call #6: Body & Background

```javascript
mcp__chrome-devtools__evaluate_script({
  function: `() => {
    const body = document.body;
    const bodyStyles = window.getComputedStyle(body);

    return {
      body: {
        backgroundColor: bodyStyles.backgroundColor,
        color: bodyStyles.color,
        fontFamily: bodyStyles.fontFamily,
        fontSize: bodyStyles.fontSize,
        lineHeight: bodyStyles.lineHeight
      }
    };
  }`
})
```

**Report:**
```
✅ CSS Data Extracted!

📊 Summary:
   - Colors: [count] unique colors
     • Backgrounds: [count] colors
     • Text: [count] colors
     • Borders: [count] colors
   - Typography: [count] font families, [count] weights, [count] sizes
   - Shadows: [count] unique shadows
   - Border Radius: [count] unique values
   - Border Width: [count] unique values
   - Buttons: [count] CTA styles extracted
   - Cards: [count] container styles extracted

🔄 Proceeding to screenshot capture...
```

---

### Step 3: Take Screenshot & Save to Disk

**Save screenshots to disk to avoid size limits:**

```javascript
// Create temp directory
Bash: mkdir -p design-system/.temp

// Take fullpage screenshot (or element-based if fullpage times out)
try {
  mcp__chrome-devtools__take_screenshot({
    fullPage: true,
    format: "png",
    filePath: "design-system/.temp/screenshot-fullpage.png"
  });
} catch {
  // Fallback: viewport only
  mcp__chrome-devtools__take_screenshot({
    fullPage: false,
    format: "png",
    filePath: "design-system/.temp/screenshot-viewport.png"
  });
}
```

**Report:**
```
✅ Screenshot captured

📸 Files created:
   - design-system/.temp/screenshot-fullpage.png [✓ / fallback: viewport]

🔄 Reading screenshot for visual analysis...
```

---

### Step 4: Read Screenshot & Analyze Design Style

**CRITICAL: Read the screenshot file using Read tool:**

```javascript
Read({
  file_path: "design-system/.temp/screenshot-fullpage.png"
})
// OR
Read({
  file_path: "design-system/.temp/screenshot-viewport.png"
})
```

**Analyze and determine (LLM does this automatically - NO user questions):**

1. **Design Style Classification:**
   - **Neo-Brutalism**: Hard shadows (no blur), minimal radius (2px), bold borders (2px), monospace fonts, bold colors
   - **Neumorphic**: Soft shadows (blur 10px+), medium radius (8-12px), subtle colors, depth illusion
   - **Minimalist**: White space, thin borders (1px), subtle shadows, clean sans-serif, muted colors
   - **Modern SaaS**: Rounded (8-16px), soft shadows, gradient accents, sans-serif, vibrant
   - **Glassmorphism**: Blur effects, transparency (opacity 70%), layered, frosted glass
   - **Retro Computing**: Monospace fonts, CRT colors (yellow/cyan), pixelated, nostalgic

2. **Visual Evidence:**
   - Shadow style: Hard edges (no blur) or soft blur?
   - Corner style: Sharp (0-2px), rounded (6-8px), or very rounded (12px+)?
   - Color approach: Bold blocks or subtle gradients?
   - Typography: Sans-serif, monospace, or serif?
   - Border style: Thick (2px+) or thin (1px)?

3. **Design Philosophy:**
   - What makes it visually appealing?
   - What emotions does it evoke? (trust, speed, playfulness, technical, friendly)
   - What principles guide it? (clarity, boldness, simplicity, elegance)
   - How does it differ from typical sites in this category?

4. **User Experience Goals:**
   - First impression? (different, familiar, innovative, classic, bold, subtle)
   - During use? (fast, delightful, efficient, calming, energetic)
   - Long-term? (memorable, trustworthy, professional, playful)

**Report:**
```
✅ Visual Analysis Complete!

🎨 Design Style Detected: [Neo-Brutalism / Neumorphic / Minimalist / Modern SaaS / etc.]

📐 Visual Evidence:
   - Shadows: [Hard edges, no blur / Soft blur 10px / None]
   - Corners: [Sharp 2px / Rounded 8px / Very rounded 16px]
   - Colors: [Bold blocks / Subtle gradients / Muted pastels]
   - Typography: [Monospace / Sans-serif / Serif]
   - Borders: [Thick 2px / Thin 1px / None]

🎯 Design Philosophy:
   - Core: [e.g., "Honest materials, bold contrasts, functional-first"]
   - Mood: [e.g., "Confident, technical, playful"]
   - Differentiator: [e.g., "Rejects soft/rounded trends, embraces brutalism"]

🔄 Proceeding to pondering phase...
```

---

### Step 5: Pondering Phase (Mandatory)

**Wrap analysis in `<pondering>` tags with this EXACT structure:**

```xml
<pondering>
# Design Analysis - [Site Name]

## Part 1: CSS Data Extracted (Source of Truth)

### Colors Found:
[List ALL extracted colors with rgb/hex values]

**Analysis:**
- Primary: [color] ([psychology: e.g., energy, trust, etc.])
- Secondary: [color] ([usage context])
- Background: [color] ([reasoning: softer than white, warm, etc.])
- Foreground: [color] ([contrast ratio: e.g., 12:1 AAA])
- [... all other colors ...]

### Typography Found:
[List ALL extracted font data]

**Analysis:**
- Font Family: [name] ([why? e.g., monospace = technical/retro])
- Weight Usage: [e.g., "Only 400 used - hierarchy through SIZE not weight"]
- Size Scale: [list all sizes found]
- Line Height: [tight/normal/relaxed - e.g., "1.2 = compact, functional"]
- Letter Spacing: [values found - e.g., "1.44px on H1 = strong separation"]

### Effects Found:
[List ALL shadows, border-radius, border-width]

**Analysis:**
- Shadow Style: [e.g., "-12px 12px 0 0 = HARD SHADOW, no blur, offset bottom-right"]
- Border Radius: [e.g., "2px everywhere = minimal, anti-smooth, brutalist"]
- Border Width: [e.g., "2px consistent = bold definition"]

### Button Styles:
[Exact extracted values]
- Padding: [e.g., "11.5px 18px"]
- Border: [e.g., "2px solid #383838"]
- Background: [colors]
- Shadow: [value or "none"]

### Card Styles:
[Exact extracted values]

---

## Part 2: Visual Analysis (from Screenshot)

### Design Style Identified: **[Neo-Brutalism / Neumorphic / etc.]**

**Visual Evidence:**
1. **[Observation 1]:**
   - [Detailed description]
   - [Why it matters for classification]

2. **[Observation 2]:**
   - [Detailed description]
   - [Why it matters]

3. **[Observation 3]:**
   - [Detailed description]
   - [Why it matters]

### What Makes It Appealing?

1. **[Quality 1 - e.g., Memorable & Unique]:**
   - [Why it's appealing]
   - [How it achieves this]

2. **[Quality 2 - e.g., Confident & Bold]:**
   - [Why it's appealing]
   - [How it achieves this]

### Design Philosophy Detected:

**Core Principles:**
1. **[Principle 1]** - [Description]
2. **[Principle 2]** - [Description]
3. **[Principle 3]** - [Description]

**User Experience Goals:**
- First impression: [description]
- During use: [description]
- Long-term: [description]

---

## Part 3: Validation (CSS matches Visual?)

| Aspect | CSS Data | Visual Shows | Match? |
|--------|----------|--------------|--------|
| Shadows | [exact value] | [visual description] | ✅/⚠️ |
| Radius | [exact value] | [visual description] | ✅/⚠️ |
| Font | [exact value] | [visual description] | ✅/⚠️ |
| Weight | [exact value] | [visual description] | ✅/⚠️ |
| Colors | [exact values] | [visual description] | ✅/⚠️ |
| Borders | [exact value] | [visual description] | ✅/⚠️ |

**Validation Result:** [CSS perfectly matches / Minor discrepancies / Major differences]

---

## Part 4: Key Differentiators

**[Site Name] vs. Typical [Industry] Sites:**
- ❌ [Common pattern] → ✅ [This site's approach]
- ❌ [Common pattern] → ✅ [This site's approach]
- ❌ [Common pattern] → ✅ [This site's approach]

**Why This Works:**
- [Reason 1: competitive advantage]
- [Reason 2: user psychology]
- [Reason 3: technical execution]

---

## Conclusion: Generate [Design Style] Style Guide

**Key Features to Include:**
1. [Feature 1] - [exact CSS value]
2. [Feature 2] - [exact CSS value]
3. [Feature 3] - [exact CSS value]
4. [... all critical features with exact values ...]

**Design Philosophy Section:**
- [Style name] aesthetic (e.g., Neo-Brutalism)
- [Core principles from Part 2]
- [UX goals]

**Critical Rules:**
- ❌ NO [anti-pattern] (e.g., "NO soft shadows - blur must be 0")
- ❌ NO [anti-pattern] (e.g., "NO rounded corners - use 2px only")
- ✅ YES to [best practice] (e.g., "YES to hard shadows")
- ✅ YES to [best practice] (e.g., "YES to monospace font")
</pondering>
```

**Report:**
```
✅ Pondering Complete!

🧠 Analysis Summary:
   - CSS Data: [count] data points extracted
   - Design Style: [style name] ✓ IDENTIFIED
   - Validation: CSS ↔ Visual alignment ✓ [Perfect / Good / Needs adjustment]
   - Philosophy: [3 core principles identified]

🔄 Proceeding to STYLE_GUIDE.md generation...
```

---

### Step 6: Generate STYLE_GUIDE.md

**Generate comprehensive 17-section guide (1500-2000 lines) using:**
- CSS data as PRIMARY source (exact values)
- Screenshot analysis for design philosophy & style classification
- Pondering conclusions for structure & critical rules

**Output file:** `design-system/STYLE_GUIDE.md`

**All 17 sections must include:**
1. Overview (detected style, tech stack)
2. Design Philosophy (from pondering Part 2)
3. Color Palette (from CSS extraction, exact HEX values)
4. Typography (from CSS extraction, exact sizes/weights)
5. Spacing System (detected from padding/margin patterns)
6. Component Styles (Button, Card, Input - from extraction)
7. Shadows & Elevation (exact CSS values)
8. Animations & Transitions (extracted transition values)
9. Border Styles (extracted border-width values)
10. Border Radius (extracted values)
11. Opacity & Transparency (if used)
12. Z-Index Layers (standard scale)
13. Responsive Breakpoints (standard or extracted)
14. CSS Variables / Tailwind Theme (design tokens in JSON)
15. Layout Patterns (container, grid examples)
16. Example Component Reference (React + Tailwind code)
17. Additional Sections (accessibility, best practices, critical rules)

**Report:**
```
✅ Design Setup Complete!

📁 Generated: design-system/STYLE_GUIDE.md ([line count] lines)

📊 Summary:
   - Design Style: [Neo-Brutalism / Neumorphic / etc.]
   - Colors: [count] extracted (HEX values) ✓
   - Typography: [font name], [count] weights, [count] sizes ✓
   - Shadows: [count] unique values ✓
   - Border Radius: [primary value - e.g., 2px / 8px] ✓
   - Components: Button, Card, Input, Badge styles ✓
   - All 17 sections: Complete ✓

🎯 Key Features:
   [Feature 1: e.g., "Hard shadows (-12px 12px 0 0)"]
   [Feature 2: e.g., "Minimal radius (2px)"]
   [Feature 3: e.g., "Monospace font (Aeonik Mono)"]

🔍 Extraction Method:
   ✅ Chrome DevTools MCP (computed styles)
   ✅ Screenshot analyzed (design style detection)
   ✅ CSS → Visual validation ✓
   ✅ Data-driven (no guessing)

💡 Next Steps:
   1. Review: design-system/STYLE_GUIDE.md
   2. Run /psetup (if needed)
   3. Start development: /csetup {change-id}
```

---

## 📋 PATH 2: Localhost Analysis (Brownfield)

**Same as Path 1 (Steps 1-6) + codebase inconsistency detection:**

1. Navigate to localhost URL
2. Extract CSS data (6 calls)
3. Take screenshot
4. Read & analyze screenshot
5. Pondering phase
6. Generate STYLE_GUIDE.md

**Additional: Codebase Scan**

```bash
# Detect inconsistencies
Glob: src/**/*.{tsx,jsx,vue,svelte}
Grep: className= patterns

# Find:
- Duplicate components (Button variants)
- Hardcoded colors vs theme
- Inconsistent spacing (not on 8px grid)
- Unused theme colors
```

**Include in guide:**
```markdown
## ⚠️ Current State Analysis (Brownfield)

### Inconsistencies Found:
1. Duplicate Button styles (4 variants) → Consolidate
2. Hardcoded colors (8 instances) → Use theme
3. Inconsistent spacing (not on 8px grid) → Standardize
```

---

## 📋 PATH 3: Interactive Greenfield

**🚨 ONLY Path 3 uses AskUserQuestion tool! 🚨**

### Step 1: Ask User Questions

Use `AskUserQuestion` tool with 4 questions:

1. **Application Type** (header: "App Type")
   - Options: SaaS Dashboard, Marketing Website, E-commerce Store, Admin Panel

2. **Design Style** (header: "Design Style")
   - Options: Minimalist, Neo-Brutalism, Modern Professional, Glassmorphism

3. **Primary Color** (header: "Primary Color")
   - Options: Blue, Green, Purple, Orange

4. **CSS Stack** (header: "CSS Stack")
   - Options: Tailwind CSS, styled-components, CSS Modules

### Step 2: Generate AI-Based Style Guide

Based on user answers, generate modern best-practice guide:

- Color palette: Primary + shades + grayscale + semantic
- Type scale: Varies by app type (SaaS: 14px, Marketing: 16px)
- Spacing: 8px grid (0.5rem to 4rem)
- Components: Tailored to design style
- Code examples: Match CSS stack

**Report:**
```
✅ Style Guide Generated (Greenfield)!

📁 design-system/STYLE_GUIDE.md (1,650 lines)

📊 Configuration:
   - Application: [user choice]
   - Style: [user choice]
   - Primary: [user choice]
   - Stack: [user choice]

🎨 Features: 17 sections complete ✓
```

---

## 🎯 Success Criteria

Verify:

1. ✅ CSS extracted BEFORE screenshot
2. ✅ Screenshot analyzed for design style (LLM, not user)
3. ✅ Pondering has 4 parts (CSS → Visual → Validation → Conclusion)
4. ✅ STYLE_GUIDE.md has all 17 sections
5. ✅ Exact CSS values used (not approximations)
6. ✅ Design philosophy matches visual analysis
7. ✅ Critical rules included (DO's and DON'Ts)

---

**Now execute the detected path.**
