<p align="center">
  <img src="https://img.shields.io/badge/Gate-🟤%20Bronze%20v0.1-%23cd7f32" alt="Gate Bronze">
  <a href="https://github.com/MYTHIK-blip/SWARMINT-AUTOPOIESIS/releases/tag/bronze-gate-v0.1">
    <img src="https://img.shields.io/badge/Release-bronze--gate--v0.1-1f6feb" alt="Release">
  </a>
  <img src="https://img.shields.io/badge/Branch-bronze%20(frozen)-8a2be2" alt="bronze branch">
  <img src="https://img.shields.io/badge/Python-3.11%2B-3776ab?logo=python&logoColor=white" alt="python">
  <img src="https://img.shields.io/badge/Mode-Air--Gap%20Ready-0b8f00" alt="Air Gap Ready">
  <img src="https://img.shields.io/badge/Provenance-HMAC%20per%20event-111111" alt="Provenance">
  <img src="https://img.shields.io/badge/License-MIT-blue" alt="License">
</p>

<h1 align="center">SWARMINT · AUTOPOIESIS <span title="Hive-grade posture">🐝</span></h1>
<p align="center"><b>Provenance-first, homeostatic SIEM embryo</b><br/>
<i>Built for degraded reality — keep signal alive under noise.</i></p>

<p align="center">
  <sub>
    <a href="#-tldr">Quickstart</a> •
    <a href="#-ethos">Ethos</a> •
    <a href="#%EF%B8%8F-architecture">Architecture</a> •
    <a href="#-data--artifacts">Artifacts</a> •
    <a href="#-security--provenance">Security</a> •
    <a href="#%EF%B8%8F-rollback--disaster-recovery">Rollback</a> •
    <a href="#-branch--tag-topology">Branches & Tags</a> •
    <a href="#-gates--roadmap">Gates</a> •
    <a href="#-operator-crib-copypaste">Operator Crib</a> •
    <a href="#-repo-layout">Repo Layout</a> •
    <a href="#-real-world-uses">Use Cases</a> •
    <a href="#-contributing">Contributing</a>
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
# Inspect artifacts
ls -lh data/processed/events.jsonl data/processed/anomalies.jsonl data/processed/fri.json
ls -lh data/reports/
Bronze is frozen at branch bronze and tag bronze-gate-v0.1.
For air-gap restores, use the curated tarball + SHA256SUMS.txt from the Release.

## 🧠 Ethos

<p>
  <img src="https://img.shields.io/badge/Provenance-First-111111" alt="Provenance First">
  <img src="https://img.shields.io/badge/Homeostasis-FRI-0b8f00" alt="Homeostasis FRI">
  <img src="https://img.shields.io/badge/Degenerate--Friendly-Minimal%20Deps-1f6feb" alt="Degenerate Friendly">
  <img src="https://img.shields.io/badge/Change%20Control-Immutable%20Gates-8a2be2" alt="Immutable Gates">
</p>

- **Provenance > spectacle** — every event is HMAC-signed + sha256’d.
- **Homeostasis as signal** — FRI (Fracture Readiness Index) tracks posture bands.
- **Degraded-reality ready** — minimal deps; deterministic restore; air-gap friendly.
- **Gates, not guesses** — releases + rollback branches you can *trust*.

```mermaid
flowchart TD
  A[Values] --> P[Provenance]
  A --> H[Homeostasis]
  A --> D[Degenerate<br/>Friendly]
  A --> G[Immutable Gates]
  P --> E[HMAC per event]
  H --> F[FRI bands]
  D --> M[Pure Python]
  G --> R[Tag + Release + Rollback]

<details> <summary><b>Principles → Practices (open)</b></summary>

Provenance → HMAC key in <code>ops/secret.key</code> (never committed); JSONL carries checksums.

Homeostasis → <code>fri.json</code> emits value + band (Green/Yellow/Orange/Red) for quick posture calls.

Degraded-friendly → one-shot runner (<code>scripts/run_embryo.sh</code>), SQLite catalog, release tarball.

Immutable gates → tag <code>bronze-gate-v0.1</code> and branch <code>bronze</code> are the rollback line.

</details> ```

## ⚙️ Architecture

<p>
  <img src="https://img.shields.io/badge/Pipeline-Ingest→Classify→Prove→Store→Detect→Assess→Report-111111" alt="Pipeline">
  <img src="https://img.shields.io/badge/FRI-Homeostasis-0b8f00" alt="FRI">
  <img src="https://img.shields.io/badge/Artifacts-JSONL%20%7C%20SQLite%20%7C%20Markdown-1f6feb" alt="Artifacts">
