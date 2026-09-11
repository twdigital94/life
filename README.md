# life

Personal automations.

## Evening journal

Tim records a spoken journal most evenings into Otter.ai under the title
**Evening journal**. A scheduled Routine runs every night and files those
recordings into the current year's journal page in Notion, so the vocal habit
ends up in the same document as the written one.

Each entry lands as lightly cleaned prose in his own voice, directly after that
day's morning entry, followed by a short actions list:

```
**Evening, Monday 7 September**
Day one of Health Freak Week, done and dusted. Feel really calm, really good...

*Actions*
- Call Matt, though he may be on holiday
- Finish the solar offer tomorrow
```

### How it runs

| | |
|---|---|
| Schedule | 00:13 Asia/Bangkok, nightly (`13 17 * * *` UTC) |
| Source | Otter.ai recordings titled "Evening journal" |
| Destination | Notion, current year's page under *Life / Journalling, Reflecting, Planning, Writing* |
| Logic | The Routine prompt (self-contained). [`SKILL.md`](.claude/skills/evening-journal/SKILL.md) mirrors it for manual runs |
| Dates | [`scripts/journal_dates.py`](scripts/journal_dates.py), manual runs only |
| Dedupe | The headings on the Notion page. No ledger |

### Where the instructions actually live

**The nightly Routine is self-contained.** Its full instructions are stored in
the Routine prompt itself, not in this repo. It does not read the skill file, run
the script, or write a ledger, and it does not need the repo cloned at all.

That is deliberate. For four nights the automation never filed a single entry,
including a run handed the exact recording and told to file it. Every entry in
the journal was put there by hand. The common factor was that the run depended on
reading instructions out of this repo and pushing a commit back. Removing that
dependency removes the whole class of failure.

**Notion is the only record.** Deduplication is a check for the heading on the
year page. There is no ledger to keep in sync, and nothing to commit.

The skill in `.claude/skills/evening-journal/` is still here for running the job
by hand in a session that does have the repo. If you change how the job works,
change the Routine prompt too, or they will drift apart.

### Finding the recording

The automation does **not** search Otter by title. It lists every recording in
the window and picks the journal out by shape: starts 18:00 to 04:00 local, runs
3 to 40 minutes, one speaker, reads as Tim reflecting rather than a client call.

Two separate things make a title search unreliable, and each has already cost a
night:

- **8 Sep:** the recording was not renamed, so Otter auto-titled it "Daily
  Reflection and Work Automation Plans" and a title search found nothing.
- **9 and 10 Sep:** the recordings *were* titled "Evening journal", and a title
  search still did not return them that night. Otter's title index lags by hours.
  By the next morning it had caught up, which is what made this so confusing.

So naming it "Evening journal" is nice but changes nothing mechanically. The
shape test is what actually finds it.

### Skipped nights and doubles

Every run looks back **4 days**, not just at last night. A skipped night is
simply skipped. A night recorded too late for that night's run gets picked up by
the next one and still filed under the right day.

Nothing is ever posted twice: each run checks the recording's Otter ID against
the ledger *and* checks whether the heading already exists on the Notion page.
The ledger is committed after every run, which is how the check survives into
the next one.

### The year rollover

There is nothing to update on 1 January. The Routine resolves the year page from
the parent index page each run and looks for one whose title starts with the
current year.

The one thing that needs a human: the **2027 page has to exist**. If it doesn't,
the run stops and says so rather than filing into 2026, and the recordings stay
safe in Otter until the page is there.

### If Tim moves country

Otter reports recording times in US Pacific, so the automation converts them to
work out which day an entry belongs to. Change `HOME_TZ` in
[`scripts/journal_dates.py`](scripts/journal_dates.py), and move the Routine's
cron to match the new midnight.

```bash
python3 scripts/journal_dates.py now
python3 scripts/journal_dates.py heading "2026/09/07 06:24:53"
```

### Running it by hand

Ask in any session with Otter and Notion connected:

> file my evening journal

The skill is idempotent, so running it by hand is safe even if the nightly run
already went through.
