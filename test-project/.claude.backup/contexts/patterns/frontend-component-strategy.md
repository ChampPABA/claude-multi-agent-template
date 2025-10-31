# Frontend Component Strategy

## Core Principle: Reuse First, Create Second

**Before creating ANY new component, ALWAYS:**
1. Search existing codebase for similar components
2. Identify reusable sub-components
3. Extract and reuse existing styles
4. Maintain consistent design patterns

---

## 🔍 Component Discovery Workflow

### Step 1: Search for Existing Components

**Before creating a new component, search the codebase:**

```bash
# Search for component files
Glob: "**/*.tsx", "**/*.jsx", "**/*.vue"

# Search for similar functionality
Grep: "export.*function.*FormInput"
Grep: "export.*const.*Button"
Grep: "interface.*Props"
```

**Common component locations:**
- `components/` or `src/components/`
- `app/components/`
- `lib/components/`
- `ui/` or `src/ui/`

### Step 2: Analyze Existing Patterns

**Read and understand:**
1. **Component structure** - How are components organized?
2. **Naming conventions** - PascalCase? camelCase? Prefixes?
3. **Props patterns** - How are props typed? Common patterns?
4. **Style approach** - CSS Modules? Tailwind? Styled-components?

**Example analysis:**
```typescript
// Found: components/ui/Button.tsx
export interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'ghost'
  size?: 'sm' | 'md' | 'lg'
  children: React.ReactNode
  onClick?: () => void
}

// Pattern detected:
// - Props interfaces exported
// - variant + size pattern used
// - children always required
// → Use this pattern for new components!
```

---

## ♻️ Reuse Strategies

### Strategy 1: Direct Reuse (Best)

**Use existing component as-is:**

```typescript
// ✅ GOOD: Reuse existing Button
import { Button } from '@/components/ui/Button'

export function LoginForm() {
  return (
    <form>
      <Button variant="primary" size="lg">
        Sign In
      </Button>
    </form>
  )
}

// ❌ BAD: Create duplicate button
export function LoginButton() {
  return <button className="primary-button">Sign In</button>
}
```

### Strategy 2: Composition (Good)

**Compose new component from existing ones:**

```typescript
// ✅ GOOD: Compose from existing components
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { Card } from '@/components/ui/Card'

export function LoginForm() {
  return (
    <Card>
      <Input label="Email" type="email" />
      <Input label="Password" type="password" />
      <Button>Sign In</Button>
    </Card>
  )
}
```

### Strategy 3: Extension (Acceptable)

**Extend existing component when needed:**

```typescript
// ✅ ACCEPTABLE: Extend existing component
import { Button, ButtonProps } from '@/components/ui/Button'

interface IconButtonProps extends ButtonProps {
  icon: React.ReactNode
  iconPosition?: 'left' | 'right'
}

export function IconButton({ icon, iconPosition = 'left', children, ...props }: IconButtonProps) {
  return (
    <Button {...props}>
      {iconPosition === 'left' && icon}
      {children}
      {iconPosition === 'right' && icon}
    </Button>
  )
}
```

### Strategy 4: New Component (Last Resort)

**Only create new component if:**
- ✅ No existing component matches functionality
- ✅ Cannot compose from existing components
- ✅ Extension would be too complex

**When creating new component:**
```typescript
// ✅ GOOD: Follow existing patterns
// 1. Check existing Button.tsx for patterns
// 2. Use same prop structure
// 3. Use same styling approach
// 4. Use same naming conventions

export interface NewComponentProps {
  variant?: 'primary' | 'secondary'  // ← Same pattern as Button
  size?: 'sm' | 'md' | 'lg'          // ← Same pattern as Button
  children: React.ReactNode          // ← Same pattern as Button
}

export function NewComponent({ variant = 'primary', size = 'md', children }: NewComponentProps) {
  // Implementation following existing patterns
}
```

---

## 🎨 Style Consistency

### Step 1: Extract Existing Styles

**Before adding styles, find existing style patterns:**

```bash
# Search for style definitions
Grep: "className.*button"
Grep: "bg-blue-"
Grep: "@apply"
Grep: "styled\."

# Read style files
Read: "styles/globals.css"
Read: "tailwind.config.js"
```

### Step 2: Reuse Style Patterns

**Example: Found existing button styles**

```typescript
// Existing Button component uses:
className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-md"

// ✅ GOOD: Reuse same colors and spacing
className="bg-blue-600 hover:bg-blue-700 px-6 py-3 rounded-md"
                                      ↑      ↑
                            Adjusted for larger size

// ❌ BAD: Introduce new colors
className="bg-indigo-500 hover:bg-indigo-600 p-3 rounded"
          ↑ New color!        ↑ Different spacing pattern!
```

