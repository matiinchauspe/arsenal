# TOPIC.md format

`TOPIC.md` is the one living document of a topic. It is a mirror of what is known today: a fact is corrected in place when it changes, and every fact lives in exactly one place, in this topic or in a linked one.

```md
# {Topic}

- Kind: industry | cross-cutting
- Links: [{other topic}](../{other-topic}/TOPIC.md), {what this topic takes from it}

## Index

| Question | Kind | Last read | Expires |
| --- | --- | --- | --- |
| [{question}](#{anchor}) | legal-fiscal \| practice | {YYYY-MM-DD} | {YYYY-MM-DD} |

## {Question}

- Kind: legal-fiscal | practice
- Asked: {YYYY-MM-DD}, {for whom, when the user said}

### Answer

{A few lines. Every claim points to the facts below, or to a fact in a linked topic.}

### Facts

- [fact] {statement}. Source: {url or document, section}. Read {YYYY-MM-DD}.
- [secondary] {statement}. Source: {url}. Read {YYYY-MM-DD}.
- [inference] {statement}, from {the facts it reasons from}.

### Pending

- [unverified] {statement}. Tried: {where it was looked for, and what blocked it}.

### Changes

- {YYYY-MM-DD} · {what a re-verification changed: was X, now Y, per {source}}
```

## Labels

Every fact carries exactly one label:

- **[fact]**: read in the primary source that owns it (the law, the agency, the provider).
- **[secondary]**: press, an industry chamber, a community, or a primary source that could not be re-read. It lives under Facts in a `practice` section and under Pending in a `legal-fiscal` one.
- **[inference]**: reasoned from cited facts, naming them. It has no source of its own and expires with the facts it reasons from.
- **[unverified]**: could not be confirmed. It lives under Pending, never under Facts.

## Kind

The kind belongs to the question, so one topic can hold both.

| Kind | Expires after | What may back the answer |
| --- | --- | --- |
| `legal-fiscal` | 6 months from the read date | only `[fact]`, and `[inference]` built from `[fact]`. Anything weaker goes to Pending. |
| `practice` | 24 months from the read date | `[fact]`, `[secondary]`, `[inference]`, each labeled |

## Freshness

A fact has **expired** when its kind's period has passed since its read date. A section is **expired** when any fact its answer rests on has expired, a linked topic's fact included; else it is **fresh**. The Index's Expires column is the earliest expiry among those facts.

Re-verifying a fact re-reads its source:

- **Unchanged:** update its read date.
- **Changed:** rewrite the fact and the answer, and add a line to Changes.
- **Gone:** move it to Pending with what blocked it, and rewrite the answer without it.

Then update the section's row in the Index.
