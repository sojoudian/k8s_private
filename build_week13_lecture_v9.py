# -*- coding: utf-8 -*-
"""CLO835 Week 13 lecture v9 - Authentication, RBAC and EKS.

v9 applies CLO835_STANDARDS.md v1.2 to lecture v8, with the method of the model build_week12_lecture_v7.py.
v8 stays on disk. Each finding of the review round 1 of 2026-11-11 (scratchpad w13review/round1.md) and its fix:

Structure
- M1 (required slides): four part dividers, Summary, Optional Topics, Key Takeaways and "Lab Week 13 at a
  Glance" (with the full "Not in the lab" note) are new.
- M2 (bullet on two slides): each diagram label and each bullet has its own text. The EKS label of B7 is a
  one-line label (0.30 in), not a bullet.
- M3 (banned words): no "resource" and no "entries" in Calibri text; the references are Consolas lines.
- M4 (cover): the kit cover() at 34 pt, "Authentication," / "RBAC and EKS", no subtitle, no "K8s".
- M5 (Course Outline): outline_week13() changes "K8s" to "Kubernetes", 10.5 pt to 12 pt, and moves the right
  tiles 0.08 in to the left, as the kit outline() does. v8 already shows Week 13 in the blue tile.
- M6 (agenda): noun phrases, no -ing form.
- M7 (titles): "Requests With and Without Credentials"; "The Access Entry and the aws-auth ConfigMap".
- M8 (bullet glyph): the kit bullets() writes the glyph and a tab, with the hanging indent.
- M18 (builder): VERSION, the __main__ guard and the overwrite guard (--force).
Language and facts
- M9 ("turn on"): "kubeadm sets Node,RBAC" (slide Authorization Modes).
- M10 (/healthz): "/healthz (deprecated since v1.16)" on the slide API Groups and Paths.
- M11 (endpoints): the core group tiles show serviceaccounts, not endpoints.
- M12 (webhook): "an outside service allows, denies or has no opinion"; the first allow or deny decides.
- M13 (sample output): each sample output line is a "# " comment, from the live log of 2026-11-11.
- M14 (other objects): the Step 5 terminal holds the lab lines of Step 5 only (week13:clo835, no delete).
- M15 (manifest): each file panel is the lab file (lab.SLIDES), with no added line.
- M16 ("Concept only"): each concept that the lab does not run has the label of B7.
- M17 (dev.to): gone. The references are v1-35.docs.kubernetes.io and docs.aws.amazon.com pages.
- M37 (terminal label): each lab terminal is "Lab Week 13, Step N" and takes its lines from the lab with
  pick()/run(); the kubectl proxy line is the one tested line of the lab.
SHOULD-FIX
- S1 (repetition): the authentication methods are on one slide; the authorization modes on one slide; the
  default AlwaysAllow one time; one EKS diagram. Each point is stated at most two times (the takeaways
  included). The idea of the v8 table "Why Authorization" (admins, developers, bots) is now the Summary
  table with the lab users kubernetes-admin, dev-user and clo835.
- S2: the modes list has AlwaysAllow and AlwaysDeny. S3: "stable in v1.8" (RBAC), "stable in v1.28" (whoami).
- S4: the methods table names each kind of bearer token. S5: "$ kubectl certificate approve dev-user", and
  "openssl genrsa, openssl req". S6: expirationSeconds 86400 = 24 hours, minimum 600, no revocation.
- S7: the groups are one table with the client types. S8: one bullet says what the API diagram shows.
- S9: no -ing form; "stable in v1.8". S10: the lab names (developer, dev-user, developers).
- S11: api-resources with persistentvolumes, as in the lab. S12: "kubectl apply -f developer-role.yaml -n week13".
- S13: each lab terminal and file panel names its lab step. S14: curl-sa and service-reader are on slides.
- S15: code names in Consolas (backticks, zone_code, code_box). S16: the EKS diagram shows the webhook (the AWS
  IAM Authenticator), the signed STS URL and the EKS authorizer. S17: admission control acts on writes only.
- S18: "Outside kube-system, a new ServiceAccount has only the API discovery permissions".
- S31: v1-35.docs.kubernetes.io links, also the authorization page.
- S32: the public paths are on the API slide only. The request slide names /version as an example.
- S33: the prompt of 2026-11-11 sets SRC = Lecture_week13_v8.pptx. cover(), agenda() and outline_week13() give
  the result of Week 12 v7 (34 pt, Kubernetes, 12 pt).
After review round 2 (scratchpad w13review2/round2_decks.md), and the classes of Week 12 rounds 5 to 7:
- MUST-FIX 9: each note line of slide 31 has 25 words or fewer to its full stop (six lines now).
- MUST-FIX 10: the Step 2 cell of slide 31 is one line. Each cell is a full sentence with one instruction and a
  full stop ("Create the certificate of dev-user. Approve its CSR.").
- MUST-FIX 11: slide 5 "Concept only: the lab does not configure or show admission control."
- MUST-FIX 12: the bootstrap token row of slide 7 says "Step 0: kubeadm join"; "the last four methods"; the
  slide 31 note says "the four other authentication methods".
- MUST-FIX 13: slide 6 "Kubernetes reserves the prefix system: for its own names" (active voice).
- SHOULD-FIX 5: slide 31 lists slide 5 for Step 2, slides 6 and 7 for Step 1, and slide 7 for Step 4 (the lab
  worker moved the Explain item of the three phases to section 3 of the Blackboard text).
- SHOULD-FIX 6: slide 15 pairs the Role developer with the RoleBinding devuser-developer-binding.
- SHOULD-FIX 7: slide 9 names the lab command cat > dev-user-csr.yaml <<EOF.
- SHOULD-FIX 8: the public paths are listed on slide 18 only (with /healthz deprecated since v1.16).
- SHOULD-FIX 9: the divider subtitles name the content, not the point.
- SHOULD-FIX 10: slide 17 "--as names the subject" (impersonate is an optional topic).
- SHOULD-FIX 11: the fields apiGroups, resources and verbs are in Consolas (slides 10 and 15).
After review round 3 (scratchpad w13review3/round3_decks.md):
- MUST-FIX 5: no "RBAC denies" (RBAC has no deny rule). Slide 11: "No authorizer allows a request for another
  path, so the API server answers 403 Forbidden"; slide 12: "so the API server denies get pods". Slide 11 now
  names the ClusterRole system:public-info-viewer, so "the public paths" has a definition (note of the report).
- MUST-FIX 6: slide 30 "AWS marks the aws-auth ConfigMap as deprecated" (active voice).
- SHOULD-FIX 1, 2: slide 31 note lines 4 to 6 name only topics that the lab does not practise.
- SHOULD-FIX 3: slide 31 lists slide 18 for Step 1 and slide 28 for Steps 3 and 5. Slide 14 shows the Step 2
  request (dev-user, get pods in week13), so the Step 2 row lists slide 14 (note of the report).
- SHOULD-FIX 4: the arrow 5 of slide 25 is an UP_ARROW. The arrow from the computer carries step 2 only, so
  its label is "2" (note of the report: step 1 runs on the computer).
- SHOULD-FIX 5: the aws-auth terminal title is "aws-auth (example only)".
- SHOULD-FIX 6: "Students have no EKS." is on slide 25 only.
After review round 4 (scratchpad w13review4/round4_decks.md):
- MUST-FIX 1: kubeadm allows system:unauthenticated to read the ConfigMap cluster-info in kube-public, so slide
  11 no longer says "only" or "another path": "The ClusterRole system:public-info-viewer allows this user to read
  some paths, for example /version" and "No authorizer allows this user to read /apis, so the API server answers 403
  Forbidden".
- SHOULD-FIX 1: the lab shows the effect of system:public-info-viewer (Step 2, /version), so slide 31 note line 5
  does not name it.
- SHOULD-FIX 2: slide 31 lists slide 10 for Step 3, slide 6 for Step 4 and slide 15 for Step 5.
- SHOULD-FIX 3: slide 28, kubernetes-admin and get nodes: "Allowed (Step 0)" (lab Step 0, kubectl get nodes -o wide).
After review round 5 (scratchpad w13review5/round5_decks.md):
- SHOULD-FIX 1 to 3: slide 31 has a row Step 0 ("Build and check the cluster.", slides 7 and 28) with rows of
  0.36 in, and lists slide 18 for Step 2, slides 6 and 10 for Steps 3 to 5.
- SHOULD-FIX 4: "allow" is the one word for a permission (slide 11); slide 21 says "allows curl to verify".
  Slide 23 takes the new lab comment "The Role service-reader allows ..." from the lab.
After review round 6 (scratchpad w13review6/round6_decks.md):
- SHOULD-FIX 1: "allow" stays the word for a permission only. Slide 21: "curl verifies the API server with the
  file ca.crt in this directory".
- SHOULD-FIX 2, 3: slide 31 lists slide 10 for Step 1, slide 17 for Step 3 and slide 14 for Step 4.
- Owner note: slide 12 uses the form of the lab comment: "No Role allows dev-user to list Pods yet, so the API
  server denies get pods".
After review round 7 (scratchpad w13review7/round7_decks.md):
- SHOULD-FIX 1, 2: slide 14 for Step 5 and slide 5 for Step 4. Then one complete pass over each pair (lab step 0
  to 6, slide 5 to 29) set every row of slide 31 (MAP31; table scratchpad w13/slide31_map.md). The column
  "Lecture slides" is 3.00 in wide, so each row stays on one line at 13 pt.
- SHOULD-FIX 3: slide 5 "The API server answers 401 Unauthorized when it cannot verify the credentials. It answers
  403 Forbidden to a denied action" ("give" stays the word for a permission).
After review round 8 (scratchpad w13review8/round8_decks.md):
- SHOULD-FIX 1 (the decision of the coordinator): the admin rule of slide 18 does not count for "states the rule",
  so slide 18 left the rows of Steps 0, 4 and 5. Note lines 3 and 5 stay true. The Step 2 row lists slide 18 for
  the row system:discovery (the kubectl proxy request passes), so note line 5 no longer names system:discovery
  (the same class as system:public-info-viewer in round 4).
- SHOULD-FIX 2 to 4: slide 21 and slide 9 for Step 2, slide 12 for Step 3 (MAP31). The columns of slide 31 are
  0.90, 8.05 and 3.15 in, so each row stays on one line at 13 pt.

After review round 9 (scratchpad w13review9/round9_decks.md). The class: a note line of slide 31 names a topic
that the evidence of a listed pair uses.
- SHOULD-FIX 1 (method A, the map stays): note line 5 names "a ServiceAccount of another namespace" (the box
  "Not possible: another namespace" of slide 20), not the ServiceAccount default of (3, 20) B.
- SHOULD-FIX 2: note line 2 no longer names system:unauthenticated, the D evidence of (2, 18).
- SHOULD-FIX 3: note line 4 says "nodes in a ClusterRole"; paths in a ClusterRole are the evidence of (2, 11)
  and (2, 18).
- SHOULD-FIX 4: note line 3 says "a change of the authorization mode" (the words of the slide 14 label).
- The check of each note topic against the evidence of each listed pair (w13/note31_check.py) found one more
  case: (2, 5) C uses the three phases, and the third phase is admission control. Note line 1 now says "the
  configuration of admission control" (the words of the slide 5 label). For the limit of 25 words, the answer
  401 moved to the start of note line 2.
- check_note31() asserts the check for each build: no code name of the evidence (USED31) and no plain term of
  TERMS31 is in the note, except in a phrase of QUAL31.

After review round 10 (scratchpad w13review10/round10_decks.md):
- SHOULD-FIX 1: "a ServiceAccount of another namespace" (note line 5) also reads as the test of Step 5 (clo835 of
  week13 in the namespace default, the evidence of (5, 14), (5, 23) and (5, 28)). Line 5 now names the Pod field:
  "a serviceAccountName of another namespace or a change of this field". QUAL31 has this phrase.
- check_note31() also checks plain text: a note phrase that names a ServiceAccount and a namespace must name the
  field serviceAccountName or a Pod.
Not changed: the lab (build_week13_lab_v5.py is the single source of each lab line), Week 12, the kit, the gate.

Input : week13/Lecture_week13_v8.pptx, for the cover, the agenda and the outline (read, never written)
Output: week13/Lecture_week13_v9.pptx (the build refuses to overwrite it without --force)

Run from the project root. It is guarded, so importing it writes nothing.
    .venv/bin/python build_week13_lecture_v9.py
"""
import os
import re
import sys

