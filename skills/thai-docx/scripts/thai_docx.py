"""thai_docx — make python-docx output render Thai correctly in Microsoft Word.

Word picks a font PER CHARACTER using several "font slots" inside one run: Latin
text uses the ascii/hAnsi slot, Thai uses the Complex Script (cs) slot. python-docx
only ever fills the Latin slot, so Thai falls back and breaks: it shrinks, bold
won't stick, and tone marks/vowels float off the consonant.

`enforce_thai(doc)` fills the cs slot (and the matching cs size/bold/italic/lang)
across every run, style, the document defaults, settings and theme, so the Thai
slot always carries the same intent as the Latin one.

Core invariant — what is safe to set where:
  * FONT (rFonts/@w:cs) and LANGUAGE (w:lang/@w:bidi): safe to set EVERYWHERE.
  * SIZE (w:szCs): only mirror it where an explicit w:sz already exists. A run/style
    with no size of its own inherits from its style (e.g. a Heading); forcing a
    body-size szCs onto it would shrink the heading. So: no sz -> no szCs.
  * BOLD/ITALIC (w:bCs/@val, w:iCs/@val): only mirror where w:b / w:i exists, and
    copy its on/off value so Thai matches the Latin weight exactly.
"""

from docx.oxml.ns import qn
from docx.oxml import OxmlElement

DEFAULT_THAI_FONT = "TH Sarabun New"
DEFAULT_SIZE_PT = 16

# Child order of w:rPr (CT_RPr). Used to insert elements python-docx has no
# get_or_add_* accessor for (w:szCs, w:lang) at a schema-valid position, so Word
# does not flag the document as corrupt.
_SZCS_SUCCESSORS = ('w:highlight', 'w:u', 'w:effect', 'w:bdr', 'w:shd', 'w:fitText',
                    'w:vertAlign', 'w:rtl', 'w:cs', 'w:em', 'w:lang',
                    'w:eastAsianLayout', 'w:specVanish', 'w:oMath')
_LANG_SUCCESSORS = ('w:eastAsianLayout', 'w:specVanish', 'w:oMath')
_CS_SUCCESSORS = ('w:em', 'w:lang') + _LANG_SUCCESSORS


def _get_or_insert(rPr, tag, successors):
    el = rPr.find(qn(tag))
    if el is None:
        el = OxmlElement(tag)
        rPr.insert_element_before(el, *successors)
    return el


def _apply_rpr(rPr, *, thai_font, latin_font, thai_hp, latin_hp, lang,
               force_size, mirror_toggles, base_size=None):
    """Apply complex-script properties to a w:rPr element.

    force_size: set sz/szCs unconditionally (use only for docDefaults, where a
        base size is wanted). Elsewhere pass False so szCs only mirrors an
        existing sz (heading-shrink guard).
    base_size: (latin_hp, thai_hp) to STAMP explicitly onto a run that has no size
        of its own. Used for plain body runs so the base size travels in the run
        itself, not only via docDefaults -- Word honours docDefaults, but many
        other viewers (the eval viewer, Google Docs, some LibreOffice paths) do
        NOT, and would otherwise show body text at their own default size. Pass
        None for heading/styled runs so they keep inheriting their style size.
    mirror_toggles: copy w:b -> w:bCs and w:i -> w:iCs (with their on/off value).
    """
    rFonts = rPr.get_or_add_rFonts()
    rFonts.set(qn('w:cs'), thai_font)
    rFonts.attrib.pop(qn('w:cstheme'), None)
    if latin_font:
        rFonts.set(qn('w:ascii'), latin_font)
        rFonts.set(qn('w:hAnsi'), latin_font)
        # A theme attribute beats the explicit font in Word, so python-docx's
        # Heading styles (asciiTheme="majorHAnsi") would show English in Cambria.
        rFonts.attrib.pop(qn('w:asciiTheme'), None)
        rFonts.attrib.pop(qn('w:hAnsiTheme'), None)

    # Language: safe everywhere.
    _get_or_insert(rPr, 'w:lang', _LANG_SUCCESSORS).set(qn('w:bidi'), lang)

    # Size.
    sz = rPr.find(qn('w:sz'))
    if force_size:
        if latin_hp is not None:
            (sz if sz is not None else rPr.get_or_add_sz()).set(qn('w:val'), str(latin_hp))
        _get_or_insert(rPr, 'w:szCs', _SZCS_SUCCESSORS).set(qn('w:val'), str(thai_hp))
    elif sz is not None:
        # Mirror this run/style's OWN Latin size onto the Thai slot 1:1, so Thai
        # matches the Latin size exactly here (e.g. a 14pt heading stays 14pt for
        # both scripts). The global base size only applies at docDefaults; using it
        # here would wrongly resize headings to the body size.
        _get_or_insert(rPr, 'w:szCs', _SZCS_SUCCESSORS).set(qn('w:val'),
                                                            sz.get(qn('w:val')))
    elif base_size is not None:
        # Plain body run with no size of its own: stamp the base size into the run
        # so every renderer shows it, not just the ones that honour docDefaults.
        lhp, thp = base_size
        rPr.get_or_add_sz().set(qn('w:val'), str(lhp))
        _get_or_insert(rPr, 'w:szCs', _SZCS_SUCCESSORS).set(qn('w:val'), str(thp))

    # Bold / italic: mirror presence AND value so Thai matches the Latin weight.
    if mirror_toggles:
        for src_tag, dst_tag, adder in (('w:b', 'w:bCs', rPr.get_or_add_bCs),
                                        ('w:i', 'w:iCs', rPr.get_or_add_iCs)):
            src = rPr.find(qn(src_tag))
            if src is not None:
                dst = adder()
                v = src.get(qn('w:val'))
                if v is None:
                    dst.attrib.pop(qn('w:val'), None)
                else:
                    dst.set(qn('w:val'), v)


