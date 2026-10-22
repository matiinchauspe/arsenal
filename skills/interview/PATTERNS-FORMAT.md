# PATTERNS.md Format

`PATTERNS.md` lives at the interview home root and tracks the algorithm patterns the user has practiced in live-coding mocks with a linked problem, so the next problem aims at what is missing rather than at what is comfortable. The first such mock creates it; the root build does not.

## Template

```md
# Patterns

## Coverage

| Pattern | Problems seen | Last scores | Average |
| --- | --- | --- | --- |
| {pattern} | {N} | {up to five, oldest first} | {average, or "never seen"} |

## Log

| Date | Problem | Pattern | Score | Record |
| --- | --- | --- | --- | --- |
| {YYYY-MM-DD} | [{title}]({link}) | {pattern} | {2.3, or 2.3 prepared} | [{record}]({path}) |
```

## Rules

- **Patterns** are the eighteen of [PROBLEMS.md](./PROBLEMS.md). Coverage lists all of them, the never-seen ones included.
- **A problem's score** is the average of its mock's scored criteria (`n/a` left out), to one decimal, marked `prepared` when the attempt was, as in QUESTIONS-FORMAT.md.
- **A weak pattern** averages below 3 over its last five unseen problems, with at least two of them. Two, not three as for weak spots, because each mock yields one problem.
- **Order.** Rebuild Coverage after each linked live-coding mock: never-seen patterns first, then weak patterns, weakest first, then the rest.
- The Log is append-only. A problem in the Log is not chosen again unless the plan asks for a retry.
- A written problem (a practical stage) has no pattern and never enters this file.
