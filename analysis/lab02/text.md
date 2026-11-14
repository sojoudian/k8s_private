<!-- Slide number: 1 -->

![../docker_logo.jpg](Image0.jpg)
CLO835 — Lab 2
Environment Variables, CMD / ENTRYPOINT,
and Publishing Docker Images to Docker Hub

### Notes:

<!-- Slide number: 2 -->

✓

CONTAINERS
WEEK 2
concepts & hands-on
lab 2

![../whale_icon.png](Image0.jpg)
CLO835, Fall 2026
2

### Notes:

<!-- Slide number: 3 -->
Agenda

App 1 — build a vanilla Flask image from scratch

Dockerfile fundamentals: CMD vs ENTRYPOINT

Why env vars matter: an image that refuses to start without one

App 2 — recolour simple-webapp-color at run time

Pass env vars at run time: -e and --env-file

Bake defaults into the image with ENV — and override them

Verify env vars with docker inspect and docker exec env

Publish: docker login → tag → push → multi-arch with buildx

![../whale_icon.png](Image0.jpg)
CLO835, Fall 2026
3

### Notes:

<!-- Slide number: 4 -->

1
App 1 — simple-webapp-flask
Build a Flask image end-to-end before we touch a single env var

![../whale_icon.png](Image0.jpg)
CLO835, Fall 2026
4

### Notes:

<!-- Slide number: 5 -->
From source to running container

Clone
git clone github.com/sojoudian/simple-webapp-flask

Probe
Run ubuntu:22.04 interactively and install Python + Flask by hand

Author
Translate the proven install steps into a Dockerfile

Build
docker build . -t clo835-week2

Test
curl http://<container-ip>:8080 — expect a Welcome response

Verify
Confirm the image runs the same way on a clean host

![../whale_icon.png](Image0.jpg)
CLO835, Fall 2026
5

### Notes:

<!-- Slide number: 6 -->
Clone the repo, then prove it works by hand
Pull the source from GitHub: github.com/sojoudian/simple-webapp-flask.
Before writing a Dockerfile, prove every install step on a throw-away ubuntu:22.04 container.
If you can run flask manually inside a container, the Dockerfile is just a transcript of those commands.
Hit the running app from a second shell with curl to confirm it answers on port 5000.

bash  —  docker

# 1. grab the source on the host
$ git clone https://github.com/sojoudian/simple-webapp-flask
$ cd simple-webapp-flask

# 2. probe interactively in a disposable container
$ docker run --rm -it -p 18080:18080 -v .:/host ubuntu:22.04 bash root@c1f0:/# apt-get update -y
root@c1f0:/# apt-get install -y python3 python3-pip git
root@c1f0:/# pip3 install flask
root@c1f0:/# cp /host/app.py /opt/   # (or paste the file)
root@c1f0:/# cd /opt && FLASK_APP=app.py flask run --host=0.0.0.0 --port=18080

# 3. from another terminal on the host
$ curl http://localhost:18080
Welcome to CLO835!

![../whale_icon.png](Image0.jpg)
CLO835, Fall 2026
6

### Notes:

<!-- Slide number: 7 -->
Turn the proven steps into a Dockerfile
FROM picks the base image — match the OS you probed on.
Each RUN is one of the apt-get / pip commands you ran by hand.
COPY brings your application code into the image at build time.
ENTRYPOINT defines the long-running process — Flask, serving on 0.0.0.0:18080.
WORKDIR keeps later commands tidy: no more cd /opt sprinkled everywhere.

Dockerfile

FROM ubuntu:22.04

