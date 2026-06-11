---
description: reports/{종목}.md → 디자인 PPTX(+선택 PDF). report-pptx 스킬 호출
argument-hint: [종목명] [--pdf]
---

`reports/$1.md`를 읽어 디자인된 PPTX 리포트를 만듭니다. 입력 파일이 없으면 경로를 확인하거나 먼저 `/analyze $1`로 리포트를 작성합니다.

## 실행

`--pdf` 인자가 있으면 PDF까지 함께 생성합니다.

```bash
python "${CLAUDE_PLUGIN_ROOT}/skills/report-pptx/build.py" "reports/$1.md" $2
```

- 출력: `reports/$1.pptx` (+ `--pdf` 시 `reports/$1.pdf`)
- 슬라이드 순서(고정): 표지 → 종목 개요 → 재무 요약(표·최근 3개년) → 가격/추세(차트) → 뉴스·심리 → 리스크 → 한 줄 종합
- 디자인: KB 옐로우(#FFBC00) 포인트 + 그레이/화이트, 맑은 고딕 고정(한글 깨짐 방지)
- PDF 변환은 `pdf-convert` 스킬(LibreOffice 헤드리스)을 내부 호출합니다. LibreOffice가 없으면 스킬이 설치 명령을 안내합니다.

실행 후 생성된 파일 경로와 슬라이드 수를 운용역에게 보고합니다. 표가 잘리거나 한글이 깨지면 원인을 점검합니다.

## 가드레일

수치 옆 출처·기준일, 매수·매도 단정 금지, 학습용 고지는 입력 .md와 스킬에서 보장됩니다. 빌드 로그에 가드레일 경고가 뜨면 해당 표현을 .md에서 고친 뒤 다시 빌드합니다.
