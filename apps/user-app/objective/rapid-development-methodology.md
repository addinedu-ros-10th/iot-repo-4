# Flutter User-App 빠른 개발 방법론 및 프로젝트 구조

## 🎯 **개발 원칙 및 철학**

### **핵심 원칙**
1. **데이터-표현 분리**: 비즈니스 로직과 UI 로직의 명확한 분리
2. **테스트 우선(TDD)**: 모든 기능에 대한 테스트 코드 우선 작성
3. **점진적 실시간화**: REST → WebSocket/SSE 단계적 전환
4. **최소 의존성**: 핵심 기능부터 시작하여 필요에 따라 증분 도입

### **개발 철학**
- **MVP(Minimum Viable Product) 우선**: 핵심 기능부터 빠르게 구현
- **Fail Fast**: 문제점을 빨리 발견하고 해결
- **Continuous Integration**: 지속적인 통합과 배포
- **User-Centric Design**: 사용자 중심의 직관적 인터페이스

## 🏗️ **권장 아키텍처 (Clean-ish + Provider)**

### **아키텍처 패턴**
```
Presentation Layer (UI)
    ↓
Domain Layer (Business Logic)
    ↓
Data Layer (Repository)
    ↓
Infrastructure Layer (External APIs)
```

### **프로젝트 구조**
```
lib/
├─ presentation/           # UI 계층
│   ├─ pages/            # 전체 화면 (global_dashboard.dart, person_dashboard.dart, schedule.dart)
│   ├─ widgets/          # 재사용 위젯 (kpi_card.dart, alert_chip.dart, sensor_card.dart)
│   └─ state/            # 상태 관리 (dashboard_provider.dart, auth_provider.dart)
├─ domain/               # 비즈니스 로직 계층
│   ├─ entities/         # 도메인 엔티티 (care_target.dart, home_snapshot.dart, alert_level.dart)
│   ├─ repositories/     # 리포지토리 인터페이스 (snapshot_repository.dart, auth_repository.dart)
│   └─ usecases/        # 유스케이스 (get_global_overview.dart, get_person_stream.dart)
├─ data/                 # 데이터 계층
│   ├─ sources/          # 데이터 소스 (rest_snapshot_api.dart, ws_snapshot_api.dart)
│   ├─ dtos/             # 데이터 전송 객체 (snapshot_dto.dart)
│   └─ repositories/     # 리포지토리 구현 (snapshot_repository_impl.dart)
└─ infra/                # 인프라 계층
    ├─ http_client.dart  # HTTP 클라이언트
    ├─ ws_client.dart    # WebSocket 클라이언트
    └─ storage.dart      # 로컬 저장소
```

## 🎨 **UI/UX 디자인 가이드라인**

### **디자인 원칙**
1. **사용자 중심 디자인**: 사용자의 니즈와 행동을 분석하여 직관적이고 효율적인 인터페이스 제공
2. **미니멀리즘**: 복잡한 시각적 요소를 줄이고 단순하고 정돈된 디자인으로 앱의 가치를 높임
3. **데이터 시각화**: 복잡한 데이터를 사용자가 쉽게 이해하고 빠르게 의사결정을 내릴 수 있도록 시각적으로 표현
4. **트렌드 반영**: AI, 아날로그 감성, 몰입형 3D, 다크모드, 벤토 그리드 레이아웃 등 2025년의 주요 UI/UX 트렌드를 적극적으로 수용
5. **적절한 여백 활용**: 디자인에 충분한 여백을 주어 시각적으로 더 세련되고 정돈된 느낌 제공

### **색상 시스템**
| 역할                       | HEX 코드    | 설명                       |
| ------------------------ | --------- | ------------------------ |
| **Primary Background**   | `#111827` | 차콜 블랙 – 대시보드 메인 배경       |
| **Secondary Background** | `#1F2937` | 다크 그레이 – 카드/패널/사이드바      |
| **Surface / Widget**     | `#FFFFFF` | 위젯·팝업 배경, 데이터 카드         |
| **Neutral Text**         | `#E5E7EB` | 본문 기본 텍스트 (화이트 톤)        |
| **Secondary Text**       | `#9CA3AF` | 설명 텍스트, 보조 정보            |
| **Accent Calm**          | `#3B82F6` | 블루 – 안정성 표현, 버튼/탭 강조     |
| **Alert Attention**      | `#F59E0B` | 앰버 – 주의(Attention) 경보 색  |
| **Alert Warning**        | `#EF4444` | 레드 – 심각/위험 경보            |
| **Alert Emergency**      | `#DC2626` | 다크 레드 – 응급(Emergency) 표시 |
| **Highlight Success**    | `#10B981` | 그린 – 정상/안정 상태 표시         |
| **Chart Accent**         | `#06B6D4` | 시안 – 그래프/센서 수치 강조        |

