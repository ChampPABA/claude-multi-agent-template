# Accessibility (a11y)

> **Purpose:** Make web applications usable by everyone, including people with disabilities

---

## WCAG Standards

**Web Content Accessibility Guidelines (WCAG) 2.1**

| Level | Compliance | Use Case |
|-------|------------|----------|
| **A** | Minimum | Basic accessibility (legal requirement in many countries) |
| **AA** | Recommended | Standard for most websites (target this) |
| **AAA** | Enhanced | Government, healthcare, education sites |

**Target:** WCAG 2.1 Level AA (industry standard)

---

## Four Principles (POUR)

### 1. Perceivable
**Users must be able to perceive the information**

- ✅ Text alternatives for images
- ✅ Captions for videos
- ✅ Color is not the only way to convey meaning
- ✅ Sufficient color contrast (4.5:1 minimum)

### 2. Operable
**Users must be able to operate the interface**

- ✅ Keyboard accessible (all functions work without mouse)
- ✅ No time limits (or adjustable timers)
- ✅ No flashing content (seizure risk)
- ✅ Skip navigation links

### 3. Understandable
**Users must be able to understand the content**

- ✅ Readable text (plain language)
- ✅ Predictable navigation
- ✅ Clear error messages with suggestions
- ✅ Labels for all form fields

### 4. Robust
**Content must be robust enough for assistive technologies**

- ✅ Valid HTML
- ✅ Semantic markup
- ✅ ARIA attributes when needed
- ✅ Works with screen readers

---

## Color Contrast

### WCAG Requirements

| Text Type | WCAG AA | WCAG AAA |
|-----------|---------|----------|
| Normal text (<18pt) | **4.5:1** | 7:1 |
| Large text (≥18pt or ≥14pt bold) | **3:1** | 4.5:1 |
| UI components (buttons, inputs) | **3:1** | N/A |

### Testing Tools

**Browser Extensions:**
- **WAVE** (WebAIM) - Visual feedback overlay
- **axe DevTools** - Comprehensive accessibility scanner
- **Lighthouse** (Chrome DevTools) - Automated audit

**Online Tools:**
- **WebAIM Contrast Checker**: https://webaim.org/resources/contrastchecker/
- **Contrast Ratio**: https://contrast-ratio.com/

### Examples

```css
/* ✅ PASS - 7:1 contrast */
background: white;    /* #FFFFFF */
color: black;         /* #000000 */

/* ✅ PASS - 4.6:1 contrast */
background: #0F2A4A;  /* Navy blue */
color: white;         /* #FFFFFF */

/* ❌ FAIL - 2.1:1 contrast */
background: #E0E0E0;  /* Light gray */
color: white;         /* #FFFFFF */

/* ❌ FAIL - 1.5:1 contrast */
background: white;
color: #E0E0E0;       /* Light gray text */
```

---

## Semantic HTML

**Use proper HTML elements for their intended purpose**

### DO (Semantic):

```html
<!-- ✅ Navigation -->
<nav>
  <ul>
    <li><a href="/">Home</a></li>
    <li><a href="/about">About</a></li>
  </ul>
</nav>

<!-- ✅ Main content -->
<main>
  <article>
    <h1>Article Title</h1>
    <p>Content...</p>
  </article>
</main>

<!-- ✅ Form -->
<form>
  <label for="email">Email:</label>
  <input type="email" id="email" name="email" required>
  <button type="submit">Submit</button>
</form>

<!-- ✅ Button -->
<button onclick="doSomething()">Click Me</button>
```

### DON'T (Non-semantic):

```html
<!-- ❌ Div soup -->
<div class="nav">
  <div class="nav-item">
    <span onclick="navigate('/')">Home</span>
  </div>
</div>

<!-- ❌ Divs for everything -->
<div class="main">
  <div class="article">
    <div class="title">Article Title</div>
    <div class="content">Content...</div>
  </div>
</div>

<!-- ❌ Div as button -->
<div onclick="doSomething()">Click Me</div>
```

**Why Semantic HTML Matters:**
- ✅ Screen readers understand structure
- ✅ Better SEO
- ✅ Keyboard navigation works automatically
- ✅ Easier to maintain

---

## Keyboard Navigation

**All interactive elements must be keyboard accessible**

### Tab Order

**Standard tab order:**
1. Links
2. Buttons
3. Form inputs (text, select, checkbox, radio)
4. Textareas

**Control tab order:**
```html
<!-- Natural tab order (top to bottom) -->
<button>First</button>
<button>Second</button>
<button>Third</button>

<!-- Custom tab order (avoid if possible) -->
<button tabindex="1">First</button>
<button tabindex="3">Third</button>
<button tabindex="2">Second</button>

<!-- Remove from tab order -->
<div tabindex="-1">Not focusable</div>

<!-- Make div focusable (use semantic HTML instead) -->
<div tabindex="0" role="button">Focusable div</div>
```

