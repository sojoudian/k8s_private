# -*- coding: utf-8 -*-
"""CLO835 Week 06 - build the lab deck and the lab script from ONE content list.

The Week 06 lecture (Week06/Week06_lecture_style_v7.pptx) teaches rollouts,
labels and selectors, and Services. This lab practises each of them on the
kubeadm cluster of Weeks 04 and 05, in 4 workshops. The design comes from the
Week 05 lab deck: its title, prerequisite, cluster and end slides are copied,
and each step is one house terminal slide.

Input : Week05/Lab_week05_v4.pptx   (never written)
Output: Week06/Lab_week06_v2.pptx
        and, with --script PATH, the localMachine.sh of the repository.

The deck and the script use the same lines, so they cannot differ.
It is guarded, so importing it writes nothing.

v2 (16 Oct 2026), after a check against the kubeadm v1.35 source:
- slide 7: the Failed events are sorted by time;
- slides 7, 8, 9 and 23: each set image is followed by its change-cause;
- slide 9: the pause is shown by UP-TO-DATE 0 and the ReplicaSet counts;
- slide 29: kubeadm CoreDNS does not cache Service names, so the call
  fails at once (sleep 2, not sleep 35); kubia-v2 is called after sleep 2.
"""
import copy, io, os, re, sys
from pptx import Presentation
from pptx.util import Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.opc.constants import RELATIONSHIP_TYPE as RT

