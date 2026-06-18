# Gumroad 公開手順（社長向け）

所要時間: 約15分

## 1. 配布 zip を用意

```powershell
cd C:\Users\user\dev\Cursor-Cloud\products\product-01
.\package-release.ps1
```

生成物: `release/DedupeCSV-v1.0.0-win64.zip`

## 2. Gumroad アカウント

1. https://gumroad.com でサインアップ
2. Settings → Payouts で振込設定（販売前に必要）

## 3. 商品作成

1. **New Product** → **Digital Product**
2. **Name**: `DedupeCSV — CSV Duplicate Remover (Windows Offline)`
3. **Price**: `$19`
4. **Upload**: `DedupeCSV-v1.0.0-win64.zip`
5. **Description**: [marketing/gumroad-listing.md](../../marketing/gumroad-listing.md) の「商品説明」をコピペ
6. **Refund policy**: 14日以内全額返金
7. **Publish**

## 4. 営業（初週）

| 日 | アクション |
|----|-----------|
| Day 1 | X に投稿（文案は gumroad-listing.md） |
| Day 2 | note 記事公開 |
| Day 3 | 知人3人にレビュー依頼 |

## 5. GitHub（任意・クラウド Agent 用）

Cursor 設定 → Integrations → GitHub で連携後:

```powershell
cd C:\Users\user\dev\Cursor-Cloud
git commit -m "Initial release: DedupeCSV v1.0.0"
# GitHub でリポジトリ作成後 push
```

クラウド Agent は [docs/cloud-agent-handoff.md](../../docs/cloud-agent-handoff.md) を参照。