### Focus Indicators

**Always visible focus states:**

```css
/* ✅ Good focus indicator */
button:focus {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

/* ✅ Alternative (box-shadow) */
input:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgb(59 130 246 / 0.5);
}

/* ❌ NEVER remove focus without replacement */
*:focus {
  outline: none;  /* Makes keyboard navigation impossible */
}
```

### Skip Links

**Allow keyboard users to skip repetitive navigation:**

```html
<!-- Hidden visually but accessible to screen readers -->
<a href="#main-content" class="skip-link">
  Skip to main content
</a>

<nav>
  <!-- Navigation items -->
</nav>

<main id="main-content">
  <!-- Main content -->
</main>
```

```css
.skip-link {
  position: absolute;
  top: -40px;
  left: 0;
  background: var(--color-primary);
  color: white;
  padding: var(--spacing-2);
  z-index: 1000;
}

.skip-link:focus {
  top: 0;  /* Show on focus */
}
```

---

## ARIA (Accessible Rich Internet Applications)

**Use ARIA when semantic HTML is not enough**

### ARIA Roles

```html
<!-- ✅ Use semantic HTML first -->
<nav>Navigation</nav>
<main>Main content</main>
<aside>Sidebar</aside>

<!-- ⚠️ Use ARIA when semantic HTML unavailable -->
<div role="navigation">Navigation</div>
<div role="main">Main content</div>
<div role="complementary">Sidebar</div>

<!-- Common roles -->
<div role="button">Custom button</div>
<div role="alert">Important message</div>
<div role="dialog">Modal dialog</div>
<div role="search">Search form</div>
```

### ARIA Labels

```html
<!-- Button with no visible text -->
<button aria-label="Close dialog">
  <svg><!-- X icon --></svg>
</button>

<!-- Icon-only link -->
<a href="/profile" aria-label="Go to profile">
  <svg><!-- User icon --></svg>
</a>

<!-- Describe element -->
<button aria-describedby="help-text">
  Submit
</button>
<p id="help-text">
  This will send your form data
</p>
```

### ARIA States

```html
<!-- Expanded/collapsed -->
<button aria-expanded="false" aria-controls="menu">
  Menu
</button>
<div id="menu" hidden>
  <!-- Menu items -->
</div>

<!-- Checked (custom checkbox) -->
<div role="checkbox" aria-checked="true">
  I agree to terms
</div>

<!-- Hidden from screen readers -->
<div aria-hidden="true">
  Decorative content
</div>

<!-- Current page in navigation -->
<nav>
  <a href="/" aria-current="page">Home</a>
  <a href="/about">About</a>
</nav>
```

### ARIA Live Regions

**Announce dynamic content changes:**

```html
<!-- Polite (wait for user to finish) -->
<div aria-live="polite">
  3 new messages
</div>

<!-- Assertive (interrupt immediately) -->
<div aria-live="assertive" role="alert">
  Error: Form submission failed
</div>

<!-- Atomic (read entire region) -->
<div aria-live="polite" aria-atomic="true">
  Loading: 45% complete
</div>
```

---

## Form Accessibility

### Labels

**Always associate labels with inputs:**

```html
<!-- ✅ Method 1: for/id -->
<label for="username">Username:</label>
<input type="text" id="username" name="username">

<!-- ✅ Method 2: Wrapping -->
<label>
  Email:
  <input type="email" name="email">
</label>

<!-- ❌ No association -->
<span>Password:</span>
<input type="password" name="password">
```

### Required Fields

```html
<!-- ✅ HTML5 required -->
<label for="email">Email (required):</label>
<input type="email" id="email" name="email" required>

<!-- ✅ ARIA required -->
<label for="phone">Phone:</label>
<input type="tel" id="phone" name="phone" aria-required="true">

<!-- ✅ Visual indicator + text -->
<label for="name">
  Name <span aria-label="required">*</span>
</label>
<input type="text" id="name" name="name" required>
```

### Error Messages

```html
<!-- ✅ Associate error with input -->
<label for="email">Email:</label>
<input
  type="email"
  id="email"
  name="email"
  aria-invalid="true"
  aria-describedby="email-error"
>
<p id="email-error" role="alert">
  Please enter a valid email address
</p>
```

### Fieldsets

**Group related inputs:**

```html
<fieldset>
  <legend>Shipping Address</legend>

  <label for="street">Street:</label>
  <input type="text" id="street" name="street">

  <label for="city">City:</label>
  <input type="text" id="city" name="city">
</fieldset>
```

