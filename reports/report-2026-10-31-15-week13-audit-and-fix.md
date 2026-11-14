# Report: Week 13, audit against the rules, fixes and gate

**Date**: 2026-10-31
**Sequence**: #15 for the day

## Summary
The result for release is 0 at this time. The file gate gives GATE 1, 119 of 119, but the live test of the new lab and lecture commands did not run. Your prompt did not ask for a cloud resource, so I created none. The final files are lecture v8, lab v3 and the Blackboard text v3. `Week13_lecture_style_v7` and lab v2 had defects that stop a release. Nothing is committed and nothing is pushed.

## What Changed

**Created**
- `build_week13_lecture_v8.py`, `week13/Lecture_week13_v8.pptx` and `.pdf` (26 slides, 0.2 MB).
- `build_week13_lab_v3.py`, `week13/Lab_week13_v3.pptx` and `.pdf` (10 slides), `week13/localMachine_v3.sh` (40 commands).
- `week13/Lab_week13_Blackboard_Submission_v3.md`, in the long form (53 rows).
- `gate_week13.py`, the pass-or-fail gate.

**Changed**
- `~/Documents/c/r/CLO835_Fall_2026/Week13`, not committed: `localMachine.sh`, `cleanup_lab13.sh`, `master-init.sh.tftpl`.
- Memory: `project-week13-deck.md`, `project-short-labs-2026-10-27.md`, `project-clo835-fall2026-repo.md`, `feedback-blackboard-lab-text-long-form.md`, `MEMORY.md`.

Earlier versions stay as they are.

## Defects found in lecture v7 and lab v2

| Area | Defect | Rule |
|---|---|---|
| Cover | The cover said "Week 11 · Lecture" and promised IRSA. No slide teaches IRSA. Week 14 has it. | Follow the schedule |
| Outline | Week 11 and Week 12 were swapped, Week 8 had no number, "AKS", "K8s- K8s-", two Week 14 tiles, and Week 1 was blue. | Outline follows the schedule |
| Agenda | ClusterRoles and default roles were on the agenda, with no slide. | Lecture teaches its agenda |
| Pictures | 11 outside screenshots, 3.2 MB. One had a pink third-party style, and one had worker names of another cluster. | No third-party screenshot, near 1 MB |
| Privacy | `irinag:~/environment $` was in a terminal. | No private name |
| Commands | `Curl http://localhost:6443 –k` had an EN DASH, the wrong scheme, and fails with 403. `resources: ["ConfigMap"]` gives no permission. `kubectl create -f` differed from the lab. | Every command runs as shown |
| Facts | A broken sentence on ServiceAccounts, `System:unauthenticated`, an invalid account number. The aws-auth ConfigMap had no note that AWS marks it as deprecated. | Every fact correct |
| Language | "Kuberntes", "serviceaccoount", "recourse", "healh", "Sas", "Devs", contractions. | ASD-STE100 |
| File | Author "Steve Canny", no title. | Quality |
| Lab label | "Lab 13", sample v1.35.9. | Label and version |
| Lab coverage | No group, no ClusterRole, no default role, no API path. | Lab practises the lecture |
| Lab files | `cat >` hid each manifest. Flannel came from `flannel-io`, and its images from `ghcr.io`. | Only `maziar` and `sojoudian` |
| Blackboard | Short form with a pledge. | Long form |
| PDF | Carlito and Linux Libertine G. | PowerPoint PDF |

## Lecture changes in v8
- 14 native diagrams replace the screenshots. Only the logo and the whale stay as images.
- New slides: "A Client Certificate Is a User", "Reaching the API", "ClusterRoles and ClusterRoleBindings", "A ClusterRole for PersistentVolumes", "Default ClusterRoles and ClusterRoleBindings".
- Order: authentication, ServiceAccounts, API paths, authorization, RBAC, cluster-level RBAC, Amazon EKS.
- The outline equals the Week 12 outline, and Week 13 is the blue tile.
- Facts follow `kubernetes.io`, the `release-1.35` source and the AWS documents: `/logs` is gone, `/livez` and `/readyz` are in, the API server default is AlwaysAllow, kubeadm turns on RBAC, members of `system:masters` bypass RBAC, access entries are the method that AWS recommends, `aws eks get-token` replaces the old client tool, and the three authentication modes are named.
- The lecture Role equals the lab Role, line for line.

