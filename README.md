# my-stock-team

**종목명만 던지면 애널리스트 팀이 재무·차트·뉴스·리스크를 나눠 분석하고, 디자인된 5부 PPTX/PDF 리포트까지 만들어 주는 Claude Code 플러그인입니다.**

> 산출물은 **무료 공개 데이터 기반 학습용**이며, 매수·매도 등 투자 판단의 근거로 쓸 수 없습니다.

---

## 설치

Claude Code에서 두 줄이면 끝납니다.

```
/plugin marketplace add durendal86/my-stock-team
/plugin install my-stock-team@my-stock-team
```

## 사용

종목명을 자연어로 말하면 됩니다.

```
삼성전자 분석해줘
```

그러면 펀더멘털·시장기술·뉴스심리 애널리스트가 **동시에** 분석하고, 리스크 매니저가 종합한 뒤, 5부 구성(표지·재무·차트·뉴스심리·리스크·종합) 리포트를 만들어 줍니다.

명령어로도 쓸 수 있습니다.

```
/analyze 삼성전자            # 종합 분석 → reports/삼성전자.md
/verify-report 삼성전자      # 완성 리포트 품질 점검(통과/보류)
/build-report 삼성전자 --pdf # 디자인 PPTX + PDF 생성
```

개별 질문은 알아서 담당 애널리스트에게 갑니다 — 재무 질문은 펀더멘털, 주가·추세는 시장기술, 뉴스·여론은 뉴스심리.

---

## ⚠️ 시작 전에: DART API 키는 각자 발급해 넣으세요

재무 분석은 **DART(전자공시) OpenAPI**를 씁니다. **키는 플러그인에 들어있지 않으며, 각자 본인 키를 발급해야 합니다.**

1. <https://opendart.fss.or.kr> 에서 무료로 인증키를 발급받습니다.
2. 작업 폴더에 `.env` 파일을 만들고 키를 넣습니다.

   ```
   DART_KEY=발급받은_키
   ```

> 키는 절대 깃에 올리지 마세요. (이 저장소의 `.gitignore`가 `.env`를 기본 차단합니다.)

## 그 외 필요 환경

| 항목 | 용도 | 비고 |
|---|---|---|
| Python 패키지 | 데이터 수집·리포트 | `OpenDartReader` `finance-datareader` `pykrx` `python-pptx` `pandas` `matplotlib` `pyyaml` |
| 한글 폰트 | 리포트·차트 글자 | 기본 **맑은 고딕(Windows)**. 다른 OS는 `skills/report-pptx/build.py`의 `FONT` 값을 설치된 한글 폰트로 변경 |
| LibreOffice | PDF 변환 | 없으면 PPTX까지만 생성. `winget install --id TheDocumentFoundation.LibreOffice -e --silent` |

---

## 구성

- **agents/** — 펀더멘털 · 시장기술 · 뉴스심리 · 리스크종합 · 검증, 5종 애널리스트
- **skills/** — `report-pptx`(디자인 PPTX 생성), `pdf-convert`(PDF 변환)
- **commands/** — `/analyze`, `/build-report`, `/verify-report`

## 팀이 지키는 원칙

- 모든 수치 옆에 `(출처: 데이터명, 연도/날짜)` — 출처 없는 수치는 쓰지 않습니다.
- 못 구한 값은 "확인 불가", 출처 없는 뉴스·루머는 "미확인"으로 표기합니다.
- 매수·매도·목표가 등 투자 행동은 **단정하지 않습니다.** 판단 근거 정리까지만, 최종 판단은 사람이 합니다.
