# Task Analyzer v2.0 - Template-Free Architecture

> **Single Source of Truth: tasks.md → phases.md**
> **Version:** 2.0.0 (Template-Free, AI-Driven)
> **Used by:** `/csetup` command

---

## 🎯 Core Philosophy

```
tasks.md (WHAT to build)
    ↓
Task Analyzer (AI-driven analysis)
    ↓
phases.md (HOW to build incrementally)
```

**Key Principles:**
1. **tasks.md is the Single Source of Truth** - Every task from tasks.md MUST appear in phases.md
2. **AI Decision, Not Keywords** - Claude analyzes context and decides (no hardcoded keyword matching)
3. **Auto-Add Best Practices** - No warnings, just add what's needed automatically
4. **Incremental by Default** - Complex tasks get milestones automatically

---

## 📋 Analysis Pipeline

### Step 1: Parse All Tasks

**Purpose:** Extract EVERY task from tasks.md without filtering

```typescript
function parseAllTasks(tasksContent: string): Task[] {
  const tasks: Task[] = []

  // Parse markdown structure
  // - Preserve hierarchy (Phase 1 > 1.1 > 1.1.1)
  // - Extract every checkbox as a task
  // - Keep original order

  const lines = tasksContent.split('\n')
  let currentPhase = null
  let currentSection = null

  for (const line of lines) {
    // Detect phase headers: "## Phase 1: Foundation"
    const phaseMatch = line.match(/^##\s*Phase\s*(\d+):?\s*(.*)$/i)
    if (phaseMatch) {
      currentPhase = {
        number: parseInt(phaseMatch[1]),
        name: phaseMatch[2].trim()
      }
      continue
    }

    // Detect section headers: "### 1.1 Configuration Module"
    const sectionMatch = line.match(/^###\s*([\d.]+)\s*(.*)$/i)
    if (sectionMatch) {
      currentSection = {
        id: sectionMatch[1],
        name: sectionMatch[2].trim()
      }
      continue
    }

    // Detect task items: "- [ ] 1.1.1 Create config/index.ts"
    const taskMatch = line.match(/^[-*]\s*\[([ xX])\]\s*([\d.]*)\s*(.*)$/i)
    if (taskMatch) {
      tasks.push({
        id: taskMatch[2] || `${currentSection?.id || '0'}.${tasks.length + 1}`,
        description: taskMatch[3].trim(),
        completed: taskMatch[1].toLowerCase() === 'x',
        phase: currentPhase,
        section: currentSection,
        originalLine: line
      })
    }
  }

  return tasks
}
```

**Important:** This parser captures ALL tasks. Nothing is filtered out.

---

### Step 2: AI-Driven Analysis (Per Task)

**Purpose:** Claude analyzes each task and makes decisions based on context

```markdown
## For Each Task, Claude Determines:

### 2.1 Complexity (1-10)
Read the task description and assess:
- How many distinct operations are involved?
- Does it touch multiple systems/layers?
- Is there significant business logic?
- Are there edge cases to handle?

Levels:
- 1-3: Simple (single operation, clear path)
- 4-6: Moderate (multiple steps, some logic)
- 7-8: Complex (cross-system, significant logic)
- 9-10: Critical (architectural changes, high stakes)

### 2.2 Risk Level (LOW / MEDIUM / HIGH)
Consider:
- What happens if this fails?
- Does it involve security, money, or user data?
- Is it reversible?
- Does it affect production?

### 2.3 Agent Assignment
Read the task and decide which agent should handle it:
- **uxui-frontend**: UI components, layouts, styling, user interactions
- **backend**: API endpoints, business logic, services, server-side
- **database**: Schema, migrations, queries, data modeling
- **frontend**: Connecting UI to APIs, state management, data fetching
- **test-debug**: Writing tests, debugging, fixing issues
- **integration**: Contract validation, E2E testing, system integration

**DO NOT use keyword matching.** Read the full context and decide.

Example:
- "Create user service that connects to database" → backend
  (It's a service layer, not database schema work)
- "Implement repository with 6 methods" → backend
  (Repository pattern is data access, handled by backend)
- "Add form validation" → uxui-frontend
  (Client-side validation is UI work)

### 2.4 Dependencies
Analyze what this task depends on and what depends on it:
- blocked_by: Tasks that must complete first
- blocks: Tasks waiting for this one
- can_parallelize: Tasks that can run simultaneously

### 2.5 Incremental Strategy Needed?
Determine if this task needs milestone-based execution:

**Needs Incremental (YES) if:**
- Involves batch processing (processing many items)
- Calls external APIs (unpredictable, needs error handling)
- Data transformation (ETL, migration)
- Multiple related methods (repository with 6 methods)
- Complex form (multi-step wizard)
- Risk = HIGH
- Complexity >= 7

**Standard (NO) if:**
- Simple CRUD operations
- Configuration/setup tasks
- Single-purpose utilities
- Low risk, low complexity
```

