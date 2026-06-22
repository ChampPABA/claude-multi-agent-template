# V1 — Imagery Style & Treatment Detection (grounded)

**Source:** NotebookLM deep research, notebook `8ddebc82` ("V1: imagery detection from headless browser"), ~85 ready web sources imported. Findings correct RESEARCH-completeness.md §1.

**Headline:** imagery **treatment** is reliably computable from `getComputedStyle`/DOM (medium, object-fit, aspect-ratio, radius, mask, clip-path, filter, blend, overlay, full-bleed). Imagery **style/subject** (photo vs illustration, editorial vs product, color grade, mood) is visual — fill from screenshot + one-line description. **Duotone has no single reliable signal** — heuristic only.

## Q1 — Per-treatment detection signals (getComputedStyle / DOM)

*(19 cited sources)*

Here is the programmatic detection mapping for each requested imagery treatment, drawing on headless browser auditing frameworks and computed style resolution methodologies:

| Imagery Treatment | Exact `getComputedStyle` Property or DOM Signal | Spec / Source Context |
| :--- | :--- | :--- |
| **`object-fit`** | `getComputedStyle(element).objectFit` | Extracted directly from the element's computed style map to identify stretching or cropping behaviors (evaluates to `fill`, `contain`, `cover`, `none`, or `scale-down`) [1]. |
| **`aspect-ratio`** | `getComputedStyle(element).aspectRatio`<br><br>**DOM Signals:** `element.naturalWidth` / `element.naturalHeight` | The computed CSS `aspect-ratio` property is compared against the native dimension proportions (natural width divided by natural height) of the `<img>` DOM node to detect layout distortions [1]. |
| **`border-radius`** | `getComputedStyle(element).borderRadius` | Read from the style map to detect shapes (e.g., a computed border-radius of `>= 50%` combined with a `1:1` aspect ratio identifies circular avatar images) [2]. |
| **`mask-image`** and **`-webkit-mask-image`** | `getComputedStyle(element).maskImage`<br>`getComputedStyle(element).webkitMaskImage` | Parses the resolved string to reconstruct alpha masking layers, looking for functions like `url(...)` referencing SVGs/external assets, or `linear-gradient`/`radial-gradient` declarations [3, 4]. |
| **`clip-path`** | `getComputedStyle(element).clipPath` | Parses the active vector crop boundaries. The output string contains geometric functions (like `circle()`, `ellipse()`, `inset()`, `polygon()`) or a `url()` referencing an SVG `<clipPath>` ID [4-6]. |
| **CSS filter functions** *(grayscale, sepia, blur, brightness, contrast, saturate, hue-rotate)* | `getComputedStyle(element).filter` | The browser composites these into a single, space-separated string of function calls. The value must be parsed (often via regex) to extract individual filter modifiers and their parameters (e.g., `/grayscale\(([^)]+)\)/`) [7, 8]. |
| **`mix-blend-mode`** | `getComputedStyle(element).mixBlendMode`<br><br>*Related:* `getComputedStyle(element).backgroundBlendMode` | Evaluates the string (e.g., `multiply`, `screen`, `overlay`, `difference`, `color`) to detect separable or non-separable blend modes applied against the element's backdrop or internal background layers [9-11]. |
| **`backdrop-filter`** | `getComputedStyle(element).backdropFilter` | Resolves the background-backdrop graphical transformations (such as blur or color shifting) applied to the area behind the element [12]. |
| **Gradient or solid overlays** | **Pseudo-styles:** `getComputedStyle(element, '::before')` or `getComputedStyle(element, '::after')`<br><br>**DOM Signals:** `element.getBoundingClientRect()` | Scrapes absolute-positioned sibling nodes or pseudo-elements matching a higher `zIndex`, looking for `background` properties containing `linear-gradient` or semi-transparent colors. Overlap state is mathematically confirmed by checking bounding box collisions using `getBoundingClientRect()` [13-16]. |
| **`full-bleed`** | Multiple `getComputedStyle` properties depending on the layout strategy:<br>• **Width:** `100vw` or `100cqw`<br>• **Margins:** Negative `marginLeft`/`marginRight`<br>• **Grid:** `gridColumn` & `display` | **Strategy A:** Element `width` resolves to `100vw` with negative lateral margins equal to ~50% of the parent width subtracted from 50vw [17].<br>**Strategy B:** Element `gridColumn` resolves to `1 / -1` while its parent container `display` resolves to `grid` [18].<br>**Strategy C:** Element `width` resolves to `100cqw` natively [19]. |

## Q2 — Duotone detection (reliability)

*(15 cited sources)*

Detecting a duotone effect programmatically from the DOM requires analyzing the structural and stylistic layers applied to an image. Because web developers use wildly different techniques to achieve duotones, **there is no single, unambiguous computable signal** that confirms a duotone. Instead, detection relies on a combination of computable DOM/CSSOM extraction and heuristic evaluation [1, 2].

