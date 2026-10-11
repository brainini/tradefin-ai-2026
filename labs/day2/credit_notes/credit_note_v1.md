# credit_note v1 — 신용평가 코멘트 덧붙임

> news_score_v1.md 뒤에 붙여 쓴다. 역할·관점·척도·규칙은 그대로, 아래만 더한다.

[입력]
가상 신용평가 코멘트 1건(text). 한 바이어가 아니라 한 국가를 다루는 거시 코멘트도 있다.

[추가 출력]
rating_action — 이번 코멘트의 등급 조치: upgrade(상향) · downgrade(하향) · affirm(유지) · watch_negative · watch_positive(워치 지정) · none(등급 조치 없음)
outlook — 코멘트가 끝난 시점의 전망: positive · stable · negative · developing · none(언급 없음)

[규칙 덧붙임]
1. 등급보다 전망·워치가 먼저 움직인다. 'Watch Negative'는 하향 직전 신호로 본다.
2. 투자적격(BBB- 이상)과 투기등급(BB+ 이하)의 경계 근처라면 한 단계 변화도 무겁게 본다.
