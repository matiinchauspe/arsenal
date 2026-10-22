# Interview skill: behavioral scope by level, and live-coding problems with links

Date: 2026-10-22 · Skill: `skills/interview` · Status: approved design

## Problem

1. **The behavioral rubric ignores the level.** It scores STAR, "I" not "we", a measurable result, reflection, timing and relevance the same way for a mid and a staff candidate. Real loops down-level a senior whose stories have a mid's scope; the skill never measures it.
2. **Live-coding problems are invented.** The agent writes `PROBLEM.md` from nothing: no link to a real problem, no record of which patterns the user has practiced, no use of what the company actually asks.

## Sources

- Hello Interview, behavioral course: eight signal areas (Scope, Ownership, Ambiguity, Perseverance, Conflict Resolution, Growth, Communication, Leadership); "Soft Skills Distinguish Senior from Junior"; pitfalls incl. "The 'We' Disease". Most lessons are paywalled: used for direction only, nothing copied.
- Tech Interview Handbook, behavioral for senior candidates: seniors must "proactively demonstrate their scope"; stories with "multiple teams, ambiguous requirements, and/or significant technical risk"; stories "acceptable for more junior candidates can raise red flags".
- Will Larson, *Staff Engineer*: staff is "evidence of impact at the company scope". Engineering Leadership newsletter, quoting a Meta hiring-committee chair: "No staff-level scope there, no staff-level offer."
- No source defines a mid-level bar: the mid row below is an inferred baseline and the skill says so.
- Grind 75 (techinterviewhandbook.org/grind75): free, curated, each problem links to `https://leetcode.com/problems/<slug>/`.
- NeetCode 150 pattern taxonomy (18 categories): Arrays & Hashing, Two Pointers, Sliding Window, Stack, Binary Search, Linked List, Trees, Tries, Heap / Priority Queue, Backtracking, Graphs, Advanced Graphs, 1-D Dynamic Programming, 2-D Dynamic Programming, Greedy, Intervals, Math & Geometry, Bit Manipulation.
- LeetCode company tags are Premium. Free alternatives: `github.com/liquidslr/leetcode-company-wise-problems`, LeetCode Discuss interview experiences.

## Scope

In: a scope criterion for behavioral mocks, scope on stories, a curated problem list with links, a pattern coverage file, dossier questions about the problems a company asks.

Out (later changes): CARL and the eight signal areas, sourced behavioral questions, an online-assessment (HackerRank-like) mock format, linked practical exercises, the full NeetCode 150.

## Design

### 1. Behavioral: scope at the level

**Rubric** (`MOCK-FORMAT.md`, Rubrics): `behavioral` gains a seventh criterion, **scope fits the level**.

**Scope table** (`MOCK-FORMAT.md`, next to the rubric), used to score it:

| Level | Scope the story shows |
| --- | --- |
| mid | A task or feature the user owned end to end (inferred baseline: no source defines it) |
| senior | A project with several people, ambiguous requirements or significant technical risk; influence without authority |
| staff | Several teams or the organization: competing priorities between teams, technical direction |

A level above staff uses the staff row. A story whose scope is a lower level's scores at most **2** on this criterion, however well told. Levels the table does not name (junior, principal) map to the nearest row, named at setup.

**Stories** (`STORIES-FORMAT.md`):

- Each story gains `- Scope: task | project | multi-team`, and the Index gains a Scope column.
- The bootstrap, when no story reaches the scope of the user's target levels in `PROFILE.md`, prompts next for one that does.
- Existing stories have no scope: the first mock or bootstrap that uses one proposes it, and writes it on the user's yes (as any story change).

**Fit** (`FIT-FORMAT.md`): no story at the scope of the process's level is a gap, handled like any other gap.

**Cheat sheet** (`SKILL.md`): stories at the level's scope come first.

**Weak spots**: the new criterion starts with no history; existing rows are untouched.

### 2. Live coding: linked problems and pattern coverage

**Curated list**: new file `skills/interview/PROBLEMS.md`, about 75 problems seeded from Grind 75, topped up from NeetCode 150 for any pattern Grind 75 leaves with fewer than 2.

