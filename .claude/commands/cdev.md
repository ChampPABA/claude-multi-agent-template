---
name: Change Develop
description: Start/continue multi-agent development for a change
category: Multi-Agent
tags: [dev, orchestration, agents]
---

## Usage

```bash
/cdev {change-id}
/cdev {change-id} --continue
/cdev {change-id} --retry
```

## What It Does

Orchestrates agent execution for change development:
1. Read current phase from flags.json
2. Get agent assignment from phases.md
3. Invoke appropriate agent(s)
4. Update progress
5. Continue or pause for user action

## Steps

### Step 1: Load Change Context

```bash
# Check prerequisites
ls openspec/changes/{change-id}/.claude/flags.json
ls openspec/changes/{change-id}/.claude/phases.md
```

If not found:
```
❌ Change not set up
Run: /csetup {change-id}
```

### Step 2: Read Current Phase

```typescript
const flags = JSON.parse(Read('openspec/changes/{change-id}/.claude/flags.json'))
const currentPhase = flags.current_phase
const phaseData = flags.phases[currentPhase]

if (phaseData.status === 'completed') {
  // Move to next phase
  currentPhase = getNextPhase(flags)
}
```

### Step 3: Check Phase Type

```typescript
const agent = phaseData.agent

if (agent === 'user') {
  // Manual action required
  output(`🛑 Phase ${phaseData.phase_number} requires manual action`)
  output(`Instructions: ${getInstructions(currentPhase)}`)
  output(`When done: /cdev ${changeId} --continue`)
  return
}

if (agent.includes('+')) {
  // Multiple agents (parallel)
  agents = agent.split('+').map(a => a.trim())
  invokeMultipleAgents(agents, changeId, currentPhase)
} else {
  // Single agent
  invokeAgent(agent, changeId, currentPhase)
}
```

### Step 4: Invoke Agent with Retry & Validation

**This step now uses the enhanced agent-executor framework!**

See: `.claude/lib/agent-executor.md` for full implementation

**High-Level Flow:**

1. **Calculate Context Size** (for model selection)
2. **Select Model** (haiku vs sonnet based on complexity)
3. **Execute Agent with Retry** (automatic retry on failure)
4. **Validate Pre-Work** (enforce mandatory checklist)
5. **Validate Output Quality** (check completeness)
6. **Handle Errors** (retry or escalate)

**Implementation:**

```typescript
// Step 4: Invoke Agent with Retry & Validation

// 4.1: Build agent prompt (with design reference + best practices - v1.8.0)
function buildAgentPrompt(phase, changeContext) {
  let prompt = `
# Phase ${phase.phase_number}: ${phase.name}

## Change Context
${changeContext.proposal}

## Tasks
${changeContext.tasks}

${phase.instructions}
`

  // 🆕 v1.8.0: Add best-practices reference for ALL agents
  const bpDir = '.claude/contexts/domain/project/best-practices/'
  if (fileExists(bpDir)) {
    const bpFiles = listFiles(bpDir).filter(f => f.endsWith('.md') && f !== 'index.md')

    // Map agent type to relevant best-practices
    const agentBpMapping = {
      'uxui-frontend': ['react', 'nextjs', 'vue', 'tailwind'],
      'frontend': ['react', 'nextjs', 'vue', 'typescript'],
      'backend': ['express', 'fastapi', 'django', 'prisma', 'drizzle'],
      'database': ['prisma', 'drizzle', 'postgres', 'mongodb'],
      'test-debug': ['vitest', 'jest', 'playwright'],
      'integration': ['typescript'] // minimal
    }

    const relevantTechs = agentBpMapping[phase.agent] || []
    const relevantFiles = bpFiles.filter(f =>
      relevantTechs.some(tech => f.toLowerCase().includes(tech))
    )

    if (relevantFiles.length > 0) {
      prompt += `

---

## 📚 Best Practices (MANDATORY - STEP 0)

**YOU MUST READ these files before writing ANY code:**

