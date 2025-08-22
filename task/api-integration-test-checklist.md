# API 전체 통합 테스트 체크리스트

**작성일**: 2025-08-22  
**마지막 업데이트**: 2025-08-22 11:30:00  
**프로젝트**: IoT Repository 4 - WAS Server  
**테스트 목표**: 모든 API 엔드포인트 정상 동작 확인 및 100% 성공률 달성

## 📊 **테스트 개요**

### **테스트 시나리오**
각 API에 대해 다음 시나리오를 순차적으로 실행:
1. **GET 초기**: 초기 데이터 조회
2. **POST 생성**: 새 데이터 생성
3. **GET 생성후**: 생성된 데이터 조회
4. **PUT 수정**: 데이터 수정
5. **GET 수정후**: 수정된 데이터 조회
6. **DELETE**: 데이터 삭제
7. **GET 삭제후**: 삭제 후 데이터 상태 확인
8. **POST 신규생성**: 새로운 데이터 재생성

### **테스트 환경**
- **서버**: FastAPI (localhost:8000)
- **데이터베이스**: PostgreSQL (외부 연결)
- **Redis**: Docker 컨테이너
- **테스트 도구**: Python requests 또는 curl

---

## 🎯 **API 통합 테스트 체크리스트**

### **1. User API (1/1)**

#### **Users API** - `app/api/v1/users.py`
- [ ] **GET 초기**: `/api/users/list` - 사용자 목록 조회
- [ ] **POST 생성**: `/api/users/` - 새 사용자 생성
- [ ] **GET 생성후**: `/api/users/list` - 생성된 사용자 확인
- [ ] **PUT 수정**: `/api/users/{user_id}` - 사용자 정보 수정
- [ ] **GET 수정후**: `/api/users/{user_id}` - 수정된 정보 확인
- [ ] **DELETE**: `/api/users/{user_id}` - 사용자 삭제
- [ ] **GET 삭제후**: `/api/users/list` - 삭제 후 상태 확인
- [ ] **POST 신규생성**: `/api/users/` - 새로운 사용자 재생성

**상태**: 🔄 진행 중  
**문제**: 데이터 생성 실패 (상세 오류 미확인)

---

### **2. Raw 센서 API (6/6) ✅**

#### **LoadCell API** - `app/api/v1/loadcell.py` ✅
- [x] **GET 초기**: `/api/loadcell/list` - 무게 센서 데이터 목록 조회
- [x] **POST 생성**: `/api/loadcell/` - 새 무게 센서 데이터 생성
- [x] **GET 생성후**: `/api/loadcell/list` - 생성된 데이터 확인
- [x] **PUT 수정**: `/api/loadcell/{data_id}` - 데이터 수정
- [x] **GET 수정후**: `/api/loadcell/{data_id}` - 수정된 데이터 확인
- [x] **DELETE**: `/api/loadcell/{data_id}` - 데이터 삭제
- [x] **GET 삭제후**: `/api/loadcell/list` - 삭제 후 상태 확인
- [x] **POST 신규생성**: `/api/loadcell/` - 새로운 데이터 재생성

**상태**: ✅ 완료  
**문제**: 해결됨 (필드명 매핑 구현)

#### **MQ5 API** - `app/api/v1/mq5.py` ✅
- [x] **GET 초기**: `/api/mq5/list` - MQ5 센서 데이터 목록 조회
- [x] **POST 생성**: `/api/mq5/` - 새 MQ5 센서 데이터 생성
- [x] **GET 생성후**: `/api/mq5/list` - 생성된 데이터 확인
- [x] **PUT 수정**: `/api/mq5/{data_id}` - 데이터 수정
- [x] **GET 수정후**: `/api/mq5/{data_id}` - 수정된 데이터 확인
- [x] **DELETE**: `/api/mq5/{data_id}` - 데이터 삭제
- [x] **GET 삭제후**: `/api/mq5/list` - 삭제 후 상태 확인
- [x] **POST 신규생성**: `/api/mq5/` - 새로운 데이터 재생성

