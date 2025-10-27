# Testing Strategy & TDD Methodology

**Red-Green-Refactor:** Write test → Watch it fail → Write code → Make it pass → Refactor

---

## Test-Driven Development (TDD)

### Automatic TDD Classification

**Orchestrator automatically determines if TDD is required based on task content.**

You don't decide. Orchestrator decides. Your job is to **follow the `tdd_required` flag**.

### When You Receive a Task

**Check the metadata from Orchestrator:**
```json
{
  "description": "Implement POST /api/auth/login",
  "type": "critical",
  "tdd_required": true,
  "workflow": "red-green-refactor",
  "reason": "API endpoint + authentication logic"
}
```

### Classification Rules (Orchestrator Logic)

✅ **TDD Required (`tdd_required: true`) for:**
- API mutations (POST, PUT, PATCH, DELETE)
- Business logic (calculations, transformations, validation)
- External service integrations (payment, email, SMS, storage)
- Data transformations (ETL, serialization, aggregations)
- Security operations (authentication, authorization, encryption)
- Complex UI logic (multi-step forms, state machines, accessibility)

⚠️ **Test-Alongside OK (`tdd_required: false`) for:**
- Simple GET endpoints (read-only)
- Presentational UI components
- Simple CRUD operations
- Configuration files
- Trivial utilities

**Note:** For full classification logic, see `@.claude/contexts/patterns/task-classification.md`

### TDD Workflow (Red-Green-Refactor)

**Use when:** `tdd_required: true`

```
1. RED Phase - Write the test first
   → Define expected behavior before implementation
   → Run test → MUST FAIL (proves test works)
   → Log: "tdd_red_phase"

2. GREEN Phase - Write minimal code
   → Just enough to make the test pass
   → Run test → MUST PASS
   → Log: "tdd_green_phase"

3. REFACTOR Phase - Improve code quality
   → Add logging for observability
   → Add error handling
   → Add documentation
   → Run test → MUST STILL PASS
   → Log: "tdd_refactor_phase"

4. Repeat
   → One test at a time
```

### Standard Workflow (Test-Alongside)

**Use when:** `tdd_required: false`

```
1. Write implementation first
2. Write tests to verify
3. Run tests → PASS
```

---

## Testing Layers

### 1. Unit Tests

**Purpose:** Test individual functions/modules in isolation

**Framework:** Vitest (JS/TS) | Pytest (Python)

#### TypeScript Example

```typescript
// __tests__/scoring.test.ts
import { describe, it, expect, vi } from 'vitest'
import { calculateDiscount } from '@/lib/pricing'
import { logger } from '@/lib/logger'

vi.mock('@/lib/logger')

describe('calculateDiscount', () => {
  it('applies 10% discount for members', () => {
    const result = calculateDiscount(100, { isMember: true })
    expect(result).toBe(90)

    expect(logger.info).toHaveBeenCalledWith(
      'discount_calculated',
      expect.objectContaining({
        originalPrice: 100,
        discount: 10,
        finalPrice: 90
      })
    )
  })

  it('no discount for non-members', () => {
    const result = calculateDiscount(100, { isMember: false })
    expect(result).toBe(100)
  })

  it('throws on invalid input', () => {
    expect(() => calculateDiscount(-1, {})).toThrow('Price must be positive')
  })
})
```

#### Python Example

```python
# tests/test_pricing.py
import pytest
from app.lib.pricing import calculate_discount
from unittest.mock import patch

@pytest.mark.parametrize("price,is_member,expected", [
    (100, True, 90),   # Member gets 10% discount
    (100, False, 100), # Non-member no discount
    (50, True, 45),    # Member discount on lower price
])
def test_calculate_discount(price, is_member, expected):
    result = calculate_discount(price, is_member=is_member)
    assert result == expected

def test_calculate_discount_invalid_price():
    with pytest.raises(ValueError, match="Price must be positive"):
        calculate_discount(-1, is_member=True)
```

**When to use:**
- Pure functions
- Business logic
- Data transformations
- Utility functions

---

### 2. Integration Tests

**Purpose:** Test multiple components working together

#### API Route Test (Next.js)

```typescript
// __tests__/api/items.test.ts
import { describe, it, expect, beforeEach } from 'vitest'
import { POST } from '@/app/api/items/route'

describe('POST /api/items', () => {
  it('creates item and returns 201', async () => {
    const request = new Request('http://localhost/api/items', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: 'Test Item',
        price: 99.99
      })
    })

    const response = await POST(request)
    const data = await response.json()

    expect(response.status).toBe(201)
    expect(data.id).toBeDefined()
    expect(data.name).toBe('Test Item')
  })

  it('returns 400 on validation error', async () => {
    const request = new Request('http://localhost/api/items', {
      method: 'POST',
      body: JSON.stringify({ name: '' }) // Missing price
    })

    const response = await POST(request)
    expect(response.status).toBe(400)
  })
})
```

#### API Test (FastAPI)

