from pathlib import Path

from dedupcsv.core import dedupe_file


def test_dedupe_file_dry_run_skips_output(tmp_path: Path):
  input_path = tmp_path / "input.csv"
  output_path = tmp_path / "output.csv"
  input_path.write_text(
    "id,name\n1,Alice\n2,Bob\n1,Alice\n",
    encoding="utf-8",
  )

  result = dedupe_file(input_path, output_path, dry_run=True)

  assert result.input_rows == 3
  assert result.output_rows == 2
  assert result.duplicates_removed == 1
  assert not output_path.exists()


def test_dedupe_file_dry_run_with_keys(tmp_path: Path):
  input_path = tmp_path / "input.csv"
  output_path = tmp_path / "output.csv"
  input_path.write_text(
    "email,status\na@example.com,old\nb@example.com,active\na@example.com,new\n",
    encoding="utf-8",
  )

  result = dedupe_file(
    input_path,
    output_path,
    key_columns=["email"],
    keep="last",
    dry_run=True,
  )

  assert result.duplicates_removed == 1
  assert not output_path.exists()
