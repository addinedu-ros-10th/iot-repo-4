# IoT Care Backend System 개발 가이드라인

**작성일**: 2025-08-22  
**마지막 업데이트**: 2025-08-22 11:30:00  
**프로젝트**: IoT Repository 4 - WAS Server

## 🚀 개발 환경 설정

### 1. 개발 머신 IP 주소 확인 및 환경변수 업데이트 (프로젝트 기동 시 필수)

#### **중요성 및 목적**
- **DB Connection Refused 방지**: IP 변경으로 인한 데이터베이스 연결 실패 사전 방지
- **개발 환경 자동화**: Agent가 스스로 환경을 파악하고 설정할 수 있도록 문서화
- **문제 반복 방지**: 이미 해결된 환경 설정 문제의 재발 방지

#### **프로젝트 기동 시 필수 수행 절차**
1. **IP 주소 조사**: 현재 개발 머신의 실제 IP 주소 확인
2. **환경변수 파일 확인**: `.env.local` 파일의 현재 설정 상태 확인
3. **IP 정보 업데이트**: 환경변수 파일의 IP 관련 설정 업데이트
4. **Docker 환경 재시작**: 업데이트된 환경변수로 컨테이너 재시작
5. **연결 상태 검증**: 데이터베이스 연결 및 API 서버 상태 확인

#### **OS별 IP 조사 명령어**

##### **Windows 환경 (Git Bash)**
```bash
# 방법 1: PowerShell 명령어 실행 (권장)
powershell -Command "ipconfig | findstr 'IPv4'"

# 방법 2: 직접 ipconfig 실행
ipconfig | grep "IPv4"

# 방법 3: 상세 정보 확인
powershell -Command "Get-NetIPAddress | Where-Object {$_.AddressFamily -eq 'IPv4' -and $_.IPAddress -notlike '127.*' -and $_.IPAddress -notlike '169.*'} | Select-Object IPAddress, InterfaceAlias"
```

##### **Linux/macOS 환경**
```bash
# 방법 1: 기본 IP 확인
ip addr show | grep "inet " | grep -v "127.0.0.1"

# 방법 2: ifconfig 사용
ifconfig | grep "inet " | grep -v "127.0.0.1"

# 방법 3: hostname 사용
hostname -I
```

#### **환경변수 파일 관리 체계**
프로젝트는 운영/개발 환경별로 환경변수를 분리하여 관리합니다:

- **`.env.local`**: 로컬 개발 환경 (현재 사용 중)
- **`.env.dev`**: 개발 서버 환경
- **`.env.prod`**: 운영 서버 환경

#### **업데이트 대상 환경변수**
- **`DB_HOST`**: 현재 개발 머신의 실제 IP 주소
- **`CADDY_DOMAIN`**: 현재 개발 머신의 실제 IP 주소
- **`REDIS_HOST`**: Redis 컨테이너 IP (일반적으로 Docker 내부 IP)

#### **AWS EC2 운영 환경 IP 주소**
- **현재 운영 환경 IP**: `ec2-43-201-96-23.ap-northeast-2.compute.amazonaws.com` ✅ **고정 IP 부여됨**
- **이전 운영 환경 IP**: `ec2-3-34-98-7.ap-northeast-2.compute.amazonaws.com`
- **업데이트 날짜**: 2025-08-23
- **IP 타입**: Elastic IP (고정 IP) - IP 주소 변경 없음

#### **SSL 인증서 제한 사항**
- **IP 주소 제한**: Let's Encrypt는 IP 주소에 직접 SSL 인증서 발급 불가
- **도메인 필요**: 실제 도메인 이름이 필요 (예: `iot-care.com`)
- **현재 설정**: HTTP 전용 (보안을 위해 내부 네트워크에서만 접근 권장)
- **HTTPS 활성화**: Route 53을 통한 실제 도메인 설정 후 가능

#### **환경변수 자동 업데이트 스크립트**

