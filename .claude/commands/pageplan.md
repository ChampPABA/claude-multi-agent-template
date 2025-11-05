# /pageplan - Page Structure & Content Planning

**Purpose:** Generate a detailed page plan for UI implementation, including component reuse strategy, content draft, and asset checklist.

**Usage:**
```bash
# With context files
/pageplan @proposal.md @prd.md @project_brief.md

# Current change only (uses proposal.md in .changes/)
/pageplan

# Specify change ID
/pageplan landing-page
```

---

## What This Command Does

1. **Reads User-Specified Context:**
   - Only reads files that user mentions with `@` prefix
   - Always reads `.changes/{change-id}/proposal.md` (if exists)
   - **Always reads `design-system/STYLE_TOKENS.json`** (lightweight, ~500 tokens) ✅
   - Validates `design-system/STYLE_GUIDE.md` exists (doesn't load full content)

2. **Searches Existing Components:**
   - Glob: `**/{Navbar,Footer,Sidebar,Header}*.{tsx,jsx,vue}`
   - Grep: Common UI patterns
   - Builds reuse vs new component list

3. **Generates page-plan.md:**
   - Component plan (reuse vs new)
   - Page structure (layout composition)
   - Content draft (AI-generated from PRD)
   - Asset checklist (user must prepare)
   - Rationale (why this structure)

4. **Outputs to:** `.changes/{change-id}/page-plan.md`

---

## Implementation Instructions

### STEP 1: Detect Change Context

```typescript
// Detect current change ID
const changesDir = '.changes/'
const changeId = detectCurrentChange() // or from command arg

if (!changeId) {
  error("No active change found. Run after OpenSpec generates proposal.md")
  return
}

const outputPath = `.changes/${changeId}/page-plan.md`
```

### STEP 2: Read Context Files

```typescript
// Only read files user specified with @
const userFiles = extractMentionedFiles(userMessage) // @prd.md, @brief.md

// Always read (if exists)
const proposalPath = `.changes/${changeId}/proposal.md`
const tokensPath = `design-system/STYLE_TOKENS.json` // 🆕 Lightweight tokens
const styleGuidePath = `design-system/STYLE_GUIDE.md` // Validate only, don't load

const contextFiles = [
  ...userFiles,
  proposalPath
].filter(fileExists)

// Read all context
let context = contextFiles.map(readFile).join('\n\n---\n\n')

// 🆕 Load design tokens (lightweight)
if (fileExists(tokensPath)) {
  const tokens = JSON.parse(Read(tokensPath))
  context += `\n\n---\n\n# Design Tokens (STYLE_TOKENS.json)\n\n`
  context += `Primary Color: ${tokens.tokens.colors.primary.DEFAULT}\n`
  context += `Spacing Scale: ${tokens.tokens.spacing.scale.join(', ')}px\n`
  context += `Component Library: ${tokens.component_library.name}\n`
  context += `Shadows: ${Object.keys(tokens.tokens.shadows).join(', ')}\n`
}

// Validate STYLE_GUIDE.md exists (don't load!)
const hasStyleGuide = fileExists(styleGuidePath)
if (!hasStyleGuide) {
  warn(`⚠️ No STYLE_GUIDE.md found - run /designsetup first`)
}

// Total context: ~1.5K tokens (vs 5K+ if loading full STYLE_GUIDE.md)
```

### STEP 3: Search Existing Components

```typescript
// Search for common shared components
const searchPatterns = [
  '**/{Navbar,Navigation}*.{tsx,jsx,vue}',
  '**/{Footer}*.{tsx,jsx,vue}',
  '**/{Sidebar,Drawer}*.{tsx,jsx,vue}',
  '**/{Header}*.{tsx,jsx,vue}',
]

const foundComponents = []
for (const pattern of searchPatterns) {
  const matches = glob(pattern)
  if (matches.length > 0) {
    foundComponents.push({
      name: extractComponentName(matches[0]),
      path: matches[0],
      exports: grepExports(matches[0])
    })
  }
}
```

### STEP 4: Analyze & Generate Plan

Based on context + found components, generate:

```markdown
# Page Plan: [Page Name]
> Generated from: [list of context files]
> Change ID: ${changeId}

## 1. Component Plan

