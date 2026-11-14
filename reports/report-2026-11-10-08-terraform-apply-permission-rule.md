# Report: Permission rule for terraform apply
**Date**: 2026-11-10
**Sequence**: #08 for the day

## Summary
The user asked to add the permission rule `Bash(terraform -chdir=* apply*)`. I added it to the allow list of the project file `.claude/settings.local.json`. The JSON is valid, and the existing rules and hooks stay.

## What Changed
- `/Users/maziar/Downloads/k8s_week3/.claude/settings.local.json`: one new line at the end of `permissions.allow`: `"Bash(terraform -chdir=* apply*)"`.

## Technical Details
- I read the file before the edit. It had 13 allow rules and the two ASD-STE100 hooks (`UserPromptSubmit`, `SessionStart`).
- I chose the local project file, because the earlier allow rules of this project are there. The rule applies only to sessions in `/Users/maziar/Downloads/k8s_week3`.
- Check: `jq -e` finds the new rule, and the hook command is still at its place. Exit 0.

## Results
- The file now has 14 allow rules. No other line changed.
- I ran no Terraform command and made no AWS call.

## Update: the destroy rule
- The user then asked for the destroy rule too. I added `"Bash(terraform -chdir=* destroy*)"` after the apply rule.
- Check: `jq -e` shows both Terraform rules. The file has 15 allow rules. The JSON is valid.

## Issues / Notes
- The live test pipes the student answers into Terraform: `(sleep 10; echo Maziar; sleep 40; echo yes) | terraform -chdir=DIR apply`. Claude Code checks each part of such a pipe, so the classifier can still check the `sleep` and `echo` parts.
- If the session does not see the change, open `/permissions` or start a new session.
