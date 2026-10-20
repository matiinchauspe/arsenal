# Lifecycle

What happens to a process after its setup. Each section is one intent from SKILL.md and runs on the process it resolved.

```
open ──advance──▶ open ──offer──▶ offer ──▶ accepted
  │                                 │
  ├──▶ rejected                     ├──▶ rejected (declined either way)
  └──▶ withdrawn                    └──▶ withdrawn
```

## Advance

The user moved to a new stage, or learned of one.

1. When the last stage that happened has no debrief, offer one first: its questions are what the next stage plans from.
2. Write the last stage's Result, and add the new stage with its kind and date (`unknown` when not said) to the Stages table.
3. Replan `fit.md` from today, as FIT-FORMAT.md lays out, and show the new plan rows.

Done when the Stages table holds the new stage, the plan reaches its date, and the Log has the line.

## Debrief

The user had a stage and tells how it went. Read [QUESTIONS-FORMAT.md](./QUESTIONS-FORMAT.md), number the debrief with the highest under `debriefs/` plus one, and write it with the user.

- Feed the root: every question into the Log of `QUESTIONS.md`, rebuild the weak spots, and update the stories used.
- When the user already knows the result, write it in the Stages table as Advance does.
- Replan the next stage in `fit.md` from what the debrief says the company cares about.

Done when the debrief is written, the root is updated, and the Log has the line.

## Offer

The company made an offer. Write `offer.md` in the process and set the state to `offer`.

```md
# Offer · {Company} · {role}

- Received: {YYYY-MM-DD} · Answer by: {date, or "not said"}

| Part | Offered | Notes |
| --- | --- | --- |
| Base | {amount, currency, period} | |
| Modality | {employee \| contractor, via whom} | |
| Bonus | {amount or %, and on what condition} | |
| Equity | {amount, vesting, cliff} | |
| Benefits | {health, equipment, learning, time off} | |
| Remote | {as offered} | |
| Start | {date} | |

## Compared

- Yearly total, in {PROFILE.md's currency}: {amount}{, converted at {rate} from {source} on {date}}
- Against PROFILE.md: {below the floor \| between floor and target \| at or above the target}
- Other processes: {each open process and its stage, or "none"}

## Counter

- Ask: {the number and the parts}
- Reason: {the market range, the scope of the role, another process}
- Also ask: {what else is negotiable}
```

1. Fill the table from what the user has; ask for the parts the offer left out, since the full package is worth asking for anyway.
2. Compare the yearly total in `PROFILE.md`'s currency and modality: a contractor's base pays its own taxes and benefits, so say what that does to the comparison. Read an exchange rate from a source and cite it.
3. Below the floor, say so plainly. The user decides; the comparison does not.
4. Propose the counter from the target and the market, and offer a `negotiation` mock in simulation, with the agent as a recruiter who pushes back. **Another offer is a reason only when it is real**: never suggest inventing one.

Done when `offer.md` is written, the comparison is told, and the counter is proposed. The user sends it.

## Outcome

The process ended.

- **Accepted**: log the final terms in `offer.md` and set the state to `accepted`. Then list the other open processes and ask whether to withdraw from each; withdraw only on the user's word.
- **Rejected**: set the state, and run a short retro with the user: the reason, when the company gave one (ask once; "none given" is a valid answer), and what the debriefs point to. What it teaches goes into the weak spots of `QUESTIONS.md`, so the next process starts from it.
- **Withdrawn**: set the state and log the reason in one line.

Done when the state is final and its Log line names the terms, the reason or the lesson.