BASE = os.environ.get("K8S_BASE", os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(BASE, "Week05/Lab_week05_v4.pptx")
OUT = os.path.join(BASE, "Week06/Lab_week06_v2.pptx")
EMU = 914400

BLUE, SLATE, MUTED, HAIRLINE = "1FA8E0", "37465A", "868686", "E0E0E0"
TERM_BG, TERM_BAR = "2A2A2A", "3A3A3A"
RED, AMBER, GREEN = "FF5F56", "FFBD2E", "27C93F"
CMD, OUTP = "4EC9E0", "BABABA"
CALIBRI, CONSOLAS = "Calibri", "Consolas"
FILE_MARK = "<<FILE>>"            # the place of the file of the right panel
FILE_LINE = "#   ... the file on the right ..."


# ------------------------------------------------------------------ content
DEPLOYMENT = """apiVersion: apps/v1
kind: Deployment
metadata:
  name: kubia
spec:
  replicas: 3
  selector:
    matchLabels:
      app: kubia
  template:
    metadata:
      labels:
        app: kubia
    spec:
      terminationGracePeriodSeconds: 5
      containers:
      - name: kubia
        image: luksa/kubia:v1
        ports:
        - name: http
          containerPort: 8080""".split("\n")

PODS = """apiVersion: v1
kind: Pod
metadata:
  name: kubia-manual
spec:
  containers:
  - name: kubia
    image: luksa/kubia:v1
---
apiVersion: v1
kind: Pod
metadata:
  name: kubia-manual-v2
  labels:
    creation_method: manual
    env: prod
spec:
  containers:
  - name: kubia
    image: luksa/kubia:v1""".split("\n")

SERVICE = """apiVersion: v1
kind: Service
metadata:
  name: kubia
spec:
  selector:
    app: kubia
  ports:
  - name: http
    port: 80
    targetPort: http""".split("\n")

NODEPORT = """apiVersion: v1
kind: Service
metadata:
  name: kubia-nodeport
spec:
  type: NodePort
  selector:
    app: kubia
  ports:
  - name: http
    port: 80
    targetPort: http
    nodePort: 30000""".split("\n")

INGRESS = """apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: kubia
spec:
  rules:
  - host: kubia.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: kubia-nodeport
            port:
              number: 80""".split("\n")

# Each entry is one slide, in order.
#   ("title", text)                          a LAB title slide (copy of slide 1)
#   ("prereq",)                              the prerequisites (copy of slide 2)
#   ("cluster",)                             preparing the cluster (copy of slide 3)
#   ("end", text)                            an end slide (copy of slide 18)
#   ("step", title, term, lines)             one full-width terminal
#   ("step2", title, term, lines, file, name, body)  a terminal and a file panel
# In the lines: "$ " is a command on the master, "L$ " a command on the
# laptop, "#" a comment, " " an empty line, FILE_MARK the file of the slide.
SLIDES = [
 ("title", "Workshop 1 – Deployment Rollouts, Revisions and Rollbacks"),
 ("prereq",),
 ("cluster",),
 ("step2", "A Deployment from a manifest", "bash", [
  "# The Deployment of the lecture: 3 replicas of kubia version 1.",
  "# Write deployment.yaml with a here-document.",
  "$ cat > deployment.yaml <<'EOF'",
  FILE_MARK,
  "EOF",
  "$ kubectl apply -f deployment.yaml",
  "$ kubectl rollout status deployment/kubia",
  " ",
  "# One Deployment, one ReplicaSet, three Pods.",
  "$ kubectl get deploy,rs,pods -o wide",
  " ",
  "# The container port has a name: http. Slide 17 uses it.",
  "# This app ignores the stop signal. terminationGracePeriodSeconds: 5",
  "# makes Kubernetes stop an old Pod after 5 seconds, not after 30.",
  ], "deployment.yaml", "deployment.yaml", DEPLOYMENT),
 ("step", "Rolling out version 2", "bash", [
  "# Record why revision 1 exists. The rollout history shows it.",
  "$ kubectl annotate deployment/kubia kubernetes.io/change-cause=\"image luksa/kubia:v1\"",
  " ",
  "# A new image starts a rollout. The Deployment makes a second ReplicaSet.",
  "$ kubectl set image deployment/kubia kubia=luksa/kubia:v2",
  "$ kubectl annotate deployment/kubia kubernetes.io/change-cause=\"image luksa/kubia:v2\"",
  "$ kubectl rollout status deployment/kubia",
  " ",
  "# The old ReplicaSet now holds 0 Pods. The new one holds the 3 Pods.",
  "$ kubectl get rs -o wide",
  " ",
  "# Ask the newest Pod which version it runs. The master reaches each Pod IP.",
  "$ kubectl get pods -l app=kubia -o wide",
  "$ curl -s $(kubectl get pods -l app=kubia --sort-by=.metadata.creationTimestamp \\",
  "    -o jsonpath='{.items[-1:].status.podIP}'):8080",
  "# This is v2 running in pod kubia-...",
  ]),
 ("step", "Rollout history and rollback", "bash", [
  "# Each revision is one ReplicaSet. CHANGE-CAUSE shows the annotation.",
  "$ kubectl rollout history deployment/kubia",
  "$ kubectl rollout history deployment/kubia --revision=2",
  " ",
  "# Go back one revision. The v1 ReplicaSet scales up again.",
  "$ kubectl rollout undo deployment/kubia",
  "$ kubectl rollout status deployment/kubia",
  " ",
  "# Revision 1 is now revision 3. A rollback is a new rollout.",
  "$ kubectl rollout history deployment/kubia",
  " ",
  "# Go to a named revision: back to v2.",
  "$ kubectl rollout undo deployment/kubia --to-revision=2",
  "$ kubectl rollout status deployment/kubia",
  "$ kubectl get rs -o wide",
  ]),
 ("step", "A failed rollout", "bash", [
  "# Roll out an image tag that does not exist, and record the change-cause.",
  "$ kubectl set image deployment/kubia kubia=luksa/kubia:v9",
  "$ kubectl annotate deployment/kubia kubernetes.io/change-cause=\"image luksa/kubia:v9\"",
  " ",
  "# The rollout cannot finish. The status command stops after 60 seconds.",
  "$ kubectl rollout status deployment/kubia --timeout=60s",
  " ",
  "# One new Pod cannot pull its image. The 3 old Pods still serve.",
  "# 25% of 3 Pods rounds down to 0, so no old Pod may stop.",
  "$ kubectl get pods -l app=kubia",
  "$ kubectl get rs",
  "$ kubectl get events --field-selector reason=Failed --sort-by=.lastTimestamp | tail -3",
  " ",
  "# Roll back the failed rollout.",
  "$ kubectl rollout undo deployment/kubia",
  "$ kubectl rollout status deployment/kubia",
  "$ kubectl get pods -l app=kubia",
  ]),
 ("step", "Rollout strategy - Recreate", "bash", [
  "# The default strategy is RollingUpdate. Change this Deployment to Recreate.",
  "$ kubectl patch deployment kubia \\",
  "    -p '{\"spec\":{\"strategy\":{\"type\":\"Recreate\",\"rollingUpdate\":null}}}'",
  "$ kubectl get deployment kubia -o jsonpath='{.spec.strategy}'; echo",
  " ",
  "# SECOND SSH SESSION - watch the Pods. Press Ctrl+C to stop.",
  "$ kubectl get pods -l app=kubia -w",
  " ",
  "# FIRST SSH SESSION - roll out v1 with Recreate, and record the change-cause.",
  "$ kubectl set image deployment/kubia kubia=luksa/kubia:v1",
  "$ kubectl annotate deployment/kubia kubernetes.io/change-cause=\"image luksa/kubia:v1\"",
  "$ kubectl rollout status deployment/kubia",
  "# All 3 old Pods stop first. Only then do the 3 new Pods start.",
  " ",
  "# Change the Deployment back to the default strategy.",
  "$ kubectl patch deployment kubia -p '{\"spec\":{\"strategy\":{\"type\":\"RollingUpdate\"}}}'",
  "$ kubectl get deployment kubia -o jsonpath='{.spec.strategy}'; echo",
  ]),
 ("step", "Pause and resume a rollout", "bash", [
  "# Pause: the Deployment accepts changes, but it does not roll them out.",
  "$ kubectl rollout pause deployment/kubia",
  "$ kubectl set image deployment/kubia kubia=luksa/kubia:v2",
  "$ kubectl annotate deployment/kubia kubernetes.io/change-cause=\"image luksa/kubia:v2\"",
  " ",
  "# The image is now v2, but UP-TO-DATE is 0. The v1 ReplicaSet keeps its 3 Pods.",
  "$ kubectl get deployment kubia -o wide",
  "$ kubectl get rs -o wide",
  " ",
  "# Resume: the change that waited rolls out now.",
  "$ kubectl rollout resume deployment/kubia",
  "$ kubectl rollout status deployment/kubia",
  " ",
  "# The v2 ReplicaSet from slide 5 gets the 3 Pods again. A Deployment",
  "# reuses the ReplicaSet that has the same Pod template, so none is new.",
  "$ kubectl get rs -o wide",
  ]),
 ("end", "Workshop 1 – The End"),

 ("title", "Workshop 2 – Using Labels to Organize K8s Pods"),
 ("step2", "Pods with labels", "bash", [
  "# Two Pods: the first has no labels, the second has two.",
  "$ cat > pods-with-labels.yaml <<'EOF'",
  FILE_MARK,
  "EOF",
  "$ kubectl apply -f pods-with-labels.yaml",
  " ",
  "# Show all the labels, or only some of them as columns.",
  "$ kubectl get pods --show-labels",
  "$ kubectl get pods -L creation_method,env",
  " ",
  "# Add a label. Change a label with --overwrite.",
  "$ kubectl label pod kubia-manual creation_method=manual",
  "$ kubectl label pod kubia-manual-v2 env=debug --overwrite",
  "$ kubectl get pods -L creation_method,env",
  ], "pods-with-labels.yaml", "pods-with-labels.yaml", PODS),
 ("step", "Select Pods with a label selector", "bash", [
  "# Equality: the label has this value.",
  "$ kubectl get pods -l creation_method=manual",
  "$ kubectl get pods --selector app=kubia",
  " ",
  "# Existence: the Pod has the label, or it does not have the label.",
  "$ kubectl get pods -l env",
  "$ kubectl get pods -l '!env'",
  " ",
  "# Set: the value is one of a list.",
  "$ kubectl get pods -l 'env in (prod,debug)'",
  " ",
  "# Two conditions: both must be true.",
  "$ kubectl get pods -l creation_method=manual,env=debug",
  ]),
 ("step", "Labels drive the ReplicaSet", "bash", [
  "# A ReplicaSet finds its Pods by label. Read its selector.",
  "$ kubectl get rs -l app=kubia -o wide",
  "$ kubectl get pods -l app=kubia --show-labels",
  " ",
  "# Take one Pod out of the selector.",
  "$ POD=$(kubectl get pods -l app=kubia --sort-by=.metadata.creationTimestamp \\",
  "    -o jsonpath='{.items[-1:].metadata.name}')",
  "$ kubectl label pod $POD app=kubia-debug --overwrite",
  " ",
  "# The ReplicaSet sees 2 Pods, and it makes a third Pod at once.",
  "$ kubectl get pods -L app",
  " ",
  "# The re-labelled Pod still runs, but no object owns it now.",
  "$ kubectl get pod $POD -o jsonpath='{.metadata.ownerReferences}'; echo",
  ]),
 ("end", "Workshop 2 – The End"),

 ("title", "Workshop 3 – Using K8s Services"),
 ("step2", "A ClusterIP Service", "bash", [
  "# One stable address for the 3 Pods. ClusterIP is the default type.",
  "$ cat > service.yaml <<'EOF'",
  FILE_MARK,
  "EOF",
  "$ kubectl apply -f service.yaml",
  "$ kubectl get svc kubia",
  " ",
  "# targetPort: http is the NAME of the container port 8080.",
  "# The endpoints are the Pods with app=kubia. The kubia-debug",
  "# Pod is not one of them.",
  "$ kubectl describe svc kubia",
  "$ kubectl get endpointslices -l kubernetes.io/service-name=kubia",
  ], "service.yaml", "service.yaml", SERVICE),
 ("step", "Reach the Service from inside the cluster", "bash", [
  "# Way 1 - a client Pod calls the Service by its name.",
  "$ kubectl run client --image=alpine:3.22 --command -- sleep 3600",
  "$ kubectl wait --for=condition=Ready pod/client --timeout=120s",
  "$ for i in 1 2 3 4 5; do kubectl exec client -- wget -qO- http://kubia; done",
  "# The Service spreads the calls over the Pods.",
  " ",
  "# Way 2 - run curl inside one of the kubia Pods.",
  "$ kubectl exec deploy/kubia -- curl -s http://kubia",
  " ",
  "# Way 3 - on a node, call the ClusterIP. The master is a node.",
  "$ curl -s http://$(kubectl get svc kubia -o jsonpath='{.spec.clusterIP}')",
  ]),
 ("step", "Endpoints follow the Pods", "bash", [
  "# Scale down. The Service keeps one endpoint: a Pod that is ready.",
  "$ kubectl scale deployment kubia --replicas=1",
  "$ kubectl describe svc kubia | grep Endpoints",
  " ",
  "# Scale to zero. A stopping Pod still answers, so wait until it is gone.",
  "$ kubectl scale deployment kubia --replicas=0",
  "$ kubectl wait --for=delete pod -l app=kubia --timeout=60s",
  "$ kubectl describe svc kubia | grep Endpoints",
  " ",
  "# No Pod, no endpoint: the call fails.",
  "$ kubectl exec client -- wget -qO- -T 5 http://kubia",
  "# wget: can't connect to remote host (10.x.x.x): Connection refused",
  " ",
  "# Scale back to 3. The endpoints come back by themselves.",
  "$ kubectl scale deployment kubia --replicas=3",
  "$ kubectl rollout status deployment/kubia",
  "$ kubectl describe svc kubia | grep Endpoints",
  ]),
 ("step", "kube-proxy writes the rules", "bash", [
  "# kube-proxy runs on every node, as one Pod of a DaemonSet.",
  "$ kubectl get pods -n kube-system -l k8s-app=kube-proxy -o wide",
  " ",
  "# A Service has no process. It is a set of rules in the kernel.",
  "$ sudo iptables-save -t nat | grep 'default/kubia:http' | head -5",
  " ",
  "# kube-proxy writes the same rules on each node. A call to the",
  "# ClusterIP on any node reaches a Pod on any node.",
  ]),
 ("step2", "A NodePort Service", "bash", [
  "# A NodePort opens one port on EVERY node.",
  "# Terraform opens 30000-32767 on all three nodes.",
  "$ cat > service-nodeport.yaml <<'EOF'",
  FILE_MARK,
  "EOF",
  "$ kubectl apply -f service-nodeport.yaml",
  " ",
  "# A NodePort Service also gets a ClusterIP.",
  "$ kubectl get svc kubia-nodeport",
  "# kube-proxy needs a moment to write the rules.",
  "$ sleep 2; curl -s http://localhost:30000",
  " ",
  "# ON YOUR OWN MACHINE, read the public addresses.",
  "L$ terraform output public_ips",
  "# Open http://<each-public-ip>:30000/ in a browser. All 3 answer.",
  ], "service-nodeport.yaml", "service-nodeport.yaml", NODEPORT),
 ("step", "A LoadBalancer Service on kubeadm", "bash", [
  "# kubeadm has no cloud load balancer. Ask for one anyway.",
  "$ kubectl expose deployment kubia --name=kubia-lb --type=LoadBalancer \\",
  "    --port=80 --target-port=http",
  " ",
  "# EXTERNAL-IP stays <pending>: no controller gives an address.",
  "$ kubectl get svc kubia-lb",
  " ",
  "# The Service still works, through the NodePort that it got.",
  "$ NP=$(kubectl get svc kubia-lb -o jsonpath='{.spec.ports[0].nodePort}')",
  "$ echo $NP",
  "$ sleep 2; curl -s http://localhost:$NP",
  " ",
  "# A cloud provider fills EXTERNAL-IP with the address of its load balancer.",
  ]),
 ("step", "A rolling update through the Service", "bash", [
  "# SECOND SSH SESSION - call the Service once a second, for 40 seconds.",
  "$ kubectl exec client -- sh -c \\",
  "    'for i in $(seq 1 40); do wget -qO- -T 2 http://kubia; sleep 1; done'",
  " ",
  "# FIRST SSH SESSION - roll out v1 with the default RollingUpdate.",
  "$ kubectl set image deployment/kubia kubia=luksa/kubia:v1",
  "$ kubectl annotate deployment/kubia kubernetes.io/change-cause=\"image luksa/kubia:v1\"",
  "$ kubectl rollout status deployment/kubia",
  " ",
  "# The second session shows v2 answers, then v1 answers. While both",
  "# versions run, the answers can mix. No call fails: an old Pod stops",
  "# only after a new Pod is ready.",
  ]),
 ("step2", "Ingress needs a controller", "bash", [
  "# An Ingress routes HTTP calls by host and path to a Service.",
  "$ cat > ingress.yaml <<'EOF'",
  FILE_MARK,
  "EOF",
  "$ kubectl apply -f ingress.yaml",
  " ",
  "# The API server keeps the rule, but ADDRESS stays empty.",
  "$ kubectl get ingress kubia",
  " ",
  "# No ingress controller runs in this cluster.",
  "# So no program reads the rule, and no program serves it.",
  "$ kubectl get ingressclass",
  ], "ingress.yaml", "ingress.yaml", INGRESS),
 ("end", "Workshop 3 – The End"),

 ("title", "Workshop 4 – Service Discovery and DNS in K8s"),
 ("step", "Discovery through DNS", "bash", [
  "# CoreDNS answers the names. Its Service is kube-dns.",
  "$ kubectl get svc -n kube-system kube-dns",
  "$ kubectl get pods -n kube-system -l k8s-app=kube-dns -o wide",
  " ",
  "# Each Pod sends its DNS questions to the ClusterIP of kube-dns.",
  "$ kubectl exec client -- cat /etc/resolv.conf",
  " ",
  "# The full name, a short form, and the short name all work.",
  "$ kubectl exec client -- wget -qO- http://kubia.default.svc.cluster.local",
  "$ kubectl exec client -- wget -qO- http://kubia.default",
  "$ kubectl exec client -- wget -qO- http://kubia",
  ]),
 ("step", "Discovery through environment variables", "bash", [
  "# A Pod gets variables for each Service that exists when the Pod starts.",
  "$ kubectl exec client -- env | grep KUBIA_SERVICE",
  " ",
  "# kubia-manual started before the Service, so it has no such variable.",
  "$ kubectl exec kubia-manual -- env | grep KUBIA_SERVICE",
  " ",
  "# DNS has no such limit. Each Pod resolves each Service name.",
  "$ kubectl exec kubia-manual -- curl -s http://kubia",
  ]),
 ("step", "The Service name is the contract", "bash", [
  "# A client calls a Service by its name. Give the same Pods a second name.",
  "$ kubectl expose deployment kubia --name=kubia-v2 --port=80 --target-port=http",
  "# kube-proxy needs a moment to write the rules.",
  "$ sleep 2; kubectl exec client -- wget -qO- -T 5 http://kubia-v2",
  " ",
  "# Delete the first name. A client that still calls it fails.",
  "# CoreDNS and kube-proxy need a moment to remove the name and the rules.",
  "$ kubectl delete service kubia",
  "$ sleep 2; kubectl exec client -- wget -qO- -T 5 http://kubia",
  "# wget: bad address 'kubia'",
  " ",
  "# The Pods did not change. Only the name is gone.",
  "$ kubectl get pods -l app=kubia",
  ]),
 ("step", "Clean up", "bash", [
  "# ON THE MASTER - remove the Kubernetes objects.",
  "$ bash cleanup_lab06.sh",
  " ",
  "# Confirm that nothing is left.",
  "$ kubectl get all,ingress | grep -E 'kubia|client'",
  " ",
  "# ON YOUR OWN MACHINE - remove the three EC2 machines.",
  "L$ terraform destroy",
  " ",
  "# Always destroy. The Learner Lab budget is small.",
  ]),
 ("end", "Workshop 4 – The End"),
]

# The cluster slide (copy of Week 05 slide 3): the lines that change.
CLUSTER_EDITS = {
    "$ cd week5_code": "$ cd CLO835_Fall_2026/Week06",
    "# NodePort 30000-32767 is open on both workers.": "# NodePort 30000-32767 is open on all three nodes.",
}
PREREQ_TITLE = "Lab 6 - Prerequisites"

# The checks of the cluster slide, as Step 0 of the script.
STEP0 = [
    "# All three nodes must reach Ready. The workers take a few minutes to join.",
    "kubectl get nodes -o wide",
    "kubectl get pods -n kube-system",
]


# ------------------------------------------------------------------ drawing
def _i(v):
    return int(round(float(v)))


def E(inches):
    return _i(float(inches) * EMU)


def _txt(slide, x, y, w, h, lines, size, font, align=PP_ALIGN.LEFT,
         bold=False, colour=None, spacing=None):
    tb = slide.shapes.add_textbox(E(x), E(y), E(w), E(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = MSO_ANCHOR.TOP
    for k, (text, col) in enumerate(lines):
        p = tf.paragraphs[0] if k == 0 else tf.add_paragraph()
        p.alignment = align
        if spacing:
            p.line_spacing = spacing
        r = p.add_run()
        r.text = text
        r.font.name = font
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.color.rgb = RGBColor.from_string(col or colour or SLATE)
    return tb


def _box(slide, x, y, w, h, fill):
    sp = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, E(x), E(y), E(w), E(h))
    sp.fill.solid()
    sp.fill.fore_color.rgb = RGBColor.from_string(fill)
    sp.line.fill.background()
    sp.shadow.inherit = False
    sp.text_frame.text = ""
    return sp


def _dot(slide, x, y, fill):
    sp = slide.shapes.add_shape(MSO_SHAPE.OVAL, E(x), E(y), E(0.13), E(0.13))
    sp.fill.solid()
    sp.fill.fore_color.rgb = RGBColor.from_string(fill)
    sp.line.fill.background()
    sp.shadow.inherit = False
    return sp


def slide_lines(lines):
    """The lines as the slide shows them: "L$ " becomes "$ ", the file mark a note."""
    out = []
    for l in lines:
        if l == FILE_MARK:
            out.append(FILE_LINE)
        elif l.startswith("L$ "):
            out.append("$ " + l[3:])
        else:
            out.append(l)
    return out


def coloured(lines, yaml=False):
    """Comment green, command (and its continuation lines) cyan, other grey."""
    out, cont = [], False
    for l in lines:
        t = l.strip()
        if yaml:
            col = OUTP
        elif t.startswith("#"):
            col = GREEN
        elif t.startswith("$") or cont:
            col = CMD
        else:
            col = OUTP
        cont = (not yaml) and (t.startswith("$") or cont) and t.endswith("\\")
        out.append((l, col))
    return out


# A rendered Consolas line is about 0.212 in tall at 11 pt with 1.15 spacing,
# and a terminal leaves 4.63 in. A character is about 0.55 em wide.
def fit_size(lines, width):
    longest = max(len(l) for l in lines)
    size = 11.0
    while size > 9.0 and (len(lines) * 0.212 * size / 11 > 4.63 or
                          longest * size * 0.55 / 72 > width - 0.36):
        size -= 0.5
    assert len(lines) * 0.212 * size / 11 <= 4.63, ("too many lines", lines[0])
    assert longest * size * 0.55 / 72 <= width - 0.36, ("line too long", max(lines, key=len))
    return size


def terminal(s, x, w, term_title, lines, yaml=False):
    _box(s, x, 1.45, w, 5.10, TERM_BG)
    _box(s, x, 1.45, w, 0.32, TERM_BAR)
    for k, col in enumerate((RED, AMBER, GREEN)):
        _dot(s, x + 0.15 + k * 0.17, 1.55, col)
    _txt(s, x, 1.49, w, 0.32, [(term_title, OUTP)], 10, CALIBRI, align=PP_ALIGN.CENTER)
    size = fit_size(lines, w)
    _txt(s, x + 0.18, 1.87, w - 0.32, 4.63, coloured(lines, yaml), size, CONSOLAS, spacing=1.15)
    return size


def house_frame(s, title, whale):
    _txt(s, 0.55, 0.40, 12.20, 0.85, [(title, BLUE)], 32, CALIBRI, bold=True)
    if whale:
        s.shapes.add_picture(io.BytesIO(whale), E(0.45), E(6.85), E(0.50), E(0.50))
    c = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, E(0.50), E(7.05), E(12.83), E(7.05))
    c.line.color.rgb = RGBColor.from_string(HAIRLINE)
    c.line.width = Pt(0.5)
    _txt(s, 9.50, 7.12, 3.35, 0.30, [("CLO835, Fall 2026     0 / 0", MUTED)],
         10, CALIBRI, align=PP_ALIGN.RIGHT)


def step_slide(prs, layout, whale, title, term, lines):
    s = prs.slides.add_slide(layout)
    house_frame(s, title, whale)
    terminal(s, 0.55, 12.20, term, slide_lines(lines))
    return s


def step2_slide(prs, layout, whale, title, term, lines, file_title, body):
    s = prs.slides.add_slide(layout)
    house_frame(s, title, whale)
    terminal(s, 0.55, 7.55, term, slide_lines(lines))
    terminal(s, 8.40, 4.35, file_title, body, yaml=True)
    return s


# ------------------------------------------------------------------ copying slides
def clone_slide(prs, src):
    """Copy a slide of the same deck, with its pictures."""
    s = prs.slides.add_slide(src.slide_layout)
    for sh in list(s.shapes):
        sh._element.getparent().remove(sh._element)
    tree = s.shapes._spTree
    for el in src.shapes._spTree:
        tag = el.tag.split("}")[-1]
        if tag in ("sp", "cxnSp", "grpSp", "graphicFrame", "pic"):
            tree.append(copy.deepcopy(el))
    ns_r = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
    for blip in tree.iter("{http://schemas.openxmlformats.org/drawingml/2006/main}blip"):
        rid = blip.get(ns_r + "embed")
        if rid:
            part = src.part.related_part(rid)
            blip.set(ns_r + "embed", s.part.relate_to(part, RT.IMAGE))
    return s


def set_text(shape, text):
    runs = [r for p in shape.text_frame.paragraphs for r in p.runs]
    runs[0].text = text
    for r in runs[1:]:
        r.text = ""


def shape_with_text(slide, text):
    found = [sh for sh in slide.shapes if sh.has_text_frame and sh.text_frame.text.strip() == text]
    assert len(found) == 1, (text, len(found))
    return found[0]


FOOTER_RE = re.compile(r"^CLO835,\s+Fall\s+\d{4}\s+\d+\s*/\s*\d+$")


def set_footer(slide, n, total):
    for sh in slide.shapes:
        if sh.has_text_frame and FOOTER_RE.match(sh.text_frame.text.strip()):
            set_text(sh, "CLO835, Fall 2026     %d / %d" % (n, total))
            return True
    return False


def sanitize(prs):
    ns = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
    fixed = 0
    for s in prs.slides:
        for el in s.shapes._spTree.iter():
            if el.tag in (ns + "off", ns + "ext", ns + "chOff", ns + "chExt"):
                for k in ("x", "y", "cx", "cy"):
                    v = el.get(k)
                    if v and ("." in v or "e" in v.lower()):
                        el.set(k, str(_i(float(v))))
                        fixed += 1
    return fixed


def whale_blob(prs):
    for s in prs.slides:
        for sh in s.shapes:
            if sh.shape_type == 13 and (sh.width or 0) < E(0.8):
                return sh.image.blob
    return None


def delete_slide(prs, slide):
    lst = prs.slides._sldIdLst
    for sid in list(lst):
        if prs.part.related_part(sid.rId) is slide.part:
            prs.part.drop_rel(sid.rId)
            lst.remove(sid)
            return


# ------------------------------------------------------------------ build
def build(out=OUT):
    prs = Presentation(SRC)
    old = list(prs.slides)
    assert len(old) == 18, "expected the 18-slide Lab_week05_v4"
    T_TITLE, T_PREREQ, T_CLUSTER, T_END = old[0], old[1], old[2], old[17]
    shape_with_text(T_TITLE, "Workshop 1 – Deployment of K8s Pod")
    shape_with_text(T_END, "Workshop 1 – The End")
    whale = whale_blob(prs)
    layout = old[3].slide_layout
    sizes = []
    for item in SLIDES:
        kind = item[0]
        if kind == "title":
            s = clone_slide(prs, T_TITLE)
            set_text(shape_with_text(s, "Workshop 1 – Deployment of K8s Pod"), item[1])
        elif kind == "prereq":
            s = clone_slide(prs, T_PREREQ)
            set_text(shape_with_text(s, "Deployment of K8s Pod  - Prerequisites"), PREREQ_TITLE)
        elif kind == "cluster":
            s = clone_slide(prs, T_CLUSTER)
            for a, b in CLUSTER_EDITS.items():
                set_text(shape_with_text(s, a), b)
        elif kind == "end":
            s = clone_slide(prs, T_END)
            set_text(shape_with_text(s, "Workshop 1 – The End"), item[1])
        elif kind == "step":
            step_slide(prs, layout, whale, item[1], item[2], item[3])
        elif kind == "step2":
            step2_slide(prs, layout, whale, item[1], item[2], item[3], item[5], item[6])
    for s in old:
        delete_slide(prs, s)
    S = list(prs.slides)
    total = len(S)
    ok = sum(1 for n, s in enumerate(S, 1) if set_footer(s, n, total))
    f = sanitize(prs)
    prs.save(out)
    print("slides      : %d" % total)
    print("footers set : %d" % ok)
    print("floats fixed: %d" % f)
    print("saved       : %s" % out)
    return total


# ------------------------------------------------------------------ the script
SCRIPT_HEAD = """#!/bin/bash
# CLO835 - Week 06 - Rollouts, Labels and Services.
# Run these ON THE MASTER NODE, section by section. Do NOT run the whole file.
#
# Terraform builds 3 machines: 1 control plane and 2 workers. The cluster forms
# itself at boot, the same way it did in Weeks 04 and 05. This week the subject
# is how a Deployment rolls out a new version, how labels select Pods, and how
# a Service gives a group of Pods one stable name and address.
#
# Each step matches one slide of Lab_week06_v2.pptx.
"""


def script_lines(lines, body=None):
    out = []
    for l in lines:
        if l == FILE_MARK:
            out += body
        elif l.startswith("L$ "):
            out.append("# ON YOUR OWN MACHINE:  " + l[3:])
        elif l.startswith("$ "):
            out.append(l[2:])
        elif l == " ":
            out.append("")
        else:
            out.append(l)
    return out


def section(n, title, slide_no):
    head = "# Step %d - %s" % (n, title)
    return ["", "#" * 56, "%s%s(slide %d)" % (head, " " * max(1, 48 - len(head)), slide_no), "#" * 56]


def write_script(path):
    out = SCRIPT_HEAD.rstrip("\n").split("\n")
    n = 0
    for k, item in enumerate(SLIDES, 1):
        if item[0] == "cluster":
            out += section(0, "check the cluster", k) + STEP0
        elif item[0] in ("step", "step2"):
            n += 1
            out += section(n, item[1], k)
            out += script_lines(item[3], item[6] if item[0] == "step2" else None)
    open(path, "w").write("\n".join(out) + "\n")
    print("script      : %s (%d steps)" % (path, n))


if __name__ == "__main__":
    args = sys.argv[1:]
    if "--script" in args:
        write_script(args[args.index("--script") + 1])
    out = OUT
    if "--out" in args:
        out = args[args.index("--out") + 1]
    if "--no-deck" not in args:
        build(out)
