"""Week14 (source self-labels "Week 12") — Introduction to K8s RBAC, Continued + HPA + IRSA.

Redesign of week14/Week12.pptx into the exact CLO835 Lab02 house design, v1 = one combined deck
like the other weeks' v1 (content untouched, verbatim per PROMPT.md R1). Reuses the proven, guarded
build_week12 engine (import is guarded → never rebuilds week12) for the palette, coord guard,
terminal/bullets/divider/closing/course-outline helpers — exactly as build_week13 did.

Genuine diagrams + AWS-console screenshots (HPA autoscaling, IAM policy pages) are cropped from the
source and embedded as-is; terminal/YAML/kubectl/aws-cli content is rebuilt as house terminal
mockups from the verbatim transcription. Hidden source slides (23,24) stay hidden.

Content lives in week14/week14_deck.json (built from the extraction). Run from a dir with whale.png,
Week04/<logo>, and week14/assets/ (the sandbox). Sandbox only — cwd-relative save.
"""

import os, json, re
from PIL import Image
import build_week12 as bw
from build_week12 import (
    Inches, Pt, BLUE, SLATE, WHITE, MUTED, BODY, CARD_BG, RULE_GRAY, LIGHTBLUE, FOOTER_GRAY,
    FONT_SANS, FONT_MONO, K8S_LOGO, WHALE,
    CENTER, LEFT, RIGHT, MIDDLE, TOP,
    title, bullets, auto_term, divider, closing,
    course_outline, whale_and_footer, add_text, add_rect, add_oval, add_line, smart_title,
    _sanitize_coords,
)

VERSION    = "v10"
FIG_BOX    = {}                                  # per-source-slide figure-box overrides (x,y,w,h)
WEEK_LABEL = "Week 12"                           # source self-labels this Week 12 (folder week14)
DECK_TITLE = "Introduction to K8s RBAC, Continued"
DECK_SUB   = "Horizontal Pods Autoscaling\nIRSA (IAM Roles for Service Accounts) — Optional"
ASSETS     = "week14/assets"
DECK_JSON  = "week14/week14_deck.json"


def embed_fig(s, fname, x, y, w, h):
    path = os.path.join(ASSETS, fname)
    iw, ih = Image.open(path).size
    ar = iw / ih
    if (w / h) > ar:
        dh = h; dw = h * ar
    else:
        dw = w; dh = w / ar
    dx = x + (w - dw) / 2.0; dy = y + (h - dh) / 2.0
    add_rect(s, Inches(dx - 0.04), Inches(dy - 0.04), Inches(dw + 0.08), Inches(dh + 0.08),
             WHITE, line=RULE_GRAY, line_width=0.75)
    s.shapes.add_picture(path, bw._i(Inches(dx)), bw._i(Inches(dy)),
                         bw._i(Inches(dw)), bw._i(Inches(dh)))


def _term_h(nlines, fs):
    return 0.5 + nlines * (fs * 1.52 / 72.0) + 0.22


def render_cover(s, n, total, role="Lecture"):
    add_text(s, Inches(0.7), Inches(2.35), Inches(8.5), Inches(1.6),
             DECK_TITLE, size=36, bold=True, color=BLUE, line_spacing=1.05)
    add_text(s, Inches(0.72), Inches(3.95), Inches(8.7), Inches(0.6),
             f"{WEEK_LABEL} · {role}", size=22, color=SLATE)
    add_text(s, Inches(0.72), Inches(4.62), Inches(8.9), Inches(0.9),
             DECK_SUB, size=15, italic=True, color=MUTED, line_spacing=1.2)
    logo_cx = Inches(10.7); logo_cy = Inches(3.55); ring_r = Inches(1.8)
    add_oval(s, logo_cx - ring_r, logo_cy - ring_r, ring_r * 2, ring_r * 2, WHITE,
             line=LIGHTBLUE, line_width=1.5)
    s.shapes.add_picture(K8S_LOGO, logo_cx - Inches(1.25), logo_cy - Inches(1.25),
                         width=Inches(2.5), height=Inches(2.5))
    s.shapes.add_picture(WHALE, Inches(0.45), Inches(6.85), width=Inches(0.5), height=Inches(0.5))
    add_text(s, Inches(9.5), Inches(7.12), Inches(3.35), Inches(0.3),
             f"CLO835, Fall 2026     {n} / {total}", size=10, color=FOOTER_GRAY, align=RIGHT)


