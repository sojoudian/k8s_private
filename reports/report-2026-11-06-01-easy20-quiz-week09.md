# Report: Easy 20-question quiz for Week 09 (Amazon EKS and the kubeadm lab)
**Date**: 2026-11-06
**Sequence**: #01 for the day

## Summary
I wrote 20 easy multiple-choice questions from the Week 09 lecture
(`Week09/Lecture_week09_v7.pptx`, Amazon EKS) and the Week 09 lab
(`Week09/Lab_week09_v4.pptx`, the jobs that EKS does for you, on a kubeadm cluster).
The builder applies the gates of the earlier easy quizzes, plus one new gate against
the earlier EKS quiz. An independent reviewer checked the quiz in 6 rounds. The rounds
found 20, 15, 8, 4, 1 and 0 defects. All defects are fixed, except one known risk in Q4.

## What Changed
- `quiz_pool_src/q_easy20_w09.py`: new. The 20 questions, each with a topic, the stem, 4 options, an optional fixed order, the reason (WHY) and one mistake for each wrong option (IF).
- `quiz_pool_src/build_easy20_w09.py`: new. A copy of `build_easy20_w56.py` with the new names. It also compares with `q_easy20_w56`, and it has the new GATE 10b against `Week09/Week08_Quiz_Blackboard.txt`.
- `quiz_pool_src/audit_easy20_w09.py`: new. A copy of `audit_easy20_w56.py` for the new files. It reads only the delivered files.
- `quiz_pool_src/Quiz_W09_Easy20/Quiz_W09_Easy20_Blackboard.txt`: new. The upload file for Blackboard Ultra, 20 rows.
- `quiz_pool_src/Quiz_W09_Easy20/Quiz_W09_Easy20_AnswerKey.txt`: new. The key for the instructor, with WHY and IF lines.
- `quiz_pool_src/Quiz_W09_Easy20/Quiz_W09_Easy20_Titles.txt`: new. One neutral title for each question, for example `clo835-e09-001 responsibility`.
- `quiz_pool_src/Quiz_W09_Easy20/Quiz_W09_Easy20_QTI21.zip`: new. The QTI 2.1 package with the neutral titles (20 items and 1 manifest).
- No deck, no lab file and no earlier quiz changed.

## Technical Details

### Scope
- Quiz 4 in the syllabus (11/18) covers ConfigMaps and Secrets, not Week 09. This quiz is a separate Week 09 quiz, as the user asked.
- 10 questions come from the lecture and 10 come from the lab.
- The Week 09 material only. Round 2 removed one question (a Pending PVC), because only the Week 10 lecture teaches that fact.

### The 20 questions
| Q | Topic | Key | Proof of the key |
|---|---|---|---|
| 1 | responsibility | D | Lecture: AWS runs the control plane; you own the workloads |
| 2 | cost | C | aws.amazon.com/eks/pricing: 0.10 USD per cluster per hour (standard support) |
| 3 | worker options | A | docs.aws.amazon.com/eks/latest/userguide/fargate.html |
| 4 | networking | D | Lecture: the VPC CNI gives each Pod a VPC address |
| 5 | endpoint | C | docs.aws.amazon.com/eks/latest/userguide/cluster-endpoint.html |
| 6 | storage | D | Lecture: EFS is ReadWriteMany across Availability Zones; EBS stays in one zone |
| 7 | storage | A | docs.aws.amazon.com/eks/latest/userguide/ebs-csi.html: AWS recommends the EKS add-on |
| 8 | permissions | B | Forbidden is the authorization step; a failed IAM check gives Unauthorized |
| 9 | certificates | B | Lab: certificates 1 year, CA 10 years; live test 2026-10-31: 364 days |
| 10 | provisioning | A | eksctl create cluster -f (eksctl documentation) |
| 11 | control plane | D | Lab: the kubelet starts the static Pods; live test: owner kind Node |
| 12 | scheduling | A | Live test 2026-10-31: Pending, NODE `<none>` |
| 13 | cluster state | B | Lab: `etcdctl get /registry/namespaces --prefix` |
| 14 | availability | B | Live test: one etcd member; the API server and etcd run on the master only |
| 15 | identity | A | Live test: `kubectl auth whoami` gives kubernetes-admin, X509 |
| 16 | maintenance | D | Live test: after the drain, all 4 Pods on workernode1 |
| 17 | maintenance | C | Live test: SchedulingDisabled after the cordon |
| 18 | clean up | C | Live test: `terraform destroy` removed 15 resources |
| 19 | upgrades | B | Live test: `kubeadm upgrade plan` only reads |
| 20 | nodes | C | Live test: `kubeadm token create --print-join-command` printed the join line |

"Live test" means the Week 09 lab run on AWS on 2026-10-31, report `report-2026-10-31-04-week09-lab-v3-live-test.md`.

### The review rounds
| Round | MUST-FIX | SHOULD-FIX | Main findings |
|---|---|---|---|
| 1 | 5 | 15 | Q9 copied the earlier EKS quiz; Q10 and Q20 had name give-aways; Q12 needed `-o wide`; Q16 needed kubeadm and `--ignore-daemonsets`; IAM tested two times |
| 2 | 5 | 10 | New Q7 outside Week 09; new give-aways in Q10, Q13 and Q14 from the round 1 fixes |
| 3 | 1 | 7 | New Q7: "Amazon EKS" only in the key |
| 4 | 1 | 3 | Q7: on EKS Auto Mode the node AMI holds the EBS driver, so the AMI option was defensible |
| 5 | 0 | 1 | Q16: the key was the odd one out in its form |
| 6 | 0 | 0 | none |

## Results
`build_easy20_w09.py`:
- GATE 1-7: 0 errors
- GATE 10: 0 repeats of an earlier pool
- GATE 10b: 0 repeats of the earlier EKS quiz
- GATE 11, 12, 13: 0 errors (feedback, fixed orders, titles)
- GATE 9: the key is the longest in 4 and the shortest in 5 questions
- GATE 8: A 5, B 5, C 5, D 5
- GATE 8b: longest run of one letter 2

`audit_easy20_w09.py`, exit code 0:
- 20 rows; 20 records in the key; 21 files in the ZIP; 20 titles; 0 errors
- Guess by the longest option 4 of 20, by the shortest 5 of 20, by the most words 2 of 20
- Guess by one letter: 5 of 20 for each letter
- 0 answer leaks; 0 question pairs at risk

## Issues / Notes
- **Q4, a known risk.** The stem gives the subnet 192.168.20.0/24, and two options are in it. One of them is the node address, so a guesser can pick the other one. The subnet is necessary for a 100% correct key, so the risk stays.
- **"Run all the code."** No EKS cluster exists for this course, so the EKS command of Q10 (`eksctl create cluster -f`) did not run. The EKS keys come from the AWS documentation. The kubeadm keys come from the live lab test of 2026-10-31. No cluster ran today, and no AWS resource was created.
- **Platform settings.** The upload file cannot shuffle the options, so the letters are balanced at 5 each. Blackboard Ultra sets each question to 1 point at upload. Use Bulk Edit Points to set the value.
- **Show only the grade** until all students finish, because the feedback can spread the answers. This is a Blackboard setting.
- **After the quiz**, read the statistics of each question. Review a question that fewer than 30% or more than 95% of students answer correctly, or that has low or negative discrimination.
