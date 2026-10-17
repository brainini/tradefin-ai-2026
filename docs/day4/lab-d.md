---
title: 4일차 실습 D — 첫 웹앱 + 배포
---

<div class="tf-lab" markdown>
<span class="tf-eyebrow">4일차 · 실습 D · 6–7교시 · 15:00–16:50 <span class="tf-daystate" data-tf-daystate="4"></span></span>

# 실습 D — 첫 웹앱 + 배포

<div class="tf-meta" markdown>
<span class="tf-chip tf-chip--time">준비 15:00–15:25 · 장비 획득</span>
<span class="tf-chip tf-chip--time">1부 15:25–15:50 · 같이 따라 하기</span>
<span class="tf-chip tf-chip--time">2부 16:00–16:50 · 자유 퀘스트</span>
<span class="tf-chip tf-chip--tool">Claude Code · Manual + Plan</span>
<span class="tf-chip tf-chip--tool">GitHub · Vercel</span>
<span class="tf-chip tf-chip--tool">채팅 경로 가능</span>
</div>

<div class="tf-flow" markdown>
<div markdown><b>상황</b> (가상) 한빛정밀(주) 디지털 TF, 월요일 15:00. 금요일의 리스크 보드는 대표님 마음에 쏙 들었지만 링크가 하나뿐이라, 회의 중에 바이어 한 곳을 보여 주려면 모두가 스크롤을 합니다. 이번 주 TF로 차출된 최 대리(나)에게 떨어진 미션 — "바이어 150곳에 **각자의 주소**를 달고, 대표님 휴대폰으로 **B048의 주소**를 보내라. 서버도 예산도 없이."</div>
<span>→</span>
<div markdown><b>넣는 것</b> 스타터 템플릿(이미 동작하는 첫 쪽 · 부품 8개 · `data/buyers.json` 150곳) + 작업 안내서 `guide/day4_lab_d.md` · 화면 규칙 `guide/design_rules.md` + 두 줄짜리 프롬프트</div>
<span>→</span>
<div markdown><b>얻는 것</b> 내 웹 주소 `https://tradefin-web-t{조}-{번호}.vercel.app` · 목록 쪽 `/buyers` · 바이어마다 하나씩 생기는 상세 쪽 `/buyers/B048` · 내가 고른 자유 퀘스트 · `main`의 커밋 2개 이상(push = 자동 배포)</div>
</div>

<div class="tf-lab__grid" markdown>
<div class="tf-lab__cell" markdown><span class="tf-lab__label">목표</span> **처음으로 내 웹앱을 세상에 띄웁니다** — 템플릿으로 내 저장소를 만들고(GitHub), 클릭 몇 번으로 운영 주소를 받고(Vercel), 내 PC에서 쪽 두 개를 더해 push하면 그 주소가 새 판으로 바뀝니다. **1부는 모두 같은 쪽 · 같은 숫자**, **2부는 자유 퀘스트** — 하고 싶은 것 한 줄로 '이런 것까지 되네'를 찾습니다</div>
<div class="tf-lab__cell" markdown><span class="tf-lab__label">오전과의 관계</span> 오전에 본 지도를 손으로 한 번 걷습니다 — 여러 모양 중 **가장 범용인 웹앱**(주소 하나 · 설치 없음 · 어느 기기든) · **내 PC → GitHub → Vercel 한 방향** · **서버에서 계산, 화면은 가볍게** · **운영 주소와 배포별 주소**. 숫자는 금요일 보드와 같은 150곳이고, 새로 만드는 모델은 없습니다</div>
</div>

<div data-tf-map></div>
</div>

!!! quote "디지털 TF 단톡방 — 오늘 14:58"

    **대표님** 금요일 보드 잘 봤어요. 그런데 회의 중에 "B048 좀" 하면 다들 30초씩 스크롤하더군요. 바이어마다 주소를 주세요. 안 바뀌는 걸로.

    **수출팀 박 팀장** B048이면 그 플랜트 현장 건이죠… 주소 생기면 저도 주세요. 걱정돼서 하루에 세 번은 열어 볼 겁니다.

    **재무팀 한 과장** 화면 숫자가 장부랑 1달러라도 다르면 바로 전화드립니다.

    **IT팀 오 주임** 서버는 없습니다. 예산도 없습니다. …요즘은 둘 다 없어도 된다고 하더군요.

    **최 대리(나)** 두 시간이면 됩니다. 설치만 안 막히면요.

!!! file "작업 안내서란? — `guide/day4_lab_d.md`"

    3일차와 같은 방식입니다. 긴 규칙은 **파일**에 적어 두고 프롬프트는 **목적**만 말합니다. 오늘은 안내서가 따로 받을 필요 없이 **템플릿 안**(`guide/`)에 들어 있어서, 내 저장소를 만드는 순간 함께 생깁니다. 프롬프트는 "「2. 목록 쪽」대로"처럼 절을 가리키고, 화면 모양은 모든 웹 실습이 함께 쓰는 `guide/design_rules.md`(토큰 색 · 'AI 티' 금지 · 휴대폰 390px · 44px 단추)를 따릅니다.

    | 누가 | 무엇을 |
    |---|---|
    | 나 | 프롬프트를 보내고, 허락 창을 읽고, 아래 '확인할 것'의 숫자와 견준다 · 브라우저와 휴대폰으로 직접 열어 본다 |
    | AI | 안내서의 그 절과 `CLAUDE.md`를 읽고 그대로 만든 뒤 `npm run build`까지 통과시키고, 끝에 '확인할 것' 3줄을 보여 준다 |
    | 안내서 | 모두가 같은 쪽 · 같은 숫자를 얻도록 파일 이름 · 계산 · 구역을 고정해 둔다 — 절은 0 늘 지킬 것 · 1 저장소 둘러보기 · 2 목록 쪽 · 3 상세 쪽 · 4 화면 규칙 · 5 검사 · 커밋 · push · 6 자유 퀘스트 · 7 배포 확인 · 8 막힐 때 · 9 숫자가 다를 때 · 10 채팅 경로 |

## 시작 전 확인 {#before}

