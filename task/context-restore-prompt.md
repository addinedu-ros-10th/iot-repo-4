# 작업 컨텍스트 복구 프롬프트

## 🚀 **빠른 작업 재개를 위한 프롬프트 메시지**

프로그램 재실행 시 아래 프롬프트를 복사하여 붙여넣으면 즉시 작업 컨텍스트를 복구할 수 있습니다.

---

## 📋 **기본 컨텍스트 복구 프롬프트**

```
현재 IoT Care Backend System 개발 작업을 진행하고 있습니다.

## 🎯 **현재 목표**
통합 테스트 API 100% 성공률 달성을 위해 Raw 센서 API 문제 해결을 완료하고, Edge 센서 및 Actuator API 문제를 해결해야 합니다.

## ✅ **완료된 작업**
1. **환경 설정**: DB 연결, 환경변수 파일(.env.*), Docker Compose 설정 완료
2. **순환 참조 문제**: Lazy loading 패턴으로 해결 완료
3. **Raw 센서 API**: MQ5, MQ7, RFID, Sound, TCRT5000, Ultrasonic API 문제 해결 완료 (100%)

## 🔄 **진행 중인 작업**
Edge 센서 및 Actuator API의 `422 Validation Error: field required` 문제 해결

## ❌ **해결해야 할 문제**
- **Edge 센서 API**: Flame, PIR, Reed, Tilt (4개)
- **Actuator API**: Buzzer, IRTX, Relay, Servo (4개)
- **문제**: 필수 필드 누락 또는 스키마 불일치

## 📁 **작업 디렉토리**
services/was-server

## 🔧 **해결 방법 패턴 (Raw 센서에서 확립)**
1. 스키마 정의 확인 (Create, Update, Response)
2. Pydantic 설정 (`orm_mode = True`)
3. SQLAlchemy 실행 (`await` 제거)
4. ORM 변환 (`from_orm` 사용)
5. Import 수정 (새로운 스키마 이름 사용)

현재 상황을 파악하고 다음 단계 작업을 진행해주세요.
```

---

## 🎯 **상세 작업 컨텍스트 복구 프롬프트**

```
현재 IoT Care Backend System 개발 작업을 진행하고 있습니다.

## 📊 **전체 진행률**
- **목표**: 통합 테스트 API 100% 성공률 달성
- **현재 진행률**: 60% (Raw 센서 API 문제 해결 완료)
- **남은 작업**: Edge 센서 및 Actuator API 문제 해결

## ✅ **완료된 작업 상세**

### 1. 환경 설정 및 인프라 문제 해결
- DB 연결 문제: 외부 DB 연결 설정 완료 (DB_HOST: 192.168.0.15)
- 환경변수 파일: `env.*` → `.env.*` 파일로 변경 완료
- Docker Compose: 캐시 제거 및 재빌드 완료
- 데이터베이스 스키마: Alembic을 통한 마이그레이션 완료

### 2. 순환 참조(Circular Import) 문제 해결
- 문제: `app.core.container` 모듈 초기화 시 순환 참조 발생
- 해결: Lazy loading 패턴 적용으로 repository/service import 지연
- 파일: `app/core/container.py` 수정 완료

### 3. Raw 센서 API 문제 해결 (100% 완료)
- MQ5 API: ✅ 정상 동작 확인
- MQ7 API: ✅ 문제 해결 완료
- RFID API: ✅ 문제 해결 완료
- Sound API: ✅ 문제 해결 완료
- TCRT5000 API: ✅ 문제 해결 완료
- Ultrasonic API: ✅ 문제 해결 완료

#### 해결된 문제들:
1. `object ChunkedIteratorResult can't be used in 'await' expression`
   - 원인: SQLAlchemy v2에서 `result.scalars().all()` 사용 시 발생
   - 해결: `await` 제거 및 `from_orm` 사용

2. `type object has no attribute 'from_attributes'`
   - 원인: Pydantic v1에서 `from_attributes` 메서드 부재
   - 해결: `from_orm` 사용 및 `orm_mode = True` 설정

3. `cannot import name 'SensorRawXXXUpdate'`
   - 원인: Raw 센서 Update 스키마 정의 누락
   - 해결: 모든 Raw 센서에 Update 스키마 추가

4. 스키마 불일치 문제
   - 원인: 이전 스키마 이름(`MQ5DataCreate` 등) 사용
   - 해결: 새로운 Raw 센서 스키마(`SensorRawMQ5Create` 등) 사용

## 🔄 **진행 중인 작업**
- 현재 단계: Raw 센서 API 문제 해결 완료
- 다음 단계: Edge 센서 및 Actuator API 문제 해결

## ❌ **해결해야 할 문제**

### Edge 센서 및 Actuator API 문제
- 문제: `422 Validation Error: field required`
- 원인: 필수 필드 누락 또는 스키마 불일치
- 영향: Edge 센서 및 Actuator 데이터 생성/수정 실패

#### 영향받는 API들:
- Edge 센서: Flame, PIR, Reed, Tilt API
- Actuator: Buzzer, IRTX, Relay, Servo API

## 📁 **수정 완료된 파일 목록**

### 스키마 파일
- ✅ `app/api/v1/schemas.py` - Raw 센서 스키마 완성

