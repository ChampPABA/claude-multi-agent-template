# Phase: Backend Implementation

**Agent:** `backend`
**Metadata:** `| TDD | api-work | production |`
**Estimated time:** 120 minutes

## 🎯 Purpose

Implement API endpoints following OpenAPI specification. Include business logic, validation, error handling, and logging.

## 📚 Context Loading

- ✅ `tech-stack.md` → Package manager, framework version
- ✅ `.claude/openapi.yaml` → API contract
- ✅ `testing.md` (RED-GREEN-REFACTOR section)
- ✅ `error-handling.md` → API error patterns
- ✅ `logging.md` → Production logging

## 📝 Follow TDD (RED → GREEN → REFACTOR)

1. **RED:** Write failing tests first
2. **GREEN:** Implement to pass tests
3. **REFACTOR:** Clean up code

## ✅ Success Criteria

- [ ] All endpoints implemented (match OpenAPI spec)
- [ ] All tests pass (TDD: RED → GREEN → REFACTOR)
- [ ] Error handling implemented
- [ ] Logging added
- [ ] Code coverage ≥ 80%

## 📤 Output

- API routes files
- Tests files
- Update flags.json
