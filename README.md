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
| Logic | [`.claude/skills/evening-journal/SKILL.md`](.claude/skills/evening-journal/SKILL.md) |
| Dates | [`scripts/journal_dates.py`](scripts/journal_dates.py) |
| Ledger | [`state/evening-journal.json`](state/evening-journal.json) |

### Setup, one manual step

The Routine needs the **Notion** and **Otter_ai** connectors attached to it.
They cannot be attached programmatically on this account, so add them once in
the Routines UI on claude.ai (open *Evening journal to Notion*, add the two
connectors). Without them the nightly session has no Notion or Otter tools and
the run fails. Nothing is lost when it does, the recordings stay in Otter and
the next good run picks them up.

### Finding the recording

Otter only uses the title "Evening journal" if Tim renamed it. When he doesn't,
Otter invents its own title, and a title-only search reports "nothing to file"
on a night he actually recorded. That happened on 8 September.

So every run does two passes: one by title, one by **shape** (starts 18:00 to
04:00 local, runs 3 to 40 minutes), then confirms from the transcript that it is
Tim alone reflecting rather than a client call. Renaming the recording in Otter
is still the most reliable path, but forgetting no longer costs an entry.

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
