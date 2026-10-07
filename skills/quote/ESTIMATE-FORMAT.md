# estimate.md Format

`estimate.md` is the scope and its hours. Scope fills it before Checkpoint 1; Estimate adds the hours after. It is internal.

## Template

```md
# Estimate · {Client} · {engagement}

## Phase 0 · before adding anything

| Defect | Fix | Warranty |
| --- | --- | --- |
| {from grounding.md} | {what gets done} | yes | no |

## Modules

Tags: ✅ asked · 💡 proposed · ⏸ later

### Phase {n} · {name the client would use}

#### M{k} · {module} {tag}
- {What it does, in the client's words}
- {Why, when the tag is 💡: the problem it solves}

### Later ⏸

#### M{k} · {module} ⏸
- {What it is, and what it would take}

## Not recommended

- {What the client asked for or the alternative offers, and why it does not fit them}

## Open questions

| # | Question for the client | Assumption the quote makes |
| --- | --- | --- |

## Hours

Hours cover the work, its tests, deploy and documentation. The low end is "everything goes as expected".

| Phase | Module | Low | High |
| --- | --- | --- | --- |
| 0 | {fix} | | |
| | **Phase {n} subtotal** | | |
| | **Total core (Phases 0–{n})** | | |
| ⏸ | {later module} | | |

## History

{"In your last N engagements, actual hours were X× the priced hours." or "No actuals yet."}
```

## Rules

- **Hours are the base of every price**, even when the work is sold by the deliverable: a deliverable's price comes from the hours it takes.
- **Phases** each ship something the client can use before the next one starts. Order them by what the client asked for most; say when a later phase could move earlier.
- **Phase 0** holds what must be fixed before anything is added on top: security holes, data at risk, broken foundations. When grounding found no defects, the section reads "Nothing to fix first".
- **Later ⏸ modules** get hours too, so the client can see what they would cost; they stay out of the core total.
- **Not recommended** names things on purpose, with the reason, so the client sees they were considered. When there are none, the section reads "None".
