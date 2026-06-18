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

# 出力せず削除件数だけ確認（dry-run）
dedupcsv run input.csv output.csv --dry-run
dedupcsv run input.csv output.csv --keys email --dry-run
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
| `--dry-run` | 出力ファイルを書き込まず、削除件数だけ表示 |

## スクリーンショット撮影手順

Gumroad 商品ページや README 用に、CLI の実行結果をキャプチャする手順です。

### 1. サンプル CSV を用意

```powershell
cd products\product-01
Copy-Item tests\fixtures\sample.csv demo-input.csv
```

### 2. ターミナルでコマンドを実行

PowerShell のフォントサイズを 14〜16pt に設定し、ウィンドウ幅を 80 文字程度に調整します。

```powershell
# 通常実行（結果テーブル付き）
dedupcsv run demo-input.csv demo-output.csv --keys email

# dry-run（削除件数の確認のみ）
dedupcsv run demo-input.csv demo-output.csv --keys email --dry-run
```

### 3. スクリーンショットを撮る

**Windows 11**

1. `Win + Shift + S` で範囲選択キャプチャ
2. ターミナル全体（コマンド行 + 結果テーブル）を含める
3. クリップボードから画像編集ソフトに貼り付けて PNG で保存

**ファイル名の例**

- `screenshot-run.png` — 通常実行の結果
- `screenshot-dry-run.png` — dry-run の結果

### 4. 確認ポイント

- コマンド行が読めること
- 「削除した重複」の件数がはっきり見えること
- dry-run では「出力ファイルは作成しません」と表示されること
- 個人情報や本番データが写っていないこと（`demo-input.csv` などのサンプルを使用）

## テスト

```powershell
pip install -r requirements-dev.txt
pytest -v
```

## ライセンス

MIT License — 詳細は [LICENSE](LICENSE)

## サポート

問題がある場合は購入元（Gumroad）からお問い合わせください。14日以内の返金に対応します。
