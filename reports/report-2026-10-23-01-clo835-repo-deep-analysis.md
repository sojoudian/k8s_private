# Report: CLO835_Fall_2026 repository — deep analysis

**Date**: 2026-10-23
**Sequence**: #01 for the day

## Summary

I read all 61 files of the public course repository, then I verified the repository
with tools. The analysis is read-only. No file of the repository changed. The
toolchain checks found 21 items. One item stops the Assignment 2 pipeline at the
first push: the supplied GitHub Actions workflow is not valid YAML. Five more items
block a documented step or cost a mark. The Terraform, the shell scripts, the
Compose file and five of the six starter applications pass every check.

## What Changed

No file of the repository changed. `git status` is the same as before: 5 modified
files and 1 untracked file in `assignment-1`, all from the 2026-10-15 repair.

Files created:
- `reports/report-2026-10-23-01-clo835-repo-deep-analysis.md` (this report)

Temporary files, in the session scratchpad only:
- `scratchpad/verify/apps/` — copies of the 6 starter applications, port 8080
  changed to 18090, built and run
- `scratchpad/verify/tf/` — copies of the 4 Terraform sets, initialised and
  validated
- `scratchpad/verify/venv/` — a virtual environment that holds PyYAML

## Technical Details

Repository: `https://github.com/sojoudian/CLO835_Fall_2026`
Local clone: `/Users/maziar/Documents/c/r/a2_test/CLO835_Fall_2026`
Branch `master`, HEAD `39a43b1 add assignment-2`.
Contents: 61 text files, 94 KB. `assignment-1`, `assignment-2`, `Week02`,
`Week03`, `Week04`, `Week05`.

### Method

1. Read every file.
2. Run `bash -n` on every shell script.
3. Parse every YAML file with PyYAML.
4. Parse every JSON file.
5. Compile every Python file.
6. Run `terraform fmt -check` on the 4 Terraform sets, in place.
7. Copy the 4 Terraform sets to the scratchpad, run `terraform init`, then
   `terraform validate`.
8. Read the AWS provider schema, and look for a deprecated resource.
9. Copy the 6 starter applications to the scratchpad, change port 8080 to 18090,
   then build and run each one and test 3 paths with `curl`.
10. Run `docker compose config` on `assignment-1/compose.yaml`.
11. Query Docker Hub for the architecture of `maziar/kubia`.
12. Grep for private data: the home IP address, `/Users/`, `.ssh/`, `AKIA`,
    a private key, the user name.
13. Compare every claim of the prose against the code that supports it.

### Tool versions on this machine

| Tool | Version |
|---|---|
| Terraform | v1.16.4 |
| AWS provider | v6.70.0 (resolved today, not pinned) |
| Go | 1.26.3 |
| Rust / Cargo | 1.96.0 |
| Node.js | v26.10.0 |
| Java | OpenJDK 27 |
| Python | 3.14.8 |
| .NET | not installed |

## Results

### Checks that pass

| Check | Result |
|---|---|
| `bash -n`, 12 shell scripts | 12 of 12 pass |
| `terraform fmt -check`, 4 sets | 4 of 4 formatted correctly |
| `terraform validate`, 4 sets | 4 of 4 `Success! The configuration is valid.` |
| `docker compose config` | `assignment-1/compose.yaml` valid |
| Python compile | 2 of 2 pass |
| JSON parse | 1 of 1 passes |
| Starter applications built and run | 5 of 6 |
| Private-data grep | 0 hits |

Each of the 5 starter applications answers `/`, `/healthz` and `/readyz` with
HTTP 200. The body of `/` is exactly `Hello world from the CLO835 class!`. I could
not run the C# starter, because this machine holds no .NET SDK. I reviewed it by
reading only.

The installed toolchain supports every version claim of the repository: `go 1.26`
in `go.mod`, `edition = "2024"` in `Cargo.toml`, `"node": ">=26"` in
`package.json`, `net10.0` in `app.csproj`, and Python 3.14 on Ubuntu 26.04.

The private-data grep is clean. The only hits are `maziar/kubia`, which is the
intended public image of the course, and the throwaway lab passwords `pw` and
`db_clo835`. There is no home IP address, no `/Users/` path, no `.ssh/` reference,
no AWS key and no private key.

### Defect 1 — the Assignment 2 workflow is not valid YAML

`assignment-2/.github/workflows/docker.yml`, line 25:

```yaml
      - run: echo "TODO: replace this step with your build-and-push steps"
```

A plain YAML scalar cannot hold a colon and a space. The scalar starts at `echo`,
so the parser meets `: replace` and stops.

```
mapping values are not allowed here
  in .../docker.yml, line 25, column 24
```

I reproduced the error with a minimal document, and I proved that single quotation
marks around the whole command make it parse.