---

### Step 3: Auto-Add Best Practices

**Purpose:** Automatically add necessary tasks that ensure quality

```markdown
## Auto-Add Rules (No Warnings, Just Add)

### Rule 1: HIGH Risk → Add Checkpoint
If task has risk = HIGH:
  → Auto-add: "Verify [task name] before proceeding"
  → Position: Immediately after the HIGH risk task

### Rule 2: External API → Add Error Handling
If task involves external API/service:
  → Auto-add: "Add error handling for [API name]"
  → Auto-add: "Add retry logic with exponential backoff"
  → Auto-add: "Add timeout handling"

### Rule 3: Implementation → Add Verification
If task is implementation (not config/setup):
  → Auto-add: "Verify [task name] works as expected"
  → Position: End of the phase

### Rule 4: Database Changes → Add Migration Safety
If task modifies database schema:
  → Auto-add: "Backup data before migration"
  → Auto-add: "Test rollback procedure"

### Rule 5: Security-Critical → Add Security Check
If task involves auth/payment/sensitive data:
  → Auto-add: "Security review for [task name]"
  → Auto-add: "Verify no sensitive data in logs"
```

**Implementation:**

```typescript
function autoAddBestPractices(task: AnalyzedTask, allTasks: Task[]): Task[] {
  const additions: Task[] = []

  // Rule 1: HIGH Risk Checkpoint
  if (task.risk === 'HIGH') {
    additions.push({
      id: `${task.id}.verify`,
      description: `Checkpoint: Verify ${task.description} before proceeding`,
      type: 'verification',
      autoAdded: true,
      reason: 'HIGH risk task requires verification checkpoint'
    })
  }

  // Rule 2: External API Error Handling
  if (task.hasExternalAPI) {
    if (!hasRelatedTask(allTasks, task, 'error handling')) {
      additions.push({
        id: `${task.id}.errors`,
        description: `Add error handling for external API in ${task.description}`,
        type: 'implementation',
        autoAdded: true,
        reason: 'External APIs require error handling'
      })
    }
  }

  // Rule 3: Implementation Verification
  if (task.type === 'implementation' && task.complexity >= 5) {
    if (!hasVerificationTask(allTasks, task)) {
      additions.push({
        id: `${task.id}.test`,
        description: `Verify ${task.description} works correctly`,
        type: 'verification',
        autoAdded: true,
        reason: 'Implementation tasks need verification'
      })
    }
  }

  // Rule 4: Database Migration Safety
  if (task.involvesDatabaseChange) {
    additions.push({
      id: `${task.id}.backup`,
      description: `Backup affected tables before ${task.description}`,
      type: 'safety',
      autoAdded: true,
      reason: 'Database changes require backup'
    })
  }

  // Rule 5: Security Review
  if (task.isSecurityCritical) {
    additions.push({
      id: `${task.id}.security`,
      description: `Security review: ${task.description}`,
      type: 'verification',
      autoAdded: true,
      reason: 'Security-critical tasks require review'
    })
  }

  return additions
}
```

---

### Step 4: Generate Incremental Milestones

**Purpose:** Break complex tasks into testable milestones

```markdown
## Milestone Generation (AI-Driven)

For tasks that need incremental approach, Claude generates milestones.

### Pattern: Repository/Service Layer (Multiple Methods)
Task: "Implement admission repository with 6 methods"

Milestone 1: Core Method (Prove Pattern)
  - Implement 1 method (the most critical one)
  - Write test for this method
  - Verify output matches expected behavior
  Exit: 1 method works correctly ✓

Milestone 2: Related Methods
  - Implement 2-3 related methods
  - Tests pass for all
  Exit: Half of methods work ✓

Milestone 3: Complete All Methods
  - Implement remaining methods
  - All tests pass
  - No regression
  Exit: All methods work ✓

### Pattern: External API Integration
Task: "Integrate Gemini API for summarization"

Milestone 1: Single Call (Happy Path)
  - Make 1 API call with hardcoded input
  - Verify response format
  - Parse and display result
  Exit: 1 call works ✓

Milestone 2: Error Handling
  - Handle API errors gracefully
  - Add retry logic
  - Handle timeouts
  Exit: Errors handled ✓

Milestone 3: Scale Up
  - Process multiple items
  - Verify performance
  - Check rate limits
  Exit: Batch processing works ✓

### Pattern: Batch Processing
Task: "Process 100 API calls to Gemini"

Milestone 1: Single Item
  - Process 1 item successfully
  Exit: 1 item works ✓

Milestone 2: Small Batch (5 items)
  - Process 5 items
  - Verify consistency
  Exit: Small batch works ✓

Milestone 3: Medium Batch (20 items)
  - Process 20 items
  - Monitor performance
  Exit: Medium batch works ✓

Milestone 4: Full Scale (100 items)
  - Process all items
  - Summarize results
  Exit: Complete ✓

### Pattern: Complex Form
Task: "Build 5-step wizard form"

Milestone 1: Form Architecture
  - Setup form framework (React Hook Form, etc.)
  - Implement navigation between steps
  - Add 2-3 fields only
  Exit: Navigation works ✓

Milestone 2: End-to-End Flow
  - Connect to API
  - Save to database
  - Success feedback
  Exit: Submit works ✓

Milestone 3: All Fields + Validation
  - Add all fields
  - Add all validation rules
  - Accessibility check
  Exit: Complete form works ✓
```

