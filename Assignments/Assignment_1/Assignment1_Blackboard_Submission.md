# Assignment 1: Create a Dockerfile, Build a Docker Image, and Run Containers Locally with Docker Hub

**Value:** 15% of the final grade
**Due:** the week of September 25

## What You Build

A two-tier web application:

- a Flask web tier;
- a MySQL data tier.

Each tier runs in its own container. Both containers run on a custom Docker
bridge network.

Start from this code:
https://github.com/sojoudian/CLO835_Fall_2026/tree/master/assignment-1

You may use your own two-tier application instead.

## The Order of the Work

Keep this order. You cannot pull an image before the push creates it.

1. **Build** the two images with the Docker CLI.
2. **Push** the two images to your own Docker Hub repositories.
3. **Pull** the two images back with `docker pull`.
4. **Run** the containers.

## The Four Parts

### 1. Build and Push the Images
Build both images with the Docker CLI, and push them to your own Docker Hub
repositories.

Before you push, run `docker images` and confirm that the web image and the
MySQL image show **different IMAGE IDs**. The MySQL image is about 1 GB, and the
web image is about 380 MB. One wrong `docker tag` command publishes the same
image two times, and the database container then starts a web server.

### 2. Run Three Web Application Instances
Run three instances of the web application on one host:

- `blue` on port 8081;
- `pink` on port 8082;
- `lime` on port 8083.

### 3. Update and Redeploy
Update the application, rebuild the image, push it to Docker Hub, and redeploy.

### 4. Use Docker Compose
Define the whole stack in a Docker Compose file, and bring it up with one
command.

## What to Submit

Submit all of the following:

- a link to your public GitHub repository with the source code and the
  Dockerfiles;
- links to your Docker Hub repositories for the webapp image and the MySQL
  image;
- a recording, 15 minutes or less, that follows the script below;
- a report that describes the problems you met and how you solved them.

**Important:** a submission without the report is not satisfactory.

## Recording Requirements

The recording must show all of the following, in this order:

1. You build both images locally, after you merge your changes into the master
   branch.
2. You push both images to Docker Hub.
3. You pull both images back with `docker pull`.
4. The MySQL container runs on a custom bridge network, and you connect to the
   database.
5. Three webapp containers run at the same time:
    - `blue` on port 8081;
    - `pink` on port 8082;
    - `lime` on port 8083.
6. The three pages answer from your own machine, in a browser or with `curl`.
7. The containers reach each other by name, for example `ping pink` from inside
   `blue`.
8. You explain why three applications can all listen on port 8080 on one host.
9. You bring the whole stack up with `docker compose up -d`, and you show both
   services running.

The list is a checklist of what the recording must demonstrate. Keep the build,
push and pull steps in the order above.

## Two Rules

- Every commit must carry a date before the due date.
- Never commit a Docker Hub password or an access token.

## Grade Breakdown

| Requirement | Marks |
|---|---|
| Dockerfiles build both images, and the images reach Docker Hub | 10 |
| GitHub repository configured, master branch protected, no credentials in the repo | 5 |
| Both images built with the Docker CLI and published to Docker Hub | 10 |
| Images pulled from Docker Hub onto the host | 5 |
| MySQL container runs on a custom bridge network, and you connect to it | 15 |
| Three containers run at once on 8081, 8082 and 8083, and answer from your machine | 20 |
| Containers reach each other by name | 10 |
| You explain the shared port 8080 | 10 |
| A Docker Compose file brings both services up with one command | 15 |
| **Total** | **100** |

## Integrity Pledge

By submitting my assignment, I affirm that I will not give or receive any
unauthorized help in this submission, and that all work provided is my own. I
agree to abide by Seneca's Academic Integrity Policy.

## Plagiarism

A plagiarized assignment receives a mark of zero on the assignment and a failing
grade in the course. You may also receive a permanent note of plagiarism on your
academic record.
