<!-- Slide number: 1 -->

Hands-on Lab
Networking, Storage
and Security in one stack

![docker_logo.jpg](Picture5.jpg)
Build a MySQL + Adminer stack with a user-defined network, a persistent volume, and a hardened runtime.
Instructor: Professor Maziar
CLO835 · Week 3 · ~30 minutes

![whale.png](Picture7.jpg)
CLO835, Fall 2026     1 / 8

<!-- Slide number: 2 -->
What you'll build
Three concepts, one stack. Each step lights up one of this week's pillars.

Networking

Time

~30 minutes
Create a user-defined network so containers find each other by name.

Prereqs

Docker installed; bash shell

Storage

Images

mysql:8 · adminer:latest
Attach a named volume to MySQL so data survives docker rm.

Network

user-defined bridge

Security

Volume

named (mysql-data)
Scan the image, run as non-root, drop capabilities, mount the password as a secret.

Scanner

docker scout / trivy

Verify

Deliverable

Lab notebook (commands + output)
Use Adminer to log in, confirm the row survives a restart.

![whale.png](Picture43.jpg)
CLO835, Fall 2026     2 / 8

<!-- Slide number: 3 -->
Step 1 — Create a user-defined network

GOAL   Make a private bridge network so MySQL and Adminer can find each other by name. The default bridge does NOT do DNS — that's the whole point.

Expected
bash — docker

A bridge network named clo835-net with the subnet you asked for, and no containers attached yet.
# 1. create the network
$ docker network create \
    --driver bridge \
    --subnet 172.28.0.0/16 \
    clo835-net
3a7b1e9c8d5f...

# 2. confirm it exists
$ docker network ls | grep clo835
3a7b1e9c8d5f   clo835-net   bridge   local

# 3. inspect — note IPAM range and empty Containers map
$ docker network inspect clo835-net
[ { "Name": "clo835-net",
    "Driver": "bridge",
    "IPAM": { "Config":
        [{ "Subnet": "172.28.0.0/16" }] },
    "Containers": {} } ]
Why a custom bridge?
Only user-defined bridge networks enable name-based DNS resolution. The default bridge network does not.

![whale.png](Picture16.jpg)
CLO835, Fall 2026     3 / 8

<!-- Slide number: 4 -->
Step 2 — MySQL on the network, backed by a volume

GOAL   Run MySQL on clo835-net with a named volume so the data dir lives outside the container. Then write one row.

Expected
bash — docker

mysql-db running, attached to clo835-net, volume mounted.
# 1. create the named volume (explicit is better)
$ docker volume create mysql-data
mysql-data

# 2. start MySQL on the network, with the volume
$ docker run -d \
    --name mysql-db \
    --network clo835-net \
    -e MYSQL_ROOT_PASSWORD=db_clo835 \
    --mount type=volume,source=mysql-data,target=/var/lib/mysql \
    mysql:8

# 3. seed one row — proof that data lives on the volume
$ docker exec mysql-db \
    mysql -uroot -pdb_clo835 --table -e "
       CREATE DATABASE foo;
       USE foo;
       CREATE TABLE pets(name VARCHAR(20));
       INSERT INTO pets VALUES('Puffball');
       SELECT * FROM pets;"

$ docker ps --format \
   '{{.Names}}\t{{.Status}}'
mysql-db   Up 12 seconds

$ docker volume ls
DRIVER  NAME
local   mysql-data
Why a volume, not a bind mount?
Named volumes are Docker-managed, portable across hosts, and the right default for databases.

![whale.png](Picture18.jpg)
CLO835, Fall 2026     4 / 8

<!-- Slide number: 5 -->
Step 3 — Connect a web UI by container name

GOAL   Start Adminer on the same network and point it at "mysql-db" by name — no IPs. This is service discovery in action.

Expected
bash — docker

Adminer login succeeds. You can browse the foo database and see the pets table with Puffball.
# 1. start Adminer on clo835-net, publish port 8080
$ docker run -d \
    --name adminer \
    --network clo835-net \
    -p 8080:8080 \
    adminer:latest

