# -*- coding: utf-8 -*-
"""CLO835 Week 06 lab v4 - Rollouts, Labels and Services, in ONE workshop.

v3 had 4 workshops and 21 steps. That does not fit in one 90-minute lab. The
user set the limit: no lab is longer than the Week 03 and Week 04 labs (at most
Step 0 to Step 6, about 60 commands). v4 keeps the 5 main lessons of v3, with
the same tested manifests: a Deployment, a rollout and a rollback, labels that
drive the ReplicaSet, a ClusterIP Service with DNS, and a NodePort Service.

Outputs: Week06/Lab_week06_v4.pptx, Week06/localMachine_v4.sh,
Week06/Lab_week06_Blackboard_Submission_v4.md, ~/Documents/c/r/CLO835_Fall_2026/Week06/
Run from the project root. It is guarded, so importing it writes nothing.
"""
import sys

import build_week06_lab_v3 as v3
import lab_kubeadm as L

F = L.FILE_MARK

SLIDES = [
 ("title", "Workshop 1 – Rollouts, Labels and Services"),
 ("prereq",),
 ("cluster",),
 ("step2", "A Deployment from a manifest", "bash", [
  "# The Deployment of the lecture: 3 replicas of kubia version 1.",
  "$ cat > deployment.yaml <<'EOF'",
  F,
  "EOF",
  "$ kubectl apply -f deployment.yaml",
  "$ kubectl rollout status deployment/kubia",
  " ",
  "# One Deployment, one ReplicaSet, three Pods.",
  "$ kubectl get deploy,rs,pods -o wide",
  ], "deployment.yaml", "deployment.yaml", v3.DEPLOYMENT),
 ("step", "Roll out version 2, then roll back", "bash", [
  "# Record why each revision exists. The history shows it.",
  "$ kubectl annotate deployment/kubia kubernetes.io/change-cause=\"image maziar/kubia:v1\"",
  "$ kubectl set image deployment/kubia kubia=maziar/kubia:v2",
  "$ kubectl annotate deployment/kubia kubernetes.io/change-cause=\"image maziar/kubia:v2\"",
  "$ kubectl rollout status deployment/kubia",
  " ",
  "# A second ReplicaSet holds the 3 Pods. The first one holds 0.",
  "$ kubectl get rs -o wide",
  "$ kubectl rollout history deployment/kubia",
  " ",
  "# Go back one revision. Revision 1 comes back as revision 3.",
  "$ kubectl rollout undo deployment/kubia",
  "$ kubectl rollout status deployment/kubia",
  "$ kubectl rollout history deployment/kubia",
  ]),
 ("step", "Labels drive the ReplicaSet", "bash", [
  "# The ReplicaSet finds its Pods by the label app=kubia.",
  "$ kubectl get pods --show-labels",
  "$ kubectl get pods -l app=kubia",
  " ",
  "# Take the newest Pod out of the selector: change its label.",
  "$ POD=$(kubectl get pods -l app=kubia --sort-by=.metadata.creationTimestamp \\",
  "    -o jsonpath='{.items[-1:].metadata.name}')",
  "$ kubectl label pod $POD app=kubia-debug --overwrite",
  " ",
  "# The ReplicaSet sees 2 Pods, so it makes a third Pod at once.",
  "$ kubectl rollout status deployment/kubia",
  "$ kubectl get pods -L app",
  " ",
  "# The re-labelled Pod still runs. No object owns it now.",
  "$ kubectl get pod $POD -o jsonpath='{.metadata.ownerReferences}'; echo",
  ]),
 ("step2", "A ClusterIP Service and its DNS name", "bash", [
  "# One stable address for the Pods with app=kubia.",
  "$ cat > service.yaml <<'EOF'",
  F,
  "EOF",
  "$ kubectl apply -f service.yaml",
  "$ kubectl get svc kubia",
  "$ kubectl get endpointslices -l kubernetes.io/service-name=kubia",
  "# 3 endpoints. The kubia-debug Pod is not one of them.",
  " ",
  "# A client Pod calls the Service by its name.",
  "$ kubectl run client --image=maziar/alpine-curl --command -- sleep 3600",
  "$ kubectl wait --for=condition=Ready pod/client --timeout=120s",
  "$ for i in 1 2 3 4; do kubectl exec client -- curl -s http://kubia; done",
  "$ kubectl exec client -- curl -s http://kubia.default.svc.cluster.local",
  ], "service.yaml", "service.yaml", v3.SERVICE),
 ("step2", "A NodePort Service", "bash", [
  "# A NodePort opens one port on EVERY node.",
  "$ cat > service-nodeport.yaml <<'EOF'",
  F,
  "EOF",
  "$ kubectl apply -f service-nodeport.yaml",
  "$ kubectl get svc kubia-nodeport",
  "$ sleep 2; curl -s http://localhost:30000",
  " ",
  "# ON YOUR OWN MACHINE, read the public addresses.",
  "L$ terraform output public_ips",
  "# Open http://<each-public-ip>:30000/ in a browser.",
  "# All 3 nodes answer.",
  ], "service-nodeport.yaml", "service-nodeport.yaml", v3.NODEPORT),
 ("step", "Clean up", "bash", [
  "# ON THE MASTER - remove the Kubernetes objects.",
  "$ bash cleanup_lab06.sh",
  " ",
  "# Confirm that nothing is left.",
  "$ kubectl get all | grep -E 'kubia|client'",
  " ",
  "# ON YOUR OWN MACHINE - remove the three EC2 machines.",
  "L$ terraform destroy",
  " ",
  "# Always destroy. The Learner Lab budget is small.",
  ]),
 ("end", "Workshop 1 – The End"),
]

