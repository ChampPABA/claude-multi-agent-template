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
1. **Parses ALL tasks** from tasks.md (single source of truth)
2. **AI-driven analysis** - complexity, risk, dependencies, agent assignment
3. **Auto-adds best practices** - checkpoints, error handling, verification
4. **Generates incremental milestones** for complex tasks
5. Generates `.claude/phases.md` (agent workflow)
6. Generates `.claude/flags.json` (progress tracking)
7. Generates `.claude/context.md` (change-specific tech)

**v2.0 Architecture:** Template-Free, AI-Driven

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

### Step 1.6: Memory Context Query (v2.2.0 - claude-mem Integration)

**WHY:** Query past work to leverage decisions, avoid repeating mistakes, and maintain consistency.

```typescript
// Extract keywords from change-id and proposal title
const changeKeywords = changeId.split('-').join(' ')
const proposalPath = `openspec/changes/${changeId}/proposal.md`
const proposalContent = fileExists(proposalPath) ? Read(proposalPath) : ''
const proposalTitle = proposalContent.match(/^#\s+(.+)/m)?.[1] || changeId

output(`\n🧠 Querying claude-mem for related past work...`)

// Use mem-search skill to find related observations
// The skill auto-invokes when asking about past work
const queries = [
  `decisions about ${changeKeywords}`,
  `bugs related to ${changeKeywords}`,
  `implementations of ${changeKeywords}`
]

// Claude will auto-invoke mem-search for these queries
// Results are stored for inclusion in research-checklist.md

let pastLearnings = []

// Note: In practice, Main Claude asks these questions naturally
// and mem-search skill returns relevant observations

output(`   Searched for: ${changeKeywords}`)
output(`   (Results will be included in research-checklist.md if relevant)`)
output(``)

// Store for later use in research-checklist.md generation
// pastLearnings will be populated by mem-search results
```

**Integration with research-checklist.md:**

When generating `research-checklist.md` (Step 2.6), include a "Past Learnings" section:

```markdown
## Past Learnings (from claude-mem)

> Related observations from previous sessions:

| ID | Type | Summary | Relevance |
|----|------|---------|-----------|
| #12345 | decision | Chose Drizzle over Prisma | HIGH |
| #12340 | bugfix | Fixed N+1 query in user list | MEDIUM |

### Key Takeaways:
- Use Drizzle patterns established in #12345
- Watch for N+1 queries (see #12340 for solution)
```

If no relevant observations found:
```markdown
## Past Learnings (from claude-mem)

No related past work found. Proceeding fresh.
```

---

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

### Step 2.6: Generate Pre-Work Context (v3.2.0 - Consolidated)

> **EXECUTE THESE STEPS** - Not pseudocode, actual instructions for Main Claude
> **Output:** `openspec/changes/{changeId}/pre-work-context.md`
> **Purpose:** Single file containing ALL context agents need before implementation

**This step consolidates:**
- Adaptive Depth Research (domain knowledge)
- Library Best Practices (from Context7)
- Integration Warnings (cross-library concerns)
- Critical Checklists (security/compliance requirements)

---

#### Step 2.6.1: Analyze Change Characteristics

**Read and analyze these files:**
- `openspec/changes/{changeId}/proposal.md`
- `openspec/changes/{changeId}/tasks.md`
- `openspec/changes/{changeId}/design.md` (if exists)

**Determine:**
1. **Primary Type:** marketing | dashboard | api | auth | database | general
2. **Complexity (1-10):** Based on features, integrations, external APIs
3. **Risk Level:** LOW | MEDIUM | HIGH
4. **Domains:** healthcare, fintech, ecommerce, saas (if applicable)
5. **Features:** payment, auth, multi-tenancy, realtime (if detected)

**Output:**
```
📊 Change Analysis:
   Type: auth
   Complexity: 6/10
   Risk Level: HIGH
   Domains: fintech
   Features: payment, auth
```

---

#### Step 2.6.2: Detect Libraries

**Read these files and identify library/framework names:**
- `package.json` (dependencies, devDependencies)
- `requirements.txt` or `pyproject.toml` (Python)
- `openspec/changes/{changeId}/proposal.md`
- `openspec/changes/{changeId}/design.md`

**Look for:** React, Next.js, Vue, Angular, FastAPI, Express, Django, Prisma, Drizzle, SQLAlchemy, Vitest, Jest, Playwright, Stripe, better-auth, etc.

**Output:**
```
🔍 Libraries Detected:
   - Next.js (from package.json)
   - Prisma (from design.md)
   - better-auth (from tasks.md)
```

