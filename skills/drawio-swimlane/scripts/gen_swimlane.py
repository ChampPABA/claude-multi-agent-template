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

kinds: start end process decision output document store subprocess
Usage: python3 gen_swimlane.py spec.json out.drawio
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

# kind -> (w, h, style)  — skill standard: NO decorative colour (white fill, black stroke)
KIND = {
    "start":      (120, 40, "ellipse;whiteSpace=wrap;html=1;"),
    "end":        (120, 40, "ellipse;whiteSpace=wrap;html=1;"),
    "process":    (150, 50, "rounded=0;whiteSpace=wrap;html=1;"),
    "decision":   (140, 80, "rhombus;whiteSpace=wrap;html=1;"),
    "output":     (150, 60, "shape=parallelogram;perimeter=parallelogramPerimeter;size=0.1;whiteSpace=wrap;html=1;"),
    "document":   (150, 60, "shape=document;whiteSpace=wrap;html=1;"),
    "store":      (130, 60, "shape=cylinder;whiteSpace=wrap;html=1;"),
    "subprocess": (150, 50, "shape=process;whiteSpace=wrap;html=1;"),
}
EDGE = ("edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;"
        "html=1;endArrow=block;endFill=1;")

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
            out.append(f'        <mxCell id="{n["id"]}" value="{esc(n["text"])}" style="{n["style"]}" '
                       f'vertex="1" parent="pool"><mxGeometry x="{bx:g}" y="{by:g}" '
                       f'width="{w:g}" height="{h}" as="geometry"/></mxCell>')
        else:
            lx = (LANE_W - w) / 2; ly = n["cy"] - POOL_Y - h / 2
            out.append(f'        <mxCell id="{n["id"]}" value="{esc(n["text"])}" style="{n["style"]}" '
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
        out.append(f'        <mxCell id="e{k}" value="{label}" style="{EDGE}{port}{extra}" edge="1" '
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
            if "+" in txt:
                warns.append(f"page '{name}': {where} '{txt}' uses '+' - write '&' instead")
            if ptype == "overview" and re.match(r"\s*\d+\s*[\.\)\-]", txt):
                warns.append(f"page '{name}': {where} '{txt}' starts with a sequence/funnel number - "
                             f"an overview page carries block names, not step numbers")
        for n in nodes:
            terse(n.get("text", ""), f"node '{n['id']}'")
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

if __name__ == "__main__":
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
                     f"generated by this script). The .drawio is now the source of truth: "
                     f"edit its XML directly, or delete/rename the file to regenerate.")
    xml, warns2 = build_document(spec)
    for w in warns2:
        print("WARN " + w)
    open(out_path, "w").write(xml)
    print("wrote", out_path)
