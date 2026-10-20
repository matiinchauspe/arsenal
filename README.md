<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/arsenal-dark.svg">
    <img src="assets/arsenal-light.svg" alt="Arsenal" width="200">
  </picture>
</p>

<h1 align="center">Arsenal</h1>

Portable skills to carry into any project or harness. Each skill lives in `skills/<name>/SKILL.md`,
the open Agent Skills format, so any agent that reads `SKILL.md` can use it.

## Install

### Claude Code

```
/plugin marketplace add matiinchauspe/arsenal
/plugin install arsenal@arsenal
```

Skills are namespaced by the plugin: `teach` is invoked as `/arsenal:teach`.

To try a local checkout without installing it:

```
claude --plugin-dir path/to/arsenal
```

### Other agents

Point the agent's skill discovery at `skills/`, or copy or symlink a single `skills/<name>/` folder
into the agent's skills directory.

## Skills

| Skill   | What it does | Invocation |
| ------- | ------------ | ---------- |
| `teach` | Teaches you a topic over several sessions: a mission, short interactive HTML lessons, reference sheets, a glossary and learning records | user (`/arsenal:teach <topic>`) |
| `quote` | Quotes a piece of work for a client: grounds it in what exists today, scopes and estimates it, prices it with your policy, and writes a client proposal (HTML) plus an internal quote, tracked from draft to sent to outcome | user (`/arsenal:quote <client>: <ask>`) |
| `research` | Researches a topic, an industry or something many industries share, into a living document of labeled, sourced and dated facts that outlives any project, re-verifying what has expired | user (`/arsenal:research <topic>: <question>`) |
| `diagram` | Draws the diagram a question calls for (flow, sequence, states, use cases, journey, ER) from code, a client's ask or a research topic, as Mermaid it renders and checks before handing over, with every element traced to its source | model and user (`/arsenal:diagram <what>, from <source>`) |
| `interview` | Prepares you for software engineering interviews: a profile and story bank shared by every process, a plan per process counted back from its date, mocks scored on your own words, debriefs, and the offer | user (`/arsenal:interview <company>: <what's coming or what happened>`) |
| `idea` | Clarifies a product or startup idea: a map of falsifiable assumptions, each researched by trying to refute it, ranged unit economics computed by a script, and a dated verdict with what the idea demands | user (`/arsenal:idea <idea>: <what to do>`) |

### `teach`: where your learning lives

Each topic gets its own **learning workspace**, kept apart from whatever project you opened the agent in:

- `$ARSENAL_LEARN_HOME/<topic>/` when the variable is set, else `~/learn/<topic>/`.
- If the current directory already holds a `MISSION.md`, that directory is the learning workspace.

Run `/arsenal:teach` with no topic to pick up one you already started.

### `quote`: where your quotes live

Quotes live in `$ARSENAL_QUOTES_HOME` when the variable is set, else `~/quotes/`, never in the client's repo:

- `POLICY.md` at the root holds your pricing policy (rate, payment terms, warranty, retainer, weekly capacity, signing identities). The first quote interviews you to write it.
- Each engagement gets `<client>/<YYYY-MM-engagement>/`, with `STATUS.md`, `grounding.md`, `estimate.md`, `quote.md` (internal) and `proposal.html` (for the client).

Tell it what happened as it happens: `/arsenal:quote acme: sent it` freezes the version the client saw,
`acme: accepted Phase 2 only` records the outcome, and `acme: Phase 2 took 50 h` records actual hours.

### `research`: where your research lives

Research lives in `$ARSENAL_RESEARCH_HOME` when the variable is set, else `~/research/`, never in a client's repo:

- One folder per topic, holding one living `TOPIC.md`. A topic is an industry (`inmobiliarias`) or something many industries share (`facturacion-arca`); an industry links a shared topic instead of copying it.
- Every fact carries a label (`[fact]`, `[secondary]`, `[inference]`, `[unverified]`), its source and the date it was read. A legal or fiscal answer rests only on primary sources and expires after 6 months; an industry practice expires after 24.

