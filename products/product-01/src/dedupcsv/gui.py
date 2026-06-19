"""Mac-inspired GUI for DedupeCSV."""

from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox

import customtkinter as ctk

from dedupcsv import __version__
from dedupcsv.core import DedupeError, DedupeResult, dedupe_file, read_csv

# Mac-like light palette
BG = "#F5F5F7"
CARD = "#FFFFFF"
ACCENT = "#007AFF"
ACCENT_HOVER = "#0066D6"
TEXT = "#1D1D1F"
TEXT_SECONDARY = "#86868B"
BORDER = "#E5E5EA"
SUCCESS = "#34C759"
WARNING = "#FF9500"
FONT_FAMILY = "Segoe UI"


def resolve_key_columns(selected: list[str]) -> list[str] | None:
  """Return selected columns, or None when all columns should be used."""
  return selected if selected else None


def duplicate_stat_color(duplicates_removed: int) -> str:
  if duplicates_removed == 0:
    return SUCCESS
  return WARNING


class Card(ctk.CTkFrame):
  def __init__(self, master: ctk.CTk, title: str, **kwargs) -> None:
    super().__init__(
      master,
      fg_color=CARD,
      corner_radius=12,
      border_width=1,
      border_color=BORDER,
      **kwargs,
    )
    self.grid_columnconfigure(0, weight=1)
    self._title = ctk.CTkLabel(
      self,
      text=title,
      font=ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold"),
      text_color=TEXT,
      anchor="w",
    )
    self._title.grid(row=0, column=0, sticky="w", padx=20, pady=(16, 8))


