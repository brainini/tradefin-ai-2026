#!/usr/bin/env python3
"""d3_end_scored.csv 점검 — 3일차 실습 B의 최종 파일이 약속을 지키는지 본다(표준 라이브러리만 씁니다).

    python tools/check_scored.py                                   # 기본: workbench/day3/outputs/d3_end_scored.csv
    python tools/check_scored.py 내파일.csv --scoring data/checkpoints/d3_start_scoring.csv
    uv run python tools/check_scored.py                            # 내 PC에서는 이렇게 해도 된다

점검(✅ / ❌ / 건너뜀):
   1 파일이 있고 UTF-8로 읽힌다
   2 열이 정확히 6개 — buyer_id · ref_date · pd_30d · grade · threshold_used · model_version (이 순서)
   3 150행
   4 buyer_id가 겹치지 않는다 · (예측 대상 파일이 있으면) 그 150곳과 같다
   5 ref_date가 모두 2026-09-30
   6 pd_30d가 0~1 사이 숫자
   7 grade가 S · A · B · C 중 하나
   8 threshold_used가 0~1 사이 한 가지 값
   9 grade가 규칙(C ≥ t · B ≥ t/2 · A ≥ t/4 · 나머지 S)과 같다
  10 model_version이 비어 있지 않다
끝에 등급 분포를 보여 준다. ❌이 하나라도 있으면 종료 코드 1.
출력은 Markdown 표라서 GitHub Actions의 job summary($GITHUB_STEP_SUMMARY)에 그대로 쓸 수 있다.
"""
import argparse
import csv
import sys
from collections import Counter
from pathlib import Path

COLUMNS = ["buyer_id", "ref_date", "pd_30d", "grade", "threshold_used", "model_version"]
REF_DATE = "2026-09-30"
N_ROWS = 150
BOUNDARY_TOL = 1e-4   # pd_30d를 반올림해 저장하면 경계 바로 옆 행이 갈릴 수 있다 — 이 안쪽은 경고만 한다


def to_float(text: str):
    try:
        return float(text)
    except (TypeError, ValueError):
        return None


