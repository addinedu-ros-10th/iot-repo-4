"""
API 라우터 등록

모든 API 라우터를 메인 애플리케이션에 등록합니다.
"""

from fastapi import APIRouter

from app.api.v1 import users, devices, cds, dht, flame, imu, loadcell, mq5, mq7, rfid, sound, tcrt5000, ultrasonic
from app.api.v1 import edge_flame, edge_pir, edge_reed, edge_tilt
from app.api.v1 import actuator_buzzer, actuator_irtx, actuator_relay, actuator_servo
from app.api.v1 import device_rtc

# 메인 API 라우터
api_router = APIRouter()

# v1 API 라우터 등록
api_router.include_router(users.router, prefix="/v1", tags=["users"])
api_router.include_router(devices.router, prefix="/v1", tags=["devices"])

# Raw 센서 데이터 API 라우터 등록
api_router.include_router(cds.router, prefix="/v1")
api_router.include_router(dht.router, prefix="/v1")
api_router.include_router(flame.router, prefix="/v1")
api_router.include_router(imu.router, prefix="/v1")
api_router.include_router(loadcell.router, prefix="/v1")
api_router.include_router(mq5.router, prefix="/v1")
api_router.include_router(mq7.router, prefix="/v1")
api_router.include_router(rfid.router, prefix="/v1")
api_router.include_router(sound.router, prefix="/v1")
api_router.include_router(tcrt5000.router, prefix="/v1")
api_router.include_router(ultrasonic.router, prefix="/v1")

# Edge 센서 API 라우터 등록
api_router.include_router(edge_flame.router, prefix="/v1")
api_router.include_router(edge_pir.router, prefix="/v1")
api_router.include_router(edge_reed.router, prefix="/v1")
api_router.include_router(edge_tilt.router, prefix="/v1")

# Actuator 로그 API 라우터 등록
api_router.include_router(actuator_buzzer.router, prefix="/v1")
api_router.include_router(actuator_irtx.router, prefix="/v1")
api_router.include_router(actuator_relay.router, prefix="/v1")
api_router.include_router(actuator_servo.router, prefix="/v1")

# DeviceRTCStatus API 라우터 등록
api_router.include_router(device_rtc.router, prefix="/v1")

__all__ = ["api_router"]

