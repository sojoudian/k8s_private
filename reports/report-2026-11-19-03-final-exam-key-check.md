# Report: Check of the Questions and Keys of the Week 11 Final Exam Upload File
**Date**: 2026-11-19
**Sequence**: #03 for the day

## Summary
I checked the 40 questions of
`/Users/maziar/Documents/c/r/k8s_private/summer_2026_CLO835_exam/Week11_Final_Exam_Blackboard_Ultra.txt` (the file
in the Blackboard test "Week 11 - Final Exam 20%") for technical correctness. 2 keys are wrong (Q6, Q17). 4
questions have a wrong or loose fact in the stem or an option, but their key is the best option (Q1, Q4, Q11,
Q28). The other 34 keys are correct. I changed no file and nothing in Blackboard.

## What Changed
- Created this report. No other file changed. The upload file and the Blackboard test did not change.

## Technical Details
- Method: I read each stem, each option and each key. I compared them with the Docker and Kubernetes
  documentation, the AWS EKS pricing model, the Week 3 lab text (`Lab03_Instructions.md`), the summer Lab03 text
  (`Labs/Lab03/Lab03.txt`) and the summer answer key with its rationale (`CLO835_Final_Exam_AnswerKey.md`).
- I ran no container and no cluster for this check.

### MUST-FIX: the key is wrong

**Q6 (CMD and ENTRYPOINT).** Delivered key: "A prints goodbye and B prints hello goodbye".
- With no ENTRYPOINT, the arguments of `docker run` replace the whole CMD, also the program. So container A runs
  the program `goodbye`. alpine has no such program, so A does not start:
  `exec: "goodbye": executable file not found in $PATH`. Container B runs `echo hello goodbye` and prints
  "hello goodbye".
- No option is correct. The summer rationale ("A runs echo goodbye") is wrong.
- Possible fix: a new key "A fails with executable file not found, and B prints hello goodbye". Another fix:
  change the stem to `docker run A echo goodbye`; then A prints "goodbye", and the B part needs a new run
  command.

**Q17 (kubectl and the cluster version).** Delivered key: True.
- Kubernetes version skew policy (v1.35): kubectl is supported within one minor version (older or newer) of
  kube-apiserver. A different major version is not supported (all releases are v1).
- The statement "may differ in MAJOR version" is false. "should run the same MINOR version" is also stricter
  than the policy. The key must be False, or the statement must change.
- Source of the error: the summer Week04 slide 18 ("Major version mismatch is supported, minor isn't"). The
  summer Lab03 text asks "what would happen on a major version skew", which agrees with the policy and not with
  the slide.
- Possible fix: "True or False: kubectl is supported within one minor version (older or newer) of the API
  server of the cluster." Key: True.

### SHOULD-FIX: a wrong or loose fact, but the key is the best option

**Q4 (Flask port).** `flask run --port=18080` (and `app.run()`) listens on 127.0.0.1 if no host is given. Then
`-p 8080:18080` gets no answer, and no option is correct. The CLO835 Mock Exam (Q9) teaches this case, so
students can choose to see Q4 in this way. Fix: the stem says "launches the server with --host=0.0.0.0
--port=18080".

**Q11 (macvlan).** Docker macvlan does not get IP addresses from the DHCP server of the LAN. Docker IPAM gives
each container an address from the `--subnet` (or `--ip-range`) of the network. The stem ("an IP handed out by
the LAN's DHCP server") and option D ("can pull a real LAN IP") state a false fact. The key macvlan is still
the only fit. Fix: "with its own MAC address and an IP address of the LAN subnet", and option D "...gets its own
MAC on the physical network and an IP address of the LAN subnet".

**Q28 (NodePort).** Option D (the key): "A ClusterIP service is also created automatically". Kubernetes creates
one Service only; a Service of type NodePort also gets a cluster IP. Fix: "The Service also gets a cluster IP,
and the node port comes from the range 30000-32767."

**Q1 (option E).** "docker start resumes a stopped container" uses the word of `docker unpause`. `docker start`
starts the main process again from the beginning; the files of the container stay. The option is correct as
the course uses it. Fix (optional): "docker start starts a stopped container again, and its files are still
there."

### Notes: correct keys with an edge case (no change needed)
- Q19: the stem names the "Cloud9 host". The Fall Week 4 lab (`Week04/lab_commands.txt`) uses kind with
  `extraPortMappings`, but it does not name Cloud9. "the host" is safer.
- Q26 option C: true for the default iptables mode. In IPVS mode, kube-proxy puts the cluster IPs on the
  interface `kube-ipvs0`.
- Q35: with EKS access entries, access policies also authorize requests (the EKS authorizer), not only RBAC.
- Q37: with a ReadWriteOnce volume (for example EBS), Pods on a second node cannot attach it.
- Q36: $0.10 per cluster-hour (standard support): 3 x 730 x 0.10 = 219.00 USD. Extended support costs more.
- Q13, Q14, Q15 agree with the Week 3 lab, which the Fall course also uses (`week03/cleanup_lab03.sh`):
  `mkdir -p $PWD/mysql-data` then a bind mount, ERROR 1049, subnet 172.28.0.0/16, the server name mysql-db,
  only Adminer on 8080, and `--cap-drop=ALL` with chown, setuid, setgid, dac_override and fowner added back
  (so the Q15 key False is correct).

### Keys that I found correct
Q1 (A, B, E, F), Q2 False, Q3 C, Q4 B, Q5 (A, C, E, F), Q7 D, Q8 C, Q9 C, Q10 B, Q11 D, Q12 A, Q13 B,
Q14 (A, C, D), Q15 False, Q16 B, Q18 (A, B, C, D), Q19 C, Q20 B, Q21 C, Q22 False, Q23 C, Q24 (A, B, C),
Q25 B, Q26 (A, B, C), Q27 B, Q28 D, Q29 A, Q30 C, Q31 (A, B, C, E), Q32 C, Q33 B, Q34 (A, B, E), Q35 True,
Q36 C, Q37 D, Q38 (A, B, C, E), Q39 C, Q40 B.

## Results
- 40 questions checked: 2 wrong keys (Q6, Q17), 4 wording faults with a usable key (Q4, Q11, Q28, Q1), and
  5 notes with no change needed.
- The question numbers are the order of the upload file and of the instructor view in Blackboard.

## Issues / Notes
- The same faults are in the Summer 2026 exam, because the file is a copy of it.
- No change is made yet, as the user asked.
- No server started, so no port is used.
