# -*- coding: utf-8 -*-
"""CLO835 Week 13 lecture v8 - Authentication, RBAC and Amazon EKS.

Fixes every defect of the check against PROMPT.md, DESIGN_LANGUAGE.md and PREFERENCES.md
(report 2026-10-31-15). v7 said "Week 11" on the cover, had the old course outline, promised
topics that it did not teach, showed outside screenshots, and had commands that fail as shown.
Each diagram is now a native house diagram. The lecture teaches ClusterRoles and the default
roles, and the facts on Amazon EKS follow the AWS documents of 2026.

Input : Week12/Lecture_week12_v6.pptx, for the cover and the outline (read, never written)
Output: week13/Lecture_week13_v8.pptx

Run from the project root. It is guarded, so importing it writes nothing.
    python build_week13_lecture_v8.py
"""
import re

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

import build_week08 as E
from build_week09_lecture_v6 import arrow, box, label, zone
from build_week12_lecture_v6 import finish

SRC = "Week12/Lecture_week12_v6.pptx"
OUT = "week13/Lecture_week13_v8.pptx"
SLATE, STEPS, GREEN, RED = E.SLATE, E.STEPS, E.GOAL_GREEN, E.ALERT_RED
UP, DOWN = MSO_SHAPE.UP_ARROW, MSO_SHAPE.DOWN_ARROW
LEFT, RIGHT = MSO_SHAPE.LEFT_ARROW, MSO_SHAPE.RIGHT_ARROW
BOTH, UP_DOWN = MSO_SHAPE.LEFT_RIGHT_ARROW, MSO_SHAPE.UP_DOWN_ARROW
LEVEL = {0: (228600, E.BLUE, "▪  "), 1: (612647, STEPS[1], "–  "), 2: (996695, E.MUTED, "•  ")}
YAML_KEYS = ("apiVersion", "kind", "metadata", "rules", "subjects", "roleRef", "data")
BOTTOM = 6.70

ROLE = """apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: developer
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["list", "get", "create", "update"]
- apiGroups: [""]
  resources: ["configmaps"]
  verbs: ["create"]
---""".split("\n")

BINDING = """apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: devuser-developer-binding
subjects:
- kind: User
  name: dev-user
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: developer
  apiGroup: rbac.authorization.k8s.io""".split("\n")

CURL_API = ["# Every client can read the version.",
            "$ curl -k https://localhost:6443/version",
            "",
            "# RBAC denies most other paths. The user system:anonymous gets 403 Forbidden.",
            "$ curl -k https://localhost:6443/apis",
            "",
            "# kubectl proxy sends your credentials to the API server.",
            "$ kubectl proxy --port=8001 &",
            "$ sleep 2; curl -s http://localhost:8001/apis | head -8",
            "$ kill %1"]

PV_READER = ["# A ClusterRole that reads PersistentVolumes, and a ServiceAccount.",
             "$ kubectl create clusterrole pv-reader --verb=get,list --resource=persistentvolumes",
             "$ kubectl create serviceaccount clo835",
             "",
             "# Test 1: a RoleBinding.",
             "$ kubectl create rolebinding pv-test --clusterrole=pv-reader --serviceaccount=default:clo835",
             "$ kubectl auth can-i list persistentvolumes -A --as=system:serviceaccount:default:clo835",
             "no",
             "",
             "# Test 2: a ClusterRoleBinding.",
             "$ kubectl delete rolebinding pv-test",
             "$ kubectl create clusterrolebinding pv-test --clusterrole=pv-reader --serviceaccount=default:clo835",
             "$ kubectl auth can-i list persistentvolumes -A --as=system:serviceaccount:default:clo835",
             "yes",
             "",
             "# Delete these objects. The lab uses the same names.",
             "$ kubectl delete clusterrolebinding pv-test",
             "$ kubectl delete clusterrole pv-reader",
             "$ kubectl delete serviceaccount clo835"]

DEFAULTS = ["# The paths that an authenticated user can read.",
            "$ kubectl get clusterrole system:discovery -o yaml",
            "",
            "# The subject of the binding is the group system:authenticated.",
            "$ kubectl get clusterrolebinding system:discovery -o yaml",
            "",
            "# The subject of this binding is the group system:masters.",
            "$ kubectl get clusterrolebinding cluster-admin -o yaml",
            "",
            "# The group of the user kubernetes-admin is kubeadm:cluster-admins.",
            "$ kubectl get clusterrolebinding kubeadm:cluster-admins -o yaml"]

CLUSTER_ADMIN = ["$ kubectl describe clusterrole cluster-admin",
                 "Name:         cluster-admin",
                 "Labels:       kubernetes.io/bootstrapping=rbac-defaults",
                 "Annotations:  rbac.authorization.kubernetes.io/autoupdate: true",
                 "PolicyRule:",
                 "  Resources  Non-Resource URLs  Resource Names  Verbs",
                 "  ---------  -----------------  --------------  -----",
                 "  *.*        []                 []              [*]",
                 "             [*]                []              [*]"]

AWS_AUTH = """apiVersion: v1
kind: ConfigMap
metadata:
  name: aws-auth
  namespace: kube-system
data:
  mapRoles: |
    - rolearn: arn:aws:iam::111122223333:role/worker-node-instance-role
      username: system:node:{{EC2PrivateDNSName}}
      groups:
        - system:bootstrappers
        - system:nodes""".split("\n")

REFERENCES = ["https://kubernetes.io/docs/reference/access-authn-authz/authentication/",
              "https://kubernetes.io/docs/reference/access-authn-authz/rbac/",
              "https://www.cncf.io/blog/2020/07/31/kubernetes-rbac-101-authentication/",
              "https://docs.aws.amazon.com/eks/latest/userguide/cluster-auth.html",
              "https://docs.aws.amazon.com/eks/latest/userguide/grant-k8s-access.html",
              "https://docs.aws.amazon.com/eks/latest/userguide/access-entries.html",
              "https://docs.aws.amazon.com/eks/latest/userguide/auth-configmap.html",
              "https://dev.to/aws-builders/eks-auth-deep-dive-4fib"]


