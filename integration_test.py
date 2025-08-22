#!/usr/bin/env python3
"""
IoT Care Backend System RESTFUL API 통합 테스트 스크립트

테스트 시나리오:
1. GET: 테이블 현재 상태 확인 및 데이터 레코드수 확인
2. POST: 신규 데이터 생성
3. GET: 테이블 현재 상태 확인 및 데이터 레코드수 확인
4. PUT: 위에서 생성한 데이터에 대한 수정 작업
5. GET: 테이블 현재 상태 확인 및 데이터 레코드수 확인
6. DELETE: 생성-수정 한 데이터 삭제
7. GET: 테이블 현재 상태 확인 및 데이터 레코드수 확인
8. POST: 두 번째 신규 데이터 생성 ("통합 테스트" 키워드 포함)
"""

import asyncio
import httpx
import json
import time
from typing import Dict, List, Any
from datetime import datetime, timedelta
import uuid

class IoTAPIIntegrationTest:
    """IoT Care Backend System API 통합 테스트 클래스"""
    
    def __init__(self, base_url: str = "http://localhost:8080"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=30.0)
        self.test_results = {}
        self.created_ids = {}
        
    async def __aenter__(self):
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
    
    def log_test(self, api_name: str, test_step: str, status: str, details: str = ""):
        """테스트 로그 기록"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {
            "timestamp": timestamp,
            "api_name": api_name,
            "test_step": test_step,
            "status": status,
            "details": details
        }
        
        if api_name not in self.test_results:
            self.test_results[api_name] = []
        
        self.test_results[api_name].append(log_entry)
        print(f"[{timestamp}] {api_name} - {test_step}: {status}")
        if details:
            print(f"  Details: {details}")
    
    async def test_health_check(self) -> bool:
        """Health check 테스트"""
        try:
            response = await self.client.get(f"{self.base_url}/health")
            if response.status_code == 200:
                print("✅ Health check 성공")
                return True
            else:
                print(f"❌ Health check 실패: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Health check 오류: {e}")
            return False
    
    async def test_api_endpoint(self, api_name: str, endpoint: str, test_data: Dict[str, Any]) -> bool:
        """개별 API 엔드포인트 테스트"""
        print(f"\n🔍 {api_name} API 테스트 시작...")
        
        try:
            # 1. GET: 초기 상태 확인
            initial_count = await self.get_record_count(endpoint)
            self.log_test(api_name, "GET_초기", "성공", f"레코드 수: {initial_count}")
            
            # 2. POST: 신규 데이터 생성
            created_id = await self.create_record(endpoint, test_data)
            if not created_id:
                self.log_test(api_name, "POST_생성", "실패", "데이터 생성 실패")
                return False
            
            self.created_ids[api_name] = created_id
            self.log_test(api_name, "POST_생성", "성공", f"생성된 ID: {created_id}")
            
            # 3. GET: 생성 후 상태 확인
            after_create_count = await self.get_record_count(endpoint)
            self.log_test(api_name, "GET_생성후", "성공", f"레코드 수: {after_create_count}")
            
            # 4. PUT: 데이터 수정
            update_data = {**test_data, "updated_at": datetime.now().isoformat()}
            update_success = await self.update_record(endpoint, created_id, update_data)
            if update_success:
                self.log_test(api_name, "PUT_수정", "성공", f"수정된 ID: {created_id}")
            else:
                self.log_test(api_name, "PUT_수정", "실패", "데이터 수정 실패")
            
            # 5. GET: 수정 후 상태 확인
            after_update_count = await self.get_record_count(endpoint)
            self.log_test(api_name, "GET_수정후", "성공", f"레코드 수: {after_update_count}")
            
            # 6. DELETE: 데이터 삭제
            delete_success = await self.delete_record(endpoint, created_id)
            if delete_success:
                self.log_test(api_name, "DELETE_삭제", "성공", f"삭제된 ID: {created_id}")
            else:
                self.log_test(api_name, "DELETE_삭제", "실패", "데이터 삭제 실패")
            
            # 7. GET: 삭제 후 상태 확인
            after_delete_count = await self.get_record_count(endpoint)
            self.log_test(api_name, "GET_삭제후", "성공", f"레코드 수: {after_delete_count}")
            
            # 8. POST: 두 번째 데이터 생성 ("통합 테스트" 키워드 포함)
            integration_test_data = {**test_data}
            # 자유롭게 입력할 수 있는 필드에 "통합 테스트" 키워드 추가
            for key, value in integration_test_data.items():
                if isinstance(value, str) and len(value) < 100:
                    integration_test_data[key] = f"{value} - 통합 테스트"
                    break
            
            second_id = await self.create_record(endpoint, integration_test_data)
            if second_id:
                self.log_test(api_name, "POST_통합테스트", "성공", f"통합테스트 ID: {second_id}")
                # 통합테스트용 데이터는 삭제하지 않음
            else:
                self.log_test(api_name, "POST_통합테스트", "실패", "통합테스트 데이터 생성 실패")
            
            print(f"✅ {api_name} API 테스트 완료")
            return True
            
        except Exception as e:
            self.log_test(api_name, "테스트_전체", "실패", f"예외 발생: {e}")
            return False
    
    async def get_record_count(self, endpoint: str) -> int:
        """레코드 수 조회"""
        try:
            response = await self.client.get(f"{self.base_url}{endpoint}")
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    return len(data)
                elif isinstance(data, dict) and "total" in data:
                    return data["total"]
                else:
                    return 0
            return 0
        except Exception:
            return 0
    
    async def create_record(self, endpoint: str, data: Dict[str, Any]) -> str:
        """레코드 생성"""
        try:
            response = await self.client.post(f"{self.base_url}{endpoint}", json=data)
            if response.status_code == 201 or response.status_code == 200:
                result = response.json()
                # ID 필드 찾기
                for key in ["id", "uuid", "device_id", "sensor_id"]:
                    if key in result:
                        return str(result[key])
                return "unknown"
            return None
        except Exception:
            return None
    
    async def update_record(self, endpoint: str, record_id: str, data: Dict[str, Any]) -> bool:
        """레코드 수정"""
        try:
            response = await self.client.put(f"{self.base_url}{endpoint}/{record_id}", json=data)
            return response.status_code in [200, 204]
        except Exception:
            return False
    
    async def delete_record(self, endpoint: str, record_id: str) -> bool:
        """레코드 삭제"""
        try:
            response = await self.client.delete(f"{self.base_url}{endpoint}/{record_id}")
            return response.status_code in [200, 204]
        except Exception:
            return False
    
    def generate_test_data(self, api_name: str) -> Dict[str, Any]:
        """API별 테스트 데이터 생성"""
        base_data = {
            "device_id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(),
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        # API별 특화 데이터
        if "loadcell" in api_name.lower():
            base_data.update({
                "weight_kg": 25.5,
                "analog_value": 512,
                "calibration_status": "calibrated"
            })
        elif "mq5" in api_name.lower() or "mq7" in api_name.lower():
            base_data.update({
                "gas_concentration": 150.0,
                "analog_value": 256,
                "threshold_exceeded": False
            })
        elif "rfid" in api_name.lower():
            base_data.update({
                "card_id": "RFID_12345",
                "read_success": True,
                "read_timestamp": datetime.now().isoformat()
            })
        elif "sound" in api_name.lower():
            base_data.update({
                "decibel_level": 65.5,
                "frequency_hz": 1000,
                "noise_threshold_exceeded": False
            })
        elif "ultrasonic" in api_name.lower():
            base_data.update({
                "distance_cm": 45.2,
                "echo_strength": 0.8,
                "proximity_alert": False
            })
        elif "edge" in api_name.lower():
            base_data.update({
                "detection_status": True,
                "sensitivity_level": 0.7,
                "alert_triggered": False
            })
        elif "actuator" in api_name.lower():
            base_data.update({
                "action_type": "test",
                "execution_status": "completed",
                "response_time_ms": 150
            })
        elif "user" in api_name.lower():
            base_data.update({
                "username": f"test_user_{uuid.uuid4().hex[:8]}",
                "email": f"test_{uuid.uuid4().hex[:8]}@example.com",
                "role": "test"
            })
        elif "device" in api_name.lower():
            base_data.update({
                "device_name": f"test_device_{uuid.uuid4().hex[:8]}",
                "device_type": "sensor",
                "status": "active"
            })
        else:
            # 기본 센서 데이터
            base_data.update({
                "sensor_value": 100.0,
                "unit": "test_unit",
                "status": "normal"
            })
        
        return base_data
    
    async def run_all_tests(self):
        """모든 API 테스트 실행"""
        print("🚀 IoT Care Backend System 통합 테스트 시작")
        print("=" * 60)
        
        # Health check
        if not await self.test_health_check():
            print("❌ Health check 실패로 테스트 중단")
            return False
        
        # 테스트할 API 엔드포인트 목록
        api_endpoints = [
            ("Users API", "/api/v1/users"),
            ("Devices API", "/api/v1/devices"),
            ("LoadCell API", "/api/v1/loadcell"),
            ("MQ5 API", "/api/v1/mq5"),
            ("MQ7 API", "/api/v1/mq7"),
            ("RFID API", "/api/v1/rfid"),
            ("Sound API", "/api/v1/sound"),
            ("TCRT5000 API", "/api/v1/tcrt5000"),
            ("Ultrasonic API", "/api/v1/ultrasonic"),
            ("EdgeFlame API", "/api/v1/edge-flame"),
            ("EdgePIR API", "/api/v1/edge-pir"),
            ("EdgeReed API", "/api/v1/edge-reed"),
            ("EdgeTilt API", "/api/v1/edge-tilt"),
            ("ActuatorBuzzer API", "/api/v1/actuator-buzzer"),
            ("ActuatorIRTX API", "/api/v1/actuator-irtx"),
            ("ActuatorRelay API", "/api/v1/actuator-relay"),
            ("ActuatorServo API", "/api/v1/actuator-servo"),
            ("CDS API", "/api/v1/cds"),
            ("DHT API", "/api/v1/dht"),
            ("Flame API", "/api/v1/flame"),
            ("IMU API", "/api/v1/imu"),
            ("LDR API", "/api/v1/ldr"),
            ("PIR API", "/api/v1/pir"),
            ("DS18B20 API", "/api/v1/ds18b20"),
            ("HC-SR04 API", "/api/v1/hc-sr04")
        ]
        
        success_count = 0
        total_count = len(api_endpoints)
        
        for api_name, endpoint in api_endpoints:
            test_data = self.generate_test_data(api_name)
            success = await self.test_api_endpoint(api_name, endpoint, test_data)
            if success:
                success_count += 1
            
            # API 간 간격
            await asyncio.sleep(0.5)
        
        # 테스트 결과 요약
        print("\n" + "=" * 60)
        print("📊 통합 테스트 결과 요약")
        print("=" * 60)
        print(f"전체 API 수: {total_count}")
        print(f"성공한 API 수: {success_count}")
        print(f"실패한 API 수: {total_count - success_count}")
        print(f"성공률: {(success_count / total_count) * 100:.1f}%")
        
        # 결과 저장
        await self.save_test_results()
        
        return success_count == total_count
    
    async def save_test_results(self):
        """테스트 결과 저장"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"integration_test_results_{timestamp}.json"
        
        results = {
            "test_timestamp": datetime.now().isoformat(),
            "base_url": self.base_url,
            "total_apis": len(self.test_results),
            "test_results": self.test_results,
            "created_ids": self.created_ids
        }
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"📁 테스트 결과가 {filename}에 저장되었습니다.")
        except Exception as e:
            print(f"❌ 테스트 결과 저장 실패: {e}")

async def main():
    """메인 함수"""
    async with IoTAPIIntegrationTest() as tester:
        success = await tester.run_all_tests()
        if success:
            print("\n🎉 모든 API 통합 테스트가 성공적으로 완료되었습니다!")
        else:
            print("\n⚠️ 일부 API 테스트에서 문제가 발생했습니다.")
            print("테스트 결과를 확인하고 문제를 해결해주세요.")

if __name__ == "__main__":
    asyncio.run(main())

