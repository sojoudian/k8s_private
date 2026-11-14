# -*- coding: utf-8 -*-
"""CLO835 - 20 easy questions from the lecture on PersistentVolumes,
StorageClasses and StatefulSets, and from the lab that practises them on a
kubeadm cluster.

Each record holds:
  t    the topic (it becomes the neutral title)
  q    the stem
  a    the four options; the first one is correct
  fix  (optional) the four options in their logical order
  why  the feedback for the correct option
  mis  the mistake that each wrong option shows, in the order of a[1:]

Questions 1 to 10 come from the lecture, and questions 11 to 20 from the lab.
Each key comes from a live run on the kubeadm cluster of 2026-11-10
(Kubernetes v1.35.10), or from the Kubernetes documentation.

Round 2 (2026-11-10): the 13 findings of review round 1 are applied
(M1 to M5, S1 to S8). Q11 is a new question about a cordoned node, and Q16 is
a new question about the field clusterIP: None.
Round 3 (2026-11-10): the 9 findings of review round 2 are applied.
Round 4 (2026-11-10): the 8 findings of review round 3 are applied; Q1 and Q3 are new
application questions (Q1 proof: probe3.log).
Round 5 (2026-11-10): the 7 findings of review round 4 are applied; Q3 uses the class
manual (proof: probe4.log P14). build_easy20_w10.py has the new GATE 8c.
Round 6 (2026-11-10): the 7 findings of review round 5 are applied; the class of Q3 is
now fast (proof: probe5.log P15). GATE 8c also blocks ABCD runs and repeated blocks.
Round 7 (2026-11-10): the 6 findings of review round 6 are applied, and no wrong option
of Q5 or Q9 holds "but".
Round 8 (2026-11-10): the 5 findings of review round 7 are applied; Q13 keeps a time order.
Round 9 (2026-11-10): the 3 findings of review round 8 are applied (Q18, Q5, and the
convergence cue in Q1, Q6 and Q17).
Round 10 (2026-11-10): the 3 SHOULD-FIX findings of review round 9 are applied (round 9
found no MUST-FIX), and Q5 D and Q10 A change so that no key is the clear centre of
its options (the round 5 convergence count was 6.4 of 20).
Round 11 (2026-11-10): the 2 SHOULD-FIX findings of review round 10 are applied (Q10, Q18).
"""

