# 실행 검증 보고서

기존 배포본 검증 기록입니다. 새 테스트 실행 결과는 저장소 루트의 `test_evidence/`에 생성됩니다.

검증일: 2026-10-20 (Australia/Sydney)

| 항목 | 관찰 결과 |
|---|---|
| 운영체제 | Windows 11 Home x64, 10.0.26200 |
| Python | 3.12.14 |
| 자동 테스트 | 12개 통과, 최종 로그는 validation/pytest.txt |
| 정답 세트 | 직접 구성한 4개 페이지, 필수 기법 결과 16건 |
| TP / FP / FN | 16 / 0 / 0 |
| 최종 정밀도 / 재현율 | 100% / 100% |
| 1차 선별 재현율 | 100% |
| 소스 검사 실행 시간 | validation/metrics.json의 elapsed_sec |
| 배포본 검사 실행 시간 | 6.406초 (현재 최종 smoke 실행) |
| 배포본 CLI / GUI 시작 종료 코드 | 0 / 0 |
| 배포본 정답 일치 | 16개 위치·URL·기법 모두 일치 |
| 배포본 외부 경로 환경변수 | PLAYWRIGHT_BROWSERS_PATH, PYTHONPATH, PYTHONHOME, VIRTUAL_ENV를 제거하고 실행 |
| 전용 GPU 의존 | 없음. Chromium은 --disable-gpu로 실행 |

원시 근거: `validation/metrics.json`, `pytest.txt`, `packaged_smoke.json`, `packaged_result.json`.

DOM 테스트는 조상 clipping, 큰 양수 좌표, 정상 긴 본문, 동일 src의 복수 iframe 경로도 검사합니다. 경계 테스트는 robots 제한, 인증 화면, 404, 동일 출처 리디렉션, 외부 출처 탐색 제외, 시간 초과 저장을 검사합니다. GUI 기능은 소스 실행의 실제 Qt 이벤트 루프에서 검사하며 배포본에서는 창 생성·정상 종료를 별도로 검사했습니다.

빌드 도중 Windows 경로 길이와 ICU DLL 충돌을 발견했습니다. 전체 Chromium 헤드리스 배포와 필요한 심볼 검사 후 Windows 기본 ICU 사용으로 수정했습니다. 실패 중간 산출물을 제출용으로 간주하지 않았으며 최종 smoke 결과는 수정 후 실행 결과입니다.

이는 자체 테스트의 재현 가능한 실행 결과입니다. 공모전 원본 PDF, 공식 스키마, 숨겨진 평가 데이터, 별도 깨끗한 Windows PC, 물리적으로 GPU가 없는 별도 장비와 30분 대규모 부하 조건은 검증하지 않았습니다. 따라서 공모전 제출 적합성 확정과 전체 Definition of Done 달성을 주장하지 않습니다.
