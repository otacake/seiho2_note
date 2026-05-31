from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STUDY_DIR = ROOT / "study"
FIRST_PART_DIR = STUDY_DIR / "first_part"
COVERAGE_PATH = STUDY_DIR / "coverage" / "canonical_problems.csv"
SHOKEN_YEAR_DIR = ROOT / "note" / "所見分析" / "年度別"
OUTPUT_DIR = STUDY_DIR / "past_exam_memory"
UNITS_DIR = OUTPUT_DIR / "units"
CARDS_DIR = OUTPUT_DIR / "cards"

TARGET_YEAR_RE = re.compile(r"\b(?:H2[3-9]|20(?:18|19|20|21|22|23|24|25))\b")
CARD_HEADER_RE = re.compile(r"^## CARD\s+(.+?)\s*$", re.MULTILINE)
META_RE = re.compile(r"^[ \t]*- ([a-zA-Z_]+):[ \t]*(.*?)[ \t]*$", re.MULTILINE)
SECTION_RE = re.compile(r"^###\s+(.+?)\s*$", re.MULTILINE)
PROBLEM_ANSWER_SPLIT_RE = re.compile(r"^##\s+解答例\s*$", re.MULTILINE)
MAJOR_QUESTION_RE = re.compile(r"^（([１２12])）", re.MULTILINE)
SUBQUESTION_RE = re.compile(r"^(?:（([アイウエオ])）|([①②③④⑤])(?=\s|$))", re.MULTILINE)
ANSWER_MAJOR_RE = re.compile(r"^問題３[．.]（([１２12])）", re.MULTILINE)
ANSWER_SUB_RE = re.compile(r"^(?:（([アイウエオ])）|([①②③④⑤]))", re.MULTILINE)
ANSWER_HEADING_RE = re.compile(r"^＜(.+?)＞", re.MULTILINE)
WORD_LIMIT_RE = re.compile(r"制限字数は(?:それぞれ)?([０-９0-9,，]+)字")
POINTS_RE = re.compile(r"（([０-９0-9]+)点）")

INDEX_FIELDS = [
    "memory_id",
    "year",
    "part",
    "problem_no",
    "sub_no",
    "unit",
    "question_type",
    "points",
    "word_limit",
    "source_ref",
    "source_path",
    "answer_source",
    "wb_origin",
    "card_type",
    "deck",
    "priority",
    "status",
]

UNIT_INFO = {
    "01_生命保険会計": "生保2::過去問丸暗記::01_生命保険会計",
    "03_契約者配当": "生保2::過去問丸暗記::03_契約者配当",
    "04_リスク管理_ALM_ストレステスト": "生保2::過去問丸暗記::04_リスク管理_ALM_ストレステスト",
    "05_事業費": "生保2::過去問丸暗記::05_事業費",
    "06_ソルベンシー": "生保2::過去問丸暗記::06_ソルベンシー",
    "07_内部管理会計_区分経理": "生保2::過去問丸暗記::07_内部管理会計_区分経理",
    "08_相互会社と株式会社": "生保2::過去問丸暗記::08_相互会社と株式会社",
    "90_計理人実務基準": "生保2::過去問丸暗記::90_計理人実務基準",
}

