# -*- coding: utf-8 -*-
"""CLO835 Week 13 lecture v10 - Authentication, RBAC and EKS.

v10 takes lecture v9 (build_week13_lecture_v9.py) by import and replaces only the slide functions that the Week 13
v10 loop changes (report 2026-11-18-08). v9 stays on disk. The slide count (32) and the slide numbers do not change.

Phase 1 audit (the defects L1 to L5) and their fixes:
- L1 (B7), slide 5: "Each request to the API server has three phases" was false for a read. The first bullet says
  "A request to the API server passes two or three phases, in this order:". The last bullet says that the API
  server stores the new or changed object after admission control.
- L2 (B7), slide 20: a new ServiceAccount outside kube-system has only the permissions of every authenticated user
  (system:discovery, system:basic-user, system:public-info-viewer), not only the discovery permissions.
- L3 (B7, C8): each topic that slide 31 names as "Not in the lab" has a "Concept only" label on its slide.
- L4 (B7), slide 31: one list, with one line for each part, in place of five "Also not in the lab:" paragraphs.
  Each sentence has 25 words or fewer (the gate splits a sentence at a period or a colon).
- L5 (A5, C8): the lab is build_week13_lab_v6 (V.lab, V.LAB and V.FILES), and the paths are Week13/.
- Page read of phase 3: the slide 17 label is one line below the third bullet; the slide 31 note has five lines.

Phase 4 finding P2 (C4): the run values of slides 9, 12 and 23 come from pass 1 of 2026-11-18
(scratchpad w13live/gate/run1.log): AGE 0s, notAfter=Nov 20 04:26:24 2026 GMT, the credential-id hash, and
"resourceVersion": "678".

Review round 1 (scratchpad w13review_r1/lecture.md, 6 MUST-FIX and 8 SHOULD-FIX), all applied:
- L-M1, slide 5: admission control acts on a request that creates, changes, deletes or connects to an object
  (for example kubectl exec), not on a request that only reads. The diagram box says "Create, change, delete,
  connect".
- L-M2, slides 15 and 31: kubectl wait uses watch, kubectl certificate approve uses update, and the ClusterRole
  view has watch. So the label and the note say "no rule that the lab writes has watch, patch or deletecollection"
  and "No command of dev-user uses update or configmaps".
- L-M3, slides 6, 17 and 31: the slide 6 label names no group system:unauthenticated (the anonymous request of
  Step 2 has it); the note names "nodes or a path in a ClusterRole".
- L-M4, slide 20: the label does not say that the lab uses no other namespace (Step 5 tests clo835 in default),
  and it names no ServiceAccount default (the Pod web of Step 3 gets it).
- L-M5, slide 17: the two verdict boxes say "auth can-i: no" and "auth can-i: yes", so "a PersistentVolume has no
  namespace" and "in the whole cluster" are each stated at most two times.
- L-M6, slide 20: the example of the last bullet is kubectl auth whoami only, so /api is stated two times.
- L-S1, slide 8: "kube-controller-manager never approves a CSR for this signer automatically".
- L-S2, slides 10 and 31: "the discovery path /api" (Steps 4 and 5 read /api/v1/namespaces/week13/services).
- L-S3, slide 14: "The first authorizer that allows or denies the request decides".
- L-S4, slides 14 and 15: the least-privilege point moves to the caption of slide 15.
- L-S5, slide 21: "ca.crt in the directory of the token".
- L-S6, slide 12: "Extra shows a hash of the certificate".
- L-S7, slide 22: the verb list for a GET of a collection, the verb get for a GET of one object.
- L-S8, slide 10: the value "" in apiGroups is the core group.
- The Step 5 comment of lab v6 (lab finding B-S3) reaches slide 23 through pick().

Review round 2 (scratchpad w13review_r2/lecture.md, 4 MUST-FIX and 8 SHOULD-FIX), all applied:
- L-M1, slide 6: "Kubernetes stores no normal users and no groups" (it stores ServiceAccounts).
- L-M2, slide 15: "the lab does not write a rule with watch, patch or deletecollection" (view has watch).
- L-M3, slide 17, and L-M4, slides 20 and 31: the labels have the form "the lab does not ..." and are true; the
  lab shows that a new ServiceAccount gets Forbidden, so the label and the note name "kubectl auth whoami as a
  ServiceAccount" in place of "the default permissions of a new ServiceAccount".
- L-S1, L-S2, slide 31 (and slide 18): "the rule for the prefix system:"; no ClusterRole cluster-admin and no
  group kubeadm:cluster-admins in the note (kubernetes-admin is in kubeadm:cluster-admins).
- L-S3, slide 21: the user name is on one line. L-S4, slide 23: a subject can be a ServiceAccount of another
  namespace (concept only). L-S5, slide 22: the verbs of POST, PUT, PATCH and DELETE (PATCH concept only).
- L-S6, slide 27: in the mode CONFIG_MAP you cannot remove the creator access. L-S7, slides 7 and 30: "verifies",
  "user". L-S8, slide 8: the CertificateSigningRequest API is stable in v1.19.

Review round 3 (scratchpad w13review_r3/lecture.md, 3 MUST-FIX and 7 SHOULD-FIX), all applied:
- L-M1, slide 16: the bullet on developers-view does not repeat "in week13 only" (slide 17 and the lab comment
  state it). L-M3, slide 30: bullet 3 does not repeat that RBAC decides (slides 5 and 21 state it).
- L-M2, slide 31: "a PATCH request" is in the Part 3 line (slide 22 is in Part 3).
- L-S1, slide 5: a no-break space keeps `kubectl exec` on one line. L-S2, slide 11: the sample has "details": {}.
- L-S3, slide 31: the Part 1 sentence has 25 words or fewer. L-S4, slide 8: expirationSeconds is stable in v1.24.
- L-S5, slide 15: "The request verbs". L-S6, slide 17 (12.2.4): a ClusterRoleBinding for the Pods of all
  namespaces, concept only, also in the slide 31 note. L-S7, slide 27: "admin permissions" (one word, A1).

check_note31() of v10 (a copy of v9 with one change: a RoleBinding phrase may name a ServiceAccount of another
namespace) checks the note of slide 31, with the phrases of QUAL31 below. MAP31 does not change.

Input : Week13/Lecture_week13_v8.pptx, for the cover, the agenda and the outline (read, never written).
Output: Week13/Lecture_week13_v10.pptx. The build does not overwrite it, unless you give --force. The code that
writes the output runs only under __main__, so an import writes nothing.
"""
import re

