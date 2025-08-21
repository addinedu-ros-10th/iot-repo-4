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
# 센서 데이터 스키마
# ============================================================================

# CDS (조도 센서) 스키마
class CDSDataCreate(BaseModel):
    """CDS 센서 데이터 생성 스키마"""
    time: datetime
    device_id: str
    analog_value: Optional[int] = None
    lux_value: Optional[float] = None
    raw_payload: Optional[dict] = None


class CDSDataUpdate(BaseModel):
    """CDS 센서 데이터 수정 스키마"""
    analog_value: Optional[int] = None
    lux_value: Optional[float] = None
    raw_payload: Optional[dict] = None


class CDSDataResponse(BaseModel):
    """CDS 센서 데이터 응답 스키마"""
    time: datetime
    device_id: str
    analog_value: Optional[int] = None
    lux_value: Optional[float] = None
    raw_payload: Optional[dict] = None

    class Config:
        from_attributes = True


# DHT (온습도 센서) 스키마
class DHTDataCreate(BaseModel):
    """DHT 센서 데이터 생성 스키마"""
    time: datetime
    device_id: str
    temperature_c: Optional[float] = None
    humidity_percent: Optional[float] = None
    raw_payload: Optional[dict] = None


class DHTDataUpdate(BaseModel):
    """DHT 센서 데이터 수정 스키마"""
    temperature_c: Optional[float] = None
    humidity_percent: Optional[float] = None
    raw_payload: Optional[dict] = None


class DHTDataResponse(BaseModel):
    """DHT 센서 데이터 응답 스키마"""
    time: datetime
    device_id: str
    temperature_c: Optional[float] = None
    humidity_percent: Optional[float] = None
    raw_payload: Optional[dict] = None

    class Config:
        from_attributes = True


# Flame (화재 감지 센서) 스키마
class FlameDataCreate(BaseModel):
    """Flame 센서 데이터 생성 스키마"""
    time: datetime
    device_id: str
    analog_value: Optional[int] = None
    flame_detected: Optional[bool] = None
    raw_payload: Optional[dict] = None


class FlameDataUpdate(BaseModel):
    """Flame 센서 데이터 수정 스키마"""
    analog_value: Optional[int] = None
    flame_detected: Optional[bool] = None
    raw_payload: Optional[dict] = None


class FlameDataResponse(BaseModel):
    """Flame 센서 데이터 응답 스키마"""
    time: datetime
    device_id: str
    analog_value: Optional[int] = None
    flame_detected: Optional[bool] = None
    raw_payload: Optional[dict] = None

    class Config:
        from_attributes = True


# 기존 센서 데이터 스키마 (향후 확장용)
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


# IMU (관성 측정 장치) 센서 스키마
class IMUDataCreate(BaseModel):
    """IMU 센서 데이터 생성 스키마"""
    time: datetime
    device_id: str
    accel_x: Optional[float] = None
    accel_y: Optional[float] = None
    accel_z: Optional[float] = None
    gyro_x: Optional[float] = None
    gyro_y: Optional[float] = None
    gyro_z: Optional[float] = None
    raw_payload: Optional[dict] = None


class IMUDataUpdate(BaseModel):
    """IMU 센서 데이터 수정 스키마"""
    accel_x: Optional[float] = None
    accel_y: Optional[float] = None
    accel_z: Optional[float] = None
    gyro_x: Optional[float] = None
    gyro_y: Optional[float] = None
    gyro_z: Optional[float] = None
    raw_payload: Optional[dict] = None


class IMUDataResponse(BaseModel):
    """IMU 센서 데이터 응답 스키마"""
    time: datetime
    device_id: str
    accel_x: Optional[float] = None
    accel_y: Optional[float] = None
    accel_z: Optional[float] = None
    gyro_x: Optional[float] = None
    gyro_y: Optional[float] = None
    gyro_z: Optional[float] = None
    raw_payload: Optional[dict] = None

    class Config:
        from_attributes = True


# LoadCell (로드셀) 센서 스키마
class LoadCellDataCreate(BaseModel):
    """LoadCell 센서 데이터 생성 스키마"""
    time: datetime
    device_id: str
    raw_value: Optional[int] = None
    weight_kg: Optional[float] = None
    calibrated: Optional[bool] = None
    raw_payload: Optional[dict] = None


