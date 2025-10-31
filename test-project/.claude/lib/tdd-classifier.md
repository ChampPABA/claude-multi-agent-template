# TDD Classification Logic

> **Automatically determines which phases require TDD workflow**

---

## 🎯 Purpose

Provides logic to classify tasks and determine whether they require TDD (Test-Driven Development) workflow. Ensures consistent TDD decisions across all changes.

**Result Format:**
```
TDD Decision:
  required: true/false
  reason: "Why TDD is/isn't required"
  workflow: "red-green-refactor" | "test-alongside" | "none"
  confidence: "high" | "medium" | "low"
```

---

## 🔍 Classification Rules

### Rule 1: Backend API Endpoints

**Always TDD:**
- Authentication logic (login, register, password, JWT)
- Authorization logic (permissions, roles, access)
- Payment processing (Stripe, charges, refunds)
- Financial calculations
- Data validation with business rules
- External API integrations (SendGrid, webhooks)

**Test-Alongside OK:**
- Simple CRUD operations (basic findOne, findMany, create, update, delete)
- Read-only endpoints with no business logic
- Health check endpoints

### Rule 2: Frontend UI

**TDD Required:**
- Multi-step forms with complex validation
- State machines (wizards, checkout flows, onboarding)
- Complex client-side calculations

**Test-Alongside OK:**
- Presentational components
- Simple forms
- Static pages

### Rule 3: Database

**Never TDD:**
- Schema design
- Migration files
- Database setup scripts

**Reason:** Schemas are declarative, not imperative logic

### Rule 4: Integration

**Never TDD:**
- Contract validation (validation itself, not implementation)
- Report generation
- Documentation

### Rule 5: Test-Debug

**Never TDD:**
- Test-debug agent writes tests - no TDD needed

---

## 🤖 Classification Logic

**Main Claude should follow this logic in `/csetup` when generating phases.md:**

### Step 1: Determine Phase Type

Identify agent type from phase:
- backend, api, endpoint → Backend rules
- frontend, ui, uxui-frontend → Frontend rules
- database, schema, migration → Database rules
- integration, contract, validation → Integration rules
- test, test-debug → Test rules

### Step 2: Check Critical Keywords (Backend Only)

**Critical keywords** (always TDD):
- auth, login, register, password, token, jwt
- payment, stripe, charge, refund, transaction
- permission, role, access, authorization
- email, notification, sendgrid, sms
- webhook, callback, integration
- calculation, formula, compute
- validation, business rule, constraint

**If found:**
- TDD Required: YES
- Reason: "Critical backend logic requires TDD for correctness"
- Workflow: red-green-refactor
- Confidence: high

### Step 3: Check CRUD Pattern (Backend Only)

**CRUD keywords:**
- list, get, fetch, read, retrieve, view

**If simple CRUD:**
- TDD Required: NO
- Reason: "Simple CRUD read operation - test-alongside OK"
- Workflow: test-alongside
- Confidence: high

### Step 4: Check Complexity

**Backend:**
- Complex → TDD required (red-green-refactor, medium confidence)
- Medium/Simple → test-alongside OK

**Frontend:**
- Check for complex UI keywords:
  - multi-step, wizard, stepper
  - state machine, workflow
  - validation, form validation
  - calculation, formula
  - checkout, payment form, onboarding
- If found → TDD required (red-green-refactor, high confidence)
- Otherwise → test-alongside OK

**Database/Integration/Test:**
- Always NO TDD (workflow: none, high confidence)

---

## 🔧 Complexity Estimation

**How to estimate complexity:**

1. **Time-based scoring:**
   - < 30 minutes → +0 points
   - 30-90 minutes → +1 point
   - > 90 minutes → +2 points

2. **Keyword-based scoring:**
   - Contains: multiple, complex, advanced, sophisticated → +1 point
   - Contains: integration, calculation, validation → +1 point
   - Contains: business logic, algorithm, optimization → +1 point

3. **Length-based scoring:**
   - Description > 500 chars → +1 point
   - Description > 10 lines → +1 point
   - Keywords > 5 → +1 point

4. **Classification:**
   - Score ≤ 2 → simple
   - Score 3-5 → medium
   - Score > 5 → complex

---

## 📊 Usage in /csetup

**When generating phases.md:**

For each phase:
1. Extract task description from tasks.md
2. Extract keywords from description
3. Estimate complexity (time + keywords + length)
4. Classify TDD (phase type + keywords + complexity)
5. Add TDD metadata to phases.md

