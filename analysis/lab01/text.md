<!-- Slide number: 1 -->
# CLO835 – Portable Technologies In Cloud

<!-- Slide number: 2 -->
# Lab1 – Run Docker Containers

![6 quick Docker tips to make managing your containers easier | TechRepublic](Picture2.jpg)

<!-- Slide number: 3 -->

# Run Docker Containers

bash  —  docker

$ docker version
Docker version 29.4.2, build 055a478
$ docker run busybox echo hello world
hello world
$ _
We use Docker Desktop to run containers locally without putting strain on laptop resources.
Prefix Docker commands with sudo when required.

![Docker whale](Graphic81.jpg)

<!-- Slide number: 4 -->

# Run Docker Containers

![](Picture4.jpg)
docker version

![Docker whale](Graphic81.jpg)

<!-- Slide number: 5 -->

# Run Docker Containers
docker run busybox echo hello world

![](Picture4.jpg)

![Docker whale](Graphic81.jpg)

<!-- Slide number: 6 -->

# Run Ubuntu on Docker Containers

bash  —  docker

$ docker run -it ubuntu
root@04c0bb0a6c07:/#
root@04c0bb0a6c07:/# figlet CLO835
bash: figlet: command not found
# Install figlet
root@04c0bb0a6c07:/# apt-get update
root@04c0bb0a6c07:/# apt-get install figlet
root@04c0bb0a6c07:/# figlet CLO835  # Runs successfully
root@04c0bb0a6c07:/# exit
$ figlet CLO835  # not installed on host!
# Re-run container – figlet?
$ docker run -it ubuntu
root@04c0bb0a6c07:/# figlet CLO835
bash: figlet: command not found
root@04c0bb0a6c07:/# _

This is a brand-new container.
It runs a bare-bones, no-frills ubuntu system.
-it is shorthand for -i -t.
-i connects us to the container’s stdin.
-t requests a pseudo-terminal.

![Docker whale](Graphic81.jpg)

<!-- Slide number: 7 -->

# List All Containers

![Docker whale](Graphic81.jpg)
docker ps lists running containers.
Add -a to include stopped ones.
Each row shows the ID, image, command, and exit status.
Names are auto-assigned when not specified.

bash  —  docker

maziar@Firebolt ~ $ docker ps -a
CONTAINER ID  IMAGE    COMMAND              CREATED         STATUS                      NAMES
d58f0bebfd30  ubuntu   "/bin/bash"          6 minutes ago   Exited (0) 2 minutes ago    laughing_poincare
b46d26cee73a  ubuntu   "/bin/bash"          13 minutes ago  Exited (0) 10 minutes ago   inspiring_mahavira
cd3ad4f5dd8a  busybox  "echo hello world"   19 minutes ago  Exited (0) 19 minutes ago   xenodochial_khorana
maziar@Firebolt ~ $ _

<!-- Slide number: 8 -->

# Reattach to an Existing Container
docker run creates a new container — figlet won’t be there.
docker start <id> resumes a stopped container with its files intact.
docker attach <id> reconnects your terminal to it.
Use the ID from: docker ps -a — here, b46d26cee73a.
Now figlet CLO835 runs — the install persisted.

bash  —  docker

$ docker start b46d26cee73a
b46d26cee73a
$ docker attach b46d26cee73a
root@b46d26cee73a:/# figlet CLO835
  ____ _     ___   ___ _________
 / ___| |   / _ \ ( _ )___ / ___|
| |   | |  | | | |/ _ \ |_ \___ \
| |___| |__| |_| | (_) |__) |__) |
 \____|_____\___/ \___/____/____/
root@b46d26cee73a:/# _

![Docker whale](Graphic81.jpg)

<!-- Slide number: 9 -->

# Or Use the Container Name
Every container also gets a friendly auto-name (see the NAMES column).
Names work anywhere an ID works — easier to type and remember.
inspiring_mahavira is the same container as b46d26cee73a.
The prompt still shows the short ID — that’s the container’s hostname.
Set your own name with docker run --name myapp ….

bash  —  docker

$ docker start inspiring_mahavira
inspiring_mahavira
$ docker attach inspiring_mahavira
root@b46d26cee73a:/# figlet CLO835
  ____ _     ___   ___ _________
 / ___| |   / _ \ ( _ )___ / ___|
