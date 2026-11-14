"""Lab01 — CLO835 Fall 2026 lab deck, built from the CLO835_Fall_2026/Week02 repo.

Modelled on finalWork/Lab01.pptx: a cover, a lab divider, a run of
bullets + dark-terminal pages, and a closing page.

Design language is REUSED, NOT COPIED: this module imports build_week12, the
proven house engine, so the palette, the fonts, the chrome, the terminal mockup,
the bullet glyphs and the coordinate guard are the SAME objects.

Every command on every slide is taken VERBATIM from the repo at
/Users/maziar/Documents/c/r/CLO835_Fall_2026/Week02:
  main.tf  variables.tf  bootstrap.sh  runAWS_EC2.sh  localMachine.sh  README.md

Run from a directory that holds whale.png and docker_logo.jpg. Sandbox only.
"""

import build_week12 as bw
from build_week12 import (
    Inches, Pt,
    BLUE, SLATE, BODY, MUTED, LIGHTBLUE, WHITE, CARD_BG, RULE_GRAY, FOOTER_GRAY,
    GOAL_GREEN, TERMBG,
    FONT_SANS, FONT_MONO, WHALE,
    CENTER, LEFT, RIGHT, MIDDLE, TOP,
    add_text, add_rect, add_rounded_rect, add_oval, add_line,
    title, bullets, auto_term, divider, whale_and_footer, _sanitize_coords,
)

VERSION     = "v1"
WEEK_LABEL  = "Week 2"
DECK_TITLE  = "CLO835 – Portable Technologies In Cloud"
DECK_SUB    = "Lab 1 — one EC2 machine, deployed by hand, then as a container"
DOCKER_LOGO = "docker_logo.jpg"
OUT         = f"Lab01_{VERSION}.pptx"


# ---------------------------------------------------------------- terminal fit
def _term_h(nlines, fs):
    return 0.5 + nlines * (fs * 1.52 / 72.0) + 0.22


