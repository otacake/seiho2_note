# Anki エクスポート

## 目的

`study/first_part/` の Markdown を、Anki に取り込める TSV に変換する。

## 想定する学習フロー

1. Markdown で `問題 / ざっくり説明 / 要するに何か / 問題意識 / 詳細説明 / 基準答案` を管理する
2. 条文や係数表など `穴埋め向き` のカードは、必要に応じて `### Anki穴埋め` を追加する
3. スクリプトで TSV に出力する
4. Anki では `Basic` と `Cloze` を使い分ける

## 実行方法

```powershell
python scripts/export_anki_first_part.py
```

出力先:

- `study/anki/exports/first_part_cards.tsv`
- `study/anki/exports/first_part_cloze.tsv`

## Basic TSV の列

1. `id`
2. `source`
3. `tags`
4. `front`
5. `back`

## Cloze TSV の列

1. `id`
2. `source`
3. `tags`
4. `text`

## Anki 取り込み時の想定

- `first_part_cards.tsv`
  ノートタイプ: Basic もしくは自作の 5 フィールド型
- `first_part_cloze.tsv`
  ノートタイプ: Cloze
- `id` は重複管理用、`source` と `tags` は検索用

## Front / Back の中身

- `front`
  問題文のみ

- `back`
  問題文
  `ざっくり説明` (ある場合)
  `要するに何か`
  `問題意識`
  `詳細説明`
  `基準答案`

したがって、反転後に `問題と解答が両方見える` 形になる。

## `Anki穴埋め` の書き方

Markdown カードに次のような節を追加すると、Cloze 用 TSV に出力される。

```md
### Anki穴埋め
支払備金として積立を要求されるのは、{{c1::既発生未払}} と {{c2::IBNR}} である。
```

運用ルール:

- 条文列挙
- 係数表
- 穴埋め年度差
- 完全文暗唱より `空欄再生` が効くもの

こういうカードを優先して `Anki穴埋め` に回す。
