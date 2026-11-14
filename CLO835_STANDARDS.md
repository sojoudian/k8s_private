# CLO835 Standards and Preferences

Version 1.2, 2026-11-11. Owner: Maziar Sojoudian (GitHub `sojoudian`, Docker Hub `maziar`).

This file collects every standard and preference for the CLO835 lectures, labs, quizzes and the
practical work in the AWS Academy Learner Lab. Its sources:

- `~/.claude/CLAUDE.md` and the project `CLAUDE.md` (the mandatory rules).
- `~/.claude/PREFERENCES.md` (15 sections, 2026-10-27).
- `PROMPT.md` and `DESIGN_LANGUAGE.md` (the deck design spec of 2026-05).
- The memory folder of this project.
- The Week 05 audit (report 2026-10-07-01).
- The gate `gate_week12.py` and the quiz tools in `quiz_pool_src/`.
- The work of 2026-11-09 and 2026-11-10: Week 07 lecture v7 and lab v3, Week 10 lecture v11, lab v4 and
  the easy quiz.

Where two sources do not agree, the newer rule in this file wins. A rule that came from a defect also says
why, in one line. An independent reviewer checked version 1; version 1.1 has the 20 fixes of that review.
Version 1.2 adds the rule of the user of 2026-11-11: a lab on AWS has no cleanup script (C1, C5, C7, C9, E3).

**Rules of PROMPT.md and DESIGN_LANGUAGE.md that this file replaces:**
- R1 (keep the source text verbatim): ASD-STE100 and correct facts now win. Keep the source text only when
  it is correct and in ASD-STE100. Adopt a hand edit of the user exactly.
- The cover title of 44 pt: it is now 34 pt.
- R7 (a Python logo as the Pod icon): the decks use native shapes.
- R8 and the old names `WeekNN_lab_style_vN`: the names are now those of A5.
- The `soffice` render: make the PDF with PowerPoint (A6).
- The reference deck `Week04_v02_02`: the reference redesign is now `week01/Week01_lecture_style_v5.pptx`.
- TERM_ERR F07178: an error line uses FF5F56 (B2).

---

## Part A. How to work

### A1. Language: ASD-STE100 (the highest priority)

Write every sentence in ASD-STE100: the chat, the reports, the slides, the lab comments, the Blackboard
texts, the quiz stems, the options and the feedback.

- Keep a procedural sentence to 20 words or fewer.
- Keep a descriptive sentence to 25 words or fewer. The deck gate fails a sentence above 25 words.
- Use the active voice and the present tense.
- Give one instruction in one sentence, and start it with the verb.
- Keep the articles (the, a, an).
- Use no contraction, and no possessive `'s` in a deck (the gate pattern fails both). Verbatim program output
  is the only exception, for example `error: the server doesn't have a resource type "storageclass"`.
- Use no slang, no idiom and no phrasal verb. Examples found in review: "holds back", "stays in one piece",
  "touch the data", "at once", "carry over", "shut down", "turn off", "hand over", "go out", "go past".
- Keep a paragraph to 6 sentences or fewer.
- Use a vertical list for complex data.
- Do not use "we".
- Numbers in a deck: the gate wants a word for the digits 2 to 9 before "step", "file", "method", "way",
  "entries" and "section" in prose ("three files"). A Blackboard text keeps the digit in "all 7 sections".
  A technical value keeps its digits (40 commands, 15 resources, 5Gi).

**One word for one meaning.** Use the left term. Never use the right term for the same meaning.

| Use | Do not use |
|---|---|
| Kubernetes | K8s, K8s- |
| Pod (capital P) | pod, POD, pet |
| directory | folder |
| create (an object or a volume) | make |
| delete (an API object, in a step or an option) | "the claim goes", "the Pod goes" |
| master node (lab texts and Blackboard texts) | control-plane node |
| control plane (the components) | master (for the components) |
| claim, PersistentVolumeClaim (PVC) | volume claim (alone) |
| PersistentVolume (PV) at first use, then PV | volume (for a PV) |
| DNS name (the full name of a Pod) | host name (for the full name) |
| show (command output; the model texts also say "display its contents" for a file) | print |
| reject (an API server or a builder that does not accept something) | refuse |
| setting, field, flag | option, parameter |
| stay, stays | keep, keeps (in deck text) |
| environment variable | variable (alone) |
| ConfigMap, etcd | Config Map, ETCD |

The deck gate bans these words outside Consolas text:
- `options`, `parameters`, `keep`, `keeps`, `way`, `ways`, `description`, `entries`, `resource`
- `POD`, `PODs`, `K8s-`, `Config Map`, `ETCD`, `we`, `Overrid...`, `bake`, `dumped`, `never on disk`
- `command line` (except "command line interface"), `control-plane node`, `control-plane disk`
- `variable` (without "environment"), `secret volume`, `configMap volume`, `mounted files`, `mounted folder`

### A2. Scope and permission (the second priority)

- Do exactly what the prompt asks, and nothing more.
- Change a file only when the prompt asks for that change.
- Create a cloud resource only when the prompt asks for it. The approval of one prompt does not apply to the
  next prompt.
- Run a command with a side effect only when the prompt asks for it.
- A question is not permission. A complaint, swearing or anger is not permission.
- When the user is angry, answer in one or two lines and take no action.
- Offer an action in one sentence, then wait for a clear yes.
- A pasted brief is context only. Acknowledge it and wait.
- "Analyze" means a read-only pass. "Audit" means read-only first. Fix only when the user says so.
- "Fix all of these" means every defect of the list, not a selection.
- "Mostly" is not acceptable. Meet each rule 100 %.
- "Up to my standards" means the same checks as the Week 05 audit of 2026-10-07 (report 2026-10-07-01).
- "Make X the same way as Y" means the whole process of Y, including the lecture fixes that Y needed.
- A fix of X can make Y false (for example, a lab change that makes a lecture slide false). Then make the
  smallest change to Y, bump its version, and say so in the answer.
