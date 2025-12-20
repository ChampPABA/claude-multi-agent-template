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

### STEP 0.1: Find Extracted Site Data

1. Search for extracted site data:
   ```
   Glob: design-system/extracted/*/data.yaml
   ```

**If no files found:**
```
❌ No extracted data found

Please extract at least 1 site first:
  /extract https://motherduck.com
  /extract https://linear.app

Then run: /designsetup @prd.md @project.md
```
→ STOP here, do not continue

**If files found:**
```
✅ Found extracted sites: [list site names]
```
→ Continue to STEP 0.2

### STEP 0.2: Load Extracted Site Data

For each extracted site found:
1. Extract the site name from the path (the folder name between `extracted/` and `/data.yaml`)
2. Read the data.yaml file
3. Parse the YAML content
4. Store in memory for later use (map site name to data)

→ Continue to STEP 0.3

### STEP 0.3: Load Context Files (Optional)

1. Check if user provided context files (arguments starting with `@`)

**If no context files provided:**
- Set contexts as empty
- Will use interactive mode later
→ Continue to STEP 0.4

**If context files provided:**
For each context file argument:
1. Remove the `@` prefix to get the file path
2. Check if file exists:
   - **If not found:** Warn user and skip this file
   - **If found:** Read the file content and store with filename as key

→ Continue to STEP 0.4

### STEP 0.4: Report Discovery Results

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

### STEP 1.1: Check for Context Files

**If context files were loaded in STEP 0.3:**
→ Continue to STEP 1.2 (AI Analysis)

**If no context files:**
→ Skip to STEP 1.3 (Interactive Questions)

### STEP 1.2: AI Analysis of Context Files

1. Ask Claude to analyze the context files and identify project characteristics

**Analysis Prompt:**
```
You are analyzing project context to recommend design directions.

Context Files:
[Include each context file name and first 2000 characters of content]

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
```

2. Parse the JSON response from Claude

**If has_context is true:**
→ Skip to STEP 1.4 (Report)

**If has_context is false:**
→ Continue to STEP 1.3 (Interactive Questions)

### STEP 1.3: Interactive Questions (Fallback)

Ask user to answer these questions:

**Question 1: Product Type**
- Header: "Product Type"
- Single selection
- Options:
  - "SaaS Dashboard" - Business software, data tools, analytics
  - "E-commerce" - Online store, marketplace, shopping
  - "Marketing Site" - Landing pages, content, blog
  - "Internal Tool" - Admin panels, workflows, dashboards

**Question 2: Target Audience**
- Header: "Audience"
- Single selection
- Options:
  - "Gen Z (18-25)" - Young, tech-savvy, bold preferences
  - "Millennials (26-40)" - Professional, value-driven, modern
  - "Enterprise (40+)" - Conservative, trust-focused, established
  - "Developers" - Technical, efficiency-focused, minimal

**Question 3: Brand Personality**
- Header: "Brand"
- Multiple selection allowed
- Options:
  - "Bold" - Stand out, memorable, confident, different
  - "Professional" - Trustworthy, credible, serious, polished
  - "Playful" - Fun, friendly, approachable, warm
  - "Minimal" - Clean, simple, understated, elegant

Build context analysis from user answers:
- product_type: from Question 1
- target_audience.demographics: from Question 2
- target_audience.tech_savvy: "high" if Gen Z or Developers selected, otherwise "medium"
- brand_personality: list from Question 3 (converted to lowercase)

→ Continue to STEP 1.4

### STEP 1.4: Report Context Analysis

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

**Loop Configuration:**
- Maximum rounds: 3
- Current round: starts at 1
- User must accept to exit loop

### STEP 2.1: Start New Round

Display round header:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 ROUND [current round]/3: Style Selection
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

→ Continue to STEP 2.2

### STEP 2.2: Build Style Options from Extracted Data

For each extracted site:
1. Extract the following information from the site's data:
   - site: site name
   - style: data.style.detected
   - confidence: data.style.confidence
   - characteristics: data.style.characteristics
   - feel: data.style.feel
   - colors: data.colors.primary
   - animations: data.animation_libraries
   - scrollPatterns: data.scroll_animations.patterns
   - decorativeTypes: data.decorative_elements.types
2. Add to options list

→ Continue to STEP 2.3

### STEP 2.3: Calculate Match Scores

For each style option:
1. Start with base score = confidence value
2. Apply brand personality bonuses:
   - **If brand includes "bold":**
     - Add +15 if style is "Neo-Brutalism" or "Playful/Creative"
   - **If brand includes "professional":**
     - Add +15 if style is "Minimalist" or "Modern SaaS"
   - **If brand includes "playful":**
     - Add +15 if style is "Playful/Creative"
   - **If brand includes "minimal":**
     - Add +15 if style is "Minimalist"
3. Cap final score at 100 (max)
4. Store as matchScore

Sort all options by matchScore (highest first)

→ Continue to STEP 2.4

### STEP 2.4: Display Verbose Style Options

For each scored option (in sorted order):
1. Assign a letter (A, B, C, etc.)
2. Mark the first option (highest score) as "RECOMMENDED"
3. Display in this format:

