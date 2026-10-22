# Interview: behavioral scope by level and linked live-coding problems · Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Score behavioral stories against the scope their level is hired for, and make algorithm live-coding mocks link real LeetCode problems chosen by the patterns the user lacks.

**Architecture:** The `interview` skill is Markdown read by an agent: no code, no build, no test suite. Each task edits one or two skill files with exact text. Verification is reading the result against the spec, plus one script that checks every problem link in the new `PROBLEMS.md` against LeetCode's public GraphQL endpoint.

**Tech Stack:** Markdown, `sd` and `rg` for edits and checks, `curl` + `jq` for link checks. Spec: `docs/superpowers/specs/2026-10-22-interview-level-and-problems-design.md`.

**Rules for the executor:**
- Use `bat`, `rg`, `fd`, `sd`, `eza`, never `cat`, `grep`, `find`, `sed`, `ls`.
- Never build. No "Co-Authored-By" or AI attribution in commits; conventional commits.
- The working tree carries the user's **uncommitted edits** to `README.md`, `skills/idea/MAP-FORMAT.md` and `skills/idea/SKILL.md`. Never stage, commit, revert or reformat them. Stage only the files each task names (Task 8 explains how to stage only our part of `README.md`).
- Match the skill's prose: short declarative sentences, bold for the rule's name, `·` as separator, no exclamation marks.

---

### Task 1: Behavioral rubric gains "scope fits the level"

**Files:**
- Modify: `skills/interview/MOCK-FORMAT.md` (Rubrics table, `behavioral` row; new section after the table)

- [ ] **Step 1: Add the criterion to the `behavioral` row**

Replace the line

```
| `behavioral` | STAR complete · "I", not "we": the user's own actions · a measurable or concrete result · reflection: what was learned · two to three minutes, timed as above · answers the question asked |
```

with

```
| `behavioral` | STAR complete · "I", not "we": the user's own actions · a measurable or concrete result · reflection: what was learned · two to three minutes, timed as above · answers the question asked · scope fits the level, by [Scope by level](#scope-by-level) |
```

- [ ] **Step 2: Add the scope table right after the Rubrics table (before `## 4. The record`)**

```md
### Scope by level

The behavioral criterion **scope fits the level** asks whether the story shows the reach the level is hired for. A story whose scope is a lower level's scores at most 2 on it, however well told. A level the table does not name takes the nearest row (junior takes mid, principal takes staff), named at setup. A question no story answers (why this company, say) scores it `n/a`.

| Level | Scope the story shows | Story scope in `STORIES.md` |
| --- | --- | --- |
| mid | A task or feature the user owned end to end. No source defines a mid bar: this row is a baseline | `task` |
| senior | A project with several people, ambiguous requirements or significant technical risk; influence without authority | `project` |
| staff | Several teams or the organization: competing priorities between teams, technical direction | `multi-team` |

Sources: Tech Interview Handbook, *Behavioral interviews for senior candidates* (seniors "proactively demonstrate their scope"; stories "acceptable for more junior candidates can raise red flags"); Will Larson, *Staff Engineer* (staff is "evidence of impact at the company scope").
```

- [ ] **Step 3: Check**

Run: `rg -n "scope fits the level|### Scope by level" skills/interview/MOCK-FORMAT.md`
Expected: three matches (the rubric row, the heading, the sentence in the section).

- [ ] **Step 4: Commit**

```bash
git add skills/interview/MOCK-FORMAT.md
git commit -m "feat(interview): score behavioral scope against the level"
```

---

### Task 2: Stories declare their scope

**Files:**
- Modify: `skills/interview/STORIES-FORMAT.md` (template Index, story fields, bootstrap, rules)

- [ ] **Step 1: Index gains a Scope column**

Replace

```
| Id | Title | Competencies | Last scored | Used in |
| --- | --- | --- | --- | --- |
| [S-01](#s-01) | {title} | {competency}, {competency} | {score}/4, {YYYY-MM-DD}, or "never" | {company · stage, YYYY-MM-DD; …} |
```

with

```
| Id | Title | Competencies | Scope | Last scored | Used in |
| --- | --- | --- | --- | --- | --- |
| [S-01](#s-01) | {title} | {competency}, {competency} | {task \| project \| multi-team, or "unset"} | {score}/4, {YYYY-MM-DD}, or "never" | {company · stage, YYYY-MM-DD; …} |
```

- [ ] **Step 2: Each story gains a Scope field**

Replace

