# IoT Care App 개발 관리 문서

## 📁 **프로젝트 구조 개요**

이 프로젝트는 모노레포(Monorepo) 구조로 구성되어 있으며, IoT Care App의 전체 개발 과정을 관리하는 문서들을 포함합니다.

```
iot-repo-4/
├─ services/                    # Backend 서비스들
│   └─ was-server/            # WAS 서버 (FastAPI)
├─ apps/                       # Frontend 애플리케이션들
│   └─ user-app/              # Flutter User-App
├─ task/                       # 개발 관리 문서 (현재 위치)
│   ├─ flutter-user-app/      # Flutter User-App 관련 문서
│   ├─ backend-apis/          # Backend APIs 관련 문서
│   ├─ development-methodology/ # 개발 방법론 관련 문서
│   └─ checkpoints/           # 개발 체크포인트
└─ README.md                   # 프로젝트 메인 README
```

## 🎯 **주요 개발 영역**

### **1. Backend APIs (FastAPI)**
- **위치**: `services/was-server/`
- **기술 스택**: FastAPI, SQLAlchemy, PostgreSQL
- **아키텍처**: Clean Architecture, Dependency Injection
- **상태**: ✅ 완성된 APIs (Users, Devices, Sensors), ✅ 신규 APIs (User Management, Home State, Environmental)

### **2. Flutter User-App (Web)**
- **위치**: `apps/user-app/`
- **기술 스택**: Flutter Web, Provider, Dio
- **아키텍처**: Clean Architecture + Provider
- **상태**: 🔄 계획 및 설계 완료, 🚀 개발 시작 예정

## 📚 **문서 구조 및 내용**

### **📱 Flutter User-App (`task/flutter-user-app/`)**
- **`development-overview.md`**: Flutter User-App 개발 개요 및 현재 상태
- **개발 우선순위**: 대시보드 → 스케줄 관리 → 인증 시스템 → 실시간화
- **기술 스택**: Flutter Web, Provider, Dio, fl_chart
- **UI/UX**: 다크모드 기반, 무채색 + 포인트 컬러 시스템

### **🔧 Backend APIs (`task/backend-apis/`)**
- **`current-status.md`**: Backend APIs 개발 현황 및 최근 추가 테이블 상태
- **구현된 APIs**: 8개 센서 APIs + 5개 신규 관리 APIs
- **아키텍처**: Clean Architecture, Repository Pattern, Dependency Injection
- **해결된 이슈**: Pydantic v1 호환성, SQLAlchemy v2 동기/비동기, FastAPI Body Parameter

### **📖 개발 방법론 (`task/development-methodology/`)**
- **`tdd-and-clean-architecture.md`**: TDD 및 Clean Architecture 개발 방법론 가이드
- **TDD 사이클**: Red → Green → Refactor
- **테스트 전략**: 단위 테스트(70%) + 통합 테스트(20%) + API 테스트(10%)
- **코드 품질**: 테스트 커버리지 70% 이상, 코드 복잡도 최적화

## 🚀 **최근 개발 현황 (2025-08-23)**

### **✅ 완료된 작업**
1. **Backend APIs 확장**: 5개 신규 테이블 및 RESTful APIs 구현
2. **Flutter User-App 설계**: 아키텍처, UI/UX, 개발 방법론 완성
3. **개발 방법론 문서화**: TDD, Clean Architecture 가이드 작성
4. **모노레포 구조 정리**: Task 폴더 하위 구조 체계화

### **🔄 진행 중인 작업**
1. **Flutter Web 프로젝트 생성**: 기본 구조 및 의존성 설정
2. **API 통합 테스트**: 신규 APIs 검증 및 성능 최적화

### **📋 다음 단계**
1. **Flutter 프로젝트 초기화**: SDK 설치, 프로젝트 생성, 기본 구조 설정
2. **대시보드 개발**: Phase 1 우선순위 기능 구현
3. **TDD 적용**: 테스트 우선 개발 방식으로 안전한 개발 진행

## 🎨 **UI/UX 디자인 가이드라인**