### 리포지토리 파일
- ✅ `app/infrastructure/repositories/mq5_repository.py`
- ✅ `app/infrastructure/repositories/mq7_repository.py`
- ✅ `app/infrastructure/repositories/rfid_repository.py`
- ✅ `app/infrastructure/repositories/sound_repository.py`
- ✅ `app/infrastructure/repositories/tcrt5000_repository.py`
- ✅ `app/infrastructure/repositories/ultrasonic_repository.py`

### 서비스 파일
- ✅ `app/use_cases/mq5_service.py`
- ✅ `app/use_cases/mq7_service.py`
- ✅ `app/use_cases/rfid_service.py`
- ✅ `app/use_cases/sound_service.py`
- ✅ `app/use_cases/tcrt5000_service.py`
- ✅ `app/use_cases/ultrasonic_service.py`

### API 파일
- ✅ `app/api/v1/mq5.py`
- ✅ `app/api/v1/mq7.py`
- ✅ `app/api/v1/rfid.py`
- ✅ `app/api/v1/sound.py`
- ✅ `app/api/v1/tcrt5000.py`
- ✅ `app/api/v1/ultrasonic.py`

## 🎯 **다음 단계 목표**
1. **Edge 센서 API 문제 해결**
   - 필수 필드 누락 문제 파악
   - 스키마 불일치 문제 해결
   - API 정상 동작 확인

2. **Actuator API 문제 해결**
   - 필수 필드 누락 문제 파악
   - 스키마 불일치 문제 해결
   - API 정상 동작 확인

3. **통합 테스트 100% 성공률 달성**
   - 모든 API 엔드포인트 정상 동작 확인
   - POST/GET/PUT/DELETE 메서드 정상 동작 확인

## 🔧 **기술적 인사이트**
1. **Pydantic 버전 호환성**: v1에서는 `from_orm`, v2에서는 `model_validate` 사용
2. **SQLAlchemy 비동기 처리**: `execute()`는 비동기이지만 결과 객체는 동기적으로 처리
3. **스키마 일관성**: 모든 Raw 센서는 동일한 패턴(`time`, `device_id`, `raw_payload`) 사용
4. **환경변수 관리**: `.env.*` 파일 사용으로 Docker 환경에서 안정적 동작

## 📝 **최근 작업 로그**
- 2025-08-22 11:30: Raw 센서 API 문제 해결 완료
- 2025-08-22 11:00: MQ5 API 정상 동작 확인
- 2025-08-22 10:30: 스키마 import 문제 해결
- 2025-08-22 10:00: Pydantic 호환성 문제 해결
- 2025-08-22 09:30: SQLAlchemy 비동기 실행 문제 해결

현재 상황을 파악하고 Edge 센서 및 Actuator API 문제 해결을 진행해주세요.
```

---

## 🚨 **긴급 상황 복구 프롬프트**

```
🚨 긴급 상황: IoT Care Backend System 개발 작업 중단

## 📍 **현재 위치**
- 작업 디렉토리: services/was-server
- 마지막 작업: Raw 센서 API 문제 해결 완료 (60% 진행률)
- 다음 작업: Edge 센서 및 Actuator API 문제 해결

## ⚡ **즉시 확인해야 할 사항**
1. Docker 컨테이너 상태: `docker-compose ps`
2. 서버 로그: `docker logs iot-care-app --tail 20`
3. API 상태: `curl http://localhost:8000/health`

## 🔄 **작업 재개 방법**
1. 위의 "상세 작업 컨텍스트 복구 프롬프트" 사용
2. 현재 상황 파악 후 다음 단계 진행
3. Edge 센서 API 문제 해결 시작

현재 상황을 파악하고 작업을 재개해주세요.
```

---

## 📚 **프롬프트 사용 가이드**

### 1. **기본 컨텍스트 복구**
- 프로그램 재실행 직후 사용
- 빠른 상황 파악 및 작업 재개

### 2. **상세 작업 컨텍스트 복구**
- 상세한 작업 내역 확인 필요 시 사용
- 전체 프로젝트 상황 파악 시 사용

### 3. **긴급 상황 복구**
- 예상치 못한 중단 상황 발생 시 사용
- 즉시 시스템 상태 확인 필요 시 사용

### 4. **프롬프트 선택 기준**
- **빠른 재개**: 기본 컨텍스트 복구
- **상세 확인**: 상세 작업 컨텍스트 복구
- **긴급 상황**: 긴급 상황 복구

---

## 💡 **효과적인 사용 팁**

1. **프롬프트 복사**: 전체 프롬프트를 복사하여 AI 도구에 붙여넣기
2. **상황별 선택**: 현재 상황에 맞는 프롬프트 선택
3. **단계별 진행**: 복구 후 단계별로 작업 진행
4. **문서 참조**: 필요 시 관련 개발 문서 참조

이 프롬프트들을 사용하여 언제든지 작업 컨텍스트를 빠르게 복구하고 작업을 이어갈 수 있습니다.

---

**마지막 업데이트**: 2025-08-22 11:30:00  
**현재 진행률**: 60% (Raw 센서 API 완료, Edge 센서 및 Actuator API 진행 중)
