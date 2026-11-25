# CLO835 Summer 2026: Final Exam 20% (Questions and Correct Answers)

- Course: Portable Technologies in Cloud (CLO835), Blackboard course CLO835027.MERGED.2264, Summer 2026.
- Test: "Final Exam 20%" in Blackboard Ultra:
  https://learn.senecapolytechnic.ca/ultra/courses/_782173_1/assessment/test/_26573844_1
- Settings in Blackboard: due Mon Jul 13, 2026, 9:59 PM (EDT); time limit 60 minutes, automatic submission;
  1 attempt; access code required; 100 points.
- Questions: 40, 2.5 points each. Types: 26 multiple choice with one correct option, 9 multiple choice with
  more than one correct option (select all), and 5 True/False.
- Blackboard shows the questions and the multiple-choice options to students in a random order. The
  letters A to F in this file follow the order of the instructor view.
- The text of each question and each option is a copy of the Blackboard text, with no change.
- Source: the instructor view (Content and Settings), read on 2026-11-19. A SHA-256 checksum of each
  question (the stem, the options and the correct-answer marks) agrees with the Blackboard page: 40 of 40.

## Answer Key

| Question | Type | Correct answer |
|--:|---|---|
| 1 | Multiple choice, more than one correct option | A, B, E, F |
| 2 | True/False | False |
| 3 | Multiple choice, one correct option | C |
| 4 | Multiple choice, one correct option | B |
| 5 | Multiple choice, more than one correct option | A, C, E, F |
| 6 | Multiple choice, one correct option | A |
| 7 | Multiple choice, one correct option | D |
| 8 | Multiple choice, one correct option | C |
| 9 | Multiple choice, one correct option | C |
| 10 | Multiple choice, one correct option | B |
| 11 | Multiple choice, one correct option | D |
| 12 | Multiple choice, one correct option | A |
| 13 | Multiple choice, one correct option | B |
| 14 | Multiple choice, more than one correct option | A, C, D |
| 15 | True/False | False |
| 16 | Multiple choice, one correct option | B |
| 17 | True/False | True |
| 18 | Multiple choice, more than one correct option | A, B, C, D |
| 19 | Multiple choice, one correct option | C |
| 20 | Multiple choice, one correct option | B |
| 21 | Multiple choice, one correct option | C |
| 22 | True/False | False |
| 23 | Multiple choice, one correct option | C |
| 24 | Multiple choice, more than one correct option | A, B, C |
| 25 | Multiple choice, one correct option | B |
| 26 | Multiple choice, more than one correct option | A, B, C |
| 27 | Multiple choice, one correct option | B |
| 28 | Multiple choice, one correct option | D |
| 29 | Multiple choice, one correct option | A |
| 30 | Multiple choice, one correct option | C |
| 31 | Multiple choice, more than one correct option | A, B, C, E |
| 32 | Multiple choice, one correct option | C |
| 33 | Multiple choice, one correct option | B |
| 34 | Multiple choice, more than one correct option | A, B, E |
| 35 | True/False | True |
| 36 | Multiple choice, one correct option | C |
| 37 | Multiple choice, one correct option | D |
| 38 | Multiple choice, more than one correct option | A, B, C, E |
| 39 | Multiple choice, one correct option | C |
| 40 | Multiple choice, one correct option | B |

## Questions

### Question 1 (Multiple choice, more than one correct option, 2.5 points)

Based on the container lifecycle and CLI slides, select ALL statements that are TRUE.

- A. docker exec runs a new command inside a running container without touching its main process. **(correct)**
- B. docker stop sends SIGTERM and then SIGKILL after 10 seconds if the container has not stopped. **(correct)**
- C. Running docker run against an image reuses the most recent stopped container started from that image.
- D. docker ps with no flags lists stopped containers as well as running ones.
- E. docker start resumes a stopped container with its filesystem intact. **(correct)**
- F. docker rm can remove a running container only if you add the -f flag. **(correct)**

