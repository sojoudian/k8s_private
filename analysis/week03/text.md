<!-- Slide number: 1 -->
CLO835 · CLOUD ARCHITECTURE & ADMINISTRATION
WEEK 03
Docker Layers,
Copy-on-Write &
Storage

Instructor: Professor Maziar
Seneca Polytechnic · ITAS Program

### Notes:

<!-- Slide number: 2 -->
LEARNING OBJECTIVES
What you'll learn this week

01
02
Docker image layers
The container R/W layer
How images are built as a stack of read-only layers and why layering matters for caching and image size.
Where runtime changes live, and how copy-on-write isolates each container from its base image.

03
04
Volumes vs. bind mounts
Hands-on lab
Two ways to persist data outside the container's writable layer, and when to use each.
Run MySQL with and without a volume — observe data loss, then fix it.

CLO835 · Week 3
Agenda
2 / 14

### Notes:

<!-- Slide number: 3 -->
FOUNDATIONS
What is a Docker layer?
A layer is the filesystem change produced by a single instruction in a Dockerfile.

Each FROM, RUN, COPY, or ADD adds a new read-only layer on top of the previous one. The image is the stack.

CMD ["python", "app.py"]
Layer 5 · entrypoint

COPY . /app
Layer 4 · application code

RUN pip install -r requirements.txt
Layer 3 · dependencies

WORKDIR /app
Cached builds

✓
Layer 2 · working dir
Unchanged layers are reused — rebuilds skip work that didn't change.

FROM python:3.12-slim

Layer 1 · base image
Smaller transfers

✓
Pulling an image only downloads layers you don't already have.

Container R/W layer (added when container starts)

Immutability

✓
Layers are read-only. Runtime changes go to a separate writable layer.

CLO835 · Week 3
What is a layer
3 / 14

### Notes:

<!-- Slide number: 4 -->
MECHANICS
Copy-on-Write: how containers stay isolated
Read from a lower layer

1

KEY QUESTION
If a process only reads /etc/config, Docker serves the file directly from the image layer. No copy is made.
What happens to data in the R/W layer when the container is deleted?
Write triggers a copy

2
On first write, the file is copied up into the container's R/W layer. Subsequent writes modify the copy, not the original.

ANSWER
It's gone.

The R/W layer is bound to the container's lifecycle. docker rm deletes the layer and every change it held. The underlying image layers are untouched — and useless for recovering your data.
Lower layers stay clean

3
The image is never mutated. Every container gets its own writable layer on top of the same shared read-only base.

CLO835 · Week 3
Copy-on-write
4 / 14

### Notes:

<!-- Slide number: 5 -->
WHY THIS MATTERS
The problem: containers are ephemeral by default
Scenario
The fix
Mount storage from outside the container
You run MySQL in a container. A user signs up. The row is written to /var/lib/mysql — which lives in the container's R/W layer.

The container crashes. You run docker rm to clean up. You restart MySQL.

The user is gone.
Docker gives you three options to keep data alive past container deletion:

Volumes
Managed by Docker. Best for most cases.

Bind mounts
Map a host path directly. Good for dev.

tmpfs
In-memory only. Sensitive or scratch data.

CLO835 · Week 3
The problem
5 / 14

### Notes:

<!-- Slide number: 6 -->
STORAGE OPTIONS
Volume vs. bind mount vs. tmpfs
|  | Volume | Bind mount | tmpfs |
| --- | --- | --- | --- |
| Location | Docker-managed area on host (/var/lib/docker/volumes) | Any host path you choose | Host RAM only |
| Created with | docker volume create | docker run -v /host:/ctr | --tmpfs /ctr/path |
| Survives container delete? | Yes | Yes | No |
| Survives host reboot? | Yes | Yes | No |
| Portable across hosts? | Yes (volume drivers) | No (tied to host path) | No |
| Best for | Production data (databases, app state) | Live-editing source code during development | Secrets, caches, scratch space |

Rule of thumb:  use volumes in production · use bind mounts while developing on your laptop · use tmpfs for secrets you never want on disk.

CLO835 · Week 3
Storage comparison
6 / 14

### Notes:

<!-- Slide number: 7 -->
DEVELOPER WORKFLOW
Three ways to change code in a container

01
02
03
Rebuild the image
Edit inside the container
Bind-mount your source

› Edit code locally
› docker build  (rebuilds the image)
› docker run    (start a fresh container)
› docker exec -it <ctr> bash
› apt install vim   (install an editor)
› Edit files in place — lost on rm
› docker run -v $(pwd):/app …
› Edit locally with your IDE
› Container sees changes instantly

Cleanest. Slowest feedback loop.
Quick hack. Changes disappear with the container.
Best for active development.

·

!

✓

CLO835 · Week 3
Editing in a container
7 / 14

### Notes:

<!-- Slide number: 8 -->

LAB 02
Hands-on:
Docker Storage
OBJECTIVES
DETAILS
Run MySQL in a container and observe data loss after deletion
Re-run the same workload with a bind mount and prove data survives
Compare the legacy -v flag with the modern --mount flag
Time
~30 minutes
Prereqs
Docker installed; terminal access
Deliverable
Lab notebook with commands, outputs, and answers

### Notes:

<!-- Slide number: 9 -->
LAB · STEP 1 OF 3
Part A — Run MySQL with no persistent storage

GOAL  Create a database, write a row, delete the container, and watch the data disappear.

