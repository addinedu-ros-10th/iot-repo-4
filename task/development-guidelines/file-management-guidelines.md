# 파일/폴더 관리 개발 지침

## 📋 개요

프로젝트 내 파일/폴더의 생성, 이동, 삭제 작업 시 참조 관계를 확인하고 경로 문제를 방지하기 위한 지침입니다.

## ⚠️ 필수 사전 검사 항목

### **1. 참조 관계 검사**
파일/폴더 작업 전 반드시 다음을 확인해야 합니다:

#### **1-1. 해당 파일을 참조하는 파일들 검사**
```bash
# 프로젝트 전체에서 특정 파일/폴더를 참조하는 파일들 검색
grep_search -query "파일명|폴더명" -include_pattern "*.py,*.js,*.html,*.md,*.sh,*.bat"
```

#### **1-2. 해당 파일이 참조하는 파일들 검사**
```bash
# 특정 파일 내에서 참조하는 경로들 검사
grep_search -query "\.\./|/home/|/Users/|C:\\|D:\\" -include_pattern "*.py,*.js,*.html,*.md,*.sh,*.bat"
```

### **2. 경로 문제 유형별 대응**

#### **2-1. 상대 경로 문제**
- **문제**: `../.env.local`, `../config/` 등 상대 경로 사용
- **해결**: 절대 경로 또는 프로젝트 루트 기준 경로로 수정
- **예시**: `../.env.local` → `../../.env.local` 또는 `os.path.join(project_root, '.env.local')`

### **2-4. 중복 파일 문제**
- **문제**: 파일명이 같지만 내용이나 기능이 다른 파일들
- **해결**: 내용 분석 후 기능별로 다른 이름으로 구분
- **예시**: 
  - `test_api_status.py` (포트 미지정) → `test_api_status_local.py`
  - `test_api_status.py` (포트 8000) → `test_api_status_port8000.py`
  - `test_connection.py` (백엔드) → `test_backend_connection.py`
  - `test_connection.py` (Flask) → `test_flask_connection.py`

#### **2-2. 하드코딩된 경로 문제**
- **문제**: `/home/user/project/`, `C:\project\` 등 하드코딩된 경로
- **해결**: 환경 변수 또는 동적 경로 생성으로 수정
- **예시**: `os.environ.get('PROJECT_ROOT')` 또는 `os.path.dirname(os.path.abspath(__file__))`

#### **2-3. API 엔드포인트 경로 문제**
- **문제**: 하드코딩된 API URL (`http://localhost:5000`, `/api/users` 등)
- **해결**: 설정 파일 또는 환경 변수를 통한 동적 관리
- **예시**: `config.API_BASE_URL`, `os.environ.get('API_HOST')`

## 🔍 작업 절차

### **1단계: 현재 위치 확인 (필수!)**
```bash
# 1. 현재 작업 디렉토리 확인
pwd

# 2. 프로젝트 루트 확인
echo "프로젝트 루트: $(git rev-parse --show-toplevel)"

# 3. 대상 파일/폴더 존재 확인
ls -la 대상_파일명
ls -la 대상_폴더명
```

### **🚀 자동화된 안전 작업 도구 사용 (권장!)**
```bash
# 환경 확인
./scripts/safe_file_operations.sh check

# 안전한 파일 이동
./scripts/safe_file_operations.sh move 소스_파일 대상_경로

# 안전한 파일 복사
./scripts/safe_file_operations.sh copy 소스_파일 대상_경로

# 안전한 파일 삭제
./scripts/safe_file_operations.sh delete 대상_파일
```

### **🔍 외부 참조 확인 절차 (파일명 변경 시 필수!)**
```bash
# 1. 변경 전 파일명으로 전체 프로젝트 검색
grep_search -query "변경할_파일명" -include_pattern "*.py,*.md,*.sh,*.txt,*.yml,*.yaml,*.json"

# 2. 검색 결과 분석
# - 파일 참조 (import, include 등)
# - 실행 명령 (python, sh 등)
# - 문서 참조 (README, 가이드 등)

# 3. 각 참조 파일 수정
# - 파일명 변경
# - 경로 수정
# - 실행 명령 수정

# 4. 수정 후 재검증
grep_search -query "새_파일명" -include_pattern "*.py,*.md,*.sh,*.txt,*.yml,*.yaml,*.json"
```

### **2단계: 사전 검사**
```bash
# 1. 참조 파일들 검색
grep_search -query "대상_파일명" -include_pattern "*"

# 2. 경로 문제 검사
grep_search -query "\.\./|/home/|/Users/|C:\\|D:\\" -include_pattern "*"

# 3. 의존성 파일들 확인
# - requirements.txt
# - import 문
# - 설정 파일
# - 환경 변수 파일

# 4. 외부 참조 확인 (중요!)
grep_search -query "변경할_파일명" -include_pattern "*.py,*.md,*.sh,*.txt,*.yml,*.yaml,*.json"
```

