#!/usr/bin/env python3
"""Deterministic layout gate for draw.io swimlane flowcharts.

The eyeball verify-loop keeps intermittently missing a whole CLASS of failure:
the XML looks right because ONE coordinate lines up, so the model talks itself
into it, but the rendered connector is broken. This script turns those
judgement calls into hard gates. The recurring members of that class:

  - a return/loop routed *above the topmost node* or through the lane-header band
    (the "over-the-top" back-edge);
  - an end-stab whose perpendicular axis is centered but whose APPROACH axis is on
    the wrong side of the face, so the arrow stabs in from inside/beyond the box;
  - a waypoint dropped INSIDE the very box it routes to/past, so the line cuts the
    body even though the entry point itself is centered;
  - a segment driven straight THROUGH an unrelated box (P1, the no-crossing rule);
  - two connectors CROSSING (also P1) - hard unless one is marked jumpStyle=arc to
    declare the crossing legible/unavoidable.

It resolves lane-relative child geometry to absolute page coords (a node that is
a child of a lane has its y measured from the lane's top, NOT the page), then
applies the checks below.

Usage:
    python check_layout.py flow.drawio            # all pages
    python check_layout.py flow.drawio --page 2   # 1-based page

Exit code 1 if any HARD violation is found, else 0. Same-side (P8), bend-heavy, and
auto-route (portless) notes are ADVISORY (never fail). An auto-route advisory means
the gate could NOT fully trace that edge, so a clean Gate-1 run with zero auto-route
advisories is the signal the diagram is verified without a PNG render.
"""
from __future__ import annotations

import sys
import argparse
import xml.etree.ElementTree as ET

TOL = 2.0  # px slack for floating-point / grid noise

Point = tuple[float, float]
Box = tuple[float, float, float, float]  # (x0, y0, x1, y1) absolute


def parse_style(style: str | None) -> dict[str, str | bool]:
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


def fnum(x: str | None) -> float | None:
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


class Cell:
    def __init__(self, el: ET.Element) -> None:
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

    def is_lane(self) -> bool:
        return "swimlane" in self.style or "pool" in self.style

    def is_text(self) -> bool:
        return self.style.get("text") is True or "text" in self.style

    def is_rhombus(self) -> bool:
        return "rhombus" in self.style


def abs_origin(cell: Cell, cells: dict[str, Cell]) -> Point:
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


def node_box(cell: Cell, cells: dict[str, Cell]) -> Box:
    """Absolute (x0, y0, x1, y1) bounding box of a node."""
    ox, oy = abs_origin(cell, cells)
    x0 = ox + cell.x
    y0 = oy + cell.y
    return x0, y0, x0 + cell.w, y0 + cell.h


def pt_in_node(px: float, py: float, box: Box, is_rhombus: bool, inset: float) -> bool:
    """Is point strictly inside the node body (with inset)? Rhombus uses the
    diamond region so a waypoint near a bbox CORNER (outside the rhombus) is not
    a false positive."""
    x0, y0, x1, y1 = box
    if px <= x0 + inset or px >= x1 - inset or py <= y0 + inset or py >= y1 - inset:
        return False
    if is_rhombus:
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        hw, hh = (x1 - x0) / 2, (y1 - y0) / 2
        if hw <= 0 or hh <= 0:
            return False
        return abs(px - cx) / hw + abs(py - cy) / hh < 1.0
    return True


def seg_hits_rect(ax: float, ay: float, bx: float, by: float, box: Box, inset: float) -> bool:
    """Axis-aligned segment vs rect interior (inset to ignore grazing the edge).
    A diagonal segment is ignored - the perpendicular-stab checks own those."""
    x0, y0, x1, y1 = box
    x0 += inset; y0 += inset; x1 -= inset; y1 -= inset
    if x1 <= x0 or y1 <= y0:
        return False
    if abs(ax - bx) <= TOL:                       # vertical segment at x=ax
        if not (x0 < ax < x1):
            return False
        lo, hi = sorted((ay, by))
        return lo < y1 and hi > y0
    if abs(ay - by) <= TOL:                       # horizontal segment at y=ay
        if not (y0 < ay < y1):
            return False
        lo, hi = sorted((ax, bx))
        return lo < x1 and hi > x0
    return False