UNIT_GUIDES = {
    "01_生命保険会計": {
        "big_picture": [
            "生命保険会計は、保険料が入った瞬間の見た目ではなく、将来の保険金や給付金を払い続けられるかを数字で表す単元です。普通の会社なら売上と費用を期間で対応させればかなりの部分を説明できますが、生命保険会社では約束が何十年も残ります。受け取った保険料の中には、今年の収益にしてよい部分と、将来の支払に備えて負債として残すべき部分が混ざっています。",
            "この単元で暗記する文言は、現金主義、責任準備金、支払備金、有価証券評価、利源分析などに分かれています。ばらばらに見えますが、どれも「今期利益をどう測るか」と「将来の支払能力をどう守るか」の間を調整するための道具です。",
        ],
        "position": "答案を覚えるときは、各論点を会計処理の名前としてではなく、現金の入り、将来負債への積立、既発生債務の認識、剰余の発生源の分析という流れのどこにあるかへ置いてください。",
    },
    "03_契約者配当": {
        "big_picture": [
            "契約者配当は、保険料に織り込まれた安全割増や実績差から生じた剰余を、どの契約者へ、どの程度、どのタイミングで返すかを扱う単元です。単なる利益還元ではありません。長期契約を守るための内部留保、公正・衡平な契約者間配分、会社の健全性を同時に見ます。",
            "配当の問題で問われるのは、剰余が出たらすぐ返すかどうかではなく、返してよい剰余なのか、誰の貢献による剰余なのか、返した後も残存契約群団を守れるのか、という判断です。",
        ],
        "position": "暗記事項は、配当の理由、割当と分配、公正・衡平、アセット・シェア、通常配当・特別配当、保険計理人の確認に分かれます。すべて「還元」と「健全性」の綱引きを説明する材料です。",
    },
    "04_リスク管理_ALM_ストレステスト": {
        "big_picture": [
            "リスク管理・ALM・ストレステストは、会社がどの壊れ方を先に疑い、どの指標で見つけ、どの経営行動へつなげるかを扱う単元です。保険会社は長い負債を持つため、金利、解約、死亡率、流動性、市場急変が時間差をもって資産・負債・自己資本に波及します。",
            "ALMは資産運用の小技ではなく、負債の性質に合わせて資産とリスクを管理する考え方です。ストレステストは悲観シナリオを作る作業ではなく、通常のモデルでは見えにくい壊れ方を経営判断へ戻す作業です。",
        ],
        "position": "暗記事項は、リスクの定義、ERM、必要資本、モデル限界、ALM、流動性、ストレステストに分かれます。どれも「何をリスクと呼び、どの経路で会社が傷み、どう管理に戻すか」を答えるための部品です。",
    },
    "05_事業費": {
        "big_picture": [
            "事業費は、保険を売るため、維持するため、管理するためにかかる費用をどう測り、商品別・チャネル別にどう読ませるかを扱う単元です。生命保険では新契約時に大きな費用が先に出て、保険料からの回収は長い期間に分かれます。ここに普通の費用管理と違う難しさがあります。",
            "予定事業費枠、費差損益、商品別原価管理、事業費モニタリングは、すべて「費用が高いか低いか」だけではなく、その費用をどの商品が生み、どの将来収益で回収するのかを判断するための道具です。",
        ],
        "position": "暗記事項は、枠の定義や計算だけでなく、新契約費の回収、費差損益の読み方、商品別収益性、モニタリング資料の意味へ結びつけて覚えると崩れにくくなります。",
    },
    "06_ソルベンシー": {
        "big_picture": [
            "ソルベンシーは、予測どおりの支払を超える悪化が起きても、保険会社が契約上の債務を履行できるかを扱う単元です。責任準備金が通常想定される支払に備えるものだとすると、ソルベンシーはその外側にある不確実性を受け止める財政的な厚みです。",
            "静的評価、動的評価、自己資本、早期是正措置、経済価値ベース規制は、見ている角度が違います。ある一時点で足りているか、将来経路でも足りるか、市場整合的に見ると何が変わるか、監督上どこで介入するかを分けて読む単元です。",
        ],
        "position": "暗記事項は、支払能力を守るための箱を一つずつ名前で覚えるだけでは足りません。責任準備金、自己資本、リスク量、経済価値評価、監督措置がどうつながるかを置きながら再現します。",
    },
    "07_内部管理会計_区分経理": {
        "big_picture": [
            "内部管理会計・区分経理は、法定会計だけでは見えにくい収益性やリスクを、経営判断に使える形へ分解する単元です。法定会計は契約者保護と支払能力確保に強い一方、新契約の価値、商品別採算、チャネル別の損益、将来利益の見通しはそのままでは読み切れません。",
            "区分経理は、商品や資産の区分ごとに損益・資産・負債を分けて、内部補助や配当の不公平を見えやすくする仕組みです。EVやMCEVは、法定会計より将来利益と経済価値を前に出して読むための道具です。",
        ],
        "position": "暗記事項は、法定会計の限界、内部管理会計の必要性、EV、区分経理、商品区分・全社区分・資産区分の関係を、経営が何を判断したいのかに結びつけて覚えるための材料です。",
    },
    "08_相互会社と株式会社": {
        "big_picture": [
            "相互会社と株式会社は、会社の主体、利益の帰属、配当の意味、資本調達の形がどう違うかを扱う単元です。見た目は会社形態の比較ですが、配当、内部留保、基金、非社員契約、公正・衡平の考え方へ波及します。",
            "相互会社では契約者が社員として会社の構成員になるため、剰余の分配や非社員契約の扱いに独特の注意が出ます。株式会社では株主資本と契約者配当を分けて考える必要があります。",
        ],
        "position": "暗記事項は、制度名を覚えるより、誰が会社の残余利益を受けるのか、誰を守る規制なのか、配当や区分経理にどのように跳ねるのかを置いて覚えます。",
    },
    "90_計理人実務基準": {
        "big_picture": [
            "保険計理人実務基準は、保険計理人が責任準備金、配当、将来収支分析などを確認するときの実務上の型を扱う単元です。試験では条文暗記に見えますが、実際には会社の判断をどの観点から検証するのかが問われています。",
            "配当確認や将来収支分析では、単に計算結果を見るのではなく、会社全体、商品区分、代表契約、将来の健全性を段階的に確認します。",
        ],
        "position": "暗記事項は、実務基準の条文番号を孤立して覚えるのではなく、保険計理人が何を確認し、どの報告・判断へつなげるかの手順として覚えると再現しやすくなります。",
    },
}