##### **Windows 환경용 업데이트 스크립트**
```bash
#!/bin/bash
# update_env_vars.sh

echo "🔍 현재 개발 머신 IP 주소 조사 중..."

# Windows 환경에서 IP 주소 추출
CURRENT_IP=$(powershell -Command "Get-NetIPAddress | Where-Object {$_.AddressFamily -eq 'IPv4' -and $_.IPAddress -notlike '127.*' -and $_.IPAddress -notlike '169.*'} | Select-Object -First 1 -ExpandProperty IPAddress" | tr -d '\r')

if [ -z "$CURRENT_IP" ]; then
    echo "❌ IP 주소를 찾을 수 없습니다."
    exit 1
fi

echo "✅ 현재 IP 주소: $CURRENT_IP"

# .env.local 파일 업데이트
if [ -f ".env.local" ]; then
    echo "📝 .env.local 파일 업데이트 중..."
    
    # DB_HOST 업데이트
    sed -i "s/DB_HOST=.*/DB_HOST=$CURRENT_IP/g" .env.local
    
    # CADDY_DOMAIN 업데이트
    sed -i "s/CADDY_DOMAIN=.*/CADDY_DOMAIN=$CURRENT_IP/g" .env.local
    
    echo "✅ 환경변수 업데이트 완료"
    echo "📋 업데이트된 내용:"
    grep -E "^(DB_HOST|CADDY_DOMAIN)=" .env.local
else
    echo "❌ .env.local 파일을 찾을 수 없습니다."
    exit 1
fi
```

##### **수동 업데이트 명령어**
```bash
# DB_HOST 업데이트
sed -i "s/DB_HOST=.*/DB_HOST=$CURRENT_IP/g" .env.local

# CADDY_DOMAIN 업데이트  
sed -i "s/CADDY_DOMAIN=.*/CADDY_DOMAIN=$CURRENT_IP/g" .env.local

# 업데이트 확인
grep -E "^(DB_HOST|CADDY_DOMAIN)=" .env.local
```

#### **환경변수 업데이트 후 Docker 재시작 절차**
```bash
# 1. 컨테이너 및 볼륨 완전 제거
docker-compose down --volumes --remove-orphans

# 2. Docker 시스템 정리
docker system prune -f

# 3. 프로젝트 재시작
docker-compose up -d

# 4. 상태 확인
docker-compose ps

# 5. API 서버 상태 확인
curl -s http://localhost:8000/health

# 6. 데이터베이스 연결 상태 확인
docker logs iot-care-app | grep -i "database\|connection"
```

#### **연결 상태 검증 체크리스트**
- [ ] Docker 컨테이너 정상 실행 상태
- [ ] API 서버 Health Check 응답 (200 OK)
- [ ] 데이터베이스 연결 로그 확인
- [ ] Redis 연결 상태 확인
- [ ] 외부 데이터베이스 서버 연결 가능 여부

### 2. Agent 자동화 및 행동 유도 방안

#### **Agent 자동 실행 체크리스트**
프로젝트 기동 시 Agent가 자동으로 수행해야 할 작업들:

- [ ] **IP 주소 자동 조사**: 현재 개발 머신의 IP 주소 자동 감지
- [ ] **환경변수 자동 업데이트**: `.env.local` 파일의 IP 관련 설정 자동 수정
- [ ] **Docker 환경 재시작**: 업데이트된 환경변수로 컨테이너 자동 재시작
- [ ] **연결 상태 자동 검증**: 데이터베이스 및 API 서버 연결 상태 자동 확인
- [ ] **문제 발생 시 자동 진단**: 연결 실패 시 원인 분석 및 해결 방안 제시

#### **Agent 행동 유도 프롬프트 템플릿**
```
프로젝트 기동 시 다음 순서로 작업을 수행하세요:

1. IP 조사: 현재 개발 머신의 IP 주소를 OS에 맞는 명령어로 확인
2. 환경변수 업데이트: .env.local 파일의 DB_HOST, CADDY_DOMAIN을 현재 IP로 수정
3. Docker 재시작: docker-compose down && docker-compose up -d
4. 연결 검증: API 서버 health check 및 데이터베이스 연결 상태 확인
5. 문제 진단: 오류 발생 시 로그 분석 및 해결 방안 제시

각 단계별로 결과를 확인하고 다음 단계로 진행하세요.
```

#### **자동화 스크립트 실행 권장사항**
- **Windows 환경**: `update_env_vars.sh` 스크립트 자동 실행
- **Linux/macOS 환경**: `update_env_vars.sh` 스크립트 자동 실행
- **수동 실행**: 스크립트 실행 불가 시 수동 명령어 실행

