# grounding.md Format

`grounding.md` is what exists today and what the work competes with, every claim cited. Scope, estimate and proposal all build on it, so an uncited claim here becomes an unfounded price later.

## Template

```md
# Grounding · {Client} · {engagement}

Source: repo | running system | client documents | nothing
Consulted: {YYYY-MM-DD}

## Today

- {What exists and works, one fact per line} ({citation})
- {What is broken, risky or missing} ({citation})

## Defects

- {Defect} ({citation}) · risk: {what it costs the client} · warranty: yes | no

## The alternative

{What the client would do instead: a product, a vendor, a spreadsheet, doing nothing.}
- Price: {amount and period, or "none"} ({source}, {YYYY-MM-DD})
- Paid today: {yes | no; a trial or an evaluation is no} ({source}, {YYYY-MM-DD})
- What it does that this work will not, and the reverse.

## External costs

| Item | Plan | Cost | Why this plan | Source (consulted) |
| --- | --- | --- | --- | --- |

## Earlier engagements

- {engagement} · {state} · {what it delivered that this one builds on}
```

## Citations, by source kind

- **Repo:** `path:line` for every claim about the code.
- **Running system:** the URL or screen, and what was seen there.
- **Client documents or messages:** which document or message, quoted briefly.
- **Nothing:** Today reads "built from scratch", and Defects is left out.

## Rules

- **Warranty** marks a defect in work the user delivered earlier (a footer, a commit author, an earlier engagement says so). It is fixed free in Phase 0; say how you know it is theirs.
- **The alternative with no price** (doing nothing, an in-house option) still gets named; its price reads "none", and the quote carries no break-even.
- **External costs** are the running costs the client will pay: hosting, services, licences, per-use fees. Each row has its source and the date you consulted it; a price you could not verify reads "unverified" and becomes an assumption.
- **Earlier engagements** is left out for a client's first one.
