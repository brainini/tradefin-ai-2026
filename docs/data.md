# 데이터

## 시나리오 — (가상) 한빛정밀(주) {#scenario}

6일 동안 같은 가상 회사의 데이터로 실습합니다. 회사 이름도 숫자도 과정을 위해 만든 **합성 데이터**이며 실존 기업과 무관합니다.

| 항목 | 내용 |
|---|---|
| 회사 | 대전 소재 정밀부품·산업용 센서 수출 중소기업(가상) |
| 규모 | 바이어 **150**곳 · **20**개국 · **36**개월 · 인보이스 약 **5,000**건 |
| 결제조건 | 송금(선수금·사후송금) 약 70%, 신용장 6~8%, 나머지 D/A·D/P |
| 고민 | 미수금이 늘고, 연체를 늦게 안다 |
| 기준일 | Day1 바이어 스냅샷 **2026-09-30** |

결제조건 비중은 실제 한국 수출과 닮게 만들었습니다 — 한국 수출 결제는 송금 70.7%, 신용장 약 6%입니다(2024, 업계 집계 · 원통계 미표기 — [레퍼런스](references.md#d1-32)).
무역금융 판단은 여러분이 전문가입니다. 이 시나리오는 방법을 연습하는 무대입니다.

## Day1 파일 {#files}

--8<-- "docs/_snippets/day1/files_all_root.md"

- 매일 아침 09:00에 전날 실습의 **강사 정답 파일(체크포인트)**이 올라옵니다. 어제를 놓쳐도 그 파일로 오늘 합류합니다.
- 모든 컬럼의 뜻·단위는 **데이터 사전**(`data_dictionary.xlsx`)의 `columns` 시트에 있습니다.

## 바이어 스냅샷 `d1_buyers_raw` 핵심 컬럼 {#buyers}

153행 · 23열 · 시트 `buyers`(안내는 `readme` 시트). ★는 Lab2에서 직접 쓰는 컬럼입니다.

!!! warning "원천 입력 오류가 섞여 있습니다"
    실무 대장처럼 담당자가 입력한 그대로의 데이터입니다. **무엇이 이상한지는 Lab2에서 직접 찾습니다** — 오늘은 진단만, 정제는 Day2입니다.

| 컬럼 | 한글명 | 뜻 | 단위 |
|---|---|---|---|
| `buyer_id` ★ | 바이어 ID | B001~B150 형식의 가명 식별자 | – |
| `buyer_name` | 바이어명(가상) | 가상 상호(실존 기업과 무관) | – |
| `country` | 국가명(원천 표기) | 담당자가 입력한 국가명 그대로 | – |
| `country_code` ★ | 국가코드 | ISO 3166-1 alpha-3 세 글자 코드(예: USA, DEU) | – |
| `region` ★ | 권역 | 북미·중남미 / 서유럽 / 중동부유럽 / 동아시아 / 동남아·남아 / 중동·아프리카 | – |
| `industry` | 업종 | `oem_manufacturer`(완제품 제조사) · `distributor`(유통·대리점) · `retail`(소매) · `epc_contractor`(EPC·설치 시공) · `utility`(유틸리티) · `public_agency`(공공기관) | – |
| `segment` | 고객 구분 | private(민간) / public(공공) | – |
| `buyer_type` | 공공 유형 | PRIVATE / UN(UN 계열 기구) / MDB(다자개발은행 재원 사업) / EM_GOV(신흥국 정부) / DM_GOV(선진국 정부) | – |
| `payment_terms_raw` ★ | 결제조건(원천 표기) | 담당자가 입력한 결제조건 그대로. Lab2에서 [코드 7종](#codes)으로 바꾼다 | – |
| `ar_balance` | 매출채권 잔액 | 기준일 미결제 잔액(청구 통화 기준) | 통화 |
| `ar_currency` | 잔액 통화(원천 표기) | 청구 통화 | – |
| `max_dpd_days` ★ | 연체일수(최악) | 기준일에 남은 미결 인보이스 중 결제기일을 가장 오래 넘긴 날수(0 = 연체 없음) | 일 |
| `overdue_amount` | 미납 결제 금액 | 결제기일이 지난 미결 잔액(청구 통화 기준) | 통화 |
| `pay_score` | 바이어 신용도 점수 | 결제 이력으로 만든 1~100점(PAYDEX형) | 점 |
| `oecd_crc` | 국가위험등급 | OECD 국가위험분류 0~7(높을수록 위험), "-" = 분류 대상 아님(고소득 OECD국) | 등급 |
| `ksure_insured` ★ | K-SURE 부보 여부 | 바이어 단위 단기수출보험 가입 여부 | Y/N |
| `since_date` | 거래 시작일 | 첫 거래일 | 날짜 |
| `fin_summary_text` | 재무 요약문 | 재무 상태를 요약한 영문 1~2문장 | – |
| `revenue_usd_fy2025` | 매출액 | 바이어의 FY2025 매출 | USD |
| `current_ratio_fy2025` | 유동비율 | 유동자산 ÷ 유동부채 | 배 |
| `debt_to_equity_fy2025` | 부채비율 | 총부채 ÷ 자기자본 | 배 |
| `dso_fy2025` | 매출채권회전일(DSO) | 매출채권 ÷ 매출 × 365 | 일 |
| `op_margin_fy2025` | 영업이익률 | 영업이익 ÷ 매출(소수: 0.08 = 8%) | 비율 |

Lab2에서 새로 만드는 열 4개: `payment_method`(코드 7종) · `dpd_num`(숫자로 바꾼 연체일) · `aging_bucket`(연체 구간) · `is_overdue`(연체 1 / 아님 0) — [Lab2 새 열 만들기](day1/lab2.md#new-columns).

## 결제방식 코드 7종 {#codes}

| 코드 | 뜻 | 대금 받는 시점 | 위험을 지는 쪽 |
|---|---|---|---|
| `TT_ADV` | 선수금 송금(T/T in advance, cash in advance) | 선적 전 | 수출자 위험은 거의 없음 |
| `TT_SPLIT_30_70` | 분할 송금 — 30% 선수금 + 70% 선적 후 송금 | 30% 선적 전 · 70% 선적 후 | 잔금 70%는 수출자 |
| `OA` | 사후송금(Open Account, T/T after shipment) | 선적 후 30·60·90일 | 수출자 전부 |
| `DA` | 인수인도조건 추심(Documents against Acceptance) | 수입자가 어음을 인수한 뒤 만기 | 수출자(추심은행은 지급을 보증하지 않음) |
| `DP` | 지급인도조건 추심(Documents against Payment) | 대금을 내야 서류를 내줌 | 수출자(안 내면 물품 반송·재판매) |
| `LC_SIGHT` | 일람불 신용장(Sight L/C) | 서류 제시·심사 후 | 개설은행·국가(서류 하자는 수출자) |
| `LC_USANCE` | 기한부 신용장(Usance L/C) | 만기 | 개설은행·국가 |

## 연체 구간(에이징) {#aging}

| 구간 | 뜻 |
|---|---|
| Current | 연체 없음(결제기일 전·당일, 연체일 ≤ 0) |
| 1-30 | 1~30일 연체 |
| 31-60 | 31~60일 연체 |
| 61-90 | 61~90일 연체 |
| 91+ | 91일 이상 연체 |
| 확인필요 | 연체일이 숫자가 아니라 구간을 정할 수 없음 |

구간은 바이어마다 **가장 오래 연체된 인보이스(최악 연체일)** 기준입니다.

## 인보이스 원장 `d1_invoices` (🟣 Challenge) {#invoices}

5,033행(36개월) · 시트 `invoices`. 바이어 한 줄 요약이 아니라 인보이스 하나하나가 들어 있습니다.

| 컬럼 | 뜻 |
|---|---|
| `invoice_id` · `buyer_id` · `country_code` | 인보이스 번호 · 바이어 ID · 국가코드 |
| `invoice_date` · `due_date` · `settled_date` | 발행일(= 선적일로 가정) · 결제기일 · 완납일(2026-09-30까지 다 받지 못했으면 빈칸) |
| `payment_method` · `terms_days` | 결제방식 코드 7종 · 선적 후 결제기일까지 날수 |
| `currency` · `amount_ccy` · `amount_usd` | 청구 통화 · 원통화 금액 · 달러 환산 금액 |
| `status` | 2026-09-30 기준 상태: paid(완납) / open(미결) / default(부도 바이어 미회수) / written_off(대손 처리). 데이터 사전의 returned(D/P 서류 반송)는 Day1 원장에 없습니다 |
| `ksure_insured` · `dispute_flag` · `dispute_type` | 보험 가입 여부 · 분쟁 여부 · 분쟁 유형(QUALITY 품질 · QUANTITY 수량 · DOCS 서류 · PRICE 가격, 분쟁이 없으면 빈칸) |

나머지 컬럼(환율·원화 금액·환차손익 등)은 데이터 사전 `columns` 시트를 보세요.

## SEC 추출 비율표 `real_buyers_ratios` {#ratios}

Lab1 보고서 발췌 4개사의 재무 원값과 4대 비율을 미국 SEC의 XBRL 공시 데이터(companyfacts API)에서 뽑은 표입니다(9행: 발췌와 같은 기간 + 비교 기간).

| 컬럼 | 뜻 |
|---|---|
| `company` · `form` · `fiscal_period_end` · `row_role` | 회사 · 공시 종류 · 기준일 · 그 행의 용도(발췌와 같은 기간인지 등) |
| `current_assets` … `operating_income` | 유동자산·유동부채·총부채·자기자본·매출채권·매출·영업이익 — 모두 **달러 원 단위**(발췌 재무표는 천 달러) |
| `current_ratio` · `debt_to_equity` · `dso_days` · `op_margin_pct` | 유동비율 · 부채비율(자본잠식이면 빈칸, `negative_equity_flag` = 1) · DSO(일) · 영업이익률(%) |
| `xbrl_tags_used` · `data_note` · `filing_url` | 어떤 계정 태그에서 뽑았나 · 주의 사항 · 원문 공시 주소 |
| `going_concern_flag` · `later_event` … | 이후 경과 — **실습이 끝난 뒤** 봅니다 |

## 보고서 발췌 {#reports}

| 파일 | 원문 | 단위 |
|---|---|---|
| `halden_fictional_annual_report.md` | **가상** 연차보고서(강사 창작, FY2026) — SEC 공시 아님 | 천 파운드 |
| `irobot.md` | [iRobot Form 10-K FY2024](https://www.sec.gov/Archives/edgar/data/1159167/000115916725000011/irbt-20241228.htm) (2025-03-12 접수) | 천 달러 |
| `plug_power.md` | [PART A 10-Q 2023년 3분기](https://www.sec.gov/Archives/edgar/data/1093691/000155837023018601/plug-20230930x10q.htm) · [PART B 10-K FY2023](https://www.sec.gov/Archives/edgar/data/1093691/000155837024002178/plug-20231231x10k.htm) · [PART C 10-K FY2024](https://www.sec.gov/Archives/edgar/data/1093691/000155837025002049/plug-20241231x10k.htm) | 천 달러 |
| `wolfspeed.md` | [Wolfspeed Form 10-Q (2025-03-30 분기)](https://www.sec.gov/Archives/edgar/data/895419/000089541925000071/wolf-20250330.htm) | 백만 달러 |
| `big_lots.md` | [Big Lots Form 10-Q (2024-05-04 분기)](https://www.sec.gov/Archives/edgar/data/768835/000076883524000049/big-20240504.htm) | 천 달러 |
| `gorman_note.md` | D&B 샘플 보고서(가상 기업) **링크와 읽기 안내만** | 달러 |

SEC 발췌는 영어 원문을 고치지 않았고(둥근 따옴표만 곧은 따옴표로 바꿈), `[E1]` 같은 번호와 한국어 소제목은 편집자가 붙인 것입니다.

## 라이선스와 출처 {#license}

라이선스 전문은 과정 저장소 맨 위 폴더의 `LICENSE`(코드 · MIT) · `LICENSE-DATA.md`(데이터·문서 · CC BY 4.0과 제3자 자료의 이용 조건)에, 제3자 자료의 출처 표기는 `NOTICE.md`에 있습니다(© 2026 Taegu Han).

| 대상 | 조건 |
|---|---|
| (가상) 한빛정밀 합성 데이터 · Halden 가상 보고서 · 이 사이트의 글 | **CC BY 4.0** — 출처를 밝히면 자유롭게 쓸 수 있습니다 |
| 실습 코드(노트북·도구) | MIT |
| SEC 공시 발췌(iRobot · Plug Power · Wolfspeed · Big Lots) | 미국 SEC EDGAR에 제출된 **공개 공시를 교육 목적으로 일부 발췌**한 것입니다. 원문의 저작권과 책임은 각 회사에 있고, 원문 전체는 위 링크에서 봅니다 |
| SEC 비율표 | SEC XBRL companyfacts API(data.sec.gov)에서 2026-10-01에 추출·계산 |
| D&B Gorman 샘플 | **링크만** 제공합니다. PDF에 D&B 저작권 표시가 있으므로 저장소·공유 드라이브·단체방에 올리지 않고 각자 링크에서 받아 개인 실습에만 씁니다 |
| 환율(데이터 안의 원화 환산) | 미국 연준 FRED H.10 기준 교차환율 — 한국은행 매매기준율과 소폭(약 ±1%) 다를 수 있습니다 |
| 글꼴(차트·노트북의 한글) | NanumGothic — SIL Open Font License 1.1 |

이 사이트의 어떤 자료도 투자·여신 판단 자료가 아닙니다.

## 데이터 위생 {#hygiene}

오늘 데이터는 전부 가상이거나 공개 공시입니다. 회사 실데이터를 쓰려면 [데이터 위생 5원칙](setup.md#hygiene)과
[익명화 체크리스트](setup.md#byod)를 먼저 확인하세요. **AI 대화창은 외부 채널입니다.**
