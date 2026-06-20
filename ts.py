#!/usr/bin/env python3
"""ts — Instant timestamp converter for developers.

Zero-dependency CLI tool for bidirectional epoch ↔ human-readable
timestamp conversion. Auto-detects seconds, milliseconds, and microseconds.
"""

import argparse
import sys
import time
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


# ---------------------------------------------------------------------------
# Epoch detection helpers
# ---------------------------------------------------------------------------

def detect_epoch_unit(value: int) -> str:
    """Return 's', 'ms', or 'us' based on digit-length heuristics."""
    digits = len(str(abs(value)))
    if digits <= 10:
        return "s"
    elif digits <= 13:
        return "ms"
    else:
        return "us"


def epoch_to_dt(value: int, tz: ZoneInfo | None = None) -> datetime:
    """Convert an epoch value to a timezone-aware datetime (UTC base)."""
    unit = detect_epoch_unit(value)
    if unit == "s":
        dt = datetime.fromtimestamp(value, tz=timezone.utc)
    elif unit == "ms":
        dt = datetime.fromtimestamp(value / 1000, tz=timezone.utc)
    else:
        dt = datetime.fromtimestamp(value / 1_000_000, tz=timezone.utc)
    if tz is not None:
        dt = dt.astimezone(tz)
    return dt


# ---------------------------------------------------------------------------
# Human-readable → epoch parsing
# ---------------------------------------------------------------------------

def parse_human_to_epoch(text: str, tz: ZoneInfo | None = None) -> int:
    """Parse a human-readable datetime string and return epoch seconds.

    Supports: ISO 8601, common date/datetime formats, and the keyword 'now'.
    """
    text = text.strip()

    if text.lower() == "now":
        return int(time.time())

    # Ordered list of formats to try
    formats = [
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%S.%f%z",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M:%S.%f",
        "%Y-%m-%d",
    ]

    dt: datetime | None = None
    for fmt in formats:
        try:
            dt = datetime.strptime(text, fmt)
            break
        except ValueError:
            continue

    if dt is None:
        raise ValueError(f"Cannot parse datetime: {text!r}")

    # If no timezone info, treat as UTC unless --tz / --local was given
    if dt.tzinfo is None:
        if tz is not None:
            dt = dt.replace(tzinfo=tz)
        else:
            dt = dt.replace(tzinfo=timezone.utc)

    return int(dt.timestamp())


# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------

def fmt_utc(dt: datetime) -> str:
    """Return 'YYYY-MM-DD HH:MM:SS UTC'."""
    utc_dt = dt.astimezone(timezone.utc)
    return utc_dt.strftime("%Y-%m-%d %H:%M:%S UTC")


def fmt_tz(dt: datetime) -> str:
    """Return 'YYYY-MM-DD HH:MM:SS <TZ_NAME>'."""
    tzname = dt.tzinfo.tzname(dt) if hasattr(dt.tzinfo, "tzname") else str(dt.tzinfo)
    return dt.strftime(f"%Y-%m-%d %H:%M:%S {tzname}")


# ---------------------------------------------------------------------------
# Core conversion logic
# ---------------------------------------------------------------------------

def convert_one(token: str, tz: ZoneInfo | None = None) -> str:
    """Convert a single token (epoch int or human string) and return a display line."""
    token = token.strip()
    if not token:
        return ""

    # Try integer epoch first
    try:
        value = int(token)
    except ValueError:
        pass
    else:
        unit = detect_epoch_unit(value)
        dt = epoch_to_dt(value, tz=tz)
        if tz is not None:
            return f"{token} → {fmt_tz(dt)}"
        return f"{token} → {fmt_utc(dt)}"

    # Human-readable → epoch
    try:
        epoch_s = parse_human_to_epoch(token, tz=tz)
    except ValueError:
        return f"{token} → ERROR: unrecognised format"

    if tz is not None:
        dt = datetime.fromtimestamp(epoch_s, tz=tz)
        return f"{token} → {epoch_s} ({fmt_tz(dt)})"
    dt = datetime.fromtimestamp(epoch_s, tz=timezone.utc)
    return f"{token} → {epoch_s} ({fmt_utc(dt)})"