from pptx import Presentation
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

import build_week08 as E
import build_week13_lab_v5 as lab
from build_week07_lecture_v7 import (BLUE, DOWN, LEFT, RIGHT, SLATE, STEPS, TOP, UP, agenda, arrow, box, bullets,
                                     cover, flow, grid, keep_first, new_slide, number_and_save, rich, runs, term,
                                     text_slide, zone)

VERSION = "v9"
SRC = "week13/Lecture_week13_v8.pptx"
OUT = "week13/Lecture_week13_%s.pptx" % VERSION
TITLE = "CLO835 Week 13 Lecture: Authentication, RBAC and EKS"
GREEN, RED = E.GOAL_GREEN, E.ALERT_RED

# ---------------------------------------------------------------- the lab, as the single source of each command
LAB = {n: lab.SLIDES[2 + n][3] for n in range(1, 6)}               # Step 1 to Step 5 of Lab_week13_v5
FILES = {n: lab.SLIDES[2 + n][6] for n in (1, 3, 4, 5)}            # the manifest of each two-panel step
assert [lab.SLIDES[2 + n][1] for n in range(1, 6)] == [
    "A new user is a signed certificate", "Authenticated, not authorized", "A Role and a RoleBinding for dev-user",
    "A Pod calls the API with its token", "A Role and a ClusterRole for the ServiceAccount"]


