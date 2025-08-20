"""
API 스키마 정의

FastAPI 엔드포인트의 요청/응답 모델을 정의합니다.
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field, validator
from uuid import UUID


# ============================================================================
# 사용자 관련 스키마
# ============================================================================

class UserBase(BaseModel):
    """사용자 기본 스키마"""
    user_name: str = Field(..., min_length=1, max_length=100, description="사용자 이름")
    email: Optional[EmailStr] = Field(None, description="이메일 주소")
    phone_number: Optional[str] = Field(None, description="전화번호")
    user_role: str = Field(..., description="사용자 역할")

    @validator('phone_number')
    def validate_phone_number(cls, v):
        if v is not None:
            # 전화번호 형식 검증 (한국 전화번호)
            import re
            # 01012345678 형식 허용 (11자리)
            phone_pattern = re.compile(r'^01[0-9]{8,9}$')
            if not phone_pattern.match(v):
                raise ValueError('올바른 전화번호 형식이 아닙니다')
        return v

    @validator('user_role')
    def validate_user_role(cls, v):
        allowed_roles = ['admin', 'caregiver', 'family', 'user']
        if v not in allowed_roles:
            raise ValueError(f'허용되지 않는 역할입니다. 허용된 역할: {allowed_roles}')
        return v


class UserCreate(UserBase):
    """사용자 생성 요청 스키마"""
    pass


class UserUpdate(BaseModel):
    """사용자 수정 요청 스키마"""
    user_name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    user_role: Optional[str] = None

    @validator('phone_number')
    def validate_phone_number(cls, v):
        if v is not None:
            import re
            # 01012345678 형식 허용 (11자리)
            phone_pattern = re.compile(r'^01[0-9]{8,9}$')
            if not phone_pattern.match(v):
                raise ValueError('올바른 전화번호 형식이 아닙니다')
        return v

    @validator('user_role')
    def validate_user_role(cls, v):
        if v is not None:
            allowed_roles = ['admin', 'caregiver', 'family', 'user']
            if v not in allowed_roles:
                raise ValueError(f'허용되지 않는 역할입니다. 허용된 역할: {allowed_roles}')
        return v


class UserResponse(UserBase):
    """사용자 응답 스키마"""
    user_id: UUID
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserListResponse(BaseModel):
    """사용자 목록 응답 스키마"""
    users: List[UserResponse]
    total: int
    page: int
    size: int


# ============================================================================
# 디바이스 관련 스키마
# ============================================================================

class DeviceBase(BaseModel):
    """디바이스 기본 스키마"""
    location_label: Optional[str] = Field(None, max_length=200, description="설치 위치 라벨")


class DeviceCreate(DeviceBase):
    """디바이스 생성 요청 스키마"""
    device_id: str = Field(..., min_length=1, max_length=64, description="디바이스 고유 ID")
    user_id: Optional[UUID] = Field(None, description="할당된 사용자 ID")


class DeviceUpdate(BaseModel):
    """디바이스 수정 요청 스키마"""
    location_label: Optional[str] = Field(None, max_length=200)
    user_id: Optional[UUID] = None


class DeviceResponse(DeviceBase):
    """디바이스 응답 스키마"""
    device_id: str
    user_id: Optional[UUID] = None
    installed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class DeviceListResponse(BaseModel):
    """디바이스 목록 응답 스키마"""
    devices: List[DeviceResponse]
    total: int
    page: int
    size: int


class DeviceAssignmentRequest(BaseModel):
    """디바이스 할당 요청 스키마"""
    user_id: UUID = Field(..., description="할당할 사용자 ID")


# ============================================================================
# 공통 응답 스키마
# ============================================================================

class SuccessResponse(BaseModel):
    """성공 응답 스키마"""
    message: str
    data: Optional[dict] = None


class ErrorResponse(BaseModel):
    """에러 응답 스키마"""
    error: str
    detail: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class PaginationParams(BaseModel):
    """페이지네이션 파라미터"""
    page: int = Field(1, ge=1, description="페이지 번호")
    size: int = Field(10, ge=1, le=100, description="페이지 크기")


# ============================================================================
# 센서 데이터 스키마 (향후 확장용)
# ============================================================================

class SensorDataBase(BaseModel):
    """센서 데이터 기본 스키마"""
    device_id: str
    timestamp: datetime
    value: float
    unit: Optional[str] = None


class SensorDataResponse(SensorDataBase):
    """센서 데이터 응답 스키마"""
    id: int

    class Config:
        from_attributes = True 