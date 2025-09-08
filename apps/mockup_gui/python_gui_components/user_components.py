#!/usr/bin/env python3
"""
사용자 관련 컴포넌트 모듈
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Dict, Any, Optional
import math

class UserRelationshipGraph(tk.Frame):
    """사용자 관계 네트워크 그래프"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent
        self.users = []
        self.relationships = []
        self.node_radius = 30
        self.node_positions = {}
        self.selected_node = None
        self.show_all_users = False
        self.current_selected_user = None
        self.user_selection_callbacks = [] # 사용자 선택 콜백 목록
        self._create_widgets()
    
    def add_user_selection_callback(self, callback):
        """사용자 선택 콜백 추가"""
        self.user_selection_callbacks.append(callback)
    
    def _create_widgets(self):
        """위젯 생성"""
        # 메인 프레임
        main_frame = tk.Frame(self, relief=tk.RAISED, borderwidth=2)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 제목
        title_label = tk.Label(main_frame, text="👥 사용자 관계 네트워크", 
                              font=("Arial", 12, "bold"))
        title_label.pack(pady=5)
        
        # 사용자 선택 프레임
        selection_frame = tk.Frame(main_frame)
        selection_frame.pack(fill=tk.X, padx=10, pady=5)
        
        selection_label = tk.Label(selection_frame, text="사용자 선택:")
        selection_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.user_var = tk.StringVar()
        self.user_combo = ttk.Combobox(selection_frame, 
                                       textvariable=self.user_var,
                                       state="readonly",
                                       width=20)
        self.user_combo.pack(side=tk.LEFT, padx=(0, 5))
        self.user_combo.bind("<<ComboboxSelected>>", self._on_user_selected)
        
        # 전체 보기/숨김 토글 버튼
        self.toggle_button = tk.Button(selection_frame, text="전체 보기", 
                                      command=self._toggle_all_users,
                                      bg="lightblue")
        self.toggle_button.pack(side=tk.LEFT, padx=(10, 0))
        
        # 캔버스 (그래프 그리기용)
        self.canvas = tk.Canvas(main_frame, bg='white', height=300)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 스크롤바
        h_scrollbar = tk.Scrollbar(main_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        h_scrollbar.pack(fill=tk.X)
        v_scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.canvas.config(xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set)
        
        # 마우스 이벤트 바인딩
        self.canvas.bind("<Button-1>", self._on_canvas_click)
        self.canvas.bind("<B1-Motion>", self._on_canvas_drag)
        
        # 초기 그래프 표시
        self._display_sample_graph()
        
        # 상태 변수
        self.show_all_users = False
        self.current_selected_user = None
    
    def _display_sample_graph(self):
        """샘플 그래프 표시"""
        # 샘플 사용자 데이터
        sample_users = [
            {'user_id': '1', 'user_name': '김철수', 'user_role': 'user'},
            {'user_id': '2', 'user_name': '이영희', 'user_role': 'caregiver'},
            {'user_id': '3', 'user_name': '박민수', 'user_role': 'family'},
            {'user_id': '4', 'user_name': '최지영', 'user_role': 'user'}
        ]
        
        # 샘플 관계 데이터
        sample_relationships = [
            {'user_id': '1', 'related_user_id': '2', 'relationship_type': 'caregiver'},
            {'user_id': '1', 'related_user_id': '3', 'relationship_type': 'family'},
            {'user_id': '4', 'related_user_id': '2', 'relationship_type': 'caregiver'}
        ]
        
        self.update_graph(sample_users, sample_relationships)
    
    def update_graph(self, users: List[Dict[str, Any]], relationships: List[Dict[str, Any]]):
        """그래프 데이터 업데이트"""
        self.users = users
        self.relationships = relationships
        
        print(f"📊 그래프 업데이트: {len(users)}명 사용자, {len(relationships)}개 관계")
        
        # 사용자 선택 콤보박스 업데이트
        if users:
            user_options = [f"{user.get('user_name', 'Unknown')} ({user.get('user_role_kr', user.get('user_role', 'Unknown'))})" for user in users]
            self.user_combo['values'] = user_options
            if user_options:
                self.user_combo.set(user_options[0])
                self.current_selected_user = users[0]['user_id']
                print(f"✅ 기본 선택 사용자: {users[0]['user_name']}")
        
        # 관계 데이터 디버깅
        if relationships:
            print(f"🔗 관계 데이터 상세:")
            for i, rel in enumerate(relationships[:5]):  # 처음 5개만 출력
                print(f"  {i+1}. {rel.get('user_id', 'N/A')} -> {rel.get('related_user_id', 'N/A')} ({rel.get('relationship_type', 'N/A')})")
        else:
            print("⚠️ 관계 데이터가 없습니다.")
        
        self._calculate_node_positions()
        self._draw_graph()
    
    def _on_user_selected(self, event=None):
        """사용자 선택 이벤트"""
        selected_user = self.user_combo.get()
        if selected_user:
            # 선택된 사용자 이름에서 user_id 추출
            for user in self.users:
                user_display = f"{user.get('user_name', 'Unknown')} ({user.get('user_role_kr', user.get('user_role', 'Unknown'))})"
                if user_display == selected_user:
                    self.current_selected_user = user['user_id']
                    print(f"👤 사용자 관계 그래프에서 선택됨: {user['user_name']} ({user['user_id']})")
                    
                    # 콜백 호출
                    for callback in self.user_selection_callbacks:
                        try:
                            callback(user['user_id'])
                        except Exception as e:
                            print(f"❌ 사용자 선택 콜백 실행 오류: {e}")
                    
                    # 그래프 다시 그리기
                    self._draw_graph()
                    break
    
    def _toggle_all_users(self):
        """전체 사용자 보기/숨김 토글"""
        self.show_all_users = not self.show_all_users
        
        if self.show_all_users:
            self.toggle_button.config(text="선택 사용자만", bg="lightcoral")
        else:
            self.toggle_button.config(text="전체 보기", bg="lightblue")
        
        self._draw_graph()
    
    def _calculate_node_positions(self):
        """노드 위치 계산"""
        if not self.users:
            return
        
        # 원형 배치
        center_x = 400
        center_y = 150
        radius = 120
        
        for i, user in enumerate(self.users):
            angle = (2 * math.pi * i) / len(self.users)
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            
            self.node_positions[user['user_id']] = (x, y)
    
    def _draw_graph(self):
        """그래프 그리기"""
        # 캔버스 초기화
        self.canvas.delete("all")
        
        if not self.users:
            print("⚠️ 사용자 데이터가 없어 그래프를 그릴 수 없습니다.")
            return
        
        # 노드 위치 계산
        self._calculate_node_positions()
        
        # 관계선 그리기
        display_relationships = []
        if self.show_all_users:
            # 모든 사용자와 관계 표시
            display_relationships = self.relationships
        else:
            # 선택된 사용자와 직접적인 관계만 표시
            if self.current_selected_user:
                display_relationships = [
                    rel for rel in self.relationships 
                    if rel.get('user_id') == self.current_selected_user or rel.get('related_user_id') == self.current_selected_user
                ]
        
        print(f"🔗 관계선 그리기: {len(display_relationships)}개 관계")
        
        for rel in display_relationships:
            user1_pos = self.node_positions.get(rel['user_id'])
            user2_pos = self.node_positions.get(rel['related_user_id'])
            
            print(f"  - 관계: {rel['user_id']} -> {rel['related_user_id']} ({rel['relationship_type']})")
            print(f"    위치: {user1_pos} -> {user2_pos}")
            
            if user1_pos and user2_pos:
                # 관계선 그리기
                self.canvas.create_line(
                    user1_pos[0], user1_pos[1], 
                    user2_pos[0], user2_pos[1],
                    fill="darkblue", width=2, arrow=tk.LAST
                )
                
                # 관계 타입 레이블
                mid_x = (user1_pos[0] + user2_pos[0]) / 2
                mid_y = (user1_pos[1] + user2_pos[1]) / 2
                
                self.canvas.create_text(
                    mid_x, mid_y - 10,
                    text=rel['relationship_type'],
                    font=("Arial", 8), fill="darkblue"
                )
                print(f"    ✅ 관계선 그리기 완료")
            else:
                print(f"    ❌ 위치 정보 없음")
        
        # 노드 그리기
        display_users = []
        if self.show_all_users:
            display_users = self.users
        else:
            # 선택된 사용자와 직접적인 관계가 있는 사용자만 표시
            if self.current_selected_user:
                related_user_ids = {self.current_selected_user}
                for rel in display_relationships:
                    related_user_ids.add(rel['user_id'])
                    related_user_ids.add(rel['related_user_id'])
                
                display_users = [user for user in self.users if user['user_id'] in related_user_ids]
        
        print(f"🎯 노드 그리기: {len(display_users)}명 사용자")
        
        for user in display_users:
            user_id = user['user_id']
            if user_id in self.node_positions:
                pos = self.node_positions[user_id]
                
                # 노드 색상 설정 (선택된 사용자는 강조)
                if user_id == self.current_selected_user:
                    node_color = "yellow"
                    outline_color = "red"
                    outline_width = 3
                else:
                    node_color = "lightblue"
                    outline_color = "darkblue"
                    outline_width = 2
                
                # 노드 원 그리기
                self.canvas.create_oval(
                    pos[0] - 20, pos[1] - 20,
                    pos[0] + 20, pos[1] + 20,
                    fill=node_color, outline=outline_color, width=outline_width
                )
                
                # 사용자 이름
                self.canvas.create_text(
                    pos[0], pos[1] - 30,
                    text=user.get('user_name', 'Unknown'),
                    font=("Arial", 10, "bold"), fill="black"
                )
                
                # 사용자 역할
                role_text = user.get('user_role_kr', user.get('user_role', 'Unknown'))
                self.canvas.create_text(
                    pos[0], pos[1] + 30,
                    text=role_text,
                    font=("Arial", 8), fill="darkgray"
                )
                
                print(f"  ✅ 노드 그리기: {user.get('user_name', 'Unknown')} at {pos}")
            else:
                print(f"  ❌ 노드 위치 없음: {user.get('user_name', 'Unknown')} ({user_id})")
    
    def _calculate_node_positions_for_users(self, users_to_display):
        """특정 사용자들의 노드 위치 계산"""
        if not users_to_display:
            return
        
        # 원형 배치
        center_x = 400
        center_y = 150
        radius = 120
        
        for i, user in enumerate(users_to_display):
            angle = (2 * math.pi * i) / len(users_to_display)
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            
            self.node_positions[user['user_id']] = (x, y)
    
    def _get_relationship_color(self, relationship_type: str) -> str:
        """관계 타입별 색상 반환"""
        colors = {
            'caregiver': '#FF6600',  # 주황
            'family': '#0066CC',     # 파랑
            'friend': '#66CC00',     # 초록
            'neighbor': '#CC66CC'    # 보라
        }
        return colors.get(relationship_type, '#CCCCCC')
    
    def _get_user_role_color(self, user_role: str) -> str:
        """사용자 역할별 색상 반환"""
        colors = {
            'user': '#E6F3FF',       # 연한 파랑
            'caregiver': '#FFF2E6',  # 연한 주황
            'family': '#E6F7FF',     # 연한 하늘
            'admin': '#F0E6FF'       # 연한 보라
        }
        return colors.get(user_role, '#F0F0F0')
    
    def _on_canvas_click(self, event):
        """캔버스 클릭 이벤트"""
        # 클릭된 노드 찾기
        clicked_node = None
        for user in self.users:
            pos = self.node_positions.get(user['user_id'])
            if pos:
                x, y = pos
                distance = math.sqrt((event.x - x)**2 + (event.y - y)**2)
                if distance <= self.node_radius:
                    clicked_node = user
                    break
        
        if clicked_node:
            self.selected_node = clicked_node
            self._highlight_selected_node()
            print(f"선택된 사용자: {clicked_node['user_name']} ({clicked_node['user_role']})")
    
    def _on_canvas_drag(self, event):
        """캔버스 드래그 이벤트"""
        # 노드 드래그 기능 (향후 구현)
        pass
    
    def _highlight_selected_node(self):
        """선택된 노드 하이라이트"""
        # 모든 노드 기본 스타일로 복원
        for user in self.users:
            pos = self.node_positions.get(user['user_id'])
            if pos:
                x, y = pos
                node_color = self._get_user_role_color(user['user_role'])
                self.canvas.itemconfig(f"node_{user['user_id']}", 
                                     fill=node_color, outline="black", width=2)
        
        # 선택된 노드 하이라이트
        if self.selected_node:
            pos = self.node_positions.get(self.selected_node['user_id'])
            if pos:
                self.canvas.itemconfig(f"node_{self.selected_node['user_id']}", 
                                     fill="yellow", outline="red", width=3)

class UserInfoTable(tk.Frame):
    """사용자 정보 테이블"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent
        self.users = []
        self.tree = None
        self.toggle_button = None
        self.filter_var = None
        self.filter_combo = None
        self.user_selection_callbacks = []
        self._create_widgets()
    
    def add_user_selection_callback(self, callback):
        """사용자 선택 콜백 추가"""
        self.user_selection_callbacks.append(callback)
    
    def _on_tree_select(self, event):
        """트리뷰 선택 이벤트"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            user_id = item['values'][0]  # 첫 번째 컬럼이 user_id
            print(f"👤 사용자 테이블에서 선택됨: {user_id}")
            
            # 콜백 호출
            for callback in self.user_selection_callbacks:
                try:
                    callback(user_id)
                except Exception as e:
                    print(f"❌ 사용자 선택 콜백 실행 오류: {e}")
    
    def _create_widgets(self):
        """위젯 생성"""
        # 메인 프레임
        main_frame = tk.Frame(self, relief=tk.RAISED, borderwidth=2)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 헤더 프레임
        header_frame = tk.Frame(main_frame)
        header_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # 제목
        title_label = tk.Label(header_frame, text="👥 사용자 목록", 
                              font=("Arial", 12, "bold"))
        title_label.pack(side=tk.LEFT)
        
        # 필터링 프레임
        filter_frame = tk.Frame(header_frame)
        filter_frame.pack(side=tk.LEFT, padx=(20, 0))
        
        filter_label = tk.Label(filter_frame, text="역할별 필터:", font=("Arial", 9))
        filter_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.filter_var = tk.StringVar(value="전체")
        self.filter_combo = ttk.Combobox(filter_frame, 
                                        textvariable=self.filter_var,
                                        values=["전체", "돌봄대상자", "돌봄제공자", "가족", "보호자", "관리자"],
                                        state="readonly",
                                        width=12)
        self.filter_combo.pack(side=tk.LEFT, padx=(0, 10))
        self.filter_combo.bind("<<ComboboxSelected>>", self._on_filter_changed)
        
        self.toggle_button = tk.Button(header_frame, text="접기", 
                                      command=self._toggle_table,
                                      bg="lightgray", relief=tk.RAISED)
        self.toggle_button.pack(side=tk.RIGHT)
        
        # 테이블 프레임
        self.table_frame = tk.Frame(main_frame)
        self.table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 트리뷰 생성
        columns = ("ID", "이름", "이메일", "역할", "전화번호", "생성일")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings", height=10)
        
        # 컬럼 설정
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor=tk.CENTER)
        
        # 스크롤바
        scrollbar = ttk.Scrollbar(self.table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # 배치
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 선택 이벤트 바인딩
        self.tree.bind("<<TreeviewSelect>>", self._on_tree_select)
        
        # 더블클릭 이벤트
        self.tree.bind("<Double-1>", self._on_user_double_click)
        
        # 초기 데이터 표시
        self._display_sample_data()
    
    def _display_sample_data(self):
        """샘플 데이터 표시"""
        sample_users = [
            {
                'user_id': '1',
                'user_name': '김철수',
                'email': 'kim@example.com',
                'user_role': '사용자',
                'phone_number': '010-1234-5678',
                'created_at': '2024-01-15'
            },
            {
                'user_id': '2',
                'user_name': '이영희',
                'email': 'lee@example.com',
                'user_role': '돌봄 제공자',
                'phone_number': '010-2345-6789',
                'created_at': '2024-01-20'
            },
            {
                'user_id': '3',
                'user_name': '박민수',
                'email': 'park@example.com',
                'user_role': '가족',
                'phone_number': '010-3456-7890',
                'created_at': '2024-02-01'
            }
        ]
        
        self.update_table(sample_users)
    
    def update_table(self, users: List[Dict[str, Any]]):
        """테이블 데이터 업데이트"""
        self.users = users
        self._apply_filter()
    
    def _apply_filter(self):
        """필터 적용"""
        # 기존 데이터 삭제
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # 필터링된 사용자 목록
        filtered_users = self._get_filtered_users()
        
        # 새 데이터 추가
        for user in filtered_users:
            values = (
                user.get('user_id', ''),
                user.get('user_name', ''),
                user.get('email', ''),
                user.get('user_role_kr', user.get('user_role', '')),
                user.get('phone_number', ''),
                user.get('created_at', '')
            )
            self.tree.insert('', tk.END, values=values)
    
    def _get_filtered_users(self) -> List[Dict[str, Any]]:
        """필터링된 사용자 목록 반환"""
        if not self.users:
            return []
        
        filter_value = self.filter_var.get()
        print(f"🔍 필터 적용: {filter_value}")
        
        if filter_value == "전체":
            print(f"✅ 전체 사용자 표시: {len(self.users)}명")
            return self.users
        
        # 한국어 역할명을 영문으로 매핑
        role_mapping = {
            "돌봄대상자": "care_target",
            "돌봄제공자": "caregiver", 
            "가족": "family",
            "보호자": "guardian",
            "관리자": "admin"
        }
        
        target_role = role_mapping.get(filter_value, filter_value)
        print(f"🎯 대상 역할: {filter_value} -> {target_role}")
        
        filtered_users = [user for user in self.users if user.get('user_role') == target_role]
        print(f"✅ 필터링 결과: {len(filtered_users)}명")
        
        return filtered_users
    
    def _on_filter_changed(self, event=None):
        """필터 변경 이벤트"""
        self._apply_filter()
    
    def _toggle_table(self):
        """테이블 접기/펼치기"""
        if self.table_frame.winfo_viewable():
            self.table_frame.pack_forget()
            self.toggle_button.config(text="펼치기")
        else:
            self.table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
            self.toggle_button.config(text="접기")
    
    def _on_user_double_click(self, event):
        """사용자 더블클릭 이벤트"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            user_data = dict(zip(['user_id', 'user_name', 'email', 'user_role', 'phone_number', 'created_at'], 
                                item['values']))
            
            # 상세 정보 표시
            self._show_user_details(user_data)
    
    def _show_user_details(self, user_data: Dict[str, Any]):
        """사용자 상세 정보 표시"""
        detail_window = tk.Toplevel(self)
        detail_window.title(f"사용자 상세 정보 - {user_data['user_name']}")
        detail_window.geometry("400x300")
        detail_window.transient(self)
        detail_window.grab_set()
        
        # 상세 정보 표시
        info_frame = tk.Frame(detail_window, padx=20, pady=20)
        info_frame.pack(fill=tk.BOTH, expand=True)
        
        # 제목
        title_label = tk.Label(info_frame, text=f"👤 {user_data['user_name']} 상세 정보", 
                              font=("Arial", 14, "bold"))
        title_label.pack(pady=(0, 20))
        
        # 정보 레이블들
        info_labels = [
            ('ID', user_data['user_id']),
            ('이름', user_data['user_name']),
            ('이메일', user_data['email']),
            ('역할', user_data['user_role']),
            ('전화번호', user_data['phone_number']),
            ('가입일', user_data['created_at'])
        ]
        
        for label_text, value in info_labels:
            frame = tk.Frame(info_frame)
            frame.pack(fill=tk.X, pady=5)
            
            label = tk.Label(frame, text=f"{label_text}:", width=10, anchor=tk.W, font=("Arial", 10, "bold"))
            label.pack(side=tk.LEFT)
            
            value_label = tk.Label(frame, text=value, anchor=tk.W, font=("Arial", 10))
            value_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # 닫기 버튼
        close_button = tk.Button(info_frame, text="닫기", command=detail_window.destroy,
                                bg="lightgray", relief=tk.RAISED)
        close_button.pack(pady=(20, 0))

class UserDashboardSummary(tk.Frame):
    """사용자 대시보드 요약"""
    
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
        title_label = tk.Label(main_frame, text="📊 대시보드 요약", 
                              font=("Arial", 12, "bold"))
        title_label.pack(pady=5)
        
        # 요약 정보 프레임
        summary_frame = tk.Frame(main_frame)
        summary_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # 통계 정보
        stats_data = [
            ("총 사용자", "12명", "#0066CC"),
            ("활성 디바이스", "8개", "#00CC66"),
            ("오늘 알림", "3건", "#FF6600"),
            ("위기 상황", "0건", "#FF0000")
        ]
        
        for i, (label, value, color) in enumerate(stats_data):
            stat_frame = tk.Frame(summary_frame)
            stat_frame.pack(side=tk.LEFT, padx=(0, 20))
            
            stat_label = tk.Label(stat_frame, text=label, font=("Arial", 9), fg="gray")
            stat_label.pack()
            
            stat_value = tk.Label(stat_frame, text=value, font=("Arial", 16, "bold"), fg=color)
            stat_value.pack()
        
        # 최근 활동 프레임
        activity_frame = tk.Frame(main_frame)
        activity_frame.pack(fill=tk.X, padx=10, pady=10)
        
        activity_label = tk.Label(activity_frame, text="최근 활동", font=("Arial", 10, "bold"))
        activity_label.pack(anchor=tk.W)
        
        # 활동 목록
        activities = [
            "14:30 - 김철수님 온도 센서 알림",
            "14:15 - 이영희님 방문 기록",
            "13:45 - 시스템 점검 완료",
            "13:20 - 박민수님 가스 센서 정상"
        ]
        
        for activity in activities:
            activity_item = tk.Label(activity_frame, text=f"• {activity}", 
                                    font=("Arial", 9), fg="darkgray", anchor=tk.W)
            activity_item.pack(anchor=tk.W, padx=(10, 0))
    
    def update_summary(self, summary_data: Dict[str, Any]):
        """요약 정보 업데이트"""
        # 실제 구현에서는 데이터 기반으로 업데이트
        pass

if __name__ == "__main__":
    # 테스트 코드
    root = tk.Tk()
    root.title("사용자 컴포넌트 테스트")
    root.geometry("800x600")
    
    # 사용자 관계 그래프 테스트
    relationship_graph = UserRelationshipGraph(root)
    relationship_graph.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # 사용자 정보 테이블 테스트
    user_table = UserInfoTable(root)
    user_table.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # 대시보드 요약 테스트
    dashboard_summary = UserDashboardSummary(root)
    dashboard_summary.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    root.mainloop()
