---
name: ifcg-doc
description: >-
  Rewrite an IFCG Thai document (ระเบียบ/ข้อบังคับ, วาระเสนอคณะกรรมการ, ประกาศ,
  บันทึกภายใน) into the approved IFCG wording and layout and hand back a Word .docx
  with Thai Distributed (กระจายแบบไทย) body text, Noto Sans Thai and A4. Use this
  whenever someone at IFCG (บริษัท ไอเอฟซีจี จำกัด (มหาชน)) pastes or uploads a Thai
  draft and wants it cleaned up, formatted, "จัดหน้าให้", "แก้ภาษาให้เป็นทางการ",
  "ทำเป็น docx", "ทำวาระเข้าบอร์ด", or types /ifcg-doc, even if they do not say
  "docx" or "skill". Works in the Gemini app and in Claude.
---

# ifcg-doc

The result is a .docx, never a Google Doc: Docs has no Thai Distributed alignment.

## Steps

Two turns: the user approves the wording before any file is made, because fixing
a word in chat is cheaper than rebuilding the .docx.

1. Rewrite the draft in the style below. Missing facts (date, signer) become a
   visible `[ระบุ...]`; never fill them in yourself.
2. Reply in Thai with only what changed, not the full text (a ระเบียบ runs to 80+ ข้อ
   and unchanged ข้อ read as in the draft): a table ข้อ / เดิม / ใหม่ / เหตุผล, then
   "ควรตรวจ" (looks wrong but left as written) and the `[ระบุ...]` blanks to fill.
   End with "ตอบ ok เพื่อสร้างไฟล์ หรือบอกจุดที่อยากแก้" and stop. If the user
   asked for the file straight away ("ทำไฟล์เลย"), skip this step.
3. After ok, or after applying their edits: the page design (logo, address, background
   pattern, embedded font) lives in `IFCG-letterhead.docx` (`assets/` of this skill).
   It must be attached to the chat or in the working folder; if it isn't, ask for it.
   Claude: set `TEMPLATE` to the file in `assets/`.
4. Put the approved text in `CONTENT` (one entry per paragraph, kinds in "Layout")
   and run the code block under "Build the .docx" with only `OUTPUT`, `TEMPLATE` and
   `CONTENT` changed. The rest writes the Thai settings Word needs; a rewritten
   version drops some and the reader sees stretched lines or a shrunken Thai font.
   If a check at the end fails, fix `CONTENT` and run again; keep the checks.
5. Reply with the file. Say to open it in Microsoft Word; Google Docs shows Thai
   Distributed as left-aligned.

## Wording: the IFCG style

A style for any topic, not a template. Examples are Champ's own edits.

- **Substance stays exact.** Numbers, dates, units ("6 วันทำงาน"), names, ข้อ and
  มาตรา references are not changed. A clause that looks wrong, duplicated, or
  unclear enough that fixing it means guessing what it meant stays as written and
  goes in "ควรตรวจ"; in a ระเบียบ a guessed meaning becomes the rule.
- **One item, one paragraph.** Join sentences the author broke with Enter to make a
  line end on screen; Word wraps by itself and the manual break leaves half-lines.
- **Short, plain, formal.** Cut filler and add the missing joining word:
  "สามารถที่บริหารจัดการเวลาการทำงานที่มีความเหมาะสมสถานการณ์" →
  "สามารถบริหารจัดการเวลาการทำงานให้มีความเหมาะสมกับสถานการณ์".
  Shortest official form: "388 อาคารอามีโก้ทาวเวอร์ ชั้น 19 บี", not
  "ห้องเลขที่ โซนบี/2 ชั้นที่ 19".
- **Same thing, same word.** "บริษัทฯ" after the first full name, every time; one
  term per role and per unit through the whole document.
- **No AI or sales tone.** No em-dash (—), emoji, or hype ("ยกระดับ", "อย่างไร้รอยต่อ",
  "ขับเคลื่อน", "ความเป็นเลิศ"). Thai terms over English (HR → ฝ่ายทรัพยากรบุคคล,
  ซีอีโอ → ประธานเจ้าหน้าที่บริหาร).
- **Lists.** Bold label with a colon: "**ความสอดคล้องกับกฎหมายแรงงาน:** ...".
  Section numbers run without gaps.

## Layout

