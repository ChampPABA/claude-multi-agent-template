# Change Workflow Pattern

> **Multi-Agent Orchestration with OpenSpec Integration**

---

## 🎯 Overview

This pattern describes how the multi-agent system integrates with OpenSpec to deliver change-based development workflows.

**Key Concepts:**
- **Per-change context**: Each OpenSpec change has isolated `.claude/` directory
- **Adaptive phases**: 6 workflow templates auto-selected based on task analysis
- **Real-time tracking**: `flags.json` updated by agents after each phase
- **Progress visibility**: Terminal-based progress views (`/cview`, `/cstatus`)

---

## 📋 Workflow Commands

### 1. `/csetup {change-id}` - Change Setup (Includes Project Setup)

**When to use:** After creating OpenSpec change, before development

**What it does:**
1. Reads `proposal.md`, `tasks.md`, `design.md`
2. Analyzes task types (frontend, backend, database, script, etc.)
3. Selects appropriate phase template (6 options)
4. Generates `phases.md` (agent workflow)
5. Generates `flags.json` (progress tracking)
6. Generates `context.md` (change-specific tech)

**Output:**
```
openspec/changes/CHANGE-XXX/.claude/
├── phases.md      # Agent workflow (19 phases for full-stack)
├── flags.json     # Progress tracking (updated by agents)
└── context.md     # Change-specific tech & patterns
```

**Phase Templates:**

| Template | Phases | Use Case | Example |
|----------|--------|----------|---------|
| **full-stack** | 19 | Frontend + Backend + Database | User auth system |
| **frontend-only** | 11 | UI components only | Landing page |
| **backend-only** | 10 | API endpoints only | REST API |
| **script-only** | 7 | CLI tools | Data migration script |
| **bug-fix** | 5 | Fix existing code | Patch security bug |
| **refactor** | 4 | Code improvements | Extract reusable components |

---

### 2. `/cdev {change-id}` - Start/Continue Development

**When to use:** After `/csetup`, to execute agent workflow

**What it does:**
1. Reads current phase from `flags.json`
2. Gets agent assignment from `phases.md`
3. Invokes appropriate agent(s)
4. Updates progress in `flags.json`
5. Continues or pauses for user action

**Workflow:**
```
1. User: "/cdev CHANGE-003"
   ↓
2. Read flags.json → Current phase: "frontend-mockup"
   ↓
3. Read phases.md → Agent: "uxui-frontend"
   ↓
4. Invoke uxui-frontend agent with:
   - Project context (domain/)
   - Change context (.claude/)
   - OpenSpec files (proposal, tasks, design)
   - Current phase instructions
   ↓
5. Agent completes phase → Updates flags.json
   ↓
6. Check next phase:
   - If automated → Continue?
   - If user action → Pause
   - If complete → Done!
```

**Example Session:**
```bash
$ /cdev CHANGE-003

✅ Reading change context...
📁 Change: CHANGE-003 Create Landing Page
📊 Template: frontend-only (11 phases)
📍 Current: Phase 1/11 Frontend Mockup

Invoking uxui-frontend agent...

[Agent executes Phase 1...]

✅ Phase 1 completed! (95 minutes)

📁 Files created:
   - src/app/page.tsx
   - src/components/landing/hero-section.tsx
   - src/components/landing/features-section.tsx

📍 Next: Phase 2 Accessibility Test (test-debug)

Continue? (yes/no)
> yes

[Continues...]

🛑 Phase 3 requires manual testing.
Test visual consistency using agent-browser.
When done: /cdev CHANGE-003 --continue

$ [User tests]

$ /cdev CHANGE-003 --continue

Updating flags → Phase 3 marked completed
📍 Next: Phase 4 Business Logic Validation
Continue? (yes/no)
> yes

[Continues until complete...]

✅ All phases completed! (11/11)
Ready to archive!
```

---

### 3. `/cview {change-id}` - View Progress

**When to use:** Check detailed phase-by-phase progress

