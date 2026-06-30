#!/usr/bin/env python3
"""Deterministic draw.io vertical-swimlane generator.

The model writes a tiny JSON spec (lanes + nodes + edges as pure topology); this engine
computes ALL geometry/ports/waypoints so the output passes scripts/check_layout.py by
construction. No model tokens are spent on XML, and no full XML is ever emitted by the
model -> the 32k-output spawn crash cannot occur.

Routing rules are the NotebookLM synthesis of ELK / yFiles / yEd channel-router / Sugiyama
+ our own routing.md / priority-rules.md (see references/routing.md).

Spec JSON:
{
  "title": "F1 - ...",
  "lanes": ["Candidate", "Recruiter", ...],          # columns, left to right
  "nodes": [{"id":"n1","lane":0,"kind":"process","text":"...", "row":0?}],  # row optional (defaults to list order)
  "edges": [{"src":"n1","dst":"n2","label":"Yes"?}]   # route is INFERRED from geometry
}
kinds: start end process decision output document store subprocess
Usage: python3 gen_swimlane.py spec.json out.drawio
"""
import json, sys

LANE_W = 195
POOL_X, POOL_Y = 56, 60
ROW0, ROWSTEP = 120, 90
GUT = 12          # how far inside a lane-boundary/pool-margin a back-edge track sits
TRACK = 14        # spacing between nested back-edge tracks (Left-Edge)
STAB = 16         # min straight stab from the gutter into the target face (so the arrow reads)

# kind -> (w, h, style)  — skill standard: NO decorative colour (white fill, black stroke)
KIND = {
    "start":      (120, 40, "ellipse;whiteSpace=wrap;html=1;"),
    "end":        (120, 40, "ellipse;whiteSpace=wrap;html=1;"),
    "process":    (150, 50, "rounded=0;whiteSpace=wrap;html=1;"),
    "decision":   (140, 80, "rhombus;whiteSpace=wrap;html=1;"),
    "output":     (150, 50, "shape=parallelogram;perimeter=parallelogramPerimeter;whiteSpace=wrap;html=1;"),
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

def build(spec):
    title = spec["title"]; lanes = spec["lanes"]; N = len(lanes)
    lane_ids = [f"lane{i}" for i in range(N)]
    nodes = spec["nodes"]; edges = spec["edges"]
    lane_cx = lambda i: POOL_X + i * LANE_W + LANE_W / 2
    row_cy = lambda r: ROW0 + r * ROWSTEP
    for idx, n in enumerate(nodes):
        n.setdefault("row", idx)
        n["w"], n["h"], n["style"] = KIND[n["kind"]]
        n["cx"], n["cy"] = lane_cx(n["lane"]), row_cy(n["row"])
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
    # overlap, so the second is moved to the next free face. >4 connectors on a node can't
    # be placed cleanly -> recorded in `over` and reported (use the free-form LLM path).
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

    out = ['<?xml version="1.0" encoding="UTF-8"?>', '<mxfile host="app.diagrams.net">',
           f'  <diagram name="{esc(title)}">',
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
        w, h = n["w"], n["h"]; lx = (LANE_W - w) / 2; ly = n["cy"] - POOL_Y - h / 2
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
        (ex, ey), (ix, iy) = FR[ef], FR[nf]
        pts = "".join(f'<mxPoint x="{x:g}" y="{y:g}"/>' for x, y in wp)
        arr = f'<Array as="points">{pts}</Array>' if pts else ''
        # ports MUST live in the style string (draw.io + check_layout.py read them there,
        # NOT as mxCell attributes) — otherwise the gate can't trace the face stabs.
        port = (f"exitX={ex};exitY={ey};exitDx=0;exitDy=0;"
                f"entryX={ix};entryY={iy};entryDx=0;entryDy=0;")
        out.append(f'        <mxCell id="e{k}" value="{label}" style="{EDGE}{port}{extra}" edge="1" '
                   f'source="{e["src"]}" target="{e["dst"]}" parent="1">'
                   f'<mxGeometry relative="1" as="geometry">{arr}</mxGeometry></mxCell>')
    out += ['      </root>', '    </mxGraphModel>', '  </diagram>', '</mxfile>']
    if over:
        sys.stderr.write("WARN over-envelope (use free-form LLM path) at nodes: "
                         + ", ".join(sorted(set(over))) + "\n")
    return "\n".join(out)

if __name__ == "__main__":
    spec = json.load(open(sys.argv[1]))
    open(sys.argv[2], "w").write(build(spec))
    print("wrote", sys.argv[2])