- When the user asks for change X, change X is the only change. Never remove an approved element without
  a question.
- Adopt a hand edit of the user exactly, with its typing mistakes. Trust the diff, not the slide number.
- A request for a slide narrative gets the text only. Do not offer speaker notes.

### A3. The answer in the chat

- Answer in 1 to 4 lines. Give no recap, no file list, no table and no sources block.
- Name the report path only.
- A yes-or-no question gets "Yes" or "No" first. "Only yes or no" means one word.
- "Just list X" means one flat list: no categories, no preface, no caveat.
- Give a longer answer only when the user asks for it, for example "in a few paragraphs" or
  "give me the full text".
- A Blackboard text that the user will paste: give it in one code block, exactly as the file holds it.
- Never claim "fixed", "good" or "done" without the proof of A7.

### A4. Reports

- Write a report after every substantive action:
  `/Users/maziar/Downloads/k8s_week3/reports/report-YYYY-MM-DD-NN-short-description.md`.
- Number the reports of one day in order (01, 02, ...).
- Use the sections Summary, What Changed, Technical Details, Results, Issues / Notes.
- Put every number, method, review count and open item in the report.
- Skip the report for a pure question with no action.

### A5. Files, versions and builders

- Never overwrite a delivered file. Bump the version for every rebuild after a delivery.
- A file is delivered when the user has received it in an answer. Before that, a rebuild with `--force` is
  allowed.
- Each deck or lab builder has a `VERSION` constant and a `__main__` guard. Without `--force` it stops when
  an output exists, and it writes nothing. Importing a builder writes nothing.
- A builder reads its input deck and never writes it.
- These tools overwrite their outputs with no guard. Copy them to a new version name before a change after
  a delivery:
  - the quiz builder `build_easy20_wNN.py` and `qti_pack.py`;
  - `tools/deck_pipe.sh` (it writes the PDF of the deck);
  - a lab builder without `--no-repo` (it writes the course repo folder).
- Names (since 2026-10-27):
  - `WeekNN/Lecture_weekNN_vN.pptx` and `.pdf`, built by `build_weekNN_lecture_vN.py`.
  - `WeekNN/Lab_weekNN_vN.pptx` and `.pdf`, built by `build_weekNN_lab_vN.py`.
  - `WeekNN/localMachine_vN.sh` (the student script, written by the lab builder).
  - `WeekNN/Lab_weekNN_Blackboard_Submission_vN.md` (written by the lab builder).
  - `quiz_pool_src/Quiz_WNN_Easy20/` with `_Blackboard.txt`, `_AnswerKey.txt`, `_Titles.txt` and
    `_QTI21.zip`.
- When the user asks to delete old versions, move them to the macOS Trash with `/usr/bin/trash`.
  - First check that no current builder reads them.
  - Then list the old builders that now fail.
- The scratchpad under `/private/tmp` is volatile. Keep each tool that a standard needs in
  `/Users/maziar/Downloads/k8s_week3/tools/`.

### A6. The machine and the tools

- Use absolute paths. Do not use `cd` in the shell, because it moves the session. Use
  `terraform -chdir=DIR` and `git -C DIR`.
- Use `/Users/maziar/Downloads/k8s_week3/.venv/bin/python` for python-pptx work. Use `-I` for a script that
  reads untrusted files.
- The editor is vi. Never write `nano`.
- A local server uses port 18090, then 18091, and so on.
- Make every deck PDF with PowerPoint, not LibreOffice (`tools/export_pdf.sh`).
  - LibreOffice puts Carlito and Linux Libertine G in place of Calibri and Consolas.
  - Then the terminal columns do not align, and the layout check is false.

### A7. "Fixed", "good", "done": 0 or 1

The user: "this is computer science it should be either 0 or 1".

Say "fixed" or "good" only after all of these steps:
1. Read all the rule sources: this file, PREFERENCES.md, PROMPT.md, DESIGN_LANGUAGE.md, the Week 05 audit
   (report 2026-10-07-01) and the feedback memories.
2. Run the pass-or-fail gate on the final files, with no output cut.
3. Read every page of the PowerPoint PDF with your eyes. Check the fonts with `pdffonts`.
4. Get an independent review: a fresh subagent with the rules and the files, not your conclusion.
5. Fix each finding. Then run the gate and a new review again, because a fix can make a new defect.
6. State the scope of the claim ("the 25 listed defects", not "all flaws"). State what is not tested.

---

## Part B. Lecture decks

### B1. Canvas and chrome

- The canvas is 13.333 x 7.5 in (16:9), with a white background and the blank layout.
- Use Calibri and Consolas only, in the `.pptx` and in the PDF.
- Put the whale and the footer on every slide:
  - the whale at (0.45, 6.85), 0.5 x 0.5 in;
  - the footer `CLO835, Fall 2026     N / TOTAL`, where TOTAL is the slide count of this deck.
- Put no shape in the title band (top between 0.3 and 1.42 in), except the title text box.
- Put no shape in the footer band (bottom below 6.705 in), except the chrome.
- Put no shape off the canvas. Use an integer for every coordinate, because a float moves the shape to the
  corner.
- Keep the deck near 1 MB. When you remove a picture, also drop its image part.
- Set the file Title, the Author "Maziar Sojoudian" and Last Modified By, in the `.pptx` and in the PDF.
- Keep no blank thumbnail and no speaker notes.
- Keep a slide hidden when the source deck hides it. Otherwise hide no slide.
- Use only two pictures: the whale and the Kubernetes logo. Draw everything else as a native shape.

### B2. Palette (hex values, from the gate)