```
- Competencies: {from the list below}
- When: {year}, at {company}
```

with

```
- Competencies: {from the list below}
- Scope: {task | project | multi-team}
- When: {year}, at {company}
```

- [ ] **Step 3: Add a Scope section right after the `## Competencies` section (before `## The bootstrap`)**

```md
## Scope

How far the story reaches, which is what MOCK-FORMAT.md's [Scope by level](./MOCK-FORMAT.md#scope-by-level) scores against the level: `task` (a task or feature the user owned), `project` (a project with several people, ambiguity or real technical risk), `multi-team` (several teams or the organization). Set it from what the user did, not from the size of the company. A story written before scope existed reads `unset`: the first mock or bootstrap that uses it proposes one, written on the user's yes.
```

- [ ] **Step 4: The bootstrap asks for a story at the target scope**

Replace

```
Prompt next for a competency no story covers yet.
```

with

```
Prompt next for a competency no story covers yet. When no story reaches the scope of the levels in `PROFILE.md`'s Targets, prompt next for one that does ("a time you led something across several teams").
```

- [ ] **Step 5: Check**

Run: `rg -n "Scope" skills/interview/STORIES-FORMAT.md`
Expected: the Index header, the `- Scope:` field, the `## Scope` heading, and the bootstrap sentence.

- [ ] **Step 6: Commit**

```bash
git add skills/interview/STORIES-FORMAT.md
git commit -m "feat(interview): tag stories with their scope"
```

---

### Task 3: Fit and cheat sheet use the scope

**Files:**
- Modify: `skills/interview/FIT-FORMAT.md` (The plan rules)
- Modify: `skills/interview/SKILL.md` (Cheat sheet, first bullet)

- [ ] **Step 1: Fit names the scope gap**

In `FIT-FORMAT.md`, after the line starting `- **Unknown kind.**`, add:

```
- **Scope gap.** When the process has a behavioral stage and no story in `STORIES.md` reaches the scope of its level (MOCK-FORMAT.md's [Scope by level](./MOCK-FORMAT.md#scope-by-level)), that is a gap like any other: the plan drafts such a story when the user has one untold, or the gap reads out of reach with how to talk about it honestly.
```

- [ ] **Step 2: Cheat sheet puts level-scope stories first**

In `SKILL.md`, replace

```
- The stories most likely to be asked, each as a three-line STAR reminder, mapped to the questions they answer.
```

with

```
- The stories most likely to be asked, each as a three-line STAR reminder, mapped to the questions they answer; stories at the scope of the process's level come first.
```

- [ ] **Step 3: Check**

Run: `rg -n "Scope gap|scope of the process's level" skills/interview/FIT-FORMAT.md skills/interview/SKILL.md`
Expected: one match in each file.

- [ ] **Step 4: Commit**

```bash
git add skills/interview/FIT-FORMAT.md skills/interview/SKILL.md
git commit -m "feat(interview): plan for a missing story at the level's scope"
```

---

### Task 4: The curated problem list

**Files:**
- Create: `skills/interview/PROBLEMS.md`
- Create (scratch only, not committed): `$SCRATCH/check-problems.sh`, where `$SCRATCH` is the session's scratchpad directory

- [ ] **Step 1: Write `skills/interview/PROBLEMS.md`**

