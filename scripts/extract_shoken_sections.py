from __future__ import annotations

import json
import re
from pathlib import Path

import fitz


ROOT = Path(__file__).resolve().parents[1]
PAST_QUESTIONS_DIR = ROOT / "note" / "過去問"
OUTPUT_DIR = ROOT / "note" / "所見分析"
OUTPUT_JSON = OUTPUT_DIR / "sections.json"
OUTPUT_YEARS_DIR = OUTPUT_DIR / "年度別"
OUTPUT_FIXES_TABLE = OUTPUT_DIR / "文字補整対応表.md"

QUESTION_MARKERS = (
    "問題３．",
    "問題3．",
    "問題３.",
    "問題3.",
)

ANSWER_HEADERS = (
    "生保２（解答例）",
    "生保2（解答例）",
)

SECTION2_HEADERS = (
    "【 第 Ⅱ 部 】",
    "【第Ⅱ部】",
    "【 第Ⅱ部 】",
    "【第 Ⅱ部】",
)

YEAR_LINE_RE = re.compile(r"^(?:平成 ?\d+ ?年度|20\d{2} ?年度)$")
PAGE_ID_RE = re.compile(r"^生保[２2]\s*[･・…\.]{2,}\s*\d+$")
PAGE_NUMBER_RE = re.compile(r"^[一―\-]+\d+[一―\-]+$")
MARKER_ONLY_RE = re.compile(r"^[○●・◆◇■□※➢▪►▶]$")
PAREN_ITEM_RE = re.compile(
    r"^(?:"
    r"（[０-９0-9一二三四五六七八九十]+）|"
    r"（[アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲンｱ-ﾝA-Za-zＡ-Ｚａ-ｚ]+）"
    r")"
)
LETTER_ITEM_RE = re.compile(r"^[Ａ-ＺA-Z][．.]")
SIMPLE_ITEM_RE = re.compile(r"^[①②③④⑤⑥⑦⑧⑨⑩○●・◆◇■□※➢▪►▶]")
STANDALONE_LINE_RE = re.compile(
    r"^(?:"
    r"問題[０-９0-9一二三四五六七八九十]+[．.]|"
    r"[\[［].*[\]］]|"
    r"各[０-９0-9].*点.*|"
    r"以\s*上|"
    r"＜.*＞"
    r")$"
)
ITEM_START_RE = re.compile(
    r"^(?:"
    r"（[０-９0-9一二三四五六七八九十]+）|"
    r"（[アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲンｱ-ﾝA-Za-zＡ-Ｚａ-ｚ]+）|"
    r"[①②③④⑤⑥⑦⑧⑨⑩]|"
    r"[Ａ-ＺA-Z][．.]|"
    r"[○●・◆◇■□※➢▪►▶]"
    r")"
)
TERMINAL_END_RE = re.compile(r"[。！？：:］】]$")

