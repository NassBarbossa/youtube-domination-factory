import json
import os
import tempfile
import pytest
from json_io import read_json, write_json

def test_read_json_valid_file(tmp_path):
    f = tmp_path / "test.json"
    f.write_text('{"key": "value"}')
    assert read_json(str(f)) == {"key": "value"}

def test_read_json_missing_file_returns_default(tmp_path):
    result = read_json(str(tmp_path / "missing.json"), default={"items": []})
    assert result == {"items": []}

def test_read_json_corrupted_file_returns_default(tmp_path):
    f = tmp_path / "bad.json"
    f.write_text("not json {{{")
    result = read_json(str(f), default={"items": []})
    assert result == {"items": []}

def test_write_json_creates_file(tmp_path):
    path = str(tmp_path / "out.json")
    write_json(path, {"key": "value"})
    with open(path) as f:
        assert json.load(f) == {"key": "value"}

def test_write_json_atomic_no_corruption_on_existing(tmp_path):
    path = str(tmp_path / "out.json")
    write_json(path, {"original": True})
    write_json(path, {"updated": True})
    with open(path) as f:
        assert json.load(f) == {"updated": True}

def test_write_json_creates_parent_dirs(tmp_path):
    path = str(tmp_path / "sub" / "dir" / "out.json")
    write_json(path, {"nested": True})
    with open(path) as f:
        assert json.load(f) == {"nested": True}
