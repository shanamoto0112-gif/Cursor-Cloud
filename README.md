# Cursor-Cloud

1人社長 × Cursor によるツール販売スタートアップ体験プロジェクト。

## 構成

```
research/     # 市場リサーチブリーフ
decisions/    # 商品・価格・チャネルの決定ログ
products/     # 販売ツール本体
minutes/      # 会議・進捗記録
marketing/    # 販売ページ文案・SNS投稿
```

## 初回商品

[products/product-01/](products/product-01/) — CSV重複除去ツール（DedupeCSV）

## 開発

```powershell
cd products/product-01
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -r requirements-dev.txt
pytest
python -m dedupcsv --help
```

## ライセンス

各プロダクト配下の LICENSE を参照。