| Token | Hex | Use |
|---|---|---|
| BLUE | 1FA8E0 | accent, titles |
| SLATE | 37465A | dark text, outlines |
| BODY | 3F3F3F | body text |
| MUTED | 868686 | subtitles, notes, footer |
| LIGHTBLUE | CFDBEE | rings, light fills |
| CARD_BG | F4F7FB | cards |
| RULE_GRAY | E0E0E0 | separators |
| GOAL_GREEN | 27AE60 | success marks |
| ALERT_RED | E74C3C | caution cards |
| TERMBG | 2A2A2A | terminal body |
| STEPS | 1FA8E0, 2196A0, 1F8FCD, 1F7AB8, 2466A0, 37465A | step fills |
| terminal | 3A3A3A, FF5F56, FFBD2E, 27C93F, BABABA, 4EC9E0 | terminal bar and text; FF5F56 also for error lines |
| white | FFFFFF | |

Use no other color. Shape variety does not give permission for an outside color.

### B3. Text sizes

- The cover title is 34 pt. A content title is 30 pt, bold, BLUE, with one style in the deck.
- Body text is at least 12 pt. The Course Outline slide uses 12 pt.
- Terminal text is 9 to 14 pt. The title bar of a terminal can be 10 pt.
- At 11 pt Consolas with spacing 1.0, one terminal line is about 0.185 in. So 25 lines fit in a terminal of
  5.22 in, and 26 lines do not (measured in the PowerPoint PDF, 2026-11-10).
- Use Consolas for a code name, a command, a file name, a path and an IP address. In body text it is bold
  SLATE.

### B4. Bullets

- PowerPoint for Mac does not show an `a:buChar` bullet with "▪".
- Write the glyph as a bold run plus a tab (`"▪\t"`), with a hanging indent (marL, and indent -228600).
  The indent then works as the tab stop.
- Keep the bullet hierarchy of the source slide (parent, child, grandchild).

### B5. Terminals

- Each command line starts with `$` (the master) or `L$` (your own machine, in a lab deck).
- A comment line starts with `#`. A sample output line is a comment.
- No line wraps in the PowerPoint PDF, and no text is outside the terminal box. The gate checks both.
- Use no EN DASH, no curly quotation mark, no zero-width space and no other non-ASCII character in Consolas
  text.
- Each command runs as shown on the course cluster, with the current syntax (`kubectl exec POD -- cmd`,
  `networking.k8s.io/v1`).
- A terminal labeled "Lab Week N, Step M" holds only commands that exist in that lab step.

### B6. Diagrams and images

- Draw native house diagrams. Use no third-party screenshot, no watermark, no WMF and no image below 110 DPI.
- Use a shape arrow (for example `LEFT_RIGHT_ARROW`) for a horizontal or a vertical arrow, not a connector.
  A connector with zero extent is not visible in PowerPoint and Keynote.
- When you put labels around a logo, put them at least 0.40 in past the ring radius.
- Draw a line under a bar before the bar, so that the line does not cross the bar text.
- A text extract misses the content in an image. Render the slide and compare.
- Read a deck with `prs.slides`, because `slideN.xml` is the creation order, not the deck order.

### B7. Content

- Make every fact correct for Kubernetes v1.35. Check it on kubernetes.io or on the live cluster.
- Name the version for a feature that became stable (for example "stable in v1.32").
- Use the current API. Remove a removed feature, and mark a deprecated feature as deprecated.
- State a point one time. State it a second time only when it is necessary. Never state it three times.
  No two lectures hold the same slide.
- Give no two slides the same title. Put no bullet word for word on two slides.
- Use no fragment card (a card that holds a piece of another card).
- Make a bullet describe what the slide shows.
- Make the Course Outline follow the course schedule (G3).
- Each lecture has these slides:
  - a cover, an agenda and the Course Outline;
  - part dividers, then the content;
  - Optional Topics (marked "not in the lab or in the quiz");
  - Key Takeaways;
  - "Lab Week NN at a Glance".
- "Lab Week NN at a Glance" maps each lab step to its lecture slides. Its note "Not in the lab: ..." names
  each lecture topic that the lab does not practise. Keep this slide true when the lab changes.
- The examples of the lecture use the objects of the lab (for example `data-pv`, `data-pvc`, `writer`,
  the StorageClass `standard`, the StatefulSet `kubia`).
- A concept that the lab does not run gets the label "Concept only: the lab does not run X."
- Every reference link returns HTTP 200, and it names no third-party account (F2).
- Put the instructor name and the institution on a cover only when the source deck has them.

### B8. The build and QA pipeline of a deck

1. Build with the builder, from the project root: `.venv/bin/python build_weekNN_lecture_vN.py`.
2. Export, set the PDF info, run the gate and make page sheets:
   `SHEETS=<scratch folder> tools/deck_pipe.sh WeekNN Lecture_weekNN_vN "<PDF title>" lecture`.
3. Check that the gate (`tools/rungate.py`, which runs `deck_checks` of `gate_week12.py`) shows `FAILED: 0`.
   The 32 checks:
   - the canvas, a size near 1 MB, the fonts of the `.pptx` and of the PDF;
   - the PDF page count, the PDF newer than the `.pptx`;
   - the footer and the whale on every slide, no shape off the canvas, the footer band, the title band;
   - no image below 110 DPI, no hidden slide (source has none), no speaker notes;
   - body text at least 12 pt, terminal text 9 to 14 pt;
   - no duplicate title, no bullet word for word on two slides;
   - no non-ASCII in Consolas, no banned word, no contraction, small numbers in words;
   - each command starts with `$`, no sentence above 25 words;
   - no banned image, editor or private path, 0 float coordinates, palette only;
   - only the logo and the whale as images, no blank thumbnail, the file title and author;
   - no wrapped terminal line and no text past a terminal box in the PDF.
4. Read every page of the PDF.
5. Get an independent review. Fix, then do steps 1 to 5 again.

---

