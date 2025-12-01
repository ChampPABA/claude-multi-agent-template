# CLAUDE.md

> **Navigation Hub for AI Agents**
> **Template Version:** 2.0.0 - Claude 4.5 Optimized + Design System v2.0
> **Latest:** Full template refactored with Claude 4.5 best practices (agents ~65% smaller) + Interactive design setup with theme selection

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
| `STYLE_GUIDE.md` | **Visual design** (colors, typography, spacing) | UI/Frontend phases |
| `tokens.json` | Design tokens with style/theme/animations (~800 tokens) | Quick UI reference |
| `page-plan.md` | UI component layout + content strategy | uxui-frontend agent |
| `phases.md` | Execution plan with agent assignments | All phases |
| `flags.json` | Progress tracking | All phases |

### Key Distinction

```
OpenSpec design.md    = Technical Architecture (data flow, API structure, system design)
Template STYLE_GUIDE  = Visual Design (colors, fonts, spacing, component styles)
```

**Agents should read BOTH when relevant:**
- `uxui-frontend` → STYLE_GUIDE.md (visual) + design.md (if has UI architecture)
- `backend` → design.md (API/data architecture)
- `database` → design.md (data models, relationships)
- `frontend` → STYLE_GUIDE.md (visual) + design.md (API contracts)

---

## 🎯 What is This Template?

Universal, framework-agnostic template for AI-assisted development.

**What's Included:**
- ✅ 6 Specialized Agents (integration + 5 domain specialists)
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

**Design/UI (v2.0.0):**
- `/extract https://site.com` - Extract design from reference sites (multi-URL, style detection)
- `/designsetup @prd.md` - Interactive design setup (3-round loop, theme selection)
- `design-system/tokens.json` - Design tokens with style/theme/animations (~800 tokens) ✨
- `design-system/patterns/*.md` - Selective code patterns (buttons, cards, forms, animations, decorations)
- `design-system/STYLE_GUIDE.md` - Human-readable guide (no code, ~150 lines)
- `.claude/extractions/*.json` - Extracted site data
- `@/.claude/lib/document-loader.md` - Token-efficient loading patterns
- `@/.claude/contexts/design/index.md` (General design principles - fallback)

**Development:**
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
- `/csetup` - **v1.8.0+:** Now auto-detects tech stack + generates best practices (replaces /psetup, /agentsetup)

**Page Planning (UI Tasks) - v2.0.0:**
- `/pageplan @prd.md @brief.md` - Generate page structure with auto page type detection
- Output: `openspec/changes/{id}/page-plan.md` (component reuse, buyer avatar, conversion copy, asset checklist)
- Auto-detects page type (landing/dashboard/auth) from proposal.md/tasks.md
- Reads tokens.json for style/theme/animations
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
- `@/.claude/lib/tdd-classifier.md` - TDD classification logic (used by /csetup)
- `@/.claude/lib/task-analyzer.md` - Task analysis with milestone generation
- `@/.claude/lib/flags-updater.md` - Progress tracking protocol (Main Claude updates flags.json)
- `@/.claude/lib/agent-router.md` - Mandatory agent routing rules (enforce delegation)
- `@/.claude/contexts/patterns/agent-discovery.md` - Shared agent discovery flow

---

## 📚 Best Practices System (v1.8.0)

**Quick Summary:**
- `/csetup` **auto-detects tech stack** from: package.json → design.md → proposal/tasks (3 sources)
- **Auto-generates best practices** from Context7 MCP (React, Next.js, Prisma, etc.)
- Files created in `.claude/contexts/domain/project/best-practices/`
- **Agents read** best practices before coding (validated by agent-executor)
- `/cdev` **injects** relevant best-practices paths into agent prompts

**Flow:**
```
/csetup → detect stack → query Context7 → generate best-practices
/cdev   → inject paths into prompt → agent reads → validation checks
```

---

## 🎨 Design System v2.0.0 (Interactive Setup)

**→ See:** `@/.claude/lib/detailed-guides/design-system.md` for complete guide

**Quick Summary:**
- `/extract https://site.com` → Extracts design from reference sites (multi-URL, style detection)
- `/designsetup @prd.md` → Interactive 3-round loop with theme selection
- Generates:
  - `tokens.json` - Design tokens with style/theme/animations (~800 tokens) **FOR AGENTS**
  - `patterns/*.md` - Code patterns (buttons, cards, forms, animations, decorations) **SELECTIVE LOADING**
  - `STYLE_GUIDE.md` - Human-readable guide (no code, ~150 lines) **FOR HUMANS**