**Generation Logic:**

```typescript
function generateMilestones(task: AnalyzedTask): Milestone[] {
  // Claude analyzes the task and determines appropriate milestones
  // based on the patterns above

  // The number of milestones depends on:
  // - Task complexity
  // - Risk level
  // - Type of work (API, form, batch, etc.)

  // Each milestone has:
  // - id: sequential number
  // - name: short description
  // - tasks: subtasks to complete
  // - exitCriteria: what must be true to proceed
  // - checkpoint: "Report results before next milestone"
}
```

---

### Step 5: Sort and Order

**Purpose:** Arrange tasks in optimal execution order

```typescript
function sortTasks(tasks: AnalyzedTask[]): AnalyzedTask[] {
  // Sorting rules:

  // 1. Respect original phase order from tasks.md
  // Phase 1 tasks before Phase 2 tasks, etc.

  // 2. Within each phase, order by:
  //    a. Dependencies first (tasks with no blockers)
  //    b. HIGH risk early (fail fast)
  //    c. Foundation before features
  //    d. Lower complexity first (quick wins)

  // 3. Mark parallelizable tasks
  //    Tasks with no shared dependencies can run together

  return tasks.sort((a, b) => {
    // Phase order
    if (a.phase.number !== b.phase.number) {
      return a.phase.number - b.phase.number
    }

    // Dependencies: unblocked tasks first
    const aBlocked = a.dependencies.blockedBy.length
    const bBlocked = b.dependencies.blockedBy.length
    if (aBlocked !== bBlocked) {
      return aBlocked - bBlocked
    }

    // Risk: HIGH risk first (to fail fast)
    const riskOrder = { HIGH: 0, MEDIUM: 1, LOW: 2 }
    if (a.risk !== b.risk) {
      return riskOrder[a.risk] - riskOrder[b.risk]
    }

    // Complexity: simpler first (quick wins)
    return a.complexity - b.complexity
  })
}
```

---

### Step 5.5: Inject UX Testing Phase (v2.7.0)

> **CRITICAL:** Auto-inject Phase X.5 (ux-tester) after EVERY uxui-frontend phase
> **Purpose:** User approval gate - validate UI from user perspectives before backend work

```typescript
function injectUXTestingPhases(phases: Phase[], tasks: AnalyzedTask[]): Phase[] {
  // Find all phases with uxui-frontend agent
  const uiFrontendPhases = phases.filter(p => {
    const phaseTasks = tasks.filter(t => t.phase?.number === p.number)
    return getMostCommonAgent(phaseTasks) === 'uxui-frontend'
  })

  if (uiFrontendPhases.length === 0) {
    return phases // No UI work, skip injection
  }

  // For EACH uxui-frontend phase, inject a .5 phase after it
  const newPhases = [...phases]

  uiFrontendPhases.forEach(uiPhase => {
    const uxTestingPhase = {
      number: `${uiPhase.number}.5`,
      name: 'UX Testing (Approval Gate)',
      agent: 'ux-tester',
      isApprovalGate: true,
      strategy: 'approval-required',
      description: `
        Test UI from user perspectives before proceeding.
        - Auto-generate personas based on product context
        - Test each persona via Chrome DevTools
        - Calculate weighted conversion prediction
        - PAUSE for user approval before next phase
      `,
      tasks: [
        { description: 'Generate personas from product context', autoAdded: true },
        { description: 'Test UI from each persona perspective', autoAdded: true },
        { description: 'Generate UX test report with conversion prediction', autoAdded: true },
        { description: '⏸️ PAUSE: Wait for user approval', autoAdded: true }
      ]
    }

    // Insert after the UI phase
    const insertIndex = newPhases.findIndex(p => p.number === uiPhase.number) + 1
    newPhases.splice(insertIndex, 0, uxTestingPhase)
  })

  return newPhases
}
```

