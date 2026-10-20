# MAP.md format

`MAP.md` is the one source of truth of an idea: what it is, what it rests on, and how sure we are of each part. A state that changes is rewritten in place; the history lives in `STATUS.md`'s Log.

```md
# {slug}

> {One-line pitch: who, what pain, what you offer.}

- Model: subscription | transactional | one-time | ads
- Created: {YYYY-MM-DD}
- Research topics: [{topic}]({research home}/{topic}/TOPIC.md), ...

## View

{the question, the Mermaid block and the source list `diagram` handed back}

## Problem

| ID | Assumption | Impact | State | Evidence |
| --- | --- | --- | --- | --- |
| P1 | {falsifiable statement} | critical \| high \| low | {state} | {links, or "none yet"} |

## Customer

{same table, IDs CU1, CU2...}

## Solution

{same table, IDs S1...}

## Competition and value added

{same table, IDs V1...}

## Market

{same table, IDs M1...}

## Economics

{same table, IDs E1...}

{the latest run, as ECONOMICS-FORMAT.md lays out, or "Not run yet."}

## Channel

{same table, IDs CH1...}

## Tests

{the test blocks, as TEST-FORMAT.md lays out, or "None."}

## Verdict

{the verdicts, newest first, as LIFECYCLE.md lays out, or "None yet."}
```

## Zones

The seven zones are fixed and always in this order:

| Zone | ID prefix | The question it answers |
| --- | --- | --- |
| Problem | `P` | Does the pain exist, and does it hurt enough to pay? |
| Customer | `CU` | Who exactly suffers it, and how many are they? |
| Solution | `S` | Does what you propose solve that pain? |
| Competition and value added | `V` | Who solves it today, and why would they pick you? |
| Market | `M` | Is it big enough, and is it growing or shrinking? |
| Economics | `E` | Can the numbers close? |
| Channel | `CH` | How do you reach that customer, and at what cost? |

An ID is never reused: a removed assumption leaves a gap in the numbering.

## Assumptions

An assumption is a statement **that can turn out false**. "People want to be more organized" can never be false, so it is not one; "salon owners with 2 to 5 chairs lose more than 3 bookings a week to no-shows" is. Rewrite a vague one until a fact could break it.

Every idea starts with these, which New fills in from the pitch:

- One Value added assumption: "{segment} would pick this over {what they use today} because {what is better}".
- `E1`: "On base inputs the idea reaches the target with a plausible market share", `critical`.

### Impact

- `critical`: if it is false, the idea dies.
- `high`: if it is false, the idea has to pivot (another segment, another price, another channel).
- `low`: if it is false, it is adjusted on the way.

### States

| State | Means | Reached by |
| --- | --- | --- |
| `unknown` | nothing read yet | New |
| `researched (for)` | research tried to break it and failed | Continue |
| `researched (against)` | the facts lean against it, but no `[fact]` proves it false | Continue |
| `researched (mixed)` | the facts point both ways, or are too weak to lean | Continue |
| `in-test` | a test is written and waiting for the user | Test |
| `validated` | a real-world test passed its threshold | Result |
| `dead` | a `[fact]` from a primary source, or a failed test, proves it false | Continue or Result |

```
unknown ──► researched (for | against | mixed) ──► in-test ──► validated
               │                                           └──► dead
               └──► dead   (only on a primary-source [fact] against it)
```

- **Desk research never validates.** It reaches `researched (for)` at most.
- **`[secondary]` and `[inference]` never kill.** Alone they leave an assumption `researched (against)`.
- An assumption already researched is researched again when a fact it rests on expires, or when the user brings new evidence; its state moves between the researched states.
- A `dead` or `validated` assumption only changes when the user explicitly reopens it; the Log says why.

### Evidence

Evidence is a link, never a copied fact:

- A `research` section: `[{topic} § {question}]({research home}/{topic}/TOPIC.md#{anchor})`.
- A test in this map: `[T{n}](#tests)`.
- An economics run: `[run {YYYY-MM-DD}](#economics)`.

## Competition

A Competition and value added assumption asks `research` for a **competitor table** in the industry topic, as the Answer of a section titled "Who solves {the problem} today", every cell backed by a fact under that section's Facts:

```md
| Competitor | Segment | Price | Weakness users report | Source |
| --- | --- | --- | --- | --- |
| {name} | {who it serves} | {price and period, or "free"} | {what reviews or forums complain about} | {fact or secondary, with its source} |
```

The value-added assumption is researched against that table: "better than {competitors} at {what} for {segment}" is broken by a competitor that already does it for that segment.

## The view

`diagram` draws one overview, so it stays within its node limit. Hand it:

- The question: "Where does {slug} stand?"
- The kind: a `flowchart LR` with one node per zone, in the order above, and no edges between them.
- Each node's label: the zone's name and its counts by state (`Problem · 1 for · 1 unknown`).
- Each node's color: the state of its riskiest assumption, in this order from worst to best: `dead` > `researched (against)` > `unknown` > `researched (mixed)` > `in-test` > `researched (for)` > `validated`.
- The source: this `MAP.md`.

Write what it hands back under `## View`, replacing the previous view. Redraw it every time a state changes. With no Node, `diagram` marks it unverified; the tables stay the source of truth.

# STATUS.md format

```md
# {slug}

- State: exploring | testing | discarded | parked
- Target: {amount} {currency} a month, or "break-even"
- Verdict: {the latest verdict} on {YYYY-MM-DD}, or "none yet"

## Log

- {YYYY-MM-DD} · {one line: what happened, and why}
```

The Log is append-only. Every intent that changes the idea writes one line: an assumption's new state and the fact behind it, a test written, a result, an economics run, a verdict, an outcome, a declined offer of a test.

# IDEAS.md format

`<ideas home>/IDEAS.md` keeps every idea Generate proposed and the user did not pick, newest last:

```md
# Ideas not picked

- {YYYY-MM-DD} · {pitch} · Pays: {who} · Would die if: {the assumption most likely to kill it} · From: {the starting point}
```