_ACR = {"api":"API","sa":"SA","iam":"IAM","eks":"EKS","aks":"AKS","jwt":"JWT","sso":"SSO",
        "oidc":"OIDC","csr":"CSR","hpa":"HPA","arn":"ARN","sts":"STS","rbac":"RBAC","irsa":"IRSA",
        "aws":"AWS","tls":"TLS","https":"HTTPS","pv":"PV","pvc":"PVC","qps":"QPS","cpu":"CPU"}
def fix_acr(t):
    return re.sub(r"[A-Za-z0-9]+", lambda m: _ACR.get(m.group(0).lower(), m.group(0)), t)


_CMD = ("$", "#", "kubectl", "k ", "aws", "eksctl", "curl", "openssl", "cat ", "printenv",
        "export", "echo", "/kubectl", "/ $", "/$", "kubeconfig", "helm", "chmod", "cd ", "./")
def _cmd_like(t):
    st = t.strip()
    return any(st.startswith(c) for c in _CMD)

def _command_body_lines(body):
    lines = [b["text"] for b in body if b.get("text", "").strip()]
    if len(lines) >= 3 and sum(_cmd_like(l) for l in lines) >= 0.55 * len(lines):
        return [b["text"] for b in body]
    return None


def _eff_lines(g, w_in, fs):
    cpl = max(10, int(w_in * 72 / (fs * 0.60)))
    return sum(max(1, -(-len(l) // cpl)) for l in g)

def _term_stack(s, groups, y0=1.66, ymax=6.6):
    groups = [g for g in groups if any(l.strip() for l in g)]
    if not groups:
        return
    if len(groups) == 1:
        g, w = groups[0], 11.5; fs = 13
        while fs > 8 and _term_h(_eff_lines(g, w, fs), fs) > (ymax - y0): fs -= 1
        auto_term(s, 0.9, y0, w, min(ymax - y0, _term_h(_eff_lines(g, w, fs), fs)), "bash", g, font_size=fs)
    else:
        g0, g1, w = groups[0], groups[1], 5.95; fs = 12
        while fs > 7 and max(_term_h(_eff_lines(g0, w, fs), fs), _term_h(_eff_lines(g1, w, fs), fs)) > (ymax - y0):
            fs -= 1
        h0 = min(ymax - y0, _term_h(_eff_lines(g0, w, fs), fs))
        h1 = min(ymax - y0, _term_h(_eff_lines(g1, w, fs), fs))
        auto_term(s, 0.6, y0, w, h0, "bash", g0, font_size=fs)
        auto_term(s, 6.85, y0, w, h1, "bash", g1, font_size=fs)


def _items(body):
    return [(min(int(b.get("level", 0)), 2), b["text"]) for b in body]

def _codes(d):
    out = []
    for cb in d.get("code_blocks", []):
        lines = cb.get("lines", [])
        if any(l.strip() for l in lines):
            out.append((cb.get("lang", "bash"), lines))
    return out


def _norm_ws(t):
    # source titles/bodies carry nbsp (\xa0) and vertical-tab (\x0b) soft breaks — render as spaces
    return t.replace("\xa0", " ").replace("\x0b", " ").replace("\n", " ")


def render_slide(s, n, total, d):
    st = d["slide_type"]
    ttl = fix_acr(smart_title(_norm_ws(d["title"]))) if d.get("title") else ""

    if st == "cover":
        render_cover(s, n, total, d.get("cover_role", "Lecture"))
        return

    if st == "section_divider":
        raw = d["title"]
        kick, main = "SECTION", ttl
        for sep in ["–", ":", " - ", "-"]:
            if sep in raw:
                left, right = raw.split(sep, 1)
                kick = fix_acr(smart_title(left.strip())); main = fix_acr(smart_title(right.strip()))
                break
        sub = d["body"][0]["text"] if d.get("body") else None
        divider(s, kick if len(kick) <= 14 else "SECTION", main, subtitle=sub)
        whale_and_footer(s, n, total)
        return

    if st == "closing":
        closing(s, ttl if len(ttl) < 40 else "The End")
        whale_and_footer(s, n, total)
        return

    if st == "course_outline":
        title(s, "Course Outline")
        labels = [b["text"] for b in d.get("body", [])]
        hl = {i: BLUE for i in d.get("highlight", [])}
        course_outline(s, labels, hl)
        whale_and_footer(s, n, total)
        return

    # ---- generic content ----
    body_raw = d.get("body", [])
    codes = _codes(d)
    figfiles = [f["file"] for f in d.get("figures", []) if f.get("file")]
    cmd = _command_body_lines(body_raw)
    body = [] if cmd is not None else _items(body_raw)
    term_groups = ([cmd] if cmd is not None else []) + [lines for _, lines in codes]

    if ttl:
        title(s, ttl)

    if figfiles:
        if term_groups:
            # commands/code AND a figure: terminal(s) on top (content-fit), figure below.
            flat = []
            for i, g in enumerate(term_groups):
                if i:
                    flat.append("")
                flat.extend(g)
            fs = 12
            while fs > 8 and _term_h(_eff_lines(flat, 11.5, fs), fs) > 3.4: fs -= 1
            th = min(3.5, _term_h(_eff_lines(flat, 11.5, fs), fs))
            auto_term(s, 0.9, 1.5, 11.5, th, "bash", flat, font_size=fs)
            fy = 1.6 + th
            embed_fig(s, figfiles[0], 1.15, fy, 11.0, 6.55 - fy)
        elif body:
            # very-wide figures (aspect > 2.4) read better full-width BELOW the bullets;
            # otherwise bullets-left + figure-right.
            fp = os.path.join(ASSETS, figfiles[0])
            iw, ih = Image.open(fp).size
            if iw / ih > 2.4 and d.get("n") not in FIG_BOX:
                bullets(s, 1.6, body, x=0.6, w=12.1, size=14, line_spacing=1.2, space_after=5)
                by = min(1.7 + len(body) * 0.34 + 0.2, 3.5)
                embed_fig(s, figfiles[0], 0.7, by, 11.93, 6.55 - by)
            else:
                bsize = 14 if len(body) <= 5 else 12.5   # denser explanation -> smaller bullets
                bullets(s, 1.55, body, x=0.6, w=6.0, size=bsize,
                        line_spacing=1.18, space_after=5)
                box = FIG_BOX.get(d.get("n"), (6.85, 1.75, 5.95, 4.7))
                embed_fig(s, figfiles[0], *box)
        elif ttl:
            embed_fig(s, figfiles[0], 1.15, 1.55, 11.0, 5.05)
        else:
            # full-image slide (no title, no text — e.g. slide 17 IAM console screenshot)
            embed_fig(s, figfiles[0], 0.7, 0.7, 11.93, 6.1)
    elif term_groups and d.get("term_fs"):
        # explicit terminal font size (from a hand-authored slide); shrink only to avoid footer overflow
        g = term_groups[0]; y0 = 1.55; ymax = 6.95
        fs = d["term_fs"]
        while fs > 8 and _term_h(_eff_lines(g, 11.5, fs), fs) > (ymax - y0):
            fs -= 1
        h = min(ymax - y0, _term_h(_eff_lines(g, 11.5, fs), fs))
        auto_term(s, 0.9, y0, 11.5, h, "bash", g, font_size=fs)
    elif term_groups and body:
        bullets(s, 1.62, body, x=0.6, w=5.85, size=13.5, line_spacing=1.22, space_after=6)
        flat = []
        for i, g in enumerate(term_groups):
            if i:
                flat.append("")
            flat.extend(g)
        fs = 12
        while fs > 8 and _term_h(_eff_lines(flat, 5.95, fs), fs) > 5.0: fs -= 1
        h = min(5.0, _term_h(_eff_lines(flat, 5.95, fs), fs))
        auto_term(s, 6.85, 1.62, 5.95, h, "bash", flat, font_size=fs)
    elif term_groups:
        _term_stack(s, term_groups)
    elif body:
        sz = 16 if len(body) <= 6 else 14
        bullets(s, 1.72, body, x=0.6, w=12.1, size=sz)
    whale_and_footer(s, n, total)


def build_deck(slides, out):
    prs = bw.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]
    total = len(slides)
    for i, d in enumerate(slides, 1):
        s = prs.slides.add_slide(blank)
        render_slide(s, i, total, d)
        if d.get("hidden"):
            s._element.set("show", "0")
    _sanitize_coords(prs)
    prs.save(out)
    nh = sum(1 for d in slides if d.get("hidden"))
    print(f"wrote {out}  ({total} slides, {nh} hidden)")


# v2 split (partition of the 30 source slides; each in exactly ONE deck).
# LECTURE = concepts/theory + front/back matter; LAB = the workshops that apply them + cleanup.
# (Confirmed by the classification panel — see report.)
LECTURE_NS = [1, 2, 3, 11, 20, 21, 28, 29]   # 11 (kubeconfig CONCEPT) -> lecture per panel
LAB_NS     = [4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19,
              22, 23, 24, 25, 26, 27, 30]
_LAB_COVER = {"n": 0, "slide_type": "cover", "title": "", "body": [], "code_blocks": [],
              "figures": [], "cover_role": "Lab"}


def build():
    """v1: one combined deck, like the other weeks' v1."""
    with open(DECK_JSON) as fh:
        deck = json.load(fh)["slides"]
    build_deck(deck, "week14/Week14_lab_style_v1.pptx")


# v5/v6: house-terminal pages inserted AFTER the kubeconfig concept slide (source 11), showing the
# `kubectl config` commands taught for working with clusters/users/contexts/namespaces.
# v6 = the user's edit: split into THREE terminals, the first two showing REAL captured output from
# their k3d-kabana-dev cluster (command + output), the third the context-mutation commands. Output
# preserved verbatim (kept exactly as run: k3d-kabana-dev, DATA+OMITTED, table alignment).
_KC_TITLE = "Working with kubeconfig – kubectl config"
_KUBECONFIG_TERMINALS = [
    {"n": 111, "slide_type": "content", "title": _KC_TITLE, "body": [], "figures": [], "term_fs": 12,
     "code_blocks": [{"lang": "bash", "lines": [
        "# kubeconfig lives at ~/.kube/config by default — view the merged config",
        "$ kubectl config view",
        "apiVersion: v1",
        "clusters:",
        "- cluster:",
        "    certificate-authority-data: DATA+OMITTED",
        "    server: https://0.0.0.0:59478",
        "  name: k3d-kabana-dev",
        "contexts:",
        "- context:",
        "    cluster: k3d-kabana-dev",
        "    user: admin@k3d-kabana-dev",
        "  name: k3d-kabana-dev",
        "current-context: k3d-kabana-dev",
        "kind: Config",
        "users:",
        "- name: admin@k3d-kabana-dev",
        "  user:",
        "    client-certificate-data: DATA+OMITTED",
        "    client-key-data: DATA+OMITTED",
     ]}]},
    {"n": 112, "slide_type": "content", "title": _KC_TITLE, "body": [], "figures": [], "term_fs": 14,
     "code_blocks": [{"lang": "bash", "lines": [
        "# List every context — each bundles a CLUSTER + USER + NAMESPACE",
        "$ kubectl config get-contexts",
        "CURRENT   NAME             CLUSTER          AUTHINFO               NAMESPACE",
        "*         k3d-kabana-dev   k3d-kabana-dev   admin@k3d-kabana-dev",
     ]}]},
    {"n": 113, "slide_type": "content", "title": _KC_TITLE, "body": [], "figures": [], "term_fs": 14,
     "code_blocks": [{"lang": "bash", "lines": [
        "# Which context is kubectl using right now?",
        "$ kubectl config current-context",
        "",
        "# Switch context — changes cluster, user AND namespace together",
        "$ kubectl config use-context context-1",
        "",
        "# Pin a default namespace on the current context",
        "$ kubectl config set-context --current --namespace=dev",
        "",
        "# Define a context = one cluster + one user + a namespace",
        "$ kubectl config set-context context-1 --cluster=cluster-1 --user=user-1 --namespace=dev",
     ]}]},
]


def build_all():
    """v2: split into lecture + lab, matching the other weeks. (v5 inserts a kubeconfig terminal.)"""
    with open(DECK_JSON) as fh:
        by_n = {d["n"]: d for d in json.load(fh)["slides"]}
    assert set(LECTURE_NS).isdisjoint(LAB_NS), "a slide is in both decks"
    assert set(LECTURE_NS) | set(LAB_NS) == set(by_n), "partition misses/duplicates a slide"
    lecture = []
    for nn in LECTURE_NS:
        lecture.append(by_n[nn])
        if nn == 11:
            lecture.extend(_KUBECONFIG_TERMINALS)         # kubectl config terminals after concept
    lab = [_LAB_COVER] + [by_n[n] for n in LAB_NS]          # synthetic Lab cover
    build_deck(lecture, f"week14/Week14_lecture_style_{VERSION}.pptx")
    build_deck(lab, f"week14/Week14_lab_style_{VERSION}.pptx")


if __name__ == "__main__":
    build_all()
