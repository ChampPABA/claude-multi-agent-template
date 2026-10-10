#!/usr/bin/env python3
"""Deterministic draw.io vertical-swimlane generator.

The model writes a tiny JSON spec (lanes + nodes + edges as pure topology); this engine
computes ALL geometry/ports/waypoints so the output passes scripts/check_layout.py by
construction. No model tokens are spent on XML, and no full XML is ever emitted by the
model -> the 32k-output spawn crash cannot occur.

Routing rules are the NotebookLM synthesis of ELK / yFiles / yEd channel-router / Sugiyama
+ our own routing.md / priority-rules.md (see references/routing.md).

Spec JSON - one page (a short flow; the original flat form):
{
  "title": "F1 - ...",
  "lanes": ["Candidate", "Recruiter", ...],          # columns, left to right
  "nodes": [{"id":"n1","lane":0,"kind":"process","text":"...", "row":0?}],
  "edges": [{"src":"n1","dst":"n2","label":"Yes"?}]   # route is INFERRED from geometry
}

Spec JSON - multi-page (an overview + one detail page per sub-process):
{
  "title": "LeadX Flow",
  "pages": [
    {"name": "L0 - Overview", "type": "overview",
     "lanes": ["Customer", "LeadX", "AIA"],
     "nodes": [{"id":"b1","kind":"subprocess","text":"L1 - Apply",
                "spans":["Customer","LeadX"], "expands_to":"L1 - Apply"}],
     "edges": [...]},
    {"name": "L1 - Apply", "type": "detail", "lanes":[...], "nodes":[...], "edges":[...]}
  ]
}

Overview pages: a node with "spans" (lane NAMES) becomes a band covering exactly those
lanes - a child of the pool, width = the spanned lane widths, uniform height, placed
below the lane-header band. Lane order on an overview is re-derived by participant
clustering (co-blocked lanes adjacent, hubs central) so every band's span is minimal;
detail pages keep the author's flow order. "expands_to" binds a band to its detail page
(lint: band text == page name, 1:1, detail lanes within the band's span).

kinds (BPMN-lite): start end process decision subprocess (+ document for a real hand-off)
Optional node fields: outside ("LINE" -> sub-line "นอกระบบ · LINE"), type (user|manual|service|send;
service -> sub-line "ระบบทำเอง"), system ("aaa-portal" -> the box sits inside that system's dashed
lasso frame), page/changes/errors (passed through). Spec-level: verbs, entities.
Usage: python3 gen_swimlane.py spec.json out.drawio
       python3 gen_swimlane.py --read flow.drawio spec.json   # hand-edited drawio -> spec + report
"""
import json, sys, os, re, hashlib, html as _html
from itertools import permutations

LANE_W = 195
POOL_X, POOL_Y = 56, 60
ROW0, ROWSTEP = 120, 90
GUT = 12          # how far inside a lane-boundary/pool-margin a back-edge track sits
TRACK = 14        # spacing between nested back-edge tracks (Left-Edge)
STAB = 16         # min straight stab from the gutter into the target face (so the arrow reads)
BAND_H = 50       # uniform height of an overview spanning band
BAND_INSET = 14   # gap between a band and the lane borders it spans (a band must read as
                  # floating over the lanes, not pasted onto their separator lines)
LBL_X = -0.7      # edge-label position along the edge: toward the SOURCE, so a branch label
                  # (Yes/No) sits by the decision that forked it, not at mid-edge

# kind -> (w, h, style)  — BPMN-lite 5-shape budget (+ document only for a real hand-off).
# NO decorative colour (white fill, black stroke). Start/End are small circles; the End is
# thick and its label (the outcome) sits BELOW it; the Start label sits to its LEFT so it
# never lands on the connector leaving its bottom.
CIRCLE = "ellipse;aspect=fixed;html=1;"   # no wrap: the outcome label sits outside a 36px circle
KIND = {
    "start":      (36, 36, CIRCLE + "labelPosition=left;verticalLabelPosition=middle;align=right;verticalAlign=middle;spacingRight=6;"),
    "end":        (36, 36, CIRCLE + "strokeWidth=3;labelPosition=center;verticalLabelPosition=bottom;align=center;verticalAlign=top;"),
    "process":    (150, 50, "rounded=1;whiteSpace=wrap;html=1;"),
    "decision":   (140, 80, "rhombus;whiteSpace=wrap;html=1;"),
    "document":   (150, 60, "shape=document;whiteSpace=wrap;html=1;"),
    "subprocess": (150, 50, "shape=mxgraph.bpmn.task;taskMarker=abstract;isLoopSub=1;"
                            "rectStyle=rounded;size=10;fillColor=#FFFFFF;whiteSpace=wrap;html=1;"),
}
TYPES = ("user", "manual", "service", "send")   # optional node "type"; service = system-started work
SUBLINE_H = 12    # extra box height when a node carries a small second line
EDGE = ("edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;"
        "html=1;endArrow=block;endFill=1;")

def subline(n):
    if n.get("outside"):
        return f"นอกระบบ · {n['outside']}"
    if n.get("type") == "service":
        return "ระบบทำเอง"
    return ""

def label_html(n):
    """Node value: the label, plus an optional smaller second line (where / who does it)."""
    txt = _html.escape(n.get("text", ""))
    sub = subline(n)
    return f'{txt}<br><font style="font-size:10px">{_html.escape(sub)}</font>' if sub else txt

def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;"))

# ---- face helpers: (exitX,exitY) fractions on the box, draw.io convention ----
TOP, BOT, LEFT, RIGHT = (0.5, 0), (0.5, 1), (0, 0.5), (1, 0.5)

def infer_route(s, t):
    if s["id"] == t["id"]:               return "self"
    if t["row"] > s["row"]:
        return "v" if t["lane"] == s["lane"] else "L"
    if t["row"] == s["row"]:             return "h"
    return "up"                           # t.row < s.row  -> back-edge

def get_pages(spec):
    """Normalize the flat single-page spec and the pages[] form into one list."""
    if "pages" in spec:
        return spec["pages"]
    page = {k: spec[k] for k in ("lanes", "nodes", "edges")}
    page["name"] = spec.get("title", "Flow")
    return [page]

