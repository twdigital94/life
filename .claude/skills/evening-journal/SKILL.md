---
name: evening-journal
description: Pull Tim's "Evening journal" voice recordings from Otter.ai and file them into the current year's journal page in Notion as lightly cleaned prose, with an actions list. Runs nightly via a scheduled Routine, but can also be invoked by hand ("file my evening journal", "check for evening journal entries", "did last night's journal get filed"). Handles skipped nights and never double-posts.
---

# Evening journal to Notion

> **The nightly Routine does not use this file.** Its instructions are stored in
> the Routine prompt itself, because the scheduled run cannot be relied on to
> have this repo. This file is for running the job by hand. Keep the two in step:
> if you change the method here, change the Routine prompt as well.

Tim records a spoken journal most evenings, lying down away from screens, into
Otter.ai. This skill moves those recordings into his written journal in Notion so
he has one continuous document.

He often titles the recording "Evening journal", but **the title is not how it is
found** and must not be relied on. See step 3.

He may skip nights. He may record late. Neither is a problem: this skill looks
back over several days every run and files anything that is missing, so a
skipped night is simply skipped and a late one gets picked up the next run.

## Configuration

| Setting | Value |
|---|---|
| Home timezone | `Asia/Bangkok` (UTC+7) |
| Otter reports times in | US Pacific (`America/Los_Angeles`) |
| How the journal is identified | By shape, never by title (step 3) |
| Evening window | 18:00 to 04:00 local, 3 to 40 minutes |
| Journal index page | `33f2072f-71a5-8068-9cbd-d0122fdf7a97` ("Journalling, Reflecting, Planning, Writing") |
| Lookback window | 4 days |
| State file | `state/evening-journal.json` |

**Timezone.** Tim is nomadic. If he moves, change `HOME_TZ` in
`scripts/journal_dates.py` and the "Home timezone" row above. Everything else
derives from it, including which calendar day an entry is filed under.

**Year page.** Never hardcode the year page ID. Resolve it each run (step 2) so
that 1 January needs no maintenance.

## Steps

### 1. Establish "now" in Tim's timezone

```bash
python3 scripts/journal_dates.py now
```

This prints the current date and time in the home timezone, plus the lookback
window to search Otter (as US Pacific dates, which is what Otter filters on).

### 2. Resolve the current year's journal page

Fetch the journal index page `33f2072f-71a5-8068-9cbd-d0122fdf7a97` and find the
child page for the current year. Titles have varied over the years ("2026",
"2023 Journal"), so match on the year appearing at the **start** of the title.

If no page exists for the current year, **stop and tell Tim** rather than
inventing one or falling back to last year's page. He may want it created inside
a particular structure. Say plainly that the page is missing and the entries are
still sitting in Otter.

### 3. Find candidate recordings

**Do not search by title.** `title_contains` cannot be trusted here, for two
separate reasons, both of which have already caused a missed night:

1. Tim does not always rename the recording, and Otter then invents a title of
   its own ("Daily Reflection and Work Automation Plans").
2. Otter's title index lags. On 9 September a recording titled exactly
   "Evening journal" was **not** returned by `title_contains: "evening journal"`
   even with no date filter at all, while a plain listing returned it fine.

So a title search can miss a correctly named recording. Do not use one, not even
as a first pass. It is not a shortcut, it is the failure mode.

**Instead, list and classify.** One `otter_search` over the window from step 1,
with **no `title_contains` and no `query`**, and `include_shared_meetings: false`.
Set `page_size: 25` and page through if there is a `next_cursor`. Then test each
result:

```bash
python3 scripts/journal_dates.py classify "2026/09/09 06:24:24" "8m 18s"
```

The shape test keeps recordings that start in the evening local window (18:00 to
04:00) and run 3 to 40 minutes. Client calls and work notes sit outside that
window or run far longer, so they drop out on their own. A title of "Evening
journal" is a helpful confirmation when it happens to be there, but it is never
what you search on.

**Then confirm before writing.** A shape match is a candidate, not a verdict.
Fetch the transcript and check it is Tim talking to himself: one speaker, first
person, reflecting on his day. If there is a second speaker, or it reads like a
client call, a meeting, or him narrating a work process, **skip it** and say in
your report that you skipped it and why. Never file a client conversation into
his personal journal.

For each surviving result, compute the calendar day it belongs to:

```bash
python3 scripts/journal_dates.py heading "2026/09/09 06:24:24"
```

This converts the Otter timestamp from US Pacific into the home timezone and
prints the entry heading, e.g. `**Evening, Wednesday 9 September**`. Recordings
made just after midnight still belong to the evening that just ended, so the
script rolls any recording before 04:00 local back to the previous day.

### 4. Skip anything already filed