def _is_plain_body_para(p):
    """True if a paragraph uses the default body style (no pStyle, or 'Normal'),
    i.e. plain body text that should carry the base size explicitly. Paragraphs
    with a named style (Heading 1, Title, a custom style...) are left to inherit
    that style's own size."""
    pPr = p.find(qn('w:pPr'))
    pStyle = pPr.find(qn('w:pStyle')) if pPr is not None else None
    return pStyle is None or pStyle.get(qn('w:val')) == 'Normal'


def _in_table(p):
    """True if the paragraph sits inside a table cell (nested tables included)."""
    return next(p.iterancestors(qn('w:tc')), None) is not None


def _set_thai_distribute(p):
    """Set Thai Distributed alignment on a body paragraph, unless it is already
    centred/right (a title or signature line that should keep its alignment).
    thaiDistribute's last line stays naturally left-aligned, so this is safe even
    on single-line paragraphs."""
    pPr = p.get_or_add_pPr()
    jc = pPr.find(qn('w:jc'))
    if jc is not None and jc.get(qn('w:val')) in ('center', 'right', 'end'):
        return
    pPr.get_or_add_jc().set(qn('w:val'), 'thaiDistribute')


def _iter_run_parts(doc):
    """Yield the root element of every package part that can contain runs
    (document body, headers, footers, footnotes, endnotes, comments...).

    Sweeping w:r descendants of each such part covers tables, nested tables and
    text boxes for free, because they are all just w:r descendants."""
    seen = set()
    for part in doc.part.package.iter_parts():
        el = getattr(part, 'element', None)
        if el is None or id(el) in seen:
            continue
        if el.find(qn('w:body')) is not None or el.tag in (
                qn('w:hdr'), qn('w:ftr'), qn('w:footnotes'), qn('w:endnotes'),
                qn('w:comments')):
            seen.add(id(el))
            yield el