| kind | use for |
|---|---|
| `field` | "เรื่อง ...", "เรียน ...", "อ้างถึง ...": bold label, text lined up after it |
| `title` | document title |
| `subtitle` | second title line: English title, company name, "เรื่อง ..." of a ประกาศ |
| `heading` | section heading inside the document ("ก. การทดลองปฏิบัติงาน", "การลากิจ"), centred |
| `topic` | numbered section of a วาระ or บันทึก ("1. วัตถุประสงค์") |
| `para` | numbered item ("13. ...") and any body paragraph |
| `sub` | one level in: "13.1 ...", หมายเหตุ, text under a `topic` |
| `item` | numbered or dashed list line under a `topic` ("1. **ป้ายกำกับ:** ...", "- ...") |
| `center` | approval sentence, date line, signer "(นาย...)", position |
| `table` | `("table", [[header...], [row...]])` |
| `pagebreak` | `("pagebreak", "")` |

`**...**` inside text makes it bold.

IFCG shapes (adapt to the content):

- **ประกาศ:** `title` "ประกาศบริษัท ไอเอฟซีจี จำกัด (มหาชน)" → `subtitle` "เรื่อง ..."
  → `para` → `para` "จึงประกาศมาเพื่อทราบโดยทั่วกัน" → `center` "ประกาศ ณ วันที่ ..."
  → `center` signer → `center` position.
- **ระเบียบ:** `title` → `subtitle` English title, company → `para` สถานที่ตั้ง,
  ประเภทกิจการ → `heading` คำนำ → per หมวด and sub-topic a `heading`, per ข้อ a
  `para`, per ข้อย่อย a `sub` → `center` approval sentence → one signer, the
  approver, with นาย/นาง/นางสาว.
- **วาระเสนอคณะกรรมการ:** `field` "เรื่อง ..." → `field` "เรียน ประธานกรรมการ
  และคณะกรรมการบริษัท ไอเอฟซีจี จำกัด (มหาชน)" → `topic` + `sub` / `item`: 1. วัตถุประสงค์,
  2. หลักการและเหตุผล, 3. รายละเอียด (`table`: ลำดับ | หมวดหมู่/ข้อ | ข้อความเดิม |
  ข้อความใหม่ที่ขอเสนอแก้ไข | เหตุผล/ความจำเป็น), 4. ผลกระทบและประโยชน์ที่คาดว่าจะได้รับ,
  5. ข้อเสนอเพื่อพิจารณา ending "จึงเรียนมาเพื่อโปรดพิจารณา". A full text that follows
  starts after a `pagebreak`.

## Build the .docx

Needs only `python-docx`.

