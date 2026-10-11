"""조기경보 엔진(scripts/ews.py)의 속성 테스트 — 데이터가 바뀌어도 항상 맞아야 하는 성질만 검사한다(4일차 15:00 공개).

    uv run pytest labs/day4/tests/test_ews_props.py -q
    uv run pytest labs/day4/tests/test_ews_props.py --rules workbench/day4/rules/alert_rules.yml     # 내 규칙을 더한 판으로

- 경계값: dpd 30은 선적 보류에 들고 29는 들지 않는다 / 통지 기한까지 10일은 임박, 0일도 임박, -1일은 경과
- 면제: 신용장(LC_*)은 선적 보류에서 빠진다 / 보험에 안 든 건은 통지 규칙에서 빠진다
- 멱등: 같은 기준일로 다시 돌리면 결과 파일 3종이 글자까지 같고, 중복 키(기준일 + 규칙 + 인보이스)가 없다
- 일관: 단계 건수는 다시 센 값과 같다 / 선적 보류 바이어 = D+30 바이어 + 신용사건 바이어
- 권고: 문장은 모두 '권고(사람 승인 전)' 또는 '요청' — 이미 했다고 말하지 않는다
- 기대값: 과정 원장(기준일 2026-09-30)으로 돌리면 D+30 21건 233,455달러 · 선적 보류 19곳 · 통지 임박 9건 · 경과 14건 · 연체 확률 높음 18곳

엔진이 지켜야 할 모양(이 테스트가 읽는 것)
  호출   main(["--asof", "2026-09-30", "--rules", 규칙.yml, "--data", 데이터 폴더, "--out", 결과 폴더]) → 0 을 돌려준다
  입력   데이터 폴더의 d4_open_inv.csv · d4_start_scored.csv(workbench/day4/data/ 의 작업 사본)
  결과   alerts.csv(열: rule_id · tier · buyer_id · invoice_id · dpd · amount_usd · action · stage · asof — 같은 기준일 줄은 새 결과로 바꾸고 다른 기준일 줄은 쌓는다)
         alert_summary.json(stages.{단계}.count · amount_usd · tiers.{등급}.alerts · rules.{규칙}.alerts · ship_hold.count · buyers · reasons ·
                            notice.soon_invoices · overdue_invoices · pd_watch_buyers)
         alert_digest.md(문장은 '권고(사람 승인 전)') · run_log.jsonl(실행마다 한 줄)
"""
from __future__ import annotations

import csv
import importlib.util
import json
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[3]
WORK_DATA = ROOT / "workbench/day4/data"
ASOF = "2026-09-30"

INV_COLS = ["invoice_id", "buyer_id", "country_code", "payment_method", "currency", "ksure_insured", "ship_date", "due_date",
            "amount_ccy", "amount_usd", "paid", "insurance_type", "terms_change_date", "bank_change_request"]
# 바이어 표는 진짜 d4_start_scored.csv 와 같은 35개 열을 갖춘다 — 내가 규칙에 쓴 열(예: current_limit_usd · open_ar_usd)이 있어도 같은 테스트가 돈다
BUYER_COLS = ["buyer_id", "ref_date", "pd_30d", "pred_late", "threshold_used", "grade", "grade_rule", "rank_pct", "grade_quantile",
              "top_feature_1", "top_contrib_1", "top_feature_2", "top_contrib_2", "top_feature_3", "top_contrib_3", "top_reasons_ko",
              "model_version", "buyer_name", "country_code", "currency", "payment_method", "terms_days", "ksure_insured", "ksure_limit_usd",
              "monthly_sales_usd", "open_ar_usd", "overdue_amount_usd", "current_limit_usd", "oecd_crc", "pd_annual_assumed", "lgd_assumed",
              "coverage_ratio", "strategic_flag", "bankruptcy_flag", "buyer_type"]


def pick(option: str | None, default: Path) -> Path:
    if not option:
        return default
    p = Path(option)
    return p if p.is_absolute() else ROOT / p