class DedupeApp(ctk.CTk):
  def __init__(self) -> None:
    super().__init__()
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    self.title(f"DedupeCSV v{__version__}")
    self.geometry("720x780")
    self.minsize(640, 700)
    self.configure(fg_color=BG)

    self._input_path: Path | None = None
    self._encoding: str | None = None
    self._column_vars: dict[str, tk.BooleanVar] = {}
    self._keep_var = tk.StringVar(value="first")

    self._build_layout()

  def _build_layout(self) -> None:
    self.grid_columnconfigure(0, weight=1)
    self.grid_rowconfigure(4, weight=1)

    header = ctk.CTkFrame(self, fg_color=BG)
    header.grid(row=0, column=0, sticky="ew", padx=28, pady=(24, 8))
    header.grid_columnconfigure(0, weight=1)

    ctk.CTkLabel(
      header,
      text="DedupeCSV",
      font=ctk.CTkFont(family=FONT_FAMILY, size=28, weight="bold"),
      text_color=TEXT,
      anchor="w",
    ).grid(row=0, column=0, sticky="w")
    ctk.CTkLabel(
      header,
      text="CSV の重複行を除去 — オフライン・安全",
      font=ctk.CTkFont(family=FONT_FAMILY, size=14),
      text_color=TEXT_SECONDARY,
      anchor="w",
    ).grid(row=1, column=0, sticky="w", pady=(4, 0))

    file_card = Card(self, "1. CSV を選ぶ")
    file_card.grid(row=1, column=0, sticky="ew", padx=28, pady=(8, 8))

    self._file_label = ctk.CTkLabel(
      file_card,
      text="ファイルが選択されていません",
      font=ctk.CTkFont(family=FONT_FAMILY, size=14),
      text_color=TEXT_SECONDARY,
      anchor="w",
      wraplength=560,
      justify="left",
    )
    self._file_label.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 12))

    ctk.CTkButton(
      file_card,
      text="ファイルを選ぶ",
      command=self._pick_file,
      fg_color=ACCENT,
      hover_color=ACCENT_HOVER,
      text_color="#FFFFFF",
      corner_radius=10,
      height=40,
      font=ctk.CTkFont(family=FONT_FAMILY, size=14, weight="bold"),
    ).grid(row=2, column=0, sticky="w", padx=20, pady=(0, 16))

    columns_card = Card(self, "2. 重複判定に使う列")
    columns_card.grid(row=2, column=0, sticky="ew", padx=28, pady=(0, 8))
    columns_card.grid_rowconfigure(2, weight=1)

    ctk.CTkLabel(
      columns_card,
      text="未選択の場合は全列で判定します",
      font=ctk.CTkFont(family=FONT_FAMILY, size=12),
      text_color=TEXT_SECONDARY,
      anchor="w",
    ).grid(row=1, column=0, sticky="w", padx=20, pady=(0, 8))

    self._columns_frame = ctk.CTkScrollableFrame(
      columns_card,
      fg_color="#FAFAFA",
      corner_radius=8,
      height=180,
      label_text="",
    )
    self._columns_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 12))
    self._columns_frame.grid_columnconfigure(0, weight=1)

    self._columns_placeholder = ctk.CTkLabel(
      self._columns_frame,
      text="CSV を選ぶと列名が表示されます",
      font=ctk.CTkFont(family=FONT_FAMILY, size=13),
      text_color=TEXT_SECONDARY,
      anchor="w",
    )
    self._columns_placeholder.grid(row=0, column=0, sticky="w", padx=8, pady=8)

    keep_card = Card(self, "3. 残す行")
    keep_card.grid(row=3, column=0, sticky="ew", padx=28, pady=(0, 8))

    keep_row = ctk.CTkFrame(keep_card, fg_color="transparent")
    keep_row.grid(row=1, column=0, sticky="w", padx=20, pady=(0, 16))

    ctk.CTkRadioButton(
      keep_row,
      text="最初の行を残す",
      variable=self._keep_var,
      value="first",
      font=ctk.CTkFont(family=FONT_FAMILY, size=14),
      text_color=TEXT,
      fg_color=ACCENT,
      hover_color=ACCENT_HOVER,
    ).pack(side="left", padx=(0, 24))
    ctk.CTkRadioButton(
      keep_row,
      text="最後の行を残す",
      variable=self._keep_var,
      value="last",
      font=ctk.CTkFont(family=FONT_FAMILY, size=14),
      text_color=TEXT,
      fg_color=ACCENT,
      hover_color=ACCENT_HOVER,
    ).pack(side="left")

    preview_card = Card(self, "4. 結果プレビュー")
    preview_card.grid(row=4, column=0, sticky="nsew", padx=28, pady=(0, 8))

    stats = ctk.CTkFrame(preview_card, fg_color="transparent")
    stats.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 16))
    stats.grid_columnconfigure((0, 1, 2), weight=1)

    self._input_stat = self._make_stat(stats, "入力行数", "—", 0)
    self._duplicate_stat = self._make_stat(stats, "削除する重複", "—", 1, large=True)
    self._output_stat = self._make_stat(stats, "残る行数", "—", 2)

    self._meta_label = ctk.CTkLabel(
      preview_card,
      text="「プレビュー」で件数を確認できます",
      font=ctk.CTkFont(family=FONT_FAMILY, size=12),
      text_color=TEXT_SECONDARY,
      anchor="w",
    )
    self._meta_label.grid(row=2, column=0, sticky="w", padx=20, pady=(0, 16))

    actions = ctk.CTkFrame(self, fg_color=BG)
    actions.grid(row=5, column=0, sticky="ew", padx=28, pady=(0, 24))
    actions.grid_columnconfigure((0, 1), weight=1)

    ctk.CTkButton(
      actions,
      text="プレビュー",
      command=self._preview,
      fg_color="#E5E5EA",
      hover_color="#D1D1D6",
      text_color=TEXT,
      corner_radius=10,
      height=44,
      font=ctk.CTkFont(family=FONT_FAMILY, size=15, weight="bold"),
    ).grid(row=0, column=0, sticky="ew", padx=(0, 8))

    ctk.CTkButton(
      actions,
      text="実行して保存",
      command=self._run,
      fg_color=ACCENT,
      hover_color=ACCENT_HOVER,
      text_color="#FFFFFF",
      corner_radius=10,
      height=44,
      font=ctk.CTkFont(family=FONT_FAMILY, size=15, weight="bold"),
    ).grid(row=0, column=1, sticky="ew", padx=(8, 0))

  def _make_stat(
    self,
    parent: ctk.CTkFrame,
    label: str,
    value: str,
    column: int,
    *,
    large: bool = False,
  ) -> ctk.CTkLabel:
    box = ctk.CTkFrame(parent, fg_color="#FAFAFA", corner_radius=10)
    box.grid(row=0, column=column, sticky="nsew", padx=4)
    ctk.CTkLabel(
      box,
      text=label,
      font=ctk.CTkFont(family=FONT_FAMILY, size=12),
      text_color=TEXT_SECONDARY,
    ).pack(padx=12, pady=(12, 4))
    value_label = ctk.CTkLabel(
      box,
      text=value,
      font=ctk.CTkFont(family=FONT_FAMILY, size=32 if large else 24, weight="bold"),
      text_color=TEXT,
    )
    value_label.pack(padx=12, pady=(0, 12))
    return value_label

  def _pick_file(self) -> None:
    path = filedialog.askopenfilename(
      title="CSV ファイルを選ぶ",
      filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
    )
    if not path:
      return

    self._load_file(Path(path))

  def _load_file(self, path: Path) -> None:
    try:
      _rows, encoding, fieldnames = read_csv(path)
    except DedupeError as exc:
      messagebox.showerror("エラー", str(exc))
      return

    self._input_path = path
    self._encoding = encoding
    self._file_label.configure(text=str(path), text_color=TEXT)
    self._populate_columns(fieldnames)
    self._clear_preview()

  def _populate_columns(self, fieldnames: list[str]) -> None:
    for child in self._columns_frame.winfo_children():
      child.destroy()

    self._column_vars.clear()
    for index, name in enumerate(fieldnames):
      var = tk.BooleanVar(value=False)
      self._column_vars[name] = var
      ctk.CTkCheckBox(
        self._columns_frame,
        text=name,
        variable=var,
        font=ctk.CTkFont(family=FONT_FAMILY, size=13),
        text_color=TEXT,
        fg_color=ACCENT,
        hover_color=ACCENT_HOVER,
        border_color=BORDER,
        corner_radius=6,
      ).grid(row=index, column=0, sticky="w", padx=8, pady=4)

  def _selected_columns(self) -> list[str]:
    return [name for name, var in self._column_vars.items() if var.get()]

  def _require_input(self) -> Path | None:
    if self._input_path is None:
      messagebox.showwarning("CSV 未選択", "先に CSV ファイルを選んでください。")
      return None
    return self._input_path

  def _run_dedupe(self, output_path: Path, *, dry_run: bool) -> DedupeResult | None:
    input_path = self._require_input()
    if input_path is None:
      return None

    try:
      return dedupe_file(
        input_path,
        output_path,
        key_columns=resolve_key_columns(self._selected_columns()),
        keep=self._keep_var.get(),
        dry_run=dry_run,
      )
    except DedupeError as exc:
      messagebox.showerror("エラー", str(exc))
      return None

  def _update_preview(self, result: DedupeResult, *, dry_run: bool) -> None:
    self._input_stat.configure(text=f"{result.input_rows:,}")
    self._output_stat.configure(text=f"{result.output_rows:,}")
    self._duplicate_stat.configure(
      text=f"{result.duplicates_removed:,}",
      text_color=duplicate_stat_color(result.duplicates_removed),
    )
    mode = "プレビュー（ファイルは作成しません）" if dry_run else "保存完了"
    self._meta_label.configure(
      text=f"{mode} · 文字コード: {result.encoding}",
      text_color=TEXT_SECONDARY,
    )

  def _clear_preview(self) -> None:
    self._input_stat.configure(text="—", text_color=TEXT)
    self._output_stat.configure(text="—", text_color=TEXT)
    self._duplicate_stat.configure(text="—", text_color=TEXT)
    self._meta_label.configure(text="「プレビュー」で件数を確認できます")

  def _preview(self) -> None:
    result = self._run_dedupe(Path("_preview_placeholder.csv"), dry_run=True)
    if result is not None:
      self._update_preview(result, dry_run=True)

  def _run(self) -> None:
    if self._require_input() is None:
      return

    default_name = f"{self._input_path.stem}_重複除去.csv"
    output_path = filedialog.asksaveasfilename(
      title="保存先を選ぶ",
      defaultextension=".csv",
      initialfile=default_name,
      filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
    )
    if not output_path:
      return

    result = self._run_dedupe(Path(output_path), dry_run=False)
    if result is not None:
      self._update_preview(result, dry_run=False)
      messagebox.showinfo(
        "完了",
        f"重複 {result.duplicates_removed:,} 件を除去しました。\n\n{output_path}",
      )


def main() -> None:
  app = DedupeApp()
  app.mainloop()


if __name__ == "__main__":
  main()
