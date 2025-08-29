#!/usr/bin/env python3
"""
데이터베이스 연결 및 쿼리 모듈
"""

import psycopg2
import psycopg2.extras
from datetime import datetime, timedelta
import json
from typing import List, Dict, Any, Optional

class DatabaseManager:
    def __init__(self):
        # .env.local 파일의 설정을 사용
        self.config = {
            'host': '192.168.0.2',
            'port': 15432,
            'user': 'svc_dev',
            'password': 'IOT_dev_123!@#',
            'database': 'iot_care'
        }
        self.connection = None
    
    def connect(self) -> bool:
        """데이터베이스 연결"""
        try:
            self.connection = psycopg2.connect(**self.config)
            print("✅ 데이터베이스 연결 성공")
            return True
        except Exception as e:
            print(f"❌ 데이터베이스 연결 실패: {e}")
            return False
    
    def disconnect(self):
        """데이터베이스 연결 해제"""
        if self.connection:
            self.connection.close()
            print("🔌 데이터베이스 연결 해제")
    
    def get_users(self) -> List[Dict[str, Any]]:
        """사용자 목록 조회 (모든 사용자)"""
        try:
            cursor = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cursor.execute("""
                SELECT u.user_id, u.user_name, u.email, u.user_role, u.created_at,
                       u.phone_number, u.phone_number as address, 
                       '1990-01-01'::date as birth_date, 'unknown' as gender
                FROM users u
                ORDER BY u.created_at DESC
            """)
            users = cursor.fetchall()
            cursor.close()
            
            print(f"📋 사용자 조회 완료: {len(users)}명")
            
            # user_role 한국어 번역
            role_translations = {
                'care_target': '돌봄대상자',
                'caregiver': '돌봄제공자',
                'family': '가족',
                'guardian': '보호자',
                'admin': '관리자',
                'user': '사용자'
            }
            
            for user in users:
                user_role = user.get('user_role', '')
                if user_role in role_translations:
                    user['user_role_kr'] = role_translations[user_role]
                else:
                    user['user_role_kr'] = user_role
                
                print(f"  - {user.get('user_name', 'Unknown')}: {user.get('user_role', 'Unknown')} -> {user.get('user_role_kr', 'Unknown')}")
            
            return [dict(user) for user in users]
        except Exception as e:
            print(f"❌ 사용자 조회 실패: {e}")
            return []
    
    def get_user_relationships(self, user_id: str) -> List[Dict[str, Any]]:
        """사용자 관계 조회"""
        try:
            cursor = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            # 먼저 user_relationships 테이블의 구조 확인
            cursor.execute("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'user_relationships'
                ORDER BY ordinal_position
            """)
            columns = cursor.fetchall()
            print(f"📋 user_relationships 테이블 컬럼: {[col['column_name'] for col in columns]}")
            
            # 특정 사용자의 관계 데이터 조회 (subject_user_id 또는 target_user_id가 해당 사용자인 경우)
            cursor.execute("""
                SELECT ur.relationship_id, ur.subject_user_id, ur.target_user_id, ur.relationship_type,
                       ur.created_at, 
                       u1.user_name as subject_user_name, u1.email as subject_user_email,
                       u2.user_name as target_user_name, u2.email as target_user_email
                FROM user_relationships ur
                JOIN users u1 ON ur.subject_user_id = u1.user_id
                JOIN users u2 ON ur.target_user_id = u2.user_id
                WHERE ur.subject_user_id = %s OR ur.target_user_id = %s
                ORDER BY ur.created_at DESC
                LIMIT 20
            """, (user_id, user_id))
            relationships = cursor.fetchall()
            cursor.close()
            
            print(f"📊 사용자 {user_id}의 관계 조회 완료: {len(relationships)}개")
            
            # 컬럼명을 기존 코드와 호환되도록 변환
            converted_relationships = []
            for rel in relationships:
                # 현재 사용자가 subject인지 target인지 확인
                if rel['subject_user_id'] == user_id:
                    # 현재 사용자가 주체인 경우
                    converted_rel = {
                        'relationship_id': rel['relationship_id'],
                        'user_id': rel['subject_user_id'],
                        'related_user_id': rel['target_user_id'],
                        'relationship_type': rel['relationship_type'],
                        'created_at': rel['created_at'],
                        'user_name': rel['subject_user_name'],
                        'email': rel['subject_user_email'],
                        'related_user_name': rel['target_user_name'],
                        'related_user_email': rel['target_user_email']
                    }
                else:
                    # 현재 사용자가 대상인 경우 (역방향 관계)
                    converted_rel = {
                        'relationship_id': rel['relationship_id'],
                        'user_id': rel['target_user_id'],
                        'related_user_id': rel['subject_user_id'],
                        'relationship_type': f"{rel['relationship_type']}_reverse",
                        'created_at': rel['created_at'],
                        'user_name': rel['target_user_name'],
                        'email': rel['target_user_email'],
                        'related_user_name': rel['subject_user_name'],
                        'related_user_email': rel['subject_user_email']
                    }
                
                converted_relationships.append(converted_rel)
                print(f"  - 관계: {converted_rel['user_id']} -> {converted_rel['related_user_id']} ({converted_rel['relationship_type']})")
            
            return converted_relationships
            
        except Exception as e:
            print(f"❌ 사용자 관계 조회 실패: {e}")
            return []
    
    def get_home_state_snapshots(self, user_id: str, hours: int = 24) -> List[Dict[str, Any]]:
        """홈 상태 스냅샷 조회 (시간 범위별)"""
        try:
            cursor = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cursor.execute("""
                SELECT hss.*, d.device_name, d.device_type
                FROM home_state_snapshots hss
                JOIN devices d ON hss.device_id = d.device_id
                WHERE hss.user_id = %s
                AND hss.timestamp >= NOW() - INTERVAL '%s hours'
                ORDER BY hss.timestamp ASC
            """, (user_id, hours))
            snapshots = cursor.fetchall()
            cursor.close()
            return [dict(snap) for snap in snapshots]
        except Exception as e:
            print(f"❌ 홈 상태 스냅샷 조회 실패: {e}")
            return []
    
    def get_actuator_logs(self, user_id: str, hours: int = 24) -> List[Dict[str, Any]]:
        """액추에이터 로그 조회"""
        try:
            cursor = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cursor.execute("""
                SELECT al.*, d.device_name
                FROM actuator_log_buzzer al
                JOIN devices d ON al.device_id = d.device_id
                WHERE al.user_id = %s
                AND al.timestamp >= NOW() - INTERVAL '%s hours'
                ORDER BY al.timestamp ASC
            """, (user_id, hours))
            logs = cursor.fetchall()
            cursor.close()
            return [dict(log) for log in logs]
        except Exception as e:
            print(f"❌ 액추에이터 로그 조회 실패: {e}")
            return []
    
    def get_sensor_events(self, user_id: str, hours: int = 24) -> List[Dict[str, Any]]:
        """센서 이벤트 조회"""
        try:
            cursor = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cursor.execute("""
                SELECT se.*, d.device_name
                FROM sensor_event_button se
                JOIN devices d ON se.device_id = d.device_id
                WHERE se.user_id = %s
                AND se.timestamp >= NOW() - INTERVAL '%s hours'
                ORDER BY se.timestamp ASC
            """, (user_id, hours))
            events = cursor.fetchall()
            cursor.close()
            return [dict(event) for event in events]
        except Exception as e:
            print(f"❌ 센서 이벤트 조회 실패: {e}")
            return []
    
    def get_devices(self, user_id: str) -> List[Dict[str, Any]]:
        """사용자별 디바이스 조회"""
        try:
            cursor = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cursor.execute("""
                SELECT device_id, device_name, device_type, location, status, created_at
                FROM devices
                WHERE user_id = %s
                ORDER BY created_at DESC
            """, (user_id,))
            devices = cursor.fetchall()
            cursor.close()
            return [dict(device) for device in devices]
        except Exception as e:
            print(f"❌ 디바이스 조회 실패: {e}")
            return []
    
    def get_data_timeline(self, user_id: str, hours: int = 24) -> List[Dict[str, Any]]:
        """통합 데이터 타임라인 조회 (시뮬레이션용)"""
        try:
            cursor = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            # 먼저 테이블 구조 확인
            cursor.execute("""
                SELECT table_name, column_name 
                FROM information_schema.columns 
                WHERE table_name IN ('home_state_snapshots', 'actuator_log_buzzer', 'sensor_event_button')
                ORDER BY table_name, ordinal_position
            """)
            columns = cursor.fetchall()
            print(f"📋 테이블 컬럼 정보: {[f'{col['table_name']}.{col['column_name']}' for col in columns]}")
            
            # 홈 상태 스냅샷 (time 컬럼 사용, user_id 컬럼 확인)
            try:
                cursor.execute("""
                    SELECT 'snapshot' as data_type, time as timestamp, 
                           json_build_object('alert_level', alert_level, 'detected_activity', detected_activity) as data
                    FROM home_state_snapshots
                    WHERE time >= NOW() - INTERVAL '%s hours'
                    ORDER BY time ASC
                    LIMIT 10
                """, (hours,))
                snapshots = cursor.fetchall()
                print(f"📊 홈 상태 스냅샷: {len(snapshots)}개")
                
                # 데이터 형식 검증
                for i, snap in enumerate(snapshots[:2]):
                    print(f"  📋 스냅샷 {i+1}: {snap.get('timestamp', 'no_timestamp')} - {snap.get('data', {})}")
                    
            except Exception as e:
                print(f"⚠️ 홈 상태 스냅샷 조회 실패: {e}")
                snapshots = []
            
            # 액추에이터 로그 (time 컬럼 사용)
            try:
                cursor.execute("""
                    SELECT 'actuator' as data_type, time as timestamp,
                           json_build_object('buzzer_type', buzzer_type, 'state', state, 'reason', reason) as data
                    FROM actuator_log_buzzer
                    WHERE time >= NOW() - INTERVAL '%s hours'
                    ORDER BY time ASC
                    LIMIT 10
                """, (hours,))
                actuators = cursor.fetchall()
                print(f"📊 액추에이터 로그: {len(actuators)}개")
                
                # 데이터 형식 검증
                for i, act in enumerate(actuators[:2]):
                    print(f"  📋 액추에이터 {i+1}: {act.get('timestamp', 'no_timestamp')} - {act.get('data', {})}")
                    
            except Exception as e:
                print(f"⚠️ 액추에이터 로그 조회 실패: {e}")
                actuators = []
            
            # 센서 이벤트 (time 컬럼 사용)
            try:
                cursor.execute("""
                    SELECT 'event' as data_type, time as timestamp,
                           json_build_object('event_type', event_type, 'button_state', button_state) as data
                    FROM sensor_event_button
                    WHERE time >= NOW() - INTERVAL '%s hours'
                    ORDER BY time ASC
                    LIMIT 10
                """, (hours,))
                events = cursor.fetchall()
                print(f"📊 센서 이벤트: {len(events)}개")
                
                # 데이터 형식 검증
                for i, event in enumerate(events[:2]):
                    print(f"  📋 이벤트 {i+1}: {event.get('timestamp', 'no_timestamp')} - {event.get('data', {})}")
                    
            except Exception as e:
                print(f"⚠️ 센서 이벤트 조회 실패: {e}")
                events = []
            
            cursor.close()
            
            # 모든 데이터를 시간순으로 정렬
            all_data = []
            for item in snapshots + actuators + events:
                # timestamp가 datetime 객체인지 확인하고 변환
                timestamp = item.get('timestamp')
                if timestamp and not isinstance(timestamp, datetime):
                    try:
                        if isinstance(timestamp, str):
                            timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                        else:
                            timestamp = datetime.now()  # 기본값
                    except Exception as e:
                        print(f"⚠️ timestamp 변환 실패: {timestamp} -> {e}")
                        timestamp = datetime.now()  # 기본값
                
                # 변환된 데이터 추가
                converted_item = dict(item)
                converted_item['timestamp'] = timestamp
                all_data.append(converted_item)
            
            # 시간순 정렬
            all_data.sort(key=lambda x: x['timestamp'])
            print(f"✅ 데이터 타임라인 조회 완료: {len(all_data)}개 포인트")
            
            # 최종 데이터 형식 검증
            if all_data:
                print(f"  📅 시간 범위: {all_data[0]['timestamp']} ~ {all_data[-1]['timestamp']}")
                print(f"  🔍 데이터 타입 분포: {[item['data_type'] for item in all_data]}")
            
            return all_data
            
        except Exception as e:
            print(f"❌ 데이터 타임라인 조회 실패: {e}")
            return []
    
    def test_connection(self) -> bool:
        """데이터베이스 연결 테스트"""
        if not self.connect():
            return False
        
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            cursor.close()
            print(f"✅ PostgreSQL 버전: {version[0]}")
            return True
        except Exception as e:
            print(f"❌ 연결 테스트 실패: {e}")
            return False
        finally:
            self.disconnect()

if __name__ == "__main__":
    # 연결 테스트
    db = DatabaseManager()
    db.test_connection()
