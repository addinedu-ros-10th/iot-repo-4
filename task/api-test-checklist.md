# 🧪 IoT Care API TDD 테스트 체크리스트

## 📋 테스트 개요
- **테스트 방식**: TDD (Test-Driven Development)
- **테스트 도구**: curl, bash 스크립트
- **테스트 환경**: Docker 컨테이너 (localhost:8000)
- **테스트 일시**: 2024-08-20

## 🎯 테스트 목표
1. **의존성 주입 문제 해결 확인**
2. **API 엔드포인트 가용성 검증**
3. **에러 처리 및 응답 형식 검증**
4. **성능 및 안정성 테스트**

## 📊 API 테스트 대상 (57개 엔드포인트)

### **1. 사용자 관리 API**
- [ ] **POST** `/api/v1/users/` - 사용자 생성
- [ ] **GET** `/api/v1/users/` - 사용자 목록 조회
- [ ] **GET** `/api/v1/users/{user_id}` - 특정 사용자 조회
- [ ] **PUT** `/api/v1/users/{user_id}` - 사용자 정보 수정
- [ ] **DELETE** `/api/v1/users/{user_id}` - 사용자 삭제

### **2. 디바이스 관리 API**
- [ ] **POST** `/api/v1/devices/` - 디바이스 생성
- [ ] **GET** `/api/v1/devices/` - 디바이스 목록 조회
- [ ] **GET** `/api/v1/devices/{device_id}` - 특정 디바이스 조회
- [ ] **PUT** `/api/v1/devices/{device_id}` - 디바이스 정보 수정
- [ ] **DELETE** `/api/v1/devices/{device_id}` - 디바이스 삭제
- [ ] **GET** `/api/v1/{user_id}/devices` - 사용자별 디바이스 조회

### **3. 센서 데이터 API**

#### **3.1 LoadCell 센서**
- [ ] **POST** `/api/v1/loadcell/` - LoadCell 데이터 생성
- [ ] **GET** `/api/v1/loadcell/` - LoadCell 데이터 목록 조회
- [ ] **GET** `/api/v1/loadcell/latest/{device_id}` - 최신 LoadCell 데이터
- [ ] **GET** `/api/v1/loadcell/{device_id}/{timestamp}` - 특정 시간 LoadCell 데이터
- [ ] **PUT** `/api/v1/loadcell/{device_id}/{timestamp}` - LoadCell 데이터 수정
- [ ] **DELETE** `/api/v1/loadcell/{device_id}/{timestamp}` - LoadCell 데이터 삭제
- [ ] **GET** `/api/v1/loadcell/{device_id}/statistics` - LoadCell 통계

#### **3.2 MQ5 센서**
- [ ] **POST** `/api/v1/mq5/` - MQ5 데이터 생성
- [ ] **GET** `/api/v1/mq5/` - MQ5 데이터 목록 조회
- [ ] **GET** `/api/v1/mq5/latest/{device_id}` - 최신 MQ5 데이터
- [ ] **GET** `/api/v1/mq5/{device_id}/{timestamp}` - 특정 시간 MQ5 데이터
- [ ] **PUT** `/api/v1/mq5/{device_id}/{timestamp}` - MQ5 데이터 수정
- [ ] **DELETE** `/api/v1/mq5/{device_id}/{timestamp}` - MQ5 데이터 삭제
- [ ] **GET** `/api/v1/mq5/{device_id}/statistics` - MQ5 통계

#### **3.3 MQ7 센서**
- [ ] **POST** `/api/v1/mq7/` - MQ7 데이터 생성
- [ ] **GET** `/api/v1/mq7/` - MQ7 데이터 목록 조회
- [ ] **GET** `/api/v1/mq7/latest/{device_id}` - 최신 MQ7 데이터
- [ ] **GET** `/api/v1/mq7/{device_id}/{timestamp}` - 특정 시간 MQ7 데이터
- [ ] **PUT** `/api/v1/mq7/{device_id}/{timestamp}` - MQ7 데이터 수정
- [ ] **DELETE** `/api/v1/mq7/{device_id}/{timestamp}` - MQ7 데이터 삭제
- [ ] **GET** `/api/v1/mq7/{device_id}/statistics` - MQ7 통계