GitHub rejects the complete workflow file. The student copies this folder to a new
repository, pushes, and reads `Invalid workflow file`. The purpose of the step is
the opposite: to prove that the pipeline starts.

The fix is one line. Put the command in single quotation marks, or remove the colon.

### Defect 2 — the deploy commands name the wrong path

`assignment-2/README.md` lines 117 and 118 say the files are `k8s/deployment.yaml`
and `k8s/service.yaml`. That is correct.

Lines 145 and 186 say:

```bash
kubectl apply  -f deployment.yaml -f service.yaml
kubectl delete -f deployment.yaml -f service.yaml
```

The `k8s/` prefix is absent. A student who copies the block reads
`error: the path "deployment.yaml" does not exist`.

### Defect 3 — node port 30000 collides with the Week 05 lab

Assignment 2 tells the student to build the cluster from `Week05`, and it requires
node port **30000**.

`Week05/localMachine.sh` line 197 pins the lab Service `nginx-http` to node port
**30000** as well.

If the student does not run `cleanup_lab05.sh` first, `kubectl apply` of the
assignment Service fails:

```
provided port is already allocated
```

The troubleshooting table of `assignment-2/README.md` does not hold this symptom.

### Defect 4 — the assignment never says how to put the YAML on the master

`assignment-2/README.md` line 34: "Run every `kubectl` command of this assignment
on the control plane machine." Line 141 repeats it.

The README holds no `git clone`, no `scp` and no editor step. The student writes
the two manifests on a laptop, and the README never says how they reach the master.

### Defect 5 — Week 04 still calls a cleanup script that is not on the master

`Week04/localMachine.sh` line 82 calls `./cleanup_lab04.sh`.

The student runs Terraform on a laptop, so `Week04/cleanup_lab04.sh` stays on the
laptop. `Week04/master-init.sh.tftpl` does not write the file to the node.

Week 05 fixes this: `Week05/master-init.sh.tftpl` lines 48 to 65 write
`/home/ubuntu/cleanup_lab05.sh` and make it executable. Week 04 needs the same
block.

### Defect 6 — Week 03 has the same gap, on the EC2 path

`Week03/localMachine.sh` line 133 calls `./cleanup_lab03.sh`. Line 3 says to run
the lab on a laptop, where the file is present.

But the folder also ships `main.tf` and `bootstrap.sh` that build an EC2 machine
with Docker, and lines 62 and 63 of the same script explain EC2 behaviour:
"On EC2 the DHCP search domain is ec2.internal". So the lab does run on EC2. On
that machine `cleanup_lab03.sh` is absent, because `bootstrap.sh` does not write
it.

### Defect 7 — the Week 02 README names an instance type that the lab kills

`Week02/README.md` line 64:

> `r6i.large`, 2 vCPU, 16 GB. The lab blocks `xlarge` and larger.

`Week02/main.tf` line 53 sets `instance_type = "m5.large"`, and line 52 says:

> the Learner Lab blocks xlarge and larger, and it stops newer generations such as
> r6i a few seconds after launch.

The README recommends the exact type that the code comment says the lab stops. The
memory figure is wrong too: `m5.large` holds 8 GB, not 16 GB.

### Defect 8 — "change that one line" is not true for any language

`assignment-2/README.md` lines 98 to 100 say that each starter holds one marked
`MESSAGE` constant, and that version 0.3 needs that one line.

Every starter also holds a version constant that stays at `0.2`:

| Language | Lines to change | Where |
|---|---|---|
| Python | 2 | `app.py:7` VERSION, `app.py:8` MESSAGE |
| Go | 2 | `main.go:14` version, `main.go:15` message |
| Java | 2 | `Main.java:12` VERSION, `Main.java:13` MESSAGE |
| C# | 2 | `Program.cs:8` Version, `Program.cs:9` Message |
| Node.js | 3 | `package.json:3`, `server.js:7`, `server.js:8` |
| Rust | 4 | `Cargo.toml:3`, `Cargo.lock:7`, `main.rs:8`, `main.rs:9` |

The result reaches the grader. The image carries tag `0.3`, and
`kubectl logs` prints `CLO835 app v0.2 listening on :8080`.

### Defect 9 — the Week 02 step map is off by one

`Week02/localMachine.sh` lines 21 to 24 map each Dockerfile line to a step of
`runAWS_EC2.sh`. Three of the four are wrong.

| Line | The file says | The true step |
|---|---|---|
| `RUN apt-get install python3 python3-venv` | step 2 | 2, correct |
| `RUN python3 -m venv /opt/venv` | step 4 | **3** |
| `RUN pip install -r requirements.txt` | step 4 | **3** |
| `CMD ["python3", "app.py"]` | step 5 | **4** |