#### **문제 발생 시 Agent 대응 방안**
1. **연결 실패 감지**: 데이터베이스 연결 오류 로그 확인
2. **IP 변경 의심**: 환경변수 파일의 IP 설정과 현재 IP 비교
3. **자동 해결 시도**: IP 업데이트 및 Docker 재시작 자동 실행
4. **수동 개입 필요 시**: 사용자에게 구체적인 해결 단계 안내

#### **일반적인 문제 및 해결 방안**

##### **1. 데이터베이스 연결 실패 (Connection Refused)**
- **증상**: `connection to server at "IP", port "PORT" failed: Connection refused`
- **원인**: 
  - 외부 데이터베이스 서버가 실행되지 않음
  - SSH tunnel 연결 끊어짐
  - 방화벽이나 네트워크 설정 문제
  - 포트 번호 오류
- **해결 방안**:
  1. **SSH tunnel 연결 상태 확인 및 재연결** (우선순위)
  2. 외부 데이터베이스 서버 실행 상태 확인
  3. 네트워크 연결 및 포트 설정 확인
  4. 방화벽 설정 확인

##### **데이터베이스 사용 정책**
- **✅ 사용**: 외부 PostgreSQL 서버 (SSH tunnel 경유)
- **❌ 사용 금지**: 로컬 PostgreSQL 컨테이너
- **이유**: 
  - 실제 운영 환경과 동일한 구조 유지
  - 데이터 일관성 보장
  - 개발팀 간 동일한 데이터베이스 환경 공유

##### **2. Actuator API 의존성 오류**
- **증상**: `NameError: name 'DependencyContainer' is not defined`
- **원인**: 
  - `DependencyContainer` 클래스 import 누락
  - 순환 import 문제
- **해결 방안**:
  1. `app/core/container.py`에서 `DependencyContainer` import 확인
  2. 순환 import 문제 해결
  3. 의존성 주입 구조 검증

##### **3. Pydantic 호환성 경고**
- **증상**: `'orm_mode' has been renamed to 'from_attributes'`
- **원인**: Pydantic v1과 v2 간 호환성 문제
- **해결 방안**:
  1. 스키마에서 `orm_mode = True` → `from_attributes = True` 변경
  2. Pydantic 버전 호환성 확인
  3. 스키마 구조 검증

#### **문제 해결 우선순위**
1. **높음**: 데이터베이스 연결 문제 (API 동작 불가)
2. **중간**: Actuator API 의존성 문제 (일부 API 동작 불가)
3. **낮음**: Pydantic 호환성 경고 (기능에는 영향 없음)

#### 환경변수 파일 관리 체계
프로젝트는 운영/개발 환경별로 환경변수를 분리하여 관리합니다:

- **`.env.local`**: 로컬 개발 환경 (현재 사용 중)
- **`.env.dev`**: 개발 서버 환경
- **`.env.prod`**: 운영 서버 환경

#### Windows 환경에서 IP 주소 확인
```bash
# Git Bash에서 PowerShell 명령어 실행
powershell -Command "ipconfig"

# 또는 직접 실행
ipconfig
```

#### 환경변수 파일 업데이트
- **파일 위치**: `services/was-server/.env.local`
- **업데이트 대상**:
  - `DB_HOST`: 현재 개발 머신의 실제 IP 주소
  - `CADDY_DOMAIN`: 현재 개발 머신의 실제 IP 주소

#### 업데이트 명령어
```bash
# DB_HOST 업데이트
sed -i 's/DB_HOST=이전IP/DB_HOST=현재IP/g' .env.local

# CADDY_DOMAIN 업데이트  
sed -i 's/CADDY_DOMAIN=이전IP/CADDY_DOMAIN=현재IP/g' .env.local
```

#### 환경변수 업데이트 후 Docker 재시작
```bash
# 컨테이너 및 볼륨 완전 제거
docker-compose down --volumes --remove-orphans

# Docker 시스템 정리
docker system prune -f

# 프로젝트 재시작
docker-compose up -d

# 상태 확인
docker-compose ps
curl -s http://localhost:8000/health
```

