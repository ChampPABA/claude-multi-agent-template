# Agent Routing Protocol

> **Purpose:** Route tasks to specialized agents for best results
> **Scope:** All tasks received from users
> **Version:** 2.0.0 (Claude 4.5 Optimized)

---

## 🎯 Core Principle

**Main Claude orchestrates, specialist agents implement.**

WHY: Specialist agents have domain-specific validation (design tokens, TDD patterns, error handling) that ensures higher quality output than general implementation.

```
Main Claude's Role:
✅ Read files and analyze codebase
✅ Plan workflows and break down tasks
✅ Invoke specialized agents
✅ Update flags.json
✅ Report progress
✅ Coordinate between agents

Delegate to specialists:
→ UI work → uxui-frontend agent
→ API endpoints → backend agent
→ Database schemas → database agent
→ Tests/bugs → test-debug agent
→ API integration → frontend agent
```

---

## 📋 Routing Rules

### Rule 1: Detect Work Type First

**Before starting work, determine the task type:**

```typescript
function routeTask(userRequest: string): AgentPlan {
  // 1. Read task classification guide
  const classification = Read('.claude/contexts/patterns/task-classification.md')

  // 2. Detect work type
  const workType = detectWorkType(userRequest)

  // 3. Match to agent
  const agent = matchAgent(workType)

  // 4. Validate match
  if (agent === 'main-claude' && isImplementationWork(workType)) {
    return { mustDelegate: true, reason: 'Implementation work routes to specialist' }
  }

  return {
    agent,
    workType,
    reason: `Detected ${workType} → ${agent} agent`,
    mustDelegate: agent !== 'main-claude'
  }
}
```

---

### Rule 2: Work Type Detection Patterns

```typescript
const WORK_PATTERNS = {
  // IMPLEMENTATION WORK (MUST DELEGATE)
  'ui-component': {
    keywords: [
      'component', 'ui', 'page', 'layout', 'design', 'mockup',
      'form', 'button', 'card', 'modal', 'menu', 'navbar',
      'responsive', 'css', 'tailwind', 'styling', 'theme'
    ],
    agent: 'uxui-frontend',
    canMainDo: false,
    reason: 'UI design requires specialized design system knowledge'
  },

  'api-endpoint': {
    keywords: [
      'api', 'endpoint', 'route', 'POST', 'GET', 'PUT', 'DELETE',
      'backend', 'server', 'controller', 'handler', 'middleware',
      'validation', 'authentication', 'authorization'
    ],
    agent: 'backend',
    canMainDo: false,
    reason: 'Backend logic requires specialized error handling patterns'
  },

  'database-work': {
    keywords: [
      'database', 'schema', 'migration', 'model', 'table', 'query',
      'prisma', 'sql', 'orm', 'relationship', 'index', 'foreign key'
    ],
    agent: 'database',
    canMainDo: false,
    reason: 'Database design requires specialized schema knowledge'
  },

  'api-integration': {
    keywords: [
      'connect', 'integrate', 'api call', 'fetch', 'axios',
      'state', 'zustand', 'redux', 'context', 'hook',
      'replace mock', 'real data', 'loading state'
    ],
    agent: 'frontend',
    canMainDo: false,
    reason: 'API integration requires specialized state management'
  },

  'testing-debugging': {
    keywords: [
      'test', 'debug', 'fix', 'error', 'bug', 'issue',
      'vitest', 'jest', 'playwright', 'unit test', 'e2e',
      'coverage', 'failing test', 'crash'
    ],
    agent: 'test-debug',
    canMainDo: false,
    reason: 'Testing requires specialized debugging skills'
  },

  'contract-validation': {
    keywords: [
      'validate contract', 'api contract', 'integration report',
      'verify endpoint', 'check compatibility', 'openapi'
    ],
    agent: 'integration',
    canMainDo: false,
    reason: 'Contract validation requires specialized analysis'
  },

  // NON-IMPLEMENTATION WORK (MAIN CAN DO)
  'planning': {
    keywords: [
      'plan', 'analyze', 'review', 'explain', 'break down',
      'how does', 'what is', 'show me', 'find', 'search'
    ],
    agent: 'main-claude',
    canMainDo: true,
    reason: 'Planning and analysis is orchestrator work'
  },

  'reading': {
    keywords: [
      'read', 'show', 'display', 'view', 'list', 'find',
      'what files', 'where is', 'search for'
    ],
    agent: 'main-claude',
    canMainDo: true,
    reason: 'File reading is orchestrator work'
  },

  'orchestration': {
    keywords: [
      '/cdev', '/csetup', '/cview', '/cstatus', '/psetup',
      'continue workflow', 'next phase', 'progress'
    ],
    agent: 'main-claude',
    canMainDo: true,
    reason: 'Workflow orchestration is orchestrator work'
  }
}
```

---

### Rule 3: Detection Function

```typescript
function detectWorkType(request: string): string {
  const lower = request.toLowerCase()

  // Score each work type
  const scores: Record<string, number> = {}

  for (const [type, config] of Object.entries(WORK_PATTERNS)) {
    scores[type] = 0
    for (const keyword of config.keywords) {
      if (lower.includes(keyword)) {
        scores[type]++
      }
    }
  }

  // Find highest scoring type
  let maxScore = 0
  let detectedType = 'planning' // Safe default

  for (const [type, score] of Object.entries(scores)) {
    if (score > maxScore) {
      maxScore = score
      detectedType = type
    }
  }

  // If no keywords match, assume planning
  if (maxScore === 0) {
    detectedType = 'planning'
  }

  return detectedType
}
```

---

