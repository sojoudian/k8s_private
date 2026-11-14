# CLO835 Semester Project Ideas

Course: "Portable Technologies in Cloud" — cloud, Docker, Kubernetes, DevOps (not coding-focused).
Infra: AWS Academy Cloud9 + Learner Lab (EKS with LabRole).

---

## Short version — 5 projects

All on AWS Cloud9 + Learner Lab (EKS with LabRole). Teams of 2–3. Live demo + individual oral. Teardown required.

### 1. Portable two-tier app: kind → EKS
Same web+DB app, one Git repo, deployed to both local kind and EKS. EBS-CSI PV/PVC, ConfigMap, Secret, LoadBalancer. Rolling update v1→v2 (v2 prints student ID), then rollback.
Oral: "Run both now. Why NodePort on kind but LoadBalancer on EKS? Delete the DB pod — data survives? Show the EBS volume ID and AZ."

### 2. Stateful DB + backup/restore + DR on EKS
Database as StatefulSet, per-replica PVCs (EBS-CSI), headless service, Secret creds. Prove backup→delete→restore (EBS snapshot) and node-drain survival.
Oral: "Restore from your snapshot live. Show the snapshot ID. What breaks if two replicas share one PVC?"

### 3. CI/CD pipeline to EKS with rollback
GitHub Actions builds/pushes on merge (tag = version + SHA), deploys to EKS, canary/blue-green + auto rollback on failed health check.
Oral: "Trigger a deploy now. Force it to fail — show the rollback. Where are your creds and why not in the repo?"

### 4. Secure + autoscaling service on EKS
Harden: image scan gate in CI, non-root + cap-drop + no-new-privileges, K8s Secrets, RBAC least-privilege, NetworkPolicy. Add HPA. Load-test to trigger scale-out.
Oral: "Prove your service account can't delete pods in another namespace. Run the load test — show HPA scaling. Which CVEs did you fix?"

### 5. Scaling + cost engineering on EKS
HPA + cluster autoscaler, load-test to scale, real AWS cost + teardown report within budget. No coding.
Oral: "Show scale-out live. What did this cluster cost? Prove full teardown."

Why AI-resistant (all 5): real Learner Lab resource IDs (EKS ARN, EBS volume/snapshot IDs, LoadBalancer DNS) can't be faked; live demo from their Cloud9; break-and-fix-live segment; student ID in output; git commits dated across the term.

Pick #1 — widest coverage, best fit to "Portable Technologies."

---

## Long version — analysis + full design

### Part 1 — What the course actually equips students to do

By the end of the term a CLO835 student can operate this toolchain (grounded in the decks/labs/assignments):

| Domain | Concrete skills they've done with their hands |
|---|---|
| Docker | Dockerfiles (ENV/CMD/ENTRYPOINT), build/tag/push to Docker Hub, multi-arch buildx, user-defined bridge networks + DNS service discovery, named volumes vs bind mounts, hardening (`--cap-drop`, secret files, `no-new-privileges`, `scout`/`trivy` scanning) |
| Git / CI-CD | branch + PR workflow, GitHub Actions building & publishing images on merge, creds as GH Actions secrets, image tags = version + commit SHA |
| Kubernetes | `kubectl`, Pods/ReplicaSets/Deployments, rolling update + rollback, Services (ClusterIP/NodePort/LoadBalancer), labels/selectors, Volumes, PV/PVC/StorageClass, EBS CSI dynamic provisioning, StatefulSets + headless service + peer discovery, ConfigMaps & Secrets (Wk 10). Coming: RBAC (12), HPA (13), Helm (14) |
| Cloud / EKS | provision EKS via eksctl (CloudFormation under the hood), Cloud9 + Learner Lab, LabRole IAM + K8s RBAC auth, `aws eks update-kubeconfig`, VPC-CNI, node groups vs Fargate, cost/teardown discipline |
| IaC / DevOps | Terraform (EC2 + kind), cloud-init bootstrap, kubeconfig wiring, teardown |

