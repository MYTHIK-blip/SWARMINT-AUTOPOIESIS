# SWARMINT-AUTOPOIESIS  
**Provenance-first, homeostatic SIEM embryo** · *Bronze Gate*

[![Status](https://img.shields.io/badge/gate-🟤_Bronze-v0.1)](#status)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](#quickstart)
[![License](https://img.shields.io/badge/license-MIT-lightgrey)](#license)

A minimal yet complete telemetry refinery that ingests `auth.log`, classifies events (PvP/PvE/Unknown), signs them with HMAC provenance, detects anomalies, computes **FRI (Fracture Readiness Index)**, and emits JSONL/SQLite + Markdown reports. Designed for **clear rollbacks, promotion gates, and supply-chain hygiene**.

---

## TL;DR (Bronze)
- **Gate:** `bronze-gate-v0.1` (tag) · **Branch:** `bronze` (immutable rollback)  
- **You can:** clone `--branch bronze`, or rehydrate from the **release tarball** + `SHA256SUMS.txt`  
- Pipeline: ingest → classify → **prove** → store → anomaly → **FRI** → report

---

## Table of Contents
- [Status](#status)
- [Quickstart](#quickstart)
- [Architecture](#architecture)
- [Data & Artifacts](#data--artifacts)
- [Security & Provenance](#security--provenance)
- [Rollback & DR](#rollback--dr)
- [Promotion Gates & Roadmap](#promotion-gates--roadmap)
- [Repo Layout](#repo-layout)
- [Configuration](#configuration)
- [Scripts](#scripts)
- [Quality Gates (CI/Pre-commit)](#quality-gates-ci-pre-commit)
- [Contributing](#contributing)
- [License](#license)

---

## Status
- **Latest Release:** 🟤 **Bronze Gate v0.1** — SIEM embryo  
- **Channels:**  
  - Tag: `bronze-gate-v0.1`  
  - Branch: `bronze` (protected, immutable rollback)  
  - Default dev branch: `main` (evolves toward Silver)

> **Industry alignment:** Release tag + protected rollback branch + release artifacts with checksums mirrors standard enterprise DR and change-control practice.

---

## Quickstart

### Requirements
- Linux/macOS (WSL2 OK)
- Python **3.11+**
- `git`, `make` (optional)

### Install & Smoke Run
```bash
git clone git@github.com:MYTHIK-blip/SWARMINT-AUTOPOIESIS.git
cd SWARMINT-AUTOPOIESIS
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# (if present) pip install -r ops/requirements.lock.txt

# Place or symlink a sample auth log:
#   cp /var/log/auth.log data/raw/auth.log
# Or generate via scripts/sample_data.py

bash scripts/run_embryo.sh
# Outputs -> data/processed/*.jsonl, catalog.db, fri.json, and data/reports/report_*.md
<details><summary>Air-gap rehydrate (no git history)</summary>
Download SWARMINT-AUTOPOIESIS_bronze-gate-v0.1_src.tar.gz and SHA256SUMS.txt from the Release page.

Verify and extract:

bash
Copy code
sha256sum -c SHA256SUMS.txt
tar -xzf SWARMINT-AUTOPOIESIS_bronze-gate-v0.1_src.tar.gz
cd SWARMINT-AUTOPOIESIS && python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
bash scripts/run_embryo.sh
</details>
Architecture
mermaid
Copy code
flowchart LR
  A[auth.log] --> B[Ingest\n(scripts/ingest.py)]
  B --> C{Classifier\nPvP / PvE / Unknown}
  C --> D[Provenance\nHMAC + sha256]
  D --> E[Store\nJSONL + SQLite]
  E --> F[Anomaly Detector]
  F --> G[FRI Compute]
  G --> H[Report\nMarkdown]
Design tenets

Homeostatic: track FRI bands (Green/Yellow/Orange/Red) to signal posture shifts

Provenance-first: every event signed with HMAC + sha256

Minimal surface: pure-Python, no heavy deps, runs on constrained boxes

DR-ready: deterministic release pack + immutable rollback branch

Data & Artifacts
pgsql
Copy code
data/
  raw/
    auth.log                  # source input
  processed/
    events.jsonl              # signed events
    anomalies.jsonl           # anomaly findings
    fri.json                  # aggregate FRI snapshot
    catalog.db                # SQLite catalog (local vault)
  reports/
    report_YYYY-MM-DD_HHMMSS.md
events.jsonl fields (excerpt): ts, host, facility, severity, classifier, sha256, hmac, raw_line

FRI: scalar with banding → Green/Yellow/Orange/Red (used to gate responses)

Security & Provenance
HMAC event signing using key read from ops/secret.key (never committed).

.gitignore excludes raw vaults, DBs, and reports by default to avoid accidental leakage.

Recommended next step: signed tags (SSH/GPG) and SBOM at Gold.

OPSEC note: If a secret key ever appeared in history, rotate immediately and invalidate old reports.

Rollback & DR
Clone the immutable Bronze branch:

bash
Copy code
git clone --branch bronze --single-branch git@github.com:MYTHIK-blip/SWARMINT-AUTOPOIESIS.git SWARMINT-AUTOPOIESIS-EMBRYO
Rehydrate from release tarball (air-gap):

bash
Copy code
sha256sum -c SHA256SUMS.txt
tar -xzf SWARMINT-AUTOPOIESIS_bronze-gate-v0.1_src.tar.gz
Verify release/tag locally:

bash
Copy code
git tag -l | grep bronze-gate-v0.1
# (If signed later)
# git verify-tag -v bronze-gate-v0.1
Promotion Gates & Roadmap
mermaid
Copy code
stateDiagram-v2
  [*] --> Bronze
  Bronze --> Silver: Stability + Observability
  Silver --> Gold: Packaging + Dashboards + SBOM
  Gold --> Diamond: Governance + Mutation + Lineage
  Diamond --> [*]
🟤 Bronze (v0.1) – functional SIEM embryo ✓
Ingest → classify → HMAC → anomalies → FRI → JSONL/SQLite/Markdown

🥈 Silver (v0.2) – stability & observability
Dict packs + reclassifier, structured logs/metrics, CLI (swarmint), GH Actions CI, optional OTel/Loki exporter

🥇 Gold (v0.3) – packaging & integrity
Docker/compose, journalctl/ufw/nginx parsers, deception role inputs, SBOM, Grafana JSON dashboards

💎 Diamond (v1.0) – governance & mutation
Mutation budgets/ledger, provenance lineage, H-I-T-L triage console, environment promotion

Repo Layout
graphql
Copy code
config/
  process.yaml            # normalization/processing knobs
  schema/
    event.schema.json
    anomaly.schema.json

scripts/
  run_embryo.sh           # one-shot pipeline runner
  ingest.py               # parse + classify + sign
  fri.py                  # compute FRI
  report.py               # markdown report
  sample_data.py          # sample generator
  bronze_check.sh         # quick sanity checks

data/                     # local vault (ignored by git)
tests/                    # pytest for schemas + ingest
ops/
  run-record.json         # run metadata
  secret.key              # HMAC key (ignored by git)

.pre-commit-config.yaml, .ruff.toml, mypy.ini, requirements.txt
Configuration
config/process.yaml (excerpt of intent)

Input paths / globbing

Parse/normalization toggles

Classifier thresholds / dictionaries (to be expanded in Silver)

Report knobs (sections, limits)

Schemas

config/schema/event.schema.json – event payload invariants

config/schema/anomaly.schema.json – anomaly records

Scripts
scripts/run_embryo.sh – Orchestrates the full run (ingest → store → FRI → report)

scripts/ingest.py – Reads data/raw/auth.log, classifies, signs, writes events.jsonl + catalog.db

scripts/fri.py – Computes FRI (banded)

scripts/report.py – Emits Markdown report to data/reports/

scripts/sample_data.py – Generates synthetic auth.log for testing

scripts/bronze_check.sh – Lightweight gate checks (fsck, ruff, mypy, pytest)

Quality Gates (CI / Pre-commit)
Local dev

bash
Copy code
pre-commit install
pre-commit run --all-files
ruff check .
mypy .
pytest -q
CI (recommended minimal)

Lint + typecheck + tests on PRs

On tags matching *-gate-*: build report + attach to Release

Contributing
Commit emoji map

✨ feat, 🐛 fix, 📚 docs, ♻️ refactor, 🧪 test, 🧹 chore, 🔒 sec, ⚙️ ci

Branch rules

main: protected; PRs + checks required

bronze: immutable; no direct commits, no force-push

Issues and PRs welcome. Please avoid committing any real logs or secrets.

License
MIT — © 2025 MYTHIK-blip. See LICENSE.
