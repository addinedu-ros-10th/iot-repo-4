# Context 복원 프롬프트

## 🚨 **Context 끊김 상황에서 사용할 프롬프트**

### 📋 **기본 프롬프트**
```
안녕하세요. Context가 끊겼습니다. 

현재 작업 중인 프로젝트는 "독거노인 통합 돌봄 서비스 백엔드 시스템"을 위한 Docker Compose 기반 FastAPI 프로젝트 구축입니다.

task/ 폴더의 다음 파일들을 확인하여 작업 맥락을 복원해주세요:
1. task/README.md - 전체 요구사항 요약
2. task/checklist.md - 현재 진행 상황 및 체크리스트
3. task/work-log.md - 실시간 작업 로그
4. task/context-management.md - Context 관리 전략

현재 진행 중인 작업과 다음 단계를 파악한 후, 작업을 계속 진행해주세요.
```

### 🔍 **상세 프롬프트 (더 많은 정보가 필요한 경우)**
```
안녕하세요. Context가 끊겼습니다. 

현재 작업 중인 프로젝트는 "독거노인 통합 돌봄 서비스 백엔드 시스템"을 위한 Docker Compose 기반 FastAPI 프로젝트 구축입니다.

다음 정보를 확인하여 작업 맥락을 복원해주세요:

**프로젝트 개요:**
- 목적: 독거노인 통합 돌봄 서비스 백엔드 시스템
- 기술: Docker Compose + FastAPI + SQLAlchemy + Alembic
- 아키텍처: 클린 아키텍처 + 의존성 주입
- 환경: local/dev/prod 분리

**현재 상황 파악을 위해 확인할 파일들:**
1. task/README.md - 전체 요구사항 요약
2. task/checklist.md - 현재 진행 상황 및 체크리스트
3. task/work-log.md - 실시간 작업 로그
4. task/context-management.md - Context 관리 전략
5. task/requirements-summary.md - 요구사항 상세 요약

**특별히 확인해야 할 사항:**
- 현재 진행 중인 Phase와 단계
- 완료된 작업과 남은 작업
- 최근 의사결정 사항
- 다음 작업 계획

위 파일들을 확인한 후, 현재 상황을 요약하고 다음 단계를 제안해주세요.
```

### ⚡ **간단한 프롬프트 (빠른 복원이 필요한 경우)**
```
Context 끊김. task/ 폴더의 checklist.md와 work-log.md를 확인하여 현재 작업 상황을 파악하고 계속 진행해주세요.
```

---

## 🎯 **사용 방법**

### 1. **Context가 완전히 끊긴 경우**
- **상세 프롬프트** 사용
- 전체 맥락을 파악한 후 작업 재개

### 2. **일부 맥락만 끊긴 경우**
- **기본 프롬프트** 사용
- 핵심 정보만 확인 후 작업 재개

### 3. **빠른 복원이 필요한 경우**
- **간단한 프롬프트** 사용
- 최소한의 정보로 빠른 복원

---

## 📁 **파일 구조 요약**

```
task/
├── README.md                    # 전체 요구사항 요약
├── checklist.md                 # 현재 진행 상황 및 체크리스트
├── work-log.md                  # 실시간 작업 로그
├── context-management.md         # Context 관리 전략
├── requirements-summary.md       # 요구사항 상세 요약
└── context-restore-prompt.md    # 이 파일 (Context 복원 프롬프트)
```

---

## 💡 **프롬프트 사용 팁**

1. **Context 끊김 감지 시**: 즉시 위 프롬프트 중 하나를 사용
2. **프롬프트 선택**: 상황에 맞는 적절한 프롬프트 선택
3. **맥락 복원 후**: 작업 로그에 Context 복원 기록
4. **예방**: 정기적으로 작업 상황 요약하여 Context 유지

이 프롬프트를 사용하면 Context가 끊겨도 빠르게 맥락을 복원하고 작업을 계속할 수 있습니다.

