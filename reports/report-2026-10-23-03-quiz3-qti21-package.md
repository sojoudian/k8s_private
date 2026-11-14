# Report: Quiz 3 QTI 2.1 package

**Date**: 2026-10-23
**Sequence**: #03 for the day

## Summary

The Quiz 3 pool is now a QTI 2.1 package. Blackboard Ultra imports the package
into a question bank. The tab delimited .txt file cannot go into a bank, because
the bank import accepts a ZIP file or a QTI 2.1 package only. The package holds
100 multiple choice items and one manifest. An independent audit reads the ZIP
file and the answer key, and reports 0 errors.

## What Changed

- `quiz_pool_src/build_qti3.py` — new. It reads `Quiz03_Pool_Blackboard.txt` and
  writes the package.
- `quiz_pool_src/audit_qti3.py` — new. It is the independent audit. It opens the
  ZIP file and the key, and imports no question source.
- `quiz_pool_src/Quiz03_Pool_QTI21.zip` — new. It is the upload file, 72 935
  bytes, 101 members.

## Technical Details

Package layout:

- `imsmanifest.xml` at the ZIP root. The namespace is IMS Content Packaging
  v1.1. Each question is one `resource` of type `imsqti_item_xmlv2p1`.
- `items/clo835-q3-001.xml` to `items/clo835-q3-100.xml`.

Each item file holds one `assessmentItem`:

- The namespace is `http://www.imsglobal.org/xsd/imsqti_v2p1`.
- A `responseDeclaration` of cardinality `single` and base type `identifier`
  holds the correct option identifier.
- A `choiceInteraction` holds the stem in `prompt` and the four options in
  `simpleChoice`. The attribute `shuffle` is `false`, and `maxChoices` is 1.
- The `responseProcessing` element names the standard `match_correct` template.
  The template keeps the item inside the supported set, because Blackboard skips
  an item that carries custom response processing rules.
- The option order follows the .txt file, so the balanced answer key stays
  correct: A 25, B 25, C 25, D 25.

The option identifiers carry the item identifier as a prefix, for example
`clo835-q3-001-choiceA`. This keeps every identifier unique in the package.

## Results

`python3 build_qti3.py`:

- questions: 100
- package: `Quiz03_Pool_QTI21.zip`, 72 935 bytes

`python3 audit_qti3.py`, exit code 0:

- files in the ZIP: 101, items 100
- resources in the manifest: 100
- records in the key: 100
- answer mismatches against the key: 0
- errors: 0

The audit also confirms these facts for each of the 100 items:

- The XML parses.
- The manifest list and the ZIP list agree.
- Each item holds exactly one correct value, and the value names one of its own
  four options.
- The stem matches the key.
- The answer letter and the answer text match the key.
- The item names the `match_correct` template.

## Issues / Notes

- The package is not tested against a live Blackboard course. No upload ran.
- Blackboard import path: Course Content, then Details & Actions, then Question
  banks, then Manage banks, then the plus icon, then Import from QTI 2.1 package.
- Points do not travel in the package. Set the points in the test, in the
  question pool control: show 20 questions at 5 points each.
- The staging folder `qti3_stage` is removed. The builder makes it again at each
  run.
