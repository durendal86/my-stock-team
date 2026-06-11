"""pdf-convert 스킬 — LibreOffice 헤드리스로 오피스 문서를 PDF로 변환한다.

사용:
    python convert.py <입력파일> [입력파일2 ...] [--outdir DIR]

- 입력: .pptx .ppt .docx .doc .xlsx .xls .odp .odt 등 LibreOffice가 여는 포맷
- 출력: 기본은 입력 파일과 같은 폴더에 같은 이름의 .pdf
- LibreOffice 미설치 시 안내 메시지를 출력하고 종료한다.
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import time
from pathlib import Path

# Windows 콘솔(cp949)에서도 안전하게 출력 (✓ 등 비ASCII 깨짐 방지)
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SOFFICE_CANDIDATES = [
    r"C:\Program Files\LibreOffice\program\soffice.exe",
    r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
]


def find_soffice() -> str | None:
    for p in SOFFICE_CANDIDATES:
        if Path(p).exists():
            return p
    return shutil.which("soffice")


def convert(files: list[Path], outdir: Path | None) -> int:
    soffice = find_soffice()
    if not soffice:
        print("LibreOffice(soffice)를 찾지 못했습니다. 설치:")
        print("  winget install --id TheDocumentFoundation.LibreOffice -e --silent")
        return 1

    failed = 0
    for f in files:
        if not f.exists():
            print(f"✗ 입력 없음: {f}")
            failed += 1
            continue
        out = (outdir or f.parent)
        out.mkdir(parents=True, exist_ok=True)
        pdf = out / (f.stem + ".pdf")
        before = pdf.stat().st_mtime if pdf.exists() else None

        # soffice는 실패해도 종료코드 0인 경우가 있어 산출물 존재/갱신으로 판정한다
        subprocess.run(
            [soffice, "--headless", "--convert-to", "pdf",
             "--outdir", str(out), str(f)],
            capture_output=True, timeout=300,
        )
        for _ in range(20):           # 비동기 마무리 대기 (최대 ~10초)
            if pdf.exists() and (before is None or pdf.stat().st_mtime > before):
                break
            time.sleep(0.5)

        if pdf.exists() and (before is None or pdf.stat().st_mtime > before):
            print(f"✓ {f.name} → {pdf} ({pdf.stat().st_size / 1024:.1f} KB)")
        else:
            print(f"✗ 변환 실패: {f.name}")
            failed += 1
    return 1 if failed else 0


def main() -> None:
    ap = argparse.ArgumentParser(description="오피스 문서 → PDF 변환 (LibreOffice 헤드리스)")
    ap.add_argument("files", nargs="+", help="변환할 파일 경로")
    ap.add_argument("--outdir", type=Path, default=None, help="출력 폴더 (기본: 입력과 동일)")
    args = ap.parse_args()
    sys.exit(convert([Path(f) for f in args.files], args.outdir))


if __name__ == "__main__":
    main()
