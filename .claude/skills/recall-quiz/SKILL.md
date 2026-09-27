---
name: recall-quiz
description: Build Tim's next "Second Pass" quiz round from his own Notion notes (Marketing Insights, book highlights, Life Insights, Learning Thai) and load it into his quiz page, with spaced repetition so missed ideas come back in 2 days and then a week. Runs every second morning via a scheduled Routine, but use it by hand whenever Tim says "quiz me", "new quiz round", "make me a quiz", "test me on my notes", "what did I get wrong last time", "change my Thai task", or asks about his recall quiz, Second Pass, spaced repetition on his notes, or remembering what he reads and listens to. Also use it when he asks to add a new note source to the quiz or to change how it works.
---

# Second Pass: recall quiz from Tim's notes

> **The scheduled Routine carries its own copy of these instructions** in its
> prompt, so it does not depend on this repo being cloned. If you change the
> method here, update the Routine prompt too (see "Keeping the Routine in step").

Tim takes a lot of notes from books, podcasts, newsletters and emails, and almost
never revisits them. This skill turns those notes into a 10 minute quiz every
couple of days. The point is not to test him, it is to **get him thinking**:
recall the idea, connect it to other ideas, and apply it to his work and life.
Missed ideas come back soon, known ideas drift further out.

## How it fits together

| Piece | Where |
|---|---|
| Quiz page | https://claude.ai/artifact/7gyNY5a7bgoMmCxtPJpX15 ("Second Pass") |
| Page source | `.claude/skills/recall-quiz/assets/second-pass.html` |
| Page data | The page's own database, read and written with the `ArtifactData` tool |
| Example round | `.claude/skills/recall-quiz/references/example-round.json` (round 1) |
| Schedule | Routine "Second Pass quiz round", every second day at 06:52 Asia/Bangkok. Needs the Notion connector attached in the Routines UI |
| Timezone | Asia/Bangkok. Change here and in the Routine cron if Tim moves |

**The page is the engine; you only write data.** It renders whatever round
`meta/current` points at, grades the answers, and does all the spacing maths
itself. A normal run never republishes the HTML. It reads the database, reads
Notion, writes one new round document and moves the pointer.

### Database layout (artifact database)

| Document | Written by | What it holds |
|---|---|---|
| `meta/current` | you | `{roundId, number, updatedAt}`, the round the page shows |
| `rounds/<YYYY-MM-DD>` | you | The whole round (schema below) |
| `results/<roundId>` | page | `{roundId, startedAt, finishedAt?, answers:[{qid, type, section, rating, response, ideaIds, coach?, at}]}` |
| `ideas/<ideaId>` | page | `{id, title, note, source, url, section, box, due, lastSeen, history:[{d, r, q}]}` |
| `thai/<taskId>` | page | `{id, done, note, updatedAt}`, how the weekly Thai task went |

Ratings are `got`, `shaky`, `missed`. The page schedules each idea: missed comes
back in **2 days**, a first "got it" in **7 days**, then 16, 35, 90. Shaky comes
back in about half the current gap (minimum 2 days). Never write to `ideas/` or
`results/` yourself; that is the page's job and two writers would clash.

## Sources in Notion

| Source | Where | Notes |
|---|---|---|
| Marketing Insights | data source `collection://2fc2072f-71a5-80d5-90cc-000b95785eb5` (under TWdigital / Marketing Brain) | One page per insight. Mostly Hormozi, plus Seth Godin and others. Title is `Insights`, plus `Source`, `Topics` |
| Books | data source `collection://2f42072f-71a5-80c8-9f1a-000b673c9f8c` (Life / Reading) | One page per book of Kindle highlights with page numbers. **Italic lines are Tim's own reactions**; those are gold. Use any book page with content, whatever its Status |
| Life Insights | page `3602072f-71a5-80fd-a165-d793c748a14e` | Podcast notes in toggles (Naval, Mark Manson, Tim Ferriss, James Clear). Yellow-highlighted lines are his own thoughts |
| Life Insights - emails | data source `collection://1b445a86-be94-462e-80d2-27932cb5abd5` | Newsletter pieces (JL Collins, Chris Williamson, Hormozi) |
| Learning Thai | page `3e82072f-71a5-8071-a70b-d94c73151a93` | Everyday phrases he actually uses. Thai section only |
| Thai Language School | page `3e82072f-71a5-8021-9900-f66ed9bc55ac` (child of Learning Thai) | Course notes from a few years ago, Lessons 1 to 11. Thai section only |
| Thai Language (older) | page `3382072f-71a5-808c-9055-cf0c5ef32294` | A few pronunciation notes |

If Tim adds a new source, add it to this table and the Routine prompt. Find
things with `notion-search`, list databases with `notion-query-data-sources`,
and read pages with `notion-fetch`.

