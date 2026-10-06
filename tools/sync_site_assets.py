#!/usr/bin/env python
"""Day1 수강생용 파일을 과정 사이트(docs/downloads/day1/)로 복사하고, 페이지에 끼워 넣을 '파일 받기' 표를 만든다.

사용 (저장소 루트에서, 표준 라이브러리만 사용):
    python tools/sync_site_assets.py            # 복사 + 표 갱신. 빠진 파일은 경고만 하고 계속한다
    python tools/sync_site_assets.py --check    # 아무것도 바꾸지 않고 상태만 출력(빠진 파일이 있으면 종료코드 1)
    python tools/sync_site_assets.py --strict   # 복사하되, 빠진 파일이 하나라도 있으면 종료코드 1

원칙
- 아래 DAY1_FILES 허용 목록(allowlist)에 있는 '수강생용' 파일만 복사한다.
  강사 정답(instructor/…/answers), data/raw/(정답 컬럼 포함), data/checkpoints/(다음 날 정답본)는 절대 복사하지 않는다.
  (허용 목록에 금지 경로가 섞이면 즉시 중단한다.)
- 아직 만들어지지 않은 파일은 건너뛴다. 사이트 표에는 '준비 중'으로 나오고 링크를 걸지 않으므로
  `mkdocs build --strict`가 깨지지 않는다. 파일이 생긴 뒤 이 스크립트를 다시 돌리면 링크가 생긴다.
- docs/downloads/day1/ 안에서 허용 목록 밖의 파일은 지운다(예전에 잘못 들어간 파일 정리).
- 같은 파일들을 묶은 day1_files.zip(압축 안 폴더 이름 D1/)도 만든다 — 수강생이 한 번에 받을 수 있게.

결과물
    docs/downloads/day1/...                    배포용 사본(.gitignore 대상 — 원본은 data/·labs/에 있다)
    docs/_snippets/day1/files_*.md             Day1·Lab 페이지에 끼워 넣는 표(mkdocs.yml에서 사이트 빌드 제외)
"""

from __future__ import annotations

import argparse
import shutil
import sys
import zipfile
from dataclasses import dataclass, field
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DOCS = REPO / "docs"
DEST = DOCS / "downloads" / "day1"
SNIP = DOCS / "_snippets" / "day1"
ZIP_NAME = "day1_files.zip"
ZIP_ROOT = "D1"

# 경로에 이 조각이 들어 있으면 수강생용이 아니다 — 허용 목록 실수 방지용 안전장치
FORBIDDEN_PARTS = (
    "instructor/",
    "answers",
    "data/raw/",
    "data/checkpoints/",
    "expected",
    "_clean",
    "dirt_log",
    "code_table",
)


@dataclass
class Item:
    src: str  # 저장소 루트 기준 원본 경로
    dest: str  # docs/downloads/day1/ 기준 경로
    title: str  # 표에 쓰는 짧은 이름
    desc: str  # 무엇인가(한 줄)
    labs: tuple[str, ...]  # 쓰는 곳: lab1 / lab2 / lab3 / data
    track: str  # 🟢 / 🔵 / 🟣 / 확장
    note_missing: str = "준비 중"
    exists: bool = field(default=False, init=False)
    size: int = field(default=0, init=False)


