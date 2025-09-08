# TDD 및 Clean Architecture 개발 방법론 가이드

## 🎯 **개요**

이 문서는 IoT Care App 프로젝트에서 적용하고 있는 TDD(Test-Driven Development)와 Clean Architecture 개발 방법론에 대한 상세한 가이드입니다. 빠른 개발과 코드 품질 향상을 위한 실용적인 접근 방법을 제시합니다.

## 🧪 **TDD (Test-Driven Development) 방법론**

### **TDD의 핵심 원칙**
1. **Red-Green-Refactor 사이클**: 실패하는 테스트 작성 → 최소 구현 → 리팩토링
2. **테스트 우선**: 모든 기능에 대한 테스트 코드를 먼저 작성
3. **점진적 개발**: 작은 단위로 테스트하고 구현하여 안전하게 개발
4. **지속적 피드백**: 빠른 피드백을 통한 문제점 조기 발견

### **TDD 개발 사이클**

#### **1단계: Red (실패하는 테스트 작성)**
```python
# test_home_state_snapshot.py
def test_alert_level_calculation():
    """경보 레벨 계산 로직 테스트"""
    snapshot = HomeStateSnapshot(
        time=datetime.now(),
        user_id="test_user",
        alert_level="Normal"
    )
    
    # 위험 상황 시뮬레이션
    snapshot.kitchen_mq5_gas_ppm = 1000  # 위험 수준
    snapshot.bedroom_pir_motion = True    # 움직임 감지
    
    # 경보 레벨이 자동으로 업데이트되어야 함
    assert snapshot.alert_level == "Warning"
    assert "가스 농도 위험" in snapshot.alert_reason
```

#### **2단계: Green (최소 구현으로 테스트 통과)**
```python
# home_state_snapshot.py
class HomeStateSnapshot:
    def __init__(self, time, user_id, alert_level="Normal"):
        self.time = time
        self.user_id = user_id
        self.alert_level = alert_level
        self.alert_reason = ""
        self.kitchen_mq5_gas_ppm = 0
        self.bedroom_pir_motion = False
    
    def update_alert_level(self):
        """센서 데이터 기반 경보 레벨 자동 업데이트"""
        if self.kitchen_mq5_gas_ppm > 500:
            self.alert_level = "Warning"
            self.alert_reason = "가스 농도 위험"
        elif self.bedroom_pir_motion and self.alert_level == "Normal":
            self.alert_level = "Attention"
            self.alert_reason = "침실 움직임 감지"
```

#### **3단계: Refactor (코드 품질 향상)**
```python
# home_state_snapshot.py (리팩토링 후)
class HomeStateSnapshot:
    ALERT_THRESHOLDS = {
        'gas_warning': 500,
        'gas_emergency': 1000,
        'sound_warning': 80,
        'sound_emergency': 100
    }
    
    def __init__(self, time, user_id, alert_level="Normal"):
        self.time = time
        self.user_id = user_id
        self.alert_level = alert_level
        self.alert_reason = ""
        self._initialize_sensors()
    
    def _initialize_sensors(self):
        """센서 데이터 초기화"""
        self.kitchen_mq5_gas_ppm = 0
        self.bedroom_pir_motion = False
        self.livingroom_sound_db = 0
    
    def update_alert_level(self):
        """센서 데이터 기반 경보 레벨 자동 업데이트"""
        self._check_gas_levels()
        self._check_motion_patterns()
        self._check_sound_levels()
    
    def _check_gas_levels(self):
        """가스 농도 기반 경보 확인"""
        if self.kitchen_mq5_gas_ppm > self.ALERT_THRESHOLDS['gas_emergency']:
            self._set_alert("Emergency", "가스 농도 긴급 위험")
        elif self.kitchen_mq5_gas_ppm > self.ALERT_THRESHOLDS['gas_warning']:
            self._set_alert("Warning", "가스 농도 위험")
    
    def _set_alert(self, level, reason):
        """경보 설정"""
        self.alert_level = level
        self.alert_reason = reason
```

### **TDD 적용 시나리오**