# 2. prove DNS works from inside the network
$ docker run --rm \
    --network clo835-net \
    alpine nslookup mysql-db
Name:    mysql-db
Address: 172.28.0.2

# 3. open the Adminer UI
# Browser → http://localhost:8080
#   System:   MySQL
#   Server:   mysql-db        ← BY NAME, not IP
#   Username: root
#   Password: db_clo835

clo835-net   ·   172.28.0.0/16

adminer

mysql-db
:8080
vol: mysql-data
DNS
Outside → :8080 → adminer → mysql-db

![whale.png](Picture25.jpg)
CLO835, Fall 2026     5 / 8

<!-- Slide number: 6 -->
Step 4 — Now harden it

GOAL   Apply the four pillars in order: scan the image, restart the MySQL container as non-root, drop capabilities, and stop passing the password through an env var.

What you just did
bash — docker

# 1. IMAGE — scan for vulnerabilities
$ docker scout cves mysql:8
   (or: trivy image mysql:8)

# 2. SECRETS — keep the password OFF the command line
$ echo 'db_clo835' > ./db_password.txt
$ chmod 600 ./db_password.txt

# 3. RUNTIME — restart MySQL hardened
$ docker rm -f mysql-db
$ mkdir -p $PWD/mysql-data

docker run -d \
    --name mysql-db \
    --network clo835-net \
    --mount type=bind,source=$PWD/mysql-data,target=/var/lib/mysql \
    --mount type=bind,source=$PWD/db_password.txt,target=/run/secrets/db_password,readonly \
    -e MYSQL_ROOT_PASSWORD_FILE=/run/secrets/db_password \
    --cap-drop=ALL \
    --cap-add=CHOWN \
    --cap-add=SETGID \
    --cap-add=SETUID \
    --cap-add=DAC_OVERRIDE \
    --cap-add=FOWNER \
    --security-opt=no-new-privileges \
    mysql:8
Image

1
Scan with Scout or Trivy before you ship.
Secrets

2
Password in a file with 0600, mounted read-only at /run/secrets/.
Runtime

3
Drop ALL caps · add back only chown/setuid/setgid · no new privs.
Network

4
Stayed on clo835-net — never published MySQL's 3306 to the host.

![whale.png](Picture29.jpg)
CLO835, Fall 2026     6 / 8

<!-- Slide number: 7 -->
Verify everything works — then clean up

GOAL   Confirm the row survived the MySQL restart, then tear down every resource you created. Leave no orphans.
Verify
Tear down

bash — verify
bash — cleanup

# stack is healthy?
$ docker ps --filter network=clo835-net
NAMES      STATUS         PORTS
adminer    Up 2 minutes   :8080->8080
mysql-db   Up 30 seconds  3306/tcp

# row survived the restart?
$ docker exec mysql-db bash -c \
    'mysql -uroot -p"$(cat /run/secrets/db_password)" -e "USE foo; SELECT * FROM pets;" 2>/dev/null'
# stop and remove the containers
$ docker rm -f mysql-db adminer

# remove the network
$ docker network rm clo835-net

# remove the volume (deletes the data!)
$ docker volume rm mysql-data

# delete the local secret file
$ rm ./db_password.txt

# confirm nothing is left behind
$ docker ps -a --filter network=clo835-net
$ docker network ls | grep clo835
$ docker volume ls | grep mysql-data
# all three should print nothing

![whale.png](Picture21.jpg)
CLO835, Fall 2026     7 / 8

<!-- Slide number: 8 -->
Submit your lab notebook.
Commands you ran, outputs you saw, answers to the reflections below.
Reflect

1
What would break if you put MySQL on the default bridge network instead?

2
Why does --mount type=volume beat -v for the data directory here?

3
Which of the four security pillars did this lab NOT touch — and how would you add it?
Good luck — Professor Maziar  ·  CLO835 · Seneca Polytechnic · ITAS Program

![whale.png](Picture14.jpg)
CLO835, Fall 2026     8 / 8
