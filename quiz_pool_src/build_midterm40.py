# -*- coding: utf-8 -*-
"""CLO835 - build the 40 question mid-term exam (Weeks 01 to 06, 09 and 10).

A copy of build_easy20_w13.py, scaled from 20 to 40 questions (2026-11-14):
GATE 8 10 of each letter; GATE 8c each letter 2 or 3 times in each quarter of 10;
GATE 9 window 8 to 12; GATE 10 also checks the delivered upload files of the older
quizzes and exams (GATE 10b). The output folder is new, so nothing delivered changes.

It reuses the seven gates of build2.py and adds the gates that the design
rules ask for:

GATE 8   The key holds 5 A, 5 B, 5 C and 5 D, because an upload file cannot
         turn on option shuffling.
GATE 8b  No more than 3 equal letters stand together.
GATE 8c  Each letter is the key 2 or 3 times in each half, and no two letters
         alternate over 5 questions (review round 4).
GATE 9   The correct option is the strictly longest in 4 to 6 of the 20
         questions, and the strictly shortest in 4 to 6.
GATE 10  No question repeats a question of an earlier pool.
GATE 11  Each question carries the feedback: one reason for the correct
         option, and one mistake for each wrong option.
GATE 12  A question whose options form a number list, a time list or a name
         list keeps that logical order. The builder reads the order from the
         fix field, and it balances the letters with the other questions.
GATE 13  Each question carries a neutral title: an identifier and a topic.
         The title holds no option text.
"""
import os, re, sys, hashlib, collections, itertools, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build2 import verify

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "Exam_W11_Midterm40")
TAG = "M11"
PREFIX = "clo835-m11"
TITLE = "Mid-term exam - Weeks 01 to 10"
OUTFILE = "Exam_W11_Midterm40_Blackboard.txt"
OTHER_POOLS = ("q2_w01", "q2_w02", "q2_w03", "q3_quiz3", "q_easy20",
               "q_easy20_w34", "q_easy20_w56", "q_easy20_w09", "q_easy20_w10",
               "q_easy20_w12", "q_easy20_w13")
LETTERS = "ABCD"


def letters_for(qs, seed, run_limit=3):
    """Give one letter to each question.

    A question with a fix field keeps its logical order, so its letter
    follows from that order. The other questions take the letters that are
    left, and each letter holds the same count.
    """
    n = len(qs)
    per = n // 4
    fixed = {}
    for i, q in enumerate(qs):
        if "fix" in q:
            fixed[i] = LETTERS[q["fix"].index(q["a"][0])]
    pool = []
    for L in LETTERS:
        pool += [L] * (per - list(fixed.values()).count(L))
    if len(pool) != n - len(fixed):
        raise SystemExit("the fixed orders make the letter balance impossible")
    free = [i for i in range(n) if i not in fixed]
    rng = random.Random(int(hashlib.md5(seed.encode()).hexdigest(), 16))
    for _ in range(400000):
        rng.shuffle(pool)
        out = dict(fixed)
        out.update(dict(zip(free, pool)))
        order = [out[i] for i in range(n)]
        if max(len(list(g)) for _, g in itertools.groupby(order)) <= run_limit \
                and halves_ok(order) and not alternation(order):
            return order
    raise SystemExit("no balanced order found")


def halves_ok(order):
    """GATE 8c - each letter is the key 2 or 3 times in each block of 10 questions
    (the rule of the 20 question quizzes, applied to each quarter of the 40)."""
    parts = [order[i:i + 10] for i in range(0, len(order), 10)]
    return all(2 <= part.count(L) <= 3 for part in parts for L in LETTERS)


def alternation(order):
    """GATE 8c - no two letters alternate over 5 questions (x y x y x, round 4),
    no 4 letters in alphabet order (A B C D or D C B A, round 5), and no block
    of 3 letters that repeats at once (x y z x y z, round 5)."""
    n = len(order)
    if any(order[i] == order[i + 2] == order[i + 4] and order[i + 1] == order[i + 3]
           and order[i] != order[i + 1] for i in range(n - 4)):
        return True
    if any("".join(order[i:i + 4]) in ("ABCD", "DCBA") for i in range(n - 3)):
        return True
    return any(order[i:i + 3] == order[i + 3:i + 6] for i in range(n - 5))


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


