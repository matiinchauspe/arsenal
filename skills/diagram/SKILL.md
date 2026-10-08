---
name: diagram
description: Draw a flowchart, sequence, state, use case, journey or ER diagram that answers one question, from code, a client's ask or a research topic, as Mermaid rendered and checked before it is handed over. Use when the user asks for a diagram, a flow, a sequence or the states of something; when a document, a proposal or a lesson needs one; and before drawing any diagram in ASCII.
argument-hint: "<what to draw>, from <source>"
---

A diagram is a **blueprint of one thing**: it answers one question, and everything on it can be traced to its source. Mermaid is always the source of the drawing, so the next person can edit one line when the flow changes. **A diagram that looks right and is wrong is worse than no diagram**, because people believe it.

## The source

Draw only from the source you were given: code, a client's ask, a research topic, the conversation. Reading that source is the work; anything it does not settle is either an assumption drawn as one (step 4) or a question for the user. What is normal in an industry, or anything else outside the source, is research: say so and suggest `research`.

No source named → ask for one. Done when you can name the source, and for code, the files and the commit.

## Where it lands

The diagram lives beside what it explains:

| Destination | What is written |
| --- | --- |
| A document in a repo (a runbook, `docs/`, the agent docs) | A `mermaid` code block in the `.md` that explains the flow, created when missing |
| An HTML document: a proposal from `quote`, a lesson or reference from `teach` | The rendered SVG inline in the document, and its source at `diagrams/<slug>.mmd` in the folder that owns it (the engagement, the learning workspace) |
| A section of a `research` topic | Nothing: hand the Mermaid back, and `research` writes it into the section |
| Anything else | The conversation; when it is for someone else, one self-contained HTML page embedding the SVG, written where the user says (else the system temp directory) and published as a link when the host can and the user says yes |

A document that already holds a diagram answering the same question, in ASCII or Mermaid, gets it **replaced in place**: two drawings of one thing leave the reader choosing which to believe. Other old diagrams stay as they are.

## The run

### 1. Question

Write the question the diagram answers in one sentence ("What states can a subscription be in, and what moves it?"). It goes above the diagram. A request that yields no one-sentence question is not ready: ask until it does. Reached from another skill's unattended work, take the question from what that work needs drawn, and let it reach the user with the hand-over.

Done when the question is one sentence, and the user did not correct it or will see it in the hand-over.

### 2. Kind

The question picks the kind:

| The question asks | Kind | Mermaid |
| --- | --- | --- |
| What happens, in what order, between whom? | Sequence | `sequenceDiagram` |
| What states can X be in, and what moves it? | State | `stateDiagram-v2` |
| What steps and decisions are there? | Flow | `flowchart` |
| Who can do what with the system? | Use case | `usecase-beta` |
| What does a person go through, and how does it feel? | Journey | `journey` |
| What things exist, and how do they relate? | ER | `erDiagram` |

`usecase-beta` needs Mermaid 12: `actor Name` lines, then `systemBoundary "System"` holding one `Id("Use case")` per line, closed by `end`, then `Name --> Id`. Where it lands in a renderer that may run an older Mermaid (a repo `.md` read on GitHub), draw the use cases as a `flowchart` with the actors as nodes instead.

A question no row fits (what a system is built from, what happened when) takes the Mermaid type made for it (`C4Context`, `timeline`), named to the user.

Done when the kind follows from the question by this table, or the type made for it is named.

### 3. Scope

Past roughly 12 to 15 nodes, split instead of crowding: one **overview**, plus a **zoom** for each part that needs detail, each with its own question. A zoom links back to the overview, and the overview names its zooms.

A diagram bound for a printed document (a `quote` proposal, a `teach` reference) also fits in **half a printed page**: a figure taller than the page prints blank or cut, and one that only just fits strands the half page before it. It must also stay **legible**: printed at the page width, a diagram wider than about 1000px (its SVG `viewBox`) shrinks its text below a readable size. Stretched to the page width, as in a proposal, both mean a width of at most about 1000px and a height of at most about 0.7 times the width. A tall `TD` flow goes `LR` and a long `LR` row goes `TD`, as long as that keeps it inside both; one that fits neither way splits.

Done when every diagram is within the limit, fits half a page legibly when it will be printed, and has its own question.

### 4. Draw

Write the Mermaid. Keep ids short and ASCII (`pro`, `cancel`) and put the words in labels; quote any label holding punctuation.

- **Facts and assumptions look different.** What the source shows is drawn solid. What the flow needs but the source does not show is drawn dashed where the kind has a dashed line with no other meaning (`-.->` in a flowchart); elsewhere its label starts with `assumed:`. A diagram of a future project is all proposed: write **Proposed** above it instead of marking each element.
- **Every element is traceable.** Under the diagram, list each element with its source: `file:line` for code, the client's own sentence for an ask, the fact it rests on for a research topic. A diagram drawn from code ends that list with `based on <short sha>, <YYYY-MM-DD>`. A diagram stamped Proposed carries no list.

Done when every diagram is stamped Proposed, or each of its nodes and edges is in the source list or marked as an assumption.

### 5. Check

Render it and look at it before anyone else does. Write the Mermaid to a file in the system temp directory, never beside the destination, and render it there:

```
npx -y @mermaid-js/mermaid-cli -i <tmp>/<slug>.mmd -o <tmp>/<slug>.png -s 2
```

The first run downloads a headless browser and can take minutes; later runs are quick.

- **It fails to render:** fix it and render again (the usual causes: a reserved word such as `end` as an id, punctuation in an unquoted label, syntax recalled wrong). After three failed renders, stop and show the user the error: broken Mermaid is never handed over.
- **It renders:** read the PNG. Crossing edges, overlapping labels or a cramped side mean a change: flip the direction (`LR` ↔ `TD`), shorten labels, or split (step 3). Render again after each change.
- **There is no Node:** hand it over marked **unverified**.

A diagram bound for a printed document is checked where it lands, not only alone: the PNG cannot show how it breaks across pages, and mermaid-cli shrinks it to fit 800px, so its size is read from the SVG `viewBox`, never from the PNG. Render the SVG and inline it as step 6 does, into a copy of the document in the temp directory, never the document itself, print the copy to PDF with a headless Chrome or Chromium (the one mermaid-cli downloaded will do):

```
<chrome> --headless --no-pdf-header-footer --print-to-pdf=<tmp>/<slug>.pdf <tmp>/<copy>.html
```

and look at every page the diagram touches. A blank or cut figure, text too small to read, or a page left half empty before it, sends it back to step 3; print again after each change.

Done when the last render is clean to read and, for a printed document, its pages print it whole and legible; or the diagram is marked unverified, or the user has the error.

### 6. Hand over

Write it where it lands, with the question above it and the source list below. For an SVG, render the same file with `-o <tmp>/<slug>.svg` and inline it **as rendered**: never trimmed or edited by hand, since the `.mmd` beside it must still produce what the reader sees. A change goes into the `.mmd` and renders again. Give the user (or the skill that asked) where it is (a path, a link, or, when it lands nowhere, the diagram itself with its source list), the question it answers, and every assumption on it.

Done when they have all three, and the diagram sits only where the table above puts it.

## Language

Labels, the Proposed and `assumed:` marks, the question and the source list follow the language of the document the diagram lands in, and the language of the person who will see it when it lands nowhere.
