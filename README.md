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