## Steps

### 1. Work out today

Today is the current date in Asia/Bangkok, as `YYYY-MM-DD`. That is the new
round's id. Also note the weekday for `dateLabel` ("Tue 29 Sep").

### 2. Read the state

With `ArtifactData` on the page URL:

- `get` `meta/current` for the last round id and number.
- If `rounds/<today>` already exists, stop: today's round is already made
  (perhaps by hand). Report that in one line and do nothing else. Only replace it
  if Tim explicitly asks for a fresh round today, and never once
  `results/<today>` has answers in it.
- `get` the last round and its `results/<lastId>`.
- `list` `ideas` (limit 1000). This is the full memory of what he has seen.
- `list` `thai` for how the recent Thai tasks went.
- `list` `rounds` (limit 10 is enough) to see recent quotes and question types
  so you don't repeat them.

From that, build three lists:

- **Due**: ideas with `due <= today`. Missed first, then oldest due.
- **Unanswered**: ideas from the last round's questions that have no answer in
  its results. He skipped them, so treat them as due.
- **Seen**: every idea id in `ideas`. Anything not in here is new.

If he did not touch the last round at all, keep this round light (the due and
unanswered ideas plus a couple of new ones) rather than piling on.

### 3. Pick the ideas

Aim for **8 or 9 idea questions** plus **3 or 4 Thai questions**. That is about
10 minutes. Mix:

- **Reviews (up to 4)**: from Due and Unanswered. Ask about the same idea from a
  **different angle and question type** than last time (the idea's `history`
  shows the type used). If he missed a recall question, try a scenario or a
  match; if he got an MCQ, make him produce it himself this time. The idea keeps
  its id, so the page carries its schedule on.
- **New (4 to 6)**: ideas not yet seen. Spread across Marketing Insights, Books
  and Life Insights where possible. Favour notes added in the last couple of
  weeks, because seeing fresh notes come back quickly is what will keep him
  taking notes. Read one or two book pages properly each run rather than
  skimming them all; rotate books over time.
- **At least one cross-source question** that puts two ideas from different
  sources side by side (Hormozi's "price is a signal" next to Alchemy's
  "reassuringly expensive" aspirin; Guidara's 5% next to Sutherland's 20% more
  enjoyable). This is where the best thinking happens.
- **One or two "apply it" long answers**, never more. One about his work (he
  runs TWdigital, a small digital marketing agency, with clients like Carrick
  Winery, Croplands, Coolshrub and Calm Mind Rebellion), and/or one about his
  life (he lives in Chiang Mai, is into breathwork, journalling and fitness,
  and wants to meet new people).

Where Tim wrote his own reaction to a highlight (italics in book notes, yellow
highlights in Life Insights), put it in `yourNote` so he sees what he thought
at the time. His own applications stick far better than the author's words.

### 4. Write the questions

Question types the page supports:

| `type` | Use it for | Fields |
|---|---|---|
| `mcq` | Quick recall, "who said it", scenario judgement | `options` (3 or 4), `correct` (index) |
| `short` | Recall from memory in a sentence | `answer` |
| `long` | Apply it to work or life. No right answer | `answer` (the idea, restated), optional `scenario` |
| `cloze` | One missing word or phrase. Put `___` in `prompt` | `answer`, `accept` (other spellings) |
| `match` | 4 or 5 pairs: quote to author, idea to example, Thai to English | `pairs` [[left, right], ...] |
| `order` | A real sequence: a playbook, a process, steps in a story | `items` in the correct order (page shuffles) |

Every question also has: `kind: "q"`, a unique `id` within the round (`q1`...,
Thai `t1`...), `section` (`ideas` or `thai`), a short `label` eyebrow ("Recall",
"Apply it · your work", "Who said it", "Two books, one move"), `ideas` (list of
`{id, title, note, source, url}`), `prompt`, and `explain` (shown after
answering). Optional: `scenario`, `yourNote`, `thai` (Thai script shown with the
question), `speak` (Thai script revealed only after answering, with a play
button).

