# Context Optimization (v1.2.0)

> **Detailed guide to token-efficient loading strategies**
> **Source:** Extracted from CLAUDE.md (Navigation Hub)
> **Version:** 1.4.0

---

## ⚡ The Problem: Token Waste

**Before v1.2.0:**
```
/pageplan     → reads STYLE_GUIDE.md (~5K tokens)
/csetup       → reads STYLE_GUIDE.md (~5K tokens)
/cdev         → sends STYLE_GUIDE.md (~5K tokens)
uxui-frontend → reads STYLE_GUIDE.md (~5K tokens)
────────────────────────────────────────────────
Total: ~20K tokens (same content read 4 times!)
```

**After v1.2.0:**
```
/designsetup  → generates STYLE_TOKENS.json (~500 tokens) ✅
/pageplan     → reads STYLE_TOKENS.json (~500 tokens) ✅
/csetup       → validates files exist (0 tokens) ✅
/cdev         → sends reference only (~200 tokens) ✅
uxui-frontend → reads STYLE_TOKENS.json + selective STYLE_GUIDE (~3.5K) ✅
────────────────────────────────────────────────
Total: ~4.7K tokens (70% reduction!) ✨
```

---

## The Solution: 3-Tier Loading

### Tier 1: STYLE_TOKENS.json (500 tokens)

- Lightweight design tokens only
- Used by: /pageplan, /csetup, agents
- Contains: Colors, spacing, typography, shadows

**Purpose:** Quick reference for planning and validation

### Tier 2: design-context.md (1K tokens)

- Project design summary
- File paths and quick reference
- Used by: agents (STEP 0.5)

**Purpose:** Agent orientation and file discovery

### Tier 3: STYLE_GUIDE.md (5K tokens)

- Full reference with examples
- Loaded selectively (specific sections only)
- Used by: agents (when needed)

**Purpose:** Complete design system documentation

---

## Document Loading Pattern

**See:** `../document-loader.md` for complete unified pattern

### Pattern A: Planning (/pageplan, /csetup)

```typescript
Read: STYLE_TOKENS.json (~500 tokens)
Validate: STYLE_GUIDE.md exists (0 tokens)
Total: ~500 tokens
```

### Pattern B: Execution (/cdev)

```typescript
Send: Design reference (~200 tokens)
Agent reads: STYLE_TOKENS.json (~500 tokens)
Total: ~700 tokens
```

### Pattern C: Agent (uxui-frontend)

```typescript
Read: STYLE_TOKENS.json (~500 tokens)
Read: STYLE_GUIDE sections (~2K tokens, selective)
Total: ~2.5K tokens
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
1. `design-system/STYLE_GUIDE.md` (full guide, 17 sections)
2. `design-system/STYLE_TOKENS.json` (tokens only) **NEW!**

**Agents automatically use both!**

---

## 🔗 See Also

- `../document-loader.md` - Complete unified loading pattern
- `../../commands/designsetup.md` - /designsetup command (generates both files)
- `context-loading-protocol.md` - How agents load context
- `../../contexts/patterns/ui-component-consistency.md` - Component reuse patterns
