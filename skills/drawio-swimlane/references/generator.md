# Deterministic backend — `scripts/gen_swimlane.py`

A bundled generator that turns a tiny **JSON flow spec** into a gate-clean `.drawio`. The
model writes only the *semantics* (lanes, nodes, edges as pure topology); the script
computes every coordinate, port and waypoint so the result passes `check_layout.py` by
construction. The model spends **zero tokens on XML geometry** and never emits full XML,
so the Build→Verify→Fix loop (and its 32k-output crashes) is replaced by **spec → generate
→ gate-once**.

Use this for **authoring a new swimlane from a process description** — the common case.
Keep the free-form hand-authoring path (the rest of SKILL.md) for what the engine can't
route cleanly (see "When it can't" below) and for **cleaning up an existing `.drawio`**
(the generator builds from a spec, it does not ingest a diagram).

## Spec schema

```json
{
  "title": "F1 - Create & publish a job",
  "lanes": ["Candidate", "Recruiter", "Hiring Manager", "System"],
  "nodes": [
    {"id": "n1", "lane": 1, "kind": "start",    "text": "Start"},
    {"id": "n2", "lane": 1, "kind": "process",  "text": "Fill job details"},
    {"id": "n3", "lane": 1, "kind": "decision", "text": "Approval required?"},
    {"id": "n4", "lane": 3, "kind": "output",   "text": "Job live"}
  ],
  "edges": [
    {"src": "n1", "dst": "n2"},
    {"src": "n2", "dst": "n3"},
    {"src": "n3", "dst": "n4", "label": "No"},
    {"src": "n3", "dst": "n2", "label": "Yes - revise"}
  ]
}
```

- `lane`: 0-based column index into `lanes` (left→right). Lanes are actors who *act*; cap ~7.
- `row`: optional; defaults to list order. One node per row, descending staircase — order
  `nodes` in flow sequence **across all lanes** so a target is always below its source.
  **Give two steps the SAME `row`** when they are at the same stage in adjacent lanes (e.g. a
  decision and the review it hands to): the hand-off becomes a clean horizontal, and it frees
  the reviewer's top face so a reject loop can leave straight up. The engine routes a back-edge
  out of the source's **top** (straight up, into the target's near side) whenever that top is
  free and the lane above is clear — otherwise it uses a side gutter.
- `kind`: `start end process decision output document store subprocess`. Pick by what the
  step *means* (a step that forks = `decision`; an I/O output = `output` = parallelogram).
  **Terminators (`start`/`end`) carry a short label only** ("Start", "End") — long text
  overflows the ellipse.
- `edges`: pure topology. **The route is inferred** from node positions — do not specify it.
  A decision is the only shape that may have >1 outgoing edge.

The engine assigns shapes (no decorative colour — white fill, black stroke, per the skill),
allocates one connector per box face (decisions fork at distinct vertices; merges enter at
distinct faces), and routes back-edges (loops to a higher row) up an inter-lane gutter with
Left-Edge track nesting, marking a genuinely unavoidable interleave crossing `jumpStyle=arc`.

## Writing a clean spec (what makes it read hand-drawn)

The engine routes whatever topology you give it; these authoring choices are what make the
result look deliberate rather than mechanical. Worked specs in `references/examples/`.

- **Same `row` for same-stage steps in adjacent lanes** — e.g. a decision and the review it
  hands to. Turns the hand-off into a clean horizontal and lets the reject loop leave the
  reviewer's top. (Keep decisions ~2 lanes apart so the horizontal arrow is visible.)
- **One terminal per outcome class, merged** — if two branches both just *end*, point them at
  a **single** `end` node rather than one each ("Declined" + "End"). A long connector into the
  shared End reads as "this path also finishes here".
- **Short terminator labels** — `start`/`end` are small ellipses; use "Start"/"End", not a
  sentence (it overflows).
- **Order nodes in true flow sequence across lanes** so every forward edge points down.
- Let the engine pick routes and faces — never hand-set ports; just describe topology.

## Run

```bash
python3 scripts/gen_swimlane.py spec.json out.drawio
python3 scripts/check_layout.py out.drawio        # MUST run — the honest gate
```

## When it can't (the gate tells you — trust it, don't eyeball)

The engine handles the common topologies. A **congested hub** (e.g. two decisions plus a
return loop converging on one node) can exceed what a deterministic per-node layout places
cleanly. You do **not** judge this by eye — `check_layout.py` now catches it:

- a **HARD** failure (crossing / overlap / shared face-point / through-box), or
- a **`runs alongside`** near-miss advisory (a connector hugging a box it isn't attached to), or
- a `WARN over-envelope` line the generator prints (a node needing >4 faces).

If any of those remain after generation, that diagram is past the engine's envelope:
**author it with the free-form path**, or generate the draft and nudge the few bad
connectors in draw.io desktop. Do not ship a generated diagram that the gate flags.

## Routing rules the engine encodes

Synthesized (NotebookLM) from ELK / yFiles / yEd channel-router / Sugiyama / BPMN + our
gate. Forward: same-lane = straight down (0 bend); cross-lane = 1-bend side→top; same-row =
side→side. Back-edge = exit a free side toward an inter-lane gutter, up the gutter, into a
free side of the target (short spans nest innermost; same-target interleavers that can't be
split get one `jumpStyle=arc`). Merge = the same-lane inbound keeps the straight top; each
cross-lane inbound takes a distinct free face. Decision = enter top vertex; each branch
leaves a distinct vertex toward where it goes.