```
┌─────────────────────────────────────────────────────────────┐
│ Option [Letter]: [Style Name] [⭐ RECOMMENDED if first]
│ Source: [site name]
│ Match Score: [score]%
├─────────────────────────────────────────────────────────────┤
│
│ 📝 Characteristics:
│    • [characteristic 1]
│    • [characteristic 2]
│    ...
│
│ 🎭 Feel: [feel description]
│
│ 🎨 Colors: [primary colors list]
│
│ 🎬 Animations Available:
│    • [animation 1]
│    • [animation 2]
│    (or "(none detected)")
│
│ 📜 Scroll Patterns:
│    • [pattern 1]
│    • [pattern 2]
│    (or "(none detected)")
│
│ 🖼️ Decorative Elements:
│    • [element 1]
│    • [element 2]
│    (or "(none detected)")
│
└─────────────────────────────────────────────────────────────┘
```

→ Continue to STEP 2.5

### STEP 2.5: Ask User to Select Style

Ask user to choose:
- Header: "Style"
- Single selection
- Options:
  - For each scored option: "[Letter]: [Style Name]" - "[Score]% match - [Feel]"
  - Last option: "Mix/Custom" - "ผสมหลาย style หรือปรับแต่งเอง"

**If user selects "Mix/Custom":**
1. Display prompt: "พิมพ์ความต้องการ (ตัวอย่าง: 'ชอบ border ของ A แต่อยากได้สี soft กว่านี้'):"
2. Get text input from user
3. Display: "🤖 กำลังปรับตาม feedback: '[input]'..."
4. Increment round counter
5. **If round <= 3:** → Go back to STEP 2.1 (new round with adjusted options)
6. **If round > 3:** → Continue to STEP 2.10 (max rounds reached)

**If user selects a specific style (A, B, C, etc.):**
1. Extract the letter (A=0, B=1, C=2, etc.)
2. Get the corresponding option from scored list
3. Store as selectedStyle
→ Continue to STEP 2.6

### STEP 2.6: Animation Selection

Display round header:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 ROUND [current round]/3: Animation Selection
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Step 2.6.1: Collect All Available Animations**

For each extracted site:
1. **From animation_libraries:**
   - For each library: Add entry with type="library", name=lib.name, source=siteName, description="[lib.name] library detected"

2. **From scroll_animations.patterns:**
   - For each pattern: Add entry with type="scroll", name=pattern, source=siteName, description="Scroll animation: [pattern]"

3. **From component_animations:**
   - **If button_hover is not "none":**
     - Add entry with type="component", name="Button: [button_hover]", source=siteName, description=button_hover value
   - **If card_hover is not "none":**
     - Add entry with type="component", name="Card: [card_hover]", source=siteName, description=card_hover value

**Step 2.6.2: Display Available Animations**

Display header: "🎬 Available Animations (จาก references ทั้งหมด):"

For each animation (numbered 1, 2, 3, etc.):
```
[number] [animation name]
    Type: [type]
    Source: [source site]
    Description: [description]
```

**Step 2.6.3: Ask User to Select Animations**

Ask user to choose:
- Header: "Animations"
- Multiple selection allowed
- Question: "เลือก animations ที่ต้องการ (เลือกได้หลายอัน):"
- Options:
  - For each animation: "[animation name]" - "From [source]: [description]"

Parse user's selections and store as selectedAnimations list

→ Continue to STEP 2.7

### STEP 2.7: Theme & Decorative Direction

Display round header:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 ROUND [current round]/3: Theme & Decorative Direction
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Step 2.7.1: AI Theme Recommendations**

Ask Claude to recommend 3-4 theme options based on project context.

**Recommendation Prompt:**
```
Based on project context, recommend 3-4 theme options.

Project Context:
- Product Type: [from context analysis]
- Target Audience: [from context analysis]
- Brand Personality: [from context analysis]
[If context files exist: list context file names]
[If context files exist: include first 500 chars of first file]

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
```

Parse the JSON response to get theme options list.

**Step 2.7.2: Display Theme Options**

Display header: "🎨 Theme Recommendations (based on your project):"

For each theme option:
```
┌─────────────────────────────────────────────────────────────┐
│ Theme [Letter]: [theme name]
├─────────────────────────────────────────────────────────────┤
│
│ 📝 Description: [description]
│ 🎭 Feeling: [feeling]
│
│ ✅ Decorative Elements (Use):
│    • [element 1]
│    • [element 2]
│    ...
│
│ ❌ Avoid:
│    • [avoid 1]
│    • [avoid 2]
│    ...
│
│ 🎯 Icons (Lucide): [icons list]
│
│ 💡 Why: [match_reason]
│
└─────────────────────────────────────────────────────────────┘
```

**Step 2.7.3: Ask User to Select Theme**

Ask user to choose:
- Header: "Theme"
- Single selection
- Question: "เลือก theme หรือพิมพ์ custom:"
- Options:
  - For each theme: "[Letter]: [name]" - "[feeling] - [first 3 decorative elements]"
  - "No Theme" - "ไม่ใช้ theme - geometric/abstract"
  - "Custom" - "กำหนด theme เอง"

