# Report: Week 12, fix of the 12 defects of report #11

**Date**: 2026-10-31
**Sequence**: #12 for the day

## Summary
I fixed 11 of the 12 defects of report #11, and part of the twelfth. The lecture is now v5, the
lab is now v4, and the Blackboard text is now v4. **The work is not complete.** The AWS session
expired (`ExpiredToken`), so lab v4 and the slide 6 and slide 8 manifests have no live test.
The two `terraform output` commands also wait for this test. Until it passes, do not treat
these files as final.

## What Changed

**Created**
- `build_week12_lecture_v5.py`, `Week12/Lecture_week12_v5.pptx` and `.pdf`.
- `build_week12_lab_v4.py`, `Week12/Lab_week12_v4.pptx` and `.pdf`, `Week12/localMachine_v4.sh`.
- `Week12/Lab_week12_Blackboard_Submission_v4.md`.

**Changed**
- `~/Documents/c/r/CLO835_Fall_2026/Week12`, not committed: `localMachine.sh`,
  `cleanup_lab12.sh`, `master-init.sh.tftpl`.
- Memory: `project-week12-deck.md`, `MEMORY.md`, and the new `reference-pdf-from-powerpoint.md`.

Earlier versions stay as they are.

## Fixes

| No | Status | Fix |
|---|---|---|
| 1 | Fixed | Slide 11: "Step 2 has 3 methods". Slide 14: "A Secret uses the same 2 steps:". Slide 15: "Step 2 has the same 3 methods as a ConfigMap". |
| 2 | Fixed | Slide 13 says that etcd stores the Secret. Slide 15 says that it is not encrypted. Slide 18 has no etcd bullet. |
| 3 | Fixed | One word now: "command-line arguments", "executable", "Pod manifest", "methods", "stores", and "inject" for data. "Pass" is for arguments only. |
| 4 | Fixed | Slide 3: "Week 5: K8s – Pods, ReplicaSets". |
| 5 | Fixed, no live test | Slides 6 and 8 hold full manifests, `generic-pod.yaml` and `fortune-env.yaml`. Slide 6 uses `maziar/alpine-curl`. |
| 6 | Fixed | Slide 4 has a bullet on `nginx.conf`. Slide 5: "Two Dockerfile instructions set what a container runs:". Slide 8: one parent and one child bullet, with no "Problems:". |
| 7 | Fixed | Slide 14: the base64 bullet is one level below Declarative. |
| 8 | Fixed | PowerPoint made both PDFs. `pdffonts` shows only Calibri and Consolas, and the columns align. |
| 9 | Fixed | Lab slide 7: "On the node, the volume is in memory (tmpfs), not on the disk." |
| 10 | Fixed, no live test | Step 4 creates `app-secret` with `--from-file=DB_Password`. `secret-pod.yaml` has `envFrom` with `secretRef`. `printenv` shows both keys. |
| 11 | Fixed | `tee` writes each manifest and shows it, so 5 lines have a command. The rubric table is below: 53 rows, 0 empty cells. |
| 12 | Part fixed | `docker run` passed. `terraform output public_ips` and `private_ips` wait for AWS. |

## Slide 5 test
- I ran `docker run -it docker.io/maziar/fortune:args 15` exactly as the slide shows it, with a real terminal.
- Output: "Configured to generate new fortune every 15 seconds", then 4 writes, 15 to 16 seconds apart.
- Docker Desktop was off, so the test started it, then closed it.
- On this Apple Silicon computer, Docker shows a platform warning, because the image is `linux/amd64`.
- Your 15 containers stay as they were. The test removed its own container and the image `maziar/fortune:args`.

## Results

**Offline check of the final files**

| Check | Lecture v5 | Lab v4 |
|---|---|---|
| Slides, footers | 21, `N / 21` | 10, `N / 10` |
| Size | 0.18 MB | 0.07 MB |
| Fonts in the `.pptx` and in the PDF | Calibri, Consolas | Calibri, Consolas |
| Float coordinates, shapes off the canvas | 0, 0 | 0, 0 |
| Duplicate titles, duplicate bullets | 0, 0 | 0, 0 |
| Non-ASCII characters in Consolas text | 0 | 0 |
| Images | Logo and whale only | Whale only |

- I read each line of `PREFERENCES.md` again, with no output cut. I viewed all 31 pages of the PowerPoint PDFs.
- PowerPoint is the first render with the real fonts. No terminal line wraps, and no shape meets the footer.
- A search finds 0 uses of "options", "parameters", "keeps", "ways", "description", "PODs", "K8s-", "never on disk", and `process` as a word for the executable.
- `etcd` is in the bullets of slides 13 and 15 only.
- Slide 2 repeats the title of slide 4 as an agenda line, and slides 9 and 20 both have the label "configMap volume". I do not count these as bullets on two slides.
- `localMachine.sh` in the clone equals `Week12/localMachine_v4.sh`. `bash -n` and `terraform fmt -check` pass.
- The lab has 43 commands, 1 more than v3.
- No server started on this computer, so no port is used.

