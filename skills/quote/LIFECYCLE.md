# Lifecycle

What happens to an engagement after its proposal is written. Each section is one intent from SKILL.md and runs on the engagement it resolved.

```
draft ──sent──▶ sent ──▶ accepted (all or some phases) ──finished──▶ closed
  ▲               │
  └── revision ───┤
                  └────▶ rejected (with reason)
```

## Sent

A sent version is **frozen**: it is exactly what the client saw, and it never changes again.

1. When the last Log line of `STATUS.md` does not record `proposal written v{N}` for the current version, the draft is unfinished or a revision is under way: tell the user and stop.
2. Copy `proposal.html` to `proposal-v{N}.html` and `quote.md` to `quote-v{N}.md`, with N the version in `STATUS.md`.
3. Set the state to `sent` and log the date, plus how or to whom it went when the user said.

Done when both frozen copies exist and match their drafts byte for byte, and `STATUS.md` reads `sent`. Any later change to the engagement is a revision, which opens `v{N+1}`.

## Outcome

The client answered the sent version.

- **Accepted**: all phases, or some. Log which phases were accepted; in the Hours table, write "not accepted" in the Actual column of the others.
- **Rejected**: log the reason in one line. When the user gave none, ask once; "unknown" is a valid answer.

Done when the state is `accepted` or `rejected` and its Log line names the phases or the reason.

## Actual hours

Recording is optional: record what the user volunteers.

- Write the hours the user gives into the Actual column of each phase they name.
- When the user says the work is finished, set the state to `closed` and log it; phases with no actuals stay blank.

Done when every phase the user gave hours for has them in the Hours table, and the state is `closed` exactly when the user said the work is finished.