def keep_first(prs, count):
    """Keep the cover, the agenda and the outline. Saving drops the other slide parts."""
    ids = prs.slides._sldIdLst
    for sid in list(ids)[count:]:
        prs.part.drop_rel(sid.rId)
        ids.remove(sid)


def set_only_run(shape, text):
    para = shape.text_frame.paragraphs[0]
    para.runs[0].text = text
    for extra in para.runs[1:]:
        extra._r.getparent().remove(extra._r)


def current_week(outline):
    """The blue tile of the current week moves from Week 12 to Week 13."""
    labels = {"Week 12: K8s – ConfigMaps & Secrets": None, "Week 13: K8s – RBAC and EKS": None}
    for sh in outline.shapes:
        if sh.has_text_frame and sh.text_frame.text in labels:
            labels[sh.text_frame.text] = sh
    blue, normal = labels["Week 12: K8s – ConfigMaps & Secrets"], labels["Week 13: K8s – RBAC and EKS"]
    frames = [[sh for sh in outline.shapes if sh.shape_type == 1 and sh.top == tb.top
               and abs(sh.left - (tb.left - Inches(0.16))) < Inches(0.02)][0] for tb in (blue, normal)]
    for one, two in (frames, (blue, normal)):
        one.left, two.left = two.left, one.left
        one.top, two.top = two.top, one.top
    set_only_run(blue, "Week 13: K8s – RBAC and EKS")
    set_only_run(normal, "Week 12: K8s – ConfigMaps & Secrets")


def new_slide(prs, title):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    E.add_text(s, Inches(0.55), Inches(0.40), Inches(12.2), Inches(0.85), title, size=30, bold=True,
               color=E.BLUE, line_spacing=1.05)
    E.add_line(s, Inches(0.57), Inches(1.38), Inches(5.2), Inches(1.38), color=E.BLUE, width=2)
    return s


def bullets(s, x, y, w, items, size=14, after=4, h=None):
    """Each item is (level, text). Text between backticks is inline code: mono, bold and Slate."""
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h or BOTTOM - y))
    frame = tb.text_frame
    frame.margin_left = frame.margin_right = frame.margin_top = frame.margin_bottom = 0
    frame.word_wrap = True
    for i, (lvl, text) in enumerate(items):
        margin, color, glyph = LEVEL[lvl]
        p = frame.paragraphs[0] if i == 0 else frame.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.line_spacing = 1.15
        p.space_after = Pt(after)
        ppr = p._p.get_or_add_pPr()
        ppr.set("marL", str(margin))
        ppr.set("indent", "-228600")
        points = max(size - lvl, 12)
        run = p.add_run()
        run.text = glyph
        run.font.name, run.font.size, run.font.bold = E.FONT_SANS, Pt(points), True
        run.font.color.rgb = color
        for k, part in enumerate(re.split("`", text)):
            if not part:
                continue
            run = p.add_run()
            run.text = part
            run.font.size = Pt(points)
            run.font.name = E.FONT_MONO if k % 2 else E.FONT_SANS
            run.font.bold = bool(k % 2)
            run.font.color.rgb = SLATE if k % 2 else E.BODY
    return tb


def line_color(line, going, yaml):
    text = line.strip()
    if text.startswith("#"):
        return E.TERM_GRN
    if text.startswith("$") or going:
        return E.TERM_CYAN
    if yaml and line.split(":")[0] in YAML_KEYS:
        return E.TERM_CYAN
    return E.TERM_GRAY


def term(s, x, y, w, bar, lines, size=11, yaml=False, h=None):
    """A house terminal that fits its lines."""
    rows, going = [], False
    for line in lines:
        rows.append([(line, line_color(line, going, yaml))] if line else [])
        going = (line.strip().startswith("$") or going) and line.rstrip().endswith("\\")
    height = h or 0.32 + 0.10 + len(lines) * size * 1.17 * 1.15 / 72 + 0.16
    E.terminal(s, Inches(x), Inches(y), Inches(w), Inches(height), bar, rows, font_size=size)
    return y + height


def tile(s, x, y, w, h, text, fill, size=11):
    """A box with code in it."""
    E.add_rounded_rect(s, Inches(x), Inches(y), Inches(w), Inches(h), fill, radius_ratio=0.10)
    E.add_text(s, Inches(x + 0.04), Inches(y), Inches(w - 0.08), Inches(h), text, font=E.FONT_MONO, size=size, bold=True,
               color=E.WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.0)


def note(s, x, y, w, h, text, color=SLATE, align=PP_ALIGN.CENTER, bold=False):
    E.add_text(s, Inches(x), Inches(y), Inches(w), Inches(h), text, size=12, bold=bold, color=color, align=align,
               anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.0)


def flow(s, x, y, w, text, fill=E.BLUE, kind=RIGHT, h=0.56):
    """An arrow shape with its label inside."""
    arrow(s, kind, x, y, w, h, fill=fill)
    inset = 0.22 if kind == LEFT else 0.06
    E.add_text(s, Inches(x + inset), Inches(y), Inches(w - 0.28), Inches(h), text, size=12, bold=True, color=E.WHITE,
               align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.0)


