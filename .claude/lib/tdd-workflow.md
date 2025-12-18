# TDD Workflow (Red-Green-Refactor)

> **Test-Driven Development methodology for complex/critical tasks**
> **Version:** 1.4.0
> **Purpose:** Eliminate duplication across backend/frontend/database agents

---

## 📋 Overview

This document defines the TDD (Test-Driven Development) workflow using the Red-Green-Refactor cycle.

**Why this exists:**
- ✅ Single source of truth for TDD methodology
- ✅ Prevents errors in critical code (auth, payment, migrations)
- ✅ Ensures testability (write tests first)
- ✅ Consistent TDD practice across agents

**Who uses this:**
- **backend agent:** When `tdd_required: true` (auth, payment, security)
- **frontend agent:** When `tdd_required: true` (complex state, multi-step forms)
- **database agent:** When `tdd_required: true` (migrations, schema changes)

**When to use TDD:**
- ✅ Authentication/authorization logic
- ✅ Payment processing
- ✅ Security-critical features
- ✅ Complex business logic
- ✅ Database migrations
- ✅ Multi-step workflows
- ✅ Any task with `tdd_required: true` flag

**When NOT to use TDD (use Test-Alongside):**
- ❌ Simple CRUD endpoints
- ❌ Read-only queries
- ❌ Presentational UI components
- ❌ Static pages
- ❌ Any task with `tdd_required: false` flag

---

## 🔄 The Red-Green-Refactor Cycle

### Overview:

```
1. 🔴 RED Phase: Write Test First
   ├─→ Test MUST fail (feature doesn't exist yet)
   └─→ Defines expected behavior

2. 🟢 GREEN Phase: Minimal Implementation
   ├─→ Write just enough code to pass tests
   └─→ Focus on making it work (not perfect)

3. 🔵 REFACTOR Phase: Improve Code Quality
   ├─→ Add error handling, logging, validation
   ├─→ Improve structure and readability
   └─→ Tests MUST still pass
```

**Key Principle:** Tests drive the implementation, not the other way around.

---

## 🔴 RED Phase: Write Test First

### Purpose:

- Define expected behavior BEFORE writing code
- Ensure feature is testable from the start
- Document requirements as executable tests

### Protocol:

**Step 1: Write failing tests**

```
✅ DO:
- Write comprehensive test cases
- Cover success cases
- Cover error cases
- Cover edge cases
- Use descriptive test names

❌ DON'T:
- Write implementation code yet
- Skip error cases
- Use vague test names
- Assume implementation details
```

**Step 2: Run tests**

```bash
# Expected result: ❌ FAILED
# This is CORRECT! Tests should fail in RED phase.
```

**Step 3: Verify test failure**

```
✅ Test failed for the right reason:
   - Feature doesn't exist (404, Connection refused)
   - Endpoint not found
   - Function not defined

❌ Test failed for wrong reason:
   - Syntax error in test
   - Wrong import
   - Test configuration issue
```

---

## 🟢 GREEN Phase: Minimal Implementation

### Purpose:

- Make tests pass with simplest possible code
- Don't worry about perfect code yet
- Focus on correctness, not elegance

### Protocol:

**Step 1: Write minimal code**

```
✅ DO:
- Write just enough to make tests pass
- Use hardcoded values (will refactor later)
- Keep it simple and straightforward

❌ DON'T:
- Over-engineer
- Add unnecessary features
- Optimize prematurely
- Add complex error handling (save for REFACTOR)
```

**Step 2: Run tests**

```bash
# Expected result: ✅ PASSED
# All (or most) tests should pass now.
```

**Step 3: Verify all tests pass**

```
✅ If all tests pass:
   → Move to REFACTOR phase

⚠️ If some tests still fail:
   → Fix implementation (stay in GREEN phase)

❌ If tests pass but you added extra features:
   → Remove extra features (YAGNI principle)
```

---

## 🔵 REFACTOR Phase: Production Quality