# 보고서 폴더(data/day1/reports/*.md)는 폴더째 허용한다. 알려진 파일은 아래 설명을 쓰고,
# 새로 생긴 .md는 기본 설명으로 표에 들어간다.
REPORT_INFO = {
    "halden_fictional_annual_report.md": (
        "Halden(가상) 연차보고서 발췌",
        "가상 영국 유통 바이어의 연차보고서(FY2026). Lab1 1–3단계에서 AI에 올린다",
        ("lab1",),
        "🟢",
    ),
    "irobot.md": (
        "iRobot 10-K FY2024 발췌",
        "실제 SEC 공시 발췌(영어 원문 그대로). Lab1 4단계",
        ("lab1",),
        "🟢",
    ),
    "plug_power.md": (
        "Plug Power 공시 3건 발췌",
        "PART A 10-Q 2023년 3분기 · PART B 10-K FY2023 · PART C 10-K FY2024. Lab1 Standard",
        ("lab1",),
        "🔵",
    ),
    "wolfspeed.md": (
        "Wolfspeed 10-Q 발췌",
        "2025-03-30 분기 보고서 발췌. 다 했으면(확장)",
        ("lab1",),
        "확장",
    ),
    "big_lots.md": (
        "Big Lots 10-Q 발췌",
        "2024-05-04 분기 보고서 발췌. 다 했으면(확장)",
        ("lab1",),
        "확장",
    ),
    "gorman_note.md": (
        "D&B 샘플(Gorman) 안내",
        "D&B 샘플 신용보고서 링크와 읽기 안내만 있다(PDF는 링크에서 직접 받는다). 확장",
        ("lab1",),
        "확장",
    ),
    "README.md": (
        "보고서 폴더 안내",
        "파일 목록·인용 찾는 요령·단위 주의·이용 조건",
        ("lab1",),
        "🟢",
    ),
}
REPORT_ORDER = [
    "halden_fictional_annual_report.md",
    "irobot.md",
    "plug_power.md",
    "wolfspeed.md",
    "big_lots.md",
    "gorman_note.md",
    "README.md",
]


def build_items() -> list[Item]:
    items = [
        Item("labs/day1/d1_end_eda_template.xlsx", "d1_end_eda_template.xlsx", "실습 템플릿",
             "시트 00_코드표 ~ 07_내AX프로젝트. 오늘 결과를 모두 여기에 모아 제출한다",
             ("lab1", "lab2", "lab3"), "🟢"),
    ]
    report_dir = REPO / "data" / "day1" / "reports"
    names = list(REPORT_ORDER)
    if report_dir.is_dir():
        names += sorted(p.name for p in report_dir.glob("*.md") if p.name not in REPORT_INFO)
    for name in names:
        title, desc, labs, track = REPORT_INFO.get(
            name, (name, "Day1 보고서 발췌(추가 자료)", ("lab1",), "확장")
        )
        items.append(Item(f"data/day1/reports/{name}", f"reports/{name}", title, desc, labs, track))
    items += [
        Item("data/day1/real_buyers_ratios.csv", "real_buyers_ratios.csv", "SEC 추출 비율표(CSV)",
             "SEC companyfacts API에서 뽑은 4개사 원값과 4대 비율(9행). AI 숫자를 대조한다",
             ("lab1",), "🟢"),
        Item("data/day1/real_buyers_ratios.xlsx", "real_buyers_ratios.xlsx", "SEC 추출 비율표(엑셀)",
             "같은 내용 + 열 설명(dictionary)·출처(source) 시트", ("lab1",), "🟢"),
        Item("data/day1/d1_buyers_raw.xlsx", "d1_buyers_raw.xlsx", "바이어 스냅샷(엑셀)",
             "(가상) 한빛정밀 해외 바이어 현황 153행 · 시트 buyers · 기준일 2026-09-30 · 원천 입력 오류 포함",
             ("lab2",), "🟢"),
        Item("data/day1/d1_buyers_raw.csv", "d1_buyers_raw.csv", "바이어 스냅샷(CSV)",
             "같은 내용 CSV(UTF-8 BOM). 엑셀 파일이 안 올라가는 AI 도구와 Colab(Challenge B-8)에서 쓴다",
             ("lab2",), "🟢"),
        Item("data/data_dictionary.xlsx", "data_dictionary.xlsx", "데이터 사전",
             "컬럼 뜻·단위(columns), 코드표(codes), 결제조건 표기 → 코드(payment_terms_map)",
             ("lab2", "data"), "🟢"),
        Item("labs/day1/ax_canvas_template.md", "ax_canvas_template.md", "AX 캔버스 양식",
             "내 AX 프로젝트 캔버스 7칸 + 과업 선정 3기준(메모장·워드에 붙여 써도 된다)",
             ("lab3",), "🟢"),
        Item("labs/day1/d1_challenge.ipynb", "d1_challenge.ipynb", "Challenge 노트북",
             "Colab용. A: SEC API로 비율 계산 · B: 인보이스 원장 분석(DPD·코호트·롤레이트·DSO)",
             ("lab1", "lab2"), "🟣"),
        Item("data/day1/d1_invoices.xlsx", "d1_invoices.xlsx", "인보이스 원장(엑셀)",
             "인보이스 5,033건(36개월) · 시트 invoices. Challenge B", ("lab2",), "🟣"),
        Item("data/day1/d1_invoices.csv", "d1_invoices.csv", "인보이스 원장(CSV)",
             "같은 내용 CSV(UTF-8 BOM). Colab에 올릴 때 쓴다", ("lab2",), "🟣"),
    ]
    return items


