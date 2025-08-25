# Flutter User-App 개발 개요 및 현황

## 🎯 **프로젝트 개요**

### **서비스 목적**
Flutter 기반으로 개발된 보호자 앱으로, 실시간 모니터링 기능을 제공합니다. 생활 요약과 안심 메시지, 원격 제어 기능을 통해 보호자의 편의를 극대화하며, 돌봄 대상자 전체에 대한 집계성 분석과 개인별 분석이 가능합니다.

### **주요 기능**
1. **인증 기능**: 돌봄 대상자, 담당자를 중심으로 가족과 돌봄 제공자의 권한을 인증된 정보로 확인
2. **대시보드**: 돌봄 대상자 개인 대시보드와 전체 집계 데이터 대시보드
3. **스케줄 관리**: 복약 일정, 병원 진료 일정, 돌봄 제공자 방문 일정 등

## 🏗️ **기술 아키텍처**

### **아키텍처 패턴**
- **Clean Architecture + Provider**: 데이터-표현 분리, 테스트 우선(TDD), 점진적 실시간화
- **레이어 구조**: Presentation → Domain → Data → Infrastructure

### **기술 스택**
- **프레임워크**: Flutter Web (개발 효율성과 범용성)
- **상태 관리**: Provider
- **HTTP 클라이언트**: Dio
- **WebSocket**: web_socket_channel
- **차트**: fl_chart
- **로컬 저장소**: Hive, SharedPreferences

## 📁 **프로젝트 구조**

```
apps/user_app/
├─ lib/
│   ├─ presentation/           # UI 계층
│   │   ├─ pages/            # 전체 화면
│   │   ├─ widgets/          # 재사용 위젯
│   │   └─ state/            # 상태 관리
│   ├─ domain/               # 비즈니스 로직 계층
│   │   ├─ entities/         # 도메인 엔티티
│   │   ├─ repositories/     # 리포지토리 인터페이스
│   │   └─ usecases/        # 유스케이스
│   ├─ data/                 # 데이터 계층
│   │   ├─ sources/          # 데이터 소스
│   │   ├─ dtos/             # 데이터 전송 객체
│   │   └─ repositories/     # 리포지토리 구현
│   ├─ infra/                # 인프라 계층
│   │   ├─ http_client.dart  # HTTP 클라이언트
│   │   ├─ ws_client.dart    # WebSocket 클라이언트
│   │   └─ storage.dart      # 로컬 저장소
│   └─ config/               # 설정 계층
│       ├─ environment.dart  # 환경별 설정
│       └─ app_colors.dart   # 색상 시스템
├─ objective/                 # 개발 목표 및 계획
│   ├─ app-development-overview.md
│   ├─ implementation-checklist.md
│   ├─ development-progress.md
│   └─ rapid-development-methodology.md
└─ README.md
```

## 🎨 **UI/UX 디자인**

### **디자인 원칙**
- 사용자 중심 디자인
- 미니멀리즘
- 데이터 시각화
- 2025년 UI/UX 트렌드 반영
- 적절한 여백 활용

### **색상 시스템**
- **배경**: 무채색(블랙+그레이) 기반
- **기본 UI**: 블루/시안 (안정·신뢰)
- **위기 알림**: 옐로우·레드 계열 (경보 레벨)
- **긍정/완료 상태**: 그린

## 📋 **개발 우선순위**

### **Phase 1: 대시보드 (1순위) - 2주** ✅ **완료**
- [x] 돌봄 대상자 전체 집계 데이터 대시보드
- [x] 기본 프로젝트 구조 설정
- [x] Clean Architecture 레이어 구성
- [x] 색상 시스템 및 테마 설정
- [x] KPI 카드 위젯 구현
- [x] 전역 대시보드 페이지 구현
- [x] 환경별 설정 관리
- [x] 기본 의존성 설정
- [x] **홈 상태 스냅샷 대시보드 구현** 🆕
- [x] **실시간 센서 모니터링 기능** 🆕
- [x] **경보 시스템 및 위험 상태 감지** 🆕

