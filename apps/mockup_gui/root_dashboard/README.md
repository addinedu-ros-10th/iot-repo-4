# Root Dashboard

이 폴더는 원래 루트 디렉토리에 있던 Flask 대시보드 애플리케이션입니다.

## 📁 폴더 구조

```
root_dashboard/
├── app.py              # Flask 메인 애플리케이션
├── templates/          # HTML 템플릿
│   └── index.html     # 메인 대시보드 페이지
├── static/            # 정적 파일
│   └── js/           # JavaScript 파일
│       └── dashboard.js # 대시보드 기능
├── requirements.txt   # Python 의존성
└── README.md         # 이 파일
```

## 🚀 실행 방법

```bash
cd apps/mockup_gui/root_dashboard
pip install -r requirements.txt
python app.py
```

## 🌐 접속 URL

- 로컬: http://localhost:5000
- 네트워크: http://[IP]:5000

## 📋 주요 기능

- 사용자 대시보드
- 데이터베이스 연결 (PostgreSQL)
- 사용자 관리
- 실시간 데이터 모니터링
