---
name: idea
description: Clarify a product, startup or digital-business idea into a map of falsifiable assumptions, each researched by trying to refute it, with ranged unit economics and a dated verdict the user decides on; or generate ideas from signals found in the market.
disable-model-invocation: true
argument-hint: "<idea>: what to do (an idea to map, a test result, verdict), generate: <starting point, or nothing to scan the market>, generate quick: <starting point>, or nothing to list your ideas"
---

An idea is a building on ground nobody has surveyed. This skill never promises the building stands: it surveys the ground fast and says where it will not hold. Each idea is a **map of falsifiable assumptions** in seven zones, and every step lowers the uncertainty with facts that are labeled, sourced and dated. **Research tries to break an assumption, never to confirm it**: an agent asked to confirm an idea always does, and only what survives an attempt to break it is worth anything. Desk research is the default and is fast; a real-world test is offered, never required. The decision is always the user's.

## Locating the idea

The **ideas home** is `$ARSENAL_IDEAS_HOME` when set, else `~/ideas`. Each idea is one folder, `<ideas home>/<slug>/`, holding `MAP.md` and `STATUS.md`; `<ideas home>/IDEAS.md` keeps the ideas Generate proposed and the user did not pick.

1. **No argument:** the intent is **List**.
2. An argument whose part before the first colon is exactly `generate` or `generate quick` (or the argument `generate` alone) is **Generate**, quick for the second; what follows its colon is the starting point, and an empty one means an open scan.
3. Otherwise split the argument at its first colon into the idea and the rest. Slug the idea in kebab-case; if it is close to an existing idea's folder, ask whether it is the same idea.
4. Read the intent from the rest; when it fits none of these, ask what the user wants to do:

| Intent | Example argument | Idea folder | Then |
| --- | --- | --- | --- |
| **List** | (nothing) | none | [List](#list) |
| **Generate** | `generate: I'm an accountant and small firms keep asking me for the same report`, `generate`, `generate quick: logistics` | none | [Generate](#generate) |
| **New** | `salon-bookings: salons take a deposit with each booking so no-shows cost the client` | missing: create it | [New](#new) |
| **Continue** | `salon-bookings`, `salon-bookings: go on` | exists | [Continue](#continue) |
| **Test** | `salon-bookings: design the interview for P1` | exists | [TEST-FORMAT.md](./TEST-FORMAT.md), Test |
| **Result** | `salon-bookings: did 6 interviews, 4 lost a booking last month` | exists | [TEST-FORMAT.md](./TEST-FORMAT.md), Result |
| **Verdict** | `salon-bookings: verdict` | exists | [LIFECYCLE.md](./LIFECYCLE.md), Verdict |
| **Outcome** | `salon-bookings: I'm parking it`, `salon-bookings: discard it` | exists | [LIFECYCLE.md](./LIFECYCLE.md), Outcome |

A description of an idea under a slug whose folder already holds a different idea asks for another slug.

Done when you hold the ideas home, one intent and, unless it is List or Generate, one absolute idea path, and have told the user all of them.

## Where things are written

Write only inside the ideas home, and inside the research home through `research`. Facts about a market, an industry or a competitor live in `research` topics and are linked from `MAP.md`, never copied: they expire, and `research` is what re-verifies them. The repo the session was opened in is never written to. Every intent that changes an idea appends one line to its `STATUS.md` Log, as [MAP-FORMAT.md](./MAP-FORMAT.md) lays out.

## List

Read every `STATUS.md` and `MAP.md` under the ideas home and show one row per idea: slug, state, the latest verdict and its date, how many critical assumptions are still open, and whether the verdict is stale ([LIFECYCLE.md](./LIFECYCLE.md), Stale verdicts). Then ask which idea to continue, or whether to start or generate one. With no ideas yet, ask for the first idea, or for a starting point to generate from.

Done when the user has the table, or was asked for the first idea.

## Generate

A generated idea starts from a **signal**: a sourced, dated fact showing that people lose money or time on a problem today. An idea pulled from memory is a guess about a market nobody looked at, so Generate researches before it proposes.

The starting point is whatever the user gives: a **problem** they have seen, an **industry** they know, a **skill** they have, a hunch, an idea half thought through, or any mix. With none, the scan is **open**: the research picks where to look. Never ask for a profile, and never ask for a starting point the user did not give.

1. **Signals:** hand `research` one question that hunts for signals, in the background when the host can; tell the user it started, and propose when it returns. The topic is the industry the starting point names (`salons-ar`), reusing one another idea created; an open scan, or a starting point that names no industry, uses the cross-cutting `market-signals` topic. Everything the user said goes into the question as **leads**: a hunch ("clinics still book by WhatsApp"), a competitor they named, a figure they remember. The research looks for signals around the leads first, and re-verifies each one, never taking it as a source; it also asks what contradicts a lead, since a hunch is an assumption like any other. The section's kind is `practice`. The question asks for concrete, sourced cases of: complaints repeated in forums, reviews or communities; people paying for a manual workaround (spreadsheets, freelancers, an agency) to do a repetitive task; incumbents with bad reviews or prices their users resent; a recent law, platform change or price change that forces people to act. For each signal it also asks **what already solves it and what that costs**: a pain with a cheap solution its users like is not an opening. An open scan asks for signals across markets and names the 2 or 3 where they cluster.
2. **Propose** 3 to 5 ideas, each resting on one signal from that section, as: a one-line pitch, who pays, the signal with its link, what already solves it, and **the assumption most likely to kill it**, phrased so a fact could break it. A signal shows that the pain exists, never that someone pays to remove it: that is what Continue tries to break. Leave out a signal the research found already well solved, and say so. When no signal holds an idea, say so and ask for a narrower starting point: never fill the list from memory.
3. The user picks one, combines two, or asks for another round. Another round first uses the signals no idea used yet, and runs a new signals question only when none is left.
4. Append the ideas not picked to `IDEAS.md` as MAP-FORMAT.md lays out, and run **New** on the picked one, carrying its signal.

**Quick** (`generate quick: <starting point>`) skips step 1 and proposes from memory, as a fast filter; it needs a starting point, so ask for one when it has none. Each of its ideas says `Signal: none (from memory)` instead of a signal and what already solves it.

Done when one idea went to New and the rest are in `IDEAS.md`.

## New

Read [MAP-FORMAT.md](./MAP-FORMAT.md) and [ECONOMICS-FORMAT.md](./ECONOMICS-FORMAT.md).

1. Write the pitch in one line: who, what pain, what you offer. Ask only what the description leaves impossible to write. A description that names a direction but no offer ("something for accountants") is a starting point, not an idea: offer to run Generate with it, and on a yes go there.
2. Propose the revenue model (ECONOMICS-FORMAT.md, Models), and ask for the target (ECONOMICS-FORMAT.md, Inputs).
3. Propose 2 to 4 assumptions per zone, each falsifiable and with its impact, including the two every idea starts with (MAP-FORMAT.md, Assumptions). Rewrite a vague one until a fact could break it, and say what you rewrote.
4. **Checkpoint:** show the pitch, the model, the target and the assumptions. An idea that came from Generate with a signal keeps it as its Origin (MAP-FORMAT.md), and its topic joins the Research topics; its assumptions still start `unknown`, since the signal was found by looking for pain, not by trying to break it. The user corrects, removes or adds; then write `MAP.md`, and `STATUS.md` with the state `exploring`, and draw the view (MAP-FORMAT.md, The view).
5. Offer to start Continue now.

Done when `MAP.md` holds the pitch, the model and every zone with at least one assumption, the user has seen them at the checkpoint, and the Log has the line.

## Continue

Read `MAP.md`, MAP-FORMAT.md, and the `research` sections its evidence links. When the latest verdict is stale, say so first.

1. **Pick** the next open assumption. An assumption is **open** when it is `unknown`, unless its Evidence says `nothing found` and since then the user brought no lead and no related fact expired; or when it is researched and a fact it rests on has expired or the user brought a new lead; `E1` is also open again when one of its inputs changes (ECONOMICS-FORMAT.md, Writing a run, step 4). A researched assumption with neither is not picked again: a critical one left `researched (mixed)` or `researched (against)` gets the offer of a test instead (step 5). Pick the open `critical` one with the least evidence, `unknown` before `researched (mixed)` before `researched (against)`; on a tie, the cheapest to research. With no critical one open, the same over `high`. An assumption `in-test` waits for the user: skip it. `E1` waits for `python3` when a run stopped without it (ECONOMICS-FORMAT.md, Running), and for its inputs; Continue picks the assumptions it waits on ahead of it, even when they are `low` (ECONOMICS-FORMAT.md, Writing a run). Tell the user which one and why. When nothing is left to pick, say the map is ready for a verdict, and go to step 5.
2. **Economics:** when the pick is `E1`, run the economics as ECONOMICS-FORMAT.md lays out, and skip step 3. Any other Economics assumption is researched like the rest (step 3), with a question that tries to show its input is worse than its base value.
3. **Research:** hand the question to `research`, in the background when the host can, so the user keeps working; a host that cannot runs it in the foreground. The topic is the industry's (`salons-ar`) or a cross-cutting one (`online-payments-ar`), reusing a topic another idea already created. **Phrase the question to refute the assumption**: "what shows salon owners do not lose bookings to no-shows, or do not care?", never "confirm that salons lose bookings". A Competition and value added assumption asks for the competitor table (MAP-FORMAT.md, Competition). While its research runs, the assumption's Evidence adds `researching since {YYYY-MM-DD}` (step 4 removes it) and Continue skips it; a session that ends before the answer leaves it open again: a `researching since` from an earlier session is removed, and the assumption is picked as if it were not there.
4. **Update:** when the answer returns, set the assumption's state by the transitions in MAP-FORMAT.md, link the sections, redraw the view, and log it.
5. A critical assumption left `researched (mixed)` or `researched (against)`, or `unknown` with `nothing found`, gets the offer of a test (TEST-FORMAT.md), except `E1` (ECONOMICS-FORMAT.md, Writing a run) and one whose test is still open (TEST-FORMAT.md, Result). The user may decline; the Log says so, the offer is not repeated for that assumption until its state changes, and Continue goes on.

The user may ask for several assumptions in one turn; each still gets its own refuting question.

Done when the picked assumption has a new state backed by linked facts, or a dated `nothing found`, or the economics ran, or nothing was left to pick; the view is redrawn when a state changed; the Log has the line; and the user knows what Continue would pick next, or that the map is ready for a verdict.

## Language

An idea keeps the language it was created in: the language of the conversation that created it. Its `research` questions are asked in that language too.

## Never

- **State a market fact from memory.** A competitor, a price, a market size or a law is `research`, with its label and its source.
- **Validate from the desk.** Desk research reaches `researched (for)` at most; `validated` takes a real-world test.
- **Do arithmetic on money in your head.** Every derived number comes from `economics.py`.
- **Judge the user.** The verdict describes what the idea demands; whether that fits the user is theirs to say.
- **Move a threshold** after a test ran.