#### **시나리오 1: 새로운 API 엔드포인트 개발**
```python
# 1. 테스트 작성
def test_create_home_state_snapshot():
    """홈 상태 스냅샷 생성 API 테스트"""
    client = TestClient(app)
    
    snapshot_data = {
        "time": "2025-08-23T15:00:00Z",
        "user_id": "test_user",
        "entrance_pir_motion": True,
        "kitchen_mq5_gas_ppm": 100
    }
    
    response = client.post("/api/home-state-snapshots/create", json=snapshot_data)
    
    assert response.status_code == 201
    assert response.json()["user_id"] == "test_user"
    assert response.json()["alert_level"] == "Normal"

# 2. 최소 구현
@router.post("/create", response_model=HomeStateSnapshotResponse)
async def create_home_state_snapshot(
    snapshot_data: HomeStateSnapshotCreate,
    snapshot_service: IHomeStateSnapshotService = Depends(get_home_state_snapshot_service)
):
    return await snapshot_service.create_snapshot(snapshot_data)

# 3. 리팩토링 및 검증
```

#### **시나리오 2: 비즈니스 로직 개발**
```python
# 1. 테스트 작성
def test_priority_sorting_by_alert_level():
    """경보 레벨별 우선순위 정렬 테스트"""
    snapshots = [
        HomeStateSnapshot(time=datetime.now(), user_id="user1", alert_level="Normal"),
        HomeStateSnapshot(time=datetime.now(), user_id="user2", alert_level="Emergency"),
        HomeStateSnapshot(time=datetime.now(), user_id="user3", alert_level="Warning"),
        HomeStateSnapshot(time=datetime.now(), user_id="user4", alert_level="Attention")
    ]
    
    sorted_snapshots = sort_by_priority(snapshots)
    
    assert sorted_snapshots[0].alert_level == "Emergency"
    assert sorted_snapshots[1].alert_level == "Warning"
    assert sorted_snapshots[2].alert_level == "Attention"
    assert sorted_snapshots[3].alert_level == "Normal"

# 2. 최소 구현
def sort_by_priority(snapshots):
    """경보 레벨별 우선순위 정렬"""
    priority_order = {"Emergency": 0, "Warning": 1, "Attention": 2, "Normal": 3}
    return sorted(snapshots, key=lambda x: priority_order.get(x.alert_level, 4))

# 3. 리팩토링 및 성능 최적화
```

## 🏗️ **Clean Architecture 적용**

### **Clean Architecture의 핵심 원칙**
1. **의존성 규칙**: 외부 계층이 내부 계층에 의존하지 않음
2. **계층 분리**: 각 계층은 명확한 책임과 경계를 가짐
3. **테스트 용이성**: 비즈니스 로직을 독립적으로 테스트 가능
4. **프레임워크 독립성**: 특정 프레임워크에 종속되지 않음

### **4계층 구조**

#### **1. Presentation Layer (표현 계층)**
```python
# app/api/v1/home_state_snapshots.py
@router.get("/{user_id}/latest", response_model=HomeStateSnapshotResponse)
async def get_latest_snapshot(
    user_id: str = Path(..., description="사용자 ID"),
    snapshot_service: IHomeStateSnapshotService = Depends(get_home_state_snapshot_service)
):
    """사용자의 최신 홈 상태 스냅샷 조회"""
    try:
        snapshot = await snapshot_service.get_latest_snapshot(user_id)
        if not snapshot:
            raise HTTPException(status_code=404, detail="스냅샷을 찾을 수 없습니다")
        return snapshot
    except Exception as e:
        logger.error(f"스냅샷 조회 실패: {e}")
        raise HTTPException(status_code=500, detail="내부 서버 오류")
```