**Output:**
```
════════════════════════════════════════════════════════════
📋 CHANGE-003: Create Landing Page (frontend-only)
════════════════════════════════════════════════════════════

📊 Overall Progress: [████████████░░░░░░░░] 64% (7/11 phases complete)

⏱️  Time Tracking:
    Total Spent:      2h 55min
    Total Estimated:  3h 15min
    Efficiency:       111% (ahead of schedule)
    Remaining:        ~35 minutes

════════════════════════════════════════════════════════════
✅ COMPLETED PHASES (7)
════════════════════════════════════════════════════════════

[1] Frontend Mockup (uxui-frontend)
    ⏱️  2025-10-30 10:00 → 11:35 (95 min, estimated 90 min)
    📁 Created: 4 files
       - src/app/page.tsx
       - src/components/landing/hero-section.tsx
       - src/components/landing/features-section.tsx
       - src/components/landing/cta-section.tsx
    ✓ Tasks: 1.1, 1.2, 1.3, 2.1, 2.2, 2.3, 3.1, 3.2, 3.3
    📝 All landing page sections created. Responsive design implemented.

[2] Accessibility Test (test-debug)
    ⏱️  2025-10-30 11:35 → 11:43 (8 min, estimated 10 min)
    🎯 Lighthouse: 98/100
    ✓ Contrast ratio: Pass
    ✓ ARIA labels: Complete
    📝 Minor contrast adjustment made to CTA button.

[... 5 more completed phases ...]

════════════════════════════════════════════════════════════
🔄 IN PROGRESS (1)
════════════════════════════════════════════════════════════

[8] Refactor (test-debug) ← CURRENT
    ⏱️  Started: 2025-10-30 14:15 (15 minutes ago)
    ⏱️  Estimated: 20 minutes total (~5 minutes remaining)
    📝 Extracting reusable button component. Optimizing CSS classes.

════════════════════════════════════════════════════════════
⏳ PENDING (3)
════════════════════════════════════════════════════════════

[9] Test Coverage Report (test-debug)
    ⏱️  Estimated: 5 minutes
    📋 Generate final coverage report

[10] Documentation (integration)
     ⏱️  Estimated: 15 minutes
     📋 Update README, add JSDoc comments

[11] Final Report (integration)
     ⏱️  Estimated: 10 minutes
     📋 Generate verbose report for archive
```

---

### 4. `/cstatus {change-id}` - Quick Status

**When to use:** Quick glance at progress

**Output:**
```
📊 CHANGE-003: feature | frontend-only

Progress: [████████░░] 64% (7/11 phases)

Current Phase: #8 Refactor (test-debug)
├─ Started: 14:15 (15 minutes ago)
├─ Estimated: 20 minutes
└─ Status: in_progress

✅ Completed: 7 phases
🔄 In Progress: 1 phase
⏳ Remaining: 3 phases

⏱️ Time:
├─ Spent: 2h 55min (estimated: 3h 15min)
├─ Remaining: ~35 minutes
└─ Efficiency: 111% (ahead of estimate)

📈 Stats:
├─ Tests: 12 passed, 0 failed (75% coverage)
├─ Issues: 2 found, 2 fixed, 0 remaining
└─ Files: 4 created, 2 modified

🎯 Next Steps:
1. Complete refactoring (20 min)
2. Test coverage report (5 min)
3. Documentation (15 min)

Commands:
→ Detailed view: /cview CHANGE-003
→ Continue dev: /cdev CHANGE-003
```

---

## 🗺️ Agent Discovery Flow

**Every agent follows this 5-level discovery sequence:**

```
Level 1: Find Current Project
Read: .claude/contexts/domain/index.md
→ Extract: Current project name

Level 2: Load Project Overview
Read: .claude/contexts/domain/{project}/README.md
→ Extract: Tech stack summary, package manager

Level 3: Check Best Practices Index
Read: .claude/contexts/domain/{project}/best-practices/index.md
→ Extract: Relevant files for this agent

Level 4: Load Relevant Best Practices
Read: .claude/contexts/domain/{project}/best-practices/{files}
→ Extract: Framework-specific patterns

Level 5: Change Context (Current Task)
IF openspec/changes/{change-id}/.claude/ EXISTS:
  1. Read: context.md → Change-specific tech
  2. Read: flags.json → Current progress
  3. Read: phases.md → Current phase instructions
  4. Read: proposal.md, tasks.md, design.md → Requirements
ELSE:
  Skip (working on general task, not OpenSpec change)

✅ Discovery Complete
Report: "✅ Project Context Loaded"
```

---

## 📤 Agent Post-Work (Flags Update)

**After completing a phase, agents should update flags.json:**

```json
{
  "phases": {
    "frontend-mockup": {
      "status": "completed",
      "completed_at": "2025-10-30T11:35:00Z",
      "actual_minutes": 95,
      "tasks_completed": ["1.1", "1.2", "1.3"],
      "files_created": [
        "src/app/page.tsx",
        "src/components/landing/hero-section.tsx"
      ],
      "notes": "All sections created. Responsive design implemented."
    }
  },
  "current_phase": "accessibility-test",
  "updated_at": "2025-10-30T11:35:00Z"
}
```

**Files agents should not update (read-only):**

| File | WHY Read-Only |
|------|---------------|
| `tasks.md` | OpenSpec owns this file |
| `phases.md` | Generated once, treated as read-only |
| `proposal.md`, `design.md` | OpenSpec specification files |

---

## 🔄 Phase Templates Detail

### Full-Stack (19 phases)

**Use case:** Frontend + Backend + Database

**Phases:**
1. Frontend Mockup (uxui-frontend, 90 min)
2. Accessibility Test (test-debug, 10 min)
3. Manual UX Test (user, 15 min)
4. Business Logic Validation (integration, 10 min)
5. User Approval (user, 5 min)
6. API Design (integration, 30 min)
7. Backend (backend, 120 min)
8. Database (database, 30 min) - parallel with #7
9. Backend Tests (test-debug, 30 min)
10. Contract Backend (integration, 10 min)
11. Frontend Integration (frontend, 60 min)
12. Contract Frontend (integration, 10 min)
13. Component Tests (test-debug, 20 min)
14. Responsive Test (user, 15 min)
15. E2E Tests (test-debug, 45 min)
16. Manual Flow Test (user, 30 min)
17. Refactor (test-debug, 20 min)
18. Documentation (integration, 15 min)
19. Final Report (integration, 10 min)

