# Report: Delete the Old Week 07 and Week 10 Decks
**Date**: 2026-11-10
**Sequence**: #02 for the day

## Summary
The user asked: "delete the old versions of the powerpoints". I moved the 22 old .pptx files of the folders Week07 and Week10 to the macOS Trash. Each folder now has only the current lecture deck and the current lab deck.

## What Changed
Moved to the Trash (with `/usr/bin/trash`):

- Week07 (9 files):
  - Lab_week07_v1.pptx
  - Lab_week07_v2.pptx
  - Lecture_week07_v6.pptx
  - Week07_lab_style_v1.pptx
  - Week07_lab_style_v2.pptx
  - Week07_lab_style_v3.pptx
  - Week07_lab_style_v4.pptx
  - Week07_lab_style_v5.pptx
  - week7_old.pptx (the user's old file, the source of v6)
- Week10 (13 files):
  - Lab_week10_v1.pptx
  - Lab_week10_v2.pptx
  - Lecture_week10_v8.pptx
  - Lecture_week10_v9.pptx
  - Week09_lab_style_v1.pptx
  - Week09_lab_style_v2.pptx
  - Week09_lecture_style_v2.pptx to Week09_lecture_style_v7.pptx (6 files)
  - Week09.pptx (the source of the old Week 10 lecture)

Kept:

- Week07/Lecture_week07_v7.pptx
- Week07/Lab_week07_v3.pptx
- Week10/Lecture_week10_v10.pptx
- Week10/Lab_week10_v3.pptx

## Technical Details
- Scope: the folders Week07 and Week10, because this conversation is about these two weeks. I did not touch the other week folders.
- Scope: .pptx files only. The old PDFs, the old Blackboard .md files and the old localMachine scripts stay.
- Method: the Trash, not a permanent delete. Finder "Put Back" restores each file.
- Check before the delete: the current builders do not read an old deck.
  - `build_week07_lecture_v7.py` and `build_week10_lecture_v10.py` read only `Week12/Lecture_week12_v6.pptx`.
  - `build_week07_lab_v3.py` and `build_week10_lab_v3.py` name an old deck only in the docstring.
- The course repo folders `CLO835_Fall_2026/Week07` and `Week10` have no .pptx file. I did not change the course repo.

## Results
- `/usr/bin/trash` exit code 0.
- A `find` for .pptx files now shows only the 4 kept decks.

## Issues / Notes
1. These old builders now fail, because their input decks are in the Trash: `build_week07.py`, `build_week07_lab_v1.py`, `build_week07_lab_v2.py`, `build_week07_lecture_v6.py`, `build_week10_lab_v1.py`, `build_week10_lab_v2.py`, `build_week10_lecture_v8.py`, `dedup_lectures.py`, `retarget_accounts.py`, `retarget_kind.py`, `fix_outline_week15.py`.
2. `Week07/Week07_lab_style_v1.pptx` had a second hard link in a different folder. That other copy stays.
3. The old PDFs stay in Week07 (6 files) and Week10 (8 files).
4. The Trash keeps the files until the user empties it.
