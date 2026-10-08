<!-- 자동 생성: tools/sync_site_assets.py — 직접 고치지 말고 스크립트를 다시 돌리세요 -->

| 파일 | 무엇인가 | 쓰는 곳 | 크기 | 받기 |
|---|---|---|---|---|
| **`day1_files.zip`**<br>**한 번에 받기** | 아래 파일 전부를 `D1` 폴더 하나로 묶은 압축 파일. 보고서 발췌(.md)는 `D1/reports` 폴더 안에 있다 | 전체 | 10.1 MB | [:material-folder-download: **받기**](../downloads/day1/day1_files.zip){ download="day1_files.zip" } |
| `d1_encoding_test.csv`<br>깨진 CSV 연습 파일 | 한글 열 이름·바이어명이 든 8행 가상 표. UTF-8(BOM 없음)이라 엑셀에서 더블클릭하면 한글이 깨진다 → 실습 A-1 ①에서 UTF-8로 다시 연다 | 실습 A 필수 | 1 KB | [:material-download: 받기](../downloads/day1/d1_encoding_test.csv){ download="d1_encoding_test.csv" } |
| `d1_encoding_test_utf8bom.csv`<br>깨진 CSV 연습 파일(비교용) | 같은 내용을 UTF-8(BOM 포함)로 저장한 짝 파일. 더블클릭해도 바로 열린다 — 정상 화면과 비교할 때만 쓴다 | 실습 A 참고 | 1 KB | [:material-download: 받기](../downloads/day1/d1_encoding_test_utf8bom.csv){ download="d1_encoding_test_utf8bom.csv" } |
| `halden_fictional_annual_report.md`<br>Halden(가상) 연차보고서 발췌 | 가상 영국 유통 바이어의 연차보고서(FY2026). 실습 A-2에서 Claude Code로 읽고 ChatGPT 또는 Claude 웹으로 교차 확인한다 | 실습 A 필수 | 11 KB | [:material-download: 받기](../downloads/day1/reports/halden_fictional_annual_report.md){ download="halden_fictional_annual_report.md" } |
| `irobot.md`<br>iRobot 10-K FY2024 발췌 | 실제 SEC 공시 발췌(영어 원문 그대로). 다 했으면 같은 방식으로 한 번 더 하고 비율표와 대조한다 | 실습 A 선택 | 15 KB | [:material-download: 받기](../downloads/day1/reports/irobot.md){ download="irobot.md" } |
| `wolfspeed.md`<br>Wolfspeed 10-Q 발췌 | 2025-03-30 분기 보고서 발췌. 분기라 기간 일수(91일)에 주의 — 다 했으면 | 실습 A 선택 | 11 KB | [:material-download: 받기](../downloads/day1/reports/wolfspeed.md){ download="wolfspeed.md" } |
| `big_lots.md`<br>Big Lots 10-Q 발췌 | 2024-05-04 분기 보고서 발췌. 더 해 보고 싶을 때 | 실습 A 선택 | 12 KB | [:material-download: 받기](../downloads/day1/reports/big_lots.md){ download="big_lots.md" } |
| `plug_power.md`<br>Plug Power 공시 3건 발췌 | PART A 10-Q 2023년 3분기 · PART B 10-K FY2023 · PART C 10-K FY2024. 경고 문구가 부도로 이어지지 않은 오탐 반례 — 더 해 보고 싶을 때 | 실습 A 선택 | 17 KB | [:material-download: 받기](../downloads/day1/reports/plug_power.md){ download="plug_power.md" } |
| `gorman_note.md`<br>D&B 샘플(Gorman) 안내 | D&B 샘플 신용보고서 링크와 읽기 안내만 있다(PDF는 링크에서 직접 받는다). 더 해 보고 싶을 때 | 실습 A 선택 | 2 KB | [:material-download: 받기](../downloads/day1/reports/gorman_note.md){ download="gorman_note.md" } |
| `README.md`<br>보고서 폴더 안내 | 파일 목록 · 인용 찾는 요령 · 단위 주의 · 이용 조건 | 실습 A 참고 | 9 KB | [:material-download: 받기](../downloads/day1/reports/README.md){ download="README.md" } |
| `real_buyers_ratios.csv`<br>SEC 추출 비율표(CSV) | SEC companyfacts API에서 뽑은 4개사 원값과 4대 비율(9행). 다 했으면 iRobot 행으로 AI 숫자를 대조한다 | 실습 A 선택 | 10 KB | [:material-download: 받기](../downloads/day1/real_buyers_ratios.csv){ download="real_buyers_ratios.csv" } |
| `real_buyers_ratios.xlsx`<br>SEC 추출 비율표(엑셀) | 같은 내용 + 열 설명(dictionary)·원천(source) 시트 | 실습 A 선택 | 12 KB | [:material-download: 받기](../downloads/day1/real_buyers_ratios.xlsx){ download="real_buyers_ratios.xlsx" } |
| `d1_buyers_raw.xlsx`<br>바이어 스냅샷(엑셀) | (가상) 한빛정밀 해외 바이어 현황 153행 · 시트 buyers · 기준일 2026-09-30 · 원천 입력 오류 포함. 실습 B에서 진단 → 코드표 → 변수 정의서 → EDA 노트북 → 손 검산 | 실습 B 필수 | 28 KB | [:material-download: 받기](../downloads/day1/d1_buyers_raw.xlsx){ download="d1_buyers_raw.xlsx" } |
| `d1_buyers_raw.csv`<br>바이어 스냅샷(CSV) | 같은 내용 CSV(UTF-8 BOM). 엑셀 파일이 올라가지 않는 AI 도구에서 쓴다 | 실습 B 선택 | 36 KB | [:material-download: 받기](../downloads/day1/d1_buyers_raw.csv){ download="d1_buyers_raw.csv" } |
| `data_dictionary.xlsx`<br>데이터 사전 | 컬럼 뜻·단위(columns), 코드표(codes), 결제조건 표기 → 코드(payment_terms_map) | 실습 B 참고 | 29 KB | [:material-download: 받기](../downloads/day1/data_dictionary.xlsx){ download="data_dictionary.xlsx" } |
| `issue_definition_template.md`<br>현안 정의서 양식 | 실습 B-2 ⑥에서 프롬프트 B5가 읽는 양식 — 결제방식별 근거 숫자 표 · 내 업무라면(직접 쓰기) | 실습 B 필수 | 2 KB | [:material-download: 받기](../downloads/day1/issue_definition_template.md){ download="issue_definition_template.md" } |
| `d1_invoices.xlsx`<br>인보이스 원장(엑셀) | 인보이스 5,033건(36개월) · 시트 invoices. 오전 시연 3의 입력 — 실습 B 다 했으면 | 실습 B 선택 | 488 KB | [:material-download: 받기](../downloads/day1/d1_invoices.xlsx){ download="d1_invoices.xlsx" } |
| `d1_invoices.csv`<br>인보이스 원장(CSV) | 같은 내용 CSV(UTF-8 BOM). AI 채팅에 올릴 때 쓴다 | 실습 B 선택 | 678 KB | [:material-download: 받기](../downloads/day1/d1_invoices.csv){ download="d1_invoices.csv" } |
| `day1_slides.pdf`<br>강의 슬라이드(PDF) | 그날 강의 슬라이드의 수강생판 — 발표자 노트 제외, 외부 기관 화면 캡처는 자리 표시(강의장에서만 보여 준다). 당일 18:00 공개 | 실습 A · 실습 B 참고 | 9.9 MB | [:material-download: 받기](../downloads/day1/day1_slides.pdf){ download="day1_slides.pdf" } |
