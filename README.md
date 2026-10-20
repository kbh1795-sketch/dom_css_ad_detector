# dom_css_ad_detector

A two-stage illegal ad detector for public-sector websites using Unicode normalization and DOM/CSS analysis, with subpage and nested iframe scanning, detection evidence, and precise element locations.

문자 정규화와 DOM/CSS 분석을 결합한 Windows 11용 공공 웹사이트 불법광고 의심 콘텐츠 탐지 도구입니다. 전용 GPU나 외부 AI API 없이 실행합니다.

## 주요 기능

- **2단계 분석:** 키워드·문자 변형·CSS 은닉 선별 후 홍보성과 공익 문맥을 검증합니다.
- **필수 4기법:** `HOMOGLYPH`, `JAMO`, `TRANSPARENT`, `OFFSCREEN`을 분리하여 출력합니다.
- **크롤링:** 동일 출처 하위 링크, 쿼리가 다른 게시글, JavaScript DOM, 중첩 iframe을 검사합니다.
- **위치 검증:** 고유 CSS 위치와 원문 일치를 확인합니다.
- **GUI:** 검사 시작·중지, 진행 현황, 결과 필터·정렬, 상세 근거와 복사를 지원합니다.
- **JSON:** 스키마 검증과 중복 제거 후 UTF-8 결과를 저장합니다.

## 빠른 시작

Windows 11 x64와 Python 3.11 이상이 필요합니다. 저장소 루트에서 실행해 주세요.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
.\.venv\Scripts\python.exe -m playwright install chromium
.\.venv\Scripts\python.exe main.py
```

`requirements-lock.txt`는 기존 Windows 검증 환경의 고정 버전입니다. 해당 Python 버전에서 설치할 수 없다면 `requirements.txt`를 사용한 뒤 테스트를 다시 실행해 주세요.

명령행 검사:

```powershell
.\.venv\Scripts\python.exe main.py --url https://example.go.kr --config config.example.json --output result.json
```

기본 결과는 `main.py`와 같은 폴더의 `result.json` 및 `scan_details.json`에 저장됩니다. 배포 실행 파일은 실행 파일과 같은 폴더에 저장합니다. 접근통제나 CAPTCHA를 우회하지 않습니다.

## 테스트와 빌드

```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\build.ps1 -Python .\.venv\Scripts\python.exe
```

빌드 결과는 `release/PublicWebAdDetector/`에 생성됩니다. 실행 파일과 `_internal` 폴더를 함께 배포해 주세요. 대용량 실행 파일·Chromium은 소스 커밋에서 제외하며, 배포 시 GitHub Releases의 첨부 파일로 관리합니다.

## 저장소 구조

```text
dom_css_ad_detector/
├── detector/                 # 수집·선별·검증·위치·JSON·GUI
├── tests/                    # 단위·브라우저·GUI 테스트와 로컬 사이트
├── docs/                     # 매뉴얼·설계·한계·검증 보고서
│   ├── images/               # 제안서용 SVG 도식
│   └── validation/           # 기존 배포본의 검증 기록
├── schemas/result.schema.json
├── main.py
├── config.example.json
├── requirements.txt
├── requirements-lock.txt
├── build.ps1
└── THIRD_PARTY_NOTICES.md
```

`test_evidence/`는 테스트 실행 시 생성되는 로컬 결과이며 Git에서 제외합니다. `docs/validation/`은 기존 검증 기록으로, 새 테스트 실행 결과와 구분합니다.

## 문서

- [사용자 설명서](docs/USER_MANUAL.md)
- [설치·빌드·테스트](docs/BUILD.md)
- [요구사항 명세](docs/SRS.md)
- [요구사항 이행 현황](docs/REQUIREMENTS_STATUS.md)
- [기존 실행 검증 보고서](docs/TEST_REPORT.md)
- [알려진 한계](docs/KNOWN_LIMITATIONS.md)
- [GitHub 업로드 안내](docs/GITHUB.md)
- [제삼자 라이선스 고지](THIRD_PARTY_NOTICES.md)

## 검증 범위

기존 Windows 11 검증에서 자동 테스트 12개를 통과했으며, 자체 정답 16건에 대해 TP 16 / FP 0 / FN 0을 확인했습니다. 이는 제한된 로컬 데이터의 결과이며 실제 공공 웹사이트의 성능을 보장하지 않습니다. 공식 공모전 스키마와 `topic`의 최종 적합성은 별도 확인이 필요합니다.

클릭 전용 댓글, 무한 스크롤, 이미지 OCR, Shadow DOM과 복잡한 CSS 은닉은 현재 검사 범위에 제한이 있습니다. 상세 내용은 알려진 한계 문서를 확인해 주세요.

## 라이선스

프로젝트 소스는 [MIT License](LICENSE)를 따릅니다. 사용하는 라이브러리와 배포본에 포함되는 구성요소는 각 프로젝트의 라이선스를 따르며, 자세한 내용은 [제삼자 라이선스 고지](THIRD_PARTY_NOTICES.md)를 확인해 주세요.
