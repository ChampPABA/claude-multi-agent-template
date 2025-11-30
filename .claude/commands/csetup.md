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

### Step 2.5: Validate Design System & Page Plan (v2.0.0)

> **Updated v2.0.0:** Validate design files + read page-plan.md if exists

```typescript
// Detect if change involves UI/frontend work
const tasksContent = Read('openspec/changes/{change-id}/tasks.md')
const hasFrontend = tasksContent.toLowerCase().match(/(ui|component|page|frontend|design|responsive)/i)

let tokens = null
let pagePlan = null
let pageType = 'generic'

if (hasFrontend) {
  output(`\n🎨 UI work detected - validating design system...`)

  const tokensPath = 'design-system/tokens.json' // v2.0 tokens
  const styleGuidePath = 'design-system/STYLE_GUIDE.md'
  const pagePlanPath = `openspec/changes/${changeId}/page-plan.md`

  const hasTokens = fileExists(tokensPath)
  const hasStyleGuide = fileExists(styleGuidePath)
  const hasPagePlan = fileExists(pagePlanPath)

  // ========== LOAD tokens.json (v2.0 structure) ==========
  if (hasTokens) {
    tokens = JSON.parse(Read(tokensPath))
    output(`✅ tokens.json Loaded:`)
    output(`   - Style: ${tokens.style.name}`)
    output(`   - Theme: ${tokens.theme.name}`)
    output(`   - Animations: ${tokens.animations.enabled ? 'Enabled' : 'Disabled'}`)
  }

  // ========== LOAD page-plan.md (if exists) ==========
  if (hasPagePlan) {
    pagePlan = Read(pagePlanPath)
    output(`✅ page-plan.md Found`)

    // Extract page type from page-plan.md
    const pageTypeMatch = pagePlan.match(/Page Type:\*\*\s*(.*)/i)
    if (pageTypeMatch) {
      pageType = pageTypeMatch[1].trim().toLowerCase()
      output(`   - Page Type: ${pageType}`)
    }
  } else {
    output(`ℹ️ page-plan.md not found (optional)`)
    output(`   → Run /pageplan first for better component planning`)
  }

  if (!hasTokens || !hasStyleGuide) {
    warn(`
⚠️ WARNING: UI work detected but design system incomplete!

Found:
  ${hasStyleGuide ? '✅' : '❌'} STYLE_GUIDE.md
  ${hasTokens ? '✅' : '❌'} tokens.json
  ${hasPagePlan ? '✅' : '❌'} page-plan.md

This may result in:
  - Inconsistent colors (random hex codes)
  - Arbitrary spacing (p-5, gap-7)
  - Duplicate components

Recommendation:
  1. Run: /designsetup
  2. Run: /pageplan @prd.md (optional but recommended)
  3. Then: /csetup ${changeId}

Continue anyway? (yes/no)
    `)

    const answer = await askUser()
    if (answer === 'no') {
      return error('Setup cancelled. Run /designsetup first.')
    }
  } else {
    output(`✅ Design System Ready`)
    output(`   - STYLE_GUIDE.md ✓`)
    output(`   - tokens.json ✓`)
    if (hasPagePlan) output(`   - page-plan.md ✓`)
  }
}
```

---

### Step 2.7: Auto-Setup Best Practices (v1.8.0)

> **NEW:** Auto-detect tech stack and generate best-practices (replaces /psetup and /agentsetup)

