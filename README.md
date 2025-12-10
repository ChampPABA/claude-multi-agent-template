# Claude Agent Kit

> Multi-Agent Implementation Engine for [OpenSpec](https://github.com/Fission-AI/OpenSpec)

[![npm version](https://badge.fury.io/js/@champpaba%2Fclaude-agent-kit.svg)](https://www.npmjs.com/package/@champpaba/claude-agent-kit)

## Quick Start

```bash
npm install -g @champpaba/claude-agent-kit
cd your-project
cak init

# In Claude Code
/csetup my-feature
/cdev my-feature
```

## Agents

| Agent | Phase | Role |
|-------|-------|------|
| uxui-frontend | 1 | UI with mock data |
| ux-tester | 1.5 | Persona-based UX testing (approval gate) |
| backend | 2 | API endpoints |
| database | 2 | Schemas |
| integration | 2.5 | Contract validation |
| frontend | 3 | Connect UI to API |
| test-debug | 4 | Tests & fixes |

## Features

- **Template-Free Architecture (v3.0.0)** - AI-driven task analysis, no hardcoded templates
- **Task Analyzer v2.0** - Complexity scoring, auto-add best practices, incremental milestones
- **Critical Flow Injection (v2.8.0)** - Non-negotiable security items auto-injected for auth, payment, healthcare, fintech
- **UX-Tester Agent (v2.7.0)** - Persona-based UX testing with weighted conversion prediction
- **Smart Topic Query (v2.5.0)** - Cross-library integration detection + risk summary
- **Adaptive Depth Research (v2.4.0)** - Dynamic research layers (0-10+) based on change complexity
- **Zero-Maintenance Tech Detection** - Auto-detects ANY library in ANY language via Context7
- **Visual Page Planning** - Layout wireframes, component plans, animation blueprints
- **Cross-session Context** - `PROJECT_STATUS.yml` maintains state across sessions
- **Design System v2.1** - YAML-based extraction with single data.yaml output

## Template-Free Architecture (v3.0.0)

```
Problem: Templates override user's tasks.md structure
         e.g., "refactor" template = 2 phases, but tasks.md has 5 phases

Solution: Task Analyzer v2.0 - AI-driven analysis, tasks.md is single source of truth

Before (Template-based):
  tasks.md (5 phases) → template selection → phases.md (2 phases) ❌ LOST TASKS

After (Template-free):
  tasks.md (5 phases) → AI analysis → phases.md (5 phases + auto-adds) ✅ ALL PRESERVED

Task Analyzer v2.0 Pipeline:
  1. Parse ALL tasks from tasks.md (preserve hierarchy)
  2. AI Analysis: complexity, risk, agent, dependencies (NO keyword matching)
  3. Auto-Add: security review, checkpoints, error handling (NO warnings)
  4. Generate Milestones: batch processing, external API, repository patterns
  5. Sort: dependencies first, HIGH risk early, foundation before features
  6. Inject UX Testing: Phase X.5 after every uxui-frontend phase
```

**Auto-Add Rules (no user confirmation needed):**
| Condition | Auto-Added Task |
|-----------|-----------------|
| HIGH risk | Checkpoint before next phase |
| External API | Error handling, retry, timeout |
| Implementation (complexity >= 5) | Verification task |
| Database changes | Backup verification, rollback test |
| Security-critical | Security review, log check |

**Incremental Milestone Patterns:**
| Pattern | Strategy | Example |
|---------|----------|---------|
| Batch Processing | 1 → 5 → 20 → full | "Process 10,000 records" |
| External API | mock → single → errors → scale | "Send 100 API calls" |
| Repository Layer | 1 method → half → all | "Implement 8 methods" |
| Complex Form | 1 field → 1 step → full | "Multi-step wizard" |

## Critical Flow Injection (v2.8.0)

```
Problem: Research is flexible, but security items are non-negotiable
         e.g., Password hashing, PCI-DSS, HIPAA compliance

Solution: Auto-inject critical items based on change analysis

Detected Flows → Injected Items:
  ├── Auth     → Password hashing, JWT secure storage, session mgmt (7 items)
  ├── Payment  → PCI key security, no card storage, webhook verification (5 items)
  ├── Healthcare → HIPAA: PHI encryption, access control, audit trail (5 items)
  └── Fintech  → PCI-DSS: encryption, key rotation, audit logging (6 items)

Each item has:
  { id, check, why, severity: 'critical' }
```

**How it works:**
1. `/csetup` analyzes change → detects `hasAuth`, `hasPayment`, `industryContext`
2. Research layers are generated dynamically (flexible)
3. Critical items are INJECTED into appropriate layers (non-negotiable)
4. Agents receive checklist with both research + critical items

## Smart Topic Query (v2.5.0)

```
Problem: Context7 queries missed integration docs (e.g., Drizzle + Auth.js adapter)

Solution: Include other library names in Context7 topic query

Old: topic = "best practices, patterns"
New: topic = "best practices, adapter, integration, {other-lib-names}"

Result:
  ├── drizzle.md (with Auth.js adapter info)
  ├── auth-js.md (with DrizzleAdapter config)
  └── INTEGRATION_RISKS.md (cross-library concerns)
```

**Detected Risk Patterns:** adapter, schema/column naming, sync, webhook, lifecycle

## Adaptive Depth Research (v2.4.0)

```
/csetup analyzes change complexity and generates research layers:

  Typo fix           → 0 layers (no research needed)
  Simple API         → 2 layers (Best Practice, API Design)
  Auth system        → 4 layers (+Security, +Testing)
  E-commerce         → 7 layers (+Payment, +UX, +Integration)
  Healthcare (HIPAA) → 10 layers (+Compliance, +Audit, etc.)

Knowledge Sources:
  ├── Domain (UX, DB design, Security) → Claude's Knowledge
  └── Stack (Prisma, React, Next.js)   → Context7
```

## Flow (v2.5.0)

```
/designsetup → tokens.json, patterns/*.md
       ↓
/pageplan → page-plan.md (VISUAL: layout, components, animations)
       ↓
/csetup → research-checklist.md (RESEARCH: best practices, content)
        → best-practices/*.md (Stack: Context7 + Smart Topic Query)
        → INTEGRATION_RISKS.md (if cross-library risks detected)
       ↓
/cdev → Agents read all files in STEP 0
```

**Separation of Concerns:**
| Command | Focus | Output |
|---------|-------|--------|
| `/pageplan` | Visual (layout, wireframe, animations) | `page-plan.md` |
| `/csetup` | Research (best practices, content, UX) | `research-checklist.md` |

## Commands

**CLI:** `cak init` | `cak update`

**Slash:** `/designsetup` `/pageplan` `/csetup {id}` `/cdev {id}` `/cstatus {id}` `/pstatus`

## Links

[npm](https://www.npmjs.com/package/@champpaba/claude-agent-kit) | [GitHub](https://github.com/ChampPABA/claude-multi-agent-template) | [OpenSpec](https://github.com/Fission-AI/OpenSpec)

MIT License
