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
The lecture questions use only the core facts that lectures v9 and v10 keep: the request path,
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

v2 (2026-11-18, the Week 13 v10 loop, report 2026-11-18-08). v1 stays on disk. Lecture v10 teaches the
same facts as lecture v9. The findings of the phase 1 audit and their fixes:
- Q1 (D3), Q11: the stem said "Nobody approves or denies it", so it removed the option Denied. The stem now
  says "You run no other command, and no other user works on the cluster."
- Q2 (D3), Q12: the field name expirationSeconds removed "86400 hours" and "86400 days". The new wrong
  options are "Until an administrator deletes the CSR dev-user" and "With no limit, because Kubernetes
  cannot revoke a certificate".
- Q3 (D2): each short form has its long form at its first use in the question: RBAC (Q4, Q7, Q8, Q15,
  Q16), CN (Q2), IAM and CLI (Q10). Q8 and Q10 name no RBAC in an option now; Q18 has no TLS, HTTPS or
  HTTP; Q19 has no JSON and no RBAC in its feedback. EKS stays, as in the Week 09 quiz.
Phase 4 finding P1 (D6): the signer starts a certificate 5 minutes before the signature, so the Q12 feedback
says "is valid for 24 hours", not "expires 24 hours after the signature".
Review round 1 of the loop (scratchpad w13review_r1/quiz.md: 5 MUST-FIX, 7 SHOULD-FIX), all applied:
- Q-M1 = P1 (Q12). Q-M2 (Q9): "only" in the two one-group options. Q-M3 (Q13): "Only the content of ...".
- Q-M4: Q5 (the scope of a RoleBinding) tested the fact of Q20, so Q5 is now the question "edit role". Its
  scenario needs a live probe (D5).
- Q-M5: the form "with no" was in 4 wrong options and in no key: Q9, Q12 and Q18 have new wrong options.
- Q-S1 (Q8): the ClusterRole cluster-admin stays; a new wrong option in place of super-admin.conf.
- Q-S2 (Q9): the stem defines CN and O. Q-S3 (Q10): two wrong options also say "access".
- Q-S4, Q-S5 (Q11), Q-S6 (Q6), Q-S7 (Q10): the feedback texts.
Review round 2 (scratchpad w13review_r2/quiz.md: 1 MUST-FIX, 5 SHOULD-FIX), all applied:
- Q-M1: Q15 "role verbs" is a new record: dev-user creates the Pod web, then deletes it (the lab names).
- Q-S1 (Q3): a new option D. Q-S2 (Q10): the key "An access entry that names ci-deployer". Q-S3 (Q14,
  Q19): the stems name the token, not curl. Q-S4 (Q11): "kube-controller-manager never approves/denies".
- Q-S5 (Q16): the probe with dev-user and its context is for the next live cluster.
- With the lecture finding L-M1: the Q2 WHY says "Kubernetes stores no normal users". The Q19 WHY says
  "allows", the one word of the course for a permission (A1).
Review round 3 (scratchpad w13review_r3/quiz.md: 1 MUST-FIX, 3 SHOULD-FIX), all applied:
- Q-M1 (Q9): each option has a reason, so the key is not the only option of its form (D3).
- Q-S1 (Q10): the IAM role eks-admin creates the cluster, so IF A is also true for the creator (D2, D6).
- Q-S2 (Q12) and Q-S3 (Q2): the stems say "with the default settings"; the Q12 WHY names the maximum of
  the signer (1 year by default).
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
 "q": "On the master node of a kubeadm cluster with the default settings, the kubeconfig file holds the users "
      "kubernetes-admin and dev-user. The certificate authority (CA) of the cluster signed "
      "the certificate of dev-user after kubectl certificate approve dev-user. You run "
      "kubectl get users. What does the command show?",
 "a": ["An error, because the API server has no type users",
       "kubernetes-admin and dev-user, the users of the kubeconfig file",
       "dev-user, because kubectl certificate approve creates a User object",
       "No resources found"],
 "why": "Kubernetes stores no normal users. The API server has no User object and no type users, "
        "so kubectl get users fails. It shows the error: the server doesn't have a resource"
        ' type "users". A user is only a name in a credential, for example the common name (CN) of a '
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
       "A PodList of default, because every client gets read access to default"],
 "fix": ["401 Unauthorized, because the request has no credentials",
         "403 Forbidden for the user system:anonymous",
         "403 Forbidden for the user system:unauthenticated",
         "A PodList of default, because every client gets read access to default"],
 "why": "Anonymous authentication is active by default. The API server gives a request with"
        " no credentials the user system:anonymous and the group system:unauthenticated. No"
        " authorizer allows this user to list Pods, so the API server returns 403 "
        "Forbidden.",
 "mis": ["401 is the answer for credentials that the API server rejects. A request with no "
         "credentials becomes the user system:anonymous, and the API server returns 403, "
         "because no authorizer allows the request.",
         "system:unauthenticated is the group of an anonymous request. The message names "
         "the user, system:anonymous.",
         "A namespace gives no access by itself. Only an authorizer allows a request, and no "
         "authorizer allows system:anonymous to list Pods."]},

