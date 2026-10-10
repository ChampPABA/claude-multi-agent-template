"""Gate, then render one signoff page from a confirmed drawio-swimlane spec + signoff.json.

usage: python3 build_signoff.py SPEC.json SIGNOFF.json OUT.html

The gate runs first. Any finding -> it prints every finding, writes nothing, exits 1.
Flow layout comes from the spec's topology, not from drawio positions: one row per flow
depth, one column per lane (a lane widens when two of its steps share a row).
"""
import html, json, math, re, sys
from pathlib import Path

esc = html.escape
TEMPLATE = Path(__file__).resolve().parent.parent / 'assets' / 'page.html'
TASK = ('process', 'document', 'subprocess')
GENERIC_END = {'', 'end', 'จบ', 'สิ้นสุด'}
# meta / instruction text Champ rejected as "AI smell": a signoff carries content only
BANNED = ['บันทึกได้เมื่อ', 'ตกลงแล้วไม่ต้อง', 'ไม่มีความเห็น', 'ว่าง = ผ่าน', 'ว่าง=ผ่าน', 'วิธีตอบ', 'วิธีอ่าน',
          'ปิดรอบ', 'claude.ai', 'POC']
STATUS = {'have': 'มีแล้ว', 'extend': 'มีแล้ว ต้องเพิ่ม', 'add': 'ต้องสร้างใหม่', 'decided': 'ตัดสินแล้ว', 'decide': 'รอตัดสิน'}
WF_BTN = re.compile(r'\[\[(.+?)(?:->(\w+))?\]\]')
LANE_W, BOX_W, HEAD_H, GAP, MARGIN = 210, 182, 36, 34, 40
THAI_MARK = re.compile('[ัิ-ฺ็-๎]')


# ---------------------------------------------------------------- input
def chapters_of(spec):
    """Detail pages of the spec -> [{id, title, lanes, nodes, edges}]; overview pages are skipped."""
    pages = spec['pages'] if 'pages' in spec else [dict(spec, name=spec['title'])]
    out = []
    for p in pages:
        if p.get('type') == 'overview':
            continue
        cid, _, title = p['name'].partition(' - ')
        out.append(dict(id=cid.strip(), title=(title or cid).strip(), lanes=p['lanes'],
                        nodes=p['nodes'], edges=p['edges']))
    return out


def key(cid, nid):
    """Step key 'A3-t1': spec ids may be bare ('t1') or already prefixed ('A3-t1')."""
    return nid if nid.startswith(cid + '-') else f'{cid}-{nid}'


def strings(x, path=''):
    if isinstance(x, str):
        yield path, x
    elif isinstance(x, dict):
        for k, v in x.items():
            yield from strings(v, f'{path}.{k}' if path else k)
    elif isinstance(x, list):
        for i, v in enumerate(x):
            yield from strings(v, f'{path}[{v["id"] if isinstance(v, dict) and "id" in v else i}]')


# ---------------------------------------------------------------- layout
def lines(text, per=20):
    return max(1, math.ceil(len(THAI_MARK.sub('', text)) / per))


def layout(ch):
    nodes = {n['id']: dict(n) for n in ch['nodes']}
    out = {k: [] for k in nodes}
    for e in ch['edges']:
        out[e['src']].append(e['dst'])
    start = next(n['id'] for n in ch['nodes'] if n['kind'] == 'start')
    back, state = set(), {}

    def dfs(u):  # back edge = edge into a node still on the DFS stack
        state[u] = 1
        for v in out[u]:
            if state.get(v) == 1:
                back.add((u, v))
            elif v not in state:
                dfs(v)
        state[u] = 2
    dfs(start)
    depth = {start: 0}
    for _ in nodes:  # longest path over forward edges; flows are small
        for e in ch['edges']:
            if (e['src'], e['dst']) not in back and e['src'] in depth:
                depth[e['dst']] = max(depth.get(e['dst'], 0), depth[e['src']] + 1)
    num, k = {}, 0
    for nid in sorted(nodes, key=lambda i: (depth[i], nodes[i]['lane'])):
        if nodes[nid]['kind'] in TASK:
            k += 1
            num[nid] = k
    rows = {}
    for nid, n in nodes.items():
        rows.setdefault((depth[nid], n['lane']), []).append(nid)
    nl = len(ch['lanes'])
    cols = [max([len(v) for (d, l), v in rows.items() if l == i] or [1]) for i in range(nl)]
    lx, x = [], MARGIN
    for i in range(nl):
        lx.append(x)
        x += LANE_W * cols[i]

    def h(n):
        if n['kind'] in ('start', 'end'):
            return 30
        if n['kind'] == 'decision':
            return 56
        return 22 + 17 * lines(n['text']) + (16 if sub_line(n) else 0)
    y = HEAD_H + 24
    for d in range(max(depth.values()) + 1):
        here = [i for i in nodes if depth[i] == d]
        rh = max(h(nodes[i]) for i in here)
        for (dd, l), ids in rows.items():
            if dd != d:
                continue
            for j, nid in enumerate(ids):
                n = nodes[nid]
                cx = lx[l] + (LANE_W * cols[l] / 2 if len(ids) == 1 else LANE_W * j + LANE_W / 2)
                n.update(cx=cx, cy=y + rh / 2, h=h(n), w=BOX_W if n['kind'] in TASK else (64 if n['kind'] == 'decision' else 30))
        y += rh + GAP
    return nodes, back, num, lx, cols, x + 24, y + 8


