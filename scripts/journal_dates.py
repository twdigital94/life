#!/usr/bin/env python3
"""Date helpers for the evening-journal automation.

Otter reports recording times in US Pacific. Tim lives somewhere else. This
works out which calendar day an evening recording actually belongs to, and
formats the heading used in the Notion journal.

Change HOME_TZ when Tim moves. Nothing else needs touching.

Usage:
    python3 scripts/journal_dates.py now
    python3 scripts/journal_dates.py heading "2026/09/07 06:24:53"
"""

import sys
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

HOME_TZ = ZoneInfo("Asia/Bangkok")   # Tim's current base. Update when he moves.
OTTER_TZ = ZoneInfo("America/Los_Angeles")  # What Otter reports times in.

LOOKBACK_DAYS = 4        # How far back each run checks, to catch late/missed nights.
EVENING_ROLLBACK_HOUR = 4  # A recording before this hour belongs to the previous evening.


def parse_otter(stamp: str) -> datetime:
    """Turn an Otter 'YYYY/MM/DD HH:MM:SS' string into a home-timezone datetime."""
    naive = datetime.strptime(stamp.strip(), "%Y/%m/%d %H:%M:%S")
    return naive.replace(tzinfo=OTTER_TZ).astimezone(HOME_TZ)


def journal_day(local: datetime):
    """The day an evening recording belongs to.

    Recording at 20:24 on the 7th belongs to the 7th. Recording at 00:40 on the
    8th is still the evening of the 7th, so roll it back.
    """
    return (local - timedelta(days=1)).date() if local.hour < EVENING_ROLLBACK_HOUR else local.date()


def heading(day) -> str:
    """The Notion heading, matching the page's existing style: **Evening, Monday 7 September**"""
    return f"**Evening, {day.strftime('%A')} {day.day} {day.strftime('%B')}**"


def cmd_now():
    local = datetime.now(HOME_TZ)
    # Otter filters on its own Pacific dates, so give the window in those terms.
    end_pt = local.astimezone(OTTER_TZ)
    start_pt = end_pt - timedelta(days=LOOKBACK_DAYS)
    print(f"local_now        {local:%Y-%m-%d %H:%M:%S %Z}")
    print(f"local_today      {local:%Y-%m-%d} ({local:%A})")
    print(f"otter_created_after   {start_pt:%Y/%m/%d}")
    print(f"otter_created_before  {end_pt:%Y/%m/%d}")
    print(f"year             {local.year}")


def cmd_heading(stamp: str):
    local = parse_otter(stamp)
    day = journal_day(local)
    print(f"recorded_local   {local:%Y-%m-%d %H:%M:%S %Z}")
    print(f"journal_day      {day:%Y-%m-%d}")
    print(f"year             {day.year}")
    print(f"heading          {heading(day)}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    if sys.argv[1] == "now":
        cmd_now()
    elif sys.argv[1] == "heading" and len(sys.argv) > 2:
        cmd_heading(sys.argv[2])
    else:
        sys.exit(__doc__)
