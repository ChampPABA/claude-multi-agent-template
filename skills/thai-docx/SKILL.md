---
name: thai-docx
description: >-
  Fix broken Thai rendering in Word (.docx) files generated with python-docx.
  Use this WHENEVER you create, edit, or generate a .docx that contains Thai text
  (สัญญา, คำให้การ, บันทึก, เอกสารราชการ, TH Sarabun New, ภาษาไทยใน Word), or when a
  Thai .docx looks wrong in Microsoft Word: Thai font shrinks while English stays
  big, bold/italic does not apply to Thai, tone marks/vowels (วรรณยุกต์/สระ) float
  off the consonant, justified Thai stretches characters apart, or the person
  editing it later sees boxes under ¶ / Shift+Enter jumps a whole line. Also use
  for Thai university reports in the DPU APA 7th format (มหาวิทยาลัยธุรกิจบัณฑิตย์,
  รายงาน/ภาคนิพนธ์ APA7), and to QA-verify a generated Thai .docx before sending it.
  python-docx alone produces Thai that breaks in real Word even when it looks fine
  in the preview or LibreOffice, so reach for this skill any time Thai + Word + a
  generated document are involved, even if the user does not name the problem.
---

# thai-docx

Make python-docx output render Thai correctly in **Microsoft Word** (where the
reader actually opens it), not just in the preview.

## Why Thai breaks (read this once)

Word chooses a font **per character**, using several "font slots" inside a single
run. Latin text uses the **ascii/hAnsi** slot; Thai (a *complex script*) uses the
**Complex Script (cs)** slot. python-docx only ever fills the Latin slot — it sets
`w:ascii`/`w:hAnsi`/`w:sz` and leaves the cs side (`w:cs`, `w:szCs`, `w:bCs`,
`w:iCs`, `w:lang/@w:bidi`) empty. So the Thai half of every run falls back, which
is exactly these symptoms:

| Symptom | Empty cs property | What Word does |
|---|---|---|
| Thai shrinks (~10pt) while English is 16pt | `w:szCs` | size applies to Latin only |
| Bold/italic doesn't stick to Thai | `w:bCs` / `w:iCs` | weight applies to Latin only |
| วรรณยุกต์/สระ float off the consonant | `w:rFonts/@w:cs` | falls back to a font with no Thai mark positioning |
| Lines break mid-word | `w:lang/@w:bidi` | no Thai dictionary for line breaking |
| Lines end ~60% full, Thai Distributed stretches them letter by letter | `<w:cs/>` on the run | Word skips its Thai word breaker and breaks only at real spaces |

**The preview lies.** Word's own preview and LibreOffice silently guess a Thai
font when the cs slot is empty, so the document looks fine there and breaks on the
reader's real Microsoft Word. Never sign off from a screenshot. Verify the XML
with the scanner (below).

## The fix: one call before save

```python
from docx import Document
import sys; sys.path.insert(0, '<skill>/scripts')
from thai_docx import enforce_thai

doc = Document()
# ... build the document normally with python-docx ...
enforce_thai(doc)          # fills every Thai (cs) slot + Thai-Distributed body (default)
doc.save('out.docx')
```

**Default alignment = Thai Distributed (กระจายแบบไทย).** A bare `enforce_thai(doc)`
distributes body paragraphs (`w:jc='thaiDistribute'`), which is
the ราชการ norm and renders beautifully in **real Microsoft Word**. For a plainly
left-aligned document pass `enforce_thai(doc, distribute=False)`. Headings, centred
titles and signatures keep their own alignment either way, and **table cells are never
distributed**: a narrow cell holds only a few words a line, so distribution would push
them far apart (the ห่าง look); cells stay ชิดซ้าย or whatever alignment you set on
them yourself.

> ⚠️ **thaiDistribute is a Word-only feature.** LibreOffice, Google Docs and previews
> render it as plain **left-aligned** (ชิดซ้าย) — that is the viewer's limitation, not
> a bug in the file. Judge alignment only in real Microsoft Word.

