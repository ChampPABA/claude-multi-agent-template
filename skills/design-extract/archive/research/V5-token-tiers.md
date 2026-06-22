# V5 — Token Tiers & Multi-theme (grounded)

**Source:** NotebookLM deep research, notebook `197e27c8` ("V5: multi-theme + token tiers per W3C"), ~108 ready web sources imported. Findings correct RESEARCH-completeness.md §4.

**Headline (two overclaims fixed):** (1) The primitive→semantic→component **tier split is a community convention, NOT W3C-mandated.** (2) The W3C Design Tokens Format Module has **no native multi-theme / `$themes` mechanism** — multi-theme must be detected on the **live site**. Spec status: **stable, 2025.10 Final Community Group Report (28 Oct 2025).**

## Q1 — Multi-theme / dark-mode DOM+CSS signals + per-theme palette capture

*(7 cited sources)*

To detect multiple themes or dark mode on a website and extract per-theme color palettes, you must monitor specific environment signals and programmatically manipulate them. 

**Exact DOM and CSS Signals for Theme Detection**
Modern web design systems generally broadcast theme modifications through the following root-level signals:
*   **DOM Attributes:** Custom attributes such as `[data-theme="dark"]` or `[data-dark-mode]` are mapped to root nodes (like `<html>` or `<body>`). Modifying these attributes forces the browser to re-evaluate the CSS specificity tree and apply theme-specific variable overrides [1-3].
*   **CSS Utility Classes:** Similarly, utility classes like `.dark` or `.light` applied to root elements (`html.dark` or `body.light`) act as toggles for active system overrides [1, 2].
*   **Media Queries:** The `@media (prefers-color-scheme: dark)` rule targets the operating system's color scheme preferences directly, allowing themes to switch without executing JavaScript or altering DOM attributes [1, 2, 4].
*   **CSS Functions:** The native `light-dark()` CSS function resolves colors dynamically based on the `color-scheme` property configured on the `:root` element, removing the need for media query wrappers [1, 2].

**Per-Theme Palette Capture Method**
To capture the complete design token palette for every supported theme, you can orchestrate a headless browser (such as Playwright or Puppeteer) to force these state transitions and harvest the resulting styles [5]. The method involves the following steps:

**1. Programmatic State Manipulation**
You must force the headless browser into the desired theme state using two primary mechanisms:
*   **Manipulating the DOM:** Execute a JavaScript payload within the page context to query the root elements, strip away any conflicting classes or attributes, and explicitly append the target class (e.g., `.dark`) or data attribute (e.g., `data-theme="dark"`) [5]. 
*   **Emulating Media Queries:** Override the system-level media queries programmatically by calling the headless browser's APIs to mock the `prefers-color-scheme` state [5, 6].

**2. Harvesting Computed Styles**
Once the specific theme is successfully forced, extract the active values by evaluating `window.getComputedStyle(document.documentElement)` [6, 7]. This native browser function retrieves the final resolved values of all CSS custom properties, automatically computing complex variable chains, inheritances, and fallbacks [7]. 

**3. Iteration and Mapping**
By cycling through the different emulated states—toggling the attribute/class to "light", harvesting the computed properties, and then repeating the process for "dark"—the automated pipeline captures the exact CSS variable differences between the themes [6]. This allows you to compile a distinct and complete map of the color palette for each theme in the design system [6].

## Q2 — W3C Design Tokens Format Module: status + token types (answer in Thai)

*(16 cited sources)*

สถานะการเผยแพร่ของข้อกำหนด **W3C Design Tokens Format Module** ในช่วงปลายปี 2025 คือการบรรลุ **เวอร์ชันเสถียรเวอร์ชันแรก (First stable version)** ภายใต้ชื่อ 2025.10 Final Community Group Report ซึ่งมีการประกาศเมื่อวันที่ 28 ตุลาคม 2025 [1, 2]

**ประเภทของโทเค็น (Token Types)**
ข้อกำหนดนี้รองรับประเภทของโทเค็นหลากหลายรูปแบบ โดยแบ่งออกเป็นประเภทพื้นฐานและประเภทเชิงซ้อน (Composite types) ได้แก่:
* **ประเภทพื้นฐาน:** Color (สี), Dimension (มิติขนาด), Duration (ระยะเวลา), Font Family (ตระกูลฟอนต์), Font Weight (น้ำหนักฟอนต์), Number (ตัวเลข), Cubic Bézier (เส้นโค้งเคิร์ฟของแอนิเมชัน) และ Asset (ไฟล์สื่อ) [3]
* **ประเภทเชิงซ้อน (Composite types):** เป็นประเภทที่เกิดจากการรวมค่าย่อยๆ หลายค่าเข้าด้วยกันตามโครงสร้างที่กำหนดไว้ เช่น Shadow (เงา), Transition (การเปลี่ยนผ่าน), Typography (รูปแบบตัวอักษร), Border (เส้นขอบ), Gradient (การไล่สี) และ Stroke style (สไตล์ของเส้น) [4-10]