def slide4(prs):
    s = new_slide(prs, "Authentication and Authorization Process in Kubernetes")
    bullets(s, 0.60, 1.55, 5.55, [
        (0, "The Kubernetes API server uses one or more authentication methods"),
        (1, "X.509 client certificates"), (1, "Static token file"), (1, "Bootstrap tokens"),
        (1, "ServiceAccount tokens"), (1, "OpenID Connect tokens"), (1, "Webhook token authentication"),
        (1, "Authenticating proxy"),
        (0, "An authentication method gets the user name, the user ID and the groups of the client from the request"),
        (0, "The API server then starts the authorization phase"),
        (0, "Admission control can change or deny the request")])
    box(s, 6.40, 2.25, 1.10, 0.80, "User", STEPS[5])
    arrow(s, RIGHT, 7.56, 2.48, 0.36, 0.34)
    zone(s, 7.98, 1.65, 3.05, 4.15, "API server", color=STEPS[1], fill=E.CARD_BG)
    for y, text, fill in ((2.25, "Authentication", STEPS[0]), (3.45, "Authorization", STEPS[3]),
                          (4.65, "Admission control", STEPS[4])):
        box(s, 8.15, y, 2.70, 0.80, text, fill, size=14)
    arrow(s, DOWN, 9.33, 3.08, 0.34, 0.34)
    arrow(s, DOWN, 9.33, 4.28, 0.34, 0.34)
    arrow(s, RIGHT, 11.09, 4.88, 0.36, 0.34)
    box(s, 11.51, 4.65, 1.24, 0.80, "etcd", STEPS[5])
    return s


def slide5(prs):
    s = new_slide(prs, "Kubernetes API Client Types")
    bullets(s, 0.60, 1.55, 12.10, [(0, "The Kubernetes API has two types of clients")], h=0.40)
    bullets(s, 0.60, 2.05, 6.00, [
        (0, "Users: human clients"),
        (1, "Administrators who deploy Kubernetes add-ons and extensions"),
        (1, "Developers who deploy applications"),
        (1, "Kubernetes does not manage users. An external system manages them, for example:"),
        (2, "Single sign-on (SSO)"), (2, "AWS IAM"), (2, "Google accounts")], after=5)
    bullets(s, 6.85, 2.05, 5.85, [
        (0, "Processes"),
        (1, "Applications that call the Kubernetes API"),
        (1, "Observability tools that collect metrics from the Kubernetes API"),
        (1, "Security tools that query the Kubernetes API"),
        (1, "Kubernetes manages ServiceAccounts for processes")], after=5)
    return s


def method(s, y, name):
    zone(s, 5.05, y, 7.70, 1.16, name, color=STEPS[1], fill=E.CARD_BG)


def slide6(prs):
    s = new_slide(prs, "Authentication Methods")
    bullets(s, 0.60, 1.55, 4.20, [
        (0, "Kubernetes authenticates a client with one of these methods:"),
        (1, "A client certificate"), (1, "A bearer token (OpenID Connect or ServiceAccount)"),
        (1, "An authenticating proxy")])
    method(s, 1.52, "OpenID Connect token")
    box(s, 5.20, 1.92, 1.50, 0.62, "OIDC provider", STEPS[3], size=12)
    flow(s, 6.76, 1.95, 1.40, "1. Token")
    box(s, 8.22, 1.92, 0.90, 0.62, "Client", STEPS[5], size=12)
    flow(s, 9.18, 1.95, 2.12, "2. Request and token")
    box(s, 11.36, 1.92, 1.25, 0.62, "API server", STEPS[5], size=12)
    method(s, 2.76, "ServiceAccount token")
    box(s, 5.20, 3.16, 0.90, 0.62, "Pod", STEPS[3], size=12)
    flow(s, 6.16, 3.19, 5.14, "Request with the token in the Authorization header")
    box(s, 11.36, 3.16, 1.25, 0.62, "API server", STEPS[5], size=12)
    method(s, 4.00, "Authenticating proxy")
    box(s, 5.20, 4.40, 0.90, 0.62, "Client", STEPS[5], size=12)
    flow(s, 6.16, 4.43, 1.30, "1. Request")
    box(s, 7.52, 4.40, 0.90, 0.62, "Proxy", STEPS[3], size=12)
    flow(s, 8.48, 4.43, 2.82, "2. X-Remote-User header")
    box(s, 11.36, 4.40, 1.25, 0.62, "API server", STEPS[5], size=12)
    method(s, 5.24, "X.509 client certificate")
    box(s, 5.20, 5.64, 0.90, 0.62, "Client", STEPS[5], size=12)
    flow(s, 6.16, 5.67, 5.14, "TLS handshake with the certificate that the cluster CA signed")
    box(s, 11.36, 5.64, 1.25, 0.62, "API server", STEPS[5], size=12)
    return s


def certificate_slide(prs):
    s = new_slide(prs, "A Client Certificate Is a User")
    bullets(s, 0.60, 1.65, 5.40, [
        (0, "The common name (CN) of the certificate is the user name"),
        (0, "The organization (O) field of the certificate is a group"),
        (0, "`kubectl config set-credentials` adds the certificate to the kubeconfig file"),
        (0, "`kubectl config set-context` links this user to a cluster and a namespace")], size=15, after=10)
    rows = (("openssl req", "Create a key and a certificate signing request (CSR)", STEPS[0]),
            ("CertificateSigningRequest", "Send the CSR to the API server", STEPS[1]),
            ("$ kubectl certificate approve", "An administrator approves the CSR", STEPS[3]),
            (".status.certificate", "The cluster CA signs the certificate", STEPS[4]))
    for k, (code, text, fill) in enumerate(rows):
        y = 1.65 + k * 1.22
        tile(s, 6.25, y, 3.35, 0.86, code, fill, size=12)
        note(s, 9.72, y, 3.03, 0.86, text, align=PP_ALIGN.LEFT)
        if k < 3:
            arrow(s, DOWN, 7.76, y + 0.90, 0.32, 0.28, fill=SLATE)
    return s


def slide7(prs):
    s = new_slide(prs, "Groups in Kubernetes")
    bullets(s, 0.60, 1.55, 12.10, [
        (0, "Kubernetes supports groups, so that you do not bind a role to each user"),
        (0, "Kubernetes has two types of groups:"),
        (0, "System-assigned groups: the API server assigns these groups, and their names start with `system:`"),
        (1, "`system:authenticated`"), (1, "`system:serviceaccounts:<namespace>`"), (1, "`system:unauthenticated`"),
        (0, "User-asserted groups: an external system asserts these groups in the certificate, in the token or through "
            "the authentication webhook"),
        (1, "Groups do not exist as objects in the API server"),
        (0, "A certificate or a token can name any group")], after=6)
    return s


