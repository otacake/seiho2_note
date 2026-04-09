# Coverage

`coverage/` は、WB・ノート・`study/first_part` を突合して、`何を扱うべきか` と `どこまで drafted できたか` を見える化するための台帳置き場です。

## 生成物

- `canonical_problems.csv`
  - git 追跡する正本
- `problem_inventory.xlsx`
  - ローカル確認用の Excel 出力
  - `summary` `wb_raw` `notes_raw` `canonical` の 4 シートを持つ

## 実行方法

```powershell
python scripts/build_problem_inventory.py
```

## 前提

- `note/` 配下のローカル資料を参照する
- `pdftotext` が見つかる環境では、WB PDF のテキスト抽出も使う
- `study/first_part/` のファイル名は `02-07_...` のような `scope_key` 付きにしておくと突合が安定する

## canonical_problems.csv の主な列

- `canonical_id`
  - 統合問題 ID
- `chapter`
  - 単元
- `title`
  - 統合後の代表タイトル
- `source_refs`
  - 対応する過去問出典
- `origin`
  - `notes_only` / `wb_only` / `wb+notes`
- `note_file`
  - 対応するノートファイル
- `study_card_id`
  - 対応した `first_part` カード ID
- `match_reason`
  - `title` `ref` `similar` `excluded` など、突合理由
- `study_status`
  - `drafted` / `missing` / `excluded`
- `needs_web_lookup`
  - ローカル資料だけで不足しそうな場合の目印
- `answer_strategy`
  - 回答案出の優先順位

## 2026-04-10 時点の集計

- `drafted=171`
- `missing=11`
- `excluded=10`

今回の更新で、`保険2第6章` `保険2第7章` `保険2第8章` と `生命保険会社の保険計理人の職務` の残件は解消済みです。残件は chapter 1 と `横断 リスク管理・ALM` に限られます。
