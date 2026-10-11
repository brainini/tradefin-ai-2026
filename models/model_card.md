# 모델 카드 — day3_lgbm_v1 (30일 연체확률 pd_30d)

> (가상) 한빛정밀(주) 교육용 합성 데이터로 학습한 **교육용 모델**이다. 실제 여신 판단에 쓰지 않는다.

| 항목 | 내용 |
|---|---|
| 목적 | 바이어별 `late_30d`(기준일 후 30일 안에 외상 인보이스가 '만기 + 30일'선을 미결로 넘을 확률) 예측 → S/A/B/C 등급 |
| 학습 데이터 | `data/checkpoints/d3_features_panel.csv` 바이어×월 패널(거래 중 바이어) — 학습 2024-03~2025-12(2,723행), 검증 2026-01~08(1,084행), 최종 모델은 2024-03~2026-08 전체(3,807행) |
| 알고리즘 | LightGBM 이진 분류(불균형 보정 없음 — 확률이 보정된 상태로 나온다), 파라미터 `{"n_estimators": 300, "learning_rate": 0.03, "num_leaves": 7, "min_child_samples": 30, "subsample": 0.8, "subsample_freq": 1, "colsample_bytree": 0.8, "reg_lambda": 5.0}`, seed 42 |
| 특성 | 42개 — `feature_list.json`(숫자 33 · 이진 2 · 결제방식 원-핫 7). 빈칸은 그대로(LightGBM 처리) |
| 검증(2026-01~08) | ROC-AUC 0.9759 · PR-AUC 0.7089 · Brier 0.02563 · 양성률 5.6% |
| 임계값 | t = 0.1698 — 비용 FN:FP = 5:1 최소(학습 기간 월별 확장창 12개). 이론값 1/6 = 0.1667 |
| 혼동행렬(검증, t) | TP 55 · FN 6 · FP 46 · TN 977 (재현율 0.902, 정밀도 0.545) |
| 등급 | S < t/4 ≤ A < t/2 ≤ B < t ≤ C → 2026-09-30 150개사: {'S': 127, 'A': 2, 'B': 3, 'C': 18} |
| 파일 | `day3_lgbm.pkl`(joblib, LGBMClassifier) · `day3_lgbm.txt`(LightGBM 네이티브 — 버전 의존이 적다, stlite용) · `feature_list.json` · `grade_cutoffs.json` · `metrics.json` |
| 한계 | ① 합성 데이터(150개사) ② 라벨이 '이미 결제기일이 지난 미결 건'에서만 생기므로 현재 연체 지표가 예측을 거의 결정한다(검증 AUC가 높은 이유) — 지금 연체가 없는 바이어끼리의 순위는 신뢰도가 낮다 ③ 신규 바이어·조작된 재무제표(브로커형 사기)는 모델이 낮은 위험으로 볼 수 있다 ④ SHAP 기여는 모델의 판단 근거이지 원인이 아니다 |
| 재현 | `python tools/build_checkpoints.py` → `python tools/train_day3_model.py`(같은 seed·데이터·라이브러리 버전이면 같은 결과). 버전: {"python": "3.13.9", "lightgbm": "4.7.0", "scikit-learn": "1.9.1", "pandas": "3.0.6", "numpy": "2.5.3", "shap": "0.52.0"} |
