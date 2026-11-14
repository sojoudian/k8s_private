# CLO835 Final Exam - Answer Key & Rationale

**40 questions** grounded in the finalWork course slides. Type mix: 26 multiple-choice, 9 multiple-answer (select all), 5 true/false.

## How to upload to Blackboard Ultra

1. In your Ultra course, open the **Tests** tool (or a Test/Question Bank) and choose **Create** or open an existing test.
2. Use **Upload Questions** (Original courses: *Tests, Surveys, and Pools -> Build/Upload Questions*; Ultra: create a test, then the **plus -> Upload questions** option) and select `CLO835_Final_Exam_Blackboard.txt`.
3. Set the **points per question** in the upload dialog (e.g. 2 points x 50 = 100).
4. Review the imported questions, then Submit. Blackboard randomizes answer order on display by default, so the option order in the file does not leak the key.

The `.txt` is the file you upload. This answer key is for your review only - do not upload it.

---

### Q1. [MA] (very_hard, source: Lab01 slides 07, 13; Week01 slide 32)

Based on the container lifecycle and CLI slides, select ALL statements that are TRUE.

- A. docker exec runs a new command inside a running container without touching its main process. **(CORRECT)**
- B. docker stop sends SIGTERM and then SIGKILL after 10 seconds if the container has not stopped. **(CORRECT)**
- C. Running docker run against an image reuses the most recent stopped container started from that image.
- D. docker ps with no flags lists stopped containers as well as running ones.
- E. docker start resumes a stopped container with its filesystem intact. **(CORRECT)**
- F. docker rm can remove a running container only if you add the -f flag. **(CORRECT)**

_Rationale:_ exec adds a command to a running container, stop is a graceful SIGTERM then SIGKILL after 10s, start resumes a stopped container with files intact, and rm needs -f to force-remove a running one. docker run always creates a NEW container (it never reuses a stopped one), and plain docker ps hides stopped containers unless you add -a.

### Q2. [TF] (very_hard, source: Lab01 slide 06; Week01 slide 33)

True or False: If you run docker run -it ubuntu, install figlet, exit, then run docker run -it ubuntu again, the second container already has figlet installed, because package installs performed in a container are written back into the ubuntu image.

- Answer: **False**

_Rationale:_ False: each docker run makes a brand-new container whose changes live only in that container's read-write layer; images are immutable, so the install is never written back and the second container reports 'figlet: command not found'.

### Q3. [MC] (hard, source: Week01 slides 28, 31)

You start four containers from the same ubuntu:15.04 image. Based on how images and containers relate, which statement is TRUE about disk and memory usage?

- A. Each container copies the entire image filesystem, so four full copies exist on disk.
- B. Copy-on-write duplicates every image layer at container start to guarantee isolation.
- C. The four containers share the read-only image layers, and each gets its own thin read-write layer on top. **(CORRECT)**
- D. All four containers write directly into the shared image layers, so a file created in one appears in the others.

_Rationale:_ An image is a read-only stack of layers; each container adds a thin read-write layer via copy-on-write, so the heavy image layers are shared and not recopied. The 'write directly into shared layers' option is wrong because writes go to each container's private R/W layer, keeping containers isolated.

### Q4. [MC] (very_hard, source: Week02 slides 24 and 26)

The Flask image's ENTRYPOINT launches the server with --port=18080, so the app listens on 18080 inside the container. You start it with docker run -d -p 8080:18080 web. From the host, which curl reaches the app and why?

- A. curl http://localhost:18080, because -p reads as 8080:18080 meaning container 8080 maps to host 18080
- B. curl http://localhost:8080, because -p uses HOST:CONTAINER order, so host 8080 forwards to container 18080 **(CORRECT)**
- C. curl http://localhost:8080, because -p uses CONTAINER:HOST order, so container 8080 forwards to host 18080
- D. Either port works, because EXPOSE forces both sides of the mapping to be identical

_Rationale:_ The -p flag is HOST:CONTAINER, so 8080:18080 forwards host port 8080 to the container's 18080 where Flask listens; options 1 and 3 invert the order, and EXPOSE never equalizes the two sides.

### Q5. [MA] (very_hard, source: Week02 slide 17 and Lab02 slide 18)

Select ALL statements about Docker image tags, naming, and registry addresses that are TRUE.