#### **3.4 RFID 센서**
- [ ] **POST** `/api/v1/rfid/` - RFID 데이터 생성
- [ ] **GET** `/api/v1/rfid/` - RFID 데이터 목록 조회
- [ ] **GET** `/api/v1/rfid/latest/{device_id}` - 최신 RFID 데이터
- [ ] **GET** `/api/v1/rfid/{device_id}/{timestamp}` - 특정 시간 RFID 데이터
- [ ] **PUT** `/api/v1/rfid/{device_id}/{timestamp}` - RFID 데이터 수정
- [ ] **DELETE** `/api/v1/rfid/{device_id}/{timestamp}` - RFID 데이터 삭제
- [ ] **GET** `/api/v1/rfid/{device_id}/statistics` - RFID 통계

#### **3.5 Sound 센서**
- [ ] **POST** `/api/v1/sound/` - Sound 데이터 생성
- [ ] **GET** `/api/v1/sound/` - Sound 데이터 목록 조회
- [ ] **GET** `/api/v1/sound/latest/{device_id}` - 최신 Sound 데이터
- [ ] **GET** `/api/v1/sound/{device_id}/{timestamp}` - 특정 시간 Sound 데이터
- [ ] **PUT** `/api/v1/sound/{device_id}/{timestamp}` - Sound 데이터 수정
- [ ] **DELETE** `/api/v1/sound/{device_id}/{timestamp}` - Sound 데이터 삭제
- [ ] **GET** `/api/v1/sound/{device_id}/statistics` - Sound 통계

#### **3.6 TCRT5000 센서**
- [ ] **POST** `/api/v1/tcrt5000/` - TCRT5000 데이터 생성
- [ ] **GET** `/api/v1/tcrt5000/` - TCRT5000 데이터 목록 조회
- [ ] **GET** `/api/v1/tcrt5000/latest/{device_id}` - 최신 TCRT5000 데이터
- [ ] **GET** `/api/v1/tcrt5000/{device_id}/{timestamp}` - 특정 시간 TCRT5000 데이터
- [ ] **PUT** `/api/v1/tcrt5000/{device_id}/{timestamp}` - TCRT5000 데이터 수정
- [ ] **DELETE** `/api/v1/tcrt5000/{device_id}/{timestamp}` - TCRT5000 데이터 삭제
- [ ] **GET** `/api/v1/tcrt5000/{device_id}/statistics` - TCRT5000 통계

#### **3.7 Ultrasonic 센서**
- [ ] **POST** `/api/v1/ultrasonic/` - Ultrasonic 데이터 생성
- [ ] **GET** `/api/v1/ultrasonic/` - Ultrasonic 데이터 목록 조회
- [ ] **GET** `/api/v1/ultrasonic/latest/{device_id}` - 최신 Ultrasonic 데이터
- [ ] **GET** `/api/v1/ultrasonic/{device_id}/{timestamp}` - 특정 시간 Ultrasonic 데이터
- [ ] **PUT** `/api/v1/ultrasonic/{device_id}/{timestamp}` - Ultrasonic 데이터 수정
- [ ] **DELETE** `/api/v1/ultrasonic/{device_id}/{timestamp}` - Ultrasonic 데이터 삭제
- [ ] **GET** `/api/v1/ultrasonic/{device_id}/statistics` - Ultrasonic 통계

### **4. Edge 센서 API**

#### **4.1 Edge Flame 센서**
- [ ] **POST** `/api/v1/edge-flame/` - Edge Flame 데이터 생성
- [ ] **GET** `/api/v1/edge-flame/` - Edge Flame 데이터 목록 조회
- [ ] **GET** `/api/v1/edge-flame/latest/{device_id}` - 최신 Edge Flame 데이터
- [ ] **GET** `/api/v1/edge-flame/{device_id}/{timestamp}` - 특정 시간 Edge Flame 데이터
- [ ] **PUT** `/api/v1/edge-flame/{device_id}/{timestamp}` - Edge Flame 데이터 수정
- [ ] **DELETE** `/api/v1/edge-flame/{device_id}/{timestamp}` - Edge Flame 데이터 삭제
- [ ] **GET** `/api/v1/edge-flame/{device_id}/stats/sync` - Edge Flame 동기화 통계
- [ ] **GET** `/api/v1/edge-flame/{device_id}/stats/drift` - Edge Flame 드리프트 분석

