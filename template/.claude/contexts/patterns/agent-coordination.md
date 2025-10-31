# Agent Coordination Pattern

> **Purpose:** Guide Main Claude on when to run agents sequentially, in parallel, or conditionally.

---

## 🎯 Core Principle

**Maximize parallelism, minimize waiting.**

- ✅ Run agents in **parallel** when they don't depend on each other
- ✅ Run agents **sequentially** when one depends on another's output
- ✅ Run agents **conditionally** when only needed in specific scenarios

---

## 📊 Execution Strategies

### 🔵 Sequential Execution
**Run agents one after another**

**When to use:**
- Agent B needs output from Agent A
- Agent B modifies what Agent A created
- Order matters for correctness

**Example:**
```
uxui-frontend → frontend
(frontend needs the UI components that uxui-frontend creates)
```

**How to execute:**
```markdown
1. Run uxui-frontend first
2. Wait for completion
3. Then run frontend
```

---

### 🟢 Parallel Execution
**Run agents at the same time**

**When to use:**
- Agents are completely independent
- No shared dependencies
- Can work simultaneously without conflicts

**Example:**
```
backend + database (parallel)
(backend creates API logic, database creates schema - independent)
```

**How to execute:**
```markdown
1. Run backend AND database simultaneously
2. Wait for BOTH to complete
3. Then proceed to next phase
```

**Benefits:**
- ⚡ 2x faster (if 2 agents run parallel)
- 🔄 Better resource utilization

---

### 🟡 Conditional Execution
**Run agent only if condition is met**

**When to use:**
- Agent only needed in specific scenarios
- Optional validation/enhancement
- Feature flags or environment-specific

**Example:**
```
integration (conditional)
Run ONLY IF both frontend AND backend exist
```

**How to execute:**
```markdown
IF (frontend code exists AND backend code exists):
  Run integration agent
ELSE:
  Skip (nothing to validate)
```

---

## 🔄 Common Workflows

### 1. Full-Stack Feature (Login System)

**Task:** "Build a login system with email/password"

**Execution Plan:**

```
Phase 1: UI with Mock Data (Sequential)
├─ uxui-frontend → Create login form UI with mock data
└─ ⏸️  PAUSE for manual approval (optional)

Phase 2: Backend + Database (Parallel)
├─ backend → Create POST /api/login endpoint
└─ database → Create User table + migration
    (Run simultaneously - no dependency)

Phase 2.5: Contract Validation (Conditional)
└─ integration → Verify frontend expects what backend returns
    (Run ONLY IF both exist)

Phase 3: Connect UI to API (Sequential)
└─ frontend → Replace mock data with real API calls
    (Depends on Phase 2 completion)

Phase 4: Testing (Sequential)
└─ test-debug → Run all tests, fix bugs
    (Depends on Phase 3 completion)
```

**Timeline:**
```
Without parallel: ~30 minutes
  uxui (5m) → backend (10m) → database (5m) → integration (2m) → frontend (5m) → test (3m)

With parallel: ~20 minutes
  uxui (5m) → [backend + database parallel] (10m) → integration (2m) → frontend (5m) → test (3m)

Savings: 10 minutes (33% faster)
```

---

### 2. UI-Only Feature (Landing Page)

**Task:** "Create a landing page with hero, features, and CTA sections"

**Execution Plan:**

```
Phase 1: UI Components (Sequential)
└─ uxui-frontend → Create all sections (hero, features, CTA)

Phase 2: Testing (Sequential)
└─ test-debug → Test responsive design, accessibility
    (Depends on Phase 1)
```

**No backend/database needed → Simple workflow**

---

### 3. API-Only Feature (Analytics Endpoint)

**Task:** "Create GET /api/analytics endpoint with aggregations"

**Execution Plan:**

```
Phase 1: Database Query (Sequential)
└─ database → Create complex aggregation query
    (Needs to be tested first)

Phase 2: API Endpoint (Sequential)
└─ backend → Create GET /api/analytics using query
    (Depends on database query)

Phase 3: Testing (Sequential)
└─ test-debug → Test endpoint with various inputs
    (Depends on Phase 2)
```

**No frontend needed → Backend-only workflow**

---

### 4. Refactoring Task (Extract Shared Component)

**Task:** "Extract repeated button styles into shared component"

**Execution Plan:**

```
Phase 1: Refactor (Sequential)
└─ uxui-frontend → Extract ButtonComponent, update all usages

Phase 2: Testing (Sequential)
└─ test-debug → Ensure all buttons still work correctly
    (Depends on Phase 1)
```

**Simple refactor → No multiple agents needed**

---

## 🎯 Decision Matrix