```md
# Problems

The curated list a live-coding mock picks from when neither the company's real questions nor its dossier name a problem: free LeetCode problems, seeded from Grind 75 (techinterviewhandbook.org/grind75) and topped up from NeetCode 150 where a pattern had fewer than two. Patterns are NeetCode's eighteen. Title, link and tags only: the statement is read on the site, never copied here.

Difficulty is LeetCode's own. Add a problem only with a link checked to exist and to be free.

| Problem | Link | Pattern | Difficulty |
| --- | --- | --- | --- |
| Two Sum | https://leetcode.com/problems/two-sum/ | Arrays & Hashing | easy |
| Valid Anagram | https://leetcode.com/problems/valid-anagram/ | Arrays & Hashing | easy |
| Contains Duplicate | https://leetcode.com/problems/contains-duplicate/ | Arrays & Hashing | easy |
| Ransom Note | https://leetcode.com/problems/ransom-note/ | Arrays & Hashing | easy |
| Longest Palindrome | https://leetcode.com/problems/longest-palindrome/ | Arrays & Hashing | easy |
| Majority Element | https://leetcode.com/problems/majority-element/ | Arrays & Hashing | easy |
| Group Anagrams | https://leetcode.com/problems/group-anagrams/ | Arrays & Hashing | medium |
| Top K Frequent Elements | https://leetcode.com/problems/top-k-frequent-elements/ | Arrays & Hashing | medium |
| Product of Array Except Self | https://leetcode.com/problems/product-of-array-except-self/ | Arrays & Hashing | medium |
| Valid Palindrome | https://leetcode.com/problems/valid-palindrome/ | Two Pointers | easy |
| 3Sum | https://leetcode.com/problems/3sum/ | Two Pointers | medium |
| Container With Most Water | https://leetcode.com/problems/container-with-most-water/ | Two Pointers | medium |
| Sort Colors | https://leetcode.com/problems/sort-colors/ | Two Pointers | medium |
| Trapping Rain Water | https://leetcode.com/problems/trapping-rain-water/ | Two Pointers | hard |
| Best Time to Buy and Sell Stock | https://leetcode.com/problems/best-time-to-buy-and-sell-stock/ | Sliding Window | easy |
| Longest Substring Without Repeating Characters | https://leetcode.com/problems/longest-substring-without-repeating-characters/ | Sliding Window | medium |
| Find All Anagrams in a String | https://leetcode.com/problems/find-all-anagrams-in-a-string/ | Sliding Window | medium |
| Minimum Window Substring | https://leetcode.com/problems/minimum-window-substring/ | Sliding Window | hard |
| Valid Parentheses | https://leetcode.com/problems/valid-parentheses/ | Stack | easy |
| Implement Queue using Stacks | https://leetcode.com/problems/implement-queue-using-stacks/ | Stack | easy |
| Min Stack | https://leetcode.com/problems/min-stack/ | Stack | medium |
| Evaluate Reverse Polish Notation | https://leetcode.com/problems/evaluate-reverse-polish-notation/ | Stack | medium |
| Largest Rectangle in Histogram | https://leetcode.com/problems/largest-rectangle-in-histogram/ | Stack | hard |
| Basic Calculator | https://leetcode.com/problems/basic-calculator/ | Stack | hard |
| Binary Search | https://leetcode.com/problems/binary-search/ | Binary Search | easy |
| First Bad Version | https://leetcode.com/problems/first-bad-version/ | Binary Search | easy |
| Search in Rotated Sorted Array | https://leetcode.com/problems/search-in-rotated-sorted-array/ | Binary Search | medium |
| Time Based Key-Value Store | https://leetcode.com/problems/time-based-key-value-store/ | Binary Search | medium |
| Median of Two Sorted Arrays | https://leetcode.com/problems/median-of-two-sorted-arrays/ | Binary Search | hard |
| Merge Two Sorted Lists | https://leetcode.com/problems/merge-two-sorted-lists/ | Linked List | easy |
| Linked List Cycle | https://leetcode.com/problems/linked-list-cycle/ | Linked List | easy |
| Reverse Linked List | https://leetcode.com/problems/reverse-linked-list/ | Linked List | easy |
| Middle of the Linked List | https://leetcode.com/problems/middle-of-the-linked-list/ | Linked List | easy |
| LRU Cache | https://leetcode.com/problems/lru-cache/ | Linked List | medium |
| Merge k Sorted Lists | https://leetcode.com/problems/merge-k-sorted-lists/ | Linked List | hard |
| Invert Binary Tree | https://leetcode.com/problems/invert-binary-tree/ | Trees | easy |
| Maximum Depth of Binary Tree | https://leetcode.com/problems/maximum-depth-of-binary-tree/ | Trees | easy |
| Balanced Binary Tree | https://leetcode.com/problems/balanced-binary-tree/ | Trees | easy |
| Diameter of Binary Tree | https://leetcode.com/problems/diameter-of-binary-tree/ | Trees | easy |
| Subtree of Another Tree | https://leetcode.com/problems/subtree-of-another-tree/ | Trees | easy |
| Lowest Common Ancestor of a Binary Search Tree | https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/ | Trees | medium |
| Binary Tree Level Order Traversal | https://leetcode.com/problems/binary-tree-level-order-traversal/ | Trees | medium |
| Validate Binary Search Tree | https://leetcode.com/problems/validate-binary-search-tree/ | Trees | medium |
| Kth Smallest Element in a BST | https://leetcode.com/problems/kth-smallest-element-in-a-bst/ | Trees | medium |
| Binary Tree Right Side View | https://leetcode.com/problems/binary-tree-right-side-view/ | Trees | medium |
| Construct Binary Tree from Preorder and Inorder Traversal | https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/ | Trees | medium |
| Lowest Common Ancestor of a Binary Tree | https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/ | Trees | medium |
| Serialize and Deserialize Binary Tree | https://leetcode.com/problems/serialize-and-deserialize-binary-tree/ | Trees | hard |
| Implement Trie (Prefix Tree) | https://leetcode.com/problems/implement-trie-prefix-tree/ | Tries | medium |
| Design Add and Search Words Data Structure | https://leetcode.com/problems/design-add-and-search-words-data-structure/ | Tries | medium |
| Word Search II | https://leetcode.com/problems/word-search-ii/ | Tries | hard |
| Kth Largest Element in a Stream | https://leetcode.com/problems/kth-largest-element-in-a-stream/ | Heap / Priority Queue | easy |
| K Closest Points to Origin | https://leetcode.com/problems/k-closest-points-to-origin/ | Heap / Priority Queue | medium |
| Task Scheduler | https://leetcode.com/problems/task-scheduler/ | Heap / Priority Queue | medium |
| Find Median from Data Stream | https://leetcode.com/problems/find-median-from-data-stream/ | Heap / Priority Queue | hard |
| Subsets | https://leetcode.com/problems/subsets/ | Backtracking | medium |
| Permutations | https://leetcode.com/problems/permutations/ | Backtracking | medium |
| Combination Sum | https://leetcode.com/problems/combination-sum/ | Backtracking | medium |
| Letter Combinations of a Phone Number | https://leetcode.com/problems/letter-combinations-of-a-phone-number/ | Backtracking | medium |
| Word Search | https://leetcode.com/problems/word-search/ | Backtracking | medium |
| Flood Fill | https://leetcode.com/problems/flood-fill/ | Graphs | easy |
| 01 Matrix | https://leetcode.com/problems/01-matrix/ | Graphs | medium |
| Number of Islands | https://leetcode.com/problems/number-of-islands/ | Graphs | medium |
| Rotting Oranges | https://leetcode.com/problems/rotting-oranges/ | Graphs | medium |
| Clone Graph | https://leetcode.com/problems/clone-graph/ | Graphs | medium |
| Course Schedule | https://leetcode.com/problems/course-schedule/ | Graphs | medium |
| Accounts Merge | https://leetcode.com/problems/accounts-merge/ | Graphs | medium |
| Minimum Height Trees | https://leetcode.com/problems/minimum-height-trees/ | Graphs | medium |
| Word Ladder | https://leetcode.com/problems/word-ladder/ | Graphs | hard |
| Network Delay Time | https://leetcode.com/problems/network-delay-time/ | Advanced Graphs | medium |
| Min Cost to Connect All Points | https://leetcode.com/problems/min-cost-to-connect-all-points/ | Advanced Graphs | medium |
| Cheapest Flights Within K Stops | https://leetcode.com/problems/cheapest-flights-within-k-stops/ | Advanced Graphs | medium |
| Climbing Stairs | https://leetcode.com/problems/climbing-stairs/ | 1-D Dynamic Programming | easy |
| House Robber | https://leetcode.com/problems/house-robber/ | 1-D Dynamic Programming | medium |
| Coin Change | https://leetcode.com/problems/coin-change/ | 1-D Dynamic Programming | medium |
| Word Break | https://leetcode.com/problems/word-break/ | 1-D Dynamic Programming | medium |
| Partition Equal Subset Sum | https://leetcode.com/problems/partition-equal-subset-sum/ | 1-D Dynamic Programming | medium |
| Longest Palindromic Substring | https://leetcode.com/problems/longest-palindromic-substring/ | 1-D Dynamic Programming | medium |
| Maximum Profit in Job Scheduling | https://leetcode.com/problems/maximum-profit-in-job-scheduling/ | 1-D Dynamic Programming | hard |
| Unique Paths | https://leetcode.com/problems/unique-paths/ | 2-D Dynamic Programming | medium |
| Longest Common Subsequence | https://leetcode.com/problems/longest-common-subsequence/ | 2-D Dynamic Programming | medium |
| Maximum Subarray | https://leetcode.com/problems/maximum-subarray/ | Greedy | medium |
| Jump Game | https://leetcode.com/problems/jump-game/ | Greedy | medium |
| Insert Interval | https://leetcode.com/problems/insert-interval/ | Intervals | medium |
| Merge Intervals | https://leetcode.com/problems/merge-intervals/ | Intervals | medium |
| Spiral Matrix | https://leetcode.com/problems/spiral-matrix/ | Math & Geometry | medium |
| Rotate Image | https://leetcode.com/problems/rotate-image/ | Math & Geometry | medium |
| String to Integer (atoi) | https://leetcode.com/problems/string-to-integer-atoi/ | Math & Geometry | medium |
| Add Binary | https://leetcode.com/problems/add-binary/ | Bit Manipulation | easy |
| Counting Bits | https://leetcode.com/problems/counting-bits/ | Bit Manipulation | easy |
| Number of 1 Bits | https://leetcode.com/problems/number-of-1-bits/ | Bit Manipulation | easy |
| Single Number | https://leetcode.com/problems/single-number/ | Bit Manipulation | easy |
```

