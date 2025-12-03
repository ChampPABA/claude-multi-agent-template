# CLAUDE.md

> **Navigation Hub for AI Agents**
> **Version:** 2.3.0 - Zero-Maintenance Tech Detection + Claude 4.5 Optimized

---

## Quick Start

```bash
# Design
/extract https://site.com    # Extract design from reference
/designsetup @prd.md         # Interactive design setup

# Development
/csetup {change-id}          # Setup change (auto-detect stack)
/cdev {change-id}            # Start multi-agent development
/cstatus {change-id}         # Quick progress check
/pstatus                     # Update PROJECT_STATUS.yml
```

---

## File Conventions

| OpenSpec Files | Purpose |
|----------------|---------|
| `proposal.md` | WHY - Goals, scope |
| `tasks.md` | WHAT - Implementation checklist |
| `design.md` | Technical architecture (optional) |

| Template Files | Purpose |
|----------------|---------|
| `STYLE_GUIDE.md` | Visual design (colors, fonts) |
| `tokens.json` | Design tokens (~800 tokens) |
| `page-plan.md` | UI component layout |
| `phases.md` | Agent workflow |
| `flags.json` | Progress tracking |

**Key:** `design.md` = Technical Architecture | `STYLE_GUIDE` = Visual Design

---

## Agents

| Agent | Phase | Role |
|-------|-------|------|
| uxui-frontend | 1 | UI with mock data |
| backend | 2 | API endpoints |
| database | 2 | Schemas/migrations |
| integration | 2.5 | Contract validation |
| frontend | 3 | Connect UI to API |
| test-debug | 4 | Tests & fixes |

**Main Claude:** Orchestrator only (plan, coordinate, report) - delegates implementation to agents.

---

## Key Features

### Best Practices (v2.3.0 - Zero Maintenance)

```
/csetup auto-detects libraries from:
├── Spec files (proposal.md, design.md, tasks.md)
├── JS/TS (package.json, imports)
├── Python (requirements.txt, pyproject.toml)
├── Rust (Cargo.toml), Go (go.mod), PHP, Ruby
└── Context7 validates → generates best-practices/*.md
```

### Design System (v2.0.0)

```
/extract → .claude/extractions/*.json
/designsetup → tokens.json + patterns/*.md + STYLE_GUIDE.md
/pageplan → page-plan.md (auto-detects page type)
```

**Page Type Handling:**
| Type | Decorations | Scroll Anims | Buyer Avatar |
|------|-------------|--------------|--------------|
| Landing | ✅ Full | ✅ | ✅ |
| Dashboard | ❌ Minimal | ❌ | ❌ |
| Auth | ❌ None | ❌ | ❌ |

### Validation Flow (4-Layer)

```
/csetup
├── Step 2.6: Feature BP (auth, payment, upload standards)
├── Step 2.7: Stack BP (auto-detected libraries)
└── Step 2.8: Library Capability (verify lib supports spec)

/cdev
└── Agent Step 0.5: Double-check feasibility
```

### TaskMaster Analysis (v1.3.0)

For each task: Complexity (1-10), Dependencies, Risk (LOW/MED/HIGH), Research needs, Priority (0-100).

### Incremental Testing (v1.6.0)

Triggered for: Risk=HIGH OR (Risk=MEDIUM + Complexity≥7) OR External API.
Milestone-based: Test 1 → 10 → errors → scale.

---

## Navigation

**Design:**
- `design-system/tokens.json` - Design tokens
- `design-system/patterns/*.md` - Code patterns
- `design-system/STYLE_GUIDE.md` - Human guide

**Patterns:**
- `.claude/contexts/patterns/task-classification.md` - Agent selection
- `.claude/contexts/patterns/agent-coordination.md` - Parallel/sequential
- `.claude/contexts/patterns/error-recovery.md` - Error handling

**Implementation:**
- `.claude/lib/agent-executor.md` - Agent retry & escalation
- `.claude/lib/task-analyzer.md` - Task analysis
- `.claude/lib/tdd-classifier.md` - TDD classification
- `.claude/lib/flags-updater.md` - Progress tracking

**Indexing (3 Levels):**
1. `.claude/contexts/domain/index.md` - Project Registry
2. `.claude/contexts/domain/{project}/README.md` - Project Overview
3. `.claude/contexts/domain/{project}/best-practices/index.md` - BP Registry

---

## PROJECT_STATUS.yml

Cross-session context for blockers, infrastructure, priorities.

**Update triggers:**
| Event | Update |
|-------|--------|
| Blocker resolved | Remove from `blockers` |
| Infrastructure change | Update `infrastructure` |
| `/csetup` started | Update `current_focus` |
| Archive change | Add to `completed_changes` |
| Future idea mentioned | Add to `future_ideas` |
| Tech debt found | Add to `technical_debt` |

---

## Claude 4.5 Principles Applied

| Before | After |
|--------|-------|
| "MUST", "WILL BE REJECTED" | Professional tone |
| "Don't do X" | "Use X instead" |
| Rules without context | Rules with WHY |
| ~1000 lines/agent | ~250-350 lines (65% smaller) |

**Shared components:** `.claude/agents/_shared/` (pre-work, package-manager, boundaries)

---

## What's NOT Included

- ❌ Framework patterns → Generated via `/csetup` + Context7
- ❌ Package managers → Auto-detected
- ❌ Spec frameworks → Optional (OpenSpec, BMAD, SpecKit)

**Use Context7 for framework-specific docs!**