def sub_line(n):
    if n.get('outside'):
        return f'นอกระบบ · {n["outside"]}'
    if n.get('type') == 'service':
        return 'ระบบทำเอง'
    return ''


def flow_svg(ch, nodes, back, num, lx, cols, W, H):
    cid = ch['id']
    top = lambda n: n['cy'] - n['h'] / 2
    bot = lambda n: n['cy'] + n['h'] / 2
    s = [f'<svg class="hflow" viewBox="0 0 {W} {H}" width="{W}" role="img" aria-label="{esc(ch["title"])}">',
         f'<defs><marker id="ar-{cid}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="arh"/></marker></defs>']
    for i, name in enumerate(ch['lanes']):
        w = LANE_W * cols[i]
        s.append(f'<rect class="lh" x="{lx[i]}" y="0" width="{w}" height="{HEAD_H}"/><text class="lt" x="{lx[i] + w / 2}" y="23" text-anchor="middle">{esc(name)}</text>'
                 f'<rect class="lane" x="{lx[i]}" y="{HEAD_H}" width="{w}" height="{H - HEAD_H - 4}"/>')
    # system frames: consecutive steps of one lane done in the same system, in row order
    for i in range(len(ch['lanes'])):
        run, groups = [], []
        for n in sorted((n for n in nodes.values() if n['lane'] == i and n['kind'] not in ('start', 'end')), key=lambda n: n['cy']):
            if run and n.get('system') != run[0].get('system'):
                groups.append(run)
                run = []
            if n.get('system'):
                run.append(n)
        if run:
            groups.append(run)
        for g in groups:
            x0 = min(n['cx'] - BOX_W / 2 for n in g) - 9
            x1 = max(n['cx'] + BOX_W / 2 for n in g) + 9
            y0, y1 = min(top(n) for n in g) - 14, max(bot(n) for n in g) + 12
            s.append(f'<rect class="sys" x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" rx="4"/><text class="sl" x="{x0 + 6}" y="{y0 - 4}">{esc(g[0]["system"])}</text>')
    for e in ch['edges']:
        a, b, lab = nodes[e['src']], nodes[e['dst']], e.get('label', '')
        if (e['src'], e['dst']) in back:
            # loop back just left of both boxes; enter below centre so it never shares the forward arrow's tip
            yb = bot(a) + 14
            xl = min(a['cx'] - a['w'] / 2, b['cx'] - b['w'] / 2) - 14
            pts = [(a['cx'], bot(a)), (a['cx'], yb), (xl, yb), (xl, b['cy'] + 10), (b['cx'] - b['w'] / 2, b['cy'] + 10)]
            tx, ty = xl + 6, yb - 5
        elif a['kind'] == 'decision' and abs(b['cx'] - a['cx']) > 1:
            sx = a['cx'] + (a['w'] / 2 if b['cx'] > a['cx'] else -a['w'] / 2)
            pts = [(sx, a['cy']), (b['cx'], a['cy']), (b['cx'], top(b))]
            tx, ty = (sx + b['cx']) / 2 - 14, a['cy'] - 6
        elif abs(b['cx'] - a['cx']) < 1:
            pts = [(a['cx'], bot(a)), (b['cx'], top(b))]
            tx, ty = a['cx'] + 6, (bot(a) + top(b)) / 2
        else:
            side = b['cx'] - b['w'] / 2 if b['cx'] > a['cx'] else b['cx'] + b['w'] / 2
            pts = [(a['cx'], bot(a)), (a['cx'], b['cy']), (side, b['cy'])]
            tx, ty = a['cx'] + 6, b['cy'] - 6
        s.append(f'<path class="e" d="M{" L".join(f"{x:.0f},{y:.0f}" for x, y in pts)}" marker-end="url(#ar-{cid})"/>')
        if lab:
            s.append(f'<text class="el" x="{tx:.0f}" y="{ty:.0f}">{esc(lab)}</text>')
    for nid, n in nodes.items():
        cx, cy = n['cx'], n['cy']
        if n['kind'] == 'start':
            s.append(f'<circle class="ev" cx="{cx}" cy="{cy}" r="13"/>')
        elif n['kind'] == 'end':
            s.append(f'<circle class="evend" cx="{cx}" cy="{cy}" r="14"/><text class="el" x="{cx}" y="{cy + 32}" text-anchor="middle">{esc(n["text"])}</text>')
        elif n['kind'] == 'decision':
            s.append(f'<path class="box" d="M{cx},{cy - 28} L{cx + 32},{cy} L{cx},{cy + 28} L{cx - 32},{cy} Z"/>'
                     f'<text class="bt" x="{cx}" y="{cy + 4}" text-anchor="middle">{esc(n["text"])}</text>')
        else:
            x0, y0, sub = cx - BOX_W / 2, top(n), sub_line(n)
            s.append(f'<g class="go" tabindex="0" role="link" data-step="{key(cid, nid)}">'
                     f'<rect class="box" x="{x0}" y="{y0}" width="{BOX_W}" height="{n["h"]}" rx="6"/>'
                     f'<text class="bn" x="{x0 + 7}" y="{y0 + 14}">{num[nid]}</text>'
                     f'<foreignObject x="{x0 + 14}" y="{y0}" width="{BOX_W - 28}" height="{n["h"]}"><div xmlns="http://www.w3.org/1999/xhtml" class="bl">'
                     f'<div>{esc(n["text"])}</div>{f"<div class=bs>{esc(sub)}</div>" if sub else ""}</div></foreignObject></g>')
    s.append('</svg>')
    return ''.join(s)


