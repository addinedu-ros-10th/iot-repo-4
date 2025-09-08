#!/usr/bin/env python3
"""
GUI 컨트롤 컴포넌트 모듈
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Dict, Any
import threading

class SimulationControlPanel(tk.Frame):
    """시뮬레이션 제어 패널"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent
        self.callbacks = {}
        self._create_widgets()
    
    def _create_widgets(self):
        """위젯 생성"""
        # 메인 프레임
        main_frame = tk.Frame(self, relief=tk.RAISED, borderwidth=2)
        main_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # 제목
        title_label = tk.Label(main_frame, text="🎮 시뮬레이션 제어", 
                              font=("Arial", 12, "bold"))
        title_label.pack(pady=5)
        
        # 토글 스위치 프레임
        toggle_frame = tk.Frame(main_frame)
        toggle_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # 토글 스위치 (실시간/시뮬레이션)
        self.toggle_var = tk.BooleanVar(value=False)
        toggle_label = tk.Label(toggle_frame, text="실시간 모드:")
        toggle_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.toggle_switch = tk.Checkbutton(toggle_frame, 
                                           text="ON", 
                                           variable=self.toggle_var,
                                           command=self._on_toggle_change,
                                           selectcolor="green",
                                           activebackground="lightgreen")
        self.toggle_switch.pack(side=tk.LEFT)
        
        # 재생 제어 프레임
        control_frame = tk.Frame(main_frame)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # 재생/일시정지 버튼
        self.play_button = tk.Button(control_frame, 
                                    text="▶️ 재생", 
                                    command=self._on_play_click,
                                    bg="lightblue", 
                                    relief=tk.RAISED)
        self.play_button.pack(side=tk.LEFT, padx=(0, 5))
        
        self.pause_button = tk.Button(control_frame, 
                                     text="⏸️ 일시정지", 
                                     command=self._on_pause_click,
                                     bg="lightyellow", 
                                     relief=tk.RAISED)
        self.pause_button.pack(side=tk.LEFT, padx=(0, 5))
        
        self.stop_button = tk.Button(control_frame, 
                                    text="⏹️ 정지", 
                                    command=self._on_stop_click,
                                    bg="lightcoral", 
                                    relief=tk.RAISED)
        self.stop_button.pack(side=tk.LEFT, padx=(0, 5))
        
        # 속도 조절 프레임
        speed_frame = tk.Frame(main_frame)
        speed_frame.pack(fill=tk.X, padx=10, pady=5)
        
        speed_label = tk.Label(speed_frame, text="재생 속도:")
        speed_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.speed_var = tk.StringVar(value="1x")
        speed_combo = ttk.Combobox(speed_frame, 
                                   textvariable=self.speed_var,
                                   values=["0.5x", "1x", "2x", "5x"],
                                   state="readonly",
                                   width=8)
        speed_combo.pack(side=tk.LEFT, padx=(0, 5))
        speed_combo.bind("<<ComboboxSelected>>", self._on_speed_change)
        
        # 진행률 표시 프레임
        progress_frame = tk.Frame(main_frame)
        progress_frame.pack(fill=tk.X, padx=10, pady=5)
        
        progress_label = tk.Label(progress_frame, text="진행률:")
        progress_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.progress_bar = ttk.Progressbar(progress_frame, 
                                           length=200, 
                                           mode='determinate')
        self.progress_bar.pack(side=tk.LEFT, padx=(0, 5))
        
        self.progress_text = tk.Label(progress_frame, text="0%")
        self.progress_text.pack(side=tk.LEFT, padx=(0, 5))
        
        # 시간 표시 프레임
        time_frame = tk.Frame(main_frame)
        time_frame.pack(fill=tk.X, padx=10, pady=5)
        
        time_label = tk.Label(time_frame, text="현재 시간:")
        time_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.current_time_label = tk.Label(time_frame, text="--:--:--", 
                                         font=("Courier", 10))
        self.current_time_label.pack(side=tk.LEFT, padx=(0, 5))
        
        # 상태 표시 프레임
        status_frame = tk.Frame(main_frame)
        status_frame.pack(fill=tk.X, padx=10, pady=5)
        
        status_label = tk.Label(status_frame, text="상태:")
        status_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.status_label = tk.Label(status_frame, text="대기 중", 
                                    fg="blue", font=("Arial", 9, "bold"))
        self.status_label.pack(side=tk.LEFT, padx=(0, 5))
    
    def _on_toggle_change(self):
        """토글 스위치 변경 이벤트"""
        is_realtime = self.toggle_var.get()
        if is_realtime:
            self.toggle_switch.config(text="실시간", selectcolor="red")
            self.status_label.config(text="실시간 모드", fg="red")
        else:
            self.toggle_switch.config(text="시뮬레이션", selectcolor="green")
            self.status_label.config(text="시뮬레이션 모드", fg="green")
        
        # 콜백 호출
        if 'toggle_changed' in self.callbacks:
            self.callbacks['toggle_changed'](is_realtime)
    
    def _on_play_click(self):
        """재생 버튼 클릭 이벤트"""
        if 'play_clicked' in self.callbacks:
            self.callbacks['play_clicked']()
    
    def _on_pause_click(self):
        """일시정지 버튼 클릭 이벤트"""
        if 'pause_clicked' in self.callbacks:
            self.callbacks['pause_clicked']()
    
    def _on_stop_click(self):
        """정지 버튼 클릭 이벤트"""
        if 'stop_clicked' in self.callbacks:
            self.callbacks['stop_clicked']()
    
    def _on_speed_change(self, event):
        """속도 변경 이벤트"""
        speed = self.speed_var.get()
        if 'speed_changed' in self.callbacks:
            self.callbacks['speed_changed'](speed)
    
    def add_callback(self, event: str, callback: Callable):
        """콜백 함수 추가"""
        self.callbacks[event] = callback
    
    def update_progress(self, progress: float):
        """진행률 업데이트"""
        self.progress_bar['value'] = progress * 100
        self.progress_text.config(text=f"{progress * 100:.1f}%")
    
    def update_current_time(self, time_str: str):
        """현재 시간 업데이트"""
        self.current_time_label.config(text=time_str)
    
    def update_status(self, status: str, color: str = "black"):
        """상태 업데이트"""
        self.status_label.config(text=status, fg=color)

