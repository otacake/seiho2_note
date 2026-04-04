# Coverage

WB とノートの問題一覧を統合し、`何を扱うべきか` と `どこまで対応したか` を証跡として残すための台帳。

## 生成物

- `problem_inventory.xlsx`
  - `summary`
  - `wb_raw`
  - `notes_raw`
  - `canonical`
- `canonical_problems.csv`

## 実行方法

```powershell
python scripts/build_problem_inventory.py
```

## canonical シートの見方

- `canonical_id`
  統合問題ID
- `chapter`
  単元
- `title`
  統合後の代表タイトル
- `source_refs`
  対応する過去問出典
- `origin`
  `notes_only` / `wb_only` / `wb+notes`
- `study_status`
  `drafted` / `missing`
- `answer_strategy`
  回答案出の優先順位
- `needs_web_lookup`
  ローカル資産だけで不足しそうな場合の目印
