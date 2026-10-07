# Changelog

All notable changes to Arsenal are recorded here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow
[Semantic Versioning](https://semver.org/). The version is the one in `.claude-plugin/plugin.json`.

## [Unreleased]

### Fixed

- **`quote`**: the break-even now counts what the client keeps paying for the alternative while
  the work is built, until the phase that replaces it is delivered. Before, it dropped the
  alternative in month 1, which put the first real quote's break-even 9 months too early.
- **`quote`**: the policy now records when the retainer starts (suggested: at the first phase
  delivered), and the quote and proposal state it.
- **`quote`**: the proposal shows the monthly running cost against the alternative as bars, with
  the break-even month in the caption. The cumulative curve beside the weeks-based timeline read as
  a delivery date.

## [0.2.0] - 2026-10-06

### Added

- **`quote`** (`/arsenal:quote <client>: <ask>`): quotes any work sold by the hour or by the
  deliverable. It grounds the quote in what exists today (a repo, a running system, the client's
  documents, or nothing) and in the alternative it competes with, scopes it into phases, estimates
  hour ranges, and prices it with your policy. It stops at two checkpoints, after the scope and
  after the price, and writes two documents: `proposal.html` for the client and `quote.md` for you.
  - Quotes live at `$ARSENAL_QUOTES_HOME`, default `~/quotes/`, one folder per client and
    engagement; the skill reads the client's repo but never writes into it.
  - Your pricing policy lives in `POLICY.md`. Each quote snapshots the values it used, and an
    exception lives in that quote with its reason. When the policy is missing, the skill
    interviews you first.
  - The proposal shows a fixed price and an estimated delivery time per phase. Hours stay internal
    unless the client asks to see them. It is one self-contained HTML file that opens offline and
    prints to A4, signed by an identity you choose for each engagement.
  - A sent version is frozen as `vN`; later changes become `vN+1`. `STATUS.md` tracks each
    engagement from draft to sent to accepted or rejected, and optional actual hours feed back into
    later estimates as information.

## [0.1.0] - 2026-10-06

The first release: Arsenal is a Claude Code plugin marketplace that ships one plugin, `arsenal`.

### Added

- **Marketplace and plugin.** Install with `/plugin marketplace add matiinchauspe/arsenal` and
  `/plugin install arsenal@arsenal`. Skills live in `skills/<name>/SKILL.md`, the open Agent
  Skills format, so agents other than Claude Code can use them too.
- **`teach`** (`/arsenal:teach <topic>`): teaches a topic over several sessions, grounded in a
  mission. It produces short interactive HTML lessons, reference sheets, a glossary and learning
  records. Adapted from Matt Pocock's `teach` (mattpocock/skills@3216582, MIT). Changes from the
  upstream skill:
  - Each topic gets its own learning workspace at `$ARSENAL_LEARN_HOME/<topic>/`, default
    `~/learn/<topic>/`, outside the project the agent was opened in.
  - `GLOSSARY.md` is part of the workspace. The upstream skill ships its format but never links it.
  - Lessons follow the language of the conversation.

[0.2.0]: https://github.com/matiinchauspe/arsenal/releases/tag/v0.2.0
[0.1.0]: https://github.com/matiinchauspe/arsenal/releases/tag/v0.1.0
