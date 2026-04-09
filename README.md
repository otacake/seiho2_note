# seiho2

このリポジトリは、`生保2` の学習資産を育てるワークスペースであり、同時にローカル Codex skill も同居している作業用リポジトリです。

## 主要ディレクトリ

- `note/`
  - 単元別マークダウン、第一部分析、ローカル PDF など、元資料側の置き場
- `study/`
  - 第I部向けの `first_part` カード、Anki エクスポート、coverage 台帳
- `scripts/`
  - 台帳再生成、Anki エクスポートなどの補助スクリプト
- `ops/work_logs/`
  - 日付ごとの作業ログ
- `.agents/skills/ja-natural-humanizer/`
  - Codex の自動検出用 skill
- `skills/ja-natural-humanizer/`
  - 人が読みやすいように置いているミラー

## よく使うコマンド

```powershell
python scripts/build_problem_inventory.py
python scripts/export_anki_first_part.py
```

- `build_problem_inventory.py`
  - `note/` と `study/first_part/` を突合し、`study/coverage/canonical_problems.csv` と `study/coverage/problem_inventory.xlsx` を再生成する
- `export_anki_first_part.py`
  - `study/first_part/` を読み、`study/anki/exports/first_part_cards.tsv` と `study/anki/exports/first_part_cloze.tsv` を出力する

## 現在地

2026-04-10 時点の canonical 集計は次のとおりです。

- `drafted=171`
- `missing=11`
- `excluded=10`

今回の整備で、`保険2第6章 ソルベンシー`、`保険2第7章 内部管理会計・区分経理`、`保険2第8章 相互会社と株式会社`、`生命保険会社の保険計理人の職務` の残件は解消済みです。残件は chapter 1 と `横断 リスク管理・ALM` のみです。

## 作業の進め方

1. 作業開始時に `codex/...` ブランチを切る
2. `ops/work_logs/` に当日のログを作る
3. 必要な `study/first_part/` や `scripts/` を更新する
4. `python scripts/build_problem_inventory.py` と `python scripts/export_anki_first_part.py` を実行する
5. 生成結果と canonical の残件を確認して commit / push する

## skill について

このリポジトリには `ja-natural-humanizer` のローカル skill も置いてあります。Codex からは `.agents/skills/ja-natural-humanizer/` が自動検出され、`skills/ja-natural-humanizer/` は人向けのミラーです。