**Approval Gate Workflow:**

```
Phase N: uxui-frontend (build UI)
    ↓
Phase N.5: ux-tester (APPROVAL GATE)
    → Auto-generate personas (3-5 based on product)
    → Test each persona via Chrome DevTools
    → Calculate weighted conversion prediction
    → Generate UX test report
    → ⏸️ PAUSE: Wait for user decision
    ↓
[User APPROVE] → Continue to Phase N+1
[User REJECT] → Loop back to Phase N with feedback
```

**Skip Conditions:**

```typescript
function shouldSkipUXTesting(phase: Phase, context: ChangeContext): boolean {
  // Skip if:
  // 1. Backend-only or API-only change
  if (context.changeType === 'backend-only' || context.changeType === 'api-only') {
    return true
  }

  // 2. User explicitly disabled (via flags)
  if (context.flags?.skip_ux_testing === true) {
    return true
  }

  // 3. Minor UI fix (average complexity < 3)
  const avgComplexity = phase.tasks.reduce((sum, t) => sum + (t.complexity || 5), 0) / phase.tasks.length
  if (avgComplexity < 3) {
    return true
  }

  return false
}
```

**Output Example:**

```markdown
## Phase 1: Frontend Mockup
**Agent:** uxui-frontend
...

---

## Phase 1.5: UX Testing (Approval Gate)
**Agent:** ux-tester
**Strategy:** APPROVAL REQUIRED

### Persona Testing
Auto-generated personas will test this UI:
- [ ] Generate personas from product context
- [ ] Test UI from each persona perspective
- [ ] Generate UX test report

### Approval Gate
⏸️ **PAUSE:** Development stops here until user approves.

**User Options:**
- `approve` → Continue to Phase 2
- `reject [feedback]` → Return to Phase 1 with specific feedback

---

## Phase 2: Backend API
...
```

---

### Step 6: Generate phases.md

**Purpose:** Create the final workflow file

```markdown
## Output Structure

# Phases: {Change Title}

> **Generated by:** Task Analyzer v2.0 (Template-Free)
> **Source:** tasks.md (Single Source of Truth)
> **Strategy:** Incremental development (small → large)
> **Generated:** {timestamp}

---

## Overview

| Phase | Name | Tasks | Agent | Strategy | Risk |
|-------|------|-------|-------|----------|------|
| 1 | Foundation | 17 | backend | standard | LOW |
| 2 | Repository Layer | 15 | backend | incremental (12 milestones) | MEDIUM |
| ... | ... | ... | ... | ... | ... |

**Total Tasks:** {original} + {auto-added} = {total}
**Incremental Milestones:** {count}

---

## Phase 1: Foundation

**Agent:** backend
**Strategy:** Standard
**Risk:** LOW

### Tasks

- [ ] 1.1.1 Create config/index.ts
- [ ] 1.1.2 Create app.config.ts
...

### Auto-Added (Best Practices)
- [ ] Verify Phase 1 foundation works correctly

**Exit Criteria:**
- [ ] All tasks completed
- [ ] All existing tests pass

---

## Phase 2: Repository Layer

**Agent:** backend
**Strategy:** INCREMENTAL
**Risk:** MEDIUM
**TDD Required:** Yes

### Task 2.2: Admission Repository
**Complexity:** 8/10 | **Why Agent:** Data access layer, database operations

#### Milestone 1/3: Core Method
**Goal:** Prove repository pattern works

- [ ] Write test for searchAdmissionRounds()
- [ ] Implement method
- [ ] Verify output matches current behavior

**Exit Criteria:**
- [ ] Test passes
- [ ] Method returns correct data

**CHECKPOINT:** Report results before Milestone 2

---

#### Milestone 2/3: Related Methods
...

---

## Auto-Added Tasks Summary

| Task | Reason | Phase |
|------|--------|-------|
| Error handling for external API | External APIs require error handling | 2 |
| Security review: auth system | Security-critical tasks require review | 3 |
| ... | ... | ... |

---

**End of phases.md**
```

---

## 🔧 Integration with /csetup

