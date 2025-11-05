# Agent Handoff Protocol

> **Standard handoff format for multi-agent workflows**
> **Version:** 1.4.0
> **Purpose:** Eliminate duplication, ensure clear communication between agents

---

## 📋 Overview

When an agent completes a task in a multi-agent workflow, it should provide a **handoff report** for the next agent.

**Why this exists:**
- ✅ Next agent doesn't waste time reading all code
- ✅ API contracts/interfaces are crystal clear
- ✅ Prevents miscommunication and bugs
- ✅ Saves time (no reverse-engineering needed)

**Who uses this:**
- All 6 agents when working in multi-phase workflows
- Especially important for: uxui-frontend → frontend, backend → frontend, database → backend

**When to use:**
- ✅ Multi-phase OpenSpec workflows (/csetup → /cdev)
- ✅ When work depends on another agent
- ✅ When handing off complex logic or data structures

**When NOT needed:**
- ❌ Single-agent tasks
- ❌ Independent work (no dependencies)
- ❌ User explicitly says "skip handoff"

---

## 📝 Standard Handoff Template

### Base Format (All Agents):

```markdown
## ✅ Task Complete: [Task Name]

**Agent:** {agent-name}

**What I Did:**
- {summary-of-work-done}
- {key-changes-made}
- {files-created-or-modified}

**For Next Agent ({next-agent-name}):**

{agent-specific-handoff-info}

**Important Notes:**
- {any-gotchas-or-warnings}
- {configuration-needed}
- {things-to-watch-out-for}

**Files Created/Modified:**
- {file-path-1}
- {file-path-2}
- {file-path-3}
```

---

## 🎨 Agent-Specific Handoff Formats

### 1. uxui-frontend → frontend

**Purpose:** Hand off UI with mock data to connect to real APIs

**Template:**

```markdown
## ✅ Task Complete: Create {component-name} UI

**Agent:** uxui-frontend

**What I Did:**
- Created {ComponentName} component with {features}
- Added form validation ({validation-rules})
- Created submit button with loading state
- Using mock data for now (hardcoded values)

**For Next Agent (Frontend):**

**Component Location:**
- {component-path}

**Current Mock Implementation:**
\`\`\`typescript
// Remove this mock logic:
const mockFunction = (param1, param2) => {
  // ...hardcoded mock data...
}
\`\`\`

**Replace With:**
\`\`\`typescript
// Real API call:
const response = await fetch('/api/{endpoint}', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ param1, param2 })
})

if (!response.ok) {
  const error = await response.json()
  throw new Error(error.detail || 'Request failed')
}

const data = await response.json()
// data = { expected-structure }
\`\`\`

**State Management Needed:**
- Store {what-to-store} (localStorage/cookie/global state)
- Add {actions-needed} (e.g., logout, refresh)

**Important Notes:**
- Form already validates {what} (client-side)
- Loading state already handled (disable button during submit)
- Error messages displayed {where} (update with API error)
- Success: redirect to {page}

**Files Created:**
- {component-path}
- {related-components}
```

**Example:**

```markdown
## ✅ Task Complete: Create login form UI

**Agent:** uxui-frontend

**What I Did:**
- Created LoginForm component with email/password inputs
- Added form validation (required, email format)
- Created submit button with loading state
- Using mock data for now (hardcoded credentials)

**For Next Agent (Frontend):**

**Component Location:**
- components/LoginForm.tsx

**Current Mock Implementation:**
\`\`\`typescript
// Remove this mock logic:
const mockLogin = (email: string, password: string) => {
  if (email === 'test@example.com' && password === 'password123') {
    return { token: 'mock-token', user: { id: '1', email } }
  }
  throw new Error('Invalid credentials')
}
\`\`\`

**Replace With:**
\`\`\`typescript
// Real API call:
const response = await fetch('/api/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ email, password })
})

if (!response.ok) {
  const error = await response.json()
  throw new Error(error.detail || 'Login failed')
}

const data = await response.json()
// data = { token: string, user: { id, email, name } }
\`\`\`

**State Management Needed:**
- Store JWT token (localStorage or cookie)
- Store user object (global state - Zustand/Redux)
- Add logout action (clear token + user)

**Important Notes:**
- Form already validates email format (client-side)
- Loading state already handled (disable button during submit)
- Error messages displayed below form (update with API error)
- Success: redirect to dashboard or home page

**Files Created:**
- components/LoginForm.tsx
- components/ui/Input.tsx (reusable)
- components/ui/Button.tsx (reusable)
```

---

### 2. backend → frontend

**Purpose:** Hand off API contract for frontend to integrate

**Template:**