</p>

- **Ingest** `auth.log` → normalize tokens.  
- **Classify** → *PvP / PvE / Unknown*.  
- **Provenance** → HMAC + SHA256 per event.  
- **Store** → `events.jsonl` + `catalog.db` (SQLite).  
- **Detect** → `anomalies.jsonl`.  
- **Assess** → `fri.json` (value + band).  
- **Report** → human-readable Markdown.

```mermaid
flowchart LR
  subgraph Input
    A[ data/raw/auth.log ]
  end

  A --> B[ scripts/ingest.py<br/>parse + normalize ]
  B --> C{ classify<br/>PvP | PvE | Unknown }
  C --> D[ provenance<br/>HMAC + sha256 ]
  D --> E[ persist<br/>events.jsonl + catalog.db ]
  E --> F[ anomalies.jsonl ]
  E --> G[ scripts/fri.py → fri.json ]
  F --> H[ scripts/report.py ]
  G --> H
  H --> I[ data/reports/report_*.md ]

Legend

Ingest = parse & normalize auth records

Provenance = HMAC (secret in ops/secret.key) + SHA256

Assess = FRI posture (Green/Yellow/Orange/Red)

<details> <summary><b>Execution path & runners</b></summary>

Primary runner: <code>bash scripts/run_embryo.sh</code>

Direct pieces: <code>scripts/ingest.py</code>, <code>scripts/fri.py</code>, <code>scripts/report.py</code>

Synthetic input: <code>scripts/sample_data.py</code> (safe for demos)

State lands under <code>data/</code> (ignored by Git)

</details> ```

## 📦 Data & Artifacts

<p>
  <img src="https://img.shields.io/badge/Formats-JSONL%20%7C%20SQLite%20%7C%20Markdown-1f6feb" alt="Formats">
  <img src="https://img.shields.io/badge/Integrity-HMAC%20%2B%20SHA256-111111" alt="Integrity">
  <img src="https://img.shields.io/badge/Vault-Local%20(data%2F)-0b8f00" alt="Vault">
</p>

data/
raw/
auth.log
processed/
events.jsonl # signed events (sha256 + hmac)
anomalies.jsonl # detector findings
fri.json # homeostasis index (value + band)
catalog.db # SQLite catalog (local vault)
reports/
report_YYYY-MM-DD_HHMMSS.md

- `events.jsonl` — one event per line; includes `sha256` and `hmac` for provenance.  
- `anomalies.jsonl` — detector outputs with references back to event ids/hashes.  
- `fri.json` — aggregate posture (`fri` float + band: Green/Yellow/Orange/Red).  
- `catalog.db` — local SQLite for quick exploratory queries (not for long-term storage).  
- `reports/*.md` — human-readable situational summary for operators.

> `data/` is **ignored by Git** to prevent leakage of real logs or derived vaults.

<details>
<summary><b>Event (JSONL excerpt)</b></summary>

```json
{
  "ts": "2025-08-30T08:12:34Z",
  "host": "node-01",
  "facility": "auth",
  "severity": "notice",
  "classifier": "PvP",
  "sha256": "3f0d…",
  "hmac": "a91c…",
  "raw": "sshd[1234]: Failed password for invalid user test from 203.0.113.10 port 51234 ssh2"
}
</details> <details> <summary><b>FRI (example)</b></summary>

{ "fri": 0.62, "band": "Yellow" }
</details> <details> <summary><b>SQLite quick look (catalog.db)</b></summary>

sqlite3 data/processed/catalog.db \
  "SELECT ts, host, classifier FROM events ORDER BY ts DESC LIMIT 10;"
</details>
Provenance fields

sha256 — content checksum of canonicalized event payload.

hmac — keyed MAC using ops/secret.key (generated locally, never committed).

# one-time local key
mkdir -p ops && openssl rand -hex 32 > ops/secret.key && chmod 600 ops/secret.key

## 🔐 Security & Provenance

<p>
  <img src="https://img.shields.io/badge/Provenance-HMAC%20%2B%20SHA256-111111" alt="Provenance">
  <img src="https://img.shields.io/badge/Secrets-Never%20Commit-cc0000" alt="Never Commit">
  <img src="https://img.shields.io/badge/Rollback-Immutable%20Gates-8a2be2" alt="Immutable Gates">
  <img src="https://img.shields.io/badge/Air--Gap-Ready-0b8f00" alt="Air Gap Ready">
</p>

- **HMAC per event** — each canonicalized event is checksummed (sha256) and signed (HMAC).  
- **Key stays local** — `ops/secret.key` is **generated on the node**, ignored by Git.  
- **No data leakage** — `data/` vaults + reports are ignored; do not commit real logs.  
- **Release hygiene** — curated tarball + `SHA256SUMS.txt` for deterministic restore.  
- **Gates** — `bronze` branch + `bronze-gate-v0.1` tag are the immutable rollback line.

<details>
<summary><b>Generate / rotate HMAC key</b></summary>

```bash
# one-time key (local only)
mkdir -p ops
openssl rand -hex 32 > ops/secret.key
chmod 600 ops/secret.key

