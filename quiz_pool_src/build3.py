# -*- coding: utf-8 -*-
"""CLO835 - build the Quiz 3 pool for Blackboard.

It reuses the seven gates of build2.py and adds three gates that the Quiz 3
rules ask for:

GATE 8   The key holds 25 A, 25 B, 25 C and 25 D. The upload file cannot turn
         on option shuffling, so the builder balances the key itself.
GATE 9   The correct option is the strictly longest option in 20 to 30 of the
         100 questions. It is never always the longest and never never.
GATE 10  No question of this pool carries a fact of the Docker pools.
"""
import os, re, sys, hashlib, collections, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build2 import verify, content_words   # the gates of the earlier pools

OUT = os.path.dirname(os.path.abspath(__file__))
TAG = "Q3"
TITLE = ("Quiz 3 pool - Pods, Labels, Namespaces, ReplicaSets, Deployments, "
         "Rollouts, Services, Ingress, Volumes")
OUTFILE = "Quiz03_Pool_Blackboard.txt"


def balanced_letters(n, seed):
    """n letters, equal share of A B C D, in a fixed order.

    An md5 integer holds about 38 decimal digits. It runs out after some 25
    divisions, so a hand made shuffle leaves the tail of a 100 item list in
    order. This function uses a generator with a fixed seed instead, and it
    rejects an order that puts more than 4 equal letters together.
    """
    import random
    per = n // 4
    letters = ["A"] * per + ["B"] * per + ["C"] * per + ["D"] * per
    rng = random.Random(int(hashlib.md5(seed.encode()).hexdigest(), 16))
    for _ in range(1000):
        rng.shuffle(letters)
        if max(len(list(g)) for _, g in itertools.groupby(letters)) <= 4:
            return letters
    raise SystemExit("no balanced order found")


def emit(qs, tag, title, outfile):
    letters = balanced_letters(len(qs), tag + title)
    lines, key, pos = [], [], collections.Counter()
    for n, (q, letter) in enumerate(zip(qs, letters), 1):
        target = "ABCD".index(letter)
        wrong = list(q["a"][1:])
        s = int(hashlib.md5((tag + q["q"]).encode()).hexdigest(), 16)
        for i in range(len(wrong) - 1, 0, -1):          # fixed order of the three
            s, j = divmod(s, i + 1)
            wrong[i], wrong[j] = wrong[j], wrong[i]
        opts = wrong[:target] + [q["a"][0]] + wrong[target:]
        row = ["MC", q["q"]]
        for o in opts:
            row += [o, "correct" if o == q["a"][0] else "incorrect"]
        lines.append("\t".join(row))
        pos[letter] += 1
        key.append("%3d. [%s] %s\n     ANSWER %s: %s"
                   % (n, q["t"], q["q"], letter, q["a"][0]))
    open(os.path.join(OUT, outfile), "w").write("\n".join(lines) + "\n")
    kf = outfile.replace("_Blackboard.txt", "_AnswerKey.txt")
    open(os.path.join(OUT, kf), "w").write(
        "CLO835 Fall 2026 - %s\n"
        "%d questions. Blackboard draws 20 of them at random, 5 points each.\n"
        "Every question stands on its own. No question needs a slide.\n"
        "Correct answers per letter: %s\n%s\n\n%s\n"
        % (title, len(qs), dict(sorted(pos.items())), "=" * 70,
           "\n\n".join(key)))
    return pos


def cross_docker(qs):
    """GATE 10 - against the three Docker pools."""
    import importlib
    def _w(t):
        return {x for x in re.findall(r"[a-z]{4,}", t.lower())}
    out = []
    for other in ("q2_w01", "q2_w02", "q2_w03"):
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


if __name__ == "__main__":
    import q3_quiz3
    qs = q3_quiz3.QUESTIONS
    bad = 0

    errs, stat = verify(qs, TAG, target=100)
    print("GATE 1-7 : %d questions, %d errors" % (len(qs), len(errs)))
    for e in errs[:80]:
        print("    ", e)
    bad += len(errs)

    xe = cross_docker(qs)
    print("GATE 10  : %d repeats of a Docker pool" % len(xe))
    for e in xe[:20]:
        print("    ", e)
    bad += len(xe)

    lo, hi = 20, 30
    print("GATE 9   : correct option is the longest in %d (window %d-%d), "
          "shortest in %d" % (stat["longest"], lo, hi, stat["shortest"]))
    if not lo <= stat["longest"] <= hi:
        print("     FAIL"); bad += 1

    if bad:
        print("\n%d problems. Nothing written." % bad)
        sys.exit(1)

    pos = emit(qs, TAG, TITLE, OUTFILE)
    print("GATE 8   : key per letter %s" % dict(sorted(pos.items())))
    if sorted(pos.values()) != [25, 25, 25, 25]:
        print("     FAIL"); sys.exit(1)
    key_order = [l for l in balanced_letters(len(qs), TAG + TITLE)]
    run = max(len(list(g)) for _, g in itertools.groupby(key_order))
    print("GATE 8b  : longest run of one letter %d (limit 4)" % run)
    if run > 4:
        print("     FAIL"); sys.exit(1)
    print("wrote %s and the answer key" % OUTFILE)
