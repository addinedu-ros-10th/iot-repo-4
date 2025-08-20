# FastAPI 프로젝트 구축 요구사항 요약 및 관리

## 📋 **원본 요구사항 (사용자 최초 요청)**

### 1. Docker Compose 기반 환경 관리
- `local`, `dev`, `prod` 환경을 분리하여 Docker Compose로 관리
- `.env` 파일을 활용한 환경 변수 관리
- `.gitignore`에 `.env` 파일 추가

### 2. 웹 서버 및 SSL 설정
- Caddy를 웹 서버로 사용하여 Let's Encrypt SSL 자동 적용
- Docker Compose에서 Caddy 컨테이너와 FastAPI 컨테이너를 네트워크로 연결
- Caddyfile을 통해 리버스 프록시 및 자동 SSL 설정

### 3. 아키텍처 및 의존성 관리
- 최신 클린 아키텍처 적용
- 의존성 역전 및 의존성 주입(DI) 구현
- 프로젝트를 `domain`, `use_cases`, `interfaces` 등 레이어별로 명확하게 분리
- FastAPI의 `Depends` 기능을 활용하여 의존성 주입 구현

### 4. 데이터베이스 및 ORM
- SQLAlchemy + Alembic 조합을 사용해 ORM 관리
- **로컬 DB**: `host=localhost`, `port=15432`, `dbname=iot_care`, `user=svc_dev`, `password=IOT_dev_123!@#`
- **운영 DB**: `host=ec2-52-79-78-247.ap-northeast-2.compute.amazonaws.com`, `port=5432`, `dbname=iot_care`, `user=svc_app`, `password=IOT_was_123!@#`
- Docker Compose 스크립트에 `alembic upgrade head` 명령어 포함
- **최초 기동 시 데이터 유실 방지**를 위해 `alembic stamp head` 사용

### 5. 데이터 모델 및 유효성 검사
- Pydantic 모델을 API 요청/응답의 유효성 검사에 사용
- SQLAlchemy 모델과 별개로 Pydantic 모델을 정의하여 API의 데이터 스키마를 명확하게 분리

### 6. 태스크 스케줄 관리
- APScheduler와 같은 라이브러리를 사용해 주기적인 데이터 수집, 알림 전송 등의 태스크를 관리

### 7. 테스트 및 자동화
- TDD(Test-Driven Development) 방식을 적용
- `pytest`와 `httpx`를 사용하여 API 엔드포인트에 대한 단위 테스트 및 통합 테스트 코드 작성
- `pytest-html`과 같은 플러그인을 활용하여 테스트 결과를 HTML 보고서로 자동 생성

### 8. API 및 프로젝트 문서화
- FastAPI의 내장 기능을 활용하여 Swagger UI와 ReDoc을 활성화
- `docs/` 경로 아래에 프로젝트 아키텍처 다이어그램, 의존성 관리, ORM 가이드, 테스트 보고서, API 명세, 환경 변수 가이드 포함

### 9. 모노레포 및 프로젝트 역할
- 이 프로젝트는 모노레포의 `services/was-server` 폴더 내에 위치하도록 구성
- 모든 개발 문서와 코드는 WAS 서버에 초점을 맞춰 작성

### 10. 로깅 및 모니터링
- `logging` 모듈을 사용하여 요청/응답, 에러, 주요 이벤트 등을 기록
- 파일 로깅, 콘솔 로깅 등 환경에 맞는 로깅 핸들러를 구성
- 로그 파일은 Docker Volume을 통해 호스트 머신에 저장되어 컨테이너가 재시작되어도 유실되지 않도록 설정

### 11. `.gitignore` 구성
- `.env` 파일, 가상 환경 폴더, 파이썬 컴파일 파일, Alembic 생성 파일, 테스트 및 빌드 결과물, 로깅 파일 포함

---

## 🔄 **피드백 및 수정사항**

### 1. 작업 완료 체크 및 일시 중지
- 작업이 완료된 내용은 체크리스트에 체크
- 체크할 때마다 작업을 일시 중지하고 내용 설명 및 확인 요청

### 2. DB 컨테이너 제거
- DB는 컨테이너가 아니라 DB SERVER에 직접 접속
- db 컨테이너 제거

### 3. 컨테이너 데이터 영구성 보장
- 컨테이너에 있는 데이터가 일회성/휘발성이지 않게 반영구적으로 관리
- Docker Volume을 통한 데이터 영구 저장

### 4. 요구사항 기록 및 관리
- 지금까지 요청한 요청사항과 앞으로 요청할 요청사항도 모두 재사용 및 확인 가능
- task 폴더 안에 기록 및 관리

### 5. Context 길이 부족 극복 방안 개선
- 추가 개선 방안 반영

---

## 📝 **추가 요구사항 및 질문**

### 1. Docker Compose 컨테이너 구성
- 컨테이너 구성 방식 및 네트워크 설정

### 2. TDD 방식 적용
- 서버 구축 시에도 TDD 방식 적용 방법

### 3. Context 길이 부족 극복 방안
- 작업 진행 중 context 길이 부족 시 극복 방안
- task 폴더 아래에 지속적으로 작업 목표 및 내역 현황을 관리하고 재확인
- 더 좋은 방안이 있는 경우 역제안 요청

### 4. Prod 환경 AWS EC2 고려사항
- 추가 고려사항 제안 요청

### 5. 클린 아키텍처 레이어 구성 설명
- Adapter 레이어 위치
- 서비스 로직 위치

### 6. 환경 변수 파일 분리 관리
- 환경별 설정 파일 분리 방법

---

## 🚀 **구현 우선순위 (수정됨)**

### Phase 1: 기본 인프라
1. Docker Compose 환경 구성 (DB 컨테이너 제외)
2. FastAPI 기본 구조 설정
3. 외부 DB 연결 및 ORM 설정

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

---

## 📁 **수정된 프로젝트 구조**
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

**참고**: DB는 외부 서버에 직접 연결하므로 컨테이너 없음

