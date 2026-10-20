---
name: idea
description: Clarify a product, startup or digital-business idea into a map of falsifiable assumptions, each researched by trying to refute it, with ranged unit economics and a dated verdict the user decides on.
disable-model-invocation: true
argument-hint: "<idea>: what to do (an idea to map, a test result, verdict), generate: <starting point>, or nothing to list your ideas"
---

An idea is a building on ground nobody has surveyed. This skill never promises the building stands: it surveys the ground fast and says where it will not hold. Each idea is a **map of falsifiable assumptions** in seven zones, and every step lowers the uncertainty with facts that are labeled, sourced and dated. **Research tries to break an assumption, never to confirm it**: an agent asked to confirm an idea always does, and only what survives an attempt to break it is worth anything. Desk research is the default and is fast; a real-world test is offered, never required. The decision is always the user's.

## Locating the idea

The **ideas home** is `$ARSENAL_IDEAS_HOME` when set, else `~/ideas`. Each idea is one folder, `<ideas home>/<slug>/`, holding `MAP.md` and `STATUS.md`; `<ideas home>/IDEAS.md` keeps the ideas Generate proposed and the user did not pick.

1. **No argument:** the intent is **List**.
2. An argument that starts with `generate` is **Generate**; what follows its colon is the starting point.
3. Otherwise split the argument at its first colon into the idea and the rest. Slug the idea in kebab-case; if it is close to an existing idea's folder, ask whether it is the same idea.
4. Read the intent from the rest; when it fits none of these, ask what the user wants to do:

| Intent | Example argument | Idea folder | Then |
| --- | --- | --- | --- |
| **List** | (nothing) | none | [List](#list) |
| **Generate** | `generate: I'm an accountant and small firms keep asking me for the same report` | none | [Generate](#generate) |
| **New** | `salon-bookings: salons take a deposit with each booking so no-shows cost the client` | missing: create it | [New](#new) |
| **Continue** | `salon-bookings`, `salon-bookings: go on` | exists | [Continue](#continue) |
| **Test** | `salon-bookings: design the interview for P1` | exists | [TEST-FORMAT.md](./TEST-FORMAT.md), Test |
| **Result** | `salon-bookings: did 6 interviews, 4 lost a booking last month` | exists | [TEST-FORMAT.md](./TEST-FORMAT.md), Result |
| **Verdict** | `salon-bookings: verdict` | exists | [LIFECYCLE.md](./LIFECYCLE.md), Verdict |
| **Outcome** | `salon-bookings: I'm parking it`, `salon-bookings: discard it` | exists | [LIFECYCLE.md](./LIFECYCLE.md), Outcome |

A description of an idea under a slug whose folder already holds a different idea asks for another slug.

Done when you hold the ideas home, one intent and, unless it is List or Generate, one absolute idea path, and have told the user all of them.

## Where things are written

Write only inside the ideas home. Facts about a market, an industry or a competitor live in `research` topics and are linked from `MAP.md`, never copied: they expire, and `research` is what re-verifies them. The repo the session was opened in is never written to. Every intent that changes an idea appends one line to its `STATUS.md` Log, as [MAP-FORMAT.md](./MAP-FORMAT.md) lays out.

## List

Read every `STATUS.md` and `MAP.md` under the ideas home and show one row per idea: slug, state, the latest verdict and its date, how many critical assumptions are still open, and whether the verdict is stale ([LIFECYCLE.md](./LIFECYCLE.md), Stale verdicts). Then ask which idea to continue, or whether to start or generate one. With no ideas yet, ask for the first idea, or for a starting point to generate from.

Done when the user has the table, or was asked for the first idea.

## Generate

When the argument gave no starting point, ask for one: a **problem** the user has seen, an **industry** they know, or a **skill** they have. Never ask for a profile: the starting point is all Generate needs.

1. Propose 3 to 5 ideas, each as: a one-line pitch, who pays, and **the assumption most likely to kill it**, phrased so a fact could break it. Do not research yet: this is a quick filter, and an idea earns research by being picked.
2. The user picks one, combines two, or asks for another round.
3. Append the ideas not picked to `IDEAS.md` as MAP-FORMAT.md lays out, and run **New** on the picked one.

Done when one idea went to New and the rest are in `IDEAS.md`.

## New

Read [MAP-FORMAT.md](./MAP-FORMAT.md) and [ECONOMICS-FORMAT.md](./ECONOMICS-FORMAT.md).

1. Write the pitch in one line: who, what pain, what you offer. Ask only what the description leaves impossible to write.
2. Propose the revenue model (ECONOMICS-FORMAT.md, Models), and ask for the target (ECONOMICS-FORMAT.md, Inputs).
3. Propose 2 to 4 assumptions per zone, each falsifiable and with its impact, including the two every idea starts with (MAP-FORMAT.md, Assumptions). Rewrite a vague one until a fact could break it, and say what you rewrote.
4. **Checkpoint:** show the pitch, the model, the target and the assumptions. The user corrects, removes or adds; then write `MAP.md`, and `STATUS.md` with the state `exploring`, and draw the view (MAP-FORMAT.md, The view).
5. Offer to start Continue now.

Done when `MAP.md` holds the pitch, the model and every zone with at least one assumption, the user has seen them at the checkpoint, and the Log has the line.

## Continue

Read `MAP.md`, MAP-FORMAT.md, and the `research` sections its evidence links. When the latest verdict is stale, say so first.

1. **Pick** the next assumption: the open `critical` one with the least evidence, `unknown` before `researched (mixed)` before `researched (against)`; on a tie, the cheapest to research. With no critical one open, the same over `high`. An assumption `in-test` waits for the user, and an Economics assumption waits for its inputs (ECONOMICS-FORMAT.md, Writing a run): skip both. Tell the user which one and why.
2. **Economics:** when the pick is in the Economics zone, run the economics as ECONOMICS-FORMAT.md lays out, and skip step 3.
3. **Research:** hand the question to `research`, in the background when the host can, so the user keeps working; a host that cannot runs it in the foreground. The topic is the industry's (`salons-ar`) or a cross-cutting one (`online-payments-ar`), reusing a topic another idea already created. **Phrase the question to refute the assumption**: "what shows salon owners do not lose bookings to no-shows, or do not care?", never "confirm that salons lose bookings". A Competition and value added assumption asks for the competitor table (MAP-FORMAT.md, Competition).
4. **Update:** when the answer returns, set the assumption's state by the transitions in MAP-FORMAT.md, link the sections, redraw the view, and log it.
5. A critical assumption left `researched (mixed)` or `researched (against)` gets the offer of a test (TEST-FORMAT.md). The user may decline; the Log says so and Continue goes on.

The user may ask for several assumptions in one turn; each still gets its own refuting question.

Done when the picked assumption has a new state backed by linked facts, or the economics ran; the view is redrawn; the Log has the line; and the user knows what Continue would pick next, or that the map is ready for a verdict.

## Language

An idea keeps the language it was created in: the language of the conversation that created it. Its `research` questions are asked in that language too.

## Never

- **State a market fact from memory.** A competitor, a price, a market size or a law is `research`, with its label and its source.
- **Validate from the desk.** Desk research reaches `researched (for)` at most; `validated` takes a real-world test.
- **Do arithmetic on money in your head.** Every derived number comes from `economics.py`.
- **Judge the user.** The verdict describes what the idea demands; whether that fits the user is theirs to say.
- **Move a threshold** after a test ran.
