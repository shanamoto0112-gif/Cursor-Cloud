# クラウドエージェント引き継ぎメモ

push 後、クラウドエージェントに以下を依頼してください。

## 依頼文（コピー用）

> `products/product-01` の DedupeCSV に対して以下を実施してください:
> 1. pytest を全件パスすることを確認
> 2. エッジケース（BOM 付き UTF-8、空行のみ、不正 CSV）のテスト追加
> 3. README にスクリーンショット撮影手順を追記
> 4. `build.ps1` で exe ビルドが通ることを確認
> 5. `dist/` に配布用 zip（exe + README + LICENSE + sample.csv）を作成
> 6. 完了したら PR を作成

## ローカルで実施済み

- MVP コアロジック
- 基本テスト 10 件
- Gumroad 文案

## GitHub 接続（未実施時）

```powershell
cd C:\Users\user\dev\Cursor-Cloud
git init
git add .
git commit -m "Initial commit: DedupeCSV MVP and startup structure"
# GitHub でリポジトリ作成後:
git remote add origin https://github.com/YOUR_USER/cursor-cloud.git
git push -u origin main
```

Cursor 設定 → Integrations → GitHub から連携すると、クラウドエージェントがリポジトリをクローンできます。
