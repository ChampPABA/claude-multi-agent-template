# Task Classification for Agent Selection

> **Purpose:** Help Main Claude select the right specialist agent for any given task.
>
> **How to use:** Read **Part 1 (Quick Reference)** first. If uncertain, consult **Part 2 (Detailed Scenarios)**.

---

## Part 1: Quick Reference (Read This First!)

### 🎯 Agent Selection Matrix

| Task Type | Keywords to Look For | Agent | Phase | Example |
|-----------|---------------------|-------|-------|---------|
| **UI Design** | component, layout, form, page, design, mock, prototype | **uxui-frontend** | 1 | "Create login form" |
| **API Integration** | connect, fetch, integrate, replace mock, state management | **frontend** | 3 | "Connect form to backend" |
| **API Endpoint** | POST, GET, PUT, DELETE, endpoint, route, validation | **backend** | 2 | "Create /api/login" |
| **Database** | schema, model, migration, table, query, relationship | **database** | 2 | "Add User table" |
| **Testing/Bugs** | test, fix, debug, error, failing | **test-debug** | 1,3,4 | "Fix test errors" |
| **Contract Check** | validate contracts, verify API, integration report | **integration** | 2.5 | "Check API contracts" |

---

### 🔄 Common Workflows

#### **Full-Stack Feature (Login System)**
```
Phase 1: uxui-frontend      → Create login form UI (mock data)
Phase 2a: backend           → Create POST /api/login endpoint
Phase 2b: database          → Create User model + migration
         (2a and 2b run in parallel)
Phase 2.5: integration      → Verify frontend expects what backend returns
Phase 3: frontend           → Connect form to real API (replace mock)
Phase 4: test-debug         → Run integration tests, fix bugs
```

#### **UI-Only Feature (Landing Page)**
```
Phase 1: uxui-frontend      → Create all sections (hero, features, etc.)
Phase 2: test-debug         → Test responsive design, accessibility
```

#### **API-Only Feature (Analytics Endpoint)**
```
Phase 1: backend            → Create GET /api/analytics endpoint
Phase 2: database           → Create complex query (if needed)
Phase 3: test-debug         → Test endpoint with various inputs
```

---

### 🚦 Decision Tree (Ultra-Strict Boundaries)

**Ask yourself:**

1. **"Is this ONLY about UI/UX appearance?"**
   - ✅ YES → **uxui-frontend** agent
   - ❌ NO → Go to Q2

2. **"Does this involve connecting UI to a backend?"**
   - ✅ YES → **frontend** agent
   - ❌ NO → Go to Q3

3. **"Does this involve creating API endpoints or business logic?"**
   - ✅ YES → **backend** agent
   - ❌ NO → Go to Q4

4. **"Does this involve database schema or complex queries?"**
   - ✅ YES → **database** agent
   - ❌ NO → Go to Q5

5. **"Is this about testing or fixing bugs?"**
   - ✅ YES → **test-debug** agent
   - ❌ NO → Go to Q6

6. **"Is this about validating API contracts?"**
   - ✅ YES → **integration** agent
   - ❌ NO → Ask user to clarify the task

---

## Part 2: Detailed Scenarios (Consult When Uncertain)

### Scenario 1: "Build a login page"

**Analysis:**
- Keywords: "login **page**" (UI focus)
- No mention of backend/API

**Agent:** uxui-frontend

**Reasoning:**
- User wants the UI/UX only
- Should use mock data for now
- Don't connect to real API yet

**Output:**
- Login form component
- Mock credentials for testing
- TODO comment: "Connect to /api/login (backend agent)"

---

### Scenario 2: "Implement authentication"

**Analysis:**
- Keywords: "implement" (full feature)
- "authentication" (backend + frontend + database)

**Ambiguous!** → Ask user to clarify:

**Ask user:**
> "Do you want:
>
> A) Just the login UI with mock data? → uxui-frontend
>
> B) The backend API endpoint? → backend + database
>
> C) Full authentication (all phases)? → uxui → backend → database → frontend → test"

**If user says "full authentication":**
```
Phase 1: uxui-frontend  → Login form UI (mock)
Phase 2: backend        → POST /api/login endpoint
Phase 2: database       → User model + sessions table (parallel)
Phase 2.5: integration  → Verify contracts
Phase 3: frontend       → Connect UI to API
Phase 4: test-debug     → Integration tests
```

---

### Scenario 3: "Connect the login form to the backend"

**Analysis:**
- Keywords: "**connect**" (integration)
- Implies UI already exists
- Implies backend already exists