SCRIPT_HEAD = """#!/bin/bash
# CLO835 - Week 06 - Rollouts, Labels and Services.
# Run these ON THE MASTER NODE, section by section. Do NOT run the whole file.
#
# Terraform builds 3 machines: 1 control plane and 2 workers. The cluster forms
# itself at boot, the same way it did in Weeks 04 and 05.
#
# Each step matches one slide of Lab_week06_v4.pptx.
"""

CLEANUP = """kubectl delete service kubia kubia-nodeport 2>/dev/null
kubectl delete deployment kubia 2>/dev/null
kubectl delete pod client --now 2>/dev/null
kubectl delete pod -l app=kubia-debug --now 2>/dev/null
rm -f ./deployment.yaml ./service.yaml ./service-nodeport.yaml

kubectl get all | grep -E "kubia|client\""""

BLACKBOARD = [
 ("Rollouts", "A Deployment rolls out a new image with a new ReplicaSet, and it can roll back.",
  ["Show the Deployment, its ReplicaSet and its 3 Pods.",
   "Show the two ReplicaSets after the rollout to maziar/kubia:v2.",
   "Show the rollout history before and after the undo, and explain why revision 1 becomes revision 3."]),
 ("Labels", "A ReplicaSet finds its Pods by label.",
  ["Show the Pods with their labels.",
   "Show the new Pod that the ReplicaSet makes after you change the label of one Pod.",
   "Explain why the re-labelled Pod has no owner."]),
 ("Services", "A Service gives the Pods one stable name and address.",
  ["Show the ClusterIP Service and its 3 endpoints.",
   "Show the client calls to http://kubia and to the full DNS name.",
   "Show the NodePort page from the public address of each of the three nodes.",
   "Show the clean-up and terraform destroy."]),
]

if __name__ == "__main__":
    L.check_lines(SLIDES)
    L.make_lab("06", SLIDES, "Week06/Lab_week06_v4.pptx", SCRIPT_HEAD, script_path="Week06/localMachine_v4.sh")
    if "--no-repo" not in sys.argv:
        dst, files = L.make_repo_folder("06", "Rollouts, Labels and Services", CLEANUP, "Week06/localMachine_v4.sh")
        print("repo folder : %s (%d files)" % (dst, len(files)))
    L.blackboard_text("06", "The Terraform configuration in Week 06 creates the same three Ubuntu 26.04 EC2 "
                      "machines as Weeks 04 and 05.", BLACKBOARD, "Week06/Lab_week06_Blackboard_Submission_v4.md")
    print("blackboard  : Week06/Lab_week06_Blackboard_Submission_v4.md")
