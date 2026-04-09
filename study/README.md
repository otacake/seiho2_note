# Study Workspace

`study/` は、第I部向けの学習カード、Anki エクスポート、coverage 台帳を置く本体ディレクトリです。

## ディレクトリ構成

- `first_part/`
  - 第I部カード本体
- `anki/exports/`
  - Anki 取り込み用 TSV
- `coverage/`
  - canonical 台帳と再生成物の説明

## first_part の書式

各カードは次の形にそろえます。

```markdown
## CARD FP-XXX-0001

- source: H26-2; note
- tags: first_part ...
- priority: A

### 問題
...

### ざっくり説明
...

### 要するに何か
...

### 問題意識
...

### 基準答案
...
```

- `問題` `要するに何か` `問題意識` `基準答案` は必須
- `ざっくり説明` `詳細説明` `Anki穴埋め` は任意
- 章ファイル名は `02-06_ソルベンシー.md` のように `scope_key_章名.md` で置くと coverage 側と突合しやすい

## 基本方針

- 第I部は `ワークブック + 過去問 + 補助メモ` を単元別に再編し、問題と基準答案を 1 対 1 で管理する
- 丸暗記前提でも、`要するに何を聞いているか` と `なぜその論点が必要か` は別欄に置く
- Anki は `問題を見て基準答案を再生する` 使い方を前提に設計する

## 再生成手順

```powershell
python scripts/build_problem_inventory.py
python scripts/export_anki_first_part.py
```

2026-04-10 時点では、`first_part_cards.tsv` に `171` 枚、`first_part_cloze.tsv` に `15` 枚が出力されています。
