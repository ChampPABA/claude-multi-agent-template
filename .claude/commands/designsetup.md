# /designsetup - Synthesize Style Guide from Extracted Data

You are a senior design systems architect with experience at FANG-level companies.

Your task is to analyze extracted design data, synthesize with project context, and generate a comprehensive STYLE_GUIDE.md with AI-recommended style directions.

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

Generate production-ready style guide at: `design-system/STYLE_GUIDE.md`

**Process:**
1. Load all extracted data from `design-system/extracted/`
2. Analyze project context (from @files or user input)
3. Generate 2-3 style direction options with AI reasoning
4. User selects preferred option
5. Generate comprehensive STYLE_GUIDE.md (17 sections, 1500-2000 lines)

**Key Principles:**
1. **Multi-Source Synthesis**: Combine best patterns from all extracted sites
2. **Context-Aware**: Match style to target audience + brand personality
3. **Transparent Reasoning**: Show why each option fits
4. **User Choice**: Present options with pros/cons, let user decide

---

## STEP 0: Discovery & Validation

```javascript
// 1. Find extracted sites
const extractedFiles = glob('design-system/extracted/*/data.yaml');

if (extractedFiles.length === 0) {
  return error(`
    ❌ No extracted data found

    Please extract at least 1 site first:
      /extract https://airbnb.com
      /extract https://blackbird.com
      /extract https://linear.app

    Then run: /designsetup @prd.md @project.md
  `);
}

// 2. Load all extracted data
const extractedData = {};
for (const file of extractedFiles) {
  const siteName = path.dirname(file).split('/').pop();
  extractedData[siteName] = YAML.parse(Read(file));
}

// 3. Load context files
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
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎨 Design Setup Started
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Extracted Sites: ${Object.keys(extractedData).length}
${Object.entries(extractedData).map(([site, data]) =>
  `   - ${site} (${data.meta.coverage.percentage}% coverage, ${data.meta.extracted_at.split('T')[0]})`
).join('\n')}

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

## STEP 2: Style Direction Analysis (AI Pondering)

```javascript
const ponderingPrompt = `
You are a design systems architect creating style direction recommendations.

Extracted Sites Summary:
${Object.entries(extractedData).map(([site, data]) => `
## ${site}
- Style: ${data.sections.overview.style || 'Unknown'}
- Colors: ${data.sections.color_palette.primary.slice(0, 3).map(c => c.hex).join(', ')}
- Shadows: ${data.sections.shadows_elevation.values.slice(0, 2).join(', ')}
- Border Radius: ${data.sections.border_radius.values.slice(0, 3).join(', ')}
- Typography: ${data.sections.typography.fonts.slice(0, 2).join(', ')}
- Button Animation: ${Object.values(data.animations).find(a => a.type === 'button')?.description || 'N/A'}
- Card Animation: ${Object.values(data.animations).find(a => a.type === 'card')?.description || 'N/A'}
`).join('\n')}

Project Context:
- Product: ${contextAnalysis.product_type}
- Target Audience: ${contextAnalysis.target_audience.demographics} (tech-savvy: ${contextAnalysis.target_audience.tech_savvy})
- Brand Personality: ${contextAnalysis.brand_personality.join(', ')}
- Market Position: ${contextAnalysis.market_position || 'Not specified'}

Task: Generate 2-3 style direction options ranked by fit.

Instructions:
1. Wrap thinking in <pondering> tags
2. Consider:
   - Which extracted patterns fit target audience best?
   - Which style matches brand personality?
   - What differentiates from competitors?
   - What are implementation trade-offs?
3. Recommend 2-3 distinct style directions
4. Rank by fit score (0-100)

Return JSON:
{
  "pondering": "...",
  "recommended_count": 2 or 3,
  "options": [
    {
      "name": "Neo-Brutalism" | "Warm Minimalist" | "Modern Professional" | "Playful Rounded" | "Technical Clean" | other,
      "fit_score": 0-100,
      "rationale": "Why this fits (2-3 sentences)",
      "sources": {
        "colors": "site-name | custom",
        "shadows": "site-name",
        "typography": "site-name | custom",
        "spacing": "site-name",
        "button_hover": "site-name",
        "card_hover": "site-name",
        "input_focus": "site-name",
        "border_radius": "site-name",
        "overall_vibe": "site-name"
      },
      "customizations": [
        "Adapt Airbnb warmth to bold colors",
        "Use Blackbird hard shadows instead of soft"
      ],
      "advantages": [
        "string (3-5 advantages)"
      ],
      "disadvantages": [
        "string (2-4 disadvantages)"
      ]
    }
  ]
}

Important:
- Option 1 = highest fit score (primary recommendation)
- Option 2 = good alternative (different approach)
- Option 3 (if needed) = safe fallback
- Each option should be DISTINCT (different visual feel)
- Source mapping must reference actual extracted sites
`;

