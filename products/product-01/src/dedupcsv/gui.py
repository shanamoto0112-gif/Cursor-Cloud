"""Mac-inspired GUI for DedupeCSV."""

from __future__ import annotations

import tkinter as tk
import tkinter.font as tkfont
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

WINDOW_FONT_CANDIDATES = (
  "Yu Gothic UI",
  "Meiryo UI",
  "MS UI Gothic",
  "Hiragino Sans",
  "Helvetica Neue",
  "Segoe UI",
)


def get_font_family() -> str:
  available = set(tkfont.families())
  for name in WINDOW_FONT_CANDIDATES:
    if name in available:
      return name
  return "TkDefaultFont"


def make_font(size: int, *, weight: str = "normal") -> ctk.CTkFont:
  return ctk.CTkFont(family=get_font_family(), size=size, weight=weight)


def resolve_key_columns(selected: list[str]) -> list[str] | None:
  """Return selected columns, or None when all columns should be used."""
  return selected if selected else None


def duplicate_stat_color(duplicates_removed: int) -> str:
  if duplicates_removed == 0:
    return SUCCESS
  return WARNING


class Card(ctk.CTkFrame):
  def __init__(self, master: ctk.CTkBaseClass, title: str, **kwargs) -> None:
    super().__init__(
      master,
      fg_color=CARD,
      corner_radius=12,
      border_width=1,
      border_color=BORDER,
      **kwargs,
    )
    self.grid_columnconfigure(0, weight=1)
    ctk.CTkLabel(
      self,
      text=title,
      font=make_font(13, weight="bold"),
      text_color=TEXT,
      anchor="w",
    ).grid(row=0, column=0, sticky="w", padx=20, pady=(16, 8))