## Part C. Labs

### C1. Size and structure

- A lab is one workshop, Step 0 to Step 6, with about 30 to 40 commands on the master, for 90 minutes.
  - The Week 03 and Week 04 labs are the size model.
  - The user rejected a lab of 21 steps with anger.
- The lab deck has 10 slides:
  1. the title "Workshop 1 – <topic>";
  2. "Lab Week NN - Prerequisites";
  3. the cluster slide (Step 0);
  4. to 8. the five step slides (Steps 1 to 5);
  9. "Destroy the cluster" (Step 6): only `terraform destroy` on your own machine, and the comment
     "# This also deletes every Kubernetes object and every file of the lab." (`lab_destroy_only.py`);
  10. "Workshop 1 – The End".
- Put one step on one terminal slide. A step with a manifest uses the two-panel slide: the terminal on the
  left and the file on the right.
- The label of a lab is "Lab Week NN", never "Lab NN", because the Blackboard numbers differ (G1).
- Make the lab practise every topic of the lecture, within the size limit. The size limit wins. The lecture
  slide "Lab Week NN at a Glance" names each topic that is not in the lab.

### C2. One content list

- One content list (`SLIDES` in the builder) makes the deck, `localMachine.sh` and the repo copy, so they
  cannot differ.
- Each script step names its slide ("Step 2 - <title> (slide 5)").
- `L.check_lines()` rejects a non-ASCII character in a command line or a file line.
- The builder also writes the Blackboard text (`BLACKBOARD_TEXT`).

### C3. Commands

- Each command runs as shown on the live cluster, and exits 0. The live gate allows no non-zero exit.
- Use `kubectl wait` (for a condition or a jsonpath) in place of a long `sleep`. A short `sleep` before a
  `wait` is allowed when the object does not exist yet.
- Write a manifest with `cat > file.yaml <<'EOF'`, and show the file in the right panel.
- Use only images of Docker Hub `maziar`, with a tag that exists (F2). Docker Official Images and the
  images that kubeadm pulls from registry.k8s.io are allowed.
- Use `maziar/alpine-curl` as the helper image. It runs as root and has `nslookup -type=SRV`. Do not use
  `busybox`.
- Record the change-cause after each `kubectl set image`.
- Give each object one name for the whole lab and the lecture (for example `data-pv`, `data-pvc`, `writer`,
  `dnstest`, `kubia`).
- Delete each helper Pod at the end of its step when the lecture shows the delete.

### C4. Comments and sample output

- Each comment and each sample output agrees with the live output of the final commands.
- The sample versions are the versions that the cluster installs now (v1.35.10 on 2026-11-10).
- Explain an output that can confuse a student. Example: "The Events can show an early FailedBinding event.
  The Status field gives the result: Bound."
- Use the words of the lecture and the glossary of A1.

### C5. The repo folder of a week

- `~/Documents/c/r/CLO835_Fall_2026/WeekNN/` holds the 7 files of Week 04, with the same names, order and
  wording, plus the extra files of the week. It has no README. The files:
  - `.gitignore`, `bootstrap.sh`, `localMachine.sh`;
  - `main.tf`, `master-init.sh.tftpl`, `variables.tf`, `worker-join.sh.tftpl`.
- In `variables.tf`, `key_name` has no default, and `lab_instance_profile` defaults to `LabInstanceProfile`.
- `master-init.sh.tftpl` writes each extra file of the lab (for example `local-path-storage.yaml`) to
  `/home/ubuntu`. `localMachine.sh` calls only files that the master holds.
- No cleanup script (the user, 2026-11-11): `terraform destroy` removes the three machines, and with them
  every Kubernetes object and every file of the lab. So the folder has no `cleanup_labNN.sh`, the master
  gets none, and Step 6 holds only `terraform destroy`. Use `make_repo_folder(..., None, ...)` of
  `lab_kubeadm.py`. Exception: Week 03 runs Docker on the laptop of the student, where `terraform destroy`
  removes nothing, so it keeps `cleanup_lab03.sh`.
- Put no Terraform state, no `.terraform` folder, no `.pem` and no key file in the repo.
- Before anything enters the public repo, do the scan of F3. Run `bash -n` on each script and
  `terraform fmt -check`. Run `terraform validate` in the sandbox copy (E3), because `init` writes files.

### C6. The cluster

- Use kubeadm on EC2: 1 master and 2 workers, `m5.large`, Ubuntu 26.04 ("resolute"), Kubernetes v1.35,
  containerd, Flannel, and the network interface at MTU 1500. Never use kind. Students have no EKS.
- Measured values:
  - 2026-11-10: Kubernetes v1.35.10, Ubuntu 26.04.1, containerd 2.2.2, and `terraform apply` adds 15
    resources;
  - 2026-10-31: the 3 nodes were Ready 1 min 58 s after the apply started.
- The message of the day of the master names the week and `localMachine.sh`.
- Use no Helm. Deployments use raw YAML with `kubectl apply`, `set image` and `rollout undo`.
- Storage on the course cluster is the local-path provisioner (`maziar/local-path-provisioner:v0.0.37`).
  Its default StorageClass `standard` has WaitForFirstConsumer and reclaimPolicy Delete. The EBS CSI
  driver exists only on EKS.

### C7. The Blackboard lab text (long form)

- The model is the item `Lab04 - 2.5%` (Lab Week 06). Week 12 v5 is the newest form that passes the gate.
- Start with `# Lab Week NN: <Topic>` and `## Submission Instructions`, with "all 7 sections" and the
  paragraph on the recording.
- Write one numbered section for each lab step: `## 1.` (the cluster) to `## 7.` ("Destroy the Cluster":
  only `terraform destroy`, the Destroy complete! output and the number of resources; no cleanup item).
- In each section, write a short intro, `You must:`, the `Run ...` and `Show ...` items, and the
  `Explain ...` items last.