`enforce_thai(doc)` walks every run (body, tables, nested tables, text boxes,
headers, footers, footnotes), every style, the document defaults, `settings.xml`
and the theme, and sets the complex-script properties.

**Defaults = the ราชการ standard, so a bare `enforce_thai(doc)` is normally all you need:**

| | default | opt out with |
|---|---|---|
| Font | TH Sarabun New (Thai + Latin) | `thai_font=`, `latin_font=` |
| Size | **16pt on everything, headings included** (they differ by weight, not size) | `uniform=False` → each heading keeps its own size |
| Page | **A4, margins ซ้าย 3 / ขวา 2 / บน 2.5 / ล่าง 2 ซม.** (python-docx would emit US Letter) | `page=False` |
| Alignment | Thai Distributed on body paragraphs (table cells stay ชิดซ้าย) | `distribute=False` → ชิดซ้าย |
| Word breaks | `<w:cs/>` on every Thai run, so Word breaks Thai itself; break points inside long URLs only | — (see below) |
| Layout | ราชการ | `style="dpu-apa7"` → DPU APA 7th report (see below) |

### The invariant behind `uniform=False`

With `uniform=False`, `enforce_thai` never resizes text it did not size itself:

- **Font (`w:cs`) and language (`w:lang/@w:bidi`): set everywhere.** Always safe.
- **Size (`w:szCs`): only mirror where an explicit `w:sz` already exists.** A run
  or style with no size of its own *inherits* from its paragraph style (e.g. a
  Heading). Forcing a body-size `szCs` onto it would shrink the heading. So:
  no `w:sz` → no `w:szCs`, and the heading scales from its style. The 16pt base is
  set once at the document defaults, where unspecified text picks it up.
- **Bold/italic (`w:bCs`/`w:iCs`): only mirror where `w:b`/`w:i` exists**, copying
  the on/off value so Thai weight matches Latin exactly.

### Common options

```python
# Plain left-aligned (ชิดซ้าย) instead of Thai Distributed:
enforce_thai(doc, distribute=False)

# Keep each heading's own size instead of flattening everything to 16pt:
enforce_thai(doc, uniform=False)

# Leave the document's existing page size/margins alone:
enforce_thai(doc, page=False)

# Another Thai font / size:
enforce_thai(doc, thai_font="TH SarabunPSK", size_pt=14)
```

`latin_font=` only reaches runs with **no Thai in them**. A run that holds Thai is
flagged `<w:cs/>`, and Word then draws every character in it, English included, in
the Thai font. Keep one font for the whole document (the default) unless you put
English in runs of its own.

### Word breaks: `<w:cs/>`, not zero-width spaces