AI-resistance DNA already in the course (extend it, don't reinvent):
1. "Explain why / what would happen if…" attached to every graded criterion (the labs do this on every line).
2. Personalised output — Assignment 2 bakes the student's own Seneca ID into the running app; own Docker Hub repo; own AWS account.
3. Evidence = name-labelled screenshots + real command output.
4. Timed git history — "all commits dated before the deadline."
5. AI explicitly allowed for code, but the deliverable requires personal artifacts + understanding.

### Part 2 — Design principles for an AI-proof, in-person-defended semester project

The strongest AI-resistance lever is the AWS Cloud9 + Learner Lab infra, because it produces student-unique, real, un-fabricatable identifiers:

- Real resource IDs an LLM cannot invent: EKS cluster ARN, EBS volume IDs, LoadBalancer DNS name, ENI IDs, EBS snapshot IDs, CloudFormation stack IDs — all tied to their account and this term.
- Live demo from their Cloud9 during the presentation (the running system, not slides).
- A "break-it-and-fix-it live" segment — AI can write a manifest, but can't troubleshoot their broken cluster in front of you.
- Per-student randomised parameters (student ID in output + an assigned port/colour/DB/failure-scenario) so answers can't be copied between students.
- A per-component oral question bank (the lab "explain why" pattern, scaled up).
- A mandatory teardown + cost report — fits the ~$50 / 4-hour-session / us-east-1 Learner Lab limits and proves they operated it.

Suggested logistics: teams of 2–3; 25–30% of grade; 3 milestones across the back half of term (proposal → mid-build checkpoint → final demo); final grade split ~60% working system + 40% individual oral defense (every member answers independently).

### Part 3 — The project proposals

#### Project A (flagship) — "Portable Two-Tier App: Local → Cloud"
Directly embodies the course name.
Deploy the same containerised two-tier app (web + stateful DB) from one Git source of truth to two targets: local kind (in Cloud9) and Amazon EKS, and account for every difference.
- Phases: containerise (Dockerfile + push to their Docker Hub) → CI/CD (GitHub Actions builds/publishes on merge) → deploy to kind → deploy to EKS with EBS-CSI PV/PVC/StorageClass, ConfigMaps, Secrets, LoadBalancer → rolling update v1→v2 (v2 prints their student ID) → rollback.
- AI-proof core: run it on both targets live and explain why the same app needs a different Service type (NodePort vs LoadBalancer) and different storage (local-path vs EBS CSI). Real LoadBalancer DNS + EBS volume ID shown in the AWS console.
- Oral: "Show both running now. Delete the DB pod on EKS — does data survive? Why? Show me the EBS volume backing it and its AZ. Why did your v2 rollout not drop traffic?"
- Cloud9/Learner-Lab fit: short-lived EKS cluster, teardown report at the end.

#### Project B — "Stateful Data Platform + Backup & Disaster Recovery on EKS"
Extends the old final ("stateful app on EKS with PVs") into the part AI can't fake: recovery.
Run a real DB (MySQL/Mongo/Postgres) as a StatefulSet on EKS with per-replica PVCs (EBS CSI), headless service, Secret-based credentials — then implement and prove a backup → destroy → restore cycle (EBS snapshot or logical dump) and a resilience drill (delete a stateful pod / drain a node → PV re-attaches, data survives).
- AI-proof core: a working restore demoed live. You cannot bluff a restore. Real snapshot IDs, real volume IDs.
- Oral: "Delete pod db-0 now and narrate what happens to its PV. Show your snapshot. Restore from it live. What breaks if two replicas share one PVC?"

#### Project C — "CI/CD & Progressive Delivery Pipeline to EKS"
Assignment 2, leveled up from kind → EKS + progressive delivery.
GitHub Actions builds/publishes on merge (tag = version + SHA) → deploys to EKS → controlled rolling update and a blue-green / canary release → automated rollback on failed health check. The entire release history must be reconstructable from git + Actions run logs.
- AI-proof core: their GitHub Actions history must show real green runs dated across the term; a burst the night before is a tell. Live: trigger a release, then force a failure and show the rollback.
- Oral: "Trigger a deploy right now and explain each stage. Make it fail — show the rollback. Where are your registry creds and why aren't they in the repo?"

#### Project D — "Secure & Observable Microservice on EKS"
Ties Week 10 Secrets → Week 12 RBAC → Week 13 HPA into one capstone.
Deploy a small app on EKS and harden + instrument it: image-scan gate in CI (scout/trivy), non-root + cap-drop + no-new-privileges, K8s Secrets (no plaintext), RBAC least-privilege service account, NetworkPolicy, plus HPA (+ metrics-server or Prometheus/Grafana). Then run load + failure drills showing self-healing and autoscaling.
- AI-proof core: security/scaling evidence must come from their cluster — `kubectl auth can-i` outputs, `describe` showing dropped capabilities, scan reports with real CVE counts on their image, a live load test that visibly scales the HPA.
- Oral: "Prove your service account cannot delete pods in another namespace. Run your load test and show HPA scale-out. Which CVEs did your scan find, and which did you fix and how?"

#### Project E (optional, ops-only) — "Scaling & Cost Engineering on EKS"
Deploy an app, drive HPA (+ cluster autoscaling), load-test to trigger scale-out/in, and produce a real AWS cost analysis + teardown-discipline report proving they operated within the Learner Lab budget. Almost zero coding — pure cloud/K8s operation. Good as a lighter or solo option.

### Recommendation
Make Project A the default flagship (truest "portable technologies" story, widest defensible integration), and offer B / C / D as alternative tracks so teams self-select and answers can't be shared. All four run on Cloud9 + Learner Lab if you enforce short-lived EKS clusters and a teardown report.
