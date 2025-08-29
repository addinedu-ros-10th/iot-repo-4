#!/usr/bin/env python3
"""
Flask 앱 연결 테스트
"""

import urllib.request
import urllib.error
import json

def test_flask_app():
    """Flask 앱 테스트"""
    try:
        print("🔍 Flask 앱 연결 테스트 중...")
        
        # 메인 페이지 테스트
        print("  - 메인 페이지 테스트...")
        response = urllib.request.urlopen('http://localhost:5000/')
        html = response.read().decode('utf-8')
        print(f"    ✅ 메인 페이지 응답: {len(html)} 문자")
        print(f"    HTML 미리보기: {html[:200]}...")
        
        # API 테스트
        print("\n  - API 테스트...")
        
        # 사용자 목록 API
        print("    - 사용자 목록 API...")
        response = urllib.request.urlopen('http://localhost:5000/api/users')
        data = json.loads(response.read().decode('utf-8'))
        if data['success']:
            print(f"      ✅ 사용자 {len(data['data'])}명 조회 성공")
        else:
            print(f"      ❌ 사용자 조회 실패: {data['error']}")
        
        # 대시보드 통계 API
        print("    - 대시보드 통계 API...")
        response = urllib.request.urlopen('http://localhost:5000/api/dashboard/stats')
        data = json.loads(response.read().decode('utf-8'))
        if data['success']:
            print(f"      ✅ 통계 조회 성공: {data['data']}")
        else:
            print(f"      ❌ 통계 조회 실패: {data['error']}")
            
    except urllib.error.URLError as e:
        print(f"❌ 연결 실패: {e}")
        print("   Flask 앱이 실행 중인지 확인하세요.")
    except Exception as e:
        print(f"❌ 테스트 실패: {e}")

if __name__ == '__main__':
    test_flask_app()