### **Phase 2: 스케줄 관리 (2순위) - 1.5주** 🔄 **진행 중**
- [ ] 복약/병원/방문 일정 CRUD
- [ ] 권한 기반 필터링
- [ ] 캘린더 UI 구현

### **Phase 3: 인증 시스템 (3순위) - 1주** ⏳ **대기 중**
- [ ] JWT 기반 로그인/로그아웃
- [ ] 관계 기반 접근 제어
- [ ] 권한별 기능 제한

### **Phase 4: 실시간화 (점진적) - 1주** ⏳ **대기 중**
- [ ] REST → WebSocket/SSE 전환
- [ ] 오프라인 캐시 구현
- [ ] 재시도 정책 설정

## 🧪 **TDD 개발 방법론**

### **테스트 타입**
1. **단위 테스트**: 경보 판정, 우선순위 정렬
2. **리포지토리 테스트**: DTO↔Entity 매핑, 에러/재시도
3. **위젯 테스트**: 리스트 렌더링, 상태 칩 컬러 매핑
4. **골든 테스트**: 핵심 위젯 UI 스냅샷

### **테스트 커버리지 목표**
- 전체: 70% 이상
- 핵심 도메인: 90% 이상
- UI 컴포넌트: 80% 이상

## 🚀 **실행 환경 분리**

### **환경별 설정**
- **로컬**: `http://localhost`
- **개발**: `http://dev-api.care.app`
- **스테이징**: `http://staging-api.care.app`
- **프로덕션**: `http://ec2-43-201-96-23.ap-northeast-2.compute.amazonaws.com`

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

## ⚠️ **중요한 개발 지침**

### **Flutter 명령어 사용 시 주의사항**
**🚨 Flutter 명령어를 사용할 때는 반드시 올바른 프로젝트 경로에서 실행해야 합니다!**

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

**자주 발생하는 오류:**
- `Error: No pubspec.yaml file found` → Flutter 프로젝트 디렉토리가 아님
- `SocketException: Address already in use` → 포트 충돌 (다른 포트 사용)
- `This application is not configured to build on the web` → 웹 지원 미설정

## 🔄 **CI/CD 파이프라인**

### **GitHub Actions**
- 코드 품질 검사 (`flutter analyze`, `flutter format`)
- 테스트 실행 (`flutter test --coverage`)
- 빌드 검증 (`flutter build web --release`)
- 자동 배포 (스테이징/프로덕션)
- 코드 커버리지 리포트 (Codecov)

## 📊 **현재 개발 상태**

### **완료된 작업**
- [x] 프로젝트 계획 및 아키텍처 설계
- [x] 개발 방법론 문서화
- [x] UI/UX 디자인 가이드라인
- [x] 기술 스택 선정
- [x] 프로젝트 구조 설계
- [x] Flutter Web 프로젝트 생성
- [x] 기본 의존성 설정
- [x] Clean Architecture 프로젝트 구조 설정
- [x] 환경 설정 및 색상 시스템 구현
- [x] 기본 위젯 및 페이지 구조 생성
- [x] 전역 대시보드 페이지 구현
- [x] **API 서비스 계층 구현** 🆕
- [x] **DTO 모델 및 데이터 매핑** 🆕
- [x] **Provider 기반 상태 관리** 🆕
- [x] **홈 상태 스냅샷 대시보드** 🆕
- [x] **실시간 센서 모니터링** 🆕
- [x] **경보 시스템 및 위험 상태 감지** 🆕

### **진행 중인 작업**
- [ ] Phase 2: 스케줄 관리 기능 개발
- [ ] API 연동 및 데이터 처리 로직 구현
- [ ] 상태 관리 및 Provider 설정

### **다음 단계**
- [ ] 스케줄 관리 페이지 구현
- [ ] API 서비스 계층 구현
- [ ] 상태 관리 Provider 구현
- [ ] 테스트 코드 작성

## 🎯 **성공 지표**

