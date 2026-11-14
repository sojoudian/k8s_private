# Report: Audit of the Week 07 and Week 10 lectures against the preferences and standards
**Date**: 2026-11-09
**Sequence**: #02 for the day

## Summary
Neither lecture meets the preferences and standards. The Week 07 lecture (`Week07/Lecture_week07_v6.pptx`) has 37 defects: 2 high, 8 medium and 27 low. The Week 10 lecture (`Week10/Lecture_week10_v9.pptx`) has 49 defects: 3 high, 15 medium and 31 low. The tables also give 18 additions for Week 07, 22 additions for Week 10 and 12 rule conflicts. This audit is read-only, and I changed no deck.

## What Changed
- Created this report. No project file, no deck and no repository file changed.

## Technical Details
- Rule sources read: `~/.claude/PREFERENCES.md`, both `CLAUDE.md` files, `PROMPT.md`, `DESIGN_LANGUAGE.md`, all `feedback-*` memories, the Week 05 audit of 2026-10-07 (the meaning of "my standards") and `gate_week12.py`.
- Gate: the deck checks of `gate_week12.py`, with ROOT set to each week. Week 07: 31 of 32 pass. Week 10: 22 of 32 pass.
- Two independent reviewers read every rule source, the decks in deck order, the PDF pages as pictures, the source decks, the labs and the Kubernetes v1.35 documentation. I merged their findings with my own pass and checked the high findings again.
- Checks that I made myself:
  - All slide images exist on Docker Hub: `maziar/kubia:0.1`, `maziar/kubia:v1`, `maziar/fortune:env`, `maziar/alpine-git:latest` and `maziar/alpine-curl:latest`.
  - `sojoudian/kubia` has the branch `master` and the file `app.js`.
  - Week 07 PDF: Quartz (macOS), Calibri and Consolas. Week 10 PDF: LibreOffice 26.8.1.1, Carlito and LinuxLibertineG.
  - Week 07 lab step 5 installs the local-path provisioner as the StorageClass `standard`, and uses `busybox:1.36`.

## Results