| |   | |  | | | |/ _ \ |_ \___ \
| |___| |__| |_| | (_) |__) |__) |
 \____|_____\___/ \___/____/____/
root@b46d26cee73a:/# _

![Docker whale](Graphic81.jpg)

<!-- Slide number: 10 -->

# Start and Attach in One Step: -ai
docker start -ai combines start and attach into a single command.
-a attaches your terminal’s output (STDOUT/STDERR); -i attaches input (STDIN) — same flags as run -it.
Works with the container NAME or its ID — both forms are equivalent.
One step instead of two — fewer keystrokes when you’re iterating.

bash  —  docker

# By name
$ docker start -ai inspiring_mahavira
root@b46d26cee73a:/#
# Or by ID — same result
$ docker start -ai b46d26cee73a
root@b46d26cee73a:/# _

![Docker whale](Graphic81.jpg)

<!-- Slide number: 11 -->

![Docker whale](Graphic81.jpg)
# Foreground vs Background Is Arbitrary
The distinction between foreground and background containers is arbitrary.
From Docker’s perspective, all containers are the same they run the same way whether or not a client is attached.
You can always detach from one container and reattach later — to the same one or a different one.
Analogy: attaching to a container is like plugging a keyboard and screen into a physical server. The server runs either way.

bash  —  docker

# Start container with a visible running process
$ docker run -it ubuntu bash -c "while true; do date; sleep 1; done"
Wed May  6 20:00:01 UTC 2026
Wed May  6 20:00:02 UTC 2026
Wed May  6 20:00:03 UTC 2026
# Detach (press Ctrl+P then Ctrl+Q)
^P^Q
# Prove it's still running
$ docker ps
CONTAINER ID   STATUS    NAMES
b46d26cee73a   Up 2m     inspiring_mahavira
# Reattach when you want
$ docker attach inspiring_mahavira
Wed May  6 20:00:47 UTC 2026
Wed May  6 20:00:48 UTC 2026
root@b46d26cee73a:/# _

<!-- Slide number: 12 -->

# Detached Mode, Ports, and Volumes

bash  —  docker

-d runs the container detached — in the background.
-p host:container maps a host port to a container port.
-p 8001:80 exposes nginx on localhost:8001.
-v host:container mounts a host directory into the container.
-v /tmp:/var/lib makes host /tmp appear at /var/lib inside — files persist outside the container.
# Run in the background (-d)
$ docker run -d nginx
9f4b3c8e2a1d…
# Map host:container port (-p)
$ docker run -p 8001:80 -d nginx
c3d4e5f6a7b8…
$ docker ps
CONTAINER ID  IMAGE  PORTS
9f4b3c8e2a1d  nginx  80/tcp
c3d4e5f6a7b8  nginx  0.0.0.0:8001->80/tcp
# Browse to it
$ curl localhost:8001
<h1>Welcome to nginx!</h1>
# Volume Mapping
$ docker run -v /tmp:/var/lib -d nginx
e1a2b3c4d5e6… _

![Docker whale](Graphic81.jpg)

<!-- Slide number: 13 -->

# Container Lifecycle Commands

bash  —  docker
docker attach — reconnect your terminal to a running container.
docker exec — run a new command inside a running container, without touching its main process.
docker stop — send SIGTERM, then SIGKILL after 10 s.
docker start — restart a stopped container; the filesystem is preserved.
docker rm — delete a stopped container (use -f to force-remove a running one).

# attach — reconnect to a running container
$ docker attach inspiring_mahavira
root@b46d26cee73a:/#
# exec — run a NEW command inside
$ docker exec inspiring_mahavira cat /etc/hosts
127.0.0.1   localhost
172.17.0.2  b46d26cee73a
# stop — graceful SIGTERM, then SIGKILL
$ docker stop b46d26cee73a
b46d26cee73a
# start — bring it back, files intact
$ docker start b46d26cee73a
b46d26cee73a
# rm — delete (must be stopped)
$ docker stop b46d26cee73a

![Docker whale](Graphic81.jpg)

<!-- Slide number: 14 -->

# Inspecting Containers

bash  —  docker
docker ps — only the running containers.
docker ps -a — every container, including stopped ones.
docker inspect <id> — full metadata as JSON: state, mounts, network, env.
docker logs <id> — whatever the container wrote to stdout/stderr.