def show_current(tz: ZoneInfo | None = None) -> list[str]:
    """Return lines describing the current time."""
    now = time.time()
    epoch_s = int(now)
    epoch_ms = int(now * 1000)
    epoch_us = int(now * 1_000_000)
    lines = [
        f"Epoch s : {epoch_s}",
        f"Epoch ms: {epoch_ms}",
        f"Epoch μs: {epoch_us}",
    ]
    dt_utc = datetime.fromtimestamp(now, tz=timezone.utc)
    lines.append(f"UTC     : {fmt_utc(dt_utc)}")

    if tz is not None:
        dt_tz = datetime.fromtimestamp(now, tz=tz)
        lines.append(f"{tz.key}: {fmt_tz(dt_tz)}")
    else:
        # Show local time
        dt_local = datetime.fromtimestamp(now)
        local_tz = dt_local.astimezone().tzinfo
        local_name = local_tz.tzname(dt_local) if hasattr(local_tz, "tzname") else str(local_tz)
        lines.append(f"Local   : {dt_local.strftime('%Y-%m-%d %H:%M:%S')} {local_name}")

    return lines


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ts",
        description="Instant timestamp converter — epoch ↔ human-readable",
        epilog="Examples:\n  ts\n  ts 1718901234\n  ts 1718901234000 --tz America/New_York\n  ts 2024-06-20T14:33:54Z\n  ts now\n  ts 1718901234 1718902000\n  cat timestamps.txt | ts --stdin\n",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "values",
        nargs="*",
        help="Timestamp(s) to convert: epoch int, ISO date, or 'now'",
    )
    parser.add_argument(
        "--tz",
        metavar="TZ",
        default=None,
        help="Target timezone (e.g. America/New_York, Europe/London)",
    )
    parser.add_argument(
        "--local",
        action="store_true",
        default=False,
        help="Use system local timezone (overrides --tz)",
    )
    parser.add_argument(
        "--stdin",
        action="store_true",
        default=False,
        help="Read timestamps from stdin (one per line)",
    )
    return parser


def resolve_tz(args) -> ZoneInfo | None:
    """Return the ZoneInfo to use, or None for UTC."""
    if args.local:
        # Derive local timezone
        local_dt = datetime.now().astimezone()
        tzinfo = local_dt.tzinfo
        if isinstance(tzinfo, ZoneInfo):
            return tzinfo
        # Fallback: try common resolution via time module
        try:
            local_tz_name = time.tzname[0]
            # Not all names are IANA — best effort
            return ZoneInfo(local_tz_name)
        except (ZoneInfoNotFoundError, Exception):
            # Last resort: fixed offset
            offset = timedelta(seconds=-time.timezone if time.daylight == 0 else -time.altzone)
            # Can't make a ZoneInfo from fixed offset easily; return UTC
            return None
    if args.tz:
        try:
            return ZoneInfo(args.tz)
        except ZoneInfoNotFoundError:
            print(f"ERROR: unknown timezone {args.tz!r}", file=sys.stderr)
            sys.exit(1)
    return None


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    tz = resolve_tz(args)

    # No args → show current time
    if not args.values and not args.stdin:
        for line in show_current(tz):
            print(line)
        return

    # Collect tokens
    tokens: list[str] = []
    if args.stdin:
        for line in sys.stdin:
            stripped = line.strip()
            if stripped:
                tokens.append(stripped)
    tokens.extend(args.values)

    if not tokens:
        parser.print_help()
        sys.exit(1)

    for token in tokens:
        result = convert_one(token, tz=tz)
        if result:
            print(result)


if __name__ == "__main__":
    main()
