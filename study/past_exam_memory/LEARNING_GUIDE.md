# 生保2 過去問丸暗記Anki 学習ガイド

このガイドは、`study/past_exam_memory/exports/生保2_過去問丸暗記.apkg` を Anki に取り込んだ後の使い方を固定するためのメモです。

## 結論

このデッキは、穴埋め暗記デッキではなく、過去問答案を白紙再現するためのデッキです。

使う順番は次のとおりです。

1. `whole` を主教材にする
2. `chunk` は長い答案の修理用に使う
3. `cloze` は数値・語句・列挙名の補助確認にだけ使う

## カード種別

### whole

原問題だけを見て、答案を白紙再現するカードです。

本番の小中問対策では、これを主に回します。頭の中だけで済ませず、紙かメモに答案の骨子を書いてから答えを見るのが基本です。

### chunk

長い答案を段落・観点ごとに分けたカードです。

最初から全件を回すものではありません。`whole` で2回以上 `Again` になったカード、または答案の流れが毎回崩れるカードだけ、該当する `chunk` で修理します。

### cloze

数値、制度名、条文語句、列挙名を抜く補助カードです。

答案本文を作る主役ではありません。最後に5分程度、抜け漏れ確認として使います。

## Ankiでの推奨フィルター

通常デッキをそのまま押しても使えますが、最初は `whole` だけを抽出して回すのが安全です。

Ankiで `ツール` -> `フィルターデッキを作成` を開き、検索欄に次を入れます。

```text
tag:past_exam_memory tag:whole (is:new OR is:due)
```

設定は次を推奨します。

- 件数: `9999`
- 並び順: 期日順、またはランダム
- 回答に基づいてカードを再スケジュール: ON

`chunk` を修理用に回す場合は、検索欄を次にします。

```text
tag:past_exam_memory tag:chunk (is:new OR is:due)
```

`cloze` を確認用に回す場合は、検索欄を次にします。

```text
tag:past_exam_memory tag:cloze (is:new OR is:due)
```

## 1日の進め方

1. まず復習カードを終わらせる
2. 新規 `whole` を8〜12枚だけ追加する
3. 各カードで答案骨子を書く
4. 答えを見て、厳しめに評価する
5. 崩れたカードだけ `chunk` で修理する
6. 最後に必要なら `cloze` を5分だけ見る

新規カードを増やしすぎないことが重要です。長文答案の白紙再現カードは重いので、最初から20枚以上入れると復習負荷が急に膨らみます。

## 評価基準

- `Again`: 何も出ない、または答案の流れが作れない
- `Hard`: 骨子は出たが、重要語句・列挙・順序が崩れた
- `Good`: だいたい再現できた
- `Easy`: ほぼ自動で再現できた

忘れたカードに `Hard` を押さないこと。忘れているなら `Again` にします。`Hard` は「思い出せたが重かった」場合だけに使います。

## 2週間の初動

### 1〜2週目

`whole` だけを回します。

目的は、答案を完璧にすることではなく、どの問題にどの答案が対応するかを身体に入れることです。

### 3週目

`whole` で落ちたカードだけ `chunk` を使って修理します。

長い答案を丸ごと眺めるのではなく、崩れた段落単位で再現できるようにします。

### 4週目以降

`whole` を中心に継続し、`cloze` で数値・語句・列挙を確認します。

## 単元の優先順

最初は次の順番で回します。

1. `01_生命保険会計`
2. `06_ソルベンシー`
3. `04_リスク管理_ALM_ストレステスト`
4. `03_契約者配当`
5. `05_事業費`
6. `07_内部管理会計_区分経理`
7. `08_相互会社と株式会社`
8. `90_計理人実務基準`

## 根拠メモ

読み直しよりも、自分で思い出す練習の方が長期保持に効きやすいです。特にこの試験では、答案を見て理解するだけでは足りず、問題文から答案を再現する力が必要になります。

参考にした研究・資料:

- Roediger & Karpicke (2006), Test-Enhanced Learning: Taking Memory Tests Improves Long-Term Retention
  - https://gwern.net/doc/psychology/spaced-repetition/2006-roediger.pdf
- Karpicke & Blunt (2011), Retrieval Practice Produces More Learning than Elaborative Studying with Concept Mapping
  - https://pubmed.ncbi.nlm.nih.gov/21252317/
- Dunlosky et al. (2013), Improving Students' Learning With Effective Learning Techniques
  - https://pubmed.ncbi.nlm.nih.gov/26173288/
- Anki Manual: Filtered Decks & Cramming
  - https://docs.ankiweb.net/filtered-decks.html
- Anki Manual: Searching
  - https://docs.ankiweb.net/searching.html
- Anki Manual: Deck Options
  - https://docs.ankiweb.net/deck-options.html
