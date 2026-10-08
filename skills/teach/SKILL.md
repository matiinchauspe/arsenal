---
name: teach
description: Teach the user a new skill or concept over several sessions, in a learning workspace of its own.
disable-model-invocation: true
argument-hint: "What would you like to learn about?"
---

The user has asked you to teach them something. This is a stateful request: they intend to learn the topic over multiple sessions, and every session picks up from the state left by the last one.

## Locating the learning workspace

A **learning workspace** is one folder per topic, holding the whole state of the user's learning. It lives apart from whatever project the session was opened in, because what the user learns outlives that project. Resolve it before anything else:

1. **The current directory holds a `MISSION.md`**, and the user named no topic or named the topic of that mission → it is the learning workspace.
2. **Otherwise**, the **learning home** is `$ARSENAL_LEARN_HOME` when set, else `~/learn`. Slug the topic the user named (kebab-case, e.g. `rust-ownership`) and use `<learning home>/<slug>/`.
   - If the user named no topic, list the folders under the learning home and ask which one to continue, or what new topic to start.
   - If the topic is close to an existing folder, ask whether it is the same topic before creating a second one.
   - Create the folder when it does not exist.

Done when you hold one absolute path and have told the user where their learning lives. Every path below is relative to that folder; read and write the learning state only there, and leave the session's own directory untouched.

## Inside the learning workspace

The state of their learning is captured in several files:

