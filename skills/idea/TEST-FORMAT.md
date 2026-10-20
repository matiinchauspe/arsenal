# Test format

A test is how an assumption leaves the desk. It is **always optional**: offer it when a critical assumption is left `researched (mixed)` or `researched (against)`, or `unknown` with `nothing found`, or when the user asks, never for `E1` (ECONOMICS-FORMAT.md, Writing a run); a declined offer is logged and the work goes on. **The threshold is written before the test runs, and never moves afterwards**: a threshold set after the result is a way of convincing yourself it passed.

## Kinds

Pick the cheapest kind that can settle the assumption:

| Kind | Settles | Typical threshold |
| --- | --- | --- |
| `interviews` | whether the problem exists and hurts (Problem, Customer) | "at least 4 of 6 lost a booking to a no-show in the last month" |
| `smoke-test` | whether people want the solution enough to act (Solution, Value added, Channel) | "at least 5% of 200 visits leave their email" |
| `pre-sale` | whether they pay (Economics, Value added) | "at least 3 of 20 asked pay the deposit" |

A pre-sale is the strongest signal there is, because it is real money; prefer it whenever the user can sell before building.

### Interviews

The questions ask about what the person **did**, never what they would do. Everyone says they would use it, and almost nobody pays.

- Ask about the last time it happened: "When did a client last miss a booking? What did you do?"
- Ask what it cost them and what they already tried: someone who never looked for a fix does not hurt enough.
- Never pitch before the questions are done: once they know the idea, they are polite about it.
- Count what happened, never opinions: "lost a booking last month" counts, "it would be useful" does not.

Write 5 to 8 questions in the test block.

### Smoke test

Write what the page must say (the pitch, the price when it is being tested, one call to action) and where the traffic comes from. The skill does not build the page.

## The test block

Under `## Tests` in `MAP.md`, numbered `T1`, `T2`... and never reused:

```md
### T{n} · {assumption ID} · {kind}

- Written: {YYYY-MM-DD}
- Assumption: {ID}: {statement}
- Before: {the assumption's state when the test was written}
- Method: {what the user does, step by step}
- Sample: {how many, who, where to find them}
- Metric: {what is counted}
- Passes when: {the threshold, as a number}
- Questions: {interviews only: the numbered questions}
- Result: pending
```

## Test

1. Name the assumption, or take the one Continue would pick among the critical ones it offers a test for (SKILL.md, Continue, step 5).
2. Propose the kind, the sample, the metric and the threshold, and say why that threshold: what result would make you believe it, and what would not.
3. **Checkpoint:** the user corrects the block; then write it with the assumption's current state as **Before**, set the assumption to `in-test`, link the test, redraw the view and log it.

Done when the block is written with a threshold, and the assumption is `in-test`.

## Result

The user ran a test and tells what happened.

1. Write the raw numbers the user gives under the block's Result, with the date: "6 interviewed, 4 lost a booking last month". Quotes from interviews go in as said.
2. Compare against **Passes when**, and nothing else:
   - Meets **Passes when** → `validated`.
   - Misses it → `dead`.
   - A smaller sample than the block says: **inconclusive**. The assumption goes back to the block's **Before** state, and the test stays open.
3. A user who wants a different threshold after seeing the result gets a new test, `T{n+1}`, with the new threshold; the Log says it changed from what to what. The result already in stays judged against the old threshold.
4. Link the result, redraw the view, log it, and say what changed in the verdict, if there is one.

Done when the result is written, the assumption has its state from the threshold, and the Log has the line.
