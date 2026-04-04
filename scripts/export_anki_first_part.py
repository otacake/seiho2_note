from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


CARD_HEADER_RE = re.compile(r"^## CARD\s+(.+?)\s*$", re.MULTILINE)
NON_CARD_HEADER_RE = re.compile(r"^##\s+(?!CARD).+?\s*$", re.MULTILINE)
SECTION_RE = re.compile(r"^###\s+(.+?)\s*$", re.MULTILINE)
META_RE = re.compile(r"^[ \t]*- ([a-zA-Z_]+):[ \t]*(.*?)[ \t]*$", re.MULTILINE)
BOLD_RE = re.compile(r"\*\*(.+?)\*\*")


def parse_card_block(block: str) -> dict[str, str]:
    lines = block.strip().splitlines()
    card_id = lines[0].replace("## CARD", "", 1).strip()

    meta: dict[str, str] = {}
    sections: dict[str, str] = {}

    meta_matches = list(META_RE.finditer(block))
    for match in meta_matches:
        meta[match.group(1)] = match.group(2).strip()

    section_matches = list(SECTION_RE.finditer(block))
    for idx, match in enumerate(section_matches):
        name = match.group(1).strip()
        start = match.end()
        end = section_matches[idx + 1].start() if idx + 1 < len(section_matches) else len(block)
        sections[name] = block[start:end].strip()

    required = ["問題", "要するに何か", "問題意識", "基準答案"]
    missing = [name for name in required if name not in sections]
    if missing:
        raise ValueError(f"{card_id}: missing sections: {', '.join(missing)}")

    source = meta.get("source", "")
    tags = meta.get("tags", "")

    front = normalize_text(sections["問題"])
    back_parts = [f"出典: {source}" if source else "", "【問題】", normalize_text(sections["問題"])]
    if "ざっくり説明" in sections:
        back_parts.extend(["【ざっくり説明】", normalize_text(sections["ざっくり説明"])])
    back_parts.extend(
        [
            "【要するに何か】",
            normalize_text(sections["要するに何か"]),
            "【問題意識】",
            normalize_text(sections["問題意識"]),
            "【詳細説明】",
            normalize_text(sections.get("詳細説明", "")),
            "【基準答案】",
            normalize_text(sections["基準答案"]),
        ]
    )
    back = "\n\n".join(back_parts).strip()

    cloze = sections.get("Anki穴埋め", "").strip()

    return {
        "id": card_id,
        "source": source,
        "tags": tags,
        "front": front,
        "back": back,
        "cloze": cloze,
    }


def normalize_text(text: str) -> str:
    # Markdown emphasis is useful in source files but noisy in Anki plain-text TSV.
    return BOLD_RE.sub(r"\1", text).replace("`", "")


def parse_markdown(path: Path) -> list[dict[str, str]]:
    text = path.read_text(encoding="utf-8")
    matches = list(CARD_HEADER_RE.finditer(text))
    non_card_matches = list(NON_CARD_HEADER_RE.finditer(text))
    cards: list[dict[str, str]] = []

    for idx, match in enumerate(matches):
        start = match.start()
        next_card_start = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        next_non_card_start = len(text)
        for other in non_card_matches:
            if other.start() > start:
                next_non_card_start = other.start()
                break
        end = min(next_card_start, next_non_card_start)
        block = text[start:end]
        cards.append(parse_card_block(block))

    return cards


def collect_cards(input_dir: Path) -> list[dict[str, str]]:
    cards: list[dict[str, str]] = []
    for path in sorted(input_dir.glob("*.md")):
        if path.name in {"README.md", "暗記リスト.md"}:
            continue
        cards.extend(parse_markdown(path))
    return cards


def write_basic_tsv(cards: list[dict[str, str]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh, delimiter="\t", quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["id", "source", "tags", "front", "back"])
        for card in cards:
            writer.writerow(
                [
                    card["id"],
                    card["source"],
                    card["tags"],
                    card["front"],
                    card["back"],
                ]
            )


def write_cloze_tsv(cards: list[dict[str, str]], output_path: Path) -> int:
    cloze_cards = [card for card in cards if card.get("cloze")]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh, delimiter="\t", quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["id", "source", "tags", "text"])
        for card in cloze_cards:
            writer.writerow(
                [
                    card["id"],
                    card["source"],
                    card["tags"],
                    normalize_text(card["cloze"]),
                ]
            )
    return len(cloze_cards)


def main() -> None:
    parser = argparse.ArgumentParser(description="Export first-part markdown cards to Anki TSV.")
    parser.add_argument(
        "--input-dir",
        default="study/first_part",
        help="Directory containing markdown card files.",
    )
    parser.add_argument(
        "--output",
        default="study/anki/exports/first_part_cards.tsv",
        help="Output TSV path for Basic-style cards.",
    )
    parser.add_argument(
        "--cloze-output",
        default="study/anki/exports/first_part_cloze.tsv",
        help="Output TSV path for Cloze-style cards.",
    )
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    output_path = Path(args.output)
    cloze_output_path = Path(args.cloze_output)

    cards = collect_cards(input_dir)
    write_basic_tsv(cards, output_path)
    cloze_count = write_cloze_tsv(cards, cloze_output_path)
    print(f"exported {len(cards)} basic cards to {output_path}")
    print(f"exported {cloze_count} cloze cards to {cloze_output_path}")


if __name__ == "__main__":
    main()
