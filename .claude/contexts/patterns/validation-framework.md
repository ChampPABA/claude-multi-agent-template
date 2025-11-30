# Comprehensive Validation Framework

> **Validation patterns for agent pre-work**
> **Version:** 2.0.0 (Claude 4.5 Optimized)

---

## 🎯 Overview

Every agent has pre-work steps that ensure quality output.

WHY: Pre-work validation prevents inconsistent output (mismatched colors, missing error handling, duplicate components).

**Principles:**
1. **Report Before Code** - Agent must report completion BEFORE implementation
2. **Validation Gates** - Orchestrator validates BEFORE allowing next step
3. **Rejection with Guidance** - Clear feedback if validation fails
4. **Pattern-Specific** - Each agent has unique validation requirements

---

## 📋 Validation Checklists by Agent

### 1️⃣ **uxui-frontend Agent**

**Required Pre-Work:**

```markdown
## ✅ Pre-Implementation Validation Report

### A. Design Foundation ✓
- [x] Read: design/index.md
- [x] Read: design/box-thinking.md
- [x] Read: design/color-theory.md
- [x] Read: design/spacing.md
- [x] Read: design/shadows.md
- [x] Read: patterns/ui-component-consistency.md
- [x] Read: patterns/frontend-component-strategy.md

**Summary:** Loaded design system, spacing scale (8/16/24/32/40/48px), color tokens, shadow patterns.

### B. Box Thinking Analysis ✓
**Component:** [Landing Page]

**Structure:**
```
Landing Page
├─ Hero (container) - padding: 48px
│  ├─ Headline (h1)
│  ├─ Subtitle (p)
│  └─ CTA Button
└─ Features (container) - gap: 24px
   └─ FeatureCard x3 (grid)
      ├─ Icon
      ├─ Title
      └─ Description
```

**Spacing Plan:**
- Hero: padding-12 (48px)
- Card gap: gap-6 (24px)
- Card padding: padding-6 (24px)

**Responsive:**
- Mobile (<640px): Stack vertically
- Tablet (640-1024px): 2-column grid
- Desktop (>1024px): 3-column grid

### C. Component Search ✓
**Search Performed:**
```bash
Glob: "**/*{Hero,Feature,Card,Button,Icon}*.{tsx,jsx}"
Grep: "export.*function.*(Button|Card)"
```

**Results:**
- ✅ Found: components/ui/Button.tsx
- ✅ Found: components/ui/Card.tsx
- ❌ Not found: Hero, FeatureCard

**Decision:**
- **Reuse:** Button (variant="primary", size="lg")
- **Reuse:** Card (for FeatureCard base)
- **Create New:** HeroSection, FeatureCard (no alternatives exist)

**Justification:** Hero and FeatureCard are domain-specific, cannot reuse generic components.

### D. Design Tokens Extracted ✓
**Reference:** components/ui/Button.tsx

```typescript
const DESIGN_TOKENS = {
  spacing: {
    padding: 'px-4 py-2',  // Button default
    gap: 'gap-4'            // Between elements
  },
  colors: {
    primary: 'bg-blue-600',
    primaryHover: 'hover:bg-blue-700',
    text: 'text-white',
    muted: 'text-foreground/70'
  },
  shadows: 'shadow-sm',
  radius: 'rounded-md',
  transitions: 'transition-colors duration-200'
}
```

**Consistency Check:**
- ✅ All buttons use bg-blue-600/700
- ✅ All rounded corners use rounded-md
- ✅ All shadows use shadow-sm
- ✅ Will follow these patterns

### E. Mock Data Strategy ✓
```typescript
const MOCK_DATA = {
  hero: {
    headline: "Welcome to Our Platform",
    subtitle: "Build amazing things",
    ctaText: "Get Started"
  },
  features: [
    { id: 1, title: "Fast", description: "Lightning speed", icon: "⚡" },
    { id: 2, title: "Secure", description: "Bank-level security", icon: "🔒" },
    { id: 3, title: "Scalable", description: "Grows with you", icon: "📈" }
  ]
}
// TODO: Replace with API call in Phase 3
```

### F. Ready to Implement ✓
✅ All design contexts loaded
✅ Box thinking complete
✅ Existing components searched
✅ Design tokens extracted
✅ Mock data prepared

**Proceeding with implementation...**
```

