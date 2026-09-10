# Working with Tim

## Explaining problems

When something breaks, explain it in plain English. Tim asked for this
specifically, after a debugging explanation that was accurate but hard to follow.

**Do this:**

- Lead with what actually went wrong, in one sentence a non-engineer would get.
- Say what it means for him, not what the code does.
- Use everyday words. "Otter's search by name is slow to update" beats "the
  title index has replication lag".
- Keep it short. A few short paragraphs, not a report.
- If there were two causes, separate them clearly and plainly.
- Own the mistake plainly when it was mine. No hedging, no padding.

**Not this:**

- Tool names, parameter names, field names, status codes, timestamps in UTC, or
  log output, unless he asks to see the detail.
- Tables of technical findings when a sentence would do.
- Narrating the investigation step by step. Give him the conclusion.
- Softening it so much that the actual problem gets lost.

The test: could he repeat the explanation to someone else an hour later? If not,
it is too complicated.

He is technical enough to follow detail when he wants it, so offer it rather than
withholding it. Just do not lead with it.

## Automations in this repo

Anything running unattended reports back to him the same way: short, plain, and
clear about whether it did something, did nothing, or broke. He reads these when
he wakes up, so a wall of detail is worse than useless.
