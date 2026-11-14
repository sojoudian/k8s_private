# -*- coding: utf-8 -*-
"""CLO835 - build the 20 question easy quiz for Blackboard.

It reuses the seven gates of build2.py and adds the gates that the design
rules ask for:

GATE 8   The key holds 5 A, 5 B, 5 C and 5 D, because an upload file cannot
         turn on option shuffling.
GATE 8b  No more than 3 equal letters stand together.
GATE 9   The correct option is the strictly longest in 4 to 6 of the 20
         questions, and the strictly shortest in 4 to 6.
GATE 10  No question repeats a question of the Docker pools or of the Quiz 3
         pool.
GATE 11  Each question carries the feedback: one reason for the correct
         option, and one mistake for each wrong option.
"""
import os, re, sys, hashlib, collections, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build2 import verify

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "Quiz_W03W04_Easy20")
TAG = "E34"
TITLE = "Easy quiz - Docker Networking, Storage, Security and Kubernetes Introduction"
OUTFILE = "Quiz_W03W04_Easy20_v2_Blackboard.txt"
OTHER_POOLS = ("q2_w01", "q2_w02", "q2_w03", "q3_quiz3", "q_easy20")


def balanced_letters(n, seed, run_limit=3):
    """n letters, an equal share of A, B, C and D, in a fixed order."""
    import random
    per = n // 4
    letters = ["A"] * per + ["B"] * per + ["C"] * per + ["D"] * per
    rng = random.Random(int(hashlib.md5(seed.encode()).hexdigest(), 16))
    for _ in range(1000):
        rng.shuffle(letters)
        if max(len(list(g)) for _, g in itertools.groupby(letters)) <= run_limit:
            return letters
    raise SystemExit("no balanced order found")


def cross_pools(qs):
    """GATE 10 - against the pools that already exist."""
    import importlib
    def _w(t):
        return {x for x in re.findall(r"[a-z]{4,}", t.lower())}
    out = []
    for other in OTHER_POOLS:
        og = importlib.import_module(other).QUESTIONS
        for i, x in enumerate(qs, 1):
            for j, y in enumerate(og, 1):
                same = re.sub(r"[^a-z0-9]+", "", x["a"][0].lower()) == \
                       re.sub(r"[^a-z0-9]+", "", y["a"][0].lower())
                A, B = _w(x["q"]), _w(y["q"])
                jac = len(A & B) / len(A | B) if (A | B) else 0
                if (same and jac >= 0.45) or jac >= 0.80:
                    out.append("%s Q%d repeats %s Q%d" % (TAG, i, other, j))
    return out


def feedback_gate(qs):
    """GATE 11 - the feedback must be complete."""
    out = []
    for n, q in enumerate(qs, 1):
        if not q.get("why", "").strip():
            out.append("%s Q%d: no reason for the correct option" % (TAG, n))
        mis = q.get("mis", [])
        if len(mis) != 3 or not all(m.strip() for m in mis):
            out.append("%s Q%d: the wrong options have no mistake text" % (TAG, n))
        for bad in ("slide", "week ", "deck", "lecture"):
            if bad in (q.get("why", "") + " ".join(mis)).lower():
                out.append("%s Q%d: the feedback points at a slide or a week" % (TAG, n))
    return out


def emit(qs, tag, title, outfile):
    letters = balanced_letters(len(qs), tag + title)
    lines, key, pos = [], [], collections.Counter()
    for n, (q, letter) in enumerate(zip(qs, letters), 1):
        target = "ABCD".index(letter)
        wrong = list(q["a"][1:])
        order = list(range(3))
        s = int(hashlib.md5((tag + q["q"]).encode()).hexdigest(), 16)
        for i in range(2, 0, -1):
            s, j = divmod(s, i + 1)
            order[i], order[j] = order[j], order[i]
        wrong = [wrong[i] for i in order]
        mis = [q["mis"][i] for i in order]
        opts = wrong[:target] + [q["a"][0]] + wrong[target:]
        row = ["MC", q["q"]]
        for o in opts:
            row += [o, "correct" if o == q["a"][0] else "incorrect"]
        lines.append("\t".join(row))
        pos[letter] += 1

        shown = "ABCD"
        block = ["%3d. [%s] %s" % (n, q["t"], q["q"])]
        for i, o in enumerate(opts):
            mark = "*" if o == q["a"][0] else " "
            block.append("   %s %s. %s" % (mark, shown[i], o))
        block.append("     ANSWER %s" % letter)
        block.append("     WHY: %s" % q["why"])
        for w, m in zip(wrong, mis):
            block.append("     IF %s: %s" % (shown[opts.index(w)], m))
        key.append("\n".join(block))

    open(os.path.join(OUT, outfile), "w").write("\n".join(lines) + "\n")
    kf = outfile.replace("_Blackboard.txt", "_AnswerKey.txt")
    open(os.path.join(OUT, kf), "w").write(
        "CLO835 Fall 2026 - %s\n"
        "%d questions. Every student gets all of them.\n"
        "Every question stands on its own. No question needs a slide.\n"
        "Correct answers per letter: %s\n"
        "The star marks the correct option. WHY gives the reason. IF gives the "
        "mistake behind a wrong option.\n%s\n\n%s\n"
        % (title, len(qs), dict(sorted(pos.items())), "=" * 70,
           "\n\n".join(key)))
    return pos


if __name__ == "__main__":
    import q_easy20_w34 as q_easy20
    qs = q_easy20.QUESTIONS
    bad = 0

    errs, stat = verify(qs, TAG, target=20)
    print("GATE 1-7 : %d questions, %d errors" % (len(qs), len(errs)))
    for e in errs[:40]:
        print("    ", e)
    bad += len(errs)

    xe = cross_pools(qs)
    print("GATE 10  : %d repeats of an earlier pool" % len(xe))
    for e in xe[:20]:
        print("    ", e)
    bad += len(xe)

    fe = feedback_gate(qs)
    print("GATE 11  : %d feedback errors" % len(fe))
    for e in fe[:20]:
        print("    ", e)
    bad += len(fe)

    lo, hi = 4, 6
    print("GATE 9   : correct option is the longest in %d (window %d-%d), "
          "shortest in %d" % (stat["longest"], lo, hi, stat["shortest"]))
    if not lo <= stat["longest"] <= hi:
        print("     FAIL"); bad += 1
    if not lo <= stat["shortest"] <= hi:
        print("     FAIL"); bad += 1

    if bad:
        print("\n%d problems. Nothing written." % bad)
        sys.exit(1)

    pos = emit(qs, TAG, TITLE, OUTFILE)
    print("GATE 8   : key per letter %s" % dict(sorted(pos.items())))
    if sorted(pos.values()) != [5, 5, 5, 5]:
        print("     FAIL"); sys.exit(1)
    order = balanced_letters(len(qs), TAG + TITLE)
    run = max(len(list(g)) for _, g in itertools.groupby(order))
    print("GATE 8b  : longest run of one letter %d (limit 3)" % run)
    if run > 3:
        print("     FAIL"); sys.exit(1)
    print("wrote %s and the answer key" % OUTFILE)
