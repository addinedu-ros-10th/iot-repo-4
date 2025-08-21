"""
SQLAlchemy ORM 모델

데이터베이스의 모든 테이블에 대한 SQLAlchemy ORM 모델을 정의합니다.
"""

from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, String, Integer, Numeric, Boolean, Text, SmallInteger, BigInteger
from sqlalchemy import DateTime, UUID, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID, JSONB

Base = declarative_base()


class User(Base):
    """사용자 테이블 ORM 모델"""
    __tablename__ = "users"
    
    user_id: Mapped[str] = Column(PostgresUUID, primary_key=True)
    user_role: Mapped[str] = Column(String(20), nullable=False)
    user_name: Mapped[str] = Column(Text, nullable=False)
    email: Mapped[Optional[str]] = Column(Text, nullable=True)
    phone_number: Mapped[Optional[str]] = Column(Text, nullable=True)
    created_at: Mapped[Optional[datetime]] = Column(DateTime(timezone=True), nullable=True, default=datetime.utcnow)
    
    # 관계 정의
    devices: Mapped[List["Device"]] = relationship("Device", back_populates="user")


class Device(Base):
    """디바이스 테이블 ORM 모델"""
    __tablename__ = "devices"
    
    device_id: Mapped[str] = Column(String(64), primary_key=True)
    user_id: Mapped[Optional[str]] = Column(PostgresUUID, ForeignKey("users.user_id"), nullable=True)
    location_label: Mapped[Optional[str]] = Column(Text, nullable=True)
    installed_at: Mapped[Optional[datetime]] = Column(DateTime(timezone=True), nullable=True, default=datetime.utcnow)
    
    # 관계 정의
    user: Mapped[Optional[User]] = relationship("User", back_populates="devices")


class DeviceRTCStatus(Base):
    """디바이스 RTC 상태 테이블 ORM 모델"""
    __tablename__ = "device_rtc_status"
    
    time: Mapped[datetime] = Column(DateTime(timezone=True), primary_key=True)
    device_id: Mapped[str] = Column(String(64), ForeignKey("devices.device_id"), primary_key=True)
    rtc_epoch_s: Mapped[Optional[int]] = Column(BigInteger, nullable=True)
    drift_ms: Mapped[Optional[int]] = Column(Integer, nullable=True)
    sync_source: Mapped[Optional[str]] = Column(Text, nullable=True)
    raw_payload: Mapped[Optional[dict]] = Column(JSONB, nullable=True)


# 센서 데이터 테이블들
class SensorRawCDS(Base):
    """CDS 센서 원시 데이터 테이블 ORM 모델"""
    __tablename__ = "sensor_raw_cds"
    
    time: Mapped[datetime] = Column(DateTime(timezone=True), primary_key=True)
    device_id: Mapped[str] = Column(String(64), ForeignKey("devices.device_id"), primary_key=True)
    analog_value: Mapped[Optional[int]] = Column(Integer, nullable=True)
    lux_value: Mapped[Optional[Numeric]] = Column(Numeric, nullable=True)
    raw_payload: Mapped[Optional[dict]] = Column(JSONB, nullable=True)


class SensorRawDHT(Base):
    """DHT 센서 원시 데이터 테이블 ORM 모델"""
    __tablename__ = "sensor_raw_dht"
    
    time: Mapped[datetime] = Column(DateTime(timezone=True), primary_key=True)
    device_id: Mapped[str] = Column(String(64), ForeignKey("devices.device_id"), primary_key=True)
    temperature: Mapped[Optional[Numeric]] = Column(Numeric, nullable=True)
    humidity: Mapped[Optional[Numeric]] = Column(Numeric, nullable=True)
    heat_index: Mapped[Optional[Numeric]] = Column(Numeric, nullable=True)
    raw_payload: Mapped[Optional[dict]] = Column(JSONB, nullable=True)


class SensorRawFlame(Base):
    """화염 센서 원시 데이터 테이블 ORM 모델"""
    __tablename__ = "sensor_raw_flame"
    
    time: Mapped[datetime] = Column(DateTime(timezone=True), primary_key=True)
    device_id: Mapped[str] = Column(String(64), ForeignKey("devices.device_id"), primary_key=True)
    analog_value: Mapped[Optional[int]] = Column(Integer, nullable=True)
    flame_detected: Mapped[Optional[bool]] = Column(Boolean, nullable=True)
    raw_payload: Mapped[Optional[dict]] = Column(JSONB, nullable=True)