---

#### Step 2.6.3: Fetch Best Practices via Context7

**For EACH detected library, call these MCP tools:**

```
1. mcp__context7__resolve-library-id
   Input: { libraryName: "Next.js" }
   Output: Get the context7CompatibleLibraryID (e.g., "/vercel/next.js")

2. mcp__context7__get-library-docs
   Input: {
     context7CompatibleLibraryID: "/vercel/next.js",
     topic: "best practices, patterns, common mistakes, [other-lib-names]",
     mode: "code"
   }
   Output: Documentation with best practices
```

**Smart Topic Query:** Include OTHER detected library names in the topic for cross-library integration docs.
Example: When fetching Prisma docs, include "Next.js, React" in topic.

**Skip if:**
- Library not found in Context7 (note in warnings section instead)
- Library already has cached best practices from previous run

---

#### Step 2.6.4: Determine Research Layers

**Based on change analysis, select relevant research layers:**

| Trigger | Layer | Focus |
|---------|-------|-------|
| Always (complexity > 1) | Best Practices | How do others do this? |
| hasAuth OR hasPayment | Security | Authentication, data protection |
| healthcare OR fintech | Compliance | HIPAA, PCI-DSS, regulations |
| isExternalFacing + hasUI | UX Patterns | User journey, accessibility |
| marketing type | Conversion Psychology | Triggers, objections, social proof |
| hasDatabase | Data Architecture | Normalization, indexing, scaling |
| hasAPI | API Design | REST/GraphQL, versioning, errors |
| payment feature | Payment Flows | PCI compliance, webhooks, idempotency |

**For each selected layer, generate:**
- 3-5 key questions to consider
- 2-3 recommendations from domain knowledge
- Warnings if applicable

---

#### Step 2.6.5: Detect Integration Warnings

**Cross-reference library combinations for known issues:**

| Combination | Warning |
|-------------|---------|
| better-auth + custom JWT | better-auth handles JWT internally - don't duplicate |
| Prisma + serverless | Cold starts can timeout - use connection pooling |
| Next.js 14+ + pages router | App router is default - check which is intended |
| React 19 + old state libs | Check compatibility with new React features |

**Check Context7 docs for integration warnings:**
- Look for "migration", "breaking changes", "compatibility" in docs
- Note version-specific warnings

---

#### Step 2.6.6: Generate Critical Checklist Items

**Based on change characteristics, inject required items:**

**If hasAuth:**
```
☐ Password hashing with bcrypt/argon2 (cost ≥ 10)
☐ Rate limiting on login (max 5 per 15 min)
☐ Session timeout configured
☐ CSRF protection on state-changing endpoints
☐ Cookies: httpOnly, secure, sameSite=strict
```

**If hasPayment:**
```
☐ NO raw card storage (use Stripe tokens)
☐ HTTPS on all payment pages
☐ Webhook signature verification
☐ Idempotency keys for payments
☐ Server-side price verification
```

**If healthcare/fintech:**
```
☐ Encryption at rest for PII/PHI
☐ Audit logging for sensitive data access
☐ Data minimization applied
☐ Compliance documentation prepared
```

---

#### Step 2.6.7: Write pre-work-context.md

**Create `openspec/changes/{changeId}/pre-work-context.md`:**

```markdown
# Pre-Work Context: {changeId}

> **Generated:** {date}
> **Purpose:** All context agents need before implementation
> **Read by:** All agents in STEP 0

---

## 1. Change Analysis

| Aspect | Value |
|--------|-------|
| Type | {primaryType} |
| Complexity | {complexity}/10 |
| Risk Level | {riskLevel} |
| Domains | {domains or "General"} |
| Features | {features or "None detected"} |

---

## 2. Library Best Practices

### {Library 1}

**Source:** Context7 ({context7Id})

**DO:**
- {best practice 1}
- {best practice 2}

**DON'T:**
- {anti-pattern 1}
- {anti-pattern 2}

**Code Example:**
```{lang}
{example code from Context7}
```

### {Library 2}
{repeat structure}

---

## 3. Research Findings

### L1: {Layer Name}

**Key Questions:**
- {question 1}
- {question 2}

**Recommendations:**
- {recommendation based on domain knowledge}

**Warnings:**
- {warning if applicable}

{repeat for each layer}

---

## 4. Integration Warnings

⚠️ **{Library A} + {Library B}:**
{warning description}

⚠️ **{Another combination}:**
{warning description}

---

## 5. Critical Checklist

> **MUST complete before marking phase done**

### Security
{security items if applicable}

### Compliance
{compliance items if applicable}

### Data Protection
{data items if applicable}

---

## 6. Quick Reference

**Package Manager:** {from tech-stack.md or detected}
**Test Command:** {detected test script}
**Build Command:** {detected build script}

---

**Agents: Read this file in STEP 0 before implementation.**
```