- A. The bare name ubuntu actually resolves to library/ubuntu, i.e. index.docker.io/library/ubuntu **(CORRECT)**
- B. A local image named clo835-week2 can be pushed to Docker Hub exactly as-is, without adding a username/repository namespace prefix
- C. A tag is like a bookmark pointing at a specific image ID; tagging an image adds another tag rather than renaming it **(CORRECT)**
- D. Two different tags can never point to the same image ID, so each tag forces Docker to store a separate copy of the layers
- E. When pushing to a private registry, the registry address is encoded inside the image tag itself, for example registry.example.net:5000/image **(CORRECT)**
- F. Tagging one image as both :v1.0 and :latest can leave both tags pointing at the exact same image ID **(CORRECT)**

_Rationale:_ Tags are bookmarks to an image ID (they add, not rename), the registry address lives in the tag, ubuntu expands to library/ubuntu, and :v1.0 and :latest can share one image ID; a bare local name must be re-tagged with a user/repo namespace for Hub, and multiple tags sharing an ID store no duplicate layers, so options 2 and 4 are false.

### Q6. [MC] (hard, source: Lab02 slide 8)

Two images are built from alpine:3.20. Image A ends with CMD ["echo","hello"] and Image B ends with ENTRYPOINT ["echo","hello"]. You then run docker run A goodbye and, separately, docker run B goodbye. What does each container print?

- A. A prints goodbye and B prints hello goodbye **(CORRECT)**
- B. A prints hello goodbye and B prints goodbye
- C. A prints hello and B prints hello, because the run argument is ignored in both
- D. A prints goodbye and B prints goodbye

_Rationale:_ Arguments after the image name REPLACE a CMD entirely (so A runs echo goodbye), but are APPENDED to an ENTRYPOINT (so B runs echo hello goodbye). Option 2 reverses the two behaviors, the classic misconception.

### Q7. [MC] (hard, source: Week02 slides 8 and 9)

Regarding EXPOSE and publishing container ports, which statement is TRUE?

- A. Writing EXPOSE 8080 in the Dockerfile is by itself enough for a client outside the host to reach port 8080
- B. A container port can become public only if it was first declared with EXPOSE and then published with -p
- C. docker run -P (uppercase) publishes only the single lowest-numbered port declared with EXPOSE
- D. docker run -p 8080:80 makes the port public even if the image never declared that port with EXPOSE **(CORRECT)**

_Rationale:_ All ports are private by default and -p publishes a port whether or not it was declared with EXPOSE, so option 4 is correct; option 2 is wrong because EXPOSE is not a prerequisite for -p, and -P publishes ALL EXPOSE'd ports, not just the lowest.

### Q8. [MC] (hard, source: Lab02 slide 19)

You run docker buildx build --platform linux/amd64,linux/arm64 -t $REPO:v1.0 --push . Which statement about the result is correct?

- A. It produces two separate tags, one per architecture, and clients must choose the right one by hand
- B. Because two platforms are targeted, you must still run docker tag and docker push afterward to upload each variant
- C. It publishes ONE tag backed by a manifest list, and a client automatically pulls the variant that matches its CPU **(CORRECT)**
- D. The --push flag caches both images locally so they can be inspected before any upload happens

_Rationale:_ buildx publishes a single tag carrying multiple platform variants under a manifest list, and clients pull the one that fits their CPU; --push uploads straight to the registry (skipping the local cache) with no separate tag/push step, making options 2 and 4 wrong.

### Q9. [MC] (very_hard, source: Week03 slide 6)

You run docker run -d --name db postgres and docker run -d --name api myapi with no --network flag on either, so both land on the default bridge. Inside api, code tries to open a TCP connection to the hostname db. What happens?

- A. It connects, because the embedded DNS on the default bridge resolves db to its container IP
- B. It connects, because Docker automatically writes every container name into each container's /etc/hosts
- C. It fails to resolve db by name, because embedded DNS name resolution works only on user-defined networks; the containers would have to use IP addresses instead **(CORRECT)**
- D. It fails completely, because containers on the default bridge cannot reach each other at all, even by IP address

_Rationale:_ Slides 3 and 6 state name-based DNS only works on networks you create yourself, not the default bridge. Option 4 is the trap: default-bridge containers CAN still reach each other by IP, so the failure is name resolution, not connectivity.