**Validation Keywords:**
- Contains: "Design Foundation ✓"
- Contains: "Box Thinking Analysis ✓"
- Contains: "Component Search ✓"
- Contains: "Design Tokens Extracted ✓"
- Contains: "Ready to Implement ✓"

---

### 2️⃣ **backend Agent**

**Required Pre-Work:**

```markdown
## ✅ Pre-Implementation Validation Report

### A. Patterns Loaded ✓
- [x] Read: patterns/error-handling.md
- [x] Read: patterns/logging.md
- [x] Read: patterns/testing.md

### B. Existing Endpoints Search ✓
**Search Performed:**
```bash
Grep: "router\\.(post|get|put|delete).*\\/api\\/auth"
Grep: "@app\\.(post|get).*\\/api\\/auth"
```

**Results:**
- ❌ No existing /api/auth/login
- ❌ No existing /api/auth/register
- ✅ Can proceed with implementation

### C. TDD Workflow (if metadata: | TDD |) ✓
**TDD Required:** YES (metadata flag detected)

**Phase Plan:**
1. 🔴 RED: Write 7 tests FIRST
   - test_register_success
   - test_register_duplicate_email
   - test_register_invalid_email
   - test_register_weak_password
   - test_login_success
   - test_login_invalid_credentials
   - test_login_validation_error

2. ✅ GREEN: Minimal implementation
   - User model
   - Password hashing (bcrypt)
   - JWT generation
   - Registration endpoint
   - Login endpoint

3. 🔧 REFACTOR: Add production quality
   - Structured logging
   - Error handling
   - Type hints
   - Docstrings

**Commitment:** Will follow RED-GREEN-REFACTOR strictly.

### D. Error Handling Pattern ✓
**From:** patterns/error-handling.md

```python
# Pattern to follow:
try:
    # Business logic
    user = await create_user(...)
    logger.info("user_created", extra={"user_id": user.id})
    return {"id": user.id}
except HTTPException:
    raise  # Re-raise HTTP exceptions
except Exception as e:
    logger.error("user_creation_error", extra={"error": str(e)})
    raise HTTPException(status_code=500, detail="Internal server error")
```

### E. Logging Pattern ✓
**From:** patterns/logging.md

```python
# All significant events:
logger.info("api_route_entry", extra={"route": "/api/auth/login"})
logger.info("login_success", extra={"user_id": user.id})
logger.warning("login_failed", extra={"email": email, "reason": "invalid_credentials"})
logger.error("login_error", extra={"error": str(e)})
```

### F. Ready to Implement ✓
✅ Patterns loaded
✅ Existing endpoints searched
✅ TDD workflow planned
✅ Error handling pattern identified
✅ Logging pattern identified

**Proceeding with TDD (RED phase first)...**
```

**Validation Keywords:**
- Contains: "Patterns Loaded ✓"
- Contains: "Existing Endpoints Search ✓"
- IF TDD: Contains "TDD Workflow" + "RED-GREEN-REFACTOR"
- Contains: "Error Handling Pattern ✓"
- Contains: "Logging Pattern ✓"
- Contains: "Ready to Implement ✓"

---

### 3️⃣ **frontend Agent**

**Required Pre-Work:**

```markdown
## ✅ Pre-Implementation Validation Report

### A. Patterns Loaded ✓
- [x] Read: patterns/error-handling.md
- [x] Read: patterns/logging.md
- [x] Read: patterns/testing.md

### B. API Contract Review ✓
**From:** integration agent / API spec

**Endpoints to Connect:**
- POST /api/auth/login
  - Request: { email: string, password: string }
  - Success (200): { token: string, user: { id, email } }
  - Error (401): { detail: "Invalid credentials" }
  - Error (422): { detail: [...validation errors] }

**State Management Needed:**
- Auth state (user, token, isLoading)
- Form state (email, password, errors)

### C. State Management Strategy ✓
**Framework:** Zustand (from tech-stack.md)

```typescript
// Create auth store
import { create } from 'zustand'

