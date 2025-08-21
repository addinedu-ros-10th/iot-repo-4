# IoT Care Backend System 이슈 및 해결 방안

## 🔴 현재 진행 중인 이슈

### Issue #4: ImportError - Edge 센서 인터페이스 import 실패
**발생 시점**: 2024-12-19 17:00  
**상태**: 🔴 진행 중  
**우선순위**: 높음 (시스템 시작 불가)

#### 문제 상세
```
ImportError: cannot import name 'IEdgeFlameRepository' from 'app.interfaces.repositories.sensor_repository' (/app/app/interfaces/repositories/sensor_repository.py)
```

#### 문제 원인 분석
1. **인터페이스 파일 구조 불일치**: 
   - `container.py`에서 `sensor_repository`에서 Edge 센서 관련 인터페이스를 import하려고 시도
   - 실제로는 각 센서별로 개별 인터페이스 파일이 생성되어야 함
   - `sensor_repository.py`에 Edge 센서 인터페이스가 정의되어 있지 않음

2. **의존성 주입 시스템 오류**:
   - `container.py`의 import 문이 잘못된 경로를 참조
   - 존재하지 않는 인터페이스들을 import하려고 시도

3. **파일 구조 불일치**:
   - API 구현은 완료되었지만, 인터페이스 레이어의 구조가 일치하지 않음

#### 해결 방안
**Phase 1: 인터페이스 파일 구조 정리**
- 각 센서별 개별 인터페이스 파일 확인 및 생성
- `sensor_repository.py` 파일의 내용 확인 및 수정
- 누락된 인터페이스 정의 추가

**Phase 2: 의존성 주입 시스템 수정**
- `container.py`의 import 문 수정
- 올바른 인터페이스 파일에서 import하도록 변경
- 의존성 주입 함수들의 올바른 연결 확인

**Phase 3: 시스템 재시작 및 테스트**
- 수정된 코드로 시스템 재시작
- Import 오류 해결 확인
- API 서버 정상 동작 검증

#### 진행 상황
- [x] 문제 원인 파악
- [x] 해결 계획 수립
- [ ] 인터페이스 파일 구조 정리
- [ ] import 문 수정
- [ ] 시스템 재시작 테스트

#### 예상 완료 시간
- **Phase 1**: 30분
- **Phase 2**: 30분  
- **Phase 3**: 15분
- **총 예상 시간**: 1시간 15분

---

## ✅ 해결된 이슈

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
- [ ] **Issue #4**: ImportError 해결
  - [ ] 인터페이스 파일 구조 정리
  - [ ] import 문 수정
  - [ ] 시스템 재시작 테스트

### 완료된 이슈
- [x] **Issue #3**: psycopg2 설치 오류
- [x] **Issue #2**: Pydantic 버전 호환성 문제  
- [x] **Issue #1**: Clean Architecture 위반 문제

---

## 🚨 향후 주의사항

### 1. 인터페이스 파일 구조 관리
- 각 센서별로 개별 인터페이스 파일 생성 시 일관성 유지
- `container.py`의 import 문과 실제 파일 구조 일치 확인

### 2. 의존성 주입 시스템 검증
- 새로운 API 추가 시 의존성 주입 함수 정상 작동 확인
- import 경로의 정확성 검증

### 3. 시스템 통합 테스트
- API 구현 완료 후 반드시 시스템 통합 테스트 수행
- Import 오류 및 의존성 문제 사전 검증

---

## 📞 지원 및 문의

이슈 해결 과정에서 추가 지원이 필요한 경우:
1. 로그 파일 확인
2. 파일 구조 검증
3. 개발팀에 상세 이슈 리포트 제출

**현재 Issue #4 해결 진행 중이며, 완료 후 시스템 통합 테스트를 진행할 예정입니다.**