### Q10. [MC] (very_hard, source: Week03 slide 3)

You start docker run -d --network app-net --name web -p 8080:80 nginx, then start a second container named client on the same app-net network. What URL should client use to reach the nginx server?

- A. http://web:8080, because clients must always target the published host port
- B. http://web:80, because container-to-container traffic uses the container's own port via the network's DNS name, and the -p mapping only serves the outside world **(CORRECT)**
- C. http://localhost:8080, because every container on app-net shares the host's localhost
- D. It cannot reach nginx until a second mapping such as -p 80:80 is added to the web container

_Rationale:_ Slide 3 states the outside world reaches containers only through published ports; internal traffic on a user-defined network resolves the name and hits the container port (80). The 8080 host mapping is irrelevant to container-to-container calls, so web:8080 is the trap.

### Q11. [MC] (hard, source: Week03 slide 4)

A team needs each container to appear as a distinct device on the office physical LAN, with its own MAC address and an IP handed out by the LAN's DHCP server, so external hosts can address each container directly. Which Docker network driver fits this requirement?

- A. host, because it shares the host stack and therefore exposes the host's own MAC and IP to the container
- B. overlay, because it spans multiple machines and assigns each container a routable cluster IP
- C. bridge, because the default isolated virtual switch already places containers on the physical LAN
- D. macvlan, because each container is given its own MAC on the physical network and can pull a real LAN IP **(CORRECT)**

_Rationale:_ Slide 4 lists macvlan as giving each container its own MAC on the physical net and real LAN IPs. host only shares the single host's MAC/IP (no per-container identity), so it cannot give each container a distinct LAN address.

### Q12. [MC] (hard, source: Week03 slide 7)

Comparing Docker's CNM with Kubernetes' CNI as taught, which statement is TRUE?

- A. Kubernetes CNI presents a single flat cluster network where every pod is reachable by default, and isolation must be added explicitly with NetworkPolicy resources **(CORRECT)**
- B. Docker's CNM leaves containers unisolated by default, mirroring Kubernetes' flat-network philosophy
- C. CNM is the plugin-based model driven by CNI plugins, while Kubernetes relies on libnetwork drivers
- D. In Docker CNM, DNS is scoped per namespace, exactly the way Kubernetes scopes cluster DNS

_Rationale:_ Slide 7 shows CNI as a single flat network, every pod reachable, isolation off by default needing NetworkPolicy. Option 2 is wrong because CNM isolation is ON by default (bridging requires explicit work), the opposite of a flat model.

### Q13. [MC] (very_hard, source: Lab03 slides 4, 6 and 7)

In the Week 3 lab, Step 2 starts MySQL with --mount type=volume,source=mysql-data,target=/var/lib/mysql and inserts a Puffball row. Step 4 removes that container and restarts MySQL hardened with --mount type=bind,source=$PWD/mysql-data,target=/var/lib/mysql. The Step 5 SELECT then fails with ERROR 1049: Unknown database 'foo'. What best explains this?

- A. --cap-drop=ALL stripped MySQL's permission to read its data files, permanently corrupting the foo database.
- B. The hardened container bind-mounted an empty host directory ($PWD/mysql-data) over /var/lib/mysql, so MySQL initialized a fresh data dir; the Puffball row is still intact on the named volume mysql-data. **(CORRECT)**
- C. The row was written to a tmpfs mount in Step 2, so it vanished the moment the first container was removed.
- D. --security-opt=no-new-privileges blocked MySQL from re-attaching the named volume, which dropped every database.

_Rationale:_ A named volume (source=mysql-data) and a host bind mount (source=$PWD/mysql-data) are two different storage locations that merely share a name; the bind dir was empty, so MySQL bootstrapped a fresh data dir while the real row stays safe on the named volume. cap-drop=ALL is wrong because the lab adds back the caps MySQL needs and the data is not corrupted, just not mounted.

### Q14. [MA] (very_hard, source: Week03 slides 4, 6 and Lab03 slides 3, 5, 6)

Select ALL statements that are TRUE about the Week 3 MySQL + Adminer lab and Docker networking as taught.