**New Features in v2.0.0:**
- 🎯 **Style Detection:** Neo-Brutalism, Minimalist, Glassmorphism, Modern SaaS, etc.
- 🎭 **Theme Selection:** AI recommends themes based on project context
- 🎬 **Animation Support:** GSAP, ScrollTrigger, Framer Motion detection
- 📜 **Scroll Patterns:** stacking-cards, parallax, fade-in, slide-in
- 🖼️ **Decorative Direction:** USE/AVOID elements for theme consistency

**Flow:**
```
/extract → .claude/extractions/*.json
           ↓
/designsetup → tokens.json + patterns/*.md + STYLE_GUIDE.md
           ↓
/pageplan → page-plan.md (reads tokens.json, auto-detects page type)
           ↓
/csetup → phases.md (reads page-plan.md)
           ↓
/cdev → uxui-frontend (reads tokens.json + patterns/*.md selectively)
```

---

## ⚡ Context Optimization (v2.0.0)

**→ See:** `@/.claude/lib/detailed-guides/context-optimization.md` for complete guide

**Quick Summary:**
- **Problem:** 20K tokens wasted (STYLE_GUIDE.md read 4x by different commands/agents)
- **Solution (v2.0.0):**
  - `tokens.json` (~800 tokens) - **PRIMARY: All agents read this**
  - `patterns/*.md` - **SELECTIVE: Load based on page type**
  - `STYLE_GUIDE.md` (~150 lines) - **HUMAN-READABLE: No code**
- **Page Type Detection:**
  - Landing/Marketing → Full patterns (buttons, cards, scroll-animations, decorations)
  - Dashboard/Admin → Minimal patterns (buttons, cards, forms)
  - Auth → Clean patterns (buttons, forms)
- **Result:** 84% token reduction (~800 tokens vs ~5000), 4x faster, theme consistency

---

## 📋 Page Planning System (v2.0.0 - Auto Page Type Detection)

**→ See:** `@/.claude/lib/detailed-guides/page-planning.md` for complete guide

**Quick Summary:**
- **Problem:** Agents duplicate components (Navbar 3x), use random colors, lorem ipsum content, wrong decorations for page type
- **Solution:** `/pageplan @prd.md @brief.md` → Generates `openspec/changes/{id}/page-plan.md` with:
  - **Auto page type detection** (landing/dashboard/auth from proposal.md/tasks.md)
  - **tokens.json integration** (style, theme, animations, decorative direction)
  - **Selective pattern loading** (only load patterns relevant to page type)
  - Component reuse plan ✅ (prevent duplicates)
  - Buyer avatar analysis (Eugene Schwartz framework) **for marketing pages only**
  - Conversion-optimized content (pain → promise → CTA) **for marketing pages only**
  - Asset checklist ✅ (performance-optimized)

**Page Type Handling:**
| Page Type | Decorations | Scroll Anims | Buyer Avatar | Patterns Loaded |
|-----------|-------------|--------------|--------------|-----------------|
| Landing/Marketing | ✅ Full | ✅ Enabled | ✅ Enabled | buttons, cards, scroll-anims, decorations |
| Dashboard/Admin | ❌ Minimal | ❌ Disabled | ❌ Skipped | buttons, cards, forms |
| Auth (Login/Register) | ❌ None | ❌ Disabled | ❌ Skipped | buttons, forms |

**Benefits:**
- Auto-detects page type from context (no manual config)
- Theme + decorations from tokens.json applied consistently
- 84% token reduction (selective pattern loading)
- Conversion-optimized only where needed (marketing pages)

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
- **6 specialist agents**: integration (validate contracts), uxui-frontend (UI with mock data), test-debug (tests/bugs), frontend (connect UI to API), backend (API endpoints), database (schemas/migrations)
- **Main Claude's role**: Orchestrator (plan, coordinate, report), NOT implementer (no writing code directly)
- **Self-check protocol**: Checklist before ANY work (detect work type → select agent → delegate)
- **Agent pre-work**: STEP 0 (project discovery for ALL) + STEP 1-5 (design fundamentals for uxui-frontend only)

**Example workflow:**
```
User: "Build login system"
→ Phase 1: uxui-frontend (UI)
→ Phase 2: backend + database (parallel)
→ Phase 2.5: integration (validate contracts)
→ Phase 3: frontend (connect UI to API)
→ Phase 4: test-debug (tests)
```

---

## 🆕 v2.0.0: Claude 4.5 Optimization + Design System v2.0

**Based on:** [Claude 4 Best Practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-4-best-practices)

### Claude 4.5 Changes Applied

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

### Best Practices Applied

