# Connector routing mechanics (draw.io swimlanes)

Read this when an edge won't lay out cleanly from the one-line invariant in
SKILL.md — i.e. you're deciding **which face** an edge leaves/enters, **where the
corner goes**, how to route a **loop/return**, or how to split a big flow across
**pages**. Simple 0–1-bend hand-offs don't need any of this; the invariant plus
the routing table's first rows cover them.

## Contents
1. The routing invariant (one law for every connector)
2. Routing table (by target position)
3. Decision-diamond ports
4. The stab in XML (exact waypoint coordinates)
5. Loops and returns
6. Unavoidable crossings
7. Multi-page for big flows

---

## 1. The routing invariant — one law for every connector

**Both end segments are straight perpendicular stabs into the CENTRE of the face they
touch.** The **first** leg leaves the source face straight out before any bend — exit a
**right** face → go right first, a **bottom** → go down first, a **left** → left first, a
**top** → up first. The **last** leg enters the target face straight in, arrowhead along
its travel — **down** into a top, **up** into a bottom, **left** into a right face,
**right** into a left. Never a sideways nub at either end.

So a 1-bend L has its single corner at the **source centre on the exit axis AND the
target centre on the entry axis** — both, not one. Then choose faces for the **fewest
bends**: **0** when the two centres share an axis, **1** when offset on one axis, **2**
only when offset on both *and* a 1-bend L would cross something (P1 no-crossing always
beats saving a bend). General geometry, any boxes anywhere. `check_layout.py` hard-fails
an off-centre stab at **either** end and flags bend-heavy edges as advisory.

## 2. Routing table — by the position of target T relative to source S (box centres)

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
face, the straight same-column edge keeps it and the other moves to the face toward its
own neighbour. *(A box that is both a hand-off target and a loop-end — e.g. a loop-back
edge arrives straight up into its bottom while a forward branch enters its side — is just
two table rows applied to one box.)*

## 3. Decision-diamond ports

The descending flow enters the **top vertex**; the continuing (happy) branch exits toward
where flow goes next (the side toward the next lane, or the bottom if it stays in lane).
Each other branch exits a **remaining free vertex** — for a reject/back branch, **never
the top** (the top belongs to the incoming flow; exiting upward sends the line over
everything — the classic over-the-top reject). Prefer the **vertex facing the loop
target**: if the target box is off to one side, exit that **side** so the return is a
short horizontal hop into it; use the **bottom** only when the target sits below. Keep the
loop **tight** — take the shortest in-body route to the target's own row; don't drop to
the far bottom of the pool just to climb all the way back up.

Fixed connection points on a rhombus are the **vertices**: top `0.5,0` / bottom `0.5,1` /
left `0,0.5` / right `1,0.5` — never fractional, or the line lands on the bounding box
instead of the diamond.

## 4. The stab in XML (exact waypoint coordinates, both ends)

The **first waypoint shares the exit port's *other* coordinate** and the **last waypoint
shares the entry port's *other* coordinate**, so each end leg is one clean perpendicular
run (lead-in `>=~20px`). For any port: top/bottom port → the waypoint's **X = that box's
centre-X**; left/right port → the waypoint's **Y = that box's centre-Y**. A 1-bend L's
lone corner must satisfy **both** (e.g. side exit + top entry → corner X = target centre-X
*and* corner Y = source centre-Y). Off by even ~20px and the router jogs — the exact
miscalc `check_layout.py` flags at both ends (watch lane-relative vs absolute coords when
you compute a centre).

**Every waypoint must sit in clear space** — a gutter or the gap between boxes — **never
inside the box it routes to/past, and never on the far side of the face it enters.** For a
top entry the corner's y must be **above** the box top (so the arrow comes *down* into
it); for a bottom entry, below; left, to the left; right, to the right. A corner that
lands centred on the face but *inside* the body still passes a naive centre-check yet
renders as an arrow stabbing in from the wrong side — so `check_layout.py` hard-fails a
waypoint inside any box and a last/first waypoint on the wrong side of its face.

> **An auto-routed edge (no explicit waypoints) on perpendicular faces is the one geometry
> the gate cannot fully trace** — it flags this as an advisory. Add the corner waypoint so
> the edge's real path is checkable; that is also what lets you skip the PNG render.

## 5. Loops and returns

Loops/returns stay **inside the pool body** and route **down or sideways through empty
lane space** — never up over the top. A return edge must not pass **above the topmost
node** or through the **lane-header/title band**: that empty strip "crosses nothing",
which is exactly why it tempts you, but a line up there reads as broken
(`check_layout.py` hard-fails it). A genuine back-loop to a *higher* box goes straight
**up a clear column or an inner gutter** to the target's own row, then enters its side —
it does not shoot up out of the source and across the top. Take the shortest path that
crosses no *box* between the ports the plan assigned; detour through a gutter inside the
pool border only when a direct route would cross a box; if even that crosses, use a small
connector node (ellipse "back to X"). Explicit `<Array as="points">` waypoints, sharp
90°, **never overlap or cross** another line (P1 wins).

## 6. Unavoidable crossings

If a crossing genuinely cannot be removed by reordering nodes or rerouting, add
`jumpStyle=arc` to **one** of the two edges. This both renders the crossing legibly and
tells `check_layout.py` the crossing is acknowledged, so the gate downgrades it from a
hard fail to an allowed advisory. Use this only as the last resort — first reorder/reroute
(a crossing usually means two steps are out of flow order).

## 7. Multi-page for big flows (roughly >~12 nodes, or clearly separable phases)

Ask before splitting when it's borderline — a short flow belongs on ONE page. When it is
big: an **overview page** whose boxes are sub-process **bands** wired together as one flow,
then **one detail page per sub-process**. Generate both from ONE spec (`pages` array —
schema and band rules in `references/generator.md`): the engine spans each band across
exactly the lanes its sub-process involves (a pool child, uniform height, below the lane
headers) and orders the overview lanes by **participant clustering** — lanes that share a
band sit adjacent, hub participants central — so every band's span is minimal. Detail pages
keep per-lane BPMN distribution; mirror the overview's lane order there when the flow
allows, so the whole document shares one column map.

**Overview ↔ detail binding (linted at generate time — broken binding is a FAIL):**

1. A band's text EQUALS its detail page name — the reader navigates by exact name match.
2. One sub-process band : one detail page (folding several bands into one page is the
   allowed exception, not the default).
3. The detail page's Start is the band's entry; its (single) End is the band's exit.
4. The detail page's lanes are exactly the lanes the band spans — everyone the
   sub-process involves appears on the band, and no one else gets a lane on its page.

The *specific* decomposition — which sub-processes exist, what lives on each page — comes
from the task, not this skill.