실습 C에서 바로 이어집니다. 14:50–15:00 쉬는 시간에 다섯 줄을 봐 둡니다. 실습 C의 [기다리는 동안 — 장비 획득](lab-c.md#gear)을 했다면 절반은 끝나 있습니다.

<div class="tf-checklist" data-title="시작 전 확인 5가지" markdown>

- [ ] 실습 C를 커밋 · push했다(멈춘 자리여도 커밋까지) — 실습 D는 **새 저장소**에서 하고, 과정 저장소는 그대로 둡니다
- [ ] Node.js 24를 설치했다(실습 C 13:03) — 안 했으면 D-0 · 01에서
- [ ] vercel.com에 **Continue with GitHub**로 가입했다(Hobby · 실습 C 13:22)
- [ ] supabase.com 가입(내일 씁니다 · 실습 C 14:03) — 안 했으면 D-0 · 03의 빌드를 기다리는 동안
- [ ] 회사 실데이터 · 실명 · 회사 이름은 웹앱에도 AI 도구에도 넣지 않는다 — 내 웹 주소는 **누구나** 열 수 있다

</div>

이 쪽의 단축키는 Windows 기준입니다. Mac은 ++ctrl++ 대신 ++cmd++를 누르고(미리보기 ++cmd+shift+v++), 터미널 ++ctrl+grave++와 소스 제어 ++ctrl+shift+g++만 Mac에서도 ++ctrl++입니다.

## 오늘의 장비 — 스타터 템플릿 {#starter}

오늘은 파일을 받지 않습니다. 템플릿 <https://github.com/brainini/tradefin-web-starter>로 **내 저장소**를 만들면(D-0 · 02) 아래가 모두 들어 있고, 첫 쪽은 **이미 동작합니다** — 1부는 '잘 되는 것'에서 출발합니다. 채팅 경로만 ZIP으로 받습니다 — [템플릿 ZIP](https://github.com/brainini/tradefin-web-starter/archive/refs/heads/main.zip)(또는 내 저장소의 **Code → Download ZIP**).

| 자리 | 들어 있는 것 | 오늘 |
|---|---|---|
| `app/page.tsx` | 첫 쪽 '한빛정밀 웹 작업대' — 큰 숫자 3개 · '이 쪽이 보이면 배포 성공' · 배포 배지 | 그대로(배포 확인용) |
| `app/api/health/route.ts` | 배포 배지가 부르는 주소 — 어디서 · 어느 커밋으로 도는지 | 그대로 |
| `components/` | 부품 8개 — 메뉴 `SiteNav` · 쪽 머리 `PageHeader` · 큰 숫자 `KpiCard` · 등급 `GradeBadge` · 막대 `BarRow` · 표(휴대폰은 카드) `DataTable` · 알림 `Notice` · 배지 `DeployBadge` | 가져다 씀 |
| `lib/format.ts` | 숫자 모양 — `usd()` → $1,047,782 · `pct()` → 77.0% · `int()` · `krw()` · `kst()` | 가져다 씀 |
| `data/buyers.json` | 바이어 150곳 × 16칸 — 금요일 보드와 같은 합성 데이터 | **읽기만** |
| `guide/` | 작업 안내서 `day4_lab_d.md` · 화면 규칙 `design_rules.md` · 5 · 6일차 안내서 | AI가 읽음 |
| `CLAUDE.md` | 이 저장소의 규칙 — 버전 고정 · 데이터와 비밀은 서버에서만 · build 통과 전엔 '완료' 금지 | AI가 매번 읽음 |
| `scripts/doctor.mjs` | 막히면 먼저 — `npm run doctor`가 `✓` · `✗`와 고치는 법을 한국어로 | 실행만 |
| `prisma/` · `lib/db.ts` | 내일(5일차) DB를 붙일 자리 | 오늘은 안 씀 |

**`data/buyers.json`의 칸** — 이름은 영어, 뜻은 아래와 같습니다(3일차 `buyer_board.csv`를 웹앱용 이름으로 바꾼 것).

| 칸 | 뜻 | 예(B048) |
|---|---|---|
| `id` · `name` | 바이어 번호 · 이름(가상 회사) | B048 · Changzhou Wenant Engineering Co., Ltd. |
| `countryCode` · `countryKo` | 나라 코드 · 한글 나라 이름(20개 나라) | CHN · 중국 |
| `region` · `industry` | 지역 6개 · 업종 6개 | 동아시아 · 플랜트 시공(EPC) |
| `paymentMethod` · `termsDays` | 결제방식 · 결제기간(일) | 외상(O/A) · 30 |
| `openArUsd` · `overdueUsd` | 받을 돈(채권) · 그중 기일이 지난 돈(연체), 달러 | 24530 · 24530 |
| `pctAr31p` | 채권 중 기일을 31일 넘긴 몫(0–1, 채권이 0이면 없음) | 1.0 |
| `oldestOpenDays` · `avgDaysLate12m` | 가장 오래 밀린 인보이스의 연체일 · 최근 1년 평균 지연일(없을 수 있음) | 90 · 30.8 |
| `pd30d` · `grade` | 위험 점수(0–1, 이미 매긴 값) · 신호등 등급 S · A · B · C | 0.7699 · C |
| `signals` | 위험 신호(쉬운 말, 1–3개) | 최근 1년 분쟁 비율 50% · … |

## 오늘의 지도 — 세 군데, 한 방향 {#map}

웹앱은 세 군데를 한 방향으로 흐릅니다. 이 표 하나가 오늘 오후의 전부입니다.

| 자리 | 하는 일 | 주소 · 누가 보나 |
|---|---|---|
| **내 PC** | 코드를 고치고 바로 미리 본다 — `npm run dev` | `http://localhost:3000` — 나만 |
| **GitHub** | 코드를 보관하고 기록한다 — 커밋 = 세이브 포인트 | `github.com/내 아이디/tradefin-web-T2-07` |
| **Vercel** | push를 받으면 빌드해서 세상에 띄운다 | `https://tradefin-web-t2-07.vercel.app` — **누구나** |

- **한 방향** — 내 PC에서 고침 → 커밋 → push → Vercel이 저절로 빌드 → 운영 주소가 새 판으로 → 대표님 휴대폰.
- **빌드가 실패하면** Vercel은 지난번 잘 된 판을 그대로 띄워 둡니다 — 대표님 화면은 깨지지 않습니다.
- **주소는 두 가지** — Domains의 짧은 주소가 **운영 주소**(대표님께 보낼 것). 배포마다 생기는 긴 주소(`…-abc123xyz-….vercel.app`)는 Vercel 로그인 벽이 있는 **임시 출입증**입니다. 그 사기꾼도 한 글자 다른 주소를 좋아하니, 주소는 언제나 Domains에서 복사합니다.

## Lv0 · 장비 획득 — 주소가 먼저 {#d0}

<div class="tf-phase" markdown>

<span class="tf-eyebrow">준비 · 실습 D-0 · 15:00–15:25 · 터미널 · GitHub · Vercel · VS Code</span>

장비 넷 — 클라우드에 주소부터, 내 PC는 그다음

**목표** 내 저장소와 운영 주소를 먼저 만들고(클라우드), 내 PC에서 같은 쪽을 띄운다 — 내 PC 설치가 느려도 주소는 이미 있다

1. Node 24 확인 — `node -v`
2. 템플릿으로 내 저장소 — Use this template
3. Vercel에 첫 배포 — Import → Deploy → 운영 주소
4. 내 PC 작업대 — Clone → `npm ci` → `npm run doctor` → `npm run dev`(15:25 규칙)

**결과물** 내 저장소 `tradefin-web-T{조}-{번호}` · 운영 주소 · `localhost:3000`

</div>

### D-0 · 01 장비 획득 · Node 24 확인 (15:00–15:03) { #d0-1 .step data-tool="터미널" }

**왜** Node.js는 웹앱의 엔진입니다 — 내 PC에서 웹앱을 돌리고 빌드하는 프로그램이고, npm은 그 부품 가게입니다. 실습 C 시간에 설치했다면 확인만 합니다. VS Code 재시작 → `node -v` → v24

!!! me "내가 할 일"

    1. VS Code를 **완전히 끄고**(창을 모두 닫기) 다시 켭니다 — 설치한 Node를 새 터미널이 알아보게.
    2. 아무 창에서나 터미널(++ctrl+grave++)을 열고 한 줄을 실행합니다. `npm`은 아직 치지 않습니다 — 지금 열린 과정 저장소 창의 터미널은 Windows에서 PowerShell이라 `npm`이 빨간 글자로 막힐 수 있습니다. npm은 D-0 · 04의 웹 저장소 터미널(명령 프롬프트)에서 `npm run doctor`가 확인합니다.

        ```text
        node -v
        ```

    3. Node를 모른다는 글이 나오면 — `'node'은(는) 내부 또는 외부 명령 … 아닙니다`(명령 프롬프트) · `'node' 용어가 … 인식되지 않습니다`(PowerShell) · `command not found: node`(Mac) — 지금 설치합니다. <https://nodejs.org/dist/v24.22.0/> → Windows `node-v24.22.0-x64.msi` · Mac `node-v24.22.0.pkg`(열어서 기본값으로 설치). Windows는 실행 → **Next** → **라이선스 동의에 체크** → **Next** 세 번 → 'Tools for Native Modules' 화면은 **'Automatically install the necessary tools' 칸을 비운 채**(체크돼 있으면 해제) **Next** → **Install**(Next는 모두 다섯 번 · 관리자 확인 창이 뜨면 **예**) → Finish. 강의장 USB에도 같은 파일이 있습니다. 설치가 끝나면 1번부터 다시.
    4. 회사 PC라 관리자 권한이 없어 설치가 막히면 — 설치 없이 D-0 · 02 · 03을 하고, D-0 · 04에서 **Codespaces 길**로 갑니다.

!!! ok "확인할 것"

    - [ ] `node -v` → `v24.22.0`(`v24.`로 시작하면 됩니다) — npm은 D-0 · 04의 `npm run doctor`가 확인합니다
    - [ ] 관리자 권한이 없다면 D-0 · 04의 Codespaces 길을 기억해 둠

??? fix "`npm`을 쳤더니 빨간 글자 — `… npm.ps1 파일을 로드할 수 없습니다`"

    고장이 아닙니다. Windows PowerShell의 기본 보안 설정이 npm의 스크립트 파일(`npm.ps1`)을 막은 것입니다. 지금 확인만 하려면 `npm.cmd -v`(`11.`로 시작하면 됩니다). D-0 · 04에서 여는 웹 저장소의 터미널은 **명령 프롬프트(cmd)**라 `npm`을 그대로 씁니다. 자세히는 [준비 9-2](../setup.md#npm-policy).

??? fix "`v22.…` · `v20.…`처럼 옛 판이 나와요"

    전에 깔린 Node가 남아 있습니다. 24.22.0 설치 파일을 그대로 실행하면 덮어씁니다. 설치 뒤 VS Code를 완전히 끄고 다시 켭니다 — 열려 있던 터미널은 옛 판을 기억합니다.

??? fix "설치했는데도 `node`를 모른대요"

    VS Code를 완전히 끄지 않은 경우가 대부분입니다(창 하나라도 남으면 그대로). 그래도 안 되면 PC를 다시 시작합니다. Mac은 터미널을 새 창으로 엽니다.

**획득:** Node 24 — 웹앱 엔진

### D-0 · 02 장비 획득 · 템플릿으로 내 저장소 (15:03–15:07) { #d0-2 .step data-tool="GitHub" }

**왜** 템플릿은 '빵틀'입니다 — 그대로 찍어 **내 저장소**를 만들어야 내가 push할 수 있고, Vercel이 내 것을 띄웁니다. 과정 저장소(`tradefin-my-…`)와는 따로입니다. 템플릿 → Use this template → 내 저장소

!!! me "내가 할 일"

    1. <https://github.com/brainini/tradefin-web-starter>를 엽니다(GitHub에 로그인한 채).
    2. 오른쪽 위 초록 단추 **Use this template → Create a new repository**.
    3. **Owner**는 나 · **Repository name** `tradefin-web-T{조}-{번호}`(예: `tradefin-web-T2-07`) · **Public** · 'Include all branches'는 끈 채로 → **Create repository**.

!!! ok "확인할 것"

    - [ ] 내 저장소 첫 화면에 `CLAUDE.md` · `guide/` · `data/`가 보인다
    - [ ] 저장소 이름이 `tradefin-web-T2-07` 꼴이고 **Public**이다

??? fix "Use this template 단추가 안 보여요"

    로그인했는지 봅니다(오른쪽 위에 내 프로필 사진). 창이 좁으면 단추가 줄어 보입니다 — 창을 넓히거나 브라우저 확대를 100%로.

??? fix "이름을 잘못 지었어요"

    Vercel에 연결하기 전이면 내 저장소 → **Settings** → Repository name을 고치고 **Rename**. 이미 연결했다면 그대로 둡니다 — 이름이 조금 달라도 실습은 같습니다.

<p class="tf-check"><time>15:07</time> 손 점검 — 내 저장소 tradefin-web-T○-○○가 Public으로 보인다</p>

**획득:** 내 저장소 — 내 코드의 집

### D-0 · 03 장비 획득 · Vercel에 첫 배포 — Import → Deploy (15:07–15:15) { #d0-3 .step data-tool="Vercel" }

**왜** 빌드는 Vercel의 컴퓨터가 합니다. 그래서 내 PC 설치가 느려도 **주소는 먼저** 생깁니다 — 오늘 대표님께 보낼 주소가 여기서 태어납니다. Import → Deploy → Domains의 운영 주소

!!! me "내가 할 일"

    1. <https://vercel.com> → **Log in → Continue with GitHub**(가입은 실습 C 때 했습니다. 아직이면 **Sign Up → Hobby → Continue with GitHub**, 휴대폰 문자 인증을 물으면 합니다).
    2. **Add New… → Project**. 'Import Git Repository' 목록에 내 저장소가 없으면 **Install**(또는 **Adjust GitHub App Permissions →**) → GitHub 화면에서 **Only select repositories** → `tradefin-web-T2-07` → **Install**(또는 Save).
    3. 내 저장소 옆 **Import** → 설정은 **하나도 바꾸지 않고** → **Deploy**. 1–3분 걸립니다.
    4. 기다리는 동안(가입이 아직이면) — <https://supabase.com> → **Start your project → Continue with GitHub** → 기본 Free 조직 그대로. 프로젝트는 만들지 않습니다(내일 함께).
    5. 축하 화면이 뜨면 **Continue to Dashboard** → **Domains**에 보이는 짧은 주소(예: `tradefin-web-t2-07.vercel.app`)를 눌러 엽니다. 이 주소를 메모장에 적어 둡니다 — **운영 주소**.

!!! ok "확인할 것"

    - [ ] 첫 쪽 '한빛정밀 웹 작업대' — 바이어 **150곳** · C등급 **17곳** · C등급 채권 **$1,047,782**
    - [ ] 아래 배지가 `production · ○○○○○○○ · icn1`(가운데 7글자는 커밋 번호, `icn1`은 서울)
    - [ ] 주소가 Domains의 짧은 주소다 — `-abc123xyz-`가 낀 긴 주소가 아니다

!!! info "빌드 기록에서 볼 두 줄"

    배포 화면의 **Build Logs**를 열면 `prisma generate`가 끝났다는 줄(`✔ Generated Prisma Client`)과 `▲ Next.js 16.4.2` 줄이 보입니다. 내 PC에서 `npm run build`를 하면 같은 줄이 나옵니다 — Vercel은 내 저장소를 받아 **똑같은 명령**을 돌립니다.

??? fix "Import 목록에 내 저장소가 없어요"

    Vercel의 GitHub 앱이 그 저장소를 볼 권한이 없습니다. 목록 아래 **Adjust GitHub App Permissions →** → Repository access에서 **Only select repositories** → `tradefin-web-T2-07` 추가 → **Save** → Vercel 화면으로 돌아와 새로 고침.

??? fix "빌드가 Error로 끝났어요"

    Import 화면에서 설정을 바꿨는지 봅니다 — Framework Preset `Next.js` · Root Directory `./` 그대로여야 합니다. 바꿨다면 프로젝트 → **Settings → Build and Deployment**에서 되돌리고 **Deployments → … → Redeploy**. 그래도 Error면 Build Logs의 빨간 줄을 캡처해 손을 듭니다.

??? fix "주소를 열었더니 Vercel 로그인 화면이 나와요"

    배포별 긴 주소(`tradefin-web-t2-07-abc123xyz-….vercel.app`)를 연 것입니다. 프로젝트 첫 화면의 **Domains** 주소를 엽니다 — 그 주소는 로그인 없이 누구나 열립니다.

??? fix "주소가 `tradefin-web-t2-07-○○○.vercel.app`처럼 끝이 붙어 있어요"

    같은 이름이 이미 있어서 Vercel이 다른 짧은 주소를 준 것입니다. **Domains**에 있는 그 주소가 내 운영 주소입니다 — 그대로 씁니다.

<p class="tf-check"><time>15:15</time> 손 점검 — 운영 주소에서 첫 쪽 · 배지 production · icn1</p>

**획득:** 운영 주소 — 세상에 하나뿐인 내 웹 주소

### D-0 · 04 장비 획득 · 내 PC 작업대 — Clone → npm ci → doctor → dev (15:10–15:25) { #d0-4 .step data-tool="VS Code · 터미널" }

**왜** 고치는 일은 내 PC에서 하고, 미리 보기는 `localhost`에서 합니다. `npm ci`는 웹앱 부품을 잠금 파일(`package-lock.json`)에 적힌 판 그대로 받는 일이라 강의장 Wi-Fi에서 2–20분 걸립니다 — 그동안 화면은 이미 Vercel에 떠 있습니다. `Git: Clone` → `npm ci` → `npm run doctor` → `npm run dev`

!!! me "내가 할 일"

    1. VS Code → ++ctrl+shift+p++ → `Git: Clone` → **Clone from GitHub** → `tradefin-web-T2-07` → 폴더 `C:\work`(Mac은 `~/work`) 고르기 → **Open** → **Yes, I trust the authors**. 창 제목에 `tradefin-web-T2-07` — 과정 저장소 창과 헷갈리지 않게 봐 둡니다.
    2. 새 터미널(++ctrl+grave++)을 엽니다 — Windows는 이 저장소의 설정으로 **명령 프롬프트(cmd)**가 열립니다. 부품을 받습니다.

        ```text
        npm ci
        ```

    3. `added … packages`가 나오면 점검하고 켭니다.

        ```text
        npm run doctor
        npm run dev
        ```

    4. 터미널의 `http://localhost:3000`을 ++ctrl++ + 클릭합니다. 이 터미널은 **켜 둔 채** 둡니다 — 끄면 미리 보기도 꺼집니다(끌 때는 ++ctrl+c++). 다른 명령은 터미널 오른쪽 위 **+**로 새 터미널에서.
    5. Claude Code 패널을 **이 창에서** 열고 모드를 **Manual**로 둡니다.

!!! warning "15:25 규칙 — `npm ci`가 안 끝났으면 Codespaces로"

    내 저장소(GitHub) → 초록 **Code → Codespaces → Create codespace on main**. 브라우저에 VS Code가 열리고 `npm ci`가 저절로 돕니다(3–5분). 끝나면 그 터미널에서 `npm run doctor` → `npm run dev` → 오른쪽 아래 알림의 **Open in Browser**. Claude Code 패널에도 로그인합니다. 내 PC의 `npm ci`는 그대로 두어도 됩니다 — 끝나면 내일부터 내 PC로 합니다.

!!! ok "확인할 것"

    - [ ] `npm run doctor` 맨 아래 결과 줄에 `✗ 0` — `– .env 없음(5일차)`는 정상입니다(내일 만듭니다)
    - [ ] `localhost:3000`에 운영 주소와 같은 첫 쪽 · 배지 `내 PC · development`
    - [ ] Claude Code 패널이 `tradefin-web-T2-07` 창에서 열리고 모드가 Manual

??? fix "PowerShell에서 `npm.ps1 … 이 시스템에서 스크립트를 실행할 수 없으므로`"

    PowerShell 터미널이 열린 것입니다. 터미널 오른쪽 위 **∨ → Command Prompt**로 새 터미널을 엽니다. 꼭 PowerShell이어야 하면 `npm.cmd ci`처럼 `npm.cmd`로 쓰거나, 한 번만 `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`(묻으면 `Y`).

??? fix "`npm ci`가 10분째 그대로 · `ETIMEDOUT` · `ECONNRESET`"

    강의장 Wi-Fi에 스무 명이 한꺼번에 받는 중입니다. 화면은 이미 Vercel에 떠 있으니 기다리며 아래 1부 소개를 읽어 둡니다. 15:25에도 안 끝나면 위의 Codespaces 길로. 강사 USB가 돌면 `npm ci --cache <USB의 npm-cache 폴더> --prefer-offline`.

??? fix "설치 끝 무렵 `binaries.prisma.sh`에 연결하지 못한대요"

    DB 도구(Prisma)의 부품 하나를 받는 주소인데, 회사망 · 강의장 망이 막았을 수 있습니다. 휴대폰 핫스팟에 붙여 `npm ci`를 다시 하거나 Codespaces로 갑니다.

??? fix "doctor에 `✗`나 `!` 줄이 있어요"

    `✗`는 지금 고칠 것, `!`는 알아 둘 것입니다. 줄마다 아래 `→`에 고치는 법이 한국어로 적혀 있습니다 — 그대로 합니다. 'claude를 찾지 못했습니다' · '홈 폴더 경로에 한글' 같은 `!` 줄은 오늘은 그대로 두어도 됩니다(claude는 내일 씁니다). '연결 안 됨'이면 와이파이를 바꾸거나 휴대폰 핫스팟으로.

??? fix "`Port 3000 is in use` · 3001로 열렸어요"

    다른 프로그램이 3000번을 쓰고 있습니다. 터미널의 `Local:` 줄 주소(`http://localhost:3001`)를 엽니다. `npm run dev`를 두 번 켠 것이면 하나를 ++ctrl+c++로 끕니다.

<p class="tf-check"><time>15:25</time> 손 점검 — localhost:3000의 첫 쪽(또는 Codespaces) · Claude Code 패널이 이 창에</p>

**획득:** 내 PC 작업대 — 고치면 1초 만에 보이는 미리 보기

## 1부 · 같이 따라 하기 — 모두 같은 결과 {#d1}

<div class="tf-phase" markdown>

<span class="tf-eyebrow">1부 · 실습 D-1 · 15:25–15:50 · Claude Code · Git · Vercel</span>

둘러보고 → 쪽 두 개 → push하면 운영 주소가 새 판으로 — 모두 같은 쪽, 같은 숫자

**목표** 이 쪽 그대로 따라 해 `/buyers`(목록)와 `/buyers/[id]`(상세)를 만들고 운영 주소에 올린다 — 누가 해도 숫자가 같다

1. 퀘스트 1 · 마을 지도 — 저장소 둘러보기(읽기만)
2. 퀘스트 2 · 150곳에 문패 달기 — 목록 · 상세 쪽(Plan)
3. 보스전 · 대표님 휴대폰에 B048 주소 보내기 — 세이브 포인트 · push · 배포

**결과물** `lib/buyers.ts` · `lib/metrics.ts` · `app/buyers/` 아래 쪽 파일 3개 · 메뉴 한 줄 · 커밋 1개 · 운영 주소의 `/buyers/B048`

</div>

### D-1 · 01 퀘스트 1 · 마을 지도 — 저장소 둘러보기(읽기만) (15:25–15:28) { #d1-1 .step data-tool="Claude Code" }

**왜** 이 저장소에는 이미 부품 8개와 데이터가 있습니다. 새로 만들기 전에 '있는 것'부터 알면 AI도 사람도 덜 헤맵니다 — 있는 부품을 다시 만들면 화면마다 모양이 달라집니다. 저장소 → **d1**(읽기만) → 표 다섯 개

!!! me "내가 할 일"

    1. Claude Code 모드가 **Manual**인지 보고 아래 **d1**을 보냅니다.
    2. 파일을 읽고 세는 허락 창이 1–3번 뜹니다 — 무엇을 실행하는지 읽고 `1 Yes`.

**이 단계의 목적** 화면을 만들기 전에 이 저장소에 이미 있는 부품과 데이터를 파악한다.

!!! prompt "프롬프트 d1 — 저장소 둘러보기(읽기만)"

    --8<-- "labs/day4/prompts_d.md:d1"

!!! ok "확인할 것"

    - [ ] 부품 **8개** 표 — SiteNav · PageHeader · KpiCard · GradeBadge · BarRow · DataTable · Notice · DeployBadge(브라우저 부품은 DeployBadge 하나)
    - [ ] `lib/format.ts`의 함수 5개(`usd` · `krw` · `pct` · `int` · `kst`) · `data/buyers.json` **150줄 × 키 16개**
    - [ ] 다음 계획 — 쪽 2개 `/buyers`(목록) · `/buyers/[id]`(상세), 파일은 아직 하나도 만들지 않았다

!!! ai "AI가 하는 일"

    안내서 「1」을 읽고 `components/` · `lib/` · `data/` · `app/`을 엽니다. 줄 수와 빈칸을 세는 짧은 `node` 명령을 실행하고(허락 창 1–3번 · 1분 안팎) 표 다섯 개로 답합니다. 파일은 만들지 않습니다.

??? fix "AI가 바로 파일을 만들기 시작했어요"

    ++esc++로 멈추고 "안내서 0절대로 — 1절은 읽기만. 방금 만든 파일이 있으면 알려 줘"라고 보냅니다. 만든 파일은 허락 창에서 `No`를 눌렀다면 생기지 않았습니다.

??? fix "안내서를 찾을 수 없대요 · `@guide`가 칩으로 안 붙어요"

    창 제목을 봅니다 — 과정 저장소 창에서 보냈을 수 있습니다. `tradefin-web-T2-07` 창의 Claude Code 패널에서 다시 보냅니다. 입력창에 `@guide/day4`까지 치고 Tab을 눌러 칩으로 붙는지도 봅니다.

<p class="tf-check"><time>15:28</time> 손 점검 — d1 답에 부품 8개 · 150줄 × 16키</p>

**획득:** 마을 지도 — 무엇이 어디에 있는지

### D-1 · 02 퀘스트 2 · 150곳에 문패 달기 — 목록 · 상세 쪽 (15:28–15:45) { #d1-2 .step data-tool="Claude Code · Plan · 브라우저" }

**왜** "바이어마다 주소"는 웹앱에서 **'쪽 하나 = 주소 하나'**입니다. 목록 쪽 `/buyers`는 150곳을 한 화면에, 상세 쪽은 폴더 이름 `[id]`의 대괄호 자리에 B048 · B134 …가 들어가 **파일 하나로 주소 150개**가 생깁니다. 숫자는 서버에서 `data/buyers.json`으로 계산하고, 화면은 있는 부품으로 그립니다. 안내서 「2」 · 「3」 → **d2**(Plan) → 파일 5개 + 메뉴 한 줄 → `npm run build`

!!! me "내가 할 일"

    1. 모드를 **Plan**으로 바꾸고 **d2**를 보냅니다 — 큰 작업이라 계획부터 읽습니다.
    2. 계획에서 세 가지를 봅니다 — **새 파일 5개**(`lib/buyers.ts` · `lib/metrics.ts` · `app/buyers/page.tsx` · `app/buyers/[id]/page.tsx` · `app/buyers/[id]/not-found.tsx`) + **고칠 곳 1줄**(`components/SiteNav.tsx`의 메뉴) · 쪽마다 구역 순서 · 마지막 `npm run build`. 맞으면 승인 창에서 **`2 Yes, and manually approve edits`**. 계획 끝의 '정해 주세요'는 기본값 그대로 승인해도 됩니다.
    3. 쓰기 허락 창(6번 안팎)에서 **무엇을 · 어디에**를 읽고 `1 Yes`, `npm run build` 실행 창도 `1 Yes`. 끝나면 AI의 '확인할 것 3줄'을 읽습니다.
    4. 켜 둔 브라우저(`localhost:3000`)를 새로 고침 → 위 메뉴 **바이어** → 큰 숫자 확인 → 등급 칩 **C** → 목록의 B048 → 상세. 주소창에 직접 `localhost:3000/buyers/B999`도 쳐 봅니다.
    5. **휴대폰 폭** — ++f12++ → ++ctrl+shift+m++(기기 툴바) → 너비 `390`. 표가 카드로 바뀌고 옆으로 밀리지 않는지 봅니다. Mac은 ++cmd+option+i++ → ++cmd+shift+m++.

**이 단계의 목적** 대표님이 휴대폰으로 볼 바이어 목록 쪽과, 바이어마다 주소가 따로 있는 상세 쪽을 만든다.

!!! prompt "프롬프트 d2 — 목록 · 상세 쪽 · Plan 모드"

    --8<-- "labs/day4/prompts_d.md:d2"

!!! ok "확인할 것"

    - [ ] `/buyers` 큰 숫자 — 위험 바이어 **17곳** · C등급 채권 **$1,047,782**(전체의 **24.4%**) · 전체 채권 **$4,290,904**(150곳) · 연체 **$560,191**(26곳) · 등급 칩 **S 126 · A 4 · B 3 · C 17**
    - [ ] 위험 상위 10 = **B048 · B134 · B118 · B031 · B047 · B062 · B066 · B104 · B059 · B119** · 칩 **C**를 누르면 주소가 `/buyers?grade=C`로 바뀌고 목록이 **17곳**
    - [ ] `/buyers/B048` — 플랜트 시공(EPC) · 외상(O/A) · 30일 · $24,530 · $24,530 · 100.0% · 90일 · 30.8일 · 77.0% · C, 신호 3개 아래 '이 신호들은 확인해 볼 이유이지, 연체의 원인이라는 뜻은 아닙니다.' · `/buyers/B999` → '바이어를 찾을 수 없습니다'
    - [ ] `npm run build` 통과 — route 표에 `ƒ /buyers` · `ƒ /buyers/[id]` · 390px에서 가로 스크롤 없음

!!! ai "AI가 하는 일"

    안내서 「2」 · 「3」 · 「4」와 `guide/design_rules.md`를 읽고 계획을 먼저 보여 줍니다(Plan 모드라 아무것도 고치지 않습니다 · 1–2분). 승인하면 파일 5개를 쓰고 메뉴 한 줄을 고친 뒤(쓰기 허락 창 6번 안팎 · 3–6분) `npm run build`를 돌립니다(실행 허락 창 · 1–3분). 켜 둔 개발 서버가 바뀐 파일을 바로 읽으니 브라우저는 새로 고침만 하면 됩니다.

??? ok "참고 실행 값 — 내 화면과 대조"

    같은 데이터 · 같은 규칙이면 누가 만들어도 같은 숫자입니다.

    **위험 상위 10**(`pd30d` 큰 순 · 모두 C등급)

    | 순위 | 바이어 | 나라 | 위험 점수 | 채권 | 연체 | 첫 신호 |
    |---|---|---|---|---|---|---|
    | 1 | B048 Changzhou Wenant Engineering Co., Ltd. | 중국 | 77.0% | $24,530 | $24,530 | 최근 1년 분쟁 비율 50% |
    | 2 | B134 Camolin Instrumentación S.A. de C.V. | 멕시코 | 70.9% | $93,460 | $59,200 | 연체 금액 $59,200 |
    | 3 | B118 Tevura Automation Inc. | 미국 | 70.3% | $20,060 | $20,060 | 지급 지연이 늘어나는 중(+30일) |
    | 4 | B031 Kalaro Industrial S.A. de C.V. | 멕시코 | 69.3% | $70,120 | $19,200 | 지급 지연이 늘어나는 중(+29일) |
    | 5 | B047 Corost Comercializadora S.A. de C.V. | 멕시코 | 67.4% | $54,540 | $27,300 | 연체 금액 $27,300 |
    | 6 | B062 Galeth Instruments LLC | 미국 | 55.5% | $35,660 | $18,310 | 연체 금액 $18,310 |
    | 7 | B066 Marano Home & Lab Stores FZE | 아랍에미리트 | 54.2% | $80,550 | $10,610 | 최근 30일 부정적인 뉴스가 많음 |
    | 8 | B104 Sarant Ingeniería S.A. de C.V. | 멕시코 | 43.7% | $10,190 | $10,190 | 연체 금액 $10,190 |
    | 9 | B059 PT Sarida Sarana Industri | 인도네시아 | 41.4% | $40,560 | $4,980 | 지급 지연이 늘어나는 중(+36일) |
    | 10 | B119 Galost Automation Ltd. | 인도 | 38.3% | $48,780 | $21,910 | 연체 금액 $21,910 |

    **지역별 채권**(큰 순) — 합 $4,290,904

    | 지역 | 곳 수 | 채권 | 그중 C등급 | C 몫 |
    |---|---|---|---|---|
    | 동남아·남아 | 38 | $1,319,352 | $89,340 | 6.8% |
    | 동아시아 | 29 | $971,884 | $137,602 | 14.2% |
    | 북미·중남미 | 28 | $733,666 | $471,650 | **64.3%** |
    | 서유럽 | 23 | $543,729 | $14,580 | 2.7% |
    | 중동·아프리카 | 19 | $543,680 | $292,050 | 53.7% |
    | 중동부유럽 | 13 | $178,593 | $42,560 | 23.8% |

    **B048의 신호 3개** — 최근 1년 분쟁 비율 50% · 가장 오래된 미결이 90일째 · 31일 넘은 채권이 100%. 등급별 채권은 S $2,630,341 · A $144,250 · B $468,531 · C $1,047,782. 목록(전체)의 순서도 위험 점수 순이라 맨 위 다섯은 위 표와 같고, `?grade=C`의 17곳은 상위 10 다음에 B008 · B073 · B041 · B140 · B075 · B087 · B085가 이어집니다.

??? fix "계획에 `lib/metrics.ts`가 없어요 · 쪽 안에서 바로 계산하겠대요"

    승인 창에서 `3 No, keep planning`을 고르고 "안내서 「2」대로 계산은 lib/metrics.ts의 순수 함수로, 쪽은 부르기만 하게 계획을 다시"라고 보냅니다. 계산을 한곳에 모아야 내일 DB로 바꿀 때 쪽을 고치지 않습니다.

??? fix "위험 상위 10의 1위가 B048이 아니에요"

    채권(금액) 순으로 정렬한 것입니다(그러면 B005가 1위). "위험 상위 10은 pd30d 큰 순, 같으면 id 순으로"라고 보냅니다.

??? fix "등급 칩이 S 126 · A 4 · B 3 · C 17이 아니에요"

    위험 점수로 등급을 다시 매긴 것입니다. "등급은 grade 칸 그대로 — 다시 매기지 마"라고 보냅니다.

??? fix "`Type error: … params …` · `searchParams …`가 나요"

    Next.js 16에서 주소의 값(`params` · `searchParams`)은 **Promise**라 `await`로 꺼내야 합니다. 오류 끝 10줄을 붙여 아래 **d-fix**를 보내 원인부터 받고, 맞으면 "고쳐"라고 보냅니다.

??? fix "등급 칩을 눌러도 목록이 그대로예요"

    "칩은 Link로 주소를 /buyers?grade=C처럼 바꾸고, 쪽은 await searchParams로 읽어 전체 목록만 거르는지 확인해"라고 보냅니다. 큰 숫자 · 상위 10 · 지역별은 일부러 바뀌지 않습니다(언제나 150곳 기준).

??? fix "`31일 넘긴 채권 비중`이 1.0% · 10000.0%처럼 나와요"

    비율을 두 번 바꾼 것입니다 — 데이터의 값은 0–1(1.0 = 100%)이고 `pct()`가 100을 곱합니다. 아래 **d-check**에 그 칸 이름 · 화면 값 · 기대값(`100.0%`)을 넣어 보냅니다.

??? fix "휴대폰 폭에서 옆으로 밀려요"

    "390px에서 화면보다 넓은 요소를 찾아 design_rules 5절대로 고쳐 — 숫자는 그대로"라고 보냅니다. 큰 숫자 4개가 휴대폰에서도 4열이거나, `DataTable` 대신 맨 표를 쓴 경우가 흔합니다.

??? fix "숫자가 위 값과 달라요"

    바로 고치게 하지 말고 어디서 갈렸는지부터 묻습니다. `{항목}` · `{화면 값}` · `{기대값}`을 바꿔 보냅니다.

    --8<-- "labs/day4/prompts_d.md:d-check"

<p class="tf-check"><time>15:45</time> 손 점검 — localhost의 /buyers에서 C 17곳 · /buyers/B048 열림 · build 통과</p>

**획득:** 바이어마다 주소 150개

### D-1 · 03 보스전 · 대표님 휴대폰에 B048 주소 보내기 — 세이브 포인트 · push (15:45–15:50) { #d1-3 .step data-tool="Claude Code · Git · Vercel · 휴대폰" }

**왜** 내 PC의 `localhost`는 나만 봅니다. 커밋(세이브 포인트)을 GitHub에 push하면 Vercel이 그것을 받아 새로 빌드하고 운영 주소를 바꿉니다 — 대표님 손에 닿는 것은 그 주소입니다. **d3** → 커밋 · push → Vercel Ready → 휴대폰

!!! me "내가 할 일"

    1. 모드 **Manual** → **d3**. AI가 `npm run build` · `npm run doctor:secrets`를 돌린 뒤 **파일 목록 · 메시지 두 줄 · 브랜치 `main`**을 보여 주고 기다립니다 — 목록에 `.env` · `.next` · `node_modules` · `lib/generated`가 없는지 보고 "좋아". 커밋 · push 허락 창도 읽고 `1 Yes`.

        ```text
        4일차: 바이어 목록 · 상세 쪽 추가

        왜: 대표님이 150곳을 주소 하나로 휴대폰에서 보게
        ```

    2. Vercel → 내 프로젝트 → **Deployments** — 맨 위 줄이 Building에서 **Ready**로(1–3분).
    3. **보스전** — 운영 주소 뒤에 `/buyers/B048`을 붙인 주소를 휴대폰으로 보냅니다(카카오톡 '나에게 보내기' 등). 휴대폰에서 열어 12칸과 신호 3개를 보고, 같은 주소를 PC의 시크릿 창(++ctrl+shift+n++)에서도 한 번 엽니다.

**이 단계의 목적** 만든 쪽을 내 운영 주소에 올려, 대표님 휴대폰에서 B048의 주소가 열리게 한다.

!!! prompt "프롬프트 d3 — 검사 · 커밋 · push"

    --8<-- "labs/day4/prompts_d.md:d3"

!!! ok "확인할 것 — 보스전 클리어 조건"

    - [ ] 휴대폰에서 `https://tradefin-web-t2-07.vercel.app/buyers/B048` — 내 PC와 같은 12칸 · 신호 3개 · 가로 스크롤 없음
    - [ ] 운영 주소의 `/buyers` 큰 숫자가 내 PC와 같다 — **17곳 · $1,047,782 · $4,290,904 · $560,191**
    - [ ] 첫 쪽 배지 `production · ○○○○○○○ · icn1`의 7글자 = AI가 알려 준 커밋 번호 · 시크릿 창에서도 로그인 없이 열린다

!!! ai "AI가 하는 일"

    안내서 「5」대로 build와 비밀 검사를 돌리고(실행 허락 창 2번 · 1–2분) 파일 목록 · 메시지를 보여 준 뒤 기다립니다. 승인하면 커밋 · push하고(허락 창 2–3번) 커밋 7글자를 알려 줍니다. 그다음은 Vercel이 저절로 합니다 — push된 `main`을 받아 빌드하고 운영 주소를 바꿉니다.

??? fix "Deployments가 Error예요"

    운영 주소는 지난번 잘 된 판(첫 쪽)을 그대로 보여 줍니다 — 대표님 화면은 깨지지 않았습니다. 그 배포를 눌러 **Build Logs**에서 빨간 줄과 그 위 10줄을 복사해 아래 **d-fix**에 붙여 보냅니다. 내 PC에서는 되는데 Vercel에서만 안 되면 **파일 이름 대소문자**가 흔한 원인입니다(Windows는 `KpiCard`와 `kpicard`를 같게 봅니다).

    --8<-- "labs/day4/prompts_d.md:d-fix"

??? fix "push가 거부되거나 로그인을 물어요"

    VS Code 왼쪽 아래 계정 아이콘에서 GitHub에 로그인합니다. `GH007 … private email`이면 [3일차 실습 A의 커밋 막히면](../day3/lab-a.md#a1-5)대로 noreply 주소로 바꾸고 커밋을 다시 만듭니다.

??? fix "파일 목록에 `.env`나 `.next`가 보여요"

    `No`를 누르고 "안내서 5절대로 그 파일은 빼고 목록을 다시"라고 보냅니다. `.gitignore`가 막아 주지만, 허락 창을 읽는 것은 사람입니다.

??? fix "휴대폰에 옛 화면이 보여요"

    Deployments 맨 위가 Ready인지 보고 휴대폰에서 새로 고침합니다. 첫 쪽 배지의 7글자가 방금 커밋과 같으면 새 판입니다.

<p class="tf-check"><time>15:50</time> 보스전 — 휴대폰에서 /buyers/B048. 10분 쉽니다</p>

**획득:** 세이브 포인트 1 · 보스 처치 — 대표님 손에 B048의 주소

## 2부 · 자유 퀘스트 — 내 웹앱을 내 마음대로 {#d2}

<div class="tf-phase" markdown>

<span class="tf-eyebrow">2부 · 실습 D-2 · 16:00–16:50 · Claude Code · 브라우저 · Vercel</span>

하고 싶은 것 한 줄 — 방향은 AI가 셋 제안, 고르는 것은 나

**목표** 1부의 웹앱을 내 방향으로 키워 운영 주소로 낸다 — 1부의 숫자는 그대로, 모양과 기능은 사람마다 다르게

1. 자유 퀘스트 — 열린 프롬프트 · 씨앗 · 아무거나
2. 세이브 포인트 — 390px · 비밀 검사 · push
3. 마지막 관문 — `[발표]`에 운영 주소

**결과물** 나만의 기능 · 커밋 2개 이상 · 운영 주소

</div>

!!! quote "디지털 TF 단톡방 — 오늘 15:58"

    **대표님** B048 주소 잘 받았습니다. 여기서부터는 최 대리 마음대로 해 보세요. 숫자만 그대로면 됩니다.

    **IT팀 오 주임** 키(API 키) 없이 되는 것부터 하시죠. 키는 잃어버리는 순간 남의 것이 됩니다.

    **정 영양사님** (지나가다가) 말로 찾는 게 되면 식당 키오스크에도 해 주세요. "오늘 몇 인분?" 하면 알려 주게.

    **재무팀 한 과장** 게임이요? …점수 계산은 정확하게 나오죠?

**노는 법** — 16:00에 강사가 '와!' 씨앗 두세 개를 1분 보여 줍니다(같은 숫자 · 다른 모습).

1. 아래 씨앗에서 하나를 고르거나, 하고 싶은 것을 **한 줄**로 씁니다. 몰라도 됩니다 — `몰라도 됨` 그대로 보내도 됩니다.
2. AI가 **'와!' 방향 3개**를 제안합니다 → 번호를 고르거나 고쳐서 답합니다("2번인데 더 게임처럼") → AI가 계획 3줄 → "좋아, 만들어".
3. 다 되면 AI의 '확인할 것 3줄'을 **내 브라우저에서 직접** 해 봅니다. 한 바퀴 15–20분 — 남으면 한 바퀴 더(작게).
4. 아이디어가 막히면 **아무거나**(d-wow) — 지금 결과로 할 수 있는 가장 놀라운 것 3가지를 AI가 먼저 꺼냅니다.

### D-2 · 01 자유 퀘스트 · 내 웹앱을 내 마음대로 (16:00–16:35) { #d2-1 .step data-tool="Claude Code · 브라우저" }

**왜** 1부는 모두 같은 결과였지만 2부는 내 방향입니다. 자세한 주문서 대신 하고 싶은 것 한 줄 — AI가 먼저 제안하고 사람이 고릅니다. 웹앱은 브라우저 위에서 돌아서, 키 하나 없이도 **듣고 · 말하고 · 알리고 · 설치되는** 기능을 쓸 수 있습니다. "이런 것까지 되네?"를 찾는 시간입니다. 한 줄 → **d-free** → '와!' 3개 → 고르기 → 계획 3줄 → 만들기

!!! me "내가 할 일"

    1. 모드 **Manual**. 아래 **d-free**의 `{하고 싶은 것 한 줄 · 몰라도 됨}` 자리만 바꿔 보냅니다(중괄호도 지웁니다) — 씨앗을 그대로 옮겨도, `몰라도 됨`이라고 써도 됩니다.
    2. 제안 3개를 읽고 하나를 고릅니다 — 마음에 안 들면 "더 엉뚱하게" · "대표님이 '와' 할 만하게" · "게임처럼"으로 다시.
    3. 계획 3줄을 읽고 "좋아, 만들어". 패키지 설치 · API 키 · 바깥으로 보내기를 물으면 키 없는 길이 있는지 먼저 묻습니다.
    4. 쓰기 · 실행 허락 창을 읽고 `1 Yes` → 끝나면 '확인할 것 3줄'을 브라우저(`localhost`)에서 직접. 마이크 · 소리는 PC에서 해 보고, 휴대폰은 push 뒤 운영 주소로.

**이 단계의 목적** 내 웹앱을 내가 고른 방향으로 키운다 — 1부의 쪽과 숫자는 그대로.

!!! prompt "프롬프트 d-free — 자유 퀘스트"

    --8<-- "labs/day4/prompts_d.md:d-free"

**씨앗** — 한 줄씩입니다. 그대로 써도, 섞어도, 바꿔도 됩니다.

| 씨앗 | 이런 것 | 종류 |
|---|---|---|
| 말로 바이어 찾기 | 마이크 단추를 누르고 "B048" · "멕시코"라고 말하면 그 바이어로 — 브라우저 음성 인식, 키 없음 | 와! · 듣기 |
| 읽어 주는 상세 쪽 | '읽어 주기' 단추를 누르면 브라우저가 B048의 상태를 한국어로 또박또박 — 키 없음 | 와! · 말하기 |
| 홈 화면 앱 | 대표님 휴대폰 홈 화면에 아이콘으로 설치 — 주소창 없이 앱처럼 열린다(PWA) | 와! · 설치 |
| 등급 맞히기 퀴즈 | 신호만 보고 S · A · B · C를 맞히는 10문제 — 점수와 '오늘의 칭호' | 게임 |
| 검색 · 정렬 | 이름 몇 글자로 찾기 · 점수 순 / 돈 순 단추 — 주소에 남아 그대로 보낼 수 있게 | 실속 |
| 지역 쪽 | 돈이 어디에 물려 있나 — 지역 6곳 타일과 지역마다 주소 | 실속 |
| 내 3일차 디자인 | 금요일의 `design.md`(과정 저장소 `workbench/day3/outputs/`에서 이 저장소로 복사)로 색 · 글자 · 간격만 — 숫자는 그대로 | 내 취향 |

**다음 목적** 아이디어가 없거나 더 놀라고 싶을 때 — 지금 결과로 할 수 있는 가장 놀라운 것을 AI가 먼저 제안한다.

!!! prompt "프롬프트 d-wow — 아무거나"

    --8<-- "labs/day4/prompts_d.md:d-wow"

!!! ok "확인할 것"

    - [ ] 고른 방향이 내 화면에서 동작한다 — AI의 '확인할 것 3줄'을 내 손으로 해 봤다
    - [ ] 1부 그대로 — `/buyers` C **17곳** · **$1,047,782**, `/buyers/B048` 12칸 그대로
    - [ ] `npm run build` 통과 · 키 · 비밀 · 실명 없음 · 새 패키지는 내가 허락한 것만

!!! ai "AI가 하는 일"

    안내서 「6」대로 지금 쪽 · 데이터 · 부품을 읽고 '와!' 방향 3개를 먼저 제안합니다(파일을 고치지 않음 · 1–2분). 사람이 고르면 계획 3줄을 보이고, 승인 뒤 만들어 `npm run build`까지 통과시킵니다(허락 창 3–6번 · 5–15분). 패키지 · 키 · 바깥 발송이 필요하면 만들기 전에 묻습니다.

??? fix "마이크 단추를 눌러도 아무 일이 없어요"

    음성 인식은 Chrome · Edge · 휴대폰 Safari에서 됩니다(Firefox는 안 됩니다). 주소창 왼쪽 자물쇠 → **마이크 허용**, 주소가 `localhost`나 `https://`(운영 주소)인지 봅니다. PC에 마이크가 없으면 push한 뒤 휴대폰으로 해 봅니다.

??? fix "읽어 주기가 영어 발음 · 기계음이에요"

    그 PC에 한국어 목소리가 없는 것입니다. "목소리 목록에서 ko-KR을 고르고, 없으면 그렇다고 화면에 한 줄"이라고 보냅니다. 휴대폰에서는 대개 한국어 목소리가 있습니다.

??? fix "홈 화면에 설치하는 메뉴가 안 보여요"

    운영 주소(`https://`)에서 해 봅니다(내 PC의 `localhost`는 PC Chrome만 됩니다). Android Chrome은 ⋮ → **홈 화면에 추가**(또는 **앱 설치**), iPhone은 Safari의 공유 단추 → **홈 화면에 추가**, PC Chrome은 주소창 오른쪽의 설치 아이콘.

??? fix "AI가 패키지를 설치하거나 API 키를 달래요"

    안내서 6절대로 먼저 묻는 것입니다. "키 없이, 새 패키지 없이 되는 길로 다시 제안해"라고 보냅니다. 꼭 필요한 패키지라면 강사와 상의합니다 — 잠금 파일이 바뀌면 내일 실습에도 영향이 갑니다.

??? fix "1부 숫자가 바뀌었어요 · 1부 쪽이 깨졌어요"

    "방금 바꾼 것 중 1부 쪽을 건드린 곳을 되돌려 — 안내서 6절 5번"이라고 보냅니다. 급하면 소스 제어(++ctrl+shift+g++)에서 그 파일 → **Discard Changes** — 1부를 커밋해 두었으니 세이브 포인트로 돌아갑니다.

??? fix "제안이 너무 평범해요"

    **d-wow**를 보내거나 "셋 다 키 없이 되는 브라우저 기능이나 게임으로, 대표님이 '와' 할 만하게 다시"라고 보냅니다.

<p class="tf-check"><time>16:35</time> 손 점검 — 내 자유 퀘스트가 localhost에서 동작 · 1부 숫자 그대로</p>

**획득:** 나만의 기능 — "이런 것까지 되네"

### D-2 · 02 세이브 포인트 · 390px · 비밀 검사 · push (16:35–16:45) { #d2-2 .step data-tool="브라우저 · 터미널 · Claude Code" }

**왜** 운영 주소는 누구나 엽니다. 올리기 전에 두 가지만 봅니다 — 휴대폰에서 깨지지 않는지(390px), 비밀이 섞이지 않았는지(`doctor:secrets`). 390px → `npm run doctor:secrets` → **d3** → Ready

!!! me "내가 할 일"

    1. **390px** — ++f12++ → ++ctrl+shift+m++ → 너비 `390`. `/buyers` · `/buyers/B048` · 내가 더한 쪽에서 옆으로 밀리는 곳이 없는지 봅니다.
    2. 새 터미널(오른쪽 위 **+** — 개발 서버 터미널은 그대로)에서 비밀 검사를 합니다.

        ```text
        npm run doctor:secrets
        ```

    3. **d3**를 한 번 더 보냅니다 — 이번에는 AI가 2부 메시지(`4일차: 자유 퀘스트 — …`)를 씁니다. 파일 목록 · 메시지를 읽고 승인합니다.
    4. Deployments → **Ready** → 운영 주소에서 내 자유 퀘스트를 휴대폰으로 열어 봅니다.

**이 단계의 목적** 2부 결과를 세이브 포인트로 남기고 운영 주소를 새 판으로 바꾼다 — 비밀 없이, 휴대폰에서 깨지지 않게.

!!! prompt "프롬프트 d3 — 검사 · 커밋 · push(2부)"

    --8<-- "labs/day4/prompts_d.md:d3"

!!! ok "확인할 것"

    - [ ] 390px에서 가로 스크롤 없음 — `/buyers` · `/buyers/B048` · 내가 더한 쪽
    - [ ] `npm run doctor:secrets` 모두 PASS
    - [ ] 운영 주소에 2부 기능이 보이고, 첫 쪽 배지의 7글자 = 마지막 커밋

??? fix "`doctor:secrets`에 FAIL이 있어요"

    FAIL 줄이 무엇을 · 어디서 찾았는지 알려 줍니다(키 모양의 글자 · 비밀번호가 든 주소 · 실제 메일 등). 그 줄을 붙여 "이 줄을 안내서 0절대로 고칠 방법만 먼저"라고 보내고, 고친 뒤 다시 검사합니다. FAIL이 남아 있으면 push하지 않습니다.

??? fix "16:45인데 2부가 build를 통과하지 못해요"

    2부는 push하지 않습니다 — 운영 주소에는 이미 1부 판이 떠 있습니다. 그 주소로 `[발표]`하고, 2부는 발표의 '안 된 것'으로 말합니다.

<p class="tf-check"><time>16:45</time> 세이브 포인트 2 — doctor:secrets PASS · Ready</p>

**획득:** 세이브 포인트 2

### D-2 · 03 마지막 관문 · `[발표]`에 운영 주소 (16:45–16:50) { #d2-3 .step data-tool="오픈채팅 · 휴대폰" }

**왜** 오늘의 결과물은 파일이 아니라 **주소 하나**입니다. 누가 어디서 열어도 같은 화면이어야 합니다. 시크릿 창 → `[발표]` → 4문장

!!! me "내가 할 일"

    1. 운영 주소의 `/buyers`를 시크릿 창(또는 휴대폰)에서 한 번 엽니다.
    2. <span data-tf-link="open_chat">오픈채팅</span>에 이 양식으로 올립니다.

        ```text
        [발표] 조-번호 / 별명 / D / 한 줄 / 운영 주소
        예) [발표] T2-07 / 바다 / D / 말하면 바이어를 찾아 주는 웹앱 / https://tradefin-web-t2-07.vercel.app/buyers
        ```

    3. 발표 4문장을 **내 말로** 씁니다 — 불편(상황) → 시연(1부 + 내 자유 퀘스트) → 안 된 것 → 이렇게 고쳤다 / 내 업무라면.

        ```text
        1. 불편: 대표님은 회의 중에 바이어 한 곳을 바로 보여 줄 주소가 필요했다.
        2. 시연: (휴대폰으로 운영 주소를 열고) /buyers/B048 — 그리고 2부에 ○○를 더했다.
        3. 안 된 것: ○○에서 막혔다(예: Vercel 빌드가 파일 이름 대소문자로 실패).
        4. 이렇게 고쳤다 / 내 업무라면: ○○ — 내 업무의 ○○ 표도 주소 하나로 만들겠다.
        ```

!!! ok "확인할 것"

    - [ ] 시크릿 창에서 로그인 없이 열린다 · 주소가 운영 주소(Domains의 짧은 주소)다
    - [ ] 오픈채팅에 `[발표]` 양식으로 올렸고, 발표 4문장이 있다

**8교시(17:00) 쇼케이스** — 3일차와 같습니다. 한 사람 2분(1:45 노랑 · 2:00 종), 강사 노트북에서 내 운영 주소를 열고 4문장으로 말합니다. 주소가 안 열리면 그 블록 끝으로 미룹니다. 다섯 명이 끝날 때마다 1분은 서로의 주소를 휴대폰으로 눌러 보는 시간입니다. 17:40 '투표 시작' 뒤 마음에 드는 발표의 메시지 2개에 공감을 누릅니다(내 팀 제외) — 17:46 TOP 3.

<p class="tf-check"><time>16:50</time> [발표] · 4문장 — 17:00 쇼케이스</p>

**획득:** 업적 '첫 웹앱 출시'

!!! late "늦었다면"

    **최소 경로는 D-0 · 02 · 03(운영 주소) → d2 → d3** 입니다. d1과 2부는 건너뛰어도 됩니다. 15:15에 운영 주소가 없으면 다른 것보다 D-0 · 02 · 03부터 — 주소가 오늘의 첫 결과물입니다. 15:25에 `npm ci`가 안 끝났으면 Codespaces(D-0 · 04). 15:45에 build가 안 되면 **d-fix**로 원인만 받고 손을 듭니다 — 고친 뒤 d3. 16:45에 2부가 build를 통과하지 않으면 push하지 않고 1부 판으로 `[발표]`합니다. 오늘 1부를 못 끝내도 내일 아침에 합류하는 길이 있습니다(5일차 아침에 안내).

## 다 했으면 — 한 바퀴 더 {#more}

하나만 골라도 좋습니다. 회사 실데이터는 쓰지 않습니다 — 내 업무로 넓힐 때는 **열 이름만, 데이터 없이**.

<div class="grid cards tf-ext" markdown>

-   <span class="tf-level">기본 · 10분 · Claude Code</span>

    **씨앗 하나 더**

    고르지 않은 씨앗을 한 바퀴 더 — 작게. '와!' 씨앗을 했다면 이번엔 실속 씨앗, 실속을 했다면 이번엔 '와!'. 끝나면 d3로 세이브 포인트.

-   <span class="tf-level">기본 · 5분 · 휴대폰</span>

    **짝의 주소로 놀러 가기**

    옆 사람의 운영 주소를 휴대폰으로 열어 '와!' 하나 · 아쉬운 점 하나를 말해 줍니다. 그 사람의 `/buyers/B048`과 내 것의 숫자가 같은지도 봅니다 — 같은 데이터 · 같은 규칙이면 같아야 합니다.

-   <span class="tf-level">도전 · 10분 · Claude 또는 Claude Code</span>

    **내 업무 웹앱 상상**

    내 업무에서 '주소 하나로 보고 싶은 표'를 **열 이름만** 적고 "이걸 목록 쪽 · 상세 쪽으로 만든다면 계획 3줄"을 받습니다 — 6일차 해커톤의 씨앗이 됩니다.

</div>

## 채팅 경로 — Claude Code를 못 쓸 때 {#chat-path}

Claude Code 계정이 없거나(무료 플랜은 쓸 수 없습니다) 확장이 로그인되지 않으면 **claude.ai + GitHub 웹**으로 같은 문장을 보냅니다. 데이터는 합성이라 올려도 됩니다. 이 길에서는 내 PC 설치(`npm ci`)가 필요 없고, 빌드는 Vercel이 합니다. 진행 표시는 같은 단계 — 끝낸 단계의 '이 단계 완료'를 눌러 둡니다.

1. **D-0 · 02 · 03** — 그대로 합니다(브라우저만으로 됩니다). 운영 주소까지 받습니다.
2. **파일 받기** — 내 저장소 → **Code → Download ZIP** → 압축을 풉니다.
3. **D-1 · 01 · 02** — claude.ai 새 대화(파일 첨부 · 코드 실행이 켜져 있어야 합니다)에 `CLAUDE.md` · `guide/day4_lab_d.md` · `guide/design_rules.md` · `data/buyers.json` · `lib/format.ts` · `components/`의 8개 · `app/layout.tsx` · `app/page.tsx`를 첨부하고, 아래 **채팅 시작** 문장을 먼저 보낸 뒤 d1 → d2를 그대로 보냅니다. 계획을 보여 주면 읽고 "좋아, 진행해".
4. **올리기** — 답의 파일마다 GitHub 내 저장소 → **Add file → Create new file** → 이름 칸에 경로째(`lib/buyers.ts` · `app/buyers/[id]/page.tsx` — `/`를 치면 폴더가 생깁니다) → 내용 붙여 넣기 → **Commit changes…** → 메시지 → **Commit directly to the `main` branch**. 이미 있는 파일(`components/SiteNav.tsx`)은 그 파일을 열고 연필(Edit) → 통째로 바꿔 붙여 넣기. `lib` → 쪽 → 메뉴 순서로 올리면 중간 빌드도 덜 깨집니다.
5. **D-1 · 03** — 커밋마다 Vercel이 새로 빌드합니다. 마지막 파일까지 올린 뒤 Deployments 맨 위가 Ready면 보스전(휴대폰으로 `/buyers/B048`). Error면 Build Logs의 빨간 줄과 그 위 10줄을 대화에 붙이고 **d-fix**.
6. **2부** — 같은 대화에서 d-free · d-wow → 답의 파일 → GitHub 웹. 대화가 길어져 앞 파일을 잊으면 새 대화에 같은 파일과 새로 만든 파일을 다시 올리고 d-chat부터.

??? prompt "채팅 시작 — claude.ai 첫 메시지"

    --8<-- "labs/day4/prompts_d.md:d-chat"

ChatGPT만 쓸 수 있다면 같은 파일을 올리고 같은 문장을 보냅니다 — 받은 파일을 GitHub 웹으로 올리는 길은 같습니다.

## 막힐 때 {#troubleshooting}

단계 안의 '막히면'에 없는 것까지 모았습니다. 오류가 나면 먼저 `npm run doctor`, 그다음 **d-fix**(원인부터 · 아직 고치지 않기)입니다.

| 증상 | 이렇게 해 보세요 |
|---|---|
| PowerShell에 `npm.ps1 … 이 시스템에서 스크립트를 실행할 수 없으므로` | 이 저장소의 터미널은 명령 프롬프트(cmd)로 열립니다 — 터미널 오른쪽 위 **∨ → Command Prompt**. 그래도 PowerShell이면 `npm.cmd ci`처럼 `npm.cmd`로, 또는 한 번만 `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`(`Y`) |
| `npm ci`가 10분 넘게 그대로 · `ETIMEDOUT` | 화면은 이미 Vercel에 떠 있으니 기다려도 됩니다. 15:25에도 안 끝나면 Codespaces([D-0 · 04](#d0-4)). 강사 USB가 돌면 `npm ci --cache <USB의 npm-cache 폴더> --prefer-offline` |
| `binaries.prisma.sh`에 연결하지 못함(설치 끝 무렵) | 회사망 · 강의장 망이 막은 것 — 휴대폰 핫스팟으로 `npm ci`를 다시, 안 되면 Codespaces |
| 내 PC에선 되는데 Vercel 빌드만 실패 · `Module not found` | **파일 이름 대소문자** — Windows는 `KpiCard`와 `kpicard`를 같게 보지만 Vercel(Linux)은 다르게 봅니다. 오류 줄을 붙여 **d-fix** |
| 주소를 열었더니 Vercel 로그인 화면 | 배포별 긴 주소(`…-abc123xyz-….vercel.app`)를 연 것 — 프로젝트의 **Domains** 주소를 씁니다 |
| Vercel의 Import 목록에 내 저장소가 없다 | **Adjust GitHub App Permissions →** → Only select repositories에 `tradefin-web-T2-07` 추가 → Save → Vercel에서 새로 고침 |
| `'use client'` 파일이 데이터를 import한다 · `useState … only works in a Client Component` | 데이터는 서버 쪽(`page.tsx`)에서 읽고, 누르기가 필요한 작은 부품만 `'use client'`로 — 값은 props로 넘깁니다. **d-fix**로 원인부터 |
| `Port 3000 is in use` · 3001로 열렸다 | 터미널의 `Local:` 줄 주소를 엽니다. `npm run dev`를 두 번 켰다면 하나를 ++ctrl+c++로 |
| AI가 `npm run dev`를 또 켜려다 'Another next dev server is already running' | 정상입니다 — 내 터미널에 이미 켜져 있습니다. 브라우저를 새로 고침하면 됩니다 |
| 사용 한도에 걸렸다 | 입력창에 `/model` → **Sonnet**으로 바꿔 봅니다. 풀리는 시각까지 짝과 한 화면으로, 또는 [채팅 경로](#chat-path) → [FAQ](../faq.md#q-usage-limit) |
| 허락 창이 계속 뜬다 | 정상입니다. 무엇을 · 어디에를 읽고 `1 Yes`. `.env`를 여는 창 · `git push --force` · `git reset --hard`는 `No` |
| AI가 시키지 않은 2부까지 만들었다 | "안내서 0절대로 프롬프트가 가리킨 절만 — 방금 더한 ○○는 되돌려"라고 보냅니다 |
| 과정 저장소 창에서 프롬프트를 보냈다 | 창 제목을 봅니다 — 실습 D는 `tradefin-web-T2-07` 창. 과정 저장소에 생긴 파일은 지우지 말고 손을 듭니다 |
| 휴대폰에서 옛 화면이 보인다 | Deployments 맨 위가 Ready인지 보고 새로 고침. 첫 쪽 배지의 7글자가 마지막 커밋과 같은지 봅니다 |
