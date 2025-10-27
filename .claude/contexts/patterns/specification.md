# Specification & Change Management

**Goal:** Track what your system can do, plan changes safely, and maintain living documentation.

---

## What is OpenSpec?

OpenSpec is a **lightweight specification framework** for tracking system capabilities and planning changes.

**Key Concepts:**
- **Specs** - What your system CAN do (living documentation)
- **Changes** - What you PLAN to add/modify (proposals before coding)
- **Requirements** - Individual capabilities (testable, verifiable)

**Think of it as:**
- Git for code → OpenSpec for capabilities
- Issue tracker for bugs → OpenSpec for features

---

## Directory Structure

```
project/
├── openspec/
│   ├── specs/                    # Current capabilities (WHAT system does)
│   │   ├── user-auth/
│   │   │   └── spec.md           # Requirement 1, 2, 3...
│   │   ├── payment-api/
│   │   │   └── spec.md
│   │   └── email-service/
│   │       └── spec.md
│   ├── changes/                  # Proposed changes (WHAT you plan)
│   │   ├── add-oauth/
│   │   │   ├── proposal.md       # Why, what, impact
│   │   │   ├── tasks.md          # Implementation checklist
│   │   │   ├── design.md         # Architecture (if complex)
│   │   │   └── specs/
│   │   │       └── oauth/
│   │   │           └── spec.md   # New/updated requirements
│   │   └── archive/              # Completed changes
│   └── AGENTS.md                 # OpenSpec workflow guide
```

---

## When to Use OpenSpec

### ✅ USE OpenSpec for:

1. **New Features** - Adding capabilities to the system
2. **Breaking Changes** - Modifying existing behavior
3. **Architecture Changes** - Refactoring major components
4. **API Changes** - Adding/modifying endpoints
5. **Database Schema Changes** - Adding/modifying models
6. **Major Performance Work** - Optimization that affects behavior
7. **Security Enhancements** - Auth, authorization, encryption changes

### ❌ SKIP OpenSpec for:

1. **Bug Fixes** - Restoring spec behavior
2. **Typos/Formatting** - Non-functional changes
3. **Documentation Updates** - README, comments
4. **Non-breaking Dependency Updates** - Library version bumps
5. **Configuration Changes** - .env, config files

---

## Workflow

### Phase 1: Planning (Before Coding)

```
1. Check for conflicts
   → Run: openspec list
   → Run: openspec list --specs
   → Ensure no overlapping work

2. Create change proposal
   → mkdir -p openspec/changes/[change-id]/specs/[capability]
   → Write: proposal.md (why, what, impact)
   → Write: tasks.md (implementation plan)
   → Write: design.md (if complex architecture)
   → Write: specs/[capability]/spec.md (requirements)

3. Validate proposal
   → Run: openspec validate [change-id] --strict
   → Fix all validation errors
   → Re-run until valid

4. Get approval
   → Wait for team/user approval
   → DO NOT code yet!
```

---

### Phase 2: Implementation (After Approval)

```
5. Implement following tasks.md
   → Use 4-phase methodology (MVT → Complexity → Scale → Deploy)
   → Mark tasks complete as you go
   → Update tasks.md with progress

6. Test thoroughly
   → Unit tests (TDD for critical paths)
   → Integration tests
   → E2E tests
   → Performance tests

7. Validate again
   → Run: openspec validate [change-id] --strict
   → Ensure all requirements implemented
```

---

### Phase 3: Completion (After Testing)

```
8. Archive change
   → Run: openspec archive [change-id]
   → Moves specs to openspec/specs/
   → Moves change to openspec/changes/archive/

9. Commit and deploy
   → git add .
   → git commit -m "feat: [description]"
   → git push
```

---

## proposal.md Template

```markdown
# Proposal: [Change Title]

## Why (Business Justification)

**Problem:** [What problem are we solving?]

**User Impact:** [How does this help users?]

**Business Value:** [Revenue, cost savings, user satisfaction?]

## What (Solution Overview)

**Approach:** [High-level solution]

**Capabilities Added:**
- Capability 1: [Description]
- Capability 2: [Description]

**Capabilities Modified:**
- Capability X: [What changes]

**Capabilities Removed:**
- Capability Y: [Why removing]

## Impact Analysis

**Breaking Changes:** [Yes/No - If yes, explain]

**Database Migrations:** [Required/Not Required]

**API Changes:** [New endpoints, modified responses]

**Dependencies:** [New libraries, services]

**Performance:** [Expected impact on latency, throughput]

**Security:** [New attack surfaces, mitigations]

## Success Criteria

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Risk 1 | Low/Med/High | Low/Med/High | How to handle |

## Alternatives Considered

**Option A:** [Description] - **Rejected because:** [Reason]

**Option B:** [Description] - **Rejected because:** [Reason]
```

---

## tasks.md Template