- Each `Run` item names a command of that lab step. Each `Explain` item has its answer in the lecture or in a
  lab comment. Build the table of F4.
- End with `## Submission Requirements` (six items) and the paragraph "Important: Use your own screenshots
  ...". Add no Academic Integrity Pledge.
- Write "master node", not "control-plane node" (the gate checks it). Write "control-plane Pods" with a
  capital P.
- Use the words of the deck in the section titles. Examples: "Show That the Data Stays after the Pod and
  the Claim", "Show the Identity of a Pod".
- When the lab changes after students submitted, grade those submissions against the old text.

### C8. Lecture and lab agree

- Each command in a lecture terminal labeled "Lab Week NN, Step M" exists in that lab step.
- Each manifest on a lecture slide is identical to the lab manifest.
- The lecture slide "Lab Week NN at a Glance" lists the right slides for each step and the right
  "Not in the lab" topics.
- When the lab changes, check these three points again. Example: Week 10 lab v4 added the Released phase,
  so lecture v11 changed slide 37.

### C9. The lab checks

Only `deck_checks` of `gate_week12.py` is generic. Its lab, Blackboard and live checks are hard-coded for
Week 12 (folder, file names, title, Flannel images, the runner format `@@CMD/@@STEP/@@RC`). For another
week, check these points by hand or with a copy of the gate for that week:
- the 7 files and the extras; at most 40 commands; Step 0 to Step 6; each step names its slide;
- `bash -n`; `terraform fmt`; no cleanup script in the folder, in master-init or in `localMachine.sh`;
- the repo script equals the deck script;
- images of `maziar` only (Flannel too); no state or key file; the repo scan;
- the Blackboard title, 7 sections, no pledge, Explain items last, the Important paragraph last, no
  "control-plane node";
- live: `terraform output public_ips` and `private_ips`; a full pass on a new cluster with 0 non-zero exits
  (a planned denial, such as a Forbidden answer that a comment predicts, is not a failure); the tested
  commands equal the final commands; the destroy is complete.

`tools/instrument.py` writes `### [n] exit <code>` lines, not the `@@RC` lines of the Week 12 gate.

---

## Part D. Quizzes

### D1. The kinds of quiz

- An easy quiz of 20 questions for one or two weeks: 10 from the lecture and 10 from the lab. Every student
  gets all 20.
- A pool of 100 questions for one lecture (Weeks 01 to 03), from which Blackboard draws.
- The syllabus quizzes (Quiz 1 to 5) are separate items. Check the syllabus before you name one.

### D2. Each question (the rules of 2026-10-26)

- Test one important concept. Do not test a small detail.
- The question stands alone, because a student has no slides during the quiz. Never write a question about a
  picture, a slide, a numbered step or a table.
- Use only content that the course teaches (the lecture, the lab and the earlier weeks). Search the deck
  before you keep a question. A wrong option can use a term that the students have seen.
- Test knowledge that is true in any good source.
- Name no slide, page, chapter or week.
- Prefer an application question with one clear result: an output, a status, a value or a decision.
- A prepared student answers in 1 to 2 minutes, with no calculator.
- Write short sentences in the active voice, with one word for one meaning (A1).
- Use no negative stem. The upload file cannot hold bold text (GATE 14 rejects `<b>`), and the audit fails
  "not" in a stem.
- Define a short form at its first use in each question: "PersistentVolume (PV)".
- Name in the stem every object that an option names. Example: the stem names both workers when an option
  names `workernode2`.
- Close each gap of the scenario in the stem. Examples: "The provisioner still runs." "Nobody changed the
  StatefulSet kubia or its Pods." "The cluster has no StorageClass."

### D3. The options

- Write 4 options, with exactly 1 correct option.
- Make each wrong option a real student mistake that a student with no knowledge cannot remove.
- Use no trick option (two options that differ only in case or in quotes).
- Make each option fit the grammar of the stem, and answer the question that the stem asks.
- Put numbers, times and names in a logical order (the `fix` field of the source).
- Use no "all of the above", "none of the above" or "both A and B". The audit also rejects an option that
  starts with "Both".
- Make the correct option the strictly longest in about 1 question of 4, and the strictly shortest in about
  1 of 4 (GATE 9: 4 to 6 of 20 each).
- No option implies another option: if option X is true, option Y must not also be true.
  Found:
  - Q3: "binds, and the rest of the PV stays free" implied the key.
  - Q18: "turns off authentication" implied "trusts each request from the master".
  - Q11: two options had one result.
- No option contradicts itself (for example "Bound, because a free PV ..."), or the stem.
- No word or form is only in wrong options, or only in keys, across the quiz.
  Found: "but" in 5 wrong options and 0 keys; "Kubernetes" as the actor in 6 wrong options and 0 keys;
  "Ready" in 2 keys and 0 wrong options.
- The key is not the only option of its form. Examples: the only option with a reason, the only one
  without "(default)", the only one in which nothing happens.
- The key is not the convergence centre of its options. Make a wrong option share as many words with the
  others.
- The key does not repeat stem words that no wrong option repeats (GATE 4 and the audit).

### D4. Across the quiz or the pool

- Test each fact one time.
- No question gives the answer to another question through its stem, its options or its key. Check every
  pair. Found: Q5 and Q9 gave the Released state of Q12; the key of Q16 gave Q17; "always" in Q7 gave Q15.
- No question repeats a question of an earlier pool (GATE 10, 8 pools). No wrong option repeats a wrong
  option whose feedback an earlier pool gave (Q18 and the Week 09 "SSH key" option).
- Keep the questions of one pool at the same difficulty.
- Do not copy a practice question and change only the names or values.
- For a random draw, calculate the chance that one quiz holds both questions of a pair:
  1 - C(N-1-k, n-1) / C(N-1, n-1).