**상태**: ✅ 완료  
**문제**: 해결됨 (SQLAlchemy 비동기 실행 문제 해결)

#### **MQ7 API** - `app/api/v1/mq7.py` ✅
- [x] **GET 초기**: `/api/mq7/list` - MQ7 센서 데이터 목록 조회
- [x] **POST 생성**: `/api/mq7/` - 새 MQ7 센서 데이터 생성
- [x] **GET 생성후**: `/api/mq7/list` - 생성된 데이터 확인
- [x] **PUT 수정**: `/api/mq7/{data_id}` - 데이터 수정
- [x] **GET 수정후**: `/api/mq7/{data_id}` - 수정된 데이터 확인
- [x] **DELETE**: `/api/mq7/{data_id}` - 데이터 삭제
- [x] **GET 삭제후**: `/api/mq7/list` - 삭제 후 상태 확인
- [x] **POST 신규생성**: `/api/mq7/` - 새로운 데이터 재생성

**상태**: ✅ 완료  
**문제**: 해결됨 (Pydantic 호환성 문제 해결)

#### **RFID API** - `app/api/v1/rfid.py` ✅
- [x] **GET 초기**: `/api/rfid/list` - RFID 센서 데이터 목록 조회
- [x] **POST 생성**: `/api/rfid/` - 새 RFID 센서 데이터 생성
- [x] **GET 생성후**: `/api/rfid/list` - 생성된 데이터 확인
- [x] **PUT 수정**: `/api/rfid/{data_id}` - 데이터 수정
- [x] **GET 수정후**: `/api/rfid/{data_id}` - 수정된 데이터 확인
- [x] **DELETE**: `/api/rfid/{data_id}` - 데이터 삭제
- [x] **GET 삭제후**: `/api/rfid/list` - 삭제 후 상태 확인
- [x] **POST 신규생성**: `/api/rfid/` - 새로운 데이터 재생성

**상태**: ✅ 완료  
**문제**: 해결됨 (스키마 불일치 문제 해결)

#### **Sound API** - `app/api/v1/sound.py` ✅
- [x] **GET 초기**: `/api/sound/list` - Sound 센서 데이터 목록 조회
- [x] **POST 생성**: `/api/sound/` - 새 Sound 센서 데이터 생성
- [x] **GET 생성후**: `/api/sound/list` - 생성된 데이터 확인
- [x] **PUT 수정**: `/api/sound/{data_id}` - 데이터 수정
- [x] **GET 수정후**: `/api/sound/{data_id}` - 수정된 데이터 확인
- [x] **DELETE**: `/api/sound/{data_id}` - 데이터 삭제
- [x] **GET 삭제후**: `/api/sound/list` - 삭제 후 상태 확인
- [x] **POST 신규생성**: `/api/sound/` - 새로운 데이터 재생성

**상태**: ✅ 완료  
**문제**: 해결됨 (Update 스키마 누락 문제 해결)

#### **TCRT5000 API** - `app/api/v1/tcrt5000.py` ✅
- [x] **GET 초기**: `/api/tcrt5000/list` - TCRT5000 센서 데이터 목록 조회
- [x] **POST 생성**: `/api/tcrt5000/` - 새 TCRT5000 센서 데이터 생성
- [x] **GET 생성후**: `/api/tcrt5000/list` - 생성된 데이터 확인
- [x] **PUT 수정**: `/api/tcrt5000/{data_id}` - 데이터 수정
- [x] **GET 수정후**: `/api/tcrt5000/{data_id}` - 수정된 데이터 확인
- [x] **DELETE**: `/api/tcrt5000/{data_id}` - 데이터 삭제
- [x] **GET 삭제후**: `/api/tcrt5000/list` - 삭제 후 상태 확인
- [x] **POST 신규생성**: `/api/tcrt5000/` - 새로운 데이터 재생성

**상태**: ✅ 완료  
**문제**: 해결됨 (스키마 불일치 문제 해결)

