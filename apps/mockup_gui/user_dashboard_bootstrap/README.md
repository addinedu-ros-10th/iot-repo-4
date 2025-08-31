# 🚀 IoT Care Bootstrap Dashboard

## 📋 **프로젝트 개요**
현대적이고 세련된 Bootstrap 기반의 IoT Care 모니터링 대시보드입니다. Glassmorphism 디자인과 모던한 UI/UX를 적용하여 사용자 경험을 향상시켰습니다.

## ✨ **주요 특징**

### **🎨 현대적 디자인**
- **Glassmorphism**: 반투명 유리 효과와 블러 효과
- **Gradient Colors**: 세련된 그라데이션 컬러 팔레트
- **Dark Mode First**: 다크 테마 우선 디자인
- **Responsive Grid**: 반응형 Bento Grid 레이아웃

### **🚀 고급 기능**
- **Real-time Updates**: 실시간 데이터 업데이트
- **Interactive Charts**: Chart.js 기반 인터랙티브 차트
- **Smooth Animations**: AOS 라이브러리 기반 부드러운 애니메이션
- **Micro-interactions**: 호버 효과 및 전환 애니메이션

### **📱 사용자 경험**
- **Loading States**: 스켈레톤 로딩 애니메이션
- **Toast Notifications**: 사용자 친화적인 알림 시스템
- **Responsive Design**: 모든 디바이스에서 최적화된 경험
- **Accessibility**: 접근성 고려한 UI/UX

## 🏗️ **기술 스택**

### **Backend**
- **Flask**: Python 웹 프레임워크
- **PostgreSQL**: 데이터베이스
- **psycopg2**: PostgreSQL Python 드라이버

### **Frontend**
- **Bootstrap 5.3.2**: CSS 프레임워크
- **Chart.js**: 데이터 시각화
- **AOS**: 스크롤 애니메이션
- **Bootstrap Icons**: 아이콘 라이브러리

### **JavaScript**
- **ES6+**: 모던 JavaScript 문법
- **Async/Await**: 비동기 처리
- **Class-based Architecture**: 객체지향 설계

## 🚀 **시작하기**

### **1. 환경 설정**
```bash
# 프로젝트 디렉토리로 이동
cd apps/mockup_gui/user_dashboard_bootstrap

# 가상환경 생성 (선택사항)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 또는
venv\Scripts\activate     # Windows

# 의존성 설치
pip install -r requirements.txt
```

### **2. 환경 변수 설정**
```bash
# .env 파일 생성
DB_HOST=192.168.0.2
DB_PORT=15432
DB_USER=svc_dev
DB_PASSWORD=IOT_dev_123!@#
DB_NAME=iot_care
```

### **3. 애플리케이션 실행**
```bash
# Flask 앱 실행
python app.py

# 브라우저에서 접속
# http://localhost:5001
```

## 📁 **프로젝트 구조**

```
user_dashboard_bootstrap/
├── app.py                 # Flask 메인 애플리케이션
├── requirements.txt       # Python 의존성
├── README.md             # 프로젝트 문서
├── templates/
│   └── index.html        # 메인 대시보드 템플릿
└── static/
    └── js/
        └── dashboard.js  # 대시보드 JavaScript 로직
```

## 🎨 **디자인 시스템**

### **컬러 팔레트**
- **Primary**: `#667eea` → `#764ba2` (그라데이션)
- **Secondary**: `#f093fb` → `#f5576c` (그라데이션)
- **Success**: `#4facfe` → `#00f2fe` (그라데이션)
- **Warning**: `#43e97b` → `#38f9d7` (그라데이션)
- **Danger**: `#fa709a` → `#fee140` (그라데이션)

### **타이포그래피**
- **Font Family**: Inter, -apple-system, BlinkMacSystemFont
- **Gradient Text**: 그라데이션 효과가 적용된 제목
- **Responsive Typography**: 화면 크기에 따른 반응형 텍스트

### **컴포넌트**
- **Glass Cards**: 반투명 유리 효과 카드
- **Status Indicators**: 애니메이션이 있는 상태 표시기
- **Custom Buttons**: 글래스 효과 버튼
- **Loading Skeletons**: 스켈레톤 로딩 애니메이션

## 🔧 **API 엔드포인트**

### **대시보드 통계**
- `GET /api/dashboard/stats` - 대시보드 통계 데이터

### **사용자 관리**
- `GET /api/users` - 사용자 목록
- `GET /api/users/<user_id>/relationships` - 사용자 관계
- `GET /api/users/<user_id>/timeline` - 사용자 타임라인

## 📊 **대시보드 구성**

### **1. 헤더 섹션**
- 프로젝트 제목 및 설명
- 시스템 상태 표시
- 실시간 시계

### **2. 통계 카드**
- 전체 사용자 수
- 활성 디바이스 수
- 오늘 알림 수
- 위기 상황 수

### **3. 메인 그리드**
- 센서 데이터 차트
- 사용자 목록
- 최근 활동
- 시스템 상태

## 🎯 **향후 개선 계획**

### **Phase 1: 기본 기능** ✅
- [x] 현대적 UI/UX 디자인
- [x] 반응형 레이아웃
- [x] 기본 차트 및 데이터 표시
- [x] 실시간 업데이트

### **Phase 2: 고급 기능** 🔄
- [ ] 사용자 상세 정보 모달
- [ ] 데이터 필터링 및 검색
- [ ] 설정 페이지
- [ ] 테마 커스터마이징

### **Phase 3: 확장 기능** ⏳
- [ ] 실시간 알림 시스템
- [ ] 데이터 내보내기
- [ ] 사용자 권한 관리
- [ ] 다국어 지원

## 🌟 **디자인 참고 자료**

### **Inspiration Sources**
- **Dribbble**: https://dribbble.com/tags/glassmorphism
- **Behance**: https://www.behance.net/search/projects?search=glassmorphism
- **Awwwards**: https://www.awwwards.com/websites/glassmorphism/

### **Color Palettes**
- **Coolors**: https://coolors.co/palettes/trending
- **Color Hunt**: https://colorhunt.co/palettes/dark

### **UI Components**
- **Bootstrap**: https://getbootstrap.com/docs/5.3/
- **Bootstrap Icons**: https://icons.getbootstrap.com/

## 📝 **라이선스**
이 프로젝트는 MIT 라이선스 하에 배포됩니다.

---

**개발자**: AI Assistant  
**최종 업데이트**: 2025-08-25  
**프로젝트**: IoT Care Bootstrap Dashboard


