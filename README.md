# my-stock-team

역할별 애널리스트 서브에이전트와 리포트 생성 스킬을 묶은 **대형주 리서치 팀** Claude Code 플러그인입니다.
종목명을 주면 여러 애널리스트가 협업해 분석하고, 디자인된 5부 PPTX/PDF 리포트를 만듭니다.

> 본 플러그인의 산출물은 **무료 공개 데이터 기반 학습용**입니다. 매수·매도 등 투자 판단의 근거로 사용할 수 없습니다.

## 구성

```
my-stock-team/
├── .claude-plugin/
│   ├── plugin.json         # 플러그인 매니페스트 (name, version 1.0.0)
│   └── marketplace.json    # 설치 카탈로그
├── agents/                 # 서브에이전트 5종
│   ├── fundamental-analyst.md       # 재무·실적·공시 (DART)
│   ├── market-tech-analyst.md       # 가격·추세·거래량 (FinanceDataReader)
│   ├── news-sentiment-analyst.md    # 뉴스·이슈·심리 (WebSearch)
│   ├── risk-manager-synthesizer.md  # 리스크·종합 (+ pykrx 시총·거래대금)
│   └── verification-analyst.md      # 완성 리포트 품질 점검 (통과/보류)
├── skills/
│   ├── report-pptx/        # reports/{종목}.md → 디자인 PPTX
│   └── pdf-convert/        # 오피스 문서 → PDF (LibreOffice 헤드리스)
└── commands/
    ├── analyze.md          # /analyze — 종합 분석 파이프라인
    ├── build-report.md     # /build-report — PPTX(+PDF) 생성
    └── verify-report.md    # /verify-report — 품질 점검
```

## 설치

로컬 마켓플레이스로 추가한 뒤 설치합니다.

```
/plugin marketplace add /path/to/my-stock-team
/plugin install my-stock-team@my-stock-team-marketplace
```

(또는 이 폴더를 git 저장소로 올리고 `/plugin marketplace add <owner>/<repo>` 로 공유)

## 사용

```
/analyze 삼성전자            # 3인 병렬 분석 → 리스크 종합 → reports/삼성전자.md → 검증 → 리포트
/verify-report 삼성전자      # 완성 리포트 품질 점검 (통과/보류)
/build-report 삼성전자 --pdf # 디자인 PPTX + PDF 생성
```

개별 질문은 라우팅 규칙에 따라 담당 에이전트가 처리합니다(재무→펀더멘털, 가격→시장기술, 뉴스→뉴스심리).

## 필요 환경

- **Python 패키지**: `OpenDartReader`, `finance-datareader`, `pykrx`, `python-pptx`, `pandas`, `matplotlib`, `pyyaml`
- **DART API 키**: 펀더멘털 애널리스트는 환경변수 `DART_KEY`를 읽습니다. **플러그인에는 키가 포함되어 있지 않습니다** — 각자 `.env` 또는 환경변수로 설정하세요. (DART OpenAPI에서 무료 발급)
- **한글 폰트**: 리포트/차트는 **맑은 고딕(Malgun Gothic, Windows 기준)** 을 사용합니다. 다른 OS에서는 설치된 한글 폰트명에 맞게 `skills/report-pptx/build.py`의 `FONT` 값을 조정하세요.
- **PDF 변환**: LibreOffice가 필요합니다(`winget install --id TheDocumentFoundation.LibreOffice -e --silent` 또는 OS별 설치). 없으면 PPTX까지만 생성됩니다.

## 가드레일 (전 산출물 공통)

- 모든 수치 옆 `(출처: 데이터명, 연도/날짜)` — 출처 없는 수치 금지
- 못 구한 값은 "확인 불가", 출처 없는 뉴스·루머는 "미확인"
- 매수·매도·보유·목표가·비중 조정 등 투자 행동 단정 금지 (의사결정 지원까지만, 최종 판단은 사람)
- 리포트 첫머리 학습용 고지 + 끝에 데이터 출처·기준일 목록