class DedupeApp(ctk.CTk):
  def __init__(self) -> None:
    super().__init__()
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    self.title(f"DedupeCSV v{__version__}")
    self.geometry("760x720")
    self.minsize(680, 640)
    self.configure(fg_color=BG)

    self._input_path: Path | None = None
    self._encoding: str | None = None
    self._column_vars: dict[str, tk.BooleanVar] = {}
    self._keep_var = tk.StringVar(value="first")

    self._build_layout()

  def _build_layout(self) -> None:
    self.grid_columnconfigure(0, weight=1)
    self.grid_rowconfigure(1, weight=1)

    header = ctk.CTkFrame(self, fg_color=BG)
    header.grid(row=0, column=0, sticky="ew", padx=28, pady=(16, 4))
    header.grid_columnconfigure(0, weight=1)

    ctk.CTkLabel(
      header,
      text="DedupeCSV",
      font=make_font(24, weight="bold"),
      text_color=TEXT,
      anchor="w",
    ).grid(row=0, column=0, sticky="w")
    ctk.CTkLabel(
      header,
      text="CSV 重複行除去 (Remove Duplicate CSV Rows) — オフライン (Offline)",
      font=make_font(13),
      text_color=TEXT_SECONDARY,
      anchor="w",
    ).grid(row=1, column=0, sticky="w", pady=(2, 0))

    content = ctk.CTkFrame(self, fg_color=BG)
    content.grid(row=1, column=0, sticky="nsew", padx=28, pady=(0, 4))
    content.grid_columnconfigure(0, weight=1)
    content.grid_rowconfigure(1, weight=1)

    file_card = Card(content, "1. CSV を選ぶ (Select CSV)")
    file_card.grid(row=0, column=0, sticky="ew", pady=(0, 6))

    self._file_label = ctk.CTkLabel(
      file_card,
      text="ファイル未選択 (No file selected)",
      font=make_font(13),
      text_color=TEXT_SECONDARY,
      anchor="w",
      wraplength=620,
      justify="left",
    )
    self._file_label.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 8))

    ctk.CTkButton(
      file_card,
      text="ファイルを選ぶ (Choose File)",
      command=self._pick_file,
      fg_color=ACCENT,
      hover_color=ACCENT_HOVER,
      text_color="#FFFFFF",
      corner_radius=10,
      height=36,
      font=make_font(13, weight="bold"),
    ).grid(row=2, column=0, sticky="w", padx=20, pady=(0, 12))

    columns_card = Card(content, "2. 重複判定列 (Key Columns)")
    columns_card.grid(row=1, column=0, sticky="nsew", pady=(0, 6))
    columns_card.grid_columnconfigure(0, weight=1)
    columns_card.grid_rowconfigure(2, weight=1)

    ctk.CTkLabel(
      columns_card,
      text="未選択時は全列で判定 (Use all columns if none selected)",
      font=make_font(11),
      text_color=TEXT_SECONDARY,
      anchor="w",
    ).grid(row=1, column=0, sticky="w", padx=20, pady=(0, 6))

    self._columns_frame = ctk.CTkScrollableFrame(
      columns_card,
      fg_color="#FAFAFA",
      corner_radius=8,
      label_text="",
    )
    self._columns_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 12))
    self._columns_frame.grid_columnconfigure(0, weight=1)

    self._columns_placeholder = ctk.CTkLabel(
      self._columns_frame,
      text="CSV を選ぶと列名が表示されます (Columns appear after file selection)",
      font=make_font(12),
      text_color=TEXT_SECONDARY,
      anchor="w",
      wraplength=560,
      justify="left",
    )
    self._columns_placeholder.grid(row=0, column=0, sticky="w", padx=8, pady=8)

    keep_card = Card(content, "3. 残す行 (Keep Row)")
    keep_card.grid(row=2, column=0, sticky="ew")

    keep_row = ctk.CTkFrame(keep_card, fg_color="transparent")
    keep_row.grid(row=1, column=0, sticky="w", padx=20, pady=(0, 12))

    ctk.CTkRadioButton(
      keep_row,
      text="最初の行 (First)",
      variable=self._keep_var,
      value="first",
      font=make_font(13),
      text_color=TEXT,
      fg_color=ACCENT,
      hover_color=ACCENT_HOVER,
    ).pack(side="left", padx=(0, 24))
    ctk.CTkRadioButton(
      keep_row,
      text="最後の行 (Last)",
      variable=self._keep_var,
      value="last",
      font=make_font(13),
      text_color=TEXT,
      fg_color=ACCENT,
      hover_color=ACCENT_HOVER,
    ).pack(side="left")

    footer = ctk.CTkFrame(self, fg_color=BG)
    footer.grid(row=2, column=0, sticky="ew", padx=28, pady=(0, 16))
    footer.grid_columnconfigure(0, weight=1)

    preview_card = Card(footer, "4. 結果 (Preview)")
    preview_card.grid(row=0, column=0, sticky="ew", pady=(0, 8))

    stats = ctk.CTkFrame(preview_card, fg_color="transparent")
    stats.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 4))
    stats.grid_columnconfigure((0, 1, 2), weight=1)

    self._input_stat = self._make_stat(stats, "入力 / Input", "-", 0)
    self._duplicate_stat = self._make_stat(
      stats,
      "重複 / Duplicates",
      "-",
      1,
      highlight=True,
    )
    self._output_stat = self._make_stat(stats, "残り / Output", "-", 2)

    self._summary_label = ctk.CTkLabel(
      preview_card,
      text="",
      font=make_font(12, weight="bold"),
      text_color=TEXT,
      anchor="center",
      wraplength=640,
      justify="center",
    )
    self._summary_label.grid(row=2, column=0, sticky="ew", padx=16, pady=(0, 2))

    self._meta_label = ctk.CTkLabel(
      preview_card,
      text="プレビュー (Preview) で件数を確認",
      font=make_font(11),
      text_color=TEXT_SECONDARY,
      anchor="center",
      wraplength=640,
      justify="center",
    )
    self._meta_label.grid(row=3, column=0, sticky="ew", padx=16, pady=(0, 8))

    actions = ctk.CTkFrame(footer, fg_color=BG)
    actions.grid(row=1, column=0, sticky="ew")
    actions.grid_columnconfigure((0, 1), weight=1)

    ctk.CTkButton(
      actions,
      text="プレビュー (Preview)",
      command=self._preview,
      fg_color="#E5E5EA",
      hover_color="#D1D1D6",
      text_color=TEXT,
      corner_radius=10,
      height=40,
      font=make_font(14, weight="bold"),
    ).grid(row=0, column=0, sticky="ew", padx=(0, 8))

    ctk.CTkButton(
      actions,
      text="実行して保存 (Run & Save)",
      command=self._run,
      fg_color=ACCENT,
      hover_color=ACCENT_HOVER,
      text_color="#FFFFFF",
      corner_radius=10,
      height=40,
      font=make_font(14, weight="bold"),
    ).grid(row=0, column=1, sticky="ew", padx=(8, 0))

  def _make_stat(
    self,
    parent: ctk.CTkFrame,
    label: str,
    value: str,
    column: int,
    *,
    highlight: bool = False,
  ) -> ctk.CTkLabel:
    box = ctk.CTkFrame(parent, fg_color="#FAFAFA", corner_radius=8, height=68)
    box.grid(row=0, column=column, sticky="nsew", padx=3, pady=2)
    box.grid_propagate(False)
    box.grid_columnconfigure(0, weight=1)

    ctk.CTkLabel(
      box,
      text=label,
      font=make_font(10),
      text_color=TEXT_SECONDARY,
      anchor="center",
    ).pack(padx=6, pady=(6, 0))

    value_label = ctk.CTkLabel(
      box,
      text=value,
      font=make_font(22 if highlight else 18, weight="bold"),
      text_color=TEXT,
      anchor="center",
    )
    value_label.pack(padx=6, pady=(0, 6))
    return value_label

  def _pick_file(self) -> None:
    path = filedialog.askopenfilename(
      title="CSV ファイルを選ぶ (Select CSV File)",
      filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
    )
    if not path:
      return

    self._load_file(Path(path))

  def _load_file(self, path: Path) -> None:
    try:
      _rows, encoding, fieldnames = read_csv(path)
    except DedupeError as exc:
      messagebox.showerror("エラー (Error)", str(exc))
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
        font=make_font(13),
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
      messagebox.showwarning(
        "CSV 未選択 (No CSV Selected)",
        "先に CSV ファイルを選んでください。\nPlease select a CSV file first.",
      )
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
      messagebox.showerror("エラー (Error)", str(exc))
      return None

  def _format_count(self, value: int) -> str:
    return f"{value:,}"

  def _update_preview(self, result: DedupeResult, *, dry_run: bool) -> None:
    self._input_stat.configure(text=self._format_count(result.input_rows))
    self._output_stat.configure(text=self._format_count(result.output_rows))
    duplicate_color = duplicate_stat_color(result.duplicates_removed)
    self._duplicate_stat.configure(
      text=self._format_count(result.duplicates_removed),
      text_color=duplicate_color,
    )

    if result.duplicates_removed == 0:
      summary = "重複は見つかりませんでした (No duplicates found)"
    else:
      summary = (
        f"重複 {self._format_count(result.duplicates_removed)} 件を削除します "
        f"(Will remove {self._format_count(result.duplicates_removed)} duplicates)"
      )
    self._summary_label.configure(text=summary, text_color=duplicate_color)

    mode = "プレビュー (Preview)" if dry_run else "保存完了 (Saved)"
    self._meta_label.configure(
      text=f"{mode} · 文字コード (Encoding): {result.encoding}",
      text_color=TEXT_SECONDARY,
    )
    self.update_idletasks()

  def _clear_preview(self) -> None:
    self._input_stat.configure(text="-", text_color=TEXT)
    self._output_stat.configure(text="-", text_color=TEXT)
    self._duplicate_stat.configure(text="-", text_color=TEXT)
    self._summary_label.configure(text="")
    self._meta_label.configure(text="プレビュー (Preview) で件数を確認")

  def _preview(self) -> None:
    result = self._run_dedupe(Path("_preview_placeholder.csv"), dry_run=True)
    if result is not None:
      self._update_preview(result, dry_run=True)

  def _run(self) -> None:
    if self._require_input() is None:
      return

    default_name = f"{self._input_path.stem}_deduped.csv"
    output_path = filedialog.asksaveasfilename(
      title="保存先を選ぶ (Choose Save Location)",
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
        "完了 (Done)",
        (
          f"重複 {self._format_count(result.duplicates_removed)} 件を除去しました。\n"
          f"Removed {self._format_count(result.duplicates_removed)} duplicates.\n\n"
          f"{output_path}"
        ),
      )


def main() -> None:
  app = DedupeApp()
  app.mainloop()


if __name__ == "__main__":
  main()