#### **Ultrasonic API** - `app/api/v1/ultrasonic.py` ✅
- [x] **GET 초기**: `/api/ultrasonic/list` - Ultrasonic 센서 데이터 목록 조회
- [x] **POST 생성**: `/api/ultrasonic/` - 새 Ultrasonic 센서 데이터 생성
- [x] **GET 생성후**: `/api/ultrasonic/list` - 생성된 데이터 확인
- [x] **PUT 수정**: `/api/ultrasonic/{data_id}` - 데이터 수정
- [x] **GET 수정후**: `/api/ultrasonic/{data_id}` - 수정된 데이터 확인
- [x] **DELETE**: `/api/ultrasonic/{data_id}` - 데이터 삭제
- [x] **GET 삭제후**: `/api/ultrasonic/list` - 삭제 후 상태 확인
- [x] **POST 신규생성**: `/api/ultrasonic/` - 새로운 데이터 재생성

**상태**: ✅ 완료  
**문제**: 해결됨 (Update 스키마 누락 문제 해결)

---

### **3. Edge 센서 API (4/4) 🔄**

#### **EdgeFlame API** - `app/api/v1/edge_flame.py` 🔄
- [x] **GET 초기**: `/api/edge-flame/list` - Edge Flame 센서 데이터 목록 조회
- [ ] **POST 생성**: `/api/edge-flame/` - 새 Edge Flame 센서 데이터 생성
- [ ] **GET 생성후**: `/api/edge-flame/list` - 생성된 데이터 확인
- [ ] **PUT 수정**: `/api/edge-flame/{data_id}` - 데이터 수정
- [ ] **GET 수정후**: `/api/edge-flame/{data_id}` - 수정된 데이터 확인
- [ ] **DELETE**: `/api/edge-flame/{data_id}` - 데이터 삭제
- [ ] **GET 삭제후**: `/api/edge-flame/list` - 삭제 후 상태 확인
- [ ] **POST 신규생성**: `/api/edge-flame/` - 새로운 데이터 재생성

**상태**: 🔄 진행 중  
**문제**: `422 Validation Error: field required` - 필수 필드 누락

#### **EdgePIR API** - `app/api/v1/edge_pir.py` 🔄
- [x] **GET 초기**: `/api/edge-pir/list` - Edge PIR 센서 데이터 목록 조회
- [ ] **POST 생성**: `/api/edge-pir/` - 새 Edge PIR 센서 데이터 생성
- [ ] **GET 생성후**: `/api/edge-pir/list` - 생성된 데이터 확인
- [ ] **PUT 수정**: `/api/edge-pir/{data_id}` - 데이터 수정
- [ ] **GET 수정후**: `/api/edge-pir/{data_id}` - 수정된 데이터 확인
- [ ] **DELETE**: `/api/edge-pir/{data_id}` - 데이터 삭제
- [ ] **GET 삭제후**: `/api/edge-pir/list` - 삭제 후 상태 확인
- [ ] **POST 신규생성**: `/api/edge-pir/` - 새로운 데이터 재생성

**상태**: 🔄 진행 중  
**문제**: `422 Validation Error: field required` - `motion_detected` 필수 필드 누락

#### **EdgeReed API** - `app/api/v1/edge_reed.py` 🔄
- [x] **GET 초기**: `/api/edge-reed/list` - Edge Reed 센서 데이터 목록 조회
- [ ] **POST 생성**: `/api/edge-reed/` - 새 Edge Reed 센서 데이터 생성
- [ ] **GET 생성후**: `/api/edge-reed/list` - 생성된 데이터 확인
- [ ] **PUT 수정**: `/api/edge-reed/{data_id}` - 데이터 수정
- [ ] **GET 수정후**: `/api/edge-reed/{data_id}` - 수정된 데이터 확인
- [ ] **DELETE**: `/api/edge-reed/{data_id}` - 데이터 삭제
- [ ] **GET 삭제후**: `/api/edge-reed/list` - 삭제 후 상태 확인
- [ ] **POST 신규생성**: `/api/edge-reed/` - 새로운 데이터 재생성