def guard(items: list[Item]) -> None:
    for it in items:
        low = it.src.lower()
        bad = [p for p in FORBIDDEN_PARTS if p in low]
        if bad or ".." in Path(it.dest).parts or Path(it.dest).is_absolute():
            sys.exit(f"[중단] 수강생용이 아닌 경로가 허용 목록에 있습니다: {it.src} (금지 조각: {bad})")


def human_size(n: int) -> str:
    if n >= 1024 * 1024:
        return f"{n / 1024 / 1024:.1f} MB"
    return f"{max(1, round(n / 1024)):,} KB"


def copy_files(items: list[Item], dry: bool) -> None:
    expected = {it.dest for it in items} | {ZIP_NAME}
    if not dry:
        DEST.mkdir(parents=True, exist_ok=True)
        # 허용 목록 밖 파일 정리
        for p in sorted(DEST.rglob("*"), reverse=True):
            rel = p.relative_to(DEST).as_posix()
            if p.is_file() and rel not in expected:
                p.unlink()
                print(f"  - 삭제(허용 목록 밖): downloads/day1/{rel}")
            elif p.is_dir() and not any(p.iterdir()):
                p.rmdir()
    for it in items:
        src = REPO / it.src
        it.exists = src.is_file()
        if not it.exists:
            stale = DEST / it.dest
            if not dry and stale.exists():
                stale.unlink()
            print(f"  ! 없음(건너뜀): {it.src}")
            continue
        it.size = src.stat().st_size
        if not dry:
            out = DEST / it.dest
            out.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, out)
        print(f"  + {it.src}  →  docs/downloads/day1/{it.dest}  ({human_size(it.size)})")


