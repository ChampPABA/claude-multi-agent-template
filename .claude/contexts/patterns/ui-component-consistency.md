# UI Component Visual Consistency

**Core Principle:** Before creating ANY UI component, extract and reuse design tokens from existing similar components to ensure 100% visual consistency.

---

## 🎯 The Problem

**Symptom:** New components look "slightly different" from existing ones.

**Common Issues:**
- Icon opacity: `opacity-50` vs `text-foreground/70`
- Spacing: `px-4` vs `px-3` (inconsistent padding)
- Colors: `text-gray-500` vs `text-foreground/70` (hardcoded vs theme-aware)
- Border radius: `rounded` vs `rounded-md` (inconsistent corners)

**Root Cause:**
- ❌ Agent creates component without checking existing ones
- ❌ No visual comparison with reference components
- ❌ Missing design token extraction step
- ❌ No cross-component validation

---

## 📋 Mandatory Workflow

**ALWAYS follow these 6 steps before creating UI components:**

### Step 1: Search for Similar Components

```bash
# Find components with similar functionality
Glob: "**/*{Field,Input,Select,Dropdown}*.{tsx,jsx,vue}"
Grep: "ChevronDown"
Grep: "dropdown.*icon"
```

**Questions to ask:**
- Is there a component with similar user interaction?
- What component has the same visual element (icon, border, shadow)?
- Which component shares the same state behavior (focus, error, disabled)?

---

### Step 2: Extract Design Tokens

**Read reference component and document these properties:**

#### Icon Properties
```typescript
const ICON_TOKENS = {
  component: 'ChevronDown',                    // Which icon?
  size: 'h-4 w-4',                             // Dimensions
  color: 'text-foreground/70',                 // ⚠️ NOT opacity-50
  position: 'right-3 top-1/2 -translate-y-1/2', // Absolute positioning
  pointer: 'pointer-events-none',              // Interaction
}
```

#### Input/Select Properties
```typescript
const INPUT_TOKENS = {
  padding: 'pl-3 pr-10 py-2',                  // pr-10 = space for icon
  border: 'border-input',
  borderError: 'border-destructive',
  borderRadius: 'rounded-md',
  background: 'bg-background',
  text: 'text-foreground',
  placeholder: 'placeholder:text-muted-foreground',

  // States
  focus: 'focus:ring-2 focus:ring-primary focus:ring-offset-2',
  disabled: 'disabled:opacity-50 disabled:cursor-not-allowed',
  transition: 'transition-colors',
}
```

#### Layout Structure
```typescript
const LAYOUT_TOKENS = {
  wrapper: 'relative',          // Required for absolute icon positioning
  input: 'appearance-none',     // Hide native select arrow
  icon: 'absolute',             // Icon positioning
}
```

#### Animation Properties (🆕 v1.4.0 - MANDATORY)
```typescript
const ANIMATION_TOKENS = {
  // Hover state
  hover: {
    properties: ['transform', 'box-shadow'],  // GPU-accelerated only
    values: ['scale(1.05)', 'shadow-lg'],
    duration: '150ms',                         // From data.yaml
    easing: 'ease-in-out',
    classes: 'hover:scale-105 hover:shadow-lg transition-all duration-150'
  },

  // Focus state (inputs)
  focus: {
    properties: ['box-shadow', 'border-color'],
    values: ['ring-2 ring-primary', 'border-primary'],
    duration: '200ms',
    easing: 'ease-in-out',
    classes: 'focus:ring-2 focus:ring-primary focus:border-primary transition-all duration-200'
  },

  // Active state (press feedback)
  active: {
    properties: ['transform'],
    values: ['scale(0.95)'],
    duration: '100ms',
    easing: 'ease-in-out',
    classes: 'active:scale-95'
  },

  // Rationale
  description: 'Button scale + shadow pattern (consistency with other buttons)'
}
```

**Critical Rules:**
1. ✅ Extract animation from reference component (same as colors, spacing)
2. ✅ Use durations from data.yaml (150ms, 300ms, 500ms)
3. ✅ Use GPU-accelerated properties (transform, opacity) - NOT width, height, top, left
4. ✅ Same component type = same animation pattern (buttons scale, cards elevate shadow)
5. ❌ NO random durations (200ms, 250ms) - only 150/300/500ms
6. ❌ NO inconsistent patterns (button A scales, button B changes color)

---

### Step 3: Apply Tokens to New Component

**Example: Creating ComboboxField**

```typescript
// ❌ WRONG - Custom values without reference
<div>
  <select className="px-4 py-3">...</select>
  <ChevronDown className="opacity-50 h-5 w-5" />
</div>

// ✅ CORRECT - Extracted tokens from FormField
<div className="relative">
  <Combobox className="appearance-none pl-3 pr-10 py-2 rounded-md border border-input">
    ...
  </Combobox>
  <ChevronDown className="absolute right-3 top-1/2 -translate-y-1/2 h-4 w-4 text-foreground/70 pointer-events-none" />
</div>
```

**Key Rules:**
1. Use **exact same classes** for identical elements
2. Prefer **theme tokens** (`text-foreground/70`) over hardcoded colors (`text-gray-500`)
3. Match **spacing patterns** exactly (`pl-3 pr-10 py-2`)
4. Reuse **state classes** (focus, hover, disabled)

---

### Step 4: Visual Comparison Test

**Use Browser DevTools to compare pixel-by-pixel:**

