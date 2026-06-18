"""Core deduplication logic."""

from __future__ import annotations

import csv
import io
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, TextIO


ENCODINGS_TO_TRY = ("utf-8-sig", "utf-8", "cp932", "shift_jis")


@dataclass
class DedupeResult:
    input_rows: int
    output_rows: int
    duplicates_removed: int
    encoding: str


class DedupeError(Exception):
    """User-facing deduplication error."""


def detect_encoding(path: Path) -> str:
  raw = path.read_bytes()
  if raw.startswith(b"\xef\xbb\xbf"):
    return "utf-8-sig"
  for encoding in ("utf-8", "cp932", "shift_jis"):
    try:
      raw.decode(encoding)
      return encoding
    except UnicodeDecodeError:
      continue
  raise DedupeError(
    "ファイルの文字コードを判別できませんでした。"
    "UTF-8 または Shift_JIS (CP932) で保存してください。"
  )


def _normalize_cell(value: str | None) -> str:
  if value is None:
    return ""
  return value.strip()


def _row_key(row: dict[str, str], key_columns: list[str] | None) -> tuple[str, ...]:
  if key_columns:
    return tuple(_normalize_cell(row.get(col)) for col in key_columns)
  return tuple(_normalize_cell(v) for v in row.values())


def dedupe_rows(
  rows: Iterable[dict[str, str]],
  *,
  key_columns: list[str] | None = None,
  keep: str = "first",
) -> list[dict[str, str]]:
  if keep not in {"first", "last"}:
    raise DedupeError("keep は first または last を指定してください。")

  seen: dict[tuple[str, ...], dict[str, str]] = {}
  order: list[tuple[str, ...]] = []

  for row in rows:
    key = _row_key(row, key_columns)
    if keep == "first":
      if key not in seen:
        seen[key] = row
        order.append(key)
    else:
      if key in seen:
        order.remove(key)
      seen[key] = row
      if key not in order:
        order.append(key)

  return [seen[key] for key in order]


def read_csv(path: Path, encoding: str | None = None) -> tuple[list[dict[str, str]], str, list[str]]:
  chosen = encoding or detect_encoding(path)
  text = path.read_text(encoding=chosen)
  if not text.strip():
    raise DedupeError("CSV ファイルが空です。")

  reader = csv.DictReader(io.StringIO(text))
  if reader.fieldnames is None:
    raise DedupeError("CSV にヘッダー行がありません。")

  fieldnames = list(reader.fieldnames)
  rows = list(reader)
  return rows, chosen, fieldnames


def write_csv(
  path: Path,
  rows: list[dict[str, str]],
  fieldnames: list[str],
  encoding: str,
) -> None:
  path.parent.mkdir(parents=True, exist_ok=True)
  with path.open("w", encoding=encoding, newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)


def dedupe_file(
  input_path: Path,
  output_path: Path,
  *,
  key_columns: list[str] | None = None,
  keep: str = "first",
  encoding: str | None = None,
  dry_run: bool = False,
) -> DedupeResult:
  if not input_path.exists():
    raise DedupeError(f"入力ファイルが見つかりません: {input_path}")

  rows, chosen_encoding, fieldnames = read_csv(input_path, encoding)

  if key_columns:
    missing = [col for col in key_columns if col not in fieldnames]
    if missing:
      raise DedupeError(
        "指定したキー列が見つかりません: "
        + ", ".join(missing)
        + f"\n利用可能な列: {', '.join(fieldnames)}"
      )

  deduped = dedupe_rows(rows, key_columns=key_columns, keep=keep)
  if not dry_run:
    write_csv(output_path, deduped, fieldnames, chosen_encoding)

  return DedupeResult(
    input_rows=len(rows),
    output_rows=len(deduped),
    duplicates_removed=len(rows) - len(deduped),
    encoding=chosen_encoding,
  )


def dedupe_stream(
  input_handle: TextIO,
  output_handle: TextIO,
  *,
  key_columns: list[str] | None = None,
  keep: str = "first",
  encoding: str = "utf-8",
) -> DedupeResult:
  reader = csv.DictReader(input_handle)
  if reader.fieldnames is None:
    raise DedupeError("CSV にヘッダー行がありません。")

  fieldnames = list(reader.fieldnames)
  rows = list(reader)
  deduped = dedupe_rows(rows, key_columns=key_columns, keep=keep)

  writer = csv.DictWriter(output_handle, fieldnames=fieldnames)
  writer.writeheader()
  writer.writerows(deduped)

  return DedupeResult(
    input_rows=len(rows),
    output_rows=len(deduped),
    duplicates_removed=len(rows) - len(deduped),
    encoding=encoding,
  )
