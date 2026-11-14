# -*- coding: utf-8 -*-
"""CLO835 - build Blackboard question pools that stand on their own.

The first attempt failed. It checked that a question matched the deck. It never
checked that a student could answer the question WITHOUT the slide. This builder
rejects that whole class of question, plus four other defects.

GATE 1  Self-contained. The stem and the options may not point at a slide, a
        deck, a table, an agenda, a numbered step, or an earlier question.
GATE 2  Fact. The correct answer may not repeat a statement that is wrong in
        2026, even when a lecture slide says it.
GATE 3  No longest-answer giveaway. The correct option may be the strictly
        longest in at most 30 of 100 questions, and the strictly shortest in at
        most 30. Guessing by length must not pass.
GATE 4  No answer leak. The correct option may not share clearly more content
        words with the stem than every distractor does.
GATE 5  Structure. Four options, one correct, no repeat, no TAB, no newline,
        no repeated stem.
"""
import hashlib, re, sys, os, collections

OUT = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- GATE 1
BANNED_STEM = [
    "the deck", "this deck", "the slide", "on the slide", "the slides",
    "the table", "the lecture", "the example", "in the example", "that example",
    "the agenda", "the diagram", "the chart", "the scenario", "the course",
    "according to", "does the deck", "takeaway", "rule of thumb",
    "which other", "which second", "which third", "which fourth",
    "which fifth", "which sixth", "listed first", "listed second",
    "listed third", "listed fourth", "listed fifth", "listed sixth",
    "step 1", "step 2", "step 3", "step 4", "step 5", "step 6",
    "first step", "second step", "third step", "fourth step",
    "layer 1", "layer 2", "layer 3", "layer 4", "layer 5",
    "the week", "this week", "the figure", "shown above", "the list above",
    # added after the second review: these also point outside the question
    "in this model", "this split", "the two instructions", "which of the three",
    "of the three", "the three options", "that model", "this model",
]
BANNED_OPTION = ["the deck", "the slide", "the table", "the lecture"]

# ---------------------------------------------------------------- GATE 2
# A correct answer may never carry one of these. Each one is a statement that a
# lecture slide makes and that is wrong today.
BANNED_IN_CORRECT = [
    ("lowest layer", "a read is served by the HIGHEST layer that holds the file"),
    ("docker scan", "docker scan was removed in 2023; use docker scout or Trivy"),
    ("every instruction creates a layer", "only RUN, COPY and ADD create a filesystem layer"),
    ("each instruction creates a new layer", "only RUN, COPY and ADD create a filesystem layer"),
    ("must be the first instruction", "ARG may appear before FROM"),
    ("expose publishes", "EXPOSE documents a port; it does not publish it"),
]

STOP = set("""a an the and or of to in on for with that this these those is are was were be been
which what when where why how does do did can could will would should may might must into from
by as at it its their your you we our one two three four five first second third than then also
more most less least other another same different only not no yes about over under between each
every any all some both many much few after before while during until since because so such""".split())


def content_words(s):
    return {w for w in re.findall(r"[a-z0-9_.-]{5,}", s.lower()) if w not in STOP}


def verify(qs, tag, target=100):
    errs, warns = [], []
    stems = {}
    longest = shortest = 0
    for n, q in enumerate(qs, 1):
        w = "%s Q%d" % (tag, n)
        stem, opts = q["q"], q["a"]

        # GATE 5 - structure
        if len(opts) != 4:
            errs.append("%s: %d options" % (w, len(opts)))
            continue
        if len(set(opts)) != 4:
            errs.append("%s: repeated option" % w)
        for f in [stem] + list(opts):
            if "\t" in f or "\n" in f:
                errs.append("%s: TAB or newline" % w)
            if not f.strip():
                errs.append("%s: empty field" % w)
        k = re.sub(r"[^a-z0-9]+", "", stem.lower())
        if k in stems:
            errs.append("%s: duplicate stem of Q%d" % (w, stems[k]))
        stems[k] = n

        # GATE 1 - self-contained
        low = stem.lower()
        for b in BANNED_STEM:
            if b in low:
                errs.append("%s: stem points outside itself -> %r" % (w, b))
        for o in opts:
            for b in BANNED_OPTION:
                if b in o.lower():
                    errs.append("%s: option points outside itself -> %r" % (w, b))

        # GATE 2 - fact
        c = opts[0].lower()
        for bad, why in BANNED_IN_CORRECT:
            if bad in c:
                errs.append("%s: correct answer is wrong in 2026 (%s)" % (w, why))

        # GATE 3 - length tally
        L = [len(o) for o in opts]
        if L[0] > max(L[1:]):
            longest += 1
        if L[0] < min(L[1:]):
            shortest += 1

        # GATE 4 - answer leak
        sw = content_words(stem)
        share = [len(sw & content_words(o)) for o in opts]
        if share[0] - max(share[1:]) >= 2:
            errs.append("%s: answer leak, correct option repeats the stem wording" % w)

    # GATE 6 - one question may not hand over the answer to another in the same
    # pool: same correct answer AND a stem that overlaps heavily.
    import itertools
    def _w(t):
        return {x for x in re.findall(r"[a-z]{4,}", t.lower())}
    for i, j in itertools.combinations(range(len(qs)), 2):
        same = re.sub(r"[^a-z0-9]+", "", qs[i]["a"][0].lower()) == \
               re.sub(r"[^a-z0-9]+", "", qs[j]["a"][0].lower())
        A, B = _w(qs[i]["q"]), _w(qs[j]["q"])
        jac = len(A & B) / len(A | B) if (A | B) else 0
        if same and jac >= 0.50:
            errs.append("%s Q%d and Q%d: same answer and near-identical stem"
                        % (tag, i + 1, j + 1))

    if len(qs) != target:
        errs.append("%s: %d questions, need %d" % (tag, len(qs), target))
    pct = 100.0 * longest / max(1, len(qs))
    pcs = 100.0 * shortest / max(1, len(qs))
    if pct > 30:
        errs.append("%s: correct option is the longest in %d%% (limit 30%%)" % (tag, pct))
    if pcs > 30:
        errs.append("%s: correct option is the shortest in %d%% (limit 30%%)" % (tag, pcs))
    return errs, {"longest": longest, "shortest": shortest}