class SensorRawIMU(Base):
    """IMU 센서 원시 데이터 테이블 ORM 모델"""
    __tablename__ = "sensor_raw_imu"
    
    time: Mapped[datetime] = Column(DateTime(timezone=True), primary_key=True)
    device_id: Mapped[str] = Column(String(64), ForeignKey("devices.device_id"), primary_key=True)
    accel_x: Mapped[Optional[Numeric]] = Column(Numeric, nullable=True)
    accel_y: Mapped[Optional[Numeric]] = Column(Numeric, nullable=True)
    accel_z: Mapped[Optional[Numeric]] = Column(Numeric, nullable=True)
    gyro_x: Mapped[Optional[Numeric]] = Column(Numeric, nullable=True)
    gyro_y: Mapped[Optional[Numeric]] = Column(Numeric, nullable=True)
    gyro_z: Mapped[Optional[Numeric]] = Column(Numeric, nullable=True)
    mag_x: Mapped[Optional[Numeric]] = Column(Numeric, nullable=True)
    mag_y: Mapped[Optional[Numeric]] = Column(Numeric, nullable=True)
    mag_z: Mapped[Optional[Numeric]] = Column(Numeric, nullable=True)
    temperature: Mapped[Optional[Numeric]] = Column(Numeric, nullable=True)
    raw_payload: Mapped[Optional[dict]] = Column(JSONB, nullable=True)


class SensorRawLoadCell(Base):
    """로드셀 센서 원시 데이터 테이블 ORM 모델"""
    __tablename__ = "sensor_raw_loadcell"
    
    time: Mapped[datetime] = Column(DateTime(timezone=True), primary_key=True)
    device_id: Mapped[str] = Column(String(64), ForeignKey("devices.device_id"), primary_key=True)
    raw_value: Mapped[Optional[int]] = Column(Integer, nullable=True)
    weight_kg: Mapped[Optional[Numeric]] = Column(Numeric, nullable=True)
    calibrated: Mapped[Optional[bool]] = Column(Boolean, nullable=True)
    raw_payload: Mapped[Optional[dict]] = Column(JSONB, nullable=True)


class SensorRawMQ5(Base):
    """MQ5 가스 센서 원시 데이터 테이블 ORM 모델"""
    __tablename__ = "sensor_raw_mq5"
    
    time: Mapped[datetime] = Column(DateTime(timezone=True), primary_key=True)
    device_id: Mapped[str] = Column(String(64), ForeignKey("devices.device_id"), primary_key=True)
    analog_value: Mapped[Optional[int]] = Column(Integer, nullable=True)
    ppm_value: Mapped[Optional[Numeric]] = Column(Numeric, nullable=True)
    gas_type: Mapped[Optional[str]] = Column(Text, nullable=True)
    raw_payload: Mapped[Optional[dict]] = Column(JSONB, nullable=True)


class SensorRawMQ7(Base):
    """MQ7 가스 센서 원시 데이터 테이블 ORM 모델"""
    __tablename__ = "sensor_raw_mq7"
    
    time: Mapped[datetime] = Column(DateTime(timezone=True), primary_key=True)
    device_id: Mapped[str] = Column(String(64), ForeignKey("devices.device_id"), primary_key=True)
    analog_value: Mapped[Optional[int]] = Column(Integer, nullable=True)
    ppm_value: Mapped[Optional[Numeric]] = Column(Numeric, nullable=True)
    gas_type: Mapped[Optional[str]] = Column(Text, nullable=True)
    raw_payload: Mapped[Optional[dict]] = Column(JSONB, nullable=True)


class SensorRawRFID(Base):
    """RFID 센서 원시 데이터 테이블 ORM 모델"""
    __tablename__ = "sensor_raw_rfid"
    
    time: Mapped[datetime] = Column(DateTime(timezone=True), primary_key=True)
    device_id: Mapped[str] = Column(String(64), ForeignKey("devices.device_id"), primary_key=True)
    card_id: Mapped[Optional[str]] = Column(Text, nullable=True)
    card_type: Mapped[Optional[str]] = Column(Text, nullable=True)
    read_success: Mapped[Optional[bool]] = Column(Boolean, nullable=True)
    raw_payload: Mapped[Optional[dict]] = Column(JSONB, nullable=True)


class SensorRawSound(Base):
    """사운드 센서 원시 데이터 테이블 ORM 모델"""
    __tablename__ = "sensor_raw_sound"
    
    time: Mapped[datetime] = Column(DateTime(timezone=True), primary_key=True)
    device_id: Mapped[str] = Column(String(64), ForeignKey("devices.device_id"), primary_key=True)
    analog_value: Mapped[Optional[int]] = Column(Integer, nullable=True)
    db_value: Mapped[Optional[Numeric]] = Column(Numeric, nullable=True)
    threshold_exceeded: Mapped[Optional[bool]] = Column(Boolean, nullable=True)
    raw_payload: Mapped[Optional[dict]] = Column(JSONB, nullable=True)