{"t": "authorization order",
 "q": "The API server runs with --authorization-mode=Node,RBAC,Webhook. RBAC means "
      "role-based access control. A RoleBinding in "
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

{"t": "edit role",
 "q": "A RoleBinding in the namespace dev binds the default ClusterRole edit to the user ben. "
      "ben has no other permission in dev. The namespace dev also has the Deployment web and "
      "the Secret db. Which command of ben gets the answer Forbidden?",
 "a": ["kubectl get rolebindings -n dev",
       "kubectl get secrets -n dev",
       "kubectl delete deployment web -n dev",
       "kubectl scale deployment web --replicas=3 -n dev"],
 "fix": ["kubectl delete deployment web -n dev",
         "kubectl get rolebindings -n dev",
         "kubectl get secrets -n dev",
         "kubectl scale deployment web --replicas=3 -n dev"],
 "why": "The ClusterRole edit gives read and write access to most objects of a namespace, also "
        "to Secrets, but no access to Roles or RoleBindings. So ben cannot list the "
        "RoleBindings of dev.",
 "mis": ["edit can read and change the Secrets of dev. Of these objects, edit excludes only "
         "RoleBindings.",
         "edit can delete the Deployments of dev. Of these objects, edit excludes only "
         "RoleBindings.",
         "edit can scale the Deployments of dev. Of these objects, edit excludes only "
         "RoleBindings."]},

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
        "Secrets can give more permissions.",
 "mis": ["view can read the ConfigMaps of qa. Of these four types, view excludes only "
         "Secrets.",
         "view can read the Deployments of qa. Of these four types, view excludes only "
         "Secrets.",
         "view can read the Pods of qa. Of these four types, view excludes only Secrets."]},

{"t": "two bindings",
 "q": "The cluster uses role-based access control (RBAC). In the namespace dev, the "
      "RoleBinding admin-binding binds the Role pod-admin to the "
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
      "the ClusterRoleBinding cluster-admin, and the ClusterRole cluster-admin stays. Now no binding names ops-lead or "
      "system:masters. The node workernode2 exists, and ops-lead runs kubectl delete node "
      "workernode2. What is the result, and why?",
 "a": ["Deleted, because the group system:masters bypasses each check of the authorization modes",
       "Deleted, because the ClusterRole cluster-admin still allows each request",
       "NotFound for workernode2, because ops-lead can see no node without a binding",
       "Forbidden, because no binding now allows a request of the group system:masters"],
 "why": "The group system:masters bypasses all authorization checks, also role-based "
        "access control (RBAC) and Webhook."
        " No binding can limit this access, so the API server deletes the node.",
 "mis": ["A ClusterRole alone allows nothing, because only a binding gives its rules to a "
         "subject. The API server deletes the node because system:masters bypasses "
         "authorization.",
         "The request passes authorization, and the node exists, so the API server deletes "
         "it.",
         "The group system:masters needs no binding. It has full access, also when no binding "
         "names it."]},