QUESTIONS = [
# ------------------------------------------------------------ the lecture
{"t": "hostpath",
 "q": "A Pod mounts the node directory /var/log through a hostPath volume, "
      "and the mount sets no readOnly field. A container writes to a file in "
      "that directory. What is the result?",
 "a": ["The file on the node changes, and the change stays",
       "The write fails, because a hostPath mount is read-only by default",
       "The write goes to a copy in the container, not to the node",
       "The kubelet undoes the change when the Pod stops"],
 "why": "A hostPath volume gives the Pod the real directory of the node, and "
        "a mount is read-write unless it sets readOnly: true. The change stays "
        "on the node after the Pod stops. For this reason, mount only the "
        "necessary path, with readOnly: true.",
 "mis": ["A volume mount is read-write unless it sets readOnly: true.",
         "A hostPath volume is the node directory itself, not a copy.",
         "The kubelet changes no hostPath data; the file stays on the node."]},
{"t": "access modes",
 "q": "A claim has the access mode ReadWriteOnce. Two Pods on the same node "
      "use this claim. What happens?",
 "a": ["Each Pod runs and can write to the same volume",
       "The first Pod runs, and the second Pod stays Pending",
       "Each Pod runs, but the second Pod can only read the volume",
       "Each Pod runs and sees a different empty volume"],
 "why": "ReadWriteOnce limits the volume to one node, not to one Pod. Many Pods "
        "on that node can mount it for reading and writing. ReadWriteOncePod "
        "limits the volume to one Pod.",
 "mis": ["This is the behavior of ReadWriteOncePod, which allows one Pod in the whole cluster.",
         "No access mode gives write access to one Pod and read access to the next Pod.",
         "One claim gives one volume, so both Pods see the same files."]},

{"t": "binding",
 "q": "The StorageClass fast has volumeBindingMode: Immediate. The only "
      "Available PersistentVolume (PV) of this class has 5Gi and ReadWriteOnce. "
      "A claim of the class fast asks for 2Gi with ReadWriteOnce. What "
      "happens to the claim?",
 "a": ["It binds to the 5Gi PV",
       "It stays Pending",
       "Kubernetes divides the PV and gives it a 2Gi part",
       "The provisioner of the class creates a new 2Gi PV for it"],
 "why": "Kubernetes binds a claim to a PV with at least the requested size, "
        "the same access mode and the same class. The 5Gi PV matches, and the "
        "claim gets the whole PV.",
 "mis": ["A larger PV is a match, so the claim does not wait for an exact size.",
         "One claim binds to the whole PV; Kubernetes does not divide a PV.",
         "A matching PV exists, so Kubernetes binds the claim to it; a provisioner acts only when no PV matches."]},
{"t": "class name",
 "q": "A cluster has a default StorageClass. A claim sets storageClassName: \"\" "
      "and asks for 3Gi. All PersistentVolumes (PVs) with no class are Bound "
      "to other claims. What happens to the new claim?",
 "a": ["It stays Pending with no new PV",
       "The default StorageClass creates a 3Gi PV for it",
       "The API server rejects it, because the class name is empty",
       "It binds to a free PV of the default StorageClass"],
 "why": "An empty storageClassName turns off dynamic provisioning for the "
        "claim. The claim binds only to a PV with no class, so it waits in "
        "Pending until such a PV is free.",
 "mis": ["The default class serves a claim with no storageClassName field, not a claim with an empty name.",
         "An empty class name is valid; it has the meaning: no class.",
         "A claim with an empty class name binds only to a PV with no class."]},

{"t": "reclaim policy",
 "q": "A provisioner created the PersistentVolume (PV) of a claim, with the "
      "reclaim policy Delete. The provisioner still runs. No Pod uses the "
      "claim. You delete the claim. What happens to the PV?",
 "a": ["The provisioner deletes the storage and the PV",
       "The provisioner deletes the PV and keeps the storage",
       "The provisioner makes the PV Available for the next claim",
       "The PV stays until an administrator approves the deletion"],
 "why": "Delete is the default policy of a dynamic PV. When you delete the "
        "claim, the provisioner deletes the storage, and then it deletes the PV. "
        "If no provisioner runs, the PV stays.",
 "mis": ["The Delete policy deletes the storage as well as the PV.",
         "No current policy makes a PV Available again; Recycle did that, and it is deprecated.",
         "No approval step exists; the provisioner deletes the storage and then the PV."]},

{"t": "expansion",
 "q": "A StorageClass has allowVolumeExpansion: true. A Bound claim of this "
      "class has 10Gi. You change the request of the claim to 5Gi. What "
      "happens?",
 "a": ["The API server rejects the change, because a claim can only grow",
       "The volume becomes 5Gi, and the data stays",
       "The volume becomes 5Gi, and Kubernetes deletes the data",
       "The API server rejects the change, because the claim is Bound"],
 "why": "allowVolumeExpansion lets a claim grow. A request that is smaller "
        "than the current capacity is invalid, so the API server rejects the "
        "change, and the claim stays at 10Gi.",
 "mis": ["A volume can grow, but it cannot shrink.",
         "Kubernetes never shrinks a volume, so it deletes no data for a smaller request.",
         "A Bound claim accepts a larger request; only a smaller request is invalid."]},

{"t": "dns name",
 "q": "The StatefulSet mysql runs in the namespace shop. Its serviceName is "
      "the headless Service mysql-h. Which DNS name does the Pod mysql-0 get?",
 "a": ["mysql-0.mysql-h.shop.svc.cluster.local",
       "mysql-0.shop.svc.cluster.local",
       "mysql-h.mysql-0.shop.svc.cluster.local",
       "mysql-0.mysql-h.default.svc.cluster.local"],
 "fix": ["mysql-0.mysql-h.default.svc.cluster.local",
         "mysql-0.mysql-h.shop.svc.cluster.local",
         "mysql-0.shop.svc.cluster.local",
         "mysql-h.mysql-0.shop.svc.cluster.local"],
 "why": "The DNS name of a Pod of a StatefulSet is the Pod name, then the "
        "headless Service, then the namespace, then svc.cluster.local.",
 "mis": ["The name needs the headless Service between the Pod name and the namespace.",
         "The Pod name comes first, then the name of the Service.",
         "The Pod runs in the namespace shop, not in default."]},

{"t": "updates",
 "q": "A StatefulSet has 4 Pods, web-0 to web-3. Its rolling update has "
      "partition: 2. You change the image. Which Pods get the new image?",
 "a": ["web-2 and web-3",
       "web-0 and web-1",
       "web-0 to web-3",
       "web-3 only"],
 "fix": ["web-0 and web-1",
         "web-0 to web-3",
         "web-2 and web-3",
         "web-3 only"],
 "why": "With partition: N, only the Pods with an ordinal of N or higher get "
        "the update. The Pods web-2 and web-3 change, and web-0 and web-1 stay "
        "on the old image.",
 "mis": ["The partition protects the low ordinals, not the high ordinals.",
         "Without a partition all Pods change; partition: 2 keeps web-0 and web-1 on the old image.",
         "partition: 2 starts at ordinal 2, so web-2 changes too."]},

{"t": "scale down",
 "q": "A StatefulSet has 3 Pods, and each Pod has a claim from the volume "
      "claim template. The manifest uses only the default settings. "
      "You scale the StatefulSet to 1 replica. What happens to the claims of "
      "the Pods that the scale down deletes?",
 "a": ["Kubernetes keeps them Bound, with their data",
       "Kubernetes deletes them with the Pods",
       "Kubernetes moves their data into the claim of the Pod that stays",
       "Kubernetes keeps the claims and deletes their data"],
 "why": "The default retention policy is Retain for a delete and for a scale "
        "down. The claims stay, so a later scale up gives each Pod its old "
        "data again.",
 "mis": ["Deletion with the Pods needs the policy whenScaled: Delete.",
         "Each claim belongs to one ordinal; Kubernetes moves no data between claims.",
         "A scale down does not change the data in a claim."]},

{"t": "binding mode",
 "q": "A StorageClass has volumeBindingMode: WaitForFirstConsumer. You create "
      "a claim of this class, and no Pod uses it yet. What is the status of "
      "the claim, and why?",
 "a": ["Pending, because it waits for a Pod",
       "Failed, because no Pod uses the claim",
       "Pending, because it waits for a matching PV",
       "Bound, because the matching PV waits for the first Pod"],
 "why": "With WaitForFirstConsumer, Kubernetes binds the claim or provisions a "
        "PV only when a Pod uses it, so that the PV is on the node of the Pod. "
        "Until then, Pending is normal.",
 "mis": ["Failed is a phase of a PV after a failed reclaim; this claim waits in Pending.",
         "The claim waits for a Pod, not for a matching PV.",
         "With WaitForFirstConsumer, Kubernetes binds the claim only after a Pod uses it."]},
# ------------------------------------------------------------ the lab
{"t": "node affinity",
 "q": "The cluster has the workers workernode1 and workernode2. The hostPath "
      "PersistentVolume (PV) data-pv has a nodeAffinity rule for workernode1. "
      "You cordon workernode1. A new Pod uses the claim of "
      "data-pv. What happens to the Pod?",
 "a": ["It stays Pending until you uncordon workernode1",
       "The API server rejects the new Pod",
       "It runs on workernode2 with a copy of the data",
       "It runs on workernode1 and ignores the cordon"],
 "why": "The nodeAffinity of the PV allows only workernode1, and a cordoned "
        "node gets no new Pods from the scheduler. The scheduler finds no "
        "node, so the Pod "
        "waits in Pending until you uncordon workernode1.",
 "mis": ["The API server accepts the Pod; the scheduler then finds no node for it.",
         "The kubelet copies no volume data between nodes.",
         "The scheduler puts no new Pod on a cordoned node, also when the PV of the Pod is on that node."]},

{"t": "pv phase",
 "q": "The PersistentVolume (PV) data-pv has the reclaim policy Retain. You "
      "delete the Pod that uses its claim, and then the claim. What does "
      "kubectl get pv data-pv show in the STATUS column?",
 "a": ["Released",
       "Available",
       "Bound",
       "Failed"],
 "fix": ["Available",
         "Bound",
         "Released",
         "Failed"],
 "why": "With Retain, the PV and its data stay after you delete the claim. The "
        "PV becomes Released. It still names the old claim, so no new claim "
        "can bind to it until an administrator deletes or reuses it.",
 "mis": ["A Released PV does not become Available by itself; an administrator must delete or reuse it.",
         "A PV is Bound only while its claim exists.",
         "Failed means that an automatic reclaim failed; Retain does no automatic reclaim."]},

{"t": "pod order",
 "q": "You apply the StatefulSet kubia with replicas: 2 and the default Pod "
      "management policy. When does Kubernetes create the Pod kubia-1?",
 "a": ["After kubia-0 is Running and Ready",
       "At the same time as kubia-0",
       "Before kubia-0, from the highest ordinal",
       "As soon as kubia-0 is Running, before it is Ready"],
 "fix": ["Before kubia-0, from the highest ordinal",
         "At the same time as kubia-0",
         "As soon as kubia-0 is Running, before it is Ready",
         "After kubia-0 is Running and Ready"],
 "why": "With the default policy OrderedReady, Kubernetes creates the Pods in "
        "order. It waits until kubia-0 is Running and Ready, and then it "
        "creates kubia-1.",
 "mis": ["Creation at the same time needs podManagementPolicy: Parallel.",
         "The reverse order applies to a scale down and to an update.",
         "Kubernetes waits until kubia-0 is Ready, not only Running."]},

{"t": "claim names",
 "q": "The StatefulSet kubia has a volume claim template with the name data. "
      "Which claim does the Pod kubia-1 use?",
 "a": ["data-kubia-1",
       "data-1",
       "kubia-1-data",
       "kubia-data-1"],
 "fix": ["data-1",
         "data-kubia-1",
         "kubia-1-data",
         "kubia-data-1"],
 "why": "A claim name is the template name, then the Pod name: data, then "
        "kubia-1.",
 "mis": ["The claim name holds the Pod name, not only the ordinal.",
         "The template name comes first, and the Pod name follows it.",
         "The claim name holds the full Pod name kubia-1 after the template name."]},

{"t": "pod identity",
 "q": "Nobody changed the StatefulSet kubia or its Pods. You delete its Pod kubia-0, and "
      "the StatefulSet replaces it. Which property of the new Pod can be "
      "different from the old Pod?",
 "a": ["Its IP address",
       "Its ordinal",
       "Its claim",
       "Its labels"],
 "why": "The new Pod gets the same name, the same claim and the same DNS name. "
        "It can get a new IP address, so clients use the DNS name.",
 "mis": ["The new Pod has the ordinal 0 again, as its name kubia-0 shows.",
         "The new Pod uses the same claim, data-kubia-0, and its data.",
         "The labels come from the Pod template and the ordinal, and neither changed."]},

{"t": "headless service",
 "q": "Which field in a Service manifest makes the Service headless?",
 "a": ["clusterIP: None",
       "type: Headless",
       "publishNotReadyAddresses: true",
       "sessionAffinity: None"],
 "why": "A headless Service has the field clusterIP: None. It gets no cluster "
        "IP address, and its DNS name returns the IP address of each Ready Pod.",
 "mis": ["Headless is not a Service type; the types are ClusterIP, NodePort, LoadBalancer and ExternalName.",
         "publishNotReadyAddresses adds the Pods that are not Ready to the DNS records; it does not remove the cluster IP address.",
         "sessionAffinity controls which Pod gets the requests of one client; it does not remove the cluster IP address."]},

{"t": "peer discovery",
 "q": "What does the output of nslookup -type=SRV for the headless Service "
      "of a StatefulSet show?",
 "a": ["The DNS name and the port of each Ready Pod",
       "The IP address of each node, with no port",
       "One record that names the Service and its port",
       "The name of each node, with a NodePort"],
 "why": "Kubernetes creates an SRV record for each named port of a headless "
        "Service. Each record names the DNS name and the port of one Ready "
        "Pod, so a peer can find all the members with one query.",
 "mis": ["The SRV records point to the Pods, not to the nodes, and each record holds a port.",
         "One record for the whole Service is the result for a normal Service, not for a headless Service.",
         "The SRV records of a headless Service point to Pods, not to nodes."]},

{"t": "proxy",
 "q": "kubectl proxy runs on port 8001 of the master. A curl request to "
      "localhost:8001 reaches a Pod through the API server, and the curl "
      "command names no token. Why does the API server accept it?",
 "a": ["kubectl proxy adds the credentials of the kubeconfig file",
       "The API server does no authentication for a request to a Pod",
       "kubectl proxy turns off authentication on the API server",
       "curl reads the token of the kubeconfig file by itself"],
 "why": "kubectl proxy listens on a local port. It sends each request to the "
        "API server with the credentials of the kubeconfig file.",
 "mis": ["A request to a Pod through the API server is an API request, so the API server checks its credentials.",
         "kubectl proxy changes nothing on the API server; it only adds credentials to each request.",
         "curl knows nothing about the kubeconfig file."]},

{"t": "default class",
 "q": "You build a new cluster with kubeadm, and you install no storage "
      "add-on. What does kubectl get storageclass show?",
 "a": ["No resources found",
       "standard (default)",
       "error: the server doesn't have a resource type \"storageclass\"",
       "local-path (default)"],
 "why": "kubeadm installs no provisioner and no StorageClass. An administrator "
        "adds them later, for example the local-path provisioner.",
 "mis": ["The class standard comes from a provisioner that you install.",
         "StorageClass is a built-in API type. A new cluster has the type, but no object of it.",
         "local-path comes with some small distributions, not with kubeadm."]},

{"t": "troubleshooting",
 "q": "A claim stays Pending. Which command shows the reason?",
 "a": ["kubectl describe pvc NAME",
       "kubectl logs pvc/NAME",
       "kubectl get pvc NAME",
       "kubectl get pv"],
 "why": "kubectl describe shows the Events of the claim at the end of the "
        "output. The Events give the reason, for example that no PV matches "
        "or that the claim waits for a Pod.",
 "mis": ["A claim has no logs; only containers have logs.",
         "The table shows the status, but not the reason.",
         "The PV list shows the volumes, but not why a claim waits."]},
]
