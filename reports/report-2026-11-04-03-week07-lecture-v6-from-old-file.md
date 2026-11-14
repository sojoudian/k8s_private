# Report: Week 07 lecture v6, built from the old file
**Date**: 2026-11-04
**Sequence**: #03 for the day

## Summary
You asked for a lecture based on your old file `Week07/week7_old.pptx`. The new lecture
is `Week07/Lecture_week07_v6.pptx`, with a PowerPoint PDF. It has 15 slides: the 14 slides
of the old file in the same order, and the Course Outline after the agenda. Each point of
the old file is on a slide. The old pictures are now native house diagrams and house
terminals. The text is in ASD-STE100, and the facts follow the Kubernetes v1.35 documents.

## What Changed
**Created**
- `build_week07_lecture_v6.py`: the builder. It is guarded, it reads its inputs only, and it
  refuses to overwrite its output.
- `Week07/Lecture_week07_v6.pptx` (0.16 MB) and `Week07/Lecture_week07_v6.pdf` (PowerPoint
  export, 15 pages).

**Not changed**
- `Week07/week7_old.pptx`, `Week07/Week07_lab_style_v1.pptx` to `v5`, the lab, and the course
  repository. Nothing was committed or pushed.

## Technical Details

### Inputs
- `Week07/week7_old.pptx`: the content. The builder checks its 14 titles and stops if the
  file changes.
- `Week12/Lecture_week12_v6.pptx`: the cover, the agenda frame and the Course Outline, as
  in the Week 13 lecture builder.
- The engine `build_week08.py` and the helpers of the Week 09, 12 and 13 lecture builders.

### Slide map

| Old slide | New slide | What the new slide holds |
|---|---|---|
| 1 Cover | 1 | Same title, in two lines. "Week 7 · Lecture" |
| 2 Agenda | 2 | The 5 old items, with the same hierarchy, and 3 items for the slides that the old agenda did not name |
| - | 3 | Course Outline. Week 7 is the blue tile |
| 3 K8s Volumes | 4 | All 7 points. v5 had removed 6 of them |
| 4 Volumes | 5 | All 7 points |
| 5 Volumes vs PersistentVolumes | 6 | All 9 points. "won't be discussed further" is now "The Week 10 lecture teaches PersistentVolumes in detail" |
| 6 Volume Types | 7 | The same 7 types, with the v1.35 status of each |
| 7 Volume Types, Cont | 8 | The same types and groups, with the v1.35 status. fc and local join the old iscsi |
| 8 Volume Type: emptyDir | 9 | All 5 points, plus the emptyDir manifest of the lab |
| 9 Volume Lifecycle | 10 | All 6 points |
| 10 Using GitRepo Volume | 11 | The 3-step diagram, drawn natively. v5 had removed it |
| 11 Pod Manifest with GitRepo | 12 | The manifest of the lab, the 4 old notes, and a note for the emptyDir |
| 12 Managing configuration | 13 | All 8 points |
| 13 Persistent Volumes: Amazon EBS | 14 | The 2 old points as history, then the CSI method and a PVC manifest |
| 14 Using NFS Volume | 15 | The same manifest and 4 notes |

### Facts and their sources
Source: the Kubernetes "Volumes" page for v1.35, v1.33 and v1.32, downloaded on
2026-11-04. The course cluster runs v1.35.10.
- gitRepo: "deprecated and is disabled by default" in v1.35. The page recommends an init
  container that clones into an emptyDir. The `GitRepoVolumeDriver` feature gate enables it.
- In-tree drivers removed: awsElasticBlockStore v1.27 (`ebs.csi.aws.com`), azureDisk v1.27
  (`disk.csi.azure.com`), gcePersistentDisk v1.28 (`pd.csi.storage.gke.io`).
- Not in the v1.35 page: cinder, cephfs, glusterfs, rbd, vsphereVolume, flocker, quobyte,
  photonPersistentDisk, scaleIO. The v1.33 page gives the removal versions of the first five.
- flexVolume: deprecated since v1.23.
- A volume with no type becomes an emptyDir. The data of an emptyDir stays after a
  container crash, and goes when the Pod leaves the node.

### Decisions
1. **Old pictures.** Slide 10 of the old file is a figure from a book, so it is a
   third-party picture (section 13). Slide 11 now draws the same 3 steps in the palette,
   with an init container in place of the gitRepo volume. Slides 11, 13 and 14 of the old
   file are YAML pictures. They are now house terminals.
2. **Manifests.** The emptyDir and the git manifests are the live-tested manifests of lab
   Week 07 (steps 4 and 6), so the lecture and the lab agree. The git manifest clones
   `sojoudian/kubia.git`, which exists. v5 named `sojoudian/kubia-website-example.git`, which
   returns 404. The EBS and NFS manifests use `maziar/kubia:v1` in place of `image: ...`.