def expected_grade(p: float, t: float) -> str:
    if p >= t:
        return "C"
    if p >= t / 2:
        return "B"
    if p >= t / 4:
        return "A"
    return "S"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", nargs="?", default="workbench/day3/outputs/d3_end_scored.csv")
    ap.add_argument("--scoring", default="data/checkpoints/d3_start_scoring.csv",
                    help="예측 대상 150곳 파일 — 없으면 buyer_id 대조만 건너뛴다")
    ap.add_argument("--allow-extra", action="store_true", help="6열 말고 다른 열이 더 있어도 된다(강사 기준 파일용)")
    args = ap.parse_args()

    rows_out: list[tuple[str, str, str]] = []   # (점검, 결과, 설명)
    failed = False

    def add(name: str, ok, detail: str = "") -> None:
        nonlocal failed
        mark = "✅" if ok is True else ("건너뜀" if ok is None else "❌")
        if ok is False:
            failed = True
        rows_out.append((name, mark, detail))

    path = Path(args.file)
    rows: list[dict] = []
    header: list[str] = []
    try:
        text = path.read_bytes().decode("utf-8-sig")
        reader = csv.DictReader(text.splitlines())
        header = list(reader.fieldnames or [])
        rows = list(reader)
        add("1 파일 · UTF-8", True, f"`{path}`")
    except FileNotFoundError:
        add("1 파일 · UTF-8", False, f"`{path}` 파일이 없습니다")
    except UnicodeDecodeError:
        add("1 파일 · UTF-8", False, "UTF-8이 아닙니다 — 엑셀이면 'CSV UTF-8(쉼표로 분리)'로 다시 저장")

    if rows or header:
        ok_cols = header == COLUMNS or (args.allow_extra and header[: len(COLUMNS)] == COLUMNS)
        add("2 열 6개와 이름 · 순서", ok_cols, "" if ok_cols else f"읽은 열: {', '.join(header)}")
        add("3 150행", len(rows) == N_ROWS, f"{len(rows)}행")

        ids = [r.get("buyer_id", "") for r in rows]
        dup = [k for k, v in Counter(ids).items() if v > 1]
        detail = f"겹친 buyer_id: {', '.join(dup[:5])}" if dup else ""
        ok_ids: bool | None = not dup
        scoring = Path(args.scoring)
        if ok_ids and scoring.is_file():
            want = {r["buyer_id"] for r in csv.DictReader(scoring.read_bytes().decode("utf-8-sig").splitlines())}
            if set(ids) != want:
                ok_ids = False
                detail = f"예측 대상 150곳과 다릅니다(빠진 {len(want - set(ids))} · 더 있는 {len(set(ids) - want)})"
            else:
                detail = "예측 대상 150곳과 같습니다"
        elif ok_ids:
            detail = f"겹치지 않습니다(`{scoring}`이 없어 150곳 대조는 건너뜀)"
        add("4 buyer_id", ok_ids, detail)

        bad_date = sorted({r.get("ref_date", "") for r in rows if r.get("ref_date") != REF_DATE})
        add("5 ref_date = 2026-09-30", not bad_date, f"다른 값: {', '.join(bad_date[:3])}" if bad_date else "")

        ps = [to_float(r.get("pd_30d", "")) for r in rows]
        bad_p = [i + 2 for i, p in enumerate(ps) if p is None or not 0 <= p <= 1]
        add("6 pd_30d는 0~1 숫자", not bad_p, f"{len(bad_p)}행(첫 줄 {bad_p[0]}행)이 숫자가 아니거나 0~1 밖 — 0~100으로 저장했나요?" if bad_p else "")

        grades = [r.get("grade", "") for r in rows]
        bad_g = sorted({g for g in grades if g not in ("S", "A", "B", "C")})
        add("7 grade는 S · A · B · C", not bad_g, f"다른 값: {', '.join(repr(g) for g in bad_g[:4])}" if bad_g else "")

        ts = {to_float(r.get("threshold_used", "")) for r in rows}
        ok_t = len(ts) == 1 and None not in ts and 0 < next(iter(ts)) < 1
        add("8 threshold_used는 한 가지 값", ok_t, f"t = {next(iter(ts))}" if ok_t else f"읽은 값: {sorted(str(x) for x in ts)[:4]}")

        if ok_t and not bad_p and not bad_g:
            t = next(iter(ts))
            wrong = []
            near = []
            for i, (p, g) in enumerate(zip(ps, grades)):
                e = expected_grade(p, t)
                if e != g:
                    edges = (t, t / 2, t / 4)
                    (near if min(abs(p - x) for x in edges) <= BOUNDARY_TOL else wrong).append(f"{ids[i]}({g}→{e})")
            if wrong:
                add("9 grade = t 규칙", False, f"규칙과 다른 {len(wrong)}행: {', '.join(wrong[:5])} — IFS를 C부터 검사했나요?")
            elif near:
                add("9 grade = t 규칙", True, f"경계 바로 옆(반올림) {len(near)}행은 통과: {', '.join(near[:3])}")
            else:
                add("9 grade = t 규칙", True, "C ≥ t · B ≥ t/2 · A ≥ t/4 · 나머지 S")
        else:
            add("9 grade = t 규칙", None, "앞 점검(6 · 7 · 8)을 먼저 고치세요")

        mv = {r.get("model_version", "").strip() for r in rows}
        add("10 model_version", "" not in mv and bool(mv), f"{', '.join(sorted(mv)[:3])}" if "" not in mv else "빈 칸이 있습니다")

    verdict = "❌ 실패" if failed else "✅ 통과"
    out = [f"## d3_end_scored.csv 점검 — {verdict}", "", "| 점검 | 결과 | 설명 |", "|---|---|---|"]
    out += [f"| {n} | {m} | {d} |" for n, m, d in rows_out]
    if rows and not failed:
        dist = Counter(r["grade"] for r in rows)
        out += ["", "**등급 분포** — " + " · ".join(f"{g} {dist.get(g, 0)}곳" for g in "SABC")]
    if failed:
        out += ["", "❌ 줄을 먼저 고치세요. 병합 여부는 사람이 정합니다."]
    print("\n".join(out))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
