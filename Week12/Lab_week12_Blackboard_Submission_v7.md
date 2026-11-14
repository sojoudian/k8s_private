# Lab Week 12: ConfigMaps and Secrets

## Submission Instructions

Submit a report demonstrating your completion and understanding of all 7 sections of Lab Week 12.

The lab recording demonstrates the steps required to complete this assignment. You may follow the recording step by step. However, your submission must include your own screenshots, actual command outputs, and explanations for all required tasks.

## 1. Build the Cluster and Verify Its Status

The Week 12 Terraform configuration builds three Ubuntu 26.04 EC2 instances, as in Weeks 04 to 10: one master node and two worker nodes. kubeadm forms the Kubernetes cluster at boot.

You must:

- Update the repo with git fetch and git reset --hard origin/master.
- Run terraform init and terraform apply.
- Run terraform output public_ips and terraform output private_ips, and show the addresses of all three nodes.
- Show an SSH session connected to the master node.
- Run kubectl get nodes -o wide and show all three nodes in the Ready state.
- Run kubectl get pods -n kube-system and show the control-plane Pods in the Running state.

## 2. Replace the CMD of an Image

The args field of a container replaces the CMD of its image. The command field replaces the ENTRYPOINT. Copy the commands of each step from localMachine.sh. Run them on the master node.

You must:

- Create the week12 namespace.
- Create fortune-args.yaml and display its contents.
- Apply the manifest.
- Run kubectl wait, and show that the fortune-args Pod is Ready.
- Run kubectl logs fortune-args -n week12 | head -4, and show the interval of 2 seconds.
- Explain why you do not put configuration data in a container image.
- Explain which Docker instruction the command field replaces, and which instruction the args field replaces.

## 3. Use a ConfigMap as Environment Variables

The values stay in a ConfigMap, not in the Pod manifest.

You must:

- Create the LOG_LEVEL file.
- Create the app-config ConfigMap with --from-literal and --from-file.
- Create config-env.yaml and display its contents.
- Apply the manifest.
- Run kubectl wait, and show that the config-env Pod is Ready.
- Run the printenv command for GREETING, COLOR, APP_COLOR, APP_MODE, LOG_LEVEL and KUBERNETES_SERVICE_HOST, and show the values.
- Explain the difference between --from-literal and --from-file.
- Explain the difference between env, configMapKeyRef and envFrom.

## 4. Use a ConfigMap as a Volume

Each key of a ConfigMap becomes a file in the volume.

You must:

- Create config-volume.yaml and display its contents.
- Apply the manifest.
- Run kubectl wait, and show that the config-volume Pod is Ready.
- Run the ls and cat commands on /etc/app-config, and show the value of APP_COLOR.
- Change APP_COLOR to green with kubectl patch.
- Run the until loop, and show the new value green in the file.
- Show that APP_COLOR in the config-env Pod is still blue.
- Explain why the file changes and the environment variable does not change.

## 5. Use a Secret, and Find the ServiceAccount Token

Kubernetes injects the data of a Secret into a container as an environment variable or as a file. Each Pod also gets a ServiceAccount token. The last two Explain items ask about lecture topics that the lab does not run.

You must:

- Create the DB_Password file.
- Create the app-secret Secret with --from-literal and --from-file.
- Read DB_Password with the jsonpath command and base64 -d.
- Create secret-pod.yaml and display its contents.
- Apply the manifest.
- Run kubectl wait, and show that the secret-pod Pod is Ready.
- Show DB_Password and DB_Host as environment variables, and DB_Host as a file.
- Run the mount command, and show that the Secret volume is tmpfs.
- Run the ls command on /var/run/secrets/kubernetes.io/serviceaccount and show the three files.
- Run kubectl get secrets -n week12 and show that no Secret holds the token.
- Explain the difference between secretKeyRef and secretRef.
- Explain why base64 is not encryption.
- Explain what tmpfs protects, and what it does not protect.
- Explain which permissions the default ServiceAccount has.
- Explain why an environment variable is not the recommended method for a Secret.

## 6. Use a Second Environment, and Read a Secret from etcd

The same Pod manifest gets other values in another namespace. By default, etcd stores a Secret as plain bytes.

You must:

- Create config-dev.yaml and display its contents.
- Apply the manifest with kubectl apply -f config-dev.yaml.
- Apply config-env.yaml in the week12-dev namespace.
- Run kubectl wait, and show that the Pod is Ready.
- Run the printenv command in week12-dev, and show red and dev.
- Store the etcdctl command and its certificate flags, as the lab shows.
- Run the etcdctl get command for the Secret of week12-dev, and show dev-pass in the output.
- Explain why config-dev.yaml holds a base64 value in the data field of the Secret.
- Explain how the same Pod manifest gets other values in the second namespace.
- Explain two methods that protect a Secret.

## 7. Destroy the Cluster

At the end of the lab, destroy all three EC2 instances. This also deletes every Kubernetes object and every file of the lab.

You must:

- Run terraform destroy in the Week12 directory on your own machine.
- Include the final Terraform output, which shows the message Destroy complete!
- State the number of resources Terraform destroyed.

## Submission Requirements

Your report must include all of the following:

- Your name clearly visible in every screenshot.
- Screenshots demonstrating the required commands and results in all 7 sections.
- Actual output from the commands you executed.
- Clear, detailed explanations of the commands, their purpose, and the results.
- Highlighted or clearly visible output where appropriate.
- Answers to every explanation question specified in the lab.

Important: Use your own screenshots and outputs from your lab environment. Screenshots or outputs copied from the recording or another student's submission do not demonstrate your own work.