${relevantFiles.map(f => `
### ${f.replace('.md', '')}
\`\`\`
Read: ${bpDir}${f}
\`\`\`
`).join('')}

**After reading, REPORT:**
\`\`\`
✅ Best Practices Loaded
   ${relevantFiles.map(f => `- ${f.replace('.md', '')} ✓`).join('\n   ')}
\`\`\`

**If you skip this, your work will be REJECTED!**

---
`
    }
  }

  // Add design reference for uxui-frontend agent (not full content!)
  if (phase.agent === 'uxui-frontend') {
    const tokensPath = 'design-system/STYLE_TOKENS.json'
    const styleGuidePath = 'design-system/STYLE_GUIDE.md'
    const hasTokens = fileExists(tokensPath)
    const hasStyleGuide = fileExists(styleGuidePath)

    if (hasTokens || hasStyleGuide) {
      prompt += `

---

## 🎨 Design System (MANDATORY Reading - STEP 0.5)

**Required Files (YOU MUST READ in STEP 0.5):**

${hasTokens ? `
1. **STYLE_TOKENS.json** (~500 tokens) ✅ REQUIRED
   \`\`\`
   Read: design-system/STYLE_TOKENS.json
   \`\`\`
   Contains: Colors, spacing, typography, shadows, borders, animations
` : ''}

${hasStyleGuide ? `
2. **STYLE_GUIDE.md** (selective sections ~2K tokens) 📖 OPTIONAL
   \`\`\`
   Read: design-system/STYLE_GUIDE.md
   \`\`\`
   Load only sections you need:
   - Section 6: Component Styles
   - Section 15: Layout Patterns
   - Section 16: Example Component Reference
` : ''}

**Critical Rules:**
- ❌ **NO** hardcoded colors: \`text-gray-500\`, \`#64748b\`
- ✅ **USE** theme tokens: \`text-foreground/70\`, \`bg-muted\`
- ❌ **NO** arbitrary spacing: \`p-5\`, \`gap-7\`
- ✅ **USE** spacing scale: \`p-4\`, \`p-6\`, \`gap-8\`
- ❌ **NO** inconsistent shadows: mixing \`shadow-sm\` and \`shadow-lg\`
- ✅ **USE** consistent patterns: all cards use \`shadow-md\`

**YOU MUST REPORT:**
\`\`\`
✅ Design System Loaded
   - STYLE_TOKENS.json ✓
   - Design Tokens Extracted: [list key tokens]
\`\`\`

If you skip this, your work will be REJECTED!

---
`
    } else {
      prompt += `

---

⚠️ **WARNING:** No design system found!
Using fallback: .claude/contexts/design/*.md (universal principles)

Run \`/designsetup\` to generate project-specific design system.

---
`
    }
  }

  return prompt
}

const prompt = buildAgentPrompt(phase, changeContext)

// 4.2: Execute agent with retry & validation
output(`\n🚀 Invoking ${phase.agent} agent (model: opus)...`)

const result = await executeAgentWithRetry(
  phase.agent,
  phase,
  changeContext,
  {
    max_retries: 2,
    retry_delay: 5000,
    timeout: 600000,  // 10 minutes
    validate_output: true
  }
)

