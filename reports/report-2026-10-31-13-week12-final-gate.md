# Report: Week 12, final investigation, fixes and gate

**Date**: 2026-10-31
**Sequence**: #13 for the day

## Summary
The gate result is 1: 101 of 101 checks pass. The final files are lecture v6, lab v5 and the
Blackboard text v5. The lab passed 2 live passes of 40 commands each, with 0 non-zero exits.
All lecture commands ran from the deck, in slide order. All 15 resources are destroyed. One
command stays untested: `git pull` on lab slide 3 gives lab v5 only after your push.

## Why the defects came in rounds
- I checked only `PREFERENCES.md`, and only the lines that I remembered. I did not read `PROMPT.md`, `DESIGN_LANGUAGE.md`, the Week 05 audit or the feedback rules for these checks.
- I checked by eye and by short scripts, with no pass-or-fail gate.
- I read PDFs from LibreOffice, not with the real fonts.
- I said "fixed" when I had fixed a list. The list was not the standard.
- No independent reader saw the work. The 2 reviewers of this round found 30 defects that I missed.

Now the check is a script: `gate_week12.py` prints GATE 1 only when every check passes.

## What Changed

**Created**
- `build_week12_lecture_v6.py`, `Week12/Lecture_week12_v6.pptx` and `.pdf`.
- `build_week12_lab_v5.py`, `Week12/Lab_week12_v5.pptx` and `.pdf`, `Week12/localMachine_v5.sh`.
- `Week12/Lab_week12_Blackboard_Submission_v5.md`.
- `Week12/assets/kube-flannel-v0.28.10.yml`, the Flannel manifest with the `maziar` images.
- `gate_week12.py`, the pass-or-fail gate.

**Changed**
- `~/Documents/c/r/CLO835_Fall_2026/Week12`, not committed: `localMachine.sh`,
  `cleanup_lab12.sh`, `master-init.sh.tftpl`.
- Memory: `project-week12-deck.md`, `project-short-labs-2026-10-27.md`,
  `project-clo835-fall2026-repo.md`, `feedback-no-all-fixed-claim.md`, `MEMORY.md`.

Earlier versions stay as they are.

## Lecture changes in v6

| Area | Change | Rule |
|---|---|---|
| Run in order | Slides 10, 11, 14, 15, 16 and 18 now run in slide order, in one namespace, with no name collision. | Commands run as shown |
| Files | Slides 10 and 14 create the file that `--from-file` reads. | Commands run as shown |
| Agreement | Slide 14 has 2 keys, as slide 16 and the lab show. Declarative slides use `kubectl apply`. `secret-pod` has the container and the image of the lab. | Lecture and lab agree |
| Facts | Slide 8: the kubelet injects environment variables for the Services that exist when the Pod starts, and for the API server. Slide 14: `data` and `stringData`. Slide 13: base64 is not encryption. | Every fact correct |
| Repetition | Removed from slides 13, 14, 19 and 7. The etcd points are on slides 13 and 15, and tmpfs is on slide 18. | State a point one time |
| Language | One word: object, three files, volume, environment variable, configuration data, stores, Secret manifests. Active voice on slides 15 and 18. | ASD-STE100 |
| Summary | Slide 20 uses `app-config`, `app-secret`, `/etc/app-config` and `/etc/secret-volume`. | Lecture and lab agree |
| Terminals | `$` on each command, cyan continuation lines, 9 pt or more, real output on slides 16 and 18. | DESIGN_LANGUAGE.md |
| Layout | All content above y = 6.70. Body text 12 pt or more. Inline code is Consolas, bold, Slate. Small numbers in words. | DESIGN_LANGUAGE.md |
| Palette | The red Week 11 tile is now ALERT_RED `E74C3C`. | Stay in palette |
| File | Title and author set. Blank thumbnail removed. | Quality |

## Lab changes in v5

