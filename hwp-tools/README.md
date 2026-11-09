# HWP tools

`python-hwpx` 6.11.0 기반 한글 문서 생성·변환 유틸리티.

## 지원 기능

- `.hwpx` → `.hwp` 변환
- `.hwp` → `.hwpx` 변환
- UTF-8 일반 텍스트(`.txt`) → `.hwp` 또는 `.hwpx` 생성
- 저장 뒤 확장자와 실제 컨테이너 형식 비교, 문서 재열기, 본문 텍스트 일치 검사

## 설치

Python 3.10 이상 필요. 한컴오피스 설치는 필요하지 않음.

```bash
python -m pip install -r requirements.txt
```

## 실행

```bash
python hwp_tools.py convert report.hwpx report.hwp
python hwp_tools.py convert report.hwp report.hwpx
python hwp_tools.py create notes.txt notes.hwp
python hwp_tools.py create notes.txt notes.hwpx
```

새 문서 생성은 TXT의 각 줄을 한 문단으로 추가함. 복잡한 서식의 보고서는 먼저 HWPX로 작성하고 HWP로 변환하는 것을 권장함.

## 검증

- 2026-11-09, Python 환경에 `python-hwpx==6.11.0` 설치
- 기존 한국어 보고서 HWPX(38문단) → HWP → HWPX: 파일 생성·재열기·본문 일치 통과
- 새 텍스트 문서 → HWP/HWPX: 파일 생성·재열기 통과
- HWP: OLE/Compound File 서명 `D0 CF 11 E0 A1 B1 1A E1` 확인
- HWPX: ZIP 서명 확인

## 제한 사항

- 내용 검증은 텍스트 기준. 표·도형·각주·글꼴·쪽 배치의 완전 보존을 보장하지 않음.
- 한컴오피스 데스크톱에서 시각적 렌더링 검증은 별도로 진행해야 함.
- DOC/DOCX/PDF를 이 도구에서 직접 변환하지 않음.
- 복잡한 원본은 `fallback="error"` 정책 때문에 변환이 실패할 수 있음. 실패 시 입력 파일은 변경되지 않음.

## 출처

- [python-hwpx 6.11.0 (PyPI)](https://pypi.org/project/python-hwpx/6.11.0/)
- [python-hwpx (GitHub)](https://github.com/airmang/python-hwpx)

패키지 자체와 샘플 수행평가 문서는 이 저장소에 포함하지 않음.
