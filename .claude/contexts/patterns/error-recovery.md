# Error Recovery Pattern

> **Purpose:** Guide agents on how to handle errors, retry intelligently, and escalate when stuck.

---

## 🎯 Core Principle

**Don't get stuck. Retry smart, escalate fast.**

Agents should:
1. ✅ Try to fix errors automatically (up to 3 attempts)
2. ✅ Escalate to Main Claude when blocked
3. ✅ Provide clear context for escalation

---

## 🔍 Step 1: Identify Error Type

When an agent encounters an error, first classify it:

### ✅ Fixable Errors (Retry)
Errors that agent can fix automatically:
- **Missing import/dependency** → Add import, install package
- **Typo in code** → Fix typo
- **Validation error** → Add validation
- **Wrong HTTP method** → Fix method
- **Missing field** → Add field
- **Type mismatch** → Fix type

**Action:** Retry with fix (up to 3 attempts)

---

### Blocking Errors (Escalate Immediately)
Errors that agent cannot fix alone:
- **Missing environment variable** (e.g., DATABASE_URL not set)
- **Service not running** (e.g., PostgreSQL not running)
- **Missing file/resource** (e.g., API spec doesn't exist)
- **Insufficient permissions** (e.g., can't write to directory)
- **Infrastructure issue** (e.g., network timeout)
- **Ambiguous requirements** (e.g., "should we use JWT or sessions?")

**Action:** Escalate immediately (don't waste time retrying)

---

### 🤔 Unclear Errors (Try Once, Then Escalate)
Errors where root cause is unclear:
- **Stack trace without clear message**
- **Unexpected behavior** (works locally, fails in test)
- **Third-party service error**
- **Complex dependency conflict**

**Action:**
1. Try obvious fix once
2. If still fails → Escalate with details

---

## 🔄 Step 2: Retry Logic

### For Fixable Errors:

```markdown
Attempt 1: Fix Obvious Issue
- Read error message carefully
- Apply most obvious fix
- Run test/command again

Attempt 2: Re-read Documentation
- Search Context7 for relevant docs
- Check if using correct pattern
- Apply fix based on docs
- Run test/command again

Attempt 3: Different Approach
- Try alternative solution
- Example: If fetch fails, try different HTTP library
- Example: If query slow, try different query structure
- Run test/command again

After 3 Attempts: STOP and Escalate
- Don't waste more time
- Escalate to Main Claude with full context
```

### Example (Backend Agent):

```
Error: "Cannot find module 'fastapi'"

Attempt 1: Install missing package
→ Run: uv pip install fastapi
→ Test: Import works ✅ FIXED!

Error: "Validation error: email field required"

Attempt 1: Add email field to Pydantic model
→ Test: Still fails ❌

Attempt 2: Check Context7 docs for Pydantic validation
→ Fix: Email should be EmailStr, not str
→ Test: Works ✅ FIXED!

Error: "Database connection refused"

→ This is BLOCKING ERROR (database not running)
→ Escalate immediately (don't retry)
```

---

## 📤 Step 3: Escalation Format

When escalating to Main Claude, provide this information:

### Template:

```markdown
⚠️ **Escalation Required**

**Agent:** {agent-name}
**Task:** {task-description}
**Attempts:** {number-of-attempts}
**Error Type:** {fixable/blocking/unclear}

**Error Message:**
```
{full-error-message}
{stack-trace-if-available}
```

**What I Tried:**
1. {attempt-1-description} → {result}
2. {attempt-2-description} → {result}
3. {attempt-3-description} → {result}

**Current State:**
- Files modified: {list-of-files}
- Tests passing: {yes/no}
- Code compiling: {yes/no}

**Need Help With:**
- {specific-question-1}
- {specific-question-2}
- {specific-question-3}

**Suggested Next Steps:**
- {suggestion-1}
- {suggestion-2}
```

### Example Escalation:

```markdown
⚠️ **Escalation Required**

**Agent:** backend
**Task:** Create POST /api/auth/login endpoint
**Attempts:** 3
**Error Type:** Unclear

**Error Message:**
```
AssertionError: assert 200 == 401
  Expected status code 200, got 401
  Test: test_login_success
```

**What I Tried:**
1. Checked credentials in test → Correct (test@example.com / password123)
2. Added debug logging to endpoint → Shows user found in database
3. Checked password hashing → bcrypt.verify() returns True

**Current State:**
- Files modified: app/api/auth.py, tests/test_auth.py
- Tests passing: 2/3 (test_login_success fails)
- Code compiling: Yes

**Need Help With:**
- Why does endpoint return 401 even when credentials are correct?
- Is there middleware blocking the request?
- Should I check JWT token generation logic?

**Suggested Next Steps:**
- Review middleware configuration
- Check if CORS is blocking response
- Verify JWT secret is set in environment
```

---

## 📊 Error Recovery Decision Tree

```
┌─────────────────┐
│  Error Occurs   │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  Is this a BLOCKING ERROR?          │
│  (env var, service down, etc.)      │
└─┬───────────────────────────────┬───┘
  │ YES                           │ NO
  ▼                               ▼
┌──────────────────┐    ┌──────────────────┐
│  Escalate        │    │  Is error clear? │
│  Immediately     │    └─┬────────────┬───┘
└──────────────────┘      │ YES        │ NO
                          ▼            ▼
                 ┌──────────────┐  ┌──────────────┐
                 │ Fixable?     │  │ Try once     │
                 └─┬──────────┬─┘  └──────┬───────┘
                   │ YES      │ NO        │
                   ▼          ▼           ▼
              ┌─────────┐  ┌──────┐  ┌──────┐
              │ Retry   │  │Escal.│  │Escal.│
              │ (max 3) │  └──────┘  └──────┘
              └─┬───────┘
                │
                ▼
         ┌──────────────┐
         │ Fixed after  │
         │ 3 attempts?  │
         └─┬──────────┬─┘
           │ YES      │ NO
           ▼          ▼
       ┌────────┐  ┌──────────┐
       │Continue│  │ Escalate │
       └────────┘  └──────────┘
```

---

## 🎯 Agent-Specific Guidelines

### Backend Agent
**Common Fixable Errors:**
- Missing imports → Add import
- Validation errors → Fix Pydantic/Zod schema
- Type errors → Fix type annotations

**Common Blocking Errors:**
- Database not running → Escalate
- Missing DATABASE_URL → Escalate
- Port already in use → Escalate (or suggest: kill process)

---

### Database Agent
**Common Fixable Errors:**
- Migration syntax error → Fix SQL/Prisma syntax
- Missing index → Add index
- Wrong data type → Fix type

**Common Blocking Errors:**
- Cannot connect to database → Escalate
- Destructive migration without confirmation → Escalate (ask user)
- Migration conflict (already applied) → Escalate

---

### Test-Debug Agent
**Common Fixable Errors:**
- Test assertion fails → Fix code to pass test
- Mock data incorrect → Fix mock
- Import error → Add import

**Common Blocking Errors:**
- Test framework not installed → Escalate (install needed)
- Test requires external service → Escalate (mock or skip)
- Test flaky (random pass/fail) → Escalate after 2 attempts

---

### Frontend Agent
**Common Fixable Errors:**
- API fetch fails → Fix API URL
- State update error → Fix state logic
- Type error → Fix TypeScript types

**Common Blocking Errors:**
- Backend API not running → Escalate
- CORS error → Escalate (backend config needed)
- Environment variable missing → Escalate

---

### UX-UI Frontend Agent
**Common Fixable Errors:**
- CSS syntax error → Fix syntax
- Component prop error → Fix props
- Missing dependency → Install package

**Common Blocking Errors:**
- Design spec unclear → Escalate (ask for clarification)
- Asset missing (logo, image) → Escalate (request asset)
- Conflicting design requirements → Escalate

---

### Integration Agent
**Common Fixable Errors:**
- Type mismatch in contract → Document mismatch
- Missing field → Document missing field

**Common Blocking Errors:**
- Frontend or Backend doesn't exist → Escalate (cannot validate)
- API spec file missing → Escalate (request spec)

---

## 📋 Logging Error Recovery

**Always log each attempt:**

```json
{
  "event": "error_recovery_attempt",
  "agent": "backend",
  "task": "Create POST /api/login",
  "attempt": 1,
  "error_type": "fixable",
  "error_message": "Missing import: FastAPI",
  "fix_applied": "Added: from fastapi import FastAPI",
  "result": "success"
}
```

```json
{
  "event": "error_recovery_escalation",
  "agent": "backend",
  "task": "Create POST /api/login",
  "attempts": 3,
  "error_type": "unclear",
  "error_message": "Test fails with 401 despite correct credentials",
  "escalation_reason": "Root cause unclear after 3 attempts",
  "context_provided": true
}
```

---

## ✅ Summary

### DO:
- ✅ Classify error first (fixable/blocking/unclear)
- ✅ Retry up to 3 times for fixable errors
- ✅ Escalate immediately for blocking errors
- ✅ Provide full context when escalating
- ✅ Log all attempts and results

### DON'T:
- ❌ Don't retry forever (max 3 attempts)
- ❌ Don't retry blocking errors (waste of time)
- ❌ Don't escalate without context (unhelpful)
- ❌ Don't guess randomly (read docs first)
- ❌ Don't skip logging (observability critical)

---

**Remember:** Getting unstuck fast is more valuable than fixing everything yourself. Escalate when needed!
