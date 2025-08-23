# API 통합 테스트 문제 분석 및 해결 방안

**작성일**: 2025-08-22  
**마지막 업데이트**: 2025-08-22 11:30:00  
**프로젝트**: IoT Repository 4 - WAS Server  
**테스트 실행일**: 2025-08-23 01:47:38

## 📊 **테스트 결과 요약**

### **전체 현황**
- **전체 API 수**: 17개
- **성공한 API 수**: 0개
- **실패한 API 수**: 17개
- **성공률**: 0.0%

### **테스트 시나리오**
각 API에 대해 8단계 테스트 진행:
1. GET 초기 → 2. POST 생성 → 3. GET 생성후 → 4. PUT 수정 → 5. GET 수정후 → 6. DELETE → 7. GET 삭제후 → 8. POST 신규생성

---

## 🚨 **발견된 문제 목록**

### **1. 데이터베이스 연결 문제 (우선순위: 높음)**

#### **문제 현황**
- **증상**: `[Errno 111] Connection refused` 또는 `connection to server at "192.168.0.2", port 15432 failed: Connection refused`
- **영향**: Users API, CDS API, LoadCell API, MQ5 API, MQ7 API
- **원인**: 데이터베이스 서버 연결 실패

#### **문제 세부사항**
```
Users API: [Errno 111] Connection refused
CDS API: [Errno 111] Connection refused  
LoadCell API: [Errno 111] Connection refused
MQ5 API: connection to server at "192.168.0.2", port 15432 failed: Connection refused
MQ7 API: connection to server at "192.168.0.2", port 15432 failed: Connection refused
```

#### **해결 방안**
1. **데이터베이스 서버 상태 확인**: 외부 PostgreSQL 서버 실행 상태 점검
2. **네트워크 연결 확인**: 방화벽, 포트 설정, 네트워크 연결 상태 확인
3. **환경변수 검증**: `.env.local` 파일의 DB_HOST, DB_PORT 설정 확인
4. **데이터베이스 서버 재시작**: 필요시 외부 데이터베이스 서버 재시작

---

### **2. Raw 센서 API 스키마 불일치 문제 (우선순위: 높음)**

#### **문제 현황**
- **증상**: `'SensorRawXXXCreate' object has no attribute '필드명'`
- **영향**: RFID API, Sound API, TCRT5000 API, Ultrasonic API
- **원인**: 테스트 데이터와 API 스키마 간 필드명 불일치

#### **문제 세부사항**
```
RFID API: 'SensorRawRFIDCreate' object has no attribute 'card_id'
Sound API: 'SensorRawSoundCreate' object has no attribute 'db_value'
TCRT5000 API: 'SensorRawTCRT5000Create' object has no attribute 'analog_value'
Ultrasonic API: 'SensorRawUltrasonicCreate' object has no attribute 'distance_cm'
```

#### **해결 방안**
1. **스키마 검증**: `app/api/v1/schemas.py`에서 Raw 센서 스키마 필드명 확인
2. **테스트 데이터 수정**: 통합 테스트 스크립트의 테스트 데이터를 실제 스키마에 맞게 수정
3. **필드명 매핑**: ORM 모델과 API 스키마 간 필드명 일치성 확보
4. **스키마 업데이트**: 필요시 API 스키마를 테스트 데이터에 맞게 수정

---

### **3. Edge 센서 API 필수 필드 누락 문제 (우선순위: 중간)**

#### **문제 현황**
- **증상**: `422 Validation Error: Field required`
- **영향**: EdgeFlame API, EdgePIR API, EdgeReed API, EdgeTilt API
- **원인**: 테스트 데이터에 필수 필드 누락

#### **문제 세부사항**
```
EdgeFlame API: "flame_detected" 필드 누락
EdgePIR API: "motion_detected" 필드 누락
EdgeReed API: "switch_state" 필드 누락
EdgeTilt API: "tilt_detected" 필드 누락
```

#### **해결 방안**
1. **스키마 분석**: Edge 센서 API 스키마에서 필수 필드 확인
2. **테스트 데이터 수정**: 필수 필드를 포함한 테스트 데이터 생성
3. **스키마 검증**: Pydantic 스키마의 필수 필드 설정 확인
4. **데이터 구조 일치**: 테스트 데이터와 API 스키마 간 구조 일치성 확보

