"""CLI entry point."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from dedupcsv import __version__
from dedupcsv.core import DedupeError, dedupe_file

app = typer.Typer(
  name="dedupcsv",
  help="CSV の重複行を除去するオフライン CLI ツール",
  add_completion=False,
)
console = Console()


def _parse_columns(value: Optional[str]) -> list[str] | None:
  if not value:
    return None
  columns = [part.strip() for part in value.split(",") if part.strip()]
  return columns or None


@app.command()
def run(
  input: Path = typer.Argument(..., help="入力 CSV ファイル"),
  output: Path = typer.Argument(..., help="出力 CSV ファイル"),
  keys: Optional[str] = typer.Option(
    None,
    "--keys",
    "-k",
    help="重複判定に使う列名（カンマ区切り）。未指定時は全列",
  ),
  keep: str = typer.Option(
    "first",
    "--keep",
    help="first=最初の行を残す / last=最後の行を残す",
  ),
  encoding: Optional[str] = typer.Option(
    None,
    "--encoding",
    "-e",
    help="文字コード（未指定時は自動判定: UTF-8 / Shift_JIS）",
  ),
) -> None:
  """CSV ファイルから重複行を除去します。"""
  try:
    result = dedupe_file(
      input,
      output,
      key_columns=_parse_columns(keys),
      keep=keep,
      encoding=encoding,
    )
  except DedupeError as exc:
    console.print(f"[red]エラー:[/red] {exc}")
    raise typer.Exit(code=1) from exc

  table = Table(title="DedupeCSV 結果")
  table.add_column("項目")
  table.add_column("値", justify="right")
  table.add_row("入力行数", str(result.input_rows))
  table.add_row("出力行数", str(result.output_rows))
  table.add_row("削除した重複", str(result.duplicates_removed))
  table.add_row("文字コード", result.encoding)
  table.add_row("出力先", str(output))
  console.print(table)


@app.command()
def version() -> None:
  """バージョンを表示します。"""
  console.print(f"DedupeCSV v{__version__}")


def main() -> None:
  app()


if __name__ == "__main__":
  main()
