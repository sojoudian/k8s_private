<!-- Slide number: 1 -->
1
CLO835, Summer 2022

<!-- Slide number: 2 -->
# Agenda

<!-- Slide number: 3 -->
# Course Outline

### Notes:

<!-- Slide number: 4 -->

![6 quick Docker tips to make managing your containers easier | TechRepublic](Picture2.jpg)
# Lab 1– Docker Networks

<!-- Slide number: 5 -->
# List the networks
$ docker network ls
NETWORK ID NAME DRIVER
6bde79dfcf70 bridge bridge
8d9c78725538 none null
eb0eeab782f4 host host
4c1ff84d6d3f blog-dev overlay
228a4355d548 blog-prod overlay

# Create a new network
$ docker network create [network name]

<!-- Slide number: 6 -->
# What's a network?
Conceptually, a Docker "network" is a virtual switch
(we can also think about it like a VLAN, or a WiFi SSID, for instance)
By default, containers are connected to a single network
 (but they can be connected to zero, or many networks, even dynamically)
Each network has its own subnet (IP address range)
A network can be local (to a single Docker Engine) or global (span multiple hosts)
Containers can have network aliases providing DNS-based service discovery
(and each network has its own "domain", "zone", or "scope")

<!-- Slide number: 7 -->
# Basic Connectivity and DNS
$ docker run -it -d --name ubuntu1 ubuntu
$ docker run -it -d --name ubuntu2 ubuntu
$ docker inspect ubuntu1 # What network is this container using

# Try pinging ubuntu1 from the host using it’s IP and DNS
$ apt install -y iputils-ping – Install Ping utility
$ ping 172.12.0.3
$ ping ubuntu2

# Ty the same from inside the container ubuntu1
$ docker exec -it ubuntu1 /bin/sh
# ping 172.12.0.3
# ping ubuntu2

<!-- Slide number: 8 -->
# Create a new network
docker network create  -d bridge --subnet 182.18.0.0/24 --gateway  182.18.0.1 new-network

# Deploy a mysql database using the mysql:5.6 image and name it mysql-db. Attach it to the newly created network new-networkSet the database password to use db_pass123. The environment variable to set is MYSQL_ROOT_PASSWORD
$ docker run -d -e MYSQL_ROOT_PASSWORD=db_pass123 --name mysql-db --network new-network mysql:5.6

# Run a simple app and link it to DB container
$ docker run --network=new-network -e DB_Host=mysql-db -e DB_Password=db_pass123 -p 38080:8080 --name webapp --link mysql-db:mysql-db -d kodekloud/simple-webapp-mysql

# Can containers on a default “bridge” network connect to containers on “new-network”?

### Notes:

<!-- Slide number: 9 -->
# Connectivity Explained

![Multiple containers on the default bridge network, on a Linux machine](Picture2.jpg)

<!-- Slide number: 10 -->
#

![Multiple containers in multiple bridge networks, on a Linux machine](Picture2.jpg)

<!-- Slide number: 11 -->
# CNM vs CNI
CNM is the model used by Docker
Kubernetes uses a different model, architecture around CNI
(CNI is a kind of API between a container engine and CNI plugins)
Docker model:
multiple isolated networks
per-network service discovery
network interconnection requires extra steps
Kubernetes model:
single flat network
per-namespace service discovery
network isolation requires extra steps (Network Policies)

<!-- Slide number: 12 -->

# Service discovery with containers

Let's try to run an application that requires two containers.
The first container is a web server.
The other one is a redis data store.
We will place them both on the ”new-network” network created before.

![Database](Graphic6.jpg)

<!-- Slide number: 13 -->

$ docker run --net new-network-d -P jpetazzo/trainingwheels
# Check the port that has been allocated to it:

$ docker ps –l

# If we connect to the application now, we will see an error page
# Start the container:
$ docker run --net new-network --net-alias redis -d redis

# That container must be on the same network as the web server.

# It must have the right network alias (redis) so the application can find it. Mind the dot!
$ docker run --net new-network --rm alpine nslookup redis.

<!-- Slide number: 14 -->

![6 quick Docker tips to make managing your containers easier | TechRepublic](Picture2.jpg)

# Lab 1– The End

<!-- Slide number: 15 -->
# Docker Layers
Docker Layers

![](Picture5.jpg)

<!-- Slide number: 16 -->
# COPY ON WRITE

![](Picture5.jpg)
What happens to the modified data in Read Write layer when container is deleted?

