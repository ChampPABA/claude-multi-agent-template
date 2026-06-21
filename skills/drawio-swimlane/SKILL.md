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

## How to work — Plan, Build, Verify, Fix

Reliable diagrams come from doing these **in order**, not from drawing and hoping.
Each phase has a detailed home below; this is the spine that ties them together:

1. **Plan on paper first.** Before writing any XML, fix the flow **sequence across
   all lanes** (the descending staircase) and write the **per-box port plan** —
   which of the 4 faces each edge uses. Routing conflicts are per-box, not per-edge,
   so deciding ports up front is what prevents the mess. → "Place nodes…" + "Plan
   each box's 4 ports".
2. **Build** the `.drawio` from that plan: lanes, then nodes, then edges with fixed
   connection points. → "draw.io authoring specifics".
3. **Verify** — never trust the XML. Run `scripts/check_layout.py` (a hard gate that
   catches the "looks-right-in-XML but renders broken" faults the eye keeps missing —
   over-the-top back-edges, waypoints inside a box, wrong-side stabs, lines through a
   box), **then** export the PNG and look at it against P1–P8. → "Verify loop".
4. **Fix** by the priority order (lowest P-number wins) and re-verify. A hand edit is
   **not done** until `check_layout.py` exits 0 **and** the re-exported PNG looks
   clean — never declare a diagram finished off an unverified edit.

Why the script+PNG gate: "it looks right in the XML" is the trap. You cannot see an
overlap, a header-crossing, or a 5px misalignment by reading tags. Measure, don't
assume.

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
2. **P2 - Top-down within a lane.** Same-lane flow exits the bottom and enters the
   next box's top, running straight down. But the happy path often **hands off
   sideways to the next lane** - a cross-lane hand-off (including a decision's
   continuing branch) exits the **side facing the target lane**, not the bottom.
   The only upward lines are labeled loops/returns.
3. **P3 - Straight main trunk.** Minimize bends on the happy path; keep it a
   straight line.
4. **P4 - Align node centers** so trunk edges are dead straight (same center-X
   down a lane; same center-Y for a horizontal hand-off).
5. **P5 - Decision diamond connects at its 4 vertices** (top/bottom/left/right
   points), not the flat sides. The **continuing (happy) branch exits toward where
   flow goes next** - the side toward the next lane, or the bottom if it stays in
   lane; each other branch/loop takes a different free vertex by the shortest
   non-crossing route.
6. **P6 - Minimize bends on branch/secondary connectors.**
7. **P7 - Compact.** No big empty gaps; loops use the gutter or a connector node.
   Split a cluster to its own page if it would otherwise need a long stray loop.
8. **P8 - Prefer <=1 connector per side** of a box. *Taste only, not research-
   backed - the weakest rule. Apply only when free at P1-P7; then the
   higher-source connector takes the top, the lower keeps the side.*

Key consequence: **do NOT bend a straight happy-path line just to avoid two
connectors on one side.** Two lines may share a side if they don't cross (P3 > P8).
Full rationale + citations: `references/priority-rules.md`.

## Place nodes to avoid back-edges (descending staircase)

A forward edge should never run *upward* - an upward line reads as a loop and
confuses. Fix this at layout time (node placement), not by rerouting:

- Lay out y by the flow **sequence across all lanes**, not per-lane from the top.
  A later step sits lower than the step that triggers it - even in a different lane -
  so the whole thing becomes a **descending staircase**. A hand-off target placed
  *higher* than its source is forbidden (it forces an accidental back-edge).
- The *only* upward lines allowed are genuine labeled loops/returns (redo,
  reject-back, retry). How each edge actually enters/leaves a box is the **port plan**
  under "draw.io authoring specifics" below.

## draw.io authoring specifics

