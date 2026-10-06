# tools — 데이터·사이트·노트북 도구

(가상) 한빛정밀(주) 합성 데이터를 만들어 Day별 파일로 나누는 파이프라인, 과정 사이트를 빌드하는 도구, Challenge 노트북 빌더가 들어 있습니다. 사양: `03_실습자료_기획안_Part1` §4·§5. 명령은 모두 **저장소 루트**에서 실행합니다.

> **과정 중에는 일부 파일이 이 저장소에 없습니다.** 실습의 정답(숨은 등급·심어 둔 결함·시나리오·정답 문구)이 들어 있는 생성기 설정과 생성기는 `.gitignore` 2절로 막아 두었다가 **과정이 끝난 뒤(2026-10-21 이후)** 올립니다(아래 '과정 뒤 공개' 표). 과정 중에 쓸 파일은 `data/day1/`·`data/checkpoints/`·`data/external/`에 이미 만들어져 있습니다.

## 지금 쓸 수 있는 도구

```bash
pip install -r requirements-docs.txt              # 사이트 빌드용(MkDocs)
python tools/sync_site_assets.py                  # 수강생 파일 → docs/downloads/ 복사 + '파일 받기' 표 조각
mkdocs build --strict -d site                     # 사이트 빌드(tools/mkdocs_hooks.py가 훅으로 붙는다)

pip install nbformat                              # 노트북 생성용(실행 검사까지 하려면 nbclient ipykernel pandas도)
python tools/build_day1_notebook.py               # Challenge 노트북 labs/day1/d1_challenge.ipynb 생성 + 규칙 점검(네트워크 없음)
python tools/build_day1_notebook.py --org <org>   # Colab 배지·데이터 주소(RAW_BASE)의 <org>를 GitHub 조직 이름으로 채워서 생성
python tools/build_day1_notebook.py --execute --user-agent "Gildong Hong gildong.hong@mycompany.com"
                                                  # 실행 검사(SEC에 접속) — User-Agent는 실행하는 사람의 영문 이름 + 이메일
```

| 파일 | 역할 | 과정 중 이 저장소만으로 실행 |
|---|---|---|
| `sync_site_assets.py` | 허용 목록에 있는 수강생 파일만 `docs/downloads/`로 복사하고 '파일 받기' 표 조각(`docs/_snippets/day1/`)과 `day1_files.zip`을 만든다. 정답·원천 경로가 섞이면 멈춘다 | 된다 |
| `mkdocs_hooks.py` | MkDocs 훅 — 내려받기용 `.md`를 페이지로 바꾸지 않고 그대로 복사, 프롬프트 제목(`## P1-4 …`)의 앵커를 `#p1-4`로 고정 | 된다(`mkdocs.yml`이 부른다) |
| `build_day1_notebook.py` | Challenge 노트북 `labs/day1/d1_challenge.ipynb`(출력 없는 수강생용)을 만들고 규칙을 점검한다. `--execute`는 사본을 임시 폴더에서 위→아래로 실행해 SEC 값과 대조한다. **`--user-agent`는 기본값이 없다** — SEC 규칙대로 본인 영문 이름과 이메일을 넘긴다(없거나 예시 주소면 실행 검사를 시작하지 않는다) | 생성·점검은 된다. 실행 검사의 일부 대조 항목(정답 차트 표·원천·강사 정답)은 그 파일이 있을 때만 한다 |
| `build_preview.py` | Day1 실습 가이드 한 페이지 미리보기(강사 검토용 HTML). 사이트와 같은 md·`mkdocs.yml` 설정으로 만들고 태그 짝·내부 링크·라이브러리 프롬프트 포함을 검사한다. 먼저 `sync_site_assets.py`. 출력 기본값은 저장소 밖 `../instructor/day1/preview/`(`--out`으로 바꾼다) | 된다(`--out` 지정) |
| `fetch_external.py` | 외부 공개 데이터 캐시 수집(FRED 환율 4종 → `data/external/`) — 네트워크는 이 스크립트만 쓴다 | 안 된다(`config.yaml`을 읽는다) |
| `tf_common.py` | 경로·설정·난수 스트림·환율·xlsx/CSV 쓰기 공용 함수 | — (다른 도구가 import) |
| `snapshot.py` | 기준일 스냅샷 피처·라벨 계산 — 누수 검사에도 쓴다 | — (생성기가 import) |
| `dictionary_spec.py` | 수강생용 데이터 사전의 정의(뜻·단위·출처만 적은 중립 설명)·코드표 | — (생성기가 import) |
| `make_day1_charts.py` | Day1 차트 4종(라이트·다크) + 표 버전 CSV → `docs/assets/day1/`(정답 수치라 과정 뒤 공개) | 안 된다(`config.yaml`을 읽는다) |
| `fonts/` | 차트·노트북용 한글 글꼴 NanumGothic(SIL OFL 1.1, `fonts/OFL.txt`) | — |
| `requirements-tools.txt` | 저장소 루트 `requirements.txt`를 그대로 가리킨다 | — |