#### **2. Use Cases Layer (유스케이스 계층)**
```python
# app/use_cases/home_state_snapshot_service.py
class HomeStateSnapshotService(IHomeStateSnapshotService):
    def __init__(self, snapshot_repository: IHomeStateSnapshotRepository):
        self._repository = snapshot_repository
    
    async def get_latest_snapshot(self, user_id: str) -> Optional[HomeStateSnapshotResponse]:
        """사용자의 최신 홈 상태 스냅샷 조회"""
        # 비즈니스 로직: 권한 확인, 데이터 검증 등
        if not self._validate_user_access(user_id):
            raise ValueError("사용자 접근 권한이 없습니다")
        
        # 도메인 엔티티 조회
        snapshot_entity = await self._repository.get_latest_snapshot(user_id)
        
        if not snapshot_entity:
            return None
        
        # 응답 모델로 변환
        return HomeStateSnapshotResponse.from_orm(snapshot_entity)
    
    def _validate_user_access(self, user_id: str) -> bool:
        """사용자 접근 권한 검증"""
        # 실제 구현에서는 JWT 토큰이나 세션 정보를 확인
        return True
```

#### **3. Repository Interface Layer (리포지토리 인터페이스 계층)**
```python
# app/interfaces/repositories/home_state_snapshot_repository.py
class IHomeStateSnapshotRepository(ABC):
    """홈 상태 스냅샷 리포지토리 인터페이스"""
    
    @abstractmethod
    async def get_latest_snapshot(self, user_id: str) -> Optional[HomeStateSnapshot]:
        """사용자의 최신 스냅샷 조회"""
        pass
    
    @abstractmethod
    async def create_snapshot(self, snapshot: HomeStateSnapshot) -> HomeStateSnapshot:
        """새로운 스냅샷 생성"""
        pass
    
    @abstractmethod
    async def get_snapshots_by_time_range(
        self, 
        user_id: str, 
        start_time: datetime, 
        end_time: datetime
    ) -> List[HomeStateSnapshot]:
        """시간 범위별 스냅샷 조회"""
        pass
```

#### **4. Infrastructure Layer (인프라 계층)**
```python
# app/infrastructure/repositories/home_state_snapshot_repository.py
class HomeStateSnapshotRepository(IHomeStateSnapshotRepository):
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_latest_snapshot(self, user_id: str) -> Optional[HomeStateSnapshot]:
        """사용자의 최신 스냅샷 조회"""
        query = select(HomeStateSnapshotModel).where(
            HomeStateSnapshotModel.user_id == user_id
        ).order_by(HomeStateSnapshotModel.time.desc()).limit(1)
        
        result = self.db.execute(query)
        db_model = result.scalar_one_or_none()
        
        if not db_model:
            return None
        
        # ORM 모델을 도메인 엔티티로 변환
        return self._to_domain_entity(db_model)
    
    def _to_domain_entity(self, db_model: HomeStateSnapshotModel) -> HomeStateSnapshot:
        """ORM 모델을 도메인 엔티티로 변환"""
        return HomeStateSnapshot(
            time=db_model.time,
            user_id=db_model.user_id,
            entrance_pir_motion=db_model.entrance_pir_motion,
            entrance_rfid_status=db_model.entrance_rfid_status,
            entrance_reed_is_closed=db_model.entrance_reed_is_closed,
            livingroom_pir_1_motion=db_model.livingroom_pir_1_motion,
            livingroom_pir_2_motion=db_model.livingroom_pir_2_motion,
            livingroom_sound_db=db_model.livingroom_sound_db,
            livingroom_mq7_co_ppm=db_model.livingroom_mq7_co_ppm,
            livingroom_button_state=db_model.livingroom_button_state,
            kitchen_pir_motion=db_model.kitchen_pir_motion,
            kitchen_sound_db=db_model.kitchen_sound_db,
            kitchen_mq5_gas_ppm=db_model.kitchen_mq5_gas_ppm,
            kitchen_loadcell_1_kg=db_model.kitchen_loadcell_1_kg,
            kitchen_loadcell_2_kg=db_model.kitchen_loadcell_2_kg,
            kitchen_button_state=db_model.kitchen_button_state,
            kitchen_buzzer_is_on=db_model.kitchen_buzzer_is_on,
            bedroom_pir_motion=db_model.bedroom_pir_motion,
            bedroom_sound_db=db_model.bedroom_sound_db,
            bedroom_mq7_co_ppm=db_model.bedroom_mq7_co_ppm,
            bedroom_loadcell_kg=db_model.bedroom_loadcell_kg,
            bedroom_button_state=db_model.bedroom_button_state,
            bathroom_pir_motion=db_model.bathroom_pir_motion,
            bathroom_sound_db=db_model.bathroom_sound_db,
            bathroom_temp_celsius=db_model.bathroom_temp_celsius,
            bathroom_button_state=db_model.bathroom_button_state,
            detected_activity=db_model.detected_activity,
            alert_level=db_model.alert_level,
            alert_reason=db_model.alert_reason,
            action_log=db_model.action_log,
            extra_data=db_model.extra_data
        )
```