- **Vertical swimlanes** = lanes side by side as columns, flow top->bottom. Each
  lane: `style="swimlane;html=1;startSize=30;horizontal=1;fillColor=none;"`.
  `horizontal=1` keeps each lane's title a **horizontal bar across the top of its
  column** - the clean, readable header. Do NOT build the pool with
  `childLayout=stackLayout` / `horizontalStack=1`, and do NOT put `horizontal=0` on
  a lane: that rotates the title into vertical text clinging to the lane's left edge
  instead of a top header, and reads as broken. Lanes are **flat siblings**, not a
  managed stack-layout pool. A **diagram title** goes as a horizontal `text` element
  **above the lanes** (smaller negative/lower y than the lane tops), or, if you wrap the
  lanes in a pool, the pool itself uses `horizontal=1` so its title is a top bar too. A
  title **below the pool** or as a vertical strip clinging to the left edge reads as
  broken - `check_layout.py` hard-fails a title placed below the lanes. **Lanes must abut - NO gap between them:** lane(N+1).x =
  lane(N).x + lane(N).width, so borders touch like a real pool (a visible gap
  between lanes reads as broken). Give all lanes the same height. Nodes are children
  of their lane (geometry is lane-relative); edges use `parent="1"` (root) so
  waypoints are in absolute page coords.
- **Page setup - infinite canvas, grid on.** Set the `mxGraphModel` to
  `page="0" grid="1" gridSize="10"` (keep `pageWidth`/`pageHeight` as harmless A4
  stubs, e.g. 1169×827). Why `page="0"`: swimlane heights are unpredictable, and a
  fixed page (`page="1"`) draws page-break dashes slicing the flow the moment content
  exceeds the page height - the diagram looks broken in the editor and you'd have to
  recompute `pageHeight` every time. The **swimlane pool is already the visible
  frame**, so you lose nothing. And it doesn't affect output: PNG/SVG export **crops
  to the content bounding box + border regardless** of page settings, and the grid
  never appears in exports. Use the **same header on every page** of a multi-page file
  so tabs look consistent. (Only switch to `page="1"` with a content-fitted
  `pageWidth`/`pageHeight` if the deliverable is a paginated PDF for print.)

  ```xml
  <mxGraphModel dx="800" dy="600" grid="1" gridSize="10" guides="1" tooltips="1"
    connect="1" arrows="1" fold="1" page="0" pageScale="1"
    pageWidth="1169" pageHeight="827" math="0" shadow="0">
  ```
- **No decoration unless asked:** omit fillColor (white) / strokeColor (black).
  **Terminators are unfilled too** - a Start/End is a plain open `ellipse`
  (`ellipse;whiteSpace=wrap;html=1;`), NOT a solid black BPMN-style dot. Filling it
  black (or any color) you weren't asked for is the same unwanted decoration as
  coloring a process box.
- **Pick the shape from what the step MEANS, not by habit** - a review/approval
  drawn as a plain rectangle hides that a decision is being made. Choose by what the
  step *does*:

  | The step means... | Shape | draw.io style |
  |---|---|---|
  | Start / End of the flow | terminator | `ellipse;whiteSpace=wrap;html=1;` (unfilled) |
  | An action someone performs (submit, create, send, provision) | process | `rounded=0` |
  | A **question that branches** - "approve?", "ready?", pass/fail, or any "evaluates / reviews / checks then forks" | decision | `rhombus` |
  | Generic data input or output (neither a document nor a stored set) | I/O | `shape=parallelogram` |
  | A document / report / form / record produced or consumed | document | `shape=document` |
  | A persistent store read or written (database, queue, registry) | data store | `shape=cylinder` |
  | A whole sub-process expanded on its own page | sub-process | `shape=process` (rectangle with vertical side bars - not a plain box) |

  Rule of thumb: if the flow **forks** at a step (2+ outcomes), it is a decision
  diamond - even if the source word was "evaluates" or "reviews".
- **Flow structure (by the book):** every flow begins at exactly one Start
  terminator and ends at one or more End terminators - nothing enters or leaves a
  flow except through a terminator. **Only a decision diamond may fork** (have more
  than one outgoing edge); every other shape has exactly one outgoing edge on the
  happy path - use a decision to make any branch explicit. Every connector carries
  exactly **one arrowhead at its target end** - no bidirectional or headless lines.
- **Edges - one consistent style, sharp corners:**
  `edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=block;`
  with **fixed connection points** (decision vertices: top `0.5,0` / bottom `0.5,1` /
  left `0,0.5` / right `1,0.5` - never fractional on a rhombus, or the line lands on the
  bounding box instead of the diamond).