**If user selects "Custom":**
1. Display prompt: "พิมพ์ theme ที่ต้องการ (ตัวอย่าง: 'อวกาศ - จรวด, ดาวเทียม, ดาว'):"
2. Get text input from user
3. Build custom theme:
   - name: "Custom"
   - description: [user input]
   - decorative_elements: [split user input by comma and trim]
   - avoid_elements: []
4. Store as selectedTheme

**If user selects "No Theme":**
1. Build abstract theme:
   - name: "Abstract"
   - description: "No specific theme - geometric and abstract decorations"
   - decorative_elements: ["geometric shapes", "gradients", "blobs"]
   - avoid_elements: []
2. Store as selectedTheme

**If user selects a specific theme (A, B, C, etc.):**
1. Extract the letter (A=0, B=1, C=2, etc.)
2. Get the corresponding theme from options list
3. Store as selectedTheme

→ Continue to STEP 2.8

### STEP 2.8: Display Summary and Confirmation

Display summary header:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ SUMMARY - Please Confirm
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎨 Style: [selectedStyle.style] (from [selectedStyle.site])
   Feel: [selectedStyle.feel]

🎬 Animations Enabled:
   ✅ [animation 1]
   ✅ [animation 2]
   (or "(none selected)" if empty)

🎭 Theme: [selectedTheme.name]
   Decorations: [decorative_elements list]
   Avoid: [avoid_elements list or "(none)"]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Step 2.8.1: Ask User to Confirm**

Ask user to confirm:
- Header: "Confirm"
- Single selection
- Question: "ยืนยันการตั้งค่านี้?"
- Options:
  - "Yes, Generate" - "สร้าง design system ตามนี้"
  - "Adjust" - "ปรับแต่งอีกรอบ"
  - "Start Over" - "เริ่มใหม่ตั้งแต่ต้น"

**If user selects "Yes, Generate":**
- Mark as accepted
→ Exit loop, continue to STEP 3

**If user selects "Start Over":**
- Reset round counter to 1
→ Go back to STEP 2.1 (start fresh)

**If user selects "Adjust":**
- Increment round counter
→ Continue to STEP 2.9 (check round limit)

### STEP 2.9: Check Round Limit

**If current round <= 3:**
→ Go back to STEP 2.1 (new adjustment round)

**If current round > 3 (max rounds reached):**
→ Continue to STEP 2.10

### STEP 2.10: Max Rounds Reached - Force Decision

Display warning:
```
⚠️ ครบ 3 รอบแล้ว

แนะนำ:
1. รัน /extract กับ reference ใหม่
2. หรือ accept แล้วค่อย manual edit ไฟล์ที่สร้าง
```

Ask user for final decision:
- Header: "Force"
- Single selection
- Question: "ต้องการ generate ตาม settings ปัจจุบันไหม?"
- Options:
  - "Yes" - "Generate ตาม settings ล่าสุด"
  - "Cancel" - "ยกเลิก"

**If user selects "Yes":**
- Mark as accepted
→ Continue to STEP 3

**If user selects "Cancel":**
- Display: "Design setup cancelled."
→ STOP (exit command)

---

**Report:**
```
✅ User Selection Complete!

🎨 Style: ${selectedStyle.style}
🎬 Animations: ${selectedAnimations.length} selected
🎭 Theme: ${selectedTheme.name}

🔄 Generating design system files...
```

---

## STEP 3: Generate Preview YAMLs (Legacy - Optional)

> **Note:** This step is optional and creates preview files for each option. In the new flow, we skip directly to generating the final files.

**If you want to generate preview files:**

For each style option that was presented to the user:
1. Assign a letter (A, B, C, etc.)
2. Ask Claude to generate an abbreviated YAML preview

**Preview Generation Prompt:**
```
You are generating a preview style guide in YAML format.

Style Direction: [option.name]
Fit Score: [option.fit_score]%
Rationale: [option.rationale]

Source Mapping:
[JSON of option.sources]

Customizations:
[list of option.customizations]

Extracted Data (for reference):
[First 5000 chars of extractedData JSON]

Task: Create abbreviated YAML preview with key values only.

Format:
```yaml
meta:
  style_name: "[option.name]"
  fit_score: [option.fit_score]
  sources: [list of source sites]

colors:
  primary:
    hex: "#..."  # From [option.sources.colors]
    rationale: "Why this color fits"
  secondary:
    hex: "#..."
  # ... 5-10 key colors

typography:
  font_family: "..."  # From [option.sources.typography]
  h1: { size: "...", weight: "..." }
  # ... key type styles

shadows:
  brutal: "..."  # From [option.sources.shadows]
  # ... 3-5 key shadows

spacing:
  grid: "..."  # From [option.sources.spacing]

components:
  button:
    hover_animation: "..."  # From [option.sources.button_hover]
    description: "..."
  card:
    hover_animation: "..."  # From [option.sources.card_hover]
  # ... key components

