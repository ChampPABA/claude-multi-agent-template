# /designsetup - Interactive Design System Setup

You are a senior design systems architect with experience at FANG-level companies.

Your task is to guide user through an **interactive design system setup** with verbose options, theme selection, and decorative direction.

---

## 📖 Usage

```bash
/designsetup [@context-files...]

Arguments:
  @context-files    Optional. Context files (prd.md, project.md, brief.md, etc.)

Examples:
  /designsetup @prd.md @project.md
  /designsetup @docs/brief.md @docs/requirements.md
  /designsetup  # No context (interactive fallback)
```

---

## 🎯 Mission

Generate design system files:
- `design-system/data.yaml` (~300 lines) - **PRIMARY: Agent reads this** (merged tokens + psychology)
- `design-system/README.md` (~100 lines) - **Human-readable summary**

**Process:**
1. Load all extracted data from `design-system/extracted/*/data.yaml`
2. Present verbose style options with Match scores
3. **Interactive Loop** (max 3 rounds): Present → Feedback → Adjust
4. Theme selection + Decorative direction recommendation
5. Merge psychology + tokens → Generate data.yaml + README.md

**Key Principles:**
1. **Interactive Loop**: User must accept 100% before generating
2. **Verbose Options**: Show full details (characteristics, feel, examples)
3. **Theme + Decorations**: Agent recommends based on project context
4. **Psychology Preserved**: Emotions, target audience, why it works

---

## STEP 0: Discovery & Validation

```javascript
// 1. Find extracted sites from design-system/extracted/*/data.yaml
const extractedDirs = glob('design-system/extracted/*/data.yaml');

if (extractedDirs.length === 0) {
  return error(`
    ❌ No extracted data found

    Please extract at least 1 site first:
      /extract https://motherduck.com
      /extract https://linear.app

    Then run: /designsetup @prd.md @project.md
  `);
}

// 2. Load all extracted site data (YAML format with psychology)
const extractedData = {};
for (const file of extractedDirs) {
  const siteName = path.basename(path.dirname(file)); // Get folder name
  extractedData[siteName] = YAML.parse(Read(file));
}

// 4. Load context files
const contextArgs = args.filter(arg => arg.startsWith('@'));
const contexts = {};

if (contextArgs.length > 0) {
  for (const arg of contextArgs) {
    const filePath = arg.substring(1); // Remove @

    if (!exists(filePath)) {
      warn(`Context file not found: ${filePath} (skipping)`);
      continue;
    }

    const fileName = path.basename(filePath);
    contexts[fileName] = Read(filePath);
  }
}
```

**Report:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎨 Design Setup Started
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Extracted Sites: ${Object.keys(extractedData).length}
${Object.entries(extractedData).map(([site, data]) =>
  `   - ${site}: ${data.style.detected} (${data.style.confidence}% confidence)`
).join('\n')}

${mergedInsights ? `📋 Merged Insights: Available (${mergedInsights.meta.sites_count} sites)` : ''}

📁 Context Files: ${Object.keys(contexts).length || 'None (will use interactive mode)'}
${Object.keys(contexts).length > 0 ? Object.keys(contexts).map(c => `   - ${c}`).join('\n') : ''}

🔄 Analyzing context...
```

---

## STEP 1: Context Analysis

```javascript
let contextAnalysis;

if (Object.keys(contexts).length > 0) {
  // AI analyzes context files
  const analysisPrompt = `
You are analyzing project context to recommend design directions.

Context Files:
${Object.entries(contexts).map(([name, content]) => `
## ${name}
${content.substring(0, 2000)}  // First 2000 chars
`).join('\n')}

Task: Identify project characteristics and return JSON.

Return JSON:
{
  "has_context": true,
  "target_audience": {
    "age_range": "18-25" | "26-40" | "40+" | "mixed",
    "demographics": "string",
    "tech_savvy": "low" | "medium" | "high",
    "description": "string"
  },
  "brand_personality": ["bold" | "professional" | "playful" | "minimal" | "technical", ...],
  "product_type": "SaaS" | "E-commerce" | "Marketing" | "Internal Tool" | "Other",
  "market_position": "string (differentiation strategy)",
  "design_preferences": {
    "mentioned": boolean,
    "details": "string (if any design preferences mentioned)"
  },
  "business_goals": ["string", ...]
}

If context is insufficient or unclear, set "has_context": false.
`;

  contextAnalysis = await LLM({
    prompt: analysisPrompt,
    response_format: 'json'
  });

} else {
  contextAnalysis = { has_context: false };
}

// If no context, ask user
if (!contextAnalysis.has_context) {
  const userInput = await AskUserQuestion({
    questions: [
      {
        question: "What type of product are you building?",
        header: "Product Type",
        multiSelect: false,
        options: [
          { label: "SaaS Dashboard", description: "Business software, data tools, analytics" },
          { label: "E-commerce", description: "Online store, marketplace, shopping" },
          { label: "Marketing Site", description: "Landing pages, content, blog" },
          { label: "Internal Tool", description: "Admin panels, workflows, dashboards" }
        ]
      },
      {
        question: "Who is your target audience?",
        header: "Audience",
        multiSelect: false,
        options: [
          { label: "Gen Z (18-25)", description: "Young, tech-savvy, bold preferences" },
          { label: "Millennials (26-40)", description: "Professional, value-driven, modern" },
          { label: "Enterprise (40+)", description: "Conservative, trust-focused, established" },
          { label: "Developers", description: "Technical, efficiency-focused, minimal" }
        ]
      },
      {
        question: "What brand personality do you want?",
        header: "Brand",
        multiSelect: true,
        options: [
          { label: "Bold", description: "Stand out, memorable, confident, different" },
          { label: "Professional", description: "Trustworthy, credible, serious, polished" },
          { label: "Playful", description: "Fun, friendly, approachable, warm" },
          { label: "Minimal", description: "Clean, simple, understated, elegant" }
        ]
      }
    ]
  });

  contextAnalysis = {
    has_context: true,
    from_user_input: true,
    product_type: userInput.answers["Product Type"],
    target_audience: {
      demographics: userInput.answers["Audience"],
      tech_savvy: userInput.answers["Audience"].includes("Gen Z") || userInput.answers["Audience"].includes("Developers") ? "high" : "medium"
    },
    brand_personality: userInput.answers["Brand"].split(',').map(s => s.trim().toLowerCase())
  };
}
```

**Report:**
```
✅ Context Analysis Complete!

🎯 Project Profile:
   - Product: ${contextAnalysis.product_type}
   - Audience: ${contextAnalysis.target_audience.demographics}
   - Brand: ${contextAnalysis.brand_personality.join(', ')}
   ${contextAnalysis.market_position ? `- Position: ${contextAnalysis.market_position}` : ''}

🔄 Generating style direction options...
```

---

## STEP 2: Interactive Style Selection (Verbose + Loop)

> **Key Change:** Interactive loop until user accepts 100%

```javascript
let round = 1;
let maxRounds = 3;
let userAccepted = false;
let selectedStyle = null;
let selectedAnimations = [];
let selectedTheme = null;

