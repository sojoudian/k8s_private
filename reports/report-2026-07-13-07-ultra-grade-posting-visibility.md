# Report: Ultra "Post grades automatically" timing + answer-key visibility for the timed exam
**Date**: 2026-07-13
**Sequence**: #07 for the day

## Summary
Answered whether students see their grade immediately or at the 10 PM deadline with "Post assessment grades automatically" ON, for the all-auto-graded (MC/MA/TF) CLO835 exam in a fixed 7-10 PM window. Verified via research (3 agents, high confidence, official Anthology + university guides): the grade posts IMMEDIATELY on submission; the due date does not withhold it. Also clarified that the correct-answer key is a separate control (Assessment results) that must not be set to "After submission" for a shared window.

## What Changed
- No exam files changed (this is Ultra test-settings guidance).
- Scratch only: `ultra_grade_posting.js` (3-agent research; agents completed research but failed the strict output schema - findings recovered from transcripts).
- This report + a new memory `reference-blackboard-ultra-grade-visibility`.

## Technical Details
- Confirmed behavior:
  - "Post assessment grades automatically" ON + all auto-graded questions => student sees the numeric grade the instant they submit, NOT at the due date, NOT when instructor posts. Toggle defaults ON for Ultra Tests.
  - The due date alone does NOT hide the grade; only the checkbox does.
  - To withhold scores until after 10 PM: turn the checkbox OFF before the test opens (grade stored but shows "Not graded"), then Gradebook > test column > Post > "Post all grades" after 10 PM.
  - Correct answers / feedback are separate (Assessment results section: Submission View, Automated question feedback, Question scores, Correct answers), each with a timing dropdown (after submission / after due date / after all grades posted / specific date). Default hidden. Ultra enforces feedback shows at or before correct answers.
  - INTEGRITY: never set correct answers or feedback to "After submission" in a shared window - it leaks the key to early finishers. Use "After the due date" or later.
- Recommendation given: for a clean sealed exam, turn OFF auto-post, keep answers hidden or "After due date", and Post all grades after 10 PM.

## Results
Delivered a definitive, sourced answer distinguishing the score release (immediate with auto-post) from the answer-key release (separate, default hidden), with exact steps for both the instant-feedback and fully-sealed options.

## Issues / Notes
- The research workflow's agents hit the StructuredOutput retry cap (wrapped answers in stray XML tags vs the strict additionalProperties:false schema). Findings were fully recovered from the agent transcripts; all three agreed. Lesson: keep verification schemas lenient (fewer required fields, no additionalProperties:false) for research agents that emit long prose.
