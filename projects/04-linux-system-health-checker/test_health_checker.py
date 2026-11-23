"""Tests for health_checker.py (Linux). Run with: pytest -q"""
import sys

import pytest

import health_checker as hc

pytestmark = pytest.mark.skipif(sys.platform != "linux", reason="reads /proc")


def test_classify():
    assert hc.classify(10, 80, 90) == "OK"
    assert hc.classify(85, 80, 90) == "WARNING"
    assert hc.classify(95, 80, 90) == "CRITICAL"


def test_memory_info_is_sane():
    mem = hc.memory_info()
    assert 0 <= mem["percent"] <= 100
    assert mem["total_gib"] > 0


def test_cpu_percent_range():
    assert 0 <= hc.cpu_percent(interval=0.2) <= 100


def test_quiet_run_exit_code(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(hc, "BASE_DIR", tmp_path)
    code = hc.main(["--quiet", "--interval", "0.1"])
    assert code in (0, 1, 2)
    out = capsys.readouterr().out
    assert any(word in out for word in ("OK", "WARNING", "CRITICAL"))
    assert list((tmp_path / "reports").glob("*.json"))
