# -*- coding: utf-8 -*-
"""CLO835 Week 09 lecture v6 - Managed K8s, Amazon EKS.

Fixes every lecture defect of reports/report-2026-10-31-02-week09-standards-audit.md:
L1 cover week, L2 and L3 Course Outline, L4 and L5 third-party images replaced by
native house diagrams, L6 dead links, L7 storage slide and reading list, L8 bullets
in ASD-STE100, L9 title style. The cards of slides 3, 6 and 10 hold larger text.

Input : Week09/Week08_lecture_style_v5.pptx (read, never written)
Output: Week09/Lecture_week09_v6.pptx

Run from the project root. It is guarded, so importing it writes nothing.
"""
import re

from pptx import Presentation
from pptx.enum.dml import MSO_LINE
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

import build_week08 as E
from retarget_accounts import replace_in_paragraph

SRC = "Week09/Week08_lecture_style_v5.pptx"
OUT = "Week09/Lecture_week09_v6.pptx"
TOTAL = 12
NEW_SLIDE_AT = 10
WHITE, SLATE, BLUE = E.WHITE, E.SLATE, E.BLUE
STEPS = E.STEPS

REPLACE = {
    1: [("Week 8 · Lecture", "Week 9 · Lecture")],
    2: [("Week 9: K8s- K8s- PVs & K8s in AKS", "Week 9: K8s – PVs & K8s in EKS"),
        ("Week 13: K8s – RBAC and AKS", "Week 13: K8s – RBAC and EKS")],
    3: [("EKS is managed Kubernetes: AWS runs the hard parts so you can focus on your apps.",
         "EKS is managed Kubernetes. AWS runs the control plane, and you run your applications."),
        ("API server & scheduler", "API server and scheduler"),
        ("Multi-AZ high availability", "High availability across Availability Zones"),
        ("Version upgrades & patching", "Version upgrades and security patches"),
        ("No SSH: you reach it only through the Kubernetes API",
         "No SSH: you reach the control plane through the Kubernetes API only"),
        ("Your workloads (pods, services)", "Your workloads (Pods, Services)"),
        ("Scaling & app configuration", "Scaling and application configuration"),
        ("App data & access policies", "Application data and access policies"),
        ("Why EKS?  Less cluster operations — more time on your applications.",
         "EKS gives you less cluster work and more time for your applications.")],
    4: [("Cluster COST Estimate – Control Plane Only!", "Cluster Cost Estimate: Control Plane Only"),
        ("1 Clusters x 0.10 USD", "1 cluster x 0.10 USD"),
        ("Control plane only — worker nodes are billed separately.",
         "This cost is for the control plane only. AWS bills the worker nodes separately.")],
    5: [("Amazon EKS -  High level Architecture", "Amazon EKS: High-Level Architecture"),
        ("Master nodes are running in AWS VPC, not in our VPC",
         "The control plane runs in a VPC that AWS owns, not in your VPC.")],
    6: [("Where your pods actually run. EKS gives you three choices:",
         "Your Pods run on worker nodes. EKS gives you three choices:"),
        ("EC2 nodes AWS provisions for you", "AWS creates the EC2 nodes for you"),
        ("AWS handles create, update & drain", "AWS creates, updates and drains the nodes"),
        ("Easiest day-to-day option", "This option needs the least daily work"),
        ("You create & run the EC2 nodes", "You create and run the EC2 nodes"),
        ("Full control over the instances", "You have full control of the instances"),
        ("More setup & maintenance", "This option needs more setup and maintenance"),
        ("Serverless — no nodes to manage", "You manage no nodes"),
        ("AWS runs each pod for you", "AWS runs each Pod for you"),
        ("Pay per pod, not per node", "You pay for each Pod, not for each node"),
        ("One cluster can mix managed node groups and Fargate.",
         "One cluster can use managed node groups and Fargate together.")],
    7: [("Amazon EKS Cluster creation", "Amazon EKS Cluster Creation"),
        ("Cluster creation spans two layers: the steps you run, and the managed control plane AWS provisions underneath.",
         "Cluster creation has two layers: the steps that you run, and the steps that AWS runs."),
        ("The workflow you run", "The steps that you run")],
    8: [("EKS ARCHITECTURE FOR CONTROL PLANE AND WORKER NODE COMMUNICATION",
         "EKS Control Plane and Worker Node Communication")],
    9: [("Pods live inside your VPC and get real network identities.",
         "Pods run inside your VPC and get VPC IP addresses."),
        ("VPC CNI — every pod gets a real VPC IP address (not a hidden overlay network)",
         "The VPC CNI gives each Pod a VPC IP address. It uses no overlay network."),
        ("Public — reach the cluster API from the internet", "Public: you reach the cluster API from the internet"),
        ("Private — reach it only from inside your VPC", "Private: you reach the cluster API from inside your VPC only"),
        ("Control plane ↔ worker nodes talk over AWS-managed ENIs placed in your VPC, secured with TLS",
         "The control plane and the worker nodes communicate through AWS-managed ENIs in your VPC. TLS protects this traffic."),
        ("This is the control-plane ↔ node path shown in the previous diagram.",
         "The previous diagram shows this path.")],
    10: [("Access & Provisioning", "Access and Provisioning"),
         ("Authentication & authorization", "Authentication and authorization"),
         ("Who you are → AWS IAM (your user or role)", "AWS IAM identifies you (your user or your role)"),
         ("What you can do in the cluster → Kubernetes RBAC", "Kubernetes RBAC sets what you can do in the cluster"),
         ("aws eks update-kubeconfig wires kubectl to the cluster using your IAM identity",
          "aws eks update-kubeconfig connects kubectl to the cluster with your IAM identity"),
         ("eksctl & provisioning", "eksctl and provisioning"),
         ("eksctl = the official CLI to create & manage EKS clusters",
          "eksctl is the official CLI to create and manage EKS clusters"),
         ("Under the hood it builds AWS CloudFormation stacks (Infrastructure as Code)",
          "eksctl creates AWS CloudFormation stacks (Infrastructure as Code)"),
         ("You describe the cluster in a config file: eks_config.yaml",
          "You describe the cluster in a configuration file: eks_config.yaml")],
    11: [("https://docs.giantswarm.io/getting-started/persistent-volumes/aws/",
          "https://docs.aws.amazon.com/eks/latest/userguide/storage.html"),
         ("https://github.com/sojoudian/eksctl/tree/main/examples",
          "https://eksctl.io/usage/creating-and-managing-clusters/")],
}

