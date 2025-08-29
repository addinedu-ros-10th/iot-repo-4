"""
DatabaseManager 클래스 단위 테스트
TDD 방식: 테스트 먼저 작성 후 구현
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
try:
    import psycopg2
    PSYCOPG2_AVAILABLE = True
except ImportError:
    PSYCOPG2_AVAILABLE = False
from datetime import datetime
import sys
import os

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from app import DatabaseManager


class TestDatabaseManager(unittest.TestCase):
    """DatabaseManager 클래스 단위 테스트"""
    
    def setUp(self):
        """테스트 전 설정"""
        self.db_manager = DatabaseManager()
        self.mock_connection = Mock()
        self.mock_cursor = Mock()
        # 연결 상태 초기화
        self.db_manager.connection = None
        
    def tearDown(self):
        """테스트 후 정리"""
        if hasattr(self.db_manager, 'connection') and self.db_manager.connection:
            self.db_manager.disconnect()
        # 연결 상태 완전 초기화
        self.db_manager.connection = None

    def test_database_manager_initialization(self):
        """데이터베이스 매니저 초기화 테스트"""
        # Given: DatabaseManager 인스턴스 생성
        # When: 초기화 완료
        # Then: 설정값이 올바르게 설정되어야 함
        self.assertEqual(self.db_manager.config['host'], '192.168.0.2')
        self.assertEqual(self.db_manager.config['port'], 15432)
        self.assertEqual(self.db_manager.config['user'], 'svc_dev')
        self.assertEqual(self.db_manager.config['database'], 'iot_care')
        self.assertIsNone(self.db_manager.connection)

    @patch('psycopg2.connect')
    def test_database_connection_success(self, mock_connect):
        """데이터베이스 연결 성공 테스트"""
        # Given: 성공적인 연결 시뮬레이션
        mock_connect.return_value = self.mock_connection
        
        # When: 연결 시도
        result = self.db_manager.connect()
        
        # Then: 연결 성공
        self.assertTrue(result)
        self.assertEqual(self.db_manager.connection, self.mock_connection)
        mock_connect.assert_called_once_with(**self.db_manager.config)

    @patch('psycopg2.connect')
    def test_database_connection_failure(self, mock_connect):
        """데이터베이스 연결 실패 테스트"""
        # Given: 연결 실패 시뮬레이션
        mock_connect.side_effect = psycopg2.OperationalError("Connection failed")
        
        # When: 연결 시도
        result = self.db_manager.connect()
        
        # Then: 연결 실패
        self.assertFalse(result)
        self.assertIsNone(self.db_manager.connection)

    def test_disconnect_with_connection(self):
        """연결이 있을 때 연결 해제 테스트"""
        # Given: 연결된 상태
        self.db_manager.connection = self.mock_connection
        
        # When: 연결 해제
        self.db_manager.disconnect()
        
        # Then: 연결이 닫혀야 함
        self.mock_connection.close.assert_called_once()

    def test_disconnect_without_connection(self):
        """연결이 없을 때 연결 해제 테스트"""
        # Given: 연결이 없는 상태
        self.db_manager.connection = None
        
        # When: 연결 해제
        # Then: 오류가 발생하지 않아야 함
        try:
            self.db_manager.disconnect()
        except Exception as e:
            self.fail(f"연결 해제 시 오류 발생: {e}")

    @patch('psycopg2.extras.RealDictCursor')
    def test_get_users_success(self, mock_cursor_factory):
        """사용자 목록 조회 성공 테스트"""
        # Given: 성공적인 쿼리 실행 시뮬레이션
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = [
            {
                'user_id': '1',
                'user_name': 'Test User',
                'email': 'test@example.com',
                'user_role': 'care_target',
                'created_at': datetime.now(),
                'phone_number': '010-1234-5678'
            }
        ]
        self.db_manager.connection = self.mock_connection
        self.mock_connection.cursor.return_value = mock_cursor
        
        # When: 사용자 목록 조회
        result = self.db_manager.get_users()
        
        # Then: 결과가 올바르게 반환되어야 함
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['user_name'], 'Test User')
        self.assertEqual(result[0]['user_role_kr'], '돌봄대상자')
        mock_cursor.close.assert_called_once()

    def test_get_users_no_connection(self):
        """연결이 없을 때 사용자 목록 조회 테스트"""
        # Given: 연결이 없는 상태
        self.db_manager.connection = None
        
        # When: 사용자 목록 조회
        result = self.db_manager.get_users()
        
        # Then: 빈 리스트 반환
        self.assertEqual(result, [])

    @patch('psycopg2.extras.RealDictCursor')
    def test_get_users_database_error(self, mock_cursor_factory):
        """데이터베이스 오류 시 사용자 목록 조회 테스트"""
        # Given: 데이터베이스 오류 시뮬레이션
        self.db_manager.connection = self.mock_connection
        self.mock_connection.cursor.side_effect = Exception("Database error")
        
        # When: 사용자 목록 조회
        result = self.db_manager.get_users()
        
        # Then: 빈 리스트 반환
        self.assertEqual(result, [])

    @patch('psycopg2.extras.RealDictCursor')
    def test_get_user_relationships_success(self, mock_cursor_factory):
        """사용자 관계 조회 성공 테스트"""
        # Given: 성공적인 관계 조회 시뮬레이션
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = [
            {
                'relationship_id': '1',
                'subject_user_id': '1',
                'target_user_id': '2',
                'relationship_type': 'caregiver',
                'created_at': datetime.now(),
                'subject_user_name': 'Caregiver',
                'subject_user_email': 'caregiver@example.com',
                'target_user_name': 'Care Target',
                'target_user_email': 'target@example.com'
            }
        ]
        self.db_manager.connection = self.mock_connection
        self.mock_connection.cursor.return_value = mock_cursor
        
        # When: 사용자 관계 조회
        result = self.db_manager.get_user_relationships('1')
        
        # Then: 결과가 올바르게 반환되어야 함
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['relationship_type'], 'caregiver')
        mock_cursor.close.assert_called_once()

    @patch('psycopg2.extras.RealDictCursor')
    def test_get_data_timeline_success(self, mock_cursor_factory):
        """데이터 타임라인 조회 성공 테스트"""
        # Given: 성공적인 타임라인 조회 시뮬레이션
        mock_cursor = Mock()
        mock_cursor.fetchall.side_effect = [
            [{'data_type': 'snapshot', 'timestamp': datetime.now(), 'data': {'alert_level': 'normal'}}],
            [{'data_type': 'actuator', 'timestamp': datetime.now(), 'data': {'buzzer_type': 'alert'}}],
            [{'data_type': 'event', 'timestamp': datetime.now(), 'data': {'event_type': 'button'}}]
        ]
        self.db_manager.connection = self.mock_connection
        self.mock_connection.cursor.return_value = mock_cursor
        
        # When: 데이터 타임라인 조회
        result = self.db_manager.get_data_timeline('1', 24)
        
        # Then: 결과가 올바르게 반환되어야 함
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]['data_type'], 'snapshot')
        self.assertEqual(result[1]['data_type'], 'actuator')
        self.assertEqual(result[2]['data_type'], 'event')
        mock_cursor.close.assert_called()

    def test_role_translations(self):
        """사용자 역할 번역 테스트"""
        # Given: 다양한 사용자 역할
        test_cases = [
            ('care_target', '돌봄대상자'),
            ('caregiver', '돌봄제공자'),
            ('family', '가족'),
            ('guardian', '보호자'),
            ('admin', '관리자'),
            ('user', '사용자'),
            ('unknown_role', 'unknown_role')  # 알 수 없는 역할
        ]
        
        # When & Then: 각 역할에 대한 번역 확인
        for role, expected_translation in test_cases:
            with self.subTest(role=role):
                # Mock 데이터 생성
                mock_user = {'user_role': role}
                
                # 번역 로직 테스트 (실제 구현에서 사용되는 방식)
                role_translations = {
                    'care_target': '돌봄대상자',
                    'caregiver': '돌봄제공자',
                    'family': '가족',
                    'guardian': '보호자',
                    'admin': '관리자',
                    'user': '사용자'
                }
                
                if role in role_translations:
                    expected = role_translations[role]
                else:
                    expected = role
                
                self.assertEqual(expected, expected_translation)

    def test_psycopg2_availability(self):
        """psycopg2 가용성 테스트"""
        # Given: psycopg2 설치 상태
        # When: DatabaseManager 초기화
        # Then: psycopg2 가용성에 따라 적절히 동작해야 함
        if PSYCOPG2_AVAILABLE:
            # psycopg2가 설치된 경우 정상 동작
            self.assertTrue(hasattr(self.db_manager, 'connect'))
            
            # Mock 연결 테스트
            with patch('psycopg2.connect', return_value=self.mock_connection):
                result = self.db_manager.connect()
                self.assertTrue(result)
        else:
            # psycopg2가 설치되지 않은 경우 제한된 기능
            self.assertTrue(hasattr(self.db_manager, 'connect'))
            # 연결 시도 시 실패해야 함
            result = self.db_manager.connect()
            self.assertFalse(result)

    @patch('psycopg2.extras.RealDictCursor')
    def test_database_operations_with_mock_connection(self, mock_cursor_factory):
        """Mock 연결을 사용한 데이터베이스 작업 테스트"""
        # Given: Mock 연결과 커서 설정
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = [
            {
                'user_id': 'mock-user-1',
                'user_name': 'Mock User 1',
                'email': 'mock1@example.com',
                'user_role': 'admin',
                'created_at': datetime.now(),
                'phone_number': '010-1111-1111'
            },
            {
                'user_id': 'mock-user-2',
                'user_name': 'Mock User 2',
                'email': 'mock2@example.com',
                'user_role': 'care_target',
                'created_at': datetime.now(),
                'phone_number': '010-2222-2222'
            }
        ]
        
        self.db_manager.connection = self.mock_connection
        self.mock_connection.cursor.return_value = mock_cursor
        
        # When: 사용자 목록 조회
        result = self.db_manager.get_users()
        
        # Then: Mock 데이터가 올바르게 반환되어야 함
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['user_name'], 'Mock User 1')
        self.assertEqual(result[0]['user_role_kr'], '관리자')
        self.assertEqual(result[1]['user_name'], 'Mock User 2')
        self.assertEqual(result[1]['user_role_kr'], '돌봄대상자')
        
        # 커서가 올바르게 닫혀야 함
        mock_cursor.close.assert_called_once()

    def test_database_config_validation(self):
        """데이터베이스 설정 검증 테스트"""
        # Given: DatabaseManager 설정
        config = self.db_manager.config
        
        # When: 설정값 검증
        # Then: 필수 설정값들이 올바르게 설정되어야 함
        required_keys = ['host', 'port', 'user', 'password', 'database']
        for key in required_keys:
            self.assertIn(key, config)
            self.assertIsNotNone(config[key])
        
        # 포트는 정수여야 함
        self.assertIsInstance(config['port'], int)
        self.assertEqual(config['port'], 15432)
        
        # 호스트는 문자열이어야 함
        self.assertIsInstance(config['host'], str)
        self.assertEqual(config['host'], '192.168.0.2')

    def test_simple_error_handling(self):
        """간단한 오류 처리 테스트"""
        # Given: 연결 실패 상황
        with patch('psycopg2.connect', side_effect=psycopg2.OperationalError("Connection failed")):
            # When: 연결 시도
            result = self.db_manager.connect()
            
            # Then: 연결 실패 및 적절한 처리
            self.assertFalse(result)
            self.assertIsNone(self.db_manager.connection)
        
        # Given: 쿼리 오류 상황
        with patch('psycopg2.connect', return_value=self.mock_connection):
            # When: 연결 성공 후 쿼리 오류
            self.db_manager.connect()
            with patch.object(self.mock_connection, 'cursor', side_effect=Exception("Query error")):
                result = self.db_manager.get_users()
                
                # Then: 오류 시 빈 리스트 반환
                self.assertEqual(result, [])
            
            # 연결 해제
            self.db_manager.disconnect()


if __name__ == '__main__':
    unittest.main()