```typescript
// 1. Detect tech stack from multiple sources
output(`\n🔍 Detecting Tech Stack...`)

// Source 1: package.json / requirements.txt (if exists)
let packageStack = []
if (fileExists('package.json')) {
  const pkg = JSON.parse(Read('package.json'))
  const deps = { ...pkg.dependencies, ...pkg.devDependencies }
  packageStack = Object.keys(deps).filter(d =>
    ['next', 'react', 'vue', 'express', 'fastapi', 'prisma', 'drizzle', 'vitest', 'jest'].some(k => d.includes(k))
  )
  output(`   📦 From package.json: ${packageStack.join(', ') || 'none'}`)
}

// Source 2: design.md (architecture section)
let designStack = []
const designPath = `openspec/changes/${changeId}/design.md`
if (fileExists(designPath)) {
  const designContent = Read(designPath)
  // Look for tech stack section
  const techMatch = designContent.match(/tech.*stack|architecture|framework/gi)
  if (techMatch) {
    designStack = extractTechFromText(designContent)
    output(`   📐 From design.md: ${designStack.join(', ') || 'none'}`)
  }
}

// Source 3: proposal.md + tasks.md (keywords)
const proposalContent = Read(`openspec/changes/${changeId}/proposal.md`)
const tasksContent = Read(`openspec/changes/${changeId}/tasks.md`)
const combined = (proposalContent + ' ' + tasksContent).toLowerCase()

const techDetection = {
  react: /\b(react|jsx|tsx|use[A-Z]\w+|usestate|useeffect)\b/i,
  nextjs: /\b(next\.?js|next js|app router|pages router)\b/i,
  vue: /\b(vue|vuex|pinia|nuxt)\b/i,
  express: /\b(express\.js|express js|expressjs)\b/i,
  fastapi: /\b(fastapi|fast api)\b/i,
  django: /\b(django)\b/i,
  prisma: /\b(prisma)\b/i,
  drizzle: /\b(drizzle)\b/i,
  postgres: /\b(postgres|postgresql)\b/i,
  mongodb: /\b(mongodb|mongoose)\b/i,
  tailwind: /\b(tailwind)\b/i,
  typescript: /\b(typescript)\b/i,
  vitest: /\b(vitest)\b/i,
  jest: /\b(jest)\b/i,
  playwright: /\b(playwright)\b/i
}

const proposalStack = []
for (const [tech, pattern] of Object.entries(techDetection)) {
  if (pattern.test(combined)) {
    proposalStack.push(tech)
  }
}
output(`   📝 From proposal/tasks: ${proposalStack.join(', ') || 'none'}`)

// Merge all sources (remove duplicates)
const detectedStack = [...new Set([...packageStack, ...designStack, ...proposalStack])]

// 2. If no stack detected, ask user
if (detectedStack.length === 0) {
  output(`\n⚠️ Could not auto-detect tech stack`)

  const answer = await askUserQuestion({
    questions: [{
      question: 'What tech stack will you use?',
      header: 'Stack',
      options: [
        { label: 'Next.js + React', description: 'Full-stack React framework' },
        { label: 'FastAPI + Python', description: 'Python async API' },
        { label: 'Express + Node', description: 'Node.js backend' },
        { label: 'Vue + Nuxt', description: 'Vue.js framework' }
      ],
      multiSelect: true
    }]
  })

  // Parse user selection into detectedStack
  detectedStack.push(...parseUserStackSelection(answer))
}

output(`\n✅ Final Tech Stack: ${detectedStack.join(', ')}`)

// 3. Check if best-practices already exist
const bpDir = '.claude/contexts/domain/project/best-practices/'
const existingBp = fileExists(bpDir) ? listFiles(bpDir) : []

const missingBp = detectedStack.filter(tech => {
  return !existingBp.some(f => f.toLowerCase().includes(tech.toLowerCase()))
})

// 4. Generate missing best-practices from Context7
if (missingBp.length > 0) {
  output(`\n📚 Generating Best Practices from Context7...`)

  // Create directory structure if needed
  if (!fileExists('.claude/contexts/domain/')) {
    mkdir('.claude/contexts/domain/project/best-practices/')
  }

  // Context7 library ID mapping
  const context7Ids = {
    react: '/facebook/react',
    nextjs: '/vercel/next.js',
    vue: '/vuejs/vue',
    express: '/expressjs/express',
    fastapi: '/fastapi/fastapi',
    prisma: '/prisma/prisma',
    drizzle: '/drizzle-team/drizzle-orm',
    vitest: '/vitest-dev/vitest',
    jest: '/jestjs/jest',
    playwright: '/microsoft/playwright',
    tailwind: '/tailwindlabs/tailwindcss'
  }

  for (const tech of missingBp) {
    const libraryId = context7Ids[tech.toLowerCase()]

    if (libraryId) {
      output(`   📖 Fetching ${tech} best practices...`)

      // Query Context7 for best practices
      const docs = await mcp__context7__get-library-docs({
        context7CompatibleLibraryID: libraryId,
        topic: 'best practices, common mistakes, anti-patterns, patterns',
        mode: 'code'
      })

      // Generate best-practices file
      const bpContent = generateBestPracticesFile(tech, docs)
      Write(`.claude/contexts/domain/project/best-practices/${tech}.md`, bpContent)

      output(`   ✅ ${tech}.md generated`)
    } else {
      output(`   ⚠️ ${tech} - no Context7 mapping, using universal patterns`)
    }
  }

  // Generate index.md
  generateBestPracticesIndex(detectedStack, changeId)
  output(`   ✅ index.md generated`)

  // Generate domain/index.md if not exists
  if (!fileExists('.claude/contexts/domain/index.md')) {
    generateDomainIndex('project', detectedStack)
    output(`   ✅ domain/index.md generated`)
  }

  output(`\n✅ Best Practices Setup Complete!`)
  output(`   Files: ${missingBp.length + 1} generated`)
  output(`   Location: .claude/contexts/domain/project/best-practices/`)
} else {
  output(`\n✅ Best Practices: Already configured (${existingBp.length} files)`)
}

// 5. Store detected stack in context.md (for agents to reference)
const stackForContext = {
  detected: detectedStack,
  bestPracticesPath: '.claude/contexts/domain/project/best-practices/',
  files: [...existingBp, ...missingBp.map(t => `${t}.md`)]
}
```

