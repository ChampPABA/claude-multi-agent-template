# Extraction Steps

---

## STEP 0: Parse Input & Setup

1. Validate URL — if missing, error: "URL required. Usage: /extract https://airbnb.com"
2. Normalize — trim whitespace, add `https://` if missing
3. Extract site name — remove `www.` and TLD (e.g., `www.airbnb.com` → `airbnb`)
4. Check existing — if `design-system/extracted/{siteName}/data.yaml` exists, ask user to re-extract or keep
5. Create dirs: `mkdir -p design-system/extracted/{siteName}/screenshots`

---

## STEP 1: Open page + trigger lazy content

```bash
agent-browser open {url}
```

Wait for page load. If redirect occurs, verify final URL is the intended site.

Then scroll the page to bottom and back to top. Many sites lazy-load CSS and content on scroll — if we extract before scrolling, we'll miss stylesheets, images, and components that only load when visible. This single scroll pass ensures all lazy resources are loaded before extraction begins.

---

## STEP 2: Extract data (3 focused calls)

Split extraction into 3 focused calls rather than 1 mega call. Each call has a clear scope, which produces more thorough extraction per category. Writing 80-100 lines of focused JS per call gives better results than 200+ lines trying to do everything at once.

**Resilience tips (apply to all 3 calls):**
- Wrap each category in try/catch — if one fails, continue with others and return partial data.
- For stylesheet parsing, skip cross-origin stylesheets that throw SecurityError.

### Call 1: Visual styles (via getComputedStyle)

Sample top 50-100 visible elements. Return as JSON.

| # | Key | What to Extract |
|---|-----|-----------------|
| 1 | `colors` | backgroundColor, color, borderColor → RGB to HEX + frequency count. Skip transparent. Include all shades — dark mode sites often have many near-black variants that matter. |
| 2 | `typography` | fontSize, fontWeight, fontFamily, lineHeight, letterSpacing on h1-h6 + p + button + a + span. Collect unique fonts (especially custom/variable fonts), all weights (including non-standard like 510, 590), full size scale. |
| 3 | `shadows` | All boxShadow values from elements. Include offset shadows (e.g., `4px 4px 0px` = neo-brutalist), layered shadows (multiple values), and ring shadows (`0 0 0 Npx`). A single offset shadow still counts as a shadow system — don't skip it. |
| 4 | `spacing` | padding, margin, gap values. Detect grid base (4px or 8px). Skip "auto". |
| 5 | `borders` | borderRadius (including 9999px pills and 50% circles), borderWidth (1px vs 2-3px = different design language), borderColor. |
| 6 | `components` | Query buttons (`button, a[role="button"], .btn, [class*="button"]`), cards (`[class*="card"], article`), inputs (`input, textarea, select`). Add `data-extract-id` attribute to each. Capture all computed styles + transition properties. |
| 7 | `layout` | Container widths, grid columns, max-width on main containers. Parse media query breakpoints from accessible stylesheets. |

### Call 2: Stylesheet analysis (via document.styleSheets)

Parse all accessible stylesheets. Return as JSON.

| # | Key | What to Extract |
|---|-----|-----------------|
| 8 | `keyframes` | All `CSSKeyframesRule` entries — name + full CSS text. Include ALL keyframes, even library-specific ones (Toastify__, swiper-, sonner-). |
| 9 | `transitions` | transition, transitionDuration, transitionTimingFunction, transitionProperty from elements. Identify signature easing curves (custom cubic-bezier = design intent). |
| 10 | `css_animations` | animationName, animationDuration, animationDelay, animationIterationCount, animationTimingFunction from elements. |
| 11 | `hover_rules` | All rules with `:hover` selector — extract the property changes. |
| 12 | `focus_rules` | All rules with `:focus`, `:focus-visible`, `:focus-within` selector. |
| 13 | `loading_patterns` | See "Detecting loading & feedback states" below. |
| 14 | `feedback_patterns` | See "Detecting loading & feedback states" below. |
| 15 | `css_custom_props` | All `--*` custom properties. Search on `:root`, `html`, `body`, `[data-theme]`, and `document.documentElement`. CSS-in-JS frameworks often place variables on specific elements rather than `:root`, so checking multiple targets catches more. Group by category: `--color-*`, `--font-*`, `--spacing-*`, `--shadow-*`, `--transition-*`, `--animation-*`, `--easing-*`, `--radius-*`. |

### Call 3: DOM structure (via querySelectorAll)

Query the live DOM. Return as JSON.