**Correct answer: A, B, E, F**

### Question 2 (True/False, 2.5 points)

True or False: If you run docker run -it ubuntu, install figlet, exit, then run docker run -it ubuntu again, the second container already has figlet installed, because package installs performed in a container are written back into the ubuntu image.

- True
- False **(correct)**

**Correct answer: False**

### Question 3 (Multiple choice, one correct option, 2.5 points)

You start four containers from the same ubuntu:15.04 image. Based on how images and containers relate, which statement is TRUE about disk and memory usage?

- A. Each container copies the entire image filesystem, so four full copies exist on disk.
- B. Copy-on-write duplicates every image layer at container start to guarantee isolation.
- C. The four containers share the read-only image layers, and each gets its own thin read-write layer on top. **(correct)**
- D. All four containers write directly into the shared image layers, so a file created in one appears in the others.

**Correct answer: C**

### Question 4 (Multiple choice, one correct option, 2.5 points)

The Flask image's ENTRYPOINT launches the server with --port=18080, so the app listens on 18080 inside the container. You start it with docker run -d -p 8080:18080 web. From the host, which curl reaches the app and why?

- A. curl http://localhost:18080, because -p reads as 8080:18080 meaning container 8080 maps to host 18080
- B. curl http://localhost:8080, because -p uses HOST:CONTAINER order, so host 8080 forwards to container 18080 **(correct)**
- C. curl http://localhost:8080, because -p uses CONTAINER:HOST order, so container 8080 forwards to host 18080
- D. Either port works, because EXPOSE forces both sides of the mapping to be identical

**Correct answer: B**

### Question 5 (Multiple choice, more than one correct option, 2.5 points)

Select ALL statements about Docker image tags, naming, and registry addresses that are TRUE.

- A. The bare name ubuntu actually resolves to library/ubuntu, i.e. index.docker.io/library/ubuntu **(correct)**
- B. A local image named clo835-week2 can be pushed to Docker Hub exactly as-is, without adding a username/repository namespace prefix
- C. A tag is like a bookmark pointing at a specific image ID; tagging an image adds another tag rather than renaming it **(correct)**
- D. Two different tags can never point to the same image ID, so each tag forces Docker to store a separate copy of the layers
- E. When pushing to a private registry, the registry address is encoded inside the image tag itself, for example registry.example.net:5000/image **(correct)**
- F. Tagging one image as both :v1.0 and :latest can leave both tags pointing at the exact same image ID **(correct)**

**Correct answer: A, C, E, F**

### Question 6 (Multiple choice, one correct option, 2.5 points)

Two images are built from alpine:3.20. Image A ends with CMD ["echo","hello"] and Image B ends with ENTRYPOINT ["echo","hello"]. You then run docker run A goodbye and, separately, docker run B goodbye. What does each container print?

- A. A prints goodbye and B prints hello goodbye **(correct)**
- B. A prints hello goodbye and B prints goodbye
- C. A prints hello and B prints hello, because the run argument is ignored in both
- D. A prints goodbye and B prints goodbye

**Correct answer: A**

### Question 7 (Multiple choice, one correct option, 2.5 points)

Regarding EXPOSE and publishing container ports, which statement is TRUE?

- A. Writing EXPOSE 8080 in the Dockerfile is by itself enough for a client outside the host to reach port 8080
- B. A container port can become public only if it was first declared with EXPOSE and then published with -p
- C. docker run -P (uppercase) publishes only the single lowest-numbered port declared with EXPOSE
- D. docker run -p 8080:80 makes the port public even if the image never declared that port with EXPOSE **(correct)**

**Correct answer: D**

### Question 8 (Multiple choice, one correct option, 2.5 points)

You run docker buildx build --platform linux/amd64,linux/arm64 -t $REPO:v1.0 --push . Which statement about the result is correct?

