# 문제 분석 및 예방 정책

## 📋 **개요**
이 문서는 IoT Care Backend System에서 발생한 통합테스트와 수동테스트 결과 차이점을 분석하고, 향후 같은 문제를 방지하기 위한 정책을 정의합니다.

## 🚨 **발생한 문제**

### **문제 현상**
- **통합테스트 결과**: GET 메서드 100% 성공
- **수동 테스트 결과**: GET 메서드에서 PostgreSQL 오류 발생
- **오류 메시지**: `PostgreSQLDeviceRepository.__init__() takes 1 positional argument but 2 were given`

### **근본 원인 분석**

#### **1. 의존성 주입 불일치**
- **Container**: `PostgreSQLDeviceRepository(db_session)`로 세션 전달
- **Repository**: `__init__(self)`로 세션을 받지 않음
- **결과**: 생성자 호출 시 인자 개수 불일치 오류

#### **2. 테스트 환경 차이**
- **통합테스트**: Mock 객체나 다른 Repository 구현체 사용 가능성
- **수동 테스트**: 실제 Container와 Repository 연결
- **결과**: 실제 환경에서만 오류 발생

#### **3. 코드 일관성 부족**
- 일부 Repository는 올바르게 구현 (`PostgreSQLUserRepository`)
- 일부 Repository는 잘못 구현 (`PostgreSQLDeviceRepository`)
- **결과**: 일관되지 않은 의존성 주입 패턴

## 🔧 **해결 방법**

### **1. Repository 생성자 수정**
```python
# 수정 전
def __init__(self):
    pass

# 수정 후
def __init__(self, db_session: AsyncSession):
    self.db_session = db_session
```

### **2. 세션 관리 방식 통일**
```python
# 수정 전
async def _get_session(self) -> AsyncSession:
    return await get_session()

# 수정 후
async def _get_session(self) -> AsyncSession:
    return self.db_session
```

### **3. Container와 Repository 간 인터페이스 일치**
- 모든 Repository가 동일한 생성자 시그니처 사용
- 세션 주입 패턴 통일
- 의존성 주입 컨테이너와 Repository 구현체 간 일관성 보장

## 🛡️ **예방 정책**

### **1. 코드 리뷰 체크리스트**
- [ ] Repository 생성자가 `db_session: AsyncSession` 매개변수 받음
- [ ] `_get_session` 메서드가 주입된 세션 사용
- [ ] Container의 Repository 생성 호출과 Repository 생성자 시그니처 일치
- [ ] 모든 Repository가 동일한 패턴 사용

### **2. 테스트 전략 개선**
- **단위 테스트**: 각 Repository의 생성자와 메서드 개별 테스트
- **통합 테스트**: 실제 Container와 Repository 연결 테스트
- **수동 테스트**: 실제 API 엔드포인트 호출 테스트
- **테스트 환경**: Mock 객체와 실제 객체 모두 테스트

### **3. 개발 가이드라인**
- Repository 구현 시 반드시 `db_session: AsyncSession` 매개변수 받기
- 세션 관리 방식 통일 (주입된 세션 사용)
- Container와 Repository 간 인터페이스 일치 확인
- 코드 일관성 검증 자동화 도구 사용

### **4. 품질 관리 프로세스**
- **코드 리뷰**: 의존성 주입 패턴 일관성 검증
- **정적 분석**: 타입 체크 및 인터페이스 일치 검증
- **테스트 커버리지**: 실제 환경과 테스트 환경 모두 커버
- **문서화**: Repository 구현 패턴 표준화

## 📊 **영향받는 컴포넌트**

### **수정 완료**
- ✅ `PostgreSQLDeviceRepository`: 생성자에 `db_session` 매개변수 추가

### **검증 필요**
- 🔍 모든 Repository 클래스의 생성자 시그니처 확인
- 🔍 Container와 Repository 간 인터페이스 일치 확인
- 🔍 세션 관리 방식 통일성 검증

## 🎯 **향후 개선 계획**

### **단기 (1-2주)**
1. 모든 Repository 클래스 생성자 시그니처 검증
2. 의존성 주입 패턴 일관성 확보
3. 테스트 환경과 실제 환경 일치성 검증

### **중기 (1개월)**
1. 자동화된 코드 품질 검증 도구 도입
2. Repository 구현 패턴 표준화 문서 작성
3. 개발자 교육 및 가이드라인 공유

### **장기 (3개월)**
1. 지속적 통합/배포(CI/CD) 파이프라인에 품질 검증 단계 추가
2. 코드 리뷰 프로세스 표준화
3. 품질 메트릭 모니터링 및 개선

## 📚 **참고 자료**
- [FastAPI Dependency Injection](https://fastapi.tiangolo.com/tutorial/dependencies/)
- [SQLAlchemy AsyncSession](https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html)
- [Clean Architecture Principles](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)

## 📅 **문서 정보**
- **작성일**: 2025-08-22
- **작성자**: AI Assistant
- **검토자**: 개발팀
- **버전**: 1.0.0
- **상태**: 활성

