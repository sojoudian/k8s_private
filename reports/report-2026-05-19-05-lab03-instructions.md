# Report: Lab 03 Submission Instructions
**Date**: 2026-05-19
**Sequence**: #05 for the day

## Summary
Wrote `Lab03_Instructions.md` — a submission rubric for the Week 3 hands-on lab. Format mirrors the Lab 01 instructions the user shared: a top header, an "Instructions" preamble, five bullets each describing one deliverable + the evidence required + an "Explain" question, then the submission requirements and integrity pledge. The PowerPoint filename is intentionally not referenced (user said they may rename it to Lab03.pptx).

## What Changed
- **`Lab03_Instructions.md`** — new file. 5 bullets, each tied to one of the lab's five main exercises.

## Technical Details
**Bullet → lab step mapping:**
1. **Network creation** — evidence: `docker network create` + `docker network inspect` showing the IPAM subnet and empty Containers map. Explain question: why user-defined bridge over default bridge? Would `nslookup` work on the default bridge?
2. **MySQL with named volume** — evidence: `docker ps` + `docker volume ls` + `SELECT * FROM pets` returning Puffball. Explain question: named volume vs bind mount for a database, why a volume is the right default.
3. **Adminer + service discovery** — evidence: the `docker run` command + `nslookup` output + browser screenshot of Adminer showing the pets row. Explain question: how DNS works on a user-defined network, and what the nslookup output proves.
4. **Security hardening** — evidence: the rebuilt `docker run` command + `ls -l` showing 0600 permissions on the secret file + `docker inspect` confirming CapDrop, CapAdd, SecurityOpt. Explain question: why drop-all-then-add-back is safer than the default capability set, and what specific attack `no-new-privileges` prevents.
5. **Verify + teardown** — evidence: the SELECT showing data survived + the full cleanup command sequence + three `docker ... ls | grep` commands all returning no matches. Explain question: which mount made the survival possible, and why Docker doesn't warn before deleting a non-empty volume.

**Format choices that match Lab 01:**
- `* - ` bullet prefix preserved
- "Lab 03" header at top, "Lab Week03" referenced in the instructions preamble (Lab 01 mirrors this: header "Lab 01", preamble references "Lab Week02")
- Each bullet ends with "Explain ..." followed by a probing question (one or two), not just a recap question
- Submission requirements line spacing and wording copied verbatim except for the topic-specific bullets
- Integrity Pledge text quoted verbatim from the Lab 01 example

## Results
- File written to `/Users/maziar/Downloads/k8s_week3/Lab03_Instructions.md`.
- No PowerPoint filename referenced — uses "Lab 03" and "Lab Week03" instead so the deck can be renamed freely.
- 5 bullets aligned 1:1 with the 5 step / verify slides in the hands-on lab deck.

**Port allocation:** N/A — no dev server.

## Issues / Notes
- **Markdown vs plain text**: Saved as `.md` so it renders as formatted text in any markdown viewer, but the content reads cleanly as plain text too (the original Lab 01 was shared in plain text). If the user wants it in `.docx` or `.txt`, the conversion is trivial.
- **The "Explain" questions are intentionally probing** — they go beyond "what did you do?" and ask "why does this work and what would break?", matching the Lab 01 pattern (e.g. "what would happen if ENTRYPOINT were written as CMD instead"). They are not answered in the instructions; students must work them out.
- **Bullet 4 references specific capability names** (chown, setuid, setgid) — these are the three MySQL needs to function. If the lab deck changes to drop or add different caps, this bullet needs updating too.
- **No screenshot file format specified** — the integrity pledge and submission requirements match Lab 01 verbatim. If you want PNG/JPG enforced, add a line.
- **No total point breakdown** — Lab 01 didn't have one either. If you grade with point values per bullet (e.g., 20 each = 100), append a "Marking" section before Submission.
