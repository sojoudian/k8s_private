# Report: Assignment 1 — Fixed and Verified by Running It
**Date**: 2026-10-15
**Sequence**: #02 for the day

## Summary
The user asked for Assignment 1 to be 100% correct. Report #01 fixed eight
defects, but it could not test them, because the Docker daemon was off. I
started Docker Desktop and ran the assignment end to end. **The run found three
more defects that reading could not find.** The worst one corrupts the seed data
of every student. All eleven defects are now fixed, and all fifteen checks pass.

## What Changed

### New files
- `assignment-1/.dockerignore` — new.
- This report.

### Changed files, in the public repository
`~/Documents/c/r/a2_test/CLO835_Fall_2026/assignment-1/`
- `Dockerfile_mysql` — rewritten. It no longer uses `--init-file`.
- `mysql.sql` — rewritten. The two seed rows now carry different `emp_id`.
- `Dockerfile` — adds `iputils-ping` (report #01).
- `compose.yaml` — adds `build: .` to `pink` and `lime`; the health check now
  uses TCP.
- `README.md` — the wait loop, the connection test, the sizes and the trouble
  table now hold tested values.

### Changed in the project
- `Assignments/Assignment_1/Assignment1_Blackboard_Submission.md` — the image
  size now reads 380 MB, the measured value.

### Unchanged
- `app.py`, `requirements.txt`, `templates/`.
- `Assignments/Assignment_1/CLO835_Assignment1.docx`, the original handout.
- Nothing is committed, and nothing is pushed.

## Technical Details

### Defect 9 — THE SEED DATA IS INSERTED THREE TIMES
`Dockerfile_mysql` held `CMD [ "mysqld", "--init-file=/tmp/mysql.sql" ]`.
`--init-file` runs on **every container start**. Measured:

| Event | Rows in `employees.employee` |
|---|---|
| First start | **6** |
| After one restart | **8** |
| After two restarts | 10, and so on |

The file holds two INSERT statements, so the table should hold 2 rows. The
MySQL entrypoint starts the server more than one time during the first start,
and the init file runs at each start.

`compose.yaml` keeps the data in a named volume, so a student that runs
`docker compose restart` adds two more rows each time.

**The fix** is the pattern that the official image gives. A `.sql` file in
`/docker-entrypoint-initdb.d/` runs **one time only**, when the data directory
is empty. The custom `CMD` goes.

Measured after the fix: 2 rows at the first start, and 2 rows after a restart.

### Defect 10 — the build context carries the student `venv` and `.git`
Step 1 of the README tells a student to make a virtual environment named `venv`
in that folder. `COPY . .` then copies it into the image, with `.git`.

Measured with a 120 MB `venv` and a 40 MB `.git`:

| | Image size | `/app` holds |
|---|---|---|
| No `.dockerignore` | **544 MB** | `.git`, `venv`, both Dockerfiles, README, compose |
| With `.dockerignore` | **376 MB** | `app.py`, `mysql.sql`, `requirements.txt`, `templates` |

A `.git` folder inside a published image can also carry the history of a file
that held a token.

### Defect 11 — the wait loop can end too early
The README used `mysqladmin ping -uroot -ppw`, over the local socket. MySQL runs
a temporary server during the first start. That server answers on the socket,
so the loop can end before the real server is ready.

`-h 127.0.0.1` forces TCP, and the temporary server does not listen on TCP. The
README and the Compose health check now use the TCP form. On this machine both
forms ended at 6 s, so the defect is a race, not a certainty.

### Defect 4, proven and not assumed
Report #01 took the missing `ping` from a web search. I built the original apt
list and ran it:

```
$ docker run --rm a1_noping sh -c 'which ping || echo "ping: NOT INSTALLED"'
ping: NOT INSTALLED
$ docker run --rm my_app sh -c 'which ping'
/usr/bin/ping
```

The 10-mark requirement was impossible with the supplied `Dockerfile`.

## Results

### The full run, from zero, after every fix

| # | Check | Result |
|---|---|---|
| 1 | `docker build -t my_db -f Dockerfile_mysql .` | OK |
| 2 | `docker build -t my_app -f Dockerfile .` | OK |
| 3 | The two IMAGE IDs differ | OK, `7bfb59886067` and `32254ba5b189` |
| 4 | `docker tag` for Docker Hub | OK, each tag keeps its own ID |
| 5 | MySQL starts on the custom bridge network | OK |
| 6 | The README wait loop ends | OK, 6 s |
| 7 | Seed rows | **2** |
| 8 | blue 8081, pink 8082, lime 8083 | HTTP 200, `#89CFF0`, `#f4c2c2`, `#C1FF9C` |
| 9 | `ping pink` from inside `blue` | OK, 0% packet loss |
| 10 | `ping lime` from inside `blue` | OK, 0% packet loss |
| 11 | POST `/addemp` on blue | OK |
| 12 | POST `/fetchdata` on pink reads the same row | OK |
| 13 | `docker compose up -d` | OK, the database reports healthy |
| 14 | The three ports, under Compose | HTTP 200 on all three |
| 15 | Seed rows under Compose, and after a restart | **2** |

The three colours match `app.py` exactly. Check 12 proves that the three
containers share one database.

### The machine is clean
- Containers that I made: 0 left. The user `webapp` container, from three weeks
  ago, is untouched.
- Networks that I made: 0 left.
- Volumes that I made: 4 removed, by creation time. The 8 user volumes are
  untouched.
- Images that I made: 0 left. `mysql:8.0` stays, because the assignment needs it.
- The safety grep on `assignment-1/` is clean.

## Issues / Notes
- **Docker Desktop is now running.** It was not running before. Quit it if you
  do not need it.
- **The push to Docker Hub is not tested.** A push needs your account
  credentials, and I do not enter credentials. The `docker tag` step is tested,
  and that is where the student defect happened. Run one push before class.
- The test machine is `aarch64`. A student on an Intel machine gets a slightly
  different image size. The README says "about 380 MB".
- `app.py` still holds the default password `passwors`, which is a typo. A
  student always sets `DBPWD`, and the README says so. I did not change it,
  because a change to the default could surprise a student that already works.
- `app.py` opens the database connection at import. A web container therefore
  stops at once when the database is not ready. Compose handles this with the
  health check. The README wait loop handles the manual path.
- `assignment-1/.dockerignore` is a new, untracked file. Add it before you
  commit.
