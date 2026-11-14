"""Week12 LAB v3 — a single, deliberately *simple* workshop.

The v2 lab deck carries TWO workshops: WS1 (env vars + ConfigMaps, incl. ConfigMap
volumes / nginx files) and WS2 (Secrets with openssl-generated TLS certs + HTTPS).
Neither is "super easy": WS1 sprawls across five techniques (manifest env, configMap
env, args, create-from-file, volume-as-files) and WS2 needs openssl/TLS/HTTPS.

v3 keeps ONE new workshop that teaches the whole subject — ConfigMaps *and* Secrets —
via the single simplest mechanism: inject a literal value into a Pod as an environment
variable. No volumes, no nginx, no openssl, no TLS. Create -> inject -> verify, twice
(ConfigMap then Secret), then a one-slide comparison.

Reuses the exact CLO835 house design by importing build_week12 (import is guarded, so
it never rebuilds). Run from a dir with Week04/<logo>, whale.png, Week12/assets/.
"""

import build_week12 as bw
from build_week12 import (
    Inches, Pt, BLUE, SLATE, WHITE, MUTED, BODY, CARD_BG, RULE_GRAY, LIGHTBLUE,
    FONT_SANS, FONT_MONO, MIDDLE, TOP, LEFT, CENTER,
    title, bullets, auto_term, divider, closing, render_cover, whale_and_footer,
    add_text, add_rect, add_rounded_rect, add_line, _sanitize_coords,
)

VERSION = "v3"


def term_h(nlines, fs):
    """Content-fit terminal height (chrome + one line per row) — no black void."""
    return 0.5 + nlines * (fs * 1.52 / 72.0) + 0.22


def two_terms(s, n, total, ttl, intro, lt, lcode, rt, rcode, *, y=1.95):
    """title + one intro line + two content-fit terminals side by side (house layout)."""
    title(s, ttl)
    if intro:
        bullets(s, 1.42, [(0, intro)], x=0.6, w=12.2, size=16,
                line_spacing=1.15, space_after=0)
    avail = 6.72 - y
    nmax = max(len(lcode), len(rcode))
    fs = 13
    while fs > 9 and term_h(nmax, fs) > avail:
        fs -= 1
    h = term_h(nmax, fs)
    auto_term(s, 0.60, y, 5.95, h, lt, lcode, font_size=fs)
    auto_term(s, 6.85, y, 5.95, h, rt, rcode, font_size=fs)
    whale_and_footer(s, n, total)


# ------------------------------------------------------------------ slides

def s_cover(s, n, total):
    render_cover(s, n, total, "Lab")


def s_divider(s, n, total):
    divider(s, "WORKSHOP",
            "Inject Configuration into a Pod",
            subtitle="ConfigMaps & Secrets as environment variables — the simple way")
    whale_and_footer(s, n, total)


def s_goals(s, n, total):
    title(s, "Goals")
    bullets(s, 1.75, [
        (0, "Create a ConfigMap and a Secret from literal values"),
        (0, "Inject their values into a Pod as environment variables"),
        (0, "See how a Secret differs from a ConfigMap — and when to use each"),
    ], x=0.6, w=12.1, size=18, level_step=0, line_spacing=1.35, space_after=14)
    bw.add_rounded_rect(s, Inches(0.6), Inches(4.45), Inches(8.4), Inches(0.95),
                        CARD_BG, line=RULE_GRAY, line_width=0.75, radius_ratio=0.08)
    add_rect(s, Inches(0.6), Inches(4.50), Inches(0.12), Inches(0.85), BLUE)
    add_text(s, Inches(0.95), Inches(4.55), Inches(7.9), Inches(0.8),
             "Prereqs: a running cluster and kubectl. Everything lives in one "
             "namespace (week10) so cleanup is a single command.",
             size=13, color=BODY, anchor=MIDDLE, line_spacing=1.15)
    whale_and_footer(s, n, total)