border_radius:
  values: [...]  # From [option.sources.border_radius]
```

Return only the YAML content.
```

3. Write the preview to file:
   - Path: `design-system/synthesis/options/option-[letter]-[name-kebab-case].yaml`
   - Content: YAML from Claude's response

**Skip this step in most cases** - proceed directly to STEP 3.5

---

## STEP 3.5: Quick User Input (Legacy - v1.4.0)

> **Note:** This step is from an older version and asks for preferences before presenting options. This is now integrated into STEP 2's interactive loop. Can be skipped.

**If you want to collect user preferences upfront:**

Display header:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 Quick Question
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Ask user about special preferences:
- Header: "Preferences"
- Single selection
- Question: "มีอะไรอยากปรับหรือเน้นเป็นพิเศษไหม? (optional)"
- Options:
  - "ไม่มี ใช้ AI แนะนำ" - "ให้ AI เลือกสิ่งที่เหมาะสมที่สุด"
  - "มีสี CI ของตัวเอง" - "ระบุสีแบรนด์"
  - "ชอบ component เฉพาะ" - "ชอบ button/card ของเว็บใดเป็นพิเศษ"
  - "ปรับอื่นๆ" - "Typography, shadows, หรืออื่นๆ"

Initialize userPreferences with type: 'none'

**If user selects "มีสี CI ของตัวเอง":**
1. Display prompt:
   ```
   กรุณาระบุสี (HEX format, คั่นด้วย comma):
   ตัวอย่าง: #0d7276, #f97316

   สีของคุณ:
   ```
