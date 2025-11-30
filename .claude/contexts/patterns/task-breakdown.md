# Task Breakdown Methodology

**Core Principle:** Small → Test → Fix → Scale → Deploy (Incremental Development)

---

## 4-Phase Methodology

Start small and iterate. This approach catches bugs early and reduces rework.

**Progression:**

1. **Phase 1: MVT (Minimum Viable Test)** - Start small (1 item)
2. **Phase 2: Complexity** - Add validation and edge cases (2-3 items)
3. **Phase 3: Scale** - Full implementation (5-15 items)
4. **Phase 4: Deploy** - Production readiness and monitoring

---

## Phase 1: MVT (Minimum Viable Test)

**Goal:** Prove the concept works with **1 simple case** before scaling

### Characteristics

- ✅ **Single item/entity** (1 question, 1 user, 1 product)
- ✅ **Happy path only** (no edge cases yet)
- ✅ **Minimal validation** (basic checks only)
- ✅ **Quick iteration** (< 1 hour to complete)
- ✅ **Logged** (basic observability)

### Example: E-commerce Product Creation

**❌ Wrong Approach (jumping to scale):**
```
Task: Implement product creation with:
- 5 categories
- 10 fields per product
- Image uploads
- Price validation
- Inventory management
```

**✅ Correct MVT (Phase 1):**
```
Task 1.1: Create single product with 2 fields (name, price)
Task 1.2: Test with 1 product → Verify database insert
Task 1.3: Log operation (product_created event)
```

### Example: IELTS Audio Recording

**❌ Wrong:**
```
Implement Part 1, 2, 3 with all questions
```

**✅ Correct MVT:**
```
Task 1.1: Record 1 question (Part 1, Question 1)
Task 1.2: Submit audio to API
Task 1.3: Get score and display
```

---

## Phase 2: Complexity

**Goal:** Add validation, error handling, and edge cases with **2-3 items**

### Characteristics

- ✅ **2-3 items/entities** (2-3 questions, 2-3 products)
- ✅ **Input validation** (Zod/Pydantic schemas)
- ✅ **Error handling** (try-catch with specific errors)
- ✅ **Edge cases** (empty input, duplicates, invalid data)
- ✅ **Comprehensive logging** (errors + success paths)

### Example: E-commerce Product Creation

```
Phase 2: Complexity (2-3 products)

Task 2.1: Add Zod validation schema
- name: min 3 chars, max 100 chars
- price: positive number, max 2 decimals
- Test with invalid inputs (empty name, negative price)

Task 2.2: Add error handling
- Duplicate product name → 409 Conflict
- Invalid input → 400 Bad Request
- Database error → 500 Internal Server Error

Task 2.3: Test with 2-3 products
- Valid products
- Duplicate names
- Invalid prices

Task 2.4: Add logging
- product_validation_error
- product_duplicate_error
- product_created_success
```

### Example: IELTS Audio Recording

```
Phase 2: Complexity (2-3 questions)

Task 2.1: Add audio validation
- Duration: 30-45s for Part 1
- File size: < 1.5 MB
- MIME type: audio/webm, audio/mp3

Task 2.2: Add error handling
- Permission denied → Show clear message
- File too large → Show size limit
- Network error → Retry logic

Task 2.3: Test with 2-3 questions
- Valid recordings
- Too short (<30s)
- Too long (>45s)
- Permission denied

Task 2.4: Add comprehensive logging
```

---

## Phase 3: Scale

**Goal:** Full implementation with **5-15 items** and complete workflows

### Characteristics

- ✅ **Full scale** (all questions, all products, all features)
- ✅ **Complete workflows** (entire user journey)
- ✅ **Performance optimization** (pagination, caching)
- ✅ **Integration tests** (end-to-end flows)
- ✅ **Production-like data** (realistic volumes)

### Example: E-commerce Product Catalog

```
Phase 3: Scale (Full catalog)

Task 3.1: Implement all product categories (5-10 categories)
Task 3.2: Add all product fields (name, price, description, images, inventory)
Task 3.3: Add image upload to cloud storage
Task 3.4: Add pagination (20 products per page)
Task 3.5: Add filtering (by category, price range)
Task 3.6: Add sorting (by price, date, name)
Task 3.7: Integration tests (create → list → filter → update → delete)
Task 3.8: Performance testing (100+ products)
```