### **기능적 지표**
- [x] 기본 대시보드 기능 정상 동작
- [x] **홈 상태 스냅샷 대시보드 완성** 🆕
- [x] **실시간 센서 모니터링 구현** 🆕
- [x] **경보 시스템 및 위험 상태 감지** 🆕
- [ ] 실시간 데이터 업데이트 지연 시간 < 3초
- [ ] 사용자 인증 및 권한 관리 정상 동작
- [ ] 스케줄 관리 기능 완성도 100%

### **성능 지표**
- [x] 앱 로딩 시간 < 2초
- [ ] 데이터 렌더링 시간 < 500ms
- [ ] 메모리 사용량 최적화
- [ ] 네트워크 요청 최적화

### **품질 지표**
- [ ] 테스트 커버리지 70% 이상
- [ ] 코드 품질 점수 90% 이상
- [ ] 사용자 경험 만족도 4.5/5.0 이상

## 🚨 **리스크 관리**

### **기술적 리스크**
1. **Flutter Web 성능 이슈**: 사전 성능 테스트, 최적화 기법 적용
2. **실시간 데이터 처리 복잡성**: 단계적 구현, 폴백 메커니즘 준비
3. **대용량 데이터 렌더링 성능**: 가상화, 페이지네이션, 지연 로딩
4. **잘못된 경로에서 Flutter 명령어 실행**: 경로 확인 절차 표준화

### **일정 리스크**
1. **개발 인력 부족**: 우선순위 조정, 핵심 기능 우선 구현
2. **API 연동 지연**: Mock 데이터 활용, 병렬 개발 진행
3. **테스트 시간 부족**: TDD 방식으로 개발과 테스트 동시 진행

## 📝 **최근 개발 완료 내용 (2025-08-23)**

### **Phase 1 완료 항목들**
1. **프로젝트 구조**: Clean Architecture 기반 4계층 구조 완성
2. **환경 설정**: 로컬/개발/스테이징/프로덕션 환경별 설정 완성
3. **색상 시스템**: 다크모드 기반 색상 테마 및 경보별 색상 매핑 완성
4. **기본 위젯**: KPI 카드, 경보 레벨 카드 등 재사용 가능한 위젯 구현
5. **전역 대시보드**: 전체 돌봄 대상자 현황을 한눈에 볼 수 있는 대시보드 완성
6. **의존성 관리**: Provider, Dio, fl_chart 등 핵심 라이브러리 설정 완료
7. **API 서비스 계층**: Backend API와 통신하는 서비스 클래스 구현 완료
8. **DTO 모델**: 사용자, 관계, 홈 상태 스냅샷 데이터 전송 객체 구현 완료
9. **상태 관리**: Provider 패턴을 사용한 상태 관리 시스템 구현 완료
10. **홈 상태 스냅샷 대시보드**: IoT 센서 데이터를 실시간으로 모니터링하는 대시보드 완성

### **구현된 주요 기능**
- **환영 섹션**: 사용자 친화적인 환영 메시지 및 통계 정보
- **KPI 섹션**: 경보 수준별 현황을 시각적으로 표현하는 카드 레이아웃
- **빠른 액션**: 자주 사용하는 기능에 빠르게 접근할 수 있는 버튼들
- **최근 활동**: 실시간 활동 내역을 시간순으로 표시하는 리스트
- **돌봄 대상자 목록**: 관계 기반 돌봄 대상자 정보 표시
- **홈 상태 모니터링**: 5개 공간의 센서 상태 및 환경 데이터 실시간 표시
- **경보 시스템**: 4단계 경보 수준별 통계 및 위험 상태 즉시 감지
- **센서 상태 요약**: 입구, 거실, 주방, 침실, 화장실 센서 활성/비활성 상태
- **환경 데이터**: 소음, 가스, 온도 등 실시간 환경 정보 모니터링

---

**문서 버전**: 3.0  
**작성일**: 2025-08-23  
**작성자**: AI Assistant  
**프로젝트**: Flutter Dashboard 중심 User-App 개발 개요
