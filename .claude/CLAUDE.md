# CLAUDE.md

> **Navigation Hub for AI Agents**
> **Template Version:** 3.5.0 - UX Tester v2.0 (Token Optimized)
> **Latest:** Single Source of Truth for design compliance (prevention + detection)

---

## 📁 File Naming Conventions (OpenSpec + Template)

> **IMPORTANT:** Avoid confusion between OpenSpec files and Template files

### OpenSpec Files (from [Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec))

| File | Purpose | When to Read |
|------|---------|--------------|
| `proposal.md` | WHY - Goals, scope, rationale | Phase planning |
| `tasks.md` | WHAT - Implementation checklist | Task tracking |
| `design.md` | **Technical/Architecture decisions** (optional) | Backend/Database phases |
| `specs/` | Delta specs (ADDED/MODIFIED/REMOVED) | Requirement validation |

### Template Files (from claude-multi-agent-template)

| File | Purpose | When to Read |
|------|---------|--------------|
| `README.md` | **Visual design summary** (human-readable) | UI/Frontend phases |
| `data.yaml` | Design tokens + psychology (~300 lines) | Quick UI reference |
| `page-plan.md` | UI component layout + content strategy | uxui-frontend agent |
| `pre-work-context.md` | **v3.2.0!** All agent context (best practices, warnings, checklist) | All agents - STEP 0 ✨ |
| `phases.md` | Execution plan with agent assignments | All phases |
| `flags.json` | Progress tracking | All phases |

### Key Distinction

```
OpenSpec design.md    = Technical Architecture (data flow, API structure, system design)
Template data.yaml    = Visual Design (colors, fonts, spacing, component styles)
```

**Agents should read BOTH when relevant:**
- `uxui-frontend` → data.yaml (visual tokens) + design.md (if has UI architecture)
- `backend` → design.md (API/data architecture)
- `database` → design.md (data models, relationships)
- `frontend` → data.yaml (visual tokens) + design.md (API contracts)

---

## 🎯 What is This Template?

Universal, framework-agnostic template for AI-assisted development.

**What's Included:**
- ✅ 7 Specialized Agents (integration + ux-tester + 5 domain specialists)
- ✅ Universal Patterns (logging, testing, error-handling, agent selection)
- ✅ Design Foundation (color theory, spacing, typography)
- ✅ **Auto-Generated Best Practices** (from Context7 MCP per project)
- ✅ **3-Level Indexing** (agents auto-discover project context)
- ✅ Domain-Specific Support (add your business logic)

**What's NOT Included:**
- ❌ Framework patterns → Generated dynamically via `/csetup`
- ❌ Package managers → Auto-detected by `/csetup`
- ❌ Spec frameworks → Optional (OpenSpec, BMAD, SpecKit)

---

## 📖 Quick Navigation

**Design/UI (v2.1.0):**
- `/extract https://site.com` - Extract design from reference sites (one site at a time, incremental)
- `/designsetup @prd.md` - Interactive design setup (3-round loop, theme selection)
- `design-system/extracted/*/data.yaml` - Extracted site data (full YAML with 17+ sections)
- `design-system/data.yaml` - **v2.1!** Complete design data for agents (~800 lines) ✨
- `design-system/README.md` - Human-readable summary (~100 lines)
- `@/.claude/lib/document-loader.md` - Token-efficient loading patterns
- `@/.claude/contexts/design/index.md` (General design principles - fallback)

**Development:**
- `@/.claude/contexts/patterns/development-principles.md` - **v3.1.0!** SOLID, DRY, KISS, Fail Fast (Level 1 - ALL agents) ✨
- `@/.claude/contexts/patterns/tdd-classification.md` - TDD workflow classification patterns
- `@/.claude/contexts/patterns/task-classification.md` (Agent selection guide)
- `@/.claude/contexts/patterns/agent-coordination.md` (When to run agents parallel/sequential)
- `@/.claude/contexts/patterns/error-recovery.md` (How agents handle errors & escalate)
- `@/.claude/contexts/patterns/logging.md`
- `@/.claude/contexts/patterns/testing.md`
- `@/.claude/contexts/patterns/task-breakdown.md`
- `@/.claude/contexts/patterns/frontend-component-strategy.md`