### D5. Correctness and proof

- Run all the code. Each key has a proof: the live lab log, a probe run on the live cluster, or the
  Kubernetes documentation. Write the proof map in the report (the question and its log line).
- Run each new or changed scenario on the cluster before you keep it. Use the exact names of the stem
  (for example the class `fast`, not `manual`).
- A lecture slide can itself be wrong. Fix the deck, not only the quiz.

### D6. Feedback

- WHY gives the reason for the correct option.
- IF gives one mistake for each wrong option, in the order of `a[1:]`. The builder gives it the delivered
  letter. Check the letters after each rebuild.
- The feedback names no slide, week, deck or lecture.
- The feedback is also correct for the edge cases (for example a static PV of a WaitForFirstConsumer class).

### D7. Platform rules

- The upload file cannot shuffle the options, so balance the keys: 5 A, 5 B, 5 C and 5 D (GATE 8).
- No run of more than 3 equal letters (GATE 8b; the builder limit is `run_limit=3`).
- GATE 8c:
  - each letter is the key 2 or 3 times in each half of the quiz;
  - no two letters alternate over 5 questions;
  - no ABCD or DCBA run;
  - no block of 3 letters that repeats immediately.
- Give each question a neutral title: `clo835-eNN-001 topic`, with lowercase letters and spaces in the topic.
- Use no `<`, `>` or `&` in a stem or an option. Blackboard reads the text as HTML, and `<none>` broke Q12 of
  Week 09 ("Content Error"). Quotes are safe, and the QTI packer escapes the XML.

### D8. The quiz builder (`build_easy20_wNN.py`)

- GATE 1 to 6 come from `build2.verify`: self-contained, fact, length, answer leak, structure, and no pair
  that gives an answer to another.
- GATE 7 of `build2.py` (no fact in two pools) is not called. GATE 10 (earlier pools) does that job.
- GATE 8 letters 5 each; GATE 8b runs; GATE 8c halves and patterns; GATE 9 longest and shortest 4 to 6.
- GATE 11 feedback complete; GATE 12 logical order kept; GATE 13 neutral titles; GATE 14 no HTML character.
- When a gate fails, the builder writes nothing.

### D9. The audit (`audit_easy20_wNN.py`)

It reads only the delivered files: the upload file, the key, the titles and the ZIP. It checks:
- 20 rows of 10 fields, one correct option, no banned option, and no "not" in a stem;
- the letters, the runs and the length guesses (a length guess with ties shared must be 6.0 of 20 or less);
- the leaks (words of 3 or more letters, plurals folded, no trailing period) and the pairs at risk;
- the key records, the ZIP items and the titles.

### D10. Cue simulations

Run `python3 -I tools/quiz_cue_sim.py <upload file>`. It exits 1 when a strategy scores more than 30 %
(6.0 of 20), with ties shared. Its strategies:
- always A, B, C or D;
- the longest, the shortest, the most words, the fewest words, the middle length;
- the most words shared with the stem;
- the convergence centre, raw and stemmed, and the odd one out.

Also look for a word that only wrong options have, or only keys have, across the quiz (D3). The tool does
not check this.

### D11. The review loop

1. Build, pack, audit and simulate. All must pass.
2. Give the quiz to a fresh independent reviewer (a new subagent). Give it the rules, the files, the course
   content, the proof logs and the earlier pools. Ask for MUST-FIX and SHOULD-FIX lists.
3. Apply every finding. Prove each new scenario live. Build, audit and simulate again.
4. Do the next round with a new reviewer, because a fix can make a new give-away, cue or second correct
   option.
5. Stop at a round with 0 MUST-FIX and 0 SHOULD-FIX. When only some questions changed in the last round,
   that round can check those questions and their give-aways with all the others.
6. Write the counts of each round in the report.
   - Week 09: 20, 15, 8, 4, 1, 0.
   - Week 10: 13, 9, 8, 7, 7, 6, 5, 3, 3, 2, 0.

### D12. Blackboard delivery of a quiz

- For a test, use "Upload questions from file" with the tab-delimited `.txt` file.
- For a question bank, import the QTI 2.1 ZIP: Course Content, Details & Actions, Question banks, Manage
  banks, the plus icon, Import from QTI 2.1 package. A bank imports only a ZIP or a QTI package.
- Neither file carries the points. Ultra gives 1 point to each question. Use Bulk Edit Points.
- Show only the grade until all students finish. Show the correct answers and the feedback after the due
  date, never "after submission" in a shared window.
- Auto post shows the score at the moment of the submit. For an exam window, set auto post to off, and post
  all grades after the window.
- After the quiz, read the statistics of each question. Review a question when:
  - fewer than 30 % of students answer it correctly;
  - more than 95 % of students answer it correctly;
  - its discrimination is low or negative.

---

## Part E. Practical work in the AWS Learner Lab

### E1. The environment (verified 2026-11-10 unless a date is given)

- Account 499333804030, role `voclabs`, region `us-east-1`. The user starts the lab and gives the
  `aws sts get-caller-identity` output.
- Use the local AWS configuration. Never copy, show or store a key.
- The key pair `Maziar` exists, with the fingerprint `6e:c1:64:a7:ab:56:de:c9:00:3f:f9:56:7e:d0:92:57`. It
  matches `~/.ssh/mazSeneca`. The key pair `vockey` also exists.
- Instance sizes (`run-instances --dry-run` with the Ubuntu 26.04 AMI):
  - allowed: `t3.medium`, `m5.large`, `r8i.large`, `c7i.large`;
  - blocked: `m5.xlarge`, `t3.xlarge`, `r8i.xlarge`. The ceiling is 2 vCPU.
- At most 9 running instances (verified 2026-10-27). Above 9, the lab stops the new instances. So run at most
  3 lab clusters at the same time. The account attribute `max-instances` shows 20, but the lab limit is 9.