```markdown
## ✅ Task Complete: Create {endpoint-method} {endpoint-path}

**Agent:** backend

**What I Did:**
- Created {endpoint-method} {endpoint-path} endpoint
- Added {validation-type} validation
- Implemented {business-logic}
- Added error handling ({error-cases})

**For Next Agent (Frontend):**

**API Contract:**
- **Endpoint:** {METHOD} {path}
- **Request Body:**
  \`\`\`json
  {
    "field1": "type (validation-rules)",
    "field2": "type (validation-rules)"
  }
  \`\`\`
- **Success Response ({status-code}):**
  \`\`\`json
  {
    "field1": "type (description)",
    "field2": "type (description)"
  }
  \`\`\`
- **Error Response ({status-code}):**
  \`\`\`json
  {
    "detail": "error message format"
  }
  \`\`\`

**Authentication Required:**
- {Yes/No}
- If yes: Include "Authorization: Bearer {token}" header

**Important Notes:**
- {special-requirements}
- {edge-cases}
- {rate-limiting}

**Files Created:**
- {endpoint-file}
- {model-file}
- {test-file}
```

**Example:**

```markdown
## ✅ Task Complete: Create POST /api/auth/login

**Agent:** backend

**What I Did:**
- Created POST /api/auth/login endpoint
- Added email/password validation with Pydantic
- Implemented JWT token generation
- Added error handling (401 for invalid credentials)

**For Next Agent (Frontend):**

**API Contract:**
- **Endpoint:** POST /api/auth/login
- **Request Body:**
  \`\`\`json
  {
    "email": "string (required, must be valid email)",
    "password": "string (required, min 8 chars)"
  }
  \`\`\`
- **Success Response (200):**
  \`\`\`json
  {
    "token": "string (JWT token, expires in 7 days)",
    "user": {
      "id": "string (UUID)",
      "email": "string",
      "name": "string | null"
    }
  }
  \`\`\`
- **Error Response (401):**
  \`\`\`json
  {
    "detail": "Invalid credentials"
  }
  \`\`\`
- **Error Response (422):**
  \`\`\`json
  {
    "detail": [
      {
        "loc": ["body", "email"],
        "msg": "field required",
        "type": "value_error.missing"
      }
    ]
  }
  \`\`\`

**Important Notes:**
- Store JWT token in localStorage or httpOnly cookie
- Include token in Authorization header: "Bearer {token}"
- Token expires in 7 days - handle refresh or re-login
- Validate email format on frontend before sending (better UX)

**Files Created:**
- app/api/auth.py (endpoint handler)
- app/models/user.py (User model)
- tests/test_auth.py (unit tests)
```

---

### 3. database → backend

**Purpose:** Hand off schema/queries for backend to use

**Template:**

```markdown
## ✅ Task Complete: Create {model-name} schema/queries

**Agent:** database

**What I Did:**
- Created {ModelName} model/schema
- Added {fields} with {constraints}
- Created migration {migration-id}
- Implemented {query-types}

**For Next Agent (Backend):**

**Model Location:**
- {model-file-path}

**Schema:**
\`\`\`typescript
{
  field1: type (constraints),
  field2: type (constraints),
  relationships: [...]
}
\`\`\`

**Available Queries:**
\`\`\`typescript
// Find by ID
const user = await db.{model}.findUnique({ where: { id } })

// Find by email
const user = await db.{model}.findFirst({ where: { email } })

// Create
const user = await db.{model}.create({ data: {...} })

// Update
const user = await db.{model}.update({ where: { id }, data: {...} })
\`\`\`

**Validation Rules:**
- {field1}: {validation-rules}
- {field2}: {validation-rules}

**Important Notes:**
- {indexes-created}
- {cascading-deletes}
- {unique-constraints}

**Files Created:**
- {schema-file}
- {migration-file}
```

**Example:**

```markdown
## ✅ Task Complete: Create User schema

**Agent:** database

**What I Did:**
- Created User model with auth fields
- Added email unique constraint
- Created migration 20250101000000_create_users
- Implemented CRUD queries

**For Next Agent (Backend):**

**Model Location:**
- prisma/schema.prisma → model User

**Schema:**
\`\`\`typescript
{
  id: string (UUID, primary key),
  email: string (unique, required),
  password: string (hashed, required),
  name: string? (optional),
  createdAt: DateTime (auto),
  updatedAt: DateTime (auto)
}
\`\`\`

**Available Queries:**
\`\`\`typescript
// Find by email
const user = await db.user.findUnique({ where: { email } })

// Create user
const user = await db.user.create({
  data: { email, password: hashedPassword, name }
})

// Update user
const user = await db.user.update({
  where: { id },
  data: { name }
})
\`\`\`

**Validation Rules:**
- email: Must be valid email format, unique
- password: Min 8 chars (hash before storing!)
- name: Optional, max 255 chars

**Important Notes:**
- Email has unique index for fast lookups
- Password should be hashed with bcrypt (backend's job)
- createdAt/updatedAt auto-managed by Prisma

**Files Created:**
- prisma/schema.prisma (User model)
- prisma/migrations/20250101000000_create_users/migration.sql
```

