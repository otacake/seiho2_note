# Codex 用 日本語自然文 skill パック

このフォルダは、Codex で日本語の文章を自然に書いたり、既存文の AI くささを減らしたりするための skill パックです。

## フォルダ構成

- `.agents/skills/ja-natural-humanizer/`
  - Codex の自動検出用です。
- `skills/ja-natural-humanizer/`
  - 人が見やすいように同じ内容をミラーしています。
- `AGENTS.md`
  - 「このskills使って」と言ったときに、ローカル skill を優先して使わせるための導線です。

## そのままの使い方

このフォルダをリポジトリ直下に置いたまま Codex を起動し、次のように言います。

```text
このskills使って。以下の文章を、人が書いた感じの自然な日本語に直して。
```

あるいは、skill 名を明示しても構いません。

```text
ja-natural-humanizer を使って、次の社内文を自然な日本語に整えて。
```

## 補助ファイル

- `skills/ja-natural-humanizer/assets/input_template.md`
  - プロンプトに貼る入力欄
- `skills/ja-natural-humanizer/assets/textlintrc_natural_japanese.json`
  - textlint の叩き台
- `skills/ja-natural-humanizer/references/adapted_patterns.md`
  - 16 項目の詳細例
- `skills/ja-natural-humanizer/references/source_notes.md`
  - 設計根拠メモ
