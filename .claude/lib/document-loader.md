# Document Loader - Unified Loading Pattern

> **Token-efficient, consistent document loading for all commands and agents**
> **Version:** 2.0.0 (Claude 4.5 Optimized)

---

## 🎯 Purpose

Provide a **single, consistent pattern** for loading project context across all commands and agents.

**Benefits:**
- ✅ **Token-efficient:** Load only what's needed (~1.5K vs 5K+ tokens)
- ✅ **Consistent:** Same pattern everywhere
- ✅ **Maintainable:** Change once, apply everywhere
- ✅ **Fast:** Lightweight files = faster loading

---

## 📋 Loading Tiers (Priority Order)

### Tier 1: Project Context (Always Load)
```
File: .claude/contexts/domain/{project}/design-context.md
Tokens: ~1000
Contains: Project summary, design file paths, quick token reference

When: EVERY command/agent that deals with UI/design
Why: Lightweight summary that points to full resources
```

### Tier 2: Design Tokens (Load for UI Work)
```
File: design-system/data.yaml
Tokens: ~500
Contains: Colors, spacing, typography, shadows, borders, animations

When: Commands/agents that need design tokens (pageplan, csetup, uxui-frontend)
Why: Lightweight token-only file for quick reference
```

### Tier 3: Human-Readable Summary (Optional)
```
File: design-system/README.md
Tokens: ~100 (human-readable summary)
Contains: Quick reference for humans, not for agents

When: Human wants to read design summary
Why: Short, scannable summary for humans
```

### Tier 4: Universal Principles (Fallback)
```
Files: .claude/contexts/design/*.md
Tokens: ~3000 (all 9 files)
Contains: Box thinking, color theory, spacing, typography (universal)

When: No project-specific style guide exists
Why: Universal design principles apply to any project
```

---

## 🔄 Loading Patterns by Command

### Pattern A: Planning Commands (/pageplan, /csetup)

**Goal:** Understand design system efficiently

```typescript
function loadDesignContext(projectName: string) {
  const context = {}

  // 1. Try design-context.md (project summary)
  const designContextPath = `.claude/contexts/domain/${projectName}/design-context.md`
  if (exists(designContextPath)) {
    context.summary = Read(designContextPath) // ~1K tokens
  }

  // 2. Load data.yaml (design tokens only)
  const tokensPath = 'design-system/data.yaml'
  if (exists(tokensPath)) {
    context.tokens = JSON.parse(Read(tokensPath)) // ~500 tokens
  }

  // 3. Validate data.yaml loaded successfully
  if (!context.tokens && hasFrontendWork) {
    warn(`⚠️ UI work detected but no data.yaml
          Run: /designsetup`)
  }

  return context // Total: ~1.5K tokens
}
```

**Usage:**
```typescript
// In /pageplan
const designContext = loadDesignContext(currentProject)

// Use tokens for component planning
const primaryColor = designContext.tokens.colors.primary.DEFAULT
const spacingScale = designContext.tokens.spacing.scale
```

---

### Pattern B: Execution Commands (/cdev)

**Goal:** Send design reference to agents (not full content)

```typescript
function buildDesignReference(projectName: string): string {
  const designContextPath = `.claude/contexts/domain/${projectName}/design-context.md`
  const tokensPath = 'design-system/data.yaml'

  // Don't load content! Just send paths + minimal summary
  return `
## 🎨 Design System Reference

**For uxui-frontend agent (STEP 0.5):**

1. Read: ${designContextPath} (~1K tokens)
   → Project design summary, file paths

2. Read: ${tokensPath} (~500 tokens)
   → Design tokens (colors, spacing, typography, psychology)

**Style Guidelines:**
| Instead of | Use | WHY |
|------------|-----|-----|
| text-gray-500 | text-foreground/70 | Theme-aware |
| p-5 | p-4 or p-6 | Spacing scale |

**Report format:**
"Design Context Loaded: design-context.md + data.yaml"
"Design Tokens Extracted: [list key tokens]"
  `

  // Total sent: ~200 tokens (reference only, not content!)
}
```

---

### Pattern C: Agent Self-Discovery (uxui-frontend STEP 0.5)

**Goal:** Agent loads design context efficiently

