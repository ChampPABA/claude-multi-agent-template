#!/usr/bin/env python3
"""Deterministic layout gate for draw.io swimlane flowcharts.

The eyeball verify-loop keeps intermittently missing ONE failure mode: a
return/loop connector that routes *above the topmost node* or through the
lane-header band - the "over-the-top" back-edge. It looks like it "crosses
nothing" (no box is in the empty header strip), so the model talks itself into
it. This script turns that judgement call into a hard gate.

It resolves lane-relative child geometry to absolute page coords (a node that is
a child of a lane has its y measured from the lane's top, NOT the page), then
flags any edge waypoint that sits in the header band or above every node.

Usage:
    python check_layout.py flow.drawio            # all pages
    python check_layout.py flow.drawio --page 2   # 1-based page

Exit code 1 if any HARD violation (over-the-top / header-band) is found, else 0.
P8 same-side and decision-vertex notes are ADVISORY (never fail the build).
"""
import sys
import argparse
import xml.etree.ElementTree as ET

TOL = 2.0  # px slack for floating-point / grid noise


def parse_style(style):
    d = {}
    for part in (style or "").split(";"):
        if not part:
            continue
        if "=" in part:
            k, v = part.split("=", 1)
            d[k] = v
        else:
            d[part] = True
    return d


