---
title: 5일차 실습 C — 사라지는 수첩 미스터리(확인 기록 · DB 붙이기)
---

<div class="tf-lab" markdown>
<span class="tf-eyebrow">5일차 · 실습 C · 4–5교시 · 13:00–14:50 <span class="tf-daystate" data-tf-daystate="5"></span></span>

# 실습 C — 사라지는 수첩 미스터리

<div class="tf-meta" markdown>
<span class="tf-chip">확인 기록 · DB 붙이기</span>
<span class="tf-chip tf-chip--time">1부 같이 따라 하기 13:00–14:34</span>
<span class="tf-chip tf-chip--time">2부 자유 퀘스트 14:34–14:50</span>
<span class="tf-chip tf-chip--tool">Claude Code · Plan → Manual</span>
<span class="tf-chip tf-chip--tool">Supabase(서울)</span>
<span class="tf-chip tf-chip--tool">Prisma 7</span>
<span class="tf-chip tf-chip--tool">Vercel</span>
<span class="tf-chip tf-chip--tool">작업 안내서</span>
<span class="tf-chip tf-chip--tool">채팅 경로 · Codespaces</span>
</div>

<div class="tf-flow" markdown>
<div markdown><b>상황</b> (가상) 한빛정밀(주) 디지털 TF, 화요일 13:00. 수출팀 박 팀장님이 어제 B048(Changzhou Wenant Engineering)에 전화해 '다음 주 입금 약속'을 받아 냈습니다. 금요일에 만든 보드에서 '확인 완료'를 누르고 메모까지 적었는데 — 새로 고침 한 번에 감쪽같이 사라졌습니다. 혹시 몰라 적어 둔 종이 수첩은 회의실 어딘가에서 실종. 범인은 **아무것도 기억하지 못하는 앱**입니다. 디지털 TF 최 대리(나)에게 떨어진 미션 — "앱에 금고(DB)를 달아, 누가 · 언제 · 무엇을 확인했는지 새로 고쳐도 · 휴대폰에서도 남게 하라."</div>
<span>→</span>
<div markdown><b>넣는 것</b> 새 Supabase 프로젝트(서울 · 무료) + 어제 만든 웹앱(`/buyers` · `/buyers/[id]`) + `data/buyers.json`(바이어 150곳 · 가상) + **작업 안내서** `guide/day5_lab_c.md` + 두 줄짜리 프롬프트</div>
<span>→</span>
<div markdown><b>얻는 것</b> 1부 — 금고의 표 `Buyer`(150곳) · `Review`(확인 기록) + 자물쇠(RLS) · 금고를 읽는 쪽 셋 · 새로 고쳐도 남는 확인 기록 · **휴대폰과 내 PC가 같은 기록을 보는 배포 주소** / 2부 — 내가 고른 기능 하나 · 커밋 2개 + push</div>
</div>

