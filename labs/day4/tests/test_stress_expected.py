"""스트레스 시뮬레이터의 '기대값 테스트' — 강사 정답본의 숫자와 맞는지 본다(4일차 14:45 공개).

속성 테스트(test_stress_props.py)가 '어떤 시뮬레이션이든 지킬 성질'이라면, 이쪽은 '이 데이터와 이 설계에서 나와야 하는 숫자'다.
시나리오 S0–S4의 공식 기대손실은 계산식 하나라 정확히 같아야 하고, 몬테카를로의 P99는 난수 방식에 따라 ±3% 안팎으로 달라지니 범위로 본다.
절감액은 정의에 따라 6.7천 달러에서 3만 달러까지 달라진다 — 여기서는 시연 2의 카드 정의를 쓴다:
  외상 거래 바이어(신용장 · 선수금 제외)의 Σ elc × (현행 한도 − 제안 한도), S3는 S0의 2.5배(PD 배수)
실행   uv run pytest labs/day4/tests/test_stress_expected.py -q
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "workbench" / "day4" / "outputs"
NO_LIMIT = {"LC_SIGHT", "LC_USANCE", "TT_ADV"}


@pytest.fixture(scope="module")
def res(request) -> pd.DataFrame:
    opt = request.config.getoption("--stress")
    path = (Path(opt) if Path(opt).is_absolute() else ROOT / opt) if opt else OUT / "stress_results.csv"
    if not path.exists():
        pytest.fail(f"결과 파일이 없다 — 먼저 시뮬레이터를 돌린다: uv run python labs/day4/stress_mc.py  (찾은 곳: {path})")
    return pd.read_csv(path, encoding="utf-8-sig")


def test_formula_expected_loss_per_scenario(res):
    el = res.groupby("scenario_id")["el_formula_usd"].first()
    want = {"S0": 43_366, "S1": 45_866, "S2": 49_618, "S3": 62_121, "S4": 107_691}
    got = {k: round(float(el[k])) for k in want if k in el.index}
    assert got == want, f"공식 기대손실 {got} (기대 {want})"


def test_s3_p99_is_in_the_expected_band(res):
    s3 = res[(res["scenario_id"] == "S3") & (res["n_sims"] >= 10_000)].set_index("rho")["mc_p99_usd"]
    assert 150_000 <= float(s3[0.0]) <= 172_000, f"S3 ρ 0의 P99 {s3[0.0]:,.0f} (기대 약 16만 — 15만~17.2만 안)"
    assert float(s3[0.2]) >= 1.15 * float(s3[0.0]), f"ρ 0.2의 P99 {s3[0.2]:,.0f}가 ρ 0의 {s3[0.0]:,.0f}보다 15% 이상 크지 않다"


def test_savings_from_the_proposed_limits():
    path = OUT / "limits_proposed.xlsx"
    if not path.exists():
        pytest.skip("한도안(limits_proposed.xlsx)이 없어 건너뜀 — 실습 A ②를 먼저")
    lim = pd.read_excel(path, sheet_name="limits")
    buyers = pd.read_csv(ROOT / "data" / "checkpoints" / "d4_start_scored.csv", encoding="utf-8-sig")
    credit = set(buyers.loc[~buyers["payment_method"].isin(NO_LIMIT), "buyer_id"])
    use = lim[lim["buyer_id"].isin(credit)]
    saving_s0 = float((use["elc"] * (use["current_limit"] - use["L"])).sum())
    assert saving_s0 == pytest.approx(6_722, abs=2), f"S0 절감액 {saving_s0:,.0f} (기대 6,722)"
    assert saving_s0 * 2.5 == pytest.approx(16_805, abs=5), f"S3 절감액 {saving_s0 * 2.5:,.0f} (기대 16,805)"