SUB_ID_MAP = {
    "ア": "A",
    "イ": "B",
    "ウ": "C",
    "エ": "D",
    "オ": "E",
    "①": "1",
    "②": "2",
    "③": "3",
    "④": "4",
    "⑤": "5",
}


@dataclass
class SourceCard:
    card_id: str
    path: Path
    unit: str
    source: str
    tags: str
    priority: str
    question: str
    answer: str
    understanding: str
    cloze: str


@dataclass
class MemoryCard:
    memory_id: str
    parent_memory_id: str
    year: str
    part: str
    problem_no: str
    sub_no: str
    unit: str
    question_type: str
    points: str
    word_limit: str
    source_ref: str
    source_path: str
    answer_source: str
    wb_origin: str
    card_type: str
    deck: str
    priority: str
    status: str
    question: str
    answer: str
    cloze: str = ""


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8-sig", newline="\n")


def normalize_fullwidth_number(text: str) -> str:
    return text.translate(str.maketrans("０１２３４５６７８９", "0123456789")).replace(",", "").replace("，", "")


def slug(text: str) -> str:
    value = re.sub(r"[^A-Za-z0-9_-]+", "-", text)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "unknown"


def unit_from_first_part_file(path: Path) -> str:
    name = path.name
    if name.startswith("02-01"):
        return "01_生命保険会計"
    if name.startswith("02-03"):
        return "03_契約者配当"
    if name.startswith("02-04"):
        return "04_リスク管理_ALM_ストレステスト"
    if name.startswith("02-05"):
        return "05_事業費"
    if name.startswith("02-06"):
        return "06_ソルベンシー"
    if name.startswith("02-07"):
        return "07_内部管理会計_区分経理"
    if name.startswith("02-08"):
        return "08_相互会社と株式会社"
    if name.startswith("90_") or name.startswith("91_"):
        return "90_計理人実務基準"
    return "90_計理人実務基準"


def unit_from_chapter(chapter: str) -> str:
    if "第1章" in chapter or "生命保険会計" in chapter:
        return "01_生命保険会計"
    if "第3章" in chapter or "契約者配当" in chapter:
        return "03_契約者配当"
    if "リスク管理" in chapter or "ALM" in chapter or "ストレス" in chapter:
        return "04_リスク管理_ALM_ストレステスト"
    if "第5章" in chapter or "事業費" in chapter:
        return "05_事業費"
    if "第6章" in chapter or "ソルベンシー" in chapter:
        return "06_ソルベンシー"
    if "第7章" in chapter or "内部管理会計" in chapter or "区分経理" in chapter:
        return "07_内部管理会計_区分経理"
    if "第8章" in chapter or "相互会社" in chapter or "株式会社" in chapter:
        return "08_相互会社と株式会社"
    if "計理人" in chapter or "実務基準" in chapter:
        return "90_計理人実務基準"
    return "90_計理人実務基準"


def unit_from_text(text: str) -> str:
    if any(word in text for word in ["ストレステスト", "ALM", "リスク管理", "市場リスク", "流動性リスク", "資産負債"]):
        return "04_リスク管理_ALM_ストレステスト"
    if any(word in text for word in ["事業費", "原価", "予定事業費", "費差"]):
        return "05_事業費"
    if any(word in text for word in ["ソルベンシー", "経済価値", "保険負債", "自己資本", "支払保証"]):
        return "06_ソルベンシー"
    if any(word in text for word in ["内部管理会計", "区分経理", "利源分析", "Embedded Value", "ＥＶ", "EV"]):
        return "07_内部管理会計_区分経理"
    if any(word in text for word in ["相互会社", "株式会社", "非社員契約"]):
        return "08_相互会社と株式会社"
    if any(word in text for word in ["保険計理人", "実務基準"]):
        return "90_計理人実務基準"
    if any(word in text for word in ["契約者配当", "社員配当", "配当"]):
        return "03_契約者配当"
    return "01_生命保険会計"