## Not done

**Live test.** The driver is ready at
`/private/tmp/claude-501/-Users-maziar-Downloads-k8s-week3/4b692c4c-a5fe-4559-849f-f6432d702f32/scratchpad/w12a/live12b.sh`. It:
- runs `terraform output public_ips` and `terraform output private_ips` exactly;
- runs 2 full passes of lab v4, 43 commands each;
- reads the manifests and commands of the lecture from the `.pptx` file, so it runs what the slides show;
- runs a recovery test that includes the new file `DB_Password`;
- destroys all resources.

## Issues / Notes

**New findings, not changed**
- Lecture slides 11 and 15, "inject methods": the volume block shows `volumes:` with no `volumeMounts:`. These are parts of a manifest, so they cannot run alone, and the mount is not shown. This was not in the 12 defects.
- Lecture slide 20 shows `emptyDir` with 2 containers, and the lab does not practise this. Week 07 covers it, and slide 20 is a summary.

**Other**
- Slide 3 of Week 12 now says "K8s – Pods". Week 10 v9 still says "K8s- PODs".
- The PDFs of earlier weeks still use Carlito and Linux Libertine G.
- `git pull` on lab slide 3 gives lab v2 until you push.
- The outlines of Weeks 01-03, 06, 13 and 14 still differ on Weeks 14 and 15.
- The Blackboard name of this lab is your decision.

## Rubric table

Each row is one "You must" line of `Lab_week12_Blackboard_Submission_v4.md`. A script checked that each
command is on the named slide.

