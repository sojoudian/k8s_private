#!/usr/bin/env python3
"""CLO835 - guess strategies on a Blackboard upload file (tab-delimited, MC rows).

Usage: python3 -I quiz_cue_sim.py <Quiz_..._Blackboard.txt>

Each strategy picks one option in each question, without any knowledge. A tie
shares the point (1/k). The script shows the score of each strategy and exits 1
when one strategy scores more than 30 % of the questions (6.0 of 20).

Strategies: always A, B, C, D; the longest and the shortest option (characters);
the most and the fewest words; the middle length; the most words shared with the
stem; the convergence centre (the most words shared with the other options),
raw and with simple stemming; and the option that shares the fewest words with
the others (the odd one out).
Based on the round 5 to round 8 review scripts of the Week 10 quiz (2026-11-10).
"""
import re
import sys

STOP = set("a an the and or of to in on for with that this is are be it its by as at from "
           "but each one no not only".split())


def words(s, stem=False):
    out = set()
    for w in re.findall(r"[a-z0-9]+(?:[.:-][a-z0-9]+)*", s.lower()):
        if w in STOP or len(w) < 3:
            continue
        if stem:
            for suf in ("ing", "es", "ed", "s"):
                if len(w) > 4 and w.endswith(suf):
                    w = w[:-len(suf)]
                    break
        out.add(w)
    return out


def main(path):
    rows = [l.rstrip("\n").split("\t") for l in open(path) if l.strip()]
    tot = {}

    def share(name, scores, k, best=max):
        b = best(scores)
        if scores[k] == b:
            tot[name] = tot.get(name, 0.0) + 1.0 / scores.count(b)
        else:
            tot.setdefault(name, 0.0)

    for f in rows:
        opts = [f[2], f[4], f[6], f[8]]
        k = [f[3], f[5], f[7], f[9]].index("correct")
        for i, L in enumerate("ABCD"):
            tot["always " + L] = tot.get("always " + L, 0.0) + (1.0 if i == k else 0.0)
        ln = [len(o) for o in opts]
        wd = [len(o.split()) for o in opts]
        share("longest", ln, k)
        share("shortest", ln, k, min)
        share("most words", wd, k)
        share("fewest words", wd, k, min)
        mid = sorted(ln)
        middle = [-abs(x - (mid[1] + mid[2]) / 2.0) for x in ln]
        share("middle length", middle, k)
        sw = words(f[1])
        share("stem overlap", [len(sw & words(o)) for o in opts], k)
        for stem in (False, True):
            conv = [sum(len(words(o, stem) & words(p, stem)) for j, p in enumerate(opts) if j != i)
                    for i, o in enumerate(opts)]
            share("convergence" + (" (stemmed)" if stem else ""), conv, k)
        conv = [sum(len(words(o) & words(p)) for j, p in enumerate(opts) if j != i) for i, o in enumerate(opts)]
        share("odd one out", conv, k, min)

    n = len(rows)
    limit = 0.30 * n
    bad = 0
    for name in sorted(tot):
        flag = "FAIL" if tot[name] > limit + 1e-9 else "ok"
        bad += flag == "FAIL"
        print("%-22s %5.2f of %d  %s" % (name, tot[name], n, flag))
    print("limit %.1f of %d (30 %%): %s" % (limit, n, "FAIL" if bad else "PASS"))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
