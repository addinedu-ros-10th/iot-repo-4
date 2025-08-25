# Flutter Dashboard 중심 User-App

## 📱 **프로젝트 개요**

Flutter 기반으로 개발된 보호자/관리자 앱으로, 실시간 모니터링 기능을 제공합니다. 생활 요약과 안심 메시지, 원격 제어 기능을 통해 보호자의 편의를 극대화하며, 돌봄 대상자 전체에 대한 집계성 분석과 개인별 분석이 가능합니다.

### **주요 특징**
- 🏠 **실시간 모니터링**: IoT 센서 데이터 기반 실시간 홈 상태 모니터링
- 📊 **대시보드 중심**: 직관적이고 정보가 풍부한 대시보드 제공
- 🚨 **위기 상황 감지**: 스마트 홈 센서 데이터 기반 위기 상황 조기 경보
- 📈 **생활 패턴 분석**: 6개월간의 초단위 센싱 데이터 기반 패턴 분석
- 👥 **권한 기반 접근**: 사용자 역할과 관계에 따른 데이터 접근 제어

## 🎯 **주요 기능**

### **1. 인증 및 권한 관리**
- 사용자 로그인/로그아웃
- 역할별 권한 관리 (admin, caregiver, care_target, family)
- 관계 기반 데이터 접근 제어

### **2. 대시보드 (핵심 기능)**
- **개인 대시보드**: 돌봄 대상자 개인의 실시간 센서 데이터 표시
- **전체 집계 대시보드**: 돌봄 대상자 전체의 상태 모니터링 및 위기 상황 우선순위 정렬

### **3. 스케줄 관리**
- 복약 일정 관리
- 병원 방문 일정 관리
- 돌봄 제공자/담당자 방문 일정 관리

## 🏗️ **기술 스택**

### **프론트엔드**
- **프레임워크**: Flutter Web
- **상태 관리**: Provider/Riverpod
- **HTTP 클라이언트**: Dio
- **차트 라이브러리**: Flutter Charts
- **UI 컴포넌트**: Material Design 3

### **백엔드 연동**
- **API**: RESTful API (기존 WAS Server)
- **인증**: JWT Token
- **실시간 데이터**: WebSocket 또는 Server-Sent Events
- **데이터 캐싱**: Local Storage + Memory Cache

## 📁 **프로젝트 구조**

```
apps/user-app/
├── lib/
│   ├── models/           # 데이터 모델
│   ├── services/         # API 서비스
│   ├── providers/        # 상태 관리
│   ├── screens/          # 화면 컴포넌트
│   ├── widgets/          # 재사용 위젯
│   ├── utils/            # 유틸리티 함수
│   └── constants/        # 상수 정의
├── objective/            # 개발 목표 및 계획 문서
│   ├── app-development-overview.md      # 개발 개요
│   ├── implementation-checklist.md      # 구현 체크리스트
│   └── development-progress.md          # 개발 진행 상황
├── test/                 # 테스트 파일
├── web/                  # 웹 전용 설정
├── pubspec.yaml          # 의존성 설정
└── README.md             # 프로젝트 문서
```

## 🚀 **시작하기**

### **필수 요구사항**
- Flutter SDK 3.10.0 이상
- Dart SDK 3.0.0 이상
- Node.js 16.0.0 이상 (웹 빌드용)
- Chrome 브라우저 (개발 및 테스트용)

### **설치 및 실행**

#### **1. Flutter 환경 설정**
```bash
# Flutter SDK 설치 확인
flutter doctor

# Flutter Web 활성화
flutter config --enable-web
```

#### **2. 프로젝트 클론 및 의존성 설치**
```bash
# 프로젝트 디렉토리로 이동
cd apps/user-app

# 의존성 설치
flutter pub get
```

#### **3. 개발 서버 실행**
```bash
# 웹 개발 서버 실행
flutter run -d chrome

# 또는 특정 포트로 실행
flutter run -d chrome --web-port 8080
```

#### **4. 프로덕션 빌드**
```bash
# 웹 빌드 생성
flutter build web

# 빌드된 파일은 build/web/ 디렉토리에 생성됩니다
```

## 🔧 **개발 가이드**

### **개발 환경 설정**

#### **VS Code 설정**
1. Flutter 및 Dart 확장 프로그램 설치
2. Flutter SDK 경로 설정
3. 디버깅 설정 구성

#### **Chrome DevTools 설정**
1. Chrome에서 개발자 도구 열기 (F12)
2. Flutter Inspector 탭 활성화
3. 디버깅 및 성능 분석 도구 활용

### **코드 스타일 가이드**

#### **네이밍 컨벤션**
- **클래스명**: PascalCase (예: `UserDashboard`)
- **변수명**: camelCase (예: `userName`)
- **상수명**: SCREAMING_SNAKE_CASE (예: `API_BASE_URL`)
- **파일명**: snake_case (예: `user_dashboard.dart`)