- A. A user-defined bridge gives containers name-based DNS, so Adminer can reach the database using the server name mysql-db instead of an IP. **(CORRECT)**
- B. The default bridge network provides the same automatic name resolution, so creating clo835-net is optional.
- C. In the hardened setup MySQL's port 3306 is never published to the host; only Adminer's 8080 is exposed. **(CORRECT)**
- D. Containers on clo835-net receive addresses from the 172.28.0.0/16 subnet defined when the network was created. **(CORRECT)**
- E. The overlay driver would be the correct choice here because clo835-net spans a single host.
- F. tmpfs is the recommended mount for the MySQL data directory so the seeded row survives docker rm.

_Rationale:_ User-defined bridges add DNS (default bridge does not), MySQL 3306 is deliberately unpublished while Adminer publishes 8080, and clo835-net uses the 172.28.0.0/16 subnet. Overlay is a multi-host driver and tmpfs is RAM-only that does NOT survive docker rm, so both are false.

### Q15. [TF] (very_hard, source: Lab03 slide 6)

True or False: In the hardened MySQL run, --cap-drop=ALL is used on its own with no --cap-add flags, because MySQL needs no Linux capabilities once the process is not running as root.

- Answer: **False**

_Rationale:_ False: the lab drops ALL and then explicitly adds back the five capabilities MySQL still needs (CHOWN, SETGID, SETUID, DAC_OVERRIDE, FOWNER); dropping everything with no add-backs would break startup.

### Q16. [MC] (hard, source: Week03 slide 11)

You run docker run -v /srv/missing:/var/lib/mysql mysql:8 where /srv/missing does not exist on the host, then rewrite it as docker run --mount type=bind,source=/srv/missing,target=/var/lib/mysql mysql:8. How do the two commands differ in this exact case?

- A. Both fail identically, because a bind-mount source must always pre-exist on the host.
- B. -v silently creates /srv/missing as an empty directory and mounts it, while --mount fails fast with a clear error because the source path does not exist. **(CORRECT)**
- C. -v fails because it cannot create host paths, while --mount silently creates the missing directory.
- D. Both silently create the directory; the only real difference is that --mount is more verbose to type.

_Rationale:_ Per the slide, with a missing host path -v silently creates it while --mount fails fast with a clear error. The 'both verbose only' option is the trap for students who think -v and --mount are purely cosmetic variants.

### Q17. [TF] (very_hard, source: Week04 slide 18)

True or False: In this course's deployment prerequisites, kubectl and the cluster may differ in MAJOR version, but they should run the same MINOR version.

- Answer: **True**

_Rationale:_ The prerequisites slide states 'Same MINOR version as the cluster. Major version mismatch is supported, minor isn't.', so matching the minor version is what the course requires, making the statement true.

### Q18. [MA] (hard, source: Week04 slide 13)

According to the control-plane-vs-data-plane table, which of the following run on a WORKER node (the data plane)? Select all that apply.

- A. kubelet **(CORRECT)**
- B. kube-proxy **(CORRECT)**
- C. container runtime (containerd / CRI-O) **(CORRECT)**
- D. CNI plugin **(CORRECT)**
- E. kube-scheduler
- F. etcd

_Rationale:_ The worker/data-plane column lists kubelet, kube-proxy, container runtime, cni-plugin, and the workload pods. kube-scheduler and etcd are master/control-plane components, so they are the incorrect choices.

### Q19. [MC] (hard, source: Lab04 slide 5)

In the lab's kind.yaml the cluster maps containerPort 30000 and 30001 to hostPort 30000 and 30001 via extraPortMappings. What does this accomplish?

- A. It exposes the kube-apiserver to the host on ports 30000-30001.
- B. It gives every pod a routable public IP address.
- C. It makes NodePort Services published on 30000-30001 reachable from the Cloud9 host. **(CORRECT)**
- D. It assigns each node a dedicated /24 pod subnet.

_Rationale:_ The slide's goal states the YAML 'reserves host ports 30000-30001 for NodePort services', so the mapping lets host traffic reach NodePort Services in that range. The apiserver distractor is wrong because it listens on https://127.0.0.1:6443, not those ports.

### Q20. [MC] (very_hard, source: Week05 slide 4)

A Pod runs two containers: web listening on TCP 8080, and a sidecar. Based on how the course describes a Pod's networking, which statement is TRUE?

