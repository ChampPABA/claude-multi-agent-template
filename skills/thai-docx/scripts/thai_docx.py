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
    if latin_font:
        rFonts.set(qn('w:ascii'), latin_font)
        rFonts.set(qn('w:hAnsi'), latin_font)

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
                 uniform_size_pt=None, distribute=True, lang="th-TH", add_zwsp=False):
    """Make `doc` render Thai correctly in Microsoft Word. Call once before save().

    thai_font:   Complex-script font (Thai). Default "TH Sarabun New".
    latin_font:  Latin font. Default None -> same as thai_font (whole doc one font,
                 the usual Thai-gov-doc case). Pass a different value, e.g.
                 "Times New Roman", to split Latin vs Thai fonts within one run.
    size_pt:     Base size for text that specifies none of its own. Default 16pt.
    thai_size_pt/latin_size_pt: override the base size per script (Thai often looks
                 smaller than a Latin font at the same point size).
    uniform_size_pt: FORCE one size onto EVERYTHING, headings included, overriding
                 each heading's own size. This is the Thai government-document norm
                 (TH Sarabun New 16pt everywhere; headings differ only by weight,
                 not size). When None (default) heading sizes are preserved.
    distribute:  Set Thai Distributed (กระจายแบบไทย, w:jc='thaiDistribute') on body
                 content paragraphs -- the Thai government norm for เนื้อความ, and the
                 DEFAULT (True). Renders beautifully in real Microsoft Word (verified
                 by eye); note it shows as plain left-aligned in LibreOffice / Google
                 Docs / previews, which do not support thaiDistribute -- that is a
                 viewer limitation, not a defect. Pass distribute=False for a plainly
                 left-aligned (ชิดซ้าย) document. Only
                 plain body paragraphs are distributed; headings and centred/right
                 paragraphs (titles, signatures, ที่/เรื่อง/เรียน lines) are left as
                 they are, because distributing a short meta line looks wrong.
                 thaiDistribute is a justify type, so the last line of a paragraph
                 stays naturally left-aligned (not stretched). Distribute REQUIRES
                 word-boundary breaks to look right, so it auto-enables add_zwsp,
                 and sets w:doNotExpandShiftReturn to stop Shift+Enter lines
                 stretching. Needs pythainlp for the word breaks.
    add_zwsp:    Insert zero-width spaces at Thai word boundaries so justified /
                 Thai-distributed paragraphs break between words instead of
                 stretching glyphs apart. Needs pythainlp; skipped with a warning
                 if absent. Mutates run text, so do it last.
    """
    if uniform_size_pt is not None:
        size_pt = thai_size_pt = latin_size_pt = uniform_size_pt
    force_all = uniform_size_pt is not None      # override heading sizes too
    latin_font = latin_font or thai_font
    thai_hp = round((thai_size_pt or size_pt) * 2)
    latin_hp = round((latin_size_pt or size_pt) * 2)
    common = dict(thai_font=thai_font, latin_font=latin_font, lang=lang)

    _enforce_doc_defaults(doc, thai_hp=thai_hp, latin_hp=latin_hp, **common)
    _enforce_styles(doc, thai_hp=thai_hp, latin_hp=(latin_hp if force_all else None),
                    force_size=force_all, **common)
    base = (latin_hp, thai_hp)
    for root in _iter_run_parts(doc):
        for p in root.iter(qn('w:p')):
            plain = _is_plain_body_para(p)
            # Stamp the base size on plain body paragraphs; a paragraph with a named
            # style (Heading/Title/...) keeps that style's size -- UNLESS force_all
            # (uniform_size_pt) is set, which flattens everything to one size.
            stamp = base if (force_all or plain) else None
            for r in p.iter(qn('w:r')):
                _apply_rpr(r.get_or_add_rPr(), thai_hp=thai_hp, latin_hp=latin_hp,
                           force_size=force_all, mirror_toggles=True, base_size=stamp,
                           **common)
            if distribute and plain:
                _set_thai_distribute(p)
    _enforce_settings(doc, lang=lang, no_expand_shift_return=distribute)
    _enforce_theme(doc, thai_font=thai_font)
    if add_zwsp or distribute:      # distribute needs word breaks to look right
        _insert_zwsp(doc)
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
        _apply_rpr(rPr, thai_font=thai_font, latin_font=latin_font,
                   thai_hp=thai_hp, latin_hp=latin_hp, lang=lang,
                   force_size=force_size, mirror_toggles=True)


def _enforce_settings(doc, *, lang, no_expand_shift_return=False):
    settings_el = doc.settings.element
    tfl = settings_el.find(qn('w:themeFontLang'))
    if tfl is None:
        tfl = OxmlElement('w:themeFontLang')
        settings_el.append(tfl)
    tfl.set(qn('w:bidi'), lang)
    # Stop a line that ends with Shift+Enter from being stretched full width under
    # Thai Distributed / justify (the usual cause of a lone stretched short line).
    if no_expand_shift_return and settings_el.find(qn('w:doNotExpandShiftReturn')) is None:
        settings_el.append(OxmlElement('w:doNotExpandShiftReturn'))


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


def _insert_zwsp(doc):
    try:
        from pythainlp.tokenize import word_tokenize
    except ImportError:
        import warnings
        warnings.warn("pythainlp not installed; skipping ZWSP word-break insertion. "
                      "Justified Thai paragraphs may stretch glyphs apart.")
        return
    zwsp = '​'
    has_thai = lambda s: any('฀' <= c <= '๿' for c in s)
    for root in _iter_run_parts(doc):
        for t in root.iter(qn('w:t')):
            if t.text and has_thai(t.text):
                t.text = zwsp.join(word_tokenize(t.text))