- [ ] **Step 2: Write the link check script to the scratchpad**

`$SCRATCH/check-problems.sh`:

```bash
#!/usr/bin/env bash
# Checks every row of PROBLEMS.md against LeetCode's public GraphQL:
# the slug exists, it is free, and its title and difficulty match the row.
set -u
file="${1:-skills/interview/PROBLEMS.md}"
fail=0
while IFS='|' read -r _ title link pattern difficulty _; do
  title="$(echo "$title" | xargs)"; link="$(echo "$link" | xargs)"; difficulty="$(echo "$difficulty" | xargs)"
  [[ "$link" == https://leetcode.com/problems/* ]] || continue
  slug="${link#https://leetcode.com/problems/}"; slug="${slug%/}"
  body=$(jq -nc --arg s "$slug" '{query:"query q($s:String!){question(titleSlug:$s){title difficulty isPaidOnly}}",variables:{s:$s}}')
  res=$(curl -s https://leetcode.com/graphql -H 'Content-Type: application/json' -H 'Referer: https://leetcode.com' -d "$body")
  got_title=$(echo "$res" | jq -r '.data.question.title // empty')
  got_diff=$(echo "$res" | jq -r '.data.question.difficulty // empty' | tr '[:upper:]' '[:lower:]')
  paid=$(echo "$res" | jq -r '.data.question.isPaidOnly // empty')
  if [[ -z "$got_title" ]]; then echo "MISSING  $slug ($(echo "$res" | head -c 80))"; fail=1; continue; fi
  [[ "$paid" == "true" ]] && { echo "PAID     $slug"; fail=1; }
  [[ "$got_title" != "$title" ]] && { echo "TITLE    $slug: row '$title', site '$got_title'"; fail=1; }
  [[ "$got_diff" != "$difficulty" ]] && { echo "DIFF     $slug: row $difficulty, site $got_diff"; fail=1; }
  sleep 0.3
done < <(rg '^\| ' "$file")
[[ $fail == 0 ]] && echo "ALL OK"
```