interface AuthState {
  user: User | null
  token: string | null
  isLoading: boolean
  login: (email: string, password: string) => Promise<void>
  logout: () => void
}

const useAuthStore = create<AuthState>((set) => ({
  user: null,
  token: null,
  isLoading: false,
  login: async (email, password) => {
    set({ isLoading: true })
    try {
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        body: JSON.stringify({ email, password })
      })
      const data = await response.json()
      set({ user: data.user, token: data.token, isLoading: false })
    } catch (error) {
      set({ isLoading: false })
      throw error
    }
  },
  logout: () => set({ user: null, token: null })
}))
```

### D. Error Handling Strategy ✓
```typescript
// User-friendly error messages
const handleError = (error: ApiError) => {
  if (error.status === 401) {
    toast.error("Invalid email or password")
  } else if (error.status === 422) {
    // Show validation errors
    error.detail.forEach(err => {
      setFieldError(err.loc[1], err.msg)
    })
  } else {
    toast.error("Something went wrong. Please try again.")
  }

  // Log for debugging (no sensitive data)
  logger.error("login_failed", { status: error.status })
}
```

### E. Component Integration Plan ✓
**Existing Component:** LoginForm (from uxui-frontend phase)

**Changes Required:**
1. Replace mock onClick with real useAuthStore
2. Add loading state (disable button, show spinner)
3. Add error handling (toast notifications)
4. Add form validation (client-side)
5. Add redirect after success

### F. Ready to Implement ✓
✅ Patterns loaded
✅ API contract reviewed
✅ State management strategy defined
✅ Error handling strategy defined
✅ Component integration plan ready

**Proceeding with implementation...**
```

**Validation Keywords:**
- Contains: "Patterns Loaded ✓"
- Contains: "API Contract Review ✓"
- Contains: "State Management Strategy ✓"
- Contains: "Error Handling Strategy ✓"
- Contains: "Ready to Implement ✓"

---

### 4️⃣ **database Agent**

**Required Pre-Work:**

```markdown
## ✅ Pre-Implementation Validation Report

### A. Patterns Loaded ✓
- [x] Read: patterns/error-handling.md
- [x] Read: patterns/logging.md

### B. Existing Schema Search ✓
**Search Performed:**
```bash
Glob: "**/*.prisma"
Glob: "**/*models*.py"
Grep: "class.*\\(Base\\)"
Grep: "model User"
```

**Results:**
- ❌ No existing User model
- ✅ Can proceed with schema design

### C. Schema Design Plan ✓
**Model:** User

**Fields:**
- id: string (UUID, primary key)
- email: string (unique, indexed)
- hashed_password: string (never exposed)
- created_at: datetime (auto)
- updated_at: datetime (auto)

**Constraints:**
- Unique: email
- Index: email (for fast lookups)

**Relationships:**
- User → Sessions (1:N) - for JWT token management

### D. Migration Strategy ✓
**ORM:** Prisma (from tech-stack.md)

```bash
# Generate migration
pnpm prisma migrate dev --name add_user_model

# This will create:
# prisma/migrations/YYYYMMDD_add_user_model/migration.sql
```

### E. Query Functions Plan ✓
```typescript
// Create user
async function createUser(email: string, hashedPassword: string): Promise<User>

// Find by email (for login)
async function findUserByEmail(email: string): Promise<User | null>

// Update password
async function updatePassword(userId: string, newHashedPassword: string): Promise<void>
```

### F. Performance Considerations ✓
- ✅ Index on email (unique constraint also creates index)
- ✅ Use select() to avoid exposing hashed_password
- ✅ No N+1 queries (direct lookups)

### G. Ready to Implement ✓
✅ Patterns loaded
✅ Existing schemas searched
✅ Schema design planned
✅ Migration strategy defined
✅ Query functions planned
✅ Performance considered

**Proceeding with schema implementation...**
```

**Validation Keywords:**
- Contains: "Patterns Loaded ✓"
- Contains: "Existing Schema Search ✓"
- Contains: "Schema Design Plan ✓"
- Contains: "Migration Strategy ✓"
- Contains: "Ready to Implement ✓"

