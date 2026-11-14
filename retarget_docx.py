# -*- coding: utf-8 -*-
"""CLO835 - replace text in a .docx file and write the next version of it.

The input file is read and never written. Only word/document.xml changes; every
other part of the package is copied byte for byte. A replacement may span more
than one run: the new text goes into the first run of the span, so that run
keeps its format, and the rest of the span is removed from the other runs.

It uses lxml and zipfile only (both come with the project .venv).
It is guarded, so importing it writes nothing.
"""
import zipfile
from lxml import etree

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
XML_SPACE = "{http://www.w3.org/XML/1998/namespace}space"


def _texts(p):
    """The w:t elements of one paragraph, in order (runs, hyperlinks, fields)."""
    return [t for t in p.iter(W + "t")]


def replace_in_paragraph(p, old, new):
    count = 0
    while True:
        ts = _texts(p)
        text = "".join(t.text or "" for t in ts)
        at = text.find(old)
        if at < 0:
            return count
        end, pos, first = at + len(old), 0, None
        for t in ts:
            s = t.text or ""
            a, b = pos, pos + len(s)
            pos = b
            if b <= at or a >= end:
                continue
            head = s[:max(0, at - a)]
            tail = s[max(0, end - a):] if end < b else ""
            if first is None:
                first = t
                t.text = head + new + tail
            else:
                t.text = tail
            t.set(XML_SPACE, "preserve")
        count += 1


def paragraph_texts(path):
    z = zipfile.ZipFile(path)
    root = etree.fromstring(z.read("word/document.xml"))
    return ["".join(t.text or "" for t in _texts(p)) for p in root.iter(W + "p")]


def retarget(src, out, pairs):
    """Apply (old, new) pairs to every paragraph. Return the count per old text.
    A triple (old, new, "exact") replaces only a paragraph whose whole text is old."""
    zin = zipfile.ZipFile(src)
    root = etree.fromstring(zin.read("word/document.xml"))
    done = {pr[0]: 0 for pr in pairs}
    for p in root.iter(W + "p"):
        for pr in pairs:
            old, new = pr[0], pr[1]
            if len(pr) == 3:
                if "".join(t.text or "" for t in _texts(p)) != old:
                    continue
            done[old] += replace_in_paragraph(p, old, new)
    xml = etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = xml if item.filename == "word/document.xml" else zin.read(item.filename)
            zout.writestr(item, data)
    return done, [old for old, n in done.items() if n == 0]


if __name__ == "__main__":
    import sys
    for f in sys.argv[1:]:
        for i, t in enumerate(paragraph_texts(f)):
            print("%4d  %s" % (i, t))
