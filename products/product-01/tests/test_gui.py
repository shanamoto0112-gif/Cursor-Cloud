import tkinter as tk

from dedupcsv.gui import duplicate_stat_color, resolve_key_columns


def test_resolve_key_columns_empty_means_all():
  assert resolve_key_columns([]) is None


def test_resolve_key_columns_with_selection():
  assert resolve_key_columns(["得意先コード", "得意先ｻﾌﾞｺｰﾄﾞ"]) == [
    "得意先コード",
    "得意先ｻﾌﾞｺｰﾄﾞ",
  ]


def test_duplicate_stat_color():
  assert duplicate_stat_color(0) == "#34C759"
  assert duplicate_stat_color(5) == "#FF9500"


def test_gui_module_imports():
  from dedupcsv.gui import get_font_family, make_font, resolve_key_columns

  assert resolve_key_columns([]) is None
  root = tk.Tk()
  root.withdraw()
  assert get_font_family()
  assert make_font(12)
  root.destroy()
