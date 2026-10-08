# 실습 A · 4–5교시 — 한도 최적화와 스트레스 테스트

!!! abstract "한눈에 보기 — 실습 A"
    | 항목 | 내용 |
    |---|---|
    | 목표 | **정책 손잡이 하나를 바꿨을 때 한도 · 잠재가격 · 손실이 어떻게 달라지는지 숫자로 설명한다** — 바이어별 한도 엔진을 만들어 테스트로 확인하고, 실험 카드 1장과 스트레스 시나리오 1개를 해석해 PR로 남긴다 |
    | 시간 | **13:00–14:50**(110분) · 쉬는 시간 13:50–14:00 |
    | 오전 시연을 이렇게 따라 한다 | 시연 1(규정 문장에서 한도 엔진까지)을 **줄인다** — 설계 1쪽 · 질문 답안 카드 · 속성 테스트 8개를 제공해 모델링 질문을 빨리 끝낸다. 시연 2(쇼크 시뮬레이터)는 **제공 스크립트로 돌리고 내 시나리오 하나를 더해** 해석에 시간을 쓴다. 그리고 **변형**한다 — 실험 카드 9장 중 1장을 골라 사람마다 다른 결과를 낸다(17:00 공유) |
    | 입력 | `labs/day4/MODEL_SPEC.md`(설계 1쪽) · `data/checkpoints/d4_start_scored.csv` · `d4_params.csv` · `d4_open_inv.csv` · `d4_scenarios.csv` · `rag/corpus/hanbit_credit_policy.md`(규정) |
    | 도구 | VS Code · **Claude Code**(Plan → 계획 승인 후 수동 승인) · uv · PuLP 3.3.2 · pytest · Git · GitHub |
    | 산출물 | `scripts/limits_lp.py` · `limits_proposed.xlsx` · `model_card.md` · `stress_results.csv` · `loss_hist.png` · `workbench/day4/experiments.md` / **커밋 + push + PR 1개** |
    | 프롬프트 | [A1](../prompts/day4.md#a1) · [A2](../prompts/day4.md#a2) · [A3](../prompts/day4.md#a3) · [A4](../prompts/day4.md#a4) · [A5](../prompts/day4.md#a5) · [A6](../prompts/day4.md#a6) |

이 실습의 목표는 AI가 최적화 코드를 잘 짜는지 보는 것이 아닙니다. **정책 문장을 어떻게 해석할지(질문에 답하는 일) · 무엇을 완료로 볼지(테스트) · 손잡이를 바꾸면 무엇이 변할지(실험)를 내가 정하고**, AI가 쓴 모델의 숫자를 **테스트로 의심해 보는 것**입니다. 강사가 돌아다니며 한 분씩 2–3분 확인합니다. 막히면 손을 들거나 노트북 위에 빨간 표시(스티커)를 올리세요.

## 슬라이드의 단계 {#slide-steps}

슬라이드 두 장(실습 A · A 시작 프롬프트)과 같은 순서입니다. 아래 ①–⑥이 이 단계를 풀어 쓴 것입니다.

!!! abstract "실습 A · 한도 최적화와 스트레스 테스트 (13:00–14:50)"
    1. **준비** — 브랜치 `d4-limits` · 파일 받기 · `uv sync`
    2. **모델** — Plan 모드 표 · 질문 3개 → 답안 카드 → 코드
    3. **검증** — 속성 테스트 8개 · 걸린 제약 · 잠재가격 기록
    4. **실험 카드 1장** — worktree로 나란히 돌린다
    5. **스트레스** — 제공 스크립트 + 내 시나리오 1개 해석
    6. **14:45 기대값 테스트** → PR(무엇을 · 결과 · 남은 질문)

    산출: 한도안 xlsx · 스트레스 표 · 실험 기록 · PR

## 시간표와 점검 시각 {#time}

| 시각 | 단계 | 하는 일 | 점검 |
|---|---|---|---|
| 13:00–13:10 | [① 준비](#a-prep) | 저장소 열기 · 브랜치 `d4-limits` · 파일 받기 · `uv sync` · 설계 1쪽 읽기 | **13:10** 브랜치 · `MODEL_SPEC.md`가 열린다 |
| 13:10–13:35 | [② 모델](#a-model) | Plan 모드 → A1 → 표와 질문 3개 → 답(A2) → 계획 승인 | **13:35** 표에 결정변수 1 · 목적 1 · 제약 4종 + 상하한 |
| 13:35–13:50 | [③ 검증](#a-test) | 속성 테스트 8개 → `constraints` 시트에서 걸린 제약 · 잠재가격 → `experiments.md` → 커밋 · (선택) 버그 카드 | **13:50** 속성 테스트 8개 통과 · 걸린 제약 2개 |
| 13:50–14:00 | 쉬는 시간 | | |
| 14:00–14:15 | [④ 실험 카드](#a-exp) | 14:00 강사의 worktree 장(2분) → 카드 1장 → 새 창 → A4 → 한 줄 기록 | **14:15** `experiments.md`에 실험 1줄 |
| 14:15–14:40 | [⑤ 스트레스](#a-stress) | `stress_mc.py` → 표 · 그림 · 절감액 → A5 내 시나리오 U1 → 3줄 해석 | **14:40** 기대손실 순서 · 평균 ±3% · 해석 3줄 |
| 14:40–14:50 | [⑥ 대조 · PR](#a-pr) | **14:45 기대값 테스트 공개** → 다시 받기 → 기대값 테스트 → A6 → PR | **14:50** PR 링크 |

!!! tip "늦었다면"
    13:35에 아직 ② 중이어도 괜찮습니다. 막히면 10분 안에 손을 들고, 14:00까지 한도안이 없으면 [채팅 경로](#chat-path)로 바꿉니다. **실습 B는 실습 A의 결과를 쓰지 않으니** 14:50에 못 끝나도 B는 15:00에 새로 시작합니다.

## 입력 파일 {#files}

`uv run python tools/get_day_files.py 4`가 받아 줍니다(아래 ①). 데이터는 **10/19(월) 08:30**에 공개됩니다.

| 파일 | 위치 | 쓰는 곳 |
|---|---|---|
| 설계 1쪽 | `labs/day4/MODEL_SPEC.md` — 기준일 2026-09-30 · 바이어별로 미리 계산할 것 · 결정변수 · 목적 · 제약 4종 · 출력 시트 | ② |
| 바이어 150곳 | `data/checkpoints/d4_start_scored.csv` — 3일차 기준 등급 + 한도 계산 열 | ②–⑤ |
| 정책 숫자 | `data/checkpoints/d4_params.csv` — 65행, `excel_name`으로 찾는다 · 값은 소수(0.04 = 4%) | ② ④ |
| 미결 인보이스 | `data/checkpoints/d4_open_inv.csv` — 300건 · 선적 보류 판정 | ② |
| 시나리오 | `data/checkpoints/d4_scenarios.csv` — S0–S4 + 참고 행 | ⑤ |
| 규정 | `rag/corpus/hanbit_credit_policy.md` — 가상 여신관리규정(질문의 근거) | ② |
| 테스트 | `labs/day4/tests/` — 속성 테스트(`test_limits_props.py` · `test_stress_props.py`)는 이미 있고, **기대값 테스트 2개는 14:45에** 올라옵니다 | ③ ⑤ ⑥ |
| 스트레스 스크립트 | `labs/day4/stress_mc.py`(제공 참고 스크립트) | ⑤ |
| 실험 카드 | `labs/day4/experiment_cards.md` — 9장 | ④ |
| 버그 카드(선택) | `data/checkpoints/d4_params_bug.csv` | ③ |

받은 파일은 `workbench/day4/data/`에 **작업 사본**도 만들어집니다. `data/`의 원본은 읽기만 하고, 고쳐 쓸 것(정책 숫자 · 시나리오)은 사본이나 새 파일로 합니다. 저장소 없이 채팅 경로로 가는 분은 [4일차 → 파일 받기](index.md#files)에서 받습니다.

!!! warning "총액 비율 70%는 규정에 없는 숫자입니다"
    허용 여신 총액 = 바이어 상한의 합 × `TotalCapShare`(0.7)는 **교육용 가정**입니다. 코드에 0.7을 쓰지 않고 `d4_params.csv`에서만 읽게 합니다 — 오늘의 정책 실험이 바로 이 숫자를 바꾸는 일입니다.

---

## ① 준비 (13:00–13:10) {#a-prep}

1. VS Code에서 **내 저장소**를 열고(폴더 **'신뢰'**), 편집기 오른쪽 위의 Claude 아이콘으로 **Claude Code 패널**을 엽니다. 로그인된 상태이고 입력창 아래 모드 표시가 **Manual 또는 Plan**인지 봅니다(Auto로 시작했다면 바꿉니다 — 시작 모드는 PC마다 다릅니다).
2. 터미널을 열고(++ctrl+grave++) 내 PC를 `main`으로 맞춥니다.

    ```text
    git switch main
    git pull
    ```

3. 오늘 파일을 받습니다. 처음 쓰는 PC이면 `uv sync`를 먼저 한 번 합니다.

    ```text
    uv sync
    uv run python tools/get_day_files.py 4
    ```

    `[받음] data/checkpoints/d4_start_scored.csv  (사본 만듦)`처럼 파일마다 한 줄씩 나오면 됩니다. 08:30 전이면 "공개 전"이라고 알려 줍니다 — 시각이 지난 뒤 같은 명령을 다시 실행합니다. `uv sync`가 인터넷(프록시) 때문에 실패하면 손을 듭니다.
4. **브랜치 `d4-limits`**를 만듭니다. 일 하나에 갈래 하나입니다.

    ```text
    git switch -c d4-limits
    ```

5. `labs/day4/MODEL_SPEC.md`를 엽니다(++ctrl+shift+v++ 미리보기). 1쪽짜리 **설계**입니다 — 바이어마다 미리 계산할 값(상한 · 하한 · 계수) → 결정변수 `L` → 목적 → 제약 네 가지. 오늘 'AI에게 시킬 정책 문장'이 이 한 쪽입니다.

<figure markdown="span">
  ![VS Code 탐색기와 MODEL_SPEC.md, 바이어 CSV 미리보기](../assets/screens/d4-limit-inputs.png){ width="760" loading=lazy }
  <figcaption>오전 시연 1의 입력 화면 — 설계 1쪽(MODEL_SPEC.md) · CSV 3종 · 규정을 VS Code에서 연 모습</figcaption>
</figure>

**13:10 점검** — 상태 표시줄에 `d4-limits`가 보이고, `MODEL_SPEC.md`와 `data/checkpoints/d4_*.csv`가 열리는지 봅니다.

---

## ② 모델 — Plan 모드로 표와 질문부터 (13:10–13:35) {#a-model}

AI가 코드를 쓰기 전에 **표로 말하고 질문하게** 합니다. 이 질문에 답하는 것이 사람이 끼어드는 자리입니다.

1. 입력창 아래 모드 표시기를 눌러 **Plan**으로 바꿉니다(파일을 고치지 못하는 읽기 전용 모드입니다).
2. 프롬프트 **A1**을 보냅니다.

    ??? example "프롬프트 A1 — 펼쳐서 복사"
        --8<-- "labs/day4/prompts.md:a1"

3. 계획이 열리기까지 **3분쯤** 걸릴 수 있습니다. 그동안 `MODEL_SPEC.md`를 다시 읽어 둡니다. Plan 중에 `uv run`을 쓰는 승인 창이 뜨면 명령을 읽고 `1 Yes`합니다.
4. 계획에서 **표**(결정변수 · 목적 · 제약)와 **질문 3개**를 읽습니다. 질문은 보통 **규정과 설계가 어긋나는 곳**입니다 — 승인 기준 · 선적 보류 일수 · EL 식 같은 것. 실행마다 조금씩 다르게 나옵니다.
5. 질문에 답합니다(프롬프트 **A2**). **답안 카드**를 펼쳐 해당하는 것을 골라 씁니다.

    ??? example "프롬프트 A2 — 펼쳐서 복사"
        --8<-- "labs/day4/prompts.md:a2"

    ??? note "질문 답안 카드 — Plan이 질문을 올린 뒤에 펼칩니다"
        Plan의 질문은 실행마다 조금 다릅니다. 아래 6문항 가운데 **해당하는 것**을 골라 그대로 답하고, 카드에 없는 질문은 `MODEL_SPEC.md`와 규정으로 따져 내가 정합니다. 답이 규정과 다르면 "모델 카드의 가정 · 한계에 적는다"가 오늘의 약속입니다.

        | # | 질문(흔한 모양) | 답 |
        |---|---|---|
        | 1 | '사람 승인 필요'를 무엇 기준으로 세나? 규정 제15조 ③과 설계는 "현행 대비 30% 이상 감액"이라 한다 | **제안 한도(L) 기준**으로 센다. 다만 신용장 · 전액 선수금 바이어는 신용한도 조항을 적용하지 않으니(규정 제2조 ②) **승인 판정에서 뺀다**(`approval` 열에 '대상 아님'으로 표시) |
        | 2 | 규정 제27조는 연체 45일 초과에서 선적 보류, 설계는 30일(D+30). 어느 쪽? | **설계대로 D+30**(보험 면책 기준). 규정과 다른 점은 `model_card.md`에 '규정 개정 검토 사항'으로 적는다 |
        | 3 | 제16조 EL 식과 설계의 근사식이 다르다 | **설계식**을 쓴다. 차이는 `model_card.md`의 한계에 적는다 |
        | 4 | 총허용익스포저 70%(`TotalCapShare`)는 규정에 없는 숫자인데 그대로 쓰나? | **교육용 가정**이다. `d4_params.csv`의 `TotalCapShare`에서만 읽고 코드에 쓰지 않는다. 오후 실험에서 바꿔 볼 값이다 |
        | 5 | 제17조 ① 바이어 1곳 한도는 자기자본의 10%를 넘지 못한다 — 설계에는 없다. 넣나? | 모든 상한이 그 값보다 작아 **걸릴 수 없으니 제약으로 넣지 않는다.** 코드로 확인만 하고 `model_card.md`에 적는다 |
        | 6 | 계수가 같은 바이어가 여럿이면 한도를 어떻게 나누나? | **솔버가 정한 대로** 둔다. 솔버끼리 비교는 바이어별 한도가 아니라 **목적함수 · 걸린 제약 · 잠재가격**으로 한다 |

        이 카드는 저장소에 넣지 않았습니다 — Plan 중에 Claude가 저장소 파일을 읽으면 질문 없이 답을 가져가기 때문입니다. 14:45에 공개되는 기대값 테스트는 이 답을 기준으로 판정하니, 1번 · 2번 답이 다르면 숫자가 어긋납니다.

6. 계획 승인 창이 뜨면 **`2 Yes, and manually approve edits`**를 고릅니다. 계획대로 실행하되 **파일을 쓰거나 명령을 돌릴 때마다 한 번씩 확인**합니다. 맨 위 `use auto mode`는 고르지 않습니다.
7. 허락 창이 뜨면 **무엇을 · 어디에**(`scripts/limits_lp.py` 새 파일 · `uv run pytest …`)를 읽고 `1 Yes`합니다. Claude는 코드를 쓰고 테스트까지 돌려 **'걸린 제약 2개와 잠재가격의 뜻'을 쉬운 말 3줄**로 정리합니다.

**13:35 점검** — 계획의 표에 **결정변수 1(바이어별 한도 `L`) · 목적 1(연 기대이익) · 제약 4종**(총액 · EL 예산 · 국가별 · B등급 비중)과 바이어별 상하한이 있는지, 내가 질문에 답했는지 봅니다. 코드가 이미 만들어지고 있다면 더 좋습니다.

---

## ③ 검증 — 테스트가 완료를 정한다 (13:35–13:50) {#a-test}

'AI가 다 됐다고 말한 것'은 완료가 아닙니다. **테스트가 통과해야** 완료입니다.

1. 터미널에서 속성 테스트를 돌립니다(Claude가 이미 돌렸다면 한 번 더 내 눈으로).

    ```text
    uv run python scripts/limits_lp.py
    uv run pytest labs/day4/tests/test_limits_props.py -q
    ```

    **8개 모두 통과**해야 합니다(`8 passed`). 속성 테스트는 '답이 얼마인가'가 아니라 **어떤 답이든 지켜야 할 규칙**을 봅니다 — 풀이 상태 Optimal · 모든 한도가 [하한, 상한] 안 · 총액 · EL 예산 · 국가별 합 · B등급 비중 · 선적 보류와 신용장 · 선수금 바이어는 0 · 두 솔버(PuLP와 HiGHS)의 목적함수 차이 < 0.01%.
2. 실패하면 바로 고치게 하지 말고 **고장 보고 4요소**로 정리하게 합니다(프롬프트 **A3**).

    ??? example "프롬프트 A3 — 펼쳐서 복사"
        --8<-- "labs/day4/prompts.md:a3"

3. `workbench/day4/outputs/limits_proposed.xlsx`를 엽니다(엑셀이 없으면 Claude Code에게 "constraints 시트를 표로 보여 줘"). **constraints 시트**에서 `slack`이 0이고 `shadow_price`가 0보다 큰 줄이 **걸린 제약**입니다. 오전 시연 1에서 본 모양 그대로입니다.

<figure markdown="span">
  ![테스트 통과 터미널과 엑셀 constraints 시트의 걸린 제약 두 줄](../assets/screens/d4-limit-tests-excel.png){ width="760" loading=lazy }
  <figcaption>오전 시연 1의 결과 — 테스트 통과 · 두 솔버의 목적함수 차이 · constraints 시트의 걸린 제약 2줄(노란 강조)</figcaption>
</figure>

4. `workbench/day4/experiments.md`를 새로 만들어 **기준 모델**을 적습니다 — 목적함수 · 걸린 제약 이름 · 잠재가격, 그리고 **쉬운 말 한 줄**("총액을 1달러 늘리면 연 기대이익이 약 0.67달러 늘어난다"처럼). 숫자는 `constraints` 시트에서 옮깁니다.
5. 커밋합니다. **커밋 메시지는 두 줄**입니다 — 첫 줄 `4일차: 무엇을 했다`, 한 줄 비우고 `왜: 이유`.

    ```text
    4일차: 바이어별 한도 엔진과 모델 카드 추가

    왜: 정책 문장을 최적화 모델로 옮기고 속성 테스트로 확인하려고
    ```

    소스 제어(++ctrl+shift+g++)에서 `scripts/limits_lp.py` · `workbench/day4/outputs/`의 결과 · `experiments.md`를 골라(`+`) 커밋합니다. 받은 데이터 사본(`workbench/day4/data/`)은 올리지 않아도 됩니다.

!!! example "버그 카드(선택) — 속성 테스트가 잡을까?"
    `data/checkpoints/d4_params_bug.csv`는 정책 숫자 표에서 **한 칸이 틀린 판**입니다. 엔진을 이 파일로 돌려 별도 폴더에 결과를 내고 같은 테스트를 겁니다.

    ```text
    uv run python scripts/limits_lp.py --params data/checkpoints/d4_params_bug.csv --out workbench/day4/outputs/bug
    uv run pytest labs/day4/tests/test_limits_props.py -q --params data/checkpoints/d4_params_bug.csv --result workbench/day4/outputs/bug/limits_proposed.xlsx
    ```

    (`--params` · `--out` 옵션이 아직 없으면 [A4](../prompts/day4.md#a4)의 앞 두 줄로 엔진에 더합니다.) **먼저 예측하세요 — 8개가 통과할까요?** 결과를 보고 ① 어느 숫자가 이상한지(목적함수의 부호와 크기 · 한도 합계) ② 속성 테스트가 왜 못 잡는지(규칙은 지키는 '틀린 답'도 있다) ③ 무엇이 잡는지(14:45의 기대값 테스트 · 목적함수 점검 · 입력 단위 점검)를 고장 보고 4요소로 적어 봅니다. 힌트 하나 — 금리는 소수(0.04047)로 적는 칸입니다.

**13:50 점검** — **속성 테스트 8개 통과**, `experiments.md`에 걸린 제약(총액 · 나이지리아 국가 캡)과 잠재가격이 적혀 있고, 커밋이 **1개** 있으면 됩니다. 10분 쉽니다.

---

## ④ 실험 카드 — worktree로 나란히 (14:00–14:15) {#a-exp}

14:00에 강사가 **worktree 장**을 2분 보여 줍니다. 같은 저장소에 **작업 폴더를 하나 더** 펼쳐, 한 창의 Claude Code가 기준 모델을 다루는 동안 다른 창에서 정책 실험을 해도 서로의 파일을 덮지 않습니다.

1. **카드 1장을 뽑습니다** — `labs/day4/experiment_cards.md`의 9장 가운데 ①–⑤ 하나를 권합니다(⑥–⑨는 더 하기). 짝과 다른 카드를 고르면 17:00 공유가 풍성해집니다.
2. VS Code 소스 제어 보기에서 **저장소 줄**의 `…` → **Worktrees** → **Create Worktree…** → '새 브랜치 만들기'로 브랜치 이름(`d4-exp` 또는 `d4-cap80`) → 폴더 경로는 기본값 그대로 Enter. **저장소 줄이 안 보이면** 소스 제어 제목줄의 `…` 메뉴에서 **Repositories**를 켜거나 F1 → `Git: Create Worktree…`.
3. 만든 뒤 **새 창으로 엽니다** — File › New Window로 새 창을 열고 Open Folder로 그 폴더를 고르거나, 터미널에서 `code -n 경로`. 그 창의 Claude Code로 실험합니다.

<figure markdown="span">
  ![VS Code 소스 제어 — 저장소 줄의 … 단추, Worktrees › Create Worktree… 메뉴, 새 브랜치 이름 d4-cap80 입력](../assets/screens/d4-worktree-create.png){ width="760" loading=lazy }
  <figcaption>worktree 만들기 — ① 저장소 줄의 … 단추 ② Worktrees › Create Worktree… ③ 새 브랜치 이름 입력</figcaption>
</figure>

4. 새 폴더는 **비어 있는 새 체크아웃**입니다 — 가상환경(`.venv`)과 받은 파일이 없으니 새 창 터미널에서:

    ```text
    uv sync
    uv run python tools/get_day_files.py 4
    ```

5. **돌리기 전에 예측**을 `experiments.md`에 적습니다(목적함수가 늘까 줄까 · 걸린 제약이 바뀔까). 그다음 프롬프트 **A4**를 보냅니다 — 엔진에 `--params`(정책 값 파일)와 `--out`(결과 폴더) 옵션을 더하게 하고, **작업 사본**의 숫자를 바꿔 다시 풉니다.

    ??? example "프롬프트 A4 — 펼쳐서 복사"
        --8<-- "labs/day4/prompts.md:a4"

6. 결과를 읽고 `experiments.md`에 **한 줄**로 적습니다(바꾼 것 · 예측 · 목적함수 전 → 후 · 걸린 제약 · 한 줄 해석). 기준 모델의 결과 파일이 **덮이지 않았는지**(`workbench/day4/outputs/limits_proposed.xlsx`의 수정 시각) 봅니다.
7. 실험 결과도 같은 속성 테스트로 봅니다(정책 값은 바뀌었어도 '규칙을 지키는가'는 같습니다):

    ```text
    uv run pytest labs/day4/tests/test_limits_props.py -q --params workbench/day4/data/d4_params.csv --result workbench/day4/outputs/exp/limits_proposed.xlsx
    ```

**잠재가격을 실험으로 확인하는 법** — 카드 ①(총액 70% → 80%)이면 오전에 잠재가격 0.6723으로 어림한 값(총액이 약 30만 달러 늘면 이익이 약 20만 달러)과 실제로 다시 푼 값을 견줍니다. 실제가 어림보다 조금 큰 이유는 **국가 캡도 총액에 비례해 함께 늘기 때문**입니다 — 크게 바꿀 때는 어림이 아니라 다시 풀어 확인합니다.

**14:15 점검** — `experiments.md`에 실험 **한 줄**(예측 + 결과)이 있고, 그 실험을 커밋했는지 봅니다. 새 폴더에서 커밋하면 그 브랜치(`d4-exp`)에 쌓입니다 — 실험이 끝나면 남길 결과만 커밋하고 worktree는 지웁니다(명령 팔레트 `Git: Delete Worktree…`).

---

## ⑤ 스트레스 — 제공 스크립트에 내 시나리오를 더한다 (14:15–14:40) {#a-stress}

오전 시연 2의 시뮬레이터를 **제공 스크립트**로 줄인 단계입니다. 직접 만드는 것은 '더 하기'입니다.

1. 원래 창(기준 폴더 · 브랜치 `d4-limits`)으로 돌아와 스크립트를 그대로 돌립니다.

    ```text
    uv run python labs/day4/stress_mc.py
    ```

    10초쯤 뒤 **시나리오 S0–S4마다 공식 기대손실 · 시뮬레이션 평균 · P95 · P99 · ES99**(상관 ρ = 0과 0.2 두 줄씩)와, 한도안이 있으면 한도 재배정의 **연 기대손실 절감액**이 출력됩니다. `workbench/day4/outputs/stress_results.csv` · `loss_hist.png`가 만들어집니다.
2. 표를 읽습니다 — ① 기대손실은 S0 → S4로 갈수록 커집니다 ② 시뮬레이션 **평균은 공식 기대손실과 ±3% 안**입니다 ③ **P99는 평균보다 훨씬 큽니다**(꼬리) ④ ρ = 0.2면 평균은 그대로인데 P99만 커집니다(오전의 '상관' 장). `loss_hist.png`를 열어 S0 · S3의 분포와 점선(P99)을 봅니다.

<figure markdown="span">
  ![브라우저의 스트레스 리포트 — 시나리오별 공식 기대손실 표와 시나리오 5개의 손실 분포](../assets/screens/d4-stress-report.png){ width="760" loading=lazy }
  <figcaption>오전 시연 2의 결과 화면(웹 리포트) — 오늘 제공 스크립트는 같은 계산을 표 · CSV · 그림 파일로 냅니다</figcaption>
</figure>

3. **내 시나리오 U1**을 더하고 해석합니다(프롬프트 **A5**). `{PD 배수}` · `{LGD}`에 내 가정을 넣습니다 — 예: 바이어국 통화 −30% · 금리 +200bp를 한 묶음으로 보고 PD 배수 2.0 · LGD 0.7. 오전 시연 2의 선택지 가운데 (a)–(e) 하나를 대신 골라도 됩니다.

    ??? example "프롬프트 A5 — 펼쳐서 복사"
        --8<-- "labs/day4/prompts.md:a5"

4. 해석 3줄을 `experiments.md`에 붙여 둡니다. **'가정 시나리오에서의 추정'**이라는 표현이 들어 있는지, 숫자가 `stress_results.csv`에서 온 것인지 확인합니다 — 시나리오는 예측이 아니라 '만약'입니다.
5. 같은 성질을 테스트가 봅니다.

    ```text
    uv run pytest labs/day4/tests/test_stress_props.py -q
    ```

!!! info "절감액은 정의에 따라 숫자가 크게 달라집니다"
    '제안 한도가 현행 한도보다 연 기대손실을 얼마나 줄이나'는 **무엇을 셀지**(외상 거래 바이어만인가 · 신용사건 바이어의 한도를 0으로 줄인 몫을 넣나)에 따라 6천 달러대에서 3만 달러대까지 달라집니다. 제공 스크립트는 외상 거래 바이어만 · 한도 1달러당 기대손실(`elc`) 열을 씁니다. 보고서에는 **정의를 함께 적습니다.**

**14:40 점검** — 기대손실이 S0 < S1 < … < S4 순이고, 시뮬레이션 평균이 공식 기대손실의 ±3% 안이며, 내 시나리오 해석이 3줄 있으면 됩니다.

---

## ⑥ 기대값 테스트 · PR (14:40–14:50) {#a-pr}

14:45에 강사가 **기대값 테스트**를 공개합니다. 속성 테스트가 '어떤 답이든 지킬 규칙'이라면, 기대값 테스트는 **'이 데이터와 이 설계에서 나와야 하는 답'**입니다.

1. 파일 받기 명령을 한 번 더 실행합니다(새로 올라온 파일만 받습니다).

    ```text
    uv run python tools/get_day_files.py 4
    ```

2. 기대값 테스트를 돌립니다.

    ```text
    uv run pytest labs/day4/tests/test_limits_expected.py labs/day4/tests/test_stress_expected.py -q
    ```

    | 확인할 것 | 오전 시연에서 본 숫자 | 어긋나면 |
    |---|---|---|
    | 목적함수(연 기대이익 지표) | 약 **3,135,799**달러(± 0.01%) | 정책 값을 원본에서 읽었나 · 선적 보류 기준(30일) · 총액 반올림 |
    | 걸린 제약 · 잠재가격 | **총액 0.6723 · 나이지리아 국가 캡 1.3959** | 국가 캡 기준(총허용익스포저 × 국가 비율) · 규칙 4 |
    | 한도 합계 | 총액과 같다(**260만** 달러) | 상한 합 × 70%를 10만 달러 단위로 반올림 |
    | '사람 승인 필요' · 증액 곳 수 | 질문 1의 답에 따라 정해진다 | 신용장 · 선수금 바이어를 승인 판정에서 뺐나 |
    | 공식 기대손실 | S0 43,366 · S3 62,121 · S4 107,691달러 | 신용사건 PD 100% · 신용장 LGD · 보상비율 |

    어긋나면 **고치기 전에** [어디서 갈렸나](../prompts/day4.md#mismatch)를 AI에게 묻습니다. 정책 실험 폴더에서 돌리면 일부러 어긋납니다 — 어긋난 폭이 실험 결과입니다.
3. 프롬프트 **A6**으로 PR 제목과 본문 3줄을 씁니다.

    ??? example "프롬프트 A6 — 펼쳐서 복사"
        --8<-- "labs/day4/prompts.md:a6"

4. **push**하고 PR을 **만듭니다** — 소스 제어의 **Publish Branch**(또는 `git push -u origin d4-limits`) → GitHub의 **Compare & pull request**. 허락 창에서 **push 대상이 `d4-limits`**인지 읽고 승인합니다. **PR 병합(merge)은 오늘 하지 않습니다**(워크플로 PR만 실습 B에서 병합).

**14:50 점검** — 기대값 테스트 결과(통과 또는 어긋난 이유 한 줄)가 `experiments.md`에 있고, **PR 링크**가 있으면 실습 A 완료입니다.

### 실습 A 완료 기준 {#checkpoint}

- [ ] `scripts/limits_lp.py` · `workbench/day4/outputs/limits_proposed.xlsx`(limits · constraints · summary) · `model_card.md`가 있다
- [ ] 속성 테스트 8개가 통과하고, 규정과 다르게 정한 곳이 `model_card.md`에 있다
- [ ] `experiments.md`에 기준 모델(걸린 제약 · 잠재가격)과 실험 카드 1줄(예측 + 결과 + 해석)이 있다
- [ ] `stress_results.csv` · `loss_hist.png`와 내 시나리오의 해석 3줄이 있다('가정 시나리오에서의 추정')
- [ ] 기대값 테스트를 돌렸다(어긋나면 이유 한 줄) · 커밋 메시지에 `왜:` 줄 · `d4-limits` push · PR 링크

---

## 더 하기 — 빨리 끝난 분 {#extend}

하나만 골라도 됩니다.

| 더 하기 | 하는 일 | 확인 |
|---|---|---|
| **시뮬레이터를 직접** | 오전 시연 2의 [프롬프트](../prompts/day4.md#demo-2)로 `scripts/stress_mc.py`를 직접 만들고 제공 스크립트와 숫자를 대조한다 | 평균이 제공 스크립트와 ±3% 안(난수 방식이 다르면 P99는 ±3% 안팎) |
| **두 번째 카드 ⑧ · ⑨** | 회수 시간 배분(0·1 변수 MIP) 또는 조기결제 할인율 고르기를 새 모델로 세운다 | 카드의 가정이 코드에 그대로 들어갔나 · 시간(또는 매입 한도)이 줄면 어떻게 달라지나 |
| **규정 문서까지** | 오전 시연 1의 [프롬프트 전체판](../prompts/day4.md#demo-1)으로 규정 문서와 설계를 함께 읽혀 질문이 어떻게 달라지는지 본다 | 같은 설계라도 질문이 다르게 나오는 것을 기록 |
| **버그 카드** | 위 ③의 버그 카드를 기대값 테스트까지 걸어 무엇이 잡는지 표로 | 속성 8개 대 기대값 5개 |

---

## 채팅 경로 — Claude Code를 못 쓸 때 {#chat-path}

Claude Code 계정이 없거나(무료 플랜은 쓸 수 없습니다) 확장이 로그인되지 않으면 **ChatGPT 또는 Claude 웹**에 파일을 올려 **같은 문장**으로 합니다. 오늘 파일은 합성 데이터라 올려도 됩니다. 프롬프트는 [A1–A6](../prompts/day4.md#chat-path)와 같고 경로 · 저장 줄만 바꿉니다.

1. 웹 채팅에 `d4_start_scored.csv` · `d4_params.csv` · `d4_open_inv.csv`를 **첨부**하고 `MODEL_SPEC.md` 내용은 본문에 붙여 넣습니다. A1의 `@파일`과 경로는 지우고 **"SciPy linprog(HiGHS)로 풀어 xlsx로 내려 줘"**를 덧붙입니다. ChatGPT는 **데이터 분석** 기능이, Claude는 **코드 실행** 기능이 켜져 있어야 계산합니다. 무료 계정은 하루 업로드가 3개라 올릴 파일을 고릅니다.
2. 표와 질문 3개가 오면 위 [답안 카드](#a-model)로 답합니다. 받은 `limits_proposed.xlsx`의 **목적함수가 오전 시연의 약 3,135,799달러인지**, 걸린 제약이 총액과 나이지리아 국가 캡인지 **손으로 대조**합니다(테스트 파일을 돌릴 수 없으니 이것이 검증입니다).
3. 스트레스는 `labs/day4/stress_mc.py`와 `d4_start_scored.csv` · `d4_scenarios.csv`를 올려 **"이 스크립트를 그대로 실행해 표와 히스토그램을 보여 줘"**. 내 시나리오 U1은 "scenarios 파일에 U1 한 줄을 더해 다시 실행해 줘".
4. 엑셀이 편하면 `data/checkpoints/d4_limit_model.xlsx`의 **해 찾기**(단순 LP)로도 같은 답을 구할 수 있습니다.
5. 결과 파일을 내 PC에서 같은 이름으로 `workbench/day4/outputs/`에 두고, **GitHub 웹에서 올립니다.**
    1. 내 저장소 화면의 브랜치 선택(`main ▾`)에 `d4-limits`를 입력하고 **Create branch**를 누릅니다.
    2. `workbench/day4/outputs/` 폴더로 들어가 **Add file → Upload files**로 결과 파일을 끌어다 놓고, 커밋 메시지 첫 줄과 설명 칸(`왜:`)을 쓴 뒤 **Commit directly to the `d4-limits` branch**를 고르고 **Commit changes**.
    3. **Pull requests → New pull request**로 PR을 만듭니다.

!!! warning "GitHub 웹의 Upload files는 .gitignore를 보지 않습니다"
    고른 파일을 그대로 올립니다. 올리기 전에 파일 이름과 내용을 한 번 봅니다 — 회사 실데이터 · 키 · 실명은 올리지 않습니다.

---

## 막힐 때 {#troubleshooting}

| 증상 | 이렇게 해 보세요 |
|---|---|
| `get_day_files.py`가 "공개 전"이라고 한다 | 08:30 이후 같은 명령을 다시 실행합니다. 계속 안 되면 [4일차 → 파일 받기](index.md#files) |
| `uv sync`가 실패한다(프록시 · 사내 망) | 손을 듭니다. Codespaces나 채팅 경로로 바꿀 수 있습니다 |
| Plan 모드 질문에 답하지 않고 승인해 버렸다 | 괜찮습니다. 모델 카드에 AI가 고른 가정이 적혀 있으니 읽고, 규정과 다르면 "이 가정은 답안 카드의 N번대로 바꿔 줘"라고 다시 시킵니다 |
| 계획 승인 창에서 `use auto mode`를 눌러 파일 변경이 묻지 않고 진행됐다 | 괜찮습니다. 다음부터 `2 Yes, and manually approve edits`를 고르거나 모드를 Manual로 바꿉니다. 만들어진 파일은 소스 제어의 diff로 읽어 봅니다 |
| '선형이 아니다'(non-linear) 오류 | 결정변수 식에 `IF` · `MIN` · `MAX`를 썼습니다. 상한 · 하한 · 계수는 열로 **미리 계산**하고 식에는 곱과 합만 두라고 다시 지시합니다 |
| 국가 캡이 안 맞다 | 기준은 **총허용익스포저 × 국가 비율**입니다(바이어 상한의 합이 아닙니다). 총액이 10만 달러 단위로 반올림됐는지도 봅니다 |
| 금리 단위(4.047 대 0.04047) | 정책 숫자 표의 값은 소수입니다(`TSOFR3M` 0.04047). 입력 단위를 점검하고 "금리 칸의 값은 소수"라고 한 줄 덧붙입니다 |
| `pulp`에서 `LpVariable` · 솔버 호출 오류 | AI가 PuLP 4.0 문법을 섞어 썼습니다. 이 저장소는 **3.3.2로 고정**입니다 — 오류 전문을 그대로 다시 주고 "PuLP 3.3.2 문법으로"라고 합니다 |
| 속성 테스트가 실패한다 | 실패한 테스트 이름이 가리키는 성질 하나만 봅니다. [A3](../prompts/day4.md#a3)의 고장 보고 4요소로 정리한 뒤 어느 쪽(코드 · 테스트 · 설계)이 틀렸는지부터 묻습니다 |
| 두 솔버의 바이어별 한도가 다르다 | 정상입니다. 계수가 같은 바이어끼리 나누는 방식이 솔버마다 다릅니다 — 목적함수 · 걸린 제약 · 잠재가격으로 비교합니다 |
| 실험 폴더에서 `data/checkpoints/…` 파일이 없다 | 새 폴더(worktree)는 받은 파일이 없습니다. `uv sync` → `uv run python tools/get_day_files.py 4`를 다시 실행합니다 |
| 실험 결과가 기준 결과를 덮어썼다 | `--out workbench/day4/outputs/exp`를 빠뜨렸습니다. 기준 모델을 다시 돌려 되돌리고 A4를 다시 보냅니다 |
| 그래프의 한글이 □로 나온다 | `CLAUDE.md`의 글꼴 `tools/fonts/NanumGothic-Regular.ttf`를 쓰라고 다시 지시합니다 |
| 숫자를 AI가 '암산'한 것 같다 | "숫자는 코드로 계산한 값만 쓰고 모르면 '확인 필요'라고 써"를 다시 지시하고, 계산한 코드를 보여 달라고 합니다 |
| 허락 창이 계속 뜬다 | 읽고 `1 Yes`를 누릅니다. 모르는 명령이면 `No` 하고 "이 명령이 뭐 하는 거야?"라고 묻습니다. `2 … for this project`는 쓰지 않습니다 |
| push가 거부된다 · 로그인을 묻는다 | VS Code 왼쪽 아래 **계정 아이콘**에서 GitHub에 로그인합니다. `GH007 … private email` 오류면 `git config --global user.email`을 noreply 주소로 바꾸고 다시 커밋합니다 |
