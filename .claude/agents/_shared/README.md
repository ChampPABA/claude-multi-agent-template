# Shared Agent Components

> **Version:** 2.0.0 (Claude 4.5 Optimized)
> **Purpose:** Single source of truth for content shared across all 6 agents

---

## Why This Exists

**Before v2.0.0:**
- Same content duplicated 6 times (once per agent)
- ~3,000 tokens wasted on duplication
- Updates required changing 6 files

**After v2.0.0:**
- Shared content in `_shared/` folder
- Agents reference with 1-line link
- ~2,500 tokens saved (83% reduction)
- Updates require changing 1 file

---

## Files in This Folder

| File | Purpose | Token Savings |
|------|---------|---------------|
| `pre-work-checklist.md` | Validation before implementation | ~200 tokens × 6 |
| `package-manager.md` | Package manager protocol | ~100 tokens × 6 |
| `documentation-policy.md` | What files agents can create | ~70 tokens × 6 |
| `agent-boundaries.md` | When to use which agent | ~80 tokens × 6 |

---

## How Agents Reference

Instead of duplicating content, agents use:

```markdown
## Pre-Work Checklist
→ See `.claude/agents/_shared/pre-work-checklist.md`
```

This approach:
- Saves tokens (1 line vs 30 lines)
- Ensures consistency (single source of truth)
- Simplifies maintenance (update once)

---

## Claude 4.5 Optimization Notes

These files follow Claude 4.5 best practices:

1. **Professional tone** - No aggressive CAPS or threats
2. **Positive instructions** - "Use X" instead of "Don't use Y"
3. **WHY context** - Each rule explains its purpose
4. **Concise format** - Tables and bullet points, not prose