### 2. 가상환경 활성화
```bash
# 가상환경 활성화
source .venv/Scripts/activate

# 패키지 설치 확인
pip list | grep fastapi
```

### 3. 환경별 설정 전환
```bash
# 로컬 개발 환경
cp .env.local .env

# 개발 서버 환경
cp .env.dev .env

# 운영 서버 환경
cp .env.prod .env
```

## 🚨 **중요: 디렉토리 및 파일 생성 시 주의사항**

### **디렉토리 생성 전 확인 절차**
1. **현재 위치 확인**: `pwd` 명령으로 현재 작업 디렉토리 확인
2. **대상 경로 확인**: `ls -la` 명령으로 대상 디렉토리 존재 여부 확인
3. **중복 방지**: 동일한 이름의 디렉토리/파일이 이미 존재하는지 확인
4. **경로 검증**: 생성할 디렉토리/파일의 경로가 올바른지 검증

### **파일 관리 원칙**
- **절대 경로 사용 금지**: 하드코딩된 절대 경로 사용 금지
- **상대 경로 우선**: 현재 작업 디렉토리 기준 상대 경로 사용
- **경로 검증 의무**: 파일 생성/수정 전 경로 유효성 검증 필수
- **중복 확인**: 동일한 이름의 파일/디렉토리 생성 전 존재 여부 확인

## 📋 **Task 파일 통합 관리 지침**

### **Task 파일 중앙 집중식 관리 원칙**
**모든 개발 관련 문서는 프로젝트 루트의 `task/` 디렉토리에서 통합 관리되어야 합니다.**

#### **관리 대상 문서**
- **개발 요청 및 계획**: 프로젝트 요구사항, 개발 계획, 작업 할당
- **개발 이력**: 작업 로그, 진행 상황, 완료된 작업 내역
- **개발 현황**: 현재 진행률, 해결된 문제, 진행 중인 이슈
- **문제 해결**: 발생한 문제, 해결 방법, 트러블슈팅 기록
- **개발 지침**: 코딩 표준, 아키텍처 가이드, 베스트 프랙티스

#### **Task 파일 통합 관리 구조**
```
iot-repo-4/
├── task/                           # 🎯 전체 프로젝트 통합 관리
│   ├── README.md                   # Task 관리 개요
│   ├── checklist.md                # 개발 체크리스트
│   ├── work-log.md                 # 개발 작업 로그
│   ├── current-development-status.md # 현재 개발 현황
│   ├── issues-and-solutions.md     # 문제 및 해결책
│   ├── phase4-progress-summary.md  # Phase 4 진행 요약
│   ├── requirements-summary.md     # 요구사항 요약
│   ├── api-implementation-progress.md # API 구현 진행 상황
│   ├── context-restore-prompt.md   # 작업 컨텍스트 복구
│   ├── development-guidelines.md   # 개발 지침 (현재 파일)
│   ├── api-test-checklist.md       # API 테스트 체크리스트
│   ├── api-endpoint-management-guidelines.md # API 엔드포인트 관리
│   ├── problem-analysis-and-prevention-policy.md # 문제 분석 및 예방
│   ├── tdd-implementation-plan.md  # TDD 구현 계획
│   ├── ai-agent-work-guidelines.md # AI 에이전트 작업 지침
│   ├── context-management.md       # 컨텍스트 관리
│   └── checkpoints/                # 체크포인트 문서
│       ├── phase1-1-complete.md
│       ├── phase1-2-complete.md
│       └── ...
├── services/
│   └── was-server/                 # WAS 서버 전용
│       ├── app/                    # 애플리케이션 코드
│       ├── docs/                   # 기술 문서
│       └── ...                     # 기타 서비스 파일
└── ...
```

#### **Task 파일 통합 관리 규칙**

##### **1. 중앙 집중식 관리**
- **모든 개발 관련 문서는 `iot-repo-4/task/` 디렉토리에 통합 보관**
- **서비스별 개별 task 디렉토리는 허용하지 않음**
- **문서 중복 및 분산 관리는 금지**

##### **2. 문서 통합 절차**
- **신규 문서 작성**: 프로젝트 루트 `task/` 디렉토리에 직접 작성
- **기존 문서 통합**: 서비스별 task 디렉토리의 문서를 프로젝트 루트로 이동
- **문서 업데이트**: 최신 정보로 통합하여 중복 제거

