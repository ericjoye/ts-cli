"""Tests for ts — timestamp converter."""

import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest

# Import functions directly from the module under test
sys.path.insert(0, str(Path(__file__).parent))
from ts import (
    detect_epoch_unit,
    epoch_to_dt,
    parse_human_to_epoch,
    convert_one,
    show_current,
    resolve_tz,
    build_parser,
)

TS_PATH = str(Path(__file__).parent / "ts.py")

# Correct epoch for 2024-06-20 14:33:54 UTC
KNOWN_EPOCH = 1718894034
KNOWN_DATE = "2024-06-20 14:33:54 UTC"


# ---------------------------------------------------------------------------
# detect_epoch_unit
# ---------------------------------------------------------------------------

class TestDetectEpochUnit:
    def test_seconds(self):
        assert detect_epoch_unit(KNOWN_EPOCH) == "s"

    def test_seconds_small(self):
        assert detect_epoch_unit(0) == "s"

    def test_seconds_10_digits(self):
        assert detect_epoch_unit(9999999999) == "s"

    def test_milliseconds(self):
        assert detect_epoch_unit(KNOWN_EPOCH * 1000) == "ms"

    def test_milliseconds_13_digits(self):
        assert detect_epoch_unit(9999999999999) == "ms"

    def test_microseconds(self):
        assert detect_epoch_unit(KNOWN_EPOCH * 1_000_000) == "us"

    def test_microseconds_16_digits(self):
        assert detect_epoch_unit(9999999999999999) == "us"

    def test_negative_seconds(self):
        assert detect_epoch_unit(-KNOWN_EPOCH) == "s"


# ---------------------------------------------------------------------------
# epoch_to_dt
# ---------------------------------------------------------------------------

class TestEpochToDt:
    def test_known_epoch(self):
        dt = epoch_to_dt(KNOWN_EPOCH)
        assert dt.year == 2024
        assert dt.month == 6
        assert dt.day == 20
        assert dt.hour == 14
        assert dt.minute == 33
        assert dt.second == 54

    def test_zero_epoch(self):
        dt = epoch_to_dt(0)
        assert dt.year == 1970
        assert dt.month == 1
        assert dt.day == 1

    def test_milliseconds(self):
        dt = epoch_to_dt(KNOWN_EPOCH * 1000)
        assert dt.year == 2024
        assert dt.month == 6
        assert dt.day == 20

    def test_microseconds(self):
        dt = epoch_to_dt(KNOWN_EPOCH * 1_000_000)
        assert dt.year == 2024
        assert dt.month == 6
        assert dt.day == 20

    def test_with_timezone(self):
        tz = ZoneInfo("America/New_York")
        dt = epoch_to_dt(KNOWN_EPOCH, tz=tz)
        assert dt.tzinfo is not None
        # 2024-06-20 14:33:54 UTC = 10:33:54 EDT (UTC-4 in summer)
        assert dt.hour == 10


# ---------------------------------------------------------------------------
# parse_human_to_epoch
# ---------------------------------------------------------------------------

class TestParseHumanToEpoch:
    def test_iso_with_z(self):
        epoch = parse_human_to_epoch("2024-06-20T14:33:54Z")
        assert epoch == KNOWN_EPOCH

    def test_iso_with_t(self):
        epoch = parse_human_to_epoch("2024-06-20 14:33:54")
        assert epoch == KNOWN_EPOCH

    def test_date_only(self):
        epoch = parse_human_to_epoch("2024-06-20")
        dt = datetime(2024, 6, 20, tzinfo=timezone.utc)
        assert epoch == int(dt.timestamp())

    def test_now(self):
        before = int(time.time())
        epoch = parse_human_to_epoch("now")
        after = int(time.time())
        assert before <= epoch <= after

    def test_invalid_raises(self):
        with pytest.raises(ValueError):
            parse_human_to_epoch("not-a-date")


# ---------------------------------------------------------------------------
# convert_one
# ---------------------------------------------------------------------------

