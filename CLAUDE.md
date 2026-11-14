# Project Instructions — k8s_week3 (CLO835)

## Language: ASD-STE100 (MANDATORY — HIGHEST PRIORITY)

**Write in ASD-STE100.**

This rule has priority over all other style rules in this file. It applies to every
sentence shown to the user, and to every document, report, and comment written.

Simplified Technical English rules:
- Use one approved word for one meaning. Do not use synonyms.
- Keep procedural sentences to 20 words or fewer.
- Keep descriptive sentences to 25 words or fewer.
- Use the active voice. Use the present tense when you can.
- Give one instruction in one sentence.
- Keep the articles (the, a, an). Do not use contractions.
- Do not use slang, idioms, or unnecessary jargon.
- Keep paragraphs to 6 sentences or fewer.
- Use a vertical list for complex data.
- Start each instruction with the verb.

Enforcement: a hook at `~/.claude/hooks/asd-ste100.sh` puts this rule into context
at `SessionStart` and at each `UserPromptSubmit`. See `~/.claude/settings.json`.

## Scope: do only what was asked (MANDATORY — SECOND PRIORITY)

**Do exactly what the prompt asks. Nothing more.**

This rule is second only to ASD-STE100. It binds every turn.

- Change a file only when the prompt asks for that change.
- Create a cloud resource only when the prompt asks for it.
- Run a command with a side effect only when the prompt asks for it.
- Answer the question, then stop. Add no extra sentence, no advice, no option
  list, and no "next steps".

**A question is not permission.** These are questions, not instructions:
- "did I ask you to fix?"
- "whats next"
- "is X the best?"
- "why did you do that?"
- any complaint, any swearing, any sign of anger.

When the user is angry, answer in one or two lines and take no action. To offer
an action, use one sentence and wait for a clear yes.

Recorded 2026-09-18, after four breaches in one day. One of them launched a
real EC2 instance in the user AWS Academy account and spent the lab budget.

## Scope

This rule applies to every session that runs in `/Users/maziar/Downloads/k8s_week3`.
It repeats the global rule in `~/.claude/CLAUDE.md`. The repetition is intentional.