def s_create_cm(s, n, total):
    left = [
        "# Create the workshop namespace",
        "$ kubectl create namespace week10",
        "",
        "# Create a ConfigMap from literals",
        "$ kubectl create configmap \\",
        "    fortune-config \\",
        "    --from-literal=sleep-interval=25 \\",
        "    --from-literal=sky-color=blue \\",
        "    -n week10",
        "",
        "# Inspect what was stored",
        "$ kubectl get cm fortune-config \\",
        "    -n week10 -o yaml",
    ]
    right = [
        "apiVersion: v1",
        "kind: ConfigMap",
        "metadata:",
        "  name: fortune-config",
        "  namespace: week10",
        "data:",
        '  sleep-interval: "25"',
        "  sky-color: blue",
    ]
    two_terms(s, n, total, "Step 1 · Create a ConfigMap",
              "A ConfigMap stores non-sensitive configuration as plain-text key/value pairs.",
              "bash", left, "fortune-config  -o yaml", right)


def s_inject_cm(s, n, total):
    left = [
        "# fortune-env-cm.yaml",
        "apiVersion: v1",
        "kind: Pod",
        "metadata:",
        "  name: fortune-env-cm",
        "spec:",
        "  containers:",
        "  - image: luksa/fortune:env",
        "    name: html-generator",
        "    env:",
        "    - name: INTERVAL",
        "      valueFrom:",
        "        configMapKeyRef:",
        "          name: fortune-config",
        "          key: sleep-interval",
    ]
    right = [
        "# Deploy the Pod",
        "$ kubectl apply \\",
        "    -f fortune-env-cm.yaml -n week10",
        "",
        "# The ConfigMap value is now an",
        "# environment variable in the container",
        "$ kubectl exec fortune-env-cm \\",
        "    -n week10 -- printenv INTERVAL",
        "25",
    ]
    two_terms(s, n, total, "Step 2 · Inject the ConfigMap as an Env Var",
              "Reference a key with configMapKeyRef — its value becomes a container environment variable.",
              "fortune-env-cm.yaml", left, "bash", right)


def s_create_secret(s, n, total):
    left = [
        "# Create a Secret from a literal",
        "$ kubectl create secret generic \\",
        "    fortune-secret \\",
        "    --from-literal=api-key=s3cr3t-value \\",
        "    -n week10",
        "",
        "# The value is base64-encoded, not",
        "# plain text like a ConfigMap",
        "$ kubectl get secret fortune-secret \\",
        "    -n week10 -o yaml",
    ]
    right = [
        "apiVersion: v1",
        "kind: Secret",
        "metadata:",
        "  name: fortune-secret",
        "  namespace: week10",
        "type: Opaque",
        "data:",
        "  api-key: czNjcjN0LXZhbHVl",
        "",
        "# echo czNjcjN0LXZhbHVl | base64 -d",
        "#   -> s3cr3t-value",
    ]
    two_terms(s, n, total, "Step 3 · Create a Secret",
              "A Secret works just like a ConfigMap, but is meant for sensitive data and stored base64-encoded.",
              "bash", left, "fortune-secret  -o yaml", right)


def s_inject_secret(s, n, total):
    left = [
        "# fortune-secret-env.yaml",
        "apiVersion: v1",
        "kind: Pod",
        "metadata:",
        "  name: fortune-secret-env",
        "spec:",
        "  containers:",
        "  - image: luksa/fortune:env",
        "    name: html-generator",
        "    env:",
        "    - name: API_KEY",
        "      valueFrom:",
        "        secretKeyRef:",
        "          name: fortune-secret",
        "          key: api-key",
    ]
    right = [
        "# Deploy the Pod",
        "$ kubectl apply \\",
        "    -f fortune-secret-env.yaml -n week10",
        "",
        "# Kubernetes decodes the Secret and",
        "# exposes it as a plain env var",
        "$ kubectl exec fortune-secret-env \\",
        "    -n week10 -- printenv API_KEY",
        "s3cr3t-value",
    ]
    two_terms(s, n, total, "Step 4 · Inject the Secret as an Env Var",
              "Injecting a Secret is identical to a ConfigMap — just use secretKeyRef instead of configMapKeyRef.",
              "fortune-secret-env.yaml", left, "bash", right)