class LoadCellDataUpdate(BaseModel):
    """LoadCell 센서 데이터 수정 스키마"""
    raw_value: Optional[int] = None
    weight_kg: Optional[float] = None
    calibrated: Optional[bool] = None
    raw_payload: Optional[dict] = None


class LoadCellDataResponse(BaseModel):
    """LoadCell 센서 데이터 응답 스키마"""
    time: datetime
    device_id: str
    raw_value: Optional[int] = None
    weight_kg: Optional[float] = None
    calibrated: Optional[bool] = None
    raw_payload: Optional[dict] = None

    class Config:
        from_attributes = True


# MQ5 (가스 센서) 스키마
class MQ5DataCreate(BaseModel):
    """MQ5 가스 센서 데이터 생성 스키마"""
    time: datetime
    device_id: str
    analog_value: Optional[int] = None
    ppm_value: Optional[float] = None
    gas_type: Optional[str] = None
    raw_payload: Optional[dict] = None


class MQ5DataUpdate(BaseModel):
    """MQ5 가스 센서 데이터 수정 스키마"""
    analog_value: Optional[int] = None
    ppm_value: Optional[float] = None
    gas_type: Optional[str] = None
    raw_payload: Optional[dict] = None


class MQ5DataResponse(BaseModel):
    """MQ5 가스 센서 데이터 응답 스키마"""
    time: datetime
    device_id: str
    analog_value: Optional[int] = None
    ppm_value: Optional[float] = None
    gas_type: Optional[str] = None
    raw_payload: Optional[dict] = None

    class Config:
        from_attributes = True


# MQ7 (가스 센서) 스키마
class MQ7DataCreate(BaseModel):
    """MQ7 가스 센서 데이터 생성 스키마"""
    time: datetime
    device_id: str
    analog_value: Optional[int] = None
    ppm_value: Optional[float] = None
    gas_type: Optional[str] = None
    raw_payload: Optional[dict] = None


class MQ7DataUpdate(BaseModel):
    """MQ7 가스 센서 데이터 수정 스키마"""
    analog_value: Optional[int] = None
    ppm_value: Optional[int] = None
    gas_type: Optional[str] = None
    raw_payload: Optional[dict] = None


class MQ7DataResponse(BaseModel):
    """MQ7 가스 센서 데이터 응답 스키마"""
    time: datetime
    device_id: str
    analog_value: Optional[int] = None
    ppm_value: Optional[float] = None
    gas_type: Optional[str] = None
    raw_payload: Optional[dict] = None

    class Config:
        from_attributes = True


# RFID (RFID 센서) 스키마
class RFIDDataCreate(BaseModel):
    """RFID 센서 데이터 생성 스키마"""
    time: datetime
    device_id: str
    card_id: Optional[str] = None
    card_type: Optional[str] = None
    read_success: Optional[bool] = None
    raw_payload: Optional[dict] = None


class RFIDDataUpdate(BaseModel):
    """RFID 센서 데이터 수정 스키마"""
    card_id: Optional[str] = None
    card_type: Optional[str] = None
    read_success: Optional[bool] = None
    raw_payload: Optional[dict] = None


class RFIDDataResponse(BaseModel):
    """RFID 센서 데이터 응답 스키마"""
    time: datetime
    device_id: str
    card_id: Optional[str] = None
    card_type: Optional[str] = None
    read_success: Optional[bool] = None
    raw_payload: Optional[dict] = None

    class Config:
        from_attributes = True


# Sound (사운드 센서) 스키마
class SoundDataCreate(BaseModel):
    """Sound 센서 데이터 생성 스키마"""
    time: datetime
    device_id: str
    analog_value: Optional[int] = None
    db_value: Optional[float] = None
    threshold_exceeded: Optional[bool] = None
    raw_payload: Optional[dict] = None


class SoundDataUpdate(BaseModel):
    """Sound 센서 데이터 수정 스키마"""
    analog_value: Optional[int] = None
    db_value: Optional[float] = None
    threshold_exceeded: Optional[bool] = None
    raw_payload: Optional[dict] = None


class SoundDataResponse(BaseModel):
    """Sound 센서 데이터 응답 스키마"""
    time: datetime
    device_id: str
    analog_value: Optional[int] = None
    db_value: Optional[float] = None
    threshold_exceeded: Optional[bool] = None
    raw_payload: Optional[dict] = None

    class Config:
        from_attributes = True


