#!/usr/bin/env python3
import argparse
import datetime
import hashlib
import hmac
import json
import os
import pathlib
import re
import sqlite3
import uuid
from typing import Any, Dict

import yaml
from jsonschema import Draft202012Validator

VERSION = "p1.0.0"

AUTH_FAIL_RE = re.compile(
    r"Failed password for\s+(?P<user>\S+)\s+from\s+(?P<ip>\d+\.\d+\.\d+\.\d+)"
)
AUTH_OK_RE = re.compile(
    r"Accepted password for\s+(?P<user>\S+)\s+from\s+(?P<ip>\d+\.\d+\.\d+\.\d+)"
)
INVALID_USER_RE = re.compile(r"Invalid user\s+(?P<user>\S+)\s+from\s+(?P<ip>\d+\.\d+\.\d+\.\d+)")

LOCAL_PREFIXES = ("127.", "10.", "192.168.", "172.16.")


def load_config(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        data: Dict[str, Any] = yaml.safe_load(f) or {}
    return data


def ensure_secret(secret_file: str) -> bytes:
    p = pathlib.Path(secret_file)
    if not p.exists():
        p.parent.mkdir(parents=True, exist_ok=True)
        s = os.urandom(32)
        p.write_bytes(s)
        return s
    return p.read_bytes()


def provenance_sign(secret: bytes, payload: bytes) -> str:
    return hmac.new(secret, payload, hashlib.sha256).hexdigest()


def classify(parsed: dict) -> str:
    ip = parsed.get("ip", "")
    is_local = ip.startswith(LOCAL_PREFIXES)
    if parsed.get("action") == "auth_fail" and not is_local:
        return "PvP"
    if (
        "bot" in parsed.get("raw_line", "").lower()
        or "crawler" in parsed.get("raw_line", "").lower()
    ):
        return "PvE"
    if parsed.get("action") in ("auth_ok", "invalid_user"):
        return "PvE"
    return "Unknown"


def parse_line(line: str) -> dict:
    parsed = {"raw_line": line.strip()}
    if m := AUTH_FAIL_RE.search(line):
        parsed.update({"user": m.group("user"), "ip": m.group("ip"), "action": "auth_fail"})
    elif m := AUTH_OK_RE.search(line):
        parsed.update({"user": m.group("user"), "ip": m.group("ip"), "action": "auth_ok"})
    elif m := INVALID_USER_RE.search(line):
        parsed.update({"user": m.group("user"), "ip": m.group("ip"), "action": "invalid_user"})
    else:
        parsed.update({"action": "unknown"})
    return parsed


def init_sqlite(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS events(
        event_id TEXT PRIMARY KEY,
        ts_utc TEXT NOT NULL,
        host TEXT, sensor TEXT, decoy INTEGER,
        raw_line TEXT, parsed_json TEXT,
        pvx TEXT, chimera INTEGER,
        sha256 TEXT, signature TEXT,
        classifier_ver TEXT
    );""")
    c.execute("""CREATE TABLE IF NOT EXISTS anomalies(
        anomaly_id TEXT PRIMARY KEY,
        ts_utc TEXT NOT NULL,
        seed_ids TEXT,
        sketch TEXT, similarity REAL,
        complexity_hint TEXT,
        sha256 TEXT, signature TEXT
    );""")
    conn.commit()
    return conn


def load_schema(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        data: Dict[str, Any] = json.load(f)
    return data


def write_jsonl(path: str, obj: dict):
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="Path to auth.log or similar")
    ap.add_argument("--config", required=True, help="Path to process.yaml")
    args = ap.parse_args()

    cfg = load_config(args.config)
    event_schema = load_schema(cfg["schema"]["event"])
    anomaly_schema = load_schema(cfg["schema"]["anomaly"])

    secret = ensure_secret(cfg["provenance"]["secret_file"])

    events_jsonl = cfg["storage"]["events_jsonl"]
    anomalies_jsonl = cfg["storage"]["anomalies_jsonl"]
    db_path = cfg["storage"]["sqlite_db"]
    pathlib.Path(events_jsonl).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(anomalies_jsonl).parent.mkdir(parents=True, exist_ok=True)

    conn = init_sqlite(db_path)
    cur = conn.cursor()

    host = "vps01"
    sensor = "sshd"
    decoy = False

    with open(args.input, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            parsed = parse_line(line)
            pvx = classify(parsed)
            ts = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
            event_id = str(uuid.uuid4())
            core = {
                "event_id": event_id,
                "ts_utc": ts,
                "source": {"host": host, "sensor": sensor, "decoy": decoy},
                "raw": {},
                "parsed": parsed,
                "labels": {"pvx": pvx, "att&ck": [], "chimera": False},
                "fri_delta": None,
                "provenance": {
                    "sha256": hashlib.sha256(parsed["raw_line"].encode("utf-8")).hexdigest(),
                    "signature": "",
                    "sbom_ref": "ops/sbom.spdx.json",
                    "attestation": "ops/attestation.json",
                },
                "classifier_ver": VERSION,
                "reclass_history": [],
            }
            payload = json.dumps(
                {"event_id": event_id, "ts": ts, "pvx": pvx, "raw": parsed.get("raw_line", "")},
                sort_keys=True,
            ).encode("utf-8")
            core["provenance"]["signature"] = provenance_sign(secret, payload)

            Draft202012Validator(event_schema).validate(core)

            write_jsonl(events_jsonl, core)
            cur.execute(
                "INSERT INTO events VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                (
                    core["event_id"],
                    core["ts_utc"],
                    host,
                    sensor,
                    int(decoy),
                    parsed.get("raw_line", ""),
                    json.dumps(parsed),
                    pvx,
                    0,
                    core["provenance"]["sha256"],
                    core["provenance"]["signature"],
                    VERSION,
                ),
            )

            if pvx == "Unknown":
                anomaly_id = str(uuid.uuid4())
                sketch = hashlib.sha256(parsed.get("raw_line", "").encode("utf-8")).hexdigest()[:16]
                anomaly = {
                    "anomaly_id": anomaly_id,
                    "ts_utc": ts,
                    "seed_event_ids": [event_id],
                    "signature": {"sketch": sketch, "similarity": 0.0},
                    "complexity_hint": "NP-like",
                    "dictionary_matches": [],
                    "decision": None,
                    "provenance": {
                        "sha256": hashlib.sha256(sketch.encode("utf-8")).hexdigest(),
                        "signature": provenance_sign(secret, sketch.encode("utf-8")),
                    },
                    "notes": None,
                }
                Draft202012Validator(anomaly_schema).validate(anomaly)
                write_jsonl(anomalies_jsonl, anomaly)
                cur.execute(
                    "INSERT INTO anomalies VALUES (?,?,?,?,?,?,?,?)",
                    (
                        anomaly_id,
                        ts,
                        json.dumps([event_id]),
                        sketch,
                        0.0,
                        "NP-like",
                        anomaly["provenance"]["sha256"],
                        anomaly["provenance"]["signature"],
                    ),
                )

    conn.commit()
    conn.close()
    print(f"Ingest complete. JSONL at {events_jsonl} / {anomalies_jsonl}; DB at {db_path}")


if __name__ == "__main__":
    main()