---

#### Step 2.6.8: Output Summary

```
✅ Pre-Work Context Generated!

   📄 File: openspec/changes/{changeId}/pre-work-context.md

   Contents:
   - Change Analysis: {type}, {complexity}/10, {risk}
   - Libraries: {count} ({names})
   - Research Layers: {count}
   - Integration Warnings: {count}
   - Critical Checklist Items: {count}

   📌 Agents will read this in STEP 0
```

---

#### Step 2.6.9: Skip Conditions

**Skip this step entirely if:**
- Change is trivial (complexity = 1, risk = LOW, no special features)
- Output: `✅ Pre-Work Context: Skipped (trivial change)`

**Skip library lookup if:**
- No new libraries detected
- All libraries already have Context7 cache

---

**⚠️ IMPORTANT:** This step requires YOU (Main Claude) to:
1. Actually read the spec files
2. Actually call Context7 MCP tools
3. Actually write the pre-work-context.md file

Do NOT treat this as pseudocode. EXECUTE these instructions.

---

### Step 2.7: Library Capability Validation (v2.2.0)

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


---

### Step 3: Task Analyzer v2.0 (Template-Free, AI-Driven)

> **NEW in v2.0:** No templates, no keyword matching. AI analyzes tasks and makes decisions.
> **See:** `.claude/lib/task-analyzer.md` for complete analysis logic

```typescript
const tasksContent = Read(`openspec/changes/${changeId}/tasks.md`)

output(`\n📊 Task Analyzer v2.0 (Template-Free)...`)

// ========== 3.1 Parse ALL Tasks ==========
// Extract EVERY task from tasks.md - nothing is filtered out
const allTasks = parseAllTasks(tasksContent)
output(`   Found: ${allTasks.length} tasks from tasks.md`)

// ========== 3.2 AI-Driven Analysis ==========
// Claude analyzes each task and decides:
// - complexity (1-10)
// - risk (LOW/MEDIUM/HIGH)
// - agent (based on context, NOT keywords)
// - dependencies (blocked_by, blocks)
// - needsIncremental (boolean)

const analyzedTasks = []

output(`\n🔍 Analyzing each task...`)

for (const task of allTasks) {
  // AI reads the task description and context, then decides:

  const analysis = {
    // Complexity: How many operations? Multiple systems? Business logic?
    complexity: /* AI determines 1-10 based on task scope */,

    // Risk: What if this fails? Security/money/data involved?
    risk: /* AI determines LOW/MEDIUM/HIGH */,

    // Agent: Read the full context and decide which agent
    // DO NOT use keyword matching - understand the task
    agent: /* AI decides: uxui-frontend, backend, database, frontend, test-debug, integration */,
    agentReason: /* Brief explanation why this agent */,

    // Dependencies: What must complete first? What's waiting for this?
    dependencies: {
      blockedBy: /* AI identifies blocking tasks */,
      blocks: /* AI identifies tasks this blocks */,
      canParallelize: /* Tasks with no shared dependencies */
    },

    // Incremental: Does this need milestone-based execution?
    // YES if: batch processing, external API, data transformation,
    //         multiple methods, complex form, HIGH risk, complexity >= 7
    needsIncremental: /* AI determines based on task nature */
  }

  analyzedTasks.push({ ...task, ...analysis })
}

// Report analysis
output(`\n📊 Analysis Results:`)
output(`   Complexity: avg ${avgComplexity}/10`)
output(`   Risk: ${highRiskCount} HIGH, ${mediumRiskCount} MEDIUM, ${lowRiskCount} LOW`)
output(`   Agents: ${agentBreakdown}`)

// ========== 3.3 Auto-Add Best Practices ==========
// No warnings - just add what's needed automatically

const additions = []

for (const task of analyzedTasks) {
  // Rule 1: HIGH Risk → Add checkpoint
  if (task.risk === 'HIGH') {
    additions.push({
      id: `${task.id}.verify`,
      description: `Checkpoint: Verify ${task.description} before proceeding`,
      type: 'verification',
      autoAdded: true,
      reason: 'HIGH risk task requires verification checkpoint',
      phase: task.phase
    })
  }

  // Rule 2: External API → Add error handling
  if (task.hasExternalAPI) {
    if (!hasRelatedTask(allTasks, 'error handling')) {
      additions.push({
        id: `${task.id}.errors`,
        description: `Add error handling for external API`,
        type: 'implementation',
        autoAdded: true,
        reason: 'External APIs require error handling',
        phase: task.phase
      })
    }
  }

  // Rule 3: Security-Critical → Add security review
  if (task.isSecurityCritical) {
    additions.push({
      id: `${task.id}.security`,
      description: `Security review: ${task.description}`,
      type: 'verification',
      autoAdded: true,
      reason: 'Security-critical tasks require review',
      phase: task.phase
    })
  }

  // Rule 4: Database Changes → Add migration safety
  if (task.involvesDatabaseChange) {
    additions.push({
      id: `${task.id}.backup`,
      description: `Backup affected tables before ${task.description}`,
      type: 'safety',
      autoAdded: true,
      reason: 'Database changes require backup',
      phase: task.phase
    })
  }
}

output(`   Auto-added: ${additions.length} best practice tasks`)

// ========== 3.4 Generate Incremental Milestones ==========
// For tasks that need milestone-based execution

for (const task of analyzedTasks) {
  if (task.needsIncremental) {
    // AI generates appropriate milestones based on task type:
    // - Repository/Service: method-by-method
    // - External API: mock → single → errors → scale
    // - Batch Processing: 1 → 5 → 20 → 100
    // - Complex Form: architecture → e2e → all fields

    task.milestones = generateMilestones(task)
  }
}

const incrementalCount = analyzedTasks.filter(t => t.milestones).length
const totalMilestones = analyzedTasks.reduce((sum, t) => sum + (t.milestones?.length || 0), 0)
output(`   Incremental: ${incrementalCount} tasks with ${totalMilestones} milestones`)

// ========== 3.5 Sort by Priority ==========
// Respect original phase order, then sort within phases

const sortedTasks = sortTasks([...analyzedTasks, ...additions])

// Sorting rules:
// 1. Preserve original phase order from tasks.md
// 2. Within each phase:
//    a. Dependencies first (no blockers)
//    b. HIGH risk early (fail fast)
//    c. Foundation before features
//    d. Lower complexity first (quick wins)

output(`\n✅ Task Analysis Complete`)
output(`   Total: ${allTasks.length} original + ${additions.length} auto-added = ${sortedTasks.length} tasks`)
```