2. Get text input from user
3. Parse colors: split by comma, trim, filter only valid HEX format (#RRGGBB)
4. **If valid colors found:**
   - Set userPreferences.type = 'custom_colors'
   - Set userPreferences.colors.primary = first color
   - Set userPreferences.colors.secondary = second color (or null)
   - Set userPreferences.colors.accent = third color (or null)
   - Display: "✅ รับสีแล้ว: [colors list]"

**If user selects "ชอบ component เฉพาะ":**
1. Display prompt: "ระบุความชอบ (ตัวอย่าง: 'ชอบ button ของ motherduck, card ของ gitingest'):"
2. Get text input from user
3. Set userPreferences.type = 'component_preference'
4. Set userPreferences.text = user input
5. Display: "✅ บันทึกความชอบแล้ว"

**If user selects "ปรับอื่นๆ":**
1. Display prompt: "ระบุสิ่งที่อยากปรับ (ตัวอย่าง: 'ใช้ font Inter, shadow แบบ soft'):"
2. Get text input from user
3. Set userPreferences.type = 'other_adjustment'
4. Set userPreferences.text = user input
5. Display: "✅ บันทึกการปรับแต่งแล้ว"

Display final message:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔄 กำลังสร้าง style options (พร้อม preferences ของคุณ)...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**In most cases, skip this step** - preferences are handled in STEP 2's interactive loop

---

## STEP 4: Present Options to User (Legacy - Old Flow)

> **Note:** This step is from the old flow (v1.x). In the new flow (v2.0+), user selection happens in STEP 2's interactive loop. This step is now DEPRECATED.

**Old flow (for reference only):**

Display analysis summary:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎨 Design Direction Analysis Complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Based on:
✓ [number] extracted sites ([site names])
✓ Target: [target audience]
✓ Brand: [brand personality]
✓ Product: [product type]
[If preferences: ✓ User preferences: [preferences]]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

For each style option:
Display:
```
Option [Letter]: [option.name] [⭐ (Recommended) if first]
Fit Score: [option.fit_score]%

Rationale:
[option.rationale]

Component Sources:
- Colors: [option.sources.colors]
- Shadows: [option.sources.shadows]
- Typography: [option.sources.typography]
- Button hover: [option.sources.button_hover]
- Card hover: [option.sources.card_hover]
- Input focus: [option.sources.input_focus]
- Border radius: [option.sources.border_radius]
- Overall vibe: [option.sources.overall_vibe]

Customizations Applied:
  • [customization 1]
  • [customization 2]
  ...

Advantages:
  ✅ [advantage 1]
  ✅ [advantage 2]
  ...

Disadvantages:
  ⚠️ [disadvantage 1]
  ⚠️ [disadvantage 2]
  ...

Preview: design-system/synthesis/options/option-[letter]-[name-kebab].yaml

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Ask user to select:
- Header: "Style"
- Single selection
- Question: "Select design direction:"
- Options:
  - For each option: "[Letter]: [name]" - "[score]% fit - [first 100 chars of rationale]..."

Extract selected index and get corresponding option.

**Report:**
```
✅ Style Selected: [selectedOption.name]

🔄 Generating comprehensive design system...
```

**In current version (v2.0+), skip this step** - user selection is handled in STEP 2

---

## STEP 5: Generate Final Design System (Legacy - Deprecated in v2.0+)

> **Note:** This step is from the old flow (v1.x). In the current flow (v2.0+), design system generation happens in STEP 5.5 (data.yaml), STEP 5.6 (patterns/*.md), and STEP 5.7 (README.md). This step is now DEPRECATED.

**Old flow (for reference only):**

This step would generate a comprehensive 1500-2000 line README.md by:

1. Preparing a prompt for Claude with:
   - Selected option details (name, fit score, rationale)
   - Source mapping (which site provided which design elements)
   - Customizations applied
   - Full extracted data from all sites
   - Preview YAML content
   - Project context (product type, audience, brand)

2. The prompt would request a complete design system markdown file with:
   - Header with metadata (source, date, style, tech stack, primary color)
   - Quick reference section (most-used patterns table, design tokens JSON)
   - Table of contents (all 17 sections)
   - Section 1: Overview (summary, characteristics, tech stack, goals)
   - Section 2: Design Philosophy (core principles, visual identity, differentiators, UX goals)
   - Section 3: Color Palette (primary/secondary colors with hex, usage, psychology, source, CSS variables, Tailwind classes)
   - Section 4: Typography (font family, weights, text styles for all headings with exact Tailwind classes and sources)
   - Section 5: Spacing System (grid base, scale array from source)
   - Section 6: Component Styles (buttons, cards, etc. with exact classes, animations, sources)
   - Section 7: Shadows & Elevation (levels and usage from source)
   - Sections 8-16: [Other design system sections]
   - Section 17: Additional Sections (implementation best practices, accessibility guidelines, critical DO/DON'T rules)
   - Footer with project name, date, sources

3. Ask Claude's LLM to generate the content (max 16000 tokens)

4. Write the generated content to `design-system/README.md`

**In current version (v2.0+), skip this step** - generation is split into STEP 5.5, 5.6, and 5.7

---

## STEP 5.5: Generate tokens.json and data.yaml (Enhanced v2.0.0)

> **Enhanced v2.0.0:** Now includes style, theme, animations, decorative_direction, and patterns_index

Display progress:
```
🔄 Generating enhanced tokens.json...
```

### Build Tokens Data Structure

Create a data structure with the following sections:

**1. Schema & Meta:**
- schema: "https://json-schema.org/draft-07/schema"
- version: "2.0.0"
- meta.generated_at: current timestamp (ISO format)
- meta.generated_by: "/designsetup command v2.0.0"
- meta.source_sites: list of extracted site names
- meta.description: "Design tokens for agents (~800 tokens). Human-readable guide: README.md"

**2. Style (from user selection in STEP 2):**
- style.name: selectedStyle.style
- style.confidence: selectedStyle.confidence
- style.characteristics: selectedStyle.characteristics
- style.feel: selectedStyle.feel
- style.source_site: selectedStyle.site

**3. Theme (from user selection in STEP 2.7):**
- theme.name: selectedTheme.name
- theme.description: selectedTheme.description
- theme.feeling: selectedTheme.feeling (or description if feeling not set)
- theme.decorative_elements.use: selectedTheme.decorative_elements
- theme.decorative_elements.avoid: selectedTheme.avoid_elements
- theme.icons_suggestion: selectedTheme.icons_suggestion (or ["Lucide icons"] as fallback)

**4. Animations (from user selection in STEP 2.6):**
- animations.enabled: true if selectedAnimations has items, false otherwise
- animations.libraries: extractedData[selectedStyle.site].animation_libraries (or empty array)
- animations.selected_patterns: selectedAnimations list
- animations.scroll_animations.enabled: true if any selected animation includes 'scroll', 'parallax', 'fade', or 'stacking'
- animations.scroll_animations.patterns: extractedData[selectedStyle.site].scroll_animations.patterns (or empty)
- animations.component_animations.button_hover: from selected site's data (or "scale + shadow" as fallback)
- animations.component_animations.card_hover: from selected site's data (or "translateY + shadow" as fallback)
- animations.component_animations.input_focus: from selected site's data (or "ring" as fallback)
- animations.duration.fast: "150ms"
- animations.duration.normal: "200ms"
- animations.duration.slow: "300ms"
- animations.easing.default: "ease-in-out"
- animations.easing.bounce: "cubic-bezier(0.68, -0.55, 0.265, 1.55)"

**5. Colors (from selectedStyle):**
- colors.primary.DEFAULT: selectedStyle.colors[0] (or "#0d7276" as fallback)
- colors.primary.foreground: "#ffffff"
- colors.primary.hover: darken primary color by 10%
- colors.primary.tailwind: "bg-primary, text-primary, border-primary"
- colors.secondary.DEFAULT: selectedStyle.colors[1] (or "#64748b" as fallback)
- colors.secondary.foreground: "#ffffff"
- colors.secondary.hover: darken secondary color by 10%
- colors.accent.DEFAULT: selectedStyle.colors[2] (or primary color, or "#f97316")
- colors.accent.foreground: "#ffffff"
- colors.background: { DEFAULT: "#ffffff", muted: "#f1f5f9", subtle: "#f8fafc" }
- colors.foreground: { DEFAULT: "#0a0a0a", muted: "#64748b", subtle: "#94a3b8" }
- colors.border: { DEFAULT: "#e2e8f0", hover: "#cbd5e1", focus: primary color }
- colors.semantic: { success: "#10b981", warning: "#f59e0b", error: "#ef4444", info: "#3b82f6" }

**Color Darkening Logic:**
To darken a hex color by a percentage:
1. Remove '#' prefix and convert to integer
2. Calculate amount: round(2.55 * percent)
3. Extract RGB: R = (num >> 16), G = (num >> 8 & 0xFF), B = (num & 0xFF)
4. Subtract amount from each: max(R - amount, 0), max(G - amount, 0), max(B - amount, 0)
5. Recombine and convert back to hex with '#' prefix

**6. Typography (from selected site):**
- typography.font_family.sans: extractedData[selectedStyle.site].typography.fonts[0] (or "'Inter', sans-serif")
- typography.font_family.mono: "'Fira Code', monospace"
- typography.font_size: { xs: "12px", sm: "14px", base: "16px", lg: "18px", xl: "20px", 2xl: "24px", 3xl: "30px", 4xl: "36px", 5xl: "48px" }
- typography.font_weight: { normal: "400", medium: "500", semibold: "600", bold: "700" }
- typography.headings: { h1: "text-5xl font-bold", h2: "text-4xl font-bold", h3: "text-3xl font-semibold", h4: "text-2xl font-semibold", h5: "text-xl font-medium", h6: "text-lg font-medium" }

**7. Spacing (from selected site):**
- spacing.scale: extractedData[selectedStyle.site].spacing.common (or [4, 8, 12, 16, 24, 32, 48, 64, 96])
- spacing.grid_base: extractedData[selectedStyle.site].spacing.grid_base (or "8px")
- spacing.common_patterns: { component_padding: "p-4 (16px) or p-6 (24px)", section_gap: "gap-8 (32px) or gap-12 (48px)", layout_margin: "mt-16 (64px) or mt-24 (96px)" }

**8. Shadows (from selected site):**
- shadows.values: extractedData[selectedStyle.site].shadows (or default array)
- shadows.usage: { cards: "shadow-md", dropdowns: "shadow-lg", modals: "shadow-xl", buttons_hover: "shadow-sm" }

**9. Borders (from selected site):**
- borders.radius: extractedData[selectedStyle.site].border_radius (or ["4px", "8px", "12px", "9999px"])
- borders.usage: { inputs: "rounded-md", buttons: "rounded-lg", cards: "rounded-xl", avatars: "rounded-full" }

**10. Patterns Index:**
- patterns_index.buttons: "design-system/patterns/buttons.md"
- patterns_index.scroll_animations: "design-system/patterns/scroll-animations.md"
- patterns_index.decorations: "design-system/patterns/decorations.md"
- patterns_index.cards: "design-system/patterns/cards.md"
- patterns_index.forms: "design-system/patterns/forms.md"

**11. Component Library:**
- component_library.name: "shadcn/ui"
- component_library.install_command: "npx shadcn-ui@latest init"
- component_library.common_components: ["button", "card", "input", "select", "dialog", "dropdown-menu", "badge", "avatar", "tooltip"]

**12. Critical Rules:**
- critical_rules.colors: ["❌ NO hardcoded hex values", "✅ USE theme tokens (bg-primary, text-foreground)"]
- critical_rules.spacing: ["❌ NO arbitrary values (p-5, gap-7)", "✅ USE spacing scale (p-4, p-6, gap-8)"]
- critical_rules.consistency: ["❌ NO mixing patterns", "✅ USE consistent patterns from tokens"]

### Generate data.yaml

Call the helper function (see Helper section below) to generate YAML format with:
- Tokens data from above
- Psychology data from extractedData[selectedStyle.site]
- All design tokens in YAML format

Write to file: `design-system/data.yaml`

Display confirmation:
```
✅ data.yaml generated (~300 lines)
```

→ Continue to STEP 5.6

---

## STEP 5.6: Generate patterns/*.md Files

> **Code patterns for agents** - Selective loading based on page type

### STEP 5.6.1: Display Progress Message

Display progress message:
```
🔄 Generating pattern files...
```

### STEP 5.6.2: Create Patterns Directory

Create the patterns directory:
- Path: `design-system/patterns`

### STEP 5.6.3: Generate buttons.md

Build the buttons pattern content with these sections:

1. **Header metadata:**
   - Source: selectedStyle.site
   - Style: selectedStyle.style
   - Load when: "Any UI page"

2. **Button variants** (each with TSX code example):
   - Primary Button (with conditional hover based on tokensData.animations.component_animations.button_hover)
   - Secondary Button
   - Ghost Button
   - Outline Button
   - Icon Button

3. **Button sizes:**
   - Small: px-3 py-1.5 text-sm rounded-md
   - Medium (default): px-4 py-2 text-base rounded-lg
   - Large: px-6 py-3 text-lg rounded-lg

### STEP 5.6.4: Generate scroll-animations.md

Build the scroll animations pattern content with these sections:

1. **Header metadata:**
   - Source: selectedStyle.site
   - Style: selectedStyle.style
   - Load when: "Landing pages, marketing pages"
   - Libraries: List from tokensData.animations.libraries or "CSS/Tailwind"

2. **Enabled Patterns list:** List from selectedAnimations or "No scroll animations selected"

3. **Code examples** (TSX):
   - Fade In on Scroll (CSS with IntersectionObserver)
   - Stacking Cards (GSAP ScrollTrigger)
   - Parallax Section (CSS with scroll handler)
   - Slide In from Side (Left and Right animations)

Write the content to `design-system/patterns/scroll-animations.md`

### STEP 5.6.5: Generate decorations.md

Build the decorations pattern content with these sections:

1. **Header metadata:**
   - Theme: selectedTheme.name
   - Load when: "Landing pages, marketing pages (NOT dashboards)"

2. **Theme Direction:**
   - USE These Elements: List from selectedTheme.decorative_elements
   - AVOID These Elements: List from selectedTheme.avoid_elements or "(none specified)"
   - Suggested Icons (Lucide): List from selectedTheme.icons_suggestion or "Default Lucide icons"

3. **Code examples** (TSX):
   - Gradient Background (subtle overlay and mesh gradient)
   - Blob Shapes (animated blob with CSS keyframes)
   - Grid Pattern (dot grid and line grid backgrounds)
   - Floating Elements (floating icons with animation)
   - Dividers & Separators (wave divider SVG and gradient line)

Write the content to `design-system/patterns/decorations.md`

### STEP 5.6.6: Generate cards.md

Build the cards pattern content with these sections:

1. **Header metadata:**
   - Source: selectedStyle.site
   - Style: selectedStyle.style
   - Load when: "Any UI page"

2. **Card variants** (each with TSX code example):
   - Default Card
   - Interactive Card (with conditional hover based on tokensData.animations.component_animations.card_hover)
   - Feature Card (with icon container)
   - Pricing Card (with popular badge, price, features list, CTA button)
   - Testimonial Card (with avatar, name, title, quote)

Write the content to `design-system/patterns/cards.md`

### STEP 5.6.7: Generate forms.md

Build the forms pattern content with these sections:

1. **Header metadata:**
   - Source: selectedStyle.site
   - Style: selectedStyle.style
   - Load when: "Auth pages, settings, any form UI"

2. **Form elements** (each with TSX code example):
   - Input Field (with label, input, helper text)
   - Input with Error (error state styling and error message)
   - Select Field (dropdown)
   - Checkbox (with label)
   - Form Layout (complete form with submit button)

Write the content to `design-system/patterns/forms.md`

### STEP 5.6.8: Display Completion Message

Display completion message:
```
✅ Pattern files generated:
   - design-system/patterns/buttons.md
   - design-system/patterns/scroll-animations.md
   - design-system/patterns/decorations.md
   - design-system/patterns/cards.md
   - design-system/patterns/forms.md
```

→ Continue to STEP 5.7

---

## STEP 5.7: Generate Lean README.md (Human-Readable)

> **Human-readable guide** - No code, just descriptions and visuals

### STEP 5.7.1: Display Progress Message

Display progress message:
```
🔄 Generating lean README.md (human-readable)...
```

### STEP 5.7.2: Build README Content

Build a markdown document with these 11 sections:

**Header:**
- Title: "[selectedStyle.style] Design System"
- Metadata: Style, Theme, Generated date, Sources

**Section 1: Overview**
- Description of design system (style + theme)
- Feel: selectedStyle.feel
- Characteristics: List from selectedStyle.characteristics

**Section 2: Color Palette**
- Primary Color (value, usage, feel)
- Secondary Color (value, usage)
- Background Colors (DEFAULT, muted, subtle)
- Text Colors (DEFAULT, muted, subtle)
- Semantic Colors (success, warning, error, info)

**Section 3: Typography**
- Font Family (sans, monospace)
- Heading Sizes (H1-H6 with px sizes and weights)
- Body Text (large, base, small, extra small)

**Section 4: Spacing System**
- Base Unit: tokensData.spacing.grid_base
- Scale: List from tokensData.spacing.scale
- Common Patterns (component padding, section gap, layout margin)

**Section 5: Shadows & Elevation**
- Elevation Levels (0-4)
- Usage guide for each level

**Section 6: Border Radius**
- Values: List from tokensData.borders.radius
- Usage guide (inputs, buttons, cards, avatars)

**Section 7: Theme**
- Theme name: selectedTheme.name
- Description and feeling
- Decorative Elements to USE (list)
- Elements to AVOID (list or "none specified")
- Suggested Icons

**Section 8: Animations**
- Enabled status (Yes/No)
- Libraries list or "CSS/Tailwind only"
- Selected Patterns list or "No scroll animations"
- Component Animations (button hover, card hover, input focus)
- Timing (fast, normal, slow)

**Section 9: Component Library**
- Recommended: tokensData.component_library.name
- Common Components list

**Section 10: Code Patterns**
- Reference links to all 5 pattern files

**Section 11: Critical Rules**
- Colors rules (NO hardcoded hex, USE tokens)
- Spacing rules (NO arbitrary values, USE scale)
- Consistency rules (NO mixing, USE consistent patterns)

**Footer:**
- "Generated by /designsetup v2.0.0"
- "Sources: [list of extracted sites]"

### STEP 5.7.3: Write README File

Write the markdown content to `design-system/README.md`

### STEP 5.7.4: Display Confirmation

Display confirmation message:
```
✅ README.md generated (lean, human-readable, ~100 lines)
```

→ Continue to STEP 6

---

## STEP 6: Final Report

Display a comprehensive final report with these sections:

**Header:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Design Setup Complete!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Summary Section:**
- Style: [selectedStyle.style] (from [selectedStyle.site])
- Theme: [selectedTheme.name]
- Sources: [list of extracted sites]
- Animations: [count] patterns enabled

**Style Characteristics:**
- List first 4 characteristics from selectedStyle.characteristics

**Theme Direction:**
- USE: First 3 elements from selectedTheme.decorative_elements
- AVOID: First 2 elements from selectedTheme.avoid_elements or "(none)"

**Files Created:**
- FOR AGENTS section:
  - design-system/data.yaml (~300 lines)
  - design-system/patterns/buttons.md
  - design-system/patterns/cards.md
  - design-system/patterns/forms.md
  - design-system/patterns/scroll-animations.md
  - design-system/patterns/decorations.md

- FOR HUMANS section:
  - design-system/README.md (~100 lines)

**Next Steps:**
1. Review generated files (commands provided)
2. Plan your pages with /pageplan
3. Setup & develop with /csetup and /cdev

**How It Works:**
- Explain /pageplan reads data.yaml and auto-detects page type
- Explain uxui-frontend agent reads data.yaml and selective patterns
- Mention content includes Psychology, Target Audience, Why It Works

**Footer:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Helper: Generate data.yaml

This helper function generates the complete data.yaml file by merging psychology data from extracted sites with design tokens.

**Inputs:**
- tokensData: Design tokens object built in STEP 5.5
- extractedData: All extracted site data
- selectedStyle: Selected style object from user choice

**Process:**

1. Get psychology data from the selected site:
   - selectedSiteData = extractedData[selectedStyle.site]
   - psychology = selectedSiteData.psychology or empty object

2. Build YAML content with 5 major sections:

**Section 1: Header Comments**
- Generated by: /designsetup
- Source: selectedStyle.site
- Style: selectedStyle.style

**Section 2: Meta**
- generated_at: Current ISO timestamp
- source_site: selectedStyle.site
- style: selectedStyle.style
- theme: tokensData.theme.name or "default"

**Section 3: Psychology & Analysis**
- style_classification: From psychology or selectedStyle.style
- emotions_evoked: List of {emotion, reason} or "# Not available"
- target_audience:
  - primary: {description, age_range, tech_savvy}
  - secondary: {description}
- visual_principles: List of {name, description} or "# Not available"
- why_it_works: List of strings or "# Not available"
- design_philosophy: {core_belief, key_principles list} or "Not specified"

**Section 4: Design Tokens**
- style: {detected, characteristics list, feel}
- colors: {primary, secondary, background, foreground, muted, accent}
- typography: {font_family, heading_font, weights array, sizes object}
- spacing: {base, scale array}
- border_radius: {sm, md, lg, full}
- shadows: {sm, md, lg}

**Section 5: Animations**
- durations: {fast, normal, slow}
- easing: {default, bounce}
- component_animations: {button_hover, card_hover}
- scroll_animations: {enabled boolean, patterns array}

**Section 6: Theme Direction**
- theme: {name, decorative_elements list, avoid_elements list}

**Output:** Returns the complete YAML content as a string

---

## Error Handling

Handle these error scenarios throughout the workflow:

### Error 1: No Extracted Data (STEP 0.1)

**When:** No design-system/extracted/*/data.yaml files found

**Action:** Display error message and stop execution:
```
❌ No extracted data found

Please extract at least 1 site:
  /extract https://airbnb.com

Then run: /designsetup @prd.md
```

### Error 2: AI Analysis Fails (STEP 1.2, 2.3, etc.)

**When:** LLM call fails during context analysis or style generation

**Action:** Catch error and display message with debugging guidance:
```
❌ AI analysis failed: [error.message]

This may be due to:
- Extracted data too large (try fewer sites)
- API rate limit (wait and retry)
- Invalid context files

Retry or use --debug for details
```

### Error 3: User Cancels (STEP 2.8)

**When:** User selects "Cancel" option at max rounds or during confirmation

**Action:** Display cancellation message and preserve data:
```
⚠️ Design setup cancelled

Your data is preserved:
- Extracted: design-system/extracted/
- Options: design-system/synthesis/options/

Run /designsetup again when ready.
```

### Error 4: Write Fails (STEP 5.6, 5.7)

**When:** Unable to write to design-system/ directory

**Action:**
1. Save backup to temporary location: /tmp/style-guide-backup.md
2. Display error message with backup location:
```
❌ Failed to write README.md

Check permissions: design-system/

Backup saved: /tmp/style-guide-backup.md
```

---

**Now execute the synthesis.**