## 과정 뒤 공개 — 지금 저장소에 없는 파일

아래 파일은 `.gitignore` 2절에 있어 과정 중에는 올라가지 않습니다. 위 표의 '안 된다' 도구와 아래 순서는 이 파일들이 공개된 뒤에 돌릴 수 있습니다.

| 파일 | 역할 | 왜 지금은 없나 |
|---|---|---|
| `config.yaml` | 모든 파라미터(교육용 가정 표시). 값은 여기서만 바꾼다 | 오염 계획·시나리오 설정 |
| `generate_data.py` | 바이어 → 부도 추첨 → 인보이스 → 결제조건 믹스 보정 → 연체 보정 → 충당 → 재무·뉴스·사건 | 숨은 정답 컬럼을 만든다 |
| `build_checkpoints.py` | 오염 주입, Day별 체크포인트, 데이터 사전 두 벌(수강생용 + 강사용 전체), 강사 정답 파일 | 오염 목록·정답 문구 |
| `day1_expected.py` | 강사용 Day1 EDA 기대값 문서 | 정답 숫자 |
| `validate_data.py` | 데이터 검사 V01~V20 | 정답 컬럼을 검사한다 |
| `build_day1_template.py` | 실습 템플릿 `labs/day1/d1_end_eda_template.xlsx` · AX 캔버스 `labs/day1/ax_canvas_template.md`(둘 다 지금 저장소에 있다)와 강사 정답 워크북을 만들고 검사한다(`--check`: 검사만) | Lab1·Lab2 정답 문구 |
| `news_pool/` | 고정 헤드라인 풀(128개) | 점수 열이 Day2 정답 |

만드는 순서(과정 뒤, 저장소 루트):

```bash
pip install -r requirements.txt
python tools/fetch_external.py fred           # 1) FRED 환율 캐시(네트워크는 여기서만)
python tools/generate_data.py                 # 2) 원천 세계 → data/raw/ (seed 20261014, 약 40초)
python tools/build_checkpoints.py             # 3) Day1 배포본·d2_start·데이터 사전·강사 정답
python tools/validate_data.py                 # 4) V01~V20 검사(실패 시 종료코드 1)
python tools/make_day1_charts.py              # 5) Day1 실습 가이드 차트 → docs/assets/day1/
python tools/build_day1_template.py           # 6) Day1 엑셀 템플릿·AX 캔버스·강사 정답 워크북 + 검사
python tools/build_day1_notebook.py           # 7) Challenge 노트북(위 '지금 쓸 수 있는 도구')
```

- 재현성: 같은 seed·config·라이브러리 버전이면 같은 파일 해시(`data/raw/_manifest.json`, `data/checkpoints/_manifest.json`).
- 강사 정답 출력 위치: `config.yaml`의 `outputs.answers_dir`(기본 `../instructor/day1/answers`, 공개 저장소 밖).
- 라이선스: 이 폴더의 코드는 MIT(`LICENSE`), 글꼴은 SIL OFL 1.1 — 저장소 루트의 `NOTICE.md`를 봅니다.