while (!userAccepted && round <= maxRounds) {
  output(`
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 ROUND ${round}/${maxRounds}: Style Selection
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  `);

  // ========== STYLE OPTIONS (VERBOSE) ==========

  const styleOptions = [];

  // Generate options from extracted data
  for (const [siteName, data] of Object.entries(extractedData)) {
    styleOptions.push({
      site: siteName,
      style: data.style.detected,
      confidence: data.style.confidence,
      characteristics: data.style.characteristics,
      feel: data.style.feel,
      colors: data.colors.primary,
      animations: data.animation_libraries,
      scrollPatterns: data.scroll_animations.patterns,
      decorativeTypes: data.decorative_elements.types
    });
  }

  // Calculate match scores based on context
  const scoredOptions = styleOptions.map(opt => {
    let score = opt.confidence;

    // Bonus for matching brand personality
    if (contextAnalysis.brand_personality) {
      if (contextAnalysis.brand_personality.includes('bold') &&
          (opt.style === 'Neo-Brutalism' || opt.style === 'Playful/Creative')) {
        score += 15;
      }
      if (contextAnalysis.brand_personality.includes('professional') &&
          (opt.style === 'Minimalist' || opt.style === 'Modern SaaS')) {
        score += 15;
      }
      if (contextAnalysis.brand_personality.includes('playful') &&
          opt.style === 'Playful/Creative') {
        score += 15;
      }
      if (contextAnalysis.brand_personality.includes('minimal') &&
          opt.style === 'Minimalist') {
        score += 15;
      }
    }

    return { ...opt, matchScore: Math.min(score, 100) };
  }).sort((a, b) => b.matchScore - a.matchScore);

  // Display verbose options
  for (const [index, option] of scoredOptions.entries()) {
    const letter = String.fromCharCode(65 + index);
    const isRecommended = index === 0;

    output(`
┌─────────────────────────────────────────────────────────────┐
│ Option ${letter}: ${option.style} ${isRecommended ? '⭐ RECOMMENDED' : ''}
│ Source: ${option.site}
│ Match Score: ${option.matchScore}%
├─────────────────────────────────────────────────────────────┤
│
│ 📝 Characteristics:
│ ${option.characteristics.map(c => `   • ${c}`).join('\n│ ')}
│
│ 🎭 Feel: ${option.feel}
│
│ 🎨 Colors: ${option.colors.join(', ')}
│
│ 🎬 Animations Available:
│ ${option.animations.length > 0 ? option.animations.map(a => `   • ${a.name}`).join('\n│ ') : '   (none detected)'}
│
│ 📜 Scroll Patterns:
│ ${option.scrollPatterns.length > 0 ? option.scrollPatterns.map(p => `   • ${p}`).join('\n│ ') : '   (none detected)'}
│
│ 🖼️ Decorative Elements:
│ ${option.decorativeTypes.length > 0 ? option.decorativeTypes.map(d => `   • ${d}`).join('\n│ ') : '   (none detected)'}
│
└─────────────────────────────────────────────────────────────┘
    `);
  }

  // Ask user to select or provide feedback
  const styleChoice = await AskUserQuestion({
    questions: [{
      question: "เลือก style ที่ชอบ หรือพิมพ์ feedback:",
      header: "Style",
      multiSelect: false,
      options: [
        ...scoredOptions.map((opt, i) => ({
          label: `${String.fromCharCode(65 + i)}: ${opt.style}`,
          description: `${opt.matchScore}% match - ${opt.feel}`
        })),
        { label: "Mix/Custom", description: "ผสมหลาย style หรือปรับแต่งเอง" }
      ]
    }]
  });

  if (styleChoice.answers["Style"] === "Mix/Custom") {
    output(`
พิมพ์ความต้องการ (ตัวอย่าง: "ชอบ border ของ A แต่อยากได้สี soft กว่านี้"):
    `);
    const customInput = await getUserTextInput();

    // AI interprets and adjusts
    output(`
🤖 กำลังปรับตาม feedback: "${customInput}"...
    `);

    round++;
    continue; // Loop again with adjusted options
  }

  // User selected a style
  const selectedIndex = styleChoice.answers["Style"].charCodeAt(0) - 65;
  selectedStyle = scoredOptions[selectedIndex];

  // ========== ANIMATION SELECTION ==========

  output(`
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 ROUND ${round}/${maxRounds}: Animation Selection
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  `);

  // Collect all available animations from all sites
  const allAnimations = [];

  for (const [siteName, data] of Object.entries(extractedData)) {
    // Animation libraries
    for (const lib of data.animation_libraries) {
      allAnimations.push({
        type: 'library',
        name: lib.name,
        source: siteName,
        description: `${lib.name} library detected`
      });
    }

    // Scroll patterns
    for (const pattern of data.scroll_animations.patterns) {
      allAnimations.push({
        type: 'scroll',
        name: pattern,
        source: siteName,
        description: `Scroll animation: ${pattern}`
      });
    }

    // Component animations
    if (data.component_animations.button_hover !== 'none') {
      allAnimations.push({
        type: 'component',
        name: `Button: ${data.component_animations.button_hover}`,
        source: siteName,
        description: data.component_animations.button_hover
      });
    }
    if (data.component_animations.card_hover !== 'none') {
      allAnimations.push({
        type: 'component',
        name: `Card: ${data.component_animations.card_hover}`,
        source: siteName,
        description: data.component_animations.card_hover
      });
    }
  }

  // Display animations
  output(`
🎬 Available Animations (จาก references ทั้งหมด):

${allAnimations.map((anim, i) => `
[${i + 1}] ${anim.name}
    Type: ${anim.type}
    Source: ${anim.source}
    Description: ${anim.description}
`).join('')}
  `);

  const animChoice = await AskUserQuestion({
    questions: [{
      question: "เลือก animations ที่ต้องการ (เลือกได้หลายอัน):",
      header: "Animations",
      multiSelect: true,
      options: allAnimations.map((anim, i) => ({
        label: `${anim.name}`,
        description: `From ${anim.source}: ${anim.description}`
      }))
    }]
  });

  selectedAnimations = animChoice.answers["Animations"]
    ? animChoice.answers["Animations"].split(',').map(s => s.trim())
    : [];

  // ========== THEME + DECORATIVE DIRECTION ==========

  output(`
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 ROUND ${round}/${maxRounds}: Theme & Decorative Direction
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  `);

  // AI recommends themes based on context
  const themePrompt = `
Based on project context, recommend 3-4 theme options.

Project Context:
- Product Type: ${contextAnalysis.product_type}
- Target Audience: ${contextAnalysis.target_audience?.demographics || 'Unknown'}
- Brand Personality: ${contextAnalysis.brand_personality?.join(', ') || 'Unknown'}
${Object.keys(contexts).length > 0 ? `- Context Files: ${Object.keys(contexts).join(', ')}` : ''}
${Object.keys(contexts).length > 0 ? `- Brief Summary: ${Object.values(contexts)[0]?.substring(0, 500)}` : ''}

Return JSON array:
[
  {
    "name": "Theme Name",
    "description": "What this theme represents",
    "feeling": "How it makes users feel",
    "decorative_elements": ["element1", "element2", "element3"],
    "avoid_elements": ["avoid1", "avoid2"],
    "icons_suggestion": ["Lucide icon names"],
    "match_reason": "Why this theme fits the project"
  }
]
`;

  const themeOptions = await LLM({
    prompt: themePrompt,
    response_format: 'json'
  });

  output(`
🎨 Theme Recommendations (based on your project):
  `);

  for (const [index, theme] of themeOptions.entries()) {
    output(`
┌─────────────────────────────────────────────────────────────┐
│ Theme ${String.fromCharCode(65 + index)}: ${theme.name}
├─────────────────────────────────────────────────────────────┤
│
│ 📝 Description: ${theme.description}
│ 🎭 Feeling: ${theme.feeling}
│
│ ✅ Decorative Elements (Use):
│ ${theme.decorative_elements.map(e => `   • ${e}`).join('\n│ ')}
│
│ ❌ Avoid:
│ ${theme.avoid_elements.map(e => `   • ${e}`).join('\n│ ')}
│
│ 🎯 Icons (Lucide): ${theme.icons_suggestion.join(', ')}
│
│ 💡 Why: ${theme.match_reason}
│
└─────────────────────────────────────────────────────────────┘
    `);
  }

  const themeChoice = await AskUserQuestion({
    questions: [{
      question: "เลือก theme หรือพิมพ์ custom:",
      header: "Theme",
      multiSelect: false,
      options: [
        ...themeOptions.map((t, i) => ({
          label: `${String.fromCharCode(65 + i)}: ${t.name}`,
          description: `${t.feeling} - ${t.decorative_elements.slice(0, 3).join(', ')}`
        })),
        { label: "No Theme", description: "ไม่ใช้ theme - geometric/abstract" },
        { label: "Custom", description: "กำหนด theme เอง" }
      ]
    }]
  });

  if (themeChoice.answers["Theme"] === "Custom") {
    output(`พิมพ์ theme ที่ต้องการ (ตัวอย่าง: "อวกาศ - จรวด, ดาวเทียม, ดาว"):`);
    const customTheme = await getUserTextInput();
    selectedTheme = {
      name: 'Custom',
      description: customTheme,
      decorative_elements: customTheme.split(',').map(s => s.trim()),
      avoid_elements: []
    };
  } else if (themeChoice.answers["Theme"] === "No Theme") {
    selectedTheme = {
      name: 'Abstract',
      description: 'No specific theme - geometric and abstract decorations',
      decorative_elements: ['geometric shapes', 'gradients', 'blobs'],
      avoid_elements: []
    };
  } else {
    const themeIndex = themeChoice.answers["Theme"].charCodeAt(0) - 65;
    selectedTheme = themeOptions[themeIndex];
  }

  // ========== CONFIRMATION ==========

  output(`
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ SUMMARY - Please Confirm
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎨 Style: ${selectedStyle.style} (from ${selectedStyle.site})
   Feel: ${selectedStyle.feel}

🎬 Animations Enabled:
${selectedAnimations.map(a => `   ✅ ${a}`).join('\n') || '   (none selected)'}

🎭 Theme: ${selectedTheme.name}
   Decorations: ${selectedTheme.decorative_elements.join(', ')}
   Avoid: ${selectedTheme.avoid_elements.join(', ') || '(none)'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  `);

  const confirmation = await AskUserQuestion({
    questions: [{
      question: "ยืนยันการตั้งค่านี้?",
      header: "Confirm",
      multiSelect: false,
      options: [
        { label: "Yes, Generate", description: "สร้าง design system ตามนี้" },
        { label: "Adjust", description: "ปรับแต่งอีกรอบ" },
        { label: "Start Over", description: "เริ่มใหม่ตั้งแต่ต้น" }
      ]
    }]
  });

  if (confirmation.answers["Confirm"] === "Yes, Generate") {
    userAccepted = true;
  } else if (confirmation.answers["Confirm"] === "Start Over") {
    round = 1;
  } else {
    round++;
  }

  if (round > maxRounds && !userAccepted) {
    output(`
⚠️ ครบ ${maxRounds} รอบแล้ว

แนะนำ:
1. รัน /extract กับ reference ใหม่
2. หรือ accept แล้วค่อย manual edit ไฟล์ที่สร้าง
    `);

    const forceChoice = await AskUserQuestion({
      questions: [{
        question: "ต้องการ generate ตาม settings ปัจจุบันไหม?",
        header: "Force",
        multiSelect: false,
        options: [
          { label: "Yes", description: "Generate ตาม settings ล่าสุด" },
          { label: "Cancel", description: "ยกเลิก" }
        ]
      }]
    });

    if (forceChoice.answers["Force"] === "Yes") {
      userAccepted = true;
    } else {
      return output('Design setup cancelled.');
    }
  }
}
```

**Report:**
```
✅ User Selection Complete!

