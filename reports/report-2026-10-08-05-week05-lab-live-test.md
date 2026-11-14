# Report: The Week 05 Lab, Tested Live on AWS
**Date**: 2026-10-08
**Sequence**: #05 for the day

## Summary
The whole Week 05 lab ran on a real AWS cluster, from `terraform apply` to
`terraform destroy`. Every command in `localMachine.sh` was executed in order.
One defect was found, fixed, and re-tested from a clean first boot. The lab now
performs as the slides describe. Nothing is left running.

## What Changed
| File | Change |
|------|--------|
| `CLO835_Fall_2026/Week05/master-init.sh.tftpl` | The master now writes `cleanup_lab05.sh` into `/home/ubuntu` at first boot. |

Nothing else was changed. Nothing is committed or pushed.

## The defect

**Step 13 could not run.** `localMachine.sh` ends with `./cleanup_lab05.sh`. The
student runs Terraform on their own laptop, so that file never reaches the
master. The live test proved it:

```
ubuntu@masternode:~$ ls cleanup_lab05.sh
ls: cannot access 'cleanup_lab05.sh': No such file or directory
```

**The fix.** `master-init.sh.tftpl` writes the script into `/home/ubuntu`, sets
the execute bit and gives it to `ubuntu`. A check confirms the copy inside the
template stays byte-identical to `Week05/cleanup_lab05.sh`.

**Week 04 has the same defect.** Its Step 6 calls `./cleanup_lab04.sh`, which is
also absent from its master. It is NOT changed, because you did not ask for that.

## What was tested

### Terraform
| Action | Result |
|---|---|
| `init`, `validate`, `fmt -check` | pass |
| `plan` | 16 to add, 0 to change, 0 to destroy |
| `apply` | 16 added in about 70 seconds |
| AMI | `ami-080341f184b848d0b`, Ubuntu 26.04.1 LTS |
| Subnet choice | `us-east-1f`, a zone that offers `m5.large`. `us-east-1e` does not, and the offerings filter excluded it. |
| `destroy` | 16 destroyed, 0 left in state |

### The cluster forms by itself
All three nodes reached `Ready` **31 seconds** after the master answered SSH.

```
masternode    Ready  control-plane  v1.35.9  Ubuntu 26.04.1 LTS  containerd://2.2.2
workernode1   Ready  worker         v1.35.9
workernode2   Ready  worker         v1.35.9
```

Both workers carry the `worker` role, so the background labelling loop works.
Nine `kube-system` pods ran, including both CoreDNS replicas.

### The MTU fix holds
```
ens5       mtu 1500
flannel.1  mtu 1450
```

### Every step
| Step | Slide | Result |
|---|---|---|
| 0 | 3 | 3 nodes Ready, `kube-system` healthy |
| 1 | 4 | Pod scheduled on `workernode1`, IP `10.244.2.2`. Port forward returned the nginx page. |
| 2 | 5 | `kubia-manual.yaml` matched the slide. `maziar/kubia` pulled and ran. `kubectl explain` answered. |
| 3 | 6 | `READY 2/2`. `kubectl logs -c logger` returned the dates. The sidecar reached nginx on `127.0.0.1`. |
| 4 | 7 | `logs`, `logs -c`, `--tail 1 --follow` and `-o yaml` all answered. |
| 5 | 8 | `--show-labels`, `-l app=web`, `-l 'rel in (stable,beta)'`, `-l app!=web` and `--overwrite` all selected correctly. |
| 6 | 9 | `kubectl scale pod` FAILED with exit 1, which is the lesson. The Deployment then created all three objects. |
| 7 | 10 | ReplicaSet made 3 Pods across both workers. It did NOT adopt the stand-alone `kubia` Pod. |
| 8 | 11 | Scaled 1 to 3 and back to 1. |
| 9 | 12, 13 | A second ReplicaSet appeared, the first went to 0, the image became `alpine:3.15`. |
| 10 | 14 | `rollout history` listed 2 revisions. `undo` returned the image to `alpine:3.14`. |
| 11 | 15 | A deleted Pod was replaced at once, count stayed 3. The stand-alone Pod was not replaced. |
| 12 | 16 | See below. |
| 13 | 17 | After the fix, the script was present and removed everything. |

### The critical test, NodePort from the internet
The Pod ran on `workernode1` only. All three public addresses answered with the
full page:

| Node | Address | Result |
|---|---|---|
| masternode | `3.236.107.100` | HTTP 200, 896 bytes |
| workernode1 | `32.198.56.68` | HTTP 200, 896 bytes |
| workernode2 | `100.52.199.105` | HTTP 200, 896 bytes |

The body arrived whole, not only the headers. That is the MTU fix working.

### The cleanup
```
service "nginx-http" deleted
replicaset.apps "kubia-rs" deleted
pod "nginx" deleted ... "kubia" ... "pingpong" ... "web-with-sidecar" deleted
namespace "pingpong" deleted
done
```
No Pod, Service or ReplicaSet remained outside the system namespaces. No yaml
file remained in the home directory.

## Results

Final AWS state:
- Running instances in the account: **0**
- `week05-k8s-*` security groups: **0**
- Volumes in `available` state: **0**
- Resources in the Terraform state: **0**

The repository folder is clean. `.terraform`, the lock file, the state files and
the plan file were all removed after the test. `git status` shows `?? Week05/`.

## Issues / Notes
- Three full cluster builds were made and destroyed. Three `m5.large` for about
  25 minutes in total, so roughly 0.12 USD.
- A second finding, not fixed: changing `user_data` on an existing instance does
  not re-run it. Terraform modified the master in place and cloud-init skipped
  the new script, because it runs once per instance. It matters only to somebody
  editing the template mid-life, never to a student. Adding
  `user_data_replace_on_change = true` would remove it, but Week 04 does not have
  it either.
