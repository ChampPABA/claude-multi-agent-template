---
name: Change Setup
description: Setup change context by analyzing tasks and generating agent workflow
category: Multi-Agent
tags: [setup, change, multi-agent]
---

## Usage

```bash
/csetup {change-id}
```

## What It Does

Analyzes OpenSpec files (proposal, tasks, design) and:
1. Detects task types (frontend, backend, API, script, etc.)
2. Selects appropriate phase template
3. Generates `.claude/phases.md` (agent workflow)
4. Generates `.claude/flags.json` (progress tracking)
5. Generates `.claude/context.md` (change-specific tech)

## Steps

### Step 1: Check Prerequisites

```bash
# Check if change exists
ls openspec/changes/{change-id}/
```

If not found:
```
❌ Error: Change {change-id} not found
Please create the change with OpenSpec first
```

### Step 2: Read OpenSpec Files

Read in order:
1. `openspec/changes/{change-id}/proposal.md`
2. `openspec/changes/{change-id}/tasks.md`
3. `openspec/changes/{change-id}/design.md` (if exists)

---

### Step 2.5: Validate Design System (Context Optimization v1.2.0)

> **New:** Validate design files exist for UI work

```typescript
// Detect if change involves UI/frontend work
const tasksContent = Read('openspec/changes/{change-id}/tasks.md')
const hasFrontend = tasksContent.toLowerCase().match(/(ui|component|page|frontend|design|responsive)/i)

if (hasFrontend) {
  output(`\n🎨 UI work detected - validating design system...`)

  const tokensPath = 'design-system/STYLE_TOKENS.json'
  const styleGuidePath = 'design-system/STYLE_GUIDE.md'

  const hasTokens = fileExists(tokensPath)
  const hasStyleGuide = fileExists(styleGuidePath)

  if (!hasTokens || !hasStyleGuide) {
    warn(`
⚠️ WARNING: UI work detected but design system incomplete!

Found:
  ${hasStyleGuide ? '✅' : '❌'} STYLE_GUIDE.md
  ${hasTokens ? '✅' : '❌'} STYLE_TOKENS.json

This may result in:
  - Inconsistent colors (random hex codes)
  - Arbitrary spacing (p-5, gap-7)
  - Duplicate components

Recommendation:
  1. Run: /designsetup
  2. Then: /csetup ${changeId}

Continue anyway? (yes/no)
    `)

    const answer = await askUser()
    if (answer === 'no') {
      return error('Setup cancelled. Run /designsetup first.')
    }
  } else {
    output(`✅ Design System Ready`)
    output(`   - STYLE_GUIDE.md ✓`)
    output(`   - STYLE_TOKENS.json ✓`)
  }
}
```

---

### Step 3: Analyze Tasks

**Parse tasks.md content and detect keywords:**

```typescript
// Load detection keywords
const keywords = Read('.claude/templates/phase-templates.json').detection_keywords

// Analyze tasks.md
const tasksContent = Read('openspec/changes/{change-id}/tasks.md')
const lower = tasksContent.toLowerCase()

// Detect categories
const hasFrontend = keywords.frontend.some(kw => lower.includes(kw))
const hasBackend = keywords.backend.some(kw => lower.includes(kw))
const hasDatabase = keywords.database.some(kw => lower.includes(kw))
const hasAPI = keywords.api_integration.some(kw => lower.includes(kw))
const hasScript = keywords.script.some(kw => lower.includes(kw))
const isBugFix = keywords.bug_fix.some(kw => lower.includes(kw))
const isRefactor = keywords.refactor.some(kw => lower.includes(kw))
```

**Output detection results:**
```
🔍 Analyzing tasks.md...

Detected:
✅ Frontend work: YES (found: component, ui, responsive)
✅ Backend work: YES (found: api, endpoint)
✅ Database work: YES (found: database, schema)
❌ Script/CLI: NO
❌ Bug fix: NO
❌ Refactor: NO

Change type: feature
```

### Step 4: Select Template

