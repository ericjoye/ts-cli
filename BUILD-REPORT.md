# BUILD-REPORT: ts-cli

## What was built

`ts` — a zero-dependency CLI timestamp converter for developers. Single Python 3.11+ file, stdlib only.

## File layout

```
~/businesses/ts-cli/
├── ts              # Main CLI script (executable, single file)
├── test_ts.py      # 40 pytest tests
├── pyproject.toml  # PyPI packaging config (project name: ts-cli)
├── README.md       # Install instructions + usage
├── BRIEF.md        # Product brief (epoch examples corrected)
└── BUILD-REPORT.md # This file
```

## How to run

```bash
# Direct execution
python3 ts                    # Current time
python3 ts 1718894034         # Epoch → human
python3 ts 1718894034000      # Epoch ms → human (auto-detected)
python3 ts "2024-06-20T14:33:54Z"  # Human → epoch
python3 ts now                # Current epoch
python3 ts 1718894034 --tz America/New_York  # Timezone
python3 ts 1718894034 --local              # Local timezone
python3 ts 1718894034 1718895000           # Batch
echo "1718894034" | python3 ts --stdin      # Pipe mode

# Make executable
chmod +x ts && ./ts

# Tests
pip install pytest && pytest test_ts.py -v   # 40 tests pass
```

## What works

All 5 MVP features:
1. **Epoch → human** with auto-detection of seconds (≤10 digits), milliseconds (11-13), microseconds (16+)
2. **Human → epoch** supporting ISO 8601 (`YYYY-MM-DDTHH:MM:SSZ`), `YYYY-MM-DD HH:MM:SS`, `YYYY-MM-DD`, and `now`
3. **Current time** (`ts` with no args) shows epoch s/ms/μs, UTC, and local time
4. **Timezone support** via `--tz IANA_NAME` (uses `zoneinfo` stdlib) and `--local` for system timezone
5. **Batch mode** via multiple args or `--stdin` pipe

## Test results

40/40 pytest tests pass covering:
- Unit tests: `detect_epoch_unit` (8), `epoch_to_dt` (5), `parse_human_to_epoch` (5), `convert_one` (6), `show_current` (2)
- Integration tests: CLI subprocess (14) including no-args, epoch, ms, μs, human→epoch, now, batch, --tz, --local, --stdin, invalid input, zero epoch, bad timezone

## Known gaps / v2 ideas

- No PyPI publish done yet (requires `twine` + PyPI credentials) — `pyproject.toml` is ready
- No shell completion (bash/zsh/fish)
- No duration math (e.g., "2h30m from now")
- No cron expression parsing
- `--local` timezone detection falls back to UTC on systems where IANA name can't be resolved from `time.tzname`
- The script is named `ts.py` in the repo; for PyPI install the entry point maps `ts` → `ts:main`

## Decisions

- **Epoch auto-detection by digit count**: Simple heuristic — ≤10 digits = seconds, 11-13 = ms, 16+ = μs. Covers all real-world timestamps (epoch seconds won't hit 11 digits until 2286).
- **UTC default**: All conversions default to UTC unless `--tz` or `--local` is specified.
- **zoneinfo over pytz**: Python 3.9+ stdlib `zoneinfo` provides IANA timezone support with zero dependencies.
- **Single file**: Ships as one `ts.py` file for easy `curl` install; `pyproject.toml` wraps it for PyPI.
