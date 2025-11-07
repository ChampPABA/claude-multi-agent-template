# Animation & Micro-interaction Patterns

> **Purpose:** Add life and polish to UI through thoughtful animations and interactions
> **Audience:** uxui-frontend agent (primary), all frontend agents
> **Integration:** Used with `/pageplan` Section 2.6 (Animation Blueprint)
> **Philosophy:** Match Flow Engineer Step 3 - Design animations systematically

**Key Principles:**
- **Purpose:** Every animation should have a purpose (guide attention, provide feedback, show transition)
- **Performance:** Use `transform` and `opacity` only (GPU-accelerated)
- **Accessibility:** Respect `prefers-reduced-motion` for users sensitive to motion
- **Subtlety:** Animations should enhance, not distract
- **Consistency:** Same component type = same animation pattern

---

## 📘 How to Use This File

**Priority:**
1. **Page-specific plan:** `openspec/changes/{id}/page-plan.md` Section 2.6 (if exists)
2. **Project tokens:** `design-system/STYLE_TOKENS.json` (animation tokens)
3. **General guidelines:** This file (fallback when above don't exist)

**When to read:**
- uxui-frontend agent STEP 0 (after loading project context)
- When creating components with interactions
- When no page-plan.md Animation Blueprint exists

---

## ⚡ Animation Performance Rules

### ✅ Fast Properties (GPU-accelerated)

**Use these properties for smooth 60fps animations:**

```css
/* ✅ GOOD - GPU accelerated */
.element {
  transform: translateX(100px);  /* Position */
  transform: scale(1.1);         /* Size */
  transform: rotate(45deg);      /* Rotation */
  opacity: 0.5;                  /* Transparency */
}
```

### ❌ Slow Properties (Avoid)

**These trigger layout recalculation - use sparingly:**

```css
/* ❌ BAD - Causes reflow/repaint */
.element {
  width: 200px;      /* Triggers layout */
  height: 100px;     /* Triggers layout */
  top: 50px;         /* Triggers layout */
  left: 100px;       /* Triggers layout */
  margin: 20px;      /* Triggers layout */
}
```

**Source:** FreeCodeCamp Performance Handbook
- `transform`/`opacity`: ~3ms render time
- Layout properties: ~14ms render time (4-5× slower)

---

## 🎯 Animation Duration Guidelines

**Standard Durations (from STYLE_TOKENS.json):**

| Token | Duration | Use Case | Example |
|-------|----------|----------|---------|
| **fast** | 150ms | Micro-interactions | Button hover, icon rotation |
| **normal** | 300ms | Transitions, reveals | Card elevation, modal entrance |
| **slow** | 500ms | Complex animations | Page transitions, carousel |

**❌ DON'T use random durations:** 200ms, 250ms, 400ms (inconsistent)
**✅ DO use token durations:** 150ms, 300ms, 500ms (consistent, predictable)

```css
/* Fast (hover effects) */
.button:hover {
  transform: translateY(-2px);
  transition: transform 150ms ease-out;
}

/* Normal (modal entrance) */
.modal {
  animation: fadeIn 300ms ease-out;
}

/* Slow (page transition) */
.page-transition {
  animation: slideIn 500ms ease-in-out;
}
```

---

## 🧩 Component Animation Patterns

> **Purpose:** Standard animation patterns for common components
> **Source:** Based on STYLE_TOKENS.json + `/pageplan` Section 2.6
> **Principle:** Same component type = same animation pattern (consistency)

### Button Components

#### Pattern: Scale + Shadow (Primary/CTA)
```tsx
<button className="
  transition-all duration-150
  hover:scale-105 hover:shadow-lg
  active:scale-95
">
  Get Started
</button>
```

**States:**
- **Hover:** Scale(1.05) + Shadow(md→lg) | 150ms
- **Active:** Scale(0.95) | 100ms (immediate feedback)
- **Disabled:** Opacity(70%) | static

**Rationale:** Creates depth, confirms interactivity, tactile press feedback

---

#### Pattern: Background Shift (Secondary)
```tsx
<button className="
  transition-colors duration-150
  hover:bg-secondary/80
">
  Learn More
</button>
```

**Rationale:** Subtle, doesn't distract from primary CTA

---

### Card Components

#### Pattern: Shadow Elevation
```tsx
<div className="
  transition-shadow duration-300
  hover:shadow-xl hover:border-primary/50
">
  {/* Card content */}
</div>
```

**States:**
- **Hover:** Shadow(sm→xl) + Border glow | 300ms
- **Click (if interactive):** Scale(0.98) | 100ms

**Rationale:** Elegant, smooth, matches Material Design

---

### Input & Form Components

#### Pattern: Ring + Border Shift
```tsx
<input className="
  transition-all duration-200
  focus:ring-2 focus:ring-primary focus:border-primary
" />
```

**States:**
- **Focus:** Ring(2px primary) + Border(primary) | 200ms
- **Error:** Border(destructive) + optional shake | 300ms

**Rationale:** Clear focus indicator (accessibility), balanced duration

---

## 🎨 Entrance Animations

### 1. Fade In

**Use for:** Images, cards, content sections

```css
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.fade-in {
  animation: fadeIn 300ms ease-out;
}
```

**React/Next.js:**
```tsx
<div className="animate-fadeIn opacity-0">
  Content appears smoothly
</div>

// Tailwind config
module.exports = {
  theme: {
    extend: {
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
      },
      animation: {
        fadeIn: 'fadeIn 300ms ease-out forwards',
      },
    },
  },
}
```

---

### 2. Slide In

**Use for:** Sidebars, notifications, modals

```css
/* Slide from bottom */
@keyframes slideInBottom {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.slide-in-bottom {
  animation: slideInBottom 300ms ease-out;
}

/* Slide from right (sidebar) */
@keyframes slideInRight {
  from {
    transform: translateX(100%);
  }
  to {
    transform: translateX(0);
  }
}

.sidebar {
  animation: slideInRight 250ms ease-out;
}
```

---

### 3. Scale In

**Use for:** Modals, tooltips, popovers

```css
@keyframes scaleIn {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.modal {
  animation: scaleIn 200ms ease-out;
}
```

---

### 4. Scroll-Triggered Animations

**Use for:** Elements that appear on scroll (lazy reveal)

**Using Intersection Observer:**

```tsx
import { useEffect, useRef } from 'react'

export function ScrollReveal({ children }: { children: React.ReactNode }) {
  const ref = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('animate-fadeInUp')
        }
      },
      { threshold: 0.1 }
    )

    if (ref.current) observer.observe(ref.current)
    return () => observer.disconnect()
  }, [])

  return (
    <div ref={ref} className="opacity-0">
      {children}
    </div>
  )
}
```

**CSS:**
```css
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fadeInUp {
  animation: fadeInUp 400ms ease-out forwards;
}
```

---

## 🖱️ Micro-interactions

### 1. Hover Effects

**Card Lift (common pattern):**

```css
.card {
  transition: transform 200ms ease-out,
              box-shadow 200ms ease-out;
}

.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
}
```

**Button Scale:**

```css
.button {
  transition: transform 150ms ease-out;
}

.button:hover {
  transform: scale(1.05);
}
```

**Link Underline Animation:**

```css
.link {
  position: relative;
  text-decoration: none;
}

.link::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 0;
  height: 2px;
  background: currentColor;
  transition: width 200ms ease-out;
}

.link:hover::after {
  width: 100%;
}
```

---

### 2. Click/Press Effects

**Scale Down (tactile feedback):**

```css
.button {
  transition: transform 100ms ease-out;
}

.button:active {
  transform: scale(0.98);
}
```

**Ripple Effect (Material Design):**

```tsx
import { useState } from 'react'

export function RippleButton({ children, onClick }: any) {
  const [ripples, setRipples] = useState<Array<{ x: number; y: number; id: number }>>([])

  const handleClick = (e: React.MouseEvent<HTMLButtonElement>) => {
    const rect = e.currentTarget.getBoundingClientRect()
    const x = e.clientX - rect.left
    const y = e.clientY - rect.top

    setRipples([...ripples, { x, y, id: Date.now() }])
    setTimeout(() => setRipples((prev) => prev.slice(1)), 600)

    onClick?.(e)
  }

  return (
    <button className="relative overflow-hidden" onClick={handleClick}>
      {children}
      {ripples.map((ripple) => (
        <span
          key={ripple.id}
          className="absolute bg-white/30 rounded-full animate-ripple"
          style={{
            left: ripple.x,
            top: ripple.y,
            width: 10,
            height: 10,
          }}
        />
      ))}
    </button>
  )
}
```

**CSS:**
```css
@keyframes ripple {
  to {
    transform: translate(-50%, -50%) scale(10);
    opacity: 0;
  }
}

.animate-ripple {
  animation: ripple 600ms ease-out forwards;
  transform: translate(-50%, -50%);
}
```

---

### 3. Focus States

**Ring Animation:**

```css
.input:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.5);
  transition: box-shadow 150ms ease-out;
}
```

**Border Glow:**

```css
.input {
  border: 2px solid transparent;
  transition: border-color 200ms ease-out;
}

.input:focus {
  border-color: var(--color-primary);
}
```

---

## 🔄 Loading States

### 1. Skeleton Loader

```tsx
export function SkeletonCard() {
  return (
    <div className="border rounded-lg p-6 space-y-4">
      <div className="h-4 bg-gray-200 rounded animate-pulse" />
      <div className="h-4 bg-gray-200 rounded animate-pulse w-3/4" />
      <div className="h-8 bg-gray-200 rounded animate-pulse" />
    </div>
  )
}
```

**CSS:**
```css
@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
```

---

### 2. Shimmer Effect

```css
@keyframes shimmer {
  0% {
    background-position: -1000px 0;
  }
  100% {
    background-position: 1000px 0;
  }
}

.skeleton {
  background: linear-gradient(
    90deg,
    #f0f0f0 25%,
    #e0e0e0 50%,
    #f0f0f0 75%
  );
  background-size: 1000px 100%;
  animation: shimmer 2s infinite;
}
```

---

### 3. Spinner (Button Loading)

```tsx
export function ButtonWithSpinner({ loading, children, ...props }: any) {
  return (
    <button {...props} disabled={loading}>
      {loading ? (
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
          Loading...
        </div>
      ) : (
        children
      )}
    </button>
  )
}
```

**CSS:**
```css
@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.animate-spin {
  animation: spin 1s linear infinite;
}
```

---

## 🎭 Transition Choreography

### 1. Stagger Effect (List Items)

**Animate list items with delay:**

```tsx
export function StaggerList({ items }: { items: string[] }) {
  return (
    <ul>
      {items.map((item, index) => (
        <li
          key={item}
          className="animate-fadeInUp"
          style={{ animationDelay: `${index * 100}ms` }}
        >
          {item}
        </li>
      ))}
    </ul>
  )
}
```

---

### 2. Page Transitions

```tsx
import { AnimatePresence, motion } from 'framer-motion'

export function PageTransition({ children }: { children: React.ReactNode }) {
  return (
    <AnimatePresence mode="wait">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -20 }}
        transition={{ duration: 0.3 }}
      >
        {children}
      </motion.div>
    </AnimatePresence>
  )
}
```

---

## ♿ Accessibility: Reduced Motion

**Always respect user preferences:**

```css
/* Default: animations enabled */
.element {
  animation: slideIn 300ms ease-out;
}

/* User prefers reduced motion */
@media (prefers-reduced-motion: reduce) {
  .element {
    animation: none;
    transition: none;
  }
}
```

**React Hook:**

```tsx
import { useEffect, useState } from 'react'

export function usePrefersReducedMotion() {
  const [prefersReducedMotion, setPrefersReducedMotion] = useState(false)

  useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)')
    setPrefersReducedMotion(mediaQuery.matches)

    const handler = (e: MediaQueryListEvent) => setPrefersReducedMotion(e.matches)
    mediaQuery.addEventListener('change', handler)
    return () => mediaQuery.removeEventListener('change', handler)
  }, [])

  return prefersReducedMotion
}
```

---

## 📋 Animation Checklist

**Before implementing animations:**

- [ ] **Performance:** Using `transform`/`opacity` only? ✓
- [ ] **Duration:** 150-600ms (appropriate for use case)? ✓
- [ ] **Easing:** Using `ease-out` (most cases) or `ease-in-out`? ✓
- [ ] **Purpose:** Animation has clear purpose (not decorative)? ✓
- [ ] **Accessibility:** Respects `prefers-reduced-motion`? ✓
- [ ] **Subtlety:** Animation enhances, doesn't distract? ✓

---

## 🚨 Common Mistakes

### ❌ Mistake 1: Animating layout properties

```css
/* ❌ BAD: Width triggers layout recalculation */
.element:hover {
  width: 200px;
  transition: width 300ms;
}

/* ✅ GOOD: Scale uses transform (GPU) */
.element:hover {
  transform: scaleX(1.2);
  transition: transform 300ms;
}
```

---

### ❌ Mistake 2: Too long animations

```css
/* ❌ BAD: Feels sluggish */
.button:hover {
  transform: scale(1.05);
  transition: transform 1000ms;
}

/* ✅ GOOD: Snappy and responsive */
.button:hover {
  transform: scale(1.05);
  transition: transform 150ms ease-out;
}
```

---

### ❌ Mistake 3: Forgetting reduced motion

```css
/* ❌ BAD: Ignores user preference */
.element {
  animation: spinForever 2s infinite;
}

/* ✅ GOOD: Respects accessibility */
.element {
  animation: spinForever 2s infinite;
}

@media (prefers-reduced-motion: reduce) {
  .element {
    animation: none;
  }
}
```

---

## 📚 Additional Resources

**Libraries:**
- **Framer Motion:** https://www.framer.com/motion/ (React animations)
- **GSAP:** https://greensock.com/gsap/ (High-performance animations)
- **Auto Animate:** https://auto-animate.formkit.com/ (Zero-config animations)

**Inspiration:**
- **UI Movement:** https://uimovement.com/
- **Lottie Files:** https://lottiefiles.com/
- **Codrops:** https://tympanus.net/codrops/

---

**💡 Remember:** The best animations are the ones users don't consciously notice - they just make the UI feel better!
