<!--
  SWARMINT-AUTOPOIESIS — Enterprise/Gamer Readme
  Vibe: palantir x cyber-arcade | Bronze-solid, Silver-ready
-->

<p align="center">
  <img src="https://img.shields.io/badge/Gate-🟤%20Bronze%20v0.1-%23cd7f32" alt="Gate Bronze">
  <a href="https://github.com/MYTHIK-blip/SWARMINT-AUTOPOIESIS/releases/tag/bronze-gate-v0.1">
    <img src="https://img.shields.io/badge/Release-bronze--gate--v0.1-1f6feb" alt="Release">
  </a>
  <img src="https://img.shields.io/badge/Branch-bronze%20(frozen)-8a2be2" alt="bronze branch">
  <img src="https://img.shields.io/badge/Python-3.11%2B-3776ab?logo=python&logoColor=white" alt="python">
  <img src="https://img.shields.io/badge/Mode-Air--Gap%20Ready-0b8f00" alt="Air Gap Ready">
  <img src="https://img.shields.io/badge/Provenance-HMAC%20per%20event-111111" alt="Provenance">
  <img src="https://img.shields.io/github/stars/MYTHIK-blip/SWARMINT-AUTOPOIESIS?style=social" alt="stars">
  <img src="https://img.shields.io/github/downloads/MYTHIK-blip/SWARMINT-AUTOPOIESIS/total" alt="downloads">
  <img src="https://img.shields.io/badge/License-MIT-blue" alt="License">
</p>

<h1 align="center">SWARMINT · AUTOPOIESIS</h1>
<p align="center"><b>Provenance-first, homeostatic SIEM embryo</b><br/>
<i>Built for degraded reality — keep signal alive under noise.</i></p>

<p align="center">
  <sub>
    <a href="#-tldr">Quickstart</a> •
    <a href="#%EF%B8%8F-architecture">Architecture</a> •
    <a href="#-data--artifacts">Artifacts</a> •
    <a href="#%EF%B8%8F-rollback--disaster-recovery">Rollback</a> •
    <a href="#-branch--tag-topology">Branches & Tags</a> •
    <a href="#%EF%B8%8F-gates--roadmap">Gates</a> •
    <a href="#-operator-crib-copypaste">Operator Crib</a>
  </sub>
</p>

<hr/>

## ⚡ TL;DR

