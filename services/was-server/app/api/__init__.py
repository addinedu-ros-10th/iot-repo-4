"""
API 패키지 초기화

API 버전 관리 및 라우터 등록을 담당합니다.
"""

from fastapi import APIRouter
from app.api.v1 import users, devices, sensors

# API 버전별 라우터 등록
api_router = APIRouter()

# v1 API 등록
api_router.include_router(users.router, prefix="/v1/users", tags=["users"])
api_router.include_router(devices.router, prefix="/v1/devices", tags=["devices"])
api_router.include_router(sensors.router, prefix="/v1/sensors", tags=["sensors"])

__all__ = ["api_router"]

