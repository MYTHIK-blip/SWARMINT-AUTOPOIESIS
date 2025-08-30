#!/usr/bin/env bash
set -euo pipefail
python -m pip install -r requirements.txt >/dev/null
ruff check .
mypy scripts --ignore-missing-imports
pytest -q
python scripts/ingest.py --input data/raw/auth.log --config config/process.yaml
python scripts/fri.py --config config/process.yaml
python scripts/report.py --config config/process.yaml
echo "BRONZE CHECK COMPLETE"