def pick(step, *starts):
    """The lines of lab step `step` that start with one of `starts`, with their continuation lines."""
    lines, out, k = LAB[step], [], 0
    while k < len(lines):
        line = lines[k]
        if any(line.startswith(st) for st in starts):
            out.append(line)
            while line.rstrip().endswith("\\"):
                k += 1
                line = lines[k]
                out.append(line)
        k += 1
    missing = [st for st in starts if not any(l.startswith(st) for l in out)]
    assert not missing, (step, missing)
    return out


def run(step, *pairs):
    """Each lab command (found by its start) followed by its live output as comment lines (B5)."""
    out = []
    for start, output in pairs:
        found = pick(step, start)
        assert sum(1 for l in found if l.startswith("$")) == 1, (step, start, found)
        out += found + ["# " + o for o in output]
    return out


# The live output of the lab commands (Kubernetes v1.35.10, 2026-11-11, scratchpad w13/peerlive/pass.log).
CSR_TABLE = ["NAME       AGE   SIGNERNAME                            REQUESTOR          REQUESTEDDURATION   CONDITION",
             "dev-user   1s    kubernetes.io/kube-apiserver-client   kubernetes-admin   24h                 Approved,Issued"]
WHOAMI = ["ATTRIBUTE                                           VALUE",
          "Username                                            dev-user",
          "Groups                                              [developers system:authenticated]",
          "Extra: authentication.kubernetes.io/credential-id   [X509SHA256=61385367aa35815e69c7c4c262c6c551ff7ccdaff62d2de"
          "78f500a9fef5d7d6f]"]
FORBIDDEN_JSON = [
    "{",
    '  "kind": "Status",',
    '  "apiVersion": "v1",',
    '  "metadata": {},',
    '  "status": "Failure",',
    r'  "message": "services is forbidden: User \"system:serviceaccount:week13:clo835\" cannot list resource '
    r'\"services\" in API group \"\" in the namespace \"week13\"",',
    '  "reason": "Forbidden",',
    '  "details": {',
    '    "kind": "services"',
    "  },",
    '  "code": 403',
    "}"]
SERVICE_LIST = ["{", '  "kind": "ServiceList",', '  "apiVersion": "v1",', '  "metadata": {', '    "resourceVersion": "670"',
                "  },", '  "items": []', "}"]
API_RESOURCES = ["NAME                                SHORTNAMES   APIVERSION                        NAMESPACED   KIND",
                 "persistentvolumes                   pv           v1                                false        "
                 "PersistentVolume"]

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

EKS = "Concept only: the lab does not use Amazon EKS. Students have no EKS."
EKS_SHORT = "Concept only: the lab does not use Amazon EKS."
MONO_EM = 0.5498                                                     # the width of one Consolas character, in em


# ---------------------------------------------------------------- the helpers of the model, and two more

def divider(prs, kicker, text, subtitle):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    E.divider(s, kicker, text, subtitle)
    return s


def zone_code(s, x, y, w, h, label, color=SLATE, fill=E.WHITE):
    """zone() of the kit, but backticks in the label mark a code name in Consolas (B3)."""
    E.add_rounded_rect(s, E.Inches(x), E.Inches(y), E.Inches(w), E.Inches(h), fill, line=color, line_width=1.25,
                       radius_ratio=0.03)
    tb = s.shapes.add_textbox(E.Inches(x + 0.14), E.Inches(y + 0.07), E.Inches(w - 0.28), E.Inches(0.3))
    frame = tb.text_frame
    frame.margin_left = frame.margin_right = frame.margin_top = frame.margin_bottom = 0
    runs(frame.paragraphs[0], label, 12, color=color, bold=True, code_color=color)


def code_box(s, x, y, w, h, head, code, fill, size=13, mono_head=False):
    """A box with a heading in Calibri and code lines in Consolas (white on the fill color).
    mono_head=True: the heading is a code name too (B3), so it is in Consolas."""
    E.add_rounded_rect(s, E.Inches(x), E.Inches(y), E.Inches(w), E.Inches(h), fill, radius_ratio=0.10)
    lines = [head] + (code.split("\n") if code else [])
    tb = E.add_text(s, E.Inches(x + 0.08), E.Inches(y), E.Inches(w - 0.16), E.Inches(h), lines, size=size,
                    bold=True, color=E.WHITE, align=E.CENTER, anchor=E.MIDDLE, line_spacing=1.05)
    for p in tb.text_frame.paragraphs[1:]:
        for r in p.runs:
            r.font.name = E.FONT_MONO
            r.font.bold = False
    if mono_head:
        for r in tb.text_frame.paragraphs[0].runs:
            r.font.name = E.FONT_MONO


def concept(s, x, y, w, text):
    """The label of B7 for a concept that the lab does not run."""
    rich(s, x, y, w, 0.45, text, size=13, color=E.MUTED)


def eks_label(s, text=EKS):
    """The label of each Amazon EKS slide. It is a label, not a bullet. Review round 3: only slide 25 also says
    "Students have no EKS.", so that point is on one slide."""
    rich(s, 0.60, 1.55, 12.10, 0.30, text, size=13, color=E.MUTED)


def mark(s, x, y, w, h, text, color=SLATE, align=PP_ALIGN.CENTER, size=12):
    """A bold diagram label (12 pt or more, B3). Backticks mark code."""
    rich(s, x, y, w, h, text, size=size, color=color, align=align, anchor=MSO_ANCHOR.MIDDLE, bold=True, spacing=1.0)


def shell(s, x, y, w, bar, lines, size=10, spacing=1.0, h=None):
    """term() of the kit, after a check that the longest line fits the box (B5: no wrapped terminal line)."""
    widest = max(len(l) for l in lines) * size * MONO_EM / 72
    assert widest <= w - 0.38, (bar, round(widest, 2), w - 0.38, max(lines, key=len))
    return term(s, x, y, w, bar, lines, size=size, spacing=spacing, h=h)


def verdict_grid(s, x, y, widths, head, rows, row_h=0.58, head_h=0.50, size=13):
    """A house table: Allowed in green, Forbidden in red; code in the header is white Consolas."""
    yy = y
    for r, row in enumerate([head] + rows):
        high = head_h if r == 0 else row_h
        xx = x
        for c, (cell, cw) in enumerate(zip(row, widths)):
            fill = SLATE if r == 0 else (E.CARD_BG if r % 2 else E.WHITE)
            E.add_rect(s, Inches(xx), Inches(yy), Inches(cw), Inches(high), fill, line=E.RULE_GRAY, line_width=0.75)
            tb = s.shapes.add_textbox(Inches(xx + 0.10), Inches(yy), Inches(cw - 0.20), Inches(high))
            frame = tb.text_frame
            frame.margin_left = frame.margin_right = frame.margin_top = frame.margin_bottom = 0
            frame.word_wrap = True
            frame.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = frame.paragraphs[0]
            p.alignment = PP_ALIGN.LEFT if c == 0 else PP_ALIGN.CENTER
            if r == 0:
                runs(p, cell, size, color=E.WHITE, bold=True, code_color=E.WHITE)
            elif c == 0:
                runs(p, cell, size)
            else:
                word, _, rest = cell.partition(" ")
                runs(p, word, size, color=GREEN if word == "Allowed" else RED, bold=True)
                if rest:
                    runs(p, " " + rest, size)
            xx += cw
        yy += high
    return yy