#### **폴더 구조 규칙**
- **models/**: 데이터 모델 클래스
- **services/**: API 호출 및 비즈니스 로직
- **providers/**: 상태 관리 Provider
- **screens/**: 전체 화면 컴포넌트
- **widgets/**: 재사용 가능한 위젯
- **utils/**: 유틸리티 함수 및 헬퍼
- **constants/**: 상수 정의

### **상태 관리 패턴**

#### **Provider 사용법**
```dart
// 상태 정의
class UserProvider extends ChangeNotifier {
  User? _user;
  User? get user => _user;

  void setUser(User user) {
    _user = user;
    notifyListeners();
  }
}

// 위젯에서 사용
class UserProfileScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Consumer<UserProvider>(
      builder: (context, userProvider, child) {
        final user = userProvider.user;
        if (user == null) {
          return CircularProgressIndicator();
        }
        return Text('Welcome, ${user.name}');
      },
    );
  }
}
```

### **API 연동 패턴**

#### **HTTP 클라이언트 설정**
```dart
// Dio 인스턴스 설정
final dio = Dio(BaseOptions(
  baseUrl: 'http://localhost/api',
  connectTimeout: Duration(seconds: 5),
  receiveTimeout: Duration(seconds: 3),
));

// 인터셉터 설정
dio.interceptors.add(InterceptorsWrapper(
  onRequest: (options, handler) {
    // 토큰 추가
    final token = getToken();
    if (token != null) {
      options.headers['Authorization'] = 'Bearer $token';
    }
    handler.next(options);
  },
  onError: (error, handler) {
    // 에러 처리
    if (error.response?.statusCode == 401) {
      // 토큰 만료 처리
      logout();
    }
    handler.next(error);
  },
));
```

## 🧪 **테스트**

### **테스트 실행**
```bash
# 단위 테스트 실행
flutter test

# 특정 테스트 파일 실행
flutter test test/widget_test.dart

# 커버리지 리포트 생성
flutter test --coverage
```

### **테스트 작성 가이드**

#### **위젯 테스트 예시**
```dart
testWidgets('Login form validation test', (WidgetTester tester) async {
  await tester.pumpWidget(LoginScreen());

  // 로그인 버튼이 비활성화되어 있는지 확인
  final loginButton = find.byType(ElevatedButton);
  expect(tester.widget<ElevatedButton>(loginButton).enabled, false);

  // 이메일 입력
  await tester.enterText(find.byKey(Key('email_field')), 'test@example.com');
  await tester.pump();

  // 비밀번호 입력
  await tester.enterText(find.byKey(Key('password_field')), 'password123');
  await tester.pump();

  // 로그인 버튼이 활성화되었는지 확인
  expect(tester.widget<ElevatedButton>(loginButton).enabled, true);
});
```

## 📱 **배포**

### **웹 배포**

#### **1. 빌드 생성**
```bash
flutter build web --release
```

#### **2. 배포 옵션**
- **정적 호스팅**: Netlify, Vercel, GitHub Pages
- **웹 서버**: Nginx, Apache
- **클라우드**: AWS S3, Google Cloud Storage

#### **3. 환경별 설정**
```bash
# 개발 환경
flutter run -d chrome --dart-define=ENVIRONMENT=development

# 프로덕션 환경
flutter build web --dart-define=ENVIRONMENT=production
```

## 📚 **문서 및 리소스**

### **프로젝트 문서**
- [개발 개요](objective/app-development-overview.md) - 프로젝트 전체 개요 및 요구사항
- [구현 체크리스트](objective/implementation-checklist.md) - 구현해야 할 기능들의 상세 체크리스트
- [개발 진행 상황](objective/development-progress.md) - 개발 진행률 및 일정 관리

### **Flutter 관련 리소스**
- [Flutter 공식 문서](https://flutter.dev/docs)
- [Flutter Web 가이드](https://flutter.dev/web)
- [Dart 언어 가이드](https://dart.dev/guides)
- [Material Design 3](https://m3.material.io/)

### **API 문서**
- [WAS Server API 문서](http://localhost/docs) - 백엔드 API 스펙
- [Swagger UI](http://localhost/docs) - API 테스트 및 문서

## 🤝 **기여하기**

### **개발 프로세스**
1. 이슈 생성 또는 기존 이슈 확인
2. 기능 브랜치 생성 (`feature/기능명`)
3. 코드 작성 및 테스트
4. Pull Request 생성
5. 코드 리뷰 및 머지

### **코드 리뷰 체크리스트**
- [ ] 코드 스타일 가이드 준수
- [ ] 적절한 테스트 작성
- [ ] 문서 업데이트
- [ ] 성능 영향 검토
- [ ] 보안 취약점 검토

## 🐛 **문제 해결**

### **일반적인 문제들**

#### **1. Flutter Web 빌드 실패**
```bash
# Flutter 클린 및 재빌드
flutter clean
flutter pub get
flutter build web
```

#### **2. 의존성 충돌**
```bash
# 의존성 트리 확인
flutter pub deps

# 의존성 업데이트
flutter pub upgrade
```

#### **3. 웹 성능 이슈**
- Flutter Inspector를 사용한 렌더링 성능 분석
- 불필요한 rebuild 방지를 위한 `const` 위젯 사용
- 이미지 최적화 및 lazy loading 구현

## 📞 **지원 및 연락처**

### **개발팀**
- **프로젝트 매니저**: [이름] - [이메일]
- **프론트엔드 개발자**: [이름] - [이메일]
- **백엔드 개발자**: [이름] - [이메일]

### **이슈 보고**
- [GitHub Issues](https://github.com/your-repo/issues) - 버그 리포트 및 기능 요청
- [프로젝트 위키](https://github.com/your-repo/wiki) - 상세 문서 및 가이드

---

**프로젝트 버전**: 1.0.0  
**마지막 업데이트**: 2025-08-23  
**라이선스**: MIT License
