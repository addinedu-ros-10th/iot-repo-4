# 개발 작업 가이드라인

## 🏗️ **모노레포 구조 및 작업 경로**

### **프로젝트 루트 구조**
```
iot-repo-4/                    # 모노레포 루트
├── doc/                       # 프로젝트 전체 문서
├── task/                      # 작업 관리 및 가이드라인
├── services/                  # 서비스별 구현체
│   └── was-server/           # WAS 서버 (FastAPI)
│       ├── app/               # FastAPI 애플리케이션
│       ├── docker/            # Docker 관련 파일
│       ├── docs/              # WAS 서버 문서
│       └── ...
└── README.md                  # 프로젝트 전체 README
```

### **WAS 서버 작업 경로**
- **모든 WAS 관련 작업은 `services/was-server/` 경로 이하에서 수행**
- **절대 경로 사용 금지**: `services/was-server/` 기준으로 상대 경로 사용
- **프로젝트 루트에서 작업 시**: `cd services/was-server` 후 작업 수행

### **클린 아키텍처 레이어 구조**
```
services/was-server/app/
├── domain/                    # 도메인 모델 (엔티티, 값 객체)
├── use_cases/                 # 비즈니스 로직 (유스케이스)
├── interfaces/                # 어댑터 레이어 (API, 외부 서비스)
├── infrastructure/            # 인프라 구현 (DB, Redis, 외부 API)
├── api/                       # API 라우터 및 엔드포인트
└── core/                      # 핵심 설정 및 공통 기능
```

## 🔧 **개발 작업 규칙**

### **1. 경로 관리**
- **작업 시작 시**: `cd services/was-server` 명령으로 WAS 서버 디렉토리로 이동
- **상대 경로 사용**: `./app/`, `./config/`, `./tests/` 등
- **절대 경로 금지**: 전체 경로를 하드코딩하지 않음

### **2. 파일 생성 및 수정**
- **WAS 서버 파일**: `services/was-server/` 경로 이하에만 생성
- **프로젝트 전체 파일**: `task/`, `doc/` 등 루트 레벨에만 생성
- **경로 확인**: 파일 생성/수정 전 현재 작업 디렉토리 확인

### **3. 명령어 실행**
```bash
# 올바른 작업 순서
cd services/was-server          # WAS 서버 디렉토리로 이동
mkdir -p app/domain            # 상대 경로 사용
touch app/domain/__init__.py   # 상대 경로 사용

# 잘못된 예시 (절대 경로 사용)
mkdir -p /c/Users/.../services/was-server/app/domain  # ❌
```

## 📁 **디렉토리별 역할**

### **services/was-server/**
- **app/**: FastAPI 애플리케이션 코드
- **docker/**: Docker 관련 설정 파일
- **docs/**: WAS 서버 전용 문서
- **tests/**: 테스트 코드
- **config/**: 설정 파일
- **logs/**: 로그 파일

### **task/**
- **checklist.md**: 작업 체크리스트
- **work-log.md**: 작업 진행 로그
- **development-guidelines.md**: 개발 가이드라인 (이 파일)
- **checkpoints/**: 단계별 완료 보고서

### **doc/**
- **monorepo-guide.md**: 모노레포 가이드
- **project-structure.md**: 프로젝트 구조 설명
- **README.md**: 프로젝트 전체 개요

## ⚠️ **주의사항**

1. **모노레포 구조 준수**: 각 서비스는 지정된 경로에서만 작업
2. **경로 혼동 방지**: 작업 시작 전 현재 디렉토리 확인
3. **절대 경로 사용**: `services/was-server/` 기준 절대 경로 사용
4. **상대 경로 금지**: `app/domain/__init__.py` 등 모호한 상대 경로 사용 금지
5. **문서화**: 모든 작업은 task/ 폴더에 기록
6. **파일 도구 우선**: 터미널 명령어 대신 list_dir, read_file 등 파일 도구 우선 사용

---

**작성일**: 2024-08-20  
**작성자**: AI Assistant  
**검토자**: 사용자