Here is how detecting an SVG filter compares to detecting a CSS overlay, and why the process ultimately remains ambiguous.

### 1. Detecting SVG Filters (`<feColorMatrix>` + `<feComponentTransfer>`)
High-fidelity duotone effects on the web are typically created using SVG filter primitives [3]. To detect this, a headless automation engine must parse the computed `filter` property (e.g., `filter: url('#filter-id')`) and locate the corresponding `<filter>` element in the DOM [3]. 

This detection method is highly mathematical and computable because the transformation steps are explicitly defined in the markup:
* **Step 1 (Desaturation):** The script checks for an `<feColorMatrix>` element with a $5 \times 5$ matrix. If the RGB columns contain values that collapse the image into linear luminance (e.g., rows of `0.33`), it confirms the image is being converted to grayscale [4, 5].
* **Step 2 (Gradient Mapping):** The script then looks for an `<feComponentTransfer>` element containing `<feFuncR>`, `<feFuncG>`, and `<feFuncB>` tags with `type="table"` [5, 6]. 
* **Color Extraction:** By extracting the space-separated fractions in the `tableValues` attribute and multiplying them by 255, an audit script can definitively calculate the exact shadow and highlight RGB colors used to create the duotone gradient map [7-9]. 

### 2. Detecting CSS Overlays + Blend Modes
A more lightweight, CSS-only approach to duotones involves styling a grayscale image with a colored overlay and blending them together [10]. Detecting this approach is more complex because the styles are decoupled from the image node itself.

* **Identifying the Overlay:** The script must scrape the element's pseudo-elements (`::before` or `::after`) or absolute-positioned sibling containers [11]. It looks for a solid or gradient background combined with a specific `mix-blend-mode` (like `multiply`, `screen`, `lighten`, or `color`) or `background-blend-mode` [10, 12].
* **Confirming the Effect:** Simply finding an overlay is not enough. The script must execute a **bounding-box collision detection** algorithm using `getBoundingClientRect()` to mathematically confirm that the colored overlay's coordinates actually overlap the target image [11]. If they intersect, and the overlay has transparency or a blend mode, the visual treatment is confirmed [13].

### Is Detection Unambiguous or Heuristic?
Ultimately, **detection is inherently heuristic and ambiguous**. 

While the "Render Layer Filters & Blend Modes" are considered deterministic and computable (since they are explicitly declared in the CSSOM) [1], the actual **visual intent** cannot be reliably proven from code alone. There are two major reasons for this ambiguity:

1. **The "Black Box" of the Source Asset:** Standard website code does not self-describe its semantic content [2]. An auditing script can read that an image has a computed `filter: grayscale(1)` combined with a colored overlay, but it cannot know what the underlying image looks like [2]. For example, the original image file might *already* be a pre-rendered duotone created in Photoshop, meaning no CSS modifiers are present in the DOM at all.
2. **Contextual Rendering:** Even if the exact SVG duotone matrix is found in the DOM, the code cannot confirm if the underlying asset is a photograph (where a duotone effect makes sense) or a flat vector icon (where the filter might just change a solid color) [1, 2]. 

**Conclusion:**
Because of this fundamental limitation, relying strictly on DOM signals is considered a "Stage 1" heuristic [14]. To unambiguously confirm that an image is presented as a duotone, modern auditing frameworks must capture a rendered screenshot of the layout bounds and pass it to a multimodal vision model for qualitative visual classification [2, 15].

## Q3 — Computable (DOM) vs visual-judgment (screenshot) split

*(3 cited sources)*

**Group A: Machine-readable attributes from DOM/CSS `getComputedStyle`**
These attributes are deterministically extracted from the browser's Document Object Model (DOM) and Cascading Style Sheets Object Model (CSSOM) and are ideal for structured YAML outputs [1].
*   **Asset Dimensions & Box Position:** Calculated with pixel-perfect accuracy by the browser's layout engine and easily extracted using `getBoundingClientRect()` [2].
*   **Object Fit & Aspect Ratio:** Directly extractable from the computed style map (e.g., `object-fit`, `aspect-ratio`) to identify scaling, stretching, or cropping behaviors [2].
*   **Render Layer Filters & Blend Modes:** Explicitly declared in the CSS code, allowing direct extraction of `filter` lists, color matrices, and `mix-blend-mode` properties [2].

**Group B: Attributes requiring visual judgment from a screenshot**
Because standard website code does not self-describe semantic visual content, these attributes require capturing a screenshot of the layout bounds and passing it to a multimodal vision model for qualitative analysis [3].
*   **Color Grading & Mood:** CSS files do not contain semantic mood descriptors, meaning the emotional resonance of pixel values must be interpreted visually [2].
*   **Imagery Genre (e.g., Photo vs. Illustration/Vector):** Because CSS classes can be arbitrarily named or obfuscated, code alone cannot reliably distinguish raster photographs from flat vector artwork [2, 3].
*   **Aesthetic Presentation Style (e.g., Editorial vs. Product vs. Lifestyle):** Determining the visual intent and contextual aesthetic of an image requires semantic scene understanding [2].
*   **Subject Focus & Cropping Safeness:** Calculating whether responsive scaling and cropping will accidentally slice out a human subject requires visual saliency mapping [2].

