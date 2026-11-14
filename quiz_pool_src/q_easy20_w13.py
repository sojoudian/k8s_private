# -*- coding: utf-8 -*-
"""CLO835 - 20 easy questions from the lecture on authentication, RBAC, ServiceAccounts and
Amazon EKS access, and from the lab that practises them on a kubeadm cluster.

Each record holds:
  t    the topic (it becomes the neutral title)
  q    the stem
  a    the four options; the first one is correct
  fix  (optional) the four options in their logical order
  why  the feedback for the correct option
  mis  the mistake that each wrong option shows, in the order of a[1:]

Questions 1 to 10 come from the lecture, and questions 11 to 20 from the lab.
The lecture questions use only the core facts that lecture v9 must keep: the request path,
no stored users, the client certificate (CN and O), system:anonymous, the order of the
authorization modes, the scope of RBAC objects, the default ClusterRoles, no deny rule,
system:masters, ServiceAccount user names, and EKS access entries.

Each key has a proof: the live lab log peerlive/pass.log of 2026-11-11 (Kubernetes v1.35.10),
a probe marker "@@Qn" of probe_w13.sh, or a quote of the Kubernetes v1.35 or the AWS
documentation. The proof map goes in the report of this quiz.

Round 1 (2026-11-11): the first draft. The probe proofs are pending. probe_w13.log does not
exist until the owner runs probe_w13.sh on the master node, after the lab pass 1.
Lecture v9 (Lecture_week13_v9.pdf of 2026-11-11 03:45) teaches each fact of questions 1 to 10:
slides 5, 6, 8, 11, 14, 15, 17, 18 and 26. No independent review has run yet.
Round 2 (2026-11-11): the findings of review round 1 (1 MUST-FIX, 15 SHOULD-FIX) are applied.
Lecture v9 of 04:37 (review rounds 2 and 3 of the deck) still teaches each fact of questions
1 to 10. No key and no WHY says "RBAC denies": the deck says that no authorizer allows the
request, so the API server answers 403 Forbidden.
Round 3 (2026-11-11): the findings of review round 2 (0 MUST-FIX, 8 SHOULD-FIX) are applied.
Round 4 (2026-11-11): the findings of review round 3 (0 MUST-FIX, 2 SHOULD-FIX) are applied.
Round 5 (2026-11-11): the findings of review round 4 (0 MUST-FIX, 2 SHOULD-FIX) are applied.
Round 6 (2026-11-11): the finding of review round 5 (0 MUST-FIX, 1 SHOULD-FIX: the CSR also
holds a signature) is applied to the Q13 feedback.
Round 7 (2026-11-11): the finding of review round 6 (0 MUST-FIX, 1 SHOULD-FIX: "sign" in the Q11
feedback has the certificate as its object) is applied.
"""