# The cards of these slides were more than half empty.
RESIZE = {3: (16, ["TextBox 6", "TextBox 10"]),
          6: (15, ["TextBox 6", "TextBox 10", "TextBox 14"]),
          10: (16, ["TextBox 5", "TextBox 9"])}

REMOVE = {5: ["Picture 3"],
          7: ["TextBox 4", "Picture 5", "TextBox 7", "Picture 8"],
          8: ["Picture 2"]}


def shape_named(slide, name):
    found = [sh for sh in slide.shapes if sh.name == name]
    assert len(found) == 1, (name, len(found))
    return found[0]


def remove_shape(slide, name):
    sh = shape_named(slide, name)
    if sh.shape_type == 13:
        slide.part.drop_rel(sh._element.blipFill.blip.rEmbed)
    sh._element.getparent().remove(sh._element)


def apply_text(prs):
    for no, pairs in REPLACE.items():
        slide = prs.slides[no - 1]
        for old, new in pairs:
            hits = sum(replace_in_paragraph(p, old, new)
                       for sh in slide.shapes if sh.has_text_frame
                       for p in sh.text_frame.paragraphs)
            assert hits == 1, (no, old, hits)
    prs.slides[7].shapes[0].text_frame.paragraphs[0].runs[0].font.size = Pt(32)


def apply_sizes(prs):
    for no, (size, names) in RESIZE.items():
        slide = prs.slides[no - 1]
        for name in names:
            for p in shape_named(slide, name).text_frame.paragraphs:
                for r in p.runs:
                    r.font.size = Pt(size)


def box(s, x, y, w, h, text, fill, *, color=WHITE, size=13, bold=True, line=None, radius=0.10):
    E.add_rounded_rect(s, Inches(x), Inches(y), Inches(w), Inches(h), fill, line=line, radius_ratio=radius)
    E.add_text(s, Inches(x + 0.08), Inches(y), Inches(w - 0.16), Inches(h), text, size=size, bold=bold,
               color=color, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.05)


