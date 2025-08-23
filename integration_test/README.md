# Integration Test 폴더

이 폴더는 IoT Care Backend System의 통합 테스트 관련 파일들을 관리합니다.

## 📁 폴더 구조

```
integration_test/
├── README.md                           # 이 파일
├── integration_test.py                 # 통합 테스트 실행 스크립트
├── integration_test_results_*.json     # 테스트 결과 파일들
└── latest_results/                     # 최신 테스트 결과 (향후 추가 예정)
```

## 🧪 통합 테스트 실행

### 기본 실행
```bash
cd integration_test
python integration_test.py
```

### 특정 환경에서 실행
```bash
# 로컬 환경
python integration_test.py --env local

# 개발 환경
python integration_test.py --env dev

# 운영 환경
python integration_test.py --env prod
```

## 📊 테스트 결과 파일

### 파일 명명 규칙
- `integration_test_results_YYYYMMDD_HHMMSS.json`
- 예: `integration_test_results_20250822_161351.json`

### 결과 파일 구조
각 결과 파일은 다음 정보를 포함합니다:
- 테스트 실행 시간
- API별 테스트 결과 (GET, POST, PUT, DELETE)
- 성공/실패 통계
- 오류 상세 정보

## 🔍 테스트 시나리오

### 1. Health Check
- API 서버 상태 확인
- 데이터베이스 연결 상태 확인

### 2. CRUD 테스트
각 API에 대해 다음 순서로 테스트:
1. **GET (초기)**: 기존 데이터 조회
2. **POST**: 새 데이터 생성
3. **GET (생성후)**: 생성된 데이터 확인
4. **PUT**: 데이터 수정
5. **GET (수정후)**: 수정된 데이터 확인
6. **DELETE**: 데이터 삭제
7. **GET (삭제후)**: 삭제 확인
8. **POST (신규생성)**: 새로운 데이터 생성

### 3. 테스트 대상 API
- Users (사용자 관리)
- Devices (디바이스 관리)
- Sensors (센서 데이터)
  - CDS, DHT, Flame, IMU, LoadCell
  - MQ5, MQ7, RFID, Sound, TCRT5000, Ultrasonic
- Edge Sensors (엣지 센서)
  - EdgeFlame, EdgePIR, EdgeReed, EdgeTilt
- Actuators (액추에이터)
  - ActuatorBuzzer, ActuatorIRTX, ActuatorRelay, ActuatorServo

## 📈 성공률 목표

- **전체 API**: 100% 성공률
- **Health Check**: 100% 성공률
- **GET 메서드**: 100% 성공률
- **POST 메서드**: 100% 성공률
- **PUT 메서드**: 100% 성공률
- **DELETE 메서드**: 100% 성공률

## 🚨 문제 해결

### Health Check 실패
1. Docker 컨테이너 상태 확인
2. API 서버 로그 확인
3. 환경변수 설정 확인

### POST 메서드 실패
1. 필드명 불일치 확인 (ORM 모델 vs 스키마)
2. 필수 필드 누락 확인
3. 데이터베이스 연결 상태 확인

### Import Error
1. 가상환경 활성화 확인
2. 필수 패키지 설치 확인
3. 의존성 순환 참조 확인

## 📝 로그 및 모니터링

### 테스트 실행 로그
- 콘솔 출력으로 실시간 진행 상황 확인
- 상세 오류 메시지 및 스택 트레이스

### 결과 분석
- JSON 결과 파일을 통한 상세 분석
- 성공률 통계 및 트렌드 분석
- API별 성능 지표

## 🔧 개발 환경 설정

### 필수 패키지
```bash
pip install httpx asyncio pydantic-settings email-validator psycopg2-binary redis
```

### 환경변수
- `.env.local`: 로컬 개발 환경
- `.env.dev`: 개발 서버 환경
- `.env.prod`: 운영 서버 환경

### Docker 환경
```bash
# 컨테이너 상태 확인
docker-compose ps

# 로그 확인
docker-compose logs app

# 재시작
docker-compose restart app
```

---

**마지막 업데이트**: 2025-08-22 23:35:00  
**관리자**: AI Assistant
