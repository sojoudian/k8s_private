"""Assemble week14/week14_deck.json (builder input) from the raw extraction + crop results,
and crop the diagram/screenshot figures from the hi-res source into week14/assets/.
Run from the bx14 sandbox (has week14/assets, w14src images via absolute path).
"""
import json, os
from PIL import Image

SB   = "/private/tmp/claude-501/-Users-maziar-Downloads-k8s-week3/4c65ef92-e3a8-40bf-9a8a-97634bbfb537/scratchpad"
SRC  = f"{SB}/w14src"
RAW  = f"{SB}/week14_deck_raw.json"
CROP = f"{SB}/week14_crops.json"          # {crops:[...]}
ASSETS = "week14/assets"                    # cwd-relative (run from bx14)

# Course-outline labels (slide 3), reading order (boustrophedon), VERBATIM per the user's
# 2026-07-27 slide-3 edit — adopted EXACTLY as shown (typos kept: "11:" w/o "Week", "SecretsWeek",
# two "Week 13" tiles). Week 1 highlighted.
OUTLINE = [
    "Week 1: Docker Introduction",
    "Week 2: Docker Image Management",
    "Week 3: Docker Networking, Storage & Security",
    "Week 4: K8s Introduction",
    "Week 5:K8s- PODs, ReplicaSets",
    "Week 6: K8s – Services & Deployments",
    "Week 7: K8s – Volumes",
    "Study Week",
    "Week 9: K8s- K8s- PVs & K8s in AKS",
    "Week 10: K8s: Storage classes & Statefulsets",
    "11: Exam & Mock Exam week",
    "Week 12: K8s- Configmaps & SecretsWeek",
    "Week 13: K8s – RBAC and AKS",
    "Week 13: Project presentation",
    "Week 14: Project presentation",
    "Term End",
]

# Dead-link replacements (eksworkshop.com restructured; /beginner/* now redirects to the homepage).
# Verified 2026-07-27: the 110_irsa content moved to the /docs/security/... path.
LINK_FIXES = {
    "https://www.eksworkshop.com/beginner/110_irsa/":
        "https://www.eksworkshop.com/docs/security/iam-roles-for-service-accounts/",
}

# Hand-curated fixes for slides the extractor structured wrong (filled after first render QA).
OVERRIDES = {
    # slide 24 is a fully-annotated screenshot (arrows+labels+title baked around it);
    # crop the whole thing and render full-bleed with no duplicate house title.
    24: {"title": ""},
    # slide 20 (HPA concept): keep the 3 VERBATIM source bullets, then ADD a teachable walkthrough
    # of the diagram's numbered control loop (1->2->3->4), which was only tiny text in the figure.
    20: {"body": [
        {"level": 0, "text": "HPA is the process of automatically adjusting the number of replicas based on the requested metric"},
        {"level": 0, "text": "Enabled and controlled by HorizontalPodAutoscaler resource"},
        {"level": 0, "text": "The HPA controller polls metrics server every 15 seconds and adjusts the number of replicas on the target resource (Deployment, ReplicaSet, Replication-Controller, or StatefulSet) to meet the target metric value"},
        {"level": 0, "text": "The control loop, step by step (numbers match the diagram):"},
        {"level": 1, "text": "Query the Metrics Server for each managed pod's current metric (e.g. CPU utilization)"},
        {"level": 1, "text": "Calculate the replica count needed to bring the metric to (or near) the target value"},
        {"level": 1, "text": "Update the replica count on the target's Scale sub-resource (Deployment \u2192 ReplicaSet)"},
        {"level": 1, "text": "The ReplicaSet then adds or removes Pods to reach the desired number"},
    ]},
    # slide 11 (kubeconfig CONCEPT) had ONLY the diagram, no text -> user asked for a teachable
    # explanation to be ADDED (intentional addition, not a source-verbatim change).
    11: {"body": [
        {"level": 0, "text": "kubeconfig is the file kubectl reads (by default ~/.kube/config) to decide WHICH cluster to contact, as WHICH user, and in WHICH namespace."},
        {"level": 0, "text": "It stores three independent lists:"},
        {"level": 1, "text": "Clusters \u2013 each is an API-server address + its CA certificate (the \"where\")."},
        {"level": 1, "text": "Users \u2013 each holds credentials: a client certificate, token, or auth plugin (the \"who\")."},
        {"level": 1, "text": "Contexts \u2013 a named bundle of one Cluster + one User + an optional namespace."},
        {"level": 0, "text": "kubectl uses the current-context by default; switch environments in one command:  kubectl config use-context <name>  (list them with kubectl config get-contexts)."},
        {"level": 0, "text": "In the diagram each Context links a User to a Cluster \u2013 e.g. Context 1 = User 1 on Cluster 1 (namespace dev), while Contexts 2 and 3 both target Cluster 2."},
        {"level": 0, "text": "One file can define many users, clusters, and contexts, and the same user or cluster may be reused by several contexts (here Users 2 and 4 are defined but unused)."},
    ]},
    # source textbox has a soft line-break (\x0b) between "configmap." and "check";
    # the image-extraction merged them. Restore the space (verbatim intent).
    8: {"title": "Map IAM User  to K8s user in aws-auth configmap. check  access to K8s API"},
}