def edge_polyline(e: Cell, cells: dict[str, Cell]) -> list[Point]:
    """Full point list: source port (if a fixed exit port is set) + waypoints +
    target port (if a fixed entry port is set). Endpoints are absolute."""
    pts = []
    ex0, ey0 = fnum(e.style.get("exitX")), fnum(e.style.get("exitY"))
    ix0, iy0 = fnum(e.style.get("entryX")), fnum(e.style.get("entryY"))
    src, tgt = cells.get(e.source), cells.get(e.target)
    if src and src.x is not None and ex0 is not None and ey0 is not None:
        sox, soy = abs_origin(src, cells)
        pts.append((sox + src.x + ex0 * src.w, soy + src.y + ey0 * src.h))
    pts.extend(e.points)
    if tgt and tgt.x is not None and ix0 is not None and iy0 is not None:
        tox, toy = abs_origin(tgt, cells)
        pts.append((tox + tgt.x + ix0 * tgt.w, toy + tgt.y + iy0 * tgt.h))
    return pts


def _seg_cross(a1: Point, b1: Point, a2: Point, b2: Point) -> bool:
    """True if an axis-aligned segment a1-b1 crosses an axis-aligned segment a2-b2
    at an interior point (shared endpoints / collinear touches don't count)."""
    def orient(a: Point, b: Point) -> str | None:
        if abs(a[0] - b[0]) <= TOL:
            return "v"
        if abs(a[1] - b[1]) <= TOL:
            return "h"
        return None
    o1, o2 = orient(a1, b1), orient(a2, b2)
    if o1 is None or o2 is None or o1 == o2:
        return False  # only check the clean horizontal-vs-vertical case
    h = (a1, b1) if o1 == "h" else (a2, b2)
    v = (a1, b1) if o1 == "v" else (a2, b2)
    hy = h[0][1]
    vx = v[0][0]
    hx_lo, hx_hi = sorted((h[0][0], h[1][0]))
    vy_lo, vy_hi = sorted((v[0][1], v[1][1]))
    return (hx_lo + TOL < vx < hx_hi - TOL) and (vy_lo + TOL < hy < vy_hi - TOL)