def enforce_thai(doc, *, thai_font=DEFAULT_THAI_FONT, latin_font=None,
                 size_pt=DEFAULT_SIZE_PT, thai_size_pt=None, latin_size_pt=None,
                 uniform=True, distribute=True, page=True, lang="th-TH",
                 style=None):
    """Make `doc` render Thai correctly in Microsoft Word. Call once before save().

    thai_font:   Complex-script font (Thai). Default "TH Sarabun New".
    latin_font:  Latin font. Default None -> same as thai_font (whole doc one font,
                 the usual Thai-document case). A different value only reaches
                 runs with NO Thai in them: a run holding Thai is flagged <w:cs/>,
                 and Word then draws every character of that run, Latin included,
                 in the cs font and size.
    size_pt:     Body size. Default 16pt (TH Sarabun New 16pt = the ราชการ norm).
    thai_size_pt/latin_size_pt: override the size per script (Thai often looks
                 smaller than a Latin font at the same point size).
    uniform:     FORCE size_pt onto EVERYTHING, headings included, overriding each
                 heading's own size. DEFAULT (True), because that is the Thai
                 government-document norm: one font, one size, headings differ only
                 by weight. Pass uniform=False to preserve each heading's own size.
    page:        Set A4 with ราชการ margins (left 3cm, right 2cm, top 2.5cm,
                 bottom 2cm) on every section. DEFAULT (True) -- python-docx
                 otherwise emits US Letter, which is wrong for a Thai document.
                 Pass page=False to keep the document's existing page setup.
    distribute:  Set Thai Distributed (กระจายแบบไทย, w:jc='thaiDistribute') on body
                 content paragraphs -- the Thai government norm for เนื้อความ, and the
                 DEFAULT (True). Shows as plain left-aligned in LibreOffice / Google
                 Docs / previews, which do not support thaiDistribute -- a viewer
                 limitation, not a defect. Pass distribute=False for ชิดซ้าย. Only
                 plain body paragraphs OUTSIDE tables are distributed; headings and
                 centred/right paragraphs keep their alignment, and table cells are
                 never distributed (a narrow cell would push its few words far
                 apart, the "ตารางห่าง" look).
    style:       None (ราชการ defaults above) or "dpu-apa7": the Dhurakij Pundit
                 University APA 7th report layout -- margins 2.54cm all round,
                 chapter heading 20pt, page number top right. See _apply_dpu_apa7.
                 Overrides `uniform` and `page`.
    """
    dpu = style == 'dpu-apa7'
    if style not in (None, 'dpu-apa7'):
        raise ValueError(f"unknown style {style!r}; use None or 'dpu-apa7'")
    force_all = uniform and not dpu              # override heading sizes too
    latin_font = latin_font or thai_font
    thai_hp = round((thai_size_pt or size_pt) * 2)
    latin_hp = round((latin_size_pt or size_pt) * 2)
    common = dict(thai_font=thai_font, latin_font=latin_font, lang=lang)

    if dpu:     # before the cs pass, so szCs/bCs mirror the preset's sizes and bold
        _apply_dpu_apa7(doc)
    _enforce_doc_defaults(doc, thai_hp=thai_hp, latin_hp=latin_hp, **common)
    _enforce_styles(doc, thai_hp=thai_hp, latin_hp=(latin_hp if force_all else None),
                    force_size=force_all, **common)
    base = (latin_hp, thai_hp)
    for root in _iter_run_parts(doc):
        for p in root.iter(qn('w:p')):
            plain = _is_plain_body_para(p)
            # Stamp the base size on plain body paragraphs; a paragraph with a named
            # style (Heading/Title/...) keeps that style's size -- UNLESS force_all
            # (uniform) is set, which flattens everything to one size.
            stamp = base if (force_all or plain) else None
            for r in p.iter(qn('w:r')):
                rPr = r.get_or_add_rPr()
                _apply_rpr(rPr, thai_hp=thai_hp, latin_hp=latin_hp,
                           force_size=force_all, mirror_toggles=True, base_size=stamp,
                           **common)
                # <w:cs/> is what makes Word run its Thai word breaker on this run.
                # Word writes it itself on every run of typed Thai; without it a
                # generated run breaks only at real spaces, so lines end ~60% full
                # and Thai Distributed stretches them wide (checked in Word 365
                # with no Thai editing language installed).
                if _has_thai(''.join(t.text or '' for t in r.iter(qn('w:t')))):
                    _get_or_insert(rPr, 'w:cs', _CS_SUCCESSORS)
                for t in r.iter(qn('w:t')):
                    if t.text:
                        t.text = _break_long_tokens(t.text)
            # Never distribute inside a table: a narrow cell holds only 2-4
            # words a line, and thaiDistribute pushes them edge-to-edge across
            # the cell width -- the "ตารางห่าง" look. Thai tables are ชิดซ้าย by
            # convention; cell alignment the builder set (e.g. a centred header
            # row) is kept untouched.
            if distribute and plain and not _in_table(p):
                _set_thai_distribute(p)
            if dpu and plain and not _in_table(p):
                _set_first_line_indent(p)
    if page and not dpu:
        _enforce_page(doc)
    _enforce_settings(doc, lang=lang)
    _enforce_theme(doc, thai_font=thai_font)
    return doc


def _enforce_doc_defaults(doc, *, thai_font, latin_font, thai_hp, latin_hp, lang):
    styles_el = doc.styles.element
    docDefaults = styles_el.find(qn('w:docDefaults'))
    if docDefaults is None:
        docDefaults = OxmlElement('w:docDefaults')
        styles_el.insert(0, docDefaults)
    rPrDefault = docDefaults.find(qn('w:rPrDefault'))
    if rPrDefault is None:
        rPrDefault = OxmlElement('w:rPrDefault')
        docDefaults.append(rPrDefault)
    rPr = rPrDefault.find(qn('w:rPr'))
    if rPr is None:
        rPr = OxmlElement('w:rPr')
        rPrDefault.append(rPr)
    _apply_rpr(rPr, thai_font=thai_font, latin_font=latin_font, thai_hp=thai_hp,
               latin_hp=latin_hp, lang=lang, force_size=True, mirror_toggles=False)