### Step 3: Extract to Shared Utilities (if needed)

**If you find repeated styles, suggest extraction:**

```typescript
// Found pattern:
// Button: "px-4 py-2 rounded-md font-medium"
// Card: "px-6 py-4 rounded-md shadow-sm"
// Input: "px-3 py-2 rounded-md border"

// Suggest extraction to design tokens:
const spacing = {
  sm: 'px-3 py-2',
  md: 'px-4 py-2',
  lg: 'px-6 py-4'
}

const rounded = 'rounded-md'  // Consistent corner radius
```

---

## 📋 Component Creation Checklist

Before creating a new component, complete this checklist:

### 1. Discovery Phase
- [ ] Searched for existing similar components
- [ ] Read at least 3 existing components to understand patterns
- [ ] Identified reusable sub-components
- [ ] Found existing style patterns

### 2. Planning Phase
- [ ] Can I reuse existing component? (Try first!)
- [ ] Can I compose from existing components?
- [ ] Can I extend existing component?
- [ ] Do I really need a new component?

### 3. Implementation Phase
- [ ] Follow existing naming conventions
- [ ] Use same prop patterns (variant, size, etc.)
- [ ] Reuse existing styles and colors
- [ ] Use existing spacing patterns
- [ ] Import and use existing sub-components

### 4. Validation Phase
- [ ] Component looks consistent with existing UI
- [ ] Props interface matches existing patterns
- [ ] Styles match existing color palette
- [ ] No duplicate functionality with existing components

---

## 🛠️ Tools for Discovery

### Glob Tool - Find Components
```
Pattern: "**/*Button*.{tsx,jsx,vue}"
Pattern: "**/*Form*.{tsx,jsx,vue}"
Pattern: "**/components/**/*.{tsx,jsx,vue}"
```

### Grep Tool - Search Patterns
```
Pattern: "export.*function.*Button"
Pattern: "interface.*Props"
Pattern: "className=.*bg-blue"
Pattern: "@apply.*button"
```

### Read Tool - Analyze Components
```
Read: "components/ui/Button.tsx"
Read: "styles/globals.css"
Read: "tailwind.config.js"
```

---

## 📊 Example Workflow

**Task:** Create a login form

### ❌ BAD Workflow (No Discovery)
```
1. Create LoginForm.tsx
2. Create LoginButton.tsx
3. Create LoginInput.tsx
4. Add custom styles
→ Result: Duplicate components, inconsistent styles
```

### ✅ GOOD Workflow (Discovery First)
```
1. Search existing components:
   Glob: "**/*{Button,Input,Form}*.tsx"
   → Found: components/ui/Button.tsx
   → Found: components/ui/Input.tsx
   → Found: components/ui/Card.tsx

2. Read existing components:
   Read: "components/ui/Button.tsx"
   → Props: variant, size, children
   → Styles: bg-blue-600, px-4 py-2, rounded-md

3. Compose LoginForm:
   import { Button } from '@/components/ui/Button'
   import { Input } from '@/components/ui/Input'
   import { Card } from '@/components/ui/Card'

4. Result: Consistent UI, reused components, minimal new code
```

---

## 🎯 Key Principles

1. **Search Before Create** - Always search existing codebase first
2. **Reuse > Compose > Extend > Create** - Follow this priority
3. **Consistency Over Uniqueness** - Match existing patterns, don't innovate
4. **Extract Common Patterns** - Identify and suggest reusable utilities
5. **Document Reuse** - Comment where components are reused from

---

## 🚨 Anti-Patterns to Avoid

### ❌ Creating Duplicate Components
```typescript
// BAD: Creating new button when Button exists
export function LoginButton() { ... }

// GOOD: Reuse existing Button
import { Button } from '@/components/ui/Button'
```

### ❌ Inconsistent Styling
```typescript
// BAD: New color scheme
className="bg-indigo-500"  // When project uses bg-blue-*

// GOOD: Reuse existing colors
className="bg-blue-600"  // Match existing buttons
```

### ❌ Different Prop Patterns
```typescript
// BAD: Different naming
interface Props {
  type: 'big' | 'small'  // When existing uses 'size'
}

// GOOD: Match existing patterns
interface Props {
  size: 'sm' | 'md' | 'lg'  // Same as Button component
}
```

---

## 📚 Related Patterns

- `@/.claude/contexts/design/` - Design system foundation
- `@/.claude/contexts/patterns/code-standards.md` - Code quality guidelines
- `@/.claude/contexts/patterns/development-principles.md` - KISS, YAGNI principles

---

**Remember:** The best code is code you don't have to write. Reuse first, create last.
