#!/usr/bin/env python3
"""
시뮬레이션 엔진 모듈
"""

import time
import threading
from datetime import datetime, timedelta
from typing import List, Dict, Any, Callable, Optional
import json

class TimeSimulationEngine:
    def __init__(self, data_timeline: List[Dict[str, Any]]):
        self.data_timeline = data_timeline
        self.current_index = 0
        self.is_playing = False
        self.playback_speed = 1.0  # 1x, 2x, 5x
        self.timer = None
        self.simulation_thread = None
        self.callbacks = []
        self.start_time = None
        self.simulation_start_time = None
        
        # 데이터 타임라인 정리
        self._prepare_timeline()
    
    def _prepare_timeline(self):
        """데이터 타임라인 준비"""
        if not self.data_timeline:
            return
        
        # 시간순 정렬
        self.data_timeline.sort(key=lambda x: x['timestamp'])
        
        # 시작/종료 시간 설정
        self.start_time = self.data_timeline[0]['timestamp']
        self.end_time = self.data_timeline[-1]['timestamp']
        
        print(f"📅 시뮬레이션 시간 범위: {self.start_time} ~ {self.end_time}")
        print(f"📊 총 데이터 포인트: {len(self.data_timeline)}")
    
    def add_callback(self, callback: Callable[[Dict[str, Any], int], None]):
        """데이터 업데이트 콜백 추가"""
        self.callbacks.append(callback)
    
    def start_simulation(self):
        """시뮬레이션 시작"""
        if self.is_playing:
            print("⚠️ 이미 재생 중입니다.")
            return
        
        if not self.data_timeline:
            print("⚠️ 시뮬레이션할 데이터가 없습니다.")
            return
        
        if len(self.data_timeline) == 0:
            print("⚠️ 데이터 타임라인이 비어있습니다.")
            return
        
        print(f"▶️ 시뮬레이션 시작 준비 중...")
        print(f"  - 데이터 포인트: {len(self.data_timeline)}개")
        print(f"  - 시작 시간: {self.data_timeline[0]['timestamp']}")
        print(f"  - 종료 시간: {self.data_timeline[-1]['timestamp']}")
        print(f"  - 재생 속도: {self.playback_speed}x")
        
        self.is_playing = True
        self.simulation_start_time = datetime.now()
        self.current_index = 0
        
        print(f"▶️ 시뮬레이션 시작 (속도: {self.playback_speed}x)")
        
        # 별도 스레드에서 시뮬레이션 실행
        self.simulation_thread = threading.Thread(target=self._simulation_loop)
        self.simulation_thread.daemon = True
        self.simulation_thread.start()
        
        print(f"✅ 시뮬레이션 스레드 시작됨")
    
    def pause_simulation(self):
        """시뮬레이션 일시정지"""
        if not self.is_playing:
            return
        
        self.is_playing = False
        print("⏸️ 시뮬레이션 일시정지")
    
    def stop_simulation(self):
        """시뮬레이션 정지"""
        self.is_playing = False
        self.current_index = 0
        print("⏹️ 시뮬레이션 정지")
    
    def set_speed(self, speed: float):
        """재생 속도 설정"""
        self.playback_speed = speed
        print(f"⚡ 재생 속도 변경: {speed}x")
    
    def set_position(self, index: int):
        """시뮬레이션 위치 설정"""
        if 0 <= index < len(self.data_timeline):
            self.current_index = index
            self._notify_callbacks()
            print(f"📍 시뮬레이션 위치: {index}/{len(self.data_timeline)}")
    
    def _simulation_loop(self):
        """시뮬레이션 메인 루프"""
        print(f"🔄 시뮬레이션 루프 시작: {len(self.data_timeline)}개 데이터")
        
        while self.is_playing and self.current_index < len(self.data_timeline):
            try:
                # 현재 데이터 포인트 처리
                current_data = self.data_timeline[self.current_index]
                print(f"📊 처리 중: 인덱스 {self.current_index}, 타입: {current_data.get('data_type', 'unknown')}")
                
                # 콜백 호출
                self._notify_callbacks()
                
                # 다음 데이터 포인트로 이동
                self.current_index += 1
                
                # 시뮬레이션 완료 체크
                if self.current_index >= len(self.data_timeline):
                    print("🏁 시뮬레이션 완료")
                    self.is_playing = False
                    break
                
                # 다음 데이터 포인트가 있으면 대기 시간 계산
                if self.current_index < len(self.data_timeline):
                    next_data = self.data_timeline[self.current_index]
                    
                    # timestamp가 datetime 객체인지 확인
                    if isinstance(current_data['timestamp'], datetime) and isinstance(next_data['timestamp'], datetime):
                        time_diff = (next_data['timestamp'] - current_data['timestamp']).total_seconds()
                    else:
                        # 문자열이거나 다른 형식인 경우 기본값 사용
                        time_diff = 1.0
                        print(f"⚠️ timestamp 형식 오류, 기본 대기 시간 사용: {time_diff}초")
                    
                    wait_time = time_diff / self.playback_speed
                    
                    # 최소 대기 시간 설정 (너무 빠르게 재생되지 않도록)
                    min_wait = 0.1
                    wait_time = max(wait_time, min_wait)
                    
                    print(f"⏱️ 대기 시간: {wait_time:.2f}초 (속도: {self.playback_speed}x)")
                    
                    # GUI 블로킹 방지를 위해 짧은 간격으로 체크
                    check_interval = 0.1
                    elapsed = 0
                    
                    while elapsed < wait_time and self.is_playing:
                        time.sleep(check_interval)
                        elapsed += check_interval
                        
                        # 진행률 로그 (1초마다)
                        if int(elapsed * 10) % 10 == 0:
                            progress = self.get_progress()
                            print(f"📈 진행률: {progress*100:.1f}% ({self.current_index}/{len(self.data_timeline)})")
                else:
                    print("🏁 시뮬레이션 완료 (데이터 범위 초과)")
                    self.is_playing = False
                    break
                    
            except Exception as e:
                print(f"❌ 시뮬레이션 루프 오류: {e}")
                self.is_playing = False
                break
        
        print(f"🔚 시뮬레이션 루프 종료 (재생 상태: {self.is_playing})")
    
    def _notify_callbacks(self):
        """콜백 함수들 호출"""
        if 0 <= self.current_index < len(self.data_timeline):
            current_data = self.data_timeline[self.current_index]
            print(f"📞 콜백 호출: 인덱스 {self.current_index}, 콜백 수 {len(self.callbacks)}")
            
            for i, callback in enumerate(self.callbacks):
                try:
                    callback(current_data, self.current_index)
                    print(f"  ✅ 콜백 {i+1} 실행 성공")
                except Exception as e:
                    print(f"  ❌ 콜백 {i+1} 실행 오류: {e}")
        else:
            print(f"⚠️ 콜백 호출 실패: 인덱스 {self.current_index}가 범위를 벗어남 (0~{len(self.data_timeline)-1})")
    
    def get_current_data(self) -> Optional[Dict[str, Any]]:
        """현재 데이터 포인트 반환"""
        if 0 <= self.current_index < len(self.data_timeline):
            return self.data_timeline[self.current_index]
        return None
    
    def get_progress(self) -> float:
        """진행률 반환 (0.0 ~ 1.0)"""
        if not self.data_timeline:
            return 0.0
        return self.current_index / len(self.data_timeline)
    
    def get_current_time(self) -> Optional[datetime]:
        """현재 시뮬레이션 시간 반환"""
        current_data = self.get_current_data()
        if current_data:
            return current_data['timestamp']
        return None
    
    def get_status(self) -> Dict[str, Any]:
        """시뮬레이션 상태 반환"""
        return {
            'is_playing': self.is_playing,
            'playback_speed': self.playback_speed,
            'current_index': self.current_index,
            'total_data': len(self.data_timeline),
            'progress': self.get_progress(),
            'current_time': self.get_current_time(),
            'start_time': self.start_time,
            'end_time': self.end_time
        }

