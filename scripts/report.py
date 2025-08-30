#!/usr/bin/env python3
import argparse
import json
import pathlib
import sqlite3
import time
from typing import Any, Dict

import yaml


def load_config(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        data: Dict[str, Any] = yaml.safe_load(f) or {}
    return data


def counts(db_path: str):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT pvx, COUNT(*) FROM events GROUP BY pvx")
    pvx = {row[0]: row[1] for row in c.fetchall()}
    c.execute("SELECT COUNT(*) FROM anomalies")
    anomalies = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM events")
    total = c.fetchone()[0]
    conn.close()
    return total, pvx, anomalies


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    args = ap.parse_args()
    cfg = load_config(args.config)
    db = cfg["storage"]["sqlite_db"]
    total, pvx, anomalies = counts(db)
    fri = (
        json.loads(pathlib.Path("data/processed/fri.json").read_text())
        if pathlib.Path("data/processed/fri.json").exists()
        else {"fri_score": None, "band": "unknown"}
    )
    ts = time.strftime("%Y-%m-%d_%H%M%S", time.gmtime())
    out_dir = pathlib.Path(cfg["report"]["out_dir"])
    out_dir.mkdir(parents=True, exist_ok=True)
    md_path = out_dir / f"report_{ts}.md"
    md = [
        f"# SWARMINT-AUTOPOIESIS · Bronze Report ({ts} UTC)",
        "",
        f"- Total events: **{total}**",
        f"- PvP: **{pvx.get('PvP',0)}**, PvE: **{pvx.get('PvE',0)}**, Unknown: **{pvx.get('Unknown',0)}**",
        f"- Anomalies: **{anomalies}**",
        f"- FRI: **{fri['fri_score']}** · Band: **{fri['band']}**",
        "",
        "Artifacts:",
        "- events.jsonl / anomalies.jsonl in `data/processed/`",
        f"- SQLite catalog at `{cfg['storage']['sqlite_db']}`",
        "",
    ]
    md_path.write_text("\n".join(md))

    run_record = {
        "ts_utc": ts,
        "inputs": {"config": args.config},
        "artifacts": {
            "events_jsonl": cfg["storage"]["events_jsonl"],
            "anomalies_jsonl": cfg["storage"]["anomalies_jsonl"],
            "sqlite_db": cfg["storage"]["sqlite_db"],
            "fri_json": "data/processed/fri.json",
            "report_md": str(md_path),
        },
        "policy": {"gate": "BRONZE", "version": "1.0"},
    }
    pathlib.Path(cfg["run_record"]["path"]).write_text(json.dumps(run_record, indent=2))
    print(f"Wrote report to {md_path} and run-record to {cfg['run_record']['path']}")


if __name__ == "__main__":
    main()
