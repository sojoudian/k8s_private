"""Week13 (source self-labels "Week 11") — Introduction to K8s RBAC + IRSA.

Redesign of week13/week13.pptx into the exact CLO835 Lab02 house design, v1 = one combined
deck like the other weeks' v1 (content untouched, verbatim per PROMPT.md R1). Reuses the proven,
guarded build_week12 engine (import is guarded → never rebuilds week12) for the palette, coord
guard, terminal/bullets/divider/closing/course-outline helpers, exactly as build_week12_v3_lab did.

Genuine diagrams (auth flow, RBAC who/what, IRSA, kubeconfig) are cropped from the source and
embedded as-is (the week12 FIG pattern); terminal/YAML/kubectl content is rebuilt as house
terminal mockups from the verbatim transcription. Hidden source slides stay hidden.

Content lives in week13_deck.json (built from the extraction). Run from a dir with whale.png,
Week04/<logo>, and week13/assets/ (the sandbox). Sandbox only — cwd-relative save.
"""

import os, json
from PIL import Image
import build_week12 as bw
from build_week12 import (
    Inches, Pt, BLUE, SLATE, WHITE, MUTED, BODY, CARD_BG, RULE_GRAY, LIGHTBLUE, FOOTER_GRAY,
    FONT_SANS, FONT_MONO, K8S_LOGO, WHALE,
    CENTER, LEFT, RIGHT, MIDDLE, TOP,
    title, bullets, auto_term, two_col_terminal, divider, closing, comparison_table,
    course_outline, whale_and_footer, add_text, add_rect, add_oval, add_line, smart_title,
    render_content, _flatten_code, _sanitize_coords,
)

VERSION    = "v6"

# Per-source-slide figure-box overrides (x, y, w, h) — used where the user hand-placed a figure.
# slide 8 (ServiceAccounts): user re-cropped fig8 and repositioned it in v3.
FIG_BOX = {8: (7.0, 2.92, 5.54, 2.34)}
WEEK_LABEL = "Week 11"                          # source self-labels this Week 11 (folder week13)
DECK_TITLE = "Introduction to K8s RBAC"
DECK_SUB   = "IRSA (IAM Roles for Service Accounts)"
ASSETS     = "week13/assets"
DECK_JSON  = "week13/week13_deck.json"


# ---- self-contained figure embed (aspect from the real file; no global FIG_ASPECT) ----
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


# ---- cover (house style; memes dropped, verbatim title kept) ----
def render_cover(s, n, total, role="Lecture"):
    add_text(s, Inches(0.7), Inches(2.35), Inches(8.9), Inches(1.5),
             DECK_TITLE, size=42, bold=True, color=BLUE, line_spacing=1.05)
    add_text(s, Inches(0.72), Inches(3.95), Inches(8.7), Inches(0.6),
             f"{WEEK_LABEL} · {role}", size=22, color=SLATE)
    add_text(s, Inches(0.72), Inches(4.62), Inches(8.7), Inches(0.5),
             DECK_SUB, size=15, italic=True, color=MUTED)
    logo_cx = Inches(10.7); logo_cy = Inches(3.55); ring_r = Inches(1.8)
    add_oval(s, logo_cx - ring_r, logo_cy - ring_r, ring_r * 2, ring_r * 2, WHITE,
             line=LIGHTBLUE, line_width=1.5)
    s.shapes.add_picture(K8S_LOGO, logo_cx - Inches(1.25), logo_cy - Inches(1.25),
                         width=Inches(2.5), height=Inches(2.5))
    s.shapes.add_picture(WHALE, Inches(0.45), Inches(6.85), width=Inches(0.5), height=Inches(0.5))
    add_text(s, Inches(9.5), Inches(7.12), Inches(3.35), Inches(0.3),
             f"CLO835, Fall 2026     {n} / {total}", size=10, color=FOOTER_GRAY, align=RIGHT)


