---
name: drawio-swimlane
description: Author, clean up, or review draw.io swimlane and cross-functional flowcharts to a professional standard. Make sure to use this skill whenever the user works on a .drawio flowchart, process diagram, or swimlane (lanes per role/entity, top-down process flows with decision diamonds), and ESPECIALLY when connector lines look messy - crossings, overlaps, lines cutting through boxes, too many bends, curved corners, or multiple lines piling on one side of a box. Also use when laying out any top-down flowchart or process map in draw.io even if the word "swimlane" is not said, or when someone asks to make a .drawio diagram "cleaner / straighter / prettier" or "fix the arrows". Encodes an evidence-based priority order (Purchase/Ware graph-aesthetics research) for resolving layout conflicts, the draw.io XML specifics (fixed connection points, 90-degree corners, decision-vertex connections, gutter/connector-node loops), and a REQUIRED export-PNG-and-visually-inspect verification loop.
allowed-tools: Read, Write, Edit, Bash
---

# draw.io Swimlane Flowchart Skill

Produce clean, professional swimlane (cross-functional) flowcharts as native
`.drawio` files, and fix messy ones. The hard part is connector routing; this
skill gives a **priority-ordered rule set** so conflicts resolve by evidence, not
guesswork, and a **verify loop** (export PNG, look at it) because the XML alone
can't tell you if lines overlap.

## Triggers

- "create a swimlane / cross-functional flowchart"
- "make this .drawio flow cleaner", "lines are crossing / overlapping / messy"
- "draw the process flow for X with lanes per role"
- "ทำ flowchart / swimlane", "เส้นมันทับกัน ปรับให้สวย"

## Priority order (resolve any conflict by lowest P-number)

When two layout rules conflict, the higher-priority rule wins.

1. **P1 - No crossings / no overlapping lines.** Reroute (extra bends, outer
   gutter, or a connector node) rather than let lines cross or overlap. *Strongest
   readability factor (Purchase 1997, Ware 2002).*
2. **P2 - Top-down flow.** Enter boxes from the top, exit from the bottom; the
   happy path runs straight down. Back-loops route through an outer gutter, never
   through the main column.
3. **P3 - Straight main trunk.** Minimize bends on the happy path; keep it a
   straight line.
4. **P4 - Align node centers** so trunk edges are dead straight (same center-X
   down a lane; same center-Y for a horizontal hand-off).
5. **P5 - Decision diamond connects at its 4 vertices** (top/bottom/left/right
   points), not the flat sides.
6. **P6 - Minimize bends on branch/secondary connectors.**
7. **P7 - Compact.** No big empty gaps; loops use the gutter or a connector node.
   Split a cluster to its own page if it would otherwise need a long stray loop.
8. **P8 - Prefer <=1 connector per side** of a box. *Taste only, not research-
   backed - the weakest rule. Apply only when it costs nothing at P1-P7.*

Key consequence: **do NOT bend a straight happy-path line just to avoid two
connectors on one side.** Two lines may share a side if they don't cross (P3 > P8).
Full rationale + citations: `references/priority-rules.md`.

## When 1-per-side (P8) actually applies

Only when spreading connectors costs nothing higher up: the connector whose
**source sits higher** moves to the **top**; the lower source keeps the side.

## draw.io authoring specifics

- **Vertical swimlanes** = lanes side by side as columns, flow top->bottom. Each
  lane: `style="swimlane;html=1;startSize=30;"`. **Lanes must abut - NO gap between
  them:** lane(N+1).x = lane(N).x + lane(N).width, so borders touch like a real
  pool (a visible gap between lanes reads as broken). Give all lanes the same
  height. Nodes are children of their lane (geometry is lane-relative); edges use
  `parent="1"` (root) so waypoints are in absolute page coords.
- **No decoration unless asked:** omit fillColor (white) / strokeColor (black).
- **Shapes:** terminator `ellipse`; process `rounded=0`; decision `rhombus`;
  document `shape=document`; data store `shape=cylinder`; sub-process (overview
  drill-down box) `shape=process`.
- **Edges - one consistent style, sharp corners:**
  `edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=block;`
  plus **fixed connection points** so routing is predictable:
  - forward (down, same lane): `exitX=0.5;exitY=1; entryX=0.5;entryY=0;`
  - cross-lane hand-off: `exitX=1;exitY=0.5; entryX=0;entryY=0.5;` (same center-Y => straight horizontal)
  - decision vertices: top `0.5,0` / bottom `0.5,1` / left `0,0.5` / right `1,0.5` (never fractional on a rhombus - fractional points land on the bounding box, not the diamond, so the line touches the frame)
- **Arrowhead must stab straight into the target.** Choose the entry side so the
  edge's LAST segment runs perpendicular into the target's face and the arrowhead
  clearly points into the box - not a glancing/parallel approach that grazes a
  corner. (E.g. a line coming from below should enter the box's bottom face, not
  curl into its side.)
- **Stay inside the frame.** Every line - including gutters and back-loops - must
  stay INSIDE the pool/outer-lane border. Never route a waypoint outside the
  leftmost/rightmost lane edge (it reads as a line escaping the diagram).
- **Back-loop / return:** route through a gutter that sits **inside the frame** -
  in the slack between boxes and the lane border, or along the bottom inside the
  pool - with explicit `<Array as="points">` waypoints (sharp 90deg, clear of all
  boxes). If there isn't room inside, replace the long loop with a small terminal
  "connector node" (e.g. an ellipse "back to X") instead of escaping the frame.
- **Crossings that are unavoidable:** add `jumpStyle=arc` to one edge.
- Multi-page set for big flows: an overview page (sub-process boxes) + one page per
  sub-process; numbering like `TC-0` overview, `TC-1..n` details.

## Verify loop (REQUIRED - never trust the XML)

Export each page to PNG via the draw.io desktop CLI and look at it; iterate.

```bash
# WSL2 path to the CLI (adjust per OS: macOS /Applications/draw.io.app/...; Linux: drawio)
DRAWIO="/mnt/c/Program Files/draw.io/draw.io.exe"
WININ=$(wslpath -w flow.drawio)
# -p is 1-based page index; -s scales up for legibility
"$DRAWIO" -x -f png -e -b 10 -p 2 -s 1.5 -o "$(wslpath -w page2.png)" "$WININ"
```

Then Read the PNG and check against P1-P8. A quick same-side (P8) audit can be
scripted by parsing exitX/exitY & entryX/entryY per node, but P8 is advisory - do
not "fix" a P8 case if the fix breaks P1-P4.

Optional human-viewable output: wrap the `.drawio` XML in a `data-mxgraph` div that
loads `https://viewer.diagrams.net/js/viewer-static.min.js` -> open the HTML in a
browser (multi-page nav included), no install needed.

## Workflow

```
1. Lanes = entities (<=7). Order by who acts first. Vertical columns.
2. Place nodes; align center-X down each lane (P4).
3. Draw edges with fixed connection points; happy path straight down (P2/P3).
4. Decisions: connect at vertices; main exit bottom, branches to sides (P5).
5. Loops/returns: gutter waypoints or connector node (P1/P7).
6. Export PNG -> inspect -> fix by priority order -> repeat until clean.
```
