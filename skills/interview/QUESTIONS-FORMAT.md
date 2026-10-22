# QUESTIONS.md and debrief formats

`QUESTIONS.md` lives at the interview home root. It logs every question the user faced, in mocks and in real interviews, so their weak spots are measured rather than guessed. Debriefs live in each process, at `debriefs/{NNNN}-{stage}.md`, and feed it.

## QUESTIONS.md

```md
# Questions

## Weak spots

| Type | Criterion | Last scores | Average |
| --- | --- | --- | --- |
| {type} | {criterion} | {up to five, oldest first} | {average} |

## Log

| Date | Source | Type | Question | Score | Record |
| --- | --- | --- | --- | --- | --- |
| {YYYY-MM-DD} | {mock \| real · {company} {stage}} | {type} | {the question, close to verbatim} | {2.3, 2.3 prepared, or 2 self} | [{record}]({path}) |
```

- A mock row's score is the average of the question's scored criteria (`n/a` left out), to one decimal, marked `prepared` when the attempt was. A real row's score is the user's own rating, marked `self`.
- A live-coding question with a linked problem writes its Question as `[{title}]({link}) · {pattern}`, so the Log and `PATTERNS.md` point at the same problem.
- **A weak spot** is a criterion whose last five scores average below 3, counting only unseen attempts and leaving out `n/a`. It needs at least three scores from at least two mocks: before that it is too early to call, and it is left out. Rebuild the table after each mock or debrief, weakest first; the three at the top are what Practice proposes.
- The Log is append-only. A real question is the most valuable row in the file: the next mock of its type for that company starts from it.

## Debrief

Write it as soon after the interview as the user can: memory of the exact questions fades within a day. Interview the user one section at a time.

```md
# Debrief · {stage} · {YYYY-MM-DD}

- Interviewers: {their roles}
- Format: {length, tool, what was shared on screen}

## Questions asked

- {the question, as close to verbatim as the user remembers}: {how it went}. Self: {1–4}. Missing: {what a better answer had}

## Stories used

- {story id}: {how it landed, and the follow-ups it drew}

## What they seemed to care about

- {a signal: what they probed most, what they skipped}

## Surprises

- {what the plan did not prepare for}

## For the next stage

- {what to change in the plan}
```

Done when every question the user remembers is in the debrief and in the Log of `QUESTIONS.md`, and every story used has its Used in updated.