**Helper: generateBestPracticesFile()**
```typescript
function generateBestPracticesFile(tech: string, context7Docs: string): string {
  return `# ${tech} Best Practices

> **Source:** Context7 MCP
> **Generated:** ${new Date().toISOString().split('T')[0]}

---

## Best Practices

${extractDos(context7Docs)}

---

## Anti-Patterns to Avoid

${extractDonts(context7Docs)}

---

## 🎯 Quick Checklist

Before committing ${tech} code:
${extractChecklist(context7Docs)}

---

**Agents read this file in STEP 0 before implementation.**
`
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

---

### Step 3.5: Analyze Tasks (TaskMaster-style - v1.3.0)

> **NEW:** Enhanced task analysis with complexity, dependencies, risk assessment

**See:** `.claude/lib/task-analyzer.md` for complete analysis logic

```typescript
import { analyzeTask } from '.claude/lib/task-analyzer.md'

// Parse tasks from tasks.md
const tasks = parseTasksFromMd(tasksContent)
const analyzedTasks = []

output(`\n📊 Analyzing ${tasks.length} tasks...`)

for (const task of tasks) {
  // 1. Complexity scoring (1-10)
  const complexity = calculateComplexity(task)

  // 2. Dependency detection
  const dependencies = detectDependencies(task, tasks)

  // 3. Risk assessment
  const risk = assessRisk(task, complexity)
  risk.mitigation = generateMitigation(risk, task)

  // 4. Research requirements
  const research = detectResearchNeeds(task)

  // 5. Subtask breakdown (if needed)
  const needsBreakdown = needsSubtaskBreakdown(task, complexity)
  const subtasks = needsBreakdown ? generateSubtasks(task) : []

  // 6. Priority ranking
  const priority = calculatePriority(task, { complexity, dependencies, risk })

  analyzedTasks.push({
    ...task,
    complexity: {
      score: complexity,
      level: getComplexityLevel(complexity),
      factors: explainComplexity(task, complexity)
    },
    dependencies,
    risk: {
      ...risk,
      mitigation
    },
    research,
    subtasks,
    priority: {
      score: priority,
      label: getPriorityLabel(priority),
      reason: explainPriority(task, priority)
    },
    estimatedTime: {
      original: task.estimatedTime,
      adjusted: adjustTimeForComplexity(task.estimatedTime, complexity, risk),
      buffer: calculateBuffer(complexity, risk)
    }
  })
}

// Sort by priority (CRITICAL → HIGH → MEDIUM → LOW)
analyzedTasks.sort((a, b) => b.priority.score - a.priority.score)

// Calculate testing strategy stats (NEW in v1.4.0)
const incrementalTasks = analyzedTasks.filter(t => t.testingStrategy?.type === 'incremental')
const totalMilestones = incrementalTasks.reduce((sum, t) => sum + (t.testingStrategy?.milestones?.length || 0), 0)