class SensorRawTCRT5000(Base):
    """TCRT5000 근접 센서 원시 데이터 테이블 ORM 모델"""
    __tablename__ = "sensor_raw_tcrt5000"
    
    time: Mapped[datetime] = Column(DateTime(timezone=True), primary_key=True)
    device_id: Mapped[str] = Column(String(64), ForeignKey("devices.device_id"), primary_key=True)
    digital_value: Mapped[Optional[bool]] = Column(Boolean, nullable=True)
    analog_value: Mapped[Optional[int]] = Column(Integer, nullable=True)
    object_detected: Mapped[Optional[bool]] = Column(Boolean, nullable=True)
    raw_payload: Mapped[Optional[dict]] = Column(JSONB, nullable=True)


class SensorRawUltrasonic(Base):
    """초음파 센서 원시 데이터 테이블 ORM 모델"""
    __tablename__ = "sensor_raw_ultrasonic"
    
    time: Mapped[datetime] = Column(DateTime(timezone=True), primary_key=True)
    device_id: Mapped[str] = Column(String(64), ForeignKey("devices.device_id"), primary_key=True)
    distance_cm: Mapped[Optional[Numeric]] = Column(Numeric, nullable=True)
    raw_value: Mapped[Optional[int]] = Column(Integer, nullable=True)
    measurement_valid: Mapped[Optional[bool]] = Column(Boolean, nullable=True)
    raw_payload: Mapped[Optional[dict]] = Column(JSONB, nullable=True)


# 엣지 센서 테이블들
class SensorEdgeFlame(Base):
    """화염 엣지 센서 테이블 ORM 모델"""
    __tablename__ = "sensor_edge_flame"
    
    time: Mapped[datetime] = Column(DateTime(timezone=True), primary_key=True)
    device_id: Mapped[str] = Column(String(64), ForeignKey("devices.device_id"), primary_key=True)
    flame_detected: Mapped[bool] = Column(Boolean, nullable=False)
    confidence: Mapped[Optional[Numeric]] = Column(Numeric, nullable=True)
    alert_level: Mapped[Optional[str]] = Column(Text, nullable=True)
    processing_time: Mapped[Optional[Numeric]] = Column(Numeric, nullable=True)
    raw_payload: Mapped[Optional[dict]] = Column(JSONB, nullable=True)


class SensorEdgePIR(Base):
    """PIR 엣지 센서 테이블 ORM 모델"""
    __tablename__ = "sensor_edge_pir"
    
    time: Mapped[datetime] = Column(DateTime(timezone=True), primary_key=True)
    device_id: Mapped[str] = Column(String(64), ForeignKey("devices.device_id"), primary_key=True)
    motion_detected: Mapped[bool] = Column(Boolean, nullable=False)
    confidence: Mapped[Optional[Numeric]] = Column(Numeric, nullable=True)
    motion_direction: Mapped[Optional[str]] = Column(Text, nullable=True)
    motion_speed: Mapped[Optional[Numeric]] = Column(Numeric, nullable=True)
    processing_time: Mapped[Optional[Numeric]] = Column(Numeric, nullable=True)
    raw_payload: Mapped[Optional[dict]] = Column(JSONB, nullable=True)


class SensorEdgeReed(Base):
    """Reed 스위치 엣지 센서 테이블 ORM 모델"""
    __tablename__ = "sensor_edge_reed"
    
    time: Mapped[datetime] = Column(DateTime(timezone=True), primary_key=True)
    device_id: Mapped[str] = Column(String(64), ForeignKey("devices.device_id"), primary_key=True)
    switch_state: Mapped[bool] = Column(Boolean, nullable=False)
    confidence: Mapped[Optional[Numeric]] = Column(Numeric, nullable=True)
    magnetic_field_detected: Mapped[Optional[bool]] = Column(Boolean, nullable=True)
    magnetic_strength: Mapped[Optional[Numeric]] = Column(Numeric, nullable=True)
    processing_time: Mapped[Optional[Numeric]] = Column(Numeric, nullable=True)
    raw_payload: Mapped[Optional[dict]] = Column(JSONB, nullable=True)


