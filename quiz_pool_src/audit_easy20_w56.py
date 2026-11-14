#!/usr/bin/env python3
"""Independent audit of the easy 20 question quiz.

It reads the three delivered files only. It imports no question source.
"""
import itertools
import re
import sys
import xml.etree.ElementTree as ET
import zipfile

D = "/Users/maziar/Downloads/k8s_week3/quiz_pool_src/Quiz_W05W06_Easy20/"
TXT = D + "Quiz_W05W06_Easy20_Blackboard.txt"
KEY = D + "Quiz_W05W06_Easy20_AnswerKey.txt"
ZIP = D + "Quiz_W05W06_Easy20_QTI21.zip"
TIT = D + "Quiz_W05W06_Easy20_Titles.txt"
Q = "{http://www.imsglobal.org/xsd/imsqti_v2p1}"
CP = "{http://www.imsglobal.org/xsd/imscp_v1p1}"
LETTERS = "ABCD"
err = []

# ---------------------------------------------------------------- the .txt
rows = []
for line in open(TXT):
    f = line.rstrip("\n").split("\t")
    if len(f) != 10 or f[0] != "MC":
        err.append("bad row: %r" % f[:2]); continue
    opts = [(f[2], f[3]), (f[4], f[5]), (f[6], f[7]), (f[8], f[9])]
    rows.append({"stem": f[1], "opts": opts})
print("rows in the upload file: %d" % len(rows))
if len(rows) != 20:
    err.append("the upload file holds %d rows, not 20" % len(rows))

letters, longest, shortest, most_words = [], 0, 0, 0
for n, r in enumerate(rows, 1):
    marks = [m for _, m in r["opts"]]
    if marks.count("correct") != 1:
        err.append("Q%d: %d correct options" % (n, marks.count("correct")))
        continue
    i = marks.index("correct")
    letters.append(LETTERS[i])
    texts = [t for t, _ in r["opts"]]
    if len(set(texts)) != 4:
        err.append("Q%d: a repeated option" % n)
    L = [len(t) for t in texts]
    W = [len(t.split()) for t in texts]
    if L[i] > max(L[:i] + L[i + 1:]):
        longest += 1
    if L[i] < min(L[:i] + L[i + 1:]):
        shortest += 1
    if W[i] > max(W[:i] + W[i + 1:]):
        most_words += 1
    for t in texts:
        low = t.lower()
        if low in ("all of the above", "none of the above") or low.startswith("both "):
            err.append("Q%d: a banned option -> %s" % (n, t))
    if " NOT " in r["stem"] or re.search(r"\bnot\b", r["stem"]):
        err.append("Q%d: the stem holds a negative word" % n)

tally = {l: letters.count(l) for l in LETTERS}
print("correct answers per letter: %s" % tally)
if sorted(tally.values()) != [5, 5, 5, 5]:
    err.append("the letters are not balanced")
run = max(len(list(g)) for _, g in itertools.groupby(letters))
print("longest run of one letter: %d" % run)
if run > 3:
    err.append("a run of %d equal letters" % run)

print("guess by the longest option: %d of %d" % (longest, len(rows)))
print("guess by the shortest option: %d of %d" % (shortest, len(rows)))
print("guess by the most words: %d of %d" % (most_words, len(rows)))
for name, v in (("longest", longest), ("shortest", shortest), ("most words", most_words)):
    if v > 7:
        err.append("guessing by the %s option wins %d times" % (name, v))

# answer leak and give-away between two questions
STOP = set("""a an the and or of to in on for with that this these those is are was were be been
which what when where why how does do did can could will would should may might must into from
by as at it its their your you we our one two three four five first second third than then also
more most less least other another same different only not no yes about over under between each
every any all some both many much few after before while during until since because so such""".split())
def cw(s):
    return {w for w in re.findall(r"[a-z0-9_.-]{5,}", s.lower()) if w not in STOP}
leak = 0
for n, r in enumerate(rows, 1):
    marks = [m for _, m in r["opts"]]
    i = marks.index("correct")
    sw = cw(r["stem"])
    share = [len(sw & cw(t)) for t, _ in r["opts"]]
    if share[i] - max(share[:i] + share[i + 1:]) >= 2:
        leak += 1
        err.append("Q%d: the correct option repeats the stem wording" % n)
print("answer leaks: %d" % leak)

def w4(t):
    return {x for x in re.findall(r"[a-z]{4,}", t.lower())}
pairs = 0
for a, b in itertools.combinations(range(len(rows)), 2):
    ia = [m for _, m in rows[a]["opts"]].index("correct")
    ib = [m for _, m in rows[b]["opts"]].index("correct")
    same = re.sub(r"[^a-z0-9]+", "", rows[a]["opts"][ia][0].lower()) == \
           re.sub(r"[^a-z0-9]+", "", rows[b]["opts"][ib][0].lower())
    A, B = w4(rows[a]["stem"]), w4(rows[b]["stem"])
    jac = len(A & B) / len(A | B) if (A | B) else 0
    if (same and jac >= 0.45) or jac >= 0.80:
        pairs += 1
        err.append("Q%d and Q%d carry the same fact" % (a + 1, b + 1))