Idea objects: `id` is a stable slug, `<author>-<concept>` (e.g.
`hormozi-price-is-a-signal`, `thai-tao-rai`). **Reuse an existing id** from
`ideas` when you are asking about the same concept again, or the schedule
breaks. `title` is a short concept name he would recognise ("Price is a
signal"), `note` is the Notion page title, `source` is the person or page, `url`
is the Notion page link.

Writing well:

- **Vary the angle.** Don't make every question "what did X say about Y". Use
  scenarios from his real work ("A Croplands lead has been on three calls and
  still hasn't bought. Which of Hormozi's two problems is it?"), predictions
  ("what happened to close rates?"), odd-one-out, and "which idea explains this".
- **Plausible wrong answers.** The best distractors are other real ideas from
  his notes, so even the wrong options teach something. Say so in `explain`.
- **Keep it in his words and at his level.** Plain NZ English, no jargon he
  didn't use himself. No em dashes.
- **Stay faithful to the notes.** Never invent a claim and pin it on an author.
  If you add context from general knowledge, make it clearly yours in `explain`.
- `explain` should add something, not just repeat the answer: a second detail
  from the same note, a link to another idea, or his own note.
- Keep prompts to one or two sentences. Long context goes in `scenario`.

### 5. Quotes

Put **one or two** quote cards between questions: `{kind: "quote", text, mark,
by}`. `mark` is the few words to highlight. Take them verbatim from his notes
(books, Life Insights, the italic quotes in Unreasonable Hospitality). They can
echo the round's theme but must never give away an answer in the same round.
Don't reuse a quote from the last five rounds.

### 6. Thai section

Always last. 3 or 4 questions drawn from his Learning Thai and Thai Language
School notes, **only on things already in his notes**: he wants to confirm he
knows it, not learn new material in the quiz. Include any Thai ideas that are
due. Mix match, cloze, MCQ and short "how do you say" questions. Add Thai
script in `thai` or `speak` so he can hear it (the page uses the device's Thai
voice when one exists). Only add script you are confident in. His
romanisation is loose (krap/krab/khrap, pom/phom), so put the common variants in
`accept`.

If his notes contain something slightly off, don't quiz him on the wrong
version. Quiz him on it correctly and gently point out the difference in
`explain` (e.g. "nam khaeng" is ice itself, not water with ice).

**The weekly task** (`thaiTask`) is one small real-world mission for the week,
somewhere out in Thai daily life, since he doesn't have many Thai friends yet:
street stalls, 7-Eleven, the market, a Grab driver, a barber, the gym front
desk, a coffee shop. Built around phrases from his notes plus **one** new common
expression (the `phrase`). His level is basic, so keep it achievable in a
minute or two of talking.

- Look at the most recent `thai/<id>` doc. If the current task is **less than 6
  days old**, carry the same `thaiTask` object over unchanged (same `id`), so
  his progress sticks to it.
- Otherwise write a new one with `id` = today. Build on how the last one went:
  if he did it and his note says it went well, step up a little; if he didn't
  do it or struggled, make the next one easier or in a friendlier setting.
- Shape: `{id, title, phrase: {roman, thai, meaning}, where, steps: [...], stretch}`.
  Steps are the actual lines to say, in order. Four or five steps.

### 7. Round shape

```json
{
  "id": "2026-09-29",
  "number": 2,
  "dateLabel": "Tue 29 Sep",
  "headline": "A short, specific title for the round's theme",
  "intro": "One or two sentences on what's in it, e.g. how many are coming back.",
  "minutes": 10,
  "nextRound": "Thursday morning",
  "items": [ ...questions and quotes in the order he'll see them... ],
  "thaiTask": { ... }
}
```

Order the items so it flows: open with a quick win (an MCQ or match), put the
long answers in the middle, never two long answers in a row, a quote card after
the first third, Thai questions last. See `references/example-round.json` for a
complete real round.

### 8. Save it

Write the round to a JSON file first and check it parses (`python3 -m json.tool`).
Check every `mcq` has a valid `correct` index, every `cloze` prompt contains
`___`, and question ids are unique. Then one `ArtifactData` `batch` on the page
URL:

1. `set` `rounds/<today>` from the file (`file_path`).
2. `set` `meta/current` to `{roundId, number, updatedAt}`.

The round goes first so the pointer never points at a missing round. Don't
touch `ideas`, `results` or `thai`.

## Reporting back

Tim reads this when he wakes up. One or two plain lines:

- It worked: "Round 7 is ready: 3 ideas coming back, 5 new (mostly Alchemy and
  Hormozi), new Thai task at the market." Plus the page link.
- Nothing to do (today's round already in play): say so in one line.
- Something broke (Notion or the page database unreachable, a write refused):
  what failed, in plain English, and that the previous round is still on the page.

No lists of question ids, no tool names, no JSON.

## Changing the page

Only if Tim asks for a change to how the quiz looks or works. Edit
`assets/second-pass.html` and republish it to the same URL with the `Artifact`
tool (pass `url`, omit `capabilities` so `db` and `sample` carry over). The
database survives republishing. If a new question type is added, add it to the
table in step 4 and to the Routine prompt.

## Keeping the Routine in step

The Routine's prompt is this file's body from "Second Pass: recall quiz" down,
pasted in full. After editing this file, update the Routine prompt the same way
(`update_trigger` with the new text), or the two will drift.