##### **3. 문서 분류 및 명명 규칙**
- **상태별 분류**: 완료(✅), 진행 중(🔄), 문제 발생(❌), 대기 중(📋)
- **일관된 명명**: `YYYY-MM-DD_문서명.md` 형식 권장
- **버전 관리**: 문서 변경 이력 추적 및 관리

##### **4. 접근 및 수정 권한**
- **읽기 권한**: 모든 개발자에게 공개
- **수정 권한**: 담당 개발자 또는 프로젝트 관리자
- **검토 의무**: 주요 문서 수정 시 검토 및 승인 절차

#### **Task 파일 통합 관리 이점**
1. **정보 일관성**: 모든 개발 관련 정보를 한 곳에서 관리
2. **중복 제거**: 동일한 정보의 중복 보관 방지
3. **검색 효율성**: 필요한 정보를 빠르게 찾을 수 있음
4. **협업 개선**: 팀원 간 정보 공유 및 협업 효율성 향상
5. **유지보수성**: 문서 관리 및 업데이트 작업 단순화

#### **Task 파일 통합 관리 체크리스트**
- [ ] 모든 개발 관련 문서가 `iot-repo-4/task/` 디렉토리에 통합 보관됨
- [ ] 서비스별 개별 task 디렉토리 제거 완료
- [ ] 문서 중복 및 분산 관리 해결 완료
- [ ] 문서 분류 및 명명 규칙 적용 완료
- [ ] 문서 접근 및 수정 권한 설정 완료
- [ ] 문서 통합 관리 이점 확인 및 검증 완료

---

## 🏗️ **Clean Architecture 구현 지침**

### **1. 레이어 분리 원칙**
- **Domain Layer**: 순수한 비즈니스 로직만 포함
- **Use Case Layer**: 애플리케이션 비즈니스 규칙 구현
- **Interface Layer**: 추상화된 Repository/Service 인터페이스
- **Infrastructure Layer**: 구체적인 구현체 (데이터베이스, 외부 API 등)
- **API Layer**: HTTP 엔드포인트 및 요청/응답 처리

### **2. 의존성 방향**
```
API Layer → Use Case Layer → Domain Layer
     ↓              ↓              ↓
Interface Layer ← Interface Layer ← Interface Layer
     ↓              ↓              ↓
Infrastructure Layer → Infrastructure Layer → Infrastructure Layer
```

**중요**: 의존성은 항상 안쪽(Domain)을 향해야 하며, 바깥쪽(Infrastructure)에서 안쪽으로 의존할 수 없음

### **3. 인터페이스 분리 원칙**
- 각 Repository/Service는 단일 책임을 가져야 함
- 인터페이스는 구체적인 구현에 의존하지 않아야 함
- 의존성 주입을 통해 구체적인 구현체를 주입받아야 함

---

## 📁 **프로젝트 구조 관리**

### **디렉토리 구조**
```
iot-repo-4/
├── task/                           # 🎯 전체 프로젝트 통합 관리
│   ├── checklist.md               # 개발 체크리스트
│   ├── work-log.md                # 개발 작업 로그
│   ├── development-guidelines.md  # 개발 지침
│   └── ...                        # 기타 개발 관련 문서
├── services/
│   └── was-server/                # WAS 서버 전용
│       ├── app/                   # 애플리케이션 코드
│       ├── docs/                  # 기술 문서
│       └── ...                    # 기타 서비스 파일
└── ...
```

### **파일 관리 규칙**
- **공통 문서**: 프로젝트 루트 `task/` 폴더에 통합 배치
- **서비스별 문서**: 해당 서비스 디렉토리 내 `docs/` 폴더에 배치 (기술 문서만)
- **문서 통합**: 모든 개발 관련 문서는 프로젝트 루트 `task/` 폴더에서 통합 관리

---

## 🔧 **코딩 표준**

### **1. Python 코딩 스타일**
- **PEP 8 준수**: Python 공식 스타일 가이드 준수
- **타입 힌트 사용**: 모든 함수와 변수에 타입 힌트 명시
- **문서화**: 모든 클래스와 함수에 docstring 작성
- **에러 처리**: 적절한 예외 처리 및 로깅 구현

