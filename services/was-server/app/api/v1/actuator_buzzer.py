"""
Buzzer 액추에이터 로그 API

Buzzer 액추에이터 로그 데이터에 대한 RESTful API 엔드포인트를 제공합니다.
"""

from typing import Optional, List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from app.core.container import DependencyContainer
from app.interfaces.services.actuator_service_interface import IActuatorBuzzerService
from app.api.v1.schemas import (
    ActuatorBuzzerDataCreate, ActuatorBuzzerDataUpdate, ActuatorBuzzerDataResponse
)

router = APIRouter(prefix="/actuator-buzzer", tags=["actuator-buzzer"])


@router.post("/", response_model=ActuatorBuzzerDataResponse, status_code=201)
async def create_actuator_buzzer_data(
    data: ActuatorBuzzerDataCreate,
    container: DependencyContainer = Depends()
) -> ActuatorBuzzerDataResponse:
    """Buzzer 액추에이터 로그 생성"""
    service = container.get_actuator_buzzer_service()
    return await service.create_actuator_data(data)


@router.get("/", response_model=List[ActuatorBuzzerDataResponse])
async def get_actuator_buzzer_data_list(
    device_id: Optional[str] = Query(None, description="디바이스 ID"),
    start_time: Optional[datetime] = Query(None, description="시작 시간"),
    end_time: Optional[datetime] = Query(None, description="종료 시간"),
    buzzer_type: Optional[str] = Query(None, description="부저 타입"),
    state: Optional[str] = Query(None, description="상태"),
    limit: int = Query(100, ge=1, le=1000, description="조회 개수"),
    offset: int = Query(0, ge=0, description="오프셋"),
    container: DependencyContainer = Depends()
) -> List[ActuatorBuzzerDataResponse]:
    """Buzzer 액추에이터 로그 목록 조회"""
    service = container.get_actuator_buzzer_service()
    return await service.get_actuator_data_list(
        device_id=device_id,
        start_time=start_time,
        end_time=end_time,
        buzzer_type=buzzer_type,
        state=state,
        limit=limit,
        offset=offset
    )


@router.get("/latest/{device_id}", response_model=ActuatorBuzzerDataResponse)
async def get_latest_actuator_buzzer_data(
    device_id: str,
    container: DependencyContainer = Depends()
) -> ActuatorBuzzerDataResponse:
    """최신 Buzzer 액추에이터 로그 조회"""
    service = container.get_actuator_buzzer_service()
    data = await service.get_latest_actuator_data(device_id)
    if not data:
        raise HTTPException(status_code=404, detail="액추에이터 로그를 찾을 수 없습니다")
    return data


@router.get("/{device_id}/{timestamp}", response_model=ActuatorBuzzerDataResponse)
async def get_actuator_buzzer_data(
    device_id: str,
    timestamp: datetime,
    container: DependencyContainer = Depends()
) -> ActuatorBuzzerDataResponse:
    """Buzzer 액추에이터 로그 조회"""
    service = container.get_actuator_buzzer_service()
    data = await service.get_actuator_data(device_id, timestamp)
    if not data:
        raise HTTPException(status_code=404, detail="액추에이터 로그를 찾을 수 없습니다")
    return data


@router.put("/{device_id}/{timestamp}", response_model=ActuatorBuzzerDataResponse)
async def update_actuator_buzzer_data(
    device_id: str,
    timestamp: datetime,
    data: ActuatorBuzzerDataUpdate,
    container: DependencyContainer = Depends()
) -> ActuatorBuzzerDataResponse:
    """Buzzer 액추에이터 로그 수정"""
    service = container.get_actuator_buzzer_service()
    return await service.update_actuator_data(device_id, timestamp, data)


@router.delete("/{device_id}/{timestamp}", status_code=204)
async def delete_actuator_buzzer_data(
    device_id: str,
    timestamp: datetime,
    container: DependencyContainer = Depends()
) -> None:
    """Buzzer 액추에이터 로그 삭제"""
    service = container.get_actuator_buzzer_service()
    await service.delete_actuator_data(device_id, timestamp)


@router.get("/{device_id}/statistics")
async def get_actuator_buzzer_statistics(
    device_id: str,
    start_time: Optional[datetime] = Query(None, description="시작 시간"),
    end_time: Optional[datetime] = Query(None, description="종료 시간"),
    container: DependencyContainer = Depends()
) -> dict:
    """Buzzer 액추에이터 로그 통계 조회"""
    service = container.get_actuator_buzzer_service()
    return await service.get_actuator_statistics(device_id, start_time, end_time)
