# Report: Week 06 lecture repaired to the Week 05 standard
**Date**: 2026-10-14
**Sequence**: #02 for the day

## Summary
I repaired all 14 defects that the audit of this morning found in
`Week06_lecture_style_v5.pptx`. I also found and corrected one more defect while
I worked: the Ingress manifest used an API that Kubernetes removed in version
1.22. The result is `Week06/Week06_lecture_style_v6.pptx`, 41 slides. I replaced
30 third-party screenshots with native house diagrams and house terminals. The
file is now 0.93 MB, against 10.5 MB.

## What Changed
- Created `build_week06_v6.py` at the repository root. It is guarded, so an
  import writes nothing. It reads v5 and never writes it.
- Created `Week06/Week06_lecture_style_v6.pptx` (41 slides, 0.93 MB).
- Created `Week06/Week06_lecture_style_v6.pdf`.
- Created `reports/report-2026-10-14-02-week06-lecture-repair.md`.
- `Week06_lecture_style_v5.pptx` is unchanged.

## Technical Details

### The three broken commands
| Slide | v5 | v6 |
|---|---|---|
| 12 | `kubectl get pods –selector app=App1` | `kubectl get pods --selector app=App1` |
| 24 | `kubectl scale deploy nginx-deployment --replicas=3 deployment` | `kubectl scale deploy kubia --replicas=3` |
| 36 | `kubectl exec -it kubia-3inly bash` | `kubectl exec -it kubia-3inly -- bash` |

### The defect found during the repair
Slide 40 held the Ingress manifest as an image. The image showed
`apiVersion: extensions/v1beta1` and a `serviceName` / `servicePort` backend.
Kubernetes removed that API in version 1.22. The lab cluster runs version 1.35,
so the manifest fails. The slide now shows a house terminal with:

    apiVersion: networking.k8s.io/v1
    ...
        pathType: Prefix
        backend:
          service:
            name: kubia-nodeport
            port:
              number: 80

### The screenshots
30 slides lost a third-party screenshot and gained a native house diagram or a
house terminal. The builder draws each one from measured coordinates. I rendered
the deck to PDF, then to PNG, and read every changed slide. Two review rounds
were needed. The first round found an overlap on slides 18, 20, 27, 31 and 33,
text that ran out of the terminal on slide 32, and a tile that ran past the
right edge on slide 9. The second round found none.

A removed picture leaves its image part inside the file, because the
relationship still names it. The builder calls `slide.part.drop_rel()` for each
picture that it deletes. This is what takes the file from 10.5 MB to 0.93 MB.

### The course outline
Slide 3 put ConfigMaps at Week 11 and the exam at Week 12. The syllabus holds
the Mid-Term on 11/11 and ConfigMaps on 11/18, so the exam comes first. The
grid now follows the schedule of 2026-07-15: a Study Week at Week 8, the exam at
Week 11, ConfigMaps at Week 12, HPA at Week 14 and the project at Week 15. The
Week 6 cell is filled in house blue and carries the word "Today".

### The language
I rewrote 22 bullets into ASD-STE100. Examples: "b/w" to "between", "fwding
rules" to "forwarding rules", "a bunch of iptables rules" to "a set of iptables
rules", "Ips ... everytime" to "A new Pod gets a new IP address".

One bullet set was wrong, not only informal. Slide 25 said "Services are created
by KubeProxy". The API server creates the Service object. Kube-proxy writes the
forwarding rules.

Slide 38 described the old screenshot by colour ("Blue and Orange POD are on
same node"). The new diagram has no such colours, so I rewrote the four bullets
to describe what the new diagram shows.

## Results

| Check | v5 | v6 |
|---|---|---|
| Slides | 41 | 41 |
| Footer total | `/ 71` | `/ 41` |
| Footer sequence | jumps 1-10, 16, 17, 22-49, 71 | 1 to 41, in order |
| Hidden slides | none | 13, as the source deck has it |
| Typefaces | Calibri, Consolas | Calibri, Consolas |
| Off-palette colour | 0 in XML, many inside the images | 0 |
| Float EMU coordinates | 0 | 0 |
| Non-ASCII in a Consolas run | 4 | 0 |
| Third-party screenshots | 33 slides | 0 |
| Third-party watermark | 2 on slide 22 | 0 |
| Images below 110 DPI | 6 | 0 |
| WMF images | 1 | 0 |
| Shapes outside the frame | 1 (slide 22) | 0 |
| File size | 10.5 MB | 0.93 MB |

Three images remain. All three are at 426 DPI or better:
- slide 1, the Kubernetes logo;
- slide 5, a photograph of shipping containers;
- slide 16, a photograph of a data centre.

None is a technical diagram, so none carries a third-party drawing style or a
watermark.

## Issues / Notes
- The XML palette check cannot see a colour inside a raster image. It gave v5 a
  false pass. The geometry check that I wrote for this repair
  (`scratchpad/geom.py`) catches the overlap class, and it now reports 0.
- The Week 06 LAB deck (`Week06_lab_style_v4.pptx`) is not audited and not
  changed. It may hold the same defects.
- The hidden slide 13 is hidden, not deleted. Its screenshot is replaced too, so
  the deck holds no third-party drawing even on a hidden page.