- A. The sidecar must use the web container's own Pod-internal DNS name to reach it, since each container is assigned its own IP.
- B. The sidecar can reach web at localhost:8080 because both containers share the Pod's single network namespace. **(CORRECT)**
- C. The sidecar can also bind and listen on TCP 8080 at the same time, since each container has its own independent network stack.
- D. Each of the two containers is assigned a separate IP address inside the Pod.

_Rationale:_ The slides state all containers in a Pod share one network stack and intercommunicate over 127.0.0.1 under a single IP, so localhost:8080 works (B); C is wrong because a shared network namespace means only one container can bind 8080.

### Q21. [MC] (very_hard, source: Week05 slide 22)

A ReplicaSet is defined with replicas: 3 and is currently running exactly 3 matching Pods. An admin then manually creates one standalone Pod that happens to carry the exact label the ReplicaSet selects on. What does the ReplicaSet controller do?

- A. Nothing, because the ReplicaSet only counts Pods it originally created from its own template.
- B. It scales the desired count up to 4 so the new Pod is included permanently.
- C. It terminates one Pod so that the current count matches the desired count of 3. **(CORRECT)**
- D. It leaves all 4 Pods running and reports 4/3 ready indefinitely.

_Rationale:_ A ReplicaSet identifies its Pods purely by label selector and deletes surplus Pods when current exceeds desired, so it kills one to return to 3; it does not track ownership by template origin, ruling out A.

### Q22. [TF] (very_hard, source: Week05 slide 8)

In the frontend/backend collocation example, the pattern the course recommends is to place the frontend process and the backend process in two separate containers within a single Pod.

- Answer: **False**

_Rationale:_ False: the slide crosses out both the single-container and the two-containers-in-one-Pod options and marks the correct approach as two separate Pods (a frontend Pod and a backend Pod).

### Q23. [MC] (very_hard, source: Week06_Part_A slides 5, 6, 10)

A Deployment currently runs nginx:1.7.0. An operator runs kubectl set image deployment/myapp-deployment nginx=nginx:1.9.1. Which description matches what Kubernetes does?

- A. It edits the pods in the existing ReplicaSet in place, swapping their image without creating any new object.
- B. It requires the deployment to be deleted and re-created before the image change takes effect.
- C. It creates a new deployment revision by rolling out a new ReplicaSet for nginx:1.9.1 while scaling the old ReplicaSet down. **(CORRECT)**
- D. It changes the image only in the YAML file and waits for the next kubectl apply to actually roll it out.

_Rationale:_ Updating the image triggers a rollout that creates a new revision backed by a new ReplicaSet while the old one is scaled down (as in the Revision 1 to Revision 2 diagram); pods in an existing ReplicaSet are never mutated in place.

### Q24. [MA] (very_hard, source: Week06_Part_A slides 7, 8, 9)

Based on the Rollout and Recreate strategy slides, select ALL statements that are TRUE.

- A. RollingUpdate is the default rollout strategy. **(CORRECT)**
- B. The Recreate strategy causes application downtime and should be specified explicitly. **(CORRECT)**
- C. During a RollingUpdate the load balancer serves traffic to both old and new pods until the rollout completes. **(CORRECT)**
- D. Recreate is the default strategy, so RollingUpdate must instead be requested explicitly.
- E. RollingUpdate necessarily incurs a brief application downtime while the pods swap over.
- F. The Recreate strategy upgrades pods one at a time specifically to avoid any downtime.

_Rationale:_ The slides state RollingUpdate is the default with no downtime and gradually shifts the LB from old to new pods, while Recreate causes downtime and must be specified; the false options reverse the default, wrongly attribute downtime to RollingUpdate, and describe rolling behavior as Recreate.

### Q25. [MC] (hard, source: Week06_Part_A slide 6)

During a rollout, kubectl rollout status deployment/myapp-deployment prints: Waiting for rollout to finish: 9 of 10 updated replicas are available... Which statement best describes this state?

- A. The rollout has failed because only 9 of the intended 10 replicas will ever come up.
- B. The rollout is still in progress: 9 of the 10 new-version replicas are up and Kubernetes is waiting for the 10th before reporting success. **(CORRECT)**
- C. There are 9 old-version pods still serving traffic and only 1 new-version pod has been created so far.
- D. The deployment is permanently stuck at 90 percent and requires a manual restart to continue.