{"t": "certificate subject",
 "q": "The certificate authority (CA) of the cluster signs a client certificate with the "
      "subject /CN=kim/O=ops/O=audit. The subject has one common name (CN) field and two "
      "organization (O) fields. No object with the name ops or audit exists in the "
      "cluster. Which user name and which groups does the API server get from this "
      "certificate?",
 "a": ["The user kim in the groups ops and audit, from the O fields",
       "The user kim in the group ops only, from the first O field of the subject",
       "The user kim in the group audit only, from the last O field of the subject",
       "The user kim in no group, because each group must be an object"],
 "fix": ["The user kim in the group ops only, from the first O field of the subject",
         "The user kim in the group audit only, from the last O field of the subject",
         "The user kim in the groups ops and audit, from the O fields",
         "The user kim in no group, because each group must be an object"],
 "why": "The API server takes the user name from the common name (CN), and one group from "
        "each organization (O) field. A group is no object in the API server, so ops and "
        "audit need no object.",
 "mis": ["Each O field gives one group, so the second O field adds the group audit.",
         "Each O field gives one group, so the first O field also adds the group ops.",
         "A group is only a name in the certificate. The API server needs no object for it."]},

{"t": "eks identities",
 "q": "A team creates a new Amazon EKS cluster with the AWS Identity and Access Management (IAM) role "
      "eks-admin. The IAM role ci-deployer must also run kubectl commands on this cluster. Which method "
      "does AWS recommend for this?",
 "a": ["An access entry that names ci-deployer",
       "A mapRoles item in aws-auth that gives ci-deployer access",
       "A client certificate for ci-deployer that the EKS cluster signs",
       "A RoleBinding that gives ci-deployer access, with no other change"],
 "why": "AWS recommends the access entry. You manage each access entry with the EKS API, "
        "the AWS command line interface (CLI) or the AWS console. AWS marks the aws-auth ConfigMap as deprecated.",
 "mis": ["AWS marks the aws-auth ConfigMap as deprecated, and it recommends the access "
         "entry in its place.",
         "Amazon EKS authenticates an IAM role through AWS IAM, and an access entry maps it"
         " to Kubernetes. A client certificate is no IAM identity.",
         "A RoleBinding decides what a user can do. Without an access entry or an aws-auth item, the"
         " API server cannot map the IAM role to a Kubernetes user."]},

# ------------------------------------------------------------ the lab
{"t": "csr condition",
 "q": "You create the certificate signing request (CSR) qa-user with the signer "
      "kubernetes.io/kube-apiserver-client and the usage client auth. You run no other "
      "command, and no other user works on the cluster. Two minutes later, you run kubectl get csr qa-user. What does the "
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
 "mis": ["Approved,Issued comes only after an approval, for example with kubectl certificate "
         "approve. kube-controller-manager never approves a request for this signer.",
         "kube-controller-manager never denies this request. Denied comes only after a denial, for example with "
         "kubectl certificate deny.",
         "Failed means that the signer cannot sign an approved request because of a permanent "
         "error. Nobody approved this request."]},

{"t": "certificate lifetime",
 "q": "A kubeadm cluster runs with the default settings. The file dev-user-csr.yaml sets "
      "expirationSeconds: 86400 in the certificate signing "
      "request (CSR) dev-user. You apply it, and you run kubectl certificate approve "
      "dev-user. How long is the signed certificate of dev-user valid?",
 "a": ["24 hours",
       "1 year",
       "Until an administrator deletes the CSR dev-user",
       "For an unlimited time, because Kubernetes cannot revoke a certificate"],
 "fix": ["24 hours",
         "1 year",
         "Until an administrator deletes the CSR dev-user",
         "For an unlimited time, because Kubernetes cannot revoke a certificate"],
 "why": "expirationSeconds gives the lifetime in seconds. 86400 seconds are 24 hours, less than "
        "the maximum of the signer, which is 1 year by default. So kubectl get csr shows "
        "REQUESTEDDURATION 24h, and the certificate is valid for 24 hours.",
 "mis": ["One year is the default lifetime of the signer, for a CSR with no "
         "expirationSeconds.",
         "A delete of the CSR changes nothing in the signed certificate. The certificate stays "
         "valid until its end date.",
         "Kubernetes cannot revoke a certificate, but each certificate has an end date. This "
         "certificate is valid for 24 hours."]},

