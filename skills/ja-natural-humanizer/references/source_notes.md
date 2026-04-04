# 設計根拠メモ

この skill は、次の資料を踏まえて構成しています。

## 1. Zenn 記事
- m0370「AI生成文から『AIくささ』を取り除く技術と、Claude Codeスキルに組み込むまでの話」
- 日本語に移植しやすい論点として、16 項目のチェックリストが整理されている。
- humanizer_academic 由来の 10 項目と、blader/humanizer 由来の 6 項目を統合している。

## 2. Humanizer 系 skill
- blader/humanizer
  - Identify AI patterns
  - Rewrite problematic sections
  - Preserve meaning
  - Maintain voice
  - Add soul
  - Final anti-AI pass
- matsuikentaro1/humanizer_academic
  - 学術文脈向けに、過剰な意義づけ、AI頻出語彙、曖昧な出典、ダッシュ類などを具体化している

## 3. Codex の現在の skill 仕様
- SKILL.md の YAML frontmatter に `name` と `description` が必要
- repo では `.agents/skills` が自動検出の対象
- `AGENTS.md` は作業前に読まれるため、「このskills使って」のような依頼をローカル skill に結びつける導線として有効

## 4. 日本語の骨格
- 一文一義
- 早い位置に必要情報を置く
- 箇条書きに頼りすぎない
- 名詞の連結を増やしすぎず、動詞で言い切る
- 略語は初出で定義する

## 5. この skill で意識していること
- 「人間らしさ」を雑さで代用しない
- 直訳調、テンプレ調、チャットボット残留表現を減らす
- 媒体に応じて温度を変える
- ユーザーの文体サンプルがある場合は、それを優先する