_Rationale:_ The word updated means new-version replicas, so 9 of 10 new pods are already available and the command keeps waiting until all 10 are before it prints successfully rolled out; it counts updated (new) replicas, not the remaining old ones.

### Q26. [MA] (very_hard, source: Week06_Part_B slides 46, 34-35, 36, 42)

Select ALL statements that are TRUE according to the lecture.

- A. The Endpoints resource is built from the service's selector and holds the IP and port pairs of the matching pods. **(CORRECT)**
- B. When a client connects to a service, the service proxy selects one of the endpoint IP:port pairs and redirects the connection to it. **(CORRECT)**
- C. A ClusterIP is a virtual IP that no process, network namespace, or interface actually owns. **(CORRECT)**
- D. A NodePort service lets you freely choose any node port, such as 80 or 8080, to match the container.
- E. A LoadBalancer service provisions a working external load balancer even when the underlying infrastructure offers no load-balancer service.

_Rationale:_ The Endpoints and Kube-Proxy slides confirm the selector-built endpoint list, the proxy redirect, and the virtual (unowned) ClusterIP; a NodePort must fall in 30000-32767, and a LoadBalancer only works when the infrastructure provides load-balancer-as-a-service.

### Q27. [MC] (hard, source: Week06_Part_B slide 38)

A Service manifest declares spec.ports with port: 80 and targetPort: 8080, no type field, and selector app: kubia. Which statement correctly describes how port and targetPort behave?

- A. port 80 is the container's listening port, and targetPort 8080 is the port on the service's virtual IP.
- B. Clients connect to the service's virtual IP on port 80, and the service forwards those requests to the pods' container port 8080. **(CORRECT)**
- C. port and targetPort must be set to the same value or the API server rejects the Service.
- D. targetPort 8080 is the external node port that clients outside the cluster connect to.

_Rationale:_ On the Service Manifest slide, port is the port the service is available on and targetPort is the container port it forwards to; option A swaps the two roles, which is the classic misconception.

### Q28. [MC] (hard, source: Week06_Part_B slide 36; Lab06 slide 58)

You run: k expose deployment blue --type=NodePort --port=80. Which statement about the resulting Service is TRUE?

- A. The NodePort type replaces the ClusterIP, so the service no longer has a cluster-internal virtual IP.
- B. You can set the node port to 8080 so it matches the container's listening port.
- C. The node port is opened only on the single node where the backing pod is scheduled.
- D. A ClusterIP service is also created automatically, and the externally reachable port is allocated from the 30000-32767 range. **(CORRECT)**

_Rationale:_ The NodePort slide states a NodePort automatically creates a ClusterIP service and allocates a port in 30000-32767 that is opened on all nodes; option C is wrong because the lab shows the service is reachable on both workers' public IPs.

### Q29. [MC] (hard, source: Week06_Part_B slides 34-35)

Which statement about kube-proxy and Services is TRUE?

- A. kube-proxy programs iptables rules on every node but does not itself perform the actual packet routing. **(CORRECT)**
- B. kube-proxy is a per-node userspace process that every packet destined for a Service is routed through.
- C. A Service is a real process with its own network namespace and interface that kube-proxy launches.
- D. kube-proxy runs only on the control-plane node and pushes rules to the workers from there.

_Rationale:_ The slides say kube-proxy modifies IPTABLES on each node and explicitly does NOT do the actual routing, and that a Service is virtual with no process, namespace, or interface; options B and C restate the exact misconceptions the slides refute.

### Q30. [MC] (hard, source: Week06_Part_B slide 47; slide 45)

A Service named web-service lives in the namespace apps. From a pod in a different namespace, which fully qualified in-cluster DNS name resolves to that service?

- A. web-service.svc.apps.cluster.local
- B. apps.web-service.svc.cluster.local
- C. web-service.apps.svc.cluster.local **(CORRECT)**
- D. web-service.default.svc.cluster.local

_Rationale:_ The in-cluster FQDN pattern is <service>.<namespace>.svc.cluster.local, as shown by web-service.apps.svc.cluster.local on the Service Networking slide; the other options scramble the segment order or use the wrong namespace.

### Q31. [MA] (very_hard, source: Week07 slides 5, 6, 7, 8, 9, 11)