# rotate on suspicion (invalidate old reports downstream if needed)
mv ops/secret.key ops/secret.key.old.$(date +%Y%m%d%H%M%S)
openssl rand -hex 32 > ops/secret.key && chmod 600 ops/secret.key

# (optional) record a non-secret key identifier (e.g., sha256 of key file) in ops/run-record.json
python - <<'PY'
import hashlib, json, pathlib, time
p=pathlib.Path("ops/secret.key")
kid=hashlib.sha256(p.read_bytes()).hexdigest()[:12]
rr=pathlib.Path("ops/run-record.json")
rec={"hmac_kid":kid,"rotated_at":time.strftime("%FT%TZ",time.gmtime())}
rr.write_text(json.dumps(rec, indent=2)+"\n")
print("KID:", kid)
PY
</details> <details> <summary><b>Secret scanning (local)</b></summary>

# run pre-commit hooks (includes detect-secrets baseline)
pre-commit run --all-files || true

# update / audit the baseline if needed
detect-secrets scan > .secrets.baseline
detect-secrets audit .secrets.baseline
Spot-check history

# look for accidental additions of known secret paths / patterns
git log -p -- ops/secret.key || true
git log -G 'BEGIN PRIVATE KEY|password|token' -- . || true
</details> <details> <summary><b>If a secret ever leaked in history</b></summary>

# 1) Rotate keys immediately (see rotate block), redeploy artifacts
# 2) Remove from history (choose one tool)
pipx install git-filter-repo  # or: brew install git-filter-repo

git filter-repo --path ops/secret.key --invert-paths
git push --force-with-lease origin main

# 3) Invalidate downstream reports produced with the old key
# 4) Announce rotation scope in SECURITY.md / Release notes
</details> <details> <summary><b>Supply chain hardening (next gates)</b></summary>
Signed tags & releases (GPG/SSH) + git verify-tag in operator runbooks.

SBOM for Python deps at release time.

Branch protections: disallow force-push to main & bronze, require PR checks.

</details>
.gitignore (already present, key lines)

# secrets
ops/secret.key

# local vaults / artifacts
/data/
/dist/
/.venv/
/.mypy_cache/
/.pytest_cache/
/.ruff_cache/
## 🛡️ Rollback & Disaster Recovery

<p>
  <img src="https://img.shields.io/badge/Rollback-Immutable%20Branch-8a2be2" alt="Immutable">
  <img src="https://img.shields.io/badge/Release-Tarball%20%2B%20SHA256SUMS-111111" alt="Tarball">
  <img src="https://img.shields.io/badge/Air--Gap-Ready-0b8f00" alt="Air Gap">
</p>

<details>
<summary><b>Fast dev rollback — frozen branch</b></summary>

```bash
git fetch --all --tags
git switch bronze
</details> <details> <summary><b>Deterministic restore — verified tarball (air-gap)</b></summary>
Download from the Bronze Release:

SWARMINT-AUTOPOIESIS_bronze-gate-v0.1_src.tar.gz

SHA256SUMS.txt

sha256sum -c SHA256SUMS.txt
tar -xzf SWARMINT-AUTOPOIESIS_bronze-gate-v0.1_src.tar.gz
cd SWARMINT-AUTOPOIESIS
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt || true
bash scripts/run_embryo.sh
</details> <details> <summary><b>Pin exact Bronze tag (detached)</b></summary>

git fetch --all --tags
git switch --detach bronze-gate-v0.1
</details> <details> <summary><b>Verify rollback line (all SHAs should match)</b></summary>

git rev-parse bronze-gate-v0.1^{}
git rev-parse origin/bronze
git rev-parse bronze
</details> <details> <summary><b>Disaster drill (clean room)</b></summary>

# clone to a new working dir
git clone --branch bronze --single-branch git@github.com:MYTHIK-blip/SWARMINT-AUTOPOIESIS.git SWARMINT-AUTOPOIESIS-EMBRYO
cd SWARMINT-AUTOPOIESIS-EMBRYO
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt || true
python -u scripts/sample_data.py
bash scripts/run_embryo.sh
</details> ```