# TCRT5000 (근접 센서) 스키마
class TCRT5000DataCreate(BaseModel):
    """TCRT5000 근접 센서 데이터 생성 스키마"""
    time: datetime
    device_id: str
    digital_value: Optional[bool] = None
    analog_value: Optional[int] = None
    object_detected: Optional[bool] = None
    raw_payload: Optional[dict] = None


class TCRT5000DataUpdate(BaseModel):
    """TCRT5000 근접 센서 데이터 수정 스키마"""
    digital_value: Optional[bool] = None
    analog_value: Optional[int] = None
    object_detected: Optional[bool] = None
    raw_payload: Optional[dict] = None


class TCRT5000DataResponse(BaseModel):
    """TCRT5000 근접 센서 데이터 응답 스키마"""
    time: datetime
    device_id: str
    digital_value: Optional[bool] = None
    analog_value: Optional[int] = None
    object_detected: Optional[bool] = None
    raw_payload: Optional[dict] = None

    class Config:
        from_attributes = True


# Ultrasonic (초음파 센서) 스키마
class UltrasonicDataCreate(BaseModel):
    """Ultrasonic 센서 데이터 생성 스키마"""
    time: datetime
    device_id: str
    distance_cm: Optional[float] = None
    raw_value: Optional[int] = None
    measurement_valid: Optional[bool] = None
    raw_payload: Optional[dict] = None


class UltrasonicDataUpdate(BaseModel):
    """Ultrasonic 센서 데이터 수정 스키마"""
    distance_cm: Optional[float] = None
    raw_value: Optional[int] = None
    measurement_valid: Optional[bool] = None
    raw_payload: Optional[dict] = None


class UltrasonicDataResponse(BaseModel):
    """Ultrasonic 센서 데이터 응답 스키마"""
    time: datetime
    device_id: str
    distance_cm: Optional[float] = None
    raw_value: Optional[int] = None
    measurement_valid: Optional[bool] = None
    raw_payload: Optional[dict] = None

    class Config:
        from_attributes = True


# Edge 센서 스키마들
class EdgeFlameDataCreate(BaseModel):
    """Edge Flame 센서 데이터 생성 스키마"""
    time: datetime
    device_id: str
    flame_detected: bool
    confidence: Optional[float] = None
    alert_level: Optional[str] = None
    raw_payload: Optional[dict] = None


class EdgeFlameDataUpdate(BaseModel):
    """Edge Flame 센서 데이터 수정 스키마"""
    flame_detected: Optional[bool] = None
    confidence: Optional[float] = None
    alert_level: Optional[str] = None
    raw_payload: Optional[dict] = None


class EdgeFlameDataResponse(BaseModel):
    """Edge Flame 센서 데이터 응답 스키마"""
    time: datetime
    device_id: str
    flame_detected: bool
    confidence: Optional[float] = None
    alert_level: Optional[str] = None
    raw_payload: Optional[dict] = None

    class Config:
        from_attributes = True


class EdgePIRDataCreate(BaseModel):
    """Edge PIR 센서 데이터 생성 스키마"""
    time: datetime
    device_id: str
    motion_detected: bool
    confidence: Optional[float] = None
    motion_direction: Optional[str] = None
    raw_payload: Optional[dict] = None


class EdgePIRDataUpdate(BaseModel):
    """Edge PIR 센서 데이터 수정 스키마"""
    motion_detected: Optional[bool] = None
    confidence: Optional[float] = None
    motion_direction: Optional[str] = None
    raw_payload: Optional[dict] = None


class EdgePIRDataResponse(BaseModel):
    """Edge PIR 센서 데이터 응답 스키마"""
    time: datetime
    device_id: str
    motion_detected: bool
    confidence: Optional[float] = None
    motion_direction: Optional[str] = None
    raw_payload: Optional[dict] = None

    class Config:
        from_attributes = True


class EdgeReedDataCreate(BaseModel):
    """Edge Reed 스위치 센서 데이터 생성 스키마"""
    time: datetime
    device_id: str
    switch_state: bool
    magnetic_field_detected: Optional[bool] = None
    raw_payload: Optional[dict] = None