def outline_week13(prs):
    """The Course Outline. v8 already shows Week 13 in the blue tile, so only the other changes of the kit
    outline() apply: Kubernetes, not K8s; 12 pt, not 10.5 pt; the right tiles 0.08 in to the left."""
    s = prs.slides[2]
    for sh in s.shapes:
        if sh.has_text_frame:
            for p in sh.text_frame.paragraphs:
                for r in p.runs:
                    r.text = r.text.replace("K8s – ", "Kubernetes – ").replace("K8s ", "Kubernetes ")
                    if r.font.size and r.font.size.pt == 10.5:
                        r.font.size = Pt(12)            # the body text minimum, also on the outline
    for sh in s.shapes:                                 # the right tiles ended at 12.91 in, past the footer rule
        if Inches(1.5) < sh.top < Inches(6.7) and sh.shape_type != 13:
            sh.left = sh.left - Inches(0.08)
    texts = {sh.text_frame.text: sh for sh in s.shapes if sh.has_text_frame}
    tile = texts["Week 13: Kubernetes – RBAC and EKS"]
    frame = [sh for sh in s.shapes if sh.shape_type == 1 and sh.top == tile.top
             and abs(sh.left - (tile.left - Inches(0.16))) < Inches(0.02)][0]
    assert str(frame.fill.fore_color.rgb) == "1FA8E0", frame.fill.fore_color.rgb
    assert not any("K8s" in t for t in texts), [t for t in texts if "K8s" in t]


def agenda_week13(prs, items):
    """agenda() of the kit removes the shape "TextBox 3". In v8 the agenda box has another name."""
    old = [sh for sh in prs.slides[1].shapes if sh.has_text_frame and sh.text_frame.text.startswith("▪")]
    assert len(old) == 1, len(old)
    old[0].name = "TextBox 3"
    agenda(prs, items)


# ---------------------------------------------------------------- Part 1: authentication

def s_part1(prs):
    return divider(prs, "Part 1", "Authentication", "Users, groups, certificates and tokens")


def s_path(prs):
    s = new_slide(prs, "The Path of a Request to the API Server")
    bullets(s, 0.60, 1.65, 6.20, [
        (0, "Each request to the API server has three phases, in this order:"),
        (1, "Authentication finds the user name and the groups of the client"),
        (1, "Authorization decides if this user can do this action on this object"),
        (1, "Admission control can change or reject a request that creates, changes or deletes an object. It does "
            "not act on a read"),
        (0, "The API server answers 401 Unauthorized when it cannot verify the credentials. It answers 403 "
            "Forbidden to a denied action"),
        (0, "After the three phases, the API server stores the object in etcd")], size=16, after=11, h=4.30)
    concept(s, 0.60, 6.20, 6.20, "Concept only: the lab does not configure or show admission control.")
    code_box(s, 7.05, 3.30, 1.40, 1.00, "Client", "kubectl", STEPS[5], size=13)
    arrow(s, RIGHT, 8.50, 3.62, 0.38, 0.38)
    zone(s, 8.95, 1.65, 2.55, 4.55, "API server", color=STEPS[1], fill=E.CARD_BG)
    for k, (text, fill) in enumerate((("1. Authentication\nWho are you?", STEPS[0]),
                                      ("2. Authorization\nCan you do this?", STEPS[3]),
                                      ("3. Admission control\nWrite requests only", STEPS[4]))):
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
        (0, "Kubernetes stores no users and no groups. The API server finds them in the credentials of each request"),
        (0, "Bind a role to a group, not to each user. Kubernetes reserves the prefix `system:` for its own names")],
        size=15, after=6, h=0.85)
    concept(s, 0.60, 6.20, 12.10, "Concept only: the lab does not show the groups of `clo835` or the group "
            "`system:unauthenticated`.")
    return s


def s_methods(prs):
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
        ["Webhook token", "An outside service checks the token. Amazon EKS uses this method", "No"],
        ["Authenticating proxy", "A trusted proxy sets the user name in a request header", "No"]],
        row_h=0.50, size=13)
    concept(s, 0.60, end + 0.10, 12.10, "Concept only: the lab does not run the last four methods.")
    return s


def s_certificate(prs):
    s = new_slide(prs, "A Client Certificate Is a User")
    bullets(s, 0.60, 1.65, 7.00, [
        (0, "Kubernetes trusts each client certificate that the cluster CA signed"),
        (0, "The common name (CN) is the user name. Each organization (O) field is a group"),
        (0, "The signer `kubernetes.io/kube-apiserver-client` signs only after an approval. No controller approves "
            "it automatically"),
        (0, "`expirationSeconds: 86400` asks for 24 hours. The minimum is 600 seconds (ten minutes)"),
        (0, "Kubernetes v1.35 cannot revoke a certificate: it is valid until it expires. A short lifetime limits "
            "the risk of a lost key")], size=17, after=14, h=4.95)
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
    s = new_slide(prs, "The Certificate of dev-user")
    shell(s, 0.60, 1.55, 5.30, "dev-user-csr.yaml (Lab Week 13, Step 1)", FILES[1], size=10.5)
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
        ("$ kubectl get csr dev-user  ", CSR_TABLE),
        ("$ kubectl get csr dev-user -o", []),
        ("$ openssl x509", ["subject=O=developers, CN=dev-user", "notAfter=Nov 12 05:27:22 2026 GMT"])),
        size=9.5)
    return s


def s_api(prs):
    s = new_slide(prs, "API Groups and Paths")
    bullets(s, 0.60, 1.62, 5.00, [
        (0, "The core group is at `/api/v1`. Its objects have `apiVersion: v1`"),
        (0, "A named group is at `/apis/<group>/<version>`, for example `/apis/apps/v1`"),
        (0, "An RBAC rule has the fields `apiGroups`, `resources` and `verbs`. Each tile of the diagram is a value "
            "of `resources`"),
        (0, "Each authenticated user can read the discovery paths, for example `/api` and `/apis`")],
        size=15, after=8, h=4.40)
    concept(s, 0.60, 6.10, 5.00, "Concept only: the lab does not read the path `/api`.")
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


def s_anonymous(prs):
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
                   '  "reason": "Forbidden",', '  "code": 403'])) + [""] +
          run(2, ("$ kubectl proxy", ["Starting to serve on 127.0.0.1:8001", "{", '  "kind": "APIGroupList",',
                                      '  "apiVersion": "v1",', '  "groups": ['])) +
          pick(2, "# kill %1 stops the proxy"), size=12)
    return s


