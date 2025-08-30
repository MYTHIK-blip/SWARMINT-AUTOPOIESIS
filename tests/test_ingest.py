import json
import pathlib


def test_events_written():
    p = pathlib.Path("data/processed/events.jsonl")
    assert p.exists(), "events.jsonl missing"
    line = p.read_text().strip().splitlines()[0]
    evt = json.loads(line)
    assert "event_id" in evt and "provenance" in evt