---

### **4. Actuator API 필수 필드 누락 문제 (우선순위: 중간)**

#### **문제 현황**
- **증상**: `422 Validation Error: Field required`
- **영향**: ActuatorBuzzer API, ActuatorIRTX API, ActuatorRelay API, ActuatorServo API
- **원인**: 테스트 데이터에 필수 필드 누락

#### **문제 세부사항**
```
ActuatorBuzzer API: "buzzer_type", "state" 필드 누락
ActuatorIRTX API: "command_hex" 필드 누락
ActuatorRelay API: "channel", "state" 필드 누락
ActuatorServo API: "channel" 필드 누락
```

#### **해결 방안**
1. **스키마 분석**: Actuator API 스키마에서 필수 필드 확인
2. **테스트 데이터 수정**: 필수 필드를 포함한 테스트 데이터 생성
3. **스키마 검증**: Pydantic 스키마의 필수 필드 설정 확인
4. **데이터 구조 일치**: 테스트 데이터와 API 스키마 간 구조 일치성 확보

---

## 🎯 **해결 우선순위 및 계획**

### **Phase 1: 데이터베이스 연결 문제 해결 (즉시 해결 필요)**
**예상 시간**: 1-2시간
1. **데이터베이스 서버 상태 확인**
   - 외부 PostgreSQL 서버 실행 상태 점검
   - 네트워크 연결 및 포트 설정 확인
2. **환경변수 설정 검증**
   - `.env.local` 파일의 DB_HOST, DB_PORT 설정 확인
   - 데이터베이스 연결 문자열 검증
3. **연결 테스트**
   - 데이터베이스 서버 직접 연결 테스트
   - 애플리케이션에서 데이터베이스 연결 테스트

### **Phase 2: Raw 센서 API 스키마 불일치 문제 해결 (1-2시간)**
**예상 시간**: 1-2시간
1. **스키마 분석**
   - `app/api/v1/schemas.py`에서 Raw 센서 스키마 필드명 확인
   - ORM 모델과 API 스키마 간 필드명 비교
2. **테스트 데이터 수정**
   - 통합 테스트 스크립트의 테스트 데이터를 실제 스키마에 맞게 수정
   - 필드명 불일치 해결
3. **스키마 일치성 확보**
   - 필요시 API 스키마를 테스트 데이터에 맞게 수정
   - 일관된 필드명 사용

### **Phase 3: Edge 센서 및 Actuator API 필수 필드 문제 해결 (2-3시간)**
**예상 시간**: 2-3시간
1. **스키마 분석**
   - Edge 센서 및 Actuator API 스키마에서 필수 필드 확인
   - Pydantic 스키마의 필수 필드 설정 확인
2. **테스트 데이터 수정**
   - 필수 필드를 포함한 테스트 데이터 생성
   - 데이터 구조와 API 스키마 간 일치성 확보
3. **스키마 검증**
   - 모든 필수 필드가 포함된 테스트 데이터로 검증
   - 422 Validation Error 해결

### **Phase 4: 통합 테스트 재실행 및 검증 (1-2시간)**
**예상 시간**: 1-2시간
1. **수정된 코드로 통합 테스트 재실행**
   - 모든 API 엔드포인트 정상 동작 확인
   - POST/GET/PUT/DELETE 메서드 정상 동작 확인
2. **성공률 확인**
   - 목표: 100% 성공률 달성
   - 추가 문제 발생 시 즉시 해결
3. **최종 검증**
   - 모든 API의 CRUD 작업 정상 동작 확인
   - 성능 및 안정성 검증

---

## 🔧 **구체적인 해결 방법**

### **1. 데이터베이스 연결 문제 해결**

#### **환경변수 확인**
```bash
# .env.local 파일 확인
cat .env.local

# 데이터베이스 연결 테스트
psql -h 192.168.0.15 -p 15432 -U username -d database_name
```

#### **Docker 컨테이너 재시작**
```bash
# 컨테이너 재시작
docker-compose down
docker-compose up -d

# 로그 확인
docker logs iot-care-app
```

### **2. 스키마 불일치 문제 해결**

#### **스키마 파일 확인**
```bash
# 스키마 파일 내용 확인
cat app/api/v1/schemas.py | grep -A 10 "SensorRaw"
```