// 4.3: Handle result
if (result.success) {
  output(`\n✅ Phase ${phase.phase_number} completed successfully!`)
  output(`⏱️ Execution time: ${(result.execution_time / 1000).toFixed(1)}s`)
  output(`🔄 Retries used: ${result.retries_used}`)
  output(`✅ Validation: ${result.validation_passed ? 'PASSED' : 'SKIPPED'}`)

  // Continue to Step 5: Post-Execution
} else {
  output(`\n❌ Phase ${phase.phase_number} failed`)
  output(`Error: ${result.error}`)
  output(`Retries used: ${result.retries_used}`)

  // Escalate to user
  const action = await escalateToUser(phase.agent, phase, result)

  switch (action) {
    case 'retry':
      output(`Retrying Phase ${phase.phase_number}...`)
      // Restart Step 4
      return executePhaseAgain(changeId, phase)

    case 'skip':
      output(`⚠️ Skipping Phase ${phase.phase_number}`)
      await markPhaseAsSkipped(changeId, phase, result.error)
      // Continue to next phase
      break

    case 'abort':
      output(`🛑 Workflow aborted`)
      output(`Resume with: /cdev ${changeId}`)
      return
  }
}
```

**Helper Functions Used:**

1. **buildAgentPrompt()**: See `.claude/lib/agent-executor.md`
2. **executeAgentWithRetry()**: See `.claude/lib/agent-executor.md`
3. **escalateToUser()**: See `.claude/lib/agent-executor.md`

**Model Strategy:**
- All agents use `model: opus` (fixed)
- Opus 4.5 is the latest Claude model with best performance
- Quality maintained through comprehensive validation framework

---

### Step 4.5: Validation Details

**Validation is handled automatically inside executeAgentWithRetry():**

See `.claude/lib/agent-executor.md` for complete validation flow including:
- Pre-work validation (checks required checklist items)
- Output quality checks (completion markers, code blocks, test results)
- Retry logic (max 2 retries with feedback)
- Escalation (user options on failure)

**Agent-specific validation requirements:**

See `.claude/contexts/patterns/validation-framework.md` for complete checklist per agent:
- uxui-frontend: Design Foundation, Box Thinking, Component Search, Design Tokens
- backend: Patterns Loaded, Endpoint Search, TDD Workflow (if required), Error Handling
- database: Schema Analysis, Migration Strategy, Existing Schemas Search
- frontend: API Contract Verification, State Management, Error Handling
- test-debug: Test Infrastructure, Coverage Targets, Test Plan
- integration: Contract Collection, Schema Validation, Data Flow Analysis

---

### Step 4.7: Validate Page Plan Compliance (uxui-frontend only)

**Only runs for uxui-frontend agent when page-plan.md exists:**

**Purpose:** Verify agent implemented ALL sections from page-plan.md, not a subset.

```typescript
// Check if page-plan.md exists
const pagePlanPath = `openspec/changes/${changeId}/page-plan.md`
const hasPagePlan = fileExists(pagePlanPath)

