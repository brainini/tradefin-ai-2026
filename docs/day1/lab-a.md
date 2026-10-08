# 실습 A · 4–5교시 — 내 작업 환경 · 첫 커밋 · 보고서 읽고 검증하기

!!! abstract "한눈에 보기 — 실습 A"
    | 항목 | 내용 |
    |---|---|
    | 목표 | 모두가 같은 환경(VS Code · Claude Code · GitHub)에서 **첫 커밋을 올리고**, 그 환경에서 해외 기업 보고서의 위험 신호와 재무비율을 **근거와 함께** 뽑는다 |
    | 시간 | **A-1 13:00–13:50** · 휴식 10분 · **A-2 14:00–14:50** |
    | 오전 시연을 이렇게 따라 한다 | 시연 3(템플릿 → clone → CLAUDE.md → 커밋 · push)을 **간소화** · 시연 2(공시 위험 신호)를 **변형**(다른 회사 · Claude Code로 읽고 파일로 저장 · 비율 계산 · 다른 AI와 교차 확인) |
    | 입력 | 가상 연차보고서 `data/day1/reports/halden_fictional_annual_report.md` |
    | 도구 | VS Code · **Claude Code**(모드 Manual) · GitHub · **ChatGPT 또는 Claude 웹** · 엑셀 |
    | 산출물 | 내 저장소 주소 · `CLAUDE.md` · `d1_signals_halden.md` · `d1_ratios_halden.md` · **커밋 2개 이상** |
    | 프롬프트 | [A0](../prompts/day1.md#a0) · [A1](../prompts/day1.md#a1) · [A1 재질문](../prompts/day1.md#a1-retry) · [A2](../prompts/day1.md#a2) · [A3](../prompts/day1.md#a3) |

이 실습의 목표는 AI가 보고서를 잘 요약하는지 보는 것이 아닙니다. **AI가 가져온 근거와 숫자가 진짜인지 우리가 확인하는 것**입니다.
강사가 돌아다니며 한 분씩 2–3분 확인합니다. 막히면 손을 들거나 노트북 위에 빨간 표시(스티커)를 올리세요. 짝과 한 화면을 같이 봐도 좋습니다.

## 시간표와 점검 시각 {#time}

| 시각 | 단계 | 하는 일 | 점검 |
|---|---|---|---|
| 13:00–13:20 | [① 설치 점검](#a1-check) | VS Code · Git · uv · 확장 3종 · Claude Code 로그인 · 학습 설정 끄기 · 깨진 CSV | **13:20 손 점검** |
| 13:20–13:30 | [② 내 저장소 만들기](#a1-repo) | 과정 템플릿 → Use this template → 내 공개 저장소 | 내 저장소 페이지가 열렸다 |
| 13:30–13:35 | [③ clone · 환경](#a1-clone) | Git: Clone → 작성자 신뢰 → `uv sync` | **13:35 손 점검** |
| 13:35–13:45 | [④ Claude Code · CLAUDE.md](#a1-claude) | 모드 Manual 확인 → CLAUDE.md 읽고 내 규칙 더하기 | 모드 Manual · diff에 내가 더한 줄 |
| 13:45–13:50 | [⑤ 첫 커밋 · push](#a1-commit) | 커밋 → push → GitHub에서 확인 → 주소 제출 | **13:50 첫 push** |
| 13:50–14:00 | 휴식 | | |
| 14:00–14:15 | [⑥ 위험 신호 표](#a2-signals) | 프롬프트 A1로 Halden 보고서 → 표를 파일로 저장 | 파일이 생겼다 |
| 14:15–14:20 | [⑦ 인용 확인](#a2-quotes) | 인용 2개를 ++ctrl+f++ 로 찾아 일치 · 불일치 표시 | **14:20 손 점검**(표시 2개) |
| 14:20–14:30 | [⑧ 비율 계산](#a2-ratios) | 프롬프트 A2 — 코드로 계산 | 공식 · 대입값 · 코드 |
| 14:30–14:40 | [⑨ 교차 확인](#a2-cross) | 프롬프트 A3(ChatGPT 또는 Claude 웹) → 두 결과 대조 | 차이와 원인 한 줄 |
| 14:40–14:50 | [⑩ 기준값 · 커밋](#a2-commit) | 강사 화면의 기준값과 비교 → 원인 기록 → 커밋 · push | **14:50 두 번째 push** |

!!! tip "늦었다면"
    13:35에 아직 ③ 중이어도 괜찮습니다. 설치가 막혔으면 [Codespaces](#chat-path)나 채팅 경로로 바로 바꾸고, 강사에게 손을 드세요. ⑥부터는 모두 같은 파일로 시작합니다.

## 입력 파일 {#files}

내 저장소(③ 이후)에 이미 들어 있습니다 — 따로 받을 것이 없습니다.

| 파일 | 위치 | 쓰는 곳 |
|---|---|---|
| 가상 연차보고서 Halden | `data/day1/reports/halden_fictional_annual_report.md` | ⑥–⑩ |
| 깨진 CSV 연습 파일 | `data/day1/d1_encoding_test.csv`(비교용 `d1_encoding_test_utf8bom.csv`) | ① |
| iRobot 공시 발췌 · SEC 추출 비율표 | `data/day1/reports/irobot.md` · `data/day1/real_buyers_ratios.csv` | 다 했으면 |

저장소를 아직 만들지 못했거나 채팅 경로로 가는 분은 [1일차 → 파일 받기](index.md#files)에서 필요한 파일만 받습니다. 프롬프트의 빈칸(`{파일}` · `{회사}`)은 [빈칸 값 표](../prompts/day1.md#values)에 있습니다.

---

## A-1 · 내 작업 환경과 첫 커밋 {#a1}

### ① 설치 점검 (13:00–13:20) {#a1-check}

사전 준비에서 해 온 것을 **한 칸씩 확인**합니다. 안 된 칸은 [사전 준비](../setup.md)의 해당 항목으로 가거나 강사를 부릅니다.

- [ ] **터미널** — VS Code를 열고 ++ctrl+grave++ (키보드의 백틱 `` ` `` 키)로 터미널을 엽니다. 다음 세 줄이 모두 버전을 보여 주면 됩니다.

    ```text
    code --version
    git --version
    uv --version
    ```

    "찾을 수 없다 / 인식되지 않는다"가 나오면 터미널과 VS Code를 **완전히 닫았다가 새로 엽니다.** 그래도 같으면 [사전 준비 — Git](../setup.md#git) · [uv](../setup.md#uv)를 봅니다.
- [ ] **커밋 작성자 이름** — 로그인이 아니라 **커밋에 찍히는 작성자 표시**입니다. 이 저장소는 공개이므로 실명과 회사 이메일 대신 별명과 GitHub의 noreply 주소를 권합니다.

    ```text
    git config --global user.name "내 별명"
    git config --global user.email "내GitHub아이디@users.noreply.github.com"
    ```

    noreply 주소는 GitHub **Settings → Emails**에서 "Keep my email addresses private"를 켜면 보입니다.
- [ ] **확장 3종** — ++ctrl+shift+x++ 로 확장 화면을 열어 **Claude Code for VS Code**(게시자 **Anthropic**) · **Python** · **Jupyter**가 설치돼 있는지 봅니다. 비슷한 이름의 다른 확장이 많으니 게시자를 꼭 확인합니다.
- [ ] **Claude Code 로그인** — 파일을 하나 열면 편집기 오른쪽 위에 Claude 아이콘이 보입니다(아래 상태 표시줄의 `Claude Code`도 같습니다). 누르면 로그인 방법을 묻습니다.

    <figure markdown="span">
      ![Claude Code 설치 네 단계 — 확장 설치, 작성자 신뢰, 로그인 방법 고르기, 첫 질문과 답](../assets/screens/d1-claude-code-install.png){ loading=lazy }
      <figcaption>① 확장 설치(게시자 Anthropic) → ② 폴더 작성자 신뢰 → ③ 로그인 방법 → ④ 첫 질문과 답, 입력창 아래의 모드(Manual)</figcaption>
    </figure>

    구독 계정(Pro · Team · Enterprise)은 **Claude.ai Subscription**, API 계정은 **Anthropic Console**을 고르고 브라우저에서 승인합니다. 그림 ②의 신뢰 창 문구가 `code-server provides…`로 보이는 것은 브라우저에서 도는 VS Code로 찍어서입니다 — 여러분 화면에는 `Code provides…`로 나옵니다. **무료(Free) 플랜으로는 로그인되지 않습니다** — [채팅 경로](#chat-path)로 갑니다.
- [ ] **AI의 '모델 개선(학습)' 설정 끄기** — 쓰는 서비스마다 끕니다. 켜져 있으면 내가 올린 대화가 모델 학습에 쓰일 수 있습니다.

    <figure markdown="span">
      ![ChatGPT 설정 데이터 제어 화면 — 모델 개선을 위한 데이터 학습 허용 스위치가 켜진 상태(파란색)와 끈 뒤(회색)](../assets/screens/d1-chatgpt-data-controls.png){ loading=lazy }
      <figcaption>ChatGPT — 설정 › 데이터 제어 › '모델 개선을 위한 데이터 학습 허용': ① 켜짐(파란색) → ② 끈 뒤(회색)</figcaption>
    </figure>

    - **ChatGPT** — 설정 › 데이터 제어에서 위 스위치를 끕니다(계정 화면에 따라 '모든 사람을 위한 모델 개선'처럼 이름이 조금 다를 수 있습니다).
    - **Claude(claude.ai)** — 설정 › 개인정보에서 '모델 개선(Help improve Claude)' 스위치를 끕니다.
    - 학습을 꺼 둬도 **좋아요 · 싫어요 버튼을 누르면** 그 대화가 개선용으로 저장될 수 있으니 누르지 않습니다. 민감한 내용은 임시(시크릿) 채팅을 씁니다. 자세한 안내는 [사전 준비 — AI 학습 설정 끄기](../setup.md#ai-training).
- [ ] **깨진 CSV 다시 열기** — [파일 받기](index.md#files)에서 `d1_encoding_test.csv`를 받아 엑셀에서 **더블클릭**하면 한글이 깨져 보입니다. 이번에는 이렇게 엽니다. 엑셀 새 통합 문서 → **데이터 › 텍스트/CSV에서** → 파일 선택 → **파일 원본: 65001: 유니코드(UTF-8)**로 바꾸기 → **로드**. 한글이 제대로 보이면 됩니다(파일이 망가진 것이 아니라 읽는 규칙이 달랐던 것입니다).

**13:20 손 점검** — 강사가 돌며 위 칸을 확인합니다.

### ② 내 저장소 만들기 (13:20–13:30) {#a1-repo}

과정 템플릿으로 **내 공개 저장소**를 만듭니다. 이 저장소가 오늘부터 여섯 날의 작업장이 됩니다.

1. 브라우저에서 GitHub에 **로그인**한 뒤 [github.com/brainini/tradefin-ai-2026](https://github.com/brainini/tradefin-ai-2026)을 엽니다. 이름 옆에 **Public template** 표시가 있는 저장소입니다.

    <figure markdown="span">
      ![GitHub의 과정 템플릿 저장소 첫 화면 — 저장소 이름 옆 Public template 표시에 빨간 상자](../assets/screens/d1-template-repo.png){ loading=lazy }
      <figcaption>템플릿 저장소 — 이름 옆 'Public template'. 그림은 로그아웃 상태라 보이지 않지만, <strong>GitHub에 로그인하면</strong> 화면 위쪽(Code 단추 근처)에 초록색 <strong>Use this template</strong> 단추가 나타납니다</figcaption>
    </figure>

2. **Use this template → Create a new repository**를 누릅니다.
3. **Owner**는 내 계정, **Repository name**은 `tradefin-my-T{조}-{번호}`(예: 1조 1번 → `tradefin-my-T1-01`), 공개 범위는 **Public**으로 둡니다. **Create repository**를 누릅니다.
4. 내 저장소 페이지가 열리면 끝입니다. 주소(`https://github.com/내아이디/tradefin-my-T1-01`)를 복사해 둡니다.

!!! note "왜 공개인가"
    짝이 초대 없이 보고 댓글을 달 수 있고, 내일부터 쓰는 브랜치 · PR · 자동 검사가 모두 공개 저장소에서 무료로 돌아갑니다. 대신 **회사 실데이터 · 실명 · 키 · 비밀번호는 절대 올리지 않습니다.** 비공개로 만들어졌다면 Settings › Collaborators에서 짝과 강사를 초대합니다.

### ③ clone · 환경 (13:30–13:35) {#a1-clone}

1. VS Code에서 ++ctrl+shift+p++ → **`Git: Clone`** → ②에서 복사한 내 저장소 주소를 붙여 넣고 Enter → 저장할 폴더를 고릅니다. 처음에는 GitHub 로그인 창이 뜰 수 있습니다(브라우저에서 승인).

    <figure markdown="span">
      ![VS Code 명령 팔레트에서 Git: Clone을 고르고 저장소 주소를 붙여 넣는 두 장면](../assets/screens/d1-git-clone.png){ loading=lazy }
      <figcaption>① 명령 팔레트에서 <code>Git: Clone</code> → ② 주소 칸에 <strong>내 저장소 주소</strong>를 붙여 넣기(그림의 주소는 강사 시연 저장소)</figcaption>
    </figure>

2. 폴더를 열면 **"이 폴더의 작성자를 신뢰합니까?"** 창이 뜹니다 — **Yes, I trust the authors**를 누릅니다. 신뢰하지 않으면(제한 모드) Claude Code가 동작하지 않습니다.
3. 터미널에서 환경을 만듭니다. 처음에는 몇 분 걸릴 수 있습니다(교실 Wi-Fi가 붐비면 더 걸립니다).

    ```text
    uv sync
    uv run python scripts/hello.py
    ```

    `환경 준비 완료 — Python 3.13.x · pandas 3.x.x`가 나오면 성공입니다. `.venv` 폴더가 생기지만 커밋하지는 않습니다(자동으로 제외돼 있습니다).

**13:35 손 점검** — 저장소가 열렸고 `hello.py`가 한 줄을 찍었는지 봅니다.

### ④ Claude Code · CLAUDE.md (13:35–13:45) {#a1-claude}

1. 파일을 하나 열고 편집기 오른쪽 위의 **Claude 아이콘**으로 패널을 엽니다. 패널이 좁으면 `Claude Code: Open in New Tab`으로 편집기 탭에 열면 넓게 보입니다.
2. **입력창 아래의 모드 표시부터 봅니다.** 시작 모드는 PC마다 다를 수 있어서, **Manual**이 아니면 모드 단추를 눌러 **Manual**로 바꿉니다(필수). Manual은 파일 편집과 명령 실행을 **매번 내가 승인**하는 모드입니다.

    <figure markdown="span">
      ![VS Code 다섯 구역 — 탐색기, 편집기, 터미널, 소스 제어, Claude Code 패널에 번호를 붙인 화면](../assets/screens/d1-vscode-five-zones.png){ width="760" loading=lazy }
      <figcaption>VS Code 다섯 구역 — ① 탐색기 ② 편집기 ③ 터미널 ④ 소스 제어(파란 배지 = 바뀐 파일 수) ⑤ Claude Code 패널. 패널 입력창 아래에 모드(<strong>Manual</strong>)와 모델 이름이 보입니다</figcaption>
    </figure>

3. 저장소에는 **`CLAUDE.md`가 이미 들어 있습니다.** Claude Code가 대화를 시작할 때마다 먼저 읽는 업무 매뉴얼입니다. 탐색기에서 열어 **한 번 읽어 봅니다**(원본 `data/`는 읽기만, 결과는 `workbench/`에, 숫자는 코드와 함께, 모르면 '확인 필요' …).
4. Claude Code에게 **내 업무 규칙 한두 줄**을 더해 달라고 합니다. 규칙은 직접 정합니다(회사 이름 · 실명 · 실제 숫자는 쓰지 않습니다 — 공개 저장소입니다).

    ??? example "프롬프트 A0 — 펼쳐서 복사"
        ```text
        @CLAUDE.md 를 읽고, '일하는 방식' 맨 아래에 내 업무 규칙 두 줄을 더해 줘.
        - {내 규칙 ①}
        - {내 규칙 ②}
        다른 줄은 고치지 마. 바뀔 내용(diff)을 먼저 보여 줘.
        ```
        규칙 예: "숫자에는 기준일과 통화(또는 단위)를 함께 쓴다" · "외국어 문서의 인용은 원문 그대로 두고 번역은 따로 쓴다" · "메일은 초안 파일로만 만들고 보내지 않는다" · "추정한 값에는 '추정'이라고 표시한다".

5. **허락 창**이 뜨면 오른쪽의 **바뀌는 내용(diff)을 읽습니다.** 내가 더한 줄만 바뀌는지 확인하고 `1 Yes`를 누릅니다. 다른 줄까지 바뀌면 `No`로 거절하고 "다른 줄은 고치지 마"를 다시 말합니다. `2 Yes, allow all edits…`처럼 허락 범위를 넓히는 선택은 오늘 쓰지 않습니다.

!!! tip "허락 창 읽는 법 — 세 가지"
    **무엇을**(어떤 파일 · 어떤 명령) · **어디에**(어느 폴더) · **지우는가**(없애거나 덮어쓰는 것이 있는가). 모르는 명령이면 `No`로 거절하고 "이 명령이 뭐 하는 거야?"라고 물어보세요. 파일 삭제 · 강제 push · `git reset --hard`는 거절합니다.

<figure markdown="span">
  ![Claude Code의 명령 허락 창 — 스크립트를 실행하고 합계를 검산하는 명령 전체가 보이고 1 Yes, 2 Yes allow for this project, 3 No 선택지가 있다](../assets/screens/d1-permission-bash.png){ width="760" loading=lazy }
  <figcaption>명령 허락 창의 예(시연 3의 한 장면 — 스크립트 실행 + 합계 검산). 명령을 <strong>끝까지 읽고</strong> <code>1 Yes</code>. 2번(<code>Yes, allow … for this project</code>)은 허락 범위를 넓히는 선택이라 오늘은 쓰지 않습니다</figcaption>
</figure>

### ⑤ 첫 커밋 · push (13:45–13:50) {#a1-commit}

1. 왼쪽 막대의 **소스 제어** 아이콘(가지 모양, 바뀐 파일 수가 파란 배지로 보입니다)을 누르면 `CLAUDE.md` 한 파일이 **M**(수정)으로 보입니다. 파일을 눌러 바뀐 줄(diff)을 한 번 더 봅니다.
2. 위의 메시지 칸에 씁니다. 첫 줄은 **무엇을**, **한 줄 비우고**, 다음 줄은 **왜**입니다(`CLAUDE.md`의 규칙 — 빈 줄이 있어야 `git log --oneline`에 첫 줄만 보입니다).

    ```text
    1일차: CLAUDE.md에 내 업무 규칙 추가

    왜: 매번 같은 말을 반복하지 않으려고
    ```

3. **Commit**을 누르고(스테이징 안내가 뜨면 **Yes**), 이어서 **Sync Changes**(또는 아래 상태 표시줄의 ⟳ 0↓ 1↑)를 눌러 GitHub에 올립니다(push). 처음에는 GitHub 로그인 창이 뜹니다.
4. 브라우저에서 **내 저장소**를 새로고침해 방금 커밋이 맨 위에 보이는지, 메시지에 `왜:` 줄이 있는지 확인합니다.

    <figure markdown="span">
      ![GitHub 커밋 화면 — 첫 줄은 무엇을, 그 아래 왜: 로 시작하는 줄이 있는 메시지와 바뀐 줄의 비교(diff)](../assets/screens/d1-github-commit.png){ width="760" loading=lazy }
      <figcaption>GitHub에서 본 커밋 하나 — 메시지(무엇 · 왜)와 바뀐 줄(diff). 그림은 강사 시연 저장소의 두 번째 커밋입니다</figcaption>
    </figure>
5. 내 저장소 주소를 강사가 안내하는 제출 폼에 붙여 넣습니다(링크는 [사이트 홈의 공지](../index.md)에 있습니다).

!!! info "Claude Code에게 시켜도 됩니다"
    입력창에 "바뀐 내용을 요약해서 커밋하고 push 해 줘"라고 쓰면 같은 순서를 밟습니다. 허락 창의 명령에서 **커밋 메시지에 '무엇'과 '왜'가 있는지**, **어느 브랜치로 push하는지**(`main`)를 읽고 승인합니다.

**13:50 첫 push** — 내 저장소 화면에 내 커밋이 보이면 A-1 완료입니다.

### A-1 완료 기준

- [ ] 내 공개 저장소가 있고 VS Code로 열었다 · `uv sync`가 끝났다
- [ ] Claude Code 모드가 **Manual**이고, 첫 질문에 답이 돌아왔다
- [ ] `CLAUDE.md`에 내가 더한 규칙이 있고 **커밋 1개**가 GitHub에 보인다(메시지에 `왜:` 줄)
- [ ] Claude · ChatGPT의 학습 설정을 껐다

---

## A-2 · AI로 보고서 읽고 검증하기 {#a2}

오전 시연 2를 **다른 회사로** 해 봅니다. 가상 영국 유통 바이어 Halden의 연차보고서이고, 이번에는 채팅이 아니라 **Claude Code로 읽고 결과를 파일로 저장**합니다. 같은 보고서를 **다른 AI**에도 시켜 두 결과를 견줍니다.

### ⑥ 위험 신호 표 (14:00–14:15) {#a2-signals}

1. Claude Code 패널의 `+`(새 대화)로 **새 대화**를 엽니다. 모드가 **Manual**인지 다시 봅니다. 한 대화에서는 문서 하나만 다룹니다.
2. 프롬프트 **A1**을 붙여 넣고 `{파일}` · `{회사}`를 바꿉니다(`data/day1/reports/halden_fictional_annual_report.md` · `halden`).

    ??? example "프롬프트 A1 — 펼쳐서 복사"
        ```text
        @data/day1/reports/halden_fictional_annual_report.md 을 읽고 대금 지급 위험 신호를 찾아라.
        <역할> 수출기업 신용관리 분석가 </역할>
        <맥락> 이 바이어에게 60일 외상(O/A)으로 수출한다. 결정은 사람이 한다. </맥락>
        <과제> 체크리스트 8개 유형(계속기업 불확실성 · 유동성 부족 · 차입 약정 위반 · 차입 만기 ·
        매출 감소·영업손실 · 자본잠식 · 결제조건 변경 · 구조조정)을 하나씩 점검하라. </과제>
        <형식> 위험 신호 표: 신호 | 원문 인용 | 위치 | 심각도(상/중/하) + 안심 요소 표 + 세 줄 요약 </형식>
        <제약> 인용은 원문 그대로. 찾지 못한 유형은 '명시되지 않음' </제약>
        결과는 outputs 폴더에 d1_signals_halden.md 로 저장해.
        ```

3. 허락 창이 뜨면 읽고 `1 Yes`합니다(파일 읽기 · 결과 파일 쓰기). 결과는 **`workbench/day1/outputs/d1_signals_halden.md`**에 저장됩니다.
4. 탐색기에서 그 파일을 열고 ++ctrl+shift+v++ 로 **Markdown 미리보기**를 켜면 표가 보입니다.

<figure markdown="span">
  ![6요소 프롬프트의 결과 표 — 신호, 영문 원문 인용, 쪽, 심각도, 왜 위험한가 열이 있는 표의 앞부분](../assets/screens/d1-signals-table-example.png){ width="760" loading=lazy }
  <figcaption>이런 모양의 표가 나오면 방향이 맞습니다(오전 시연 2의 결과 예시 — 다른 회사의 공시입니다). 원문 인용 열과 위치(쪽) 열이 있어 <strong>직접 찾아 검증</strong>할 수 있습니다</figcaption>
</figure>

**확인할 것** — 표 세 종류(위험 신호 · 안심 요소 · 세 줄 요약)가 있는지, 체크리스트 8개 유형이 표에 보이는지(찾지 못한 유형은 '명시되지 않음'), 안심 요소가 위험 신호 표에 섞이지 않았는지 봅니다.

### ⑦ 인용 확인 (14:15–14:20) {#a2-quotes}

AI가 준 **문장**은 원문에서 직접 찾아봅니다.

1. 표에서 **원문 인용 2개**를 고릅니다(서로 다른 신호로).
2. 탐색기에서 `data/day1/reports/halden_fictional_annual_report.md`를 엽니다.
3. ++ctrl+f++ 를 누르고 인용 문장을 붙여 넣습니다. **일치**하면 편집기에 강조가 뜨고(`1 of 1`), 없으면 `No results`가 나옵니다. 안 찾아지면 문장 중간의 **짧은 낱말 4–5개**로 다시 찾아 봅니다.
4. 결과 파일의 표에 **확인 열**을 하나 더하고, 찾은 행에 `일치`, 못 찾은 행에 `불일치`를 직접 적습니다(표시 2개).

    ```text
    | 신호 | 원문 인용 | 위치 | 심각도 | 확인 |
    |---|---|---|---|---|
    | … | "…" | … | 상 | 일치 |
    ```

5. **불일치**가 있으면 A1 재질문으로 그 행만 다시 시킵니다.

    ??? example "프롬프트 A1 재질문 — 펼쳐서 복사"
        ```text
        표의 {N}번 행 인용을 원문에서 찾지 못했다. 원문 문장을 글자 그대로 다시 인용하고, 없으면 '명시되지 않음'으로 바꿔라.
        ```

**14:20 손 점검** — 표시 2개가 있는지 봅니다.

### ⑧ 비율 계산 (14:20–14:30) {#a2-ratios}

AI가 준 **숫자**는 공식 · 대입한 값 · 계산 코드를 받아 다시 확인합니다. 숫자는 AI의 암산이 아니라 **코드가** 내게 합니다.

??? example "프롬프트 A2 — 펼쳐서 복사"
    ```text
    @data/day1/reports/halden_fictional_annual_report.md 의 재무표로 4개 비율을 계산해 줘.
    - 유동비율 = 유동자산 ÷ 유동부채, 부채비율 = 총부채 ÷ 자기자본, DSO = 매출채권 ÷ 매출 × 기간 일수, 영업이익률 = 영업이익 ÷ 매출
    - 표: 비율 | 공식 | 대입한 숫자(원문 위치) | 결과 | 해석 한 줄
    - 계산은 scripts/ratios_halden.py 로 하고 코드를 남겨. 기간이 1년이 아니면 일수를 바꿔.
    - 결과는 outputs 폴더에 d1_ratios_halden.md 로 저장해.
    ```

1. 같은 대화에서 A2를 붙여 넣고 허락 창을 읽어 승인합니다(코드 파일 쓰기 · `uv run` 실행).
2. 결과 `d1_ratios_halden.md`와 코드 `scripts/ratios_halden.py`가 생겼는지 봅니다.
3. 대입한 숫자가 **재무표의 어느 줄 · 어느 열**인지, 그 열이 **당기**인지, 단위(천 파운드)와 기간(연간 = 365일)을 밝혔는지 봅니다. 자본이 0 이하이면 부채비율은 '해석 불가'입니다.

??? note "좋은 답의 모양 — 시연에서 본 예(다른 회사의 분기 공시)"
    <figure markdown="span">
      ![Claude Code의 재무비율 계산 답 — 결과 표, 대입한 숫자와 원문 위치 표, 계산 코드, 계산 기준과 주의할 점](../assets/screens/d1-ratio-answer.png){ width="720" loading=lazy }
      <figcaption>공식 · 대입한 숫자와 위치 · 계산 코드가 한 답에 있고, 계산 기준(분기 매출이라 기간 일수 91일)을 밝힙니다</figcaption>
    </figure>

### ⑨ 교차 확인 (14:30–14:40) {#a2-cross}

**ChatGPT 또는 Claude 웹**의 **새 대화**에 같은 보고서를 올려 같은 비율을 계산시킵니다. 다른 회사의 AI일수록 차이가 잘 드러나니 둘 다 있으면 ChatGPT를 권합니다.

??? example "프롬프트 A3 — 펼쳐서 복사"
    ```text
    첨부한 연차보고서의 재무표로 유동비율·부채비율·DSO·영업이익률을 계산해 줘.
    공식, 대입한 숫자와 그 위치, 사용한 파이썬 코드를 보여 줘. 원문에 없는 숫자는 쓰지 마.
    ```

1. 새 대화를 열고 `halden_fictional_annual_report.md`를 **첨부**합니다([파일 받기](index.md#files)에서 받은 파일).
2. A3를 붙여 넣어 결과를 받습니다. 코드를 실행하는 기능(ChatGPT는 데이터 분석, Claude는 코드 실행)이 켜져 있어야 계산을 코드로 합니다.
3. 두 결과(A2와 A3)를 **`d1_ratios_halden.md` 아래에 나란히** 붙이고, 다르면 **차이의 원인을 한 줄** 적습니다 — 어느 열을 썼나 · 총부채를 어떻게 더했나 · 기간 일수를 몇 일로 했나.

!!! warning "회사 파일은 올리지 않습니다"
    오늘 올리는 파일은 가상 보고서와 공개 공시뿐입니다. 회사 실데이터는 익명화한 것이라도 AI 대화창에 올리지 않습니다.

### ⑩ 기준값 · 커밋 (14:40–14:50) {#a2-commit}

1. **14:40**에 강사가 **기준값을 강사 화면으로** 보여 줍니다(파일로 나눠 주지 않습니다). 그 전까지는 내 숫자를 믿고 가 봅니다.
2. 기준값과 내 숫자(A2)·AI 숫자(A3)를 비교합니다. 다르면 **차이의 원인**(열 · 단위 · 합산 방식 · 기간 일수)을 `d1_ratios_halden.md` 맨 아래에 적습니다. 맞은 것도 "맞았다"고 한 줄 적어 둡니다.
3. 커밋하고 push합니다.

    ```text
    1일차: Halden 위험 신호 표와 재무비율 추가

    왜: 인용과 계산 코드를 남겨 AI 결과를 검증하려고
    ```

**14:50 두 번째 push** — 내 저장소에 커밋이 **2개 이상**이고, `workbench/day1/outputs/`에 두 파일이 보이면 A-2 완료입니다.

### A-2 완료 기준 {#checkpoint}

- [ ] `d1_signals_halden.md` — 위험 신호 표 + 안심 요소 표 + 세 줄 요약 · **인용 2개에 일치/불일치 표시**
- [ ] `d1_ratios_halden.md` — 비율 4개의 공식 · 대입값 · 두 AI의 결과 대조 · 차이의 원인
- [ ] `scripts/ratios_halden.py` — 계산 코드가 저장소에 있다
- [ ] 커밋 2개 이상, 메시지에 `왜:` 줄

## 다 했으면 {#extend}

- **iRobot 공시로 반복**: ⑥–⑧을 `data/day1/reports/irobot.md`(`{회사}` = `irobot`)로 한 번 더 하고, `data/day1/real_buyers_ratios.csv`에서 iRobot 행(`row_role`이 '발췌 일치')의 `current_ratio` · `debt_to_equity` · `dso_days` · `op_margin_pct`와 AI 결과를 견줍니다. 차이가 **1%를 넘으면 원인**(기간 · 단위 · 총부채 정의)을 적습니다.
- **Wolfspeed 분기 공시**: `wolfspeed.md`로 A2를 하되 **분기 보고서라 기간 일수가 91일**입니다. 365를 곱하면 DSO가 약 4배로 부풀려집니다.
- **프롬프트 저장**: 잘 된 A1을 고쳐 `workbench/day1/prompts/A1_위험신호_v2.md`로 저장하고 커밋합니다 — 프롬프트도 이름과 판 번호를 붙여 이력을 남깁니다.

---

## 막힐 때 {#troubleshooting}

| 증상 | 이렇게 해 보세요 |
|---|---|
| 로그인 창이 안 뜬다 | 브라우저 팝업을 허용하고 다시 누릅니다. 로그인 뒤 VS Code로 돌아오지 못하면 브라우저에 표시된 코드를 패널에 붙여 넣습니다 |
| Claude 아이콘(Spark)이 안 보인다 | 파일을 하나 엽니다 → VS Code를 업데이트합니다 → ++ctrl+shift+p++ → `Developer: Reload Window` → 폴더 신뢰(제한 모드가 아닌지) |
| 모드가 Auto · Plan으로 시작한다 | 입력창 아래 모드 단추를 눌러 **Manual**로 바꿉니다. 시작 모드는 저장소 설정으로 정할 수 없어 PC마다 다릅니다 |
| push가 거부된다 · 로그인을 묻는다 | VS Code 왼쪽 아래 **계정 아이콘**에서 GitHub에 로그인합니다. `GH007 … private email` 오류면 `git config --global user.email`을 noreply 주소로 바꾸고 다시 커밋합니다 |
| `Use this template` 단추가 안 보인다 | GitHub에 **로그인**했는지 봅니다(로그아웃 화면에는 없습니다) |
| `uv` · `git` · `code`를 찾을 수 없다 | 터미널과 VS Code를 **완전히 닫았다가** 새로 엽니다. 그래도 같으면 설치를 다시 합니다 |
| `uv sync`가 오래 걸린다 · 실패한다 | 처음에는 몇 분 걸립니다. 회사 망이 pypi.org · github.com을 막으면 개인 노트북이나 Codespaces로 갑니다 |
| 인용이 Ctrl+F로 안 찾아진다 | 문장 중간의 짧은 낱말 4–5개로 찾습니다. 그래도 없으면 **불일치** — A1 재질문으로 그 행만 다시 |
| 두 AI의 숫자가 다르다 | 당기 · 전기 열을 바꿔 썼는지, 단위(천 파운드)와 기간(365일)이 같은지, 총부채를 유동 + 비유동으로 더했는지 봅니다 |
| 결과 파일이 안 만들어졌다 | 허락 창에서 `No`를 눌렀는지 확인하고 "결과를 outputs 폴더에 저장해 줘"를 다시 말합니다 |

## 설치가 막혔거나 Claude Code를 못 쓸 때 {#chat-path}

**Codespaces(브라우저로 같은 작업실)** — 회사 PC라 설치가 막힌 경우입니다. 내 저장소 → **Code → Codespaces → Create codespace on main**. 몇 분 뒤 브라우저에 VS Code가 열리고 Python 3.13 · uv · 확장 3종이 준비됩니다. Claude Code 패널에서 로그인하고, Codespaces는 **Plan 모드로 시작**하니 승인할 때 편집마다 승인하는 선택('manually approve edits')을 고릅니다. 개인 계정은 월 사용 시간이 정해져 있으니 비상용으로만 씁니다 → [사전 준비 — Codespaces](../setup.md#codespaces).

**채팅 경로(Claude Code 계정이 없을 때)** — 같은 실습을 claude.ai 또는 ChatGPT와 GitHub 웹 화면으로 합니다.

1. [파일 받기](index.md#files)에서 `halden_fictional_annual_report.md`를 받습니다.
2. 새 대화에 보고서를 **첨부**하고 A1 · A2를 붙여 넣습니다. `@파일` 줄은 지우고, "결과는 outputs 폴더에 … 저장해" 줄은 **"결과는 Markdown 표로 보여 줘"**로 바꿉니다. 인용 확인(⑦)은 받은 파일을 메모장이나 브라우저에서 열어 ++ctrl+f++ 로 같은 방식으로 합니다. ChatGPT 무료는 하루 업로드 수가 적으니 Claude를 먼저 권합니다.
3. 받은 표를 복사해 `d1_signals_halden.md` · `d1_ratios_halden.md`로 저장하고, 내 저장소(②에서 만든 것)의 `workbench/day1/outputs/` 폴더에서 **Add file → Upload files**(또는 **Create new file**)로 올립니다. 커밋 메시지는 '무엇' · 빈 줄 · '왜'로 씁니다.
4. GitHub 로그인이 안 되면 결과 파일을 USB나 메신저로 강사에게 전달하고, 다음 날 아침 시작 파일로 합류합니다.

더 많은 경우는 [사전 준비 — 자주 막히는 곳](../setup.md#stuck)과 [FAQ](../faq.md)에 있습니다.

## 다음 — 실습 B {#next}

15:00에 [실습 B](lab-b.md)를 시작합니다. 같은 저장소에서 **바이어 150곳 파일**을 진단하고 노트북으로 탐색합니다. 쉬는 시간에 A-2 결과를 한 번 더 push해 두세요.
