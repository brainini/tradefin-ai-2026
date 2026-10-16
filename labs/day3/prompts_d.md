# 3일차 프롬프트 — 실습 D

실습 D '바이어 리스크 한눈에'(6–7교시 · 15:00–16:50)에서 쓰는 프롬프트입니다. 모두 **Claude Code**(VS Code 확장 · 내 저장소를 연 채로)에서 보냅니다. 복사 버튼 :material-content-copy: 으로 통째로 복사하고, `{중괄호}` 자리만 바꿔 붙여 넣습니다(중괄호 기호도 지웁니다).

**프롬프트는 짧고, 긴 규칙은 작업 안내서에 있습니다.** 프롬프트마다 첫 줄이 '목적', 다음 줄이 할 일입니다. 정제 규칙 · 화면 구성 · 설정 숫자 · HTML 규칙 · 커밋 규칙 같은 세부는 `labs/day3/lab-d/lab_d_guide.md`의 절에 있고, 프롬프트는 「1. 메모와 표 훑기」처럼 절 이름으로 가리킵니다. 궁금하면 안내서를 열어 봐도 됩니다.

| 부 · 단계 | 프롬프트 | 안내서의 절 | 남는 것 |
|---|---|---|---|
| 1부 · D-1 · 01 | [d1](#d1) 메모와 표 훑기 | 1 | 답만(파일 없음) |
| 1부 · D-1 · 02 | 없음 — 레퍼런스 사냥은 손으로 | – | `workbench/day3/refs/` 캡처 2장 · `links.md` |
| 1부 · D-1 · 03 | [d2](#d2) 디자인 주문서 | 2 | `workbench/day3/outputs/design.md` |
| 1부 · D-1 · 04 | [d3](#d3) 첫 화면 v1(Plan) | 3 · 4 | `scripts/board_page.py` · `buyer_board.html` v1 |
| 1부 · D-1 · 05 | [d8](#d8) 커밋 | 5 | 커밋 1개 |
| 2부 · D-2 · 01 | [스타일 A–E](#style) 하나 · 고르기 어려우면 [머리 3안](#heads) | 6 | v2 · (`head_options.html`) |
| 2부 · D-2 · 02 | [기능 ①–⑥](#feat) 1–2개 | 7 | v3 |
| 2부 · D-2 · 03 | [d6](#d6) 비평 · [d6-fix](#d6) 하나만 고치기 | 8 | v4 |
| 2부 · D-2 · 04 | [d7](#d7) 게시 · claude.ai는 [d7-chat](#d7) | 9 | 공유 링크 |
| 2부 · D-2 · 05 | [d8-push](#d8-push) 커밋 · push | 5 | 커밋 · `d3-board` push |
| 언제든 | [d-check](#d-check) 숫자가 다를 때 · [d-chat](#d-chat) 채팅 경로 첫 메시지 | 10 · 11 | – |

---

## 1부 · 같이 따라 하기

### d1 · 메모와 표 훑기 {#d1}

**모드 Manual** · 읽기만 합니다(파일을 만들지 않음)

<!-- --8<-- [start:d1] -->
```text
목적: 화면을 그리기 전에 대표님 요청과 표를 숫자로 먼저 파악한다.
@labs/day3/lab-d/lab_d_guide.md 의 「1. 메모와 표 훑기」대로 @labs/day3/lab-d/ceo_request.md 와 @labs/day3/lab-d/buyer_board.csv 를 읽기만 하고 답해 줘.
```
<!-- --8<-- [end:d1] -->

### d2 · 디자인 주문서 {#d2}

결과 `workbench/day3/outputs/design.md`. 캡처를 파일로 두지 않고 입력창에 붙여 넣었다면 두 `@경로`를 '붙여 넣은 두 화면'으로 바꿉니다.

<!-- --8<-- [start:d2] -->
```text
목적: 레퍼런스 2장을 AI가 지킬 '디자인 주문서'로 바꾼다(화면은 아직 만들지 않는다).
@workbench/day3/refs/ref1.png 와 @workbench/day3/refs/ref2.png 를 보고 @labs/day3/lab-d/lab_d_guide.md 의 「2. 디자인 주문서」대로 design.md 를 써 줘.
```
<!-- --8<-- [end:d2] -->

### d3 · 첫 화면 v1 {#d3}

**모드 Plan** · 결과 `scripts/board_page.py` · `workbench/day3/outputs/buyer_board.html`

<!-- --8<-- [start:d3] -->
```text
목적: 대표님이 월요일에 볼 보드 첫 화면(v1)을 만든다. 먼저 계획을 보여 주고, 내가 승인하면 만들어.
@labs/day3/lab-d/lab_d_guide.md 의 「3. 첫 화면 v1」과 「4. 결과 페이지 규칙」대로, 토큰은 @workbench/day3/outputs/design.md 에서.
```
<!-- --8<-- [end:d3] -->

### d8 · 커밋 {#d8}

<!-- --8<-- [start:d8] -->
```text
목적: v1을 저장해 두고, 2부에서 무엇을 바꿔도 이 화면으로 돌아올 수 있게 한다.
@labs/day3/lab-d/lab_d_guide.md 의 「5. 커밋 규칙」대로 d3-board 브랜치에 커밋해 줘.
```
<!-- --8<-- [end:d8] -->

---

## 2부 · 내 스타일로 키우기

### 스타일 A–E — 하나 고르기 {#style}

D-2 · 01. 하나만 보냅니다. 결과는 v2(`design.md`에 '(v2에서 바뀜)' 줄).

<!-- --8<-- [start:style-a] -->
```text
목적: 보드 전체를 'A 밝은 미니멀'로 바꾼다(v2) — 숫자와 구역은 그대로.
@labs/day3/lab-d/lab_d_guide.md 의 「6. 2부 옵션 — 스타일」에서 A와 공통 규칙대로 해 줘.
```
<!-- --8<-- [end:style-a] -->

<!-- --8<-- [start:style-b] -->
```text
목적: 보드 전체를 'B 다크 금융 터미널'로 바꾼다(v2) — 숫자와 구역은 그대로.
@labs/day3/lab-d/lab_d_guide.md 의 「6. 2부 옵션 — 스타일」에서 B와 공통 규칙대로 해 줘.
```
<!-- --8<-- [end:style-b] -->

<!-- --8<-- [start:style-c] -->
```text
목적: 보드 전체를 'C 매거진 · 보고서형'으로 바꾼다(v2) — 숫자와 구역은 그대로.
@labs/day3/lab-d/lab_d_guide.md 의 「6. 2부 옵션 — 스타일」에서 C와 공통 규칙대로 해 줘.
```
<!-- --8<-- [end:style-c] -->

<!-- --8<-- [start:style-d] -->
```text
목적: 보드 전체를 'D 휴대폰 앱형'으로 바꾼다(v2) — 숫자와 구역은 그대로.
@labs/day3/lab-d/lab_d_guide.md 의 「6. 2부 옵션 — 스타일」에서 D와 공통 규칙대로 해 줘.
```
<!-- --8<-- [end:style-d] -->

<!-- --8<-- [start:style-e] -->
```text
목적: 내가 고른 레퍼런스의 분위기까지 따라 보드를 바꾼다(v2) — 숫자와 구역은 그대로.
@labs/day3/lab-d/lab_d_guide.md 의 「6. 2부 옵션 — 스타일」에서 E와 공통 규칙대로 해 줘.
```
<!-- --8<-- [end:style-e] -->

### 머리 3안 비교 — 고르기 어려울 때 {#heads}

`{A · B · C}`는 견줘 볼 세 안으로 바꿉니다(예: `B · C · D`). 하나를 고르면 그 안의 스타일 프롬프트를 보냅니다.

<!-- --8<-- [start:heads] -->
```text
목적: 바로 고르기 어려우니 머리 영역만 세 안으로 견줘 보고 고른다.
@labs/day3/lab-d/lab_d_guide.md 의 「6. 2부 옵션 — 스타일」 '머리 3안 비교'대로 {A · B · C} 세 안을 만들어 줘.
```
<!-- --8<-- [end:heads] -->

### 기능 ①–⑥ — 1–2개 더하기 {#feat}

D-2 · 02. 한 번에 하나씩 보내고, 브라우저를 새로 고쳐 본 뒤 다음 것을 보냅니다. 결과는 v3.

<!-- --8<-- [start:feat-1] -->
```text
목적: 상위 10의 한 곳을 누르면 '확인해 볼 이유'가 보이고, 판단은 사람이 단추로 남기게 한다.
@labs/day3/lab-d/lab_d_guide.md 의 「7. 2부 옵션 — 기능」 ① 상세 패널대로 보드에 더해 줘.
```
<!-- --8<-- [end:feat-1] -->

<!-- --8<-- [start:feat-2] -->
```text
목적: 대표님이 위험 선 세 개를 나란히 놓고 '어디에 그을지' 견주게 한다.
@labs/day3/lab-d/lab_d_guide.md 의 「7. 2부 옵션 — 기능」 ② 선 시나리오 비교대로 보드에 더해 줘.
```
<!-- --8<-- [end:feat-2] -->

<!-- --8<-- [start:feat-3] -->
```text
목적: 돈이 어느 지역에 물려 있는지 지도처럼 한눈에 보이게 한다.
@labs/day3/lab-d/lab_d_guide.md 의 「7. 2부 옵션 — 기능」 ③ 지역 타일 · 히트맵대로 보드에 더해 줘.
```
<!-- --8<-- [end:feat-3] -->

<!-- --8<-- [start:feat-4] -->
```text
목적: 회의 자리에 놓을 A4 한 장을 같은 숫자로 뽑게 한다.
@labs/day3/lab-d/lab_d_guide.md 의 「7. 2부 옵션 — 기능」 ④ 경영진 한 장대로 보드에 더해 줘.
```
<!-- --8<-- [end:feat-4] -->

<!-- --8<-- [start:feat-5] -->
```text
목적: 대표님께 메신저로 보낼 3줄을 보드가 지금 숫자로 써 주게 한다.
@labs/day3/lab-d/lab_d_guide.md 의 「7. 2부 옵션 — 기능」 ⑤ 3줄 브리핑대로 보드에 더해 줘.
```
<!-- --8<-- [end:feat-5] -->

<!-- --8<-- [start:feat-6] -->
```text
목적: 내 아이디어를 보드에 더한다 — {내 아이디어 한 줄}.
@labs/day3/lab-d/lab_d_guide.md 의 「7. 2부 옵션 — 기능」 ⑥대로 계획 3줄을 먼저 보여 주고, 내가 좋다고 하면 만들어.
```
<!-- --8<-- [end:feat-6] -->

### d6 · AI 티 지우기 — 비평 · 하나만 고치기 {#d6}

D-2 · 03. 먼저 내 화면을 캡처해 `workbench/day3/refs/my_v3.png`로 저장합니다. `{번호}`는 비평 표의 번호 하나입니다.

<!-- --8<-- [start:d6] -->
```text
목적: AI는 제 화면을 못 본다 — 캡처를 보여 주고 디자이너처럼 아쉬운 점을 짚게 한다(아직 고치지 않는다).
@workbench/day3/refs/my_v3.png 가 지금 내 화면이야. @labs/day3/lab-d/lab_d_guide.md 의 「8. AI 티 지우기」 '비평'대로 답해 줘.
```
<!-- --8<-- [end:d6] -->

<!-- --8<-- [start:d6-fix] -->
```text
목적: 한 번에 하나만 고쳐, 무엇이 좋아졌는지 눈으로 확인한다.
비평 표의 {번호}번만 고쳐 줘 — @labs/day3/lab-d/lab_d_guide.md 의 「8. AI 티 지우기」 '하나만 고치기'대로.
```
<!-- --8<-- [end:d6-fix] -->

### d7 · 게시 {#d7}

D-2 · 04. 경로 1은 Claude Code, 경로 2는 claude.ai 새 대화(`buyer_board.html` 첨부)입니다. 게시된 링크는 처음에 **나만** 볼 수 있습니다 — 공유를 '링크가 있는 사람'으로 바꿉니다.

<!-- --8<-- [start:d7] -->
```text
목적: 대표님이 휴대폰으로 열 링크 하나를 만든다.
@labs/day3/lab-d/lab_d_guide.md 의 「9. 게시」대로 workbench/day3/outputs/buyer_board.html 을 그대로 Claude 아티팩트로 게시해 줘.
```
<!-- --8<-- [end:d7] -->

<!-- --8<-- [start:d7-chat] -->
```text
목적: 내 보드를 claude.ai에서 그대로 띄워 공유 링크를 만든다.
첨부한 buyer_board.html을 한 글자도 바꾸지 말고(다시 만들거나 React로 바꾸지 말고) 그대로 아티팩트로 띄워 줘. 띄운 뒤 선 17%의 C등급 곳 수 · C등급 채권을 파일 안 데이터로 계산해 알려 줘.
```
<!-- --8<-- [end:d7-chat] -->

### d8-push · 커밋 · push {#d8-push}

D-2 · 05.

<!-- --8<-- [start:d8-push] -->
```text
목적: 오늘 결과를 GitHub에 올려 월요일에도 같은 화면을 다시 만들 수 있게 한다.
@labs/day3/lab-d/lab_d_guide.md 의 「5. 커밋 규칙」대로 지금까지의 변경을 커밋하고 d3-board 브랜치를 push해 줘.
```
<!-- --8<-- [end:d8-push] -->

---

## 언제든

### d-check · 숫자가 다를 때 {#d-check}

`{항목}` · `{화면 값}` · `{기대값}`은 다른 숫자의 이름 · 내 화면의 값 · 실습 쪽 '확인할 것'의 값입니다.

<!-- --8<-- [start:d-check] -->
```text
목적: 숫자가 다르면 고치기 전에 어디서 갈렸는지부터 찾는다.
화면의 {항목}이 {화면 값}인데 기대값은 {기대값}이야. 아직 고치지 말고 @labs/day3/lab-d/lab_d_guide.md 의 「10. 숫자가 다를 때」대로 알려 줘.
```
<!-- --8<-- [end:d-check] -->

### d-chat · 채팅 경로 첫 메시지 {#d-chat}

Claude Code를 못 쓸 때, claude.ai 새 대화에 `buyer_board.csv` · `ceo_request.md` · `lab_d_guide.md`를 첨부하고 이 글을 먼저 보낸 뒤 d1부터 같은 문장을 보냅니다.

<!-- --8<-- [start:d-chat] -->
```text
목적: Claude Code 없이 claude.ai에서 같은 실습을 한다.
첨부한 lab_d_guide.md(작업 안내서)의 「11. 채팅 경로」를 먼저 읽고, 이어서 보내는 프롬프트도 그 절대로 읽어 줘.
```
<!-- --8<-- [end:d-chat] -->
