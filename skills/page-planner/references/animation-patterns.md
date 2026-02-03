# Animation Patterns

Animation blueprint guide based on data.yaml tokens.

---

## Core Principles

**From data.yaml:**
- Durations: 150ms (quick), 300ms (normal), 500ms (slow)
- Easing: ease-in-out (default)
- Properties: GPU-accelerated ONLY (transform, opacity)

**Avoid:**
- width, height (causes layout recalculation)
- top, left, margin (use transform instead)
- font-size (causes text reflow)

---

## Button Animations

### Primary CTA

**Hover:**
- Properties: scale(1.05) + box-shadow
- Duration: 150ms
- Code: `transition-all duration-150 hover:scale-105 hover:shadow-lg`

**Active:**
- Properties: scale(0.95)
- Duration: 100ms
- Code: `active:scale-95`

**Loading:**
- Properties: opacity(70%) + spinner
- Duration: 300ms
- Code: `disabled:opacity-70`

### Secondary Button

**Hover:**
- Properties: background-color shift
- Duration: 150ms
- Code: `transition-colors duration-150 hover:bg-secondary/80`

---

## Card Animations

### Feature Card

**Hover:**
- Properties: box-shadow (sm → xl)
- Duration: 300ms
- Code: `transition-shadow duration-300 hover:shadow-xl`

### Interactive Card

**Hover:**
- Properties: box-shadow + border glow
- Duration: 300ms
- Code: `transition-all duration-300 hover:shadow-xl hover:border-primary/50`

**Active:**
- Properties: scale(0.98)
- Duration: 100ms
- Code: `active:scale-98`

---

## Input Animations

### Text Input

**Focus:**
- Properties: ring-2 + border-color
- Duration: 200ms
- Code: `transition-all duration-200 focus:ring-2 focus:ring-primary focus:border-primary`

**Error:**
- Properties: border-destructive
- Duration: 300ms
- Code: `border-destructive` (optionally + shake animation)

---

## Navigation Animations

### Desktop Menu Hover

- Properties: background-color
- Duration: 150ms
- Code: `transition-colors duration-150 hover:bg-accent`

### Mobile Sidebar Slide

- Properties: translateX(-100% → 0)
- Duration: 300ms
- Easing: cubic-bezier(0.4, 0, 0.2, 1)

**Framer Motion:**
```tsx
<motion.div
  initial={{ x: "-100%" }}
  animate={{ x: 0 }}
  exit={{ x: "-100%" }}
  transition={{ duration: 0.3, ease: [0.4, 0, 0.2, 1] }}
>
```

---

## Icon Animations

### Chevron Rotate

- Properties: rotate(0° → 180°)
- Duration: 200ms
- Code: `transition-transform duration-200 [data-state=open]:rotate-180`

### Loading Spinner

- Properties: rotate(360°)
- Duration: 1000ms
- Easing: linear
- Code: `animate-spin`

---

## Modal Animations

### Background Overlay

- Properties: opacity(0 → 100%)
- Duration: 200ms
- Code: `transition-opacity duration-200`

### Dialog Content

- Properties: opacity + scale(0.95 → 1)
- Duration: 300ms
- Easing: ease-in-out

---

## Performance Guidelines

**GPU-accelerated (preferred):**
- transform (translate, scale, rotate)
- opacity
- filter (blur, brightness)

**Avoid for animations:**
- width, height
- top, left, margin
- font-size

---

## Animation Checklist

Before implementing:
- [ ] All buttons use scale + shadow (150ms)
- [ ] All cards use shadow elevation (300ms)
- [ ] All inputs use ring (200ms)
- [ ] All durations from data.yaml
- [ ] All properties GPU-accelerated
- [ ] Tested on mobile (not janky)