def slide8(prs):
    s = new_slide(prs, "ServiceAccounts")
    bullets(s, 0.60, 1.55, 5.45, [
        (0, "Each namespace has a default ServiceAccount"),
        (0, "A ServiceAccount is a Kubernetes object"),
        (0, "Many Pods can use the same ServiceAccount"),
        (0, "A Pod can use only one ServiceAccount, from its own namespace"),
        (0, "The token of the ServiceAccount authenticates the Pod and gives the user name of the Pod"),
        (0, "The administrator configures the authorization mode. This mode finds the permissions of the Pod"),
        (0, "The default of the API server is AlwaysAllow. kubeadm and Amazon EKS turn on RBAC")], after=6)
    zone(s, 6.30, 1.60, 1.70, 4.20, "Namespace: foo", color=STEPS[1], fill=E.CARD_BG)
    zone(s, 8.15, 1.60, 3.00, 4.20, "Namespace: bar", color=STEPS[1], fill=E.CARD_BG)
    zone(s, 11.30, 1.60, 1.45, 4.20, "Namespace: baz", color=STEPS[1], fill=E.CARD_BG)
    for x in (6.42, 7.20, 8.28, 9.25, 10.22, 11.67):
        box(s, x, 2.15, 0.70, 0.62, "Pod", STEPS[0], size=12)
    for x in (6.60, 7.38, 8.46, 9.43, 10.40):
        arrow(s, DOWN, x, 2.85, 0.32, 0.72, fill=SLATE)
    box(s, 6.42, 3.65, 1.48, 0.90, "ServiceAccount\ndefault", STEPS[5], size=12)
    box(s, 8.28, 3.65, 1.38, 0.90, "ServiceAccount\ndefault", STEPS[5], size=12)
    box(s, 9.74, 3.65, 1.31, 0.90, "ServiceAccount\nother", STEPS[5], size=12, radius=0.08)
    arrow(s, DOWN, 11.86, 2.85, 0.32, 1.07, fill=RED)
    arrow(s, LEFT, 11.09, 3.92, 1.09, 0.36, fill=RED)
    note(s, 11.36, 4.34, 1.33, 0.40, "Not possible", color=RED, bold=True)
    box(s, 11.36, 4.84, 1.33, 0.86, "ServiceAccount\ndefault", STEPS[5], size=12)
    note(s, 6.36, 4.70, 1.58, 0.70, "Many Pods use one ServiceAccount", bold=True)
    return s


def slide9(prs):
    s = new_slide(prs, "Authorization in Kubernetes")
    bullets(s, 0.60, 1.75, 12.10, [
        (0, "Before version 1.6.0, the RBAC mode was alpha. With the default mode AlwaysAllow, every client had full access to the Kubernetes API"),
        (0, "In version 1.8.0, the role-based access control (RBAC) authorization mode became generally available (GA)"),
        (0, "Properties of the RBAC authorization mode:"),
        (1, "RBAC stops unauthorized users from viewing or changing the cluster state"),
        (1, "A default or new ServiceAccount cannot create, read, update or delete objects until you grant it permissions")],
        size=16, after=10)
    return s


