# -*- coding: utf-8 -*-
"""Hand-picked set: the 20 hardest questions from the three Week 01-03 pools.

Chosen for reasoning, not recall. Each one needs a rule applied to a situation,
a counter-intuitive fact, or two similar things told apart.
The same gates run on this file as on the pools.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import q2_w01, q2_w02, q2_w03, build2

SRC = {"W01": q2_w01.QUESTIONS, "W02": q2_w02.QUESTIONS, "W03": q2_w03.QUESTIONS}

# (pool, a fragment that must match exactly one stem in that pool)
PICKS = [
 # ---- Week 01: kernel, layers, cache, Dockerfile traps ----
 ("W01", "capped at 512 MB of memory and cannot see host processes"),
 ("W01", "weaker than a virtual machine as an isolation boundary"),
 ("W01", "910 MB image share the same base"),
 ("W01", "reads a file that exists in three layers"),
 ("W01", "edits line 2 of a ten line Dockerfile"),
 ("W01", "copy the dependency list before the source code"),
 ("W01", "may legally appear before FROM"),
 # ---- Week 02: EXPOSE, publishing, CMD against ENTRYPOINT ----
 ("W02", "declares EXPOSE 8080 and is started with no port flag"),
 ("W02", "One serves on port 80, and nothing is published"),
 ("W02", "Two containers both need host port 8080"),
 ("W02", 'ENTRYPOINT ["python"] and CMD ["app.py"]'),
 ("W02", 'only CMD ["python", "app.py"]'),
 ("W02", "sets both ENTRYPOINT and CMD, and the user types nothing"),
 ("W02", "default command is a shell, and no terminal is attached"),
 # ---- Week 03: networking defaults, copy-on-write, storage ----
 ("W03", "cannot resolve the name redis"),
 ("W03", "two different user-defined networks try to resolve each other"),
 ("W03", "isolation default in Kubernetes"),
 ("W03", "edits a configuration file that arrived with the image"),
 ("W03", "does not exist, and -v is used"),
 ("W03", "Which kind of mounted data is lost with it"),
]


def pick():
    out = []
    for pool, frag in PICKS:
        hits = [q for q in SRC[pool] if frag in q["q"]]
        if len(hits) != 1:
            raise SystemExit("PICK MATCHED %d: %s / %r" % (len(hits), pool, frag))
        q = dict(hits[0])
        q["t"] = "%s - %s" % (pool, q["t"])
        out.append(q)
    return out


if __name__ == "__main__":
    qs = pick()
    errs, stat = build2.verify(qs, "HARD20", target=20)
    print("HARD20: %d questions | longest %d | shortest %d | %d errors"
          % (len(qs), stat["longest"], stat["shortest"], len(errs)))
    for e in errs:
        print("   ", e)
    # no two of the twenty may carry the same fact
    x = build2.cross_pool({"A": qs[:10], "B": qs[10:]})
    print("cross repeats inside the set: %d" % len(x))
    for e in x:
        print("   ", e)
    if errs or x:
        sys.exit(1)
    pos = build2.emit(qs, "HARD20", "Weeks 01-03 - 20 harder questions",
                      "CLO835_Hard20_Blackboard.txt")
    print("wrote CLO835_Hard20_Blackboard.txt | key position %s" % dict(sorted(pos.items())))