import build_week13_lab_v6 as lab
import build_week13_lecture_v9 as V
from build_week13_lecture_v9 import (E, GREEN, LEFT, PP_ALIGN, RED, RIGHT, DOWN, SLATE, STEPS, TOP, API_RESOURCES,
                                     EKS_SHORT, FORBIDDEN_JSON, arrow, box, bullets, code_box, concept, eks_label,
                                     flow, grid, mark, new_slide, pick, rich, run, shell, text_slide, zone,
                                     zone_code)

VERSION = "v10"
V.VERSION = VERSION
V.SRC = "Week13/Lecture_week13_v8.pptx"
V.OUT = "Week13/Lecture_week13_%s.pptx" % VERSION

# L5: the lab of v6 is the single source of each lab line.
V.lab = lab
V.LAB = {n: lab.SLIDES[2 + n][3] for n in range(1, 6)}
V.FILES = {n: lab.SLIDES[2 + n][6] for n in (1, 3, 4, 5)}
assert lab.VERSION == "v6"

# P2: the run values of pass 1 of 2026-11-18 (Kubernetes v1.35.10).
V.CSR_TABLE = ["NAME       AGE   SIGNERNAME                            REQUESTOR          REQUESTEDDURATION   CONDITION",
               "dev-user   0s    kubernetes.io/kube-apiserver-client   kubernetes-admin   24h                 "
               "Approved,Issued"]
V.WHOAMI = ["ATTRIBUTE                                           VALUE",
            "Username                                            dev-user",
            "Groups                                              [developers system:authenticated]",
            "Extra: authentication.kubernetes.io/credential-id   [X509SHA256=4e6be90f19215b7a4e7b0274b815f7963d2c6120855a"
            "40e0b15b1e01468de116]"]
V.SERVICE_LIST = [l.replace('"670"', '"678"') for l in V.SERVICE_LIST]
assert '    "resourceVersion": "678"' in V.SERVICE_LIST
NOT_AFTER = "notAfter=Nov 20 04:26:24 2026 GMT"


def s_path(prs):
    """Slide 5 (L1, L3, L-M1)."""
    s = new_slide(prs, "The Path of a Request to the API Server")
    bullets(s, 0.60, 1.65, 6.20, [
        (0, "A request to the API server passes two or three phases, in this order:"),
        (1, "Authentication finds the user name and the groups of the client"),
        (1, "Authorization decides if this user can do this action on this object"),
        (1, "Admission control can change or reject a request that creates, changes, deletes or connects to an "
            "object, for example `kubectl\u00a0exec`. It does not act on a request that only reads an object"),
        (0, "The API server answers 401 Unauthorized when it cannot verify the credentials. It answers 403 "
            "Forbidden to a denied action"),
        (0, "After admission control, the API server stores the new or changed object in etcd")],
        size=16, after=11, h=4.30)
    concept(s, 0.60, 6.10, 6.20, "Concept only: the lab does not configure or show admission control. It does not "
            "get the answer 401.")
    code_box(s, 7.05, 3.30, 1.40, 1.00, "Client", "kubectl", STEPS[5], size=13)
    arrow(s, RIGHT, 8.50, 3.62, 0.38, 0.38)
    zone(s, 8.95, 1.65, 2.55, 4.55, "API server", color=STEPS[1], fill=E.CARD_BG)
    for k, (text, fill) in enumerate((("1. Authentication\nWho are you?", STEPS[0]),
                                      ("2. Authorization\nCan you do this?", STEPS[3]),
                                      ("3. Admission control\nCreate, change, delete, connect", STEPS[4]))):
        y = 2.10 + k * 1.45
        box(s, 9.10, y, 2.25, 1.00, text, fill, size=13)
        if k < 2:
            arrow(s, DOWN, 10.05, y + 1.05, 0.34, 0.36, fill=SLATE)
    for y, text in ((2.42, "401\nUnauthorized"), (3.87, "403\nForbidden")):
        arrow(s, RIGHT, 11.42, y, 0.30, 0.36, fill=RED)
        mark(s, 11.76, y - 0.22, 1.00, 0.80, text, color=RED)
    arrow(s, RIGHT, 11.42, 5.32, 0.30, 0.36, fill=SLATE)
    box(s, 11.76, 5.05, 0.99, 0.90, "etcd", SLATE, size=13)
    return s


def s_clients(prs):
    """Slide 6 (L3, L-M3: the anonymous request of Step 2 has the group system:unauthenticated)."""
    s = new_slide(prs, "Users, ServiceAccounts and Groups")
    end = grid(s, 0.60, 1.62, [1.65, 1.85, 2.00, 3.60, 3.00], [
        ["Client", "Who it is", "Stored in Kubernetes", "User name in the lab", "Groups in the lab"],
        ["A normal user", "A person, for example a developer", "No. An outside system manages it", "`dev-user`",
         ["`developers`", "`system:authenticated`"]],
        ["A ServiceAccount", "A process in a Pod", "Yes, as an object in a namespace",
         "`system:serviceaccount:week13:clo835`",
         ["`system:serviceaccounts`", "`system:serviceaccounts:week13`", "`system:authenticated`"]],
        ["An anonymous request", "A request with no credentials", "No", "`system:anonymous`",
         "`system:unauthenticated`"]], row_h=0.92, size=12)
    bullets(s, 0.60, end + 0.20, 12.10, [
        (0, "Kubernetes stores no normal users and no groups. The API server finds them in the credentials of each "
            "request"),
        (0, "Bind a role to a group, not to each user. Kubernetes reserves the prefix `system:` for its own names")],
        size=15, after=6, h=0.85)
    concept(s, 0.60, 6.20, 12.10, "Concept only: the lab does not show the groups of `clo835` or the rule for the "
            "prefix `system:`.")
    return s