// Store for phases.md generation
const taskAnalysis = {
  tasks: analyzedTasks,
  summary: {
    total: analyzedTasks.length,
    priority: {
      critical: analyzedTasks.filter(t => t.priority.label === 'CRITICAL').length,
      high: analyzedTasks.filter(t => t.priority.label === 'HIGH').length,
      medium: analyzedTasks.filter(t => t.priority.label === 'MEDIUM').length,
      low: analyzedTasks.filter(t => t.priority.label === 'LOW').length
    },
    risk: {
      high: analyzedTasks.filter(t => t.risk.level === 'HIGH').length,
      medium: analyzedTasks.filter(t => t.risk.level === 'MEDIUM').length,
      low: analyzedTasks.filter(t => t.risk.level === 'LOW').length
    },
    researchRequired: analyzedTasks.filter(t => t.research?.required).length,
    subtasksExpanded: analyzedTasks.filter(t => t.subtasks.length > 0).length,
    averageComplexity: (analyzedTasks.reduce((sum, t) => sum + t.complexity.score, 0) / analyzedTasks.length).toFixed(1),
    // NEW: Incremental Testing stats
    incrementalTesting: incrementalTasks.length,
    standardTesting: analyzedTasks.length - incrementalTasks.length,
    totalMilestones: totalMilestones
  }
}
```

**Output analysis report:**
```
✅ Task Analysis Complete

📊 Summary:
   Total tasks: 8
   Expanded to: 15 subtasks

📈 Priority Distribution:
   🔴 CRITICAL: 2 tasks (Login, Payment)
   🟠 HIGH: 3 tasks (User Profile, API endpoints)
   🟡 MEDIUM: 2 tasks (Email notifications)
   🟢 LOW: 1 task (Documentation)

⚠️ Risk Assessment:
   🔴 HIGH risk: 2 tasks (Payment integration, Auth system)
      → Mitigation: TDD required, security checklist
   ⚠️ MEDIUM risk: 3 tasks
   ✅ LOW risk: 3 tasks

🔄 Testing Strategy (NEW in v1.4.0):
   🔄 Incremental: 3 tasks (11 milestones total)
      → Payment integration (4 milestones)
      → Auth system (4 milestones)
      → User data migration (3 milestones)
   ▶️ Standard: 5 tasks

🔬 Research Required: 2 tasks
   - React Query v5 migration (15 min)
   - Stripe payment best practices (15 min)

📦 Subtask Breakdown: 3 tasks expanded
   - Login system → 3 subtasks (UI, API, Integration)
   - User CRUD → 4 subtasks (Create, Read, Update, Delete)

⏱️ Time Estimates:
   Original: 6.5 hours
   Adjusted: 9.2 hours (+41% buffer for complexity/risk)
   Average complexity: 5.8/10
```

---

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

**🆕 ENHANCED v1.3.0: Inject Task Analysis Metadata**

```typescript
// Add research phases (if needed)
const researchPhases = []
analyzedTasks.filter(t => t.research?.required).forEach((task, i) => {
  researchPhases.push({
    id: `research-${i + 1}`,
    phaseNumber: `0.${i + 1}`, // Before implementation
    name: `Research: ${task.research.category}`,
    agent: 'integration',
    estimatedMinutes: task.research.estimatedTime,
    task: task,
    queries: task.research.queries,
    reason: task.research.reason
  })
})

// Merge with existing phases (research goes first)
const allPhases = [...researchPhases, ...phaseSections]
```

**Generate enhanced phases.md:**
```markdown
# Agent Workflow: {CHANGE_ID} {Change Title}

> **Auto-generated by `/csetup {change-id}`**
> **Template:** {template-name} ({total-phases} phases)
> **Reason:** {detection-reason}
> **Source:** proposal.md + tasks.md (TaskMaster-analyzed)
> **Last updated:** {current-datetime}

---

## 📊 Task Analysis Summary (v1.4.0 - Incremental Testing)

**Analyzed Tasks:** {taskAnalysis.summary.total}
**Average Complexity:** {taskAnalysis.summary.averageComplexity}/10

**Priority Distribution:**
- 🔴 CRITICAL: {taskAnalysis.summary.priority.critical}
- 🟠 HIGH: {taskAnalysis.summary.priority.high}
- 🟡 MEDIUM: {taskAnalysis.summary.priority.medium}
- 🟢 LOW: {taskAnalysis.summary.priority.low}

**Risk Assessment:**
- 🔴 HIGH risk: {taskAnalysis.summary.risk.high} tasks
- ⚠️ MEDIUM risk: {taskAnalysis.summary.risk.medium} tasks
- ✅ LOW risk: {taskAnalysis.summary.risk.low} tasks

**Testing Strategy:** (NEW in v1.4.0)
- 🔄 Incremental: {taskAnalysis.summary.incrementalTesting} tasks ({taskAnalysis.summary.totalMilestones} milestones)
- ▶️ Standard: {taskAnalysis.summary.standardTesting} tasks