## Lab changes in v3
- 40 commands, Step 0 to Step 6.
- Added: `/version`, the anonymous 403, `kubectl proxy`, a binding for the group `developers` with the default ClusterRole `view`, the failed RoleBinding for a PersistentVolume, the ClusterRole and the ClusterRoleBinding.
- Removed to keep the limit: admin `auth whoami`, `get pods` after the Role, `can-i delete pods`, `can-i --list`, `can-i list services -n week13`, and two `get-contexts` commands.
- `tee` writes each manifest and shows it.
- `cleanup_lab13.sh` now deletes the ClusterRole and the ClusterRoleBinding.
- The master writes the Flannel manifest with the `maziar` images.

## Independent review
- Lab reviewer: 17 items. Lecture reviewer: 48 items. Second-pass reviewer on the fixes: 16 items.
- I applied each confirmed item, except the items below.
- The first gate failed on 4 checks. I fixed them.

**Items that I did not apply**
- Lab 5: `kubectl get clusterrolebinding cluster-admin` is not in the lab. The binding with `view` practises default roles, and the limit is 40. The lecture runs this command.
- Lab 14: `create configmap` as dev-user and `get serviceaccounts` are not in the lab, because the limit is 40.
- Lab 17: the NodePort comment stays. It is true, and it is shared template text.
- Lecture 23: no `aws eks create-access-entry` terminal, because no EKS exists here to test it.
- Lecture 33: no `$ vi` line. A comment says to save the two parts in one file.
- Lecture 39: no separate kubeconfig slide. The certificate slide has two bullets, and Week 14 teaches kubeconfig.
- Lecture 43: slide 21 keeps its diagram. It shows the flow, and slide 24 shows the parts.
- Lecture 44: itnext.io stays out, because it returned 403 to curl. The AWS and Kubernetes pages replace it.
- Second pass 7: the opening and closing Blackboard sentences stay. They are your own item text, the same as in Weeks 06 to 12.
- Second pass 12 and 13: "control-plane Pods" and "Verify Its Status" stay. They are your own Blackboard form.
- Changed in another place: Lab 13 asked for the group `dev-users`. I changed the lecture label to `developers`, because the tested lab uses this name.

## Technical Details
- `gate_week13.py` uses the deck checks of `gate_week12.py`, and it adds checks for the cover, the outline, the agenda, text below 6.70 in, the manifest match, the topics of the lab, the clean-up and the Blackboard text.
- Both PDFs come from PowerPoint. `pdffonts` shows Calibri and Consolas only.
- I read all lecture and lab pages from PowerPoint.
- All 8 reference links returned 200.
- All image tags exist on Docker Hub: `maziar/curl:latest`, `maziar/kubia:v1`, `maziar/flannel:v0.28.10`, `maziar/flannel-cni-plugin:v1.9.1-flannel3`.
- The AWS session is valid for account `499333804030`. I ran one read-only identity call.

## Results
- `gate_week13.py` with no live folder: GATE 1, 119 of 119.
- Rubric table: 53 rows, 0 empty cells.
- `terraform fmt` passes. The scan of the folder finds no home path, no key, no outside account.
- No server started on this computer, so no port is used.

## Issues / Notes

**Not done**
- The live test did not run. The driver is `/private/tmp/claude-501/-Users-maziar-Downloads-k8s-week3/4b692c4c-a5fe-4559-849f-f6432d702f32/scratchpad/w13/live13.sh`. It runs the lab 2 times, the lecture commands from the deck, a recovery test and destroy.
- No new command has run on a cluster: `kubectl proxy` in one line, the group binding, the failed RoleBinding, and the 22 lecture commands. "This step takes about 40 seconds" is an estimate until this test.
- No reviewer re-read the fixes of the second pass. The gate covers them.
- Lab v3 reaches students only after your push of the 3 files in the clone.
- I did not view the decks in Keynote.

**Limits by design**
- Slides on Amazon EKS have no lab step, because students have no EKS.