```md
| Problem | Link | Pattern | Difficulty |
| --- | --- | --- | --- |
| Two Sum | https://leetcode.com/problems/two-sum/ | Arrays & Hashing | easy |
```

- Patterns are the 18 NeetCode categories, each with at least 2 problems.
- Title, link and tags only: never a problem statement.
- Every link is checked to exist before the file is committed. LeetCode blocks automated fetches, so slugs come from the Grind 75 and NeetCode 150 lists themselves and any slug that cannot be confirmed is left out.

**Dossier** (`SKILL.md`, setup step 2): the company question to `research` adds: when the company interviews with algorithm problems, which ones it has asked, with links (free sources above; company tags are Premium and never assumed).

**Choosing the problem** (`MOCK-FORMAT.md`, setup), for a live-coding mock whose stage is algorithmic:

1. A real question from `QUESTIONS.md` for this company.
2. A problem the dossier cites, with its link.
3. From `PROBLEMS.md`: a pattern the user has never seen, then the weakest pattern in `PATTERNS.md`.
4. Difficulty by level: mid easy or medium, senior medium, staff medium or hard.

Never a problem already in `PATTERNS.md`, unless the plan asks for a retry. When the dossier says the stage is practical (build an endpoint, refactor, consume an API), the agent writes the problem as today: no link and no pattern row. A stage with no dossier answer is treated as algorithmic.

**Workspace** (`MOCK-FORMAT.md`, Live coding), still local:

- `PROBLEM.md`: the link, the function signature and the constraints that matter. No statement: the user reads it on the site.
- `solution.{ext}` and `solution.test.{ext}`: unchanged.
- Hidden tests: written before the user starts, as today. The agent writes them from its knowledge of the problem and cannot read the site, so **the official statement wins**: a hidden test the user shows contradicts it is dropped, and the record says so.
- Optional: the user submits to the site's judge after the mock; the verdict ("accepted", "wrong answer on …") goes into the record as second evidence and never changes a score.

**Pattern coverage**: new root file `PATTERNS.md`, with its format in a new `PATTERNS-FORMAT.md`.

```md
# Patterns

## Coverage

| Pattern | Problems seen | Last scores | Average |
| --- | --- | --- | --- |
| {pattern} | {N} | {up to five, oldest first} | {average} |

## Log

| Date | Problem | Pattern | Score | Record |
| --- | --- | --- | --- | --- |
| {YYYY-MM-DD} | [{title}]({link}) | {pattern} | {score, or "prepared"} | [{record}]({path}) |
```

- A problem's score is the average of its mock's scored criteria, as in `QUESTIONS.md`.
- A **weak pattern** averages below 3 over at least 2 unseen problems. Two, not three, because each mock yields one problem.
- The Log is append-only; Coverage is rebuilt after each live-coding mock, weakest first, with never-seen patterns listed.
- `PATTERNS.md` is created by the first linked live-coding mock; the root build does not require it.
- The mock record and the `QUESTIONS.md` Log row carry the link and the pattern.
- **Practice** shows never-seen and weak patterns next to the weak spots.

## Files touched

- `skills/interview/MOCK-FORMAT.md`: rubric criterion, scope table, problem choice, workspace, record fields.
- `skills/interview/STORIES-FORMAT.md`: Scope field and column, bootstrap prompt.
- `skills/interview/FIT-FORMAT.md`: scope gap.
- `skills/interview/SKILL.md`: root files list, dossier question, Practice overview, cheat sheet order, Mocks done line.
- `skills/interview/QUESTIONS-FORMAT.md`: link and pattern in Log rows of live-coding questions.
- `skills/interview/PROBLEMS.md`: new.
- `skills/interview/PATTERNS-FORMAT.md`: new.

## Verification

- Every link in `PROBLEMS.md` comes from a Grind 75 or NeetCode 150 entry; each of the 18 patterns has at least 2 problems.
- A dry read of the skill: a senior behavioral mock with a task-scope story scores scope at most 2; a live-coding practice mock with an empty `PATTERNS.md` picks a never-seen pattern from `PROBLEMS.md` and writes `PROBLEM.md` with a link and no statement.

## Housekeeping

This spec, and the plan that follows it, are deleted from the branch before merge, as with the idea skill.
