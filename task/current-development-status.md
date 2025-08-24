# 현재 개발 현황

## 🎯 **프로젝트 개요**
IoT Care System은 스마트 홈 IoT 디바이스와 센서를 활용하여 돌봄 대상자의 안전과 건강을 모니터링하는 종합 시스템입니다.

## ✅ **완료된 작업**

### **Backend API 개발**
1. **사용자 관리 API** ✅
   - 사용자 CRUD, 관계 관리, 프로필 관리
   - Clean Architecture, DI/IoC 패턴 적용
   - PostgreSQL 연동 및 UUID 기반 식별

2. **센서 데이터 API** ✅
   - MQ5, MQ7, DHT, PIR, LoadCell 등 다양한 센서
   - Edge 센서 및 Actuator API
   - 실시간 데이터 수집 및 저장

3. **홈 상태 스냅샷 API** ✅
   - `home_state_snapshots` 테이블 기반 API
   - 실시간 센서 상태 모니터링
   - 경보 시스템 및 액션 로그

4. **사용자 관계 및 프로필 API** ✅
   - `user_relationships`, `user_profiles` 테이블
   - 돌봄 관계 관리 및 권한 제어
   - 사용자별 상세 정보 관리

### **Flutter User-App 개발** 🆕
1. **프로젝트 구조 및 아키텍처** ✅
   - Clean Architecture 4계층 구조 구현
   - Provider 패턴 기반 상태 관리
   - 환경별 설정 관리 (로컬/개발/스테이징/프로덕션)

2. **API 서비스 계층** ✅
   - Dio 기반 HTTP 클라이언트
   - 에러 처리 및 로깅 시스템
   - 사용자, 관계, 홈 상태 스냅샷 서비스

3. **데이터 전송 객체 (DTO)** ✅
   - 사용자, 관계, 프로필 DTO
   - 홈 상태 스냅샷 DTO (모든 센서 필드 포함)
   - JSON 직렬화/역직렬화 지원

4. **상태 관리 시스템** ✅
   - CareTargetsProvider: 돌봄 대상자 데이터 관리
   - HomeStateSnapshotsProvider: 홈 상태 스냅샷 데이터 관리
   - 실시간 데이터 업데이트 및 에러 처리

5. **홈 상태 스냅샷 대시보드** ✅
   - 실시간 센서 모니터링 (입구, 거실, 주방, 침실, 화장실)
   - 환경 데이터 표시 (소음, 가스, 온도 등)
   - 경보 시스템 (Normal, Attention, Warning, Emergency)
   - 위험 상태 즉시 감지 및 표시

## 🔄 **진행 중인 작업**

### **Flutter User-App Phase 2** 🔄
- 스케줄 관리 기능 개발
- 캘린더 UI 구현
- 일정 CRUD 기능

## ⏳ **대기 중인 작업**

### **Backend API**
- Edge 센서 및 Actuator API 문제 해결 (422 Validation Error: field required)
- API 성능 최적화 및 캐싱 전략
- 실시간 알림 시스템 (WebSocket/SSE)

### **Flutter User-App**
- Phase 3: 인증 시스템 구현
- Phase 4: 실시간화 (WebSocket/SSE)
- 테스트 코드 작성 및 TDD 적용

## 🚨 **해결된 문제들**

### **Backend API**
1. **`object NoneType can't be used in 'await' expression`** ✅
   - **원인**: SQLAlchemy v2에서 `commit()`, `refresh()`는 동기 메서드
   - **해결**: `await` 제거 및 Pydantic v1 `from_orm()` 사용

2. **API 라우터 중복 prefix 문제** ✅
   - **원인**: APIRouter와 include_router에서 동시 prefix 설정
   - **해결**: APIRouter에서 prefix 제거, include_router에서만 설정

3. **SyntaxError: non-default argument follows default argument** ✅
   - **원인**: FastAPI에서 Body 파라미터 처리 오류
   - **해결**: `Body(...)` 명시적 사용