def joined(v):
    return ' · '.join(v) if isinstance(v, list) else (v or '')


def step_table(ch, nodes, num, pidx):
    cid, rows = ch['id'], []
    for nid in sorted(num, key=num.get):
        n = nodes[nid]
        if n.get('page'):
            p = n['page']
            where = f'<a class="where w-sys" href="#wf-{p}" data-go="wf-{p}">{esc(pidx[p]["title"])}</a> <span class="hpid">{p}</span>'
        elif n.get('system'):
            where = f'<span class="where w-sys">{esc(n["system"])}</span>'
        elif n.get('outside'):
            where = f'<span class="where w-out">{esc(n["outside"])}</span>'
        elif n.get('type') == 'service':
            where = '<span class="where w-out">ระบบทำเอง</span>'
        else:
            where = '–'
        rows.append(f'<tr data-step="{key(cid, nid)}"><td class="num">{cid}.{num[nid]}</td><td>{esc(n["text"])}</td><td>{esc(ch["lanes"][n["lane"]])}</td>'
                    f'<td>{where}</td><td>{esc(joined(n.get("changes"))) or "–"}</td><td>{esc(joined(n.get("errors"))) or "–"}</td></tr>')
    for n in ch['nodes']:
        if n['kind'] == 'end':
            rows.append(f'<tr class="endrow"><td class="num">จบ</td><td colspan="5">{esc(n["text"])}</td></tr>')
    return ('<div class="htbl"><table><tr><th>ขั้น</th><th>ทำอะไร</th><th>ใคร</th><th>ทำที่ไหน</th><th>เกิดอะไรขึ้น</th><th>ถ้าไม่ผ่าน</th></tr>'
            + ''.join(rows) + '</table></div>')