### **2. FastAPI 사용 규칙**
- **의존성 주입**: `Depends()`를 사용한 의존성 주입 구현
- **Pydantic 모델**: 요청/응답 데이터 검증을 위한 Pydantic 스키마 사용
- **HTTP 상태 코드**: 적절한 HTTP 상태 코드 반환
- **에러 응답**: 일관된 에러 응답 형식 사용

### **3. 데이터베이스 접근**
- **Repository 패턴**: 데이터 접근 로직을 Repository 클래스로 캡슐화
- **트랜잭션 관리**: 적절한 트랜잭션 경계 설정
- **연결 풀링**: 데이터베이스 연결 풀 관리
- **비동기 처리**: SQLAlchemy async 기능 활용

---

## 🧪 **테스트 지침**

### **1. TDD 원칙**
- **테스트 우선**: 기능 구현 전 테스트 코드 작성
- **리팩토링**: 테스트 통과 후 코드 개선
- **커버리지**: 최소 80% 이상의 테스트 커버리지 유지

### **2. 테스트 구조**
- **Unit Test**: 개별 함수/클래스 단위 테스트
- **Integration Test**: 여러 컴포넌트 간 통합 테스트
- **End-to-End Test**: 전체 시스템 동작 테스트

### **3. 테스트 데이터**
- **테스트 DB**: 테스트 전용 데이터베이스 사용
- **Fixture**: 테스트 데이터를 위한 fixture 파일 사용
- **Cleanup**: 테스트 후 데이터 정리

---

## 📚 **문서화 지침**

### **1. 필수 문서**
- **README.md**: 프로젝트 개요 및 시작 가이드
- **API 문서**: Swagger UI를 통한 자동 API 문서 생성
- **개발 가이드**: 개발자 온보딩 및 참고 자료
- **배포 가이드**: 운영 환경 배포 및 관리 방법

### **2. 문서 관리**
- **버전 관리**: 문서 변경 이력 관리
- **검토 프로세스**: 문서 작성 후 검토 및 승인 절차
- **정기 업데이트**: 프로젝트 진행에 따른 문서 정기 업데이트

---

## 🚀 **배포 및 운영**

### **1. 환경별 설정**
- **Local**: 개발자 로컬 환경
- **Development**: 개발 서버 환경
- **Production**: 운영 서버 환경

### **2. 컨테이너 관리**
- **Docker**: 애플리케이션 컨테이너화
- **Docker Compose**: 다중 컨테이너 오케스트레이션
- **볼륨 관리**: 데이터 영속성을 위한 볼륨 마운트

### **3. 모니터링**
- **로깅**: 구조화된 로그 수집 및 관리
- **메트릭**: 성능 및 상태 메트릭 수집
- **알림**: 이상 상황 발생 시 알림 시스템

---

## 📋 **체크리스트**

### **개발 시작 전**
- [ ] 현재 작업 디렉토리 확인 (`pwd`)
- [ ] 대상 경로 존재 여부 확인 (`ls -la`)
- [ ] 개발 지침 문서 검토
- [ ] 기존 코드 구조 파악
- [ ] Task 파일 통합 관리 상태 확인

### **코드 작성 중**
- [ ] Clean Architecture 원칙 준수
- [ ] 의존성 주입 패턴 적용
- [ ] 적절한 에러 처리 구현
- [ ] 타입 힌트 및 문서화

### **테스트 및 검증**
- [ ] TDD 원칙에 따른 테스트 코드 작성
- [ ] 모든 테스트 케이스 통과 확인
- [ ] 코드 리뷰 및 개선
- [ ] 문서 업데이트

### **Task 파일 관리**
- [ ] 모든 개발 관련 문서가 `task/` 디렉토리에 통합 보관됨
- [ ] 문서 중복 및 분산 관리 해결됨
- [ ] 문서 분류 및 명명 규칙 적용됨
- [ ] 문서 접근 및 수정 권한 설정됨

---

**마지막 업데이트**: 2025-08-22 11:30:00  
**작성자**: AI Assistant  
**검토자**: 사용자  
**상태**: 활성 ✅  
**Task 파일 통합 관리**: 완료 ✅
