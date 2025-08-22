# IoT Care Backend System 이슈 및 해결 방안

## 🔴 현재 진행 중인 이슈

### Issue #5: POST 메서드 실패 - 필드명 불일치 및 필수 필드 누락
**발생 시점**: 2025-08-22 10:30:00  
**상태**: 🔴 진행 중  
**우선순위**: 높음 (통합 테스트 0% 성공률)

#### 문제 상세
1. **필드명 불일치**: ORM 모델과 API 스키마 간 필드명 불일치
   - LoadCell: `raw_value` vs `weight_kg`
   - MQ5/MQ7: `analog_value` vs `ppm_value`
   - RFID: `card_id` vs `card_type`
   - Sound: `analog_value` vs `db_value`
   - TCRT5000: `digital_value` vs `object_detected`
   - Ultrasonic: `raw_value` vs `distance_cm`

2. **필수 필드 누락**: Edge 센서와 Actuator API에서 필수 필드 누락
   - EdgePIR: `motion_detected` 필수 필드 누락
   - EdgeReed: `switch_state` 필수 필드 누락
   - EdgeTilt: `tilt_detected` 필수 필드 누락
   - ActuatorBuzzer: `buzzer_type`, `state` 필수 필드 누락
   - ActuatorIRTX: `command_hex` 필수 필드 누락
   - ActuatorRelay: `channel`, `state` 필수 필드 누락
   - ActuatorServo: `channel` 필수 필드 누락

3. **데이터 생성 실패**: Users, CDS, EdgeFlame API에서 상세 오류 미확인

#### 문제 원인 분석
1. **스키마-ORM 불일치**: API 스키마와 ORM 모델 간 필드명 정의 차이
2. **테스트 데이터 부정확**: 실제 스키마와 일치하지 않는 테스트 데이터
3. **오류 로깅 부족**: 상세 오류 메시지 미확인으로 원인 파악 어려움

#### 해결 방안
**Phase 1: 필드명 불일치 해결 (1시간)**
- LoadCell, MQ5, MQ7, RFID, Sound, TCRT5000, Ultrasonic 리포지토리 수정
- ORM 모델과 스키마 간 필드명 매핑 로직 구현
- LoadCell, MQ5 리포지토리는 이미 수정 완료

**Phase 2: 필수 필드 누락 해결 (30분)**
- Edge 센서와 Actuator API 테스트 데이터에 필수 필드 추가
- 스키마 검증 통과하도록 데이터 구조 수정

**Phase 3: 오류 로깅 강화 (30분)**
- Users, CDS, EdgeFlame API 오류 원인 파악
- 상세 오류 메시지 확인 및 로깅 개선

**Phase 4: 통합 테스트 재실행 (1시간)**
- 수정된 코드로 통합 테스트 재실행
- 성공률 확인 및 추가 문제 해결

#### 진행 상황
- [x] 문제 원인 파악
- [x] 해결 계획 수립
- [x] LoadCell 리포지토리 수정 완료
- [x] MQ5 리포지토리 수정 완료
- [ ] 나머지 센서 리포지토리 수정
- [ ] Edge 센서 및 Actuator API 테스트 데이터 수정
- [ ] 통합 테스트 재실행

#### 예상 완료 시간
- **Phase 1**: 1시간
- **Phase 2**: 30분  
- **Phase 3**: 30분
- **Phase 4**: 1시간
- **총 예상 시간**: 3시간

---

## ✅ 해결된 이슈

### Issue #4: ImportError - Edge 센서 인터페이스 import 실패 (해결됨)
**발생 시점**: 2024-12-19 17:00  
**해결 시점**: 2025-08-22 10:30:00  
**상태**: ✅ 해결됨

#### 문제 상세
```
ImportError: cannot import name 'container' from partially initialized module 'app.core.container' (most likely due to a circular import)
```

#### 문제 원인 분석
1. **순환 import 문제**: `container.py`에서 API 모듈들을 직접 import
2. **인터페이스 의존성**: `actuator_service_interface.py`에서 `app.api.v1.schemas` import
3. **의존성 주입 시스템 오류**: API 모듈과 컨테이너 간 순환 참조

#### 해결 방안
**Phase 1: 인터페이스 파일 구조 정리**
- `actuator_service_interface.py`에서 스키마 import 제거
- 타입 힌트를 문자열로 변경하여 forward reference 사용

**Phase 2: 의존성 주입 시스템 수정**
- `container.py`에서 모든 import를 lazy loading 방식으로 변경
- 각 메서드 내에서 필요한 모듈을 import하도록 수정

**Phase 3: 시스템 재시작 및 테스트**
- 수정된 코드로 시스템 재시작
- Import 오류 해결 확인
- API 서버 정상 동작 검증