| Area | Change | Rule |
|---|---|---|
| Size | 40 commands, from 43. | Lab size limit |
| Flannel | The master writes `/root/kube-flannel.yml`. The cluster ran `maziar/flannel:v0.28.10`. | Only `maziar` and `sojoudian` |
| Coverage | Step 2 and Step 4 use `--from-file`. Step 4 uses `secretRef`. Step 2 shows `KUBERNETES_SERVICE_HOST`. | Practise every topic |
| Agreement | Each Pod sets `command` and `args`, as the lecture does. | Lecture and lab agree |
| Etcd | Step 5 reads the Secret of `week12-dev`, so the lab now uses that Secret. | Quality |
| Answers | Each Explain line has its answer on a slide. The comments now give the reason. | Rubric must be runnable |
| Facts | `| head -4` shows the interval line. `sleep 120` gives the kubelet time. The tmpfs comment says "on the node". | Every fact correct |
| Display | `tee` writes each manifest and shows it, with no new command. | Rubric must be runnable |
| Blackboard | 51 rows, 0 empty cells. The text matches the lab, in order. | Rubric must be runnable |

## Live test
- Account `499333804030`, `us-east-1`, key pair `Maziar`. Student prompts for `key_name` and `yes`.
- `terraform apply`: 15 added. All 3 nodes Ready 2 minutes after the start.
- `terraform output public_ips` and `terraform output private_ips` both ran as shown.
- Kubernetes v1.35.10. `cleanup_lab12.sh` on the master equals the repository file.
- Pass 1 and pass 2: 40 commands each, 0 non-zero exits.
- Recovery test: clean-up from a half-way state returned 0 in 43 seconds, and left 0 namespaces.
- `terraform destroy`: 15 destroyed. After it: 0 instances and 0 `week12` security groups.
- Slide 5 `docker run`: passed earlier as shown, 15 seconds apart. The slide and the image did not change.

**Results that prove the text**
- `printenv` gave `hello`, `blue`, `blue`, `prod`, `debug`, `10.96.0.1`.
- `kubectl logs` gave "Configured to generate new fortune every 2 seconds", then lines 2 seconds apart.
- After the patch, the file said `green`, and the environment variable said `blue`.
- `mount` gave `tmpfs on /etc/secret-volume`, and slide 18 shows this line.
- `etcdctl get` gave `dev-pass` for the Secret of `week12-dev`.

**After the test**
- Comments and the Blackboard text changed. The gate proves that the tested commands equal the final commands.
- A diff proves that the lecture manifests and commands equal the tested files.

## Results
- `gate_week12.py`: GATE 1, 101 of 101. It covers both decks, both PDFs, the repository, the Blackboard text and the live logs.
- Both PDFs come from PowerPoint, and `pdffonts` shows Calibri and Consolas only.
- I viewed all pages from PowerPoint with the real fonts.
- The registry shows that slide 5 matches the image: `apt-get update ; apt-get -y install fortune`, `ENTRYPOINT`, `CMD ["10"]`.
- All 6 links of slide 21 return 200.
- No commit and no push. The clone holds `Week12` for your git step.
- No server started on this computer, so no port is used.

## Reviewer items that I did not apply
- Slide 16 keeps 2 Secret rows. This is the real output when the slides run in order, and the lab comment is about its own namespace.
- "Set" stays for a person who writes a value in a manifest. "Inject" stays on slides 4, 10 and 14, as the source says.
- The comment `calls ./cleanup_lab12.sh` stays, because it is shared template wording.
- `tmpfs`, `etcd`, `kubelet` and `base64` stay in Calibri, as names of things.

## Issues / Notes

**Limits of this result**
- `git pull` on lab slide 3 gives lab v5 only after your push.
- I did not view the decks in Keynote, because this computer has only PowerPoint.
- The reviewers did not read the last small fixes. The gate and the live test cover them.
- When slide 14 runs in order, `kubectl apply` shows a harmless warning about the missing annotation.
- On Apple Silicon, `docker run` shows a platform warning, because the image is `linux/amd64`.

**Other weeks, not changed**
- Weeks 04 to 11, 13 and 14 still apply Flannel from `flannel-io`. This breaks your account rule. `sojoudian/flannel` and `sojoudian/clo835-mirrors` return 404.
- The PDFs of earlier weeks use Carlito and Linux Libertine G.
- Week 10 v9 still says "K8s- PODs". The outlines of Weeks 01-03, 06, 13 and 14 differ on Weeks 14 and 15.
- Weeks 07 and 14 still name `busybox`.

