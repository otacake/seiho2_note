# 2026-04-11 coverage cleanup

## 目的
- `study/coverage/canonical_problems.csv` の `missing` のうち、実際にはカードが存在するものを解消する。
- OCR 断片や見出し残骸による偽論点を `excluded` として整理する。
- `study/first_part/02-01_生命保険会計.md` と coverage 台帳の対応を実態に合わせる。

## 実施内容
- `study/first_part/02-01_生命保険会計.md` に `FP-LA-0058` から `FP-LA-0065` を追加し、生命保険会計の未収載カードを補完した。
- `scripts/build_problem_inventory.py` に title override を追加し、以下の偽 missing を既存カードへ正しく結び付けた。
- `事業年度末責任準備金の積立方とその考え方①` -> `FP-LA-0021`
- `事業年度末責任準備金の積立方とその考え方②` -> `FP-LA-0022`
- `事業年度末責任準備金の積立方とその考え方③` -> `FP-LA-0023`
- `リスクと資本・必要資本要件に対するインプット項目` -> `FP-RM-0002`
- `ERM体制の「内部統制体制」について(COSO)` -> `FP-RM-0005`
- `各リスクを計測するモデル` -> `FP-RM-0006`
- OCR ノイズとして以下を `excluded` 判定へ追加した。
- `5.2 事業費`
- `・蔵銀枠（第 1 保険年度）：30 万円`
- `運用利回り          5%`
- `ス、全期チルメル式責任準備金 セ．危険準備金 ソ．貸倒引当金 タ．責任準備金`
- タイトル類似度の丸数字ブーストを削除し、本文に丸数字があるだけで誤マッチしにくいようにした。

## 確認結果
- `python scripts/build_problem_inventory.py` 実行済み。
- `study/coverage/canonical_problems.csv` を UTF-8 で確認した結果、集計は以下のとおり。
- `drafted = 178`
- `excluded = 14`
- `missing = 0`

## 補足
- 端末上では一部ファイルが文字化けして見えることがあるため、coverage 台帳の最終確認は UTF-8 明示で行った。
- `problem_inventory.xlsx` も同時に再生成済み。