def slide10(prs):
    s = new_slide(prs, "API Groups")
    bullets(s, 0.60, 1.55, 5.00, [
        (0, "The Kubernetes API has many paths"),
        (1, "`/version`: the version of the cluster"),
        (1, "`/livez` and `/readyz`: the health of the API server"),
        (1, "`/api`: the core group, with the main functions of the cluster"),
        (1, "`/apis`: the named groups. All newer features are in a named group"),
        (2, "API groups"), (2, "Resources"), (2, "Verbs")], after=6)
    zone(s, 5.85, 1.50, 6.90, 2.32, "Core group", color=STEPS[0], fill=E.CARD_BG)
    tile(s, 7.70, 1.56, 1.00, 0.30, "/api", SLATE)
    arrow(s, RIGHT, 8.74, 1.61, 0.26, 0.20, fill=SLATE)
    tile(s, 9.04, 1.56, 0.80, 0.30, "/v1", SLATE)
    core = ["namespaces", "pods", "replicationcontrollers", "events", "endpoints", "nodes", "bindings",
            "persistentvolumes", "persistentvolumeclaims", "configmaps", "secrets", "services"]
    for k, name in enumerate(core):
        tile(s, 6.00 + (k % 3) * 2.22, 1.95 + (k // 3) * 0.45, 2.16, 0.38, name, STEPS[0], size=10.5)
    zone(s, 5.85, 3.90, 6.90, 2.75, "Named groups", color=STEPS[3], fill=E.CARD_BG)
    tile(s, 7.70, 3.96, 1.00, 0.30, "/apis", SLATE)
    groups = ["/apps", "/networking.k8s.io", "/certificates.k8s.io", "/rbac.authorization.k8s.io"]
    for x, w, name in zip((6.00, 6.92, 8.58, 10.40), (0.86, 1.60, 1.76, 2.24), groups):
        tile(s, x, 4.36, w, 0.38, name, STEPS[3], size=10)
    tile(s, 6.00, 4.84, 0.86, 0.34, "/v1", SLATE, size=10)
    note(s, 6.92, 4.82, 2.60, 0.34, "Resources of /apps/v1", align=PP_ALIGN.LEFT, bold=True)
    for k, name in enumerate(("deployments", "replicasets", "statefulsets")):
        tile(s, 6.00 + k * 1.46, 5.22, 1.40, 0.38, name, STEPS[3], size=10.5)
    note(s, 6.00, 5.66, 2.60, 0.34, "Verbs", align=PP_ALIGN.LEFT, bold=True)
    for k, name in enumerate(("list", "get", "create", "delete", "update", "watch")):
        tile(s, 6.00 + k * 1.10, 6.04, 1.04, 0.38, name, STEPS[1], size=10.5)
    return s


def slide11(prs):
    s = new_slide(prs, "Reaching the API")
    bullets(s, 0.60, 1.55, 12.10, [
        (0, "The API server treats a request with no credentials as the user `system:anonymous`"),
        (0, "This user can read `/version`, `/healthz`, `/livez` and `/readyz`. RBAC denies most other paths with 403 Forbidden"),
        (0, "`kubectl proxy` listens on port 8001 and authenticates each request for you")], h=1.15)
    term(s, 0.70, 2.80, 12.05, "bash, on the master node", CURL_API, size=13)
    return s


def slide12(prs):
    s = new_slide(prs, "Why Authorization")
    bullets(s, 0.60, 1.55, 5.60, [
        (0, "Authorization decides what users and ServiceAccounts can do after authentication"),
        (0, "It helps you to apply least privilege"),
        (0, "Developers must not change the nodes"),
        (0, "Use Roles and RoleBindings to restrict users to their own namespaces"),
        (0, "Authorization modes:"),
        (1, "Node authorization"), (1, "Attribute-based access control (ABAC)"), (1, "Role-based access control (RBAC)"),
        (1, "Webhook")])
    x0, heads = 6.45, ((3.00, "Command"), (1.08, "Admins"), (1.14, "Developers"), (1.08, "Bots"))
    x = x0
    for w, text in heads:
        E.add_rect(s, Inches(x), Inches(2.00), Inches(w), Inches(0.55), SLATE)
        note(s, x + 0.04, 2.00, w - 0.08, 0.55, text, color=E.WHITE, bold=True)
        x += w
    rows = (("$ kubectl get pods", "Allowed", "Allowed", "Forbidden"),
            ("$ kubectl get nodes", "Allowed", "Forbidden", "Forbidden"),
            ("$ kubectl delete node workernode2", "Allowed", "Forbidden", "Forbidden"))
    for r, row in enumerate(rows):
        y, x = 2.55 + r * 0.85, x0
        E.add_rect(s, Inches(x0), Inches(y), Inches(6.30), Inches(0.85), E.CARD_BG if r % 2 else E.WHITE, line=E.RULE_GRAY)
        for (w, _), text in zip(heads, row):
            if text.startswith("$"):
                E.add_text(s, Inches(x + 0.08), Inches(y), Inches(w - 0.12), Inches(0.85), text, font=E.FONT_MONO, size=11,
                           bold=True, color=SLATE, anchor=MSO_ANCHOR.MIDDLE)
            else:
                note(s, x, y, w, 0.85, text, color=GREEN if text == "Allowed" else RED, bold=True)
            x += w
    return s


def slide13(prs):
    s = new_slide(prs, "Authorization Modes")
    bullets(s, 0.60, 1.55, 5.20, [
        (0, "Node: the API server authorizes the requests of kubelets"),
        (0, "ABAC: a policy file with attributes decides"),
        (0, "How RBAC works"),
        (1, "RBAC gives a standard method to control access"),
        (1, "Define a Role, for example Developer"),
        (1, "Bind the user to that Role"),
        (0, "How a webhook works"),
        (1, "An external system makes all the authorization decisions"),
        (1, "A user sends a request to the API server, and Open Policy Agent allows or denies the request")], after=5)
    zone(s, 6.05, 1.50, 6.70, 2.72, "RBAC", color=STEPS[0], fill=E.CARD_BG)
    for y, text in ((1.86, "dev-user"), (2.40, "dev-user-2"), (2.94, "Group: developers"), (3.56, "security-1")):
        box(s, 6.20, y, 1.70, 0.46, text, STEPS[5], size=12)
        arrow(s, RIGHT, 7.96, y + 0.08, 0.62, 0.30, fill=SLATE)
    box(s, 8.65, 1.86, 3.95, 1.54, "Role: Developer\nList, get, create and update Pods\nCreate ConfigMaps", STEPS[3], size=13)
    box(s, 8.65, 3.50, 3.95, 0.58, "ClusterRole: Security\nView and approve certificate signing requests", STEPS[4], size=12)
    zone(s, 6.05, 4.30, 6.70, 2.35, "Webhook", color=STEPS[1], fill=E.CARD_BG)
    box(s, 6.20, 5.05, 1.20, 0.80, "dev-user", STEPS[5])
    arrow(s, RIGHT, 7.46, 5.28, 0.42, 0.34, fill=SLATE)
    box(s, 7.94, 5.05, 1.20, 0.80, "API server", STEPS[3])
    flow(s, 9.20, 4.68, 1.72, "Allow this request?", h=0.72)
    flow(s, 9.20, 5.46, 1.72, "Allow", kind=LEFT, fill=GREEN, h=0.72)
    box(s, 10.98, 5.05, 1.62, 0.80, "Open Policy Agent", STEPS[4])
    return s


def slide14(prs):
    s = new_slide(prs, "RBAC Introduction")
    bullets(s, 0.60, 1.65, 5.10, [
        (0, "To use RBAC:"),
        (1, "Create a Role"), (1, "Specify the rules"), (1, "Create a RoleBinding"),
        (1, "Bind the user to the Role with the RoleBinding"),
        (0, "A Role and a RoleBinding work in one namespace only")], size=15, after=8)
    box(s, 5.85, 2.25, 1.20, 1.10, "User\ndev-user", STEPS[5], size=13)
    arrow(s, RIGHT, 7.11, 2.62, 0.40, 0.34)
    zone(s, 7.57, 1.65, 5.18, 4.65, "One namespace", color=STEPS[1], fill=E.CARD_BG)
    E.add_rounded_rect(s, Inches(7.70), Inches(2.25), Inches(2.60), Inches(1.10), STEPS[3], radius_ratio=0.10)
    note(s, 7.74, 2.34, 2.52, 0.40, "RoleBinding", color=E.WHITE, bold=True)
    E.add_text(s, Inches(7.74), Inches(2.78), Inches(2.52), Inches(0.40), "devuser-developer-binding", font=E.FONT_MONO,
               size=10, bold=True, color=E.WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    arrow(s, RIGHT, 10.36, 2.62, 0.34, 0.34)
    box(s, 10.76, 2.25, 1.84, 1.10, "Role\ndeveloper", STEPS[4], size=13)
    arrow(s, DOWN, 11.51, 3.42, 0.34, 0.42)
    note(s, 7.70, 3.92, 3.00, 0.34, "The rules of the Role", align=PP_ALIGN.LEFT, bold=True)
    tile(s, 7.70, 4.32, 1.70, 0.72, "pods", STEPS[0], size=13)
    box(s, 9.48, 4.32, 3.12, 0.72, "list, get, create, update", STEPS[1], size=14)
    tile(s, 7.70, 5.14, 1.70, 0.72, "configmaps", STEPS[0], size=13)
    box(s, 9.48, 5.14, 3.12, 0.72, "create", STEPS[1], size=14)
    return s


def slide15(prs):
    s = new_slide(prs, "Role and RoleBinding")
    role = ["# RBAC matches the name in the API path: configmaps."] + ROLE
    bottom = term(s, 0.70, 1.55, 5.95, "developer-role.yaml, part 1", role, size=11, yaml=True, h=3.50)
    term(s, 6.85, 1.55, 5.90, "developer-role.yaml, part 2", BINDING, size=11, yaml=True, h=3.50)
    term(s, 0.70, bottom + 0.12, 12.05, "bash", ["# Save the two parts in one file. The lab uses the namespace week13.",
                                                 "$ kubectl apply -f developer-role.yaml"], size=12)
    return s


def slide16(prs):
    s = new_slide(prs, "RBAC Resources")
    bullets(s, 0.60, 1.55, 5.60, [
        (0, "Roles and ClusterRoles set which verbs a subject can use on which resources"),
        (0, "Verbs: `create`, `delete`, `deletecollection`, `get`, `list`, `patch`, `update`, `watch`"),
        (0, "RoleBindings and ClusterRoleBindings bind a role to users, groups or ServiceAccounts"),
        (0, "A role defines what a subject can do. A binding defines who can do it"),
        (0, "RBAC rules only add permissions. There is no deny rule")], after=8)
    zone(s, 6.35, 1.75, 1.85, 4.45, "Who", color=STEPS[1], fill=E.CARD_BG)
    for y, text in ((2.20, "Admins group"), (3.45, "User A"), (4.70, "ServiceAccount")):
        box(s, 6.47, y, 1.61, 1.00, text, STEPS[5], size=12)
    arrow(s, RIGHT, 8.24, 3.78, 0.24, 0.34, fill=SLATE)
    box(s, 8.52, 3.45, 1.20, 1.00, "RoleBinding", STEPS[3], size=12)
    arrow(s, RIGHT, 9.76, 3.78, 0.24, 0.34, fill=SLATE)
    box(s, 10.04, 2.40, 0.72, 3.10, "Role", STEPS[4], size=12)
    arrow(s, RIGHT, 10.80, 2.82, 0.30, 0.34, fill=GREEN)
    arrow(s, RIGHT, 10.80, 4.72, 0.30, 0.34, fill=RED)
    box(s, 11.14, 2.40, 1.61, 1.18, "Some resources\nAllowed", GREEN, size=12)
    box(s, 11.14, 4.30, 1.61, 1.18, "Other resources\nNot allowed", RED, size=12)
    return s


def namespace_box(s, x, name):
    zone(s, x, 1.50, 2.20, 2.72, name, color=STEPS[1], fill=E.CARD_BG)
    box(s, x + 0.08, 1.92, 1.18, 0.46, "RoleBinding", STEPS[3], size=12)
    arrow(s, RIGHT, x + 1.28, 2.01, 0.18, 0.28, fill=SLATE)
    box(s, x + 1.48, 1.92, 0.64, 0.46, "Role", STEPS[4], size=12)
    arrow(s, DOWN, x + 1.66, 2.42, 0.28, 0.26, fill=SLATE)
    box(s, x + 0.96, 2.72, 1.16, 0.62, "Namespaced resources", STEPS[0], size=12)


def slide17(prs):
    s = new_slide(prs, "ClusterRoles and ClusterRoleBindings")
    bullets(s, 0.60, 1.55, 4.90, [
        (0, "Some Kubernetes resources have no namespace, for example nodes and PersistentVolumes"),
        (0, "Some API paths, such as `/readyz`, are not Kubernetes resources"),
        (0, "Cluster administrators need cluster-level access"),
        (0, "A ClusterRole covers these cases"),
        (0, "A ClusterRole can also be a common role. RoleBindings in many namespaces can use it")], h=3.55)
    term(s, 0.70, 5.20, 4.75, "bash", ["# NAMESPACED is false.", "$ kubectl api-resources --sort-by name \\",
                                       "    | grep -E 'NAMESPACED|^nodes'"], size=11)
    for x, name in ((5.65, "Namespace A"), (8.00, "Namespace B"), (10.35, "Namespace C")):
        namespace_box(s, x, name)
    box(s, 8.08, 3.44, 1.18, 0.46, "RoleBinding", STEPS[3], size=12)
    zone(s, 5.65, 4.32, 6.90, 2.33, "Cluster scope: no namespace", color=SLATE, fill=E.CARD_BG)
    arrow(s, DOWN, 8.53, 3.94, 0.28, 1.06, fill=SLATE)
    note(s, 8.90, 4.40, 3.55, 0.56, "A RoleBinding grants the rules of a ClusterRole in its own namespace only", bold=True)
    box(s, 5.85, 5.08, 1.85, 0.90, "ClusterRoleBinding", STEPS[3], size=12)
    arrow(s, RIGHT, 7.76, 5.36, 0.30, 0.34, fill=SLATE)
    box(s, 8.12, 5.08, 1.40, 0.90, "ClusterRole", STEPS[4], size=12)
    arrow(s, RIGHT, 9.58, 5.36, 0.30, 0.34, fill=SLATE)
    box(s, 9.94, 5.08, 2.40, 0.90, "Cluster-level resources", STEPS[0], size=12)
    return s


def slide18(prs):
    s = new_slide(prs, "A ClusterRole for PersistentVolumes")
    bullets(s, 0.60, 1.55, 12.10, [
        (0, "To grant access to a cluster-level resource, always use a ClusterRoleBinding"),
        (0, "`kubectl auth whoami` shows your user and groups. `kubectl auth can-i` tests an action. "
            "`--as` tests it for another subject")], h=0.80)
    term(s, 0.70, 2.40, 12.05, "bash", PV_READER, size=10)
    return s


def slide19(prs):
    s = new_slide(prs, "Default ClusterRoles and ClusterRoleBindings")
    bullets(s, 0.60, 1.55, 6.00, [
        (0, "The API server creates default ClusterRoles and ClusterRoleBindings"),
        (0, "User-facing roles:"),
        (1, "`cluster-admin`: any action on any resource"),
        (1, "`admin`: read and write access in a namespace, with Roles and RoleBindings"),
        (1, "`edit`: read and write access in a namespace, with no Roles and no RoleBindings"),
        (1, "`view`: read access in a namespace, with no Secrets"),
        (0, "The names of most other default roles start with `system:`")])
    term(s, 6.80, 1.60, 5.95, "bash", DEFAULTS, size=10.5)
    return s


def slide20(prs):
    s = new_slide(prs, "Amazon EKS Authentication for IAM Users and Roles")
    bullets(s, 0.60, 1.55, 5.45, [
        (0, "An identity provider (IdP), such as Active Directory (AD), an OIDC provider or AWS IAM, must store and verify "
            "user identities"),
        (0, "Amazon EKS maps these identities to Kubernetes users and groups"),
        (0, "The Amazon EKS control plane uses:"),
        (1, "Authentication: webhook token authentication"),
        (1, "Authorization: RBAC, then the Amazon EKS authorizer for access policies"),
        (0, "AWS IAM does not control the permissions inside the cluster. Kubernetes RBAC or EKS access policies control them")])
    note(s, 6.20, 1.46, 1.85, 0.84, "1. Generate a signed AWS Security Token Service (STS) URL", bold=True)
    box(s, 6.40, 2.35, 1.30, 1.15, "Client", STEPS[5])
    flow(s, 7.76, 2.22, 1.56, "2. AWS identity", h=0.68)
    flow(s, 7.76, 2.98, 1.56, "4. Allow or deny", kind=LEFT, fill=GREEN, h=0.68)
    box(s, 9.38, 2.20, 1.30, 1.46, "API server", STEPS[3])
    flow(s, 10.74, 2.22, 1.10, "3. Verify", h=0.68)
    flow(s, 10.74, 2.98, 1.10, "Identity", kind=LEFT, fill=STEPS[1], h=0.68)
    box(s, 11.90, 2.20, 0.85, 1.46, "AWS STS", STEPS[4])
    arrow(s, UP_DOWN, 9.90, 3.72, 0.26, 0.78, fill=SLATE)
    box(s, 8.88, 4.56, 2.30, 0.95, "Role-based access control (RBAC)", STEPS[5])
    return s


def slide21(prs):
    s = new_slide(prs, "Special Case: The IAM Identity That Created the Cluster")
    bullets(s, 0.60, 1.55, 5.75, [
        (0, "In the `CONFIG_MAP` mode, Amazon EKS grants `system:masters` permissions to the IAM role or IAM user that "
            "creates the cluster"),
        (0, "Members of `system:masters` bypass all RBAC checks. No binding can revoke this access"),
        (0, "`cluster-admin` is a very powerful role. Use it with the same care as the root user"),
        (0, "In the `CONFIG_MAP` mode, no visible configuration shows this mapping"),
        (0, "In the `API` and `API_AND_CONFIG_MAP` modes, Amazon EKS creates a cluster admin access entry for this identity "
            "by default")], after=6)
    term(s, 6.55, 1.60, 6.20, "bash", CLUSTER_ADMIN, size=10)
    return s


def slide22(prs):
    s = new_slide(prs, "Mapping IAM Identities to Kubernetes Users and Groups")
    bullets(s, 0.60, 1.55, 5.00, [
        (0, "AWS recommends access entries. You manage an access entry with the EKS API, the AWS CLI or the AWS console"),
        (0, "The `aws-auth` ConfigMap is the older method. AWS marks it as deprecated"),
        (0, "This ConfigMap is in the namespace `kube-system`, and it has these sections:"),
        (1, "`mapRoles`"), (1, "`mapUsers`"), (1, "`mapAccounts`"),
        (0, "A cluster has one of three authentication modes: `CONFIG_MAP`, `API_AND_CONFIG_MAP` or `API`")], after=6)
    term(s, 5.80, 1.60, 6.95, "aws-auth ConfigMap", AWS_AUTH, size=10.5, yaml=True)
    return s


def slide23(prs):
    s = new_slide(prs, "Amazon EKS Access for IAM Users: Server Side")
    box(s, 0.70, 3.35, 1.20, 1.10, "Client", STEPS[5])
    flow(s, 1.96, 2.92, 1.82, "IAM token and Kubernetes action", h=0.92)
    flow(s, 1.96, 3.96, 1.82, "Allow or deny", kind=LEFT, fill=GREEN, h=0.92)
    box(s, 3.84, 2.00, 1.40, 3.80, "EKS API server", STEPS[3], size=14)
    flow(s, 5.30, 1.96, 1.72, "IAM token", h=0.72)
    flow(s, 5.30, 2.74, 1.72, "Kubernetes user", kind=LEFT, h=0.72)
    flow(s, 5.30, 4.44, 1.72, "User and action", h=0.72)
    flow(s, 5.30, 5.22, 1.72, "Allow or deny", kind=LEFT, fill=GREEN, h=0.72)
    zone(s, 7.10, 1.50, 5.65, 2.55, "Authentication: webhook", color=STEPS[1], dashed=True, fill=E.CARD_BG)
    box(s, 7.25, 1.90, 2.65, 0.82, "AWS IAM Authenticator server", STEPS[1], size=13)
    arrow(s, BOTH, 9.96, 2.14, 1.20, 0.34, fill=SLATE)
    box(s, 11.22, 1.90, 1.40, 0.82, "AWS STS", STEPS[4])
    arrow(s, UP_DOWN, 8.46, 2.75, 0.24, 0.42, fill=SLATE)
    box(s, 7.25, 3.20, 2.65, 0.72, "aws-auth or access entries", STEPS[5], size=13)
    note(s, 9.96, 2.56, 2.70, 0.56, "The server verifies the IAM identity", bold=True)
    zone(s, 7.10, 4.15, 5.65, 2.05, "Authorization", color=STEPS[0], dashed=True, fill=E.CARD_BG)
    box(s, 7.25, 4.55, 2.65, 0.74, "Role-based access control (RBAC)", STEPS[3], size=13)
    arrow(s, BOTH, 9.96, 4.75, 0.70, 0.34, fill=SLATE)
    box(s, 10.72, 4.55, 1.90, 0.74, "Roles and RoleBindings", STEPS[5], size=13)
    box(s, 7.25, 5.36, 2.65, 0.74, "Amazon EKS authorizer", STEPS[3], size=13)
    arrow(s, BOTH, 9.96, 5.56, 0.70, 0.34, fill=SLATE)
    box(s, 10.72, 5.36, 1.90, 0.74, "EKS access policies", STEPS[5], size=13)
    return s


def slide24(prs):
    s = new_slide(prs, "Amazon EKS Access for IAM Users: Client Side")
    zone(s, 0.70, 1.50, 8.20, 5.15, "Client host", color=SLATE, dashed=True, fill=E.CARD_BG)
    for x, name in ((3.05, "kubectl"), (4.40, "kubelet"), (5.75, "Code")):
        tile(s, x, 1.92, 1.20, 0.68, name, STEPS[5], size=13)
    arrow(s, DOWN, 4.82, 2.66, 0.36, 0.56, fill=SLATE)
    note(s, 5.26, 2.66, 2.20, 0.56, "Kubernetes action", align=PP_ALIGN.LEFT, bold=True)
    box(s, 3.65, 3.28, 2.70, 1.00, "Kubernetes client library", STEPS[3], size=14)
    flow(s, 2.35, 3.46, 1.24, "Read", kind=LEFT, h=0.62)
    tile(s, 0.90, 3.40, 1.40, 0.76, "kubeconfig", STEPS[1], size=12)
    flow(s, 6.41, 3.28, 2.44, "IAM token and action", h=1.00)
    arrow(s, DOWN, 4.28, 4.34, 0.36, 0.86, fill=SLATE)
    note(s, 3.52, 4.54, 0.72, 0.42, "Run", bold=True)
    arrow(s, UP, 5.36, 4.34, 0.36, 0.86, fill=SLATE)
    note(s, 5.76, 4.46, 1.50, 0.58, "IAM token", align=PP_ALIGN.LEFT, bold=True)
    tile(s, 3.65, 5.28, 2.70, 0.92, "aws eks get-token", STEPS[1], size=14)
    arrow(s, RIGHT, 8.92, 3.60, 0.70, 0.36)
    box(s, 9.68, 3.10, 3.07, 1.36, "EKS API server", STEPS[3], size=15)
    return s


def slide25(prs):
    s = new_slide(prs, "References")
    bullets(s, 0.60, 1.75, 12.10, [(0, url) for url in REFERENCES], size=16, after=10)
    return s


def main():
    prs = Presentation(SRC)
    keep_first(prs, 3)
    cover, agenda, outline = prs.slides[0], prs.slides[1], prs.slides[2]
    by_name = {sh.name: sh for sh in cover.shapes}
    set_only_run(by_name["TextBox 1"], "Introduction to K8s RBAC")
    set_only_run(by_name["TextBox 2"], "Week 13 · Lecture")
    set_only_run(by_name["TextBox 3"], "Authentication, RBAC and Amazon EKS")
    current_week(outline)
    old = [sh for sh in agenda.shapes if sh.name == "TextBox 3"][0]
    old._element.getparent().remove(old._element)
    bullets(agenda, 0.60, 1.75, 12.10, [
        (0, "Understanding authentication"),
        (0, "What ServiceAccounts are and why Pods use them"),
        (0, "Understanding role-based access control (RBAC)"),
        (0, "Using Roles and RoleBindings"),
        (0, "Using ClusterRoles and ClusterRoleBindings"),
        (0, "Understanding the default roles and bindings"),
        (0, "Enabling IAM users to access an Amazon EKS cluster")], size=16, after=10)
    built = [cover, agenda, outline]
    for make in (slide4, slide5, slide6, certificate_slide, slide7, slide8, slide10, slide11, slide12, slide9, slide13,
                 slide14, slide16, slide15, slide17, slide18, slide19, slide20, slide22, slide21, slide23, slide24, slide25):
        built.append(make(prs))
    total = len(built)
    for no, s in enumerate(built, 1):
        if no <= 3:
            for sh in s.shapes:
                if sh.has_text_frame and sh.text_frame.text.startswith("CLO835, Fall 2026"):
                    set_only_run(sh, "CLO835, Fall 2026     %d / %d" % (no, total))
        else:
            E.whale_and_footer(s, no, total)
    finish(prs, "CLO835 Week 13 Lecture: Authentication, RBAC and Amazon EKS")
    E._sanitize_coords(prs)
    prs.save(OUT)
    print("wrote %s (%d slides)" % (OUT, total))


if __name__ == "__main__":
    import sys
    # SHOULD-FIX 14 of review round 2 (2026-11-11): this old builder overwrote delivered files.
    # Use build_week13_lecture_v9.py. Importing this file still works.
    sys.exit("build_week13_lecture_v8.py is an old version. Use build_week13_lecture_v9.py.")
    main()