An entry is already filed if **either** check trips:

- Its heading already appears in the year page's content. **This is the check
  that matters.** Notion is the record.
- Its Otter ID appears in `state/evening-journal.json`. This ledger is a
  convenience for manual runs only and may be out of date, since the nightly
  Routine does not write to it. If the two disagree, trust Notion.

To check the page without pulling 350k characters into context, fetch it and
slice the saved file:

```bash
python3 -c "
d = open('<saved-fetch-file>').read()
print('**Evening, Monday 7 September**' in d)
"
```

### 5. Write the entry

Fetch the full transcript with `otter_fetch`. Then write it up as **lightly
cleaned prose**:

- **Keep his voice.** First person, his phrasing, his swearing. This is his
  private journal, not a work document. Do not sand it down, do not make it
  polite, do not make it sound like a report.
- **Cut the noise.** Filler, false starts, repeated words, "um", verbal
  throat-clearing, and asides to the recorder ("test test 123", "hoping this is
  still recording", anything addressed to Claude or about the transcript itself).
- **Fix transcription errors** where the intent is obvious. Otter reliably
  mangles people's names, Thai place names, supplement names, and his own
  shorthand. Cross-check names against how they are spelled in earlier entries on
  the journal page rather than going with Otter's spelling. Some NZ slang is
  correct as transcribed and should be left alone.
- **When unsure, leave it exactly as he said it.** A slightly odd phrase in his
  journal is harmless. A confident wrong guess quietly rewrites his memory of the
  day, which is the one thing this automation must never do.
- **Do not invent.** Never add a thought he did not have. If a passage is too
  garbled to recover, leave it out rather than filling the gap.
- **Paragraph it.** Three to six paragraphs, broken where his thinking turns.
- Preserve meaning and intent exactly. This is cleanup, not a rewrite.

Then append the actions, taken from what he actually said he would do. Rewrite
Otter's stiff third-person action items into his own voice, drop the
`Tim Walker - tim@twsocial.co.nz :` prefix, and drop any that are just restating
the reflection rather than a real next step.

Final shape:

```
**Evening, Monday 7 September**
First paragraph of cleaned prose.

Second paragraph.

*Actions*
- Call Matt, though he's on holiday
- Finish the solar offer
- Start cold calling
```

If a recording has no real actions in it, leave the `*Actions*` block out
entirely rather than printing an empty heading.

### 6. Insert it in the right place

Entries on the year page run oldest to newest, headed like
`**Monday, 7 September**`. The evening entry belongs directly after that day's
morning entry.

- **Normal nightly run** (the entry is the newest thing on the page): append with
  `notion-update-page`, `command: insert_content`, `position: {"type":"end"}`.
  Cheap, and no risk of mangling the page.
- **Backfilling an older night** (later-dated content already sits below where
  this belongs): use `command: update_content` with an `old_str` anchored on the
  heading of the entry it should sit *before*, and an `new_str` of your entry
  followed by that same heading. Pick an anchor string that appears exactly once.

Leave a blank line between the evening entry and whatever follows.

### 7. Record what you filed

Append to `state/evening-journal.json`:

```json
{
  "otter_id": "L8N8eFA2octILx-IduwYrRpkrW8",
  "recorded_pt": "2026/09/07 06:24:53",
  "local_date": "2026-09-07",
  "heading": "**Evening, Monday 7 September**",
  "year_page": "33f2072f-71a5-8088-97ac-f07ef4ea9101",
  "filed_at": "2026-09-08T00:13:00+07:00"
}
```

Then commit and push to whatever branch the session was cloned on, so the next
run's fresh clone sees it:

```bash
BRANCH=$(git rev-parse --abbrev-ref HEAD)
git add state/evening-journal.json
git commit -m "Log evening journal entry for <date>"
git push -u origin "$BRANCH"
```

The commit is the audit trail and it is what makes deduplication survive into
the next run, since each run starts from a fresh clone. **Do not skip the push.**

## Reporting back

Keep it short. Tim is asleep when this runs and reads it later.

- Filed something: name the date(s), link the year page, one line on what the
  entry was about.
- Nothing to file: say so in one line. A skipped night is normal and needs no
  commentary.
- Something broke (no year page, Otter unreachable, push rejected): say exactly
  what failed and that the recording is still safe in Otter.

Never message him just to say the night was quiet if nothing at all happened and
nothing broke.

## Things to get right

- **Never double-post.** Both dedupe checks, every run.
- **Never invent journal content.** Under-including beats fabricating.
- **Never reformat or touch existing entries** on the page. Only add.
- The transcript is personal and often raw. It goes to Notion and nowhere else:
  no email, no ClickUp, no summarising it into another surface unless he asks.