```typescript
// In agent prompt (uxui-frontend)
async function loadDesignSystem(projectName: string) {
  const report = []

  // STEP 0.5.1: Load design-context.md
  const designContextPath = `.claude/contexts/domain/${projectName}/design-context.md`
  let designContext = null

  if (exists(designContextPath)) {
    designContext = Read(designContextPath) // ~1K tokens
    report.push(`✅ design-context.md loaded`)
  } else {
    warn(`⚠️ No design-context.md - using fallback`)
  }

  // STEP 0.5.2: Load data.yaml
  const tokensPath = 'design-system/data.yaml'
  let tokens = null

  if (exists(tokensPath)) {
    tokens = JSON.parse(Read(tokensPath)) // ~500 tokens
    report.push(`✅ data.yaml loaded`)
  }

  // STEP 0.5.3: Extract key tokens
  const extractedTokens = {
    primary: tokens?.tokens.colors.primary.DEFAULT || '#000',
    spacing: tokens?.tokens.spacing.scale || [4,8,16,24,32,48],
    shadows: tokens?.tokens.shadows || {},
    componentLibrary: tokens?.component_library.name || 'unknown'
  }

  report.push(`✅ Design Tokens Extracted:`)
  report.push(`   - Primary: ${extractedTokens.primary}`)
  report.push(`   - Spacing: ${extractedTokens.spacing.join(', ')}px`)
  report.push(`   - Component Library: ${extractedTokens.componentLibrary}`)

  // STEP 0.5.4: data.yaml contains all design info - no need for separate files

  // Report to user
  output(`
✅ Design System Loaded

${report.join('\n')}

🎯 Ready to implement with design system awareness!
  `)

  return extractedTokens
}
```

---

## 📊 Token Comparison

| Approach | Tier 1 | Tier 2 | Tier 3 | Total | Use Case |
|----------|--------|--------|--------|-------|----------|
| **Planning** (pageplan, csetup) | design-context.md (1K) | data.yaml (500) | - | **1.5K** | ✅ Efficient |
| **Execution** (/cdev) | Reference only (200) | - | - | **200** | ✅ Very efficient |
| **Agent** (uxui-frontend) | design-context.md (1K) | data.yaml (500) | - | **1.5K** | ✅ Efficient |

**Savings: 70-95% reduction in tokens!**

---

## 📋 Best Practices

| Practice | WHY |
|----------|-----|
| Load design-context.md first | Entry point with file paths |
| Load data.yaml for UI work | Lightweight token reference |
| Use data.yaml for tokens | ~500 tokens, contains all design info |
| Validate files exist before loading | Prevent errors |
| Report what was loaded | Transparency for debugging |
| Skip design files for backend/database | Not needed, saves tokens |
| Use project name variable for paths | Portability |

---

## 🔄 Fallback Strategy

**If design-context.md doesn't exist:**

```typescript
function loadDesignFallback() {
  warn(`⚠️ No design-context.md found
       Attempting fallback...`)

  // Option 1: Load data.yaml directly
  if (exists('design-system/data.yaml')) {
    return { tokens: JSON.parse(Read('design-system/data.yaml')) }
  }

  // Option 2: Load universal design principles
  warn(`⚠️ No data.yaml - using universal principles`)
  return {
    universal: [
      Read('.claude/contexts/design/box-thinking.md'),
      Read('.claude/contexts/design/color-theory.md'),
      Read('.claude/contexts/design/spacing.md')
    ]
  }
}
```

---

## 📖 Usage Examples

### Example 1: /pageplan Command

```typescript
// In /pageplan implementation
const projectName = getProjectName()
const designContext = loadDesignContext(projectName)

if (designContext.tokens) {
  // Use tokens for planning
  const primary = designContext.tokens.colors.primary.DEFAULT
  output(`Using primary color: ${primary}`)
}

if (!designContext.tokens) {
  warn(`⚠️ No data.yaml - run /designsetup first`)
}
```

### Example 2: /cdev Command

```typescript
// In /cdev implementation
const designRef = buildDesignReference(projectName)

const agentPrompt = `
${taskDescription}

${designRef}

Now implement the task following design system guidelines.
`

Task(agent='uxui-frontend', prompt=agentPrompt)
```

### Example 3: uxui-frontend Agent

```typescript
// In agent STEP 0.5
const tokens = await loadDesignSystem(projectName)

// Use tokens in implementation
const Button = `
<button className="
  bg-primary
  text-primary-foreground
  px-4 py-2
  rounded-lg
  shadow-sm
  hover:shadow-md
  transition-all duration-200
">
  {children}
</button>
`
```

---

## 🎯 Integration Checklist

**To adopt this pattern in a command:**

- [ ] Identify if command deals with UI/design
- [ ] Use appropriate loading pattern (A, B, or C)
- [ ] Load design-context.md first
- [ ] Load data.yaml if needed
- [ ] Load data.yaml for design tokens
- [ ] Validate files exist
- [ ] Report what was loaded
- [ ] Handle fallback gracefully

---

**This pattern ensures consistent, token-efficient design context loading across the entire template! 🚀**
