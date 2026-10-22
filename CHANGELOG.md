# Changelog

All notable changes to Arsenal are recorded here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow
[Semantic Versioning](https://semver.org/). The version is the one in `.claude-plugin/plugin.json`.

## [0.7.1] - 2026-10-22

### Fixed

- **`interview`**: a linked live-coding problem that is a design one (LRU cache, min stack, trie) gets
  a class with its methods instead of a function, and one built on `ListNode` or `TreeNode` gets those
  types and helpers to build them from arrays, which the site defines for the user and a local
  workspace lacks.

## [0.7.0] - 2026-10-22

### Changed

- **`interview`**: behavioral stories are scored against the level, and live-coding mocks link real
  problems.
  - The behavioral rubric gains "scope fits the level": a task for mid, a project for senior, several
    teams for staff, grounded in the Tech Interview Handbook and *Staff Engineer*. A story with a lower
    level's scope scores at most 2. Stories carry a scope, and a process with no story at its level's
    scope names it as a gap.
  - `PROBLEMS.md`: 92 free LeetCode problems across NeetCode's 18 patterns, title and link only. A
    live-coding mock picks the company's real questions first, then the dossier's, then the pattern
    the user lacks, and `PATTERNS.md` tracks coverage and weak patterns. Practical stages still get a
    written problem.
  - Hidden tests yield to the official statement; the site's judge is a second piece of evidence that
    never changes a score.

## [0.6.0] - 2026-10-20

### Added

- **`idea`** (`/arsenal:idea <idea>: <what to do>`): clarifies a product, startup or digital-business
  idea into an explicit decision.
  - Lives at `$ARSENAL_IDEAS_HOME`, default `~/ideas/`: one folder per idea with `MAP.md` and
    `STATUS.md`, and `IDEAS.md` for generated ideas not picked.
  - An idea is a map of falsifiable assumptions in seven fixed zones (problem, customer, solution,
    competition and value added, market, economics, channel), each with an impact and a state, drawn
    as an overview with `diagram`.
  - Continue picks the critical assumption with the least evidence and hands `research` a question
    phrased to refute it. Desk research reaches `researched` at most and can kill on a primary
    `[fact]`; `validated` takes a real-world test (interviews, smoke test, pre-sale), always optional,
    with its threshold written before it runs and never moved.
  - Unit economics in three scenarios computed by `economics.py`: net contribution after replacing
    churn, LTV, LTV/CAC, payback, customers and market share needed for the user's target, and a
    sensitivity pass whose deciding variable becomes a critical assumption.
  - The verdict (discard, not enough information, worth testing) always carries the best reason not to
    do it and what the idea demands (capital, skills, hours, access, time to revenue), never a
    judgment of the user, and goes stale when the facts it rests on expire.

## [0.5.0] - 2026-10-19

### Added

- **`interview`** (`/arsenal:interview <company>: <what's coming or what happened>`): prepares you
  for software engineering interviews, from the first application to the offer.
  - Lives at `$ARSENAL_INTERVIEWS_HOME`, default `~/interviews/`. The root holds what every process
    shares: `PROFILE.md`, a STAR story bank in `STORIES.md`, and `QUESTIONS.md`, which logs every
    question faced and measures the weak spots. Each process gets its own folder with `STATUS.md`.
  - A new process matches the JD against the profile and writes a plan counted back from the next
    stage's date: weeks out it studies gaps (or hands them to `teach`), days out it only simulates.
    The company's process and the market range come from `research`.
  - Mocks for recruiter, behavioral, live-coding, system-design, frontend, client-case and
    negotiation stages, as drills or simulations, replicating a stage's known format (an async
    video in one take). Every criterion is scored on a quote from the user's answer, ties score
    low, a criterion that does not fit the stage is `n/a`, and an answer given after coaching is
    recorded as prepared and never counts toward a weak spot. Live coding runs hidden tests, fixed
    before any code exists, against a real file.
  - Spoken answers are timed with whatever the user already records or dictates with, found and
    confirmed on the first spoken mock and kept in the profile with their measured pace; with no
    tool, the system's own recorder, a stopwatch, or an estimate marked as such. A hard time limit
    is a format, not a criterion: what is said past it is not scored.
  - Debriefs feed real questions back into the root; an offer is compared against the profile's
    floor and target and gets a counter; a rejection ends in a retro that feeds the weak spots.

## [0.4.0] - 2026-10-08

### Added