QUESTIONS = [
# ------------------------------------------------------------ the lecture
{"t": "api server phases",
 "q": "The certificate authority (CA) of the cluster signed a client certificate for the "
      "user ana. No binding names ana, and ana has no permission on Pods. No namespace shop"
      " exists, and admission control rejects each new object in a missing namespace. ana "
      "runs kubectl run web --image=maziar/kubia:v1 -n shop. What does ana get, and why?",
 "a": ["Forbidden, because authorization denies ana before admission control sees the request",
       "NotFound, because admission control runs before authorization",
       "Forbidden, because admission control checks ana before authorization",
       "BadRequest, because admission control checks the namespace before authentication"],
 "why": "The API server checks a request in this order: authentication, then authorization,"
        " then admission control. The certificate of ana passes authentication. No "
        "authorizer allows the request of ana, so the API server returns 403 Forbidden, and"
        " admission control never sees the request.",
 "mis": ["Admission control runs after authorization, and only for a request that "
         "authorization allows. An administrator gets NotFound for this command.",
         "Admission control runs after authorization, and only for a request that "
         "authorization allows. Here authorization denies the request first.",
         "Authentication runs first. The check of the namespace is part of admission "
         "control, and admission control runs last."]},

{"t": "users",
 "q": "On the master node of a kubeadm cluster, the kubeconfig file holds the users "
      "kubernetes-admin and dev-user. The certificate authority (CA) of the cluster signed "
      "the certificate of dev-user after kubectl certificate approve dev-user. You run "
      "kubectl get users. What does the command show?",
 "a": ["An error, because the API server has no type users",
       "kubernetes-admin and dev-user, the users of the kubeconfig file",
       "dev-user, because kubectl certificate approve creates a User object",
       "No resources found"],
 "why": "Kubernetes stores no users. The API server has no User object and no type users, "
        "so kubectl get users fails. It shows the error: the server doesn't have a resource"
        ' type "users". A user is only a name in a credential, for example the CN of a '
        "client certificate.",
 "mis": ["kubectl config get-users shows the users of the kubeconfig file. kubectl get "
         "users asks the API server, and the API server has no type users.",
         "kubectl certificate approve lets the cluster CA sign the certificate. It creates "
         "no User object, because Kubernetes has no User object.",
         "kubectl shows No resources found for a known type with no objects. The API server"
         " knows no type users."]},

{"t": "request without credentials",
 "q": "A kubeadm cluster runs with the default settings. On the master node, you run curl "
      "-k https://localhost:6443/api/v1/namespaces/default/pods with no token and no client"
      " certificate. What does the API server return?",
 "a": ["403 Forbidden for the user system:anonymous",
       "401 Unauthorized, because the request has no credentials",
       "403 Forbidden for the user system:unauthenticated",
       "A PodList of default, because the API server skips authorization with -k"],
 "fix": ["401 Unauthorized, because the request has no credentials",
         "403 Forbidden for the user system:anonymous",
         "403 Forbidden for the user system:unauthenticated",
         "A PodList of default, because the API server skips authorization with -k"],
 "why": "Anonymous authentication is active by default. The API server gives a request with"
        " no credentials the user system:anonymous and the group system:unauthenticated. No"
        " authorizer allows this user to list Pods, so the API server returns 403 "
        "Forbidden.",
 "mis": ["401 is the answer for credentials that the API server rejects. A request with no "
         "credentials becomes the user system:anonymous, and the API server returns 403, "
         "because no authorizer allows the request.",
         "system:unauthenticated is the group of an anonymous request. The message names "
         "the user, system:anonymous.",
         "-k only stops curl from verifying the certificate of the API server. The API "
         "server still checks the request."]},

{"t": "authorization order",
 "q": "The API server runs with --authorization-mode=Node,RBAC,Webhook. A RoleBinding in "
      "the namespace dev binds a Role with get and list on Pods to the user joe. The "
      "webhook denies each request of joe. joe runs kubectl get pods -n dev. Which "
      "authorizer decides this request?",
 "a": ["RBAC: it gives an allow, so the API server stops the check there",
       "The webhook: the API server gives a deny priority over an allow",
       "Node: the API server lets the first mode of the flag decide",
       "All three: the API server needs each authorizer to allow it"],
 "fix": ["Node: the API server lets the first mode of the flag decide",
         "RBAC: it gives an allow, so the API server stops the check there",
         "The webhook: the API server gives a deny priority over an allow",
         "All three: the API server needs each authorizer to allow it"],
 "why": "The API server asks the authorizers in the order of the flag. The first allow or "
        "deny decides, and no other authorizer runs. Node has no opinion on a request of "
        "joe. RBAC allows it, so the webhook gets no question.",
 "mis": ["The first allow or deny decides. The webhook is after RBAC in the list, so the "
         "API server does not ask it.",
         "The Node authorizer decides only on requests of kubelets. For joe, it has no "
         "opinion, and the next authorizer runs.",
         "One allow is enough. The API server stops at the first authorizer that allows or "
         "denies the request."]},

{"t": "rolebinding scope",
 "q": "A RoleBinding in the namespace dev binds the default ClusterRole edit to the user "
      "ben. ben has no other permission on Pods. The cluster also has the namespaces "
      "default, kube-system and prod. In which namespaces can ben list Pods?",
 "a": ["Only in dev, because the RoleBinding is in the namespace dev",
       "In dev and in default only",
       "In every namespace, because the RoleBinding names a ClusterRole for the whole cluster",
       "In every namespace except kube-system"],
 "fix": ["Only in dev, because the RoleBinding is in the namespace dev",
         "In dev and in default only",
         "In every namespace except kube-system",
         "In every namespace, because the RoleBinding names a ClusterRole for the whole cluster"],
 "why": "A RoleBinding gives the rules of a ClusterRole only in the namespace of the "
        "RoleBinding. So ben can list Pods in dev, and the API server denies the same "
        "request in each other namespace.",
 "mis": ["The namespace default gets no special permissions. The RoleBinding in dev gives "
         "nothing in default.",
         "A ClusterRole is only a set of rules. The binding decides where the rules apply, "
         "and a RoleBinding applies them in its own namespace.",
         "kube-system gets no special rule here. The RoleBinding gives nothing outside dev."]},

{"t": "view role",
 "q": "A RoleBinding in the namespace qa binds the default ClusterRole view to the user "
      "lee. The user lee has no other permission in qa. The namespace qa has the Deployment"
      " web with its Pods, the ConfigMap settings and the Secret db. Which command of lee "
      "gets the answer Forbidden?",
 "a": ["kubectl get secrets -n qa",
       "kubectl get configmaps -n qa",
       "kubectl get deployments -n qa",
       "kubectl get pods -n qa"],
 "fix": ["kubectl get configmaps -n qa",
         "kubectl get deployments -n qa",
         "kubectl get pods -n qa",
         "kubectl get secrets -n qa"],
 "why": "The ClusterRole view gives read access to most objects of a namespace, but not to "
        "Secrets. A Secret can hold the token of a ServiceAccount, so read access to "
        "Secrets would give more permissions.",
 "mis": ["view can read the ConfigMaps of qa. Of these four types, view excludes only "
         "Secrets.",
         "view can read the Deployments of qa. Of these four types, view excludes only "
         "Secrets.",
         "view can read the Pods of qa. Of these four types, view excludes only Secrets."]},

{"t": "two bindings",
 "q": "In the namespace dev, the RoleBinding admin-binding binds the Role pod-admin to the "
      "user sam. pod-admin gives create, update and delete on Pods. The newer RoleBinding "
      "reader-binding binds the Role pod-reader to sam, and pod-reader gives get and list "
      "on Pods. Which verbs on Pods can sam use in dev, and why?",
 "a": ["All five verbs, because RBAC adds the rules of every binding",
       "Only get and list, because RBAC uses the newer binding and ignores the older binding",
       "No verb, because two Roles with different rules conflict",
       "Only create, update and delete, because RBAC uses the older binding and ignores the newer binding"],
 "fix": ["No verb, because two Roles with different rules conflict",
         "Only get and list, because RBAC uses the newer binding and ignores the older binding",
         "Only create, update and delete, because RBAC uses the older binding and ignores the newer binding",
         "All five verbs, because RBAC adds the rules of every binding"],
 "why": "RBAC rules only add permissions, and RBAC has no deny rule. The user sam gets the "
        "rules of both bindings, so sam can use all five verbs.",
 "mis": ["A newer RoleBinding replaces no older binding. RBAC adds the rules of both.",
         "Two RBAC rules cannot conflict, because each rule only adds permissions.",
         "An older RoleBinding blocks no newer binding. RBAC adds the rules of both."]},

{"t": "system masters",
 "q": "The user ops-lead is a member of the group system:masters. An administrator deletes "
      "the ClusterRoleBinding cluster-admin. Now no binding names ops-lead or "
      "system:masters. The node workernode2 exists, and ops-lead runs kubectl delete node "
      "workernode2. What is the result, and why?",
 "a": ["Deleted, because the group system:masters bypasses each check of the authorization modes",
       "Forbidden, because only super-admin.conf gives the power of system:masters",
       "NotFound for workernode2, because ops-lead can see no node without a binding",
       "Forbidden, because the RBAC check now denies each request of the group system:masters"],
 "why": "The group system:masters bypasses all authorization checks, also RBAC and Webhook."
        " No binding can limit this access, so the API server deletes the node.",
 "mis": ["Each credential with the group system:masters bypasses authorization. "
         "super-admin.conf is only one example of such a credential.",
         "The request passes authorization, and the node exists, so the API server deletes "
         "it.",
         "RBAC does not check system:masters. The group has full access with no binding."]},

{"t": "certificate subject",
 "q": "The certificate authority (CA) of the cluster signs a client certificate with the "
      "subject /CN=kim/O=ops/O=audit. No object with the name ops or audit exists in the "
      "cluster. Which user name and which groups does the API server get from this "
      "certificate?",
 "a": ["The user kim in the group ops and in the group audit",
       "The user kim in the group ops, from the first O field",
       "The user kim in the group audit, from the last O field",
       "The user kim with no group, because a group must exist as an object"],
 "fix": ["The user kim in the group ops, from the first O field",
         "The user kim in the group audit, from the last O field",
         "The user kim in the group ops and in the group audit",
         "The user kim with no group, because a group must exist as an object"],
 "why": "The API server takes the user name from the common name (CN), and one group from "
        "each organization (O) field. A group is no object in the API server, so ops and "
        "audit need no object.",
 "mis": ["Each O field gives one group, so the second O field adds the group audit.",
         "Each O field gives one group, so the first O field also adds the group ops.",
         "A group is only a name in the certificate. The API server needs no object for it."]},

{"t": "eks identities",
 "q": "A team creates a new Amazon EKS cluster. The IAM role ci-deployer must run kubectl "
      "commands on this cluster. Which method does AWS recommend for this?",
 "a": ["An access entry for ci-deployer",
       "A mapRoles item for ci-deployer in aws-auth",
       "A client certificate for ci-deployer that the EKS cluster signs",
       "An RBAC binding that names ci-deployer, with no other change"],
 "why": "AWS recommends the access entry. You manage each access entry with the EKS API, "
        "the AWS CLI or the AWS console. The aws-auth ConfigMap is deprecated.",
 "mis": ["AWS marks the aws-auth ConfigMap as deprecated, and it recommends the access "
         "entry in its place.",
         "Amazon EKS authenticates an IAM role through AWS IAM, and an access entry maps it"
         " to Kubernetes. A client certificate is no IAM identity.",
         "RBAC decides what a user can do. Without an access entry or an aws-auth item, the"
         " API server cannot map the IAM role to a Kubernetes user."]},

# ------------------------------------------------------------ the lab
{"t": "csr condition",
 "q": "You create the certificate signing request (CSR) qa-user with the signer "
      "kubernetes.io/kube-apiserver-client and the usage client auth. Nobody approves or "
      "denies it. Two minutes later, you run kubectl get csr qa-user. What does the "
      "CONDITION column show?",
 "a": ["Pending",
       "Approved,Issued",
       "Denied",
       "Failed"],
 "fix": ["Approved,Issued",
         "Denied",
         "Failed",
         "Pending"],
 "why": "kube-controller-manager never approves a request for the signer "
        "kubernetes.io/kube-apiserver-client. The request stays Pending until an "
        "administrator approves or denies it. After 24 hours, Kubernetes deletes a Pending "
        "request.",
 "mis": ["Approved,Issued comes only after kubectl certificate approve. No controller "
         "approves this signer.",
         "Denied comes only after kubectl certificate deny.",
         "Failed means that the signer could not sign the certificate of an approved request. Nobody approved "
         "this request."]},

{"t": "certificate lifetime",
 "q": "The file dev-user-csr.yaml sets expirationSeconds: 86400 in the certificate signing "
      "request (CSR) dev-user. You apply it, and you run kubectl certificate approve "
      "dev-user. How long is the signed certificate of dev-user valid?",
 "a": ["24 hours",
       "1 year",
       "86400 hours",
       "86400 days"],
 "fix": ["24 hours",
         "1 year",
         "86400 hours",
         "86400 days"],
 "why": "expirationSeconds gives the lifetime in seconds. 86400 seconds are 24 hours, so "
        "kubectl get csr shows REQUESTEDDURATION 24h, and the certificate expires one day "
        "later.",
 "mis": ["One year is the default lifetime of the signer, for a CSR with no "
         "expirationSeconds.",
         "The value is in seconds, not in hours.",
         "The value is in seconds, not in days."]},

{"t": "certificate request",
 "q": "You create dev-user.key with openssl genrsa, and dev-user.csr with openssl req and "
      "this key. The file dev-user-csr.yaml holds a certificate signing request (CSR) for "
      "dev-user, and kubectl apply sends it to the API server. Which data does the request "
      "field of this CSR hold?",
 "a": ["The content of dev-user.csr, as base64 text",
       "The content of dev-user.key, as base64 text",
       "The content of dev-user.key and dev-user.csr, as base64 text",
       "Only the subject of dev-user.csr, as base64 text"],
 "fix": ["Only the subject of dev-user.csr, as base64 text",
         "The content of dev-user.csr, as base64 text",
         "The content of dev-user.key and dev-user.csr, as base64 text",
         "The content of dev-user.key, as base64 text"],
 "why": "The request field holds the file dev-user.csr as base64 text. This file holds the "
        "subject and the public key, and openssl req signs it with dev-user.key. No API object "
        "holds the private key dev-user.key.",
 "mis": ["The private key never goes to the API server. The request field holds "
         "dev-user.csr, with the public key.",
         "The private key never goes to the API server. The request field holds only "
         "dev-user.csr.",
         "The request field holds all of dev-user.csr, and this file also holds the public key and "
         "a signature."]},

{"t": "serviceaccount user",
 "q": "The Pod curl-sa runs in the namespace week13 as the ServiceAccount clo835. No Role "
      "and no binding names clo835 yet. The Pod sends a request to list the Services of "
      "week13 with curl and the token of clo835. The API server returns 403 Forbidden. "
      "Which user does the message name?",
 "a": ["system:serviceaccount:week13:clo835",
       "system:serviceaccount:clo835",
       "system:serviceaccount:clo835:week13",
       "system:serviceaccounts:week13"],
 "fix": ["system:serviceaccount:clo835",
         "system:serviceaccount:clo835:week13",
         "system:serviceaccount:week13:clo835",
         "system:serviceaccounts:week13"],
 "why": "The token of a ServiceAccount gives the user name system:serviceaccount:, then the"
        " namespace, then the name of the ServiceAccount. The 403 message names "
        "system:serviceaccount:week13:clo835.",
 "mis": ["The user name of a ServiceAccount also has its namespace, week13, before the name"
         " clo835.",
         "The namespace comes first, and the name of the ServiceAccount comes last.",
         "system:serviceaccounts:week13 is the group of all ServiceAccounts of week13. The "
         "message names the user."]},

{"t": "role verbs",
 "q": "In the namespace sales, the RoleBinding devuser-developer-binding binds the Role "
      "developer to dev-user. The Role gives list, get, create and update on Pods. No other"
      " binding gives dev-user a permission on Pods. The Pod web runs in sales, and no Pod "
      "api exists. dev-user runs each command with --context=dev-user@kubernetes -n sales. "
      "Which command gets the answer Forbidden?",
 "a": ["kubectl delete pod web",
       "kubectl get pods",
       "kubectl get pod web",
       "kubectl run api --image=maziar/kubia:v1"],
 "fix": ["kubectl delete pod web",
         "kubectl get pod web",
         "kubectl get pods",
         "kubectl run api --image=maziar/kubia:v1"],
 "why": "RBAC allows only the verbs of the rules. The Role developer has no verb delete, so"
        " kubectl delete pod web gets Forbidden.",
 "mis": ["kubectl get pods uses the verb list, and the Role gives list.",
         "kubectl get pod web uses the verb get, and the Role gives get.",
         "kubectl run uses the verb create, and the Role gives create."]},

{"t": "resource names",
 "q": "No binding in the namespace dev applies to dev-user yet. You create a Role in dev "
      'with one rule and the verbs ["create"], and a RoleBinding in dev that binds this '
      "Role to dev-user. Which rule lets dev-user run kubectl --context=dev-user@kubernetes"
      " create configmap app-config --from-literal=APP_COLOR=blue -n dev?",
 "a": ['apiGroups [""] and resources ["configmaps"]',
       'apiGroups [""] and resources ["ConfigMap"]',
       'apiGroups ["core"] and resources ["configmaps"]',
       'apiGroups ["core"] and resources ["ConfigMap"]'],
 "fix": ['apiGroups [""] and resources ["ConfigMap"]',
         'apiGroups [""] and resources ["configmaps"]',
         'apiGroups ["core"] and resources ["ConfigMap"]',
         'apiGroups ["core"] and resources ["configmaps"]'],
 "why": "RBAC matches the name in the API path: configmaps, in lowercase and in the plural."
        " ConfigMaps are in the core group, and RBAC writes the core group as the empty "
        'string "".',
 "mis": ["ConfigMap is the kind. RBAC compares the rule with the name configmaps of the API"
         " path, so this rule matches nothing.",
         "RBAC writes the core group as the empty string, not as core. This rule matches no"
         " API group.",
         "This rule has two mistakes: ConfigMap is the kind, and RBAC writes the core group"
         " as the empty string."]},

{"t": "api paths",
 "q": "On the master node of a kubeadm cluster with the default settings, you run curl -k "
      "with no token and no client certificate. You ask the API server for the paths /api, "
      "/apis, /apis/apps and /version. Which path returns its data?",
 "a": ["/version",
       "/api",
       "/apis",
       "/apis/apps"],
 "fix": ["/api",
         "/apis",
         "/apis/apps",
         "/version"],
 "why": "The default ClusterRole system:public-info-viewer lets every client read /version,"
        " also a client with no credentials. The discovery paths /api, /apis and /apis/apps"
        " need an authenticated user.",
 "mis": ["/api shows the versions of the core group. Only an authenticated user can read "
         "it.",
         "/apis shows the named API groups. Only an authenticated user can read it.",
         "/apis/apps shows the versions of the group apps. Only an authenticated user can "
         "read it."]},

{"t": "cacert flag",
 "q": "The Pod curl-sa runs as the ServiceAccount clo835. In curl-sa, you send a request to"
      " https://kubernetes.default.svc with the header Authorization: Bearer and the token "
      "of clo835. The command has no --cacert flag with the file ca.crt, and no -k flag. "
      "What is the result?",
 "a": ["curl rejects the certificate of the API server, and the request gets no answer",
       "The request works, because the token alone is enough for HTTPS",
       "The API server rejects the request, because it needs ca.crt to check the Pod",
       "curl sends the request with no TLS, and the token goes as plain text"],
 "why": "ca.crt holds the certificate of the cluster certificate authority (CA). curl uses "
        "it to verify the API server. Without it, curl cannot trust the certificate of the "
        "API server, so curl stops before it sends the HTTP request.",
 "mis": ["The token proves who the Pod is. curl must also trust the server, and for this it"
         " needs ca.crt.",
         "ca.crt is no credential. curl uses it to verify the API server.",
         "curl never changes HTTPS to plain HTTP. It stops when it cannot trust the server."]},

{"t": "service call",
 "q": "The Pod curl-sa in the namespace week13 runs as the ServiceAccount clo835. After the"
      " Pod starts, you create in week13 the Role service-reader and the RoleBinding "
      "service-reader-binding. The Role gives get and list on Services, and the RoleBinding"
      " binds it to clo835. The namespace week13 has no Service. The Pod sends GET "
      "https://kubernetes.default.svc/api/v1/namespaces/week13/services with curl and the "
      "token of clo835. What does the API server return?",
 "a": ['A ServiceList with "items": [], because week13 has no Service',
       'The text "No resources found in week13 namespace."',
       'A Status with "code": 404, because week13 has no Service',
       'A Status with "code": 403, because curl-sa must restart to get the new permissions'],
 "why": "The Role service-reader lets clo835 list Services. The API server returns a "
        "ServiceList, and its items list is empty, because week13 has no Service.",
 "mis": ["No resources found is a message of kubectl. The API server returns JSON.",
         "A list request returns a list, also an empty one. 404 is the answer for one "
         "object that does not exist.",
         "RBAC checks each request again. The new RoleBinding works for the next request, "
         "with the same token."]},

{"t": "persistentvolume access",
 "q": "The ClusterRole pv-reader gives get and list on PersistentVolumes. kubectl "
      "api-resources shows NAMESPACED false for the kind PersistentVolume. Which binding "
      "lets the ServiceAccount clo835 of the namespace week13 list the PersistentVolumes of"
      " the cluster?",
 "a": ["A ClusterRoleBinding that binds pv-reader to clo835",
       "A RoleBinding in week13 that binds pv-reader to clo835",
       "A ClusterRoleBinding that binds a Role with a rule for PersistentVolumes to clo835",
       "A RoleBinding in week13 that binds a Role with a rule for PersistentVolumes to clo835"],
 "why": "A PersistentVolume has no namespace. A RoleBinding gives its rules only in its own"
        " namespace, so only a ClusterRoleBinding to a ClusterRole gives access to "
        "PersistentVolumes.",
 "mis": ["A RoleBinding gives its rules only in its own namespace, and a PersistentVolume "
         "is in no namespace, so kubectl auth can-i shows no.",
         "A ClusterRoleBinding can name only a ClusterRole. The API server rejects a "
         "roleRef to a Role.",
         "A Role works in one namespace only, and a PersistentVolume is in no namespace, so"
         " this Role gives no access to it."]},

]
