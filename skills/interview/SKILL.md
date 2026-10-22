---
name: interview
description: Prepare for software engineering interviews: a profile and story bank that outlive any process, a plan per process counted back from its date, mocks scored on evidence, debriefs and the offer.
disable-model-invocation: true
argument-hint: "<company>: what is coming or what happened (a new process, mock <type>, a debrief, an offer), or nothing to practice"
---

Preparing for an interview is training for a match: it has a date and a known format, and it is played out loud under a clock. The work has two layers. The **root** (the profile, the story bank, the questions) is readiness that outlives every process. A **process** is a sprint toward a date: it draws on the root and feeds what it learns back into it. **A mock that flatters is worse than no mock**, because it builds confidence the real interview takes away: every score rests on the user's own words.

## Locating the work

The **interview home** is `$ARSENAL_INTERVIEWS_HOME` when set, else `~/interviews`. Its root holds `PROFILE.md`, `STORIES.md`, `QUESTIONS.md`, `PATTERNS.md` (once a live-coding mock has linked a problem) and `practice/` (mocks tied to no process). Each **process** (one role at one company) gets one folder: `<interview home>/<company>/<YYYY-MM-role>/`, with the month it started.

1. **No argument**, or an argument with no company (`mock behavioral`): the intent is **Practice**.
2. Otherwise split the argument at its first colon into the company and the rest. Slug the company in kebab-case; if it is close to an existing company folder, ask whether it is the same company.
3. Read the intent from the rest; when it fits none of these, ask what the user wants to do:

| Intent | Example argument | Processes it targets | Then |
| --- | --- | --- | --- |
| **Practice** | (nothing), `mock system design` | none: the root | [Practice](#practice) |
| **New** | `acme: senior frontend, technical on 10/28, <JD url or path>` | none (create the folder) | [The setup](#the-setup) |
| **Mock** | `acme: mock live coding` | `open` | [Mocks](#mocks) |
| **Advance** | `acme: passed, onsite on 11/5` | `open` | [LIFECYCLE.md](./LIFECYCLE.md), Advance |
| **Debrief** | `acme: had the technical, they asked for an LRU cache` | `open` | [LIFECYCLE.md](./LIFECYCLE.md), Debrief |
| **Offer** | `acme: they offered 6k USD a month` | `open` or `offer` | [LIFECYCLE.md](./LIFECYCLE.md), Offer |
| **Outcome** | `acme: rejected`, `acme: accepted`, `acme: I withdrew` | `open` or `offer` | [LIFECYCLE.md](./LIFECYCLE.md), Outcome |

4. Among the company's processes in a targeted state: exactly one → use it; several → ask which; none → tell the user what states that company's processes are in, and stop.
5. For **New**, name the folder from today's month and a short slug of the role, and create it.

Before the first intent ever runs, the root is built. When `PROFILE.md` is missing, read [PROFILE-FORMAT.md](./PROFILE-FORMAT.md) and run its interview. When `STORIES.md` is missing, read [STORIES-FORMAT.md](./STORIES-FORMAT.md) and run its bootstrap; the user may defer it, but a behavioral or recruiter mock, and a plan with a behavioral stage, run it first.

Done when you hold the interview home, one intent and, unless it is Practice, one absolute process path, and have told the user all of them.

## Where things are written

Write only inside the interview home. The repo the session was opened in stays untouched, and so does the compensation in `PROFILE.md`: it never leaves the home. Facts about a company or a market live in `research` topics and are linked, never copied: they expire, and `research` is what re-verifies them.

Every process keeps a `STATUS.md`, which every intent reads and updates:

```md
# {Company} · {role}

- State: open | offer | accepted | rejected | withdrawn
- Level: {the level interviewed for}
- Language: {the language the interviews are held in}
- JD: {url or path, or "none"}

## Stages

| Stage | Kind | Date | Result |
| --- | --- | --- | --- |
| {Recruiter screen} | {recruiter} | {YYYY-MM-DD, or "unknown"} | {passed \| failed \| blank until it happens} |

## Log

- {YYYY-MM-DD} · {one line: what happened, and why}
```

A stage's kind is one of the mock types in [MOCK-FORMAT.md](./MOCK-FORMAT.md) (`recruiter`, `behavioral`, `live-coding`, `system-design`, `frontend`, `client-case`), or `unknown` until the company says. A stage with a known format (an async video in one take, a time to read and a time to answer, a take-home) writes it in the stage's name, and its mocks replicate it. The Log is append-only.

## The setup

### 1. Ground

Read the JD (fetch the url, or read the path), `PROFILE.md`, `STORIES.md` and `QUESTIONS.md`. Ask for whatever the argument left out: the role, the level, the stages known so far with their dates, and the language the interviews are held in. Create `STATUS.md` in state `open` with its first Log line.

Done when `STATUS.md` exists with the level, the language and at least the next stage, with its date or `unknown`.

### 2. Dossier

Hand two questions to `research`, in the background so the setup goes on:

- On the company's topic: how it interviews for this role, and what it builds and with which stack. When it codes live, whether the problems are algorithmic or practical, and which algorithm problems it has asked, each with its link: LeetCode's company tags are paid, so the free sources (`github.com/liquidslr/leetcode-company-wise-problems`, interview reports on LeetCode Discuss) are where to look.
- On the market topic for the role, level and region in `PROFILE.md`: the compensation range. Skip it when that topic holds a fresh answer.

A host that cannot run `research` in the background runs it after the checkpoint. When the answers return, close everything that waited on them, in the same turn and not at a later stage:

- Link their sections from the Sources of `fit.md`, and fill its Questions to ask them.
- Propose the compensation in `PROFILE.md`, as PROFILE-FORMAT.md lays out.
- Fold them into the plan, and write again any cheat sheet already written.

Done when both questions are with `research`, or were answered fresh, or the user declined them; and, once they return, nothing that waited on them still reads pending.

### 3. Fit

Before writing `fit.md`, read [FIT-FORMAT.md](./FIT-FORMAT.md). Match the JD's requirements against the profile and the stories, name the gaps, and write the plan counted back from the next stage's date.

Done when every requirement has its evidence or reads `none`, every gap says whether it closes before the stage, and every day until the next stage has a plan row or reads rest.

### CHECKPOINT · "Is this the plan?"

Show: the stages and their dates, the requirements with their strength, the gaps and how each is handled, the plan with each day's mode, and what is still pending from `research`. Corrections go back into `STATUS.md` and `fit.md`, then show the checkpoint again.

Done when the user confirms the plan.

## Practice

The root is the readiness every process draws on, so practice with no process aims at the root's weak points. Read `QUESTIONS.md`, the index of `STORIES.md`, `PATTERNS.md` when it exists, and every `STATUS.md` in state `open`. Show:

- Each open process with its next stage, its date and the days left.
- The three weakest spots, by QUESTIONS-FORMAT.md's rule, each with its latest evidence.
- The competencies no story covers, and whether any story reaches the scope of the levels in `PROFILE.md`'s Targets.
- The patterns never seen and the weak patterns, by [PATTERNS-FORMAT.md](./PATTERNS-FORMAT.md)'s rule, when the user's targets include live coding.

Then propose one mock: its type, its mode and why. When an open process has a stage within 3 days, propose that stage's mock under that process instead. With an argument naming a type, skip the proposal and run that one. A mock with no process is written under `practice/`, and its mode is drill unless the user asks for a simulation.

Done when the user has the overview and has run a mock, or said no.

## Mocks

Read [MOCK-FORMAT.md](./MOCK-FORMAT.md) and follow it. The mode comes from the day's row in `fit.md` (drill or simulation); the user's word overrides it. A mock that touches a story updates `STORIES.md` only with the user's confirmation.

Done when MOCK-FORMAT.md's record is written, and `QUESTIONS.md`, `STORIES.md`, `PATTERNS.md` (for a linked live-coding problem) and the plan row are updated.

## Cheat sheet

The day before each stage, the plan writes `cheatsheet-<stage>.html` into the process: one printable page, two at most, to read on the morning of the interview. Build it like `teach`'s reference documents: beautiful, quick to scan, Tufte rather than a slide.

- The stories most likely to be asked, each as a three-line STAR reminder, mapped to the questions they answer; stories at the scope of the process's level come first.
- The company facts that matter for this stage, each with its read date, from the dossier.
- The two or three rubric criteria this user keeps missing, from `QUESTIONS.md`, as reminders.
- For a recruiter stage: the one-minute pitch and the answer to the expectations question, built from `PROFILE.md` without writing the floor.
- Three questions to ask the interviewer, grounded in the dossier rather than generic.

A system design or a past project the stage will ask about is drawn with the `diagram` skill and embedded as the SVG it renders. Open the cheat sheet for the user when you can (`open` on macOS, `xdg-open` on Linux).

Done when it holds every section above that applies to the stage (the pitch and the expectations answer only for a recruiter stage), the three questions to ask among them, prints in at most two pages, and every company fact on it carries its read date.

## What this skill does not do

- **Teach a topic from zero.** A gap that needs weeks of learning goes to `/arsenal:teach <topic>`, and the plan links its learning workspace. A mock only trains what the user already knows.
- **Know a company from memory.** How a company interviews, what it pays and what it builds is `research`. Never state it from recall.
- **Send anything.** Applications, emails and counteroffers are the user's to send.

## Language

The root and the process files follow the language of the conversation. A mock is held in the process's interview language (in `PROFILE.md`'s default for practice), and so are the cheat sheet's answers; the feedback out of character follows the conversation.