```markdown
# Tasks: [Change Title]

Implementation broken down into 4 phases following TDD methodology.

## Phase 1: MVT (Minimum Viable Test)

**Goal:** Single item, prove concept works

### Task 1.1: [First Component] (TDD Test-First if critical)

**If TDD Required:**

#### 1.1.1: [Method/Feature] (TDD Cycle)

**Red Phase:**
- [ ] Write test: "should [expected behavior]"
- [ ] Run test → Verify FAILS
- [ ] Log: `test_written`, `testName: "[name]"`

**Green Phase:**
- [ ] Implement MINIMAL code
- [ ] Run test → Verify PASSES
- [ ] Log: `test_passed`

**Refactor Phase:**
- [ ] Add error handling
- [ ] Add logging: `logger.info('[event]')`
- [ ] Run test → Verify still PASSES

---

### Task 1.2: [Second Component]
- [ ] Subtask 1
- [ ] Subtask 2
- [ ] Test with 1 item → Verify works

---

## Phase 2: Complexity

**Goal:** Add validation, error handling (2-3 items)

### Task 2.1: Add Validation
- [ ] Zod/Pydantic schemas
- [ ] Input validation
- [ ] Test invalid inputs

### Task 2.2: Add Error Handling
- [ ] try-catch blocks
- [ ] Custom error classes
- [ ] Logging all errors

### Task 2.3: Test with 2-3 Items
- [ ] Valid inputs
- [ ] Invalid inputs
- [ ] Edge cases

---

## Phase 3: Scale

**Goal:** Full implementation (5-15 items)

### Task 3.1: Implement Full Feature
- [ ] All items/entities
- [ ] Complete workflows
- [ ] Integration tests

### Task 3.2: Performance Optimization
- [ ] Pagination
- [ ] Caching
- [ ] Database indexes

---

## Phase 4: Deploy

**Goal:** Production readiness

### Task 4.1: E2E Tests
- [ ] Complete user flows
- [ ] Cross-browser testing

### Task 4.2: Performance Testing
- [ ] API latency < 200ms (p95)
- [ ] Page load time < 2s

### Task 4.3: Documentation
- [ ] README updated
- [ ] API docs (OpenAPI)
- [ ] JSDoc comments

### Task 4.4: Code Review Checklist
- [ ] All tests passing
- [ ] Test coverage > 80%
- [ ] All operations logged
- [ ] Type safety (no 'any')
- [ ] No console.log statements

### Task 4.5: OpenSpec Validation
- [ ] Run: openspec validate --strict
- [ ] Fix all errors

### Task 4.6: Deployment Checklist
- [ ] Environment variables
- [ ] Database migrations
- [ ] CI/CD configured

### Task 4.7: Cleanup
- [ ] Remove temp files
- [ ] Remove commented code
- [ ] Run lint
```

---

## spec.md Template

```markdown
# [Capability Name] Specification

**Capability ID:** `[kebab-case-name]`
**Status:** Active
**Last Updated:** YYYY-MM-DD

---

## Overview

[Brief description of what this capability does]

---

## Requirements

### REQ-1: [Requirement Title]

**Description:** [What this requirement does]

**Acceptance Criteria:**
- [ ] Criterion 1
- [ ] Criterion 2

**Scenarios:**
- **Given** [initial state]
- **When** [action]
- **Then** [expected result]

**Error Handling:**
- Invalid input → 400 Bad Request
- Not found → 404 Not Found
- Server error → 500 Internal Server Error

**Logging:**
- Success: `logger.info('[event]', { context })`
- Error: `logger.error('[event]', { error, context })`

**Tests:**
- Unit: `tests/unit/[feature].test.ts`
- Integration: `tests/integration/[feature].test.ts`

---

### REQ-2: [Another Requirement]

[Same structure as REQ-1]

---

## Dependencies

**Internal:**
- `lib/logger.ts` (logging)
- `lib/db.ts` (database)

**External:**
- `@prisma/client` (ORM)
- `zod` (validation)

---

## API Endpoints (if applicable)

### POST /api/[endpoint]

**Request:**
```json
{
  "field1": "value1",
  "field2": "value2"
}
```

**Response (200):**
```json
{
  "id": "uuid",
  "field1": "value1",
  "createdAt": "ISO-8601"
}
```

**Errors:**
- 400 - Validation failed
- 409 - Duplicate entry
- 500 - Server error

---

## Database Schema (if applicable)

```prisma
model Entity {
  id        String   @id @default(uuid())
  field1    String
  field2    Int
  createdAt DateTime @default(now())

  @@map("entities")
}
```

---

## Performance Targets

- API Response Time: < 200ms (p95)
- Database Query Time: < 50ms (p95)
- Page Load Time: < 2s

---

## Security Considerations

- Input validation (Zod/Pydantic)
- SQL injection prevention (Prisma/SQLAlchemy)
- XSS prevention (sanitization)
- CSRF protection (tokens)

---

## Known Limitations

- Limitation 1: [Description]
- Limitation 2: [Description]
```

---

## OpenSpec Commands

```bash
# List active changes
openspec list

# List all specs
openspec list --specs

# Show change details
openspec show [change-id]

# Show change as JSON
openspec show [change-id] --json

# Show only deltas (changes)
openspec show [change-id] --json --deltas-only

# Validate change
openspec validate [change-id]

# Validate strictly (all checks)
openspec validate [change-id] --strict

# Validate all changes
openspec validate --all

# Archive change
openspec archive [change-id]

# Update OpenSpec CLI
openspec update
```

---

## Best Practices

### DO:
- ✅ Create proposal BEFORE coding
- ✅ Validate with `--strict` flag
- ✅ Write testable requirements
- ✅ Use 4-phase methodology in tasks.md
- ✅ Archive changes after deployment
- ✅ Keep specs up-to-date

### DON'T:
- ❌ Code before proposal approval
- ❌ Skip validation
- ❌ Write vague requirements
- ❌ Leave changes unarchived
- ❌ Forget to update specs after changes

---

## Example: Add User Authentication

```
openspec/changes/add-user-auth/
├── proposal.md           # Why: Users need login
├── tasks.md              # 4-phase plan (MVT → Deploy)
├── design.md             # JWT tokens, bcrypt hashing
└── specs/
    └── user-auth/
        └── spec.md       # REQ-1: Login, REQ-2: Signup, REQ-3: Logout
```

**After implementation:**
```
openspec archive add-user-auth
→ Moves specs/user-auth/ to openspec/specs/user-auth/
→ Moves add-user-auth/ to openspec/changes/archive/
```

---

**💡 Remember:** Spec first, code second. Plan carefully, implement confidently!