def check_page(root: ET.Element, page_name: str) -> tuple[list[str], list[str]]:
    cells: dict[str, Cell] = {}
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

    # absolute boxes for every flow node, used by the waypoint/segment checks
    node_boxes = [(n, node_box(n, cells), n.is_rhombus())
                  for n in nodes if n.x is not None and n.w is not None]

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

    # HARD: no edge waypoint may sit INSIDE a box (any box, source/target included).
    # A turn dropped inside the box it is about to enter makes the connector stab in
    # from the wrong side / cut through the body - and the perpendicular-stab check
    # below passes it because the entry coordinate itself is centered. This is the
    # exact failure mode that keeps slipping the eye (one coord "looks right").
    for e in edges:
        label = e.value or e.id or "<edge>"
        for (px, py) in e.points:
            for (n, nb, is_rh) in node_boxes:
                if pt_in_node(px, py, nb, is_rh, TOL):
                    hard.append(
                        f"edge '{label}': waypoint ({px:g},{py:g}) sits INSIDE box "
                        f"'{n.value or n.id}'. A turn must stay in clear space (a gutter "
                        f"or the gap between boxes), never inside the box it routes to/past. "
                        f"For a top entry the corner's y must be ABOVE the box top.")
                    break

    # HARD: an edge segment must not pass THROUGH a box that is neither its source nor
    # its target. This is P1 (the top-priority no-crossing rule) and was previously
    # unguarded - a straight leg can clip a box with NO waypoint inside it.
    for e in edges:
        poly = edge_polyline(e, cells)
        if len(poly) < 2:
            continue
        label = e.value or e.id or "<edge>"
        hit = None
        for (ax, ay), (bx, by) in zip(poly, poly[1:]):
            for (n, nb, is_rh) in node_boxes:
                if is_rh or n.id in (e.source, e.target):
                    continue
                if seg_hits_rect(ax, ay, bx, by, nb, TOL):
                    hit = n
                    break
            if hit:
                break
        if hit:
            hard.append(
                f"edge '{label}': a segment passes THROUGH box '{hit.value or hit.id}' "
                f"(not its source/target). Reroute through a gutter or a connector node (P1).")

    # HARD: the final segment must be a perpendicular stab into the entered face -
    # centered on that face (perpendicular axis) AND approaching from the OUTSIDE
    # (approach axis). The center check alone passed e_dconf_auto: x was centered
    # but the last waypoint sat below the top edge, so the arrow stabbed UP from
    # inside the box. Both halves are needed.
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
        btop, bbot = toy + tgt.y, toy + tgt.y + tgt.h
        bleft, bright = tox + tgt.x, tox + tgt.x + tgt.w
        if ey in (0.0, 1.0):            # top/bottom face -> last leg must be vertical
            cx = tox + tgt.x + ex * tgt.w
            face = "top" if ey == 0.0 else "bottom"
            if abs(lx - cx) > TOL + 1:
                hard.append(
                    f"edge '{label}' -> {tname} {face}: off-center entry (last waypoint "
                    f"x={lx:g}, face center x={cx:g}) - final leg isn't a straight vertical "
                    f"stab; the arrow grazes in sideways. Set last waypoint x={cx:g}.")
            side_ok = (ly <= btop + TOL) if ey == 0.0 else (ly >= bbot - TOL)
            if not side_ok:
                where = "above" if ey == 0.0 else "below"
                hard.append(
                    f"edge '{label}' -> {tname} {face}: last waypoint y={ly:g} is on the WRONG "
                    f"side of the {face} face (box top={btop:g}, bottom={bbot:g}) - the arrow "
                    f"stabs in from inside/beyond, reading as a back-edge. The corner must sit "
                    f"{where} the box.")
        elif ex in (0.0, 1.0):          # left/right face -> last leg must be horizontal
            cy = toy + tgt.y + ey * tgt.h
            face = "left" if ex == 0.0 else "right"
            if abs(ly - cy) > TOL + 1:
                hard.append(
                    f"edge '{label}' -> {tname} {face}: off-center entry (last waypoint "
                    f"y={ly:g}, face center y={cy:g}) - final leg isn't a straight horizontal "
                    f"stab. Set last waypoint y={cy:g}.")
            side_ok = (lx <= bleft + TOL) if ex == 0.0 else (lx >= bright - TOL)
            if not side_ok:
                where = "left of" if ex == 0.0 else "right of"
                hard.append(
                    f"edge '{label}' -> {tname} {face}: last waypoint x={lx:g} is on the WRONG "
                    f"side of the {face} face (box left={bleft:g}, right={bright:g}) - the arrow "
                    f"stabs in from inside/beyond. The corner must sit {where} the box.")

    # HARD: the FIRST segment must be a perpendicular stab OUT of the source face
    # (mirror of the entry rule): centered on the face AND leaving to the OUTSIDE
    # before any bend.
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
        btop, bbot = soy + src.y, soy + src.y + src.h
        bleft, bright = sox + src.x, sox + src.x + src.w
        if xy in (0.0, 1.0):           # top/bottom exit -> first leg must be vertical
            cx = sox + src.x + xx * src.w
            face = "top" if xy == 0.0 else "bottom"
            if abs(fx - cx) > TOL + 1:
                hard.append(
                    f"edge '{label}' <- {sname} {face}: off-centre EXIT (first waypoint "
                    f"x={fx:g}, face centre x={cx:g}) - it doesn't leave straight out the "
                    f"face before bending. Set first waypoint x={cx:g}.")
            side_ok = (fy <= btop + TOL) if xy == 0.0 else (fy >= bbot - TOL)
            if not side_ok:
                where = "above" if xy == 0.0 else "below"
                hard.append(
                    f"edge '{label}' <- {sname} {face}: first waypoint y={fy:g} is on the WRONG "
                    f"side of the {face} face (box top={btop:g}, bottom={bbot:g}) - it doesn't "
                    f"leave the box before bending. The corner must sit {where} the box.")
        elif xx in (0.0, 1.0):         # left/right exit -> first leg must be horizontal
            cy = soy + src.y + xy * src.h
            face = "left" if xx == 0.0 else "right"
            if abs(fy - cy) > TOL + 1:
                hard.append(
                    f"edge '{label}' <- {sname} {face}: off-centre EXIT (first waypoint "
                    f"y={fy:g}, face centre y={cy:g}) - it doesn't leave straight out the "
                    f"face before bending. Set first waypoint y={cy:g}.")
            side_ok = (fx <= bleft + TOL) if xx == 0.0 else (fx >= bright - TOL)
            if not side_ok:
                where = "left of" if xx == 0.0 else "right of"
                hard.append(
                    f"edge '{label}' <- {sname} {face}: first waypoint x={fx:g} is on the WRONG "
                    f"side of the {face} face (box left={bleft:g}, right={bright:g}) - it doesn't "
                    f"leave the box before bending. The corner must sit {where} the box.")

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

    # ADVISORY: an edge with NO explicit waypoints whose fixed ports don't line up
    # will be auto-routed with a jog. Usually harmless; flag so a real misalignment
    # gets a look (kept advisory - draw.io's auto-route is often a clean orthogonal).
    # These advisories are also the PNG-skip tripwire: an auto-routed edge is the one
    # case the crossing/through-box HARD checks above cannot fully see (they only trace
    # axis-aligned legs), so as long as ANY of these fire, the diagram still needs the
    # one final visual glance. Zero auto-route advisories + Gate 1 exit 0 = the script
    # saw every edge's real geometry, and the PNG can be skipped.
    for e in edges:
        if e.points or e.source is None or e.target is None:
            continue
        ex0, ey0 = fnum(e.style.get("exitX")), fnum(e.style.get("exitY"))
        ix0, iy0 = fnum(e.style.get("entryX")), fnum(e.style.get("entryY"))
        if None in (ex0, ey0, ix0, iy0):
            continue
        src, tgt = cells.get(e.source), cells.get(e.target)
        if not src or not tgt or src.x is None or tgt.x is None:
            continue
        sox, soy = abs_origin(src, cells)
        tox, toy = abs_origin(tgt, cells)
        sx, sy = sox + src.x + ex0 * src.w, soy + src.y + ey0 * src.h
        txp, typ = tox + tgt.x + ix0 * tgt.w, toy + tgt.y + iy0 * tgt.h
        if ey0 in (0.0, 1.0) and iy0 in (0.0, 1.0) and abs(sx - txp) > TOL + 1:
            advisory.append(
                f"edge '{e.value or e.id}': no waypoints, source/target centre-x differ "
                f"({sx:g} vs {txp:g}) - draw.io will jog it. Align centres or add a waypoint.")
        elif ex0 in (0.0, 1.0) and ix0 in (0.0, 1.0) and abs(sy - typ) > TOL + 1:
            advisory.append(
                f"edge '{e.value or e.id}': no waypoints, source/target centre-y differ "
                f"({sy:g} vs {typ:g}) - draw.io will jog it. Align centres or add a waypoint.")
        elif (ey0 in (0.0, 1.0)) != (iy0 in (0.0, 1.0)):
            advisory.append(
                f"edge '{e.value or e.id}': no waypoints, exit and entry are on "
                f"perpendicular faces - draw.io auto-routes an L the gate cannot trace. "
                f"Add the corner waypoint so its geometry is checkable (or render to confirm).")

    # HARD: two connectors cross (a horizontal leg of one meets a vertical leg of
    # another in open space). Crossings are P1, the strongest readability rule, so an
    # un-acknowledged crossing is a hard fail - this is what lets the script stand in
    # for the eye instead of every diagram paying for a PNG render. The one legitimate
    # crossing is the legible kind: when it genuinely cannot be routed away, the author
    # marks ONE of the two edges with jumpStyle=arc (or =gap/=sharp). A crossing where
    # either edge carries jumpStyle is therefore treated as acknowledged -> advisory,
    # not a fail. (Caveat the skill must respect: this only sees axis-aligned legs;
    # an auto-routed edge with no explicit waypoints can render a crossing the script
    # never evaluates - hence the auto-route advisory above is the PNG-skip tripwire.)
    polys = [(e, edge_polyline(e, cells)) for e in edges]
    reported = set()
    for i in range(len(polys)):
        e1, p1 = polys[i]
        if len(p1) < 2:
            continue
        for j in range(i + 1, len(polys)):
            e2, p2 = polys[j]
            if len(p2) < 2:
                continue
            pair = frozenset((e1.id, e2.id))
            if pair in reported:
                continue
            crossed = False
            for (a1, b1) in zip(p1, p1[1:]):
                for (a2, b2) in zip(p2, p2[1:]):
                    if _seg_cross(a1, b1, a2, b2):
                        crossed = True
                        break
                if crossed:
                    break
            if crossed:
                reported.add(pair)
                n1, n2 = e1.value or e1.id, e2.value or e2.id
                if e1.style.get("jumpStyle") or e2.style.get("jumpStyle"):
                    advisory.append(
                        f"edges '{n1}' and '{n2}' cross but one has jumpStyle "
                        f"(acknowledged/legible) - allowed.")
                else:
                    hard.append(
                        f"edges '{n1}' and '{n2}' cross (P1). Reorder nodes so the "
                        f"sequence no longer forces it, or reroute (extra bend / outer "
                        f"gutter / connector node). Only if truly unavoidable, add "
                        f"jumpStyle=arc to one edge to mark it legible.")

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


def main() -> None:
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