TEXT_FIXES: tuple[tuple[str, str], ...] = (
    ("問題3．（1）1 以下は、", "問題3．（1） 以下は、"),
    ("基本的な事項につ1≡いて", "基本的な事項について"),
    ("課題で：\n…はない。", "課題ではない。"),
    ("将来≡1釣な", "将来的な"),
    ("望ま1 1れる。 i", "望まれる。"),
    ("問題3．（2）1 以下は・", "問題3．（2） 以下は、"),
    ("アクチェ1 1アリー", "アクチュアリー"),
    (" 1≡ 問題文では、", "問題文では、"),
    ("設けてい≡…ない。", "設けていない。"),
    ("3つの課題をミ…含む", "3つの課題を含む"),
    ("答案はミ1多くはなかった。", "答案は多くはなかった。"),
    ("答案は多くはなかった。 逆に、", "答案は多くはなかった。\n逆に、"),
    ("＝1 逆に・", "逆に、"),
    ("一書β", "一部"),
    ("標1 1準", "標準"),
    ("…1 解答においては、", "解答においては、"),
    ("散見された。 解答においては、", "散見された。\n解答においては、"),
    ("ほし1：レ、。 ・ 1", "ほしい。"),
    ("ご留意いただきたル・。）O一般的に", "ご留意いただきたい。）○一般的に"),
    ("ことコ（40点）", "こと。（40点）"),
    ("1間", "1問"),
    ("保険金杜", "保険会社"),
    ("保有契約南昌ポートフォリオ", "保有契約ポートフォリオ"),
    ("ソルベンシー1工", "ソルベンシーII"),
    ("必要とな一216川る", "必要となる"),
    ("高けれ一217山ば", "高ければ"),
    ("ご留意いただきたル・。）", "ご留意いただきたい。）"),
    ("発生する一であろう", "発生するであろう"),
    ("必要があるう。", "必要があろう。"),
    (
        "見直しである。2．新基準の概要ソルベンシー・マージン比率（新基準）の主な改正点は以下のとおりである。",
        "見直しである。\n2．新基準の概要\nソルベンシー・マージン比率（新基準）の主な改正点は以下のとおりである。",
    ),
    ("基本となる。・\n・これら", "基本となる。\n・これら"),
    ("ソルベンシ」", "ソルベンシー"),
    ("マ』ジン", "マージン"),
    ("・}ージン", "・マージン"),
    ("I AS B", "IASB"),
    ("O A LM", "○ ALM"),
    ("。）O一般的に", "。）○一般的に"),
    ("ご留意いただきたい。）○一般的に、", "ご留意いただきたい。）\n○一般的に、"),
    ("はOとなる", "は0となる"),
    ("」・ｱのため、", "。このため、"),
    ("こととなる。。このため、", "こととなる。このため、"),
    ("会言十監査", "会計監査"),
    ("ディスクロ附予", "ディスクロ資料"),
    ("必要がある。問題3．（2）", "必要がある。\n\n問題3．（2）"),
    ("必要となろう。〈会社の収益・リスク管理＞", "必要となろう。\n＜会社の収益・リスク管理＞"),
    ("中長1期", "中長期"),
    ("経営攻策", "経営政策"),
    ("連続桂", "連続性"),
    ("館薗香", "齟齬"),
    ("回過する", "回避する"),
    ("宋実現", "未実現"),
    ("蒋の経過", "時の経過"),
    ("だけはなく", "だけでなく"),
    ("デュレーシヨン", "デュレーション"),
    ("契約着", "契約者"),
    ("差j等", "差異等"),
    ("噺契約", "新契約"),
    ("に関しても、新契約の初期利益」", "に関しても、「新契約の初期利益」"),
    ("新南晶", "新商品"),
    ("トーダル", "トータル"),
    ("参カロ者", "参加者"),
    ("フiコー", "フロー"),
    ("展閉", "展開"),
    ("特徴がある。〔初期利益〕", "特徴がある。\n〔初期利益〕"),
    ("計上されることとなる。〔計算前提の変動性〕", "計上されることとなる。\n〔計算前提の変動性〕"),
    ("［比較可能性］", "〔比較可能性〕"),
    ("縮小を通じALM", "縮小を通じてALM"),
    ("それに維持するため", "それを維持するため"),
    ("「前提条件と実績との差異等に", "「前提条件と実績との差異」等に"),
    ("ニコア・マージン", "コア・マージン"),
    ("実旅", "実施"),
    ("取引」は", "取引』は"),
    ("マーケットヘのインパクト", "マーケットへのインパクト"),
    ("〔初期利益］", "〔初期利益〕"),
    ("［計算前提の変動性コ", "〔計算前提の変動性〕"),
    ("リズク", "リスク"),
    ("ソルベンシ∵", "ソルベンシー"),
    ("ソノレペンシー", "ソルベンシー"),
    ("アクチェアリー", "アクチュアリー"),
    ("ソルベンシ一", "ソルベンシー"),
    ("べ一ス", "ベース"),
    ("にっいて", "について"),
    ("本間題", "本問題"),
    ("会杜", "会社"),
    ("合杜", "会社"),
    ("讐", "等"),
    ("その池", "その他"),
    ("改主", "改正"),
    ("収益カ", "収益力"),
    ("’般的に", "一般的に"),
    ("リスクヘの", "リスクへの"),
    ("迅㏿", "迅速"),
    ("構㐀", "構造"),
)


def find_first(text: str, patterns: tuple[str, ...], start: int = 0) -> tuple[int, str | None]:
    hits = []
    for pattern in patterns:
        idx = text.find(pattern, start)
        if idx >= 0:
            hits.append((idx, pattern))
    if not hits:
        return -1, None
    hits.sort(key=lambda item: item[0])
    return hits[0]