---

### 4. backend → integration

**Purpose:** Hand off API implementation for contract validation

**Template:**

```markdown
## ✅ Task Complete: Implement {endpoint-method} {endpoint-path}

**Agent:** backend

**What I Did:**
- Implemented {endpoint-method} {endpoint-path}
- Added validation, error handling, logging
- Tested manually with {tool}

**For Next Agent (Integration):**

**Endpoint to Validate:**
- {METHOD} {path}

**Expected Behavior:**
- Request: {describe}
- Response: {describe}
- Errors: {describe}

**Test Cases:**
\`\`\`
1. Valid request → 200 + expected response
2. Missing field → 422 + validation error
3. Invalid credentials → 401 + error message
\`\`\`

**Important Notes:**
- {authentication-requirements}
- {edge-cases}

**Files Created:**
- {endpoint-file}
- {test-file}
```

---

### 5. integration → frontend

**Purpose:** Hand off validated contract for frontend integration

**Template:**

```markdown
## ✅ Task Complete: Validate {endpoint-method} {endpoint-path}

**Agent:** integration

**What I Did:**
- Validated API contract for {endpoint}
- Tested {test-cases}
- Confirmed response structure matches

**For Next Agent (Frontend):**

**Validated API Contract:**
- **Endpoint:** {METHOD} {path}
- **Request:** (see backend handoff)
- **Response:** (see backend handoff)
- **Tested:** ✅ All cases passed

**Integration Notes:**
- {special-considerations}
- {error-handling-recommendations}

**Ready for Integration:**
- ✅ Contract validated
- ✅ Response structure confirmed
- ✅ Error cases documented
```

---

### 6. frontend → test-debug

**Purpose:** Hand off integrated feature for testing

**Template:**

```markdown
## ✅ Task Complete: Connect {feature-name} to API

**Agent:** frontend

**What I Did:**
- Connected {ComponentName} to {endpoint}
- Implemented state management with {tool}
- Added error handling and loading states

**For Next Agent (Test-Debug):**

**Test Scenarios:**
1. {scenario-1}
2. {scenario-2}
3. {scenario-3}

**Expected Behavior:**
- {describe-expected-flow}

**Files to Test:**
- {component-file}
- {state-file}
- {util-file}

**Important Notes:**
- {edge-cases}
- {known-issues}
```

---

## 🔄 Handoff Flow Examples

### Example 1: Full Login Feature Flow

```
Phase 1: uxui-frontend
└─→ Handoff to: frontend
    └─→ Handoff to: test-debug

Phase 2 (parallel):
├─→ backend
│   └─→ Handoff to: integration
└─→ database
    └─→ Handoff to: backend

Phase 2.5: integration
└─→ Handoff to: frontend

Phase 3: frontend
└─→ Handoff to: test-debug

Phase 4: test-debug
└─→ Final report to user
```

**Handoff Chain:**

1. **uxui-frontend → frontend:**
   - "Here's the LoginForm with mock data, replace with real API"

2. **database → backend:**
   - "Here's the User model, use these queries"

3. **backend → integration:**
   - "Here's POST /api/auth/login, validate the contract"

4. **integration → frontend:**
   - "Contract validated ✅, ready to integrate"

5. **frontend → test-debug:**
   - "Connected form to API, test these scenarios"

---

## 📊 Best Practices

### ✅ DO:

- Provide clear, actionable handoff info
- Include code snippets (what to replace/add)
- Document API contracts explicitly
- List all files created/modified
- Note important gotchas and warnings
- Keep handoff concise but complete

### ❌ DON'T:

- Assume next agent will "figure it out"
- Skip important details (API structure, validation rules)
- Use vague descriptions ("fix the code")
- Forget to list files created
- Skip handoff for complex multi-agent tasks

### 📏 Length Guidelines:

- **Minimum:** 10-15 lines (brief tasks)
- **Typical:** 20-40 lines (standard tasks)
- **Maximum:** 60-80 lines (complex tasks)
- **Too Long?** Split into sections, use collapsible details

---

## 🎯 Quick Reference

### Handoff Checklist:

```markdown
Before marking task complete, verify your handoff includes:

[ ] Task name clearly stated
[ ] Agent name (your role)
[ ] Summary of what you did
[ ] Files created/modified (with paths)
[ ] Next agent identified
[ ] Agent-specific handoff info:
    - uxui-frontend: Mock code to replace
    - backend: API contract details
    - database: Schema and query examples
    - integration: Validation results
    - frontend: Test scenarios
[ ] Important notes/gotchas
[ ] Code snippets (what to replace/add)
```

---

## 🔗 See Also

- `agent-router.md` - Agent routing rules (who calls who)
- `validation-framework.md` - Pre-work validation requirements
- `context-loading-protocol.md` - How agents load context
- `agent-executor.md` - How /cdev executes agents with retry