- A. It produces two separate tags, one per architecture, and clients must choose the right one by hand
- B. Because two platforms are targeted, you must still run docker tag and docker push afterward to upload each variant
- C. It publishes ONE tag backed by a manifest list, and a client automatically pulls the variant that matches its CPU **(correct)**
- D. The --push flag caches both images locally so they can be inspected before any upload happens

**Correct answer: C**

### Question 9 (Multiple choice, one correct option, 2.5 points)

You run docker run -d --name db postgres and docker run -d --name api myapi with no --network flag on either, so both land on the default bridge. Inside api, code tries to open a TCP connection to the hostname db. What happens?

- A. It connects, because the embedded DNS on the default bridge resolves db to its container IP
- B. It connects, because Docker automatically writes every container name into each container's /etc/hosts
- C. It fails to resolve db by name, because embedded DNS name resolution works only on user-defined networks; the containers would have to use IP addresses instead **(correct)**
- D. It fails completely, because containers on the default bridge cannot reach each other at all, even by IP address

**Correct answer: C**

### Question 10 (Multiple choice, one correct option, 2.5 points)

You start docker run -d --network app-net --name web -p 8080:80 nginx, then start a second container named client on the same app-net network. What URL should client use to reach the nginx server?

- A. http://web:8080, because clients must always target the published host port
- B. http://web:80, because container-to-container traffic uses the container's own port via the network's DNS name, and the -p mapping only serves the outside world **(correct)**
- C. http://localhost:8080, because every container on app-net shares the host's localhost
- D. It cannot reach nginx until a second mapping such as -p 80:80 is added to the web container

**Correct answer: B**

### Question 11 (Multiple choice, one correct option, 2.5 points)

A team needs each container to appear as a distinct device on the office physical LAN, with its own MAC address and an IP handed out by the LAN's DHCP server, so external hosts can address each container directly. Which Docker network driver fits this requirement?

- A. host, because it shares the host stack and therefore exposes the host's own MAC and IP to the container
- B. overlay, because it spans multiple machines and assigns each container a routable cluster IP
- C. bridge, because the default isolated virtual switch already places containers on the physical LAN
- D. macvlan, because each container is given its own MAC on the physical network and can pull a real LAN IP **(correct)**

**Correct answer: D**

### Question 12 (Multiple choice, one correct option, 2.5 points)

Comparing Docker's CNM with Kubernetes' CNI as taught, which statement is TRUE?

- A. Kubernetes CNI presents a single flat cluster network where every pod is reachable by default, and isolation must be added explicitly with NetworkPolicy resources **(correct)**
- B. Docker's CNM leaves containers unisolated by default, mirroring Kubernetes' flat-network philosophy
- C. CNM is the plugin-based model driven by CNI plugins, while Kubernetes relies on libnetwork drivers
- D. In Docker CNM, DNS is scoped per namespace, exactly the way Kubernetes scopes cluster DNS

**Correct answer: A**

### Question 13 (Multiple choice, one correct option, 2.5 points)

In the Week 3 lab, Step 2 starts MySQL with --mount type=volume,source=mysql-data,target=/var/lib/mysql and inserts a Puffball row. Step 4 removes that container and restarts MySQL hardened with --mount type=bind,source=$PWD/mysql-data,target=/var/lib/mysql. The Step 5 SELECT then fails with ERROR 1049: Unknown database 'foo'. What best explains this?

- A. --cap-drop=ALL stripped MySQL's permission to read its data files, permanently corrupting the foo database.
- B. The hardened container bind-mounted an empty host directory ($PWD/mysql-data) over /var/lib/mysql, so MySQL initialized a fresh data dir; the Puffball row is still intact on the named volume mysql-data. **(correct)**
- C. The row was written to a tmpfs mount in Step 2, so it vanished the moment the first container was removed.
- D. --security-opt=no-new-privileges blocked MySQL from re-attaching the named volume, which dropped every database.

**Correct answer: B**

