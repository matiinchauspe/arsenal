# Economics format

The economics answer one question: **can this close, and what does it hinge on?** They are unit economics with three scenarios, never a multi-year projection: at the idea stage a P&L is invented numbers with decimals. **Every derived number comes from `economics.py`**, never from your head.

## Models

The model sets how a customer pays. Propose it from the pitch; the user corrects it.

| Model | Revenue per customer per month | Model inputs |
| --- | --- | --- |
| `subscription` | price | `price` |
| `transactional` | volume × take rate | `volume` (what a customer moves a month), `take_rate` (0 to 1) |
| `one-time` | price ÷ months between purchases | `price`, `months_between_purchases` |
| `ads` | ad revenue per user | `ad_arpu` (a customer is a user) |

For `one-time`, `monthly_churn` is the monthly share of buyers who never buy again.

## Inputs

Every model also takes:

| Input | What it is | Where it comes from |
| --- | --- | --- |
| `gross_margin` | 0 to 1: what is left of the revenue after the cost of serving the customer (infra, payment fees, AI tokens, support) | the provider's own prices, read by `research` |
| `cac` | cost to acquire one customer | the Channel zone; an industry benchmark is `[secondary]`, never `[fact]` |
| `monthly_churn` | 0 to 1: the share of customers lost each month | a benchmark for the model and the segment |
| `fixed_costs` | the minimum a month to operate | the providers' prices plus what the user says they would spend |
| `reachable_market` | how many customers the idea can reach | the Market zone |

`price` comes from the competitor table (MAP-FORMAT.md, Competition). When nobody charges for anything similar, say so: that is information, and the price is then an `[inference]` named as such.

Every input has three values: **pessimistic** (bad for the business: low price, high CAC, high churn), **base** and **optimistic**. Each value is labeled as TOPIC-FORMAT.md in `research` defines and links the fact it comes from. A value with no linked fact can only be the user's own estimate (Running, step 1), labeled `[unverified]`. No value, and no target, may be above 1e12: `economics.py` rejects it.

**The target** is asked once per idea: "how much a month do you want it to make, once costs are paid?" It is written in `STATUS.md`; with no answer, the target is break-even (0).

**The plausible share** (`max_share`) is the largest share of the reachable market the idea may need. It defaults to 10%, a rule of thumb; the user may change it, and the run says which was used.

## Running

1. For each value with no linked fact, hand `research` a question for it, or ask the user for their estimate (labeled `[unverified]`, user's estimate); never fill one from memory. When E1 is picked again because an input's fact expired, hand that fact to `research` to re-verify first.
2. Write `<idea>/economics.json`:

```json
{
  "model": "subscription",
  "currency": "USD",
  "target": 1000,
  "max_share": 0.10,
  "inputs": {
    "price": {"pessimistic": 15, "base": 20, "optimistic": 25},
    "gross_margin": {"pessimistic": 0.7, "base": 0.8, "optimistic": 0.85},
    "cac": {"pessimistic": 60, "base": 40, "optimistic": 30},
    "monthly_churn": {"pessimistic": 0.08, "base": 0.05, "optimistic": 0.03},
    "fixed_costs": {"pessimistic": 800, "base": 500, "optimistic": 400},
    "reachable_market": {"pessimistic": 5000, "base": 10000, "optimistic": 15000}
  }
}
```

3. Run `python3 <this skill's folder>/economics.py <idea>/economics.json`. It exits 2 with the reason on a wrong input: fix the JSON and run it again.
4. Without `python3`, tell the user, and stop the economics: `E1` stays where it is, and the verdict cannot be "worth testing" until a run exists.

## Formulas

What the script computes, written under every run so anyone can redo it:

- **Contribution** = revenue per customer × gross margin
- **Net contribution** = contribution − monthly churn × CAC: what a customer leaves once replacing the customers who churn is paid for
- **LTV** = contribution ÷ monthly churn
- **LTV / CAC**: below 3 is a warning; below 1 every customer loses money
- **CAC payback** = CAC ÷ contribution, in months
- **Customers needed** = (fixed costs + target) ÷ net contribution, rounded up; for break-even the target is 0
- **Market share needed** = customers needed ÷ reachable market
- **Sensitivity**: each input except the reachable market moved to its pessimistic value alone, the rest at base, ranked by how many customers it adds. The first is **the deciding variable**.

A scenario **closes** when its net contribution is positive and its market share for the target is at most `max_share`. The **result**:

- **doesn't close**: the base scenario does not close.
- **closes, but hinges on {X}**: base closes, pessimistic does not. X is the deciding variable.
- **closes comfortably**: even pessimistic closes. Rare: give the inputs a second look, and say so.

## Writing a run

Under the Economics zone's table in `MAP.md`, on top of the previous runs, which are kept below it so a verdict's `run {date}` link still resolves:

```md
### Run {YYYY-MM-DD}

| Input | Pessimistic | Base | Optimistic | Source |
| --- | --- | --- | --- | --- |
| {input} | {value} | {value} | {value} | {label and link for each value} |

{the script's output, pasted as it printed it}

{the Formulas list above}
```

Then:

1. Set `E1` from the result: **closes comfortably** or **closes, but hinges** → `researched (for)`; **doesn't close** → `researched (against)`. When the deciding variable's base value is `[unverified]`, E1 goes to `researched (mixed)` at most. Link the run.
2. When the deciding variable is not already a `critical` Economics assumption, add one, `critical`, and say so: "{input} is no worse than {its base value}", that is at most it for `cac`, `monthly_churn`, `fixed_costs` and `months_between_purchases`, and at least it for the rest.
3. Log the run with its result.

`E1` waits until at least one Competition and value added assumption (for the price), one Channel assumption (for CAC) and one Market assumption (for the reachable market) is in any state but `unknown`, whatever its impact; one left `unknown` with `nothing found` also counts, and its input is then the user's estimate (Running, step 1). Continue picks those ahead of `E1`, even when they are `low`; a zone with none gets one added, impact `high`, and the user is told. A run is **stale** when a fact one of its inputs links has expired; Continue runs it again after `research` re-verifies that fact.