| Rubric line | Exact command or source |
|---|---|
| Run terraform init and terraform apply. | Lab 3: `terraform init` ; Lab 3: `terraform apply` |
| Run terraform output public_ips and terraform output private_ips, and show the addresses of all three nodes. | Lab 3: `terraform output public_ips` ; Lab 3: `terraform output private_ips` |
| Show an SSH session connected to the control-plane node. | Lab 3: `ssh -i <your-key>.pem ubuntu@<masternode-public-ip>` |
| Run kubectl get nodes -o wide and show all three nodes in the Ready state. | Lab 3: `kubectl get nodes -o wide` |
| Run kubectl get pods -n kube-system and show the control-plane pods in the Running state. | Lab 3: `kubectl get pods -n kube-system` |
| Explain why you do not put configuration data in a container image. | Lecture 4 |
| Create the week12 namespace. | Lab 4: `kubectl create namespace week12` |
| Create fortune-args.yaml and display its contents. | Lab 4: `tee fortune-args.yaml <<'EOF'` |
| Apply the manifest and wait until the fortune-args Pod is Ready. | Lab 4: `kubectl apply -f fortune-args.yaml -n week12` ; Lab 4: `kubectl wait --for=condition=Ready pod/fortune-args -n week12 --timeout=120s` |
| Run kubectl logs fortune-args -n week12 --tail=4 and show the fortunes. | Lab 4: `kubectl logs fortune-args -n week12 --tail=4` |
| Explain the difference between ENTRYPOINT and command, and between CMD and args. | Lecture 6 |
| Create the app-config ConfigMap with the --from-literal options. | Lab 5: `kubectl create configmap app-config -n week12` |
| Create app.properties, then create the app-file ConfigMap with --from-file, and show the result. | Lab 5: `app.properties` ; Lab 5: `kubectl create configmap app-file -n week12 --from-file=app.properties -o yaml` |
| Create config-env.yaml and display its contents. | Lab 5: `tee config-env.yaml <<'EOF'` |
| Apply the manifest and wait until the config-env Pod is Ready. | Lab 5: `kubectl apply -f config-env.yaml -n week12` ; Lab 5: `kubectl wait --for=condition=Ready pod/config-env -n week12 --timeout=120s` |
| Run the printenv command for GREETING, COLOR, APP_COLOR and APP_MODE, and show the values. | Lab 5: `printenv GREETING COLOR APP_COLOR APP_MODE` |
| Explain the difference between --from-literal and --from-file. | Lecture 10 |
| Explain the difference between env, configMapKeyRef and envFrom. | Lecture 11 |
| Create config-volume.yaml and display its contents. | Lab 6: `tee config-volume.yaml <<'EOF'` |
| Apply the manifest and wait until the config-volume Pod is Ready. | Lab 6: `kubectl apply -f config-volume.yaml -n week12` ; Lab 6: `kubectl wait --for=condition=Ready pod/config-volume -n week12 --timeout=120s` |
| Run the ls and cat commands on /etc/app-config, and show the value of APP_COLOR. | Lab 6: `-- ls /etc/app-config` ; Lab 6: `-- cat /etc/app-config/APP_COLOR; echo` |
| Change APP_COLOR to green using kubectl patch. | Lab 6: `kubectl patch configmap app-config -n week12` |
| Wait 90 seconds, then show the new value in the file. | Lab 6: `sleep 90; kubectl exec config-volume -n week12 -- cat /etc/app-config/APP_COLOR; echo` |
| Show that APP_COLOR in the config-env Pod is still blue. | Lab 6: `kubectl exec config-env -n week12 -- printenv APP_COLOR` |
| Explain why the file changes and the environment variable does not change. | Lab 6: `A variable never changes in a running Pod.` |
| Create the DB_Password file, then create the app-secret Secret with --from-literal and --from-file. | Lab 7: `printf 'paswrd' > DB_Password` ; Lab 7: `--from-literal=DB_Host=mysql --from-file=DB_Password` |
| Read DB_Password with the jsonpath command and base64 -d. | Lab 7: `kubectl get secret app-secret -n week12 -o jsonpath='{.data.DB_Password}' \| base64 -d; echo` |
| Create secret-pod.yaml and display its contents. | Lab 7: `tee secret-pod.yaml <<'EOF'` |
| Apply the manifest and wait until the secret-pod Pod is Ready. | Lab 7: `kubectl apply -f secret-pod.yaml -n week12` ; Lab 7: `kubectl wait --for=condition=Ready pod/secret-pod -n week12 --timeout=120s` |
| Show DB_Password and DB_Host as variables, and DB_Host as a file. | Lab 7: `printenv DB_Password DB_Host` ; Lab 7: `-- cat /etc/secret-volume/DB_Host; echo` |
| Run the mount command, and show that the Secret volume is tmpfs. | Lab 7: `kubectl exec secret-pod -n week12 -- mount \| grep secret-volume` |
| Run the ls command on /var/run/secrets/kubernetes.io/serviceaccount and show the 3 files. | Lab 7: `-- ls /var/run/secrets/kubernetes.io/serviceaccount` |
| Run kubectl get secrets -n week12 and show that no Secret holds the token. | Lab 7: `kubectl get secrets -n week12` |
| Explain the difference between secretKeyRef and secretRef. | Lab 7: `secretKeyRef reads one key. secretRef injects every key.` |
| Explain why base64 is not encryption. | Lab 7: `base64 is an encoding, not encryption.` |
| Explain what tmpfs protects, and what it does not protect. | Lecture 18 ; Lecture 13 |
| Explain which permissions the default ServiceAccount has. | Lecture 16 |
| Create config-dev.yaml and display its contents. | Lab 8: `tee config-dev.yaml <<'EOF'` |
| Apply the manifest using kubectl apply -f config-dev.yaml. | Lab 8: `kubectl apply -f config-dev.yaml` |
| Apply config-env.yaml in the week12-dev namespace and wait until the Pod is Ready. | Lab 8: `kubectl apply -f config-env.yaml -n week12-dev` ; Lab 8: `kubectl wait --for=condition=Ready pod/config-env -n week12-dev --timeout=120s` |
| Run the printenv command in week12-dev, and show red and dev. | Lab 8: `kubectl exec config-env -n week12-dev -- printenv APP_COLOR APP_MODE` |
| Read DB_Password of the Secret in week12-dev. | Lab 8: `kubectl get secret app-secret -n week12-dev` |
| Set the ETCD variable, as the lab shows. | Lab 8: `ETCD="etcdctl --endpoints=https://127.0.0.1:2379` |
| Run the etcdctl get command for the Secret, and show paswrd in the output. | Lab 8: `get /registry/secrets/week12/app-secret \| grep -a -o paswrd` |
| Explain why config-dev.yaml holds a base64 value in the data field of the Secret. | Lecture 14 |
| Explain how the same Pod manifest gets different values in the two namespaces. | Lecture 12 |
| Explain two ways to protect a Secret. | Lab 8: `Protect it: encryption at rest, RBAC, or an external secret store.` |
| Run bash cleanup_lab12.sh on the control-plane node. | Lab 9: `bash cleanup_lab12.sh` |
| Run kubectl get namespaces \| grep week12 and show that nothing is left. | Lab 9: `kubectl get namespaces \| grep week12` |
| From the Week 12 directory on your own machine, run terraform destroy. | Lab 9: `terraform destroy` |
| Include the final Terraform output showing Destroy complete!. | Lab 9: `terraform destroy` |
| State the number of resources Terraform removed. | Lab 9: `terraform destroy` |
| Explain why the deletion of a namespace removes the Pods, ConfigMaps and Secrets in it. | cleanup_lab12.sh: `kubectl delete namespace week12 week12-dev` |
