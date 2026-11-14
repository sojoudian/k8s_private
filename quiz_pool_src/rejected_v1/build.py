"""CLO835 - build a Blackboard question pool from a lecture deck.

Safety rules, written after the Week 01 quiz shipped two unanswerable questions:
  1. Every question carries `src`: a substring that MUST appear in the deck text.
     If it does not appear, the build FAILS. No question can invent a fact.
  2. No question may come from a slide whose content is only a picture.
  3. Exactly 4 options, exactly 1 correct, no repeated option, no repeated stem.
  4. No TAB and no newline inside any field, because the upload is tab-delimited.
Option a[0] is always the correct one in the source file. The builder shuffles
with a fixed seed per question, so the output is reproducible.
"""
import hashlib, re, sys, os

ROOT = "/Users/maziar/Downloads/k8s_week3"
OUT = os.path.dirname(os.path.abspath(__file__))
DECKS = {
    "W01": ("week01/Week01_lecture_style_v5.pptx", "Week01_Pool_Blackboard.txt",
            "Week 01 - Docker Introduction"),
    "W02": ("week02/Week02_lecture_style_v1.pptx", "Week02_Pool_Blackboard.txt",
            "Week 02 - Docker Image Management"),
    "W03": ("week03/Week03_lecture_style_v1.pptx", "Week03_Pool_Blackboard.txt",
            "Week 03 - Docker Networking, Storage and Security"),
}


def deck_text(path):
    from pptx import Presentation
    prs = Presentation(os.path.join(ROOT, path))
    per = {}
    for i, s in enumerate(prs.slides, 1):
        buf = []
        for sh in s.shapes:
            if sh.has_text_frame and sh.text_frame.text.strip():
                t = sh.text_frame.text.strip()
                if t.startswith("CLO835, Fall"):
                    continue
                buf.append(t)
        per[i] = "\n".join(buf)
    return per


def norm(s):
    """Compare on letters and digits only, so spacing and dashes never matter."""
    return re.sub(r"[^a-z0-9]+", "", s.lower())


def verify(qs, per_slide, tag):
    errs = []
    stems = {}
    flat = norm("\n".join(per_slide.values()))
    for n, q in enumerate(qs, 1):
        where = "%s Q%d (slide %s)" % (tag, n, q["s"])
        if len(q["a"]) != 4:
            errs.append("%s: %d options, need 4" % (where, len(q["a"])))
        if len(set(q["a"])) != len(q["a"]):
            errs.append("%s: repeated option" % where)
        for f in [q["q"]] + list(q["a"]):
            if "\t" in f or "\n" in f:
                errs.append("%s: TAB or newline in a field" % where)
        k = norm(q["q"])
        if k in stems:
            errs.append("%s: duplicate stem, same as Q%d" % (where, stems[k]))
        stems[k] = n
        src = norm(q["src"])
        if src not in norm(per_slide.get(q["s"], "")):
            if src in flat:
                errs.append("%s: src is in the deck but NOT on slide %s" % (where, q["s"]))
            else:
                errs.append("%s: src NOT FOUND in the deck -> %r" % (where, q["src"]))
    return errs


def emit(qs, tag, title, outfile):
    lines, key = [], []
    for n, q in enumerate(qs, 1):
        seed = int(hashlib.md5((tag + q["q"]).encode()).hexdigest(), 16)
        idx = list(range(4))
        # deterministic Fisher-Yates
        for i in range(3, 0, -1):
            seed, j = divmod(seed, i + 1)
            idx[i], idx[j] = idx[j], idx[i]
        row = ["MC", q["q"]]
        for pos, src_i in enumerate(idx):
            row += [q["a"][src_i], "correct" if src_i == 0 else "incorrect"]
        lines.append("\t".join(row))
        letter = "ABCD"[idx.index(0)]
        key.append("%3d. [slide %2s] %s\n     ANSWER %s: %s"
                   % (n, q["s"], q["q"], letter, q["a"][0]))
    open(os.path.join(OUT, outfile), "w").write("\n".join(lines) + "\n")
    kf = outfile.replace("_Blackboard.txt", "_AnswerKey.txt")
    open(os.path.join(OUT, kf), "w").write(
        "CLO835 Fall 2026 - %s - question pool (%d questions)\n%s\n\n%s\n"
        % (title, len(qs), "=" * 66, "\n\n".join(key)))
    return outfile, kf


def select(qs, target=100):
    """Trim to exactly `target`, keeping the slide spread.

    Each slide keeps a share of `target` proportional to the number of
    questions written for it (largest remainder method), and within a slide the
    questions written first are kept. Every slide that has a question keeps at
    least one.
    """
    import collections
    order = []
    by = collections.OrderedDict()
    for q in qs:
        by.setdefault(q["s"], []).append(q)
    total = len(qs)
    if total <= target:
        return qs
    quota, rem = {}, {}
    for s, group in by.items():
        exact = len(group) * target / total
        quota[s] = max(1, int(exact))
        rem[s] = exact - int(exact)
    # trim or grow to hit target exactly
    while sum(quota.values()) > target:
        s = max((s for s in quota if quota[s] > 1), key=lambda s: (-quota[s], rem[s]))
        quota[s] -= 1
    while sum(quota.values()) < target:
        s = max(quota, key=lambda s: (rem[s], len(by[s]) - quota[s]))
        if quota[s] >= len(by[s]):
            rem[s] = -1
            continue
        quota[s] += 1
    out = []
    for s, group in by.items():
        out.extend(group[:quota[s]])
    return out


if __name__ == "__main__":
    import importlib
    total_err = 0
    for tag in ("W01", "W02", "W03"):
        mod = importlib.import_module("q_" + tag.lower())
        qs = select(mod.QUESTIONS, 100)
        path, outfile, title = DECKS[tag]
        per = deck_text(path)
        errs = verify(qs, per, tag)
        print("%s: %d questions, %d errors" % (tag, len(qs), len(errs)))
        for e in errs[:40]:
            print("   ", e)
        total_err += len(errs)
        if not errs:
            a, b = emit(qs, tag, title, outfile)
            print("    wrote %s and %s" % (a, b))
    sys.exit(1 if total_err else 0)
