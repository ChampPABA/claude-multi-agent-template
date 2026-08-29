---
name: drawio-swimlane
description: Author, clean up, or review draw.io swimlane and cross-functional flowcharts to a professional standard. Make sure to use this skill whenever the user works on a .drawio flowchart, process diagram, or swimlane (lanes per role/entity, top-down process flows with decision diamonds), and ESPECIALLY when connector lines look messy - crossings, overlaps, lines cutting through boxes, too many bends, curved corners, or multiple lines piling on one side of a box. Also use when laying out any top-down flowchart or process map in draw.io even if the word "swimlane" is not said, or when someone asks to make a .drawio diagram "cleaner / straighter / prettier" or "fix the arrows". Encodes an evidence-based priority order (Purchase/Ware graph-aesthetics research) for resolving layout conflicts, the draw.io XML specifics (fixed connection points, 90-degree corners, decision-vertex connections, gutter/connector-node loops), and a script layout-gate (check_layout.py) that catches the render-breaking faults, plus a final visual check only when the gate cannot see an edge. Its deterministic generator also builds multi-page overview+detail documents (sub-process bands spanning lanes, one detail page per band) and never overwrites a hand-edited .drawio.
allowed-tools: Read, Write, Edit, Bash
---

# draw.io Swimlane Flowchart Skill

Produce clean, professional swimlane (cross-functional) flowcharts as native
`.drawio` files, and fix messy ones. The hard part is connector routing; this
skill gives a **priority-ordered rule set** so conflicts resolve by evidence, not
guesswork, and a **script gate** (`check_layout.py`) that turns the render-breaking
faults the eye keeps missing into hard failures — so the layout converges in the XML
instead of in an expensive look-at-the-PNG loop.

## Two ways to build — pick by the task

- **Authoring a new swimlane from a process description → use the deterministic backend**
  (`scripts/gen_swimlane.py`). Write a tiny JSON flow spec (lanes + nodes + edges as pure
  topology); the script computes all geometry and emits a gate-clean `.drawio`. The model
  spends **zero tokens on XML** and never re-emits full XML, so there is no Build→Verify→Fix
  loop and no 32k-output crash. This is the common case and the default. **→ read
  `references/generator.md` for the spec schema and how to run it.** Run `check_layout.py`
  after — if it flags a HARD fault, a `runs alongside` near-miss, or the generator prints
  `WARN over-envelope`, that diagram is a congested hub past the engine's envelope: fall back
  to the hand-authoring path below (or nudge the few bad connectors in draw.io desktop).
  A big flow (multi-phase) is the same one spec with a `pages` array: an **overview page**
  of sub-process bands + one **detail page** per band (see `references/generator.md`).

  **File lifecycle:** a generated `.drawio` is spec-owned until its first hand edit; the
  generator embeds a per-page provenance hash and **refuses to overwrite a hand-edited
  page** (exit 1, naming it). Once hand-edited, that `.drawio` — not the spec — is the
  source of truth: keep editing the XML. Delete/rename the file to regenerate; there is
  no `--force`.
- **Cleaning up an existing messy `.drawio`, or a congested hub the generator can't route**
  → hand-author with the Plan / Build / Verify / Fix process below. The generator builds
  from a spec; it cannot ingest and reroute an existing diagram.

## How to work — Plan, Build, Verify, Fix

Reliable diagrams come from doing these **in order**, not from drawing and hoping:

1. **Plan on paper first.** Fix the flow **sequence across all lanes** (the descending
   staircase) and the **per-box port plan** — which of the 4 faces each edge uses.
   Routing conflicts are per-box, not per-edge, so deciding ports up front is what
   prevents the mess.
2. **Build** the `.drawio` from that plan: lanes, then nodes, then edges with fixed
   connection points.
3. **Verify** with `scripts/check_layout.py` (the hard gate). It catches the
   "looks-right-in-XML but renders broken" faults — over-the-top back-edges, waypoints
   inside a box, wrong-side stabs, lines through a box, **and crossings (P1)**. Only do
   the PNG glance when the gate says it couldn't see an edge. → "Verify loop".