| # | Key | What to Extract |
|---|-----|-----------------|
| 16 | `icons` | `svg` count + viewBox sizes, `[class*="icon"]`, `i[class*="fa"]`, icon `<img>` elements. Detect icon system: inline-svg, icon-font (@font-face with icon-related name), or img-based. |
| 17 | `forms` | `form`, `input`, `select`, `textarea`, `label` elements. Detect form types (newsletter/search/login/contact), layout patterns, validation attributes (required, pattern, min/max). |
| 18 | `accessibility` | Count all `aria-*` attributes (break down by type: aria-label, aria-hidden, aria-expanded, etc.), `role` attributes (list unique roles), `tabindex` elements. List semantic HTML tags present: nav, main, footer, header, section, article, aside. Note which are missing. |
| 19 | `animation_libs` | Check `script[src]` for: gsap, framer-motion, lottie, anime.js, three.js, rive. Check DOM for: `lottie-player`, `spline-viewer`, `[data-framer-component-type]`, `canvas[data-engine]`. |
| 20 | `scroll_animations` | `[data-aos]`, `[data-scroll]`, `[data-animate]`, `.reveal`, `.animate-on-scroll`, `[data-intersection]` elements. Count and list animation types/values. |
| 21 | `bg_media` | `video[autoplay]`, `video[muted]`, `video[loop]`, `img[src$=".gif"]`, `source[type*="webm"]`, `lottie-player` elements. |
| 22 | `svg_animations` | `animate`, `animateTransform`, `animateMotion` elements inside SVGs (SMIL animations). Count and describe. |
| 23 | `alert_elements` | `[role="alert"]`, `[aria-live]` elements. |
| 24 | `navigation` | `nav` elements, `header` nav structure, menu items (`a` inside `nav`), dropdown menus (`[aria-expanded]`), mobile menu toggle buttons. |
| 25 | `toast_libraries` | Detect installed toast/notification libraries by checking for their DOM footprint — even if no toast is currently showing, many libraries inject a container element on load. Check: `[class*="Toastify"]`, `[data-sonner-toaster]`, `.swal2-container`, `[class*="notistack"]`, `.notyf`, `[class*="hot-toast"]`, `[data-headlessui-state]`. Report which library is present. |

### Detecting loading & feedback states

Different CSS approaches use very different patterns. Class name matching alone won't work on Tailwind or CSS-in-JS sites. Use a layered detection approach so nothing slips through:

**Layer 1 — Stylesheet class/selector matching (traditional CSS):**
Search `document.styleSheets` rules for selectors containing: `error`, `success`, `warning`, `alert`, `toast`, `notification`, `loading`, `skeleton`, `spinner`, `shimmer`, `pulse`.

**Layer 2 — CSS property patterns (works on Tailwind + any framework):**
Search stylesheet rules for property value patterns that indicate states:
- Danger/error: rules using red-range colors (#ef4444, #dc2626, #f87171, rgb(239,68,68), etc.) on border or background
- Success: green-range colors (#22c55e, #16a34a, #4ade80)
- Warning: amber-range colors (#f59e0b, #d97706, #fbbf24)
- Spinners: `@keyframes` where the name or content contains `spin`, `rotate`, or has `transform: rotate(360deg)` / `rotate(1turn)`
- Skeletons: rules with `linear-gradient` + `background-size` animation pattern, or `@keyframes` with shimmer/pulse

**Layer 3 — DOM elements + data attributes (library-specific):**
Check for elements and attributes from common toast/notification libraries:
- Toastify: `[class*="Toastify"]`
- Sonner: `[data-sonner-toast]`, `[data-sonner-toaster]`
- react-hot-toast: `[data-hot-toast]`, `[role="status"]` near toast containers
- SweetAlert2: `.swal2-popup`, `.swal2-container`
- Notistack: `[class*="SnackbarContent"]`, `[class*="notistack"]`
- Notyf: `.notyf`, `.notyf__toast`
- HeadlessUI: `[data-headlessui-state]`
- Generic: `[data-state]`, `[data-status]`, `[data-type]` on notification-like elements

---

## STEP 3: Interactive states + toast trigger (SINGLE agent-browser execute call)

Write ONE JavaScript for all interactive states. Execute in a **SINGLE** call. Return as JSON.

1. **Toast trigger** — If a toast library was detected in STEP 2 Call 3 (`toast_libraries`), try to trigger it to force its CSS to load. Check if the library's global function exists and call it briefly:
   - Sonner: `typeof window.toast === 'function' && window.toast('test')`
   - Toastify: `typeof window.Toastify === 'function' && window.Toastify({text:'test',duration:100}).showToast()`
   - After triggering, wait 200ms, then capture any newly loaded stylesheet rules related to the toast library. Dismiss/remove the test toast immediately.
   - If the global function doesn't exist, skip — the library may be module-scoped.

2. **Hover diffs** — Loop elements with `data-extract-id`: capture default styles → `dispatchEvent(new MouseEvent('mouseenter'))` → wait transition duration (fallback 300ms) → capture hover styles → `dispatchEvent(new MouseEvent('mouseleave'))` → record diffs. Skip on failure, no retry.

3. **Focus rings** — `element.focus()` on 3-5 interactive elements → capture outline, box-shadow, border → `element.blur()`.

4. **Contrast ratios** — Calculate luminance ratio for primary text/background pairs. Flag WCAG AA (<4.5:1) and AAA (<7:1).

---

## STEP 4: Screenshot

Full-page screenshot (or viewport fallback). Save to `screenshots/full-page.png`. One screenshot is enough.

---

## STEP 5: Psychology analysis

Analyze screenshot + extracted data for:

| Field | What to Analyze |
|-------|-----------------|
| style_classification | Neo-Brutalism, Minimalist, Glassmorphism, etc. → see [style-detection.md](style-detection.md) |
| emotions_evoked | Feelings the design triggers and why |
| target_audience | Primary/secondary audience with demographics |
| visual_principles | Key design patterns observed |
| why_it_works | Strategic design decisions |
| design_philosophy | Core beliefs and principles |

---

## STEP 6: Generate data.yaml

1. Map extracted data to 17 output sections
2. Calculate coverage (X/17 sections)
3. `coverage.missing` is **required** — list all undetected section names
4. Write to `design-system/extracted/{siteName}/data.yaml`

→ See [output-format.md](output-format.md) for complete schema

---

## STEP 7: Final Report

Display: coverage %, psychology status, screenshot path, output path, next steps.
