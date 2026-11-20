import sys
sys.path.insert(0, "/Users/maziar/Documents/c/r/k8s_private")
import gate_week12 as g
folder, stem = sys.argv[1].strip("/"), sys.argv[2]
kind = sys.argv[3] if len(sys.argv) > 3 else "lecture"
g.ROOT = "/Users/maziar/Documents/c/r/k8s_private/%s/" % folder
g.deck_checks(stem, kind)
print("FAILED:", len(g.FAILS))