RUN apt-get update -y \
 && apt-get install -y python3 python3-pip \
 && rm -rf /var/lib/apt/lists/*

RUN pip3 install flask

WORKDIR /opt
COPY app.py .

EXPOSE 18080
ENTRYPOINT ["flask", "run", "--host=0.0.0.0", "--port=18080"]
ENV FLASK_APP=app.py

![../whale_icon.png](Image0.jpg)
CLO835, Fall 2026
7

### Notes:

<!-- Slide number: 8 -->
CMD vs ENTRYPOINT — what really happens at run time
CMD = the default command. Anything you type after the image name REPLACES it entirely.
ENTRYPOINT = the fixed program. Anything you type after the image name is APPENDED to it as arguments.
Rule of thumb: ENTRYPOINT is what the container IS; CMD is what it does by default.
Two tiny images make the contrast obvious — same base, same command, different keyword.

bash  —  docker

# --- image A: CMD only ---
FROM alpine:3.20
CMD ["echo", "hello"]

$ docker run cmd-demo            # → hello
$ docker run cmd-demo goodbye    # → goodbye   (CMD replaced)

# --- image B: ENTRYPOINT only ---
FROM alpine:3.20
ENTRYPOINT ["echo", "hello"]

$ docker run entry-demo          # → hello
$ docker run entry-demo goodbye  # → hello goodbye (appended)

![../whale_icon.png](Image0.jpg)
CLO835, Fall 2026
8

### Notes:

<!-- Slide number: 9 -->
Build the image, run it, prove it answers
docker build . -t clo835-week2 turns the Dockerfile into a tagged local image.
Run detached with -d and publish the container port to a host port with -p HOST:CONTAINER.
Hit the host port from your browser or curl. A 200 means the image is portable.
docker logs <id> is your first stop when anything misbehaves.

bash  —  docker

# build
$ docker build . -t clo835-week2

$ docker images | grep clo835-week2
REPOSITORY      TAG     IMAGE ID       SIZE
clo835-week2    latest  d499aabc96e2   456MB

# run and publish port 8080
$ docker run -d -p 18080:18080 --name web clo835-week2
f0a1b2c3d4e5...

$ curl -s http://localhost:18080
Welcome to CLO835!

$ docker logs web | tail -2
 * Running on http://0.0.0.0:18080

![../whale_icon.png](Image0.jpg)
CLO835, Fall 2026
9

### Notes:

<!-- Slide number: 10 -->

⚙
Environment variables
Motivate it, see it, then formalise the mechanics

![../whale_icon.png](Image0.jpg)
CLO835, Fall 2026
10

### Notes:

<!-- Slide number: 11 -->
Why do we even need env vars? Some images refuse to start without them
Run postgres with nothing extra and the container exits immediately.
docker logs reveals the real error: a required env var was not supplied.
This is by design — the image won't ship with a default password baked in.
Re-run with -e POSTGRES_PASSWORD=... and the container becomes healthy in seconds.

bash  —  docker

$ docker run -d --name pg postgres:16
8c4a92ff77ce...

$ docker ps -a | grep pg
8c4a92ff77ce  postgres:16  Exited (1) 2 seconds ago

$ docker logs pg | tail -3
Error: Database is uninitialized and superuser password is
not specified.  You must specify POSTGRES_PASSWORD to a
non-empty value for the superuser.

# now provide the required env var
$ docker rm pg && docker run -d --name pg \
      -e POSTGRES_PASSWORD=clo835-secret postgres:16

$ docker ps --format '{{.Names}}  {{.Status}}'
pg  Up 6 seconds (healthy)

![../whale_icon.png](Image0.jpg)
CLO835, Fall 2026
11

### Notes:

<!-- Slide number: 12 -->
See it in action: recolour simple-webapp-color at run time
Clone github.com/sojoudian/simple-webapp-color — the repo already ships a working Dockerfile.
The Dockerfile has ONE default (ENV APP_COLOR=teal). The Flask app reads os.environ['APP_COLOR'] at request time.
Run the same image twice with different -e APP_COLOR=... values — different pages, same bytes on disk.
Don't worry about the flags yet — the next three slides will dissect exactly what -e, ENV, and inspect are doing here.

bash  —  docker

$ git clone https://github.com/sojoudian/simple-webapp-color
$ cd simple-webapp-color && docker build -t color_app .

# default — page renders teal
$ docker run -d -p 8080:8080 --name c1 color_app

# override to magenta — same image, different env
$ docker run -d -p 8081:8080 \
    -e APP_COLOR=blue --name c2 color_app

$ curl -s http://localhost:8080 | grep -o 'bg-[a-z]*'
background: #e74c3c
$ curl -s http://localhost:8081 | grep -o 'bg-[a-z]*'
background: #2980b9

![../whale_icon.png](Image0.jpg)
CLO835, Fall 2026
12

### Notes:

<!-- Slide number: 13 -->
Now the catalog: passing env vars at run time with -e and --env-file
-e KEY=value sets one variable for the running container — repeatable, exactly as you saw on slides 11 and 12.
-e KEY (no =value) forwards the value from your host shell. Handy for secrets you don't want in shell history.
--env-file=path loads many KEY=value pairs from a text file (one per line, no quotes needed).
All three take effect for THIS run only — they do not modify the image.

bash  —  docker

# several at once + forward from host shell
$ export DB_PASSWORD=hunter2
$ docker run \
    -e APP_MODE=demo \
    -e DB_USER=postgres \
    -e DB_PASSWORD \
    color_app

# bulk-load from a file
$ cat env.list
APP_COLOR=red
APP_MODE=demo
DB_USER=postgres

$ docker run --env-file=env.list color_app

![../whale_icon.png](Image0.jpg)
CLO835, Fall 2026
13

### Notes:

<!-- Slide number: 14 -->

⇧
Publish to Docker Hub
docker login  →  tag  →  push  →  multi-arch with buildx

![../whale_icon.png](Image0.jpg)
CLO835, Fall 2026
16

### Notes:

<!-- Slide number: 15 -->
Authenticate the Docker CLI to Docker Hub
Create a free account at hub.docker.com, then a public repository named after your image (e.g. maziar/clo835-flask).
Go to Account Settings → Security → New Access Token. Treat the token like a password.
docker login -u <username> prompts for the token and caches it under ~/.docker/config.json.
For CI: pipe the token in over stdin so it never lands in shell history.

bash  —  docker

# interactive — paste the PAT when prompted
$ docker login -u maziar
Password: ********
Login Succeeded

# non-interactive, for CI / scripts
$ echo "$DOCKERHUB_TOKEN" \
    | docker login -u maziar --password-stdin

# remember the repo name for the next slides
$ export REPO=maziar/clo835-flask

# log out when you're done on a shared machine
$ docker logout

![../whale_icon.png](Image0.jpg)
CLO835, Fall 2026
17

### Notes:

<!-- Slide number: 16 -->
Tag, push, verify — your image is now globally pullable
Local image names like clo835-week2 don't fit Docker Hub's namespace — tag the image as <user>/<repo>:<version>.
docker push streams the layers up. Layers your image shares with other images on Hub upload almost instantly.
Verify the tag on hub.docker.com — and prove it's pullable from a clean machine before declaring victory.
Same workflow for color_app: tag → push → done.

bash  —  docker

# tag the local image with the Hub repo + version
$ docker tag clo835-week2 "$REPO:v1.0"
$ docker tag clo835-week2 "$REPO:latest"

$ docker images | grep clo835-flask
maziar/clo835-flask  v1.0     d499aabc96e2
maziar/clo835-flask  latest   d499aabc96e2

# push
$ docker push "$REPO:v1.0"
v1.0: digest: sha256:27669... size: 1372
$ docker push "$REPO:latest"

# prove anyone can now pull it
$ docker rmi "$REPO:v1.0"
$ docker pull "$REPO:v1.0"
Status: Downloaded newer image for maziar/clo835-flask:v1.0

![../whale_icon.png](Image0.jpg)
CLO835, Fall 2026
18

### Notes:

<!-- Slide number: 17 -->
One image, every architecture — docker buildx
Reality of 2026: laptops are ARM64 (Apple Silicon), most servers are still AMD64 (x86). A single-arch image breaks on the other side.
buildx publishes ONE tag that carries multiple platform variants under a manifest list — clients pull the variant that fits their CPU.
--push tells buildx to skip the local cache and upload straight to the registry. No separate docker tag / docker push step needed.
Verify the multi-arch manifest with docker buildx imagetools inspect — both platforms should be listed.

bash  —  docker

# one-time: create a builder that supports multi-arch
$ docker buildx create --name multi --use
$ docker buildx inspect --bootstrap

# build for BOTH architectures and push in one shot
$ docker buildx build \
    --platform linux/amd64,linux/arm64 \
    -t "$REPO:v1.0" \
    --push .

# confirm the manifest contains both variants
$ docker buildx imagetools inspect "$REPO:v1.0"
Name:      docker.io/maziar/clo835-flask:v1.0
MediaType: application/vnd.docker.distribution.manifest.list.v2+json
Manifests:
  - Platform: linux/amd64
  - Platform: linux/arm64

![../whale_icon.png](Image0.jpg)
CLO835, Fall 2026
19

### Notes:

<!-- Slide number: 18 -->
Lab 2 — wrap-up
From an empty directory to a published, env-driven image.

Built

Configured

Shipped
simple-webapp-flask
vanilla Flask image
(Dockerfile from scratch)
simple-webapp-color
env vars at run time
verified with inspect / exec
docker login + PAT
tag → push → pull
multi-arch via buildx
Next: orchestrate these images on Kubernetes (EKS).

![../docker_logo.jpg](Image0.jpg)

![../whale_icon.png](Image1.jpg)
CLO835, Fall 2026
20

### Notes:
