# Agent Boundaries (Shared Reference)

> **Purpose:** Clear boundaries prevent agents from doing wrong work

---

## Why Boundaries Matter

Without clear boundaries:
- Agents overlap work (duplicate effort)
- Wrong agent does wrong task (quality drops)
- Integration issues (mismatched interfaces)

With clear boundaries:
- Each agent focuses on specialty
- Clean handoffs between phases
- Higher quality output

---

## Agent Routing Quick Reference

| Task Type | Use Agent | Phase |
|-----------|-----------|-------|
| UI components (mock data) | uxui-frontend | 1 |
| API endpoints | backend | 2 |
| Database schemas/migrations | database | 2 |
| Contract validation | integration | 2.5 |
| Connect UI to API | frontend | 3 |
| Tests, bugs, debugging | test-debug | 1,3,4 |

---

## Boundary Violations to Avoid

**uxui-frontend:**
- Uses mock data with setTimeout
- Connect to real APIs → use frontend agent instead

**frontend:**
- Connects existing UI to real APIs
- Create new UI from scratch → use uxui-frontend instead

**backend:**
- Creates API endpoints with validation
- Write database queries directly → use database agent instead

**database:**
- Creates schemas, migrations, typed queries
- Write API logic → use backend agent instead

---

## Why Agent Specialization Works

Each agent has deep context for its domain:
- uxui-frontend: Design patterns, accessibility, visual consistency
- backend: Security patterns, validation, error handling
- database: Query optimization, indexes, relationships
- integration: Contract validation, type safety
- frontend: State management, API integration, error UI
- test-debug: Test patterns, debugging, coverage

→ Full routing rules: `.claude/lib/agent-router.md`
