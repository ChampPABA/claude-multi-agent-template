# Tier 1: Core Contexts (Always Load)

These files contain **foundational knowledge** that ALL agents should load at the start of every task.

## Files

| File | Purpose | Size |
|------|---------|------|
| `development-principles.md` | SOLID, DRY, KISS, YAGNI, Fail Fast | ~500 lines |
| `code-standards.md` | Naming conventions, formatting, structure | ~400 lines |

## Why These Are Tier 1

1. **Universal applicability** - Every agent (UI, backend, database, test) needs these principles
2. **Foundation for quality** - Violations of these principles cause bugs and tech debt
3. **Small enough** - ~900 lines total, acceptable baseline cost

## Loading

Agents should load these files in **STEP 0** before any task-specific work:

```markdown
## STEP 0: Load Core Contexts

Read and apply principles from:
1. @/.claude/contexts/_core/development-principles.md
2. @/.claude/contexts/_core/code-standards.md
```

## See Also

- **Tier 2** (Agent-Specific): `patterns/`, `design/` - loaded based on agent role
- **Tier 3** (On-Demand): queried when specific topics arise