3. **Volume type slides.** In June you chose to keep the old Volume Types list and the
   gitRepo diagram (memory `project-week07-deck`). The rules of 2026-10-27 require correct
   facts and current API (section 14) and no third-party picture (section 13). So v6 adds the
   v1.35 status to each type, and it redraws the diagram.
4. **Words.** The text follows the word choices of the Week 12 gate: "store" not "keep",
   "methods" not "ways", "settings" not "parameters", and no "we". The emptyDir steps are
   now instructions ("Start with...", "Add...", "Mount...").
5. **One fact on slide 4.** "Unlike Network, processes and CPU, filesystems are unique per
   container" is now "The containers of a Pod share the network, but not the filesystem".
   Containers in a Pod do not share the process namespace by default.

### Independent review
One reviewer agent read the deck, the PDF pages, the old file and its pictures, the builder,
the lab script, the rules and the saved documents. It did not see my notes. It found 13
points. I checked each one against the files.

**Fixed (10)**
1. Slide 4 said that Kubernetes removes a volume when the Pod ends. The data of a persistent
   volume stays. Now: Kubernetes mounts the volume when the Pod starts, and unmounts it when
   the Pod ends.
2. Slide 10 said that Kubernetes destroys a volume with the Pod. Now: Kubernetes deletes an
   emptyDir volume with the Pod, and only unmounts or detaches remote storage. A volume is
   created when Kubernetes starts the Pod on a node. "mostly" is gone.
3. Slide 8: `local` is a disk, a partition or a directory of the node, through a static
   PersistentVolume only.
4. Slide 12: `sojoudian/kubia` has no `index.html`. The card now says that nginx serves the
   files of the repository, for example `/app.js`, as in the lab.
5. One word for one meaning: slide 8 says "removed the in-tree drivers", as slide 7 does, and
   "Other volume types".
6. Active voice: "Kubernetes deprecated ..." on slides 7, 8 and 11, and "where Kubernetes
   mounts it" on slide 9.
7. Slide 14: a new bullet says that the manifest needs the EBS CSI driver, for example on
   Amazon EKS, and that the lab uses the StorageClass `standard`.
8. Slide 15: the card names `192.168.0.55` as an example address.
9. Slide 2: the agenda adds "A Git repository in a volume", "NFS" and "Managing
   configuration".
10. Slide 15: the terminal and the cards end at the same height. The builder comments now
    name lab Steps 1 and 3.

**Kept (3)**
- The lifecycle points on slides 4 and 10. The old file states them on both slides. v5
  removed the slide 4 bullets, and you asked for the old content. Rule 14 permits a second
  statement when it is necessary. The two slides use different words.
- 9 pt terminal text on slides 9, 12 and 14. The gate permits 9 to 14 pt, and v5 used 9 pt
  for the same manifests of 25 or more lines. A larger size needs a split of these slides.
- The indent of a wrapped bullet line. The shared helper `bullets()` of the Week 13 builder
  sets it for all the current lectures.

The reviewer confirmed: the removal versions, the 3 CSI driver names, flexVolume v1.23,
gitRepo disabled by default, the 9 types that v1.35 does not include, the 3 image tags on
Docker Hub, and the `master` branch of `sojoudian/kubia`.

### Checks
- The deck checks of `gate_week12.py`, run with `ROOT = "Week07/"` and the agenda line
  "managing configuration" added to the allowed repeats (as for the Week 12 agenda): 32 of
  32 pass. They
  cover the canvas, the size, the fonts in the deck and in the PDF, the footers, the whale,
  the bands, the DPI, 12 pt body text, 9 to 14 pt terminal text, duplicate titles and
  bullets, non-ASCII in Consolas, the replaced words, contractions, sentences over 25 words,
  banned images and paths, floats, the palette, the images, and the terminal fit in the PDF.
- The outline: the 16 tile texts and positions equal Week 12 v6. The blue frame is on
  Week 7, and the red frame is on Week 11.
- A rebuild in a sandbox gives the same 65 parts. A second run stops with "exists".
- I viewed all 15 pages of the PowerPoint PDF, and again each changed page after the review.

## Results
- `Week07/Lecture_week07_v6.pptx`: 15 slides, 16:9, Calibri and Consolas, 0 float
  coordinates, 2 images (logo and whale), 0.16 MB.
- `Week07/Lecture_week07_v6.pdf`: 15 pages, Calibri and Consolas only.
- Gate: 32 of 32 deck checks pass. Independent review: 10 of 13 points fixed, 3 kept with a
  reason.
- No server started, so no port is used.

## Issues / Notes
- The manifests did not run on a cluster in this work. The emptyDir and git manifests are
  the lab manifests that ran live on 2026-10-27. The EBS manifest needs the EBS CSI driver,
  which the kubeadm cluster does not have. The NFS manifest needs an NFS server.
- Slide 15 shows the same NFS manifest as Week 10 v9 slide 8. The old file had it too.
- The old file has no References slide, so v6 has none.
- The first two builds had two faults, found in the render: the terminals were off the
  slide, and the cover title ran under the logo. Both are fixed in the delivered file.