```python
# ===== 1) Fill in =====
OUTPUT = "ifcg_document.docx"
TEMPLATE = ""  # path to IFCG-letterhead.docx; leave "" to search the working folders
CONTENT = [
    ("field", "เรื่อง ขออนุมัติแก้ไขเปลี่ยนแปลงระเบียบและข้อบังคับการทำงาน"),
    ("field", "เรียน ประธานกรรมการ และคณะกรรมการบริษัท ไอเอฟซีจี จำกัด (มหาชน)"),
    ("topic", "1. วัตถุประสงค์"),
    ("sub", "เพื่อนำเสนอให้คณะกรรมการบริษัทพิจารณาและอนุมัติ..."),
    ("item", "1. **ความสอดคล้องกับกฎหมายแรงงาน:** มีข้อกำหนดบางประการ..."),
    ("table", [["ลำดับ", "หมวดหมู่/ข้อ", "ข้อความเดิม", "ข้อความใหม่ที่ขอเสนอแก้ไข", "เหตุผล/ความจำเป็น"],
               ["1.", "คำนำ", "...", "...", "..."]]),
    ("pagebreak", ""),
    ("title", "ระเบียบและข้อบังคับการทำงาน"),
    ("heading", "ก. การทดลองปฏิบัติงาน"),
    ("para", "1. ผู้สมัครซึ่งได้รับคัดเลือกเข้าเป็นพนักงานต้องทดลองปฏิบัติงานเป็นระยะเวลา 119 วัน"),
    ("sub", "1.1 เงินเดือนซึ่งจะจ่ายให้ถึงวันที่เลิกจ้าง"),
    ("center", "(นายวิทูร เลิศพนมวรรณ)"),
]

# ===== 2) Do not change below this line =====
import glob, re, zipfile
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

FONT, INK, FILL = "Noto Sans Thai", "1F1F1F", "C6D9F1"
THAI = re.compile("[฀-๿]")
MARK = re.compile(r"^(\d+(?:\.\d+)*\.?|[-•]|\(\d+\)|\d+\)|[ก-ฮ]\.)\s+(.*)$", re.S)  # "1." "1.1" "-" "ก."
STYLE = {  # kind: (align, size, bold, left cm, hanging cm, space before pt)
    "title": ("center", 14, True, 0, 0, 0), "subtitle": ("center", 12, True, 0, 0, 0),
    "heading": ("center", 12, True, 0, 0, 12), "field": ("thaiDistribute", 12, False, 1.27, 1.27, 0),
    "topic": ("left", 12, True, 1.27, 0.635, 12), "para": ("thaiDistribute", 12, False, 0, 0, 0),
    "sub": ("thaiDistribute", 12, False, 1.27, 0, 0), "item": ("thaiDistribute", 12, False, 1.9, 0.635, 0),
    "center": ("center", 12, False, 0, 0, 0),
}

def el(tag, **attrs):
    e = OxmlElement(tag)
    for k, v in attrs.items():
        e.set(qn(k), v)
    return e

def add_run(p, text, size, bold):
    r = p.add_run(text)
    rPr = r._r.get_or_add_rPr()  # children in schema order: rFonts b bCs color sz szCs cs lang
    rPr.append(el("w:rFonts", **{"w:ascii": FONT, "w:hAnsi": FONT, "w:eastAsia": FONT, "w:cs": FONT}))
    if bold:
        rPr.append(el("w:b")); rPr.append(el("w:bCs"))
    rPr.append(el("w:color", **{"w:val": INK}))
    rPr.append(el("w:sz", **{"w:val": str(size * 2)})); rPr.append(el("w:szCs", **{"w:val": str(size * 2)}))
    if THAI.search(text):
        rPr.append(el("w:cs"))  # turns on Word's Thai word breaker; without it lines stretch
    rPr.append(el("w:lang", **{"w:val": "en-US", "w:bidi": "th-TH"}))

def add_text(p, text, size, bold):
    for i, part in enumerate(text.split("**")):  # **bold** segments
        if part:
            add_run(p, part, size, bold or i % 2 == 1)

def fmt(p, align, left=0, hanging=0, before=0):
    f = p.paragraph_format
    f.space_before, f.space_after, f.line_spacing = Pt(before), Pt(0), 1.0
    f.left_indent, f.first_line_indent = Cm(left), Cm(-hanging)
    p._p.get_or_add_pPr().get_or_add_jc().set(qn("w:val"), align)

def add_table(doc, rows):
    cols = max(len(r) for r in rows)
    rows = [list(r) + [""] * (cols - len(r)) for r in rows]  # pad short rows
    fmt(doc.add_paragraph(), "left")  # blank line before the table
    t = doc.add_table(rows=len(rows), cols=cols)
    t.style, t.autofit = "Table Grid", False
    mar = el("w:tblCellMar")  # keep text off the cell borders
    for side in ("left", "right"):
        mar.append(el(f"w:{side}", **{"w:w": "85", "w:type": "dxa"}))
    look = t._tbl.tblPr.find(qn("w:tblLook"))  # schema order: tblCellMar comes before tblLook
    look.addprevious(mar) if look is not None else t._tbl.tblPr.append(mar)
    base = lambda s: len(re.sub("[\u0E31\u0E34-\u0E3A\u0E47-\u0E4E]", "", s))  # marks above/below take no width
    least = [0.24 * max(base(w) for w in re.split(r"(?<=/)|\s+", str(rows[0][j]))) + 0.4 for j in range(cols)]
    longest = [max(1, max(len(str(r[j])) for r in rows[1:] or rows)) for j in range(cols)]
    spare = max(0, 15.9 - sum(least))  # header words never break; the rest goes to the longer columns
    widths = [a + spare * n / sum(longest) for a, n in zip(least, longest)]
    widths = [w * 15.9 / sum(widths) for w in widths]
    t.rows[0]._tr.get_or_add_trPr().append(el("w:tblHeader"))  # header row repeats on every page
    for j, w in enumerate(widths):
        t.columns[j].width = Cm(w)
    for i, row in enumerate(rows):
        for j, text in enumerate(row):
            cell = t.cell(i, j)
            cell.width = Cm(widths[j])
            p = cell.paragraphs[0]
            fmt(p, "center" if i == 0 or j == 0 else "left")  # never distribute a narrow cell
            add_text(p, str(text), 12, i == 0)
            if i == 0:
                tcPr = cell._tc.get_or_add_tcPr()
                tcPr.append(el("w:shd", **{"w:val": "clear", "w:color": "auto", "w:fill": FILL}))
                tcPr.append(el("w:vAlign", **{"w:val": "center"}))
    fmt(doc.add_paragraph(), "left")

if not TEMPLATE:
    found = sorted(glob.glob("**/IFCG-letterhead*.docx", recursive=True) + glob.glob("/mnt/data/IFCG-letterhead*.docx"))
    TEMPLATE = found[0] if found else ""
assert TEMPLATE, "ไม่พบไฟล์หัวกระดาษ IFCG-letterhead.docx: ขอให้ผู้ใช้แนบไฟล์นี้มาด้วย"
doc = Document(TEMPLATE)  # logo, address, background pattern and embedded Noto Sans Thai come from here
for child in list(doc.element.body):
    if child.tag != qn("w:sectPr"):
        doc.element.body.remove(child)
lang = doc.settings.element.find(qn("w:themeFontLang"))
if lang is None:
    lang = el("w:themeFontLang"); doc.settings.element.append(lang)
lang.set(qn("w:bidi"), "th-TH")  # Word uses its Thai dictionary for line breaks

prev = None
for kind, value in CONTENT:
    if kind == "table":
        add_table(doc, value)
        continue
    if kind == "pagebreak":
        doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
        continue
    assert "\n" not in value, f"one paragraph per entry, no Enter inside: {value[:40]}"
    align, size, bold, left, hanging, before = STYLE[kind]
    first = len(doc.paragraphs) == 0
    p = doc.add_paragraph()
    if first:
        before = 30  # first line clears the logo
    elif kind == "center" and prev != "center":
        before = 18  # gap above a signature or approval block
    fmt(p, align, left, hanging, before)
    prev = kind
    p.paragraph_format.keep_with_next = kind in ("title", "subtitle", "heading", "topic")
    m = MARK.match(value)
    if kind == "field":  # bold label, then the text lines up after it
        label, _, rest = value.partition(" ")
        add_run(p, label.strip("*"), size, True); p.add_run("\t"); add_text(p, rest, size, bold)
    elif kind in ("topic", "item") and m:  # number hangs, wrapped lines align with the text
        add_text(p, m.group(1), size, bold or m.group(2).startswith("**")); p.add_run("\t"); add_text(p, m.group(2), size, bold)
    else:
        add_text(p, value, size, bold)
doc.save(OUTPUT)

# ===== 3) Self-check: the saved file really has the Thai settings and the letterhead =====
z = zipfile.ZipFile(OUTPUT)
xml = z.read("word/document.xml").decode("utf8")
runs = [r for r in re.findall(r"<w:r>.*?</w:r>", xml, re.S) if THAI.search(r)]
assert runs and all("<w:cs/>" in r and 'w:cs="Noto Sans Thai"' in r and "<w:szCs " in r for r in runs), "Thai run missing settings"
if any(k in ("para", "sub", "item") for k, _ in CONTENT):
    assert 'w:jc w:val="thaiDistribute"' in xml, "no Thai Distributed paragraph"
assert not re.search(r"<w:tc>(?:(?!</w:tc>).)*thaiDistribute", xml, re.S), "table cell distributed"
w, h = map(int, re.search(r'<w:pgSz w:w="(\d+)" w:h="(\d+)"', xml).groups())
assert abs(w - 11906) < 10 and abs(h - 16838) < 10, "page is not A4"
assert any(n.startswith("word/media/") for n in z.namelist()) and "headerReference" in xml, "letterhead missing"
assert 'w:bidi="th-TH"' in z.read("word/settings.xml").decode("utf8"), "settings lack Thai"
print("ตรวจไฟล์ผ่าน:", OUTPUT, "| ย่อหน้าภาษาไทย", len(runs), "run")
```