def s_whoami(prs):
    s = new_slide(prs, "Authenticated, Not Authorized")
    bullets(s, 0.60, 1.62, 12.10, [
        (0, "`kubectl config set-credentials` writes the certificate and the key of `dev-user` into the kubeconfig "
            "file"),
        (0, "`kubectl config set-context` links `dev-user` to the cluster `kubernetes` and the namespace `week13`"),
        (0, "`kubectl auth whoami` (stable in v1.28) shows the user and the groups that the API server finds"),
        (0, "No Role allows `dev-user` to list Pods yet, so the API server denies `get pods`")], size=16, after=5,
        h=1.75)
    shell(s, 0.60, 3.50, 12.15, "Lab Week 13, Step 2", run(
        2, ("$ kubectl create namespace", ["namespace/week13 created"]),
        ("$ kubectl config set-credentials", ['User "dev-user" set.']),
        ("$ kubectl config set-context", ['Context "dev-user@kubernetes" created.']),
        ("$ kubectl --context=dev-user@kubernetes auth whoami", WHOAMI),
        ("$ kubectl --context=dev-user@kubernetes get pods",
         ['Error from server (Forbidden): pods is forbidden: User "dev-user" cannot list resource "pods" in API '
          'group "" in the namespace "week13"'])), size=10.5)
    return s


# ---------------------------------------------------------------- Part 2: authorization and RBAC

def s_part2(prs):
    return divider(prs, "Part 2", "Authorization and RBAC", "Modes, Roles and bindings")


def s_modes(prs):
    s = new_slide(prs, "Authorization Modes")
    bullets(s, 0.60, 1.62, 6.70, [
        (0, "The API server asks its authorizers in order. The first allow or deny decides"),
        (0, "When no authorizer has an opinion, the API server denies the request"),
        (0, "The modes of the flag `--authorization-mode`:"),
        (1, "`Node`: the requests of a kubelet, for the Pods on its node"),
        (1, "`RBAC`: Roles and bindings, as API objects (stable in v1.8)"),
        (1, "`Webhook`: an outside service allows, denies or has no opinion"),
        (1, "`ABAC`: a policy file on the API server"),
        (1, "`AlwaysAllow` and `AlwaysDeny`: for tests only"),
        (0, "The default is `AlwaysAllow`. kubeadm sets `Node,RBAC`"),
        (0, "Least privilege: give each user and each ServiceAccount only the permissions that it needs")],
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
    s = new_slide(prs, "The Four RBAC Objects")
    bullets(s, 0.60, 1.62, 6.00, [
        (0, "A Role or a ClusterRole holds rules. Each rule sets `apiGroups`, `resources` and `verbs`"),
        (0, "A RoleBinding or a ClusterRoleBinding gives one role to subjects: users, groups or ServiceAccounts"),
        (0, "The verbs: `get`, `list`, `watch`, `create`, `update`, `patch`, `delete` and `deletecollection`"),
        (0, "Rules only add permissions. RBAC has no deny rule")], size=15, after=6, h=2.85)
    grid(s, 0.60, 4.55, [1.25, 1.95, 2.90], [
        ["Scope", "What: the rules", "Who: the subjects"],
        ["One namespace", "Role `developer`", ["RoleBinding", "`devuser-developer-binding`"]],
        ["The whole cluster", "ClusterRole `pv-reader`", "ClusterRoleBinding `pv-test`"]], row_h=0.78, size=12.5)
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
    mark(s, 7.00, 5.82, 5.63, 0.60, "No rule has the verb `delete`, so `dev-user` cannot delete a Pod",
         align=PP_ALIGN.LEFT, size=13)
    return s


def s_role_lab(prs):
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
        (0, "The RoleBinding `developers-view` gives the group `developers` the ClusterRole `view`, in `week13` "
            "only. So `dev-user` can list the Services there")], size=14, after=6, h=6.65 - y - 0.20)
    shell(s, 8.95, 1.55, 3.80, "developer-role.yaml (Lab Week 13, Step 3)", FILES[3], size=10)
    return s


def s_cluster(prs):
    s = new_slide(prs, "ClusterRoles and ClusterRoleBindings")
    bullets(s, 0.60, 1.62, 6.00, [
        (0, "A ClusterRole and a ClusterRoleBinding have no namespace. Use them for nodes, PersistentVolumes and "
            "paths such as `/readyz`"),
        (0, "A RoleBinding that names a ClusterRole gives the rules in its own namespace only"),
        (0, "`kubectl auth can-i` asks if a subject can do an action. `--as` names the subject")],
        size=14, after=6, h=2.15)
    for k, (kind, verdict, fill) in enumerate((("RoleBinding", "No: a PersistentVolume has no namespace", RED),
                                               ("ClusterRoleBinding", "Yes: in the whole cluster", GREEN))):
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
    concept(s, 0.60, 6.28, 12.10, "Concept only: the lab does not bind `admin` or `edit`. Step 3 binds `view`.")
    return s


# ---------------------------------------------------------------- Part 3: ServiceAccounts

def s_part3(prs):
    return divider(prs, "Part 3", "ServiceAccounts", "The identity of a Pod")


def s_sa(prs):
    s = new_slide(prs, "The ServiceAccount of a Pod")
    bullets(s, 0.60, 1.62, 6.40, [
        (0, "A ServiceAccount is an object in a namespace. Each namespace has the ServiceAccount `default`"),
        (0, "`serviceAccountName` names one ServiceAccount in the namespace of the Pod. With no name, the Pod gets "
            "`default`"),
        (0, "You set it when you create the Pod. You cannot change it in a Pod that exists"),
        (0, "The kubelet mounts a token of the ServiceAccount into the Pod. The Week 12 lecture shows this token "
            "volume"),
        (0, "Outside `kube-system`, a new ServiceAccount has only the API discovery permissions")],
        size=15, after=8, h=4.40)
    concept(s, 0.60, 6.15, 6.40, "Concept only: the lab does not show the ServiceAccount `default`.")
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
    s = new_slide(prs, "A Pod Calls the API with Its Token")
    zone_code(s, 0.60, 1.62, 3.35, 2.35, "Pod `curl-sa` in `week13`", color=STEPS[1], fill=E.CARD_BG)
    code_box(s, 0.78, 2.02, 3.00, 1.75, "The token file",
             "/var/run/secrets/\nkubernetes.io/\nserviceaccount/token", STEPS[3], size=12)
    flow(s, 4.05, 2.10, 2.05, "1. Bearer token")
    flow(s, 4.05, 3.05, 2.05, "4. 403 Forbidden", fill=RED, kind=LEFT)
    zone_code(s, 6.20, 1.62, 6.55, 2.35, "API server: `kubernetes.default.svc`", color=STEPS[3], fill=E.CARD_BG)
    code_box(s, 6.35, 2.10, 3.70, 1.55, "2. Authentication: the user",
             "system:serviceaccount:\nweek13:clo835", STEPS[0], size=12.5)
    arrow(s, RIGHT, 10.10, 2.70, 0.30, 0.36, fill=SLATE)
    code_box(s, 10.45, 2.10, 2.15, 1.55, "3. RBAC: no rule allows", "list services", STEPS[4], size=12.5)
    shell(s, 0.60, 4.15, 5.00, "curl-sa.yaml (Lab Week 13, Step 4)", FILES[4], size=11.5)
    bullets(s, 5.85, 4.20, 6.90, [
        (0, "`serviceAccountName: clo835` gives the Pod the ServiceAccount `clo835`"),
        (0, "`curl` sends the token in the header `Authorization: Bearer`"),
        (0, "`curl` verifies the API server with the file `ca.crt` in this directory"),
        (0, "The token proves who the Pod is. RBAC then decides what it can do")], size=16, after=12, h=2.45)
    return s


