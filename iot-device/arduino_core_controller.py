#!/usr/bin/env python3

import asyncio
import httpx
import json
import time
from typing import Dict, List, Any
from datetime import datetime, timedelta
import uuid
import os
from dotenv import load_dotenv
import serial
import struct

class Iot_api:
    def __init__(self, base_url: str = "http://ec2-43-201-96-23.ap-northeast-2.compute.amazonaws.com"):

        user = uuid.uuid4()
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=120.0)
               
        # 환경 변수 로드
        load_dotenv('.env.local')

        self.api_endpoints = {
            "Users": "/api/users",
            "CDS": "/api/cds",
            "LoadCell": "/api/loadcell",
            "MQ5": "/api/mq5",
            "MQ7": "/api/mq7",
            "RFID": "/api/rfid",
            "Sound": "/api/sound",
            "TCRT5000": "/api/tcrt5000",
            "Ultrasonic": "/api/ultrasonic",
            "EdgeFlame": "/api/edge-flame",
            "EdgePIR": "/api/edge-pir",
            "EdgeReed": "/api/edge-reed",
            "EdgeTilt": "/api/edge-tilt",
            "ActuatorBuzzer": "/api/actuator-buzzer",
            "ActuatorIRTX": "/api/actuator-irtx",
            "ActuatorRelay": "/api/actuator-relay",
            "ActuatorServo": "/api/actuator-servo",
        }
        
    async def __aenter__(self):
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
        
        pass
        
    async def test_health_check(self) -> bool:
        """Health check 테스트"""
        try:
            print(f"🔍 Health check 시도: {self.base_url}/health")
            response = await self.client.get(f"{self.base_url}/health")
            print(f"📡 Response status: {response.status_code}")
            print(f"📡 Response body: {response.text}")
            
            if response.status_code == 200:
                print("✅ Health check 성공")
                return True
            else:
                print(f"❌ Health check 실패: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Health check 오류: {e}")
            import traceback
            traceback.print_exc()
            return False

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


    async def create_data(self, endpoint: str, data: Dict[str, Any]) -> str:
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
        

class Iot_Serial(Iot_api):
    def __init__(self):
        super().__init__()
        self.test_health_check()
        self.port = '/dev/ttyACM0'
        self.baud = 57600
        self.source = {"Load_cell" : 0x00,
                    "MQ5" : 0x01,
                    "MQ7": 0x02,
                    "RFID_Out" : 0x03,
                    "RFID_In" : 0x13,
                    "IRTX" : 0x04,
                    "Buzzer" : 0x05,
                    "LM35" : 0x06,
                    "Sound" : 0x07,
                    "PIR" : 0x08,
                    "IMU" : 0x09,
                    "LED" : 0x0A
                    }

        self.conn = serial.Serial(port= self.port, baudrate=self.baud, timeout=1)

        self.endpoint = ""
        self.trans_data = ""
    def get_data(self):
        if self.conn.readable():
            res = self.conn.read_until(b'\r\n')
            if (len(res) < 10):
                return
            else:
                pass
                # print(res)
            if not self.SOFcheck(res):
                print("Error in SOF")
                return
            if not self.EOFcheck(res):
                print("Error in EOF")
                return
            if not self.DESINATIONcheck(res):
                print("Not for controller")
                return
            
            self.SOURCEcheck(res)
            



    def SOFcheck(self, data):
        if (data[0] == 0x04):
            return True
        else:
            return False
    
    def EOFcheck(self, data):
        if (data[-3] == 0xFA):
            return True
        else:
            return False
        
    def DESINATIONcheck(self, data):
        if (data[2] == 0xFD):
            return True
        else:
            return False
        
    def SOURCEcheck(self, data):
        if (data[1] == self.source["Load_cell"]):
            self.endpoint = self.api_endpoints["LoadCell"]
            self.trans_data = {
                "time": datetime.now().isoformat(),
                "device_id": "10fa45f2-f375-41c9-a62a-093efcd01bd3_Load_Cell_1",
                "raw_payload": {"weight_kg": float(struct.unpack("f", data[3:7])[0]), "calibration_factor": 0.0, "temperature": 0.0}
            }
        elif (data[1] == self.source["MQ5"]):
            self.endpoint = self.api_endpoints["MQ5"]
            self.trans_data = {
                "time": datetime.now().isoformat(),
                "device_id": "10fa45f2-f375-41c9-a62a-093efcd01bd3_MQ5_Gas_Sensor_1",
                "raw_payload": {"gas_level": float(struct.unpack("f", data[3:7])[0]), "temperature": 0.0}
            }   
        elif (data[1] == self.source["MQ7"]):
            self.endpoint = self.api_endpoints["MQ7"]
            self.trans_data = {
                "time": datetime.now().isoformat(),
                "device_id": "10fa45f2-f375-41c9-a62a-093efcd01bd3_MQ7_CO_Sensor_1",
                "raw_payload": {"co_level": struct.unpack("f", data[3:7][0]), "temperature": 0.0}
            }
        elif (data[1] == self.source["RFID_Out"]):
            self.endpoint = self.api_endpoints["RFID"]
            self.trans_data = {
                "time": datetime.now().isoformat(),
                "device_id": "3",
                "raw_payload": {"card_id": struct.unpack("i", data[3:8]), "reader_location": "main_entrance_out"}
            }
        elif (data[1] == self.source["RFID_IN"]):
            self.endpoint = self.api_endpoints["RFID"]
            self.trans_data = {
                "time": datetime.now().isoformat(),
                "device_id": "4",
                "raw_payload": {"card_id": struct.unpack("i", data[3:8]), "reader_location": "main_entrance_in"}
            }

        elif (data[1] == self.source["IRTX"]):
            self.endpoint = self.api_endpoints["ActuatorIRTX"]
            self.trans_data = {
                "time": datetime.now().isoformat(),
                "device_id": "4",
                "raw_payload": {"protocol": "NEC", "command_hex": struct.unpack("C",data[3:5])}
            }
        # elif (data[1] == self.source["Buzzer"]):
        # elif (data[1] == self.source["LM35"]):
        # elif (data[1] == self.source["Sound"]):
        # elif (data[1] == self.source["PIR"]):
        # elif (data[1] == self.source["IMU"]):
        # elif (data[1] == self.source["LED"]):
        else:
            print("Invalid Source")
            return

        self.source = {"Load_cell" : 0x00,
                    "MQ5" : 0x01,
                    "MQ7": 0x02,
                    "RFID_Out" : 0x03,
                    "RFID_In" : 0x13,
                    "IRTX" : 0x04,
                    "Buzzer" : 0x05,
                    "LM35" : 0x06,
                    "Sound" : 0x07,
                    "PIR" : 0x08,
                    "IMU" : 0x09,
                    "LED" : 0x0A
                    }

async def main():
    """메인 함수"""
    async with Iot_Serial() as tester:
        success = await tester.test_health_check()
        if not success:
            print("\n 서버와의 통신 상태가 불량합니다.")
            return
        while (True):
            tester.get_data()
            print(tester.trans_data)
            await tester.create_data(tester.endpoint, tester.trans_data)

if __name__ == "__main__":
    asyncio.run(main())