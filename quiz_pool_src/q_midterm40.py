# -*- coding: utf-8 -*-
"""CLO835 - the mid-term exam: 40 multiple-choice questions on Weeks 01 to 06, 09 and 10.

Scope (the user, 2026-11-14): Week 01 Docker Introduction, Week 02 Docker Image Management,
Week 03 Docker Networking, Storage and Security, Week 04 Kubernetes Introduction, Week 05 Pods and
ReplicaSets, Week 06 Services and Deployments, Week 09 PersistentVolumes and Kubernetes in Amazon EKS,
Week 10 StorageClasses and StatefulSets. Week 07 is not in the list of the user, so no question
tests it. Week 08 was the study week. Nothing after Week 10.

Each record holds:
  t    the topic (it becomes the neutral title)
  q    the stem
  a    the four options; the first one is correct
  fix  (optional) the four options in their logical order
  why  the feedback for the correct option
  mis  the mistake that each wrong option shows, in the order of a[1:]

Questions by week: 1-6 Week 01, 7-11 Week 02, 12-14 Week 03, 15-18 Week 04, 19-24 Week 05,
25-30 Week 06, 31-34 Week 09, 35-40 Week 10. Weeks 03 and 09 have few facts that the earlier
pools and exams do not already test, so Weeks 01, 05 and 10 have more questions.

The content sources (the current decks and the lab scripts of the public course repo):
week01/Week01_lecture_style_v5, finalWork/Lab01, week02/Week02_lecture_style_v1, week02/Lab01_v1,
week03/Week03_lecture_style_v2, week03/Lab03_lab_style_v1, Week04/FINAL/Week04_v2 and Lab_week04_v2,
Week05/lecture_week05_v4 and Lab_week05_v5, Week06/Week06_lecture_style_v7 and Lab_week06_v5,
Week09/Lecture_week09_v7 and Lab_week09_v5, Week10/Lecture_week10_v12 and Lab_week10_v5.

Round 1 (2026-11-14): the first draft. No live run: the Docker daemon of the laptop is off, and the
prompt gives no permission for AWS. Each key has a proof in the live-tested lab scripts or in the
documentation (the proof map is in the report).
Round 2 (2026-11-14): the findings of review round 1 (24 MUST-FIX, 16 SHOULD-FIX) are applied.
20 questions are new, because they repeated a fact of an earlier pool or exam. Two replacements
differ from the reviewer text: Q3 tests docker logs (the docker rmi behavior with the containerd
image store has no proof here), and Q28 tests a paused rollout (the reviewer's two-Deployment
question repeats the key of q_easy20_w56 Q11). The titles are neutral.
Round 3 (2026-11-14): the findings of review round 2 (9 MUST-FIX, 11 SHOULD-FIX) are applied. Three
questions are new: Q17 (a new image under the same tag), Q25 (the released Pod) and Q26 (no -n flag).
Q17 differs from the reviewer text, because the reviewer proposed a kubelet question, and review
round 1 rejected the kubelet as a repeat of q_easy20_w09 Q11.
Round 4 (2026-11-14): the findings of review round 3 (5 MUST-FIX, all in the feedback, and 18
SHOULD-FIX) are applied. Q16 now tests the selector of an exposed Deployment.
Round 5 (2026-11-14): the findings of review round 4 (5 MUST-FIX, 10 SHOULD-FIX) are applied. In Q29,
the third option is an HTTP 503 answer, not "the name resolves to no address", because review
round 2 reported that form as answered by the feedback of q_easy20_w56 Q14.
Round 6 (2026-11-14): the findings of review round 5 (5 MUST-FIX, 10 SHOULD-FIX) are applied. New:
Q14 (a container name in use), Q22 (kubectl logs --tail 1 --follow) and Q34 (Fargate beside a node
group). In Q17, the reviewer text is used for two wrong options.
Round 7 (2026-11-14): the findings of review round 6 (4 MUST-FIX, 8 SHOULD-FIX) are applied. New: Q13
(sudo with no-new-privileges) and Q5 (the short container ID as the host name). The reviewer text for
Q5 (docker start -ai) is not used, because review round 1 reported that fact as a repeat of
CLO835_Final_Exam_v2 Q1. In Q1, option A is the reinstall option, not a DOCKER_HOST option, because
the course does not teach DOCKER_HOST.
Round 8 (2026-11-15): the findings of review round 7 (3 MUST-FIX, 11 SHOULD-FIX) are applied. New:
Q10 (permissions of an SSH key file), Q39 (a Pod with an unbound claim) and Q40 (a StorageClass with
no volumeBindingMode). Q10 differs from the reviewer text, because the named-port question is near
q3_quiz3 Q75, and the kernel forwarding fact is CLO835_Final_Exam_v2 Q29.
Round 9 (2026-11-15): the findings of review round 8 (3 MUST-FIX, 4 SHOULD-FIX) are applied. Q10 drops the
sudo option (OpenSSH checks only a key file of the user who runs ssh), and Q13, Q19 and Q34 lose the
persistence and negation words in their keys.
Round 10 (2026-11-15): the findings of review round 9 (4 MUST-FIX, 6 SHOULD-FIX) are applied. The main fix
removes the cue "pick the shorter option of the most similar pair" (17.00 of 40 before).
Round 11 (2026-11-15): the findings of review round 10 (6 MUST-FIX, 5 SHOULD-FIX) are applied. Q13 is new
(MYSQL_ROOT_PASSWORD_FILE and docker inspect), because the course names no-new-privileges but does not
teach how sudo acts under it. The Q13 key avoids the path text of the stem, so it leaks no stem word.
Round 12 (2026-11-15): the findings of review round 11 (3 MUST-FIX, 6 SHOULD-FIX) are applied. Q13 is new
again (chown with --cap-drop=ALL), because the -e and docker inspect fact is q2_w02 Q69. Q39 drops the
storageClassName "" premise of q_easy20_w10 Q4. Q40 moves to the EBS CSI driver, because local-path
cannot provision a claim with Immediate binding. The new options avoid the word "needs", which only
wrong options used.
Round 13 (2026-11-15): the findings of review round 12 (6 MUST-FIX, 5 SHOULD-FIX) are applied. Q23 now
says that READY counts no init container that runs to completion (a sidecar counts in v1.35).
Round 14 (2026-11-15): the findings of review round 13 (5 MUST-FIX, 3 SHOULD-FIX) are applied. Q11 IF D
now fits the course Terraform, where var.region has the default us-east-1.
Round 15 (2026-11-15): the findings of review round 14 (1 MUST-FIX, 1 SHOULD-FIX) are applied: Q18 D and
Q35 D move the key out of the most similar pair, and Q35 C is a full sentence.
Round 16 (2026-11-15): the findings of review round 15 (1 MUST-FIX, 9 SHOULD-FIX) are applied. Q17 WHY now
says that a later container start pulls the new :latest image. The Q40 D edit of the reviewer is not
used, because it gives the same result as Q40 C. Other texts differ from the reviewer, so that the
word-count and odd-form cues stay at 12.0 of 40 or lower.
Round 17 (2026-11-15): the findings of review round 16 (1 MUST-FIX, 1 SHOULD-FIX) are applied. The key
was too seldom the odd one out (3.5 of 40), so 14 options change. Q32 and Q2 also change, so that no
word is only in wrong options and the pair cues stay at 12.0 of 40 or lower.
"""