### **의존성 주입 (Dependency Injection)**

#### **Container 설정**
```python
# app/core/container.py
class Container:
    def __init__(self):
        self._repositories = {}
        self._services = {}
    
    def get_home_state_snapshot_repository(self, db: AsyncSession) -> IHomeStateSnapshotRepository:
        """홈 상태 스냅샷 리포지토리 의존성 주입"""
        if 'home_state_snapshot_repository' not in self._repositories:
            self._repositories['home_state_snapshot_repository'] = HomeStateSnapshotRepository(db)
        return self._repositories['home_state_snapshot_repository']
    
    def get_home_state_snapshot_service(self, db: AsyncSession) -> IHomeStateSnapshotService:
        """홈 상태 스냅샷 서비스 의존성 주입"""
        if 'home_state_snapshot_service' not in self._services:
            repository = self.get_home_state_snapshot_repository(db)
            self._services['home_state_snapshot_service'] = HomeStateSnapshotService(repository)
        return self._services['home_state_snapshot_service']

# 전역 컨테이너 인스턴스
container = Container()

# 의존성 주입 함수
def get_home_state_snapshot_service(db: AsyncSession = Depends(get_db)) -> IHomeStateSnapshotService:
    return container.get_home_state_snapshot_service(db)
```

## 📊 **테스트 전략 및 커버리지**

### **테스트 피라미드**

#### **1. 단위 테스트 (Unit Tests) - 70%**
```python
# test_domain_entities.py
class TestHomeStateSnapshot:
    def test_alert_level_calculation(self):
        """경보 레벨 계산 로직 테스트"""
        snapshot = HomeStateSnapshot(
            time=datetime.now(),
            user_id="test_user"
        )
        
        # 가스 농도 위험 상황
        snapshot.kitchen_mq5_gas_ppm = 1000
        snapshot.update_alert_level()
        
        assert snapshot.alert_level == "Warning"
        assert "가스 농도 위험" in snapshot.alert_reason
    
    def test_motion_pattern_detection(self):
        """움직임 패턴 감지 로직 테스트"""
        snapshot = HomeStateSnapshot(
            time=datetime.now(),
            user_id="test_user"
        )
        
        # 여러 센서에서 동시 움직임 감지
        snapshot.entrance_pir_motion = True
        snapshot.livingroom_pir_1_motion = True
        snapshot.kitchen_pir_motion = True
        
        activity = snapshot.detect_activity()
        assert activity == "사용자 이동 중"
```

#### **2. 통합 테스트 (Integration Tests) - 20%**
```python
# test_repository_integration.py
class TestHomeStateSnapshotRepository:
    @pytest.mark.asyncio
    async def test_create_and_retrieve_snapshot(self, db_session):
        """스냅샷 생성 및 조회 통합 테스트"""
        repository = HomeStateSnapshotRepository(db_session)
        
        # 테스트 데이터 생성
        snapshot = HomeStateSnapshot(
            time=datetime.now(),
            user_id="test_user",
            alert_level="Normal"
        )
        
        # 저장
        created_snapshot = await repository.create_snapshot(snapshot)
        assert created_snapshot.user_id == "test_user"
        
        # 조회
        retrieved_snapshot = await repository.get_latest_snapshot("test_user")
        assert retrieved_snapshot is not None
        assert retrieved_snapshot.alert_level == "Normal"
```

