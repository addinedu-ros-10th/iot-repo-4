"""
Flask API 엔드포인트 단위 테스트
TDD 방식: 테스트 먼저 작성 후 구현
"""

import unittest
import json
import sys
import os
from unittest.mock import Mock, patch, MagicMock

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from app import app, db_manager


class TestAPIEndpoints(unittest.TestCase):
    """Flask API 엔드포인트 단위 테스트"""
    
    def setUp(self):
        """테스트 전 설정"""
        self.app = app.test_client()
        self.app.testing = True
        
    def tearDown(self):
        """테스트 후 정리"""
        pass

    def test_root_endpoint(self):
        """루트 엔드포인트 테스트"""
        # Given: 루트 경로 요청
        # When: GET / 요청
        response = self.app.get('/')
        
        # Then: 200 상태 코드와 HTML 응답
        self.assertEqual(response.status_code, 200)
        self.assertIn('text/html', response.content_type)
        self.assertIn('IoT Care Dashboard', response.data.decode('utf-8'))

    @patch('app.db_manager.connect')
    @patch('app.db_manager.get_users')
    @patch('app.db_manager.disconnect')
    def test_get_users_api_success(self, mock_disconnect, mock_get_users, mock_connect):
        """사용자 목록 API 성공 테스트"""
        # Given: 성공적인 데이터베이스 연결 및 사용자 데이터
        mock_connect.return_value = True
        mock_get_users.return_value = [
            {
                'user_id': '1',
                'user_name': 'Test User',
                'email': 'test@example.com',
                'user_role': 'care_target',
                'user_role_kr': '돌봄대상자'
            }
        ]
        
        # When: GET /api/users 요청
        response = self.app.get('/api/users')
        
        # Then: 성공 응답과 사용자 데이터
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(data['data'][0]['user_name'], 'Test User')
        
        # 데이터베이스 연결/해제 확인
        mock_connect.assert_called_once()
        mock_disconnect.assert_called_once()

    @patch('app.db_manager.connect')
    def test_get_users_api_connection_failure(self, mock_connect):
        """사용자 목록 API 연결 실패 테스트"""
        # Given: 데이터베이스 연결 실패
        mock_connect.return_value = False
        
        # When: GET /api/users 요청
        response = self.app.get('/api/users')
        
        # Then: 실패 응답
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], '데이터베이스 연결 실패')

    @patch('app.db_manager.connect')
    @patch('app.db_manager.get_user_relationships')
    @patch('app.db_manager.disconnect')
    def test_get_user_relationships_api_success(self, mock_disconnect, mock_get_relationships, mock_connect):
        """사용자 관계 API 성공 테스트"""
        # Given: 성공적인 관계 데이터 조회
        mock_connect.return_value = True
        mock_get_relationships.return_value = [
            {
                'relationship_id': '1',
                'user_id': '1',
                'related_user_id': '2',
                'relationship_type': 'caregiver'
            }
        ]
        
        # When: GET /api/users/1/relationships 요청
        response = self.app.get('/api/users/1/relationships')
        
        # Then: 성공 응답과 관계 데이터
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(data['data'][0]['relationship_type'], 'caregiver')

    @patch('app.db_manager.connect')
    @patch('app.db_manager.get_data_timeline')
    @patch('app.db_manager.disconnect')
    def test_get_user_timeline_api_success(self, mock_disconnect, mock_get_timeline, mock_connect):
        """사용자 타임라인 API 성공 테스트"""
        # Given: 성공적인 타임라인 데이터 조회
        mock_connect.return_value = True
        mock_get_timeline.return_value = [
            {
                'data_type': 'snapshot',
                'timestamp': '2025-08-25T10:00:00',
                'data': {'alert_level': 'normal'}
            }
        ]
        
        # When: GET /api/users/1/timeline?hours=24 요청
        response = self.app.get('/api/users/1/timeline?hours=24')
        
        # Then: 성공 응답과 타임라인 데이터
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(data['data'][0]['data_type'], 'snapshot')

    def test_get_user_timeline_api_invalid_hours(self):
        """사용자 타임라인 API 잘못된 시간 파라미터 테스트"""
        # Given: 잘못된 시간 파라미터
        # When: GET /api/users/1/timeline?hours=invalid 요청
        response = self.app.get('/api/users/1/timeline?hours=invalid')
        
        # Then: 기본값 24시간으로 처리되어야 함
        self.assertEqual(response.status_code, 200)

    @patch('app.db_manager.connect')
    @patch('app.db_manager.disconnect')
    def test_get_dashboard_stats_api_success(self, mock_disconnect, mock_connect):
        """대시보드 통계 API 성공 테스트"""
        # Given: 성공적인 데이터베이스 연결
        mock_connect.return_value = True
        
        # When: GET /api/dashboard/stats 요청
        response = self.app.get('/api/dashboard/stats')
        
        # Then: 성공 응답과 통계 데이터
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('total_users', data['data'])
        self.assertIn('active_devices', data['data'])
        self.assertIn('today_alerts', data['data'])
        self.assertIn('crisis_situations', data['data'])

    def test_api_endpoints_content_type(self):
        """API 엔드포인트 응답 타입 테스트"""
        # Given: API 엔드포인트들
        endpoints = [
            '/api/users',
            '/api/dashboard/stats'
        ]
        
        # When & Then: 각 엔드포인트가 JSON 응답을 반환해야 함
        for endpoint in endpoints:
            with self.subTest(endpoint=endpoint):
                response = self.app.get(endpoint)
                self.assertEqual(response.content_type, 'application/json')

    def test_api_error_handling(self):
        """API 오류 처리 테스트"""
        # Given: 예외가 발생하는 상황
        with patch('app.db_manager.connect', side_effect=Exception("Test error")):
            # When: API 요청 시 예외 발생
            response = self.app.get('/api/users')
            
            # Then: 오류 응답이 올바르게 처리되어야 함
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertFalse(data['success'])
            self.assertIn('error', data)

    def test_api_response_structure(self):
        """API 응답 구조 테스트"""
        # Given: API 응답 구조
        expected_structure = {
            'success': bool,
            'data': (list, dict) if 'data' in ['users', 'relationships', 'timeline'] else dict,
            'error': str if 'error' in ['error'] else None
        }
        
        # When: API 요청
        response = self.app.get('/api/users')
        
        # Then: 응답 구조가 올바르게 형성되어야 함
        data = json.loads(response.data)
        self.assertIn('success', data)
        self.assertIsInstance(data['success'], bool)
        
        if data['success']:
            self.assertIn('data', data)
        else:
            self.assertIn('error', data)

    def test_user_id_parameter_validation(self):
        """사용자 ID 파라미터 검증 테스트"""
        # Given: 다양한 사용자 ID 형식
        test_user_ids = ['1', 'user-123', 'uuid-format', '12345']
        
        # When & Then: 각 사용자 ID로 API 요청이 성공해야 함
        for user_id in test_user_ids:
            with self.subTest(user_id=user_id):
                with patch('app.db_manager.connect', return_value=True):
                    with patch('app.db_manager.get_user_relationships', return_value=[]):
                        with patch('app.db_manager.disconnect'):
                            response = self.app.get(f'/api/users/{user_id}/relationships')
                            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()