- `MISSION.md`: The _reason_ the user is interested in the topic. This grounds all teaching. Use the format in [MISSION-FORMAT.md](./MISSION-FORMAT.md).
- `GLOSSARY.md`: The canonical language for the topic, holding only terms the user already understands. Use the format in [GLOSSARY-FORMAT.md](./GLOSSARY-FORMAT.md).
- `./reference/*.html`: Reference materials. These are the compressed learnings from the lessons: cheat sheets, reference algorithms, syntax, yoga poses. They are the raw units of learning. They should be beautiful documents which print out well, and are designed for quick reference.
- `RESOURCES.md`: Resources which can be explored to ground your teaching in contextual knowledge, or to acquire knowledge and wisdom. Use the format in [RESOURCES-FORMAT.md](./RESOURCES-FORMAT.md).
- `./learning-records/*.md`: Learning records, which capture what the user has learned. These are loosely equivalent to architectural decision records in software development: they capture non-obvious lessons and key insights that may need to be revised later, or drive future sessions. They are used to calculate the zone of proximal development. They are titled `0001-<dash-case-name>.md`, where the number increments each time. Use the format in [LEARNING-RECORD-FORMAT.md](./LEARNING-RECORD-FORMAT.md).
- `./lessons/*.html`: Lessons. A **lesson** is a single, self-contained HTML output that teaches one tightly-scoped thing tied to the mission. This is the primary unit of teaching.
- `./assets/*`: Reusable **components** shared across lessons. See [Assets](#assets).
- `NOTES.md`: A scratchpad for you to jot down user preferences, or working notes.

Write lessons, reference documents and the glossary in the language the user is learning in: the language of the conversation, unless `NOTES.md` says otherwise.

## Philosophy

To learn at a deep level, the user needs three things:

- **Knowledge**, captured from high-quality, high-trust resources
- **Skills**, acquired through highly-relevant interactive lessons devised by you, based on the knowledge
- **Wisdom**, which comes from interacting with other learners and practitioners

Before the `RESOURCES.md` is well-populated, your focus should be to find high-quality resources which will help the user acquire knowledge. Never trust your parametric knowledge.

Some topics may require more skills than knowledge. Learning more about theoretical physics might be more knowledge-based. For yoga, more skills-based.

### Fluency vs Storage Strength

Split between two types of learning:

- **Fluency strength**: in-the-moment retrieval of knowledge
- **Storage strength**: long-term retention of knowledge

Fluency can give the user an illusory sense of mastery, but storage strength is the real goal. Design lessons which build long-term retention by desirable difficulty:

- Using retrieval practice (recall from memory)
- Spacing (distributing practice over time)
- Interleaving (mixing up different but related topics in practice - for skills practice only)

## Lessons

A lesson is the main thing you produce: the unit in which knowledge and skills reach the user. Each lesson is one self-contained HTML file, saved to `./lessons/` and titled `0001-<dash-case-name>.html` where the number increments each time.

A lesson should be **beautiful**, with clean, readable typography and layout, since the user will return to these later to review. Think Tufte.

The lesson should be short, and completable very quickly. Learners' working memory is very small, and we need to stay within it. But each lesson should give the user a single tangible win that they can build on. It should be directly tied to the mission, and should be in the user's zone of proximal development.

Open the lesson file for the user when you can (`open` on macOS, `xdg-open` on Linux).

Each lesson should link via HTML anchors to other lessons and reference documents.

Each lesson should recommend a primary source for the user to read or watch. This should be the most high-quality, high-trust resource you found on the topic.

Each lesson should contain a reminder to ask followup questions to the agent. The agent is their teacher, and can assist with anything that's unclear.

## Assets

Lessons are built from reusable **components**, stored in `./assets/`: stylesheets, quiz widgets, simulators, diagram helpers, and anything else a second lesson could reuse.

Reuse is the default, not the exception. Before authoring a lesson, read `./assets/` and build from the components already there. When a lesson needs something new and reusable, write it as a component in `./assets/` and link to it, so a future lesson reuses it instead of duplicating it.

A shared stylesheet is the first component every learning workspace earns: every lesson links it, so the lessons look like one consistent course rather than a pile of one-offs. As the learning workspace grows, so should the component library.

## The Mission

Every lesson should be tied into the mission - the reason that the user is interested in learning about the topic.

If the user is unclear about the mission, or the `MISSION.md` is not populated, your first job should be to question the user on why they want to learn this.

Failing to understand the mission will mean knowledge acquisition is not grounded in real-world goals. Lessons will feel too abstract. You will have no way of judging what the user should do next.

Missions may change as the user develops more skills and knowledge. This is normal - update the `MISSION.md` and add a learning record to capture the change. Confirm with the user before changing the mission.

## Zone Of Proximal Development

Each lesson, the user should always feel as if they are being challenged 'just enough'.

The user may specify an exact thing they want to learn. If they don't, figure out their zone of proximal development by:

- Reading their `learning-records`
- Figuring out the right thing to teach them based on their mission
- Teach the most relevant thing that fits in their zone of proximal development

## Knowledge

Lessons should be designed around a skill the user is going to learn. The knowledge in the lesson should be only what's required to acquire that skill. You teach the knowledge first, then get the user to practice the skills via an interactive feedback loop.

Knowledge should first be gathered from trusted resources. Use `RESOURCES.md` to keep track of them. Lessons should be littered with citations - links to external resources to back up any claim made. This increases the trustworthiness of the lesson.

For acquiring knowledge, difficulty is the enemy. It eats working memory you need for understanding.

## Skills

If knowledge is all about acquisition, skills are about durability and flexibility. Make the knowledge stick.

For skill acquisition, difficulty is the tool. Effortful retrieval is what builds storage strength. Skills should be taught through interactive lessons. There are several tools at your disposal:

- Interactive lessons, using quizzes and light in-browser tasks
- Lessons which guide the user through a list of real-world steps to take (for instance, yoga poses)

Each of these should be based on a **feedback loop**, where the user receives feedback on their performance. This feedback loop should be as tight as possible, giving feedback immediately - and ideally automatically.

For quizzes, each answer should be exactly the same number of words (and characters, if possible), so formatting gives the user no clue about the answer.

## Acquiring Wisdom

Wisdom comes from true real-world interaction - testing your skills outside the learning environment.

When the user asks a question that appears to require wisdom, your default posture should be to attempt to answer - but to ultimately delegate to a **community**.

A community is a place (online or offline) where the user can test their skills in the real world. This might be a forum, a subreddit, a real-world class (budget permitting) or a local interest group.

Find high-reputation communities the user can join. If the user expresses a preference that they don't want to join a community, respect it.

## Reference Documents

While creating lessons, also create reference documents. Lessons can reference these documents - they are useful for tracking raw units of knowledge useful across lessons.

Lessons will rarely be revisited later - reference documents will be. They should be the compressed essence of the lesson, in a format designed for quick reference.

Some learning topics lend themselves to reference:

- Syntax and code snippets for programming
- Algorithms and flowcharts for processes
- Yoga poses and sequences for yoga
- Exercises and routines for fitness

A process, a sequence or a relation, in a lesson or a reference document, is drawn with the `diagram` skill and embedded as the SVG it renders.

The glossary is the essential reference for any topic with its own nomenclature. Once `GLOSSARY.md` exists, every lesson adheres to it.

## `NOTES.md`

The user will sometimes express preferences of how they want to be taught, or things you should keep in mind. This is the place to record those preferences, so you can refer back to them when designing lessons or working with the user.

## Attribution

Adapted from **Matt Pocock's `teach`** (github.com/mattpocock/skills at `3216582`, MIT). Changes: the learning workspace moved out of the current directory into a per-topic folder under a learning home, `GLOSSARY.md` added to the workspace files (the upstream ships its format but never links it), lessons follow the conversation's language, and the OpenAI agent wiring dropped.
