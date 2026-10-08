<!-- 자동 생성: tools/sync_site_assets.py — 직접 고치지 말고 스크립트를 다시 돌리세요 -->

| 파일 | 무엇인가 | 쓰는 곳 | 크기 | 받기 |
|---|---|---|---|---|
| **`day5_files.zip`**<br>**한 번에 받기** | 지금까지 공개된 아래 파일을 `D5` 폴더 하나로 묶은 압축 파일 · 하위 폴더 `D5/rag` 포함 | 전체 | 36 KB | [:material-folder-download: **받기**](../downloads/day5/day5_files.zip){ download="day5_files.zip" } |
| `d5_start.csv`<br>5일차 시작 파일(미결 인보이스) | 2026-09-30 기준 미결 인보이스(300행 이하) · 29열(등급 · 한도 · 독촉 단계 · 통지 기한 · 미결 잔액 포함). 앱 ⓪ 통합 상황판 · 환율 타일의 입력(메일 주소는 가상) | 실습 B 필수 | – | 공개 예정<br>10/20(화) 08:30 |
| `hanbit_credit_policy.pdf`<br>(가상) 한빛정밀 여신관리규정 PDF | 가상 사내 규정(11쪽 · 35조 + 부칙 + 별표 4개). 채팅 프로젝트에 올리고(실습 A2) Claude Code가 조 단위로 자른다(A3) | 실습 A 필수 | – | 공개 예정<br>10/20(화) 08:30 |
| `goldset_20.csv`<br>골든셋 20문항(평가 코드용) | 질문 · 기대 답 · 근거 조항 · 유형(기권 문항 포함). 정답 칸이 있어 평가 코드(eval.py)만 읽는다 — 채팅 프로젝트에는 올리지 않는다 | 실습 A 필수 | 8 KB | [:material-download: 받기](../downloads/day5/rag/goldset_20.csv){ download="goldset_20.csv" } |
| `goldset_questions.csv`<br>골든셋 질문 목록(채팅 경로) | 골든셋의 질문 두 열(q_id · question) 20줄 — 정답 칸이 없다. 채팅 경로에서 대화창에 붙인다 | 실습 A 선택 | – | 공개 예정<br>10/20(화) 08:30 |
| `eval_sheet_template.xlsx`<br>검색 평가 시트(채팅 경로) | 채팅으로 받은 조항 ID 상위 5개(r1–r5)를 붙이면 규정 정답 10문항의 P@K · R@K · F1@K(K = 1 · 3 · 5) · Hit@3 · MRR · Top-K가 계산된다. 실험 전후 두 탭 | 실습 A 선택 | 21 KB | [:material-download: 받기](../downloads/day5/rag/eval_sheet_template.xlsx){ download="eval_sheet_template.xlsx" } |
| `hanbit_credit_policy.md`<br>(가상) 여신관리규정 텍스트판 | 같은 규정의 Markdown 판 — PDF에서 글자가 잘 안 뽑힐 때의 대체 입력(조 머리 `## 제N조`) | 실습 A 선택 | 23 KB | [:material-download: 받기](../downloads/day5/rag/corpus/hanbit_credit_policy.md){ download="hanbit_credit_policy.md" } |
| `README.md`<br>RAG 문서 안내 · 공식 링크 | 무엇을 어디서 받나: 수출보험 약관 · 법령은 공식 사이트 링크에서 각자 받는다(재배포 금지) + 조항 ID 규칙 · 조 단위로 자르는 법 | 실습 A 참고 | 6 KB | [:material-download: 받기](../downloads/day5/rag/corpus/README.md){ download="README.md" } |
| `spec_fx_tile.md`<br>요구사항 카드 — 환율 타일 | '원화 환산(오늘 환율)' 타일의 목적 · 화면 · 완료 기준(Given · When · Then) · 데이터와 계산 · 하지 않을 것. 내 사본에 Then 한 줄을 더한다(실습 B2) | 실습 B 필수 | – | 공개 예정<br>10/20(화) 08:30 |
| `tone_matrix.csv`<br>독촉 톤 표(연체 단계 × 등급 → 템플릿) | 기본값은 지금 앱의 규칙 그대로. 내 사본의 한 칸 이상을 고쳐 라우팅이 표를 읽게 만든다(실습 B4) | 실습 B 필수 | – | 공개 예정<br>10/20(화) 08:30 |
| `upload_sample.csv`<br>대시보드 업로드 연습 파일 | 앱 ① 업로드 → 자동 전처리 화면을 시험해 보는 작은 샘플(입력 오류 포함, 100행 + 중복 1행, 가상 데이터) | 실습 B 선택 | 9 KB | [:material-download: 받기](../downloads/day5/upload_sample.csv){ download="upload_sample.csv" } |
| `ax_proposal_template.md`<br>AI 도입 기획서 양식(11장) | 오늘 21:00까지 1–6장 초안을 plan_draft__T{조}-{번호}.docx로(비공개 폼) → 6일차에 7–11장. Word · Google Docs로 옮겨 .docx로 낸다 | 실습 B 필수 | 8 KB | [:material-download: 받기](../downloads/day5/ax_proposal_template.md){ download="ax_proposal_template.md" } |
| `day5_slides.pdf`<br>강의 슬라이드(PDF) | 그날 강의 슬라이드의 수강생판 — 발표자 노트 제외, 외부 기관 화면 캡처는 자리 표시(강의장에서만 보여 준다). 당일 18:00 공개 | 실습 A · 실습 B 참고 | – | 공개 예정<br>10/20(화) 18:00 |

!!! note "공개 전 파일"
    '공개 예정'으로 표시된 파일은 적힌 시각에 이 표에 링크가 생깁니다. 시각이 지났는데도 링크가 없으면 화면을 새로 고치고, 그래도 없으면 강사에게 알려 주세요.