**Total: ~7 hours**

---

### Frontend-Only (11 phases)

**Use case:** UI components only, no backend

**Phases:**
1. Frontend Mockup (uxui-frontend, 90 min)
2. Accessibility Test (test-debug, 10 min)
3. Manual UX Test (user, 15 min)
4. Business Logic Validation (integration, 10 min)
5. User Approval (user, 5 min)
6. Component Tests (test-debug, 20 min)
7. Responsive Test (user, 15 min)
8. Refactor (test-debug, 20 min)
9. Test Coverage (test-debug, 5 min)
10. Documentation (integration, 15 min)
11. Final Report (integration, 10 min)

**Total: ~3.25 hours**

---

### Backend-Only (10 phases)

**Use case:** API endpoints only, no UI

**Phases:**
1. API Design (integration, 30 min)
2. Backend (backend, 120 min)
3. Database (database, 30 min) - parallel with #2
4. Backend Tests (test-debug, 30 min)
5. Contract Validation (integration, 10 min)
6. E2E API Tests (test-debug, 30 min)
7. Refactor (backend, 20 min)
8. Test Coverage (test-debug, 5 min)
9. Documentation (integration, 15 min)
10. Final Report (integration, 10 min)

**Total: ~5 hours**

---

### Script-Only (7 phases)

**Use case:** CLI tools, data migration scripts

**Phases:**
1. Script Implementation (backend, 60 min)
2. Automated Tests (test-debug, 20 min)
3. Manual Testing (user, 15 min)
4. Refactor (backend, 15 min)
5. Test Coverage (test-debug, 5 min)
6. Documentation (integration, 10 min)
7. Final Report (integration, 5 min)

**Total: ~2.2 hours**

---

### Bug-Fix (5 phases)

**Use case:** Fix existing bugs

**Phases:**
1. Fix Implementation (varies by bug location, 30 min)
2. Unit Tests (test-debug, 15 min)
3. Manual Verification (user, 10 min)
4. Regression Tests (test-debug, 15 min)
5. Final Report (integration, 5 min)

**Total: ~1.25 hours**

---

### Refactor (4 phases)

**Use case:** Code improvements, extract components

**Phases:**
1. Refactor Implementation (test-debug, 45 min)
2. Unit Tests (test-debug, 20 min)
3. Documentation (integration, 10 min)
4. Final Report (integration, 5 min)

**Total: ~1.3 hours**

---

## 📊 Template Selection Logic

**Detection keywords in `tasks.md`:**

```typescript
const keywords = {
  frontend: ["component", "page", "ui", "responsive", "form", "button", ...],
  backend: ["api", "endpoint", "route", "server", "controller", ...],
  database: ["database", "schema", "migration", "model", "table", ...],
  script: ["script", "cli", "command", "tool", "migrate", ...],
  bug_fix: ["fix", "bug", "issue", "error", "crash", ...],
  refactor: ["refactor", "extract", "improve", "optimize", ...]
}

// Selection logic
if (isBugFix) template = 'bug-fix'
else if (isRefactor) template = 'refactor'
else if (hasScript && !hasFrontend && !hasBackend) template = 'script-only'
else if (hasFrontend && hasBackend) template = 'full-stack'
else if (hasFrontend && !hasBackend) template = 'frontend-only'
else if (hasBackend && !hasFrontend) template = 'backend-only'
else template = 'full-stack' // Safe default
```

---

## 🎯 Best Practices

### 1. Run `/csetup` First
- Auto-detects tech stack and generates best practices
- Analyzes tasks and generates workflow
- Required for agent discovery

### 2. Use `/cdev` for Execution
- Orchestrates agent workflow
- Updates progress automatically
- Handles user actions

### 3. Check Progress with `/cview` or `/cstatus`
- `/cview` for detailed breakdown
- `/cstatus` for quick glance
- Real-time updates from `flags.json`

### 4. Agents Update `flags.json` After Each Phase
- Marks phase as completed
- Records actual time spent
- Lists files created
- Adds summary notes

---

## 🔍 Troubleshooting

**Problem:** `/cdev` says "Change not set up"
**Solution:** Run `/csetup {change-id}` first

**Problem:** Agent doesn't load project context
**Solution:** Run `/csetup` to create domain/ structure (auto-detects tech stack)

**Problem:** Progress tracking not working
**Solution:** Check if `flags.json` exists and is valid JSON

**Problem:** Agent skips change context
**Solution:** Verify `openspec/changes/{change-id}/.claude/` exists

---

## 📚 Related Files

- Templates: `.claude/templates/`
- Commands: `.claude/commands/csetup.md`, `/cdev.md`, `/cview.md`, `/cstatus.md`
- Agents: `.claude/agents/01-06-*.md`
- Patterns: `.claude/contexts/patterns/`

---

**💡 Remember:** This workflow integrates OpenSpec with multi-agent orchestration for systematic, trackable, change-based development!