def s_token_lab(prs):
    s = new_slide(prs, "The API Call of the Pod curl-sa")
    y = shell(s, 0.60, 1.55, 12.15, "Lab Week 13, Step 4", run(
        4, ("$ kubectl create serviceaccount", ["serviceaccount/clo835 created"]),
        ("$ kubectl apply -f curl-sa.yaml", ["pod/curl-sa created"]),
        ("$ kubectl wait", ["pod/curl-sa condition met"])) + [""] +
        pick(4, "# Ask the API server") + run(4, ("$ kubectl exec curl-sa", FORBIDDEN_JSON)), size=9)
    bullets(s, 0.60, y + 0.18, 12.10, [
        (0, "The answer is a Status object with the reason Forbidden and the code 403. Its message names the user "
            "of the token: the ServiceAccount `clo835`")], size=14, after=4, h=0.75)
    return s


def s_reader(prs):
    s = new_slide(prs, "A Role for the ServiceAccount")
    y = shell(s, 0.60, 1.55, 8.00, "Lab Week 13, Step 5",
              pick(5, "# The Role service-reader") +
              run(5, ("$ kubectl apply -f service-reader.yaml",
                      ["role.rbac.authorization.k8s.io/service-reader created",
                       "rolebinding.rbac.authorization.k8s.io/service-reader-binding created"])) + [""] +
              pick(5, "# The same call") + run(5, ("$ kubectl exec curl-sa", SERVICE_LIST)) + [""] +
              pick(5, "# A Role and its RoleBinding") +
              run(5, ("$ kubectl auth can-i list services", ["no"])), size=9.5)
    bullets(s, 0.60, y + 0.15, 8.00, [
        (0, "The subject of the RoleBinding is the ServiceAccount `clo835` of the namespace `week13`"),
        (0, "The token of `curl-sa` does not change. Only the new Role and RoleBinding change the answer")],
        size=14, after=4, h=6.65 - y - 0.15)
    shell(s, 8.85, 1.55, 3.90, "service-reader.yaml (Lab Week 13, Step 5)", FILES[5], size=10)
    return s


# ---------------------------------------------------------------- Part 4: Amazon EKS (concept only)

def s_part4(prs):
    return divider(prs, "Part 4", "Amazon EKS", "IAM identities in the cluster (concept only)")


def s_eks_auth(prs):
    s = new_slide(prs, "Authentication with IAM on Amazon EKS")
    eks_label(s)
    code_box(s, 0.60, 2.05, 2.75, 1.20, "Your computer", "kubectl\naws eks get-token", SLATE, size=13)
    code_box(s, 4.60, 2.05, 2.75, 1.20, "AWS STS", "GetCallerIdentity", STEPS[5], size=13)
    zone(s, 0.60, 3.80, 6.75, 2.80, "EKS control plane", color=STEPS[3], fill=E.CARD_BG)
    box(s, 0.80, 4.25, 2.35, 0.90, "API server", STEPS[3], size=14)
    box(s, 4.80, 4.25, 2.35, 0.90, "AWS IAM Authenticator", STEPS[1], size=13)
    box(s, 0.80, 5.55, 2.35, 0.90, "RBAC and the EKS authorizer", STEPS[4], size=13)
    code_box(s, 4.80, 5.55, 2.35, 0.90, "Access entry or", "aws-auth", STEPS[0], size=13)
    arrow(s, DOWN, 2.45, 3.30, 0.40, 0.90, fill=BLUE)
    mark(s, 2.92, 3.40, 0.90, 0.40, "2", align=PP_ALIGN.LEFT, size=14)
    arrow(s, MSO_LR, 3.22, 4.52, 1.52, 0.36, fill=BLUE)
    mark(s, 3.22, 4.10, 1.52, 0.36, "3", size=14)
    arrow(s, MSO_UD, 5.78, 3.30, 0.40, 0.90, fill=BLUE)
    mark(s, 6.25, 3.40, 0.60, 0.40, "4", align=PP_ALIGN.LEFT, size=14)
    arrow(s, E.MSO_SHAPE.UP_ARROW, 5.78, 5.18, 0.40, 0.34, fill=BLUE)
    mark(s, 6.25, 5.15, 0.60, 0.40, "5", align=PP_ALIGN.LEFT, size=14)
    arrow(s, DOWN, 1.78, 5.18, 0.40, 0.34, fill=BLUE)
    mark(s, 2.25, 5.15, 0.60, 0.40, "6", align=PP_ALIGN.LEFT, size=14)
    rich(s, 7.70, 2.00, 5.05, 4.60, [
        "1. `kubectl` runs `aws eks get-token`. The token is a signed URL for the AWS STS call "
        "`GetCallerIdentity`. It is valid for 15 minutes.",
        "2. `kubectl` sends the request and the token to the EKS API server.",
        "3. The API server sends the token to its authentication webhook, the AWS IAM Authenticator.",
        "4. The authenticator calls the signed URL. AWS STS returns the IAM identity.",
        "5. An access entry or the `aws-auth` ConfigMap maps this identity to a Kubernetes user and groups.",
        "6. Kubernetes RBAC and the Amazon EKS authorizer allow or deny the request."],
        size=13.5, spacing=1.08, after=7)
    return s


def s_access(prs):
    s = new_slide(prs, "The Access Entry and the aws-auth ConfigMap")
    eks_label(s, EKS_SHORT)
    bullets(s, 0.60, 2.00, 6.30, [
        (0, "An access entry maps one IAM role or IAM user to a Kubernetes user name and groups. AWS recommends this "
            "method"),
        (0, "You manage each access entry with the EKS API, the AWS CLI or the AWS console, outside the cluster"),
        (0, "Two methods give permissions to an access entry:"),
        (1, "An access policy: Kubernetes permissions that AWS defines, for example `AmazonEKSViewPolicy`, for the "
            "cluster or for some namespaces"),
        (1, "Kubernetes groups, with your own RBAC bindings"),
        (0, "After you enable the access entry method, you cannot disable it"),
        (0, "The `aws-auth` ConfigMap in `kube-system` is the old method. AWS marks it as deprecated")],
        size=14, after=6, h=4.65)
    end = grid(s, 7.15, 2.00, [2.60, 3.00], [
        ["Authentication mode", "IAM identities come from"],
        ["`CONFIG_MAP`", "The `aws-auth` ConfigMap only"],
        ["`API_AND_CONFIG_MAP`", "An access entry or the ConfigMap"],
        ["`API`", "An access entry only"]], row_h=0.50, size=12.5)
    shell(s, 7.15, end + 0.18, 5.60, "aws-auth (example only)", AWS_AUTH, size=9)
    return s