class AlertLevelAnalyzer:
    """위기 등급 분석기"""
    
    @staticmethod
    def analyze_alert_level(sensor_data: Dict[str, Any]) -> str:
        """센서 데이터 기반 위기 등급 분석"""
        try:
            # 센서 데이터에서 alert_level 추출
            if 'alert_level' in sensor_data:
                return sensor_data['alert_level']
            
            # 센서 값 기반 위기 등급 계산
            if 'sensor_data' in sensor_data:
                sensor_values = sensor_data['sensor_data']
                
                # 온도 센서 (DHT)
                if 'temperature' in sensor_values:
                    temp = sensor_values['temperature']
                    if temp > 35 or temp < 10:
                        return 'emergency'
                    elif temp > 30 or temp < 15:
                        return 'warning'
                    elif temp > 25 or temp < 20:
                        return 'attention'
                
                # 가스 센서 (MQ5, MQ7)
                if 'gas_level' in sensor_values:
                    gas = sensor_values['gas_level']
                    if gas > 800:
                        return 'emergency'
                    elif gas > 600:
                        return 'warning'
                    elif gas > 400:
                        return 'attention'
                
                # 소음 센서
                if 'noise_level' in sensor_values:
                    noise = sensor_values['noise_level']
                    if noise > 100:
                        return 'emergency'
                    elif noise > 80:
                        return 'warning'
                    elif noise > 60:
                        return 'attention'
            
            return 'normal'
            
        except Exception as e:
            print(f"❌ 위기 등급 분석 오류: {e}")
            return 'normal'
    
    @staticmethod
    def get_alert_color(alert_level: str) -> str:
        """위기 등급별 색상 반환"""
        colors = {
            'emergency': '#FF0000',  # 빨강
            'warning': '#FF6600',    # 주황
            'attention': '#FFCC00',  # 노랑
            'normal': '#00CC00'      # 초록
        }
        return colors.get(alert_level, '#CCCCCC')
    
    @staticmethod
    def get_alert_icon(alert_level: str) -> str:
        """위기 등급별 아이콘 반환"""
        icons = {
            'emergency': '🚨',
            'warning': '⚠️',
            'attention': '🔶',
            'normal': '✅'
        }
        return icons.get(alert_level, '❓')

