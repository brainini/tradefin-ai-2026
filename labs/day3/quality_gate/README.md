# 3일차 품질 게이트 — 내 PR에도 ✅ / ❌ 붙이기 (수업 뒤 · 선택)

8교시 시연 6에서 본 장면입니다. PR을 열면 GitHub 서버가 검사를 돌려 결과(✅ / ❌)를 붙이고, 기준에 못 미치면 ❌가 됩니다. **병합 버튼은 사람이 누릅니다.** 이 폴더는 그것을 내 저장소에서 해 보는 두 가지 판입니다. 공개 저장소면 GitHub Actions는 무료입니다.

| 판 | 무엇을 검사하나 | 필요한 것 | 걸리는 시간 |
|---|---|---|---|
| **수강생판** — `d3-check.yml` + `check_scored.py` | 내 `d3_end_scored.csv`가 약속(150행 · 6열 · 등급 규칙)을 지키는지 | 내 저장소만(설치할 것 없음) | 약 5분 |
| **시연판** — `demo/` | PR이 바꾼 설정으로 다시 학습해 기준 모델과 견주는 품질 게이트(PR-AUC · Brier · 비용) | `uv add pyyaml` · 새 저장소 권장 | 약 20분 |

## 수강생판 — 세 단계

1. **두 파일을 내 저장소에 둡니다.** VS Code 탐색기에서 끌어다 놓거나 터미널에서:

    ```text
    mkdir -p .github/workflows tools
    cp labs/day3/quality_gate/d3-check.yml .github/workflows/d3-check.yml
    cp labs/day3/quality_gate/check_scored.py tools/check_scored.py
    ```

    (Windows PowerShell이면 `New-Item -ItemType Directory -Force .github/workflows, tools`로 폴더를 만든 뒤 `Copy-Item`을 씁니다.)
2. **내 PC에서 먼저 점검합니다.** `uv run python tools/check_scored.py` — 표가 나오고 모두 ✅이면 됩니다. 파일 경로는 기본 `workbench/day3/outputs/d3_end_scored.csv`입니다.
3. **커밋 · push · PR.** 브랜치(`d3-model`)에 올리고 PR을 열면(이미 열려 있으면 push만) PR 화면 아래 **Checks**에 `check-scored`가 뜨고, 20초쯤 뒤 ✅ 또는 ❌가 됩니다. 요약표는 Actions 실행 화면의 **Summary**에서 봅니다.

### 점검하는 열 가지

| # | 점검 | ❌일 때 먼저 볼 것 |
|---|---|---|
| 1 | 파일이 있고 UTF-8 | 파일 이름 · 위치 / 엑셀이면 'CSV UTF-8(쉼표로 분리)'로 저장 |
| 2 | 열이 정확히 6개 — `buyer_id` · `ref_date` · `pd_30d` · `grade` · `threshold_used` · `model_version` (이 순서) | 열 이름 · 순서 · 빠진 열 |
| 3 | 150행 | `d3_start_scoring.csv`를 읽었는지 |
| 4 | `buyer_id`가 겹치지 않고 예측 대상 150곳과 같다 | 행을 지웠거나 정렬하다 섞이지 않았는지 |
| 5 | `ref_date`가 모두 2026-09-30 | 시험셋(2026-08-31 등) 행이 섞이지 않았는지 |
| 6 | `pd_30d`가 0~1 사이 숫자 | 0~100으로 저장하지 않았는지(엑셀 서식만 %로) |
| 7 | `grade`가 S · A · B · C 중 하나 | 빈 칸 · `#NAME?` |
| 8 | `threshold_used`가 0~1 사이 한 가지 값 | t를 17로 적지 않았는지 |
| 9 | `grade`가 규칙(C ≥ t · B ≥ t/2 · A ≥ t/4 · 나머지 S)과 같다 | 엑셀 IFS를 **C부터** 검사했는지 · 경계 옆 행의 반올림(0.0001 이내는 통과) |
| 10 | `model_version`이 비어 있지 않다 | 빈 칸 |

내 저장소의 `data/checkpoints/d3_start_scoring.csv`가 커밋돼 있지 않으면(과정 템플릿의 `.gitignore`가 막습니다) 4번의 '150곳과 같다' 대조만 건너뜁니다.

!!! note "push가 거부되면"
    `.github/workflows/` 파일을 push할 때 'workflow' 권한이 없다는 오류가 나면, 저장소 화면에서 **Add file → Create new file**로 `.github/workflows/d3-check.yml`을 만들어 내용을 붙여 넣습니다.

## 시연판 — 설정을 바꾼 PR을 기준과 견주기

[`demo/README.md`](demo/README.md)에 단계가 있습니다. 시연 6에서 본 것과 같은 데이터(가상 패널 4,017행) · 같은 설정 세 개(기준 · 잎 15 · 깊은 나무)로, 깊은 나무는 ROC-AUC가 올라도 비용이 늘어 ❌가 되고 잎 15는 ✅가 되는 것을 직접 확인합니다. 시연의 프롬프트 세 개(MLflow 기록 · PR 열기 · 결과 요약)는 [`labs/day3/prompts.md`](../prompts.md)의 '시연 6' 항목(사이트: 프롬프트 → 3일차 → 시연 프롬프트)에 있습니다.

두 판 모두 **가상(합성) 데이터**만 쓰고, 회사 실데이터 · 키 · 비밀번호는 저장소에 올리지 않습니다.
