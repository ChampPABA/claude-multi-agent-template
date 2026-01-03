# Changelog

> **Version History for Claude Agent Kit**
> For current features, see `CLAUDE.md`

---

## v3.5.2: UX Tester v3.0 - Inline Output (No File Creation)

**Problem Solved:** User ไม่ต้องการให้ ux-tester สร้างไฟล์ .md แยก - ต้องการ verbose output ใน response แทน

**Solution:** Rewrote ux-tester to v3.0 - output inline verbose ใน response โดยไม่สร้างไฟล์

### Key Changes

| Before | After |
|--------|-------|
| สร้าง `ux-test-report.md` | ❌ ไม่สร้างไฟล์ |
| Compact format (MAX 150 lines) | ✅ Verbose ได้เลย |
| Table-only output | ✅ Detailed descriptions OK |

### Files Changed

| File | Change |
|------|--------|
| `.claude/agents/07-ux-tester.md` | v2.1→v3.0, inline output, no file creation |
| `.claude/commands/cdev.md` | Section 6: No File Output enforcement |
| `.claude/templates/phases-sections/ux-testing.md` | Remove file references |

### What Changed

- **Agent v3.0**: ห้ามสร้างไฟล์ .md, output ใน response เท่านั้น
- **Verbose OK**: ละเอียดได้เลย ไม่มี line limit
- **cdev.md**: Inject "NO FILE CREATION" rule เมื่อ invoke ux-tester

---

## v3.5.1: UX Tester Report Format Enforcement

**Problem Solved:** UX Tester agent ignored the compact report format from v3.5.0 and still generated verbose reports (~200+ lines). Root cause: format template was "passive" - no enforcement mechanism.

**Solution:** Added CRITICAL format rules to agent file + format enforcement injection in cdev.md.

### Key Changes

| Change | Location | Purpose |
|--------|----------|---------|
| CRITICAL format rules | `07-ux-tester.md` | Hard limits: MAX 150 lines, tables only |
| Section 6 enforcement | `cdev.md` Step 4.1 | Inject format rules when invoking ux-tester |

### Files Changed

| File | Change |
|------|--------|
| `.claude/agents/07-ux-tester.md` | Added "⚠️ CRITICAL: Report Format Rules" section, version 2.0→2.1 |
| `.claude/commands/cdev.md` | Added Section 6: Report Format Enforcement (ux-tester only) |

### Format Rules Enforced

- MAX 150 lines total
- Tables ONLY (no paragraphs for personas/issues)
- 1 row per persona, 1 row per issue
- MAX 10 steps in Human Testing Guide
- No verbose persona backgrounds/stories

---

## v3.5.0: UX Tester v2.0 - Token Optimized + Human Testing Guide

**Problem Solved:** UX Tester agent generated verbose reports (~200 lines) with repetitive persona details, consuming excessive tokens (~3,500). Users couldn't easily test the UI themselves because the report was technical and long.

**Solution:** Rewrote `07-ux-tester.md` from 607 lines to 162 lines (-74% tokens). Added Human Testing Guide with step-by-step instructions for manual testing.

### Key Changes

| Metric | Before | After | Reduction |
|--------|--------|-------|-----------|
| Agent prompt lines | 607 | 162 | -73% |
| Estimated tokens | ~3,500 | ~900 | -74% |
| Report lines | ~200 | ~50 | -75% |

### New Features

**1. Compact Report Format** - Summary table instead of verbose persona sections

**2. Human Testing Guide** - Step-by-step instructions (1, 2, 3...) for manual testing

**3. Approval Checklist** - 6 items to check before approve/reject

### What Was Removed

- Verbose persona examples (TOEIC course)
- Repetitive step-by-step sub-instructions
- Duplicate report format templates

### Files Changed

| File | Change |
|------|--------|
| `.claude/agents/07-ux-tester.md` | Complete rewrite v2.0 |

---

## v3.4.0: Complete Pseudocode Elimination

**Problem Solved:** Agents read TypeScript/JavaScript pseudocode and interpreted it as "examples" or "reference documentation" rather than executable instructions. This caused agents to not follow the intended workflow.

**Solution:** Converted ~3,210 lines of pseudocode across all 8 command files to imperative step-by-step instructions following the pattern established in `design-validator.md`.

### Key Changes