**Research Phases:** {taskAnalysis.summary.researchRequired} added
**Subtasks Expanded:** {taskAnalysis.summary.subtasksExpanded} tasks

**Time Estimates:**
- Original: {calculateOriginalTime(analyzedTasks)} hours
- Adjusted: {calculateAdjustedTime(analyzedTasks)} hours
- Buffer: +{calculateTotalBuffer(analyzedTasks)}%

---

## 📊 Workflow Overview

| Phase | Agent | Type | Est. Time | Status |
|-------|-------|------|-----------|--------|
{phase-table-rows}

**Total estimated time:** ~{total-hours} hours

**Phases skipped (not needed for {template-name}):**
{skipped-phases-list}

---

---

## 🔬 Research Phases (if applicable)

${researchPhases.map((phase, i) => `
### Phase 0.${i + 1}: ${phase.name}

**Agent:** integration
**Estimated Time:** ${phase.estimatedMinutes} min
**Type:** Research

**Reason:** ${phase.reason}

**Research Queries:**
${phase.queries.map(q => `- ${q}`).join('\n')}

**Instructions:**
1. Use WebSearch or Context7 to gather information
2. Summarize findings in research notes
3. Update task context with relevant insights
4. Proceed to implementation with informed decisions

---
`).join('')}

---

## 🚀 Implementation Phases

${allPhases.map((phaseSection, index) => {
  // Find matching task from analyzedTasks
  const matchingTask = analyzedTasks.find(t =>
    phaseSection.toLowerCase().includes(t.description.toLowerCase().split(' ')[0])
  )

  let metadata = ''
  let milestonesSection = ''

  if (matchingTask) {
    // Standard metadata
    metadata = `
**Task Metadata (TaskMaster Analysis):**
- **Complexity:** ${matchingTask.complexity.score}/10 (${matchingTask.complexity.level})
  - Factors: ${matchingTask.complexity.factors.join(', ')}
- **Priority:** ${matchingTask.priority.label} (${matchingTask.priority.score}/100)
  - ${matchingTask.priority.reason}
- **Risk:** ${matchingTask.risk.level}
${matchingTask.risk.mitigation.length > 0 ? `  - Mitigation:\n${matchingTask.risk.mitigation.map(m => `    - ${m}`).join('\n')}` : ''}
- **Dependencies:**
  - Blocked by: ${matchingTask.dependencies.blockedBy.length > 0 ? matchingTask.dependencies.blockedBy.join(', ') : 'None'}
  - Blocks: ${matchingTask.dependencies.blocks.length > 0 ? matchingTask.dependencies.blocks.join(', ') : 'None'}
  - Can parallelize with: ${matchingTask.dependencies.parallelizable.length > 0 ? matchingTask.dependencies.parallelizable.slice(0, 3).join(', ') : 'None'}
- **Time Estimate:** ${matchingTask.estimatedTime.original} min → ${matchingTask.estimatedTime.adjusted} min (+${matchingTask.estimatedTime.buffer}% buffer)

${matchingTask.subtasks.length > 0 ? `**Subtasks:**\n${matchingTask.subtasks.map(st => `  - ${st.id}: ${st.description} (${st.estimatedTime} min)`).join('\n')}\n` : ''}
`

    // NEW: Incremental Testing Milestones (v1.4.0)
    if (matchingTask.testingStrategy?.type === 'incremental' && matchingTask.testingStrategy.milestones) {
      metadata += `
**Testing Strategy:** 🔄 INCREMENTAL
- **Reason:** ${matchingTask.testingStrategy.reason}
- **Total Milestones:** ${matchingTask.testingStrategy.milestones.length}

`

      // Generate milestone subsections
      milestonesSection = matchingTask.testingStrategy.milestones.map(milestone => `
#### Milestone ${milestone.id}/${matchingTask.testingStrategy.milestones.length}: ${milestone.name}

**Test Scope:** ${milestone.testScope}
**Estimated Time:** ${milestone.estimatedTime} min
**Retry Limit:** ${milestone.retryLimit} attempts

**Exit Criteria:**
${milestone.exitCriteria.map(criterion => `- [ ] ${criterion}`).join('\n')}

**Instructions for Agent:**
1. **Implement:** ${milestone.name}
2. **Test:** ${milestone.testScope}
3. **Validate:** Check ALL exit criteria above
4. **Report results in this format:**

\`\`\`
## Milestone ${milestone.id} Results

**Implementation Summary:**
[Brief description of what was implemented]

**Test Results:**
${milestone.exitCriteria.map(criterion => `- [ ] ${criterion} - [PASS/FAIL] - [Brief explanation]`).join('\n')}

**Issues Found (if any):**
[List any issues encountered]

**Conclusion:**
[PASS → Ready for Milestone ${milestone.id + 1}]
[FAIL → Need to fix [X] before retry]
\`\`\`

5. **IF FAILED:** Debug issues → Retry (max ${milestone.retryLimit} attempts)
6. **IF ALL RETRIES FAIL:** Escalate to Main Claude for guidance
7. **IF PASSED:** Proceed to ${milestone.id < matchingTask.testingStrategy.milestones.length ? `Milestone ${milestone.id + 1}` : 'next phase'}

---
`).join('\n')
    } else if (matchingTask.testingStrategy?.type === 'standard') {
      metadata += `
**Testing Strategy:** ▶️ STANDARD
- **Reason:** ${matchingTask.testingStrategy.reason}

`
    }
  }

  return `${phaseSection}\n${metadata}${milestonesSection}`
}).join('\n---\n\n')}

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

