# Report: The remaining labs against their lectures
**Date**: 2026-10-27
**Sequence**: #11 for the day

## Summary
The user asked if the remaining labs are 100% according to the lectures. They are
not. None of the 5 lab decks after Week 06 matches its lecture fully. Week 12 is
the closest: it is correct and runnable, but it practises only part of the
lecture. Weeks 08, 09, 13 and 14 need Amazon EKS, Cloud9 and (13, 14) new IAM
users, which the course environment does not give the students. They also hold 14
broken commands on visible slides. Week 07 has no lab. This check is read-only;
no file changed.

## What Changed
- Created this report. No deck, script or memory changed.

## Technical Details

### Method
- Dumped each lab and its new lecture in deck order (titles, bullets, terminals,
  hidden flags) and compared them topic by topic.
- Read the text inside the lab images with macOS Vision OCR.
- Searched every command line for an EN DASH, a curly quotation mark or a
  zero-width space.

### The decks compared
| Week | Lab | Lecture (after report #10) |
|---|---|---|
| 07 | none | `Week07/Week07_lab_style_v5.pptx` |
| 08 | `Week09/Week08_lab_style_v3.pptx` (30, 1 hidden) | `Week09/Week08_lecture_style_v5.pptx` |
| 09 | `Week10/Week09_lab_style_v2.pptx` (31) | `Week10/Week09_lecture_style_v7.pptx` |
| 12 | `Week12/Week12_lab_v2.pptx` (10) | `Week12/Week12_v3.pptx` |
| 13 | `week13/Week13_lab_style_v6.pptx` (26, 6 hidden) | `week13/Week13_lecture_style_v7.pptx` |
| 14 | `week14/Week14_lab_style_v11.pptx` (23, 2 hidden) | `week14/Week14_lecture_style_v11.pptx` |

`CLO835_Workshops_Lab_v2.pptx` (45) is the summer merge of the Week 08 and
Week 09 labs. It holds the same defects.

### Result per lab
| Week | Verdict | Main reasons |
|---|---|---|
| 07 | no lab | emptyDir is practised in the Week 08 lab, hostPath and PV/PVC in the Week 09 lab; the gitRepo/init-container and NFS examples are practised nowhere |
| 08 | no | needs EKS + Cloud9; Kubernetes Dashboard (not in the lecture, `kubernetes/dashboard` v2.0.0 from 2020); 2 broken commands; the fortune Pod manifest is a cropped picture that shows 6 lines only |
| 09 | no | needs EKS (eksctl, gp2, EBS CSI add-on, LabRole); 7 broken commands; 3 `luksa` links and the `luksa/kubia-pet-peers` image; `alpine/curl`; slide 2 still says "kind and minikube"; the cleanup removes Week 08 objects, not Week 09 ones |
| 12 | partly | correct and runnable on kubeadm, but it practises only ConfigMap and Secret from literals as env vars; it injects a Secret as an env var, which lecture slide 19 calls "not the recommended way" |
| 13 | no | the ServiceAccount workshop (slides 2 to 7) is hidden; needs EKS + IAM user and policy creation; 7 broken commands (`– sh`); two "Workshop 2" title slides |
| 14 | no | Workshop 1 is the Week 13 IAM workshop again, word for word; the lecture's `kubectl config` commands are not practised; Workshop 2 (node IAM role, Kinesis) is not in the lecture; 2 broken commands |

### 1. Environment (critical)
- `PREFERENCES.md` section 10: the students have no EKS; the course uses the
  kubeadm cluster on EC2. The Week 08, 09, 13 and 14 labs all start with
  `eksctl create cluster` and run in Cloud9.
- Week 13 and 14 create an IAM user (`aws iam create-user`), access keys and an
  IAM policy, and Week 14 changes the node instance role. The AWS Academy Learner
  Lab does not allow a student to create IAM users, roles or policies.
- The lectures of Weeks 08, 13 and 14 teach EKS, so lab and lecture agree with
  each other, but neither one can be practised in the course environment.
- Week 14 HPA on a kubeadm cluster would need `--kubelet-insecure-tls` on
  metrics-server. The mirrored `components.yaml` does not hold that flag.

### 2. Broken commands on visible slides (14)
| Lab | Slide | Command |
|---|---|---|
| 08 | 8 | `aws –-version` (EN DASH) |
| 08 | 24 | `k get all –n week8` |
| 09 | 5 | `eksctl create cluster –f eks_config.yaml` |
| 09 | 9 | `k get all –n kube-proxy` (also the wrong namespace: kube-proxy runs in kube-system) |
| 09 | 14 | `k get pvc –n week9` |
| 09 | 15 | `k get pods –n week9` |
| 09 | 22 | `k create –f kubia-statefulset.yaml` |
| 13 | 9 (×2), 10, 11, 13, 15, 16 | `kubectl exec -it test -n ... – sh` |
Hidden slides of Week 13 hold 5 more.

Other command defects:
- Week 08 slide 13: removes `aws_session_token` from the config; Learner Lab credentials need it.
- Week 09 slide 15: `k delete pod-xxx redis` (wrong syntax); `redis:3.2.5` (2016).
- Week 09 slide 23: `curl -X POST -d "..."` has no URL.
- Week 14 slide 13: `k run awscli ... -- ec2 describe-instances` ends the pod, then
  `k exec awscli -- ecr describe-repositories` runs with no `aws` and no pod.
- Week 14 slide 21: `k autoscale ... \ --cpu-percent=50 \ --min=1 ...` on one line;
  each `\ ` becomes an escaped space, so the flags arrive with a leading space.

### 3. Lecture topics that no lab practises
- Week 07: the gitRepo replacement (init container + emptyDir), NFS.
- Week 08: nothing of the EKS architecture beyond the cluster creation.
- Week 09: the StorageClass manifest (slide 19 of v7).
- Week 12: command/args (slides 5 to 7), ConfigMap from a file or YAML, `envFrom`,
  ConfigMap and Secret as volumes, the default token mount, tmpfs.
- Week 13: ServiceAccounts and tokens (hidden), groups, IRSA (named in the title
  and agenda, taught nowhere).
- Week 14: `kubectl config view / get-contexts / use-context / set-context`.

### 4. Lab topics that the lecture does not teach
- Week 08: the Kubernetes Dashboard (3 slides); the fortune emptyDir pod and the
  NodePort/LoadBalancer exposure (Week 06 and 07 topics).
- Week 14: pod access through the worker node IAM role (Kinesis).

### 5. Left over from the lecture changes of today
- Week 08 lab slide 3 keeps the 2 bullets that report #10 removed from the
  lecture; slide 18 keeps the "Volume Lifecycle" slide.
- Week 09 lab slide 17 keeps "WHAT ARE STATEFULSETS??".
- Week 09 lab slide 2 still says "kind and minikube". My kind answer of today
  called this file superseded. That was wrong: it is the current lab.
- Other accounts: Week 08 `kubernetes/dashboard`, `weaveworks/eksctl`; Week 09
  `luksa/...` (3 links, 1 image), `alpine/curl`.

### 6. Duplicates inside and between labs
- Week 08 slides 21 and 22: the same title and the same 3 bullets.
- Week 08 slides 27 and 28: the same title.
- Week 13: two slides titled "Workshop 2".
- Week 14 slides 2 to 9 = Week 13 slides 18 to 25.

### 7. Files the student never receives
`eks_config.yaml`, `fortune_pod.yaml` (cropped picture), `mongodb_hostpath.yaml`,
`mongodb_aws.yaml`, `redis_*.yaml`, `kubia-statefulset.yaml`, `kubia-clusterIP.yaml`,
`kubia-headless.yaml`, `kubectl-proxy-pod.yaml`, `service-reader.yaml`,
`clo835-role.yaml`, `creds.sh`, `switch_to_admin.sh`, `iam_policy.json`,
`eks_config_week11.yaml`, `eks_config_auth.yaml`, and the "Week8-Document".
No course repository folder exists after Week 06.

### 8. Names and labels
- Covers: Week 09 lecture "Week 10 · Lecture" against its lab "Week 9 · Lab";
  Weeks 12, 13, 14 say Week 10, 11, 12.
- Namespaces: Week 12 uses `week10`; Week 13 outputs say `week10` and mix
  `week11-1` with `week11-2`; Week 14 uses `week12` and then `week11`.
- Week 13 and 14 outputs show a real AWS account ID, `047923129740`.

## Results
- 0 of 5 labs are 100% according to their lectures. Week 07 has no lab.
- 14 broken commands on visible slides, 5 more on hidden slides.
- 4 of 5 labs depend on EKS, Cloud9 and IAM rights that the students do not have.

## Issues / Notes
- I changed nothing. The fixes are a design decision: either rebuild Weeks 08,
  09, 13 and 14 on the kubeadm cluster (as Weeks 04 to 06 were), or keep EKS and
  confirm that the Learner Lab permits it.
- I did not run any lab command. The findings come from reading.
