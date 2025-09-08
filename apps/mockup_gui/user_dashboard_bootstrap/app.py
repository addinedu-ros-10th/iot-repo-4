#!/usr/bin/env python3
"""
IoT Care Bootstrap Dashboard - Flask 백엔드
현대적이고 세련된 Bootstrap 기반 사용자 대시보드
"""

from flask import Flask, render_template, jsonify, request
try:
    import psycopg2
    import psycopg2.extras
    PSYCOPG2_AVAILABLE = True
except ImportError:
    PSYCOPG2_AVAILABLE = False
    print("⚠️ psycopg2가 설치되지 않았습니다. 데이터베이스 기능이 제한됩니다.")

from datetime import datetime, timedelta
import json
from typing import List, Dict, Any, Optional
import os

app = Flask(__name__)

class DatabaseManager:
    """데이터베이스 연결 및 쿼리 관리"""
    
    def __init__(self):
        self.config = {
            'host': '192.168.0.26',
            'port': 15432,
            'user': 'svc_dev',
            'password': 'IOT_dev_123!@#',
            'database': 'iot_care'
        }
        self.connection = None
    
    def connect(self) -> bool:
        """데이터베이스 연결"""
        if not PSYCOPG2_AVAILABLE:
            print("❌ psycopg2가 설치되지 않아 데이터베이스 연결이 불가능합니다.")
            return False
            
        try:
            self.connection = psycopg2.connect(**self.config)
            return True
        except Exception as e:
            print(f"❌ 데이터베이스 연결 실패: {e}")
            return False
    
    def disconnect(self):
        """데이터베이스 연결 해제"""
        if self.connection:
            self.connection.close()
    
    def get_users(self) -> List[Dict[str, Any]]:
        """사용자 목록 조회"""
        if not PSYCOPG2_AVAILABLE:
            return []
            
        try:
            cursor = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cursor.execute("""
                SELECT u.user_id, u.user_name, u.email, u.user_role, u.created_at,
                       u.phone_number, u.phone_number as address, 
                       '1990-01-01'::date as birth_date, 'unknown' as gender
                FROM users u
                ORDER BY u.created_at DESC
                LIMIT 100
            """)
            users = cursor.fetchall()
            cursor.close()
            
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
            
            return [dict(user) for user in users]
        except Exception as e:
            print(f"❌ 사용자 조회 실패: {e}")
            return []
    
    def get_user_relationships(self, user_id: str) -> List[Dict[str, Any]]:
        """사용자 관계 조회"""
        if not PSYCOPG2_AVAILABLE:
            return []
            
        try:
            cursor = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
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
            
            # 컬럼명을 기존 코드와 호환되도록 변환
            converted_relationships = []
            for rel in relationships:
                if rel['subject_user_id'] == user_id:
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
            
            return converted_relationships
            
        except Exception as e:
            print(f"❌ 사용자 관계 조회 실패: {e}")
            return []
    
    def get_data_timeline(self, user_id: str, hours: int = 24) -> List[Dict[str, Any]]:
        """통합 데이터 타임라인 조회"""
        if not PSYCOPG2_AVAILABLE:
            return []
            
        try:
            cursor = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            # 홈 상태 스냅샷
            cursor.execute("""
                SELECT 'snapshot' as data_type, time as timestamp, 
                       json_build_object('alert_level', alert_level, 'detected_activity', detected_activity) as data
                FROM home_state_snapshots
                WHERE time >= NOW() - INTERVAL '%s hours'
                ORDER BY time ASC
                LIMIT 20
            """, (hours,))
            snapshots = cursor.fetchall()
            
            # 액추에이터 로그
            cursor.execute("""
                SELECT 'actuator' as data_type, time as timestamp,
                       json_build_object('buzzer_type', buzzer_type, 'state', state, 'reason', reason) as data
                FROM actuator_log_buzzer
                WHERE time >= NOW() - INTERVAL '%s hours'
                ORDER BY time ASC
                LIMIT 20
            """, (hours,))
            actuators = cursor.fetchall()
            
            # 센서 이벤트
            cursor.execute("""
                SELECT 'event' as data_type, time as timestamp,
                       json_build_object('event_type', event_type, 'button_state', button_state) as data
                FROM sensor_event_button
                WHERE time >= NOW() - INTERVAL '%s hours'
                ORDER BY time ASC
                LIMIT 20
            """, (hours,))
            events = cursor.fetchall()
            
            cursor.close()
            
            # 모든 데이터를 시간순으로 정렬
            all_data = []
            for item in snapshots + actuators + events:
                timestamp = item.get('timestamp')
                if timestamp and not isinstance(timestamp, datetime):
                    try:
                        if isinstance(timestamp, str):
                            timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                        else:
                            timestamp = datetime.now()
                    except Exception:
                        timestamp = datetime.now()
                
                converted_item = dict(item)
                converted_item['timestamp'] = timestamp
                all_data.append(converted_item)
            
            # 시간순 정렬
            all_data.sort(key=lambda x: x['timestamp'])
            return all_data
            
        except Exception as e:
            print(f"❌ 데이터 타임라인 조회 실패: {e}")
            return []

# 전역 데이터베이스 매니저
db_manager = DatabaseManager()

@app.route('/')
def index():
    """메인 대시보드 페이지"""
    return render_template('index.html')

@app.route('/api/users')
def get_users():
    """사용자 목록 API"""
    try:
        if db_manager.connect():
            users = db_manager.get_users()
            db_manager.disconnect()
            return jsonify({'success': True, 'data': users})
        else:
            return jsonify({'success': False, 'error': '데이터베이스 연결 실패'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/users/<user_id>/relationships')
def get_user_relationships(user_id):
    """사용자 관계 API"""
    try:
        if db_manager.connect():
            relationships = db_manager.get_user_relationships(user_id)
            db_manager.disconnect()
            return jsonify({'success': True, 'data': relationships})
        else:
            return jsonify({'success': False, 'error': '데이터베이스 연결 실패'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/users/<user_id>/timeline')
def get_user_timeline(user_id):
    """사용자 데이터 타임라인 API"""
    try:
        hours = request.args.get('hours', 24, type=int)
        if db_manager.connect():
            timeline = db_manager.get_data_timeline(user_id, hours)
            db_manager.disconnect()
            return jsonify({'success': True, 'data': timeline})
        else:
            return jsonify({'success': False, 'error': '데이터베이스 연결 실패'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/dashboard/stats')
def get_dashboard_stats():
    """대시보드 통계 API"""
    try:
        if db_manager.connect():
            # 간단한 통계 데이터
            stats = {
                'total_users': 275,
                'active_devices': 8,
                'today_alerts': 3,
                'crisis_situations': 0
            }
            db_manager.disconnect()
            return jsonify({'success': True, 'data': stats})
        else:
            return jsonify({'success': False, 'error': '데이터베이스 연결 실패'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    print("🚀 IoT Care Bootstrap Dashboard 시작 중...")
    print("📱 브라우저에서 http://localhost:5001 으로 접속하세요")
    app.run(debug=True, host='0.0.0.0', port=5001)

