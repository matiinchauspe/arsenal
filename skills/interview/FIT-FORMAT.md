# fit.md Format

`fit.md` lives in the process folder. It holds how the user matches the role, what is missing, and the plan to the next stage, counted back from its date.

## Template

```md
# Fit · {Company} · {role}

Written: {YYYY-MM-DD}. Next stage: {stage} ({kind}) on {YYYY-MM-DD}, in {N} days.

## Sources

- JD: {url or path}
- Company: [{research topic, section}]({path}), read {YYYY-MM-DD}, or "pending"
- Market: [{research topic, section}]({path}), read {YYYY-MM-DD}, or "pending"

## Requirements

| Requirement | Evidence | Strength |
| --- | --- | --- |
| {from the JD, in its own words} | {a PROFILE.md line, or a story id, or "none"} | strong \| thin \| gap |

## Gaps

- **{Gap}**: {what it would take to close}. {Closes before {stage}: how, in the plan · Delegated: `/arsenal:teach {topic}`, at {learning workspace path} · Out of reach: how to talk about it honestly}

## Plan

| Date | Serves | Work | Mode | Done |
| --- | --- | --- | --- | --- |
| {YYYY-MM-DD} | {stage} | {mock {type} · story {id} · study {what} · cheat sheet · rest} | {drill \| simulation \| —} | {✓ \| ✗ \| blank} |

## Questions to ask them

- {A question grounded in a company fact, with the fact it comes from}
```

## The plan

The plan is counted back from the next stage's date. The days left decide what is worth doing:

| Days to the stage | What the plan holds | Mocks |
| --- | --- | --- |
| 14 or more | Gaps that close in time are studied; a gap that needs more than the time left is delegated to `teach` or handled as out of reach | Mostly drills |
| 4 to 13 | No new topics: only what the user already partly knows. Stories polished | Drills and simulations alternate |
| 1 to 3 | Nothing new. Simulations of the stage's exact kind, and the cheat sheet the day before | Simulations only |
| 0 | Only the cheat sheet | None |

- **Respect the time.** A day's work fits the prep hours in `PROFILE.md`.
- **Space and mix.** A weak type returns on spaced days (one, three and seven days later), not on consecutive ones, and drills mix types rather than repeating one.
- **Unknown kind.** A stage whose kind is `unknown` is planned from what the company dossier says about it, and as behavioral until it does.
- **Scope gap.** When the process has a behavioral stage and no story in `STORIES.md` reaches the scope of its level (MOCK-FORMAT.md's [Scope by level](./MOCK-FORMAT.md#scope-by-level)), that is a gap like any other: the plan drafts such a story when the user has one untold, or the gap reads out of reach with how to talk about it honestly.
- **Replan forward.** When a date changes or a debrief lands, rewrite the rows from today on. Past rows stay with their Done mark: a skipped day is ✗, not deleted.