**Agent:** frontend

**Prerequisites check:**
1. ✅ UI exists? (from uxui-frontend)
2. ✅ Backend exists? (from backend)
3. ❌ If either missing → create them first

**Output:**
- Remove mock data from UI
- Add real API calls (fetch/axios)
- Add error handling
- Add loading states

---

### Scenario 4: "Create POST /api/users endpoint"

**Analysis:**
- Keywords: "POST" + "/api/" (backend)
- "endpoint" (backend)

**Agent:** backend

**Reasoning:**
- Pure API work
- No UI involved
- No complex database queries (simple CRUD)

**Output:**
- API route handler
- Request validation (Pydantic/Zod)
- Response format
- Basic database query (e.g., `db.create(User)`)

---

### Scenario 5: "Add User and Post models with relationship"

**Analysis:**
- Keywords: "models" + "relationship" (database)

**Agent:** database

**Reasoning:**
- Schema design
- Relationships (1:N, M:N)
- Migrations

**Output:**
- User model (schema)
- Post model (schema)
- Relationship (User → Posts 1:N)
- Migration file

---

### Scenario 6: "Fix the failing login test"

**Analysis:**
- Keywords: "**fix**" + "**failing**" + "**test**"

**Agent:** test-debug

**Reasoning:**
- Bug fixing
- Test-related

**Workflow:**
1. Run test
2. Analyze error
3. Fix code (max 3-4 iterations)
4. If still failing → escalate to Main Claude

---

### Scenario 7: "Optimize the user query performance"

**Analysis:**
- Keywords: "**optimize**" + "**query**" (database)
- No UI/API changes

**Agent:** database

**Reasoning:**
- Query optimization
- Indexes, eager loading
- Database-layer work

**Output:**
- Add indexes
- Refactor query (prevent N+1)
- Benchmark results

---

### Scenario 8: "Add loading spinner to button"

**Analysis:**
- Keywords: "loading spinner" (UI)
- "button" (component)

**Agent:** uxui-frontend

**Reasoning:**
- Visual/UX change only
- No API logic change

**Output:**
- Update button component
- Add spinner animation
- Add `isLoading` prop

---

### Scenario 9: "Validate email format on the server"

**Analysis:**
- Keywords: "**validate**" + "**server**" (backend)

**Agent:** backend

**Reasoning:**
- Server-side validation
- Business logic
- Not UI validation (client-side)

**Output:**
- Add Pydantic/Zod email validation
- Return 422 if invalid
- Error message

---

### Scenario 10: "Make the dashboard responsive on mobile"

**Analysis:**
- Keywords: "**responsive**" + "**mobile**" (UI)
- No API/backend changes

**Agent:** uxui-frontend

**Reasoning:**
- Layout/styling work
- CSS/responsive design

**Output:**
- Update component styles
- Add mobile breakpoints
- Test on 320px, 768px, 1024px

---

## Part 3: Edge Cases (Consult for Tricky Scenarios)

### Edge Case 1: "Add caching to API responses"

**Question:** frontend or backend?

**Answer:** **backend** agent

**Reasoning:**
- Caching logic lives on server (Redis, in-memory)
- Frontend just receives cached responses

---

### Edge Case 2: "Add optimistic UI updates"

**Question:** frontend or uxui-frontend?

**Answer:** **frontend** agent

**Reasoning:**
- Requires API integration logic
- State management (update before API response)
- Not pure UI work

---

### Edge Case 3: "Create API documentation"

**Question:** Which agent?

**Answer:** **backend** agent (if OpenAPI/Swagger) OR **manual task** (if writing docs)

**Reasoning:**
- Backend agent can generate OpenAPI spec
- But writing long-form docs → outside agent scope

---

### Edge Case 4: "Migrate from mock data to real API"

**Question:** frontend or uxui-frontend?

**Answer:** **frontend** agent

**Reasoning:**
- uxui-frontend creates UI with mock
- frontend replaces mock with real API

---

### Edge Case 5: "Add rate limiting to API"

**Question:** backend or database?

**Answer:** **backend** agent

**Reasoning:**
- Middleware logic (backend layer)
- May use Redis (external service)
- Not database schema work

---

## Part 4: Multi-Agent Tasks (How to Break Down)

### Example: "Build a blog system"