### **색상 사용 전략**
- **배경**: 무채색(블랙+그레이) 기반으로 차분하게 구성
- **기본 UI**: 블루/시안 계열로 안정성과 신뢰감 표현
- **위기 알림**: 옐로우·레드 계열로 경보 레벨에 따른 시각적 강조
- **긍정/완료 상태**: 그린 계열로 성공과 완료 상태 표현

## 🔧 **기술 스택 및 라이브러리**

### **핵심 라이브러리**
```yaml
dependencies:
  flutter:
    sdk: flutter
  
  # 상태 관리
  provider: ^6.1.1
  
  # HTTP 클라이언트
  dio: ^5.4.0
  
  # WebSocket
  web_socket_channel: ^2.4.0
  
  # 로컬 저장소
  shared_preferences: ^2.2.2
  hive: ^2.2.3
  
  # 차트 및 데이터 시각화
  fl_chart: ^0.66.0
  
  # 날짜/시간 처리
  intl: ^0.19.0
  
  # 이미지 처리
  cached_network_image: ^3.3.0
  
  # 유틸리티
  uuid: ^4.2.1
  json_annotation: ^4.8.1

dev_dependencies:
  flutter_test:
    sdk: flutter
  
  # 코드 생성
  build_runner: ^2.4.7
  json_serializable: ^6.7.1
  
  # 테스트 도구
  mockito: ^5.4.4
  http_mock_adapter: ^0.6.1
  
  # 코드 품질
  flutter_lints: ^3.0.1
```

### **Pub.dev 라이브러리 중심 UI 구성**
1. **fl_chart**: 센서 데이터 시각화 및 트렌드 차트
2. **cached_network_image**: 이미지 캐싱 및 최적화
3. **intl**: 다국어 지원 및 날짜/시간 포맷팅
4. **provider**: 상태 관리 및 의존성 주입

## 🧪 **TDD 개발 방법론**

### **테스트 타입 구성**
1. **단위 테스트(Unit)**: 경보 판정 `inferAlert()`, 우선순위 정렬 `sortByPriority()`
2. **리포지토리 테스트**: DTO↔Entity 매핑, 에러/재시도, 오프라인 캐시
3. **위젯 테스트(Widget)**: 리스트 렌더링, 탭/네비게이션, 상태 칩 컬러 매핑
4. **골든 테스트(Golden, 선택)**: 핵심 위젯 UI 스냅샷(다크/라이트)

### **TDD 사이클 (Red → Green → Refactor)**
1. **Red**: failing 테스트 작성
2. **Green**: 최소 구현으로 테스트 통과
3. **Refactor**: 중복 제거 및 경계 명확화

### **테스트 커버리지 목표**
- **전체**: 70% 이상
- **핵심 도메인**: 90% 이상
- **UI 컴포넌트**: 80% 이상

## 🚀 **실행 환경 분리**

### **환경별 설정**
```dart
// lib/config/environment.dart
enum Environment { local, development, staging, production }

class EnvironmentConfig {
  static Environment _environment = Environment.local;
  
  static void setEnvironment(Environment env) {
    _environment = env;
  }
  
  static String get apiBaseUrl {
    switch (_environment) {
      case Environment.local:
        return 'http://localhost:8000';
      case Environment.development:
        return 'http://dev-api.care.app';
      case Environment.staging:
        return 'http://staging-api.care.app';
      case Environment.production:
        return 'https://api.care.app';
    }
  }
  
  static bool get enableLogging {
    return _environment != Environment.production;
  }
  
  static bool get enableAnalytics {
    return _environment == Environment.production;
  }
}
```

### **환경별 실행 명령어**
```bash
# 로컬 개발
flutter run -d chrome --dart-define=ENVIRONMENT=local

# 개발 서버
flutter run -d chrome --dart-define=ENVIRONMENT=development

# 스테이징
flutter run -d chrome --dart-define=ENVIRONMENT=staging

# 프로덕션
flutter run -d chrome --dart-define=ENVIRONMENT=production
```

## 🔄 **CI/CD 파이프라인**

### **GitHub Actions 워크플로우**
```yaml
# .github/workflows/ci.yml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.19.0'
          channel: 'stable'
      
      - run: flutter pub get
      - run: flutter analyze
      - run: flutter test --coverage
      - run: flutter build web --release
      
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          file: coverage/lcov.info
          flags: unittests
          name: codecov-umbrella
          fail_ci_if_error: true

  deploy-staging:
    needs: test
    if: github.ref == 'refs/heads/develop'
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Staging
        run: echo "Deploy to staging environment"

  deploy-production:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Production
        run: echo "Deploy to production environment"
```

