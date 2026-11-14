# Report: Week 06 Lecture v7 — Repetition Removed
**Date**: 2026-10-14
**Sequence**: #07 for the day

## Summary
The user asked me to update the lecture content, to state a point two times at
the most, and to state it one time when one time is enough. I built
`Week06/Week06_lecture_style_v7.pptx` from v6. The deck goes from 41 slides to
34 slides. Seven slides go, nine slides lose their repeated bullets, two slides
get a new title, and one slide loses two of its five rows. No fact is lost.

## What Changed
- **Created** `build_week06_v7.py` at the project root. It is guarded by
  `if __name__ == "__main__"`, it reads v6, and it never writes v6.
- **Created** `Week06/Week06_lecture_style_v7.pptx` — 34 slides, 0.86 MB.
- **Created** `Week06/Week06_lecture_style_v7.pdf` — 2.0 MB.
- **Unchanged**: `Week06_lecture_style_v6.pptx`, 935 205 bytes, 12:23.

## Technical Details

### Seven slides go
Each one states only facts that another slide states.

| v6 slide | Title | Where its facts live now |
|---|---|---|
| 9 | Deployment Strategy | slide 7 and slide 8, which teach each strategy |
| 17 | Exposing Containers in Kubernetes | merged into slide 16 |
| 20 | How can I access the POD? | the question is slide 16, the answer is slide 27 |
| 21 | Introducing Kubernetes Services | slide 18 and slide 19 |
| 25 | Kube-Proxy | merged into slide 26 |
| 28 | Service Type: NodePort | slide 27 and slide 29 |
| 32 | Service Type: ClusterIP | slide 31, slide 18 and slide 29 |

The three pairs of slides that shared one title are gone. No two slides of v7
carry the same title.

### Nine slides lose repeated text

| v6 slide | Change |
|---|---|
| 16 | takes the three challenges of slide 17: a Pod can fail, a client outside has no route, a client cannot know which Pod |
| 18 | drops 2 bullets. The diagram and its caption teach the tiers |
| 19 | drops row 3 (DNS, now slide 36 only) and row 5 (one stable address, now slide 18 only). The three rows re-centre |
| 23 | drops the 3 sub-bullets. The 3 numbered tiles beside them say the same |
| 26 | takes the 4 facts of slide 25, and keeps its own diagram |
| 27 | drops `(we can connect to any node on that port...)`, which repeats the bullet above it, and drops the kube-proxy line |
| 31 | drops the caption that repeats its own bullet |
| 34 | drops the 2 bullets that slide 33 carries word for word |
| 37 | merges bullet 1 and bullet 2, which both named a list of IP addresses and ports |
| 38 | drops bullet 1 and bullet 2. Slide 26 teaches the cross-node fact |

### Two slides get a new title
- v6 slide 26, `How does it work?` becomes `Kube-Proxy`, because it now holds the
  whole subject.
- v6 slide 34, `Service Type: LoadBalancer` becomes `Why a Load Balancer?`,
  because slide 33 holds the type and slide 34 holds the reason.

### Fact counts, before and after

| Fact | v6 slides | v7 slides |
|---|---|---|
| A NodePort opens on every node | 6 | 2 |
| The port range is 30000-32767 | 5 | 1 |
| A Service gives one stable address | 6 | 2, as problem and answer |
| You cannot use a Pod IP address | 4 | 2, as problem and answer |
| kube-proxy writes iptables rules | 3 | 1 |
| A Service carries a DNS name | 6 | 1 in prose, 2 diagram labels |
| A ClusterIP answers inside only | 5 | 2 |
| port against targetPort | 3 | 2, and the second is a named-port example |
| A Service load balances | 4 | 1 |
| A LoadBalancer flows through a NodePort | 2, word for word | 1 |

Two facts stay at two mentions on purpose:
- `A ClusterIP answers inside the cluster only` — slide 19 needs it to explain
  why three ways reach the Service from inside. Slide 25 defines the type.
- `one stable address` and `you cannot use a Pod IP` — slide 15 states the
  problem, and slide 16 and slide 17 give the answer.

The only word-for-word repeat that remains is the `kubectl rollout` command set
on slide 6 and slide 9. Slide 9 is the command summary, so that repeat is the
purpose of the slide.

### Technique
- A slide deletion needs two steps. Remove the entry from `sldIdLst`, then call
  `prs.part.drop_rel(rId)`. python-pptx then drops the orphan parts at save.
- A bullet rewrite copies the XML of an existing paragraph as a template, so the
  run formatting of the house design survives.
- `trim_why_services()` groups the shapes of slide 19 by the top of each row
  background, deletes two groups, and shifts the rest to new tops.

## Results
- 34 slides, 0.86 MB, from 41 slides and 0.93 MB.
- Hidden slide: 12, which is `Services in the Traditional Environment`. v6 hid
  the same slide at index 13.
- Footers read `1 / 34` to `34 / 34`, in sequence.
- Fonts: Calibri 563 runs, Consolas 122 runs. No other typeface.
- 0 non-ASCII characters inside Consolas.
- 0 duplicate slide titles.
- Geometry: 0 real overflows. The checker reports 47 label boxes short by 0.02
  to 0.05 in; v6 reports 53 of the same. They are an artifact of the estimator
  padding, and PowerPoint grows a text box.
- Visual check: rendered to PDF with LibreOffice, then to PNG with `pdftoppm`.
  I read slides 15, 16, 17, 19, 21, 27 and 31. All are correct.

## Issues / Notes
- Slide 16 and slide 19 now carry two bullets beside a diagram, so the left
  column holds white space. The balance is acceptable, and the diagram carries
  the slide.
- The PDF holds 33 pages, not 34, because LibreOffice drops the hidden slide.
  A PDF page N answers to slide N+1 from page 12.
- `Week06_lab_style_v4.pptx` (31 slides) is still not audited. The source holds
  `DNS in K8s` three times inside the lab partition, so it needs the same pass.