### Purpose:

- Improve code quality while keeping tests green
- Add error handling, logging, validation
- Optimize and clean up

### Protocol:

**Step 1: Improve code quality**

```
✅ DO:
- Add error handling (try/catch, validation)
- Add structured logging (entry, success, error)
- Add type hints / TypeScript types
- Add docstrings / JSDoc comments
- Extract reusable functions
- Follow coding standards
- Improve variable names

❌ DON'T:
- Change test expectations (tests are requirements)
- Break existing functionality
- Add untested features
```

**Step 2: Run tests after EACH change**

```bash
# After every refactor:
# Expected result: ✅ PASSED (tests still pass!)
```

**Step 3: Verify tests still pass**

```
✅ If tests pass:
   → Continue refactoring
   → When satisfied, mark task complete

❌ If tests fail:
   → Undo last change
   → Fix refactoring
   → Run tests again
```

---

## 📚 Language-Specific Examples

### Python (FastAPI + Pytest)

#### 🔴 RED Phase:

```python
# tests/test_auth.py (WRITE THIS FIRST!)
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_login_success(client: AsyncClient):
    """Test successful login with valid credentials"""
    response = await client.post("/api/auth/login", json={
        "email": "test@example.com",
        "password": "password123"
    })

    assert response.status_code == 200
    data = response.json()
    assert "token" in data
    assert data["user"]["email"] == "test@example.com"

@pytest.mark.asyncio
async def test_login_invalid_credentials(client: AsyncClient):
    """Test invalid credentials return 401"""
    response = await client.post("/api/auth/login", json={
        "email": "wrong@example.com",
        "password": "wrongpass"
    })

    assert response.status_code == 401
    assert "invalid" in response.json()["detail"].lower()

@pytest.mark.asyncio
async def test_login_validation_error(client: AsyncClient):
    """Test validation on missing fields"""
    response = await client.post("/api/auth/login", json={
        "email": "not-an-email"
        # Missing password
    })

    assert response.status_code == 422  # Validation error
```

**Run tests:**
```bash
pytest tests/test_auth.py -v

# Expected: ❌ FAILED (endpoint doesn't exist)
```

#### 🟢 GREEN Phase:

```python
# app/api/auth.py (NOW write implementation)
from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.post("/api/auth/login")
async def login(email: str, password: str):
    """Minimal implementation - just make tests pass"""

    # Hardcoded for now (will refactor later)
    if email == "test@example.com" and password == "password123":
        return {
            "token": "fake-token-123",
            "user": {"email": email}
        }

    # Invalid credentials
    raise HTTPException(status_code=401, detail="Invalid credentials")
```

**Run tests:**
```bash
pytest tests/test_auth.py -v

# Expected: ✅ PASSED (2-3 tests passing)
```

#### 🔵 REFACTOR Phase:

```python
# app/api/auth.py (Refactor with production quality)
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.lib.logger import logger
from app.lib.auth import verify_password, create_jwt_token
from app.db import get_db
from app.models.user import User

router = APIRouter()

class LoginRequest(BaseModel):
    """Login request validation schema"""
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    """Login response schema"""
    token: str
    user: dict

@router.post("/api/auth/login", response_model=LoginResponse)
async def login(
    data: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Authenticate user and return JWT token.

    Raises:
        HTTPException 401: Invalid credentials
        HTTPException 500: Server error
    """

    # Log entry
    logger.info("api_route_entry", extra={
        "route": "/api/auth/login",
        "method": "POST",
        "email": data.email
    })

    try:
        # Query database
        result = await db.execute(
            select(User).where(User.email == data.email)
        )
        user = result.scalar_one_or_none()

        # Verify credentials
        if not user or not verify_password(data.password, user.hashed_password):
            logger.warning("login_failed", extra={
                "email": data.email,
                "reason": "invalid_credentials"
            })
            raise HTTPException(
                status_code=401,
                detail="Invalid credentials"
            )

        # Generate JWT token
        token = create_jwt_token(user.id)

        # Log success
        logger.info("login_success", extra={
            "user_id": user.id,
            "email": data.email
        })

        return LoginResponse(
            token=token,
            user={
                "id": user.id,
                "email": user.email,
                "name": user.name
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("login_error", extra={
            "error": str(e),
            "email": data.email
        })
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )
```

