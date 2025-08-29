# 📚 IoT Care Project - 문서 관리 시스템

## 🔍 **빠른 검색 및 네비게이션**

### **📊 프로젝트 현황 한눈에 보기**
- **[📈 현재 개발 현황](current-development-status.md)** - 전체 프로젝트 상태 및 완성도
- **[📝 작업 로그](work-log.md)** - 시간순 작업 기록 및 히스토리
- **[✅ 체크포인트](checkpoints/)** - 단계별 완료 현황

### **🔧 개발 관련 문서**
- **[🏗️ 개발 가이드라인](development-guidelines.md)** - 프로젝트 개발 표준 및 규칙
- **[🧪 개발 방법론](development-methodology/)** - TDD, Clean Architecture 등
- **[🤖 AI 에이전트 가이드](ai-agent-work-guidelines.md)** - AI 협업 가이드라인

### **📱 애플리케이션별 문서**
- **[🔌 백엔드 API](backend-apis/)** - FastAPI 백엔드 개발 현황
- **[📱 Flutter 앱](flutter-user-app/)** - Flutter 사용자 앱 개발 현황
- **[🎨 Mockup GUI](../apps/mockup_gui/)** - 대시보드 및 GUI 프로토타입

### **🧪 테스트 및 품질 관리**
- **[✅ 테스트 결과](testing-results/)** - 모든 테스트 결과 데이터
- **[📋 테스트 시나리오](testing-scenarios/)** - 테스트 계획 및 시나리오
- **[🔍 API 테스트](api-test-checklist.md)** - API 테스트 체크리스트

### **🔍 검색 및 관리 시스템**
- **[🔍 통합 검색 가이드](search-guide.md)** - 효율적인 문서 검색 방법
- **[📝 문서 관리 워크플로우](document-workflow.md)** - 문서 작성 및 관리 표준
- **[🔄 컨텍스트 재확보 가이드](context-recovery-guide.md)** - 프로젝트 컨텍스트 관리 및 복구

### **📋 체크리스트 및 가이드**
- **[✅ 프로젝트 체크리스트](checklist.md)** - 전체 프로젝트 체크리스트
- **[🔗 API 엔드포인트 관리](api-endpoint-management-guidelines.md)** - API 관리 가이드라인
- **[🧪 TDD 구현 계획](tdd-implementation-plan.md)** - TDD 적용 계획

---

## 🏷️ **키워드별 빠른 검색**

### **🔍 기술 스택별**
- **FastAPI**: [백엔드 API 현황](backend-apis/current-status.md), [API 테스트](api-integration-test-checklist.md)
- **Flutter**: [Flutter 앱 개발](flutter-user-app/development-overview.md), [사용자 앱 컨텍스트](flutter-user-app-context.md)
- **PostgreSQL**: [데이터베이스 관리](../services/was-server/maintenance/database/), [API 테스트](api-integration-test-checklist.md)
- **Docker**: [인프라 구성](../services/was-server/docker-compose.yml), [환경 설정](../services/was-server/environment/)

### **🔍 기능별**
- **사용자 관리**: [사용자 관리 API](new-user-management-api-summary.md), [권한 관리](../services/was-server/maintenance/permissions/)
- **디바이스 관리**: [디바이스 API](backend-apis/current-status.md), [센서 데이터](../services/was-server/maintenance/data/)
- **대시보드**: [Bootstrap 대시보드](../apps/mockup_gui/user_dashboard_bootstrap/), [Flask 대시보드](../apps/mockup_gui/user_dashboard_flask/)
- **테스트**: [TDD 테스트](tdd-implementation-plan.md), [통합 테스트](api-integration-test-checklist.md)

### **🔍 상태별**
- **✅ 완료**: [Backend APIs](backend-apis/current-status.md), [Flutter Phase 1](flutter-user-app/development-overview.md)
- **🔄 진행중**: [Flutter Phase 2](current-development-status.md), [통합 테스트](current-development-status.md)
- **📋 계획**: [성능 최적화](current-development-status.md), [보안 강화](current-development-status.md)

---

## 📁 **디렉토리 구조**