<div class="tf-lab__grid" markdown>
<div class="tf-lab__cell" markdown><span class="tf-lab__label">목표</span> 앱에 **기억**을 답니다 — 금고(DB) 빌리기 → 열쇠 받기 → 서랍(표) 짜기 → 서랍 채우기 → 쪽이 금고 읽기 → 기록 쓰기 → 배포 주소에도 열쇠. 화면의 숫자는 어제와 **한 자리도** 같고, 달라지는 것은 '이제 남는다'는 것 하나입니다</div>
<div class="tf-lab__cell" markdown><span class="tf-lab__label">오전과의 관계</span> 오전에 본 쉬운 그림 다섯을 손으로 해 봅니다 — 왜 DB인가(배포한 앱은 쓴 것을 기억하지 못한다) · 연결 문자열과 풀러(앱은 6543 · 표 만들기는 5432) · `schema.prisma` = 표 설계도 · 서버 액션 = 창구(검사는 서버가) · 환경 변수는 두 곳(내 PC `.env` · Vercel) — 바꾸면 Redeploy → [1교시](class.md#p1) · [2교시](class.md#p2)</div>
</div>

<div data-tf-map></div>
</div>

!!! quote "디지털 TF 단톡방 — 오늘 12:47"

    **박 팀장(수출팀)** 분명히 적었어요. B048 '다음 주 입금 약속', 확인 완료까지 눌렀다고요. 오늘 열어 보니… 없어요.

    **오 주임(IT팀)** 범인 찾았습니다. 그 앱은 새로 고침 한 번이면 다 잊습니다. 금붕어가 더 오래 기억해요.

    **한 과장(재무팀)** 기록이 없으면 다음 주에 독촉 메일이 또 나갑니다. 약속한 바이어한테 독촉이라니, 그건 사고예요.

    **정 영양사님(한빛식당)** 제 감 노트는 30년째 한 장도 안 없어졌는데요.

    **대표님** 확인한 내용, 저도 휴대폰에서 바로 봤으면 해요. 누가 언제 확인했는지도요.

    **최 대리(나)** 앱에 금고를 달겠습니다. 두 시간이면 됩니다. …금고 비밀번호는 안 잊어버리겠습니다.

!!! file "작업 안내서란? — `guide/day5_lab_c.md`"

    3일차 · 4일차와 같은 방식입니다. 긴 규칙(표 설계의 모델 글 · 처음 데이터 넣는 법 · 쪽 바꾸는 법 · 확인 기록의 검사 순서와 안내 문구 · 커밋 규칙)은 내 웹 저장소의 **작업 안내서**에 절마다 들어 있고, 프롬프트는 "「2. 표 설계」대로"처럼 그 절을 가리킵니다. 그래서 프롬프트는 두 줄 — **첫 줄은 목적**, 둘째 줄은 할 일입니다.

    | 누가 | 무엇을 |
    |---|---|
    | 나 | 금고를 만들고 **열쇠(비밀번호 · 연결 주소)를 직접** 다룬다 · 프롬프트를 보내고 허락 창을 읽는다 · '확인할 것'과 견준다 |
    | AI | 안내서의 그 절대로 코드를 쓰고 명령을 허락받아 실행한 뒤, 끝에 '확인할 것' 3줄을 보여 준다 — `.env`는 열지 못한다(저장소 설정이 막아 둔다) |
    | 안내서 | 모두가 같은 표 · 같은 숫자를 얻도록 모델 글 · 문구 · 파일 이름을 고정해 둔다 — 열어 봐도 된다(고치지는 않는다) |

## 시작 전 확인 {#before}

점심 전에 봐 두면 13:00부터 금고 만들기에 바로 들어갑니다. 하나라도 막히면 점심 전에 손을 듭니다.

<div class="tf-checklist" data-title="시작 전 확인 5가지" markdown>

- [ ] 어제 만든 내 배포 주소 `https://tradefin-web-t{조}-{번호}.vercel.app/buyers`가 열린다(안 되면 아래 C-0 · 01의 '합류')
- [ ] supabase.com에 로그인된다(4일차에 가입) — 프로젝트는 13:00에 함께 만든다
- [ ] VS Code에 **웹 저장소**가 열려 있고 터미널이 명령 프롬프트(cmd)다
- [ ] 휴대폰으로 내 배포 주소를 열 수 있다(보스전에 씁니다)
- [ ] 비밀번호를 적을 곳(종이 · 휴대폰 메모)이 있다 — 채팅 · 프롬프트 · 오픈채팅 · 저장소에는 적지 않는다

</div>

이 쪽의 단축키는 Windows 기준입니다. Mac은 ++ctrl++ 대신 ++cmd++를 누르고(미리보기 ++cmd+shift+v++), 터미널 ++ctrl+grave++와 소스 제어 ++ctrl+shift+g++만 Mac에서도 ++ctrl++입니다.

## 쓰는 파일 — 이미 내 웹 저장소에 {#files}

오늘은 받을 파일이 없습니다. 모두 4일차에 만든 내 웹 저장소에 **이미 들어 있고**, 고친 안내서는 `npm run guide:update`로 받습니다(C-0 · 01). 저장소 없이 채팅 경로로 하는 분은 템플릿 <https://github.com/brainini/tradefin-web-starter>에서 **Code → Download ZIP**으로 받습니다.

| 파일 | 무엇 | 오늘 |
|---|---|---|
| `data/buyers.json` | 바이어 150곳 × 16칸(가상) — 어제 쪽들이 읽던 파일 | 처음 데이터로 금고에 넣는다(파일은 읽기만) |
| `guide/day5_lab_c.md` | **작업 안내서** — 절 0–11 | AI가 읽는다 |
| `prisma/schema.prisma` | 표 설계도 — 지금은 모델 없음 | 모델 `Buyer` · `Review`를 더한다 |
| `prisma.config.ts` · `lib/db.ts` | 금고 연결 설정 · 연결 함수 — 미리 시험해 둔 파일 | 고치지 않는다 |
| `.env.example` | 비밀의 **이름표**(값 없음) | `npm run env:init`으로 `.env`를 만든다 |
| `scripts/doctor.mjs` | 의사 — `doctor` · `doctor:db` · `doctor:secrets` | 막히면 먼저 |

!!! warning "금고 비밀번호와 연결 주소는 딱 두 곳에만"

    내 PC의 `.env`와 Vercel의 환경 변수 — 이 두 곳 말고는 어디에도 쓰지 않습니다. Claude Code 입력창 · claude.ai 대화 · 오픈채팅 · 화면 캡처 · 커밋 모두 안 됩니다. AI가 `.env`를 열겠다고 허락을 구하면 `No`. 실수로 새었으면 숨기지 말고 손을 듭니다 — Supabase에서 비밀번호를 새로 만들고(Reset) 두 곳을 고치면 끝납니다.

## 0 · 출발 전 — 장비 점검 {#part0}

### C-0 · 01 퀘스트 0 · 장비 점검 — 안내서 새 판 · doctor (12:50–13:00) { #c0-1 .step data-tool="터미널 · VS Code" }

**왜** 어젯밤 안내서가 고쳐졌을 수 있습니다. 내 웹 저장소에 새 판을 받고, 오늘 쓸 도구가 다 있는지 의사(doctor)에게 진찰받습니다. 아침 08:40에 했어도 한 번 더 해도 됩니다 — 같은 판이면 바뀌는 것이 없습니다. `git pull` → `npm run guide:update` → `npm run doctor`

!!! me "내가 할 일"

    1. VS Code 창 제목에 `tradefin-web`이 보이는지 봅니다(과정 저장소 `tradefin-my-…`가 아닙니다).
    2. 터미널(++ctrl+grave++)에서 차례로 실행합니다.

        ```text
        git pull
        npm run guide:update
        npm run doctor
        ```

    3. `guide:update`가 `✓ 받았습니다`라고 하면, 바뀐 파일은 소스 제어(++ctrl+shift+g++)의 **Staged Changes**에 이미 올라가 있습니다 → 화면의 '다음:' 줄의 메시지(`5일차: 안내서 받기`)로 **Commit**. `✓ 이미 템플릿과 같습니다`면 할 일이 없습니다.
    4. `npm run dev`를 켜 둡니다(터미널 오른쪽 위 `+`로 터미널 하나 더) → 브라우저에서 `http://localhost:3000/buyers`가 어제처럼 열리는지 봅니다. 이 터미널은 실습 내내 켜 둡니다 — AI는 개발 서버를 새로 켜지 않습니다.

**이 단계의 목적** 최신 안내서를 받고, 오늘 쓸 도구가 다 있는지 확인합니다.

!!! ai "AI가 하는 일"

    이번 단계는 사람 차례입니다(AI 없음). `doctor`는 아무것도 고치지 않고, 걸린 곳마다 `→` 줄로 고치는 법을 알려 줍니다.

!!! ok "확인할 것"

    - [ ] 탐색기의 `guide/`에 `day5_lab_c.md`가 있다
    - [ ] `doctor` 끝 줄이 `✗ 0`이다 — `– .env 없음(5일차)` 한 줄은 정상(13:10에 만듭니다)
    - [ ] `localhost:3000/buyers`가 어제와 같은 숫자로 열린다

??? fix "`guide:update`가 '커밋하지 않은 변경이 있어 멈춥니다'라고 해요"

    `guide/` · `data/` · `hackathon/`에 커밋하지 않은 변경이 있다는 뜻입니다. 흔한 까닭은 아침에 받은 안내서를 아직 커밋하지 않은 것입니다.

    1. 소스 제어(++ctrl+shift+g++)의 **Staged Changes**에 아침에 받은 `guide/…`가 있으면 → 그대로 메시지 `5일차: 안내서 받기`로 **Commit** → `npm run guide:update`를 다시 실행합니다.
    2. 내가 실수로 고친 파일이면 → `git restore --staged <파일>` → `git restore <파일>`로 되돌리고 다시 실행합니다(`git restore`만으로는 Staged Changes가 그대로 남습니다).

    헷갈리면 손을 듭니다 — 지우기 전에 같이 봅니다.

??? fix "`npm`이 '이 시스템에서 스크립트를 실행할 수 없으므로'라며 막혀요"

    PowerShell의 실행 정책입니다. 터미널 오른쪽 위 `+` 옆 `∨` → **Command Prompt**를 고르거나, `npm` 대신 `npm.cmd`로 칩니다.

??? fix "어제 웹앱이 없어요 · `/buyers`가 '찾을 수 없습니다'예요"

    기준본으로 합류합니다 — 먼저 지금 변경을 커밋한 뒤 `npm run catchup -- day4-d` → `npm run build` → 화면이 알려 주는 메시지(`5일차: 합류 — 4일차 실습 D 기준본`)로 커밋 → push. 그다음 C-1 · 01로 갑니다 → [웹 작업대 → 합류](../web.md#update)

<span class="tf-chip tf-chip--ok">획득</span> 최신 안내서 · 진단서(doctor ✗ 0)

<p class="tf-check"><time>13:00</time> 손 점검 — 창 제목 tradefin-web · doctor ✗ 0 · localhost:3000/buyers</p>

## 1부 · 같이 따라 하기 — 모두 같은 결과 {#part1}

<div class="tf-phase" markdown>

<span class="tf-eyebrow">1부 · C-1 13:00–13:50 · 쉬는 시간 · C-2 14:00–14:34 · Supabase · Claude Code · Vercel</span>

금고를 빌리고, 서랍을 짜고, 바이어 150곳을 넣고, 쪽이 금고를 읽게 하고, 사라지지 않는 수첩을 단다 — **모두 같은 프롬프트, 같은 숫자**

**목표** 새로 고쳐도 · 다른 기기에서도 남는 확인 기록. 배포 주소와 내 PC가 **같은 금고**를 본다

1. 퀘스트 1 금고 터 잡기 — Supabase 새 프로젝트(서울) · c1
2. 퀘스트 2 금고 열쇠 — 연결 주소 두 줄 → `.env` → doctor:db
3. 퀘스트 3 서랍 두 칸 — 표 설계(Plan) → db:push · RLS
4. 퀘스트 4 서랍 채우기 — 150곳, 두 번 넣어도 150
5. 세이브 포인트 1 — 커밋
6. 퀘스트 5 쪽이 금고를 읽는다 — 어제와 같은 숫자
7. 퀘스트 6 사라지지 않는 수첩 — 확인 기록(서버 액션)
8. 보스전 — 휴대폰에서 쓴 기록이 내 PC에도

**결과물** 표 `Buyer`(150) · `Review` · RLS 켬 · 금고를 읽는 쪽 셋 · 확인 기록 입력 칸과 목록 · Vercel 환경 변수 · 커밋 2개 + push

</div>

**금고와 앱은 이렇게 자랍니다** — 데이터는 금고(Supabase)에, 설계도와 코드는 저장소(GitHub)에 남습니다.

| 단계 | 금고(Supabase)에 생기는 것 | 저장소 · 앱에 생기는 것 |
|---|---|---|
| C-1 · 01 | 프로젝트 `tradefin-web`(서울) | – |
| C-1 · 02 | – | 내 PC의 `.env`에 열쇠 두 줄(커밋되지 않음) |
| C-1 · 03 | 표 `Buyer` · `Review`(0행) · 자물쇠(RLS) | `prisma/schema.prisma`에 모델 둘 |
| C-1 · 04 | `Buyer` 150행 | `prisma/seed.ts` |
| C-2 · 01 | – | 쪽 셋이 금고를 읽음 |
| C-2 · 02 | `Review` 1행 | 확인 기록 입력 칸 · 목록 |
| C-2 · 03 | `Review` 2행(휴대폰에서) | 배포 주소에도 열쇠(Vercel 환경 변수) |

### C-1 · 01 퀘스트 1 · 금고 터 잡기 — Supabase 새 프로젝트(서울) (13:00–13:10) { #c1-1 .step data-tool="Supabase · Claude Code" }

**왜** 기록이 사라지지 않으려면 앱 바깥에 **금고**가 있어야 합니다. 배포한 앱(Vercel)은 요청 하나가 끝나면 쓴 것을 기억하지 못하기 때문입니다. Supabase에서 내 금고(PostgreSQL DB)를 서울에 하나 빌립니다. 만드는 데 2–3분 — 그동안 AI에게 오늘 바뀌는 곳을 정리하게 합니다. 비밀번호 정하기 → **New project** → **c1**(읽기만)

!!! me "내가 할 일"

    1. 비밀번호를 먼저 정해 **내 메모에만** 적습니다 — **영문 대소문자 + 숫자, 16자 이상, 기호 없이**. 기호(`@` `#` `:` `/` `?` …)가 들어가면 연결 주소가 깨집니다.
    2. 브라우저에서 <https://supabase.com/dashboard> → 4일차에 가입한 계정으로 로그인합니다.
    3. **New project**를 누르고 칸을 채웁니다.

        - **Organization** — 내 조직(가입할 때 생긴 것)
        - **Project name** — `tradefin-web`
        - **Database Password** — 1에서 정한 비밀번호. **Generate a password**로 만든 값에 기호가 없으면 그것을 메모해 써도 됩니다
        - **Region** — **Northeast Asia (Seoul)**. 'Asia-Pacific'처럼 넓은 지역만 보이면 정확한 지역을 고르는 쪽에서 Seoul
        - 나머지(보안 · 고급 설정)는 그대로

    4. **Create new project**를 누르고, 만들어지는 동안 Claude Code 입력창에 **c1**을 보냅니다.

**이 단계의 목적** 앱 바깥에 금고를 하나 빌리고, 그동안 오늘 바뀌는 곳을 정리합니다.

!!! prompt "프롬프트 c1 — 오늘의 설계(읽기만)"

    --8<-- "labs/day5/prompts_c.md:c1"

!!! ai "AI가 하는 일"

    안내서와 지금 파일들을 읽고, 오늘 바뀌는 파일 표와 세 줄을 답합니다(파일은 만들지 않습니다 · 30초–1분). `.env`는 열지 않습니다 — 저장소의 `.claude/settings.json`이 막아 둡니다.

!!! ok "확인할 것"

    - [ ] Supabase에 프로젝트 `tradefin-web` · 지역 Seoul(`ap-northeast-2`) · 만들기가 끝나 대시보드가 열린다
    - [ ] 비밀번호가 **내 메모에만** 있다
    - [ ] c1의 표에 바뀌는 파일 **9개**(새 4 · 고침 5)와 바꾸지 않는 파일 넷(`lib/db.ts` · `prisma.config.ts` · `lib/metrics.ts` · `data/`)

??? fix "무료 프로젝트 2개 한도라 더 만들 수 없대요"

    쓰지 않는 다른 프로젝트를 쉬게(Pause) 합니다 — 그 프로젝트의 Project Settings → General → **Pause project**. 쉬게 한 프로젝트는 나중에 Restore로 되살립니다. 그 뒤 다시 New project.

??? fix "Region 목록에 Seoul이 없어요"

    넓은 지역(General region)만 보이는 화면입니다. 정확한 지역(Specific region)을 고르는 쪽을 열어 **Northeast Asia (Seoul)**을 고릅니다. 배포 서버가 서울(`icn1`)에 있어서 금고도 서울이어야 빠릅니다.

??? fix "비밀번호를 잊었어요 · 기호를 넣어 버렸어요"

    프로젝트의 Database → Settings → **Reset database password**에서 영문 + 숫자 16자 이상으로 다시 만듭니다. 만들기 전이면 그냥 다시 정하면 됩니다.

??? fix "c1이 '4일차 쪽이 없습니다'라고 해요"

    C-0 · 01의 '어제 웹앱이 없어요'대로 합류한 뒤 c1을 다시 보냅니다.

<span class="tf-chip tf-chip--ok">장비 획득</span> 내 금고(서울) 1개 · 금고 비밀번호(내 메모에만)

<p class="tf-check"><time>13:10</time> 손 점검 — 프로젝트 tradefin-web(Seoul) 완성 · c1 표에 9개</p>

### C-1 · 02 퀘스트 2 · 금고 열쇠 받기 — 연결 주소 두 줄 → .env → doctor:db (13:10–13:20) { #c1-2 .step data-tool="Supabase · VS Code · 터미널" }

**왜** 앱이 금고를 찾아가려면 **주소 + 열쇠**가 든 한 줄(연결 문자열)이 필요합니다. 오늘은 두 줄입니다 — 앱(내 PC · Vercel)이 쓰는 **6543**(트랜잭션 풀러)과, 표를 만드는 명령이 쓰는 **5432**(세션 풀러). 비밀번호가 들어가는 줄이라 이 단계는 **사람이 직접** 하고, AI에게는 보여 주지 않습니다. **Connect** → `.env` → `npm run doctor:db`

!!! me "내가 할 일"

    1. Supabase 프로젝트 화면 위쪽 **Connect** → **ORMs** 탭 → 도구가 **Prisma**인지 봅니다. `DATABASE_URL`(…`:6543`…) · `DIRECT_URL`(…`:5432`…) 두 줄이 든 칸을 복사 단추로 복사합니다. 칸 이름이 `.env.local`이어도 우리는 `.env`에 넣습니다. 같은 창의 `schema.prisma` 조각은 **쓰지 않습니다**(Prisma 7은 주소를 `prisma.config.ts`가 읽습니다).
    2. 터미널에서 `.env`를 만듭니다.

        ```text
        npm run env:init
        ```

    3. ++ctrl+p++ → `.env` 입력 → 엽니다. `DATABASE_URL=""` 줄과 `DIRECT_URL=""` 줄을 지우고, 그 자리에 복사한 두 줄을 붙여 넣습니다. 아래 `APPROVER_PIN` · `FX_FORCE_FALLBACK` 줄은 그대로 둡니다(실습 D에서 씁니다).
    4. 두 줄의 `[YOUR-PASSWORD]`를 **대괄호까지 지우고** 내 비밀번호로 바꿉니다(두 군데) → ++ctrl+s++로 저장.
    5. 의사에게 열쇠를 보여 줍니다.

        ```text
        npm run doctor:db
        ```

**이 단계의 목적** 금고 열쇠 두 줄을 내 PC의 `.env`에만 넣고, 둘 다 열리는지 확인합니다.

!!! ai "AI가 하는 일"

    이번 단계는 사람 차례입니다(AI 없음). `doctor:db`는 두 줄의 모양(포트 · 사용자 이름 · `[YOUR-PASSWORD]` · 기호 · 직접 연결 주소)을 먼저 보고, 실제로 접속해 봅니다 — 비밀번호는 `****`로 가려서 보여 줍니다.

!!! ok "확인할 것"

    - [ ] `✓ DATABASE_URL … :6543 (트랜잭션 풀러) 연결 OK · PostgreSQL 17.x`
    - [ ] `✓ DIRECT_URL … :5432 (세션 풀러) 연결 OK`
    - [ ] `– 표: 아직 없음` · 끝 줄 `✗ 0` · 화면 어디에도 비밀번호가 그대로 보이지 않는다(`:****@`)

??? ok "참고 실행 값 — 내 결과를 본 뒤 펼쳐 보기"

    모양의 예입니다. 사용자 이름 뒷부분 · 주소의 `aws-…` 숫자 · 버전 끝자리 · 응답 시간은 사람마다 다릅니다.

    ```text
    == DB 점검 (npm run doctor:db) — .env의 주소 두 개(비밀번호는 ****)
    ✓ DATABASE_URL 모양 OK — postgresql://postgres.abcde…:****@aws-1-ap-northeast-2.pooler.supabase.com:6543/postgres (트랜잭션 풀러 — 앱 · Vercel)
    ✓ DATABASE_URL … :6543 (트랜잭션 풀러) 연결 OK · PostgreSQL 17.x · 80ms
    – 표: 아직 없음(표 만들기는 npm run db:push)
    ✓ DIRECT_URL 모양 OK — postgresql://postgres.abcde…:****@aws-1-ap-northeast-2.pooler.supabase.com:5432/postgres (세션 풀러 — db:push)
    ✓ DIRECT_URL … :5432 (세션 풀러) 연결 OK · PostgreSQL 17.x · 60ms

    결과: ✓ 4 · ! 0 · ✗ 0 · – 1 — 문제 없음
    ```

??? fix "`[YOUR-PASSWORD]가 그대로 있습니다` · `대괄호 [ ]가 남아 있습니다`"

    두 줄 모두에서 `[YOUR-PASSWORD]`를 대괄호까지 지우고 비밀번호만 넣습니다 → ++ctrl+s++ → 다시 `npm run doctor:db`.

??? fix "`비밀번호가 틀렸습니다`(28P01)"

    오타이거나 프로젝트를 만들 때 쓴 비밀번호와 다릅니다. 잊었으면 Database → Settings → **Reset database password**(영문 + 숫자) → `.env`의 두 줄 모두 고칩니다.

??? fix "`Tenant or user not found` · `사용자 이름이 … 모양이 아닙니다`"

    사용자 이름은 `postgres.<프로젝트 ref>` 꼴이어야 합니다. 손으로 고치지 말고 Connect → ORMs → Prisma에서 두 줄을 다시 복사합니다.

??? fix "`직접 연결 주소입니다(db.….supabase.co …)`"

    Connect 화면의 다른 칸(직접 연결)을 복사했습니다. 직접 연결은 IPv6 전용이라 대부분의 네트워크에서 닿지 않습니다 — **ORMs → Prisma** 칸의 `….pooler.supabase.com` 주소로 바꿉니다.

??? fix "`시간 초과` · `ETIMEDOUT`"

    회사 · 학교 네트워크가 5432 · 6543 포트를 막을 수 있습니다. 휴대폰 핫스팟으로 바꿔 다시 → 그래도 안 되면 [채팅 경로](#chat-path)의 Codespaces.

??? fix "`.env가 없습니다` · `…가 비어 있습니다`"

    `npm run env:init`을 했는지, 붙여 넣은 뒤 ++ctrl+s++로 저장했는지 봅니다(탭 이름 옆 흰 점 = 저장 안 됨).

<span class="tf-chip tf-chip--ok">획득</span> 금고 열쇠 두 개(6543 앱용 · 5432 명령용) — 내 PC에만

<p class="tf-check"><time>13:20</time> 손 점검 — doctor:db 두 줄 연결 OK · 표: 아직 없음</p>

### C-1 · 03 퀘스트 3 · 서랍 두 칸 — 표 설계(Plan) → db:push (13:20–13:32) { #c1-3 .step data-tool="Claude Code · Plan · 터미널" }

**왜** 금고 안에 **서랍(표)**을 짭니다. 서랍 모양은 설계도 `prisma/schema.prisma`에 적고, `npm run db:push` 한 번이 그대로 금고에 만듭니다. 설계도는 사람이 읽고 승인합니다 — 바이어 하나에 확인 기록이 여럿 붙는 모양(1 : N)입니다. **c2**(Plan) → 계획 읽기 → `db:push` 허락

| 서랍 | 한 줄 = | 칸 | 오늘 줄 수 |
|---|---|---|---|
| `Buyer` | 바이어 한 곳 | `id`(B001 …) · 이름 · 나라 · 지역 · 업종 · 결제 · 채권 · 연체 · 위험 점수 · 등급 · 신호 … 16칸 + 그 바이어의 기록 목록 | 150(C-1 · 04) |
| `Review` | 확인 기록 한 건 | `id`(1, 2, 3 … 자동) · `buyerId`(어느 바이어) · `status`(확인 필요 · 확인 완료 · 보류) · `memo` · `reviewer`(별명) · `createdAt`(자동) | 쓰는 만큼 |

!!! me "내가 할 일"

    1. 입력창 아래 모드 표시를 눌러 **Plan**으로 바꿉니다.
    2. **c2**를 보냅니다. 계획이 열리면 바꿀 파일 **하나**(`prisma/schema.prisma`) · 모델 **둘** · 명령 `npm run db:push`를 읽습니다.
    3. 승인 창에서 **`2 Yes, and manually approve edits`** → 쓰기 허락 창(무엇을 · 어디에)을 읽고 `1 Yes`.
    4. `npm run db:push` 허락 창 — 명령이 정확히 이것인지 읽고 `1 Yes`. `migrate` · `--accept-data-loss` · `--force-reset`이 보이면 `No`.
    5. Supabase 왼쪽 메뉴 **Table Editor**에서 표 둘을 봅니다(안 보이면 새로 고침).

**이 단계의 목적** 금고 안에 바이어 서랍과 확인 기록 서랍을 만들고, 자물쇠(RLS)를 채웁니다.

!!! prompt "프롬프트 c2 — 표 설계 · Plan 모드"

    --8<-- "labs/day5/prompts_c.md:c2"

!!! ai "AI가 하는 일"

    계획을 먼저 보여 줍니다(Plan 모드라 아직 아무것도 고치지 않습니다). 승인하면 `schema.prisma` 끝에 모델 두 개를 더하고, `npm run db:push`를 허락받아 실행합니다(허락 창 2–3번 · 1–3분). 이 명령 하나가 표 만들기 → 앱이 쓸 코드 다시 만들기(generate) → 표마다 RLS 켜기를 차례로 합니다. 끝으로 `npm run build`.

!!! ok "확인할 것"

    - [ ] 터미널에 `Your database is now in sync with your Prisma schema`와 `Generated Prisma Client (7.10.1)`
    - [ ] 끝 줄 `✓ RLS 켬 2/2 (Buyer · Review)`
    - [ ] Table Editor에 `Buyer` · `Review` — 둘 다 0행

??? ok "참고 실행 값 — 내 결과를 본 뒤 펼쳐 보기"

    주소 · 걸린 시간은 사람마다 다르고, 실제 화면에는 몇 줄 앞에 그림 글자가 붙어 보이기도 합니다. 찾을 것은 세 줄 — `in sync` · `Generated Prisma Client` · `RLS 켬 2/2`.

    ```text
    > tradefin-web@0.1.0 db:push
    > prisma db push && prisma generate && node scripts/doctor.mjs rls

    Loaded Prisma config from prisma.config.ts.

    Prisma schema loaded from prisma/schema.prisma.
    Datasource "db": PostgreSQL database "postgres", schema "public" at "aws-1-ap-northeast-2.pooler.supabase.com:5432"

    Your database is now in sync with your Prisma schema. Done in 2.1s

    Loaded Prisma config from prisma.config.ts.

    Prisma schema loaded from prisma/schema.prisma.

    ✔ Generated Prisma Client (7.10.1) to ./lib/generated/prisma in 44ms

    == RLS 켜기 (public 표 전부 — 이미 켜져 있으면 그대로)
    ✓ RLS 켬 2/2 (Buyer · Review) — Supabase 공개 API로는 읽고 쓸 수 없음 · 앱은 서버에서 그대로

    결과: ✓ 1 · ! 0 · ✗ 0 — 문제 없음
    ```

    모델 글(안내서 「2. 표 설계」와 같아야 합니다): `Buyer` 17줄(칸 16 + `reviews Review[]`) · `Review` 7줄 + `@@index([buyerId])`.

!!! info "RLS 켬 — 서랍마다 채우는 자물쇠"

    Supabase는 표마다 인터넷용 자동 창구(공개 API)를 열 수 있습니다. **RLS(행 단위 보안)**를 켜고 열어 줄 규칙을 하나도 두지 않으면, 그 창구로는 아무것도 보이지 않습니다. 우리 앱은 서버에서 금고 비밀번호로 직접 들어가므로(Prisma) 그대로 읽고 씁니다 — 문지기는 우리 서버 코드입니다. 그래서 `db:push`가 끝날 때마다 의사가 자물쇠를 채웁니다.

??? fix "'data loss' · `Do you want to ignore the warning(s)?`가 나와요"

    아무것도 고르지 말고(또는 `N`) 손을 듭니다. 이미 있는 칸을 바꾸거나 지우려 할 때 나오는 경고입니다 — 오늘 1부에서는 나올 일이 없습니다.

??? fix "계획 대신 '쓰기가 막혔다' · 'Plan 모드를 풀어 달라'는 답이 와요"

    정상입니다 — Plan 모드는 파일 쓰기를 막습니다. "계획만 먼저 보여 줘"라고 보내고, 계획을 읽은 뒤 승인합니다.

??? fix "AI가 `schema.prisma`의 `datasource`에 `url = env(…)`을 더했어요 · `P1012`"

    Supabase 화면의 옛 조각을 따라 한 것입니다. Prisma 7은 주소를 `prisma.config.ts`가 읽으므로 빼야 합니다 — "안내서 「2. 표 설계」대로 datasource 블록은 처음 그대로 두고 url · directUrl을 지워"라고 보냅니다.

??? fix "`Connection url is empty` · `Can't reach database server at localhost:5432`"

    `.env`의 열쇠가 비었거나(`DIRECT_URL=""` 그대로) `.env`를 저장하지 않아 자리표시 주소(`localhost:5432`)가 쓰였습니다. C-1 · 02로 돌아가 두 줄을 붙여 넣고 ++ctrl+s++ → `npm run doctor:db`가 `✗ 0`이 된 뒤 c2를 다시 보냅니다.

??? fix "`비밀번호가 틀렸습니다` · `Tenant or user not found` · 연결 오류"

    열쇠 문제입니다. `npm run doctor:db`를 돌려 C-1 · 02의 막히면으로 고친 뒤 c2를 다시 보냅니다. 원인을 모르겠으면 [막힐 때](#troubleshooting)의 'DB 오류 — 원인부터' 프롬프트에 doctor 결과를 붙입니다.

??? fix "RLS 줄이 `2/2`가 아니에요"

    새 프로젝트가 아니라 다른 표가 있는 프로젝트를 쓴 것입니다. 오늘 실습은 그대로 되지만 숫자가 표 수만큼 다릅니다 — 가능하면 새 프로젝트 `tradefin-web`로 다시 합니다.

<span class="tf-chip tf-chip--ok">획득</span> 서랍 두 칸(`Buyer` · `Review`) · 서랍 자물쇠(RLS)

<p class="tf-check"><time>13:32</time> 손 점검 — RLS 켬 2/2 · Table Editor에 Buyer · Review(0행)</p>

### C-1 · 04 퀘스트 4 · 서랍 채우기 — 150곳, 두 번 넣어도 150 (13:32–13:45) { #c1-4 .step data-tool="Claude Code · 터미널" }

**왜** 빈 서랍에 바이어 150곳을 넣습니다(처음 데이터 = **시드**). 실수로 두 번 넣어도 300곳이 되면 안 됩니다 — 어제 메일 당번 로봇처럼 **두 번 돌려도 같은 결과**. 그래서 같은 번호(`id`)가 이미 있으면 건너뛰게 넣습니다. **c3** → `prisma/seed.ts` → `npm run db:seed` 두 번

!!! me "내가 할 일"

    1. 입력창 아래 모드를 **Manual**로 돌려놓고 **c3**를 보냅니다.
    2. 쓰기 허락 창에서 `prisma/seed.ts`(새 파일)를 읽고 `1 Yes`.
    3. `npm run db:seed` 허락 창을 읽고 `1 Yes` → 결과 세 줄을 읽습니다.
    4. AI가 한 번 더 실행하겠다고 물으면 또 `1 Yes` — 이번엔 `새로 넣음 0행`이어야 합니다.
    5. Table Editor → `Buyer`에서 행 수와 B048 줄을 봅니다.

**이 단계의 목적** 바이어 150곳을 금고에 넣고, 두 번 넣어도 150곳인지 확인합니다.

!!! prompt "프롬프트 c3 — 처음 데이터"

    --8<-- "labs/day5/prompts_c.md:c3"

!!! ai "AI가 하는 일"

    `prisma/seed.ts`를 쓰고 `npm run db:seed`를 두 번 실행합니다(허락 창 3–4번 · 1–3분). 넣은 뒤 금고에서 다시 세어 세 줄을 찍습니다 — 숫자는 눈이 아니라 DB가 센 값입니다. 끝으로 `npm run build`(`seed.ts`도 타입 검사를 받습니다).

!!! ok "확인할 것"

    - [ ] 1차 `새로 넣음 150행 · 이미 있던 행 0행`
    - [ ] 2차 `새로 넣음 0행 · 이미 있던 행 150행` — 두 번 다 `Buyer 150행 (S 126 · A 4 · B 3 · C 17)`
    - [ ] Table Editor의 `Buyer` 150행 · B048의 `grade`가 `C` · `pctAr31p`가 1

??? ok "참고 실행 값 — 내 결과를 본 뒤 펼쳐 보기"

    아래 세 줄(`새로 넣음` · `Buyer` · `Review`)은 seed가 찍는 줄이라 글자까지 같아야 합니다. 그 앞은 npm · Prisma가 찍는 줄이고, 끝에 Prisma가 '다 했다'는 한 줄을 더 찍습니다.

    ```text
    > tradefin-web@0.1.0 db:seed
    > prisma db seed

    Loaded Prisma config from prisma.config.ts.

    Running seed command `tsx prisma/seed.ts` ...
    새로 넣음 150행 · 이미 있던 행 0행
    Buyer 150행 (S 126 · A 4 · B 3 · C 17)
    Review 0행
    ```

    빈칸(`null`)이 있는 칸 — `pctAr31p` 59곳(받을 돈이 0인 곳) · `avgDaysLate12m` 14곳(최근 1년 외상 거래가 없는 곳). Table Editor에서 `NULL`로 보이면 맞습니다.

??? fix "`Unique constraint failed`가 나요"

    `skipDuplicates` 없이 넣었습니다. "안내서 「3. 처음 데이터」대로 createMany에 skipDuplicates: true"라고 보냅니다. 앞에서 넣은 줄은 그대로 있으니 지우지 않습니다.

??? fix "`An error occurred while running the seed command`가 나와요"

    진짜 까닭은 **그 바로 위 줄**에 있습니다. `DATABASE_URL이 없습니다`면 `.env`가 없거나 저장되지 않은 것 — C-1 · 02로 돌아가 저장 → `npm run doctor:db` → c3를 다시. 다른 글이면 그 줄을 붙여 '원인부터' 프롬프트로 묻습니다.

??? fix "AI가 `id`를 새로 만들었어요(1, 2, 3 …) · 2차에 300행"

    `id`는 JSON의 `B001`–`B150` 그대로여야 합니다. "안내서 「3. 처음 데이터」대로 id는 JSON 그대로 — 고쳐 줘"라고 보내고, 손을 들어 잘못 들어간 줄을 같이 정리합니다.

<span class="tf-chip tf-chip--ok">획득</span> 바이어 150곳(금고 안) · '두 번 해도 같은 결과' 배지

<p class="tf-check"><time>13:45</time> 손 점검 — 2차 새로 넣음 0행 · Buyer 150행</p>

### C-1 · 05 세이브 포인트 1 — 커밋(push는 아직) (13:45–13:50) { #c1-5 .step data-tool="Git · Claude Code" }

**왜** 서랍 설계와 채우는 법을 세이브해 두면, 오후에 무엇을 망가뜨려도 여기로 돌아옵니다. 금고 속 데이터는 저장소가 아니라 Supabase에 있습니다 — 저장소에는 **설계도와 채우는 법**만 남깁니다. `prisma/` 두 파일 → 두 줄 메시지 → 커밋 1개

!!! me "내가 할 일"

    1. 소스 제어(++ctrl+shift+g++)에서 `prisma/schema.prisma` · `prisma/seed.ts`만 `+`로 고릅니다. `.env`는 목록에 아예 보이지 않는 것이 정상입니다(`.gitignore`가 숨깁니다) — 보이면 고르지 말고 손.
    2. 메시지 칸에 두 줄을 쓰고 **Commit**을 누릅니다(push는 C-2 · 03에서).

        ```text
        5일차: 바이어 · 확인 기록 표와 처음 데이터 추가

        왜: 새로 고쳐도 사라지지 않게 기록을 DB에 남기려고
        ```

    3. Claude Code에 맡겨도 됩니다 — 아래 보조 프롬프트를 보내면 파일 목록 · 메시지를 먼저 보여 주고 묻습니다.

**이 단계의 목적** 표 설계와 처음 데이터를 '무엇 · 왜' 두 줄로 세이브합니다.

??? prompt "보조 프롬프트 — 세이브 포인트 1 맡기기"

    --8<-- "labs/day5/prompts_c.md:c-commit"

!!! ok "확인할 것"

    - [ ] `git log --oneline` 맨 위 `5일차: 바이어 · 확인 기록 표와 처음 데이터 추가`
    - [ ] 커밋에 `prisma/` 두 파일만 — `.env` · `lib/generated/` · `.next/` 없음

??? fix "`.env`가 소스 제어 목록에 보여요"

    고르지 말고 손을 듭니다. `.gitignore`가 바뀌었을 수 있습니다. 실수로 커밋까지 했다면 push 전에 `git rm --cached .env` → 다시 커밋하고, 그래도 걱정되면 Supabase 비밀번호를 Reset합니다.

<span class="tf-chip tf-chip--ok">획득</span> 세이브 파일 1

<p class="tf-check"><time>13:50</time> 커밋 1개 — 메시지에 왜: 줄. 10분 쉽니다</p>

### C-2 · 01 퀘스트 5 · 쪽이 금고를 읽는다 — 목록 · 상세 · 첫 화면을 DB로 (14:00–14:12) { #c2-1 .step data-tool="Claude Code · 브라우저" }

**왜** 이제 화면이 파일(`data/buyers.json`) 대신 금고를 읽습니다. 숫자는 어제와 **한 자리도** 달라지면 안 됩니다 — 같은 데이터를 다른 곳에서 읽을 뿐이니까요. 바뀌는 것은 `lib/buyers.ts`의 두 함수 속뿐이고(어제 async로 만들어 둔 까닭), 쪽마다 '요청 때마다 읽기' 한 줄이 붙습니다. **c4** → `npm run build`(ƒ 세 줄) → 브라우저에서 어제와 비교

!!! me "내가 할 일"

    1. **c4**를 보냅니다. 쓰기 허락 창(파일 4개)을 읽고 승인합니다.
    2. 켜 둔 개발 서버의 탭에서 `localhost:3000/buyers`를 새로 고칩니다(++f5++) → 어제 숫자와 견줍니다.
    3. 첫 화면 `localhost:3000`의 첫 카드 작은 글이 `Supabase DB에서 읽음`으로 바뀌었는지 봅니다 — 금고에서 읽는다는 표시입니다.

**이 단계의 목적** 쪽 셋이 파일 대신 금고를 읽게 바꾸고, 숫자가 어제와 같은지 확인합니다.

!!! prompt "프롬프트 c4 — 쪽을 DB로"

    --8<-- "labs/day5/prompts_c.md:c4"

!!! ai "AI가 하는 일"

    `lib/buyers.ts`의 두 함수 속을 DB 읽기로 바꾸고, 쪽 셋에 `export const dynamic = "force-dynamic"` 한 줄을 붙인 뒤 `npm run build`를 돌립니다(허락 창 2–4번 · 2–4분). 계산 파일 `lib/metrics.ts`는 건드리지 않습니다.

!!! ok "확인할 것"

    - [ ] `/buyers` KPI — 위험 바이어 **17곳** · C등급 채권 **$1,047,782**(전체의 **24.4%**) · 전체 채권 **$4,290,904**(150곳) · 연체 금액 **$560,191**(26곳)
    - [ ] 위험 상위 1위 **B048** · `/buyers/B048` 위험 점수 **77.0%** · 등급 C — 어제와 같다
    - [ ] build의 route 표에 `ƒ /` · `ƒ /buyers` · `ƒ /buyers/[id]`

??? ok "참고 실행 값 — 내 화면을 본 뒤 펼쳐 보기"

    어제(4일차 실습 D)와 같은 값입니다 — 데이터는 같고 읽는 곳만 바뀌었습니다.

    | 어디 | 값 |
    |---|---|
    | 등급 칩 | 전체 150 · S 126 · A 4 · B 3 · C 17 — `?grade=C`면 17줄 |
    | 위험 상위 10(순서대로) | B048 · B134 · B118 · B031 · B047 · B062 · B066 · B104 · B059 · B119 |
    | 지역별 채권(큰 순) | 동남아·남아 $1,319,352 · 동아시아 $971,884 · 북미·중남미 $733,666 · 서유럽 $543,729 · 중동·아프리카 $543,680 · 중동부유럽 $178,593 |
    | `/buyers/B048` 12칸 | 중국 · 동아시아 · 플랜트 시공(EPC) · 외상(O/A) · 30일 · $24,530 · $24,530 · 100.0% · 90일 · 30.8일 · 77.0% · C + 신호 3개 |
    | 첫 화면 카드 | 바이어 150곳 · C등급 17곳 · C등급 채권 $1,047,782(전체 미결 $4,290,904의 24.4%) |

??? fix "숫자가 어제와 달라요"

    고치기 전에 어디서 갈렸는지부터 묻습니다 — [막힐 때](#troubleshooting)의 '숫자가 다를 때' 프롬프트. 흔한 원인은 seed가 덜 들어간 것(Buyer 행 수)과 `getBuyers()`에 거르기 · 정렬을 더한 것입니다.

??? fix "화면에 `DATABASE_URL이 없습니다`가 떠요"

    개발 서버를 `.env`를 만들기 전에 켰습니다. 개발 서버 터미널에서 ++ctrl+c++ → `npm run dev`로 다시 켭니다.

??? fix "build가 `Type error: … Buyer …`로 멈춰요"

    DB가 돌려주는 모양과 어제의 형이 조금 다를 때입니다. 오류 끝 10줄을 그대로 붙여 "lib/metrics.ts는 고치지 말고 lib/buyers.ts에서 맞춰"라고 보냅니다.

<span class="tf-chip tf-chip--ok">획득</span> 어제와 같은 숫자 — 이번엔 금고에서

<p class="tf-check"><time>14:12</time> 손 점검 — /buyers 17곳 · $1,047,782 · B048 1위 · 첫 카드 'Supabase DB에서 읽음'</p>

### C-2 · 02 퀘스트 6 · 사라지지 않는 수첩 — 확인 기록 쓰기 (14:12–14:24) { #c2-2 .step data-tool="Claude Code · 브라우저" }

**왜** 드디어 미스터리를 풉니다. 상세 쪽에 '확인 기록' 칸을 달아 박 팀장님의 'B048 · 다음 주 입금 약속'을 금고에 적습니다. 저장은 **서버 액션**이 합니다 — 단추를 누르면 서버에서 도는 함수(창구)이고, 빈 메모 · 너무 긴 메모는 서버가 거릅니다. 브라우저의 검사는 건너뛸 수 있으니 진짜 문지기는 서버입니다. **c5** → 계획 승인 → 기록 하나 → 새로 고침 → 그래도 남아 있다

!!! me "내가 할 일"

    1. **c5**를 보냅니다. 계획(새 파일 3개 · 바꿀 파일 2개 · 화면)을 읽고 "좋아, 진행해" → 쓰기 허락 창을 읽고 승인합니다.
    2. `localhost:3000/buyers/B048` → 아래 **확인 기록**에서 상태 `확인 완료` · 메모 `다음 주 입금 약속` · 별명(실명 대신) → **기록 남기기**.
    3. ++f5++ — 기록이 그대로 있으면 미스터리 해결입니다.
    4. 문지기 시험 두 번 — ① 메모를 비우고 **기록 남기기** ② 이 쪽 맨 위 '상황' 문단을 통째로 복사해 메모 칸에 붙여 넣고 **기록 남기기**(200자가 넘습니다).
    5. 첫 화면 `localhost:3000`의 **최근 확인 기록**을 보고, Supabase Table Editor → `Review`도 새로 고쳐 봅니다.

**이 단계의 목적** 남긴 기록이 금고에 저장돼, 새로 고쳐도 · 다른 기기에서도 보이게 합니다.

!!! prompt "프롬프트 c5 — 확인 기록 쓰기"

    --8<-- "labs/day5/prompts_c.md:c5"

!!! ai "AI가 하는 일"

    계획을 먼저 보이고, 승인하면 `lib/reviews.ts`(읽기) · `app/buyers/[id]/actions.ts`(서버 액션 — 검사 → 저장 → 화면 새로) · `components/ReviewForm.tsx`(입력 칸)를 만들고 상세 쪽 · 첫 화면에 구역을 붙인 뒤 `npm run build`(허락 창 3–5번 · 3–5분). 검사 순서와 안내 문구는 안내서 「5. 확인 기록 쓰기」에 글자 그대로 있습니다.

!!! ok "확인할 것"

    - [ ] 기록이 맨 위에 `확인 완료 · 다음 주 입금 약속 · {별명} · 2026-10-20 14:1x` 꼴로 보이고 ++f5++ 뒤에도 남아 있다 · Table Editor `Review` **1행**
    - [ ] 빈 메모 → `메모를 적어 주세요` · '상황' 문단 → `메모는 200자 이내로 적어 주세요` — 두 번 다 `Review`는 그대로 1행
    - [ ] 첫 화면 **최근 확인 기록**에 B048 한 줄(누르면 B048 쪽)

??? ok "참고 실행 값 — 서버 검사표(안내서 「5. 확인 기록 쓰기」)"

    검사는 이 순서로 하고, 처음 걸린 하나만 보여 줍니다. 걸리면 저장하지 않습니다. 글자 수는 앞뒤 빈칸을 지운 뒤 셉니다.

    | 넣은 것 | 결과 |
    |---|---|
    | `확인 완료` · `다음 주 입금 약속` · 별명 | 저장 — `저장했습니다 — 새로 고쳐도 남아 있습니다` |
    | 메모 빈칸(빈칸만 친 것도) | `메모를 적어 주세요` |
    | 메모 201자 이상('상황' 문단은 약 310자) | `메모는 200자 이내로 적어 주세요` |
    | 메모 딱 200자 | 저장 |
    | 별명 빈칸 · 21자 이상 | `확인한 사람(별명)을 적어 주세요` · `별명은 20자 이내로 적어 주세요` |
    | 메모 · 별명 둘 다 빈칸 | `메모를 적어 주세요`(메모가 먼저) |

    시각은 서울 시각 `YYYY-MM-DD HH:MM` 꼴(`kst()`)입니다.

??? fix "저장했다는데 새로 고치면 사라져요"

    기록이 금고가 아니라 화면에만 머문 것입니다. "안내서 「5. 확인 기록 쓰기」대로 서버 액션이 db().review.create로 저장하는지, 쪽에 force-dynamic이 있는지 보여 줘"라고 묻습니다.

??? fix "'상황' 문단을 붙였는데 200자에서 잘려 들어가요"

    입력 칸에 `maxLength`가 붙어 브라우저가 잘라 낸 것입니다. 오늘은 서버 검사를 시험하려고 일부러 두지 않습니다 — "안내서 5절대로 입력 칸의 maxLength · required를 빼"라고 보냅니다.

??? fix "build가 `Only async functions are allowed to be exported in a "use server" file`"

    서버 액션 파일에서 처음 상태 값이나 형을 내보낸 것입니다. 오류 끝 줄을 붙여 "그 값은 폼 부품 쪽으로 옮겨"라고 보냅니다.

??? fix "시각이 9시간 다르게 보여요 · `Hydration failed`"

    시각 글자를 브라우저에서 만든 것입니다. "시각은 서버에서 kst()로 만들어 넘겨"라고 보냅니다.

??? fix "기록 남기기를 누를 때마다 상태 · 별명이 처음으로 돌아가요"

    React 19는 `<form action>`으로 보낸 폼을 결과와 상관없이(검사에 걸려도) 처음 값으로 되돌립니다. "안내서 5절대로 폼은 onSubmit에서 startTransition으로 보내게 고쳐"라고 보냅니다.

<span class="tf-chip tf-chip--ok">획득</span> 새로 고쳐도 남는 수첩 — 사라지는 수첩 미스터리 해결

<p class="tf-check"><time>14:24</time> 손 점검 — B048 확인 기록 1줄이 새로 고쳐도 남음 · 빈 메모 · 200자 넘김 안내</p>

### C-2 · 03 보스전 · 휴대폰에서 쓴 기록이 내 PC에도 (14:24–14:34) { #c2-3 .step data-tool="Claude Code · Vercel · 휴대폰" }

**왜** 마지막 고비 — 대표님은 휴대폰으로 보십니다. 배포 주소도 **같은 금고**를 보려면 두 가지가 필요합니다. ① 새 코드를 올린다(push) ② Vercel에도 열쇠를 준다(환경 변수 `DATABASE_URL`). 환경 변수는 저장한 뒤 **새로 만든 배포에만** 들어가므로, 넣은 다음 **Redeploy**를 한 번 누릅니다. **c6**(점검 → 커밋 → push) → Vercel 환경 변수 → Redeploy → 휴대폰 ↔ 내 PC

!!! me "내가 할 일"

    1. **c6**를 보냅니다. `doctor:secrets` 표가 모두 PASS인지, 파일 목록에 `.env`가 없는지, 브랜치가 `main`인지 읽고 승인합니다(push까지).
    2. vercel.com → 내 프로젝트 → **Settings** → 왼쪽 **Environment Variables**.
    3. 이름 `DATABASE_URL` · 값 = VS Code의 `.env`에서 `DATABASE_URL=` 줄의 **따옴표 안만** 복사(포트 `6543`인 줄) · 종류(**Type**)는 **Secret** · 대상은 **Production**과 **Preview** → **Save**. `DIRECT_URL`은 넣지 않습니다(내 PC의 표 만들기용).
    4. **Deployments** → 맨 위 배포(방금 push한 것 — 아직 Building이면 Ready가 될 때까지 기다립니다) 오른쪽 **⋯** → **Redeploy** → 창에서 다시 **Redeploy**. 새 배포가 **Ready**가 될 때까지 1–2분.
    5. 휴대폰으로 `https://tradefin-web-t{조}-{번호}.vercel.app/buyers/B048`을 엽니다 — 내 PC에서 쓴 `다음 주 입금 약속`이 보이나요?
    6. 휴대폰에서 한 줄 남깁니다 — `보류` · `휴대폰에서 시험` · 별명 → **기록 남기기**.
    7. 내 PC의 `localhost:3000/buyers/B048`에서 ++f5++ — 휴대폰 기록이 맨 위에 있으면 **보스 격파**입니다.

**이 단계의 목적** 배포 주소에도 열쇠를 주어, 휴대폰과 내 PC가 같은 금고를 보게 합니다.

!!! prompt "프롬프트 c6 — 배포 전 점검 · 출격"

    --8<-- "labs/day5/prompts_c.md:c6"

!!! ai "AI가 하는 일"

    `npm run build` → `npm run doctor:secrets`(표로) → 파일 목록 · 메시지 두 줄 · 브랜치를 먼저 보이고 → 승인하면 커밋 · `git push origin main`(허락 창 3–4번 · 1–3분). 끝에 **내게 남은 두 줄**(환경 변수 · Redeploy)을 알려 줍니다. Vercel 화면은 AI가 만지지 않습니다.

!!! ok "확인할 것"

    - [ ] `doctor:secrets` 끝 줄 `결과: PASS 6 · WARN 0 · FAIL 0` · 배포 주소 첫 화면 배지가 `production · {push한 7글자} · icn1`
    - [ ] 휴대폰의 배포 주소 `/buyers/B048`에 **내 PC에서 쓴 기록**이 보인다
    - [ ] 내 PC에 **휴대폰에서 쓴 기록**이 맨 위 · Table Editor `Review` **2행** — **같은 금고**

??? ok "참고 실행 값 — `doctor:secrets` 모양"

    ```text
    == 비밀 점검 (npm run doctor:secrets) — 커밋될 파일 …개 · .next/static …개
    ✓ PASS 추적 중인 .env 없음
    ✓ PASS 비밀번호가 든 DB 주소 없음
    ✓ PASS NEXT_PUBLIC_ 이름에 비밀 없음
    ✓ PASS 키 모양(sk-ant- · sk-proj- · ghp_ · github_pat_ · AKIA · PRIVATE KEY) 없음
    ✓ PASS .next/static에 .env 값 없음(이름 DATABASE_URL · DIRECT_URL 확인)
    ✓ PASS 실제처럼 보이는 이메일 없음(app · components · lib · data · prisma)

    결과: PASS 6 · WARN 0 · FAIL 0
    ```

    push 뒤 Redeploy 전에 배포 주소를 열면 잠깐 오류 화면이 보일 수 있습니다 — 열쇠(환경 변수)가 없는 배포라서입니다. Redeploy가 Ready가 되면 사라집니다.

??? fix "배포 주소가 `Application error` · 500이에요"

    세 가지를 차례로 봅니다 — ① Environment Variables에 `DATABASE_URL`이 있고 Production에 체크됐나 ② 저장한 **뒤에** Redeploy를 했나(맨 위 배포가 Ready인가) ③ 값에 따옴표(`"`)까지 들어가지 않았나 — Secret은 저장 뒤 값이 보이지 않으니, 헷갈리면 그 변수의 **⋯** → **Edit**에서 따옴표 안만 다시 붙여 넣고 **Save** → Redeploy. 그래도 안 되면 Vercel 프로젝트의 **Logs**에서 빨간 줄을 복사해 '원인부터' 프롬프트에 붙입니다.

??? fix "Redeploy 창에 'Use existing Build Cache'가 보여요"

    그대로 두고 **Redeploy**를 눌러도 됩니다. 환경 변수는 캐시와 상관없이 새 배포에 들어갑니다.

??? fix "링크를 열면 Vercel 로그인 화면이 떠요"

    배포마다 생기는 긴 주소(`tradefin-web-t2-07-abc123…vercel.app`)를 연 것입니다. 프로젝트의 **Domains**에 있는 짧은 운영 주소로 엽니다.

??? fix "휴대폰 기록이 내 PC에서 안 보여요"

    Vercel의 값이 다른 프로젝트(다른 금고)의 주소일 수 있습니다. Supabase Table Editor의 `Review`에 휴대폰 기록이 있으면 내 PC 쪽 문제(새로 고침 · 개발 서버), 없으면 Vercel 쪽 값을 다시 넣고 Redeploy.

??? fix "push가 `rejected` · `fetch first`로 거부돼요"

    GitHub 웹에서 먼저 고친 커밋이 있습니다. "git pull --rebase 뒤 다시 push해 줘 — 먼저 무엇을 할지 보여 줘"라고 보냅니다.

<span class="tf-chip tf-chip--ok">획득</span> 같은 금고를 보는 두 화면 — 보스 격파

<p class="tf-check"><time>14:34</time> 손 점검 — 1부 완성: 휴대폰 기록이 내 PC에 · Review 2행. 여기까지 모두 같은 앱입니다</p>

## 2부 · 자유 퀘스트 — 금고 달린 수첩, 내 마음대로 {#part2}

<div class="tf-phase" markdown>

<span class="tf-eyebrow">2부 · C-2 14:34–14:50 · Claude Code · 브라우저</span>

1부에서 모두 같은 금고 · 같은 수첩을 만들었습니다. 이제 **사양서 없이** — 하고 싶은 것을 한 줄로 말하면(몰라도 됨) AI가 재미있는 방향 3개를 먼저 제안합니다

**목표** 10분 안팎의 기능 하나로 '이런 것까지 되네?'를 하나 만든다 — 1부의 표 · 숫자는 그대로

1. 열린 프롬프트 하나(떠오르지 않으면 '아무거나')
2. AI의 방향 3개 → 고르기 → 계획 3줄 → 승인 → 만들기
3. 세이브 포인트 2 — 점검 · 커밋 · push

**결과물** 내가 고른 기능 하나 · 커밋 1개 + push

</div>

### C-2 · 04 자유 퀘스트 — 내 마음대로 키우기 (14:34–14:46) { #c2-4 .step data-tool="Claude Code · 브라우저" }

**왜** 금고가 생기면 할 수 있는 일이 확 늘어납니다 — 기록이 쌓이니 세고 · 뽑고 · 알리고 · 놀 수 있습니다. 오늘은 옵션별 설명서가 없습니다. 한 줄만 말하면 AI가 방향을 제안하고, 고르는 것은 나입니다. 열린 프롬프트 → 방향 3개 → 고르기 → 계획 3줄 → 만들기

**씨앗 — 한 줄만 골라 프롬프트의 빈칸에 넣어도 됩니다**(말 · 소리 · 알림은 오전에 본 [키 없이 30줄](class.md#no-key)의 그 브라우저 기능입니다)

- **말로 남기는 수첩**(와!) — 마이크 단추를 누르고 "B048 다음 주 입금 약속"이라고 말하면 메모 칸이 채워진다 · 브라우저 음성 인식 · 키 없음 · Chrome · Edge
- **읽어 주는 수첩**(와!) — '읽어 줘' 단추 하나로 최근 확인 기록 5개를 소리로 · 브라우저 읽기 기능 · 키 없음
- **약속 알림**(와!) — 메모에 '다음 주' · '10/27' 같은 날이 있으면 D-day 꼬리표, 그날 열면 브라우저 알림(PC Chrome · Edge) · 키 없음
- **C등급 도장 깨기**(게임) — C등급 17곳에 기록이 생길 때마다 도장 하나, 17개를 다 모으면 엔딩 화면
- **오늘의 확인왕**(게임) — 별명마다 확인한 곳 수 막대 · 1등에게 왕관 글자
- **한 과장님용 엑셀** — 확인 기록을 CSV로 내려받기(엑셀에서 한글이 안 깨지게)
- **쓰기 코드** — 공개 주소라 '그 사기꾼'도 쓸 수 있다 — 기록 전에 코드를 묻게(값은 내가 `.env` · Vercel에)

!!! me "내가 할 일"

    1. 아래 **자유 퀘스트** 프롬프트의 `{…}`를 씨앗 한 줄이나 내 말로 바꿔 보냅니다(정말 몰라도 되면 '몰라도 됨'). 떠오르지 않으면 **'아무거나'** 프롬프트를 보냅니다.
    2. AI가 보여 준 방향 3개 중 하나를 고르거나 고쳐 답합니다 — 예: "2번, 그런데 읽어 주는 목소리를 아나운서처럼".
    3. 계획 3줄을 읽고 승인 → 허락 창 → 브라우저에서 직접 해 봅니다. 마이크 · 알림은 브라우저가 권한을 물으면 **허용**.
    4. 한 번 더 키우고 싶으면 한 줄 더 보냅니다 — 끝에 "1부의 표와 숫자는 그대로"를 붙이면 안전합니다.

**이 단계의 목적** 1부의 앱을 내가 원하는 쪽으로 키워, '이런 것까지 되네?'를 하나 만듭니다.

!!! prompt "프롬프트 — 자유 퀘스트(열린 프롬프트)"

    --8<-- "labs/day5/prompts_c.md:c-free"

???+ prompt "프롬프트 — '아무거나'(가장 놀라운 것 3가지)"

    --8<-- "labs/day5/prompts_c.md:c-wow"

!!! ai "AI가 하는 일"

    안내서 「7. 자유 퀘스트」대로 방향 3개를 먼저 제안하고(아직 만들지 않습니다), 고르면 계획 3줄 → 승인 → 만들기 → `npm run build`(5–10분). 패키지 · API 키 · 바깥으로 보내기가 필요하면 만들기 전에 묻습니다 — 그때는 "키 없이 되는 길로"라고 답하면 됩니다.

!!! ok "확인할 것"

    - [ ] 1부가 그대로다 — `/buyers` KPI **17곳 · $1,047,782** · B048의 확인 기록 2줄
    - [ ] 내가 고른 기능을 브라우저에서 직접 해 봤다(AI가 보여 준 '확인할 것 3줄'대로)
    - [ ] `npm run build` 통과

??? fix "마이크 · 알림 단추를 눌러도 아무 일이 없어요"

    브라우저가 권한을 막았거나 지원하지 않는 브라우저입니다. 주소창 왼쪽 자물쇠 → 마이크 · 알림 **허용** → 새로 고침. 음성 인식은 Chrome · Edge에서, `localhost`나 `https` 주소에서만 됩니다. 알림은 PC 브라우저에서만 됩니다 — 휴대폰에서는 화면 안 꼬리표로 확인합니다.

??? fix "AI가 패키지를 설치하거나 API 키를 넣자고 해요"

    "키 없이 · 새 패키지 없이 되는 길로 다시 제안해 줘"라고 답합니다. 브라우저에 들어 있는 기능(말 · 소리 · 알림)으로 대부분 됩니다.

??? fix "표에 칸을 더하겠대요 · 'data loss'를 물어요"

    칸 더하기는 `npm run db:push`로만 합니다. 'data loss'가 보이면 고르지 말고 손 — 1부의 표를 지우는 일은 없어야 합니다.

??? fix "AI가 제안 없이 바로 만들기 시작했어요"

    Esc로 멈추고 "만들지 말고 방향 3개만 먼저 제안해 줘"라고 보냅니다.

<span class="tf-chip tf-chip--ok">획득</span> 나만의 기능 하나 — '이런 것까지 되네?'

<p class="tf-check"><time>14:46</time> 손 점검 — 내 기능 하나가 화면에 · 1부 숫자 그대로</p>

### C-2 · 05 세이브 포인트 2 — 점검 · 커밋 · push (14:46–14:50) { #c2-5 .step data-tool="Git · GitHub · Vercel" }

**왜** 자유 퀘스트 결과를 배포 주소에 올립니다. Vercel에는 이미 열쇠(`DATABASE_URL`)가 있어서 이번에는 push만으로 됩니다(Redeploy 불필요). **c-push** → `doctor:secrets` → 커밋 → push

!!! me "내가 할 일"

    1. **c-push**를 보냅니다 — 파일 목록 · 메시지 · 브랜치(`main`)를 읽고 승인합니다. 메시지는 이런 꼴입니다.

        ```text
        5일차: 자유 퀘스트 — {더한 것 한 줄}

        왜: {누가 무엇이 편해지나 한 줄}
        ```

    2. Vercel의 Deployments가 **Ready**가 되면 휴대폰으로 내 기능을 한 번 더 해 봅니다(브라우저 알림은 PC에서만 뜹니다).
    3. 17:00 쇼케이스를 실습 C로 할 분은 16:50까지 <span data-tf-link="open_chat">오픈채팅</span>에 `[발표] T{조}-{번호} / 별명 / C / 한 줄 / https://….vercel.app/buyers/B048`을 올립니다.

**이 단계의 목적** 완성한 앱을 점검하고 내 주소에 올려 둡니다.

??? prompt "보조 프롬프트 — 세이브 포인트 2"

    --8<-- "labs/day5/prompts_c.md:c-push"

!!! ok "확인할 것"

    - [ ] `doctor:secrets` 모두 PASS · 커밋 메시지 첫 줄 `5일차: 자유 퀘스트 — …`
    - [ ] 배포 주소에서 내 기능이 보인다(첫 화면 배지의 7글자 = push한 커밋)

<span class="tf-chip tf-chip--ok">획득</span> 세이브 파일 2 · 배포 주소의 내 기능

<p class="tf-check"><time>14:50</time> 커밋 2개 이상 · main push — 15:00 실습 D로 이어집니다</p>

!!! late "늦었다면"

    최소 경로는 금고(C-1 · 01) → 열쇠(C-1 · 02) → c2 → c3 → c4 → 보스전의 환경 변수 + Redeploy입니다 — '배포 주소가 금고를 읽는다'가 남습니다. 확인 기록 쓰기(c5)는 건너뛰어도 됩니다. 많이 늦었거나 4일차 쪽이 없으면 **합류**: 지금 변경을 커밋 → `npm run catchup -- day5-c` → `npm run build` → 내 금고에 `npm run db:push` → `npm run db:seed` → 커밋(`5일차: 합류 — 실습 C 기준본`) → push → 환경 변수 + Redeploy. 14:24에 아직 C-2 · 01이면 c5를 건너뛰고 c6로 — 그때까지의 코드가 올라갑니다. 2부에서 막히면 세이브 포인트 2만 합니다.

## 다 했으면 — 금고 안을 들여다보기 {#more}

자유 퀘스트까지 했으면 금고를 조금 더 들여다봅니다. 셋 다 5분 안팎이고, 바이어 표(`Buyer`)는 건드리지 않습니다.

<div class="grid cards tf-ext" markdown>

-   <span class="tf-level">기본 · 5분 · Supabase</span>

    **SQL로 금고에 묻기(읽기만)**

    Claude Code에 "Review 표에서 상태별 기록 수를 세는 SELECT 한 줄만 써 줘 — 실행은 내가 한다"를 보내고, Supabase 왼쪽 **SQL Editor**에 붙여 **Run**. 2일차 SQL 그대로입니다 — 앱의 `findMany`도 결국 `SELECT`입니다.

-   <span class="tf-level">응용 · 5분 · Supabase</span>

    **문지기를 피해 들어가면?**

    Table Editor에서 `Review`에 직접 한 줄을 넣고 메모를 300자로 채운 뒤 내 쪽을 새로 고칩니다. 앱의 '200자 검사'는 **앱을 거칠 때만** 일합니다 — 꼭 지켜야 할 규칙은 DB에도(칸 길이 제한) 둔다는 이야기. 본 뒤에는 그 줄을 지웁니다.

-   <span class="tf-level">개념 · 5분 · Claude Code</span>

    **db push와 migrate는 뭐가 다를까**

    "우리 수업이 db push를 쓰는 까닭과, migrate가 따로 남기는 것(바뀐 이력 파일)을 3줄로 — 명령은 실행하지 마"를 보냅니다. 여러 사람이 같은 금고를 바꾸는 회사에서는 그 이력이 커밋처럼 필요합니다.

</div>

## 채팅 경로 — Claude Code를 못 쓸 때 {#chat-path}

표 만들기 · 데이터 넣기는 **터미널이 필요**합니다. 그래서 채팅 경로는 '글은 claude.ai가, 명령은 내가 Codespaces 터미널에서'입니다. 진행 표시는 같은 단계 — 끝낸 단계의 '이 단계 완료'를 눌러 둡니다.

1. **Codespaces 열기** — GitHub의 내 웹 저장소 → **Code** → **Codespaces** → **Create codespace on main**(첫 준비 2–5분 · [웹 작업대 → Codespaces](../web.md#codespaces)). 터미널에서 C-0 · 01과 같은 명령을 칩니다. `.env`도 그 안에서 `npm run env:init`으로 만듭니다(커밋되지 않습니다).
2. **claude.ai 새 대화** — 안내서 「11. 채팅 경로」에 적힌 파일들(작업 안내서 · `CLAUDE.md` · `guide/design_rules.md` · `prisma/schema.prisma` · `lib/` · 쪽 파일)을 첨부하고 아래 **채팅 시작**을 먼저 보낸 뒤, c1부터 같은 문장을 보냅니다.
3. **붙여 넣기 · 명령** — AI가 파일마다 전체 내용을 주면 Codespaces 편집기에 붙여 넣고, `npm run db:push` · `npm run db:seed` · `npm run build`를 내가 칩니다. 결과 끝 10줄을 대화에 붙입니다.
4. **보스전** — Codespaces에서 '내 PC'는 포트 3000 주소(`https://…-3000.app.github.dev`)입니다. 그 주소와 휴대폰으로 같은 금고를 봅니다. 커밋 · push는 Codespaces의 소스 제어에서, Vercel은 같은 두 줄(환경 변수 · Redeploy).

비밀번호 · 연결 주소는 claude.ai 대화에도 붙이지 않습니다 — DB 상태는 `npm run doctor:db` 결과(비밀번호가 가려짐)만 붙입니다. 구독이 없어 Claude Code도 claude.ai 파일 첨부도 어려우면 **짝의 PC**에서 함께 합니다(금고는 각자의 Supabase 프로젝트로).

??? prompt "채팅 시작 — claude.ai 첫 메시지"

    --8<-- "labs/day5/prompts_c.md:c-chat"

## 막힐 때 {#troubleshooting}

단계 안의 '막히면'에 없는 것만 모았습니다.

| 증상 | 이렇게 해 보세요 |
|---|---|
| 허락 창이 계속 뜬다 | 정상입니다. 무엇을 · 어디에 읽고 `1 Yes`. `npm run db:push` · `npm run db:seed` · `npm run build` · `git` 명령은 읽고 승인합니다. 모르는 명령이면 `No` 하고 "이 명령이 뭐 하는 거야?" |
| AI가 `.env`를 열겠다고 한다 | `No`. 저장소 설정이 막지만, 허락 창이 뜨면 거절합니다 — 값은 내가 다룹니다 |
| `npm run doctor:db`에 `✗` 줄 | 그 줄의 `→`를 따라 고칩니다. 모르겠으면 아래 'DB 오류 — 원인부터'에 결과를 붙입니다(비밀번호는 가려져 있습니다) |
| `db push`가 data loss를 묻는다 | 고르지 말고 손 — 이미 있는 칸을 바꾸거나 지우려는 것입니다 |
| 배포 주소만 500 | 보스전의 막히면 — 환경 변수 · Redeploy · 값의 따옴표 → Vercel **Logs** |
| `.env`를 커밋 · push했다 | 손을 듭니다 → `git rm --cached .env` → 커밋 → Supabase에서 비밀번호 Reset → `.env`와 Vercel 두 곳 고치고 Redeploy |
| Supabase 프로젝트가 Paused | 대시보드에서 **Restore** — 무료 프로젝트는 1주 넘게 안 쓰면 쉽니다 |
| 회사망이 5432 · 6543을 막는다 | 휴대폰 핫스팟 → [채팅 경로](#chat-path)의 Codespaces |
| 사용 한도에 걸렸다 | 풀리는 시각을 확인하고, 그동안은 짝의 화면이나 채팅 경로로 → [FAQ](../faq.md#q-usage-limit) |
| 대화가 길어져 AI가 앞 단계를 잊는다 | 새 대화를 열고 "@guide/day5_lab_c.md 를 읽고 「N. …」부터 이어서"로 시작합니다 — 규칙은 안내서에, 결과는 금고와 저장소에 다 있습니다 |

??? prompt "DB 오류 — 원인부터(고치기 전에)"

    --8<-- "labs/day5/prompts_c.md:c-dbfix"

??? prompt "숫자가 다를 때 — 어디서 갈렸나"

    --8<-- "labs/day5/prompts_c.md:c-check"

`{오류 끝 10줄}` · `{항목}` · `{화면 값}` · `{기대값}`을 바꿔 보냅니다. 원인을 찾은 뒤 "고쳐"라고 하면 한 번에 하나씩 고칩니다.
