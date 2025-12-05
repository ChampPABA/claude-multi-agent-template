# CLAUDE.md

> **Navigation Hub for AI Agents**
> **Template Version:** 2.5.0 - Smart Topic Query
> **Latest:** Cross-library integration detection + Integration risk summary + Proactive error prevention

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

## 📚 Best Practices System (v2.5.0 - Smart Topic Query)

**Quick Summary:**
- `/csetup` **dynamically detects any library** from spec text + package files (no hardcoded mappings)
- **Works with any language:** JavaScript, Python, Rust, Go, PHP, Ruby - automatically
- **Context7 validates** each potential library name and resolves to official docs
- **v2.5.0:** Smart Topic Query includes other library names for cross-library integration docs
- **v2.5.0:** Auto-generates `INTEGRATION_RISKS.md` with detected concerns
- Files created in `.claude/contexts/domain/project/best-practices/`
- **Agents read** best practices + integration risks before coding

**Key Changes:**
| Version | Change |
|---------|--------|
| v2.3.0 | NLP extraction + Context7 resolution (zero maintenance) |
| v2.5.0 | Smart Topic Query + Integration Risk Detection |

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

**Flow (v2.5.0):**
```
/csetup → extract potential library names from ALL text sources
        → Context7 resolve-library-id (validates if real library)
        → Context7 get-library-docs (Smart Topic Query with other lib names)
        → detect integration risks from docs content
        → generate .md files for each verified library
        → generate INTEGRATION_RISKS.md if risks detected
/cdev   → inject paths into prompt → agent reads → validation checks
```

**Output Files:**
| File | Content |
|------|---------|
| `{lib}.md` | Library best practices with integration info |
| `INTEGRATION_RISKS.md` | Cross-library risks + checklist (if any detected) |
| `index.md` | Registry of all best practices files |

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

**Flow (v2.4.0):**
```
/extract → .claude/extractions/*.json
           ↓
/designsetup → tokens.json + patterns/*.md + STYLE_GUIDE.md
           ↓
/pageplan → page-plan.md (VISUAL: layout, components, animations, assets)
           ↓
/csetup → research-checklist.md (RESEARCH: best practices, content, UX)
        → best-practices/*.md (Stack: Context7)
        → phases.md
           ↓
/cdev → uxui-frontend reads:
        - tokens.json (design tokens)
        - patterns/*.md (code patterns)
        - page-plan.md (visual structure)
        - research-checklist.md (content & UX)
```

**Separation of Concerns:**
| Command | Focus | Output |
|---------|-------|--------|
| `/pageplan` | Visual (layout, wireframe, animations) | `page-plan.md` |
| `/csetup` | Research (best practices, content, UX) | `research-checklist.md` |

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

## 🆕 v2.5.0: Smart Topic Query + Integration Risk Detection

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

## 🆕 v2.4.0: Adaptive Depth Research

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

### Output Example

```markdown
# Research Checklist: healthcare-portal

> Generated by Adaptive Depth Research (v2.4.0)
> Complexity: 9/10 | Risk: HIGH

## Summary

| Layer | Focus | Status |
|-------|-------|--------|
| L1: Best Practice | How do others implement healthcare? | ⏳ Pending |
| L2: Security Requirements | What security measures? | ⏳ Pending |
| L3: Healthcare Compliance | What HIPAA regulations? | ⏳ Pending |
...

## L1: Best Practice / Industry Standard

**Focus:** How do others implement healthcare portals?

### Key Questions
- [ ] What is the industry standard for healthcare portals?
- [ ] What are common patterns and anti-patterns?
...
```

---

