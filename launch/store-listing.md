# ts-cli — PyPI Store Listing

## Package Name

`ts-cli`

## Short Description (≤500 chars)

Zero-dependency CLI for bidirectional epoch ↔ human-readable timestamp conversion. Auto-detects seconds, milliseconds, and microseconds. Supports ISO 8601, timezone conversion, batch mode, and stdin pipes. Single Python file, stdlib only, Python 3.9+.

## Long Description

`ts` is a developer CLI tool that solves the daily annoyance of converting Unix timestamps. Every developer hits this dozens of times a week — a log line says `1718901234`, a JWT exp claim is `1750000000000`, or you need the current epoch for an API call.

**Why `ts` instead of `date` or a browser?**

- `date -d @X` only works on Linux, doesn't handle milliseconds, and differs across OSes
- Browser converters (epochconverter.com) require context-switching
- Python one-liners require Googling the syntax each time
- No single tool does bidirectional conversion with auto-detection

**Features:**

- **Auto-detection**: Distinguishes seconds (≤10 digits), milliseconds (11–13), microseconds (16+)
- **Bidirectional**: Epoch → human AND human → epoch
- **ISO 8601**: Full support for `YYYY-MM-DDTHH:MM:SSZ` and variants
- **Timezone support**: `--tz IANA_NAME` or `--local` for system timezone
- **Batch mode**: Multiple args or `--stdin` pipe for processing files
- **Zero dependencies**: Single Python file, stdlib only (argparse, datetime, zoneinfo, time)
- **Cross-platform**: Linux, macOS, Windows/WSL — anywhere Python 3.9+ runs

**Install:**

```bash
pip install ts-cli
```

Or without pip:

```bash
curl -fsSL https://raw.githubusercontent.com/ericjoye/ts-cli/main/ts \
  -o /usr/local/bin/ts && chmod +x /usr/local/bin/ts
```

**Usage:**

```bash
ts                          # Current time
ts 1718901234               # Epoch → human
ts 1718901234000            # Milliseconds auto-detected
ts "2024-06-20T14:33:54Z"  # ISO 8601 → epoch
ts now                      # Current epoch
ts 1718901234 --tz America/New_York
cat timestamps.txt | ts --stdin
```

40/40 tests pass. MIT licensed.

## Keywords

timestamp, epoch, unix timestamp, epoch converter, time converter, cli, developer tools, devtools, datetime, iso 8601, timezone, batch, pipe, python cli, zero dependency, cross platform

## Classifiers

- Programming Language :: Python :: 3
- License :: OSI Approved :: MIT License
- Operating System :: OS Independent
- Topic :: Utilities
- Topic :: Software Development :: Libraries
- Environment :: Console

## Project Links

- Homepage: https://github.com/ericjoye/ts-cli
- Repository: https://github.com/ericjoye/ts-cli
- Issues: https://github.com/ericjoye/ts-cli/issues
