# PROFILE.md Format

`PROFILE.md` lives at the interview home root and describes the user as a candidate: the same for every process, written from what the user says. It is private: the compensation in it never leaves the interview home.

## Template

```md
# Profile

Updated: {YYYY-MM-DD}

## Experience

- Years: {N}, as {current or last level and role}
- CV: {absolute path, or "none"}
- {Role} at {company} ({years}): {what the user owned, in one line}

## Targets

- Roles: {e.g. senior frontend, full-stack}
- Levels: {e.g. senior, staff}
- Where: {remote from {country}, hybrid in {city}, relocation yes/no}
- Companies: {kinds the user wants or avoids: product, agency, startup, big tech}

## Languages

- Code: {the language mocks are coded in}, tested with {the test runner}
- Interviews: {the languages the user interviews in}; default {one of them}

## Time

- Prep hours: {per weekday}, {per weekend day}

## Speaking

- Recording: {the tool the user answers spoken mocks with, where it leaves each recording, and how its duration is read; or "none: stopwatch"; or "none: estimated"}
- Pace: {words per minute, per interview language, measured {YYYY-MM-DD} over {N} answers; or "not measured"}

## Compensation

- Currency and modality: {e.g. USD, contractor}
- Market: [{research topic, section}]({path}), read {YYYY-MM-DD}
- Anchor: {the top of the range the user says first}
- Target: {what the user aims to sign}
- Floor: {below this, the user walks away}
- Beyond cash: {what weighs in an offer: remote, equity, learning, stability}
```

## The interview

Run it when `PROFILE.md` is missing. Ask one section at a time, in template order: say in one line what the section is used for (Targets decide which requirements and levels the fit measures against, Time sizes each day of the plan), then offer the suggestion below for the user to confirm or change. Write down only what the user confirms.

| Section | Suggestion |
| --- | --- |
| Experience | Read the CV when the user gives one, and propose the lines from it |
| Targets | The role and level the experience points to |
| Languages | TypeScript tested with Vitest; interviews in the conversation's language |
| Time | 1 hour per weekday, 3 per weekend day |
| Speaking | Left for the first spoken mock, which sets it up as MOCK-FORMAT.md lays out |
| Compensation | No suggestion until the market is read: hand the range for the target role, level and region to `research`. Then propose the anchor at the top of that range and the target between its median and its top, as soon as the range returns, even in the middle of a process: never leave it for a later stage. The floor has no suggestion: ask |

Done when every section holds a value the user confirmed (Compensation may wait for `research`, marked pending), and `PROFILE.md` is written with today's date.

## Rules

- **Update it when reality moves.** A new job, a new target, a market re-read: update the section and its date, and tell the user what changed.
- **Pace is measured, never assumed.** After each mock with measured durations, update the pace for that language from every measured answer so far (total words ÷ total minutes).
- **The floor is never said out loud.** Not in a cheat sheet, not in a mock answer, not in any file outside the home. Answers about expectations are built from the anchor.
