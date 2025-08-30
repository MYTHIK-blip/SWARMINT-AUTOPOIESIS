#!/usr/bin/env python3
import argparse
import json
import pathlib
import sqlite3
from typing import Any, Dict

import yaml


def load_config(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        data: Dict[str, Any] = yaml.safe_load(f) or {}
    return data


def compute_fri(db_path: str, weights: Dict[str, float]) -> float:
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM events WHERE pvx='PvP'")
    pvp: int = int(c.fetchone()[0])
    c.execute("SELECT COUNT(*) FROM anomalies")
    anoms: int = int(c.fetchone()[0])
    conn.close()
    score: float = pvp * float(weights.get("auth_fail", 1.0)) + anoms * float(
        weights.get("anomaly", 2.0)
    )
    return score


def band(score: float, bands: dict) -> str:
    if score <= bands.get("green_max", 3):
        return "green"
    if score <= bands.get("amber_max", 6):
        return "amber"
    return "red"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    args = ap.parse_args()
    cfg = load_config(args.config)
    db = cfg["storage"]["sqlite_db"]
    score = compute_fri(db, cfg["fri"]["weights"])
    b = band(score, cfg["fri"]["bands"])
    out = {"fri_score": score, "band": b}
    pathlib.Path("data/processed/fri.json").write_text(json.dumps(out))
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