- [ ] **Step 3: Run it**

Run: `bash $SCRATCH/check-problems.sh`
Expected: `ALL OK`.

- On `TITLE` or `DIFF`: fix the row to the site's value.
- On `PAID` or `MISSING`: remove the row, then rerun the pattern count below; if a pattern drops under two, add a free NeetCode 150 problem of that pattern and rerun the script.
- If every row prints `MISSING` with an HTML or 403 body, the endpoint is blocking scripts: instead check each slug against the NeetCode list in `https://github.com/neetcode-gh/leetcode` or the Grind 75 list (fetch with WebFetch), leave out any slug neither confirms, and say so in the commit body.

- [ ] **Step 4: Check pattern coverage**

Run: `rg '^\| .*https://leetcode' skills/interview/PROBLEMS.md | awk -F'|' '{gsub(/^ +| +$/,"",$4); print $4}' | sort | uniq -c`
Expected: exactly 18 patterns, each with a count of 2 or more.

- [ ] **Step 5: Commit**

```bash
git add skills/interview/PROBLEMS.md
git commit -m "feat(interview): add a curated list of linked LeetCode problems by pattern"
```

---

### Task 5: The pattern coverage format

**Files:**
- Create: `skills/interview/PATTERNS-FORMAT.md`

- [ ] **Step 1: Write the file**

````md
# PATTERNS.md Format

`PATTERNS.md` lives at the interview home root and tracks the algorithm patterns the user has practiced in live-coding mocks with a linked problem, so the next problem aims at what is missing rather than at what is comfortable. The first such mock creates it; the root build does not.

## Template