<!-- Slide number: 17 -->

# Docker Storage

![Docker Storage. In this section, we will discuss how… | by Sumeet Gyanchandani | Towards Data Science](Picture4.jpg)

![Manage data in Docker | Docker Documentation](Picture6.jpg)

### Notes:
https://docs.docker.com/storage/

<!-- Slide number: 18 -->
# Docker Storage

![](Picture7.jpg)
Docker volume create data_volume
Volume Mount:
Docker run –v data_volume:/var/lib/mysql mysql
Bind Mount:
Docker run –v /data/mysql:/var/lib/mysql mysql

### Notes:
https://docs.docker.com/storage/

<!-- Slide number: 19 -->

# Docker Layers

![Layers of a container based on the Ubuntu image](Picture2.jpg)

![](Picture4.jpg)

<!-- Slide number: 20 -->

# Making changes to the code
Option 1:
Edit the code locally
Rebuild the image
Re-run the container

Option 2:
Enter the container (with docker exec)
Install an editor
Make changes from within the container

Option 3:
Use a bind mount to share local files with the container
Make changes locally
Changes are reflected in the container

<!-- Slide number: 21 -->
# Lab 2 – Docker Storage

![6 quick Docker tips to make managing your containers easier | TechRepublic](Picture2.jpg)

<!-- Slide number: 22 -->

# Running MySQL DB as a container

# Run MySQL DB as a container
$ docker run --name mysql-db -d -e MYSQL_ROOT_PASSWORD=db_clo835 mysql

# Add some data to the DB and print it out
$ docker exec –it mysql-db /bin/bash

# mysql  -uroot –pdb_clo835
# create database foo;
# use foo;
# create table myTable (name VARCHAR(20), owner VARCHAR(20), species VARCHAR(20), sex CHAR(1), birth DATE, death DATE);
# INSERT INTO myTable VALUES ('Puffball','Diane','hamster','f','1999-03-30',NULL);
# select * from myTable;

$ docker exec -it mysql-db mysql -pdb_clo835 -e "use foo; select * from myTable;"

# Stop and delete the container
$ docker stop <container id>
$ docker rm  <container id>
# Explain: What happened to the data when we removed the container and why?

<!-- Slide number: 23 -->
# Running MySQL DB as a Container with a mounted volume
# Add persistent volume binding and re-run
$ docker run --name mysql-db -d -e MYSQL_ROOT_PASSWORD=db_pass123 -v /opt/data:/var/lib/mysql mysql

# Create DB and populate it with some entries
$ docker exec mysql-db /bin/sh
..

# Stop and delete the container
$ docker stop <container id>
$ docker rm  <container id>

# Explain: What happened to the data and why?
$ docker run --name mysql-db -d --env MYSQL_ROOT_PASSWORD=db_pass123 -v /opt/data:/var/lib/mysql mysql
$ docker exec mysql-db mysql –pdb_clo835 –e ’use foo; select * from myTable’

<!-- Slide number: 24 -->

# Running MySQL DB as a Container with a mounted volume
The -v /path/on/host:/path/in/container syntax is the "old" syntax
The modern syntax looks like this:
--mount type=bind,source=/path/on/host,target=/path/in/container
--mount is more explicit, but -v is quicker to type
--mount supports all mount types; -v doesn't support tmpfs mounts
--mount fails if the path on the host doesn't exist; -v creates it
With the new syntax, our command becomes:
$ docker run –mount-type=bind,source=/opt/data,target= /var/lib/mysql -d mysql-db

<!-- Slide number: 25 -->
# Lab 2 – The End

![6 quick Docker tips to make managing your containers easier | TechRepublic](Picture2.jpg)

<!-- Slide number: 26 -->
# Build the Docker Image in Cloud9 Environment
In your Cloud9 environment, change directory and clone our application source repo
https://github.com/jpetazzo/wordsmith

For now, we only care about the first part (about writing Dockerfiles).Place each Dockerfile in its own directory, like this

![](Picture1.jpg)
$ git clone https://github.com/jpetazzo/wordsmith.git
$ cd wordsmith

<!-- Slide number: 27 -->
# Build the Docker Image in Cloud9 and Publish To Amazon ECR
# Verify the image is in Amazon ECR
aws ecr describe-images –repository-name session10-test-dogs

![Picture 7](Picture7.jpg)

<!-- Slide number: 28 -->
# Lab 3 – Build Docker Image and Publish to Amazon ECR with GitHub Actions

