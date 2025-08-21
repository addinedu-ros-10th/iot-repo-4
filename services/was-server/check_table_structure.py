#!/usr/bin/env python3
"""
테이블 구조 확인 스크립트
"""

import psycopg2
from psycopg2.extras import RealDictCursor

def check_table_structure():
    """테이블 구조를 확인합니다."""
    
    # 데이터베이스 연결
    conn = psycopg2.connect(
        host='192.168.2.81',
        port=15432,
        database='iot_care',
        user='svc_dev',
        password='IOT_dev_123!@#'
    )
    
    cur = conn.cursor()
    
    try:
        print("🔍 테이블 구조 확인 중...")
        
        # Edge 센서 테이블들의 구조 확인
        tables = ['sensor_edge_flame', 'sensor_edge_pir', 'sensor_edge_reed', 'sensor_edge_tilt']
        
        for table_name in tables:
            print(f"\n📋 {table_name} 테이블 구조:")
            cur.execute(f"""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns 
                WHERE table_name = '{table_name}' 
                ORDER BY ordinal_position;
            """)
            
            columns = cur.fetchall()
            for col in columns:
                nullable = "NULL" if col[2] == "YES" else "NOT NULL"
                default = f" DEFAULT {col[3]}" if col[3] else ""
                print(f"  - {col[0]}: {col[1]} {nullable}{default}")
            
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    check_table_structure() 