# Research Archive — extract skill provenance

These files are **not read during an extraction run**. They are the grounding/decision trail behind the detection methods in `references/extraction-steps.md` and `references/output-format.md`. Read them when you need to answer *"why does extract do X this way?"* or revisit a design decision.

The actual detection logic is already inlined into the reference files — the `§`-numbers there are shorthand labels, not pointers to read these files at runtime.

| File | What it grounds | Notes |
|------|-----------------|-------|
| `RESEARCH-completeness.md` | The whole skill — consolidated proposal + decision tracker (§0–§12). Motion research (§3) lives inline here; there is no V3 file. | The master doc. Start here. |
| `research/V1-imagery.md` | `imagery` section detection (treatment vs visual_description, duotone ambiguity, bounded sampling) | NotebookLM deep-research, ~85 sources |
| `research/V2-composition.md` | `page_composition` (section-type table, bento vs feature-grid, nav-behavior protocol, airiness heuristics) | NotebookLM, ~50 effective sources; 7 corrections to first draft |
| `research/V4-completeness.md` | Completeness audit — which design dimensions are extractable vs recreation-only (gaps A–D) | NotebookLM, 60–80 unique sources |
| `research/V5-token-tiers.md` | `css_custom_properties` tier classification + multi-theme detection; W3C Design Tokens spec status | NotebookLM, ~108 sources; corrects 2 overclaims |

**Recall in conversation:** to bring this back without reading files, query Hindsight (e.g. `hindsight memory recall claude_code "extract skill nav-behavior detection research"`).