**Selection logic:**
```typescript
let template: string

if (isBugFix) {
  template = 'bug-fix'
} else if (isRefactor) {
  template = 'refactor'
} else if (hasScript && !hasFrontend && !hasBackend) {
  template = 'script-only'
} else if (hasFrontend && hasBackend) {
  template = 'full-stack'
} else if (hasFrontend && !hasBackend && !hasAPI) {
  template = 'frontend-only'
} else if (hasBackend && !hasFrontend) {
  template = 'backend-only'
} else {
  // Default to safest option
  template = 'full-stack'
}
```

**Output:**
```
📋 Template selected: full-stack
   - Total phases: 19
   - Estimated time: 7 hours
   - Reason: Frontend + Backend + Database detected
```

### Step 5: Generate phases.md

**Load template and phase sections:**
```typescript
// Load template
const templateData = Read('.claude/templates/phase-templates.json').templates[template]

// Load phase sections
const phaseSections = templateData.phases.map(phaseId => {
  return Read(`.claude/templates/phases-sections/${phaseId}.md`)
})

// Extract task IDs from tasks.md
const taskIds = extractTaskIds(tasksContent) // e.g., ["1.1", "1.2", "2.1", ...]
```

**🆕 ENHANCED: Add TDD Classification**

For each phase, add TDD metadata:
1. Extract task description from tasks.md
2. Estimate complexity (time + keywords + length)
3. Classify TDD requirement (phase type + keywords + complexity)
4. Add TDD metadata to phase: `tdd_required`, `tdd_reason`, `tdd_workflow`

**See:** `.claude/lib/tdd-classifier.md` for complete classification logic

**Quick Reference:**
- Backend auth/payment → TDD required (critical logic)
- Simple CRUD read → test-alongside OK
- Multi-step wizard UI → TDD required (complex state machine)
- Database schema → no TDD needed (declarative)

---

**Generate phases.md:**
```markdown
# Agent Workflow: {CHANGE_ID} {Change Title}

> **Auto-generated by `/csetup {change-id}`**
> **Template:** {template-name} ({total-phases} phases)
> **Reason:** {detection-reason}
> **Source:** proposal.md + tasks.md + design.md
> **Last updated:** {current-datetime}

---

## 📊 Workflow Overview

| Phase | Agent | Type | Est. Time | Status |
|-------|-------|------|-----------|--------|
{phase-table-rows}

**Total estimated time:** ~{total-hours} hours

**Phases skipped (not needed for {template-name}):**
{skipped-phases-list}

---

{phase-section-1}

---

{phase-section-2}

---

... (all phases)

---

**End of phases.md**
```

Write to: `openspec/changes/{change-id}/.claude/phases.md`

### Step 6: Generate flags.json

**Load template and populate:**
```typescript
// Load template
const flagsTemplate = Read('.claude/templates/flags-template.json')

// Populate with change data
const flags = {
  ...flagsTemplate,
  change_id: changeId,
  change_type: changeType, // from proposal or detection
  template: templateName,
  created_at: new Date().toISOString(),
  updated_at: new Date().toISOString(),
  current_phase: templateData.phases[0], // First phase
  meta: {
    ...flagsTemplate.meta,
    total_phases: templateData.total_phases,
    pending_phases: templateData.total_phases,
    total_estimated_minutes: templateData.estimated_minutes
  }
}

// Initialize all phases as pending
templateData.phases.forEach((phaseId, index) => {
  flags.phases[phaseId] = {
    phase_number: index + 1,
    status: 'pending',
    agent: getAgentForPhase(phaseId),
    estimated_minutes: getEstimatedMinutes(phaseId)
  }
})
```

Write to: `openspec/changes/{change-id}/.claude/flags.json`

### Step 7: Generate context.md

**Load template and populate:**
```typescript
// Load template
let contextTemplate = Read('.claude/templates/context-template.md')

// Load project tech stack
const projectTech = Read('.claude/contexts/domain/project/tech-stack.md')

// Detect additional tech from proposal/tasks
const additionalTech = detectAdditionalTech(proposalContent, tasksContent)

// 🆕 Load design info (if UI work)
let designInfo = ''
if (hasFrontend) {
  const tokensPath = 'design-system/STYLE_TOKENS.json'

  if (fileExists(tokensPath)) {
    const tokens = JSON.parse(Read(tokensPath))

    designInfo = `
