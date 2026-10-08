<!-- 자동 생성: tools/sync_site_assets.py — 직접 고치지 말고 스크립트를 다시 돌리세요 -->

| 파일 | 무엇인가 | 쓰는 곳 | 크기 | 받기 |
|---|---|---|---|---|
| **`day3_files.zip`**<br>**한 번에 받기** | 지금까지 공개된 아래 파일을 `D3` 폴더 하나로 묶은 압축 파일 | 전체 | 61 KB | [:material-folder-download: **받기**](downloads/day3/day3_files.zip){ download="day3_files.zip" } |
| `d3_start_features.csv`<br>학습용 특성(300행) | 150개사 × 기준일 2개(2026-02-28 · 08-31)의 53열 표. 정답 late_30d(정상 0 / 연체 1, 연체 16건) · split_suggested(학습 212행 · 시험 88행) · sample_weight(정답으로 계산한 가중치 — 특성으로 쓰면 누수) | 실습 A 필수 | – | 공개 예정<br>10/16(금) 08:30 |
| `d3_start_scoring.csv`<br>예측 대상(150행) | 같은 특성, 기준일 2026-09-30, 정답(late_30d) 없음 — 실습 B에서 점수와 등급을 붙일 대상 | 실습 B 필수 | – | 공개 예정<br>10/16(금) 08:30 |
| `d3_features_panel.csv`<br>바이어 × 월 패널 | 같은 특성의 월별 패널(4,017행, 2024-01~2026-08, 연체 215건). 표준 트랙의 시간 분할 비교 · 오전 시연 1의 입력 | 실습 A 선택 | – | 공개 예정<br>10/16(금) 08:30 |
| `d3_grade_banding.xlsx`<br>등급 매칭 시트 | 실습 B-1: pred 시트에 점수를 붙이고 이름 t(빈칸)에 내 임계값 → 직접 쓰는 IFS 등급(C부터) · 경계 · 분포 · 단조성(시험셋) 시트 | 실습 B 필수 | 33 KB | [:material-download: 받기](downloads/day3/d3_grade_banding.xlsx){ download="d3_grade_banding.xlsx" } |
| `fx_forecast_inputs.csv`<br>환율 예측 입력 | 원/달러 일별 종가 767행(FRED DEXKOUS, 2023-09~2026-09)과 학습(train)·확인(valid) 구간 표시. 실습 B-2의 환율 위험 구간 | 실습 B 필수 | 73 KB | [:material-download: 받기](downloads/day3/fx_forecast_inputs.csv){ download="fx_forecast_inputs.csv" } |
| `d3_shap_report_template.docx`<br>근거 메모 양식 | 실습 B-2: 메모 프롬프트(B4)의 출력 5칸(결론 · 위험↑ 3 · 위험↓ 2 · 확인할 것 3 · 한계 3) + 그림 2칸 — A4 1장. Markdown판도 있다 | 실습 B 선택 | 37 KB | [:material-download: 받기](downloads/day3/d3_shap_report_template.docx){ download="d3_shap_report_template.docx" } |
| `shap_sample_3buyers.csv`<br>SHAP 표본 3곳(채팅 경로용) | B118 · B005 · B085의 pd_30d · 등급 · 위험을 올린 상위 3 · 낮춘 상위 2(강사 모델 값). 내 PC에서 SHAP을 못 돌릴 때 근거 메모(B4)를 쓰는 재료 | 실습 B 선택 | – | 공개 예정<br>10/16(금) 08:30 |
| `fred_dexkous.csv`<br>FRED 원/달러 원본 | 미국 연준 FRED DEXKOUS 원본 시계열(퍼블릭 도메인, 출처 표기 요청). 오전 시연 2에서 인터넷이 막혔을 때의 대체 입력 | 실습 B 참고 | 15 KB | [:material-download: 받기](downloads/day3/fred_dexkous.csv){ download="fred_dexkous.csv" } |
| `day3_slides.pdf`<br>강의 슬라이드(PDF) | 그날 강의 슬라이드의 수강생판 — 발표자 노트 제외, 외부 기관 화면 캡처는 자리 표시(강의장에서만 보여 준다). 당일 18:00 공개 | 실습 A · 실습 B 참고 | – | 공개 예정<br>10/16(금) 18:00 |

!!! note "공개 전 파일"
    '공개 예정'으로 표시된 파일은 적힌 시각에 이 표에 링크가 생깁니다. 시각이 지났는데도 링크가 없으면 화면을 새로 고치고, 그래도 없으면 강사에게 알려 주세요.