---

### 5️⃣ **test-debug Agent**

**Required Pre-Work:**

```markdown
## ✅ Pre-Implementation Validation Report

### A. Patterns Loaded ✓
- [x] Read: patterns/testing.md
- [x] Read: patterns/error-handling.md
- [x] Read: patterns/logging.md

### B. Test Scope Analysis ✓
**Phase:** Component Tests / Backend Tests / E2E Tests

**Components to Test:**
- HeroSection
- FeatureCard
- LoginForm

**Coverage Target:** 85% (from project standards)

### C. Test Strategy ✓
**Framework:** Vitest (from tech-stack.md)

**Test Types:**
1. **Unit Tests**
   - Component rendering
   - Props validation
   - Event handlers
   - State changes

2. **Integration Tests**
   - Component interactions
   - API mocking
   - State management

### D. Existing Test Patterns ✓
**Search Performed:**
```bash
Grep: "describe.*test.*it\\("
Grep: "expect\\(.*\\)\\.toBe"
```

**Pattern Found:**
```typescript
// Existing pattern in __tests__/Button.test.tsx
describe('Button', () => {
  it('renders with correct text', () => {
    render(<Button>Click me</Button>)
    expect(screen.getByText('Click me')).toBeInTheDocument()
  })

  it('calls onClick when clicked', () => {
    const handleClick = vi.fn()
    render(<Button onClick={handleClick}>Click</Button>)
    fireEvent.click(screen.getByText('Click'))
    expect(handleClick).toHaveBeenCalledTimes(1)
  })
})
```

**Will follow this pattern.**

### E. Debug Strategy (if tests fail) ✓
**Max Iterations:** 3-4
**Per Iteration:**
1. Read error messages carefully
2. Identify root cause
3. Fix code or test
4. Re-run
5. Log iteration results

**If stuck after 4 iterations:**
- Escalate to main Claude with:
  - Error messages
  - Code attempted
  - Suspected root cause

### F. Ready to Implement ✓
✅ Patterns loaded
✅ Test scope analyzed
✅ Test strategy defined
✅ Existing patterns identified
✅ Debug strategy prepared

**Proceeding with test implementation...**
```

**Validation Keywords:**
- Contains: "Patterns Loaded ✓"
- Contains: "Test Scope Analysis ✓"
- Contains: "Test Strategy ✓"
- Contains: "Existing Test Patterns ✓"
- Contains: "Ready to Implement ✓"

---

### 6️⃣ **integration Agent**

**Required Pre-Work:**

```markdown
## ✅ Pre-Implementation Validation Report

### A. Validation Type ✓
**Phase:** API Design / Contract Validation / Business Logic

**Tasks:**
- [ ] Generate OpenAPI spec (if API Design)
- [ ] Validate backend/frontend contracts (if Contract Validation)
- [ ] Verify requirements (if Business Logic)

### B. Contract Sources ✓
**Backend API Files:**
```bash
Glob: "**/api/**/*.{py,ts,js}"
Grep: "router\\.(post|get|put|delete)"
Grep: "@app\\.(post|get)"
```

**Frontend API Calls:**
```bash
Grep: "fetch\\(.*\\/api\\/"
Grep: "axios\\.(post|get)"
```

### C. Validation Checklist ✓
**For Each Endpoint:**
- [ ] Request schema matches
- [ ] Response schema matches
- [ ] Status codes match
- [ ] Error responses match
- [ ] Types compatible

### D. Business Requirements Check ✓
**From:** proposal.md

**Requirements:**
1. User registration with email validation
2. User login with JWT
3. Secure password storage

**Implementation Check:**
- [x] Registration endpoint exists → POST /api/auth/register
- [x] Login endpoint exists → POST /api/auth/login
- [x] Email validation → Pydantic EmailStr
- [x] JWT generation → lib/jwt.py
- [x] Password hashing → bcrypt

**Result:** All requirements met ✓

### E. Ready to Validate ✓
✅ Validation type identified
✅ Contract sources located
✅ Validation checklist prepared
✅ Business requirements reviewed

**Proceeding with validation...**
```

