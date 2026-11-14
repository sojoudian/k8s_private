# -*- coding: utf-8 -*-
"""CLO835 - 20 easy questions from the Amazon EKS lecture and from the lab that
shows, on a kubeadm cluster, the Kubernetes jobs that EKS does for you.

Each record holds:
  t    the topic (it becomes the neutral title)
  q    the stem
  a    the four options; the first one is correct
  fix  (optional) the four options in their logical order
  why  the feedback for the correct option
  mis  the mistake that each wrong option shows, in the order of a[1:]

Round 2 (2026-11-06): the 20 findings of review round 1 are applied.
Round 3 (2026-11-06): the 15 findings of review round 2 are applied.
Round 4 (2026-11-06): the 8 findings of review round 3 are applied (Q4 kept).
Round 5 (2026-11-06): the 4 findings of review round 4 are applied.
Round 6 (2026-11-06): the 1 finding of review round 5 (Q16) is applied.
Upload fix (2026-11-06): Q12 had <none>; Blackboard reads the text as HTML.
"""

QUESTIONS = [
# ------------------------------------------------------------ managed EKS
{"t": "responsibility",
 "q": "A team moves its web application from a kubeadm cluster to Amazon EKS. "
      "Which job does the team still do on EKS?",
 "a": ["Set the replica count of each Deployment",
       "Replace a failed control plane machine",
       "Install the security patches of the scheduler",
       "Set up the load balancer in front of the API server"],
 "why": "On EKS, AWS runs the control plane: the API server, the scheduler and "
        "etcd. The team still owns its workloads, and the replica count is a "
        "setting of a workload.",
 "mis": ["AWS repairs and replaces the machines of the control plane.",
         "AWS applies the security patches of the control plane.",
         "AWS sets up the load balancer of the API server when it creates the cluster."]},

{"t": "cost",
 "q": "An EKS cluster runs for one full day at the standard price. It has no "
      "worker nodes and no Pods. What does AWS bill for its control plane?",
 "a": ["2.40 USD",
       "0.00 USD",
       "0.10 USD",
       "24.00 USD"],
 "fix": ["0.00 USD",
         "0.10 USD",
         "2.40 USD",
         "24.00 USD"],
 "why": "AWS bills 0.10 USD for each hour of each EKS control plane, also when "
        "no node runs. One day has 24 hours, and 24 x 0.10 USD = 2.40 USD.",
 "mis": ["The control plane costs money also when no node runs.",
         "0.10 USD is the price of one hour, not of one day.",
         "This value uses 1.00 USD for each hour in place of 0.10 USD."]},

{"t": "worker options",
 "q": "A team wants to manage no servers for its Pods, and it wants to pay for "
      "each Pod. Which EKS worker option fits?",
 "a": ["AWS Fargate",
       "EC2 Auto Scaling",
       "Managed nodes",
       "Self-managed nodes"],
 "fix": ["AWS Fargate",
         "EC2 Auto Scaling",
         "Managed nodes",
         "Self-managed nodes"],
 "why": "With Fargate, AWS runs each Pod on capacity that AWS manages. The team "
        "manages no node, and AWS bills the CPU and the memory of each Pod.",
 "mis": ["An Auto Scaling group adds EC2 servers, and AWS bills each server.",
         "A managed node group puts EC2 nodes in the account, and AWS bills each node.",
         "Self-managed nodes give the team the most server work."]},

{"t": "networking",
 "q": "A worker node of an EKS cluster has the address 192.168.20.34 in the "
      "subnet 192.168.20.0/24. The cluster uses the Amazon VPC CNI. Which "
      "address can a new Pod of a Deployment on that node get?",
 "a": ["192.168.20.57",
       "10.244.1.7",
       "172.17.0.2",
       "192.168.20.34"],
 "fix": ["10.244.1.7",
         "172.17.0.2",
         "192.168.20.34",
         "192.168.20.57"],
 "why": "The VPC CNI gives each Pod its own address from the VPC subnet of the "
        "node. There is no overlay network, so a Pod address looks like a node "
        "address.",
 "mis": ["10.244.x.x is the Flannel overlay range of a kubeadm cluster.",
         "172.17.x.x is the default bridge range of Docker.",
         "The node keeps its own address. Each Pod of a Deployment gets a different address."]},

{"t": "endpoint",
 "q": "The API endpoint of an EKS cluster is private only. From where can "
      "kubectl reach the cluster API?",
 "a": ["From a machine inside the VPC of the cluster",
       "From any EC2 machine in the same AWS Region",
       "From your laptop at home, with an IAM admin user",
       "From the master node, after an SSH login"],
 "why": "A private endpoint answers only inside the VPC of the cluster, or in a "
        "network that connects to that VPC. A public endpoint answers from the "
        "internet.",
 "mis": ["A Region holds many VPCs. A machine in a different VPC has no route to the endpoint.",
         "IAM rights give no network route. A private endpoint has no address on the internet.",
         "EKS gives no SSH access to the control plane."]},

{"t": "storage",
 "q": "Pods in three Availability Zones of an EKS cluster must read and write "
      "the same files at the same time. Which storage fits?",
 "a": ["Amazon EFS, through the EFS CSI driver",
       "Amazon EBS, through the EBS CSI driver",
       "An emptyDir volume in each Pod",
       "A hostPath volume on one worker node"],
 "why": "An EFS file system gives shared files (ReadWriteMany) to Pods in many "
        "Availability Zones.",
 "mis": ["An EBS volume stays in one Availability Zone, and one node mounts it (ReadWriteOnce).",
         "Each emptyDir volume belongs to one Pod, so the Pods share nothing.",
         "A hostPath volume exists on one node only, and the other nodes cannot see it."]},

{"t": "storage",
 "q": "A team runs its cluster on Amazon EKS, and it needs the EBS CSI driver. "
      "Which way to install the driver does AWS recommend?",
 "a": ["As an Amazon EKS add-on of the cluster",
       "As a Docker container that you start on each node",
       "With a user data script on each Amazon EKS node",
       "As a DaemonSet manifest that you write by hand"],
 "why": "AWS recommends the EKS add-on for each CSI driver. AWS tests each "
        "add-on version for EKS, and you start each update from the console, "
        "the AWS CLI or eksctl.",
 "mis": ["The driver runs as Pods that Kubernetes manages; a container by hand on each node is no install method.",
         "A user data script runs one time at boot; AWS recommends the add-on, which you manage for the whole cluster.",
         "A manifest by hand can work, but AWS recommends the add-on: AWS tests each version for EKS."]},

{"t": "permissions",
 "q": "A user runs kubectl get pods on an EKS cluster. The answer is "
      "Forbidden. Which part denies the request?",
 "a": ["Kubernetes RBAC",
       "AWS IAM",
       "The kubelet of the node",
       "The VPC security group"],
 "fix": ["AWS IAM",
         "Kubernetes RBAC",
         "The kubelet of the node",
         "The VPC security group"],
 "why": "IAM answers the question: who are you? Kubernetes authorization "
        "(RBAC) answers the question: what can you do in the cluster? "
        "Forbidden comes from the authorization step inside the cluster.",
 "mis": ["IAM proves who the user is. A failed IAM check gives Unauthorized, not Forbidden.",
         "The kubelet runs Pods; it does not decide on a kubectl get pods request.",
         "A security group stops network traffic; it sends no Forbidden answer."]},

{"t": "certificates",
 "q": "kubeadm builds a cluster today with the default settings. Nobody "
      "upgrades the cluster, and "
      "nobody renews anything. When does the certificate of the API server "
      "expire?",
 "a": ["After one year",
       "After 90 days",
       "After five years",
       "After ten years"],
 "fix": ["After 90 days",
         "After one year",
         "After five years",
         "After ten years"],
 "why": "kubeadm gives each certificate of the cluster one year. Only the CA "
        "certificates get 10 years. On a kubeadm cluster the renewal is your "
        "job; on EKS, AWS manages the certificates.",
 "mis": ["90 days is a common life of a web certificate, not of a kubeadm certificate.",
         "kubeadm uses no five-year period.",
         "Ten years is the life of the CA certificates only."]},

{"t": "provisioning",
 "q": "You describe an EKS cluster and its node group in the file "
      "cluster.yaml. Which command builds the cluster and its node group from "
      "that file?",
 "a": ["eksctl create cluster -f cluster.yaml",
       "eksctl create nodegroup -f cluster.yaml",
       "kubeadm init --config cluster.yaml",
       "kubectl apply -f cluster.yaml"],
 "fix": ["eksctl create cluster -f cluster.yaml",
         "eksctl create nodegroup -f cluster.yaml",
         "kubeadm init --config cluster.yaml",
         "kubectl apply -f cluster.yaml"],
 "why": "eksctl is the official CLI for EKS. eksctl create cluster reads the "
        "file and creates the cluster and the node group through AWS "
        "CloudFormation stacks.",
 "mis": ["create nodegroup adds a node group to a cluster that exists already.",
         "kubeadm builds a cluster on machines that you own; it cannot create EKS.",
         "kubectl apply sends objects to a cluster that exists already."]},

# ------------------------------------------------------------ kubeadm lab
{"t": "control plane",
 "q": "On a kubeadm master, which component starts the control plane Pods from "
      "the files in /etc/kubernetes/manifests?",
 "a": ["The kubelet",
       "containerd",
       "kubeadm",
       "The controller manager"],
 "fix": ["containerd",
         "kubeadm",
         "The controller manager",
         "The kubelet"],
 "why": "The kubelet reads each file of that folder and runs it as a static "
        "Pod. No Deployment owns these Pods; the node owns them.",
 "mis": ["containerd runs the containers that the kubelet asks for; it reads no Pod file.",
         "kubeadm runs one time to build the cluster; it is no service that runs all the time.",
         "The controller manager is itself one of the static Pods."]},

{"t": "scheduling",
 "q": "The scheduler of a cluster is down. You create a new Pod with kubectl "
      "run. What does kubectl get pod -o wide show for it?",
 "a": ["STATUS Pending, with no node",
       "STATUS Running on masternode",
       "STATUS ContainerCreating on workernode1",
       "STATUS Error, with no node"],
 "why": "The scheduler picks a node for each new Pod. With no scheduler, the "
        "API server stores the Pod, but no component binds it to a node, so "
        "it waits in Pending.",
 "mis": ["No other component puts the Pod on the master; that is the job of the scheduler.",
         "ContainerCreating comes only after the Pod has a node.",
         "The API server accepts the Pod; nothing fails, the Pod only waits."]},

{"t": "cluster state",
 "q": "You create a Namespace with the name billing. Where does the cluster "
      "store this object?",
 "a": ["In etcd, as a key",
       "In a kube-system ConfigMap",
       "In the kubeconfig file",
       "In the API server memory only"],
 "why": "etcd is the database of the cluster. Every object is a key there, for "
        "example /registry/namespaces/billing.",
 "mis": ["A ConfigMap is itself an object, and etcd stores it too.",
         "The kubeconfig file holds the connection data of kubectl, not cluster objects.",
         "The API server writes each object to etcd; it keeps no object only in memory."]},

{"t": "availability",
 "q": "A kubeadm cluster has one master, from kubeadm init, and two workers, "
      "from kubeadm join. The master machine stops. What happens to the "
      "cluster API?",
 "a": ["It stops until the master runs again; Pods on the workers keep running",
       "A worker takes over as the master, and the API keeps working",
       "It keeps working, because each worker runs an API server too",
       "It answers read requests, but it refuses every change"],
 "why": "One master gives no high availability. The API server and etcd stop "
        "with the master, so kubectl gets no answer. The Pods that run on the "
        "workers continue to run.",
 "mis": ["kubeadm makes no worker into a master by itself.",
         "A worker runs the kubelet and kube-proxy, but no API server.",
         "With the master gone, no API server runs, so no request gets an answer."]},

{"t": "identity",
 "q": "On a kubeadm master, kubectl auth whoami prints the user "
      "kubernetes-admin. What proves this identity to the API server?",
 "a": ["A client certificate in the kubeconfig file",
       "A ServiceAccount token in kube-system",
       "The TLS certificate of the API server",
       "The SSH key that you used to log in"],
 "why": "kubeadm writes a client certificate into the admin kubeconfig file. "
        "The API server checks that certificate against the CA of the cluster.",
 "mis": ["A ServiceAccount token identifies a process in a Pod; whoami then shows a ServiceAccount.",
         "The certificate of the API server proves the identity of the server, not of the user.",
         "The SSH key opens the machine, not the Kubernetes API."]},

{"t": "maintenance",
 "q": "A kubeadm cluster has one master and two workers. A Deployment runs 4 "
      "Pods: 2 on workernode1 and 2 on workernode2. workernode1 has room for 2 "
      "more Pods. You run kubectl drain workernode2 --ignore-daemonsets, and "
      "the drain completes. Where do the 2 Pods from workernode2 run then?",
 "a": ["On workernode1, as 2 new Pods",
       "Nowhere; the Deployment keeps only 2 Pods",
       "On the master node, as 2 new Pods",
       "Nowhere until workernode2 takes Pods again"],
 "why": "A drain marks the node unschedulable and evicts its Pods. The "
        "Deployment makes 2 new Pods to keep 4, and the scheduler puts them on "
        "the free worker.",
 "mis": ["The Deployment keeps its replica count; it makes new Pods.",
         "kubeadm puts a taint on the master, so application Pods do not go there.",
         "workernode1 has room, so the new Pods start there and wait for nothing."]},

{"t": "maintenance",
 "q": "Two Pods run on workernode2. You run kubectl cordon workernode2. What "
      "happens?",
 "a": ["The two Pods keep running, and new Pods go to other nodes",
       "The two Pods move to other nodes at once",
       "The two Pods stop, and the node shows NotReady",
       "The two Pods keep running, and new Pods still go there"],
 "why": "A cordon marks the node SchedulingDisabled. The scheduler sends no new "
        "Pod there, and the Pods on the node keep running. A drain is the "
        "command that moves them.",
 "mis": ["A cordon moves nothing; a drain evicts the Pods.",
         "The node stays Ready; only the scheduling stops.",
         "A cordon exists to stop new Pods on that node."]},

{"t": "clean up",
 "q": "You delete every Deployment and Pod of a kubeadm cluster with kubectl. "
      "The three EC2 machines that Terraform made still run. Which command "
      "stops the AWS charge for the machines?",
 "a": ["terraform destroy",
       "kubeadm reset --force",
       "kubectl delete nodes --all",
       "terraform plan -destroy"],
 "fix": ["kubeadm reset --force",
         "kubectl delete nodes --all",
         "terraform destroy",
         "terraform plan -destroy"],
 "why": "Terraform made the machines, so terraform destroy removes them. AWS "
        "stops the charge when the instances are gone.",
 "mis": ["kubeadm reset removes the cluster setup, but the EC2 machine still runs.",
         "A delete of the Node objects changes Kubernetes only; the machines still run.",
         "plan -destroy only shows what a destroy would remove; it removes nothing."]},

{"t": "upgrades",
 "q": "You run sudo kubeadm upgrade plan on the master of a kubeadm cluster. "
      "What does the command change?",
 "a": ["It only reads the cluster and reports the versions",
       "It downloads the new control plane images and starts none",
       "It upgrades the control plane to the newest version",
       "It renews every certificate of the cluster"],
 "why": "upgrade plan checks the cluster and prints the versions that are "
        "available. It only reads. kubeadm upgrade apply makes the change.",
 "mis": ["upgrade plan pulls no image; upgrade apply does that work.",
         "kubeadm upgrade apply upgrades the control plane.",
         "upgrade plan renews nothing; kubeadm upgrade apply and kubeadm certs renew renew the certificates."]},

{"t": "nodes",
 "q": "A new EC2 machine must become the third worker of a kubeadm cluster. "
      "Which command on the master gives the exact line to run on the new "
      "machine?",
 "a": ["kubeadm token create --print-join-command",
       "kubeadm config print join-defaults",
       "kubeadm join phase preflight",
       "kubeadm token list"],
 "fix": ["kubeadm config print join-defaults",
         "kubeadm join phase preflight",
         "kubeadm token create --print-join-command",
         "kubeadm token list"],
 "why": "This command makes a new bootstrap token and prints the full kubeadm "
        "join line, with the token and the hash of the CA certificate.",
 "mis": ["This command prints a default join configuration with no real token and no real hash.",
         "This command runs the checks of a join on the new machine; it prints no join line.",
         "This command lists the tokens, but it gives no CA hash and no join line."]},
]