TXT_POOLS = ("../CLO835_Final_Exam_Blackboard.txt", "../CLO835_Final_Exam_v2_Blackboard.txt",
             "../CLO835_Hard20_Blackboard.txt", "../week01/Week01_Quiz_Blackboard.txt",
             "../week01/Week01_Quiz_v2_Blackboard.txt", "../Week04/FINAL/Week04_Quiz_Blackboard.txt",
             "../Week04/FINAL/Week04_Quiz_v2_Blackboard.txt", "../Week09/Week08_Quiz_Blackboard.txt")


def txt_pools(qs):
    """GATE 10b - against the delivered upload files that have no Python source."""
    def _w(t):
        return {x for x in re.findall(r"[a-z]{4,}", t.lower())}
    out = []
    for rel in TXT_POOLS:
        path = os.path.join(HERE, rel)
        for j, line in enumerate(open(path, encoding="utf8", errors="replace"), 1):
            f = line.rstrip("\n").split("\t")
            if len(f) < 3:
                continue
            keys = [f[k - 1] for k in range(3, len(f)) if f[k] == "correct"] if f[0] in ("MC", "MA") else [f[2]]
            for i, x in enumerate(qs, 1):
                A, B = _w(x["q"]), _w(f[1])
                jac = len(A & B) / len(A | B) if (A | B) else 0
                same = any(re.sub(r"[^a-z0-9]+", "", x["a"][0].lower()) == re.sub(r"[^a-z0-9]+", "", k.lower())
                           for k in keys)
                if (same and jac >= 0.45) or jac >= 0.80:
                    out.append("%s Q%d repeats %s row %d" % (TAG, i, os.path.basename(rel), j))
    return out


def html_gate(qs):
    """GATE 14 - Blackboard reads the upload text as HTML. A < , > or & in a
    stem or an option breaks the question ("Content Error")."""
    out = []
    for n, q in enumerate(qs, 1):
        for f in [q["q"]] + list(q["a"]):
            if re.search(r"[<>&]", f):
                out.append("%s Q%d: HTML character in %r" % (TAG, n, f[:50]))
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
        if len(set(mis)) != len(mis):
            out.append("%s Q%d: two wrong options carry one mistake text" % (TAG, n))
        for bad in ("slide", "week ", "deck", "lecture"):
            if bad in (q.get("why", "") + " ".join(mis)).lower():
                out.append("%s Q%d: the feedback points at a slide or a week" % (TAG, n))
    return out


def order_gate(qs):
    """GATE 12 - a fixed order must hold the same four options."""
    out = []
    for n, q in enumerate(qs, 1):
        if "fix" in q and sorted(q["fix"]) != sorted(q["a"]):
            out.append("%s Q%d: the fixed order and the options do not agree" % (TAG, n))
    return out


def title_gate(qs):
    """GATE 13 - a title gives an identifier and a topic only."""
    out = []
    for n, q in enumerate(qs, 1):
        t = title_of(n, q)
        if not re.match(r"^%s-\d{3} [a-z][a-z ]*$" % PREFIX, t):
            out.append("%s Q%d: bad title form -> %r" % (TAG, n, t))
        for o in q["a"]:
            if o.lower() in t.lower():
                out.append("%s Q%d: the title holds an option" % (TAG, n))
    return out


def title_of(n, q):
    """Give the neutral title of one question."""
    return "%s-%03d %s" % (PREFIX, n, q["t"])