class EdgeReedDataUpdate(BaseModel):
    """Edge Reed 스위치 센서 데이터 수정 스키마"""
    switch_state: Optional[bool] = None
    magnetic_field_detected: Optional[bool] = None
    raw_payload: Optional[dict] = None


class EdgeReedDataResponse(BaseModel):
    """Edge Reed 스위치 센서 데이터 응답 스키마"""
    time: datetime
    device_id: str
    switch_state: bool
    magnetic_field_detected: Optional[bool] = None
    raw_payload: Optional[dict] = None

    class Config:
        from_attributes = True


class EdgeTiltDataCreate(BaseModel):
    """Edge Tilt 센서 데이터 생성 스키마"""
    time: datetime
    device_id: str
    tilt_detected: bool
    tilt_angle: Optional[float] = None
    tilt_direction: Optional[str] = None
    raw_payload: Optional[dict] = None


class EdgeTiltDataUpdate(BaseModel):
    """Edge Tilt 센서 데이터 수정 스키마"""
    tilt_detected: Optional[bool] = None
    tilt_angle: Optional[float] = None
    tilt_direction: Optional[str] = None
    raw_payload: Optional[dict] = None


class EdgeTiltDataResponse(BaseModel):
    """Edge Tilt 센서 데이터 응답 스키마"""
    time: datetime
    device_id: str
    tilt_detected: bool
    tilt_angle: Optional[float] = None
    tilt_direction: Optional[str] = None
    raw_payload: Optional[dict] = None

    class Config:
        from_attributes = True


# Actuator 로그 스키마들
class ActuatorBuzzerDataCreate(BaseModel):
    """Buzzer 액추에이터 로그 생성 스키마"""
    time: datetime
    device_id: str
    buzzer_type: str
    state: str
    freq_hz: Optional[int] = None
    duration_ms: Optional[int] = None
    reason: Optional[str] = None
    raw_payload: Optional[dict] = None


class ActuatorBuzzerDataUpdate(BaseModel):
    """Buzzer 액추에이터 로그 수정 스키마"""
    buzzer_type: Optional[str] = None
    state: Optional[str] = None
    freq_hz: Optional[int] = None
    duration_ms: Optional[int] = None
    reason: Optional[str] = None
    raw_payload: Optional[dict] = None


class ActuatorBuzzerDataResponse(BaseModel):
    """Buzzer 액추에이터 로그 응답 스키마"""
    time: datetime
    device_id: str
    buzzer_type: str
    state: str
    freq_hz: Optional[int] = None
    duration_ms: Optional[int] = None
    reason: Optional[str] = None
    raw_payload: Optional[dict] = None

    class Config:
        from_attributes = True


class ActuatorIRTXDataCreate(BaseModel):
    """IR TX 액추에이터 로그 생성 스키마"""
    time: datetime
    device_id: str
    protocol: Optional[str] = None
    address_hex: Optional[str] = None
    command_hex: str
    repeat_cnt: Optional[int] = None
    raw_payload: Optional[dict] = None


class ActuatorIRTXDataUpdate(BaseModel):
    """IR TX 액추에이터 로그 수정 스키마"""
    protocol: Optional[str] = None
    address_hex: Optional[str] = None
    command_hex: Optional[str] = None
    repeat_cnt: Optional[int] = None
    raw_payload: Optional[dict] = None


class ActuatorIRTXDataResponse(BaseModel):
    """IR TX 액추에이터 로그 응답 스키마"""
    time: datetime
    device_id: str
    protocol: Optional[str] = None
    address_hex: Optional[str] = None
    command_hex: str
    repeat_cnt: Optional[int] = None
    raw_payload: Optional[dict] = None

    class Config:
        from_attributes = True


# ============================================================================
# Actuator 로그 관련 스키마
# ============================================================================

class ActuatorBuzzerDataCreate(BaseModel):
    """Buzzer 액추에이터 로그 생성 스키마"""
    time: datetime
    device_id: str
    buzzer_type: str
    state: str
    freq_hz: Optional[int] = None
    duration_ms: Optional[int] = None
    reason: Optional[str] = None
    raw_payload: Optional[dict] = None


class ActuatorBuzzerDataUpdate(BaseModel):
    """Buzzer 액추에이터 로그 수정 스키마"""
    buzzer_type: Optional[str] = None
    state: Optional[str] = None
    freq_hz: Optional[int] = None
    duration_ms: Optional[int] = None
    reason: Optional[str] = None
    raw_payload: Optional[dict] = None