def emit(qs, tag, title, outfile):
    lines, key, pos = [], [], collections.Counter()
    for n, q in enumerate(qs, 1):
        seed = int(hashlib.md5((tag + q["q"]).encode()).hexdigest(), 16)
        idx = list(range(4))
        for i in range(3, 0, -1):
            seed, j = divmod(seed, i + 1)
            idx[i], idx[j] = idx[j], idx[i]
        row = ["MC", q["q"]]
        for s_i in idx:
            row += [q["a"][s_i], "correct" if s_i == 0 else "incorrect"]
        lines.append("\t".join(row))
        letter = "ABCD"[idx.index(0)]
        pos[letter] += 1
        key.append("%3d. [%s] %s\n     ANSWER %s: %s"
                   % (n, q["t"], q["q"], letter, q["a"][0]))
    open(os.path.join(OUT, outfile), "w").write("\n".join(lines) + "\n")
    kf = outfile.replace("_Blackboard.txt", "_AnswerKey.txt")
    open(os.path.join(OUT, kf), "w").write(
        "CLO835 Fall 2026 - %s - question pool (%d questions)\n"
        "Every question stands on its own. No question needs a slide.\n%s\n\n%s\n"
        % (title, len(qs), "=" * 70, "\n\n".join(key)))
    return pos


POOLS = {
    "W01": ("Week01_Pool_v2_Blackboard.txt", "Week 01 - Docker Introduction"),
    "W02": ("Week02_Pool_Blackboard.txt", "Week 02 - Docker Image Management"),
    "W03": ("Week03_Pool_Blackboard.txt", "Week 03 - Docker Networking, Storage and Security"),
}

def cross_pool(pools):
    """GATE 7 - the same fact must not sit in two pools, in case one test draws
    from more than one of them."""
    import itertools
    def _w(t):
        return {x for x in re.findall(r"[a-z]{4,}", t.lower())}
    out = []
    for (ta, qa), (tb, qb) in itertools.combinations(pools.items(), 2):
        for i, x in enumerate(qa, 1):
            for j, y in enumerate(qb, 1):
                same = re.sub(r"[^a-z0-9]+", "", x["a"][0].lower()) == \
                       re.sub(r"[^a-z0-9]+", "", y["a"][0].lower())
                A, B = _w(x["q"]), _w(y["q"])
                jac = len(A & B) / len(A | B) if (A | B) else 0
                if (same and jac >= 0.45) or jac >= 0.80:
                    out.append("%s Q%d and %s Q%d carry the same fact" % (ta, i, tb, j))
    return out


if __name__ == "__main__":
    import importlib
    bad = 0
    pools = {}
    for tag in ("W01", "W02", "W03"):
        pools[tag] = importlib.import_module("q2_" + tag.lower()).QUESTIONS
    xerrs = cross_pool(pools)
    print("cross-pool repeats: %d" % len(xerrs))
    for e in xerrs[:40]:
        print("   ", e)
    bad += len(xerrs)
    for tag in ("W01", "W02", "W03"):
        qs = pools[tag]
        errs, stat = verify(qs, tag)
        print("%s: %d questions | longest %d%% | shortest %d%% | %d errors"
              % (tag, len(qs), stat["longest"], stat["shortest"], len(errs)))
        for e in errs[:60]:
            print("   ", e)
        bad += len(errs)
        if not errs:
            outfile, title = POOLS[tag]
            pos = emit(qs, tag, title, outfile)
            print("    wrote %s | key position %s" % (outfile, dict(sorted(pos.items()))))
    sys.exit(1 if bad else 0)