## 🌳 Branch & Tag Topology

<p>
  <img src="https://img.shields.io/badge/Default-main-1f6feb" alt="main">
  <img src="https://img.shields.io/badge/Rollback-bronze%20(frozen)-8a2be2" alt="bronze">
  <img src="https://img.shields.io/badge/ReleaseTag-bronze--gate--v0.1-%23cd7f32" alt="tag">
</p>

```mermaid
flowchart LR
  subgraph Bronze Line (Rollback)
    T[(tag: bronze-gate-v0.1)]
    B[(branch: bronze)]
    T --- B
  end

  subgraph Development
    M[(main)]
    S[(feature/* e.g., silver)]
    S --> M
  end

  B --> M
Contract

bronze = immutable rollback branch (no force-push; no direct commits).

bronze-gate-v0.1 = release tag pointing to the exact Bronze commit.

main = active development (future gates originate here via PRs).

Feature branches (e.g. silver) → PR → squash merge into main.

<details> <summary><b>Consistency checks</b></summary>

# all should match the same SHA at Bronze
git rev-parse bronze-gate-v0.1^{}
git rev-parse origin/bronze
git rev-parse bronze

# show remote branches; confirm bronze exists and is tracking
git ls-remote --heads origin | grep refs/heads/bronze

# protect branches (recommended): in GitHub → Settings → Branches
# - Protect 'main' (PRs + status checks once CI exists)
# - Protect 'bronze' (no pushes; no force pushes)
</details> ```

## 🛣️ Gates & Roadmap

<p>
  <img src="https://img.shields.io/badge/Now-🟤%20Bronze%20v0.1-%23cd7f32" alt="Bronze">
  <img src="https://img.shields.io/badge/Next-🥈%20Silver%20v0.2-1f6feb" alt="Silver">
  <img src="https://img.shields.io/badge/Then-🥇%20Gold%20v0.3-ffd700" alt="Gold">
  <img src="https://img.shields.io/badge/Target-💎%20Diamond%20v1.0-8a2be2" alt="Diamond">
</p>

```mermaid
stateDiagram-v2
  [*] --> Bronze
  Bronze --> Silver: Stability + Observability
  Silver --> Gold: Packaging + Parsers + SBOM
  Gold --> Diamond: Governance + Mutation + Lineage
  Diamond --> [*]
🟤 Bronze (v0.1) — ✅ Shipped
Ingest → classify → HMAC → anomalies → FRI → JSONL/SQLite/Markdown
Artifacts: release tag bronze-gate-v0.1, immutable branch bronze, tarball + SHA256SUMS.txt.

Exit criteria (met):

 Immutable rollback branch & tag

 Deterministic tarball + checksums

 Readme & operator crib

 Basic tests & local pre-commit hygiene

🥈 Silver (v0.2) — Stability & Observability
Focus on signal visibility and operator ergonomics without expanding surface area.

Planned scope:

Metrics emitter → data/processed/metrics.json

Totals: events, anomalies, PvP/PvE/Unknown counts

FRI: value + band

Build meta: git_rev, tag (if any), dataset_sha256 (auth.log)

Minimal CI (GitHub Actions)

On PRs to main: ruff + mypy + pytest -q

On tags matching *-gate-*: run pipeline; attach report_*.md + metrics.json to Release

Classifier “dict packs” (seedable rule dictionaries for auth failure heuristics)

CLI polish (optional): python -m scripts.ingest / small wrapper swarmint

Structured logs for pipeline steps (start/end + durations)

Exit criteria (checklist):

 metrics.json produced by run_embryo.sh

 CI green on PRs (lint/type/test)

 Release workflow publishes metrics & report on *-gate-* tags

 README badges updated (CI, metrics)

Milestone: Silver Smoke (mid-gate validation) → metrics + CI running on silver PR before full gate.

🥇 Gold (v0.3) — Packaging & Integrity
Make it deployable + auditable.

Planned scope:

Docker/Compose (single-service) for embryo

Parsers for journalctl, ufw, nginx access/error

Deception-input hooks (harmless canaries)

SBOM at release (Python deps snapshot)

Grafana/JSON dashboards (read-only posture view)

Exit criteria:

 Image published (GHCR) + compose up

 SBOM attached to Release

 Parsers + dashboards documented

💎 Diamond (v1.0) — Governance & Mutation
Operate safely under change.

Planned scope:

Mutation budgets + ledger, provenance lineage across runs

HITL triage console (operator review loop)

Environment promotions (dev → staging → prod)

Policy docs & response playbooks

Exit criteria:

 Mutation ledger & lineage export

 Review console MVP

 Promotion policy + playbooks merged

Now / Next / Later
Now: Keep Bronze immutable; merge docs; prep Silver branch

Next (Silver): metrics + CI + dict packs; tag silver-gate-v0.2

Later (Gold+): containers, parsers, SBOM, dashboards → governance

<details> <summary><b>Kick off Silver (optional; run when ready)</b></summary>

# create a working branch for Silver
git switch main
git pull --ff-only
git switch -c silver

# (you'll add metrics + CI in this branch; open PR back to main)
# sample PR command:
# gh pr create -f -B main -t "feat(silver): metrics + minimal CI" -b "Adds metrics.json and CI (ruff/mypy/pytest); seeds dict packs."
</details> ```