```
task/
├── 📊 핵심 상태 문서
│   ├── current-development-status.md    # 현재 개발 현황
│   ├── work-log.md                     # 작업 로그
│   └── README.md                       # 이 파일 (문서 인덱스)
│
├── 🏗️ 개발 관련
│   ├── development-guidelines.md        # 개발 가이드라인
│   ├── development-methodology/         # 개발 방법론
│   └── ai-agent-work-guidelines.md     # AI 에이전트 가이드
│
├── 📱 애플리케이션별
│   ├── backend-apis/                   # 백엔드 API 문서
│   ├── flutter-user-app/               # Flutter 앱 문서
│   └── flutter-user-app-context.md     # Flutter 앱 컨텍스트
│
├── 🧪 테스트 및 품질
│   ├── testing-results/                # 테스트 결과
│   ├── testing-scenarios/              # 테스트 시나리오
│   ├── api-test-checklist.md           # API 테스트 체크리스트
│   ├── api-integration-test-checklist.md # API 통합 테스트
│   └── tdd-implementation-plan.md      # TDD 구현 계획
│
├── 📋 체크리스트 및 가이드
│   ├── checklist.md                    # 프로젝트 체크리스트
│   ├── api-endpoint-management-guidelines.md # API 관리 가이드
│   └── tdd-implementation-plan.md      # TDD 구현 계획
│
├── ✅ 체크포인트
│   ├── phase1-1-complete.md            # Phase 1-1 완료
│   ├── phase1-2-complete.md            # Phase 1-2 완료
│   ├── phase1-3-complete.md            # Phase 1-3 완료
│   └── phase1-3-build-tools-complete.md # 빌드 도구 완료
│
└── 📝 기타 문서
    ├── requirements-summary.md          # 요구사항 요약
    ├── issues-and-solutions.md          # 이슈 및 해결책
    ├── context-restore-prompt.md        # 컨텍스트 복원
    ├── api-integration-test-issues.md   # API 통합 테스트 이슈
    ├── problem-analysis-and-prevention-policy.md # 문제 분석 및 예방 정책
    ├── context-management.md            # 컨텍스트 관리
    ├── commit-message-2025-08-25.md    # 커밋 메시지
    ├── phase4-progress-summary.md       # Phase 4 진행 요약
    └── new-user-management-api-summary.md # 사용자 관리 API 요약
```

---

## 🚀 **빠른 시작 가이드**

### **🆕 처음 방문하신 분**
1. **[📈 현재 개발 현황](current-development-status.md)** - 프로젝트 전체 상태 확인
2. **[✅ 체크포인트](checkpoints/)** - 완료된 단계들 확인
3. **[📝 작업 로그](work-log.md)** - 최근 작업 내용 확인

### **🔍 특정 정보를 찾고 계신 분**
1. **기술 관련**: 위의 키워드별 검색 섹션 활용
2. **상태 확인**: 상태별 필터링 섹션 활용
3. **전체 탐색**: 디렉토리 구조 섹션 활용

### **📱 개발자**
1. **[🏗️ 개발 가이드라인](development-guidelines.md)** - 개발 표준 확인
2. **[🧪 테스트 관련](testing-scenarios/)** - 테스트 방법론 확인
3. **[🔌 API 문서](backend-apis/)** - 백엔드 API 현황 확인

---

## 📊 **문서 통계**

- **총 문서 수**: 29개
- **핵심 상태 문서**: 3개
- **개발 관련 문서**: 3개
- **애플리케이션별 문서**: 3개
- **테스트 및 품질 문서**: 5개
- **체크리스트 및 가이드**: 3개
- **체크포인트 문서**: 4개
- **검색 및 관리 시스템**: 3개
- **기타 문서**: 5개

---

## 🔄 **최근 업데이트**

- **2025-08-27**: 문서 인덱스 시스템 구축 완료
- **2025-08-25**: TDD 테스트 완료, Bootstrap 대시보드 완성
- **2025-08-24**: API 통합 테스트 진행
- **2025-08-23**: Backend APIs 완성, Flutter User-App Phase 1 완성

---

## 📝 **변경 사항 히스토리**

### **v3.0 (2025-08-27) - 문서 관리 시스템 고도화**
- ✅ **문서 인덱스 시스템**: 체계적인 문서 분류 및 빠른 검색 기능
- ✅ **크로스 레퍼런스**: Obsidian 스타일 위키 링크 시스템 구축
- ✅ **태그 시스템**: 문서 분류 및 검색을 위한 태그 추가
- ✅ **변경 사항 추적**: 문서 버전 관리 및 히스토리 시스템

### **v2.0 (2025-08-25) - TDD 테스트 및 Bootstrap 대시보드**
- ✅ **TDD 테스트**: 42개 테스트 완료, 100% 성공률 달성
- ✅ **Bootstrap 대시보드**: 현대적 UI/UX 구현 완료
- ✅ **프로젝트 완성도**: 78% → 85%로 향상

### **v1.0 (2025-08-23) - 초기 문서 관리 시스템 구축**
- ✅ **기본 구조**: 프로젝트 문서 관리 및 분류 시스템
- ✅ **문서 체계화**: 카테고리별 문서 분류 및 구조화
- ✅ **개발 가이드**: 개발 방법론 및 가이드라인 문서화

---

**📝 작성자**: AI Assistant  
**📅 최종 업데이트**: 2025-08-27  
**🔍 검토자**: Development Team  
**📊 프로젝트**: IoT Care Project  
**🏷️ 버전**: v3.0 (문서 인덱스 시스템 구축)

