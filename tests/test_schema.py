import pathlib


def test_schemas_exist():
    assert pathlib.Path("config/schema/event.schema.json").exists()
    assert pathlib.Path("config/schema/anomaly.schema.json").exists()