### Question 14 (Multiple choice, more than one correct option, 2.5 points)

Select ALL statements that are TRUE about the Week 3 MySQL + Adminer lab and Docker networking as taught.

- A. A user-defined bridge gives containers name-based DNS, so Adminer can reach the database using the server name mysql-db instead of an IP. **(correct)**
- B. The default bridge network provides the same automatic name resolution, so creating clo835-net is optional.
- C. In the hardened setup MySQL's port 3306 is never published to the host; only Adminer's 8080 is exposed. **(correct)**
- D. Containers on clo835-net receive addresses from the 172.28.0.0/16 subnet defined when the network was created. **(correct)**
- E. The overlay driver would be the correct choice here because clo835-net spans a single host.
- F. tmpfs is the recommended mount for the MySQL data directory so the seeded row survives docker rm.

**Correct answer: A, C, D**

### Question 15 (True/False, 2.5 points)

True or False: In the hardened MySQL run, --cap-drop=ALL is used on its own with no --cap-add flags, because MySQL needs no Linux capabilities once the process is not running as root.

- True
- False **(correct)**

**Correct answer: False**

### Question 16 (Multiple choice, one correct option, 2.5 points)

You run docker run -v /srv/missing:/var/lib/mysql mysql:8 where /srv/missing does not exist on the host, then rewrite it as docker run --mount type=bind,source=/srv/missing,target=/var/lib/mysql mysql:8. How do the two commands differ in this exact case?

- A. Both fail identically, because a bind-mount source must always pre-exist on the host.
- B. -v silently creates /srv/missing as an empty directory and mounts it, while --mount fails fast with a clear error because the source path does not exist. **(correct)**
- C. -v fails because it cannot create host paths, while --mount silently creates the missing directory.
- D. Both silently create the directory; the only real difference is that --mount is more verbose to type.

**Correct answer: B**

### Question 17 (True/False, 2.5 points)

True or False: In this course's deployment prerequisites, kubectl and the cluster may differ in MAJOR version, but they should run the same MINOR version.

- True **(correct)**
- False

**Correct answer: True**

### Question 18 (Multiple choice, more than one correct option, 2.5 points)

According to the control-plane-vs-data-plane table, which of the following run on a WORKER node (the data plane)? Select all that apply.

- A. kubelet **(correct)**
- B. kube-proxy **(correct)**
- C. container runtime (containerd / CRI-O) **(correct)**
- D. CNI plugin **(correct)**
- E. kube-scheduler
- F. etcd

**Correct answer: A, B, C, D**

### Question 19 (Multiple choice, one correct option, 2.5 points)

In the lab's kind.yaml the cluster maps containerPort 30000 and 30001 to hostPort 30000 and 30001 via extraPortMappings. What does this accomplish?

- A. It exposes the kube-apiserver to the host on ports 30000-30001.
- B. It gives every pod a routable public IP address.
- C. It makes NodePort Services published on 30000-30001 reachable from the Cloud9 host. **(correct)**
- D. It assigns each node a dedicated /24 pod subnet.

**Correct answer: C**

### Question 20 (Multiple choice, one correct option, 2.5 points)

A Pod runs two containers: web listening on TCP 8080, and a sidecar. Based on how the course describes a Pod's networking, which statement is TRUE?

- A. The sidecar must use the web container's own Pod-internal DNS name to reach it, since each container is assigned its own IP.
- B. The sidecar can reach web at localhost:8080 because both containers share the Pod's single network namespace. **(correct)**
- C. The sidecar can also bind and listen on TCP 8080 at the same time, since each container has its own independent network stack.
- D. Each of the two containers is assigned a separate IP address inside the Pod.

**Correct answer: B**

### Question 21 (Multiple choice, one correct option, 2.5 points)

A ReplicaSet is defined with replicas: 3 and is currently running exactly 3 matching Pods. An admin then manually creates one standalone Pod that happens to carry the exact label the ReplicaSet selects on. What does the ReplicaSet controller do?

