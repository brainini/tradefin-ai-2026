---
title: 웹 작업대(4–6일차)
---

<div class="tf-hero" markdown>
<span class="tf-eyebrow">시작하기 · 4–6일차 수업판 · 웹 실습의 작업실</span>

# 웹 작업대 — 4–6일차

AI와 함께 만들 수 있는 것은 많습니다 — 웹앱 · 모바일 앱 · 사내 시스템 · 자동화 프로그램 · 챗봇 · 게임까지. 그중 4–6일차는 **가장 범용인 웹앱**을 만듭니다. 주소 하나면 누구의 휴대폰에서도 열리고, 설치가 없고, 고치면 바로 모두에게 바뀌기 때문입니다. 이 쪽은 그 웹앱을 만드는 작업실 — **웹 스타터 저장소**의 지도 · 명령 · 점검 도구 · Vercel · Supabase · 막힐 때를 한곳에 모았습니다.

<div class="tf-meta" markdown>
<span class="tf-chip">Next.js 16 · React 19 · TypeScript · Tailwind CSS</span>
<span class="tf-chip">Prisma 7 · Supabase(5일차)</span>
<span class="tf-chip">GitHub → Vercel 배포</span>
<span class="tf-chip">막히면 Codespaces</span>
</div>

<div class="tf-buttons" markdown>
[설치 · 가입](setup.md#web-setup){ .md-button .md-button--primary }
[4일차 수업판](day4/class.md){ .md-button }
[5일차 수업판](day5/class.md){ .md-button }
[6일차 해커톤](day6/hack.md){ .md-button }
[막힐 때](#stuck){ .md-button }
</div>
</div>

!!! tip "왜 웹앱부터?"

    **주소 하나**로 나눠 주고 · **설치 없이** 열리고 · 휴대폰 · 태블릿 · PC **모든 기기**에서 같고 · push하면 **바로 모두에게** 바뀌고 · 홈 화면에 **앱처럼 설치**(PWA)도 되고 · AI 코딩 도구가 **가장 잘 만드는 분야**입니다. iPhone은 iOS 26부터 홈 화면에 추가한 사이트가 기본으로 '웹 앱'으로 열리고, 말로 앱을 만드는 빌더들의 기본 결과물도 웹앱(주소)입니다. 모바일 앱 · 사내 시스템 · 게임도 결국 같은 부품(화면 · 서버 · 데이터 · AI)으로 만들어지니, 웹앱 하나를 손으로 만들어 보면 나머지 모양이 읽힙니다.

## 저장소 둘, VS Code 창 둘 {#two-repos}

4일차부터는 저장소가 하나 더 생깁니다. 4일차 실습 C(메일함 아침 당번 로봇)까지는 원래 쓰던 **과정 저장소**, 4일차 실습 D부터는 웹 스타터로 만든 **웹 저장소**에서 일합니다.

| 저장소 | 폴더 예 | 언제 | 무엇 |
|---|---|---|---|
| 내 과정 저장소 `tradefin-my-T{조}-{번호}` | `C:\work\tradefin-my-T2-07` | 1–3일차 · **4일차 실습 C** | 파이썬(uv) — 메일함 아침 당번 로봇 |
| 내 웹 저장소 `tradefin-web-T{조}-{번호}` | `C:\work\tradefin-web-T2-07` | **4일차 실습 D · 5일차 실습 C · D** | Next.js 웹앱 — 바이어 목록 · 상세 → DB · 확인 기록 → 환율 타일 · 승인 대기열 |
| 내 해커톤 저장소 `hack-T{조}-{번호}` | `C:\work\hack-T2-07` | **6일차** | 같은 스타터로 하나 더 — 내 아이디어 앱 |

- VS Code 창 맨 위 제목 표시줄에 폴더 이름이 보입니다. 프롬프트를 보내기 전에 **지금 어느 창인지** 한 번 봅니다.
- 웹 저장소는 과정 저장소와 이력이 이어져 있지 않습니다. 웹 저장소의 고쳐진 안내서는 `get_day_files.py`가 아니라 [`npm run guide:update`](#update)로 받습니다.
- 저장소 이름 · 파일 · 커밋에는 실명 · 회사명을 쓰지 않습니다. 웹 저장소도 **공개(Public)**라서 가상 데이터만 둡니다.

## 시작 경로는 하나 — 주소부터 {#start}

4일차 실습 D의 첫 25분입니다. **내 주소(운영 주소)가 먼저** 생기고, 내 PC 설치는 그다음입니다 — `npm ci`가 느려도 첫 배포는 이미 Vercel의 클라우드에서 끝나 있습니다.

<div class="tf-timeline" markdown>

1. <time>GitHub</time> 웹 스타터 [`brainini/tradefin-web-starter`](https://github.com/brainini/tradefin-web-starter) → **Use this template → Create a new repository** · Owner는 내 계정 · 이름 `tradefin-web-T{조}-{번호}` · **Public** · 'Include all branches'는 끈 채로
2. <time>Vercel</time> **Add New → Project** → GitHub 앱 설치(**Only select repositories** → 방금 만든 저장소) → **Import** → 설정은 건드리지 않고 **Deploy** → 빌드가 끝나면 운영 주소 `tradefin-web-t2-07.vercel.app`
3. <time>VS Code</time> ++ctrl+shift+p++ → `Git: Clone` → 내 웹 저장소 → 폴더 `C:\work` → **Open** → **Yes, I trust the authors**
4. <time>터미널</time> `npm ci`(Wi-Fi에 따라 2–20분) → `npm run doctor` → `npm run dev` → 브라우저에서 http://localhost:3000

</div>

- README에 있을 수 있는 '한 번에 배포' 단추(Deploy with Vercel 같은 것)는 쓰지 않습니다. 내 저장소를 먼저 만들고 Vercel이 **그 저장소를 가져오게(Import)** 해야, push할 때마다 내 주소가 새로 배포됩니다.
- 첫 화면에 **'이 쪽이 보이면 배포 성공'**과 배포 배지가 보이면 됩니다. 배지는 Vercel에서 `production · 커밋 7자리 · icn1`, 내 PC에서 `내 PC · development`처럼 어디서 돌고 있는지를 보여 줍니다(스타터의 `/api/health`가 알려 줍니다).
- **4일차 15:25까지 `npm ci`가 끝나지 않으면 [Codespaces](#codespaces)로** 옮깁니다. 기다리는 동안에도 Vercel의 내 주소는 살아 있습니다.
- Node 24 설치 · Vercel · Supabase 가입은 [사전 준비 → 4–6일차 웹 실습 준비](setup.md#web-setup)에 있습니다.

## 스타터 지도 — 무엇이 어디에 {#map}

스타터는 **처음부터 돌아가는 웹앱**입니다. 첫 화면 · 부품 · 데이터 · 안내서 · 점검 도구가 들어 있어서, 1부는 '빈 화면에서 시작'이 아니라 '되는 것에서 시작'합니다.

| 폴더 · 파일 | 무엇 | 고쳐도 되나 |
|---|---|---|
| `app/` | **쪽(주소)** — 폴더가 곧 주소입니다. `page.tsx` 첫 화면 · `layout.tsx` 틀 · `not-found.tsx` · `api/health/route.ts`(배포 배지가 부르는 작은 창구) | 실습에서 쪽을 더한다 |
| `components/` | **화면 부품** — `SiteNav` · `PageHeader` · `KpiCard` · `GradeBadge` · `BarRow` · `DataTable` · `Notice` · `DeployBadge` | 있는 것을 먼저 쓴다 |
| `lib/` | **계산 · 형식 · DB** — `format.ts`(`usd()` · `krw()` · `pct()` · `kst()` 서울 시각) · `db.ts`(DB 연결) | `db.ts`는 고치지 않는다 |
| `data/` | **원본 데이터** — `buyers.json` · `buyers.csv`(바이어 150곳) · `fx_fallback.json`(저장된 환율) · `tone_matrix.csv` · `dunning_templates.md` · `README.md`(데이터 사전) | 읽기만 |
| `guide/` | **작업 안내서** — `design_rules.md`(화면 규칙) · `day4_lab_d.md` · `day5_lab_c.md` · `day5_lab_d.md` · `day6_hackathon.md`. 프롬프트가 「절」을 가리키면 AI가 그 절을 읽고 그대로 합니다 | 읽기만 |
| `hackathon/` | **6일차 양식** — 아이디어 카드 · SPEC 틀 · README 틀 · 발표 대본 · 심사 기준 · 아이디어 씨앗 · 가상 데이터 견본 | 6일차에 복사해 쓴다 |
| `prisma/` | **표 설계** — `schema.prisma`(5일차 실습 C에서 모델을 더한다) | 5일차부터 |
| `scripts/` | **도구** — `doctor.mjs`(점검) · `env-init.mjs` · `update-guide.mjs` · `catchup.mjs` · `lib/`(AI 엔진 찾기 · 부르기) | `doctor` · `lib/`는 고치지 않는다 |
| `CLAUDE.md` · `AGENTS.md` | AI가 매번 먼저 읽는 규칙(한국어) · Next.js 판 안내 | 6일차에 내 절을 더한다 |
| `package.json` · `package-lock.json` | 부품 목록과 정확한 판(고정) | 고치지 않는다 — 새 패키지는 먼저 묻기 |
| `.env.example` · `vercel.json` · `.devcontainer/` · `.vscode/` · `.claude/` | 비밀값의 **이름만** · 서울 지역 설정 · Codespaces 설정 · VS Code 설정(터미널은 명령 프롬프트) · AI 권한 | `.env.example`은 새 변수 이름만 더한다(값 없이) · 나머지는 고치지 않는다 |

- 스택은 **판을 고정**했습니다 — Next.js 16.4.2 · React 19.3.1 · TypeScript 5.9.3 · Tailwind CSS 4.3.3 · Prisma 7.10.1 · Node 24. AI가 "최신으로 올릴까요?"라고 물어도 올리지 않습니다(`CLAUDE.md`에 적혀 있습니다).
- 데이터는 모두 **(가상) 한빛정밀(주)의 합성 데이터**입니다. 3일차 리스크 보드의 바이어 150곳과 같은 바이어입니다.

## 명령 한눈에 {#commands}

터미널(++ctrl+grave-accent++)에서 웹 저장소 폴더 기준으로 실행합니다. 파이썬 쪽에 익숙하다면 오른쪽 칸과 견주어 보세요.

| 명령 | 하는 일 | 언제 | 파이썬(uv)이라면 |
|---|---|---|---|
| `npm ci` | `package-lock.json`에 적힌 판 그대로 부품을 설치 | 새 저장소마다 처음 한 번 | `uv sync` |
| `npm run dev` | 내 PC에서 개발 서버 — http://localhost:3000 · 끄기는 ++ctrl+c++ | 화면을 보며 만들 때 | `uv run …` |
| `npm run build` | **출고 검사** — 타입 오류 0이어야 통과. Vercel도 같은 검사를 한다 | 커밋 · push 전마다 | – |
| `npm run doctor` | 내 작업대 점검 — 줄마다 통과 / 실패와 고치는 법 | 막히면 먼저 · 매일 아침 | – |
| `npm run doctor:db` | DB 주소 두 줄 점검 · 연결 시험(비밀번호는 가려서) | 5일차 | – |
| `npm run doctor:secrets` | 비밀 · 키 · 실제 메일 주소가 섞이지 않았는지 | push 전 | – |
| `npm run env:init` | `.env.example` → `.env` 만들기(없을 때만) | 5일차 13:10 | – |
| `npm run db:push` | 표 설계를 내 DB에 반영 → 코드 다시 만들기 → 표마다 RLS 켜기 | 5일차 | – |
| `npm run db:seed` | 처음 데이터(바이어 150곳) 넣기 — 두 번 넣어도 150곳 | 5일차 | – |
| `npm run drafts` | AI가 독촉 초안을 미리 쓴다(`claude -p`) — 시험은 `npm run drafts -- --dry-run` | 5일차 실습 D | – |
| `npm run guide:update` | 고쳐진 안내서 · 데이터 · 해커톤 양식 받기 | 매일 아침 · 강사가 말할 때 | `get_day_files.py` |
| `npm run catchup -- day4-d` | 기준본으로 합류(`day4-d` · `day5-c` · `day5-d`) | 늦었을 때 | 그날 시작 파일 |

!!! warning "버전 없이 설치하지 않습니다"

    `npm install 이름`처럼 판을 적지 않고 설치하면 시험판이 깔릴 수 있습니다(예: `prisma`의 최신 표시는 시험판입니다). 새 패키지가 꼭 필요하면 AI가 **이름 · 이유 · 고정 판**을 먼저 묻고, 사람이 승인한 뒤 `npm i 이름@판 --save-exact`로 설치합니다. `npx prisma …`도 직접 치지 않고 위의 `npm run` 명령을 씁니다.

## 점검 도구 — `npm run doctor` {#doctor}

막히면 **사람보다 먼저 doctor**에게 묻습니다. 줄마다 통과 / 실패가 나오고, 실패한 줄에는 고치는 법이 한국어로 붙어 있습니다.

| 명령 | 보는 것 | 언제 |
|---|---|---|
| `npm run doctor` | Node 24.x · npm · git · 부품 설치(Next.js · Prisma 판) · 원격 저장소(origin) · `.env`가 있는지(값은 보이지 않음) · AI 엔진(`claude`)을 찾았는지와 그 판 · `ANTHROPIC_API_KEY`가 **없는지** · 사용자 폴더 · 저장소 경로에 한글 · 빈칸이 있는지 · 저장소가 OneDrive 안인지 · 연결(npm · Prisma 엔진 · GitHub · Vercel · Supabase · 환율 API) | 설치 직후 · 매일 아침 · 막힐 때 |
| `npm run doctor:db` | 주소 두 줄의 모양 — 포트 6543 · 5432, 사용자 `postgres.…`, `[YOUR-PASSWORD]`가 남았는지, 괄호 · 기호, 직접 연결 주소(`db.….supabase.co`)를 쓰지 않았는지 → 두 주소로 실제 연결 · 응답 시간 · 표 개수. 오류 번호를 한국어 해결책으로 바꿔 준다 | 5일차 `.env`를 채운 뒤 · DB 오류 때 |
| `npm run doctor:secrets` | 커밋된 `.env` · 비밀번호가 든 DB 주소 · 비밀 냄새가 나는 `NEXT_PUBLIC_` 이름 · 화면 코드(`.next/static`)에 박힌 `.env` 값 · 키 모양 문자열이 있으면 **실패**, `@….example`이 아닌 메일 주소는 **경고** | push 전 · 발표 전 |

- 4일차에는 `.env`가 없는 것이 정상입니다 — doctor가 '5일차'라고 알려 줍니다.
- `ANTHROPIC_API_KEY`가 설정돼 있으면 doctor가 경고합니다. 스타터의 도우미는 그 키를 빼고 AI 엔진을 부르지만, VS Code의 Claude Code는 그 키로 API 요금을 낼 수 있으니 쓰지 않는 키라면 지웁니다 → [사전 준비 0-4](setup.md#claude-code).
- AI 엔진(`claude -p`)은 **따로 설치하지 않습니다.** VS Code의 Claude Code 확장 안에 이미 들어 있고, 스타터의 도구가 그 자리를 찾아 씁니다. 못 찾으면 doctor가 어디를 봤는지 알려 줍니다.

## 고쳐진 안내서 받기 · 늦었을 때 합류 {#update}

템플릿으로 만든 저장소는 그 순간의 사본이라, 강사가 안내서를 고쳐도 저절로 오지 않습니다. 명령 두 개가 그 다리입니다.

**`npm run guide:update`** — 웹 스타터에서 `guide/` · `data/` · `hackathon/`만 새 판으로 가져옵니다.

1. 처음이면 스타터를 `starter`라는 이름의 원격으로 더하고, 새 판을 받아 위 세 폴더만 바꿉니다.
2. 그 폴더에 **커밋하지 않은 변경이 있으면 멈춥니다** — 먼저 커밋하고 다시 실행합니다.
    `data/` · `hackathon/`에서 **내가 고쳐 커밋한 파일**(예: 6일차에 채운 아이디어 카드)은 덮어쓰지 않고 '건너뜀'으로 알려 줍니다.
3. 끝에 바뀐 파일 목록(`git status --short`)과 '다음:' 줄을 보여 줍니다 → 그 메시지(`5일차: 안내서 받기`)로 **커밋**합니다. 커밋하기 전에는 `catchup`도, 다음 `guide:update`도 멈춥니다.
4. 무엇이 바뀌는지 먼저 보려면 `npm run guide:update -- --check`(파일은 그대로). 강사가 따로 말할 때만 `-- --infra`(점검 도구 · DB 연결 파일) · `-- --deps`(부품 목록 + `npm ci`)를 붙입니다.

**`npm run catchup -- day4-d`** — 지난 실습을 못 끝냈거나 결석했을 때 **기준본**으로 합류합니다(`day4-d` · `day5-c` · `day5-d`).

1. 스타터의 기준본에서 `app/` · `components/` · `lib/` · `prisma/`(5일차 실습 D는 초안 스크립트도)를 가져옵니다. 작업 트리가 깨끗하지 않으면 멈춥니다.
2. `npm run build`로 확인 → 커밋 `5일차: 합류 — 4일차 실습 D 기준본` → push(내 주소가 새로 배포됩니다).
3. 5일차 기준본으로 합류했다면 **내 DB**에 `npm run db:push` → `npm run db:seed`를 한 번 합니다(표와 데이터는 저장소가 아니라 내 Supabase에 있습니다).

## 설치가 막히면 — Codespaces {#codespaces}

Codespaces는 GitHub이 빌려주는 클라우드 컴퓨터에서 브라우저로 VS Code를 쓰는 서비스입니다. 웹 스타터에는 설정(`.devcontainer`)이 들어 있어서 **Node 24 설치와 `npm ci`가 저절로** 끝난 작업실이 열립니다. 관리자 권한이 없거나, 회사 망이 npm을 막거나, `npm ci`가 끝나지 않을 때 씁니다.

1. github.com에서 **내 웹 저장소**를 열고 초록색 **Code** → **Codespaces** 탭 → **Create codespace on main**.
2. 처음에는 몇 분 걸립니다. 터미널의 `npm ci`가 끝나면 `npm run doctor` → `npm run dev`.
3. 오른쪽 아래 알림(또는 **포트** 탭의 '내 웹앱' 3000)에서 **브라우저에서 열기**를 누르면 내 화면이 보입니다.
4. Claude Code 패널에서 **Sign in** — 브라우저에 나온 코드를 패널에 붙여 넣습니다. Codespaces는 **Plan** 모드로 시작합니다.
5. 여기서 커밋 · push해도 Vercel이 똑같이 배포합니다. 쓰지 않을 때는 왼쪽 아래 **Codespaces** → **Stop Current Codespace**.

- 개인 무료 계정은 한 달 사용 시간이 정해져 있습니다(과정 저장소의 [0-9](setup.md#codespaces)와 같은 한도). 비상용으로 쓰고, 끝나면 멈춥니다.
- 5일차 `npm run drafts`의 AI 엔진도 Codespaces 안의 Claude Code 확장에서 찾습니다.

## Vercel — 내 주소 {#vercel}

| 알아 둘 것 | 이렇게 |
|---|---|
| push = 배포 | `main`에 커밋 · push하면 Vercel이 새로 빌드해 내 주소를 바꿉니다. **빌드가 실패하면 마지막으로 성공한 화면이 그대로** 남습니다 — 고쳐서 다시 push |
| 운영 주소 · 긴 배포 주소 | 나눠 줄 주소는 짧은 **운영 주소** `tradefin-web-t2-07.vercel.app`(이름은 소문자)입니다. 배포마다 생기는 긴 주소(`…-해시-….vercel.app`)는 남이 열면 **Vercel 로그인 화면**이 뜹니다. 프로젝트 화면의 **Domains**에 보이는 주소를 씁니다 |
| 이름이 이미 있으면 | Vercel이 다른 짧은 주소를 정합니다 — 역시 **Domains**에 보이는 주소가 내 운영 주소입니다 |
| 환경 변수(5일차) | **Settings → Environment Variables**에 이름 · 값 · 대상(Production · Preview)을 넣고 **Redeploy**. 값을 바꾼 뒤 다시 배포하지 않으면 예전 값으로 돕니다 |
| 지역 | 스타터의 `vercel.json`이 서버를 **서울(`icn1`)**에 둡니다. 5일차 DB도 서울로 만들어 가까이 둡니다 |
| 저장소가 목록에 없다 | GitHub 앱 권한이 '선택한 저장소만'이라서입니다 → Import 화면의 **Adjust GitHub App Permissions** → 저장소 추가(6일차 `hack-…`도 같은 방법) |
| 요금 | **Hobby(무료)** — 개인 · 비상업용입니다. 카드 등록 없이 씁니다. 결제 화면이 나오면 멈추고 손을 듭니다 |
| 로그 | 배포 실패는 **Deployments → 해당 배포 → Build Logs**의 맨 아래 10줄을, 화면의 500 오류는 **Logs**를 봅니다 |

## Supabase — 내 DB(5일차) {#supabase}

| 언제 | 무엇 |
|---|---|
| 4일차 실습 C · D 중 | **가입만** — GitHub로(Continue with GitHub). 프로젝트는 아직 만들지 않습니다 → [사전 준비 9-4](setup.md#supabase) |
| 5일차 13:00 | 함께 **New project** — 이름 `tradefin-web` · 지역 **Northeast Asia (Seoul)** · DB 비밀번호는 **영문 + 숫자 16자 이상, 기호 없이**(내 메모에만 · 채팅 · 저장소 · 캡처 금지) |
| 5일차 13:10 | **Connect → ORMs → Prisma**에서 두 줄을 복사 → `npm run env:init` → ++ctrl+p++ → `.env`를 열어 붙여 넣기 → `[YOUR-PASSWORD]` 두 곳을 내 비밀번호로 → 저장 → `npm run doctor:db` |
| 5일차 14:24 | Vercel 환경 변수에 `DATABASE_URL`(6543 줄)을 넣고 Redeploy — 휴대폰과 내 PC가 **같은 DB**를 봅니다 |

- **주소 두 줄의 역할** — `DATABASE_URL`은 **트랜잭션 풀러(포트 6543)**: 앱과 Vercel이 씁니다. `DIRECT_URL`은 **세션 풀러(포트 5432)**: 표를 바꾸는 명령(`npm run db:push`)이 씁니다. `db.….supabase.co`로 시작하는 직접 연결 주소는 쓰지 않습니다(무료 요금제에서는 IPv6 전용이라 많은 망에서 닿지 않습니다).
- **표는 `npm run db:push`로만** 바꿉니다. "데이터가 지워진다"는 질문이 나오면 `N`을 누르고 손을 듭니다.
- 무료 요금제는 **프로젝트 2개**까지이고, **일주일 동안 쓰지 않으면 일시정지**됩니다 → 대시보드에서 **Restore**(몇 분).
- **6일차**는 저장이 꼭 필요한 아이디어만 DB를 씁니다. 그때는 **새 프로젝트**를 만듭니다 — 5일차 DB에 다른 표 설계를 밀어 넣으면 기존 표가 지워질 수 있습니다. 2개 한도에 걸리면 5일차 프로젝트를 일시정지합니다. 저장이 필요 없으면 `data/*.json`으로 충분합니다.

## 지킬 것 다섯 줄 {#rules}

<div class="tf-rules" markdown>

1. **비밀은 두 곳에만** — 내 PC의 `.env`와 Vercel 환경 변수 칸. 코드 · 커밋 · 채팅 · 캡처에는 남기지 않습니다. AI에게도 `.env`를 열지 말라고 `CLAUDE.md`와 권한 설정이 막아 둡니다.
2. **`NEXT_PUBLIC_`으로 시작하는 값은 브라우저로 간다** — 누구나 볼 수 있으니 비밀을 넣지 않습니다.
3. **데이터는 가상만** — (가상) 한빛정밀(주), 메일 주소는 `@….example`. 실명 · 실제 회사 · 계좌는 쓰지 않습니다.
4. **실제로 보내지 않는다** — 메일 · 메시지는 초안과 승인 기록까지. 되돌릴 수 없는 일은 사람이 누릅니다.
5. **push 전에 `npm run build`와 `npm run doctor:secrets`** — 둘 다 통과해야 내 주소에 올립니다.

</div>

`.env`를 실수로 커밋했다면 파일을 지우는 것으로 끝나지 않습니다(이력에 남습니다) → [FAQ → .env를 커밋했어요](faq.md#q-env-committed).

## 막힐 때 {#stuck}

**10분 규칙** — 10분 넘게 같은 곳에서 막히면 아래 사다리를 한 칸씩 올라갑니다.

1. `npm run doctor`(DB면 `npm run doctor:db`) — 실패한 줄의 고치는 법대로
2. 실습 쪽의 **'원인부터' 프롬프트** — 오류 끝 10줄을 붙여 원인 후보와 확인 방법만 먼저 묻는다(아직 고치지 않게)
3. 짝에게 2분
4. 손을 들거나 노트북 위에 빨간 표시 — 또는 오픈채팅에 `[도움] T{조}-{번호} / 단계 / 증상 한 줄` + 캡처(비밀번호 · 키가 보이지 않게)
5. [Codespaces](#codespaces)로 옮기기 · 실습 쪽의 채팅 경로

| 증상 | 이렇게 |
|---|---|
| PowerShell에서 `npm.ps1 … 스크립트를 실행할 수 없으므로` | 스타터의 VS Code 터미널은 명령 프롬프트(cmd)가 기본입니다. 그래도 PowerShell이면 `npm.cmd ci`처럼 쓰거나 한 번만 `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` → [사전 준비 9-2](setup.md#npm-policy) |
| `node`(또는 `npm`)를 찾을 수 없다 | Node 설치 뒤 **VS Code를 완전히 닫았다가 다시** 엽니다(창 하나만 닫으면 안 됩니다) → [사전 준비 9-1](setup.md#node) |
| `npm ci`가 끝나지 않는다 · `ETIMEDOUT` | 기다리는 동안 Vercel의 내 주소는 살아 있습니다. 15:25 규칙 → Codespaces. `binaries.prisma.sh`가 막혔다면 휴대폰 핫스팟이나 Codespaces |
| 내 PC에서는 되는데 Vercel 빌드만 실패 | 파일 이름의 **대소문자** — Windows는 구분하지 않고 Vercel(Linux)은 구분합니다. 빌드 로그 맨 아래 10줄을 '원인부터' 프롬프트에 |
| 보낸 주소가 Vercel 로그인 화면으로 열린다 | 긴 배포 주소를 보냈습니다 → **Domains**의 운영 주소 |
| GitHub 앱이 내 저장소를 못 본다 | **Adjust GitHub App Permissions** → 저장소 추가 |
| `… only works in a Client Component` | 클릭 · 상태(`useState`) 같은 화면 움직임을 서버 컴포넌트에 썼습니다 → 움직이는 부분만 작은 부품으로 떼고 맨 위에 `'use client'`. 데이터 읽기는 서버 쪽에 그대로 |
| `'use client'` 파일이 데이터 · DB · 비밀값을 읽는다 | 그 코드는 브라우저로 갑니다 → 데이터는 서버 컴포넌트에서 읽고, 화면 부품에는 값만 넘깁니다(props) |
| 3000번이 이미 쓰인다 | Next.js가 3001 같은 다른 번호로 엽니다 — 터미널의 `Local:` 줄을 읽습니다 |
| 사용 한도에 걸렸다 | `/model`로 Sonnet · 짝과 한 화면 · 실습 쪽의 채팅 경로 → [FAQ](faq.md#q-usage-limit) |

웹 실습에서 자주 묻는 것은 [FAQ → 4–6일차 웹 실습](faq.md#web)에, 용어는 [용어집 → 웹 실습 용어](glossary.md#web)에 있습니다.
