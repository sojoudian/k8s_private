#!/usr/bin/env python3
"""Make a QTI 2.1 package from a Blackboard tab delimited pool file.

Usage: qti_pack.py <pool.txt> <out.zip> <bank name> <id prefix>
Blackboard Ultra imports the ZIP file into a question bank.
"""
import os
import shutil
import sys
import zipfile
from xml.sax.saxutils import escape, quoteattr

LETTERS = "ABCD"

ITEM = """<?xml version="1.0" encoding="UTF-8"?>
<assessmentItem xmlns="http://www.imsglobal.org/xsd/imsqti_v2p1"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.imsglobal.org/xsd/imsqti_v2p1 http://www.imsglobal.org/xsd/qti/qtiv2p1/imsqti_v2p1.xsd"
    identifier="{iid}" title={title} adaptive="false" timeDependent="false">
  <responseDeclaration identifier="RESPONSE" cardinality="single" baseType="identifier">
    <correctResponse>
      <value>{correct}</value>
    </correctResponse>
  </responseDeclaration>
  <outcomeDeclaration identifier="SCORE" cardinality="single" baseType="float">
    <defaultValue>
      <value>0</value>
    </defaultValue>
  </outcomeDeclaration>
  <itemBody>
    <choiceInteraction responseIdentifier="RESPONSE" shuffle="false" maxChoices="1" minChoices="1">
      <prompt>{stem}</prompt>
{choices}
    </choiceInteraction>
  </itemBody>
  <responseProcessing template="http://www.imsglobal.org/question/qti_v2p1/rptemplates/match_correct"/>
</assessmentItem>
"""

CHOICE = '      <simpleChoice identifier="{cid}">{text}</simpleChoice>'

MANIFEST = """<?xml version="1.0" encoding="UTF-8"?>
<manifest identifier="MANIFEST-{mid}"
    xmlns="http://www.imsglobal.org/xsd/imscp_v1p1"
    xmlns:imsmd="http://www.imsglobal.org/xsd/imsmd_v1p2"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.imsglobal.org/xsd/imscp_v1p1 http://www.imsglobal.org/xsd/qti/qtiv2p1/imscp_v1p2_v1p0.xsd">
  <metadata>
    <schema>QTIv2.1 Package</schema>
    <schemaversion>1.0.0</schemaversion>
    <imsmd:lom>
      <imsmd:general>
        <imsmd:title>
          <imsmd:langstring xml:lang="en">{bank}</imsmd:langstring>
        </imsmd:title>
      </imsmd:general>
    </imsmd:lom>
  </metadata>
  <organizations/>
  <resources>
{resources}
  </resources>
</manifest>
"""

RESOURCE = """    <resource identifier="{rid}" type="imsqti_item_xmlv2p1" href="{href}">
      <file href="{href}"/>
    </resource>"""


def read_rows(path):
    """Read the pool file and give one record for each question."""
    out = []
    for line in open(path):
        f = line.rstrip("\n").split("\t")
        if len(f) != 10 or f[0] != "MC":
            raise SystemExit("bad row: %r" % f[:2])
        opts = [(f[2], f[3]), (f[4], f[5]), (f[6], f[7]), (f[8], f[9])]
        if [m for _, m in opts].count("correct") != 1:
            raise SystemExit("bad correct count in: %s" % f[1])
        out.append({"stem": f[1], "opts": opts})
    return out


def short_title(stem, limit=60):
    """Cut the stem to a short item title."""
    if len(stem) <= limit:
        return stem
    return stem[:limit].rsplit(" ", 1)[0] + "..."


def main():
    src, out, bank, prefix = sys.argv[1:5]
    titles = None
    if len(sys.argv) > 5:                      # one neutral title for each row
        titles = [t.rstrip("\n") for t in open(sys.argv[5]) if t.strip()]
    rows = read_rows(src)
    if titles is not None and len(titles) != len(rows):
        raise SystemExit("%d titles for %d questions" % (len(titles), len(rows)))
    stage = out + ".stage"
    if os.path.isdir(stage):
        shutil.rmtree(stage)
    os.makedirs(os.path.join(stage, "items"))

    resources, hrefs = [], []
    for n, row in enumerate(rows, 1):
        iid = "%s-%03d" % (prefix, n)
        choices, correct = [], None
        for i, (text, mark) in enumerate(row["opts"]):
            cid = "%s-choice%s" % (iid, LETTERS[i])
            choices.append(CHOICE.format(cid=cid, text=escape(text)))
            if mark == "correct":
                correct = cid
        xml = ITEM.format(
            iid=iid,
            title=quoteattr(titles[n - 1] if titles else short_title(row["stem"])),
            correct=correct,
            stem=escape(row["stem"]),
            choices="\n".join(choices),
        )
        href = "items/%s.xml" % iid
        open(os.path.join(stage, href), "w").write(xml)
        hrefs.append(href)
        resources.append(RESOURCE.format(rid="%s-res" % iid, href=href))

    open(os.path.join(stage, "imsmanifest.xml"), "w").write(
        MANIFEST.format(mid=prefix.upper(), bank=escape(bank),
                        resources="\n".join(resources)))

    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(os.path.join(stage, "imsmanifest.xml"), "imsmanifest.xml")
        for href in hrefs:
            z.write(os.path.join(stage, href), href)
    shutil.rmtree(stage)
    print("questions: %d" % len(rows))
    print("package: %s (%d bytes)" % (out, os.path.getsize(out)))


if __name__ == "__main__":
    main()