class SensorEdgeTilt(Base):
    """틸트 센서 엣지 테이블 ORM 모델"""
    __tablename__ = "sensor_edge_tilt"
    
    time: Mapped[datetime] = Column(DateTime(timezone=True), primary_key=True)
    device_id: Mapped[str] = Column(String(64), ForeignKey("devices.device_id"), primary_key=True)
    tilt_detected: Mapped[bool] = Column(Boolean, nullable=False)
    confidence: Mapped[Optional[Numeric]] = Column(Numeric, nullable=True)
    tilt_angle: Mapped[Optional[Numeric]] = Column(Numeric, nullable=True)
    tilt_direction: Mapped[Optional[str]] = Column(Text, nullable=True)
    processing_time: Mapped[Optional[Numeric]] = Column(Numeric, nullable=True)
    raw_payload: Mapped[Optional[dict]] = Column(JSONB, nullable=True)


# 액추에이터 로그 테이블들
class ActuatorLogBuzzer(Base):
    """부저 액추에이터 로그 테이블 ORM 모델"""
    __tablename__ = "actuator_log_buzzer"
    
    time: Mapped[datetime] = Column(DateTime(timezone=True), primary_key=True)
    device_id: Mapped[str] = Column(String(64), ForeignKey("devices.device_id"), primary_key=True)
    buzzer_type: Mapped[str] = Column(Text, nullable=False)
    state: Mapped[str] = Column(Text, nullable=False)
    freq_hz: Mapped[Optional[int]] = Column(Integer, nullable=True)
    duration_ms: Mapped[Optional[int]] = Column(Integer, nullable=True)
    reason: Mapped[Optional[str]] = Column(Text, nullable=True)
    raw_payload: Mapped[Optional[dict]] = Column(JSONB, nullable=True)


class ActuatorLogIRTX(Base):
    """IR 송신 액추에이터 로그 테이블 ORM 모델"""
    __tablename__ = "actuator_log_ir_tx"
    
    time: Mapped[datetime] = Column(DateTime(timezone=True), primary_key=True)
    device_id: Mapped[str] = Column(String(64), ForeignKey("devices.device_id"), primary_key=True)
    protocol: Mapped[Optional[str]] = Column(Text, nullable=True)
    address_hex: Mapped[Optional[str]] = Column(Text, nullable=True)
    command_hex: Mapped[str] = Column(Text, nullable=False)
    repeat_cnt: Mapped[Optional[int]] = Column(Integer, nullable=True)
    raw_payload: Mapped[Optional[dict]] = Column(JSONB, nullable=True)


class ActuatorLogRelay(Base):
    """릴레이 액추에이터 로그 테이블 ORM 모델"""
    __tablename__ = "actuator_log_relay"
    
    time: Mapped[datetime] = Column(DateTime(timezone=True), primary_key=True)
    device_id: Mapped[str] = Column(String(64), ForeignKey("devices.device_id"), primary_key=True)
    channel: Mapped[int] = Column(SmallInteger, nullable=False, default=1)
    state: Mapped[str] = Column(Text, nullable=False)
    reason: Mapped[Optional[str]] = Column(Text, nullable=True)
    raw_payload: Mapped[Optional[dict]] = Column(JSONB, nullable=True)


class ActuatorLogServo(Base):
    """서보 액추에이터 로그 테이블 ORM 모델"""
    __tablename__ = "actuator_log_servo"
    
    time: Mapped[datetime] = Column(DateTime(timezone=True), primary_key=True)
    device_id: Mapped[str] = Column(String(64), ForeignKey("devices.device_id"), primary_key=True)
    channel: Mapped[int] = Column(SmallInteger, nullable=False, default=1)
    angle_deg: Mapped[Optional[Numeric]] = Column(Numeric, nullable=True)
    pwm_us: Mapped[Optional[int]] = Column(Integer, nullable=True)
    reason: Mapped[Optional[str]] = Column(Text, nullable=True)
    raw_payload: Mapped[Optional[dict]] = Column(JSONB, nullable=True)


# Alembic 버전 테이블
class AlembicVersion(Base):
    """Alembic 버전 테이블 ORM 모델"""
    __tablename__ = "alembic_version"
    
    version_num: Mapped[str] = Column(String, primary_key=True)


# 모든 모델을 리스트로 관리
__all__ = [
    "Base",
    "User",
    "Device", 
    "DeviceRTCStatus",
    "SensorRawCDS",
    "SensorRawDHT",
    "SensorRawFlame",
    "SensorRawIMU",
    "SensorRawLoadCell",
    "SensorRawMQ5",
    "SensorRawMQ7",
    "SensorRawRFID",
    "SensorRawSound",
    "SensorRawTCRT5000",
    "SensorRawUltrasonic",
    "SensorEdgeFlame",
    "SensorEdgePIR",
    "SensorEdgeReed",
    "SensorEdgeTilt",
    "ActuatorLogBuzzer",
    "ActuatorLogIRTX",
    "ActuatorLogRelay",
    "ActuatorLogServo",
    "AlembicVersion"
] 