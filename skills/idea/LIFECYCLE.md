# Lifecycle

What happens to an idea once its map exists. Each section is one intent from SKILL.md and runs on the idea it resolved.

```
exploring ──▶ testing
    │  ▲         │
    │  └─────────┤
    ├──▶ parked ─┤
    └──▶ discarded
```

Any state may go back to `exploring`.

## Verdict

The user asks for the verdict. It can be asked at any time; the rules say what it can be.

1. Read `MAP.md`. When the economics run is stale, or a fact the map rests on has expired, say so first and offer to re-verify through `research`; the user may ask for the verdict as it stands.
2. Apply the rules **top to bottom**; the first that matches is the verdict:

| Verdict | When |
| --- | --- |
| **Discard** | A `critical` assumption is `dead`, or the latest economics run doesn't close |
| **Not enough information** | A `critical` assumption is still `unknown`: Continue has not reached it, or research found nothing either way |
| **Worth testing** | None of the above: no critical dead, none unknown, the economics close on base, and every critical left `researched (mixed)` or `researched (against)` is in To test next |

A critical `researched (against)` counts as `researched (mixed)` in these rules, and is named first among the assumptions to test and as the best reason not to do it. A critical `in-test` counts as the state it had before the test (its block's Before), and is listed under To test next as already running, as is a critical whose test stays open after an inconclusive Result (TEST-FORMAT.md, Result). `E1` is never tested itself: To test next lists in its place the test ECONOMICS-FORMAT.md, Writing a run, step 5, offers for it.

3. Write the verdict at the top of `## Verdict`, keeping the previous ones below it, and copy its name and date into `STATUS.md`:

```md
### {YYYY-MM-DD} · {Discard | Not enough information | Worth testing}

- Why: {the rule that matched, with the assumption IDs and the economics result}
- Best reason not to do it: {one or two lines, linked; then every impact lowered after research since the previous verdict}
- To test next: {every critical left mixed or against, at least 2, each with the test kind that settles it} (Worth testing only)
- Still unknown: {the critical IDs} (Not enough information only)
- Rests on: {the research sections and the economics run, and the earliest expiry among their facts}

#### What this idea demands

- Capital to start: {range and currency}: {what it goes to}
- Key skills: {the two or three that decide it, e.g. "selling B2B by phone", "content SEO"}
- Hours a week: {to an MVP} · {to operate it}
- Access: {who must be reached, and how many: "50 salon owners"}
- Time to first revenue: {range}
- Hardest part: {one line}
```

**The best reason not to do it is always written**, even for "worth testing": the strongest fact or assumption against the idea, and every impact lowered after research since the previous verdict, with the reason the Log gives. Not finding one means the research did not look hard enough: go back to the weakest critical assumption.

**What this idea demands describes the work, never the user.** It never says whether the user can do it: the user compares it with what they have. Each line that rests on a fact links it; the rest is an `[inference]`, named as such.

4. Show the verdict, and ask what the user wants to do (Outcome). "Worth testing" offers to design the tests to test next (TEST-FORMAT.md).

Done when the verdict is written with its reason, the best reason not to do it and what the idea demands, `STATUS.md` has it, and the Log has the line.

## Outcome

The user decides. Set the state in `STATUS.md` and log the reason in the user's words:

- **testing**: the user will run tests. When the latest verdict is not "worth testing", say what it is first; the user decides anyway. Offer Test for each assumption to test next.
- **parked**: good, not now. Nothing else changes; List keeps showing it, with its verdict going stale as its facts expire.
- **discarded**: the reason is logged. The map stays as it is: it is what the next idea in the same industry learns from, and its `research` topics stay for that idea.
- **exploring**: back to work on the map; Continue picks the next assumption.

Done when `STATUS.md` has the new state and the Log has the reason.

## Stale verdicts

A verdict is **stale** when a fact it rests on has expired, as `research` defines expiry, or when an assumption changed state after the verdict's date. List shows it as stale, and Continue says so before picking. A stale verdict is never handed back as current: offer to re-verify the expired facts through `research`, or just issue it again when only states changed.
