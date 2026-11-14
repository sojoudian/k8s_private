# -*- coding: utf-8 -*-
"""CLO835 - 20 easy questions from the Docker Networking, Storage and Security
lecture and from the Kubernetes Introduction lecture.

Each record holds:
  t    the topic
  q    the stem
  a    the four options; the first one is correct
  why  the feedback for the correct option
  mis  the mistake that each wrong option shows, in the order of a[1:]
"""

QUESTIONS = [
# ------------------------------------------------------------ docker networks
{"t": "networks",
 "q": "Two containers run on the default bridge network. One container calls "
      "the other by its container name. What is the result?",
 "a": ["The name does not resolve",
       "The name resolves to the private address of the other container",
       "The name resolves after a restart of the Docker daemon",
       "The name resolves to the address of the host"],
 "why": "The default bridge network has no name service. A network that you "
        "create yourself gives each container a DNS name.",
 "mis": ["Name resolution works on a user-defined network only.",
         "A restart does not add a name service to the default bridge.",
         "A container name never points at the host."]},

{"t": "networks",
 "q": "You create the network app-net. Which option puts a new container on "
      "that network at start?",
 "a": ["--network app-net",
       "--link app-net",
       "--net-alias app-net",
       "--hostname app-net"],
 "why": "The --network option names the network for the new container.",
 "mis": ["The --link option joins two containers; it is also old.",
         "The --net-alias option adds a second name inside a network.",
         "The --hostname option sets the host name inside the container."]},

{"t": "networks",
 "q": "A container must use the network interfaces of the host directly, with "
      "no address translation. Which driver fits?",
 "a": ["The host driver",
       "The macvlan driver",
       "The overlay driver",
       "The bridge driver"],
 "why": "The host driver shares the network stack of the host, so the traffic "
        "takes no bridge and no translation.",
 "mis": ["The macvlan driver gives the container its own address on the "
         "physical network, through its own interface.",
         "The overlay driver joins containers across more than one host.",
         "The bridge driver builds a private switch with translation."]},

{"t": "networks",
 "q": "A container listens on port 80 on a network that you created. A "
      "browser on another machine must reach it. What do you do?",
 "a": ["Publish the port with -p on the host",
       "Add the container name to the host file of the other machine",
       "Create a second network for the browser",
       "Give the container a second address"],
 "why": "A port stays private until you publish it to the host.",
 "mis": ["A name helps inside the network only; the port stays closed.",
         "A second network adds no path from outside the host.",
         "A second address stays inside the host."]},

# ------------------------------------------------------------ docker storage
{"t": "storage",
 "q": "You run a database in a container and you mount nothing. You delete "
      "the container, then you start a new one from the same image. What "
      "happens to the rows?",
 "a": ["The rows are gone with the write layer of the old container",
       "The rows come back, because the image holds them",
       "The rows come back after a restart of the Docker daemon",
       "The rows stay in the area that Docker manages"],
 "why": "A container writes to its own layer. The delete of the container "
        "removes that layer and the data in it.",
 "mis": ["An image is read-only; it never takes the new rows.",
         "A restart does not bring back a layer that Docker removed.",
         "Docker keeps data in its managed area for a volume only."]},

{"t": "storage",
 "q": "A container holds a password file in a tmpfs mount. The host restarts. "
      "What happens to the file?",
 "a": ["It is gone, because a tmpfs mount lives in memory",
       "It stays, because Docker copies it to the disk",
       "It stays in the area that Docker manages for volumes",
       "It stays until you remove the container"],
 "why": "A tmpfs mount uses the memory of the host, so it holds the data for "
        "the life of the container only.",
 "mis": ["Docker writes no copy of a tmpfs mount.",
         "A tmpfs mount takes no space in the volume area.",
         "The data goes away with the memory, before you remove anything."]},

{"t": "storage",
 "q": "A bind mount names a host path that is missing. How do the -v option "
      "and the --mount option behave?",
 "a": ["-v makes the path, and --mount stops with an error",
       "-v stops with an error, and --mount makes the path",
       "Each option makes the path in silence",
       "Each option stops with an error"],
 "why": "The old -v option makes a missing host path in silence. The --mount "
        "option stops at once, so a typing mistake is visible.",
 "mis": ["The two options behave the other way round.",
         "The --mount option makes no path for you.",
         "The -v option makes no error for a missing path."]},

{"t": "storage",
 "q": "A database container needs data that stays after you delete the "
      "container, and Docker must manage the storage area. Which mount fits?",
 "a": ["A volume",
       "A bind mount",
       "A tmpfs mount",
       "No mount, because the image keeps the data"],
 "why": "Docker makes and manages a volume, and the volume stays after the "
        "container goes away.",
 "mis": ["A bind mount ties the data to a path of one host.",
         "A tmpfs mount holds the data in memory only.",
         "An image is read-only, so it keeps no new data."]},

# ------------------------------------------------------------ docker security
{"t": "security",
 "q": "A colleague asks you to mount the file /var/run/docker.sock into an "
      "application container. Why is that dangerous?",
 "a": ["The container gets full control of the Docker daemon",
       "The container loses its network interface",
       "The daemon stops when the container stops",
       "The container runs slower"],
 "why": "The socket is the control channel of the daemon. A process that "
        "reaches it can start any container on the host and read any file.",
 "mis": ["The mount adds a file; it changes no network interface.",
         "The daemon does not follow the life of the container.",
         "Speed is not the problem here."]},

{"t": "security",
 "q": "Which Dockerfile instruction makes the main process run with the "
      "rights of a normal account?",
 "a": ["USER appuser",
       "ENV USER=appuser",
       "LABEL user=appuser",
       "RUN chmod -R 777 /app"],
 "why": "The USER instruction sets the account for the instructions after it "
        "and for the process in the container.",
 "mis": ["An environment variable holds a name; it changes no account.",
         "A label is metadata for people and tools only.",
         "Open file rights make the container weaker, not stronger."]},

# ------------------------------------------------------------ k8s introduction
{"t": "orchestration",
 "q": "Containers already run on one machine. Which job does Kubernetes add?",
 "a": ["It places containers across many machines and replaces the failed ones",
       "It writes the Dockerfile for the application",
       "It builds the container images",
       "It stores the images in a registry"],
 "why": "Kubernetes is a cluster manager. It places the work, it watches it, "
        "and it brings the cluster back to the state that you declare.",
 "mis": ["A developer writes the Dockerfile.",
         "A build tool makes the images.",
         "A registry stores the images."]},

{"t": "orchestration",
 "q": "A worker node fails while it runs several pods of a deployment. What "
      "does the cluster do with that work?",
 "a": ["It starts replacement pods on the nodes that work",
       "It waits for an administrator to start the pods again",
       "It moves the failed node to a new address",
       "It stops the application until the node returns"],
 "why": "A controller compares the state that you declare with the state of "
        "the cluster, and it fills the missing copies.",
 "mis": ["The cluster repairs this case without a person.",
         "A new address does not repair a node that is down.",
         "The other nodes keep the application alive."]},

{"t": "kubectl",
 "q": "Which file gives kubectl the address of the cluster and the "
      "credentials for it?",
 "a": ["~/.kube/config",
       "~/.docker/config.json",
       "/etc/kubernetes/manifests",
       "/var/lib/kubelet/config.yaml"],
 "why": "The kubeconfig file holds the clusters, the users and the contexts. "
        "The KUBECONFIG variable can point at another file.",
 "mis": ["That file holds the registry logins for Docker.",
         "That folder holds the manifests of the control plane pods.",
         "That file configures the agent on a node."]},

{"t": "kubectl",
 "q": "Which command sends the manifest file app.yaml to the cluster?",
 "a": ["kubectl apply -f app.yaml",
       "kubectl get -f app.yaml",
       "kubectl describe app.yaml",
       "kubectl push app.yaml"],
 "why": "The apply command posts the file to the API server, and the cluster "
        "moves to the state in the file.",
 "mis": ["The get command reads objects; it changes nothing.",
         "The describe command prints the detail of one object.",
         "The kubectl program has no push command."]},

{"t": "architecture",
 "q": "Which part of the control plane answers every kubectl command?",
 "a": ["The API server",
       "The controller manager",
       "The scheduler",
       "The key value store"],
 "why": "The API server is the front door of the cluster. Every tool, every "
        "controller and every agent talks to it.",
 "mis": ["The controller manager watches objects; it answers no client.",
         "The scheduler places pods; it answers no client.",
         "The key value store keeps the data behind the API server."]},

{"t": "architecture",
 "q": "A new pod waits with no node. Which part of the control plane chooses "
      "the node for it?",
 "a": ["The scheduler",
       "The kubelet",
       "The kube-proxy",
       "The controller manager"],
 "why": "The scheduler reads the free resources, the rules and the taints, "
        "and it binds the pod to one node.",
 "mis": ["The kubelet runs on a node and starts the work after the choice.",
         "The kube-proxy writes the network rules for the services.",
         "The controller manager keeps the counts, not the placement."]},

{"t": "k8s networking",
 "q": "Two pods run on different nodes of one cluster. How do they reach "
      "each other?",
 "a": ["Directly by pod address, with no address translation",
       "Through an address translation rule on each node",
       "Through the address of the node and a port map",
       "Through a proxy process on the control plane"],
 "why": "The Kubernetes network model asks for one flat address space. A "
        "network plugin makes it real.",
 "mis": ["The model forbids translation between pods.",
         "A port map belongs to a published port, not to pod traffic.",
         "The control plane carries no pod traffic."]},

{"t": "k8s networking",
 "q": "How does a cluster stop two nodes from giving one address to two "
      "different pods?",
 "a": ["It gives each node its own subnet",
       "It keeps one address list in the key value store",
       "It translates the addresses between the nodes",
       "It gives each pod the address of its node"],
 "why": "Each node receives a part of the pod address range, and the network "
        "plugin routes between those parts.",
 "mis": ["The nodes hand out addresses themselves, from their own range.",
         "Translation between pods is against the network model.",
         "A pod needs its own address, not the address of the node."]},

{"t": "kubeadm",
 "q": "The lab builds a cluster with kubeadm on three EC2 machines. Where "
      "does the control plane run?",
 "a": ["On the master node, as static Pods",
       "On each of the two workers",
       "In a Docker container on your laptop",
       "In a service that AWS manages for you"],
 "why": "kubeadm init starts the API server, etcd, the scheduler and the "
        "controller manager as static Pods on the master node.",
 "mis": ["The workers join with kubeadm join and run only the kubelet and your Pods.",
         "kubeadm builds the cluster on real machines, not in a container on a laptop.",
         "A managed service such as EKS runs the control plane for you; kubeadm does not."]},

{"t": "kubectl",
 "q": "Which command asks for five copies of the deployment web?",
 "a": ["kubectl scale deploy web --replicas=5",
       "kubectl resize deploy web --count=5",
       "kubectl run web --replicas=5",
       "kubectl edit deploy web --replicas=5"],
 "why": "The scale command changes the number of copies in the object, and "
        "the controller starts or stops pods until the number agrees.",
 "mis": ["The kubectl program has no resize command.",
         "The run command makes one new pod.",
         "The edit command opens the object in an editor and takes no count."]},
]