def s_creator(prs):
    s = new_slide(prs, "The IAM Identity That Created the Cluster")
    eks_label(s, EKS_SHORT)
    bullets(s, 0.60, 2.00, 6.00, [
        (0, "`bootstrapClusterCreatorAdminPermissions` (default `true`) gives admin access to the IAM identity that "
            "creates the cluster"),
        (0, "Modes `API` and `API_AND_CONFIG_MAP`: an access entry with `AmazonEKSClusterAdminPolicy`. You can "
            "see it and remove the policy"),
        (0, "Mode `CONFIG_MAP`: Amazon EKS puts the identity in `system:masters`. No visible configuration shows it"),
        (0, "Record which identity created each cluster. AWS calls the removal of this admin access a best "
            "practice")], size=15, after=12, h=4.60)
    grid(s, 6.85, 2.00, [1.75, 2.50, 1.65], [
        ["Admin identity", "kubeadm (the lab)", "Amazon EKS"],
        ["An authorizer checks it", ["`kubernetes-admin` of `admin.conf`", "in `kubeadm:cluster-admins`"],
         "The creator, as an access entry"],
        [["In `system:masters`:", "no authorization check"], "The user of `super-admin.conf`",
         "The creator, in the mode `CONFIG_MAP`"]], row_h=1.35, size=12)
    return s


# ---------------------------------------------------------------- the end of the lecture

def s_summary(prs):
    s = new_slide(prs, "Summary: Who Can Do What in the Lab")
    A, F = "Allowed", "Forbidden"
    end = verdict_grid(s, 0.60, 1.62, [4.30, 2.60, 2.60, 2.60],
                       ["Request, after Step 5", "`kubernetes-admin`", "`dev-user`", "`clo835`"], [
                           ["`$ kubectl get pods -n week13`", A, A, F],
                           ["`$ kubectl delete pod web -n week13`", A, F + " (Step 3)", F],
                           ["`$ kubectl get services -n week13`", A, A + " (Step 3)", A + " (Step 5)"],
                           ["`$ kubectl get services -n default`", A, F, F + " (Step 5)"],
                           ["`$ kubectl get persistentvolumes`", A, F, A + " (Step 5)"],
                           ["`$ kubectl get nodes`", A + " (Step 0)", F, F]], row_h=0.60, size=13)
    concept(s, 0.60, end + 0.20, 12.10, "Concept only: the lab does not run the cells with no step number.")
    return s


def s_optional(prs):
    return text_slide(prs, "Optional Topics", [
        (0, "`--authorization-config` (stable in v1.32): a file sets the chain of authorizers, also with more than "
            "one webhook"),
        (0, "The authentication configuration file (stable in v1.34) sets the JWT authenticators and the anonymous "
            "authenticator"),
        (0, "The verbs `escalate`, `bind` and `impersonate`, and aggregated ClusterRoles"),
        (0, "Amazon EKS can also give an AWS IAM role to a Pod: IAM roles for ServiceAccounts (IRSA) and EKS Pod "
            "Identity"),
        (0, "These topics are not in the lab or in the quiz")], size=17, after=11)


def s_takeaways(prs):
    return text_slide(prs, "Key Takeaways", [
        (0, "Authentication finds who sends a request. Authorization decides what this client can do"),
        (0, "The CN of a client certificate is the user name, and each O field is a group"),
        (0, "A Pod proves its identity with the token of its ServiceAccount. RBAC decides what the ServiceAccount "
            "can do"),
        (0, "A Role says what, and a RoleBinding says who"),
        (0, "An object with no namespace, such as a PersistentVolume, needs a ClusterRole and a ClusterRoleBinding"),
        (0, "On Amazon EKS, AWS recommends the access entry. AWS marks the `aws-auth` ConfigMap as deprecated")],
        size=17, after=11)


def s_lab(prs):
    s = new_slide(prs, "Lab Week 13 at a Glance")
    rows = [
        ["Lab step", "What you do", "Lecture slides"],
        ["Step 0", "Build and check the cluster.", nos(s_methods, s_summary)],
        ["Step 1", "Create the certificate of `dev-user`. Approve its CSR.",
         nos(s_clients, s_methods, s_certificate, s_certificate_lab, s_api, s_defaults)],
        ["Step 2", "Send requests with no credentials and through `kubectl proxy`. Authenticate as `dev-user`.",
         nos(s_path, s_clients, s_methods, s_certificate, s_certificate_lab, s_api, s_anonymous, s_whoami, s_modes,
             s_defaults, s_token)],
        ["Step 3", "Create the Role `developer` and its RoleBinding. Bind the group `developers` to the ClusterRole "
                   "`view`.", nos(s_path, s_clients, s_certificate, s_api, s_whoami, s_modes, s_objects, s_role_lab,
                                  s_cluster, s_defaults, s_sa, s_summary)],
        ["Step 4", "Call the API from the Pod `curl-sa` with the token of `clo835`.",
         nos(s_path, s_clients, s_methods, s_api, s_modes, s_sa, s_token, s_token_lab, s_reader)],
        ["Step 5", "Give `clo835` the Role `service-reader`. Test `pv-reader` with a RoleBinding and a "
                   "ClusterRoleBinding.", nos(s_clients, s_api, s_modes, s_objects, s_cluster, s_token, s_token_lab,
                                              s_reader, s_summary)],
        ["Step 6", "Destroy the cluster.", "–"]]
    found = {int(r[0][-1]): r[2] for r in rows[1:7]}
    assert found == MAP31, (found, MAP31)
    end = grid(s, 0.60, TOP + 0.08, [0.90, 8.05, 3.15], rows, row_h=0.36, size=13)
    note = [
        "Not in the lab: the configuration of admission control, the four other authentication methods, and the "
        "minimum lifetime and the revocation of a certificate.",
        "Also not in the lab: the answer 401, the prefix `system:`, the groups of a ServiceAccount, and the paths "
        "`/api`, `/livez`, `/readyz` and `/healthz`.",
        "Also not in the lab: a change of the authorization mode, RBAC with no deny rule, and the ClusterRoles "
        "`cluster-admin`, `admin` and `edit`.",
        "Also not in the lab: the verbs `watch`, `patch` and `deletecollection`, a command that uses `update` or "
        "`configmaps`, and nodes in a ClusterRole.",
        "Also not in the lab: `system:masters`, `kubeadm:cluster-admins`, a `serviceAccountName` of another namespace "
        "or a change of this field, and the optional topics.",
        "Also not in the lab: the API discovery permissions of a new ServiceAccount, the cells with no step on slide "
        "%d and Amazon EKS." % nos(s_summary)]
    check_note31(note)
    rich(s, 0.60, end + 0.10, 12.10, 6.68 - end - 0.10, note, size=12, color=E.MUTED, after=2)
    return s