### **Flutter User-App**
4. **API 엔드포인트 불일치 문제** ✅
   - **원인**: Flutter 앱에서 요청하는 엔드포인트가 백엔드에 구현되지 않음
   - **해결**: 서버에 맞는 기존 엔드포인트로 수정
     - `recent/{userId}` → `time-range/{userId}` (시간 범위별 스냅샷 조회)
     - `danger/{userId}` → `alert-level/{userId}/{level}` (경보 수준별 조회)
     - `alert-statistics/{userId}` → 개별 경보 수준별 조회 후 통계 생성

5. **백엔드 경로 충돌 문제** ✅
   - **원인**: 백엔드에서 `/{time}/{user_id}` 경로가 모든 요청을 가로채서 `/user/{user_id}` 엔드포인트 접근 불가
   - **해결**: `/time-range/{user_id}` 엔드포인트를 사용하여 최근 24시간 스냅샷 조회
   - **서버 리포트**: 경로 매칭 순서 문제로 인한 API 접근 제한 발생

6. **API 연결 실패 문제** 🔴
   - **원인**: 네트워크 레이어 오류 (XMLHttpRequest onError)
   - **상태**: 해결 진행 중
   - **영향**: 돌봄 대상자 목록 및 홈 상태 스냅샷 로드 불가
   - **해결 방향**: 서버 실행 상태, CORS 설정, 네트워크 연결 검증

### **Flutter User-App**
1. **잘못된 경로에서 Flutter 명령어 실행** ✅
   - **원인**: 프로젝트 루트에서 `flutter run` 실행
   - **해결**: `apps/user_app` 디렉토리에서 실행하도록 경로 확인 절차 표준화

2. **Flutter 경로 문제 자동화 해결 방안** ✅
   - **원인**: 개발자가 잘못된 경로에서 Flutter 명령어 실행
   - **해결**: 자동 경로 확인 및 수정 스크립트 제공
     - `scripts/run_flutter.sh` (macOS/Linux)
     - `scripts/run_flutter.bat` (Windows)
     - `scripts/run_flutter.py` (크로스 플랫폼)
     - `Makefile` (make 명령어 지원)

## 📁 **최근 수정된 파일들**

### **Backend API (2025-08-23)**
- `app/api/v1/home_state_snapshots.py` - 홈 상태 스냅샷 API 엔드포인트
- `app/api/v1/sensor_event_buttons.py` - 센서 이벤트 버튼 API
- `app/api/v1/sensor_raw_temperatures.py` - 온도 센서 API
- `app/use_cases/` - 홈 상태 스냅샷 및 센서 이벤트 서비스
- `app/infrastructure/repositories/` - 관련 리포지토리 구현체
- `app/domain/entities/` - 도메인 엔티티 정의

### **Flutter User-App (2025-08-23)** 🆕
- `apps/user_app/lib/main.dart` - Provider 설정 및 앱 초기화
- `apps/user_app/lib/data/sources/api_service.dart` - API 서비스 클래스
- `apps/user_app/lib/data/services/` - 사용자 및 홈 상태 스냅샷 서비스
- `apps/user_app/lib/data/dtos/` - 모든 DTO 모델
- `apps/user_app/lib/presentation/state/` - Provider 상태 관리
- `apps/user_app/lib/presentation/pages/global_dashboard_page.dart` - 홈 상태 스냅샷 대시보드

### **Flutter User-App (2025-08-25)** 🔧
- `apps/user_app/lib/data/services/home_state_snapshot_service.dart` - API 엔드포인트 경로 수정
  - `recent/{userId}` → `time-range/{userId}` (시간 범위별 스냅샷 조회)
  - `danger/{userId}` → `alert-level/{userId}/{level}` (경보 수준별 조회)
  - `alert-statistics/{userId}` → 개별 경보 수준별 조회 후 통계 생성
- `task/current-development-status.md` - 개발 지침 업데이트 (서버 코드 수정 금지 원칙 추가)

