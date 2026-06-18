# 進捗メモ — Cloud Agent 未使用について

**日時**: 2026-06-18  
**論点**: v1.0 はローカル Agent が cloud-polish まで完了。Cloud 体験は v1.1 で実施。

---

## 状況

| 項目 | 状態 |
|------|------|
| v1.0 MVP・テスト・exe・zip | ローカルで完了 |
| GitHub push | **未実施**（`gh auth login` が必要） |
| Cloud Agent | **未起動** |

## 正しい流れ（これから）

```
ローカルで v1.0 push → Cloud で v1.1 実装 → PR マージ
```

## 社長の次の3アクション

1. `gh auth login` または Cursor → Integrations → GitHub 連携
2. 「GitHub にプッシュして」と Cursor に依頼
3. Cloud 選択 + [cloud-agent-mission-v1.1.md](../docs/cloud-agent-mission-v1.1.md) の依頼文を貼る

## 決定

v1.1（dry-run、CI、README 追記）は **意図的に Cloud に残す**。