```md
# Patterns

## Coverage

| Pattern | Problems seen | Last scores | Average |
| --- | --- | --- | --- |
| {pattern} | {N} | {up to five, oldest first} | {average, or "never seen"} |

## Log

| Date | Problem | Pattern | Score | Record |
| --- | --- | --- | --- | --- |
| {YYYY-MM-DD} | [{title}]({link}) | {pattern} | {2.3, or 2.3 prepared} | [{record}]({path}) |
```

## Rules

- **Patterns** are the eighteen of [PROBLEMS.md](./PROBLEMS.md). Coverage lists all of them, the never-seen ones included.
- **A problem's score** is the average of its mock's scored criteria (`n/a` left out), to one decimal, marked `prepared` when the attempt was, as in QUESTIONS-FORMAT.md.
- **A weak pattern** averages below 3 over its last five unseen problems, with at least two of them. Two, not three as for weak spots, because each mock yields one problem.
- **Order.** Rebuild Coverage after each linked live-coding mock: never-seen patterns first, then weak patterns, weakest first, then the rest.
- The Log is append-only. A problem in the Log is not chosen again unless the plan asks for a retry.
- A written problem (a practical stage) has no pattern and never enters this file.
````

The block above is fenced with four backticks only so the inner ```` ```md ```` template survives; the file itself starts at `# PATTERNS.md Format`.

- [ ] **Step 2: Check**

Run: `bat -p skills/interview/PATTERNS-FORMAT.md`
Expected: heading, intro paragraph, `## Template` with one fenced block, `## Rules` with six bullets.

- [ ] **Step 3: Commit**

```bash
git add skills/interview/PATTERNS-FORMAT.md
git commit -m "feat(interview): track live-coding pattern coverage in PATTERNS.md"
```

---

### Task 6: Live-coding mocks pick and link the problem

**Files:**
- Modify: `skills/interview/MOCK-FORMAT.md` (Setup question order; Live coding section; record header; root update)

- [ ] **Step 1: Point the setup's question order at the live-coding rule**

Replace

```
Choose the questions in this order: real questions from `QUESTIONS.md` for this company and type, then what the company dossier says it asks, then the weak spots in `QUESTIONS.md`, then questions fit for the level. Never repeat a question the user already answered in a mock, unless it is a retry the plan asked for.
```

with

```
Choose the questions in this order: real questions from `QUESTIONS.md` for this company and type, then what the company dossier says it asks, then the weak spots in `QUESTIONS.md`, then questions fit for the level. Never repeat a question the user already answered in a mock, unless it is a retry the plan asked for. A live-coding mock chooses its problem as [Live coding](#live-coding) lays out.
```

- [ ] **Step 2: Rewrite the Live coding section**

Replace everything from `### Live coding` up to (not including) `### System design` with:

```md
### Live coding

**The problem.** A stage the company dossier says is practical (build an endpoint, refactor, consume an API) gets a problem written for it, close to what the company asks, with no link. Any other live-coding stage, one the dossier says nothing about included, takes a real problem with a link, in this order:

1. A real question from `QUESTIONS.md` for this company.
2. A problem the company dossier cites, with its link.
3. From [PROBLEMS.md](./PROBLEMS.md): a pattern `PATTERNS.md` has never seen, then its weakest pattern, by [PATTERNS-FORMAT.md](./PATTERNS-FORMAT.md)'s rule.

Difficulty follows the level: mid easy or medium, senior medium, staff medium or hard. Never a problem already in the Log of `PATTERNS.md`, unless the plan asks for a retry.

The mock lives in `mocks/{NNNN}-live-coding/`, in the language and test runner of `PROFILE.md`:

- `PROBLEM.md`: for a linked problem, its title and link, the function signature in the mock's language and the constraints that matter, never the statement: the user reads it on the site. For a written problem, the statement, two examples and the constraints. No tests either way.
- `solution.{ext}`: an empty function with its signature.
- `solution.test.{ext}`: empty. The user's own tests go here, and they count.

Before the user starts, write the **hidden tests** (the edge cases a strong candidate covers) into the system temp directory, outside the interview home, so they are fixed before any code exists and the user cannot see them. Read the solution file on every turn, as an interviewer watches the shared editor, and probe what it shows. When the user says they are done, or the time is up, move the hidden tests into the folder and run both suites. When the folder cannot run them as it is, set up the minimum the runner needs (a `package.json`, say) and tell the user.

A linked problem's hidden tests come from what the agent knows of it, and the site cannot be read, so **the official statement wins**: a hidden test the user shows contradicts it is dropped, and the record says so. After the mock the user may submit to the site's judge; its verdict goes into the record as a second piece of evidence and never changes a score.
```