### 🔄 Reuse Components (Found in codebase)
[For each found component]
- **[ComponentName]**
  - Path: \`[path]\`
  - Usage: \`<ComponentName prop="value" />\`
  - Notes: [Any notes about usage]

### ✅ Create New Components

#### Shared Components (reusable across pages)
[Components that will be used in multiple pages]
- **[ComponentName]**
  - Purpose: [description]
  - Will be used in: [list pages]
  - Store at: \`/components/[category]/[ComponentName].tsx\`

#### Page-Specific Components (used only here)
[Components for this page only]
- **[ComponentName]**
  - Purpose: [description]
  - Compose with: [other components]
  - Store at: \`/app/[page]/[ComponentName].tsx\`

## 2. Page Structure

\`\`\`tsx
<Layout>
  <ComponentA />  {/* Reuse */}
  <ComponentB />  {/* New shared */}
  <ComponentC />  {/* New specific */}
</Layout>
\`\`\`

## 3. 📦 Assets to Prepare (คุณต้องเตรียม)

### Images
- [ ] \`filename.jpg\` (widthxheight, format)
      → Place at: \`/public/images/filename.jpg\`
      → Purpose: [description]

### Icons
- [ ] [description] (size, format)
      → Place at: \`/public/icons/\`
      → Style: [match STYLE_GUIDE]

### Other Assets
[Fonts, videos, etc.]

---

## 4. 📝 Content Draft (AI-Generated - กรุณา Review & Edit)

### [Section Name]

**[Element Type]:** "[Content]"
_([length] chars - based on [source])_

[Repeat for all content elements]

---

**Instructions for User:**
1. Review content above
2. Edit tone, length, messaging as needed
3. Prepare assets per checklist
4. When ready, run: \`/csetup ${changeId}\`

---

## 5. Design Notes

**Design System Files:**
- Tokens (lightweight): \`design-system/STYLE_TOKENS.json\`
- Full guide (reference): \`design-system/STYLE_GUIDE.md\`

**Key Design Tokens:**
- Primary color: [from STYLE_TOKENS.json]
- Font family: [from STYLE_TOKENS.json]
- Spacing scale: [from STYLE_TOKENS.json]
- Component library: [from STYLE_TOKENS.json]
- Shadows: [from STYLE_TOKENS.json]

**Agent Instructions:**
- uxui-frontend MUST read STYLE_TOKENS.json in STEP 0.5
- Use theme tokens (text-foreground/70), NOT hardcoded colors
- Use spacing scale (p-4, p-6), NOT arbitrary values (p-5)

## 6. Implementation Notes

### Component Imports (Reference)
\`\`\`tsx
// Reuse
[import statements for reused components]

// shadcn/ui or component library
[import statements]

// New (to be created)
[import statements with comments]
\`\`\`

---

## Next Steps
1. ✅ Review & edit content draft
2. ✅ Prepare assets (images, icons)
3. ✅ Run \`/csetup ${changeId}\` when ready
4. ✅ Run \`/cdev ${changeId}\` to implement
```

### STEP 5: Write Output & Report

```typescript
// Write page-plan.md
writeFile(outputPath, pagePlanContent)

// Report to user
console.log(`
✅ Page plan generated!

📄 Output: ${outputPath}

📊 Summary:
- Found components: ${foundComponents.length} (reuse)
- New shared: ${newSharedComponents.length}
- New specific: ${newSpecificComponents.length}
- Assets needed: ${assetsCount}
- Content sections: ${contentSections.length}

📝 Next Steps:
1. Review content in ${outputPath}
2. Edit as needed (tone, messaging)
3. Prepare assets per checklist
4. Run: /csetup ${changeId}
`)
```

---

## Example Scenarios

### Scenario 1: Landing Page (First page)
```bash
User: /pageplan @prd.md @project_brief.md

Result:
- Found components: 0 (empty project)
- New shared: Navbar, Footer (will reuse later)
- New specific: HeroSection, FeatureGrid
- Content: Headlines, descriptions from PRD
```

### Scenario 2: Dashboard (Has existing components)
```bash
User: /pageplan @prd.md

Result:
- Found components: Navbar ✅, Footer ✅
- New shared: Sidebar (for dashboard/profile/admin)
- New specific: DashboardStats, ActivityTimeline
- Content: Dashboard-specific text
```

### Scenario 3: Backend API (No UI)
```bash
User: /pageplan

Result:
- Error: "This change doesn't involve UI work. Skip /pageplan."
- OR: Detect from proposal.md and auto-skip
```

---

## Error Handling

1. **No change ID found:**
   - Error: "No active change. Run after OpenSpec generates proposal."

2. **No @mentions and no proposal.md:**
   - Error: "No context files provided. Use: /pageplan @prd.md"

3. **No UI work detected:**
   - Warning: "This change appears to be backend/API work. /pageplan is for UI tasks."
   - Ask: "Continue anyway? (Y/N)"

4. **STYLE_GUIDE.md missing:**
   - Warning: "No STYLE_GUIDE.md found. Run /designsetup first for best results."
   - Continue: Use general design principles as fallback

---

## Implementation Priority

**Critical:**
- ✅ Read user-specified files only
- ✅ Search existing components
- ✅ Generate component reuse plan
- ✅ Generate content draft from PRD

**Nice to have:**
- Asset checklist detail level
- Auto-detect UI vs backend tasks
- Suggest component classification

---

## Integration with Multi-Agent Flow

```
tasks.md → /pageplan → page-plan.md → /csetup → /cdev
              ↓            ↓              ↓         ↓
           Search       User review   Phases   uxui-frontend
           components   & edit                  reads plan
                                                 skips search
```

**Agent behavior:**
- `uxui-frontend`: Reads page-plan.md in STEP 0, skips component search (STEP 3)
- `frontend`: May read page-plan.md for component locations
- Other agents: Ignore page-plan.md (not relevant)

---

**END OF COMMAND SPECIFICATION**