**Run tests:**
```bash
pytest tests/test_auth.py -v

# Expected: ✅ PASSED (all tests still passing!)
```

---

### TypeScript (Next.js + Vitest)

#### 🔴 RED Phase:

```typescript
// __tests__/api/auth.test.ts (WRITE THIS FIRST!)
import { describe, it, expect } from 'vitest'
import { POST } from '@/app/api/auth/login/route'

describe('POST /api/auth/login', () => {
  it('should return 200 and token for valid credentials', async () => {
    const request = new Request('http://localhost/api/auth/login', {
      method: 'POST',
      body: JSON.stringify({
        email: 'test@example.com',
        password: 'password123'
      })
    })

    const response = await POST(request)
    const data = await response.json()

    expect(response.status).toBe(200)
    expect(data).toHaveProperty('token')
    expect(data.user.email).toBe('test@example.com')
  })

  it('should return 401 for invalid credentials', async () => {
    const request = new Request('http://localhost/api/auth/login', {
      method: 'POST',
      body: JSON.stringify({
        email: 'wrong@example.com',
        password: 'wrongpass'
      })
    })

    const response = await POST(request)
    const data = await response.json()

    expect(response.status).toBe(401)
    expect(data.error).toMatch(/invalid/i)
  })

  it('should return 422 for missing email', async () => {
    const request = new Request('http://localhost/api/auth/login', {
      method: 'POST',
      body: JSON.stringify({
        password: 'password123'
        // Missing email
      })
    })

    const response = await POST(request)

    expect(response.status).toBe(422)
  })
})
```

**Run tests:**
```bash
vitest run __tests__/api/auth.test.ts

# Expected: ❌ FAILED (route doesn't exist)
```

#### 🟢 GREEN Phase:

```typescript
// app/api/auth/login/route.ts (NOW write implementation)
import { NextResponse } from 'next/server'

export async function POST(request: Request) {
  const body = await request.json()
  const { email, password } = body

  // Hardcoded for now (will refactor later)
  if (email === 'test@example.com' && password === 'password123') {
    return NextResponse.json({
      token: 'fake-token-123',
      user: { email }
    })
  }

  // Invalid credentials
  return NextResponse.json(
    { error: 'Invalid credentials' },
    { status: 401 }
  )
}
```

**Run tests:**
```bash
vitest run __tests__/api/auth.test.ts

# Expected: ✅ PASSED (2-3 tests passing)
```

#### 🔵 REFACTOR Phase:

```typescript
// app/api/auth/login/route.ts (Refactor with production quality)
import { NextResponse } from 'next/server'
import { z } from 'zod'
import { logger } from '@/lib/logger'
import { verifyPassword, createJwtToken } from '@/lib/auth'
import { prisma } from '@/lib/db'

const LoginSchema = z.object({
  email: z.string().email('Invalid email format'),
  password: z.string().min(8, 'Password must be at least 8 characters')
})

export async function POST(request: Request) {
  // Log entry
  logger.info('api_route_entry', {
    route: '/api/auth/login',
    method: 'POST'
  })

  try {
    // Parse and validate request
    const body = await request.json()
    const validation = LoginSchema.safeParse(body)

    if (!validation.success) {
      logger.warning('validation_error', {
        errors: validation.error.errors
      })
      return NextResponse.json(
        { error: 'Validation failed', details: validation.error.errors },
        { status: 422 }
      )
    }

    const { email, password } = validation.data

    // Query database
    const user = await prisma.user.findUnique({
      where: { email }
    })

    // Verify credentials
    if (!user || !(await verifyPassword(password, user.hashedPassword))) {
      logger.warning('login_failed', {
        email,
        reason: 'invalid_credentials'
      })
      return NextResponse.json(
        { error: 'Invalid credentials' },
        { status: 401 }
      )
    }

    // Generate JWT token
    const token = createJwtToken(user.id)

    // Log success
    logger.info('login_success', {
      userId: user.id,
      email: user.email
    })

    return NextResponse.json({
      token,
      user: {
        id: user.id,
        email: user.email,
        name: user.name
      }
    })

  } catch (error) {
    logger.error('login_error', {
      error: error instanceof Error ? error.message : 'Unknown error'
    })
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}
```

