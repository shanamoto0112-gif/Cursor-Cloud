# GitHub リポジトリ作成 & push 手順

`gh` CLI がない環境向け。Cursor に任せても OK。

## 方法 A: Cursor に任せる（推奨）

チャットで以下を送信:

> GitHub に cursor-cloud リポジトリを作ってプッシュして

（Cursor 設定 → Integrations → GitHub 連携が必要）

## 方法 B: ブラウザで手動

1. https://github.com/new を開く
2. Repository name: `cursor-cloud`
3. **Public**、README 等は追加しない（空のリポジトリ）
4. Create repository
5. PowerShell で実行:

```powershell
cd C:\Users\user\dev\Cursor-Cloud
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/cursor-cloud.git
git push -u origin main
```

`YOUR_USERNAME` を自分の GitHub ユーザー名に置き換える。

## push 後: Cloud Agent 起動

1. [cursor.com/agents](https://cursor.com/agents) または Cursor Desktop で **Cloud** を選択
2. リポジトリ `cursor-cloud` を選択
3. [cloud-agent-mission-v1.1.md](cloud-agent-mission-v1.1.md) の依頼文を貼り付け

---

## 確認

```powershell
git remote -v
# origin  https://github.com/YOUR_USERNAME/cursor-cloud.git が表示されれば OK
```