4. **Fix** by the priority order (lowest P-number wins) and re-run the gate. A hand edit
   is **not done** until `check_layout.py` exits 0.

Why a script gate, not eyeballing: "it looks right in the XML" is the trap — you cannot
see an overlap, a header-crossing, or a 5px misalignment by reading tags. The script
measures it. The PNG used to be a mandatory loop; it is now a **single final glance**,
needed only for the one thing the script can't trace (see "Verify loop").

## Scale the process to the diagram size

- **Small (≤~12 nodes, ≤2–3 lanes):** build it **inline in one pass** — no need to spin
  up a separate agent. Plan ports, write the XML, run Gate 1. If the gate exits 0 with no
  auto-route advisory, it is done — **no PNG render**.
- **Large / multi-phase (>~12 nodes, or clearly separable phases):** split into
  an overview page + one detail page per sub-process — one spec, `pages` array
  (`references/generator.md`; binding rules in `references/routing.md` §7) — and do
  the single final visual glance.

## Triggers

- "create a swimlane / cross-functional flowchart"
- "make this .drawio flow cleaner", "lines are crossing / overlapping / messy"
- "draw the process flow for X with lanes per role"
- "ทำ flowchart / swimlane", "เส้นมันทับกัน ปรับให้สวย"

## Priority order (resolve any conflict by lowest P-number)

When two layout rules conflict, the higher-priority (lower-numbered) rule wins.

| P | Rule |
|---|------|
| **P1** | **No crossings / no overlapping lines.** Reroute (extra bends, outer gutter, connector node) rather than cross. *Strongest readability factor (Purchase 1997, Ware 2002).* |
| **P2** | **Top-down within a lane.** Same-lane flow exits the bottom, enters the next box's top, straight down. A cross-lane hand-off (incl. a decision's continuing branch) exits the **side facing the target lane**. Only labeled loops/returns go upward. |
| **P3** | **Straight main trunk.** Minimize bends on the happy path. |
| **P4** | **Align node centers** so trunk edges are dead straight (same center-X down a lane; same center-Y for a horizontal hand-off). |
| **P5** | **Decision diamond connects at its 4 vertices** (top/bottom/left/right points), not the flat sides. The continuing branch exits toward where flow goes next; other branches take a free vertex by the shortest non-crossing route. |
| **P6** | **Minimize bends on branch/secondary connectors.** |
| **P7** | **Compact.** No big empty gaps; loops use the gutter or a connector node. Split a cluster to its own page rather than draw a long stray loop. |
| **P8** | **Prefer ≤1 connector per side** of a box. *Taste only, weakest rule — apply only when free at P1–P7.* |

Key consequence: **do NOT bend a straight happy-path line just to avoid two connectors on
one side.** Two lines may share a side if they don't cross (P3 > P8). Full rationale +
citations: `references/priority-rules.md`.

## Place nodes to avoid back-edges (descending staircase)

A forward edge should never run *upward* — an upward line reads as a loop and confuses.
Fix this at layout time (node placement), not by rerouting:

- Lay out y by the flow **sequence across all lanes**, not per-lane from the top. A later
  step sits lower than the step that triggers it — even in a different lane — so the whole
  thing becomes a **descending staircase**. A hand-off target placed *higher* than its
  source is forbidden (it forces an accidental back-edge).
- The *only* upward lines allowed are genuine labeled loops/returns (redo, reject-back,
  retry).

## draw.io authoring specifics

