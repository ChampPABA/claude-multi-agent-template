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
(the generator builds from a spec; it does not ingest a diagram).

## Spec schema

**One page** — a short flow stays in the original flat form:

```json
{
  "title": "F1 - Publish a job",
  "verbs": ["Fill", "Publish", "Approve"],
  "lanes": ["Recruiter", "Hiring Manager"],
  "nodes": [
    {"id": "F1-s",  "lane": 0, "kind": "start",    "text": "Start"},
    {"id": "F1-t1", "lane": 0, "kind": "process",  "text": "Fill job details", "page": "P2"},
    {"id": "F1-d1", "lane": 0, "kind": "decision", "text": "Approval required?"},
    {"id": "F1-t2", "lane": 0, "kind": "process",  "text": "Publish job",
     "changes": "Job → live", "errors": ["duplicate title"]},
    {"id": "F1-e",  "lane": 0, "kind": "end",      "text": "Job live"}
  ],
  "edges": [
    {"src": "F1-s",  "dst": "F1-t1"},
    {"src": "F1-t1", "dst": "F1-d1"},
    {"src": "F1-d1", "dst": "F1-t2", "label": "No"},
    {"src": "F1-d1", "dst": "F1-t1", "label": "Yes"},
    {"src": "F1-t2", "dst": "F1-e"}
  ]
}
```

**Multiple pages** — an overview + one detail page per sub-process. Same file, one
`pages` array, one `.drawio` with a `<diagram>` per page:

```json
{
  "title": "LeadX Flow",
  "pages": [
    {"name": "L0 - Overview", "type": "overview",
     "lanes": ["Customer", "LeadX", "AIA"],
     "nodes": [
       {"id": "s",  "lane": 0, "kind": "start", "text": "Start"},
       {"id": "b1", "kind": "subprocess", "text": "L1 - สมัครและคัดกรอง",
        "spans": ["Customer", "LeadX"], "expands_to": "L1 - สมัครและคัดกรอง"},
       {"id": "b2", "kind": "subprocess", "text": "L2 - ออกแบบแผน",
        "spans": ["LeadX", "AIA"], "expands_to": "L2 - ออกแบบแผน"},
       {"id": "e",  "lane": 2, "kind": "end", "text": "ออกกรมธรรม์แล้ว"}
     ],
     "edges": [{"src": "s", "dst": "b1"}, {"src": "b1", "dst": "b2"}, {"src": "b2", "dst": "e"}]}
  ]
}
```

(Worked multi-page example: `references/examples/leadx-overview.json`.)

- `lane`: 0-based column index into `lanes` (left→right). Lanes are actors who *act*; cap ~7.
- `row`: optional; defaults to list order. One node per row, descending staircase — order
  `nodes` in flow sequence **across all lanes** so a target is always below its source.
  **Give two steps the SAME `row`** when they are at the same stage in adjacent lanes (e.g. a
  decision and the review it hands to): the hand-off becomes a clean horizontal, and it frees
  the reviewer's top face so a reject loop can leave straight up. The engine routes a back-edge
  out of the source's **top** (straight up, into the target's near side) whenever that top is
  free and the lane above is clear — otherwise it uses a side gutter.
- `id`: the box's **permanent step id** (e.g. `A3-t1`); the renderer numbers boxes from it
  and the JSON's non-visual data is keyed by it, so never renumber.
- `kind`: BPMN-lite only — `start end process decision subprocess`, plus `document` for a
  real hand-off. Anything else (`output`, `store`) is a FAIL. Pick by what the step *means*
  (a step that forks = `decision`). The `end` text names the outcome ("Partner active").
- `system`: the system the step is done in (e.g. `aaa-portal`); never a lane name. The
  engine draws one dashed lasso frame per system cluster (a member row gap > 2 starts a new
  frame): it encloses the members, notches around every other box, and may cross lanes.
  It is emitted as a dashed polyline edge (`sysframe=1`, no source/target) behind the
  boxes, so its corners stay draggable in draw.io. A box can't have both `system` and
  `outside` (FAIL). Worked example: `references/examples/aaa-partner-signing.json`.
