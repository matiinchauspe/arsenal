# `idea` skill: design

Date: 2026-10-20 · Target version: arsenal 0.6.0

## Purpose

Take a new product, startup or digital-business idea, of any industry, from a vague sentence to an
explicit decision: worth testing, discard, or not enough information. The idea is walked as a **map
of falsifiable assumptions**, and each step lowers uncertainty with labeled, sourced, dated evidence.
The skill never promises certainty: what it guarantees is that every number shows where it came
from, every test has its pass/fail threshold fixed before it runs, and the decision stays the user's.

Speed comes first. Desk research is the default and the only required path; real-world tests are
offered, never required.

## Decisions

| Decision | Choice | Why |
| --- | --- | --- |
| Entry point | The user brings an idea (**New**) or a starting point to generate one from (**Generate**) | Both happen; generating is a short door into the same flow |
| Map shape | Assumptions grouped in 7 fixed zones, each with impact and state | Tells you where to go next: the riskiest, least-evidenced assumption, not the next empty box |
| Evidence | Desk research by default; real-world tests optional | The user wants speed; tests are for the idea that survives the desk |
| Economics | Unit economics with pessimistic/base/optimistic ranges and a sensitivity pass | Answers "can this close, and what does it hinge on?" without a 3-year P&L's false precision |
| Founder fit | No profile; the verdict lists **What this idea demands** and the user compares | The user's profile must never discard an idea up front |
| Map format | `MAP.md` as source of truth, with a Mermaid view drawn by `diagram` | Versionable, readable by any agent, same convention as the rest of arsenal |
| Architecture | `idea` owns the map, the economics and the verdict; market facts live in `research` topics and are linked | Facts expire and get re-verified; two ideas in one industry share research |
| Calculations | A fixed stdlib-only `economics.py` | Same inputs, same outputs; an LLM doing mental arithmetic on money is the soft measurement this skill exists to avoid |

Rejected: a self-contained skill that researches into the map (duplicates `research`, facts never
expire); two skills `idea-generate` + `idea-validate` (YAGNI); an interactive HTML map (maintenance
on every change); a full financial projection (invented numbers with decimals); a founder profile
(rejected by the user).

## Location and files

- Invoked by the user only (`disable-model-invocation: true`): `/arsenal:idea <idea>: <what to do>`.
- The **ideas home** is `$ARSENAL_IDEAS_HOME` when set, else `~/ideas`.
- Each idea is `<ideas home>/<slug>/` with:
  - `MAP.md`: the source of truth. One-line pitch, revenue model, the 7 zones with their
    assumptions, the economics, the Mermaid view, the tests and the latest verdict.
  - `STATUS.md`: the idea's state and an append-only log.
- `<ideas home>/IDEAS.md`: one line per idea that Generate proposed and the user did not pick.
- Writes happen only inside the ideas home, and inside the research home through `research`. The
  repo the session was opened in is never written to.
- An idea keeps the language of the conversation that created it.

### Idea states

`exploring → testing | discarded | parked`. `testing` is reached when the verdict is "worth testing"
and the user decides to test. `parked` is "good, not now". Any state may return to `exploring`.

## Intents

| Intent | Example argument | What it does |
| --- | --- | --- |
| **List** | (nothing) | Lists ideas with state, latest verdict and expired facts; offers to continue one or generate a new one |
| **Generate** | `generate: I'm an accountant and I see that...` | Proposes 3-5 ideas from a problem, an industry or a skill; the user picks one into **New** |
| **New** | `salon-bookings: an app so that...` | Creates the folder, writes the pitch and revenue model, proposes the initial assumptions per zone |
| **Continue** | `salon-bookings` | Researches the critical assumption with the least evidence |
| **Test** | `salon-bookings: design the interview` | Optional: designs the test of an assumption, threshold fixed first |
| **Result** | `salon-bookings: did 6 interviews, 4 said...` | Records the result against the threshold; the assumption becomes `validated` or `dead` |
| **Verdict** | `salon-bookings: verdict` | Issues the verdict with "What this idea demands" |
| **Outcome** | `salon-bookings: I'm discarding it` | Changes the idea's state and logs why |

