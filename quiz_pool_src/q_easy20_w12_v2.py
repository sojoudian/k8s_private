# -*- coding: utf-8 -*-
"""CLO835 - 20 easy questions from the lecture on ConfigMaps and Secrets, and from
the lab that practises them on a kubeadm cluster.

Each record holds:
  t    the topic (it becomes the neutral title)
  q    the stem
  a    the four options; the first one is correct
  fix  (optional) the four options in their logical order
  why  the feedback for the correct option
  mis  the mistake that each wrong option shows, in the order of a[1:]

Questions 1 to 10 come from the lecture, and questions 11 to 20 from the lab.
Each key comes from a live run on the kubeadm cluster of 2026-11-10
(Kubernetes v1.35.10): the lab logs run1.log and run2.log, and the probe logs
probe1.log, probe2.log and probe2_kubelet.log.

Round 1 (2026-11-10): the first draft.
Round 3 (2026-11-11): the 6 MUST-FIX and 13 SHOULD-FIX findings of review round 2 are
applied. Q2 tests the fact of the slide (the container does not start), Q17 and Q20 are new,
Q11 and Q17 keep a logical option order, and the printenv stems name the kubectl exec command.
Round 4 (2026-11-11): lab v7 has no cleanup step (standards v1.2), so it deletes no namespace.
Q20 (namespace delete) gives its place to Q20 (env precedence), from the comment of Step 4:
"When env and envFrom set the same name, the value of env wins." Its proof is probe4.log.
This proof is pending. probe4.log does not exist until the owner runs probe4.sh on the cluster.
Round 5 (2026-11-11): the 5 MUST-FIX and 11 SHOULD-FIX findings of review round 3 are applied.
The lab and the lecture now say "has priority", so Q20 says "has priority over" in place of
"wins". probe4.sh also holds the Pod log-cmkeyref, the proof for the configMapKeyRef option
of Q8. This proof is also pending.
Round 6 (2026-11-11): the findings of review round 4 (2 MUST-FIX, 8 SHOULD-FIX) are applied.
Round 7 (2026-11-11): the findings of review round 5 (1 MUST-FIX, 5 SHOULD-FIX) are applied.
Q8 has new options B (stringData) and D (a non-root user). probe4.sh now holds the Pods
log-stringdata and log-nonroot, in place of log-cmkeyref. These proofs are also pending.
Round 8 (2026-11-11): the findings of review round 6 (0 MUST-FIX, 2 SHOULD-FIX) and the phrase cue "the Pod, and" are applied.
Round 9 (2026-11-11): the finding of review round 7 (0 MUST-FIX, 1 SHOULD-FIX) is applied.
Round 10 (2026-11-11): the finding of review round 8 (0 MUST-FIX, 1 SHOULD-FIX) is applied; the proof of Q18 is probe4.log @@Q18 (pending).
v2 (2026-11-18, Week 12 loop, report 2026-11-18-06): the proofs are live. Lab pass 1 and pass 2 of
lab v8 and the probes probe12.sh (scratchpad w12live/probe_p1.log) prove all 20 keys on Kubernetes
v1.35.10, also Q8 (secretKeyRef, stringData, non-root, Secret volume), Q18 and Q20. The text above
names the logs of 2026-11-10 and 2026-11-11; the proofs of Q8, Q18 and Q20 are no longer pending.
v2 review round 1 (1 MUST-FIX, 4 SHOULD-FIX, scratchpad w12review_r1/quiz.md) is applied:
- Q4 A: "the files of the volume are read-only" (the old option gave the key of Q14, D4).
- Q17: the stem names kube-root-ca.crt, which options A and C name (D2). The projected token
  volume of secret-pod in week12 holds ca.crt from the ConfigMap kube-root-ca.crt of the same
  namespace (pass 1, Step 4, and the projected volume of kubernetes.io service-accounts-admin).
- Q5 B: "Nothing, because cGFzc3dvcmQ= is the password" (the key was the only option with no
  credential, D3); Q5 D: "the cluster", not "the cluster database" (A1, the lecture says etcd).
- A1 -ing forms: the Q8 stem, the Q4 WHY and the Q14 IF D.
v2 review round 2 (1 MUST-FIX, 1 SHOULD-FIX, scratchpad w12review_r2/quiz.md) is applied:
- Q8 (D3, MUST-FIX): the non-root option kept "the same secretKeyRef", so a student could remove it with
  no knowledge, and the key was the only option "as a file". The key is now "Mount the Secret as a
  volume for the password, in place of secretKeyRef", and the wrong option is "Give the password
  through secretRef, in place of secretKeyRef in env". Its live proof is probe12b.sh (q8secretref).
- Q5 D (D3, D4): "The base64 encryption key of the cluster", so the key is not the only option with base64.
v2 review round 3 (0 MUST-FIX, 2 SHOULD-FIX, scratchpad w12review_r3/quiz.md) is applied:
- Q8 D (D3): no "in env" (secretRef is a field of envFrom); probe12b.sh still proves it.
- Q5 IF D (D6): "No key of the cluster protects the base64 text in this manifest" (a SealedSecret is the
  edge case of a manifest that a key protects).
Round 2 (2026-11-10): the 13 MUST-FIX and 18 SHOULD-FIX findings of review round 1 are
applied. Q4 uses the full volume, Q7 a Secret volume only, Q8 is a decision, Q11 asks for
the command, Q13 asks for printenv APP_COLOR, Q14 is an action, and Q16 reads a file of the
Secret volume. A1 words: reject, environment variable, master node, user.
"""

