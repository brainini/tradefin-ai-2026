# 실습 B · 6–7교시 — 뉴스 위험지수와 융합 특성표

!!! abstract "한눈에 보기 — 실습 B"
    | 항목 | 내용 |
    |---|---|
    | 목표 | 뉴스 100건을 0–10 점수로 바꿔 **검증**하고, 실습 A의 정제 표와 합친 오늘의 산출물 `d2_end_features.csv`(150행)를 **PR**로 올린다 |
    | 시간 | **15:00–16:50**(110분) · 이어서 17:00–17:20 [8교시 합치기](#period8) |
    | 오전 시연을 이렇게 따라 한다 | 시연 5(뉴스 → 구조화 점수 → 골든셋 평가 → 프롬프트 v2)를 **간소화** — API 대신 **Claude Code 세션 안에서 직접 채점**(키 불필요) · 300건 → 100건 · 골든셋은 15:35 공개 **정답 20건**. 시연 3의 시간 창 집계 · LEFT JOIN을 결합 단계에 · 시연 1의 worktree를 **두 번째 작업대**로 직접 해 보기. 수집 점검(robots.txt · 약관)은 각자 **다른 나라 사이트**로 |
    | 입력 | `data/checkpoints/d2_news.csv`(뉴스 300건, 앞 100행 사용) · `d2_news_answer.csv`(15:35) · 실습 A의 `d2_buyers_clean.csv` |
    | 도구 | VS Code(소스 제어 › Worktrees) · **Claude Code** · Claude 웹(약관 읽기) · Git · GitHub |
    | 산출물 | `news_scored.jsonl`(100줄) · `eval.md` · `수집점검.md` · **`d2_end_features.csv`(150행)** · 데이터 사전 갱신 · PR 1개 |
    | 프롬프트 | [B1](../prompts/day2.md#b1) · [약관 읽기](../prompts/day2.md#terms) · [B2](../prompts/day2.md#b2) · [B3](../prompts/day2.md#b3) · [B4](../prompts/day2.md#b4) · [B5](../prompts/day2.md#b5) · [B6](../prompts/day2.md#b6) |

AI가 매긴 점수가 **믿을 만한가**를 확인하는 것이 이 실습의 목표입니다. 점수를 만드는 것보다 **형식 검사 · 정답과 비교 · 기준일 이전 정보만**이 중요합니다.
강사가 돌아다니며 한 분씩 2–3분 확인합니다. 막히면 손을 들거나 빨간 표시를 올리세요.

## 시간표와 점검 시각 {#time}

| 시각 | 단계 | 하는 일 | 점검 |
|---|---|---|---|
| 15:00–15:10 | [① 작업대](#b-bench) | `main` 최신화 → worktree `d2-news` → 새 창 · B1 | **15:10 손 점검** — 새 창 상태 표시줄 `d2-news` |
| 15:10–15:20 | [② 수집 점검](#b-collect) | 뉴스 사이트 1곳의 `robots.txt` · 약관 → `수집점검.md` 5칸 | 결론 1줄 |
| 15:20–15:45 | [③ 채점](#b-score) | B2(1–50행 → 51–100행) → B3 검사 · 위반 행 재채점 | **15:45 JSONL 100줄 · 위반 0** |
| 15:35 | 정답 공개 | `get_day_files.py 2`를 한 번 더 — `d2_news_answer.csv`가 들어옵니다 | |
| 15:45–16:05 | [④ 평가](#b-eval) | B4 → `eval.md` + 오차 큰 2건의 원인 메모 | 숫자 3개 + 원인 2건 |
| 16:05–16:30 | [⑤ 융합](#b-join) | B5 → `d2_end_features.csv` → 데이터 사전에 새 열 | **16:30 확인표** |
| 16:30–16:50 | [⑥ 기록](#b-pr) | 확인표 대조 → 커밋 → PR(머지는 8교시) | **16:50 PR 열림** |

!!! tip "실습 A가 아직 머지되지 않았다면"
    ①에서 `main` 대신 **실습 A의 브랜치(`d2-clean`)**에서 worktree를 만들어도 됩니다. A 결과(`d2_buyers_clean.csv`)가 B5의 입력이기 때문입니다. 8교시에 두 PR을 차례로 머지합니다.

## 입력 파일 {#files}

| 파일 | 위치 | 쓰는 곳 |
|---|---|---|
| 바이어 뉴스(합성 300건) | `data/checkpoints/d2_news.csv` — 열: `news_id` · `buyer_id` · `ref_window` · `date` · `lang` · `headline` · `body_short` · `source_type`. 최신순, 앞 100행 = 2026-06-22 ~ 09-30 | ③ ⑤ |
| 뉴스 정답 20건(골든셋) | `data/checkpoints/d2_news_answer.csv` — **15:35 공개**. 열: `news_id` · `news_sent_0_10_true`(정답 점수) · `label_true`(정답 라벨) 등 | ④ |
| 채점 규칙 | `workbench/day2/prompts/news_score_v1.md`(내 저장소에 이미 있습니다) — 관점 · 척도 · 근거 · 형식 | ③ |
| 수집 점검 양식 | `workbench/day2/rules/수집점검.md`(내 저장소에 이미 있습니다) | ② |
| 실습 A 정제 표 | `workbench/day2/outputs/d2_buyers_clean.csv`(A에서 만든 것, `main`에 머지됨) | ⑤ |
| 워밍업 10건 | `labs/day2/news_warmup_10.txt` — **채팅 경로**에서 형식을 시험할 때만 | 선택 |

---

## ① 작업대 — worktree로 두 번째 폴더 (15:00–15:10) {#b-bench}

오전 시연 1처럼 **같은 저장소의 다른 브랜치를 별도 폴더**로 꺼냅니다. 실습 A의 폴더는 그대로 두고, 새 폴더에서 `d2-news` 브랜치 일을 합니다.

1. 메인 창에서 `main`으로 돌아와 실습 A의 머지를 받습니다.

    ```text
    git switch main
    git pull
    ```

2. **worktree를 만듭니다.** 왼쪽 막대 **소스 제어**(++ctrl+shift+g++)를 열고 아래 순서로 누릅니다.
    1. 소스 제어 제목줄의 `…`(Views and More Actions)에서 **Repositories**에 체크합니다(처음 한 번 — 기본은 꺼져 있습니다). 저장소 줄이 보입니다.
    2. **저장소 줄** 오른쪽의 `…` → **Worktrees** → **Create Worktree…**
    3. 맨 위 `+ Create new branch…`를 고르고 이름에 **`d2-news`**를 쓰고 Enter. 위치(Worktree path)는 **기본값 그대로** Enter.

    <figure markdown="span">
      ![VS Code 소스 제어에서 worktree를 만드는 세 장면 — 저장소 줄의 … 단추, Worktrees › Create Worktree… 메뉴, 새 브랜치 이름 입력 칸](../assets/screens/d2-worktree-create.png){ width="720" loading=lazy }
      <figcaption>① 저장소 줄의 <code>…</code> → ② <code>Worktrees › Create Worktree…</code> → ③ 새 브랜치 이름 <code>d2-news</code>. 메뉴 이름은 VS Code 버전에 따라 조금 다를 수 있습니다</figcaption>
    </figure>

3. **새 창으로 엽니다.** 소스 제어의 Worktrees 목록에서 `d2-news`를 오른쪽 단추로 눌러 **Open Worktree in New Window**를 고릅니다(메뉴가 없으면 **File → Open Folder…**로 방금 만든 폴더 — `…worktrees/d2-news`를 새 창에서 엽니다). 새 창의 **왼쪽 아래 상태 표시줄에 `d2-news`**가 보여야 합니다.
4. 새 창에서 **Claude Code 패널**을 열고 모드가 **Manual**인지 봅니다. 프롬프트 **B1**을 보냅니다. 새 작업 폴더에는 `.venv`와 `.gitignore`로 뺀 받은 파일이 **없어서** 환경과 파일을 다시 만들어야 합니다 — 오전 worktree 장의 '주의'를 직접 겪는 장면입니다.

    ??? example "프롬프트 B1 — 펼쳐서 복사"
        --8<-- "labs/day2/prompts.md:b1"

    허락 창(`uv sync` · 파일 받기 명령)을 읽고 `1 Yes`합니다. 처음에는 `uv sync`에 1–2분 걸릴 수 있습니다.

!!! note "worktree가 어려우면"
    원래 폴더에서 브랜치만 만들어도 됩니다 — `git switch -c d2-news`(또는 상태 표시줄의 브랜치 이름 → `+ Create new branch…`). 새 창이 없는 대신 B1(환경 다시 만들기)은 건너뜁니다.

**15:10 손 점검** — 새 창 상태 표시줄에 `d2-news`가 보이는지 봅니다.

---

## ② 수집 점검 — 가져와도 되는가 (15:10–15:20) {#b-collect}

뉴스를 모으기 전에 **가져와도 되는 글인지**부터 봅니다. 오전에 본 순서 — **공식 API가 먼저, 스크래핑은 약관 · robots.txt · 법을 본 뒤.** 오늘은 **점검만** 하고 기사를 수집하지 않습니다.

1. 관심 바이어 **국가의 뉴스 사이트 한 곳**을 정합니다(짝과 다른 사이트로).
2. 브라우저 주소창에 `사이트주소/robots.txt`를 쳐서 봅니다. `Disallow:` 줄(막힌 경로) **3개**를 적습니다. robots.txt는 봇에게 알리는 출입 범위일 뿐, 지켰다고 **허락을 받은 것은 아닙니다.**

    <figure markdown="span">
      ![정체를 밝힌 curl로 받은 robots.txt와 Claude Code가 정리한 수집 조건 표](../assets/screens/d2-robots-conditions.png){ width="720" loading=lazy }
      <figcaption>robots.txt를 읽는 예(오전 시연 4 — 미국 SEC의 공식 데이터 창구). 허용 경로 · 금지 경로 · 요청 간격 · 정체 밝히기가 한 표로 정리됩니다</figcaption>
    </figure>

3. **이용약관**을 찾아 자동 수집 · 크롤링 · AI 학습을 금지하는 조항을 찾습니다. 약관 전문을 Claude 웹에 붙여 [약관 읽기 프롬프트](../prompts/day2.md#terms)로 **원문 그대로 인용**하게 하고, **내가 ++ctrl+f++ 로 원문에서 확인**합니다.

    ??? example "프롬프트 — 약관 읽기(Claude 웹) · 펼쳐서 복사"
        --8<-- "labs/day2/prompts.md:terms"

4. `workbench/day2/rules/수집점검.md`의 **다섯 칸**(목적 · 공식 API/RSS 유무 · robots.txt Disallow 3개 · 약관 조항 원문 · 남길 항목)을 채우고 **결론을 하나** 고릅니다 — **API 사용 / 수동 열람만 / 수집 불가.**

    <figure markdown="span">
      ![수집점검.md의 Markdown 미리보기 — 다섯 칸과 결론 선택](../assets/screens/d2-collect-check.png){ width="640" loading=lazy }
      <figcaption>채워진 수집 점검표의 예(공식 API가 있는 사이트 기준). 칸마다 근거가 있고 결론은 하나입니다</figcaption>
    </figure>

!!! warning "점검만 합니다"
    사이트에서 기사를 **수집하지 않습니다.** 로그인 · 차단을 우회하거나 기사 **본문을 복사해 저장소에 올리지 않습니다**(남기는 것은 제목 · 날짜 · 주소 · 점수). 오늘 점수화할 뉴스는 과정이 준 합성 뉴스(`d2_news.csv`)입니다.

---

## ③ 채점 — 규칙대로, 네가 직접 (15:20–15:45) {#b-score}

규칙 파일 `workbench/day2/prompts/news_score_v1.md`를 한 번 열어 읽어 봅니다 — **관점**(대금 지급 능력 · 의사만) · **척도**(0 파산 … 10 지급 위험을 낮춤) · **근거**(원문 구절 그대로) · **형식**(입력 1행 = JSON 1줄). 오전에 본 점수화 프롬프트의 뼈대와 같습니다.

<figure markdown="span">
  ![VS Code 편집기에 나란히 열린 프롬프트 파일 news_score_v1.md와 스키마 파일](../assets/screens/d2-prompt-v1.png){ width="760" loading=lazy }
  <figcaption>점수화 규칙 파일과 출력 스키마가 나란히 열린 모습(오전 시연 5). 내 저장소의 <code>news_score_v1.md</code>가 같은 모양입니다</figcaption>
</figure>

1. 프롬프트 **B2**를 보냅니다. **"네가 직접"**이 핵심입니다 — 외부 API나 키워드 규칙 스크립트로 점수를 매기게 하지 않고, Claude Code가 세션 안에서 기사를 읽고 채점합니다.

    ??? example "프롬프트 B2 — 펼쳐서 복사"
        --8<-- "labs/day2/prompts.md:b2"

2. `workbench/day2/outputs/news_scored.jsonl`이 **한 줄에 JSON 하나**로 100줄이 쌓입니다(50행씩 두 번). 한 줄은 이런 모양입니다 — 키 7개가 모두 있어야 합니다.

    ```text
    {"news_id":"N0231","buyer_id":"B017","date":"2026-08-12","news_sent_0_10":3,"label":"high","evidence":"has delayed payments by up to 60 days","confidence":0.8}
    ```

3. 프롬프트 **B3**으로 검사 스크립트를 만들고 위반 행만 다시 채점하게 합니다.

    ??? example "프롬프트 B3 — 펼쳐서 복사"
        --8<-- "labs/day2/prompts.md:b3"

**확인할 것** 검사 결과가 **100줄 · 위반 0**입니다. `evidence`가 번역 · 요약된 행이 걸러졌는지, 다시 채점한 행이 어느 줄이었는지 봅니다. 숫자 열(`news_sent_0_10`)은 0–10의 **정수**, `label`은 점수 대역(0–2 severe · 3–4 high · 5 watch · 6–10 low)과 맞아야 합니다.

!!! info "점수가 높을수록 안전합니다"
    `news_sent_0_10`은 **높을수록 안전**(0 파산 … 10 지급 위험을 낮춤)하고, **위험지수**는 `news_risk_30d = 10 − 평균`입니다. 두 말을 섞지 않습니다.

**15:45 손 점검** — JSONL 100줄 · 위반 0.

---

## ④ 평가 — 정답 20건과 비교 (15:45–16:05) {#b-eval}

사람이 정답을 단 20건과 비교해 **AI 점수가 얼마나 맞는지** 숫자로 봅니다. 일관성이 정확성은 아닙니다 — 같은 점수를 늘 내도 틀릴 수 있습니다.

1. **15:35 이후** 터미널에서 파일 받기를 한 번 더 합니다. `d2_news_answer.csv`가 `data/checkpoints/`에 들어옵니다.

    ```text
    uv run python tools/get_day_files.py 2
    ```

2. 프롬프트 **B4**를 보냅니다.

    ??? example "프롬프트 B4 — 펼쳐서 복사"
        --8<-- "labs/day2/prompts.md:b4"

3. `workbench/day2/outputs/eval.md`에 세 숫자와 오차 큰 2건이 있는지 봅니다.

    | 지표 | 뜻 | 읽는 법 |
    |---|---|---|
    | **MAE** | AI 점수와 정답 차이의 절댓값 평균 | 1.0이면 평균 1점 차이 |
    | **±2 이내 비율** | 차이가 2점 이하인 건의 비율 | 실무 허용 오차 안의 비율 |
    | **라벨 일치율** | severe · high · watch · low가 같은 비율 | 경보 단위의 정확도 — 다수 범주(low)에 속기 쉽습니다 |

4. **오차가 가장 큰 2건**의 원문을 읽고 **왜 틀렸는지**(국가 · 업황 기사인가, 점수가 가운데로 몰렸나, 근거를 잘못 읽었나) `eval.md` 끝에 메모합니다. 8교시 결과 공유에서 씁니다.

    <figure markdown="span">
      ![시연 5 결과 — 채점 결과 JSONL 앞 다섯 줄과 프롬프트 v1과 v2의 평가표 비교](../assets/screens/d2-jsonl-eval.png){ width="760" loading=lazy }
      <figcaption>채점 JSONL과 평가표의 예(오전 시연 5). 표본이 작아 같은 프롬프트도 잴 때마다 숫자가 조금씩 달라집니다</figcaption>
    </figure>

!!! note "숫자가 나쁘면"
    실패가 아니라 **프롬프트 v2를 만들 이유**입니다. 오차의 공통점을 찾아 규칙 **한 줄**만 고치고(`news_score_v2.md`) 같은 정답으로 다시 재면 됩니다 — 한 번에 한 줄씩 고쳐야 어느 줄이 효과였는지 압니다. 다 했으면 아래 [다 했으면](#extend) ④.

---

## ⑤ 융합 — 30일 창 집계 · LEFT JOIN (16:05–16:30) {#b-join}

뉴스를 **바이어별로 30일 창**으로 모아 실습 A의 정제 표 옆에 붙입니다. 오전 특성 공학의 마지막 그림 — 바이어 × 기준일 한 줄.

1. 프롬프트 **B5**를 보냅니다.

    ??? example "프롬프트 B5 — 펼쳐서 복사"
        --8<-- "labs/day2/prompts.md:b5"

    - 창은 `(2026-08-01, 2026-08-31]` — **9월 기사가 섞이면** 기준일 뒤 정보가 특성에 들어간 것입니다(시점 정합성).
    - 뉴스가 없는 바이어는 **평균 5 + `no_news_flag=1`**로 채워 행이 사라지지 않게 합니다. 5는 척도의 가운데 값이자 경계 칸이라 **플래그 없이 쓰면 위험 쪽으로 읽힐 수 있습니다.**
    - 결합 뒤 행이 150이 아니면 키가 중복된 것입니다 — LEFT JOIN 전에 뉴스 쪽을 **바이어별로 먼저 집계**했는지 봅니다.

2. 결과 `workbench/day2/outputs/d2_end_features.csv`를 열어 봅니다(Rainbow CSV 확장이 있으면 열마다 색이 다릅니다).

    <figure markdown="span">
      ![바이어별 30일 뉴스 특성 CSV와 아래 터미널의 검증 줄 — 창 안 기사 46건, 바이어 37곳, 9월 기사 제외](../assets/screens/d2-news-features.png){ width="720" loading=lazy }
      <figcaption>30일 창 집계의 예(오전 시연 5의 바이어별 뉴스 특성). 아래 검증 줄이 창 · 건수 · 중복을 한 번에 확인합니다</figcaption>
    </figure>

3. `workbench/day2/data/데이터사전.md`에 **새 열**(`overdue_usd` · `cum_dpd_days` · `news_cnt_30d` · `news_sent_0_10_30d` · `news_sent_min_30d` · `news_risk_30d` · `no_news_flag`)을 적습니다. 초안은 AI에게 받아도 되지만 **'시점 점검' 칸은 내가 씁니다.**

    ??? example "프롬프트 B5 이어서 — 데이터 사전 초안 · 펼쳐서 복사"
        --8<-- "labs/day2/prompts.md:b5-dict"

**16:30 확인표**를 엽니다. 평가 숫자는 사람마다 다르게 나오는 것이 정상이니, **구조가 맞는지**를 봅니다.

??? success "실습 B 확인표 — 16:30에 엽니다"
    | 확인 | 기대값 |
    |---|---|
    | 채점 결과 | 100줄 = 입력 100행 · 형식 위반 0 |
    | 30일 창 | 기사 46건 · 바이어 37곳 · 9월 기사 0건 |
    | 결합 결과 | 150행 · `buyer_id` 첫 열 · `late_30d` 끝 열 · ID 중복 0 |
    | 뉴스 평균 | `news_sent_0_10_30d` ≈ 5.4(내 점수에 따라 조금 다름) |
    | B001 | 뉴스 0건 → 5.0 · `no_news_flag` 1 |
    | 평가 | MAE · ±2 비율 · 일치율 + 오차 원인 2건 |

    - 30일 창이 8월 1일 초과 · 8월 31일 이하면 기사 46건 · 바이어 37곳이 잡히고 **9월 기사는 0건**이어야 합니다.
    - 뉴스 평균이 5.4 근처인 것은 뉴스가 없는 바이어(113곳)가 5로 채워지기 때문입니다.
    - 결합 뒤 150행이 아니면 키 중복(1:N) — 뉴스 쪽을 바이어별로 먼저 집계했는지 봅니다.
    - 평가 숫자가 나쁘면 실패가 아니라 v2를 만들 이유입니다.

---

## ⑥ 기록 — 커밋 · PR (16:30–16:50) {#b-pr}

1. 소스 제어에서 바뀐 파일을 훑어봅니다. `workbench/day2/` 안의 새 파일(`news_scored.jsonl` · `eval.md` · `수집점검.md` · `d2_end_features.csv` · `데이터사전.md`)과 `scripts/validate_scores.py`만 있어야 합니다. **키 · 실데이터 · 기사 본문은 없어야** 합니다.
2. 커밋합니다(메시지는 첫 줄 · 빈 줄 · `왜:` 줄).

    ```text
    2일차: 뉴스 100건 점수화와 융합 특성표 추가

    왜: 뉴스를 기준일 이전 30일 창으로 집계해 정제 표에 붙이려고
    ```

3. push하고(**Publish Branch**) **PR을 엽니다.** 본문에 무엇을 했는지 · 확인한 값(150행 · 9월 기사 0건 · 평가 숫자) · 오차가 큰 2건의 원인을 씁니다. **머지는 8교시에** 합니다.

**16:50 PR 열림** — 내 저장소에 PR 두 개(A는 머지됨, B는 열림)가 보이면 됩니다.

### 실습 B 완료 기준 {#checkpoint}

- [ ] `workbench/day2/rules/수집점검.md` 다섯 칸과 결론 하나가 있다
- [ ] `news_scored.jsonl`이 100줄이고 검사 결과 위반 0이다
- [ ] `eval.md`에 MAE · ±2 이내 비율 · 라벨 일치율과 오차 큰 2건의 원인이 있다
- [ ] `d2_end_features.csv`가 150행이고 `buyer_id`가 첫 열 · `late_30d`가 끝 열 · ID 중복 0 · 9월 기사 0건이다
- [ ] 데이터 사전에 새 열이 있다 · PR이 열렸다

## 다 했으면 {#extend}

1. **두 모델로 채점해 κ 보기** — 같은 50건을 ChatGPT와 Claude 웹으로 각각 채점하고(채팅 경로 방식), 둘 사이의 일치도(코헨 카파)를 구해 봅니다. 두 번째 채점자가 있으면 '일관성'을 볼 수 있습니다.
2. **신용평가 코멘트 점수화** — 강사가 공유하는 가상 코멘트 1–2건을 점수화합니다. 스키마에 `rating_action` · `outlook`을 더합니다(오전의 등급 조치 · 전망 · 워치).
3. **API 키가 있다면** — 구조화 출력과 배치로 300건 전체를 채점합니다(오전 시연 5의 코드 참고, 스키마는 `workbench/day2/schemas/news_score.schema.json`). `anthropic` 패키지는 기본 환경에 없으니 `uv add anthropic`이 필요합니다(Claude Code에게 시키면 더하기 전에 알려 줍니다). 키는 환경변수로만 두고 **파일 · 커밋에 쓰지 않습니다.**
4. **프롬프트 v2** — `eval.md`의 오차 큰 건에서 공통점을 찾아 `news_score_v1.md`를 복사한 `news_score_v2.md`에서 **규칙 한 줄만** 고치고, 같은 정답 20건으로 다시 평가해 비교한 뒤 커밋 메시지에 MAE 변화를 적습니다. 파일을 복사한 직후에는 `git diff --no-index news_score_v1.md news_score_v2.md`로 바뀐 줄을 봅니다(새 파일은 그냥 `git diff`에 안 나옵니다).
5. **공개 기사 5건** — 내 바이어(가명) 관련 공개 기사 5건을 **사람이 직접 열람**해 제목 · 날짜 · 주소만 `private/my_news.csv`에 적습니다(본문 복사 금지 · **커밋 금지**). 같은 프롬프트로 제목만 점수화해 봅니다.

---

## 8교시 — 두 작업을 main으로 합치기 (17:00–17:20) {#period8}

오늘 두 작업(PR A · PR B)을 `main`으로 모으고 이력을 확인합니다. **오전 시연 1의 마지막 장면을 각자 재현**합니다.

1. **셀프 리뷰 4가지** — PR B의 Files changed를 내가 먼저 봅니다: **행 수**(150) · **테스트** 통과 · **비밀값**(키 · 실데이터 없음) · **규칙 문서** 갱신.
2. **짝이 코멘트 1개**를 남기고 **반영 커밋**을 올립니다(실습 A와 같은 방법).
3. **머지합니다.** PR 화면 아래 **Merge pull request → Create a merge commit → Confirm.** 충돌이 나면(예: 두 PR이 같은 줄을 고친 경우) Claude Code에게 맡기되 **해결된 diff는 내가 읽은 뒤** 머지합니다.

    ??? example "프롬프트 B6 — 충돌이 날 때 · 펼쳐서 복사"
        --8<-- "labs/day2/prompts.md:b6"

4. **worktree를 정리합니다.** 소스 제어의 Worktrees에서 `d2-news` 작업대를 삭제하거나, 터미널에서 `git worktree list`로 경로를 확인한 뒤 `git worktree remove <경로>`를 칩니다. 새 창은 닫습니다.
5. 오늘의 이력을 봅니다.

    ```text
    git switch main
    git pull
    git log --graph --oneline -n 12
    ```

    <figure markdown="span">
      ![git log --graph 출력 — 두 갈래가 병합 커밋으로 main에 합쳐지는 그래프](../assets/screens/d2-git-graph.png){ width="720" loading=lazy }
      <figcaption>갈래 두 개가 <code>main</code>으로 합쳐진 이력의 예(오전 시연 1). 내 그래프에서는 커밋 이름이 다릅니다</figcaption>
    </figure>

**확인** — `main`에 `workbench/day2/outputs/d2_end_features.csv`가 있고, PR 두 개가 머지됐고, 이슈가 닫혔습니다.

!!! question "머지가 끝났는데 worktree를 지우지 않으면?"
    폴더와 그 안의 `.venv`가 디스크를 차지하고, 같은 브랜치를 다른 폴더에서 다시 꺼낼 때 막힙니다.

**17:20–17:35 결과 공유** — 두세 분이 화면을 보여 줍니다: 커밋 그래프 · 평가 숫자 · 오차 큰 건의 원인 하나. 이어서 정리 · 자가 점검 · 내일 예고는 [2일차 개요](index.md#tomorrow)에 있습니다.

---

## 채팅 경로 — Claude Code를 못 쓸 때 {#chat-path}

Claude Code를 못 쓰면 **Claude 또는 ChatGPT 웹**으로 같은 결과에 도착합니다. worktree 대신 GitHub 웹에서 `d2-news` 브랜치를 만들어 올립니다.

1. **채점**: 웹 채팅에 `workbench/day2/prompts/news_score_v1.md`의 내용을 붙이고, 그 아래에 `d2_news.csv`의 **1–50행**(머리글 포함)을 붙여 보냅니다. JSON Lines가 오면 이어서 **51–100행**을 같은 방식으로 보냅니다. 먼저 [워밍업 10건](https://github.com/brainini/tradefin-ai-2026/blob/main/labs/day2/news_warmup_10.txt)으로 형식을 시험해도 좋습니다. 답이 중간에 끊기면 `계속`을 보냅니다.
2. **검사 · 평가 · 결합**: 같은 채팅의 **코드 실행(Claude) 또는 데이터 분석(ChatGPT)**에 채점 JSONL · 정답 CSV(`d2_news_answer.csv`) · 실습 A의 `d2_buyers_clean.csv`를 올려 B3 · B4 · B5와 같은 요청을 합니다(경로 줄은 지우고, 결과는 "CSV · Markdown 파일로 내려받게 해 줘"). ChatGPT 무료는 하루 업로드가 적으니 Claude를 먼저 권합니다.
3. **올리기**: 내 저장소에서 브랜치 선택에 `d2-news`를 입력해 **Create branch** → `workbench/day2/outputs/`에 **Add file → Upload files**로 결과 파일을 올리고 **Commit directly to the `d2-news` branch** → **Compare & pull request**로 PR. 머지는 8교시에 합니다.
4. 유료 Claude 계정에는 데스크톱 앱의 작업 폴더 연결(Cowork)로 맡기는 길도 있습니다. **연결한 폴더의 파일은 Anthropic 클라우드에서 처리**되니 합성 데이터일 때만 씁니다.

!!! warning "GitHub 웹의 Upload files는 .gitignore를 보지 않습니다"
    고른 파일을 그대로 올립니다. 올리기 전에 파일 이름과 내용을 봅니다 — 키 · 실데이터 · 기사 본문은 올리지 않습니다.

---

## 막힐 때 {#troubleshooting}

| 증상 | 이렇게 해 보세요 |
|---|---|
| 새 창의 Claude Code가 `data/checkpoints/…` 파일이 없다고 한다 | 정상입니다 — 새 작업 폴더에는 받은 파일이 없습니다. B1(또는 `uv run python tools/get_day_files.py 2`)을 다시 실행합니다 |
| `uv sync`가 오래 걸린다 · 실패한다 | 교실 Wi-Fi가 붐비면 몇 분 걸립니다. 계속 실패하면 원래 폴더에서 `d2-news` 브랜치만 만들어 진행합니다 |
| Worktrees 메뉴가 안 보인다 | VS Code를 업데이트하거나 터미널에서 `git worktree add ../내저장소-news -b d2-news`를 쳐서 만든 뒤 그 폴더를 새 창에서 엽니다 |
| 채점이 중간에 끊기거나 줄 수가 모자란다 | 이어서 `계속`(채팅) · "51행부터 이어서 써 줘"(Claude Code). B3 검사가 빠진 행을 찾아 줍니다 |
| 점수가 대부분 5–7에 몰린다 | `news_score_v1.md`의 [척도] 앵커를 다시 읽게 하고 `애매하면 5로 뭉개지 말고 confidence를 낮춰라`를 덧붙여 다시 채점합니다 |
| `evidence`가 원문과 다르다(번역 · 요약) | B3이 잡아낸 행만 `evidence는 번역하지 말고 원문 구절 그대로 넣어라`로 다시 채점합니다 |
| 결합 뒤 150행이 아니다 | 뉴스를 바이어별로 먼저 집계(건수 · 평균 · 최솟값)한 뒤 `buyer_id`로 LEFT JOIN 했는지 봅니다 |
| 9월 기사가 섞인다 | 창 조건 `(2026-08-01, 2026-08-31]`을 확인합니다 — 8월 31일 이하만 |
| `d2_news_answer.csv`가 안 보인다 | 15:35 이후 `uv run python tools/get_day_files.py 2`를 다시 실행합니다 |
| 머지 때 충돌이 난다 | B6 프롬프트로 맡기고 **해결된 diff를 읽은 뒤** 머지합니다. 충돌 표식(`<<<<<<<`)이 남아 있으면 안 됩니다 |