- A. Nothing, because the ReplicaSet only counts Pods it originally created from its own template.
- B. It scales the desired count up to 4 so the new Pod is included permanently.
- C. It terminates one Pod so that the current count matches the desired count of 3. **(correct)**
- D. It leaves all 4 Pods running and reports 4/3 ready indefinitely.

**Correct answer: C**

### Question 22 (True/False, 2.5 points)

In the frontend/backend collocation example, the pattern the course recommends is to place the frontend process and the backend process in two separate containers within a single Pod.

- True
- False **(correct)**

**Correct answer: False**

### Question 23 (Multiple choice, one correct option, 2.5 points)

A Deployment currently runs nginx:1.7.0. An operator runs kubectl set image deployment/myapp-deployment nginx=nginx:1.9.1. Which description matches what Kubernetes does?

- A. It edits the pods in the existing ReplicaSet in place, swapping their image without creating any new object.
- B. It requires the deployment to be deleted and re-created before the image change takes effect.
- C. It creates a new deployment revision by rolling out a new ReplicaSet for nginx:1.9.1 while scaling the old ReplicaSet down. **(correct)**
- D. It changes the image only in the YAML file and waits for the next kubectl apply to actually roll it out.

**Correct answer: C**

### Question 24 (Multiple choice, more than one correct option, 2.5 points)

Based on the Rollout and Recreate strategy slides, select ALL statements that are TRUE.

- A. RollingUpdate is the default rollout strategy. **(correct)**
- B. The Recreate strategy causes application downtime and should be specified explicitly. **(correct)**
- C. During a RollingUpdate the load balancer serves traffic to both old and new pods until the rollout completes. **(correct)**
- D. Recreate is the default strategy, so RollingUpdate must instead be requested explicitly.
- E. RollingUpdate necessarily incurs a brief application downtime while the pods swap over.
- F. The Recreate strategy upgrades pods one at a time specifically to avoid any downtime.

**Correct answer: A, B, C**

### Question 25 (Multiple choice, one correct option, 2.5 points)

During a rollout, kubectl rollout status deployment/myapp-deployment prints: Waiting for rollout to finish: 9 of 10 updated replicas are available... Which statement best describes this state?

- A. The rollout has failed because only 9 of the intended 10 replicas will ever come up.
- B. The rollout is still in progress: 9 of the 10 new-version replicas are up and Kubernetes is waiting for the 10th before reporting success. **(correct)**
- C. There are 9 old-version pods still serving traffic and only 1 new-version pod has been created so far.
- D. The deployment is permanently stuck at 90 percent and requires a manual restart to continue.

**Correct answer: B**

### Question 26 (Multiple choice, more than one correct option, 2.5 points)

Select ALL statements that are TRUE according to the lecture.

- A. The Endpoints resource is built from the service's selector and holds the IP and port pairs of the matching pods. **(correct)**
- B. When a client connects to a service, the service proxy selects one of the endpoint IP:port pairs and redirects the connection to it. **(correct)**
- C. A ClusterIP is a virtual IP that no process, network namespace, or interface actually owns. **(correct)**
- D. A NodePort service lets you freely choose any node port, such as 80 or 8080, to match the container.
- E. A LoadBalancer service provisions a working external load balancer even when the underlying infrastructure offers no load-balancer service.

**Correct answer: A, B, C**

### Question 27 (Multiple choice, one correct option, 2.5 points)

A Service manifest declares spec.ports with port: 80 and targetPort: 8080, no type field, and selector app: kubia. Which statement correctly describes how port and targetPort behave?

- A. port 80 is the container's listening port, and targetPort 8080 is the port on the service's virtual IP.
- B. Clients connect to the service's virtual IP on port 80, and the service forwards those requests to the pods' container port 8080. **(correct)**
- C. port and targetPort must be set to the same value or the API server rejects the Service.
- D. targetPort 8080 is the external node port that clients outside the cluster connect to.