# Running containers only
$ docker ps
CONTAINER ID  IMAGE  STATUS  NAMES
c3d4e5f6a7b8  nginx  Up 3m  eager_kepler
# All containers — including stopped
$ docker ps -a
c3d4e5f6a7b8  nginx    Up 3m       eager_kepler
b46d26cee73a  ubuntu   Exited (0)  inspiring_mahavira
# Full metadata (truncated JSON)
$ docker inspect c3d4e5f6a7b8
[{
  "Id": "c3d4e5f6a7b8…",
  "State": { "Running": true },
  "Image": "nginx",
}]
# stdout / stderr from the container
$ docker logs c3d4e5f6a7b8
nginx: ready for start up
172.17.0.1 - GET / 200
172.17.0.1 - GET /favicon 404
$ _

![Docker whale](Graphic81.jpg)

<!-- Slide number: 15 -->

# Managing Images

bash  —  docker
Images are the templates — containers are running instances of them.
docker images — list every image cached locally.
docker rmi <image> — remove a cached image (no container may be using it).
docker run pulls implicitly if the image is missing, then starts a container.
docker pull <image> — download the image only; no container is created.

# List local images
$ docker images
REPOSITORY  TAG     IMAGE ID      SIZE
ubuntu      latest  a8780b506fa4  77MB
nginx       latest  605c77e624dd  141MB
busybox     latest  3f57d9401f8d  4.86MB
# Remove an image
$ docker rmi ubuntu
Untagged: ubuntu:latest
# run pulls implicitly if missing
$ docker run nginx
Unable to find image 'nginx:latest' locally
latest: Pulling from library/nginx
Status: Downloaded newer image
# pull only — no container created
$ docker pull nginx
Status: Image is up to date
$ _

![Docker whale](Graphic81.jpg)

<!-- Slide number: 16 -->

# Environment Variables and the $VAR Gotcha

bash  —  docker
-e VAR=value sets an environment variable inside the container.
Gotcha: $VAR is expanded by your host shell before docker run ever sees the args.
echo $K8S_COLOR prints the host’s value — not the container’s.
Fix 1: printenv K8S_COLOR — no $, nothing for the host shell to expand.
Fix 2: /bin/sh -c '…' with single quotes — expansion happens inside the container.

# Set a host env var
$ export K8S_COLOR=GREEN
# Surprise: prints GREEN, not BLUE
$ docker run -e K8S_COLOR=BLUE ubuntu echo $K8S_COLOR
GREEN ← the host shell expanded $K8S_COLOR
   before docker ever saw it
# Fix 1: no $ — nothing to expand
$ docker run -e K8S_COLOR=BLUE ubuntu printenv  K8S_COLOR
BLUE
# Fix 2: defer expansion to container
$ docker run -e K8S_COLOR=BLUE ubuntu \
    /bin/sh -c 'echo $K8S_COLOR'
BLUE
$ _

![Docker whale](Graphic81.jpg)

<!-- Slide number: 17 -->
# Lab 1 – The end

![6 quick Docker tips to make managing your containers easier | TechRepublic](Picture2.jpg)

<!-- Slide number: 18 -->
# Run the Hello-World Docker container on Amazon EC2
# Create ssh key pair and Amazon Linux EC2 in a public subnet in default VPC.
# Use the provided Terraform code to deploy the EC2 instance
$ ssh-keygen –t rsa –f week1-dev
$ tf init
$ tf apply –auto-approve

# Log into the instance
$ ssh -i week1-dev <elastic IP>

# Is docker running?
# Install Docker and run Hello-World container
$ sudo yum update -y
$ sudo yum install docker -y
$ sudo systemctl start docker
$ sudo systemctl status docker
$ docker ps # Why does it fail?

<!-- Slide number: 19 -->
# Run the Hello-World Docker container on Amazon EC2

# Who has access to this socket?
$ ls -ltra /var/run/docker.sock

# Add ec2-user to the docker group to enable docker cli use w/o sudo in the next session
$ sudo usermod -a -G docker ec2-user

# Log out of EC2  and log in again
$ docker info
$ docker run  -it -p 80:80 hello-world

# List all the running containers
$ docker ps

# List all the images
$ docker images

![Picture 3](Picture3.jpg)