### **색상 시스템**
- **배경**: 무채색(블랙+그레이) 기반 차분한 구성
- **기본 UI**: 블루/시안 계열로 안정성과 신뢰감 표현
- **위기 알림**: 옐로우·레드 계열로 경보 레벨에 따른 시각적 강조
- **긍정/완료 상태**: 그린 계열로 성공과 완료 상태 표현

### **디자인 원칙**
1. **사용자 중심 디자인**: 직관적이고 효율적인 인터페이스
2. **미니멀리즘**: 복잡한 시각적 요소 최소화
3. **데이터 시각화**: 복잡한 데이터를 쉽게 이해할 수 있는 표현
4. **2025년 트렌드 반영**: AI, 다크모드, 벤토 그리드 레이아웃

## 🧪 **개발 방법론**

### **TDD (Test-Driven Development)**
- **Red-Green-Refactor 사이클**: 실패하는 테스트 → 최소 구현 → 리팩토링
- **테스트 우선**: 모든 기능에 대한 테스트 코드 먼저 작성
- **점진적 개발**: 작은 단위로 안전하게 개발 진행

### **Clean Architecture**
- **4계층 구조**: Presentation → Use Cases → Repository Interface → Infrastructure
- **의존성 규칙**: 외부 계층이 내부 계층에 의존하지 않음
- **테스트 용이성**: 비즈니스 로직을 독립적으로 테스트 가능

### **Dependency Injection**
- **중앙 집중식 의존성 관리**: Container 패턴으로 의존성 주입
- **Lazy Loading**: 필요할 때만 인스턴스 생성
- **테스트 용이성**: Mock 객체로 의존성 격리

## 📊 **성공 지표 및 모니터링**

### **기능적 지표**
- 모든 대시보드 기능 정상 동작
- 실시간 데이터 업데이트 지연 시간 < 3초
- 사용자 인증 및 권한 관리 정상 동작
- 스케줄 관리 기능 완성도 100%

### **성능 지표**
- 앱 로딩 시간 < 2초
- 데이터 렌더링 시간 < 500ms
- 메모리 사용량 최적화
- 네트워크 요청 최적화

### **품질 지표**
- 테스트 커버리지 70% 이상
- 코드 품질 점수 90% 이상
- 사용자 경험 만족도 4.5/5.0 이상

## 🔄 **CI/CD 파이프라인**

### **GitHub Actions**
- **코드 품질 검사**: `flutter analyze`, `flutter format`
- **테스트 실행**: `flutter test --coverage`
- **빌드 검증**: `flutter build web --release`
- **자동 배포**: 스테이징/프로덕션 환경별 자동 배포
- **코드 커버리지**: Codecov 연동으로 테스트 커버리지 모니터링

## 🚨 **리스크 관리**

### **기술적 리스크**
1. **Flutter Web 성능 이슈**: 사전 성능 테스트, 최적화 기법 적용
2. **실시간 데이터 처리 복잡성**: 단계적 구현, 폴백 메커니즘 준비
3. **대용량 데이터 렌더링 성능**: 가상화, 페이지네이션, 지연 로딩

### **일정 리스크**
1. **개발 인력 부족**: 우선순위 조정, 핵심 기능 우선 구현
2. **API 연동 지연**: Mock 데이터 활용, 병렬 개발 진행
3. **테스트 시간 부족**: TDD 방식으로 개발과 테스트 동시 진행

## 📝 **개발 프로세스**

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

## 🔗 **관련 링크**

### **Backend APIs**
- [FastAPI 서버](http://localhost:8000)
- [API 문서 (Swagger)](http://localhost:8000/docs)
- [ReDoc 문서](http://localhost:8000/redoc)

### **Flutter User-App**
- [개발 목표 및 계획](apps/user-app/objective/)
- [구현 체크리스트](apps/user-app/objective/implementation-checklist.md)
- [개발 진행 상황](apps/user-app/objective/development-progress.md)

### **개발 가이드**
- [빠른 개발 방법론](apps/user-app/objective/rapid-development-methodology.md)
- [TDD 및 Clean Architecture 가이드](task/development-methodology/tdd-and-clean-architecture.md)

---

**문서 버전**: 2.0  
**마지막 업데이트**: 2025-08-23  
**작성자**: AI Assistant  
**프로젝트**: IoT Care App 개발 관리 문서

