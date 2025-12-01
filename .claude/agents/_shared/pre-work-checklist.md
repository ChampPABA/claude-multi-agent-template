# Pre-Work Checklist (Shared by All Agents)

> **Version:** 2.1.2 (Instruction-based Library Detection)
> **Purpose:** Single source of truth for pre-work validation

---

## Pre-Work Steps

Complete these steps before implementation to ensure alignment with project standards:

### Step 0: Library Requirements Check

**Scan for required libraries before writing code:**

1. **Read `tasks.md`** - Look for these patterns:
   - `Install X and dependencies` → Use library X
   - `Configure X with Y adapter` → Use X with adapter Y
   - Backtick packages like `better-auth` → Required dependency

2. **Read `design.md`** - Look for these patterns:
   - `### D1: Use X Library` → Decision to use X
   - `**Decision:** Use X` → Chosen library
   - Alternatives table → Shows why X was chosen over others

3. **List required libraries** in your validation report

4. **Use the libraries specified in tasks.md/design.md**
   - WHY: The team chose these libraries for specific reasons (compatibility, features, constraints)
   - Custom implementations waste effort and may miss edge cases the library handles

**Example:**
```
tasks.md says: "Install better-auth and dependencies"
→ Use better-auth library
→ Follow better-auth documentation patterns

WHY not custom? better-auth handles OAuth flows, session management, 
and security edge cases that custom code would need to re-implement.
```

---

### Step 1-4: Standard Checks

1. **Context Discovery** - Load project context via agent-discovery.md
2. **Pattern Loading** - Load relevant patterns for your agent type
3. **Validation Report** - Provide pre-implementation validation report
4. **Wait for Approval** - Proceed only after orchestrator validation

→ Details: `.claude/contexts/patterns/validation-framework.md` (agent-specific sections)

---

## Validation Report Template

```markdown
Pre-Implementation Validation

Library Requirements: (Step 0)
- [ ] Scanned tasks.md for "Install X" patterns
- [ ] Scanned design.md for design decisions
- Required libraries: {list from tasks.md/design.md}

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
- [ ] Required libraries identified
- [ ] Approach planned (using specified libraries)
```

---

## Why This Matters

Pre-work validation prevents:
- **Wrong library choices** - Using custom code when a library was already chosen by the team
- Misaligned implementations (wrong patterns, wrong style)
- Duplicate components (not searching existing code first)
- Wrong package manager usage (CI/CD breaks)
- Missing best practices (outdated patterns)

→ 80% of implementation issues are caught at validation stage