**Output:**
```
📊 Task Analyzer v2.0 (Template-Free)...
   Found: 47 tasks from tasks.md

🔍 Analyzing each task...

📊 Analysis Results:
   Complexity: avg 5.8/10
   Risk: 8 HIGH, 15 MEDIUM, 24 LOW
   Agents: backend (35), test-debug (8), uxui-frontend (4)

   Auto-added: 12 best practice tasks
   Incremental: 6 tasks with 18 milestones

✅ Task Analysis Complete
   Total: 47 original + 12 auto-added = 59 tasks

🧪 UX Testing Injection...
   Injected Phase 1.5 (ux-tester) after Phase 1
   ✅ 1 UX approval gate(s) added
```

---

### Step 4: Create .claude Directory

**Create output directory before generating files:**
```typescript
// Create .claude directory for change-specific files
const claudeDir = `openspec/changes/${changeId}/.claude`

if (!fileExists(claudeDir)) {
  mkdir(claudeDir)
  output(`📁 Created: ${claudeDir}`)
}
```

WHY: `/cdev` expects files at `openspec/changes/{id}/.claude/` - creating the directory first ensures consistent file paths.

### Step 4.5: Inject UX Testing Phases (v2.7.0)

> **CRITICAL:** Auto-inject Phase X.5 (ux-tester) after EVERY uxui-frontend phase
> **Purpose:** User approval gate before proceeding to backend development

