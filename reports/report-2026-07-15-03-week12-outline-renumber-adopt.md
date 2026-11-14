# Report: Adopt user's hand-edited Course Outline (slide 3) into Week12 lecture v2

**Date**: 2026-07-15
**Sequence**: #03 for the day

## Summary
The user hand-edited the Course Outline (slide 3) of `Week12_lecture_style_v2.pptx` — a week renumbering — and asked me to adopt it. I read the edited tiles from the screenshot, mapped them back through the deck's boustrophedon layout to sequential reading order, updated the slide-3 data, and rebuilt. The rebuilt slide 3 now matches the screenshot pixel-for-pixel in content and highlights.

## What Changed
- `wk12_content.json` slide 3 body — 8 of the 16 tiles retext'd (week renumber).
- `build_week12.py` (repo root) regenerated; `Week12/Week12_lecture_style_v2.pptx` + `Week12/Week12_lab_style_v2.pptx` rebuilt and redelivered (lab deck unchanged — no course outline in it).
- Memory: `clo835-course-schedule.md` rewritten to the 2026-07-15 schedule; `project-week12-deck.md` + `MEMORY.md` updated.

## Technical Details
- The edit: from row 3 on, weeks shifted +1 — Week 8→**09**, 9→**10**, this deck 10→**11** (BLUE, current), Exam 11→**12** (RED), 12→**13**, 13→**14**; old Week 14 "Helm Charts & Deployment Automation" replaced by **Week 15: Project presentation**; Week 14 tile now two lines "Week 14: K8s – HPA" / "Project presentation". Weeks 1–7, Study Week, Term End unchanged.
- The course_outline renders items in sequential reading order via a boustrophedon (snake) layout; I verified every one of the 16 tiles lands in the correct visual cell against the screenshot before and after.
- Highlight logic is content-based (`"configmap"+"secret"`→BLUE, `"exam"`→RED), so it auto-tracked to the new Week 11 / Week 12 tiles with no code change. 0 float coords; footers still 1/21.

## Results
- Slide 3 adopted exactly. Rendered at 130 dpi and compared to the user's screenshot: all 16 tiles match in text, order, wrapping, and the two highlights (Week 11 blue, Week 12 red).
- Only the lecture deck's slide 3 changed; everything else in both v2 decks is identical to before.

## Issues / Notes
- **Schedule revision recorded:** the user's outline moves ConfigMaps from Week 12 to **Week 11** and Exam from Week 11 to **Week 12**, drops Helm, and adds Project presentation to Weeks 14–15. This supersedes the 2026-07-06 schedule memory (now updated).
- **Cover-vs-outline mismatch (OPEN):** the outline now marks this deck as **Week 11**, but both v2 covers (and the v1 cover) still say **"Week 10 · Lecture/Lab"** with the "Week 10 feels like 100" tagline. Per "change only what was asked," I adopted slide 3 only and did NOT touch the covers. Flagged to the user with a recommendation to flip `WEEK_LABEL` to "Week 11" (one line, quick rebuild) — awaiting confirmation.