def is_page_artifact(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return False
    return bool(
        YEAR_LINE_RE.fullmatch(stripped)
        or PAGE_ID_RE.fullmatch(stripped)
        or PAGE_NUMBER_RE.fullmatch(stripped)
    )


def normalize_inline_whitespace(line: str) -> str:
    line = line.replace("\u3000", " ")
    line = re.sub(r"[ \t]+", " ", line)
    return line.strip()


def join_wrapped_text(left: str, right: str) -> str:
    if not left:
        return right
    if not right:
        return left
    if left.endswith(" "):
        return left + right.lstrip()
    if MARKER_ONLY_RE.fullmatch(left):
        return f"{left} {right.lstrip()}"
    if re.search(r"[A-Za-z0-9]$", left) and re.match(r"[A-Za-z0-9]", right):
        return f"{left} {right}"
    return left + right


def is_heading_like_item(line: str) -> bool:
    if PAREN_ITEM_RE.match(line) or LETTER_ITEM_RE.match(line):
        return True
    if SIMPLE_ITEM_RE.match(line) and "。" not in line and "：" not in line and ":" not in line and len(line) <= 40:
        return True
    return False


def classify_line(line: str) -> str:
    if not line:
        return "blank"
    if STANDALONE_LINE_RE.fullmatch(line):
        return "standalone"
    if is_heading_like_item(line):
        return "standalone"
    if ITEM_START_RE.match(line):
        return "item"
    return "text"


def clean_lines(text: str) -> list[str]:
    raw_lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    lines: list[str] = []
    i = 0
    while i < len(raw_lines):
        line = normalize_inline_whitespace(raw_lines[i])
        if is_page_artifact(line):
            i += 1
            continue
        if MARKER_ONLY_RE.fullmatch(line):
            j = i + 1
            while j < len(raw_lines):
                candidate = normalize_inline_whitespace(raw_lines[j])
                if is_page_artifact(candidate):
                    j += 1
                    continue
                if not candidate:
                    j += 1
                    continue
                line = f"{line} {candidate}"
                i = j
                break
        lines.append(line)
        i += 1
    return lines


def validate_text_fixes() -> None:
    seen_before: set[str] = set()
    seen_pairs: set[tuple[str, str]] = set()
    for before, after in TEXT_FIXES:
        if before in seen_before:
            raise ValueError(f"duplicate fix source detected: {before!r}")
        pair = (before, after)
        if pair in seen_pairs:
            raise ValueError(f"duplicate fix pair detected: {pair!r}")
        seen_before.add(before)
        seen_pairs.add(pair)


def apply_text_fixes(text: str) -> str:
    for before, after in TEXT_FIXES:
        text = text.replace(before, after)
    return text


def collect_fix_sources(sections: list[dict[str, object]]) -> dict[str, list[str]]:
    fix_sources = {before: set() for before, _ in TEXT_FIXES}

    for section in sections:
        year = str(section["year"])
        markdown_name = f"{year}.md"
        for key in ("_question_text_normalized_raw", "_answer_text_normalized_raw"):
            text = str(section[key])
            for before, after in TEXT_FIXES:
                if before in text:
                    fix_sources[before].add(markdown_name)
                text = text.replace(before, after)

    return {
        before: sorted(markdown_names, key=year_sort_key_from_name)
        for before, markdown_names in fix_sources.items()
    }


def format_table_cell(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("|", "\\|")
        .replace("\n", "<br>")
    )


def format_markdown_sources(markdown_names: list[str]) -> str:
    if not markdown_names:
        return "（未検出）"
    return "<br>".join(
        f"[{name}](年度別/{name})"
        for name in markdown_names
    )


def write_fix_table(fix_sources: dict[str, list[str]]) -> None:
    rows = [
        "# 文字補整対応表",
        "",
        f"件数: {len(TEXT_FIXES)}",
        "",
        "元のMarkdownは、現行の年度別Markdownで当該補整が実際に適用されたファイルです。`（未検出）` は予備ルールです。",
        "",
        "| 補整前 | 補整後 | 元のMarkdown |",
        "| --- | --- | --- |",
    ]
    for before, after in TEXT_FIXES:
        rows.append(
            "| "
            + " | ".join(
                [
                    format_table_cell(before),
                    format_table_cell(after),
                    format_markdown_sources(fix_sources.get(before, [])),
                ]
            )
            + " |"
        )
    OUTPUT_FIXES_TABLE.write_text("\n".join(rows) + "\n", encoding="utf-8")


def normalize_block(text: str, *, apply_fixes: bool = True) -> str:
    lines = clean_lines(text)
    paragraphs: list[str] = []
    buffer = ""
    buffer_kind = ""

    for line in lines:
        kind = classify_line(line)
        if kind == "blank":
            if buffer:
                paragraphs.append(buffer)
                buffer = ""
                buffer_kind = ""
            if paragraphs and paragraphs[-1] != "":
                paragraphs.append("")
            continue

        if kind == "standalone":
            if buffer:
                paragraphs.append(buffer)
                buffer = ""
                buffer_kind = ""
            paragraphs.append(line)
            continue

        if kind == "item":
            if buffer:
                paragraphs.append(buffer)
            buffer = line
            buffer_kind = "item"
            continue

        if not buffer:
            buffer = line
            buffer_kind = "text"
            continue

        if buffer_kind == "text" and TERMINAL_END_RE.search(buffer):
            paragraphs.append(buffer)
            buffer = line
            buffer_kind = "text"
            continue

        buffer = join_wrapped_text(buffer, line)

    if buffer:
        paragraphs.append(buffer)

    text = "\n".join(paragraphs)
    text = re.sub(r"\n{3,}", "\n\n", text)
    if apply_fixes:
        text = apply_text_fixes(text)
    return text.strip()


def year_sort_key_from_name(name: str) -> tuple[int, str]:
    return year_sort_key(Path(name))


def year_sort_key(path: Path) -> tuple[int, str]:
    stem = path.stem
    if stem.startswith("H") and stem[1:].isdigit():
        return (1988 + int(stem[1:]), stem)
    digits = re.sub(r"\D", "", stem)
    if digits:
        return (int(digits[:4]), stem)
    return (9999, stem)


def extract_sections(pdf_path: Path) -> dict[str, object]:
    doc = fitz.open(str(pdf_path))
    text = "".join(page.get_text("text") for page in doc)

    question_start, question_marker = find_first(text, QUESTION_MARKERS)
    answer_header_start, answer_header = find_first(text, ANSWER_HEADERS)
    if question_start < 0 or answer_header_start < 0:
        raise ValueError(
            f"required markers not found for {pdf_path.name}: "
            f"question_start={question_start}, answer_header_start={answer_header_start}"
        )

    question_section = text[question_start:answer_header_start].strip()
    answer_start, answer_marker = find_first(text, QUESTION_MARKERS, start=answer_header_start)
    if answer_start < 0:
        raise ValueError(f"answer question marker not found for {pdf_path.name}")

    answer_section = text[answer_start:].strip()
    section2_start, section2_header = find_first(text, SECTION2_HEADERS)
    question_text_normalized_raw = normalize_block(question_section, apply_fixes=False)
    answer_text_normalized_raw = normalize_block(answer_section, apply_fixes=False)

    return {
        "file": str(pdf_path.relative_to(ROOT)).replace("\\", "/"),
        "year": pdf_path.stem,
        "question_marker": question_marker,
        "answer_header": answer_header,
        "answer_marker": answer_marker,
        "section2_header": section2_header,
        "section2_header_found": section2_start >= 0,
        "question_text": question_section,
        "question_text_normalized": apply_text_fixes(question_text_normalized_raw),
        "answer_text": answer_section,
        "answer_text_normalized": apply_text_fixes(answer_text_normalized_raw),
        "_question_text_normalized_raw": question_text_normalized_raw,
        "_answer_text_normalized_raw": answer_text_normalized_raw,
    }


def write_year_markdown(section: dict[str, object]) -> None:
    year = str(section["year"])
    content = "\n".join(
        [
            f"# {year} 所見問題",
            "",
            "## 問題",
            "",
            str(section["question_text_normalized"]),
            "",
            "## 解答例",
            "",
            str(section["answer_text_normalized"]),
            "",
        ]
    )
    (OUTPUT_YEARS_DIR / f"{year}.md").write_text(content, encoding="utf-8")


def main() -> None:
    validate_text_fixes()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_YEARS_DIR.mkdir(parents=True, exist_ok=True)
    pdf_paths = sorted(PAST_QUESTIONS_DIR.glob("*H.pdf"), key=year_sort_key)
    sections = [extract_sections(path) for path in pdf_paths]
    fix_sources = collect_fix_sources(sections)
    write_fix_table(fix_sources)

    serializable_sections = []
    for section in sections:
        serializable_section = {
            key: value
            for key, value in section.items()
            if not key.startswith("_")
        }
        serializable_sections.append(serializable_section)
    OUTPUT_JSON.write_text(
        json.dumps(serializable_sections, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    for section in sections:
        write_year_markdown(section)
    print(f"wrote {OUTPUT_JSON}")


if __name__ == "__main__":
    main()