**Phase metadata includes:**
```markdown
| TDD | YES/NO |
| TDD Reason | {reason} |
| TDD Workflow | red-green-refactor / test-alongside / none |
| Complexity | simple / medium / complex |
```

---

## 📝 Phase Metadata Format

**Example output in phases.md:**

```markdown
## Phase 7: Backend Implementation

| Metadata | Value |
|----------|-------|
| Phase | Backend Implementation |
| Agent | backend |
| TDD | YES |
| TDD Reason | Critical backend logic requires TDD for correctness |
| TDD Workflow | red-green-refactor |
| Complexity | complex |
| Estimated | 120 minutes |

**TDD Required:** ✅ This phase MUST follow RED-GREEN-REFACTOR workflow.

**Why TDD:**
Critical backend logic requires TDD for correctness.
Detected keywords: auth, login, jwt, validation

**Workflow:**
1. 🔴 RED: Write tests FIRST (they should fail)
2. ✅ GREEN: Write minimal implementation to pass tests
3. 🔧 REFACTOR: Improve code quality while keeping tests green
```

---

## 🎯 Example Classifications

### Example 1: Authentication Endpoint

**Input:**
- Phase: backend
- Task: "Implement POST /api/auth/login with JWT token generation"
- Complexity: complex
- Keywords: auth, login, jwt, password, validation

**Output:**
- TDD Required: YES
- Reason: "Critical backend logic requires TDD for correctness"
- Workflow: red-green-refactor
- Confidence: high

### Example 2: Simple List Endpoint

**Input:**
- Phase: backend
- Task: "Implement GET /api/posts to list all posts"
- Complexity: simple
- Keywords: get, list, read

**Output:**
- TDD Required: NO
- Reason: "Simple CRUD read operation - test-alongside OK"
- Workflow: test-alongside
- Confidence: high

### Example 3: Multi-Step Form

**Input:**
- Phase: uxui-frontend
- Task: "Create multi-step checkout wizard with validation"
- Complexity: complex
- Keywords: multi-step, wizard, checkout, validation

**Output:**
- TDD Required: YES
- Reason: "Complex UI state machine requires TDD"
- Workflow: red-green-refactor
- Confidence: high

### Example 4: Simple UI Component

**Input:**
- Phase: uxui-frontend
- Task: "Create a product card component"
- Complexity: simple
- Keywords: card, component, display

**Output:**
- TDD Required: NO
- Reason: "Presentational component - test-alongside OK"
- Workflow: test-alongside
- Confidence: high

### Example 5: Database Schema

**Input:**
- Phase: database
- Task: "Create User table with email, password fields"
- Complexity: simple
- Keywords: schema, table, migration

**Output:**
- TDD Required: NO
- Reason: "Schema design is declarative - no TDD needed"
- Workflow: none
- Confidence: high

---

## 🔄 Integration Points

### 1. In /csetup Command

**Step 5: Generate phases.md with TDD metadata**

For each phase in template:
1. Get phase info (agent, estimated time)
2. Extract task description from tasks.md
3. Extract keywords from description
4. Estimate complexity using scoring system
5. Classify TDD using rules above
6. Write phase with TDD metadata to phases.md

### 2. In /cdev Command

**Step 3: Build agent prompt with TDD requirement**

Read current phase from phases.md:
- If `TDD | YES` found in phase metadata:
  - Add TDD requirement to agent prompt:
    ```
    ⚠️ TDD REQUIRED FOR THIS PHASE

    Workflow: {tdd_workflow}
    Reason: {tdd_reason}

    You MUST follow RED-GREEN-REFACTOR:
    1. Write tests FIRST (they should fail)
    2. Write minimal implementation
    3. Refactor while keeping tests green

    Your first response MUST show RED phase (failing tests).
    ```

### 3. In Validation

**Check TDD compliance in pre-work validation**

If phase has `TDD | YES`:
- Required items:
  - "TDD Workflow"
  - "RED-GREEN-REFACTOR"
  - "RED Phase: Tests written and failing" (for backend)

---

## 🎯 Benefits

✅ **Consistent TDD decisions** - No guessing, automated
✅ **Clear guidance for agents** - TDD metadata in phases.md
✅ **Enforced by validation** - Agents can't skip TDD when required
✅ **Flexible** - Test-alongside still allowed for simple tasks
✅ **Auditable** - TDD reason documented in phases.md

---

**This classification ensures TDD is used WHERE it matters, not EVERYWHERE!** 🎯