```typescript
// Group tasks by phase first
let phases = groupTasksByPhase(sortedTasks)

// Check if any phase has uxui-frontend agent
const hasUIWork = phases.some(p => {
  const phaseTasks = sortedTasks.filter(t => t.phase?.number === p.number)
  return getMostCommonAgent(phaseTasks) === 'uxui-frontend'
})

if (hasUIWork) {
  output(`\n🧪 UX Testing Injection...`)

  // Find all uxui-frontend phases
  const uiFrontendPhases = phases.filter(p => {
    const phaseTasks = sortedTasks.filter(t => t.phase?.number === p.number)
    return getMostCommonAgent(phaseTasks) === 'uxui-frontend'
  })

  // Inject .5 phase after each uxui-frontend phase
  uiFrontendPhases.forEach(uiPhase => {
    const uxTestingPhase = {
      number: `${uiPhase.number}.5`,
      name: 'UX Testing (Approval Gate)',
      agent: 'ux-tester',
      isApprovalGate: true,
      strategy: 'approval-required',
      tasks: [
        { id: `${uiPhase.number}.5.1`, description: 'Generate personas from product context', autoAdded: true },
        { id: `${uiPhase.number}.5.2`, description: 'Test UI from each persona perspective', autoAdded: true },
        { id: `${uiPhase.number}.5.3`, description: 'Generate UX test report with conversion prediction', autoAdded: true },
        { id: `${uiPhase.number}.5.4`, description: '⏸️ PAUSE: Wait for user approval', autoAdded: true }
      ]
    }

    // Insert after the UI phase
    const insertIndex = phases.findIndex(p => p.number === uiPhase.number) + 1
    phases.splice(insertIndex, 0, uxTestingPhase)

    output(`   Injected Phase ${uiPhase.number}.5 (ux-tester) after Phase ${uiPhase.number}`)
  })

  output(`   ✅ ${uiFrontendPhases.length} UX approval gate(s) added`)
}
```

**Workflow with UX Testing:**
```
Phase 1: uxui-frontend (build UI)
    ↓
Phase 1.5: ux-tester (APPROVAL GATE)
    → Generate personas
    → Test from each persona
    → Calculate conversion prediction
    → ⏸️ PAUSE for user approval
    ↓
[User APPROVE] → Continue to Phase 2
[User REJECT]  → Return to Phase 1 with feedback
```

---

### Step 5: Generate phases.md (Template-Free)

> **v2.0:** No templates loaded. Phases generated directly from analyzed tasks.
> **v2.7.0:** UX Testing phases already injected in Step 4.5

```typescript
// Generate phases.md from phases (already includes UX Testing phases)

const phasesContent = generatePhasesMarkdown(phases, sortedTasks, changeId, proposal)

function generatePhasesMarkdown(phases, tasks, changeId, proposal) {
  const title = extractTitle(proposal)
  const timestamp = new Date().toISOString()

  // Calculate totals
  const originalCount = tasks.filter(t => !t.autoAdded).length
  const autoAddedCount = tasks.filter(t => t.autoAdded).length
  const incrementalCount = tasks.filter(t => t.milestones).length
  const totalMilestones = tasks.reduce((sum, t) => sum + (t.milestones?.length || 0), 0)

  // Generate overview table
  const overviewRows = phases.map(phase => {
    const phaseTasks = tasks.filter(t => t.phase?.number === phase.number)
    const dominantAgent = getMostCommonAgent(phaseTasks)
    const hasIncremental = phaseTasks.some(t => t.milestones)
    const maxRisk = getMaxRisk(phaseTasks)

    return `| ${phase.number} | ${phase.name} | ${phaseTasks.length} | ${dominantAgent} | ${hasIncremental ? 'incremental' : 'standard'} | ${maxRisk} |`
  }).join('\n')

  // Generate phase sections
  const phaseSections = phases.map(phase => {
    return generatePhaseSection(phase, tasks.filter(t => t.phase?.number === phase.number))
  }).join('\n\n---\n\n')

  // Generate auto-added summary
  const autoAddedTasks = tasks.filter(t => t.autoAdded)
  const autoAddedSummary = autoAddedTasks.length > 0 ? `
## Auto-Added Tasks (Best Practices)

| Task | Reason | Phase |
|------|--------|-------|
${autoAddedTasks.map(t => `| ${t.description} | ${t.reason} | ${t.phase?.number || '-'} |`).join('\n')}
` : ''

  return `# Phases: ${title}

> **Generated by:** Task Analyzer v2.0 (Template-Free)
> **Source:** tasks.md (Single Source of Truth)
> **Strategy:** Incremental development (small → large)
> **Generated:** ${timestamp}

---

## Overview

| Phase | Name | Tasks | Agent | Strategy | Risk |
|-------|------|-------|-------|----------|------|
${overviewRows}

**Total Tasks:** ${originalCount} original + ${autoAddedCount} auto-added = ${tasks.length}
**Incremental Tasks:** ${incrementalCount} tasks with ${totalMilestones} milestones

---

${phaseSections}

${autoAddedSummary}

---

