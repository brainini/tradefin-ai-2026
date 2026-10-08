# 실습 B · 6–7교시 — 경보 자동화와 경영진 리포트

!!! abstract "한눈에 보기 — 실습 B"
    | 항목 | 내용 |
    |---|---|
    | 목표 | **내 규칙을 더한 조기경보를 GitHub Actions로 자동 실행하고, 같은 숫자를 독자에 맞는 보고 형식으로 만든다** — 경보 엔진과 워크플로, 자동 이슈, 숫자 대조와 레드팀을 거친 보고 파일 하나 |
    | 시간 | **15:00–16:50**(110분) · 쉬는 시간 15:50–16:00 |
    | 오전 시연을 이렇게 따라 한다 | 시연 4(조기경보를 평일 아침 9시에)를 **줄인다** — 수동 버튼 실행이 기본이고 예약은 더 하기, 웹훅은 생략하고, **내 규칙 1개를 더하는 변형**을 한다. 시연 5(경영진 리포트)는 입력 JSON · 렌더 · 숫자 대조 스크립트를 15:00에 제공해 **해석 프롬프트 · 레드팀 · 판단**에 시간을 쓰고, 읽는 사람에 따라 모양을 바꾸는 **독자 카드**로 변형한다. 시연 3(의심 메일 판독)은 더 하기 |
    | 입력 | `labs/day4/alert_rules.yml`(경보 규칙) · `data/checkpoints/d4_open_inv.csv` · `d4_start_scored.csv`(→ 작업 사본 `workbench/day4/data/`) · 15:00 공개 `d4_report_input.json` · `labs/day4/report_template.docx` · `report_schema.json` |
    | 도구 | VS Code · **Claude Code**(Plan) · GitHub **Actions** · Issues · pytest · Claude · ChatGPT |
    | 산출물 | `scripts/ews.py` · `.github/workflows/d4-ews.yml` · `scripts/post_issue.py` · 자동 이슈 · 보고 파일 · `number_trace.csv` · `redteam.md` / **PR 2개** |
    | 프롬프트 | [B1](../prompts/day4.md#b1) · [B2](../prompts/day4.md#b2) · [B3](../prompts/day4.md#b3) · [B4](../prompts/day4.md#b4) · [B5](../prompts/day4.md#b5) · [B6](../prompts/day4.md#b6) |

이 실습의 목표는 AI가 YAML을 잘 쓰는지 보는 것이 아닙니다. **무엇을 경보로 볼지(규칙) · 누가 확인하나(권고와 승인) · 보고서의 숫자를 어떻게 믿나(대조와 레드팀)를 내가 정하고**, 자동으로 도는 장치와 AI의 초안을 **내가 의심해 보는 것**입니다. 강사가 돌아다니며 한 분씩 2–3분 확인합니다. 막히면 손을 들거나 노트북 위에 빨간 표시(스티커)를 올리세요.

!!! tip "실습 A를 끝내지 못했어도 괜찮습니다"
    경보 엔진은 실습 A의 결과를 쓰지 않습니다. 오늘 입력은 `d4_open_inv.csv` · `d4_start_scored.csv`뿐이고, 보고서의 숫자는 15:00에 올라오는 지표 JSON이 대 줍니다.

## 슬라이드의 단계 {#slide-steps}

슬라이드 두 장(실습 B · B 시작 프롬프트)과 같은 순서입니다. 아래 ①–⑤가 이 단계를 풀어 쓴 것입니다.

!!! abstract "실습 B · 경보 자동화와 경영진 리포트 (15:00–16:50)"
    1. **규칙 · 엔진** — 내 규칙 1개 → `ews.py` → 테스트 (20분)
    2. **자동 실행** — 워크플로 PR → Run workflow → 이슈 (25분)
    3. **독자 카드 1장** — 제공 JSON · 렌더 스크립트로 (20분)
    4. **레드팀** — 다른 AI 한 번 → 맞는 지적만 반영 (15분)
    5. **기록** — 커밋 → PR, 본문 3줄 (10분)

    산출: 실행 · 이슈 링크 · 보고 파일 · 대조표 · 레드팀 표 · PR

## 시간표와 점검 시각 {#time}

| 시각 | 단계 | 하는 일 | 점검 |
|---|---|---|---|
| 15:00–15:20 | [① 규칙 · 엔진](#b-engine) | 브랜치 `d4-ews` · **파일 받기 다시** · 규칙 복사 + 내 규칙 1개 · B1(Plan) → `ews.py` → 테스트 | **15:20** 테스트 통과 · D+30 21건 · 선적 보류 19곳 · 통지 임박 9 · 경과 14 |
| 15:20–15:45 | [② 자동 실행](#b-auto) | 워크플로 · 이슈 스크립트 읽기 → 실행에 필요한 파일 전부 담은 PR → **병합(내가 직접)** → Run workflow → 로그 → 이슈 → 한 번 더 | **15:45** 녹색 체크 · 이슈 1건(댓글 1개) |
| 15:45–15:50 | 따라잡기 | 늦은 사람은 ②를 마치고, 끝난 사람은 독자 카드를 미리 고른다 | |
| 15:50–16:00 | 쉬는 시간 | | |
| 16:00–16:20 | [③ 독자 카드](#b-card) | 파일 받기 다시(15:00 공개분 확인) → 카드 1장: 해석(B2) → 렌더 · 표 · 메일 | **16:20** 렌더된 파일 1개 |
| 16:20–16:35 | [④ 레드팀](#b-redteam) | 숫자 대조 불일치 0 → 다른 AI에 레드팀(B4) → 맞는 지적만 반영 → 체크리스트 12항목 | **16:35** 불일치 0 · 레드팀 반영 1건 이상 |
| 16:35–16:45 | [⑤ 기록](#b-record) | 커밋 → PR(본문 3줄 — B6) | **16:45** PR 링크 |
| 16:45–16:50 | [더 하기](#extend) | 지표 JSON을 내 결과로 · 태그 · 예약 줄 · 의심 메일 판독 · 짝 PR 리뷰 | |

!!! tip "늦었다면"
    15:20에 아직 ① 중이어도 괜찮습니다. ②의 워크플로 PR만 15:45까지 열어 병합하면 이슈까지 따라올 수 있습니다 — 막히면 10분 안에 손을 들고, [채팅 경로](#chat-path)는 참고 엔진 `ews_example.py`를 씁니다. ③ 독자 카드는 **카드 ③(메일 5줄)**이 가장 빨리 끝납니다.

## 입력 파일 {#files}

`uv run python tools/get_day_files.py 4`가 받아 줍니다. 15:00에 올라오는 파일이 있으니 **실습 B를 시작하면서 한 번 더** 실행합니다.

| 파일 | 위치 | 쓰는 곳 |
|---|---|---|
| 경보 규칙 | `labs/day4/alert_rules.yml` — 연체 단계 · 규칙 7개 · 내 규칙 아이디어 3개(주석) | ① |
| 미결 인보이스 | `data/checkpoints/d4_open_inv.csv`(300건) → 사본 `workbench/day4/data/` | ① ② |
| 바이어 점수 | `data/checkpoints/d4_start_scored.csv`(150곳) → 사본 | ① ② |
| 경보 속성 테스트 | `labs/day4/tests/test_ews_props.py` — **15:00 공개**, 엔진이 지켜야 할 모양이 첫머리에 있다 | ① |
| 참고 엔진 · 이슈 스크립트 · 워크플로 예시 | `labs/day4/ews_example.py`(15:00) · `post_issue_example.py` · `ews_workflow_example.yml` — 대체 경로용 | 채팅 경로 · 막힐 때 |
| 지표 JSON | `data/checkpoints/d4_report_input.json` — **15:00 공개** · 사본 `workbench/day4/data/` | ③ |
| 보고서 양식 | `labs/day4/report_template.docx`(docxtpl) · `report_schema.json`(해석 JSON의 칸 이름) | ③ |
| 렌더 · 숫자 대조 | `labs/day4/make_report.py` · `check_numbers.py` — **15:00 공개** | ③ ④ |
| 독자 카드 · 체크리스트 | `labs/day4/audience_cards.md` · `review_checklist.md` | ③ ④ |
| 메일 예제(더 하기) | `labs/day4/mail/*.eml` 5통 · `buyer_contacts.csv` · `fraud_signals.md` | 더 하기 |

!!! warning "러너는 커밋된 파일만 봅니다"
    GitHub Actions의 러너는 **빈 컴퓨터**입니다. `data/checkpoints/`의 원본은 `.gitignore`로 빠져 GitHub에 올라가지 않으니, 경보 엔진은 **작업 사본 `workbench/day4/data/`를 읽고 그 사본을 커밋**합니다. 규칙 파일 · 엔진 · 이슈 스크립트 · 워크플로도 모두 main에 있어야 합니다.

---

## ① 규칙과 엔진 (15:00–15:20) {#b-engine}

1. 내 PC를 `main`으로 맞추고 **브랜치 `d4-ews`**를 만듭니다(실습 B는 실습 A의 PR과 따로 갑니다).

    ```text
    git switch main
    git pull
    git switch -c d4-ews
    uv run python tools/get_day_files.py 4
    ```

    `[받음] labs/day4/tests/test_ews_props.py` · `data/checkpoints/d4_report_input.json` 같은 줄이 새로 보이면 15:00 공개분이 들어온 것입니다.
2. **규칙 파일을 복사**하고 **내 규칙 1개를 더합니다.** 원본(`labs/`)은 그대로 두고 내 서랍으로 복사합니다.

    ```text
    cp labs/day4/alert_rules.yml workbench/day4/rules/alert_rules.yml
    ```

    VS Code에서 `workbench/day4/rules/alert_rules.yml`을 열고 `rules:` 맨 아래에 규칙을 하나 더합니다. 파일 안 주석에 아이디어 셋이 있습니다 — 주석(`#`)을 풀거나 내 업무에 맞게 새로 씁니다. **2026-09-30 원장의 기대 건수**:

    | 내 규칙 | 조건(`when`) | 기대 건수 |
    |---|---|---|
    | 통지 기한 7일 이내 | `ksure_insured == 'Y' and dpd > 0 and 0 <= notice_days_left <= 7` | **7건**(바이어 6곳) |
    | 180일 넘은 미결 | `dpd > 180` | **7건**(바이어 4곳) |
    | 한도 사용률 80% 이상(신용장 · 선수금 제외) | `scope: buyer` · `current_limit_usd > 0 and open_ar_usd >= 0.8 * current_limit_usd and payment_method not in [...]` | **44곳**(100% 이상이면 30곳) |
    | 사기 · 결제조건 변경 | 기존 규칙 `R-FRAUD-ACCOUNT` · `R-TERMS-CHANGE` | 오늘 원장은 **0건**이 정상(메일이 와야 울린다) |

    규칙 id와 등급(`tier`)과 권고 문장(`action`)을 함께 씁니다. 경계값(`>=` · `>`)을 정하는 것이 곧 내 판단입니다. `labs/day4/fraud_signals.md`의 사기 신호 13가지에서 골라도 됩니다.
3. 입력창 아래 모드 표시기를 **Plan**으로 바꾸고 프롬프트 **B1**을 보냅니다.

    ??? example "프롬프트 B1 — 펼쳐서 복사"
        --8<-- "labs/day4/prompts.md:b1"

4. 계획을 읽습니다 — 엔진이 읽을 파일(작업 사본) · 출력 4종 · 중복 키(인보이스 + 규칙 + 기준일) · 만들 파일 이름(`scripts/ews.py` · `.github/workflows/d4-ews.yml` · `scripts/post_issue.py`). 계획 승인 창에서 **`2 Yes, and manually approve edits`**를 고릅니다. 허락 창은 **무엇을 · 어디에**를 읽고 `1 Yes`합니다.
5. Claude가 엔진과 테스트를 마칠 때까지 기다리며(한 번 더 읽어도 좋습니다) 프롬프트의 1)·2)가 끝났는지 봅니다. 터미널에서 직접 확인합니다.

    ```text
    uv run python scripts/ews.py
    uv run pytest labs/day4/tests/test_ews_props.py -q --rules workbench/day4/rules/alert_rules.yml
    ```

    엔진 콘솔에 단계별 건수 · 선적 보류 곳 수 · 통지 임박 · 경과 건수가 한 줄씩 나옵니다. 같은 기준일로 **두 번 돌려도 `alerts.csv`가 같은지**(멱등) 한 번 더 돌려 `git diff`나 파일 크기로 봅니다.

<figure markdown="span">
  ![VS Code 좌우 분할 — 경보 규칙 파일 alert_rules.yml과 워크플로 파일 d4-ews.yml](../assets/screens/d4-ews-input.png){ width="760" loading=lazy }
  <figcaption>오전 시연 4의 입력 — 규칙 파일(왼쪽)과 워크플로 파일(오른쪽). 오늘은 규칙에 내 한 줄을 더합니다</figcaption>
</figure>

**15:20 점검** — 테스트가 통과하고, 엔진 콘솔이 **D+30 21건(USD 233,455) · 선적 보류 19곳 · 통지 임박 9건 · 경과 14건**이며(기본 규칙 기준), 내 규칙의 건수가 위 표와 맞는지 봅니다. 내 규칙이 선적 보류 목록을 바꾸는 규칙이 아니라면 이 네 숫자는 그대로입니다.

---

## ② 자동 실행 — 워크플로 PR → Run workflow → 이슈 (15:20–15:45) {#b-auto}

1. **워크플로를 읽습니다.** B1의 3)·4)가 만든 `.github/workflows/d4-ews.yml`을 열고 **네 곳을 내 눈으로** 읽습니다.
    - `on:` — 수동 버튼 `workflow_dispatch`만 있다(예약 `schedule` 줄은 없다 — 더 하기)
    - `permissions:` — `contents: read` · `issues: write`만 있다
    - `runs-on:` — `ubuntu-24.04`처럼 판 번호가 적혀 있다
    - `uses:` 뒤 — `@v7` 같은 **판 번호가 고정**돼 있다
2. **실행에 필요한 파일을 모두 한 브랜치에** 담습니다 — 하나라도 빠지면 러너가 `can't open file`(파일 없음)로 멈춥니다.

    | 담을 파일 | 왜 |
    |---|---|
    | `workbench/day4/rules/alert_rules.yml` | 내 규칙(규칙 사본) |
    | `scripts/ews.py` | 경보 엔진 |
    | `scripts/post_issue.py` | 이슈 만들기 · 댓글 달기 |
    | `.github/workflows/d4-ews.yml` | 워크플로 |
    | `workbench/day4/data/d4_open_inv.csv` · `d4_start_scored.csv` | **데이터 사본** — 원본은 `.gitignore`라 러너에 없다 |

    `git status`로 위 파일이 모두 보이는지 확인하고 소스 제어에서 골라 커밋합니다. **커밋 메시지는 두 줄**입니다(Claude Code가 제안하면 `4일차: …` / 빈 줄 / `왜: …`인지 확인).

    ```text
    4일차: 조기경보 엔진과 수동 실행 워크플로 추가

    왜: 내 규칙을 러너가 매번 같은 방식으로 돌리게 하려고
    ```

3. push하고 **PR**을 만듭니다(`d4-ews` → `main`). 허락 창에서 push 대상이 `d4-ews`인지 읽고 승인합니다. 그다음 GitHub의 PR 화면에서 **Merge pull request**를 **내가 직접** 누릅니다 — 워크플로 파일이 main에 있어야 `Run workflow` 버튼이 생기고, 러너는 main의 파일로 돕니다. (워크플로 파일이 이미 main에 있다면 `Run workflow`의 **Use workflow from**에서 작업 브랜치를 골라 병합 전에 돌려 볼 수도 있습니다.)
4. 내 PC도 `main`을 받아 둡니다(`git switch main` · `git pull`).
5. GitHub의 **Actions** 탭 → 왼쪽 **d4-ews** → 오른쪽 **Run workflow**(브랜치 `main`) → 녹색 **Run workflow** 단추. 실행이 목록에 생기면 열어 **`ews` 잡**의 스텝을 펼쳐 봅니다 — 보통 20–60초입니다. 엔진 스텝 로그의 끝에 `이슈 만들기: …/issues/번호`가 찍힙니다.

    <figure markdown="span">
      ![GitHub Actions 실행 목록을 이벤트로 거른 화면(수동 실행 예시) — 실행마다 시작 시각과 소요 시간](../assets/screens/d4-actions-run-list.png){ width="760" loading=lazy }
      <figcaption>Actions 실행 목록 — 이벤트로 거른 화면의 예시입니다(수동 실행은 workflow_dispatch로 보입니다)</figcaption>
    </figure>

6. **Issues** 탭에서 `[조기경보] 2026-09-30 기준` 이슈를 엽니다. 작성자가 `github-actions`(봇)이고 본문에 등급별 건수 표 · 연체 단계 · **선적 보류 목록** · 통지 임박 · 경과 건수가 있으며 모든 조치가 **'권고(사람 승인 전)'**입니다.
7. **한 번 더 Run workflow**를 누릅니다. 이슈는 **그대로 1건**이고 **댓글만** 하나 늘어납니다 — 같은 제목의 열린 이슈가 있으면 댓글로 갱신하는 **멱등성**입니다.

<figure markdown="span">
  ![자동 생성된 조기경보 이슈 — 건수 표 · 선적 보류 목록 · 두 번째 실행의 댓글, 녹색 체크와 아티팩트](../assets/screens/d4-ews-issue.png){ width="760" loading=lazy }
  <figcaption>오전 시연 4의 결과 예시(연습 데이터) — 다시 실행해도 이슈는 하나, 댓글만 늡니다. 실행 요약 아래 아티팩트 <code>alerts</code>에 결과 파일 4종이 보관됩니다</figcaption>
</figure>

!!! info "숫자가 오전 화면과 조금 다를 수 있습니다"
    오전 시연의 캡처는 연습 데이터로 만든 '결과 예시'입니다. 내 이슈의 숫자는 오늘 원장(`d4_open_inv.csv`)으로 돌린 값이라 **D+30 21건 · 선적 보류 19곳 · 통지 임박 9건 · 경과 14건**이 나와야 합니다(내 규칙은 그 아래 줄에 더해집니다).

**15:45 점검** — 실행에 **녹색 체크**가 있고, 이슈가 **1건**이며 댓글이 1개(다시 실행한 것)입니다. 실패(빨간 X)라면 [막힐 때](#troubleshooting)의 로그 읽기부터 — 오류 메시지는 **맨 아래 줄부터** 읽습니다.

---

## ③ 독자 카드 — 같은 숫자, 읽는 사람에 맞게 (16:00–16:20) {#b-card}

보고서의 숫자는 코드가 만든 **지표 JSON**이고, 문장과 모양만 독자에 맞춰 바뀝니다. **카드 1장**을 고릅니다(자세한 설명은 `labs/day4/audience_cards.md`).

| 카드 | 독자 | 만드는 것 | 가장 빠른 길 |
|---|---|---|---|
| ① 경영진 Word 2쪽 | 대표 · 임원 | 요약 3줄 · 표 · 결정 요청 · 가정과 한계 | B2 → `make_report.py` |
| ② 영업팀 바이어별 조치표 | 영업 담당 | 바이어 · 단계 · 조치 · 담당 · 기한 · 등급, 조건부 서식 | B3 카드 ② → `action_table.xlsx` |
| ③ 대표 보고 메일 5줄 | 대표(모바일) | 결론 · 위험 숫자 · 한 일 · 결정 요청 · 다음 확인 | B3 카드 ③ → 텍스트 |

1. 15:00에 올라온 파일이 있는지 `uv run python tools/get_day_files.py 4`로 한 번 더 확인합니다. 지표 JSON(`workbench/day4/data/d4_report_input.json`)을 엽니다 — 첫 단계 키 아홉 개(`as_of` · `portfolio` · `limits` · `scenarios` · `alerts` · `top5` · `savings` · `basis` · `approvers`)와 승인 주체(`approvers`)가 있습니다. **AI가 승인 주체를 지어내지 않고 입력에서 가져오게** 하려는 칸입니다.

<figure markdown="span">
  ![왼쪽 report_input.json 1단계 키, 오른쪽 중괄호 자리표시자가 보이는 Word 템플릿 1쪽](../assets/screens/d4-report-input.png){ width="760" loading=lazy }
  <figcaption>오전 시연 5의 입력 — 지표 JSON과 자리표시자 템플릿(왼쪽 숫자 · 오른쪽 모양)</figcaption>
</figure>

2. **카드 ① 경영진 Word** — 새 대화(Claude 또는 ChatGPT)에 프롬프트 **B2**와 지표 JSON 전문을 붙여 JSON 하나를 받아 `workbench/day4/outputs/narrative.json`으로 저장합니다(코드 블록 표시 ```는 빼고 `{`로 시작하게). 그다음:

    ??? example "프롬프트 B2 — 펼쳐서 복사"
        --8<-- "labs/day4/prompts.md:b2"

    ```text
    uv add docxtpl
    uv run python labs/day4/make_report.py
    ```

    `docxtpl`을 처음 쓰면 `uv add docxtpl`이 필요합니다(Claude Code가 하겠다고 알려 주면 읽고 승인). 렌더 스크립트는 채우기 전에 **핵심 숫자를 원본에서 다시 계산**해 지표 JSON과 맞는지 보고, 다르면 멈춥니다. 통과하면 `workbench/day4/outputs/credit_report_2026-09.docx`가 나옵니다 — Word로 열어 요약 3줄 · 결정 요청 표의 **승인 주체** · 상태 '권고(사람 승인 전)' · 머리글 'AI 작성 초안 — 담당자 검토 후 확정'을 봅니다.

    <figure markdown="span">
      ![완성된 보고서 1쪽(요약 3줄 · 결정 요청 표의 승인 주체)과 레드팀 지적에 대한 사람의 판단 표](../assets/screens/d4-report-output.png){ width="760" loading=lazy }
      <figcaption>오전 시연 5의 결과 예시 — 결정 요청마다 승인 주체가 있고, 다른 AI의 지적은 사람이 반영 · 기각을 가렸습니다</figcaption>
    </figure>

3. **카드 ② 영업팀 조치표** — Claude Code에 **B3 카드 ②**를 보냅니다(① 규칙 · 엔진의 결과 `alerts.csv`가 입력입니다).

    ??? example "프롬프트 B3 · 카드 ② — 펼쳐서 복사"
        --8<-- "labs/day4/prompts.md:b3-card2"

4. **카드 ③ 대표 보고 메일 5줄** — 새 대화에 **B3 카드 ③**과 지표 JSON을 붙입니다. 결과 5줄을 `workbench/day4/outputs/ceo_mail.txt`로 저장합니다.

    ??? example "프롬프트 B3 · 카드 ③ — 펼쳐서 복사"
        --8<-- "labs/day4/prompts.md:b3-card3"

**16:20 점검** — 카드로 만든 **파일이 1개** 있습니다(docx · xlsx · txt). 숫자가 어디서 왔는지 손가락으로 짚을 수 있어야 합니다.

---

## ④ 레드팀 — 다른 AI로 허점을 찾고, 맞는 지적만 반영 (16:20–16:35) {#b-redteam}

같은 AI는 자기 글에 관대합니다. **초안을 쓴 AI와 다른 서비스**(Claude로 썼으면 ChatGPT, 반대도 마찬가지)에 허점을 찾게 합니다.

1. **숫자 대조부터** — 카드 ①이면:

    ```text
    uv run python labs/day4/check_numbers.py
    ```

    문장 속 숫자를 정규식으로 뽑아 지표 JSON과 대조하고 `number_trace.csv`로 남깁니다. **불일치가 0이어야** 다음으로 갑니다. 불일치가 나오면 표에서 `where`(어느 문장) · `number` · `json_path` · `status`를 읽습니다 — **단위 다름**(예: '선적 보류 21곳'은 D+30 연체 21건이지 바이어 수가 아닙니다)처럼 값만 비교하면 통과해 버리는 오류를 이 표가 잡습니다. 카드 ② ③은 숫자를 손으로 한 줄씩 지표 JSON과 대조합니다.
2. **다른 AI에 레드팀** — 새 대화에 프롬프트 **B4**와 초안 · 지표 JSON을 붙입니다.

    ??? example "프롬프트 B4 — 펼쳐서 복사"
        --8<-- "labs/day4/prompts.md:b4"

3. 지적을 하나씩 **입력과 규칙을 열어 보고** 반영 / 기각을 가릅니다. 맞는 지적만 반영하고, 틀린 지적은 이유를 적어 기각합니다 — 오전 시연에서는 5건 가운데 2건이 반영되고 3건이 기각됐습니다(기각 3건 중 2건은 레드팀이 작성 규칙을 보지 못하고 입력만 보고 낸 지적). 결과를 `workbench/day4/outputs/redteam.md`에 한 줄씩 적습니다. 반영했다면 `narrative.json`을 고치고 렌더와 대조를 다시 돌립니다.
4. **체크리스트 12항목**(`labs/day4/review_checklist.md`)을 하나씩 확인합니다 — 숫자 · 가정 · '권고(사람 승인 전)' · 개인정보 · 레드팀 처리 · 초안 표시. 보고서 끝(또는 PR 본문)에 붙여 둡니다. **확정과 서명은 사람이 합니다.**

**16:35 점검** — 숫자 대조 **불일치 0**, 레드팀 반영 **1건 이상**(지적이 없었다면 '지적 없음'과 대조한 숫자 3개 — 이것도 다른 AI에게 한 번 더 확인합니다)입니다.

---

## ⑤ 기록 — 커밋 · PR (16:35–16:45) {#b-record}

1. 만든 것을 커밋합니다 — 독자 카드 파일 · `number_trace.csv` · `redteam.md` · 체크리스트 · (카드 ①이면) `narrative.json`과 지표 JSON 사본. **커밋 메시지는 두 줄**입니다.

    ```text
    4일차: 경영진 보고서 초안과 숫자 대조 · 레드팀 기록 추가

    왜: AI 초안을 코드 대조와 다른 AI 검토를 거쳐 사람이 확정하는 흐름을 남기려고
    ```

2. 브랜치(예: `d4-report`)를 push하고 PR을 만듭니다. 본문은 **프롬프트 B6**으로 3줄 — ① 무엇을 했다 ② 결과(실행 링크 · 이슈 링크 · 불일치 0 · 레드팀 반영 몇 건) ③ 남은 질문.

    ??? example "프롬프트 B6 — 펼쳐서 복사"
        --8<-- "labs/day4/prompts.md:b6"

3. 짝의 PR에 코멘트 하나를 남깁니다 — 바뀐 파일 · 커밋 메시지의 '왜' · 실데이터가 없는지 · 키가 없는지 · 한 줄.

**16:45 점검** — **PR 링크**가 있으면 됩니다. 병합은 오늘 하지 않아도 됩니다(워크플로 PR은 ②에서 병합했습니다).

### 실습 B 완료 기준 {#checkpoint}

- [ ] `workbench/day4/rules/alert_rules.yml`에 **내 규칙이 하나 더** 있고, `scripts/ews.py`가 경보 속성 테스트를 통과한다
- [ ] 워크플로 PR이 main에 병합됐고, Actions 실행에 **녹색 체크**가 있다
- [ ] 자동 이슈가 **1건**이고, 다시 실행해도 1건이다(댓글만 는다) · 모든 조치가 '권고(사람 승인 전)'
- [ ] 독자 카드 한 장의 **파일**이 있고, 숫자 대조(카드 ①은 `number_trace.csv` 불일치 0)를 했다
- [ ] 다른 AI의 레드팀 지적을 사람이 반영 / 기각으로 가려 `redteam.md`에 적었다 · 체크리스트 12항목을 확인했다
- [ ] 커밋 메시지에 `왜:` 줄 · 브랜치 push · **PR 링크**(예약 줄을 더했다면 수업 뒤 Disable workflow)

---

## 더 하기 — 빨리 끝난 분 (16:45–16:50 · 남는 시간) {#extend}

하나만 골라도 됩니다.

| 더 하기 | 하는 일 | 확인 |
|---|---|---|
| **(a) 지표 JSON을 내 결과로** | 15:00에 받은 JSON 대신 **내 실습 A 결과**(한도안 · 스트레스 표 · 경보 요약)로 같은 모양의 `report_input.json`을 직접 만든다 — 값마다 어느 파일의 어디서 왔는지 근거를 적는다 | 같은 `make_report.py`가 통과하나 · 값이 모두 원본에서 다시 계산되나 |
| **(b) 태그** | 보고서를 커밋한 뒤 `git tag report-2026-09` → `git push origin report-2026-09`. 태그는 "이 보고서를 만든 그때의 코드와 숫자"에 붙이는 이름표다 | GitHub의 Releases · Tags에 보인다 |
| **(c) 예약 줄** | 워크플로의 `on:`에 `schedule`을 더한다(평일 09:00 KST = `0 0 * * 1-5`, **cron은 UTC** — 한국 시각에서 9시간을 뺀다). 권한 줄과 cron 줄은 **내가 직접 읽고 승인** | 수업 뒤 Actions 화면에서 **Disable workflow**로 끈다 |
| **(d) 의심 메일 판독**(시연 3 변형) | `labs/day4/mail/05_surrender_bl_B119.eml`과 [B5](../prompts/day4.md#b5) → 기대 **4점 · 멈춤 · P1**(⑪ 입금 전 서류 인도 3 + ⑥ 급박 1). 또는 내가 쓴 가상 메일 1통 | 상태(멈춤 · 확인 · 기록)가 AI가 근거 문장을 어떻게 골라도 같다 · 콜백 번호는 등록 번호 |
| **(e) 짝 PR 리뷰** | 짝의 규칙 PR에 리뷰 댓글 1개 — 경계값 · 권고 문장 · 기대 건수 | 한 줄이라도 근거가 있다 |

---

## 채팅 경로 — Claude Code를 못 쓸 때 {#chat-path}

Claude Code 계정이 없거나 확장이 로그인되지 않으면 **ChatGPT · Claude 웹 + GitHub 웹 화면**으로 같은 흐름을 따라갑니다. 오늘 파일은 합성 데이터라 올려도 됩니다. 프롬프트는 [B1–B6](../prompts/day4.md#chat-path)와 같고 경로 · 저장 줄만 바꿉니다.

1. **경보 표**: ChatGPT **데이터 분석**에 `d4_open_inv.csv` · `d4_start_scored.csv` · 내 `alert_rules.yml`을 올리고 "이 규칙대로 경보를 계산해 경보 표(xlsx)와 단계별 건수를 줘. dpd = 기준일(2026-09-30) − 결제기일, 문장은 모두 '권고(사람 승인 전)'"라고 합니다. 건수가 위 [15:20 점검](#b-engine) 숫자와 같은지 대조합니다.
2. **자동 실행은 GitHub 웹 화면으로**: 내 저장소에서 **Add file → Create new file**로 `.github/workflows/d4-ews.yml`을 만들어 `labs/day4/ews_workflow_example.yml`의 글을 붙여 **main에** 커밋합니다. 같은 방법으로 `workbench/day4/data/`에 **데이터 사본 두 개**를 올리고(**Upload files**), `labs/day4/`에 `ews_example.py` · `post_issue_example.py` · `alert_rules.yml`이 main에 있는지 확인합니다. 그다음 **Actions → d4-ews → Run workflow**.
3. **보고서**: 해석은 Claude, 레드팀은 ChatGPT(또는 반대)로 **두 번 따로** 합니다. 보고서는 `labs/day4/report_template.docx`(없으면 텍스트로) 칸에 붙여 넣고, 숫자는 `check_numbers.py` 대신 지표 JSON과 **손으로** 한 줄씩 대조합니다. 체크리스트 12항목은 그대로 합니다.
4. 결과 파일을 `workbench/day4/outputs/`에 **Add file → Upload files**로 올리고 PR을 만듭니다.

!!! warning "GitHub 웹의 Upload files는 .gitignore를 보지 않습니다"
    고른 파일을 그대로 올립니다. 올리기 전에 파일 이름과 내용을 한 번 봅니다 — 회사 실데이터 · 키 · 실명은 올리지 않습니다. 워크플로 파일에 **비밀번호나 웹훅 주소를 적지 않습니다**(저장소 Secrets에 둡니다).

---

## 막힐 때 {#troubleshooting}

| 증상 | 이렇게 해 보세요 |
|---|---|
| **`Run workflow` 버튼이 안 보인다** | 워크플로 파일이 **main에 없습니다**(작업 브랜치에만 있음). PR을 먼저 병합합니다. 이미 병합했다면 Actions 탭 왼쪽 목록에 `d4-ews`가 있는지, 파일의 `on:`에 `workflow_dispatch`가 있는지 봅니다 |
| 러너에서 **`can't open file 'scripts/ews.py'`** · 파일 없음 | 실행에 필요한 파일이 PR에 **빠졌습니다**(스크립트 · 규칙 사본 · 데이터 사본 중). `git status`로 빠진 것을 찾아 커밋하고 병합한 뒤 다시 실행합니다 |
| **403** · `Resource not accessible by integration` | 워크플로의 `permissions:`에 `issues: write`가 없습니다. 권한 줄을 읽고 고칩니다(필요한 것만 — `contents: read` · `issues: write`) |
| Actions 탭이 없거나 "workflows disabled" | 회사 · 학교 계정 저장소는 조직 정책으로 Actions가 꺼져 있을 수 있습니다. 손을 듭니다 — 개인 저장소(공개)에서는 켜져 있습니다 |
| 이슈가 **실행할 때마다 새로** 생긴다 | 같은 제목의 **열린** 이슈를 찾는 부분(중복 키)이 빠졌습니다. 제목이 `[조기경보] 2026-09-30 기준`으로 같은지, 이슈를 닫지 않았는지 봅니다 |
| cron을 **한국 시각으로** 적었다 | GitHub Actions의 cron은 **UTC**입니다. 평일 09:00 KST는 `0 0 * * 1-5`. 9시 전 시각은 전날이 되어 요일 칸도 하루 당겨집니다 |
| 속성 테스트가 실패한다 | 실패한 테스트 이름이 가리키는 성질 하나만 봅니다(경계값 · 신용장 면제 · 멱등 · 일관 · 권고 문장). 첫머리의 '엔진이 지켜야 할 모양'(호출 · 입력 · 결과)과 내 엔진을 대조하고, [고장 보고 4요소](../prompts/day4.md#a3)로 정리해 AI에게 줍니다 |
| 내 규칙을 넣었더니 테스트가 실패한다 | `--rules workbench/day4/rules/alert_rules.yml`로 같은 테스트를 돌립니다. `when` 식의 열 이름이 `d4_start_scored.csv` · 인보이스 열과 같은지, 따옴표 안의 따옴표(`'LC_SIGHT'`)가 맞는지 봅니다 |
| `ModuleNotFoundError: docxtpl` · 패키지 없음 | `uv add docxtpl`(이름은 오류 메시지가 알려 줍니다). `pyproject.toml`과 `uv.lock`이 함께 바뀌니 커밋에 포함합니다 |
| `narrative.json` 형식 오류로 렌더가 멈춘다 | `report_schema.json`의 칸 이름 그대로여야 합니다 — 코드 블록 표시(```)가 남았는지, `summary`가 정확히 3줄인지, `actions`마다 세 칸(`action` · `approver` · `status`)이 있는지 봅니다 |
| **숫자 대조가 실패한다** | ① 쉼표 · 반올림은 정규화되니 가짜 불일치가 아닌지(`4,290,901`과 `4290901`) ② **단위 다름**(곳 대 건)인지 ③ `number_trace`에 빠진 숫자가 있는지. 진짜 틀린 숫자면 문장을 고치고 다시 돌립니다 |
| 레드팀이 '지적 없음'만 낸다 | 같은 AI로 했는지 봅니다. **다른 서비스**의 새 대화에 B4를 다시 보내고, 지적이 없다면 '대조한 숫자 3개'를 확인합니다 |
| 같은 AI로 레드팀을 했다 | 다른 서비스로 다시 합니다 — 자기 글에는 관대해서 허점을 덜 찾습니다 |
| `uv`가 새 폴더에서 패키지를 못 찾는다 | 새 폴더(worktree)에서는 `uv sync` → `uv run python tools/get_day_files.py 4`를 먼저 합니다 |
| 허락 창이 계속 뜬다 | 읽고 `1 Yes`를 누릅니다. 모르는 명령이면 `No` 하고 "이 명령이 뭐 하는 거야?"라고 묻습니다. `2 … for this project`는 쓰지 않습니다 |
| 병합을 Claude Code에게 시키고 싶다 | 시키지 않습니다 — **병합 버튼은 GitHub 화면에서 내가 직접** 누릅니다 |

---

## 8교시 — 아침에 건 예약 실행, 정말 돌았나 {#period8}

17:00에 실험 카드 결과를 3명이 발표하고, 17:05에 강사가 **오전 11시에 걸어 둔 16:17 예약 실행**을 Actions 탭에서 함께 확인합니다 — 이벤트를 `schedule`로 거르면 예약으로 돈 실행만 보이고, 이슈의 맨 아래 댓글에는 실행 번호 · 이벤트 · 시각이 남습니다. 사람이 누른 버튼은 없습니다. **예약 시각이 정각이 아닌 이유**(붐비는 시각에 늦게 시작하거나 건너뛸 수 있어 17분처럼 비켜 씁니다)와 **안 돌았을 때 점검할 것**(워크플로가 기본 브랜치에 있나 · cron을 UTC로 적었나 · 실행 로그에 무엇이 남았나)을 고장 보고 4요소로 같이 봅니다.

<figure markdown="span">
  ![자동 이슈의 맨 아래 댓글(수동 실행 예시) — 이벤트 이름, 실행 번호, 실행 시각](../assets/screens/d4-issue-last-comment.png){ width="760" loading=lazy }
  <figcaption>이슈의 맨 아래 댓글 예시 — 예약 실행이면 이벤트가 schedule로 적힙니다. 오늘 화면의 예시는 수동 실행(workflow_dispatch)입니다</figcaption>
</figure>

내 워크플로에 예약 줄(더 하기 (c))을 더했다면 같은 방법으로 내 저장소의 Actions 목록을 확인하고, **연습이 끝나면 Disable workflow로 끕니다.** 수업이 끝난 뒤에도 켜 두면 평일 아침마다 돌고 실패하면 메일이 옵니다.