- **Routing invariant - one law for every connector.** **Both end segments are straight
  perpendicular stabs into the CENTRE of the face they touch.** The **first** leg leaves
  the source face straight out before any bend - exit a **right** face → go right first,
  a **bottom** → go down first, a **left** → left first, a **top** → up first. The
  **last** leg enters the target face straight in, arrowhead along its travel - **down**
  into a top, **up** into a bottom, **left** into a right face, **right** into a left.
  Never a sideways nub at either end. So a 1-bend L has its single corner at the
  **source centre on the exit axis AND the target centre on the entry axis** - both, not
  one. Then choose faces for the **fewest bends**: **0** when the two centres share an
  axis, **1** when offset on one axis, **2** only when offset on both *and* a 1-bend L
  would cross something (P1 no-crossing always beats saving a bend). General geometry,
  any boxes anywhere. `check_layout.py` hard-fails an off-centre stab at **either** end
  and flags bend-heavy edges as advisory.
- **Routing table - by the position of target T relative to source S (box centres):**

  | T is... | S exits | enters T at | bends | last leg (arrow) |
  |---|---|---|---|---|
  | directly below, same column | bottom | **top-centre** | 0 | straight down |
  | directly above (a loop), column clear | top | **bottom-centre** | 0 | straight up |
  | level, to one side | side toward T | T's near side | 0 | horizontal |
  | lower **and** to one side (forward hand-off) | side toward T | **top-centre** | 1 | run across to T's centre-X, then **down** into the top |
  | lower & to one side, but S's side port is **taken** (e.g. a decision's 2nd branch) | bottom | **top-centre** | 2 | down into the **gap above T** (corner y between the box above T and T.top), across to T's centre-X, then **down** into the top — the across-leg must sit in clear space, never at/below T.top |
  | higher **and** to one side (back-loop) | side toward T | **bottom-centre** or near side | 1 | run across, then **up** into the bottom |
  | lower, but T must be entered on a *side* face | bottom | **the side facing S** | 2 | down to T's centre-Y, then **horizontal** into that side |

  **Reserve a box's vertical ports first** for a straight same-column neighbour or loop
  (0 bends); a diagonal edge then takes a remaining face. If two edges still want one
  face, the straight same-column edge keeps it and the other moves to the face toward
  its own neighbour. *(A box that is both a hand-off target and a loop-end - e.g. a
  a loop-back edge arrives straight up into its bottom while a forward branch enters its
  side - is just two table rows applied to one box.)*
- **Decision ports:** the descending flow enters the **top vertex**; the continuing
  (happy) branch exits toward where flow goes next (the side toward the next lane, or
  the bottom if it stays in lane). Each other branch exits a **remaining free vertex** —
  for a reject/back branch, **never the top** (the top belongs to the incoming flow;
  exiting upward sends the line over everything - the classic over-the-top reject).
  Prefer the **vertex facing the loop target**: if the target box is off to one side,
  exit that **side** so the return is a short horizontal hop into it; use the **bottom**
  only when the target sits below. Keep the loop **tight** - take the shortest in-body
  route to the target's own row; don't drop to the far bottom of the pool just to climb
  all the way back up.
- **The stab in XML (both ends):** the **first waypoint shares the exit port's *other*
  coordinate** and the **last waypoint shares the entry port's *other* coordinate**, so
  each end leg is one clean perpendicular run (lead-in `>=~20px`). For any port:
  top/bottom port -> the waypoint's **X = that box's centre-X**; left/right port -> the
  waypoint's **Y = that box's centre-Y**. A 1-bend L's lone corner must satisfy **both**
  (e.g. side exit + top entry -> corner X = target centre-X *and* corner Y = source
  centre-Y). Off by even ~20px and the router jogs - the exact miscalc `check_layout.py`
  flags at both ends (watch lane-relative vs absolute coords when you compute a centre).
  **Every waypoint must sit in clear space** - a gutter or the gap between boxes -
  **never inside the box it routes to/past, and never on the far side of the face it
  enters.** For a top entry the corner's y must be **above** the box top (so the arrow
  comes *down* into it); for a bottom entry, below; left, to the left; right, to the
  right. A corner that lands centred on the face but *inside* the body still passes a
  naive centre-check yet renders as an arrow stabbing in from the wrong side - so
  `check_layout.py` hard-fails a waypoint inside any box and a last/first waypoint on
  the wrong side of its face.
