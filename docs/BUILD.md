# 설치·빌드·검증

Windows 11 x64, Python 3.11 이상을 사용해 주세요. 실제 빌드는 Python 3.12.14에서 수행했습니다.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
.\.venv\Scripts\python.exe -m playwright install chromium
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe main.py
```

`requirements-lock.txt`는 이번 검증 환경의 정확한 버전입니다. 다른 Python 버전에서 해당 wheel이 없으면 `requirements.txt`의 범위로 설치한 후 테스트를 다시 실행해 주세요.

## 실행 파일

```powershell
.\build.ps1 -Python .\.venv\Scripts\python.exe
```

`release/PublicWebAdDetector` 폴더 전체가 배포물입니다. 실행 파일 단독 복사는 지원하지 않습니다. Chromium을 포함하므로 빌드와 배포에 수백 MB가 필요합니다. PyInstaller는 현재 운영체제용으로 빌드하므로 Windows에서 실행해 주세요. PowerShell 정책이 스크립트 실행을 제한하면 조직의 승인된 정책과 실행 절차를 따라 주세요.

기존 브라우저 설치를 재사용하려면 `-BrowserPath`에 해당 Playwright 브라우저 디렉터리를 지정하실 수 있습니다. `-DistPath`, `-WorkPath`도 지정 가능합니다.

빌드 마지막에는 Qt의 ICU import/export를 검사합니다. 빌드 환경의 별도 ICU DLL이 잘못 수집되어 Windows 기본 ICU를 가리는 경우, 시스템 DLL이 필요한 심볼을 제공하는지 확인한 뒤 충돌 DLL만 배포 폴더에서 제외합니다. 현재 Windows 11 환경에서 이 처리가 필요했고, 이후 동봉된 실행 파일의 CLI와 GUI 시작을 모두 검증했습니다.

## 테스트 서버와 검증

```powershell
.\.venv\Scripts\python.exe -m tests.server
# 다른 터미널에서
.\release\PublicWebAdDetector\PublicWebAdDetector.exe --url http://127.0.0.1:8765/ --output .\test-result.json
```

`tests/ground_truth.json`은 URL·DOM 위치·기법 16개 정답입니다. 통합 테스트는 임의 포트에서 서버를 시작해 필수 4기법, 복합 기법, 동적 삽입, 공익 안내, 숨김 메뉴, 중첩 iframe, 게시판 쿼리, 빈 결과, 중지 저장을 검증합니다. 브라우저에서 출력 위치를 다시 해석해 각 요소의 원문까지 비교합니다. GUI 테스트는 실제 Qt 이벤트 루프에서 시작 버튼, 결과 수, 필터, 선택·복사, 문맥 표시, 저장을 검증합니다.

평가식은 precision=TP/(TP+FP), recall=TP/(TP+FN)입니다. 1차 선별 재현율은 정답의 `(URL, 위치)`가 후보로 유지된 비율로 계산하며, 한 요소의 복수 정답 기법도 정답 행별로 집계합니다. `test_evidence/metrics.json`의 실행 시간은 실제 브라우저 검사 구간이며 테스트 전체 시간과 다릅니다.

## 제출 전 확인

공식 PDF 첨부 1~4를 확보하여 `topic`, 제출 파일명·기법 코드·스키마, 평가 URL 처리 규칙을 대조해야 합니다. 독립 Windows 11 PC에서 압축을 풀어 네트워크 조건과 파일 쓰기 권한을 확인하고 실제 평가 데이터로 성능을 다시 측정해 주세요. 필수 기능 검증 전에 AI나 추가 ETC 기법은 구현하지 않았습니다.