print("question pairs at risk: %d" % pairs)

# ---------------------------------------------------------------- the key
txt = open(KEY).read()
blocks = re.findall(
    r"^[ ]*(\d+)\. \[([^\]]+)\] ([^\n]+)\n(.*?)\n[ ]+ANSWER ([A-D])\n"
    r"[ ]+WHY: ([^\n]+)\n((?:[ ]+IF [A-D]: [^\n]+\n?)+)",
    txt, re.M | re.S)
print("records in the key: %d" % len(blocks))
if len(blocks) != len(rows):
    err.append("the key holds %d records, not %d" % (len(blocks), len(rows)))
for num, qtitle, stem, opts_txt, letter, why, ifs in blocks:
    n = int(num)
    r = rows[n - 1]
    if stem.strip() != r["stem"]:
        err.append("key %d: the stem does not match the upload file" % n)
    i = [m for _, m in r["opts"]].index("correct")
    if letter != LETTERS[i]:
        err.append("key %d: the letter does not match the upload file" % n)
    star = re.findall(r"^\s+\* ([A-D])\. (.+)$", opts_txt, re.M)
    if len(star) != 1 or star[0][0] != letter or star[0][1].strip() != r["opts"][i][0]:
        err.append("key %d: the star does not mark the correct option" % n)
    if len(re.findall(r"\s+IF [A-D]: ", ifs)) != 3:
        err.append("key %d: the mistakes are not complete" % n)
    if not why.strip():
        err.append("key %d: no reason" % n)

# ---------------------------------------------------------------- the ZIP
z = zipfile.ZipFile(ZIP)
names = z.namelist()
items = sorted(n for n in names if n.startswith("items/"))
print("files in the ZIP: %d (items %d)" % (len(names), len(items)))
if "imsmanifest.xml" not in names:
    err.append("no imsmanifest.xml at the ZIP root")
man = ET.fromstring(z.read("imsmanifest.xml"))
res = man.findall(".//%sresource" % CP)
if len(res) != len(items):
    err.append("the manifest lists %d resources for %d items" % (len(res), len(items)))
for r in res:
    if r.get("type") != "imsqti_item_xmlv2p1" or r.get("href") not in names:
        err.append("bad resource: %s" % r.get("identifier"))
for n, name in enumerate(items, 1):
    it = ET.fromstring(z.read(name))
    vals = it.findall(".//%scorrectResponse/%svalue" % (Q, Q))
    ch = it.findall(".//%ssimpleChoice" % Q)
    if len(vals) != 1 or len(ch) != 4:
        err.append("%s: %d correct values, %d options" % (name, len(vals), len(ch)))
        continue
    cids = [c.get("identifier") for c in ch]
    if vals[0].text not in cids:
        err.append("%s: the correct value is not an option" % name)
        continue
    i = cids.index(vals[0].text)
    stem = (it.find(".//%sprompt" % Q).text or "").strip()
    r = rows[n - 1]
    j = [m for _, m in r["opts"]].index("correct")
    if stem != r["stem"]:
        err.append("%s: the stem does not match the upload file" % name)
    if i != j or (ch[i].text or "").strip() != r["opts"][j][0]:
        err.append("%s: the answer does not match the upload file" % name)
    tpl = it.find("%sresponseProcessing" % Q)
    if tpl is None or not tpl.get("template", "").endswith("match_correct"):
        err.append("%s: no match_correct template" % name)

# ---------------------------------------------------------------- titles
tit = [t.rstrip("\n") for t in open(TIT) if t.strip()]
print("titles in the title file: %d" % len(tit))
if len(tit) != len(rows):
    err.append("the title file holds %d titles, not %d" % (len(tit), len(rows)))
for n, name in enumerate(items, 1):
    it = ET.fromstring(z.read(name))
    t = it.get("title") or ""
    if not re.match(r"^clo835-e56-\d{3} [a-z][a-z ]*$", t):
        err.append("%s: the title is not an identifier and a topic -> %r" % (name, t))
    if n <= len(tit) and t != tit[n - 1]:
        err.append("%s: the title and the title file do not agree" % name)
    low = t.lower()
    r = rows[n - 1]
    for o, _m in r["opts"]:
        if o.lower() in low or low in o.lower():
            err.append("%s: the title shows an option" % name)
    if r["stem"][:20].lower() in low:
        err.append("%s: the title repeats the stem" % name)

print("errors: %d" % len(err))
for e in err[:25]:
    print("  - %s" % e)
sys.exit(1 if err else 0)