#### **3. API 테스트 (API Tests) - 10%**
```python
# test_api_endpoints.py
class TestHomeStateSnapshotsAPI:
    def test_create_snapshot_endpoint(self, client):
        """스냅샷 생성 API 엔드포인트 테스트"""
        snapshot_data = {
            "time": "2025-08-23T15:00:00Z",
            "user_id": "test_user",
            "entrance_pir_motion": True,
            "kitchen_mq5_gas_ppm": 100
        }
        
        response = client.post("/api/home-state-snapshots/create", json=snapshot_data)
        
        assert response.status_code == 201
        assert response.json()["user_id"] == "test_user"
        assert response.json()["alert_level"] == "Normal"
    
    def test_get_snapshots_by_user(self, client):
        """사용자별 스냅샷 조회 API 테스트"""
        response = client.get("/api/home-state-snapshots/user/test_user")
        
        assert response.status_code == 200
        assert isinstance(response.json(), list)
```

### **테스트 커버리지 목표**
- **전체 코드**: 70% 이상
- **도메인 로직**: 90% 이상
- **리포지토리 계층**: 80% 이상
- **서비스 계층**: 85% 이상
- **API 계층**: 75% 이상

## 🚀 **빠른 개발을 위한 TDD 팁**

### **1. 작은 단위로 시작**
```python
# 너무 큰 테스트를 피하고 작은 단위로 분할
def test_alert_level_enum_values():
    """경보 레벨 enum 값 검증"""
    assert AlertLevel.NORMAL == "Normal"
    assert AlertLevel.ATTENTION == "Attention"
    assert AlertLevel.WARNING == "Warning"
    assert AlertLevel.EMERGENCY == "Emergency"

def test_alert_level_priority_order():
    """경보 레벨 우선순위 순서 검증"""
    levels = [AlertLevel.NORMAL, AlertLevel.ATTENTION, AlertLevel.WARNING, AlertLevel.EMERGENCY]
    assert levels == sorted(levels, key=lambda x: AlertLevel.get_priority(x))
```

### **2. Mock 활용으로 외부 의존성 격리**
```python
# test_service_with_mock.py
@patch('app.use_cases.home_state_snapshot_service.HomeStateSnapshotRepository')
def test_get_latest_snapshot_with_mock(self, mock_repository):
    """Mock을 활용한 서비스 테스트"""
    # Mock 설정
    mock_repo_instance = mock_repository.return_value
    mock_repo_instance.get_latest_snapshot.return_value = None
    
    # 서비스 테스트
    service = HomeStateSnapshotService(mock_repo_instance)
    result = service.get_latest_snapshot("test_user")
    
    assert result is None
    mock_repo_instance.get_latest_snapshot.assert_called_once_with("test_user")
```

### **3. 테스트 데이터 팩토리 활용**
```python
# test_factories.py
class HomeStateSnapshotFactory:
    @staticmethod
    def create_normal_snapshot(user_id: str = "test_user") -> HomeStateSnapshot:
        return HomeStateSnapshot(
            time=datetime.now(),
            user_id=user_id,
            alert_level="Normal"
        )
    
    @staticmethod
    def create_warning_snapshot(user_id: str = "test_user") -> HomeStateSnapshot:
        snapshot = HomeStateSnapshotFactory.create_normal_snapshot(user_id)
        snapshot.kitchen_mq5_gas_ppm = 1000
        snapshot.alert_level = "Warning"
        snapshot.alert_reason = "가스 농도 위험"
        return snapshot

# 테스트에서 활용
def test_alert_level_escalation(self):
    """경보 레벨 상승 로직 테스트"""
    normal_snapshot = HomeStateSnapshotFactory.create_normal_snapshot()
    warning_snapshot = HomeStateSnapshotFactory.create_warning_snapshot()
    
    assert normal_snapshot.alert_level == "Normal"
    assert warning_snapshot.alert_level == "Warning"
```

## 📝 **개발 워크플로우**

### **일일 TDD 사이클**
1. **오전 (9:00-10:00)**: 일일 계획 수립 및 테스트 시나리오 정의
2. **오전 (10:00-12:00)**: Red-Green-Refactor 사이클로 기능 개발
3. **오후 (2:00-4:00)**: 통합 테스트 및 API 테스트 실행
4. **오후 (4:00-6:00)**: 테스트 커버리지 확인 및 리팩토링

