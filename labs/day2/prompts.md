# 2일차 프롬프트 — 실습 A · B · 8교시

오후 실습에서 쓰는 프롬프트 전문입니다. 슬라이드에 나온 프롬프트와 **글자가 같습니다**(실습 B 슬라이드에는 한 줄 요약만 있고, 전문이 여기 있습니다). 복사 버튼 :material-content-copy: 으로 통째로 복사하고, `{중괄호}` 자리만 내 상황에 맞게 바꿔 붙여 넣습니다(중괄호 기호도 지웁니다).

| 쓰는 도구 | 어디서 | 이 페이지의 프롬프트 |
|---|---|---|
| **Claude Code** (VS Code 확장) | 내 저장소를 연 VS Code | [A1](#a1) · [A2](#a2) · [A3](#a3) · [A4](#a4) · [A5](#a5) · [A6](#a6) · [B1](#b1) · [B2](#b2) · [B3](#b3) · [B4](#b4) · [B5](#b5) · [B6](#b6) · [안 맞을 때](#mismatch) |
| **Claude · ChatGPT 웹** | 브라우저 새 대화 | 실습 B ② [약관 읽기](#terms) · 막혔을 때의 [채팅 경로](#chat-path) |

!!! info "'2일차 작업 폴더' · 'outputs 폴더' · 'scripts 폴더'는 어디인가"
    프롬프트에 나오는 **2일차 작업 폴더**는 이 저장소에서 `workbench/day2/`입니다. `rules/`(규칙) · `prompts/`(프롬프트) · `data/`(작업 사본 · 데이터 사전) · `outputs/`(결과) · `tests/`(테스트)가 그 안에 있습니다. 프롬프트의 **outputs 폴더**는 `workbench/day2/outputs/`이고, **scripts 폴더**는 저장소 맨 위의 `scripts/`입니다 — 저장소의 `CLAUDE.md`에 적혀 있어서 Claude Code가 먼저 읽습니다. 경로를 정확히 쓰고 싶으면 프롬프트의 `outputs/…`를 `workbench/day2/outputs/…`로 바꿔 써도 됩니다.

!!! tip "권한 모드는 일의 성격에 맞춰 바꿉니다"
    입력창 아래의 모드 표시기를 누르면 바뀝니다. **Manual**로 시작해서 → 진단할 때는 **Plan**(읽기만 · 고치지 못함) → 만들 때는 **Edit automatically**(파일 편집은 묻지 않음). Edit automatically에서도 **명령 실행은 허락 창이 뜹니다** — 읽고 `1 Yes`. `2 … for this project`처럼 허락 범위를 넓히는 선택은 쓰지 않습니다.

## 빈칸 값 {#values}

| 빈칸 | 값 | 쓰는 곳 |
|---|---|---|
| `{중위수 또는 KNN}` | **내가 고른** 결측 채우기 방식 — `중위수` 또는 `KNN` 한 단어(고른 이유는 규칙 문서 '왜' 칸에 씁니다) | A2 |
| `{번호}` | 내 저장소에 만든 이슈 번호(숫자만, 예: `1`) | A6 |

## 프롬프트를 쓰는 습관 {#habits}

1. **진단과 수정을 나눈다** — Plan 모드로 진단만 시키고, 무엇을 어떻게 고칠지는 **사람이 정해** 규칙 문서에 먼저 씁니다. 그다음에 스크립트로 옮기게 합니다.
2. **한 번에 하나** — 네 개를 한꺼번에 붙여 넣으면 어디서 틀렸는지 찾을 수 없습니다. 결과를 읽은 뒤 다음으로 갑니다.
3. **숫자는 코드가, 확인은 손으로** — 계산은 스크립트가 하고, 한 건(B001)은 엑셀로 직접 검산합니다.
4. **틀리면 바로 고치게 하지 않는다** — "어느 규칙에서 갈렸나"를 먼저 묻습니다([안 맞을 때](#mismatch)). 테스트와 규칙 중 어느 쪽이 틀렸는지 판단하는 것이 사람의 몫입니다.
5. **허락 창은 읽고 승인한다** — 무엇을 · 어디에 · 지우는지 세 가지를 읽고 `1 Yes`. 파일 삭제 · 강제 push · `git reset --hard`는 거절합니다.
6. **잘 된 프롬프트는 저장한다** — `workbench/day2/prompts/`에 이름 + 판 번호로 두고, 고칠 때마다 커밋합니다(오늘의 `news_score_v1.md`처럼).

---

## A1 · 진단 — 고치지 않고 표로 {#a1}

**도구** Claude Code · **모드 Plan** · **실습 A ②** · 결과 화면의 진단 표(저장은 아래 한 줄)

<!-- --8<-- [start:a1] -->
```text
[Plan 모드] data/checkpoints/d2_start.xlsx의 buyers 시트를 진단만 해 줘. 열별 타입·결측·표기 종류·의심 값을 표로. 고치지 마.
```
<!-- --8<-- [end:a1] -->

맨 앞 `[Plan 모드]`는 "이 프롬프트는 Plan 모드로 보낸다"는 표시입니다. 모드를 먼저 바꾸고 보내면 지워도 됩니다.

**어떻게 생겼나** 시연 2의 첫 프롬프트를 buyers 시트 하나로 줄인 것입니다. **"진단만 해 줘 · 고치지 마"**가 핵심입니다 — 진단과 수정을 한 번에 시키면 무엇을 왜 고쳤는지 검토할 기회가 사라집니다.

**끝난 뒤** 계획 승인 창이 뜨면 **`3 No, keep planning`**을 고릅니다(승인하면 AI가 바로 고치기 시작합니다). 그다음 모드를 **Edit automatically**로 바꾸고 표를 파일로 저장합니다.

<!-- --8<-- [start:a1-save] -->
```text
방금 진단 표를 2일차 작업 폴더의 outputs/profile.md로 저장해 줘.
```
<!-- --8<-- [end:a1-save] -->

**확인할 것** 통화 표기 종류(9가지), 숫자 칸에 섞인 글자, 재무 항목 결측, 자기자본 0 이하, 신용한도에 비해 큰 잔액이 표에 보이는지 봅니다. AI가 **'사람이 정해야 한다'고 짚은 곳**이 곧 A2에서 내가 정할 규칙입니다.

---

## A2 · 규칙 문서 — 사람이 정한 규칙을 넘긴다 {#a2}

**도구** Claude Code · **모드 Edit automatically** · **실습 A ③** · 결과 `workbench/day2/rules/정제규칙.md` 1–7칸

<!-- --8<-- [start:a2] -->
```text
진단 결과로 2일차 작업 폴더의 rules/정제규칙.md 1–7칸을 '규칙/왜' 두 줄씩 채워 줘. 결측은 {중위수 또는 KNN} + 결측 플래그.
```
<!-- --8<-- [end:a2] -->

`{중위수 또는 KNN}`은 **내가 고른 방식**으로 바꿉니다([빈칸 값](#values)). 짝과 다른 방식을 골라 결과를 비교해도 좋습니다.

**덧붙임 — 확인표를 맞추려면(권장)** 위 프롬프트 끝에 이어 붙입니다. 확인표의 숫자(결측 플래그 47곳 · 단위 의심 · 자본잠식)가 아래 정의를 전제로 하기 때문입니다. 다르게 정하고 싶다면 정한 대로 쓰되, 확인표와 달라지는 곳이 생길 수 있습니다.

<!-- --8<-- [start:a2-decide] -->
```text
결정: 결측 플래그 fin_missing은 유동자산·유동부채·총부채·자기자본·매출 중 하나라도 빈칸이면 1 · 잔액이 신용한도의 10배를 넘으면 unit_flag=1 후 ÷1,000 · 자기자본이 0 이하면 부채비율은 빈칸 + neg_equity=1 · 국가위험 '-'는 country_risk=0 + crc_unclassified=1 · 환율은 기준일 2026-08-31 값으로 USD 환산(엔화는 100엔 단위) · 환율 변화 열 fx_chg_30d는 시트 fx_at_ref의 chg_30d, fx_chg_30d_lag30은 fx_krw_daily.csv로 '30일 전 환율 ÷ 60일 전 환율 − 1'.
```
<!-- --8<-- [end:a2-decide] -->

**확인할 것**

- `workbench/day2/rules/정제규칙.md` 1–7칸마다 `규칙:`과 `왜:`가 **둘 다** 채워졌는지, 3칸에 결측 플래그의 정의가 있는지 봅니다.
- 소스 제어 화면에서 diff를 봅니다 — **규칙 문서만** 바뀌고 `data/`의 원본은 그대로여야 합니다.
- AI가 규칙을 되묻는 질문(예: "JPY 잔액을 한도와 어떻게 비교할까요?")은 **사람이 정할 결정**입니다. 짝과 의논해 답합니다.

---

## A3 · 정제 스크립트 — 규칙대로, 원본은 읽기만 {#a3}

**도구** Claude Code · **모드 Edit automatically** · **실습 A ④** · 결과 `scripts/clean_buyers.py` · `workbench/day2/outputs/d2_buyers_clean.csv` · `workbench/day2/outputs/dq_report.md`

<!-- --8<-- [start:a3] -->
```text
규칙대로 scripts/clean_buyers.py를 만들고 uv run으로 실행해. 원본은 읽기만, 결과는 outputs/d2_buyers_clean.csv, 전·후 비교는 outputs/dq_report.md.
```
<!-- --8<-- [end:a3] -->

**덧붙임 — 3일차 입력으로 쓰려면(권장)** 정제 결과 표에 아래 25열이 있어야 오후 실습 B와 내일 3일차가 이어집니다. 열 이름은 이대로 맞춥니다.

<!-- --8<-- [start:a3-columns] -->
```text
결과 열: buyer_id · payment_method · ccy_clean · amt_num · ar_balance_usd · pct_current · pct_ar_31p · pct_91plus · max_dpd · avg_days_late · late_ratio · dpd_trend · dispute_ratio · current_ratio · debt_to_equity · dso_buyer · op_margin · fin_missing · neg_equity · country_risk · crc_unclassified · unit_flag · fx_chg_30d · fx_chg_30d_lag30 · late_30d(마지막 열). 150행, buyer_id는 첫 열.
```
<!-- --8<-- [end:a3-columns] -->

**확인할 것**

- `scripts/clean_buyers.py`가 **원본 엑셀을 덮어쓰지 않는지**(읽기만 하는지) 훑어봅니다. `git status`에 `data/` 변경이 없어야 합니다.
- `outputs/dq_report.md`에 **전·후 건수 표**(통화 표기 9종 → 4종 · 글자 섞인 칸 · 결측)가 있는지 봅니다.
- 실행 결과가 150행인지 봅니다. 숫자는 AI의 암산이 아니라 **스크립트가 낸 값**이어야 합니다.

---

## A4 · 테스트 — 규칙의 실행 가능한 판 {#a4}

**도구** Claude Code · **모드 Edit automatically** · **실습 A ⑤** · 결과 `workbench/day2/tests/test_clean.py`

<!-- --8<-- [start:a4] -->
```text
행 수·ID 유일·통화 4종·금액 ≥ 0·B072 단위 플래그 테스트를 쓰고, 통과할 때까지 고친 뒤 커밋해 줘.
```
<!-- --8<-- [end:a4] -->

테스트 파일은 `CLAUDE.md` 규칙에 따라 2일차 작업 폴더의 `tests/`에 만들어집니다. 저장소 맨 위에서 `uv run pytest -q`를 치면 그 폴더의 테스트가 돕니다(저장소의 `pytest.ini`가 대상을 `workbench/`로 정해 둡니다). 다른 곳에 만들어졌다면 `uv run pytest -q 경로`로 돌립니다.

**테스트가 실패하면** 바로 "고쳐 줘"라고 하기 전에 **테스트와 규칙 중 어느 쪽이 틀렸는지** 먼저 판단합니다. 시연 2에서도 첫 실행에 열 하나가 빠져 실패했고, AI는 테스트가 아니라 결과를 고쳤습니다. 그 판단이 맞았는지 내가 확인하는 것이 사람의 몫입니다.

---

## A5 · 스케일 비교 표 — 선택, 특성 파일에는 넣지 않는다 {#a5}

**도구** Claude Code · **실습 A ⑤(먼저 끝난 사람)** · 결과 `workbench/day2/outputs/scaling.md`

<!-- --8<-- [start:a5] -->
```text
revenue를 로그 변환한 뒤 Min-Max와 표준화로 바꾼 비교 표(최소·중앙값 근처·최대 바이어 3곳)를 outputs/scaling.md로 만들어 줘. 특성 파일에는 넣지 마.
```
<!-- --8<-- [end:a5] -->

**확인할 것** 매출이 약 190배 차이 나는 바이어 3곳이 Min-Max · 표준화에서 어떻게 달라지는지 봅니다(극단값 한 곳이 나머지를 0 쪽으로 누릅니다). 규칙 문서에 **"정규화 열을 특성 파일에 넣지 않는 이유"** 한 줄을 적습니다 — 평가 데이터의 정보가 섞이고, 내일의 트리 모델은 스케일에 둔감합니다.

---

## A6 · 커밋 · push · PR — 선택, Claude Code에게 시켜도 됩니다 {#a6}

**도구** Claude Code · **실습 A ⑥** · 슬라이드에는 없는 보조 프롬프트입니다(VS Code 소스 제어와 GitHub 웹으로 직접 해도 같은 결과).

<!-- --8<-- [start:a6] -->
```text
지금까지의 변경을 두 커밋으로 나눠 줘: ① 규칙 문서(workbench/day2/rules/정제규칙.md) ② 스크립트·테스트·결과. 메시지는 CLAUDE.md 형식(첫 줄 '2일차: 무엇', 한 줄 비우고 '왜: 이유')으로 써. push한 뒤 PR을 만들어 줘. 본문 첫 줄은 'Closes #{번호}', 이어서 dq_report 요약 5줄과 내가 정한 규칙 목록.
```
<!-- --8<-- [end:a6] -->

**확인할 것** 허락 창의 명령에서 **커밋 메시지가 두 줄인지**, **어느 브랜치로 push하는지**(`d2-clean`, `main`이 아님)를 읽고 승인합니다. 컴퓨터에 GitHub CLI(`gh`)가 없으면 PR 만들기에서 멈춥니다 — 그때는 GitHub 저장소 화면 위쪽의 **Compare & pull request** 단추로 만듭니다. **머지는 Claude Code에게 시키지 않고** 브라우저에서 내가 누릅니다.

---

## B1 · 새 작업대에서 환경 다시 만들기 {#b1}

**도구** Claude Code(새 창 — worktree) · **실습 B ①** · 결과 `.venv` · 오늘 파일

<!-- --8<-- [start:b1] -->
```text
이 폴더는 새 worktree야. uv sync로 환경을 만들고 uv run python tools/get_day_files.py 2로 오늘 파일을 다시 받아 줘. 끝나면 현재 브랜치와 git status를 보여 줘.
```
<!-- --8<-- [end:b1] -->

**어떻게 생겼나** 새 작업 폴더에는 `.venv`와, `.gitignore`로 뺀 받은 파일(`data/checkpoints/`)이 **없습니다.** 그래서 환경과 파일을 다시 만들게 합니다 — 오전 worktree 장의 '주의'를 직접 겪는 장면입니다.

**확인할 것** 현재 브랜치가 `d2-news`인지, `git status`가 깨끗한지(받은 파일은 `.gitignore` 때문에 보이지 않습니다) 봅니다.

---

## 수집 점검 · 약관 읽기 — Claude 웹 {#terms}

**도구** **Claude 웹**(또는 ChatGPT) 새 대화 · **실습 B ②** · 결과 `workbench/day2/rules/수집점검.md`의 4칸(약관 조항 원문)

관심 바이어 국가의 뉴스 사이트 한 곳을 정하고, 그 사이트의 이용약관 전문을 열어 아래 프롬프트의 맨 끝에 붙여 넣습니다. **오늘은 점검만 합니다 — 기사를 수집하지 않습니다.**

<!-- --8<-- [start:terms] -->
```text
아래는 {사이트 이름}의 이용약관이다. 자동 수집·크롤링·스크래핑·봇·AI 학습·데이터 마이닝을 금지하거나 제한하는 조항을 찾아, 원문 문장을 한 글자도 바꾸지 말고 그대로 인용해 표로 만들어 줘. 열: 조항 위치 | 원문 | 무엇을 금지하나. 해당 조항이 없으면 '없음'이라고만 쓰고 추측하지 마.

{이용약관 전문 붙여넣기}
```
<!-- --8<-- [end:terms] -->

**확인할 것** AI가 인용한 문장을 **약관 원문에서 ++ctrl+f++ 로 직접 찾아** 글자 그대로 있는지 봅니다. 없는 문장이면 근거로 쓰지 않습니다. 원문이 영어여도 인용은 원문 그대로 둡니다. 결론은 **API 사용 / 수동 열람만 / 수집 불가** 셋 중 하나로 `수집점검.md`에 씁니다.

---

## B2 · 뉴스 채점 — 규칙대로, 네가 직접 {#b2}

**도구** Claude Code(`d2-news` 창) · **실습 B ③** · 결과 `workbench/day2/outputs/news_scored.jsonl`

<!-- --8<-- [start:b2] -->
```text
2일차 작업 폴더의 prompts/news_score_v1.md 규칙대로 data/checkpoints/d2_news.csv 1–50행을 네가 직접 읽고 채점해 줘(외부 API나 키워드 규칙 스크립트는 쓰지 마). 결과는 outputs/news_scored.jsonl에 한 행 = JSON 한 줄(news_id · buyer_id · date · news_sent_0_10 · label · evidence · confidence)로 붙여 써. 끝나면 51–100행도 같은 방식으로.
```
<!-- --8<-- [end:b2] -->

**어떻게 생겼나** 오전 시연 5를 줄인 것입니다 — API 대신 **Claude Code 세션 안에서 AI가 직접** 읽고 채점하므로 키가 필요 없습니다. **"네가 직접"**이 핵심입니다. 키워드 규칙 스크립트로 점수를 매기게 하면 AI 채점이 아니라 규칙 코드가 됩니다. 채점 규칙은 내 저장소의 `workbench/day2/prompts/news_score_v1.md`(관점 · 척도 · 근거 · 형식)입니다.

**확인할 것** `news_scored.jsonl`이 한 줄에 JSON 하나인지, 키 7개(news_id · buyer_id · date · news_sent_0_10 · label · evidence · confidence)가 모두 있는지 봅니다. 채점 중에 파일을 이어 쓰는지(처음 50행 뒤에 51–100행이 붙는지)도 봅니다.

---

## B3 · 검사 스크립트 — 위반 행만 다시 채점 {#b3}

**도구** Claude Code · **실습 B ③** · 결과 `scripts/validate_scores.py`

<!-- --8<-- [start:b3] -->
```text
scripts/validate_scores.py를 만들어 news_scored.jsonl을 검사해 줘: 100줄인지, 점수가 0–10 정수인지, 라벨이 점수 대역(0–2 severe, 3–4 high, 5 watch, 6–10 low)과 맞는지, evidence가 원문 headline·body_short 안에 그대로 있는지. 위반 행만 다시 채점해서 고쳐.
```
<!-- --8<-- [end:b3] -->

**어떻게 생겼나** 형식 검사는 AI의 눈이 아니라 **스크립트**가 합니다. 위반이 나온 행만 다시 채점하게 해서 이미 맞은 행의 점수는 건드리지 않습니다. evidence가 원문에 그대로 있는지 보는 검사는 AI가 번역 · 요약해서 옮긴 근거를 잡습니다.

**확인할 것** 검사 결과가 **위반 0**으로 끝나는지, 다시 채점한 행이 있다면 어느 줄이었는지 봅니다.

---

## B4 · 평가 — 정답 20건과 비교 {#b4}

**도구** Claude Code · **실습 B ④** · 결과 `workbench/day2/outputs/eval.md`

15:35 이후 `uv run python tools/get_day_files.py 2`를 한 번 더 실행하면 정답 파일 `d2_news_answer.csv`가 `data/checkpoints/`에 들어옵니다. 그다음 보냅니다.

<!-- --8<-- [start:b4] -->
```text
data/checkpoints/d2_news_answer.csv(정답 20건)와 비교해 MAE · ±2 이내 비율 · 라벨 일치율을 계산하고 outputs/eval.md로 써 줘. 차이가 가장 큰 2건은 원문과 함께 이유를 한 줄씩.
```
<!-- --8<-- [end:b4] -->

**확인할 것** 숫자(MAE · ±2 이내 비율 · 라벨 일치율)와 **오차가 큰 2건의 원인**이 `eval.md`에 있는지 봅니다. 평가 숫자는 사람마다 다르게 나오는 것이 정상입니다. 숫자가 나쁘면 실패가 아니라 **프롬프트 v2를 만들 이유**입니다.

---

## B5 · 융합 — 30일 창 집계와 LEFT JOIN {#b5}

**도구** Claude Code · **실습 B ⑤** · 결과 `workbench/day2/outputs/d2_end_features.csv`

<!-- --8<-- [start:b5] -->
```text
기준일 2026-08-31, 창 (2026-08-01, 2026-08-31]로 바이어별 뉴스 건수 · 평균 · 최솟값과 news_risk_30d(10 − 평균)를 만들고 outputs/d2_buyers_clean.csv에 buyer_id로 LEFT JOIN해 줘. d2_start.xlsx의 buyer_features_raw(기준일 08-31)에서 cum_dpd_days와 overdue_amount(기준일 환율로 USD 환산 → overdue_usd)도 붙여. 뉴스가 없으면 평균 5 + no_news_flag=1. 결과는 outputs/d2_end_features.csv(buyer_id 첫 열, late_30d 끝 열). 9월 기사가 0건인지, 150행인지, ID 중복이 없는지 검사하는 줄도 넣어.
```
<!-- --8<-- [end:b5] -->

**어떻게 생겼나** 시연 3의 시간 창 집계와 LEFT JOIN을 한 문장에 담았습니다. 창은 `(08-01, 08-31]` — 8월 1일은 빼고 8월 31일은 넣습니다. 기준일 **뒤**(9월) 기사가 섞이면 특성에 미래가 들어간 것입니다. 뉴스가 없는 바이어는 **평균 5 + `no_news_flag=1`**로 채워 행이 사라지지 않게 합니다.

**확인할 것** 150행 · `buyer_id` 첫 열 · `late_30d` 끝 열 · ID 중복 0, 그리고 9월 기사 0건. 새 열(`overdue_usd` · `cum_dpd_days` · `news_cnt_30d` · `news_sent_0_10_30d` · `news_sent_min_30d` · `news_risk_30d` · `no_news_flag`)이 모두 있으면 `workbench/day2/data/데이터사전.md`에 한 줄씩 적습니다.

**이어서 — 데이터 사전에 새 열 적기(선택 · 초안만 AI)** 새 열의 뜻 · 계산은 AI에게 받아도 되지만 **'시점 점검' 칸은 내가 채웁니다**(그 열이 기준일 이전 정보만으로 만들어졌는지).

<!-- --8<-- [start:b5-dict] -->
```text
workbench/day2/data/데이터사전.md의 표에 d2_end_features.csv의 새 열(overdue_usd · cum_dpd_days · news_cnt_30d · news_sent_0_10_30d · news_sent_min_30d · news_risk_30d · no_news_flag)을 같은 모양으로 한 줄씩 추가해 줘. 뜻과 계산은 쓰고, '시점 점검' 칸은 비워 둬 — 내가 쓴다.
```
<!-- --8<-- [end:b5-dict] -->

---

## B6 · 8교시 — main을 반영해 충돌 풀기 {#b6}

**도구** Claude Code · **8교시 합치기** · 충돌이 날 때만 씁니다.

<!-- --8<-- [start:b6] -->
```text
main을 반영해 충돌을 풀고 diff를 보여 줘
```
<!-- --8<-- [end:b6] -->

더 구체적으로 시키려면 이렇게 보냅니다 — **두 변경을 모두 살리고, 테스트 뒤에 push**하라는 말까지 넣습니다.

<!-- --8<-- [start:b6-long] -->
```text
main이 바뀌었어. origin/main을 이 브랜치에 merge하고, 충돌이 나면 두 변경을 모두 살리는 쪽으로 해결해 줘. 해결한 diff를 보여 주고 테스트 후 push해 줘.
```
<!-- --8<-- [end:b6-long] -->

**확인할 것** 해결된 diff를 **내가 읽고** 나서 머지 단추를 누릅니다. 충돌 표식(`<<<<<<<` · `=======` · `>>>>>>>`)이 파일에 남아 있지 않은지 봅니다.

---

## 안 맞을 때 — 어느 규칙에서 갈렸나 {#mismatch}

확인표의 숫자와 내 결과가 다르면 **바로 고치게 하지 말고** 먼저 원인을 묻습니다.

<!-- --8<-- [start:mismatch] -->
```text
확인표에서 {항목}은 {기대값}인데 내 결과는 {내 값}이야. 고치지 말고, 어느 규칙(정제규칙.md 몇 번 칸)에서 갈렸는지 찾아서 원인 후보와 확인 방법만 알려 줘.
```
<!-- --8<-- [end:mismatch] -->

`{항목}` · `{기대값}` · `{내 값}`을 바꿔 보냅니다. 원인이 규칙 문서에 있으면 **규칙 문서를 먼저 고치고**(+ '9. 변경 기록' 한 줄) 스크립트를 다시 돌립니다. 중위수 대신 KNN을 골랐다면 대체값이 달라지는 것이 정상이고, 결측 플래그 개수는 같아야 합니다.

---

## 채팅 경로 — Claude Code를 못 쓸 때 {#chat-path}

Claude Code 계정이 없거나(무료 플랜은 쓸 수 없습니다) 확장이 로그인되지 않으면 **Claude 또는 ChatGPT 웹**에 파일을 올려 같은 일을 합니다. 프롬프트는 같고, 아래 세 가지만 바꿉니다.

| 바꿀 곳 | 어떻게 |
|---|---|
| 파일 경로(`data/checkpoints/…`) | 지우고 **파일을 첨부**합니다(`d2_start.xlsx` · `d2_news.csv` · 정답 20건). ChatGPT 무료는 하루 업로드 수가 적으니 Claude를 먼저 권합니다 |
| "scripts/… 를 만들고 uv run으로 실행해" | **"코드를 실행해서 처리하고 결과 파일을 내려받게 해 줘"**로 바꿉니다(Claude는 코드 실행, ChatGPT는 데이터 분석 기능). 실행 코드도 답에 보여 달라고 합니다 |
| "outputs/…에 저장해" | 지우고 **"CSV(또는 Markdown) 파일로 내려받게 해 줘"**로 바꿉니다. 받은 파일은 내 PC에서 같은 이름으로 `workbench/day2/outputs/`에 둡니다 |

- **A 대체**: A1–A3과 같은 요청을 합니다. 규칙 문서는 채팅 답을 복사해 `정제규칙.md`로 저장합니다(양식은 `labs/day2/rules_template.md`).
- **B 대체**: 채팅에 `workbench/day2/prompts/news_score_v1.md`의 내용을 붙이고 그 아래에 뉴스 **50행씩 두 번** 붙여 JSON Lines를 받습니다. 먼저 [워밍업 10건](../day2/lab-b.md#files)으로 형식을 시험해도 좋습니다. 이어 같은 채팅의 코드 실행(Claude) 또는 데이터 분석(ChatGPT)에 JSONL · 정답 CSV · 정제 CSV를 올려 B3–B5와 같은 검사 · 평가 · 결합을 시킵니다.
- 올리기: GitHub 웹 화면의 **Add file → Upload files**(순서는 [실습 A의 채팅 경로](../day2/lab-a.md#chat-path)).
- Claude 유료 계정(Pro · Max)이면 데스크톱 앱에 작업 폴더를 연결해 같은 정리를 맡기는 길(Cowork)도 있습니다. 요즘은 채팅과 Cowork가 한 Claude로 합쳐지는 중이라 계정에 따라 메뉴가 다릅니다. **연결한 폴더의 파일은 Anthropic 클라우드에서 처리되므로** 오늘처럼 합성 데이터일 때만 씁니다.

!!! warning "데이터 위생"
    이 프롬프트는 가상(합성) 데이터용입니다. 회사 실데이터는 익명화한 것이라도 올리지 않습니다. 쓰는 AI의 '모델 개선(학습)' 설정은 끄고 시작합니다.
