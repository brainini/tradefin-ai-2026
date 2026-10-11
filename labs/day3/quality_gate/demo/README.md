# 시연판 — 설정을 바꾼 PR을 기준 모델과 견주기 (선택)

8교시 시연 6의 저장소를 내 GitHub에 다시 만들어 봅니다. 한 줄로: **PR을 열면 GitHub 서버가 같은 데이터 · 같은 시드로 다시 학습해 기준 모델(main)과 비교하고, 기준에 못 미치면 ❌가 됩니다.** AUC가 올라도 비용이 늘면 ❌입니다.

| 파일 | 하는 일 | 내 저장소에서의 자리 |
|---|---|---|
| `params.yaml` | 학습 설정(코드 밖으로 뺀 값 — 설정만 바꾼 PR은 diff 몇 줄) | 맨 위 폴더 |
| `src/train.py` | 시간 분할 LightGBM 학습 → 지표 4개(ROC-AUC · PR-AUC · Brier · 비용) JSON | `src/` |
| `src/compare.py` | 기준 지표와 비교한 요약표 · 품질 게이트(PR-AUC ≥ 기준 − 0.01 · Brier ≤ 기준 + 0.003 · 비용 ≤ 기준 × 1.10) | `src/` |
| `scripts/make_synthetic_panel.py` | **가상(합성) 패널** 4,017행 만들기(시드 57 — 실데이터 아님) | `scripts/` |
| `train.yml` | PR이 설정 · 코드 · 데이터를 바꾸면 다시 학습하고 비교하는 워크플로 | `.github/workflows/train.yml` |

## 따라 하기

과정 저장소를 어지럽히지 않도록 **템플릿으로 새 저장소를 하나 더 만들거나**(예: `tradefin-demo`), 내 저장소에서 새 브랜치로 합니다.

1. 위 표의 자리에 파일을 복사합니다. `.github/workflows/` 폴더는 직접 만들고 `train.yml`을 그 안에 `train.yml`로 둡니다.
2. 설정 읽기에 쓰는 패키지를 더합니다 — `uv add pyyaml`(`pyproject.toml` · `uv.lock`을 함께 커밋합니다. 워크플로가 `uv sync --frozen`으로 같은 환경을 만듭니다).
3. 가상 패널을 만듭니다: `uv run python scripts/make_synthetic_panel.py` → `data/panel_synthetic.csv`(4,017행 × 19열).
4. **기준 지표**를 만듭니다: `uv run python src/train.py --params params.yaml --out reports/metrics_main.json`
   기대 출력: `ROC-AUC 0.9801 · PR-AUC 0.7249 · Brier 0.0256 · 비용 90 (놓침 13 · 오경보 25)`. 같은 숫자가 나와야 합니다(시드 · 스레드 1개로 고정).
5. `params.yaml` · `src/` · `scripts/` · `data/panel_synthetic.csv` · `reports/metrics_main.json` · `.github/workflows/train.yml` · `pyproject.toml` · `uv.lock`을 `main`에 커밋 · push합니다(`.gitignore`에 `reports/metrics.json`을 더해 두면 로컬 실행 결과가 섞이지 않습니다).
6. 브랜치 `exp/deep-trees`를 만들고 `params.yaml`의 `model:` 일곱 줄을 **설정 C(깊은 나무)**로 바꿉니다.

    ```yaml
    model:
      n_estimators: 600
      learning_rate: 0.1
      num_leaves: 63
      min_child_samples: 5
      subsample: 1
      colsample_bytree: 1
      reg_lambda: 0
    ```

   커밋(메시지 두 줄: 무엇 / 왜) → push → PR을 엽니다.
7. 20–30초 뒤 PR의 **Checks**에 `train-check`가 ❌로 뜹니다. 로그인한 화면의 **Summary**에 요약표가 있습니다.

    | 지표 | 기준(main) | 이 PR | 게이트 |
    |---|---:|---:|---|
    | ROC-AUC | 0.9801 | 0.9805 | 참고 |
    | PR-AUC | 0.7249 | 0.7394 | ✅ (≥ 0.7149) |
    | Brier | 0.0256 | 0.0336 | ❌ (≤ 0.0286) |
    | 비용 | 90 | 144 | ❌ (≤ 99.0) |

   깊은 나무는 오경보가 25건에서 14건으로 줄었지만 놓침이 13건에서 26건으로 두 배가 됩니다(5 × 26 + 14 = 144).
8. `num_leaves: 15`만 바꾼 PR(설정 B)은 비용 95가 한도 99 안이라 ✅입니다(ROC-AUC 0.9809 · PR-AUC 0.7337 · Brier 0.0255). **✅여도 병합 버튼은 사람이 누릅니다.**

Claude Code에게 시킬 때는 `labs/day3/prompts.md`의 시연 6 프롬프트 세 개(MLflow 기록 · PR 열기 · 결과 요약)를 그대로 쓰면 됩니다. MLflow는 이 폴더의 필수 도구가 아닙니다(`uv add mlflow`로 더하면 실행마다 설정 · 지표가 기록되고 `uv run mlflow ui`로 비교합니다).

## 알아 둘 것

- 숫자는 가상 패널의 값입니다. 과정 패널(`d3_features_panel.csv`)이나 오전 슬라이드의 모델 카드 숫자와 다릅니다 — **같은 비교 방식**이 보이면 됩니다.
- `train.yml`의 `paths:`가 `params.yaml` · `src/**` · `data/**`를 바꾸는 PR에서만 워크플로를 돌립니다. 비용이 무료인 것은 공개 저장소일 때입니다.
- main에 '필수 검사' 보호 규칙을 켜면 ❌인 PR의 병합 버튼이 막힙니다(공개 저장소의 GitHub Free에서도 가능). 켜지 않으면 ❌여도 버튼은 눌립니다 — 그때는 사람이 게이트 결과를 읽고 정합니다.
- 회사 실데이터 · 키는 이 저장소에 올리지 않습니다.
