import pytest

from dedupcsv.core import DedupeError, dedupe_file, read_csv


def test_utf8_bom_header_only(tmp_path):
  path = tmp_path / "bom.csv"
  path.write_bytes(b"\xef\xbb\xbfid,name\n1,A\n")
  rows, encoding, fields = read_csv(path)
  assert encoding == "utf-8-sig"
  assert fields == ["id", "name"]
  assert len(rows) == 1


def test_whitespace_only_cells_deduped():
  from dedupcsv.core import dedupe_rows

  rows = [{"a": " ", "b": "x"}, {"a": "", "b": "x"}]
  result = dedupe_rows(rows, keep="first")
  assert len(result) == 1


def test_header_only_file(tmp_path):
  path = tmp_path / "header_only.csv"
  path.write_text("id,name\n", encoding="utf-8")
  out = tmp_path / "out.csv"
  result = dedupe_file(path, out)
  assert result.input_rows == 0
  assert result.output_rows == 0
  assert out.read_text(encoding="utf-8") == "id,name\n"


def test_invalid_keep_raises():
  from dedupcsv.core import dedupe_rows

  with pytest.raises(DedupeError, match="keep"):
    dedupe_rows([{"a": "1"}], keep="middle")