![6 quick Docker tips to make managing your containers easier | TechRepublic](Picture2.jpg)

<!-- Slide number: 29 -->
# Build Docker Images with GitHub Actions

![Diagram Description automatically generated](Picture4.jpg)

### Notes:
https://aws.plainenglish.io/build-a-docker-image-and-publish-it-to-aws-ecr-using-github-actions-f20accd774c3

<!-- Slide number: 30 -->

# Create a Fork of the Application Repo

![](Picture11.jpg)

# Fork the repo
https://github.com/luksa/kubernetes-in-action/fork

### Notes:
https://towardsaws.com/build-push-docker-image-to-aws-ecr-using-github-actions-8396888a8f9e

<!-- Slide number: 31 -->
# Create a Repository for  Your Images
# Create an Amazon ECR repository using CLI from your AWS Academy or Cloud9 Terminal
$ aws ecr create-repository \
    --repository-name clo835-week3

# Retrieve temporary credentials from AWS Academy. Select AWS Details and then Click on "Show" under AWS CLI.

![Graphical user interface, application Description automatically generated](Picture4.jpg)

<!-- Slide number: 32 -->

# Update Your Repo with AWS Credentials
In your repository, select Settings Secrets and variables  Actions, click on "New repository secret" and add the secrets below.

![Graphical user interface, application Description automatically generated](Picture4.jpg)

<!-- Slide number: 33 -->

# Create GitHub Actions Workflow
In the forked repo, click on Actions and select "set up workflow yourself"
Copy the workflow from the GitHub link

![](Picture6.jpg)

<!-- Slide number: 34 -->

# Verify that the Docker Image is available in Registry

![](Picture10.jpg)

![](Picture12.jpg)

<!-- Slide number: 35 -->

# Run the container in Cloud9
# Describe Repositories
$ aws ecr describe-repositories
# Export environment variable
$ export ECR={your repository uri}/clo835-week3
Eg: 863587607507.dkr.ecr.us-east-1.amazonaws.com

# Log into docker registry to get permissions to pull an image
$ aws ecr get-login-password --region us-east-1 | docker login -u AWS ${ECR} --password-stdin

# Start the webserver
$ docker run -d -p 80:8080 {your repository uri}/clo835-week3:v0.1

# Verify that the application is running
$ curl localhost
# Explain: how would you run two instances of the same application on the Cloud9 machine? Update the message printed by the application, build a new image and show it in the browser. The new and the old version of the application should run simultaneously.

<!-- Slide number: 36 -->
# Lab 3 – The End

![6 quick Docker tips to make managing your containers easier | TechRepublic](Picture2.jpg)

<!-- Slide number: 37 -->
# Lifecycle

![Picture 4](Picture4.jpg)

<!-- Slide number: 38 -->

# Docker Architecture: Namespaces

Docker takes advantage of Linux namespaces to provide isolated workspace we call "container"

Some namespaces on Linux:

PID namespace for processes isolation (PID: Process ID)

Net namespace for network isolations, manages network interfaces

IPC namespace: inter-process communication

Mnt namespace to manage mount points

### Notes:

<!-- Slide number: 39 -->

# Docker Architecture: Control Groups

Docker engine uses another Linux technology called cgroups or control groups

Cgroups are responsible for limiting resources used by the container

Cgroups ensures that containers are good multi-tenant citizens on the host

Cgroups allow Docker engine to share available VM resources between containers and set limits and constraints, if required

<!-- Slide number: 40 -->
# Docker Engine

Docker Engine is a client server application with the main components below

A server which is a long-running process called Docker daemon

REST API that defines interface that docker client can use to talk to the daemon and instruct it what to do

CLI client

### Notes:

<!-- Slide number: 41 -->

![Picture 4](Picture4.jpg)

# Docker Engine

<!-- Slide number: 42 -->

# Docker commands

![Picture 5](Picture5.jpg)

<!-- Slide number: 43 -->
# Useful links

https://docs.aws.amazon.com/AmazonECS/latest/developerguide/docker-basics.html
https://ecs-cats-dogs.workshop.aws/en/ecr/docker.html
https://blog.aquasec.com/docker-security-best-practices?_ga=2.100580638.1058616926.1651978295-1119178887.1645428243
https://github.com/luksa/kubernetes-in-action
https://towardsaws.com/build-push-docker-image-to-aws-ecr-using-github-actions-8396888a8f9e
https://iximiuz.com/en/posts/container-networking-is-simple/

43
11/12/2021