**End of phases.md**
`
}

function generatePhaseSection(phase, phaseTasks) {
  const dominantAgent = getMostCommonAgent(phaseTasks)
  const hasIncremental = phaseTasks.some(t => t.milestones)
  const maxRisk = getMaxRisk(phaseTasks)

  // v3.1.0: Use TDD classification from task-analyzer.md (Step 2.6)
  // Each task now has task.tdd = { tdd_required, workflow, reason, confidence }
  const tddTasks = phaseTasks.filter(t => t.tdd?.tdd_required === true)
  const needsTDD = tddTasks.length > 0
  const tddReasons = [...new Set(tddTasks.map(t => t.tdd?.reason).filter(Boolean))]

  let section = `## Phase ${phase.number}: ${phase.name}

**Agent:** ${dominantAgent}
**Strategy:** ${hasIncremental ? '🔄 INCREMENTAL' : 'Standard'}
**Risk:** ${maxRisk}
${needsTDD ? `**TDD Required:** ✅ YES
**TDD Reason:** ${tddReasons.slice(0, 2).join('; ')}
**TDD Workflow:** red-green-refactor

⚠️ **TDD WORKFLOW REQUIRED:**
1. 🔴 RED: Write tests FIRST (they should fail)
2. ✅ GREEN: Write minimal implementation to pass tests
3. 🔧 REFACTOR: Improve code quality while keeping tests green
` : ''}
`

  // Group tasks: incremental tasks get milestone sections, others get simple list
  const incrementalTasks = phaseTasks.filter(t => t.milestones)
  const standardTasks = phaseTasks.filter(t => !t.milestones)

  // Standard tasks section
  if (standardTasks.length > 0) {
    section += `### Tasks\n\n`
    standardTasks.forEach(task => {
      const prefix = task.autoAdded ? '✨ ' : ''
      section += `- [ ] ${prefix}${task.id} ${task.description}\n`
    })
    section += '\n'
  }

  // Incremental tasks with milestones
  incrementalTasks.forEach(task => {
    section += `### Task ${task.id}: ${task.description}
**Complexity:** ${task.complexity}/10 | **Why Agent:** ${task.agentReason}

`
    task.milestones.forEach((milestone, idx) => {
      section += `#### Milestone ${milestone.id}/${task.milestones.length}: ${milestone.name}
**Goal:** ${milestone.goal}

${milestone.tasks.map(t => `- [ ] ${t}`).join('\n')}

**Exit Criteria:**
${milestone.exitCriteria.map(c => `- [ ] ${c}`).join('\n')}

**CHECKPOINT:** Report results before ${idx < task.milestones.length - 1 ? `Milestone ${milestone.id + 1}` : 'next phase'}

---

`
    })
  })

  // Exit criteria for the phase
  section += `### Phase ${phase.number} Exit Criteria
- [ ] All tasks completed
- [ ] All tests pass
- [ ] No regression in existing functionality
`

  return section
}
```

Write to: `openspec/changes/{change-id}/.claude/phases.md`

### Step 6: Generate flags.json (Template-Free)

> **v2.0:** Flags generated from analyzed tasks, not templates.

```typescript
// Generate flags.json from sortedTasks (from Step 3)

const phases = groupTasksByPhase(sortedTasks)

const flags = {
  version: '2.0.0',
  change_id: changeId,
  change_type: detectChangeType(sortedTasks), // AI determines from task analysis
  created_at: new Date().toISOString(),
  updated_at: new Date().toISOString(),
  current_phase: phases[0]?.number || 1,
  meta: {
    total_phases: phases.length,
    pending_phases: phases.length,
    completed_phases: 0,
    total_tasks: sortedTasks.length,
    original_tasks: sortedTasks.filter(t => !t.autoAdded).length,
    auto_added_tasks: sortedTasks.filter(t => t.autoAdded).length,
    incremental_tasks: sortedTasks.filter(t => t.milestones).length,
    total_milestones: sortedTasks.reduce((sum, t) => sum + (t.milestones?.length || 0), 0)
  },
  phases: {}
}