### **2단계: 경로 문제 수정**
```bash
# 1. 상대 경로 수정
search_replace -file_path "파일경로" -old_string "잘못된_경로" -new_string "수정된_경로"

# 2. 환경 변수 설정
# .env 파일에 PROJECT_ROOT, API_HOST 등 추가

# 3. 설정 파일 생성
# config.py 또는 settings.py에 경로 설정 추가
```

### **3단계: 파일/폴더 작업**
```bash
# 1. 백업 생성 (필요시)
cp -r 원본_경로 백업_경로

# 2. 파일/폴더 이동/생성/삭제
mv 원본_경로 대상_경로
mkdir -p 새_폴더_경로
rm -rf 삭제할_폴더

# 3. 작업 후 검증
# - 파일 존재 확인
# - 경로 참조 확인
# - 실행 테스트
```

### **4단계: 사후 검증**
```bash
# 1. 파일 구조 확인
tree 대상_폴더

# 2. 경로 문제 재검사
grep_search -query "\.\./|/home/|/Users/|C:\\|D:\\" -include_pattern "*"

# 3. 실행 테스트
python 대상_파일.py
# 또는
sh 대상_스크립트.sh
```

## 📁 권장 폴더 구조

### **프로젝트 루트 레벨**
```
project_root/
├── testing/                 # 전체 시스템 테스트
├── services/                # 백엔드 서비스
├── apps/                    # 프론트엔드/웹앱
├── scripts/                 # 실행 스크립트
├── task/                    # 개발 관리 문서
├── doc/                     # 프로젝트 문서
└── .env.local              # 환경 변수
```

### **서비스별 테스트**
```
services/was-server/
├── testing/                 # 서비스별 테스트
├── tests/                   # 단위/통합 테스트
└── integration_test/        # 통합 테스트 결과
```

## 🚨 주의사항

### **1. 절대 경로 사용 금지**
- ❌ `/home/user/project/file.py`
- ❌ `C:\project\file.py`
- ✅ `os.path.join(project_root, 'file.py')`
- ✅ `config.PROJECT_ROOT + '/file.py'`

### **2. 상대 경로 사용 시 주의**
- ❌ `../config/file.conf` (폴더 이동 시 깨질 수 있음)
- ✅ `../../config/file.conf` (명확한 상대 경로)
- ✅ `os.path.join(os.path.dirname(__file__), '..', 'config', 'file.conf')`

### **3. 환경별 설정 분리**
- ✅ `.env.local` (로컬 개발)
- ✅ `.env.production` (운영 환경)
- ✅ `.env.test` (테스트 환경)

## 📝 체크리스트

파일/폴더 작업 전 체크리스트:

- [ ] **현재 위치 확인**: `pwd` 명령으로 작업 디렉토리 확인
- [ ] **프로젝트 루트 확인**: `git rev-parse --show-toplevel`로 루트 경로 확인
- [ ] **대상 파일/폴더 존재 확인**: `ls -la`로 소스 존재 여부 확인
- [ ] **참조 파일들 검사 완료**: `grep_search`로 의존성 확인
- [ ] **경로 문제 식별 및 수정 완료**: 상대 경로 vs 절대 경로 검토
- [ ] **의존성 파일들 확인 완료**: requirements.txt, import 문 등 확인
- [ ] **백업 생성 완료**: 자동 백업 또는 수동 백업 생성
- [ ] **작업 후 검증 완료**: 파일 이동/복사/삭제 결과 확인
- [ ] **중복 파일 확인**: `find . -name "파일명"`으로 중복 검사
- [ ] **중복 파일 내용 분석**: 동일한 파일명이지만 기능이 다른 경우 이름 변경
- [ ] **외부 참조 확인**: 변경된 파일명을 참조하는 모든 파일 검사 및 수정
- [ ] **실행 테스트 완료**: 관련 기능 정상 동작 확인

### **🚀 자동화 도구 사용 시 (권장)**
- [ ] **환경 확인**: `./scripts/safe_file_operations.sh check` 실행
- [ ] **안전 작업**: `./scripts/safe_file_operations.sh [명령]` 사용
- [ ] **결과 검증**: 스크립트 출력 메시지 확인

## 🔗 관련 문서

- [[Development Methodology]] - 개발 방법론
- [[Project Structure]] - 프로젝트 구조
- [[Environment Setup]] - 환경 설정
- [[Testing Guidelines]] - 테스트 지침