**Your decision**
- The Blackboard name of this lab.

**Other weeks, not changed**
- The Week 14 cover says "Week 12 · Lecture". Its agenda keeps IRSA as optional.

## Rubric table

Each row is one "You must" line of `Lab_week13_Blackboard_Submission_v3.md`. A script checked that each command or answer is on the named slide.

| Rubric line | Exact command or source |
|---|---|
| Run terraform init and terraform apply. | Lab 3: `terraform init` ; Lab 3: `terraform apply` |
| Run terraform output public_ips and terraform output private_ips, and show the addresses of all three nodes. | Lab 3: `terraform output public_ips` ; Lab 3: `terraform output private_ips` |
| Show an SSH session connected to the master node. | Lab 3: `ssh -i <your-key>.pem ubuntu@<masternode-public-ip>` |
| Run kubectl get nodes -o wide and show all three nodes in the Ready state. | Lab 3: `kubectl get nodes -o wide` |
| Run kubectl get pods -n kube-system and show the control-plane Pods in the Running state. | Lab 3: `kubectl get pods -n kube-system` |
| Explain the order of the three phases of a request in the API server. | Lecture 4: `Admission control can change or deny the request` |
| Create dev-user.key and dev-user.csr using the openssl commands. | Lab 4: `openssl genrsa -out dev-user.key 2048` ; Lab 4: `openssl req -new -key dev-user.key` |
| Create dev-user-csr.yaml and show its contents. | Lab 4: `tee dev-user-csr.yaml <<EOF` |
| Apply the manifest and approve the dev-user request. | Lab 4: `kubectl apply -f dev-user-csr.yaml` ; Lab 4: `kubectl certificate approve dev-user` |
| Run kubectl get csr dev-user and show Approved,Issued. | Lab 4: `# Approved,Issued` |
| Write the certificate to dev-user.crt. | Lab 4: `base64 -d > dev-user.crt` |
| Run the openssl x509 command, and show the subject and the end date. | Lab 4: `openssl x509 -in dev-user.crt -noout -subject -enddate` |
| Explain why Kubernetes does not store users. | Lab 4: `Kubernetes stores no users.` ; Lecture 5: `Kubernetes does not manage users.` |
| Explain what the CN and O fields of the certificate mean. | Lab 4: `CN is the user name. O is the group: developers.` |
| Create the week13 namespace. | Lab 5: `kubectl create namespace week13` |
| Add the dev-user credentials and the dev-user@kubernetes context to the kubeconfig file. | Lab 5: `kubectl config set-credentials dev-user` ; Lab 5: `kubectl config set-context dev-user@kubernetes` |
| Run the two curl commands on port 6443, and show the version and the 403 Forbidden answer. | Lab 5: `curl -k https://localhost:6443/version` ; Lab 5: `curl -k https://localhost:6443/apis` |
| Run the kubectl proxy command, and show the first lines of the APIGroupList. | Lab 5: `kubectl proxy --port=8001` |
| Run kubectl --context=dev-user@kubernetes auth whoami, and show the user and the group. | Lab 5: `kubectl --context=dev-user@kubernetes auth whoami` |
| Run kubectl --context=dev-user@kubernetes get pods, and show the Forbidden error. | Lab 5: `kubectl --context=dev-user@kubernetes get pods` |
| Explain the difference between authentication and authorization. | Lab 5: `Authentication: the API knows who dev-user is.` ; Lab 5: `Authorization: no Role lets dev-user list Pods yet.` |
| Explain why the curl command gets 403 Forbidden and the kubectl proxy request passes. | Lab 5: `With no credentials you are system:anonymous.` ; Lab 5: `kubectl proxy sends your credentials to the API server` |
| Explain why the auth whoami command passes and the get pods command fails. | Lab 5: `Every authenticated user can ask this.` ; Lab 5: `no Role lets dev-user list Pods yet` |
| Create developer-role.yaml and show its contents. | Lab 6: `tee developer-role.yaml <<'EOF'` |
| Apply the manifest using kubectl apply -f developer-role.yaml -n week13. | Lab 6: `kubectl apply -f developer-role.yaml -n week13` |
| As dev-user, create the web Pod. | Lab 6: `run web --image=maziar/kubia:v1` |
| As dev-user, try to delete the web Pod, and show the Forbidden error. | Lab 6: `delete pod web` |
| Create the developers-view RoleBinding using the kubectl create rolebinding command. | Lab 6: `kubectl create rolebinding developers-view --clusterrole=view --group=developers -n week13` |
| As dev-user, run the get services command, and show that no Forbidden error comes back. | Lab 6: `get services` |
| Explain the difference between a Role and a RoleBinding. | Lab 6: `The Role says what. The RoleBinding says who.` |
| Explain why the Role names configmaps and not ConfigMap. | Lab 6: `RBAC matches the name in the API path: configmaps, not ConfigMap.` |
| Explain how dev-user gets the permissions of the default ClusterRole view. | Lab 6: `The group of the certificate gets the default ClusterRole view.` |
| Create the clo835 ServiceAccount. | Lab 7: `kubectl create serviceaccount clo835 -n week13` |
| Create curl-sa.yaml and show its contents. | Lab 7: `tee curl-sa.yaml <<'EOF'` |
| Apply the manifest and wait until the curl-sa Pod is Ready. | Lab 7: `kubectl apply -f curl-sa.yaml -n week13` ; Lab 7: `kubectl wait --for=condition=Ready pod/curl-sa -n week13 --timeout=120s` |
| Run the curl command in the Pod, and show the Forbidden answer. | Lab 7: `curl -s --cacert $SA/ca.crt` |
| Explain how the Pod proves its identity to the API server. | Lab 7: `the token proves` |
| Explain why the API server answers Forbidden. | Lab 7: `No Role lets it list Services yet.` |
| Create service-reader.yaml and show its contents. | Lab 8: `tee service-reader.yaml <<'EOF'` |
| Apply the manifest using kubectl apply -f service-reader.yaml -n week13. | Lab 8: `kubectl apply -f service-reader.yaml -n week13` |
| Run the same curl command, and show the ServiceList. | Lab 8: `The same call now returns a ServiceList.` |
| Run kubectl auth can-i list services for the default namespace, and show no. | Lab 8: `kubectl auth can-i list services -n default` |
| Run the kubectl api-resources command, and show that NAMESPACED is false for persistentvolumes. | Lab 8: `kubectl api-resources --sort-by name \| grep -E 'NAMESPACED\|persistentvolumes'` |
| Create the pv-reader ClusterRole. | Lab 8: `kubectl create clusterrole pv-reader --verb=get,list --resource=persistentvolumes` |
| Create the pv-test RoleBinding, run kubectl auth can-i list persistentvolumes, and show no. | Lab 8: `kubectl create rolebinding pv-test --clusterrole=pv-reader` ; Lab 8: `# no` |
| Create the pv-test ClusterRoleBinding, run the same command, and show yes. | Lab 8: `kubectl create clusterrolebinding pv-test --clusterrole=pv-reader` ; Lab 8: `# yes` |
| Explain why the ServiceAccount gets the answer no in the default namespace. | Lab 8: `A Role and its RoleBinding work in one namespace only.` |
| Explain why a PersistentVolume needs a ClusterRoleBinding and not a RoleBinding. | Lab 8: `A RoleBinding does not grant access to a cluster-level resource.` ; Lecture 19: `To grant access to a cluster-level resource, always use a ClusterRoleBinding` |
| Run bash cleanup_lab13.sh on the master node, and show that only the kubernetes-admin context is left. | Lab 9: `bash cleanup_lab13.sh` ; Lab 9: `The output must show the context kubernetes-admin@kubernetes only.` |
| From the Week13 folder on your own machine, run terraform destroy. | Lab 9: `terraform destroy` |
| Include the final Terraform output showing Destroy complete!. | Lab 9: `terraform destroy` |
| State the number of resources Terraform destroyed. | Lab 9: `terraform destroy` |
| Explain why the deletion of the week13 namespace does not delete the CSR, the ClusterRole and the ClusterRoleBinding. | Lab 9: `A CSR, a ClusterRole and a ClusterRoleBinding have no namespace,` |
