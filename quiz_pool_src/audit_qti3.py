#!/usr/bin/env python3
"""Audit the QTI 2.1 package. The audit reads the ZIP file and the key only."""
import re
import sys
import xml.etree.ElementTree as ET
import zipfile

ZIP = "Quiz03_Pool_QTI21.zip"
KEY = "Quiz03_Pool_AnswerKey.txt"
Q = "{http://www.imsglobal.org/xsd/imsqti_v2p1}"
CP = "{http://www.imsglobal.org/xsd/imscp_v1p1}"
LETTERS = "ABCD"
err = []

z = zipfile.ZipFile(ZIP)
names = z.namelist()
if "imsmanifest.xml" not in names:
    err.append("no imsmanifest.xml at the ZIP root")
items = sorted(n for n in names if n.startswith("items/"))
print("files in the ZIP: %d (items %d)" % (len(names), len(items)))

man = ET.fromstring(z.read("imsmanifest.xml"))
res = man.findall(".//%sresource" % CP)
print("resources in the manifest: %d" % len(res))
hrefs = set()
for r in res:
    if r.get("type") != "imsqti_item_xmlv2p1":
        err.append("bad resource type: %s" % r.get("type"))
    h = r.get("href")
    hrefs.add(h)
    if h not in names:
        err.append("manifest points at a missing file: %s" % h)
    f = r.findall("%sfile" % CP)
    if len(f) != 1 or f[0].get("href") != h:
        err.append("bad file element in %s" % r.get("identifier"))
if hrefs != set(items):
    err.append("the manifest list and the ZIP list do not agree")

# Read the key.
key = {}
txt = z and open(KEY).read()
for m in re.finditer(r"^\s*(\d+)\. \[[^\]]+\] (.+?)\n\s+ANSWER ([A-D]): (.+?)$", txt, re.M):
    key[int(m.group(1))] = (m.group(2).strip(), m.group(3), m.group(4).strip())
print("records in the key: %d" % len(key))

ids = set()
mismatch = 0
for n, name in enumerate(items, 1):
    it = ET.fromstring(z.read(name))
    iid = it.get("identifier")
    if iid in ids:
        err.append("a repeated identifier: %s" % iid)
    ids.add(iid)
    vals = it.findall(".//%scorrectResponse/%svalue" % (Q, Q))
    if len(vals) != 1:
        err.append("%s: %d correct values" % (name, len(vals)))
        continue
    ch = it.findall(".//%ssimpleChoice" % Q)
    if len(ch) != 4:
        err.append("%s: %d options" % (name, len(ch)))
        continue
    cids = [c.get("identifier") for c in ch]
    if len(set(cids)) != 4:
        err.append("%s: repeated option identifiers" % name)
    if vals[0].text not in cids:
        err.append("%s: the correct value is not an option" % name)
        continue
    pos = cids.index(vals[0].text)
    stem = (it.find(".//%sprompt" % Q).text or "").strip()
    k_stem, k_letter, k_text = key[n]
    if stem != k_stem:
        err.append("%s: the stem does not match the key" % name)
    if LETTERS[pos] != k_letter or (ch[pos].text or "").strip() != k_text:
        mismatch += 1
        err.append("%s: the answer does not match the key" % name)
    tpl = it.find("%sresponseProcessing" % Q)
    if tpl is None or not tpl.get("template", "").endswith("match_correct"):
        err.append("%s: no match_correct template" % name)

print("items read: %d" % len(items))
print("answer mismatches against the key: %d" % mismatch)
print("errors: %d" % len(err))
for e in err[:20]:
    print("  - %s" % e)
sys.exit(1 if err else 0)
