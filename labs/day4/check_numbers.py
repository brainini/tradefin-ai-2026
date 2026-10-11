#!/usr/bin/env python3
"""check_numbers.py(참고판 · 4일차 15:00부터 받는 파일) — narrative.json 문장 속 숫자를 지표 JSON 값과 기계적으로 대조한다.

문장(summary · sections · actions · assumptions)에서 숫자를 정규식으로 뽑고, number_trace 에 적힌 json_path 의 값과 비교한다.
진짜 숫자 불일치가 1건이라도 있으면 어디가 다른지 표로 보이고 종료 코드 1로 멈춘다.
저장소 맨 위 폴더에서:  uv run python labs/day4/check_numbers.py [--input …] [--narrative …] [--out …]

읽는 것                                                         쓰는 것
  지표 JSON = workbench/day4/data/d4_report_input.json            workbench/day4/outputs/number_trace.csv
              (없으면 data/checkpoints/d4_report_input.json,       (where · number · json_path · value · status, utf-8-sig)
               내가 만든 workbench/day4/outputs/report_input.json)
  workbench/day4/outputs/narrative.json

규칙
- 건너뛰는 숫자(이름 속 숫자): 날짜(2026-09-30 · 2026-09 · 9월 30일 · 2026년 9월), 영문+숫자 이름(S3 · B118 · D+30 · D-3 ·
  H.10 · P95 · top5), 금리 기간(3M), 조문(제15조 · 제2항), 기간 · 분위 이름(1개월 · 95% 분위).
- 정규화: 쉼표 제거 → 단위 배율(% · %p ×0.01 · 억 ×1e8 · 만 ×1e4 · 천 ×1e3) → 문장에 쓴 마지막 자리의 반까지 반올림 오차 허용
  (68.2% → ±0.05%p · 58.4억 → ±0.05억 · 429만 달러 → ±5천). 끝이 0 세 개 이상인 정수(4,291,000)는 그 자리 반까지 허용.
  부호는 '감소 · 증가'로 쓰는 일이 많아 절댓값으로 비교한다.
- 문장 숫자 ↔ trace 짝짓기: number_trace 에서 같은 숫자를 찾되, 문장의 단위(곳 · 건 · 일 · 배 · % · 달러 · 원)가
  json_path 의 단위와 맞는 항목만 쓴다(예: '21곳'은 건수인 alerts.d30.count 와 짝이 되지 않는다).
- json_path 값의 종류: 숫자 → 반올림 범위 비교 · 문자열 → 그 문자열 안에 같은 숫자가 있으면 맞음(basis.definitions.* 등) ·
  배열 → 길이와 비교(top5 → 5). 'a; b'처럼 둘 이상 적으면 모두 맞아야 한다. 괄호 속 메모('(필드명)')는 무시한다.
- status(실패): 값 다름 · 단위 다름(같은 숫자의 trace 가 다른 단위 항목뿐) · trace 없음 · 경로 없음(안 풀리거나 객체를 가리킴)
  status(경고만): 문장에 없음(trace 에만 있는 숫자) · 건너뜀(trace 에만 있는 이름 · 날짜 — B134 · S0 · 2026-09-30)
- 불일치 표는 같은 숫자 · 경로 · status 를 한 건으로 묶고, 나온 위치(where)를 모두 적는다.
- 한계: report_input.json 에 없는 파생 숫자('현행 대비 49% 감소')는 trace 없음이 된다 →
  문장에서 빼거나 지표 JSON(report_input.json)에 값을 더해 숫자의 근거를 한 곳에 둔다(계산은 코드가).
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

# 저장소 맨 위 폴더 = pyproject.toml이 있는 가장 가까운 위 폴더 — scripts/ 로 복사하거나 작업 사본 폴더에서 돌려도 같은 곳을 읽는다
ROOT = next((p for p in Path(__file__).resolve().parents if (p / "pyproject.toml").exists()), Path(__file__).resolve().parents[2])
OUT = ROOT / "workbench" / "day4" / "outputs"
INPUT_CANDIDATES = [ROOT / "workbench" / "day4" / "data" / "d4_report_input.json",
                    ROOT / "data" / "checkpoints" / "d4_report_input.json", OUT / "report_input.json"]


def default_input() -> Path:
    """지표 JSON 의 기본 위치 — 작업 사본 → 원본 → 내가 만든 파일 순으로 먼저 있는 것."""
    return next((p for p in INPUT_CANDIDATES if p.exists()), INPUT_CANDIDATES[0])

# 이름 속 숫자 — 먼저 가린다(순서대로)
SKIP_RES = [
    re.compile(r"\d{4}-\d{1,2}-\d{1,2}"),                       # 2026-09-30
    re.compile(r"\d{4}\.\s?\d{1,2}\.\s?\d{1,2}\.?"),            # 2026. 9. 30.
    re.compile(r"\d{4}-\d{2}(?!\d)"),                            # 2026-09
    re.compile(r"\d{4}\s*년(\s*\d{1,2}\s*월)?(\s*\d{1,2}\s*일)?"),  # 2026년 9월 30일
    re.compile(r"\d+\s*개월"),                                    # 1개월 (기간 이름 — '월'보다 먼저)
    re.compile(r"\d{1,2}\s*월(\s*\d{1,2}\s*일)?"),               # 9월 30일 · 9월
    re.compile(r"(?<![A-Za-z0-9])[A-Za-z][A-Za-z_]*[+\-_.]?\d+(?:\.\d+)?"),  # S3 · B118 · D+30 · D-3 · H.10 · P95 · top5
    re.compile(r"(?<![\d.,])\d+[MY](?![A-Za-z])"),               # 3M (금리 기간)
    re.compile(r"제\s*\d+\s*(조|항|호)"),                         # 제15조
    re.compile(r"\d+\s*일차"),                                    # 4일차
    re.compile(r"\d+(?:\.\d+)?\s*%?\s*분위"),                     # 95% 분위 (P95 의 다른 이름)
]
NUM_RE = re.compile(
    r"(?<![A-Za-z0-9.,])(?P<dollar>\$\s?)?(?P<int>\d{1,3}(?:,\d{3})+|\d+)(?:\.(?P<dec>\d+))?"
    r"\s?(?P<unit>%p|%|억\s?원|억|만\s?달러|만\s?원|만|천|원|달러|곳|건|일|배|개)?"
)
SCALE = {"%p": 0.01, "%": 0.01, "억": 1e8, "만": 1e4, "천": 1e3}
# json_path → 단위 종류(먼저 맞는 줄). 여기 없는 경로(잠재가격 등)는 단위를 따지지 않는다.
PATH_KINDS = [
    (re.compile(r"grade_counts\.\w+$|(^|\.)(ship_hold|cut30|increase)$"), "곳"),
    (re.compile(r"(^|\.)(count|notice_soon|notice_overdue)$"), "건"),
    (re.compile(r"(^|\.)oldest_dpd$"), "일"),
    (re.compile(r"(^|\.)pd_multiplier$"), "배"),
    (re.compile(r"(^|\.)(insured_share|pd_30d)$"), "pct"),
    (re.compile(r"(^|\.)(krw_per_usd|usd_krw_level|total_ar_krw)$"), "krw"),
    (re.compile(r"_usd$|^limits\.(current_eligible|proposed|objective)$|^savings\."), "usd"),
]
FAIL = {"값 다름", "단위 다름", "trace 없음", "경로 없음"}


@dataclass
class Num:
    raw: str          # 문장에 쓴 그대로
    value: float      # 단위 배율을 곱한 값(절댓값)
    tol: float        # 반올림 허용 오차
    kind: str | None  # 문장 단위의 종류(곳 · 건 · 일 · 배 · pct · usd · krw) — 없으면 None


def unit_kind(dollar: str | None, unit: str) -> str | None:
    if dollar or unit.endswith("달러"):
        return "usd"
    if unit in ("%", "%p"):
        return "pct"
    if unit.endswith("원") or unit == "억":
        return "krw"
    return unit if unit in ("곳", "건", "일", "배") else None


def parse_match(m: re.Match) -> Num:
    digits = m["int"].replace(",", "")
    dec = m["dec"] or ""
    unit = re.sub(r"\s", "", m["unit"] or "")
    scale = next((v for k, v in SCALE.items() if unit.startswith(k)), 1.0)
    if dec:
        tol = 0.5 * 10 ** -len(dec)
    else:
        zeros = len(digits) - len(digits.rstrip("0")) if digits.strip("0") else 0
        tol = 0.5 * 10 ** zeros if zeros >= 3 else 0.5
    value = float(f"{digits}.{dec}" if dec else digits)
    return Num(raw=m.group(0).strip(), value=value * scale, tol=tol * scale, kind=unit_kind(m["dollar"], unit))


def mask(text: str) -> str:
    for r in SKIP_RES:
        text = r.sub(lambda m: " " * len(m.group(0)), text)
    return text


def numbers_in(text: str) -> list[tuple[Num, int]]:
    """문장 속 숫자와 그 위치(이름 속 숫자는 건너뜀)"""
    return [(parse_match(m), m.start()) for m in NUM_RE.finditer(mask(text))]


def resolve(data, path: str):
    """'top5[0].pd_30d' · 'scenarios.S3.mc_p95_usd' → 값. 안 풀리면 KeyError"""
    tokens = re.findall(r"\[(\d+)\]|\.?([^.\[\]]+)", path)
    if "".join(f"[{i}]" if i else f".{k}" for i, k in tokens).lstrip(".") != path.strip():
        raise KeyError(path)
    cur = data
    for idx, key in tokens:
        try:
            cur = cur[int(idx)] if idx else cur[key]
        except (KeyError, IndexError, TypeError):
            raise KeyError(path) from None
    return cur


def is_number(x) -> bool:
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def close(n: Num, x: float) -> bool:
    return abs(n.value - abs(x)) <= n.tol + 1e-9 * max(1.0, abs(x))


@dataclass
class Target:
    """json_path 하나가 가리키는 값"""
    path: str
    value: object = None
    ok: bool = False      # 경로가 풀리고 비교할 수 있는 값(숫자 · 문자열 · 배열)인가
    kind: str | None = None

    def matches(self, n: Num) -> bool:
        if is_number(self.value):
            return close(n, self.value)
        if isinstance(self.value, str):   # 문자열 안에 같은 숫자가 있으면 맞음
            return any(close(n, m.value) for m, _ in numbers_in(self.value))
        if isinstance(self.value, list):  # 배열은 길이
            return close(n, len(self.value))
        return False


@dataclass
class Trace:
    i: int
    raw: str
    path: str
    num: Num | None
    targets: list[Target] = field(default_factory=list)
    used: bool = False

    def compatible(self, n: Num) -> bool:
        return all(t.kind is None or n.kind is None or t.kind == n.kind for t in self.targets)

    def status(self, n: Num) -> str:
        if not self.targets or not all(t.ok for t in self.targets):
            return "경로 없음"
        return "OK" if all(t.matches(n) for t in self.targets) else "값 다름"

    def shown_value(self) -> str:
        return "; ".join("" if t.value is None else str(t.value) for t in self.targets)


def build_trace(ri: dict, entries: list[dict]) -> list[Trace]:
    out = []
    for i, e in enumerate(entries):
        raw, path = str(e.get("number", "")), str(e.get("json_path", ""))
        found = numbers_in(raw)  # 이름 · 날짜('B134' · 'S0' · '2026-09-30')는 숫자가 없다 → None
        tr = Trace(i=i, raw=raw, path=path, num=found[0][0] if found else None)
        for p in (re.sub(r"\([^)]*\)", "", x).strip() for x in path.split(";")):
            if not p:
                continue
            t = Target(path=p)
            try:
                t.value = resolve(ri, p)
                t.ok = isinstance(t.value, (int, float, str, list)) and not isinstance(t.value, bool)
            except KeyError:
                pass
            if is_number(t.value):
                t.kind = next((k for r, k in PATH_KINDS if r.search(p)), None)
            tr.targets.append(t)
        out.append(tr)
    return out


def sentences(nar: dict) -> list[tuple[str, str]]:
    out = [(f"summary[{i}]", s) for i, s in enumerate(nar["summary"])]
    out += [(f"sections.{k}", v) for k, v in nar["sections"].items()]
    for i, a in enumerate(nar["actions"]):
        out += [(f"actions[{i}].{k}", a[k]) for k in ("action", "approver", "status")]
    out += [(f"assumptions[{i}]", s) for i, s in enumerate(nar["assumptions"])]
    return out


def match_sentence(n: Num, trace: list[Trace]) -> tuple[str, Trace | None]:
    cands = [t for t in trace if t.num and abs(t.num.value - n.value) <= 1e-9 * max(1.0, n.value)]
    if not cands:
        return "trace 없음", None
    compat = [t for t in cands if t.compatible(n)]
    if not compat:
        return "단위 다름", cands[0]
    # 같은 숫자 · 같은 단위의 trace 가 여럿이면 글자 그대로 같은 것('1.0' ↔ '1.0') → 값이 맞는 것 순으로 쓴다
    compat.sort(key=lambda c: (c.num.raw != n.raw, c.num.kind != n.kind))
    t = next((c for c in compat if c.status(n) == "OK"), compat[0])
    return t.status(n), t


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--input", type=Path, default=default_input(), help="지표 JSON(기본: 작업 사본 → 원본 → 내가 만든 파일)")
    ap.add_argument("--narrative", type=Path, default=OUT / "narrative.json")
    ap.add_argument("--out", type=Path, default=OUT / "number_trace.csv")
    args = ap.parse_args()

    ri = json.loads(args.input.read_text(encoding="utf-8"))
    if not args.narrative.exists():
        print(f"멈춤: {args.narrative} 이(가) 아직 없습니다.")
        return 1
    nar = json.loads(args.narrative.read_text(encoding="utf-8"))
    missing = [k for k in ("summary", "sections", "actions", "assumptions", "number_trace") if k not in nar]
    if missing:
        print(f"멈춤: narrative.json 에 필수 키가 없음: {missing}")
        return 1

    trace = build_trace(ri, nar["number_trace"])
    rows, bad = [], {}
    for where, text in sentences(nar):
        for n, pos in numbers_in(text):
            status, t = match_sentence(n, trace)
            if t and status != "단위 다름":
                t.used = True
            row = {"where": where, "number": n.raw, "json_path": t.path if t else "",
                   "value": t.shown_value() if t else "", "status": status}
            rows.append(row)
            if status in FAIL:
                key = (row["number"], row["json_path"], status)
                snippet = text[max(0, pos - 15): pos + len(n.raw) + 15].replace("\n", " ")
                bad.setdefault(key, {**row, "snippet": snippet, "wheres": []})["wheres"].append(where)

    for t in trace:
        if not t.used:
            rows.append({"where": f"number_trace[{t.i}]", "number": t.raw, "json_path": t.path,
                         "value": t.shown_value(), "status": "문장에 없음" if t.num else "건너뜀"})

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["where", "number", "json_path", "value", "status"])
        w.writeheader()
        w.writerows(rows)

    counts: dict[str, int] = {}
    for r in rows:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    print(f"wrote {args.out}  ({' · '.join(f'{k} {v}' for k, v in counts.items()) or '숫자 없음'})")
    for st in ("문장에 없음", "건너뜀"):
        warn = [r for r in rows if r["status"] == st]
        if warn:
            print(f"경고: number_trace 에만 있는 항목({st}) {len(warn)}건 — " + ", ".join(str(r["number"]) for r in warn))
    if bad:
        print(f"\n## 불일치 {len(bad)}건\n")
        print("| where | 문장 일부 | number | json_path | 입력값 | status |\n|---|---|---|---|---|---|")
        for b in bad.values():
            print(f"| {' · '.join(b['wheres'])} | …{b['snippet']}… | {b['number']} | {b['json_path'] or '–'} | "
                  f"{b['value'] or '–'} | {b['status']} |")
        print("\n멈춤: 문장 숫자를 고치거나 number_trace 를 바로잡으세요(숫자는 지표 JSON 에서만).")
        return 1
    print("문장 속 숫자가 모두 지표 JSON 과 맞습니다.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
