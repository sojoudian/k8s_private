# -*- coding: utf-8 -*-
"""Replace a whole Q(...) entry in a question source file, found by its stem."""
import io, re

def load(p):
    return io.open(p, encoding="utf-8").read().split("\n")

def save(p, lines):
    io.open(p, "w", encoding="utf-8").write("\n".join(lines))

def find(lines, stem_fragment):
    hits = []
    for i, l in enumerate(lines):
        if l.startswith('Q(') and stem_fragment in l:
            j = i
            while not lines[j].rstrip().endswith("]),"):
                j += 1
            hits.append((i, j))
    return hits

def replace(lines, stem_fragment, new_entry):
    hits = find(lines, stem_fragment)
    if len(hits) != 1:
        raise SystemExit("MATCH %d for %r" % (len(hits), stem_fragment))
    i, j = hits[0]
    return lines[:i] + new_entry.rstrip("\n").split("\n") + lines[j+1:]

def apply_all(path, patches):
    lines = load(path)
    for frag, entry in patches:
        lines = replace(lines, frag, entry)
    save(path, lines)
    return len(patches)