class DataVisualizer:
    """데이터 시각화 헬퍼"""
    
    @staticmethod
    def format_timestamp(timestamp: datetime) -> str:
        """타임스탬프 포맷팅"""
        return timestamp.strftime("%H:%M:%S")
    
    @staticmethod
    def format_duration(seconds: float) -> str:
        """지속시간 포맷팅"""
        if seconds < 60:
            return f"{seconds:.1f}초"
        elif seconds < 3600:
            minutes = seconds / 60
            return f"{minutes:.1f}분"
        else:
            hours = seconds / 3600
            return f"{hours:.1f}시간"
    
    @staticmethod
    def create_summary_stats(data_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """데이터 요약 통계 생성"""
        if not data_list:
            return {}
        
        stats = {
            'total_count': len(data_list),
            'start_time': data_list[0]['timestamp'] if data_list else None,
            'end_time': data_list[-1]['timestamp'] if data_list else None,
            'alert_levels': {},
            'device_types': {},
            'data_types': {}
        }
        
        for item in data_list:
            # 위기 등급 통계
            if 'alert_level' in item:
                level = item['alert_level']
                stats['alert_levels'][level] = stats['alert_levels'].get(level, 0) + 1
            
            # 디바이스 타입 통계
            if 'device_type' in item:
                device_type = item['device_type']
                stats['device_types'][device_type] = stats['device_types'].get(device_type, 0) + 1
            
            # 데이터 타입 통계
            if 'data_type' in item:
                data_type = item['data_type']
                stats['data_types'][data_type] = stats['data_types'].get(data_type, 0) + 1
        
        return stats

if __name__ == "__main__":
    # 테스트 코드
    print("🧪 시뮬레이션 엔진 테스트")
    
    # 샘플 데이터로 테스트
    sample_data = [
        {'timestamp': datetime.now(), 'data_type': 'test', 'value': 1},
        {'timestamp': datetime.now() + timedelta(seconds=1), 'data_type': 'test', 'value': 2},
        {'timestamp': datetime.now() + timedelta(seconds=2), 'data_type': 'test', 'value': 3}
    ]
    
    engine = TimeSimulationEngine(sample_data)
    print(f"✅ 엔진 생성 완료: {len(sample_data)}개 데이터 포인트")
    
    # 위기 등급 분석 테스트
    analyzer = AlertLevelAnalyzer()
    test_sensor_data = {'sensor_data': {'temperature': 40}}
    alert_level = analyzer.analyze_alert_level(test_sensor_data)
    print(f"✅ 위기 등급 분석: {alert_level} ({analyzer.get_alert_color(alert_level)})")
