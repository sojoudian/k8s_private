# Report: Week 06 lecture audit against the Week 05 standard
**Date**: 2026-10-14
**Sequence**: #01 for the day

## Summary
I audited `Week06/Week06_lecture_style_v5.pptx` with the same checks that I applied
to the Week 05 lecture. The deck passes the mechanical checks. It fails the
content and the image checks. I found 14 defects. Three of them are broken
`kubectl` commands. A student who copies one of these commands gets an error.
I made no change. The audit is read-only.

## What Changed
- Created `reports/report-2026-10-14-01-week06-lecture-audit.md`. No other file changed.

## Technical Details
Checks applied, with the tool used:
- Slide size, slide count, hidden slides, typefaces, font colours, shape fills,
  float EMU coordinates, footer text and footer sequence: python-pptx.
- Effective image resolution: image pixel size divided by the placed size.
- Visual inspection: LibreOffice to PDF, then `pdftoppm` to PNG, 10 slides read.
- Command correctness: a text sweep for `kubectl`, `apiVersion` and image names.

The palette check reads XML only. It cannot see a colour inside a raster image.
This is why it reported zero off-palette colours while the screenshots carry
green, orange, magenta and purple. I record this as a limit of the checker.

## Results

### Pass
| Check | Result |
|---|---|
| Slide size | 13.333 x 7.500 in |
| Typefaces | Calibri 355 runs, Consolas 46 runs. No third typeface. |
| Float EMU coordinates | 0 |
| Off-palette colour in XML | 0 |
| Footer present | on all 41 slides |

### Fail - broken commands (a student copies these)
1. Slide 12 shows `kubectl get pods –selector app=App1`. The character before
   `selector` is an EN DASH (U+2013). The command needs two hyphens.
2. Slide 24 shows `kubectl scale deploy nginx-deployment --replicas=3 deployment`.
   The last word is a stray. kubectl reads it as a second resource with no name.
3. Slide 36 shows `kubectl exec -it kubia-3inly bash`. kubectl needs `--` before
   the command since version 1.18.

### Fail - house standard
4. The footers read `/ 71` on a 41-slide deck. The sequence is 1 to 10, then 16,
   17, then 22 to 49, then 71. It is the source deck numbering.
5. Slide 13 is visible. Version v3 hid it. The source `Week6.pptx` hides it.
   Versions v4 and v5 un-hid it.
6. 33 of the 41 slides carry a third-party screenshot. Week 05 uses native
   diagrams in house colours.
7. Slide 22 carries two third-party watermarks in the image: `DevOps Mojo` and
   `Ashish Patel`.
8. Slide 22 holds an image from y=0.01 in to y=7.22 in. It covers the title band
   and the footer band. The bottom labels are clipped.
9. Six images are below 110 DPI. The worst is slide 21 at 71 DPI, and it is a
   WMF file. WMF is a legacy Windows format. It renders badly on macOS and in
   Keynote.
10. Slide 36 holds a curly apostrophe (U+2019) in a Consolas terminal block.
11. The file is 10.5 MB. The Week 01 reference deck is 1.37 MB.

### Fail - content
12. Slide 3, the Course Outline, puts ConfigMaps at Week 11 and the Exam at
    Week 12. The syllabus puts the Mid-Term on 11/11 and ConfigMaps on 11/18.
    The exam comes first. The Week 05 outline uses a different design again.
13. The container image is mixed. Slides 4 and 24 use `nginx` with no tag.
    Slide 36 uses `kubia`. Week 05 uses `maziar/kubia` on every slide.
14. Slide 19 card 3 reads `(e.g. LoadBalancer and NodePort)`. It is a fragment of
    card 2, not a point of its own.

## Issues / Notes
- The XML palette check gives a false pass on a deck built from screenshots.
  Add a raster colour check before the next audit.
- The known hidden-slide regression is confirmed, not only reported.
- I made no change to any deck. The user asked for an audit only.