**Run tests:**
```bash
vitest run __tests__/api/auth.test.ts

# Expected: ✅ PASSED (all tests still passing!)
```

---

### JavaScript (Express + Jest)

#### 🔴 RED Phase:

```javascript
// __tests__/auth.test.js (WRITE THIS FIRST!)
const request = require('supertest')
const app = require('../app')

describe('POST /api/auth/login', () => {
  it('should return 200 and token for valid credentials', async () => {
    const response = await request(app)
      .post('/api/auth/login')
      .send({
        email: 'test@example.com',
        password: 'password123'
      })

    expect(response.status).toBe(200)
    expect(response.body).toHaveProperty('token')
    expect(response.body.user.email).toBe('test@example.com')
  })

  it('should return 401 for invalid credentials', async () => {
    const response = await request(app)
      .post('/api/auth/login')
      .send({
        email: 'wrong@example.com',
        password: 'wrongpass'
      })

    expect(response.status).toBe(401)
    expect(response.body.error).toMatch(/invalid/i)
  })
})
```

**Run tests:**
```bash
npm test -- auth.test.js

# Expected: ❌ FAILED (route doesn't exist)
```

#### 🟢 GREEN Phase:

```javascript
// routes/auth.js (NOW write implementation)
const express = require('express')
const router = express.Router()

router.post('/api/auth/login', (req, res) => {
  const { email, password } = req.body

  // Hardcoded for now (will refactor later)
  if (email === 'test@example.com' && password === 'password123') {
    return res.json({
      token: 'fake-token-123',
      user: { email }
    })
  }

  // Invalid credentials
  return res.status(401).json({ error: 'Invalid credentials' })
})

module.exports = router
```

**Run tests:**
```bash
npm test -- auth.test.js

# Expected: ✅ PASSED
```

#### 🔵 REFACTOR Phase:

```javascript
// routes/auth.js (Refactor with production quality)
const express = require('express')
const { z } = require('zod')
const logger = require('../lib/logger')
const { verifyPassword, createJwtToken } = require('../lib/auth')
const prisma = require('../lib/db')

const router = express.Router()

const LoginSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8)
})

router.post('/api/auth/login', async (req, res) => {
  // Log entry
  logger.info('api_route_entry', {
    route: '/api/auth/login',
    method: 'POST'
  })

  try {
    // Validate request
    const validation = LoginSchema.safeParse(req.body)
    if (!validation.success) {
      logger.warning('validation_error', { errors: validation.error.errors })
      return res.status(422).json({
        error: 'Validation failed',
        details: validation.error.errors
      })
    }

    const { email, password } = validation.data

    // Query database
    const user = await prisma.user.findUnique({ where: { email } })

    // Verify credentials
    if (!user || !(await verifyPassword(password, user.hashedPassword))) {
      logger.warning('login_failed', { email, reason: 'invalid_credentials' })
      return res.status(401).json({ error: 'Invalid credentials' })
    }

    // Generate JWT token
    const token = createJwtToken(user.id)

    // Log success
    logger.info('login_success', { userId: user.id, email: user.email })

    return res.json({
      token,
      user: {
        id: user.id,
        email: user.email,
        name: user.name
      }
    })

  } catch (error) {
    logger.error('login_error', { error: error.message })
    return res.status(500).json({ error: 'Internal server error' })
  }
})

module.exports = router
```

