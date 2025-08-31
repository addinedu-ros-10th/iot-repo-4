# README 구성 분석 보고서

## 목적
`doc/readme_references` 내 32개 참조 README의 구조를 내부 파일만으로 분석하여, 현재 프로젝트(`https://github.com/addinedu-ros-10th/iot-repo-4`)에 최적화된 포트폴리오형 README 구성을 제안한다.

## 분석 소스
- 헤딩 요약: `task/readme_refs_headings_summary.md` (32개 반영 완료)
- 원문: `doc/readme_references/README (1..32).md`

## 공통 구성 요소(빈도 상위)
- 프로젝트 개요/소개, 목표/동기, 기간/일정
- 팀 구성/역할
- 기술 스택(언어/프레임워크/DB/툴)
- 기능 리스트/주요 기능
- 요구사항: User Requirements(UR), System Requirements(SR)
- 시스템 설계: System Architecture(HW/SW), Data/ERD, Interface/통신 프로토콜, 상태/시퀀스/시나리오/Flowchart, GUI 설계/화면 구성
- 구현/결과: 하드웨어/기구, GUI, 동작/시연 영상, 결과/결론
- 문제/제약/개선, 테스트(케이스/검증), 발표자료 링크

## 개별(차별화) 요소(특정 프로젝트 중심)
- 도메인 특화: 스마트 주차(화재 연계), SmartDesk(PWM/Linear Actuator), 펫 케어(Feeder/Collar), 스마트 우편함(MQTT), 스마트 어항, 화재 대응(딥러닝/열원), CCTV(TDOA)
- 통신/프로토콜/JSON 패킷 상세 명세
- 제어 이론/알고리즘 설명(FSM/제어 규칙/우선순위)
- 테스트 매핑 표(UR↔SR↔TC)

## 포트폴리오 관점 평가: 포함/배제 기준
- 포함
  - 문제 정의/사회적 배경과 목표: 맥락 전달, 임팩트 강조
  - UR/SR 테이블: 요구사항 추적성, 엔지니어링 과정 증명
  - 아키텍처(HW/SW/배포/네트워크): 통합 설계 역량
  - 인터페이스 명세(TCP/Serial/HTTP/JSON): 시스템 연동 능력
  - 데이터/ERD와 스키마: 데이터 모델링
  - 시나리오/시퀀스/상태도: 행위/흐름 설계
  - 구현 섹션(각 서브시스템별): 역할과 기여 명확화
  - 테스트 계획/케이스/리포트: 검증 문화
  - 문제/해결/제약: 회고와 리스크 대응
  - 데모/스크린샷/영상: 결과 증거
  - 보안/인프라(SSH/DB/WAS/비밀관리): 운영 관점 역량
- 배제/축약
  - 과도한 뱃지/장식 이미지
  - 팀 프로필 장문 소개(핵심 역할 표만 유지)
  - 하드웨어 사진 과다(핵심만 정제)

## 최적 README 목차(필수 구성 완전 반영)
1. 프로젝트 개요(문제/배경/목표/기간/데모 링크)
2. 팀 구성 및 역할(표, 개인 기여 하이라이트)
3. 기술 스택(언어/프레임워크/DB/인프라/툴)
4. 기획(Planning)
   - User Requirement [PDF 참조: `doc/project_materials/기획/*`]
5. 자료조사(Research) [PDF: `doc/project_materials/자료조사/*`]
6. 기술조사(Technology Research) [PDF: `doc/project_materials/기술조사/*`]
7. 설계(Design)
   - System Requirements (SR 표) [PDF: `doc/project_materials/설계/*`]
   - System Architecture (HW/SW/배포) [PDF: 동]
   - System Scenario/Sequence/State [PDF: 동]
   - Interface Specification (TCP/Serial/HTTP/JSON) [PDF: 동]
   - Data Structure/ERD/스키마 [PDF: 동]
   - 화면 구성도/GUI 설계 [PDF: 동]
   - 상황 감지/알림 룰 및 대응 우선순위(FSM/룰 테이블) [PDF: 동]
8. 구현(Implementation)
   - 실내 센서 매핑(센서→기능 매핑표)
   - GitHub 사용(브랜치/컨벤션)
   - FastAPI 사용(API 레퍼런스 스냅샷)
   - DB 접속 보안 가이드(.env/권한/암호화)
   - 인프라 구축(SSH/DB/Security/WAS)
   - WAS 서버 개발(계층/핵심 모듈)
   - IoT Device 개발(보드/펌웨어/프로토콜)
   - PyQt 관제 서비스 개발(뷰/상태/제어)
   - 사용자 서비스 개발(로그인/역할/기능)
9. Validation(검증)
   - Test Plan(케이스 표)
   - Test Report(결과/이슈/완료기준)
10. 발표(Presentation)
    - 슬라이드/영상 링크
11. 설치 및 실행(Quick Start)
12. 라이선스/기여/연락처

## PDF 매핑 가이드(편집 시 바로 인용)
- 기획/자료/기술/설계/구현/발표: `doc/project_materials/<카테고리>/*.pdf`
- 각 목차 하위에 해당 PDF의 표/다이어그램 스냅샷과 요약을 삽입

## 다음 작업(실행 플랜, ~1h)
- 0~10분: `README.md` 목차 스캐폴딩 반영(빈 섹션+앵커)
- 10~40분: PDF별 핵심 표/다이어그램 요약 삽입(설계/검증 우선)
- 40~55분: 구현 하위 섹션 템플릿과 예시 표 삽입(센서 매핑/인터페이스/ERD 스냅샷 자리표시)
- 55~60분: Quick Start/라이선스 정리, 내부 링크 점검