## 🧰 Operator Crib (copy/paste)

<p>
  <img src="https://img.shields.io/badge/Mode-Operator--First-111111" alt="Operator">
  <img src="https://img.shields.io/badge/Hygiene-Precommit%20%7C%20Lint%20%7C%20Test-1f6feb" alt="Hygiene">
  <img src="https://img.shields.io/badge/DR-Branch%20%7C%20Tag%20%7C%20Tarball-8a2be2" alt="DR">
</p>

<details>
<summary><b>Setup & run (Bronze embryo)</b></summary>

```bash
# clone & enter
git clone git@github.com:MYTHIK-blip/SWARMINT-AUTOPOIESIS.git
cd SWARMINT-AUTOPOIESIS

# venv + deps
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt || true

# synthetic input + pipeline run
python -u scripts/sample_data.py
bash scripts/run_embryo.sh
</details> <details> <summary><b>Inspect artifacts</b></summary>

ls -lh data/processed/events.jsonl data/processed/anomalies.jsonl data/processed/fri.json
ls -lh data/reports/
head -n 3 data/processed/events.jsonl
</details> <details> <summary><b>Git hygiene & branching</b></summary>

# status (short) + current branch
git status -sb

# sync main, create a feature branch (e.g., silver)
git switch main
git pull --ff-only
git switch -c silver
</details> <details> <summary><b>Rollback verification (Bronze line)</b></summary>

git fetch --all --tags
git rev-parse bronze-gate-v0.1^{}
git rev-parse origin/bronze
git rev-parse bronze
# Expect all three SHAs to match (immutable rollback line)
</details> <details> <summary><b>Tarball pack + checksums (deterministic release)</b></summary>

mkdir -p dist
git archive --format=tar.gz --output="dist/SWARMINT-AUTOPOIESIS_bronze-gate-v0.1_src.tar.gz" bronze-gate-v0.1
( cd dist && sha256sum SWARMINT-AUTOPOIESIS_bronze-gate-v0.1_src.tar.gz > SHA256SUMS.txt )

# verify later / elsewhere
cd dist && sha256sum -c SHA256SUMS.txt
</details> <details> <summary><b>Release attach (GitHub CLI)</b></summary>

# create release if missing
gh release view bronze-gate-v0.1 >/dev/null 2>&1 || \
  gh release create bronze-gate-v0.1 \
    --title "🟤 Bronze Gate v0.1 — SIEM embryo" \
    --notes "Auth.log ingest → PvP/PvE/Unknown → HMAC → anomalies → FRI → JSONL/SQLite/Markdown."

# upload artifacts (clobber to overwrite)
gh release upload bronze-gate-v0.1 \
  dist/SWARMINT-AUTOPOIESIS_bronze-gate-v0.1_src.tar.gz \
  dist/SHA256SUMS.txt --clobber
</details> <details> <summary><b>Pre-commit + QA sweep</b></summary>

# run all hooks (ruff-format, ruff, mypy, tests, detect-secrets)
pre-commit install
pre-commit run --all-files || true

# manual checks
ruff check .
mypy .
pytest -q || true
</details> <details> <summary><b>Safe workspace cleaning (preview → execute)</b></summary>

# preview ignored-file cleanup (SAFE: does not touch tracked files)
git clean -nfdX -e ops/secret.key

# execute only if the preview looks correct
git clean -fdX -e ops/secret.key
</details> <details> <summary><b>PR merge (squash) + clean branch</b></summary>

# squash & delete the source branch after merge
gh pr merge <NUMBER> --squash --delete-branch \
  --subject "docs: master README (enterprise + arcade UX, Bronze→Silver runway)" \
  --body "Docs-only; DR playbooks, architecture diagrams, and operator crib."
</details> <details> <summary><b>Dataset fingerprint (helpful for metrics)</b></summary>

sha256sum data/raw/auth.log 2>/dev/null || echo "no local auth.log"
git rev-parse --short HEAD
</details> ```