def zone(s, x, y, w, h, label, *, color=SLATE, dashed=False, fill=WHITE):
    shp = E.add_rounded_rect(s, Inches(x), Inches(y), Inches(w), Inches(h), fill, line=color,
                             line_width=1.25, radius_ratio=0.03)
    if dashed:
        shp.line.dash_style = MSO_LINE.DASH
    E.add_text(s, Inches(x + 0.14), Inches(y + 0.07), Inches(w - 0.28), Inches(0.3), label, size=12,
               bold=True, color=color)


def arrow(s, kind, x, y, w, h, fill=BLUE):
    shp = s.shapes.add_shape(kind, E._i(Inches(x)), E._i(Inches(y)), E._i(Inches(w)), E._i(Inches(h)))
    shp.fill.solid()
    shp.fill.fore_color.rgb = fill
    shp.line.fill.background()
    shp.shadow.inherit = False


def label(s, x, y, w, h, text, *, size=11.5, color=SLATE, align=PP_ALIGN.CENTER):
    E.add_text(s, Inches(x), Inches(y), Inches(w), Inches(h), text, size=size, color=color, align=align,
               anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.05)


def slide5(s):
    bullet = shape_named(s, "TextBox 2")
    bullet.left, bullet.top, bullet.width, bullet.height = Inches(0.55), Inches(1.12), Inches(12.2), Inches(0.4)

    zone(s, 0.55, 3.45, 2.35, 1.45, "On-premises network")
    box(s, 0.95, 3.95, 1.55, 0.7, "Client", STEPS[5])
    zone(s, 0.55, 5.05, 2.35, 1.45, "Internet")
    box(s, 0.95, 5.55, 1.55, 0.7, "Client", STEPS[5])

    zone(s, 3.5, 1.7, 9.28, 4.95, "AWS Cloud")
    zone(s, 3.72, 2.12, 6.9, 1.12, "VPC that AWS owns", color=STEPS[4], fill=E.CARD_BG)
    box(s, 5.3, 2.47, 3.75, 0.62, "Amazon EKS control plane", SLATE, size=14)
    box(s, 10.8, 2.12, 1.8, 1.12, "Amazon ECR", STEPS[1], size=14)

    zone(s, 3.72, 3.42, 6.9, 3.08, "Your VPC", color=BLUE, fill=E.CARD_BG)
    for x, text, fill in ((3.9, "EC2 node (managed)", STEPS[0]), (6.13, "EC2 node (self-managed)", STEPS[3]),
                          (8.36, "Fargate Pods", STEPS[1])):
        zone(s, x, 3.8, 2.08, 2.55, "Availability Zone", color=STEPS[4], dashed=True)
        label(s, x + 0.1, 4.18, 1.88, 0.3, "Private subnet", size=11)
        box(s, x + 0.17, 4.62, 1.74, 1.45, text, fill, size=13.5)

    zone(s, 10.8, 3.42, 1.8, 3.08, "Another VPC", color=STEPS[1])
    box(s, 11.0, 4.62, 1.4, 0.7, "Client", STEPS[5])

    # The arrows come last, so no zone covers an arrow head.
    arrow(s, MSO_SHAPE.RIGHT_ARROW, 2.98, 4.12, 0.72, 0.34)
    arrow(s, MSO_SHAPE.RIGHT_ARROW, 2.98, 5.72, 0.72, 0.34)


def flow(s, y, steps, fill):
    x = 0.55
    for k, text in enumerate(steps):
        box(s, x, y, 2.55, 1.05, text, fill, size=15)
        if k < len(steps) - 1:
            arrow(s, MSO_SHAPE.RIGHT_ARROW, x + 2.6, y + 0.35, 0.42, 0.36, STEPS[0])
        x += 3.05


def slide7(s):
    head = shape_named(s, "TextBox 3")
    head.left, head.top, head.width = Inches(0.55), Inches(1.65), Inches(12.2)
    flow(s, 2.15, ["Create the EKS cluster", "Provision worker nodes", "Launch add-ons", "Launch workloads"], STEPS[3])

    head = shape_named(s, "TextBox 6")
    head.left, head.top, head.width = Inches(0.55), Inches(3.95), Inches(12.2)
    para = head.text_frame.paragraphs
    para[0].runs[0].text = "The steps that AWS runs inside “Create the EKS cluster”"
    for extra in list(para[1:]):
        extra._p.getparent().remove(extra._p)
    flow(s, 4.45, ["Create HA control plane", "IAM integration", "Certificate management", "Set up load balancer"], SLATE)


