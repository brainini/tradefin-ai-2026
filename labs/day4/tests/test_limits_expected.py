"""한도 엔진의 '기대값 테스트' 5개 — 4일차 기준 결과의 숫자와 맞는지 본다(4일차 14:45부터 받는 파일).

속성 테스트(test_limits_props.py)가 '어떤 답이든 지킬 규칙'이라면, 이쪽은 '이 데이터와 이 설계에서 나와야 하는 답'이다.
총액 비율(TotalCapShare) 70% 기준값이므로 정책 실험(예: 80%)에서는 일부러 어긋난다 — 어긋난 폭이 곧 실험 결과다.
같은 계수의 바이어끼리 한도를 나누는 방식은 솔버마다 달라서, 바이어별 한도가 아니라 목적함수 · 걸린 제약 · 잠재가격으로 비교한다.
실행   uv run pytest labs/day4/tests/test_limits_expected.py -q   (다른 결과 파일은 --result 경로)
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_RESULT = ROOT / "workbench" / "day4" / "outputs" / "limits_proposed.xlsx"


@pytest.fixture(scope="module")
def sheets(request) -> dict[str, pd.DataFrame]:
    opt = request.config.getoption("--result")
    path = (Path(opt) if Path(opt).is_absolute() else ROOT / opt) if opt else DEFAULT_RESULT
    if not path.exists():
        pytest.fail(f"결과 파일이 없다 — 먼저 엔진을 돌린다: uv run python scripts/limits_lp.py  (찾은 곳: {path})")
    return pd.read_excel(path, sheet_name=None)


def test_objective_value(sheets):
    obj = float(sheets["summary"].iloc[0]["objective"])
    assert obj == pytest.approx(3_135_799.48, rel=1e-4), f"목적함수 {obj:,.2f} (기대 3,135,799.48 ± 0.01%)"


def test_binding_constraints(sheets):
    con = sheets["constraints"]
    binding = set(con.loc[(con["slack"].abs() <= 1.0) & (con["shadow_price"] > 1e-6), "name"])
    assert binding == {"total_cap", "ctry_NGA"}, f"걸린 제약 {sorted(binding)} (기대 total_cap · ctry_NGA)"


def test_shadow_prices(sheets):
    price = dict(zip(sheets["constraints"]["name"], sheets["constraints"]["shadow_price"]))
    assert price["total_cap"] == pytest.approx(0.6723, abs=1e-3)
    assert price["ctry_NGA"] == pytest.approx(1.3959, abs=1e-3)


def test_total_limit_equals_cap(sheets):
    total = float(sheets["limits"]["L"].sum())
    assert total == pytest.approx(2_600_000, abs=1.0), f"한도 합계 {total:,.2f} (기대 2,600,000 ± 1)"


def test_approval_and_increase_counts(sheets):
    lim = sheets["limits"]
    need_ok = int((lim["approval"] == "사람 승인 필요").sum())
    increased = int((lim["L"] > lim["current_limit"] + 0.5).sum())
    assert (need_ok, increased) == (68, 22), f"사람 승인 필요 {need_ok}곳 · 증액 {increased}곳 (기대 68 · 22)"
