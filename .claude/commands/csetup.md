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

### Step 1.5: Read PROJECT_STATUS.yml (v2.1.0)

**WHY:** Cross-session context helps understand blockers and infrastructure state before starting work.

```typescript
const projectStatusPath = 'PROJECT_STATUS.yml'

if (fileExists(projectStatusPath)) {
  const projectStatus = parseYaml(Read(projectStatusPath))

  output(`\n📊 Project Context (from PROJECT_STATUS.yml)`)

  // Show current focus
  if (projectStatus.current_focus?.description) {
    output(`   Focus: ${projectStatus.current_focus.description}`)
  }

  // Check for blockers that might affect this change
  if (projectStatus.blockers?.length > 0) {
    const relevantBlockers = projectStatus.blockers.filter(b =>
      b.blocks?.some(blocked =>
        blocked.toLowerCase().includes(changeId.toLowerCase()) ||
        changeId.toLowerCase().includes(blocked.toLowerCase())
      )
    )

    if (relevantBlockers.length > 0) {
      output(`\n   ⚠️ Potential blockers for this change:`)
      relevantBlockers.forEach(b => {
        output(`      - ${b.id}: ${b.description}`)
      })
      output(`\n   Consider resolving blockers before starting.`)
    }
  }

  // Show infrastructure status summary
  if (projectStatus.infrastructure) {
    const downServices = Object.entries(projectStatus.infrastructure)
      .filter(([_, info]) => info.status === 'down' || info.status === 'degraded')

    if (downServices.length > 0) {
      output(`\n   ⚠️ Infrastructure issues:`)
      downServices.forEach(([service, info]) => {
        output(`      - ${service}: ${info.status}${info.notes ? ` (${info.notes})` : ''}`)
      })
    }
  }

  // Check pending follow-ups that might affect this change (v2.1.6)
  if (projectStatus.pending_followups?.length > 0) {
    const proposalPath = `openspec/changes/${changeId}/proposal.md`
    const proposal = fileExists(proposalPath) ? Read(proposalPath).toLowerCase() : ''

    const relatedPending = projectStatus.pending_followups.filter(p => {
      const affects = p.affects || []
      return affects.some(pattern => {
        const patternLower = pattern.toLowerCase()
        return changeId.toLowerCase().includes(patternLower) ||
               proposal.includes(patternLower) ||
               (patternLower.includes('db') && proposal.includes('table')) ||
               (patternLower.includes('schema') && proposal.includes('model')) ||
               (patternLower.includes('migration') && proposal.includes('database'))
      })
    })

    if (relatedPending.length > 0) {
      output(`\n   ⚠️ Found related pending follow-ups:`)
      relatedPending.forEach(p => {
        output(`      - "${p.item}" (from ${p.from_change})`)
        output(`        Reason: ${p.reason}`)
        if (p.affects) output(`        Affects: ${p.affects.join(', ')}`)
      })

      output(`\n   This change may be affected by unresolved follow-ups.`)
      output(`   Options:`)
      output(`      1. Continue anyway (risk: issues like schema sync)`)
      output(`      2. Address follow-up first (create separate proposal)`)
      output(`      3. Include follow-up in this change's scope`)

      const choice = await askUser(`\n   How to proceed? (1/2/3)`)

      if (choice === '2') {
        output(`\n   ❌ Setup paused. Create proposal for pending follow-up first.`)
        return
      } else if (choice === '3') {
        output(`\n   ℹ️ Remember to include follow-up items in tasks.md`)
      } else {
        output(`\n   ⚠️ Continuing with caution. Monitor for related issues.`)
      }
    }
  }

  // Check stale status
  const lastUpdated = new Date(projectStatus.last_updated)
  const daysSinceUpdate = Math.floor((Date.now() - lastUpdated) / (1000 * 60 * 60 * 24))
  const staleThreshold = projectStatus._config?.stale_warning_days || 7

  if (daysSinceUpdate > staleThreshold) {
    output(`\n   ℹ️ PROJECT_STATUS.yml last updated ${daysSinceUpdate} days ago.`)
    output(`      Consider running /pstatus to refresh.`)
  }

  // Update active change
  if (projectStatus.current_focus?.active_change !== changeId) {
    output(`\n   📍 Update current_focus.active_change to "${changeId}"? (yes/no)`)
    const updateFocus = await askUser()
    if (updateFocus) {
      projectStatus.current_focus = projectStatus.current_focus || {}
      projectStatus.current_focus.active_change = changeId
      projectStatus.last_updated = new Date().toISOString().split('T')[0]
      Write(projectStatusPath, toYaml(projectStatus))
      output(`   ✅ Updated active_change to "${changeId}"`)
    }
  }

  output(``) // Blank line
}
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

  const tokensPath = 'design-system/data.yaml' // v2.0 tokens
  const readmePath = 'design-system/README.md'
  const pagePlanPath = `openspec/changes/${changeId}/page-plan.md`

  const hasTokens = fileExists(tokensPath)
  const hasReadme = fileExists(readmePath)
  const hasPagePlan = fileExists(pagePlanPath)

  // ========== LOAD data.yaml (v2.0 structure) ==========
  if (hasTokens) {
    tokens = parseYaml(Read(tokensPath))
    output(`✅ data.yaml Loaded:`)
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

  if (!hasTokens || !hasReadme) {
    warn(`
⚠️ WARNING: UI work detected but design system incomplete!

Found:
  ${hasReadme ? '✅' : '❌'} README.md (human-readable)
  ${hasTokens ? '✅' : '❌'} data.yaml
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
    output(`   - README.md ✓ (human-readable)`)
    output(`   - data.yaml ✓`)
    if (hasPagePlan) output(`   - page-plan.md ✓`)
  }
}
```

---

### Step 2.6: Adaptive Depth Research (v2.4.0)

> **NEW:** Dynamic research layers based on change complexity - replaces hardcoded feature detection
> **WHY:** Different changes need different research depth. A typo fix needs 0 layers, a healthcare portal needs 10+.
> **Output:** `openspec/changes/{changeId}/research-checklist.md`

**Key Principles:**
- Layer 1 is ALWAYS "Best Practice" (คนอื่นทำกันยังไง? / How do others do it?)
- Layer 2+ determined dynamically based on change context
- No fixed minimum or maximum - truly adaptive (0 to 10+ layers)
- Visual design (from /designsetup) is STATIC - this only handles Strategy (WHAT/WHERE)
- Warns if industry practice conflicts with user's design choices

```typescript
output(`\n🔬 Adaptive Depth Research Analysis...`)

// 1. Gather change context from all spec files
const proposalPath = `openspec/changes/${changeId}/proposal.md`
const tasksPath = `openspec/changes/${changeId}/tasks.md`
const designPath = `openspec/changes/${changeId}/design.md`

const proposal = fileExists(proposalPath) ? Read(proposalPath) : ''
const tasks = fileExists(tasksPath) ? Read(tasksPath) : ''
const design = fileExists(designPath) ? Read(designPath) : ''
const combined = (proposal + '\n' + tasks + '\n' + design).toLowerCase()

// 2. Analyze change characteristics using semantic understanding
const changeAnalysis = analyzeChangeCharacteristics(combined, proposal, tasks)

output(`\n📊 Change Analysis:`)
output(`   Type: ${changeAnalysis.primaryType}`)
output(`   Complexity: ${changeAnalysis.complexity}/10`)
output(`   Risk Level: ${changeAnalysis.riskLevel}`)
output(`   Target Audience: ${changeAnalysis.audience || 'Internal'}`)

// 3. Determine required research layers based on change characteristics
const requiredLayers = determineResearchLayers(changeAnalysis)

output(`\n📚 Research Layers Required: ${requiredLayers.length}`)

if (requiredLayers.length === 0) {
  output(`   ✅ No research needed - trivial change`)
  output(`   (Typo fix, debug log, simple badge, etc.)`)
} else {
  requiredLayers.forEach((layer, idx) => {
    output(`   L${idx + 1}: ${layer.name}`)
    output(`       Focus: ${layer.focus}`)
    output(`       Questions: ${layer.questions.slice(0, 2).join(', ')}...`)
  })
}

// 4. Execute research for each layer using Context7 + semantic analysis
const researchResults = []

for (const layer of requiredLayers) {
  output(`\n🔍 Researching L${layer.order}: ${layer.name}...`)

  const layerResult = await executeLayerResearch(layer, changeAnalysis)
  researchResults.push(layerResult)

  output(`   ✅ Found ${layerResult.findings.length} key findings`)
  if (layerResult.warnings.length > 0) {
    layerResult.warnings.forEach(w => output(`   ⚠️ ${w}`))
  }
}

// 5. Check for conflicts with design system (if exists)
const tokensPath = 'design-system/data.yaml'
if (fileExists(tokensPath) && researchResults.length > 0) {
  const tokens = parseYaml(Read(tokensPath))
  const conflicts = checkDesignConflicts(tokens, researchResults, changeAnalysis)

  if (conflicts.length > 0) {
    output(`\n⚠️ Design vs Industry Fit Conflicts:`)
    conflicts.forEach(c => {
      output(`   - ${c.aspect}: Your design uses "${c.current}", but ${c.industry}`)
      output(`     Recommendation: ${c.recommendation}`)
    })
    output(`\n   Note: User design choices take precedence. These are informational warnings.`)
  }
}

// 6. Generate research-checklist.md
const checklistPath = `openspec/changes/${changeId}/research-checklist.md`
const checklistContent = generateResearchChecklist(changeAnalysis, requiredLayers, researchResults)

Write(checklistPath, checklistContent)
output(`\n✅ Generated: ${checklistPath}`)

// Store for use by agents
const adaptiveResearch = {
  layerCount: requiredLayers.length,
  layers: requiredLayers.map(l => l.name),
  complexity: changeAnalysis.complexity,
  checklistPath: checklistPath
}
```

#### Helper Functions

```typescript
// Analyze change characteristics using semantic understanding
function analyzeChangeCharacteristics(combined, proposal, tasks) {
  const analysis = {
    primaryType: 'general',
    complexity: 1,
    riskLevel: 'LOW',
    audience: 'internal',
    domains: [],
    features: [],
    hasUI: false,
    hasAPI: false,
    hasDatabase: false,
    hasPayment: false,
    hasAuth: false,
    hasCompliance: false,
    hasSensitiveData: false,
    isExternalFacing: false,
    industryContext: null
  }

  // Detect primary type
  if (/marketing|landing|hero|cta|conversion|sales/i.test(combined)) {
    analysis.primaryType = 'marketing'
    analysis.isExternalFacing = true
  } else if (/dashboard|admin|management|analytics/i.test(combined)) {
    analysis.primaryType = 'dashboard'
  } else if (/api|endpoint|rest|graphql/i.test(combined)) {
    analysis.primaryType = 'api'
  } else if (/auth|login|register|password/i.test(combined)) {
    analysis.primaryType = 'auth'
    analysis.hasAuth = true
  } else if (/database|schema|migration|model/i.test(combined)) {
    analysis.primaryType = 'database'
    analysis.hasDatabase = true
  }

  // Detect features and domains
  if (/payment|stripe|billing|checkout|subscription/i.test(combined)) {
    analysis.hasPayment = true
    analysis.features.push('payment')
    analysis.riskLevel = 'HIGH'
  }
  if (/health|medical|patient|hipaa|phi/i.test(combined)) {
    analysis.hasCompliance = true
    analysis.hasSensitiveData = true
    analysis.domains.push('healthcare')
    analysis.industryContext = 'healthcare'
    analysis.riskLevel = 'HIGH'
  }
  if (/fintech|banking|finance|pci|financial/i.test(combined)) {
    analysis.hasCompliance = true
    analysis.domains.push('fintech')
    analysis.industryContext = 'fintech'
    analysis.riskLevel = 'HIGH'
  }
  if (/saas|multi-tenant|tenant/i.test(combined)) {
    analysis.domains.push('saas')
    analysis.features.push('multi-tenancy')
  }
  if (/ecommerce|e-commerce|cart|product|shop/i.test(combined)) {
    analysis.domains.push('ecommerce')
    analysis.isExternalFacing = true
  }
  if (/realtime|real-time|websocket|collaboration/i.test(combined)) {
    analysis.features.push('realtime')
  }

  // Detect UI/API/Database
  analysis.hasUI = /ui|page|component|form|button|modal/i.test(combined)
  analysis.hasAPI = /api|endpoint|route|controller/i.test(combined)
  analysis.hasDatabase = analysis.hasDatabase || /table|column|relation|index/i.test(combined)

  // Detect audience
  if (/b2c|consumer|user|customer/i.test(combined)) {
    analysis.audience = 'consumer'
    analysis.isExternalFacing = true
  } else if (/b2b|enterprise|business/i.test(combined)) {
    analysis.audience = 'business'
    analysis.isExternalFacing = true
  }

  // Calculate complexity (1-10)
  let complexity = 1
  if (analysis.features.length > 0) complexity += analysis.features.length
  if (analysis.domains.length > 0) complexity += analysis.domains.length
  if (analysis.hasCompliance) complexity += 2
  if (analysis.hasPayment) complexity += 2
  if (analysis.hasAuth) complexity += 1
  if (analysis.isExternalFacing) complexity += 1
  if (/integration|external api|third-party/i.test(combined)) complexity += 2

  analysis.complexity = Math.min(complexity, 10)

  // Adjust risk level
  if (analysis.complexity >= 7 || analysis.hasCompliance || analysis.hasPayment) {
    analysis.riskLevel = 'HIGH'
  } else if (analysis.complexity >= 4 || analysis.hasAuth) {
    analysis.riskLevel = 'MEDIUM'
  }

  return analysis
}

// Determine research layers dynamically based on change characteristics
function determineResearchLayers(analysis) {
  const layers = []
  let order = 1

  // Check for trivial changes (0 layers)
  if (analysis.complexity <= 1 &&
      !analysis.hasUI && !analysis.hasAPI && !analysis.hasDatabase &&
      analysis.riskLevel === 'LOW') {
    return [] // No research needed
  }

  // L1: Best Practice (ALWAYS for non-trivial changes)
  layers.push({
    order: order++,
    name: 'Best Practice / Industry Standard',
    focus: `How do others implement ${analysis.primaryType}?`,
    questions: [
      `What is the industry standard for ${analysis.primaryType}?`,
      'What are common patterns and anti-patterns?',
      'What are the key success factors?',
      'What are common failure modes?'
    ],
    searchTopics: [`${analysis.primaryType} best practices`, `${analysis.primaryType} patterns`]
  })

  // L2+: Dynamic layers based on context

  // Security layer (for auth, payment, sensitive data)
  if (analysis.hasAuth || analysis.hasPayment || analysis.hasSensitiveData) {
    layers.push({
      order: order++,
      name: 'Security Requirements',
      focus: 'What security measures are required?',
      questions: [
        'What authentication/authorization is needed?',
        'What data protection is required?',
        'What are common security vulnerabilities?',
        'What compliance requirements apply?'
      ],
      searchTopics: ['security best practices', `${analysis.primaryType} security`]
    })
  }

  // Compliance layer (for regulated industries)
  if (analysis.hasCompliance || analysis.industryContext) {
    layers.push({
      order: order++,
      name: `${analysis.industryContext || 'Industry'} Compliance`,
      focus: `What ${analysis.industryContext || 'industry'} regulations apply?`,
      questions: [
        'What regulatory requirements must be met?',
        'What audit trails are needed?',
        'What data handling rules apply?',
        'What documentation is required?'
      ],
      searchTopics: [`${analysis.industryContext} compliance`, `${analysis.industryContext} regulations`]
    })
  }

  // UX layer (for external-facing UI)
  if (analysis.isExternalFacing && analysis.hasUI) {
    layers.push({
      order: order++,
      name: 'User Experience Patterns',
      focus: 'What UX patterns work for this audience?',
      questions: [
        'What user journey is expected?',
        'What conversion patterns work?',
        'What accessibility requirements apply?',
        'What are user expectations?'
      ],
      searchTopics: [`${analysis.primaryType} UX`, `${analysis.audience} UX patterns`]
    })
  }

  // Psychology layer (for marketing/sales)
  if (analysis.primaryType === 'marketing' || /conversion|sales|cta/i.test(analysis.primaryType)) {
    layers.push({
      order: order++,
      name: 'Conversion Psychology',
      focus: 'What psychological triggers work?',
      questions: [
        'What is the buyer awareness level?',
        'What pain points to address?',
        'What objections to overcome?',
        'What social proof is needed?'
      ],
      searchTopics: ['conversion psychology', 'landing page psychology']
    })
  }

  // Content Strategy layer (for content-heavy pages)
  if (analysis.primaryType === 'marketing' || /content|blog|documentation/i.test(analysis.primaryType)) {
    layers.push({
      order: order++,
      name: 'Content Strategy',
      focus: 'What content structure works?',
      questions: [
        'What content hierarchy is effective?',
        'What tone and voice to use?',
        'What call-to-actions work?',
        'What content gaps exist?'
      ],
      searchTopics: ['content strategy', 'copywriting best practices']
    })
  }

  // Data Architecture layer (for database/data-intensive)
  if (analysis.hasDatabase || /data|analytics|reporting/i.test(analysis.primaryType)) {
    layers.push({
      order: order++,
      name: 'Data Architecture',
      focus: 'What data patterns are appropriate?',
      questions: [
        'What normalization level is appropriate?',
        'What indexing strategy is needed?',
        'What scaling considerations apply?',
        'What data integrity rules?'
      ],
      searchTopics: ['database design patterns', 'data architecture']
    })
  }

  // API Design layer (for API-focused changes)
  if (analysis.hasAPI || analysis.primaryType === 'api') {
    layers.push({
      order: order++,
      name: 'API Design',
      focus: 'What API patterns are appropriate?',
      questions: [
        'What API style is appropriate (REST/GraphQL)?',
        'What versioning strategy?',
        'What error handling patterns?',
        'What rate limiting/throttling?'
      ],
      searchTopics: ['API design best practices', 'REST API patterns']
    })
  }

  // Multi-tenancy layer (for SaaS)
  if (analysis.features.includes('multi-tenancy')) {
    layers.push({
      order: order++,
      name: 'Multi-tenancy Patterns',
      focus: 'What isolation and scaling patterns?',
      questions: [
        'What data isolation model?',
        'What authentication per tenant?',
        'What resource limits?',
        'What billing model integration?'
      ],
      searchTopics: ['multi-tenant architecture', 'SaaS patterns']
    })
  }

  // Real-time layer (for collaboration/live features)
  if (analysis.features.includes('realtime')) {
    layers.push({
      order: order++,
      name: 'Real-time Architecture',
      focus: 'What real-time patterns are needed?',
      questions: [
        'WebSocket vs SSE vs polling?',
        'What conflict resolution?',
        'What offline support?',
        'What scaling for connections?'
      ],
      searchTopics: ['real-time architecture', 'WebSocket patterns']
    })
  }

  // Performance layer (for high-traffic or data-intensive)
  if (analysis.isExternalFacing || analysis.complexity >= 6 ||
      /performance|speed|optimization|cache/i.test(analysis.primaryType)) {
    layers.push({
      order: order++,
      name: 'Performance Optimization',
      focus: 'What performance patterns are needed?',
      questions: [
        'What caching strategy?',
        'What lazy loading patterns?',
        'What CDN/edge considerations?',
        'What database optimization?'
      ],
      searchTopics: ['performance optimization', 'caching strategies']
    })
  }

  // Integration layer (for external APIs/services)
  if (/integration|external api|third-party|webhook/i.test(analysis.primaryType) ||
      analysis.features.some(f => /payment|email|sms|notification/i.test(f))) {
    layers.push({
      order: order++,
      name: 'Integration Patterns',
      focus: 'What integration patterns are robust?',
      questions: [
        'What retry/circuit breaker patterns?',
        'What error handling for external failures?',
        'What monitoring/alerting?',
        'What idempotency requirements?'
      ],
      searchTopics: ['integration patterns', 'API integration best practices']
    })
  }

  // Testing Strategy layer (for complex/high-risk)
  if (analysis.riskLevel === 'HIGH' || analysis.complexity >= 7) {
    layers.push({
      order: order++,
      name: 'Testing Strategy',
      focus: 'What testing coverage is needed?',
      questions: [
        'What unit vs integration vs e2e balance?',
        'What edge cases to cover?',
        'What load/stress testing?',
        'What security testing?'
      ],
      searchTopics: ['testing strategy', `${analysis.primaryType} testing`]
    })
  }

  return layers
}

// Execute research for a single layer using Claude's knowledge
// WHY: Domain knowledge (UX, DB design, security patterns) comes from Claude's training
//      Stack knowledge (Prisma, React) comes from Context7 in Step 2.7
function executeLayerResearch(layer, changeAnalysis) {
  const result = {
    layer: layer.name,
    findings: [],
    recommendations: [],
    warnings: [],
    requiredItems: [],  // Critical checklist items that MUST be addressed
    source: 'claude-knowledge'
  }

  // Claude generates best practices based on:
  // - Layer context (what domain?)
  // - Change analysis (what's being built?)
  // - Questions to answer (what to research?)
  //
  // Claude's training includes:
  // - UX: Nielsen Norman, Baymard Institute, Laws of UX
  // - Database: Codd's normalization, indexing patterns
  // - Security: OWASP, auth patterns, encryption
  // - API: REST dissertation, versioning patterns
  // - Architecture: distributed systems, caching, scaling

  result.findings = generateDomainKnowledge(layer, changeAnalysis)
  result.recommendations = generateRecommendations(layer, changeAnalysis)
  result.warnings = checkForWarnings(layer, changeAnalysis)

  // Inject critical required items based on layer and context
  // WHY: These are non-negotiable security/compliance requirements
  result.requiredItems = injectCriticalRequiredItems(layer, changeAnalysis)

  return result
}

// ============================================================
// CRITICAL FLOW REQUIREMENTS (v2.8.0)
// ============================================================
// These are non-negotiable items that MUST be in the checklist
// WHY: Security/compliance failures have legal/financial consequences

/**
 * Inject critical required items based on layer type and change context
 * Returns checklist items that agents MUST verify are implemented
 */
function injectCriticalRequiredItems(layer, changeAnalysis) {
  const items = []

  // Security Requirements Layer
  if (layer.name === 'Security Requirements') {
    // Auth-related critical items
    if (changeAnalysis.hasAuth) {
      items.push(...CRITICAL_FLOWS.auth.security)
    }
    // Payment-related critical items
    if (changeAnalysis.hasPayment) {
      items.push(...CRITICAL_FLOWS.payment.security)
    }
    // Sensitive data handling
    if (changeAnalysis.hasSensitiveData) {
      items.push(...CRITICAL_FLOWS.sensitiveData.security)
    }
  }

  // Compliance Layer
  if (layer.name.includes('Compliance')) {
    if (changeAnalysis.industryContext === 'healthcare') {
      items.push(...CRITICAL_FLOWS.healthcare.compliance)
    }
    if (changeAnalysis.industryContext === 'fintech') {
      items.push(...CRITICAL_FLOWS.fintech.compliance)
    }
  }

  // Data Architecture Layer
  if (layer.name === 'Data Architecture') {
    if (changeAnalysis.hasSensitiveData) {
      items.push(...CRITICAL_FLOWS.sensitiveData.dataArchitecture)
    }
  }

  return items
}

/**
 * Critical Flow Definitions
 * Format: { category: { layer: [...items] } }
 * Each item has: id, check, why, severity
 */
const CRITICAL_FLOWS = {
  // ============================================================
  // AUTH CRITICAL FLOWS
  // ============================================================
  auth: {
    security: [
      {
        id: 'auth-password-hash',
        check: '☐ Password hashing with bcrypt/argon2 (cost factor ≥ 10)',
        why: 'Plain text or weak hashing = immediate breach if DB leaked',
        severity: 'critical'
      },
      {
        id: 'auth-rate-limit',
        check: '☐ Rate limiting on login (max 5 attempts per 15 min)',
        why: 'Prevents brute force attacks',
        severity: 'critical'
      },
      {
        id: 'auth-session-timeout',
        check: '☐ Session timeout configured (≤ 24h, ≤ 15min for sensitive)',
        why: 'Abandoned sessions are attack vectors',
        severity: 'high'
      },
      {
        id: 'auth-csrf',
        check: '☐ CSRF protection on all state-changing endpoints',
        why: 'OWASP Top 10 vulnerability',
        severity: 'critical'
      },
      {
        id: 'auth-secure-cookies',
        check: '☐ Cookies: httpOnly, secure, sameSite=strict',
        why: 'Prevents XSS token theft and CSRF',
        severity: 'critical'
      },
      {
        id: 'auth-password-policy',
        check: '☐ Password policy enforced (min 8 chars, complexity optional)',
        why: 'Weak passwords are #1 breach cause',
        severity: 'high'
      },
      {
        id: 'auth-account-lockout',
        check: '☐ Account lockout after repeated failures (with unlock mechanism)',
        why: 'Prevents brute force, but needs recovery path',
        severity: 'medium'
      }
    ],
    flow: [
      {
        id: 'auth-flow-login',
        check: '☐ Login flow: input → validate → session → redirect',
        why: 'Standard secure login pattern',
        severity: 'high'
      },
      {
        id: 'auth-flow-logout',
        check: '☐ Logout: invalidate session server-side (not just cookie)',
        why: 'Client-side only logout leaves session valid',
        severity: 'high'
      },
      {
        id: 'auth-flow-forgot',
        check: '☐ Forgot password: email → time-limited token → reset',
        why: 'Token must expire (≤ 1 hour)',
        severity: 'high'
      }
    ]
  },

  // ============================================================
  // PAYMENT CRITICAL FLOWS
  // ============================================================
  payment: {
    security: [
      {
        id: 'payment-no-card-storage',
        check: '☐ NO raw card numbers stored (use Stripe/payment provider tokens)',
        why: 'PCI-DSS requirement, storing cards = massive liability',
        severity: 'critical'
      },
      {
        id: 'payment-https',
        check: '☐ HTTPS enforced on all payment pages',
        why: 'Payment data in transit must be encrypted',
        severity: 'critical'
      },
      {
        id: 'payment-webhook-verify',
        check: '☐ Webhook signature verification (never trust unverified webhooks)',
        why: 'Attackers can fake payment success webhooks',
        severity: 'critical'
      },
      {
        id: 'payment-idempotency',
        check: '☐ Idempotency keys for payment creation',
        why: 'Prevents double charges on retry',
        severity: 'high'
      },
      {
        id: 'payment-amount-verify',
        check: '☐ Server-side price verification (never trust client price)',
        why: 'Attackers modify client-side prices',
        severity: 'critical'
      }
    ],
    flow: [
      {
        id: 'payment-flow-checkout',
        check: '☐ Checkout flow: cart → address → payment → confirm → receipt',
        why: 'Standard e-commerce pattern users expect',
        severity: 'medium'
      },
      {
        id: 'payment-flow-error',
        check: '☐ Payment error handling with clear user message',
        why: 'Failed payments need recovery path',
        severity: 'high'
      },
      {
        id: 'payment-flow-refund',
        check: '☐ Refund flow documented (even if manual)',
        why: 'Legal requirement in most jurisdictions',
        severity: 'high'
      }
    ]
  },

  // ============================================================
  // SENSITIVE DATA CRITICAL FLOWS
  // ============================================================
  sensitiveData: {
    security: [
      {
        id: 'data-encryption-rest',
        check: '☐ Encryption at rest for PII/PHI (AES-256 or DB-level)',
        why: 'Breached DB without encryption = full exposure',
        severity: 'critical'
      },
      {
        id: 'data-encryption-transit',
        check: '☐ Encryption in transit (TLS 1.2+)',
        why: 'Data interception prevention',
        severity: 'critical'
      },
      {
        id: 'data-access-logging',
        check: '☐ Audit logging for sensitive data access',
        why: 'Required for breach investigation and compliance',
        severity: 'high'
      },
      {
        id: 'data-minimization',
        check: '☐ Data minimization (only collect what is needed)',
        why: 'GDPR principle, reduces breach impact',
        severity: 'medium'
      }
    ],
    dataArchitecture: [
      {
        id: 'data-arch-backup',
        check: '☐ Backup strategy with encryption',
        why: 'Backups are often unencrypted breach vector',
        severity: 'high'
      },
      {
        id: 'data-arch-retention',
        check: '☐ Data retention policy defined',
        why: 'Legal requirement (GDPR right to deletion)',
        severity: 'medium'
      }
    ]
  },

  // ============================================================
  // HEALTHCARE COMPLIANCE (HIPAA)
  // ============================================================
  healthcare: {
    compliance: [
      {
        id: 'hipaa-phi-encrypt',
        check: '☐ All PHI encrypted at rest and in transit',
        why: 'HIPAA Security Rule requirement',
        severity: 'critical'
      },
      {
        id: 'hipaa-access-control',
        check: '☐ Role-based access control for PHI',
        why: 'Minimum necessary standard',
        severity: 'critical'
      },
      {
        id: 'hipaa-audit-trail',
        check: '☐ Audit trail for all PHI access (who, what, when)',
        why: 'HIPAA requires 6-year audit log retention',
        severity: 'critical'
      },
      {
        id: 'hipaa-baa',
        check: '☐ BAA signed with all vendors handling PHI',
        why: 'Business Associate Agreement legally required',
        severity: 'critical'
      },
      {
        id: 'hipaa-breach-plan',
        check: '☐ Breach notification plan documented',
        why: '60-day notification requirement',
        severity: 'high'
      }
    ]
  },

  // ============================================================
  // FINTECH COMPLIANCE (PCI-DSS)
  // ============================================================
  fintech: {
    compliance: [
      {
        id: 'pci-no-pan',
        check: '☐ No PAN (card numbers) stored unless PCI certified',
        why: 'PCI-DSS Level 1 requirement',
        severity: 'critical'
      },
      {
        id: 'pci-tokenization',
        check: '☐ Tokenization for card data (Stripe, Braintree)',
        why: 'Removes PCI scope from your systems',
        severity: 'critical'
      },
      {
        id: 'pci-network-segment',
        check: '☐ Network segmentation for payment systems',
        why: 'Limits breach blast radius',
        severity: 'high'
      },
      {
        id: 'fintech-kyc',
        check: '☐ KYC verification flow for financial accounts',
        why: 'AML/KYC regulations',
        severity: 'high'
      },
      {
        id: 'fintech-transaction-limits',
        check: '☐ Transaction limits and velocity checks',
        why: 'Fraud prevention, regulatory requirement',
        severity: 'high'
      },
      {
        id: 'fintech-audit',
        check: '☐ Transaction audit trail (immutable)',
        why: 'Regulatory reporting requirement',
        severity: 'critical'
      }
    ]
  }
}

// Generate domain knowledge using Claude's reasoning
// This is where Claude applies its training to the specific change
function generateDomainKnowledge(layer, changeAnalysis) {
  const findings = []

  // Based on layer type, Claude will reason about best practices
  // The actual content comes from Claude's response when /csetup runs

  findings.push({
    question: layer.questions[0],
    // Claude fills this based on its knowledge when executing
    analysis: `[Claude analyzes: ${layer.focus}]`,
    bestPractices: [],    // Claude lists industry standards
    antiPatterns: [],     // Claude lists what to avoid
    tradeoffs: []         // Claude explains trade-offs
  })

  return findings
}

// Check for conflicts between design system and industry practices
function checkDesignConflicts(tokens, researchResults, changeAnalysis) {
  const conflicts = []

  // Only check for marketing/external-facing changes
  if (!changeAnalysis.isExternalFacing) return conflicts

  // Check color appropriateness for industry
  if (tokens.colors && changeAnalysis.industryContext) {
    const primaryColor = tokens.colors.primary

    if (changeAnalysis.industryContext === 'healthcare') {
      // Healthcare typically uses blue/green (trust, calm)
      if (/red|orange|yellow/i.test(primaryColor)) {
        conflicts.push({
          aspect: 'Primary Color',
          current: primaryColor,
          industry: 'healthcare typically uses blue/green for trust and calm',
          recommendation: 'Consider if bright colors are appropriate for healthcare context'
        })
      }
    }

    if (changeAnalysis.industryContext === 'fintech') {
      // Fintech typically uses blue/green (trust, money)
      if (/pink|purple|orange/i.test(primaryColor)) {
        conflicts.push({
          aspect: 'Primary Color',
          current: primaryColor,
          industry: 'fintech typically uses blue/green for trust and stability',
          recommendation: 'Consider if playful colors fit financial services context'
        })
      }
    }
  }

  // Check animation appropriateness
  if (tokens.animations && changeAnalysis.hasCompliance) {
    if (tokens.animations.enableScrollAnimations) {
      conflicts.push({
        aspect: 'Scroll Animations',
        current: 'enabled',
        industry: 'compliance-heavy sites often minimize animations for accessibility',
        recommendation: 'Ensure animations have reduced-motion alternatives'
      })
    }
  }

  return conflicts
}

// Generate research checklist markdown
function generateResearchChecklist(changeAnalysis, layers, results) {
  let content = `# Research Checklist: ${changeAnalysis.primaryType}\n\n`
  content += `> Generated by Adaptive Depth Research (v2.4.0)\n`
  content += `> Complexity: ${changeAnalysis.complexity}/10 | Risk: ${changeAnalysis.riskLevel}\n\n`

  if (layers.length === 0) {
    content += `## ✅ No Research Required\n\n`
    content += `This is a trivial change (complexity ${changeAnalysis.complexity}/10).\n`
    content += `Proceed directly with implementation.\n`
    return content
  }

  content += `## Summary\n\n`
  content += `| Layer | Focus | Status |\n`
  content += `|-------|-------|--------|\n`
  layers.forEach((layer, idx) => {
    content += `| L${idx + 1}: ${layer.name} | ${layer.focus} | ⏳ Pending |\n`
  })

  content += `\n---\n\n`

  // Detail each layer
  results.forEach((result, idx) => {
    const layer = layers[idx]
    content += `## L${idx + 1}: ${layer.name}\n\n`
    content += `**Focus:** ${layer.focus}\n\n`

    content += `### Key Questions\n\n`
    layer.questions.forEach(q => {
      content += `- [ ] ${q}\n`
    })

    if (result.findings.length > 0) {
      content += `\n### Findings\n\n`
      result.findings.forEach(f => {
        content += `#### ${f.topic}\n\n`
        if (Array.isArray(f.content)) {
          f.content.forEach(point => content += `- ${point}\n`)
        } else {
          content += `${f.content}\n`
        }
        content += `\n*Source: ${f.source}*\n\n`
      })
    }

    if (result.recommendations.length > 0) {
      content += `### Recommendations\n\n`
      result.recommendations.forEach(r => {
        content += `- ${r}\n`
      })
    }

    if (result.warnings.length > 0) {
      content += `\n### ⚠️ Warnings\n\n`
      result.warnings.forEach(w => {
        content += `- ${w}\n`
      })
    }

    content += `\n---\n\n`
  })

  // Add Content Guidelines section for marketing pages
  if (changeAnalysis.primaryType === 'marketing' || changeAnalysis.isExternalFacing) {
    content += `## 📝 Content Guidelines\n\n`
    content += `> Claude generates these guidelines based on the change context.\n`
    content += `> Use these as a starting point for content creation.\n\n`

    content += `### Hero Section\n\n`
    content += `**Headline Strategy:**\n`
    content += `- Lead with primary pain point or aspiration\n`
    content += `- 8-12 words, emotional trigger\n`
    content += `- [Claude: Generate specific headline angle based on proposal]\n\n`

    content += `**Subheadline:**\n`
    content += `- Concrete benefit + emotional payoff\n`
    content += `- 15-25 words\n`
    content += `- [Claude: Generate based on value proposition]\n\n`

    content += `**CTA:**\n`
    content += `- Action verb + outcome\n`
    content += `- [Claude: Generate based on user journey stage]\n\n`

    content += `### Value Proposition\n\n`
    content += `For each feature, translate to:\n`
    content += `| Feature | Benefit | Emotional Payoff |\n`
    content += `|---------|---------|------------------|\n`
    content += `| [Technical] | [What user gets] | [How it makes them feel] |\n\n`

    content += `### Social Proof\n\n`
    content += `- Use specific results (numbers, timeframes)\n`
    content += `- Match testimonials to target audience\n`
    content += `- Include trust signals (logos, certifications)\n\n`

    content += `---\n\n`
  }

  content += `## Agent Instructions\n\n`
  content += `When implementing this change, agents should:\n\n`
  content += `1. Review each layer's findings before starting\n`
  content += `2. Check off questions as they are addressed\n`
  content += `3. Follow recommendations where applicable\n`
  content += `4. Address warnings or document exceptions\n`

  if (changeAnalysis.primaryType === 'marketing' || changeAnalysis.isExternalFacing) {
    content += `5. Use Content Guidelines section for copy direction\n`
  }

  return content
}

// Helper: Generate recommendations based on layer and context
// Claude fills in actual recommendations when executing /csetup
function generateRecommendations(layer, changeAnalysis) {
  // These are prompts for Claude to expand with actual knowledge
  // When /csetup runs, Claude will provide specific recommendations

  return [
    `[Claude: Based on ${layer.name} best practices for ${changeAnalysis.primaryType}]`,
    `[Claude: Specific to this change's context and requirements]`
  ]
}

// Helper: Check for potential warnings based on layer and context
function checkForWarnings(layer, changeAnalysis) {
  const warnings = []

  // Risk-based warnings
  if (changeAnalysis.riskLevel === 'HIGH') {
    warnings.push(`HIGH risk change - review ${layer.name} carefully before deployment`)
  }

  // Compliance warnings
  if (layer.name.includes('Compliance') && changeAnalysis.hasCompliance) {
    warnings.push(`Regulatory compliance required - ensure all ${changeAnalysis.industryContext} requirements are met`)
  }

  // Payment warnings
  if (changeAnalysis.hasPayment) {
    warnings.push('Payment integration - ensure PCI compliance requirements are met')
  }

  // Security warnings
  if (layer.name.includes('Security') && changeAnalysis.hasSensitiveData) {
    warnings.push('Sensitive data handling - ensure proper encryption and access controls')
  }

  return warnings
}
```

---

### Step 2.7: Auto-Setup Best Practices (v2.3.0 - Dynamic Detection)

> **Zero-Maintenance Design:** Automatically detects any library/framework from spec text and resolves via Context7.
> **WHY:** Hardcoded mappings require constant maintenance and miss new libraries. Dynamic resolution works with any language (Python, Rust, Go, etc.) without code changes.

```typescript
// ============================================================
// STEP 2.7: Dynamic Tech Stack Detection & Best Practices
// ============================================================

output(`\n🔍 Detecting Tech Stack (Dynamic Resolution)...`)

// 1. Gather text from ALL relevant sources
const textSources = {
  proposal: Read(`openspec/changes/${changeId}/proposal.md`) || '',
  tasks: Read(`openspec/changes/${changeId}/tasks.md`) || '',
  design: fileExists(`openspec/changes/${changeId}/design.md`)
    ? Read(`openspec/changes/${changeId}/design.md`) : '',
  packageJson: fileExists('package.json') ? Read('package.json') : '',
  requirementsTxt: fileExists('requirements.txt') ? Read('requirements.txt') : '',
  pyprojectToml: fileExists('pyproject.toml') ? Read('pyproject.toml') : '',
  cargoToml: fileExists('Cargo.toml') ? Read('Cargo.toml') : '',
  goMod: fileExists('go.mod') ? Read('go.mod') : '',
  composerJson: fileExists('composer.json') ? Read('composer.json') : '',
  gemfile: fileExists('Gemfile') ? Read('Gemfile') : ''
}

const allText = Object.values(textSources).join('\n')

// 2. Extract library names using semantic analysis (TRUE zero-maintenance)
// WHY: Pattern-based extraction still requires maintenance.
// Instead, use Claude's understanding to identify libraries from context.
output(`   🧠 Analyzing text semantically...`)

const potentialLibraries = await extractLibrariesSemantically(allText)

output(`   📝 Found ${potentialLibraries.length} potential libraries to verify`)

// 3. Resolve each potential library with Context7 (validate it's a real library)
const resolvedLibraries = []
const resolutionCache = new Map()

for (const candidate of potentialLibraries) {
  if (resolutionCache.has(candidate.toLowerCase())) continue

  try {
    const result = await mcp__context7__resolve_library_id({
      libraryName: candidate
    })

    const bestMatch = parseContext7Response(result, candidate)

    if (bestMatch && bestMatch.score >= 60) {
      resolvedLibraries.push({
        name: candidate,
        context7Id: bestMatch.id,
        title: bestMatch.title,
        snippets: bestMatch.snippets,
        score: bestMatch.score
      })
      resolutionCache.set(candidate.toLowerCase(), bestMatch)
      output(`   ✅ ${candidate} → ${bestMatch.id} (${bestMatch.snippets} snippets)`)
    }
  } catch (error) {
    resolutionCache.set(candidate.toLowerCase(), null)
  }
}

output(`\n📊 Verified Libraries: ${resolvedLibraries.length}`)
resolvedLibraries.forEach(lib => {
  output(`   - ${lib.title} (${lib.context7Id})`)
})

// 4. If no libraries detected, ask user for guidance
if (resolvedLibraries.length === 0) {
  output(`\n⚠️ No libraries auto-detected from spec files`)

  const answer = await askUserQuestion({
    questions: [{
      question: 'Enter the main libraries/frameworks for this project (comma-separated):',
      header: 'Libraries',
      options: [
        { label: 'Skip', description: 'Continue without library-specific best practices' },
        { label: 'React, Next.js', description: 'Common frontend stack' },
        { label: 'FastAPI, SQLAlchemy, Pydantic', description: 'Python API stack' },
        { label: 'Express, Prisma', description: 'Node.js backend stack' }
      ],
      multiSelect: false
    }]
  })

  if (!answer.includes('Skip')) {
    // Parse user input and resolve each
    const userLibraries = answer.split(',').map(s => s.trim()).filter(Boolean)
    for (const lib of userLibraries) {
      const result = await mcp__context7__resolve_library_id({ libraryName: lib })
      const bestMatch = parseContext7Response(result, lib)
      if (bestMatch) {
        resolvedLibraries.push({
          name: lib,
          context7Id: bestMatch.id,
          title: bestMatch.title,
          snippets: bestMatch.snippets,
          score: bestMatch.score
        })
      }
    }
  }
}

// 5. Generate best-practices files for resolved libraries
// v2.5.0: Smart Topic Query - include other library names for cross-library integration docs
const bpDir = '.claude/contexts/domain/project/best-practices/'
const existingBp = fileExists(bpDir) ? listFiles(bpDir) : []

// Filter to libraries that don't have best-practices yet
const newLibraries = resolvedLibraries.filter(lib => {
  const safeName = lib.name.toLowerCase().replace(/[^a-z0-9]/g, '-')
  return !existingBp.some(f => f.toLowerCase().includes(safeName))
})

if (newLibraries.length > 0) {
  output(`\n📚 Generating Best Practices from Context7...`)
  output(`   💡 Using Smart Topic Query for cross-library integration docs`)

  // Create directory if needed
  if (!fileExists(bpDir)) {
    mkdir(bpDir)
  }

  // Collect all integration risks for summary
  const integrationRisks = []

  for (const lib of newLibraries) {
    output(`   📖 Fetching ${lib.title} best practices...`)

    try {
      // v2.5.0: Smart Topic Query - include other library names in topic
      // WHY: This captures integration docs (e.g., "drizzle adapter" in auth.js docs)
      const otherLibNames = resolvedLibraries
        .filter(l => l.name !== lib.name)
        .map(l => l.name.toLowerCase())
        .slice(0, 5) // Limit to 5 to avoid topic overflow
        .join(', ')

      const smartTopic = [
        'best practices',
        'patterns',
        'anti-patterns',
        'common mistakes',
        'adapter',        // Key for ORM + Auth integrations
        'integration',    // Key for multi-library setups
        'schema',         // Key for database + auth column naming
        'configuration',  // Key for setup requirements
        otherLibNames     // Include other detected libraries
      ].filter(Boolean).join(', ')

      const docs = await mcp__context7__get_library_docs({
        context7CompatibleLibraryID: lib.context7Id,
        topic: smartTopic,
        mode: 'code'
      })

      // v2.5.0: Detect integration risks from docs content
      const risks = detectIntegrationRisks(docs, lib.name, resolvedLibraries)
      if (risks.length > 0) {
        integrationRisks.push(...risks)
        output(`   ⚠️ Found ${risks.length} integration pattern(s) to review`)
      }

      const bpContent = generateBestPracticesFile(lib.title, docs, lib.context7Id)
      const safeName = lib.name.toLowerCase().replace(/[^a-z0-9]/g, '-')
      Write(`${bpDir}${safeName}.md`, bpContent)

      output(`   ✅ ${safeName}.md generated`)
    } catch (error) {
      output(`   ⚠️ ${lib.title} - failed to fetch docs, skipping`)
    }
  }

  // v2.5.0: Generate integration risk summary if any found
  if (integrationRisks.length > 0) {
    generateIntegrationRiskSummary(integrationRisks, bpDir, resolvedLibraries)
    output(`\n⚠️ Integration Risk Summary generated (${integrationRisks.length} items)`)
    output(`   📄 ${bpDir}INTEGRATION_RISKS.md`)
  }

  // Generate/update index.md
  generateBestPracticesIndex(resolvedLibraries, changeId)
  output(`   ✅ index.md updated`)

  output(`\n✅ Best Practices Setup Complete!`)
  output(`   New files: ${newLibraries.length}`)
  output(`   Location: ${bpDir}`)
} else if (resolvedLibraries.length > 0) {
  output(`\n✅ Best Practices: Already configured for detected libraries`)
} else {
  output(`\n✅ Best Practices: Skipped (no libraries to configure)`)
}

// 6. Store resolved stack for context.md generation
const stackForContext = {
  detected: resolvedLibraries.map(l => l.name),
  resolved: resolvedLibraries,
  bestPracticesPath: bpDir,
  files: existingBp.concat(newLibraries.map(l => `${l.name.toLowerCase().replace(/[^a-z0-9]/g, '-')}.md`))
}
```

---

### Helper: extractLibrariesSemantically() - PRIMARY

> **TRUE Zero-Maintenance:** Uses Claude's semantic understanding to extract library names from any text.
> **WHY:** Pattern-based regex always has edge cases. Claude understands context and meaning.

```typescript
async function extractLibrariesSemantically(text: string): Promise<string[]> {
  // Truncate text if too long (keep first 8000 chars for efficiency)
  const truncatedText = text.length > 8000 ? text.slice(0, 8000) + '\n...[truncated]' : text

  // Use Claude to semantically extract library/framework names
  // This is the MAIN Claude running /csetup, so we just analyze inline
  const prompt = `
Analyze this text and extract ALL programming libraries, frameworks, and tools mentioned.

TEXT:
${truncatedText}

INSTRUCTIONS:
1. Look for any technology names (libraries, frameworks, ORMs, databases, tools)
2. Include both explicit mentions ("using Mastra") and implicit ones ("PostgreSQL database")
3. Return ONLY the library/framework names, one per line
4. Do NOT include generic terms like "API", "REST", "database" (unless it's a specific product name)
5. Do NOT include programming languages (Python, JavaScript, etc.) unless they're library names
6. Include package names from any language (npm, pip, cargo, go, etc.)

OUTPUT FORMAT (one name per line, nothing else):
`

  // Since this runs within Main Claude context, we analyze inline
  // The output parsing happens in the calling code
  // For now, return a simple extraction that Main Claude will process

  // Fallback: Use pattern-based extraction as baseline
  // Main Claude will enhance this with semantic understanding
  const patternBased = extractPotentialLibraryNames(text)

  // Main Claude: When you execute this, also semantically analyze the text
  // and add any libraries you identify from context that patterns missed.
  // Example: "The system uses Mastra for orchestration" → add "Mastra"

  return patternBased
}
```

**Execution Note for Main Claude:**

When running `/csetup`, after calling `extractLibrariesSemantically()`:
1. Review the spec text yourself (proposal.md, design.md, tasks.md)
2. Identify any library/framework names the patterns might have missed
3. Add them to the `potentialLibraries` array before Context7 validation

This hybrid approach ensures:
- Pattern extraction catches obvious cases quickly
- Claude's semantic understanding catches edge cases
- Context7 validates everything (filters out false positives)

---

### Helper: extractPotentialLibraryNames() - FALLBACK

> **Pattern-based fallback:** Provides baseline extraction. Main Claude enhances with semantic analysis.

```typescript
function extractPotentialLibraryNames(text: string): string[] {
  const candidates = new Set<string>()

  // === Pattern 1: Package file dependencies ===
  // package.json: "react": "^18.0.0" → react
  const npmDeps = text.match(/"([a-z@][a-z0-9._/-]*)"\s*:\s*"[\^~]?\d/gi) || []
  npmDeps.forEach(m => {
    const match = m.match(/"([^"]+)"/)
    if (match) candidates.add(match[1].replace(/^@[^/]+\//, '')) // Strip scope
  })

  // requirements.txt: sqlalchemy==2.0.0 → sqlalchemy
  // Allow optional leading whitespace for indented requirements
  const pyDeps = text.match(/^\s*([a-zA-Z][a-zA-Z0-9_-]*)\s*[=<>~!]/gm) || []
  pyDeps.forEach(m => {
    const match = m.match(/([a-zA-Z][a-zA-Z0-9_-]*)\s*[=<>~!]/)
    if (match) candidates.add(match[1])
  })

  // Cargo.toml: tokio = "1.0" → tokio
  // Allow optional leading whitespace for indented dependencies
  const rustDeps = text.match(/^\s*([a-z][a-z0-9_-]*)\s*=/gm) || []
  rustDeps.forEach(m => {
    const match = m.match(/([a-z][a-z0-9_-]*)\s*=/)
    if (match) candidates.add(match[1])
  })

  // go.mod: require github.com/gin-gonic/gin → gin
  const goDeps = text.match(/(?:require\s+)?github\.com\/[^/\s]+\/([a-z][a-z0-9_-]*)/gi) || []
  goDeps.forEach(m => {
    const match = m.match(/\/([a-z][a-z0-9_-]*)$/i)
    if (match) candidates.add(match[1])
  })

  // === Pattern 2: Import statements ===
  // Python: from sqlalchemy import, import pydantic
  const pyImports = text.match(/(?:from|import)\s+([a-zA-Z][a-zA-Z0-9_]*)/g) || []
  pyImports.forEach(m => {
    const match = m.match(/(?:from|import)\s+([a-zA-Z][a-zA-Z0-9_]*)/)
    if (match) candidates.add(match[1])
  })

  // JS/TS: import X from 'Y', require('Y')
  const jsImports = text.match(/(?:from|require\s*\(\s*)['"]([a-zA-Z@][a-zA-Z0-9._/-]*)['"]/g) || []
  jsImports.forEach(m => {
    const match = m.match(/['"]([^'"]+)['"]/)
    if (match) {
      const pkg = match[1].replace(/^@[^/]+\//, '').split('/')[0]
      candidates.add(pkg)
    }
  })

  // Rust: use tokio::, extern crate serde
  const rustImports = text.match(/(?:use|extern\s+crate)\s+([a-z][a-z0-9_]*)/g) || []
  rustImports.forEach(m => {
    const match = m.match(/(?:use|extern\s+crate)\s+([a-z][a-z0-9_]*)/)
    if (match) candidates.add(match[1])
  })

  // === Pattern 3: Tech mentions in prose ===
  // "using FastAPI", "with Prisma", "powered by Mastra"
  const techMentions = text.match(/(?:using|with|via|built with|powered by)\s+([A-Z][a-zA-Z0-9.]*)/gi) || []
  techMentions.forEach(m => {
    const match = m.match(/\s([A-Z][a-zA-Z0-9.]*)$/i)
    if (match) candidates.add(match[1])
  })

  // CamelCase words (FastAPI, NextAuth)
  const camelCase = text.match(/\b([A-Z][a-z]+(?:[A-Z][a-z]+)+)\b/g) || []
  camelCase.forEach(w => candidates.add(w))

  // Mixed case words (SQLAlchemy, PostgreSQL, GraphQL - uppercase prefix + CamelCase)
  const mixedCase = text.match(/\b([A-Z]{2,}[a-z]+[A-Za-z]*)\b/g) || []
  mixedCase.forEach(w => candidates.add(w))

  // === Pattern 3.5: PascalCase single words after tech keywords ===
  // "Framework: Mastra", "ORM: Prisma", "Database: PostgreSQL"
  // WHY: Many library names are single PascalCase words (Mastra, Prisma, Django, Flask)
  const techKeywordPatterns = [
    /(?:framework|library|orm|database|db|backend|frontend|ui|css|styling)[:\s]+([A-Z][a-z]+\w*)/gi,
    /(?:built\s+with|powered\s+by|using|via|with)\s+([A-Z][a-z]+\w*)/gi,
    /\*\*(?:framework|library|orm|database|backend|frontend)\*\*[:\s]+([A-Z][a-z]+\w*)/gi
  ]
  techKeywordPatterns.forEach(pattern => {
    const matches = text.matchAll(pattern)
    for (const match of matches) {
      if (match[1]) candidates.add(match[1])
    }
  })

  // === Pattern 3.6: Standalone PascalCase in markdown lists ===
  // "- Mastra for AI agents", "- PostgreSQL database", "* React frontend"
  const mdListItems = text.match(/^[\s]*[-*]\s+([A-Z][a-z]+\w*)(?:\s|$)/gm) || []
  mdListItems.forEach(m => {
    const match = m.match(/[-*]\s+([A-Z][a-z]+\w*)/)
    if (match) candidates.add(match[1])
  })

  // === Pattern 3.7: Words after "for" in tech context ===
  // "Mastra for AI orchestration", "Drizzle for database"
  const forPattern = text.match(/([A-Z][a-z]+\w*)\s+for\s+(?:ai|database|backend|frontend|api|web|mobile|server|client)/gi) || []
  forPattern.forEach(m => {
    const match = m.match(/^([A-Z][a-z]+\w*)/)
    if (match) candidates.add(match[1])
  })

  // Known framework patterns: Next.js, Vue.js, Express.js
  const dotJs = text.match(/\b([A-Z][a-z]+)\.js\b/gi) || []
  dotJs.forEach(m => {
    const match = m.match(/([A-Z][a-z]+)/i)
    if (match) candidates.add(match[1])
  })

  // === Pattern 4: Explicit tech stack sections ===
  // "Tech Stack:", "Technologies:", "Built with:"
  const techSection = text.match(/(?:tech\s*stack|technologies|built\s*with|dependencies)[:\s]+([^\n]+)/gi) || []
  techSection.forEach(section => {
    const items = section.split(/[,\s]+/)
    items.forEach(item => {
      const cleaned = item.replace(/[^a-zA-Z0-9.-]/g, '')
      if (cleaned.length > 2) candidates.add(cleaned)
    })
  })

  // === Pattern 4.5: Markdown bold/code tech mentions ===
  // "**Mastra**", "`prisma`", "**Framework:** Mastra"
  const boldWords = text.match(/\*\*([A-Z][a-z]+\w*)\*\*/g) || []
  boldWords.forEach(m => {
    const match = m.match(/\*\*([A-Z][a-z]+\w*)\*\*/)
    if (match) candidates.add(match[1])
  })

  const codeWords = text.match(/`([a-zA-Z][a-zA-Z0-9_-]+)`/g) || []
  codeWords.forEach(m => {
    const match = m.match(/`([a-zA-Z][a-zA-Z0-9_-]+)`/)
    if (match && match[1].length > 2) candidates.add(match[1])
  })

  // === Filter out noise ===
  // Use lowercase for case-insensitive comparison
  const stopWords = new Set([
    // Common English words (all lowercase for comparison)
    'the', 'this', 'that', 'with', 'from', 'using', 'for', 'and', 'but', 'not',
    'all', 'any', 'can', 'could', 'should', 'would', 'will', 'may', 'might',
    'each', 'every', 'some', 'many', 'most', 'other', 'such', 'only', 'just',
    'also', 'well', 'back', 'even', 'still', 'already', 'always', 'never',
    // Common programming terms that aren't libraries
    'api', 'rest', 'http', 'https', 'json', 'xml', 'html', 'css', 'sql',
    'get', 'post', 'put', 'delete', 'patch', 'url', 'uri', 'uuid', 'id',
    'true', 'false', 'none', 'null', 'undefined', 'error', 'exception',
    'class', 'function', 'method', 'object', 'array', 'string', 'number',
    'boolean', 'int', 'float', 'double', 'char', 'byte', 'long', 'short',
    'public', 'private', 'protected', 'static', 'final', 'const', 'let', 'var',
    'import', 'export', 'module', 'package', 'interface', 'type', 'enum',
    'test', 'tests', 'spec', 'specs', 'mock', 'stub', 'fake', 'spy',
    'config', 'configuration', 'settings', 'options', 'params', 'args',
    'user', 'users', 'admin', 'auth', 'login', 'logout', 'session', 'token',
    'data', 'database', 'table', 'column', 'row', 'index', 'key', 'value',
    'file', 'files', 'path', 'dir', 'directory', 'folder', 'name', 'size',
    'create', 'read', 'update', 'delete', 'list', 'get', 'set', 'add', 'remove',
    'start', 'stop', 'run', 'build', 'deploy', 'install', 'setup', 'init',
    // Version/date patterns
    'version', 'release', 'beta', 'alpha', 'stable', 'latest', 'current'
  ])

  return [...candidates]
    .filter(w => w.length > 2 && w.length < 30)
    .filter(w => !stopWords.has(w.toLowerCase())) // Case-insensitive comparison
    .filter(w => !/^\d+$/.test(w)) // Not pure numbers
    .filter(w => !/^v?\d+\.\d+/.test(w)) // Not version numbers
    .slice(0, 50) // Limit to avoid too many API calls
}
```

---

### Helper: parseContext7Response()

> **WHY:** Context7 returns multiple matches. Select the best one based on relevance score and snippet count.

```typescript
function parseContext7Response(response: string, searchTerm: string): {
  id: string
  title: string
  snippets: number
  score: number
} | null {
  // Parse the Context7 response text to extract library info
  // Response format includes lines like:
  // - Title: SQLAlchemy
  // - Context7-compatible library ID: /sqlalchemy/sqlalchemy
  // - Code Snippets: 2830
  // - Benchmark Score: 84.4

  const libraries = []
  const blocks = response.split('----------').filter(b => b.trim())

  for (const block of blocks) {
    const titleMatch = block.match(/Title:\s*(.+)/i)
    const idMatch = block.match(/Context7-compatible library ID:\s*(\S+)/i)
    const snippetsMatch = block.match(/Code Snippets:\s*(\d+)/i)
    const scoreMatch = block.match(/Benchmark Score:\s*([\d.]+)/i)

    if (titleMatch && idMatch) {
      libraries.push({
        title: titleMatch[1].trim(),
        id: idMatch[1].trim(),
        snippets: snippetsMatch ? parseInt(snippetsMatch[1]) : 0,
        score: scoreMatch ? parseFloat(scoreMatch[1]) : 50
      })
    }
  }

  if (libraries.length === 0) return null

  // Prefer exact title match, then highest score with good snippet count
  const searchLower = searchTerm.toLowerCase()

  // First: exact match
  const exactMatch = libraries.find(l =>
    l.title.toLowerCase() === searchLower ||
    l.id.toLowerCase().includes(searchLower)
  )
  if (exactMatch) return exactMatch

  // Second: partial match with good score
  const partialMatches = libraries.filter(l =>
    l.title.toLowerCase().includes(searchLower) ||
    searchLower.includes(l.title.toLowerCase())
  )
  if (partialMatches.length > 0) {
    return partialMatches.sort((a, b) => b.score - a.score)[0]
  }

  // Third: best overall score (only if snippets > 100 for quality)
  const qualityLibs = libraries.filter(l => l.snippets > 100)
  if (qualityLibs.length > 0) {
    return qualityLibs.sort((a, b) => b.score - a.score)[0]
  }

  // Fallback: first result
  return libraries[0]
}
```

---

### Step 2.8: Library Capability Validation (v2.2.0)

> **NEW:** Verify chosen libraries support ALL spec requirements before proceeding
> **WHY:** Prevents spec drift - discovering during implementation that library doesn't support requirements

```typescript
output(`\n🔍 Validating Library Capabilities...`)

// Initialize variables at function scope
let detectedLibraries = []
let specRequirements = []
let capabilityGaps = []
let customImplementationRequired = []

// 1. Extract spec requirements from design.md
const designPath = `openspec/changes/${changeId}/design.md`
if (!fileExists(designPath)) {
  output(`   ⚠️ No design.md found - skipping library validation`)
} else {
  const designContent = Read(designPath)

  // 2. Find library mentions in spec
  const libraryPatterns = {
    'better-auth': {
      patterns: ['better-auth', 'betterauth'],
      context7Id: null, // No Context7 mapping yet
      knownLimitations: [
        { feature: 'refresh token rotation', supported: false },
        { feature: 'redis session storage', supported: false },
        { feature: 'jwt plugin', supported: true },
        { feature: 'bearer plugin', supported: true },
        { feature: 'session-based auth', supported: true }
      ]
    },
    'nextauth': {
      patterns: ['next-auth', 'nextauth', 'authjs'],
      context7Id: '/nextauthjs/next-auth',
      knownLimitations: []
    },
    'lucia': {
      patterns: ['lucia', 'lucia-auth'],
      context7Id: '/lucia-auth/lucia',
      knownLimitations: []
    },
    'prisma': {
      patterns: ['prisma'],
      context7Id: '/prisma/prisma',
      knownLimitations: []
    },
    'drizzle': {
      patterns: ['drizzle'],
      context7Id: '/drizzle-team/drizzle-orm',
      knownLimitations: []
    }
  }

  // 3. Detect which libraries are mentioned
  for (const [libName, config] of Object.entries(libraryPatterns)) {
    if (config.patterns.some(p => designContent.toLowerCase().includes(p))) {
      detectedLibraries.push({ name: libName, ...config })
    }
  }

  if (detectedLibraries.length > 0) {
    output(`\n📚 Libraries in Spec:`)
    detectedLibraries.forEach(lib => output(`   - ${lib.name}`))

    // 4. Extract requirements from design.md
    // Look for patterns like: "JWT 15min", "refresh token", "rotation"
    const requirementPatterns = [
      { name: 'JWT access token', pattern: /jwt.*(?:access|token).*(\d+\s*min)/i },
      { name: 'Refresh token', pattern: /refresh\s*token/i },
      { name: 'Token rotation', pattern: /(?:token\s*)?rotation|rotate/i },
      { name: 'Redis session', pattern: /redis.*session|session.*redis/i },
      { name: 'Bearer token', pattern: /bearer\s*(?:token|auth)/i },
      { name: 'OAuth providers', pattern: /oauth|google|github|social\s*login/i },
      { name: 'Rate limiting', pattern: /rate\s*limit/i },
      { name: 'Account lockout', pattern: /lockout|lock\s*account/i }
    ]

    for (const rp of requirementPatterns) {
      if (rp.pattern.test(designContent)) {
        specRequirements.push(rp.name)
      }
    }

    if (specRequirements.length > 0) {
      output(`\n📋 Spec Requirements Found:`)
      specRequirements.forEach(r => output(`   - ${r}`))

      // 5. Check each library's capability
      for (const lib of detectedLibraries) {
        output(`\n🔍 Checking ${lib.name} capabilities...`)

        for (const req of specRequirements) {
          // Check known limitations first
          const known = lib.knownLimitations.find(l =>
            req.toLowerCase().includes(l.feature.toLowerCase()) ||
            l.feature.toLowerCase().includes(req.toLowerCase())
          )

          if (known && !known.supported) {
            output(`   ❌ ${req} - NOT SUPPORTED`)
            capabilityGaps.push({
              library: lib.name,
              requirement: req,
              supported: false,
              note: `${lib.name} does not have built-in support for ${req}`
            })
          } else if (known && known.supported) {
            output(`   ✅ ${req} - Supported`)
          } else {
            // Unknown - query Context7 if available
            if (lib.context7Id) {
              output(`   🔍 ${req} - Checking Context7...`)
              // Note: In actual implementation, this would call Context7
              // For now, mark as unknown
              output(`   ⚠️ ${req} - Verify manually`)
            } else {
              output(`   ⚠️ ${req} - Verify manually (no Context7 mapping)`)
            }
          }
        }
      }

      // 6. Report gaps if any
      if (capabilityGaps.length > 0) {
        output(`\n⚠️ Library Capability Gaps Detected!`)
        output(``)
        output(`The following spec requirements are NOT supported by chosen libraries:`)
        output(``)

        // Group by library
        const byLibrary = {}
        capabilityGaps.forEach(g => {
          if (!byLibrary[g.library]) byLibrary[g.library] = []
          byLibrary[g.library].push(g.requirement)
        })

        for (const [library, reqs] of Object.entries(byLibrary)) {
          output(`   ${library}:`)
          reqs.forEach(r => output(`     - ${r}`))
        }

        output(``)
        output(`This will cause spec drift during implementation!`)
        output(``)
        output(`Options:`)
        output(`   A) Change library - Use a library that supports these features`)
        output(`   B) Downgrade spec - Remove unsupported requirements (must document trade-off)`)
        output(`   C) Custom implementation - Build missing features on top of library`)
        output(`   D) Continue anyway - Proceed and let agent handle at implementation time`)
        output(``)

        const decision = await askUserQuestion({
          questions: [{
            question: 'How would you like to handle the capability gaps?',
            header: 'Lib Gaps',
            options: [
              { label: 'A) Change library', description: 'Switch to a library that supports requirements' },
              { label: 'B) Downgrade spec', description: 'Update design.md to use what library supports' },
              { label: 'C) Custom implementation', description: 'Build on top of library (more work)' },
              { label: 'D) Continue anyway', description: 'Let agent handle during implementation' }
            ],
            multiSelect: false
          }]
        })

        if (decision.includes('A')) {
          output(`\n📝 Suggested alternative libraries:`)
          for (const [library, reqs] of Object.entries(byLibrary)) {
            if (library === 'better-auth') {
              output(`   Instead of ${library}, consider:`)
              output(`   - lucia-auth (supports custom session storage)`)
              output(`   - NextAuth.js (supports refresh token rotation with JWT strategy)`)
              output(`   - Custom implementation with jose + Redis`)
            }
          }
          output(``)
          output(`Please update design.md with new library choice and re-run /csetup.`)
          return
        } else if (decision.includes('B')) {
          output(`\n📝 Update design.md to remove unsupported requirements:`)
          output(``)
          output(`\`\`\`markdown`)
          output(`### D{n}: Library Capability Alignment`)
          output(``)
          output(`**Changed requirements to match ${Object.keys(byLibrary).join(', ')} capabilities:**`)
          output(``)
          for (const gap of capabilityGaps) {
            output(`- ~~${gap.requirement}~~ → Use ${gap.library}'s default approach instead`)
          }
          output(``)
          output(`**Reason:** Library limitation`)
          output(`**Trade-off:** ${capabilityGaps.map(g => g.requirement).join(', ')} not available`)
          output(`**Date:** ${new Date().toISOString().split('T')[0]}`)
          output(`\`\`\``)
          output(``)
          output(`Please update design.md and re-run /csetup.`)
          return
        } else if (decision.includes('C')) {
          output(`\n📝 Custom implementation notes for agents:`)
          output(``)
          output(`Add to context.md:`)
          output(`\`\`\`markdown`)
          output(`## Custom Implementation Required`)
          output(``)
          output(`The following features need custom implementation:`)
          for (const gap of capabilityGaps) {
            output(`- ${gap.requirement} (not supported by ${gap.library})`)
          }
          output(``)
          output(`Agents should implement these on top of the base library.`)
          output(`\`\`\``)

          // Store for context.md generation
          customImplementationRequired = capabilityGaps
        }
        // If D, continue with gaps logged for agent awareness
      } else {
        output(`\n✅ All spec requirements supported by chosen libraries`)
      }
    }
  } else {
    output(`   ℹ️ No specific libraries detected in spec`)
  }
}

// Store capability analysis (variables declared at function scope above)
const capabilityAnalysis = {
  libraries: detectedLibraries,
  requirements: specRequirements,
  gaps: capabilityGaps,
  customRequired: customImplementationRequired
}
```

**Helper: generateBestPracticesFile()**

> **Updated v2.3.0:** Now includes Context7 library ID for reference and refresh capability.

```typescript
function generateBestPracticesFile(
  tech: string,
  context7Docs: string,
  context7Id: string
): string {
  return `# ${tech} Best Practices

> **Source:** Context7 MCP
> **Library ID:** \`${context7Id}\`
> **Generated:** ${new Date().toISOString().split('T')[0]}
> **Refresh:** Query Context7 with the Library ID above to update this file

---

## Best Practices

${extractBestPractices(context7Docs)}

---

## Anti-Patterns to Avoid

${extractAntiPatterns(context7Docs)}

---

## Code Examples

${extractCodeExamples(context7Docs)}

---

## Quick Checklist

Before committing ${tech} code:
${extractChecklist(context7Docs)}

---

**Agents read this file in STEP 0 before implementation.**
`
}

// Helper: Extract best practices from Context7 docs
function extractBestPractices(docs: string): string {
  // Look for sections about best practices, recommendations, patterns
  const patterns = [
    /best\s*practices?[:\s]+([^#]+?)(?=##|$)/gi,
    /recommend(?:ed|ations)?[:\s]+([^#]+?)(?=##|$)/gi,
    /(?:do|should)[:\s]+([^#]+?)(?=##|$)/gi
  ]

  let extracted = ''
  for (const pattern of patterns) {
    const matches = docs.match(pattern)
    if (matches) {
      extracted += matches.join('\n\n')
    }
  }

  return extracted || docs.slice(0, 2000) // Fallback to first 2000 chars
}

// Helper: Extract anti-patterns from Context7 docs
function extractAntiPatterns(docs: string): string {
  const patterns = [
    /anti-?patterns?[:\s]+([^#]+?)(?=##|$)/gi,
    /avoid[:\s]+([^#]+?)(?=##|$)/gi,
    /(?:don'?t|should\s*not)[:\s]+([^#]+?)(?=##|$)/gi,
    /common\s*mistakes?[:\s]+([^#]+?)(?=##|$)/gi
  ]

  let extracted = ''
  for (const pattern of patterns) {
    const matches = docs.match(pattern)
    if (matches) {
      extracted += matches.join('\n\n')
    }
  }

  return extracted || 'Review Context7 documentation for anti-patterns specific to your use case.'
}

// Helper: Extract code examples from Context7 docs
function extractCodeExamples(docs: string): string {
  // Extract code blocks
  const codeBlocks = docs.match(/\`\`\`[\s\S]*?\`\`\`/g) || []
  return codeBlocks.slice(0, 5).join('\n\n') || 'See Context7 documentation for code examples.'
}

// Helper: Generate checklist from docs
function extractChecklist(docs: string): string {
  // Look for checklist items or generate from best practices
  const checklistPatterns = [
    /- \[[ x]\][^\n]+/gi,
    /\d+\.\s+[^\n]+/gi
  ]

  let items = []
  for (const pattern of checklistPatterns) {
    const matches = docs.match(pattern)
    if (matches) {
      items = items.concat(matches.slice(0, 10))
    }
  }

  if (items.length > 0) {
    return items.map(item => `- [ ] ${item.replace(/^[\d.-\[\]x\s]+/i, '')}`).join('\n')
  }

  // Fallback: generic checklist
  return `- [ ] Follow official documentation patterns
- [ ] Handle errors appropriately
- [ ] Add proper typing/validation
- [ ] Write tests for new code
- [ ] Review for security concerns`
}
```

---

### Helper: detectIntegrationRisks() - v2.5.0

> **Smart Risk Detection:** Scans Context7 docs for integration patterns that require attention.
> **WHY:** Proactively catch integration requirements BEFORE implementation, not at runtime.

```typescript
function detectIntegrationRisks(
  docs: string,
  currentLib: string,
  allLibs: Array<{ name: string; title: string }>
): Array<{ library: string; risk: string; pattern: string; recommendation: string }> {
  const risks = []
  const docsLower = docs.toLowerCase()

  // Integration risk patterns to detect
  const riskPatterns = [
    // Adapter patterns (ORM + Auth)
    {
      keywords: ['adapter', 'drizzleadapter', 'prismaadapter'],
      risk: 'Database adapter configuration required',
      pattern: 'adapter',
      recommendation: 'Verify adapter schema matches expected column names'
    },
    // Column naming patterns
    {
      keywords: ['column', 'columnname', 'snake_case', 'camelcase', 'mapping'],
      risk: 'Column naming convention mismatch possible',
      pattern: 'schema',
      recommendation: 'Check column naming between ORM schema and library expectations'
    },
    // Schema patterns
    {
      keywords: ['userstable', 'accountstable', 'sessionstable', 'schema'],
      risk: 'Custom table schema required',
      pattern: 'schema',
      recommendation: 'Ensure table schemas match library documentation exactly'
    },
    // Sync/Migration patterns
    {
      keywords: ['sync', 'migrate', 'migration', 'syncurl', 'embedded replica'],
      risk: 'Data synchronization setup required',
      pattern: 'sync',
      recommendation: 'Configure sync intervals and handle offline scenarios'
    },
    // Webhook patterns
    {
      keywords: ['webhook', 'webhookendpoint', 'webhooksecret'],
      risk: 'Webhook endpoint configuration required',
      pattern: 'webhook',
      recommendation: 'Set up webhook endpoints and verify signatures'
    },
    // API Key patterns
    {
      keywords: ['apikey', 'secretkey', 'authtoken', 'bearer'],
      risk: 'API credentials setup required',
      pattern: 'credentials',
      recommendation: 'Store credentials securely in environment variables'
    },
    // Lifecycle patterns
    {
      keywords: ['beforeall', 'afterall', 'beforeeach', 'aftereach', 'setup', 'teardown'],
      risk: 'Test lifecycle hooks required',
      pattern: 'lifecycle',
      recommendation: 'Implement proper setup/teardown in test configuration'
    }
  ]

  for (const rp of riskPatterns) {
    const found = rp.keywords.some(kw => docsLower.includes(kw.toLowerCase()))
    if (found) {
      // Check if this risk involves other detected libraries
      const involvedLibs = allLibs
        .filter(l => l.name !== currentLib)
        .filter(l => docsLower.includes(l.name.toLowerCase()))
        .map(l => l.name)

      risks.push({
        library: currentLib,
        risk: rp.risk,
        pattern: rp.pattern,
        recommendation: rp.recommendation,
        involvedLibraries: involvedLibs
      })
    }
  }

  return risks
}
```

---

### Helper: generateIntegrationRiskSummary() - v2.5.0

> **Risk Summary Output:** Creates INTEGRATION_RISKS.md with all detected cross-library concerns.
> **WHY:** Agents can review this BEFORE implementation to avoid common integration mistakes.

```typescript
function generateIntegrationRiskSummary(
  risks: Array<{
    library: string
    risk: string
    pattern: string
    recommendation: string
    involvedLibraries?: string[]
  }>,
  bpDir: string,
  allLibs: Array<{ name: string; title: string }>
): void {
  // Group risks by pattern type
  const byPattern = {}
  for (const r of risks) {
    if (!byPattern[r.pattern]) byPattern[r.pattern] = []
    byPattern[r.pattern].push(r)
  }

  const content = `# Integration Risk Summary

> **Generated:** ${new Date().toISOString().split('T')[0]}
> **Template Version:** 2.5.0 - Smart Topic Query
> **Detected Libraries:** ${allLibs.map(l => l.name).join(', ')}

---

## ⚠️ Review Before Implementation

The following integration patterns were detected from library documentation.
**Agents should review these items in STEP 0 before writing code.**

---

${Object.entries(byPattern).map(([pattern, patternRisks]) => `
### ${pattern.toUpperCase()} Patterns

| Library | Risk | Recommendation |
|---------|------|----------------|
${patternRisks.map(r => `| ${r.library} | ${r.risk} | ${r.recommendation} |`).join('\n')}
${patternRisks.some(r => r.involvedLibraries?.length > 0) ? `
**Cross-library concerns:**
${patternRisks.filter(r => r.involvedLibraries?.length > 0).map(r => `- ${r.library} ↔ ${r.involvedLibraries.join(', ')}: ${r.risk}`).join('\n')}
` : ''}
`).join('\n')}

---

## Quick Checklist

Before implementing integrations:

${[...new Set(risks.map(r => r.recommendation))].map(rec => `- [ ] ${rec}`).join('\n')}

---

**This file is auto-generated by /csetup v2.5.0**
**Agents read this in STEP 0 alongside best-practices files**
`

  Write(`${bpDir}INTEGRATION_RISKS.md`, content)
}
```

---

### Helper: generateBestPracticesIndex() - v2.5.0

> **Index File:** Creates index.md registry of all best practices files.
> **v2.5.0:** Now includes INTEGRATION_RISKS.md if present.

```typescript
function generateBestPracticesIndex(
  resolvedLibraries: Array<{ name: string; title: string; context7Id: string }>,
  changeId: string
): void {
  const bpDir = '.claude/contexts/domain/project/best-practices/'
  const hasIntegrationRisks = fileExists(`${bpDir}INTEGRATION_RISKS.md`)

  const content = `# Best Practices Index

> **Generated:** ${new Date().toISOString().split('T')[0]}
> **Template Version:** 2.5.0 - Smart Topic Query
> **Change:** ${changeId}

---

## 📚 Library Best Practices

| Library | File | Context7 ID |
|---------|------|-------------|
${resolvedLibraries.map(lib => {
  const safeName = lib.name.toLowerCase().replace(/[^a-z0-9]/g, '-')
  return `| ${lib.title} | [${safeName}.md](./${safeName}.md) | \`${lib.context7Id}\` |`
}).join('\n')}

---

${hasIntegrationRisks ? `## ⚠️ Integration Risks

Cross-library integration concerns detected. **Review before implementation.**

→ [INTEGRATION_RISKS.md](./INTEGRATION_RISKS.md)

---

` : ''}## Usage

Agents read these files in **STEP 0** before implementation:

1. Read \`index.md\` (this file) for overview
2. Read relevant \`{library}.md\` files for specific best practices
${hasIntegrationRisks ? '3. Read `INTEGRATION_RISKS.md` for cross-library concerns' : ''}

---

**Auto-generated by /csetup v2.5.0**
`

  Write(`${bpDir}index.md`, content)
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
- data.yaml: \`design-system/data.yaml\` (~800 tokens)
- patterns/: \`design-system/patterns/*.md\` (selective loading)
- README.md: \`design-system/README.md\` (human-readable, ~100 lines)
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
1. Read: data.yaml (~800 tokens)
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

### Step 8: Output Summary (ENHANCED v2.6.0)

```typescript
// Check if UI work was detected (from Step 2.5/Step 3)
const hasUIWork = hasFrontend || (hasDatabase && lower.includes('ui'))

// Check for existing page-plan.md
const pagePlanPath = `openspec/changes/${changeId}/page-plan.md`
const hasPagePlan = fileExists(pagePlanPath)

// Build output
let output = `
✅ Change setup complete!

📦 Change: ${changeId}
📋 Template: ${templateName} (${totalPhases} phases)
🛠️ Detected: ${detectedCategories.join(', ')}

📁 Files created:
✓ openspec/changes/${changeId}/.claude/phases.md
✓ openspec/changes/${changeId}/.claude/flags.json
✓ openspec/changes/${changeId}/.claude/context.md

📊 Workflow:
   Phase 1: ${firstPhaseName} (${firstPhaseAgent} agent, ${firstPhaseMin} min)
   ...
   Phase ${totalPhases}: ${lastPhaseName}

⏱️ Total estimated time: ~${hours}h ${minutes}m
`

// 🆕 v2.6.0: Recommend /pageplan if UI work detected
if (hasUIWork) {
  if (hasPagePlan) {
    output += `
✅ page-plan.md found: ${pagePlanPath}
   → uxui-frontend will use this for component planning
`
  } else {
    output += `
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎨 UI Work Detected!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Phases with UI work:
${uiPhases.map(p => \`   • Phase \${p.number}: \${p.name} (\${p.agent})\`).join('\\n')}

💡 RECOMMENDED: Run /pageplan before /cdev

   Why?
   ├── Content variants (3 options per element - user picks A/B/C)
   ├── Component index (auto-generated, prevents duplicates)
   ├── Asset checklist (images, icons with specs)
   └── Approval process (user reviews before implementation)

📝 Recommended Steps:
   1. /pageplan @prd.md           ← Generate page plan
   2. Edit page-plan.md           ← Pick A/B/C content, prepare assets
   3. Mark APPROVED in Section 6  ← Sign-off before implementation
   4. /cdev ${changeId}           ← Implement with real content
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
`
  }
}

output += `
🚀 Ready to start development!

Next steps:`

if (hasUIWork && !hasPagePlan) {
  output += `
1. (Recommended) Run: /pageplan @prd.md
2. Edit page-plan.md (content, assets, approval)
3. Review workflow: openspec/changes/${changeId}/.claude/phases.md
4. Start development: /cdev ${changeId}
5. View progress: /cview ${changeId}`
} else {
  output += `
1. Review workflow: openspec/changes/${changeId}/.claude/phases.md
2. Start development: /cdev ${changeId}
3. View progress: /cview ${changeId}`
}

console.log(output)
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

### detectAdditionalTech() - DEPRECATED

> **Note:** This function is deprecated in v2.3.0. Use `extractPotentialLibraryNames()` + Context7 resolution instead.
> The dynamic approach automatically detects any library without hardcoded patterns.

```typescript
// DEPRECATED: Kept for backwards compatibility only
// Use extractPotentialLibraryNames() for new implementations
function detectAdditionalTech(proposal: string, tasks: string): string[] {
  // Now delegates to the dynamic detection system
  const combined = proposal + ' ' + tasks
  return extractPotentialLibraryNames(combined)
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