#### **4.2 Edge PIR 센서**
- [ ] **POST** `/api/v1/edge-pir/` - Edge PIR 데이터 생성
- [ ] **GET** `/api/v1/edge-pir/` - Edge PIR 데이터 목록 조회
- [ ] **GET** `/api/v1/edge-pir/latest/{device_id}` - 최신 Edge PIR 데이터
- [ ] **GET** `/api/v1/edge-pir/{device_id}/{timestamp}` - 특정 시간 Edge PIR 데이터
- [ ] **PUT** `/api/v1/edge-pir/{device_id}/{timestamp}` - Edge PIR 데이터 수정
- [ ] **DELETE** `/api/v1/edge-pir/{device_id}/{timestamp}` - Edge PIR 데이터 삭제
- [ ] **GET** `/api/v1/edge-pir/{device_id}/stats/sync` - Edge PIR 동기화 통계
- [ ] **GET** `/api/v1/edge-pir/{device_id}/stats/drift` - Edge PIR 드리프트 분석

#### **4.3 Edge Reed 센서**
- [ ] **POST** `/api/v1/edge-reed/` - Edge Reed 데이터 생성
- [ ] **GET** `/api/v1/edge-reed/` - Edge Reed 데이터 목록 조회
- [ ] **GET** `/api/v1/edge-reed/latest/{device_id}` - 최신 Edge Reed 데이터
- [ ] **GET** `/api/v1/edge-reed/{device_id}/{timestamp}` - 특정 시간 Edge Reed 데이터
- [ ] **PUT** `/api/v1/edge-reed/{device_id}/{timestamp}` - Edge Reed 데이터 수정
- [ ] **DELETE** `/api/v1/edge-reed/{device_id}/{timestamp}` - Edge Reed 데이터 삭제
- [ ] **GET** `/api/v1/edge-reed/{device_id}/stats/sync` - Edge Reed 동기화 통계
- [ ] **GET** `/api/v1/edge-reed/{device_id}/stats/drift` - Edge Reed 드리프트 분석

#### **4.4 Edge Tilt 센서**
- [ ] **POST** `/api/v1/edge-tilt/` - Edge Tilt 데이터 생성
- [ ] **GET** `/api/v1/edge-tilt/` - Edge Tilt 데이터 목록 조회
- [ ] **GET** `/api/v1/edge-tilt/latest/{device_id}` - 최신 Edge Tilt 데이터
- [ ] **GET** `/api/v1/edge-tilt/{device_id}/{timestamp}` - 특정 시간 Edge Tilt 데이터
- [ ] **PUT** `/api/v1/edge-tilt/{device_id}/{timestamp}` - Edge Tilt 데이터 수정
- [ ] **DELETE** `/api/v1/edge-tilt/{device_id}/{timestamp}` - Edge Tilt 데이터 삭제
- [ ] **GET** `/api/v1/edge-tilt/{device_id}/stats/sync` - Edge Tilt 동기화 통계
- [ ] **GET** `/api/v1/edge-tilt/{device_id}/stats/drift` - Edge Tilt 드리프트 분석

### **5. Actuator 로그 API**

#### **5.1 Actuator Buzzer**
- [ ] **POST** `/api/v1/actuator-buzzer/` - Buzzer 로그 생성
- [ ] **GET** `/api/v1/actuator-buzzer/` - Buzzer 로그 목록 조회
- [ ] **GET** `/api/v1/actuator-buzzer/latest/{device_id}` - 최신 Buzzer 로그
- [ ] **GET** `/api/v1/actuator-buzzer/{device_id}/{timestamp}` - 특정 시간 Buzzer 로그
- [ ] **PUT** `/api/v1/actuator-buzzer/{device_id}/{timestamp}` - Buzzer 로그 수정
- [ ] **DELETE** `/api/v1/actuator-buzzer/{device_id}/{timestamp}` - Buzzer 로그 삭제
- [ ] **GET** `/api/v1/actuator-buzzer/{device_id}/statistics` - Buzzer 통계

