# 개발 지침 (Development Guidelines)

## 🎯 **개발 원칙**

### **Clean Architecture 원칙 (절대 준수 필수)**
- 도메인 중심의 계층화된 아키텍처 유지
- 의존성 역전 원칙 준수
- 인터페이스와 구현체 분리
- **🚨 절대 위배 금지: API 레이어에서 직접 Infrastructure 레이어 접근 금지**

### **TDD (Test-Driven Development)**
- 테스트 코드를 먼저 작성
- 리팩토링을 통한 코드 품질 향상
- 지속적인 테스트 실행

## 🚨 **중요: Clean Architecture 준수 지침**

### **절대 위배 금지 사항**
1. **API 레이어에서 직접 ORM 모델 사용 금지**
   ```python
   # ❌ 잘못된 방식 (절대 금지)
   from app.infrastructure.models import SensorRawLoadCell
   
   @router.post("/")
   async def create_data(data: DataCreate, db: AsyncSession = Depends(get_db)):
       db_data = SensorRawLoadCell(**data.dict())  # 직접 ORM 모델 사용
       db.add(db_data)
       await db.commit()
   
   # ✅ 올바른 방식 (반드시 준수)
   from app.interfaces.services.sensor_service_interface import ISensorService
   
   @router.post("/")
   async def create_data(data: DataCreate, sensor_service: ISensorService = Depends(get_sensor_service)):
       created_data = await sensor_service.create_sensor_data(data)  # 서비스 레이어 사용
       return created_data
   ```

2. **API 레이어에서 직접 데이터베이스 세션 사용 금지**
   ```python
   # ❌ 잘못된 방식 (절대 금지)
   async def get_data(db: AsyncSession = Depends(get_db)):
       query = select(SensorRawLoadCell)
       result = await db.execute(query)
   
   # ✅ 올바른 방식 (반드시 준수)
   async def get_data(sensor_service: ISensorService = Depends(get_sensor_service)):
       data = await sensor_service.get_sensor_data()
       return data
   ```

3. **비즈니스 로직을 API 레이어에 구현 금지**
   ```python
   # ❌ 잘못된 방식 (절대 금지)
   @router.get("/stats")
   async def get_stats(device_id: str, db: AsyncSession = Depends(get_db)):
       # API 레이어에서 직접 통계 계산
       query = select(SensorRawLoadCell).where(SensorRawLoadCell.device_id == device_id)
       result = await db.execute(query)
       data_list = result.scalars().all()
       
       # 통계 계산 로직이 API에 존재
       weight_data = [d.weight_kg for d in data_list if d.weight_kg is not None]
       avg = sum(weight_data) / len(weight_data) if weight_data else 0
   
   # ✅ 올바른 방식 (반드시 준수)
   @router.get("/stats")
   async def get_stats(device_id: str, sensor_service: ISensorService = Depends(get_sensor_service)):
       # 서비스 레이어에서 통계 계산
       stats = await sensor_service.get_sensor_statistics(device_id)
       return stats
   ```

### **Clean Architecture 레이어 구조 (반드시 준수)**
```
API Layer (app/api/)
├── 라우터 정의
├── 요청/응답 스키마 검증
└── 서비스 레이어 호출만 수행

Use Cases Layer (app/use_cases/)
├── 비즈니스 로직 구현
├── 도메인 서비스 조합
└── 트랜잭션 관리

Domain Layer (app/domain/)
├── 엔티티 정의
├── 도메인 서비스
└── 비즈니스 규칙

Interfaces Layer (app/interfaces/)
├── 리포지토리 인터페이스
├── 서비스 인터페이스
└── 외부 서비스 인터페이스

Infrastructure Layer (app/infrastructure/)
├── ORM 모델
├── 데이터베이스 연결
└── 외부 서비스 구현체
```

### **의존성 주입 패턴 (반드시 준수)**
```python
# 1. 인터페이스 정의
class ISensorService(ABC):
    @abstractmethod
    async def create_sensor_data(self, data: SensorDataCreate) -> SensorDataResponse:
        pass

# 2. 구현체 생성
class SensorService(ISensorService):
    def __init__(self, sensor_repository: ISensorRepository):
        self.sensor_repository = sensor_repository
    
    async def create_sensor_data(self, data: SensorDataCreate) -> SensorDataResponse:
        # 비즈니스 로직 구현
        pass

# 3. 컨테이너에 등록
def get_sensor_service() -> ISensorService:
    return container.get_sensor_service()

# 4. API에서 사용
@router.post("/")
async def create_data(
    data: SensorDataCreate,
    sensor_service: ISensorService = Depends(get_sensor_service)
):
    return await sensor_service.create_sensor_data(data)
```

## 🚨 **현재 발생한 문제점과 해결 방안**

### **문제점**
1. **센서 API들이 Clean Architecture 원칙 위배**
   - LoadCell, MQ5, MQ7, RFID, Sound, TCRT5000, Ultrasonic API
   - API 레이어에서 직접 ORM 모델 사용
   - 비즈니스 로직이 API 레이어에 구현됨

2. **의존성 역전 원칙 위배**
   - API가 Infrastructure 레이어에 직접 의존
   - 테스트 어려움 및 코드 재사용성 저하

### **해결 방안**
1. **즉시 리팩토링 진행**
   - 센서별 리포지토리 인터페이스 생성
   - 센서별 서비스 인터페이스 생성
   - API 레이어에서 서비스 레이어 호출로 변경

2. **새로운 API 구현 시 Clean Architecture 준수**
   - Edge 센서 API (4개)
   - Actuator 로그 API (4개)

3. **기존 API 점진적 리팩토링**
   - Users, Devices, Sensors API는 이미 준수
   - 나머지 센서 API들 단계적 리팩토링