COVER = 1
COURSE_OUTLINE = 3
REFERENCES = 29
# section-divider slides ("Workshop N– ...") and "End of workshop N" closings are set by the
# extractor's slide_type; nothing to force here unless QA finds a misclassification.
FORCE_SECTION_DIVIDER = set()
FORCE_CONTENT = set()
CROP_ADJUST = {}                            # per-slide pixel crop tweaks {n:{top:-40}}


def main():
    slides = json.load(open(RAW))["slides"]
    crops = {c["n"]: c for c in json.load(open(CROP)).get("crops", [])}

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
        if n == COVER:
            out["slide_type"] = "cover"
        elif n == COURSE_OUTLINE:
            out["slide_type"] = "course_outline"
            out["body"] = [{"level": 0, "text": t} for t in OUTLINE]
            out["highlight"] = [12]                # current week = "Week 13: K8s – RBAC and AKS" (this deck)
        elif n == REFERENCES:
            out["slide_type"] = "references"
        elif n in FORCE_SECTION_DIVIDER:
            out["slide_type"] = "section_divider"
        else:
            if n not in FORCE_CONTENT:
                out["slide_type"] = d.get("slide_type", "content")
            else:
                out["slide_type"] = "content"
            c = crops.get(n)
            if c and c.get("kind") in ("diagram","screenshot"):
                fname = f"fig{n}.png"; _crop(n, c, fname)
                out["figures"] = [{"file": fname, "desc": c.get("desc", "")}]
        if n in OVERRIDES:
            ov = OVERRIDES[n]
            for k in ("title", "body", "code_blocks", "slide_type", "figures"):
                if k in ov: out[k] = ov[k]
        # swap dead links (eksworkshop restructure)
        for b in out.get("body", []):
            if b.get("text") in LINK_FIXES:
                b["text"] = LINK_FIXES[b["text"]]
        deck.append(out)

    os.makedirs("week14", exist_ok=True)
    json.dump({"slides": deck}, open("week14/week14_deck.json", "w"), indent=1, ensure_ascii=False)
    nfig = sum(1 for d in deck if d["figures"])
    print(f"assembled {len(deck)} slides, {nfig} with cropped figures")


def _crop(n, c, fname):
    src = f"{SRC}/hi-{n:02d}.jpg"
    im = Image.open(src); W, H = im.size
    sw = W / c.get("img_w", W); sh = H / c.get("img_h", H)
    adj = CROP_ADJUST.get(n, {})
    l = max(0, int(c["left"] * sw) + adj.get("left", 0))
    t = max(0, int(c["top"] * sh) + adj.get("top", 0))
    r = min(W, int(c["right"] * sw) + adj.get("right", 0))
    b = min(H, int(c["bottom"] * sh) + adj.get("bottom", 0))
    if r - l < 20 or b - t < 20:
        l, t, r, b = int(W * 0.5), int(H * 0.18), W, int(H * 0.95)
    im.crop((l, t, r, b)).save(f"{ASSETS}/{fname}")


if __name__ == "__main__":
    main()
