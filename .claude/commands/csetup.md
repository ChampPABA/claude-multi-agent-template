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

Analyzes OpenSpec files and generates:
1. `.claude/phases.md` - Agent workflow
2. `.claude/flags.json` - Progress tracking
3. `.claude/context.md` - Change-specific tech

---

## Steps Overview

| Step | Name | Purpose |
|------|------|---------|
| 1 | Prerequisites | Verify change exists |
| 1.5 | PROJECT_STATUS | Check blockers, pending follow-ups |
| 2 | Read OpenSpec | Load proposal, tasks, design |
| 2.5 | Design System | Validate tokens.json, page-plan |
| 2.6 | Feature BP | Check auth/payment/upload standards |
| 2.7 | Stack BP | Auto-detect libraries via Context7 |
| 2.8 | Library Capability | Verify library supports spec |
| 3-3.5 | Task Analysis | Complexity, risk, dependencies |
| 4 | Select Template | full-stack/frontend/backend/etc |
| 5-7 | Generate Files | phases.md, flags.json, context.md |
| 8 | Summary | Output results |

---

## Step 1: Check Prerequisites

```bash
ls openspec/changes/{change-id}/
# If not found: ❌ Error: Change not found
```

---

## Step 1.5: Read PROJECT_STATUS.yml

Check for blockers and pending follow-ups that affect this change.

```typescript
if (fileExists('PROJECT_STATUS.yml')) {
  const status = parseYaml(Read('PROJECT_STATUS.yml'))

  // Check blockers
  const blockers = status.blockers?.filter(b =>
    b.blocks?.some(x => x.includes(changeId))
  )
  if (blockers?.length) output(`⚠️ Blockers: ${blockers.map(b => b.id)}`)

  // Check pending follow-ups (v2.1.6)
  const pending = status.pending_followups?.filter(p =>
    p.affects?.some(pattern => changeId.includes(pattern))
  )
  if (pending?.length) {
    output(`⚠️ Related pending: ${pending.map(p => p.item)}`)
    // Ask: Continue / Address first / Include in scope
  }

  // Update active_change
  status.current_focus.active_change = changeId
}
```

---

## Step 2: Read OpenSpec Files

```typescript
const proposal = Read(`openspec/changes/${changeId}/proposal.md`)
const tasks = Read(`openspec/changes/${changeId}/tasks.md`)
const design = fileExists(`...design.md`) ? Read(`...design.md`) : ''
```

---

## Step 2.5: Validate Design System

If UI work detected, validate design files exist.

```typescript
if (hasFrontend) {
  const hasTokens = fileExists('design-system/tokens.json')
  const hasStyleGuide = fileExists('design-system/STYLE_GUIDE.md')
  const hasPagePlan = fileExists(`openspec/changes/${changeId}/page-plan.md`)

  if (!hasTokens || !hasStyleGuide) {
    warn(`⚠️ Design system incomplete. Run /designsetup first.`)
  }
}
```

---

## Step 2.6: Feature Best Practice Analysis

Validate spec against industry standards for security-critical features.

```typescript
const featureDetection = {
  authentication: {
    keywords: ['login', 'auth', 'jwt', 'session'],
    tier: 1, // Blocking
    standards: [
      'Short-lived access token (15-30min)',
      'Refresh token rotation',
      'Secure token storage (httpOnly)',
      'Rate limiting'
    ]
  },
  payment: {
    keywords: ['payment', 'stripe', 'checkout'],
    tier: 1,
    standards: ['No card data on server', 'Webhook signature verification', 'Idempotency keys']
  },
  fileUpload: {
    keywords: ['upload', 'file', 's3'],
    tier: 1,
    standards: ['File type validation', 'Size limits', 'Filename sanitization']
  }
}

// Check each detected feature against standards
// If gaps found: A) Update spec, B) Document skip, C) Continue anyway
```

---

## Step 2.7: Auto-Setup Best Practices (v2.3.0)

**Zero-maintenance:** Auto-detects any library from spec text via Context7.

```typescript
// 1. Gather ALL text sources
const sources = {
  proposal, tasks, design,
  packageJson: fileExists('package.json') ? Read('package.json') : '',
  requirementsTxt: fileExists('requirements.txt') ? Read('requirements.txt') : '',
  cargoToml: fileExists('Cargo.toml') ? Read('Cargo.toml') : '',
  goMod: fileExists('go.mod') ? Read('go.mod') : ''
}

// 2. Extract potential library names (pattern + semantic)
const candidates = extractPotentialLibraryNames(Object.values(sources).join('\n'))

// 3. Validate each with Context7
for (const candidate of candidates) {
  const result = await mcp__context7__resolve_library_id({ libraryName: candidate })
  const match = parseContext7Response(result, candidate)
  if (match?.score >= 60) {
    resolvedLibraries.push({ name: candidate, context7Id: match.id, ...match })
  }
}

// 4. Generate best-practices/*.md for new libraries
for (const lib of newLibraries) {
  const docs = await mcp__context7__get_library_docs({
    context7CompatibleLibraryID: lib.context7Id,
    topic: 'best practices, patterns, anti-patterns'
  })
  Write(`${bpDir}${lib.name}.md`, generateBestPracticesFile(lib.title, docs, lib.context7Id))
}
```