Select ALL statements that are TRUE according to the Volumes lecture.

- A. A hostPath volume mounts a directory from the worker node's filesystem into the Pod. **(CORRECT)**
- B. For remote storage such as EBS, the volume is attached (not created) when the Pod starts and detached (not destroyed) when the Pod is destroyed. **(CORRECT)**
- C. An emptyDir volume shadows the directory in the container image at the point where it is mounted. **(CORRECT)**
- D. A Volume can be enumerated as a cluster API resource via kubectl get volumes.
- E. configMap and secret volumes are special volume types used to expose Kubernetes resources and cluster information to the Pod. **(CORRECT)**
- F. A gitRepo volume is the modern, recommended volume type for delivering application code.

_Rationale:_ Options A, B, C, and E restate slides 6, 9, 8, and 7 respectively. D is false because Volumes are not API resources (no kubectl get volumes), and F is false because gitRepo is deprecated.

### Q32. [MC] (hard, source: Week07 slide 5)

A student claims they can audit every volume in the cluster by running kubectl get volumes, and that a PersistentVolume can be attached straight to a Pod the same way an emptyDir is. Based on how the course distinguishes Volumes from PersistentVolumes, which statement is actually TRUE?

- A. You can list a Pod's volumes cluster-wide with kubectl get volumes because volumes are namespaced API objects.
- B. A PersistentVolume is attached to a Pod directly in the pod spec, exactly like an emptyDir.
- C. A Volume is defined inside the Pod spec and is not itself a queryable API resource, whereas a PersistentVolume is an API resource consumed by a Pod only through a PersistentVolumeClaim. **(CORRECT)**
- D. Both Volumes and PersistentVolumes are cluster-scoped API resources returned by kubectl get pv.

_Rationale:_ The slides state Volumes appear in Pod specs but do not exist as API resources (cannot kubectl get volumes), while PVs are API resources that cannot be associated with a Pod directly, only through a PVC. Option B is the classic trap: PVs are never bound to a Pod directly like an emptyDir.

### Q33. [MC] (hard, source: Week07 slides 3, 8, 9)

A container writes session files into an emptyDir volume. First its main process crashes and the kubelet restarts the container in place (same node, same Pod). Later, the entire Pod is deleted and rescheduled onto another node. What happens to the files in each case?

- A. The files are lost on the container restart but persist through the Pod deletion.
- B. The files survive the container restart but are lost when the Pod is deleted. **(CORRECT)**
- C. The files survive both events because emptyDir is permanently backed by node disk.
- D. The files are lost in both cases because emptyDir storage is scoped to a single container.

_Rationale:_ The course teaches that a volume survives across container restarts but is destroyed when the Pod is destroyed, and emptyDir shares the Pod's lifecycle. Option D wrongly treats emptyDir as per-container rather than per-Pod (it can be shared by containers in the Pod).

### Q34. [MA] (very_hard, source: Week08 slides 3, 6)

Per the slides on the control-plane vs data-plane split and access, which of the following are responsibilities that AWS handles for you (NOT the customer)? Select all that apply.

- A. Scaling, monitoring, and patching the control plane **(CORRECT)**
- B. Keeping the API server, scheduler, controllers, and etcd running **(CORRECT)**
- C. Scaling the workloads and configuring the applications
- D. Provisioning and maintaining the worker nodes' operating system in self-managed EC2
- E. Providing multi-AZ high availability for the control plane **(CORRECT)**

_Rationale:_ The slides assign control-plane scaling/monitoring/patching, running API server/scheduler/controllers/etcd, and multi-AZ HA to AWS; app scaling/configuration and self-managed EC2 node maintenance are explicitly the customer's responsibility.

### Q35. [TF] (very_hard, source: Week08 slide 11)

True or False: In EKS, 'aws eks update-kubeconfig' wires kubectl to the cluster using your AWS IAM identity, but IAM only establishes WHO you are, while WHAT you can do inside the cluster is governed by Kubernetes RBAC.

- Answer: **True**

_Rationale:_ The Access & Provisioning slide maps 'who you are' to AWS IAM and 'what you can do in the cluster' to Kubernetes RBAC, with update-kubeconfig wiring kubectl via your IAM identity, so the statement is true.

