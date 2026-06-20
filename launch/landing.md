# ts — Landing Page Copy

## Headline

**Stop Googling "epoch converter." Just type `ts`.**

## Subhead

A zero-dependency CLI tool that converts Unix timestamps to human-readable dates — and back — in milliseconds. No browser tabs. No context-switching. No dependencies.

## Benefits

- **Instant & automatic** — Paste any timestamp (seconds, milliseconds, or microseconds) and `ts` auto-detects the format. No flags, no guessing. Just `ts 1718901234000` → `2024-06-20 14:33:54 UTC`.

- **Bidirectional & timezone-aware** — Convert epoch → human OR human → epoch. Add `--tz America/New_York` or `--local` for timezone conversion. Pipe-friendly for batch processing logs.

- **Zero dependencies, single file** — One Python file, stdlib only. Install via `curl`, `pip install ts-cli`, or copy. Works on any system with Python 3.9+. No pip installs, no virtualenv, no fuss.

## CTA

```bash
pip install ts-cli
```

Or try it right now:

```bash
curl -fsSL https://raw.githubusercontent.com/ericjoye/ts-cli/main/ts -o /usr/local/bin/ts && chmod +x /usr/local/bin/ts
```

Then: `ts 1718901234`

---

*40/40 tests pass. Zero dependencies. MIT licensed.*
