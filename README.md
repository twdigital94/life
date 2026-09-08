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