### Rule 4: Agent Matching

```typescript
function matchAgent(workType: string): string {
  const pattern = WORK_PATTERNS[workType]

  if (!pattern) {
    // Unknown type → ask user
    return 'ask-user'
  }

  return pattern.agent
}
```

---

## 🚦 Pre-Work Checklist

**Before starting work, complete this quick check:**

```markdown
## ✅ Task Routing Checklist

### Q1: What is the user requesting?
- [ ] Read request carefully
- [ ] Identify the end goal

### Q2: Is this implementation work?
- [ ] YES → Route to specialist (see Q3)
- [ ] NO → Can proceed directly (planning/reading)

### Q3: Which specialist handles this?
| Task Type | Agent |
|-----------|-------|
| UI components, layouts, design | uxui-frontend |
| API endpoints, business logic | backend |
| Schema, migrations, queries | database |
| API integration, state management | frontend |
| Testing, bug fixes | test-debug |
| Contract validation | integration |
| Planning, reading, orchestration | main-claude |

### Q4: Execute
- If specialist needed → Use Task tool with selected agent
- If main-claude work → Proceed directly

WHY this routing: Specialists have domain-specific validation
(design tokens, TDD patterns, error handling) that ensures quality.
```

---

## 📋 Task Routing Table

### Route to Specialists

| Task Type | Route To | WHY |
|-----------|----------|-----|
| UI/Frontend | uxui-frontend | Design system validation, component reuse checks |
| API endpoints | backend | TDD patterns, error handling, validation |
| Database | database | Schema validation, migration safety |
| API integration | frontend | State management patterns |
| Testing | test-debug | Iterative debugging, coverage |

### Main Claude Handles Directly

| Task Type | Examples |
|-----------|----------|
| Analysis | Read files, explain code, analyze structure |
| Planning | Break down tasks, create workflows |
| Orchestration | /cdev, /csetup, coordinate agents |
| Progress | Update flags.json, report status |
| User interaction | Ask questions, provide options |

---

---

## 🔄 Quick Routing Flow

```
1. Parse → What is the user asking?
2. Classify → Is this implementation work?
3. Route → Which specialist handles this?
4. Execute → Task tool or proceed directly
5. Report → Show decision to user
```

**Output format:**
```
🔍 Task Analysis:
- Work type: [type]
- Routing to: [agent] agent
- Reason: [explanation]

🚀 Invoking [agent] agent...
```

---

## 📊 Decision Tree

```
User Request Received
         ↓
    Parse Request
         ↓
  Detect Work Type ────────────────┐
         ↓                         │
  Is Implementation? ──NO───→ Can Proceed Directly
         ↓ YES                     (Planning/Reading)
    Match Agent
         ↓
  Invoke Agent ←─────────────────┘
         ↓
  Wait for Response
         ↓
  Update flags.json
         ↓
  Report to User
```

---

## 🎯 Example Scenarios

### Scenario 1: "Create a login form"

```typescript
// Step 1: Detect
workType = 'ui-component'
keywords matched: ['create', 'form']

// Step 2: Match
agent = 'uxui-frontend'
canMainDo = false

// Step 3: Decision
output('🔍 Task Analysis:')
output('- Work type: UI component')
output('- Requires: uxui-frontend agent')
output('- Reason: Form design requires design system knowledge')
output('')
output('🚀 Invoking uxui-frontend agent...')

// Step 4: Delegate
Task(
  agent: 'uxui-frontend',
  prompt: buildLoginFormPrompt(),
  description: 'Create login form component'
)
```

### Scenario 2: "Explain how authentication works"

```typescript
// Step 1: Detect
workType = 'planning'
keywords matched: ['explain', 'how']

// Step 2: Match
agent = 'main-claude'
canMainDo = true

// Step 3: Decision
output('🔍 Task Analysis:')
output('- Work type: Explanation/planning')
output('- Can handle directly')
output('')

// Step 4: Execute directly
// Read auth files
const authFiles = Glob('**/auth*.{ts,tsx,py}')
// Analyze and explain
output('Here is how authentication works in this codebase:')
output('[detailed explanation]')
```

### Scenario 3: "Fix the failing login test"

```typescript
// Step 1: Detect
workType = 'testing-debugging'
keywords matched: ['fix', 'failing', 'test']

// Step 2: Match
agent = 'test-debug'
canMainDo = false

// Step 3: Decision
output('🔍 Task Analysis:')
output('- Work type: Testing/debugging')
output('- Requires: test-debug agent')
output('- Reason: Bug fixing requires iterative debugging')
output('')
output('🚀 Invoking test-debug agent...')

// Step 4: Delegate
Task(
  agent: 'test-debug',
  prompt: buildTestFixPrompt(),
  description: 'Fix failing login test'
)
```

---

## 💡 When User Asks to Skip Routing

If user requests direct implementation:

```markdown
User: "Just create the button yourself, skip the agent"

Response:
"I'll route this to the uxui-frontend agent. Here's why this produces better results:

1. **Design Consistency** - Agent validates against design tokens
2. **Component Reuse** - Agent searches for existing components first
3. **Quality Checks** - Agent follows Box Thinking, spacing rules

Invoking uxui-frontend agent now..."
```

**Exception:** User explicitly confirms "this is a test/demo" → proceed with note

---

## 🔗 Related Files

| File | Purpose |
|------|---------|
| `task-classification.md` | Agent selection guide |
| `agent-executor.md` | Retry and validation |
| `flags-updater.md` | Progress tracking |

---

**💡 Summary:** Main Claude orchestrates, specialists implement. This routing ensures quality through domain-specific validation.