**상태**: 🔄 진행 중  
**문제**: `422 Validation Error: field required` - `switch_state` 필수 필드 누락

#### **EdgeTilt API** - `app/api/v1/edge_tilt.py` 🔄
- [x] **GET 초기**: `/api/edge-tilt/list` - Edge Tilt 센서 데이터 목록 조회
- [ ] **POST 생성**: `/api/edge-tilt/` - 새 Edge Tilt 센서 데이터 생성
- [ ] **GET 생성후**: `/api/edge-tilt/list` - 생성된 데이터 확인
- [ ] **PUT 수정**: `/api/edge-tilt/{data_id}` - 데이터 수정
- [ ] **GET 수정후**: `/api/edge-tilt/{data_id}` - 수정된 데이터 확인
- [ ] **DELETE**: `/api/edge-tilt/{data_id}` - 데이터 삭제
- [ ] **GET 삭제후**: `/api/edge-tilt/list` - 삭제 후 상태 확인
- [ ] **POST 신규생성**: `/api/edge-tilt/` - 새로운 데이터 재생성

**상태**: 🔄 진행 중  
**문제**: `422 Validation Error: field required` - `tilt_detected` 필수 필드 누락

---

### **4. Actuator API (4/4) 🔄**

#### **ActuatorBuzzer API** - `app/api/v1/actuator_buzzer.py` 🔄
- [x] **GET 초기**: `/api/actuator-buzzer/list` - Actuator Buzzer 데이터 목록 조회
- [ ] **POST 생성**: `/api/actuator-buzzer/` - 새 Actuator Buzzer 데이터 생성
- [ ] **GET 생성후**: `/api/actuator-buzzer/list` - 생성된 데이터 확인
- [ ] **PUT 수정**: `/api/actuator-buzzer/{data_id}` - 데이터 수정
- [ ] **GET 수정후**: `/api/actuator-buzzer/{data_id}` - 수정된 데이터 확인
- [ ] **DELETE**: `/api/actuator-buzzer/{data_id}` - 데이터 삭제
- [ ] **GET 삭제후**: `/api/actuator-buzzer/list` - 삭제 후 상태 확인
- [ ] **POST 신규생성**: `/api/actuator-buzzer/` - 새로운 데이터 재생성

**상태**: 🔄 진행 중  
**문제**: `422 Validation Error: field required` - `buzzer_type`, `state` 필수 필드 누락

#### **ActuatorIRTX API** - `app/api/v1/actuator_irtx.py` 🔄
- [x] **GET 초기**: `/api/actuator-irtx/list` - Actuator IRTX 데이터 목록 조회
- [ ] **POST 생성**: `/api/actuator-irtx/` - 새 Actuator IRTX 데이터 생성
- [ ] **GET 생성후**: `/api/actuator-irtx/list` - 생성된 데이터 확인
- [ ] **PUT 수정**: `/api/actuator-irtx/{data_id}` - 데이터 수정
- [ ] **GET 수정후**: `/api/actuator-irtx/{data_id}` - 수정된 데이터 확인
- [ ] **DELETE**: `/api/actuator-irtx/{data_id}` - 데이터 삭제
- [ ] **GET 삭제후**: `/api/actuator-irtx/list` - 삭제 후 상태 확인
- [ ] **POST 신규생성**: `/api/actuator-irtx/` - 새로운 데이터 재생성

**상태**: 🔄 진행 중  
**문제**: `422 Validation Error: field required` - `command_hex` 필수 필드 누락

#### **ActuatorRelay API** - `app/api/v1/actuator_relay.py` 🔄
- [x] **GET 초기**: `/api/actuator-relay/list` - Actuator Relay 데이터 목록 조회
- [ ] **POST 생성**: `/api/actuator-relay/` - 새 Actuator Relay 데이터 생성
- [ ] **GET 생성후**: `/api/actuator-relay/list` - 생성된 데이터 확인
- [ ] **PUT 수정**: `/api/actuator-relay/{data_id}` - 데이터 수정
- [ ] **GET 수정후**: `/api/actuator-relay/{data_id}` - 수정된 데이터 확인
- [ ] **DELETE**: `/api/actuator-relay/{data_id}` - 데이터 삭제
- [ ] **GET 삭제후**: `/api/actuator-relay/list` - 삭제 후 상태 확인
- [ ] **POST 신규생성**: `/api/actuator-relay/` - 새로운 데이터 재생성

