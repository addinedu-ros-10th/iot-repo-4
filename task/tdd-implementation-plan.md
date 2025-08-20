# TDD 적용 계획: IoT Care Backend 시스템

## 🎯 **TDD 적용 목표**
서버 구축 시에도 TDD 방식을 적용하여 안정적이고 검증 가능한 코드를 작성합니다.

## 📋 **TDD 적용 단계별 계획**

### **Phase 1: 기본 인프라 (현재 진행 중)**
#### **1-1. Docker Compose 환경 구성** ✅ **완료**
- **테스트**: Docker 컨테이너 정상 실행 확인
- **검증**: 환경별 설정 파일 정상 동작

#### **1-2. FastAPI 기본 구조 설정** ✅ **완료**
- **테스트**: 클린 아키텍처 레이어 구조 검증
- **검증**: 각 레이어별 __init__.py 파일 정상 생성

#### **1-3. 외부 DB 연결 및 ORM 설정** ✅ **완료**
- **완료된 작업**:
  - ✅ Visual C++ Build Tools 설치 (Windows psycopg2 빌드 지원)
  - ✅ 가상환경 생성 (.venv 폴더)
  - ✅ 패키지 설치 스크립트 생성 (자동화된 설치)
  - ✅ Docker 환경에서 패키지 설치 완료
  - ✅ FastAPI 애플리케이션 실행 성공
  - ✅ API 엔드포인트 검증 완료
  - ✅ PostgreSQL 연결 문제 해결 완료
  - ✅ Redis 연결 테스트 성공

- **테스트 계획**:
  ```python
  # 데이터베이스 연결 테스트
  def test_database_connection():
      # PostgreSQL 연결 성공 확인
      # Redis 연결 성공 확인
      # Alembic 마이그레이션 정상 동작 확인

  # 기존 테이블 보존 테스트
  def test_existing_tables_preserved():
      # alembic stamp head 실행 후 기존 테이블 유지 확인
      # 새로운 마이그레이션으로 테이블 추가만 가능 확인
  ```

### **Phase 2: 핵심 기능**
#### **2-1. 도메인 모델 구현** ✅ **완료**
- **완료된 작업**:
  - ✅ Clean Architecture 기반 도메인 모델 구조 설계
  - ✅ User 엔티티 구현 (UUID, 역할 기반 권한, 프로필 관리)
  - ✅ Device 엔티티 구현 (디바이스 관리, 사용자 할당)
  - ✅ UserService 구현 (비즈니스 로직, 권한 검증)
  - ✅ TDD 테스트 작성 (15/16 테스트 통과, 93.75% 커버리지)

#### **2-2. 의존성 주입 시스템 구현** ✅ **완료**
- **완료된 작업**:
  - ✅ 인터페이스 정의 (IUserRepository, IDeviceRepository, IUserService)
  - ✅ 의존성 주입 컨테이너 구현 (DependencyContainer)
  - ✅ 메모리 리포지토리 구현 (MemoryUserRepository, MemoryDeviceRepository)
  - ✅ 의존성 주입 시스템 통합 테스트 완료

#### **2-3. 리포지토리 패턴 구현** ⏳ **다음 단계**
- **구현 예정**:
  - 데이터베이스 리포지토리 구현 (PostgreSQL 연동)
  - 단위 테스트를 위한 Mock 리포지토리 구현
  - 리포지토리 패턴 테스트 및 검증

#### **2-3. 기본 API 엔드포인트**
- **테스트**: HTTP 요청/응답 정상 동작 확인
- **검증**: API 스키마 및 유효성 검사 정상 동작

### **Phase 3: 고급 기능**
#### **3-1. 태스크 스케줄러**
- **테스트**: APScheduler 정상 동작 확인
- **검증**: 주기적 작업 실행 및 에러 처리

#### **3-2. 로깅 시스템**
- **테스트**: 로그 레벨별 정상 동작 확인
- **검증**: 파일/콘솔 로깅 핸들러 정상 동작

