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
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=30.0)
        self.test_results = {}
        self.created_ids = {}
        self.failed_tests = []
        
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
            
        if status == "실패":
            self.failed_tests.append(f"{api_name} - {test_step}: {details}")
    
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
            
            # 4. PUT: 데이터 수정 (선택적)
            if created_id != "unknown":
                # API별로 다른 업데이트 데이터 생성
                if "user" in api_name.lower():
                    # Users API: 기존 데이터에서 일부 필드만 수정
                    update_data = {
                        "user_name": f"updated_{test_data['user_name']}",
                        "email": f"updated_{test_data['email']}"
                    }
                else:
                    # 다른 API: 기존 데이터에 updated_at 추가
                    update_data = {**test_data, "updated_at": datetime.now().isoformat()}
                
                update_success = await self.update_record(endpoint, created_id, update_data)
                if update_success:
                    self.log_test(api_name, "PUT_수정", "성공", f"수정된 ID: {created_id}")
                else:
                    self.log_test(api_name, "PUT_수정", "실패", "데이터 수정 실패 (엔드포인트 미지원 가능성)")
            else:
                self.log_test(api_name, "PUT_수정", "건너뜀", "ID를 알 수 없어 수정 테스트 건너뜀")
            
            # 5. GET: 수정 후 상태 확인
            after_update_count = await self.get_record_count(endpoint)
            self.log_test(api_name, "GET_수정후", "성공", f"레코드 수: {after_update_count}")
            
            # 6. DELETE: 데이터 삭제 (선택적)
            if created_id != "unknown":
                delete_success = await self.delete_record(endpoint, created_id)
                if delete_success:
                    self.log_test(api_name, "DELETE_삭제", "성공", f"삭제된 ID: {created_id}")
                else:
                    self.log_test(api_name, "DELETE_삭제", "실패", "데이터 삭제 실패 (엔드포인트 미지원 가능성)")
            else:
                self.log_test(api_name, "DELETE_삭제", "건너뜀", "ID를 알 수 없어 삭제 테스트 건너뜀")
            
            # 7. GET: 삭제 후 상태 확인
            after_delete_count = await self.get_record_count(endpoint)
            self.log_test(api_name, "GET_삭제후", "성공", f"레코드 수: {after_delete_count}")
            
            # 8. POST: 두 번째 데이터 생성 ("통합 테스트" 키워드 포함)
            integration_test_data = {**test_data}
            # 자유롭게 입력할 수 있는 필드에 "통합 테스트" 키워드 추가
            for key, value in integration_test_data.items():
                if isinstance(value, str) and len(value) < 100 and key not in ['device_id', 'timestamp', 'created_at', 'updated_at']:
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
                elif isinstance(data, dict) and "items" in data:
                    return len(data["items"])
                else:
                    return 1  # 단일 객체일 경우
            return 0
        except Exception as e:
            print(f"  GET 오류: {e}")
            return 0
    
    async def create_record(self, endpoint: str, data: Dict[str, Any]) -> str:
        """레코드 생성"""
        try:
            response = await self.client.post(f"{self.base_url}{endpoint}/create", json=data)
            if response.status_code in [201, 200]:
                result = response.json()
                
                # CDS API의 경우 device_id와 timestamp를 조합하여 ID 생성
                if "cds" in endpoint.lower():
                    device_id = result.get("device_id", "")
                    time_str = result.get("time", "")
                    if device_id and time_str:
                        # timestamp를 간단한 형태로 변환 (파일명으로 사용할 수 있도록)
                        try:
                            time_obj = datetime.fromisoformat(time_str.replace('Z', '+00:00'))
                            timestamp = time_obj.strftime("%Y%m%d_%H%M%S")
                            return f"{device_id}_{timestamp}"
                        except:
                            return f"{device_id}_{time_str}"
                
                # 다른 API의 경우 기존 로직 사용
                for key in ["id", "uuid", "device_id", "sensor_id", "user_id"]:
                    if key in result:
                        return str(result[key])
                return "unknown"
            else:
                print(f"  POST 실패: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"  POST 오류: {e}")
            return None
    
    async def update_record(self, endpoint: str, record_id: str, data: Dict[str, Any]) -> bool:
        """레코드 수정"""
        try:
            # API별로 다른 엔드포인트 패턴 사용
            if "cds" in endpoint.lower():
                # CDS API: /{device_id}/{timestamp} 패턴
                device_id = data.get("device_id", record_id)
                timestamp = data.get("time", datetime.now().isoformat())
                response = await self.client.put(f"{self.base_url}{endpoint}/{device_id}/{timestamp}", json=data)
            else:
                # 일반적인 API: /{id} 패턴
                response = await self.client.put(f"{self.base_url}{endpoint}/{record_id}", json=data)
            
            return response.status_code in [200, 204]
        except Exception as e:
            print(f"  PUT 오류: {e}")
            return False
    
    async def delete_record(self, endpoint: str, record_id: str) -> bool:
        """레코드 삭제"""
        try:
            # API별로 다른 엔드포인트 패턴 사용
            if "cds" in endpoint.lower():
                # CDS API: /{device_id}/{timestamp} 패턴
                # record_id에서 device_id와 timestamp 추출
                if "_" in record_id:
                    device_id = record_id.split("_")[0]
                    timestamp = record_id.split("_")[1]
                else:
                    device_id = record_id
                    timestamp = datetime.now().isoformat()
                
                # CDS API의 DELETE 엔드포인트는 /{device_id}/{timestamp} 형태
                response = await self.client.delete(f"{self.base_url}{endpoint}/{device_id}/{timestamp}")
            else:
                # 일반적인 API: /{id} 패턴
                response = await self.client.delete(f"{self.base_url}{endpoint}/{record_id}")
            
            return response.status_code in [200, 204]
        except Exception as e:
            print(f"  DELETE 오류: {e}")
            return False
    
    def generate_test_data(self, api_name: str) -> Dict[str, Any]:
        """API별 테스트 데이터 생성"""
        current_time = datetime.now()
        
        # API별 특화 데이터
        if "user" in api_name.lower():
            unique_id = uuid.uuid4().hex[:8]
            return {
                "user_name": f"test_user_{unique_id}",
                "email": f"test_{unique_id}@example.com",
                "phone_number": "01012345678",
                "user_role": "user"
            }
        elif "cds" in api_name.lower():
            return {
                "time": current_time.isoformat(),
                "device_id": str(uuid.uuid4()),
                "analog_value": 512,
                "lux_value": 100.5,
                "raw_payload": {"test": "data"}
            }
        elif "dht" in api_name.lower():
            return {
                "time": current_time.isoformat(),
                "device_id": str(uuid.uuid4()),
                "temperature": 25.5,
                "humidity": 60.0,
                "heat_index": 26.2,
                "raw_payload": {"test": "data"}
            }
        elif "flame" in api_name.lower():
            return {
                "time": current_time.isoformat(),
                "device_id": str(uuid.uuid4()),
                "analog_value": 256,
                "flame_detected": False,
                "raw_payload": {"test": "data"}
            }
        elif "imu" in api_name.lower():
            return {
                "time": current_time.isoformat(),
                "device_id": str(uuid.uuid4()),
                "accel_x": 0.1,
                "accel_y": 0.2,
                "accel_z": 9.8,
                "gyro_x": 0.01,
                "gyro_y": 0.02,
                "gyro_z": 0.03,
                "mag_x": 0.1,
                "mag_y": 0.2,
                "mag_z": 0.3,
                "temp": 25.0,
                "raw_payload": {"test": "data"}
            }
        elif "loadcell" in api_name.lower():
            return {
                "time": current_time.isoformat(),
                "device_id": str(uuid.uuid4()),
                "weight_kg": 25.5,
                "calibrated": True,
                "raw_payload": {"test": "data"}
            }
        elif "mq5" in api_name.lower():
            return {
                "time": current_time.isoformat(),
                "device_id": str(uuid.uuid4()),
                "ppm_value": 150.0,
                "gas_type": "LPG",
                "raw_payload": {"test": "data"}
            }
        elif "mq7" in api_name.lower():
            return {
                "time": current_time.isoformat(),
                "device_id": str(uuid.uuid4()),
                "ppm_value": 200.0,
                "gas_type": "CO",
                "raw_payload": {"test": "data"}
            }
        elif "rfid" in api_name.lower():
            return {
                "time": current_time.isoformat(),
                "device_id": str(uuid.uuid4()),
                "card_type": "Mifare",
                "read_success": True,
                "raw_payload": {"test": "data"}
            }
        elif "sound" in api_name.lower():
            return {
                "time": current_time.isoformat(),
                "device_id": str(uuid.uuid4()),
                "db_value": 65.5,
                "threshold_exceeded": False,
                "raw_payload": {"test": "data"}
            }
        elif "tcrt5000" in api_name.lower():
            return {
                "time": current_time.isoformat(),
                "device_id": str(uuid.uuid4()),
                "object_detected": True,
                "raw_payload": {"test": "data"}
            }
        elif "ultrasonic" in api_name.lower():
            return {
                "time": current_time.isoformat(),
                "device_id": str(uuid.uuid4()),
                "distance_cm": 45.2,
                "measurement_valid": True,
                "raw_payload": {"test": "data"}
            }
        elif "edge_flame" in api_name.lower():
            return {
                "time": current_time.isoformat(),
                "device_id": str(uuid.uuid4()),
                "flame_detected": False,
                "confidence": 0.95,
                "alert_level": "low",
                "raw_payload": {"test": "data"}
            }
        elif "edge_pir" in api_name.lower():
            return {
                "time": current_time.isoformat(),
                "device_id": str(uuid.uuid4()),
                "motion_detected": False,
                "confidence": 0.9,
                "motion_direction": "north",
                "motion_speed": 0.5,
                "processing_time": 0.1,
                "raw_payload": {"test": "data"}
            }
        elif "edge_reed" in api_name.lower():
            return {
                "time": current_time.isoformat(),
                "device_id": str(uuid.uuid4()),
                "switch_state": False,
                "confidence": 0.9,
                "magnetic_field_detected": True,
                "magnetic_strength": 0.8,
                "processing_time": 0.1,
                "raw_payload": {"test": "data"}
            }
        elif "edge_tilt" in api_name.lower():
            return {
                "time": current_time.isoformat(),
                "device_id": str(uuid.uuid4()),
                "tilt_detected": False,
                "tilt_angle": 0.5,
                "tilt_direction": "north",
                "processing_time": 0.1,
                "raw_payload": {"test": "data"}
            }
        elif "actuator_buzzer" in api_name.lower():
            return {
                "time": current_time.isoformat(),
                "device_id": str(uuid.uuid4()),
                "buzzer_type": "piezo",
                "state": "on",
                "freq_hz": 1000,
                "duration_ms": 500,
                "raw_payload": {"test": "data"}
            }
        elif "actuator_irtx" in api_name.lower():
            return {
                "time": current_time.isoformat(),
                "device_id": str(uuid.uuid4()),
                "protocol": "NEC",
                "command_hex": "FF00",
                "raw_payload": {"test": "data"}
            }
        elif "actuator_relay" in api_name.lower():
            return {
                "time": current_time.isoformat(),
                "device_id": str(uuid.uuid4()),
                "channel": 1,
                "state": "on",
                "raw_payload": {"test": "data"}
            }
        elif "actuator_servo" in api_name.lower():
            return {
                "time": current_time.isoformat(),
                "device_id": str(uuid.uuid4()),
                "channel": 1,
                "angle_deg": 90.0,
                "raw_payload": {"test": "data"}
            }
        else:
            # 기본 센서 데이터
            return {
                "time": current_time,
                "device_id": str(uuid.uuid4()),
                "sensor_value": 100.0,
                "unit": "test_unit",
                "status": "normal",
                "raw_payload": {"test": "data"}
            }
    
    async def run_all_tests(self):
        """모든 API 테스트 실행"""
        print("🚀 IoT Care Backend System 통합 테스트 시작")
        print("=" * 60)
        
        # Health check
        if not await self.test_health_check():
            print("❌ Health check 실패로 테스트 중단")
            return False
        
        # 테스트할 API 엔드포인트 목록 (ORM 기준 prefix가 설정된 경로)
        api_endpoints = [
            ("Users API", "/api/users"),
            ("CDS API", "/api/cds"),
            ("LoadCell API", "/api/loadcell"),
            ("MQ5 API", "/api/mq5"),
            ("MQ7 API", "/api/mq7"),
            ("RFID API", "/api/rfid"),
            ("Sound API", "/api/sound"),
            ("TCRT5000 API", "/api/tcrt5000"),
            ("Ultrasonic API", "/api/ultrasonic"),
            ("EdgeFlame API", "/api/edge-flame"),
            ("EdgePIR API", "/api/edge-pir"),
            ("EdgeReed API", "/api/edge-reed"),
            ("EdgeTilt API", "/api/edge-tilt"),
            ("ActuatorBuzzer API", "/api/actuator-buzzer"),
            ("ActuatorIRTX API", "/api/actuator-irtx"),
            ("ActuatorRelay API", "/api/actuator-relay"),
            ("ActuatorServo API", "/api/actuator-servo"),
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
        
        # 실패한 테스트 출력
        if self.failed_tests:
            print("\n❌ 실패한 테스트:")
            for failed_test in self.failed_tests:
                print(f"  - {failed_test}")
        
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
            "created_ids": self.created_ids,
            "failed_tests": self.failed_tests
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
            print("\n📋 다음 단계: 수동 사용자 테스트를 진행해주세요.")
        else:
            print("\n⚠️ 일부 API 테스트에서 문제가 발생했습니다.")
            print("테스트 결과를 확인하고 문제를 해결해주세요.")

if __name__ == "__main__":
    asyncio.run(main())
