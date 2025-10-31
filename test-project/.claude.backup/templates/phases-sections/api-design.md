# Phase: API Specification

**Agent:** `integration`
**Metadata:** `| api-design |`
**Estimated time:** 30 minutes

## 🎯 Purpose

Create OpenAPI 3.0 specification for all API endpoints. Define request/response schemas, validation rules, and error responses.

## 📚 Context Loading

- ✅ `../proposal.md` → Business requirements
- ✅ `../tasks.md` → API endpoints to implement
- ✅ Frontend mockup code → Data requirements
- ⚠️ `error-handling.md` → API error patterns

## 📝 Tasks

1. Analyze frontend mockup → Determine data needs
2. Design API endpoints (RESTful)
3. Define request/response schemas (JSON Schema)
4. Define error responses (4xx, 5xx)
5. Create OpenAPI 3.0 spec file

## ✅ Success Criteria

- [ ] OpenAPI 3.0 spec complete
- [ ] All endpoints documented
- [ ] Request/response schemas defined with examples
- [ ] Error responses defined

## 📤 Output

- `.claude/openapi.yaml` (OpenAPI 3.0 spec)
- API documentation (Swagger UI / Redoc)
- Update flags.json