def clustered_order(lanes, blocks):
    """Lane order for an overview page: participants that share a band sit adjacent,
    hubs end up central - achieved by minimizing the total span of every band. Ties
    resolve to the order nearest the author's, so nothing shuffles without a reason.
    Brute force is fine: lanes are capped ~7 (40320 perms, instant)."""
    N = len(lanes)
    if N <= 1 or not blocks or N > 8:
        return list(range(N))
    pos = {nm: i for i, nm in enumerate(lanes)}
    blk = [[pos[nm] for nm in b if nm in pos] for b in blocks]
    blk = [b for b in blk if len(b) > 1]
    if not blk:
        return list(range(N))
    best, best_key = None, None
    for perm in permutations(range(N)):          # perm[k] = original index at column k
        at = [0] * N
        for k, o in enumerate(perm):
            at[o] = k
        span = sum(max(at[i] for i in b) - min(at[i] for i in b) for b in blk)
        shift = sum(abs(at[o] - o) for o in range(N))
        key = (span, shift)
        if best is None or key < best_key:
            best, best_key = perm, key
    return list(best)

# ------------------------------------------------------------ system frames ----
# A frame says WHERE a step is done (aaa-portal, Google Sheet...), not which software
# component does it. It is a dashed orthogonal LASSO: it hugs a system's boxes, bends
# around out-of-system boxes (a notch) and may cross lanes. Built on a compressed grid
# whose lines are the rect edges, so the outline is exact and the grid stays tiny.
FRAME_PAD = 8      # frame -> member box gap
FRAME_MARGIN = 8   # frame -> non-member box gap
FRAME_GAP_ROWS = 2 # a member row gap above this starts a separate frame (no swiss cheese)
FRAME_STYLE = ("endArrow=none;startArrow=none;dashed=1;dashPattern=8 4;rounded=0;html=1;"
               "edgeStyle=none;strokeColor=#5B7FA6;fontColor=#5B7FA6;fontSize=11;"
               "labelBackgroundColor=#FFFFFF;align=left;verticalAlign=bottom;sysframe=1;")

def _grow(r, d):
    return (r[0] - d, r[1] - d, r[2] + d, r[3] + d)

def _hit(a, b):                                   # open rects overlap
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]

def _lasso(members, others, top_limit):
    """Rectilinear outline loops around `members` (rects x0,y0,x1,y1) avoiding `others`."""
    mem = [(r[0], max(r[1], top_limit), r[2], r[3]) for r in (_grow(r, FRAME_PAD) for r in members)]
    bb = (min(r[0] for r in mem), max(min(r[1] for r in mem), top_limit),
          max(r[2] for r in mem), max(r[3] for r in mem))
    obs = [_grow(r, FRAME_MARGIN) for r in others if _hit(_grow(r, FRAME_MARGIN), bb)]
    raw = [_grow(r, 2) for r in others]
    notches = []
    for _ in range(len(obs) + 1):                 # each pass opens at most one enclosed obstacle
        xs = sorted({v for r in [bb] + mem + obs + notches for v in (r[0], r[2])})
        ys = sorted({v for r in [bb] + mem + obs + notches for v in (r[1], r[3])})
        nx, ny = len(xs) - 1, len(ys) - 1
        inside = lambda px, py, rs: any(r[0] < px < r[2] and r[1] < py < r[3] for r in rs)
        fill = set()
        for i in range(nx):
            for j in range(ny):
                px, py = (xs[i] + xs[i + 1]) / 2, (ys[j] + ys[j + 1]) / 2
                on = inside(px, py, [bb]) and not inside(px, py, obs + notches)
                on = (on or inside(px, py, mem)) and not inside(px, py, raw)
                if on:
                    fill.add((i, j))
        # out-cells not reachable from the bbox border = an enclosed (hole) obstacle
        seen, stack = set(), [(i, j) for i in range(nx) for j in range(ny)
                              if (i in (0, nx - 1) or j in (0, ny - 1)) and (i, j) not in fill]
        while stack:
            c = stack.pop()
            if c in seen:
                continue
            seen.add(c)
            i, j = c
            for d in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
                if 0 <= d[0] < nx and 0 <= d[1] < ny and d not in fill:
                    stack.append(d)
        hole = [(i, j) for i in range(nx) for j in range(ny) if (i, j) not in fill and (i, j) not in seen]
        if not hole:
            break
        i, j = hole[0]
        px, py = (xs[i] + xs[i + 1]) / 2, (ys[j] + ys[j + 1]) / 2
        o = next((r for r in obs if r[0] <= px <= r[2] and r[1] <= py <= r[3]), None)
        if o is None:
            break
        cuts = [(o[0] - bb[0], (bb[0] - 1, o[1], o[0], o[3])), (bb[2] - o[2], (o[2], o[1], bb[2] + 1, o[3])),
                (o[1] - bb[1], (o[0], bb[1] - 1, o[2], o[1])), (bb[3] - o[3], (o[0], o[3], o[2], bb[3] + 1))]
        ok = [c for c in sorted(cuts) if not any(_hit(c[1], m) for m in mem)]
        if not ok:
            break                                 # ponytail: no clean notch -> hole stays, gate flags it
        notches.append(ok[0][1])
    # keep components that hold a member, trace each one's boundary into loops
    comp, loops = {}, []
    for start in fill:
        if start in comp:
            continue
        stack, k = [start], len(set(comp.values()))
        while stack:
            c = stack.pop()
            if c in comp or c not in fill:
                continue
            comp[c] = k
            i, j = c
            stack += [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]
    for k in set(comp.values()):
        cells = {c for c, v in comp.items() if v == k}
        if not any(any(m[0] < (xs[i] + xs[i + 1]) / 2 < m[2] and m[1] < (ys[j] + ys[j + 1]) / 2 < m[3]
                       for m in members) for i, j in cells):
            continue
        nxt = {}
        for i, j in cells:                         # clockwise directed boundary edges (y down)
            x0, x1, y0, y1 = xs[i], xs[i + 1], ys[j], ys[j + 1]
            if (i, j - 1) not in cells: nxt.setdefault((x0, y0), []).append((x1, y0))
            if (i + 1, j) not in cells: nxt.setdefault((x1, y0), []).append((x1, y1))
            if (i, j + 1) not in cells: nxt.setdefault((x1, y1), []).append((x0, y1))
            if (i - 1, j) not in cells: nxt.setdefault((x0, y1), []).append((x0, y0))
        while nxt:
            p0 = min(nxt, key=lambda p: (p[1], p[0]))
            loop, p = [p0], p0
            while True:
                q = nxt[p].pop()
                if not nxt[p]:
                    del nxt[p]
                if q == p0:
                    break
                loop.append(q); p = q
            simp = [pt for a, pt, b in zip(loop[-1:] + loop[:-1], loop, loop[1:] + loop[:1])
                    if not ((a[0] == pt[0] == b[0]) or (a[1] == pt[1] == b[1]))]
            k0 = min(range(len(simp)), key=lambda t: (simp[t][1], simp[t][0]))
            loops.append(simp[k0:] + simp[:k0])
    return loops

