"""Tests for the training pipeline."""
import copy

import pandas as pd
import pytest

import train


@pytest.fixture
def config():
    return train.load_config(train.HERE / "config.yaml")


def test_config_is_valid(config):
    assert config["model"]["type"] in train.MODELS
    assert 0 < config["decision"]["threshold"] < 1


def test_data_validation_detects_bad_values(tmp_path, config, monkeypatch):
    bad = pd.read_csv(train.HERE / config["data"]["path"])
    bad.loc[0, "cpu_usage"] = 250
    (tmp_path / "data").mkdir()
    bad.to_csv(tmp_path / "data" / "bad.csv", index=False)
    monkeypatch.setattr(train, "HERE", tmp_path)
    cfg = copy.deepcopy(config)
    cfg["data"]["path"] = "data/bad.csv"
    with pytest.raises(train.DataValidationError):
        train.load_data(cfg)


def test_model_meets_quality_gate(config):
    bundle = train.train(config)
    assert train.passes_gate(bundle["metrics"], config["quality_gate"]) == []


def test_gate_reports_failures():
    failures = train.passes_gate({"recall": 0.5, "roc_auc": 0.95}, {"min_recall": 0.8, "min_roc_auc": 0.9})
    assert failures == ["recall 0.5 < 0.8"]