## 🧭 Repo Layout

<p>
  <img src="https://img.shields.io/badge/Layout-Operator%20Centric-111111" alt="Layout">
  <img src="https://img.shields.io/badge/Vault-data%2F%20(ignored)-0b8f00" alt="Vault">
  <img src="https://img.shields.io/badge/Scripts-Orchestrated-1f6feb" alt="Scripts">
</p>

config/
process.yaml # pipeline knobs & defaults
schema/
event.schema.json # event payload invariants
anomaly.schema.json # anomaly payload invariants

scripts/
run_embryo.sh # one-shot pipeline runner
ingest.py # parse + classify + sign (HMAC + sha256)
fri.py # compute FRI (value + band)
report.py # emit Markdown report
sample_data.py # generate synthetic auth.log
bronze_check.sh # light sanity checks (fsck/ruff/mypy/pytest)

data/ # LOCAL VAULT (gitignored)
raw/ # inputs (e.g., auth.log)
processed/ # events.jsonl, anomalies.jsonl, catalog.db, fri.json
reports/ # report_*.md

ops/
run-record.json # optional run metadata (non-secret)
secret.key # HMAC key (local, gitignored)

tests/ # pytest: schemas + ingest

.github/
ISSUE_TEMPLATE/ # issue scaffolds (optional)

(Silver) workflows/ci # ruff + mypy + pytest on PRs
.pre-commit-config.yaml # local hygiene (ruff, mypy, tests, detect-secrets)
.ruff.toml # lint rules
.mypy.ini # type-check config
requirements.txt # runtime deps
README.md # you are here

release artifacts (optional, gitignored locally)
dist/
SWARMINT-AUTOPOIESIS_bronze-gate-v0.1_src.tar.gz
SHA256SUMS.txt

<details>
<summary><b>Why this structure?</b></summary>

- **Separation of concerns** → code (`scripts/`), policy (`config/`), vault (`data/`), ops (`ops/`).
- **Safe-by-default** → `data/` and `ops/secret.key` are excluded via `.gitignore`.
- **Deterministic ops** → `dist/` holds curated release pack + checksums.
- **Testable edges** → `tests/` validate schemas & ingest behavior.
</details>

🌍 Real-World Use Cases
<p> <img src="https://img.shields.io/badge/Air--Gap-Ready-0b8f00" alt="Air Gap Ready"> <img src="https://img.shields.io/badge/Footprint-Low-111111" alt="Low Footprint"> <img src="https://img.shields.io/badge/Runs-Pure%20Python-3776ab?logo=python&logoColor=white" alt="Pure Python"> <img src="https://img.shields.io/badge/Restore-Deterministic%20Tarball-1f6feb" alt="Deterministic"> <img src="https://img.shields.io/badge/UX-Operator--First-8a2be2" alt="Operator-First"> </p>

Sector map:
<a href="#civic--government">Civic & Government</a> ·
<a href="#critical-infrastructure--ot">Critical Infrastructure & OT</a> ·
<a href="#smb--enterprise">SMB & Enterprise</a> ·
<a href="#education--research">Education & Research</a> ·
<a href="#incident-response--dfir">Incident Response & DFIR</a> ·
<a href="#field--edge--austere">Field & Edge (Austere)</a> ·
<a href="#healthcare--life-safety">Healthcare & Life Safety</a> ·
<a href="#finance--finops--fincrime">Finance & FinOps / FinCrime</a> ·
<a href="#elections--civic-trust">Elections & Civic Trust</a> ·
<a href="#media--creative--newsrooms">Media, Creative & Newsrooms</a> ·
<a href="#nonprofit--community-defense">Nonprofit & Community Defense</a> ·
<a href="#cloud--soc-pipelines">Cloud & SOC Pipelines</a> ·
<a href="#devsecops--sre-labs">DevSecOps & SRE Labs</a> ·
<a href="#personal-lab--homelab">Personal Lab / Homelab</a>

Civic & Government
<details id="civic--government"><summary><b>🛡️ City / agency posture under budget + scrutiny</b></summary>

Why SWARMINT

Runs on existing Linux hosts; no new licensing or heavy infra.