def make_zip(items: list[Item]) -> int:
    """있는 파일만 묶는다. 같은 내용이면 같은 zip이 나오도록 날짜를 고정한다."""
    path = DEST / ZIP_NAME
    present = [it for it in items if it.exists]
    if not present:
        if path.exists():
            path.unlink()
        return 0
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for it in sorted(present, key=lambda x: x.dest):
            info = zipfile.ZipInfo(f"{ZIP_ROOT}/{it.dest}", date_time=(2026, 10, 14, 9, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, (DEST / it.dest).read_bytes())
    return path.stat().st_size


LAB_LABEL = {"lab1": "Lab1", "lab2": "Lab2", "lab3": "Lab3", "data": "참고용"}


def link(it: Item, prefix: str) -> str:
    if not it.exists:
        return it.note_missing
    fname = Path(it.dest).name
    return f'[:material-download: 받기]({prefix}{it.dest}){{ download="{fname}" }}'


def table_all(items: list[Item], prefix: str, zip_size: int) -> str:
    lines = [
        "<!-- 자동 생성: tools/sync_site_assets.py — 직접 고치지 말고 스크립트를 다시 돌리세요 -->",
        "",
        "| 파일 | 무엇인가 | 쓰는 곳 | 크기 | 받기 |",
        "|---|---|---|---|---|",
    ]
    if zip_size:
        lines.append(
            f"| **`{ZIP_NAME}`**<br>**한 번에 받기** | 아래 파일 전부를 `{ZIP_ROOT}` 폴더 하나로 묶은 압축 파일."
            f" 보고서 발췌(.md)는 `{ZIP_ROOT}/reports` 폴더 안에 있다"
            f" | 전체 | {human_size(zip_size)} | [:material-folder-download: **받기**]({prefix}{ZIP_NAME})"
            f'{{ download="{ZIP_NAME}" }} |'
        )
    for it in items:
        where = " · ".join(LAB_LABEL[x] for x in it.labs)
        size = human_size(it.size) if it.exists else "–"
        lines.append(
            f"| `{Path(it.dest).name}`<br>{it.title} | {it.desc} | {where} {it.track} | {size} | {link(it, prefix)} |"
        )
    missing = [it for it in items if not it.exists]
    if missing:
        lines += [
            "",
            '!!! note "준비 중인 파일"',
            "    '준비 중'으로 표시된 파일은 강사가 올리는 대로 이 표에 링크가 생깁니다."
            " 화면을 새로 고쳐도 없으면 강사에게 알려 주세요.",
        ]
    return "\n".join(lines) + "\n"


def table_lab(items: list[Item], lab: str, prefix: str) -> str:
    lines = [
        "<!-- 자동 생성: tools/sync_site_assets.py — 직접 고치지 말고 스크립트를 다시 돌리세요 -->",
        "",
        "| 파일 | 무엇인가 | 트랙 | 받기 |",
        "|---|---|---|---|",
    ]
    for it in items:
        if lab in it.labs:
            lines.append(f"| `{Path(it.dest).name}` | {it.desc} | {it.track} | {link(it, prefix)} |")
    return "\n".join(lines) + "\n"


def write_snippets(items: list[Item], zip_size: int, dry: bool) -> None:
    outputs = {
        "files_all.md": table_all(items, "../downloads/day1/", zip_size),  # docs/day1/*.md 용
        "files_all_root.md": table_all(items, "downloads/day1/", zip_size),  # docs/*.md 용
        "files_lab1.md": table_lab(items, "lab1", "../downloads/day1/"),
        "files_lab2.md": table_lab(items, "lab2", "../downloads/day1/"),
        "files_lab3.md": table_lab(items, "lab3", "../downloads/day1/"),
    }
    if dry:
        return
    SNIP.mkdir(parents=True, exist_ok=True)
    for name, text in outputs.items():
        (SNIP / name).write_text(text, encoding="utf-8")
        print(f"  * 표 갱신: docs/_snippets/day1/{name}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true", help="아무것도 바꾸지 않고 상태만 확인")
    ap.add_argument("--strict", action="store_true", help="빠진 파일이 있으면 종료코드 1")
    args = ap.parse_args()

    items = build_items()
    guard(items)
    print(f"[sync_site_assets] 저장소: {REPO}")
    copy_files(items, dry=args.check)
    zip_size = 0 if args.check else make_zip(items)
    if zip_size:
        print(f"  + 묶음: docs/downloads/day1/{ZIP_NAME} ({human_size(zip_size)})")
    write_snippets(items, zip_size, dry=args.check)

    prompts = REPO / "labs" / "day1" / "prompts.md"
    if not prompts.is_file():
        print("  ! labs/day1/prompts.md 가 아직 없습니다 — 프롬프트 라이브러리 페이지가 비어 보입니다.")

    missing = [it.src for it in items if not it.exists]
    print(f"[sync_site_assets] 허용 목록 {len(items)}개 중 {len(items) - len(missing)}개 준비됨, {len(missing)}개 없음")
    if missing and (args.check or args.strict):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
