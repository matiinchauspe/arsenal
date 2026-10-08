---
name: research
description: Research a topic, an industry or something many industries share, into a living document of dated, sourced facts that outlives any project.
disable-model-invocation: true
argument-hint: "<topic>: <question>, or nothing to list your topics"
---

What you research for one client, the next client in the same industry needs again. Each topic keeps **one living document**: every fact in it sits in one place, carries its source and the date it was read, and is re-verified once it expires. **A stale fact is never handed back as current.**

## Locating the topic

A **topic** is one folder holding one `TOPIC.md`. The **research home** is `$ARSENAL_RESEARCH_HOME` when set, else `~/research`, and each topic lives at `<research home>/<topic>/`. A topic is either an **industry** (`inmobiliarias`, `seguros-pas`) or **cross-cutting**: something many industries share (`facturacion-arca`, `datos-personales-ar`). A cross-cutting subject always gets its own topic, and an industry links it instead of copying it.

1. **No argument:** list every topic under the research home with its kind, its last read date and how many of its questions have expired, then ask which one to continue or what new topic to start. With no topics yet, ask for the first.
2. Split the argument at its first colon into the topic and the question. An argument with no colon is either a topic, so ask for the question, or a question, so propose the topic it belongs to and let the user correct it.
3. Slug the topic in kebab-case. A topic whose facts depend on one country's law ends in that country's code (`datos-personales-ar`). If the slug is close to an existing topic, ask whether it is the same topic.
4. **New topic:** ask whether a note on it already exists somewhere, such as a research file in a client's repo. A path the user gives is the run's starting point: a lead to re-verify, never a source. Create the folder, and tell the user whether you take the topic for an industry or a cross-cutting one.

Done when you hold one absolute topic path and one question, and have told the user both.

## Where things are written

Write only inside the research home. The repo the session was opened in is never written to, and the only thing read from it is a starting-point note the user names: findings reach the project through the conversation.

## The run

### 1. Recall

Read [TOPIC-FORMAT.md](./TOPIC-FORMAT.md), then the `TOPIC.md` index, the section closest to the question, and the sections of the linked topics it leans on. A topic just created has no `TOPIC.md` yet, so it is the third case.

- A **fresh** section that answers the question: hand it back (step 4) and stop.
- An **expired** section that answers it: the run re-verifies its expired facts, keeping the section's kind, and answers from the result.
- Otherwise: the run adds a new section for the question.

Done when you can name which of the three it is and, for an expired section, list its expired facts.

### 2. Kind

Only a new section reaches this step. It gets a **kind**: `legal-fiscal` (a law, a regulation, a tax, a filing) or `practice` (what is normal in the industry: how it sells, what it pays, how it handles its clients). Propose one from the question and let the user correct it. The kind sets when the section's facts expire and which sources may back its answer, as TOPIC-FORMAT.md lays out.

Done when the section has a kind the user did not correct, or the corrected one.

### 3. Research

One run per topic at a time: when `<topic>/RUNNING` exists, tell the user which question holds it and since when, and ask whether that run is still going. A run that died leaves its `RUNNING` behind: on the user's word that it is no longer going, delete it; otherwise stop. With no `RUNNING` left, write one with the question and today's date, and hand the reading to a background agent so the user keeps working; when you cannot start one, do the reading yourself. The brief:

- The question, the topic path, its kind and its language, the section's kind, the expired facts to re-verify (if any), the starting-point note (if any), and [TOPIC-FORMAT.md](./TOPIC-FORMAT.md) to write by.
- Go to the source that owns each claim: the law in its official bulletin, the agency's own documentation, the provider's own terms. Label every fact, as TOPIC-FORMAT.md defines.
- A fact that belongs to a cross-cutting subject goes into that topic (create it when missing) and is linked from this one. When that topic has its own `RUNNING`, the fact waits under this section's Pending, naming the topic it belongs to.

Done when the reading is finished (the agent has returned, or you did it yourself), every fact in the section is written as its label's line in TOPIC-FORMAT.md, the section's answer rests only on facts its kind allows, the Index row of every section written matches it, and `RUNNING` is deleted.

### 4. Hand back

Give the user the answer in a few lines, the facts it rests on, what stays pending and why, and the path to the section. When the answer describes a process (the steps of a transfer, the life of a claim), offer to draw it with the `diagram` skill; on a yes, write the diagram it hands back (its question, the Mermaid and its source list) into the section's Answer.

Done when the user has all four, and a process answer has had its diagram offered.

## Language

A topic keeps the language it was created in: the language of the conversation that created it.
