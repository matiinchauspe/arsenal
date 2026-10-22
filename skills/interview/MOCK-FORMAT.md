# Mocks

A mock is one practice interview: the agent plays the interviewer, then steps out and scores it. The danger is kindness: an agent that hints, praises and rounds up builds fluency the real interview does not reward. Everything below exists to keep the score honest.

## 1. Setup

Settle, from the argument, `STATUS.md`, the day's plan row or the user:

- **Type**: `recruiter`, `behavioral`, `live-coding`, `system-design`, `frontend`, `client-case` or `negotiation`. A `client-case` is a client's business problem answered to the client: the case of a forward deployed, solutions or consulting role, where the listener is a buyer, not an engineer. A stage that fits no type takes the closest one, and the criteria of its rubric that do not fit the stage are named at setup.
- **Level** and **company**: the process's, or the highest level in `PROFILE.md`'s Targets for practice.
- **Mode**: **drill** (out of character after each question, then one retry) or **simulation** (in character to the end, like the real thing).
- **Length**: recruiter 20 minutes; behavioral, frontend, client-case and negotiation 30; live coding and system design 45. The user may shorten it. A stage with a known format sets the length and the rules instead, and the mock replicates them: 30 seconds to read, one take, five minutes to answer.

Choose the questions in this order: real questions from `QUESTIONS.md` for this company and type, then what the company dossier says it asks, then the weak spots in `QUESTIONS.md`, then questions fit for the level. Never repeat a question the user already answered in a mock, unless it is a retry the plan asked for. A live-coding mock chooses its problem as [Live coding](#live-coding) lays out.

Number the mock with the highest number under the folder's `mocks/` plus one, and note the start time with `date`.

Done when the type, level, mode and length are set and told to the user, and the start time is noted.

## 2. In character

- **One question at a time**, and wait for the answer.
- **Probe like a real interviewer**: "why?", "what did *you* do?", "what if traffic grew tenfold?", "what would you change?". An answer that dodges the question gets the question again.
- **No hints unless asked.** A hint the user asks for is given the way an interviewer would give it, and noted: asking well is fine, but it counts. A hint is a nudge, one sentence or the name of a missing step; never the worked answer, and never wording written for the scenario.
- **Coaching is not an attempt.** When the user asks how to answer before answering, coach them out of character (the structure, example lines), then give them a question they have not seen. An answer given after the coaching on the same question is **prepared**: it is scored and recorded, but it measures the coaching, not the user, and never counts toward a weak spot.
- **No feedback in character.** No "great answer", no nodding along. A neutral "thanks, next" is what a real interviewer gives.
- **Keep the clock.** Check `date` at each turn. When the time is up, close the way an interviewer does ("we're out of time, any questions for me?"). `date` measures the session, not a spoken answer: see [Timing a spoken answer](#timing-a-spoken-answer).

### Timing a spoken answer

A spoken answer is timed with whatever the user records with, never with a tool the skill assumes. `PROFILE.md`'s Speaking section says how; when it is empty, the first spoken mock sets it up:

1. **Ask what the user records or dictates with.** When they name a tool, find where it leaves each recording and how its duration is read (a metadata file the tool writes, or `ffprobe` on the audio or video file), read one recording to confirm it, and write that into `PROFILE.md`. A tool whose durations cannot be read this way is treated as none.
2. **None:** offer what the user already has, with no install: the system's own recorder (Voice Memos or QuickTime on macOS, the phone's recorder), whose file they hand over for `ffprobe`. Recording also trains the real thing when the stage is a recorded video.
3. **They would rather not record:** they time each answer with a stopwatch and say the time.
4. **Neither:** estimate from the words, at the pace in `PROFILE.md`, else 130 a minute, and mark the duration **estimated**.

A measured duration is exact; an estimated one is never the only evidence for a score. **The limit is a format, not a criterion:** in a stage with a hard limit (a one-take video), what the user says past the limit is not heard, so it is not scored, and the record says where the answer was cut. Every answer's duration is written in the record, against the limit when there is one.

In a drill, step out after each question for its scores and one fix, then offer one retry of the same question: answering it again from memory is the practice.

### Live coding

**The problem.** A stage the company dossier says is practical (build an endpoint, refactor, consume an API) gets a problem written for it, close to what the company asks, with no link. Any other live-coding stage, one the dossier says nothing about included, takes a real problem with a link, in this order:

1. A real question from `QUESTIONS.md` for this company, linked to its problem in PROBLEMS.md or the dossier when one matches, else written as a practical one is.
2. A problem the company dossier cites, with its link, unless the user cannot open it (a LeetCode Premium problem without Premium).
3. From [PROBLEMS.md](./PROBLEMS.md): the first pattern in the Coverage order of `PATTERNS.md`, by [PATTERNS-FORMAT.md](./PATTERNS-FORMAT.md)'s rule, that still has a problem at the level outside its Log; with no `PATTERNS.md`, every pattern is never seen, and among never-seen patterns the first in PROBLEMS.md comes first. When no pattern has one, propose a retry of the weakest problem, or the closest difficulty, and tell the user.

Difficulty follows the level: mid easy or medium, senior medium, staff medium or hard. Never a problem already in the Log of `PATTERNS.md`, unless the plan asks for a retry. A linked problem not in PROBLEMS.md takes the closest of its eighteen patterns, named at setup.

The mock lives in `mocks/{NNNN}-live-coding/`, in the language and test runner of `PROFILE.md`:

- `PROBLEM.md`: for a linked problem, its title and link, the signature in the mock's language (a class with its methods when the problem is a design one, such as an LRU cache) and the constraints that matter, never the statement: the user reads it on the site. For a written problem, the statement, two examples and the constraints. No tests either way.
- `solution.{ext}`: an empty function, or class, with its signature, and the types the signature uses that the site defines for the user (`ListNode`, `TreeNode`), with helpers that build them from arrays and back, so both suites can state their cases as arrays.
- `solution.test.{ext}`: empty. The user's own tests go here, and they count.

Before the user starts, write the **hidden tests** (the edge cases a strong candidate covers) into the system temp directory, outside the interview home, so they are fixed before any code exists and the user cannot see them. Read the solution file on every turn, as an interviewer watches the shared editor, and probe what it shows. When the user says they are done, or the time is up, move the hidden tests into the folder and run both suites. When the folder cannot run them as it is, set up the minimum the runner needs (a `package.json`, say) and tell the user.

A linked problem's hidden tests come from what the agent knows of it, and the site cannot be read, so **the official statement wins**: a hidden test the user shows to contradict it is dropped, and the record says so. Before writing the record, offer the user to submit to the site's judge; its verdict goes into the record as a second piece of evidence and never changes a score. A judge's "accepted" on code a hidden test failed is the user showing that test contradicts the statement: drop it as above. A verdict the user brings later is added to that record's Judge line.

### System design

The user answers in prose, or sketches in Mermaid in `mocks/{NNNN}-system-design/design.mmd`. When the answer describes an architecture (components and how data moves between them), the design the user described is drawn after the mock with the `diagram` skill, marked as the user's, and kept in the folder: seeing their own design drawn shows what they left out.

## 3. Out of character

Score each question against its type's rubric below. Every criterion gets a score from 1 to 4 and the user's own words as evidence:

- **1** missing · **2** weak · **3** solid · **4** strong.
- **No quote, no score.** A criterion the answer gave no evidence for scores 1.
- **Not applicable is not a 1.** A criterion that does not fit the stage or the question (named at setup, or a follow-up that asks about one thing) is `n/a` with one line of why, and never counts toward a weak spot.
- **When torn between two scores, give the lower.** Score as an interviewer hiring at the process's level would.
- **No praise without evidence.** What went well is named with its quote, like what went wrong.

Then give the **verdict** for the level (strong hire · hire · no hire · strong no hire) with one line of why, and at most **two fixes**: concrete changes the user can make next time, not a list of everything.

## Rubrics

| Type | Criteria |
| --- | --- |
| `recruiter` | Pitch in about a minute, tied to the role · why this company, from something specific about it · the expectations question answered from the anchor, or deflected until the range is known, never with a number below the anchor · logistics clear (availability, location, notice) |
| `behavioral` | STAR complete · "I", not "we": the user's own actions · a measurable or concrete result · reflection: what was learned · two to three minutes, timed as above · answers the question asked · scope fits the level, by [Scope by level](#scope-by-level) |
| `live-coding` | Clarifies and walks an example before coding · states the approach and its complexity before coding · thinks out loud · correct on the hidden tests · writes their own tests and edge cases · readable code · finishes in time |
| `system-design` | Requirements first, functional and not · estimates the scale · a high-level design before the deep dive · data model and API · names the bottlenecks and scales them · tradeoffs said out loud · drives the conversation |
| `client-case` | Restates the problem with the client's own numbers · states the assumptions, and what to ask the client · a concrete first solution, in the client's language · names the risks and how trust is earned (data, security, adoption) · tradeoffs said out loud · a next step with scope and date |
| `frontend` | Fundamentals right (event loop, rendering, the cascade, the browser) · component and API design · state and data fetching · performance · accessibility · testing · tradeoffs |
| `negotiation` | Does not accept on the spot · anchors with a reason · asks for the full package · counters toward the target · stays warm · walks away below the floor |

### Scope by level

The behavioral criterion **scope fits the level** asks whether the story shows the reach the level is hired for. A story whose scope is a lower level's scores at most 2 on it, however well told. It is scored from what the user told, not from the story's Scope in `STORIES.md`. A level the table does not name takes the nearest row (junior takes mid, principal takes staff), named at setup. A question no story answers (why this company, say) scores it `n/a`.

| Level | Scope the story shows | Story scope in `STORIES.md` |
| --- | --- | --- |
| mid | A task or feature the user owned end to end. No source defines a mid bar: this row is a baseline | `task` |
| senior | A project with several people, ambiguous requirements or significant technical risk; influence without authority | `project` |
| staff | Several teams or the organization: competing priorities between teams, technical direction | `multi-team` |

Sources: Tech Interview Handbook, *Behavioral interviews for senior candidates* (seniors "proactively demonstrate their scope"; stories "acceptable for more junior candidates can raise red flags"); Will Larson, *Staff Engineer* (staff is "evidence of impact at the company scope").

## 4. The record

Write `mocks/{NNNN}-{type}.md` under the process, or under `practice/` for practice. A live-coding or system-design mock writes it as `README.md` inside its own folder.

```md
# Mock {NNNN} · {type} · {drill | simulation}

- Date: {YYYY-MM-DD}, {start}–{end} ({minutes} min)
- Process: {company · role, or "practice"}
- Level: {level} · Language: {language}
- Problem (live coding): [{title}]({link}) · {pattern} · {difficulty}, or "written"
- Hidden tests (live coding): {passed} of {total, the dropped ones left out}{; dropped "{test}": it contradicts the statement}
- Judge (linked problem): {the site's verdict, or "not submitted"}

## Q1 · {the question}

- Attempt: {unseen | prepared}
- Answer: {a summary, with the key sentences quoted verbatim}
- Duration: {m:ss}{ of {limit}}, {measured with {tool} \| stopwatch \| estimated}, {words} words{; cut at the limit after "{last words heard}"}
- Hints: {none, or what was asked and given}
- Retry: {none, or how the retry changed the scores}

| Criterion | Score | Evidence |
| --- | --- | --- |
| {criterion} | {1–4 \| n/a} | "{the user's words}", or why it does not apply |

## Verdict

{strong hire | hire | no hire | strong no hire} for {level}: {one line of why}

## Fixes

1. {a concrete change}
2. {another, or nothing}
```

Then update the root:

- `QUESTIONS.md`: one Log row per question, as QUESTIONS-FORMAT.md lays out, and the weak spots rebuilt.
- `STORIES.md`: the stories used get their Last scored and Used in; a story whose Scope reads `unset` gets one proposed from what the user told, and a better version the mock suggested is proposed; both are written only on the user's yes.
- `PATTERNS.md`: for a live-coding mock with a linked problem, its Log row and Coverage rebuilt, as PATTERNS-FORMAT.md lays out; created by the first one.
- `fit.md`: the plan row's Done mark, when the mock belongs to a process.

Done when the record is written, every score in it carries a quote or is a 1, and the root is updated.
