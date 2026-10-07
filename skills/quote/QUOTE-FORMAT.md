# quote.md Format

`quote.md` is the internal quote: the price and every piece of reasoning behind it. It is for the user only, so it can say plainly what the proposal never will: the rate, the hours, the margin of safety, the arguments to make in the room.

## Template

```md
# Quote · {Client} · {engagement} · v{N} (internal)

Date: {YYYY-MM-DD}

## Policy snapshot

| Value | Used here | Source |
| --- | --- | --- |
| Hourly rate | {amount} | POLICY.md ({its Updated date}) |
| Charged in | {currency and rate} | POLICY.md |
| Exchange rate | {rate} | {source}, {YYYY-MM-DD} |
| Pricing rule | {rule} | POLICY.md |
| Payment terms | {terms} | POLICY.md |
| Retainer | {terms} | POLICY.md |
| Capacity | {hours per week} | POLICY.md |

## Exceptions

- {Value that departs from POLICY.md} · {why, for this client}

## Warranty

- {Phase 0 item fixed free} · {how we know it is the user's own work} · own cost ≈ {hours}
- {How to say it to the client}

## Price per phase

| Phase | Content | Range (h) | Priced (h) | Price | ≈ charged currency | Delivery |
| --- | --- | --- | --- | --- | --- | --- |
| | **Total** | | | | | |

## Retainer

- Infrastructure: {item} {cost} ({source}, {YYYY-MM-DD}), …
- Support: {hours} h a month
- Beyond that: {rate} per hour
- **Monthly: {amount}**

## Break-even

{Cumulative spend, month by month, of this work against the alternative, and the month this work becomes cheaper. State the assumption about the alternative's price over time.}

## Lever

- {If the price is too heavy: the smaller scope that still solves what the client asked for, and its price}

## Selling points

1. {An argument that holds even when this work is not the cheaper option}
```

## Rules

- **Snapshot** every value used, with its date, so a later change to `POLICY.md` never rewrites this quote. A row for a value the policy does not need (no exchange rate when the quote and charged currencies match) is left out.
- **Exceptions** reads "None" when the quote follows the policy throughout.
- **Warranty** is left out when Phase 0 has no warranty items.
- **Delivery** is the phase's high-end hours ÷ the capacity, rounded up to whole weeks. A delivery the user sets by hand at Checkpoint 2 is recorded as given, with no confirmation round, and goes in Exceptions with its reason; when it is shorter than the computed one, the reason also states the hours per week it implies.
- **The lever** follows the policy's Lever line; the cut it proposes is in scope, priced like any other phase.
- **`quote.html`**, a rendering of this file with a break-even chart, is written only when the user asks for it, following the HTML rules in [PROPOSAL-FORMAT.md](./PROPOSAL-FORMAT.md).
