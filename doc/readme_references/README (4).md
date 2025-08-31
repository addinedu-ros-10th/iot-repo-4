

# COVA: 차량 인증 및 제어 시스템

**RFID 기반 사용자 인증과 센서 진단을 통해  
운전 가능 여부를 판단하고, 안전한 차량 제어를 실현하는 시스템입니다.**

---

## 📽️ 시연 영상  
[![demo](https://github.com/addinedu-ros-9th/iot-repo-1/raw/main/images/car.png)](https://youtu.be/cT2-3-PcFhQ)

---


## 🔑 핵심 기능 요약

- **RFID 인증**: 등록된 카드만 차량 제어 가능  
- **음주 감지**: 음주 시 차량 시동 차단  
- **차량 제어**: 전진 / 후진 / 좌우회전 / 정지  
- **센서 데이터 기록**: 충격, 온도 등 센서값 DB 저장  
- **GUI 기반 상태 출력**: 실시간 상태 표시  
- **RFID 등록/조회 기능** : 사용자의 RFID카드를 등록하고 조회 
---

## 📑 목차

1. [Overview](#1-overview)  
2. [Key Features](#2-key-features)  
3. [Team Information](#3-team-information)  
4. [Development Environment](#4-development-environment)  
5. [System Design](#5-system-design)  
   - [User Requirements](#51-user-requirements)  
   - [System Requirements](#52-system-requirements)  
   - [System Architecture](#53-system-architecture)  
   - [Scenario](#54-scenario)  
   - [GUI](#55-gui)  
6. [Database Design](#6-database-design)  
   - [ER Diagram](#61-er-diagram)  
7. [Interface Specification](#7-interface-specification)  
8. [Test Cases](#8-test-cases)  
9. [Problems and Solutions](#9-problems-and-solutions)  
10. [Limitations](#10-limitations)  
11. [Conclusion and Future Work](#11-conclusion-and-future-work)

---

## 1. Overview

COVA는 운전자 인증과 상태 확인을 바탕으로 차량의 **안전한 사용을 제어 및 기록**하는 시스템입니다.  
아두이노 기반 센서와 RFID 인증 장치로 구성되며, 사용자 행동 기록 및 안전 상태를 종합적으로 판단합니다.
---

## 2. Key Features

- RFID 기반 사용자 인증
- 음주 여부 확인 (MQ2)
- 온도/조도/충격 센서 데이터 수집
- 모터 기반 차량 이동 제어
- GUI 기반 실시간 시각 피드백
- DB 연동 센서 기록

---

## 3. Team Information

| 이름   | 역할 구분 | 담당 업무 |
|--------|-----------|-----------|
| 유영훈 | 팀장      | - RFID 인증 기능 개발<br>- 음주 판단 기능 개발<br>- 소프트웨어<br>- Test Case 작성<br>- README 문서 작성 |
| 김진언 | 팀원      | - 서버 기능 개발<br>- DB 구축<br>- 소프트웨어 통합 및 검증 |
| 김태호 | 팀원      | - RFID 등록 기능 및 GUI 개발<br>- DB 연동 및 관리<br>- 발표자료 제작<br>- Scenario / ERD / GUI 문서 작성 |
| 이동연 | 팀원      | - Headlight 제어 기능 개발<br>- Reverse Alert 기능 개발<br>- Temperature 탐지 기능 개발<br>- 발표자료 제작<br>- Interface 명세서 작성 |
| 이동훈 | 팀원      | - Motor Control 및 GUI 개발<br>- Shock 탐지 기능 개발<br>- 소프트웨어 통합<br>- System Architecture 문서 작성<br>- System / User Requirements 작성 |

---

## 4. Development Environment



### 4.1 하드웨어 구성

| 항목   | 구성 목록                                                        |
|--------|------------------------------------------------------------------|
| PC     | 3대                                                              |
| 보드   | Arduino Uno, Arduino Mega                                        |
| 센서   | 가스 센서, 조도 센서, 온도 센서, 초음파 센서, RFID 센서         |
| 모터   | 모터, 모터 드라이버                                              |
| 기타   | LED, 부저                                                        |


### 4.2 소프트웨어 구성

| 항목            | 구성 내용                              |
|-----------------|-----------------------------------------|
| 프로그래밍 언어 | C++ (Arduino), Python (서버/검증)       |
| 데이터베이스    | MySQL                                   |
| 개발 도구       | Arduino IDE, VSCode, Git, GitHub        |


### 4.3 개발 도구 및 기술 스택

| 분류           | 사용 기술                                      |
|----------------|------------------------------------------------|
| 개발 환경      | ![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=flat&logo=ubuntu&logoColor=white) ![VSCode](https://img.shields.io/badge/VSCode-007ACC?style=flat&logo=visual-studio-code&logoColor=white) |
| 언어           | ![C++](https://img.shields.io/badge/C++-00599C?style=flat&logo=cplusplus&logoColor=white) ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) |
| 서버 및 백엔드 | ![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white) |
| 데이터베이스   | ![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=flat&logo=mysql&logoColor=white) |
| 형상 관리      | ![Git](https://img.shields.io/badge/Git-F05032?style=flat&logo=git&logoColor=white) ![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white) |
| 협업 도구      | ![Confluence](https://img.shields.io/badge/Confluence-172B4D?style=flat&logo=confluence&logoColor=white) ![Jira](https://img.shields.io/badge/Jira-0052CC?style=flat&logo=jira&logoColor=white) ![Slack](https://img.shields.io/badge/Slack-4A154B?style=flat&logo=slack&logoColor=white) |

---
## 5. System Design


### 5.1 User Requirements

| ID   | Description                                                          |
|------|----------------------------------------------------------------------|
| UR_1 | 사용자 정보와 사용자 고유의 카드키 정보를 Main PC 데이터 베이스에 추가/삭제할 수 있다 |
| UR_2 | 등록된 사용자의 정보는 조회할 수 있다                                      |
| UR_3 | 등록된 사용자는 고유의 카드로 등록된 차량을 제어할 수 있다                      |
| UR_4 | 등록된 사용자가 차량을 제어하기 위해서는 음주 유무를 판단 후에 제어권을 제공 받아야 한다 |
| UR_5 | 등록된 사용자가 음주 후 차량 제어 시도 시 차량 제어권을 부여하지 않고 위치 정보를 Main PC에 보내줘야 한다 |
| UR_6 | 등록된 사용자가 차량 제어 중 생성되는 정보들을 데이터 베이스에 저장할 수 있다 |
| UR_7 | 사용자가 차량 제어 중 생기는 이벤트를 Main PC에서 인지하고 후속 처리 서비스를 제공할 수 있다 |


### 5.2 System Requirements

| ID   | Function    | Description                                              |
|------|-------------|----------------------------------------------------------|
| SR_1 | 사용자 관리      | 입력된 정보(신규 사용자 정보) 등록<br>등록된 사용자인 경우 정보 조회<br>운전습관 데이터 조회<br>사용자 삭제 |
| SR_2 | 차량 도어락      | 등록된 사용자인 경우 차량 도어락 해제                              |
| SR_3 | 음주운전 예방     | 사용자의 음주상태 확인<br>음주 아님 확인 후 차량 시동 가능<br>음주 시 위치정보 전송 |
| SR_4 | 충격 감지       | 차량에 가해지는 충격 횟수 및 시간 기록                                |
| SR_5 | 온도 감지       | 차량 부품 온도 감지 및 임계값 초과 시 경고                            |
| SR_6 | 자동 헤드라이트    | 빛이 일정 이하일 때 헤드라이트 ON                            |
| SR_7 | 주차 및 운행 보조  | 초음파로 장애물 감지 → 청각/시각 경고                       |
| SR_8 | 사고 발생 처리 기능 | 충격/온도/가스 등 이상 감지 시 위치 정보 전송                     |
| SR_9 | 위험 경고       | 센서 경고 메시지를 부저 및 GUI로 송출                             |



### 5.3 System Architecture

#### 5.3.1 Hardware Architecture
 ![HW_architecture](https://github.com/addinedu-ros-9th/iot-repo-1/blob/main/images/HW_architecture.png)

#### 5.3.2 Software Architecture
 ![SW_architecture](https://github.com/addinedu-ros-9th/iot-repo-1/blob/main/images/SW_architecture.png)


### 5.4 Scenario

#### 5.4.1 RFID Register and Browse
![RFID_Register and Browse](https://github.com/addinedu-ros-9th/iot-repo-1/blob/main/images/RFID%20Register%20and%20Browse.png)
#### 5.4.2 Vehicle Authentication
![Vehicle Authentication](https://github.com/addinedu-ros-9th/iot-repo-1/blob/main/images/Vehicle%20Authentication.png)
#### 5.4.3 Shock and Temperature Management
![Shock and Temperature Management](https://github.com/addinedu-ros-9th/iot-repo-1/blob/main/images/Shock%20and%20Temperature%20Management.png)
#### 5.4.4 Vehicle Control
![Vehicle Control](https://github.com/addinedu-ros-9th/iot-repo-1/blob/main/images/Vehicle%20Control.png))
#### 5.4.5 Headlight Control
![Headlight Control](https://github.com/addinedu-ros-9th/iot-repo-1/blob/main/images/Headlight%20Control.png)
#### 5.4.6 Reverse Control Management
![Reverse Control Management](https://github.com/addinedu-ros-9th/iot-repo-1/blob/main/images/Reverse%20Control%20Management.png)



### 5.5 GUI

### 5.5.1 COVA Admin

#### 5.5.1.1 Admin Default
![Admin Default](https://github.com/addinedu-ros-9th/iot-repo-1/blob/main/images/Admin%20Default.png)
#### 5.5.1.2 RFID check
![RFID Check](https://github.com/addinedu-ros-9th/iot-repo-1/blob/main/images/RFID%20Check.png)
![RFID Check Fail](https://github.com/addinedu-ros-9th/iot-repo-1/blob/main/images/RFID%20Check%20Fail.png)
![RFID Check Duplicate](https://github.com/addinedu-ros-9th/iot-repo-1/blob/main/images/RFID%20Check%20Duplicate.png)
#### 5.5.1.3 Check Button
![Check Button](https://github.com/addinedu-ros-9th/iot-repo-1/blob/main/images/Check%20Button.png)
#### 5.5.1.4 Register Button
![Register Success](https://github.com/addinedu-ros-9th/iot-repo-1/blob/main/images/Register%20Success.png)
![Register Fail](https://github.com/addinedu-ros-9th/iot-repo-1/blob/main/images/Register%20Fail.png)
#### 5.5.1.3 Register Initialize
![Register Initialize](https://github.com/addinedu-ros-9th/iot-repo-1/blob/main/images/Register%20Initialize.png)



### 5.5.2 COVA Jr Control

#### 5.5.2.1 Control Default
![Control Default](https://github.com/addinedu-ros-9th/iot-repo-1/blob/main/images/Control%20Default.png)
#### 5.5.2.2 Door Open
![Door Open](https://github.com/addinedu-ros-9th/iot-repo-1/blob/main/images/Door%20Open.png)
#### 5.5.2.3 Engine Start(On button)
![Engine Start](https://github.com/addinedu-ros-9th/iot-repo-1/blob/main/images/Engine%20Start.png)
#### 5.5.2.3 Headlight On
![Headlight On](https://github.com/addinedu-ros-9th/iot-repo-1/blob/main/images/Headlight%20On.png)
#### 5.5.2.4 Reverse
![Reverse](https://github.com/addinedu-ros-9th/iot-repo-1/blob/main/images/Reverse.png)

---

## 6. Database Design

### 6.1 ER Diagram

### 6.1.1 Admin DB
![Admin DB](https://github.com/addinedu-ros-9th/iot-repo-1/blob/main/images/Admin%20DB.png)
### 6.1.2 Vehicle DB
![Vehicle DB](https://github.com/addinedu-ros-9th/iot-repo-1/blob/main/images/Vehicle%20DB.png)

---

## 7. Interface Specification

### 7.1 Command List

| Command | Full Name        |
|---------|------------------|
| DB      | DataBase         |
| VF      | VeriFication     |
| JS      | JSON             |
| MB      | Move Back        |
| ST      | Stop             |
| UR      | Ultrasonic       |
| LS      | Light Status     |

### 7.2 COVA Jr Sensor_Control <->  COVA Jr Control

#### 7.2.1 Local UID Verification Interface

| Interface No.     | Sender               | Receiver             | Header | Command | UID      | Status   | End   | Length(Bytes) | Description                  |
|-------------------|----------------------|----------------------|--------|---------|----------|----------|-------|----------------|------------------------------|
| -                 | -                    | -                    | 1 Byte | 2 Bytes | 4 Bytes | 1 Byte   | 1 Byte | -              | -                            |
| Rea_Ctrl_VF_01    | COVA Jr SensorControl | COVA Jr Control      | 0xAA   | VF      | Tag UID  | -        | '\\n'  | up to 8        | 등록된 uid인지 확인 요청     |
| Res_Ctrl_VF_01    | COVA Jr Control      | COVA Jr SensorControl | 0xAA   | VF      | -        | Status1* | '\\n'  | up to 8        | 등록된 uid인지 응답          |

##### 7.2.1.1 Status1 Description

| Status1 | Description                      |
|---------|----------------------------------|
| 0x01    | Boolean `true` : 등록 카드       |
| 0x00    | Boolean `false` : 미등록 카드    |


#### 7.2.2 Sensor Logging Interface

| Interface No. | Sender               | Receiver           | Header | Command | UID      | Shock   | Temp    | Length(Bytes) | Description             |
|---------------|----------------------|--------------------|--------|---------|----------|---------|---------|----------------|--------------------------|
| -             | -                    | -                  | 1 Byte | 2 Bytes | 4 Bytes | 4 Bytes | 4 Bytes | -              | -                        |
| Ctrl_DB_01    | COVA Jr SensorControl | COVA Jr Control    | 0xAA   | DB      | Tag UID  | value   | value   | 15 Bytes       | UID 기준 센서값 DB 저장 요청 |


#### 7.2.3 Ultrasonic Command Interface

| Interface No.   | Sender           | Receiver             | Command | End   | Length(Bytes) | Description                             |
|-----------------|------------------|-----------------------|---------|-------|----------------|-----------------------------------------|
| -               | -                | -                     | 2 Bytes | 1 Byte | -              | -                                       |
| Ctrl_Ultra_01   | COVA Jr Control  | COVA Jr SensorControl | MB      | 0x00  | 3 Bytes        | \"후진 시작\" 전송 → 초음파 센서 시작      |
| Ctrl_Ultra_02   | COVA Jr Control  | COVA Jr SensorControl | ST      | 0x00  | 3 Bytes        | \"멈춤\" 전송 → 초음파 센서 멈춤          |

#### 7.2.4 Driving Safefy Sensor Interface

| Interface No.  | Sender               | Receiver            | Header | Command | Value     | Length(Bytes) | Description                        |
|----------------|----------------------|---------------------|--------|---------|-----------|----------------|------------------------------------|
| -              | -                    | -                   | 1 Byte | 2 Bytes | -         | -              | -                                  |
| Ctrl_Alc01     | COVA Jr SensorControl | COVA Jr Control     | 0xAA   | VF      | Status2*  | 4 Bytes        | 음주 여부 전송 (운전 가능 판단용)       |
| Ctrl_Ultra03   | COVA Jr SensorControl | COVA Jr Control     | 0xAA   | UR      | value     | 7 Bytes        | 후방 장애물 거리 전송                  |
| Ctrl_Ls01      | COVA Jr SensorControl | COVA Jr Control     | 0xAA   | LS      | Status2*  | 4 Bytes        | 조도 상태 전송 (야간 여부 판단용 등)   |

##### 7.2.4.1 Status2 Description

| Status2 | Description                     |
|---------|----------------------------------|
| 0x01    | Boolean `true` : pass / on       |
| 0x00    | Boolean `false` : nonpass / off  |

### 7.3 COVA Jr Motor Control  <->  COVA Jr Control
#### 7.3.1 Motor Control Interface

| Interface No.   | Sender          | Receiver            | Value       | Data Type   | Length (Bytes) | Description  |
|-----------------|------------------|----------------------|-------------|-------------|----------------|--------------|
| Ctrl_Motor_01   | COVA Jr Control  | COVA Jr Motor Control | how_move*   | Byte String | 3 Bytes        | 차량 이동 제어 |

##### 7.3.1.1 how_move Description

| how_move   | Description     |
|------------|------------------|
| MF + '\\n' | Move Front       |
| MB + '\\n' | Move Back        |
| TL + '\\n' | Turn Left        |
| TR + '\\n' | Turn Right       |
| MS + '\\n' | Move Stop        |


### 7.4 COVA Jr Control <->COVA Server
#### 7.4.1 Remote UID Verification Interface

| Interface No.         | Sender           | Receiver         | Header | Command | UID      | Status    | End   | Length(Bytes) | Description                     |
|------------------------|------------------|------------------|--------|---------|----------|-----------|-------|----------------|---------------------------------|
| -                      | -                | -                | 1 Byte | 2 Bytes | 4 Bytes | 1 Byte    | 1 Byte | -              | -                               |
| Req_Ctrl_Sr_VF_01      | COVA Jr Control  | COVA Server      | 0xAA   | VF      | Tag UID  | -         | '\\n' | up to 8        | 등록된 UID인지 확인 요청         |
| Res_Ctrl_Sr_VF_01      | COVA Server      | COVA Jr Control  | 0xAA   | VF      | -        | Status1*  | '\\n' | up to 8        | 등록된 UID인지 응답              |

##### 7.4.1.1 Status1 Description

| Status1 | Description                      |
|---------|----------------------------------|
| 0x01    | Boolean `true` : 등록 카드       |
| 0x00    | Boolean `false` : 미등록 카드    |


### 7.5 Tag Reader ->COVA Admin
#### 7.5.1 Admin Registration Interface

| Interface No.     | Sender     | Receiver   | Value    | Data Type | Length (Bytes) | Description               |
|-------------------|------------|------------|----------|-----------|----------------|---------------------------|
| Req_Admin_VF_01   | Tag Reader | COVA Admin | Tag UID  | String    | 4 Bytes        | 사용자의 UID 등록 요청     |

### 7.6 COVA Admin ↔︎ COVA Server
#### 7.6.1 User Data Transfer Interface

| Interface No.         | Sender      | Receiver    | Header | Command | data_length      | Purpose      | Data         | Data Type    | Length(Bytes) | Description            |
|------------------------|-------------|-------------|--------|---------|------------------|--------------|--------------|--------------|----------------|------------------------|
| -                      | -           | -           | 1 Byte | 2 Bytes | 2 Bytes          | -            | *            | -            | -              | -                      |
| Req_Admin_Sr_VF_01     | COVA Admin  | COVA Server | 0xAA   | JS      | -                | verification | Tag UID      | JSON String  | up to 60      | 태그된 UID 전송         |
| Admin_Sr_DB_01         | COVA Admin  | COVA Server | 0xAA   | JS      | len(json_bytes)  | db           | value_data*  | Bytes        | *              | 사용자 정보 등록         |

##### 7.6.1.1 value_data Description

| Column       | Data Type (Bytes) | Description     |
|--------------|-------------------|------------------|
| uid          | JSON string (4)   | 사용자 UID       |
| user_name    | JSON string (10)  | 사용자 이름      |
| birth_date   | JSON string (10)  | 생년월일         |
| height       | JSON number (~6)  | 키               |
| weight       | JSON number (~6)  | 몸무게           |
| phone_num    | JSON string (11)  | 전화번호         |
| license_num  | JSON string (15)  | 면허번호         |

#### 7.6.2 UID Verification Response Interface

| Interface No.       | Sender       | Receiver     | Header | Command | Purpose | Message     | Data Type    | Length(Bytes) | Description         |
|---------------------|--------------|--------------|--------|---------|---------|--------------|---------------|----------------|---------------------|
| Res_Admin_Sr_VF_01  | COVA Server  | COVA Admin   | 0xAA   | -       | -       | PASS / FAIL  | JSON String   | *              | 등록 여부 전송        |

---

## 8. Test Cases

| TC ID  | 주체     | 상호작용 대상            | 행동 (입력)                           | 예상 결과 (대상 포함)                                                              | 실제 결과 |
|--------|----------|--------------------------|----------------------------------------|--------------------------------------------------------------------------------------|------------|
| TC01   | 관리자   | COVA Admin               | 대기 상태                              | [COVA Admin GUI] 유저 정보 등록 폼/확인/등록 버튼 비활성, 초기화 버튼만 활성       | pass       |
| TC02   | 관리자   | TAG Reader               | 미등록 RFID 태깅                       | [COVA Admin GUI] RFID UID 출력, 확인/등록 버튼 활성화                               | pass       |
| TC03   | 관리자   | COVA Admin               | 유저 정보 입력 후 확인 클릭            | [COVA Admin GUI] 표에 유저 정보 출력                                                | pass       |
| TC04   | 관리자   | COVA Admin               | 등록 버튼 클릭                         | [COVA Admin GUI] 등록 성공 팝업 출력                                                | pass       |
| TC05   | 관리자   | COVA Admin               | 등록 성공 팝업 OK 클릭                 | [COVA Admin GUI] 팝업 닫힘, 유저 정보 및 버튼 초기화                                 | pass       |
| TC06   | 관리자   | COVA Admin               | 등록된 RFID 태깅                       | [COVA Admin GUI] 등록 오류 팝업 출력, 기존 사용자 정보 표에 출력                    | fail       |
| TC07   | 관리자   | COVA Admin               | 등록 오류 팝업 OK 클릭                 | [COVA Admin GUI] 팝업 닫힘, 유저 정보 및 표 및 버튼 초기화                          | pass       |
| TC08   | 사용자   | COVA Jr Sensor Control   | 미등록 RFID 태깅                       | [COVA Jr Control GUI] Unregistered 출력                                             | fail       |
| TC09   | 사용자   | COVA Jr Sensor Control   | 등록된 RFID 태깅                       | [COVA Jr Control GUI] Welcome 출력                                                  | pass       |
| TC10   | 사용자   | COVA Jr Sensor Control   | 음주측정 버튼 클릭                     | [COVA Jr Control GUI] 5초 후 Engine Start 출력                                      | pass       |
| TC11   | 사용자   | COVA Jr Control          | W 키 입력                              | [COVA Jr Motor Control] 차량 전진                                                   | pass       |
| TC12   | 사용자   | COVA Jr Control          | W 키 해제                              | [COVA Jr Motor Control] 차량 정지                                                   | pass       |
| TC13   | 사용자   | COVA Jr Control          | A 키 입력                              | [COVA Jr Motor Control] 차량 좌회전                                                 | pass       |
| TC14   | 사용자   | COVA Jr Control          | A 키 해제                              | [COVA Jr Motor Control] 차량 정지                                                   | pass       |
| TC15   | 사용자   | COVA Jr Control          | D 키 입력                              | [COVA Jr Motor Control] 차량 우회전                                                 | pass       |
| TC16   | 사용자   | COVA Jr Control          | D 키 해제                              | [COVA Jr Motor Control] 차량 정지                                                   | pass       |
| TC17   | 사용자   | COVA Jr Control          | S 키 입력 (후면 1m 이내 장애물)        | [COVA Jr Motor Control] 차량 후진, [COVA Jr Sensor Control] 경고음 시작 (거리 비례) | pass       |
| TC18   | 사용자   | COVA Jr Control          | S 키 해제                              | [COVA Jr Motor Control] 차량 정지, [COVA Jr Sensor Control] 경고음 해제             | pass       |

---
## 9. Problems and Solutions

- **문제:** ESP에 너무 많은 테스크를 부여하여 하드웨어 한계에 도달  
  **해결:** ESP를 시스템에서 제외하고, PC 간 **TCP 통신** 방식으로 대체

- **문제:** HTTP 통신 방식은 실시간성이 떨어져 제어에 지연 발생  
  **해결:** 아두이노 ↔ PC 간에는 **시리얼 통신**, PC ↔ PC 간에는 **TCP 통신**을 적용하여 실시간성 확보

- **문제:** 아두이노 Uno 보드 하나로 모든 센서를 제어하고 통신을 처리하는 데 한계 발생  
  **해결:** **센서는 아두이노 Mega**, **모터는 아두이노 Uno**가 담당하도록 하드웨어 역할 분리

---

## 10. Limitations

1. 음주 측정 시 보다 정밀한 측정과 허위로 측정하는 것을 방지하는 방법 추가 필요  
2. 추가적인 서비스를 위한 GPS, 속도, 가속도 센서를 사용한 데이터 추가 필요  
3. 운전자의 개인 정보를 관리하는 서버의 보안 필요  
4. 운전자의 운전 습관을 분석하기 위한 충분한 데이터 확보 필요  
5. 초음파 센서값에 따른 모터 제어 실시간 응답 속도 향상 필요  
6. 저품질의 센서 대신 고품질의 센서를 사용해 정확한 센서값 확보 필요

---

## 11. Conclusion

- 스마트키를 통한 **스마트 인증 시스템 제작에 성공**  
- 다양한 센서 데이터를 **실시간으로 수집 및 저장하는 시스템 구현에 성공**  
- 하드웨어 분산 처리 및 통신 방식 개선을 통해 **시스템 안정성과 확장성 확보**  
- 본 시스템은 **향후 운전자 안전 향상 및 데이터 기반 서비스 확장**의 기반이 될 수 있음


