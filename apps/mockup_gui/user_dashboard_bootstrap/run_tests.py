#!/usr/bin/env python3
"""
IoT Care Bootstrap Dashboard - Test Runner
모든 테스트를 실행하고 결과를 수집하는 스크립트
"""

import unittest
import sys
import os
import json
from datetime import datetime

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(__file__))

def run_all_tests():
    """모든 테스트 실행"""
    print("🧪 IoT Care Bootstrap Dashboard 테스트 시작...")
    print("=" * 60)
    
    # 테스트 디렉토리 설정
    test_dir = os.path.join(os.path.dirname(__file__), 'tests')
    
    # 테스트 스위트 생성
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 단위 테스트 추가
    unit_test_dir = os.path.join(test_dir, 'unit')
    if os.path.exists(unit_test_dir):
        unit_tests = loader.discover(unit_test_dir, pattern='test_*.py')
        suite.addTests(unit_tests)
        print(f"✅ 단위 테스트 디렉토리 발견: {unit_test_dir}")
    else:
        print(f"⚠️ 단위 테스트 디렉토리를 찾을 수 없음: {unit_test_dir}")
    
    # 기능 테스트 추가
    functional_test_dir = os.path.join(test_dir, 'functional')
    if os.path.exists(functional_test_dir):
        functional_tests = loader.discover(functional_test_dir, pattern='test_*.py')
        suite.addTests(functional_tests)
        print(f"✅ 기능 테스트 디렉토리 발견: {functional_test_dir}")
    else:
        print(f"⚠️ 기능 테스트 디렉토리를 찾을 수 없음: {functional_test_dir}")
    
    # 통합 테스트 추가
    integration_test_dir = os.path.join(test_dir, 'integration')
    if os.path.exists(integration_test_dir):
        integration_tests = loader.discover(integration_test_dir, pattern='test_*.py')
        suite.addTests(integration_tests)
        print(f"✅ 통합 테스트 디렉토리 발견: {integration_test_dir}")
    else:
        print(f"⚠️ 통합 테스트 디렉토리를 찾을 수 없음: {integration_test_dir}")
    
    if suite.countTestCases() == 0:
        print("❌ 실행할 테스트가 없습니다.")
        return None, 0
    
    print(f"\n📋 총 {suite.countTestCases()}개의 테스트 케이스 발견")
    
    # 테스트 실행
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 결과 요약
    print("\n" + "=" * 60)
    print("📊 테스트 결과 요약")
    print("=" * 60)
    print(f"총 테스트 수: {result.testsRun}")
    print(f"성공: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"실패: {len(result.failures)}")
    print(f"오류: {len(result.errors)}")
    
    # 실패한 테스트 상세 정보
    if result.failures:
        print(f"\n❌ 실패한 테스트 ({len(result.failures)}개):")
        for test, traceback in result.failures:
            error_msg = traceback.split('AssertionError:')[1].strip() if 'AssertionError:' in traceback else 'Assertion failed'
            print(f"  - {test}: {error_msg}")
    
    # 오류가 발생한 테스트 상세 정보
    if result.errors:
        print(f"\n🚨 오류가 발생한 테스트 ({len(result.errors)}개):")
        for test, traceback in result.errors:
            error_msg = traceback.split('Exception:')[1].strip() if 'Exception:' in traceback else 'Exception occurred'
            print(f"  - {test}: {error_msg}")
    
    # 성공률 계산
    success_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100) if result.testsRun > 0 else 0
    print(f"\n🎯 성공률: {success_rate:.1f}%")
    
    # 결과를 JSON 파일로 저장
    save_test_results(result, success_rate)
    
    return result, success_rate

def save_test_results(result, success_rate):
    """테스트 결과를 JSON 파일로 저장"""
    test_results = {
        'timestamp': datetime.now().isoformat(),
        'summary': {
            'total_tests': result.testsRun,
            'successful': result.testsRun - len(result.failures) - len(result.errors),
            'failed': len(result.failures),
            'errors': len(result.errors),
            'success_rate': success_rate
        },
        'failures': [
            {
                'test': str(test),
                'traceback': traceback
            } for test, traceback in result.failures
        ],
        'errors': [
            {
                'test': str(test),
                'traceback': traceback
            } for test, traceback in result.errors
        ]
    }
    
    # 결과 파일 저장
    results_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'task', 'testing-results')
    os.makedirs(results_dir, exist_ok=True)
    
    results_file = os.path.join(results_dir, f'bootstrap_dashboard_test_results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
    
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(test_results, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 테스트 결과가 저장되었습니다: {results_file}")

def run_specific_test_category(category):
    """특정 카테고리의 테스트만 실행"""
    print(f"🧪 {category} 테스트 실행...")
    print("=" * 60)
    
    test_dir = os.path.join(os.path.dirname(__file__), 'tests', category)
    
    if not os.path.exists(test_dir):
        print(f"❌ {category} 테스트 디렉토리를 찾을 수 없습니다: {test_dir}")
        return None, 0
    
    loader = unittest.TestLoader()
    suite = loader.discover(test_dir, pattern='test_*.py')
    
    if suite.countTestCases() == 0:
        print(f"❌ {category} 카테고리에 실행할 테스트가 없습니다.")
        return None, 0
    
    print(f"📋 {suite.countTestCases()}개의 테스트 케이스 발견")
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    success_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100) if result.testsRun > 0 else 0
    
    print(f"\n📊 {category} 테스트 결과: {success_rate:.1f}% 성공")
    
    return result, success_rate

if __name__ == '__main__':
    if len(sys.argv) > 1:
        category = sys.argv[1].lower()
        if category in ['unit', 'functional', 'integration']:
            run_specific_test_category(category)
        else:
            print(f"❌ 알 수 없는 테스트 카테고리: {category}")
            print("사용 가능한 카테고리: unit, functional, integration")
    else:
        # 모든 테스트 실행
        run_all_tests()