Ask again and it answers from what it already knows, re-verifying only what has expired. `/arsenal:research` with no argument lists your topics and flags the expired ones.

### `diagram`: where your diagrams live

Nowhere of their own: a diagram lives beside what it explains. A flow of a project goes into that repo's
docs as a `mermaid` block; a flow in a proposal goes into `proposal.html` as SVG, with its source in the
engagement folder; a research process goes into the topic's section. It is the one Arsenal skill the
agent and the other skills reach on their own: `quote`, `research` and `teach` draw through it.

- Every diagram answers one question, written above it, and the question picks the kind. Past about 15
  nodes it splits into an overview and zooms.
- Every element is traced to its source (`file:line`, the client's sentence). What the source does not
  show is drawn dashed or labeled `assumed:`.
- It renders each diagram with `npx @mermaid-js/mermaid-cli` and looks at it before handing it over, so
  it needs Node. The first render downloads a headless browser.

### `interview`: where your preparation lives

Preparation lives in `$ARSENAL_INTERVIEWS_HOME` when the variable is set, else `~/interviews/`, never in a project's repo:

- The root is your readiness, shared by every process: `PROFILE.md` (experience, targets, the languages you code and interview in, your compensation anchor, target and floor), `STORIES.md` (a STAR story bank tagged by competency) and `QUESTIONS.md` (every question you faced, in mocks and for real, with your weak spots). The first run interviews you to write them.
- Each process gets `<company>/<YYYY-MM-role>/`, with `STATUS.md`, `fit.md` (the JD against your profile, the gaps, and a plan counted back from the next stage's date), `mocks/`, `debriefs/`, a printable cheat sheet before each stage, and `offer.md`.

Mocks score every criterion on a quote from your answer, and a live-coding mock runs hidden tests against code you write in a real file. Tell it what happens as it happens: `acme: had the technical, they asked X` writes a debrief, `acme: they offered X` compares the offer and proposes the counter. `/arsenal:interview` with no argument practices your weak spots. It leans on `research` for the company and the market, on `teach` for gaps that need weeks, and on `diagram` for system designs.

### `idea`: where your ideas live

Ideas live in `$ARSENAL_IDEAS_HOME` when the variable is set, else `~/ideas/`, never in a project's repo:

- Each idea gets `<slug>/`, with `MAP.md` (the pitch, the revenue model, seven zones of falsifiable
  assumptions with their impact and state, the economics, the tests and the verdicts) and `STATUS.md`
  (exploring, testing, parked or discarded, with a log). `IDEAS.md` keeps the ideas you generated and
  did not pick.
- Every assumption is researched by trying to refute it, through `research`, so its facts are labeled,
  sourced and expire. Desk research never validates: `validated` takes a real-world test, which is
  always offered and never required, with its threshold written before it runs.
- The economics run three scenarios through `economics.py` (Python 3, standard library): LTV, LTV/CAC,
  payback, customers and market share needed for your target, and the variable the result hinges on.

`/arsenal:idea generate: <a problem, an industry or a skill>` proposes ideas to pick from;
`/arsenal:idea <idea>` researches the riskiest open assumption; `<idea>: verdict` says discard, not
enough information, or worth testing, with the best reason not to do it and what the idea demands. The
map's view is drawn with `diagram`.

## Layout

```
arsenal/
├─ .claude-plugin/
│  ├─ marketplace.json   ← this repo is a marketplace…
│  └─ plugin.json        ← …that ships one plugin, `arsenal`
└─ skills/<name>/SKILL.md
```

Add a skill by adding a folder under `skills/`; the plugin picks it up with no manifest change.
Validate with `claude plugin validate .`.

## License

MIT. `skills/teach` is adapted from [mattpocock/skills](https://github.com/mattpocock/skills) (MIT);
both notices are in [LICENSE](LICENSE).
