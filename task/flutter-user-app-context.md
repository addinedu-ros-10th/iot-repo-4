# 🚀 Flutter User-App 개발 맥락 가이드

## 📋 **프로젝트 개요**

**프로젝트명**: IoT Care System - Flutter User-App  
**개발 단계**: Phase 1 (대시보드) 완료, Phase 2 (스케줄 관리) 진행 중  
**목표**: IoT 센서 데이터를 실시간으로 모니터링하고 돌봄 서비스를 관리하는 웹 애플리케이션

## 🏗️ **아키텍처 구조**

### **Clean Architecture + Provider 패턴**
```
lib/
├── data/           # 데이터 레이어
│   ├── dtos/      # Data Transfer Objects
│   ├── services/  # API 서비스
│   └── sources/   # 데이터 소스 (API, 로컬 DB)
├── domain/        # 도메인 레이어 (엔티티, 유스케이스)
├── presentation/  # 프레젠테이션 레이어
│   ├── pages/    # 화면
│   ├── widgets/  # 재사용 가능한 위젯
│   └── state/    # 상태 관리 (Provider)
└── main.dart      # 앱 진입점
```

### **주요 Provider들**
- `CareTargetsProvider`: 돌봄 대상자 관리
- `HomeStateSnapshotsProvider`: 홈 상태 스냅샷 데이터 관리
- `ApiService`: HTTP API 통신
- `UserService`: 사용자 관련 API
- `HomeStateSnapshotService`: 홈 상태 스냅샷 API

## 🔧 **핵심 기능**

### **Phase 1: 대시보드 (완료)**
- ✅ 실시간 홈 상태 모니터링
- ✅ 센서 데이터 시각화 (차트, 그래프)
- ✅ 평면도 기반 센서 상태 표시
- ✅ 활동 피드 및 경보 시스템
- ✅ 돌봄 대상자 목록 관리

### **Phase 2: 스케줄 관리 (진행 중)**
- ⏳ 일정 관리 및 알림
- ⏳ 복약 체크 및 기록
- ⏳ 돌봄 활동 스케줄링

### **Phase 3: 인증 시스템 (계획)**
- 🔲 사용자 로그인/로그아웃
- 🔲 권한 관리
- 🔲 세션 관리

### **Phase 4: 실시간화 (계획)**
- 🔲 WebSocket/SSE 연결
- 🔲 실시간 알림
- 🔲 실시간 데이터 업데이트

## 🌐 **API 통신 구조**

### **백엔드 서버**
- **URL**: `http://localhost` (개발), `http://ec2-43-201-96-23.ap-northeast-2.compute.amazonaws.com` (운영)
- **포트**: 8000 (백엔드), 8083/8084 (Flutter 웹)

### **주요 API 엔드포인트**
```dart
// 사용자 관계
GET /api/user-relationships/user/{userId}/as-subject
GET /api/user-relationships/user/{userId}/as-target

// 홈 상태 스냅샷
GET /api/home-state-snapshots/time-range/{userId}
GET /api/home-state-snapshots/alert-level/{userId}/{level}
GET /api/home-state-snapshots/latest/{userId}

// 사용자 관리
GET /api/users/{userId}
GET /api/users/list
```

### **데이터 흐름**
1. **Provider** → **Service** → **API Service** → **백엔드 서버**
2. **백엔드 응답** → **DTO 변환** → **Provider 상태 업데이트** → **UI 갱신**

## 🎨 **UI/UX 설계 원칙**

### **디자인 시스템**
- **색상**: 모노크롬 베이스 + 강한 액센트 컬러
- **스타일**: 미니멀리즘, 2025 트렌드 (AI, 아날로그, 3D, 다크모드)
- **레이아웃**: Bento Grid, 적절한 여백, 반응형 디자인

### **주요 위젯**
- `FloorPlanWidget`: 홈 평면도 및 센서 상태
- `SensorChartWidget`: 실시간 센서 데이터 차트
- `ActivityFeedWidget`: 활동 타임라인
- `GlobalDashboardPage`: 메인 대시보드

## 🚨 **현재 발생 중인 문제**