{"t": "certificate request",
 "q": "You create dev-user.key with openssl genrsa, and dev-user.csr with openssl req and "
      "this key. The file dev-user-csr.yaml holds a certificate signing request (CSR) for "
      "dev-user, and kubectl apply sends it to the API server. Which data does the request "
      "field of this CSR hold?",
 "a": ["Only the content of dev-user.csr, as base64 text",
       "Only the content of dev-user.key, as base64 text",
       "The content of dev-user.key and dev-user.csr, as base64 text",
       "Only the subject of dev-user.csr, as base64 text"],
 "fix": ["Only the subject of dev-user.csr, as base64 text",
         "Only the content of dev-user.csr, as base64 text",
         "The content of dev-user.key and dev-user.csr, as base64 text",
         "Only the content of dev-user.key, as base64 text"],
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
      "week13 with the token of clo835. The API server returns 403 Forbidden. "
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
 "q": "In the namespace week13, the RoleBinding devuser-developer-binding binds the Role developer to dev-user. "
      "The Role gives list, get, create and update on Pods, and no other binding gives dev-user a permission "
      "on Pods. dev-user creates the Pod web with kubectl --context=dev-user@kubernetes run web "
      "--image=maziar/kubia:v1, and the Pod web runs. Then dev-user runs kubectl "
      "--context=dev-user@kubernetes delete pod web. What is the result, and why?",
 "a": ["Forbidden, because no rule of the Role has the verb delete",
       "Deleted, because the creator of the Pod web gets the verb delete",
       "Deleted, because the Role gives update, and update also gives a delete",
       "Forbidden, because a running Pod gets no delete"],
 "fix": ["Forbidden, because no rule of the Role has the verb delete",
         "Forbidden, because a running Pod gets no delete",
         "Deleted, because the creator of the Pod web gets the verb delete",
         "Deleted, because the Role gives update, and update also gives a delete"],
 "why": "Role-based access control (RBAC) allows only the verbs of the rules. No rule of the Role developer "
        "has the verb delete, so the API server rejects the delete of web with Forbidden.",
 "mis": ["RBAC gives no extra permission to the creator of an object. Only the rules of the bindings count.",
         "Each verb allows only its own action. update changes an object, and only the verb delete allows a "
         "delete.",
         "The API server can delete a running Pod, and the kubelet then stops its containers. Here no rule "
         "allows the delete, so the API server rejects the request first."]},

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
 "why": "Role-based access control (RBAC) matches the name in the API path: configmaps, in lowercase and in the plural."
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
       "The request works, because the token alone is enough for the connection",
       "The API server rejects the request, because it needs ca.crt to check the Pod",
       "curl sends the request as plain text, and anyone can read the token"],
 "why": "ca.crt holds the certificate of the cluster certificate authority (CA). curl uses "
        "it to verify the API server. Without it, curl cannot trust the certificate of the "
        "API server, so curl stops before it sends the request.",
 "mis": ["The token proves who the Pod is. curl must also trust the server, and for this it"
         " needs ca.crt.",
         "ca.crt is no credential. curl uses it to verify the API server.",
         "curl never sends a request to an https address with no encryption. It stops when it "
         "cannot trust the server."]},

{"t": "service call",
 "q": "The Pod curl-sa in the namespace week13 runs as the ServiceAccount clo835. After the"
      " Pod starts, you create in week13 the Role service-reader and the RoleBinding "
      "service-reader-binding. The Role gives get and list on Services, and the RoleBinding"
      " binds it to clo835. The namespace week13 has no Service. The Pod sends GET "
      "https://kubernetes.default.svc/api/v1/namespaces/week13/services with the token of "
      "clo835, and the request reaches the API server. What does the API server return?",
 "a": ['A ServiceList with "items": [], because week13 has no Service',
       'The text "No resources found in week13 namespace."',
       'A Status with "code": 404, because week13 has no Service',
       'A Status with "code": 403, because curl-sa must restart to get the new permissions'],
 "why": "The Role service-reader allows clo835 to list Services. The API server returns a "
        "ServiceList, and its items list is empty, because week13 has no Service.",
 "mis": ["No resources found is a message of kubectl. The API server returns a list object.",
         "A list request returns a list, also an empty one. 404 is the answer for one "
         "object that does not exist.",
         "The API server checks the permissions of each request again. The new RoleBinding works for the next request, "
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