An argument is split at its first colon into the idea slug and the rest. A slug close to an existing
idea asks whether it is the same idea. Every intent appends one line to `STATUS.md`'s log.

## The map

### Zones

Fixed, always in this order:

| Zone | The question it answers |
| --- | --- |
| **Problem** | Does the pain exist, and does it hurt enough to pay? |
| **Customer** | Who exactly suffers it, and how many are they? |
| **Solution** | Does what you propose solve that pain? |
| **Competition and value added** | Who solves it today, and why would they pick you? |
| **Market** | Is it big enough, and is it growing or shrinking? |
| **Economics** | Can the numbers close? |
| **Channel** | How do you reach that customer, and at what cost? |

### Assumptions

An assumption is a statement **that can turn out false**. A vague one ("people want to be more
organized") is rewritten until it is falsifiable ("salon owners with 2-5 chairs lose more than 3
bookings a week to no-shows"). Each one has:

- **ID** by zone: `P1`, `CU2`, `S1`, `V1`, `M1`, `E1`, `CH1`.
- **Impact:** `critical` (if false, the idea dies), `high` (forces a pivot), `low` (adjusted on the way).
- **State**, with these transitions only:

```
unknown ──► researched (for | against | mixed) ──► in-test ──► validated
               │                                           └──► dead
               └──► dead   (only on a primary-source [fact] against it)
```

- **Evidence:** links to `research` sections, or to a test in `MAP.md`. Never a copied fact.

Two rules:
- **`validated` is reached only through a real-world test.** Desk research stops at "researched (for)".
- **Desk research can kill.** A law that forbids it, or four competitors giving it away free, is a
  `[fact]` against it.

New proposes 2-4 assumptions per zone from the pitch; the user corrects, removes or adds.

### Continue: what gets researched

1. Pick the `critical` assumption with the least evidence (`unknown` before `researched (mixed)`);
   on a tie, the cheapest to research. With no critical left open, the same over `high`.
2. Run the `research` flow on the industry topic (e.g. `salons-ar`) or a cross-cutting one (e.g.
   `online-payments-ar`), with the question **phrased to refute the assumption**: research looks for
   evidence against it, never for confirmation. What survives an attempt to break it is worth
   something.
3. Set the assumption's state from the facts, link them, redraw the view, log it.

Competition gets a competitor table in its `research` topic (name, segment, price, the weakness
users complain about, source); the value-added assumption states "better than {competitors} at
{what} for {segment}" and is researched against that table.

### The view

`diagram` draws the map: zones as subgraphs, assumptions as nodes colored by state. It lives in
`MAP.md` and is redrawn when a state changes.

## Economics

### Revenue model

Detected from the pitch, corrected by the user:

| Model | Revenue per customer per month |
| --- | --- |
| Subscription | price |
| Transactional (marketplace, commission) | volume × take rate |
| One-time sale | price × repurchase rate ÷ months between purchases |
| Ads / audience | users × ad ARPU |

### Inputs

Each with pessimistic / base / optimistic values, each value labeled and sourced:

- **Price:** from the competitor table. If nobody charges for anything similar, that is information.
- **Gross margin:** variable cost per customer (infra, payment fees, AI tokens, support).
- **CAC:** from the Channel zone; an industry benchmark is `[secondary]`, never `[fact]`.
- **Churn / retention:** benchmark for the model and segment.
- **Fixed monthly costs:** the minimum to operate.
- **Reachable market:** from the Market zone.
- **Target:** asked once per idea ("how much a month do you want it to make?"); none → break-even.

### Outputs

- **LTV** = monthly revenue per customer × gross margin ÷ monthly churn
- **LTV / CAC** (below 3 is a warning; below 1 every customer loses money)
- **CAC payback** in months
- **Customers needed** for break-even and for the target
- **Market share needed** = customers needed ÷ reachable market: the reality check
- **Sensitivity:** each input moved to its pessimistic value alone, the rest at base; the input that
  moves customers-needed the most is **the deciding variable**, and becomes a `critical` assumption
  in the Economics zone if it is not one already.

### `economics.py`

Stdlib-only Python. Reads a JSON of inputs (model, ranges), prints a table of outputs for the three
scenarios plus the sensitivity ranking. The agent writes the JSON, runs the script and pastes its
output with each formula and its inputs into `MAP.md`. Every derived number comes from the script,
never from the agent's head. Without `python3` the skill says so and stops the economics step.

### Economics result

- **Doesn't close:** base inputs do not reach break-even, or the market share needed is not plausible.
- **Closes, but hinges on X:** closes on base, not on pessimistic; X is the deciding variable.
- **Closes comfortably:** closes even on pessimistic. Rare; the inputs get a second look.

## Verdict

| Verdict | When |
| --- | --- |
| **Discard** | A critical assumption is `dead`, or the economics don't close |
| **Not enough information** | A critical assumption is still `unknown`: Continue has not reached it, or research found nothing either way |
| **Worth testing** | No critical dead, none unknown, economics close on base; every critical left `mixed` is among the assumptions to go test |

Rules are checked top to bottom; the first that matches is the verdict.

Every verdict carries:
- **The best reason NOT to do it**, even when positive.
- **The 2-3 assumptions to go test**, when "worth testing".
- **Its date.** When a fact it rests on expires in `research`, List and Continue show the verdict as
  **stale** and offer to re-verify before the user decides anything.

### What this idea demands

Describes the work, never judges the user: initial capital (range) and what it goes to; key skills;
hours a week to an MVP and to operate it; access needed ("reach 50 salon owners"); time to first
revenue; the hardest part to execute, in one line.

## Tests (optional)

Offered when a critical assumption stays `mixed`; the user may decline. The cheapest test that can
settle it:

- **Interviews:** questions about what the person **did**, never what they would do.
- **Smoke test:** a landing page and a conversion metric.
- **Pre-sale or deposit:** the strongest signal there is, because it is real money.

Each test is written **before** it runs: assumption, method, sample size, metric, pass/fail
threshold, date. The assumption goes to `in-test`. **Result** compares against that threshold. The
threshold never moves afterwards: changing it is a new test, and the log shows it changed.

## Generate

From a problem, an industry or a skill (asked on the spot; there is no profile), propose 3-5 ideas,
each with a one-line pitch and the assumption most likely to kill it. No research yet: it is a quick
filter. The picked one goes to New; the rest are appended to `IDEAS.md`.

## Skill files

```
skills/idea/
├── SKILL.md            # location, intents, Continue, anti-bias rule
├── MAP-FORMAT.md       # zones, assumptions, states, transitions, MAP.md + STATUS.md
├── ECONOMICS-FORMAT.md # revenue models, ranged inputs, formulas, sensitivity, economics.py contract
├── TEST-FORMAT.md      # test kinds, threshold first, Result
├── LIFECYCLE.md        # Verdict, What this idea demands, Outcome, stale verdicts
└── economics.py        # deterministic calculator, stdlib only
```

## Testing

1. `claude plugin validate .`
2. `economics.py` run against a hand-checked input for each revenue model.
3. A real run with one of the user's ideas in `ARSENAL_IDEAS_HOME=~/ideas-test`: Generate or New →
   3-4 Continue → economics → Verdict.
4. Audit the transcript against the skill text: where the agent deviated, where the text was
   ambiguous; one round of fixes.

## Release

README table row and a "where your ideas live" section; CHANGELOG `0.6.0`; `plugin.json` `0.6.0`.