| File | Lines Converted | Key Sections |
|------|-----------------|--------------|
| `cdev.md` | ~300 | Steps 2-5, approval gate, page plan validation |
| `csetup.md` | ~800 | Steps 7-8, helper functions |
| `designsetup.md` | ~1,200 | Steps 5-6, data.yaml generation |
| `extract.md` | ~400 | Steps 0-6, Chrome DevTools extraction |
| `pageplan.md` | ~200 | Steps 1-5, context loading |
| `cview.md` | ~100 | Formatting helpers |
| `cstatus.md` | ~60 | Steps 1-2, infrastructure summary |
| `pstatus.md` | ~150 | Steps 1-5, YAML updates |

### Conversion Pattern

```markdown
# ❌ BEFORE (Pseudocode - agents ignore):
```typescript
if (fileExists(path)) {
  const data = JSON.parse(Read(path))
  return data.value
}
```

# ✅ AFTER (Imperative - agents follow):
**If the file exists:**
1. Read the file at `{path}`
2. Parse the content as JSON
3. Extract and return the `value` field
```

### Why This Matters

**Before:**
- TypeScript code blocks treated as documentation
- Agents skipped procedural logic
- Inconsistent behavior between runs
- User had to manually guide agents

**After:**
- Clear numbered steps agents execute
- Conditional logic as "If X, then Y" blocks
- Consistent, reproducible behavior
- Agents self-navigate through workflows

### Files Changed

| File | Change |
|------|--------|
| `.claude/commands/cdev.md` | All pseudocode → imperative |
| `.claude/commands/csetup.md` | All pseudocode → imperative |
| `.claude/commands/designsetup.md` | All pseudocode → imperative |
| `.claude/commands/extract.md` | All pseudocode → imperative |
| `.claude/commands/pageplan.md` | All pseudocode → imperative |
| `.claude/commands/cview.md` | All pseudocode → imperative |
| `.claude/commands/cstatus.md` | All pseudocode → imperative |
| `.claude/commands/pstatus.md` | All pseudocode → imperative |
| `tests/` | Removed (tests passed, cleanup) |

---

## v3.3.0: Design Validation System (No Pseudocode)

**Problem Solved:** Design system compliance was not enforced. uxui-frontend agents didn't read `design-system/data.yaml`, resulting in hardcoded colors, arbitrary spacing, and inconsistent animations. The validation logic was written as TypeScript pseudocode that Claude never executed.

**Solution:** Created a single source of truth (`design-validator.md`) with imperative Thai/English instructions. Converted all procedural pseudocode to step-by-step commands that Claude follows.

### Key Changes

| Component | Before | After |
|-----------|--------|-------|
| design-validator.md | Did not exist | NEW - Single source of truth |
| cdev.md Step 2-5 | TypeScript pseudocode | Imperative instructions |
| ux-tester.md Steps 2-5 | TypeScript pseudocode | Imperative instructions |
| uxui-frontend STEP 0.5 | Brief mention | Full step-by-step protocol |

### Design Validation Flow

```
PREVENTION (Before Implementation)
├── Main Claude: Pre-Flight Check before invoking uxui-frontend
└── uxui-frontend: STEP 0.5 - Read data.yaml, report tokens

DETECTION (After Implementation)
└── ux-tester: Step 5.5 - Chrome DevTools style comparison
```

### What Gets Validated

| Token Category | Violation Example | Expected |
|----------------|-------------------|----------|
| Colors | #3b82f6, text-blue-500 | bg-primary, text-foreground |
| Spacing | p-5, gap-7 | p-4, p-6, gap-8 (scale) |
| Animation | duration-200 | duration-150, 300, 500ms |
| Shadows | mixed sm+xl | consistent level |

### Files Changed

| File | Change |
|------|--------|
| `.claude/lib/design-validator.md` | NEW - Single source of truth |
| `.claude/agents/02-uxui-frontend.md` | v2.1.0 - Enhanced STEP 0.5 |
| `.claude/agents/07-ux-tester.md` | v1.1.0 - Steps 2-5 rewritten |
| `.claude/commands/cdev.md` | Steps 2-5 rewritten, Step 4.0 added |
| `.claude/lib/README.md` | Added design-validator.md entry |
| `.claude/CLAUDE.md` | v3.3.0 + Design Validation section |

### Why This Matters

**Before:**
- Logic scattered across 4 files
- TypeScript pseudocode that Claude ignored
- No enforcement of design tokens
- ux-tester couldn't validate actual CSS

**After:**
- Single source of truth (design-validator.md)
- Imperative instructions Claude follows
- Pre-flight check before visual agents
- Chrome DevTools validation of computed styles

---

## v3.2.0: Consolidated Pre-Work Context

**Problem Solved:** `/csetup` generated two separate pseudocode outputs (`research-checklist.md` and `INTEGRATION_RISKS.md`) that were never actually created. Agents had to discover context from multiple scattered sources.

