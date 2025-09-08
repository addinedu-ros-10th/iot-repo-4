"""
시스템 전체 통합 테스트
백엔드와 프론트엔드의 통합 동작 테스트
"""

import unittest
import json
import sys
import os
import time
from unittest.mock import Mock, patch, MagicMock

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from app import app, db_manager


class TestSystemIntegration(unittest.TestCase):
    """시스템 전체 통합 테스트"""
    
    def setUp(self):
        """테스트 전 설정"""
        self.app = app.test_client()
        self.app.testing = True
        
    def tearDown(self):
        """테스트 후 정리"""
        pass

    def test_integration_1_full_user_workflow(self):
        """통합 테스트 1: 전체 사용자 워크플로우"""
        # Given: 관리자가 대시보드에서 사용자 정보를 종합적으로 확인하려고 함
        
        # Step 1: 메인 페이지 접근
        main_response = self.app.get('/')
        self.assertEqual(main_response.status_code, 200)
        
        # Step 2: 대시보드 통계 확인
        with patch('app.db_manager.connect', return_value=True):
            with patch('app.db_manager.disconnect'):
                stats_response = self.app.get('/api/dashboard/stats')
                self.assertEqual(stats_response.status_code, 200)
                stats_data = json.loads(stats_response.data)
                self.assertTrue(stats_data['success'])
        
        # Step 3: 사용자 목록 조회
        with patch('app.db_manager.connect', return_value=True):
            with patch('app.db_manager.get_users') as mock_get_users:
                with patch('app.db_manager.disconnect'):
                    mock_get_users.return_value = [
                        {
                            'user_id': '1',
                            'user_name': '통합테스트사용자',
                            'email': 'integration@test.com',
                            'user_role': 'care_target',
                            'user_role_kr': '돌봄대상자'
                        }
                    ]
                    
                    users_response = self.app.get('/api/users')
                    self.assertEqual(users_response.status_code, 200)
                    users_data = json.loads(users_response.data)
                    self.assertTrue(users_data['success'])
                    self.assertEqual(len(users_data['data']), 1)
        
        # Step 4: 특정 사용자 관계 조회
        with patch('app.db_manager.connect', return_value=True):
            with patch('app.db_manager.get_user_relationships') as mock_get_relationships:
                with patch('app.db_manager.disconnect'):
                    mock_get_relationships.return_value = [
                        {
                            'relationship_id': '1',
                            'user_id': '1',
                            'related_user_id': '2',
                            'relationship_type': 'caregiver'
                        }
                    ]
                    
                    relationships_response = self.app.get('/api/users/1/relationships')
                    self.assertEqual(relationships_response.status_code, 200)
                    relationships_data = json.loads(relationships_response.data)
                    self.assertTrue(relationships_data['success'])

    def test_integration_2_data_flow_across_components(self):
        """통합 테스트 2: 컴포넌트 간 데이터 흐름"""
        # Given: 여러 컴포넌트가 데이터를 주고받는 상황
        
        # Step 1: 데이터베이스 연결 상태 확인
        with patch('app.db_manager.connect', return_value=True):
            # Step 2: 사용자 데이터 조회
            with patch('app.db_manager.get_users') as mock_get_users:
                with patch('app.db_manager.disconnect'):
                    mock_get_users.return_value = [
                        {
                            'user_id': '1',
                            'user_name': '데이터플로우테스트',
                            'user_role': 'admin',
                            'user_role_kr': '관리자'
                        }
                    ]
                    
                    # Step 3: API 응답 구조 검증
                    response = self.app.get('/api/users')
                    data = json.loads(response.data)
                    
                    # 응답 구조 검증
                    self.assertIn('success', data)
                    self.assertIn('data', data)
                    self.assertTrue(data['success'])
                    
                    # 데이터 내용 검증
                    user = data['data'][0]
                    self.assertEqual(user['user_id'], '1')
                    self.assertEqual(user['user_name'], '데이터플로우테스트')
                    self.assertEqual(user['user_role_kr'], '관리자')

    def test_integration_3_error_propagation_and_handling(self):
        """통합 테스트 3: 오류 전파 및 처리"""
        # Given: 시스템의 여러 계층에서 오류가 발생하는 상황
        
        # Step 1: 데이터베이스 연결 오류
        with patch('app.db_manager.connect', return_value=False):
            response = self.app.get('/api/users')
            data = json.loads(response.data)
            
            # 오류 응답 구조 검증
            self.assertFalse(data['success'])
            self.assertIn('error', data)
            self.assertEqual(data['error'], '데이터베이스 연결 실패')
        
        # Step 2: 데이터베이스 쿼리 오류
        with patch('app.db_manager.connect', return_value=True):
            with patch('app.db_manager.get_users', side_effect=Exception("Query failed")):
                with patch('app.db_manager.disconnect'):
                    response = self.app.get('/api/users')
                    data = json.loads(response.data)
                    
                    # 오류 응답 구조 검증
                    self.assertFalse(data['success'])
                    self.assertIn('error', data)

    def test_integration_4_concurrent_operations(self):
        """통합 테스트 4: 동시 작업 처리"""
        # Given: 여러 사용자가 동시에 시스템을 사용하는 상황
        
        import threading
        import queue
        
        results = queue.Queue()
        
        def make_api_request(endpoint):
            """API 요청을 수행하는 함수"""
            try:
                with patch('app.db_manager.connect', return_value=True):
                    with patch('app.db_manager.disconnect'):
                        if 'stats' in endpoint:
                            response = self.app.get(endpoint)
                        elif 'users' in endpoint:
                            with patch('app.db_manager.get_users', return_value=[]):
                                response = self.app.get(endpoint)
                        else:
                            response = self.app.get(endpoint)
                        
                        results.put({
                            'endpoint': endpoint,
                            'status_code': response.status_code,
                            'success': True
                        })
            except Exception as e:
                results.put({
                    'endpoint': endpoint,
                    'error': str(e),
                    'success': False
                })
        
        # When: 3개의 동시 API 요청 생성
        endpoints = [
            '/api/dashboard/stats',
            '/api/users',
            '/'
        ]
        
        threads = []
        for endpoint in endpoints:
            thread = threading.Thread(target=make_api_request, args=(endpoint,))
            threads.append(thread)
            thread.start()
        
        # 모든 스레드 완료 대기
        for thread in threads:
            thread.join()
        
        # Then: 모든 요청이 성공해야 함
        self.assertEqual(results.qsize(), 3)
        
        while not results.empty():
            result = results.get()
            self.assertTrue(result['success'], f"요청 실패: {result}")

    def test_integration_5_data_consistency_and_integrity(self):
        """통합 테스트 5: 데이터 일관성 및 무결성"""
        # Given: 시스템 전체에서 데이터 일관성을 유지해야 하는 상황
        
        # Step 1: 동일한 사용자 ID로 여러 API 호출
        test_user_id = 'test-user-123'
        
        with patch('app.db_manager.connect', return_value=True):
            with patch('app.db_manager.get_users', return_value=[{'user_id': test_user_id}]):
                with patch('app.db_manager.get_user_relationships', return_value=[]):
                    with patch('app.db_manager.disconnect'):
                        # 사용자 목록 조회
                        users_response = self.app.get('/api/users')
                        users_data = json.loads(users_response.data)
                        
                        # 사용자 관계 조회
                        relationships_response = self.app.get(f'/api/users/{test_user_id}/relationships')
                        relationships_data = json.loads(relationships_response.data)
                        
                        # 데이터 일관성 검증
                        self.assertTrue(users_data['success'])
                        self.assertTrue(relationships_data['success'])
                        
                        # 사용자 ID가 일치해야 함
                        user_id_from_users = users_data['data'][0]['user_id']
                        self.assertEqual(user_id_from_users, test_user_id)

    def test_integration_6_system_performance_and_responsiveness(self):
        """통합 테스트 6: 시스템 성능 및 응답성"""
        # Given: 시스템이 빠른 응답을 제공해야 하는 상황
        
        # Step 1: 응답 시간 측정
        start_time = time.time()
        
        with patch('app.db_manager.connect', return_value=True):
            with patch('app.db_manager.disconnect'):
                response = self.app.get('/api/dashboard/stats')
        
        end_time = time.time()
        response_time = end_time - start_time
        
        # Then: 응답 시간이 허용 범위 내에 있어야 함 (1초 이내)
        self.assertLess(response_time, 1.0, f"응답 시간이 너무 김: {response_time:.3f}초")
        self.assertEqual(response.status_code, 200)

    def test_integration_7_frontend_backend_data_synchronization(self):
        """통합 테스트 7: 프론트엔드-백엔드 데이터 동기화"""
        # Given: 프론트엔드와 백엔드가 데이터를 동기화해야 하는 상황
        
        # Step 1: 백엔드 API에서 데이터 제공
        with patch('app.db_manager.connect', return_value=True):
            with patch('app.db_manager.get_users') as mock_get_users:
                with patch('app.db_manager.disconnect'):
                    mock_get_users.return_value = [
                        {
                            'user_id': 'sync-test-1',
                            'user_name': '동기화테스트1',
                            'user_role': 'care_target',
                            'user_role_kr': '돌봄대상자'
                        },
                        {
                            'user_id': 'sync-test-2',
                            'user_name': '동기화테스트2',
                            'user_role': 'caregiver',
                            'user_role_kr': '돌봄제공자'
                        }
                    ]
                    
                    # Step 2: API 응답 검증
                    response = self.app.get('/api/users')
                    data = json.loads(response.data)
                    
                    # Step 3: 데이터 구조 및 내용 검증
                    self.assertTrue(data['success'])
                    self.assertEqual(len(data['data']), 2)
                    
                    # 첫 번째 사용자 검증
                    user1 = data['data'][0]
                    self.assertEqual(user1['user_id'], 'sync-test-1')
                    self.assertEqual(user1['user_name'], '동기화테스트1')
                    self.assertEqual(user1['user_role_kr'], '돌봄대상자')
                    
                    # 두 번째 사용자 검증
                    user2 = data['data'][1]
                    self.assertEqual(user2['user_id'], 'sync-test-2')
                    self.assertEqual(user2['user_name'], '동기화테스트2')
                    self.assertEqual(user2['user_role_kr'], '돌봄제공자')

    def test_integration_8_system_reliability_and_stability(self):
        """통합 테스트 8: 시스템 안정성 및 신뢰성"""
        # Given: 시스템이 안정적으로 동작해야 하는 상황
        
        # Step 1: 연속적인 API 요청 수행
        request_count = 10
        successful_requests = 0
        
        for i in range(request_count):
            try:
                with patch('app.db_manager.connect', return_value=True):
                    with patch('app.db_manager.disconnect'):
                        response = self.app.get('/api/dashboard/stats')
                        if response.status_code == 200:
                            successful_requests += 1
            except Exception:
                pass  # 오류 발생 시 계속 진행
        
        # Then: 대부분의 요청이 성공해야 함 (80% 이상)
        success_rate = successful_requests / request_count
        self.assertGreaterEqual(success_rate, 0.8, f"성공률이 너무 낮음: {success_rate:.2%}")


if __name__ == '__main__':
    unittest.main()


