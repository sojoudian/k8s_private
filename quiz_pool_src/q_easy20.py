# -*- coding: utf-8 -*-
"""CLO835 - 20 easy questions from the Docker Introduction and the Docker
Image Management lectures.

Each record holds:
  t    the topic
  q    the stem
  a    the four options; the first one is correct
  why  the feedback for the correct option
  mis  the mistake that each wrong option shows, in the order of a[1:]
"""

QUESTIONS = [
# ------------------------------------------------------------ containers
{"t": "containers",
 "q": "You run three containers on one Linux host. How many operating system "
      "kernels do these containers use?",
 "a": ["One kernel, the kernel of the host",
       "Three kernels, one for each container",
       "Four kernels, one for the host and one for each container",
       "Two kernels, one for the host and one for all the containers"],
 "why": "Containers are processes on the host. They share the host kernel.",
 "mis": ["It treats a container like a virtual machine, which carries its own kernel.",
         "It adds a kernel for the host and one for each container.",
         "It believes that the containers get a second, separate kernel."]},

{"t": "containers",
 "q": "A container must use no more than 1 GB of memory. Which Linux kernel "
      "feature applies that limit?",
 "a": ["Control groups",
       "Namespaces",
       "The seccomp filter",
       "The union file system"],
 "why": "Control groups (cgroups) measure and limit CPU, memory, block input "
        "and output, and network use.",
 "mis": ["Namespaces hide resources from the container; they do not limit the amount.",
         "The seccomp filter blocks system calls; it does not limit memory.",
         "The union file system stacks the image layers; it does not limit memory."]},

# ------------------------------------------------------------ images
{"t": "images",
 "q": "You start two containers from the same image. What does each container get?",
 "a": ["Its own read-write layer above the image files",
       "A read-only view with no place to write",
       "A shared read-write layer for both",
       "A full copy of the image files"],
 "why": "The image stays read-only. Each container adds its own read-write "
        "layer, so one container cannot change the files of the other.",
 "mis": ["A container can write; the write goes to its own layer.",
         "The containers do not share one read-write layer.",
         "Docker uses copy-on-write, so it does not copy the full image."]},

{"t": "images",
 "q": "Which command creates a container from the image nginx and starts it?",
 "a": ["docker run nginx",
       "docker start nginx",
       "docker build nginx",
       "docker create nginx"],
 "why": "The run command creates the container and starts it in one step.",
 "mis": ["The start command starts a container that already exists.",
         "The build command makes an image; it does not start a container.",
         "The create command makes the container but leaves it stopped."]},

{"t": "images",
 "q": "You install a package inside a running container. What happens to the "
      "image that started the container?",
 "a": ["The image does not change",
       "The image gets a new layer with the package",
       "The image is built again from its Dockerfile",
       "The image takes the package when the container stops"],
 "why": "An image is immutable. The new files stay in the read-write layer of "
        "the container. A new image needs a new build or a commit.",
 "mis": ["A running container does not add a layer to its image.",
         "Docker does not start a build when you work inside a container.",
         "The container layer disappears with the container; the image stays the same."]},

{"t": "images",
 "q": "An image has the name maziar/kubia. What does the part before the "
      "slash name?",
 "a": ["The user or the organization that owns the image",
       "The registry host that stores the image",
       "The version tag of the image",
       "The base image of the build"],
 "why": "A Docker Hub name has the form user/image. An official image, for "
        "example ubuntu, has no user part.",
 "mis": ["The registry host carries a dot or a port number, for example registry.example.net:5000.",
         "The tag comes after a colon, for example maziar/kubia:0.1.",
         "The name does not show the base image."]},

# ------------------------------------------------------------ dockerfile
{"t": "dockerfile",
 "q": "A Dockerfile starts with the line RUN apt-get update, and the FROM "
      "line comes after it. What happens when you build the image?",
 "a": ["The build fails, because FROM must come before RUN",
       "The build works, because Docker sorts the instructions",
       "The build works, and Docker takes ubuntu as the parent",
       "The build works, but the image keeps no name"],
 "why": "A build needs a parent image before it can run an instruction. Only "
        "a comment, a parser directive or an ARG line may come before FROM.",
 "mis": ["Docker runs the instructions in the order of the file.",
         "Docker picks no parent image for you.",
         "A missing name is a different problem; here the build stops."]},

{"t": "dockerfile",
 "q": "You change only the last line of a Dockerfile, then you build the image "
      "again. What does the builder do with the earlier instructions?",
 "a": ["It takes their layers from the cache",
       "It removes their layers and builds them again",
       "It runs only the instructions that install packages",
       "It runs them again, because every build starts clean"],
 "why": "The builder re-uses a cached layer while the instruction and its "
        "files stay the same. The cache stops at the first change.",
 "mis": ["The builder keeps the layers of the earlier builds.",
         "The cache works for every instruction, not only for package installs.",
         "A build does not start clean; it uses the layer cache."]},

{"t": "dockerfile",
 "q": "Which line uses the exec form of the RUN instruction?",
 "a": ['RUN ["apt-get", "update"]',
       "RUN apt-get update",
       "RUN exec apt-get update",
       "RUN /bin/sh -c apt-get update"],
 "why": "The exec form is a JSON array. It starts the program directly, so no "
        "shell expands the string.",
 "mis": ["This is the shell form; it runs the command through /bin/sh -c.",
         "The word exec is not part of the two RUN forms.",
         "This line writes the shell call by hand, so it is still the shell form."]},

{"t": "dockerfile",
 "q": "A Dockerfile sits in the current folder. Which command builds an image "
      "with the name webapp?",
 "a": ["docker build -t webapp .",
       "docker build webapp .",
       "docker build --name webapp .",
       "docker create -t webapp ."],
 "why": "The -t option gives the name and the tag. The dot gives the build "
        "context, which is the current folder.",
 "mis": ["Without -t, Docker reads webapp as the build context.",
         "The build command has no --name option.",
         "The create command makes a container, not an image."]},

{"t": "dockerfile",
 "q": "Which first line starts an image that has no parent image?",
 "a": ["FROM scratch",
       "FROM base",
       "FROM none",
       "FROM ubuntu:latest"],
 "why": "The name scratch is an empty, reserved image. A base image starts "
        "from it and adds the first file system.",
 "mis": ["There is no reserved image with the name base.",
         "There is no reserved image with the name none.",
         "The image ubuntu is a parent image; it already holds a file system."]},

# ------------------------------------------------------------ ports
{"t": "ports",
 "q": "A Dockerfile declares EXPOSE 80. You start the container with the "
      "command docker run myimage. Can a user on another machine reach port 80?",
 "a": ["No, because EXPOSE alone does not publish the port",
       "No, because port 80 needs the host network driver",
       "Yes, but only after the container restarts",
       "Yes, because EXPOSE publishes the port"],
 "why": "EXPOSE is documentation for the image. A port becomes public with "
        "the -p option or with the -P option at run time.",
 "mis": ["The bridge driver also publishes a port with -p.",
         "A restart does not publish a port.",
         "EXPOSE declares a port; it does not open it on the host."]},

{"t": "ports",
 "q": "You start a container with the command docker run -p 8080:80 nginx. "
      "Which address does a browser on the host use?",
 "a": ["http://localhost:8080",
       "http://localhost:80",
       "http://localhost:8080:80",
       "http://172.17.0.2:80"],
 "why": "The first number is the host port, and the second number is the "
        "container port. The browser uses the host port.",
 "mis": ["Port 80 is the container port; the host listens on 8080.",
         "An address carries one port number.",
         "The private container address is not reachable from the host browser."]},

{"t": "ports",
 "q": "You start a container with the command docker run -P myimage. Which "
      "ports become public?",
 "a": ["Every port that the image declares with EXPOSE",
       "No port, because -P needs a port number",
       "Only port 80, the default web port",
       "Every port of the container"],
 "why": "The capital -P option publishes each declared port, and Docker picks "
        "a free host port for each one.",
 "mis": ["The capital -P option takes no port number.",
         "Docker does not prefer port 80.",
         "Docker publishes the declared ports only."]},

# ------------------------------------------------------------ cmd and entrypoint
{"t": "cmd",
 "q": "An image declares CMD sleep 20. You start it with the command "
      "docker run myimage sleep 60. Which command runs in the container?",
 "a": ["sleep 60",
       "sleep 20",
       "sleep 20, and then sleep 60",
       "No command, because the two commands conflict"],
 "why": "A command on the docker run line replaces the CMD instruction.",
 "mis": ["The CMD instruction gives the default only; the run line wins.",
         "Docker runs one command, not two.",
         "The two commands do not conflict; one replaces the other."]},

{"t": "cmd",
 "q": 'The image jobrunner declares ENTRYPOINT ["sleep"]. A student types '
      "docker run jobrunner 30. What runs inside the container?",
 "a": ["sleep 30",
       "sleep, with no parameter",
       "the program 30, which fails at once",
       "sleep and 30, as two separate programs"],
 "why": "Docker appends the arguments of the run line to the ENTRYPOINT.",
 "mis": ["The argument 30 reaches the entry point as a parameter.",
         "An ENTRYPOINT image does not read the argument as a program name.",
         "The entry point and the argument form one command line."]},

{"t": "cmd",
 "q": "A MySQL container needs the root password at start. Which part of the "
      "docker run command passes it?",
 "a": ["-e MYSQL_ROOT_PASSWORD=secret",
       "-v MYSQL_ROOT_PASSWORD=secret",
       "--password secret",
       "--name MYSQL_ROOT_PASSWORD=secret"],
 "why": "The -e option sets an environment variable, and the image reads the "
        "password from that variable.",
 "mis": ["The -v option mounts a volume.",
         "The docker run command has no --password option.",
         "The --name option names the container."]},

# ------------------------------------------------------------ registry
{"t": "registry",
 "q": "You run the command docker tag myapp:v1 myapp:latest. What happens to "
      "the tag v1?",
 "a": ["It stays, and the image carries two tags",
       "It is removed, because the image is renamed",
       "It points at an empty image",
       "It stays until the next build"],
 "why": "A tag is a pointer to an image. A new tag adds a second pointer to "
        "the same image.",
 "mis": ["The tag command adds a tag; it does not rename the image.",
         "Both tags point at the same image.",
         "A build does not remove a tag of another image."]},

{"t": "registry",
 "q": "You must push an image to a private registry at "
      "registry.example.net:5000. Where does that address belong?",
 "a": ["In the image tag, before the image name",
       "In a flag of the docker push command",
       "In the FROM line of the Dockerfile",
       "In the daemon configuration file"],
 "why": "The push command reads the destination from the tag, for example "
        "registry.example.net:5000/team/app:v1.",
 "mis": ["The push command takes the name only; it has no registry flag.",
         "The FROM line names the parent image, not the destination.",
         "The daemon configuration does not set the destination of a push."]},

# ------------------------------------------------------------ networking
{"t": "networking",
 "q": "You start a container and you give no network option. Which network "
      "driver does the container use?",
 "a": ["The bridge driver",
       "The host driver",
       "The null driver",
       "The overlay driver"],
 "why": "Docker connects a new container to the default bridge network, and "
        "the container gets a private address.",
 "mis": ["The host driver needs --net host.",
         "The null driver leaves the container with no network.",
         "The overlay driver works across more than one host, and you must create it."]},
]