#### 결과
- 순환 import 문제 완전 해결
- 의존성 주입 시스템 안정화
- API 서버 정상 시작 및 동작

---

### Issue #3: psycopg2 설치 오류 (해결됨)
**발생 시점**: 2024-12-19 14:00  
**해결 시점**: 2024-12-19 15:30  
**상태**: ✅ 해결됨

#### 문제 상세
Windows 환경에서 `psycopg2` 설치 시 Microsoft Visual C++ Build Tools 오류 발생

#### 해결 방안
1. **psycopg2-binary 사용**: 컴파일된 바이너리 패키지 사용
2. **Visual C++ Build Tools 설치**: 사용자에게 필요한 도구 설치 안내
3. **자동화 스크립트 제공**: `install_packages.bat` 및 `install_packages.ps1` 생성

#### 결과
- PostgreSQL 드라이버 정상 설치 완료
- 데이터베이스 연결 정상 작동

---

### Issue #2: Pydantic 버전 호환성 문제 (해결됨)
**발생 시점**: 2024-12-19 13:00  
**해결 시점**: 2024-12-19 13:30  
**상태**: ✅ 해결됨

#### 문제 상세
`pydantic-settings` 패키지가 Pydantic v2와 호환되지 않음

#### 해결 방안
1. **Pydantic v1 사용**: `pydantic==1.10.13` 설치
2. **python-dotenv 사용**: `pydantic-settings` 대신 `python-dotenv` 사용
3. **requirements.txt 업데이트**: 호환되는 버전으로 수정

#### 결과
- 데이터 검증 시스템 정상 작동
- 환경 변수 관리 정상 작동

---

### Issue #1: Clean Architecture 위반 문제 (해결됨)
**발생 시점**: 2024-12-19 10:00  
**해결 시점**: 2024-12-19 16:00  
**상태**: ✅ 해결됨

#### 문제 상세
기존 센서 API들이 Clean Architecture를 위반하여 직접 데이터베이스에 접근

#### 해결 방안
1. **전체 API 리팩토링**: Clean Architecture 준수하도록 수정
2. **인터페이스 분리**: Repository와 Service 인터페이스 정의
3. **의존성 주입**: FastAPI의 `Depends`를 활용한 의존성 주입 구현

#### 결과
- 모든 25개 API가 Clean Architecture 준수
- 의존성 역전 원칙 완벽 적용
- 테스트 가능한 아키텍처 구현

---

## 📋 이슈 해결 체크리스트

### 현재 진행 중
- [ ] **Issue #5**: POST 메서드 실패 해결
  - [ ] 필드명 불일치 해결 (LoadCell, MQ5 완료)
  - [ ] 나머지 센서 리포지토리 수정
  - [ ] Edge 센서 및 Actuator API 테스트 데이터 수정
  - [ ] 통합 테스트 재실행

### 완료된 이슈
- [x] **Issue #4**: ImportError 해결
- [x] **Issue #3**: psycopg2 설치 오류
- [x] **Issue #2**: Pydantic 버전 호환성 문제  
- [x] **Issue #1**: Clean Architecture 위반 문제

---

## 🚨 향후 주의사항

### 1. 스키마-ORM 일치성 관리
- API 스키마와 ORM 모델 간 필드명 일치성 확인 필수
- 새로운 필드 추가 시 양쪽 모두 동기화

### 2. 테스트 데이터 정확성
- 실제 API 스키마와 일치하는 테스트 데이터 생성
- 필수 필드 포함하여 Validation Error 방지

### 3. 오류 로깅 강화
- 상세 오류 메시지 로깅으로 문제 원인 파악
- 단계별 테스트로 문제 지점 정확히 파악

---

## 📞 지원 및 문의

이슈 해결 과정에서 추가 지원이 필요한 경우:
1. 로그 파일 확인
2. 파일 구조 검증
3. 개발팀에 상세 이슈 리포트 제출

**현재 Issue #5 해결 진행 중이며, 완료 후 통합 테스트 100% 성공률 달성을 목표로 합니다.**

---

## 🚨 리부트 후 작업 재개 가이드

### 1. 환경 복구
```bash
cd /home/guehojung/Documents/Project/IOT/iot-repo-4/services/was-server
docker-compose up -d
source venv/bin/activate
```

### 2. 서버 상태 확인
```bash
curl -s http://localhost:8000/health
```

### 3. 다음 작업 우선순위
1. LoadCell, MQ5, MQ7, RFID, Sound, TCRT5000, Ultrasonic 리포지토리 수정
2. Edge 센서와 Actuator API 테스트 데이터 수정
3. 통합 테스트 재실행 및 성공률 확인

**현재 Issue #5 해결 진행 중이며, 리부트 후 즉시 작업 재개 가능합니다.**