```bash
# Clone (SSH)
git clone git@github.com:MYTHIK-blip/SWARMINT-AUTOPOIESIS.git
cd SWARMINT-AUTOPOIESIS
bash
Copy code
# Run the Bronze embryo (with synthetic data)
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt || true
python -u scripts/sample_data.py
bash scripts/run_embryo.sh
bash
Copy code
# Check output
ls -lh data/processed/events.jsonl data/processed/anomalies.jsonl data/processed/fri.json
ls -lh data/reports/
Bronze is frozen at branch bronze and tag bronze-gate-v0.1.
For air-gap restores, use the curated tarball + SHA256SUMS.txt from the Release.

🧠 Ethos
Provenance > spectacle. Every event is HMAC-signed + checksummed.

Homeostasis as signal. FRI (Fracture Readiness Index) + banding communicates posture shifts.

Degenerate-friendly. Minimal deps, deterministic restore, runs on constrained boxes.

Immutable gates. Release + rollback you can trust.

🧩 What It Does (Bronze)
Ingest: normalize auth.log

Classify: PvP / PvE / Unknown

Provenance: HMAC + SHA256 per event (ops/secret.key, never committed)

Persist: JSONL (events.jsonl) + SQLite (catalog.db)

Detect: anomalies.jsonl

Assess: fri.json (value + band)

Report: human report data/reports/report_*.md

🗺️ Architecture
mermaid
Copy code
flowchart LR
  A[ data/raw/auth.log ] --> B[ ingest.py<br/>normalize + parse ]
  B --> C{ classify<br/>PvP / PvE / Unknown }
  C --> D[ provenance<br/>HMAC + sha256 ]
  D --> E[ store<br/>events.jsonl + catalog.db ]
  E --> F[ anomalies.jsonl ]
  E --> G[ fri.py → fri.json ]
  F --> H[ report.py ]
  G --> H[ report.py ]
  H --> I[ data/reports/report_*.md ]
Design Tenets

Small surface (pure Python)

Deterministic release tarball + checksums

Operator-first UX (copy/paste flows)

📦 Data & Artifacts
bash
Copy code
data/
  raw/
    auth.log
  processed/
    events.jsonl              # signed events
    anomalies.jsonl           # detector findings
    fri.json                  # FRI value + band
    catalog.db                # SQLite (local vault)
  reports/
    report_YYYY-MM-DD_HHMMSS.md
Event (excerpt)

json
Copy code
{
  "ts": "2025-08-30T08:12:34Z",
  "host": "node-01",
  "facility": "auth",
  "classifier": "PvP",
  "sha256": "…",
  "hmac": "…",
  "raw": "sshd[1234]: Failed password for …"
}
FRI (excerpt)

json
Copy code
{ "fri": 0.62, "band": "Yellow" }
🔐 Security & Provenance
HMAC per event using key at ops/secret.key (ignored by Git).

bash
Copy code
# generate/rotate key locally
mkdir -p ops
openssl rand -hex 32 > ops/secret.key
chmod 600 ops/secret.key
.gitignore excludes raw vaults, DBs, reports, caches, and .venv/.

Future gates: signed tags/releases, SBOM.

♻️ Rollback & Disaster Recovery
<details> <summary><b>Fast dev rollback — frozen branch</b></summary>
bash
Copy code
git fetch --all --tags
git switch bronze
</details> <details> <summary><b>Deterministic ops/air-gap restore — verified tarball</b></summary>
Download from Bronze Release:

SWARMINT-AUTOPOIESIS_bronze-gate-v0.1_src.tar.gz

SHA256SUMS.txt

bash
Copy code
sha256sum -c SHA256SUMS.txt
tar -xzf SWARMINT-AUTOPOIESIS_bronze-gate-v0.1_src.tar.gz
cd SWARMINT-AUTOPOIESIS
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt || true
bash scripts/run_embryo.sh
</details> <details> <summary><b>Pin exact Bronze tag (detached)</b></summary>
bash
Copy code
git fetch --all --tags
git switch --detach bronze-gate-v0.1
</details>
🌳 Branch / Tag Topology
scss
Copy code
(tag) bronze-gate-v0.1 ─┐
(branch) bronze ────────┤  (immutable rollback line)
                         └── main ── feature branches (e.g., silver) ──> PRs ──> main
Verify the pin

bash
Copy code
git rev-parse bronze-gate-v0.1^{}
git rev-parse origin/bronze
git rev-parse bronze
# all three SHAs should match
🛣️ Gates & Roadmap
mermaid
Copy code
stateDiagram-v2
  [*] --> Bronze
  Bronze --> Silver: Stability + Observability
  Silver --> Gold: Packaging + Parsers + SBOM
  Gold --> Diamond: Governance + Mutation + Lineage
  Diamond --> [*]
🟤 Bronze (v0.1) — Embryo shipped
Ingest → classify → HMAC → anomalies → FRI → JSONL/SQLite/Markdown.

🥈 Silver (v0.2) — Stability & Observability
metrics.json (events/anomalies/FRI + git rev + sha256s), minimal CI (ruff+mypy/pytest on PRs; on *-gate-* tags build & attach artifacts).

🥇 Gold (v0.3) — Packaging & Integrity
Docker/compose, journalctl/ufw/nginx parsers, deception inputs, SBOM, dashboards.

💎 Diamond (v1.0) — Governance & Mutation
Mutation budgets/ledger, provenance lineage, H-I-T-L triage console, environment promotions.

🧪 Dev & Quality Gates
Local hygiene

bash
Copy code
pre-commit install
pre-commit run --all-files || true
ruff check .
mypy .
pytest -q || true
Tip: Activate the venv before running Python tasks.

bash
Copy code
source .venv/bin/activate
(Silver CI — planned)

PRs: ruff + mypy + pytest

Tags *-gate-*: run pipeline; upload report_*.md + metrics.json to the Release

🧰 Operator Crib (copy/paste)
Run with synthetic input

bash
Copy code
python -u scripts/sample_data.py
bash scripts/run_embryo.sh
Show artifacts

bash
Copy code
ls -lh data/processed/events.jsonl data/processed/anomalies.jsonl data/processed/fri.json
ls -lh data/reports/
Back to latest main

bash
Copy code
git switch main
git pull --ff-only
Start Silver work

bash
Copy code
git switch main
git pull --ff-only
git switch -c silver
🧭 Repo Layout
pgsql
Copy code
config/
  process.yaml
  schema/
    event.schema.json
    anomaly.schema.json
scripts/
  run_embryo.sh
  ingest.py
  fri.py
  report.py
  sample_data.py
  bronze_check.sh
data/                    # local vault (ignored)
ops/
  run-record.json
  secret.key             # HMAC key (ignored)
tests/
.pre-commit-config.yaml
.ruff.toml
.mypy.ini
🧑‍💻 Real-World Uses
Field laptop / bastion seed SIEM (no containers needed)

Air-gapped triage: restore from tarball, run against captured logs, export markdown report

Forensics: verify checksums, re-run deterministically for reproducibility

Training: operator drills on PvP/PvE classification + FRI posture

📜 License & Attribution
MIT — see LICENSE.

Author: MYTHIK-blip (Kerehama Mcleod / MYTHIK)

