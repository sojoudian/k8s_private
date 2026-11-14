# Lab Week 12: ConfigMaps and Secrets

## Submission Instructions

Submit a report demonstrating your completion and understanding of all 7 sections of Lab Week 12.

The lab recording demonstrates the steps required to complete this assignment. You may follow the recording step by step. However, your submission must include your own screenshots, actual command outputs, and explanations for all required tasks.

## 1. Build the Cluster and Verify Its Status

The Week 12 Terraform configuration creates three Ubuntu 26.04 EC2 instances, as in Weeks 04 to 10: one control-plane node and two worker nodes. The Kubernetes cluster initializes automatically at boot.

You must:

- Run terraform init and terraform apply.
- Run terraform output public_ips and terraform output private_ips, and show the addresses of all three nodes.
- Show an SSH session connected to the control-plane node.
- Run kubectl get nodes -o wide and show all three nodes in the Ready state.
- Run kubectl get pods -n kube-system and show the control-plane pods in the Running state.
- Explain why you do not put configuration data in a container image.

## 2. Replace the CMD of an Image

The args field of a Pod replaces the CMD of the image. The command field replaces the ENTRYPOINT. Use localMachine.sh to run all the steps of this lab.

You must:

- Create the week12 namespace.
- Create fortune-args.yaml and display its contents.
- Apply the manifest and wait until the fortune-args Pod is Ready.
- Run kubectl logs fortune-args -n week12 --tail=4 and show the fortunes.
- Explain the difference between ENTRYPOINT and command, and between CMD and args.

## 3. Use a ConfigMap as Environment Variables

A ConfigMap keeps the values out of the Pod manifest.

You must:

- Create the app-config ConfigMap with the --from-literal options.
- Create app.properties, then create the app-file ConfigMap with --from-file, and show the result.
- Create config-env.yaml and display its contents.
- Apply the manifest and wait until the config-env Pod is Ready.
- Run the printenv command for GREETING, COLOR, APP_COLOR and APP_MODE, and show the values.
- Explain the difference between --from-literal and --from-file.
- Explain the difference between env, configMapKeyRef and envFrom.

## 4. Use a ConfigMap as a Volume

Each key of a ConfigMap becomes a file in the mounted folder.

You must:

- Create config-volume.yaml and display its contents.
- Apply the manifest and wait until the config-volume Pod is Ready.
- Run the ls and cat commands on /etc/app-config, and show the value of APP_COLOR.
- Change APP_COLOR to green using kubectl patch.
- Wait 90 seconds, then show the new value in the file.
- Show that APP_COLOR in the config-env Pod is still blue.
- Explain why the file changes and the environment variable does not change.

## 5. Use a Secret, and Find the ServiceAccount Token

A Secret gives sensitive data to a container as a variable or as a file. Each Pod also gets a ServiceAccount token.

You must:

- Create the DB_Password file, then create the app-secret Secret with --from-literal and --from-file.
- Read DB_Password with the jsonpath command and base64 -d.
- Create secret-pod.yaml and display its contents.
- Apply the manifest and wait until the secret-pod Pod is Ready.
- Show DB_Password and DB_Host as variables, and DB_Host as a file.
- Run the mount command, and show that the Secret volume is tmpfs.
- Run the ls command on /var/run/secrets/kubernetes.io/serviceaccount and show the 3 files.
- Run kubectl get secrets -n week12 and show that no Secret holds the token.
- Explain the difference between secretKeyRef and secretRef.
- Explain why base64 is not encryption.
- Explain what tmpfs protects, and what it does not protect.
- Explain which permissions the default ServiceAccount has.

## 6. Use a Second Environment, and Read a Secret from etcd

The same Pod manifest gets other values in another namespace. By default, etcd stores a Secret as plain bytes.

You must:

- Create config-dev.yaml and display its contents.
- Apply the manifest using kubectl apply -f config-dev.yaml.
- Apply config-env.yaml in the week12-dev namespace and wait until the Pod is Ready.
- Run the printenv command in week12-dev, and show red and dev.
- Read DB_Password of the Secret in week12-dev.
- Set the ETCD variable, as the lab shows.
- Run the etcdctl get command for the Secret, and show paswrd in the output.
- Explain why config-dev.yaml holds a base64 value in the data field of the Secret.
- Explain how the same Pod manifest gets different values in the two namespaces.
- Explain two ways to protect a Secret.

## 7. Clean Up and Destroy the Cluster

At the end of the lab, remove the Kubernetes objects and destroy all three EC2 instances.

You must:

- Run bash cleanup_lab12.sh on the control-plane node.
- Run kubectl get namespaces | grep week12 and show that nothing is left.
- From the Week 12 directory on your own machine, run terraform destroy.
- Include the final Terraform output showing Destroy complete!.
- State the number of resources Terraform removed.
- Explain why the deletion of a namespace removes the Pods, ConfigMaps and Secrets in it.

## Submission Requirements

Your report must include all of the following:

- Your name clearly visible in every screenshot.
- Screenshots demonstrating the required commands and results in all 7 sections.
- Actual output from the commands you executed.
- Clear, detailed explanations of the commands, their purpose, and the results.
- Highlighted or clearly visible output where appropriate.
- Answers to every explanation question specified in the lab.

Important: Use your own screenshots and outputs from your lab environment. Screenshots or outputs copied from the recording or another student's submission do not demonstrate your own work.