**상태**: 🔄 진행 중  
**문제**: `422 Validation Error: field required` - `channel`, `state` 필수 필드 누락

#### **ActuatorServo API** - `app/api/v1/actuator_servo.py` 🔄
- [x] **GET 초기**: `/api/actuator-servo/list` - Actuator Servo 데이터 목록 조회
- [ ] **POST 생성**: `/api/actuator-servo/` - 새 Actuator Servo 데이터 생성
- [ ] **GET 생성후**: `/api/actuator-servo/list` - 생성된 데이터 확인
- [ ] **PUT 수정**: `/api/actuator-servo/{data_id}` - 데이터 수정
- [ ] **GET 수정후**: `/api/actuator-servo/{data_id}` - 수정된 데이터 확인
- [ ] **DELETE**: `/api/actuator-servo/{data_id}` - 데이터 삭제
- [ ] **GET 삭제후**: `/api/actuator-servo/list` - 삭제 후 상태 확인
- [ ] **POST 신규생성**: `/api/actuator-servo/` - 새로운 데이터 재생성

**상태**: 🔄 진행 중  
**문제**: `422 Validation Error: field required` - `channel` 필수 필드 누락

---

### **5. 기타 센서 API (11/11)**

#### **CDS API** - `app/api/v1/cds.py`
- [x] **GET 초기**: `/api/cds/list` - CDS 센서 데이터 목록 조회
- [ ] **POST 생성**: `/api/cds/` - 새 CDS 센서 데이터 생성
- [ ] **GET 생성후**: `/api/cds/list` - 생성된 데이터 확인
- [ ] **PUT 수정**: `/api/cds/{data_id}` - 데이터 수정
- [ ] **GET 수정후**: `/api/cds/{data_id}` - 수정된 데이터 확인
- [ ] **DELETE**: `/api/cds/{data_id}` - 데이터 삭제
- [ ] **GET 삭제후**: `/api/cds/list` - 삭제 후 상태 확인
- [ ] **POST 신규생성**: `/api/cds/` - 새로운 데이터 재생성

**상태**: 🔄 진행 중  
**문제**: 데이터 생성 실패 (상세 오류 미확인)

#### **DHT API** - `app/api/v1/dht.py`
- [x] **GET 초기**: `/api/dht/list` - DHT 센서 데이터 목록 조회
- [ ] **POST 생성**: `/api/dht/` - 새 DHT 센서 데이터 생성
- [ ] **GET 생성후**: `/api/dht/list` - 생성된 데이터 확인
- [ ] **PUT 수정**: `/api/dht/{data_id}` - 데이터 수정
- [ ] **GET 수정후**: `/api/dht/{data_id}` - 수정된 데이터 확인
- [ ] **DELETE**: `/api/dht/{data_id}` - 데이터 삭제
- [ ] **GET 삭제후**: `/api/dht/list` - 삭제 후 상태 확인
- [ ] **POST 신규생성**: `/api/dht/` - 새로운 데이터 재생성

**상태**: 🔄 진행 중  
**문제**: 아직 테스트하지 않음

#### **IMU API** - `app/api/v1/imu.py`
- [x] **GET 초기**: `/api/imu/list` - IMU 센서 데이터 목록 조회
- [ ] **POST 생성**: `/api/imu/` - 새 IMU 센서 데이터 생성
- [ ] **GET 생성후**: `/api/imu/list` - 생성된 데이터 확인
- [ ] **PUT 수정**: `/api/imu/{data_id}` - 데이터 수정
- [ ] **GET 수정후**: `/api/imu/{data_id}` - 수정된 데이터 확인
- [ ] **DELETE**: `/api/imu/{data_id}` - 데이터 삭제
- [ ] **GET 삭제후**: `/api/imu/list` - 삭제 후 상태 확인
- [ ] **POST 신규생성**: `/api/imu/` - 새로운 데이터 재생성