def split_sections(block: str) -> tuple[dict[str, str], dict[str, str]]:
    meta = {m.group(1): m.group(2).strip() for m in META_RE.finditer(block)}
    section_matches = list(SECTION_RE.finditer(block))
    sections: dict[str, str] = {}
    for idx, match in enumerate(section_matches):
        start = match.end()
        end = section_matches[idx + 1].start() if idx + 1 < len(section_matches) else len(block)
        sections[match.group(1).strip()] = block[start:end].strip()
    return meta, sections


def parse_first_part_cards() -> dict[str, SourceCard]:
    cards: dict[str, SourceCard] = {}
    for path in sorted(FIRST_PART_DIR.glob("*.md")):
        if path.name in {"README.md", "暗記リスト.md"}:
            continue
        text = path.read_text(encoding="utf-8-sig")
        matches = list(CARD_HEADER_RE.finditer(text))
        for idx, match in enumerate(matches):
            start = match.start()
            end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
            block = text[start:end]
            meta, sections = split_sections(block)
            card_id = match.group(1).strip()
            understanding_parts = []
            for name in ["ざっくり説明", "要するに何か", "問題意識", "詳細説明"]:
                value = sections.get(name, "").strip()
                if value:
                    understanding_parts.append(f"#### {name}\n\n{value}")
            cards[card_id] = SourceCard(
                card_id=card_id,
                path=path,
                unit=unit_from_first_part_file(path),
                source=meta.get("source", ""),
                tags=meta.get("tags", ""),
                priority=meta.get("priority", "B"),
                question=sections.get("問題", "").strip(),
                answer=sections.get("基準答案", "").strip(),
                understanding="\n\n".join(understanding_parts).strip(),
                cloze=sections.get("Anki穴埋め", "").strip(),
            )
    return cards