def s_certificate(prs):
    """Slide 8 (L3, L-S1)."""
    s = new_slide(prs, "A Client Certificate Is a User")
    bullets(s, 0.60, 1.65, 7.00, [
        (0, "Kubernetes trusts each client certificate that the cluster CA signed"),
        (0, "The common name (CN) is the user name. Each organization (O) field is a group"),
        (0, "The CertificateSigningRequest API (stable in v1.19) asks a signer for a certificate"),
        (0, "The signer `kubernetes.io/kube-apiserver-client` signs only an approved CSR. kube-controller-manager "
            "never approves a CSR for this signer automatically"),
        (0, "`expirationSeconds: 86400` (stable in v1.24) asks for 24 hours. The minimum is 600 seconds (ten minutes)"),
        (0, "Kubernetes v1.35 cannot revoke a certificate: it is valid until it expires. A short lifetime limits "
            "the risk of a lost key")], size=16, after=10, h=4.40)
    concept(s, 0.60, 6.15, 7.00, "Concept only: the lab does not test the minimum lifetime or the revocation of a "
            "certificate.")
    rows = (("Create the key and the CSR", "openssl genrsa\nopenssl req", STEPS[0], 1.05),
            ("Send the CSR to the API server", "CertificateSigningRequest", STEPS[1], 0.80),
            ("An administrator approves the CSR", "$ kubectl certificate approve dev-user", STEPS[3], 0.80),
            ("The cluster CA signs the certificate", ".status.certificate", STEPS[4], 0.80))
    y = 1.65
    for k, (head, code, fill, high) in enumerate(rows):
        code_box(s, 7.95, y, 4.80, high, head, code, fill, size=13)
        y += high
        if k < 3:
            arrow(s, DOWN, 10.18, y + 0.06, 0.34, 0.30, fill=SLATE)
            y += 0.42
    return s


def s_certificate_lab(prs):
    """Slide 9 (P2: the end date of pass 1)."""
    s = new_slide(prs, "The Certificate of dev-user")
    shell(s, 0.60, 1.55, 5.30, "dev-user-csr.yaml (Lab Week 13, Step 1)", V.FILES[1], size=10.5)
    bullets(s, 6.20, 1.65, 6.55, [
        (0, "The lab command `cat > dev-user-csr.yaml <<EOF` has no quotes on `EOF`. So the shell writes the "
            "base64 request into the file"),
        (0, "`REQUESTEDDURATION` 24h comes from `expirationSeconds: 86400`"),
        (0, "Approved,Issued: an administrator approved the CSR, and the CA signed the certificate"),
        (0, "`kubectl get csr` reads the certificate from `.status.certificate`. `base64 -d` decodes it")],
        size=14, after=6, h=2.25)
    shell(s, 0.60, 3.98, 12.15, "Lab Week 13, Step 1", run(
        1, ("$ openssl genrsa", []), ("$ openssl req", []),
        ("$ kubectl apply", ["certificatesigningrequest.certificates.k8s.io/dev-user created"]),
        ("$ kubectl certificate approve", ["certificatesigningrequest.certificates.k8s.io/dev-user approved"]),
        ("$ kubectl get csr dev-user  ", V.CSR_TABLE),
        ("$ kubectl get csr dev-user -o", []),
        ("$ openssl x509", ["subject=O=developers, CN=dev-user", NOT_AFTER])),
        size=9.5)
    return s


