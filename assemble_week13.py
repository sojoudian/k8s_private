"""Assemble week13_deck.json (builder input) from the raw extraction + crop/truncation results,
and crop the diagram figures from the hi-res source into week13/assets/.
Run from the bx13 sandbox (has week13/assets, w13src images via absolute path).
"""
import json, os
from PIL import Image

SB   = "/private/tmp/claude-501/-Users-maziar-Downloads-k8s-week3/4c65ef92-e3a8-40bf-9a8a-97634bbfb537/scratchpad"
SRC  = f"{SB}/w13src"
RAW  = f"{SB}/week13_deck_raw.json"
CROP = f"{SB}/week13_crops.json"          # {crops:[...], truncated:[...]}
ASSETS = "week13/assets"                   # cwd-relative (run from bx13)

# Verbatim course-outline labels (slide 3), en-dashes/typos preserved
OUTLINE = [
    "Week 1: Docker Introduction",
    "Week 2: Docker Image Management",
    "Week 3: Docker Networking, Storage & Security",
    "Week 4: K8s Introduction",
    "Week 5:K8s- PODs, ReplicaSets",
    "Week 6: K8s – Services & Deployments",
    "Week 7: K8s – Volumes",
    "Study Week",
    # user's slide-3 edit (2026-07-20): weeks 8-13 renumbered +1; last tile -> Project presentation
    "Week 9: K8s- K8s- PVs & K8s in AKS",
    "Week 10: K8s: Storage classes & Statefulsets",
    "Week 11: K8s- Configmaps & Secrets",
    "Week 12: Exam & Mock Exam week",
    "Week 13: K8s – RBAC and AKS",
    "Week 14: K8s – HPA",
    "Week 14: Project presentation",
    "Term End",
]

# Hand-curated fixes for slides the extractor structured wrong.
OVERRIDES = {
    # slide 10's real title was captured as the first body bullet -> restore it
    10: {"title": "Image Pull secret used to authenticate against private registries",
         "body": [{"level": 0, "text": "Only mountable secrets can be mounted into containers"}]},
}

SECTION_DIVIDERS = {36}   # 21 has a diagram -> treat as content, not a bare divider
FORCE_CONTENT = {21}      # extraction called 21 a divider, but it carries an RBAC diagram
# per-slide crop tweaks (pixels): expand top so clipped headers show fully
CROP_ADJUST = {27: {"top": -55}}
COVER = 1
COURSE_OUTLINE = 3
REFERENCES = 45

def main():
    slides = json.load(open(RAW))["slides"]
    crops = {c["n"]: c for c in json.load(open(CROP)).get("crops", [])}
    truncs = {t["n"]: t for t in json.load(open(CROP)).get("truncated", [])}

    os.makedirs(ASSETS, exist_ok=True)
    deck = []
    for d in slides:
        n = d["n"]
        out = {
            "n": n, "hidden": bool(d.get("hidden")),
            "title": d.get("title", ""),
            "slide_type": d.get("slide_type", "content"),
            "body": d.get("body", []),
            "code_blocks": d.get("code_blocks", []),
            "figures": [],
        }
        # ---- special slide types ----
        if n == COVER:
            out["slide_type"] = "cover"; out["figures"] = []
        elif n == COURSE_OUTLINE:
            out["slide_type"] = "course_outline"
            out["body"] = [{"level": 0, "text": t} for t in OUTLINE]
            out["highlight"] = [0]              # source highlights Week 1 (faithful)
            out["figures"] = []
        elif n in SECTION_DIVIDERS:
            out["slide_type"] = "section_divider"; out["figures"] = []
        elif n in FORCE_CONTENT:
            out["slide_type"] = "content"
            c = crops.get(n)
            if c and c.get("kind") == "diagram":
                fname = f"fig{n}.png"; _crop(n, c, fname)
                out["figures"] = [{"file": fname, "desc": c.get("desc", "")}]
        elif n == REFERENCES:
            out["slide_type"] = "references"; out["figures"] = []
        else:
            # ---- crop diagram if flagged and not "drop" ----
            c = crops.get(n)
            if c and c.get("kind") == "diagram":
                fname = f"fig{n}.png"
                _crop(n, c, fname)
                out["figures"] = [{"file": fname, "desc": c.get("desc", "")}]
            else:
                out["figures"] = []
            # NOTE: truncated-slide code (12,13,19,22,28,42) is hand-curated in OVERRIDES
            # below, because the auto re-read mixed bullets + annotations + terminal text.
            if n in OVERRIDES:
                ov = OVERRIDES[n]
                if "title" in ov: out["title"] = ov["title"]
                if "body" in ov: out["body"] = ov["body"]
                if "code_blocks" in ov: out["code_blocks"] = ov["code_blocks"]
        deck.append(out)

    json.dump({"slides": deck}, open("week13/week13_deck.json", "w"),
              indent=1, ensure_ascii=False)
    nfig = sum(1 for d in deck if d["figures"])
    print(f"assembled {len(deck)} slides, {nfig} with cropped figures")


def _crop(n, c, fname):
    src = f"{SRC}/hi-{n:02d}.jpg"
    im = Image.open(src)
    W, H = im.size
    # scale box coords to actual image size (agent may report a different reference size)
    sw = W / c.get("img_w", W); sh = H / c.get("img_h", H)
    adj = CROP_ADJUST.get(n, {})
    l = max(0, int(c["left"] * sw) + adj.get("left", 0))
    t = max(0, int(c["top"] * sh) + adj.get("top", 0))
    r = min(W, int(c["right"] * sw) + adj.get("right", 0))
    b = min(H, int(c["bottom"] * sh) + adj.get("bottom", 0))
    if r - l < 20 or b - t < 20:   # guard against a degenerate box
        l, t, r, b = int(W*0.5), int(H*0.18), W, int(H*0.95)
    im.crop((l, t, r, b)).save(f"{ASSETS}/{fname}")


if __name__ == "__main__":
    main()
