# Diagram Style Rules (flowchart / swimlane)

> Evidence-based priority order for laying out our flowcharts (draw.io). When two
> rules conflict, the **lower priority number wins**. Grounded in graph-drawing
> readability research (Purchase 1997; Ware et al. 2002) and the Sugiyama layout
> pipeline. Decided 2026-06-19.

## Why a priority order

"Make it pretty" rules conflict in practice (e.g. keeping a line straight vs. not
piling two lines on one side). Research ranks which aesthetics actually affect
human comprehension, so conflicts resolve by evidence, not taste.

## Priority order (P1 = strongest, wins all conflicts)

| P | Rule | Basis |
|---|------|-------|
| **P1** | **No crossing / no overlapping lines.** Reroute (extra bends, gutter, connector node) rather than cross. | Strongest empirical predictor of comprehension errors (Purchase 1997; Ware 2002). |
| **P2** | **Top-down flow.** Enter from top, exit from bottom; the happy path runs straight down. Back-loops route through an outer gutter, never through the main column. | Universal flowchart/BPMN convention; Sugiyama phase 2. |
| **P3** | **Straightness / continuity of the main trunk.** Minimize bends on the happy path. | Strong empirical (Ware 2002). |
| **P4** | **Align node centers** so trunk edges are perfectly straight (same center-X down a lane; same center-Y for a horizontal hand-off). | Mechanism that achieves P3; also reduces crossings. |
| **P5** | **Decision diamond connects at its 4 vertices** (top/bottom/left/right points), not the flat sides. | Convention; combines flow direction + orthogonality. |
| **P6** | **Minimize bends on secondary / branch connectors.** | Moderate empirical (Purchase 1997). |
| **P7** | **Compact layout.** No large empty gaps; loops/returns use the gutter or a connector node, not a wide void. Split to a new page if a cluster causes a long stray loop. | Weak evidence; reduces clutter. |
| **P8** | **Prefer ≤1 connector per side of a box** (distribute across the 4 sides). | Taste only — *not* supported by readability research. Apply only when it costs nothing at P1–P7. |

## Conflict resolutions (the ones we hit)

- **Straight line (P3) vs. 1-per-side (P8):** straight wins. If two predecessors
  come from the same direction and can enter the same side **without crossing**,
  let them share the side rather than bending the happy path to spread them out.
  *(This is why TC-2 "เห็นสรุปรายวัน" takes both ตรง and ไม่ตรง on its left: ตรง
  stays a straight horizontal; ไม่ตรง comes up into the lower-left; no crossing.)*
- **No-crossing (P1) vs. minimize-bends (P3/P6):** no-crossing wins — accept more
  bends (or route around the outside) to remove a crossing.
- **Flow convention (P2) vs. straightest line (P3):** flow wins, *unless* it forces
  a crossing (then P1 wins). Back-loops always go to a gutter.
- **Decision-at-vertices (P5) vs. straight line (P3):** vertices win; proper node
  alignment (P4) should make the vertex connection straight anyway.
- **1-per-side (P8) vs. anything above:** P8 always yields.

## When 1-per-side *does* apply (P8)

If two connectors would land on the same side **and** moving one to another side
does not add a crossing or bend the happy path, then spread them: the connector
whose **source sits higher** moves to the **top**; the lower source keeps the side.
*(Only do this when it's free — see the P3-vs-P8 rule above.)*

## Always-on mechanics (not in the priority contest)

- **90° corners only** (`rounded=0`), never curved.
- One consistent edge style, stroke weight, arrowhead across a page.
- Label cross-lane / branch edges (yes/no, artifact name); keep labels off bends.
- Snap to grid (10px); same-row boxes share top-Y, same-column boxes share center-X.

## How we verify

`scripts/check_layout.py` is the primary gate: it hard-fails the render-breaking
faults (over-the-top back-edges, wrong-side stabs, lines through a box, and crossings —
P1) that the XML hides. Crossings are hard unless one edge carries `jumpStyle=arc` to
declare the crossing legible. P8 (same-side count), bend-heavy, and auto-route notes are
advisory — do not "fix" a P8 case if the fix violates P1–P4. Export a PNG and inspect
visually only as a final glance, and only when the gate reports an auto-route edge it
could not trace (or the flow is large enough that spacing/labels need an eye).

## Sources

Purchase 1997 "Which aesthetic has the greatest effect on human understanding?";
Ware, Purchase, Colpoys & McGill 2002 "Cognitive Measurements of Graph
Aesthetics"; Purchase et al. 2021 IEEE Access state-of-the-art review; Tamassia
1987 / Sugiyama layered-graph pipeline; Lucidchart, Nulab, draw.io, ISO 5807
flowchart guidance.