FRI gives executives a single posture dial (Green→Red) for briefings.

Deploy (minimal)

# on a bastion or audit node
git clone --branch bronze --single-branch git@github.com:MYTHIK-blip/SWARMINT-AUTOPOIESIS.git
cd SWARMINT-AUTOPOIESIS && python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt || true
sudo cp /var/log/auth.log data/raw/auth.log
bash scripts/run_embryo.sh


Signals to watch

Spike in PvP classifications; FRI drifting Yellow→Orange.

Repeated privileged auth failures from remote subnets.

Silver+

Add journalctl parser for service restarts; ufw for block trends.

</details>
Critical Infrastructure & OT
<details id="critical-infrastructure--ot"><summary><b>⚙️ OT islands with strict change windows</b></summary>

Why

Air-gap restore from tarball; deterministic artifact trail.

Operates in observation mode with minimal blast radius.

Deploy (air-gap)

sha256sum -c SHA256SUMS.txt
tar -xzf SWARMINT-AUTOPOIESIS_bronze-gate-v0.1_src.tar.gz
cd SWARMINT-AUTOPOIESIS && python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt || true
bash scripts/run_embryo.sh


Signals

Off-hours auth drift; lateral movement breadcrumbs; FRI band changes per shift.

</details>
SMB & Enterprise
<details id="smb--enterprise"><summary><b>🏢 Fast posture readouts without SIEM overhauls</b></summary>

Why

Drop-in telemetry refinery feeding your existing tools (JSONL/SQLite/Markdown).

Clear rollback branch (bronze) keeps auditors happy.

Interop

Silver: export metrics.json to log shipper; push to Loki/OTel gateway.

</details>
Education & Research
<details id="education--research"><summary><b>🎓 Teaching detection + provenance thinking</b></summary>

Why

Pure Python; readable pipeline; reproducible runs for grading/research notes.

Lab run

python -u scripts/sample_data.py
bash scripts/run_embryo.sh


Assignments

Extend classifier “dict packs”; design anomaly heuristics; reason about FRI & bias.

</details>
Incident Response & DFIR
<details id="incident-response--dfir"><summary><b>🚑 Portable triage kit for captured logs</b></summary>

Why

Works in clean rooms; provenance trail (sha256 + HMAC) supports chain-of-custody.

Workflow

Import host auth.log snapshots → run → archive report_*.md + fri.json + metrics.json (Silver).

</details>
Field & Edge (Austere)
<details id="field--edge--austere"><summary><b>🛰️ Low-power nodes; intermittent connectivity</b></summary>

Why

Minimal deps; resumable runs; markdown reports viewable offline.

Tips

Batch data/reports/ and sync when back in coverage.

</details>
Healthcare & Life Safety
<details id="healthcare--life-safety"><summary><b>🏥 Conservative change control; staff under load</b></summary>

Why

Read-only posture signal (FRI) reduces cognitive load; keeps patient care first.

Signals

Privileged account anomalies; FRI excursions during shift changes.

</details>
Finance & FinOps / FinCrime
<details id="finance--finops--fincrime"><summary><b>💳 Forensics-friendly artifacts; runbooks for audit</b></summary>

Why

Deterministic restore for audit recreations; attach reports to tickets & SAR trails.

Silver

CI verifies metrics on PR; attach artifacts to gate tags for audit packs.

</details>
Elections & Civic Trust
<details id="elections--civic-trust"><summary><b>🗳️ Chain-of-custody focus; transparent posture</b></summary>

Why

Clear rollback + signed releases (Gold) → verifiable trust surface.

Deploy

Read-only collectors on pollbook servers; daily FRI deltas for command centers.

</details>
Media, Creative & Newsrooms
<details id="media--creative--newsrooms"><summary><b>📰 Small teams; high-risk sources</b></summary>

Why

No-SaaS posture loop; can run on the same laptop as editorial tooling.

Signals

Remote auth attempts; sudden FRI spikes when embargoed content is staged.

</details>
Nonprofit & Community Defense
<details id="nonprofit--community-defense"><summary><b>🧰 Safety co-ops; volunteer operators</b></summary>

Why

Simple copy/paste ops; Markdown reports share well across low-friction tools.

Pattern

One “honey node” per collective; nightly FRI + anomaly digest.

</details>
Cloud & SOC Pipelines
<details id="cloud--soc-pipelines"><summary><b>☁️ Edge refinery → central lake</b></summary>

Why

Produce small, typed JSON for downstream enrichment; keep provenance attached.

Silver+

