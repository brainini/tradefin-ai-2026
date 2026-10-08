<!-- 자동 생성: tools/sync_site_assets.py — 직접 고치지 말고 스크립트를 다시 돌리세요 -->

| 파일 | 무엇인가 | 트랙 | 받기 |
|---|---|---|---|
| `hanbit_credit_policy.pdf` | 가상 사내 규정(11쪽 · 35조 + 부칙 + 별표 4개). 채팅 프로젝트에 올리고(실습 A2) Claude Code가 조 단위로 자른다(A3) | 필수 | 공개 예정<br>10/20(화) 08:30 |
| `goldset_20.csv` | 질문 · 기대 답 · 근거 조항 · 유형(기권 문항 포함). 정답 칸이 있어 평가 코드(eval.py)만 읽는다 — 채팅 프로젝트에는 올리지 않는다 | 필수 | [:material-download: 받기](../downloads/day5/rag/goldset_20.csv){ download="goldset_20.csv" } |
| `goldset_questions.csv` | 골든셋의 질문 두 열(q_id · question) 20줄 — 정답 칸이 없다. 채팅 경로에서 대화창에 붙인다 | 선택 | 공개 예정<br>10/20(화) 08:30 |
| `eval_sheet_template.xlsx` | 채팅으로 받은 조항 ID 상위 5개(r1–r5)를 붙이면 규정 정답 10문항의 P@K · R@K · F1@K(K = 1 · 3 · 5) · Hit@3 · MRR · Top-K가 계산된다. 실험 전후 두 탭 | 선택 | [:material-download: 받기](../downloads/day5/rag/eval_sheet_template.xlsx){ download="eval_sheet_template.xlsx" } |
| `hanbit_credit_policy.md` | 같은 규정의 Markdown 판 — PDF에서 글자가 잘 안 뽑힐 때의 대체 입력(조 머리 `## 제N조`) | 선택 | [:material-download: 받기](../downloads/day5/rag/corpus/hanbit_credit_policy.md){ download="hanbit_credit_policy.md" } |
| `README.md` | 무엇을 어디서 받나: 수출보험 약관 · 법령은 공식 사이트 링크에서 각자 받는다(재배포 금지) + 조항 ID 규칙 · 조 단위로 자르는 법 | 참고 | [:material-download: 받기](../downloads/day5/rag/corpus/README.md){ download="README.md" } |
| `day5_slides.pdf` | 그날 강의 슬라이드의 수강생판 — 발표자 노트 제외, 외부 기관 화면 캡처는 자리 표시(강의장에서만 보여 준다). 당일 18:00 공개 | 참고 | 공개 예정<br>10/20(화) 18:00 |