#### **테스트 데이터 수정**
통합 테스트 스크립트의 테스트 데이터를 실제 스키마에 맞게 수정:
- RFID API: `card_id` → `card_type`
- Sound API: `db_value` → `analog_value`
- TCRT5000 API: `analog_value` → `digital_value`
- Ultrasonic API: `distance_cm` → `raw_value`

### **3. 필수 필드 누락 문제 해결**

#### **Edge 센서 API 테스트 데이터 수정**
```json
{
  "time": "2025-08-23T01:47:32.869951",
  "device_id": "test_device_001",
  "raw_value": 100.0,
  "unit": "test_unit",
  "status": "normal",
  "flame_detected": true,  // EdgeFlame API
  "motion_detected": true, // EdgePIR API
  "switch_state": "closed", // EdgeReed API
  "tilt_detected": false,  // EdgeTilt API
  "raw_payload": {"test": "data"}
}
```

#### **Actuator API 테스트 데이터 수정**
```json
{
  "time": "2025-08-23T01:47:35.604963",
  "device_id": "test_device_001",
  "raw_value": 100.0,
  "unit": "test_unit",
  "status": "normal",
  "buzzer_type": "piezo",     // ActuatorBuzzer API
  "state": "on",              // ActuatorBuzzer API
  "command_hex": "FF00",      // ActuatorIRTX API
  "channel": 1,               // ActuatorRelay/Servo API
  "raw_payload": {"test": "data"}
}
```

---

## 📋 **해결 체크리스트**

### **Phase 1: 데이터베이스 연결 문제 해결**
- [ ] 외부 PostgreSQL 서버 실행 상태 확인
- [ ] 네트워크 연결 및 포트 설정 확인
- [ ] `.env.local` 파일의 DB_HOST, DB_PORT 설정 검증
- [ ] 데이터베이스 서버 직접 연결 테스트
- [ ] 애플리케이션에서 데이터베이스 연결 테스트

### **Phase 2: Raw 센서 API 스키마 불일치 문제 해결**
- [ ] `app/api/v1/schemas.py`에서 Raw 센서 스키마 필드명 확인
- [ ] ORM 모델과 API 스키마 간 필드명 비교
- [ ] 통합 테스트 스크립트의 테스트 데이터 수정
- [ ] 필드명 불일치 해결
- [ ] 스키마 일치성 확보

### **Phase 3: Edge 센서 및 Actuator API 필수 필드 문제 해결**
- [ ] Edge 센서 및 Actuator API 스키마에서 필수 필드 확인
- [ ] Pydantic 스키마의 필수 필드 설정 확인
- [ ] 필수 필드를 포함한 테스트 데이터 생성
- [ ] 데이터 구조와 API 스키마 간 일치성 확보
- [ ] 422 Validation Error 해결

### **Phase 4: 통합 테스트 재실행 및 검증**
- [ ] 수정된 코드로 통합 테스트 재실행
- [ ] 모든 API 엔드포인트 정상 동작 확인
- [ ] POST/GET/PUT/DELETE 메서드 정상 동작 확인
- [ ] 100% 성공률 달성
- [ ] 최종 검증 완료

---

## 🚀 **예상 결과**

### **해결 완료 후 기대 성과**
- **데이터베이스 연결**: 모든 API에서 정상적인 데이터베이스 연결
- **스키마 일치성**: 테스트 데이터와 API 스키마 간 완벽한 일치
- **필수 필드**: 모든 필수 필드가 포함된 테스트 데이터로 검증 통과
- **통합 테스트**: 100% 성공률 달성
- **API 안정성**: 모든 CRUD 작업의 안정적인 동작

### **전체 진행률 목표**
- **현재**: 0% (모든 API 실패)
- **Phase 1 완료 후**: 30% (데이터베이스 연결 문제 해결)
- **Phase 2 완료 후**: 60% (Raw 센서 API 문제 해결)
- **Phase 3 완료 후**: 90% (Edge 센서 및 Actuator API 문제 해결)
- **Phase 4 완료 후**: 100% (통합 테스트 완료)

---

**마지막 업데이트**: 2025-08-22 11:30:00  
**다음 검토 예정**: 데이터베이스 연결 문제 해결 완료 후