# ---------------------------------------------------------------- gate
def gate(chs, S):
    bad = []
    pidx = {p['id']: p for p in S.get('pages', [])}
    cids = {c['id'] for c in chs}
    steps = set()
    for ch in chs:
        cid = ch['id']
        for lane in ch['lanes']:
            if lane.strip().lower() in ('system', 'ระบบ'):
                bad.append(f'{cid}: lane "{lane}" - lanes are people only; redraw in BPMN-lite with drawio-swimlane (system frames, not a System lane)')
        ids = {n['id'] for n in ch['nodes']}
        starts = [n for n in ch['nodes'] if n['kind'] == 'start']
        if len(starts) != 1:
            bad.append(f'{cid}: needs exactly one Start, found {len(starts)}')
        for n in ch['nodes']:
            k = key(cid, n['id'])
            if '[TBD]' in n.get('text', ''):
                bad.append(f'{k}: still [TBD] "{n["text"]}" - finish it in drawio-swimlane and --read it back first')
            if n['kind'] == 'end' and n.get('text', '').strip().lower() in GENERIC_END:
                bad.append(f'{k}: End has no outcome text (say what is true at the end, e.g. "Partner active")')
            if n.get('page') and n['page'] not in pidx:
                bad.append(f'{k}: page {n["page"]} is not in signoff.json pages')
            if n['kind'] in TASK:
                steps.add(k)
        for e in ch['edges']:
            if e['src'] not in ids or e['dst'] not in ids:
                bad.append(f'{cid}: edge {e["src"]} -> {e["dst"]} points at a box that does not exist')
            elif next(n for n in ch['nodes'] if n['id'] == e['src'])['kind'] == 'decision' and not e.get('label'):
                bad.append(f'{key(cid, e["src"])} -> {e["dst"]}: decision branch has no label')
            if '[TBD]' in e.get('label', ''):
                bad.append(f'{cid}: edge {e["src"]} -> {e["dst"]} label still [TBD]')
        if len(starts) == 1 and not any('edge' in b and b.startswith(cid) for b in bad):
            seen, todo = set(), [starts[0]['id']]
            while todo:
                u = todo.pop()
                if u not in seen:
                    seen.add(u)
                    todo += [e['dst'] for e in ch['edges'] if e['src'] == u]
            for n in ch['nodes']:
                if n['id'] not in seen:
                    bad.append(f'{key(cid, n["id"])}: not reachable from Start, so it would get no step number')
        if cid not in S.get('story', {}):
            bad.append(f'{cid}: signoff.json story has no entry for this chapter')
    for k in S.get('story', {}):
        if k != 'overview' and k not in cids:
            bad.append(f'story.{k}: no chapter {k} in the spec')
    if 'overview' not in S.get('story', {}):
        bad.append('story.overview: missing')
    for q in S.get('questions', []):
        if q['chapter'] != 'overview' and q['chapter'] not in cids:
            bad.append(f'{q["id"]}: chapter {q["chapter"]} not in the spec')
        bad += [f'{q["id"]}: page {p} is not in pages' for p in q.get('pages', []) if p not in pidx]
    for p in S.get('pages', []):
        if p.get('status') != 'old' and not p.get('wireframe'):
            bad.append(f'{p["id"]}: {p.get("status")} page has no wireframe')
        bad += [f'{p["id"]}: wireframe button "{lab}" goes to {to}, not in pages'
                for lab, to in WF_BTN.findall(p.get('wireframe', '')) if to and to not in pidx]
    for m in S.get('emails', []):
        bad += [f'{m["id"]}: {f} {m[f]} is not in pages' for f in ('from_page', 'to_page') if m.get(f) not in pidx]
        if m.get('step') and m['step'] not in steps:
            bad.append(f'{m["id"]}: step {m["step"]} is not a box in the flow')
    for b in S.get('baseline', []):
        if b['status'] not in STATUS:
            bad.append(f'baseline "{b["topic"]}": status {b["status"]} not one of {", ".join(STATUS)}')
        bad += [f'baseline "{b["topic"]}": step {s} is not a box in the flow' for s in b.get('steps', []) if s not in steps]
    # free-text references (A2-d, A3.1, Q4, P8, E3) must point at something that exists
    ids = {key(c['id'], n['id']) for c in chs for n in c['nodes']}
    nums = {c['id']: sum(1 for n in c['nodes'] if n['kind'] in TASK) for c in chs}
    qids, eids = {q['id'] for q in S.get('questions', [])}, {m['id'] for m in S.get('emails', [])}
    texts = list(strings(S)) + [(f'spec {key(c["id"], n["id"])}', t) for c in chs for n in c['nodes']
                                for _, t in strings({k: n.get(k) for k in ('changes', 'errors')})]
    for path, text in texts:
        if path.endswith('wireframe'):
            continue
        bad += [f'{path}: refers to step {r}, which is not in the flow' for r in re.findall(r'\b[A-Z]\d+-[a-z]\w*\b', text)
                if r.split('-')[0] in cids and r not in ids]
        bad += [f'{path}: refers to step {c}.{n}, but {c} has {nums[c]} steps' for c, n in re.findall(r'\b([A-Z]\d+)\.(\d+)\b', text)
                if c in nums and not 1 <= int(n) <= nums[c]]
        bad += [f'{path}: refers to {r}, which is not a question' for r in re.findall(r'\bQ\d+\b', text) if r not in qids]
        bad += [f'{path}: refers to {r}, which is not in pages' for r in re.findall(r'\bP\d+\b', text) if r not in pidx]
        bad += [f'{path}: refers to {r}, which is not an email' for r in re.findall(r'\bE\d+\b', text) if r not in eids]
    for path, text in strings(S):
        if '[TBD]' in text:
            bad.append(f'signoff.json {path}: still [TBD]')
        bad += [f'signoff.json {path}: meta/instruction text "{w}" - a signoff carries content only' for w in BANNED if w in text]
    return bad


