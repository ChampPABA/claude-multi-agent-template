# TaskMaster-style Analysis (v1.3.0)

> **Detailed guide to intelligent task analysis with 6 dimensions**
> **Source:** Extracted from CLAUDE.md (Navigation Hub)
> **Version:** 1.4.0

---

## 🧠 The Problem: Dumb Task Lists

**Before v1.3.0:**
```
tasks.md (from OpenSpec):
- Create login system
- Build user dashboard
- Add payment integration

/csetup generates phases → Treats all tasks equally
→ No complexity analysis
→ No dependency detection
→ No risk assessment
→ No time buffers
→ Result: Tasks fail, delays, security issues
```

**After v1.3.0:**
```
tasks.md → TaskMaster Analysis → Intelligent phases.md

Analysis includes:
- Complexity scoring (1-10)
- Dependency graph (blocks/blocked by)
- Risk assessment (LOW/MEDIUM/HIGH)
- Research requirements detection
- Subtask breakdown (if needed)
- Priority ranking (CRITICAL → LOW)
- Time buffer calculation
```

---

## The Solution: Intelligent Task Analysis

**Inspired by:** [claude-task-master](https://github.com/eyaltoledano/claude-task-master)

**See:** `@/.claude/lib/task-analyzer.md` for complete analysis logic

---

## 6 Analysis Dimensions

### 1. Complexity Scoring (1-10)

**Factors:**
- Estimated time (> 2 hours = high)
- Security keywords (auth, payment, encryption)
- Multi-step indicators (multiple "and", "then")
- External dependencies (APIs, libraries)

**Levels:**
- 1-3: Simple (CRUD, UI components)
- 4-6: Moderate (Business logic)
- 7-8: Complex (Auth, real-time)
- 9-10: Critical (Security, migrations)

### 2. Dependency Detection

**Automatic detection:**
- UI depends on backend API ✅
- Backend depends on database ✅
- Tests depend on implementation ✅
- Integration depends on both UI + API ✅

**Outputs:**
- Blocks: Tasks this task blocks
- Blocked by: Tasks blocking this task
- Parallelizable: Can run in parallel

### 3. Risk Assessment

**Risk Factors:**
- Complexity score (9-10 = +3 risk)
- Security-critical (+3 risk)
- External dependencies (+1 risk)
- Data migration (+2 risk)

**Mitigation strategies:**
- TDD required (high risk)
- Security checklist
- Time buffer (+50% for HIGH)
- Pair programming

### 4. Research Requirements

**Auto-detects need for research:**
- New technology (React Query v5 → research)
- Best practices (performance optimization)
- Integration (Stripe setup guide)
- Migration (upgrade strategies)

**Generates research queries:**
```
Task: "Migrate to React Query v5"
→ Research Phase 0.1 added (15 min)
  Queries:
  - "React Query v5 migration guide"
  - "Breaking changes from v4 to v5"
```

### 5. Subtask Breakdown

**When to break down:**
- Complexity >= 7
- Multiple verbs (create + update + delete)
- Time > 90 minutes
- Multiple "and" connectors

**Example:**
```
Task: "Create login system"
→ Subtasks:
  1.1: Login form UI (45 min)
  1.2: Form validation (30 min)
  1.3: POST /api/login (30 min)
  1.4: JWT auth (40 min)
  1.5: Integration (20 min)
```

### 6. Priority Ranking (0-100)

**Scoring factors:**
- Business value (login, checkout = +30)
- Blocks other tasks (+10 per task)
- No blockers (+20)
- Risk level (high = +15)
- Complexity (simple = +10 for quick wins)

**Labels:**
- 80-100: CRITICAL
- 60-79: HIGH
- 40-59: MEDIUM
- 0-39: LOW

---

## Generated Output Example

**Before (Simple phases.md):**
```markdown
## Phase 1: Frontend Mockup
Agent: uxui-frontend
Estimated: 90 min
```

**After (TaskMaster-enhanced):**
```markdown
## 📊 Task Analysis Summary

Total tasks: 8 → 15 (subtask expansion)
Average complexity: 5.8/10

Priority Distribution:
- 🔴 CRITICAL: 2 (Login, Payment)
- 🟠 HIGH: 3
- 🟡 MEDIUM: 2
- 🟢 LOW: 1

Risk Assessment:
- 🚨 HIGH: 2 tasks → TDD required
- ⚠️ MEDIUM: 3 tasks
- ✅ LOW: 3 tasks

Time Estimates:
- Original: 6.5 hours
- Adjusted: 9.2 hours (+41% buffer)

---

## Phase 0.1: Research React Query v5 (Research)

Agent: integration
Time: 15 min

Queries:
- React Query v5 migration guide
- Breaking changes from v4 to v5

---

## Phase 1: Login Form UI

Agent: uxui-frontend
Time: 45 min → 60 min (+33% buffer)

**Task Metadata:**
- Complexity: 6/10 (Moderate)
- Priority: CRITICAL (85/100)
- Risk: MEDIUM
  - Mitigation: TDD required
- Dependencies:
  - Blocks: Phase 3 (Integration)
  - Parallelizable: Phase 2 (API)
- Subtasks:
  - 1.1: Email input component
  - 1.2: Password input component
  - 1.3: Submit button with loading state
```

---

## Benefits

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| **Task Analysis** | Basic | Intelligent | 6 dimensions |
| **Complexity** | Ignored | Scored 1-10 | Risk-aware |
| **Dependencies** | Manual | Auto-detected | Faster planning |
| **Time Estimates** | Optimistic | With buffer | More accurate |
| **Research Phases** | Missing | Auto-added | Informed decisions |
| **Subtasks** | None | Auto-expanded | Clearer workflow |
| **Priority** | Random | Scored 0-100 | Right order |

---

## Workflow

```bash
# 1. OpenSpec generates tasks
User: "Build login system"
→ tasks.md

# 2. /csetup analyzes tasks (STEP 3.5 - TaskMaster)
/csetup login-feature

→ Analyzing 3 tasks...
→ Expanded to 8 subtasks
→ 2 research phases added
→ Complexity: 5.8/10 average
→ Time: 3.5h → 5.2h (+48% buffer)

# 3. Enhanced phases.md generated
→ Research phases first
→ Implementation phases with metadata
→ Dependencies mapped
→ Risk mitigation noted

# 4. Execute with /cdev
/cdev login-feature

→ Agents see full context:
  - Complexity warnings
  - Risk mitigation
  - Dependency order
  - Time buffers
```

---

## 🔗 See Also

- `../../commands/csetup.md` - /csetup command (uses TaskMaster)
- `../task-analyzer.md` - Complete analysis logic implementation
- `../tdd-classifier.md` - TDD decision logic (integrated with TaskMaster)
