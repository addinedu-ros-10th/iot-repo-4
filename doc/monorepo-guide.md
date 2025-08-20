# 📚 모노레포(Monorepo) 개발 형상 관리 가이드

이 문서는 독거노인 등 1인 가구 취약계층 통합 돌봄 서비스를 위한 **모노레포(Monorepo) 기반 개발 형상 관리 가이드**입니다. 모든 개발자는 프로젝트의 효율적인 협업과 관리를 위해 아래 지침을 반드시 준수해야 합니다.

## 1. 프로젝트 구조

본 리포지토리는 여러 개의 개별 프로젝트를 포함하는 모노레포 구조로 되어 있습니다. 각 프로젝트는 기능과 역할에 따라 다음과 같은 폴더에 위치합니다.

* `apps/user-app`: 사용자 모바일/웹 애플리케이션
* `apps/pyqt-admin-service`: PyQt 기반 관제 서비스
* `services/was-server`: WAS (Web Application Server)
* `services/que-alert-server`: QUE & ALERT 서버
* `iot-device`: IOT 디바이스 관련 코드 및 펌웨어 (아두이노)

## 2. Git 워크플로

모든 작업은 Git을 통해 이루어지며, 다음 워크플로를 따릅니다.

### 2.1 브랜치 생성 및 전환

새로운 기능 개발이나 버그 수정 시 `main` 브랜치에서 작업용 브랜치를 생성합니다.

**예시**:
```bash
git checkout -b feature/your-feature-name
```

**브랜치 명명 규칙**:
- `feature/기능명`: 새로운 기능 개발
- `fix/버그명`: 버그 수정
- `docs/문서명`: 문서 수정
- `refactor/리팩토링명`: 코드 리팩토링

### 2.2 작업 및 변경 사항 추가

자신이 맡은 프로젝트 폴더(`apps/user-app`, `services/was-server` 등) 내에서만 코드를 수정합니다.

작업이 완료되면, **자신의 프로젝트 폴더의 변경 사항만** Staging Area에 추가합니다.

**예시**: IOT 디바이스(아두이노) 펌웨어 업데이트
```bash
# 아두이노 펌웨어 코드 수정 후, 해당 폴더의 변경 사항만 추가
git add iot-device/arduino/
```

**예시**: PyQt 관제 서비스 기능 추가
```bash
# PyQt 관제 서비스 코드 수정 후, 해당 폴더의 변경 사항만 추가
git add apps/pyqt-admin-service/
```

### 2.3 커밋 (Commit)

변경 사항을 커밋할 때는 아래 커밋 메시지 규칙을 준수합니다.

**형식**: `[타입]: [프로젝트명] [설명]`

**예시**:
```bash
git commit -m "feat: [IOT-Device] 센서 데이터 전송 주기 단축"
git commit -m "fix: [PyQt-Admin] 배터리 잔량 표시 버그 수정"
git commit -m "docs: [README] 프로젝트 구조 업데이트"
```

**타입**:
- `feat`: 새로운 기능 추가
- `fix`: 버그 수정
- `docs`: 문서 수정
- `refactor`: 코드 리팩토링
- `chore`: 빌드, 라이브러리 업데이트 등
- `test`: 테스트 코드 추가/수정

### 2.4 푸시 (Push)

로컬에서 작업한 커밋을 원격 리포지토리로 전송합니다.

**예시**:
```bash
git push origin feature/your-feature-name
```

### 2.5 풀 리퀘스트 (Pull Request) 및 병합 (Merge)

푸시 후 GitHub에서 Pull Request를 생성하여 코드 리뷰를 요청합니다.

**Pull Request 작성 시 포함할 내용**:
- 제목: 간결하고 명확한 설명
- 설명: 변경 사항의 상세한 설명
- 관련 이슈 번호 (있는 경우)
- 테스트 방법 및 결과
- 스크린샷 (UI 변경 시)

리뷰가 완료되면 `main` 브랜치에 병합(Merge)합니다.

## 3. 유의사항

### 3.1 부분적 푸시/풀 불가

Git은 전체 리포지토리 단위로 동작합니다. 따라서 특정 폴더만 푸시하거나 풀하는 기능은 지원하지 않습니다. `git pull`을 실행하면 모든 개발자의 최신 변경 사항이 로컬에 반영됩니다.

**예시**:
```bash
# 최신 변경 사항을 모두 가져옴
git pull
```

### 3.2 파일 충돌 (Conflict)

`git pull` 시 충돌이 발생하면, 본인이 맡은 파일의 충돌만 해결하고 다른 파일에는 영향을 주지 않도록 주의합니다.

**충돌 해결 방법**:
1. 충돌이 발생한 파일 확인: `git status`
2. 충돌 부분 수정
3. 수정된 파일을 Staging Area에 추가: `git add <파일명>`
4. 충돌 해결 완료 후 커밋: `git commit`

### 3.3 독립적 작업

각 개발자는 자신이 맡은 프로젝트 폴더 내에서만 작업해야 하며, 다른 프로젝트의 파일을 임의로 수정/삭제해서는 안 됩니다.

**권장사항**:
- 작업 전 `git pull`로 최신 상태 유지
- 자신의 프로젝트 폴더 외부 파일은 읽기 전용으로 취급
- 다른 프로젝트와의 의존성이 있는 경우 사전 협의

## 4. 모노레포의 장점

1. **코드 공유**: 공통 라이브러리와 유틸리티를 쉽게 공유
2. **일관성**: 모든 프로젝트에서 동일한 코딩 스타일과 도구 사용
3. **의존성 관리**: 프로젝트 간 의존성을 중앙에서 관리
4. **리팩토링**: 전체 코드베이스에 걸친 대규모 리팩토링 가능
5. **협업**: 팀 전체의 코드 변경사항을 한 곳에서 추적

## 5. 문제 해결

### 5.1 자주 발생하는 문제

**Q: 다른 개발자의 변경사항이 제 작업에 영향을 주나요?**
A: `git pull`로 최신 변경사항을 가져온 후 작업을 시작하면 충돌을 최소화할 수 있습니다.

**Q: 실수로 다른 프로젝트 파일을 수정했어요.**
A: `git checkout -- <파일경로>`로 해당 파일을 원래 상태로 되돌릴 수 있습니다.

**Q: 커밋 메시지를 잘못 작성했어요.**
A: `git commit --amend`로 마지막 커밋 메시지를 수정할 수 있습니다.

### 5.2 유용한 Git 명령어

```bash
# 현재 상태 확인
git status

# 변경사항 확인
git diff

# 브랜치 목록 확인
git branch -a

# 원격 저장소 정보 확인
git remote -v

# 커밋 히스토리 확인
git log --oneline

# 특정 파일의 변경 이력 확인
git log --follow <파일명>
```

## 6. 추가 리소스

- [Git 공식 문서](https://git-scm.com/doc)
- [GitHub Flow 가이드](https://guides.github.com/introduction/flow/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [모노레포 모범 사례](https://monorepo.tools/)
