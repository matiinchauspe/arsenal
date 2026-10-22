# STORIES.md Format

`STORIES.md` lives at the interview home root and is the user's story bank: the real situations behavioral questions are answered from. It serves every process, so a story polished for one interview is ready for the next.

## Template

```md
# Stories

## Index

| Id | Title | Competencies | Scope | Last scored | Used in |
| --- | --- | --- | --- | --- | --- |
| [S-01](#s-01) | {title} | {competency}, {competency} | {task \| project \| multi-team, or "unset"} | {score}/4, {YYYY-MM-DD}, or "never" | {company · stage, YYYY-MM-DD; …} |

## S-01 · {Title}

- Competencies: {from the list below}
- Scope: {task | project | multi-team}
- When: {year}, at {company}

### Situation

{Two or three lines: the context an outsider needs, and nothing more.}

### Task

{What was at stake, and what was the user's to do.}

### Action

{What the user did, in the first person: the decisions and why. Most of the story lives here.}

### Result

{What changed, with numbers where the user has them, and what the user learned.}

### Follow-ups

- {A probe an interviewer asked or will ask: "what would you do differently?"} → {the answer, in one line}

### Changes

- {YYYY-MM-DD} · {what changed in the story, and the mock or debrief it came from}
```

## Competencies

Tag stories only with these, so coverage can be counted: `ownership`, `conflict`, `failure`, `ambiguity`, `influence`, `impact`, `collaboration`, `learning`, `prioritization`, `technical-decision`, `mentoring`.

## Scope

How far the story reaches, which is what MOCK-FORMAT.md's [Scope by level](./MOCK-FORMAT.md#scope-by-level) scores against the level: `task` (a task or feature the user owned), `project` (a project with several people, ambiguity or real technical risk), `multi-team` (several teams or the organization). Set it from what the user did, not from the size of the company. A story written before scope existed reads `unset`: the first mock or bootstrap that uses it proposes one, written on the user's yes.

## The bootstrap

Run it when `STORIES.md` is missing, or when a behavioral mock finds fewer than five stories. Aim for five to eight stories that together cover most competencies. Ask for one story at a time with a concrete prompt ("a time something you shipped broke in production", "a time you disagreed with your manager"), then ask through STAR until each part is there. Prompt next for a competency no story covers yet. When no story reaches the scope of the levels in `PROFILE.md`'s Targets, prompt next for one that does ("a time you led something across several teams").

Done when there are at least five stories, or the user stopped, and the Index lists every story.

## Rules

- **The story is the user's.** Write only what the user told. Never invent a detail, and never round a number up; a result the user cannot measure says so ("no number, but the on-call pages stopped").
- **"I", not "we".** The Action says what the user did. When the user only knows what the team did, ask what was theirs.
- **Changes are confirmed.** A mock or a debrief may propose a better version: show it, and write it only on the user's yes, with a line in Changes.
- **Spoken length.** A told story lasts two to three minutes: in words, two to three times the user's pace in `PROFILE.md`. A story much longer gets cut in the Situation, never in the Action.