**Correct answer: B**

### Question 28 (Multiple choice, one correct option, 2.5 points)

You run: k expose deployment blue --type=NodePort --port=80. Which statement about the resulting Service is TRUE?

- A. The NodePort type replaces the ClusterIP, so the service no longer has a cluster-internal virtual IP.
- B. You can set the node port to 8080 so it matches the container's listening port.
- C. The node port is opened only on the single node where the backing pod is scheduled.
- D. A ClusterIP service is also created automatically, and the externally reachable port is allocated from the 30000-32767 range. **(correct)**

**Correct answer: D**

### Question 29 (Multiple choice, one correct option, 2.5 points)

Which statement about kube-proxy and Services is TRUE?

- A. kube-proxy programs iptables rules on every node but does not itself perform the actual packet routing. **(correct)**
- B. kube-proxy is a per-node userspace process that every packet destined for a Service is routed through.
- C. A Service is a real process with its own network namespace and interface that kube-proxy launches.
- D. kube-proxy runs only on the control-plane node and pushes rules to the workers from there.

**Correct answer: A**

### Question 30 (Multiple choice, one correct option, 2.5 points)

A Service named web-service lives in the namespace apps. From a pod in a different namespace, which fully qualified in-cluster DNS name resolves to that service?

- A. web-service.svc.apps.cluster.local
- B. apps.web-service.svc.cluster.local
- C. web-service.apps.svc.cluster.local **(correct)**
- D. web-service.default.svc.cluster.local

**Correct answer: C**

### Question 31 (Multiple choice, more than one correct option, 2.5 points)

Select ALL statements that are TRUE according to the Volumes lecture.

- A. A hostPath volume mounts a directory from the worker node's filesystem into the Pod. **(correct)**
- B. For remote storage such as EBS, the volume is attached (not created) when the Pod starts and detached (not destroyed) when the Pod is destroyed. **(correct)**
- C. An emptyDir volume shadows the directory in the container image at the point where it is mounted. **(correct)**
- D. A Volume can be enumerated as a cluster API resource via kubectl get volumes.
- E. configMap and secret volumes are special volume types used to expose Kubernetes resources and cluster information to the Pod. **(correct)**
- F. A gitRepo volume is the modern, recommended volume type for delivering application code.

**Correct answer: A, B, C, E**

### Question 32 (Multiple choice, one correct option, 2.5 points)

A student claims they can audit every volume in the cluster by running kubectl get volumes, and that a PersistentVolume can be attached straight to a Pod the same way an emptyDir is. Based on how the course distinguishes Volumes from PersistentVolumes, which statement is actually TRUE?

- A. You can list a Pod's volumes cluster-wide with kubectl get volumes because volumes are namespaced API objects.
- B. A PersistentVolume is attached to a Pod directly in the pod spec, exactly like an emptyDir.
- C. A Volume is defined inside the Pod spec and is not itself a queryable API resource, whereas a PersistentVolume is an API resource consumed by a Pod only through a PersistentVolumeClaim. **(correct)**
- D. Both Volumes and PersistentVolumes are cluster-scoped API resources returned by kubectl get pv.

**Correct answer: C**

### Question 33 (Multiple choice, one correct option, 2.5 points)

A container writes session files into an emptyDir volume. First its main process crashes and the kubelet restarts the container in place (same node, same Pod). Later, the entire Pod is deleted and rescheduled onto another node. What happens to the files in each case?

- A. The files are lost on the container restart but persist through the Pod deletion.
- B. The files survive the container restart but are lost when the Pod is deleted. **(correct)**
- C. The files survive both events because emptyDir is permanently backed by node disk.
- D. The files are lost in both cases because emptyDir storage is scoped to a single container.

**Correct answer: B**

### Question 34 (Multiple choice, more than one correct option, 2.5 points)

