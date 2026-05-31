from __future__ import annotations

import argparse
import hashlib
import html
import re
from pathlib import Path

import genanki


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT_DIR = ROOT / "study" / "past_exam_memory" / "cards"
DEFAULT_OUTPUT = ROOT / "study" / "past_exam_memory" / "exports" / "生保2_過去問丸暗記.apkg"

CARD_HEADER_RE = re.compile(r"^## CARD\s+(.+?)\s*$", re.MULTILINE)
META_RE = re.compile(r"^[ \t]*- ([a-zA-Z_]+):[ \t]*(.*?)[ \t]*$", re.MULTILINE)
SECTION_RE = re.compile(r"^###\s+(.+?)\s*$", re.MULTILINE)

BASIC_MODEL_ID = 2051464518
CLOZE_MODEL_ID = 2051464519

CARD_CSS = """
.card {
  font-family: "Meiryo UI", "Meiryo", "Yu Gothic UI", sans-serif;
  font-size: 20px;
  line-height: 1.75;
  text-align: left;
  color: #222;
  background: #fff;
  padding: 18px;
  word-break: break-word;
}

.front {
  font-weight: 700;
  white-space: pre-wrap;
}

.back {
  white-space: pre-wrap;
}

.block {
  margin: 0 0 0.85em 0;
}

hr {
  border: none;
  border-top: 1px solid #ddd;
  margin: 1em 0;
}

.cloze {
  color: #b00020;
  font-weight: 700;
}
""".strip()

BASIC_MODEL = genanki.Model(
    BASIC_MODEL_ID,
    "Seiho2 Past Exam Memory Basic",
    fields=[
        {"name": "ID"},
        {"name": "Front"},
        {"name": "Answer"},
    ],
    templates=[
        {
            "name": "White Recall",
            "qfmt": '<div class="front">{{Front}}</div>',
            "afmt": '{{FrontSide}}<hr id="answer"><div class="back">{{Answer}}</div>',
        }
    ],
    css=CARD_CSS,
)

CLOZE_MODEL = genanki.Model(
    CLOZE_MODEL_ID,
    "Seiho2 Past Exam Memory Cloze",
    fields=[
        {"name": "ID"},
        {"name": "Text"},
    ],
    templates=[
        {
            "name": "Cloze",
            "qfmt": '<div class="front">{{cloze:Text}}</div>',
            "afmt": '{{cloze:Text}}',
        }
    ],
    css=CARD_CSS,
    model_type=genanki.Model.CLOZE,
)


class StableNote(genanki.Note):
    @property
    def guid(self) -> str:
        return genanki.guid_for(self.fields[0])


def stable_deck_id(deck_name: str) -> int:
    digest = hashlib.sha256(deck_name.encode("utf-8")).digest()
    return int.from_bytes(digest[:4], "big") % 2_000_000_000 + 1


def split_sections(block: str) -> tuple[dict[str, str], dict[str, str]]:
    meta = {m.group(1): m.group(2).strip() for m in META_RE.finditer(block)}
    section_matches = list(SECTION_RE.finditer(block))
    sections: dict[str, str] = {}
    for idx, match in enumerate(section_matches):
        start = match.end()
        end = section_matches[idx + 1].start() if idx + 1 < len(section_matches) else len(block)
        sections[match.group(1).strip()] = block[start:end].strip()
    return meta, sections


def text_to_html(text: str) -> str:
    paragraphs = [chunk.strip() for chunk in text.replace("\r\n", "\n").split("\n\n")]
    blocks = []
    for paragraph in paragraphs:
        if not paragraph:
            continue
        escaped = html.escape(paragraph).replace("\n", "<br>")
        blocks.append(f'<div class="block">{escaped}</div>')
    return "".join(blocks)


def split_tags(tags: str, card_type: str) -> list[str]:
    values = [tag for tag in tags.split() if tag]
    if card_type not in values:
        values.append(card_type)
    return values


def parse_cards(input_dir: Path) -> list[dict[str, str]]:
    cards: list[dict[str, str]] = []
    for path in sorted(input_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8-sig")
        matches = list(CARD_HEADER_RE.finditer(text))
        for idx, match in enumerate(matches):
            start = match.start()
            end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
            block = text[start:end]
            meta, sections = split_sections(block)
            card_type = meta.get("card_type", "whole")
            deck = meta.get("deck", "生保2::過去問丸暗記")
            if card_type == "cloze":
                text_section = sections.get("Cloze", "").strip()
                if not text_section:
                    raise ValueError(f"{match.group(1)}: missing Cloze section")
                cards.append(
                    {
                        "id": meta.get("memory_id", match.group(1).strip()),
                        "deck": deck,
                        "card_type": card_type,
                        "tags": meta.get("tags", ""),
                        "front": "",
                        "answer": "",
                        "cloze": text_section,
                    }
                )
            else:
                question = sections.get("問題", "").strip()
                answer = sections.get("暗記答案", "").strip()
                if not question:
                    raise ValueError(f"{match.group(1)}: missing 問題 section")
                if not answer:
                    raise ValueError(f"{match.group(1)}: missing 暗記答案 section")
                cards.append(
                    {
                        "id": meta.get("memory_id", match.group(1).strip()),
                        "deck": deck,
                        "card_type": card_type,
                        "tags": meta.get("tags", ""),
                        "front": question,
                        "answer": answer,
                        "cloze": "",
                    }
                )
    return cards


def build_decks(cards: list[dict[str, str]]) -> list[genanki.Deck]:
    decks: dict[str, genanki.Deck] = {}
    for card in cards:
        deck_name = card["deck"]
        deck = decks.setdefault(deck_name, genanki.Deck(stable_deck_id(deck_name), deck_name))
        if card["card_type"] == "cloze":
            deck.add_note(
                StableNote(
                    model=CLOZE_MODEL,
                    fields=[card["id"], text_to_html(card["cloze"])],
                    tags=split_tags(card["tags"], card["card_type"]),
                )
            )
        else:
            deck.add_note(
                StableNote(
                    model=BASIC_MODEL,
                    fields=[card["id"], text_to_html(card["front"]), text_to_html(card["answer"])],
                    tags=split_tags(card["tags"], card["card_type"]),
                )
            )
    return [decks[name] for name in sorted(decks)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Export past-exam memory cards to an APKG with chapter subdecks.")
    parser.add_argument("--input-dir", default=str(DEFAULT_INPUT_DIR), help="Directory containing memory card Markdown.")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="Output APKG path.")
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    output_path = Path(args.output)
    cards = parse_cards(input_dir)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    genanki.Package(build_decks(cards)).write_to_file(output_path)

    print(f"exported notes={len(cards)} decks={len(set(card['deck'] for card in cards))} to {output_path}")


if __name__ == "__main__":
    main()
