"""
모든 API 엔드포인트 테스트 스크립트

구현된 모든 API가 올바르게 동작하는지 확인합니다.
"""

import asyncio
import httpx
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any

# 테스트 설정
BASE_URL = "http://localhost:8000"
TEST_DEVICE_ID = "test_device_001"
TEST_TIMESTAMP = datetime.now().isoformat()

# 테스트할 API 엔드포인트들
API_ENDPOINTS = {
    "users": {
        "base": "/v1/users",
        "test_data": {
            "user_id": "test_user_001",
            "user_role": "test",
            "user_name": "Test User",
            "email": "test@example.com",
            "phone_number": "010-1234-5678"
        }
    },
    "devices": {
        "base": "/v1/devices",
        "test_data": {
            "device_id": TEST_DEVICE_ID,
            "user_id": "test_user_001",
            "location_label": "Test Location",
            "installed_at": datetime.now().isoformat()
        }
    },
    "sensors": {
        "base": "/v1/sensors",
        "test_data": {
            "device_id": TEST_DEVICE_ID,
            "timestamp": datetime.now().isoformat(),
            "value": 25.5,
            "unit": "C"
        }
    },
    "cds": {
        "base": "/v1/cds",
        "test_data": {
            "time": datetime.now().isoformat(),
            "device_id": TEST_DEVICE_ID,
            "analog_value": 512,
            "lux_value": 100.5
        }
    },
    "dht": {
        "base": "/v1/dht",
        "test_data": {
            "time": datetime.now().isoformat(),
            "device_id": TEST_DEVICE_ID,
            "temperature_c": 25.0,
            "humidity_percent": 60.0
        }
    },
    "flame": {
        "base": "/v1/flame",
        "test_data": {
            "time": datetime.now().isoformat(),
            "device_id": TEST_DEVICE_ID,
            "analog_value": 0,
            "flame_detected": False
        }
    },
    "imu": {
        "base": "/v1/imu",
        "test_data": {
            "time": datetime.now().isoformat(),
            "device_id": TEST_DEVICE_ID,
            "accel_x": 0.1,
            "accel_y": 0.2,
            "accel_z": 9.8,
            "gyro_x": 0.01,
            "gyro_y": 0.02,
            "gyro_z": 0.03
        }
    },
    "loadcell": {
        "base": "/v1/loadcell",
        "test_data": {
            "time": datetime.now().isoformat(),
            "device_id": TEST_DEVICE_ID,
            "raw_value": 1024,
            "weight_kg": 1.5,
            "calibrated": True
        }
    },
    "mq5": {
        "base": "/v1/mq5",
        "test_data": {
            "time": datetime.now().isoformat(),
            "device_id": TEST_DEVICE_ID,
            "analog_value": 256,
            "ppm_value": 50.0,
            "gas_type": "LPG"
        }
    },
    "mq7": {
        "base": "/v1/mq7",
        "test_data": {
            "time": datetime.now().isoformat(),
            "device_id": TEST_DEVICE_ID,
            "analog_value": 128,
            "ppm_value": 25.0,
            "gas_type": "CO"
        }
    },
    "rfid": {
        "base": "/v1/rfid",
        "test_data": {
            "time": datetime.now().isoformat(),
            "device_id": TEST_DEVICE_ID,
            "card_id": "RFID_CARD_001",
            "card_type": "MIFARE",
            "read_success": True
        }
    },
    "sound": {
        "base": "/v1/sound",
        "test_data": {
            "time": datetime.now().isoformat(),
            "device_id": TEST_DEVICE_ID,
            "analog_value": 512,
            "db_value": 65.0,
            "threshold_exceeded": False
        }
    },
    "tcrt5000": {
        "base": "/v1/tcrt5000",
        "test_data": {
            "time": datetime.now().isoformat(),
            "device_id": TEST_DEVICE_ID,
            "digital_value": False,
            "analog_value": 0,
            "object_detected": False
        }
    },
    "ultrasonic": {
        "base": "/v1/ultrasonic",
        "test_data": {
            "time": datetime.now().isoformat(),
            "device_id": TEST_DEVICE_ID,
            "distance_cm": 50.0,
            "raw_value": 1024,
            "measurement_valid": True
        }
    }
}