### Example: IELTS Complete Test

```
Phase 3: Scale (All 3 parts)

Task 3.1: Implement Part 1 (5 questions)
Task 3.2: Implement Part 2 (1 long turn with cue card)
Task 3.3: Implement Part 3 (5-6 discussion questions)
Task 3.4: Add progress tracking (current part, question number)
Task 3.5: Add timer per part
Task 3.6: Add session state management
Task 3.7: Integration tests (Part 1 → Part 2 → Part 3 → Complete)
Task 3.8: Performance testing (audio processing latency)
```

---

## Phase 4: Deploy (Production Readiness)

**Goal:** Monitoring, documentation, cleanup, and deployment

### Characteristics

- ✅ **E2E tests** (complete user flows in real browser)
- ✅ **Performance benchmarks** (latency, throughput)
- ✅ **Documentation** (README, API docs, JSDoc)
- ✅ **Code review checklist** (standards, best practices)
- ✅ **Error monitoring** (Sentry, LogRocket)
- ✅ **Deployment checklist** (env vars, migrations)
- ✅ **Cleanup** (remove temp files, commented code)

### Standard Phase 4 Tasks

```
Phase 4: Production Readiness

Task 4.1: E2E Tests (Playwright)
- Complete user journey (signup → login → use feature → logout)
- Edge cases (network errors, timeouts)
- Cross-browser (Chrome, Firefox, Safari)

Task 4.2: Performance Testing
- API response time < 200ms (p95)
- Page load time < 2s
- Database query optimization (N+1 prevention)

Task 4.3: Browser Compatibility
- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

Task 4.4: Error Monitoring Setup
- Sentry integration (frontend + backend)
- Error tracking dashboard
- Alert thresholds (>10 errors/minute)

Task 4.5: Documentation
- README.md (setup, usage, deployment)
- API documentation (OpenAPI/Swagger)
- JSDoc comments on public APIs

Task 4.6: Code Review Checklist
- ✅ All tests passing (unit + integration + E2E)
- ✅ Test coverage > 85%
- ✅ All operations logged
- ✅ Type safety (no 'any' types)
- ✅ No console.log statements (use logger)
- ✅ Error handling for all async operations

Task 4.7: OpenSpec Validation (if applicable)
- Run: openspec validate --strict
- Fix all validation errors
- Archive change proposal

Task 4.8: Deployment Checklist
- Environment variables configured
- Database migrations applied
- CI/CD pipeline configured
- Rollback plan documented

Task 4.9: Cleanup
- Remove temporary files (test-*.ts, debug-*.js)
- Remove commented code
- Remove unused imports
- Run lint and fix all errors
```

---

## TDD Strategy

### When to Use TDD (REQUIRED)

✅ **Use TDD Test-First for critical code:**
- Business logic (calculations, transformations)
- API endpoints (validation, error handling)
- External service integrations
- Data transformations
- Complex algorithms

⚠️ **Test-Alongside OK for:**
- Simple CRUD operations
- UI components (presentational)
- Configuration files
- Trivial utilities

### TDD Workflow (Red-Green-Refactor)

```
1. RED Phase - Write the test first
   → Define expected behavior before implementation
   → Run test → Verify it FAILS

2. GREEN Phase - Write minimal code
   → Just enough to make the test pass
   → Run test → Verify it PASSES

3. REFACTOR Phase - Improve the code
   → Add logging
   → Add error handling
   → Optimize performance
   → Run test → Verify still PASSES

4. REPEAT - One test at a time
```

### TDD Example: Calculate Band Score

**Red Phase:**
```typescript
// tests/unit/scoring.test.ts
import { describe, it, expect } from 'vitest'
import { calculateBandScore } from '@/lib/scoring'

describe('calculateBandScore', () => {
  it('should convert 85% to IELTS 7.5', () => {
    const result = calculateBandScore(85)
    expect(result).toBe(7.5)
  })
})

// Run test → FAILS (function doesn't exist yet)
```