import re
_ACR = {"api":"API","sa":"SA","iam":"IAM","eks":"EKS","aks":"AKS","jwt":"JWT",
        "sso":"SSO","oidc":"OIDC","csr":"CSR","hpa":"HPA","arn":"ARN","sts":"STS",
        "rbac":"RBAC","irsa":"IRSA","aws":"AWS","tls":"TLS","https":"HTTPS",
        "pv":"PV","pvc":"PVC"}
def fix_acr(t):
    return re.sub(r"[A-Za-z0-9]+", lambda m: _ACR.get(m.group(0).lower(), m.group(0)), t)


_CMD = ("$", "#", "kubectl", "k ", "aws", "eksctl", "curl", "openssl", "cat ",
        "printenv", "export", "echo", "/kubectl", "/ $", "/$", "kubeconfig")
def _cmd_like(t):
    st = t.strip()
    return any(st.startswith(c) for c in _CMD)

def _command_body_lines(body):
    """If the body is really a shell-command list, return it as flat lines (for a terminal);
    else return None (keep as prose bullets)."""
    lines = [b["text"] for b in body if b.get("text", "").strip()]
    if len(lines) >= 3 and sum(_cmd_like(l) for l in lines) >= 0.55 * len(lines):
        return [b["text"] for b in body]
    return None