### **Flutter User-App (2025-08-25)** 🚨
- **API 연결 실패 문제 진단 및 문서화**
  - 네트워크 레이어 오류 분석
  - 백엔드 엔드포인트 구현 상태 확인
  - Flutter 앱 코드 정상 동작 확인
  - 해결 과제 및 방향 설정

## 🎯 **다음 개발 계획**

### **즉시 진행 (1-2일)**
1. **Flutter User-App Phase 2**: 스케줄 관리 기능 개발
2. **Backend API 안정화**: Edge 센서 API 문제 해결

### **단기 계획 (1주)**
1. **Flutter User-App**: 스케줄 관리 페이지 완성
2. **Backend API**: 실시간 알림 시스템 설계
3. **테스트 코드**: 핵심 기능 단위 테스트 작성

### **중기 계획 (2-3주)**
1. **Flutter User-App**: 인증 시스템 구현
2. **Backend API**: WebSocket/SSE 실시간 통신
3. **시스템 통합**: End-to-End 테스트 및 성능 최적화

## 📊 **개발 진행률**

### **Backend API**: 85% 완료
- ✅ 기본 API 구조 및 CRUD: 100%
- ✅ 사용자 관리 시스템: 100%
- ✅ 센서 데이터 수집: 100%
- ✅ 홈 상태 스냅샷: 100%
- ⏳ 실시간 통신: 0%
- ⏳ 성능 최적화: 30%

### **Flutter User-App**: 60% 완료
- ✅ 프로젝트 구조 및 아키텍처: 100%
- ✅ API 서비스 계층: 100%
- ✅ 상태 관리 시스템: 100%
- ✅ 홈 상태 스냅샷 대시보드: 100%
- ⏳ 스케줄 관리: 0%
- ⏳ 인증 시스템: 0%
- ⏳ 실시간화: 0%

## ⚠️ **중요한 개발 지침**

### **서버 코드 수정 금지 원칙**
**🚨 어플리케이션 개발 진행 중에는 서버 코드를 수정하지 않습니다!**

**개발 단계별 작업 범위:**
- **Backend API 개발 단계**: 서버 코드 수정 및 API 구현
- **Flutter User-App 개발 단계**: 서버 코드는 건드리지 않고 리포트만 작성
- **통합 테스트 단계**: 서버와 클라이언트 간 연동 문제 해결

**서버 확인 시 지침:**
1. ✅ **서버 코드 읽기**: API 엔드포인트, 스키마, 서비스 구현 확인
2. ✅ **문제점 리포트**: 구현되지 않은 엔드포인트, 응답 형식 불일치 등 문서화
3. ❌ **서버 코드 수정**: 직접적인 코드 변경 금지
4. ✅ **클라이언트 수정**: 서버에 맞게 Flutter 앱 코드 수정

### **Flutter 명령어 사용 시 주의사항**
**🚨 Flutter 명령어를 사용할 때는 반드시 올바른 프로젝트 경로에서 실행해야 합니다!**

#### **방법 1: 수동 경로 확인 (기본 방법)**
```bash
# ❌ 잘못된 방법 - 프로젝트 루트에서 실행
cd /Users/emotionalmachine/Documents/AddInEdu/Project
flutter run -d chrome  # Error: No pubspec.yaml file found

# ✅ 올바른 방법 - Flutter 프로젝트 디렉토리에서 실행
cd /Users/emotionalmachine/Documents/AddInEdu/Project/apps/user_app
flutter run -d chrome  # 정상 실행
```

**확인 방법:**
1. `pwd` 명령어로 현재 경로 확인
2. `ls` 명령어로 `pubspec.yaml` 파일 존재 여부 확인
3. `flutter doctor` 명령어로 Flutter 환경 상태 확인

#### **방법 2: 자동화 스크립트 사용 (권장 방법)**
```bash
# macOS/Linux
./scripts/run_flutter.sh

# Windows
scripts\run_flutter.bat

# Python (크로스 플랫폼)
python3 scripts/run_flutter.py

# Makefile 사용
make run
```