def _enforce_styles(doc, *, thai_font, latin_font, thai_hp, latin_hp=None, lang,
                    force_size=False):
    for style_el in doc.styles.element.findall(qn('w:style')):
        rPr = style_el.find(qn('w:rPr'))
        if rPr is None:
            rPr = OxmlElement('w:rPr')
            # rPr must follow w:name/w:basedOn etc.; append is schema-valid as it
            # sits late in CT_Style. python-docx places it correctly on read, and
            # for our generated styles order is already valid.
            style_el.append(rPr)
        # Default: font/lang safe, size mirrors only an existing sz, toggles mirrored.
        # force_size=True (uniform mode) overrides every style's size, headings too.
        # iter() also reaches a table style's conditional rPr (header row, first
        # column...), which otherwise keeps pointing English at the theme font.
        for rPr in style_el.iter(qn('w:rPr')):
            _apply_rpr(rPr, thai_font=thai_font, latin_font=latin_font,
                       thai_hp=thai_hp, latin_hp=latin_hp, lang=lang,
                       force_size=force_size, mirror_toggles=True)


def _enforce_page(doc):
    """A4 with the ระเบียบงานสารบรรณ margins, on every section. python-docx defaults
    to US Letter with 1"/1.25" margins, which no Thai document wants."""
    from docx.shared import Cm
    for s in doc.sections:
        s.page_width, s.page_height = Cm(21), Cm(29.7)
        s.left_margin, s.right_margin = Cm(3), Cm(2)
        s.top_margin, s.bottom_margin = Cm(2.5), Cm(2)


_DPU_INDENT_TWIPS = 864         # 0.6 in: DPU body first-line indent (first tab stop)


def _set_first_line_indent(p):
    """DPU body paragraphs start 0.6in in. Skipped where the builder already set
    an indent (a hanging-indent reference entry, a block quote), on centred/right
    lines, and on numbered/bulleted paragraphs."""
    pPr = p.get_or_add_pPr()
    jc = pPr.find(qn('w:jc'))
    if (pPr.find(qn('w:ind')) is not None or pPr.find(qn('w:numPr')) is not None
            or (jc is not None and jc.get(qn('w:val')) in ('center', 'right', 'end'))):
        return
    pPr.get_or_add_ind().set(qn('w:firstLine'), str(_DPU_INDENT_TWIPS))


def page_numbering(section, fmt, start=None):
    """Set a section's page-number format: 'thaiLetters' (ก ข ค, front matter) or
    'decimal' (1 2 3), and optionally restart at `start`. w:pgNumType must sit
    before w:cols in sectPr, or Word reports the file as corrupt."""
    sectPr = section._sectPr
    pg = sectPr.find(qn('w:pgNumType'))
    if pg is None:
        pg = OxmlElement('w:pgNumType')
        sectPr.insert_element_before(pg, 'w:cols', 'w:formProt', 'w:vAlign',
                                     'w:noEndnote', 'w:titlePg', 'w:textDirection',
                                     'w:bidi', 'w:rtlGutter', 'w:docGrid',
                                     'w:printerSettings', 'w:sectPrChange')
    pg.set(qn('w:fmt'), fmt)
    if start is not None:
        pg.set(qn('w:start'), str(start))


