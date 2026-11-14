# Report: The Week 05 and Week 06 easy quiz on a live cluster

**Date**: 2026-10-27
**Sequence**: #03 for the day

## Summary

Every fact of the 20 questions holds on a real Kubernetes cluster. The cluster
came from the Week 06 lab Terraform in the AWS Learner Lab: one master and two
workers, Kubernetes v1.35.9. The first run showed 4 failures. Each one was a
defect of the test script, not of a question. A second run with a correct test
design passed all four. The infrastructure is destroyed.

## What Changed

No quiz file changed. The questions stay as they are.

- The Terraform state of `CLO835_Fall_2026/Week06` is empty again.
- `apply.log` and `destroy.log` stay in that folder. The two plan files are
  removed.

## Technical Details

### The cluster

- Terraform plan: 15 resources, 3 EC2 instances of the type m5.large.
- Master `3.227.0.218`, workers `44.220.48.25` and `98.92.132.169`.
- The three nodes reached the ready state 4 minutes after the apply.
- Kubernetes v1.35.9, built by kubeadm from the lab user data.

### The results, first run

PASS: Q1, Q2, Q3, Q4, Q5, Q7, Q9, Q10, Q11, Q12, Q13, Q14, Q16, Q19, Q20.
FAIL: Q6, Q15, Q17, Q18.

### The cause of the four failures

- The test Pods `web` and `extra` carried the label `app=kubia`, the same
  label as the Deployment. The counts for Q6, Q17 and Q18 therefore read too
  many Pods, and a delete by label removed the client Pod of the test.
- Q15 ran a request from the master. The master is a node of the cluster, and
  a node reaches a ClusterIP address through kube-proxy. The question asks
  about a laptop outside the cluster.

### The second run

- Q6 PASS: a ReplicaSet of 3 Pods replaced the Pod `rs6-6984d9c59c-nk5bs`,
  and the new Pod carries a new name.
- Q17 PASS: the address stayed 10.97.197.187 and it answered after every Pod
  behind it changed.
- Q18 PASS: `--selector app=rs6` gave 3 Pods of 7.
- Q15 PASS: the same address answered 200 from a node and from a Pod, and a
  request from this laptop timed out after 6 seconds (curl exit 28).

### The evidence of the other questions

- Q1 the two containers of one Pod ran on `workernode2`.
- Q2 a request to 127.0.0.1:80 from the second container reached the first.
- Q4 the live Deployment carries `apps/v1`.
- Q9 the available count never fell below 3 during a rolling update. The
  strategy fields are RollingUpdate, maxSurge 25%, maxUnavailable 25%.
- Q10 the available count reached zero with the Recreate strategy.
- Q11 a new Pod with the matching label joined the Service: 4 addresses to 5.
- Q12 port 8080 of the Service reached targetPort 80 of the container.
- Q13 the node port 31536 answered 200 on all three nodes.
- Q14 the short name `kubia` resolved inside the cluster.
- Q16 the external address of a LoadBalancer Service stayed pending.
- Q19 one Ingress object carried two host rules; no controller runs, so
  nothing answered the host names.
- Q20 the Deployment built a new ReplicaSet after the delete of the old one.
- Q8 has no test of its own. The Q9 and Q10 runs prove it: a Deployment moves
  an application to a new image with no stop.

## Results

- 20 facts, 20 hold.
- `Apply complete! Resources: 0 added, 0 changed, 15 destroyed.`
- The Terraform state holds no resource, and the AWS query for the instances
  with the tag `week06-k8s-*` gives no answer.

## Issues / Notes

- The command `kubectl config set-context` failed on the master with a
  permission error for `/home/ubuntu/.kube/config.lock`. The test therefore
  ran in the default namespace. The results are not affected.
- One design rule stays open: a person must review the questions.
