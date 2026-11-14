# -*- coding: utf-8 -*-
"""Independent audit of the Quiz 3 pool.

It reads the upload file only. It does not import the question source. Every
number below comes from the artifact that Blackboard receives.
"""
import re, sys, os, itertools, collections

F = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                 "Quiz03_Pool_Blackboard.txt")
DRAW, TOTAL = 20, 100
BANNED = ["the deck", "the slide", "the lecture", "the table", "the figure",
          "the week", "this week", "the course", "according to", "the example",
          "the diagram", "step 1", "step 2", "layer 1", "layer 2", "percent",
          "liang", "the agenda", "shown above", "the list above"]

rows, bad, warn = [], [], []
for ln, line in enumerate(open(F).read().rstrip("\n").split("\n"), 1):
    f = line.split("\t")
    if f[0] != "MC" or len(f) != 10:
        bad.append("line %d: %d fields, type %r" % (ln, len(f), f[0])); continue
    stem = f[1]
    opts = [(f[2], f[3]), (f[4], f[5]), (f[6], f[7]), (f[8], f[9])]
    rows.append((ln, stem, opts))

print("A. STRUCTURE")
print("   rows                : %d" % len(rows))
if len(rows) != TOTAL:
    bad.append("row count is %d, not %d" % (len(rows), TOTAL))

letters = collections.Counter()
for ln, stem, opts in rows:
    flags = [v for _, v in opts]
    if flags.count("correct") != 1:
        bad.append("line %d: %d correct options" % (ln, flags.count("correct")))
        continue
    letters["ABCD"[flags.index("correct")]] += 1
    texts = [t for t, _ in opts]
    if len(set(texts)) != 4:
        bad.append("line %d: a repeated option" % ln)
    norm = [re.sub(r"[^a-z0-9]+", "", t.lower()) for t in texts]
    if len(set(norm)) != 4:
        bad.append("line %d: two options differ only in punctuation" % ln)
    for t in texts + [stem]:
        if not t.strip():
            bad.append("line %d: an empty field" % ln)
    for b in BANNED:
        if b in stem.lower():
            bad.append("line %d: the stem points outside itself -> %r" % (ln, b))
        for t in texts:
            if b in t.lower():
                bad.append("line %d: an option points outside itself -> %r" % (ln, b))

print("B. KEY BALANCE  (the upload file cannot shuffle options)")
print("   per letter          : %s" % dict(sorted(letters.items())))
if sorted(letters.values()) != [25, 25, 25, 25]:
    bad.append("the key is not 25 per letter")

print("C. GUESSING BY LENGTH")
def strat(pick):
    hit = 0
    for ln, stem, opts in rows:
        texts = [t for t, _ in opts]
        c = [v for _, v in opts].index("correct")
        if pick(texts) == c:
            hit += 1
    return hit
longest = strat(lambda t: max(range(4), key=lambda i: len(t[i])))
shortest = strat(lambda t: min(range(4), key=lambda i: len(t[i])))
words = strat(lambda t: max(range(4), key=lambda i: len(t[i].split())))
print("   pick the longest    : %d of %d" % (longest, TOTAL))
print("   pick the shortest   : %d of %d" % (shortest, TOTAL))
print("   pick the most words : %d of %d" % (words, TOTAL))
for name, v in (("longest", longest), ("shortest", shortest), ("most words", words)):
    if v > 35:
        bad.append("guessing by %s wins %d of %d" % (name, v, TOTAL))
    elif v > 30:
        warn.append("guessing by %s wins %d of %d" % (name, v, TOTAL))

print("D. ONE QUESTION HANDS OVER ANOTHER ANSWER")
STOP = set("""a an the and or of to in on for with that this these those is are was were be
been which what when where why how does do did can could will would should may might must
into from by as at it its their your you we our one two three four five first second third
than then also more most less least other another same different only not no yes about over
under between each every any all some both many much few after before while during until
since because so such does""".split())
def cw(s):
    return {w for w in re.findall(r"[a-z0-9_.-]{4,}", s.lower()) if w not in STOP}
pair_leak, same_ans = [], []
for (la, sa, oa), (lb, sb, ob) in itertools.combinations(rows, 2):
    ca = [t for t, v in oa if v == "correct"][0]
    cb = [t for t, v in ob if v == "correct"][0]
    na = re.sub(r"[^a-z0-9]+", "", ca.lower())
    nb = re.sub(r"[^a-z0-9]+", "", cb.lower())
    A, B = cw(sa), cw(sb)
    jac = len(A & B) / len(A | B) if (A | B) else 0
    if na == nb and jac >= 0.45:
        same_ans.append("line %d and line %d: one answer, close stems (%.2f)" % (la, lb, jac))
    if jac >= 0.75:
        pair_leak.append("line %d and line %d: near equal stems (%.2f)" % (la, lb, jac))
print("   one answer, close stems : %d" % len(same_ans))
print("   near equal stems        : %d" % len(pair_leak))
bad += same_ans + pair_leak

print("E. THE STEM CARRIES ITS OWN ANSWER")
leak = 0
for ln, stem, opts in rows:
    sw = cw(stem)
    share = [len(sw & cw(t)) for t, _ in opts]
    c = [v for _, v in opts].index("correct")
    if share[c] - max(s for i, s in enumerate(share) if i != c) >= 2:
        bad.append("line %d: the correct option repeats the stem" % ln); leak += 1
print("   answer leaks        : %d" % leak)

print("F. CHANCE THAT ONE DRAW HOLDS BOTH QUESTIONS OF A PAIR")
p = (DRAW * (DRAW - 1)) / float(TOTAL * (TOTAL - 1))
print("   draw %d of %d        : %.3f%%  (1 in %.0f)" % (DRAW, TOTAL, 100 * p, 1 / p))
print("   pairs at risk       : %d  -> joint risk %.4f%%"
      % (len(same_ans) + len(pair_leak), 100 * p * (len(same_ans) + len(pair_leak))))

print("\nWARNINGS: %d" % len(warn))
for w in warn:
    print("   ", w)
print("DEFECTS : %d" % len(bad))
for b in bad[:60]:
    print("   ", b)
sys.exit(1 if bad else 0)
