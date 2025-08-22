"""
MQ5 가스 센서 데이터 리포지토리 구현체

Clean Architecture 원칙에 따라 MQ5 가스 센서 데이터에 대한 데이터 접근을 담당합니다.
"""

from datetime import datetime
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload

from app.interfaces.repositories.sensor_repository import IMQ5Repository
from app.infrastructure.models import SensorRawMQ5
from app.api.v1.schemas import (
    MQ5DataCreate,
    MQ5DataUpdate,
    MQ5DataResponse
)


class MQ5Repository(IMQ5Repository):
    """MQ5 가스 센서 데이터 리포지토리 구현체"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self, data: MQ5DataCreate) -> MQ5DataResponse:
        """MQ5 가스 센서 데이터 생성"""
        db_data = SensorRawMQ5(**data.dict())
        self.db.add(db_data)
        await self.db.commit()
        await self.db.refresh(db_data)
        return MQ5DataResponse.from_orm(db_data)
    
    async def get_by_id(
        self,
        device_id: str,
        timestamp: datetime
    ) -> Optional[MQ5DataResponse]:
        """특정 시간의 MQ5 가스 센서 데이터 조회"""
        query = select(SensorRawMQ5).where(
            and_(
                SensorRawMQ5.device_id == device_id,
                SensorRawMQ5.time == timestamp
            )
        )
        
        result = await self.db.execute(query)
        data = result.scalar_one_or_none()
        
        if data:
            return MQ5DataResponse.from_orm(data)
        return None
    
    async def get_latest(self, device_id: str) -> Optional[MQ5DataResponse]:
        """최신 MQ5 가스 센서 데이터 조회"""
        query = (
            select(SensorRawMQ5)
            .where(SensorRawMQ5.device_id == device_id)
            .order_by(SensorRawMQ5.time.desc())
        )
        
        result = await self.db.execute(query)
        data = result.scalars().first()
        
        if data:
            return MQ5DataResponse.from_orm(data)
        return None
    
    async def get_list(
        self,
        device_id: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        limit_count: int = 100
    ) -> List[MQ5DataResponse]:
        """MQ5 가스 센서 데이터 목록 조회"""
        query = select(SensorRawMQ5)
        
        # 필터 조건 추가
        if device_id:
            query = query.where(SensorRawMQ5.device_id == device_id)
        if start_time:
            query = query.where(SensorRawMQ5.time >= start_time)
        if end_time:
            query = query.where(SensorRawMQ5.time <= end_time)
        
        # 시간 역순으로 정렬하고 제한
        query = query.order_by(SensorRawMQ5.time.desc()).limit(limit_count)
        
        result = await self.db.execute(query)
        data_list = result.scalars().all()
        
        # 결과를 리스트로 변환하여 반환
        return [MQ5DataResponse.from_orm(data) for data in data_list]
    
    async def update(
        self,
        device_id: str,
        timestamp: datetime,
        data: MQ5DataUpdate
    ) -> Optional[MQ5DataResponse]:
        """MQ5 가스 센서 데이터 수정"""
        query = select(SensorRawMQ5).where(
            and_(
                SensorRawMQ5.device_id == device_id,
                SensorRawMQ5.time == timestamp
            )
        )
        
        result = await self.db.execute(query)
        db_data = result.scalar_one_or_none()
        
        if not db_data:
            return None
        
        # 업데이트할 필드만 수정
        update_data = data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_data, field, value)
        
        await self.db.commit()
        await self.db.refresh(db_data)
        return MQ5DataResponse.from_orm(db_data)
    
    async def delete(self, device_id: str, timestamp: datetime) -> bool:
        """MQ5 가스 센서 데이터 삭제"""
        query = select(SensorRawMQ5).where(
            and_(
                SensorRawMQ5.device_id == device_id,
                SensorRawMQ5.time == timestamp
            )
        )
        
        result = await self.db.execute(query)
        db_data = result.scalar_one_or_none()
        
        if not db_data:
            return False
        
        await self.db.delete(db_data)
        await self.db.commit()
        return True
    
    async def get_statistics(
        self,
        device_id: str,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> dict:
        """MQ5 가스 센서 데이터 기본 통계 조회"""
        return await self.get_gas_statistics(device_id, start_time, end_time)
    
    async def get_gas_statistics(
        self,
        device_id: str,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> dict:
        """MQ5 가스 센서의 가스 농도 통계 정보 조회"""
        query = select(SensorRawMQ5).where(SensorRawMQ5.device_id == device_id)
        
        if start_time:
            query = query.where(SensorRawMQ5.time >= start_time)
        if end_time:
            query = query.where(SensorRawMQ5.time <= end_time)
        
        result = await self.db.execute(query)
        data_list = result.scalars().all()
        
        if not data_list:
            return {
                "device_id": device_id,
                "total_records": 0,
                "gas_stats": None,
                "gas_type_distribution": None
            }
        
        # 가스 농도 데이터가 있는 레코드만 필터링
        ppm_data = [d.ppm_value for d in data_list if d.ppm_value is not None]
        analog_data = [d.analog_value for d in data_list if d.analog_value is not None]
        
        # 가스 타입별 분포
        gas_types = {}
        for data in data_list:
            if data.gas_type:
                gas_types[data.gas_type] = gas_types.get(data.gas_type, 0) + 1
        
        stats = {
            "device_id": device_id,
            "total_records": len(data_list),
            "gas_stats": {
                "ppm_count": len(ppm_data),
                "ppm_min": min(ppm_data) if ppm_data else None,
                "ppm_max": max(ppm_data) if ppm_data else None,
                "ppm_avg": sum(ppm_data) / len(ppm_data) if ppm_data else None,
                "analog_count": len(analog_data),
                "analog_min": min(analog_data) if analog_data else None,
                "analog_max": max(analog_data) if analog_data else None,
                "analog_avg": sum(analog_data) / len(analog_data) if analog_data else None
            },
            "gas_type_distribution": gas_types
        }
        
        return stats
    
    async def get_high_concentration_alerts(
        self,
        device_id: str,
        threshold_ppm: float,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> dict:
        """MQ5 가스 센서의 높은 농도 알림 조회"""
        query = select(SensorRawMQ5).where(
            and_(
                SensorRawMQ5.device_id == device_id,
                SensorRawMQ5.ppm_value > threshold_ppm
            )
        )
        
        if start_time:
            query = query.where(SensorRawMQ5.time >= start_time)
        if end_time:
            query = query.where(SensorRawMQ5.time <= end_time)
        
        result = await self.db.execute(query)
        alert_data = result.scalars().all()
        
        alerts = []
        for data in alert_data:
            alert_level = "HIGH" if data.ppm_value > threshold_ppm * 2 else "MEDIUM"
            alerts.append({
                "timestamp": data.time,
                "ppm_value": data.ppm_value,
                "analog_value": data.analog_value,
                "alert_level": alert_level,
                "gas_type": data.gas_type
            })
        
        return {
            "device_id": device_id,
            "threshold_ppm": threshold_ppm,
            "total_alerts": len(alerts),
            "alerts": alerts,
            "alert_summary": {
                "high_level": len([a for a in alerts if a["alert_level"] == "HIGH"]),
                "medium_level": len([a for a in alerts if a["alert_level"] == "MEDIUM"])
            }
        }