class TestConvertOne:
    def test_epoch_to_human(self):
        result = convert_one(str(KNOWN_EPOCH))
        assert KNOWN_DATE in result

    def test_epoch_ms_to_human(self):
        result = convert_one(str(KNOWN_EPOCH * 1000))
        assert KNOWN_DATE in result

    def test_human_to_epoch(self):
        result = convert_one("2024-06-20T14:33:54Z")
        assert str(KNOWN_EPOCH) in result

    def test_now_keyword(self):
        result = convert_one("now")
        assert "→" in result

    def test_invalid_input(self):
        result = convert_one("garbage")
        assert "ERROR" in result

    def test_with_timezone(self):
        tz = ZoneInfo("America/New_York")
        result = convert_one(str(KNOWN_EPOCH), tz=tz)
        assert "America/New_York" in result or "EDT" in result or "EST" in result


# ---------------------------------------------------------------------------
# show_current
# ---------------------------------------------------------------------------

class TestShowCurrent:
    def test_no_args_returns_list(self):
        lines = show_current()
        assert len(lines) >= 3
        assert any("Epoch s" in l for l in lines)
        assert any("Epoch ms" in l for l in lines)
        assert any("UTC" in l for l in lines)

    def test_with_timezone(self):
        tz = ZoneInfo("UTC")
        lines = show_current(tz=tz)
        assert any("UTC" in l for l in lines)


# ---------------------------------------------------------------------------
# CLI integration tests
# ---------------------------------------------------------------------------

class TestCLI:
    def _run(self, *args):
        """Run the ts CLI and return (stdout, stderr, returncode)."""
        result = subprocess.run(
            [sys.executable, TS_PATH, *args],
            capture_output=True,
            text=True,
        )
        return result.stdout.strip(), result.stderr.strip(), result.returncode

    def test_no_args_shows_current(self):
        out, err, rc = self._run()
        assert rc == 0
        assert "Epoch s" in out
        assert "UTC" in out

    def test_epoch_arg(self):
        out, err, rc = self._run(str(KNOWN_EPOCH))
        assert rc == 0
        assert KNOWN_DATE in out

    def test_epoch_ms_arg(self):
        out, err, rc = self._run(str(KNOWN_EPOCH * 1000))
        assert rc == 0
        assert KNOWN_DATE in out

    def test_human_to_epoch(self):
        out, err, rc = self._run("2024-06-20T14:33:54Z")
        assert rc == 0
        assert str(KNOWN_EPOCH) in out

    def test_now(self):
        out, err, rc = self._run("now")
        assert rc == 0
        # Output is like "now → 1781950215 (2026-06-20 ...)"
        assert "→" in out
        # Extract the epoch number
        parts = out.split("→")[1].strip().split()
        epoch_str = parts[0]
        epoch_val = int(epoch_str)
        assert 1_700_000_000 < epoch_val < 2_000_000_000

    def test_multiple_args(self):
        out, err, rc = self._run(str(KNOWN_EPOCH), str(KNOWN_EPOCH + 1000))
        assert rc == 0
        lines = out.splitlines()
        assert len(lines) == 2

    def test_timezone_flag(self):
        out, err, rc = self._run(str(KNOWN_EPOCH), "--tz", "America/New_York")
        assert rc == 0
        assert "2024-06-20" in out

    def test_local_flag(self):
        out, err, rc = self._run(str(KNOWN_EPOCH), "--local")
        assert rc == 0

    def test_stdin_mode(self):
        inp = f"{KNOWN_EPOCH}\n{KNOWN_EPOCH + 1000}\n"
        result = subprocess.run(
            [sys.executable, TS_PATH, "--stdin"],
            input=inp,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        lines = result.stdout.strip().splitlines()
        assert len(lines) == 2

    def test_invalid_epoch(self):
        out, err, rc = self._run("garbage")
        assert rc == 0  # doesn't crash, shows error in output
        assert "ERROR" in out

    def test_zero_epoch(self):
        out, err, rc = self._run("0")
        assert rc == 0
        assert "1970-01-01 00:00:00 UTC" in out

    def test_microseconds(self):
        out, err, rc = self._run(str(KNOWN_EPOCH * 1_000_000))
        assert rc == 0
        assert KNOWN_DATE in out

    def test_date_only_input(self):
        out, err, rc = self._run("2024-06-20")
        assert rc == 0
        expected_epoch = str(int(datetime(2024, 6, 20, tzinfo=timezone.utc).timestamp()))
        assert expected_epoch in out

    def test_bad_timezone_exits(self):
        out, err, rc = self._run(str(KNOWN_EPOCH), "--tz", "Mars/Phobos")
        assert rc == 1
        assert "ERROR" in err
