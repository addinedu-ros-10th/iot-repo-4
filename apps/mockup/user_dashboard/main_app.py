#!/usr/bin/env python3
"""
IoT Care 사용자 대시보드 메인 애플리케이션
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
from datetime import datetime
from typing import Dict, Any, Optional

# 로컬 모듈 임포트
from database import DatabaseManager
from simulation_engine import TimeSimulationEngine, AlertLevelAnalyzer, DataVisualizer
from gui_controls import SimulationControlPanel, AlertLevelDisplay, DataChartDisplay
from user_components import UserRelationshipGraph, UserInfoTable, UserDashboardSummary

class IoTCareDashboard:
    """IoT Care 사용자 대시보드 메인 클래스"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("IoT Care 사용자 대시보드")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f0f0f0')
        
        # 데이터베이스 매니저
        self.db_manager = DatabaseManager()
        
        # 시뮬레이션 엔진
        self.simulation_engine = None
        
        # 데이터 저장소
        self.users = []
        self.relationships = []
        self.data_timeline = []
        
        # UI 컴포넌트들
        self.control_panel = None
        self.alert_display = None
        self.chart_display = None
        self.relationship_graph = None
        self.user_table = None
        self.summary_display = None
        
        # 시뮬레이션 상태
        self.is_simulation_mode = False
        self.current_user_id = None
        
        # UI 초기화
        self._create_widgets()
        # self._setup_callbacks() # 여기서는 호출하지 않음
        
        # 데이터 로드
        self._load_initial_data()
    
    def _create_widgets(self):
        """위젯 생성 및 배치"""
        # 메인 타이틀
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=60)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="🏠 IoT Care 스마트홈 사용자 대시보드", 
                              font=("Arial", 18, "bold"), fg="white", bg='#2c3e50')
        title_label.pack(expand=True)
        
        # 메인 컨테이너
        main_container = tk.Frame(self.root, bg='#f0f0f0')
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 상단 컨트롤 영역
        control_frame = tk.Frame(main_container, bg='#f0f0f0')
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 시뮬레이션 제어 패널
        self.control_panel = SimulationControlPanel(control_frame)
        self.control_panel.pack(fill=tk.X)
        
        # 중앙 대시보드 영역
        dashboard_frame = tk.Frame(main_container, bg='#f0f0f0')
        dashboard_frame.pack(fill=tk.BOTH, expand=True)
        
        # 좌측 패널 (위기 등급 + 요약)
        left_panel = tk.Frame(dashboard_frame, bg='#f0f0f0')
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # 위기 등급 표시
        self.alert_display = AlertLevelDisplay(left_panel)
        self.alert_display.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # 대시보드 요약
        self.summary_display = UserDashboardSummary(left_panel)
        self.summary_display.pack(fill=tk.BOTH, expand=True)
        
        # 중앙 패널 (센서 차트)
        center_panel = tk.Frame(dashboard_frame, bg='#f0f0f0')
        center_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        # 센서 데이터 차트
        self.chart_display = DataChartDisplay(center_panel)
        self.chart_display.pack(fill=tk.BOTH, expand=True)
        
        # 우측 패널 (사용자 관계 + 테이블)
        right_panel = tk.Frame(dashboard_frame, bg='#f0f0f0')
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # 사용자 관계 그래프
        self.relationship_graph = UserRelationshipGraph(right_panel)
        self.relationship_graph.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # 사용자 정보 테이블
        self.user_table = UserInfoTable(right_panel)
        self.user_table.pack(fill=tk.BOTH, expand=True)
        
        # 상태바
        status_frame = tk.Frame(self.root, bg='#34495e', height=30)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(status_frame, text="대기 중...", 
                                    font=("Arial", 9), fg="white", bg='#34495e')
        self.status_label.pack(side=tk.LEFT, padx=10)
        
        self.time_label = tk.Label(status_frame, text="", 
                                  font=("Arial", 9), fg="white", bg='#34495e')
        self.time_label.pack(side=tk.RIGHT, padx=10)
        
        # UI 컴포넌트 생성 후 콜백 설정
        # self._setup_callbacks()  # 여기서는 호출하지 않음
    
    def _setup_callbacks(self):
        """콜백 함수 설정"""
        # 시뮬레이션 제어 패널 콜백
        self.control_panel.add_callback('toggle_changed', self._on_toggle_changed)
        self.control_panel.add_callback('play_clicked', self._on_play_clicked)
        self.control_panel.add_callback('pause_clicked', self._on_pause_clicked)
        self.control_panel.add_callback('stop_clicked', self._on_stop_clicked)
        self.control_panel.add_callback('speed_changed', self._on_speed_changed)
        
        # 사용자 관계 그래프 콜백
        if self.relationship_graph:
            self.relationship_graph.add_user_selection_callback(self._on_user_selected)
        
        # 사용자 테이블 콜백
        if self.user_table:
            self.user_table.add_user_selection_callback(self._on_user_selected)
    
    def _on_user_selected(self, user_id: str):
        """사용자 선택 이벤트"""
        print(f"👤 사용자 선택됨: {user_id}")
        self.current_user_id = user_id
        
        # 선택된 사용자의 관계 데이터 로드
        try:
            if self.db_manager.connect():
                self.relationships = self.db_manager.get_user_relationships(user_id)
                
                # 관계 그래프 업데이트
                if self.relationship_graph:
                    self.relationship_graph.update_graph(self.users, self.relationships)
                
                # 데이터 타임라인 로드
                self._load_data_timeline()
                
                self.db_manager.disconnect()
                print(f"✅ 사용자 {user_id}의 데이터 업데이트 완료")
            else:
                print("❌ 데이터베이스 연결 실패")
        except Exception as e:
            print(f"❌ 사용자 데이터 업데이트 실패: {e}")
    
    def _load_initial_data(self):
        """초기 데이터 로드"""
        try:
            self.status_label.config(text="데이터베이스 연결 중...")
            
            # 데이터베이스 연결 시도
            if self.db_manager.connect():
                # 실제 데이터 로드
                self.users = self.db_manager.get_users()
                if self.users:
                    self.current_user_id = self.users[0]['user_id']
                    self.relationships = self.db_manager.get_user_relationships(self.current_user_id)
                    
                    # UI 업데이트
                    self.user_table.update_table(self.users)
                    self.relationship_graph.update_graph(self.users, self.relationships)
                    
                    # 데이터 타임라인 로드
                    self._load_data_timeline()
                    
                    # 콜백 설정 (UI 컴포넌트 생성 후)
                    self._setup_callbacks()
                    
                    self.status_label.config(text="데이터베이스 데이터 로드 완료")
                else:
                    self.status_label.config(text="사용자 데이터가 없습니다.")
                    self._load_sample_data()
            else:
                # 데이터베이스 연결 실패 시 샘플 데이터 사용
                print("⚠️ 데이터베이스 연결 실패, 샘플 데이터 사용")
                self._load_sample_data()
                
        except Exception as e:
            print(f"❌ 데이터 로드 중 오류: {e}")
            self.status_label.config(text="데이터 로드 실패, 샘플 데이터 사용")
            self._load_sample_data()
        finally:
            if self.db_manager.connection:
                self.db_manager.disconnect()
    
    def _load_data_timeline(self):
        """데이터 타임라인 로드"""
        try:
            if self.current_user_id:
                print(f"📊 사용자 {self.current_user_id}의 데이터 타임라인 로드 시작...")
                self.data_timeline = self.db_manager.get_data_timeline(self.current_user_id, hours=24)
                
                if self.data_timeline and len(self.data_timeline) > 0:
                    print(f"✅ 데이터 타임라인 로드 완료: {len(self.data_timeline)}개 포인트")
                    
                    # 데이터 형식 검증
                    for i, item in enumerate(self.data_timeline[:3]):  # 처음 3개만 검증
                        print(f"  📋 데이터 {i+1}: {item.get('data_type', 'unknown')} - {item.get('timestamp', 'no_timestamp')}")
                    
                    # 시뮬레이션 엔진 초기화
                    self.simulation_engine = TimeSimulationEngine(self.data_timeline)
                    self.simulation_engine.add_callback(self._on_data_update)
                    print(f"✅ 시뮬레이션 엔진 초기화 완료")
                else:
                    print("⚠️ 데이터 타임라인이 비어있습니다.")
                    self.data_timeline = []
                    
        except Exception as e:
            print(f"❌ 데이터 타임라인 로드 실패: {e}")
            self.data_timeline = []
    
    def _load_sample_data(self):
        """샘플 데이터 로드"""
        try:
            # 샘플 사용자 데이터 (돌봄대상자만)
            self.users = [
                {
                    'user_id': '1',
                    'user_name': '김철수',
                    'email': 'kim@example.com',
                    'user_role': 'care_target',
                    'phone_number': '010-1234-5678',
                    'created_at': '2024-01-15'
                },
                {
                    'user_id': '2',
                    'user_name': '이영희',
                    'email': 'lee@example.com',
                    'user_role': 'care_target',
                    'phone_number': '010-2345-6789',
                    'created_at': '2024-01-20'
                },
                {
                    'user_id': '3',
                    'user_name': '박민수',
                    'email': 'park@example.com',
                    'user_role': 'care_target',
                    'phone_number': '010-3456-7890',
                    'created_at': '2024-02-01'
                }
            ]
            
            # 샘플 관계 데이터
            self.relationships = [
                {'user_id': '1', 'related_user_id': '2', 'relationship_type': 'caregiver'},
                {'user_id': '1', 'related_user_id': '3', 'relationship_type': 'family'},
                {'user_id': '2', 'related_user_id': '3', 'relationship_type': 'colleague'}
            ]
            
            # 샘플 데이터 타임라인
            from datetime import datetime, timedelta
            self.data_timeline = []
            base_time = datetime.now() - timedelta(hours=24)
            
            # 24시간 동안의 샘플 데이터 생성
            for i in range(24):
                timestamp = base_time + timedelta(hours=i)
                
                # 홈 상태 스냅샷
                self.data_timeline.append({
                    'data_type': 'snapshot',
                    'timestamp': timestamp,
                    'device_id': 'temp_sensor_1',
                    'data': {
                        'sensor_data': {
                            'temperature': 20 + (i % 10),  # 20-29도 사이 변화
                            'humidity': 40 + (i % 20),     # 40-59% 사이 변화
                            'gas_level': 200 + (i % 100)   # 200-299 사이 변화
                        },
                        'alert_level': 'normal' if i < 20 else 'attention'
                    }
                })
                
                # 액추에이터 로그
                if i % 3 == 0:  # 3시간마다
                    self.data_timeline.append({
                        'data_type': 'actuator',
                        'timestamp': timestamp + timedelta(minutes=30),
                        'device_id': 'buzzer_1',
                        'data': {
                            'action': 'alert',
                            'status': 'active' if i % 6 == 0 else 'inactive'
                        }
                    })
                
                # 센서 이벤트
                if i % 2 == 0:  # 2시간마다
                    self.data_timeline.append({
                        'data_type': 'event',
                        'timestamp': timestamp + timedelta(minutes=15),
                        'device_id': 'motion_sensor_1',
                        'data': {
                            'event_type': 'motion_detected',
                            'value': 'detected' if i % 4 == 0 else 'none'
                        }
                    })
            
            # 시간순 정렬
            self.data_timeline.sort(key=lambda x: x['timestamp'])
            
            # UI 업데이트
            self.user_table.update_table(self.users)
            self.relationship_graph.update_graph(self.users, self.relationships)
            
            # 시뮬레이션 엔진 초기화
            if self.data_timeline:
                self.simulation_engine = TimeSimulationEngine(self.data_timeline)
                self.simulation_engine.add_callback(self._on_data_update)
                print(f"✅ 샘플 데이터 타임라인 로드 완료: {len(self.data_timeline)}개 포인트")
                print(f"✅ 시뮬레이션 엔진 초기화 완료")
            else:
                print("⚠️ 샘플 데이터 타임라인이 비어있습니다.")
            
            self.status_label.config(text="샘플 데이터 로드 완료")
            
        except Exception as e:
            print(f"❌ 샘플 데이터 로드 실패: {e}")
            self.status_label.config(text="샘플 데이터 로드 실패")
    
    def _on_toggle_changed(self, is_realtime: bool):
        """토글 스위치 변경 이벤트"""
        self.is_simulation_mode = not is_realtime
        
        if self.is_simulation_mode:
            self.status_label.config(text="시뮬레이션 모드")
            self.control_panel.update_status("시뮬레이션 모드", "green")
            print("🔄 시뮬레이션 모드로 전환")
            
            # 데이터 타임라인 확인
            if not self.data_timeline or len(self.data_timeline) == 0:
                print("⚠️ 데이터 타임라인이 비어있어 시뮬레이션을 시작할 수 없습니다.")
                self.status_label.config(text="시뮬레이션 모드 (데이터 없음)")
                return
            
            # 시뮬레이션 엔진이 없으면 초기화
            if not self.simulation_engine:
                print("🔄 시뮬레이션 엔진 초기화...")
                try:
                    self.simulation_engine = TimeSimulationEngine(self.data_timeline)
                    self.simulation_engine.add_callback(self._on_data_update)
                    print("✅ 시뮬레이션 엔진 초기화 완료")
                except Exception as e:
                    print(f"❌ 시뮬레이션 엔진 초기화 실패: {e}")
                    self.status_label.config(text="시뮬레이션 엔진 초기화 실패")
                    return
            
            if self.simulation_engine:
                # 시뮬레이션 엔진 상태 초기화
                self.simulation_engine.current_index = 0
                self.simulation_engine.is_playing = False
                # 진행률 초기화
                self.control_panel.update_progress(0.0)
                self.control_panel.update_current_time("--:--:--")
                print("✅ 시뮬레이션 엔진 상태 초기화 완료")
                self.status_label.config(text="시뮬레이션 모드 (준비 완료)")
            else:
                print("⚠️ 시뮬레이션 엔진이 초기화되지 않았습니다.")
                self.status_label.config(text="시뮬레이션 모드 (엔진 오류)")
        else:
            self.status_label.config(text="실시간 모드")
            self.control_panel.update_status("실시간 모드", "red")
            print("📡 실시간 모드로 전환")
    
    def _on_play_clicked(self):
        """재생 버튼 클릭 이벤트"""
        print("▶️ 재생 버튼 클릭됨")
        print(f"  - 시뮬레이션 모드: {self.is_simulation_mode}")
        print(f"  - 시뮬레이션 엔진: {'있음' if self.simulation_engine else '없음'}")
        print(f"  - 데이터 타임라인: {len(self.data_timeline) if self.data_timeline else 0}개")
        
        if self.simulation_engine and self.is_simulation_mode:
            print("▶️ 시뮬레이션 시작 시도...")
            try:
                self.simulation_engine.start_simulation()
                self.control_panel.update_status("재생 중", "green")
                self.status_label.config(text="시뮬레이션 재생 중...")
                print("▶️ 시뮬레이션 시작됨")
            except Exception as e:
                print(f"❌ 시뮬레이션 시작 실패: {e}")
                self.status_label.config(text="시뮬레이션 시작 실패")
        else:
            if not self.simulation_engine:
                print("❌ 시뮬레이션 엔진이 초기화되지 않았습니다.")
                self.status_label.config(text="시뮬레이션 엔진 없음")
            if not self.is_simulation_mode:
                print("❌ 시뮬레이션 모드가 아닙니다.")
                self.status_label.config(text="시뮬레이션 모드가 아님")
    
    def _on_pause_clicked(self):
        """일시정지 버튼 클릭 이벤트"""
        if self.simulation_engine:
            self.simulation_engine.pause_simulation()
            self.control_panel.update_status("일시정지", "orange")
            self.status_label.config(text="시뮬레이션 일시정지")
            print("⏸️ 시뮬레이션 일시정지")
    
    def _on_stop_clicked(self):
        """정지 버튼 클릭 이벤트"""
        if self.simulation_engine:
            self.simulation_engine.stop_simulation()
            self.control_panel.update_status("정지", "red")
            self.status_label.config(text="시뮬레이션 정지")
            print("⏹️ 시뮬레이션 정지")
    
    def _on_speed_changed(self, speed: str):
        """속도 변경 이벤트"""
        if self.simulation_engine:
            try:
                speed_value = float(speed.replace('x', ''))
                self.simulation_engine.set_speed(speed_value)
                print(f"⚡ 재생 속도 변경: {speed}")
            except ValueError:
                print(f"❌ 잘못된 속도 값: {speed}")
    
    def _on_data_update(self, data: Dict[str, Any], index: int):
        """데이터 업데이트 콜백"""
        try:
            # UI 업데이트 (메인 스레드에서 실행)
            self.root.after(0, self._update_ui_with_data, data, index)
            
        except Exception as e:
            print(f"❌ 데이터 업데이트 오류: {e}")
    
    def _update_ui_with_data(self, data: Dict[str, Any], index: int):
        """UI 데이터 업데이트"""
        try:
            # 진행률 업데이트
            if self.simulation_engine:
                progress = self.simulation_engine.get_progress()
                self.control_panel.update_progress(progress)
                
                # 현재 시간 업데이트
                current_time = self.simulation_engine.get_current_time()
                if current_time:
                    time_str = DataVisualizer.format_timestamp(current_time)
                    self.control_panel.update_current_time(time_str)
                    self.time_label.config(text=f"시뮬레이션 시간: {time_str}")
            
            # 차트 업데이트
            self.chart_display.update_chart(data)
            
            # 위기 등급 분석 및 업데이트
            if 'data' in data:
                alert_level = AlertLevelAnalyzer.analyze_alert_level(data['data'])
                self.alert_display.highlight_current_alert(alert_level)
                
                # 위기 등급별 통계 업데이트
                stats = DataVisualizer.create_summary_stats(self.data_timeline[:index+1])
                if 'alert_levels' in stats:
                    self.alert_display.update_alert_counts(stats['alert_levels'])
            
            # 상태 업데이트
            self.status_label.config(text=f"데이터 처리 중... ({index+1}/{len(self.data_timeline)})")
            
        except Exception as e:
            print(f"❌ UI 업데이트 오류: {e}")
    
    def _update_timer(self):
        """타이머 업데이트"""
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.config(text=f"현재 시간: {current_time}")
        self.root.after(1000, self._update_timer)
    
    def run(self):
        """애플리케이션 실행"""
        try:
            # 타이머 시작
            self._update_timer()
            
            # 메인 루프 시작
            self.root.mainloop()
            
        except Exception as e:
            print(f"❌ 애플리케이션 실행 오류: {e}")
        finally:
            # 정리 작업
            if self.db_manager:
                self.db_manager.disconnect()
            if self.simulation_engine:
                self.simulation_engine.stop_simulation()

def main():
    """메인 함수"""
    try:
        print("🚀 IoT Care 사용자 대시보드 시작...")
        
        # 애플리케이션 생성 및 실행
        app = IoTCareDashboard()
        app.run()
        
    except Exception as e:
        print(f"❌ 애플리케이션 시작 실패: {e}")
        messagebox.showerror("치명적 오류", f"애플리케이션을 시작할 수 없습니다: {e}")

if __name__ == "__main__":
    main()
