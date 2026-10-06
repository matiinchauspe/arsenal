# Changelog

All notable changes to Arsenal are recorded here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow
[Semantic Versioning](https://semver.org/). The version is the one in `.claude-plugin/plugin.json`.

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

[0.1.0]: https://github.com/matiinchauspe/arsenal/releases/tag/v0.1.0