def emit(qs, tag, title, outfile):
    order = letters_for(qs, tag + title)
    lines, key, titles, pos = [], [], [], collections.Counter()
    for n, (q, letter) in enumerate(zip(qs, order), 1):
        if "fix" in q:
            opts = list(q["fix"])
        else:
            target = LETTERS.index(letter)
            wrong = list(q["a"][1:])
            idx = list(range(3))
            s = int(hashlib.md5((tag + q["q"]).encode()).hexdigest(), 16)
            for i in range(2, 0, -1):
                s, j = divmod(s, i + 1)
                idx[i], idx[j] = idx[j], idx[i]
            wrong = [wrong[i] for i in idx]
            opts = wrong[:target] + [q["a"][0]] + wrong[target:]
        if LETTERS[opts.index(q["a"][0])] != letter:
            raise SystemExit("Q%d: the letter and the option order do not agree" % n)
        row = ["MC", q["q"]]
        for o in opts:
            row += [o, "correct" if o == q["a"][0] else "incorrect"]
        lines.append("\t".join(row))
        pos[letter] += 1
        titles.append(title_of(n, q))

        block = ["%3d. [%s] %s" % (n, title_of(n, q), q["q"])]
        for i, o in enumerate(opts):
            block.append("   %s %s. %s" % ("*" if o == q["a"][0] else " ",
                                           LETTERS[i], o))
        block.append("     ANSWER %s" % letter)
        block.append("     WHY: %s" % q["why"])
        for w, mi in zip(q["a"][1:], q["mis"]):
            block.append("     IF %s: %s" % (LETTERS[opts.index(w)], mi))
        key.append("\n".join(block))

    if not os.path.isdir(OUT):
        os.makedirs(OUT)
    open(os.path.join(OUT, outfile), "w").write("\n".join(lines) + "\n")
    open(os.path.join(OUT, outfile.replace("_Blackboard.txt", "_Titles.txt")),
         "w").write("\n".join(titles) + "\n")
    open(os.path.join(OUT, outfile.replace("_Blackboard.txt", "_AnswerKey.txt")),
         "w").write(
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
    import q_midterm40 as source
    qs = source.QUESTIONS
    bad = 0

    errs, stat = verify(qs, TAG, target=40)
    print("GATE 1-7 : %d questions, %d errors" % (len(qs), len(errs)))
    for e in errs[:40]:
        print("    ", e)
    bad += len(errs)

    for name, fn in (("GATE 10 ", cross_pools), ("GATE 10b", txt_pools),
                     ("GATE 14 ", html_gate), ("GATE 11 ", feedback_gate),
                     ("GATE 12 ", order_gate), ("GATE 13 ", title_gate)):
        e = fn(qs)
        print("%s : %d errors" % (name, len(e)))
        for x in e[:20]:
            print("    ", x)
        bad += len(e)

    lo, hi = 8, 12
    print("GATE 9   : longest %d, shortest %d (window %d-%d)"
          % (stat["longest"], stat["shortest"], lo, hi))
    if not lo <= stat["longest"] <= hi or not lo <= stat["shortest"] <= hi:
        print("     FAIL"); bad += 1

    if bad:
        print("\n%d problems. Nothing written." % bad)
        sys.exit(1)

    pos = emit(qs, TAG, TITLE, OUTFILE)
    print("GATE 8   : key per letter %s" % dict(sorted(pos.items())))
    if sorted(pos.values()) != [10, 10, 10, 10]:
        print("     FAIL"); sys.exit(1)
    order = letters_for(qs, TAG + TITLE)
    run = max(len(list(g)) for _, g in itertools.groupby(order))
    print("GATE 8b  : longest run of one letter %d (limit 3)" % run)
    print("GATE 8c  : quarters %s, alternation, ABCD run or repeated block: %s"
          % (" / ".join("".join(sorted(order[i:i + 10])) for i in range(0, 40, 10)), alternation(order)))
    if not halves_ok(order) or alternation(order):
        print("     FAIL"); sys.exit(1)
    fixed = sum(1 for q in qs if "fix" in q)
    print("GATE 12  : %d questions keep a logical option order" % fixed)
    print("wrote %s, the titles and the answer key" % OUTFILE)