- **Loops/returns** stay **inside the pool body** and route **down or sideways through
  empty lane space** — never up over the top. A return edge must not pass **above the
  topmost node** or through the **lane-header/title band**: that empty strip "crosses
  nothing", which is exactly why it tempts you, but a line up there reads as broken
  (`check_layout.py` hard-fails it). A genuine back-loop to a *higher* box goes
  straight **up a clear column or an inner gutter** to the target's own row, then
  enters its side — it does not shoot up out of the source and across the top. Take the
  shortest path that crosses no *box* between the ports the plan assigned; detour
  through a gutter inside the pool border only when a direct route would cross a box; if
  even that crosses, use a small connector node (ellipse "back to X"). Explicit
  `<Array as="points">` waypoints, sharp 90deg, **never overlap or cross** another line
  (P1 wins).
- **Crossings that are unavoidable:** add `jumpStyle=arc` to one edge.
- **Multi-page for big flows** (roughly >~12 nodes, or clearly separable phases):
  an **overview page** whose boxes are the sub-processes (`shape=process`) wired
  together as one flow, then **one detail page per sub-process**. Link a sub-process
  box to its page with an **off-page connector** (`shape=offPageConnector`, outward
  pentagon) or a matching page name (`TC-0` overview, `TC-1..n` details) so a reader
  can jump across. The *specific* decomposition - which sub-processes exist, what
  lives on each page - comes from the task, not this skill.

## Verify loop (REQUIRED - never trust the XML)

Two gates, **in order**. Gate 1 is a script so the failure the eye keeps missing
can't slip through; Gate 2 is your eyes on the rendered PNG. Iterate both until the
script exits 0 and the PNG looks clean.

**Gate 1 - `scripts/check_layout.py` (hard gate).** Resolves lane-relative child
geometry to absolute coords and hard-fails (exit 1) the whole class of "looks-right-
in-XML but renders broken" connector faults:
- a waypoint **above the topmost node** or in the **lane-header band** (over-the-top
  back-edge);
- a waypoint sitting **inside any box**, or a first/last waypoint on the **wrong side**
  of the face it leaves/enters (arrow stabs in from inside/beyond - the failure a
  naive centre-check misses);
- an off-centre first/last stab (arrow grazes in sideways);
- an edge segment driven **through a box** that isn't its source/target (P1);
- a **title below the pool**.

It also prints **advisory** notes (never fail the build): edge–edge crossings,
same-side pile-ups (P8), bend-heavy edges, and port-less edges whose ends don't line
up. Fix advisories only if free per the priority order (don't "fix" a P8 case if it
breaks P1-P4).

```bash
python3 scripts/check_layout.py flow.drawio        # exit 1 = fix before going on
```

**Gate 2 - export PNG and look.**

```bash
# WSL2 path to the CLI (adjust per OS: macOS /Applications/draw.io.app/...; Linux: drawio)
DRAWIO="/mnt/c/Program Files/draw.io/draw.io.exe"
WININ=$(wslpath -w flow.drawio)
# -p is 1-based page index; -s scales up for legibility
"$DRAWIO" -x -f png -e -b 10 -p 2 -s 1.5 -o "$(wslpath -w page2.png)" "$WININ"
```

Read the PNG and check against P1-P8. Then fix by priority order, **re-run both
gates**, and repeat. The diagram is done only when Gate 1 exits 0 and the PNG is
clean - not when the XML "looks right".

Optional human-viewable output: wrap the `.drawio` XML in a `data-mxgraph` div that
loads `https://viewer.diagrams.net/js/viewer-static.min.js` -> open the HTML in a
browser (multi-page nav included), no install needed.

## Workflow

```
1. **Lanes = actors who *act*** (a person/team/system that performs a step), not passive receivers. A thing that only *receives* a hand-off - a store that gets written to, an automated notification that gets sent - does NOT earn its own lane; fold it into the lane of whoever triggers or owns it. Cap ~7 (Miller's Law; beyond it, split into sub-process pages). Order by who acts first. Vertical columns.
2. Place nodes; align center-X down each lane (P4).
3. Draw edges: same-lane happy path straight down; cross-lane hand-off exits the side toward the next lane (P2/P3).
4. Decisions: connect at vertices; happy branch exits toward where flow continues, other branches/loops to free vertices (P5).
5. Loops/returns: shortest non-crossing route; gutter or connector node only if a direct route would cross (P1/P7).
6. Verify: run `scripts/check_layout.py` (Gate 1, hard) -> export PNG and inspect (Gate 2) -> fix by priority order -> re-run both gates until the script exits 0 and the PNG is clean.
```