**Green Phase:**
```typescript
// lib/scoring.ts
export function calculateBandScore(speechaceScore: number): number {
  // Minimal implementation (hardcoded for now)
  return 7.5
}

// Run test → PASSES
```

**Refactor Phase:**
```typescript
// lib/scoring.ts
import { logger } from '@/lib/logger'

export function calculateBandScore(speechaceScore: number): number {
  // Proper implementation
  const bandScore = Math.round((speechaceScore / 100) * 9 * 2) / 2

  // Add logging
  logger.info('band_score_calculated', {
    speechaceScore,
    bandScore
  })

  return bandScore
}

// Run test → PASSES
```

**Add More Tests:**
```typescript
it('should convert 60% to IELTS 5.5', () => {
  expect(calculateBandScore(60)).toBe(5.5)
})

it('should throw on invalid input', () => {
  expect(() => calculateBandScore(-1)).toThrow('Invalid score')
  expect(() => calculateBandScore(101)).toThrow('Invalid score')
})
```

---

## Task Breakdown Examples

### Example 1: User Authentication

**❌ Wrong (monolithic):**
```
Task: Implement complete authentication system
- Login, signup, forgot password, email verification
- OAuth (Google, GitHub)
- 2FA
- Session management
```

**✅ Correct (4-phase):**
```
Phase 1: MVT (1 user)
- Task 1.1: Login with email/password (1 user)
- Task 1.2: Session creation
- Task 1.3: Protected route check

Phase 2: Complexity (2-3 users)
- Task 2.1: Add validation (email format, password strength)
- Task 2.2: Error handling (invalid credentials, expired session)
- Task 2.3: Test with 2-3 users (valid, invalid, edge cases)

Phase 3: Scale (Full features)
- Task 3.1: Signup flow
- Task 3.2: Forgot password
- Task 3.3: Email verification
- Task 3.4: Session persistence (cookies, localStorage)

Phase 4: Deploy
- Task 4.1: E2E tests (signup → login → protected route)
- Task 4.2: Security audit (SQL injection, XSS)
- Task 4.3: Documentation (API endpoints, error codes)
```

---

### Example 2: Search Functionality

**❌ Wrong:**
```
Task: Implement search with filters, sorting, pagination
```

**✅ Correct:**
```
Phase 1: MVT (1 result)
- Task 1.1: Basic search (exact match, 1 result)
- Task 1.2: Display result

Phase 2: Complexity (2-3 results)
- Task 2.1: Fuzzy matching
- Task 2.2: Highlighting search terms
- Task 2.3: Empty state handling

Phase 3: Scale (100+ results)
- Task 3.1: Pagination (20 per page)
- Task 3.2: Filters (category, price, date)
- Task 3.3: Sorting (relevance, price, date)
- Task 3.4: Performance optimization (debounce, caching)

Phase 4: Deploy
- Task 4.1: E2E tests (search → filter → sort → paginate)
- Task 4.2: Performance testing (1000+ results)
- Task 4.3: Analytics (search queries, click-through rates)
```

---

## Quick Reference

| Phase | Items | Focus | Duration |
|-------|-------|-------|----------|
| **Phase 1: MVT** | 1 | Prove concept | < 1 hour |
| **Phase 2: Complexity** | 2-3 | Validation + errors | 1-2 hours |
| **Phase 3: Scale** | 5-15 | Full implementation | 3-5 hours |
| **Phase 4: Deploy** | N/A | Production readiness | 2-3 hours |

---

## Best Practices

### DO:
- ✅ Start with 1 item (MVT)
- ✅ Test after each phase
- ✅ Log every significant action
- ✅ Use TDD for critical paths
- ✅ Add validation in Phase 2
- ✅ Scale to full implementation in Phase 3
- ✅ Complete all Phase 4 tasks before deploying

### DON'T:
- ❌ Jump straight to full scale
- ❌ Skip validation
- ❌ Skip error handling
- ❌ Skip logging
- ❌ Skip tests
- ❌ Deploy without Phase 4 checklist

---

**💡 Remember:** If you can't test it with 1 item, you can't scale it to 100!
