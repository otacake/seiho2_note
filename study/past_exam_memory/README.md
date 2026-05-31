# 生保2 過去問丸暗記

このディレクトリは、WB と H23-2025 の過去問を単元別に並べ、原文ベースで白紙再現するための正本です。

## 使い方

1. `units/` で問題の意味と背景を確認する。
2. Anki の `whole` カードで、原問題だけを見て暗記答案を白紙再現する。
3. 長い答案は `chunk` カードで、観点・段落ごとに原文を固める。
4. `cloze` は数値、条文語句、列挙名、制度名だけに使う。

## 要約禁止ルール

- `暗記答案` は、公式解答例・WB・既存単元別Markdownの文言を原則保持する。
- 許可する加工は、OCRノイズ除去、ページヘッダ削除、改行・箇条書き整形、明らかな文字化け補正だけ。
- 意味説明、背景、言い換えは `units/` の `理解メモ` に置き、Anki の back へ混ぜない。

## 生成方法

```powershell
python scripts/build_past_exam_memory.py
python scripts/export_past_exam_memory_apkg.py
```

## 出力

- `past_exam_index.csv`: WB + H23-2025 の小中問台帳
- `units/*.md`: 単元別の原問題、暗記答案、理解メモ
- `cards/*.md`: Anki exporter 用カード
- `exports/生保2_過去問丸暗記.apkg`: 章別サブデッキ付き APKG
