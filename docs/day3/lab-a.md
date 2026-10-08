# 실습 A · 4–5교시 — 내 첫 연체 예측 모델

!!! abstract "한눈에 보기 — 실습 A"
    | 항목 | 내용 |
    |---|---|
    | 목표 | 300행 특성표로 **기준선(로지스틱)과 LightGBM**을 학습하고, **누수를 직접 확인**하고, 내 회사 비용비로 **임계값을 정해** 커밋한다 |
    | 시간 | **13:00–14:50**(110분) · 쉬는 시간 13:50–14:00 |
    | 오전 시연을 이렇게 따라 한다 | 시연 3(누수 탐정과 모델 리그전)을 **300행 · 모델 2개 · 이미 나뉜 `split_suggested`**로 **간소화**한다. 시연 4(비용으로 움직이는 임계값 엑셀)는 엑셀 대신 **Markdown 표**로 바꾸고, 비용비는 각자 고르게 **변형**한다(3:1 · 5:1 · 10:1) |
    | 입력 | `data/checkpoints/d3_start_features.csv`(300행 × 53열, 연체 16건) · `workbench/day3/rules/d3_rules.md`(오늘의 데이터 규칙) |
    | 도구 | VS Code · **Claude Code**(Plan → 계획 승인 후 수동 승인) · Git · GitHub |
    | 산출물 | `d3_data_card.md` · `d3_train.py` · `d3_eval.md` · `d3_test_pred.csv` · `model_v1.txt` · `d3_threshold.md` / **커밋 2개 이상 + push** |
    | 프롬프트 | [A0](../prompts/day3.md#a0) · [A1](../prompts/day3.md#a1) · [A2](../prompts/day3.md#a2) · [A3](../prompts/day3.md#a3) · [A4](../prompts/day3.md#a4) · [A5](../prompts/day3.md#a5) |

이 실습의 목표는 AI가 코드를 잘 짜는지 보는 것이 아닙니다. **무엇을 정답으로 볼지 · 어디서 나눌지 · 얼마나 아픈지(비용)를 내가 정하고**, AI가 쓴 모델의 숫자를 **내가 의심해 보는 것**입니다. 강사가 돌아다니며 한 분씩 2–3분 확인합니다. 막히면 손을 들거나 노트북 위에 빨간 표시(스티커)를 올리세요.

## 슬라이드의 단계 {#slide-steps}

슬라이드 두 장(실습 A-1 · A-2)과 같은 순서입니다. 아래 ①–⑨가 이 단계를 풀어 쓴 것입니다.

!!! abstract "실습 A-1 · 데이터 카드와 첫 모델 (13:00–13:50)"
    1. 오늘 파일 받기 → 브랜치 `d3-model` → Claude Code에 `@d3_rules.md`(오늘의 데이터 규칙)부터 읽히기
    2. **Plan 모드**로 데이터 카드 → `outputs/d3_data_card.md` — 행 · 열 수, 기준일별 연체 건수, 쓰면 안 되는 열과 이유
    3. `split_suggested`로 나눠 로지스틱 · LightGBM 학습 → `d3_eval.md`(AUC · PR-AUC · Brier)
    4. 누수 실험: `sample_weight`를 넣으면? → AUC 비교 후 `diff`로 원상복구 확인
    5. 커밋 — 메시지 두 줄(무엇 / 왜)

    산출: `d3_data_card.md` · `d3_eval.md` · `d3_train.py` · 커밋 1개

!!! abstract "실습 A-2 · 비용 기준 임계값 (14:00–14:50)"
    1. t = 0.05~0.50 비용표(5 × FN + FP) → `d3_threshold.md` — 최소 비용 t와 이론값 1/6을 비교한다
    2. 놓친 연체(FN) 바이어 목록과 주요 특성 3개 → 공통점 2줄
    3. 내 회사 비용비(3:1 또는 10:1)로 다시 → 무엇이 바뀌나 1줄
    4. 표준: 패널 시간 분할로 같은 실험 · 도전 ①: class weight · SMOTE 비교 · 도전 ②: 부트스트랩 AUC 구간 · worktree 병렬
    5. 14:45 기대 범위 확인 → 커밋 · push

    산출: `d3_threshold.md` · 커밋 2개 이상

## 시간표와 점검 시각 {#time}

| 시각 | 단계 | 하는 일 | 점검 |
|---|---|---|---|
| 13:00–13:10 | [① 준비](#a-prep) | 파일 받기 · 브랜치 `d3-model` · 모드 확인 · A0 규칙 읽히기 | 브랜치 `d3-model` · 파일 4개 열림 |
| 13:10–13:20 | [② 데이터 카드](#a-card) | Plan 모드 → A1 → 계획 읽기 → 승인(`2`) → `d3_data_card.md` | **13:20 점검** — 300행 · 연체 16 · 메타 열 2개 |
| 13:20–13:40 | [③ 첫 모델](#a-model) | A2 → 학습 · 평가 → `d3_eval.md` | **13:40 점검** — 시험셋 88행 · 연체 4 |
| 13:40–13:50 | [④ 누수 실험 · ⑤ 커밋](#a-leak) | A3 → AUC 비교 → diff → 첫 커밋 | **13:50** 커밋 1개 |
| 13:50–14:00 | 쉬는 시간 | | |
| 14:00–14:20 | [⑥ 비용표](#a-cost) | A4 → `d3_threshold.md` | **14:20** 임계값표 |
| 14:20–14:30 | [⑦ 놓친 바이어 · 내 비용비](#a-fn) | FN 공통점 2줄 → 비용비 3:1 또는 10:1로 다시 | 변화 1줄 |
| 14:30–14:45 | [⑧ 트랙 확장](#a-tracks) | 표준 · 도전(빨리 끝난 분) | – |
| 14:45–14:50 | [⑨ 기대 범위 · 커밋 2 · push](#a-commit) | 기대 범위 표 확인 → 커밋 · push | **14:50** 커밋 2개 이상 · push |

!!! tip "늦었다면"
    13:20에 아직 ① 중이어도 괜찮습니다. 막히면 10분 안에 손을 들고, 14:00까지 첫 모델을 못 만들었으면 [채팅 경로](#chat-path)로 바꿉니다. 실습 B는 A의 `model_v1.txt` · `d3_test_pred.csv`를 쓰니, 14:45까지는 **모델과 시험셋 예측**이 있어야 합니다.

## 입력 파일 {#files}

`uv run python tools/get_day_files.py 3`이 받아 줍니다(아래 ①). **10/16(금) 08:30**에 공개됩니다.

| 파일 | 위치 | 쓰는 곳 |
|---|---|---|
| 학습용 특성(300행) | `data/checkpoints/d3_start_features.csv` — 바이어 150곳 × 기준일 2개(2026-02-28 · 08-31) × 53열. 정답은 `late_30d`(연체 16건), `split_suggested`가 학습 212행 · 시험 88행(연체 4)을 바이어 단위로 나눠 둠 | ②–⑦ |
| 패널(표준 트랙) | `data/checkpoints/d3_features_panel.csv` — 바이어 × 월 4,017행(2024-01~2026-08, 연체 215건) | ⑧ |
| 데이터 사전 | `data/data_dictionary.xlsx` — `columns` 시트에서 모르는 열의 뜻 · 단위를 찾는다 | 모르는 열 |
| 오늘의 데이터 규칙 | `workbench/day3/rules/d3_rules.md` — 빼는 열 · 분할 · 시드 · 결과 위치 | ① |

받은 파일은 `workbench/day3/data/`에 **작업 사본**도 만들어집니다. `data/`의 원본은 읽기만 하고, 고쳐 쓸 것은 사본이나 새 파일로 합니다. 저장소 없이 채팅 경로로 가는 분은 [3일차 → 파일 받기](index.md#files)에서 받습니다.

!!! warning "`sample_weight`는 특성이 아닙니다"
    불균형을 보정하려고 **정답으로 계산해 넣은 가중치**입니다 — 연체 행은 9.375, 정상 행은 0.528. 특성으로 넣으면 누수입니다. 오늘의 함정이고, ④에서 일부러 한 번만 넣어 봅니다.

---

## ① 준비 (13:00–13:10) {#a-prep}

1. VS Code에서 **내 저장소**를 열고(폴더 **'신뢰'**), 편집기 오른쪽 위의 Claude 아이콘으로 **Claude Code 패널**을 엽니다. 로그인된 상태이고 입력창 아래 모드 표시가 **Manual 또는 Plan**인지 봅니다(Auto로 시작했다면 바꿉니다 — 시작 모드는 PC마다 다릅니다).
2. 터미널을 열고(++ctrl+grave++) 어제 PR을 머지했다면 내 PC를 `main`으로 맞춥니다.

    ```text
    git switch main
    git pull
    ```

3. 오늘 파일을 받습니다. 처음 쓰는 PC이면 `uv sync`를 먼저 한 번 합니다.

    ```text
    uv run python tools/get_day_files.py 3
    ```

    `[받음] data/checkpoints/d3_start_features.csv  (사본 만듦)`처럼 파일마다 한 줄씩 나오면 됩니다. 08:30 전이면 "공개 전"이라고 알려 줍니다 — 시각이 지난 뒤 같은 명령을 다시 실행합니다. 안 되면 [3일차 → 파일 받기](index.md#files)에서 직접 받습니다.
4. **브랜치 `d3-model`**을 만듭니다. 일 하나에 갈래 하나입니다.

    ```text
    git switch -c d3-model
    ```

    VS Code **왼쪽 아래 상태 표시줄의 브랜치 이름**을 눌러 `+ Create new branch…`로 만들어도 됩니다.
5. Claude Code에 **오늘의 규칙**을 읽힙니다(프롬프트 **A0**).

    ??? example "프롬프트 A0 — 펼쳐서 복사"
        --8<-- "labs/day3/prompts.md:a0"

**13:10 점검** — 상태 표시줄에 `d3-model`이 보이고, 파일 네 개(`d3_start_features.csv` · `d3_features_panel.csv` · `d3_start_scoring.csv` · `fx_forecast_inputs.csv`)가 열리는지 봅니다. A0의 요약에 **빼는 열 다섯 개 · 시드 42**가 들어 있으면 준비가 끝났습니다.

---

## ② 데이터 카드 — Plan 모드로 (13:10–13:20) {#a-card}

AI가 데이터를 쓰기 전에 **먼저 읽고 표로 말하게** 합니다. 열의 뜻과 누수 후보를 AI가 초안으로 쓰고, **사람이 확인**하는 단계입니다.

1. 입력창 아래 모드 표시기를 눌러 **Plan**으로 바꿉니다(파일을 고치지 못하는 읽기 전용 모드입니다).
2. 프롬프트 **A1**을 보냅니다.

    ??? example "프롬프트 A1 — 펼쳐서 복사"
        --8<-- "labs/day3/prompts.md:a1"

3. 계획이 열리면 **금지 열 표**를 읽습니다. 오전 시연 3의 계획과 같은 모양입니다 — 열을 '식별자 · 정답이나 보조 열 · 미래 정보 · 같은 정보 중복'으로 나눈 표입니다.

    <figure markdown="span">
      ![Plan 모드 계획의 특성 제외 표(구분 · 열 · 이유)와 아래 데이터 사전의 sample_weight 정의 줄](../assets/screens/d3-plan-exclude-table.png){ width="760" loading=lazy }
      <figcaption>시연 3의 계획에 나온 '특성 제외 표'와 데이터 사전의 sample_weight 정의(빨간 상자) — 오늘 데이터 카드의 표도 이런 모양입니다. 시연에서 쓴 패널 파일 기준이라 열 목록은 조금 다릅니다</figcaption>
    </figure>

4. 계획 승인 창이 뜨면 **`2 Yes, and manually approve edits`**를 고릅니다. 계획대로 실행하되 **파일을 쓰거나 명령을 돌릴 때마다 한 번씩 확인**합니다. 맨 위 `use auto mode`는 고르지 않습니다.
5. 허락 창이 뜨면 **무엇을 · 어디에**(`workbench/day3/outputs/d3_data_card.md` 새 파일)를 읽고 `1 Yes`합니다.

**13:20 점검** — 데이터 카드를 엽니다(++ctrl+shift+v++로 미리보기). 다음이 보여야 합니다.

- **300행 · 연체 16** · 기준일 2개(2월 말 3건 · 8월 말 13건)
- 메타 열 **`sample_weight` · `split_suggested`**가 '쓰면 안 되는 열'에 있고 이유가 적혀 있다
- 숫자는 AI의 암산이 아니라 **코드로 계산한 값**이다. 모르는 항목은 '데이터 확인 필요'로 적혀 있다

---

## ③ 첫 모델 — 로지스틱과 LightGBM (13:20–13:40) {#a-model}

1. 프롬프트 **A2**를 보냅니다. 허락 창의 명령(`uv run python workbench/day3/outputs/d3_train.py` 같은 것)은 **읽고** `1 Yes`합니다.

    ??? example "프롬프트 A2 — 펼쳐서 복사"
        --8<-- "labs/day3/prompts.md:a2"

2. 결과 파일이 생겼는지 봅니다.
    - `workbench/day3/outputs/d3_train.py` — 학습 코드
    - `d3_eval.md` — 두 모델의 시험셋 ROC-AUC · PR-AUC · Brier + 임계값 0.5 혼동행렬
    - `d3_test_pred.csv` — 시험 88행의 예측(`buyer_id` · `ref_date` · `late_30d` · `pd_30d`) — **실습 B-1의 단조성 점검**이 씁니다
    - `model_v1.txt` — 학습한 LightGBM — **실습 B-1에서 150곳 점수**를 낼 때 씁니다
3. 코드를 훑어봅니다. **특성에 `sample_weight` · `split_suggested` · `buyer_id` · `ref_date`가 없는지**, 시험셋으로 학습하지 않았는지(`split_suggested == "test"`는 평가에만) 봅니다.

**13:40 점검**

- 시험셋이 **88행 · 연체 4건**
- ROC-AUC가 **0.80–1.00** — 모델 · 특성 선택에 따라 사람마다 다른 것이 정상입니다(로지스틱은 대개 0.80–0.90, LightGBM은 0.93–0.97). 시험 연체가 4건뿐이라 **한 건에 크게 흔들립니다**(오전 시연 1의 표본 흔들림 그대로입니다). 0.99 이상으로 붙어 있으면 누수부터 의심합니다.
- LightGBM 설정(`num_leaves=7` · `min_child_samples=10` …)이 코드에 **프롬프트에서 준 값 그대로** 들어갔는지 봅니다 — 오전 슬라이드의 학습 코드 장에서 본 '학습 전에 사람이 정하는 설정값'에서 `min_child_samples`만 30 → 10으로 바꾼 것입니다.

---

## ④ 누수 실험 — sample_weight를 넣으면 (13:40–13:45) {#a-leak}

1. 프롬프트 **A3**을 보냅니다.

    ??? example "프롬프트 A3 — 펼쳐서 복사"
        --8<-- "labs/day3/prompts.md:a3"

2. 결과를 읽습니다. `sample_weight`를 넣으면 로지스틱도 LightGBM도 **AUC가 1.00으로 뜹니다.** 이 열 하나가 정답을 알려 주기 때문입니다 — 오전의 'AUC 1.0 연체 모델'과 같은 장면을 내 손으로 만든 것입니다.
3. 실험이 끝나면 코드가 **원래대로 돌아왔는지** 봅니다. 프롬프트가 실험 전에 `git add`로 `d3_train.py`를 스테이징해 두라고 했습니다 — 스테이징한 모습이 '원래 모습'의 기준입니다. 터미널에서:

    ```text
    git diff
    ```

    **아무것도 나오지 않으면** 코드가 원래대로입니다. `sample_weight`를 더한 줄이 보이면 아직 되돌리지 않은 것입니다 — "d3_train.py를 스테이징한 모습으로 되돌려 줘"라고 시킵니다. (`git diff`는 '스테이징한 뒤 바뀐 줄'만 보여 줍니다 — 어제 배운 작업 폴더 · 스테이징 영역의 차이입니다.)

!!! info "LightGBM의 AUC가 안 오른다면"
    열이 빠진 것이 아닐 수 있습니다. 학습셋의 연체가 **12건**뿐인데 LightGBM의 기본 설정은 '잎 하나에 최소 20행'이라 그 12건을 따로 떼어 낼 수 없습니다. A2 프롬프트가 `min_child_samples`를 슬라이드의 30에서 10으로 낮추라고 한 이유입니다 — 20이나 30으로 다시 돌려 보면 `sample_weight`를 넣어도 AUC가 그대로입니다. 로지스틱은 설정과 상관없이 바로 오릅니다. 작은 표에서는 **모델 설정이 누수를 가리기도 합니다.**

---

## ⑤ 커밋 (13:45–13:50) {#a-commit1}

**커밋 메시지는 두 줄**입니다 — 첫 줄 `3일차: 무엇을 했다`, 한 줄 비우고 `왜: 이유`.

```text
3일차: 데이터 카드와 첫 모델 추가

왜: 300행 기준선과 LightGBM을 비교하고 sample_weight 누수를 직접 확인하려고
```

1. 소스 제어(++ctrl+shift+g++)에서 `workbench/day3/`의 **outputs 파일**을 골라(`+`) 메시지 칸에 위 두 줄을 쓰고 **Commit**을 누릅니다. 받은 데이터 사본(`workbench/day3/data/`)은 올리지 않아도 됩니다.
2. 허락 창이 뜨면 명령을 읽습니다 — Claude Code에게 시켰다면 **메시지가 두 줄인지**, 어느 브랜치(`d3-model`)인지 봅니다.

**13:50 점검** — 커밋이 **1개** 있고, 메시지에 `왜:` 줄이 있는지 봅니다. 10분 쉽니다.

---

## ⑥ 비용으로 정하는 임계값 (14:00–14:20) {#a-cost}

오전 시연 4의 엑셀을 **Markdown 표**로 줄인 단계입니다. 모델이 낸 확률을 **어디서 자를지**는 모델이 아니라 **비용**이 정합니다.

1. 모드는 Edit automatically(또는 Manual 그대로)로 두고 프롬프트 **A4**를 보냅니다.

    ??? example "프롬프트 A4 — 펼쳐서 복사"
        --8<-- "labs/day3/prompts.md:a4"

2. `d3_threshold.md`를 엽니다. 임계값 `0.05 … 0.50` 열 줄에 TP · FN · FP · TN · 재현율 · 정밀도 · 비용이 있고, **비용 = 5 × FN + FP**입니다. 한 줄을 손으로 계산해 봅니다(예: t = 0.5 줄의 FN과 FP로).
3. **최소 비용 t**를 찾아 이론값 **1 ÷ (1 + 5) ≈ 0.17**과 견줍니다.

!!! note "최소 비용 t가 이론값과 다르게 나와도 정상입니다"
    시험셋 연체가 4건뿐이라 비용이 **계단처럼** 움직입니다 — 한 칸이 연체 1건이라 표의 몇 줄이 같은 값일 수 있고, 최소 비용 t는 이 설정이면 0.10–0.25 근처가 나오는 사람이 많지만 시드 · 특성 · 설정에 따라 0.05나 0.30 이상이 나오기도 합니다. 이론값 0.17과의 차이를 **한 줄로 적는 것**이 오늘의 연습입니다. 실무에서는 시험셋이 아니라 **학습 기간의 월별 검증**에서 비용이 가장 낮은 지점을 고릅니다.

**14:20 점검** — `d3_threshold.md`에 열 줄 표 + 최소 비용 t + 이론값과의 차이 한 줄이 있는지 봅니다.

---

## ⑦ 놓친 바이어와 내 비용비 (14:20–14:30) {#a-fn}

1. **놓친 연체(FN) 바이어**의 `buyer_id`와 주요 특성 3개를 표로 봅니다(A4의 둘째 문장이 이미 시켰습니다). 나란히 놓고 **공통점 2줄**을 `d3_threshold.md`에 씁니다 — 오전 '한계' 장의 내용(연체 중인 바이어가 아니라 새로 연체가 시작되는 바이어를 늦게 본다)과 맞는지 생각해 봅니다.
2. **내 회사의 비용비**를 정합니다. 놓친 연체 1건이 헛경보 몇 건만큼 아픕니까? **3:1이면 t = 0.25, 10:1이면 t ≈ 0.09**입니다. 근거는 숫자 대신 **한 줄**로 씁니다(예: "우리 팀은 신규 선적을 보류하는 비용보다 미수금 손실이 훨씬 크다").
3. 같은 표를 내 비용비로 다시 만듭니다.

    ??? example "프롬프트 A4 — 내 비용비로 다시 · 펼쳐서 복사"
        --8<-- "labs/day3/prompts.md:a4-cost"

4. **무엇이 바뀌었는지 1줄**을 씁니다 — 경보 수 · 놓친 연체 수가 5:1일 때와 어떻게 다릅니까?

---

## ⑧ 트랙 확장 — 빨리 끝난 분 (14:30–14:45) {#a-tracks}

기본 트랙(①–⑦)을 끝낸 분만 이어 갑니다. 하나만 골라도 됩니다. 프롬프트는 [A5](../prompts/day3.md#a5)입니다.

| 트랙 | 하는 일 | 확인 |
|---|---|---|
| **표준** | 패널 4,017행으로 **시간 분할** 같은 실험(학습 ≤ 2025-12-31, 시험 2026-01~08) → 300행 결과와 나란히 표 | LightGBM ROC-AUC **0.97–0.98**(시험 1,084행 · 연체 61건 — 300행보다 안정) |
| **도전 ①** | class weight · SMOTE(학습셋만) 비교 — 평균 확률이 부푸는지 | `imbalanced-learn`을 `uv add`하겠다고 Claude Code가 알려 주면 읽고 승인. 막히면 class weight만 |
| **도전 ②** | 부트스트랩으로 AUC 95% 구간 · **worktree** 두 번째 작업대에서 Claude Code 병렬 | 시험 연체 4건이면 구간이 매우 넓다 |

worktree는 VS Code **소스 제어 › … › Worktrees › Create Worktree**(브랜치 `d3-smote`)로 만들고 새 창에서 Claude Code를 하나 더 엽니다(터미널에서는 `git worktree add ../tf-d3-smote -b d3-smote`). 새 폴더에는 `.venv`와 받은 파일이 없으니 `uv sync`와 `uv run python tools/get_day_files.py 3`부터 합니다.

---

## ⑨ 기대 범위 · 커밋 · push (14:45–14:50) {#a-commit}

14:45에 강사가 **'이 숫자 근처면 맞게 가고 있다'** 표를 띄웁니다. 범위 밖이면 숫자를 고치기 전에 오른쪽 칸부터 확인합니다.

| 확인할 것 | 기대 범위 | 아니면 |
|---|---|---|
| 데이터 카드 | 300행 · 연체 16 · 기준일 2개 | 파일과 인코딩 확인 |
| 시험셋(`split_suggested`) | **88행 · 연체 4** | 분할 열 확인 |
| AUC(300행) | **0.80–1.00**, 모델 · 특성마다 흔들림 | 0.99 이상 고정이면 누수 점검 |
| `sample_weight`를 넣으면 | **AUC 1.00** | 안 오르면 열이 빠졌는지 — LightGBM이면 `min_child_samples=10`이 들어갔는지도(④의 안내) |
| 패널 시간 분할 | LightGBM **0.97–0.98** | 분할 날짜 확인 |
| 비용 최소 t(5:1) | **0.1–0.25**(이론 0.17) — 계단이라 밖(0.05 · 0.30 이상)으로 나오기도 한다 | 비용식 `5 × FN + FP` |

범위 밖이면 먼저 [어디서 갈렸나](../prompts/day3.md#mismatch)를 AI에게 묻습니다.

그다음 **두 번째 커밋**을 합니다.

```text
3일차: 비용 기준 임계값 표와 내 비용비 추가

왜: 놓친 연체 1건을 헛경보 몇 건으로 볼지에 따라 경보 선이 달라지는 것을 기록하려고
```

**push**합니다 — 소스 제어의 **Publish Branch**(또는 `git push -u origin d3-model`). 허락 창에서 **push 대상이 `d3-model`**인지 읽고 승인합니다.

**14:50 점검** — 커밋이 **2개 이상**이고 `d3-model`이 GitHub에 올라갔으면 실습 A 완료입니다. 실습 B가 이 브랜치에서 이어집니다.

### 실습 A 완료 기준 {#checkpoint}

- [ ] `workbench/day3/outputs/`에 `d3_data_card.md` · `d3_train.py` · `d3_eval.md` · `d3_test_pred.csv` · `model_v1.txt` · `d3_threshold.md`가 있다
- [ ] 시험셋이 88행(연체 4)이고, 특성에 `sample_weight` · `split_suggested`가 들어가지 않았다
- [ ] `sample_weight` 누수 실험의 AUC를 봤고 코드를 원래대로 돌렸다(`git diff`)
- [ ] 최소 비용 t와 이론값 0.17의 차이 1줄, 내 비용비로 다시 한 결과 1줄이 `d3_threshold.md`에 있다
- [ ] 커밋 2개 이상 · `d3-model` push · 커밋 메시지에 `왜:` 줄이 있다

---

## 채팅 경로 — Claude Code를 못 쓸 때 {#chat-path}

Claude Code 계정이 없거나(무료 플랜은 쓸 수 없습니다) 확장이 로그인되지 않으면 **ChatGPT 또는 Claude 웹**에 CSV를 올려 **같은 문장**으로 합니다. 오늘 파일은 합성 데이터라 올려도 됩니다. 프롬프트는 [A1–A4](../prompts/day3.md#chat-path)와 같고 경로 · 저장 줄만 바꿉니다.

1. 웹 채팅에 `d3_start_features.csv`를 **첨부**하고 A1(데이터 카드) → A2(첫 모델) → A3(누수 실험) → A4(비용표)를 차례로 보냅니다. `@파일` 표기와 `workbench/…` 경로는 지웁니다. ChatGPT는 **데이터 분석** 기능이, Claude는 **코드 실행** 기능이 켜져 있어야 계산합니다. ChatGPT 무료는 하루 업로드가 3개라 `d3_start_features.csv` · `d3_start_scoring.csv` · `fx_forecast_inputs.csv`만 올립니다.
2. 대화 환경에 LightGBM이 없다는 답이 오면 **"scikit-learn의 HistGradientBoostingClassifier(min_samples_leaf=5, max_iter=200, learning_rate=0.05)로 바꿔 줘"**라고 한 줄 덧붙입니다(같은 그래디언트 부스팅 계열 — 기본값 `min_samples_leaf=20`이면 작은 표에서 `sample_weight` 누수가 보이지 않습니다).
3. **결과를 내려받아** 내 PC에서 같은 이름으로 `workbench/day3/outputs/`에 둡니다. 답에 나온 표는 Markdown으로 받아 `d3_eval.md` · `d3_threshold.md`로 저장합니다. 모델 파일(`model_v1.txt`)과 시험 예측(`d3_test_pred.csv`)도 받아 두면 실습 B-1에서 씁니다 — 못 받으면 B-1 채팅 경로가 '학습 + 점수'를 한 번에 합니다.
4. **GitHub 웹에서 올립니다.**
    1. 내 저장소 화면의 브랜치 선택(`main ▾`)에 `d3-model`을 입력하고 **Create branch**를 누릅니다.
    2. `workbench/day3/outputs/` 폴더로 들어가 **Add file → Upload files**로 결과 파일을 끌어다 놓고, 커밋 메시지 첫 줄과 설명 칸(`왜:`)을 쓴 뒤 **Commit directly to the `d3-model` branch**를 고르고 **Commit changes**.

!!! warning "GitHub 웹의 Upload files는 .gitignore를 보지 않습니다"
    고른 파일을 그대로 올립니다. 올리기 전에 파일 이름과 내용을 한 번 봅니다 — 회사 실데이터 · 키 · 실명은 올리지 않습니다.

---

## 막힐 때 {#troubleshooting}

| 증상 | 이렇게 해 보세요 |
|---|---|
| `get_day_files.py`가 "공개 전"이라고 한다 | 08:30 이후 같은 명령을 다시 실행합니다. 계속 안 되면 [3일차 → 파일 받기](index.md#files) |
| `workbench/day3/rules/d3_rules.md`가 없다 | `uv run python tools/get_day_files.py 3`을 다시 실행합니다(없는 파일을 받아 줍니다). 그래도 없으면 강사에게 |
| 계획 승인 창에서 `use auto mode`를 눌러 파일 변경이 묻지 않고 진행됐다 | 괜찮습니다. 다음부터 `2 Yes, and manually approve edits`를 고르거나 모드를 Manual로 바꿉니다. 만들어진 파일은 소스 제어의 diff로 읽어 봅니다 |
| 시험셋이 88행이 아니다 | `split_suggested`의 `train` / `test`를 그대로 썼는지 봅니다. 무작위 분할을 만들었다면 "분할은 `split_suggested` 그대로"라고 다시 지시합니다 |
| AUC가 0.99 이상으로 붙어 있다 | 누수입니다. 특성에 `sample_weight` · `buyer_id`가 있는지 봅니다 — [어디서 갈렸나](../prompts/day3.md#mismatch) 프롬프트 |
| `sample_weight`를 넣었는데 LightGBM AUC가 안 오른다 | 열이 빠졌거나, `min_child_samples`가 기본값(20)이라 연체 12건을 못 떼어 내서입니다. A2 프롬프트의 설정(10)이 코드에 들어갔는지 보고, 아니면 10으로 낮춥니다. 로지스틱은 바로 오릅니다 |
| `import lightgbm` 오류 · 패키지가 없다 | 저장소 맨 위에서 `uv sync`. 패키지를 더할 때는 Claude Code가 `uv add 이름`을 하겠다고 먼저 알려 주면 읽고 승인합니다 |
| LightGBM에서 `eval_set` 관련 경고 · 오류 | 4.7부터 검증 세트 인자가 바뀌는 중입니다. 오류 메시지 전문을 그대로 AI에게 다시 주고 판을 고정하게 합니다 |
| 그래프의 한글이 □로 나온다 | `CLAUDE.md`의 글꼴 `tools/fonts/NanumGothic-Regular.ttf`를 쓰라고 다시 지시합니다 |
| 최소 비용 t가 0.05 · 0.35처럼 이상하다 | 시험 연체가 4건이라 계단입니다. 비용식이 `5 × FN + FP`인지만 확인하고, 이론값과의 차이를 1줄로 씁니다 |
| 숫자를 AI가 '암산'한 것 같다 | "숫자는 코드로 계산한 값만 쓰고 모르면 '데이터 확인 필요'라고 써"를 다시 지시하고, 계산한 코드를 보여 달라고 합니다 |
| 허락 창이 계속 뜬다 | 읽고 `1 Yes`를 누릅니다. 모르는 명령이면 `No` 하고 "이 명령이 뭐 하는 거야?"라고 묻습니다. `2 … for this project`는 쓰지 않습니다 |
| push가 거부된다 · 로그인을 묻는다 | VS Code 왼쪽 아래 **계정 아이콘**에서 GitHub에 로그인합니다. `GH007 … private email` 오류면 `git config --global user.email`을 noreply 주소로 바꾸고 다시 커밋합니다 |