## 🎨 Design System (Context Optimization v1.2.0)

**Design Files (Token-Efficient):**
- STYLE_TOKENS.json: \`design-system/STYLE_TOKENS.json\` (~500 tokens)
- STYLE_GUIDE.md: \`design-system/STYLE_GUIDE.md\` (~5000 tokens, load selectively)

**Key Design Tokens:**
- Primary Color: ${tokens.tokens.colors.primary.DEFAULT}
- Component Library: ${tokens.component_library.name}
- Spacing Scale: ${tokens.tokens.spacing.scale.join(', ')}px
- Shadows: ${Object.keys(tokens.tokens.shadows).slice(0, 5).join(', ')}

**Agent Loading (STEP 0.5 for uxui-frontend):**
1. Read: STYLE_TOKENS.json (~500 tokens) ✅
2. Optional: STYLE_GUIDE.md (selective sections ~2K tokens)
3. Report: Design tokens extracted

**Critical Rules:**
- ❌ NO hardcoded colors (text-gray-500)
- ✅ USE theme tokens (text-foreground/70)
- ❌ NO arbitrary spacing (p-5)
- ✅ USE spacing scale (p-4, p-6)
`
  }
}

// Replace placeholders
contextTemplate = contextTemplate
  .replace('{CHANGE_ID}', changeId)
  .replace('{CHANGE_TITLE}', extractTitle(proposalContent))
  .replace('{CHANGE_TYPE}', changeType)
  .replace('{CURRENT_PHASE_NUMBER}', '1')
  .replace('{TOTAL_PHASES}', templateData.total_phases)
  .replace('{CREATED_DATE}', new Date().toISOString())
  .replace('{CORE_TECH_LIST}', generateCoreTechList(projectTech))
  .replace('{ADDITIONAL_TECH_LIST}', generateAdditionalTechList(additionalTech))
  .replace('{CURRENT_PHASE}', templateData.phases[0])
  .replace('{STATUS}', 'pending')
  .replace('{DESIGN_SYSTEM}', designInfo) // 🆕 Add design section
```

Write to: `openspec/changes/{change-id}/.claude/context.md`

### Step 8: Output Summary

```
✅ Change setup complete!

📦 Change: {change-id}
📋 Template: {template-name} ({total-phases} phases)
🛠️ Detected: {detected-categories}

📁 Files created:
✓ openspec/changes/{change-id}/.claude/phases.md
✓ openspec/changes/{change-id}/.claude/flags.json
✓ openspec/changes/{change-id}/.claude/context.md

📊 Workflow:
   Phase 1: {first-phase-name} ({agent} agent, {estimated} min)
   ...
   Phase {n}: {last-phase-name}

⏱️ Total estimated time: ~{hours}h {minutes}m

🚀 Ready to start development!