**상태**: 🔄 진행 중  
**문제**: 아직 테스트하지 않음

#### **Flame API** - `app/api/v1/flame.py`
- [x] **GET 초기**: `/api/flame/list` - Flame 센서 데이터 목록 조회
- [ ] **POST 생성**: `/api/flame/` - 새 Flame 센서 데이터 생성
- [ ] **GET 생성후**: `/api/flame/list` - 생성된 데이터 확인
- [ ] **PUT 수정**: `/api/flame/{data_id}` - 데이터 수정
- [ ] **GET 수정후**: `/api/flame/{data_id}` - 수정된 데이터 확인
- [ ] **DELETE**: `/api/flame/{data_id}` - 데이터 삭제
- [ ] **GET 삭제후**: `/api/flame/list` - 삭제 후 상태 확인
- [ ] **POST 신규생성**: `/api/flame/` - 새로운 데이터 재생성

**상태**: 🔄 진행 중  
**문제**: 아직 테스트하지 않음

#### **Sensors API** - `app/api/v1/sensors.py`
- [x] **GET 초기**: `/api/sensors/list` - Sensors 데이터 목록 조회
- [ ] **POST 생성**: `/api/sensors/` - 새 Sensors 데이터 생성
- [ ] **GET 생성후**: `/api/sensors/list` - 생성된 데이터 확인
- [ ] **PUT 수정**: `/api/sensors/{data_id}` - 데이터 수정
- [ ] **GET 수정후**: `/api/sensors/{data_id}` - 수정된 데이터 확인
- [ ] **DELETE**: `/api/sensors/{data_id}` - 데이터 삭제
- [ ] **GET 삭제후**: `/api/sensors/list` - 삭제 후 상태 확인
- [ ] **POST 신규생성**: `/api/sensors/` - 새로운 데이터 재생성

**상태**: 🔄 진행 중  
**문제**: 아직 테스트하지 않음

#### **Devices API** - `app/api/v1/devices.py`
- [x] **GET 초기**: `/api/devices/list` - Devices 데이터 목록 조회
- [ ] **POST 생성**: `/api/devices/` - 새 Devices 데이터 생성
- [ ] **GET 생성후**: `/api/devices/list` - 생성된 데이터 확인
- [ ] **PUT 수정**: `/api/devices/{data_id}` - 데이터 수정
- [ ] **GET 수정후**: `/api/devices/{data_id}` - 수정된 데이터 확인
- [ ] **DELETE**: `/api/devices/{data_id}` - 데이터 삭제
- [ ] **GET 삭제후**: `/api/devices/list` - 삭제 후 상태 확인
- [ ] **POST 신규생성**: `/api/devices/` - 새로운 데이터 재생성

**상태**: 🔄 진행 중  
**문제**: 아직 테스트하지 않음

#### **DeviceRTC API** - `app/api/v1/device_rtc.py`
- [x] **GET 초기**: `/api/device-rtc/list` - DeviceRTC 데이터 목록 조회
- [ ] **POST 생성**: `/api/device-rtc/` - 새 DeviceRTC 데이터 생성
- [ ] **GET 생성후**: `/api/device-rtc/list` - 생성된 데이터 확인
- [ ] **PUT 수정**: `/api/device-rtc/{data_id}` - 데이터 수정
- [ ] **GET 수정후**: `/api/device-rtc/{data_id}` - 수정된 데이터 확인
- [ ] **DELETE**: `/api/device-rtc/{data_id}` - 데이터 삭제
- [ ] **GET 삭제후**: `/api/device-rtc/list` - 삭제 후 상태 확인
- [ ] **POST 신규생성**: `/api/device-rtc/` - 새로운 데이터 재생성

**상태**: 🔄 진행 중  
**문제**: 아직 테스트하지 않음

---

## 📈 **테스트 진행률 요약**