```
TABLE 1 - Week 07 lecture (Week07/Lecture_week07_v6.pptx, 15 slides): defects
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| #   | Slide    | Sev  | Type   | Issue (evidence)                             | Fix                                |
+=====+==========+======+========+==============================================+====================================+
| 1   | 4, 10    | HIGH | FACT   | "A volume follows / has the same lifecycle   | Say: an emptyDir, configMap or     |
|     |          |      |        | as its Pod". Only an ephemeral volume does.  | secret volume ends with its Pod.   |
|     |          |      |        | PV, NFS and hostPath data stay after the     | Persistent storage stays. [V]      |
|     |          |      |        | Pod. Slide 10 bullet 6 says the opposite.    |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 2   | 2, 7, 14 | HIGH | LAB    | The lab practises hostPath (step 4) and a    | Add a hostPath slide and a PVC +   |
|     |          |      |        | PVC with the StorageClass standard (step 5). | standard StorageClass slide from   |
|     |          |      |        | The lecture has 1 hostPath bullet, no        | the lab manifests, or move lab     |
|     |          |      |        | hostPath manifest, and only an EBS PVC that  | steps 4-5 to Week 10.              |
|     |          |      |        | cannot run on the lab cluster.               |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 3   | 2        | MED  | STRUCT | The agenda lists hostPath, PV/PVC and        | Make the agenda match the slides.  |
|     |          |      |        | StorageClass, but no slide teaches them. The |                                    |
|     |          |      |        | agenda puts NFS before "Managing             |                                    |
|     |          |      |        | configuration". The deck puts it after.      |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 4   | 14       | MED  | CMD    | The PVC names storageClassName: ebs-sc. No   | Add the ebs-sc StorageClass        |
|     |          |      |        | slide defines ebs-sc, so the PVC stays       | manifest (ebs.csi.aws.com, gp3,    |
|     |          |      |        | Pending, also on EKS.                        | WaitForFirstConsumer).             |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 5   | 14       | MED  | FACT   | "needs the EBS CSI driver, for example on    | State the add-on and the IAM role. |
|     |          |      |        | Amazon EKS". EKS needs the aws-ebs-csi-      | [EBS]                              |
|     |          |      |        | driver add-on and an IAM role. EKS Auto Mode |                                    |
|     |          |      |        | uses ebs.csi.eks.amazonaws.com.              |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 6   | 14, 15   | MED  | LAB    | The EBS and NFS manifests cannot run on the  | Label both "example only, not in   |
|     |          |      |        | course cluster: no EBS driver, no NFS        | the lab", or add an NFS step.      |
|     |          |      |        | server. The lab has no NFS step.             |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 7   | 4, 10    | MED  | REPEAT | Two points are on both slides: "the data     | Keep each point on slide 10 only.  |
|     |          |      |        | stays when a container restarts" and "the    |                                    |
|     |          |      |        | lifecycle of its Pod".                       |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 8   | 6, 8, 14 | LOW  | REPEAT | "The Pod uses storage through a PVC" occurs  | State each point one time.         |
|     |          |      |        | 3 times. "awsElasticBlockStore removed in    |                                    |
|     |          |      |        | v1.27" is on slides 7 and 14.                |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 9   | 13       | MED  | STRUCT | "Managing Configuration" ends with a         | Give the answer (configMap and     |
|     |          |      |        | question that no slide answers. It also      | secret volumes, env, args: Week    |
|     |          |      |        | breaks the flow between the Git slides and   | 12), or move the slide to the end. |
|     |          |      |        | the EBS slide.                               |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 10  | 2, 13    | LOW  | REPEAT | Gate fail (31 of 32): "Managing              | Put the agenda line in the gate    |
|     |          |      |        | configuration" is an agenda bullet on slide  | allow-list, or change the words.   |
|     |          |      |        | 2 and the title of slide 13.                 |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 11  | 5        | LOW  | FACT   | "Share files ... between containers that run | Say: share files between the       |
|     |          |      |        | on the same node". An emptyDir is shared     | containers of a Pod.               |
|     |          |      |        | only by the containers of one Pod.           |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 12  | 5        | LOW  | FACT   | "give them to containers safely". Kubernetes | Remove "safely", or add "encrypt   |
|     |          |      |        | stores Secrets unencrypted in etcd by        | etcd at rest". [SEC]               |
|     |          |      |        | default.                                     |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 13  | 7        | LOW  | FACT   | "v1.35 disables it by default" (gitRepo) is  | Add "since v1.33" and the gate     |
|     |          |      |        | true, but not complete. It is off by default | name. [FG]                         |
|     |          |      |        | since v1.33, behind the feature gate         |                                    |
|     |          |      |        | GitRepoVolumeDriver.                         |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 14  | 7        | LOW  | FACT   | hostPath "mounts a directory of the worker   | Say "a file or a directory of the  |
|     |          |      |        | node". It can be a file, on any node. The    | node". Add the docs warning. [V]   |
|     |          |      |        | slide gives no security warning.             |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 15  | 10       | LOW  | FACT   | "Kubernetes does not create other volumes".  | Say: a provisioner can create      |
|     |          |      |        | With dynamic provisioning (lab step 5), a    | remote storage for a PVC.          |
|     |          |      |        | provisioner creates the volume.              | Kubernetes attaches it.            |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 16  | 3, 6     | LOW  | STRUCT | Slide 6: "The Week 10 lecture teaches        | Make the week numbers agree. Make  |
|     |          |      |        | PersistentVolumes". The outline on slide 3   | it a level-1 bullet.               |
|     |          |      |        | says "Week 9: PVs". The line is a child      |                                    |
|     |          |      |        | bullet that is not a property of a PV.       |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 17  | 3        | LOW  | STRUCT | Outline: "Project presentation" is on Week   | Confirm the schedule, then correct |
|     |          |      |        | 14 and Week 15. "Week 11: Exam & Mock Exam   | both lectures.                     |
|     |          |      |        | week" against the syllabus "Mid-Term".       |                                    |
|     |          |      |        | (uncertain)                                  |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 18  | 14, 15   | MED  | REPEAT | Cross-lecture: the NFS manifest (same names) | Keep each in one week only.        |
|     |          |      |        | is on Week 07 slide 15 and Week 10 slide 8.  |                                    |
|     |          |      |        | The "old EBS in the Pod" bullets of slide 14 |                                    |
|     |          |      |        | match Week 10 slide 8.                       |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 19  | 6, 7, 8  | LOW  | LANG   | "CSI", "in-tree" and "SAN" have no           | Write "CSI (Container Storage      |
|     |          |      |        | explanation.                                 | Interface)" and "in-tree: built    |
|     |          |      |        |                                              | into Kubernetes".                  |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 20  | 5, 6,    | LOW  | LANG   | ASD-STE100: "shadows" (metaphor), "do the    | Write each sentence again in ASD-  |
|     | 9-11, 13 |      |        | same job" (idiom), "Our code", "programmers  | STE100.                            |
|     |          |      |        | find many solutions", "very different",      |                                    |
|     |          |      |        | "special directory", "So Kubernetes...",     |                                    |
|     |          |      |        | "This is true", "with the volume mounted"    |                                    |
|     |          |      |        | (passive).                                   |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 21  | 3, 14    | LOW  | LANG   | One word, one meaning: "Persistent Volumes"  | Use one term for each meaning.     |
|     |          |      |        | against "PersistentVolumes". "K8s" against   |                                    |
|     |          |      |        | "Kubernetes". The lecture says "directory",  |                                    |
|     |          |      |        | the lab says "folder".                       |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 22  | 13       | LOW  | DESIGN | The title changed from the source "Managing  | Keep the source case.              |
|     |          |      |        | configuration" to "Managing Configuration"   |                                    |
|     |          |      |        | (DESIGN 3.4 asks for sentence case).         |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 23  | 7-9, 12, | LOW  | DESIGN | Code names in body text are Calibri:         | Use Consolas for each code name.   |
|     | 14, 15   |      |        | emptyDir, hostPath, nfs, configMap, html-    |                                    |
|     |          |      |        | generator, /app.js, nfs-common.              |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 24  | 9, 12,   | LOW  | DESIGN | The terminal text is 9 pt. Slide 15 is 12    | Use 11-12 pt. Split slide 14 into  |
|     | 14       |      |        | pt, and the Week 01 reference is 12-13 pt. 9 | the PVC and the Pod.               |
|     |          |      |        | pt is hard to read on a projector.           |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 25  | 8-10, 14 | LOW  | DESIGN | The second line of a wrapped bullet starts   | Set the hanging indent equal to    |
|     |          |      |        | 0.07 in to the right of the first-line text. | the bullet width.                  |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 26  | 11       | LOW  | DESIGN | The init container box is to the right of    | Put the init container on the      |
|     |          |      |        | the nginx box, but it runs first. Two labels | left. Number the steps 1 to 4.     |
|     |          |      |        | say "2." ("2. Clone", "2. Write").           |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 27  | 12       | LOW  | CMD    | args starts with "clone" and has no "git".   | Add a card for the ENTRYPOINT.     |
|     |          |      |        | No card gives the reason: the ENTRYPOINT of  |                                    |
|     |          |      |        | maziar/alpine-git is git.                    |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 28  | 12       | LOW  | CMD    | maziar/alpine-git has no tag (latest). The   | Pin a tag. Use one YAML style. Do  |
|     |          |      |        | YAML mixes the styles ({name: html,          | the same change in the lab.        |
|     |          |      |        | mountPath: /repo}). nginx also serves the    |                                    |
|     |          |      |        | .git directory.                              |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 29  | 15       | LOW  | DESIGN | Fragment card: the mountPath card also says  | Move that fact to the nfs: card.   |
|     |          |      |        | "Each node needs the nfs-common package".    |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 30  | 4, 5     | LOW  | STRUCT | Slide 4 uses "volume" 5 times. Slide 5 then  | Give the definition first.         |
|     |          |      |        | defines it.                                  |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 31  | 8        | LOW  | FACT   | The list of removed types has no azureFile   | Complete the list. [V]             |
|     |          |      |        | (removed v1.30) and no storageos.            |                                    |
|     |          |      |        | portworxVolume (deprecated) and the types    |                                    |
|     |          |      |        | image, projected, ephemeral and csi are not  |                                    |
|     |          |      |        | named.                                       |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 32  | PDF      | LOW  | FILE   | The PDF has no Title and no Author.          | Set both at the export.            |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 33  | 9, 12    | LOW  | CMD    | nginx:alpine is not a maziar image. The      | Decide. Copy it to maziar/ if the  |
|     |          |      |        | rules conflict on this (table 5, row 2).     | rule is "maziar only".             |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 34  | lab 5    | MED  | LAB    | The lab title "The volume lives as long as   | Say "An emptyDir lives as long as  |
|     |          |      |        | the Pod" repeats defect 1. Lab slide 7 shows | the Pod".                          |
|     |          |      |        | "The file outlived the Pod".                 |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 35  | lab 2    | LOW  | LAB    | "Lab 7 - Prerequisites". The Blackboard      | Use the Blackboard name.           |
|     |          |      |        | number of this lab is probably different.    |                                    |
|     |          |      |        | (uncertain)                                  |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 36  | lab text | LOW  | LAB    | The Week 07 Blackboard text is the short     | Write the long form.               |
|     |          |      |        | form and has an Integrity Pledge. The rule   |                                    |
|     |          |      |        | is the Lab04 long form, with no pledge.      |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 37  | lab 8    | LOW  | LAB    | The Week 07 lab uses busybox:1.36. The gate  | Use a maziar image.                |
|     |          |      |        | bans busybox (table 5, row 2).               |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+

TABLE 2 - Week 07 lecture: additions
+-----+------------+--------------------------------------------------------------------+----------+
| #   | Where      | Addition                                                           | Source   |
+=====+============+====================================================================+==========+
| 1   | slide 10   | A timeline diagram of ephemeral against persistent: the Pod, the   | [V]      |
|     |            | emptyDir, and the PV, NFS and hostPath data that stays.            | [EPH]    |
+-----+------------+--------------------------------------------------------------------+----------+
| 2   | new, after | A hostPath slide: the lab manifest (DirectoryOrCreate,             | [V]      |
|     | 9          | nodeSelector), the type list, the warning, and "Pod Security       | [PSS]    |
|     |            | Baseline forbids hostPath".                                        |          |
+-----+------------+--------------------------------------------------------------------+----------+
| 3   | new,       | A PVC and StorageClass slide for the course cluster: kubeadm has   | [SC]     |
|     | before 14  | no StorageClass; the lab installs standard (rancher.io/local-path, |          |
|     |            | WaitForFirstConsumer, Delete); Pending to Bound; kubectl get       |          |
|     |            | pvc,pv.                                                            |          |
+-----+------------+--------------------------------------------------------------------+----------+
| 4   | slide 9    | emptyDir details: medium: Memory (counts against the memory        | [V]      |
|     |            | limit), sizeLimit, a different mountPath in each container,        |          |
|     |            | readOnly.                                                          |          |
+-----+------------+--------------------------------------------------------------------+----------+
| 5   | slide 9    | A native diagram of the fortune Pod: two containers, one emptyDir, | -        |
|     |            | two mount paths.                                                   |          |
+-----+------------+--------------------------------------------------------------------+----------+
| 6   | slide 8    | The image volume type: it mounts an OCI image read-only. Beta in   | [V]      |
|     |            | v1.35. Runtime support on the course containerd: uncertain.        |          |
+-----+------------+--------------------------------------------------------------------+----------+
| 7   | slide 8    | Name projected, generic ephemeral and csi as volume types.         | [V]      |
|     |            |                                                                    | [EPH]    |
+-----+------------+--------------------------------------------------------------------+----------+
| 8   | slide 7 or | gitRepo: off since v1.33, GitRepoVolumeDriver enables it,          | [V] [FG] |
|     | 11         | CVE-2024-10220 is the reason, and a ValidatingAdmissionPolicy can  |          |
|     |            | block it.                                                          |          |
+-----+------------+--------------------------------------------------------------------+----------+
| 9   | slide 11   | The clone runs one time, so a new commit needs a Pod restart. A    | [SIDE]   |
|     | or 12      | native sidecar (restartPolicy: Always, stable v1.33) can pull      |          |
|     |            | again. --depth=1 gives a smaller clone.                            |          |
+-----+------------+--------------------------------------------------------------------+----------+
| 10  | slide 15   | NFS facts: you need your own NFS server; a Pod spec cannot set     | [V]      |
|     |            | mount options (a PV can); many writers can mount it; the data      |          |
|     |            | stays.                                                             |          |
+-----+------------+--------------------------------------------------------------------+----------+
| 11  | slide 14   | EBS on EKS: the aws-ebs-csi-driver add-on and its IAM role, the    | [EBS]    |
|     |            | Auto Mode provisioner, and the ebs-sc manifest.                    |          |
+-----+------------+--------------------------------------------------------------------+----------+
| 12  | new, after | A command slide with the $ prompt: kubectl describe pod fortune;   | -        |
|     | 9          | kubectl exec fortune -c web-server -- ls /usr/share/nginx/html;    |          |
|     |            | kubectl logs gitrepo-volume-pod -c git-clone; kubectl get volumes  |          |
|     |            | (with the real error); kubectl get pv. Today the lecture has 0     |          |
|     |            | commands.                                                          |          |
+-----+------------+--------------------------------------------------------------------+----------+
| 13  | new, after | A comparison table of emptyDir, hostPath, nfs and PVC: lifetime,   | [V]      |
|     | 8          | scope (Pod, node, cluster), many nodes yes/no, typical use.        |          |
+-----+------------+--------------------------------------------------------------------+----------+
| 14  | slide 9    | readOnly, recursiveReadOnly (stable v1.33) and subPath (mount one  | [V]      |
|     |            | file).                                                             |          |
+-----+------------+--------------------------------------------------------------------+----------+
| 15  | new        | A troubleshooting card: PVC Pending (no default StorageClass, or   | [PV]     |
|     |            | WaitForFirstConsumer with no Pod); NFS mount failure without nfs-  |          |
|     |            | common; a gitRepo Pod on v1.35 (capture the error live).           |          |
+-----+------------+--------------------------------------------------------------------+----------+
| 16  | end        | A takeaways slide and a closing slide that point to lab Week 07,   | -        |
|     |            | Week 10 and Week 12.                                               |          |
+-----+------------+--------------------------------------------------------------------+----------+
| 17  | slide 5    | A caution: Kubernetes does not encrypt Secrets in etcd by default. | [SEC]    |
+-----+------------+--------------------------------------------------------------------+----------+
| 18  | end        | A references slide: the kubernetes.io Volumes page. The fortune    | [V]      |
|     |            | and gitRepo examples probably come from "Kubernetes in Action"     |          |
|     |            | (not verified).                                                    |          |
+-----+------------+--------------------------------------------------------------------+----------+

TABLE 3 - Week 10 lecture (Week10/Lecture_week10_v9.pptx, 28 slides): defects
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| #   | Slide    | Sev  | Type   | Issue (evidence)                             | Fix                                |
+=====+==========+======+========+==============================================+====================================+
| 1   | all      | HIGH | FILE   | LibreOffice made the PDF. Carlito and Linux  | Export through PowerPoint. Check   |
|     | (PDF)    |      |        | Libertine replace Calibri and Consolas, so   | with pdffonts.                     |
|     |          |      |        | the YAML columns do not align. Slide 11      |                                    |
|     |          |      |        | shows "vol-049df61 146c4d7901". Gate fail.   |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 2   | 8, 11,   | HIGH | LAB    | All PV and StorageClass examples use Amazon  | Base the examples on the course    |
|     | 14, 16,  |      |        | EBS (ebs.csi.aws.com, vol-049df61146c4d7901, | cluster. Keep EBS as one "EKS      |
|     | 17, 19   |      |        | gp3). The course cluster has no EBS driver.  | only" card.                        |
|     |          |      |        | The lab uses a hostPath PV with nodeAffinity |                                    |
|     |          |      |        | and the StorageClass standard                |                                    |
|     |          |      |        | (rancher.io/local-path). The lecture names   |                                    |
|     |          |      |        | neither.                                     |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 3   | 22       | HIGH | FACT   | "Pods start, scale and update one at a time, | Say: start and scale-up 0,1,2;     |
|     |          |      |        | in order (master before slaves)". A rolling  | scale-down and update from the     |
|     |          |      |        | update and a scale-down go from the highest  | highest ordinal. [STS]             |
|     |          |      |        | ordinal to 0.                                |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 4   | 22, 23,  | MED  | FACT   | master/slave and MASTER_HOST. MySQL 8.4      | Use source and replica. [MY]       |
|     | 25       |      |        | removed CHANGE MASTER TO and MASTER_HOST.    |                                    |
|     |          |      |        | The terms are now source, replica and        |                                    |
|     |          |      |        | SOURCE_HOST.                                 |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 5   | 11,      | MED  | FACT   | The names form no chain. Slide 16 shows      | Use one static chain with class    |
|     | 14-16,   |      |        | kubia-pvc to kubia-pv, but kubia-pv has      | "". Give the dynamic PVC another   |
|     | 19       |      |        | class "" and kubia-pvc has class fast, so    | name.                              |
|     |          |      |        | they never bind. Slide 15 uses kubia-pvc 4   |                                    |
|     |          |      |        | slides before slide 19 defines it. Slide 14  |                                    |
|     |          |      |        | adds myclaim and pv-vol1.                    |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 6   | 13       | MED  | FACT   | "Pending at first ... then Bound ... then a  | Add that bullet. [SC]              |
|     |          |      |        | Pod can use it". With WaitForFirstConsumer   |                                    |
|     |          |      |        | (slide 19 and the lab), the PVC stays        |                                    |
|     |          |      |        | Pending until a Pod uses it.                 |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 7   | 27       | MED  | CMD    | The 4 commands have no "$" (gate fail). They | Add $. Name the lab step. Add "$   |
|     |          |      |        | need the lab StatefulSet, which the slide    | kubectl delete pod dnstest".       |
|     |          |      |        | does not show. No command deletes dnstest.   |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 8   | 3        | MED  | DESIGN | The Week 11 tile has the color FF6B6B,       | Use E74C3C.                        |
|     |          |      |        | outside the palette (gate fail). Week 12     |                                    |
|     |          |      |        | uses E74C3C.                                 |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 9   | 8        | MED  | DESIGN | The bullet box is at x = 0.01 in, so the     | Confirm, then move it to 0.55 in.  |
|     |          |      |        | bullets touch the slide edge. The margin is  |                                    |
|     |          |      |        | 0.55 in. (Maybe your hand edit: uncertain.)  |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 10  | 8        | MED  | STRUCT | The title "Persistent Volumes: Storage in    | Change the title, for example      |
|     |          |      |        | the Pod" sits on a direct nfs volume, which  | "Volumes in the Pod Spec: the      |
|     |          |      |        | is the problem that PVs solve.               | Limits".                           |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 11  | 10, 13,  | MED  | REPEAT | "A Pod references the PVC": 4 times.         | State each point one time.         |
|     | 16, 20,  |      |        | "Kubernetes binds the PVC to a PV": 3 times. |                                    |
|     | 22,      |      |        | "A DNS name for each Pod": 3 times. "Each    |                                    |
|     | 25-27    |      |        | Pod has its own PVC": 2 times. The PVs of    |                                    |
|     |          |      |        | slides 11 and 14 are near copies.            |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 12  | 11, 14   | MED  | CMD    | Two PVs use the same volumeHandle            | Merge them into one PV.            |
|     |          |      |        | vol-049df61146c4d7901.                       |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 13  | 8        | MED  | CMD    | nfs.example.com is a placeholder. The        | Label it "example only", or remove |
|     |          |      |        | cluster has no NFS server and no nfs-common, | it. [V]                            |
|     |          |      |        | so the Pod stays ContainerCreating.          |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 14  | lecture  | MED  | LAB    | The lab does not practise 6 lecture topics:  | Remove them from the lecture, or   |
|     | vs lab   |      |        | hostPath in a Pod, nfs, Retain and Released, | add short lab checks (limit 40     |
|     |          |      |        | a PVC that names a StorageClass, the GET     | commands).                         |
|     |          |      |        | /data peer collection, and MySQL             |                                    |
|     |          |      |        | replication.                                 |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 15  | 4 + text | MED  | LAB    | Blackboard asks to explain nodeAffinity      | Add additions 5 and 7.             |
|     |          |      |        | (section 2), "no StorageClass at the start"  |                                    |
|     |          |      |        | (1) and "claims before the provisioner" (7). |                                    |
|     |          |      |        | The lecture does not teach PV nodeAffinity,  |                                    |
|     |          |      |        | the local type or reclaimPolicy Delete.      |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 16  | lecture  | MED  | LAB    | The lecture has no StatefulSet manifest and  | Add addition 8.                    |
|     | vs lab   |      |        | no headless Service manifest. The main lab   |                                    |
|     |          |      |        | file kubia-statefulset.yaml has no lecture   |                                    |
|     |          |      |        | slide.                                       |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 17  | 4, 17,   | MED  | LANG   | "we" in 6 places: "How do we keep data",     | Write each sentence again without  |
|     | 25, 26   |      |        | "What if we have", "we must write", "we      | "we".                              |
|     |          |      |        | cannot use it", "We do not create them ...   |                                    |
|     |          |      |        | as we did". Gate fail.                       |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 18  | many     | MED  | LANG   | One meaning, many words: folder / directory; | Use one word for each meaning.     |
|     |          |      |        | description / definition / manifest /        |                                    |
|     |          |      |        | configuration; persistent volume /           |                                    |
|     |          |      |        | PersistentVolume / Persistent Volumes; claim |                                    |
|     |          |      |        | / PVC; K8s / Kubernetes; stays / keeps /     |                                    |
|     |          |      |        | retain. Gate fail.                           |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 19  | 11       | LOW  | LANG   | "When the claim goes, Kubernetes keeps the   | Say: when you delete the claim,    |
|     |          |      |        | PersistentVolume. It does not erase or       | the PV becomes Released and keeps  |
|     |          |      |        | delete it." "goes" is vague. The Released    | its data. [PV]                     |
|     |          |      |        | state is not named.                          |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 20  | 24       | LOW  | LANG   | Idioms: "like cattle", "like pets", "When a  | Use plain words: replaceable Pods, |
|     |          |      |        | pet dies".                                   | Pods with a fixed identity.        |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 21  | 5        | LOW  | LANG   | Two instructions in one sentence. The field  | Use two sentences. Write readOnly. |
|     |          |      |        | is readOnly: true, not "ReadOnly".           |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 22  | 4, 17,   | LOW  | DESIGN | Code in Calibri: /var/log, kubectl get       | Use Consolas.                      |
|     | 18, 23,  |      |        | storageclass, spec.storageClassName,         |                                    |
|     | 25, 28   |      |        | MASTER_HOST=..., clusterIP: None, the DNS    |                                    |
|     |          |      |        | names, GET /data.                            |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 23  | 25       | LOW  | DESIGN | The DNS name breaks over two lines:          | Make the box wider.                |
|     |          |      |        | "mysql-0.mysql-" / "h.default.svc...".       |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 24  | 5        | LOW  | DESIGN | The warning card has a blue bar. A caution   | Use the red bar. Move the card up. |
|     |          |      |        | card uses the red bar. There is a 1.7 in gap |                                    |
|     |          |      |        | above the card.                              |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 25  | 12       | LOW  | DESIGN | A box ends at y = 6.72 in, in the footer     | Move the box up.                   |
|     |          |      |        | band (6.70 in). Gate fail.                   |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 26  | 28       | LOW  | DESIGN | The "2. SRV lookup" up-down arrow (0.38 x    | Make it taller, or use a one-way   |
|     |          |      |        | 0.42 in) shows as a diamond.                 | arrow.                             |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 27  | 4, 8,    | LOW  | DESIGN | Much empty space: 35-50 % of each terminal   | Fit the boxes. Use the space for   |
|     | 11,      |      |        | is empty. Slides 4, 13, 17 and 18 use only   | the additions.                     |
|     | 13-15,   |      |        | the top 40 %.                                |                                    |
|     | 17-19,   |      |        |                                              |                                    |
|     | 27       |      |        |                                              |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 28  | YAML     | LOW  | DESIGN | The YAML keys are cyan. DESIGN 2.4 keeps     | Make the YAML gray.                |
|     |          |      |        | cyan for $ command lines.                    |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 29  | all      | LOW  | DESIGN | The type sizes differ: body 13-18 pt, cover  | Use the Week 01 reference sizes.   |
|     |          |      |        | 38 pt, dividers 40 pt. The rule files        |                                    |
|     |          |      |        | conflict on the sizes.                       |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 30  | 18       | LOW  | FACT   | "A PVC that names a StorageClass asks that   | Add "when no static PV matches".   |
|     |          |      |        | storage system to provision". Kubernetes     | [PV]                               |
|     |          |      |        | first looks for a matching static PV.        |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 31  | 14, 18   | LOW  | FACT   | storageClassName: "" has no explanation. It  | Explain it. [PV]                   |
|     |          |      |        | turns off dynamic provisioning for the       |                                    |
|     |          |      |        | claim.                                       |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 32  | 5        | LOW  | FACT   | "Only root can write to the files and        | Correct the words. [V]             |
|     |          |      |        | directories on the host". The docs say some  |                                    |
|     |          |      |        | files "might only be accessible by root".    |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 33  | 4        | LOW  | FACT   | "hostPath is the first persistent storage".  | Say this.                          |
|     |          |      |        | The data stays after a Pod delete, but not   |                                    |
|     |          |      |        | after a node loss or a move to another node. |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 34  | 24       | LOW  | FACT   | A ReplicaSet replacement gets "no data":     | Correct both.                      |
|     |          |      |        | false when the template mounts a PVC. "These |                                    |
|     |          |      |        | Pods are not replicas": the API uses         |                                    |
|     |          |      |        | spec.replicas.                               |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 35  | 17       | LOW  | FACT   | "general purpose and I/O optimized EBS". The | Use the AWS names.                 |
|     |          |      |        | AWS names are General Purpose SSD (gp3) and  |                                    |
|     |          |      |        | Provisioned IOPS SSD (io2).                  |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 36  | 8        | LOW  | FACT   | "Amazon EBS has no direct volume type in a   | Make the bullet exact. [PV]        |
|     |          |      |        | Pod". The deprecated awsElasticBlockStore    |                                    |
|     |          |      |        | field migrates to CSI, and a generic         |                                    |
|     |          |      |        | ephemeral volume also works. (partly         |                                    |
|     |          |      |        | uncertain)                                   |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 37  | 10       | LOW  | FACT   | "a PV of the correct size". The PV must be   | Say "at least the requested size". |
|     |          |      |        | at least the request. The class, volumeMode  |                                    |
|     |          |      |        | and selector must also match.                |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 38  | 25       | LOW  | FACT   | The headless name returns only ready Pods    | Add both conditions. [DNS]         |
|     |          |      |        | (unless publishNotReadyAddresses). A DNS     |                                    |
|     |          |      |        | name for each Pod needs serviceName in the   |                                    |
|     |          |      |        | StatefulSet.                                 |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 39  | 23, 25   | LOW  | STRUCT | Two primary addresses: mysql-master and      | Label slide 23 "without            |
|     |          |      |        | mysql-0.mysql-h. Slide 23 shows the manual   | Kubernetes". Change its title.     |
|     |          |      |        | way, but no label says so. Its title         |                                    |
|     |          |      |        | "StatefulSets" does not fit.                 |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 40  | 26       | LOW  | FACT   | The diagram says "PVC A-0". The real name is | Use the real names.                |
|     |          |      |        | template-StatefulSet-ordinal, for example    |                                    |
|     |          |      |        | data-kubia-0.                                |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 41  | 3        | LOW  | LANG   | Outline: "Week 5: K8s- PODs, ReplicaSets"    | Use the Week 07 tile text. Confirm |
|     |          |      |        | (gate fail). Week 07 says "K8s - Pods".      | the schedule.                      |
|     |          |      |        | "Exam & Mock Exam week" against "Mid-Term".  |                                    |
|     |          |      |        | "Project presentation" on Week 14 and 15.    |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 42  | 3        | LOW  | DESIGN | The outline text is 11.5 pt (gate fail). The | Use 12 pt and one outline design.  |
|     |          |      |        | outline design (arrows, shadows) differs     |                                    |
|     |          |      |        | from Week 07.                                |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 43  | 7, 8, 15 | LOW  | CMD    | Two tags for one image: maziar/kubia:0.1 and | Use one tag.                       |
|     |          |      |        | maziar/kubia:v1.                             |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 44  | 2, 9, 21 | LOW  | STRUCT | The agenda has no Headless Service and no    | Complete the agenda. Add a         |
|     |          |      |        | peer discovery. The hostPath section has no  | divider.                           |
|     |          |      |        | divider slide.                               |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 45  | file     | LOW  | FILE   | The title and the author are empty. The      | Set the title and the author.      |
|     |          |      |        | thumbnail is blank. 2 gate fails.            | Remove the blank thumbnail.        |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 46  | 28       | LOW  | FILE   | An empty notes slide. Gate fail.             | Remove it.                         |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 47  | build    | LOW  | FILE   | Two scripts make v9:                         | Use one builder with VERSION.      |
|     |          |      |        | build_week10_lecture_v8.py writes v8,        |                                    |
|     |          |      |        | fix_outline_week15.py writes v9. No VERSION  |                                    |
|     |          |      |        | constant. It uses the build_week08 engine,   |                                    |
|     |          |      |        | not the Week 01 model engine.                |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 48  | 8        | LOW  | DESIGN | The level-2 bullet is a teal en dash. The    | Use the hierarchy template.        |
|     |          |      |        | hierarchy rule gives a slate square.         |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+
| 49  | 3, 27,   | LOW  | DESIGN | The outline tiles end at x = 12.91 in (edge  | Move the boxes to 1.42 in or       |
|     | 28       |      |        | 12.75). The text boxes of slides 27 and 28   | lower.                             |
|     |          |      |        | start at 1.35 and 1.40 in, in the title band |                                    |
|     |          |      |        | (gate fail). (uncertain)                     |                                    |
+-----+----------+------+--------+----------------------------------------------+------------------------------------+

TABLE 4 - Week 10 lecture: additions
+-----+------------+--------------------------------------------------------------------+----------+
| #   | Where      | Addition                                                           | Source   |
+=====+============+====================================================================+==========+
| 1   | slides     | An access-mode table: RWO, ROX, RWX and ReadWriteOncePod (GA       | [PV]     |
|     | 10-11      | v1.29). RWO allows many Pods on one node.                          |          |
+-----+------------+--------------------------------------------------------------------+----------+
| 2   | slides 11, | The PV phases (Available, Bound, Released, Failed) and the reclaim | [PV]     |
|     | 13         | policies (Retain, Delete; Recycle is deprecated).                  |          |
+-----+------------+--------------------------------------------------------------------+----------+
| 3   | slide 18   | The default StorageClass: the annotation is-default-class;         | [SC]     |
|     |            | storageClassName "" against no class; retroactive default (GA      |          |
|     |            | v1.28).                                                            |          |
+-----+------------+--------------------------------------------------------------------+----------+
| 4   | slide 19   | volumeBindingMode: Immediate (the default) against                 | [SC]     |
|     |            | WaitForFirstConsumer, and why the PVC is Pending.                  |          |
+-----+------------+--------------------------------------------------------------------+----------+
| 5   | slides     | reclaimPolicy is Delete by default, so a dynamic PV goes with its  | [SC]     |
|     | 19-20      | PVC. allowVolumeExpansion: a volume can grow, never shrink.        |          |
+-----+------------+--------------------------------------------------------------------+----------+
| 6   | slide 8    | A CSI slide: what CSI is, and which in-tree types are migrated or  | [V]      |
|     |            | removed.                                                           |          |
+-----+------------+--------------------------------------------------------------------+----------+
| 7   | new, after | "Storage on our kubeadm cluster": no StorageClass at the start;    | [SC]     |
|     | 20         | the local-path provisioner; standard as the default;               |          |
|     |            | WaitForFirstConsumer; a hostPath or local PV with nodeAffinity. It |          |
|     |            | answers Blackboard sections 1, 2 and 4.                            |          |
+-----+------------+--------------------------------------------------------------------+----------+
| 8   | new, after | A StatefulSet and headless Service manifest: serviceName,          | [STS]    |
|     | 26         | selector, volumeClaimTemplates, and the PVC name data-kubia-0.     |          |
+-----+------------+--------------------------------------------------------------------+----------+
| 9   | slide 26   | persistentVolumeClaimRetentionPolicy: whenDeleted and whenScaled,  | [STS]    |
|     |            | default Retain (GA v1.32). A scale-down or a delete keeps the      |          |
|     |            | PVCs.                                                              |          |
+-----+------------+--------------------------------------------------------------------+----------+
| 10  | slide 22   | The update strategy: RollingUpdate in reverse order, partition,    | [STS]    |
|     |            | OnDelete, podManagementPolicy: Parallel, minReadySeconds,          |          |
|     |            | maxUnavailable (beta).                                             |          |
+-----+------------+--------------------------------------------------------------------+----------+
| 11  | slides 22, | spec.ordinals.start (GA v1.31) and the label                       | [STS]    |
|     | 24         | apps.kubernetes.io/pod-index (GA v1.32).                           |          |
+-----+------------+--------------------------------------------------------------------+----------+
| 12  | slide 27   | SRV details: the form _port._proto.service; SRV records exist only | [DNS]    |
|     |            | for named ports; publishNotReadyAddresses; the 30 s DNS negative   |          |
|     |            | cache.                                                             |          |
+-----+------------+--------------------------------------------------------------------+----------+
| 13  | slides     | The current replication terms: source, replica, CHANGE REPLICATION | [MY]     |
|     | 22-25      | SOURCE TO ... SOURCE_HOST.                                         |          |
+-----+------------+--------------------------------------------------------------------+----------+
| 14  | slide 5    | More hostPath cautions: use a local PV instead; mount it read-     | [V]      |
|     |            | only; hostPath data does not count as ephemeral storage, so it can |          |
|     |            | fill the node disk.                                                |          |
+-----+------------+--------------------------------------------------------------------+----------+
| 15  | slide 25   | An example Pod DNS name: 10-40-2-8.default.pod.cluster.local. The  | [DNS]    |
|     |            | source picture had it.                                             |          |
+-----+------------+--------------------------------------------------------------------+----------+
| 16  | slides     | A house terminal with real output: kubectl get pv,pvc (STATUS      | -        |
|     | 13-14      | column) and kubectl describe pvc (Events of a Pending claim).      |          |
+-----+------------+--------------------------------------------------------------------+----------+
| 17  | new        | A troubleshooting card "PVC Pending": no StorageClass,             | [PV]     |
|     |            | WaitForFirstConsumer with no Pod, no matching PV (size, mode,      |          |
|     |            | class), no provisioner.                                            |          |
+-----+------------+--------------------------------------------------------------------+----------+
| 18  | slide 16   | Say what "works on another cluster" needs: a PVC with the same     | -        |
|     |            | name on that cluster.                                              |          |
+-----+------------+--------------------------------------------------------------------+----------+
| 19  | optional   | VolumeSnapshot (GA v1.20).                                         | [SNAP]   |
+-----+------------+--------------------------------------------------------------------+----------+
| 20  | optional   | VolumeAttributesClass (GA version uncertain).                      | [VAC]    |
+-----+------------+--------------------------------------------------------------------+----------+
| 21  | optional   | Generic ephemeral volumes.                                         | [EPH]    |
+-----+------------+--------------------------------------------------------------------+----------+
| 22  | end        | A takeaways slide and a lab pointer slide. The deck now ends on a  | -        |
|     |            | diagram.                                                           |          |
+-----+------------+--------------------------------------------------------------------+----------+

TABLE 5 - Rule conflicts that only you can close
+-----+------------------------------------------------------------------------+----------------------------+
| #   | Conflict (needs your decision)                                         | Affects                    |
+=====+========================================================================+============================+
| 1   | PROMPT.md R1 "keep the source text" against PREFERENCES 14 "ASD-STE100 | W07 (from your old file),  |
|     | bullets, correct facts".                                               | W10 slide 24               |
+-----+------------------------------------------------------------------------+----------------------------+
| 2   | Docker Official Images (nginx, busybox): PREFERENCES 6 "maziar only"   | W07 slides 9, 12; W07 lab  |
|     | against the memory that keeps them against the gate that bans busybox. |                            |
+-----+------------------------------------------------------------------------+----------------------------+
| 3   | Which week owns PV, PVC and StorageClass: Week 07 (agenda, slide 14,   | W07, W10, both labs        |
|     | lab step 5) or Week 10 (slides 9-20)? The outline says Week 9.         |                            |
+-----+------------------------------------------------------------------------+----------------------------+
| 4   | The outline names EKS (Weeks 9, 13), "Exam & Mock Exam" (syllabus:     | W07 slide 3, W10 slide 3   |
|     | Mid-Term) and a project presentation in Week 14. Students have no EKS. |                            |
+-----+------------------------------------------------------------------------+----------------------------+
| 5   | ALERT_RED E74C3C (PROMPT, DESIGN, gate) against the Week 05 audit      | W07 slide 3, W10 slide 3   |
|     | "house red FF5F56".                                                    |                            |
+-----+------------------------------------------------------------------------+----------------------------+
| 6   | Terminal code size: DESIGN 9-11 pt, gate 9-14 pt, Week 01 reference    | W07 slides 9, 12, 14       |
|     | 12-13 pt.                                                              |                            |
+-----+------------------------------------------------------------------------+----------------------------+
| 7   | The title and footer rules are zero-height connectors in the Week 01   | all slides                 |
|     | reference. A memory says to use a thin rectangle.                      |                            |
+-----+------------------------------------------------------------------------+----------------------------+
| 8   | The lab limit of about 40 commands against "the lab practises every    | W07 defect 6, W10 defect   |
|     | lecture topic".                                                        | 14                         |
+-----+------------------------------------------------------------------------+----------------------------+
| 9   | DESIGN 3.4 sentence case against the Title Case of all decks.          | titles                     |
+-----+------------------------------------------------------------------------+----------------------------+
| 10  | DESIGN 8 conversational style and 10.5-11 pt muted text against ASD-   | all slides                 |
|     | STE100 and the 12 pt gate.                                             |                            |
+-----+------------------------------------------------------------------------+----------------------------+
| 11  | Bullet glyph: DESIGN "■" against the Week 01 reference "▪".            | all bullets                |
+-----+------------------------------------------------------------------------+----------------------------+
| 12  | PROMPT.md names Week04_v02_02 as the reference deck. PREFERENCES names | the builders               |
|     | Week 01 v5.                                                            |                            |
+-----+------------------------------------------------------------------------+----------------------------+

Source keys: [V] kubernetes.io/docs/concepts/storage/volumes/  [PV] .../storage/persistent-volumes/  [SC]
.../storage/storage-classes/  [EPH] .../storage/ephemeral-volumes/  [SNAP] .../storage/volume-snapshots/  [VAC]
.../storage/volume-attributes-classes/  [STS] .../workloads/controllers/statefulset/  [DNS] .../services-
networking/dns-pod-service/  [SEC] .../configuration/secret/  [PSS] .../security/pod-security-standards/  [SIDE]
.../workloads/pods/sidecar-containers/  [FG] kubernetes.io/docs/reference/command-line-tools-reference/feature-gates/
[EBS] docs.aws.amazon.com/eks/latest/userguide/ebs-csi.html  [MY]
dev.mysql.com/doc/relnotes/mysql/8.4/en/news-8-4-0.html
```

## Issues / Notes
- I ran no command on a cluster, because the prompt did not ask for AWS resources. The manifests of the lab ran live on 2026-10-27 (Week 07) and 2026-10-31 (Week 10).
- I did not open the decks in Keynote or in PowerPoint. The Week 07 PDF comes from PowerPoint through macOS. The Week 10 PDF comes from LibreOffice, so its layout can differ from PowerPoint.
- I had no ASD-STE100 dictionary. The language checks cover sentence length, voice, contractions, idioms, "we" and the gate word list.
- "uncertain" in a row means that the reviewer could not prove the item.
- No server started, so no port is used.