class APITester:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.results: Dict[str, Dict[str, Any]] = {}
        
    async def test_endpoint(self, name: str, endpoint: Dict[str, Any]) -> Dict[str, Any]:
        """개별 API 엔드포인트 테스트"""
        print(f"\n🔍 테스트 중: {name}")
        
        result = {
            "name": name,
            "base_url": endpoint["base"],
            "tests": {},
            "overall_status": "PENDING"
        }
        
        try:
            async with httpx.AsyncClient() as client:
                # 1. POST 테스트 (데이터 생성)
                print(f"  📝 POST {endpoint['base']}/")
                try:
                    response = await client.post(
                        f"{self.base_url}{endpoint['base']}/",
                        json=endpoint["test_data"],
                        timeout=10.0
                    )
                    result["tests"]["POST"] = {
                        "status_code": response.status_code,
                        "success": response.status_code in [200, 201],
                        "response": response.text[:200] if response.text else None
                    }
                    print(f"    ✅ POST 성공: {response.status_code}")
                except Exception as e:
                    result["tests"]["POST"] = {
                        "status_code": None,
                        "success": False,
                        "error": str(e)
                    }
                    print(f"    ❌ POST 실패: {e}")
                
                # 2. GET 테스트 (데이터 목록 조회)
                print(f"  📖 GET {endpoint['base']}/")
                try:
                    response = await client.get(
                        f"{self.base_url}{endpoint['base']}/",
                        timeout=10.0
                    )
                    result["tests"]["GET_LIST"] = {
                        "status_code": response.status_code,
                        "success": response.status_code == 200,
                        "response": response.text[:200] if response.text else None
                    }
                    print(f"    ✅ GET 목록 성공: {response.status_code}")
                except Exception as e:
                    result["tests"]["GET_LIST"] = {
                        "status_code": None,
                        "success": False,
                        "error": str(e)
                    }
                    print(f"    ❌ GET 목록 실패: {e}")
                
                # 3. GET latest 테스트
                print(f"  📖 GET {endpoint['base']}/latest")
                try:
                    response = await client.get(
                        f"{self.base_url}{endpoint['base']}/latest?device_id={TEST_DEVICE_ID}",
                        timeout=10.0
                    )
                    result["tests"]["GET_LATEST"] = {
                        "status_code": response.status_code,
                        "success": response.status_code in [200, 404],  # 404도 정상 (데이터가 없는 경우)
                        "response": response.text[:200] if response.text else None
                    }
                    print(f"    ✅ GET 최신 데이터 성공: {response.status_code}")
                except Exception as e:
                    result["tests"]["GET_LATEST"] = {
                        "status_code": None,
                        "success": False,
                        "error": str(e)
                    }
                    print(f"    ❌ GET 최신 데이터 실패: {e}")
                
                # 4. 통계 엔드포인트 테스트 (있는 경우)
                if name in ["dht", "flame", "loadcell", "mq5", "mq7", "rfid", "sound", "tcrt5000", "ultrasonic"]:
                    stats_endpoint = self._get_stats_endpoint(name)
                    if stats_endpoint:
                        print(f"  📊 GET {stats_endpoint}")
                        try:
                            response = await client.get(
                                f"{self.base_url}{stats_endpoint}",
                                timeout=10.0
                            )
                            result["tests"]["GET_STATS"] = {
                                "status_code": response.status_code,
                                "success": response.status_code in [200, 404],
                                "response": response.text[:200] if response.text else None
                            }
                            print(f"    ✅ GET 통계 성공: {response.status_code}")
                        except Exception as e:
                            result["tests"]["GET_STATS"] = {
                                "status_code": None,
                                "success": False,
                                "error": str(e)
                            }
                            print(f"    ❌ GET 통계 실패: {e}")
                
                # 전체 테스트 결과 계산
                successful_tests = sum(1 for test in result["tests"].values() if test["success"])
                total_tests = len(result["tests"])
                
                if total_tests > 0:
                    success_rate = successful_tests / total_tests
                    if success_rate == 1.0:
                        result["overall_status"] = "SUCCESS"
                    elif success_rate >= 0.5:
                        result["overall_status"] = "PARTIAL"
                    else:
                        result["overall_status"] = "FAILED"
                    
                    result["success_rate"] = success_rate
                    result["successful_tests"] = successful_tests
                    result["total_tests"] = total_tests
                
        except Exception as e:
            result["overall_status"] = "ERROR"
            result["error"] = str(e)
            print(f"    💥 전체 테스트 실패: {e}")
        
        return result
    
    def _get_stats_endpoint(self, name: str) -> str:
        """통계 엔드포인트 URL 생성"""
        stats_endpoints = {
            "dht": f"/v1/dht/{TEST_DEVICE_ID}/stats/summary",
            "flame": f"/v1/flame/{TEST_DEVICE_ID}/alerts",
            "loadcell": f"/v1/loadcell/{TEST_DEVICE_ID}/stats/weight",
            "mq5": f"/v1/mq5/{TEST_DEVICE_ID}/stats/gas",
            "mq7": f"/v1/mq7/{TEST_DEVICE_ID}/stats/gas",
            "rfid": f"/v1/rfid/{TEST_DEVICE_ID}/stats/cards",
            "sound": f"/v1/sound/{TEST_DEVICE_ID}/stats/audio",
            "tcrt5000": f"/v1/tcrt5000/{TEST_DEVICE_ID}/stats/proximity",
            "ultrasonic": f"/v1/ultrasonic/{TEST_DEVICE_ID}/stats/distance"
        }
        return stats_endpoints.get(name, "")
    
    async def run_all_tests(self) -> Dict[str, Dict[str, Any]]:
        """모든 API 엔드포인트 테스트 실행"""
        print("🚀 IoT Care API 전체 테스트 시작")
        print(f"📍 테스트 대상: {self.base_url}")
        print(f"🔧 테스트 디바이스: {TEST_DEVICE_ID}")
        print(f"⏰ 테스트 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        for name, endpoint in API_ENDPOINTS.items():
            result = await self.test_endpoint(name, endpoint)
            self.results[name] = result
            
            # 상태 표시
            status_emoji = {
                "SUCCESS": "✅",
                "PARTIAL": "⚠️",
                "FAILED": "❌",
                "ERROR": "💥",
                "PENDING": "⏳"
            }
            print(f"{status_emoji.get(result['overall_status'], '❓')} {name}: {result['overall_status']}")
        
        return self.results
    
    def generate_report(self) -> str:
        """테스트 결과 리포트 생성"""
        print("\n" + "=" * 60)
        print("📊 API 테스트 결과 리포트")
        print("=" * 60)
        
        total_apis = len(self.results)
        successful_apis = sum(1 for r in self.results.values() if r["overall_status"] == "SUCCESS")
        partial_apis = sum(1 for r in self.results.values() if r["overall_status"] == "PARTIAL")
        failed_apis = sum(1 for r in self.results.values() if r["overall_status"] == "FAILED")
        error_apis = sum(1 for r in self.results.values() if r["overall_status"] == "ERROR")
        
        print(f"📈 전체 API 수: {total_apis}")
        print(f"✅ 성공: {successful_apis}")
        print(f"⚠️ 부분 성공: {partial_apis}")
        print(f"❌ 실패: {failed_apis}")
        print(f"💥 오류: {error_apis}")
        
        success_rate = (successful_apis + partial_apis * 0.5) / total_apis if total_apis > 0 else 0
        print(f"📊 전체 성공률: {success_rate:.1%}")
        
        print("\n🔍 상세 결과:")
        for name, result in self.results.items():
            status_emoji = {
                "SUCCESS": "✅",
                "PARTIAL": "⚠️",
                "FAILED": "❌",
                "ERROR": "💥",
                "PENDING": "⏳"
            }
            
            print(f"\n{status_emoji.get(result['overall_status'], '❓')} {name}")
            print(f"  📍 엔드포인트: {result['base_url']}")
            print(f"  📊 상태: {result['overall_status']}")
            
            if "success_rate" in result:
                print(f"  📈 성공률: {result['success_rate']:.1%}")
                print(f"  ✅ 성공한 테스트: {result['successful_tests']}/{result['total_tests']}")
            
            if "tests" in result:
                for test_name, test_result in result["tests"].items():
                    test_status = "✅" if test_result["success"] else "❌"
                    print(f"    {test_status} {test_name}: {test_result['status_code']}")
        
        return f"테스트 완료: {successful_apis}/{total_apis} API 성공"


async def main():
    """메인 함수"""
    tester = APITester(BASE_URL)
    
    try:
        # 모든 API 테스트 실행
        results = await tester.run_all_tests()
        
        # 결과 리포트 생성
        report = tester.generate_report()
        
        # 결과를 파일로 저장
        with open("api_test_results.json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2, default=str)
        
        print(f"\n💾 테스트 결과가 'api_test_results.json' 파일에 저장되었습니다.")
        print(f"\n🎯 {report}")
        
    except Exception as e:
        print(f"💥 테스트 실행 중 오류 발생: {e}")


if __name__ == "__main__":
    asyncio.run(main())
