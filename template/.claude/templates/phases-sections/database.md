# Phase: Database Schema

**Agent:** `database`
**Metadata:** `| prisma | migration |`
**Estimated time:** 30 minutes

## 🎯 Purpose

Design database schema, create migrations, add indexes for performance.

## 📚 Context Loading

- ✅ `tech-stack.md` → Database ORM (Prisma, SQLAlchemy, etc.)
- ✅ `../proposal.md` → Data requirements
- ✅ Best practices for ORM

## 📝 Tasks

1. Design Prisma/SQLAlchemy schema
2. Create migration
3. Add indexes for frequently queried fields
4. Add foreign keys and constraints

## ✅ Success Criteria

- [ ] Schema designed and created
- [ ] Migration created and applied
- [ ] Indexes added for performance
- [ ] No migration conflicts

## 📤 Output

- Schema file (schema.prisma / models.py)
- Migration files
- Update flags.json