def _eff_lines(g, w_in, fs):
    """Visual line count including wrapping of long lines at the terminal width."""
    cpl = max(10, int(w_in * 72 / (fs * 0.60)))     # Consolas ~0.6*fs pt per char
    return sum(max(1, -(-len(l) // cpl)) for l in g)

def _term_stack(s, groups, y0=1.66, ymax=6.6):
    """Render 1 or 2 terminals (wrap-aware content-fit). groups = list of line-lists."""
    groups = [g for g in groups if any(l.strip() for l in g)]
    if not groups:
        return
    if len(groups) == 1:
        g, w = groups[0], 11.5; fs = 13
        while fs > 8 and _term_h(_eff_lines(g, w, fs), fs) > (ymax - y0): fs -= 1
        auto_term(s, 0.9, y0, w, min(ymax - y0, _term_h(_eff_lines(g, w, fs), fs)),
                  "bash", g, font_size=fs)
    else:
        g0, g1, w = groups[0], groups[1], 5.95; fs = 12
        while fs > 7 and max(_term_h(_eff_lines(g0, w, fs), fs),
                             _term_h(_eff_lines(g1, w, fs), fs)) > (ymax - y0):
            fs -= 1
        # each terminal sized to its OWN content (top-aligned) — avoids empty black voids
        h0 = min(ymax - y0, _term_h(_eff_lines(g0, w, fs), fs))
        h1 = min(ymax - y0, _term_h(_eff_lines(g1, w, fs), fs))
        auto_term(s, 0.6, y0, w, h0, "bash", g0, font_size=fs)
        auto_term(s, 6.85, y0, w, h1, "bash", g1, font_size=fs)


def _items(body):
    return [(min(int(b.get("level", 0)), 2), b["text"]) for b in body]


def _codes(d):
    """Flatten this slide's code_blocks into (lang, lines) groups."""
    out = []
    for cb in d.get("code_blocks", []):
        lines = cb.get("lines", [])
        if any(l.strip() for l in lines):
            out.append((cb.get("lang", "bash"), lines))
    return out


def render_yaml_pair(s, n, total, d):
    """New page: two house terminals (Role + RoleBinding manifests) side by side, with the
    kubectl command below — the legible version of the two YAML boxes baked into slide 13's figure."""
    title(s, d.get("title", "Role and RoleBinding"))
    left, right, cmd = d["left"], d["right"], d.get("cmd", [])
    y0 = 1.55
    cmd_fs = 13
    cmd_h = _term_h(len(cmd), cmd_fs) if cmd else 0.0
    bottom = 6.55 - (cmd_h + 0.18 if cmd else 0.0)
    avail = bottom - y0
    nmax = max(len(left), len(right))
    fs = 13
    while fs > 9 and _term_h(nmax, fs) > avail:
        fs -= 1
    hL = min(avail, _term_h(len(left), fs))
    hR = min(avail, _term_h(len(right), fs))
    auto_term(s, 0.6, y0, 5.95, hL, d["left_title"], left, font_size=fs)
    auto_term(s, 6.85, y0, 5.95, hR, d["right_title"], right, font_size=fs)
    if cmd:
        cy = y0 + max(hL, hR) + 0.18
        auto_term(s, 0.6, cy, 12.2, cmd_h, "bash", cmd, font_size=cmd_fs)
    whale_and_footer(s, n, total)


def render_slide(s, n, total, d):
    st = d["slide_type"]
    ttl = fix_acr(smart_title(d["title"].replace("\n", " "))) if d.get("title") else ""

    if st == "cover":
        render_cover(s, n, total, d.get("cover_role", "Lecture"))
        return

    if st == "section_divider":
        # "Workshop 2 – Roles and rolebindings" -> kicker + main
        raw = d["title"]
        if "–" in raw or ":" in raw or "-" in raw:
            for sep in ["–", ":", " - "]:
                if sep in raw:
                    left, right = raw.split(sep, 1)
                    kick = fix_acr(smart_title(left.strip())); main = fix_acr(smart_title(right.strip()))
                    break
        else:
            kick = "SECTION"; main = ttl
        sub = d["body"][0]["text"] if d.get("body") else None
        divider(s, kick if len(kick) <= 14 else "SECTION", main, subtitle=sub)
        whale_and_footer(s, n, total)
        return

    if st == "closing":
        closing(s, ttl if len(ttl) < 40 else "Cleanup")
        whale_and_footer(s, n, total)
        return

    if st == "yaml_pair":
        render_yaml_pair(s, n, total, d)
        return

    if st == "course_outline":
        title(s, "Course Outline")
        labels = [b["text"] for b in d.get("body", [])]
        hl = {i: BLUE for i, lab in enumerate(labels) if b_is_highlighted(d, i)}
        course_outline(s, labels, hl)
        whale_and_footer(s, n, total)
        return

    # ---- generic content ----
    title(s, ttl)
    body_raw = d.get("body", [])
    codes = _codes(d)                                   # [(lang, lines), ...]
    figfiles = [f["file"] for f in d.get("figures", []) if f.get("file")]

    # command lists render as terminals, not bullets (house style)
    cmd = _command_body_lines(body_raw)
    body = [] if cmd is not None else _items(body_raw)
    term_groups = ([cmd] if cmd is not None else []) + [lines for _, lines in codes]

    if figfiles:
        # a genuine diagram is present; any YAML/code is already inside the diagram, so
        # only the separate command list (if any) still needs to be shown, above the figure.
        if cmd is not None:
            fs = 12
            while fs > 8 and _term_h(_eff_lines(cmd, 11.5, fs), fs) > 2.5: fs -= 1
            th = min(2.6, _term_h(_eff_lines(cmd, 11.5, fs), fs))
            auto_term(s, 0.9, 1.5, 11.5, th, "bash", cmd, font_size=fs)
            embed_fig(s, figfiles[0], 1.15, 1.6 + th, 11.0, 6.55 - (1.6 + th))
        elif body:
            bullets(s, 1.62, body, x=0.6, w=5.85, size=14, line_spacing=1.22, space_after=6)
            box = FIG_BOX.get(d.get("n"), (6.75, 1.62, 6.05, 4.95))
            embed_fig(s, figfiles[0], *box)
        else:
            embed_fig(s, figfiles[0], 1.15, 1.55, 11.0, 5.05)
    elif term_groups and body:
        # prose bullets left + a content-fit terminal right (no fixed-height void)
        bullets(s, 1.62, body, x=0.6, w=5.85, size=13.5, line_spacing=1.22, space_after=6)
        flat = []
        for i, g in enumerate(term_groups):
            if i:
                flat.append("")
            flat.extend(g)
        fs = 12
        while fs > 8 and _term_h(_eff_lines(flat, 5.95, fs), fs) > 5.0:
            fs -= 1
        h = min(5.0, _term_h(_eff_lines(flat, 5.95, fs), fs))
        auto_term(s, 6.85, 1.62, 5.95, h, "bash", flat, font_size=fs)
    elif term_groups:
        _term_stack(s, term_groups)
    elif body:
        sz = 16 if len(body) <= 6 else 14
        bullets(s, 1.72, body, x=0.6, w=12.1, size=sz)
    whale_and_footer(s, n, total)


def b_is_highlighted(d, i):
    return i in d.get("highlight", [])


# v2 split (partition of the 46 source slides; each in exactly ONE deck).
# LECTURE = concepts/theory + front/back matter; LAB = the workshops that apply them + cleanup.
LECTURE_NS = [1, 2, 3, 4, 5, 6, 7, 8, 15, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 43, 45]
LAB_NS     = [9, 10, 11, 12, 13, 14, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
              36, 37, 38, 39, 40, 41, 42, 44, 46]   # 44 (kubeconfig hands-on) -> lab per panel
_LAB_COVER = {"n": 0, "slide_type": "cover", "title": "", "body": [], "code_blocks": [],
              "figures": [], "cover_role": "Lab"}


def _yaml_pair_slide(s19):
    """Build the v5 'Role and RoleBinding' page from slide 19's stored YAML/command blocks."""
    role = binding = cmd = None
    for cb in s19.get("code_blocks", []):
        lines = cb.get("lines", [])
        txt = "\n".join(lines)
        if "kind: RoleBinding" in txt:
            binding = lines
        elif "kind: Role" in txt:
            role = lines
        elif any(l.strip().startswith(("kubectl", "$")) for l in lines):
            cmd = lines
    return {
        "n": 191, "slide_type": "yaml_pair", "title": "Role and RoleBinding",
        "left_title": "developer-role.yaml", "left": role or [],
        "right_title": "devuser-developer-binding.yaml", "right": binding or [],
        "cmd": ["$ " + cmd[0]] if cmd else [],
    }


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
            s._element.set("show", "0")     # preserve source hidden state
    _sanitize_coords(prs)
    prs.save(out)
    nh = sum(1 for d in slides if d.get("hidden"))
    print(f"wrote {out}  ({total} slides, {nh} hidden)")


def build():
    """v1: one combined deck (kept for reference)."""
    with open(DECK_JSON) as fh:
        deck = json.load(fh)["slides"]
    build_deck(deck, "week13/Week13_lab_style_v1.pptx")


def build_all():
    """v2: split into lecture + lab, matching the other weeks."""
    with open(DECK_JSON) as fh:
        by_n = {d["n"]: d for d in json.load(fh)["slides"]}
    assert set(LECTURE_NS).isdisjoint(LAB_NS), "a slide is in both decks"
    assert set(LECTURE_NS) | set(LAB_NS) == set(by_n), "partition misses/duplicates a slide"
    lecture = []
    for nn in LECTURE_NS:
        lecture.append(by_n[nn])
        if nn == 19:
            lecture.append(_yaml_pair_slide(by_n[19]))     # v5: legible Role/RoleBinding page
    lab = [_LAB_COVER] + [by_n[n] for n in LAB_NS]          # synthetic Lab cover
    build_deck(lecture, f"week13/Week13_lecture_style_{VERSION}.pptx")
    build_deck(lab, f"week13/Week13_lab_style_{VERSION}.pptx")


if __name__ == "__main__":
    import sys
    # SHOULD-FIX 7 of review round 3 (2026-11-11): this old builder overwrote Week13_lecture_style_v6 and
    # Week13_lab_style_v6 with no check. Importing this file still works.
    sys.exit("build_week13.py is an old version. Use build_week13_lecture_v9.py and build_week13_lab_v5.py.")
    build_all()