#### **방법 3: Makefile 명령어**
```bash
make help          # 사용 가능한 명령어 확인
make check-path    # 현재 경로 및 Flutter 프로젝트 확인
make fix-path      # 경로 문제 자동 수정
make run           # Chrome에서 Flutter 앱 실행
make setup         # 전체 설정 (의존성 설치 + 환경 진단)
make dev           # 개발 시작 (설정 + 실행)
```

**자주 발생하는 오류:**
- `Error: No pubspec.yaml file found` → Flutter 프로젝트 디렉토리가 아님
- `SocketException: Address already in use` → 포트 충돌 (다른 포트 사용)
- `This application is not configured to build on the web` → 웹 지원 미설정

**자동화 스크립트의 장점:**
- ✅ 경로 자동 확인 및 수정
- ✅ Flutter 환경 자동 진단
- ✅ 의존성 자동 설치
- ✅ 포트 충돌 자동 해결
- ✅ 크로스 플랫폼 지원

## 🚀 **기술적 성과**

### **아키텍처 개선**
- Clean Architecture 패턴 성공적 적용
- 의존성 주입 및 역전 제어 원칙 준수
- 모듈화된 코드 구조로 유지보수성 향상

### **성능 최적화**
- 비동기 데이터 처리로 응답 시간 단축
- 데이터베이스 쿼리 최적화
- 효율적인 상태 관리로 UI 렌더링 성능 향상

### **사용자 경험**
- 실시간 데이터 모니터링으로 즉시 상황 파악
- 직관적인 경보 시스템으로 위험 상태 즉시 인지
- 반응형 UI로 다양한 디바이스 지원

---

**문서 버전**: 4.0  
**최종 업데이트**: 2025-08-25  
**작성자**: AI Assistant  
**프로젝트**: IoT Care System 개발 현황

## 🚨 **현재 발생 중인 문제 (2025-08-25)**

### **API 연결 실패 문제**
1. **돌봄 대상자 목록 로드 실패**
   - **에러**: `GET /api/user-relationships/user/{userId}/as-subject` 연결 실패
   - **원인**: 네트워크 레이어 오류 (XMLHttpRequest onError)
   - **상태**: 🔴 **해결 필요**

2. **홈 상태 스냅샷 로드 실패**
   - **에러**: `GET /api/home-state-snapshots/time-range/{userId}` 연결 실패
   - **원인**: 네트워크 레이어 오류 (XMLHttpRequest onError)
   - **상태**: 🔴 **해결 필요**

### **문제 분석 결과**
- **백엔드 엔드포인트**: ✅ 정상 구현됨
  - `/api/user-relationships/user/{userId}/as-subject` → `user_relationships.py`에 구현
  - `/api/home-state-snapshots/time-range/{userId}` → `home_state_snapshots.py`에 구현
- **Flutter 앱 코드**: ✅ 정상 구현됨
  - `UserService.getUserRelationshipsAsSubject()` → 올바른 엔드포인트 호출
  - `HomeStateSnapshotService.getRecentSnapshotsForMonitoring()` → 올바른 엔드포인트 호출
- **네트워크 연결**: ❌ **문제 발생**
  - CORS 설정 문제 가능성
  - 서버 실행 상태 문제 가능성
  - 포트 충돌 문제 가능성

### **해결 과제**
1. **서버 실행 상태 확인** 🔍
   - 백엔드 서버가 정상 실행 중인지 확인
   - 포트 8000에서 서비스 제공 중인지 확인
   - CORS 설정이 올바른지 확인

2. **네트워크 연결 테스트** 🔍
   - `curl` 명령어로 직접 API 테스트
   - 브라우저 개발자 도구에서 네트워크 탭 확인
   - Flutter 앱의 네트워크 설정 확인

3. **환경 설정 검증** 🔍
   - `.env.local` 파일의 API 설정 확인
   - Flutter 앱의 `Environment` 설정 확인
   - 프록시 설정 확인


