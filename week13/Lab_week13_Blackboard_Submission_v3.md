# Lab Week 13: Authentication and RBAC

## Submission Instructions

Submit a report demonstrating your completion and understanding of all 7 sections of Lab Week 13.

The lab recording demonstrates the steps required to complete this assignment. You may follow the recording step by step. However, your submission must include your own screenshots, actual command outputs, and explanations for all required tasks.

## 1. Build the Cluster and Verify Its Status

The Week 13 Terraform configuration creates three Ubuntu 26.04 EC2 instances, as in Weeks 04 to 12: one master node and two worker nodes. The Kubernetes cluster initializes automatically at boot.

You must:

- Run terraform init and terraform apply.
- Run terraform output public_ips and terraform output private_ips, and show the addresses of all three nodes.
- Show an SSH session connected to the master node.
- Run kubectl get nodes -o wide and show all three nodes in the Ready state.
- Run kubectl get pods -n kube-system and show the control-plane Pods in the Running state.
- Explain the order of the three phases of a request in the API server.

## 2. Create a User with a Signed Certificate

Kubernetes stores no users. The cluster CA signs a certificate, and the certificate names the user and the group. Copy the commands of each step from localMachine.sh, and run them on the master node.

You must:

- Create dev-user.key and dev-user.csr using the openssl commands.
- Create dev-user-csr.yaml and show its contents.
- Apply the manifest and approve the dev-user request.
- Run kubectl get csr dev-user and show Approved,Issued.
- Write the certificate to dev-user.crt.
- Run the openssl x509 command, and show the subject and the end date.
- Explain why Kubernetes does not store users.
- Explain what the CN and O fields of the certificate mean.

## 3. Authenticate with No Authorization

Authentication proves who you are. Authorization decides what you can do.

You must:

- Create the week13 namespace.
- Add the dev-user credentials and the dev-user@kubernetes context to the kubeconfig file.
- Run the two curl commands on port 6443, and show the version and the 403 Forbidden answer.
- Run the kubectl proxy command, and show the first lines of the APIGroupList.
- Run kubectl --context=dev-user@kubernetes auth whoami, and show the user and the group.
- Run kubectl --context=dev-user@kubernetes get pods, and show the Forbidden error.
- Explain the difference between authentication and authorization.
- Explain why the curl command gets 403 Forbidden and the kubectl proxy request passes.
- Explain why the auth whoami command passes and the get pods command fails.

## 4. Create a Role, a RoleBinding and a Binding for a Group

The Role says what. The RoleBinding says who.

You must:

- Create developer-role.yaml and show its contents.
- Apply the manifest using kubectl apply -f developer-role.yaml -n week13.
- As dev-user, create the web Pod.
- As dev-user, try to delete the web Pod, and show the Forbidden error.
- Create the developers-view RoleBinding using the kubectl create rolebinding command.
- As dev-user, run the get services command, and show that no Forbidden error comes back.
- Explain the difference between a Role and a RoleBinding.
- Explain why the Role names configmaps and not ConfigMap.
- Explain how dev-user gets the permissions of the default ClusterRole view.

## 5. Call the API from a Pod

A Pod runs as a ServiceAccount, and Kubernetes mounts its token in the Pod.

You must:

- Create the clo835 ServiceAccount.
- Create curl-sa.yaml and show its contents.
- Apply the manifest and wait until the curl-sa Pod is Ready.
- Run the curl command in the Pod, and show the Forbidden answer.
- Explain how the Pod proves its identity to the API server.
- Explain why the API server answers Forbidden.

## 6. Grant Access to the ServiceAccount

A Role and its RoleBinding work in one namespace. A cluster-level resource needs a ClusterRole and a ClusterRoleBinding.

You must:

- Create service-reader.yaml and show its contents.
- Apply the manifest using kubectl apply -f service-reader.yaml -n week13.
- Run the same curl command, and show the ServiceList.
- Run kubectl auth can-i list services for the default namespace, and show no.
- Run the kubectl api-resources command, and show that NAMESPACED is false for persistentvolumes.
- Create the pv-reader ClusterRole.
- Create the pv-test RoleBinding, run kubectl auth can-i list persistentvolumes, and show no.
- Create the pv-test ClusterRoleBinding, run the same command, and show yes.
- Explain why the ServiceAccount gets the answer no in the default namespace.
- Explain why a PersistentVolume needs a ClusterRoleBinding and not a RoleBinding.

## 7. Clean Up and Destroy the Cluster

At the end of the lab, delete the Kubernetes objects and destroy all three EC2 instances.

You must:

- Run bash cleanup_lab13.sh on the master node, and show that only the kubernetes-admin context is left.
- From the Week13 folder on your own machine, run terraform destroy.
- Include the final Terraform output showing Destroy complete!.
- State the number of resources Terraform destroyed.
- Explain why the deletion of the week13 namespace does not delete the CSR, the ClusterRole and the ClusterRoleBinding.

## Submission Requirements

Your report must include all of the following:

- Your name clearly visible in every screenshot.
- Screenshots demonstrating the required commands and results in all 7 sections.
- Actual output from the commands you executed.
- Clear, detailed explanations of the commands, their purpose, and the results.
- Highlighted or clearly visible output where appropriate.
- Answers to every explanation question specified in the lab.

Important: Use your own screenshots and outputs from your lab environment. Screenshots or outputs copied from the recording or another student's submission do not demonstrate your own work.