When a person types Thai, Word marks each Thai run `<w:cs/>` ("complex-script
run"). That flag is what switches on Word's own Thai word breaker. python-docx never
writes it, so a generated run breaks only at real spaces: lines end ~60% full and
Thai Distributed stretches them wide. `enforce_thai` adds `<w:cs/>` to every run
that contains Thai. It was checked in Word 365 on a machine with **no** Thai editing
language: the same 35-page report laid out identically to a zero-width-space version
(and 37 stretched pages without either).

Do **not** insert U+200B between Thai words (an older version of this skill did).
It gives the same layout, but the file stops behaving like a Word file: every break
shows as a box once ¶ is on, and Shift+Enter (the Thai editor's habit of pushing a
split word down while the line above stays distributed) jumps a whole line.
Leave `w:doNotExpandShiftReturn` out for the same reason: Word's default stretches
the line before a Shift+Enter, and that is exactly what Thai editors rely on.

Word cannot break inside a URL, so the line before a long URL would stretch letter
by letter. `enforce_thai` puts zero-width break points inside long URLs, paths and
e-mails (non-Thai tokens over 15 chars that contain `/` or `@`) and nowhere else.

## DPU APA 7th reports: `style="dpu-apa7"`

```python
enforce_thai(doc, style="dpu-apa7")
```

For reports in the Dhurakij Pundit University APA 7th format. On top of the Thai
fixes it sets:

- **Page:** A4, margins 2.54 cm all round, no gutter.
- **Spacing:** single spacing, 0 pt before and after, on every style.
- **Headings:**
  - `Title` / `Heading 1` (cover, "บทที่ N" + chapter title): 20pt bold, centred.
  - `Heading 2` (X.Y): 16pt bold, left.
  - `Heading 3`+: 16pt regular.
  - Heading colour and the Title rule are removed.
- **Captions and footnotes:** `Caption` 16pt bold; `Footnote Text` 14pt.
- **Body:** Thai Distributed, first-line indent 0.6 in. Paragraphs that already
  have an indent are left alone, and so are centred lines, lists and table cells.
- **Page number:** a `PAGE` field top right, header 1.25 cm from the edge, hidden on
  each section's first page.

The rest is **structure the builder writes**, because only the builder knows which
paragraph is what:

- **Sections decide where the number is hidden** (the first page of every section):
  - Cover and all front matter go in **one** section, split by page breaks.
    Then only the cover hides its number (it still counts as ก).
  - Each chapter starts its own section: `doc.add_section(WD_SECTION.NEW_PAGE)`.
    Its first page is counted but shows no number.
  - Don't start a new section for คำนำ, สารบัญ, บรรณานุกรม or ภาคผนวก: use a page
    break instead, or their first page loses its number too (DPU shows it).
- **Front matter numbering:** use Thai letters, then restart at 1 for chapter 1.
  - Front matter order: ปก → บทคัดย่อ → กิตติกรรมประกาศ → สารบัญ (→ สารบัญตาราง/ภาพ).
  - Use the `page_numbering` helper, which puts the setting where Word expects it:

  ```python
  from thai_docx import page_numbering
  page_numbering(doc.sections[0], 'thaiLetters')           # front matter: ก ข ค
  page_numbering(chapter1_section, 'decimal', start=1)     # body: 1 2 3
  ```
- **Numbered headings:** X.Y is `Heading 2`, X.Y.Z is `Heading 3`, then (1), (1.1).
  Indent each lower level one more tab stop: 0.6, 0.85, 1.1, 1.35 in and so on.
- **Tables and figures:**
  - "ตารางที่ X.Y" / "ภาพที่ X.Y" in bold (`Caption` style) goes **above**.
  - The title goes on the next line, in italic.
  - "ที่มา:" goes **below**.
  - A table that runs onto a new page is headed "ตารางที่ X.Y (ต่อ)" and repeats its header row.
- **Block quote (over 40 words):** left indent 0.5 in, first line a further 0.5 in, quotation marks kept.
- **บรรณานุกรม:**
  - New page. Title centred 16pt bold; overflow pages are headed "บรรณานุกรม (ต่อ)".
  - Thai entries first (ก–ฮ), then English (A–Z).
  - Hanging indent 0.6 in: `ind left=864 hanging=864` twips.
  - Book and journal titles and journal volume numbers in italic.

## QA scanner: trust this, not the preview

After saving, always run the scanner. It reads the raw OOXML and flags any Thai
run whose cs slot is unset or that lacks `<w:cs/>`, plus a missing `themeFontLang`.

```bash
python <skill>/scripts/verify_thai_docx.py out.docx
```

Exit code **0 = clean, safe to send**; **1 = defects found** (prints each run, the
missing property, and the symptom it will cause). Wire it into CI or run it by
hand — it is the source of truth, because the preview hides these defects.

## Dependencies

- `python-docx` — the only dependency.

## Scope

This skill's job is to convert **already-written** Thai text into a .docx that
renders faithfully in Microsoft Word. It touches **font and rendering properties
only** — `enforce_thai` does not alter a single character of the text (the one
exception: invisible break points inside long URLs). It
does not clean, rewrite, or check the source text, and it does not write or review
legal content. Every generated document is a **draft** — the wording of a
contract, คำให้การ, or บันทึกความเห็น is drafted and reviewed by a person.