**Run tests:**
```bash
npm test -- auth.test.js

# Expected: ✅ PASSED (all tests still passing!)
```

---

## 🔀 TDD vs Test-Alongside

### When to Use TDD (Red-Green-Refactor):

**Use when `tdd_required: true`:**

| Scenario | Why TDD? |
|----------|----------|
| Authentication/authorization | Security-critical, complex logic |
| Payment processing | Financial data, zero tolerance for bugs |
| Database migrations | Schema changes affect entire system |
| Multi-step workflows | Complex state transitions |
| Business logic (calculations) | Need to verify correctness |

### When to Use Test-Alongside:

**Use when `tdd_required: false`:**

| Scenario | Why Test-Alongside? |
|----------|---------------------|
| Simple CRUD endpoints | Straightforward, low risk |
| Read-only queries | No side effects |
| Presentational UI | Visual, not logic-heavy |
| Static pages | No dynamic behavior |

### Test-Alongside Workflow:

```
1. Write implementation first
2. Write tests after
3. Run tests to verify
4. Refactor if needed
```

**Example:**

```python
# Step 1: Write implementation
@router.get("/api/users")
async def list_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    return {"users": [user.dict() for user in result.scalars().all()]}

# Step 2: Write tests
@pytest.mark.asyncio
async def test_list_users(client):
    response = await client.get("/api/users")
    assert response.status_code == 200
    assert "users" in response.json()
```

---

## 📊 Logging TDD Phases

### RED Phase Log:

```json
{
  "event": "tdd_red_phase",
  "task": "Implement POST /api/auth/login",
  "test_file": "tests/test_auth.py",
  "tests_written": 3,
  "status": "fail",
  "expected": "Tests should fail - endpoint not implemented yet"
}
```

### GREEN Phase Log:

```json
{
  "event": "tdd_green_phase",
  "task": "Implement POST /api/auth/login",
  "tests_passed": 2,
  "tests_failed": 1,
  "implementation": "app/api/auth.py",
  "status": "partial_pass",
  "note": "Minimal implementation complete, refactor needed"
}
```

### REFACTOR Phase Log:

```json
{
  "event": "tdd_refactor_phase",
  "task": "Implement POST /api/auth/login",
  "tests_passing": 3,
  "improvements": [
    "Added Pydantic validation schema",
    "Added database integration",
    "Added JWT token generation",
    "Added structured logging",
    "Added proper error handling"
  ],
  "status": "complete"
}
```

---

## 🎯 Quick Reference

### TDD Checklist:

```markdown
Before starting TDD workflow:

[ ] Verify `tdd_required: true` flag
[ ] Choose appropriate testing framework (Pytest, Vitest, Jest)
[ ] Read existing test patterns (search for similar tests)

🔴 RED Phase:
[ ] Write comprehensive test cases (success + errors + edge)
[ ] Run tests → verify they FAIL for right reason
[ ] Log RED phase completion

🟢 GREEN Phase:
[ ] Write minimal implementation (hardcoded OK)
[ ] Run tests → verify they PASS
[ ] Log GREEN phase completion

🔵 REFACTOR Phase:
[ ] Add error handling
[ ] Add logging (entry, success, error)
[ ] Add validation
[ ] Add type hints/comments
[ ] Run tests after EACH change → verify still PASS
[ ] Log REFACTOR phase completion

✅ Final:
[ ] All tests passing
[ ] Code quality high (error handling, logging, types)
[ ] Ready for handoff
```

---

## 🔗 See Also

- `task-analyzer.md` Step 2.6 - TDD classification logic (integrated with task analysis)
- `@/.claude/contexts/patterns/tdd-classification.md` - Full TDD classification patterns
- `validation-framework.md` - Agent validation requirements
- `context-loading-protocol.md` - How agents load testing frameworks
- `contexts/patterns/testing.md` - General testing patterns