🎨 Style: ${selectedStyle.style}
🎬 Animations: ${selectedAnimations.length} selected
🎭 Theme: ${selectedTheme.name}

🔄 Generating design system files...
```

---

## STEP 3: Generate Preview YAMLs

For each option, create a preview YAML:

```javascript
for (const [index, option] of styleOptions.options.entries()) {
  const optionLetter = String.fromCharCode(65 + index); // A, B, C

  const previewPrompt = `
You are generating a preview style guide in YAML format.

Style Direction: ${option.name}
Fit Score: ${option.fit_score}%
Rationale: ${option.rationale}

Source Mapping:
${JSON.stringify(option.sources, null, 2)}

Customizations:
${option.customizations.join('\n')}

Extracted Data (for reference):
${JSON.stringify(extractedData, null, 2).substring(0, 5000)}  // First 5000 chars

Task: Create abbreviated YAML preview with key values only.

Format:
\`\`\`yaml
meta:
  style_name: "${option.name}"
  fit_score: ${option.fit_score}
  sources: [list of source sites]

colors:
  primary:
    hex: "#..."  # From ${option.sources.colors}
    rationale: "Why this color fits"
  secondary:
    hex: "#..."
  # ... 5-10 key colors

typography:
  font_family: "..."  # From ${option.sources.typography}
  h1: { size: "...", weight: "..." }
  # ... key type styles

shadows:
  brutal: "..."  # From ${option.sources.shadows}
  # ... 3-5 key shadows

spacing:
  grid: "..."  # From ${option.sources.spacing}

components:
  button:
    hover_animation: "..."  # From ${option.sources.button_hover}
    description: "..."
  card:
    hover_animation: "..."  # From ${option.sources.card_hover}
  # ... key components

border_radius:
  values: [...]  # From ${option.sources.border_radius}
\`\`\`

Return only the YAML content.
`;

  const previewYAML = await LLM({ prompt: previewPrompt });

  Write(
    `design-system/synthesis/options/option-${optionLetter.toLowerCase()}-${option.name.toLowerCase().replace(/\s+/g, '-')}.yaml`,
    previewYAML
  );
}
```

---

## STEP 3.5: Quick User Input (🆕 v1.4.0)

> **NEW:** Ask user for quick feedback before presenting options

```javascript
output(`
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 Quick Question
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
`)

const userFeedback = await AskUserQuestion({
  questions: [{
    question: "มีอะไรอยากปรับหรือเน้นเป็นพิเศษไหม? (optional)",
    header: "Preferences",
    multiSelect: false,
    options: [
      { label: "ไม่มี ใช้ AI แนะนำ", description: "ให้ AI เลือกสิ่งที่เหมาะสมที่สุด" },
      { label: "มีสี CI ของตัวเอง", description: "ระบุสีแบรนด์" },
      { label: "ชอบ component เฉพาะ", description: "ชอบ button/card ของเว็บใดเป็นพิเศษ" },
      { label: "ปรับอื่นๆ", description: "Typography, shadows, หรืออื่นๆ" }
    ]
  }]
})

let userPreferences = { type: 'none' }