OTel exporter; Loki route; dashboards later at Gold.

</details>
DevSecOps & SRE Labs
<details id="devsecops--sre-labs"><summary><b>🧪 Hypothesis-driven detection; reproducible</b></summary>

Why

Run the same pipeline locally and in CI; attach outputs to PRs.

Snippet

# quick smoke in CI (to wire later)
ruff check .
mypy .
pytest -q || true

</details>
Personal Lab / Homelab
<details id="personal-lab--homelab"><summary><b>🏠 Learn detections; protect your stack</b></summary>

Run

python -u scripts/sample_data.py
bash scripts/run_embryo.sh


Watch

FRI across router/SSH boxes; unexpected logins from travel IPs.

</details>

## 🤝 Contributing

<p>
  <img src="https://img.shields.io/badge/Workflow-PRs%20%7C%20Squash-1f6feb" alt="PR Workflow">
  <img src="https://img.shields.io/badge/Hygiene-Precommit%20%7C%20Lint%20%7C%20Type%20%7C%20Tests-0b8f00" alt="Hygiene">
  <img src="https://img.shields.io/badge/Branches-Protected%20(main%2C%20bronze)-8a2be2" alt="Protected Branches">
</p>

**Branch rules**
- `main` — protected; changes land via PRs (squash merge recommended).
- `bronze` — immutable rollback line; **no direct commits, no force-push**.
- Feature work → `feature/<topic>` (e.g., `silver`) → PR to `main`.

**Commit emoji (suggested)**
- ✨ feat · 🐛 fix · 📚 docs · ♻️ refactor · 🧪 test · 🧹 chore · 🔒 sec · ⚙️ ci

<details>
<summary><b>Local setup & hygiene</b></summary>

```bash
# venv + deps
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt || true

# pre-commit hooks (ruff-format, ruff, mypy, tests, detect-secrets)
pre-commit install
pre-commit run --all-files || true

# manual checks
ruff check .
mypy .
pytest -q || true
</details> <details> <summary><b>Typical PR flow</b></summary>

# sync & branch
git switch main
git pull --ff-only
git switch -c feature/silver-metrics

# work … then commit
git add -A
git commit -m "✨ feat(silver): emit metrics.json + basic counters"

# push & open PR
git push -u origin HEAD
gh pr create -f -B main -t "feat(silver): metrics emitter" -b "Adds metrics.json; seeds counters & FRI band."

# squash merge & clean up
gh pr merge <NUMBER> --squash --delete-branch \
  --subject "feat(silver): metrics emitter" \
  --body "Adds metrics.json; counters; FRI band; wires into run_embryo."
</details> <details> <summary><b>Branch protection (maintainers)</b></summary>
Protect main: require PRs + status checks (CI at Silver).

Protect bronze: block pushes & force-push; allow merges from no one.

Optional: restrict who can create *-gate-* tags/releases.

</details> <details> <summary><b>Security disclosures</b></summary>
Use GitHub Security Advisories or the profile contact method.

Do not file public issues for sensitive findings.

</details> ```

## 📜 License & Attribution

<p>
  <a href="./LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue" alt="MIT"></a>
  <img src="https://img.shields.io/badge/Copyright-©%202025%20MYTHIK--blip-111111" alt="Copyright">
  <img src="https://img.shields.io/badge/Author-Kerehama%20Mcleod%20(%5FMYTHIK%5F)-1f6feb" alt="Author">
</p>

**License:** MIT — see [`LICENSE`](./LICENSE).

**Author:** Kerehama Mcleod (MYTHIK-blip / _MYTHIK_)  
**Project:** Homeostatic AI 🐝

<details>
<summary><b>How to cite (Bronze release)</b></summary>

```bibtex
@software{swarmint_autopoiesis_bronze_v0_1_2025,
  author  = {Mcleod, Kerehama},
  title   = {SWARMINT-AUTOPOIESIS: Provenance-first, homeostatic SIEM embryo},
  year    = {2025},
  version = {bronze-gate-v0.1},
  url     = {https://github.com/MYTHIK-blip/SWARMINT-AUTOPOIESIS},
  note    = {Immutable rollback branch: bronze; Release tarball with SHA256SUMS}
}
</details> <details> <summary><b>Acknowledgments</b></summary>
Python ecosystem & open-source maintainers 🫶

Operators who value provenance, minimal surface, and clear rollback lines

Future contributors shaping Silver → Gold → Diamond

</details>
<sub><i>All product names, logos, and brands are property of their respective owners. Use is for identification only and does not imply endorsement.</i></sub>