- `outside`: where an out-of-system step happens (`"LINE"`) → second line "นอกระบบ · LINE".
- `type`: `user | manual | service | send`; `service` (work the system starts by itself)
  adds the sub-line "ระบบทำเอง". What the system does after a click is NOT a box — put it
  in the clicked box's `changes`.
- `page`, `changes` (entity → state), `errors` (failure cases), and spec-level `verbs` /
  `entities`: data for the step table and the dev, passed through untouched.
- `edges`: pure topology. **The route is inferred** from node positions — do not specify it.
  A decision is the only shape that may have >1 outgoing edge.

### Overview pages (`type: "overview"`)

An overview page is the reader's map: **sub-process bands, one per detail page**, wired as
one flow — not a finer copy of the detail. Rules:

- A band is a `subprocess` node with **`spans`: the lane NAMES it involves**. The engine
  draws it as a child of the pool spanning those lanes **inset from their borders** (it
  floats over the lanes — never pasted onto the lane separator lines), uniform height,
  text wraps, below the lane-header band.
- **Lane order is re-derived by participant clustering** (lanes that share a band sit
  adjacent, hubs central) so every band's span is minimal — write lanes in any order. Plain
  lane-numbered nodes (a Start/End) follow the same reorder. Detail pages keep YOUR order,
  so mirror the overview's clustered order there when the flow allows: one canonical column
  map for the whole document reads best.
- `expands_to` binds a band to its detail page. Binding is **linted hard** (a FAIL, not a
  warning): the band's `text` must EQUAL the page name, one band : one detail page, the
  page must exist, and the detail page's lanes should sit inside the band's `spans`
  (warning).
- Keep overview labels terse **block names** — no step/funnel numbers, no annotations.

### Defaults the generator enforces (WARN lines — taste, not blockers)

From real usage: every repeated hand fix became a lint so the spec reads right the first
time. Fix WARNs unless you mean otherwise:

- **One merged End per fate.** Multiple End nodes with the same label (or bare "End"s)
  → merge into one End; reserve multiple Ends for genuinely distinct fates, each labelled
  differently (อนุมัติ vs ยกเลิก).
- **Every decision out-edge carries a branch label, and it is the WORD PAIR only**
  (ได้/ไม่ได้, ใช่/ไม่ใช่, Yes/No, ครบ/ไม่ครบ) — never "No - feedback"; where the arrow
  lands already says what happens. The rendered label rides **next to the decision**
  (near the source end), not at mid-edge.
- **Terse labels:** no `(parenthesis) annotations` in node text or edge labels (put the
  annotation in a note), no leading step numbers on any page.
- **One box = one action:** `&` or `+` in a label warns (split the box); `และ` in a task
  warns softly (fine only when truly inseparable). With a spec `verbs` list, a task label
  must start with one of those verbs (prefix match, so it works for Thai).
- **`[TBD]` is allowed** in a label; the run ends with "N box(es) still [TBD]".
- **FAILs:** a kind outside the BPMN-lite budget, an unknown `type`, a lane named after a
  system used in `system`, a box with both `system` and `outside`.

## Run

```bash
python3 scripts/gen_swimlane.py spec.json out.drawio
python3 scripts/check_layout.py out.drawio        # MUST run — the honest gate
```

### File lifecycle — the guard (no `--force`, by design)

A generated `.drawio` is **spec-owned until its first hand edit**. The generator embeds a
per-page provenance hash, and **refuses (exit 1, naming the page) to overwrite a file whose
page changed since it was generated** — your hand edits are never silently destroyed:

```
REFUSE: page 'L1 - Apply' in flow.drawio was hand-edited (or wasn't generated by this
script). The .drawio is now the source of truth: edit its XML directly, or delete/rename
the file to regenerate.
```

Once you hand-edit, **keep editing the XML directly**; the spec is stale from that moment.
To regenerate from a spec you have deliberately changed, delete or rename the old file —
that manual step IS the safety mechanism (there is no `--force` to mistype past).
A file with no provenance hash (hand-built, or generated by an older version) is also
refused — rename it aside once, then generate.

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
leaves a distinct vertex toward where it goes. Bands on an overview route by their centre
lane with the same rules.