**โครงสร้างของ `$type` และ `$value`**
รูปแบบของ W3C จะใช้เครื่องหมายดอลลาร์ (`$`) นำหน้าพร็อพเพอร์ตี้ของโทเค็นและข้อมูลเมตาเสมอ เพื่อให้ระบบสามารถแยกแยะระหว่างชื่อกลุ่ม (Nested groups) ออกจากข้อมูลของโทเค็นได้อย่างชัดเจน [11]
* **`$value`**: เป็นพร็อพเพอร์ตี้บังคับที่ใช้กำหนดค่าของโทเค็น ออบเจกต์ใดก็ตามที่บรรจุพร็อพเพอร์ตี้ `$value` ไว้ จะถูกพิจารณาว่าเป็นโทเค็นทันที โดยชื่อคีย์ของออบเจกต์นั้นจะถือเป็นชื่อของโทเค็น [12] ตัวอย่างเช่น โทเค็นประเภทมิติขนาด (Dimension) จะมีโครงสร้างย่อยเป็นตัวเลขและหน่วย เช่น `{"value": 16, "unit": "px"}` [3]
* **`$type`**: เป็นพร็อพเพอร์ตี้สำหรับใช้ระบุชนิดของโทเค็นอย่างเจาะจง เพื่อให้เครื่องมือการออกแบบและนักพัฒนาสามารถแปลความหมายค่าของโทเค็นนั้นได้อย่างถูกต้อง พร็อพเพอร์ตี้ `$type` สามารถระบุไว้ที่ตัวโทเค็นโดยตรง หรือสืบทอดค่า (Inherit) มาจากกลุ่มหลักที่ครอบโทเค็นนั้นอยู่ก็ได้ [13]

**การทำงานของการอ้างอิงนามแฝงด้วยไวยากรณ์วงเล็บปีกกา (Alias References)**
การอ้างอิงด้วยไวยากรณ์วงเล็บปีกกา เช่น `{group.token}` ถูกออกแบบมาเพื่อใช้อ้างอิงถึง **ค่าของโทเค็นแบบเต็มรูป (Complete token values)** [14]
* เมื่อระบบพบไวยากรณ์อ้างอิงนามแฝง (เช่น `{colors.blue}`) ระบบจะทำการชี้และดึงข้อมูลจากพร็อพเพอร์ตี้ `$value` ของโทเค็นเป้าหมายทั้งหมดมาใช้งาน [14]
* ไวยากรณ์นี้ใช้สำหรับการเชื่อมโยงค่าแบบโทเค็นสู่โทเค็น (Token-to-token references) เท่านั้น โดยจะไม่สามารถใช้เจาะจงไปยังพร็อพเพอร์ตี้ย่อยส่วนใดส่วนหนึ่งภายในออบเจกต์ของโทเค็นได้ (หากต้องการอ้างอิงระดับพร็อพเพอร์ตี้ย่อย ต้องใช้ไวยากรณ์ JSON Pointer เช่น `$ref` แทน) [14, 15]
* การอ้างอิงโทเค็นสามารถทำแบบต่อเนื่องเป็นทอดๆ ได้ (Chained references) แต่ **ห้าม** สร้างโครงสร้างการอ้างอิงที่วนลูปกลับมาหาตัวเอง (Circular references) โดยเด็ดขาด [16]

## Q3 — Tier classification via var() reference chains (DAG model)

*(5 cited sources)*

To classify CSS custom properties into distinct tiers by walking `var()` reference chains, the architecture is mathematically modeled as a **Directed Acyclic Graph (DAG)** [1]. In this graph, vertices represent the custom properties, and directed edges are created whenever one variable references another via the `var()` function (e.g., $u \to v$) [1, 2]. 

There is an accepted heuristic for classifying each custom property into a tier based on its position in this reference chain. This classification relies on evaluating the **structural graph properties (in-degree and out-degree)** combined with **regex-based naming conventions** [3]. 

Using this heuristic, the properties are classified into three specific tiers:

*   **Primitive Tier (Raw Values):** These are the foundational building blocks of the design system that carry absolute, literal values [3]. In the dependency graph, they act as **leaf nodes with an out-degree of zero** (they do not reference any other variables) and an in-degree of $\ge 0$ [3, 4]. Name-matching heuristics typically look for base scales, numeric ranges, or color families [3]. 
    *   *Example:* `--color-blue-500: #3b82f6;` [4]
*   **Semantic Tier (Role-Based):** These properties apply functional meaning to raw values, which helps decouple the visual theme from specific components [3]. Graphically, they are **intermediate nodes with both an in-degree and an out-degree greater than zero** [3, 4]. This means they reference primitive tokens and are, in turn, referenced by component tokens. Naming heuristics target functional states, interactive highlights, or surface assignments [3].
    *   *Example:* `--color-bg-primary: var(--color-blue-500);` [4]
*   **Component Tier:** These variables scope styling options to specific UI components [3]. In the graph, they are **root nodes with an in-degree of zero** (nothing else references them) and an out-degree greater than zero (they reference semantic tokens to apply styling) [3, 4]. Name-matching heuristics specifically target component boundaries [3]. 
    *   *Example:* `--button-primary-bg: var(--color-bg-primary);` [4]