### **자동화 항목**
1. **코드 품질 검사**: `flutter analyze`, `flutter format`
2. **테스트 실행**: `flutter test --coverage`
3. **빌드 검증**: `flutter build web --release`
4. **자동 배포**: 스테이징/프로덕션 환경별 자동 배포
5. **코버리지 리포트**: Codecov 연동으로 테스트 커버리지 모니터링

## 📋 **구현 우선순위 및 체크리스트**

### **Phase 1: 대시보드 (1순위) - 2주**
#### **전체 집계 대시보드**
- [ ] 경보 우선순위 정렬 리스트
- [ ] KPI 카드 (Normal, Attention, Warning, Emergency)
- [ ] 실시간 상태 업데이트
- [ ] 성능 최적화 (스트림 스로틀링, 리스트 가상화)

#### **개인 대시보드**
- [ ] 최신 스냅샷 표시
- [ ] 센서 데이터 카드 (입구, 거실, 주방, 침실, 욕실)
- [ ] 경보 요약 및 사유 표시
- [ ] 그래프 플레이스홀더 (시간별 데이터)

### **Phase 2: 스케줄 관리 (2순위) - 1.5주**
- [ ] 복약/병원/방문 일정 CRUD
- [ ] 권한 기반 필터링 (user_relationships)
- [ ] 캘린더 UI 구현
- [ ] 알림 시스템 연동

### **Phase 3: 인증 시스템 (3순위) - 1주**
- [ ] JWT 기반 로그인/로그아웃
- [ ] 관계 기반 접근 제어
- [ ] user_relationships 기반 대상 필터링
- [ ] 권한별 기능 제한

### **Phase 4: 실시간화 (점진적) - 1주**
- [ ] REST → WebSocket/SSE 전환 플래그
- [ ] 오프라인 캐시 구현
- [ ] 재시도 정책 설정
- [ ] 연결 상태 관리

## 🎯 **성공 지표 및 마일스톤**

### **기능적 지표**
- [ ] 모든 대시보드 기능 정상 동작
- [ ] 실시간 데이터 업데이트 지연 시간 < 3초
- [ ] 사용자 인증 및 권한 관리 정상 동작
- [ ] 스케줄 관리 기능 완성도 100%

### **성능 지표**
- [ ] 앱 로딩 시간 < 2초
- [ ] 데이터 렌더링 시간 < 500ms
- [ ] 메모리 사용량 최적화
- [ ] 네트워크 요청 최적화

### **품질 지표**
- [ ] 테스트 커버리지 70% 이상
- [ ] 코드 품질 점수 90% 이상
- [ ] 사용자 경험 만족도 4.5/5.0 이상

## 🚨 **리스크 관리 및 대응 전략**

### **기술적 리스크**
1. **Flutter Web 성능 이슈**
   - **대응**: 사전 성능 테스트, 최적화 기법 적용
2. **실시간 데이터 처리 복잡성**
   - **대응**: 단계적 구현, 폴백 메커니즘 준비
3. **대용량 데이터 렌더링 성능**
   - **대응**: 가상화, 페이지네이션, 지연 로딩

### **일정 리스크**
1. **개발 인력 부족**
   - **대응**: 우선순위 조정, 핵심 기능 우선 구현
2. **API 연동 지연**
   - **대응**: Mock 데이터 활용, 병렬 개발 진행
3. **테스트 시간 부족**
   - **대응**: TDD 방식으로 개발과 테스트 동시 진행

## 📝 **개발 프로세스 및 워크플로우**

### **일일 개발 사이클**
1. **오전 (9:00-10:00)**: 일일 계획 수립 및 이슈 확인
2. **오전 (10:00-12:00)**: TDD 방식으로 기능 개발
3. **오후 (2:00-4:00)**: 코드 리뷰 및 테스트 실행
4. **오후 (4:00-6:00)**: 문서 업데이트 및 다음 날 계획 수립

### **주간 개발 사이클**
1. **월요일**: 주간 목표 설정 및 리소스 할당
2. **수요일**: 중간 진행 상황 점검 및 이슈 해결
3. **금요일**: 주간 완료 작업 리뷰 및 다음 주 계획 수립

### **커밋 규칙 (Conventional Commits)**
```
feat: 새로운 기능 추가
fix: 버그 수정
docs: 문서 수정
style: 코드 스타일 변경
refactor: 코드 리팩토링
test: 테스트 코드 추가/수정
chore: 빌드 프로세스 또는 보조 도구 변경
```

---

**문서 버전**: 1.0  
**작성일**: 2025-08-23  
**작성자**: AI Assistant  
**프로젝트**: Flutter Dashboard 중심 User-App 빠른 개발 방법론