def _apply_dpu_apa7(doc):
    """DPU APA 7th layout (คู่มือการเขียนรายงาน APA 7th, Dhurakij Pundit University).

    A4, 2.54cm margins all round, no gutter. Single spacing, 0pt before/after.
    Title/Heading 1 (cover, chapter) 20pt bold centred; Heading 2 (X.Y) 16pt bold
    left; Heading 3+ 16pt regular. Captions 16pt bold. Footnotes 14pt. Page number
    top right, header 1.25cm from the edge, hidden on each section's first page
    (the cover, and each chapter when chapters are their own sections). Heading
    colour and the Title's rule are removed: the report is black text only."""
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Cm, Pt
    for sec in doc.sections:
        sec.page_width, sec.page_height = Cm(21), Cm(29.7)
        sec.left_margin = sec.right_margin = Cm(2.54)
        sec.top_margin = sec.bottom_margin = Cm(2.54)
        sec.header_distance = Cm(1.25)
        sec.different_first_page_header_footer = True
    header = doc.sections[0].header
    if not any(p.text.strip() for p in header.paragraphs):
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        fld = OxmlElement('w:fldSimple')
        fld.set(qn('w:instr'), 'PAGE')
        r = OxmlElement('w:r')
        t = OxmlElement('w:t')
        t.text = '1'
        r.append(t)
        fld.append(r)
        hp._p.append(fld)

    by_name = {st.name: st for st in doc.styles if st.type == 1}   # paragraph
    for st in by_name.values():
        pf = st.paragraph_format
        pf.space_before = pf.space_after = Pt(0)
        pf.line_spacing = 1.0
    look = {'Title': (20, True, 'c'), 'Heading 1': (20, True, 'c'),
            'Heading 2': (16, True, 'l'), 'Caption': (16, True, 'l'),
            'Footnote Text': (14, None, None)}
    look.update({f'Heading {n}': (16, False, 'l') for n in range(3, 10)})
    for name, (size, bold, align) in look.items():
        st = by_name.get(name)
        if st is None:
            continue
        st.font.size = Pt(size)
        if bold is not None:
            st.font.bold, st.font.italic = bold, False
        if align:
            st.paragraph_format.alignment = (WD_ALIGN_PARAGRAPH.CENTER if align == 'c'
                                             else WD_ALIGN_PARAGRAPH.LEFT)
        rPr, pPr = st.element.rPr, st.element.pPr
        for el in ((rPr.find(qn('w:color')) if rPr is not None else None),
                   (pPr.find(qn('w:pBdr')) if pPr is not None else None)):
            if el is not None:
                el.getparent().remove(el)


def _enforce_settings(doc, *, lang):
    settings_el = doc.settings.element
    tfl = settings_el.find(qn('w:themeFontLang'))
    if tfl is None:
        tfl = OxmlElement('w:themeFontLang')
        settings_el.append(tfl)
    tfl.set(qn('w:bidi'), lang)


_A_NS = 'http://schemas.openxmlformats.org/drawingml/2006/main'


def _enforce_theme(doc, *, thai_font):
    """Set the complex-script typeface and a Thai script mapping in the theme so
    even text that relies purely on theme fonts gets a Thai face. Belt-and-braces:
    enforce_thai already sets an explicit cs font on docDefaults, every style and
    every run, so the theme is only a fallback. The theme part is stored as a raw
    blob in python-docx, so we parse and rewrite it directly."""
    from lxml import etree
    try:
        theme_part = next(p for p in doc.part.package.iter_parts()
                          if 'theme' in str(getattr(p, 'partname', '')).lower())
    except StopIteration:
        return
    a = lambda tag: '{%s}%s' % (_A_NS, tag)
    root = etree.fromstring(theme_part.blob)
    changed = False
    for scheme_tag in ('majorFont', 'minorFont'):
        for scheme in root.iter(a(scheme_tag)):
            cs = scheme.find(a('cs'))
            if cs is None:
                cs = scheme.makeelement(a('cs'), {})
                scheme.append(cs)
            cs.set('typeface', thai_font)
            if scheme.find("%s[@script='Thai']" % a('font')) is None:
                scheme.append(scheme.makeelement(
                    a('font'), {'script': 'Thai', 'typeface': thai_font}))
            changed = True
    if changed:
        theme_part._blob = etree.tostring(root, xml_declaration=True,
                                          encoding='UTF-8', standalone=True)


_LONG_TOKEN = 15        # chars; longer non-Thai tokens (URLs, paths) get break points
_BREAK_AFTER = '/-_.:=?&,'


def _break_long_tokens(text):
    """Put zero-width spaces inside long URLs/paths/e-mails, and ONLY there.

    Word cannot break a URL, so the line before one ends half-empty and Thai
    Distributed stretches it letter by letter (checked in Word 365). Thai words are
    never touched: <w:cs/> lets Word break those itself, and a ZWSP inside Thai
    shows as a box under ¶ and fights the Shift+Enter habit Thai editors rely on."""
    import re

    def split(tok):
        tok = tok.replace('\u200b', '')        # idempotent on a second pass
        if (len(tok) <= _LONG_TOKEN or _has_thai(tok)
                or ('/' not in tok and '@' not in tok)):  # keep 1,000,000.00 whole
            return tok
        out, cur = [], ''
        for c in tok:
            cur += c
            if c in _BREAK_AFTER or len(cur) >= _LONG_TOKEN:
                out.append(cur)
                cur = ''
        return '\u200b'.join(out + [cur] if cur else out)
    return re.sub(r'\S+', lambda m: split(m.group(0)), text)


def _has_thai(s):
    return any('\u0e00' <= c <= '\u0e7f' for c in s)
