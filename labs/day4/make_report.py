#!/usr/bin/env python3
"""make_report.py(참고판 · 4일차 15:00 공개) — 지표 JSON(숫자) + narrative.json(해석 문장)으로 경영진 신용 리스크 리포트(.docx)를 만든다.

표의 숫자는 narrative 가 아니라 지표 JSON 에서 코드가 직접 채운다. 문장만 narrative.json 에서 온다.
채우기 전에 핵심 숫자를 원본에서 다시 계산해 지표 JSON 과 맞는지 보고, 다르면 멈춘다(종료 코드 1).
저장소 맨 위 폴더에서:  uv run python labs/day4/make_report.py [--input …] [--narrative …] [--out …]
처음 한 번 docxtpl 이 필요하다:  uv add docxtpl   (Claude Code 가 물으면 승인)

읽는 것                                                   쓰는 것
  labs/day4/report_template.docx  (docxtpl 템플릿 · 읽기만)        workbench/day4/outputs/credit_report_YYYY-MM.docx
  지표 JSON = workbench/day4/data/d4_report_input.json              (YYYY-MM 은 as_of 에서)
              (없으면 data/checkpoints/d4_report_input.json, 내가 만든 workbench/day4/outputs/report_input.json)
  workbench/day4/outputs/narrative.json  (형식은 labs/day4/report_schema.json)
  재검산: data/checkpoints/d4_start_scored.csv · d4_open_inv.csv · (있으면) workbench/day4/outputs/limits_proposed.xlsx

표시 규칙: USD 는 달러 단위 반올림 + 천 단위 쉼표 · 비율은 % 소수 한 자리 · 원화는 억 단위 소수 한 자리 ·
  반올림은 사사오입(ROUND_HALF_UP). 지표 JSON 을 내가 만들 때도 같은 규칙으로 쓴다.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
import zipfile
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

import pandas as pd

try:
    from docxtpl import DocxTemplate
    from jinja2 import Environment, StrictUndefined
except ImportError:
    sys.exit("멈춤: docxtpl 이 없습니다 — 터미널에서 'uv add docxtpl' 을 실행한 뒤 다시 돌립니다.")

ROOT = Path(__file__).resolve().parents[2]
CK = ROOT / "data" / "checkpoints"
OUT = ROOT / "workbench" / "day4" / "outputs"
INPUT_CANDIDATES = [ROOT / "workbench" / "day4" / "data" / "d4_report_input.json", CK / "d4_report_input.json", OUT / "report_input.json"]


def default_input() -> Path:
    """지표 JSON 의 기본 위치 — 작업 사본 → 원본 → 내가 만든 파일 순으로 먼저 있는 것."""
    return next((p for p in INPUT_CANDIDATES if p.exists()), INPUT_CANDIDATES[0])
TEMPLATE = ROOT / "labs" / "day4" / "report_template.docx"
LC_OR_ADV = {"LC_SIGHT", "LC_USANCE", "TT_ADV"}
STATUS = "권고(사람 승인 전)"


# --- 표시 형식 ---------------------------------------------------------------------------------
def _round(x: float, places: int) -> Decimal:
    return Decimal(str(x)).quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP)


def usd(x: float) -> str:
    """달러 단위 반올림 + 천 단위 쉼표 — 4290900.93 → '4,290,901'"""
    return f"{_round(x, 0):,}"


def pct(x: float) -> str:
    """비율 → % 소수 한 자리 — 0.6815 → '68.2%'"""
    return f"{_round(x * 100, 1)}%"


def krw_eok(x: float) -> str:
    """원 → 억 원 소수 한 자리 — 5835625265 → '58.4억 원'"""
    return f"{_round(x / 1e8, 1):,}억 원"


def count(x: int) -> str:
    return f"{int(x):,}"


def build_context(ri: dict, nar: dict) -> dict:
    """템플릿 자리표시자와 같은 키 구조 — 숫자는 report_input.json 값을 문자열로 바꿔 넣는다."""
    p, lim, al = ri["portfolio"], ri["limits"], ri["alerts"]
    return {
        "as_of": ri["as_of"],
        "portfolio": {
            "total_ar_usd": usd(p["total_ar_usd"]),
            "total_ar_krw": krw_eok(p["total_ar_krw"]),
            "krw_per_usd": count(p["krw_per_usd"]),
            "insured_share": pct(p["insured_share"]),
            "grade_counts": {g: count(n) for g, n in p["grade_counts"].items()},
            "c_ar_usd": usd(p["c_ar_usd"]),
        },
        "limits": {
            "current_eligible": usd(lim["current_eligible"]),
            "proposed": usd(lim["proposed"]),
            "cut30": count(lim["cut30"]),
            "increase": count(lim["increase"]),
            "binding": {k: f"{v:.4f}" for k, v in lim["binding"].items()},
            "objective": usd(lim["objective"]),
        },
        "scenarios": {
            sid: {
                "name_ko": s["name_ko"],
                "pd_multiplier": f"{s['pd_multiplier']:.1f}",
                "usd_krw_level": count(s["usd_krw_level"]),
                "el_usd": usd(s["el_usd"]),
                "mc_p95_usd": usd(s["mc_p95_usd"]) if "mc_p95_usd" in s else "–",
                "mc_p99_usd": usd(s["mc_p99_usd"]) if "mc_p99_usd" in s else "–",
            }
            for sid, s in ri["scenarios"].items()
        },
        "alerts": {
            "d30": {"count": count(al["d30"]["count"]), "amount_usd": usd(al["d30"]["amount_usd"])},
            "ship_hold": count(al["ship_hold"]),
            "notice_soon": count(al["notice_soon"]),
            "notice_overdue": count(al["notice_overdue"]),
        },
        "top5": [
            {
                "buyer_id": r["buyer_id"], "country": r["country"], "grade": r["grade"],
                "pd_30d": pct(r["pd_30d"]), "open_ar_usd": usd(r["open_ar_usd"]),
                "oldest_dpd": count(r["oldest_dpd"]), "alert": r["alert"], "top_reasons_ko": r["top_reasons_ko"],
            }
            for r in ri["top5"]
        ],
        "savings": {k: usd(v) for k, v in ri["savings"].items()},
        "basis": ri["basis"],
        # 문장은 narrative.json 에서 그대로
        "summary": nar["summary"],
        "sections": nar["sections"],
        "actions": nar["actions"],
        "assumptions": nar["assumptions"],
    }


# --- narrative.json 형식 검사(report_schema.json 의 규칙을 손으로) -----------------------------
def check_narrative(nar: dict) -> list[str]:
    errs: list[str] = []
    keys = {"summary", "sections", "actions", "assumptions", "number_trace"}
    if not isinstance(nar, dict):
        return ["맨 위가 JSON 객체가 아님"]
    errs += [f"필수 키 없음: {k}" for k in sorted(keys - nar.keys())]
    errs += [f"스키마에 없는 키: {k}" for k in sorted(nar.keys() - keys)]
    s = nar.get("summary")
    if not (isinstance(s, list) and len(s) == 3 and all(isinstance(x, str) for x in s)):
        errs.append("summary 는 문장 3개(위험 · 권고 · 결정 요청)의 배열이어야 함")
    sec = nar.get("sections")
    need = {"portfolio", "limits", "scenarios", "alerts"}
    if not isinstance(sec, dict) or sec.keys() != need or not all(isinstance(v, str) for v in sec.values()):
        errs.append(f"sections 는 {sorted(need)} 네 칸의 문자열이어야 함")
    acts = nar.get("actions")
    if not (isinstance(acts, list) and acts):
        errs.append("actions 는 1개 이상인 배열이어야 함")
    else:
        for i, a in enumerate(acts):
            if not isinstance(a, dict) or a.keys() != {"action", "approver", "status"}:
                errs.append(f"actions[{i}] 는 action · approver · status 세 칸이어야 함")
            elif a["status"] != STATUS:
                errs.append(f"actions[{i}].status 는 '{STATUS}' 이어야 함 (지금: {a['status']!r})")
    asm = nar.get("assumptions")
    if not (isinstance(asm, list) and asm and all(isinstance(x, str) for x in asm)):
        errs.append("assumptions 는 문장 1개 이상의 배열이어야 함")
    tr = nar.get("number_trace")
    if not isinstance(tr, list):
        errs.append("number_trace 는 배열이어야 함")
    else:
        for i, t in enumerate(tr):
            if not isinstance(t, dict) or t.keys() != {"number", "json_path"}:
                errs.append(f"number_trace[{i}] 는 number · json_path 두 칸이어야 함")
    return errs


# --- 재검산: report_input.json 의 핵심 숫자를 원본에서 다시 계산 --------------------------------
def recheck(ri: dict) -> tuple[list[dict], float]:
    scored = pd.read_csv(CK / "d4_start_scored.csv")
    inv = pd.read_csv(CK / "d4_open_inv.csv")
    limits_file = OUT / "limits_proposed.xlsx"

    total = float(scored["open_ar_usd"].sum())
    insured = float(scored.loc[scored["ksure_insured"] == "Y", "open_ar_usd"].sum()) / total
    # 선적 보류: alert_summary.json 을 옮기지 않고 인보이스에서 직접 —
    # 미결 · 기준일 대비 연체 30일 이상 · 신용장/선수금이 아닌 거래의 바이어 ∪ 파산 표시 바이어
    unpaid = inv[inv["paid"] == "N"]
    dpd = (pd.Timestamp(ri["as_of"]) - pd.to_datetime(unpaid["due_date"])).dt.days
    hold = set(unpaid.loc[(dpd >= 30) & ~unpaid["payment_method"].isin(LC_OR_ADV), "buyer_id"])
    hold |= set(scored.loc[scored["bankruptcy_flag"] == 1, "buyer_id"])
    rows = [
        {"항목": "총 미결 채권(USD)", "path": "portfolio.total_ar_usd", "input": ri["portfolio"]["total_ar_usd"],
         "recalc": round(total, 2), "ok": abs(ri["portfolio"]["total_ar_usd"] - total) <= 0.005,
         "근거": "d4_start_scored.csv · open_ar_usd 합"},
        {"항목": "부보 비중", "path": "portfolio.insured_share", "input": ri["portfolio"]["insured_share"],
         "recalc": round(insured, 6), "ok": round(insured, 4) == ri["portfolio"]["insured_share"],
         "근거": "d4_start_scored.csv · ksure_insured=='Y' 잔액 ÷ 전체(소수 4자리)"},
        {"항목": "선적 보류 바이어(곳)", "path": "alerts.ship_hold", "input": ri["alerts"]["ship_hold"],
         "recalc": len(hold), "ok": len(hold) == ri["alerts"]["ship_hold"],
         "근거": "d4_open_inv.csv 연체 ≥30일 · 신용장/선수금 제외 ∪ bankruptcy_flag"},
    ]
    if limits_file.exists():  # 실습 A 의 한도안이 있으면 합계도 대조한다 — 솔버마다 바이어별 소수점이 달라 달러 단위 오차(150곳 × 1달러 미만)는 허용
        proposed = float(pd.read_excel(limits_file, sheet_name="limits")["L"].sum())
        rows.append({"항목": "제안 한도 합계(USD)", "path": "limits.proposed", "input": ri["limits"]["proposed"],
                     "recalc": round(proposed), "ok": abs(proposed - ri["limits"]["proposed"]) <= 150,
                     "근거": "limits_proposed.xlsx · limits 시트 L 합(오차 150달러 이내)"})
    else:
        print("(한도안 limits_proposed.xlsx 가 없어 '제안 한도 합계' 재검산은 건너뜀 — 실습 A ②를 마치면 대조됩니다)\n")
    return rows, float(unpaid["amount_usd"].sum())


def leftover_tags(path: Path) -> list[str]:
    """만든 docx 안에 채워지지 않은 {{ · {% 가 남았는지"""
    with zipfile.ZipFile(path) as z:
        return [n for n in z.namelist() if n.startswith("word/") and n.endswith(".xml")
                and any(t in z.read(n).decode("utf-8") for t in ("{{", "{%", "}}", "%}"))]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--input", type=Path, default=default_input(), help="지표 JSON(기본: 작업 사본 → 원본 → 내가 만든 파일)")
    ap.add_argument("--narrative", type=Path, default=OUT / "narrative.json")
    ap.add_argument("--out", type=Path, default=None, help="기본: workbench/day4/outputs/credit_report_YYYY-MM.docx")
    args = ap.parse_args()

    ri = json.loads(args.input.read_text(encoding="utf-8"))
    if not args.narrative.exists():
        print(f"멈춤: {args.narrative} 이(가) 아직 없습니다 — labs/day4/report_schema.json 형식으로 해석 문장을 먼저 만드세요.")
        return 1
    nar = json.loads(args.narrative.read_text(encoding="utf-8"))
    errs = check_narrative(nar)
    if errs:
        print("멈춤: narrative.json 형식이 report_schema.json 과 다릅니다")
        print("\n".join(f"- {e}" for e in errs))
        return 1

    # 1) 재검산
    rows, inv_total = recheck(ri)
    print("## 재검산 (지표 JSON vs 원본)\n")
    print("| 항목 | json_path | report_input | 재계산 | 근거 | 결과 |\n|---|---|---|---|---|---|")
    for r in rows:
        print(f"| {r['항목']} | {r['path']} | {r['input']:,} | {r['recalc']:,} | {r['근거']} | {'✅' if r['ok'] else '❌ 다름'} |")
    print(f"\n참고: 인보이스 기준 미결 합(d4_open_inv.csv amount_usd) = {inv_total:,.2f} — 리포트 정의는 바이어 기준이라 비교만 보임")
    if not all(r["ok"] for r in rows):
        print("\n멈춤: 지표 JSON 이 원본과 다릅니다 — 입력 JSON 을 만든 코드를 다시 돌려 확인하세요. docx 는 만들지 않았습니다.")
        return 1

    # 2) 채우기
    ctx = build_context(ri, nar)
    tpl = DocxTemplate(TEMPLATE)
    env = Environment(undefined=StrictUndefined, autoescape=True)
    missing = tpl.get_undeclared_template_variables(env) - ctx.keys()
    if missing:
        print(f"멈춤: 템플릿이 쓰는 키가 context 에 없음: {sorted(missing)}")
        return 1
    tpl.render(ctx, env, autoescape=True)

    out = args.out or OUT / f"credit_report_{ri['as_of'][:7]}.docx"
    out.parent.mkdir(parents=True, exist_ok=True)
    tpl.save(out)
    left = leftover_tags(out)
    if left:
        print(f"멈춤: 채워지지 않은 자리표시자가 남음: {left}")
        return 1

    print(f"\nwrote {out}")
    print(f"표 숫자 예: 총 미결 {ctx['portfolio']['total_ar_usd']} USD · 부보 {ctx['portfolio']['insured_share']} · "
          f"원화 {ctx['portfolio']['total_ar_krw']} · 제안 한도 {ctx['limits']['proposed']} · 선적 보류 {ctx['alerts']['ship_hold']}곳")
    print("다음: uv run python labs/day4/check_numbers.py 로 문장 속 숫자를 대조하세요.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