1. **Tone Calibration** - Professional, direct (not aggressive)
2. **Action Orientation** - Explicit "Write code" vs "Consider"
3. **Prevent Overengineering** - Clear boundaries
4. **Encourage Exploration** - Read before implementing
5. **Rich Output When Needed** - Specify requirements
6. **Context for Rules** - Explain WHY
7. **Positive Instructions** - "Use X" not "Don't Y"

### Additional Files Refactored

Beyond the 6 agent files, these supporting files were also updated:

**Implementation Logic (lib/):**
| File | Changes |
|------|---------|
| `agent-router.md` | Routing table format, removed "CANNOT/forbidden" language |
| `agent-executor.md` | Professional rejection messages, table format |
| `context-loading-protocol.md` | WHY explanations, removed "CRITICAL" warnings |
| `flags-updater.md` | Best practices table, removed "Step 3 CANNOT be skipped" |
| `document-loader.md` | Table format for DO/DON'T sections |
| `detailed-guides/agent-system.md` | Compact table format, shared file references |

**Commands:**
| File | Changes |
|------|---------|
| `cdev.md` | WHY context for best practices, softer tone |
| `csetup.md` | Best Practices / Anti-Patterns format |
| `pageplan.md` | "Guidelines" instead of "CRITICAL Rules" |
| `designsetup.md` | "Follow this format" instead of "EXACT format" |

**Patterns (contexts/patterns/):**
| File | Changes |
|------|---------|
| `validation-framework.md` | WHY explanations, removed "🚨" symbols |
| `error-recovery.md` | "⚠️" instead of "🚨", professional escalation format |
| `ui-component-consistency.md` | "Common Issues" instead of "Red Flags" |
| `task-breakdown.md` | Positive framing for incremental approach |
| `agent-discovery.md` | Softer language, "⚠️ Fallback" instead of "🚨" |
| `code-standards.md` | "File Creation Policy" with WHY table |
| `animation-patterns.md` | "⚠️ Common Mistakes" instead of "🚨" |
| `frontend-component-strategy.md` | "⚠️ Anti-Patterns" instead of "🚨" |
| `performance-optimization.md` | "⚠️ Common Mistakes" instead of "🚨" |
| `change-workflow.md` | Table format for read-only files |
| `task-classification.md` | "Agent Capabilities Reference" section title |

**Design (contexts/design/):**
| File | Changes |
|------|---------|
| `index.md` | "should check" instead of "MUST check" |
| `box-thinking.md` | "⚠️ Common Mistakes" instead of "🚨" |

**Templates:**
| File | Changes |
|------|---------|
| `phases-sections/frontend-mockup.md` | Table with WHY for design rules |
| `design-context-template.md` | "⚠️ Design Rules" instead of "🚨 Critical" |
| `STYLE_GUIDE.template.md` | "🔧 Troubleshooting" instead of "🚨" |

**Other lib files:**
| File | Changes |
|------|---------|
| `lib/README.md` | Softer descriptions, "📌 Important" |
| `detailed-guides/taskmaster-analysis.md` | "🔴 HIGH" instead of "🚨 HIGH" |

---

## 📊 PROJECT_STATUS.yml Protocol (v2.1.0)

**WHY this exists:** New Claude sessions lose context about infrastructure state, blockers, and priorities. This file provides a quick snapshot.

### Session Start Behavior

If `PROJECT_STATUS.yml` exists in project root:
1. Read it first before other files
2. Note: `current_focus`, `blockers`, `infrastructure` state
3. If `last_updated` > 7 days (or `_config.stale_warning_days`) → Suggest: "PROJECT_STATUS.yml may be outdated. Run /pstatus?"

### Intelligent Update Prompts

Prompt "Update PROJECT_STATUS.yml?" when detecting these patterns:

| Event Detected | What to Update |
|----------------|----------------|
| After `/openspec:archive` completes | Add to `completed_changes` |
| User says "waiting for...", "need X from...", "blocked by..." | Add to `blockers` |
| User mentions blocker resolved | Remove from `blockers` |
| Infrastructure change (deploy, tunnel, DB migration) | Update `infrastructure` |
| User discusses priority shift | Update `next_priorities` |
| `/csetup {change-id}` started | Update `current_focus.active_change` |

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

# During work
User: "Domain is now configured"
Claude: "Update PROJECT_STATUS.yml?
         - Remove 'domain' from blockers
         - Update cloudflare_tunnel.waiting_for to null"

# After archiving
Claude: "Auth-system archived. Add to completed_changes?"
```

---

**💡 Remember:** This template is universal. Use Context7 for framework-specific docs!