---

## Image Accessibility

### Alt Text

```html
<!-- ✅ Descriptive alt text -->
<img
  src="sunset.jpg"
  alt="Orange sunset over ocean with waves crashing on rocks"
>

<!-- ✅ Decorative image (empty alt) -->
<img src="decorative-line.svg" alt="">

<!-- ✅ Functional image (describe function) -->
<button>
  <img src="trash.svg" alt="Delete item">
</button>

<!-- ❌ Missing alt -->
<img src="important.jpg">

<!-- ❌ Redundant alt -->
<img src="photo-sunset.jpg" alt="Image of sunset">
```

### Complex Images

```html
<!-- Chart or infographic -->
<figure>
  <img
    src="sales-chart.png"
    alt="Bar chart showing quarterly sales"
    aria-describedby="chart-desc"
  >
  <figcaption id="chart-desc">
    Q1: $10k, Q2: $15k, Q3: $12k, Q4: $18k
  </figcaption>
</figure>
```

---

## Modal Dialogs

**Accessible modal implementation:**

```html
<div
  role="dialog"
  aria-labelledby="dialog-title"
  aria-modal="true"
>
  <h2 id="dialog-title">Confirm Action</h2>
  <p>Are you sure you want to delete this item?</p>

  <button>Cancel</button>
  <button>Delete</button>
</div>
```

```javascript
// Focus management
function openModal(modalId) {
  const modal = document.getElementById(modalId);
  const focusableElements = modal.querySelectorAll(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
  );

  // Store last focused element
  const lastFocused = document.activeElement;

  // Show modal
  modal.removeAttribute('hidden');

  // Focus first element
  focusableElements[0].focus();

  // Trap focus inside modal
  modal.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      closeModal(modalId);
    }

    if (e.key === 'Tab') {
      // Trap focus (cycle through focusable elements)
    }
  });
}

function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  modal.setAttribute('hidden', '');

  // Return focus to trigger element
  lastFocused.focus();
}
```

---

## Best Practices

### DO:
- ✅ Use semantic HTML elements
- ✅ Ensure 4.5:1 contrast for text
- ✅ Provide text alternatives for images
- ✅ Make all functionality keyboard accessible
- ✅ Use visible focus indicators
- ✅ Associate labels with form inputs
- ✅ Test with screen readers (NVDA, JAWS, VoiceOver)
- ✅ Add ARIA attributes when semantic HTML insufficient

### DON'T:
- ❌ Use color alone to convey meaning
- ❌ Remove focus indicators without replacement
- ❌ Use divs/spans for interactive elements
- ❌ Forget alt text on images
- ❌ Auto-play videos with sound
- ❌ Use ARIA when semantic HTML exists
- ❌ Forget to test with keyboard only
- ❌ Rely only on automated testing (manual testing crucial)

---

## Testing Checklist

### Automated Testing

- [ ] Run Lighthouse audit (Chrome DevTools)
- [ ] Run axe DevTools extension
- [ ] Run WAVE extension
- [ ] Check HTML validation (W3C Validator)

### Manual Testing

- [ ] Navigate entire site with keyboard only (no mouse)
- [ ] Test with screen reader (NVDA/JAWS/VoiceOver)
- [ ] Zoom to 200% (content should reflow, not scroll horizontally)
- [ ] Test color contrast (all text/UI components)
- [ ] Disable images (alt text should convey meaning)
- [ ] Test forms (labels, errors, validation)

### Device Testing

- [ ] Desktop browsers (Chrome, Firefox, Safari, Edge)
- [ ] Mobile browsers (iOS Safari, Chrome Mobile)
- [ ] Screen readers (NVDA on Windows, VoiceOver on macOS/iOS)
- [ ] Keyboard-only navigation
- [ ] Touch screen navigation

---

## Quick Reference

**Contrast Ratios:**
| Element | Minimum Ratio |
|---------|---------------|
| Normal text | 4.5:1 (AA) |
| Large text | 3:1 (AA) |
| UI components | 3:1 (AA) |

**Keyboard Shortcuts:**
| Key | Action |
|-----|--------|
| Tab | Move to next focusable element |
| Shift + Tab | Move to previous element |
| Enter | Activate button/link |
| Space | Toggle checkbox, activate button |
| Esc | Close modal/dialog |
| Arrow keys | Navigate within component |

**ARIA Landmarks:**
| Role | Semantic HTML |
|------|---------------|
| `role="navigation"` | `<nav>` |
| `role="main"` | `<main>` |
| `role="complementary"` | `<aside>` |
| `role="contentinfo"` | `<footer>` |
| `role="banner"` | `<header>` |

---

**💡 Remember:** Accessibility benefits everyone, not just people with disabilities!