QUESTIONS = [
# ------------------------------------------------------------ the lecture
{"t": "injected environment variable",
 "q": "A Pod sets no env field and no envFrom field. Its container runs "
      "printenv KUBERNETES_SERVICE_HOST. What does the command show?",
 "a": ["The cluster IP address of the Service for the API server",
       "The IP address of the master node",
       "The IP address of the Pod itself",
       "The DNS name kubernetes.default.svc"],
 "why": "The kubelet injects environment variables for the Services of the namespace, "
        "and KUBERNETES_SERVICE_HOST for the API server. Its value is the cluster IP "
        "address of the Service kubernetes, for example 10.96.0.1 with the default "
        "Service subnet of kubeadm.",
 "mis": ["The API server runs on the master node. A Pod reaches it through the Service "
         "kubernetes, so the environment variable holds the cluster IP address of that Service.",
         "The environment variable gives the address of the API server, not the address "
         "of the Pod.",
         "kubernetes.default.svc is the DNS name of that Service; the environment variable "
         "holds its cluster IP address."]},

{"t": "missing configmap",
 "q": "The ConfigMap app-config is missing. You create a Pod that gets app-config "
      "through envFrom, and the reference sets no optional field. What happens?",
 "a": ["The API server accepts the Pod, and the kubelet does not start the container without app-config",
       "The API server rejects the Pod, and no Pod exists",
       "The container starts, and app-config stays missing",
       "The API server accepts the Pod, creates an empty ConfigMap app-config, and the kubelet starts the container"],
 "why": "The API server accepts the Pod, because it checks no reference to a ConfigMap. "
        "The kubelet does not start the container while the ConfigMap is missing, "
        "unless the reference sets optional: true.",
 "mis": ["The API server accepts the Pod. The kubelet checks the ConfigMap on the "
         "node, when it creates the container.",
         "This is the behavior of optional: true. Without it, the kubelet does not "
         "start the container while the ConfigMap is missing.",
         "The API server does not create the missing ConfigMap app-config; the kubelet "
         "waits until it exists."]},

{"t": "configmap size",
 "q": "A team runs kubectl create configmap big --from-file=data.bin. The file "
      "data.bin holds 2 MiB of text. What is the result?",
 "a": ["The API server rejects it, because a ConfigMap holds at most 1 MiB",
       "The API server stores the first 1 MiB of the ConfigMap, and it rejects the rest of the file",
       "The API server divides the file into two ConfigMaps of 1 MiB each",
       "The API server stores the whole ConfigMap, because a ConfigMap holds data of any size"],
 "why": "The API server checks the size of each ConfigMap, and it rejects a "
        "ConfigMap with more than 1 MiB of data. A Secret has the same limit.",
 "mis": ["The API server stores no part of an object that it rejects, so kubectl get "
         "configmap big shows NotFound.",
         "Kubernetes never divides one object into two objects.",
         "A ConfigMap and a Secret each hold at most 1 MiB."]},

{"t": "configmap volume",
 "q": "The Pod config-volume mounts the whole ConfigMap app-config as a volume at "
      "/etc/app-config. The ConfigMap holds APP_COLOR=blue. You change "
      "APP_COLOR to green with kubectl patch. Nobody restarts the Pod. What does the "
      "file /etc/app-config/APP_COLOR show three minutes later?",
 "a": ["The new value green, because the kubelet updates the files of the volume",
       "The old value, because the files of the volume are read-only",
       "An error, because the kubelet deletes the file of the volume",
       "The old value and green, because the kubelet adds the new value to the file of the volume"],
 "why": "The kubelet watches the ConfigMap, and it updates the files of the volume "
        "within about two minutes. The container then reads the new value while it runs.",
 "mis": ["The volume is read-only for the container, not for the kubelet, so the kubelet "
         "updates the files.",
         "The kubelet writes the new file, and then it replaces the old file in one action, "
         "so the file is always there.",
         "The kubelet replaces the content of the file, so the file holds only the new value."]},

{"t": "secret manifest in git",
 "q": "A Secret manifest in a public Git repository holds the line "
      "DB_Password: cGFzc3dvcmQ= in its data field. What does a reader of the "
      "repository need to get the password?",
 "a": ["The base64 decoder program on any computer",
       "The base64 encryption key of the cluster",
       "The private key of the API server",
       "Nothing, because cGFzc3dvcmQ= is the password"],
 "why": "The data field holds base64 text. base64 is an encoding, not encryption: "
        "anyone can decode it, with no key. Never put a Secret manifest in "
        "source control.",
 "mis": ["base64 is an encoding, not encryption. No key of the cluster protects the base64 "
         "text in this manifest.",
         "The key of the API server protects the HTTPS connection, not the text in a file.",
         "cGFzc3dvcmQ= is the base64 form of the password, so the reader needs a base64 decoder."]},

{"t": "secret data",
 "q": "A Secret manifest holds the line DB_Password: paswrd in its data field, as plain "
      "text. You run kubectl apply -f with this manifest. What is the result?",
 "a": ["The API server rejects the Secret, and it stores nothing",
       "The Secret holds paswrd as it is, and a Pod gets paswrd",
       "The API server encodes paswrd to base64, and it stores the Secret",
       "The API server stores the Secret, and a Pod that uses the key does not start"],
 "why": "Each value of the data field must be valid base64 text. paswrd is not "
        "valid base64, so the API server rejects the Secret. The stringData field "
        "takes plain text, and the API server encodes it.",
 "mis": ["The API server decodes each data value, and it stores no value that "
         "fails to decode.",
         "Only the stringData field gets this encoding; the data field must hold "
         "base64 text already.",
         "The API server checks the value when you apply the Secret, before a Pod uses it."]},

{"t": "secret volume access",
 "q": "The Pod app runs on workernode1. It gets the Secret db only through a Secret "
      "volume. Which user can read the Secret value?",
 "a": ["A user who can run kubectl exec in the Pod app",
       "A user who can run kubectl describe pod app",
       "A user who reads the disk of workernode1 after the node stops",
       "A user who can read the kubelet log of workernode1"],
 "why": "The kubelet stores the files of a Secret volume in tmpfs, in the memory of "
        "workernode1, not on its disk. tmpfs gives no protection inside the Pod: a user "
        "who can run kubectl exec can read each file of the volume.",
 "mis": ["kubectl describe pod shows the name of the Secret of the volume, not its values.",
         "tmpfs is in memory, so the files of the Secret are not on the disk of workernode1.",
         "The kubelet writes no Secret value to its log."]},

{"t": "secret and application log",
 "q": "An application writes all of its environment variables to its log at start. "
      "Its Pod gets DB_Password from a Secret through secretKeyRef, so the log holds the "
      "password. Which change prevents this?",
 "a": ["Mount the Secret as a volume for the password, in place of secretKeyRef",
       "Give the password through secretRef, in place of secretKeyRef",
       "Configure encryption at rest for the Secret data",
       "Give the password with stringData, in place of data in the Secret"],
 "why": "A file of a Secret volume is not an environment variable, so the application "
        "does not write it to its log with its environment variables. For this "
        "reason, a Secret volume is the better method.",
 "mis": ["secretRef also gives each key of the Secret as an environment variable, so the "
         "application still writes the password to its log.",
         "Encryption at rest protects the data in etcd; the container still gets the "
         "plain value as an environment variable.",
         "stringData changes only the manifest: the API server stores the value in data, "
         "and secretKeyRef still gives an environment variable."]},

{"t": "token mount",
 "q": "A Pod sets automountServiceAccountToken: false. Its container runs ls "
      "/var/run/secrets/kubernetes.io/serviceaccount. What is the result?",
 "a": ["An error, because the directory with ca.crt and the rest of the files does not exist",
       "The files ca.crt, namespace and token",
       "An error, because no user except root can read the files",
       "The files ca.crt and namespace, because false stops only the token"],
 "why": "When the Pod sets automountServiceAccountToken: false, the kubelet mounts no "
        "token volume, so the directory does not exist. A value in the Pod has priority "
        "over the value in its ServiceAccount.",
 "mis": ["The value false in the Pod stops the whole mount, so no file of the token "
         "volume exists.",
         "The kubelet mounts no token volume at all, so no file exists for any user.",
         "The kubelet mounts the three files together, or none of them."]},

{"t": "default serviceaccount",
 "q": "A process in a Pod sends a request to the API server to list the Pods of "
      "its namespace. It uses the token of the ServiceAccount default. Nobody gave "
      "this ServiceAccount more permissions. What is the result, and why?",
 "a": ["The API server rejects it, because the ServiceAccount of the token can only read API discovery data",
       "The API server rejects it, because the token is no longer valid",
       "The API server returns the Pods, because the token of the ServiceAccount belongs to that namespace",
       "The API server returns only the Pod of the process, because the token identifies that Pod"],
 "why": "The ServiceAccount default has API discovery permissions only. A request "
        "to list Pods gets the answer 403 Forbidden.",
 "mis": ["The API server accepts the token and names the ServiceAccount in its answer; "
         "the missing permission causes the rejection.",
         "The ServiceAccount default has no permission to list Pods, also in its "
         "own namespace.",
         "The token identifies the ServiceAccount, and the API server gives no special "
         "access to the Pod of the process."]},

# ------------------------------------------------------------ the lab
{"t": "args",
 "q": 'The image maziar/fortune:args has ENTRYPOINT ["/bin/fortuneloop.sh"] and '
      'CMD ["10"]. You create a Pod from this image with args: ["2"] and no command field. '
      'What is the result?',
 "a": ["The container runs /bin/fortuneloop.sh 2",
       "The container runs /bin/fortuneloop.sh 10",
       "The container runs /bin/fortuneloop.sh 10 2",
       "The API server rejects the Pod, because args needs a command field"],
 "fix": ["The container runs /bin/fortuneloop.sh 2",
         "The container runs /bin/fortuneloop.sh 10",
         "The container runs /bin/fortuneloop.sh 10 2",
         "The API server rejects the Pod, because args needs a command field"],
 "why": "args replaces the CMD of the image, and the ENTRYPOINT stays. The "
        "container runs /bin/fortuneloop.sh 2, and its log shows: Configured to "
        "generate new fortune every 2 seconds.",
 "mis": ["CMD gives the value 10, and args replaces CMD.",
         "args replaces CMD; Kubernetes does not add args after CMD.",
         "A Pod can set args with no command field; the ENTRYPOINT of the image "
         "then runs."]},

{"t": "from file",
 "q": "The directory /home/ubuntu holds the file LOG_LEVEL with the text debug. In "
      "/home/ubuntu, you run kubectl create configmap app-config --from-file=LOG_LEVEL. "
      "The Pod config-env gets app-config through envFrom. The Pod has no other "
      "reference to app-config. You run kubectl exec config-env -- printenv LOG_LEVEL. "
      "What does the command show?",
 "a": ["The text debug",
       "The text LOG_LEVEL",
       "The path /home/ubuntu/LOG_LEVEL",
       "No value, because envFrom injects only the keys of --from-literal"],
 "why": "--from-file creates one key from a file: the file name LOG_LEVEL is the "
        "key, and the file content debug is the value. envFrom injects each key "
        "as an environment variable.",
 "mis": ["The file name becomes the key, and the content of the file becomes the value.",
         "--from-file reads the content of the file; the path is not the value.",
         "envFrom injects each key, also a key from --from-file."]},

{"t": "configmap key",
 "q": "The ConfigMap app-config holds APP_COLOR=blue. The container of the Pod keyref "
      "sets the environment variable COLOR through valueFrom with configMapKeyRef "
      "(name app-config, key APP_COLOR). The Pod has no other reference to app-config. "
      "You run kubectl exec keyref -- printenv APP_COLOR. What does the command show?",
 "a": ["Exit code 1 with no value, because the key gives its value to COLOR",
       "blue",
       "COLOR",
       "An error, because the container does not start when COLOR differs from the key APP_COLOR"],
 "why": "configMapKeyRef gives the value of one key to the environment variable that "
        "env names, here COLOR. The key APP_COLOR does not become an environment "
        "variable of its own, so printenv APP_COLOR finds nothing. kubectl exec then "
        "shows: command terminated with exit code 1.",
 "mis": ["Only envFrom injects each key as an environment variable; configMapKeyRef gives "
         "the value to COLOR only.",
         "COLOR is the name of the environment variable, not the value of APP_COLOR.",
         "The env name can differ from the key name; configMapKeyRef connects them, and "
         "the container starts."]},

{"t": "configmap environment",
 "q": "You apply the file config-env.yaml, which holds the manifest of the Pod "
      "config-env. The Pod gets APP_COLOR=blue from the ConfigMap app-config through "
      "envFrom. You change "
      "APP_COLOR to green with kubectl patch, but printenv APP_COLOR in config-env "
      "still shows blue. Which action makes it show green?",
 "a": ["Delete the Pod, and create it again from config-env.yaml",
       "Wait five minutes, and run the printenv command again",
       "Open a new shell in the Pod config-env with kubectl exec, and run printenv APP_COLOR in it",
       "Run kubectl apply -f config-env.yaml again, with no change"],
 "why": "A container gets its environment variables when it starts. A new Pod from "
        "the same manifest starts a new container, and it gets green.",
 "mis": ["The kubelet updates the files of a ConfigMap volume, not the environment "
         "variables of a container that runs.",
         "Each process gets the environment of the container start, so the new shell "
         "shows blue.",
         "kubectl apply with no change leaves the Pod unchanged, so the container "
         "does not start again."]},

{"t": "secret type",
 "q": "You create a Secret with kubectl create secret generic app-secret "
      "--from-literal=DB_Host=mysql. What TYPE does kubectl get secrets show "
      "for app-secret?",
 "a": ["Opaque",
       "generic",
       "kubernetes.io/tls",
       "base64"],
 "fix": ["base64",
         "generic",
         "kubernetes.io/tls",
         "Opaque"],
 "why": "kubectl create secret generic creates a Secret of the type Opaque, which "
        "holds any key/value pairs.",
 "mis": ["generic is the name of the kubectl subcommand; the type that it creates "
         "is Opaque.",
         "kubernetes.io/tls is the type for a TLS certificate and its key.",
         "base64 is the encoding of the values in the API; the TYPE column shows the "
         "type of the Secret."]},

{"t": "secret file",
 "q": "The Secret app-secret holds DB_Host=mysql, from --from-literal. The Pod "
      "secret-pod mounts app-secret as a volume at /etc/secret-volume. What does "
      "cat /etc/secret-volume/DB_Host show in the container?",
 "a": ["mysql",
       "bXlzcWw=",
       "DB_Host=mysql",
       "DB_Host=bXlzcWw="],
 "fix": ["bXlzcWw=",
         "DB_Host=bXlzcWw=",
         "mysql",
         "DB_Host=mysql"],
 "why": "Each key of the Secret is a file, and the kubelet writes the decoded value "
        "into it. The application needs no base64 decoder.",
 "mis": ["bXlzcWw= is the base64 form that the API shows; the file holds the decoded value.",
         "The key is the name of the file, and the file holds only the value.",
         "The key is the name of the file, and the file holds only the decoded value."]},

{"t": "token secret",
 "q": "You create the namespace week12, and Kubernetes adds kube-root-ca.crt to it. In week12, "
      "you create the Secret app-secret with "
      "kubectl create secret generic, and then the Pod secret-pod. secret-pod uses the "
      "ServiceAccount default, and the kubelet mounts its token into secret-pod. The "
      "cluster runs Kubernetes v1.35. Which Secrets does kubectl get secrets -n week12 list?",
 "a": ["app-secret, and no other Secret",
       "app-secret and a token Secret, and no other Secret",
       "app-secret and kube-root-ca.crt only",
       "app-secret, a token Secret and kube-root-ca.crt"],
 "fix": ["app-secret, a token Secret and kube-root-ca.crt",
         "app-secret and a token Secret, and no other Secret",
         "app-secret and kube-root-ca.crt only",
         "app-secret, and no other Secret"],
 "why": "The kubelet gets a token from the TokenRequest API, and it puts the token in "
        "a projected volume. Since v1.24, Kubernetes creates no Secret for a "
        "ServiceAccount token, and kube-root-ca.crt is a ConfigMap. So the list "
        "shows app-secret only.",
 "mis": ["Since v1.24, Kubernetes creates no token Secret for a ServiceAccount.",
         "kube-root-ca.crt is a ConfigMap, not a Secret.",
         "kube-root-ca.crt is a ConfigMap, and no Secret holds the token."]},

{"t": "environments",
 "q": "The namespace week12 has the ConfigMap app-config with APP_COLOR=blue. The "
      "namespace week12-dev has its own ConfigMap app-config with APP_COLOR=red. "
      "The namespace default has its own ConfigMap app-config with APP_COLOR=green. "
      "You apply the file config-env.yaml, which holds the manifest of the Pod "
      "config-env, in week12-dev. The Pod gets app-config through envFrom. Then you run kubectl exec config-env -n week12-dev -- printenv "
      "APP_COLOR. What does the command show?",
 "a": ["red, from the ConfigMap of the namespace week12-dev",
       "blue, from the ConfigMap of the namespace week12",
       "green, because envFrom uses the ConfigMap of the namespace default",
       "An error, because configMapRef must also name the namespace week12-dev"],
 "why": "A Pod uses the ConfigMap of its own namespace. The same manifest gets "
        "red in week12-dev and blue in week12, so one manifest serves many "
        "environments.",
 "mis": ["A Pod uses no ConfigMap of another namespace.",
         "envFrom uses the ConfigMap of the namespace of the Pod, not of the namespace default, "
         "so the container gets red.",
         "configMapRef has no namespace field; the namespace of the Pod gives it."]},

{"t": "etcd storage",
 "q": "With etcdctl in the Pod etcd-masternode, you read "
      "/registry/secrets/week12-dev/app-secret. The Secret holds DB_Password=dev-pass. Nobody configured "
      "encryption at rest. What does the output hold?",
 "a": ["The value dev-pass, as plain bytes",
       "The base64 text ZGV2LXBhc3M= only",
       "A hash of dev-pass, because etcd hashes each password",
       "The metadata, because etcd stores no Secret value"],
 "why": "By default, the API server writes a Secret to etcd as plain bytes. A user "
        "who can read etcd or its backup can read the value. Encryption at rest "
        "changes this.",
 "mis": ["etcd holds the data of the Secret as decoded bytes, so dev-pass is in the "
         "output.",
         "A Pod needs the value, and a hash cannot return the value. Without "
         "encryption at rest, the API server writes the value as plain bytes.",
         "etcd holds the whole object of the Secret, with its metadata and its data."]},

{"t": "env and envfrom",
 "q": "The ConfigMap app-config holds APP_COLOR=red. You create a Pod with one container "
      "that gets app-config through envFrom and configMapRef. The container also sets "
      "APP_COLOR to blue in its env field. You run printenv APP_COLOR in it with kubectl exec. What does "
      "the command show?",
 "a": ["blue, because env has priority over envFrom",
       "red, because the value of envFrom replaces the value of env",
       "blue and red, on two lines, because the container gets both values",
       "An error, because the API server rejects one environment variable in env and in envFrom"],
 "why": "When env and envFrom set the same name, the value of env has priority over "
        "the value of envFrom. The container gets APP_COLOR=blue, so printenv shows blue.",
 "mis": ["The value of envFrom does not replace the value of env; the value of env has "
         "priority over the value of envFrom.",
         "An environment variable has one value, so printenv shows one line for one name.",
         "The API server accepts APP_COLOR in env and in envFrom, and the value of env has "
         "priority over the value of envFrom."]},
]
