# Report: Week 06 Lecture — Repetition Analysis
**Date**: 2026-10-14
**Sequence**: #06 for the day

## Summary
The user asked if `Week06_lecture_style_v6.pptx` repeats points and facts. The
answer is yes. I read all 41 slides, and I counted each fact. Eleven facts appear
on three or more slides. Three pairs of slides carry the same title. Two bullets
are word-for-word duplicates. The repetition comes from the source deck
`Week06/Week6.pptx`, not from the v6 rebuild. No file was changed.

## What Changed
- Nothing. This is a read-only analysis.
- **Created** this report only.

## Technical Details

### Method
1. Extracted the text of every shape of every slide with python-pptx, and
   recursed into the groups.
2. Compared every pair of bullets with `difflib.SequenceMatcher`, over the
   normalised text, at a ratio of 0.80 and higher.
3. Counted the slide titles.
4. Repeated steps 2 and 3 on the 71-slide source `Week06/Week6.pptx`, to find
   who introduced each repeat.

### Finding 1 — three pairs of slides share one title

| Title | Slides |
|---|---|
| Service Type: NodePort | 27 and 28 |
| Service Type: ClusterIP | 31 and 32 |
| Service Type: LoadBalancer | 33 and 34 |

The source deck holds the same three pairs, at slides 36/37, 40/41 and 42/43.
The source also holds `DNS in K8s` three times, at 66, 67 and 68, but those three
slides went to the lab deck.

### Finding 2 — two bullets are word-for-word duplicates

Slide 33 and slide 34 both carry:
- `An external load balancer is allocated for the service`
- `In practice, it will often flow through a NodePort first`

Source slides 42 and 43 hold the same two duplicates. Rule R1 of the build keeps
the source text verbatim, so the v6 rebuild carried them forward.

### Finding 3 — the "why do we need a Service" block runs six slides

Slides 16 to 21 all answer one question. They are source slides 25 to 30.

| Slide | Title | What it does |
|---|---|---|
| 16 | Exposing containers | asks the question |
| 17 | Exposing Containers in Kubernetes | asks the same question, with more parts |
| 18 | Services | answers it |
| 19 | Why Services? | answers it again, as a five-row list |
| 20 | How can I access the POD? | asks the question a third time |
| 21 | Introducing Kubernetes Services | introduces the Service a second time |

Titles 16 and 17 differ by two words.

### Finding 4 — fact frequency

| Fact | Slides | Count |
|---|---|---|
| A NodePort opens on every node | 20, 25, 27, 28, 35, 38 | 6 |
| A Service gives one stable address to a group of Pods | 16, 17, 18, 19, 21, 32 | 6 |
| A Service carries a DNS name | 15, 19, 21, 31, 32, 36 | 6 |
| A selector picks the Pods by label | 12, 15, 28, 29, 32, 37 | 6 |
| The node port range is 30000-32767 | 20, 27, 28, 35, 38 | 5 |
| A ClusterIP answers inside the cluster only | 22, 23, 31, 35, 38 | 5 |
| You cannot use a Pod IP address | 16, 17, 19, 32 | 4 |
| A Service load balances | 17, 19, 21, 28 | 4 |
| kube-proxy writes iptables rules on each node | 25, 26, 27 | 3 |
| port against targetPort | 28, 29, 32 | 3 |
| A LoadBalancer flows through a NodePort | 33, 34 | 2, verbatim |

Slide 27 states "a port on every node" twice, in two bullets that follow each
other:
- `That port is made available on all our nodes and anybody can connect to it`
- `(we can connect to any node on that port to reach the service)`

### Finding 5 — kube-proxy runs over three slides

- Slide 25, `Kube-Proxy` — `Kube-proxy writes forwarding rules on each node`.
- Slide 26, `How does it work?` — `Kube-proxy modifies IPTABLES on each node`.
- Slide 27, `Service Type: NodePort` — `Kube-proxy writes a set of iptables rules
  on each node`.

Slide 25 and slide 26 carry the same diagram shape: an API server above the
nodes, and an iptables box inside each node.

### Finding 6 — the rollout strategies run over three slides

- Slide 7, `Rollout Strategies: Rollout` — four steps, a to d.
- Slide 8, `Rollout Strategies: Recreate` — three steps, a to c.
- Slide 9, `Deployment Strategy` — both strategies, side by side.

Slide 9 holds no new fact. It is slide 7 and slide 8 in one picture.

### What the v6 rebuild did and did not do
The v6 rebuild fixed 15 defects: three broken commands, a removed Ingress API,
the footers, the hidden slide, and 30 third-party screenshots. It did not remove
a single slide, and it did not remove a single source bullet. The slide count
stayed at 41, because rule R1 keeps the source text. The repetition is therefore
untouched.

## Results
Yes, the deck repeats. The measured numbers:
- 11 facts on 3 or more slides.
- 3 pairs of slides with one title.
- 2 bullets duplicated word for word.
- 6 consecutive slides on one question.

Seven slides hold no fact that another slide does not already hold: 9, 17, 19,
21, 26, 32 and 34. A merge of those seven gives a 34-slide deck.

## Issues / Notes
- The repetition is **inherited**. Every duplicate above is in
  `Week06/Week6.pptx`. The rebuild did not add one.
- A merge breaks the footer numbering, which now reads `1/41` to `41/41`. A
  rebuild must renumber.
- Repetition is not always a defect in a lecture. Slide 35 is a summary table,
  and slide 10 is a summary of commands. A summary repeats on purpose.
- `Week06_lab_style_v4.pptx` (31 slides) is still not audited. The source holds
  `DNS in K8s` three times inside the lab partition.
