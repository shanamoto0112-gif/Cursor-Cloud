# QA チェックリスト — DedupeCSV v1.0

**日付**: 2026-06-18  
**バージョン**: 1.0.0

---

## 自動テスト

- [x] pytest 全件パス（14 tests）
- [x] UTF-8 / UTF-8-BOM / Shift_JIS
- [x] 空ファイル・欠損キー列・欠損入力ファイル
- [x] 大量行（1000行 → 100ユニーク）

## 手動確認（社長向け）

- [x] `dedupcsv run tests/fixtures/sample.csv out.csv` で 3 行出力
- [x] `--keys email` でメール重複のみ除去
- [x] exe 版スモークテスト完了

## セキュリティ

- [x] ネットワーク通信なし（オフライン CLI）
- [x] 外部 API 呼び出しなし

## 配布物

- [x] `build.ps1` / PyInstaller で exe 生成
- [x] zip: exe + README + LICENSE + sample.csv（`package-release.ps1`）

## v1.0 判定

**ステータス**: v1.0 確定。Gumroad 公開は [marketing/launch-guide.md](../../marketing/launch-guide.md) に従い社長操作。
