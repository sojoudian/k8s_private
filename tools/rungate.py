import sys
sys.path.insert(0, "/Users/maziar/Downloads/k8s_week3")
import gate_week12 as g
folder, stem = sys.argv[1].strip("/"), sys.argv[2]
kind = sys.argv[3] if len(sys.argv) > 3 else "lecture"
g.ROOT = "/Users/maziar/Downloads/k8s_week3/%s/" % folder
g.deck_checks(stem, kind)
print("FAILED:", len(g.FAILS))