// Initialize all phases from analyzed tasks
phases.forEach((phase, index) => {
  const phaseTasks = sortedTasks.filter(t => t.phase?.number === phase.number)
  const dominantAgent = getMostCommonAgent(phaseTasks)
  const hasIncremental = phaseTasks.some(t => t.milestones)

  flags.phases[phase.number] = {
    phase_number: index + 1,
    name: phase.name,
    status: 'pending',
    agent: dominantAgent,
    task_count: phaseTasks.length,
    strategy: hasIncremental ? 'incremental' : 'standard',
    milestones: hasIncremental ? phaseTasks.filter(t => t.milestones).reduce((sum, t) => sum + t.milestones.length, 0) : 0
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

// Replace placeholders (v2.0: use phases from Task Analyzer, not templates)
const phases = groupTasksByPhase(sortedTasks)
const totalPhases = phases.length

contextTemplate = contextTemplate
  .replace('{CHANGE_ID}', changeId)
  .replace('{CHANGE_TITLE}', extractTitle(proposalContent))
  .replace('{CHANGE_TYPE}', detectChangeType(sortedTasks))
  .replace('{CURRENT_PHASE_NUMBER}', '1')
  .replace('{TOTAL_PHASES}', totalPhases.toString())
  .replace('{CREATED_DATE}', new Date().toISOString())
  .replace('{CORE_TECH_LIST}', generateCoreTechList(projectTech))
  .replace('{ADDITIONAL_TECH_LIST}', generateAdditionalTechList(additionalTech))
  .replace('{CURRENT_PHASE}', phases[0]?.name || 'Phase 1')
  .replace('{STATUS}', 'pending')
  .replace('{DESIGN_SYSTEM}', designInfo) // 🆕 Add design section
```

Write to: `openspec/changes/{change-id}/.claude/context.md`

### Step 8: Output Summary (v2.0.0 - Template-Free)

```typescript
// Calculate from analyzed tasks (not templates)
const phases = groupTasksByPhase(sortedTasks)
const totalPhases = phases.length
const incrementalCount = sortedTasks.filter(t => t.milestones).length
const totalMilestones = sortedTasks.reduce((sum, t) => sum + (t.milestones?.length || 0), 0)
const autoAddedCount = sortedTasks.filter(t => t.autoAdded).length

// Check if UI work was detected
const hasUIWork = sortedTasks.some(t => t.agent === 'uxui-frontend')

// Check for existing page-plan.md
const pagePlanPath = `openspec/changes/${changeId}/page-plan.md`
const hasPagePlan = fileExists(pagePlanPath)

// Agent breakdown
const agentCounts = {}
sortedTasks.forEach(t => {
  agentCounts[t.agent] = (agentCounts[t.agent] || 0) + 1
})
const agentSummary = Object.entries(agentCounts)
  .map(([agent, count]) => `${agent} (${count})`)
  .join(', ')

// Build output
let output = `
✅ Change setup complete!

📦 Change: ${changeId}
📊 Architecture: Task Analyzer v2.0 (Template-Free)
🛠️ Agents: ${agentSummary}

📁 Files created:
✓ openspec/changes/${changeId}/.claude/phases.md
✓ openspec/changes/${changeId}/.claude/flags.json
✓ openspec/changes/${changeId}/.claude/context.md

📊 Task Analysis:
   Total: ${sortedTasks.length} tasks (${sortedTasks.filter(t => !t.autoAdded).length} original + ${autoAddedCount} auto-added)
   Incremental: ${incrementalCount} tasks with ${totalMilestones} milestones
   Phases: ${totalPhases}
   UX Approval Gates: ${phases.filter(p => p.agent === 'ux-tester').length}

📋 Phase Overview:
${phases.map((p, i) => {
  const phaseTasks = sortedTasks.filter(t => t.phase?.number === p.number)
  const agent = getMostCommonAgent(phaseTasks)
  return `   Phase ${p.number}: ${p.name} (${agent}, ${phaseTasks.length} tasks)`
}).join('\n')}
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

### getMostCommonAgent() (v2.0 - Template-Free)
```typescript
// v2.0: Agent determined by AI analysis of tasks, not phase templates
function getMostCommonAgent(tasks: AnalyzedTask[]): string {
  if (tasks.length === 0) return 'integration'

  const counts = {}
  tasks.forEach(t => {
    counts[t.agent] = (counts[t.agent] || 0) + 1
  })

  return Object.entries(counts)
    .sort((a, b) => b[1] - a[1])[0][0]
}
```

### groupTasksByPhase()
```typescript
function groupTasksByPhase(tasks: AnalyzedTask[]): Phase[] {
  const phaseMap = new Map()

  tasks.forEach(task => {
    const phaseNum = task.phase?.number || 1
    const phaseName = task.phase?.name || `Phase ${phaseNum}`

    if (!phaseMap.has(phaseNum)) {
      phaseMap.set(phaseNum, {
        number: phaseNum,
        name: phaseName,
        tasks: []
      })
    }
    phaseMap.get(phaseNum).tasks.push(task)
  })

  return Array.from(phaseMap.values()).sort((a, b) => a.number - b.number)
}
```

### getMaxRisk()
```typescript
function getMaxRisk(tasks: AnalyzedTask[]): string {
  if (tasks.some(t => t.risk === 'HIGH')) return 'HIGH'
  if (tasks.some(t => t.risk === 'MEDIUM')) return 'MEDIUM'
  return 'LOW'
}
```

### detectChangeType() (v2.0 - AI-Driven)
```typescript
function detectChangeType(tasks: AnalyzedTask[]): string {
  // Detect from analyzed tasks, not keywords
  const hasUI = tasks.some(t => t.agent === 'uxui-frontend')
  const hasBackend = tasks.some(t => t.agent === 'backend')
  const hasDatabase = tasks.some(t => t.agent === 'database')
  const hasTests = tasks.some(t => t.agent === 'test-debug')

  if (hasUI && hasBackend && hasDatabase) return 'full-stack'
  if (hasUI && !hasBackend) return 'frontend-only'
  if (hasBackend && !hasUI) return 'backend-only'
  if (hasTests && tasks.length <= 5) return 'bug-fix'

  return 'feature'
}
```

### detectAdditionalTech() - REMOVED (v3.1.0)

> **Note:** This function was removed in v3.1.0. Use Step 2.7's direct Context7 instructions instead.
> Main Claude now directly calls Context7 MCP tools to detect and resolve libraries.

---

## Error Handling

**If tasks.md is missing or empty:**
```
❌ Error: tasks.md not found or empty
Please ensure the change has been properly initialized with OpenSpec
```

**If no tasks detected:**
```
⚠️ Warning: No checkboxes found in tasks.md
Please ensure tasks.md contains checkbox items:
  - [ ] 1.1 Task description
  - [ ] 1.2 Another task
```

---

## Example Session (v2.0 - Template-Free)

```bash
$ /csetup refactor-backend-architecture

🔍 Reading OpenSpec files...
✓ Read: proposal.md (3.1 KB)
✓ Read: tasks.md (4.2 KB)
✓ Read: design.md (1.8 KB)

📊 Task Analyzer v2.0 (Template-Free)...
   Found: 47 tasks from tasks.md

🔍 Analyzing each task...

📊 Analysis Results:
   Complexity: avg 5.8/10
   Risk: 8 HIGH, 15 MEDIUM, 24 LOW
   Agents: backend (35), test-debug (8), uxui-frontend (4)

   Auto-added: 12 best practice tasks
   Incremental: 6 tasks with 18 milestones

✅ Task Analysis Complete
   Total: 47 original + 12 auto-added = 59 tasks

📁 Created: openspec/changes/refactor-backend-architecture/.claude

Generating workflow...
✓ Generated phases.md (250 lines, 5 phases)
✓ Generated flags.json (with task analysis metadata)
✓ Generated context.md (change context with tech references)

✅ Change setup complete!

📦 Change: refactor-backend-architecture
📊 Architecture: Task Analyzer v2.0 (Template-Free)
🛠️ Agents: backend (35), test-debug (8), uxui-frontend (4)

📁 Files created:
✓ openspec/changes/refactor-backend-architecture/.claude/phases.md
✓ openspec/changes/refactor-backend-architecture/.claude/flags.json
✓ openspec/changes/refactor-backend-architecture/.claude/context.md

📊 Task Analysis:
   Total: 59 tasks (47 original + 12 auto-added)
   Incremental: 6 tasks with 18 milestones
   Phases: 5

📋 Phase Overview:
   Phase 1: Foundation (backend, 17 tasks)
   Phase 2: Repository Layer (backend, 15 tasks)
   Phase 3: Service Layer (backend, 12 tasks)
   Phase 4: Migration (backend, 8 tasks)
   Phase 5: Verification (test-debug, 7 tasks)

🚀 Ready to start development!

Next steps:
1. Review workflow: openspec/changes/refactor-backend-architecture/.claude/phases.md
2. Start development: /cdev refactor-backend-architecture
3. View progress: /cview refactor-backend-architecture
```

---

## Important Notes

1. **Re-run safe:** Running `/csetup` again will **overwrite** existing files. Use with caution.
2. **Manual adjustments:** You can manually edit phases.md after generation if needed
3. **AI-driven analysis:** Agent assignment and complexity are determined by AI context understanding, not keyword matching
4. **Incremental milestones:** Complex tasks automatically get milestone-based execution for progressive validation
5. **Auto-added best practices:** Checkpoints, error handling, and verification tasks are added automatically (no warnings)
