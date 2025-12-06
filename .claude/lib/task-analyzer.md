# Task Analyzer - TaskMaster-style Analysis

> **Enhanced task analysis for intelligent phase generation**
> **Version:** 1.4.0 (Incremental Testing Integration)
> **Used by:** `/csetup` command

---

## 🎯 Purpose

Analyze tasks.md (from OpenSpec) and generate **intelligent task metadata** including:
- Complexity scoring (1-10)
- Dependency detection
- Risk assessment
- Research requirements
- Subtask breakdown recommendations
- Priority ranking
- **Incremental testing detection** (NEW in v1.4.0)
- **Milestone generation** (NEW in v1.4.0)

**Inspired by:** [claude-task-master](https://github.com/eyaltoledano/claude-task-master)

---

## 📋 Analysis Framework

### 1. Complexity Scoring (1-10)

**Factors:**
```typescript
function calculateComplexity(task: Task): number {
  let score = 3 // Base complexity

  // Factor 1: Estimated time
  if (task.estimatedTime > 120) score += 3 // > 2 hours
  else if (task.estimatedTime > 60) score += 2 // > 1 hour
  else if (task.estimatedTime > 30) score += 1 // > 30 min

  // Factor 2: Keywords
  const highComplexityKeywords = [
    'authentication', 'security', 'payment', 'real-time',
    'websocket', 'oauth', 'encryption', 'migration',
    'refactor', 'optimization', 'performance'
  ]
  const matches = highComplexityKeywords.filter(kw =>
    task.description.toLowerCase().includes(kw)
  )
  score += matches.length

  // Factor 3: Multi-step indicator
  if (task.description.match(/\band\b/gi)?.length > 2) score += 1
  if (task.description.match(/\bthen\b/gi)?.length > 1) score += 1

  // Factor 4: External dependencies
  if (task.description.match(/(api|library|service|integration)/i)) score += 1

  // Cap at 10
  return Math.min(score, 10)
}
```

**Complexity Levels:**
- 1-3: Simple (CRUD, UI components)
- 4-6: Moderate (Business logic, integrations)
- 7-8: Complex (Auth, payments, real-time)
- 9-10: Critical (Security, migrations, major refactors)

---

### 2. Dependency Detection

**Analysis:**
```typescript
function detectDependencies(task: Task, allTasks: Task[]): Dependencies {
  const dependencies = {
    blocks: [], // Tasks this task blocks
    blockedBy: [], // Tasks blocking this task
    parallelizable: [] // Tasks that can run in parallel
  }

  // Rule 1: UI depends on backend
  if (task.type === 'frontend-integration') {
    const apiTasks = allTasks.filter(t =>
      t.type === 'backend' &&
      t.description.match(/api|endpoint/i)
    )
    dependencies.blockedBy.push(...apiTasks.map(t => t.id))
  }

  // Rule 2: Backend depends on database
  if (task.type === 'backend') {
    const dbTasks = allTasks.filter(t =>
      t.type === 'database' &&
      task.description.includes(t.description.split(' ')[0]) // Common entity
    )
    dependencies.blockedBy.push(...dbTasks.map(t => t.id))
  }

  // Rule 3: Tests depend on implementation
  if (task.type === 'test') {
    const implTasks = allTasks.filter(t =>
      t.type !== 'test' &&
      task.description.toLowerCase().includes(t.description.split(' ')[0].toLowerCase())
    )
    dependencies.blockedBy.push(...implTasks.map(t => t.id))
  }

  // Rule 4: Integration depends on both UI and API
  if (task.description.match(/connect|integrate|link/i)) {
    const uiTasks = allTasks.filter(t => t.type === 'uxui-frontend')
    const apiTasks = allTasks.filter(t => t.type === 'backend')
    dependencies.blockedBy.push(...uiTasks.map(t => t.id), ...apiTasks.map(t => t.id))
  }

  // Rule 5: Parallel work (no shared entities)
  const parallelizable = allTasks.filter(t => {
    if (t.id === task.id) return false
    const taskEntities = extractEntities(task.description)
    const otherEntities = extractEntities(t.description)
    return taskEntities.every(e => !otherEntities.includes(e))
  })
  dependencies.parallelizable = parallelizable.map(t => t.id)

  return dependencies
}
```

---

### 3. Risk Assessment

**Risk Factors:**
```typescript
function assessRisk(task: Task, complexity: number): RiskLevel {
  let riskScore = 0

  // Factor 1: Complexity
  if (complexity >= 9) riskScore += 3
  else if (complexity >= 7) riskScore += 2
  else if (complexity >= 5) riskScore += 1

  // Factor 2: Security-critical
  const securityKeywords = ['auth', 'password', 'token', 'security', 'payment', 'encryption']
  if (securityKeywords.some(kw => task.description.toLowerCase().includes(kw))) {
    riskScore += 3
  }

  // Factor 3: External dependencies
  const externalKeywords = ['api', 'third-party', 'service', 'integration', 'library']
  if (externalKeywords.some(kw => task.description.toLowerCase().includes(kw))) {
    riskScore += 1
  }

  // Factor 4: Data migration
  if (task.description.match(/migrat|transform|convert/i)) {
    riskScore += 2
  }

  // Factor 5: User-facing
  if (task.type === 'uxui-frontend' && task.description.match(/checkout|payment|profile|login/i)) {
    riskScore += 1
  }

  // Risk levels
  if (riskScore >= 6) return { level: 'HIGH', score: riskScore, mitigation: [] }
  if (riskScore >= 3) return { level: 'MEDIUM', score: riskScore, mitigation: [] }
  return { level: 'LOW', score: riskScore, mitigation: [] }
}

function generateMitigation(risk: RiskLevel, task: Task): string[] {
  const mitigation = []

  if (risk.level === 'HIGH' || risk.level === 'MEDIUM') {
    mitigation.push('TDD required (write tests first)')
    mitigation.push('Code review checkpoint')
  }

  if (task.description.match(/auth|security|payment/i)) {
    mitigation.push('Security checklist validation')
    mitigation.push('Use battle-tested libraries (no custom crypto)')
  }

  if (task.description.match(/migration|transform/i)) {
    mitigation.push('Backup data before migration')
    mitigation.push('Dry-run test on staging')
  }

  if (risk.level === 'HIGH') {
    mitigation.push('Add 50% time buffer')
    mitigation.push('Pair programming recommended')
  }

  return mitigation
}
```

---

### 4. Research Requirements Detection

> **Integration with /pageplan (v1.4.0):**
> - `/pageplan` handles: Component reuse analysis + Content drafting + Asset checklist
> - `TaskMaster` handles: Technical research (libraries, APIs, migrations)
> - **No overlap:** UX/accessibility research is skipped if `page-plan.md` exists

**Decision Matrix:**

| Task Type | Has page-plan.md | Research Triggered |
|-----------|------------------|--------------------|
| UI Landing | ✅ Yes | ❌ Skip UX patterns<br>❌ Skip accessibility<br>✅ Check library/migration |
| UI Landing | ❌ No | ✅ UX patterns research<br>✅ Accessibility research<br>✅ Check library |
| API Integration | ✅ Yes | ✅ Integration research (not affected) |
| Database Migration | ❌ No | ✅ Migration research (not affected) |

**Why this separation?**
- `/pageplan` = **Design-level** (which components, what content, what assets)
- `TaskMaster` = **Technical-level** (how to implement, which libraries, what patterns)
- Avoids redundant "landing page best practices" research when page structure is already planned

**Detection Logic:**
```typescript
function detectResearchNeeds(task: Task, changeContext: any): ResearchRequirement | null {
  // Check if page-plan.md exists (skip UX/accessibility research)
  const hasPagePlan = fileExists(`openspec/changes/${changeContext.changeId}/page-plan.md`)

  const researchIndicators = {
    // Technical research (always check)
    newTechnology: /new|latest|modern|upgrade|v\d+/i,
    bestPractices: /best practice|pattern|approach|strategy|how to/i,
    integration: /integrate|connect|setup|configure/i,
    performance: /optimi[sz]e|performance|speed|faster/i,
    migration: /migrat|upgrade|convert/i,

    // UX research (skip if page-plan exists)
    uxPatterns: hasPagePlan ? null : /dashboard|landing|e-commerce|checkout|wizard|onboarding/i,
    accessibility: hasPagePlan ? null : /form|input|modal|navigation|menu|dialog|button/i,

    // Design system (always check)
    componentLibrary: /component library|ui library|design system/i,
    designGuidelines: /brand|style|visual|aesthetic|appearance/i
  }

  // Check for multiple patterns (prioritize by order)
  const detectedPatterns = []

  for (const [category, pattern] of Object.entries(researchIndicators)) {
    if (pattern && pattern.test(task.description)) {
      detectedPatterns.push({
        category,
        reason: `Task involves ${category} - requires research phase`,
        suggestedQueries: generateResearchQueries(task, category),
        estimatedTime: getEstimatedResearchTime(category)
      })
    }
  }

  // Special case: If no design system exists and UI work detected
  if (task.type === 'uxui-frontend' && !fileExists('design-system/data.yaml')) {
    detectedPatterns.push({
      category: 'missingDesignSystem',
      reason: 'No design system found - component library selection needed',
      suggestedQueries: [
        'shadcn/ui vs Radix UI comparison 2025',
        'React component library recommendations',
        'Headless UI libraries for Tailwind CSS'
      ],
      estimatedTime: 10
    })
  }

  // Log skipped research
  if (hasPagePlan && detectedPatterns.length === 0) {
    console.log(`ℹ️ UX/accessibility research skipped (page-plan.md exists)`)
  }

  // Return highest priority research need
  return detectedPatterns[0] || null
}

function getEstimatedResearchTime(category: string): number {
  const timeMap = {
    newTechnology: 15,
    bestPractices: 10,
    integration: 20,
    performance: 10,
    migration: 15,
    uxPatterns: 10,
    accessibility: 5,
    componentLibrary: 10,
    designGuidelines: 5,
    missingDesignSystem: 10
  }
  return timeMap[category] || 15
}

function generateResearchQueries(task: Task, category: string): string[] {
  const queries = []

  if (category === 'newTechnology') {
    queries.push(`Latest version and features of ${extractTechnology(task.description)}`)
    queries.push(`Migration guide from current version`)
  }

  if (category === 'bestPractices') {
    queries.push(`Best practices for ${extractContext(task.description)}`)
    queries.push(`Common pitfalls and how to avoid them`)
  }

  if (category === 'integration') {
    const services = extractServices(task.description)
    queries.push(`${services[0]} integration with ${services[1]} guide`)
    queries.push(`Authentication and security considerations`)
  }

  if (category === 'performance') {
    queries.push(`Performance optimization techniques for ${extractContext(task.description)}`)
    queries.push(`Benchmarking and profiling tools`)
  }

  if (category === 'migration') {
    const tech = extractTechnology(task.description)
    queries.push(`${tech} migration guide 2025`)
    queries.push(`Breaking changes and upgrade path`)
    queries.push(`Data migration strategies and best practices`)
  }

  if (category === 'uxPatterns') {
    const pageType = extractPageType(task.description)
    queries.push(`${pageType} best practices 2025`)
    queries.push(`${pageType} UX patterns and examples`)
    queries.push(`${pageType} conversion optimization techniques`)
  }

  if (category === 'accessibility') {
    const component = extractComponent(task.description)
    queries.push(`${component} accessibility best practices`)
    queries.push(`WCAG 2.1 guidelines for ${component}`)
    queries.push(`Screen reader support for ${component}`)
    queries.push(`Keyboard navigation patterns`)
  }

  if (category === 'componentLibrary') {
    queries.push('shadcn/ui vs Radix UI comparison 2025')
    queries.push('React component library recommendations')
    queries.push('Headless UI libraries for Tailwind CSS')
    queries.push('Component library installation and setup')
  }

  if (category === 'designGuidelines') {
    queries.push('Modern design trends 2025')
    queries.push('Color palette generation tools')
    queries.push('Typography pairing recommendations')
    queries.push('Design system structure and organization')
  }

  return queries
}

// Helper functions
function extractPageType(desc: string): string {
  const pageTypes = {
    'dashboard': 'Dashboard',
    'landing': 'Landing page',
    'e-commerce': 'E-commerce product page',
    'checkout': 'Checkout flow',
    'wizard': 'Multi-step wizard',
    'onboarding': 'User onboarding'
  }

  for (const [key, value] of Object.entries(pageTypes)) {
    if (desc.toLowerCase().includes(key)) return value
  }
  return 'Page'
}

function extractComponent(desc: string): string {
  const components = ['form', 'input', 'modal', 'navigation', 'menu', 'dialog', 'button', 'table', 'dropdown']
  const found = components.find(c => desc.toLowerCase().includes(c))
  return found ? found.charAt(0).toUpperCase() + found.slice(1) : 'Component'
}
```

---

### 5. Subtask Breakdown

**When to break down:**
```typescript
function needsSubtaskBreakdown(task: Task, complexity: number): boolean {
  // Rule 1: High complexity
  if (complexity >= 7) return true

  // Rule 2: Multiple verbs (multi-step)
  const verbs = task.description.match(/\b(create|build|implement|design|develop|add|update|refactor)\b/gi)
  if (verbs && verbs.length > 2) return true

  // Rule 3: Estimated time > 90 minutes
  if (task.estimatedTime > 90) return true

  // Rule 4: Explicit "and" connectors > 2
  if (task.description.match(/\band\b/gi)?.length > 2) return true

  return false
}

function generateSubtasks(task: Task): Subtask[] {
  const subtasks = []

  // Pattern 1: UI + Backend pattern
  if (task.description.match(/ui|component|page/i) && task.description.match(/api|backend|endpoint/i)) {
    subtasks.push({
      id: `${task.id}.1`,
      description: `Create UI component for ${extractEntity(task.description)}`,
      type: 'uxui-frontend',
      estimatedTime: 45
    })
    subtasks.push({
      id: `${task.id}.2`,
      description: `Create API endpoint for ${extractEntity(task.description)}`,
      type: 'backend',
      estimatedTime: 30
    })
    subtasks.push({
      id: `${task.id}.3`,
      description: `Integrate UI with API`,
      type: 'frontend',
      estimatedTime: 20
    })
  }

  // Pattern 2: CRUD operations
  if (task.description.match(/crud|create.*read.*update.*delete/i)) {
    ['Create', 'Read', 'Update', 'Delete'].forEach((op, i) => {
      subtasks.push({
        id: `${task.id}.${i + 1}`,
        description: `Implement ${op} operation for ${extractEntity(task.description)}`,
        type: task.type,
        estimatedTime: 20
      })
    })
  }

  // Pattern 3: Multi-entity
  const entities = extractEntities(task.description)
  if (entities.length > 1) {
    entities.forEach((entity, i) => {
      subtasks.push({
        id: `${task.id}.${i + 1}`,
        description: `${task.description.split(' ')[0]} ${entity}`,
        type: task.type,
        estimatedTime: Math.ceil(task.estimatedTime / entities.length)
      })
    })
  }

  return subtasks
}
```

---

### 6. Priority Ranking

**Priority Score:**
```typescript
function calculatePriority(task: Task, metadata: TaskMetadata): number {
  let priority = 50 // Base priority

  // Factor 1: Business value (from keywords)
  const criticalKeywords = ['login', 'checkout', 'payment', 'core', 'critical']
  if (criticalKeywords.some(kw => task.description.toLowerCase().includes(kw))) {
    priority += 30
  }

  // Factor 2: Blocks other tasks
  priority += metadata.dependencies.blocks.length * 10

  // Factor 3: No blockers (can start immediately)
  if (metadata.dependencies.blockedBy.length === 0) {
    priority += 20
  }

  // Factor 4: Risk (high risk = higher priority to tackle early)
  if (metadata.risk.level === 'HIGH') priority += 15
  if (metadata.risk.level === 'MEDIUM') priority += 5

  // Factor 5: Complexity (simpler = higher priority for quick wins)
  if (metadata.complexity <= 3) priority += 10

  // Factor 6: User-facing
  if (task.type === 'uxui-frontend') priority += 10

  return Math.min(priority, 100)
}

function getPriorityLabel(score: number): string {
  if (score >= 80) return 'CRITICAL'
  if (score >= 60) return 'HIGH'
  if (score >= 40) return 'MEDIUM'
  return 'LOW'
}
```

---

### 7. Incremental Testing Detection

> **NEW in v1.4.0:** Automatic detection of tasks that require progressive validation

**Purpose:**
Identify high-risk/complex tasks that should be broken into milestones instead of being implemented all at once.

**Detection Logic:**
```typescript
function detectTestingStrategy(task: Task, metadata: TaskMetadata): TestingStrategy {
  const { complexity, risk } = metadata

  // Rule 1: HIGH risk always requires incremental testing
  if (risk.level === 'HIGH') {
    return {
      type: 'incremental',
      reason: `HIGH risk (${risk.score}/10) - Progressive validation required to catch issues early`
    }
  }

  // Rule 2: MEDIUM risk + High complexity
  if (risk.level === 'MEDIUM' && complexity.score >= 7) {
    return {
      type: 'incremental',
      reason: `MEDIUM risk + High complexity (${complexity.score}/10) - Incremental approach reduces debugging effort`
    }
  }

  // Rule 3: External API dependencies
  if (hasExternalAPI(task)) {
    return {
      type: 'incremental',
      reason: 'External API dependency - Test with small sample first to validate integration'
    }
  }

  // Rule 4: Data-intensive operations
  if (isDataIntensive(task)) {
    return {
      type: 'incremental',
      reason: 'Data-intensive operation - Scale testing from small to large dataset'
    }
  }

  // Default: Standard testing
  return {
    type: 'standard',
    reason: 'Low risk, no external dependencies - Standard implementation approach'
  }
}

// Helper: Detect external API dependencies
function hasExternalAPI(task: Task): boolean {
  const externalAPIs = [
    'google', 'stripe', 'paypal', 'twilio', 'sendgrid',
    'aws', 'azure', 'gcp', 'firebase', 'openai',
    'third-party', 'external api', 'rest api', 'graphql api',
    'oauth', 'saml', 'maps', 'payment gateway'
  ]

  const taskLower = task.description.toLowerCase()
  return externalAPIs.some(api => taskLower.includes(api))
}

// Helper: Detect data-intensive operations
function isDataIntensive(task: Task): boolean {
  const dataIntensiveKeywords = [
    'batch', 'bulk', 'import', 'export', 'migration',
    'etl', 'thousands', 'large dataset', 'mass update',
    'data transformation', 'sync', 'replicate'
  ]

  const taskLower = task.description.toLowerCase()
  return dataIntensiveKeywords.some(kw => taskLower.includes(kw))
}
```

**Output Examples:**
```
Task: "Integrate Google Maps API for store locator"
→ Strategy: INCREMENTAL (External API dependency)

Task: "Migrate 10,000 user records from legacy database"
→ Strategy: INCREMENTAL (Data-intensive operation)

Task: "Implement user login with JWT authentication"
→ Strategy: INCREMENTAL (HIGH risk - security critical)

Task: "Create simple contact form with validation"
→ Strategy: STANDARD (Low risk, no external deps)
```

---

### 8. Milestone Generation

> **NEW in v1.4.0:** Generate progressive validation milestones for incremental tasks

**Purpose:**
Break down incremental tasks into testable milestones that validate functionality from simple → complex.

**Generation Logic:**
```typescript
function generateMilestones(task: Task, metadata: TaskMetadata): Milestone[] {
  const milestones: Milestone[] = []
  const taskLower = task.description.toLowerCase()
  const estimatedTime = metadata.estimatedTime.adjusted

  // Pattern 1: Backend API Integration
  if (hasExternalAPI(task) || taskLower.match(/api|integration|service/i)) {
    milestones.push({
      id: 1,
      name: 'Core implementation (minimal viable)',
      testScope: 'Single happy path (1 record, hardcoded input)',
      exitCriteria: [
        'Response status = 200 (or expected success code)',
        'Data structure valid (matches expected schema)',
        'Response time < 500ms',
        'API authentication works (no 401/403 errors)'
      ],
      estimatedTime: Math.ceil(estimatedTime * 0.3),
      retryLimit: 2
    })

    milestones.push({
      id: 2,
      name: 'Parameterized query',
      testScope: '10 records, dynamic user input',
      exitCriteria: [
        'Accepts dynamic input parameters',
        'Returns correct results for all 10 test cases',
        'No duplicate API calls (check request logs)',
        'Response time < 700ms average'
      ],
      estimatedTime: Math.ceil(estimatedTime * 0.3),
      retryLimit: 2
    })

    milestones.push({
      id: 3,
      name: 'Error handling + edge cases',
      testScope: 'Invalid input, API errors, timeouts, rate limits',
      exitCriteria: [
        'Invalid input handled gracefully (no crashes)',
        'API errors caught and logged correctly',
        'Timeout logic works (retry or fallback)',
        'Rate limiting detected and handled',
        'User-friendly error messages (no stack traces)'
      ],
      estimatedTime: Math.ceil(estimatedTime * 0.2),
      retryLimit: 2
    })

    milestones.push({
      id: 4,
      name: 'Scale + performance validation',
      testScope: '100-1000 records, concurrent requests',
      exitCriteria: [
        'Response time < 2s for 100 records',
        'No memory leaks under load',
        'Pagination/batching works correctly (if applicable)',
        'Caching reduces redundant API calls',
        'No database connection exhaustion'
      ],
      estimatedTime: Math.ceil(estimatedTime * 0.2),
      retryLimit: 2
    })

    return milestones
  }

  // Pattern 2: Complex Form (architecture-first approach)
  if (taskLower.match(/form|survey|questionnaire|wizard/i) && metadata.complexity.score >= 7) {
    milestones.push({
      id: 1,
      name: 'Form architecture + skeleton',
      testScope: 'Full structure with 2-3 critical fields only',
      exitCriteria: [
        'Multi-step logic works (if applicable)',
        'Validation framework integrated',
        'State management clear (React Hook Form, Formik, etc.)',
        'Navigation between steps functional',
        'Architecture supports scaling to full field count'
      ],
      estimatedTime: Math.ceil(estimatedTime * 0.4),
      retryLimit: 2
    })

    milestones.push({
      id: 2,
      name: 'End-to-end flow validation',
      testScope: 'Submit minimal form → API → Database',
      exitCriteria: [
        'Data saved to database correctly',
        'API contract validated (request/response format)',
        'Success feedback shown to user',
        'No console errors or warnings',
        'Data retrieved correctly (read-after-write test)'
      ],
      estimatedTime: Math.ceil(estimatedTime * 0.3),
      retryLimit: 2
    })

    milestones.push({
      id: 3,
      name: 'Complete all fields + validation',
      testScope: 'All fields + validation rules + accessibility',
      exitCriteria: [
        'All field validations work (required, format, custom)',
        'No UX regressions (smooth transitions, no flickers)',
        'Accessibility checklist passed (keyboard nav, ARIA labels)',
        'Form submission with all fields succeeds',
        'Error messages clear and actionable'
      ],
      estimatedTime: Math.ceil(estimatedTime * 0.3),
      retryLimit: 2
    })

    return milestones
  }

  // Pattern 3: Database Migration / ETL
  if (taskLower.match(/migrat|etl|import|batch|sync/i) || isDataIntensive(task)) {
    milestones.push({
      id: 1,
      name: 'Dry-run with 10 records',
      testScope: 'Test migration/ETL script on 10 sample records',
      exitCriteria: [
        'Data transforms correctly (validate output schema)',
        'No data loss (record count matches)',
        'Rollback mechanism works',
        'Execution time reasonable (< 5s for 10 records)',
        'Logs are clear and traceable'
      ],
      estimatedTime: Math.ceil(estimatedTime * 0.25),
      retryLimit: 2
    })

    milestones.push({
      id: 2,
      name: 'Scale to 100 records',
      testScope: 'Validate performance and edge cases',
      exitCriteria: [
        'Completes within expected time (< 30s for 100 records)',
        'Handles duplicates correctly (skip or merge)',
        'Error logging works (failed records tracked)',
        'Progress tracking accurate',
        'Memory usage stable (no leaks)'
      ],
      estimatedTime: Math.ceil(estimatedTime * 0.25),
      retryLimit: 2
    })

    milestones.push({
      id: 3,
      name: 'Full dataset migration (staging)',
      testScope: 'Migrate entire dataset on staging environment',
      exitCriteria: [
        'All records migrated successfully (100% completion)',
        'Data integrity validated (checksums match)',
        'No production impact (read-only or isolated)',
        'Rollback plan tested and documented',
        'Migration can be re-run safely (idempotent)'
      ],
      estimatedTime: Math.ceil(estimatedTime * 0.5),
      retryLimit: 2
    })

    return milestones
  }

  // Fallback: Generic incremental pattern (for unmatched patterns)
  if (metadata.risk.level === 'HIGH' || metadata.complexity.score >= 8) {
    milestones.push({
      id: 1,
      name: 'Core implementation (minimal)',
      testScope: 'Basic functionality with simplest input',
      exitCriteria: [
        'Core logic works for happy path',
        'No critical errors or crashes',
        'Basic validation passes'
      ],
      estimatedTime: Math.ceil(estimatedTime * 0.4),
      retryLimit: 2
    })

    milestones.push({
      id: 2,
      name: 'Expand functionality + edge cases',
      testScope: 'Full functionality with edge cases',
      exitCriteria: [
        'All features implemented',
        'Edge cases handled correctly',
        'Error handling comprehensive',
        'Tests pass'
      ],
      estimatedTime: Math.ceil(estimatedTime * 0.6),
      retryLimit: 2
    })

    return milestones
  }

  // Should not reach here (detectTestingStrategy should filter)
  return []
}
```

**Milestone Structure:**
```typescript
interface Milestone {
  id: number                  // Sequential (1, 2, 3, ...)
  name: string               // Short description
  testScope: string          // What to test (clear, specific)
  exitCriteria: string[]     // Checklist to validate
  estimatedTime: number      // Minutes (derived from task estimate)
  retryLimit: number         // Always 2 (as confirmed)
}
```

**Output Example:**
```
Task: "Integrate Stripe payment processing"
→ Testing Strategy: INCREMENTAL (External API + HIGH risk)
→ Milestones: 4

Milestone 1: Core implementation (minimal viable)
  Test Scope: Single happy path (1 record, hardcoded)
  Exit Criteria:
    - Response status = 200
    - Data structure valid
    - Response time < 500ms
    - API authentication works
  Estimated Time: 27 min
  Retry Limit: 2

Milestone 2: Parameterized query
  Test Scope: 10 records, dynamic input
  Exit Criteria:
    - Accepts dynamic input
    - Returns correct results for all 10
    - No duplicate API calls
    - Response time < 700ms
  Estimated Time: 27 min
  Retry Limit: 2

... (Milestone 3 & 4)
```

---

## 📊 Output Format

### Enhanced Task Metadata

```typescript
interface TaskMetadata {
  id: string
  title: string
  description: string
  type: AgentType

  // TaskMaster-style analysis
  complexity: {
    score: number          // 1-10
    level: 'Simple' | 'Moderate' | 'Complex' | 'Critical'
    factors: string[]      // What contributed to score
  }

  dependencies: {
    blocks: string[]       // Task IDs this blocks
    blockedBy: string[]    // Task IDs blocking this
    parallelizable: string[] // Can run in parallel with
  }

  risk: {
    level: 'LOW' | 'MEDIUM' | 'HIGH'
    score: number
    mitigation: string[]   // Risk mitigation strategies
  }

  research: {
    required: boolean
    category?: string
    queries?: string[]
    estimatedTime?: number
  } | null

  subtasks: Subtask[]      // If needs breakdown

  priority: {
    score: number          // 0-100
    label: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW'
    reason: string
  }

  estimatedTime: {
    original: number       // From OpenSpec
    adjusted: number       // With buffer for complexity/risk
    buffer: number         // Percentage added
  }

  // NEW in v1.4.0: Incremental Testing
  testingStrategy: {
    type: 'standard' | 'incremental'
    reason: string
    milestones?: Milestone[]  // Only if type = 'incremental'
  }
}

interface Milestone {
  id: number                  // Sequential (1, 2, 3, ...)
  name: string               // Short description
  testScope: string          // What to test (clear, specific)
  exitCriteria: string[]     // Checklist to validate
  estimatedTime: number      // Minutes (derived from task estimate)
  retryLimit: number         // Always 2
}
```

---

## 🔄 Usage in /csetup

**Integration Point: STEP 3.5 (after task detection, before template selection)**

```typescript
// STEP 3.5: Analyze Tasks (TaskMaster-style + Incremental Testing)

const tasks = parseTasksFromMd(tasksContent)
const analyzedTasks = []

for (const task of tasks) {
  const complexity = calculateComplexity(task)
  const dependencies = detectDependencies(task, tasks)
  const risk = assessRisk(task, complexity)
  const research = detectResearchNeeds(task)
  const needsBreakdown = needsSubtaskBreakdown(task, complexity)
  const subtasks = needsBreakdown ? generateSubtasks(task) : []
  const priority = calculatePriority(task, { complexity, dependencies, risk })

  // NEW: Detect testing strategy
  const metadata = { complexity: { score: complexity }, risk, dependencies }
  const testingStrategy = detectTestingStrategy(task, metadata)

  // NEW: Generate milestones if incremental
  let milestones = []
  if (testingStrategy.type === 'incremental') {
    const adjustedTime = adjustTimeForComplexity(task.estimatedTime, complexity, risk)
    milestones = generateMilestones(task, {
      ...metadata,
      complexity: { score: complexity, level: getComplexityLevel(complexity) },
      estimatedTime: { adjusted: adjustedTime }
    })
  }

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
      mitigation: generateMitigation(risk, task)
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
    },
    // NEW: Testing strategy
    testingStrategy: {
      type: testingStrategy.type,
      reason: testingStrategy.reason,
      milestones: milestones.length > 0 ? milestones : undefined
    }
  })
}

// Sort by priority
analyzedTasks.sort((a, b) => b.priority.score - a.priority.score)

// Report analysis
const incrementalCount = analyzedTasks.filter(t => t.testingStrategy.type === 'incremental').length

output(`
📊 Task Analysis Complete

Total tasks: ${analyzedTasks.length}
Priority breakdown:
  - CRITICAL: ${analyzedTasks.filter(t => t.priority.label === 'CRITICAL').length}
  - HIGH: ${analyzedTasks.filter(t => t.priority.label === 'HIGH').length}
  - MEDIUM: ${analyzedTasks.filter(t => t.priority.label === 'MEDIUM').length}
  - LOW: ${analyzedTasks.filter(t => t.priority.label === 'LOW').length}

Risk assessment:
  - HIGH risk: ${analyzedTasks.filter(t => t.risk.level === 'HIGH').length}
  - MEDIUM risk: ${analyzedTasks.filter(t => t.risk.level === 'MEDIUM').length}

Research required: ${analyzedTasks.filter(t => t.research?.required).length} tasks

Subtask breakdown: ${analyzedTasks.filter(t => t.subtasks.length > 0).length} tasks expanded

🔄 Testing Strategy (NEW):
  - Incremental: ${incrementalCount} tasks (with milestones)
  - Standard: ${analyzedTasks.length - incrementalCount} tasks
`)
```

---

## 📖 Helper Functions

```typescript
function extractEntity(description: string): string {
  // Extract main entity (User, Post, Comment, etc.)
  const match = description.match(/\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b/)
  return match ? match[1] : 'entity'
}

function extractEntities(description: string): string[] {
  const entities = description.match(/\b([A-Z][a-z]+)\b/g) || []
  return [...new Set(entities)] // Remove duplicates
}

function extractTechnology(description: string): string {
  // Extract tech names (React, Next.js, Prisma, etc.)
  const techPattern = /\b(React|Next\.js|Prisma|PostgreSQL|Redis|TypeScript|etc\.)\b/i
  const match = description.match(techPattern)
  return match ? match[1] : 'technology'
}

function extractServices(description: string): string[] {
  // Extract service/API names
  const services = description.match(/\b([A-Z][a-z]+(?:\s+API)?)\b/g) || []
  return services.slice(0, 2) // First two
}

function getComplexityLevel(score: number): string {
  if (score <= 3) return 'Simple'
  if (score <= 6) return 'Moderate'
  if (score <= 8) return 'Complex'
  return 'Critical'
}

function adjustTimeForComplexity(time: number, complexity: number, risk: RiskLevel): number {
  let adjusted = time

  // Add buffer for complexity
  if (complexity >= 7) adjusted *= 1.5
  else if (complexity >= 5) adjusted *= 1.3

  // Add buffer for risk
  if (risk.level === 'HIGH') adjusted *= 1.5
  else if (risk.level === 'MEDIUM') adjusted *= 1.2

  return Math.ceil(adjusted)
}

function calculateBuffer(complexity: number, risk: RiskLevel): number {
  let buffer = 0

  if (complexity >= 7) buffer += 50
  else if (complexity >= 5) buffer += 30

  if (risk.level === 'HIGH') buffer += 50
  else if (risk.level === 'MEDIUM') buffer += 20

  return buffer
}
```

---

## 🧪 UX Testing Phase Injection (v2.7.0)

> **NEW:** Auto-inject Phase 1.5 (UX Testing) after uxui-frontend phase

### Purpose

Ensure UI is tested from user perspectives before proceeding to backend development.

### Detection Logic

```typescript
function shouldInjectUXTesting(phases: Phase[]): boolean {
  // Check if any phase uses uxui-frontend agent
  return phases.some(p => p.agent === 'uxui-frontend')
}
```

### Injection Logic

```typescript
function injectUXTestingPhase(phases: Phase[], context?: ChangeContext): Phase[] {
  // Step 1: Check if should inject
  if (!shouldInjectUXTesting(phases)) {
    return phases // No UI work, skip injection
  }

  // Step 2: Check skip conditions (optional context)
  if (context && shouldSkipUXTesting(phases, context)) {
    return phases // Skip due to context conditions
  }

  // Step 3: Find the last uxui-frontend phase
  const lastUxuiFrontendIndex = phases
    .map((p, i) => p.agent === 'uxui-frontend' ? i : -1)
    .filter(i => i >= 0)
    .pop()

  if (lastUxuiFrontendIndex === undefined) {
    return phases
  }

  // Step 4: Create UX Testing phase
  const uxTestingPhase: Phase = {
    number: `${phases[lastUxuiFrontendIndex].number}.5`, // e.g., "1.5"
    name: 'UX Testing',
    agent: 'ux-tester',
    estimatedTime: 30,
    metadata: ['approval-gate', 'user-testing', 'persona-based'],
    requires_approval: true,
    description: 'Test UI from user perspectives before backend development'
  }

  // Step 5: Insert after the last uxui-frontend phase
  const newPhases = [...phases]
  newPhases.splice(lastUxuiFrontendIndex + 1, 0, uxTestingPhase)

  // Step 6: Renumber subsequent phases if needed
  return renumberPhases(newPhases)
}

function renumberPhases(phases: Phase[]): Phase[] {
  // Keep .5 phases as-is, renumber whole numbers
  let wholeNumber = 1

  return phases.map(phase => {
    if (phase.number.toString().includes('.5')) {
      return phase // Keep .5 as-is
    }

    const newPhase = { ...phase, number: wholeNumber }
    wholeNumber++
    return newPhase
  })
}
```

### Integration Point

**In `/csetup` command, after phase generation:**

```typescript
// STEP 4: Generate phases from template
let phases = generatePhasesFromTemplate(templateName, analyzedTasks)

// STEP 4.5: Inject UX Testing phase (NEW v2.7.0)
phases = injectUXTestingPhase(phases)

output(`
📊 Phases Generated:
${phases.map(p => `   Phase ${p.number}: ${p.name} (${p.agent})`).join('\n')}

${phases.some(p => p.agent === 'ux-tester') ?
  '🧪 UX Testing phase auto-injected after uxui-frontend' : ''}
`)

// STEP 5: Write phases.md
writePhasesFile(phases, changeId)
```

### Output Example

**Before injection:**
```
Phase 1: Frontend Mockup (uxui-frontend)
Phase 2: Backend API (backend)
Phase 3: Database Schema (database)
Phase 4: Frontend Integration (frontend)
Phase 5: Testing (test-debug)
```

**After injection:**
```
Phase 1: Frontend Mockup (uxui-frontend)
Phase 1.5: UX Testing (ux-tester) ← AUTO-INJECTED
Phase 2: Backend API (backend)
Phase 3: Database Schema (database)
Phase 4: Frontend Integration (frontend)
Phase 5: Testing (test-debug)
```

### Approval Gate Behavior

When `/cdev` reaches Phase 1.5:

1. `ux-tester` agent runs and generates report
2. Workflow **PAUSES** - waits for user
3. User options:
   - `approve` → Continue to Phase 2
   - `reject [feedback]` → Loop back to Phase 1

```
Phase 1 (uxui-frontend) ──► Phase 1.5 (ux-tester) ──► [PAUSE]
        ▲                                                │
        │                                                ▼
        └──────────── reject ◄────────────────── User Decision
                                                         │
                                                         ▼
                                               approve ──► Phase 2
```

### Skip Conditions

**Do NOT inject UX Testing if:**

```typescript
function shouldSkipUXTesting(phases: Phase[], context: ChangeContext): boolean {
  // 1. No UI work detected (redundant with shouldInjectUXTesting but kept for clarity)
  if (!phases.some(p => p.agent === 'uxui-frontend')) {
    return true
  }

  // 2. Backend-only or API-only change (detected from proposal/tasks)
  const changeType = detectChangeType(context.proposal, context.tasks)
  if (changeType === 'backend-only' || changeType === 'api-only') {
    return true
  }

  // 3. User explicitly disabled (via flags.json)
  if (context.flags?.skip_ux_testing === true) {
    return true
  }

  // 4. Minor UI fix (average complexity < 3)
  const uiPhases = phases.filter(p => p.agent === 'uxui-frontend')
  if (uiPhases.length > 0) {
    const avgComplexity = uiPhases.reduce((sum, p) => sum + (p.complexity || 5), 0) / uiPhases.length
    if (avgComplexity < 3) {
      return true
    }
  }

  return false
}

// Helper: Detect change type from content
function detectChangeType(proposal: string, tasks: string): string {
  const content = `${proposal} ${tasks}`.toLowerCase()

  // Check for UI indicators
  const hasUI = content.match(/landing|page|component|ui|frontend|form|button|modal|dashboard/i)

  // Check for backend-only indicators
  const isBackendOnly = content.match(/api.only|backend.only|no.ui|cli|cron|migration|script/i)

  if (isBackendOnly && !hasUI) return 'backend-only'
  if (!hasUI) return 'api-only'

  return 'full-stack' // default
}
```

---

**This framework transforms simple tasks.md into intelligent, analyzed workflows! 🚀**