- [ ] **Step 3: Record header carries the problem**

In the record template, replace

```
- Level: {level} · Language: {language}
```

with

```
- Level: {level} · Language: {language}
- Problem (live coding): [{title}]({link}) · {pattern} · {difficulty}, or "written"
- Hidden tests (live coding): {passed} of {total}{; dropped "{test}": it contradicts the statement}
- Judge (linked problem): {the site's verdict, or "not submitted"}
```

- [ ] **Step 4: Root update includes PATTERNS.md**

Replace

```
- `fit.md`: the plan row's Done mark, when the mock belongs to a process.
```

with

```
- `PATTERNS.md`: for a live-coding mock with a linked problem, its Log row and Coverage rebuilt, as PATTERNS-FORMAT.md lays out; created by the first one.
- `fit.md`: the plan row's Done mark, when the mock belongs to a process.
```

- [ ] **Step 5: Check**

Run: `rg -n "PROBLEMS.md|PATTERNS|official statement wins|Judge \(linked" skills/interview/MOCK-FORMAT.md`
Expected: matches in the Live coding section, the record header and the root update; `bat -p skills/interview/MOCK-FORMAT.md | rg -c "^### Live coding"` prints `1`.

- [ ] **Step 6: Commit**

```bash
git add skills/interview/MOCK-FORMAT.md
git commit -m "feat(interview): link live-coding mocks to real problems chosen by pattern"
```

---

### Task 7: SKILL.md and QUESTIONS-FORMAT.md wire it in

**Files:**
- Modify: `skills/interview/SKILL.md` (Locating, Dossier, Practice, Mocks)
- Modify: `skills/interview/QUESTIONS-FORMAT.md` (Log rules)

- [ ] **Step 1: The root lists PATTERNS.md**

Replace

```
Its root holds `PROFILE.md`, `STORIES.md`, `QUESTIONS.md` and `practice/` (mocks tied to no process).
```

with

```
Its root holds `PROFILE.md`, `STORIES.md`, `QUESTIONS.md`, `PATTERNS.md` (once a live-coding mock has linked a problem) and `practice/` (mocks tied to no process).
```

- [ ] **Step 2: The dossier asks which problems the company asks**

Replace

```
- On the company's topic: how it interviews for this role, and what it builds and with which stack.
```

with

```
- On the company's topic: how it interviews for this role, and what it builds and with which stack. When it codes live, whether the problems are algorithmic or practical, and which algorithm problems it has asked, each with its link: LeetCode's company tags are paid, so the free sources (`github.com/liquidslr/leetcode-company-wise-problems`, interview reports on LeetCode Discuss) are where to look.
```

- [ ] **Step 3: Practice shows patterns and scope**

Replace

```
The root is the readiness every process draws on, so practice with no process aims at the root's weak points. Read `QUESTIONS.md`, the index of `STORIES.md`, and every `STATUS.md` in state `open`. Show:

- Each open process with its next stage, its date and the days left.
- The three weakest spots, by QUESTIONS-FORMAT.md's rule, each with its latest evidence.
- The competencies no story covers.
```

with

```
The root is the readiness every process draws on, so practice with no process aims at the root's weak points. Read `QUESTIONS.md`, the index of `STORIES.md`, `PATTERNS.md` when it exists, and every `STATUS.md` in state `open`. Show:

- Each open process with its next stage, its date and the days left.
- The three weakest spots, by QUESTIONS-FORMAT.md's rule, each with its latest evidence.
- The competencies no story covers, and whether any story reaches the scope of the levels in `PROFILE.md`'s Targets.
- The patterns never seen and the weak patterns, by [PATTERNS-FORMAT.md](./PATTERNS-FORMAT.md)'s rule, when the user's targets include live coding.
```

- [ ] **Step 4: Mocks done line**

Replace

```
Done when MOCK-FORMAT.md's record is written, and `QUESTIONS.md`, `STORIES.md` and the plan row are updated.
```

with

```
Done when MOCK-FORMAT.md's record is written, and `QUESTIONS.md`, `STORIES.md`, `PATTERNS.md` (for a linked live-coding problem) and the plan row are updated.
```

- [ ] **Step 5: QUESTIONS.md Log rows carry link and pattern**

In `QUESTIONS-FORMAT.md`, after the bullet starting `- A mock row's score is`, add:

```
- A live-coding question with a linked problem writes its Question as `[{title}]({link}) · {pattern}`, so the Log and `PATTERNS.md` point at the same problem.
```

- [ ] **Step 6: Check**

Run: `rg -n "PATTERNS" skills/interview/SKILL.md skills/interview/QUESTIONS-FORMAT.md`
Expected: Locating, Practice (two), Mocks done line in `SKILL.md`; one line in `QUESTIONS-FORMAT.md`. And `rg -n "liquidslr" skills/interview/SKILL.md` prints the dossier line.

- [ ] **Step 7: Commit**

```bash
git add skills/interview/SKILL.md skills/interview/QUESTIONS-FORMAT.md
git commit -m "feat(interview): wire pattern coverage and problem sources into the skill"
```

---

### Task 8: README and version

**Files:**
- Modify: `README.md` (interview section, two sentences) — the file also holds the user's uncommitted `idea` edits: stage ONLY our two sentences
- Modify: `.claude-plugin/plugin.json` (`"version": "0.6.0"` → `"0.7.0"`)

- [ ] **Step 1: Edit the README in the working tree and in a copy of HEAD**

```bash
SCRATCH=<the session scratchpad>
git show HEAD:README.md > "$SCRATCH/README.head.md"
for f in README.md "$SCRATCH/README.head.md"; do
  sd -F '`STORIES.md` (a STAR story bank tagged by competency) and `QUESTIONS.md` (every question you faced, in mocks and for real, with your weak spots).' '`STORIES.md` (a STAR story bank tagged by competency and scope), `QUESTIONS.md` (every question you faced, in mocks and for real, with your weak spots) and, after your first linked live-coding mock, `PATTERNS.md` (the algorithm patterns you have practiced, and the weak ones).' "$f"
  sd -F 'and a live-coding mock runs hidden tests against code you write in a real file.' 'a behavioral story is scored against the scope your level is hired for, and a live-coding mock links a real LeetCode problem picked by the patterns you lack and runs hidden tests against code you write in a real file.' "$f"
done
```

- [ ] **Step 2: Stage only our change**

```bash
git update-index --cacheinfo 100644,"$(git hash-object -w "$SCRATCH/README.head.md")",README.md
git diff --cached README.md
```

Expected: the staged diff shows only the two interview sentences. `git diff README.md` (unstaged) still shows the user's `idea` edits.

- [ ] **Step 3: Bump the version**

Run: `sd '"version": "0.6.0"' '"version": "0.7.0"' .claude-plugin/plugin.json && rg -n version .claude-plugin/plugin.json`
Expected: `"version": "0.7.0"`.

- [ ] **Step 4: Commit**

```bash
git add .claude-plugin/plugin.json
git commit -m "docs(interview): describe scope scoring and linked problems; bump to 0.7.0"
git status --short
```

Expected after commit: only ` M README.md`, ` M skills/idea/MAP-FORMAT.md`, ` M skills/idea/SKILL.md` remain (the user's edits).

---

### Task 9: Dry read against the spec

**Files:** none modified unless a gap is found.

- [ ] **Step 1: Walk a senior behavioral mock**

Read `SKILL.md` → `MOCK-FORMAT.md` → `STORIES-FORMAT.md` as the agent would for `acme: mock behavioral` at level senior. Confirm: the rubric has seven criteria; a `task`-scope story scores at most 2 on scope; an `unset` story gets its scope proposed and written only on a yes.

- [ ] **Step 2: Walk a practice live-coding mock with no `PATTERNS.md`**

Read the path for `mock live coding` with no process. Confirm: the problem comes from `PROBLEMS.md`, a never-seen pattern, difficulty by level; `PROBLEM.md` holds link, signature and constraints with no statement; the record has Problem, Hidden tests and Judge lines; `PATTERNS.md` gets created with all eighteen patterns in Coverage.

- [ ] **Step 3: Walk a practical stage**

Confirm a stage the dossier calls practical writes its own problem, has no link, and never touches `PATTERNS.md`.

- [ ] **Step 4: Spec coverage**

Check each bullet of the spec's Design section against the files with `rg`. Fix any gap in the file it belongs to and commit it as `fix(interview): <what>`.

---

### Task 10 (before merge): Drop the spec and the plan

- [ ] **Step 1: Remove them**

```bash
git rm docs/superpowers/specs/2026-10-22-interview-level-and-problems-design.md docs/superpowers/plans/2026-10-22-interview-level-and-problems.md
git commit -m "chore: drop the interview plan and spec from the branch"
```