- `aws eks list-clusters` is allowed, and it shows no cluster. The create of a cluster is not tested.
  Students have no EKS, so no lab or project uses EKS.
- The pricing API is denied. Only `LabRole` and `LabInstanceProfile` exist, and the lab blocks IAM creation.
- The credentials expire after 4 hours.

### E2. Permission

- Use AWS only when the prompt of the user allows it. The approval of one prompt does not apply to the next
  prompt.
- Destroy all the infrastructure after the test, in the same task. Check that nothing stays.

### E3. The live test protocol of a lab

1. Copy the repo folder of the week to a sandbox folder in the scratchpad. Never run Terraform in the repo,
   because the state files must not enter the repo. Run `terraform validate` here.
2. Run `terraform -chdir=<sandbox> init`. Then run `apply`, and answer as a student: `Maziar`, then `yes`.
   - Through a pipe, wait before each answer, because Terraform reads stdin in blocks:
     `(sleep 10; echo Maziar; sleep 40; echo yes) | terraform -chdir=<sandbox> apply`.
3. Connect with `ssh -i ~/.ssh/mazSeneca ubuntu@<master public IP>`, with a known_hosts file in the
   scratchpad.
4. Check `cloud-init status` (done) and the message of the day. Check that the master holds no cleanup
   script, and that the extra files on the master are the same as the repo files.
5. Wait for the 3 Ready nodes: `kubectl wait --for=condition=Ready node --all`.
6. Make the runner in the sandbox: `tools/instrument.py <localMachine.sh> <sandbox>/pass1.sh 0`. It shows
   each command and its exit code. Copy it to the master.
7. Run pass 1 at full speed. Read the whole output, and compare each comment and sample with it.
8. Run pass 2 on a new cluster (destroy, then apply again), with 3 s between commands. The lab has no
   cleanup script, so pass 2 cannot run on the cluster of pass 1.
9. No recovery test: `terraform destroy` is the recovery. Run the runner detached on the master
   (`nohup setsid bash pass.sh > pass.log 2>&1 &`) and wait for an end marker, so that an SSH break does
   not hide the result. Before each apply, count the running instances: above 9, the Learner Lab shuts
   down the new instance ("Client.UserInitiatedShutdown", Week 14 on 2026-11-11).
10. Do the probe runs for the quiz keys (D5). Then delete ALL probe objects (Pods, claims, PVs, classes,
    namespaces, StatefulSets, files). Check that the cluster is at its start state before a further pass.
    A probe Pod named `dnstest` made a lab pass fail on 2026-11-10.
11. Run a final pass with the final repo files. After each later text change, check that the commands of the
    last build are identical to the tested commands.
12. Destroy as a student: `(sleep 10; echo Maziar; sleep 40; echo yes) | terraform -chdir=<sandbox> destroy`.
    Check "Destroy complete! Resources: 15 destroyed.", 0 instances in any state, and 0 security groups of
    the week.
13. Write the result table in the report: each pass, its command count and its non-zero exits.

---

## Part F. Repositories, accounts and security

### F1. The course repo

- The path is `~/Documents/c/r/CLO835_Fall_2026`. The remote is
  `https://github.com/sojoudian/CLO835_Fall_2026.git`, and the branch is `master`. Check the path before
  each operation, because it moved two times.
- The user does the git part. Update the files only, and leave them uncommitted. Do not commit, and do not
  ask. Run `git push` only when a prompt names it for that work.
- The history was rewritten on 2026-11-05 to one commit, `ad93eb8`. A clone made before that date stops at
  `git pull` with exit 128. The cluster slide of every lab says `cd CLO835_Fall_2026 && git pull && cd WeekNN`
  (open item H1).
- The lab engine `lab_kubeadm.py` reads the Week 06 template from the repo. A builder that reads
  `HEAD:WeekNN/<file>` must accept the committed and the uncommitted form of the file.

### F2. Accounts and images

- Name only Docker Hub `maziar` and GitHub `sojoudian` in course material.
  - Copy another image first: `docker buildx imagetools create -t maziar/X:tag SRC`.
  - Copy another repo as a fork.
- Never use `luksa/kubia`. Use `maziar/kubia`.
- Check that the tag exists before you name an image. Docker Hub on 2026-11-10:

| Image | Tags |
|---|---|
| maziar/kubia | v1, v2, 0.1, latest (v9 must stay absent) |
| maziar/kubia-pet | latest |
| maziar/alpine-curl | latest |
| maziar/alpine-git | latest |
| maziar/curl | latest |
| maziar/fortune | args, env |
| maziar/hpa-example | latest |
| maziar/flannel | v0.28.10 |
| maziar/flannel-cni-plugin | v1.9.1-flannel3 |
| maziar/local-path-provisioner | v0.0.37 |
| maziar/metrics-server | v0.7.1 |

- `maziar/kubia` is node:24-alpine. It has wget, but no curl and no bash.

### F3. Security

- Before anything enters a public repo, scan it for these items:
  - the home IP address;
  - `/Users/` paths;
  - `.ssh/` paths;
  - the user name and the email;
  - an AWS key.
- Never enter a real credential, and never sign in for the user.
- Never reproduce an AWS key. The transcript of 2026-10-31 holds Learner Lab keys; never copy them.
- `a1.zip` and `a1/` hold student data. Never put them in a public repo.
- A reference repo of the user is the whole model. Read all of it.

### F4. A rubric line must be runnable

Before an assignment or a lab text is released, build a table:
- one row for each rubric line or `Run` item;
- one column for the exact command or file that earns it.

An empty cell is a defect. Then check the order of the steps.

### F5. Git authorship

- Add no Claude attribution to a commit or a PR. Never change the git identity.
- The identity is `maziar <sojodyan@gmail.com>`. Show a bad-author commit to the user; do not rewrite it.

---