**Step 1: Break down into sub-tasks**
```markdown
1. UI Components (uxui-frontend)
   - Blog post list page
   - Single post detail page
   - Create post form

2. Backend API (backend)
   - GET /api/posts (list)
   - GET /api/posts/:id (detail)
   - POST /api/posts (create)

3. Database (database)
   - Post model (id, title, content, authorId, createdAt)
   - User → Posts relationship (1:N)
   - Indexes (authorId, createdAt)

4. Integration (integration)
   - Verify contracts for all 3 endpoints

5. Connect UI to API (frontend)
   - List page: fetch from GET /api/posts
   - Detail page: fetch from GET /api/posts/:id
   - Form: POST to /api/posts

6. Testing (test-debug)
   - Unit tests (components, API)
   - Integration tests (full flow)
```

**Step 2: Determine execution order**
```
Phase 1 (Sequential):
  1.1 uxui-frontend → Create UI (all pages)

Phase 2 (Parallel):
  2.1 backend → Create API endpoints
  2.2 database → Create Post model + migration

Phase 2.5 (Sequential):
  2.5 integration → Verify contracts

Phase 3 (Sequential):
  3.1 frontend → Connect UI to API

Phase 4 (Sequential):
  4.1 test-debug → Run tests, fix bugs
```

---

## Part 5: Ultra-Strict Boundaries (Reference)

### What Each Agent CAN and CANNOT Do

#### uxui-frontend (Blue)
**CAN:**
- ✅ Create React/Vue/Svelte components
- ✅ Design layouts (CSS, Tailwind)
- ✅ Add client-side validation UI (show error messages)
- ✅ Use mock data (setTimeout, hardcoded values)
- ✅ Add loading states (visual only)

**CANNOT:**
- ❌ Call real APIs (even fetch)
- ❌ Add state management (Zustand, Redux)
- ❌ Write Server Actions
- ❌ Connect to backend

---

#### frontend (Green)
**CAN:**
- ✅ Replace mock data with real API calls
- ✅ Add state management (Zustand, Redux, Context)
- ✅ Error handling (client-side)
- ✅ Write Server Actions (Next.js)
- ✅ Data fetching (TanStack Query, SWR)

**CANNOT:**
- ❌ Design UI components (no styling work)
- ❌ Create API endpoints
- ❌ Write database queries

---

#### backend (Purple)
**CAN:**
- ✅ Create API endpoints (routes, handlers)
- ✅ Request validation (Pydantic, Zod)
- ✅ Business logic (calculations, rules)
- ✅ Simple database queries (findOne, findMany, create, update)
- ✅ Authentication logic (JWT, bcrypt)

**CANNOT:**
- ❌ Design database schema → database agent
- ❌ Complex queries (JOINs, subqueries) → database agent
- ❌ Write migrations → database agent
- ❌ UI work

---

#### database (Pink)
**CAN:**
- ✅ Design schemas (models, tables)
- ✅ Write migrations
- ✅ Complex queries (JOINs, aggregations, subqueries)
- ✅ Add indexes, optimize queries
- ✅ Define relationships (1:N, M:N)

**CANNOT:**
- ❌ Create API endpoints → backend agent
- ❌ Business logic → backend agent
- ❌ UI work

---

#### test-debug (Red)
**CAN:**
- ✅ Run tests (unit, integration, e2e)
- ✅ Fix bugs (max 3-4 iterations)
- ✅ Add new tests
- ✅ Debug errors

**CANNOT:**
- ❌ Design features → other agents
- ❌ Write implementation from scratch (only fix bugs)

---

#### integration (Orange)
**CAN:**
- ✅ Read frontend API calls
- ✅ Read backend responses
- ✅ Compare contracts
- ✅ Report mismatches
- ✅ Recommend fixes

**CANNOT:**
- ❌ Fix code (only report)
- ❌ Run tests → test-debug
- ❌ Orchestrate workflows

---

## Summary: When in Doubt

1. **Read Part 1 (Quick Reference)** - covers 80% of cases
2. **Still uncertain?** → Check Part 2 (Detailed Scenarios) for similar examples
3. **Very tricky?** → Check Part 3 (Edge Cases)
4. **Multi-step task?** → Check Part 4 (Break down example)
5. **Still confused?** → **Ask the user to clarify!**

**Golden Rule:** When ambiguous, prefer **ultra-strict interpretation**:
- "login" alone → uxui-frontend (assume UI unless stated otherwise)
- If user wants more → they will clarify

**Remember:** It's better to under-deliver and ask for clarification than to over-deliver and create scope creep.

---

## Optional: TDD Classification

For TDD-specific task classification, see `@/.claude/contexts/patterns/tdd-classification.md`.