def s_references(prs):
    s = new_slide(prs, "References")
    rich(s, 0.60, TOP + 0.15, 12.10, 4.90, [
        "`https://v1-35.docs.kubernetes.io/docs/concepts/security/controlling-access/`",
        "`https://v1-35.docs.kubernetes.io/docs/reference/access-authn-authz/authentication/`",
        "`https://v1-35.docs.kubernetes.io/docs/reference/access-authn-authz/authorization/`",
        "`https://v1-35.docs.kubernetes.io/docs/reference/access-authn-authz/rbac/`",
        "`https://v1-35.docs.kubernetes.io/docs/reference/access-authn-authz/certificate-signing-requests/`",
        "`https://v1-35.docs.kubernetes.io/docs/concepts/security/service-accounts/`",
        "`https://docs.aws.amazon.com/eks/latest/userguide/grant-k8s-access.html`",
        "`https://docs.aws.amazon.com/eks/latest/userguide/access-entries.html`",
        "`https://docs.aws.amazon.com/eks/latest/userguide/auth-configmap.html`",
        "`https://docs.aws.amazon.com/eks/latest/best-practices/identity-and-access-management.html`"],
        size=14, after=9)
    return s


MSO_LR, MSO_UD = E.MSO_SHAPE.LEFT_RIGHT_ARROW, E.MSO_SHAPE.UP_DOWN_ARROW

SLIDES = [s_part1, s_path, s_clients, s_methods, s_certificate, s_certificate_lab, s_api, s_anonymous, s_whoami,
          s_part2, s_modes, s_objects, s_role_lab, s_cluster, s_defaults,
          s_part3, s_sa, s_token, s_token_lab, s_reader,
          s_part4, s_eks_auth, s_access, s_creator,
          s_summary, s_optional, s_takeaways, s_lab, s_references]


def nos(*makers):
    """The slide numbers of these slide builders (the cover, the agenda and the outline are 1 to 3), in order."""
    found = sorted(SLIDES.index(m) + 4 for m in makers)
    return found[0] if len(found) == 1 else ", ".join(str(n) for n in found)


# The slide 31 map of review round 7: one complete pass over each pair (lab step 0 to 6, slide 5 to 29), with
# the columns "names the step", "shows or explains a command of the step", "answers a part of an Explain item of
# the Blackboard section of the step" and "states the rule or decision that gives an output of the step"
# (table and evidence: scratchpad w13/slide31_map.md). s_lab() asserts that its rows equal this map.
# Round 8: the admin rule of slide 18 does not count for "states the rule" (the decision of the coordinator).
MAP31 = {0: "7, 28", 1: "6, 7, 8, 9, 10, 18", 2: "5, 6, 7, 8, 9, 10, 11, 12, 14, 18, 21",
         3: "5, 6, 8, 10, 12, 14, 15, 16, 17, 18, 20, 28", 4: "5, 6, 7, 10, 14, 20, 21, 22, 23",
         5: "6, 10, 14, 15, 17, 21, 22, 23, 28"}

# Round 9: no note line of slide 31 names a topic that the evidence of a listed pair uses (w13/slide31_map.md).
# USED31: the code names of that evidence and of the lab lines of the listed pairs. TERMS31: the plain terms of
# that evidence that the note also names. Each phrase of QUAL31 limits a used term to a part that no listed pair
# uses, so check_note31() removes these phrases first. Round 10: a phrase (the text between commas) that names a
# ServiceAccount and a namespace must name the field serviceAccountName or a Pod. Step 5 tests clo835 of week13
# in the namespace default, so "a ServiceAccount of another namespace" alone is a topic of the lab.
USED31 = {"dev-user", "developers", "kubernetes-admin", "clo835", "system:anonymous", "system:authenticated",
          "system:unauthenticated", "system:discovery", "system:public-info-viewer",
          "system:serviceaccount:week13:clo835", "view", "default", "developer", "devuser-developer-binding",
          "developers-view", "service-reader", "pv-reader", "pv-test", "web", "curl-sa", "CertificateSigningRequest",
          "certificates.k8s.io/v1", "ca.crt", "/version", "/apis", "/api/v1", "/apis/<group>/<version>",
          "/api/v1/namespaces/week13/services", "pods", "services", "persistentvolumes", "configmaps",
          "certificatesigningrequests", "nodes", "get", "list", "create", "update", "delete", "apiGroups",
          "resources", "verbs", "serviceAccountName", "expirationSeconds"}
TERMS31 = ("admission control", "authorization mode", "RBAC", "nodes", "discovery")
QUAL31 = ("the configuration of admission control", "a change of the authorization mode", "RBAC with no deny rule",
          "a command that uses `update` or `configmaps`", "nodes in a ClusterRole",
          "a `serviceAccountName` of another namespace or a change of this field",
          "the API discovery permissions of a new ServiceAccount")


def check_note31(lines):
    for line in lines:
        for phrase in re.split(r", |: ", line):
            if re.search("serviceaccount", phrase, re.IGNORECASE) and "namespace" in phrase.lower():
                assert "`serviceAccountName`" in phrase or "Pod" in phrase, phrase
    text = " ".join(lines)
    for phrase in QUAL31:
        assert text.count(phrase) == 1, phrase
        text = text.replace(phrase, "")
    names = set(re.findall(r"`([^`]+)`", text)) & USED31
    terms = [t for t in TERMS31 if re.search(r"\b" + re.escape(t), text, re.IGNORECASE)]
    assert not names and not terms, (names, terms)


def main():
    if os.path.exists(OUT) and "--force" not in sys.argv:
        sys.exit("%s exists. Bump VERSION; never overwrite a delivered deck." % OUT)
    prs = Presentation(SRC)
    keep_first(prs, 3)
    cover(prs, "Authentication,", "RBAC and EKS", 13)
    agenda_week13(prs, [
        (0, "Authentication of a request"),
        (1, "Users, groups and client certificates"),
        (1, "Requests with no credentials, and `kubectl proxy`"),
        (0, "Authorization with RBAC"),
        (1, "The authorization modes, and RBAC"),
        (1, "Roles, ClusterRoles, RoleBindings and ClusterRoleBindings"),
        (1, "The default ClusterRoles"),
        (0, "ServiceAccounts and their tokens"),
        (1, "The token of a Pod, and a Role for a ServiceAccount"),
        (0, "Access to Amazon EKS for IAM identities (concept only)")])
    outline_week13(prs)
    built = [prs.slides[0], prs.slides[1], prs.slides[2]] + [make(prs) for make in SLIDES]
    number_and_save(prs, built, TITLE, OUT)


if __name__ == "__main__":
    main()
