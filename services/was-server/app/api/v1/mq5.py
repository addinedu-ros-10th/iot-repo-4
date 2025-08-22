"""
MQ5 가스 센서 데이터 API

Clean Architecture 원칙에 따라 MQ5 가스 센서의 원시 데이터를 관리하는 API 엔드포인트를 제공합니다.
"""

from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database import get_db
from app.core.container import container
from app.interfaces.services.sensor_service_interface import IMQ5Service
from app.api.v1.schemas import (
    SensorRawMQ5Create,
    SensorRawMQ5Update,
    SensorRawMQ5Response
)

router = APIRouter()


def get_mq5_service(db: AsyncSession = Depends(get_db)) -> IMQ5Service:
    """MQ5 가스 센서 서비스 의존성 주입"""
    return container.get_mq5_service(db)


@router.post("/create", response_model=SensorRawMQ5Response, status_code=201)
async def create_mq5_data(
    data: SensorRawMQ5Create,
    mq5_service: IMQ5Service = Depends(get_mq5_service)
):
    """MQ5 가스 센서 데이터 생성"""
    return await mq5_service.create_sensor_data(data)


@router.get("/list", response_model=List[SensorRawMQ5Response])
async def get_mq5_data_list(
    device_id: Optional[str] = Query(None, description="디바이스 ID"),
    start_time: Optional[datetime] = Query(None, description="시작 시간"),
    end_time: Optional[datetime] = Query(None, description="종료 시간"),
    limit_count: int = Query(100, description="조회할 데이터 개수", ge=1, le=1000),
    mq5_service: IMQ5Service = Depends(get_mq5_service)
):
    """MQ5 가스 센서 데이터 목록 조회"""
    return await mq5_service.get_sensor_data_list(
        device_id=device_id,
        start_time=start_time,
        end_time=end_time,
        limit=limit_count
    )


@router.get("/latest", response_model=Optional[SensorRawMQ5Response])
async def get_latest_mq5_data(
    device_id: str = Query(..., description="디바이스 ID"),
    mq5_service: IMQ5Service = Depends(get_mq5_service)
):
    """특정 디바이스의 최신 MQ5 가스 센서 데이터 조회"""
    return await mq5_service.get_latest_sensor_data(device_id)


@router.get("/{device_id}/{timestamp}", response_model=SensorRawMQ5Response)
async def get_mq5_data(
    device_id: str,
    timestamp: datetime,
    mq5_service: IMQ5Service = Depends(get_mq5_service)
):
    """특정 시간의 MQ5 가스 센서 데이터 조회"""
    return await mq5_service.get_sensor_data(device_id, timestamp)


@router.put("/{device_id}/{timestamp}", response_model=SensorRawMQ5Response)
async def update_mq5_data(
    device_id: str,
    timestamp: datetime,
    data: SensorRawMQ5Update,
    mq5_service: IMQ5Service = Depends(get_mq5_service)
):
    """MQ5 가스 센서 데이터 수정"""
    return await mq5_service.update_sensor_data(device_id, timestamp, data)


@router.delete("/{device_id}/{timestamp}")
async def delete_mq5_data(
    device_id: str,
    timestamp: datetime,
    mq5_service: IMQ5Service = Depends(get_mq5_service)
):
    """MQ5 가스 센서 데이터 삭제"""
    success = await mq5_service.delete_sensor_data(device_id, timestamp)
    if success:
        return {"message": "데이터가 성공적으로 삭제되었습니다"}
    return {"message": "데이터 삭제 실패"}


@router.get("/{device_id}/stats/gas", response_model=dict)
async def get_mq5_gas_stats(
    device_id: str,
    start_time: Optional[datetime] = Query(None, description="시작 시간"),
    end_time: Optional[datetime] = Query(None, description="종료 시간"),
    mq5_service: IMQ5Service = Depends(get_mq5_service)
):
    """MQ5 가스 센서의 가스 농도 통계 정보 조회"""
    return await mq5_service.get_gas_statistics(device_id, start_time, end_time)


@router.get("/{device_id}/alerts/high-concentration", response_model=dict)
async def get_mq5_high_concentration_alerts(
    device_id: str,
    threshold_ppm: float = Query(100.0, description="높은 농도 임계값 (PPM)"),
    start_time: Optional[datetime] = Query(None, description="시작 시간"),
    end_time: Optional[datetime] = Query(None, description="종료 시간"),
    mq5_service: IMQ5Service = Depends(get_mq5_service)
):
    """MQ5 가스 센서의 높은 농도 알림 조회"""
    return await mq5_service.get_high_concentration_alerts(
        device_id, threshold_ppm, start_time, end_time
    )