const styleOptions = await LLM({
  prompt: ponderingPrompt,
  response_format: 'json',
  max_tokens: 4000
});
```

**Report:**
```
✅ Style Directions Generated!

🎨 ${styleOptions.recommended_count} options created
   - Primary: ${styleOptions.options[0].name} (${styleOptions.options[0].fit_score}% fit)
   - Alternative: ${styleOptions.options[1].name} (${styleOptions.options[1].fit_score}% fit)
   ${styleOptions.options[2] ? `- Fallback: ${styleOptions.options[2].name} (${styleOptions.options[2].fit_score}% fit)` : ''}

🔄 Generating option previews...
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

🔄 Generating comprehensive STYLE_GUIDE.md...
```

---

## STEP 5: Generate Final STYLE_GUIDE.md

```javascript
const styleGuidePrompt = `
You are generating the final, comprehensive STYLE_GUIDE.md file.

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

Task: Generate complete STYLE_GUIDE.md (1500-2000 lines) with ALL 17 sections.

CRITICAL: Follow the EXACT format of existing STYLE_GUIDE.md:

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

Write('design-system/STYLE_GUIDE.md', styleGuideMD);
```

---

## STEP 5.5: Generate STYLE_TOKENS.json (Context Optimization)

> **New in v1.2.0:** Generate lightweight design tokens file for token-efficient loading

```javascript
output(`
🔄 Extracting design tokens for efficient loading...
`);

// Extract design tokens from STYLE_GUIDE.md
const tokensPrompt = `
You are extracting design tokens from the STYLE_GUIDE.md into a lightweight JSON format.

Source: STYLE_GUIDE.md content below
${styleGuideMD}

Task: Extract ALL design tokens into JSON format following this exact structure:

{
  "$schema": "https://json-schema.org/draft-07/schema",
  "version": "1.0.0",
  "meta": {
    "generated_at": "${new Date().toISOString()}",
    "generated_by": "/designsetup command",
    "source": "design-system/STYLE_GUIDE.md",
    "design_style": "${selectedOption.name}",
    "description": "Lightweight design tokens extracted from STYLE_GUIDE.md (~500 tokens vs ~5000 tokens for full guide)"
  },
  "tokens": {
    "colors": {
      "primary": {
        "DEFAULT": "[extract from guide]",
        "foreground": "[extract]",
        "hover": "[extract or generate]",
        "description": "Primary brand color for CTAs, links, and accents",
        "tailwind": "bg-primary, text-primary, border-primary"
      },
      "secondary": { ... },
      "background": { ... },
      "foreground": { ... },
      "border": { ... },
      "semantic": {
        "success": "[extract]",
        "warning": "[extract]",
        "error": "[extract]",
        "info": "[extract]"
      }
    },
    "spacing": {
      "scale": [extract spacing scale array],
      "description": "4px or 8px base unit spacing scale",
      "tailwind_mapping": { ... },
      "common_patterns": {
        "component_padding": "p-4 (16px) or p-6 (24px)",
        "section_gap": "gap-8 (32px) or gap-12 (48px)",
        "layout_margin": "mt-16 (64px) or mt-24 (96px)"
      }
    },
    "typography": {
      "font_family": { ... },
      "font_size": { ... },
      "font_weight": { ... },
      "line_height": { ... },
      "headings": { ... }
    },
    "shadows": {
      "sm": "[extract]",
      "DEFAULT": "[extract]",
      "md": "[extract]",
      "lg": "[extract]",
      "xl": "[extract]",
      "usage": {
        "cards": "shadow-md",
        "dropdowns": "shadow-lg",
        "modals": "shadow-xl",
        "buttons_hover": "shadow-sm"
      }
    },
    "borders": {
      "radius": { ... },
      "width": { ... },
      "usage": { ... }
    },
    "animation": {
      "duration": { ... },
      "easing": { ... },
      "common": { ... }
    },
    "breakpoints": { ... },
    "z_index": { ... }
  },
  "component_library": {
    "name": "[extract from guide]",
    "install_command": "[extract]",
    "common_components": [extract array]
  },
  "critical_rules": {
    "colors": [
      "❌ NO hardcoded hex values",
      "✅ USE theme tokens"
    ],
    "spacing": [
      "❌ NO arbitrary values",
      "✅ USE spacing scale"
    ],
    "consistency": [
      "❌ NO mixing patterns",
      "✅ USE consistent patterns"
    ]
  }
}

