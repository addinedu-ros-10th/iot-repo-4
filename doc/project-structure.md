# IoT Care Project Structure

## Overview
독거노인 통합 돌봄 서비스를 위한 IoT 백엔드 시스템입니다.

## Architecture
- **Clean Architecture**: 도메인 중심의 계층화된 아키텍처
- **Dependency Injection**: 의존성 역전 원칙 구현
- **Repository Pattern**: 데이터 접근 추상화
- **TDD**: 테스트 주도 개발 방식

## Directory Structure

### Root Level
```
iot-repo-4/
├── doc/                    # 프로젝트 문서
├── services/               # 마이크로서비스들
│   └── was-server/        # Web Application Server
└── task/                   # 개발 작업 관리
```

### WAS Server (`services/was-server/`)
```
app/
├── __init__.py
├── main.py                 # FastAPI 애플리케이션 진입점
├── api/                    # API 레이어 (외부 인터페이스)
│   └── __init__.py
├── core/                   # 핵심 설정 및 유틸리티
│   ├── __init__.py
│   ├── config.py          # 환경 설정 관리
│   └── container.py       # 의존성 주입 컨테이너 ✅
├── domain/                 # 도메인 레이어 (비즈니스 로직)
│   ├── __init__.py
│   ├── entities/          # 도메인 엔티티
│   │   ├── user.py        # 사용자 엔티티 ✅
│   │   └── device.py      # 디바이스 엔티티 ✅
│   └── services/          # 도메인 서비스
│       └── user_service.py # 사용자 비즈니스 로직 ✅
├── infrastructure/         # 인프라스트럭처 레이어
│   ├── __init__.py
│   ├── database.py        # 데이터베이스 연결 관리 ✅
│   ├── redis_client.py    # Redis 클라이언트 ✅
│   └── repositories/      # 리포지토리 구현체
│       ├── memory_user_repository.py      # 메모리 사용자 리포지토리 ✅
│       └── memory_device_repository.py    # 메모리 디바이스 리포지토리 ✅
├── interfaces/             # 인터페이스 레이어 (추상화)
│   ├── __init__.py
│   ├── repositories/      # 리포지토리 인터페이스
│   │   ├── user_repository.py     # 사용자 리포지토리 인터페이스 ✅
│   │   └── device_repository.py   # 디바이스 리포지토리 인터페이스 ✅
│   └── services/          # 서비스 인터페이스
│       └── user_service_interface.py # 사용자 서비스 인터페이스 ✅
├── use_cases/              # 유스케이스 레이어
│   └── __init__.py
└── logs/                   # 로그 파일들

tests/                      # 테스트 코드
├── domain/                 # 도메인 모델 테스트
│   └── entities/          # 엔티티 테스트
└── core/                   # 핵심 기능 테스트
    └── test_container.py  # 의존성 주입 컨테이너 테스트 ✅

alembic/                    # 데이터베이스 마이그레이션
├── env.py                 # Alembic 환경 설정 ✅
└── script.py.mako         # 마이그레이션 스크립트 템플릿

config/                     # 설정 파일들
├── redis.conf             # Redis 설정
└── ...

docker-compose.yml          # Docker Compose 설정 ✅
Dockerfile                  # Docker 이미지 설정 ✅
requirements.txt            # Python 패키지 의존성 ✅
```

## Key Components

### 1. Domain Layer ✅
- **User Entity**: 사용자 관리, 역할 기반 권한
- **Device Entity**: IoT 디바이스 관리, 사용자 할당
- **UserService**: 사용자 비즈니스 로직, 권한 검증

### 2. Interface Layer ✅
- **Repository Interfaces**: 데이터 접근 추상화
- **Service Interfaces**: 비즈니스 로직 추상화

### 3. Infrastructure Layer ✅
- **Database**: PostgreSQL 연결 및 관리
- **Redis**: 캐싱 및 세션 관리
- **Memory Repositories**: 테스트용 인메모리 저장소

### 4. Dependency Injection ✅
- **Container**: 중앙 집중식 의존성 관리
- **Service Registry**: 서비스 및 리포지토리 등록
- **Type Safety**: 타입 안전성 보장

## Technology Stack

### Backend
- **Framework**: FastAPI 0.104.1
- **Language**: Python 3.11
- **Database**: PostgreSQL (via SSH tunnel)
- **Cache**: Redis 5.0.1
- **ORM**: SQLAlchemy 2.0.23
- **Migration**: Alembic 1.12.1

### Development Tools
- **Testing**: pytest 7.4.3
- **Code Quality**: black, flake8, mypy
- **Container**: Docker & Docker Compose

### Architecture Patterns
- **Clean Architecture**: 계층화된 아키텍처
- **Repository Pattern**: 데이터 접근 추상화
- **Dependency Injection**: 의존성 역전 원칙
- **TDD**: 테스트 주도 개발

## Current Status

### ✅ Completed
- Phase 1-3: PostgreSQL 연결 및 Alembic 초기화
- Phase 2-1: 도메인 모델 구현
- Phase 2-2: 의존성 주입 시스템 구현

### 🔄 In Progress
- Phase 2-3: 리포지토리 패턴 구현 (데이터베이스 연동)

### 📋 Planned
- Phase 3: API 엔드포인트 구현
- Phase 4: 고급 기능 구현

## Development Guidelines

### Code Organization
- 각 레이어는 명확한 책임을 가짐
- 의존성은 항상 내부 레이어를 향함
- 인터페이스를 통한 추상화

### Testing Strategy
- TDD 방식으로 개발
- 단위 테스트 우선
- 통합 테스트로 검증

### Database Management
- Alembic을 통한 스키마 관리
- 마이그레이션 기반 배포
- 롤백 지원