```typescript
// In csetup.md, replace Steps 3-5 with:

// STEP 3: Task Analyzer (Template-Free)
const tasksContent = Read(`openspec/changes/${changeId}/tasks.md`)

output(`\n📊 Analyzing tasks.md...`)

// 3.1 Parse ALL tasks
const allTasks = parseAllTasks(tasksContent)
output(`   Found: ${allTasks.length} tasks`)

// 3.2 AI Analysis (Claude decides for each task)
const analyzedTasks = []
for (const task of allTasks) {
  // Claude analyzes and decides:
  // - complexity (1-10)
  // - risk (LOW/MEDIUM/HIGH)
  // - agent (based on context, NOT keywords)
  // - dependencies
  // - needsIncremental (boolean)

  const analysis = analyzeTask(task, allTasks)
  analyzedTasks.push({ ...task, ...analysis })
}

// 3.3 Auto-Add Best Practices
const additions = []
for (const task of analyzedTasks) {
  const newTasks = autoAddBestPractices(task, allTasks)
  additions.push(...newTasks)
}
output(`   Auto-added: ${additions.length} best practice tasks`)

// 3.4 Generate Milestones for Incremental Tasks
for (const task of analyzedTasks) {
  if (task.needsIncremental) {
    task.milestones = generateMilestones(task)
  }
}
const incrementalCount = analyzedTasks.filter(t => t.milestones).length
output(`   Incremental: ${incrementalCount} tasks with milestones`)

// 3.5 Sort by Priority
const sortedTasks = sortTasks([...analyzedTasks, ...additions])

// 3.5.5 Inject UX Testing Phases (v2.7.0)
let phases = groupTasksByPhase(sortedTasks)
phases = injectUXTestingPhases(phases, sortedTasks)

const uxTestingPhases = phases.filter(p => p.agent === 'ux-tester')
if (uxTestingPhases.length > 0) {
  output(`   UX Testing: ${uxTestingPhases.length} approval gate(s) injected`)
}

// 3.6 Generate phases.md
const phasesContent = generatePhasesMarkdown(phases, sortedTasks, changeId)
Write(`openspec/changes/${changeId}/.claude/phases.md`, phasesContent)

output(`\n✅ Generated phases.md`)
output(`   - ${allTasks.length} original tasks`)
output(`   - ${additions.length} auto-added tasks`)
output(`   - ${incrementalCount} tasks with milestones`)
output(`   - ${uxTestingPhases.length} UX approval gate(s)`)
```

---

## 🚫 What's Removed (vs v1.x)

| Removed | Why |
|---------|-----|
| Keyword matching for agents | AI decides based on context |
| phase-templates.json dependency | Tasks.md is the source of truth |
| Template selection logic | No templates needed |
| Warning prompts | Auto-add instead of asking |
| Hardcoded detection rules | AI semantic understanding |

---

## ✅ What's Kept (Enhanced)

| Kept | Enhancement |
|------|-------------|
| Complexity scoring | AI-driven, not keyword-based |
| Risk assessment | AI-driven, considers full context |
| Dependency detection | AI understands relationships |
| Milestone generation | Smarter patterns, AI-driven |
| Priority sorting | Respects original structure |

---

## 📖 Example Transformation

**Input (tasks.md):**
```markdown
## Phase 1: Foundation
- [ ] 1.1.1 Create config/index.ts
- [ ] 1.1.2 Create app.config.ts

## Phase 2: Repository Layer
- [ ] 2.1 Implement admission repository with 6 methods
- [ ] 2.2 Implement exam repository with 4 methods
```

**Output (phases.md):**
```markdown
## Phase 1: Foundation
**Agent:** backend | **Strategy:** Standard | **Risk:** LOW

- [ ] 1.1.1 Create config/index.ts
- [ ] 1.1.2 Create app.config.ts
- [ ] ✨ Verify Phase 1 foundation works (auto-added)

---

## Phase 2: Repository Layer
**Agent:** backend | **Strategy:** INCREMENTAL | **Risk:** MEDIUM

### Task 2.1: Admission Repository (6 methods)
**Complexity:** 8/10

#### Milestone 1/3: Core Method
- [ ] Write test for searchAdmissionRounds()
- [ ] Implement method
- [ ] Verify output
**CHECKPOINT:** Report before Milestone 2

#### Milestone 2/3: Related Methods
- [ ] Implement findById, getUniversities, getFaculties
- [ ] All tests pass
**CHECKPOINT:** Report before Milestone 3

#### Milestone 3/3: Complete Repository
- [ ] Implement getStats
- [ ] All 6 methods work
- [ ] No regression

### Task 2.2: Exam Repository (4 methods)
**Complexity:** 7/10

#### Milestone 1/2: Core Methods
...
```

---

**This is Task Analyzer v2.0 - Template-Free, AI-Driven, Auto-Add Best Practices**