# ---------------------------------------------------------------- page
def fb(prefix, k, label):
    k = f'{prefix}-{k}'
    return (f'<div class="fb" data-key="{k}"><div class="fbh">{esc(label)}</div><textarea id="t-{k}" rows="2" aria-label="{esc(label)}"></textarea>'
            '<div class="fbrow"><button type="button" class="fbsave">บันทึก</button><span class="fbst"></span></div></div>')


def build(spec, S):
    chs = chapters_of(spec)
    pidx = {p['id']: p for p in S['pages']}
    fp = S['version']
    chip = lambda p: f'<a class="chip" href="#wf-{p}" data-go="wf-{p}">{p} {esc(pidx[p]["title"])}</a>' if pidx[p].get('wireframe') else f'<span class="chip">{p} {esc(pidx[p]["title"])}</span>'
    steplink = lambda k: f'<a href="#" data-go="step:{k}" class="mono">{k}</a>'

    def qcards(c):
        return ''.join(
            f'<div class="qcard" id="{q["id"]}"><span class="qid">{q["id"]}</span><div><b>{esc(q["question"])}</b>'
            + (f'<p>{esc(q["detail"])}</p>' if q.get('detail') else '')
            + f'<p class="dflt">ถ้าไม่มีใครแย้ง ใช้: <b>{esc(q["default"])}</b></p>'
            + (f'<small>เกี่ยวกับหน้า: {" ".join(chip(p) for p in q["pages"])}</small>' if q.get('pages') else '')
            + fb(fp, q['id'], 'เห็นต่างหรือต้องแก้') + '</div></div>'
            for q in S.get('questions', []) if q['chapter'] == c)
    nq = lambda c: sum(1 for q in S.get('questions', []) if q['chapter'] == c)
    badge = lambda c: f'<span class="badge">{nq(c)}</span>' if nq(c) else ''

    # chapters
    panes, used_in, flows = [], {}, {}
    for ch in chs:
        nodes, back, num, lx, cols, W, H = layout(ch)
        flows[ch['id']] = num
        svg, table = flow_svg(ch, nodes, back, num, lx, cols, W, H), step_table(ch, nodes, num, pidx)
        pages = []
        for nid in sorted(num, key=num.get):
            p = nodes[nid].get('page')
            if p:
                used_in.setdefault(p, []).append(key(ch['id'], nid))
                if p not in pages:
                    pages.append(p)
        qs = qcards(ch['id'])
        panes.append(f'<section class="pane" id="{ch["id"]}" role="tabpanel" hidden><p class="eyebrow">{ch["id"]}</p><h2>{ch["id"]}. {esc(ch["title"])}</h2>'
                     f'<h3>เรื่องนี้เกิดอะไรขึ้น</h3><div class="story">{esc(S["story"][ch["id"]])}</div>'
                     f'<h3>Flow</h3><div class="canvas" id="flow-{ch["id"]}">{svg}</div><h3>ทีละขั้น</h3>{table}'
                     + (f'<h3>หน้าจอในเรื่องนี้</h3><p>{" ".join(chip(p) for p in pages)}</p>' if pages else '')
                     + (f'<h3>คำถามในเรื่องนี้</h3><div class="qcards">{qs}</div>' if qs else '') + '</section>')
    chain = '<span class="arrow" aria-hidden="true">→</span>'.join(
        f'<a class="fcard" href="#{c["id"]}" data-go="{c["id"]}"><span class="mono">{c["id"]}</span><b>{esc(c["title"])}</b>'
        f'<span class="meta">{len(flows[c["id"]])} ขั้น · {nq(c["id"])} คำถาม</span></a>' for c in chs)
    oq = qcards('overview')
    overview = (f'<section class="pane" id="overview" role="tabpanel" hidden><h3>เรื่องทั้งหมด</h3><div class="story">{esc(S["story"]["overview"])}</div>'
                f'<h3>เรียงตามลำดับที่เกิดจริง</h3><div class="chain">{chain}</div>'
                + (f'<h3>เรื่องที่ยังไม่มี flow</h3><div class="qcards">{oq}</div>' if oq else '') + '</section>')

    # sitemap: one column per page.column, nav edges from wireframe buttons, email edges dashed
    NW, NH, CW, RH, X0, Y0 = 200, 54, 236, 92, 20, 60
    colnames = list(dict.fromkeys(p['column'] for p in S['pages']))
    pos, fill = {}, [0] * len(colnames)
    for p in S['pages']:
        c = colnames.index(p['column'])
        pos[p['id']] = (X0 + c * CW, Y0 + fill[c] * RH)
        fill[c] += 1
    SH, SW = Y0 + max(fill) * RH + 10, X0 + len(colnames) * CW

    def edge(a, b, cls):
        (ax, ay), (bx, by) = pos[a], pos[b]
        if ax == bx:
            x = ax + NW - 30 if by > ay else ax + 30
            return f'<path class="{cls}" d="M{x},{ay + NH if by > ay else ay} L{x},{by if by > ay else by + NH}" marker-end="url(#sarr)"/>'
        sx, tx = (ax + NW, bx) if bx > ax else (ax, bx + NW)
        mx = (sx + tx) / 2
        return f'<path class="{cls}" d="M{sx},{ay + NH / 2} C{mx},{ay + NH / 2} {mx},{by + NH / 2} {tx},{by + NH / 2}" marker-end="url(#sarr)"/>'
    nxt = {p['id']: list(dict.fromkeys(to for _, to in WF_BTN.findall(p.get('wireframe', '')) if to and to != p['id'])) for p in S['pages']}
    sm = [f'<svg class="smap" viewBox="0 0 {SW} {SH}" width="{SW}" role="img" aria-label="Sitemap">',
          '<defs><marker id="sarr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" class="sarrhead"/></marker></defs>']
    sm += [f'<rect class="scol" x="{X0 + i * CW - 10}" y="8" width="{CW - 20}" height="{SH - 14}" rx="8"/><text class="scolt" x="{X0 + i * CW}" y="34">{esc(c)}</text>' for i, c in enumerate(colnames)]
    sm += [edge(a, b, 'snav') for a in nxt for b in nxt[a]]
    sm += [edge(m['from_page'], m['to_page'], 'smail') for m in S.get('emails', [])]
    for p in S['pages']:
        x, y = pos[p['id']]
        go = f' href="#wf-{p["id"]}" data-go="wf-{p["id"]}"' if p.get('wireframe') else ''
        sm.append(f'<a{go}><g class="snode {p["status"]}"><rect x="{x}" y="{y}" width="{NW}" height="{NH}" rx="6"/>'
                  f'<text x="{x + 10}" y="{y + 22}" class="sid">{p["id"]}</text><text x="{x + 44}" y="{y + 22}" class="stitle">{esc(p["title"])}</text>'
                  f'<text x="{x + 10}" y="{y + 42}" class="surl">{esc(p["url"] if len(p["url"]) <= 28 else p["url"][:27] + "…")}</text></g></a>')
    sm.append('</svg>')
    kind = lambda p: f'<span class="kind {"new" if p["status"] == "new" else ""}">{ {"new": "ใหม่", "changed": "แก้", "old": "เดิม"}[p["status"]] }{" · " + esc(p["status_note"]) if p.get("status_note") else ""}</span>'
    live = [p for p in S['pages'] if p.get('wireframe')]
    sm_rows = ''.join(f'<tr><td><a class="pid" href="#wf-{p["id"]}" data-go="wf-{p["id"]}">{p["id"]}</a></td><td><b>{esc(p["title"])}</b><div class="mono">{esc(p["url"])}</div></td>'
                      f'<td>{kind(p)}</td><td>{esc(p["purpose"])}</td><td>{esc(p["role"])}</td><td>{esc(", ".join(f for f, _ in p.get("fields", [])))}</td>'
                      f'<td>{esc(", ".join(p.get("actions", [])))}</td><td>{", ".join(nxt[p["id"]])}</td><td>{" ".join(steplink(k) for k in used_in.get(p["id"], []))}</td></tr>' for p in live)
    mails = S.get('emails', [])
    mail_rows = ''.join(f'<tr><td><b>{m["id"]}</b></td><td>{esc(m["to"])}</td><td>{esc(m["when"])}</td><td>{esc(m["content"])}</td>'
                        f'<td>{m["from_page"]} → {m["to_page"]}</td><td>{steplink(m["step"]) if m.get("step") else "–"}</td></tr>' for m in mails)
    oos = S.get('out_of_scope', [])
    sitemap = ('<section class="pane" id="sitemap" role="tabpanel" hidden><div class="card"><h3>แผนผังหน้า</h3>'
               '<div class="legend"><span><i style="border:2px solid var(--accent)"></i>หน้าใหม่</span><span><i style="border:1.2px solid var(--ink)"></i>หน้าเดิมที่ต้องแก้</span>'
               '<span><i style="border:1.2px dashed var(--ink)"></i>หน้าเดิมไม่แก้</span><span><i style="border-top:2px solid var(--ink);height:0"></i>กดไปต่อ</span>'
               '<span><i style="border-top:2px dashed var(--muted);height:0"></i>ส่งต่อทาง email</span></div>'
               f'<div class="smapwrap">{"".join(sm)}</div></div>'
               f'<div class="card"><h3>ตารางหน้า ({len(live)} หน้า)</h3><div class="tablewrap"><table><tr><th>#</th><th>หน้า</th><th>ใหม่/แก้</th><th>ทำไมมีหน้านี้</th><th>ใครใช้</th><th>ข้อมูล</th><th>ทำอะไรได้</th><th>ไปต่อ</th><th>ขั้นใน flow</th></tr>{sm_rows}</table></div></div>'
               + (f'<div class="card"><h3>Email ({len(mails)} ฉบับ)</h3><div class="tablewrap"><table><tr><th>#</th><th>ถึง</th><th>เมื่อ</th><th>มีอะไร</th><th>จาก → ไป</th><th>ขั้นใน flow</th></tr>{mail_rows}</table></div></div>' if mails else '')
               + fb(fp, 'sitemap', 'ต้องแก้อะไรใน sitemap')
               + (f'<p class="meta">ไม่อยู่ในรอบนี้: {esc(", ".join(oos))}</p>' if oos else '') + '</section>')

    # screens: low-fi browser frame + spec panel per page
    def wbtn(m):
        lab, to = esc(m.group(1)), m.group(2)
        return f'<a class="wbtn" href="#wf-{to}" data-go="wf-{to}">{lab}</a>' if to else f'<span class="wbtn">{lab}</span>'

    def screen(p):
        side = ''
        if p['role'] in S.get('sidebars', {}):
            side = '<div class="wside">' + ''.join(f'<span class="{"on" if n == p.get("menu") else ""}">{esc(n)}</span>' for n in S['sidebars'][p['role']]) + '</div>'
        frame = (f'<div class="browser"><div class="bbar"><span class="dots">● ● ●</span><span class="burl">{esc(S.get("host", ""))}{esc(p["url"].replace(":id", "…"))}</span></div>'
                 f'<div class="bbody{" withside" if side else ""}">{side}<div class="wmain">{WF_BTN.sub(wbtn, p["wireframe"])}</div></div></div>')
        fields = ''.join(f'<tr><td><b>{esc(f)}</b></td><td>{esc(d)}</td></tr>' for f, d in p.get('fields', []))
        em = ' '.join(f'<span class="chip">{m["id"]}</span>' for m in mails if m['from_page'] == p['id'])
        panel = (f'<aside class="spec"><div class="spec-h"><span class="pid">{p["id"]}</span><div><b>{esc(p["title"])}</b><div class="mono">{esc(p["url"])}</div></div></div>'
                 f'<dl><dt>ทำไมมีหน้านี้</dt><dd>{esc(p["purpose"])}</dd><dt>ใครใช้</dt><dd>{esc(p["role"])} · {kind(p)}</dd>'
                 + (f'<dt>ช่องข้อมูล</dt><dd><table class="ftab"><tr><th>ช่อง</th><th>คำอธิบาย</th></tr>{fields}</table></dd>' if fields else '')
                 + (f'<dt>ทำอะไรได้</dt><dd>{esc(", ".join(p["actions"]))}</dd>' if p.get('actions') else '')
                 + (f'<dt>ไปหน้าถัดไป</dt><dd>{" ".join(chip(n) for n in nxt[p["id"]])} {em}</dd>' if nxt[p['id']] or em else '')
                 + (f'<dt>ใช้ในขั้น</dt><dd>{" ".join(steplink(k) for k in used_in[p["id"]])}</dd>' if p['id'] in used_in else '')
                 + (f'<dt>กรณีพิเศษ</dt><dd><ul class="states">{"".join(f"<li>{esc(s)}</li>" for s in p["states"])}</ul></dd>' if p.get('states') else '')
                 + f'</dl>{fb(fp, "page-" + p["id"], "ต้องแก้อะไรในหน้านี้")}</aside>')
        return f'<div class="subpane" id="wf-{p["id"]}"><div class="wfwrap">{frame}{panel}</div></div>'
    order = sorted(live, key=lambda p: (p['id'][0], int(re.sub(r'\D', '', p['id']) or 0)))
    screens = (f'<section class="pane" id="screens" role="tabpanel" hidden><div class="subtabs" role="tablist">'
               + ''.join(f'<button type="button" data-sub="wf-{p["id"]}"><b>{p["id"]}</b> {esc(p["title"])}</button>' for p in order)
               + ''.join(screen(p) for p in order) + '</section>')

    # baseline
    base = S.get('baseline', [])
    stats = ''.join(f'<div class="stat {s}"><span class="n">{sum(1 for b in base if b["status"] == s)}</span><span>{STATUS[s]}</span></div>'
                    for s in ['have', 'decided', 'extend', 'add', 'decide'])
    cards = ''.join(f'<div class="bcard {b["status"]}"><div class="bhead"><b>{esc(b["topic"])}</b><span class="pill {b["status"]}">{STATUS[b["status"]]}</span></div>'
                    f'<div class="bgrid"><div><small>ตอนนี้</small><p>{esc(b["now"])}</p></div><div><small>feature นี้ต้องการ</small><p>{esc(b["needed"])}</p></div></div>'
                    + (f'<div class="bfrom">{" ".join(steplink(k) for k in b["steps"])}</div>' if b.get('steps') else '') + '</div>' for b in base)
    tables = ''.join(f'<h3>{esc(t["title"])}</h3><div class="tablewrap"><table><tr><th>สถานะ</th><th>ปุ่ม</th><th>สถานะถัดไป</th><th>ใครกด</th><th>หมายเหตุ</th></tr>'
                     + ''.join(f'<tr><td>{esc(a)}</td><td><b>{esc(b)}</b></td><td>{esc(c)}</td><td>{esc(d)}</td><td>{esc(n)}</td></tr>' for a, b, c, d, n in t['rows'])
                     + '</table></div>' for t in S.get('state_tables', []))
    baseline = ('<section class="pane" id="baseline" role="tabpanel" hidden>'
                + (f'<p class="meta">เทียบกับโค้ดวันที่ {esc(S["baseline_date"])}</p>' if S.get('baseline_date') else '')
                + f'<div class="stats">{stats}</div><div class="bcards">{cards}</div>{tables}{fb(fp, "baseline", "ต้องแก้อะไรในพื้นฐานระบบ")}</section>')

    # what changed since the last version
    two = lambda title, head, rows: (f'<div class="card"><h3>{title}</h3><div class="tablewrap"><table><tr><th>อะไร</th><th>{head}</th></tr>'
                                     + ''.join(f'<tr><td><b>{esc(a)}</b></td><td>{esc(b)}</td></tr>' for a, b in rows) + '</table></div></div>') if rows else ''
    chg = two(f'{esc(S["version"])} เปลี่ยนอะไร', 'เปลี่ยนอย่างไร', S.get('changes', [])) + two('รอของ', 'สถานะ', S.get('pending', [])) + two('ตัดออกแล้ว', 'ทำไม', S.get('removed', []))
    changes = f'<section class="pane" id="changes" role="tabpanel" hidden>{chg}</section>' if chg else ''

    nav = (f'<button role="tab" data-tab="overview">ภาพรวม{badge("overview")}</button>'
           + ''.join(f'<button role="tab" data-tab="{c["id"]}"><span class="mono">{c["id"]}</span> {esc(c["title"])}{badge(c["id"])}</button>' for c in chs)
           + '<button role="tab" data-tab="sitemap">Sitemap</button><button role="tab" data-tab="screens">หน้าจอ</button>'
           + '<button role="tab" data-tab="baseline">พื้นฐานระบบ</button>'
           + (f'<button role="tab" data-tab="changes">{esc(S["version"])} เปลี่ยนอะไร</button>' if changes else ''))
    meta = ' · '.join(x for x in [esc(S.get('project', '')), esc(S['version']), esc(S.get('date', '')),
                                  f'flow: <span class="mono">{esc(S["flow_source"])}</span>' if S.get('flow_source') else ''] if x)
    out = (TEMPLATE.read_text(encoding='utf-8').replace('%TITLE%', esc(S['title'])).replace('%META%', meta).replace('%NAV%', nav)
           .replace('%PANES%', overview + ''.join(panes) + sitemap + screens + baseline + changes))
    # box numbers and table numbers come from the same numbering; assert the page agrees before shipping it
    for ch in chs:
        boxes = re.findall(rf'<g class="go"[^>]*data-step="({ch["id"]}-[^"]+)"', out)
        rows = re.findall(rf'<tr data-step="({ch["id"]}-[^"]+)"', out)
        assert sorted(boxes) == sorted(rows) and len(boxes) == len(flows[ch['id']]), f'{ch["id"]}: flow boxes and step table differ'
    return out


def main(argv):
    if len(argv) != 4:
        sys.exit(__doc__)
    spec = json.loads(Path(argv[1]).read_text(encoding='utf-8'))
    S = json.loads(Path(argv[2]).read_text(encoding='utf-8'))
    bad = gate(chapters_of(spec), S)
    if bad:
        print(f'REFUSED: {len(bad)} problem(s), nothing written', *bad, sep='\n  ')
        return 1
    Path(argv[3]).write_text(build(spec, S), encoding='utf-8')
    print(f'ok {argv[3]}')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