**Handling Edge Cases in the Reference Chain**
When walking these chains, parsers must account for complex structures to maintain an accurate graph. For instance, if a custom property includes fallback arguments (e.g., `var(--color-foreground-primary, var(--color-fallback-dark, #000000))`), the parser must construct multiple edges to correctly model the primary dependency alongside the fallback path [1]. Additionally, some design systems use "pseudo-private" variables within components (often prefixed with an underscore, like `--_button-bg`). The parser must trace these private variables back to their public entry points to ensure they are accurately grouped under the Component tier [5].

## Q4 — Is the primitive/semantic/component tier split W3C-mandated?

*(9 cited sources)*

The three-tier split of design tokens into primitive, semantic, and component tiers is **not defined or mandated by the W3C Design Tokens Format Module specification**; rather, it is a **community convention** and architectural heuristic used in modern design systems [1]. 

**The W3C Specification's Stance**
The W3C specification focuses strictly on the technical format, token types, and resolution mechanics, explicitly avoiding any mandates on how tokens should be functionally tiered. According to the W3C spec, tokens can be organized into hierarchical "Groups," but it strictly notes that **"Groups are arbitrary and tools *SHOULD NOT* use them to infer the type or purpose of design tokens"** [2, 3]. 

The specification enables tiering by allowing tokens to reference other tokens via aliases (e.g., `{colors.blue}` resolving to another token's value), but it leaves the architectural meaning of those relationships entirely up to the authors [4, 5]. The W3C spec only cares about the data types (e.g., distinguishing a Color from a Dimension) and resolving the reference chains, not whether a token serves a "semantic" or "component" role [6-8].

**The Three-Tier Model as a Community Heuristic**
Because the W3C standard is agnostic to design methodology, the separation into primitive, semantic, and component layers is an accepted **structural classification framework** applied *on top* of the tokens [1]. As discussed previously, to align with modern design system patterns, parsers and automated tools must retroactively classify tokens into these three distinct architectural tiers [1]. They achieve this by analyzing the Directed Acyclic Graph (DAG) reference chains (looking at in-degrees and out-degrees) and applying regex-based naming heuristics to guess whether a variable acts as a foundational raw value, a role-based semantic token, or a component-scoped token [1, 9].

*(Note: While the sources confirm that this three-tier model is a recognized community convention and heuristic framework, the specific design systems you mentioned—Salesforce Lightning Design System, Adobe Spectrum, and Material Design—are not detailed in the provided source material. You may want to independently verify how those specific platforms document their token architectures.)*

## Q5 — Does W3C define a native multi-theme / $themes mechanism?

*(14 cited sources)*

The W3C Design Tokens Format Module 2025.10 does **not** define a `$themes` construct or a native multi-set mechanism to handle multiple themes within a single token file [1-3]. The format module specification is focused on defining individual token properties like `$value`, `$type`, and `$description`, and leaves any custom multi-theme configurations within a single file to tool-specific extensions via the `$extensions` property [4-6].

Instead, the W3C addresses the complexities of multiple themes through a completely separate specification: the **Design Tokens Resolver Module 2025.10** [7, 8]. 

The Resolver Module is explicitly designed to coordinate tokens across multiple contexts—such as "light mode," "dark mode," or different layout densities—without duplicating files [7, 9]. Rather than storing everything in one file, it utilizes a dedicated `.resolver.json` configuration document to orchestrate how different token files or collections merge together [7, 10].

The `.resolver.json` spec defines several root-level constructs to handle themes [7, 11]:
*   **`sets`**: A dictionary defining base token collections, which can point to external JSON files containing design tokens or inline tokens [7, 12].
*   **`modifiers`**: A map defining conditional variations and contexts (e.g., a "theme" modifier with "light" and "dark" contexts). Modifiers allow you to specify the alternate token values that apply when a specific context is active [7, 13].
*   **`resolutionOrder`**: An array specifying the precise order in which `sets` and `modifiers` are merged. When resolving a theme, later declarations in this array override the preceding ones (e.g., a dark mode modifier overriding the base token set) [7, 14].

In summary, the W3C handles dark mode and multi-theme design not by cramming a `$themes` object into a single token file, but by using the **Resolver Module to dynamically weave together base `sets` and contextual `modifiers`** [7, 11].


---

## Corrections vs the §4 draft

| Draft claim | V5 verdict |
|---|---|
| "Tier completeness **from W3C spec**" / "Semantic tiers" as a standard surface | **Corrected** — tier split is a **community convention**, not spec-mandated (Q4). Model as heuristic. |
| "Multi-theme sets — **W3C supports multiple sets**" | **Corrected** — W3C has **no native multi-theme mechanism** (Q5). Detect on live site instead (Q1). |
| Spec "stable Oct 2025" | **Confirmed + refined** — 2025.10 Final Community Group Report, 28 Oct 2025 (Q2). |
| Classify `--*` into tiers via reference graph | **Confirmed + grounded** — walk `var()` chains as a **DAG**; classify by graph position (Q3). |