### **주간 개발 사이클**
1. **월요일**: 주간 목표 설정 및 테스트 계획 수립
2. **수요일**: 중간 진행 상황 점검 및 테스트 결과 분석
3. **금요일**: 주간 완료 작업 리뷰 및 다음 주 테스트 계획 수립

### **커밋 규칙 (Conventional Commits)**
```
test: 테스트 코드 추가/수정
feat: 새로운 기능 추가
fix: 버그 수정
refactor: 코드 리팩토링
docs: 문서 수정
style: 코드 스타일 변경
chore: 빌드 프로세스 또는 보조 도구 변경
```

## 🎯 **성공 지표 및 모니터링**

### **코드 품질 지표**
- **테스트 커버리지**: 70% 이상 유지
- **코드 복잡도**: 순환 복잡도 10 이하
- **중복 코드**: 5% 이하
- **코드 스멜**: 0개

### **개발 생산성 지표**
- **기능 완성도**: 계획된 기능의 90% 이상 완성
- **버그 발생률**: 기능당 버그 0.1개 이하
- **리팩토링 빈도**: 주 1회 이상
- **테스트 실행 시간**: 전체 테스트 5분 이내

---

## 🔗 **관련 문서 및 크로스 레퍼런스**

### **📊 프로젝트 현황 관련**
- [[../current-development-status.md]] - 전체 프로젝트 상태 및 완성도
- [[../work-log.md]] - 개발 작업 로그 및 히스토리
- [[../checklist.md]] - 프로젝트 체크리스트

### **🧪 테스트 관련**
- [[../testing-scenarios/bootstrap_dashboard_test_scenarios.md]] - TDD 테스트 시나리오
- [[../testing-results/]] - 테스트 결과 데이터
- [[../tdd-implementation-plan.md]] - TDD 구현 계획
- [[../api-integration-test-checklist.md]] - API 통합 테스트

### **🔧 개발 가이드라인**
- [[../development-guidelines.md]] - 개발 가이드라인
- [[../api-endpoint-management-guidelines.md]] - API 관리 가이드
- [[../ai-agent-work-guidelines.md]] - AI 에이전트 협업 가이드

### **📱 애플리케이션 개발**
- [[../backend-apis/current-status.md]] - 백엔드 API 현황
- [[../flutter-user-app/development-overview.md]] - Flutter 앱 개발 현황
- [[../flutter-user-app-context.md]] - Flutter 앱 컨텍스트

---

## 🏷️ **태그 및 분류**

#개발방법론 #TDD #CleanArchitecture #테스트주도개발 #아키텍처 #의존성주입 #리팩토링 #품질관리 #코드품질 #테스트커버리지

---

## 📝 **변경 사항 히스토리**

### **v1.1 (2025-08-27) - 크로스 레퍼런스 시스템 구축**
- ✅ **새로운 기능**: Obsidian 스타일 위키 링크 시스템 추가
- ✅ **크로스 레퍼런스**: 관련 문서 섹션 및 상호 링크 구현
- ✅ **태그 시스템**: 문서 분류 및 검색을 위한 태그 추가
- ✅ **문서 연결성**: 프로젝트 전체 문서와의 연결성 강화

### **v1.0 (2025-08-23) - 초기 개발 방법론 문서 생성**
- ✅ **기본 구조**: TDD 및 Clean Architecture 개발 방법론 가이드 문서화
- ✅ **TDD 가이드**: Red-Green-Refactor 사이클 및 테스트 전략
- ✅ **Clean Architecture**: 4계층 구조 및 의존성 규칙
- ✅ **개발 워크플로우**: 일일/주간 개발 사이클 및 커밋 규칙

---

**문서 버전**: 1.1 (크로스 레퍼런스 추가)  
**작성일**: 2025-08-23  
**최종 업데이트**: 2025-08-27  
**작성자**: AI Assistant  
**프로젝트**: TDD 및 Clean Architecture 개발 방법론 가이드