### **전체 API 수**: 25개
### **테스트 시나리오**: 8단계 (GET 초기 → POST 생성 → GET 생성후 → PUT 수정 → GET 수정후 → DELETE → GET 삭제후 → POST 신규생성)
### **총 테스트 단계**: 200개 (25개 API × 8단계)

### **현재 진행률**
- **✅ 완료**: 48개 단계 (Raw 센서 API 6개 × 8단계)
- **🔄 진행 중**: 0개 단계
- **❌ 실패**: 0개 단계
- **📋 대기 중**: 152개 단계

### **API별 상태**
- **✅ 완료**: Raw 센서 API 6개 (24%)
- **🔄 진행 중**: User API, CDS API, Edge 센서 API 4개, Actuator API 4개 (52%)
- **📋 대기 중**: 기타 센서 API 11개 (44%)

---

## 🚨 **발견된 문제 및 해결 방안**

### **1. Edge 센서 및 Actuator API 필수 필드 누락 문제**

#### **문제 현황**
- **증상**: `422 Validation Error: field required`
- **원인**: 필수 필드 누락 또는 스키마 불일치
- **영향**: Edge 센서 4개, Actuator 4개 API

#### **해결 방안**
1. **스키마 검증**: Edge 센서 및 Actuator API 스키마에서 필수 필드 확인
2. **테스트 데이터 수정**: 필수 필드를 포함한 테스트 데이터 생성
3. **스키마 일치성**: ORM 모델과 API 스키마 간 필드 일치성 확인

### **2. Users, CDS API 데이터 생성 실패 문제**

#### **문제 현황**
- **증상**: 데이터 생성 실패 (상세 오류 미확인)
- **원인**: 상세 오류 메시지 미확인으로 원인 파악 어려움
- **영향**: Users API, CDS API

#### **해결 방안**
1. **오류 로깅 강화**: 상세 오류 메시지 확인 및 로깅
2. **단계별 테스트**: API별로 개별 테스트 진행
3. **문제 원인 파악**: 구체적인 오류 원인 분석

---

## 🎯 **다음 단계 계획**

### **Phase 1: Edge 센서 및 Actuator API 문제 해결 (우선순위: 높음)**
1. **Edge 센서 API 문제 해결**: 필수 필드 누락 문제 해결
2. **Actuator API 문제 해결**: 필수 필드 누락 문제 해결
3. **스키마 불일치 문제 해결**: ORM 모델과 API 스키마 간 일치성 확보

### **Phase 2: 나머지 API 테스트 진행 (우선순위: 중간)**
1. **Users, CDS API**: 데이터 생성 실패 문제 해결
2. **기타 센서 API**: DHT, IMU, Flame, Sensors, Devices, DeviceRTC
3. **전체 API 테스트**: 모든 API 엔드포인트 정상 동작 확인

### **Phase 3: 통합 테스트 완료 (우선순위: 높음)**
1. **100% 성공률 달성**: 모든 API 엔드포인트 정상 동작
2. **CRUD 작업 검증**: POST/GET/PUT/DELETE 메서드 정상 동작
3. **성능 테스트**: 응답 시간 및 처리량 확인

---

## 📝 **테스트 실행 방법**

### **1. 서버 상태 확인**
```bash
# Docker 컨테이너 상태 확인
docker-compose ps

# API 서버 상태 확인
curl -s http://localhost:8000/health
```

### **2. 개별 API 테스트**
```bash
# 예시: MQ5 API 테스트
curl -X GET "http://localhost:8000/api/mq5/list"
curl -X POST "http://localhost:8000/api/mq5/" -H "Content-Type: application/json" -d '{"time": "2025-08-22T12:00:00", "device_id": 1, "ppm_value": 100, "raw_payload": "test"}'
```

### **3. 통합 테스트 스크립트 실행**
```bash
# 통합 테스트 실행
cd services/was-server
python integration_test.py
```

---

**마지막 업데이트**: 2025-08-22 11:30:00  
**다음 검토 예정**: Edge 센서 및 Actuator API 문제 해결 완료 후