- **Vertical swimlanes** = lanes side by side as columns, flow top→bottom. Each lane:
  `style="swimlane;html=1;startSize=30;horizontal=1;fillColor=none;"`. `horizontal=1`
  keeps each lane's title a **horizontal bar across the top of its column**. Do NOT build
  the pool with `childLayout=stackLayout` / `horizontalStack=1`, and do NOT put
  `horizontal=0` on a lane (that rotates the title into vertical text clinging to the left
  edge — reads as broken). Lanes are **flat siblings**. A **diagram title** goes as a
  horizontal `text` element **above the lanes** (smaller y than the lane tops); a title
  below the pool or as a left-edge vertical strip reads as broken — `check_layout.py`
  hard-fails a title placed below the lanes. **Lanes must abut — NO gap:**
  lane(N+1).x = lane(N).x + lane(N).width, same height for all. Nodes are children of
  their lane (geometry is lane-relative); edges use `parent="1"` (root) so waypoints are
  in absolute page coords.
- **Page setup — infinite canvas, grid on.** Set the `mxGraphModel` to
  `page="0" grid="1" gridSize="10"` (keep `pageWidth`/`pageHeight` as harmless A4 stubs).
  Swimlane heights are unpredictable; a fixed page draws page-break dashes slicing the
  flow. PNG/SVG export crops to the content bounding box + border regardless, and the grid
  never appears in exports. Use the **same header on every page** of a multi-page file.
  (Only switch to `page="1"` with a content-fitted size if the deliverable is a print PDF.)

  ```xml
  <mxGraphModel dx="800" dy="600" grid="1" gridSize="10" guides="1" tooltips="1"
    connect="1" arrows="1" fold="1" page="0" pageScale="1"
    pageWidth="1169" pageHeight="827" math="0" shadow="0">
  ```
- **No decoration unless asked:** omit fillColor (white) / strokeColor (black).
  **Terminators are unfilled too** — a Start/End is a plain open `ellipse`
  (`ellipse;whiteSpace=wrap;html=1;`), NOT a solid black BPMN dot.
- **Pick the shape from what the step MEANS, not by habit:**

  | The step means... | Shape | draw.io style |
  |---|---|---|
  | Start / End of the flow | terminator | `ellipse;whiteSpace=wrap;html=1;` (unfilled) |
  | An action someone performs (submit, create, send) | process | `rounded=0` |
  | A **question that branches** — "approve?", pass/fail, any "evaluates/reviews then forks" | decision | `rhombus` |
  | Generic data input or output | I/O | `shape=parallelogram` |
  | A document / report / form / record | document | `shape=document` |
  | A persistent store read or written (db, queue, registry) | data store | `shape=cylinder` |
  | A whole sub-process expanded on its own page | sub-process | `shape=process` |

  Rule of thumb: if the flow **forks** at a step (2+ outcomes), it is a decision diamond —
  even if the source word was "evaluates" or "reviews".
- **Flow structure (by the book):** every flow begins at exactly one Start terminator and
  ends at **one merged End** — point every path that merely finishes at the SAME End node;
  reserve multiple Ends for genuinely distinct fates, each labelled differently
  (อนุมัติ vs ยกเลิก) — nothing enters or leaves except through a
  terminator. **Only a decision diamond may fork** (>1 outgoing edge), and **every
  out-edge of a decision carries a branch label — the WORD PAIR only**
  (ได้/ไม่ได้, ใช่/ไม่ใช่, Yes/No; never "No - feedback");
  every other shape has exactly one outgoing edge on the happy path. Labels stay terse:
  no `(annotation)` parentheses, `&` not `+`, no sequence/funnel numbers. Every connector
  carries exactly **one arrowhead at its target end** — no bidirectional or headless
  lines. (The generator lints all of these — `references/generator.md`.)
- **Edges — one consistent style, sharp corners:**
  `edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=block;`
  with **fixed connection points** (decision vertices: top `0.5,0` / bottom `0.5,1` /
  left `0,0.5` / right `1,0.5` — never fractional on a rhombus).
- **Routing invariant — one law for every connector.** Both end segments are straight
  perpendicular stabs into the **centre** of the face they touch (exit straight out before
  any bend, enter straight in along the arrow — never a sideways nub at either end). Pick
  faces for the **fewest bends**: 0 when the two box centres share an axis, 1 when offset
  on one axis, 2 only when offset on both *and* a 1-bend L would cross something (P1
  beats saving a bend). `check_layout.py` enforces this. **The routing table (which face
  for which target position), the exact waypoint coordinates, decision-diamond ports,
  loop/return routing, and multi-page layout are in `references/routing.md` — read it the
  moment an edge won't route cleanly.** An auto-routed edge with no explicit waypoints on
  perpendicular faces is the one geometry the gate cannot trace — give it an explicit
  corner waypoint.

