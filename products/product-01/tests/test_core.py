import csv
from pathlib import Path

import pytest

from dedupcsv.core import DedupeError, dedupe_file, dedupe_rows, detect_encoding


def test_dedupe_rows_all_columns_keep_first():
  rows = [
    {"id": "1", "name": "Alice"},
    {"id": "2", "name": "Bob"},
    {"id": "1", "name": "Alice"},
  ]
  result = dedupe_rows(rows, keep="first")
  assert len(result) == 2
  assert result[0]["id"] == "1"
  assert result[1]["id"] == "2"


def test_dedupe_rows_key_columns_keep_last():
  rows = [
    {"email": "a@example.com", "status": "old"},
    {"email": "b@example.com", "status": "active"},
    {"email": "a@example.com", "status": "new"},
  ]
  result = dedupe_rows(rows, key_columns=["email"], keep="last")
  assert len(result) == 2
  by_email = {row["email"]: row["status"] for row in result}
  assert by_email["a@example.com"] == "new"
  assert by_email["b@example.com"] == "active"


def test_dedupe_rows_trims_whitespace():
  rows = [
    {"name": " Alice "},
    {"name": "Alice"},
  ]
  result = dedupe_rows(rows, key_columns=["name"], keep="first")
  assert len(result) == 1


def test_dedupe_file_utf8(tmp_path: Path):
  input_path = tmp_path / "input.csv"
  output_path = tmp_path / "output.csv"
  input_path.write_text(
    "id,name\n1,Alice\n2,Bob\n1,Alice\n",
    encoding="utf-8-sig",
  )

  result = dedupe_file(input_path, output_path)
  assert result.input_rows == 3
  assert result.output_rows == 2
  assert result.duplicates_removed == 1
  assert output_path.read_text(encoding="utf-8-sig").count("\n") == 3


def test_dedupe_file_shift_jis(tmp_path: Path):
  input_path = tmp_path / "input.csv"
  output_path = tmp_path / "output.csv"
  input_path.write_text(
    "id,名前\n1,田中\n2,佐藤\n1,田中\n",
    encoding="cp932",
  )

  result = dedupe_file(input_path, output_path, key_columns=["id"])
  assert result.encoding == "cp932"
  assert result.output_rows == 2


def test_empty_file_raises(tmp_path: Path):
  input_path = tmp_path / "empty.csv"
  output_path = tmp_path / "out.csv"
  input_path.write_text("", encoding="utf-8")

  with pytest.raises(DedupeError, match="空"):
    dedupe_file(input_path, output_path)


def test_missing_key_column_raises(tmp_path: Path):
  input_path = tmp_path / "input.csv"
  output_path = tmp_path / "out.csv"
  input_path.write_text("id,name\n1,Alice\n", encoding="utf-8")

  with pytest.raises(DedupeError, match="キー列"):
    dedupe_file(input_path, output_path, key_columns=["email"])


def test_missing_input_raises(tmp_path: Path):
  with pytest.raises(DedupeError, match="見つかりません"):
    dedupe_file(tmp_path / "missing.csv", tmp_path / "out.csv")


def test_detect_encoding_utf8_sig(tmp_path: Path):
  path = tmp_path / "sample.csv"
  path.write_text("id\n1\n", encoding="utf-8-sig")
  assert detect_encoding(path) == "utf-8-sig"


def test_large_file_sample(tmp_path: Path):
  input_path = tmp_path / "large.csv"
  output_path = tmp_path / "large_out.csv"

  with input_path.open("w", encoding="utf-8", newline="") as handle:
    writer = csv.writer(handle)
    writer.writerow(["id", "value"])
    for i in range(1000):
      writer.writerow([str(i % 100), f"v{i}"])

  result = dedupe_file(input_path, output_path, key_columns=["id"], keep="last")
  assert result.input_rows == 1000
  assert result.output_rows == 100
  assert result.duplicates_removed == 900