def s_api(prs):
    """Slide 10 (L-S2, L-S8)."""
    s = new_slide(prs, "API Groups and Paths")
    bullets(s, 0.60, 1.62, 5.00, [
        (0, "The core group is at `/api/v1`. Its objects have `apiVersion: v1`"),
        (0, "A named group is at `/apis/<group>/<version>`, for example `/apis/apps/v1`"),
        (0, "An RBAC rule has the fields `apiGroups`, `resources` and `verbs`. The value `\"\"` in `apiGroups` is the "
            "core group. Each tile of the diagram is a value of `resources`"),
        (0, "Each authenticated user can read the discovery paths, for example `/api` and `/apis`")],
        size=15, after=8, h=4.40)
    concept(s, 0.60, 6.10, 5.00, "Concept only: the lab does not read the discovery path `/api`.")
    zone_code(s, 5.85, 1.62, 6.90, 1.90, "Core group: `/api/v1`", color=STEPS[0], fill=E.CARD_BG)
    core = ["pods", "services", "configmaps", "secrets", "namespaces", "nodes", "serviceaccounts",
            "persistentvolumes", "persistentvolumeclaims"]
    for k, name in enumerate(core):
        x, w = ((6.00, 2.00), (8.06, 2.12), (10.24, 2.36))[k % 3]
        code_box(s, x, 2.02 + (k // 3) * 0.47, w, 0.40, name, "", STEPS[0], size=12, mono_head=True)
    zone_code(s, 5.85, 3.62, 6.90, 2.98, "Named groups: `/apis/<group>/<version>`", color=STEPS[3], fill=E.CARD_BG)
    groups = (("apps/v1", (("deployments", 1.75), ("replicasets", 1.75), ("statefulsets", 1.75))),
              ("rbac.authorization.k8s.io/v1", (("roles", 0.95), ("rolebindings", 1.50), ("clusterroles", 1.50),
                                                ("clusterrolebindings", 2.25))),
              ("certificates.k8s.io/v1", (("certificatesigningrequests", 2.85),)))
    for k, (group, names) in enumerate(groups):
        y = 4.00 + k * 0.86
        mark(s, 6.00, y, 4.50, 0.30, "`%s`" % group, align=PP_ALIGN.LEFT)
        x = 6.00
        for name, w in names:
            code_box(s, x, y + 0.33, w, 0.40, name, "", STEPS[3], size=12, mono_head=True)
            x += w + 0.08
    return s


def s_whoami(prs):
    """Slide 12 (L-S6; P2: the hash of pass 1)."""
    s = new_slide(prs, "Authenticated, Not Authorized")
    bullets(s, 0.60, 1.62, 12.10, [
        (0, "`kubectl config set-credentials` writes the certificate and the key of `dev-user` into the kubeconfig "
            "file"),
        (0, "`kubectl config set-context` links `dev-user` to the cluster `kubernetes` and the namespace `week13`"),
        (0, "`kubectl auth whoami` (stable in v1.28) shows the user and the groups that the API server finds. Extra "
            "shows a hash of the certificate"),
        (0, "No Role allows `dev-user` to list Pods yet, so the API server denies `get pods`")], size=16, after=5,
        h=1.80)
    shell(s, 0.60, 3.50, 12.15, "Lab Week 13, Step 2", run(
        2, ("$ kubectl create namespace", ["namespace/week13 created"]),
        ("$ kubectl config set-credentials", ['User "dev-user" set.']),
        ("$ kubectl config set-context", ['Context "dev-user@kubernetes" created.']),
        ("$ kubectl --context=dev-user@kubernetes auth whoami", V.WHOAMI),
        ("$ kubectl --context=dev-user@kubernetes get pods",
         ['Error from server (Forbidden): pods is forbidden: User "dev-user" cannot list resource "pods" in API '
          'group "" in the namespace "week13"'])), size=10.5)
    return s


def s_modes(prs):
    """Slide 14 (L-S3; L-S4: the least-privilege bullet moves to slide 15)."""
    s = new_slide(prs, "Authorization Modes")
    bullets(s, 0.60, 1.62, 6.70, [
        (0, "The API server asks its authorizers in order. The first authorizer that allows or denies the request "
            "decides"),
        (0, "When no authorizer has an opinion, the API server denies the request"),
        (0, "The modes of the flag `--authorization-mode`:"),
        (1, "`Node`: the requests of a kubelet, for the Pods on its node"),
        (1, "`RBAC`: Roles and bindings, as API objects (stable in v1.8)"),
        (1, "`Webhook`: an outside service allows, denies or has no opinion"),
        (1, "`ABAC`: a policy file on the API server"),
        (1, "`AlwaysAllow` and `AlwaysDeny`: for tests only"),
        (0, "The default is `AlwaysAllow`. kubeadm sets `Node,RBAC`")],
        size=15, after=5, h=4.50)
    concept(s, 0.60, 6.20, 6.70, "Concept only: the lab does not change the authorization mode.")
    code_box(s, 7.75, 1.65, 3.10, 0.80, "A request", "dev-user: get pods -n week13", STEPS[5], size=13)
    arrow(s, DOWN, 9.13, 2.50, 0.34, 0.34, fill=SLATE)
    box(s, 7.75, 2.90, 3.10, 0.90, "Node authorizer\nNo opinion: no kubelet", STEPS[0], size=13)
    arrow(s, DOWN, 9.13, 3.85, 0.34, 0.34, fill=SLATE)
    box(s, 7.75, 4.25, 3.10, 0.90, "RBAC authorizer\nDoes a binding allow it?", STEPS[3], size=13)
    arrow(s, RIGHT, 10.90, 4.52, 0.40, 0.36, fill=GREEN)
    box(s, 11.35, 4.25, 1.40, 0.90, "Yes:\nallow", GREEN, size=13)
    arrow(s, DOWN, 9.13, 5.20, 0.34, 0.34, fill=RED)
    box(s, 7.75, 5.60, 3.10, 0.90, "No authorizer allows it:\ndeny, 403 Forbidden", RED, size=13)
    mark(s, 9.55, 5.18, 1.80, 0.40, "No: no opinion", color=RED, align=PP_ALIGN.LEFT)
    return s


def s_objects(prs):
    """Slide 15 (L3, L-M2, L-S4). The table moves up to make room for the label."""
    s = new_slide(prs, "The Four RBAC Objects")
    bullets(s, 0.60, 1.62, 6.00, [
        (0, "A Role or a ClusterRole holds rules. Each rule sets `apiGroups`, `resources` and `verbs`"),
        (0, "A RoleBinding or a ClusterRoleBinding gives one role to subjects: users, groups or ServiceAccounts"),
        (0, "The request verbs: `get`, `list`, `watch`, `create`, `update`, `patch`, `delete` and `deletecollection`"),
        (0, "Rules only add permissions. RBAC has no deny rule")], size=15, after=6, h=2.20)
    end = grid(s, 0.60, 3.92, [1.25, 1.95, 2.90], [
        ["Scope", "What: the rules", "Who: the subjects"],
        ["One namespace", "Role `developer`", ["RoleBinding", "`devuser-developer-binding`"]],
        ["The whole cluster", "ClusterRole `pv-reader`", "ClusterRoleBinding `pv-test`"]], row_h=0.62, size=12.5)
    concept(s, 0.60, end + 0.08, 6.00, "Concept only: the lab does not write a rule with `watch`, `patch` or "
            "`deletecollection`. It does not use `update` or `configmaps` as `dev-user`, or show that RBAC has no "
            "deny rule.")
    zone_code(s, 6.85, 1.62, 5.90, 4.98, "Namespace `week13`", color=STEPS[1], fill=E.CARD_BG)
    code_box(s, 7.00, 2.10, 1.20, 0.95, "User", "dev-user", STEPS[5], size=12)
    arrow(s, RIGHT, 8.24, 2.40, 0.26, 0.36, fill=SLATE)
    code_box(s, 8.54, 2.10, 2.55, 0.95, "RoleBinding", "devuser-developer-binding", STEPS[3], size=12)
    arrow(s, RIGHT, 11.13, 2.40, 0.26, 0.36, fill=SLATE)
    code_box(s, 11.43, 2.10, 1.20, 0.95, "Role", "developer", STEPS[4], size=12)
    arrow(s, DOWN, 11.86, 3.12, 0.34, 0.42, fill=SLATE)
    mark(s, 7.00, 3.62, 4.80, 0.36, "The rules of the Role `developer`", align=PP_ALIGN.LEFT, size=13)
    for k, (res, verbs) in enumerate((("pods", "list, get, create, update"), ("configmaps", "create"))):
        y = 4.10 + k * 0.85
        code_box(s, 7.00, y, 2.00, 0.70, res, "", STEPS[0], size=13, mono_head=True)
        code_box(s, 9.10, y, 3.53, 0.70, verbs, "", STEPS[1], size=13, mono_head=True)
    mark(s, 7.00, 5.70, 5.63, 0.85, "No rule has the verb `delete`, so `dev-user` cannot delete a Pod. Least "
         "privilege: give each subject only the permissions that it needs", align=PP_ALIGN.LEFT, size=13)
    return s


def s_cluster(prs):
    """Slide 17 (L3, L-M5)."""
    s = new_slide(prs, "ClusterRoles and ClusterRoleBindings")
    bullets(s, 0.60, 1.62, 6.00, [
        (0, "A ClusterRole and a ClusterRoleBinding have no namespace. Use them for nodes, PersistentVolumes, "
            "paths such as `/readyz`, and the Pods of all namespaces"),
        (0, "A RoleBinding that names a ClusterRole gives the rules in its own namespace only"),
        (0, "`kubectl auth can-i` asks if a subject (`--as`) can do an action")],
        size=14, after=5, h=1.86)
    # The label is one line at the full width, between the boxes (they end at 3.53 in) and the terminal.
    rich(s, 0.60, 3.52, 12.15, 0.26, "Concept only: the lab does not put nodes or a path in a ClusterRole, or bind a "
         "ClusterRole for the Pods of all namespaces.", size=13, color=E.MUTED)
    for k, (kind, verdict, fill) in enumerate((("RoleBinding", "auth can-i: no", RED),
                                               ("ClusterRoleBinding", "auth can-i: yes", GREEN))):
        y = 1.65 + k * 1.02
        code_box(s, 6.85, y, 2.05, 0.86, kind, "pv-test", STEPS[3], size=12.5)
        arrow(s, RIGHT, 8.95, y + 0.25, 0.30, 0.36, fill=SLATE)
        code_box(s, 9.30, y, 1.60, 0.86, "ClusterRole", "pv-reader", STEPS[4], size=12.5)
        arrow(s, RIGHT, 10.95, y + 0.25, 0.30, 0.36, fill=fill)
        box(s, 11.30, y, 1.45, 0.86, verdict, fill, size=12)
    shell(s, 0.60, 3.78, 12.15, "Lab Week 13, Step 5",
          pick(5, "# A PersistentVolume has no namespace") +
          run(5, ("$ kubectl api-resources", API_RESOURCES), ("$ kubectl create clusterrole pv-reader", [])) +
          pick(5, "# A RoleBinding cannot") +
          run(5, ("$ kubectl create rolebinding pv-test", []),
              ("$ kubectl auth can-i list persistentvolumes -A --as=system:serviceaccount:week13:clo835   # n", ["no"])) +
          pick(5, "# A ClusterRoleBinding gives") +
          run(5, ("$ kubectl create clusterrolebinding pv-test", []),
              ("$ kubectl auth can-i list persistentvolumes -A --as=system:serviceaccount:week13:clo835   # y",
               ["yes"])), size=10.5)
    return s


def s_defaults(prs):
    """Slide 18 (L3)."""
    s = new_slide(prs, "The Default ClusterRoles and ClusterRoleBindings")
    end = grid(s, 0.60, 1.62, [2.95, 3.85, 5.30], [
        ["ClusterRole", "Default binding", "What it allows"],
        ["`cluster-admin`", "The group `system:masters`. kubeadm also binds `kubeadm:cluster-admins`",
         "Each verb on each object and each path"],
        ["`admin`", "None", "Read and write in a namespace, also Roles and RoleBindings"],
        ["`edit`", "None", "Read and write in a namespace, but not Roles or RoleBindings"],
        ["`view`", "None", "Read in a namespace, but not Secrets, Roles or RoleBindings"],
        ["`system:discovery`", "The group `system:authenticated`", "The discovery paths, for example `/api` and "
                                                                        "`/apis`"],
        ["`system:public-info-viewer`", "The groups `system:authenticated` and `system:unauthenticated`",
         "`/version`, `/livez`, `/readyz` and `/healthz` (deprecated since v1.16)"]], row_h=0.56, size=12.5)
    bullets(s, 0.60, end + 0.15, 12.10, [
        (0, "A member of `system:masters` bypasses RBAC and Webhook authorization. No binding can limit it"),
        (0, "In the lab, `kubectl` on the master runs as `kubernetes-admin`. The CSR of Step 1 shows it as the "
            "`REQUESTOR`")], size=14, after=4, h=0.75)
    concept(s, 0.60, 6.28, 12.10, "Concept only: the lab does not bind `admin` or `edit`, show `system:masters`, or "
            "read a health path.")
    return s


def s_sa(prs):
    """Slide 20 (L2, L3, L-M4, L-M6)."""
    s = new_slide(prs, "The ServiceAccount of a Pod")
    bullets(s, 0.60, 1.62, 6.40, [
        (0, "A ServiceAccount is an object in a namespace. Each namespace has the ServiceAccount `default`"),
        (0, "`serviceAccountName` names one ServiceAccount in the namespace of the Pod. With no name, the Pod gets "
            "`default`"),
        (0, "You set it when you create the Pod. You cannot change it in a Pod that exists"),
        (0, "The kubelet mounts a token of the ServiceAccount into the Pod. The Week 12 lecture shows this token "
            "volume"),
        (0, "Outside `kube-system`, a new ServiceAccount has only the permissions of every authenticated user, for "
            "example `kubectl auth whoami`")],
        size=15, after=8, h=4.05)
    concept(s, 0.60, 5.78, 6.40, "Concept only: the lab does not run `kubectl auth whoami` as a ServiceAccount. "
            "It does not change `serviceAccountName` or set it to a ServiceAccount of another namespace.")
    zone_code(s, 7.25, 1.62, 3.45, 4.33, "Namespace `week13`", color=STEPS[1], fill=E.CARD_BG)
    for x, pod, sa in ((7.42, "curl-sa", "clo835"), (9.12, "web", "default")):
        code_box(s, x, 2.10, 1.45, 0.80, "Pod", pod, STEPS[0], size=13)
        arrow(s, DOWN, x + 0.55, 2.96, 0.34, 0.82, fill=SLATE)
        code_box(s, x, 3.85, 1.45, 0.90, "ServiceAccount", sa, STEPS[5], size=12)
    rich(s, 7.42, 4.92, 3.15, 0.95, ["`curl-sa` names `clo835`.", "`web` names no ServiceAccount, so it gets "
                                     "`default`."], size=12.5, after=6)
    zone_code(s, 10.95, 1.62, 1.80, 4.33, "Namespace `default`", color=STEPS[1], fill=E.CARD_BG)
    arrow(s, RIGHT, 10.60, 2.32, 0.42, 0.36, fill=RED)
    mark(s, 11.05, 2.10, 1.60, 0.80, "Not possible: another namespace", color=RED)
    arrow(s, DOWN, 11.68, 2.95, 0.34, 0.85, fill=RED)
    code_box(s, 11.08, 3.85, 1.55, 0.90, "ServiceAccount", "default", STEPS[5], size=12)
    return s


def s_token(prs):
    """Slide 21 (L-S5)."""
    s = new_slide(prs, "A Pod Calls the API with Its Token")
    zone_code(s, 0.60, 1.62, 3.35, 2.35, "Pod `curl-sa` in `week13`", color=STEPS[1], fill=E.CARD_BG)
    code_box(s, 0.78, 2.02, 3.00, 1.75, "The token file",
             "/var/run/secrets/\nkubernetes.io/\nserviceaccount/token", STEPS[3], size=12)
    flow(s, 4.05, 2.10, 2.05, "1. Bearer token")
    flow(s, 4.05, 3.05, 2.05, "4. 403 Forbidden", fill=RED, kind=LEFT)
    zone_code(s, 6.20, 1.62, 6.55, 2.35, "API server: `kubernetes.default.svc`", color=STEPS[3], fill=E.CARD_BG)
    code_box(s, 6.35, 2.10, 3.70, 1.55, "2. Authentication: the user",
             "system:serviceaccount:week13:clo835", STEPS[0], size=12.5)
    arrow(s, RIGHT, 10.10, 2.70, 0.30, 0.36, fill=SLATE)
    code_box(s, 10.45, 2.10, 2.15, 1.55, "3. RBAC: no rule allows", "list services", STEPS[4], size=12.5)
    shell(s, 0.60, 4.15, 5.00, "curl-sa.yaml (Lab Week 13, Step 4)", V.FILES[4], size=11.5)
    bullets(s, 5.85, 4.20, 6.90, [
        (0, "`serviceAccountName: clo835` gives the Pod the ServiceAccount `clo835`"),
        (0, "`curl` sends the token in the header `Authorization: Bearer`"),
        (0, "`curl` verifies the API server with the file `ca.crt` in the directory of the token"),
        (0, "The token proves who the Pod is. RBAC then decides what it can do")], size=16, after=12, h=2.45)
    return s


def s_token_lab(prs):
    """Slide 22 (L-S7)."""
    s = new_slide(prs, "The API Call of the Pod curl-sa")
    y = shell(s, 0.60, 1.55, 12.15, "Lab Week 13, Step 4", run(
        4, ("$ kubectl create serviceaccount", ["serviceaccount/clo835 created"]),
        ("$ kubectl apply -f curl-sa.yaml", ["pod/curl-sa created"]),
        ("$ kubectl wait", ["pod/curl-sa condition met"])) + [""] +
        pick(4, "# Ask the API server") + run(4, ("$ kubectl exec curl-sa", FORBIDDEN_JSON)), size=9)
    bullets(s, 0.60, y + 0.10, 12.10, [
        (0, "The answer is a Status object with the reason Forbidden and the code 403. Its message names the user "
            "of the token: the ServiceAccount `clo835`"),
        (0, "The `curl` request is a GET of a collection, so RBAC checks the verb `list`. A GET of one object uses "
            "`get`, POST uses `create`, PUT uses `update`, PATCH uses `patch` and DELETE uses `delete`")],
        size=13, after=3, h=6.36 - y - 0.10)
    # A one-line label of the style of concept(), 0.30 in high, so that it stays above the footer band.
    rich(s, 0.60, 6.38, 12.10, 0.30, "Concept only: the lab does not send a PATCH request.", size=13, color=E.MUTED)
    return s


def s_methods(prs):
    """Slide 7 (round 2, L-S7: "verifies", the word of slide 5 for authentication)."""
    s = new_slide(prs, "Authentication Methods")
    rich(s, 0.60, 1.62, 12.10, 0.40, "The API server uses each method that it has. The first method that "
         "authenticates the request decides.", size=15)
    end = grid(s, 0.60, 2.10, [3.00, 6.30, 2.80], [
        ["Method", "The credential", "In the lab"],
        ["X.509 client certificate", "A certificate that the cluster CA signed", "Step 1: `dev-user`"],
        ["ServiceAccount token", "A short-lived token from the TokenRequest API, in the Pod", "Step 4: `curl-sa`"],
        ["Bootstrap token", "A token for a new node that joins the cluster with `kubeadm join`",
         "Step 0: `kubeadm join`"],
        ["Static token file", "A CSV file on the API server. A change needs a restart of the API server", "No"],
        ["OpenID Connect (OIDC) token", "An ID token from an OIDC identity provider", "No"],
        ["Webhook token", "An outside service verifies the token. Amazon EKS uses this method", "No"],
        ["Authenticating proxy", "A trusted proxy sets the user name in a request header", "No"]],
        row_h=0.50, size=13)
    concept(s, 0.60, end + 0.10, 12.10, "Concept only: the lab does not run the last four methods.")
    return s


def s_reader(prs):
    """Slide 23 (round 2, L-S4: a subject can be a ServiceAccount of another namespace)."""
    s = new_slide(prs, "A Role for the ServiceAccount")
    y = shell(s, 0.60, 1.55, 8.00, "Lab Week 13, Step 5",
              pick(5, "# The Role service-reader") +
              run(5, ("$ kubectl apply -f service-reader.yaml",
                      ["role.rbac.authorization.k8s.io/service-reader created",
                       "rolebinding.rbac.authorization.k8s.io/service-reader-binding created"])) + [""] +
              pick(5, "# The same call") + run(5, ("$ kubectl exec curl-sa", V.SERVICE_LIST)) + [""] +
              pick(5, "# A Role and its RoleBinding") +
              run(5, ("$ kubectl auth can-i list services", ["no"])), size=9.5)
    bullets(s, 0.60, y + 0.15, 8.00, [
        (0, "The subject of the RoleBinding is the ServiceAccount `clo835` of the namespace `week13`. A subject "
            "can also be a ServiceAccount of another namespace"),
        (0, "The token of `curl-sa` does not change. Only the new Role and RoleBinding change the answer")],
        size=14, after=4, h=6.65 - y - 0.15)
    y2 = shell(s, 8.85, 1.55, 3.90, "service-reader.yaml (Lab Week 13, Step 5)", V.FILES[5], size=10)
    concept(s, 8.85, y2 + 0.12, 3.90, "Concept only: the lab does not bind a ServiceAccount of another namespace.")
    return s


def s_creator(prs):
    """Slide 27 (round 2, L-S6: in the mode CONFIG_MAP, nobody can remove the creator access)."""
    s = new_slide(prs, "The IAM Identity That Created the Cluster")
    eks_label(s, EKS_SHORT)
    bullets(s, 0.60, 2.00, 6.00, [
        (0, "`bootstrapClusterCreatorAdminPermissions` (default `true`) gives admin permissions to the IAM identity that "
            "creates the cluster"),
        (0, "Modes `API` and `API_AND_CONFIG_MAP`: an access entry with `AmazonEKSClusterAdminPolicy`. You can "
            "see it and remove the policy"),
        (0, "Mode `CONFIG_MAP`: Amazon EKS puts the identity in `system:masters`. No visible configuration shows "
            "it, and you cannot remove it"),
        (0, "Record which identity created each cluster. AWS calls the removal of these admin permissions a best "
            "practice")], size=15, after=12, h=4.60)
    grid(s, 6.85, 2.00, [1.75, 2.50, 1.65], [
        ["Admin identity", "kubeadm (the lab)", "Amazon EKS"],
        ["An authorizer checks it", ["`kubernetes-admin` of `admin.conf`", "in `kubeadm:cluster-admins`"],
         "The creator, as an access entry"],
        [["In `system:masters`:", "no authorization check"], "The user of `super-admin.conf`",
         "The creator, in the mode `CONFIG_MAP`"]], row_h=1.35, size=12)
    return s


def s_takeaways(prs):
    """Slide 30 (round 2, L-S7: "user", the word of slide 5)."""
    return text_slide(prs, "Key Takeaways", [
        (0, "Authentication finds who sends a request. Authorization decides what this user can do"),
        (0, "The CN of a client certificate is the user name, and each O field is a group"),
        (0, "A Pod proves its identity with the token of its ServiceAccount"),
        (0, "A Role says what, and a RoleBinding says who"),
        (0, "An object with no namespace, such as a PersistentVolume, needs a ClusterRole and a ClusterRoleBinding"),
        (0, "On Amazon EKS, AWS recommends the access entry. AWS marks the `aws-auth` ConfigMap as deprecated")],
        size=17, after=11)


def s_anonymous(prs):
    """Slide 11 (round 3, L-S2, C4: the sample shows the line "details": {} of the live output)."""
    s = new_slide(prs, "Requests With and Without Credentials")
    bullets(s, 0.60, 1.62, 12.10, [
        (0, "A request with no credentials gets the user `system:anonymous` and the group `system:unauthenticated`"),
        (0, "The ClusterRole `system:public-info-viewer` allows this user to read some paths, for example "
            "`/version`"),
        (0, "No authorizer allows this user to read `/apis`, so the API server answers 403 Forbidden"),
        (0, "`kubectl proxy` listens on `127.0.0.1:8001`. It sends each request to the API server with your "
            "credentials")], size=15, after=5, h=1.60)
    shell(s, 0.60, 3.30, 12.15, "Lab Week 13, Step 2",
          pick(2, "$ curl -k https://localhost:6443/version") +
          ['# JSON with the version of the cluster, for example "gitVersion": "v1.35.10".'] +
          run(2, ("$ curl -k https://localhost:6443/apis",
                  [r'  "message": "forbidden: User \"system:anonymous\" cannot get path \"/apis\"",',
                   '  "reason": "Forbidden",', '  "details": {},', '  "code": 403'])) +
          run(2, ("$ kubectl proxy", ["Starting to serve on 127.0.0.1:8001", "{", '  "kind": "APIGroupList",',
                                      '  "apiVersion": "v1",', '  "groups": ['])) +
          pick(2, "# kill %1 stops the proxy"), size=12)
    return s


def s_role_lab(prs):
    """Slide 16 (round 3, L-M1, B7: slide 17 states the namespace scope of a RoleBinding; this bullet does not)."""
    s = new_slide(prs, "The Role developer and Its RoleBinding")
    y = shell(s, 0.60, 1.55, 8.15, "Lab Week 13, Step 3",
              pick(3, "# RBAC matches") +
              run(3, ("$ kubectl apply -f developer-role.yaml",
                      ["role.rbac.authorization.k8s.io/developer created",
                       "rolebinding.rbac.authorization.k8s.io/devuser-developer-binding created"])) + [""] +
              run(3, ("$ kubectl --context=dev-user@kubernetes run web", []),
                  ("$ kubectl --context=dev-user@kubernetes delete pod web",
                   ['Error from server (Forbidden): pods "web" is forbidden: User "dev-user" cannot delete ...'])) +
              [""] + pick(3, "# The group of the certificate") +
              run(3, ("$ kubectl create rolebinding developers-view",
                      ["rolebinding.rbac.authorization.k8s.io/developers-view created"]),
                  ("$ kubectl --context=dev-user@kubernetes get services", ["No resources found in week13 namespace."])),
              size=10)
    bullets(s, 0.60, y + 0.20, 8.15, [
        (0, "`devuser-developer-binding` gives the Role `developer` to the user `dev-user`"),
        (0, "`dev-user` is in the group `developers`. The RoleBinding `developers-view` gives this group the "
            "ClusterRole `view`, so `dev-user` can list the Services")], size=14, after=6, h=6.65 - y - 0.20)
    shell(s, 8.95, 1.55, 3.80, "developer-role.yaml (Lab Week 13, Step 3)", V.FILES[3], size=10)
    return s


V.QUAL31 = ("the configuration of admission control", "a change of the authorization mode", "RBAC with no deny rule",
            "a rule that you write with `watch`, `patch` or `deletecollection`",
            "A command of `dev-user` that uses `update` or `configmaps`", "nodes or a path in a ClusterRole",
            "a `serviceAccountName` of another namespace or a change of this field",
            "`kubectl auth whoami` as a ServiceAccount", "the discovery path `/api`")


def check_note31(lines):
    """check_note31() of v9, with one change of round 2 (L-S4): a phrase that names a ServiceAccount and a
    namespace must name the field serviceAccountName, a Pod or a RoleBinding."""
    for line in lines:
        for phrase in re.split(r", |: ", line):
            if re.search("serviceaccount", phrase, re.IGNORECASE) and "namespace" in phrase.lower():
                assert "`serviceAccountName`" in phrase or "Pod" in phrase or "RoleBinding" in phrase, phrase
    text = " ".join(lines)
    for phrase in V.QUAL31:
        assert text.count(phrase) == 1, phrase
        text = text.replace(phrase, "")
    names = set(re.findall(r"`([^`]+)`", text)) & V.USED31
    terms = [t for t in V.TERMS31 if re.search(r"\b" + re.escape(t), text, re.IGNORECASE)]
    assert not names and not terms, (names, terms)


def f(name):
    """The slide function with this name in V.SLIDES (the v10 function when v10 replaces it)."""
    return next(m for m in V.SLIDES if m.__name__ == name)


def nos(*names):
    return V.nos(*(f(n) for n in names))


def s_lab(prs):
    """Slide 31 (L4, L-M2, L-M3, L-S2): the map of v9, and one list with one line for each part."""
    s = new_slide(prs, "Lab Week 13 at a Glance")
    rows = [
        ["Lab step", "What you do", "Lecture slides"],
        ["Step 0", "Build and check the cluster.", nos("s_methods", "s_summary")],
        ["Step 1", "Create the certificate of `dev-user`. Approve its CSR.",
         nos("s_clients", "s_methods", "s_certificate", "s_certificate_lab", "s_api", "s_defaults")],
        ["Step 2", "Send requests with no credentials and through `kubectl proxy`. Authenticate as `dev-user`.",
         nos("s_path", "s_clients", "s_methods", "s_certificate", "s_certificate_lab", "s_api", "s_anonymous",
             "s_whoami", "s_modes", "s_defaults", "s_token")],
        ["Step 3", "Create the Role `developer` and its RoleBinding. Bind the group `developers` to the ClusterRole "
                   "`view`.", nos("s_path", "s_clients", "s_certificate", "s_api", "s_whoami", "s_modes",
                                  "s_objects", "s_role_lab", "s_cluster", "s_defaults", "s_sa", "s_summary")],
        ["Step 4", "Call the API from the Pod `curl-sa` with the token of `clo835`.",
         nos("s_path", "s_clients", "s_methods", "s_api", "s_modes", "s_sa", "s_token", "s_token_lab", "s_reader")],
        ["Step 5", "Give `clo835` the Role `service-reader`. Test `pv-reader` with a RoleBinding and a "
                   "ClusterRoleBinding.", nos("s_clients", "s_api", "s_modes", "s_objects", "s_cluster", "s_token",
                                              "s_token_lab", "s_reader", "s_summary")],
        ["Step 6", "Destroy the cluster.", "–"]]
    found = {int(r[0][-1]): r[2] for r in rows[1:7]}
    assert found == V.MAP31, (found, V.MAP31)
    end = grid(s, 0.60, TOP + 0.08, [0.90, 8.05, 3.15], rows, row_h=0.36, size=13)
    note = [
        "Not in the lab. Part 1: the configuration of admission control, the answer 401, and the rule for the prefix "
        "`system:`. The groups of a ServiceAccount, and the four other authentication methods. The minimum lifetime "
        "and the revocation of a certificate, and the discovery path `/api`.",
        "Part 2: a change of the authorization mode, RBAC with no deny rule, and a rule that you write with "
        "`watch`, `patch` or `deletecollection`. A command of `dev-user` that uses `update` or `configmaps`, nodes "
        "or a path in a ClusterRole, and a ClusterRoleBinding for the Pods of all namespaces. The paths `/livez`, `/readyz` and `/healthz`, the "
        "ClusterRoles `admin` and `edit`, and the group `system:masters`.",
        "Part 3: a `serviceAccountName` of another namespace or a change of this field, and `kubectl auth whoami` "
        "as a ServiceAccount. A PATCH request, and a RoleBinding for a ServiceAccount of another namespace.",
        "Part 4: Amazon EKS. Slides %d and %d: the cells with no step number, and the optional topics."
        % (nos("s_summary"), nos("s_optional"))]
    check_note31(note)
    rich(s, 0.60, end + 0.10, 12.10, 6.68 - end - 0.10, note, size=12, color=E.MUTED, after=2)
    return s


NEW = {m.__name__: m for m in (s_path, s_clients, s_methods, s_certificate, s_certificate_lab, s_api, s_anonymous,
                               s_whoami, s_modes, s_objects, s_role_lab, s_cluster, s_defaults, s_sa, s_token,
                               s_token_lab, s_reader, s_creator, s_takeaways, s_lab)}
V.SLIDES = [NEW.get(m.__name__, m) for m in V.SLIDES]
assert sum(1 for m in V.SLIDES if m in NEW.values()) == len(NEW) == 20 and len(V.SLIDES) == 29


if __name__ == "__main__":
    V.main()
