# ts — Instant Timestamp Converter

Zero-dependency CLI tool for bidirectional epoch ↔ human-readable timestamp conversion.

## Install

### Option 1: curl (fastest)
```bash
curl -fsSL https://raw.githubusercontent.com/ericjoye/ts-cli/main/ts \
  -o /usr/local/bin/ts && chmod +x /usr/local/bin/ts
```

### Option 2: pip
```bash
pip install ts-cli
```

### Option 3: copy
```bash
cp ts /usr/local/bin/ts && chmod +x /usr/local/bin/ts
```

Requires **Python 3.9+** (uses `zoneinfo` from stdlib). No pip dependencies.

## Usage

```bash
ts                          # Current time: epoch (s/ms/μs) + UTC + local
ts 1718901234               # Epoch seconds → human
ts 1718901234000            # Epoch milliseconds → human (auto-detected)
ts 1718901234000000         # Epoch microseconds → human (auto-detected)
ts "2024-06-20T14:33:54Z"  # ISO 8601 → epoch
ts "2024-06-20 14:33:54"   # Human → epoch
ts now                      # Current epoch in seconds
ts 1718901234 1718902000    # Batch: multiple timestamps
cat timestamps.txt | ts --stdin  # Pipe mode
ts 1718901234 --tz America/New_York  # Convert to timezone
ts 1718901234 --local       # Convert to local timezone
```

## Features

- **Auto-detection**: Distinguishes seconds (≤10 digits), milliseconds (11–13), microseconds (16+)
- **Bidirectional**: Epoch → human AND human → epoch
- **ISO 8601**: Full support for `YYYY-MM-DDTHH:MM:SSZ` and variants
- **Timezone support**: `--tz IANA_NAME` or `--local` for system timezone
- **Batch mode**: Multiple args or `--stdin` pipe
- **Zero dependencies**: Single Python file, stdlib only

## Running tests

```bash
pip install pytest
pytest test_ts.py -v
```

## License

MIT
