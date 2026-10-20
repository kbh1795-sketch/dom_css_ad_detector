# GitHub 업로드 안내

업로드할 소스 루트는 `dom_css_ad_detector` 폴더입니다. 바깥 작업 폴더의 `work/`, `outputs/`, 배포 ZIP 전체를 저장소로 올리지 마세요.

이 폴더에는 Git 이력이나 원격 주소를 새로 설정하지 않았습니다. GitHub에 만든 저장소를 clone한 뒤, 이 폴더의 내용을 복사하면 됩니다. clone한 폴더의 `.git/`과 기존 `LICENSE`는 유지해 주세요. README와 같은 이름의 파일을 이미 작성했다면 복사 전에 차이를 확인해 주세요.

소스와 테스트, 문서 및 기존 검증 기록을 커밋합니다. 실행 파일, Chromium, 가상환경, 캐시, 새 검사 결과와 환경변수 파일은 `.gitignore`로 제외합니다. 대용량 배포 ZIP은 GitHub Releases에 별도로 첨부합니다.

커밋 전에는 저장소 루트에서 `git status --short`와 `git diff --cached --stat`를 확인해 주세요. GitHub의 LICENSE 선택은 해당 프로젝트 소스에 대한 선택이며, 제삼자 라이브러리 고지를 대체하지 않습니다.