**Solution:** Consolidated all agent context into a single `pre-work-context.md` file with direct execution instructions. Merged Step 2.7 (Best Practices) into Step 2.6.

### Key Changes

| Component | Before | After |
|-----------|--------|-------|
| Step 2.6 | ~1000 lines of pseudocode | ~300 lines of direct instructions |
| Step 2.7 | Separate best practices step | Merged into Step 2.6 |
| Output files | research-checklist.md + INTEGRATION_RISKS.md + best-practices/*.md | Single `pre-work-context.md` |
| Agent discovery | Multiple files to read | One file with all context |

### Step 2.6 Structure (New - v3.2.0)

```
Step 2.6.1: Analyze Change Characteristics (type, complexity, risk)
Step 2.6.2: Detect Libraries (from package files + specs)
Step 2.6.3: Fetch Best Practices via Context7 (direct MCP calls)
Step 2.6.4: Determine Research Layers (adaptive depth)
Step 2.6.5: Detect Integration Warnings (cross-library)
Step 2.6.6: Generate Critical Checklist Items (security/compliance)
Step 2.6.7: Write pre-work-context.md (single consolidated file)
Step 2.6.8: Output Summary
Step 2.6.9: Skip Conditions
```

### pre-work-context.md Structure

```markdown
# Pre-Work Context: {changeId}

## 1. Change Analysis (type, complexity, risk)
## 2. Library Best Practices (from Context7)
## 3. Research Findings (domain knowledge)
## 4. Integration Warnings (cross-library concerns)
## 5. Critical Checklist (security/compliance must-haves)
## 6. Quick Reference (package manager, commands)
```

### Agent Pre-Work Checklist Update

**Version:** 3.0.0 (Pre-Work Context Integration)

- Step 0: Read pre-work-context.md (NEW - primary source)
- Step 0.1: Library Requirements Check (fallback)
- Step 0.2: Library Feasibility Validation (was 0.5)
- Step 0.3: Memory Context Query (was 0.6)

### Files Changed

| File | Change |
|------|--------|
| `csetup.md` | Rewrote Step 2.6 with direct execution |
| `csetup.md` | Removed Step 2.7 (merged into 2.6) |
| `csetup.md` | Renumbered Step 2.8 → Step 2.7 |
| `pre-work-checklist.md` | Added Step 0 (read pre-work-context.md) |
| `pre-work-checklist.md` | Renumbered steps (0.5→0.2, 0.6→0.3) |
| `CLAUDE.md` | Updated to v3.2.0 |

### Why This Matters

**Before:**
- Agents had to read 5+ files to get context
- research-checklist.md was pseudocode that never executed
- INTEGRATION_RISKS.md was pseudocode that never executed
- Context was scattered and inconsistent

**After:**
- Agents read ONE file (`pre-work-context.md`) in STEP 0
- All context is consolidated and actually generated
- Main Claude follows direct instructions (not pseudocode)
- Integration warnings + checklist items in one place

---

## v3.1.1: Direct Best Practices Execution

**Problem Solved:** Step 2.7 (Auto-Setup Best Practices) was written as pseudocode with helper functions (`extractLibrariesSemantically`, `parseContext7Response`, etc.) that Main Claude never actually executed. Best practices files were documented but never created.

**Solution:** Rewrote Step 2.7 as direct, executable instructions that Main Claude can follow. No more pseudocode - just clear steps with actual MCP tool names.

### Key Changes

| Component | Before | After |
|-----------|--------|-------|
| Step 2.7 | ~1000 lines of pseudocode | ~130 lines of direct instructions |
| Helper functions | 6 fake functions | Removed entirely |
| MCP tool calls | Written as code syntax | Written as clear instructions |
| Output format | Complex extraction logic | Simple template |

### Step 2.7 Structure (New)

```
Step 2.7.1: Detect Libraries (from package.json, requirements.txt, spec files)
Step 2.7.2: Resolve via Context7 (call MCP tools directly)
Step 2.7.3: Create Best Practices Files (using template)
Step 2.7.4: Create index.md (registry)
Step 2.7.5: Output Summary
Step 2.7.6: Skip Conditions
```

### Files Changed

| File | Change |
|------|--------|
| `csetup.md` | Rewrote Step 2.7, removed ~1000 lines of pseudocode |
| `csetup.md` | Removed helper functions (extractLibrariesSemantically, etc.) |
| `csetup.md` | Updated detectAdditionalTech as REMOVED |
| `CLAUDE.md` | Updated version to 3.1.1 |

### Why This Matters

Before: Main Claude would read Step 2.7 as documentation and skip it.
After: Main Claude follows clear instructions and actually calls Context7.

---

## v3.1.0: TDD Classification + Development Principles Injection

**Problem Solved:** TDD classification was a simple one-liner (`risk=HIGH || complexity>=7`) that missed critical patterns like auth, payment, and external integrations. Development principles (SOLID, DRY, KISS) were documented but never injected to agents.

**Solution:** Comprehensive TDD classification based on `tdd-classification.md` patterns, integrated into `task-analyzer.md` Step 2.6. Development principles injected to ALL agents via `/cdev`.

### Key Changes

| Component | Before | After |
|-----------|--------|-------|
| TDD classification | 1-line in csetup.md | Full pattern matching in task-analyzer.md |
| development-principles.md | Listed but not used | Injected to ALL agents via /cdev |
| tdd-classifier.md | Duplicate file | Deleted (merged into tdd-classification.md) |

### TDD Classification (Step 2.6)

Now classifies based on:

| Pattern | Examples | TDD Required |
|---------|----------|--------------|
| Security operations | auth, jwt, encrypt, permission | ✅ Always |
| Financial operations | payment, stripe, calculate, tax | ✅ Always |
| External integrations | webhook, sendgrid, twilio | ✅ Always |
| Data transformations | serialize, parse, etl | ✅ Always |
| Complex UI | multi-step, wizard, keyboard-nav | ✅ Always |
| Simple CRUD reads | get, list, fetch | ❌ Test-alongside OK |
| Presentational UI | button, card, modal | ❌ No TDD |
| Database/Integration | schema, migration, validation | ❌ No TDD |

### Development Principles Injection

`/cdev` now injects to ALL agent prompts:

```markdown
## 🏛️ Development Principles (Level 1 - ALL Agents)

**REQUIRED READING:** @.claude/contexts/patterns/development-principles.md

| Principle | Summary |
|-----------|---------|
| **KISS** | Choose simple solutions over complex ones |
| **YAGNI** | Build only what you need now |
| **SRP** | One responsibility per module |
| **DRY** | Single source of truth for all knowledge |
| **Fail Fast** | Detect and raise errors immediately |
| **Observability** | Log everything that matters |
```

### Files Changed

| File | Change |
|------|--------|
| `task-analyzer.md` | Added Step 2.6 TDD Classification |
| `csetup.md` | Updated phase generation to use TDD from tasks |
| `cdev.md` | Added development-principles injection |
| `tdd-classifier.md` | **DELETED** (merged) |
| `CLAUDE.md` | Updated references and version |

---

## v3.0.0: Template-Free Architecture (Task Analyzer v2.0)

**Problem Solved:** Phase templates (`phase-templates.json`) were limiting and caused task loss. When `tasks.md` had 5 detailed phases but template had only 2, tasks disappeared. Templates overrode the single source of truth.

**Solution:** Delete templates entirely. Use AI-driven Task Analyzer to transform `tasks.md` (WHAT) into `phases.md` (HOW).

### Key Changes

| Component | Before (v2.x) | After (v3.0) |
|-----------|---------------|--------------|
| phases.md source | phase-templates.json | tasks.md (single source of truth) |
| Agent assignment | Keyword matching | AI context understanding |
| Missing best practices | Warning prompts | Auto-add automatically |
| Complex tasks | Same as simple | Incremental milestones |
| Task filtering | Templates filter tasks | No filtering, ALL tasks kept |

### How It Works

```
tasks.md (WHAT to build)
    ↓
Step 1: Parse ALL tasks (no filtering)
Step 2: AI-driven analysis (complexity, risk, agent, dependencies)
Step 3: Auto-add best practices (no warnings)
Step 4: Generate incremental milestones
Step 5: Sort by priority (phase order → dependencies → risk)
    ↓
phases.md (HOW to build incrementally)
```

### AI-Driven Analysis (vs Keyword Matching)

**Old (keyword matching):**
```
"Create user service that connects to database"
Keywords: "service" (backend), "connects" (frontend), "database" (database)
→ Conflict! Which agent?
```

**New (AI decision):**
```
"Create user service that connects to database"
→ AI understands: This is a backend service layer
→ Agent: backend ✓
```

### Auto-Add Best Practices (No Warnings)

| Condition | Auto-Added Task |
|-----------|-----------------|
| HIGH risk task | Checkpoint: Verify before proceeding |
| External API | Error handling + retry + timeout |
| Implementation (complexity ≥ 5) | Verification task |
| Database changes | Backup + rollback test |
| Security-critical | Security review + log check |

### Incremental Milestones

Complex tasks (risk=HIGH OR complexity≥7) get automatic milestones:

| Pattern | Strategy | Milestones |
|---------|----------|------------|
| Repository/Service | method-by-method | 1 method → half → all |
| External API | mock-to-real | mock → 1 real → errors → scale |
| Batch Processing | scale-up | 1 → 5 → 20 → full |
| Complex Form | field-by-field | architecture → e2e → all fields |

### Files Changed

| File | Change |
|------|--------|
| `phase-templates.json` | **DELETED** |
| `task-analyzer.md` | Complete rewrite (v2.0) - 666 lines |
| `csetup.md` | Remove Steps 3-4 (keyword/template), new Step 3 (Task Analyzer) |

### Migration

No migration needed. Just run `/csetup` - it will generate phases.md from tasks.md directly.

---

## v2.8.0: Critical Flow Injection

**Problem Solved:** Research layers are flexible and context-dependent, but security/compliance items are non-negotiable. Previously, critical requirements like password hashing, PCI-DSS compliance, or HIPAA regulations could be missed if research didn't surface them.

**Solution:** Auto-inject critical required items into research layers based on change analysis.

### How It Works

```
/csetup analyzes change:
  ├── hasAuth: true → Inject auth security items (7 items)
  ├── hasPayment: true → Inject payment security items (5 items)
  ├── industryContext: healthcare → Inject HIPAA compliance items (5 items)
  └── industryContext: fintech → Inject PCI-DSS compliance items (6 items)

Research layers (flexible) + Critical items (non-negotiable)
```

### Critical Flow Categories

| Flow | Layer | Items | Examples |
|------|-------|-------|----------|
| Auth | Security | 7 | Password hashing (bcrypt/argon2), JWT secure storage, session timeout |
| Payment | Security | 5 | PCI key security, no card storage, webhook signature verification |
| Healthcare | Compliance | 5 | PHI encryption, role-based access, audit trail, BAA, breach plan |
| Fintech | Compliance | 6 | Data encryption, key rotation, audit logging, access controls |
| Sensitive Data | Security + Data Architecture | 6 | Encryption at rest/transit, access logging, backup, retention |

### Item Structure

Each critical item has:
```javascript
{
  id: 'auth-password-hash',           // Unique identifier
  check: '☐ Password hashing...',     // Checklist item
  why: 'Plain text passwords...',     // Explanation
  severity: 'critical'                // Always 'critical'
}
```

### Files Changed

| File | Change |
|------|--------|
| `tests/helpers.js` | `CRITICAL_FLOWS` constant + `injectCriticalRequiredItems()` function |
| `csetup.md` Step 2.6 | Calls `injectCriticalRequiredItems()` for each layer |

---

## v2.7.0: UX Testing Agent (Persona-Based)

**Problem Solved:** UI was approved by developers, not real users. No validation that the UI actually converts customers before spending time on backend development.

**Solution:** Auto-inject Phase 1.5 (ux-tester) after uxui-frontend with approval gate workflow.

### How It Works

```
Phase 1: uxui-frontend (build UI)
    ↓
Phase 1.5: ux-tester (approval gate)
    → Auto-generate personas from product context
    → Test each persona via Chrome DevTools
    → Calculate weighted conversion prediction
    → Generate UX test report
    → PAUSE for user approval
    ↓
[User approves] → Phase 2: backend + database
[User rejects]  → Loop back to Phase 1 with feedback
```

### Key Features

| Feature | Description |
|---------|-------------|
| **Auto-Generated Personas** | 3-5 personas with % breakdown based on product context |
| **Weighted Conversion** | Calculate purchase likelihood weighted by customer % |
| **Chrome DevTools Testing** | Screenshots, snapshots, click tests, mobile responsive |
| **Approval Gate** | PAUSE and wait for user approve/reject |
| **Rejection Loop** | Feedback passed to uxui-frontend, re-run Phase 1 → 1.5 |

### Files Changed

| File | Change |
|------|--------|
| `.claude/agents/07-ux-tester.md` | New agent for persona-based UX testing |
| `.claude/templates/phases-sections/ux-testing.md` | Phase template with approval gate |
| `.claude/lib/task-analyzer.md` | **v2.0:** Complete rewrite - template-free, AI-driven |
| `.claude/lib/agent-executor.md` | Approval gate execution logic |
| `.claude/commands/cdev.md` | Step 4.6 approval gate handling |

### UX Test Report Example

```markdown
# UX Test Report

## Personas Tested
| Persona | % ลูกค้า | Would Buy | Weighted |
|---------|----------|-----------|----------|
| นักศึกษา 18-24 | 40% | Maybe (50%) | +20% |
| พนักงาน 25-35 | 35% | Yes (100%) | +35% |
| ผู้สูงวัย 50-65 | 15% | No (0%) | +0% |
| ผู้ปกครอง 35-50 | 10% | Maybe (50%) | +5% |

## Conversion Prediction: 60%
## Potential After Fixes: 92.5%
```

---

## v2.5.0: Smart Topic Query + Integration Risk Detection

**Problem Solved:** Context7 queries used static topic "best practices" which missed adapter/integration documentation. Example: Drizzle + Auth.js requires specific column naming (snake_case) but this wasn't detected, causing runtime errors.

**Solution:** Smart Topic Query includes other library names in topic + automatic integration risk detection.

### How Smart Topic Query Works

```
Old (v2.4.0):
  topic: "best practices, patterns, anti-patterns, common mistakes"
  → Misses adapter-specific docs

New (v2.5.0):
  topic: "best practices, patterns, adapter, integration, schema, {other-lib-names}"
  → Gets cross-library integration docs automatically
```

### Key Features

| Feature | Description |
|---------|-------------|
| **Smart Topic** | Includes other detected library names in Context7 topic |
| **Bidirectional Query** | Query BOTH libraries (Auth.js → Drizzle, Drizzle → Auth.js) |
| **Risk Pattern Detection** | Scans docs for adapter, schema, column, sync, webhook patterns |
| **INTEGRATION_RISKS.md** | Auto-generated summary of detected integration concerns |
| **Zero Maintenance** | No hardcoded library pairs - works with any combination |

### Integration Risk Patterns Detected

| Pattern | Keywords | Example |
|---------|----------|---------|
| Adapter | adapter, drizzleadapter, prismaadapter | ORM + Auth integrations |
| Schema | column, snake_case, camelcase, mapping | Column naming mismatches |
| Sync | sync, migrate, syncurl, embedded replica | Mobile/Edge data sync |
| Webhook | webhook, webhookendpoint | Payment/notification handlers |
| Lifecycle | beforeall, aftereach, setup, teardown | Test configuration |

### Output Files

| File | Content |
|------|---------|
| `best-practices/{lib}.md` | Library-specific best practices (enhanced with integration docs) |
| `best-practices/INTEGRATION_RISKS.md` | Cross-library risk summary + checklist |

### Example Flow

```
Detected: [drizzle, auth.js, stripe]

Query drizzle with topic: "best practices, adapter, integration, auth.js, stripe"
  → Gets: Drizzle adapter patterns, column naming

Query auth.js with topic: "best practices, adapter, integration, drizzle, stripe"
  → Gets: DrizzleAdapter config, usersTable/accountsTable schema

Query stripe with topic: "best practices, adapter, integration, drizzle, auth.js"
  → Gets: Webhook patterns, payment integration

Risk Detection:
  → auth.js mentions "drizzleadapter", "userstable" → SCHEMA pattern
  → stripe mentions "webhook", "webhooksecret" → WEBHOOK pattern

Output:
  → drizzle.md (with auth.js integration info)
  → auth-js.md (with Drizzle adapter config)
  → stripe.md (with webhook patterns)
  → INTEGRATION_RISKS.md (summary of all detected risks)
```

### Files Changed

| File | Change |
|------|--------|
| `csetup.md` Step 2.7 | Smart Topic Query implementation |
| `detectIntegrationRisks()` | New: Pattern detection from docs |
| `generateIntegrationRiskSummary()` | New: INTEGRATION_RISKS.md output |

---

## v2.4.0: Adaptive Depth Research

**Problem Solved:** Previous feature detection was hardcoded (only 4 types: auth, payment, fileUpload, apiDesign) and used fixed standards. Missing domain-level best practices like "how to design a good database" or "healthcare compliance requirements."

**Solution:** Dynamic research layers that adapt to each change's complexity (0 to 10+ layers).

### Key Principles

| Principle | Description |
|-----------|-------------|
| L1 = Best Practice (ALWAYS) | "คนอื่นทำกันยังไง?" (How do others do it?) for ALL non-trivial changes |
| Dynamic Depth | No fixed min/max - truly adaptive (0-10+ layers) |
| Separation of Concerns | Visual (/designsetup) is STATIC, Strategy (research) is DYNAMIC |
| Per-Change Output | Generates `research-checklist.md` for each change |
| Design Conflict Warnings | Warns if industry practice conflicts with user's design choices |

### Layer Examples by Change Type

| Change Type | Layers | Example Layers |
|-------------|--------|----------------|
| Typo fix, debug log | 0 | None needed |
| Simple API endpoint | 2 | Best Practice, API Design |
| Auth system | 4 | Best Practice, Security, API Design, Testing |
| E-commerce checkout | 7 | Best Practice, Security, UX, Payment, Integration, Performance, Testing |
| Healthcare portal | 10 | Best Practice, Security, Compliance (HIPAA), UX, Data Architecture, API, Performance, Testing, Integration, Audit |

### Knowledge Sources (Separated)

| Step | Knowledge Type | Source | Example |
|------|----------------|--------|---------|
| **2.6** | Domain (HOW to design) | Claude's Knowledge | Normalization, UX patterns, Security |
| **2.7** | Stack (HOW to use tool) | Context7 | Prisma, React, Next.js |

### How It Works

```
1. Analyze change from proposal.md, tasks.md, design.md
   → Detect: primaryType, complexity, riskLevel, domains, features

2. Determine research layers dynamically:
   - Trivial (complexity ≤ 1, no UI/API/DB) → 0 layers
   - Non-trivial → L1 Best Practice + context-specific layers

3. Execute research per layer using Claude's knowledge:
   - Claude knows: UX (Nielsen Norman, Baymard), DB (Codd), Security (OWASP)
   - No static files needed - Claude reasons from training
   - No WebSearch needed - domain knowledge is stable

4. Generate research-checklist.md with:
   - Key questions per layer
   - Best practices (from Claude's knowledge)
   - Anti-patterns to avoid
   - Trade-offs explained
   - Recommendations specific to THIS change

5. Agents read research-checklist.md before implementing
```

**WHY Claude's Knowledge?**
- Domain principles rarely change (Normalization = 50 years, REST = 20 years)
- No maintenance needed (no static files to update)
- Context-aware (Claude applies principles to YOUR specific change)
- Stack knowledge goes to Context7 (Step 2.7) which has live docs

### Available Research Layers

| Layer | Triggered By |
|-------|--------------|
| Best Practice / Industry Standard | Always (non-trivial changes) |
| Security Requirements | hasAuth, hasPayment, hasSensitiveData |
| {Industry} Compliance | healthcare, fintech, or other regulated industries |
| User Experience Patterns | isExternalFacing + hasUI |
| Conversion Psychology | marketing/sales pages |
| Content Strategy | marketing/content pages |
| Data Architecture | hasDatabase, data-intensive |
| API Design | hasAPI |
| Multi-tenancy Patterns | SaaS with tenant isolation |
| Real-time Architecture | WebSocket, collaboration features |
| Performance Optimization | external-facing OR complexity ≥ 6 |
| Integration Patterns | external APIs, webhooks |
| Testing Strategy | HIGH risk OR complexity ≥ 7 |

### Files Changed

| File | Change |
|------|--------|
| `csetup.md` Step 2.6 | Complete rewrite - Adaptive Depth Research |
| `analyzeChangeCharacteristics()` | New: semantic analysis of change context |
| `determineResearchLayers()` | New: dynamic layer selection |
| `executeLayerResearch()` | New: Context7 + semantic research |
| `generateResearchChecklist()` | New: markdown output per change |
| `checkDesignConflicts()` | New: warns on design vs industry fit |

---

## v2.3.0: Zero-Maintenance Tech Stack Detection

**Problem Solved:** Previously, `/csetup` required hardcoded regex patterns and Context7 ID mappings for each library. Adding support for new libraries (like SQLAlchemy, Pydantic, Rust crates) required code changes.

**Solution:** Dynamic detection that works with any library in any language without maintenance.

### How It Works

```
1. Extract potential library names from ALL text sources:
   - Spec files (proposal.md, design.md, tasks.md)
   - Package files (package.json, requirements.txt, Cargo.toml, go.mod, etc.)
   - Import statements in code snippets
   - Prose mentions ("using FastAPI", "with Prisma")

2. Send each candidate to Context7 resolve-library-id:
   - If Context7 recognizes it → confirmed library ✅
   - If not recognized → not a library, skip ❌

3. For confirmed libraries, fetch best practices:
   - Context7 get-library-docs with "best practices" topic
   - Generate .md file with patterns, anti-patterns, checklist

4. Result: Best practices for ANY library, automatically!
```

### Benefits

| Aspect | Before (v1.8.0) | After (v2.3.0) |
|--------|-----------------|----------------|
| New library support | Manual code change | Automatic |
| Python stack | Partial (FastAPI, Django only) | Full (SQLAlchemy, Pydantic, Click, etc.) |
| Rust support | None | Automatic |
| Go support | None | Automatic |
| Maintenance | Required for each library | Zero |

### Files Changed

| File | Change |
|------|--------|
| `csetup.md` Step 2.7 | Complete rewrite with dynamic detection |
| `extractPotentialLibraryNames()` | New helper for NLP extraction |
| `parseContext7Response()` | New helper for Context7 response parsing |
| `generateBestPracticesFile()` | Updated signature, includes Context7 ID |
| `detectAdditionalTech()` | Deprecated, delegates to new system |

---

## v2.2.0: claude-mem Integration

**What is claude-mem?** A Claude Code plugin that automatically captures tool usage observations and provides persistent memory across sessions.

### Division of Responsibilities

| Data Type | Source | How to Access |
|-----------|--------|---------------|
| Past decisions | claude-mem (auto) | Ask: "what decisions about X?" |
| Past learnings | claude-mem (auto) | Ask: "what did we learn about X?" |
| Past bugs/fixes | claude-mem (auto) | Ask: "what bugs with X?" |
| Future ideas | claude-mem (auto) | Ask: "what ideas for X?" |
| **Blockers** | PROJECT_STATUS.yml | Read file (requires human decision) |
| **Priorities** | PROJECT_STATUS.yml | Read file (requires human decision) |
| **Tech debt** | PROJECT_STATUS.yml | Read file (actionable items) |
| What to build | tasks.md → phases.md | /csetup generates |
| How to build | Agents | /cdev executes |

### PROJECT_STATUS.yml Changes

- **REMOVED:** `decisions`, `notes`, `future_ideas` → claude-mem handles automatically
- **KEPT:** `blockers`, `next_priorities`, `technical_debt` → requires human decision
- **Query past context:** Just ask naturally → mem-search skill auto-invoked

---

## v2.1.0: Design System v2 + Context Optimization

### Design System v2 (YAML-based)

- `/extract https://site.com` → Extracts design from reference site
- `/designsetup @prd.md` → Interactive 3-round loop with theme selection
- Generates: `data.yaml` (~800 lines) + `README.md` (~100 lines)

### Context Optimization

- **Problem:** Multiple files read by different commands/agents
- **Solution:** `data.yaml` = SINGLE SOURCE for all agents

### Cross-Session Context

- `PROJECT_STATUS.yml` provides quick context snapshot for new sessions
- Contains: infrastructure state, blockers, completed work, next priorities

---

## v2.0.0: Claude 4.5 Optimization

**Based on:** [Claude 4 Best Practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-4-best-practices)

### Changes Applied

| Before | After | WHY |
|--------|-------|-----|
| "MUST", "WILL BE REJECTED" | Professional tone | Claude 4.5 works better with respectful instructions |
| "Don't do X", "Never Y" | "Use X instead" | Positive instructions are clearer |
| Rules without context | Rules with WHY | Claude applies rules more intelligently |
| Duplicated content (6x) | Shared `_shared/` folder | 83% token reduction |
| ~1000 lines per agent | ~250-350 lines | 65% smaller |

### New Shared Components

```
.claude/agents/_shared/
├── pre-work-checklist.md     # Common validation steps
├── package-manager.md        # Package manager protocol
├── documentation-policy.md   # What files to create
├── agent-boundaries.md       # When to use which agent
└── README.md                 # Overview
```

### Token Savings

| Agent | Before | After | Reduction |
|-------|--------|-------|-----------|
| uxui-frontend | ~1037 | ~375 | 64% |
| integration | ~600 | ~210 | 65% |
| backend | ~700 | ~244 | 65% |
| database | ~680 | ~273 | 60% |
| frontend | ~650 | ~296 | 54% |
| test-debug | ~580 | ~252 | 57% |
| **Total** | **~4247** | **~1650** | **61%** |

Plus ~500 tokens in shared files = **~2150 total** (was ~4247)

### Files Refactored

**Implementation Logic (lib/):** agent-router.md, agent-executor.md, context-loading-protocol.md, flags-updater.md, document-loader.md, detailed-guides/agent-system.md

**Commands:** cdev.md, csetup.md, pageplan.md, designsetup.md

**Patterns (contexts/patterns/):** validation-framework.md, error-recovery.md, ui-component-consistency.md, task-breakdown.md, agent-discovery.md, code-standards.md, animation-patterns.md, frontend-component-strategy.md, performance-optimization.md, change-workflow.md, task-classification.md

**Design (contexts/design/):** index.md, box-thinking.md

**Templates:** phases-sections/frontend-mockup.md, design-context-template.md, STYLE_GUIDE.template.md

---

## Earlier Versions

- **v1.8.0** - File Creation Policy
- **v1.6.0** - Incremental Testing
- **v1.3.0** - TaskMaster-style Analysis

See git history for details.
