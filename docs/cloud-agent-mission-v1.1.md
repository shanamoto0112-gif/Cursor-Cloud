# Cloud Agent ミッション — DedupeCSV v1.1

**前提**: v1.0 はローカル Agent で完成済み。Cloud Agent 体験用に **v1.1 をクラウドで実装** する。

---

## 依頼文（Cloud 起動時にコピペ）

```
リポジトリの products/product-01（DedupeCSV）の v1.1 を実装してください。

## 必須タスク
1. `--dry-run` オプション追加（出力ファイルを書かず、削除件数だけ表示）
2. GitHub Actions で pytest を CI 実行（.github/workflows/test.yml）
3. README に「スクリーンショット撮影手順」セクションを追記
4. 全テストパスを確認
5. 完了したら PR を作成（タイトル: feat: DedupeCSV v1.1 dry-run and CI）

## 制約
- 既存の CLI インターフェースを壊さない
- オフライン動作を維持（外部 API なし）
```

---

## 社長の操作（Cloud 起動前）

1. **GitHub に push**（下記スクリプト or Cursor に「プッシュして」）
2. Cursor エージェント入力欄で **Cloud** を選択
3. 上の依頼文を貼り付けて起動
4. PC を閉じても OK — 完了通知を待つ
5. 戻ったら PR を確認・マージ

---

## なぜ v1.0 で Cloud を使わなかったか

ローカル Agent が cloud-polish（テスト・exe・zip）まで実施したため。
プランの意図どおり **「push → Cloud → PR」** を体験するには、**未完了の v1.1 を Cloud に任せる** のが正しい流れ。