#### **5.2 Actuator IRTX**
- [ ] **POST** `/api/v1/actuator-irtx/` - IRTX 로그 생성
- [ ] **GET** `/api/v1/actuator-irtx/` - IRTX 로그 목록 조회
- [ ] **GET** `/api/v1/actuator-irtx/latest/{device_id}` - 최신 IRTX 로그
- [ ] **GET** `/api/v1/actuator-irtx/{device_id}/{timestamp}` - 특정 시간 IRTX 로그
- [ ] **PUT** `/api/v1/actuator-irtx/{device_id}/{timestamp}` - IRTX 로그 수정
- [ ] **DELETE** `/api/v1/actuator-irtx/{device_id}/{timestamp}` - IRTX 로그 삭제
- [ ] **GET** `/api/v1/actuator-irtx/{device_id}/statistics` - IRTX 통계

#### **5.3 Actuator Relay**
- [ ] **POST** `/api/v1/actuator-relay/` - Relay 로그 생성
- [ ] **GET** `/api/v1/actuator-relay/` - Relay 로그 목록 조회
- [ ] **GET** `/api/v1/actuator-relay/latest/{device_id}` - 최신 Relay 로그
- [ ] **GET** `/api/v1/actuator-relay/{device_id}/{timestamp}` - 특정 시간 Relay 로그
- [ ] **PUT** `/api/v1/actuator-relay/{device_id}/{timestamp}` - Relay 로그 수정
- [ ] **DELETE** `/api/v1/actuator-relay/{device_id}/{timestamp}` - Relay 로그 삭제
- [ ] **GET** `/api/v1/actuator-relay/{device_id}/statistics` - Relay 통계

#### **5.4 Actuator Servo**
- [ ] **POST** `/api/v1/actuator-servo/` - Servo 로그 생성
- [ ] **GET** `/api/v1/actuator-servo/` - Servo 로그 목록 조회
- [ ] **GET** `/api/v1/actuator-servo/latest/{device_id}` - 최신 Servo 로그
- [ ] **GET** `/api/v1/actuator-servo/{device_id}/{timestamp}` - 특정 시간 Servo 로그
- [ ] **PUT** `/api/v1/actuator-servo/{device_id}/{timestamp}` - Servo 로그 수정
- [ ] **DELETE** `/api/v1/actuator-servo/{device_id}/{timestamp}` - Servo 로그 삭제
- [ ] **GET** `/api/v1/actuator-servo/{device_id}/statistics` - Servo 통계

### **6. 시스템 상태 API**

#### **6.1 DeviceRTC Status**
- [ ] **POST** `/api/v1/device-rtc/` - DeviceRTC 상태 생성
- [ ] **GET** `/api/v1/device-rtc/` - DeviceRTC 상태 목록 조회
- [ ] **GET** `/api/v1/device-rtc/latest` - 최신 DeviceRTC 상태
- [ ] **GET** `/api/v1/device-rtc/{device_id}/{timestamp}` - 특정 시간 DeviceRTC 상태
- [ ] **PUT** `/api/v1/device-rtc/{device_id}/{timestamp}` - DeviceRTC 상태 수정
- [ ] **DELETE** `/api/v1/device-rtc/{device_id}/{timestamp}` - DeviceRTC 상태 삭제
- [ ] **GET** `/api/v1/device-rtc/{device_id}/stats/sync` - DeviceRTC 동기화 통계
- [ ] **GET** `/api/v1/device-rtc/{device_id}/stats/drift` - DeviceRTC 드리프트 분석

### **7. 기타 API**
- [x] **GET** `/health` - 헬스 체크
- [x] **GET** `/` - 루트 엔드포인트
- [x] **GET** `/docs` - Swagger UI
- [x] **GET** `/openapi.json` - OpenAPI 스키마

## 📈 테스트 결과 요약

### **테스트 진행률**
- **총 API 엔드포인트**: 57개
- **테스트 완료**: 4개
- **테스트 진행률**: 7%

### **문제점 분류**
- **의존성 주입 문제**: ✅ 해결됨
- **데이터베이스 연결 문제**: ⚠️ 해결 필요
- **API 등록 문제**: ✅ 해결됨
- **추상 메서드 구현 문제**: ✅ 해결됨
- **기타 문제**: 🔍 테스트 중 발견 예정

## 🎯 다음 단계
1. **단계별 API 테스트 수행**
2. **발견된 문제점 해결**
3. **테스트 결과 업데이트**
4. **최종 테스트 보고서 작성**

---

**테스트 담당자**: AI Assistant  
**작성일**: 2024-08-20  
**상태**: 테스트 준비 완료 