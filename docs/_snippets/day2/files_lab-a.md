<!-- 자동 생성: tools/sync_site_assets.py — 직접 고치지 말고 스크립트를 다시 돌리세요 -->

| 파일 | 무엇인가 | 트랙 | 받기 |
|---|---|---|---|
| `d2_start.xlsx` | 가상 바이어 150곳의 기준일(2026-08-31) 표 — 일부러 지저분하다. 실습 A는 시트 buyers만 쓴다. 나머지 시트: buyer_features_raw · fx_at_ref(기준일 환율) · invoices_raw(더 하기) · dictionary(열 설명) · dirty_list · map_ccy · map_country | 필수 | 공개 예정<br>10/15(목) 08:30 |
| `fx_krw_daily.csv` | 일별 원화 환율(미국 연준 H.10 · FRED). 환율 30일 변화와 as-of 환산을 직접 확인할 때 쓴다(엔화는 100엔 단위 → ÷100) | 참고 | [:material-download: 받기](../downloads/day2/fx_krw_daily.csv){ download="fx_krw_daily.csv" } |
| `rules_template.md` | 정제규칙.md 틀 — 칸마다 '규칙 / 왜' 두 줄 + 9 변경 기록. 내 저장소의 workbench/day2/rules/정제규칙.md와 같다. 채팅 경로에서 메모장에 붙여 쓴다 | 참고 | [:material-download: 받기](../downloads/day2/rules_template.md){ download="rules_template.md" } |
| `byod_anonymize_template.xlsx` | 자사 엑셀을 쓰기 전 점검표(규칙 7 + 마지막 확인 4) · 가상 예시 변환 수식. 원본은 내 PC에서만, 익명화본도 저장소에는 올리지 않는다(AI에는 익명화본만 · 학습 설정 끔) — 다 했으면 | 선택 | [:material-download: 받기](../downloads/day2/byod_anonymize_template.xlsx){ download="byod_anonymize_template.xlsx" } |
| `day2_slides.pdf` | 그날 강의 슬라이드의 수강생판 — 발표자 노트 제외, 외부 기관 화면 캡처는 자리 표시(강의장에서만 보여 준다). 당일 18:00 공개 | 참고 | 공개 예정<br>10/15(목) 18:00 |