## 🆕 v2.3.0: Zero-Maintenance Tech Stack Detection

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
| After `/openspec:archive` completes | Add to `completed_changes` + check Non-Goals for `pending_followups` |
| User says "waiting for...", "need X from...", "blocked by..." | Add to `blockers` |
| User mentions blocker resolved | Remove from `blockers` |
| Infrastructure change (deploy, tunnel, DB migration) | Update `infrastructure` |
| User discusses priority shift | Update `next_priorities` |
| `/csetup {change-id}` started | Update `current_focus` + **check `pending_followups` for related items** |
| **Future features/ideas:** "อยากให้มี...", "want to add...", "later we should...", "in the future..." | Add to `future_ideas` |
| **Technical debt:** "ต้องแก้...", "should refactor...", "tech debt...", "needs cleanup..." | Add to `technical_debt` |
| **Decisions made:** "ตัดสินใจว่า...", "we decided...", "going with...", "chose X over Y" | Add to `decisions` |
| **Learnings/notes:** "พบว่า...", "discovered...", "note:...", "important:..." | Add to `notes` |
| **Problems found (by Claude):** "⚠️ ปัญหาที่พบ", "ไม่มี X", "missing X", "not configured" | Add to `technical_debt` or `blockers` |
| **Config gaps:** "ไม่ได้ตั้งค่า...", "need to configure...", "should add to CI/CD" | Add to `technical_debt` |
| **Sync issues:** "DB not synced", "schema mismatch", "local vs production differs" | Add to `blockers` + `infrastructure` |
| **Non-Goal needs follow-up:** design.md has "Non-Goal: X (separate proposal)" | Add to `pending_followups` when archiving |
| **Pending resolved:** User creates proposal for pending item | Remove from `pending_followups` |

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

# Casual conversation - future idea
User: "อยากให้มี dark mode ด้วยนะ ไว้ทำทีหลัง"
Claude: "Add to PROJECT_STATUS.yml future_ideas?
         - idea: Dark mode support
         - context: User requested, low priority"

# Discussion - technical debt
User: "ตรงนี้ code มันซ้ำๆ ต้องแก้ทีหลัง"
Claude: "Add to PROJECT_STATUS.yml technical_debt?
         - item: Refactor duplicated code in auth middleware
         - priority: medium"

# Decision made
User: "ตัดสินใจใช้ Drizzle แทน Prisma แล้ว เพราะ type-safe กว่า"
Claude: "Add to PROJECT_STATUS.yml decisions?
         - decision: Use Drizzle over Prisma
         - reason: Better type safety"

# Problem found by Claude during analysis
Claude: "⚠️ ปัญหาที่พบ: ไม่มี migration step ใน CI/CD!"
Claude: "Add to PROJECT_STATUS.yml?
         technical_debt:
         - item: Add DB migration to CI/CD
         - reason: Schema not synced between local and VPS
         - priority: high"

# Config gap discovered
Claude: "Local DB กับ VPS schema ไม่ sync กัน"
Claude: "Add to PROJECT_STATUS.yml?
         blockers:
         - id: db-schema-sync
         - description: Local and VPS DB schemas out of sync
         infrastructure.database:
         - status: degraded
         - notes: Schema mismatch, need migration"

# Archive with Non-Goals that need follow-up
Claude: "Archiving add-infrastructure-cicd..."
Claude: *reads design.md, finds Non-Goals: "Database migrations (separate proposal)"*
Claude: "Add to PROJECT_STATUS.yml pending_followups?
         - item: Database migration strategy
         - from_change: add-infrastructure-cicd
         - reason: Non-Goal marked 'separate proposal'
         - affects: ['any change with DB schema']"

# /csetup checks pending_followups (Medium aggressiveness)
User: "/csetup add-auth-system"
Claude: *reads PROJECT_STATUS.yml pending_followups*
Claude: "⚠️ Found related pending follow-up:
         - 'Database migration strategy' (from add-infrastructure-cicd)
         - Affects: 'any change with DB schema'

         This change adds DB tables. The migration strategy hasn't been addressed yet.

         Options:
         1. Continue anyway (risk: schema sync issues)
         2. Address migration first (create proposal)
         3. Add migration step to this change's scope

         Which approach?"
```

---

**💡 Remember:** This template is universal. Use Context7 for framework-specific docs!
