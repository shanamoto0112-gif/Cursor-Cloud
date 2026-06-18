# DedupeCSV — CSV重複行除去ツール

Excel でリストを扱う前に、CSV の重複行を一瞬で除去する Windows 向け CLI ツールです。

## 特徴

- **オフライン動作** — データを外部に送信しません
- **日本語 CSV 対応** — UTF-8 / Shift_JIS (CP932) を自動判定
- **キー列指定** — メールアドレス列だけで重複判定など
- **大量ファイル対応** — 数千行の CSV も処理可能

## 使い方

### インストール（開発者向け）

```powershell
cd products/product-01
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -e .
```

### 基本コマンド

```powershell
# 全列が一致する行を除去（最初の行を残す）
dedupcsv run input.csv output.csv

# メール列だけで重複判定
dedupcsv run input.csv output.csv --keys email

# 最後の行を残す
dedupcsv run input.csv output.csv --keys id --keep last
```

### exe 版（配布用）

```powershell
pip install -r requirements-dev.txt
.\build.ps1
# dist\dedupcsv.exe が生成されます
```

```powershell
dist\dedupcsv.exe run input.csv output.csv --keys email
```

## オプション

| オプション | 説明 |
|-----------|------|
| `--keys`, `-k` | 重複判定に使う列名（カンマ区切り） |
| `--keep` | `first`（既定）または `last` |
| `--encoding`, `-e` | 文字コードを手動指定 |

## テスト

```powershell
pip install -r requirements-dev.txt
pytest -v
```

## ライセンス

MIT License — 詳細は [LICENSE](LICENSE)

## サポート

問題がある場合は購入元（Gumroad）からお問い合わせください。14日以内の返金に対応します。
