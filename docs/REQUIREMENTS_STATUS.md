# SRS 이행 현황

| 요구사항 | 구현·검증 | 남은 사항 |
|---|---|---|
| 2단계 탐지·독립 모듈 | TextNormalizer, ScreeningEngine, VerificationEngine, StyleAnalyzer, Crawler, LocationResolver, ResultManager, DesktopGUI | 실제 사이트 코퍼스 보정 |
| 필수 4기법 | 자모 재조합, NFKC/혼동 문자, 계산 CSS·조상 opacity·색상, 좌표·숨김·clipping | 한정된 혼동 사전, 복잡한 CSS 한계 |
| 하위 페이지·게시판·쿼리 | 같은 출처 href 탐색, query 보존, 동시 브라우저 페이지 | 클릭/폼 전용 페이지·무한 스크롤 미지원 |
| 댓글 | 이미 렌더링된 DOM과 댓글 링크 검사 | 사용자 조작 뒤 열리는 댓글 미지원 |
| 중첩 iframe | iframe 트리 재귀 검사·고유 경로·절대 src | 상대 src 재현은 제공 resolver 필요 |
| 오탐 억제 | 홍보·공익 표현·링크·기법 점수, 공익 및 숨김 UI 음성 사례 | 일반화 검증 미완료 |
| 고유 위치 | DOM 추출 시 고유성, 출력 전 원문 일치, 테스트 재탐색 | 변경된 원격 DOM 재현 보장 불가 |
| JSON | 로컬 스키마, 날짜 형식, UTF-8, 중복 제거, 기법별 별도 항목 | 공식 스키마 및 topic 미확인 |
| GUI | 비동기 스캔·중지·통계·필터·정렬·복사·상세·내보내기 | 대규모 결과 UI 성능 시험 미실시 |
| 시간·동시성 | 공유 Chromium, worker/페이지/시간 제한, 미디어 차단 | 30분 실부하 벤치마크 미실시 |
| 접근 제한 | robots, 인증/CAPTCHA 제외, 외부 링크 탐색 제한 | 모든 형태의 차단 페이지 식별 보장 불가 |
| 테스트 | 단위·DOM·GUI·브라우저·크롤링 경계, 정답 16건 | 공모전 데이터·별도 PC 검증 미실시 |
| Windows 배포 | PyInstaller와 Chromium 동봉, CLI·GUI 검증 증거 별도 파일 | 코드 서명·별도 설치 프로그램 미제공 |
| CPU-only | 전용 GPU 요구 없음, 브라우저 GPU 비활성화 | 물리적으로 GPU 없는 별도 장비 미시험 |
| 매뉴얼·소스·버전 | BUILD.md, USER_MANUAL.md, requirements-lock.txt | 공모전 첨부 1~4 대조 필요 |
| 선택적 AI·ETC | 미구현 | 필수 범위 품질 확보 후 추가 가능 |

정량 결과와 바이너리 실행 결과의 최종 근거는 `test_evidence` 폴더를 확인해 주세요. 이 표는 공식 공모전 적합성 인증을 의미하지 않습니다.