**Validation Keywords:**
- Contains: "Validation Type ✓"
- Contains: "Contract Sources ✓" OR "Requirements Check ✓"
- Contains: "Ready to Validate ✓"

---

## ✅ Validation Enforcement Logic

### Orchestrator Validation Function

```typescript
interface ValidationResult {
  passed: boolean
  missing: string[]
  report?: string
}

function validateAgentPreWork(
  agentType: string,
  agentResponse: string,
  phaseMetadata: string
): ValidationResult {
  const required: string[] = []

  // Common for all agents
  required.push("Pre-Implementation Validation Report")
  required.push("Ready to Implement ✓")

  // Agent-specific requirements
  switch (agentType) {
    case "uxui-frontend":
      required.push("Design Foundation ✓")
      required.push("Box Thinking Analysis ✓")
      required.push("Component Search ✓")
      required.push("Design Tokens Extracted ✓")
      break

    case "backend":
      required.push("Patterns Loaded ✓")
      required.push("Existing Endpoints Search ✓")
      required.push("Error Handling Pattern ✓")
      required.push("Logging Pattern ✓")

      // TDD specific
      if (phaseMetadata.includes("| TDD |")) {
        required.push("TDD Workflow")
        required.push("RED-GREEN-REFACTOR")
      }
      break

    case "frontend":
      required.push("Patterns Loaded ✓")
      required.push("API Contract Review ✓")
      required.push("State Management Strategy ✓")
      required.push("Error Handling Strategy ✓")
      break

    case "database":
      required.push("Patterns Loaded ✓")
      required.push("Existing Schema Search ✓")
      required.push("Schema Design Plan ✓")
      required.push("Migration Strategy ✓")
      break

    case "test-debug":
      required.push("Patterns Loaded ✓")
      required.push("Test Scope Analysis ✓")
      required.push("Test Strategy ✓")
      required.push("Existing Test Patterns ✓")
      break

    case "integration":
      required.push("Validation Type ✓")
      required.push("Ready to Validate ✓")
      break
  }

  // Check all requirements
  const missing = required.filter(req =>
    !agentResponse.includes(req)
  )

  return {
    passed: missing.length === 0,
    missing,
    report: missing.length === 0 ? agentResponse : undefined
  }
}
```

### Rejection Message Template

```markdown
❌ **Validation Failed**

Your response is missing required pre-work steps:

{missing.map(item => `- ${item}`).join('\n')}

**Complete all pre-work steps before implementation for quality output.**

Please provide a complete Pre-Implementation Validation Report covering:

{agent-specific requirements}

**Format:**
```markdown
## ✅ Pre-Implementation Validation Report

### A. {First Requirement} ✓
[details]

### B. {Second Requirement} ✓
[details]

...

### Ready to Implement ✓
[confirmation]
```

**Only after validation passes can you proceed with implementation.**
```

---

## 🔄 Updated Workflow

```
User: /cdev CHANGE-001
  ↓
Main Claude: Read phases.md → Phase 1 (uxui-frontend)
  ↓
Main Claude: Build prompt with validation requirement
  ↓
Main Claude: Invoke agent
  ↓
Agent: Respond with Pre-Implementation Report
  ↓
Main Claude: Validate report
  ├─ ❌ Invalid → Send rejection message → Wait for corrected report
  └─ ✅ Valid → Allow agent to proceed
       ↓
Agent: Implement with validated context
  ↓
Agent: Update flags.json
  ↓
Main Claude: Move to next phase
```

---

## 📊 Validation Coverage

| Agent | Design | TDD | Reuse | Errors | Logging | Testing | State |
|-------|--------|-----|-------|--------|---------|---------|-------|
| **uxui-frontend** | ✅ | - | ✅ | - | - | - | - |
| **backend** | - | ✅ | ✅ | ✅ | ✅ | - | - |
| **frontend** | - | - | - | ✅ | ✅ | - | ✅ |
| **database** | - | - | ✅ | ✅ | ✅ | - | - |
| **test-debug** | - | - | ✅ | - | - | ✅ | - |
| **integration** | - | - | - | - | - | - | - |

---

**Every agent, every pattern, fully validated!** ✅