// Process user feedback
if (userFeedback.answers["Preferences"] === "มีสี CI ของตัวเอง") {
  output(`
กรุณาระบุสี (HEX format, คั่นด้วย comma):
ตัวอย่าง: #0d7276, #f97316

สีของคุณ:
  `)

  const colorInput = await getUserTextInput()
  const colors = colorInput.split(',').map(s => s.trim()).filter(s => s.match(/^#[0-9A-Fa-f]{6}$/))

  if (colors.length > 0) {
    userPreferences = {
      type: 'custom_colors',
      colors: {
        primary: colors[0],
        secondary: colors[1] || null,
        accent: colors[2] || null
      }
    }
    output(`✅ รับสีแล้ว: ${colors.join(', ')}`)
  }

} else if (userFeedback.answers["Preferences"] === "ชอบ component เฉพาะ") {
  output(`
ระบุความชอบ (ตัวอย่าง: "ชอบ button ของ motherduck, card ของ gitingest"):
  `)

  const preferenceText = await getUserTextInput()
  userPreferences = {
    type: 'component_preference',
    text: preferenceText
  }
  output(`✅ บันทึกความชอบแล้ว`)

} else if (userFeedback.answers["Preferences"] === "ปรับอื่นๆ") {
  output(`
ระบุสิ่งที่อยากปรับ (ตัวอย่าง: "ใช้ font Inter, shadow แบบ soft"):
  `)

  const adjustmentText = await getUserTextInput()
  userPreferences = {
    type: 'other_adjustment',
    text: adjustmentText
  }
  output(`✅ บันทึกการปรับแต่งแล้ว`)
}

output(`
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔄 กำลังสร้าง style options (พร้อม preferences ของคุณ)...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
`)
```

---

## STEP 4: Present Options to User

```javascript
output(`
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎨 Design Direction Analysis Complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Based on:
✓ ${Object.keys(extractedData).length} extracted sites (${Object.keys(extractedData).join(', ')})
✓ Target: ${contextAnalysis.target_audience.demographics}
✓ Brand: ${contextAnalysis.brand_personality.join(', ')}
✓ Product: ${contextAnalysis.product_type}
${userPreferences.type !== 'none' ? `✓ User preferences: ${JSON.stringify(userPreferences)}` : ''}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
`);

for (const [index, option] of styleOptions.options.entries()) {
  const optionLetter = String.fromCharCode(65 + index);
  const isRecommended = index === 0;

  output(`
Option ${optionLetter}: ${option.name} ${isRecommended ? '⭐ (Recommended)' : ''}
Fit Score: ${option.fit_score}%

Rationale:
${option.rationale}

Component Sources:
- Colors: ${option.sources.colors}
- Shadows: ${option.sources.shadows}
- Typography: ${option.sources.typography}
- Button hover: ${option.sources.button_hover}
- Card hover: ${option.sources.card_hover}
- Input focus: ${option.sources.input_focus}
- Border radius: ${option.sources.border_radius}
- Overall vibe: ${option.sources.overall_vibe}

Customizations Applied:
${option.customizations.map(c => `  • ${c}`).join('\n')}

Advantages:
${option.advantages.map(a => `  ✅ ${a}`).join('\n')}

Disadvantages:
${option.disadvantages.map(d => `  ⚠️ ${d}`).join('\n')}

Preview: design-system/synthesis/options/option-${optionLetter.toLowerCase()}-${option.name.toLowerCase().replace(/\s+/g, '-')}.yaml

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
`);
}

// Ask user to select
const userChoice = await AskUserQuestion({
  questions: [{
    question: "Select design direction:",
    header: "Style",
    multiSelect: false,
    options: styleOptions.options.map((opt, i) => ({
      label: `${String.fromCharCode(65 + i)}: ${opt.name}`,
      description: `${opt.fit_score}% fit - ${opt.rationale.substring(0, 100)}...`
    }))
  }]
});

const selectedIndex = userChoice.answers["Style"].charCodeAt(0) - 65;
const selectedOption = styleOptions.options[selectedIndex];
```

**Report:**
```
✅ Style Selected: ${selectedOption.name}

🔄 Generating comprehensive design system...
```

---

## STEP 5: Generate Final Design System (Legacy - See STEP 5.7)

```javascript
const styleGuidePrompt = `
You are generating the final, comprehensive design system file.

Selected Style: ${selectedOption.name}
Fit Score: ${selectedOption.fit_score}%
Rationale: ${selectedOption.rationale}

Source Mapping:
${JSON.stringify(selectedOption.sources, null, 2)}

Customizations:
${selectedOption.customizations.join('\n')}

Full Extracted Data:
${JSON.stringify(extractedData, null, 2)}

Preview YAML:
${Read(`design-system/synthesis/options/option-${String.fromCharCode(65 + selectedIndex).toLowerCase()}-${selectedOption.name.toLowerCase().replace(/\s+/g, '-')}.yaml`)}

Project Context:
- Product: ${contextAnalysis.product_type}
- Audience: ${contextAnalysis.target_audience.demographics}
- Brand: ${contextAnalysis.brand_personality.join(', ')}

Task: Generate complete design system (1500-2000 lines) with ALL 17 sections.

Follow this format:

# [Project Name] Design System - Style Guide (${selectedOption.name})

> **Source:** Based on ${Object.keys(extractedData).join(', ')}, customized for [Project]
> **Date:** ${new Date().toISOString().split('T')[0]}
> **Design Style:** ${selectedOption.name}
> **Tech Stack:** Universal (Framework-agnostic)
> **Primary Color:** [from preview YAML]

---

## Quick Reference

### Most Used Patterns

| Pattern | Code |
|---------|------|
[Table with most-used component patterns with exact Tailwind classes]

### Design Tokens Summary

\`\`\`json
{
  "colors": { ... },
  "spacing": { ... },
  "typography": { ... },
  "borderRadius": { ... },
  "shadows": { ... }
}
\`\`\`

---

## Table of Contents

1. [Overview](#1-overview)
2. [Design Philosophy](#2-design-philosophy)
3. [Color Palette](#3-color-palette)
... (all 17)

---

## 1. Overview

**Summary:**
This design system is based on **${selectedOption.name}** aesthetics...

**Key Characteristics:**
- [List from extracted data + customizations]

**Tech Stack:**
- Framework: Universal
- Styling: Tailwind CSS recommended
- Font: [from typography source]

**Goals:**
- [Derived from rationale + advantages]

---

## 2. Design Philosophy

**Core Principles:**

1. **[Principle 1 from rationale]**
   - [Description]

2. **[Principle 2]**
   - [Description]

... (derive from ${selectedOption.name} characteristics + rationale)

**Visual Identity:**
${selectedOption.rationale}

**Key Differentiators:**
${selectedOption.advantages.slice(0, 3).map(a => `- ${a}`).join('\n')}

**User Experience Goals:**
- First Impression: [based on style name]
- During Use: [based on style name]
- Long-term: [based on style name]

---

## 3. Color Palette

[Extract from preview YAML + source data]

### Primary Colors

**Primary ([Color Name])**
- **Color**: [hex] (rgb(...))
- **Usage**: [from source data]
- **Psychology**: [analysis]
- **Source**: ${selectedOption.sources.colors}
- **CSS Variable**: \`var(--color-primary)\`
- **Tailwind**: \`bg-primary\`, \`text-primary\`, \`border-primary\`

... continue all colors from preview YAML ...

---

## 4. Typography

[Extract from source data]

**Font Family:**
\`\`\`css
font-family: [from ${selectedOption.sources.typography}]
\`\`\`

**Font Weights:**
[Table from source data]

**Text Styles:**

### Headings

**H1 - [Usage]**
\`\`\`html
<h1 className="[exact Tailwind classes from source]">
  Example Text
</h1>
\`\`\`
- **Size**: [from source]
- **Weight**: [from source]
- **Source**: ${selectedOption.sources.typography}

... continue all typography ...

---

## 5. Spacing System

[Extract from ${selectedOption.sources.spacing}]

**Grid Base:** [from source data]

**Scale:** [array from source]

---

## 6. Component Styles

### 6.2 Button Component

**Primary Button**
\`\`\`tsx
<button className="[exact classes from ${selectedOption.sources.button_hover}]">
  Click me
</button>
\`\`\`

**Animation:**
- **Type**: [from extracted animations]
- **Description**: [from animations data]
- **Source**: ${selectedOption.sources.button_hover}
- **Duration**: [from source]

... continue all components from all sources ...

---

## 7. Shadows & Elevation

[Extract from ${selectedOption.sources.shadows}]

... continue all 17 sections ...

---

## 17. Additional Sections

### 17.1 Implementation Best Practices

**Design Token Usage:**
- ✅ Use [font] for everything
- ✅ Use [spacing] grid
- ✅ Use [shadow style]
- ❌ Never [anti-pattern from disadvantages]

### 17.2 Accessibility Guidelines

[Standard accessibility section]

### 17.3 Critical Rules

**DO:**
${selectedOption.advantages.map(a => `- ✅ ${a}`).join('\n')}

**DON'T:**
${selectedOption.disadvantages.map(d => `- ❌ ${d}`).join('\n')}

---

*Customized for [Project] from ${selectedOption.name} design principles*
*Date: ${new Date().toISOString().split('T')[0]}*
*Sources: ${Object.keys(extractedData).join(', ')}*
`;

const styleGuideMD = await LLM({
  prompt: styleGuidePrompt,
  max_tokens: 16000
});

Write('design-system/README.md', styleGuideMD);
```

---

## STEP 5.5: Generate tokens.json (Enhanced v2.0.0)

> **Enhanced v2.0.0:** tokens.json now includes style, theme, animations, decorative_direction, and patterns_index

```javascript
output(`
🔄 Generating enhanced tokens.json...
`);

// Build tokens.json from user selections + extracted data
const tokensData = {
  "$schema": "https://json-schema.org/draft-07/schema",
  "version": "2.0.0",
  "meta": {
    "generated_at": new Date().toISOString(),
    "generated_by": "/designsetup command v2.0.0",
    "source_sites": Object.keys(extractedData),
    "description": "Design tokens for agents (~800 tokens). Human-readable guide: README.md"
  },

  // ========== NEW: Style & Theme (from user selection) ==========
  "style": {
    "name": selectedStyle.style,
    "confidence": selectedStyle.confidence,
    "characteristics": selectedStyle.characteristics,
    "feel": selectedStyle.feel,
    "source_site": selectedStyle.site
  },

  "theme": {
    "name": selectedTheme.name,
    "description": selectedTheme.description,
    "feeling": selectedTheme.feeling || selectedTheme.description,
    "decorative_elements": {
      "use": selectedTheme.decorative_elements,
      "avoid": selectedTheme.avoid_elements
    },
    "icons_suggestion": selectedTheme.icons_suggestion || ["Lucide icons"]
  },

  // ========== NEW: Animations (from user selection) ==========
  "animations": {
    "enabled": selectedAnimations.length > 0,
    "libraries": extractedData[selectedStyle.site]?.animation_libraries || [],
    "selected_patterns": selectedAnimations,
    "scroll_animations": {
      "enabled": selectedAnimations.some(a =>
        a.includes('scroll') || a.includes('parallax') || a.includes('fade') || a.includes('stacking')
      ),
      "patterns": extractedData[selectedStyle.site]?.scroll_animations?.patterns || []
    },
    "component_animations": {
      "button_hover": extractedData[selectedStyle.site]?.component_animations?.button_hover || "scale + shadow",
      "card_hover": extractedData[selectedStyle.site]?.component_animations?.card_hover || "translateY + shadow",
      "input_focus": extractedData[selectedStyle.site]?.component_animations?.input_focus || "ring"
    },
    "duration": {
      "fast": "150ms",
      "normal": "200ms",
      "slow": "300ms"
    },
    "easing": {
      "default": "ease-in-out",
      "bounce": "cubic-bezier(0.68, -0.55, 0.265, 1.55)"
    }
  },

  // ========== Colors (from selected style's source) ==========
  "colors": {
    "primary": {
      "DEFAULT": selectedStyle.colors[0] || "#0d7276",
      "foreground": "#ffffff",
      "hover": darkenColor(selectedStyle.colors[0] || "#0d7276", 10),
      "tailwind": "bg-primary, text-primary, border-primary"
    },
    "secondary": {
      "DEFAULT": selectedStyle.colors[1] || "#64748b",
      "foreground": "#ffffff",
      "hover": darkenColor(selectedStyle.colors[1] || "#64748b", 10)
    },
    "accent": {
      "DEFAULT": selectedStyle.colors[2] || selectedStyle.colors[0] || "#f97316",
      "foreground": "#ffffff"
    },
    "background": {
      "DEFAULT": "#ffffff",
      "muted": "#f1f5f9",
      "subtle": "#f8fafc"
    },
    "foreground": {
      "DEFAULT": "#0a0a0a",
      "muted": "#64748b",
      "subtle": "#94a3b8"
    },
    "border": {
      "DEFAULT": "#e2e8f0",
      "hover": "#cbd5e1",
      "focus": selectedStyle.colors[0] || "#0d7276"
    },
    "semantic": {
      "success": "#10b981",
      "warning": "#f59e0b",
      "error": "#ef4444",
      "info": "#3b82f6"
    }
  },

  // ========== Typography (from extracted data) ==========
  "typography": {
    "font_family": {
      "sans": extractedData[selectedStyle.site]?.typography?.fonts[0] || "'Inter', sans-serif",
      "mono": "'Fira Code', monospace"
    },
    "font_size": {
      "xs": "12px", "sm": "14px", "base": "16px", "lg": "18px",
      "xl": "20px", "2xl": "24px", "3xl": "30px", "4xl": "36px", "5xl": "48px"
    },
    "font_weight": {
      "normal": "400", "medium": "500", "semibold": "600", "bold": "700"
    },
    "headings": {
      "h1": "text-5xl font-bold",
      "h2": "text-4xl font-bold",
      "h3": "text-3xl font-semibold",
      "h4": "text-2xl font-semibold",
      "h5": "text-xl font-medium",
      "h6": "text-lg font-medium"
    }
  },

  // ========== Spacing (from extracted data) ==========
  "spacing": {
    "scale": extractedData[selectedStyle.site]?.spacing?.common || [4, 8, 12, 16, 24, 32, 48, 64, 96],
    "grid_base": extractedData[selectedStyle.site]?.spacing?.grid_base || "8px",
    "common_patterns": {
      "component_padding": "p-4 (16px) or p-6 (24px)",
      "section_gap": "gap-8 (32px) or gap-12 (48px)",
      "layout_margin": "mt-16 (64px) or mt-24 (96px)"
    }
  },

  // ========== Shadows (from extracted data) ==========
  "shadows": {
    "values": extractedData[selectedStyle.site]?.shadows || [
      "0 1px 2px 0 rgb(0 0 0 / 0.05)",
      "0 4px 6px -1px rgb(0 0 0 / 0.1)",
      "0 10px 15px -3px rgb(0 0 0 / 0.1)"
    ],
    "usage": {
      "cards": "shadow-md",
      "dropdowns": "shadow-lg",
      "modals": "shadow-xl",
      "buttons_hover": "shadow-sm"
    }
  },

  // ========== Borders (from extracted data) ==========
  "borders": {
    "radius": extractedData[selectedStyle.site]?.border_radius || ["4px", "8px", "12px", "9999px"],
    "usage": {
      "inputs": "rounded-md",
      "buttons": "rounded-lg",
      "cards": "rounded-xl",
      "avatars": "rounded-full"
    }
  },

  // ========== NEW: Patterns Index (references to patterns/*.md) ==========
  "patterns_index": {
    "buttons": "design-system/patterns/buttons.md",
    "scroll_animations": "design-system/patterns/scroll-animations.md",
    "decorations": "design-system/patterns/decorations.md",
    "cards": "design-system/patterns/cards.md",
    "forms": "design-system/patterns/forms.md"
  },

  // ========== Component Library ==========
  "component_library": {
    "name": "shadcn/ui",
    "install_command": "npx shadcn-ui@latest init",
    "common_components": ["button", "card", "input", "select", "dialog", "dropdown-menu", "badge", "avatar", "tooltip"]
  },

  // ========== Critical Rules ==========
  "critical_rules": {
    "colors": [
      "❌ NO hardcoded hex values",
      "✅ USE theme tokens (bg-primary, text-foreground)"
    ],
    "spacing": [
      "❌ NO arbitrary values (p-5, gap-7)",
      "✅ USE spacing scale (p-4, p-6, gap-8)"
    ],
    "consistency": [
      "❌ NO mixing patterns",
      "✅ USE consistent patterns from tokens"
    ]
  }
};

// Helper function to darken color
function darkenColor(hex, percent) {
  const num = parseInt(hex.replace('#', ''), 16);
  const amt = Math.round(2.55 * percent);
  const R = Math.max((num >> 16) - amt, 0);
  const G = Math.max((num >> 8 & 0x00FF) - amt, 0);
  const B = Math.max((num & 0x0000FF) - amt, 0);
  return '#' + (0x1000000 + R * 0x10000 + G * 0x100 + B).toString(16).slice(1);
}

// Write data.yaml (includes psychology from extracted sites)
const dataYaml = generateDataYaml(tokensData, extractedData, selectedStyle);
Write('design-system/data.yaml', dataYaml);
output(`✅ data.yaml generated (~300 lines)`);
```

---

## STEP 5.6: Generate patterns/*.md Files

> **Code patterns for agents** - Selective loading based on page type

```javascript
output(`
🔄 Generating pattern files...
`);

// Create patterns directory
mkdir('design-system/patterns');

// ========== 1. buttons.md ==========
const buttonsPattern = `# Button Patterns

> **Source:** ${selectedStyle.site} | **Style:** ${selectedStyle.style}
> **Load when:** Any UI page

## Primary Button
\`\`\`tsx
<button className="
  bg-primary text-primary-foreground
  px-4 py-2 rounded-lg
  font-medium
  ${tokensData.animations.component_animations.button_hover === 'scale + shadow'
    ? 'hover:scale-105 hover:shadow-md'
    : 'hover:bg-primary/90'}
  transition-all duration-200
  focus:outline-none focus:ring-2 focus:ring-primary/50
  disabled:opacity-50 disabled:cursor-not-allowed
">
  Button Text
</button>
\`\`\`

## Secondary Button
\`\`\`tsx
<button className="
  bg-secondary text-secondary-foreground
  px-4 py-2 rounded-lg
  font-medium
  hover:bg-secondary/80
  transition-all duration-200
">
  Secondary
</button>
\`\`\`

## Ghost Button
\`\`\`tsx
<button className="
  bg-transparent text-foreground
  px-4 py-2 rounded-lg
  font-medium
  hover:bg-muted
  transition-all duration-200
">
  Ghost
</button>
\`\`\`

## Outline Button
\`\`\`tsx
<button className="
  bg-transparent text-primary
  border border-primary
  px-4 py-2 rounded-lg
  font-medium
  hover:bg-primary hover:text-primary-foreground
  transition-all duration-200
">
  Outline
</button>
\`\`\`

## Icon Button
\`\`\`tsx
<button className="
  p-2 rounded-lg
  hover:bg-muted
  transition-all duration-200
">
  <Icon className="w-5 h-5" />
</button>
\`\`\`

## Button Sizes
\`\`\`tsx
// Small
className="px-3 py-1.5 text-sm rounded-md"

// Medium (default)
className="px-4 py-2 text-base rounded-lg"

// Large
className="px-6 py-3 text-lg rounded-lg"
\`\`\`
`;

Write('design-system/patterns/buttons.md', buttonsPattern);

// ========== 2. scroll-animations.md ==========
const scrollAnimationsPattern = `# Scroll Animation Patterns

> **Source:** ${selectedStyle.site} | **Style:** ${selectedStyle.style}
> **Load when:** Landing pages, marketing pages
> **Libraries:** ${tokensData.animations.libraries.map(l => l.name).join(', ') || 'CSS/Tailwind'}

## Enabled Patterns
${selectedAnimations.length > 0 ? selectedAnimations.map(a => `- ${a}`).join('\n') : '- No scroll animations selected'}

---

## Fade In on Scroll (CSS)
\`\`\`tsx
// Add to component
const [isVisible, setIsVisible] = useState(false);
const ref = useRef(null);

useEffect(() => {
  const observer = new IntersectionObserver(
    ([entry]) => setIsVisible(entry.isIntersecting),
    { threshold: 0.1 }
  );
  if (ref.current) observer.observe(ref.current);
  return () => observer.disconnect();
}, []);

return (
  <div
    ref={ref}
    className={\`
      transition-all duration-700
      \${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'}
    \`}
  >
    {children}
  </div>
);
\`\`\`

## Stacking Cards (GSAP ScrollTrigger)
\`\`\`tsx
// Requires: npm install gsap

import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

useEffect(() => {
  const cards = gsap.utils.toArray('.stacking-card');

  cards.forEach((card, i) => {
    gsap.to(card, {
      scrollTrigger: {
        trigger: card,
        start: 'top 80%',
        end: 'top 20%',
        scrub: true,
      },
      y: -50 * i,
      scale: 1 - (0.05 * i),
      opacity: 1 - (0.1 * i),
    });
  });
}, []);

// JSX
<div className="stacking-card bg-card p-6 rounded-xl shadow-md sticky top-20">
  Card Content
</div>
\`\`\`

## Parallax Section
\`\`\`tsx
// CSS approach
<div className="relative overflow-hidden">
  <div
    className="absolute inset-0 bg-cover bg-center"
    style={{
      backgroundImage: 'url(/hero-bg.jpg)',
      transform: 'translateY(var(--parallax-offset, 0))',
    }}
  />
  <div className="relative z-10 py-24">
    Content here
  </div>
</div>

// Update --parallax-offset on scroll
useEffect(() => {
  const handleScroll = () => {
    const offset = window.scrollY * 0.5;
    document.documentElement.style.setProperty('--parallax-offset', \`\${offset}px\`);
  };
  window.addEventListener('scroll', handleScroll);
  return () => window.removeEventListener('scroll', handleScroll);
}, []);
\`\`\`

## Slide In from Side
\`\`\`tsx
// Left
className="animate-slide-in-left"
// CSS: @keyframes slide-in-left { from { transform: translateX(-100%); opacity: 0; } to { transform: translateX(0); opacity: 1; } }

// Right
className="animate-slide-in-right"
// CSS: @keyframes slide-in-right { from { transform: translateX(100%); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
\`\`\`
`;

Write('design-system/patterns/scroll-animations.md', scrollAnimationsPattern);

// ========== 3. decorations.md ==========
const decorationsPattern = `# Decorative Elements

> **Theme:** ${selectedTheme.name}
> **Load when:** Landing pages, marketing pages (NOT dashboards)

## Theme Direction

### ✅ USE These Elements
${selectedTheme.decorative_elements.map(e => `- ${e}`).join('\n')}

### ❌ AVOID These Elements
${selectedTheme.avoid_elements.length > 0 ? selectedTheme.avoid_elements.map(e => `- ${e}`).join('\n') : '- (none specified)'}

### 🎯 Suggested Icons (Lucide)
${selectedTheme.icons_suggestion?.join(', ') || 'Default Lucide icons'}

---

## Gradient Background
\`\`\`tsx
// Subtle gradient overlay
<div className="
  absolute inset-0 -z-10
  bg-gradient-to-br from-primary/5 via-transparent to-accent/5
"/>

// Mesh gradient (hero sections)
<div className="
  absolute inset-0 -z-10
  bg-[radial-gradient(ellipse_80%_80%_at_50%_-20%,rgba(var(--primary),0.3),transparent)]
"/>
\`\`\`

## Blob Shapes
\`\`\`tsx
// CSS blob
<div className="
  absolute -top-20 -right-20 w-96 h-96
  bg-primary/10 rounded-full blur-3xl
  animate-blob
"/>

// CSS for animation
// @keyframes blob {
//   0%, 100% { transform: translate(0, 0) scale(1); }
//   33% { transform: translate(30px, -50px) scale(1.1); }
//   66% { transform: translate(-20px, 20px) scale(0.9); }
// }
\`\`\`

## Grid Pattern
\`\`\`tsx
// Dot grid background
<div className="
  absolute inset-0 -z-10
  bg-[radial-gradient(#e5e7eb_1px,transparent_1px)]
  [background-size:16px_16px]
"/>

// Line grid
<div className="
  absolute inset-0 -z-10
  bg-[linear-gradient(to_right,#e5e7eb_1px,transparent_1px),linear-gradient(to_bottom,#e5e7eb_1px,transparent_1px)]
  [background-size:24px_24px]
"/>
\`\`\`

## Floating Elements
\`\`\`tsx
// Floating icons (for theme: ${selectedTheme.name})
<div className="absolute top-10 left-10 animate-float opacity-20">
  <IconFromTheme className="w-12 h-12 text-primary" />
</div>

// CSS
// @keyframes float {
//   0%, 100% { transform: translateY(0); }
//   50% { transform: translateY(-20px); }
// }
\`\`\`

## Dividers & Separators
\`\`\`tsx
// Wave divider
<svg className="w-full h-16" viewBox="0 0 1200 120" preserveAspectRatio="none">
  <path d="M0,0V46.29c47.79,22.2,103.59,32.17,158,28,70.36-5.37,136.33-33.31,206.8-37.5C438.64,32.43,512.34,53.67,583,72.05c69.27,18,138.3,24.88,209.4,13.08,36.15-6,69.85-17.84,104.45-29.34C989.49,25,1113-14.29,1200,52.47V0Z" fill="currentColor" className="text-muted/30"/>
</svg>

// Gradient line
<div className="h-px bg-gradient-to-r from-transparent via-border to-transparent" />
\`\`\`
`;

Write('design-system/patterns/decorations.md', decorationsPattern);

// ========== 4. cards.md ==========
const cardsPattern = `# Card Patterns

> **Source:** ${selectedStyle.site} | **Style:** ${selectedStyle.style}
> **Load when:** Any UI page

## Default Card
\`\`\`tsx
<div className="
  bg-card text-card-foreground
  rounded-xl border shadow-md
  p-6
">
  <h3 className="text-xl font-semibold mb-2">Card Title</h3>
  <p className="text-muted-foreground">Card content goes here.</p>
</div>
\`\`\`

## Interactive Card (with hover)
\`\`\`tsx
<div className="
  bg-card text-card-foreground
  rounded-xl border shadow-md
  p-6
  ${tokensData.animations.component_animations.card_hover === 'translateY + shadow'
    ? 'hover:-translate-y-1 hover:shadow-lg'
    : 'hover:border-primary/50'}
  transition-all duration-200
  cursor-pointer
">
  <h3 className="text-xl font-semibold mb-2">Interactive Card</h3>
  <p className="text-muted-foreground">Hover me!</p>
</div>
\`\`\`

## Feature Card
\`\`\`tsx
<div className="
  bg-card text-card-foreground
  rounded-xl border shadow-md
  p-6
  hover:-translate-y-1 hover:shadow-lg
  transition-all duration-200
">
  <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center mb-4">
    <Icon className="w-6 h-6 text-primary" />
  </div>
  <h3 className="text-lg font-semibold mb-2">Feature Title</h3>
  <p className="text-muted-foreground text-sm">
    Feature description goes here.
  </p>
</div>
\`\`\`

## Pricing Card
\`\`\`tsx
<div className="
  bg-card text-card-foreground
  rounded-xl border shadow-md
  p-8
  relative overflow-hidden
">
  {/* Popular badge */}
  <div className="absolute top-4 right-4">
    <span className="bg-primary text-primary-foreground px-3 py-1 rounded-full text-xs font-medium">
      Popular
    </span>
  </div>

  <h3 className="text-xl font-bold mb-2">Pro Plan</h3>
  <div className="text-4xl font-bold mb-4">
    $29<span className="text-lg text-muted-foreground">/mo</span>
  </div>

  <ul className="space-y-3 mb-6">
    <li className="flex items-center gap-2">
      <CheckIcon className="w-5 h-5 text-primary" />
      <span>Feature 1</span>
    </li>
    {/* ... more features */}
  </ul>

  <button className="w-full bg-primary text-primary-foreground py-2 rounded-lg">
    Get Started
  </button>
</div>
\`\`\`

## Testimonial Card
\`\`\`tsx
<div className="
  bg-card text-card-foreground
  rounded-xl border shadow-md
  p-6
">
  <div className="flex items-center gap-4 mb-4">
    <img src="/avatar.jpg" className="w-12 h-12 rounded-full" />
    <div>
      <h4 className="font-semibold">John Doe</h4>
      <p className="text-sm text-muted-foreground">CEO, Company</p>
    </div>
  </div>
  <p className="text-muted-foreground italic">
    "This product is amazing! It has transformed how we work."
  </p>
</div>
\`\`\`
`;

Write('design-system/patterns/cards.md', cardsPattern);

// ========== 5. forms.md ==========
const formsPattern = `# Form Patterns

> **Source:** ${selectedStyle.site} | **Style:** ${selectedStyle.style}
> **Load when:** Auth pages, settings, any form UI

## Input Field
\`\`\`tsx
<div className="space-y-2">
  <label className="text-sm font-medium text-foreground">
    Email Address
  </label>
  <input
    type="email"
    placeholder="you@example.com"
    className="
      w-full px-4 py-2
      bg-background text-foreground
      border rounded-md
      focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary
      placeholder:text-muted-foreground
      transition-all duration-200
    "
  />
  <p className="text-sm text-muted-foreground">
    We'll never share your email.
  </p>
</div>
\`\`\`

## Input with Error
\`\`\`tsx
<div className="space-y-2">
  <label className="text-sm font-medium text-foreground">
    Password
  </label>
  <input
    type="password"
    className="
      w-full px-4 py-2
      bg-background text-foreground
      border border-error rounded-md
      focus:outline-none focus:ring-2 focus:ring-error/50
    "
  />
  <p className="text-sm text-error">
    Password must be at least 8 characters.
  </p>
</div>
\`\`\`

## Select Field
\`\`\`tsx
<div className="space-y-2">
  <label className="text-sm font-medium text-foreground">
    Country
  </label>
  <select className="
    w-full px-4 py-2
    bg-background text-foreground
    border rounded-md
    focus:outline-none focus:ring-2 focus:ring-primary/50
  ">
    <option value="">Select country</option>
    <option value="th">Thailand</option>
    <option value="us">United States</option>
  </select>
</div>
\`\`\`

## Checkbox
\`\`\`tsx
<label className="flex items-center gap-2 cursor-pointer">
  <input
    type="checkbox"
    className="
      w-4 h-4 rounded
      border border-border
      text-primary
      focus:ring-2 focus:ring-primary/50
    "
  />
  <span className="text-sm text-foreground">
    I agree to the terms and conditions
  </span>
</label>
\`\`\`

## Form Layout
\`\`\`tsx
<form className="space-y-6 max-w-md mx-auto">
  {/* Form fields */}

  <button
    type="submit"
    className="
      w-full bg-primary text-primary-foreground
      py-2 rounded-lg font-medium
      hover:bg-primary/90
      transition-all duration-200
    "
  >
    Submit
  </button>
</form>
\`\`\`
`;

Write('design-system/patterns/forms.md', formsPattern);

output(`
✅ Pattern files generated:
   - design-system/patterns/buttons.md
   - design-system/patterns/scroll-animations.md
   - design-system/patterns/decorations.md
   - design-system/patterns/cards.md
   - design-system/patterns/forms.md
`);
```

---

## STEP 5.7: Generate Lean README.md (Human-Readable)

> **Human-readable guide** - No code, just descriptions and visuals

```javascript
output(`
🔄 Generating lean README.md (human-readable)...
`);

const styleGuideMD = `# ${selectedStyle.style} Design System

> **Style:** ${selectedStyle.style}
> **Theme:** ${selectedTheme.name}
> **Generated:** ${new Date().toISOString().split('T')[0]}
> **Sources:** ${Object.keys(extractedData).join(', ')}

---

## 1. Overview

This design system follows **${selectedStyle.style}** aesthetics with a **${selectedTheme.name}** theme.

### Feel
${selectedStyle.feel}

### Characteristics
${selectedStyle.characteristics.map(c => `- ${c}`).join('\n')}

---

## 2. Color Palette

### Primary Color
- **Color:** ${tokensData.colors.primary.DEFAULT}
- **Use for:** CTAs, links, accents, interactive elements
- **Feel:** ${selectedStyle.feel}

### Secondary Color
- **Color:** ${tokensData.colors.secondary.DEFAULT}
- **Use for:** Secondary actions, less prominent elements

### Background Colors
- **Main:** ${tokensData.colors.background.DEFAULT} (white)
- **Muted:** ${tokensData.colors.background.muted} (subtle sections)
- **Subtle:** ${tokensData.colors.background.subtle} (alternating sections)

### Text Colors
- **Primary text:** ${tokensData.colors.foreground.DEFAULT}
- **Muted text:** ${tokensData.colors.foreground.muted}
- **Subtle text:** ${tokensData.colors.foreground.subtle}

### Semantic Colors
- **Success:** ${tokensData.colors.semantic.success} (green)
- **Warning:** ${tokensData.colors.semantic.warning} (amber)
- **Error:** ${tokensData.colors.semantic.error} (red)
- **Info:** ${tokensData.colors.semantic.info} (blue)

---

## 3. Typography

### Font Family
- **Primary:** ${tokensData.typography.font_family.sans}
- **Monospace:** ${tokensData.typography.font_family.mono}

### Heading Sizes
- **H1:** 48px bold - Hero headlines
- **H2:** 36px bold - Section titles
- **H3:** 30px semibold - Subsection titles
- **H4:** 24px semibold - Card titles
- **H5:** 20px medium - Feature titles
- **H6:** 18px medium - Small titles

### Body Text
- **Large:** 18px - Feature descriptions
- **Base:** 16px - Body text
- **Small:** 14px - Captions, labels
- **Extra small:** 12px - Badges, tags

---

## 4. Spacing System

### Base Unit
${tokensData.spacing.grid_base} grid system

### Scale
${tokensData.spacing.scale.map(s => `- ${s}px`).join('\n')}

### Common Patterns
- **Component padding:** 16px or 24px
- **Section gap:** 32px or 48px
- **Layout margin:** 64px or 96px

---

## 5. Shadows & Elevation

### Elevation Levels
- **Level 0:** No shadow (flat elements)
- **Level 1:** Subtle shadow (buttons on hover)
- **Level 2:** Medium shadow (cards)
- **Level 3:** Large shadow (dropdowns)
- **Level 4:** Extra large shadow (modals)

### Usage
- **Cards:** Medium shadow
- **Dropdowns:** Large shadow
- **Modals:** Extra large shadow
- **Button hover:** Subtle shadow

---

## 6. Border Radius

### Values
${tokensData.borders.radius.map(r => `- ${r}`).join('\n')}

### Usage
- **Inputs:** Medium radius (8px)
- **Buttons:** Large radius (12px)
- **Cards:** Extra large radius (16px)
- **Avatars:** Full radius (circle)

---

## 7. Theme: ${selectedTheme.name}

### Description
${selectedTheme.description}

### Feeling
${selectedTheme.feeling || selectedTheme.description}

### Decorative Elements to USE
${selectedTheme.decorative_elements.map(e => `- ✅ ${e}`).join('\n')}

### Elements to AVOID
${selectedTheme.avoid_elements.length > 0 ? selectedTheme.avoid_elements.map(e => `- ❌ ${e}`).join('\n') : '- (none specified)'}

### Suggested Icons
${selectedTheme.icons_suggestion?.join(', ') || 'Lucide icons'}

---

## 8. Animations

### Enabled
${tokensData.animations.enabled ? 'Yes' : 'No'}

### Libraries
${tokensData.animations.libraries.map(l => `- ${l.name}`).join('\n') || '- CSS/Tailwind only'}

### Selected Patterns
${selectedAnimations.length > 0 ? selectedAnimations.map(a => `- ${a}`).join('\n') : '- No scroll animations'}

### Component Animations
- **Button hover:** ${tokensData.animations.component_animations.button_hover}
- **Card hover:** ${tokensData.animations.component_animations.card_hover}
- **Input focus:** ${tokensData.animations.component_animations.input_focus}

### Timing
- **Fast:** 150ms (micro-interactions)
- **Normal:** 200ms (most transitions)
- **Slow:** 300ms (modals, page transitions)

---

## 9. Component Library

### Recommended
${tokensData.component_library.name}

### Common Components
${tokensData.component_library.common_components.map(c => `- ${c}`).join('\n')}

---

## 10. Code Patterns

**For code examples, see:**
- \`design-system/patterns/buttons.md\`
- \`design-system/patterns/cards.md\`
- \`design-system/patterns/forms.md\`
- \`design-system/patterns/scroll-animations.md\`
- \`design-system/patterns/decorations.md\`

---

## 11. Critical Rules

### Colors
- ❌ NO hardcoded hex values
- ✅ USE theme tokens (bg-primary, text-foreground)

### Spacing
- ❌ NO arbitrary values (p-5, gap-7)
- ✅ USE spacing scale (p-4, p-6, gap-8)

### Consistency
- ❌ NO mixing patterns
- ✅ USE consistent patterns from tokens

---

*Generated by /designsetup v2.0.0*
*Sources: ${Object.keys(extractedData).join(', ')}*
`;

Write('design-system/README.md', styleGuideMD);
output(`✅ README.md generated (lean, human-readable, ~100 lines)`);
```

---

## STEP 6: Final Report

```javascript
output(`
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Design Setup Complete!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Summary:
   Style: ${selectedStyle.style} (from ${selectedStyle.site})
   Theme: ${selectedTheme.name}
   Sources: ${Object.keys(extractedData).join(', ')}
   Animations: ${selectedAnimations.length} patterns enabled

🎨 Style Characteristics:
${selectedStyle.characteristics.slice(0, 4).map(c => `   • ${c}`).join('\n')}

🎭 Theme Direction:
   USE: ${selectedTheme.decorative_elements.slice(0, 3).join(', ')}
   AVOID: ${selectedTheme.avoid_elements.slice(0, 2).join(', ') || '(none)'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📦 Files Created:

   🤖 FOR AGENTS (merged data + psychology):
   ✓ design-system/data.yaml (~300 lines)
   ✓ design-system/patterns/buttons.md
   ✓ design-system/patterns/cards.md
   ✓ design-system/patterns/forms.md
   ✓ design-system/patterns/scroll-animations.md
   ✓ design-system/patterns/decorations.md

   👤 FOR HUMANS (summary):
   ✓ design-system/README.md (~100 lines)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 Next Steps:

1. Review generated files:
   cat design-system/data.yaml | head -50
   cat design-system/README.md

2. Plan your pages:
   /pageplan @prd.md @project.md

3. Setup & develop:
   /csetup feature-landing
   /cdev feature-landing

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📖 How It Works:

   /pageplan reads:
   → data.yaml (style, theme, colors, animations, psychology)
   → Auto-detects page type (landing/dashboard/auth)
   → Loads patterns/*.md selectively

   uxui-frontend agent reads:
   → data.yaml (tokens + psychology)
   → patterns/buttons.md (always)
   → patterns/cards.md (always)
   → patterns/scroll-animations.md (landing pages only)
   → patterns/decorations.md (landing pages only)
   → patterns/forms.md (forms only)

   Content includes: Psychology, Target Audience, Why It Works ✨

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
`);
```

---

## Helper: Generate data.yaml

```javascript
function generateDataYaml(tokensData, extractedData, selectedStyle) {
  // Get psychology from the selected extracted site
  const selectedSiteData = extractedData[selectedStyle.site];
  const psychology = selectedSiteData?.psychology || {};

  return `# Design System Data
# Generated by: /designsetup
# Source: ${selectedStyle.site}
# Style: ${selectedStyle.style}

meta:
  generated_at: ${new Date().toISOString()}
  source_site: ${selectedStyle.site}
  style: ${selectedStyle.style}
  theme: ${tokensData.theme?.name || 'default'}

# ============================================
# PSYCHOLOGY & ANALYSIS
# ============================================

psychology:
  style_classification: ${psychology.style_classification || selectedStyle.style}

  emotions_evoked:
${(psychology.emotions_evoked || []).map(e => `    - emotion: "${e.emotion}"
      reason: "${e.reason}"`).join('\n') || '    # Not available'}

  target_audience:
    primary:
      description: "${psychology.target_audience?.primary?.description || 'Not specified'}"
      age_range: "${psychology.target_audience?.primary?.age_range || 'mixed'}"
      tech_savvy: ${psychology.target_audience?.primary?.tech_savvy || 'medium'}
    secondary:
      description: "${psychology.target_audience?.secondary?.description || 'Not specified'}"

  visual_principles:
${(psychology.visual_principles || []).map(v => `    - name: "${v.name}"
      description: "${v.description}"`).join('\n') || '    # Not available'}

  why_it_works:
${(psychology.why_it_works || []).map(w => `    - "${w}"`).join('\n') || '    # Not available'}

  design_philosophy:
    core_belief: "${psychology.design_philosophy?.core_belief || 'Not specified'}"
    key_principles:
${(psychology.design_philosophy?.key_principles || []).map(p => `      - "${p}"`).join('\n') || '      # Not available'}

# ============================================
# DESIGN TOKENS
# ============================================

style:
  detected: ${tokensData.style.detected}
  characteristics:
${tokensData.style.characteristics.map(c => `    - "${c}"`).join('\n')}
  feel: "${tokensData.style.feel}"

colors:
  primary: "${tokensData.colors.primary}"
  secondary: "${tokensData.colors.secondary}"
  background: "${tokensData.colors.background}"
  foreground: "${tokensData.colors.foreground}"
  muted: "${tokensData.colors.muted}"
  accent: "${tokensData.colors.accent}"

typography:
  font_family: "${tokensData.typography.font_family}"
  heading_font: "${tokensData.typography.heading_font}"
  weights: [${tokensData.typography.weights.join(', ')}]
  sizes:
    h1: "${tokensData.typography.sizes.h1}"
    h2: "${tokensData.typography.sizes.h2}"
    h3: "${tokensData.typography.sizes.h3}"
    body: "${tokensData.typography.sizes.body}"
    small: "${tokensData.typography.sizes.small}"

spacing:
  base: ${tokensData.spacing.base}
  scale: [${tokensData.spacing.scale.join(', ')}]

border_radius:
  sm: "${tokensData.border_radius.sm}"
  md: "${tokensData.border_radius.md}"
  lg: "${tokensData.border_radius.lg}"
  full: "${tokensData.border_radius.full}"

shadows:
  sm: "${tokensData.shadows.sm}"
  md: "${tokensData.shadows.md}"
  lg: "${tokensData.shadows.lg}"

# ============================================
# ANIMATIONS
# ============================================

animations:
  durations:
    fast: "${tokensData.animations.durations.fast}"
    normal: "${tokensData.animations.durations.normal}"
    slow: "${tokensData.animations.durations.slow}"
  easing:
    default: "${tokensData.animations.easing.default}"
    bounce: "${tokensData.animations.easing.bounce}"
  component_animations:
    button_hover: "${tokensData.animations.component_animations.button_hover}"
    card_hover: "${tokensData.animations.component_animations.card_hover}"
  scroll_animations:
    enabled: ${tokensData.animations.scroll_animations.enabled}
    patterns:
${(tokensData.animations.scroll_animations.patterns || []).map(p => `      - "${p}"`).join('\n')}

# ============================================
# THEME DIRECTION
# ============================================

theme:
  name: "${tokensData.theme?.name || 'default'}"
  decorative_elements:
${(tokensData.theme?.decorative_elements || []).map(d => `    - "${d}"`).join('\n')}
  avoid_elements:
${(tokensData.theme?.avoid_elements || []).map(a => `    - "${a}"`).join('\n')}
`;
}
```

---

## Error Handling

```javascript
// No extracted data
if (extractedDirs.length === 0) {
  return error(`
    ❌ No extracted data found

    Please extract at least 1 site:
      /extract https://airbnb.com

    Then run: /designsetup @prd.md
  `);
}

// AI analysis fails
try {
  const styleOptions = await LLM({ ... });
} catch (error) {
  return error(`
    ❌ AI analysis failed: ${error.message}

    This may be due to:
    - Extracted data too large (try fewer sites)
    - API rate limit (wait and retry)
    - Invalid context files

    Retry or use --debug for details
  `);
}

// User cancels
if (!userChoice) {
  output(`
    ⚠️ Design setup cancelled

    Your data is preserved:
    - Extracted: design-system/extracted/
    - Options: design-system/synthesis/options/

    Run /designsetup again when ready.
  `);
  return;
}

// Write fails
try {
  Write('design-system/README.md', styleGuideMD);
} catch (error) {
  // Save backup
  Write('/tmp/style-guide-backup.md', styleGuideMD);

  return error(`
    ❌ Failed to write README.md

    Check permissions: design-system/

    Backup saved: /tmp/style-guide-backup.md
  `);
}
```

---

**Now execute the synthesis.**
