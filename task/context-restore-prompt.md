# 컨텍스트 복원 가이드 (Context Restoration Guide)

## 🎯 **목적**
AI 어시스턴트가 작업을 재개할 때 프로젝트의 현재 상태와 진행 방향을 빠르게 파악할 수 있도록 하는 가이드 문서입니다.

## 📋 **컨텍스트 복원 체크리스트**

### **1. 프로젝트 기본 정보 확인**
- [ ] **프로젝트 루트**: `/home/guehojung/Documents/Project/IOT/iot-repo-4`
- [ ] **현재 작업 서비스**: `services/was-server` (WAS 서버 구현)
- [ ] **프로젝트 유형**: IoT Care 백엔드 시스템 (FastAPI + PostgreSQL + Redis)

### **2. 현재 개발 단계 확인**
- [ ] **Phase 1**: ✅ 완료 (PostgreSQL/Redis 연결, Alembic 초기화)
- [ ] **Phase 2**: ✅ 완료 (도메인 모델, 의존성 주입, 리포지토리 패턴)
- [x] **Phase 3**: ✅ 완료 (API 엔드포인트 구현)

### **3. 최근 작업 내용 확인**
- [ ] **API 패키지 구조**: `app/api/v1/` 디렉토리 생성
- [ ] **스키마 파일**: `schemas.py` 생성 완료
- [ ] **남은 작업**: `users.py`, `devices.py`, `sensors.py`, `main.py` 구현

## 🚨 **중요 주의사항**

### **파일 경로 관리**
- **절대 경로 사용 필수**: `services/was-server/app/...`
- **상대 경로 사용 금지**: 경로 오류 발생 원인
- **작업 디렉토리 확인**: `pwd` 명령으로 현재 위치 확인

### **작업 디렉토리 확인 절차**
```bash
# 1. 현재 위치 확인
pwd

# 2. 작업 디렉토리 확인
ls -la

# 3. 필요시 올바른 디렉토리로 이동
cd services/was-server

# 4. 경로 확인 후 명령어 실행
mkdir -p app/api/v1
```

## 🔧 **현재 구현 상태**

### **완료된 컴포넌트**
- ✅ **도메인 엔티티**: User, Device
- ✅ **도메인 서비스**: UserService
- ✅ **리포지토리 인터페이스**: IUserRepository, IDeviceRepository
- ✅ **PostgreSQL 리포지토리**: PostgreSQLUserRepository, PostgreSQLDeviceRepository
- ✅ **의존성 주입**: DependencyContainer
- ✅ **ORM 모델**: 25개 테이블에 대한 SQLAlchemy 모델

### **현재 구현 중인 컴포넌트**
- 🔄 **API 엔드포인트**: 사용자, 디바이스, 센서 API
- 🔄 **FastAPI 애플리케이션**: 메인 애플리케이션 통합

### **다음 구현 예정**
- 📋 **API 테스트**: 엔드포인트 기능 검증
- 📋 **Phase 4**: 고급 기능 구현

## 📁 **프로젝트 구조**

### **현재 디렉토리 구조**
```
services/was-server/
├── app/
│   ├── api/                    # 🔄 구현 중
│   │   ├── __init__.py        # ✅ 완료
│   │   └── v1/
│   │       ├── __init__.py    # ✅ 완료
│   │       ├── schemas.py     # ✅ 완료
│   │       ├── users.py       # 📋 구현 예정
│   │       ├── devices.py     # 📋 구현 예정
│   │       └── sensors.py     # 📋 구현 예정
│   ├── core/                  # ✅ 완료
│   ├── domain/                # ✅ 완료
│   ├── infrastructure/        # ✅ 완료
│   ├── interfaces/            # ✅ 완료
│   └── main.py               # 📋 구현 예정
├── tests/                     # ✅ 완료
└── alembic/                   # ✅ 완료
```

## 🎯 **즉시 진행할 작업**

### **1단계: API 엔드포인트 구현 완료**
- `app/api/v1/users.py`: 사용자 CRUD API
- `app/api/v1/devices.py`: 디바이스 CRUD API
- `app/api/v1/sensors.py`: 센서 데이터 API

### **2단계: 메인 애플리케이션 통합**
- `app/main.py`: FastAPI 애플리케이션 설정
- API 라우터 등록 및 미들웨어 설정

### **3단계: API 테스트 및 검증**
- 엔드포인트 기능 테스트
- Docker 환경에서 실행 검증

## 🔍 **문제 해결 참고사항**

### **자주 발생하는 문제**
1. **파일 경로 오류**: 절대 경로 사용으로 해결
2. **Docker 파일 동기화**: 볼륨 마운트 설정 확인
3. **모듈 임포트 오류**: Python 경로 및 패키지 구조 확인

### **해결 방안**
- **즉시 정리**: 잘못 생성된 파일들 삭제
- **절대 경로 재생성**: 올바른 위치에 파일 재생성
- **경로 검증**: 생성된 파일 위치 재확인

## 📚 **참고 문서**

### **핵심 문서**
- `task/work-log.md`: 작업 진행 상황 상세 기록
- `task/checklist.md`: 요구사항 체크리스트
- `task/development-guidelines.md`: 개발 지침 및 문제 해결 방안
- `doc/project-structure.md`: 프로젝트 구조 설명

### **기술 문서**
- FastAPI 공식 문서
- SQLAlchemy 공식 문서
- Clean Architecture 원칙

## 🚀 **작업 재개 시 확인사항**

### **시작 전 체크**
- [ ] 현재 작업 디렉토리 확인 (`pwd`)
- [ ] 프로젝트 구조 확인 (`ls -la`)
- [ ] 최근 작업 내용 파악 (위 문서 참조)
- [ ] 파일 경로 관리 지침 준수

### **작업 진행 원칙**
1. **절대 경로 사용**: `services/was-server/app/...`
2. **단계별 구현**: 한 번에 하나의 컴포넌트씩 구현
3. **즉시 검증**: 구현 후 테스트 및 검증
4. **문서화**: 작업 진행 상황 기록

---

**작성일**: 2024-08-20  
**작성자**: AI Assistant  
**상태**: 활성화 ✅  
**최종 업데이트**: Phase 3 API 엔드포인트 구현 완료, Phase 4 준비 중