def _compare_card(s, x, w, header, hcolor, rows):
    y = 1.95
    ch = 0.62
    add_rounded_rect(s, Inches(x), Inches(y), Inches(w), Inches(3.55),
                     WHITE, line=RULE_GRAY, line_width=1.0, radius_ratio=0.05)
    add_rect(s, Inches(x), Inches(y), Inches(w), Inches(ch), hcolor)
    add_text(s, Inches(x), Inches(y), Inches(w), Inches(ch), header,
             size=17, bold=True, color=WHITE, align=CENTER, anchor=MIDDLE)
    ry = y + ch + 0.20
    for lead, rest in rows:
        # bold label on its own line, optional detail line beneath — stacked, never overlaid
        add_text(s, Inches(x + 0.30), Inches(ry), Inches(w - 0.55), Inches(0.30),
                 lead, size=13.5, bold=True, color=SLATE)
        if rest:
            add_text(s, Inches(x + 0.30), Inches(ry + 0.28), Inches(w - 0.55), Inches(0.30),
                     rest, size=12.5, color=BODY)
        ry += 0.70


def s_compare(s, n, total):
    title(s, "ConfigMaps vs Secrets")
    _compare_card(s, 0.60, 5.95, "ConfigMap", BLUE, [
        ("For non-sensitive config", "intervals, URLs, feature flags"),
        ("Stored as plain text", "kubectl get cm shows real values"),
        ("Persisted in etcd", "readable by anyone with API access"),
        ("Consumed with", "valueFrom.configMapKeyRef"),
    ])
    _compare_card(s, 6.85, 5.95, "Secret", SLATE, [
        ("For sensitive data", "keys, passwords, TLS certificates"),
        ("Stored base64, type: Opaque", "encoding, not encryption"),
        ("Also persisted in etcd", "encryption-at-rest is opt-in"),
        ("Consumed with", "valueFrom.secretKeyRef"),
    ])
    bw.add_rounded_rect(s, Inches(0.60), Inches(5.85), Inches(12.20), Inches(0.72),
                        CARD_BG, line=RULE_GRAY, line_width=0.75, radius_ratio=0.10)
    add_rect(s, Inches(0.60), Inches(5.90), Inches(0.12), Inches(0.62), BLUE)
    add_text(s, Inches(0.95), Inches(5.85), Inches(11.7), Inches(0.72),
             "Same consumption API — a Pod reads either one the same way; swap "
             "configMapKeyRef for secretKeyRef.",
             size=13.5, color=BODY, anchor=MIDDLE, line_spacing=1.1)
    whale_and_footer(s, n, total)


def s_end(s, n, total):
    closing(s, "Workshop: the End")
    whale_and_footer(s, n, total)


def s_cleanup(s, n, total):
    title(s, "Cleanup")
    code = [
        "# Delete the workshop namespace — this removes the",
        "# Pods, the ConfigMap and the Secret in one shot",
        "$ kubectl delete namespace week10",
    ]
    fs = 15
    auto_term(s, 0.9, 1.85, 11.5, term_h(len(code), fs), "bash", code, font_size=fs)
    whale_and_footer(s, n, total)


SLIDES = [s_cover, s_divider, s_goals, s_create_cm, s_inject_cm,
          s_create_secret, s_inject_secret, s_compare, s_end, s_cleanup]


def build():
    prs = bw.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]
    total = len(SLIDES)
    for i, fn in enumerate(SLIDES, 1):
        s = prs.slides.add_slide(blank)
        fn(s, i, total)
    _sanitize_coords(prs)
    out = f"Week12/Week12_lab_style_{VERSION}.pptx"
    prs.save(out)
    print(f"wrote {out}  ({total} slides)")


if __name__ == "__main__":
    build()