REFLECT
# 1. Start a MySQL container (no volume, no mount)
$ docker run --name mysql-db -d -e MYSQL_ROOT_PASSWORD=db_clo835 mysql:8

# 2. Open a shell inside the running container
$ docker exec -it mysql-db bash

# 3. Inside the container, create a DB and insert one row
root@ctr:/# mysql -uroot -pdb_clo835
mysql> CREATE DATABASE foo;
mysql> USE foo;
mysql> CREATE TABLE pets (name VARCHAR(20), owner VARCHAR(20), species VARCHAR(20));
mysql> INSERT INTO pets VALUES ('Puffball','Diane','hamster');
mysql> SELECT * FROM pets;   -- confirm the row is there, then exit twice

# 4. Stop and remove the container
$ docker stop mysql-db  &&  docker rm mysql-db
After step 4, you re-run the same command from step 1.
Where is the `pets` table?
Why?

Write your answer in your lab notebook before moving to Part B.

CLO835 · Week 3
Lab · Part A
9 / 14

### Notes:

<!-- Slide number: 10 -->
LAB · STEP 2 OF 3
Part B — Now add a bind mount

GOAL  Repeat Part A, but map /opt/data on the host to MySQL's data directory. Prove the row survives.

EXPECTED
# 1. Prepare the host directory (Docker will create it, but explicit is better)
$ mkdir -p /opt/data

# 2. Run MySQL with a bind mount.  KEEP the same password as Part A.
$ docker run --name mysql-db -d \
    -e MYSQL_ROOT_PASSWORD=db_clo835 \
    -v /opt/data:/var/lib/mysql \
    mysql:8

# 3. Insert a row (same SQL as Part A — see previous slide)
$ docker exec -it mysql-db mysql -uroot -pdb_clo835

# 4. Destroy the container
$ docker stop mysql-db  &&  docker rm mysql-db

# 5. Start a BRAND-NEW container with the same mount and the same password
$ docker run --name mysql-db -d \
    -e MYSQL_ROOT_PASSWORD=db_clo835 \
    -v /opt/data:/var/lib/mysql \
    mysql:8

# 6. Confirm the row is still there — without re-inserting anything
$ docker exec mysql-db mysql -uroot -pdb_clo835 -e "USE foo; SELECT * FROM pets;"
Step 6 should print:

+----------+-------+---------+
| name     | owner | species |
+----------+-------+---------+
| Puffball | Diane | hamster |
+----------+-------+---------+
REFLECT
Where on your host machine does the data actually live? Run `ls /opt/data` and look.

CLO835 · Week 3
Lab · Part B
10 / 14

### Notes:

<!-- Slide number: 11 -->
LAB · STEP 3 OF 3
Part C — The modern --mount syntax

LEGACY:  -v
MODERN:  --mount

$ docker run --name mysql-db -d \
    -e MYSQL_ROOT_PASSWORD=db_clo835 \
    -v /opt/data:/var/lib/mysql \
    mysql:8
$ docker run --name mysql-db -d \
    -e MYSQL_ROOT_PASSWORD=db_clo835 \
    --mount type=bind,\
      source=/opt/data,\
      target=/var/lib/mysql \
    mysql:8
How they differ
|  | -v | --mount |
| --- | --- | --- |
| Verbosity | Short, quick to type | Explicit key=value form |
| Mount types supported | bind, volume | bind, volume, tmpfs |
| Host path missing? | Silently created | Fails fast with a clear error |
| Recommended for | Quick demos | Scripts, Compose files, production |

CLO835 · Week 3
Lab · Modern --mount
11 / 14

### Notes:

<!-- Slide number: 12 -->
LAB · SAFETY NET
Troubleshooting common errors

Bind for 0.0.0.0:3306 failed: port is already allocated
Cause:  Another MySQL (host or container) is already on port 3306.
Fix:  docker ps  →  stop the conflicting container, or publish on a different host port with -p 3307:3306

permission denied while trying to connect to /var/run/docker.sock
Cause:  Your user isn't in the docker group.
Fix:  sudo usermod -aG docker $USER  →  log out and back in

Access denied for user 'root'@'localhost'
Cause:  The password in the new container doesn't match the password used when /opt/data was first initialised.
Fix:  MySQL writes the root password into the data dir on first run. Either reuse the original password, or delete /opt/data and start fresh.

docker: Error response from daemon: invalid mount config
Cause:  Typo in --mount — most often `--mount type=bind,...` missing the space after --mount, or `=` between key and type.
Fix:  Correct form: --mount type=bind,source=/host/path,target=/container/path  (one space after --mount, no = sign before `type`)

CLO835 · Week 3
Troubleshooting
12 / 14

### Notes:

<!-- Slide number: 13 -->
WRAP-UP
Key takeaways

01
Images are stacks of read-only layers.
Each Dockerfile instruction creates one. Caching, sharing, and immutability all flow from this.

02
Containers add a thin R/W layer on top.
Copy-on-write means writes don't touch the image — but the R/W layer dies with the container.

03
Anything you care about lives outside the container.
Use volumes (managed) or bind mounts (host paths) so data survives docker rm.

04
Prefer --mount over -v in new code.
It's explicit, supports all mount types, and fails loudly when the host path is wrong.

CLO835 · Week 3
Takeaways
13 / 14

### Notes:

<!-- Slide number: 14 -->

END OF WEEK 03
Questions?
See you next week.

Good luck,
Professor Maziar
CLO835 · Seneca Polytechnic · ITAS

### Notes:
