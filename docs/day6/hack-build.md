---
title: 6일차(수업판) 해커톤 단계 — H0에서 H7까지
---

<div class="tf-lab" markdown>
<span class="tf-eyebrow">6일차 · 수업판 해커톤 · 09:00–15:50 · 보스전 16:00 <span class="tf-daystate" data-tf-daystate="6"></span></span>

# 해커톤 단계 — H0에서 H7까지

<div class="tf-meta" markdown>
<span class="tf-chip tf-chip--time">아침 09:35–10:10 · 아이디어와 장비</span>
<span class="tf-chip tf-chip--time">오전 10:10–11:50 · 설계 · 첫 깃발 · 스프린트 1</span>
<span class="tf-chip tf-chip--time">오후 13:10–15:50 · 스프린트 2 · 3 · 보스전 준비</span>
<span class="tf-chip tf-chip--tool">Claude Code · Plan → Manual</span>
<span class="tf-chip tf-chip--tool">작업 안내서</span>
<span class="tf-chip tf-chip--tool">GitHub · Vercel</span>
<span class="tf-chip tf-chip--tool">Supabase(선택)</span>
</div>

<div class="tf-flow" markdown>
<div markdown><b>상황</b> (가상) 한빛정밀(주) 디지털 TF의 마지막 날. 사흘 동안 메일함 당번 로봇 · 바이어 웹앱 · 확인 기록 · 승인 대기열을 만든 최 대리(나)에게 대표님이 마지막 퀘스트를 냅니다 — "오늘은 각자 하나씩. 저녁에 제 휴대폰으로 눌러 보겠습니다." 이번에는 **퀘스트를 내가 고릅니다.**</div>
<span>→</span>
<div markdown><b>넣는 것</b> 아이디어 카드(어제 숙제) + 웹 스타터 템플릿(부품 · 가상 데이터 · 해커톤 양식 `hackathon/`) + 작업 안내서 `guide/day6_hackathon.md` + 두 줄짜리 프롬프트</div>
<span>→</span>
<div markdown><b>얻는 것</b> 운영 주소 `hack-t{조}-{번호}.vercel.app` · `SPEC.md` · `README.md` · `DEMO.md`(3분 대본) · 세이브 포인트 커밋 3개 이상 · 3분 보스전</div>
</div>

<div class="tf-lab__grid" markdown>
<div class="tf-lab__cell" markdown><span class="tf-lab__label">목표</span> 아이디어 한 장을 **운영 주소에서 눌러 볼 수 있는 웹앱**으로 만듭니다. 기능 개수가 아니라 '한 사람 · 한 순간 · 한 동작'이 끝까지 되는 것이 오늘의 승리 조건입니다 — [MVP 규칙](hack.md#mvp)</div>
<div class="tf-lab__cell" markdown><span class="tf-lab__label">어제까지와의 관계</span> 4일차의 **템플릿 → Import → 배포**, 5일차의 **DB · 서버 액션 · 사람 승인 · AI가 미리 만들기(claude -p)**를 내 아이디어에 그대로 씁니다. 새 기술은 없습니다 — **무엇을 만들지 고르는 것**이 새롭습니다</div>
</div>

<div data-tf-map></div>
</div>

!!! quote "디지털 TF 단톡방 — 오늘 10:18"

    **최 대리(나)** SPEC 다 썼습니다. 화면 9개, 기능 14개!

    **IT팀 오 주임** 오늘 퇴근은 다음 주 수요일이겠네요.

    **재무팀 한 과장** 9개 중에 대표님이 누를 건 하나입니다.

    **대표님** 하나만, 제대로.

!!! file "작업 안내서 — `guide/day6_hackathon.md`(내 해커톤 저장소 안)"

    3일차부터 쓴 방식 그대로 — 긴 규칙은 파일에, 프롬프트는 **목적**만. 다만 오늘은 사람마다 만드는 것이 달라서, 안내서에는 사양 대신 **지킬 선**(MVP 크기 · 가상 데이터 · 비밀 · 빌드 통과)과 **일하는 순서**만 있습니다. 무엇을 만들지는 내가 정합니다.

    | 누가 | 무엇을 |
    |---|---|
    | 나 | 아이디어를 고르고, 질문에 답하고, 계획과 허락 창을 읽고, **운영 주소에서 눌러 본다** |
    | AI | 안내서의 그 절대로 계획 → 만들기 → `npm run build` → 커밋 · push까지 하고, 끝에 '확인할 것' 3줄을 보여 준다 |
    | 안내서 | 오늘의 크기 · 데이터 · 비밀 · 저장 · AI 규칙을 고정해 둔다 — 열어 봐도 된다(고치지는 않는다) |

## 시작 전 확인 {#before}

<div class="tf-checklist" data-title="시작 전 확인 5가지" markdown>

- [ ] 아이디어 카드 초안(어제 숙제) — 없으면 [아이디어 씨앗](hack-ideas.md)에서 하나
- [ ] 어제와 같은 계정으로 GitHub · Vercel 로그인 · `node -v`가 `v24.22.0`
- [ ] VS Code + Claude Code 로그인 · 모드 표시가 Plan 또는 Manual(Auto면 바꿉니다)
- [ ] 휴대폰 — 운영 주소를 수시로 열어 봅니다
- [ ] 회사 실데이터 · 실명 · 실제 연락처는 어떤 AI 도구에도 넣지 않는다

</div>

이 쪽의 단축키는 Windows 기준입니다. Mac은 ++ctrl++ 대신 ++cmd++를 누르고(미리보기 ++cmd+shift+v++), 터미널 ++ctrl+grave++와 소스 제어 ++ctrl+shift+g++만 Mac에서도 ++ctrl++입니다.

## 오늘의 양식 — 스타터의 `hackathon/` {#kit}

파일 받기는 없습니다. 새 저장소를 템플릿으로 만들면 아래 양식이 이미 들어 있습니다. 양식은 **틀**이라 AI가 읽고, 결과는 저장소 맨 위의 새 파일(`SPEC.md` · `README.md` · `DEMO.md`)로 씁니다 — 아이디어 카드만 내가 직접 채웁니다.

| 파일 | 언제 | 내용 |
|---|---|---|
| `hackathon/00_idea_card.md` | H0b | 아이디어 카드 13칸 — **내가 채운다** |
| `hackathon/idea_seeds.md` | H0b | 아이디어 씨앗 40여 개(이 사이트의 [씨앗 쪽](hack-ideas.md)과 같다) |
| `hackathon/01_SPEC_template.md` | H1 | 한 장 SPEC의 틀 — AI가 이 틀로 `SPEC.md`를 쓴다 |
| `hackathon/02_CLAUDE_project.md` | H2 | `CLAUDE.md` 끝에 더할 '내 프로젝트' 절의 틀 |
| `hackathon/03_README_template.md` | H6 | README 틀 — 맨 위에 운영 주소 |
| `hackathon/04_demo_script.md` | H6 | 3분 대본 틀 · 백업 캡처 목록 |
| `hackathon/05_judging.md` | 아무 때나 | 심사 기준 · 투표 · 발표 규칙([심사 · 발표 · 투표](hack-rules.md)와 같다) |
| `hackathon/sample_data/` | H3–H4(선택) | 가상 CSV 셋 — 경비 30줄 · 방문객 20줄 · 비품 25줄 |

스타터의 `data/`(바이어 150곳 · 환율 저장본 등)와 `components/`(숫자 카드 · 표 · 배지 · 안내 상자)도 그대로 씁니다.

## 아침 · 아이디어와 장비 획득 {#morning}

<div class="tf-phase" markdown>

<span class="tf-eyebrow">아침 · 09:35–10:10 · VS Code · 오픈채팅 · GitHub · Vercel</span>

오늘의 퀘스트(아이디어)를 먼저 정하고, 쉬는 시간 뒤 해커톤의 첫 단계로 새 저장소와 운영 주소를 만든다

**목표** 09:50까지 오픈채팅에 `[아이디어]` 한 줄, 10:10까지 운영 주소가 휴대폰에서 열린다

1. 아이디어 카드 → 짝에게 1분 → `[아이디어]`(H0b)
2. 템플릿 → `hack-T{조}-{번호}` → Vercel Import → 운영 주소 → clone → `npm ci`(H0a)

**결과물** 채운 아이디어 카드 · 운영 주소(스타터 첫 화면) · 내 PC의 저장소 폴더

</div>

### H0b · 아이디어 카드 — 짝에게 1분, 오픈채팅에 한 줄 (09:35–09:50) { #h0b .step data-tool="VS Code · 오픈채팅" data-phase="아침" }

**왜** 오늘의 퀘스트를 정합니다. 카드를 남에게 1분 안에 설명해 보면 구멍이 보입니다 — "그래서 누가, 언제 여는데?" 09:50–10:00 쉬는 시간에 강사가 큰 카드에 '자르기' 답글을 답니다.

!!! me "내가 할 일"

    1. 어제 웹 저장소(`tradefin-web-…`) 창에서 ++ctrl+p++ → `00_idea_card.md`를 열어 칸을 채웁니다(메모에 써도 됩니다) — 새 저장소는 10:00 [H0a](#h0a)에서 만들고, 그때 이 카드를 붙여 넣습니다. 어제 숙제로 쓴 초안이 있으면 그대로 이어서 씁니다. 아직 없으면 [아이디어 씨앗](hack-ideas.md)에서 하나 고릅니다 — 내가 고른 씨앗도 충분히 좋은 퀘스트입니다.
    2. **09:41 짝과 2분씩** — 1분 설명, 1분 질문. 짝은 셋만 묻습니다: "누가 · 언제 여나?" "지금은 몇 분 걸리나?" "발표 때 무엇을 눌러 보여 주나?"
    3. 09:50까지 <span data-tf-link="open_chat">오픈채팅</span>에 한 줄을 올립니다(짝이면 끝에 `짝 T2-08`).

        ```text
        [아이디어] T2-07 / 앱 이름 / 한 줄
        ```

    4. 강사의 답글이 오면 카드 맨 아래에 한 줄로 옮겨 둡니다 — H1의 인터뷰가 그 크기로 줄여 줍니다.

**이 단계의 목적** 오늘 만들 것을 한 장으로 정하고, 남에게 1분 안에 설명할 수 있게 다듬습니다.

??? prompt "(선택) 프롬프트 h-idea — 아이디어가 안 떠오를 때"

    --8<-- "labs/day6/prompts_hack.md:h-idea"

!!! ok "확인할 것"

    - [ ] 카드의 '성공의 순간'이 한 문장 — 발표 때 누를 단추가 보인다
    - [ ] MVP 규칙 안 — 화면 3개 이하 · 쓰기 동작 1개 이하 · 로그인 없음 · 가상 데이터
    - [ ] 오픈채팅에 `[아이디어]` 한 줄

??? fix "아이디어가 두세 개라 못 고르겠어요"

    짝에게 둘 다 30초씩 설명하고 **짝이 더 궁금해한 쪽**을 고릅니다. 남은 것은 카드 맨 아래 '다음에 만들 것'에 적어 둡니다.

??? fix "회사 일이라 데이터가 있어야만 보여 줄 수 있어요"

    데이터는 가져오지 않습니다. 열 이름과 모양만 빌리고 값은 AI와 함께 지어냅니다 — 카드의 '데이터' 칸에 '가상 · 20줄 · 열: …'처럼 적습니다.

**획득:** 오늘의 퀘스트 — 짝이 1분 만에 알아들은 아이디어 카드 한 장

<p class="tf-check"><time>09:50</time> 오픈채팅에 [아이디어] 한 줄 — 10분 쉽니다</p>

### H0a · 장비 획득 — 새 저장소와 운영 주소 (10:00–10:10) { #h0a .step data-tool="GitHub · Vercel · 터미널" data-phase="아침" }

**왜** 오늘 저장소는 새것입니다. 어제까지의 `tradefin-web-…` 저장소와 DB는 그대로 두고, 같은 스타터로 해커톤 전용 저장소를 하나 더 만듭니다. 4일차와 같은 길 — 템플릿 → Vercel Import → **운영 주소 먼저** → clone → `npm ci`. 클라우드 배포가 먼저 되니, 내 PC의 설치가 느려도 주소는 생깁니다.

일찍 온 사람은 08:40부터 H0a를 미리 해 둬도 됩니다(선택) — 그러면 아이디어 카드도 새 저장소에 바로 쓰고, 10:00에는 [H1](#h1)부터 합니다.

!!! me "내가 할 일"

    1. GitHub에서 [`brainini/tradefin-web-starter`](https://github.com/brainini/tradefin-web-starter)를 열고 **Use this template → Create a new repository**. Owner는 나, 이름 `hack-T{조}-{번호}`(예: `hack-T2-07`), **Public**, Include all branches는 끈 채로 **Create repository**.
    2. [vercel.com](https://vercel.com) → **Add New… → Project** → 목록에서 `hack-T2-07` 옆 **Import** → 설정은 건드리지 않고 **Deploy**. 목록에 없으면 아래 막히면 첫 칸.
    3. 1–2분 뒤 축하 화면이 나오면 **Continue to Dashboard** → **Domains**에 적힌 짧은 주소(`hack-t2-07.vercel.app` 꼴)를 엽니다. 이것이 오늘의 **운영 주소**입니다 — 메모장에 붙여 둡니다.
    4. VS Code → ++ctrl+shift+p++ → `Git: Clone` → `hack-T2-07` → 부모 폴더 `C:\work` → **Open** → 폴더 **'신뢰'**. 창 제목에 `hack-T2-07`이 보이면 어제 저장소 창과 헷갈리지 않습니다.
    5. 터미널(++ctrl+grave++)에서 설치하고 점검합니다(1–3분, 와이파이에 따라 더).

        ```text
        npm ci
        npm run doctor
        ```

    6. `npm ci`가 도는 동안 [H0b](#h0b)에서 쓴 아이디어 카드를 새 저장소의 `hackathon/00_idea_card.md`(++ctrl+p++ → `00_idea_card.md`)에 붙여 넣고 ++ctrl+s++. 10:10 [H1](#h1)의 SPEC 인터뷰가 이 파일을 읽습니다.

**이 단계의 목적** 오늘 하루 고치고 올릴 내 해커톤 저장소와 운영 주소를 만듭니다.

!!! ai "AI가 하는 일"

    이 단계는 AI 없이 합니다. Vercel이 내 저장소를 받아 `prisma generate` → `next build`를 돌리고 운영 주소에 올립니다(1–2분). `npm run doctor`는 Node · 패키지 · Git · Claude Code 위치를 ✓ / ✗ 줄로 점검합니다.

!!! ok "확인할 것"

    - [ ] 운영 주소에 스타터 첫 화면과 배지 `production · <커밋 7자리> · icn1` — 휴대폰에서도 열린다
    - [ ] VS Code 창 제목에 `hack-T2-07` · 새 저장소의 `00_idea_card.md`에 내 카드 · 터미널의 `npm ci`가 끝났다
    - [ ] `npm run doctor`에 ✗ 없음(`.env 없음`은 괜찮습니다 — DB를 붙일 때만 만듭니다)

??? fix "Vercel의 Import 목록에 새 저장소가 없어요"

    4일차에 Vercel GitHub 앱을 '고른 저장소만(Only select repositories)'으로 설치해서입니다. Import 화면 아래 **Adjust GitHub App Permissions →** → Repository access에 `hack-T2-07`을 더하고 **Save** → Vercel 화면으로 돌아와 새로 고침합니다.

??? fix "주소가 `hack-t2-07-ab12cd34-….vercel.app`처럼 길어요 · 열면 Vercel 로그인을 물어요"

    배포마다 생기는 **미리보기 주소**입니다. 프로젝트의 **Domains**(또는 Settings → Domains)에 적힌 짧은 주소가 운영 주소입니다. 이름이 겹치면 `hack-t2-07-…` 꼴로 조금 길어질 수 있습니다 — Domains에 적힌 그대로 씁니다.

??? fix "`npm ci`가 10분 넘게 걸려요"

    운영 주소는 이미 생겼으니 기다리지 말고 [H1](#h1)의 SPEC 인터뷰부터 합니다 — `npm ci` 없이도 됩니다. 10:30(H3)까지 안 끝나면 GitHub의 내 저장소 → **Code → Codespaces → Create codespace**로 옮깁니다(스타터가 `npm ci`까지 해 둡니다).

??? fix "PowerShell이 'npm.ps1 … 실행할 수 없습니다'라고 해요"

    스타터는 터미널 기본값이 명령 프롬프트(cmd)입니다. 폴더를 '신뢰'했는지 보고, 터미널 오른쪽 위 `∨`에서 **Command Prompt**를 고릅니다. 급하면 `npm.cmd ci`.

**획득:** 운영 주소 — 오늘의 깃대 · 해커톤 전용 작업대(어제 저장소는 그대로)

<p class="tf-check"><time>10:10</time> 손 점검 — 운영 주소가 휴대폰에서 열리고, npm run doctor에 ✗ 없음</p>

## 오전 · 퀘스트 설계와 첫 깃발 {#forenoon}

<div class="tf-phase" markdown>

<span class="tf-eyebrow">오전 · 10:10–10:50 · Claude Code · Git · Vercel</span>

아이디어를 한 장 SPEC으로 줄이고, 기능이 없어도 운영 주소에 뼈대를 올린다

**목표** 10:50 세이브 포인트 1 — 운영 주소에 내 앱의 이름 · 쪽 이동 · 가상 예시 줄

1. SPEC 인터뷰 → `SPEC.md`(H1)
2. `CLAUDE.md`에 내 프로젝트 규칙 → 첫 커밋(H2)
3. 뼈대 → build → push → `[CP1]`(H3)

**결과물** `SPEC.md` · `CLAUDE.md`의 새 절 · 쪽 3개 이하 · 커밋 2개 이상

</div>

### H1 · 퀘스트 설계 — SPEC 인터뷰 → SPEC.md (10:10–10:25) { #h1 .step data-tool="Claude Code · Plan → Manual" data-phase="오전" }

**왜** AI는 적힌 것만 만듭니다. 질문 다섯 개에 답하면 AI가 한 쪽짜리 `SPEC.md`를 씁니다 — 시나리오는 **Given–When–Then**(이런 상황에서 · 이걸 하면 · 이게 보인다) 세 줄씩. 이 한 장이 오늘 하루 AI의 지도이고, 저녁 발표 대본의 뼈대입니다. 아이디어 카드 → **h1**(질문 5개) → 내 답 → **h1b** → `SPEC.md` → 내 손으로 고치기

!!! me "내가 할 일"

    1. 입력창 아래 모드 표시기를 **Plan**으로 바꾸고 **h1**을 보냅니다.
    2. 질문 다섯 개가 오면 번호대로 한 줄씩 답을 적습니다(메모장에 먼저 써도 됩니다). 모르는 것은 `모름`.
    3. 모드를 **Manual**로 바꾸고 **h1b**의 `{1–5}`에 내 답을 붙여 보냅니다 → 쓰기 허락 창을 읽고 `1 Yes`.
    4. `SPEC.md`를 미리보기(++ctrl+shift+v++)로 읽고 **내 손으로 고칩니다** — 특히 시나리오 1(발표 장면)의 Then과 '하지 않을 것'.

**이 단계의 목적** 내 아이디어를 오늘 안에 만들 수 있는 크기의 한 장 SPEC으로 만듭니다.

!!! prompt "프롬프트 h1 — SPEC 인터뷰(Plan · 읽기만)"

    --8<-- "labs/day6/prompts_hack.md:h1"

!!! prompt "프롬프트 h1b — SPEC.md 쓰기(빈칸 하나)"

    --8<-- "labs/day6/prompts_hack.md:h1b"

!!! ai "AI가 하는 일"

    h1 — 카드를 읽고 질문 다섯 개를 한 번에 묻습니다. 질문마다 카드에서 짐작한 예시 답이 붙고, 파일은 만들지 않습니다(10–30초). h1b — 틀대로 `SPEC.md`를 새로 씁니다(1–2분). 내 답에 없는 칸은 지어내지 않고 `(확인 필요)`로 둡니다. MVP보다 크면 줄인 안을 먼저 보여 줍니다.

!!! ok "확인할 것"

    - [ ] 시나리오 1이 Given · When · Then 세 줄이고, Then에 **눈에 보이는 결과**(숫자 · 글 · 색)가 있다
    - [ ] '하지 않을 것'이 3개 이상(로그인 · 실제 발송 · 실데이터 …)
    - [ ] 화면 3개 이하 · 쓰기 동작 1개 이하

??? ok "Given–When–Then 예 — 회의실 예약판"

    ```text
    Given 회의실 3곳이 10:00–11:00에 비어 있다
    When  10:00–11:00에 A실을 예약한다
    Then  목록에서 A실이 '예약됨'이 되고, 같은 시간 A실 예약은 막힌다
    ```

    Then이 '잘 된다'처럼 흐리면 발표에서 보여 줄 것도 흐려집니다. '무엇이 · 어떻게 보이나'로 씁니다.

??? fix "AI가 질문 없이 바로 SPEC.md를 쓰려고 해요"

    Plan 모드인지 봅니다. "질문 5개부터 — 파일은 아직 만들지 마"라고 보냅니다.

??? fix "SPEC이 너무 커요(화면 9개 · 기능 14개)"

    단톡방의 최 대리와 같습니다. [h-cut](#h-cut)으로 줄인 안부터 받습니다 — 뺀 것은 '다음 단계'로 갑니다.

**획득:** SPEC 한 장 — AI와 내가 같이 보는 오늘의 지도 · 저녁 보스전 대본의 뼈대

<p class="tf-check"><time>10:25</time> 손 점검 — SPEC.md에 시나리오 1의 세 줄과 '하지 않을 것' 3개</p>

### H2 · 규칙 새기기 — CLAUDE.md에 내 프로젝트 절 · 첫 커밋 (10:25–10:30) { #h2 .step data-tool="Claude Code · Git" data-phase="오전" }

**왜** Claude Code는 대화를 시작할 때마다 `CLAUDE.md`를 먼저 읽습니다. 맨 끝에 '내 해커톤 프로젝트' 절을 더하면 대화가 길어져도, 새 대화를 열어도 범위가 흔들리지 않습니다. `SPEC.md` → **h2** → `CLAUDE.md` 끝에 10–15줄 → 첫 세이브(커밋 · push)

!!! me "내가 할 일"

    1. **h2**를 보내고, 쓰기 허락 창에서 **더하는 줄만** 있는지 읽고 `1 Yes`.
    2. 소스 제어(++ctrl+shift+g++)에서 `SPEC.md` · `CLAUDE.md` · 아이디어 카드를 고르고 두 줄 메시지로 **Commit** → **Sync Changes**(push). Claude Code에 맡기려면 [h-save](#h-save).

        ```text
        6일차: 해커톤 SPEC과 내 프로젝트 규칙 추가

        왜: 오늘 만들 것과 하지 않을 것을 AI와 내가 같은 한 장으로 보려고
        ```

**이 단계의 목적** 오늘 하루 AI가 매번 지킬 내 프로젝트 규칙을 남기고, 첫 세이브를 합니다.

!!! prompt "프롬프트 h2 — 내 프로젝트 규칙"

    --8<-- "labs/day6/prompts_hack.md:h2"

!!! ok "확인할 것"

    - [ ] `CLAUDE.md` 맨 끝에 `## 내 해커톤 프로젝트` — 위쪽 줄은 그대로(diff에 초록 줄만)
    - [ ] 마지막 줄이 "끝날 때마다 `npm run build` 통과 + SPEC의 확인 기준 3줄"
    - [ ] 커밋 1개 · push 됨(GitHub 저장소에 `SPEC.md`가 보인다)

??? fix "CLAUDE.md의 위쪽 줄까지 바뀌었어요"

    허락 창이면 `No` → "이미 있는 줄은 고치지 말고 끝에 절 하나만 더해"라고 다시 보냅니다. 이미 저장됐다면 소스 제어에서 `CLAUDE.md`의 diff를 열어 바뀐 줄을 봅니다 — "CLAUDE.md는 끝에 더한 절만 남기고 나머지는 원래대로 되돌려"라고 보냅니다.

**획득:** 내 프로젝트 규칙 — 새 대화를 열어도 AI가 기억하는 오늘의 범위 · 첫 세이브

<p class="tf-check"><time>10:30</time> 커밋 1개 — SPEC.md · CLAUDE.md</p>

### H3 · 첫 깃발 — 뼈대 배포 · 세이브 포인트 1 (10:30–10:50) { #h3 .step data-tool="Claude Code · Plan · Vercel" data-phase="오전" }

**왜** 기능보다 주소가 먼저입니다. 껍데기라도 운영 주소에 떠 있으면 나머지 하루는 '고치고 다시 올리기'의 반복이 됩니다 — 빌드가 깨져도 마지막으로 성공한 배포는 살아 있습니다. `SPEC.md`의 화면 목록 → **h3**(Plan) → 쪽 3개 이하 → build → push → 운영 주소 → `[CP1]`

!!! me "내가 할 일"

    1. 모드 **Plan** → **h3** → 계획에서 **만들 쪽 · 지울 것(스타터 바이어 홈) · 바닥 글**을 읽고, 승인 창에서 `2 Yes, and manually approve edits`.
    2. 허락 창을 읽으며 승인합니다 → `npm run build` 통과 → 커밋 · push 허락 창(파일 목록 · 메시지 · `main`)을 읽고 승인.
    3. Vercel 프로젝트의 **Deployments**에서 새 배포가 **Ready**가 되면(1–2분) 운영 주소를 휴대폰으로 엽니다.
    4. 10:50까지 오픈채팅에 한 줄 → 옆자리 버디와 2분, 서로의 주소를 휴대폰으로 엽니다.

        ```text
        [CP1] T2-07 / https://hack-t2-07.vercel.app
        ```

**이 단계의 목적** 기능이 없어도 내 주소에서 열리는 뼈대를 먼저 배포합니다(세이브 포인트 1).

!!! prompt "프롬프트 h3 — 뼈대와 첫 배포(Plan)"

    --8<-- "labs/day6/prompts_hack.md:h3"

!!! ai "AI가 하는 일"

    계획(만들 쪽 · 바꿀 파일)을 먼저 보여 주고, 승인하면 홈을 내 앱의 첫 화면으로 바꾸고 쪽 3개 이하 · 쪽 이동 · 빈 상태와 가상 예시 줄 · 바닥 글 "(가상) 데이터 · 해커톤 시제품"을 만듭니다. 배포 배지는 첫 화면 아래에 남깁니다. `npm run build` → 커밋 · push까지 3–6분, 허락 창 4–8번.

!!! ok "확인할 것"

    - [ ] 운영 주소 첫 화면에 내 앱 이름 · 한 줄 · 쪽 이동 · 가상 예시 줄
    - [ ] 배지가 `production · <방금 커밋 7자리> · icn1` — 새 배포가 올라왔다
    - [ ] 오픈채팅에 `[CP1]` 한 줄

??? ok "세이브 포인트 1 — 이 정도면 충분합니다"

    제목 · 한 줄 · 빈 표 · '곧 열려요' 단추 — **기능 0개여도 통과**입니다. 지금 중요한 것은 push하면 운영 주소가 바뀐다는 고리가 도는 것입니다.

??? fix "내 PC에서는 되는데 Vercel 빌드만 실패해요"

    Vercel의 그 배포 → **Building** 로그 끝 10줄을 복사해 [h-fix](#h-fix)로 보냅니다. 가장 흔한 원인은 **파일 이름 대소문자**(Windows는 구별하지 않고 Vercel은 구별합니다)와 커밋하지 않은 파일입니다.

??? fix "push했는데 운영 주소가 그대로예요"

    Deployments에 새 배포가 있는지 봅니다 — **Building**이면 1–2분 기다리고, **Error**면 마지막 성공 배포가 그대로 떠 있는 것입니다(위 칸). 새 배포가 아예 없으면 push가 안 된 것입니다 — 소스 제어의 **Sync Changes**를 누릅니다.

??? fix "아침에 Vercel Import를 못 했어요"

    지금 [H0a](#h0a)의 1–3번만 합니다(3분). 그다음 이 단계의 3번부터.

**획득:** 첫 깃발 · 세이브 포인트 1 — 기능 0개여도 세상에 걸린 내 주소

<p class="tf-check"><time>10:50</time> 세이브 포인트 1 — 운영 주소에 뼈대 · 오픈채팅 [CP1]. 10분 쉽니다</p>

## 스프린트 · 시나리오 하나씩 {#sprint}

<div class="tf-phase" markdown>

<span class="tf-eyebrow">스프린트 1 · 2 · 11:00–14:20 · Claude Code · Vercel · Supabase(선택)</span>

Given–When–Then 하나 → build → push → 운영 주소에서 확인 — 이 고리를 돌 때마다 앱이 한 칸 자란다

**목표** 14:20 세이브 포인트 2 — 시나리오 1이 운영 주소에서 끝까지(휴대폰에서도)

1. 시나리오 1(발표 장면) → 되면 2 · 3
2. (선택) DB · AI가 미리 만든 결과 · 자유 퀘스트 '와!' 하나
3. 11:30 오피스아워 A · 13:00 이론 2 · 13:40 오피스아워 B

**결과물** 시나리오마다 커밋 1개 이상 · `SPEC.md`의 `[됨]` 표시

</div>

### H4 · 시나리오 하나씩 — 스프린트 1 · 2 · 세이브 포인트 2 (11:00–14:20) { #h4 .step data-tool="Claude Code · Plan · Vercel" data-phase="스프린트" }

**왜** 한 번에 다 만들면 어디서 깨졌는지 모릅니다. 시나리오 하나 → build → push → 운영 주소에서 Given–When–Then 확인 — 이 고리를 짧게 여러 번 돕니다. **시나리오 1(발표 장면)이 운영 주소에서 끝까지 되기 전에는 2로 넘어가지 않습니다.** `SPEC.md`의 시나리오 → **h4** → build → push → 운영 주소 → `[됨]`

!!! me "내가 할 일"

    1. 모드 **Plan** → **h4**의 `{번호}`를 `1`로 바꿔 보냅니다 → 계획 3–7줄(바꿀 파일 · 데이터 · 확인 방법)을 읽고 승인.
    2. 허락 창을 읽으며 승인 → build → 커밋 · push.
    3. AI가 준 **확인 방법 3줄**대로 운영 주소에서 눌러 봅니다 — 휴대폰으로도. 되면 `SPEC.md`의 시나리오 1 옆에 `[됨]`이 붙었는지 봅니다.
    4. 다음은 `{번호}` = 2, 또는 아래 카드 가운데 하나. 안 되면 오류 끝 10줄로 [h-fix](#h-fix).
    5. **14:20까지** 오픈채팅에 한 줄 → 버디와 2분.

        ```text
        [CP2] T2-07 / https://hack-t2-07.vercel.app / 된 시나리오 1
        ```

**이 단계의 목적** SPEC의 시나리오를 하나씩, 운영 주소에서 끝까지 되게 만듭니다.

!!! prompt "프롬프트 h4 — 시나리오 하나씩(빈칸 하나)"

    --8<-- "labs/day6/prompts_hack.md:h4"

!!! ai "AI가 하는 일"

    시나리오 하나만 계획합니다 — 바꿀 파일 · 데이터 · 운영 주소에서 확인하는 법. 쓰기 동작이면 서버 액션과 입력 검사(빈칸 · 길이 · 숫자 범위 → 한국어 안내)를 넣습니다. 저장은 안내서 「5. 데이터」의 결정대로(파일 · 브라우저 저장 · DB). 한 시나리오에 5–15분, build가 통과한 뒤에만 '완료'라고 합니다.

**시나리오 1이 되면 — 골라서 하나 더**(선택 · 하나씩)

<div class="grid cards tf-ext tf-promptlib" markdown>

-   <span class="tf-level">선택 · 저장이 핵심일 때 · 25분</span>

    **DB 붙이기 — 여러 사람이 같이 보는 기록**

    **이런 앱** 예약 · 신청 · 투표 · 방문 등록처럼 다른 사람의 휴대폰에서도 같은 기록이 보여야 할 때. 내 기기에서만 남으면 되면 DB 없이 브라우저 저장으로 충분합니다.

    --8<-- "labs/day6/prompts_hack.md:h-db"

    **먼저 내가 할 일** 아래 '[DB를 붙이는 순서](#db-steps)'의 1–4번(새 Supabase 프로젝트 · `.env`)

-   <span class="tf-level">선택 · AI가 미리 · 20분</span>

    **AI가 미리 만든 결과 싣기**

    **이런 앱** 가상 문의 50건을 유형별로 · 회의록에서 할 일 뽑기 · 메모 요약처럼 AI가 읽고 정리한 결과가 핵심일 때. 앱 안에는 키가 없습니다 — 5일차 초안 로봇과 같은 방식입니다.

    --8<-- "labs/day6/prompts_hack.md:h-ai"

    **끝난 뒤 내가 할 일** 터미널에서 `npx tsx scripts/ai-batch.ts --dry-run` → `npx tsx scripts/ai-batch.ts`

-   <span class="tf-level">자유 퀘스트 · 15–30분</span>

    **내 마음대로 키우기 — '와!' 하나**

    **씨앗 한 줄**(키 없이 되는 것이 많습니다)

    - 말로 받아 적는 메모 단추 — 브라우저가 듣는다(크롬 권장)
    - 결과를 소리 내어 읽어 주는 단추 — 브라우저가 말한다
    - 휴대폰을 흔들면 돌아가는 룰렛 · 점수판(게임)
    - 마감 10분 전 브라우저 알림 + 소리(PC 브라우저만 — 휴대폰 알림은 아래 .ics 캘린더로)
    - D-day를 내 휴대폰 캘린더로(.ics 내려받기)
    - A4 한 장으로 인쇄 · PDF 저장 단추

    --8<-- "labs/day6/prompts_hack.md:h-wow"

-   <span class="tf-level">아무거나 · 15분</span>

    **가장 놀라운 것 3가지**

    무엇을 더할지 떠오르지 않으면 AI에게 먼저 제안받습니다. 셋 다 마음에 안 들면 "다른 3개".

    --8<-- "labs/day6/prompts_hack.md:h-any"

</div>

!!! ok "확인할 것"

    - [ ] 시나리오 1이 **운영 주소에서** Given → When → Then 끝까지 — 휴대폰에서도
    - [ ] `SPEC.md`의 시나리오 1 옆에 `[됨]` · 시나리오마다 커밋이 있다
    - [ ] 14:20까지 오픈채팅에 `[CP2]` 한 줄

<a id="db-steps"></a>

??? me "DB를 붙이는 순서 — h-db 앞뒤로 내가 할 것"

    5일차 실습 C와 같은 길을 짧게 갑니다. **5일차 DB는 쓰지 않습니다** — 그 DB에 표를 밀어 넣으면 5일차 표가 지워질 수 있습니다.

    1. [supabase.com](https://supabase.com) → **New project** — 이름 `hack-T2-07` · 비밀번호 **영문 + 숫자 16자 이상(기호 없음)** — 내 메모에만 적습니다 · Region **Northeast Asia (Seoul)**. 무료 2개 한도에 걸리면 5일차 프로젝트를 **Pause**합니다.
    2. 프로젝트가 준비되면 **Connect → ORMs → Prisma**의 두 줄(`DATABASE_URL` 6543 · `DIRECT_URL` 5432)을 복사합니다.
    3. 터미널에서 `npm run env:init` → ++ctrl+p++ → `.env`를 엽니다. 빈 `DATABASE_URL=""` · `DIRECT_URL=""` 두 줄을 지우고 그 자리에 복사한 두 줄을 붙여 넣은 뒤, `[YOUR-PASSWORD]` 두 군데를 내 비밀번호로(대괄호까지 지우고) 바꿔 ++ctrl+s++로 저장합니다.
    4. `npm run doctor:db` — 두 줄 모두 '연결 OK'.
    5. 모드 Plan → **h-db** → 계획 읽고 승인 → `npm run db:push` 허락 → 'RLS 켬' 줄 확인 → (처음 데이터가 있으면) `npm run db:seed`.
    6. 배포: Vercel 프로젝트 **Settings → Environment Variables** → 이름 `DATABASE_URL` · 값은 `.env`의 `DATABASE_URL=` 줄(6543)에서 **따옴표 안만** → **Save** → **Deployments → 맨 위 배포의 … → Redeploy**. `DIRECT_URL`은 넣지 않습니다(내 PC의 표 만들기용).
    7. 운영 주소에서 하나 쓰고 → 휴대폰에서 새로 고침 → 같은 기록이 보이면 성공.

??? me "AI가 미리 만든 결과 — h-ai 뒤에 내가 할 것"

    1. (처음 한 번) 내 PC의 Claude Code를 찾는지 봅니다 — `npx tsx scripts/lib/ask-claude.ts --check`가 `pong`으로 끝나면 됩니다. 못 찾으면 `npm run doctor`의 안내대로.
    2. 터미널에서 먼저 연습 — AI를 부르지 않고 몇 건을 처리할지와 첫 프롬프트만 봅니다.

        ```text
        npx tsx scripts/ai-batch.ts --dry-run
        ```

    3. 진짜 실행(1–3분). 다시 돌려도 이미 만든 건은 건너뜁니다.

        ```text
        npx tsx scripts/ai-batch.ts
        ```

    4. 생긴 `data/ai_….json`을 열어 몇 건을 **내 눈으로** 확인합니다 — 이상한 것은 '확인 필요'로 바꾸게 합니다. 화면에 "AI가 미리 만든 결과 · 사람 확인 전"이 보이는지 보고 커밋 · push.

??? fix "운영 주소에서만 500 오류가 나요"

    환경 변수가 없거나, 넣은 뒤 **Redeploy**를 안 했거나, 값에 따옴표(`"`)까지 들어간 경우가 대부분입니다. Vercel 프로젝트 → **Logs**의 빨간 줄을 [h-fix](#h-fix)로 보냅니다.

??? fix "빌드가 `'use client'` · `server-only` · `fs` 오류로 깨져요"

    브라우저로 가는 부품(`'use client'`)이 데이터 파일 · DB · 비밀을 불러온 것입니다. "이 값은 서버 쪽에서 읽어 props로 넘기게 고쳐 — CLAUDE.md 2번대로"라고 보냅니다.

??? fix "화면이 깜빡이며 'Hydration' 오류가 나요"

    화면 부품에서 현재 시각(`Date`)이나 `Math.random`을 쓴 것입니다. "시각 · 무작위 값은 서버에서 정해 props로 넘기거나, 단추를 누른 뒤에 만들게 고쳐"라고 보냅니다.

??? fix "말하기 · 듣기 · 카메라 단추가 아무 일도 안 해요"

    브라우저가 허락을 물었는지 봅니다 — 주소창 왼쪽 자물쇠 → 마이크 · 카메라 **허용**. 받아쓰기(음성 인식)는 크롬에서 가장 잘 되고(엣지는 오류가 나기도 합니다), 파이어폭스는 아직 지원하지 않습니다. 운영 주소(https)와 `localhost`에서만 켜집니다. 받아쓰기는 소리가 브라우저 회사 서버를 거칠 수 있으니 실데이터는 말하지 않습니다.

??? fix "사용 한도에 걸렸어요"

    입력창에 `/model` → Sonnet으로 바꾸거나 새 대화로 시작합니다("SPEC.md와 CLAUDE.md를 읽고 시나리오 2부터 이어서"). 풀릴 때까지는 짝의 화면으로 README · 대본을 먼저 씁니다.

**획득:** 장면 완성 · 세이브 포인트 2 — 대표님 휴대폰에서도 끝까지 되는 시나리오 1

<p class="tf-check"><time>14:20</time> 세이브 포인트 2 — 시나리오 1이 운영 주소에서 끝까지 · 오픈채팅 [CP2]. 10분 쉽니다</p>

## 오후 · 광내기와 마지막 점검 {#afternoon}

<div class="tf-phase" markdown>

<span class="tf-eyebrow">스프린트 3 · 14:30–15:30 · Claude Code · 브라우저 · Git</span>

기능은 그대로 두고 첫인상을 다듬고, README와 3분 대본을 쓰고, 비밀 · 실명 0건을 확인해 얼린다

**목표** 15:30 세이브 포인트 3 = 코드 프리즈 — 이후에는 README · 오타만

1. 390 폭에서 다듬기(H5)
2. README · 3분 대본(H6) · 15:05 오피스아워 C
3. 게시 전 점검 → 마지막 push(H7)

**결과물** 다듬은 화면 · `README.md` · `DEMO.md` · 점검 FAIL 0 · 마지막 커밋

</div>

### H5 · 광내기 — 발표 화면 다듬기 (14:30–14:50) { #h5 .step data-tool="Claude Code · 브라우저" data-phase="오후" }

**왜** 기능은 그대로, 첫인상만 바꿉니다. 대표님은 휴대폰으로 엽니다 — 심사의 '390px에서 잘 보이는가'와 '전달'이 여기서 갈립니다. 3일차 실습 D에서 지운 'AI 티'(이모지 · 보라 그라데이션 · 무지개 막대)도 다시 확인합니다.

!!! me "내가 할 일"

    1. 운영 주소를 연 브라우저에서 ++f12++ → ++ctrl+shift+m++(기기 툴바) → **iPhone 12 Pro**(폭 390)를 고르고, 밀리는 곳 · 겹치는 글자 · 첫 화면에서 안 보이는 발표 장면을 찾습니다.
    2. **h5**의 `{한 줄}`에 찾은 곳을 적어 보냅니다(예: "첫 화면에서 예약 단추가 스크롤 아래에 있다").
    3. 허락 창 → build → push → 휴대폰으로 다시 봅니다.

**이 단계의 목적** 발표 화면을 공들인 것처럼 다듬습니다 — 기능과 숫자는 그대로.

!!! prompt "프롬프트 h5 — 다듬기(모양만)"

    --8<-- "labs/day6/prompts_hack.md:h5"

!!! ok "확인할 것"

    - [ ] 390 폭에서 가로로 밀리는 곳 · 겹치는 글자가 없다
    - [ ] 첫 화면 맨 위에 앱 이름 · 한 줄 · 발표 장면의 단추나 숫자
    - [ ] 이모지 · 보라 그라데이션 · 뜻 없는 아이콘이 없고, '(가상)' 표시가 보인다

??? fix "다듬었더니 기능이나 숫자가 바뀌었어요"

    "기능과 숫자는 다듬기 전으로 되돌리고 모양만 고쳐"라고 보내고, 소스 제어의 diff로 계산 줄이 바뀌었는지 봅니다.

**획득:** 광낸 첫 화면 — 390 폭에서도 반듯한 발표 장면

<p class="tf-check"><time>14:50</time> 손 점검 — 휴대폰에서 첫 화면에 발표 장면</p>

### H6 · 보스전 대본 — README와 3분 대본 (14:50–15:15) { #h6 .step data-tool="Claude Code · 타이머" data-phase="오후" }

**왜** 낯선 사람이 README만 보고 눌러 볼 수 있으면 '전달' 4점입니다. 대본은 3:00 — 문제(누가 · 언제 · 무엇이 불편)부터 20초 안에. 'AI가 한 일 / 내가 검증한 것'은 **내 말로** 답합니다 — 그 칸은 AI가 지어내지 않습니다.

!!! me "내가 할 일"

    1. **h6**을 보냅니다. AI가 두 가지를 물어 오면 내 말로 답합니다 — ① AI가 한 일과 내가 직접 확인한 것 ② 우리 회사에 들인다면(누가 · 숫자 하나로 본 효과 · 위험 하나).
    2. 스타터 README를 덮어써도 되는지 물으면 "덮어써"라고 답하고, 허락 창을 읽고 승인합니다.
    3. `DEMO.md`를 소리 내어 한 번 읽습니다 — 휴대폰 타이머 3:00. 넘치면 시연 단계를 줄입니다.
    4. 15:05 오피스아워 C(발표 · README)를 화면으로 봅니다.

**이 단계의 목적** 3분 발표 대본과 README를 사실대로 채웁니다.

!!! prompt "프롬프트 h6 — README · 3분 대본"

    --8<-- "labs/day6/prompts_hack.md:h6"

!!! ok "확인할 것"

    - [ ] `README.md` 맨 위에 운영 주소 · 시연 순서 3단계 · '데이터는 모두 가상'
    - [ ] `DEMO.md`가 3:00 안 — 0:20까지 문제와 누구, 2:10까지 시연, 2:40까지 AI가 한 일 / 내가 검증한 것
    - [ ] 백업 캡처 3장의 이름(시나리오 1의 Given · When · Then 화면)이 대본에 있다

**획득:** 3분 대본 — 낯선 사람도 눌러 보는 README · 소리 내어 3:00 안

<p class="tf-check"><time>15:15</time> 손 점검 — README 맨 위 운영 주소 · 대본 소리 내어 3:00 안</p>

### H7 · 마지막 점검 — 비밀 · 실명 0 · 세이브 포인트 3 = 코드 프리즈 (15:15–15:30) { #h7 .step data-tool="Claude Code · 터미널 · 시크릿 창" data-phase="오후" }

**왜** 운영 주소는 공개입니다 — 링크를 받은 누구나 엽니다. 비밀 · 실명 · 실제 연락처가 0건인지 **기계로** 확인하고, 15:30에 얼립니다. 얼린 뒤에는 README와 오타만 고칩니다 — 발표 직전의 '마지막 한 줄'이 앱을 깨뜨리는 일을 막습니다.

!!! me "내가 할 일"

    1. **h7**을 보내고 결과 표를 읽습니다. FAIL이 있으면 AI의 고치는 법을 읽고 승인합니다.
    2. 마지막 커밋 · push → Vercel **Ready** → **시크릿 창**과 휴대폰에서 운영 주소를 엽니다.
    3. 15:30부터는 코드를 고치지 않습니다(README · 오타만).

**이 단계의 목적** 공개 주소에 비밀 · 실명이 없는지 마지막으로 점검하고 얼립니다.

!!! prompt "프롬프트 h7 — 게시 전 점검"

    --8<-- "labs/day6/prompts_hack.md:h7"

!!! ok "확인할 것"

    - [ ] `npm run doctor:secrets` **FAIL 0**(WARN은 이유 한 줄)
    - [ ] 시크릿 창에서 운영 주소가 로그인 없이 열린다
    - [ ] 마지막 커밋이 15:30 전 · 배지의 커밋 7자리가 GitHub의 마지막 커밋과 같다

??? fix "WARN — 'example이 아닌 이메일'이 걸렸어요"

    가상 데이터에 실제처럼 보이는 주소가 들어간 것입니다. "이메일은 모두 @….example 꼴의 가상 주소로 바꿔"라고 보냅니다.

??? fix "키나 비밀번호를 커밋해 버렸어요"

    지워서 다시 커밋해도 **이력에 남습니다.** 그 키 · 비밀번호부터 폐기하고 새로 만듭니다(Supabase는 Database Settings → Reset password, 그다음 `.env`와 Vercel 두 곳을 고칩니다). 강사에게 바로 알리고, `push --force`는 하지 않습니다.

**획득:** 코드 프리즈 · 세이브 포인트 3 — 비밀 · 실명 0건, 보스전 입장권

<p class="tf-check"><time>15:30</time> 세이브 포인트 3 — 코드 프리즈 · FAIL 0 · 시크릿 창에서 열림</p>

## 보스전 준비 — 리허설 · 백업 · [발표] (15:30–15:50) {#rehearsal}

<div class="tf-checklist" data-title="보스전 전에 4가지" markdown>

- [ ] 짝(버디)과 3:00 타이머로 한 번씩 — 듣는 사람은 "첫 20초에 누가 · 무엇이 불편한지 들렸나?"만 말해 준다
- [ ] 백업 캡처 3장(시나리오 1의 Given · When · Then 화면) — 와이파이가 끊겨도 발표는 합니다. (선택) 60초 화면 녹화
- [ ] 15:45까지 오픈채팅에 `[발표] T2-07 / 별명 / 한 줄 / https://hack-t2-07.vercel.app`
- [ ] 발표 순서 · 심사 기준 · 투표 → [심사 · 발표 · 투표](hack-rules.md)

</div>

!!! late "늦었다면 — 최소 경로"

    어디서 늦었든 **운영 주소 하나와 장면 하나**가 목표입니다. 11:00에 세이브 포인트 1이 아직이면 H1 · H2를 건너뛰고 카드만으로 h3를 보냅니다("아이디어 카드의 화면 한 장으로"). 13:30에 시나리오 1이 아직이면 [h-cut](#h-cut)으로 장면 하나만 남기고 그것만 h4. 14:50에 다듬기 전이면 H5는 건너뛰고 H6의 대본만, 15:15에는 H7의 점검과 마지막 push만 합니다. 앱이 끝까지 안 돼도 **백업 캡처로 보스전은 합니다** — 무엇을 배웠는지가 발표의 절반입니다.

## 다 했으면 — 퀘스트 하나 더 {#more}

<div class="grid cards tf-ext" markdown>

-   <span class="tf-level">기본 · 15분</span>

    **시나리오 2 · 3**

    `SPEC.md`의 다음 시나리오로 h4를 한 번 더. 발표에서는 여전히 시나리오 1만 보여 줍니다 — 2 · 3은 "이것도 됩니다" 한 줄.

-   <span class="tf-level">자유 · 15–30분</span>

    **'와!' 하나 더**

    h-wow를 한 번 더 — 이번에는 `{하고 싶은 것}` 칸을 비워 두고 AI의 제안 셋 가운데 가장 엉뚱한 것을 골라 봅니다.

-   <span class="tf-level">퀘스트 · 10분</span>

    **버디의 앱에서 버그 하나 찾아 주기**

    버디의 운영 주소를 휴대폰으로 열어 이상한 곳 하나를 찾아 알려 줍니다(빈칸으로 저장 · 긴 글 · 뒤로 가기). 고치는 건 주인이 정합니다.

</div>

## 채팅 경로 — Claude Code를 못 쓸 때 {#chat-path}

Claude Code에 로그인이 안 되거나 설치가 막혀도 **발표는 합니다.**

1. **Codespaces**(가장 비슷한 길) — GitHub의 내 저장소 → **Code → Codespaces → Create codespace**. 브라우저 안의 VS Code에서 같은 프롬프트로 같은 단계를 갑니다. push하면 Vercel이 배포합니다.
2. **claude.ai 대화** — 아이디어 카드 · `SPEC.md` · README · 대본은 대화로 쓰고 파일로 받습니다. 앱은 대화에서 **한 파일짜리 HTML 앱**으로 만들어 아티팩트로 게시하고, 그 링크로 세이브 포인트와 `[발표]`를 올립니다 — 가상 데이터만, 바깥 주소 없이.
3. 대화로 받은 파일을 저장소에 올릴 때는 GitHub 웹의 **Add file → Upload files** → `main`에 커밋합니다. Upload files는 `.gitignore`를 보지 않으니 올리기 전에 파일 이름과 내용을 한 번 봅니다.

??? prompt "채팅 시작 — h-chat"

    --8<-- "labs/day6/prompts_hack.md:h-chat"

## 막힐 때 {#troubleshooting}

단계 안의 '막히면'에 없는 것만 모았습니다. 10분이 넘으면 [도움 사다리](hack.md#help)를 한 칸 오릅니다.

| 증상 | 이렇게 해 보세요 |
|---|---|
| `npm run build`가 타입 오류로 깨진다 | 오류 끝 10줄을 [h-fix](#h-fix)로 — 원인 후보 3개를 받고 하나씩 확인합니다 |
| 링크를 열면 Vercel 로그인이 뜬다 | 미리보기 주소를 공유한 것입니다 — Domains의 운영 주소로 바꿔 올립니다 |
| 390 폭에서 옆으로 밀린다 | 고정 폭 · 넓은 표 · 긴 숫자 — 어디가 밀리는지 한 문장으로 h5에 적습니다 |
| 한글이 낱자로 이상하게 끊긴다 | "화면 글에 word-break: keep-all이 빠졌는지 봐 줘" |
| 범위가 너무 커서 시간이 모자란다 | [h-cut](#h-cut) — 발표 장면 하나만 남깁니다 |
| 보여 줄 데이터가 없다 | "안내서 「5. 데이터」대로 가상 데이터 20줄을 만드는 스크립트부터" |
| AI가 안내서를 안 읽고 짐작하는 것 같다 | `@`를 치고 `day6`까지 입력한 뒤 Tab으로 경로를 넣어 "그 절을 먼저 읽고 한 줄씩 대조해 줘" |
| 대화가 길어져 앞의 결정을 잊는다 | 새 대화에서 "SPEC.md와 CLAUDE.md를 읽고 이어서 하자" — 결정은 두 파일에 다 있습니다 |
| 허락 창이 계속 뜬다 | 정상입니다. 무엇을 · 어디에 · 지우는지 읽고 `1 Yes`. 모르는 명령이면 `No` 하고 "이 명령이 뭐 하는 거야?" |

<a id="h-cut"></a>

??? prompt "범위 줄이기 — h-cut(고치지 않고 줄인 안만)"

    --8<-- "labs/day6/prompts_hack.md:h-cut"

<a id="h-fix"></a>

??? prompt "오류 — h-fix(원인부터)"

    --8<-- "labs/day6/prompts_hack.md:h-fix"

<a id="h-save"></a>

??? prompt "세이브 — h-save(커밋 · push 맡기기)"

    --8<-- "labs/day6/prompts_hack.md:h-save"

## 프롬프트 한눈에 {#prompts}

| 언제 | 프롬프트 | 안내서 절 |
|---|---|---|
| 아이디어가 안 떠오를 때 | [h-idea](#h0b) | 8-2 |
| H1 SPEC | [h1 · h1b](#h1) | 1 |
| H2 규칙 | [h2](#h2) | 2 |
| H3 첫 깃발 | [h3](#h3) | 3 |
| H4 시나리오 | [h4](#h4) · [h-db](#db-steps) · h-ai · [h-wow · h-any](#h4) | 4 · 5 · 6 · 7 · 8-2 |
| H5–H7 | [h5](#h5) · [h6](#h6) · [h7](#h7) | 8-1 · 9 · 10 |
| 아무 때나 | [h-save](#h-save) · [h-cut](#h-cut) · [h-fix](#h-fix) · [h-chat](#chat-path) | 0 · 1 · 11 · 12 |

프롬프트 원문은 과정 저장소의 `labs/day6/prompts_hack.md`에도 있습니다.