if (phase.agent === 'uxui-frontend' && hasPagePlan) {
  output(`\n🔍 Validating page-plan.md compliance...`)

  // Extract sections from page-plan.md Section 2 (Page Structure)
  const pagePlan = Read(pagePlanPath)
  const section2Match = pagePlan.match(/## 2\. Page Structure[\s\S]*?(?=## 3\.|## 2\.5|## 2\.6|$)/)

  if (section2Match) {
    // Count expected sections (extract component names from JSX)
    const componentMatches = section2Match[0].match(/<([A-Z]\w+)/g) || []
    const expectedComponents = componentMatches
      .map(m => m.replace('<', ''))
      .filter(name => name !== 'Layout' && name !== 'div') // Exclude wrappers

    const uniqueComponents = [...new Set(expectedComponents)] // Remove duplicates

    output(`\n📋 Page Plan Analysis:`)
    output(`   Expected sections: ${uniqueComponents.length}`)
    output(`   Components: ${uniqueComponents.join(', ')}`)

    // Prompt user to verify agent compliance
    output(`\n⚠️ VALIDATION REQUIRED:`)
    output(`\nDid the agent implement ALL ${uniqueComponents.length} sections?`)
    output(`\nPlease verify the implementation includes:`)
    uniqueComponents.forEach(c => output(`   - ${c}`))

    output(`\nOptions:`)
    output(`  [yes]   - All sections implemented ✓`)
    output(`  [retry] - Agent skipped sections, retry with strict enforcement`)
    output(`  [skip]  - Skip validation (not recommended)`)

    const answer = await askUser(`\nConfirm all sections implemented?`)

    if (answer === 'retry') {
      output(`\n🔄 Retrying phase with enhanced enforcement...`)
      output(`Agent will be explicitly instructed to implement all ${uniqueComponents.length} sections`)

      // Restart phase with enhanced prompt
      return executePhaseAgain(changeId, phase, {
        enforce_page_plan: true,
        required_sections: uniqueComponents
      })
    } else if (answer === 'skip') {
      warn(`\n⚠️ Skipping validation - proceed with caution`)
      warn(`   This may result in incomplete implementation`)
    } else {
      output(`\n✅ Page plan compliance confirmed`)
      output(`   All ${uniqueComponents.length} sections implemented`)
    }
  } else {
    warn(`\n⚠️ Could not parse page-plan.md Section 2`)
    warn(`   Skipping compliance validation`)
  }
} else {
  // Not uxui-frontend or no page-plan.md - skip validation
  output(`\nℹ️ Page plan validation: N/A (agent: ${phase.agent}, has plan: ${hasPagePlan})`)
}
```

**When to use:**
- ✅ Agent: uxui-frontend
- ✅ page-plan.md exists
- ✅ Phase completed successfully

**Common issues caught:**
- Agent implemented 5/10 sections (missing ProblemSection, ComparisonTable, etc.)
- Agent followed tasks.md ("4-5 components") instead of page-plan.md (10 sections)
- Agent skipped sections they thought were "optional"

**Remediation:**
- If validation fails → Retry with `enforce_page_plan: true`
- Agent will receive enhanced prompt with explicit section list
- Validation runs again after retry

---

### Step 5: Post-Execution (🆕 MANDATORY FLAGS UPDATE)

**⚠️ CRITICAL: Main Claude MUST update flags.json after EVERY phase completion**

See: `.claude/lib/flags-updater.md` for complete protocol

**Execution Order (MUST follow this sequence):**

```typescript
// 1. MANDATORY: Update flags.json
output(`\n🔄 Updating progress tracking...`)

// See flags-updater.md for updateFlagsAfterPhase() implementation
updateFlagsAfterPhase(changeId, currentPhase, agentResponse)

// This function:
// - Marks phase as completed
// - Records actual duration
// - Extracts files created/modified
// - Updates meta statistics (progress %, time remaining)
// - Moves current_phase to next phase
// - Writes back to flags.json
// - Reports progress to user

// 2. Read updated flags
const flagsPath = `openspec/changes/${changeId}/.claude/flags.json`
const flags = JSON.parse(Read(flagsPath))

// 3. Report progress to user
output(`\n📊 Progress Update:`)
output(`   ✅ ${flags.meta.completed_phases}/${flags.meta.total_phases} phases complete`)
output(`   📈 ${flags.meta.progress_percentage}% progress`)
output(`   ⏱️  ${formatDuration(flags.meta.total_actual_minutes)} spent`)
output(`   ⏱️  ${formatDuration(flags.meta.time_remaining_estimate)} remaining`)

// 4. Check next phase
if (flags.ready_to_archive) {
  // 🆕 v1.2.0: Verbose Summary Output (replaces documentation/report phases)
  output(`\n`)
  output(`╔════════════════════════════════════════════════════════════╗`)
  output(`║           ✅ CHANGE COMPLETED SUCCESSFULLY                 ║`)
  output(`╚════════════════════════════════════════════════════════════╝`)
  output(``)
  output(`📦 Change: ${changeId}`)
  output(`📋 Template: ${flags.template} (${flags.meta.total_phases} phases)`)
  output(``)
  output(`═══════════════════════════════════════════════════════════════`)
  output(`📊 EXECUTION SUMMARY`)
  output(`═══════════════════════════════════════════════════════════════`)
  output(``)
  output(`⏱️  Time:`)
  output(`   • Estimated: ${formatDuration(flags.meta.total_estimated_minutes)}`)
  output(`   • Actual:    ${formatDuration(flags.meta.total_actual_minutes)}`)
  output(`   • Variance:  ${calculateVariance(flags.meta)}`)
  output(``)
  output(`📈 Phases Completed: ${flags.meta.completed_phases}/${flags.meta.total_phases}`)

  // List all phases with status
  Object.entries(flags.phases).forEach(([phaseId, phase]) => {
    const status = phase.status === 'completed' ? '✅' :
                   phase.status === 'skipped' ? '⏭️' : '❌'
    const time = phase.actual_minutes ? `(${phase.actual_minutes}m)` : ''
    output(`   ${status} ${phase.phase_number}. ${phaseId} ${time}`)
  })

  output(``)
  output(`═══════════════════════════════════════════════════════════════`)
  output(`📁 FILES CREATED/MODIFIED`)
  output(`═══════════════════════════════════════════════════════════════`)

  // Collect all files from phase outputs
  const allFiles = collectFilesFromPhases(flags.phases)
  if (allFiles.created.length > 0) {
    output(``)
    output(`✨ Created (${allFiles.created.length}):`)
    allFiles.created.forEach(f => output(`   • ${f}`))
  }
  if (allFiles.modified.length > 0) {
    output(``)
    output(`📝 Modified (${allFiles.modified.length}):`)
    allFiles.modified.forEach(f => output(`   • ${f}`))
  }

  output(``)
  output(`═══════════════════════════════════════════════════════════════`)
  output(`🚀 NEXT STEPS`)
  output(`═══════════════════════════════════════════════════════════════`)
  output(``)
  output(`1. Review changes:  /cview ${changeId}`)
  output(`2. Test manually:   Verify the implementation works`)
  output(`3. Mark complete:   Update tasks.md (mark all [x])`)
  output(`4. Archive:         openspec archive ${changeId}`)
  output(``)
  output(`💡 Note: flags.json contains full execution history`)
  output(`   Path: openspec/changes/${changeId}/.claude/flags.json`)
  output(``)
} else {
  const nextPhase = flags.phases[flags.current_phase]

  output(`\n📍 Next: Phase ${nextPhase.phase_number}: ${flags.current_phase}`)
  output(`   Agent: ${nextPhase.agent}`)
  output(`   Estimated: ${nextPhase.estimated_minutes} min`)

  if (nextPhase.agent === 'user') {
    output('\n🛑 Next phase requires your action')
    output(`When done: /cdev ${changeId} --continue`)
  } else {
    output('\nContinue? (yes/no)')
  }
}
```

**Rules:**
- ✅ Main Claude updates flags.json (NOT sub-agent)
- ✅ Update happens IMMEDIATELY after sub-agent responds successfully
- ✅ Update happens BEFORE asking user to continue
- ✅ Progress is reported to user after EVERY update
- ✅ No exceptions - even if agent "says" it updated flags

**Common Mistake:**
```typescript
❌ WRONG:
Agent completes → Ask user to continue → (flags.json never updated)

✅ CORRECT:
Agent completes → Update flags.json → Report progress → Ask user to continue
```

---

## Example Session

```bash
$ /cdev CHANGE-003

✅ Reading change context...
📁 Change: CHANGE-003 Create Landing Page
📊 Template: frontend-only (11 phases)
📍 Current: Phase 1/11 Frontend Mockup

Invoking uxui-frontend agent...

[Agent executes Phase 1...]

✅ Phase 1 completed! (95 minutes)

📁 Files created:
   - src/app/page.tsx
   - src/components/landing/hero-section.tsx
   - src/components/landing/features-section.tsx
   - src/components/landing/cta-section.tsx

📍 Next: Phase 2 Accessibility Test (test-debug)

Continue? (yes/no)
> yes

[Continues...]

🛑 Phase 3 requires manual testing.
Test visual consistency using Chrome DevTools MCP.
When done: /cdev CHANGE-003 --continue

$ [User tests]

$ /cdev CHANGE-003 --continue

Updating flags → Phase 3 marked completed
📍 Next: Phase 4 Business Logic Validation
Continue? (yes/no)
> yes

[Continues until complete...]

✅ All phases completed! (11/11)
Ready to archive!
```

---

## Flags

- `--continue`: Skip to next phase (after manual action)
- `--retry`: Retry current phase if blocked

---

## Error Handling

**If phase blocked:**
```
❌ Phase blocked: {error}
Suggestions: {suggestions}
Retry: /cdev {change-id} --retry
```