In `runAWS_EC2.sh`, step 3 is "Install Flask" and step 4 is "Run".

### Defect 10 — the Terraform output names do not match the README

`assignment-2/README.md` lines 31 and 149 to 151 use `<master_public_ip>`,
`<worker1_public_ip>` and `<worker2_public_ip>`.

`Week05/main.tf` declares four outputs: `public_ips`, `private_ips`, `next_step`
and `nodeport_url`. `public_ips` is a map with the keys `master`, `worker-1` and
`worker-2`. None of the three README names exists.

### Defect 11 — a small version mismatch in the Assignment 1 README

`assignment-1/README.md` line 13 says "Ubuntu 24.04 and later". The Dockerfile uses
`FROM ubuntu:26.04`. The statement about PEP 668 is true, but the number does not
match the rest of the material.

### Risk 1 — nothing pins the Terraform provider

No `.tf` file in the repository holds a `terraform { required_providers { ... } }`
block or a `required_version`. Every `Week0N/.gitignore` also ignores
`.terraform.lock.hcl`, which is the file Terraform asks you to commit.

So each student resolves the provider on the day they run `terraform init`. Today
that is **AWS provider v6.70.0**, and all four sets validate on it. I read the
v6.70.0 schema: `aws_security_group_rule` is present and is **not** marked
deprecated, and `aws_instance` still holds `root_block_device` and
`metadata_options`. Nothing is broken now. Nothing holds it still either, and all
four labs share the same four resource patterns, so one provider change breaks
them together.

### Risk 2 — Flannel is unpinned

`Week04/master-init.sh.tftpl` and `Week05/master-init.sh.tftpl` install Flannel
from `releases/latest/download/kube-flannel.yml`. Every boot fetches whatever is
newest. The pod CIDR `10.244.0.0/16` is the Flannel default, so the pair matches
today.

### Risk 3 — `maziar/kubia` is a single-architecture image

Docker Hub holds one manifest, not a manifest list.

| Field | Value |
|---|---|
| Digest | `sha256:f14023fd9576029ffa4b99f237bef84483558dfb878fbbebae83a7d87cdbb2b2` |
| Platform | `linux/amd64` only |
| Created | 2026-06-03 |
| Cmd | `node app.js` |
| Port | 8080 |

The Week 05 nodes are amd64, so the lab works. The same manifest fails with
`exec format error` on an Apple Silicon kind or minikube cluster.
`Week05/localMachine.sh` uses the image on lines 42 and 140.

### Risk 4 — only Week 02 holds a README

Week 03, Week 04 and Week 05 hold no README. The student reads the comments of
`localMachine.sh` instead. Assignment 2 sends the student to Week 05 for the
cluster, and Week 05 has no prose.

### Minor items

- `assignment-1/templates/addempoutput.html` line 7: `wassuccessfully` needs a
  space.
- `assignment-1/app.py` line 12: the default password `passwors` stays, on purpose.
  The README documents it.
- `assignment-1/app.py` lines 86 to 111: `/fetchdata` raises `KeyError` and returns
  HTTP 500 for an unknown `emp_id`. The source carries the matching note
  `# Add No Employee found form`.
- `assignment-2/k8s/deployment.yaml` and `service.yaml` parse, and hold `null` for
  `metadata.name`, `spec.replicas`, `spec.type` and `nodePort`. That is the
  intended TODO state.
- `Week03/localMachine.sh` line 85 runs `docker scout cves`, which a server does
  not hold. Line 87 gives the trivy alternative, and the MOTD of `bootstrap.sh`
  warns. This is documented, so it is not a defect.
- `assignment-1/compose.yaml` builds the same `image: my_app` for the three web
  services.

### Structure notes

- Week 04 and Week 05 hold the same infrastructure. `variables.tf` and `.gitignore`
  are identical. `main.tf` differs only in the name strings and the kubeadm token,
  so the two clusters can exist at the same time.
- `bootstrap.sh` differs between Week 04 and Week 05 by one comment line only.
- The repository starts at Week 02. There is no Week 01, and no week after 05.

## Issues / Notes

- The analysis is read-only. The repository is unchanged, and nothing is committed
  or pushed.
- The Assignment 1 repair of 2026-10-15 is still uncommitted: 5 modified files and
  `assignment-1/.dockerignore` untracked.
- `terraform init` downloaded the AWS provider into the session scratchpad, about
  790 MB. The repository holds no `.terraform` folder. I ran no `terraform plan`
  and no `terraform apply`, so no AWS call and no cloud resource.
- The starter applications ran on port 18090, not 8080, and only on copies.
- I could not run the C# starter. This machine holds no .NET SDK.
- I did not verify the external repository
  `https://github.com/sojoudian/simple-webapp-flask`, which Week 02 clones.
