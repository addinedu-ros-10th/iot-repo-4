# FastAPI 프로젝트 구축 체크리스트 (수정됨)

## 📋 프로젝트 개요
독거노인 통합 돌봄 서비스 백엔드 시스템을 위한 Docker Compose 기반 FastAPI 프로젝트 구축

## ✅ 주요 요구사항 체크리스트

### 1. Docker Compose 기반 환경 관리
- [x] `docker-compose.yml` (local 환경)
- [x] `docker-compose.dev.yml` (개발 환경)
- [x] `docker-compose.prod.yml` (운영 환경)
- [x] 환경별 env 파일 구성 (env.local, env.dev, env.prod)
- [x] 모노레포 루트 .gitignore 사용 (개별 .gitignore 제거)
- [x] **PostgreSQL DB 컨테이너 제거** (외부 DB 서버 직접 연결)
- [x] **Redis 컨테이너 유지** (캐시, 세션, 태스크 큐)

### 2. 웹 서버 및 SSL 설정
- [ ] Caddy 웹 서버 설정
- [ ] Let's Encrypt SSL 자동 적용
- [ ] Caddyfile 구성 (리버스 프록시)
- [ ] Docker 네트워크 연결 설정

### 3. 아키텍처 및 의존성 관리
- [x] 클린 아키텍처 레이어 구조 생성 (domain, use_cases, interfaces, infrastructure, api, core)
- [x] 모노레포 구조 준수 및 작업 경로 규칙 수립
- [x] 각 레이어별 __init__.py 파일 생성 완료
- [ ] 의존성 역전 원칙 구현
- [ ] FastAPI Depends를 활용한 의존성 주입
- [ ] 레이어별 명확한 분리

### 4. 데이터베이스 및 ORM
- [x] **Alembic 설정** (alembic.ini, env.py, script.py.mako)
- [x] **Core 설정 모듈** (app/core/config.py)
- [x] **SQLAlchemy 데이터베이스 연결 모듈** 생성
- [x] **Redis 클라이언트 모듈** 생성
- [x] **Visual C++ Build Tools 설치** (Windows psycopg2 빌드 지원)
- [x] **가상환경 생성** (.venv 폴더)
- [x] **패키지 설치 스크립트 생성** (자동화된 설치)
- [ ] **패키지 설치 완료** (Python 의존성 패키지들)
- [ ] **기존 DB 스키마 분석** 및 안전한 초기화
- [ ] **PostgreSQL 외부 DB 서버 직접 연결** (컨테이너 없음)
- [ ] **Redis 컨테이너 연결** (캐시, 세션, 태스크 큐)
- [ ] 환경별 DB 접속 정보 구성
  - [ ] Local: localhost:15432/iot_care
  - [ ] Prod: ec2-52-79-78-247.ap-northeast-2.compute.amazonaws.com:5432/iot_care
- [ ] **`alembic stamp head`** 기존 테이블 보존 (안전한 초기화)
- [ ] `alembic upgrade head` 자동 실행

### 5. 데이터 모델 및 유효성 검사
- [ ] Pydantic 모델 정의 (API 요청/응답)
- [ ] SQLAlchemy 모델과 분리
- [ ] 데이터 유효성 검사 구현

### 6. 태스크 스케줄 관리
- [ ] APScheduler 라이브러리 적용
- [ ] 주기적 데이터 수집 기능
- [ ] 알림 전송 기능
- [ ] 스케줄 관리 인터페이스

### 7. 테스트 및 자동화
- [ ] **TDD 방식 적용** (서버 구축 시에도)
- [ ] pytest + httpx 테스트 환경
- [ ] pytest-html 플러그인 적용
- [ ] 테스트 결과 HTML 자동 생성
- [ ] 단위 테스트 및 통합 테스트 코드

### 8. API 및 프로젝트 문서화
- [ ] FastAPI Swagger UI 활성화
- [ ] ReDoc 활성화
- [ ] `docs/` 경로 하위 문서화
  - [ ] 프로젝트 아키텍처 다이어그램
  - [ ] 의존성 관리 가이드
  - [ ] ORM 가이드 (SQLAlchemy + Alembic)
  - [ ] 테스트 보고서
  - [ ] API 명세서
  - [ ] 환경 변수 가이드

### 9. 모노레포 및 프로젝트 역할
- [ ] `services/was-server` 폴더 내 위치
- [ ] WAS 서버 개발에 초점
- [ ] 모노레포 구조 반영

### 10. 로깅 및 모니터링
- [ ] logging 모듈 설정
- [ ] 요청/응답 로깅
- [ ] 에러 로깅
- [ ] 주요 이벤트 로깅
- [ ] 파일/콘솔 로깅 핸들러
- [ ] **Docker Volume을 통한 로그 영구 저장**

### 11. .gitignore 구성
- [ ] `.env` 파일
- [ ] 가상 환경 폴더 (`.venv`, `venv`)
- [ ] 파이썬 컴파일 파일 (`__pycache__`, `*.pyc`)
- [ ] Alembic 생성 파일 관리
- [ ] 테스트 및 빌드 결과물 (`.pytest_cache`, `dist`, `build`)
- [ ] 로깅 파일 (`logs/`)

### 12. **피드백 반영사항**
- [ ] **작업 완료 체크 및 일시 중지** 구현
- [ ] **DB 컨테이너 제거** 완료
- [ ] **컨테이너 데이터 영구성 보장** 적용
- [ ] **요구사항 기록 및 관리** 시스템 구축
- [ ] **Context 길이 부족 극복 방안** 개선 적용

## 🚀 구현 우선순위 (수정됨)

### Phase 1: 기본 인프라
1. **Docker Compose 환경 구성 (DB 컨테이너 제외)** ✅ **완료**
2. **FastAPI 기본 구조 설정** ✅ **완료**
3. **외부 DB 연결 및 ORM 설정** ⏳ **다음 작업**

### Phase 2: 핵심 기능
1. 클린 아키텍처 구현
2. 의존성 주입 시스템
3. 기본 API 엔드포인트

### Phase 3: 고급 기능
1. 태스크 스케줄러
2. 로깅 시스템
3. 테스트 환경 구축

### Phase 4: 문서화 및 최적화
1. API 문서 생성
2. 개발 가이드 작성
3. 성능 최적화

## 📁 수정된 프로젝트 구조
```
services/was-server/
├── app/
│   ├── domain/
│   ├── use_cases/
│   ├── interfaces/
│   ├── infrastructure/
│   └── main.py
├── alembic/
├── tests/
├── docker/
├── docs/
├── docker-compose.yml
├── docker-compose.dev.yml
├── docker-compose.prod.yml
├── .env
├── requirements.txt
└── README.md
```

**참고**: PostgreSQL은 외부 서버에 직접 연결, Redis는 컨테이너로 관리

## 🔍 검증 포인트
- [ ] 로컬 환경에서 정상 동작
- [ ] Docker 컨테이너 정상 실행 (PostgreSQL 제외, Redis 포함)
- [ ] **PostgreSQL 외부 데이터베이스 연결 성공**
- [ ] **Redis 컨테이너 연결 성공**
- [ ] API 엔드포인트 정상 응답
- [ ] SSL 인증서 정상 적용
- [ ] 테스트 코드 정상 실행
- [ ] 문서 자동 생성 확인
- [ ] **컨테이너 데이터 영구성 확인**