IMPORTANT:
- Extract ALL values from STYLE_GUIDE.md (don't use placeholders)
- If a value isn't in the guide, infer it logically (e.g., hover = 10% darker than DEFAULT)
- Keep descriptions concise but clear
- Return ONLY valid JSON (no markdown, no explanations)
`;

const tokensJSON = await LLM({
  prompt: tokensPrompt,
  max_tokens: 4000,
  temperature: 0.1 // Low temperature for consistent extraction
});

// Validate JSON
try {
  JSON.parse(tokensJSON);
  Write('design-system/STYLE_TOKENS.json', tokensJSON);
  output(`✅ STYLE_TOKENS.json generated (~500 tokens)`);
} catch (e) {
  warn(`⚠️ Failed to generate STYLE_TOKENS.json: ${e.message}`);
  warn(`Continuing without tokens file...`);
}
```

---

## STEP 6: Final Report

```
✅ Design Setup Complete!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📁 Generated: design-system/STYLE_GUIDE.md

📊 Summary:
   - Style: ${selectedOption.name}
   - Fit Score: ${selectedOption.fit_score}%
   - Sources: ${Object.keys(extractedData).join(', ')}
   - Sections: 17/17 complete ✓
   - Lines: ~${styleGuideMD.split('\n').length}

🎨 Key Features:
${selectedOption.advantages.slice(0, 4).map(a => `   ✓ ${a}`).join('\n')}

📦 Files Created:
   ✓ design-system/STYLE_GUIDE.md (final guide, ~2000 lines)
   ✓ design-system/STYLE_TOKENS.json (lightweight tokens, ~500 tokens) 🆕
   ✓ design-system/synthesis/options/ (${styleOptions.options.length} YAMLs)

⚠️ Trade-offs:
${selectedOption.disadvantages.slice(0, 2).map(d => `   • ${d}`).join('\n')}

🎯 Component Sources:
   - Colors: ${selectedOption.sources.colors}
   - Shadows: ${selectedOption.sources.shadows}
   - Typography: ${selectedOption.sources.typography}
   - Animations: ${selectedOption.sources.button_hover}, ${selectedOption.sources.card_hover}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 Next Steps:

1. Review generated files:
   - Full guide: cat design-system/STYLE_GUIDE.md | head -100
   - Tokens: cat design-system/STYLE_TOKENS.json

2. Setup project (generates design-context.md):
   /psetup

3. Start development:
   /csetup feature-login
   /cdev feature-login

4. Context Optimization (v1.2.0):
   ✅ Commands use STYLE_TOKENS.json (~500 tokens, not full guide ~5K)
   ✅ Agents load design-context.md + STYLE_TOKENS.json (~1.5K total)
   ✅ 70% token reduction while maintaining quality ✨
```

---

## Error Handling

```javascript
// No extracted data
if (extractedFiles.length === 0) {
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
  Write('design-system/STYLE_GUIDE.md', styleGuideMD);
} catch (error) {
  // Save backup
  Write('/tmp/style-guide-backup.md', styleGuideMD);

  return error(`
    ❌ Failed to write STYLE_GUIDE.md

    Check permissions: design-system/

    Backup saved: /tmp/style-guide-backup.md
  `);
}
```

---

**Now execute the synthesis.**