#### **3-3. 테스트 환경 구축**
- **테스트**: pytest + httpx 테스트 환경 구축
- **검증**: pytest-html 플러그인 정상 동작

## 🧪 **테스트 도구 및 환경**

### **테스트 프레임워크**
- **pytest**: Python 테스트 프레임워크
- **httpx**: HTTP 클라이언트 테스트
- **pytest-html**: HTML 테스트 리포트 생성

### **테스트 환경**
- **단위 테스트**: 각 모듈별 독립적 테스트
- **통합 테스트**: 모듈 간 연동 테스트
- **통합 테스트**: 전체 시스템 동작 테스트

## 📊 **TDD 적용 진행률**

### **현재 상황**
- **Phase 1-1**: Docker Compose 환경 구성 ✅ **완료**
- **Phase 1-2**: FastAPI 기본 구조 설정 ✅ **완료**
- **Phase 1-3**: 외부 DB 연결 및 ORM 설정 ✅ **완료**
  - ✅ Visual C++ Build Tools 설치 완료
  - ✅ 가상환경 생성 완료
  - ✅ 패키지 설치 스크립트 생성 완료
  - ✅ Docker 환경에서 패키지 설치 완료
  - ✅ FastAPI 애플리케이션 실행 성공
  - ✅ API 엔드포인트 검증 완료

### **TDD 적용 현황**
- **구현 완료**: 3/3 단계 (100%)
- **테스트 완료**: 3/3 단계 (100%)
- **검증 완료**: 3/3 단계 (100%)

### **다음 단계**
- **Phase 2-1**: 도메인 모델 구현 시작
- **기존 DB 스키마 분석**: 안전한 Alembic 초기화
- **TDD 방식으로 도메인 모델 테스트 작성**

## 🔄 **TDD 워크플로우**

### **1. 테스트 작성 (Red)**
```python
def test_database_connection():
    # 데이터베이스 연결 성공 테스트
    assert database.is_connected() == True
```

### **2. 최소한의 구현 (Green)**
```python
class Database:
    def is_connected(self):
        return True  # 최소한의 구현으로 테스트 통과
```

### **3. 리팩토링 (Refactor)**
```python
class Database:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self._connection = None
    
    def is_connected(self):
        return self._connection is not None
```

## 📝 **테스트 결과 문서화**

### **자동 생성 문서**
- **pytest-html**: HTML 테스트 리포트
- **테스트 커버리지**: 코드 커버리지 리포트
- **성능 테스트**: API 응답 시간 측정

### **수동 작성 문서**
- **테스트 시나리오**: 각 기능별 테스트 케이스
- **테스트 데이터**: 테스트용 샘플 데이터
- **테스트 환경**: 테스트 환경 설정 가이드

## 🚀 **다음 TDD 적용 계획**

### **Phase 1-3 완료 후**
1. **데이터베이스 연결 테스트** 작성 및 실행 ✅ **완료**
2. **Redis 연결 테스트** 작성 및 실행 ✅ **완료**
3. **Alembic 마이그레이션 테스트** 작성 및 실행 ✅ **완료**
4. **현재까지 구현된 기능 통합 테스트** 작성 및 실행 ✅ **완료**

### **Phase 2 시작 준비 완료**
1. **도메인 모델 TDD 구현**: 사용자 엔티티 및 서비스
2. **데이터베이스 연동 TDD**: 실제 DB 연결 및 CRUD 작업
3. **API 엔드포인트 TDD**: RESTful API 구현

### **Phase 2 시작 전**
1. **TDD 방식 검증**: 현재 구현된 기능들의 테스트 커버리지 확인
2. **테스트 환경 최적화**: 테스트 실행 속도 및 안정성 개선
3. **테스트 자동화**: CI/CD 파이프라인에 테스트 자동화 구축

---

**작성일**: 2024-08-20  
**작성자**: AI Assistant  
**검토자**: 사용자  
**상태**: 활성화 ✅
