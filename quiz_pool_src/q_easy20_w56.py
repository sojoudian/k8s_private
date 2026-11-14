# -*- coding: utf-8 -*-
"""CLO835 - 20 easy questions from the Pods and ReplicaSets lecture and from
the Rollouts, Labels, Selectors and Services lecture.

Each record holds:
  t    the topic
  q    the stem
  a    the four options; the first one is correct
  why  the feedback for the correct option
  mis  the mistake that each wrong option shows, in the order of a[1:]
"""

QUESTIONS = [
# ------------------------------------------------------------ pods
{"t": "pods",
 "q": "A Pod holds a web container and a log container. The cluster has three "
      "nodes. On how many nodes do these two containers run?",
 "a": ["On one node, the same node for both",
       "On two nodes, one node for each container",
       "On three nodes, one copy on each node",
       "On any node, because a container moves at any time"],
 "fix": ["On one node, the same node for both",
         "On two nodes, one node for each container",
         "On three nodes, one copy on each node",
         "On any node, because a container moves at any time"],
 "why": "A Pod is the unit of placement. The scheduler binds the whole Pod to "
        "one node, so every container of that Pod runs there.",
 "mis": ["The containers of one Pod never separate.",
         "One Pod is one copy; three nodes need three Pods.",
         "A running container stays on its node."]},

{"t": "pods",
 "q": "A log container sends a request to 127.0.0.1:8080. The web container "
      "of the same Pod listens on port 8080. What is the result?",
 "a": ["The request arrives, because the two containers share one network stack",
       "The request fails, because each container keeps its own address",
       "The request fails, because a Service is missing",
       "The request arrives only after you publish the port"],
 "why": "The containers of one Pod share one network namespace and one "
        "address, so they reach each other on the loopback interface.",
 "mis": ["One Pod has one address for all of its containers.",
         "A Service serves clients outside the Pod.",
         "A Pod needs no port map for traffic inside itself."]},

{"t": "manifest",
 "q": "Which command prints the full description of the running Pod web, with "
      "the fields that the cluster added?",
 "a": ["kubectl get pod web -o yaml",
       "kubectl logs pod/web",
       "kubectl apply pod web",
       "kubectl list pod web"],
 "fix": ["kubectl apply pod web",
         "kubectl get pod web -o yaml",
         "kubectl list pod web",
         "kubectl logs pod/web"],
 "why": "The -o yaml option prints the live object, with the metadata, the "
        "spec and the status.",
 "mis": ["The logs command prints the output of a container.",
         "The apply command needs a file and changes the object.",
         "The kubectl program has no list command."]},

{"t": "manifest",
 "q": "Which apiVersion belongs at the top of a Deployment manifest?",
 "a": ["apps/v1",
       "v1",
       "apps/v1beta1",
       "deployment/v1"],
 "fix": ["apps/v1",
         "apps/v1beta1",
         "deployment/v1",
         "v1"],
 "why": "A Deployment and a ReplicaSet belong to the apps group. A Pod and a "
        "Service belong to the core group, which is written v1.",
 "mis": ["The plain v1 group holds the Pod and the Service.",
         "The beta group is old and is gone from current clusters.",
         "There is no group with the name of the object."]},

{"t": "namespaces",
 "q": "Two teams must each run a Deployment with the name web in one cluster. "
      "What makes that possible?",
 "a": ["Two namespaces, one for each team",
       "Two labels, one for each team",
       "Two nodes, one for each team",
       "A longer name for one of the teams"],
 "why": "A namespace gives a scope for names. One name can appear one time in "
        "each namespace.",
 "mis": ["A label groups objects; it does not free the name.",
         "A node carries work; it does not hold the names.",
         "A new name answers a different request."]},

# ------------------------------------------------------------ replicasets
{"t": "replicaset",
 "q": "A ReplicaSet asks for three Pods. You delete one of its Pods by hand. "
      "What happens next?",
 "a": ["The controller starts a new Pod",
       "The deleted Pod starts again with the same name",
       "The count stays at two until you scale the object",
       "Nothing happens, because you asked for the delete"],
 "why": "The controller compares the count that you declare with the count "
        "that runs, and it closes the difference.",
 "mis": ["The new Pod carries a new name.",
         "The controller repairs the count without a command.",
         "The controller does not read who deleted the Pod."]},

{"t": "replicaset",
 "q": "Which section of a ReplicaSet manifest describes the Pods that the "
      "object must create?",
 "a": ["The template section",
       "The selector section",
       "The metadata section",
       "The replicas field"],
 "fix": ["The metadata section",
         "The replicas field",
         "The selector section",
         "The template section"],
 "why": "The template holds a whole Pod recipe: the labels and the "
        "containers. The controller stamps new Pods from it.",
 "mis": ["The selector says which Pods to count.",
         "The metadata names the ReplicaSet itself.",
         "The replicas field holds a number only."]},

{"t": "replicaset",
 "q": "A ReplicaSet runs three Pods of the version 1.0 of an application. You "
      "must move the application to the version 2.0 with no stop. Which "
      "object do you use?",
 "a": ["A Deployment",
       "A second ReplicaSet beside the first one",
       "A Service with two selectors",
       "A larger ReplicaSet"],
 "fix": ["A Deployment",
         "A larger ReplicaSet",
         "A second ReplicaSet beside the first one",
         "A Service with two selectors"],
 "why": "A Deployment holds the ReplicaSets for you. It raises the new one "
        "and lowers the old one, step by step.",
 "mis": ["Two ReplicaSets by hand give no order and no rollback.",
         "A Service sends traffic; it changes no version.",
         "More copies of 1.0 do not bring 2.0."]},

# ------------------------------------------------------------ rollouts
{"t": "rollout",
 "q": "A Deployment runs a rolling update. When does Kubernetes stop one of "
      "the old Pods?",
 "a": ["After a new Pod reports the ready state",
       "Before it starts the first new Pod",
       "After every new Pod is ready",
       "At the same moment as it starts a new Pod"],
 "fix": ["Before it starts the first new Pod",
         "At the same moment as it starts a new Pod",
         "After a new Pod reports the ready state",
         "After every new Pod is ready"],
 "why": "The default strategy keeps the application available. It adds a Pod, "
        "it waits for the ready state, and then it removes an old Pod.",
 "mis": ["That order is the Recreate strategy, and it stops the application.",
         "The update works Pod by Pod, not in one block at the end.",
         "A new Pod needs time before it can take traffic."]},

{"t": "rollout",
 "q": "Which update strategy of a Deployment leaves the application without "
      "any running Pod for a short time?",
 "a": ["The Recreate strategy",
       "The RollingUpdate strategy",
       "The Canary strategy",
       "The BlueGreen strategy"],
 "fix": ["The BlueGreen strategy",
         "The Canary strategy",
         "The Recreate strategy",
         "The RollingUpdate strategy"],
 "why": "The Recreate strategy stops the old Pods first, and it starts the "
        "new Pods after that. You must ask for it in the manifest.",
 "mis": ["The rolling strategy keeps Pods alive through the change.",
         "A canary release is a pattern; it is no strategy field.",
         "A blue-green release is a pattern that you build with Services."]},

# ------------------------------------------------------------ services
{"t": "service",
 "q": "A Service selects the Pods with the label app=kubia. You start one "
      "more Pod with that label. What happens?",
 "a": ["The new Pod joins the Service",
       "The new Pod waits for a change of the Service",
       "The new Pod stays outside, because the Service is full",
       "The Service refuses the Pod and prints an error"],
 "why": "A Service matches on labels and nothing else. Any Pod with the "
        "label joins, and any Pod that loses the label leaves.",
 "mis": ["The match is live; it needs no edit.",
         "A Service holds no limit on the number of Pods.",
         "A Service makes no error for a new Pod."]},

{"t": "service",
 "q": "A Service answers clients on port 80, and the container listens on "
      "port 8080. Which field of the Service holds 8080?",
 "a": ["targetPort",
       "port",
       "nodePort",
       "containerPort"],
 "fix": ["containerPort",
         "nodePort",
         "port",
         "targetPort"],
 "why": "The port field is the port of the Service. The targetPort field is "
        "the port inside the Pod.",
 "mis": ["The port field holds 80 here.",
         "The nodePort field holds the high port on each node.",
         "The containerPort field belongs to the Pod manifest."]},

{"t": "service",
 "q": "A user outside the cluster opens a browser at the address of a node "
      "and the port 30123, and the application answers. Which Service type "
      "is in use?",
 "a": ["The NodePort type",
       "The ClusterIP type",
       "The ExternalName type",
       "The LoadBalancer type"],
 "fix": ["The ClusterIP type",
         "The NodePort type",
         "The LoadBalancer type",
         "The ExternalName type"],
 "why": "A NodePort Service opens one high port on every node, and a client "
        "outside reaches the Pods through it.",
 "mis": ["A ClusterIP Service answers inside the cluster only.",
         "An ExternalName Service points at a name outside the cluster.",
         "A LoadBalancer Service answers on one address of the platform."]},

{"t": "service",
 "q": "A program in a Pod calls http://kubia and reaches the Service kubia in "
      "the same namespace. Which part of the cluster answers that name?",
 "a": ["The name server of the cluster",
       "The scheduler",
       "The container runtime",
       "The host file of the node"],
 "fix": ["The container runtime",
         "The host file of the node",
         "The name server of the cluster",
         "The scheduler"],
 "why": "Each Service receives a name in the cluster name server, and the "
        "search list of the Pod completes the short name.",
 "mis": ["The scheduler places Pods; it answers no name.",
         "The runtime starts containers; it answers no name.",
         "The file of the node holds no Service names."]},

{"t": "service",
 "q": "A Service of the type ClusterIP has the address 10.96.0.17. Can a "
      "laptop outside the cluster open that address?",
 "a": ["No, the address works inside the cluster only",
       "Yes, after the laptop learns the name of the Service",
       "Yes, because every Service address is public",
       "No, because the address belongs to one Pod"],
 "why": "A ClusterIP address comes from a private range of the cluster. Only "
        "the nodes and the Pods route to it.",
 "mis": ["A name does not build a route to a private address.",
         "A Service address is private until a type opens it.",
         "The address belongs to the Service, not to a Pod."]},

{"t": "service",
 "q": "You ask for a Service of the type LoadBalancer on a local cluster, and "
      "the external address stays pending. What is the reason?",
 "a": ["No platform under the cluster gives a load balancer",
       "The Service needs a second selector",
       "The Pods carry the wrong port number",
       "The cluster needs a restart of the name server"],
 "why": "A LoadBalancer Service asks the platform below the cluster for an "
        "address. A laptop cluster has no such platform.",
 "mis": ["A selector finds Pods; it gives no address.",
         "A port number does not block the external address.",
         "The name server plays no part in this step."]},

{"t": "service",
 "q": "A Pod behind a Service fails, and a new Pod takes its place with a new "
      "address. What does a client use after that?",
 "a": ["The same Service name and the same Service address",
       "The new address of the new Pod",
       "The address of the node that holds the new Pod",
       "A new Service that the cluster creates"],
 "why": "The Service address stays stable, and the list of Pods behind it "
        "changes. That is the reason to put a Service in front of Pods.",
 "mis": ["A client must never follow a Pod address.",
         "The node address reaches no Pod by itself.",
         "The cluster makes no new Service for this."]},

# ------------------------------------------------------------ labels, ingress
{"t": "labels",
 "q": "Which command lists only the Pods that carry the label app=kubia?",
 "a": ["kubectl get pods --selector app=kubia",
       "kubectl get pods --filter app=kubia",
       "kubectl get pods app=kubia",
       "kubectl describe pods app=kubia"],
 "fix": ["kubectl describe pods app=kubia",
         "kubectl get pods --filter app=kubia",
         "kubectl get pods --selector app=kubia",
         "kubectl get pods app=kubia"],
 "why": "The --selector option takes a label, and the command prints the "
        "objects that carry it.",
 "mis": ["The kubectl program has no --filter option.",
         "Without the option, kubectl reads the text as a name.",
         "The describe command needs a name, not a label."]},

{"t": "ingress",
 "q": "Two host names, shop.example.com and api.example.com, must reach two "
      "different Services through one address. Which resource does that?",
 "a": ["An Ingress",
       "A second NodePort Service",
       "A ReplicaSet with two templates",
       "A Pod with two containers"],
 "fix": ["An Ingress",
         "A Pod with two containers",
         "A ReplicaSet with two templates",
         "A second NodePort Service"],
 "why": "An Ingress reads the host name and the path of a request, and it "
        "sends the request to the Service of the rule.",
 "mis": ["A NodePort Service reads no host name.",
         "A ReplicaSet holds one template and routes nothing.",
         "A Pod runs the application; it routes no traffic."]},

{"t": "deployment",
 "q": "You delete the ReplicaSet of a healthy Deployment. What does the "
      "cluster do?",
 "a": ["The Deployment creates a new ReplicaSet",
       "The Deployment goes away with its ReplicaSet",
       "The Pods stay and no object owns them",
       "The cluster asks you for a new manifest"],
 "why": "The Deployment is the owner. It compares the state that you declare "
        "with the state of the cluster, and it builds the missing object.",
 "mis": ["A Deployment lives above the ReplicaSet and stays.",
         "The new ReplicaSet owns Pods again.",
         "The repair needs no command from you."]},
]