### Helper: extractPotentialLibraryNames()

Extracts library names from any text using multiple patterns:

```typescript
function extractPotentialLibraryNames(text: string): string[] {
  const candidates = new Set<string>()

  // Package files: "react": "^18", sqlalchemy==2.0, tokio = "1.0"
  // Import statements: from X import, import X from 'Y', use X::
  // Prose: "using FastAPI", "with Prisma", "powered by Mastra"
  // CamelCase: FastAPI, SQLAlchemy, NextAuth
  // Tech sections: "Tech Stack:", "Built with:"
  // Markdown: **Mastra**, `prisma`

  // Filter noise (stopWords: The, API, REST, Class, etc.)
  return [...candidates].filter(w => w.length > 2 && w.length < 30).slice(0, 50)
}
```

### Helper: parseContext7Response()

Selects best match from Context7 results by score and snippet count.

---

## Step 2.8: Library Capability Validation

Verify chosen libraries support ALL spec requirements.

```typescript
const libraryPatterns = {
  'better-auth': {
    patterns: ['better-auth'],
    knownLimitations: [
      { feature: 'refresh token rotation', supported: false },
      { feature: 'redis session storage', supported: false }
    ]
  }
  // ... other libraries
}

// Check each requirement against library capabilities
// If gaps: A) Change library, B) Downgrade spec, C) Custom impl, D) Continue
```

---

## Step 3: Analyze Tasks

```typescript
const keywords = Read('.claude/templates/phase-templates.json').detection_keywords

const hasFrontend = keywords.frontend.some(kw => tasks.includes(kw))
const hasBackend = keywords.backend.some(kw => tasks.includes(kw))
const hasDatabase = keywords.database.some(kw => tasks.includes(kw))
// ... etc
```

---

## Step 3.5: TaskMaster-style Analysis

**See:** `.claude/lib/task-analyzer.md` for complete logic.

For each task, analyze:
- **Complexity** (1-10): time + keywords + subtask count
- **Dependencies**: blockedBy, blocks, parallelizable
- **Risk** (LOW/MED/HIGH): security, external API, data migration
- **Research**: required queries, estimated time
- **Priority** (0-100): CRITICAL → HIGH → MEDIUM → LOW

Output summary with time buffers (+41% for complexity/risk).

---

## Step 4: Select Template

```typescript
const template = isBugFix ? 'bug-fix'
  : isRefactor ? 'refactor'
  : hasScript && !hasFrontend ? 'script-only'
  : hasFrontend && hasBackend ? 'full-stack'
  : hasFrontend ? 'frontend-only'
  : hasBackend ? 'backend-only'
  : 'full-stack' // default
```

---

## Step 5: Generate phases.md

Load template sections, inject task analysis metadata, write to change folder.

**See:** `.claude/lib/tdd-classifier.md` for TDD classification.

---

## Step 6: Generate flags.json

Initialize all phases as `pending` with agent assignments.

---

## Step 7: Generate context.md

Include: change info, tech stack, design system (if UI), pattern files to load.

---

## Step 8: Output Summary

```
✅ Change setup complete!

📦 Change: {change-id}
📋 Template: {template} ({n} phases)

📁 Files created:
✓ .claude/phases.md
✓ .claude/flags.json
✓ .claude/context.md

🚀 Next: /cdev {change-id}
```

---

## Helper Functions

### extractTaskIds()
```typescript
function extractTaskIds(content: string): string[] {
  return [...content.matchAll(/-\s*\[\s*\]\s*(\d+\.\d+)/g)].map(m => m[1])
}
```

### getAgentForPhase()
```typescript
const agentMap = {
  'frontend-mockup': 'uxui-frontend',
  'backend': 'backend',
  'database': 'database',
  'backend-tests': 'test-debug',
  'frontend-integration': 'frontend',
  // ... etc
}
```

### generateBestPracticesFile()
```typescript
function generateBestPracticesFile(tech: string, docs: string, context7Id: string): string {
  return `# ${tech} Best Practices
> **Source:** Context7 | **ID:** \`${context7Id}\`

## Best Practices
${extractBestPractices(docs)}

## Anti-Patterns
${extractAntiPatterns(docs)}

## Quick Checklist
${extractChecklist(docs)}
`
}
```

---

## Error Handling

| Error | Action |
|-------|--------|
| tasks.md missing | ❌ Create change with OpenSpec first |
| Template ambiguous | ⚠️ Default to full-stack |
| Design system incomplete | ⚠️ Suggest /designsetup |
| Feature BP gaps | Ask: Update spec / Document skip / Continue |
| Library capability gaps | Ask: Change lib / Downgrade spec / Custom impl |

---

## Notes

1. **Re-run safe:** Will overwrite existing files
2. **Manual edits OK:** Edit phases.md after generation if needed
3. **Zero maintenance:** Library detection works with any language automatically
