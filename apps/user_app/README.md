# IoT Care User-App

IoT Care System의 Flutter 기반 사용자 애플리케이션입니다.

## 🚀 빠른 시작

### **방법 1: 자동화 스크립트 사용 (권장)**

#### macOS/Linux
```bash
./scripts/run_flutter.sh
```

#### Windows
```cmd
scripts\run_flutter.bat
```

#### Python (크로스 플랫폼)
```bash
python3 scripts/run_flutter.py
```

### **방법 2: Makefile 사용**
```bash
make help          # 사용 가능한 명령어 확인
make check-path    # 현재 경로 및 Flutter 프로젝트 확인
make fix-path      # 경로 문제 자동 수정
make run           # Chrome에서 Flutter 앱 실행
make setup         # 전체 설정 (의존성 설치 + 환경 진단)
make dev           # 개발 시작 (설정 + 실행)
```

### **방법 3: 수동 실행**
```bash
# 올바른 Flutter 프로젝트 경로로 이동
cd /path/to/iot-repo-4/apps/user_app

# 의존성 설치
flutter pub get

# Chrome에서 실행
flutter run -d chrome --web-port=8084
```

## ⚠️ 중요: Flutter 경로 문제 해결

**🚨 Flutter 명령어를 사용할 때는 반드시 올바른 프로젝트 경로에서 실행해야 합니다!**

### **문제 상황**
```bash
# ❌ 잘못된 방법 - 프로젝트 루트에서 실행
cd /path/to/iot-repo-4
flutter run -d chrome  # Error: No pubspec.yaml file found

# ✅ 올바른 방법 - Flutter 프로젝트 디렉토리에서 실행
cd /path/to/iot-repo-4/apps/user_app
flutter run -d chrome  # 정상 실행
```

### **자동화 스크립트의 장점**
- ✅ 경로 자동 확인 및 수정
- ✅ Flutter 환경 자동 진단
- ✅ 의존성 자동 설치
- ✅ 포트 충돌 자동 해결
- ✅ 크로스 플랫폼 지원

## 🏗️ 프로젝트 구조

```
lib/
├── config/           # 환경 설정
├── data/            # 데이터 계층
│   ├── dtos/        # 데이터 전송 객체
│   ├── services/    # API 서비스
│   └── sources/     # 데이터 소스
├── presentation/     # 프레젠테이션 계층
│   ├── pages/       # 페이지
│   ├── state/       # 상태 관리
│   └── widgets/     # 위젯
└── main.dart        # 앱 진입점
```

## 🎨 주요 기능

- **실시간 모니터링**: IoT 센서 데이터 실시간 표시
- **홈 상태 대시보드**: 모든 센서 상태 통합 모니터링
- **경보 시스템**: 위험 상황 즉시 감지 및 알림
- **사용자 관리**: 돌봄 대상자 및 관계 관리
- **반응형 UI**: 다양한 디바이스 지원

## 🔧 개발 환경

- **Flutter**: 3.2.3+
- **Dart**: 3.2.3+
- **상태 관리**: Provider
- **HTTP 클라이언트**: Dio
- **차트**: fl_chart

## 📱 지원 플랫폼

- ✅ Web (Chrome, Safari, Firefox)
- ✅ Android
- ✅ iOS
- ✅ macOS
- ✅ Windows
- ✅ Linux

## 🚨 문제 해결

### **자주 발생하는 오류**

1. **`Error: No pubspec.yaml file found`**
   - **원인**: Flutter 프로젝트 디렉토리가 아님
   - **해결**: `cd apps/user_app` 또는 자동화 스크립트 사용

2. **`SocketException: Address already in use`**
   - **원인**: 포트 충돌
   - **해결**: 다른 포트 사용 또는 자동화 스크립트 사용

3. **`This application is not configured to build on the web`**
   - **원인**: 웹 지원 미설정
   - **해결**: `flutter config --enable-web`

### **포트 충돌 해결**
```bash
# 사용 중인 포트 확인
lsof -i :8084

# 프로세스 종료
kill -9 <PID>

# 또는 다른 포트 사용
flutter run -d chrome --web-port=8085
```

## 📚 추가 문서

- [개발 현황 문서](../../task/current-development-status.md)
- [API 문서](../../docs/api/README.md)
- [아키텍처 가이드](../../docs/architecture/README.md)

## 🤝 기여하기

1. 이슈 생성 또는 기존 이슈 확인
2. 브랜치 생성 (`feature/기능명`)
3. 코드 작성 및 테스트
4. Pull Request 생성

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.
