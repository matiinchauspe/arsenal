---
name: quote
description: Quote a piece of work for a client: a priced proposal for them, an internal quote for you, tracked from draft to sent to outcome.
disable-model-invocation: true
argument-hint: "<client>: what they want, or what happened (sent, accepted, actual hours)"
---

Every quote produces two documents for two audiences: `proposal.html` for the client, and `quote.md`, which is internal. **The reasoning behind the price never crosses into the proposal.**

## Locating the engagement

An **engagement** is one piece of work quoted to one client, kept in one folder. The **quote home** is `$ARSENAL_QUOTES_HOME` when set, else `~/quotes`. It holds `POLICY.md` (the user's pricing policy, shared by every engagement) and one folder per client, slugged in kebab-case: `<quote home>/<client>/<YYYY-MM-engagement>/`. The month is the one the engagement starts in; it dates every price and exchange rate inside.

1. Slug the client the argument names. If it is close to an existing client folder, ask whether it is the same client.
2. Read the intent from the rest of the argument; when it fits none of these, ask what the user wants to do:

| Intent | Example argument | Engagements it targets | Then |
| --- | --- | --- | --- |
| **New** | `acme: they want a booking page` | none (create the folder) | [The flow](#the-flow) from Ground |
| **Revision** | `acme: they answered the questions…` | `draft` or `sent` | [The flow](#the-flow) from Scope, as described in [Revisions](#revisions) |
| **Sent** | `acme: sent it` | `draft` | Read [LIFECYCLE.md](./LIFECYCLE.md) and follow its Sent section |
| **Outcome** | `acme: accepted Phase 2 only` | `sent` | Read [LIFECYCLE.md](./LIFECYCLE.md) and follow its Outcome section |
| **Actual hours** | `acme: Phase 2 took 50 h`, `acme: finished` | `accepted` | Read [LIFECYCLE.md](./LIFECYCLE.md) and follow its Actual hours section |

3. Among the client's engagements in a targeted state: exactly one → use it; several → ask which; none → tell the user what states the client's engagements are in, and stop.
4. For **New**, name the engagement folder from today's month and a short slug of the work, and create it.

Done when you hold one absolute engagement path and one intent, and have told the user both. Every file below is relative to that folder, except `POLICY.md`, which lives at the quote home root.

## Where things are written

Write only inside the quote home. A client's repo, system or documents are read for grounding and stay untouched, so the rate can never leak through a commit; copying the proposal anywhere else is the user's own act.

Every engagement keeps a `STATUS.md`, which every intent reads and updates:

```md
# {Client} · {engagement}

- State: draft | sent | accepted | rejected | closed
- Version: v{N}
- Signer: {identity name, or "unset"}
- show_hours: {true | false | unset}

## Hours

| Phase | Estimate (h) | Priced (h) | Actual (h) |
| --- | --- | --- | --- |
| {phase} | {low}–{high} | {hours the price is built on} | {blank until recorded} |

## Log

- {YYYY-MM-DD} · {state} v{N} · {one line: what happened, and why}
```

The Log is append-only: one dated line for each thing that happens to the engagement.

## The flow

Five steps and two **checkpoints**. Between checkpoints, work unattended: research infrastructure prices, the exchange rate and the alternative yourself, and cite each one. A question only the client can answer never stops the flow: it enters the proposal as an explicit **assumption**, and the client's answer later opens a revision.

### 1. Ground

Before writing `grounding.md`, read [GROUNDING-FORMAT.md](./GROUNDING-FORMAT.md). Establish what exists today from whatever source the work has: the repo, system or documents the argument names; else the session's directory when it is the client's project; else nothing (built from scratch). Name the alternative the work competes with. Read the client's earlier engagements, if any. Create `STATUS.md` in state `draft`, version `v1`, signer and `show_hours` unset, with its first Log line.

Done when `grounding.md` names its source kind, every statement about today carries its citation, the alternative is named (or recorded as none), and every external cost has a source and a consultation date.

### 2. Scope

Before writing `estimate.md`, read [ESTIMATE-FORMAT.md](./ESTIMATE-FORMAT.md). Fill its scope sections: Phase 0, the modules by phase, what not to do, the open questions.

Done when every module sits in one phase and carries exactly one tag (✅ asked · 💡 proposed · ⏸ later), Phase 0 lists every defect grounding found (or says there are none) with warranty items marked, and every open question is written as the assumption the quote will make.

### CHECKPOINT 1 · "Is this it?"

Show: today's state with its sources, the alternative, Phase 0 (and what of it is warranty), the modules with their tags, what not to do, and the open questions. Ask whether this is the work. Corrections go back into `grounding.md` and `estimate.md`, then show the checkpoint again.

Done when the user confirms the scope.

### 3. Estimate

Fill the hours sections of `estimate.md`, as ESTIMATE-FORMAT.md lays out. Read every `STATUS.md` under the quote home whose Hours table has actuals, and compute the history: over every phase with a numeric actual, total actual hours ÷ total priced hours.

Done when every module has a low–high hour range, every phase has a subtotal, and the history is a ratio over N engagements or reads "no actuals yet".

### 4. Price

Read `POLICY.md` before pricing anything. When it is missing, read [POLICY-FORMAT.md](./POLICY-FORMAT.md), interview the user, and write it first. Then, before writing `quote.md`, read [QUOTE-FORMAT.md](./QUOTE-FORMAT.md). Price only with values from `POLICY.md`; a value that departs from it for this engagement is an **exception** and carries its reason. When `POLICY.md` lacks a value the quote needs, ask the user for it and offer to add it. `POLICY.md` changes only when the user asks for it, or to save a new identity at Checkpoint 2.

Done when `quote.md` snapshots every policy value it used, every phase price traces to its hours through the policy's pricing rule, every phase has a delivery time, every exception carries a reason, the retainer is itemized (or the policy has none), and the break-even exists exactly when the alternative has a price and carries the alternative's cost through the build exactly when `grounding.md` records it as paid today.

### CHECKPOINT 2 · "Does it add up?"

Show: hours, price and delivery time per phase, the policy values used and every exception with its reason, the retainer, the break-even (when there is one), and the history, as information that adjusts nothing. Then settle, in the same message:

- **Who signs.** A signer `STATUS.md` already records carries over. Otherwise offer the identities saved in `POLICY.md` plus "a new one"; a new one is saved into `POLICY.md` with name, contact, logo path and accent color.
- **Show hours?** Ask when the client has asked to see hours since `show_hours` was last set. Otherwise keep its recorded value, or set it to `false` when unset, without asking.

Corrections go back to Estimate or Price, then show the checkpoint again.

Done when the user confirms the numbers and `STATUS.md` records the signer and `show_hours`.

### 5. Propose

Before writing `proposal.html`, read [PROPOSAL-FORMAT.md](./PROPOSAL-FORMAT.md). Copy each phase that has hours into the Hours table of `STATUS.md`, with its estimate range and priced hours (a Phase 0 with nothing to fix has none; Later ⏸ modules are not a phase), and append the Log line `proposal written v{N}`. Open the proposal for the user when you can (`open` on macOS, `xdg-open` on Linux). When you can publish a link, ask whether to publish one; ask every time, and publish only on a yes.

Done when `proposal.html` passes PROPOSAL-FORMAT.md's checks, `STATUS.md` is updated, and you have told the user both paths and that `/arsenal:quote <client>: sent it` freezes this version once it goes out.

## Revisions

A revision reruns the flow from Scope, with the client's answers turning assumptions into facts; update `grounding.md` only where an answer changes what exists today.

- State `draft`: overwrite the draft in place; the version stays. Log the reason.
- State `sent`: the frozen `proposal-vN.html` and `quote-vN.md` are the starting point and stay untouched. Set the state to `draft` and the version to `v{N+1}`, and log the reason.

Price a revision with the values snapshotted in the `quote.md` of the version it revises; when that version never reached Price, price from `POLICY.md` as usual, and a value its snapshot lacks comes from `POLICY.md` the same way. When `POLICY.md` has changed since, show the difference at Checkpoint 2 and let the user pick. That version's exceptions are shown at Checkpoint 2 too, for the user to keep or drop.

## Language

Write the proposal in the language of the conversation, unless the client speaks another one. The internal files follow the conversation.