- **`diagram`** (`/arsenal:diagram <what>, from <source>`, also reached by the agent and by other
  skills): draws the diagram a question calls for, from code, a client's ask or a research topic.
  - One diagram answers one question, written above it; the question picks the kind (sequence,
    state, flow, use case, journey, ER), and past about 15 nodes it splits into an overview and zooms.
  - Mermaid is always the source. It lands beside what it explains: a `mermaid` block in a repo's
    docs, inline SVG in a proposal, a section of a research topic. A diagram for the same question
    is replaced in place, never duplicated.
  - Every element is traced to its source; what the source does not show is drawn as an assumption,
    and a future project is stamped Proposed. A diagram drawn from code carries its commit.
  - Every diagram is rendered and looked at before it is handed over; with no Node it is marked
    unverified. One bound for a printed document fits half a page legibly, and is checked by
    printing a copy of that document to PDF and looking at its pages.

### Changed

- **`quote`**: a proposal draws how the delivered work will run with `diagram`, inlined as SVG.
- **`research`**: an answer that describes a process offers a diagram, written into its section.
- **`teach`**: lessons and reference documents draw processes and relations with `diagram`.

## [0.3.0] - 2026-10-07

### Added

- **`research`** (`/arsenal:research <topic>: <question>`): researches a topic into one living
  document that outlives any project, so what you learned for one client serves the next one in
  the same industry.
  - Topics live at `$ARSENAL_RESEARCH_HOME`, default `~/research/`, one folder per topic with one
    `TOPIC.md`. A topic is an industry or a cross-cutting subject; an industry links a cross-cutting
    topic instead of copying it, so every fact lives in one place.
  - Every fact is labeled `[fact]`, `[secondary]`, `[inference]` or `[unverified]`, with its source
    and read date. Each question is `legal-fiscal` (only primary sources back the answer, expires
    after 6 months) or `practice` (labeled secondary sources allowed, expires after 24 months).
  - Asking again answers from the document, re-verifying only expired facts. The reading runs in a
    background agent when the host can start one. It never writes to the project's repo.

## [0.2.1] - 2026-10-07

### Fixed

- **`quote`**: the break-even now counts what the client keeps paying for the alternative while
  the work is built, until the phase that replaces it is delivered, when the client already pays
  for it. The grounding records whether it does; a trial or an evaluation pays nothing, so the
  build then carries none of it.
- **`quote`**: the policy now records when the retainer starts (suggested: at the first phase
  delivered), and the quote and proposal state it.
- **`quote`**: the proposal shows the monthly running cost against the alternative as bars, with
  the break-even month in the caption. The cumulative curve beside the weeks-based timeline read as
  a delivery date.

## [0.2.0] - 2026-10-06

### Added

- **`quote`** (`/arsenal:quote <client>: <ask>`): quotes any work sold by the hour or by the
  deliverable. It grounds the quote in what exists today (a repo, a running system, the client's
  documents, or nothing) and in the alternative it competes with, scopes it into phases, estimates
  hour ranges, and prices it with your policy. It stops at two checkpoints, after the scope and
  after the price, and writes two documents: `proposal.html` for the client and `quote.md` for you.
  - Quotes live at `$ARSENAL_QUOTES_HOME`, default `~/quotes/`, one folder per client and
    engagement; the skill reads the client's repo but never writes into it.
  - Your pricing policy lives in `POLICY.md`. Each quote snapshots the values it used, and an
    exception lives in that quote with its reason. When the policy is missing, the skill
    interviews you first.
  - The proposal shows a fixed price and an estimated delivery time per phase. Hours stay internal
    unless the client asks to see them. It is one self-contained HTML file that opens offline and
    prints to A4, signed by an identity you choose for each engagement.
  - A sent version is frozen as `vN`; later changes become `vN+1`. `STATUS.md` tracks each
    engagement from draft to sent to accepted or rejected, and optional actual hours feed back into
    later estimates as information.

## [0.1.0] - 2026-10-06

The first release: Arsenal is a Claude Code plugin marketplace that ships one plugin, `arsenal`.

### Added

- **Marketplace and plugin.** Install with `/plugin marketplace add matiinchauspe/arsenal` and
  `/plugin install arsenal@arsenal`. Skills live in `skills/<name>/SKILL.md`, the open Agent
  Skills format, so agents other than Claude Code can use them too.
- **`teach`** (`/arsenal:teach <topic>`): teaches a topic over several sessions, grounded in a
  mission. It produces short interactive HTML lessons, reference sheets, a glossary and learning
  records. Adapted from Matt Pocock's `teach` (mattpocock/skills@3216582, MIT). Changes from the
  upstream skill:
  - Each topic gets its own learning workspace at `$ARSENAL_LEARN_HOME/<topic>/`, default
    `~/learn/<topic>/`, outside the project the agent was opened in.
  - `GLOSSARY.md` is part of the workspace. The upstream skill ships its format but never links it.
  - Lessons follow the language of the conversation.

[0.2.1]: https://github.com/matiinchauspe/arsenal/releases/tag/v0.2.1
[0.2.0]: https://github.com/matiinchauspe/arsenal/releases/tag/v0.2.0
[0.1.0]: https://github.com/matiinchauspe/arsenal/releases/tag/v0.1.0
