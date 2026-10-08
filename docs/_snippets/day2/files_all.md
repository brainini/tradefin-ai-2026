<!-- 자동 생성: tools/sync_site_assets.py — 직접 고치지 말고 스크립트를 다시 돌리세요 -->

| 파일 | 무엇인가 | 쓰는 곳 | 크기 | 받기 |
|---|---|---|---|---|
| **`day2_files.zip`**<br>**한 번에 받기** | 지금까지 공개된 아래 파일을 `D2` 폴더 하나로 묶은 압축 파일 | 전체 | 18 KB | [:material-folder-download: **받기**](../downloads/day2/day2_files.zip){ download="day2_files.zip" } |
| `d2_start.xlsx`<br>2일차 시작 파일 | 가상 바이어 150곳의 기준일(2026-08-31) 표 — 일부러 지저분하다. 실습 A는 시트 buyers만 쓴다. 나머지 시트: buyer_features_raw · fx_at_ref(기준일 환율) · invoices_raw(더 하기) · dictionary(열 설명) · dirty_list · map_ccy · map_country | 실습 A · 실습 B 필수 | – | 공개 예정<br>10/15(목) 08:30 |
| `fx_krw_daily.csv`<br>원화 환율(일별) | 일별 원화 환율(미국 연준 H.10 · FRED). 환율 30일 변화와 as-of 환산을 직접 확인할 때 쓴다(엔화는 100엔 단위 → ÷100) | 실습 A 참고 | 29 KB | [:material-download: 받기](../downloads/day2/fx_krw_daily.csv){ download="fx_krw_daily.csv" } |
| `rules_template.md`<br>정제 규칙 양식 | 정제규칙.md 틀 — 칸마다 '규칙 / 왜' 두 줄 + 9 변경 기록. 내 저장소의 workbench/day2/rules/정제규칙.md와 같다. 채팅 경로에서 메모장에 붙여 쓴다 | 실습 A 참고 | 1 KB | [:material-download: 받기](../downloads/day2/rules_template.md){ download="rules_template.md" } |
| `d2_news.csv`<br>바이어 뉴스 | 바이어별 짧은 뉴스(합성 300건, 한국어 · 영어 · 기타). 실습 B에서 앞 100행을 0–10 점수로 바꾼다 | 실습 B 필수 | – | 공개 예정<br>10/15(목) 08:30 |
| `news_warmup_10.txt`<br>워밍업 뉴스 10건 | 채팅 경로에서 50행을 붙이기 전에 형식을 시험하는 10건(한국어 4 · 영어 6, 점수 없음) | 실습 B 선택 | – | 공개 예정<br>10/15(목) 08:30 |
| `d2_news_answer.csv`<br>뉴스 정답 20건(골든셋) | 실습 B 4단계에서 AI 점수를 재는 기준 점수(MAE · ±2 이내 비율 · 라벨 일치율). 정한 시각에 공개한다 | 실습 B 필수 | – | 공개 예정<br>10/15(목) 15:35 |
| `byod_anonymize_template.xlsx`<br>BYOD 익명화 템플릿 | 자사 엑셀을 쓰기 전 점검표(규칙 7 + 마지막 확인 4) · 가상 예시 변환 수식. 원본은 내 PC에서만, 익명화본도 저장소에는 올리지 않는다(AI에는 익명화본만 · 학습 설정 끔) — 다 했으면 | 실습 A 선택 | 13 KB | [:material-download: 받기](../downloads/day2/byod_anonymize_template.xlsx){ download="byod_anonymize_template.xlsx" } |
| `day2_slides.pdf`<br>강의 슬라이드(PDF) | 그날 강의 슬라이드의 수강생판 — 발표자 노트 제외, 외부 기관 화면 캡처는 자리 표시(강의장에서만 보여 준다). 당일 18:00 공개 | 실습 A · 실습 B 참고 | – | 공개 예정<br>10/15(목) 18:00 |

!!! note "공개 전 파일"
    '공개 예정'으로 표시된 파일은 적힌 시각에 이 표에 링크가 생깁니다. 시각이 지났는데도 링크가 없으면 화면을 새로 고치고, 그래도 없으면 강사에게 알려 주세요.
