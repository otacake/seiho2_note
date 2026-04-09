# 2026-04-10 inventory / first_part / docs 作業ログ

## 目的

- 優先順位 `1. 台帳の信頼性改善 -> 2. 未整備章の first_part 追加 -> 3. README/運用導線更新` で作業する
- 作業の途中経過、判断、残課題をこのログで追えるようにする

## ブランチ

- 作業開始ブランチ: `codex/inventory-firstpart-docs`

## 進捗

### 1. 台帳の信頼性改善

- `scripts/build_problem_inventory.py` を修正
  - `study/first_part` 側のファイル名差分 (`02-04_リスク管理_ALM.md` など) を吸収するため、scope をファイル名そのものではなく `02-04` のようなキーで突合するよう変更
  - タイトル突合に `body_norm` と `SequenceMatcher` を併用し、表記ゆれや長い注記付きタイトルでも drafted 判定しやすくした
  - OCR 断片として扱うべき `確認事項に追加`、`ことを重視している。` を除外対象に追加
  - `めっちゃ長い` のような注記語もタイトル正規化で落とすよう変更
- 再生成結果
  - 変更前: `drafted=102 / missing=82 / excluded=8`
  - 変更後: `drafted=123 / missing=59 / excluded=10`
- 章別の改善
  - `横断 リスク管理・ALM`: `drafted 0 -> 12`
  - `保険2第1章 生命保険会計`: `drafted 56 -> 65`
  - `生命保険会社の保険計理人の職務`: OCR 断片 2 件を `excluded` 扱いへ整理

## 現時点の残タスク

- `study/first_part` の未作成章
  - `02-06 ソルベンシー`
  - `02-07 内部管理会計・区分経理`
  - `02-08 相互会社と株式会社`
  - `生命保険会社の保険計理人の職務` の配当以外
- `README` / `study/README` / `study/coverage/README` の現況反映
- 台帳上まだ `missing` のまま残っている chapter 1 / RM の一部論点は、必要ならカード追加かタイトル調整で吸収する