Next steps:
1. Review generated workflow: openspec/changes/{change-id}/.claude/phases.md
2. Start development: /cdev {change-id}
3. View progress: /cview {change-id}
```

---

## Helper Functions

### extractTaskIds()
```typescript
// Extract task IDs like "1.1", "1.2", "2.1" from tasks.md
function extractTaskIds(content: string): string[] {
  const regex = /-\s*\[\s*\]\s*(\d+\.\d+)/g
  const matches = [...content.matchAll(regex)]
  return matches.map(m => m[1])
}
```

### getAgentForPhase()
```typescript
function getAgentForPhase(phaseId: string): string {
  const agentMap = {
    'frontend-mockup': 'uxui-frontend',
    'accessibility-test': 'test-debug',
    'manual-ux-test': 'user',
    'business-logic-validation': 'integration',
    'user-approval': 'user',
    'api-design': 'integration',
    'backend': 'backend',
    'database': 'database',
    'backend-tests': 'test-debug',
    'contract-backend': 'integration',
    'frontend-integration': 'frontend',
    'contract-frontend': 'integration',
    'component-tests': 'test-debug',
    'responsive-test': 'user',
    'e2e-tests': 'test-debug',
    'manual-flow-test': 'user',
    'refactor': 'test-debug',
    'regression-tests': 'test-debug',
    'test-coverage': 'test-debug',
    'documentation': 'integration',
    'report': 'integration',
    'script-implementation': 'backend',
    'automated-tests': 'test-debug',
    'manual-testing': 'user',
    'fix-implementation': 'varies',
    'unit-tests': 'test-debug',
    'manual-verification': 'user',
    'refactor-implementation': 'test-debug'
  }
  return agentMap[phaseId] || 'integration'
}
```

### detectAdditionalTech()
```typescript
// Detect change-specific tech (Stripe, WebSocket, etc.)
function detectAdditionalTech(proposal: string, tasks: string): string[] {
  const combined = proposal + ' ' + tasks
  const tech = []

  if (combined.includes('stripe') || combined.includes('payment')) tech.push('Stripe')
  if (combined.includes('websocket') || combined.includes('realtime')) tech.push('WebSocket')
  if (combined.includes('redis')) tech.push('Redis')
  if (combined.includes('s3') || combined.includes('storage')) tech.push('S3/Storage')
  // Add more as needed

  return tech
}
```

---

## Error Handling

**If tasks.md is missing or empty:**
```
❌ Error: tasks.md not found or empty
Please ensure the change has been properly initialized with OpenSpec
```

**If template selection is ambiguous:**
```
⚠️ Warning: Could not confidently detect change type
Defaulting to 'full-stack' template (safest option)

If this is incorrect, please:
1. Add more descriptive keywords to tasks.md
2. Or manually specify template (future feature)
```

---

## Example Session

```bash
$ /csetup CHANGE-003

🔍 Reading OpenSpec files...
✓ Read: proposal.md (2.3 KB)
✓ Read: tasks.md (1.8 KB)
✓ Read: design.md (not found - optional)

🔍 Analyzing tasks.md...

Detected:
✅ Frontend work: YES (found: component, page, responsive, ui)
❌ Backend work: NO
❌ Database work: NO
❌ API integration: NO
❌ Script/CLI: NO

Change type: feature

📋 Template selected: frontend-only
   - Total phases: 11
   - Estimated time: 3.25 hours
   - Reason: Frontend work detected, no backend/API needed

Generating workflow...
✓ Generated phases.md (127 lines, 11 phases)
✓ Generated flags.json (initialized all phases as pending)
✓ Generated context.md (change context with core tech references)

✅ Change setup complete!

📦 Change: CHANGE-003
📋 Template: frontend-only (11 phases)
🛠️ Detected: Frontend

📁 Files created:
✓ openspec/changes/CHANGE-003/.claude/phases.md
✓ openspec/changes/CHANGE-003/.claude/flags.json
✓ openspec/changes/CHANGE-003/.claude/context.md

📊 Workflow:
   Phase 1: Frontend Mockup (uxui-frontend, 90 min)
   Phase 2: Accessibility Test (test-debug, 10 min)
   Phase 3: Manual UX Test (user, 15 min)
   Phase 4: Business Logic Validation (integration, 10 min)
   Phase 5: User Approval (user, 5 min)
   Phase 6: Component Tests (test-debug, 20 min)
   Phase 7: Responsive Test (user, 15 min)
   Phase 8: Refactor (test-debug, 20 min)
   Phase 9: Test Coverage (test-debug, 5 min)
   Phase 10: Documentation (integration, 15 min)
   Phase 11: Final Report (integration, 10 min)

⏱️ Total estimated time: ~3h 15m

🚀 Ready to start development!

Next steps:
1. Review workflow: openspec/changes/CHANGE-003/.claude/phases.md
2. Start development: /cdev CHANGE-003
3. View progress: /cview CHANGE-003
```

---

## Important Notes

1. **Re-run safe:** Running `/csetup` again will **overwrite** existing files. Use with caution.
2. **Manual adjustments:** You can manually edit phases.md after generation if needed
3. **Template accuracy:** Detection is heuristic-based. Review generated workflow before starting.
4. **Context7 integration:** Additional tech detection can trigger Context7 queries (future enhancement)
