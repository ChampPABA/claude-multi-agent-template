# Pre-Work Checklist (Shared by All Agents)

> **Version:** 2.0.0 (Claude 4.5 Optimized)
> **Purpose:** Single source of truth for pre-work validation

---

## Pre-Work Steps

Complete these steps before implementation to ensure alignment with project standards:

1. **Context Discovery** - Load project context via agent-discovery.md
2. **Pattern Loading** - Load relevant patterns for your agent type
3. **Validation Report** - Provide pre-implementation validation report
4. **Wait for Approval** - Proceed only after orchestrator validation

→ Details: `.claude/contexts/patterns/validation-framework.md` (agent-specific sections)

---

## Validation Report Template

```markdown
Pre-Implementation Validation

Project Context:
- Project: {name}
- Stack: {tech-stack}
- Package Manager: {pm} (from tech-stack.md)

Patterns Loaded:
- [ ] error-handling.md
- [ ] logging.md
- [ ] testing.md
- [ ] code-standards.md
- [ ] {agent-specific patterns}

Best Practices:
- [ ] {framework} best practices loaded (from Context7)

Ready to Implement:
- [ ] Task understood
- [ ] Dependencies identified
- [ ] Approach planned
```

---

## Why This Matters

Pre-work validation prevents:
- Misaligned implementations (wrong patterns, wrong style)
- Duplicate components (not searching existing code first)
- Wrong package manager usage (CI/CD breaks)
- Missing best practices (outdated patterns)

→ 80% of implementation issues caught at validation stage
