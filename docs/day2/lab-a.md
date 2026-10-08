# 실습 A · 4–5교시 — 바이어 표 정제 파이프라인

!!! abstract "한눈에 보기 — 실습 A"
    | 항목 | 내용 |
    |---|---|
    | 목표 | 지저분한 바이어 표(150행)를 **규칙 문서 · 스크립트 · 테스트**로 정제해, 다시 돌려도 같은 결과가 나오는 파이프라인을 **이슈 → 브랜치 → PR**로 올린다 |
    | 시간 | **13:00–14:50**(110분) · 쉬는 시간은 필요할 때 스스로 |
    | 오전 시연을 이렇게 따라 한다 | 시연 2(엑셀 → 정제 파이프라인)를 **간소화** — 시트는 buyers 하나 · 프롬프트 4개 · 확인표 제공. 시연 1의 GitHub flow를 **이슈 1개 · 브랜치 1개 · PR 1개**로 줄여 처음부터 끝까지. 결측 채우기(중위수 · KNN)는 각자 골라 **변형**하고 짝과 비교 |
    | 입력 | `data/checkpoints/d2_start.xlsx`의 시트 `buyers`(150행 × 28열, 기준일 2026-08-31) |
    | 도구 | VS Code · **Claude Code**(Plan → Edit automatically) · Git · GitHub · 엑셀(한 건 손계산) |
    | 산출물 | 이슈 1개(닫힘) · PR 1개(머지) — `정제규칙.md` · `scripts/clean_buyers.py` · `tests/test_clean.py` · `d2_buyers_clean.csv`(150행) · `dq_report.md` · `scaling.md` |
    | 프롬프트 | [A1](../prompts/day2.md#a1) · [A2](../prompts/day2.md#a2) · [A3](../prompts/day2.md#a3) · [A4](../prompts/day2.md#a4) · [A5](../prompts/day2.md#a5) · [A6](../prompts/day2.md#a6) |

이 실습의 목표는 AI가 코드를 잘 짜는지 보는 것이 아닙니다. **무엇을 어떻게 고칠지를 내가 정하고**, 그 규칙이 **스크립트와 테스트로 남아** 다음 달에도 같은 결과가 나오게 하는 것입니다.
강사가 돌아다니며 한 분씩 2–3분 확인합니다. 막히면 손을 들거나 노트북 위에 빨간 표시(스티커)를 올리세요. **짝**과 서로의 PR을 리뷰하는 사이이니 옆자리 짝을 먼저 확인합니다.

## 시간표와 점검 시각 {#time}

| 시각 | 단계 | 하는 일 | 점검 |
|---|---|---|---|
| 13:00–13:15 | [① 준비](#a-prep) | `git pull` · 파일 받기 · 모드 Manual 확인 · 이슈 1개 · 브랜치 `d2-clean` | **13:15 손 점검** — 브랜치 `d2-clean` · 모드 Manual |
| 13:15–13:30 | [② 진단](#a-diag) | Plan 모드 → A1 → 진단 표 읽기 → `profile.md`로 저장 | 진단 표에서 '사람이 정할 곳' 찾기 |
| 13:30–13:50 | [③ 규칙](#a-rules) | A2 → `정제규칙.md` 1–7칸(결측 대체는 내가 고른다) | **13:50 손 점검** — 7칸 모두 `규칙/왜` |
| 13:50–14:15 | [④ 스크립트](#a-script) | A3 → 정제 CSV 150행 + 품질 보고서 | 150행 · 원본 그대로 |
| 14:15–14:35 | [⑤ 검증](#a-verify) | A4 테스트 · **확인표** · B001 손계산 · (A5) | **14:15 확인표** · 14:35 테스트 통과 |
| 14:35–14:50 | [⑥ 기록](#a-pr) | 커밋 2개+ · PR(`Closes #n`) · 짝 리뷰 · 머지 | **14:50 PR 머지 · 이슈 닫힘** |

!!! tip "늦었다면"
    13:30에 아직 ① 중이어도 괜찮습니다. 막히면 10분 안에 손을 들고, 14:35까지 PR을 열지 못했으면 [채팅 경로](#chat-path)로 바꿉니다. 실습 B는 머지된 `main`에서 시작하니, 늦어도 14:50까지는 PR을 머지해 둡니다.

## 입력 파일 {#files}

`uv run python tools/get_day_files.py 2`가 받아 줍니다(아래 ①). 08:30에 공개됩니다.

| 파일 | 위치 | 쓰는 곳 |
|---|---|---|
| 2일차 시작 파일 | `data/checkpoints/d2_start.xlsx` — 시트 `buyers`가 오늘의 입력, `fx_at_ref`는 기준일 환율, `dictionary`는 열 설명 | ②–⑤ |
| 원화 환율(일별) | `data/checkpoints/fx_krw_daily.csv` — 환율 30일 변화를 만들 때 | ③ · ④ |
| 정제 규칙 양식 | `workbench/day2/rules/정제규칙.md`(내 저장소에 이미 있습니다) · `labs/day2/rules_template.md`(같은 내용) | ③ |

받은 파일은 `workbench/day2/data/`에 **작업 사본**도 만들어집니다. `data/`의 원본은 읽기만 하고, 고쳐 쓸 것은 사본이나 새 파일로 합니다. 저장소 없이 채팅 경로로 가는 분은 [2일차 → 파일 받기](index.md#files)에서 받습니다.

---

## ① 준비 (13:00–13:15) {#a-prep}

1. VS Code에서 **내 저장소**를 열고, 편집기 오른쪽 위의 Claude 아이콘으로 **Claude Code 패널**을 엽니다. 로그인 상태이고 입력창 아래 모드 표시가 **Manual**인지 봅니다. Auto나 Plan이면 Manual로 바꿉니다(필수 — 시작 모드는 PC마다 다릅니다).
2. 터미널을 열고(++ctrl+grave++) 어제 내 저장소의 `main`을 최신으로 맞춥니다.

    ```text
    git pull
    ```

3. 오늘 파일을 받습니다.

    ```text
    uv run python tools/get_day_files.py 2
    ```

    `[받음] data/checkpoints/d2_start.xlsx  (사본 만듦)`처럼 파일마다 한 줄씩 나오면 됩니다. 08:30 전이면 "공개 전"이라고 알려 줍니다 — 공개 시각이 지난 뒤 같은 명령을 다시 실행합니다. 안 되면 [2일차 → 파일 받기](index.md#files)에서 직접 받습니다.
4. **GitHub 웹에서 이슈를 하나 만듭니다.** 이슈는 일의 주문서입니다 — 할 일과 **완료 기준**을 적어 둡니다.
    1. 내 저장소 화면에서 **Issues** 탭을 열고 초록색 **New issue**를 누릅니다.

        <figure markdown="span">
          ![GitHub Issues 탭 — 이슈 목록 위쪽의 초록색 New issue 단추, 열린 이슈 두 개와 라벨](../assets/screens/d2-issues-list.png){ width="640" loading=lazy }
          <figcaption>Issues 탭 — 오른쪽 위 <strong>New issue</strong>. 그림은 강사 시연 저장소의 이슈 목록입니다(로그아웃 화면이라 단추 모양만 같습니다)</figcaption>
        </figure>

    2. **제목**에 `바이어 표 정제 파이프라인`, **본문**에 아래를 붙여 넣고 **Create**(또는 Submit new issue)를 누릅니다.

        ```text
        ## 할 일
        data/checkpoints/d2_start.xlsx의 buyers 시트를 규칙·스크립트·테스트로 정제한다.

        ## 완료 기준
        - [ ] 테스트 통과 · 확인표 6줄 일치
        - [ ] 정제규칙.md 1–7칸 채움
        ```

    3. 이슈가 열리면 제목 옆의 **번호**(`#1` 같은 글자)를 메모합니다. 주소 끝의 `/issues/1`이 같은 번호입니다. 이 번호를 ⑥의 PR에 `Closes #번호`로 씁니다.

        <figure markdown="span">
          ![GitHub 이슈 한 건 — 제목, 무엇을 · 해야 할 일 · 완료 기준(체크 상자) 본문, 오른쪽 라벨](../assets/screens/d2-issue-example.png){ width="640" loading=lazy }
          <figcaption>이렇게 생긴 이슈가 만들어집니다(시연 저장소의 이슈 — 본문에 할 일과 완료 기준 체크 상자가 있습니다)</figcaption>
        </figure>

5. **브랜치 `d2-clean`**을 만듭니다. 일 하나에 갈래 하나입니다. 둘 중 편한 길로 합니다.
    - Claude Code에게 `d2-clean 브랜치를 만들어 줘`라고 말하고 허락 창을 읽어 `1 Yes`.
    - 또는 VS Code **왼쪽 아래 상태 표시줄의 브랜치 이름**(`main`)을 눌러 `+ Create new branch…` → `d2-clean` → Enter.

상태 표시줄에 `d2-clean`이 보이고 모드가 **Manual**이면 준비가 끝났습니다. **13:15 손 점검** — 강사가 돌며 브랜치와 모드를 봅니다.

---

## ② 진단 — Plan 모드로 고치지 않고 (13:15–13:30) {#a-diag}

AI에게 먼저 **읽고 표로만** 말하게 합니다. 고치기 전에 무엇이 나쁜지 이름을 붙이는 단계입니다.

1. 입력창 아래 모드 표시기를 눌러 **Plan**으로 바꿉니다(Plan은 파일을 고치지 못하는 읽기 전용 모드입니다).
2. 프롬프트 **A1**을 보냅니다.

    ??? example "프롬프트 A1 — 펼쳐서 복사"
        --8<-- "labs/day2/prompts.md:a1"

3. 진단 표가 나옵니다. **표를 읽습니다** — 통화 표기(9가지), 숫자 칸에 섞인 글자, 재무 항목 빈칸, 자기자본 0 이하, 신용한도에 비해 큰 잔액.

    <figure markdown="span">
      ![Plan 모드의 진단 결과 — 통화·날짜 표기 종류 표, 통화별로 비정상적으로 작은 금액 표가 이어지고 입력창 아래에 Plan 모드 표시](../assets/screens/d2-plan-diagnosis.png){ width="760" loading=lazy }
      <figcaption>Plan 모드 진단의 예(오전 시연 2 — 엑셀 두 시트를 진단한 결과). 입력창 아래 오른쪽에 <strong>Plan</strong> 표시가 보입니다. 표의 숫자는 시트마다 다릅니다</figcaption>
    </figure>

4. 답 끝에 **계획 승인 창**이 뜹니다. **`3 No, keep planning`**을 고릅니다. 승인(1 · 2번)하면 AI가 바로 코드를 쓰기 시작해 **내가 규칙을 정하기 전에** 앞서 갑니다.
5. 모드 표시기를 **Edit automatically**로 바꾸고 진단 표를 파일로 저장합니다.

    ??? example "프롬프트 — 진단 표 저장 · 펼쳐서 복사"
        --8<-- "labs/day2/prompts.md:a1-save"

    허락 창이 뜨면 **무엇을 · 어디에**(`workbench/day2/outputs/profile.md` 새 파일)를 읽고 `1 Yes`합니다. Edit automatically에서도 **명령 실행은 매번 묻습니다.**

**확인할 것** — 진단 표 맨 아래나 설명에서 **AI가 '사람이 정해야 한다'고 짚은 곳**을 찾습니다(예: JPY · CNY 잔액을 달러 한도와 어떻게 비교할지, 단위가 의심되는 한 곳을 고칠지, 결측을 어떻게 채울지). 그것이 ③에서 내가 정할 규칙입니다.

---

## ③ 규칙 — 정제규칙.md 1–7칸 (13:30–13:50) {#a-rules}

**규칙 문서가 먼저, 코드가 나중**입니다. 규칙은 `workbench/day2/rules/정제규칙.md`의 칸마다 `규칙`(무엇을 어떻게)과 `왜`(이유) 두 줄로 씁니다.

1. 프롬프트 **A2**를 보냅니다. `{중위수 또는 KNN}`은 **내가 고른 방식**으로 바꿉니다.

    | 방식 | 한 줄 | 이럴 때 |
    |---|---|---|
    | **중위수** | 같은 기준일 150곳의 가운데 값으로 채웁니다 — 큰 회사 몇 곳에 끌리지 않지만 값이 모두 같아 분포가 좁아집니다 | 단순하고 설명이 쉬운 쪽이 좋을 때 |
    | **KNN** | 가장 닮은 바이어 k곳의 값으로 채웁니다 — 국가위험 · 규모 같은 맥락을 반영하지만 스케일에 민감하고 설명이 어렵습니다 | 맥락을 살리고 싶을 때(스케일링을 먼저) |

    어느 쪽이든 **결측 플래그를 남기고**, 채울 값은 같은 기준일 데이터로만 계산합니다. **짝과 다른 방식을 골라** 나중에 결과를 비교해 봅니다.

    ??? example "프롬프트 A2 — 펼쳐서 복사"
        --8<-- "labs/day2/prompts.md:a2"

2. **확인표를 맞추고 싶다면** 같은 프롬프트 끝에 아래 결정 줄을 이어 붙입니다(권장). 확인표의 결측 플래그 47곳 · 단위 의심 · 자본잠식이 이 정의를 전제로 합니다.

    ??? example "A2 덧붙임 — 결정 줄 · 펼쳐서 복사"
        --8<-- "labs/day2/prompts.md:a2-decide"

3. 허락 창(규칙 문서 파일 쓰기)을 읽고 `1 Yes`합니다. AI가 **규칙을 되묻는 질문**(예: "JPY 잔액을 한도와 어떻게 비교할까요?")에는 짝과 의논해 직접 답합니다 — 사람이 정할 결정입니다.
4. 소스 제어(++ctrl+shift+g++)에서 `정제규칙.md`의 diff를 봅니다. 1–7칸에 `규칙:`과 `왜:`가 채워졌고 **규칙 문서만** 바뀌었는지 확인합니다.

    <figure markdown="span">
      ![VS Code 소스 제어의 정제규칙.md 비교 화면 — 비어 있던 규칙·왜 칸이 채워진 초록 줄](../assets/screens/d2-rules-diff.png){ width="760" loading=lazy }
      <figcaption>소스 제어에서 본 규칙 문서 diff의 예(오전 시연 2). 비어 있던 '규칙 / 왜' 칸이 채워집니다</figcaption>
    </figure>

!!! note "7칸 환율 · 시차에 들어갈 것"
    기준일 2026-08-31(또는 직전 영업일) 환율로 USD 환산 · `fx_chg_30d`(기준일 환율 ÷ 30일 전 환율 − 1) · `fx_chg_30d_lag30`(30일 전 환율 ÷ 60일 전 환율 − 1, 30일 전 시점의 30일 변화). 엔화는 **100엔 단위**라 ÷100합니다. 기준일 **뒤** 환율은 쓰지 않습니다(오전 as-of 조인).

**13:50 손 점검** — 7칸이 모두 채워졌고, 결측 대체 방식과 그 이유가 '왜' 칸에 적혀 있는지 봅니다.

---

## ④ 스크립트 — 규칙대로, 원본은 읽기만 (13:50–14:15) {#a-script}

1. 프롬프트 **A3**을 보냅니다. 허락 창의 명령(`uv run python scripts/clean_buyers.py` 같은 것)을 **읽고** `1 Yes`합니다.

    ??? example "프롬프트 A3 — 펼쳐서 복사"
        --8<-- "labs/day2/prompts.md:a3"

2. 오후 실습 B와 내일 3일차로 이어지려면 결과에 아래 25열이 있어야 합니다. A3 끝에 이어 붙이거나, 결과에 빠진 열이 있으면 따로 시킵니다(열 이름은 그대로).

    ??? example "A3 덧붙임 — 결과 열 · 펼쳐서 복사"
        --8<-- "labs/day2/prompts.md:a3-columns"

3. 결과 세 가지가 생겼는지 봅니다.
    - `scripts/clean_buyers.py` — 정제 코드(저장소의 `scripts/` 폴더)
    - `workbench/day2/outputs/d2_buyers_clean.csv` — **150행**
    - `workbench/day2/outputs/dq_report.md` — 전·후 비교(통화 표기 9종 → 4종 · 글자 섞인 칸 · 결측 · 단위 의심)

    <figure markdown="span">
      ![품질 보고서 Markdown 미리보기 — 항목별 전·후 건수 표와 아래 터미널의 pytest 통과 줄](../assets/screens/d2-dq-report.png){ width="760" loading=lazy }
      <figcaption>품질 보고서의 예(오전 시연 2 — 인보이스까지 정제한 판이라 표가 더 깁니다). 정제 전 · 후 건수가 한 표에 있어야 합니다</figcaption>
    </figure>

**확인할 것**

- `scripts/clean_buyers.py`가 **원본 엑셀을 덮어쓰지 않는지** 훑어봅니다. 터미널에서 `git status`를 쳤을 때 `data/`에 변경이 없어야 합니다.
- 결과가 **150행**이고 `buyer_id`가 첫 열, `late_30d`가 끝 열인지 봅니다. 숫자는 AI의 암산이 아니라 **스크립트가 낸 값**이어야 합니다.
- `dq_report.md`에 전·후 건수 표가 있는지 봅니다. 마크다운 미리보기는 ++ctrl+shift+v++.

---

## ⑤ 검증 — 테스트 · 확인표 · 손계산 (14:15–14:35) {#a-verify}

1. 프롬프트 **A4**를 보냅니다. AI가 테스트 파일(`workbench/day2/tests/test_clean.py`)을 쓰고 실행해 통과할 때까지 고칩니다.

    ??? example "프롬프트 A4 — 펼쳐서 복사"
        --8<-- "labs/day2/prompts.md:a4"

2. 직접 한 번 돌려 봅니다. 저장소 맨 위에서:

    ```text
    uv run pytest -q
    ```

    `passed`가 보이면 통과입니다. 저장소의 `pytest.ini`가 2일차 작업 폴더(`workbench/`)의 테스트만 돌게 해 둡니다. 오류가 나면 [막힐 때](#troubleshooting)를 봅니다.

    <figure markdown="span">
      ![터미널 pytest 실행 — 전체 10 passed 줄과 테스트 파일 하나의 6개 항목이 모두 PASSED](../assets/screens/d2-pytest-passed.png){ width="720" loading=lazy }
      <figcaption>테스트 통과의 예(오전 시연 2). 항목 이름이 곧 규칙입니다 — 행 수 · ID 유일 · 통화 4종 · 금액 ≥ 0 · 단위 플래그 · 중복 0</figcaption>
    </figure>

3. **테스트가 실패하면** 바로 "고쳐 줘"라고 하지 말고 먼저 묻습니다 — **테스트가 틀렸나, 규칙이 틀렸나, 산출물이 틀렸나?** 오전 시연 2에서도 첫 실행에 열이 빠져 실패했고, AI는 테스트가 아니라 결과를 고쳤습니다. 그 판단이 맞았는지 내가 확인하는 것이 사람의 몫입니다.

    <figure markdown="span">
      ![테스트 실패 화면 — KeyError와 AI가 원인을 설명하는 문장](../assets/screens/d2-test-failure.png){ width="720" loading=lazy }
      <figcaption>실패의 예(오전 시연 2) — 오류 이름, AI의 원인 설명. '고쳐 줘' 전에 어느 쪽이 틀렸는지 먼저 봅니다</figcaption>
    </figure>

4. **B001 한 곳을 엑셀로 손계산**합니다. 새 엑셀 칸에 입력해 `d2_buyers_clean.csv`의 B001 `ar_balance_usd`와 같은지 봅니다. B001은 EUR 18,100, 기준일(2026-08-31) 환율은 유로 1,589.50원 · 달러 1,368.25원입니다.

    ```text
    =18100*1589.5/1368.25
    ```

5. **14:15 확인표**를 엽니다. 여섯 줄이 모두 맞으면 통과이고, 다르면 바로 고치지 말고 [어느 규칙에서 갈렸나](../prompts/day2.md#mismatch)를 AI에게 먼저 묻습니다.

    ??? success "실습 A 확인표 — 14:15에 엽니다(그 전에는 내 숫자를 믿고 갑니다)"
        | 확인 | 기대값 |
        |---|---|
        | 통화 정리 | USD 110 · EUR 23 · JPY 10 · CNY 7 |
        | B001 잔액(USD) | 21,026.82 (EUR 18,100 × 1,589.50 ÷ 1,368.25) |
        | 단위 의심 | B072 한 곳 → ÷1,000 후 9,665.37 USD |
        | 자본잠식 | B013 · B048 (부채비율 빈칸) |
        | 결측 처리 | 플래그 47곳 · 중위수라면 1.4218 · 1.4579 · 66.44 · 0.0654 |
        | 기록 | 테스트 통과 · 스케일 비교 표 · 커밋 2개+ · PR 1개(`Closes #n`) |

        - 결측 플래그 47곳은 유동자산 · 유동부채 · 총부채 · 자기자본 · 매출 가운데 **하나라도 빈칸**인 바이어 수입니다. 이 정의를 규칙 문서 3칸에 적어 둡니다.
        - **KNN**을 골랐다면 대체값이 중위수와 다르게 나오는 것이 정상이고, **플래그 47곳은 같아야** 합니다.
        - B001 한 행을 더 보려면: `late_ratio` 0.4444 · `dpd_trend` −19.2 · `current_ratio` 1.631 · `debt_to_equity` 0.6007 · `dso_buyer` 34.76 · `op_margin` 0.1183 · `fx_chg_30d` −0.0396 · `fx_chg_30d_lag30` −0.06.

6. **먼저 끝난 사람**은 A5로 스케일 비교 표를 만듭니다(특성 파일에는 넣지 않습니다).

    ??? example "프롬프트 A5 — 선택 · 펼쳐서 복사"
        --8<-- "labs/day2/prompts.md:a5"

    규칙 문서에 **"정규화 열을 특성 파일에 넣지 않는 이유"**를 한 줄 적습니다 — 평가 데이터의 정보가 섞이고, 내일의 트리 모델은 스케일에 둔감하기 때문입니다.

---

## ⑥ 기록 — 커밋 · PR · 짝 리뷰 · 머지 (14:35–14:50) {#a-pr}

1. **커밋을 2개 이상**으로 나눕니다 — ① 규칙 문서 ② 스크립트 · 테스트 · 결과. 소스 제어에서 파일을 골라(`+`) 메시지 칸에 **첫 줄 · 빈 줄 · `왜:` 줄**을 쓰고 **Commit**을 누릅니다.

    ```text
    2일차: 바이어 정제 규칙 1–7칸 작성

    왜: 고치는 이유를 규칙 문서에 먼저 남기려고
    ```

    ```text
    2일차: 정제 스크립트 · 테스트 · 결과 추가

    왜: 같은 규칙으로 다시 돌려도 150행이 같게 나오는지 테스트로 확인
    ```

    Claude Code에게 시켜도 됩니다(프롬프트 A6). 허락 창의 명령에서 **메시지가 두 줄인지**, **push 대상이 `d2-clean`인지** 읽고 승인합니다.

    ??? example "프롬프트 A6 — 선택 · 펼쳐서 복사"
        --8<-- "labs/day2/prompts.md:a6"

2. **push**합니다 — 소스 제어의 **Publish Branch**(또는 터미널 `git push -u origin d2-clean`).
3. **PR을 만듭니다.** 내 저장소 화면 위쪽의 노란 안내 **Compare & pull request**를 누릅니다(안 보이면 Pull requests 탭 → New pull request → base `main` ← compare `d2-clean`). **본문 첫 줄**에 `Closes #번호`(①에서 메모한 번호), 이어서 품질 보고서 요약 몇 줄과 **내가 정한 규칙** 목록을 씁니다. **Create pull request**.

    <figure markdown="span">
      ![PR 본문 Markdown 미리보기 — 요약 다섯 줄과 사람이 결정한 규칙 목록](../assets/screens/d2-pr-body.png){ width="760" loading=lazy }
      <figcaption>PR 본문의 예(오전 시연 2) — 요약과 '사람이 결정한 규칙'이 목록으로 남습니다. 다음 달 이 PR을 보는 사람이 왜 이렇게 고쳤는지 알 수 있습니다</figcaption>
    </figure>

4. **짝이 리뷰**합니다. 짝의 PR에서 **Files changed**를 열고 줄 왼쪽의 `+`를 눌러 코멘트를 **하나** 남깁니다. 데이터 PR은 이 네 가지를 봅니다 — **행 수 전·후 · 테스트 통과 · 실데이터와 키 없음 · 규칙 문서 갱신.**

    <figure markdown="span">
      ![PR Files changed 화면 — 통화 매핑표 추가 줄(초록)과 그 아래 리뷰 코멘트](../assets/screens/d2-pr-review.png){ width="760" loading=lazy }
      <figcaption>리뷰 코멘트의 예(오전 시연 1) — 바뀐 줄 바로 아래에 '무엇이 빠질 수 있는지'를 적고 고쳐 달라고 합니다</figcaption>
    </figure>

    !!! warning "짝이 내 저장소에 코멘트를 달 수 있어야 합니다"
        내 저장소가 **공개**면 로그인한 GitHub 사용자는 누구나 PR에 코멘트할 수 있습니다. **비공개**로 만들었다면 Settings → Collaborators에서 짝을 초대해 두어야 합니다(14:35에 초대하고 짝이 수락).

5. 받은 코멘트를 **반영**합니다(고치고 → 커밋 → push, PR에 자동으로 붙습니다). Claude Code에게 "PR의 리뷰 코멘트를 반영해 줘"라고 시켜도 됩니다.
6. **머지**합니다. PR 화면 아래 **Merge pull request** → **Create a merge commit**(기본) → Confirm. **머지는 Claude Code에게 시키지 않고 내가 직접** 누릅니다. 머지가 끝나면 이슈가 자동으로 닫힙니다(Issues 탭의 Closed 1).
7. 내 PC를 `main`으로 돌립니다 — 실습 B가 머지된 `main`에서 시작합니다.

    ```text
    git switch main
    git pull
    ```

**14:50 PR 머지** — 이슈가 닫히고 `main`에 정제 결과가 있으면 실습 A 완료입니다.

!!! info "Actions의 ✓ / ✗"
    저장소에 자동 검사(GitHub Actions)가 있으면 PR 화면에 ✓ 또는 ✗가 붙습니다. 오늘 내 저장소에는 검사를 켜 두지 않았으니 없어도 정상입니다. 오전 시연 1의 저장소에서는 이런 화면이 나왔습니다.

    <figure markdown="span">
      ![PR Checks 화면 — validate 검사가 성공으로 끝난 줄](../assets/screens/d2-pr-checks.png){ width="640" loading=lazy }
      <figcaption>자동 검사 통과의 예(오전 시연 1) — 머지 전에 서버가 테스트를 돌려 ✓를 붙입니다</figcaption>
    </figure>

### 실습 A 완료 기준 {#checkpoint}

- [ ] `workbench/day2/rules/정제규칙.md` 1–7칸에 `규칙` · `왜`가 모두 있고, 결측 대체 방식과 이유가 적혀 있다
- [ ] `scripts/clean_buyers.py` · `workbench/day2/outputs/d2_buyers_clean.csv`(150행) · `dq_report.md`가 있고, 원본(`data/`)은 그대로다
- [ ] `uv run pytest -q`가 통과한다 · B001을 엑셀로 손계산해 일치했다 · 확인표 여섯 줄이 맞다
- [ ] 커밋이 2개 이상이고 PR 본문 첫 줄이 `Closes #번호`다 · 짝의 리뷰 코멘트 1개를 반영했다
- [ ] PR을 머지했고 이슈가 닫혔다

## 다 했으면 {#extend}

- **인보이스 시트 정제**: `invoices_raw`(1,902행)의 날짜 4형식 · 완전 중복 · 소수점 밀림을 같은 방식(진단 → 규칙 → 스크립트 → 테스트)으로 정제합니다. 슬래시 날짜는 일/월/연이고, 일 · 월이 모두 12 이하인 칸은 순서를 사람이 정해야 합니다.
- **같은 정제를 SQL로**: 오전 시연 3 방식으로 DuckDB에 올려 같은 결과가 나오는지 견줍니다(AI가 쓴 쿼리는 원본 값으로 검증).
- **중위수 vs KNN 비교 표**: 짝과 고른 방식을 바꿔 돌려 대체값 차이를 `workbench/day2/outputs/`에 표로 남깁니다.
- **자사 데이터(BYOD)**: [익명화 점검표](../setup.md#byod)(`byod_anonymize_template.xlsx`)를 통과한 사본으로만, 내 PC에서만, `private/` 폴더에서. **커밋 금지** — 이 저장소는 공개입니다.

---

## 채팅 경로 — Claude Code를 못 쓸 때 {#chat-path}

Claude Code 계정이 없거나(무료 플랜은 쓸 수 없습니다) 확장이 로그인되지 않으면 **Claude 또는 ChatGPT 웹**에 파일을 올려 같은 결과에 도착합니다. 프롬프트는 [A1–A3](../prompts/day2.md#chat-path)과 같고 파일 경로 · 저장 줄만 바꿉니다.

1. 웹 채팅에 `d2_start.xlsx`를 **첨부**하고 A1(진단) → A2(규칙) → A3(정제)를 차례로 보냅니다. Claude는 코드 실행, ChatGPT는 데이터 분석 기능이 켜져 있어야 파일을 만들어 줍니다. ChatGPT 무료는 하루 업로드 수가 적으니 Claude를 먼저 권합니다.
2. **결과 CSV**를 내려받아 `d2_buyers_clean.csv`로 저장하고, 규칙 문서는 채팅 답을 복사해 `정제규칙.md`(양식은 [`labs/day2/rules_template.md`](https://github.com/brainini/tradefin-ai-2026/blob/main/labs/day2/rules_template.md))로 저장합니다.
3. **GitHub 웹에서 올립니다.**
    1. 내 저장소 화면의 브랜치 선택(`main ▾`)에 `d2-clean`을 입력하고 **Create branch**를 누릅니다.
    2. `workbench/day2/outputs/` 폴더로 들어가 **Add file → Upload files**로 결과 파일을 끌어다 놓고, 커밋 메시지 첫 줄과 설명 칸(`왜:`)을 쓴 뒤 **Commit directly to the `d2-clean` branch**를 고르고 **Commit changes**. 규칙 문서도 `workbench/day2/rules/`에서 같은 방법으로 올립니다.
    3. 저장소 첫 화면의 **Compare & pull request** → 본문 첫 줄 `Closes #번호` → **Create pull request**. 나머지(짝 리뷰 · 머지)는 ⑥과 같습니다.
4. Claude 유료 계정(Pro · Max)이면 데스크톱 앱에 작업 폴더를 연결해 같은 정리를 맡기는 길(Cowork)도 있습니다. 계정에 따라 Cowork 탭 대신 한 대화에서 맡기게 됩니다. **연결한 폴더의 파일은 Anthropic 클라우드에서 처리**되니 오늘처럼 합성 데이터일 때만 씁니다.

!!! warning "GitHub 웹의 Upload files는 .gitignore를 보지 않습니다"
    고른 파일을 그대로 올립니다. 올리기 전에 파일 이름과 내용을 한 번 봅니다 — 회사 실데이터 · 키 · 실명은 올리지 않습니다.

---

## 막힐 때 {#troubleshooting}

| 증상 | 이렇게 해 보세요 |
|---|---|
| Plan 모드인데 파일이 안 만들어진다 | Plan은 읽기만 합니다. 진단이 끝나면 모드를 **Edit automatically**로 바꿉니다 |
| 계획 승인 창에서 승인을 눌러 AI가 바로 스크립트를 쓰기 시작했다 | Esc로 멈추고, 만들어진 파일을 읽은 뒤 **규칙 문서(A2)를 먼저** 채워 서로 맞는지 봅니다. 다음부터는 `3 No, keep planning` |
| `uv run pytest -q`가 오류를 낸다(`streamlit` 같은 말) | 저장소 맨 위에서 `git pull`로 `pytest.ini`를 받았는지 봅니다. 그래도 같으면 `uv run pytest -q workbench/day2/tests`처럼 경로를 줍니다 |
| 테스트가 계속 실패한다 | 실패 메시지를 AI에게 보여 주되 "어느 쪽이 틀렸나(테스트 · 규칙 · 산출물)"를 먼저 판단하게 합니다 |
| 확인표와 숫자가 다르다 | [어느 규칙에서 갈렸나](../prompts/day2.md#mismatch)를 먼저 묻습니다. 규칙 문서를 고치면 '9. 변경 기록'에 한 줄 더합니다 |
| `get_day_files.py`가 "공개 전"이라고 한다 | 08:30 이후 같은 명령을 다시 실행합니다. 계속 안 되면 [2일차 → 파일 받기](index.md#files) |
| `Closes #번호`를 썼는데 이슈가 안 닫힌다 | 번호가 맞는지, PR이 `main`을 향하는지 봅니다. 이슈는 **main에 머지될 때** 닫힙니다 |
| 허락 창이 계속 뜬다 | 읽고 `1 Yes`를 누릅니다. 모르는 명령이면 `No` 하고 "이 명령이 뭐 하는 거야?"라고 묻습니다. `2 … for this project`는 쓰지 않습니다 |
| push가 거부된다 · 로그인을 묻는다 | VS Code 왼쪽 아래 **계정 아이콘**에서 GitHub에 로그인합니다. `GH007 … private email` 오류면 `git config --global user.email`을 noreply 주소로 바꾸고 다시 커밋합니다 |