## Q4 — Bounded sampling strategy by role

*(13 cited sources)*

To capture website imagery efficiently without incurring the "significant latency and API costs" of processing every image through a multimodal vision model, headless crawlers must utilize **"Heuristic-Based Sampling"** to avoid "blanket scraping of all visual nodes" [1, 2]. 

Here is a proposed bounded sampling strategy that limits the number of images processed per role while maintaining a representative aesthetic profile of the page:

**1. Hero Image: 1 Image**
*   **Sampling Bound:** **1**
*   **Rationale & Heuristics:** A hero image serves as the "primary visual introduction" at the top of a page and is designed to set the immediate tone [1]. Because a page generally only features a single hero layout, capturing exactly 1 is sufficient. The script can sample this by looking for the first element with a vertical position of $y \le 120\text{px}$, a width $\ge 960\text{px}$, and a wide aspect ratio [3]. 

**2. Card Thumbnails: 3–5 Images**
*   **Sampling Bound:** **3 to 5**
*   **Rationale & Heuristics:** Card thumbnails are "structured, repeated images" used to support scannable content summaries in grids or lists [4]. Because they share structural layout clustering (identifiable via "repeated sibling nodes" inside CSS flexbox or grid cells), processing every card in a long list is redundant [4]. A bounded sample of 3 to 5 cards is enough to verify their uniform sizing ($250\text{px}$–$600\text{px}$ width) and treatment [4].

**3. Avatars: 3–5 Images**
*   **Sampling Bound:** **3 to 5**
*   **Rationale & Heuristics:** Avatars represent users or team members and are identified by circular geometry (a 1:1 aspect ratio and `border-radius` $\ge 50\%$) within a compact bounding box ($24\text{px}$ to $120\text{px}$) [5]. Like cards, they often appear in groups or lists. Capturing 3 to 5 avatars provides a representative sample of how profile photos are masked and cropped without downloading an entire user directory [5].

**4. Decorative Backgrounds: 1–2 Images**
*   **Sampling Bound:** **1 to 2**
*   **Rationale & Heuristics:** Decorative backgrounds provide ambient texture and are detected by their massive dimensions, low computed opacity ($\le 0.2$), and the fact that other interactive DOM nodes overlap their coordinate space [6]. Since these are sitewide or section-wide themes, capturing 1 or 2 distinct background layers is enough to assess the page's atmospheric mood and aesthetic presentation [6, 7]. 

**5. Social / Open Graph (OG) Images: 1 Image**
*   **Sampling Bound:** **1**
*   **Rationale & Heuristics:** OG images do not render in the visible viewport; they are designated preview assets extracted directly from `<meta>` tags in the document head [8]. Because a page typically declares only one canonical OG image URL, the absolute bound is 1 [8].

### References on Bounded Sampling in the Sources
The provided sources address bounded sampling through two distinct lenses:
*   **Heuristic-Based Sampling for Web Audits:** The *Programmatic Analysis of Website Imagery* framework explicitly cites **"Heuristic-Based Sampling"** (referencing Skelon's layout inference engine `[9]`) as the method to "sample images selectively based on their semantic roles" [1, 10]. The framework utilizes a multi-stage architecture where "Stage 1: Fast Filtering and Layout Profiling" acts as the boundary, executing layout-based code queries to group images before sending a limited, targeted subset to the vision model (Stage 3) [11, 12].
*   **Machine Learning Data Budgets:** In the context of active machine learning, the sources cite strategies like **"diversity sampling"** and "pool-based sampling" to intelligently choose data points and maximize model performance under "stringent data budgets" [13]. This conceptual framework justifies capturing a small, highly diverse subset of elements (like 3-5 distinct card layouts) rather than exhaustively scraping every identical node.


---

## Corrections vs the §1 draft

| Draft claim | V1 verdict |
|---|---|
| Treatment signals computable from CSS (§1.2 table) | **Confirmed** — all signals resolve via `getComputedStyle` (see Q1). |
| Duotone = "proxy: SVG feColorMatrix, or overlay + blend" | **Corrected** — there is **no single unambiguous signal**; detection is heuristic and ambiguous (Q2). Flag as inferred. |
| Computable vs visual split (§1.3) | **Confirmed** — DOM gives treatment; screenshot gives style/subject/mood (Q3). |
| Bounded sampling by role, ~12–15 total (§1.4) | **Confirmed** — heuristic-based sampling by role avoids blanket capture (Q4). |