**Project Setup:**
- `/extract https://site.com` - Extract design from reference sites
- `/designsetup @prd.md` - Interactive design system setup
- `/csetup` - **v3.2.0:** Generates `pre-work-context.md` with best practices, research, warnings, checklists

**Page Planning (UI Tasks) - v2.0.0:**
- `/pageplan @prd.md @brief.md` - Generate page structure with auto page type detection
- Output: `openspec/changes/{id}/page-plan.md` (component reuse, buyer avatar, conversion copy, asset checklist)
- Auto-detects page type (landing/dashboard/auth) from proposal.md/tasks.md
- Reads data.yaml for style/theme/animations
- Loads patterns/*.md selectively based on page type
- Buyer avatar analysis (Eugene Schwartz framework) for marketing pages only
- Used by: uxui-frontend agent (auto-reads in STEP 0.5)

**OpenSpec Multi-Agent Workflow:**
- `/csetup {change-id}` - Setup change context (analyze tasks, generate workflow)
- `/cdev {change-id}` - Start/continue multi-agent development
- `/cview {change-id}` - View detailed progress for a change
- `/cstatus {change-id}` - Quick progress status for a change
- `/pstatus` - Update PROJECT_STATUS.yml (cross-session context)

**Cross-Session Context (v2.1.0):**
- `PROJECT_STATUS.yml` (project root) - Quick context snapshot for new sessions
- Contains: infrastructure state, blockers, completed work, next priorities
- Created by: `cak init` (optional) or manually
- Updated by: `/pstatus` command or Main Claude prompts

**Best Practices (Dynamic):**
- `.claude/contexts/domain/project/best-practices/` (auto-generated by `/csetup`)
- Framework-specific guidelines from Context7 MCP

**Indexing (3 Levels):**
- Level 1: `.claude/contexts/domain/index.md` (Project Registry)
- Level 2: `.claude/contexts/domain/{project}/README.md` (Project Overview)
- Level 3: `.claude/contexts/domain/{project}/best-practices/index.md` (Best Practices Registry)

**Implementation Logic:**
- `@/.claude/lib/README.md` - Implementation logic overview
- `@/.claude/lib/agent-executor.md` - Agent retry & escalation logic (used by /cdev) + Incremental testing execution
- `@/.claude/lib/task-analyzer.md` - **v3.1.0!** Template-free task analysis with TDD classification (Step 2.6) ✨
- `@/.claude/lib/flags-updater.md` - Progress tracking protocol (Main Claude updates flags.json)
- `@/.claude/lib/agent-router.md` - Mandatory agent routing rules (enforce delegation)
- `@/.claude/lib/design-validator.md` - **v3.3.0!** Design system validation (prevention + detection) ✨
- `@/.claude/contexts/patterns/agent-discovery.md` - Shared agent discovery flow

---

## 📚 Best Practices System (v3.2.0 - Consolidated Pre-Work Context)

**Quick Summary:**
- `/csetup` generates **single `pre-work-context.md`** with ALL agent context
- **Consolidates:** Best practices, research findings, integration warnings, critical checklists
- **Context7 validates** each library and fetches best practices
- **Agents read ONE file** instead of multiple scattered files
- **File location:** `openspec/changes/{changeId}/pre-work-context.md`

**Key Changes:**
| Version | Change |
|---------|--------|
| v2.3.0 | NLP extraction + Context7 resolution (zero maintenance) |
| v2.5.0 | Smart Topic Query + Integration Risk Detection |
| v3.2.0 | **Consolidated `pre-work-context.md`** (single file for all agent context) |

**Detection Sources:**
| Source | Examples |
|--------|----------|
| Spec files | proposal.md, design.md, tasks.md |
| JS/TS | package.json, import statements |
| Python | requirements.txt, pyproject.toml, imports |
| Rust | Cargo.toml, use statements |
| Go | go.mod, import statements |
| PHP | composer.json |
| Ruby | Gemfile |

**Flow (v3.2.0):**
```
/csetup → analyze change (type, complexity, risk)
        → detect libraries from spec + package files
        → Context7 resolve + fetch best practices
        → determine research layers
        → detect integration warnings
        → generate critical checklist items
        → write pre-work-context.md (single file)
/cdev   → agents read pre-work-context.md in STEP 0
```

**Output File:**
| File | Sections |
|------|----------|
| `pre-work-context.md` | 1. Change Analysis, 2. Library Best Practices, 3. Research Findings, 4. Integration Warnings, 5. Critical Checklist, 6. Quick Reference |

---

## 🎨 Design System v2.1.0 (YAML-based)

**→ See:** `@/.claude/lib/detailed-guides/design-system.md` for complete guide

**Quick Summary:**
- `/extract https://site.com` → Extracts design from reference site (one at a time, incremental)
- `/designsetup @prd.md` → Interactive 3-round loop with theme selection
- Generates:
  - `data.yaml` - Complete design data (~800 lines) **FOR AGENTS**
  - `README.md` - Human-readable summary (~100 lines) **FOR HUMANS**

**Features:**
- Style Detection: Neo-Brutalism, Minimalist, Glassmorphism, Modern SaaS, etc.
- Theme Selection: AI recommends themes based on project context
- Animation Support: GSAP, ScrollTrigger, Framer Motion detection
- Scroll Patterns: stacking-cards, parallax, fade-in, slide-in
- Decorative Direction: USE/AVOID elements for theme consistency

**Flow:**
```
/extract https://site1.com → design-system/extracted/site1/data.yaml
/extract https://site2.com → design-system/extracted/site2/data.yaml (incremental)
           ↓
/designsetup @prd.md → design-system/data.yaml + design-system/README.md
           ↓
/pageplan → page-plan.md (reads data.yaml, auto-detects page type)
           ↓
/csetup → phases.md (reads page-plan.md)
           ↓
/cdev → uxui-frontend (reads data.yaml)
```

---

## 🎯 Design Validation System (v3.3.0 - NEW!)

**→ See:** `@/.claude/lib/design-validator.md` for full specification

**Problem Solved:**
- uxui-frontend agent ไม่อ่าน design-system/data.yaml → CSS ไม่ตรง design
- ux-tester อ่านแค่ code ไม่ได้เห็น actual rendered output
- Logic กระจายหลายไฟล์ → ไม่มี enforcement

**Solution: Single Source of Truth**

```
┌─────────────────────────────────────────────────────────────┐
│                    PREVENTION (Pre-Work)                     │
├─────────────────────────────────────────────────────────────┤
│  Main Claude → Pre-Flight Design Check (before /cdev)        │
│  uxui-frontend → STEP 0.5: Read data.yaml (MANDATORY)       │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                    DETECTION (Post-Work)                     │
├─────────────────────────────────────────────────────────────┤
│  ux-tester → Chrome DevTools Style Comparison                │
│              Compare computed styles vs data.yaml tokens     │
└─────────────────────────────────────────────────────────────┘
```

**What Gets Validated:**

| Token Category | Example Violation | Expected |
|----------------|-------------------|----------|
| Colors | #3b82f6 | bg-primary (from data.yaml) |
| Spacing | p-5, gap-7 | p-4, p-6, gap-8 (scale) |
| Animation | duration-200 | duration-150, 300, 500ms |
| Shadows | mixed sm+xl | consistent level |

**Agent Responsibilities:**

| Agent | What to Do |
|-------|------------|
| Main Claude | Pre-flight check before invoking uxui-frontend |
| uxui-frontend | STEP 0.5: Read data.yaml, report loaded tokens |
| ux-tester | Step 5.5: Chrome DevTools validation |

**Files Updated:**
- `.claude/lib/design-validator.md` (NEW - Single Source of Truth)
- `.claude/agents/02-uxui-frontend.md` (v2.1.0 - references design-validator)
- `.claude/agents/07-ux-tester.md` (v1.1.0 - Design Compliance Check)
- `.claude/commands/cdev.md` (Step 4.0 - Pre-Flight Check)

---

## ⚡ Context Optimization (v2.1.0)

**→ See:** `@/.claude/lib/detailed-guides/context-optimization.md` for complete guide

**Quick Summary:**
- **Problem:** Multiple files read by different commands/agents
- **Solution (v2.1.0):**
  - `data.yaml` (~800 lines) - **SINGLE SOURCE: All agents read this**
  - `README.md` (~100 lines) - **HUMAN-READABLE: Summary only**
- **Result:** Single file for all design data, consistent across all agents

---

## 📋 Page Planning System (v2.4.0 - Visual Planning Only)

**→ See:** `@/.claude/lib/detailed-guides/page-planning.md` for complete guide

**Quick Summary:**
- **Problem:** Agents duplicate components (Navbar 3x), wrong layout structure
- **Solution:** `/pageplan` → Generates `openspec/changes/{id}/page-plan.md` with:
  - Component reuse plan ✅ (prevent duplicates)
  - Layout wireframe (ASCII art for Desktop/Tablet/Mobile)
  - Animation blueprint (hover, focus, transition patterns)
  - Asset checklist ✅ (performance-optimized)

> **Note:** Content strategy and conversion copy moved to `/csetup` (Adaptive Depth Research)

**What Goes Where:**
| Concern | Command | Output File |
|---------|---------|-------------|
| Components, Layout, Animations | `/pageplan` | `page-plan.md` |
| Content, Conversion, UX Research | `/csetup` | `research-checklist.md` |

**Benefits:**
- Clear separation of Visual vs Research
- No duplication between commands
- Agents know exactly which file has which information

---

## 🧠 TaskMaster-style Analysis (v1.3.0)

**→ See:** `@/.claude/lib/detailed-guides/taskmaster-analysis.md` for complete guide

**Quick Summary:**
- **Problem:** Dumb task lists treat all tasks equally → no complexity/dependency/risk analysis → tasks fail, delays, security issues
- **Solution:** `/csetup` uses **6 analysis dimensions**: Complexity (1-10), Dependencies (auto-detected), Risk (LOW/MEDIUM/HIGH), Research requirements, Subtask breakdown, Priority (0-100)
- **Benefits:** Intelligent phases.md with time buffers (+41%), auto-added research phases, dependency order, risk mitigation
- **Inspired by:** [claude-task-master](https://github.com/eyaltoledano/claude-task-master)

---

## 🔄 Incremental Testing (v1.6.0)

**→ See:** `@/.claude/lib/detailed-guides/incremental-testing.md` for complete guide

**Quick Summary:**
- **Problem:** All-or-nothing testing → bugs found at scale (1000 records) → hard to debug, expensive rework
- **Solution:** Milestone-based validation → Test 1 record → 10 → errors → scale → catch bugs early (75% faster debug)
- **3 Patterns:** Backend API (4 milestones), Complex Form (3 milestones), Database Migration (3 milestones)
- **Round-based Retry:** 2 attempts → Main Claude intervention (hints vs ask human) → new round (unlimited)
- **Detection:** Auto-triggered for Risk=HIGH OR (Risk=MEDIUM + Complexity≥7) OR External API OR Data-intensive (~20-30% of tasks)
- **Benefits:** 60-70% rework reduction, 40-50% net speedup, 90% success rate with progressive confidence

---

## 🤖 Agent System

**→ See:** `@/.claude/lib/detailed-guides/agent-system.md` for complete guide

**Quick Summary:**
- **7 specialist agents**: integration (validate contracts), uxui-frontend (UI with mock data), **ux-tester** (persona-based UX testing), test-debug (tests/bugs), frontend (connect UI to API), backend (API endpoints), database (schemas/migrations)
- **Main Claude's role**: Orchestrator (plan, coordinate, report), NOT implementer (no writing code directly)
- **Self-check protocol**: Checklist before ANY work (detect work type → select agent → delegate)
- **Agent pre-work**: STEP 0 (project discovery for ALL) + STEP 1-5 (design fundamentals for uxui-frontend only)
- **Approval Gate (v2.7.0)**: ux-tester phase requires user approval before proceeding to backend

**Example workflow:**
```
User: "Build login system"
→ Phase 1: uxui-frontend (UI)
→ Phase 1.5: ux-tester (approval gate) ← NEW!
→ Phase 2: backend + database (parallel)
→ Phase 2.5: integration (validate contracts)
→ Phase 3: frontend (connect UI to API)
→ Phase 4: test-debug (tests)
```

---

## 📜 Version History

> **Full changelog with technical details, code examples, and migration guides:**
> See [`.claude/CHANGELOG.md`](./CHANGELOG.md)

**Recent versions:**
| Version | Key Feature |
|---------|-------------|
| v3.5.0 | **UX Tester v2.0** (Token Optimized + Human Testing Guide) |
| v3.4.0 | Complete Pseudocode Elimination (~3,210 lines → imperative instructions) |
| v3.3.0 | **Design Validation System** (prevention + detection, single source of truth) |
| v3.2.0 | Consolidated Pre-Work Context (single `pre-work-context.md` for agents) |
| v3.1.1 | Direct Best Practices Execution (Step 2.7 rewritten, no pseudocode) |
| v3.1.0 | TDD Classification + Development Principles Injection |
| v3.0.0 | Template-Free Architecture (AI-driven Task Analyzer v2.0) |
| v2.8.0 | Critical Flow Injection (auto-inject security/compliance items) |
| v2.7.0 | UX Testing Agent (persona-based, approval gate) |
| v2.5.0 | Smart Topic Query + Integration Risk Detection |
| v2.4.0 | Adaptive Depth Research (0-10+ dynamic layers) |
| v2.3.0 | Zero-Maintenance Tech Stack Detection |
| v2.2.0 | claude-mem Integration |
| v2.1.0 | Design System v2 (YAML-based) |
| v2.0.0 | Claude 4.5 Optimization (61% token reduction) |

---

## 📊 PROJECT_STATUS.yml Protocol (v2.2.0 - claude-mem Integration)

**WHY this exists:** New Claude sessions lose context about infrastructure state, blockers, and priorities. This file provides a quick snapshot.

**v2.2.0 Changes (claude-mem integration):**
- **REMOVED:** `decisions`, `notes`, `future_ideas` → claude-mem handles automatically
- **KEPT:** `blockers`, `next_priorities`, `technical_debt` → requires human decision
- **Query past context:** Just ask naturally → mem-search skill auto-invoked

### Session Start Behavior

If `PROJECT_STATUS.yml` exists in project root:
1. Read it first before other files
2. Note: `current_focus`, `blockers`, `infrastructure` state
3. If `last_updated` > 7 days (or `_config.stale_warning_days`) → Suggest: "PROJECT_STATUS.yml may be outdated. Run /pstatus?"

### Intelligent Update Prompts

Prompt "Update PROJECT_STATUS.yml?" when detecting these patterns:

| Event Detected | What to Update |
|----------------|----------------|
| After `/openspec:archive` completes | Add to `completed_changes` + check Non-Goals for `pending_followups` |
| User says "waiting for...", "need X from...", "blocked by..." | Add to `blockers` |
| User mentions blocker resolved | Remove from `blockers` |
| Infrastructure change (deploy, tunnel, DB migration) | Update `infrastructure` |
| User discusses priority shift | Update `next_priorities` |
| `/csetup {change-id}` started | Update `current_focus` + **check `pending_followups` for related items** |
| **Technical debt:** "ต้องแก้...", "should refactor...", "tech debt...", "needs cleanup..." | Add to `technical_debt` |
| **Problems found (by Claude):** "⚠️ ปัญหาที่พบ", "ไม่มี X", "missing X", "not configured" | Add to `technical_debt` or `blockers` |
| **Config gaps:** "ไม่ได้ตั้งค่า...", "need to configure...", "should add to CI/CD" | Add to `technical_debt` |
| **Sync issues:** "DB not synced", "schema mismatch", "local vs production differs" | Add to `blockers` + `infrastructure` |
| **Non-Goal needs follow-up:** design.md has "Non-Goal: X (separate proposal)" | Add to `pending_followups` when archiving |
| **Pending resolved:** User creates proposal for pending item | Remove from `pending_followups` |
| ~~**Future ideas, Decisions, Notes**~~ | **REMOVED** - claude-mem handles automatically |

### Update Protocol

- Always ask before modifying (user confirms)
- Use `/pstatus` for comprehensive review
- Keep updates atomic (one section at a time during work)
- Auto-detect archived changes not listed and suggest additions

### Example Interaction

```
# Session start
Claude: *reads PROJECT_STATUS.yml*
Claude: "I see auth-system is active, tunnel running but waiting for domain."

# During work - blocker resolved
User: "Domain is now configured"
Claude: "Update PROJECT_STATUS.yml?
         - Remove 'domain' from blockers
         - Update cloudflare_tunnel.waiting_for to null"

# After archiving
Claude: "Auth-system archived. Add to completed_changes?"

# Discussion - technical debt (still tracked in PROJECT_STATUS)
User: "ตรงนี้ code มันซ้ำๆ ต้องแก้ทีหลัง"
Claude: "Add to PROJECT_STATUS.yml technical_debt?
         - item: Refactor duplicated code in auth middleware
         - priority: medium"

# Problem found by Claude during analysis
Claude: "⚠️ ปัญหาที่พบ: ไม่มี migration step ใน CI/CD!"
Claude: "Add to PROJECT_STATUS.yml?
         technical_debt:
         - item: Add DB migration to CI/CD
         - priority: high"

# Query past decisions (claude-mem handles this now!)
User: "เราตัดสินใจเรื่อง database ว่ายังไงมาก่อน?"
Claude: *auto-invokes mem-search skill*
Claude: "จากการค้นหา พบ 2 decisions เกี่ยวกับ database:
         - #12345: Chose Drizzle over Prisma (3 days ago)
         - #12340: PostgreSQL over MongoDB (1 week ago)"

# Query past learnings (claude-mem handles this now!)
User: "เราเคยเจอ bug เกี่ยวกับ auth ไหม?"
Claude: *auto-invokes mem-search skill*
Claude: "พบ 1 bugfix เกี่ยวกับ auth:
         - #12330: Fixed token refresh race condition"

# /csetup checks pending_followups
User: "/csetup add-auth-system"
Claude: *reads PROJECT_STATUS.yml pending_followups*
Claude: "⚠️ Found related pending follow-up:
         - 'Database migration strategy' (from add-infrastructure-cicd)

         Options:
         1. Continue anyway (risk: schema sync issues)
         2. Address migration first
         3. Add migration step to this change's scope"
```

---

## 🧠 claude-mem Integration (v2.2.0)

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

### How claude-mem Works

```
1. You work normally (Read, Write, Edit, Bash, etc.)
   → claude-mem captures tool usage automatically

2. Session ends (/clear or exit)
   → claude-mem generates session summary

3. New session starts
   → claude-mem injects recent observations

4. You ask about past work
   → mem-search skill auto-invoked
```

### Query Examples

```
# Query past decisions
"เราตัดสินใจเรื่อง authentication ยังไง?"
→ Claude auto-invokes mem-search → shows past decisions

# Query past bugs
"เราเคยแก้ bug เกี่ยวกับ token ไหม?"
→ Claude shows past bugfixes

# Query implementation details
"เราทำ pagination ยังไง?"
→ Claude shows past implementation observations
```

### Agent Memory Access

Agents query claude-mem in STEP 0 before implementation:
- Check for past decisions about similar components
- Find previous solutions to similar problems
- Avoid repeating past mistakes

→ See: `.claude/agents/_shared/pre-work-checklist.md` Step 0.6

---

**💡 Remember:** This template is universal. Use Context7 for framework-specific docs!