### **API 연결 실패 (2025-08-25)**
- **증상**: 돌봄 대상자 목록 및 홈 상태 스냅샷 로드 실패
- **에러**: `XMLHttpRequest onError callback was called`
- **원인**: 네트워크 레이어 오류 (CORS, 서버 상태, 포트 충돌 가능성)
- **상태**: 🔴 해결 진행 중

### **해결 방향**
1. 서버 실행 상태 확인
2. CORS 설정 검증
3. 네트워크 연결 테스트
4. 환경 설정 검증

## 📁 **주요 파일 구조**

### **핵심 서비스 파일**
```
lib/data/services/
├── user_service.dart              # 사용자 API 서비스
├── home_state_snapshot_service.dart # 홈 상태 스냅샷 API 서비스
└── api_service.dart               # HTTP 통신 서비스
```

### **상태 관리 파일**
```
lib/presentation/state/
├── care_targets_provider.dart     # 돌봄 대상자 상태 관리
└── home_state_snapshots_provider.dart # 홈 상태 스냅샷 상태 관리
```

### **데이터 모델 파일**
```
lib/data/dtos/
├── user_dto.dart                  # 사용자 DTO
├── user_relationship_dto.dart     # 사용자 관계 DTO
└── home_state_snapshot_dto.dart  # 홈 상태 스냅샷 DTO
```

### **UI 화면 파일**
```
lib/presentation/pages/
└── global_dashboard_page.dart     # 메인 대시보드

lib/presentation/widgets/
├── floor_plan_widget.dart         # 평면도 위젯
├── sensor_chart_widget.dart       # 센서 차트 위젯
└── activity_feed_widget.dart      # 활동 피드 위젯
```

## 🛠️ **개발 환경 설정**

### **Flutter 명령어 실행**
```bash
# 올바른 경로에서 실행 (중요!)
cd apps/user_app

# 자동화 스크립트 사용 (권장)
./scripts/run_flutter.sh          # macOS/Linux
scripts\run_flutter.bat           # Windows
python3 scripts/run_flutter.py    # 크로스 플랫폼

# Makefile 사용
make run                          # Chrome에서 실행
make setup                        # 전체 설정
make dev                          # 개발 시작
```

### **의존성 관리**
```yaml
# pubspec.yaml 주요 패키지
dependencies:
  flutter: ^3.16.0
  provider: ^6.1.1
  dio: ^5.4.0
  fl_chart: ^0.66.0
  web_socket_channel: ^2.4.0
```

## 🔍 **문제 해결 가이드**

### **자주 발생하는 문제들**
1. **`Error: No pubspec.yaml file found`**
   - **원인**: 잘못된 경로에서 Flutter 명령어 실행
   - **해결**: `cd apps/user_app` 후 실행

2. **컴파일 에러 (bool? nullability)**
   - **원인**: null safety 규칙 위반
   - **해결**: `if (nullableBool ?? false)` 형태로 수정

3. **API 연결 실패**
   - **원인**: 네트워크 레이어 오류
   - **해결**: 서버 상태, CORS 설정, 네트워크 연결 검증

### **디버깅 방법**
1. **Flutter DevTools**: `http://127.0.0.1:9100`
2. **브라우저 개발자 도구**: 네트워크 탭, 콘솔
3. **API 테스트**: `curl` 명령어로 직접 테스트

## 📚 **참고 자료**

### **개발 문서**
- `task/current-development-status.md`: 전체 개발 현황
- `apps/user_app/README.md`: 프로젝트별 README
- `scripts/`: 자동화 스크립트

### **백엔드 API 문서**
- Swagger UI: `http://localhost/docs`
- API 스키마: `services/was-server/app/api/v1/`

### **Flutter 공식 문서**
- [Flutter Web](https://docs.flutter.dev/get-started/web)
- [Provider 패턴](https://docs.flutter.dev/development/data-and-backend/state-mgmt/simple)
- [HTTP 통신](https://docs.flutter.dev/development/data-and-backend/state-mgmt/simple)

---

**문서 버전**: 1.0  
**최종 업데이트**: 2025-08-25  
**작성자**: AI Assistant  
**목적**: Flutter User-App 개발 맥락 빠른 파악
