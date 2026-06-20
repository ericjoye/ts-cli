# ts-cli — Instant Timestamp Converter

## Title
`ts` — A zero-dependency CLI timestamp converter for developers

## One-liner
Convert Unix timestamps (seconds or milliseconds) to human-readable dates and back — without leaving your terminal.

## Target user
Software developers, DevOps engineers, and SREs who work with logs, databases, JWTs, APIs, and any system that spits out Unix timestamps. They currently Google "epoch converter" or type brittle `date` commands that differ across OSes.

## Problem
Every developer hits this dozens of times a week:
- A log line says `1718901234` — what time was that?
- A JWT exp claim is `1750000000000` — is that in ms or seconds?
- You need the current epoch in milliseconds for an API call.
- You have `2024-06-20T14:00:00Z` and need the epoch.

Current solutions are painful:
- `date -d @1718901234` only works on Linux, not macOS, not Windows/WSL
- `date` doesn't handle milliseconds
- Browser-based converters (epochconverter.com) require context-switching
- Python one-liners require Googling the syntax each time
- No single tool does bidirectional conversion with auto-detection

## MVP Scope (5 features)

1. **Auto-detect and convert epoch → human-readable**
   - `ts 1718894034` → `2024-06-20 14:33:54 UTC`
   - `ts 1718894034000` → auto-detects milliseconds → `2024-06-20 14:33:54 UTC`
   - Supports seconds (10 digits), milliseconds (13 digits), microseconds (16 digits)

2. **Human-readable → epoch**
   - `ts "2024-06-20 14:33:54"` → `1718901234`
   - `ts "2024-06-20T14:33:54Z"` → ISO 8601 input
   - `ts now` → current epoch in seconds

3. **Current time**
   - `ts` (no args) → shows current time in both epoch (s + ms) and human-readable UTC + local

4. **Timezone support**
   - `ts 1718894034 --tz America/New_York` → converts to specified timezone
   - `ts 1718894034 --local` → converts to system local timezone (default: UTC)

5. **Batch mode**
   - `ts 1718894034 1718895000 1718895555` → converts multiple timestamps, one per line
   - Pipe-friendly: `cat timestamps.txt | ts --stdin`

## Tech approach
- **Language**: Python 3.11+ (stdlib only — `datetime`, `argparse`, `time`)
- **Zero external dependencies** — ships as a single file `ts` (or `ts.py`)
- **Single-file CLI** — installable via `curl ... > /usr/local/bin/ts && chmod +x`
- **Timezone support** via `zoneinfo` (Python 3.9+ stdlib) — no `pytz` needed
- **Package**: `pip install ts-cli` (optional) or just copy the single file
- **Tests**: `pytest` with 20+ cases covering edge cases (ms, μs, negative, far future)

## Risks
1. **Competition from shell builtins**: `date -d @X` on Linux is "good enough" for some. Mitigation: our tool handles ms, auto-detection, batch, and cross-platform — `date` doesn't.
2. **Low willingness to pay**: This is a $0–2/mo tool at best. Mitigation: it's a portfolio piece, not a revenue driver. Could be bundled into a "devtools" collection later.
3. **Scope creep**: Tempting to add cron parsing, duration math, etc. Mitigation: MVP is strictly epoch ↔ human. Everything else is v2.

## Definition of done for the MVP
- [ ] Single Python file `ts` works with `python3 ts` or as executable
- [ ] All 5 MVP features work correctly
- [ ] Handles edge cases: ms auto-detection, ISO 8601 input, invalid input with clear errors
- [ ] 20+ pytest tests pass
- [ ] README with install instructions (curl + pip)
- [ ] Published to PyPI as `ts-cli`