def fnum(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


class Cell:
    def __init__(self, el):
        self.id = el.get("id")
        self.value = el.get("value") or ""
        self.style = parse_style(el.get("style"))
        self.parent = el.get("parent")
        self.source = el.get("source")
        self.target = el.get("target")
        self.is_vertex = el.get("vertex") == "1"
        self.is_edge = el.get("edge") == "1"
        self.x = self.y = self.w = self.h = None
        self.points = []  # explicit edge waypoints
        geo = el.find("mxGeometry")
        if geo is not None:
            self.x, self.y = fnum(geo.get("x")), fnum(geo.get("y"))
            self.w, self.h = fnum(geo.get("width")), fnum(geo.get("height"))
            arr = geo.find("Array[@as='points']")
            if arr is not None:
                for p in arr.findall("mxPoint"):
                    px, py = fnum(p.get("x")), fnum(p.get("y"))
                    if px is not None and py is not None:
                        self.points.append((px, py))

    def is_lane(self):
        return "swimlane" in self.style or "pool" in self.style

    def is_text(self):
        return self.style.get("text") is True or "text" in self.style


def abs_origin(cell, cells):
    """Sum x/y of every vertex ancestor (lane/pool/group) -> page-absolute origin."""
    ox = oy = 0.0
    seen = set()
    p = cells.get(cell.parent)
    while p is not None and p.is_vertex and p.x is not None and p.id not in seen:
        seen.add(p.id)
        ox += p.x
        oy += p.y
        p = cells.get(p.parent)
    return ox, oy


def check_page(root, page_name):
    cells = {}
    for el in root.iter("mxCell"):
        c = Cell(el)
        if c.id is not None:
            cells[c.id] = c

    lanes = [c for c in cells.values() if c.is_vertex and c.is_lane() and c.y is not None]
    nodes = [
        c for c in cells.values()
        if c.is_vertex and not c.is_lane() and not c.is_text() and c.h is not None
    ]
    edges = [c for c in cells.values() if c.is_edge]

    hard, advisory = [], []
    if not nodes:
        return hard, advisory  # nothing to check (e.g. overview-only page)

    # absolute top-Y of every flow node, and the topmost one
    node_tops = []
    for n in nodes:
        _, oy = abs_origin(n, cells)
        node_tops.append(oy + n.y)
    topmost = min(node_tops)

    # lane-header band: header occupies [lane_top, lane_top + startSize]
    body_top = None
    for ln in lanes:
        _, oy = abs_origin(ln, cells)
        start = fnum(ln.style.get("startSize")) or 30.0
        bt = oy + ln.y + start
        body_top = bt if body_top is None else min(body_top, bt)

    # HARD: any edge waypoint above the topmost node or inside the header band
    for e in edges:
        label = e.value or e.id or "<edge>"
        for (px, py) in e.points:
            if py < topmost - TOL:
                hard.append(
                    f"edge '{label}': waypoint y={py:g} is ABOVE the topmost node "
                    f"(top={topmost:g}) - over-the-top back-edge. Route it down/around "
                    f"inside the pool body instead."
                )
            elif body_top is not None and py < body_top - TOL:
                hard.append(
                    f"edge '{label}': waypoint y={py:g} sits in the lane-header band "
                    f"(body starts y={body_top:g}). A connector must never cross the header/title."
                )

    # HARD: the final segment must be a perpendicular stab into the entered face,
    # landing on that face's connection point. One check enforces center-stab +
    # perpendicular last segment + correct arrow direction at once (the recurring
    # "arrow grazes in sideways / off-center" complaint).
    for e in edges:
        if not e.points or e.target is None:
            continue
        tgt = cells.get(e.target)
        if tgt is None or tgt.x is None or tgt.w is None or tgt.h is None:
            continue
        ex, ey = fnum(e.style.get("entryX")), fnum(e.style.get("entryY"))
        if ex is None or ey is None:
            continue
        tox, toy = abs_origin(tgt, cells)
        lx, ly = e.points[-1]
        label = e.value or e.id or "<edge>"
        tname = tgt.value or e.target
        if ey in (0.0, 1.0):            # top/bottom face -> last leg must be vertical
            cx = tox + tgt.x + ex * tgt.w
            if abs(lx - cx) > TOL + 1:
                face = "top" if ey == 0.0 else "bottom"
                hard.append(
                    f"edge '{label}' -> {tname} {face}: off-center entry (last waypoint "
                    f"x={lx:g}, face center x={cx:g}) - final leg isn't a straight vertical "
                    f"stab; the arrow grazes in sideways. Set last waypoint x={cx:g}.")
        elif ex in (0.0, 1.0):          # left/right face -> last leg must be horizontal
            cy = toy + tgt.y + ey * tgt.h
            if abs(ly - cy) > TOL + 1:
                face = "left" if ex == 0.0 else "right"
                hard.append(
                    f"edge '{label}' -> {tname} {face}: off-center entry (last waypoint "
                    f"y={ly:g}, face center y={cy:g}) - final leg isn't a straight horizontal "
                    f"stab. Set last waypoint y={cy:g}.")

    # HARD: the FIRST segment must be a perpendicular stab OUT of the source face
    # (mirror of the entry rule): exit-right -> leave horizontally first, exit-bottom ->
    # leave straight down first, THEN bend. A 1-bend L's single corner must therefore
    # sit at the source centre on the exit axis AND the target centre on the entry axis.
    for e in edges:
        if not e.points or e.source is None:
            continue
        src = cells.get(e.source)
        if src is None or src.x is None or src.w is None or src.h is None:
            continue
        xx, xy = fnum(e.style.get("exitX")), fnum(e.style.get("exitY"))
        if xx is None or xy is None:
            continue
        sox, soy = abs_origin(src, cells)
        fx, fy = e.points[0]
        label = e.value or e.id or "<edge>"
        sname = src.value or e.source
        if xy in (0.0, 1.0):           # top/bottom exit -> first leg must be vertical
            cx = sox + src.x + xx * src.w
            if abs(fx - cx) > TOL + 1:
                face = "top" if xy == 0.0 else "bottom"
                hard.append(
                    f"edge '{label}' <- {sname} {face}: off-centre EXIT (first waypoint "
                    f"x={fx:g}, face centre x={cx:g}) - it doesn't leave straight out the "
                    f"face before bending. Set first waypoint x={cx:g}.")
        elif xx in (0.0, 1.0):         # left/right exit -> first leg must be horizontal
            cy = soy + src.y + xy * src.h
            if abs(fy - cy) > TOL + 1:
                face = "left" if xx == 0.0 else "right"
                hard.append(
                    f"edge '{label}' <- {sname} {face}: off-centre EXIT (first waypoint "
                    f"y={fy:g}, face centre y={cy:g}) - it doesn't leave straight out the "
                    f"face before bending. Set first waypoint y={cy:g}.")

    # HARD: a diagram title must sit ABOVE the lanes, never below the pool.
    lane_top = min((abs_origin(ln, cells)[1] + ln.y for ln in lanes), default=None)
    lane_bot = max((abs_origin(ln, cells)[1] + ln.y + (ln.h or 0) for ln in lanes), default=None)
    if lane_top is not None:
        for c in cells.values():
            if (c.is_vertex and c.is_text() and not c.is_lane()
                    and c.y is not None and c.w is not None and c.w >= 150):
                _, oy = abs_origin(c, cells)
                ty = oy + c.y
                if ty >= lane_bot - (c.h or 0):        # title sits at/below the pool bottom
                    hard.append(
                        f"title text '{c.value[:30]}' is below the pool (y={ty:g}) - a "
                        f"diagram title must be a horizontal bar ABOVE the lanes (y<{lane_top:g}).")

    # ADVISORY: >1 connector on the same side of a box (P8 - taste only)
    side_count = {}  # (node_id, side) -> n
    for e in edges:
        for end, idattr in (("exit", e.source), ("entry", e.target)):
            if idattr is None:
                continue
            ex = fnum(e.style.get(f"{end}X"))
            ey = fnum(e.style.get(f"{end}Y"))
            if ex is None or ey is None:
                continue
            if ey in (0.0, 1.0) and ex not in (0.0, 1.0):
                side = "top" if ey == 0.0 else "bottom"
            elif ex in (0.0, 1.0):
                side = "left" if ex == 0.0 else "right"
            else:
                continue
            side_count[(idattr, side)] = side_count.get((idattr, side), 0) + 1
    for (nid, side), n in sorted(side_count.items()):
        if n > 1:
            nm = cells.get(nid).value if cells.get(nid) else nid
            advisory.append(f"node '{nm or nid}': {n} connectors on its {side} side (P8 - fix only if free)")

    # ADVISORY: bend-heavy connectors (>=3 explicit waypoints ~ >=3 bends). A clean
    # forward hand-off is 0-1 bends; a loop 1-2. More -> look for a shorter route
    # (fewer bends / a face nearer the target). Advisory: never override P1 no-crossing.
    for e in edges:
        if len(e.points) >= 3:
            advisory.append(
                f"edge '{e.value or e.id}': {len(e.points)} waypoints (bend-heavy) - "
                f"check for a shorter route, but keep it crossing-free (P1 wins).")

    return hard, advisory


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--page", type=int, default=None, help="1-based page index")
    args = ap.parse_args()

    try:
        tree = ET.parse(args.file)
    except ET.ParseError as ex:
        print(f"FAIL: cannot parse {args.file} ({ex}). If the diagram is compressed, "
              f"open it in draw.io and re-save with 'Compressed' off.")
        sys.exit(2)

    diagrams = tree.getroot().findall(".//diagram")
    if not diagrams:  # already inside a single mxGraphModel
        diagrams = [tree.getroot()]

    total_hard = 0
    for i, dg in enumerate(diagrams, 1):
        if args.page is not None and i != args.page:
            continue
        name = dg.get("name") or f"page {i}"
        model = dg.find(".//root")
        root = model if model is not None else dg
        hard, advisory = check_page(root, name)
        total_hard += len(hard)
        print(f"=== {name} ===")
        if hard:
            for h in hard:
                print(f"  HARD  {h}")
        else:
            print("  OK    no over-the-top / header-band connectors")
        for a in advisory:
            print(f"  note  {a}")

    sys.exit(1 if total_hard else 0)


if __name__ == "__main__":
    main()