def system_frames(nodes, top_limit):
    """[(system name, [corner points])] - one or more lasso loops per system."""
    rect = lambda n: (n["left"], n["top"], n["right"], n["bot"])
    out = []
    for sysname in sorted({n["system"] for n in nodes if n.get("system")}):
        mem = sorted((n for n in nodes if n.get("system") == sysname), key=lambda n: n["row"])
        clusters = [[mem[0]]]
        for n in mem[1:]:
            if n["row"] - clusters[-1][-1]["row"] > FRAME_GAP_ROWS:
                clusters.append([])
            clusters[-1].append(n)
        for cl in clusters:
            ids = {n["id"] for n in cl}
            others = [rect(n) for n in nodes if n["id"] not in ids]
            for loop in _lasso([rect(n) for n in cl], others, top_limit):
                out.append((sysname, loop))
    return out

def build_page(page, warns):
    title = page["name"]; lanes = list(page["lanes"]); N = len(lanes)
    ptype = page.get("type", "detail")
    lane_ids = [f"lane{i}" for i in range(N)]
    nodes = page["nodes"]; edges = page["edges"]

    if ptype == "overview":
        blocks = [n["spans"] for n in nodes if "spans" in n]
        order = clustered_order(lanes, blocks)
        lanes = [lanes[i] for i in order]
        remap = {old: new for new, old in enumerate(order)}
        for n in nodes:                          # plain lane-numbered nodes follow the reorder
            if "spans" not in n and isinstance(n.get("lane"), int):
                n["lane"] = remap[n["lane"]]

    lane_cx = lambda i: POOL_X + i * LANE_W + LANE_W / 2
    row_cy = lambda r: ROW0 + r * ROWSTEP
    for idx, n in enumerate(nodes):
        n.setdefault("row", idx)
        n["w"], n["h"], n["style"] = KIND[n["kind"]]
        if subline(n):
            n["h"] += SUBLINE_H
        if "spans" in n:                         # overview band: cover its lanes (inset, so
            idxs = sorted(lanes.index(nm) for nm in n["spans"])   # it floats, not pasted on
            if idxs[-1] - idxs[0] + 1 != len(idxs):
                warns.append(f"page '{title}': band '{n['text']}' spans non-adjacent lanes "
                             f"after clustering - it now also covers the lanes between them")
            n["span_lanes"] = idxs
            n["lane"] = idxs[len(idxs) // 2]     # a centre lane drives routing decisions
            n["w"] = (idxs[-1] - idxs[0] + 1) * LANE_W - 2 * BAND_INSET
            n["h"] = BAND_H
            # connectors anchor at the CENTRE LANE, never at the band midpoint: an even
            # span's midpoint sits exactly ON a lane separator, and a vertical arrow
            # dropped there rides the lane border and reads as the border, not an arrow.
            n["cx"] = lane_cx(n["lane"])
        else:
            n["cx"] = lane_cx(n["lane"])
        n["cy"] = row_cy(n["row"])
        if "span_lanes" in n:                   # a band's virtual rect MUST equal the rect it
            n["left"] = POOL_X + n["span_lanes"][0] * LANE_W + BAND_INSET   # emits (cx is an
            n["right"] = n["left"] + n["w"]     # anchor inside it, not its midpoint)
        else:
            n["left"], n["right"] = n["cx"] - n["w"] / 2, n["cx"] + n["w"] / 2
        n["top"], n["bot"] = n["cy"] - n["h"] / 2, n["cy"] + n["h"] / 2
    by_id = {n["id"]: n for n in nodes}
    nrows = max(n["row"] for n in nodes) + 1
    pool_w, pool_h = LANE_W * N, ROW0 + (nrows - 1) * ROWSTEP + 90

    # inbound count -> merge handling
    inbound = {}
    for e in edges:
        inbound.setdefault(e["dst"], []).append(e)

    # ---- forward-edge face occupancy (so a back-edge can pick a FREE face of its target) ----
    used = {n["id"]: set() for n in nodes}               # T/B/L/R faces already taken
    for e in edges:
        s, t = by_id[e["src"]], by_id[e["dst"]]; r = infer_route(s, t)
        if r == "v":   used[s["id"]].add("B"); used[t["id"]].add("T")
        elif r == "L": used[s["id"]].add("R" if t["lane"] > s["lane"] else "L"); used[t["id"]].add("T")
        elif r == "h":
            used[s["id"]].add("R" if t["lane"] > s["lane"] else "L")
            used[t["id"]].add("L" if t["lane"] > s["lane"] else "R")

    # ---- Back-edge channel planning ----
    # Route each back-edge out to a POOL OUTER MARGIN (clear of forward hand-off traffic,
    # which runs between lane centres) on the side of a FREE face of the target. Nest
    # multiple edges in a margin by span (short=inner). Interleaving spans cannot share a
    # channel without crossing and the other margin may carry forward traffic -> the
    # genuinely unavoidable crossing is marked jumpStyle=arc (legible), per routing.md §6.
    up_edges = [e for e in edges if infer_route(by_id[e["src"]], by_id[e["dst"]]) == "up"]
    def rows_of(e):
        s, t = by_id[e["src"]], by_id[e["dst"]]
        return (min(s["row"], t["row"]), max(s["row"], t["row"]))
    def interleave(a, b):
        la, ha = rows_of(a); lb, hb = rows_of(b)
        return la < lb < ha < hb or lb < la < hb < ha
    def back_side(e):                                    # which side of the target the loop enters
        s, t = by_id[e["src"]], by_id[e["dst"]]
        if s["lane"] > t["lane"]:   pref = "R"           # cross-lane: prefer side facing the source
        elif s["lane"] < t["lane"]: pref = "L"
        else:                       pref = "L" if t["lane"] <= (N - 1) / 2 else "R"  # same-lane: nearer edge
        oth = "R" if pref == "L" else "L"
        if pref not in used[t["id"]]: return pref        # ... but only if that face is free
        if oth not in used[t["id"]]: return oth          # else the opposite free side
        return pref
    side = {id(e): back_side(e) for e in up_edges}
    jump = set()
    for i, a in enumerate(up_edges):                     # same-margin interleavers -> jump the later one
        for b in up_edges[i + 1:]:
            if side[id(a)] == side[id(b)] and interleave(a, b):
                jump.add(id(b))
    def back_gutter(e):                                  # track set STAB away from the target face, so
        t = by_id[e["dst"]]; sd = side[id(e)]            #   the entry stab is long enough to read as an arrow
        lo, hi = POOL_X + 4, POOL_X + pool_w - 4         #   (and it sits in the inter-lane gap, off the boxes)
        if sd == "L":
            return min(max(t["left"] - STAB, lo), hi)
        return min(max(t["right"] + STAB, lo), hi)
    track_x = {}
    bygut = {}
    for e in up_edges:
        bygut.setdefault((back_gutter(e), side[id(e)]), []).append(e)
    for (base, sd), grp in bygut.items():
        grp.sort(key=lambda e: rows_of(e)[1] - rows_of(e)[0])   # rank 0 = shortest span
        for rank, e in enumerate(grp):                          # short = innermost (at base, by the node)
            track_x[id(e)] = base + (-rank * TRACK if sd == "L" else rank * TRACK)

    # A back-edge exits the source's TOP and runs straight up (cleaner than a side gutter)
    # when the source's top is free - i.e. its forward in-edge arrived from a side (e.g. a
    # same-row hand-off into a decision) - and the source's own lane is clear up to the
    # target's row. It then enters the target's near side. (Encodes the user's "reject leaves
    # the top of B" rule generally.)
    def lane_clear_above(s, t):
        return not any(n["lane"] == s["lane"] and t["row"] < n["row"] < s["row"] for n in nodes)
    top_exit = {id(e) for e in up_edges
                if "T" not in used[by_id[e["src"]]["id"]]
                and lane_clear_above(by_id[e["src"]], by_id[e["dst"]])}

    # ---- face allocation: every box face hosts AT MOST ONE connector ----
    # A face-centre takes one perpendicular stab. If two edges want the same face (a
    # decision forking to the same side, or two edges merging into one node) they would
    # overlap, so the second is moved to the next free face. >4 connectors on a node can't be
    # placed cleanly -> recorded in `over` and reported (use the free-form LLM path).
    FR = {"T": (0.5, 0.0), "B": (0.5, 1.0), "L": (0.0, 0.5), "R": (1.0, 0.5)}
    OPP = {"L": "R", "R": "L", "T": "B", "B": "T"}
    def fpt(n, f):
        return {"T": (n["cx"], n["top"]), "B": (n["cx"], n["bot"]),
                "L": (n["left"], n["cy"]), "R": (n["right"], n["cy"])}[f]
    def toward(a, b):
        if b["lane"] > a["lane"]: return "R"
        if b["lane"] < a["lane"]: return "L"
        return "B" if b["row"] > a["row"] else "T"
    def nat_faces(e):
        s, t = by_id[e["src"]], by_id[e["dst"]]; r = infer_route(s, t)
        if r == "v":    return "B", "T"
        if r == "L":    return ("R" if t["lane"] > s["lane"] else "L"), "T"
        if r == "h":    return ("R" if t["lane"] > s["lane"] else "L"), ("L" if t["lane"] > s["lane"] else "R")
        if r == "self": return "R", "T"
        if id(e) in top_exit:                                  # up via source top, enter target near side
            return "T", toward(t, s)
        gx = track_x[id(e)]                                    # up via side gutter
        return ("L" if gx <= s["cx"] else "R"), ("L" if gx <= t["cx"] else "R")
    occ = {n["id"]: {} for n in nodes}
    over, facemap = [], {}
    PRI = {"v": 0, "up": 1, "L": 2, "h": 2, "self": 3}
    def claim(node, want, prefs):
        o = occ[node["id"]]
        for f in [want] + [p for p in prefs if p != want]:
            if f not in o:
                o[f] = True; return f
        over.append(node["text"][:24]); return want
    def _ord(e):                                           # straighter (shorter lane jump) claims faces first
        s, t = by_id[e["src"]], by_id[e["dst"]]
        return (PRI[infer_route(s, t)], abs(s["lane"] - t["lane"]))
    for e in sorted(edges, key=_ord):
        s, t = by_id[e["src"]], by_id[e["dst"]]; ef0, nf0 = nat_faces(e)
        ef = claim(s, ef0, ["B", toward(s, t), OPP[ef0], "T"])
        nf = claim(t, nf0, [toward(t, s), "B", OPP[nf0], "T"])
        facemap[id(e)] = (ef, nf)
    def fwd_wp(s, t, ef, nf):
        sx, sy = fpt(s, ef); tx, ty = fpt(t, nf)
        he, hn = ef in ("L", "R"), nf in ("L", "R")
        if not he and not hn:                                  # vertical out, vertical in
            if abs(sx - tx) < 1: return []
            my = (sy + ty) / 2; return [(sx, my), (tx, my)]
        if he and not hn:  return [(tx, sy)]                   # side out -> top/bottom in
        if not he and hn:  return [(sx, ty)]                   # top/bottom out -> side in
        if abs(sy - ty) < 1: return [((sx + tx) / 2, sy)]      # side -> side, same row
        mx = (sx + tx) / 2; return [(mx, sy), (mx, ty)]        # side -> side, offset

    # NOTE: <diagram> is flush-left on purpose - the lifecycle guard hashes the exact
    # substring a regex can re-capture, and leading indentation would break the match.
    out = [f'<diagram name="{esc(title)}">',
           '    <mxGraphModel dx="800" dy="600" grid="1" gridSize="10" guides="1" tooltips="1" '
           'connect="1" arrows="1" fold="1" page="0" pageScale="1" pageWidth="1169" pageHeight="827" '
           'math="0" shadow="0">', '      <root>', '        <mxCell id="0"/>',
           '        <mxCell id="1" parent="0"/>']
    out.append(f'        <mxCell id="title" value="{esc(title)}" style="text;html=1;strokeColor=none;'
               'fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;fontSize=16;fontStyle=1;" '
               f'vertex="1" parent="1"><mxGeometry x="{POOL_X}" y="20" width="{pool_w}" height="30" as="geometry"/></mxCell>')
    # frames go BEFORE the pool so lanes (unfilled) and boxes (white) draw on top of them
    for fi, (sysname, loop) in enumerate(system_frames(nodes, POOL_Y + 30 + 2)):
        (sx, sy), rest = loop[0], loop[1:]
        pts = "".join(f'<mxPoint x="{x:g}" y="{y:g}"/>' for x, y in rest)
        out.append(f'        <mxCell id="frame-{fi}" value="{esc(sysname)}" style="{FRAME_STYLE}" '
                   f'edge="1" parent="1"><mxGeometry x="-1" relative="1" as="geometry">'
                   f'<mxPoint x="{sx:g}" y="{sy:g}" as="sourcePoint"/>'
                   f'<mxPoint x="{sx:g}" y="{sy:g}" as="targetPoint"/>'
                   f'<Array as="points">{pts}</Array><mxPoint x="6" y="-2" as="offset"/>'
                   f'</mxGeometry></mxCell>')
    out.append(f'        <mxCell id="pool" value="" style="swimlane;startSize=0;horizontal=0;fillColor=none;'
               'strokeColor=#000000;container=1;collapsible=0;" vertex="1" parent="1">'
               f'<mxGeometry x="{POOL_X}" y="{POOL_Y}" width="{pool_w}" height="{pool_h}" as="geometry"/></mxCell>')
    for i, (nm, lid) in enumerate(zip(lanes, lane_ids)):
        out.append(f'        <mxCell id="{lid}" value="{esc(nm)}" style="swimlane;html=1;startSize=30;'
                   'horizontal=1;fillColor=none;strokeColor=#000000;" vertex="1" parent="pool">'
                   f'<mxGeometry x="{i*LANE_W}" y="0" width="{LANE_W}" height="{pool_h}" as="geometry"/></mxCell>')
    for n in nodes:
        w, h = n["w"], n["h"]
        if "span_lanes" in n:                     # overview band: pool child, inset from the
            bx = n["span_lanes"][0] * LANE_W + BAND_INSET; by = n["cy"] - POOL_Y - h / 2
            out.append(f'        <mxCell id="{n["id"]}" value="{esc(label_html(n))}" style="{n["style"]}" '
                       f'vertex="1" parent="pool"><mxGeometry x="{bx:g}" y="{by:g}" '
                       f'width="{w:g}" height="{h}" as="geometry"/></mxCell>')
        else:
            lx = (LANE_W - w) / 2; ly = n["cy"] - POOL_Y - h / 2
            out.append(f'        <mxCell id="{n["id"]}" value="{esc(label_html(n))}" style="{n["style"]}" '
                       f'vertex="1" parent="{lane_ids[n["lane"]]}"><mxGeometry x="{lx:g}" y="{ly:g}" '
                       f'width="{w}" height="{h}" as="geometry"/></mxCell>')

    for k, e in enumerate(edges):
        s, t = by_id[e["src"]], by_id[e["dst"]]
        route = infer_route(s, t); label = esc(e.get("label", "")); extra = ""
        ef, nf = facemap[id(e)]
        if route == "up":
            if ef == "T":                                   # straight up the source centre, into target side
                wp = [(s["cx"], t["cy"])]
            else:                                           # up a side gutter
                gx = track_x[id(e)]; wp = [(gx, s["cy"]), (gx, t["cy"])]
            if id(e) in jump:
                extra = "jumpStyle=arc;"
        elif route == "self":
            gx = s["right"] + 0.4 * s["w"]; gy = s["top"] - ROWSTEP / 3
            ef, nf = "R", "T"
            wp = [(gx, s["cy"]), (gx, gy), (s["cx"], gy)]
        else:
            wp = fwd_wp(s, t, ef, nf)
        # port fractions derive from the ACTUAL anchor point: identical to the fixed
        # centre fractions (0.5/0/1) for ordinary boxes, but fractional for a wide band
        # whose connector anchors at a lane centre off the band midpoint (the gate checks
        # the stab against exactly these fractions, so they must match the waypoints).
        def frac(node, f):
            if f in ("T", "B"):
                return ((node["cx"] - node["left"]) / node["w"], 0.0 if f == "T" else 1.0)
            return (0.0 if f == "L" else 1.0, (node["cy"] - node["top"]) / node["h"])
        (ex, ey), (ix, iy) = frac(s, ef), frac(t, nf)
        pts = "".join(f'<mxPoint x="{x:g}" y="{y:g}"/>' for x, y in wp)
        arr = f'<Array as="points">{pts}</Array>' if pts else ''
        # a branch label rides NEAR ITS SOURCE (the decision), not mid-edge (user taste)
        lx = f' x="{LBL_X}"' if label else ""
        # ports MUST live in the style string (draw.io + check_layout.py read them there,
        # NOT as mxCell attributes) — otherwise the gate can't trace the face stabs.
        port = (f"exitX={ex};exitY={ey};exitDx=0;exitDy=0;"
                f"entryX={ix};entryY={iy};entryDx=0;entryDy=0;")
        out.append(f'        <mxCell id="edge-{k}" value="{label}" style="{EDGE}{port}{extra}" edge="1" '
                   f'source="{e["src"]}" target="{e["dst"]}" parent="1">'
                   f'<mxGeometry{lx} relative="1" as="geometry">{arr}</mxGeometry></mxCell>')
    out += ['      </root>', '    </mxGraphModel>', '</diagram>']
    if over:
        warns.append("over-envelope (use free-form LLM path) at nodes: " + ", ".join(sorted(set(over))))
    return "\n".join(out)

# ---------------------------------------------------------------- spec lint ----

def lint_spec(spec):
    """Structural binding errors (fatal) + taste defaults (warnings), from real usage:
    one merged End per fate, a branch label on every decision out-edge, terse labels,
    and the overview<->detail binding rules."""
    errs, warns = [], []
    pages = get_pages(spec)
    verbs = spec.get("verbs") or []
    tbd = [0]
    systems = {n["system"] for p in pages for n in p["nodes"] if n.get("system")}
    for p in pages:
        for ln in p["lanes"]:
            if ln in systems:
                errs.append(f"page '{p['name']}': lane '{ln}' is a system name - lanes are humans "
                            f"who act; a system is a dashed frame around the boxes done in it")
    pnames = [p["name"] for p in pages]
    if len(set(pnames)) != len(pnames):
        errs.append(f"duplicate page names {pnames} - each page name must be unique")
    by_name = {p["name"]: p for p in pages}
    exp = {}                                        # detail page -> [overview page that bands it]
    for p in pages:
        name, ptype = p["name"], p.get("type", "detail")
        nodes = p["nodes"]; by_id = {n["id"]: n for n in nodes}

        ends = [n for n in nodes if n["kind"] == "end"]
        fates = {}
        for n in ends:
            fates.setdefault((n.get("text") or "End").strip(), []).append(n)
        for fate, ns in fates.items():
            if len(ns) > 1:
                warns.append(f"page '{name}': {len(ns)} End nodes labelled '{fate}' - merge "
                             f"same-fate paths into ONE End (multiple Ends only for genuinely "
                             f"distinct fates, each labelled differently)")

        for e in p["edges"]:
            s, t = by_id.get(e["src"]), by_id.get(e["dst"])
            if s and s["kind"] == "decision" and not (e.get("label") or "").strip():
                warns.append(f"page '{name}': edge '{s['text']}' -> "
                             f"'{(t or {}).get('text', e['dst'])}' leaves a decision with NO "
                             f"branch label (ได้/ไม่ได้, ใช่/ไม่ใช่, Yes/No...)")

        def terse(txt, where):
            if "(" in txt:
                warns.append(f"page '{name}': {where} '{txt}' carries a (parenthesis) annotation - "
                             f"put annotations in a note, keep the label terse")
            if "&" in txt or "+" in txt:
                warns.append(f"page '{name}': {where} '{txt}' joins actions with '&'/'+' - one box "
                             f"= one action: split it (write 'และ' only if truly inseparable)")
            if re.match(r"\s*(\[TBD\]\s*)?\d+\s*[\.\)\-]", txt):
                warns.append(f"page '{name}': {where} '{txt}' starts with a step number - never "
                             f"type numbers; the renderer numbers boxes from their ids")
        for n in nodes:
            txt = n.get("text", "")
            terse(txt, f"node '{n['id']}'")
            if n["kind"] not in KIND:
                errs.append(f"page '{name}': node '{n['id']}' kind '{n['kind']}' is outside the "
                            f"BPMN-lite budget {sorted(KIND)} - an output/store is a task "
                            f"(or text like '→ สัญญา PDF'), a document only for a real hand-off")
            if n.get("system") and n.get("outside"):
                errs.append(f"page '{name}': node '{n['id']}' has both system "
                            f"'{n['system']}' and outside '{n['outside']}' - a box is done in one "
                            f"place: inside a system frame OR out of system, not both")
            if n.get("type") is not None and n["type"] not in TYPES:
                errs.append(f"page '{name}': node '{n['id']}' type '{n['type']}' not in {TYPES}")
            if "[TBD]" in txt:
                tbd[0] += 1
            if n["kind"] == "process":
                act = txt.replace("[TBD]", "").strip()
                if "และ" in act:
                    warns.append(f"page '{name}': node '{n['id']}' '{txt}' has 'และ' - one box = "
                                 f"one action (verb + object); split it unless inseparable")
                if verbs and not any(act.startswith(v) for v in verbs):
                    warns.append(f"page '{name}': node '{n['id']}' '{txt}' does not start with a "
                                 f"verb from the spec's verb list {verbs}")
            if ptype == "overview":
                if "spans" in n and n["kind"] != "subprocess":
                    warns.append(f"page '{name}': node '{n['text']}' spans lanes but isn't a "
                                 f"subprocess - only a sub-process band spans lanes on an overview")
                if "spans" not in n and n["kind"] == "subprocess":
                    warns.append(f"page '{name}': subprocess '{n['text']}' has no 'spans' - on an "
                                 f"overview a sub-process is a band over the lanes it involves")
        for e in p["edges"]:
            lbl = e.get("label", "")
            terse(lbl, "edge label")
            if lbl and (" - " in lbl or len(lbl) > 16):
                warns.append(f"page '{name}': edge label '{lbl}' is long - a branch label is the "
                             f"word pair only (ได้/ไม่ได้, Yes/No, ครบ/ไม่ครบ); where the arrow "
                             f"LANDS already says what happens next")

        for n in nodes:
            tgt = n.get("expands_to")
            if not tgt:
                continue
            if tgt not in by_name:
                errs.append(f"page '{name}': '{n['text']}' expands_to '{tgt}' but no page has "
                            f"that name")
                continue
            if n.get("text") != tgt:
                errs.append(f"page '{name}': band text '{n['text']}' != detail page name "
                            f"'{tgt}' - a reader navigates by exact name match")
            exp.setdefault(tgt, []).append(name)
            detail = by_name[tgt]
            outside = set(detail["lanes"]) - set(n["spans"])
            if outside:
                warns.append(f"page '{name}': detail page '{tgt}' has lanes {sorted(outside)} "
                             f"outside its band's span - the band should cover everyone involved")
    for tgt, srcs in exp.items():
        if len(srcs) > 1:
            errs.append(f"detail page '{tgt}' is expanded by {len(srcs)} bands {srcs} - "
                        f"1 sub-process : 1 detail page")
    if tbd[0]:
        warns.append(f"{tbd[0]} box(es) still [TBD]")
    return errs, warns

# ------------------------------------------------------- hand-edit lifecycle ----

def _hash(s):
    return hashlib.sha256(s.encode()).hexdigest()[:16]

def first_hand_edited_page(path):
    """None if every existing page is byte-identical to what this generator last wrote
    (its embedded genhash still matches); else the first page name that changed. Once a
    hand edit is detected the .drawio - not the spec - is the source of truth."""
    text = open(path, encoding="utf-8").read()
    for m in re.finditer(r"<diagram\b[^>]*>.*?</diagram>", text, re.S):
        block = m.group(0)
        attrs = block.split(">", 1)[0]
        hm = re.search(r'genhash="([^"]+)"', attrs)
        nm = re.search(r'name="([^"]*)"', attrs)
        name = _html.unescape(nm.group(1)) if nm else "?"
        if not hm:
            return name                            # not generator-owned (hand-built / old gen)
        stripped = block.replace(f' genhash="{hm.group(1)}"', "", 1)
        if _hash(stripped) != hm.group(1):
            return name                            # edited since it was generated
    return None

def build_document(spec):
    warns = []
    pages = []
    for p in get_pages(spec):
        block = build_page(p, warns)               # hash covers exactly what we emitted
        h = _hash(block)
        pages.append(block.replace('<diagram ', f'<diagram genhash="{h}" ', 1))
    doc = ['<?xml version="1.0" encoding="UTF-8"?>', '<mxfile host="app.diagrams.net">']
    doc += pages + ['</mxfile>']
    return "\n".join(doc), warns

# --------------------------------------------------------------- read-back ----
# Two-way editing: the .drawio owns the visuals (text, kind, lane, system frame, edges,
# position); the spec owns the non-visual data keyed by box id (page, changes, errors...).
# After a hand edit, `--read` pulls the visuals back into the spec and reports the diff.
# The geometry parser is check_layout's, so the gate and the read-back see the same thing.
VISUAL = ("text", "kind", "lane", "spans", "system", "outside", "row")

def _plain(value):
    """drawio html label -> (main text, sub-line or '')."""
    v = re.sub(r"<br\s*/?>|</div>|</p>", "\n", value or "", flags=re.I)
    lines = [ln.replace("\xa0", " ").strip()
             for ln in _html.unescape(re.sub(r"<[^>]+>", "", v)).split("\n")]
    lines = [ln for ln in lines if ln]
    if len(lines) > 1 and (lines[-1].startswith("นอกระบบ") or lines[-1] == "ระบบทำเอง"):
        return " ".join(lines[:-1]), lines[-1]
    return " ".join(lines), ""

def _kind(st):
    if "ellipse" in st:
        return "end" if str(st.get("strokeWidth")) == "3" else "start"
    if "rhombus" in st:
        return "decision"
    if st.get("isLoopSub") == "1" or st.get("shape") == "process":
        return "subprocess"
    if st.get("shape") == "document":
        return "document"
    return "process"

def read_page(root, page):
    """Visuals of one drawio page -> (new nodes, new edges, lane names); spec page untouched."""
    import check_layout as cl
    cells = {}
    for el in root.iter("mxCell"):
        c = cl.Cell(el)
        if c.id is not None:
            cells[c.id] = c
    cl.mark_wired(cells)
    lanes = sorted((c for c in cells.values() if c.is_vertex and c.is_lane() and c.value),
                   key=lambda c: cl.node_box(c, cells)[0])
    lane_box = [(_plain(c.value)[0], cl.node_box(c, cells)) for c in lanes]
    frames = [(_plain(f.value)[0], cl.frame_polygon(f, cells)) for f in cells.values() if f.is_frame()]
    boxes = [c for c in cells.values()
             if c.is_vertex and not c.is_lane() and not c.is_text() and not c.is_frame()
             and c.w is not None and not (cells.get(c.parent) and cells[c.parent].is_edge)]
    # spec lane order is kept (an overview re-clusters at generate time anyway)
    names = list(page["lanes"]) + [n for n, _ in lane_box if n not in page["lanes"]]
    old = {n["id"]: n for n in page["nodes"]}
    nodes, warns = [], []
    for c in boxes:
        x0, y0, x1, y1 = cl.node_box(c, cells)
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        text, sub = _plain(c.value)
        n = {"id": c.id, "text": text, "kind": _kind(c.style)}
        n["_y"], n["_x"] = cy, cx
        n["row"] = round((cy - ROW0) / ROWSTEP)
        over = [nm for nm, (a, _, b, _) in lane_box if min(x1, b) - max(x0, a) > 1]
        if "spans" in old.get(c.id, {}) or len(over) > 1:
            n["spans"] = over
        else:
            inl = [nm for nm, (a, t, b, u) in lane_box if a <= cx < b and t <= cy < u]
            if inl:
                n["lane"] = names.index(inl[0])
        if sub.startswith("นอกระบบ"):
            n["outside"] = sub.split("·", 1)[-1].strip()
        if sub == "ระบบทำเอง":
            n["type"] = "service"
        ins, part = [], []
        for nm, poly in frames:
            r = cl.box_vs_polygon((x0, y0, x1, y1), poly)
            (ins if r == "in" else part if r == "partial" else []).append(nm)
        if len(ins) == 1 and not part:
            n["system"] = ins[0]
        elif ins or part:
            warns.append(f"box '{c.id}' sits in frames {ins} / straddles {part} - "
                         f"system left unchanged (run check_layout.py)")
            if old.get(c.id, {}).get("system"):
                n["system"] = old[c.id]["system"]
        o = old.get(c.id, {})                   # keep the spec's key order and its non-visual data
        merged = {k: n.pop(k) if k in n else v for k, v in o.items() if k in n or k not in VISUAL}
        merged.update(n)
        if merged.get("type") == "service" and sub != "ระบบทำเอง":
            del merged["type"]                  # the "ระบบทำเอง" sub-line was removed by hand
        nodes.append(merged)
    nodes.sort(key=lambda n: (n["_y"], n["_x"]))
    for i, n in enumerate(nodes):
        del n["_y"], n["_x"]
        if n["row"] == i:
            del n["row"]                        # implicit row = list index
    edges = []
    for e in cells.values():
        if e.is_edge and not e.is_frame() and e.source and e.target:
            ed = {"src": e.source, "dst": e.target}
            lbl = _plain(e.value)[0]
            if lbl:
                ed["label"] = lbl
            edges.append(ed)
    return nodes, edges, names, warns

def _rows(nodes):
    return {n["id"]: n.get("row", i) for i, n in enumerate(nodes)}

def diff_page(page, nodes, edges, names):
    """Human report lines: what the drawio changed versus the spec."""
    rep = []
    lanes_old = page["lanes"]
    for nm in names[len(lanes_old):]:
        rep.append(f"lane '{nm}' is new in the drawio (renamed or added)")
    def lname(n):
        if "spans" in n:
            return n["spans"]
        return names[n["lane"]] if isinstance(n.get("lane"), int) else None
    old = {n["id"]: n for n in page["nodes"]}
    ro, rn = _rows(page["nodes"]), _rows(nodes)
    seen_lanes = {names[n["lane"]] for n in nodes if "lane" in n} | {s for n in nodes for s in n.get("spans", [])}
    for nm in lanes_old:
        if nm not in seen_lanes and any(lname(n) == nm for n in page["nodes"]):
            rep.append(f"lane '{nm}' has no boxes in the drawio (renamed or removed?)")
    for n in nodes:
        o = old.get(n["id"])
        if o is None:
            rep.append(f"new box {n['id']} '{n['text']}' - give it a permanent id")
            continue
        ch = []
        if "[TBD]" in o.get("text", "") and "[TBD]" not in n["text"]:
            ch.append("[TBD] removed")
            if o["text"].replace("[TBD]", "").strip() != n["text"]:
                ch.append(f"text -> '{n['text']}'")
        elif o.get("text", "") != n["text"]:
            ch.append(f"text '{o.get('text', '')}' -> '{n['text']}'")
        if o["kind"] != n["kind"]:
            ch.append(f"kind {o['kind']} -> {n['kind']}")
        if lname(o) != lname(n):
            ch.append(f"lane {lname(o)} -> {lname(n)}")
        for k in ("system", "outside"):
            if o.get(k) != n.get(k):
                ch.append(f"{k} {o.get(k) or 'none'} -> {n.get(k) or 'none'}")
        if (o.get("type") == "service") != (n.get("type") == "service"):
            ch.append("ระบบทำเอง " + ("added" if n.get("type") == "service" else "removed"))
        if ro[n["id"]] != rn[n["id"]]:
            ch.append(f"row {ro[n['id']]} -> {rn[n['id']]}")
        if ch:
            rep.append(f"{n['id']} '{n['text']}': " + " · ".join(ch))
    ids = {n["id"] for n in nodes}
    for o in page["nodes"]:
        if o["id"] not in ids:
            rep.append(f"box {o['id']} '{o.get('text', '')}' is gone from the drawio - kept under 'removed'")
    key = lambda e: (e["src"], e["dst"])
    oe = {key(e): e.get("label", "") for e in page["edges"]}
    ne = {key(e): e.get("label", "") for e in edges}
    for k in ne.keys() - oe.keys():
        rep.append(f"edge {k[0]} -> {k[1]} added" + (f" '{ne[k]}'" if ne[k] else ""))
    for k in oe.keys() - ne.keys():
        rep.append(f"edge {k[0]} -> {k[1]} removed")
    for k in oe.keys() & ne.keys():
        if oe[k] != ne[k]:
            rep.append(f"edge {k[0]} -> {k[1]} label '{oe[k]}' -> '{ne[k]}'")
    return rep

def _dump(o, ind=0):
    """Compact-where-short JSON, matching the hand-written spec style."""
    flat = json.dumps(o, ensure_ascii=False)
    if not isinstance(o, (dict, list)) or len(flat) + ind <= 140:
        return flat
    pad = " " * (ind + 2)
    if isinstance(o, dict):
        body = ",\n".join(f"{pad}{json.dumps(k, ensure_ascii=False)}: {_dump(v, ind + 2)}"
                          for k, v in o.items())
        return "{\n" + body + "\n" + " " * ind + "}"
    return "[\n" + ",\n".join(pad + _dump(v, ind + 2) for v in o) + "\n" + " " * ind + "]"

def read_back(drawio_path, spec_path):
    import xml.etree.ElementTree as ET
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import check_layout as cl
    spec = json.load(open(spec_path, encoding="utf-8"))
    pages = get_pages(spec)
    dgs = {(d.get("name") or ""): d for d in ET.parse(drawio_path).getroot().iter("diagram")}
    if set(dgs) != {p["name"] for p in pages}:
        sys.exit(f"FAIL: page names differ - drawio {sorted(dgs)} vs spec {sorted(p['name'] for p in pages)}. "
                 f"Rename the page in one of them so they match, then --read again.")
    changed = False
    for p in pages:
        nodes, edges, names, warns = read_page(cl.diagram_root(dgs[p["name"]]), p)
        rep = diff_page(p, nodes, edges, names)
        print(f"=== {p['name']} ===")
        for w in warns:
            print("WARN " + w)
        print("\n".join(rep) if rep else "no changes")
        changed |= bool(rep)
        ids = {n["id"] for n in nodes}
        gone = [o for o in p["nodes"] if o["id"] not in ids]
        home = p if "pages" in spec else spec   # the flat form keeps its fields at top level
        if gone:
            home["removed"] = home.get("removed", []) + gone
        home.update(lanes=names, nodes=nodes, edges=edges)
        p["nodes"] = nodes
    tbd = sum("[TBD]" in n.get("text", "") for p in pages for n in p["nodes"])
    print(f"{tbd} box(es) still [TBD]")
    if changed:
        open(spec_path, "w", encoding="utf-8").write(_dump(spec) + "\n")
        print("updated", spec_path)

if __name__ == "__main__":
    if sys.argv[1] == "--read":
        read_back(sys.argv[2], sys.argv[3])
        sys.exit(0)
    spec = json.load(open(sys.argv[1]))
    errs, warns = lint_spec(spec)
    for w in warns:
        print("WARN " + w)
    if errs:
        for e in errs:
            print("FAIL " + e)
        sys.exit(1)
    out_path = sys.argv[2]
    if os.path.exists(out_path):
        touched = first_hand_edited_page(out_path)
        if touched is not None:
            sys.exit(f"REFUSE: page '{touched}' in {out_path} was hand-edited (or wasn't "
                     f"generated by this script). Never overwrite a hand edit: read it back with "
                     f"`--read {out_path} <spec.json>`, and make further changes in the drawio XML.")
    xml, warns2 = build_document(spec)
    for w in warns2:
        print("WARN " + w)
    open(out_path, "w").write(xml)
    print("wrote", out_path)