1. Open page with both components side-by-side
2. Press F12 → Inspect Element
3. Compare CSS computed values:

```css
/* Icon - Must match exactly */
width: 16px                    /* h-4 */
height: 16px                   /* w-4 */
right: 12px                    /* right-3 (0.75rem) */
top: 50%                       /* top-1/2 */
transform: translateY(-50%)    /* -translate-y-1/2 */
opacity: 0.7                   /* text-foreground/70 */

/* Input - Must match exactly */
padding-left: 12px             /* pl-3 */
padding-right: 40px            /* pr-10 */
padding-top: 8px               /* py-2 */
padding-bottom: 8px            /* py-2 */
border-radius: 6px             /* rounded-md */
```

4. **If values differ → STOP and fix immediately**

---

### Step 5: State Consistency Check

**Test every interactive state:**

| State | Expected Behavior |
|-------|------------------|
| Normal | Icon visible, clear contrast |
| Hover | Cursor changes if interactive |
| Focus | Ring appears (same color/offset as reference) |
| Error | Border becomes `border-destructive` |
| Disabled | `opacity-50` + `cursor-not-allowed` |

**Compare each state with reference component → Must be identical**

---

### Step 6: Document Design Reference

**Add JSDoc comment with design lineage:**

```typescript
/**
 * ComboboxField - Searchable dropdown field
 *
 * VISUAL CONSISTENCY:
 * - Extracted design tokens from: components/ui/form-field.tsx
 * - Icon: ChevronDown (h-4 w-4, text-foreground/70, right-3)
 * - Matches FormField: focus ring, error states, spacing
 * - States tested: normal, focus, error, disabled
 *
 * @see components/ui/form-field.tsx - Reference component
 */
export function ComboboxField({ ... }) {
  // Implementation
}
```

---

## ⚠️ Common Issues to Avoid

### Hardcoded Colors
```typescript
// WRONG
className="text-gray-500"      // Not theme-aware
className="bg-blue-600"        // Hardcoded color

// CORRECT
className="text-foreground/70" // Theme token
className="bg-primary"         // Theme token
```

### Non-Standard Opacity/Size
```typescript
// WRONG
className="opacity-50"         // Too light for foreground
className="h-5 w-5"            // Larger than standard

// CORRECT
className="text-foreground/70" // Standard opacity via color
className="h-4 w-4"            // Standard icon size
```

### ❌ Inconsistent Spacing
```typescript
// WRONG
className="px-4 py-3"          // Different from FormField

// CORRECT
className="pl-3 pr-10 py-2"    // Matches FormField exactly
```

### ❌ Visual Discrepancy
- **If it "looks different" → STOP**
- Open browser side-by-side
- Compare with DevTools
- Fix before proceeding

---

## 📊 Common Design Tokens Reference

### Dropdown Components
```typescript
// Icon
size: 'h-4 w-4'
color: 'text-foreground/70'                    // ⚠️ NOT opacity-50
position: 'right-3 top-1/2 -translate-y-1/2'

// Container
padding: 'pl-3 pr-10 py-2'                     // pr-10 for icon space
border: 'rounded-md border border-input'
focus: 'focus:ring-2 focus:ring-primary focus:ring-offset-2'
```

### Input Components
```typescript
padding: 'px-3 py-2'
border: 'rounded-md border border-input'
background: 'bg-background'
text: 'text-foreground'
placeholder: 'placeholder:text-muted-foreground'
```

### Button Components
```typescript
height: 'h-10'
padding: 'px-4 py-2'
borderRadius: 'rounded-md'
fontWeight: 'font-medium'
transition: 'transition-colors'
```

---

## ✅ Quick Checklist

**Before committing any UI component:**

- [ ] Found similar reference component in codebase
- [ ] Extracted all design tokens (icon, spacing, colors, states, **animations**)
- [ ] Extracted animation tokens (hover, focus, active, durations)
- [ ] Verified durations match data.yaml (150/300/500ms)
- [ ] Verified animation properties are GPU-accelerated (transform, opacity)
- [ ] Applied tokens exactly (no guessing, no random values)
- [ ] Tested visual appearance in browser
- [ ] Compared computed CSS values with DevTools
- [ ] Tested all states (normal, hover, focus, error, disabled)
- [ ] Tested animation smoothness (60fps, no jank)
- [ ] Documented reference component in JSDoc
- [ ] Visually indistinguishable from reference component

---

## 🎯 Summary

**One-Sentence Rule:**
> "Before creating a UI component → Find the most similar existing component → Extract its design tokens → Apply them exactly → Test that they're 100% identical"

**Prevention Strategy:**
1. ✅ Search for reference component first
2. ✅ Extract design tokens systematically
3. ✅ Apply tokens without modification
4. ✅ Validate visual consistency in browser
5. ✅ Document design lineage

**Anti-Pattern:**
1. ❌ Create component without checking existing ones
2. ❌ Use custom values instead of extracted tokens
3. ❌ Skip visual comparison test
4. ❌ Commit without cross-component validation

---

## 📚 Related Patterns

- `@/.claude/contexts/patterns/frontend-component-strategy.md` - Component reuse strategy
- `@/.claude/contexts/design/index.md` - Design system foundation
- `@/.claude/contexts/design/box-thinking.md` - Layout analysis

---

**Remember:** Visual consistency is not optional. Users notice when components "feel different" even if they can't articulate why.
