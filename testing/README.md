# Testing

이 폴더는 다양한 테스트 스크립트들을 포함합니다.

## 📁 파일 목록

### **integration_test.py**
- IoT Care Backend System RESTFUL API 통합 테스트
- 모든 API 엔드포인트에 대한 CRUD 테스트
- 결과는 `../integration_test/` 폴더에 저장

### **test_api_status.py**
- API 상태 확인 스크립트
- 헬스 체크, Swagger UI, Users API, CDS API 테스트

### **test_app.py**
- Flask 애플리케이션 테스트용 HTTP 클라이언트
- 메인 페이지, 사용자 목록 API, 대시보드 통계 API 테스트

### **test_connection.py**
- Flask 앱 연결 테스트
- 메인 페이지 및 API 연결 상태 확인

## 🚀 실행 방법

```bash
cd apps/mockup_gui/testing

# 의존성 설치
pip install -r requirements.txt

# 개별 테스트 실행
python integration_test.py
python test_api_status.py
python test_app.py
python test_connection.py
```

## 📋 주의사항

- `test_app.py`와 `test_connection.py`는 `http://localhost:5000`에서 실행되는 Flask 앱을 테스트합니다
- `test_api_status.py`는 `http://localhost:8000`에서 실행되는 API를 테스트합니다
- `integration_test.py`는 `http://localhost:8080`에서 실행되는 API를 테스트합니다