def _eff_lines(g, w_in, fs):
    cpl = max(10, int(w_in * 72 / (fs * 0.60)))
    return sum(max(1, -(-len(l) // cpl)) for l in g)


def _fit_term(s, x, y, w, ymax, ttl, code, hi=13, lo=8):
    """Content-fit terminal: shrink the font only until the block clears ymax."""
    fs = hi
    while fs > lo and _term_h(_eff_lines(code, w, fs), fs) > (ymax - y):
        fs -= 1
    h = min(ymax - y, _term_h(_eff_lines(code, w, fs), fs))
    auto_term(s, x, y, w, h, ttl, code, font_size=fs)
    return h


# ---------------------------------------------------------------- cover
def render_cover(s, n, total):
    add_text(s, Inches(0.7), Inches(2.25), Inches(7.95), Inches(1.8),
             DECK_TITLE, size=34, bold=True, color=BLUE, line_spacing=1.10)
    add_text(s, Inches(0.72), Inches(4.28), Inches(7.9), Inches(0.6),
             f"{WEEK_LABEL} · Lab", size=22, color=SLATE)
    add_text(s, Inches(0.72), Inches(4.96), Inches(7.9), Inches(0.5),
             DECK_SUB, size=15, italic=True, color=MUTED)
    logo_cx = Inches(10.85); logo_cy = Inches(3.55); ring_r = Inches(1.70)
    add_oval(s, logo_cx - ring_r, logo_cy - ring_r, ring_r * 2, ring_r * 2, WHITE,
             line=LIGHTBLUE, line_width=1.5)
    s.shapes.add_picture(DOCKER_LOGO, logo_cx - Inches(1.3), logo_cy - Inches(1.02),
                         width=Inches(2.6), height=Inches(2.04))
    s.shapes.add_picture(WHALE, Inches(0.45), Inches(6.85), width=Inches(0.5), height=Inches(0.5))
    add_text(s, Inches(9.5), Inches(7.12), Inches(3.35), Inches(0.3),
             f"CLO835, Fall 2026     {n} / {total}", size=10, color=FOOTER_GRAY, align=RIGHT)


# ---------------------------------------------------------------- closing
def render_closing(s, n, total, text):
    add_oval(s, Inches(13.333 / 2) - Inches(0.8), Inches(2.2), Inches(1.6), Inches(1.6),
             WHITE, line=LIGHTBLUE, line_width=1.5)
    s.shapes.add_picture(DOCKER_LOGO, Inches(13.333 / 2) - Inches(0.62), Inches(2.62),
                         width=Inches(1.24), height=Inches(0.97))
    add_text(s, Inches(1.0), Inches(4.25), Inches(11.33), Inches(1.0), text,
             size=32, bold=True, color=BLUE, align=CENTER, line_spacing=1.05)
    whale_and_footer(s, n, total)


# ---------------------------------------------------------------- content
def render_content(s, n, total, d):
    body = [(b["level"], b["text"]) for b in d.get("body", [])]
    code = d.get("code_blocks", [])
    if d.get("title"):
        title(s, d["title"])
    if code and body:
        bullets(s, 1.66, body, x=0.60, w=6.05,
                size=d.get("bullet_size", 13.5), line_spacing=1.26, space_after=6)
        _fit_term(s, 7.05, 1.66, 5.75, 6.55, d.get("term_title", "bash  —  docker"),
                  code[0]["lines"], hi=d.get("term_fs", 13), lo=8)
    elif code:
        _fit_term(s, 0.90, 1.66, 11.50, 6.55, d.get("term_title", "bash  —  docker"),
                  code[0]["lines"], hi=d.get("term_fs", 14), lo=8)
    elif body:
        sz = d.get("bullet_size", 16 if len(body) <= 6 else 14)
        bullets(s, 1.72, body, x=0.60, w=12.15, size=sz,
                line_spacing=d.get("ls", 1.36), space_after=d.get("sa", 9))
    whale_and_footer(s, n, total)


def render_slide(s, n, total, d):
    st = d["slide_type"]
    if st == "cover":
        render_cover(s, n, total)
    elif st == "section_divider":
        divider(s, d["kicker"], d["title"], subtitle=d.get("subtitle"))
        whale_and_footer(s, n, total)
    elif st == "closing":
        render_closing(s, n, total, d["title"])
    else:
        render_content(s, n, total, d)


def build_deck(slides, out):
    prs = bw.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]
    total = len(slides)
    for i, d in enumerate(slides, 1):
        s = prs.slides.add_slide(blank)
        render_slide(s, i, total, d)
    _sanitize_coords(prs)
    prs.save(out)
    print(f"wrote {out}  ({total} slides)")


def _b(*items):
    return [{"level": lvl, "text": t} for lvl, t in items]


def _c(*lines):
    return [{"lines": list(lines)}]


# ============================================================================
# DECK — every command is VERBATIM from CLO835_Fall_2026/Week02.
# ============================================================================

DECK = [

 {"slide_type": "cover"},

 {"slide_type": "section_divider", "kicker": "LAB 1",
  "title": "Lab 1 – One Machine, Two Ways",
  "subtitle": "Deploy the same Flask app by hand, then as a container"},

 # ---- 3 what you build ----
 {"slide_type": "content", "title": "What You Build",
  "body": _b((0, "One Ubuntu 26.04 EC2 machine in the AWS Academy Learner Lab."),
             (0, "The machine has git and nothing else."),
             (1, "You install Python, Flask and the app by hand. Count the steps."),
             (0, "Then you build the same app as a container image on your laptop."),
             (1, "One build repeats every manual step, on any computer."),
             (0, "Finally you publish the image for two CPU types, and destroy the machine."),
             (0, "The repo holds two scripts. Run them section by section."),
             (1, "runAWS_EC2.sh on the EC2 machine."),
             (1, "localMachine.sh on your own laptop.")),
  "bullet_size": 15},

 # ---- 4 the machine ----
 {"slide_type": "content", "title": "The Machine Terraform Builds",
  "body": _b((0, "m5.large — 2 vCPU, 8 GB. The Learner Lab blocks xlarge and larger."),
             (0, "Ubuntu 26.04 LTS, because the Dockerfile says FROM ubuntu:26.04."),
             (0, "30 GB gp3 root disk."),
             (0, "A security group that opens port 22 and port 8080."),
             (0, "IMDSv2 is required, so the old metadata attack does not work."),
             (0, "The instance profile is LabInstanceProfile, the one the lab supplies.")),
  "code_blocks": _c(
      "# main.tf",
      "resource \"aws_instance\" \"vm\" {",
      "  ami                    = data.aws_ami.ubuntu.id",
      "  instance_type          = local.instance_type",
      "  key_name               = var.key_name",
      "  subnet_id              = local.lab_subnet_id",
      "  vpc_security_group_ids = [aws_security_group.vm.id]",
      "  iam_instance_profile   = var.lab_instance_profile",
      "",
      "  root_block_device {",
      "    volume_size = 30",
      "    volume_type = \"gp3\"",
      "  }",
      "",
      "  user_data = file(\"${path.module}/bootstrap.sh\")",
      "}"),
  "term_title": "hcl  —  main.tf"},

 # ---- 5 credentials ----
 {"slide_type": "content", "title": "Step 1 — Get Your AWS Credentials",
  "body": _b((0, "Click Start Lab, and wait for the dot beside AWS to turn green."),
             (0, "Click AWS Details at the top. A Cloud Access panel opens."),
             (0, "Copy the whole block that starts with [default]."),
             (0, "Paste it into ~/.aws/credentials, and replace the old content."),
             (0, "The credentials expire after 4 hours. Paste them again each session.")),
  "code_blocks": _c(
      "$ mkdir -p ~/.aws",
      "$ vi ~/.aws/credentials",
      "",
      "[default]",
      "aws_access_key_id=ASIA...",
      "aws_secret_access_key=...",
      "aws_session_token=...",
      "",
      "$ printf '[default]\\nregion = us-east-1\\n' > ~/.aws/config",
      "",
      "$ aws sts get-caller-identity",
      "{",
      "    \"Account\": \"011421346341\",",
      "    \"Arn\": \"arn:aws:sts::011421346341:assumed-role/voclabs/...\"",
      "}"),
  "term_title": "bash  —  aws cli"},

 # ---- 6 apply ----
 {"slide_type": "content", "title": "Step 2 — terraform init and terraform apply",
  "body": _b((0, "Change into the Week02 directory. Terraform reads only that folder."),
             (0, "key_name has no default, so Terraform asks you for it."),
             (1, "Type the name of YOUR key pair, from EC2 > Key Pairs."),
             (0, "The apply creates 5 resources and takes about one minute."),
             (1, "One security group, three rules, one machine.")),
  "code_blocks": _c(
      "$ cd Week02",
      "$ terraform init",
      "Terraform has been successfully initialized!",
      "",
      "$ terraform apply",
      "",
      "var.key_name",
      "  Name of YOUR EC2 key pair (AWS Console > EC2 > Key Pairs).",
      "",
      "  Enter a value: vockey",
      "",
      "Plan: 5 to add, 0 to change, 0 to destroy.",
      "  Enter a value: yes",
      "",
      "aws_instance.vm: Creation complete after 14s [id=i-01caee...]",
      "Apply complete! Resources: 5 added, 0 changed, 0 destroyed."),
  "term_title": "bash  —  terraform"},

 # ---- 7 outputs ----
 {"slide_type": "content", "title": "Step 3 — Read the Outputs",
  "body": _b((0, "Every apply ends with the addresses you need."),
             (0, "public_ip is how you reach the machine from outside."),
             (0, "private_ip is the address inside the VPC."),
             (0, "app_url is the page you open after the app runs."),
             (0, "The lab stops the machine between sessions, and the public address changes."),
             (1, "Run terraform refresh before terraform output.")),
  "code_blocks": _c(
      "Outputs:",
      "",
      "app_url    = \"http://3.91.242.254:8080/\"",
      "next_step  = \"ssh -i <your-key.pem> ubuntu@3.91.242.254\"",
      "private_ip = \"172.31.90.25\"",
      "public_ip  = \"3.91.242.254\"",
      "",
      "$ terraform output -raw public_ip",
      "3.91.242.254",
      "",
      "$ terraform output -raw private_ip",
      "172.31.90.25"),
  "term_title": "bash  —  terraform"},

 # ---- 8 ssh ----
 {"slide_type": "content", "title": "Step 4 — Open a Session on the Machine",
  "body": _b((0, "ssh refuses a key file that other users can read."),
             (1, "chmod 400 fixes it. Run it once."),
             (0, "The user on an Ubuntu image is ubuntu, not root and not ec2-user."),
             (0, "The message of the day tells you what the machine holds."),
             (0, "Only git is ready. You install everything else yourself.")),
  "code_blocks": _c(
      "$ chmod 400 your-key.pem",
      "$ ssh -i your-key.pem ubuntu@3.91.242.254",
      "",
      "Welcome to Ubuntu 26.04.1 LTS (GNU/Linux 7.0.0-1012-aws x86_64)",
      "",
      "  CLO835 - Week 02 - The manual deployment VM",
      "  -------------------------------------------",
      "  This machine has git only. Nothing else is prepared.",
      "  Follow runAWS_EC2.sh, section by section.",
      "",
      "ubuntu@ip-172-31-84-138:~$ git --version",
      "git version 2.51.0"),
  "term_title": "bash  —  ssh"},

 {"slide_type": "section_divider", "kicker": "PART 1",
  "title": "The Manual Way",
  "subtitle": "On the EC2 machine — runAWS_EC2.sh"},

 # ---- 10 clone ----
 {"slide_type": "content", "title": "Clone the Application",
  "body": _b((0, "bootstrap.sh installed git at first boot. Nothing else."),
             (0, "The repo holds three files that matter."),
             (1, "app.py — the Flask application."),
             (1, "requirements.txt — Flask==3.1.3, pinned."),
             (1, "Dockerfile — Part 2 uses this one.")),
  "code_blocks": _c(
      "$ git clone https://github.com/sojoudian/simple-webapp-flask",
      "Cloning into 'simple-webapp-flask'...",
      "Receiving objects: 100% (1508/1508), 6.08 MiB | 26.95 MiB/s, done.",
      "",
      "$ cd simple-webapp-flask",
      "$ ls -l",
      "Dockerfile  LICENSE  README.md  app.py  requirements.txt"),
  "term_title": "bash  —  git"},

 # ---- 11 install python ----
 {"slide_type": "content", "title": "Install Python",
  "body": _b((0, "Ubuntu 26.04 already ships python3, version 3.14."),
             (0, "It does NOT ship python3-venv. You install that."),
             (0, "python3-venv lives in the universe component of the archive."),
             (0, "Note what apt pulls in: pip and setuptools wheels, for the venv.")),
  "code_blocks": _c(
      "$ sudo apt-get update -y",
      "$ sudo apt-get install -y python3 python3-venv",
      "",
      "python3 is already the newest version (3.14.3-0ubuntu2).",
      "The following NEW packages will be installed:",
      "  python3-pip-whl python3-setuptools-whl python3-venv python3.14-venv",
      "",
      "$ python3 --version",
      "Python 3.14.4"),
  "term_title": "bash  —  apt"},

 # ---- 12 PEP 668 ----
 {"slide_type": "content", "title": "Install Flask — the Virtual Environment",
  "body": _b((0, "Ubuntu 24.04 and later protect the system Python. This is PEP 668."),
             (1, "pip3 install flask is refused, and nothing is installed."),
             (0, "A virtual environment is the correct answer."),
             (1, "venv holds its own python and its own pip."),
             (1, "source venv/bin/activate puts that python first on your PATH."),
             (0, "pip install -r requirements.txt then installs Flask 3.1.3 inside it.")),
  "code_blocks": _c(
      "$ pip3 install flask",
      "error: externally-managed-environment",
      "",
      "x This environment is externally managed",
      "  create a virtual environment using python3 -m venv path/to/venv",
      "  hint: See PEP 668 for the detailed specification.",
      "",
      "$ python3 -m venv venv",
      "$ source venv/bin/activate",
      "(venv) $ pip install -r requirements.txt",
      "Successfully installed Flask-3.1.3 Werkzeug-3.1.8 jinja2-3.1.6"),
  "term_title": "bash  —  pip"},

 # ---- 13 run ----
 {"slide_type": "content", "title": "Run and Test the Application",
  "body": _b((0, "app.py reads the PORT variable, and uses 8080 when it is absent."),
             (0, "host=\"0.0.0.0\" makes it listen on every interface, not only localhost."),
             (1, "Without that, the browser could never reach it."),
             (0, "Test from a second SSH session with curl."),
             (0, "Then open the browser at the public address, on port 8080."),
             (1, "The security group opens that port.")),
  "code_blocks": _c(
      "(venv) $ python3 app.py",
      " * Serving Flask app 'app'",
      " * Running on all addresses (0.0.0.0)",
      " * Running on http://127.0.0.1:8080",
      "",
      "# from a second SSH session",
      "$ curl http://localhost:8080/",
      "Welcome CLO835!",
      "",
      "$ curl 'http://localhost:8080/how%20are%20you'",
      "I am good, how about you?",
      "",
      "# in your browser",
      "#   http://3.91.242.254:8080/"),
  "term_title": "bash  —  flask"},

 # ---- 14 count the cost ----
 {"slide_type": "content", "title": "Count the Cost of the Manual Way",
  "body": _b((0, "You typed six commands to get one page on one machine."),
             (0, "Answer these before you continue:"),
             (1, "How do you repeat these steps on a second machine?"),
             (1, "How do you move this result to another computer?"),
             (1, "What stays on the machine after you stop the application?"),
             (1, "What breaks on a different Ubuntu version?"),
             (0, "Part 2 answers all four with one file and one command.")),
  "bullet_size": 16},

 {"slide_type": "section_divider", "kicker": "PART 2",
  "title": "The Container Way",
  "subtitle": "On your own laptop — localMachine.sh"},

 # ---- 16 read the dockerfile ----
 {"slide_type": "content", "title": "Read the Dockerfile",
  "body": _b((0, "Every line repeats one step you typed by hand in Part 1."),
             (0, "FROM ubuntu:26.04 is the same operating system as the EC2 machine."),
             (0, "The venv is at /opt/venv, and ENV PATH puts it first."),
             (0, "requirements.txt is copied before app.py, on purpose."),
             (1, "Docker reuses the pip layer when only app.py changes."),
             (0, "EXPOSE 8080 is documentation. It does not open the port."),
             (1, "-p 8080:8080 on docker run opens it.")),
  "code_blocks": _c(
      "FROM ubuntu:26.04",
      "",
      "ENV DEBIAN_FRONTEND=noninteractive",
      "",
      "RUN apt-get update -y \\",
      " && apt-get install -y --no-install-recommends python3 python3-venv ca-certificates \\",
      " && rm -rf /var/lib/apt/lists/*",
      "",
      "WORKDIR /opt",
      "",
      "RUN python3 -m venv /opt/venv",
      "ENV PATH=\"/opt/venv/bin:$PATH\"",
      "",
      "COPY requirements.txt .",
      "RUN pip install --no-cache-dir -r requirements.txt",
      "",
      "COPY app.py .",
      "",
      "EXPOSE 8080",
      "CMD [\"python3\", \"app.py\"]"),
  "term_title": "Dockerfile", "term_fs": 11},

 # ---- 17 build ----
 {"slide_type": "content", "title": "Build the Image",
  "body": _b((0, "docker build reads the Dockerfile and runs every line for you."),
             (0, "-t gives the image a name and a tag."),
             (0, "The dot at the end is the build context, not the Dockerfile."),
             (0, "The steps you typed by hand in Part 1 now run in about 20 seconds."),
             (0, "The result is one image, for one CPU type. Slide 20 fixes that.")),
  "code_blocks": _c(
      "$ docker build -t simple-webapp-flask:v1 .",
      "",
      " => [2/7] RUN apt-get update -y && apt-get install ...      12.4s",
      " => [4/7] RUN python3 -m venv /opt/venv                      3.1s",
      " => [6/7] RUN pip install --no-cache-dir -r requirements.txt 1.7s",
      " => [7/7] COPY app.py .                                      0.0s",
      " => exporting to image                                       1.0s",
      " => naming to docker.io/library/simple-webapp-flask:v1",
      "",
      "$ docker images | grep simple-webapp-flask",
      "simple-webapp-flask  v1  56cbafc914e9  252MB"),
  "term_title": "bash  —  docker"},

 # ---- 18 run the container ----
 {"slide_type": "content", "title": "Run and Test the Container",
  "body": _b((0, "-d runs it in the background, and prints the container id."),
             (0, "--name gives it a name you can type."),
             (1, "Remove the old one first, or the name is already in use."),
             (0, "-p 8080:8080 maps host port 8080 to container port 8080."),
             (0, "The answer is the same page as Part 1, from the same code."),
             (0, "docker logs shows what the application wrote.")),
  "code_blocks": _c(
      "$ docker rm -f webapp 2>/dev/null",
      "$ docker run -d --name webapp -p 8080:8080 simple-webapp-flask:v1",
      "b8706115d701...",
      "",
      "$ docker ps",
      "CONTAINER ID  IMAGE                   PORTS                   NAMES",
      "b8706115d701  simple-webapp-flask:v1  0.0.0.0:8080->8080/tcp  webapp",
      "",
      "$ curl http://localhost:8080/",
      "Welcome CLO835!",
      "",
      "$ docker logs webapp",
      " * Running on all addresses (0.0.0.0)"),
  "term_title": "bash  —  docker"},

 # ---- 19 cmd vs entrypoint ----
 {"slide_type": "content", "title": "CMD and ENTRYPOINT — the Difference",
  "body": _b((0, "CMD sets the default command. Anything you type REPLACES it."),
             (1, "docker run <image> bash gives you a shell, and Flask never starts."),
             (0, "ENTRYPOINT sets a fixed command. Anything you type is APPENDED to it."),
             (1, "docker run <image> bash would run python3 app.py bash."),
             (1, "app.py ignores the extra word, so Flask still starts."),
             (0, "Our Dockerfile uses CMD, so the container is easy to debug.")),
  "code_blocks": _c(
      "# CMD [\"python3\", \"app.py\"]   <- what our Dockerfile uses",
      "",
      "$ docker run -it simple-webapp-flask:v1 bash",
      "root@a1b2c3d4e5f6:/opt# ls",
      "app.py  requirements.txt  venv",
      "root@a1b2c3d4e5f6:/opt#        # Flask did NOT start",
      "",
      "# ENTRYPOINT [\"python3\", \"app.py\"]   <- if it were this instead",
      "",
      "$ docker run -it simple-webapp-flask:v1 bash",
      " * Running on http://127.0.0.1:8080",
      "#        # \"bash\" became an argument. Flask DID start."),
  "term_title": "bash  —  docker"},

 # ---- 20 buildx ----
 {"slide_type": "content", "title": "Publish for Every CPU",
  "body": _b((0, "A Mac with Apple Silicon builds arm64. The EC2 machine is x86_64."),
             (1, "That image fails there with exec format error."),
             (0, "buildx builds both, and --push sends both under one name."),
             (1, "Docker then picks the correct one on each machine."),
             (0, "--push is required, not --load."),
             (1, "A local image list holds one CPU type only."),
             (0, "--push also tags, so docker tag is not needed.")),
  "code_blocks": _c(
      "$ docker login",
      "Login Succeeded",
      "",
      "$ docker buildx build \\",
      "    --platform linux/amd64,linux/arm64 \\",
      "    -t <user>/simple-webapp-flask:v1 --push .",
      "",
      " => [linux/amd64 6/7] RUN pip install ...                 1.7s",
      " => [linux/arm64 6/7] RUN pip install ...                 4.9s",
      " => pushing manifest for docker.io/<user>/simple-webapp-flask:v1",
      "",
      "# On plain Docker Engine, run this ONCE first:",
      "$ docker buildx create --use"),
  "term_title": "bash  —  buildx"},

 # ---- 21 inspect ----
 {"slide_type": "content", "title": "Prove Both CPU Types Are There",
  "body": _b((0, "imagetools inspect reads the manifest list on Docker Hub."),
             (0, "Both linux/amd64 and linux/arm64 must appear under Manifests."),
             (0, "Capture your Docker Hub repository page with the tag visible."),
             (0, "Now ANY computer with Docker repeats all of Part 1 with one command."),
             (1, "That is the point of the whole lab.")),
  "code_blocks": _c(
      "$ docker buildx imagetools inspect <user>/simple-webapp-flask:v1",
      "",
      "Name:      docker.io/<user>/simple-webapp-flask:v1",
      "MediaType: application/vnd.oci.image.index.v1+json",
      "",
      "Manifests:",
      "  Name:      ...simple-webapp-flask:v1@sha256:4fde9f1c...",
      "  Platform:  linux/amd64",
      "",
      "  Name:      ...simple-webapp-flask:v1@sha256:11cd2646...",
      "  Platform:  linux/arm64",
      "",
      "# on the EC2 machine, or on any computer",
      "$ docker run -d -p 8080:8080 <user>/simple-webapp-flask:v1"),
  "term_title": "bash  —  buildx"},

 # ---- 22 destroy ----
 {"slide_type": "content", "title": "Delete the Machine",
  "body": _b((0, "Run terraform destroy in the Week02 directory, not in the app folder."),
             (1, "Terraform reads the .tf files and the state file from there."),
             (0, "terraform.tfstate records what to delete. It is not in git."),
             (0, "A stopped machine still pays for its 30 GB disk."),
             (0, "One 4-hour session costs roughly 0.40 USD of your 50 USD budget.")),
  "code_blocks": _c(
      "$ docker rm -f webapp",
      "",
      "$ cd Week02",
      "$ terraform destroy",
      "",
      "Plan: 0 to add, 0 to change, 5 to destroy.",
      "  Enter a value: yes",
      "",
      "aws_instance.vm: Destroying... [id=i-01caee6446f8856c0]",
      "aws_instance.vm: Destruction complete after 33s",
      "aws_security_group.vm: Destruction complete after 2s",
      "",
      "Destroy complete! Resources: 5 destroyed."),
  "term_title": "bash  —  terraform"},

 # ---- 23 submit ----
 {"slide_type": "content", "title": "What to Submit",
  "body": _b((0, "The Terraform outputs, and an ssh session on the machine."),
             (0, "git --version on the new machine, and python3 -m venv failing before you install it."),
             (0, "curl returning Welcome CLO835! on the EC2 machine, and the same page in a browser."),
             (0, "docker build, docker ps, and curl on your own laptop."),
             (0, "imagetools inspect showing both linux/amd64 and linux/arm64."),
             (0, "Your Docker Hub repository page with the tag visible."),
             (0, "Destroy complete! at the end."),
             (0, "Put your name on every screenshot. Explain every command.")),
  "bullet_size": 14},

 {"slide_type": "closing", "title": "Lab 1 – The end"},
]


def build_all():
    build_deck(DECK, OUT)


if __name__ == "__main__":
    # RUN-SAFETY: guarded so importing never writes.
    build_all()