// 🆕 Load design info (if UI work) - v2.0.0
let designInfo = ''
if (hasFrontend && tokens) {
  designInfo = `
## 🎨 Design System (v2.0.0)

**Design Files:**
- tokens.json: \`design-system/tokens.json\` (~800 tokens)
- patterns/: \`design-system/patterns/*.md\` (selective loading)
- STYLE_GUIDE.md: \`design-system/STYLE_GUIDE.md\` (human-readable, ~150 lines)
${pagePlan ? `- page-plan.md: \`openspec/changes/${changeId}/page-plan.md\` ✅` : ''}

**Style Direction:**
- Style: ${tokens.style.name}
- Theme: ${tokens.theme.name}
- Feel: ${tokens.style.feel}

**Design Tokens:**
- Primary Color: ${tokens.colors.primary.DEFAULT}
- Component Library: ${tokens.component_library.name}
- Spacing Scale: ${tokens.spacing.scale.join(', ')}px
- Animations: ${tokens.animations.enabled ? 'Enabled' : 'Disabled'}

**Theme & Decorations:**
${pageType.includes('landing') || pageType.includes('marketing') ? `
- Decorations: ✅ Enabled
- USE: ${tokens.theme.decorative_elements.use.slice(0, 3).join(', ')}
- AVOID: ${tokens.theme.decorative_elements.avoid.slice(0, 2).join(', ') || '(none)'}
- Scroll Animations: ✅ Enabled
` : `
- Decorations: ❌ Disabled (${pageType} page)
- Scroll Animations: ❌ Disabled
`}

**Pattern Files to Load:**
${pageType.includes('landing') || pageType.includes('marketing') ?
`- patterns/buttons.md ✅
- patterns/cards.md ✅
- patterns/scroll-animations.md ✅
- patterns/decorations.md ✅` :
pageType.includes('auth') ?
`- patterns/buttons.md ✅
- patterns/forms.md ✅` :
`- patterns/buttons.md ✅
- patterns/cards.md ✅
- patterns/forms.md ✅`}

**Agent Loading (STEP 0.5 for uxui-frontend):**
1. Read: tokens.json (~800 tokens)
2. Read: page-plan.md (if exists)
3. Load patterns selectively based on page type
4. Report: Design tokens + page type extracted

**Style Guidelines:**

| Instead of | Use | WHY |
|------------|-----|-----|
| text-gray-500 | text-foreground/70 | Theme-aware |
| p-5 | p-4 or p-6 | Spacing scale |
| ${pageType.includes('landing') ? '✅ Apply decorations from theme' : '❌ Skip decorations for this page type'} | | |
`
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
   - Total phases: 9
   - Estimated time: 2h 50m
   - Reason: Frontend work detected, no backend/API needed

Generating workflow...
✓ Generated phases.md (115 lines, 9 phases)
✓ Generated flags.json (initialized all phases as pending)
✓ Generated context.md (change context with core tech references)

✅ Change setup complete!

📦 Change: CHANGE-003
📋 Template: frontend-only (9 phases)
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

⏱️ Total estimated time: ~2h 50m

💡 Note: Documentation/Report phases removed in v1.2.0
   → Verbose summary output in terminal when change completes
   → flags.json contains full execution history

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