| Scenario | Agents Needed | Execution | Rationale |
|----------|---------------|-----------|-----------|
| **Full-stack CRUD** | uxui → backend + database (parallel) → integration → frontend → test | Mixed | Backend + database independent |
| **UI component only** | uxui → test | Sequential | Simple workflow |
| **API endpoint only** | backend → test (or database → backend → test) | Sequential | Backend may need database |
| **Database schema** | database → test | Sequential | Simple workflow |
| **Complex query** | database → backend → test | Sequential | Backend uses database query |
| **Connect existing UI to API** | integration → frontend → test | Sequential | Validate then connect |
| **Bug fix** | test-debug | Single agent | Focused debugging |

---

## 🚀 Optimization Tips

### 1. **Identify Independent Work**
Before starting, ask:
- "Can backend work without waiting for database?"
- "Can database schema be designed independently?"

If YES → Run in parallel

---

### 2. **Batch Similar Tasks**
Instead of:
```
Create User endpoint → Test → Create Post endpoint → Test
```

Do:
```
Create User + Post endpoints (batch) → Test both together
```

**Benefit:** Fewer context switches

---

### 3. **Use Integration Agent Wisely**
Only run integration agent when:
- ✅ Both frontend AND backend exist
- ✅ API contracts might mismatch
- ❌ Don't run if only UI or only API exists (nothing to validate)

---

### 4. **Defer Testing When Safe**
Instead of:
```
uxui → test → backend → test → frontend → test
```

Do:
```
uxui → backend + database (parallel) → frontend → test (once at end)
```

**Benefit:** Faster iteration (test once instead of 3 times)

**⚠️ Trade-off:** If test fails, harder to debug (but usually worth it)

---

## 📋 Coordination Checklist

**Before starting multi-agent task, ask:**

### 🔍 Analysis Questions
- [ ] What agents are needed? (List all)
- [ ] Which agents depend on others? (Map dependencies)
- [ ] Which agents can run in parallel? (Identify independent work)
- [ ] Are there any conditional agents? (integration, optional features)

### ⚡ Optimization Questions
- [ ] Can I reduce sequential steps by parallelizing?
- [ ] Can I batch similar work to avoid context switching?
- [ ] Can I defer testing to end instead of after each agent?
- [ ] Is there a faster path to MVP?

### 🎯 Execution Plan
- [ ] Write down the phase breakdown
- [ ] Mark parallel agents clearly
- [ ] Identify manual approval points (if any)
- [ ] Estimate time savings from parallelism

---

## 📖 Example: Main Claude Analysis

**User Request:** "Build a blog system with posts and comments"

**Main Claude's Internal Thought Process:**

```markdown
Step 1: What agents are needed?
- uxui-frontend (blog list, post detail, comment form)
- backend (GET /posts, POST /comments, etc.)
- database (Post + Comment models)
- frontend (connect UI to API)
- test-debug (test everything)

Step 2: Dependencies?
- uxui-frontend → independent (uses mock data)
- backend → independent (can create endpoints)
- database → independent (can design schema)
- frontend → depends on uxui + backend + database
- test-debug → depends on everything

Step 3: Can we parallelize?
YES! backend + database can run together (independent)

Step 4: Execution Plan:
Phase 1: uxui-frontend (create UI with mock)
Phase 2: backend + database (parallel - create API + schema)
Phase 2.5: integration (verify contracts)
Phase 3: frontend (connect UI to real API)
Phase 4: test-debug (test all features)

Step 5: Execute:
Run uxui-frontend...
✅ Done

Run backend AND database in parallel...
✅ Both done

Run integration...
✅ Contracts match

Run frontend...
✅ Done

Run test-debug...
✅ All tests pass

Task complete!
```

---

## 🎨 Visual Workflow Examples

### Sequential (Waterfall)
```
[uxui] ──► [backend] ──► [database] ──► [frontend] ──► [test]
  5m        10m           5m             5m            3m
Total: 28 minutes
```

### Parallel (Optimized)
```
[uxui] ──► [backend  ] ──► [frontend] ──► [test]
  5m       [database ]       5m            3m
              10m (parallel)
Total: 23 minutes (18% faster)
```

### Hybrid (Best)
```
[uxui] ──► [backend + database] ──► [integration] ──► [frontend] ──► [test]
  5m           10m (parallel)           2m              5m            3m
Total: 25 minutes (but safer with validation)
```

---

## ✅ Summary

### Key Principles:
1. **Parallel > Sequential** (when safe)
2. **Validate contracts** (use integration agent)
3. **Defer testing** (batch at end when possible)
4. **Map dependencies** (before starting)

### Common Patterns:
- **Full-stack:** uxui → [backend + database] → integration → frontend → test
- **UI-only:** uxui → test
- **API-only:** backend → test (or database → backend → test)
- **Refactor:** specialist agent → test

### When in Doubt:
- **Ask:** "Does Agent B need Agent A's output?"
- **If YES:** Sequential
- **If NO:** Parallel
- **If MAYBE:** Run integration agent to verify

---

**Remember:** The goal is speed AND quality. Parallelize when safe, validate when needed, test thoroughly.
