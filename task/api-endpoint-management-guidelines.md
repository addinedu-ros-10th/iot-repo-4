# API 엔드포인트 관리 지침

## 📋 **개요**
이 문서는 IoT Care Backend System의 API 엔드포인트 관리에 대한 지침을 정의합니다.

## 🎯 **목표**
- API 엔드포인트 중복 경로 방지
- ORM 기준 그룹화 관리
- 일관된 네이밍 규칙 적용
- 시스템 안정성 100% 달성

## 🏗️ **API 라우터 등록 구조**

### **기본 원칙**
1. **중복 prefix 방지**: `/api/v1/v1/...` 같은 중복 경로 금지
2. **ORM 기준 그룹화**: 데이터 모델별로 논리적 그룹화
3. **일관된 네이밍**: RESTful API 설계 원칙 준수

### **현재 구조**
```
app.include_router(api_router, prefix="/api")
```

### **API 그룹별 등록**
```python
# Users & Devices 그룹
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(devices.router, prefix="/devices", tags=["devices"])

# Raw 센서 데이터 그룹
api_router.include_router(cds.router, prefix="/cds", tags=["sensors"])
api_router.include_router(dht.router, prefix="/dht", tags=["sensors"])
api_router.include_router(flame.router, prefix="/flame", tags=["sensors"])
api_router.include_router(imu.router, prefix="/imu", tags=["sensors"])
api_router.include_router(loadcell.router, prefix="/loadcell", tags=["sensors"])
api_router.include_router(mq5.router, prefix="/mq5", tags=["sensors"])
api_router.include_router(mq7.router, prefix="/mq7", tags=["sensors"])
api_router.include_router(rfid.router, prefix="/rfid", tags=["sensors"])
api_router.include_router(sound.router, prefix="/sound", tags=["sensors"])
api_router.include_router(tcrt5000.router, prefix="/tcrt5000", tags=["sensors"])
api_router.include_router(ultrasonic.router, prefix="/ultrasonic", tags=["sensors"])

# Edge 센서 그룹
api_router.include_router(edge_flame.router, prefix="/edge-flame", tags=["edge-sensors"])
api_router.include_router(edge_pir.router, prefix="/edge-pir", tags=["edge-sensors"])
api_router.include_router(edge_reed.router, prefix="/edge-reed", tags=["edge-sensors"])
api_router.include_router(edge_tilt.router, prefix="/edge-tilt", tags=["edge-sensors"])

# Actuator 로그 그룹
api_router.include_router(actuator_buzzer.router, prefix="/actuator-buzzer", tags=["actuators"])
api_router.include_router(actuator_irtx.router, prefix="/actuator-irtx", tags=["actuators"])
api_router.include_router(actuator_relay.router, prefix="/actuator-relay", tags=["actuators"])
api_router.include_router(actuator_servo.router, prefix="/actuator-servo", tags=["actuators"])

# DeviceRTCStatus 그룹
api_router.include_router(device_rtc.router, prefix="/device-rtc", tags=["device-status"])
```

## 🛣️ **API 경로 규칙**

### **최종 URL 구조**
- **Users API**: `/api/users`
- **LoadCell API**: `/api/loadcell`
- **MQ5 API**: `/api/mq5`
- **EdgeFlame API**: `/api/edge-flame`
- **ActuatorBuzzer API**: `/api/actuator-buzzer`

### **금지사항**
- ❌ `/api/v1/v1/users` (중복 prefix)
- ❌ `/api/v1/users` (불필요한 v1 prefix)
- ❌ `/users` (api prefix 누락)
- ❌ API 파일에서 `router = APIRouter(prefix="/...")` 설정 (중복 prefix 방지)
- ❌ API 라우터와 개별 API 파일에서 동시에 prefix 설정

## 🏷️ **태그 그룹화**

### **태그 분류**
- `["users"]`: 사용자 관련 API
- `["devices"]`: 디바이스 관련 API
- `["sensors"]`: 원시 센서 데이터 API
- `["edge-sensors"]`: Edge 센서 데이터 API
- `["actuators"]`: 액추에이터 로그 API
- `["device-status"]`: 디바이스 상태 API

## 📝 **개발 시 주의사항**

### **새로운 API 추가 시**
1. ORM 모델과 일치하는 prefix 사용
2. 적절한 태그 그룹 선택
3. 중복 경로 확인
4. **중복 prefix 방지**: API 파일에서 `prefix` 설정 금지, API 라우터에서만 설정
5. 통합테스트 스크립트 업데이트

### **기존 API 수정 시**
1. 경로 변경 시 통합테스트 스크립트 동기화
2. 태그 그룹 일관성 유지
3. 문서 업데이트

## 🔍 **검증 방법**

### **통합테스트**
- `python integration_test.py` 실행
- 모든 API 엔드포인트 100% 성공률 달성
- 경로 중복 확인

### **Swagger UI 확인**
- `http://localhost:8000/docs` 접근
- API 경로 구조 검증
- 태그 그룹화 확인

## 📚 **참고 자료**
- [FastAPI Router Documentation](https://fastapi.tiangolo.com/tutorial/bigger-applications/)
- [RESTful API Design Principles](https://restfulapi.net/)
- [Clean Architecture Principles](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)

## 📅 **최종 업데이트**
- **날짜**: 2025-08-22
- **버전**: 1.0.0
- **작성자**: AI Assistant
- **검토자**: 개발팀
