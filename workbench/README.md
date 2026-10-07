# workbench — 내 작업 기록 폴더

이 폴더는 **2일차 8교시에 과정 저장소를 템플릿으로 만든 내 개인 저장소**(`tradefin-my-T{조}-{번호}`)에서 씁니다.
2–5일차에 만든 **규칙 · 프롬프트 · 데이터 사전 · 결과 파일**을 날마다 커밋해, '언제 · 무엇을 · 왜' 바꿨는지 남기는 곳입니다.
과정 저장소(`brainini/tradefin-ai-2026`)에 있는 이 폴더는 빈 틀입니다. 2일차 서랍에만 시작 파일 3개(`정제규칙.md` · `P2-2_감성점수.md` · `데이터사전.md`)가 들어 있습니다 — 내 내용으로 고쳐 같은 이름으로 올리면 내 파일로 바뀝니다.

## 구조

```text
workbench/
  README.md        ← 이 파일
  day2/
    rules/         사람이 정한 규칙(.md)
    prompts/       내가 쓰고 고친 프롬프트(이름 + 판 번호)
    data/          데이터 사전, 과정이 준 가상 데이터의 작은 사본
    outputs/       그날 결과 파일(CSV · 엑셀 · Orange .ows · 노트북)
  day3/            (같은 서랍 4개)
  day4/            (같은 서랍 4개)
  day5/            (같은 서랍 4개)
```

서랍마다 있는 `.gitkeep`은 빈 폴더를 GitHub 화면에 보이게 하려고 넣은 빈 파일입니다. 그대로 두어도 됩니다.

## 서랍 4개

| 서랍 | 넣는 것 | 파일 이름 예 |
|---|---|---|
| `rules/` | 사람이 정한 규칙 — 정제 규칙 · 등급 컷 · 경보 기준 · AI 사용 규칙 | `정제규칙.md` |
| `prompts/` | 실제로 쓴 프롬프트. 이름과 판 번호를 붙이고, 고칠 때마다 커밋 | `P2-2_감성점수.md` |
| `data/` | 데이터 사전, 과정이 준 **가상 데이터**의 작은 사본 | `데이터사전.md` |
| `outputs/` | 그날 결과 파일 | `d2_end_features.csv` · `d3_orange_model.ows` |

그날 폴더(`dayN/`) 바로 아래에는 메모 파일을 둡니다: `notes.md`(재현 메모) · `issues.md`(이슈 링크) · `spec.md`(명세 1장) · `links.md`(앱 · 챗봇 · 워크플로 주소).

## 일차별로 넣을 것

| 일차 | 넣을 것 | 언제 |
|---|---|---|
| 2일차 | `rules/정제규칙.md` · `prompts/P2-2_감성점수.md` · `data/데이터사전.md` · `outputs/d2_end_features.csv` | 8교시 첫 커밋 — 커밋 2개 이상(규칙 한 줄을 고쳐 두 번째 커밋) |
| 3일차 | `outputs/d3_orange_model.ows` · `outputs/d3_end_scored.csv` · `notes.md`(시드 · AUC · 버전) — 🔵 Colab의 'GitHub에 사본 저장'도 이 폴더로 | 8교시 |
| 4일차 | `prompts/P4-1_리포트.md`(고칠 때마다 커밋하고 diff 확인) · `issues.md`(디버깅 이슈 링크) | 블록 B · 8교시 |
| 5일차 | `spec.md`(명세 1장 — Given/When/Then) · `links.md`(앱 · 챗봇 · 워크플로 주소) | 블록 B · 8교시 |

## 커밋 메시지는 두 줄

```text
무엇: 결측 대체를 평균에서 중위수로 바꿈
왜: 매출 규모가 한쪽으로 치우쳐 평균이 대표값이 아님
```

## 올리면 안 되는 것

이 저장소는 **공개**가 기본입니다. 비공개로 바꿔도 아래 규칙은 같습니다.

- 회사 실데이터 — **익명화본도 포함**. 회사 문서, 고객 · 바이어 실명
- API 키 · 비밀번호 · `secrets.toml` · `.env`
- 이름 · 이메일 · 전화 · 계좌 같은 개인정보
- 실명 · 회사명이 들어간 파일 이름이나 커밋 메시지

저장소의 `.gitignore`가 `secrets.toml` · `.env` · `private/` 폴더 · 이름에 `_private`가 든 파일을 막아 주지만,
**GitHub 웹 화면의 Upload files는 `.gitignore`와 관계없이 고른 파일을 그대로 올립니다.** 올리기 전에 파일을 한 번 더 봅니다.
실수로 올렸다면 파일을 지우는 것으로 끝나지 않습니다(커밋 이력에 남습니다). 바로 강사에게 알리고, 키였다면 키부터 교체합니다.

## 웹 화면만으로 하는 법

| 하고 싶은 것 | 누르는 곳 |
|---|---|
| 파일 올리기 | 서랍 폴더로 들어가 **Add file** → **Upload files** → 끌어다 놓기 → 메시지 두 줄 → **Commit changes** |
| 파일 고치기 | 파일을 열고 연필 아이콘(**Edit this file**) → 고치기 → **Commit changes** |
| 바뀐 이력 보기 | 파일 화면의 **History** → 커밋을 누르면 diff(빨강 = 지운 줄, 초록 = 더한 줄) |
| 이전 버전 열기 | 커밋 목록에서 `<>`(Browse repository at this point) |

버튼 이름은 GitHub가 바꿀 수 있습니다. 자세한 순서는 과정 사이트의 [기초 F2 · 첫 커밋](https://brainini.github.io/tradefin-ai-2026/foundations/f2.html#first-commit)에 있습니다.
