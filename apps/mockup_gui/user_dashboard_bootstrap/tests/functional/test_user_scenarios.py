"""
사용자 시나리오 기반 기능 테스트
실제 사용자 사용 패턴을 시뮬레이션한 테스트
"""

import unittest
import json
import sys
import os
from unittest.mock import Mock, patch, MagicMock

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from app import app


class TestUserScenarios(unittest.TestCase):
    """사용자 시나리오 기반 기능 테스트"""
    
    def setUp(self):
        """테스트 전 설정"""
        self.app = app.test_client()
        self.app.testing = True
        
    def tearDown(self):
        """테스트 후 정리"""
        pass

    def test_scenario_1_admin_dashboard_access(self):
        """시나리오 1: 관리자가 대시보드에 접근하여 전체 현황 파악"""
        # Given: 관리자가 대시보드에 접근
        # When: 메인 페이지 로드
        response = self.app.get('/')
        
        # Then: 대시보드가 정상적으로 로드되어야 함
        self.assertEqual(response.status_code, 200)
        html_content = response.data.decode('utf-8')
        
        # 필수 UI 요소들이 포함되어야 함
        self.assertIn('IoT Care Dashboard', html_content)
        self.assertIn('전체 사용자', html_content)
        self.assertIn('활성 디바이스', html_content)
        self.assertIn('센서 데이터 현황', html_content)
        self.assertIn('사용자 목록', html_content)

    @patch('app.db_manager.connect', return_value=True)
    @patch('app.db_manager.get_users')
    @patch('app.db_manager.disconnect')
    def test_scenario_2_user_management_workflow(self, mock_disconnect, mock_get_users, mock_connect):
        """시나리오 2: 사용자 관리 워크플로우"""
        # Given: 관리자가 사용자 목록을 확인하려고 함
        mock_get_users.return_value = [
            {
                'user_id': '1',
                'user_name': '김철수',
                'email': 'kim@example.com',
                'user_role': 'care_target',
                'user_role_kr': '돌봄대상자'
            },
            {
                'user_id': '2',
                'user_name': '이영희',
                'email': 'lee@example.com',
                'user_role': 'caregiver',
                'user_role_kr': '돌봄제공자'
            }
        ]
        
        # When: 사용자 목록 API 호출
        response = self.app.get('/api/users')
        
        # Then: 사용자 목록이 정상적으로 반환되어야 함
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['data']), 2)
        
        # 사용자 역할 번역이 올바르게 되어야 함
        user1 = data['data'][0]
        user2 = data['data'][1]
        self.assertEqual(user1['user_role_kr'], '돌봄대상자')
        self.assertEqual(user2['user_role_kr'], '돌봄제공자')

    @patch('app.db_manager.connect', return_value=True)
    @patch('app.db_manager.get_user_relationships')
    @patch('app.db_manager.disconnect')
    def test_scenario_3_care_relationship_analysis(self, mock_disconnect, mock_get_relationships, mock_connect):
        """시나리오 3: 돌봄 관계 분석"""
        # Given: 관리자가 특정 사용자의 돌봄 관계를 분석하려고 함
        mock_get_relationships.return_value = [
            {
                'relationship_id': '1',
                'user_id': '1',
                'related_user_id': '2',
                'relationship_type': 'caregiver',
                'created_at': '2025-08-25T10:00:00',
                'user_name': '김철수',
                'email': 'kim@example.com',
                'related_user_name': '이영희',
                'related_user_email': 'lee@example.com'
            }
        ]
        
        # When: 사용자 관계 API 호출
        response = self.app.get('/api/users/1/relationships')
        
        # Then: 돌봄 관계가 정상적으로 반환되어야 함
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['data']), 1)
        
        relationship = data['data'][0]
        self.assertEqual(relationship['relationship_type'], 'caregiver')
        self.assertEqual(relationship['user_name'], '김철수')
        self.assertEqual(relationship['related_user_name'], '이영희')

    @patch('app.db_manager.connect', return_value=True)
    @patch('app.db_manager.get_data_timeline')
    @patch('app.db_manager.disconnect')
    def test_scenario_4_monitoring_data_analysis(self, mock_disconnect, mock_get_timeline, mock_connect):
        """시나리오 4: 모니터링 데이터 분석"""
        # Given: 관리자가 24시간 모니터링 데이터를 분석하려고 함
        mock_get_timeline.return_value = [
            {
                'data_type': 'snapshot',
                'timestamp': '2025-08-25T10:00:00',
                'data': {'alert_level': 'normal', 'detected_activity': 'sleeping'}
            },
            {
                'data_type': 'actuator',
                'timestamp': '2025-08-25T11:00:00',
                'data': {'buzzer_type': 'alert', 'state': 'active', 'reason': 'movement_detected'}
            },
            {
                'data_type': 'event',
                'timestamp': '2025-08-25T12:00:00',
                'data': {'event_type': 'button_press', 'button_state': 'pressed'}
            }
        ]
        
        # When: 사용자 타임라인 API 호출 (24시간)
        response = self.app.get('/api/users/1/timeline?hours=24')
        
        # Then: 모니터링 데이터가 정상적으로 반환되어야 함
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['data']), 3)
        
        # 데이터 타입별로 올바르게 분류되어야 함
        data_types = [item['data_type'] for item in data['data']]
        self.assertIn('snapshot', data_types)
        self.assertIn('actuator', data_types)
        self.assertIn('event', data_types)

    @patch('app.db_manager.connect', return_value=True)
    @patch('app.db_manager.disconnect')
    def test_scenario_5_dashboard_statistics_overview(self, mock_disconnect, mock_connect):
        """시나리오 5: 대시보드 통계 개요"""
        # Given: 관리자가 대시보드 통계를 확인하려고 함
        # When: 대시보드 통계 API 호출
        response = self.app.get('/api/dashboard/stats')
        
        # Then: 통계 데이터가 정상적으로 반환되어야 함
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        
        stats = data['data']
        # 필수 통계 항목들이 포함되어야 함
        self.assertIn('total_users', stats)
        self.assertIn('active_devices', stats)
        self.assertIn('today_alerts', stats)
        self.assertIn('crisis_situations', stats)
        
        # 통계 값들이 숫자여야 함
        self.assertIsInstance(stats['total_users'], int)
        self.assertIsInstance(stats['active_devices'], int)
        self.assertIsInstance(stats['today_alerts'], int)
        self.assertIsInstance(stats['crisis_situations'], int)

    def test_scenario_6_error_handling_and_recovery(self):
        """시나리오 6: 오류 처리 및 복구"""
        # Given: 시스템에 오류가 발생한 상황
        with patch('app.db_manager.connect', side_effect=Exception("Database connection failed")):
            # When: API 요청 시 오류 발생
            response = self.app.get('/api/users')
            
            # Then: 오류가 적절히 처리되어야 함
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertFalse(data['success'])
            self.assertIn('error', data)
            self.assertIsInstance(data['error'], str)

    def test_scenario_7_concurrent_user_access(self):
        """시나리오 7: 동시 사용자 접근"""
        # Given: 여러 사용자가 동시에 대시보드에 접근
        import threading
        import time
        
        results = []
        
        def make_request():
            response = self.app.get('/')
            results.append(response.status_code)
        
        # When: 5개의 동시 요청 생성
        threads = []
        for i in range(5):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
            thread.start()
        
        # 모든 스레드 완료 대기
        for thread in threads:
            thread.join()
        
        # Then: 모든 요청이 성공해야 함
        self.assertEqual(len(results), 5)
        for status_code in results:
            self.assertEqual(status_code, 200)

    def test_scenario_8_data_consistency_across_apis(self):
        """시나리오 8: API 간 데이터 일관성"""
        # Given: 여러 API에서 동일한 사용자 정보를 조회
        with patch('app.db_manager.connect', return_value=True):
            with patch('app.db_manager.get_users', return_value=[{'user_id': '1', 'user_name': 'Test User'}]):
                with patch('app.db_manager.disconnect'):
                    # When: 사용자 목록과 관계 정보를 순차적으로 조회
                    users_response = self.app.get('/api/users')
                    relationships_response = self.app.get('/api/users/1/relationships')
                    
                    # Then: 데이터 일관성이 유지되어야 함
                    users_data = json.loads(users_response.data)
                    relationships_data = json.loads(relationships_response.data)
                    
                    self.assertTrue(users_data['success'])
                    self.assertTrue(relationships_data['success'])
                    
                    # 사용자 ID가 일치해야 함
                    user_id_from_users = users_data['data'][0]['user_id']
                    self.assertEqual(user_id_from_users, '1')


if __name__ == '__main__':
    unittest.main()