class AlertLevelDisplay(tk.Frame):
    """위기 등급 표시 컴포넌트"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent
        self.alert_levels = ['emergency', 'warning', 'attention', 'normal']
        self.alert_colors = {
            'emergency': '#FF0000',
            'warning': '#FF6600', 
            'attention': '#FFCC00',
            'normal': '#00CC00'
        }
        self.alert_icons = {
            'emergency': '🚨',
            'warning': '⚠️',
            'attention': '🔶',
            'normal': '✅'
        }
        self._create_widgets()
    
    def _create_widgets(self):
        """위젯 생성"""
        # 메인 프레임
        main_frame = tk.Frame(self, relief=tk.RAISED, borderwidth=2)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 제목
        title_label = tk.Label(main_frame, text="🚨 위기 등급 모니터링", 
                              font=("Arial", 12, "bold"))
        title_label.pack(pady=5)
        
        # 위기 등급 표시 프레임
        self.alert_frames = {}
        for level in self.alert_levels:
            frame = tk.Frame(main_frame, relief=tk.SUNKEN, borderwidth=1)
            frame.pack(fill=tk.X, padx=10, pady=2)
            
            # 아이콘과 레이블
            icon_label = tk.Label(frame, text=self.alert_icons[level], font=("Arial", 16))
            icon_label.pack(side=tk.LEFT, padx=5, pady=5)
            
            level_label = tk.Label(frame, text=level.upper(), 
                                  font=("Arial", 10, "bold"))
            level_label.pack(side=tk.LEFT, padx=5, pady=5)
            
            # 카운트 레이블
            count_label = tk.Label(frame, text="0", 
                                  font=("Arial", 12, "bold"),
                                  fg=self.alert_colors[level])
            count_label.pack(side=tk.RIGHT, padx=10, pady=5)
            
            # 사용자 목록 (접기/펼치기)
            user_frame = tk.Frame(frame)
            user_frame.pack(fill=tk.X, padx=20, pady=2)
            
            user_list = tk.Listbox(user_frame, height=3, selectmode=tk.SINGLE)
            user_list.pack(fill=tk.X)
            
            # 접기/펼치기 버튼
            toggle_button = tk.Button(user_frame, text="접기")
            toggle_button.pack(pady=2)
            
            # 버튼 참조를 lambda에 전달 (변수 정의 후)
            toggle_button.config(command=lambda f=user_frame, b=toggle_button: self._toggle_user_list(f, b))
            
            self.alert_frames[level] = {
                'frame': frame,
                'count_label': count_label,
                'user_list': user_list,
                'toggle_button': toggle_button,
                'user_frame': user_frame
            }
    
    def _toggle_user_list(self, user_frame, button):
        """사용자 목록 접기/펼치기"""
        # 현재 버튼 텍스트로 상태 확인
        if button.cget("text") == "펼치기":
            user_frame.pack(fill=tk.X, padx=20, pady=2)
            button.config(text="접기")
        else:
            user_frame.pack_forget()
            button.config(text="펼치기")
    
    def update_alert_counts(self, alert_data: Dict[str, Any]):
        """위기 등급별 카운트 업데이트"""
        for level in self.alert_levels:
            if level in self.alert_frames:
                count = alert_data.get(level, 0)
                self.alert_frames[level]['count_label'].config(text=str(count))
    
    def update_user_list(self, level: str, users: list):
        """특정 위기 등급의 사용자 목록 업데이트"""
        if level in self.alert_frames:
            user_list = self.alert_frames[level]['user_list']
            user_list.delete(0, tk.END)
            
            for user in users:
                user_list.insert(tk.END, f"{user.get('user_name', 'Unknown')} - {user.get('device_name', 'Unknown')}")
    
    def highlight_current_alert(self, current_level: str):
        """현재 위기 등급 하이라이트"""
        for level in self.alert_levels:
            if level in self.alert_frames:
                frame = self.alert_frames[level]['frame']
                if level == current_level:
                    frame.config(bg='yellow', relief=tk.RAISED, borderwidth=3)
                else:
                    frame.config(bg='white', relief=tk.SUNKEN, borderwidth=1)

class DataChartDisplay(tk.Frame):
    """데이터 차트 표시 컴포넌트"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent
        self._create_widgets()
    
    def _create_widgets(self):
        """위젯 생성"""
        # 메인 프레임
        main_frame = tk.Frame(self, relief=tk.RAISED, borderwidth=2)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 제목
        title_label = tk.Label(main_frame, text="📊 센서 데이터 차트", 
                              font=("Arial", 12, "bold"))
        title_label.pack(pady=5)
        
        # 차트 영역 (간단한 텍스트 기반 차트)
        self.chart_text = tk.Text(main_frame, height=15, width=50, 
                                  font=("Courier", 9))
        self.chart_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 스크롤바
        scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.chart_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.chart_text.config(yscrollcommand=scrollbar.set)
        
        # 초기 차트 표시
        self._display_sample_chart()
    
    def _display_sample_chart(self):
        """샘플 차트 표시"""
        sample_chart = """
시간별 센서 데이터 변화
========================

시간    | 온도 | 습도 | 가스 | 소음
--------|------|------|------|------
00:00   | 22°C | 45%  | 200  | 45dB
01:00   | 23°C | 46%  | 210  | 47dB
02:00   | 22°C | 44%  | 195  | 43dB
03:00   | 21°C | 43%  | 190  | 42dB
04:00   | 20°C | 42%  | 185  | 40dB
05:00   | 19°C | 41%  | 180  | 38dB

현재 상태: 정상
마지막 업데이트: --:--:--
        """
        self.chart_text.delete(1.0, tk.END)
        self.chart_text.insert(1.0, sample_chart)
    
    def update_chart(self, data: Dict[str, Any]):
        """차트 데이터 업데이트"""
        # 실제 구현에서는 matplotlib이나 다른 차트 라이브러리 사용
        # 여기서는 간단한 텍스트 업데이트
        current_time = data.get('timestamp', '--:--:--')
        if isinstance(current_time, str):
            time_str = current_time
        else:
            time_str = current_time.strftime("%H:%M:%S")
        
        self.chart_text.delete(1.0, tk.END)
        self.chart_text.insert(1.0, f"마지막 업데이트: {time_str}\n")
        self.chart_text.insert(tk.END, f"데이터 타입: {data.get('data_type', 'Unknown')}\n")
        self.chart_text.insert(tk.END, f"디바이스: {data.get('device_id', 'Unknown')}\n")
        
        # 데이터 내용 표시
        if 'data' in data:
            data_content = data['data']
            if isinstance(data_content, dict):
                for key, value in data_content.items():
                    self.chart_text.insert(tk.END, f"{key}: {value}\n")

if __name__ == "__main__":
    # 테스트 코드
    root = tk.Tk()
    root.title("GUI 컨트롤 테스트")
    root.geometry("400x600")
    
    # 시뮬레이션 제어 패널 테스트
    control_panel = SimulationControlPanel(root)
    control_panel.pack(fill=tk.X, padx=10, pady=10)
    
    # 위기 등급 표시 테스트
    alert_display = AlertLevelDisplay(root)
    alert_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # 데이터 차트 표시 테스트
    chart_display = DataChartDisplay(root)
    chart_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    root.mainloop()
