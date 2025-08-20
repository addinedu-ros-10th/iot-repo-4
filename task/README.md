# FastAPI 프로젝트 구축 요구사항 체크리스트

## 📋 프로젝트 개요
독거노인 통합 돌봄 서비스 백엔드 시스템을 위한 Docker Compose 기반 FastAPI 프로젝트 구축

## ✅ 주요 요구사항 체크리스트

### 1. Docker Compose 기반 환경 관리
- [ ] `docker-compose.yml` (local 환경)
- [ ] `docker-compose.dev.yml` (개발 환경)
- [ ] `docker-compose.prod.yml` (운영 환경)
- [ ] `.env` 환경 변수 파일 구성
- [ ] `.gitignore`에 `.env` 파일 추가

### 2. 웹 서버 및 SSL 설정
- [ ] Caddy 웹 서버 설정
- [ ] Let's Encrypt SSL 자동 적용
- [ ] Caddyfile 구성 (리버스 프록시)
- [ ] Docker 네트워크 연결 설정

### 3. 아키텍처 및 의존성 관리
- [ ] 클린 아키텍처 적용 (domain, use_cases, interfaces 레이어)
- [ ] 의존성 역전 원칙 구현
- [ ] FastAPI Depends를 활용한 의존성 주입
- [ ] 레이어별 명확한 분리

### 4. 데이터베이스 및 ORM
- [ ] SQLAlchemy + Alembic ORM 설정
- [ ] 환경별 DB 접속 정보 구성
  - [ ] Local: localhost:15432/iot_care
  - [ ] Prod: ec2-52-79-78-247.ap-northeast-2.compute.amazonaws.com:5432/iot_care
- [ ] `alembic upgrade head` 자동 실행
- [ ] `alembic stamp head` 최초 기동 시 적용

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
- [ ] TDD 방식 적용
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
- [ ] Docker Volume을 통한 로그 저장

### 11. .gitignore 구성
- [ ] `.env` 파일
- [ ] 가상 환경 폴더 (`.venv`, `venv`)
- [ ] 파이썬 컴파일 파일 (`__pycache__`, `*.pyc`)
- [ ] Alembic 생성 파일 관리
- [ ] 테스트 및 빌드 결과물 (`.pytest_cache`, `dist`, `build`)
- [ ] 로깅 파일 (`logs/`)

## 🚀 구현 우선순위

### Phase 1: 기본 인프라
1. Docker Compose 환경 구성
2. FastAPI 기본 구조 설정
3. 데이터베이스 연결 및 ORM 설정

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

## 📁 예상 프로젝트 구조
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

## 🔍 검증 포인트
- [ ] 로컬 환경에서 정상 동작
- [ ] Docker 컨테이너 정상 실행
- [ ] 데이터베이스 연결 성공
- [ ] API 엔드포인트 정상 응답
- [ ] SSL 인증서 정상 적용
- [ ] 테스트 코드 정상 실행
- [ ] 문서 자동 생성 확인