class ActuatorBuzzerDataResponse(BaseModel):
    """Buzzer 액추에이터 로그 응답 스키마"""
    time: datetime
    device_id: str
    buzzer_type: str
    state: str
    freq_hz: Optional[int] = None
    duration_ms: Optional[int] = None
    reason: Optional[str] = None
    raw_payload: Optional[dict] = None

    class Config:
        from_attributes = True


class ActuatorIRTXDataCreate(BaseModel):
    """IR TX 액추에이터 로그 생성 스키마"""
    time: datetime
    device_id: str
    protocol: Optional[str] = None
    address_hex: Optional[str] = None
    command_hex: str
    repeat_cnt: Optional[int] = None
    raw_payload: Optional[dict] = None


class ActuatorIRTXDataUpdate(BaseModel):
    """IR TX 액추에이터 로그 수정 스키마"""
    protocol: Optional[str] = None
    address_hex: Optional[str] = None
    command_hex: Optional[str] = None
    repeat_cnt: Optional[int] = None
    raw_payload: Optional[dict] = None


class ActuatorIRTXDataResponse(BaseModel):
    """IR TX 액추에이터 로그 응답 스키마"""
    time: datetime
    device_id: str
    protocol: Optional[str] = None
    address_hex: Optional[str] = None
    command_hex: str
    repeat_cnt: Optional[int] = None
    raw_payload: Optional[dict] = None

    class Config:
        from_attributes = True


class ActuatorRelayDataCreate(BaseModel):
    """Relay 액추에이터 로그 생성 스키마"""
    time: datetime
    device_id: str
    channel: int
    state: str
    reason: Optional[str] = None
    raw_payload: Optional[dict] = None


class ActuatorRelayDataUpdate(BaseModel):
    """Relay 액추에이터 로그 수정 스키마"""
    channel: Optional[int] = None
    state: Optional[str] = None
    reason: Optional[str] = None
    raw_payload: Optional[dict] = None


class ActuatorRelayDataResponse(BaseModel):
    """Relay 액추에이터 로그 응답 스키마"""
    time: datetime
    device_id: str
    channel: int
    state: str
    reason: Optional[str] = None
    raw_payload: Optional[dict] = None

    class Config:
        from_attributes = True


class ActuatorServoDataCreate(BaseModel):
    """Servo 액추에이터 로그 생성 스키마"""
    time: datetime
    device_id: str
    channel: int
    angle_deg: Optional[float] = None
    pwm_us: Optional[int] = None
    reason: Optional[str] = None
    raw_payload: Optional[dict] = None


class ActuatorServoDataUpdate(BaseModel):
    """Servo 액추에이터 로그 수정 스키마"""
    channel: Optional[int] = None
    angle_deg: Optional[float] = None
    pwm_us: Optional[int] = None
    reason: Optional[str] = None
    raw_payload: Optional[dict] = None


class ActuatorServoDataResponse(BaseModel):
    """Servo 액추에이터 로그 응답 스키마"""
    time: datetime
    device_id: str
    channel: int
    angle_deg: Optional[float] = None
    pwm_us: Optional[int] = None
    reason: Optional[str] = None
    raw_payload: Optional[dict] = None

    class Config:
        from_attributes = True


# Device RTC 상태 스키마
class DeviceRTCDataCreate(BaseModel):
    """Device RTC 상태 생성 스키마"""
    time: datetime
    device_id: str
    rtc_epoch_s: Optional[int] = None
    drift_ms: Optional[int] = None
    sync_source: Optional[str] = None
    raw_payload: Optional[dict] = None


class DeviceRTCDataUpdate(BaseModel):
    """Device RTC 상태 수정 스키마"""
    rtc_epoch_s: Optional[int] = None
    drift_ms: Optional[int] = None
    sync_source: Optional[str] = None
    raw_payload: Optional[dict] = None


class DeviceRTCDataResponse(BaseModel):
    """Device RTC 상태 응답 스키마"""
    time: datetime
    device_id: str
    rtc_epoch_s: Optional[int] = None
    drift_ms: Optional[int] = None
    sync_source: Optional[str] = None
    raw_payload: Optional[dict] = None

    class Config:
        from_attributes = True 