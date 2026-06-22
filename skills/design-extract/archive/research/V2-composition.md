# V2 Composition: Page-Section Anatomy + Navigation Behavior Detection

> **Source:** NotebookLM deep-research notebook "V2: page anatomy + nav behavior detection" (181 web sources imported, 2026-06-22).
> **Primary cited report:** "Computational Detection of Webpage Layout Anatomy and Dynamic Navigation Behaviors" (NotebookLM-synthesized, reference ID `c1e403d4-5b05-4e70-9fe4-173f4b0ed3a9`, citation scores 0.99-1.0 across follow-ups).
> **Method:** `notebooklm source add-research --mode deep --import-all` + 4 follow-up `ask --json` queries capturing `references[].cited_text`.
> **Caveat:** The synthesized research report (`c1e403d4`) is itself NotebookLM's aggregation of 50 underlying web sources (listed in §Source Index below). Inline numeric markers like `[1]`, `[22]` reference that report's citation index. Treat second-order; where the underlying source is a peer-reviewed paper or MDN, confidence is HIGH. Where it is a Medium/Reddit/Forum post, confidence is MEDIUM and signals should be validated against a real DOM before shipping.

---

## 1. Section-Type Classification Signal Table

| Section type | DOM / computed-style / content signal | Confidence | Pitfalls |
|---|---|---|---|
| **Header / nav** | `<header>` or `<nav>` semantic tag **+** bounding-box `y` near 0 **+** `position: fixed\|sticky` **+** high anchor-tag density, low text-to-link ratio [19,20,21] | HIGH | Semantic tag alone is unreliable; must confirm `getBoundingClientRect().top ≈ 0`. Some sites inject `sticky` via JS scroll listener, not initial CSS — see §3 sticky validation. |
| **Hero (centered)** | Parent `text-align: center` **+** Flexbox/Grid `justify-content: center` / `align-items: center` **+** vertically stacked heading+sub+CTA [19,21] | HIGH | "Centered" can be visual-only via margins; check computed `text-align` and flex alignment, not just layout. |
| **Hero (split)** | Two non-overlapping child columns, each ~45-50% parent width, adjacent on same horizontal plane; one column = copy+CTA, other = image/product [22] | HIGH | Must verify column widths via `getBoundingClientRect()` — `display:flex` alone doesn't guarantee 50/50 split. Three-column "split" is a different subtype. |
| **Hero (full-bleed-image)** | Parent bbox `width >= 95vw` AND `height >= 80vh` **+** `background-size: cover` OR absolute-positioned child `<img>` matching parent dimensions [19] | HIGH | `100vw` includes scrollbar width on desktop; use `95vw` threshold. Background-image vs `<img>` tag are equivalent signals. |
| **Hero (video-bg)** | Full-bleed container + child `<video>` with `muted`, `loop`, `autoplay`, absolute-positioned, `z-index < 0` [19] | HIGH | Some players use `<canvas>` or WebGL instead — those are "canvas hero," a rarer subtype not covered by sources. **UNVERIFIED** for canvas/WebGL heroes. |
| **Hero (product)** | Split hero layout **+** media column has gallery/carousel/zoom **+** text column has price nodes + "Add to Cart" / "Buy Now" CTA signatures [23,24,25] | MEDIUM | CTA keyword matching is fragile (i18n, custom copy). Carousel detection requires checking for `[aria-live]` or transform-style transitions. |
| **Hero (stat)** | Horizontal grid of metrics, `font-size >= 40px`, `font-weight: 700`, large numbers + smaller labels [19] | MEDIUM | The `>= 40px` threshold is from the synthesized report, **not empirically validated** against real sites. Stat rows also appear as standalone sections, not just heroes. |
| **Logo strip** | Grid/flex row, height `40-120px`, high density of inline `<img>`/`<svg>`, consistent dimensions/aspect ratios, **zero text nodes** [16,26,27] | HIGH | Grayscale/opacity signal in the existing draft (`filter:grayscale` or low opacity) is **not cited** as a reliable signal in the research — dimensions + zero-text + low-height is the supported signature. Grayscale is common but optional. |
| **Feature grid** | `display: grid` + equal-width columns (`repeat(3, 1fr)`) or wrapping flex **+** immediate children have **nearly identical bbox heights and widths** [4,16,21] | HIGH | The "identical child dimensions" check is the disambiguator vs bento. Must measure `getBoundingClientRect()` on children. |
| **Bento grid** | `display: grid` + (any of): `grid-template-areas` with repeating identifiers, `grid-auto-flow: dense`, or children with `grid-column-start/end` or `grid-row-start/end` containing `span` [16,17,22] | HIGH | See §2 for the verbatim detection function. The `grid-auto-flow: dense` signal alone is **weaker** than explicit `grid-template-areas` or span rules — some uniform grids use `dense` for packing. |
| **Testimonial** | `<blockquote>` semantic tag OR classpath keywords (`quote`, `review`, `testimonial`) OR italicized font-style **+** avatar images (`border-radius: 50%`) **+** star ratings (5 repeating SVG/vector icons) [18,24] | MEDIUM | Class-keyword matching is fragile. The strongest combined signal is blockquote + circular avatar + star-icon row. Lone blockquotes appear in non-testimonial contexts (article quotes). |
| **Pricing** | Grid sibling elements + currency symbols (`$`,`€`,`£`) paired with large numeric fonts + billing intervals (`/mo`, `per year`, `annually`) + CTAs ("Start Trial", "Choose Plan") + siblings share identical heights + matching bullet feature lists [23,28,29] | MEDIUM | Currency regex misses SaaS showing only "$12" without symbol context. The "identical sibling heights + matching bullet lists" structural signal is more reliable than price regex alone. |
| **CTA band** | Narrow, full-width section + `background-color` distinctly differing from adjacent sections + centered prominent heading + minimal supporting text + single stylized button targeting action URL [4,21] | MEDIUM | "Contrasting bg" requires comparing computed bg against previous section's bg — not a standalone property. The single-button + minimal-text signal is stronger than contrast. |
| **FAQ accordion** | Multi-layered check: (1) stacked siblings with bold interactive triggers + trailing `+` or `v` icons; (2) hidden answer containers with computed `height: 0px` OR `display: none` OR `visibility: hidden`; (3) WAI-ARIA: trigger `aria-expanded="false"`, panel `aria-hidden="true"`; (4) **behavioral**: click trigger → `aria-expanded` flips to `true`, `aria-hidden` to `false`, child height → `scrollHeight` [30,31,32] | HIGH | The existing draft's `<details>` signal is **incomplete** — many FAQ components are JS-driven divs, not native `<details>`. The behavioral click-test (layer 4) is the most reliable confirmation. `<details>` is a sufficient but not necessary signal. |
| **Footer** | `<footer>` semantic tag **+** positional: bottom 15% zone of page height **+** content signature: dense vertical link-list columns, social links, copyright, "Privacy Policy" [4,19] | HIGH | `<footer>` alone can match multiple per page (section footers). The bottom-15% positional check + link-list density disambiguates the page footer. |