def slide8(s):
    zone(s, 0.9, 1.6, 5.0, 4.95, "Your VPC", color=BLUE, dashed=True)
    box(s, 1.2, 2.2, 2.5, 3.85, "EC2 worker nodes\nAuto Scaling group", SLATE, size=15)
    box(s, 4.8, 4.55, 0.9, 0.8, "ENI", STEPS[0], size=15)

    zone(s, 7.4, 1.6, 5.0, 4.95, "VPC that AWS owns", color=SLATE, dashed=True)
    box(s, 8.2, 2.2, 3.4, 1.0, "Network Load Balancer\nStatic IP addresses", STEPS[3], size=14)
    box(s, 8.2, 4.25, 3.4, 1.4, "EKS control plane", SLATE, size=16)
    arrow(s, MSO_SHAPE.DOWN_ARROW, 9.72, 3.28, 0.38, 0.9)

    label(s, 5.95, 2.15, 1.4, 0.3, "API access", size=13)
    arrow(s, MSO_SHAPE.RIGHT_ARROW, 3.78, 2.5, 4.34, 0.36)
    arrow(s, MSO_SHAPE.LEFT_ARROW, 5.78, 4.77, 2.34, 0.36, STEPS[1])
    label(s, 5.95, 5.2, 1.4, 0.8, "ENI attachment:\nkubectl exec\nand logs", size=12)
    arrow(s, MSO_SHAPE.LEFT_ARROW, 3.78, 4.77, 0.94, 0.36, STEPS[1])
    label(s, 3.78, 4.4, 0.94, 0.3, "TLS", size=13)


def storage_slide(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    E.title(s, "Persistent Volumes on EKS")
    E.add_text(s, Inches(0.55), Inches(1.12), Inches(12.2), Inches(0.4),
               "A PersistentVolume on EKS needs a CSI driver. AWS recommends the EKS add-on to install each driver.",
               size=14, color=E.BODY)
    E.concept_card(s, 0.70, 1.75, 5.80, 4.15, "Amazon EBS: block storage", [
        "The EBS CSI driver creates an EBS volume for a PersistentVolume",
        "The usual access mode is ReadWriteOnce",
        "The volume stays in one Availability Zone",
        "You cannot mount an EBS volume to a Fargate Pod",
    ], BLUE, body_size=16)
    E.concept_card(s, 6.85, 1.75, 5.80, 4.15, "Amazon EFS: shared file storage", [
        "The EFS CSI driver mounts an EFS file system as a PersistentVolume",
        "Many Pods share the same files (ReadWriteMany)",
        "Pods in different Availability Zones can use the file system",
        "A Fargate Pod mounts EFS with no driver installation",
    ], SLATE, body_size=16)
    E.add_text(s, Inches(0.70), Inches(6.05), Inches(11.95), Inches(0.4),
               "Each CSI driver needs IAM permissions.", size=13.5, italic=True, color=E.MUTED,
               align=PP_ALIGN.CENTER)
    E.whale_and_footer(s, NEW_SLIDE_AT, TOTAL)
    ids = prs.slides._sldIdLst
    last = ids[-1]
    ids.remove(last)
    ids.insert(NEW_SLIDE_AT - 1, last)


def renumber(prs):
    for k, slide in enumerate(prs.slides, 1):
        hits = 0
        for sh in slide.shapes:
            if sh.has_text_frame:
                for p in sh.text_frame.paragraphs:
                    for r in p.runs:
                        if re.fullmatch(r"CLO835, Fall 2026\s+\d+ / \d+", r.text):
                            r.text = "CLO835, Fall 2026     %d / %d" % (k, TOTAL)
                            hits += 1
        assert hits == 1, (k, hits)


def main():
    prs = Presentation(SRC)
    assert len(prs.slides) == 11
    apply_text(prs)
    apply_sizes(prs)
    for no, names in REMOVE.items():
        for name in names:
            remove_shape(prs.slides[no - 1], name)
    slide5(prs.slides[4])
    slide7(prs.slides[6])
    slide8(prs.slides[7])
    storage_slide(prs)
    renumber(prs)
    assert len(prs.slides) == TOTAL
    E._sanitize_coords(prs)
    prs.save(OUT)
    print("wrote %s (%d slides)" % (OUT, TOTAL))


if __name__ == "__main__":
    main()