**Your decision**
- The Blackboard name of this lab.

## Rubric table

Each row is one "You must" line of `Lab_week12_Blackboard_Submission_v5.md`. A script checked that each
command or answer is on the named slide.

| Rubric line | Exact command or source |
|---|---|
| Run terraform init and terraform apply. | Lab 3: `terraform init` ; Lab 3: `terraform apply` |
| Run terraform output public_ips and terraform output private_ips, and show the addresses of all three nodes. | Lab 3: `terraform output public_ips` ; Lab 3: `terraform output private_ips` |
| Show an SSH session connected to the master node. | Lab 3: `ssh -i <your-key>.pem ubuntu@<masternode-public-ip>` |
| Run kubectl get nodes -o wide and show all three nodes in the Ready state. | Lab 3: `kubectl get nodes -o wide` |
| Run kubectl get pods -n kube-system and show the control-plane Pods in the Running state. | Lab 3: `kubectl get pods -n kube-system` |
| Explain why you do not put configuration data in a container image. | Lecture 4 |
| Create the week12 namespace. | Lab 4: `kubectl create namespace week12` |
| Create fortune-args.yaml and show its contents. | Lab 4: `tee fortune-args.yaml <<'EOF'` |
| Apply the manifest and wait until the fortune-args Pod is Ready. | Lab 4: `kubectl apply -f fortune-args.yaml -n week12` ; Lab 4: `kubectl wait --for=condition=Ready pod/fortune-args -n week12 --timeout=120s` |
| Run kubectl logs fortune-args -n week12 \| head -4, and show the interval of 2 seconds. | Lab 4: `kubectl logs fortune-args -n week12 \| head -4` |
| Explain the difference between ENTRYPOINT and command, and between CMD and args. | Lecture 6 |
| Create the LOG_LEVEL file, then create the app-config ConfigMap with --from-literal and --from-file. | Lab 5: `printf 'debug' > LOG_LEVEL` ; Lab 5: `--from-file=LOG_LEVEL` |
| Create config-env.yaml and show its contents. | Lab 5: `tee config-env.yaml <<'EOF'` |
| Apply the manifest and wait until the config-env Pod is Ready. | Lab 5: `kubectl apply -f config-env.yaml -n week12` ; Lab 5: `kubectl wait --for=condition=Ready pod/config-env -n week12 --timeout=120s` |
| Run the printenv command for GREETING, COLOR, APP_COLOR, APP_MODE, LOG_LEVEL and KUBERNETES_SERVICE_HOST, and show the values. | Lab 5: `printenv GREETING COLOR APP_COLOR APP_MODE LOG_LEVEL KUBERNETES_SERVICE_HOST` |
| Explain the difference between --from-literal and --from-file. | Lab 5: `--from-file makes one key from a file. The file name is the key.` |
| Explain the difference between env, configMapKeyRef and envFrom. | Lab 5: `env sets one value. configMapKeyRef reads one key.` |
| Create config-volume.yaml and show its contents. | Lab 6: `tee config-volume.yaml <<'EOF'` |
| Apply the manifest and wait until the config-volume Pod is Ready. | Lab 6: `kubectl apply -f config-volume.yaml -n week12` ; Lab 6: `kubectl wait --for=condition=Ready pod/config-volume -n week12 --timeout=120s` |
| Run the ls and cat commands on /etc/app-config, and show the value of APP_COLOR. | Lab 6: `-- ls /etc/app-config` ; Lab 6: `-- cat /etc/app-config/APP_COLOR; echo` |
| Change APP_COLOR to green using kubectl patch. | Lab 6: `kubectl patch configmap app-config -n week12` |
| Wait 2 minutes, then show the new value in the file. | Lab 6: `sleep 120; kubectl exec config-volume -n week12 -- cat /etc/app-config/APP_COLOR; echo` |
| Show that APP_COLOR in the config-env Pod is still blue. | Lab 6: `kubectl exec config-env -n week12 -- printenv APP_COLOR` |
| Explain why the file changes and the environment variable does not change. | Lab 6: `The kubelet updates the file in about a minute.` ; Lab 6: `An environment variable gets its value when the container starts.` ; Lab 6: `It does not change while the container runs.` |
| Create the DB_Password file, then create the app-secret Secret with --from-literal and --from-file. | Lab 7: `printf 'paswrd' > DB_Password` ; Lab 7: `--from-literal=DB_Host=mysql --from-file=DB_Password` |
| Read DB_Password with the jsonpath command and base64 -d. | Lab 7: `kubectl get secret app-secret -n week12 -o jsonpath='{.data.DB_Password}' \| base64 -d; echo` |
| Create secret-pod.yaml and show its contents. | Lab 7: `tee secret-pod.yaml <<'EOF'` |
| Apply the manifest and wait until the secret-pod Pod is Ready. | Lab 7: `kubectl apply -f secret-pod.yaml -n week12` ; Lab 7: `kubectl wait --for=condition=Ready pod/secret-pod -n week12 --timeout=120s` |
| Show DB_Password and DB_Host as environment variables, and DB_Host as a file. | Lab 7: `printenv DB_Password DB_Host` ; Lab 7: `-- cat /etc/secret-volume/DB_Host; echo` |
| Run the mount command, and show that the Secret volume is tmpfs. | Lab 7: `kubectl exec secret-pod -n week12 -- mount \| grep secret-volume` |
| Run the ls command on /var/run/secrets/kubernetes.io/serviceaccount and show the three files. | Lab 7: `-- ls /var/run/secrets/kubernetes.io/serviceaccount` |
| Run kubectl get secrets -n week12 and show that no Secret holds the token. | Lab 7: `kubectl get secrets -n week12` |
| Explain the difference between secretKeyRef and secretRef. | Lab 7: `secretKeyRef reads one key. secretRef injects every key.` |
| Explain why base64 is not encryption. | Lab 7: `Anyone can decode it, with no key.` |
| Explain what tmpfs protects, and what it does not protect. | Lecture 18 ; Lecture 13 |
| Explain which permissions the default ServiceAccount has. | Lecture 16 |
| Explain why an environment variable is not the recommended method for a Secret. | Lecture 19 |
| Create config-dev.yaml and show its contents. | Lab 8: `tee config-dev.yaml <<'EOF'` |
| Apply the manifest using kubectl apply -f config-dev.yaml. | Lab 8: `kubectl apply -f config-dev.yaml` |
| Apply config-env.yaml in the week12-dev namespace and wait until the Pod is Ready. | Lab 8: `kubectl apply -f config-env.yaml -n week12-dev` ; Lab 8: `kubectl wait --for=condition=Ready pod/config-env -n week12-dev --timeout=120s` |
| Run the printenv command in week12-dev, and show red and dev. | Lab 8: `kubectl exec config-env -n week12-dev -- printenv APP_COLOR APP_MODE` |
| Set the ETCD shell variable, as the lab shows. | Lab 8: `ETCD="etcdctl --endpoints=https://127.0.0.1:2379` |
| Run the etcdctl get command for the Secret of week12-dev, and show dev-pass in the output. | Lab 8: `get /registry/secrets/week12-dev/app-secret \| grep -a -o dev-pass` |
| Explain why config-dev.yaml holds a base64 value in the data field of the Secret. | Lecture 14 |
| Explain how the same Pod manifest gets other values in the second namespace. | Lecture 12 |
| Explain two ways to protect a Secret. | Lab 8: `Protect it: encryption at rest, RBAC, or an external secret store.` |
| Run bash cleanup_lab12.sh on the master node, and show that both namespaces are deleted. | Lab 9: `bash cleanup_lab12.sh` |
| From the Week12 folder on your own machine, run terraform destroy. | Lab 9: `terraform destroy` |
| Include the final Terraform output showing Destroy complete!. | Lab 9: `terraform destroy` |
| State the number of resources Terraform destroyed. | Lab 9: `terraform destroy` |
| Explain why the deletion of a namespace deletes the Pods, ConfigMaps and Secrets in it. | Lab 9: `Each Pod, ConfigMap and Secret belongs to one namespace. Kubernetes deletes them with it.` |
