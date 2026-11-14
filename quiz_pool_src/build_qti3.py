#!/usr/bin/env python3
"""Make a QTI 2.1 package from the Quiz 3 pool.

The input is the tab delimited Blackboard file. The output is a ZIP file.
Blackboard Ultra imports the ZIP file into a question bank.
"""
import os
import shutil
import zipfile
from xml.sax.saxutils import escape

SRC = "Quiz03_Pool_Blackboard.txt"
OUT = "Quiz03_Pool_QTI21.zip"
STAGE = "qti3_stage"
BANK = "CLO835 Quiz 3 Pool"
LETTERS = "ABCD"

ITEM = """<?xml version="1.0" encoding="UTF-8"?>
<assessmentItem xmlns="http://www.imsglobal.org/xsd/imsqti_v2p1"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.imsglobal.org/xsd/imsqti_v2p1 http://www.imsglobal.org/xsd/qti/qtiv2p1/imsqti_v2p1.xsd"
    identifier="{iid}" title="{title}" adaptive="false" timeDependent="false">
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
<manifest identifier="MANIFEST-CLO835-QUIZ3"
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
        if len(f) != 10:
            raise SystemExit("bad field count: %d" % len(f))
        if f[0] != "MC":
            raise SystemExit("bad question type: %s" % f[0])
        opts = [(f[2], f[3]), (f[4], f[5]), (f[6], f[7]), (f[8], f[9])]
        flags = [m for _, m in opts]
        if flags.count("correct") != 1:
            raise SystemExit("bad correct count: %r" % flags)
        out.append({"stem": f[1], "opts": opts})
    return out


def short_title(stem, limit=60):
    """Cut the stem to a short item title."""
    if len(stem) <= limit:
        return stem
    return stem[:limit].rsplit(" ", 1)[0] + "..."


def main():
    rows = read_rows(SRC)
    if os.path.isdir(STAGE):
        shutil.rmtree(STAGE)
    os.makedirs(os.path.join(STAGE, "items"))

    resources = []
    for n, row in enumerate(rows, 1):
        iid = "clo835-q3-%03d" % n
        choices = []
        correct = None
        for i, (text, mark) in enumerate(row["opts"]):
            cid = "%s-choice%s" % (iid, LETTERS[i])
            choices.append(CHOICE.format(cid=cid, text=escape(text)))
            if mark == "correct":
                correct = cid
        xml = ITEM.format(
            iid=iid,
            title=escape(short_title(row["stem"]), {'"': "&quot;"}),
            correct=correct,
            stem=escape(row["stem"]),
            choices="\n".join(choices),
        )
        href = "items/%s.xml" % iid
        with open(os.path.join(STAGE, href), "w") as fh:
            fh.write(xml)
        resources.append(RESOURCE.format(rid="%s-res" % iid, href=href))

    with open(os.path.join(STAGE, "imsmanifest.xml"), "w") as fh:
        fh.write(MANIFEST.format(bank=escape(BANK), resources="\n".join(resources)))

    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(os.path.join(STAGE, "imsmanifest.xml"), "imsmanifest.xml")
        for n in range(1, len(rows) + 1):
            href = "items/clo835-q3-%03d.xml" % n
            z.write(os.path.join(STAGE, href), href)

    print("questions: %d" % len(rows))
    print("package: %s (%d bytes)" % (OUT, os.path.getsize(OUT)))


if __name__ == "__main__":
    main()