@pytest.fixture(scope="module")
def ews(request):
    path = pick(request.config.getoption("--engine"), ROOT / "scripts/ews.py")
    if not path.exists():
        pytest.fail(f"엔진 파일이 없다 — 먼저 scripts/ews.py 를 만든다 (찾은 곳: {path})")
    spec = importlib.util.spec_from_file_location("ews_under_test", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert hasattr(module, "main"), "엔진에 main(argv) 함수가 있어야 한다(이 파일 첫머리의 '엔진이 지켜야 할 모양')"
    return module


@pytest.fixture(scope="module")
def rules(request) -> Path:
    path = pick(request.config.getoption("--rules"), ROOT / "labs/day4/alert_rules.yml")
    assert path.exists(), f"규칙 파일이 없다: {path}"
    return path


def due_for(dpd: int) -> str:
    return (pd.Timestamp(ASOF) - pd.Timedelta(days=dpd)).strftime("%Y-%m-%d")


def invoice(n: int, buyer: str = "B001", dpd: int = 0, method: str = "OA", insured: str = "N", usd: float = 1000.0, **kw) -> dict:
    row = dict(invoice_id=f"INV-T-{n:04d}", buyer_id=buyer, country_code="USA", payment_method=method, currency="USD",
               ksure_insured=insured, ship_date="2026-06-01", due_date=due_for(dpd), amount_ccy=usd, amount_usd=usd, paid="N",
               insurance_type="개별" if insured == "Y" else "", terms_change_date="", bank_change_request="N")
    row.update(kw)
    return row


def buyer(b: str = "B001", pd30: float = 0.01, bankrupt: int = 0, method: str = "OA", insured: str = "N", **kw) -> dict:
    row = dict(buyer_id=b, ref_date=ASOF, pd_30d=pd30, pred_late=int(pd30 >= 0.1698), threshold_used=0.1698, grade="S",
               grade_rule="t/4·t/2·t", rank_pct=0.5, grade_quantile="S", top_feature_1="x", top_contrib_1=0.0, top_feature_2="x",
               top_contrib_2=0.0, top_feature_3="x", top_contrib_3=0.0, top_reasons_ko="", model_version="test", buyer_name="Test Co.",
               country_code="USA", currency="USD", payment_method=method, terms_days=60, ksure_insured=insured, ksure_limit_usd=0,
               monthly_sales_usd=10000.0, open_ar_usd=0.0, overdue_amount_usd=0.0, current_limit_usd=100000, oecd_crc="",
               pd_annual_assumed=0.005, lgd_assumed=0.6, coverage_ratio=0.0, strategic_flag=0, bankruptcy_flag=bankrupt, buyer_type="PRIVATE")
    row.update(kw)
    return row


def write_csv(path: Path, rows: list[dict], cols: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


@pytest.fixture
def run(ews, rules, tmp_path):
    """작은 가짜 원장으로 엔진을 돌려 요약(dict)을 돌려주는 함수. 결과 파일은 tmp_path/out/ 에 남는다."""
    def _run(invoices: list[dict], buyers: list[dict], asof: str = ASOF, out: str = "out") -> dict:
        data = tmp_path / "data"
        data.mkdir(exist_ok=True)
        write_csv(data / "d4_open_inv.csv", invoices, INV_COLS)
        write_csv(data / "d4_start_scored.csv", buyers, BUYER_COLS)
        assert ews.main(["--asof", asof, "--rules", str(rules), "--data", str(data), "--out", str(tmp_path / out)]) == 0
        return json.loads((tmp_path / out / "alert_summary.json").read_text(encoding="utf-8"))
    return _run


def alerts_of(tmp: Path, out: str = "out") -> pd.DataFrame:
    return pd.read_csv(tmp / out / "alerts.csv", encoding="utf-8-sig", keep_default_na=False, dtype=str)


def invoices_hit(df: pd.DataFrame, rule: str) -> set[str]:
    return set(df[df["rule_id"] == rule]["invoice_id"])


# ------------------------------------------------------------------ 경계값 · 면제
def test_d30_boundary_is_inclusive(run, tmp_path):
    run([invoice(1, dpd=29), invoice(2, dpd=30), invoice(3, dpd=31)], [buyer()])
    assert invoices_hit(alerts_of(tmp_path), "R-D30-HOLD") == {"INV-T-0002", "INV-T-0003"}  # '>=' 그대로: 30 포함, 29 제외


def test_letters_of_credit_are_exempt_from_hold(run, tmp_path):
    inv = [invoice(1, dpd=40, method="LC_SIGHT"), invoice(2, dpd=40, method="LC_USANCE"), invoice(3, dpd=40, method="DA")]
    run(inv, [buyer(method="DA")])
    assert invoices_hit(alerts_of(tmp_path), "R-D30-HOLD") == {"INV-T-0003"}


@pytest.mark.parametrize("dpd,left,expected", [(20, 10, "SOON"), (19, 11, None), (31, 0, "SOON"), (32, -1, "OVERDUE"), (33, -2, "OVERDUE")])
def test_notice_window_edges(run, tmp_path, dpd, left, expected):
    """통지 기한 = 결제기일 + 1개월. 기한까지 0~10일은 '임박', 지났으면 '경과'. 보험에 든 건만."""
    run([invoice(1, dpd=dpd, insured="Y"), invoice(2, dpd=dpd, insured="N")], [buyer()])
    got = alerts_of(tmp_path)
    soon, over = invoices_hit(got, "R-KSURE-NOTICE-SOON"), invoices_hit(got, "R-KSURE-NOTICE-OVERDUE")
    assert soon == ({"INV-T-0001"} if expected == "SOON" else set())
    assert over == ({"INV-T-0001"} if expected == "OVERDUE" else set())


def test_not_yet_due_never_triggers_notice(run, tmp_path):
    run([invoice(1, dpd=0, insured="Y"), invoice(2, dpd=-5, insured="Y")], [buyer()])
    got = alerts_of(tmp_path)
    assert not invoices_hit(got, "R-KSURE-NOTICE-SOON") and not invoices_hit(got, "R-KSURE-NOTICE-OVERDUE")


def test_paid_invoices_are_ignored(run, tmp_path):
    run([invoice(1, dpd=60, paid="Y"), invoice(2, dpd=60)], [buyer()])
    assert invoices_hit(alerts_of(tmp_path), "R-D30-HOLD") == {"INV-T-0002"}


def test_credit_event_buyer_without_open_invoice_is_still_listed(run):
    s = run([invoice(1, buyer="B001", dpd=-10)], [buyer("B001"), buyer("B002", bankrupt=1)])
    assert s["ship_hold"]["buyers"] == ["B002"] and s["ship_hold"]["reasons"]["B002"] == ["R-CREDIT-EVENT"]


def test_pd_watch_uses_the_threshold_with_greater_or_equal(run, tmp_path):
    s = run([invoice(1)], [buyer("B001", pd30=0.1698), buyer("B002", pd30=0.1697)])
    got = alerts_of(tmp_path)
    assert set(got[got["rule_id"] == "R-PD-WATCH"]["buyer_id"]) == {"B001"} and s["pd_watch_buyers"] == 1


# ------------------------------------------------------------------ 멱등
def test_same_asof_twice_gives_identical_files(run, tmp_path):
    inv = [invoice(1, dpd=45, insured="Y"), invoice(2, dpd=8), invoice(3, dpd=-2)]
    run(inv, [buyer(bankrupt=1)])
    first = {n: (tmp_path / "out" / n).read_bytes() for n in ("alerts.csv", "alert_summary.json", "alert_digest.md")}
    run(inv, [buyer(bankrupt=1)])
    second = {n: (tmp_path / "out" / n).read_bytes() for n in first}
    assert first == second
    assert len((tmp_path / "out" / "run_log.jsonl").read_text(encoding="utf-8").strip().splitlines()) == 2  # 기록만 한 줄 늘어난다


def test_other_asof_rows_accumulate_without_duplicates(run, tmp_path):
    inv = [invoice(1, dpd=45)]
    run(inv, [buyer()], asof="2026-09-30")
    run(inv, [buyer()], asof="2026-10-01")
    run(inv, [buyer()], asof="2026-09-30")
    got = alerts_of(tmp_path)
    assert sorted(got["asof"].unique()) == ["2026-09-30", "2026-10-01"]
    assert not got.duplicated(["asof", "rule_id", "buyer_id", "invoice_id"]).any()


# ------------------------------------------------------------------ 작업 사본 데이터(과정 원장)로
@pytest.fixture(scope="module")
def working_copy(ews, rules, tmp_path_factory):
    if not (WORK_DATA / "d4_open_inv.csv").exists():
        pytest.skip("workbench/day4/data/ 에 d4_open_inv.csv 가 없습니다 — uv run python tools/get_day_files.py 4")
    tmp = tmp_path_factory.mktemp("work")
    assert ews.main(["--asof", ASOF, "--rules", str(rules), "--data", str(WORK_DATA), "--out", str(tmp)]) == 0
    return dict(alerts=pd.read_csv(tmp / "alerts.csv", encoding="utf-8-sig", keep_default_na=False, dtype=str),
                summary=json.loads((tmp / "alert_summary.json").read_text(encoding="utf-8")),
                digest=(tmp / "alert_digest.md").read_text(encoding="utf-8"))


def test_no_duplicate_keys_in_working_copy(working_copy):
    assert not working_copy["alerts"].duplicated(["asof", "rule_id", "buyer_id", "invoice_id"]).any()


def test_stage_counts_match_an_independent_count(working_copy):
    inv = pd.read_csv(WORK_DATA / "d4_open_inv.csv", encoding="utf-8-sig", keep_default_na=False)
    inv = inv[inv["paid"] == "N"]
    dpd = (pd.Timestamp(ASOF) - pd.to_datetime(inv["due_date"])).dt.days
    ranges = {"D-3": (-3, -1), "D+7": (7, 14), "D+15": (15, 29), "D+30": (30, 10**6)}
    for name, (lo, hi) in ranges.items():
        sel = (dpd >= lo) & (dpd <= hi)
        got = working_copy["summary"]["stages"][name]
        assert got["count"] == int(sel.sum())
        assert got["amount_usd"] == pytest.approx(float(inv.loc[sel, "amount_usd"].sum()), abs=0.01)


def test_ship_hold_is_d30_buyers_plus_credit_event_buyers(working_copy):
    a = working_copy["alerts"]
    expect = set(a[a["rule_id"] == "R-D30-HOLD"]["buyer_id"]) | set(a[a["rule_id"] == "R-CREDIT-EVENT"]["buyer_id"])
    assert set(working_copy["summary"]["ship_hold"]["buyers"]) == expect
    assert working_copy["summary"]["ship_hold"]["count"] == len(expect)


def test_hold_never_includes_letters_of_credit(working_copy):
    a = working_copy["alerts"]
    inv = pd.read_csv(WORK_DATA / "d4_open_inv.csv", encoding="utf-8-sig", keep_default_na=False)
    lc = set(inv[inv["payment_method"].isin(["LC_SIGHT", "LC_USANCE"])]["invoice_id"])
    assert not (set(a[a["rule_id"] == "R-D30-HOLD"]["invoice_id"]) & lc)


def test_every_sentence_is_a_recommendation(working_copy):
    digest, a = working_copy["digest"], working_copy["alerts"]
    assert "권고(사람 승인 전)" in digest
    for done in ("발송했", "차단했", "송금했", "중단했", "보류했"):  # 이미 했다는 말은 없다
        assert done not in digest
    hold_actions = set(a[a["rule_id"].isin(["R-D30-HOLD", "R-CREDIT-EVENT", "R-FRAUD-ACCOUNT"])]["action"])
    assert hold_actions and all("권고" in x for x in hold_actions)


def test_summary_counts_add_up(working_copy):
    s = working_copy["summary"]
    assert sum(v["alerts"] for v in s["rules"].values()) == len(working_copy["alerts"])
    assert sum(v["alerts"] for v in s["tiers"].values()) == len(working_copy["alerts"])


def test_expected_counts_on_the_course_ledger(working_copy):
    """과정 원장(기준일 2026-09-30, 미결 300건)의 기대값 — 규칙 파일에 내 규칙을 더해도 이 숫자는 그대로다."""
    s = working_copy["summary"]
    if s["open_invoices"] != 300:
        pytest.skip(f"과정 원장(미결 300건)이 아니라 건너뜀(지금 {s['open_invoices']}건)")
    d30 = s["stages"]["D+30"]
    assert (d30["count"], round(d30["amount_usd"])) == (21, 233_455), f"D+30 {d30['count']}건 {d30['amount_usd']:,.0f}달러 (기대 21건 233,455달러)"
    assert s["ship_hold"]["count"] == 19, f"선적 보류 {s['ship_hold']['count']}곳 (기대 19곳)"
    assert (s["notice"]["soon_invoices"], s["notice"]["overdue_invoices"]) == (9, 14), (
        f"통지 임박 {s['notice']['soon_invoices']}건 · 경과 {s['notice']['overdue_invoices']}건 (기대 9 · 14)")
    assert s["pd_watch_buyers"] == 18, f"연체 확률 높음 {s['pd_watch_buyers']}곳 (기대 18곳)"
