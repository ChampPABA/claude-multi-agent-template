# Task Analyzer - TaskMaster-style Analysis

> **Enhanced task analysis for intelligent phase generation**
> **Version:** 1.3.0 (TaskMaster Integration)
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
  const hasPagePlan = fileExists(`.changes/${changeContext.changeId}/page-plan.md`)

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
  if (task.type === 'uxui-frontend' && !fileExists('design-system/STYLE_GUIDE.md')) {
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
}
```

---

## 🔄 Usage in /csetup

**Integration Point: STEP 3.5 (after task detection, before template selection)**

```typescript
// STEP 3.5: Analyze Tasks (TaskMaster-style)

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
    }
  })
}

// Sort by priority
analyzedTasks.sort((a, b) => b.priority.score - a.priority.score)

// Report analysis
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

**This framework transforms simple tasks.md into intelligent, analyzed workflows! 🚀**