## 🚨 **중요: 파일 경로 관리 지침**

### **절대 경로 사용 원칙**
- **모든 파일 생성 시 절대 경로 사용 필수**
- **상대 경로 사용 금지** (경로 오류 발생 원인)
- **올바른 경로 형식**: `services/was-server/app/...`

### **작업 디렉토리 확인 절차**
파일/디렉토리 생성 명령어 실행 전 **반드시** 다음 절차 수행:

1. **현재 위치 확인**
   ```bash
   pwd
   ```

2. **작업 디렉토리 확인**
   ```bash
   ls -la
   ```

3. **필요시 올바른 디렉토리로 이동**
   ```bash
   cd services/was-server
   ```

4. **경로 확인 후 명령어 실행**
   ```bash
   mkdir -p app/api/v1
   ```

### **파일 생성 시 경로 검증**
- `edit_file` 도구 사용 시 **절대 경로** 명시
- 파일 생성 후 `find` 명력으로 실제 위치 확인
- 잘못된 위치 발견 시 즉시 정리

### **잘못된 경로 문제 해결 방안**
1. **즉시 정리**: 잘못 생성된 파일들 삭제
2. **절대 경로 재생성**: 올바른 위치에 파일 재생성
3. **경로 검증**: 생성된 파일 위치 재확인

## 🔧 **개발 환경 설정**

### **Docker 환경**
- Docker Compose를 통한 일관된 개발 환경
- 볼륨 마운트를 통한 파일 동기화
- 컨테이너 재시작 시 파일 변경사항 반영

### **데이터베이스 연결**
- PostgreSQL 연결 시 비밀번호 특수문자 처리
- SSH 터널을 통한 안전한 데이터베이스 접근
- 환경 변수를 통한 설정 관리

## 📁 **프로젝트 구조 관리**

### **디렉토리 구조**
```
services/was-server/
├── app/                    # 메인 애플리케이션
│   ├── api/               # API 레이어 (라우터만)
│   ├── core/              # 핵심 설정
│   ├── domain/            # 도메인 레이어 (엔티티, 서비스)
│   ├── use_cases/         # 유스케이스 레이어 (비즈니스 로직)
│   ├── infrastructure/    # 인프라스트럭처 레이어 (ORM, DB)
│   └── interfaces/        # 인터페이스 레이어 (추상화)
├── tests/                 # 테스트 코드
└── alembic/               # 데이터베이스 마이그레이션
```

### **파일 명명 규칙**
- Python 파일: `snake_case.py`
- 클래스: `PascalCase`
- 함수/변수: `snake_case`
- 상수: `UPPER_SNAKE_CASE`

## 🧪 **테스트 지침**

### **테스트 작성 원칙**
- 각 도메인 엔티티별 단위 테스트
- 리포지토리 패턴 테스트
- 의존성 주입 시스템 테스트
- 통합 테스트를 통한 전체 시스템 검증

### **테스트 실행**
```bash
# 전체 테스트 실행
pytest

# 특정 테스트 파일 실행
pytest tests/core/test_container.py

# 상세 출력과 함께 실행
pytest -v
```

## 📝 **코드 품질**

### **코드 스타일**
- Black을 통한 코드 포맷팅
- Flake8을 통한 린팅
- MyPy를 통한 타입 체크

### **문서화**
- 모든 함수와 클래스에 docstring 작성
- 복잡한 로직에 주석 추가
- README 파일 최신 상태 유지

## 🚀 **배포 및 운영**

### **환경별 설정**
- `env.local`: 로컬 개발 환경
- `env.dev`: 개발 서버 환경
- `env.prod`: 운영 서버 환경

### **Docker 배포**
- 개발용: `docker-compose.dev.yml`
- 운영용: `docker-compose.prod.yml`
- 환경별 설정 파일 분리

## 🔍 **문제 해결 가이드**

### **자주 발생하는 문제**
1. **파일 경로 오류**: 절대 경로 사용으로 해결
2. **Docker 파일 동기화**: 볼륨 마운트 설정 확인
3. **데이터베이스 연결**: SSH 터널 및 환경 변수 확인
4. **모듈 임포트 오류**: Python 경로 및 패키지 구조 확인
5. **Clean Architecture 위배**: 인터페이스와 서비스 레이어 사용 필수

### **Clean Architecture 위배 시 해결 절차**
1. **문제 상황 파악**: API 레이어에서 직접 DB 접근 코드 식별
2. **인터페이스 생성**: 해당 도메인의 리포지토리/서비스 인터페이스 생성
3. **서비스 구현**: 비즈니스 로직을 서비스 레이어로 이동
4. **API 수정**: API 레이어에서 서비스 레이어 호출로 변경
5. **테스트 작성**: 새로운 구조에 대한 테스트 코드 작성
6. **검증**: Clean Architecture 원칙 준수 확인

## 📚 **참고 자료**

### **기술 문서**
- FastAPI 공식 문서
- SQLAlchemy 공식 문서
- Clean Architecture 원칙
- TDD 방법론

### **프로젝트 문서**
- `task/work-log.md`: 작업 진행 상황
- `task/checklist.md`: 요구사항 체크리스트
- `doc/project-structure.md`: 프로젝트 구조 설명

## ⚠️ **중요 경고**

**Clean Architecture 원칙을 위배하는 코드는 절대 작성하지 마세요!**

- API 레이어에서 직접 ORM 모델 사용 금지
- 비즈니스 로직을 API 레이어에 구현 금지
- 의존성 주입을 통한 인터페이스 사용 필수
- 모든 새로운 API는 이 지침을 준수하여 구현

**위배 시 즉시 리팩토링 진행 필수!**
