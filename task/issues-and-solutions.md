# 문제 및 해결책

## 🔴 **해결된 문제들**

### 1. 순환 참조(Circular Import) 문제 ✅ 해결됨
- **문제**: `ImportError: cannot import name 'container' from partially initialized module 'app.core.container'`
- **원인**: `app.core.container` 모듈 초기화 시 순환 참조 발생
- **해결**: Lazy loading 패턴 적용으로 repository/service import 지연
- **파일**: `app/core/container.py`
- **상태**: ✅ 완료

### 2. SQLAlchemy 비동기 실행 문제 ✅ 해결됨
- **문제**: `object ChunkedIteratorResult can't be used in 'await' expression`
- **원인**: SQLAlchemy v2에서 `result.scalars().all()` 사용 시 발생
- **해결**: `await` 제거 및 `from_orm` 사용
- **파일**: 모든 Raw 센서 리포지토리 파일
- **상태**: ✅ 완료

### 3. Pydantic 호환성 문제 ✅ 해결됨
- **문제**: `type object has no attribute 'from_attributes'`
- **원인**: Pydantic v1에서 `from_attributes` 메서드 부재
- **해결**: `from_orm` 사용 및 `orm_mode = True` 설정
- **파일**: `app/api/v1/schemas.py`
- **상태**: ✅ 완료

### 4. Raw 센서 Update 스키마 누락 문제 ✅ 해결됨
- **문제**: `cannot import name 'SensorRawXXXUpdate' from 'app.api.v1.schemas'`
- **원인**: Raw 센서 Update 스키마 정의 누락
- **해결**: 모든 Raw 센서에 Update 스키마 추가
- **파일**: `app/api/v1/schemas.py`
- **상태**: ✅ 완료

### 5. 스키마 불일치 문제 ✅ 해결됨
- **문제**: 이전 스키마 이름(`MQ5DataCreate` 등) 사용으로 인한 import 오류
- **원인**: 새로운 Raw 센서 스키마(`SensorRawMQ5Create` 등)와 불일치
- **해결**: 모든 서비스 파일에서 새로운 스키마 이름 사용
- **파일**: 모든 Raw 센서 서비스 파일
- **상태**: ✅ 완료

## 🟡 **진행 중인 문제들**

### 1. Edge 센서 및 Actuator API 필수 필드 문제 🔄 진행 중
- **문제**: `422 Validation Error: field required`
- **원인**: 필수 필드 누락 또는 스키마 불일치
- **영향**: Edge 센서 및 Actuator 데이터 생성/수정 실패
- **상태**: 🔄 진행 중
- **예상 완료**: 오후 작업 중

#### 영향받는 API들:
- **Edge 센서**: Flame, PIR, Reed, Tilt
- **Actuator**: Buzzer, IRTX, Relay, Servo

## 🔵 **해결 방법 패턴**

### Raw 센서 API 문제 해결 패턴
1. **스키마 정의 확인**: Create, Update, Response 스키마 모두 존재하는지 확인
2. **Pydantic 설정**: `orm_mode = True` 설정으로 Pydantic v1 호환성 확보
3. **SQLAlchemy 실행**: `await` 제거로 결과 객체 즉시 반환
4. **ORM 변환**: `from_orm` 사용으로 SQLAlchemy 모델을 Pydantic 모델로 변환
5. **Import 수정**: 모든 파일에서 새로운 스키마 이름 사용

### 적용된 파일들
- **스키마**: `app/api/v1/schemas.py`
- **리포지토리**: 6개 Raw 센서 리포지토리 파일
- **서비스**: 6개 Raw 센서 서비스 파일
- **API**: 6개 Raw 센서 API 파일

## 📊 **문제 해결 현황**

| 문제 유형 | 총 문제 수 | 해결됨 | 진행 중 | 미해결 |
|-----------|------------|--------|----------|--------|
| 순환 참조 | 1 | 1 | 0 | 0 |
| SQLAlchemy | 6 | 6 | 0 | 0 |
| Pydantic | 6 | 6 | 0 | 0 |
| 스키마 누락 | 5 | 5 | 0 | 0 |
| 스키마 불일치 | 6 | 6 | 0 | 0 |
| 필수 필드 | 8 | 0 | 8 | 0 |
| **총계** | **32** | **24** | **8** | **0** |

## 🎯 **다음 단계 목표**

### 1. Edge 센서 API 문제 해결
- **목표**: 4개 Edge 센서 API 정상 동작
- **예상 시간**: 2-3시간
- **방법**: Raw 센서와 동일한 패턴 적용

### 2. Actuator API 문제 해결
- **목표**: 4개 Actuator API 정상 동작
- **예상 시간**: 2-3시간
- **방법**: Raw 센서와 동일한 패턴 적용

### 3. 통합 테스트 100% 성공률 달성
- **목표**: 모든 API 엔드포인트 정상 동작
- **예상 시간**: 1-2시간
- **방법**: 전체 API 테스트 및 검증

## 🔧 **기술적 인사이트**

### 1. Pydantic 버전 호환성
- **v1**: `from_orm`, `orm_mode = True`
- **v2**: `model_validate`, `from_attributes = True`

### 2. SQLAlchemy 비동기 처리
- `execute()`는 비동기이지만 결과 객체는 동기적으로 처리
- `await`의 적절한 사용 위치 파악 필요

### 3. 스키마 일관성
- 모든 Raw 센서는 동일한 패턴(`time`, `device_id`, `raw_payload`) 사용
- 일관된 스키마 구조로 유지보수성 향상

### 4. 환경변수 관리
- `.env.*` 파일 사용으로 Docker 환경에서 안정적 동작
- 환경별 설정 분리로 개발/운영 환경 구분

---

**마지막 업데이트**: 2025-08-22 11:30:00  
**다음 검토 예정**: Edge 센서 및 Actuator API 문제 해결 완료 후