def load_coverage_rows() -> list[dict[str, str]]:
    with COVERAGE_PATH.open(encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def source_years(source: str) -> str:
    years = []
    for match in re.finditer(r"\b(?:H\d{1,2}|20\d{2})\b", source):
        value = match.group(0)
        if value not in years:
            years.append(value)
    return "; ".join(years)


def first_ref_parts(source: str) -> tuple[str, str, str]:
    match = re.search(r"\b(H\d{1,2}|20\d{2})[-－](\d+)(?:[-－](\d+))?", source)
    if match:
        return match.group(1), match.group(2), match.group(3) or ""
    match = re.search(r"\b(H\d{1,2}|20\d{2})\b", source)
    if match:
        return match.group(1), "", ""
    return "", "", ""


def format_front(question: str, source_ref: str, points: str = "", word_limit: str = "") -> str:
    lines = []
    if source_ref:
        lines.append(f"出典: {source_ref}")
    if points or word_limit:
        details = []
        if points:
            details.append(f"{points}点")
        if word_limit:
            details.append(f"制限字数: {word_limit}字")
        lines.append(" / ".join(details))
    if lines:
        lines.append("")
    lines.append(question.strip())
    return "\n".join(lines).strip()


def answer_chunks(answer: str, max_chars: int = 850) -> list[tuple[str, str]]:
    clean = answer.strip()
    if len(clean) <= max_chars:
        return []
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", clean) if p.strip()]
    if len(paragraphs) <= 1:
        lines = [line.rstrip() for line in clean.splitlines() if line.strip()]
        paragraphs = []
        current: list[str] = []
        for line in lines:
            if current and (len("\n".join(current)) + len(line) > max_chars):
                paragraphs.append("\n".join(current))
                current = []
            current.append(line)
        if current:
            paragraphs.append("\n".join(current))

    chunks: list[tuple[str, str]] = []
    current: list[str] = []
    for paragraph in paragraphs:
        current_text = "\n\n".join(current)
        if current and len(current_text) + len(paragraph) > max_chars:
            chunk_text = "\n\n".join(current).strip()
            chunks.append((chunk_title(chunk_text, len(chunks) + 1), chunk_text))
            current = [paragraph]
        else:
            current.append(paragraph)
    if current:
        chunk_text = "\n\n".join(current).strip()
        chunks.append((chunk_title(chunk_text, len(chunks) + 1), chunk_text))
    return chunks if len(chunks) > 1 else []


def chunk_title(text: str, index: int) -> str:
    for line in text.splitlines():
        stripped = line.strip(" 　・-○")
        if stripped:
            return stripped[:48]
    return f"第{index}ブロック"


def question_shape(card: MemoryCard) -> tuple[str, str]:
    text = "\n".join([card.question, card.answer])
    if card.status == "long_context":
        return (
            "長文所見の文脈",
            "この設問は初回の全文暗記対象ではありません。小中問で覚えた定義や比較を、状況設定の中でどう使うかを見るための位置づけです。原文答案を丸ごと覚えるより、どの単元知識が長文のどこで使われるかを確認します。",
        )
    if "穴埋め" in text:
        return (
            "用語固定型",
            "この設問は、制度の細い部品を正確な語句で戻すためのものです。意味を理解していても、用語や勘定名がずれると点になりにくいので、白紙再現では言葉の順序と箱の名前まで確認します。",
        )
    if any(word in text for word in ["相違", "違い", "比較", "対比"]):
        return (
            "比較型",
            "この設問は、二つ以上の制度や処理を同じ軸で並べる力を見ています。暗記するときは片方ずつ覚えるのではなく、目的、対象、評価方法、実務上の使いどころの差を対応させます。",
        )
    if any(word in text for word in ["列挙", "挙げ"]):
        return (
            "列挙型",
            "この設問は、観点の抜け漏れをなくすことが中心です。各項目の説明を長くする前に、まず見出しを全部出せる状態にします。その後で、それぞれが何を守る項目なのかを一文で添えます。",
        )
    if any(word in text for word in ["留意", "所見"]):
        return (
            "判断型",
            "この設問は、知識を並べるだけでなく、会社や契約群団がどう傷むかを考えて判断する問題です。暗記事項は結論の丸写しではなく、リスクの起点、波及経路、管理上の対応を順に出すための骨組みとして使います。",
        )
    if any(word in text for word in ["意義", "目的", "必要性", "理由"]):
        return (
            "意義型",
            "この設問は、制度や処理がなぜ必要なのかを問います。定義を言うだけでは足りません。何が放置されると困るのか、その制度がどの不都合を小さくするのかまでつなげて読むと、暗記答案の文言が動きます。",
        )
    return (
        "説明型",
        "この設問は、制度や処理の輪郭を短く再現するためのものです。まず対象を言い、次に仕組みを言い、最後に実務上なぜその扱いになるのかを置くと、答案の順序を戻しやすくなります。",
    )


def root_explanation(card: MemoryCard) -> str:
    guide = UNIT_GUIDES.get(card.unit, {})
    shape_name, shape_body = question_shape(card)
    if card.part == "II":
        exam_role = "第II部の小中問は、後続の所見を書くための前提をそろえる役割を持ちます。ここで出した定義や比較が、そのまま長文答案の見出しや判断材料になります。"
    else:
        exam_role = "第I部・WB型の小問は、単元知識を短い設問で正確に戻す訓練です。原問題を見た瞬間に、何を聞かれているか、どの答案ブロックを出すかを決めることが狙いです。"

    position = guide.get("position", "")
    return "\n\n".join(
        [
            "#### そもそも何の話か",
            guide.get("big_picture", [""])[0],
            "#### この暗記事項の位置づけ",
            "\n\n".join([position, exam_role]).strip(),
            f"#### 設問の型: {shape_name}",
            shape_body,
            "#### 読後に戻る問い",
            "暗記答案を読む前よりも、次の三つが言える状態になっていれば十分です。何を守るための制度・処理なのか。どの指標、負債、剰余、リスクに効いているのか。この答案を長文所見で使うなら、どの見出しの材料になるのか。",
        ]
    ).strip()


def make_memory_card(
    memory_id: str,
    source_card: SourceCard,
    source_ref: str,
    wb_origin: str,
    answer_source: str,
    year: str = "",
    problem_no: str = "",
    sub_no: str = "",
    priority: str | None = None,
) -> MemoryCard:
    unit = source_card.unit
    return MemoryCard(
        memory_id=memory_id,
        parent_memory_id="",
        year=year or source_years(source_ref),
        part="I",
        problem_no=problem_no,
        sub_no=sub_no,
        unit=unit,
        question_type="first_part",
        points="",
        word_limit="",
        source_ref=source_ref,
        source_path=rel(source_card.path),
        answer_source=answer_source,
        wb_origin=wb_origin,
        card_type="whole",
        deck=UNIT_INFO[unit],
        priority=priority or source_card.priority or "B",
        status="carded",
        question=format_front(source_card.question, source_ref),
        answer=source_card.answer,
    )


def add_chunks(card: MemoryCard) -> list[MemoryCard]:
    chunks = []
    for idx, (title, body) in enumerate(answer_chunks(card.answer), start=1):
        chunks.append(
            MemoryCard(
                memory_id=f"{card.memory_id}-C{idx:02d}",
                parent_memory_id=card.memory_id,
                year=card.year,
                part=card.part,
                problem_no=card.problem_no,
                sub_no=card.sub_no,
                unit=card.unit,
                question_type=card.question_type,
                points=card.points,
                word_limit=card.word_limit,
                source_ref=card.source_ref,
                source_path=card.source_path,
                answer_source=card.answer_source,
                wb_origin=card.wb_origin,
                card_type="chunk",
                deck=card.deck,
                priority=card.priority,
                status="carded",
                question=f"{card.question}\n\n観点: {title}",
                answer=body,
            )
        )
    return chunks


def build_first_part_memory_cards(source_cards: dict[str, SourceCard]) -> tuple[list[MemoryCard], dict[str, str]]:
    cards: list[MemoryCard] = []
    included_card_ids: set[str] = set()
    card_understanding: dict[str, str] = {}

    for row in load_coverage_rows():
        if row["study_status"] == "excluded":
            continue
        origin = row["origin"]
        if origin not in {"wb+notes", "wb_only"}:
            continue
        card_id = row["study_card_id"]
        source_card = source_cards.get(card_id)
        if not source_card or not source_card.answer:
            continue
        year, problem_no, sub_no = first_ref_parts(row["source_refs"] or source_card.source)
        memory_id = f"PEM-WB-{row['canonical_id']}-W"
        card = make_memory_card(
            memory_id=memory_id,
            source_card=source_card,
            source_ref=row["source_refs"] or source_card.source,
            wb_origin=origin,
            answer_source=f"study_card:{card_id}",
            year=year,
            problem_no=problem_no,
            sub_no=sub_no,
            priority=source_card.priority,
        )
        cards.append(card)
        cards.extend(add_chunks(card))
        included_card_ids.add(card_id)
        card_understanding[card.memory_id] = source_card.understanding

        if source_card.cloze:
            cloze_id = f"PEM-WB-{row['canonical_id']}-Z01"
            cards.append(
                MemoryCard(
                    memory_id=cloze_id,
                    parent_memory_id=card.memory_id,
                    year=card.year,
                    part=card.part,
                    problem_no=card.problem_no,
                    sub_no=card.sub_no,
                    unit=card.unit,
                    question_type=card.question_type,
                    points=card.points,
                    word_limit=card.word_limit,
                    source_ref=card.source_ref,
                    source_path=card.source_path,
                    answer_source=card.answer_source,
                    wb_origin=origin,
                    card_type="cloze",
                    deck=card.deck,
                    priority=card.priority,
                    status="carded",
                    question=card.question,
                    answer="",
                    cloze=source_card.cloze,
                )
            )

    for source_card in source_cards.values():
        if source_card.card_id in included_card_ids:
            continue
        if not TARGET_YEAR_RE.search(source_card.source):
            continue
        if not source_card.answer:
            continue
        year, problem_no, sub_no = first_ref_parts(source_card.source)
        memory_id = f"PEM-FP-{slug(source_card.card_id)}-W"
        card = make_memory_card(
            memory_id=memory_id,
            source_card=source_card,
            source_ref=source_card.source,
            wb_origin="non_wb",
            answer_source=f"study_card:{source_card.card_id}",
            year=year,
            problem_no=problem_no,
            sub_no=sub_no,
            priority=source_card.priority,
        )
        cards.append(card)
        cards.extend(add_chunks(card))
        card_understanding[card.memory_id] = source_card.understanding

    return cards, card_understanding


def split_by_matches(text: str, matches: list[re.Match[str]]) -> dict[str, str]:
    parts: dict[str, str] = {}
    for idx, match in enumerate(matches):
        start = match.start()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        label = next(group for group in match.groups() if group)
        parts[label.translate(str.maketrans("１２", "12"))] = text[start:end].strip()
    return parts


def sub_id(label: str) -> str:
    return SUB_ID_MAP.get(label, slug(label).upper())


def parse_year_file(path: Path) -> list[MemoryCard]:
    text = path.read_text(encoding="utf-8-sig")
    split_match = PROBLEM_ANSWER_SPLIT_RE.search(text)
    if not split_match:
        return []
    problem_text = text[: split_match.start()]
    answer_text = text[split_match.end() :]
    year = path.stem.removesuffix("H")

    major_questions = split_by_matches(problem_text, list(MAJOR_QUESTION_RE.finditer(problem_text)))
    major_answers = split_by_matches(answer_text, list(ANSWER_MAJOR_RE.finditer(answer_text)))
    cards: list[MemoryCard] = []

    for major_no, major_block in major_questions.items():
        sub_matches = list(SUBQUESTION_RE.finditer(major_block))
        if not sub_matches:
            continue
        major_answer = major_answers.get(major_no, "")
        sub_answers = split_by_matches(major_answer, list(ANSWER_SUB_RE.finditer(major_answer)))
        if not sub_answers:
            heading_matches = list(ANSWER_HEADING_RE.finditer(major_answer))
            heading_parts = split_by_matches(major_answer, heading_matches)
            labels = [next(group for group in match.groups() if group) for match in sub_matches]
            ordered_heading_values = list(heading_parts.values())
            if len(ordered_heading_values) >= len(labels):
                sub_answers = {label: ordered_heading_values[idx] for idx, label in enumerate(labels)}
        for idx, sub_match in enumerate(sub_matches):
            sub_no = next(group for group in sub_match.groups() if group)
            start = sub_match.start()
            end = sub_matches[idx + 1].start() if idx + 1 < len(sub_matches) else len(major_block)
            preamble = major_block[:start].strip()
            sub_question = major_block[start:end].strip()
            word_limit_match = WORD_LIMIT_RE.search(sub_question)
            word_limit = normalize_fullwidth_number(word_limit_match.group(1)) if word_limit_match else ""
            points_match = POINTS_RE.search(sub_question)
            points = normalize_fullwidth_number(points_match.group(1)) if points_match else ""
            answer = sub_answers.get(sub_no, "").strip()
            unit = unit_from_text("\n".join([preamble, sub_question, answer]))
            is_long = "所見を述べ" in sub_question or (word_limit.isdigit() and int(word_limit) >= 2500)
            source_ref = f"{year} 生保2 問3({major_no})({sub_no})"
            memory_id = f"PEM-II-{slug(year)}-3-{major_no}-{sub_id(sub_no)}-W"
            if is_long:
                cards.append(
                    MemoryCard(
                        memory_id=memory_id,
                        parent_memory_id="",
                        year=year,
                        part="II",
                        problem_no=f"3({major_no})",
                        sub_no=sub_no,
                        unit=unit,
                        question_type="part2_long_context",
                        points=points,
                        word_limit=word_limit,
                        source_ref=source_ref,
                        source_path=rel(path),
                        answer_source=rel(path),
                        wb_origin="non_wb",
                        card_type="whole",
                        deck=UNIT_INFO[unit],
                        priority="B",
                        status="long_context",
                        question=format_front("\n\n".join([preamble, sub_question]).strip(), source_ref, points, word_limit),
                        answer="",
                    )
                )
                continue
            if not answer:
                cards.append(
                    MemoryCard(
                        memory_id=memory_id,
                        parent_memory_id="",
                        year=year,
                        part="II",
                        problem_no=f"3({major_no})",
                        sub_no=sub_no,
                        unit=unit,
                        question_type="part2_small",
                        points=points,
                        word_limit=word_limit,
                        source_ref=source_ref,
                        source_path=rel(path),
                        answer_source=rel(path),
                        wb_origin="non_wb",
                        card_type="whole",
                        deck=UNIT_INFO[unit],
                        priority="A",
                        status="needs_answer",
                        question=format_front("\n\n".join([preamble, sub_question]).strip(), source_ref, points, word_limit),
                        answer="",
                    )
                )
                continue
            card = MemoryCard(
                memory_id=memory_id,
                parent_memory_id="",
                year=year,
                part="II",
                problem_no=f"3({major_no})",
                sub_no=sub_no,
                unit=unit,
                question_type="part2_small",
                points=points,
                word_limit=word_limit,
                source_ref=source_ref,
                source_path=rel(path),
                answer_source=rel(path),
                wb_origin="non_wb",
                card_type="whole",
                deck=UNIT_INFO[unit],
                priority="A",
                status="carded",
                question=format_front("\n\n".join([preamble, sub_question]).strip(), source_ref, points, word_limit),
                answer=answer,
            )
            cards.append(card)
            cards.extend(add_chunks(card))
    return cards


def build_part2_memory_cards() -> list[MemoryCard]:
    cards: list[MemoryCard] = []
    for path in sorted(SHOKEN_YEAR_DIR.glob("*.md")):
        if path.stem.removesuffix("H") not in {"H23", "H24", "H25", "H26", "H27", "H28", "H29", "2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025"}:
            continue
        cards.extend(parse_year_file(path))
    return cards


def write_readme() -> None:
    text = """# 生保2 過去問丸暗記

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
"""
    write_text(OUTPUT_DIR / "README.md", text)


def index_row(card: MemoryCard) -> dict[str, str]:
    return {field: getattr(card, field) for field in INDEX_FIELDS}


def card_markdown(card: MemoryCard) -> str:
    lines = [
        f"## CARD {card.memory_id}",
        "",
        f"- memory_id: {card.memory_id}",
        f"- parent_memory_id: {card.parent_memory_id}",
        f"- card_type: {card.card_type}",
        f"- deck: {card.deck}",
        f"- tags: past_exam_memory unit_{card.unit} part_{card.part} priority_{card.priority}",
        f"- source_ref: {card.source_ref}",
        f"- answer_source: {card.answer_source}",
        "",
        "### 問題",
        card.question.strip(),
        "",
    ]
    if card.card_type == "cloze":
        lines.extend(["### Cloze", card.cloze.strip(), ""])
    else:
        lines.extend(["### 暗記答案", card.answer.strip(), ""])
    return "\n".join(lines).strip() + "\n"


def write_cards(cards: list[MemoryCard]) -> None:
    grouped: dict[str, list[MemoryCard]] = {unit: [] for unit in UNIT_INFO}
    for card in cards:
        if card.status != "carded":
            continue
        grouped.setdefault(card.unit, []).append(card)
    for unit, unit_cards in grouped.items():
        if not unit_cards:
            continue
        body = [f"# {unit} Ankiカード", ""]
        for card in unit_cards:
            body.append(card_markdown(card))
        write_text(CARDS_DIR / f"{unit}.md", "\n".join(body).strip() + "\n")


def write_units(cards: list[MemoryCard], understanding_by_parent: dict[str, str]) -> None:
    grouped: dict[str, list[MemoryCard]] = {unit: [] for unit in UNIT_INFO}
    for card in cards:
        if card.card_type != "whole":
            continue
        grouped.setdefault(card.unit, []).append(card)
    for unit, unit_cards in grouped.items():
        if not unit_cards:
            continue
        guide = UNIT_GUIDES.get(unit, {})
        lines = [
            f"# {unit}",
            "",
            "このファイルは理解補助用です。Anki の暗記答案には、この理解メモを混ぜません。",
            "",
            "## 単元の大枠",
            "",
            "\n\n".join(guide.get("big_picture", [])),
            "",
            "## 暗記事項の位置づけ",
            "",
            guide.get("position", ""),
            "",
        ]
        for card in unit_cards:
            lines.extend(
                [
                    f"## {card.memory_id} {card.source_ref}",
                    "",
                    f"- status: {card.status}",
                    f"- card_type: {card.card_type}",
                    f"- deck: {card.deck}",
                    f"- source_path: {card.source_path}",
                    "",
                    "### 原問題",
                    card.question.strip(),
                    "",
                    "### 暗記対象原文",
                    card.answer.strip() if card.answer else "（長文所見のため初回は全文暗記カード化しない）",
                    "",
                    "### 根本解説",
                    root_explanation(card),
                    "",
                    "### 理解メモ",
                    understanding_by_parent.get(card.memory_id, "").strip() or "未作成。暗記対象原文には混ぜない。",
                    "",
                ]
            )
        write_text(UNITS_DIR / f"{unit}.md", "\n".join(lines).strip() + "\n")


def write_index(cards: list[MemoryCard]) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with (OUTPUT_DIR / "past_exam_index.csv").open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=INDEX_FIELDS)
        writer.writeheader()
        for card in cards:
            writer.writerow(index_row(card))


def main() -> None:
    source_cards = parse_first_part_cards()
    first_cards, understanding_by_parent = build_first_part_memory_cards(source_cards)
    part2_cards = build_part2_memory_cards()
    all_cards = first_cards + part2_cards

    write_readme()
    write_index(all_cards)
    write_units(all_cards, understanding_by_parent)
    write_cards(all_cards)

    carded = [card for card in all_cards if card.status == "carded"]
    long_context = [card for card in all_cards if card.status == "long_context"]
    needs_answer = [card for card in all_cards if card.status == "needs_answer"]
    print(f"index={len(all_cards)}")
    print(f"carded={len(carded)}")
    print(f"long_context={len(long_context)}")
    print(f"needs_answer={len(needs_answer)}")
    print(f"units={UNITS_DIR}")
    print(f"cards={CARDS_DIR}")


if __name__ == "__main__":
    main()