QUESTIONS = [
    # ------------------------------------------------------------------ Week 01
    {"t": "docker cli access as a normal user",
     "q": "On an Amazon Linux EC2 machine, you install Docker and start it. As ec2-user, docker ps fails "
          "with permission denied on /var/run/docker.sock, and sudo docker ps works. What fixes this for "
          "ec2-user?",
     "a": ["Add ec2-user to the group docker, then start a new SSH session",
           "Start the Docker daemon again with sudo systemctl start docker",
           "Run docker login as ec2-user, then run docker ps",
           "Install Docker again with sudo yum install docker -y"],
     "why": "The daemon socket belongs to root and to the group docker. A member of the group docker can use "
            "the socket. A new group applies at the next login, for example in a new SSH session.",
     "mis": ["The daemon already runs, because sudo docker ps works. The problem is the access to the socket.",
             "docker login gives access to a registry. It gives no access to the local socket.",
             "The installation is complete. A new installation does not change the groups of ec2-user."]},

    {"t": "environment variable in a docker run command",
     "q": "In a bash shell on your laptop, you run export K8S_COLOR=GREEN. Then you run "
          "docker run -e K8S_COLOR=BLUE ubuntu echo $K8S_COLOR. What does the container show in your terminal?",
     "a": ["GREEN",
           "BLUE",
           "A blank line only",
           "The text $K8S_COLOR"],
     "why": "bash replaces $K8S_COLOR with GREEN before Docker gets the arguments. The container runs echo "
            "GREEN.",
     "mis": ["The container has K8S_COLOR=BLUE, but it never gets the text $K8S_COLOR.",
             "bash has a value for K8S_COLOR, so the argument is GREEN.",
             "The text has no single quotes, so bash expands it."]},

    {"t": "output of docker logs",
     "q": "The main process of the container web writes its start message to standard output (stdout). It "
          "writes each request to /var/log/app.log, a regular file in the container. What does docker logs web show?",
     "a": ["The start message only",
           "The start message and the requests of /var/log/app.log",
           "The requests of /var/log/app.log, and no start message",
           "The output that each docker exec command sends to your terminal"],
     "why": "docker logs shows what the main process writes to stdout and stderr. A file in the container "
            "is not part of that stream.",
     "mis": ["docker logs reads no file of the container. It shows the stdout and stderr stream only.",
             "The start message goes to stdout, so docker logs shows it. The file is not in the stream.",
             "The output of docker exec goes to your terminal. docker logs shows the stream of the main "
             "process."]},

    {"t": "keys ctrl p and ctrl q in a container",
     "q": "You start a container with docker run -it, and its main process shows the date every second in "
          "your terminal. You press Ctrl+P, then Ctrl+Q. What happens to the container?",
     "a": ["It runs, even after you close the terminal",
           "It stops, and Docker then ends its main process",
           "It runs until you close the terminal",
           "It pauses, and docker ps shows it as Paused"],
     "why": "Ctrl+P, Ctrl+Q detaches your terminal. A container runs with or without a client attached, so it "
            "continues to run with no terminal.",
     "mis": ["Detach does not stop the main process. The container stops only when its main process ends.",
             "After the detach, the container has no link to your terminal. A closed terminal changes nothing.",
             "Docker does not pause a container when you detach. docker ps shows it as Up."]},

    {"t": "prompt inside a new container",
     "q": "You run docker run -it ubuntu, and the prompt shows root@04c0bb0a6c07:/#. What is 04c0bb0a6c07?",
     "a": ["The short ID of the container, which is also its host name",
           "The ID of the image ubuntu, which docker images shows",
           "A random name that Docker shows in the NAMES column",
           "The MAC address of the eth0 interface of the container"],
     "why": "Docker sets the host name of a new container to its short container ID. The same ID is in the "
            "CONTAINER ID column of docker ps.",
     "mis": ["The image ID is a different value. The prompt shows the ID of the container.",
             "Docker gives a random name of two words, for example laughing_poincare, in the NAMES column. The "
             "prompt shows the ID.",
             "A MAC address has six pairs of hex digits with colons, for example 02:42:ac:11:00:02. The prompt "
             "shows the host name, which is the short container ID."]},

    {"t": "docker run with no local image",
     "q": "A host has no copy of the image nginx, and it can reach Docker Hub. You run docker run -d nginx, with no docker pull before it. "
          "What happens?",
     "a": ["Docker pulls the image, and then it starts a new container",
           "The command fails, because no local image exists",
           "Docker pulls nginx:latest, and it creates no container",
           "Docker creates a container, and it waits for a pull"],
     "why": "docker run pulls a missing image first. Then it creates the container and starts it. docker pull "
            "only downloads, and it creates no container.",
     "mis": ["A missing image is no error for docker run. It pulls the image from Docker Hub first.",
             "That is the result of docker pull. docker run also creates and starts a container.",
             "docker run does the pull itself. It waits for no other command."]},

    # ------------------------------------------------------------------ Week 02
    {"t": "container start on an amazon machine",
     "q": "You build an image with docker build on a Mac with Apple Silicon, and you push it to Docker Hub. "
          "An x86_64 (amd64) EC2 machine pulls the image and starts it. The container fails at start with exec format error. "
          "What is the cause?",
     "a": ["The image holds arm64 programs, and the CPU of the EC2 machine is amd64",
           "The amd64 EC2 machine runs the image on an older Linux kernel than the Mac",
           "The CMD uses the shell form, and the image has no bash",
           "The tag on Docker Hub points at an older image"],
     "why": "docker build creates an image for the CPU type of the build machine, here arm64. An amd64 CPU "
            "cannot run arm64 programs, so the start fails with exec format error.",
     "mis": ["A difference of kernel versions gives other errors. Here, exec format error comes from a CPU "
             "type that does not match.",
             "The shell form uses /bin/sh, not bash. A missing shell gives a different error.",
             "An older image for the same CPU type starts. The error comes from the CPU type."]},

    {"t": "terraform destroy in a lab directory",
     "q": "You built the lab machine with terraform apply. Later, you delete the file terraform.tfstate, "
          "and the machine still runs. Then you run terraform destroy in the same directory. What "
          "happens?",
     "a": ["Terraform completes and deletes nothing, and the machine stays in AWS",
           "Terraform reads the .tf files and deletes the machine",
           "Terraform finds the machine by its tags and deletes it",
           "Terraform fails, because no state file exists"],
     "why": "Terraform deletes only the objects that its state file records. With no state, the plan has 0 "
            "objects to destroy, and the machine stays in AWS. Delete it in the EC2 console, or import it "
            "into a new state.",
     "mis": ["The .tf files describe the objects that you want. Only the state file links them to the real "
             "AWS objects.",
             "terraform destroy does not search AWS by tags. It uses the state file.",
             "A missing state file is no error for terraform destroy. With no state, the destroy completes and "
             "deletes nothing."]},

    {"t": "published port with no answer",
     "q": "A Flask application in a container listens on 127.0.0.1:8080 only. You start the container with "
          "-p 8080:8080. On the host, curl http://localhost:8080 gets no answer. What is the cause?",
     "a": ["The application listens on loopback, and Docker forwards to the container IP",
           "The host port and the container port need two different numbers, for example -p 8081:8080",
           "The host firewall blocks the published port on localhost",
           "The application listens on 127.0.0.1, so -p needs the form 127.0.0.1:8080:8080"],
     "why": "The container has its own loopback interface. Docker forwards the published port to the IP "
            "address of the container, so the application must listen on that address, for example on "
            "0.0.0.0.",
     "mis": ["The two numbers can be equal. The host port and the container port are in different network "
             "namespaces.",
             "Docker writes the firewall rules for a published port. The request reaches the container, and "
             "no program listens on eth0.",
             "The address in -p is an address of the host. Docker still sends the traffic to the container "
             "IP."]},

    {"t": "permissions of an ssh key file",
     "q": "In a bash shell on your macOS or Linux laptop, you run ssh -i lab.pem ubuntu@3.91.242.254. ssh rejects "
          "the key file lab.pem, because other users on your laptop can read it. Which command fixes this?",
     "a": ["chmod 400 lab.pem",
           "ssh-keygen -t rsa -f lab.pem",
           "chmod +r lab.pem",
           "chmod 755 lab.pem"],
     "fix": ["ssh-keygen -t rsa -f lab.pem",
             "chmod +r lab.pem",
             "chmod 400 lab.pem",
             "chmod 755 lab.pem"],
     "why": "ssh rejects a private key file of your user when other users have any permission on it. chmod 400 "
            "gives read permission to the owner only, so ssh accepts the key.",
     "mis": ["ssh-keygen creates a new key pair. AWS knows only the public key of the old key pair, so the new "
             "key fails.",
             "+r adds the read permission for every user. Other users can still read lab.pem, so ssh still rejects "
             "the key.",
             "755 lets every user read the key, so ssh still rejects it."]},

    {"t": "terraform apply asks for a value",
     "q": "In the directory of a lab, terraform apply shows var.key_name and Enter a value, and it waits. "
          "What does this tell you?",
     "a": ["An input variable in the .tf files has no default",
           "The AWS credentials in ~/.aws/credentials have expired",
           "No EC2 key pair for key_name exists in the AWS account",
           "Terraform shows each setting of the lab when no state file exists"],
     "why": "Terraform asks for each input variable that has no default and no value from the command, a "
            "file or a TF_VAR_ environment variable. key_name has no default, so terraform apply and "
            "terraform destroy both ask for it.",
     "mis": ["Expired credentials give an authentication error from AWS, not a question for a value.",
             "Terraform asks for the value before it calls AWS. A wrong key pair name gives an error later.",
             "Terraform asks for key_name also when a state file exists, for example at terraform destroy. It "
             "shows only the input variables with no value."]},

    # ------------------------------------------------------------------ Week 03
    {"t": "docker run with the read only flag",
     "q": "You start a container with docker run --read-only, and you mount no volume and no tmpfs. The image holds the directory /app. Its main "
          "process creates a new file /app/cache.txt. What happens?",
     "a": ["The write fails with a read-only file system error",
           "The file goes into the writable layer of the container",
           "The new file goes to a memory area that Docker adds for --read-only",
           "The container does not start without a memory area from --tmpfs"],
     "why": "--read-only mounts the root file system of the container as read-only. This container has no "
            "volume and no tmpfs, so the write to /app fails.",
     "mis": ["With --read-only, the top layer of the container is also read-only.",
             "--read-only adds no writable memory area at /app. Only a tmpfs mount, from --tmpfs or --mount type=tmpfs, gives one.",
             "--read-only needs no tmpfs mount. The container starts, and only the write fails."]},

    {"t": "docker run with the cap drop flag",
     "q": "You start an alpine container with --cap-drop=ALL and no --cap-add flag. Its main process runs as root. "
          "It creates the file /tmp/report.txt, and then it runs chown nobody /tmp/report.txt. What happens?",
     "a": ["The kernel rejects the change of owner with Operation not permitted",
           "The user nobody now owns the file /tmp/report.txt, because root can chown",
           "The container fails at start, because it has no capability CHOWN",
           "With no --cap-add, Docker rejects --cap-drop=ALL"],
     "why": "--cap-drop=ALL drops every Linux capability, also for root. chown needs the capability CHOWN, so the "
            "kernel rejects the call with Operation not permitted.",
     "mis": ["In a container, root has only the capabilities that Docker gives it. With --cap-drop=ALL, root has "
             "none, so root stays the owner.",
             "A container needs no capability to start. The container runs, and only the chown fails.",
             "Docker accepts --cap-drop=ALL with no --cap-add flag. --cap-add only adds a capability again, when "
             "the process needs it."]},

    {"t": "second docker run of one web image",
     "q": "The container webapp runs with -p 8000:8080. You built the image simple-webapp-flask:v2 on this "
          "host. You run docker run -d --name webapp -p 8081:8080 simple-webapp-flask:v2. What happens?",
     "a": ["Docker rejects the command, because another container has the name webapp",
           "Docker starts the new container with the name webapp-1",
           "Docker puts the new container in place of the old one",
           "The daemon blocks the new container, because webapp uses the container port 8080"],
     "why": "A container name belongs to one container on the host. The running container holds the name "
            "webapp, so the daemon rejects the new run with a Conflict error. Delete the old container first, "
            "or choose a new name.",
     "mis": ["Docker adds no number to a name that you choose. Only an automatic name is random.",
             "docker run replaces no container. Delete the old one yourself, for example with docker rm -f "
             "webapp.",
             "Each container has its own network namespace, so both containers can use port 8080 inside. The "
             "host ports 8000 and 8081 differ."]},

    # ------------------------------------------------------------------ Week 04
    {"t": "service of the type loadbalancer on aws",
     "q": "A self-managed Kubernetes cluster runs on EC2 machines, and it has no load balancer add-on. You "
          "create a Service of the type LoadBalancer, and AWS creates a load balancer for it. Which component "
          "of the cluster asks AWS for the load balancer?",
     "a": ["The cloud controller manager",
           "The kube-proxy of each node",
           "The scheduler",
           "The kubelet of each node, through the AWS API of its EC2 machine"],
     "why": "The cloud controller manager is the part of the control plane that talks to the cloud API. Its "
            "service controller creates the load balancer of each Service of the type LoadBalancer.",
     "mis": ["kube-proxy writes the network rules of its node. It does not talk to the cloud API.",
             "The scheduler places Pods on nodes. It creates no cloud object.",
             "The kubelet runs the Pods of its node, and it creates no load balancer. The load balancer serves the "
             "whole Service."]},

    {"t": "selector of an exposed deployment",
     "q": "You create a Deployment with kubectl create deployment store --image=nginx. Then you run kubectl "
          "expose deployment store --port=80. Which selector does the new Service get?",
     "a": ["app=store",
           "deployment=store",
           "name=store",
           "run=store"],
     "fix": ["app=store", "deployment=store", "name=store", "run=store"],
     "why": "kubectl create deployment sets app=store on the Pod template and in its selector. kubectl expose "
            "copies the selector of the Deployment into the Service.",
     "mis": ["kubectl create deployment sets no label with the key deployment.",
             "kubectl create deployment sets no label with the key name.",
             "kubectl run sets run=NAME. kubectl create deployment sets app=NAME."]},

    {"t": "image tag latest in a deployment",
     "q": "The Deployment web uses the image maziar/web:latest. You push a new image with the same tag "
          "maziar/web:latest. Then you run kubectl apply -f with the same manifest. What happens?",
     "a": ["The Deployment starts no rollout, because the Pod template has no change",
           "The Deployment starts a rollout, and the Pods get the new image one at a time",
           "kubectl apply rejects the manifest, because the Deployment web already exists",
           "The Deployment starts a rollout, and no node pulls the new image"],
     "why": "A rollout starts only when the Pod template changes. The manifest names the same tag, so the Pod "
            "template stays the same, and no new Pod starts. The running containers continue to use the old "
            "image. A container that starts later pulls the new image, because the tag :latest gets "
            "imagePullPolicy: Always.",
     "mis": ["The Deployment compares the Pod template, not the image on Docker Hub. The template is the same.",
             "kubectl create rejects an object that exists. kubectl apply updates the object that exists, and here "
             "the Pod template stays the same.",
             "The Pod template has no change, so the Deployment creates no new ReplicaSet, and no new Pod starts."]},

    {"t": "word before the equals sign in set image",
     "q": "You created a Deployment with kubectl create deployment nginx-deploy --image=nginx. In the command "
          "kubectl set image deployment/nginx-deploy nginx=nginx:1.27, what does the word nginx before the "
          "equals sign name?",
     "a": ["The container of the Pod template to update",
           "The image repository of the Pods to update",
           "The ReplicaSet of the Pods to update",
           "The label of the Pods to update"],
     "why": "set image takes CONTAINER=IMAGE pairs. kubectl create deployment names the container after the "
            "image, so the container is nginx.",
     "mis": ["The new image comes after the equals sign. The name before it is a container.",
             "set image names a container. The Deployment then creates a new ReplicaSet for the new Pod template.",
             "set image selects no Pods by label. It changes a container in the Pod template."]},

    # ------------------------------------------------------------------ Week 05
    {"t": "kubectl scale on a pod",
     "q": "You created the Pod pingpong with kubectl run pingpong --image alpine ping 127.0.0.1. Then you run "
          "kubectl scale pod pingpong --replicas=3. What happens?",
     "a": ["The command fails, and one pingpong Pod exists",
           "The command succeeds, and kubectl starts two more Pods",
           "The command succeeds, and a new ReplicaSet runs three Pods",
           "The API server rejects the command, and the Pod pingpong stops"],
     "why": "A Pod has no replica count. Only an object such as a Deployment or a ReplicaSet scales, so the "
            "command fails.",
     "mis": ["kubectl scale copies no Pod. The command fails, because a Pod has no replica count.",
             "kubectl scale creates no controller. You create a Deployment yourself.",
             "A rejected command changes no object. The Pod pingpong continues to run."]},

    {"t": "dry run of kubectl run",
     "q": "You run kubectl run kubia --image maziar/kubia --dry-run=client -o yaml. What does the command do?",
     "a": ["kubectl shows the manifest, and it sends no create request",
           "kubectl creates the Pod, checks it, and then deletes it",
           "It runs the Pod in a separate test namespace",
           "The API server checks the Pod, and it stores nothing"],
     "why": "With --dry-run=client, kubectl only shows the object that it would send. -o yaml shows it as a "
            "manifest, which you can write to a file.",
     "mis": ["A client dry run sends no create request, so it creates no Pod.",
             "A client dry run creates no object in any namespace.",
             "That is --dry-run=server. With --dry-run=client, the API server gets no create request."]},

    {"t": "label selector with in",
     "q": "Three Pods carry these labels: nginx has rel=canary, kubia has rel=beta, and web has rel=stable. "
          "You run kubectl get pods -l 'rel in (stable,beta)'. Which Pods does the command show?",
     "a": ["kubia and web",
           "nginx and kubia",
           "web only",
           "nginx, kubia and web"],
     "fix": ["web only", "kubia and web", "nginx and kubia", "nginx, kubia and web"],
     "why": "The set-based selector matches each Pod whose rel value is stable or beta: kubia and web. "
            "nginx has canary.",
     "mis": ["nginx has rel=canary, and canary is outside the set.",
             "The set holds stable and beta, so kubia matches too.",
             "The selector filters by value. canary is outside the set, so nginx does not match."]},

    {"t": "kubectl logs with two flags",
     "q": "The Pod ticker runs ping 127.0.0.1, and its container writes one line every second. You run "
          "kubectl logs ticker --tail 1 --follow. What does kubectl show?",
     "a": ["The newest line, and then each new line until you press Ctrl+C",
           "The newest line only, and then your prompt returns",
           "Every line from the start, and then your prompt returns",
           "Every line from the start, and then each new line until you press Ctrl+C"],
     "why": "--tail 1 shows only the newest line that the container wrote. --follow then shows each new line "
            "until you stop kubectl with Ctrl+C.",
     "mis": ["That is the result of --tail 1 alone. With --follow, kubectl continues to show the new lines.",
             "That is the result of kubectl logs with no flag.",
             "That is the result of --follow alone. --tail 1 starts at the newest line."]},

    {"t": "ready column of a pod",
     "q": "The command kubectl get pod web shows READY 1/2. What does 1/2 tell you?",
     "a": ["One of its two containers is ready",
           "The Pod is ready for one of the two Services that select it",
           "Its first init container is done, and the second one runs",
           "One container restarted once, and the Pod allows two restarts"],
     "why": "READY shows the number of ready containers of the Pod, then the number of its containers. Here "
            "one container is ready. READY counts no init container that runs to completion.",
     "mis": ["READY counts the containers of the Pod. A Service selects a Pod by its labels.",
             "READY counts no init container that runs to completion. While such an init container runs, STATUS "
             "shows Init:1/2.",
             "The RESTARTS column counts restarts. Kubernetes sets no limit of two restarts."]},

    {"t": "kubectl logs with two containers",
     "q": "The Pod shop has no annotations. It lists two containers: app, then agent. You run kubectl logs "
          "shop with no -c flag. What does kubectl show?",
     "a": ["The log of app only",
           "The logs of app and agent in time order",
           "The log of agent only",
           "An error that asks for the -c flag"],
     "why": "With no -c flag, kubectl takes the first container of the Pod, here app. It also shows the "
            "message Defaulted container \"app\" out of: app, agent.",
     "mis": ["With no -c flag and no --all-containers flag, kubectl logs shows the log of one container only.",
             "kubectl takes the first container of the list, not the last.",
             "Old kubectl versions did this. A current kubectl takes the first container."]},

    # ------------------------------------------------------------------ Week 06
    {"t": "label change on a pod of a deployment",
     "q": "The Deployment kubia has the selector tier=web, and its ReplicaSet runs three Pods with this "
          "label. You change the label of one Pod to tier=debug with kubectl label --overwrite. What happens "
          "to the Pod with the label tier=debug?",
     "a": ["It continues to run, and the ReplicaSet no longer owns it",
           "It continues to run, and the ReplicaSet still owns it",
           "The ReplicaSet deletes it, because the ReplicaSet still owns it",
           "The ReplicaSet deletes it, because it is no longer in the Deployment"],
     "why": "The Pod no longer matches the selector of the ReplicaSet, so the ReplicaSet releases it. The Pod "
            "continues to run, and its list of owners is empty.",
     "mis": ["The ReplicaSet owns only the Pods that match its selector, so it released this Pod.",
             "The ReplicaSet owns only the Pods that match its selector. It released this Pod, and it deletes nothing.",
             "The ReplicaSet releases a Pod that leaves its selector, and it deletes no Pod. The Pod continues to run "
             "with no owner."]},

    {"t": "kubectl get with no namespace flag",
     "q": "You create the Deployment orders with the flag -n billing. Your kubeconfig context names no "
          "namespace. Then you run kubectl get deployment orders with no -n flag. What does kubectl show?",
     "a": ["A NotFound error from the API server, for the namespace default",
           "The Deployment orders, because kubectl searches every namespace",
           "An error, and kubectl asks you to add the -n flag",
           "An empty table, with the column names only"],
     "why": "With no -n flag, kubectl uses the namespace of the context, here default. The Deployment "
            "orders is in the namespace billing, so the API server answers NotFound.",
     "mis": ["kubectl searches one namespace: the namespace of the -n flag, or else the namespace of the "
             "context.",
             "kubectl asks for no flag. The API server answers NotFound, because the namespace default holds "
             "no Deployment orders.",
             "A get with a name shows that object or a NotFound error. It shows no empty table."]},

    {"t": "revisions after rollout undo",
     "q": "The Deployment kubia has revision 1 (image v1) and revision 2 (image v2). You run kubectl rollout "
          "undo deployment/kubia, and the rollout completes. Which revision numbers does the Deployment kubia "
          "have now?",
     "a": ["Revisions 2 and 3, and revision 3 is the current one",
           "Revisions 1 and 2, and revision 1 is the current one",
           "Revisions 1 and 3, and revision 3 is the current one",
           "Revisions 1, 2 and 3, and revision 3 is the current one"],
     "fix": ["Revisions 1 and 2, and revision 1 is the current one",
             "Revisions 1 and 3, and revision 3 is the current one",
             "Revisions 1, 2 and 3, and revision 3 is the current one",
             "Revisions 2 and 3, and revision 3 is the current one"],
     "why": "undo makes the old Pod template the newest revision. Kubernetes gives it the next number, 3, and "
            "revision 1 leaves the list.",
     "mis": ["The rollback is a new revision with a new number. Revision 1 does not stay.",
             "Revision 2 stays in the list. Kubernetes gives the template of revision 1 the new number 3, so the "
             "number 1 leaves the list.",
             "Revision 1 and the rollback hold one Pod template. Revision 1 leaves the list, and its template "
             "gets the number 3."]},

    {"t": "paused rollout of a deployment",
     "q": "You run kubectl rollout pause deployment/kubia. Then you change the image of the Deployment kubia "
          "from v1 to v2. What happens to the Pods of kubia?",
     "a": ["They continue to run v1 until you resume the Deployment",
           "The Deployment replaces them with v2 Pods",
           "They continue to run v1 until the pause time limit ends",
           "kubectl rejects a change of the Pod template during the pause"],
     "why": "A paused Deployment records each change of its Pod template, and it starts no rollout. kubectl "
            "rollout resume starts the rollout with the latest template.",
     "mis": ["The pause stops new rollouts. The Deployment replaces no Pod until the resume.",
             "A pause has no time limit. Kubernetes does not check the progress deadline of a paused Deployment.",
             "kubectl accepts changes to a paused Deployment. Only the rollout waits."]},

    {"t": "service with a selector that matches no pod",
     "q": "The ClusterIP Service checkout has the selector tier=checkout, and no Pod has this label. A client Pod in the "
          "same namespace runs curl http://checkout. What happens?",
     "a": ["The name resolves to the Service address, and the connection fails",
           "The connection waits until a Pod with the label tier=checkout starts",
           "The Service answers with the error 503, because it has no Pod",
           "The Service starts a Pod with the label tier=checkout and then answers"],
     "why": "The DNS name of a ClusterIP Service points at its cluster IP address, with or without Pods. The "
            "Service has no endpoints, so the connection fails.",
     "mis": ["A Service holds no connection for later. With no endpoints, the connection fails, and curl shows "
             "an error.",
             "A Service has no process of its own, so it sends no HTTP answer. With no endpoints, the "
             "connection fails.",
             "A Service creates no Pods. A Deployment or a ReplicaSet creates them."]},

    {"t": "ports of a loadbalancer service",
     "q": "On Amazon EKS, you create the Service web. Its spec sets only a selector, type: LoadBalancer and "
          "port: 80. AWS gives it an external address. What does the PORT(S) column of kubectl get service web "
          "show?",
     "a": ["80 and one node port on every node, for example 80:32143/TCP",
           "Only 80/TCP, because a load balancer opens no other port",
           "80/TCP and 443/TCP, because a load balancer adds HTTPS",
           "Only 32143/TCP, with no Service port"],
     "why": "By default, a LoadBalancer Service also gets a node port on every node and a ClusterIP. The load "
            "balancer often sends the traffic through that node port.",
     "mis": ["Kubernetes gives a LoadBalancer Service a node port by default.",
             "The Service opens only the ports of its manifest. Port 443 needs its own entry.",
             "The column shows the Service port first, then the node port."]},

    # ------------------------------------------------------------------ Week 09
    {"t": "storage for a fargate pod",
     "q": "On Amazon EKS, a Pod runs on AWS Fargate, and it needs a PersistentVolume (PV). Which storage can "
          "this Pod use, and how?",
     "a": ["An EFS file system, which Fargate mounts by itself for the Pod",
           "An EFS file system, after you install a driver on Fargate",
           "An EBS volume that the CSI (Container Storage Interface) driver mounts",
           "An EBS volume that you attach to the Pod by hand"],
     "why": "A Fargate Pod mounts an EFS file system with no driver installation. AWS cannot mount an EBS "
            "volume to a Fargate Pod.",
     "mis": ["You manage no Fargate node, so you install no driver on Fargate. Fargate mounts EFS by itself.",
             "The EBS CSI driver serves Pods on EC2 nodes. A Fargate Pod cannot mount EBS.",
             "AWS can attach no EBS volume to a Fargate Pod."]},

    {"t": "kubectl logs on amazon eks",
     "q": "On Amazon EKS, you run kubectl logs for a Pod on an EC2 worker node. The control plane runs in a "
          "VPC that AWS owns. How does the control plane reach the kubelet of the node?",
     "a": ["Through elastic network interfaces that AWS creates in your VPC",
           "Through the public address of the node, outside your VPC",
           "Through the AWS load balancer of the cluster API endpoint",
           "Through the NodePort range 30000-32767 of the node"],
     "why": "EKS puts AWS-managed elastic network interfaces (ENIs) into your VPC. The control plane uses them "
            "for kubectl logs and kubectl exec, and TLS protects the traffic.",
     "mis": ["The traffic stays on the ENIs in your VPC, and TLS protects it.",
             "The load balancer carries the calls to the API server. The control plane reaches the kubelet through the ENIs.",
             "The NodePort range serves Services. The kubelet uses its own port."]},

    {"t": "pending claims of the ebs csi driver",
     "q": "On Amazon EKS, the EBS CSI (Container Storage Interface) driver add-on runs. Each new claim of the class gp3 has a Pod that names it, and "
          "each claim stays Pending. The Events show an AWS access error for CreateVolume. What must you fix?",
     "a": ["The IAM permissions that the driver uses for each call to the EC2 API",
           "The AWS access keys of the user who creates each claim",
           "The access mode of each claim, from ReadWriteOnce to ReadWriteMany",
           "The kubeconfig of the driver, on each worker node"],
     "why": "The driver calls the EC2 API to create each EBS volume, and each CSI driver needs IAM permissions "
            "for these calls. With no permission, AWS rejects CreateVolume, and the claim stays Pending.",
     "mis": ["The user creates only the claim, through the Kubernetes API. The driver calls AWS with its own IAM identity.",
             "An access mode sets how nodes mount the volume. The AWS access error comes from the IAM permissions of "
             "the driver.",
             "The driver uses its own IAM identity for the calls to AWS."]},

    {"t": "batch pods on fargate",
     "q": "A team runs its web Pods on a managed node group of the EKS cluster shop. It now wants to run a "
          "batch Deployment on AWS Fargate. Which statement is true?",
     "a": ["The team can add Fargate, and the web Pods run on the node group",
           "The team must delete the node group of the web Pods, and then add Fargate",
           "The team can add Fargate, and the web Pods also run on Fargate",
           "The team must create one more cluster, and then add Fargate to it"],
     "why": "One EKS cluster can use managed node groups and Fargate together. Fargate runs only the Pods that "
            "the team selects for it, so the node group runs the web Pods as before.",
     "mis": ["Fargate works beside a managed node group. The team deletes no node group.",
             "Fargate runs only the Pods that the team selects for it. The web Pods stay on the node group.",
             "One cluster can use both worker choices. A second cluster only adds a second control plane bill."]},

    # ------------------------------------------------------------------ Week 10
    {"t": "nfs volume in a pod manifest",
     "q": "A Pod manifest has an nfs volume with the server 10.0.0.5. A second team must run this manifest on "
          "a second cluster, with the NFS server of that cluster. Which change lets both clusters use one Pod "
          "manifest?",
     "a": ["The Pod names a claim that each cluster binds to its own PersistentVolume",
           "The Pod lists two nfs volumes, one for the NFS server of each cluster",
           "The claim of the Pod names the NFS server of each cluster",
           "The second team copies the data of 10.0.0.5 to the NFS server of its own cluster"],
     "why": "A claim hides the details of the storage. Each cluster has its own PersistentVolume (PV) for the "
            "claim, so the Pod manifest stays the same on both clusters.",
     "mis": ["The Pod mounts both volumes, so each cluster still needs the server 10.0.0.5.",
             "A claim binds only to a PV, and it holds no server address. The PV of each cluster holds the NFS "
             "details.",
             "A copy of the data does not change the manifest. The manifest still names 10.0.0.5."]},

    {"t": "scope of a persistentvolume",
     "q": "Users in the namespace dev and in the namespace qa create PersistentVolumeClaims (PVCs). In which "
          "scope does a PersistentVolume (PV) exist?",
     "a": ["At cluster level, outside every namespace",
           "In the namespace of the claim that binds it",
           "At node level, on the node that holds its storage",
           "In the namespace default, until a claim binds it"],
     "why": "A PV is a cluster-level object, as a node is. A claim is in a namespace, and it binds to a PV of "
            "the cluster.",
     "mis": ["The claim is in a namespace. The PV that it binds stays at cluster level.",
             "The storage of a PV can be on one node, but the PV object is at cluster level, as a node object is.",
             "A PV has no namespace at all, before and after a claim binds it. kubectl puts only a namespaced "
             "object into the namespace of the context, for example default."]},

    {"t": "claim created before a storageclass",
     "q": "On a new kubeadm cluster, you create the claim data with ReadWriteOnce and no storageClassName field. The cluster has "
          "no StorageClass and no PersistentVolume (PV), so the claim stays Pending. Then you install the "
          "local-path provisioner and its default class standard, with WaitForFirstConsumer. What happens to "
          "the claim data?",
     "a": ["It gets the class standard, and it binds when a Pod uses it",
           "It stays Pending until you delete it and create a new claim",
           "It stays Pending, and it binds after a change to storageClassName",
           "The provisioner gives it the class standard only after a restart"],
     "why": "A claim with no class field gets the default class, also when the default class comes later "
            "(retroactive default). The class standard uses WaitForFirstConsumer, so the claim binds when a "
            "Pod uses it.",
     "mis": ["Kubernetes also sets the default class on the old claim. You need no new claim.",
             "Kubernetes sets the default class on the old claim. You change nothing in the claim.",
             "Kubernetes sets the default class on the old claim, and the provisioner needs no restart. It creates "
             "the PV when a Pod uses the claim."]},

    {"t": "statefulset with ondelete",
     "q": "The StatefulSet web has three Pods, web-0 to web-2, and updateStrategy: OnDelete. You change the "
          "image in its Pod template. Nobody deletes a Pod, and no node fails. What happens to the three Pods?",
     "a": ["Each Pod runs the old image until you delete that Pod",
           "Each Pod gets the new image, in reverse order from web-2 to web-0",
           "Each Pod runs the old image, also after you delete that Pod",
           "Each Pod gets the new image at its next container restart"],
     "why": "With OnDelete, the StatefulSet controller changes no running Pod. When you delete a Pod, the "
            "controller creates it again from the new template.",
     "mis": ["That is the default RollingUpdate. OnDelete waits until you delete each Pod.",
             "With OnDelete, the controller creates a deleted Pod again from the new template.",
             "A container restart uses the same Pod, with its old image. Only a new Pod gets the new "
             "template."]},

    {"t": "pod that uses a claim with no matching pv",
     "q": "No PersistentVolume (PV) matches the claim cache, and no provisioner can create one for it. You create "
          "the Pod worker, which uses the claim cache. What happens to the Pod worker?",
     "a": ["It waits in Pending until a PV binds to the claim",
           "It runs, and the claim holds an empty directory for the Pod",
           "It stays in ContainerCreating on the node that the scheduler chooses",
           "It fails, and the Pod stays in the phase Failed"],
     "why": "The claim stays Pending, because no PV matches and no provisioner creates one. A Pod cannot start while its claim is Pending, so the Pod waits in Pending. When a matching "
            "PV binds to the claim, the Pod starts.",
     "mis": ["Kubernetes starts no container of the Pod before the claim is Bound. The claim holds no directory "
             "for the Pod.",
             "The scheduler gives the Pod no node while its claim is Pending. With no node, the Pod does not "
             "reach ContainerCreating.",
             "A Pod with a claim that is not Bound does not fail. It waits in Pending."]},

    {"t": "storageclass with no binding mode field",
     "q": "On Amazon EKS, the manifest of the StorageClass slow names the provisioner ebs.csi.aws.com and sets no "
          "volumeBindingMode field. No PersistentVolume (PV) of this class exists. The driver runs and can create "
          "EBS volumes. You create the claim logs of the class slow, and "
          "no Pod uses the claim. What happens to the claim logs?",
     "a": ["It becomes Bound immediately, with a new PV from the provisioner",
           "It stays Pending until a Pod uses it, and then the provisioner creates a PV",
           "It stays Pending until you add a volumeBindingMode field to the class",
           "The API server rejects it, because the class has no binding mode"],
     "why": "When the manifest of the class sets no volumeBindingMode field, the API server sets Immediate. The provisioner creates a PV as soon "
            "as the claim exists, and the claim becomes Bound with no Pod.",
     "mis": ["That is the behavior of WaitForFirstConsumer. With no field, the class uses Immediate.",
             "The API server sets Immediate when the field is missing. The class needs no change.",
             "volumeBindingMode is optional. The API server sets the default Immediate, and it accepts the "
             "claim."]},

]
