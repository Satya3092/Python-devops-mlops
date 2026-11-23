"""Tests for log_analyzer.py - run with: pytest -q"""
import pytest

from log_analyzer import LogParseError, analyse, main, normalise, parse_line


def test_parse_valid_line():
    entry = parse_line("2026-11-20 10:00:01 ERROR Database timeout after 5000ms")
    assert entry["level"] == "ERROR"
    assert entry["message"] == "Database timeout after 5000ms"


@pytest.mark.parametrize("line", ["garbage", "2026-11-20 10:00:01 DEBUG not counted", ""])
def test_parse_invalid_line(line):
    with pytest.raises(LogParseError):
        parse_line(line)


def test_normalise_groups_numbers_and_ips():
    assert normalise("[10.0.0.5] timeout after 2418ms") == "timeout after <N>ms"


def test_sample_folder_counts():
    report = analyse(["sample_logs"])
    assert report["totals"] == {"INFO": 7, "WARNING": 3, "ERROR": 4}
    assert report["bad_lines"] == 1


def test_fail_on_errors_exit_code(capsys):
    assert main(["sample_logs", "--fail-on-errors", "3"]) == 1
    assert main(["sample_logs", "--fail-on-errors", "100"]) == 0


def test_missing_path_returns_2():
    assert main(["does-not-exist"]) == 2