Per the slides on the control-plane vs data-plane split and access, which of the following are responsibilities that AWS handles for you (NOT the customer)? Select all that apply.

- A. Scaling, monitoring, and patching the control plane **(correct)**
- B. Keeping the API server, scheduler, controllers, and etcd running **(correct)**
- C. Scaling the workloads and configuring the applications
- D. Provisioning and maintaining the worker nodes' operating system in self-managed EC2
- E. Providing multi-AZ high availability for the control plane **(correct)**

**Correct answer: A, B, E**

### Question 35 (True/False, 2.5 points)

True or False: In EKS, 'aws eks update-kubeconfig' wires kubectl to the cluster using your AWS IAM identity, but IAM only establishes WHO you are, while WHAT you can do inside the cluster is governed by Kubernetes RBAC.

- True **(correct)**
- False

**Correct answer: True**

### Question 36 (Multiple choice, one correct option, 2.5 points)

A team runs 3 separate EKS clusters in us-east-1, each with worker nodes, for 730 hours in a month. Using the pricing model taught in the slides, what is the monthly charge attributable ONLY to the EKS cluster (control plane) portion, before any node costs?

- A. 73.00 USD
- B. 146.00 USD
- C. 219.00 USD **(correct)**
- D. 0.00 USD because the control plane is free and only nodes are billed

**Correct answer: C**

### Question 37 (Multiple choice, one correct option, 2.5 points)

You deploy a standard Deployment (not a StatefulSet) with replicas: 3, whose pod template mounts a single PersistentVolumeClaim. According to the lecture, what is TRUE of the result?

- A. Each of the 3 pods automatically gets its own separate PVC and PersistentVolume.
- B. The pods are created one at a time in sequence, pod-0 fully ready before pod-1 starts.
- C. Each pod receives a stable, ordinal hostname such as web-0, web-1, and web-2.
- D. All 3 replicas are identical and mount the same single volume, because the volume is defined at the pod-template level. **(correct)**

**Correct answer: D**

### Question 38 (Multiple choice, more than one correct option, 2.5 points)

Select ALL statements that are TRUE about StatefulSets as taught in the lecture and lab.

- A. Each pod is assigned an ordinal index that starts at 0 and increments by 1. **(correct)**
- B. A pod that is deleted and rescheduled keeps the same name and reattaches to the same PVC/storage. **(correct)**
- C. The per-replica PVCs are created by the StatefulSet through a volumeClaimTemplate rather than being created separately. **(correct)**
- D. All pods in a StatefulSet are created in parallel to speed up startup.
- E. Pods are scaled up and down in order, gracefully, one at a time. **(correct)**
- F. Every pod shares one single PVC, exactly like a Deployment does.

**Correct answer: A, B, C, E**

### Question 39 (Multiple choice, one correct option, 2.5 points)

A PersistentVolume is defined with accessModes listing both ReadWriteOnce and ReadOnlyMany. Based on how the lecture describes these access modes, which statement is TRUE about how this volume may be consumed?

- A. It can be mounted read-write by many clients simultaneously across different nodes.
- B. ReadWriteOnce means the volume may only ever be mounted read-only, and only one time.
- C. It can be mounted read-write by a single client, or read-only by many clients. **(correct)**
- D. ReadOnlyMany permits many clients to mount the volume read-write at the same time.

**Correct answer: C**

### Question 40 (Multiple choice, one correct option, 2.5 points)

Which statement about the headless Service used to expose a StatefulSet is TRUE as described in the lecture?

- A. It is a normal ClusterIP Service that load-balances write traffic evenly across all the MySQL pods.
- B. It is defined with clusterIP: None and gives each pod a stable DNS name such as mysql-0.mysql-h.default.svc.cluster.local, without load-balancing. **(correct)**
- C. It assigns one shared virtual IP that every pod answers on, chosen at random per request.
- D. It is needed only for Deployments and provides no benefit for StatefulSets.

**Correct answer: B**
