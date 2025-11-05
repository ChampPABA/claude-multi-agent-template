# Best Practices System

> **Detailed guide to auto-generated framework-specific best practices**
> **Source:** Extracted from CLAUDE.md (Navigation Hub)
> **Version:** 1.4.0

---

## 📚 How It Works

1. **Run `/agentsetup`** to detect tech stack and generate best practices
2. **Context7 queries** latest framework docs (React, Next.js, Prisma, etc.)
3. **Best practices files** created in `domain/{project}/best-practices/`
4. **Agents auto-discover** project via 3-level indexing
5. **Code quality** enforced by framework-specific patterns

---

## Generated Files

```
.claude/contexts/domain/
├── index.md                              # Level 1 - Project Registry
└── {project}/
    ├── README.md                         # Level 2 - Project Overview
    ├── tech-stack.md                     # Tech details
    └── best-practices/
        ├── index.md                      # Level 3 - Best Practices Registry
        ├── react-18.md                   # ✅ DO's, ❌ DON'Ts, 🎯 Checklist
        ├── nextjs-15.md
        ├── prisma-6.md
        └── vitest-2.md
```

---

## Agent Discovery Flow

**Every agent follows this sequence (STEP 0):**

```
1. Read: domain/index.md → Get current project name
2. Read: domain/{project}/README.md → Get tech stack
3. Read: domain/{project}/best-practices/index.md → Get relevant files
4. Read: domain/{project}/best-practices/{files} → Load best practices
5. Report: "✅ Project Context Loaded"
```

**Example: uxui-frontend agent**
```
✅ Project Context Loaded

📁 Project: my-app
🛠️ Stack: Next.js 15, React 18, Prisma 6
📚 Best Practices Loaded:
   - React 18 ✓
   - Next.js 15 ✓

🎯 Ready to create UI components!
```

---

## Design System / Style Guide Generation

### How It Works

`/designsetup` **auto-detects** your project context and generates a comprehensive style guide.

**Three Smart Paths:**

1. **Path 1: Reference Design** (Priority 1)
   - Detects: `reference/`, `design-reference/`, `designs/` folders
   - Analyzes: HTML files (SingleFile exports), screenshots
   - **Auto-detects design style** (Neo-Brutalism, Minimalist, Modern, etc.)
   - Output: Style guide based on reference design (17 sections, always)

2. **Path 2: Brownfield - Reverse Engineering** (Priority 2)
   - Detects: Existing codebase (> 10 components)
   - Extracts: Colors, spacing, typography, component patterns
   - Output: Style guide reflecting current state + cleanup suggestions

3. **Path 3: Greenfield - AI-Generated** (Priority 3)
   - Detects: Empty project (< 10 components)
   - Asks: Application type (SaaS, Marketing, E-commerce, etc.)
   - Output: Modern, best-practice style guide

### Generated File

```
design-system/
└── STYLE_GUIDE.md    ← Comprehensive 17-section guide
```

**All 17 Sections (Complete):**
1. Overview
2. Design Philosophy
3. Color Palette (HEX codes, usage, Tailwind classes)
4. Typography (headings, body, weights)
5. Spacing System (4px/8px grid)
6. Component Styles (Button, Card, Input, Badge, etc.)
7. Shadows & Elevation
8. Animations & Transitions
9. Border Styles
10. Border Radius
11. **Opacity & Transparency** (standalone)
12. **Z-Index Layers** (standalone)
13. **Responsive Breakpoints** (standalone)
14. CSS Variables / Tailwind Theme (Design Tokens in JSON)
15. Layout Patterns
16. Example Component Reference (React + Tailwind code)
17. Additional Sections (Best Practices, Accessibility, Icon System)

### Workflow

```bash
# Recommended flow:

# 1. Generate style guide FIRST (optional but recommended)
/designsetup

# 2. Setup project (discovers style guide)
/psetup

# 3. Start development (agents use STYLE_GUIDE.md)
/csetup feature-login
/cdev feature-login
```

### Agent Discovery

**uxui-frontend agent automatically reads:**
1. `design-system/STYLE_GUIDE.md` (if exists) ← **Priority #1**
2. `.claude/contexts/design/*.md` (general principles) ← Fallback

**Why this matters:**
- ✅ Ensures visual consistency (no hardcoded colors, spacing)
- ✅ Prevents duplicate components
- ✅ Enforces accessibility standards
- ✅ Speeds up development (reuse patterns)

---

## 🔗 See Also

- `../../commands/agentsetup.md` - /agentsetup command (generates best practices)
- `../../commands/designsetup.md` - /designsetup command (generates style guide)
- `../../commands/psetup.md` - /psetup command (one-time project setup)
- `../../contexts/patterns/agent-discovery.md` - Shared agent discovery flow
- `context-loading-protocol.md` - How agents load framework-specific context
