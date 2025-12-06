# Context Optimization (v1.2.0)

> **Detailed guide to token-efficient loading strategies**
> **Source:** Extracted from CLAUDE.md (Navigation Hub)
> **Version:** 1.4.0

---

## ⚡ The Problem: Token Waste

**Before v1.2.0:**
```
/pageplan     → reads data.yaml (~800 tokens)
/csetup       → reads data.yaml (~800 tokens)
/cdev         → sends data.yaml (~800 tokens)
uxui-frontend → reads data.yaml (~800 tokens)
────────────────────────────────────────────────
Total: ~20K tokens (same content read 4 times!)
```

**After v1.2.0:**
```
/designsetup  → generates data.yaml (~500 tokens) ✅
/pageplan     → reads data.yaml (~500 tokens) ✅
/csetup       → validates files exist (0 tokens) ✅
/cdev         → sends reference only (~200 tokens) ✅
uxui-frontend → reads data.yaml (~800 tokens) ✅
────────────────────────────────────────────────
Total: ~4.7K tokens (70% reduction!) ✨
```

---

## The Solution: 3-Tier Loading

### Tier 1: data.yaml (500 tokens)

- Lightweight design tokens only
- Used by: /pageplan, /csetup, agents
- Contains: Colors, spacing, typography, shadows

**Purpose:** Quick reference for planning and validation

### Tier 2: design-context.md (1K tokens)

- Project design summary
- File paths and quick reference
- Used by: agents (STEP 0.5)

**Purpose:** Agent orientation and file discovery

### Tier 3: README.md (100 tokens)

- Human-readable summary
- NOT for agents (use data.yaml instead)
- Used by: humans reviewing design

**Purpose:** Quick human reference

---

## Document Loading Pattern

**See:** `../document-loader.md` for complete unified pattern

### Pattern A: Planning (/pageplan, /csetup)

```typescript
Read: data.yaml (~500 tokens)
Validate: data.yaml exists (0 tokens)
Total: ~500 tokens
```

### Pattern B: Execution (/cdev)

```typescript
Send: Design reference (~200 tokens)
Agent reads: data.yaml (~500 tokens)
Total: ~700 tokens
```

### Pattern C: Agent (uxui-frontend)

```typescript
Read: data.yaml (~800 tokens)
Total: ~800 tokens
```

---

## Benefits

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| **Token Usage** | ~20K | ~4.7K | 70% reduction |
| **Speed** | Slow | Fast | 3-4x faster |
| **Consistency** | Random | Enforced | 100% |
| **Quality** | Same | Same | Maintained |

---

## Generated Files

**/designsetup now creates:**
1. `design-system/data.yaml` (tokens + psychology, ~800 lines) **FOR AGENTS**
2. `design-system/README.md` (human-readable summary, ~100 lines) **FOR HUMANS**

**Agents read data.yaml only!**

---

## 🔗 See Also

- `../document-loader.md` - Complete unified loading pattern
- `../../commands/designsetup.md` - /designsetup command (generates both files)
- `context-loading-protocol.md` - How agents load context
- `../../contexts/patterns/ui-component-consistency.md` - Component reuse patterns