## Verify loop

Gate 1 (the script) is the **primary** gate and runs every time. It now catches the full
P1 set — including **crossings** — as hard failures, so it stands in for the eye on every
render-breaking fault. Gate 2 (PNG) is a **single final glance**, not a loop, and is
needed only when the script tells you it couldn't see an edge.

**Gate 1 — `scripts/check_layout.py` (hard gate).** Resolves lane-relative geometry to
absolute coords and hard-fails (exit 1):
- a waypoint **above the topmost node** or in the **lane-header band** (over-the-top
  back-edge);
- a waypoint **inside any box**, or a first/last waypoint on the **wrong side** of the
  face it leaves/enters;
- an **off-centre** first/last stab;
- a segment driven **through a box** that isn't its source/target (P1);
- **two edges that cross** (P1) — unless one carries `jumpStyle=arc` to declare the
  crossing legible/unavoidable;
- a **title below the pool**.

Advisory (never fail): P8 same-side pile-ups, bend-heavy edges, and **auto-route**
(portless / perpendicular-face) edges. That last one is the PNG tripwire below.

```bash
python3 scripts/check_layout.py flow.drawio        # exit 1 = fix before going on
```

**Gate 2 — final visual glance (conditional, capped — NOT a loop).**

- **Skip the PNG** when Gate 1 exits 0 **and prints no auto-route advisory.** That means
  the script traced every edge's real geometry, so a render cannot reveal a routing fault
  it didn't already catch. Small inline diagrams almost always land here.
- **Render once** when an auto-route advisory remains (the script couldn't trace that
  edge) **or** the diagram is large/complex enough that label overflow, spacing, or lane
  balance matter. Export **one** PNG at `-s 1` and look.
- **Cap: at most ~2 renders.** If it still isn't clean after a second look, **stop and
  report** what's wrong rather than looping out more PNGs. The script — not repeated
  rendering — is what converges the layout.

```bash
# WSL2 path (adjust per OS: macOS /Applications/draw.io.app/...; Linux: drawio)
DRAWIO="/mnt/c/Program Files/draw.io/draw.io.exe"
WININ=$(wslpath -w flow.drawio)
"$DRAWIO" -x -f png -e -b 10 -p 2 -s 1 -o "$(wslpath -w page2.png)" "$WININ"   # -p is 1-based
```

The diagram is **done** when Gate 1 exits 0 and either no auto-route advisory remained or
the single PNG looked clean — not when the XML "looks right".

Optional human-viewable output: wrap the `.drawio` XML in a `data-mxgraph` div that loads
`https://viewer.diagrams.net/js/viewer-static.min.js` → open the HTML in a browser
(multi-page nav included), no install needed.

## Workflow

```
1. Lanes = actors who *act* (a person/team/system that performs a step), not passive
   receivers. A store that only gets written to, or a notification that only gets sent,
   does NOT earn a lane — fold it into the lane of whoever triggers it. Cap ~7
   (Miller's Law). Order by who acts first. Vertical columns, abutting.
2. Place nodes; align center-X down each lane (P4); descending staircase across lanes.
3. Draw edges: same-lane happy path straight down; cross-lane hand-off exits the side
   toward the next lane (P2/P3). Routing detail → references/routing.md.
4. Decisions: connect at vertices; happy branch exits toward where flow continues, other
   branches/loops to free vertices (P5). Label every out-edge.
5. Loops/returns: shortest non-crossing route inside the pool body (P1/P7).
6. Verify: run scripts/check_layout.py (hard). Fix by priority order; re-run until exit 0.
   Render one PNG only if an auto-route advisory remains or the flow is large (cap ~2).
```