## Part G. Blackboard Ultra and the course

### G1. Lab item names

| Lab | Blackboard item |
|---|---|
| Lab Week 05 | `Lab03 - 2.5%` |
| Lab Week 06 | `Lab04 - 2.5%` |
| Lab Week 09 | `Lab05 - 2.5%` |
| Lab Week 10 | `Lab06 - 2.5%` (due Sat Nov 21, 2026, 11:59 PM) |

`Labs/LabNN.txt` covers Week NN+1. Check the item name before you name a lab number.

### G2. Lab items

- A lab item is an assignment: "File upload and Text entry", 100 points, 1 attempt, grades posted by hand.
- Paste the Blackboard lab text of C7. Update it only after the repo holds the matching lab.

### G3. The schedule (Fall 2026)

| Week | Topic |
|---|---|
| 01 | Docker Introduction |
| 02 | Docker Image Management |
| 03 | Docker Networking, Storage and Security |
| 04 | Kubernetes Introduction |
| 05 | Pods and ReplicaSets |
| 06 | Services and Deployments |
| 07 | Volumes |
| 08 | Study Week |
| 09 | PVs and Kubernetes in EKS |
| 10 | StorageClasses and StatefulSets |
| 11 | Exam and Mock Exam |
| 12 | ConfigMaps and Secrets |
| 13 | RBAC and EKS |
| 14 | HPA and project presentation |
| 15 | Project presentation |

The syllabus row of 12/9 still says Helm. Week 14 and Week 15 both say "Project presentation" (the text of
the user, 2026-10-31).

### G4. Grading text for students

- The feedback column states only where the student lost marks. Use no praise, no tips and no summary.
- Write one short clause for each lost item, in the form "The <part> part: missing <the screenshot, output
  or explanation>."
- For a wrong answer, write "the explanation is incorrect (<what it should be>)."
- Write "—" for full marks.
- Deduct only for a rubric gap, not for a typing mistake. Verify a claim before you present it.
- For a live demo or a presentation, write only what the professor saw. Invent no detail.
- Keep integrity notes and notes for the professor in a separate block.

---

## Part H. Open items (2026-11-10)

1. The `git pull` line of the cluster slide fails in a clone made before 2026-11-05 (all labs).
2. `Lab_week10_Blackboard_Submission_v4.md` says "control-plane node" 4 times and "control-plane pods" one
   time. C7 asks for "master node" and "control-plane Pods".
3. Lecture v11 slides 21 and 23 say that the provisioner "makes" a directory. The lab says "creates".
4. Lab Week 10 v4 does not practise these lecture topics, because of the limit of 40 commands:
   - a Pending claim with WaitForFirstConsumer;
   - the claim retention policy;
   - the scale-down order;
   - the access modes other than ReadWriteOnce;
   - the SRV name form.
5. The Week 07 lab v3 changes have no live test.
6. These images have only the tag `latest`: `maziar/alpine-curl`, `maziar/alpine-git`, `maziar/kubia-pet`,
   `maziar/curl`, `maziar/hpa-example`.
7. The course repo has uncommitted changes in Week07 and Week10. GitHub holds lab v3 of Week 10.
8. Weeks 04, 05, 06, 07, 09, 10 and 14 apply the `flannel-io` manifest URL. Only Weeks 12 and 13 use
   `maziar/flannel`.
9. The Week07 repo folder holds 9 files, because `local-path-storage.yaml` is in it.
10. Week 12 lab v7 (2026-11-11) has no cleanup script: `make_repo_folder(..., None, ...)`, Step 6 only
    `terraform destroy`. The repo change is not committed yet (HEAD 5b97e4f still has `cleanup_lab12.sh`). The
    lab and live checks of `gate_week12.py` now want no cleanup script and pass 2 on a new cluster.
11. The Week05 lab has Step 0 to Step 13.

---

## Appendix. Commands

These are templates. Use them for a NEW version, or before a delivery. Each line names the Week 10 files only
as an example. Run them from the project root, because the builders use relative paths.

```bash
P=/Users/maziar/Downloads/k8s_week3

# Deck: build a new version, then export, set the PDF info, run the gate and make page sheets
$P/.venv/bin/python $P/build_week10_lab_v5.py --no-repo
SHEETS=<scratch folder> $P/tools/deck_pipe.sh Week10 Lab_week10_v5 "CLO835 Week 10 Lab: Persistent Storage and StatefulSets" lab

# Quiz: build with the gates, pack, audit, simulate (these overwrite the outputs of that quiz)
Q=$P/quiz_pool_src; D=$Q/Quiz_W10_Easy20
$P/.venv/bin/python -I $Q/build_easy20_w10.py
$P/.venv/bin/python -I $Q/qti_pack.py $D/Quiz_W10_Easy20_Blackboard.txt $D/Quiz_W10_Easy20_QTI21.zip \
  "CLO835 Easy quiz - PersistentVolumes, StorageClasses and StatefulSets" clo835-e10 $D/Quiz_W10_Easy20_Titles.txt
$P/.venv/bin/python -I $Q/audit_easy20_w10.py
python3 -I $P/tools/quiz_cue_sim.py $D/Quiz_W10_Easy20_Blackboard.txt

# Lab live test: the runners go to the sandbox, not to the project
S=<sandbox folder>
python3 $P/tools/instrument.py ~/Documents/c/r/CLO835_Fall_2026/Week10/localMachine.sh $S/pass1.sh 0
python3 $P/tools/instrument.py ~/Documents/c/r/CLO835_Fall_2026/Week10/localMachine.sh $S/pass2.sh 3

# AWS checks that create no resource
aws sts get-caller-identity
aws ec2 run-instances --dry-run --image-id <ami> --instance-type m5.large --key-name Maziar --count 1
```

The canonical files of each week are in the memory index (`MEMORY.md`) of this project.
