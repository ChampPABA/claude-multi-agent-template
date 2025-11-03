# Stripe Design System Analysis

## Extraction Summary

**Site:** stripe.com
**Extracted:** 2025-11-03
**Coverage:** 15/17 sections (88%)

---

## Design Style Classification

**Primary Style:** Modern SaaS / Fintech
**Secondary Influences:** Minimalist, Professional

### Visual Characteristics:
- Clean, professional aesthetic
- Strong use of purple (#635BFF) as brand color
- Deep navy (#0A2540) for trust and stability
- Subtle shadows for depth without overwhelming
- Generous whitespace
- Sans-serif typography (custom Sohne font)

---

## Visual Principles

1. **Clarity Over Decoration**
   - Minimal ornamental elements
   - Focus on content hierarchy
   - Clean typography with clear weight distinctions (300, 425, 500, 700)

2. **Subtle Depth**
   - Multi-layered shadows: `rgba(50, 50, 93, 0.25) 0px 50px 100px -20px, rgba(0, 0, 0, 0.3) 0px 30px 60px -30px`
   - Creates floating card effects without heavy shadows
   - Elevation through shadow, not borders

3. **Purposeful Color**
   - Purple (#635BFF) for primary actions and brand moments
   - Navy (#0A2540) for trust and professionalism
   - Accent colors for functional purposes: green (#15BE53) for success, cyan (#00C4C4) for info

4. **Smooth Interactions**
   - Fast transitions (0.15s) with custom easing: `cubic-bezier(0.215, 0.61, 0.355, 1)`
   - Subtle hover states - opacity changes rather than dramatic color shifts
   - Consistent interaction patterns across components

---

## Psychology & Emotion

### What This Design Evokes:

1. **Trust & Professionalism**
   - Deep navy (#0A2540) communicates stability
   - Clean layouts suggest organization
   - Subtle shadows create premium feel

2. **Modern Innovation**
   - Purple brand color feels contemporary
   - Smooth animations suggest technical sophistication
   - Clean typography feels current

3. **Approachability**
   - Light backgrounds (#F6F9FC) feel open and welcoming
   - Generous spacing reduces cognitive load
   - Soft shadows (vs. hard borders) feel friendly

### Why It Works:
- **Financial services require trust** → Navy + professional layout
- **Developers are the audience** → Clean, logical hierarchy
- **Premium product** → Subtle depth, custom typography
- **Global scale** → Minimal cultural baggage in design

---

## Target Audience

### Primary: Developers & Technical Decision Makers
- Clean code-like hierarchy
- Minimal distraction
- Logical information architecture
- Fast, smooth interactions that feel "engineered"

### Secondary: Business Executives
- Professional aesthetic builds confidence
- Clear value propositions
- Enterprise-grade visual language

---

## Key Differentiators

**vs. Typical SaaS:**
1. **Custom Typography:** Sohne font (not default system fonts)
2. **Purple Brand Color:** Distinctive vs. common blue
3. **Multi-layer Shadows:** More sophisticated than single-shadow approach
4. **Minimal Borders:** Depth through shadow, not lines
5. **Custom Easing:** `cubic-bezier(0.215, 0.61, 0.355, 1)` instead of linear/ease

**vs. Traditional Fintech:**
1. **Vibrant Purple:** Breaking from conservative blues/greens
2. **Modern Typography:** Custom variable font vs. traditional serifs
3. **Generous Whitespace:** Less dense than traditional finance UIs
4. **Smooth Animations:** More dynamic than static enterprise UIs

---

## Design Philosophy

### Core Beliefs:

1. **"Clarity Is King"**
   - Every element serves a purpose
   - Strong typography hierarchy (32px → 18px → 16px → 13px → 10px)
   - Consistent spacing (multiples of 8px implied from 16px, 32px values)

2. **"Depth Through Subtlety"**
   - Shadows create elevation without being heavy
   - Multiple shadow layers for realistic depth
   - Prefer gradient shadows over flat colors

3. **"Brand Without Noise"**
   - Purple used strategically, not everywhere
   - Navy anchors the palette
   - Accent colors serve functional purposes

4. **"Speed Matters"**
   - Fast transitions (0.15s)
   - Custom easing for natural movement
   - Hover states that feel instant

5. **"Premium Defaults"**
   - Custom typography (Sohne)
   - Thoughtful border radius (16.5px, not 16px - shows intentionality)
   - Professional polish in every detail

---

## Technical Patterns Observed

### Border Radius System:
- **Large buttons:** 16.5px (distinctive, not standard 16px)
- **Small elements:** 8px, 4px
- **Pills:** 9999px (infinite rounding)

### Shadow System:
- **Card elevation:** Multi-layer with 50px-100px spread
- **Subtle borders:** `rgba(50, 50, 93, 0.07) 0px 0px 0px 1px`
- **Hover states:** Additional shadow layers

### Animation Strategy:
- **Property:** Usually opacity or background-color (not transform)
- **Duration:** 0.15s (fast enough to feel instant)
- **Easing:** Custom cubic-bezier for natural feel
- **Philosophy:** Subtle feedback, not flashy effects

---

## Recommendations for Reuse

### What to Copy Exactly:
1. ✅ Shadow system (multi-layer approach)
2. ✅ Transition timing (0.15s + custom easing)
3. ✅ Border radius values (16.5px distinctive)
4. ✅ Color palette structure (brand + navy + accents)

### What to Adapt:
1. 🔧 Purple → Your brand color
2. 🔧 Sohne font → Your chosen typeface
3. 🔧 Specific padding values → Match your content density

### What to Avoid:
1. ❌ Don't copy purple if you want to differentiate
2. ❌ Don't use same shadows if targeting different emotion (e.g., playful vs. professional)
3. ❌ Don't use same spacing if your content needs different density

---

**End of Analysis**