### Q36. [MC] (hard, source: Week08 slide 4)

A team runs 3 separate EKS clusters in us-east-1, each with worker nodes, for 730 hours in a month. Using the pricing model taught in the slides, what is the monthly charge attributable ONLY to the EKS cluster (control plane) portion, before any node costs?

- A. 73.00 USD
- B. 146.00 USD
- C. 219.00 USD **(CORRECT)**
- D. 0.00 USD because the control plane is free and only nodes are billed

_Rationale:_ The slide charges 0.10 USD per hour per cluster x 730 hours = 73.00 USD per cluster, so 3 clusters = 219.00 USD; 73.00 forgets to multiply by the 3 clusters and 0.00 wrongly assumes the control plane is free.

### Q37. [MC] (very_hard, source: Week09 slides 24 and 28)

You deploy a standard Deployment (not a StatefulSet) with replicas: 3, whose pod template mounts a single PersistentVolumeClaim. According to the lecture, what is TRUE of the result?

- A. Each of the 3 pods automatically gets its own separate PVC and PersistentVolume.
- B. The pods are created one at a time in sequence, pod-0 fully ready before pod-1 starts.
- C. Each pod receives a stable, ordinal hostname such as web-0, web-1, and web-2.
- D. All 3 replicas are identical and mount the same single volume, because the volume is defined at the pod-template level. **(CORRECT)**

_Rationale:_ The lecture explains that all replicas in a ReplicaSet/Deployment are identical and reference the same volume since volumes are defined at the pod level; per-pod PVCs, ordinal names, and ordered creation are StatefulSet features, not Deployment behavior.

### Q38. [MA] (very_hard, source: Week09 slides 24, 27, 34 and Lab07 slide 38)

Select ALL statements that are TRUE about StatefulSets as taught in the lecture and lab.

- A. Each pod is assigned an ordinal index that starts at 0 and increments by 1. **(CORRECT)**
- B. A pod that is deleted and rescheduled keeps the same name and reattaches to the same PVC/storage. **(CORRECT)**
- C. The per-replica PVCs are created by the StatefulSet through a volumeClaimTemplate rather than being created separately. **(CORRECT)**
- D. All pods in a StatefulSet are created in parallel to speed up startup.
- E. Pods are scaled up and down in order, gracefully, one at a time. **(CORRECT)**
- F. Every pod shares one single PVC, exactly like a Deployment does.

_Rationale:_ Ordinal indexing from 0, sticky identity with storage reattachment, PVCs from a volumeClaimTemplate, and ordered one-at-a-time scaling are all stated; StatefulSet pods are created sequentially (not in parallel), and each pod gets its own PVC (not a shared one).

### Q39. [MC] (hard, source: Week09 slide 13)

A PersistentVolume is defined with accessModes listing both ReadWriteOnce and ReadOnlyMany. Based on how the lecture describes these access modes, which statement is TRUE about how this volume may be consumed?

- A. It can be mounted read-write by many clients simultaneously across different nodes.
- B. ReadWriteOnce means the volume may only ever be mounted read-only, and only one time.
- C. It can be mounted read-write by a single client, or read-only by many clients. **(CORRECT)**
- D. ReadOnlyMany permits many clients to mount the volume read-write at the same time.

_Rationale:_ The lecture states the volume can be mounted by a single client for reading and writing (ReadWriteOnce) or by multiple clients for reading only (ReadOnlyMany); it says nothing about ReadWriteMany here, so the 'many clients read-write' option is wrong.

### Q40. [MC] (hard, source: Week09 slides 32 and 33)

Which statement about the headless Service used to expose a StatefulSet is TRUE as described in the lecture?

- A. It is a normal ClusterIP Service that load-balances write traffic evenly across all the MySQL pods.
- B. It is defined with clusterIP: None and gives each pod a stable DNS name such as mysql-0.mysql-h.default.svc.cluster.local, without load-balancing. **(CORRECT)**
- C. It assigns one shared virtual IP that every pod answers on, chosen at random per request.
- D. It is needed only for Deployments and provides no benefit for StatefulSets.

_Rationale:_ The lecture states the headless service sets ClusterIP: None, does not load-balance, and lets each pod be reached by its own stable DNS name; a normal service would load-balance, which is exactly why it cannot be used to always reach the master.

