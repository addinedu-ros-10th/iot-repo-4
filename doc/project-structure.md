# 🏗️ 프로젝트 구조 가이드

이 문서는 IoT 프로젝트 4조의 모노레포 구조와 각 프로젝트의 역할에 대한 상세한 설명입니다.

## 📁 전체 프로젝트 구조

```
iot-repo-4/
├── README.md                 # 프로젝트 메인 문서
├── doc/                      # 프로젝트 문서들
│   ├── monorepo-guide.md    # 모노레포 관리 가이드
│   ├── project-structure.md # 프로젝트 구조 설명 (현재 문서)
│   └── ...
├── apps/                     # 애플리케이션 프로젝트들
│   ├── user-app/            # 사용자 모바일/웹 애플리케이션
│   └── pyqt-admin-service/  # PyQt 기반 관제 서비스
├── services/                 # 서버 및 백엔드 서비스들
│   ├── was-server/          # WAS (Web Application Server)
│   └── que-alert-server/    # QUE & ALERT 서버
├── iot-device/              # IoT 디바이스 관련 코드
│   └── arduino/             # 아두이노 펌웨어
├── shared/                   # 공통 라이브러리 및 유틸리티
├── tests/                    # 테스트 코드
└── config/                   # 설정 파일들
```

## 🎯 각 프로젝트 상세 설명

### 📱 apps/user-app
**사용자 모바일/웹 애플리케이션**

- **목적**: 취약계층 사용자가 서비스를 이용할 수 있는 인터페이스
- **기술 스택**: React Native, Flutter, 또는 웹 기술
- **주요 기능**:
  - 사용자 인증 및 프로필 관리
  - IoT 디바이스 상태 모니터링
  - 긴급 상황 알림 및 신고
  - 돌봄 서비스 요청 및 관리

### 🖥️ apps/pyqt-admin-service
**PyQt 기반 관제 서비스**

- **목적**: 관리자가 전체 시스템을 모니터링하고 제어할 수 있는 데스크톱 애플리케이션
- **기술 스택**: Python, PyQt5/PyQt6
- **주요 기능**:
  - IoT 디바이스 실시간 모니터링
  - 사용자 관리 및 권한 설정
  - 시스템 상태 대시보드
  - 알림 및 이벤트 관리

### 🌐 services/was-server
**Web Application Server**

- **목적**: 전체 시스템의 중앙 서버 역할
- **기술 스택**: Node.js, Python Flask/Django, 또는 Java Spring
- **주요 기능**:
  - RESTful API 제공
  - 데이터베이스 연동 및 관리
  - 사용자 인증 및 권한 관리
  - IoT 디바이스와의 통신 중계

### 🔔 services/que-alert-server
**QUE & ALERT 서버**

- **목적**: 메시지 큐 관리 및 알림 서비스
- **기술 스택**: Redis, RabbitMQ, 또는 Apache Kafka
- **주요 기능**:
  - 메시지 큐 관리
  - 실시간 알림 전송
  - 이벤트 스트림 처리
  - 긴급 상황 대응 시스템

### 🔌 iot-device
**IoT 디바이스 관련 코드**

- **목적**: 실제 IoT 하드웨어와 연동되는 코드
- **기술 스택**: Arduino, ESP32, 또는 Raspberry Pi
- **주요 기능**:
  - 센서 데이터 수집
  - 데이터 전송 및 수신
  - 디바이스 상태 모니터링
  - 펌웨어 업데이트

## 🔗 프로젝트 간 의존성

```
user-app ←→ was-server ←→ que-alert-server
    ↑           ↑              ↑
    └─── iot-device ──────────┘
```

### 의존성 설명

1. **user-app ↔ was-server**: 사용자 인증, 데이터 요청/응답
2. **pyqt-admin-service ↔ was-server**: 관리자 기능, 시스템 모니터링
3. **iot-device ↔ was-server**: 센서 데이터 전송, 명령 수신
4. **was-server ↔ que-alert-server**: 알림 및 이벤트 처리

## 📋 개발 환경 설정

### 필수 요구사항

- **Git**: 버전 관리
- **Node.js**: 웹 애플리케이션 개발
- **Python**: PyQt 및 서버 개발
- **Arduino IDE**: IoT 디바이스 개발
- **Docker**: 서비스 컨테이너화 (선택사항)

### 권장 개발 도구

- **VS Code**: 통합 개발 환경
- **Postman**: API 테스트
- **GitHub Desktop**: Git GUI 클라이언트
- **Arduino IDE**: IoT 디바이스 개발

## 🚀 배포 및 운영

### 개발 환경
- 각 프로젝트별 독립적인 개발 서버
- 로컬 데이터베이스 사용
- 테스트용 IoT 디바이스

### 운영 환경
- AWS 또는 클라우드 서비스 활용
- 프로덕션 데이터베이스
- 실제 IoT 디바이스 연동

## 📚 추가 문서

- [모노레포 관리 가이드](./monorepo-guide.md)
- [API 문서](./api-docs.md)
- [배포 가이드](./deployment-guide.md)
- [문제 해결 가이드](./troubleshooting.md)