```python
# tests/test_api.py
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_item(client: AsyncClient):
    response = await client.post("/api/items", json={
        "name": "Test Item",
        "price": 99.99
    })

    assert response.status_code == 201
    data = response.json()
    assert data["id"] is not None
    assert data["name"] == "Test Item"

@pytest.mark.asyncio
async def test_create_item_validation_error(client: AsyncClient):
    response = await client.post("/api/items", json={
        "name": ""  # Invalid
    })

    assert response.status_code == 422  # Validation error
```

**When to use:**
- API routes
- Database operations
- External service integrations
- Multi-step workflows

---

### 3. E2E Tests (Playwright)

**Purpose:** Test complete user flows in real browser

```typescript
// e2e/checkout.spec.ts
import { test, expect } from '@playwright/test'

test('user completes checkout flow', async ({ page }) => {
  // Add item to cart
  await page.goto('/products')
  await page.click('button:text("Add to Cart")')

  // Go to cart
  await page.click('[href="/cart"]')
  await expect(page.locator('h1')).toContainText('Shopping Cart')

  // Proceed to checkout
  await page.click('button:text("Checkout")')

  // Fill shipping info
  await page.fill('#name', 'John Doe')
  await page.fill('#email', 'john@example.com')
  await page.fill('#address', '123 Main St')
  await page.click('button:text("Continue")')

  // Payment
  await page.fill('#cardNumber', '4242424242424242')
  await page.fill('#expiry', '12/25')
  await page.fill('#cvc', '123')
  await page.click('button:text("Pay Now")')

  // Verify order confirmation
  await expect(page.locator('h1')).toContainText('Order Confirmed')
  await expect(page.locator('[data-testid="order-number"]')).toBeVisible()
})

test('shows validation errors on empty form', async ({ page }) => {
  await page.goto('/checkout')
  await page.click('button:text("Continue")')

  await expect(page.locator('text=Name is required')).toBeVisible()
  await expect(page.locator('text=Email is required')).toBeVisible()
})
```

**When to use:**
- Complete user journeys
- Cross-browser compatibility
- UI/UX validation
- Critical paths

---

## Testing Best Practices

### DO:
- ✅ Test behavior, not implementation
- ✅ Write tests first for critical code (TDD)
- ✅ Mock external dependencies
- ✅ Use descriptive test names
- ✅ Test edge cases and error scenarios
- ✅ Keep tests fast (< 1s per test)
- ✅ Verify logging in tests

### DON'T:
- ❌ Test framework internals (React hooks, etc.)
- ❌ Test trivial code (getters/setters)
- ❌ Write flaky tests (time-dependent)
- ❌ Skip error case tests
- ❌ Commit failing tests

---

## Test Organization

### TypeScript/JavaScript
```
project/
├── __tests__/
│   ├── unit/
│   │   ├── lib/
│   │   │   ├── pricing.test.ts
│   │   │   └── validation.test.ts
│   │   └── utils/
│   │       └── formatters.test.ts
│   ├── integration/
│   │   ├── api/
│   │   │   ├── items.test.ts
│   │   │   └── users.test.ts
│   │   └── stores/
│   │       └── app-store.test.ts
│   └── e2e/
│       ├── checkout.spec.ts
│       └── auth.spec.ts
├── vitest.config.ts
└── playwright.config.ts
```

### Python
```
project/
├── tests/
│   ├── unit/
│   │   ├── test_pricing.py
│   │   └── test_validation.py
│   ├── integration/
│   │   ├── test_api.py
│   │   └── test_db.py
│   └── conftest.py (fixtures)
└── pytest.ini
```

---

## Coverage Guidelines

| Type | Target Coverage |
|------|----------------|
| Business Logic | 95%+ |
| API Routes | 90%+ |
| Utilities | 85%+ |
| UI Components | 70%+ |

---

## Quick Reference

### Vitest Commands
```bash
pnpm test                    # Run all tests
pnpm test -- --run          # Run without watch mode
pnpm test -- path/to/test   # Run specific test
pnpm test -- --coverage     # Run with coverage
```

### Pytest Commands
```bash
pytest                      # Run all tests
pytest -v                   # Verbose output
pytest tests/unit/          # Run specific directory
pytest --cov=app           # Run with coverage
pytest -k "test_create"    # Run tests matching pattern
```

### Playwright Commands
```bash
pnpm test:e2e              # Run E2E tests
pnpm test:e2e --ui         # Run with UI mode
pnpm test:e2e --debug      # Run with debugger
```

---

---

## Trust the Classification

**Orchestrator uses comprehensive pattern matching:**
- API endpoints (HTTP methods, routes)
- Business logic (calculations, validation)
- External integrations (Stripe, SendGrid, Twilio, S3, etc.)
- Data transformations (ETL, serialization)
- Security operations (auth, encryption)

**Your responsibility:**
1. Check `tdd_required` flag in task metadata
2. If `true` → Use Red-Green-Refactor workflow
3. If `false` → Use Test-Alongside workflow
4. Log each phase for observability

**Don't override the classification unless you find a clear error.**
If classification seems wrong, report to user for pattern refinement.

---

**💡 Remember:** Tests are documentation. Write tests that explain what your code does!