**Citations (numeric refs map to the synthesized report's source index):**
- [4] Medium — Architecting High-Performance CSS (landing-page anatomy)
- [16] Banani AI — Bento Grid explained
- [17] Medium — CSS Grid Bento UI
- [18] Semantic Scholar — Content-based Title Extraction
- [19] tdcommons — Layout-Aware Text Extraction (heuristic segmentation; **peer-reviewed**, HIGH confidence for positional/footer/header signals)
- [20] dainemawer — Determine When Sticky Element is Stuck
- [21] MDN — Box Model
- [22] wearedevelopers — Building Bento Grid Layout with Modern CSS Grid
- [23] ProxyScrape — Scrape Prices from Websites
- [24] Scrapfly — Track Competitor Pricing
- [25] TestMu AI — Playwright JavaScript
- [26] MDN — CSS Selectors
- [27] Univ. Manchester — Analysing Visual Complexity of Web Pages (**peer-reviewed**, HIGH confidence for density/airiness model)
- [28] Reddit r/webscraping — pricing extraction
- [29] Octoparse — Price Scraping
- [30] Reddit r/webdev — FAQ accordion
- [31] Stack Overflow — FAQ accordion show/hide
- [32] a11y with Lindsey — JavaScript and Accessibility: Accordions

---

## 2. Bento vs Feature-Grid Disambiguation

**Verbatim detection logic (from source `c1e403d4`, score 1.0):**

The disambiguation hinges on **grid architecture**, not visual appearance. Both use `display: grid` — the difference is whether children are uniform or asymmetrically placed.

**Feature Grid** — uniform repeating cards:
- `display: grid` + equal-width columns (e.g. `grid-template-columns: repeat(3, 1fr)`) OR wrapping flex
- **Immediate children have nearly identical bbox heights and widths** [22]
- No `grid-template-areas`, no `span` on children

**Bento Grid** — asymmetric compartments. A grid is classified bento if **any** of these hold:
1. `grid-template-areas` is non-`none` AND contains a row where the same area-name spans multiple cells (i.e. `new Set(cells).size < cells.length` for at least one row) [22]
2. Any child has `grid-column-start/end` or `grid-row-start/end` containing `span` [22]
3. `grid-auto-flow` === `dense` [22] — **weakest signal alone**, some uniform grids use dense packing

**Pitfall flagged:** Signal #3 alone (`grid-auto-flow: dense`) is the most error-prone — it produces false positives on uniform grids that use dense packing for fill. Require #1 or #2 for high confidence. Best practice: require at least two of the three, OR #1/#2 alone.

**Reference code structure (paraphrased from source, verbatim was truncated in citation):**
```js
function classifyGrid(el) {
  const s = getComputedStyle(el);
  if (s.display !== 'grid') return null;

  // Signal 1: grid-template-areas with repeating names
  const areas = s.gridTemplateAreas;
  const hasAreaSpans = areas && areas !== 'none' &&
    areas.match(/"([^"]+)"/g).some(row => {
      const cells = row.replace(/"/g,'').trim().split(/\s+/);
      return new Set(cells).size < cells.length;
    });

  // Signal 2: any child with col/row span
  const children = Array.from(el.children);
  const hasVaryingSpans = children.some(c => {
    const cs = getComputedStyle(c);
    return [cs.gridColumnStart, cs.gridColumnEnd, cs.gridRowStart, cs.gridRowEnd]
      .some(v => String(v).includes('span'));
  });

  // Signal 3: dense auto-flow (weak alone)
  const denseFlow = s.gridAutoFlow === 'dense';

  // Children uniform? (feature-grid signal)
  const bboxes = children.map(c => c.getBoundingClientRect());
  const uniform = bboxes.every(b =>
    Math.abs(b.width - bboxes[0].width) < 5 &&
    Math.abs(b.height - bboxes[0].height) < 5
  );

  if (uniform && !hasAreaSpans && !hasVaryingSpans) return 'feature-grid';
  if (hasAreaSpans || hasVaryingSpans) return 'bento';
  if (denseFlow && !uniform) return 'bento';
  return 'feature-grid';
}
```

---

## 3. Navigation Behavior Detection Protocol

### 3.1 Sticky / pinned

`position: sticky|fixed` in initial CSS is **necessary but not sufficient** — some sites inject sticky via scroll-listener JS classes [20,39]. Two validation methods:

**Method A — Programmatic scroll sample (cited, score 1.0):**
1. Record `Y_initial = header.getBoundingClientRect().top` at scrollY=0
2. `window.scrollTo(0, 500)`
3. Record `Y_scrolled = header.getBoundingClientRect().top`
4. If `Y_scrolled` remains locked to top offset (~0) → sticky confirmed [20,39]

**Method B — IntersectionObserver boundary trick (cited, score 1.0):**
Inject an `IntersectionObserver` on the header with `-1px` top offset; if `intersectionRatio < 1` after a micro-scroll, the header is stuck [39]. Lighter than full scroll-sample, but requires JS injection.

**Recommendation:** Use Method A — it reuses the same scroll infrastructure needed for §3.3 transparent-to-solid detection.

### 3.2 Transparent-over-hero

Cited detection (source `c1e403d4`, ref [35]):
1. Header `position` is `absolute` or `fixed`
2. Header bbox **overlaps** hero container bbox
3. Header `background-color` alpha == 0 OR `background` resolves to `transparent`

### 3.3 Transparent-to-solid-on-scroll (alpha sampling)

**This is the core cited method (source `c1e403d4`, score 1.0).** The exact `scrollY=0` vs `scrollY=400` protocol from the existing §2.3 draft is **supported by the research**:

```js
async function detectTransparentToSolid(page, selector) {
  // Step 1: scroll to top
  await page.evaluate(() => window.scrollTo(0, 0));
  const bgAtZero = await page.evaluate(sel =>
    getComputedStyle(document.querySelector(sel)).backgroundColor, selector);
  const alphaAtZero = parseAlpha(bgAtZero);

  // Step 2: scroll past hero threshold (400px is the cited value)
  await page.evaluate(() => window.scrollTo(0, 400));
  await page.waitForTimeout(200);  // wait for CSS opacity transition
  const bgAtScrolled = await page.evaluate(sel =>
    getComputedStyle(document.querySelector(sel)).backgroundColor, selector);
  const alphaAtScrolled = parseAlpha(bgAtScrolled);

  return alphaAtZero < 0.2 && alphaAtScrolled > 0.8;
}

function parseAlpha(c) {
  if (c === 'transparent') return 0;
  const m = c.match(/rgba?\(.*,\s*([\d.]+)\)/);
  return m ? parseFloat(m[1]) : 1;  // default 1 for opaque rgb()
}
```

**Cited thresholds:** `alphaAtZero < 0.2 && alphaAtScrolled > 0.8` [c1e403d4]. The `scrollY=400` value and the 200ms transition-wait are in the source.

**Pitfall (NOT in research — flagging from domain knowledge):** Sites using Lenis/Locomotive smooth-scroll hijack native scroll, so `window.scrollTo` may not move the actual viewport. The existing §3 motion research already documents this; the extract skill must use the driver's native wheel-input or `page.mouse.wheel` rather than `window.scrollTo` on hijacked pages. **UNVERIFIED by this NotebookLM run** — the research did not address scroll-hijack interaction.

### 3.4 Glass / backdrop-filter blur

Cited (source `c1e403d4`, score 0.99):
> "A frosted glass visual effect, programmatically identified when the navigation container's computed `backdrop-filter` property contains a valid `blur(...)` filter (e.g. `backdrop-filter: blur(8px)`) **alongside a semi-transparent background color**."

**Both conditions required** — `backdrop-filter: blur` alone without translucent bg is not glass (it's just blur). Check `backdrop-filter` string contains `blur(` AND bg-color alpha is between 0 and ~0.7.

### 3.5 Center-logo vs left-logo

- **Center-logo:** logo element's horizontal midpoint == header container's vertical center axis; nav links flank logo in separate containers on both sides
- **Left-logo:** logo at far-left edge; links/CTAs aligned right via flexbox `justify-content: space-between` [4,21]

### 3.6 Mega-menu

Programmatic hover/click on primary nav links → wait for layout transition → expanded menu container bbox `width >= 60%` of viewport [25,41].

### 3.7 Mobile hamburger overlay

Emulate mobile viewport (`width < 768px`) → confirm desktop links hidden (`display: none` or off-screen) → click hamburger → drawer slides in (verify via `transform` matrix change or visibility flip) [33,35,42,43].

---

## 4. Computable vs Visual-Judgment Split

**Directly computable from CSS/DOM (HIGH confidence, no screenshot needed):**
- Aesthetic values: bg colors, border styles, opacities, font weights [c1e403d4 score 1.0]
- Computed dimensions: bbox coords `(x, y, width, height)` from layout engine [c1e403d4 score 1.0]
- Layout frameworks: `display: grid`, `grid-template-areas`, `grid-auto-flow` [c1e403d4 score 1.0]
- Glass/blur: `backdrop-filter: blur(...)` string presence [c1e403d4 score 0.99]
- All nav behaviors in §3 (sticky, transparent, glass, logo position, mega-menu, mobile drawer)
- All section-type classifications in §1 (these are computable; "visual judgment" below is about *qualities*, not *types*)

**Visual heuristics — require mathematical modeling over multiple elements (MEDIUM confidence; the formulas exist but thresholds are not empirically validated against real design taxonomy):**

> "Attributes like airiness, complexity, and balance cannot be read directly from a single computed style property." [c1e403d4 score 1.0, citing ref 27 Univ. Manchester peer-reviewed paper]

**Airiness Ratio (AR)** — cited formula [c1e403d4 score 0.97, from ref 27 peer-reviewed]:

$$AR = 1 - \frac{\sum_{i=1}^{N} \text{Area}(B_i \cap V)}{\text{Area}(V)}$$

Where `V` = active viewport, `B_i` = bbox of each "contentful" element (visible text nodes, active images, opaque vector graphics). Cited thresholds: `AR >= 0.45` = airy/minimal; `AR <= 0.20` = dense. **These thresholds are from the synthesized report citing ref 27 — UNVERIFIED empirically against modern SaaS design. Flag as provisional.**

**Balance Score (BS)** — cited formula [c1e403d4 score 1.0, refs 45/46]:

$$BS = 1 - \frac{\left| \sum_{j \in L} w_j h_j x_{\text{offset},j} - \sum_{k \in R} w_k h_k x_{\text{offset},k} \right|}{\sum_{i=1}^{M} w_i h_i x_{\text{offset},i}}$$

Where `L`/`R` = elements left/right of central axis `X_axis = W_container/2`, `w_i`/`h_i` = element width/height, `x_offset,i` = horizontal distance from element center to axis. `BS → 1.0` = balanced.

**Proportion Score (PS)** — cited formula [c1e403d4 score 0.99, refs 45/46]:

$$PS = \frac{1}{N} \sum_{i=1}^{N} \left| \frac{w_i}{h_i} - \phi \right|$$

Where `φ ≈ 1.618` (golden ratio). Measures conformity to aesthetic ratios.

**Split verdict:**
| Field | Classification | Source |
|---|---|---|
| Grid geometry, nav behavior, section type, colors, dimensions, glass | **Computable** | Direct CSS/DOM |
| Airiness/density | **Visual heuristic** (formula exists, thresholds provisional) | AR formula, ref 27 |
| Symmetry/balance | **Visual heuristic** (formula exists) | BS formula, refs 45/46 |
| Proportion | **Visual heuristic** (formula exists) | PS formula, refs 45/46 |

**Practical recommendation for the extract skill:** Compute AR/BS/PS as numeric values (the formulas are deterministic from bboxes), but **do not bucket them into "airy/balanced/dense" labels automatically** — the thresholds are unvalidated. Instead, emit the raw scores and let the vision/screenshot pass (or a human) assign the qualitative label. This matches the existing draft's `visual_notes` field being "vision-filled."

---

## 5. Corrections to Existing §2 Draft (`RESEARCH-completeness.md`)

Comparing the captured research against the current §2 (lines 110-192):

| Draft claim | Verdict | Correction |
|---|---|---|
| Hero = "first large section after header; largest font-size text; min-height >= 60vh" | **PARTIALLY UNSUPPORTED** | The `60vh` threshold is **not in the research**. Cited hero detection is "first prominent section below header" + per-subtype bbox rules (full-bleed needs `>= 80vh`, not 60vh). The `60vh` figure is **UNVERIFIED** — lower it or remove. |
| Hero subtypes listed as "centered / split / full-bleed-image / video-bg / product / stat" | **CORRECT** | All six subtypes confirmed with specific detection signals (§1). |
| Logo strip = "row of `<img>` with `filter:grayscale` or low opacity" | **MOSTLY WRONG / OVERSPECIFIC** | Grayscale/opacity is **not a cited reliable signal**. Cited signature is: grid/flex row, height `40-120px`, high density of inline img/SVG, consistent dimensions, **zero text nodes** [16,26,27]. Grayscale is common but optional — remove it as a primary signal. |
| Feature grid = "grid of cards: icon + title + text" | **UNDER-SPECIFIED** | Content signature (icon+title+text) is secondary. Primary signal: `display:grid` equal-width cols **+ immediate children with nearly identical bbox dimensions** [22]. Add the uniformity check. |
| Bento grid = "grid with varying col-span/row-span / grid-template-areas" | **CORRECT but incomplete** | Add `grid-auto-flow: dense` as a third (weaker) signal [22]. See §2 — but flag dense-alone as low-confidence. |
| Testimonial = "quote + avatar + name pattern" | **UNDER-SPECIFIED** | Add: `<blockquote>` semantic tag, classpath keywords, italicized font-style, circular avatar (`border-radius: 50%`), 5-star rating row [18,24]. |
| FAQ = "`<details>` or `[aria-expanded]` accordion" | **INCOMPLETE** | Native `<details>` is sufficient-but-not-necessary. Most modern FAQ accordions are JS-driven divs. The **behavioral click-test** (click trigger → `aria-expanded` flips, height → scrollHeight) is the reliable confirmation [30,31,32]. Add the 4-layer check from §1. |
| Footer = "`<footer>`" | **UNDER-SPECIFIED** | Add positional check (bottom 15% of page height) + content signature (link-list columns, social, copyright, "Privacy Policy") [4,19]. |
| Nav `transparent-to-solid-on-scroll` = "alpha 0 at top, ~1 after scroll" | **CORRECT, well-supported** | The `scrollY=0` vs `scrollY=400` alpha-sampling protocol is directly cited (§3.3). Thresholds `alpha < 0.2` at top and `> 0.8` scrolled are in the source. **Add the 200ms transition-wait** — the draft omits it. |
| Nav glass = "`backdrop-filter: blur(...)`" | **PARTIALLY WRONG** | Glass requires `backdrop-filter: blur(...)` **AND** a semi-transparent bg color [c1e403d4 score 0.99]. The draft's check is necessary-but-not-sufficient. Add the bg-alpha check. |
| Mega-menu = "large dropdown panels" | **UNDER-SPECIFIED** | Cited: programmatic hover/click + expanded menu bbox `width >= 60%` viewport [25,41]. Add the width threshold. |
| `visual_notes: density (airy\|balanced\|dense), symmetry` | **SUPPORTED but thresholds unvalidated** | The AR/BS/PS formulas exist (§4) but the qualitative buckets ("airy/dense") use provisional thresholds (`AR >= 0.45` / `<= 0.20`) that are **not empirically validated** against modern design. Recommend: emit raw scores, let vision pass assign labels. |

**Net summary of corrections:**
1. **Hero min-height threshold `60vh` is unverified** — full-bleed subtype cites `80vh`; the generic `60vh` has no source. Remove or re-anchor.
2. **Logo-strip grayscale signal is wrong/overspecific** — replace with height+density+uniform-dimensions+zero-text signature.
3. **FAQ detection is incomplete** — add the 4-layer check including behavioral click-test; native `<details>` alone misses JS-driven accordions.
4. **Glass detection is incomplete** — add the semi-transparent bg-color requirement (not just backdrop-filter).
5. **Bento "dense" signal is under-flagged** — add `grid-auto-flow: dense` but mark it weak-alone.
6. **Nav scroll-wait is missing** — add the 200ms transition-wait between scrollY=0 and scrollY=400 reads.
7. **Density/symmetry thresholds are provisional** — formulas are cited but the airy/dense cutoffs need empirical validation before shipping as labels.

---

## 6. Source Index (50 sources from the synthesized report)

The NotebookLM report aggregated these underlying sources (numbered as cited in §1-§4):

1. arXiv — Extraction of Relevant Images for Boilerplate Removal
2. White Rose Research — Automated visual classification of DOM-based presentation failure reports (**peer-reviewed**)
3. iPullRank — Googlebot is Chrome
4. Medium — Architecting High-Performance CSS
5. FitLayout/2 — Web Page Analysis Framework (GitHub)
6. web.dev — Constructing the Object Model
7. W3C — Paint Timing (spec)
8. Firecrawl — Playwright vs Puppeteer 2026
9. DEV Community — Browser Tools for AI Agents
10. Lightpanda — CDP vs Playwright vs Puppeteer
11. testomat.io — Playwright Locators
12. Puppeteer docs — Page interactions
13. Playwright docs — Emulation
14. BrowserCat — Playwright vs Puppeteer scraping
15. DataDome — Detecting Headless Chrome stealth
16. Banani AI — Bento Grid explained
17. Medium — CSS Grid Bento UI
18. Semantic Scholar — Content-based Title Extraction (**peer-reviewed**)
19. tdcommons — Layout-Aware Text Extraction (**peer-reviewed**, HIGH confidence)
20. dainemawer — Determine When Sticky Element is Stuck
21. MDN — Box Model
22. wearedevelopers — Building Bento Grid Layout
23. ProxyScrape — Scrape Prices
24. Scrapfly — Track Competitor Pricing
25. TestMu AI — Playwright JavaScript
26. MDN — CSS Selectors
27. Univ. Manchester — Analysing Visual Complexity (**peer-reviewed**, HIGH confidence)
28. Reddit r/webscraping — pricing extraction
29. Octoparse — Price Scraping
30. Reddit r/webdev — FAQ accordion
31. Stack Overflow — FAQ accordion show/hide
32. a11y with Lindsey — Accordions
33. Hatchd — Testing UI and SEO with Jest/Puppeteer
34. Google Research — Hybrid Page Layout Analysis (**peer-reviewed**, HIGH confidence)
35. Drupal.org — hamburger menu issue
36. ResearchGate — Automated Repair of Asymmetric Web Pages (**peer-reviewed**)
37. GeneratePress — Header semi-transparent on scroll
38. Webshare — Scroll in Puppeteer
39. Stack Overflow — Event to detect position:sticky triggered
40. Stack Overflow — Puppeteer scroll down
41. Builder.io Forum — Visual Mega Menu
42. TestDino — Playwright Mobile Testing
43. Checkly — Emulating mobile devices with Playwright
44. ARVO Journals — Symmetry Detection (**peer-reviewed**)
45. ResearchGate — Improving Symmetric Structure (**peer-reviewed**)
46. Semantic Scholar — Automated Repair of Asymmetric Web Pages (**peer-reviewed**)
47. DreamX — Balance Design Principle
48. Houzz — Symmetry in Design
49. ResearchGate — WebExtension framework for webpage segmentation (**peer-reviewed**)
50. ResearchGate — Automated visual classification (**peer-reviewed**)

**Source-count caveat:** 181 sources were imported by `--import-all`, but the synthesized research report draws on ~50 (indexed above). The 181 includes many near-duplicates and tangential results (e.g., face-symmetry test, unrelated ResearchGate figures). The **effective cited basis is ~50 sources**, of which ~12 are peer-reviewed papers (HIGH confidence) and ~38 are blog/forum/docs (MEDIUM confidence, validate against real DOM before shipping). All hero-subtype thresholds (40px stat font, 95vw/80vh full-bleed, 45-50% split columns) and the airy/dense AR thresholds (0.45/0.20) come from the synthesized report and lack direct peer-reviewed citation — treat as provisional, validate empirically.
