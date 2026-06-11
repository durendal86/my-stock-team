---
name: pdf-convert
description: >
  PPTX·DOCX·XLSX 등 오피스 문서를 LibreOffice 헤드리스로 PDF로 변환한다.
  사용자가 "PDF로 변환해줘/뽑아줘/저장해줘"라고 하면 사용한다.
  예: "reports/삼성전자.pptx PDF로 변환해줘", "리서치 합본 PDF로 저장해줘".
---

# pdf-convert

오피스 문서(.pptx .docx .xlsx .odp 등)를 **PDF로 변환**한다. 변환 엔진은 LibreOffice 헤드리스.

## 실행 방법

```bash
python .claude/skills/pdf-convert/convert.py <입력파일> [입력파일2 ...] [--outdir DIR]
```

- 출력 기본값: 입력 파일과 **같은 폴더**, 같은 이름의 `.pdf`
- 여러 파일을 한 번에 넘길 수 있다 (배치 변환)
- 한글 파일명 그대로 지원

## 동작 규칙

1. 변환 전 입력 파일 존재를 확인하고, 변환 후 **PDF 생성/갱신 여부로 성공을 판정**한다
   (soffice는 실패해도 종료코드 0인 경우가 있어 산출물 기준으로 검증).
2. 성공 시 `✓ 파일명 → 경로 (크기)`, 실패 시 `✗`를 출력한다 — 결과를 사용자에게 그대로 전달한다.
3. LibreOffice가 없으면 설치 명령을 안내한다:
   `winget install --id TheDocumentFoundation.LibreOffice -e --silent`
   (설치는 시스템 변경이므로 사용자 동의 후 진행한다.)

## 연계

- `report-pptx` 스킬은 `--pdf` 플래그로 이 변환을 내장 호출한다:
  `python .claude/skills/report-pptx/build.py reports/{종목명}.md --pdf`
- 합본 스크립트(`scripts/combine_reports.py`) 산출물도 이 스킬로 변환하면 된다.
