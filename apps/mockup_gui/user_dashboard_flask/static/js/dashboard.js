/**
 * IoT Care 사용자 대시보드 JavaScript
 */

class DashboardManager {
    constructor() {
        this.simulationActive = false;
        this.simulationPlaying = false;
        this.simulationSpeed = 1;
        this.currentTime = new Date();
        this.simulationInterval = null;
        this.sensorChart = null;
        this.users = [];
        this.relationships = [];
        this.timelineData = [];
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.updateCurrentTime();
        this.loadDashboardStats();
        this.loadUsers();
        this.initSensorChart();
        this.setupCollapsibleSections();
        
        // 1초마다 현재 시간 업데이트
        setInterval(() => this.updateCurrentTime(), 1000);
    }

    setupEventListeners() {
        // 시뮬레이션 컨트롤
        document.getElementById('simulationToggle').addEventListener('change', (e) => {
            this.toggleSimulationMode(e.target.checked);
        });

        document.getElementById('playBtn').addEventListener('click', () => {
            this.playSimulation();
        });

        document.getElementById('pauseBtn').addEventListener('click', () => {
            this.pauseSimulation();
        });

        document.getElementById('stopBtn').addEventListener('click', () => {
            this.stopSimulation();
        });

        document.getElementById('speedSelect').addEventListener('change', (e) => {
            this.setSimulationSpeed(parseInt(e.target.value));
        });

        // 사용자 선택
        document.getElementById('userSelect').addEventListener('change', (e) => {
            this.onUserSelected(e.target.value);
        });

        document.getElementById('toggleAllUsers').addEventListener('click', () => {
            this.toggleAllUsersView();
        });

        // 역할 필터
        document.getElementById('roleFilter').addEventListener('change', (e) => {
            this.filterUsersByRole(e.target.value);
        });
    }

    setupCollapsibleSections() {
        // 위기 등급 모니터링 토글
        document.getElementById('toggleCrisisMonitoring').addEventListener('click', () => {
            this.toggleSection('crisisMonitoringContent', 'toggleCrisisMonitoring');
        });

        // 최근 활동 토글
        document.getElementById('toggleRecentActivity').addEventListener('click', () => {
            this.toggleSection('recentActivityContent', 'toggleRecentActivity');
        });

        // 사용자 목록 토글
        document.getElementById('toggleUserList').addEventListener('click', () => {
            this.toggleSection('userListContent', 'toggleUserList');
        });
    }

    toggleSection(contentId, buttonId) {
        const content = document.getElementById(contentId);
        const button = document.getElementById(buttonId);
        const icon = button.querySelector('i');
        
        if (content.style.display === 'none') {
            content.style.display = 'block';
            icon.className = 'bi bi-chevron-down';
        } else {
            content.style.display = 'none';
            icon.className = 'bi bi-chevron-right';
        }
    }

    updateCurrentTime() {
        const now = new Date();
        const timeString = now.toLocaleTimeString('ko-KR');
        document.getElementById('current-time').textContent = timeString;
    }

    async loadDashboardStats() {
        try {
            const response = await fetch('/api/dashboard/stats');
            const data = await response.json();
            
            if (data.success) {
                const stats = data.data;
                document.getElementById('totalUsers').textContent = stats.total_users;
                document.getElementById('activeDevices').textContent = stats.active_devices;
                document.getElementById('todayAlerts').textContent = stats.today_alerts;
                document.getElementById('crisisSituations').textContent = stats.crisis_situations;
                
                // 위기 등급별 사용자 수 업데이트 (임시 데이터)
                this.updateCrisisLevels();
            }
        } catch (error) {
            console.error('대시보드 통계 로드 실패:', error);
        }
    }

    updateCrisisLevels() {
        // 임시 데이터로 위기 등급별 사용자 수 설정
        document.getElementById('emergencyCount').textContent = '2';
        document.getElementById('warningCount').textContent = '5';
        document.getElementById('attentionCount').textContent = '8';
        document.getElementById('normalCount').textContent = '260';
    }

    async loadUsers() {
        try {
            const response = await fetch('/api/users');
            const data = await response.json();
            
            if (data.success) {
                this.users = data.data;
                this.populateUserTable();
                this.populateUserSelect();
                this.updateRecentActivity();
            }
        } catch (error) {
            console.error('사용자 목록 로드 실패:', error);
        }
    }

    populateUserTable() {
        const tbody = document.getElementById('userTableBody');
        tbody.innerHTML = '';
        
        this.users.forEach(user => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>
                    <span class="status-indicator status-active"></span>
                    ${user.user_name || '이름 없음'}
                </td>
                <td>${user.user_role_kr || user.user_role || '역할 없음'}</td>
                <td>
                    <span class="badge bg-success">활성</span>
                </td>
            `;
            
            row.addEventListener('click', () => {
                this.onUserSelected(user.user_id);
            });
            
            tbody.appendChild(row);
        });
    }

    populateUserSelect() {
        const select = document.getElementById('userSelect');
        select.innerHTML = '<option value="">사용자 선택...</option>';
        
        this.users.forEach(user => {
            const option = document.createElement('option');
            option.value = user.user_id;
            option.textContent = `${user.user_name || '이름 없음'} (${user.user_role_kr || user.user_role || '역할 없음'})`;
            select.appendChild(option);
        });
    }

    filterUsersByRole(role) {
        const tbody = document.getElementById('userTableBody');
        tbody.innerHTML = '';
        
        const filteredUsers = role ? this.users.filter(user => user.user_role === role) : this.users;
        
        filteredUsers.forEach(user => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>
                    <span class="status-indicator status-active"></span>
                    ${user.user_name || '이름 없음'}
                </td>
                <td>${user.user_role_kr || user.user_role || '역할 없음'}</td>
                <td>
                    <span class="badge bg-success">활성</span>
                </td>
            `;
            
            row.addEventListener('click', () => {
                this.onUserSelected(user.user_id);
            });
            
            tbody.appendChild(row);
        });
    }

    async onUserSelected(userId) {
        if (!userId) return;
        
        try {
            // 사용자 관계 로드
            const response = await fetch(`/api/users/${userId}/relationships`);
            const data = await response.json();
            
            if (data.success) {
                this.relationships = data.data;
                this.drawRelationshipGraph(userId);
            }
            
            // 사용자 타임라인 로드
            const timelineResponse = await fetch(`/api/users/${userId}/timeline`);
            const timelineData = await timelineResponse.json();
            
            if (timelineData.success) {
                this.timelineData = timelineData.data;
                this.updateSensorChart();
            }
            
        } catch (error) {
            console.error('사용자 데이터 로드 실패:', error);
        }
    }

    drawRelationshipGraph(selectedUserId) {
        const container = document.getElementById('relationshipGraph');
        container.innerHTML = '';
        
        if (this.relationships.length === 0) {
            container.innerHTML = `
                <div class="d-flex align-items-center justify-content-center h-100 text-muted">
                    <i class="bi bi-info-circle me-2"></i>
                    선택된 사용자의 관계가 없습니다
                </div>
            `;
            return;
        }
        
        // 간단한 관계 그래프 그리기
        const canvas = document.createElement('canvas');
        canvas.width = container.offsetWidth;
        canvas.height = container.offsetHeight;
        container.appendChild(canvas);
        
        const ctx = canvas.getContext('2d');
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // 사용자 노드 그리기
        const nodes = [];
        const selectedUser = this.users.find(u => u.user_id === selectedUserId);
        
        if (selectedUser) {
            // 선택된 사용자를 중앙에 배치
            nodes.push({
                id: selectedUserId,
                name: selectedUser.user_name || '이름 없음',
                x: canvas.width / 2,
                y: canvas.height / 2,
                isSelected: true
            });
            
            // 관계된 사용자들을 주변에 배치
            this.relationships.forEach((rel, index) => {
                const relatedUserId = rel.related_user_id;
                const relatedUser = this.users.find(u => u.user_id === relatedUserId);
                
                if (relatedUser) {
                    const angle = (index / this.relationships.length) * 2 * Math.PI;
                    const radius = Math.min(canvas.width, canvas.height) * 0.3;
                    const x = canvas.width / 2 + Math.cos(angle) * radius;
                    const y = canvas.height / 2 + Math.sin(angle) * radius;
                    
                    nodes.push({
                        id: relatedUserId,
                        name: relatedUser.user_name || '이름 없음',
                        x: x,
                        y: y,
                        isSelected: false
                    });
                }
            });
            
            // 노드 그리기
            nodes.forEach(node => {
                ctx.beginPath();
                ctx.arc(node.x, node.y, 30, 0, 2 * Math.PI);
                ctx.fillStyle = node.isSelected ? '#dc3545' : '#0d6efd';
                ctx.fill();
                ctx.strokeStyle = '#ffffff';
                ctx.lineWidth = 3;
                ctx.stroke();
                
                // 텍스트 그리기
                ctx.fillStyle = '#ffffff';
                ctx.font = '12px Arial';
                ctx.textAlign = 'center';
                ctx.fillText(node.name.substring(0, 8), node.x, node.y + 5);
            });
            
            // 관계선 그리기
            this.relationships.forEach(rel => {
                const fromNode = nodes.find(n => n.id === rel.user_id);
                const toNode = nodes.find(n => n.id === rel.related_user_id);
                
                if (fromNode && toNode) {
                    ctx.beginPath();
                    ctx.moveTo(fromNode.x, fromNode.y);
                    ctx.lineTo(toNode.x, toNode.y);
                    ctx.strokeStyle = '#6c757d';
                    ctx.lineWidth = 2;
                    ctx.stroke();
                }
            });
        }
    }

    toggleAllUsersView() {
        const container = document.getElementById('relationshipGraph');
        container.innerHTML = `
            <div class="d-flex align-items-center justify-content-center h-100 text-muted">
                <i class="bi bi-diagram-3 me-2"></i>
                전체 사용자 관계 네트워크
            </div>
        `;
    }

    updateRecentActivity() {
        const activityList = document.getElementById('activityList');
        activityList.innerHTML = '';
        
        // 임시 활동 데이터
        const activities = [
            { type: '센서', message: '홈 상태 스냅샷 업데이트', time: '2분 전' },
            { type: '알림', message: '새로운 이벤트 감지됨', time: '5분 전' },
            { type: '사용자', message: '사용자 로그인', time: '10분 전' },
            { type: '시스템', message: '데이터베이스 연결 확인', time: '15분 전' }
        ];
        
        activities.forEach(activity => {
            const div = document.createElement('div');
            div.className = 'activity-item';
            div.innerHTML = `
                <div class="d-flex justify-content-between align-items-start">
                    <div>
                        <strong>${activity.type}</strong>: ${activity.message}
                    </div>
                    <small class="text-muted">${activity.time}</small>
                </div>
            `;
            activityList.appendChild(div);
        });
    }

    initSensorChart() {
        const ctx = document.getElementById('sensorChart').getContext('2d');
        
        this.sensorChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: '알림 레벨',
                    data: [],
                    borderColor: '#dc3545',
                    backgroundColor: 'rgba(220, 53, 69, 0.1)',
                    tension: 0.4
                }, {
                    label: '센서 이벤트',
                    data: [],
                    borderColor: '#0d6efd',
                    backgroundColor: 'rgba(13, 110, 253, 0.1)',
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: true,
                        text: '실시간 센서 데이터'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 10
                    }
                }
            }
        });
    }

    updateSensorChart() {
        if (!this.sensorChart || this.timelineData.length === 0) return;
        
        const labels = [];
        const alertData = [];
        const eventData = [];
        
        this.timelineData.slice(-20).forEach((item, index) => {
            const time = new Date(item.timestamp).toLocaleTimeString('ko-KR', {
                hour: '2-digit',
                minute: '2-digit'
            });
            labels.push(time);
            
            if (item.data_type === 'snapshot') {
                alertData.push(item.data.alert_level || 0);
                eventData.push(0);
            } else if (item.data_type === 'event') {
                alertData.push(0);
                eventData.push(1);
            } else {
                alertData.push(0);
                eventData.push(0);
            }
        });
        
        this.sensorChart.data.labels = labels;
        this.sensorChart.data.datasets[0].data = alertData;
        this.sensorChart.data.datasets[1].data = eventData;
        this.sensorChart.update();
    }

    toggleSimulationMode(enabled) {
        this.simulationActive = enabled;
        
        if (enabled) {
            document.getElementById('playBtn').disabled = false;
            document.getElementById('pauseBtn').disabled = false;
            document.getElementById('stopBtn').disabled = false;
            console.log('✅ 시뮬레이션 모드 활성화');
        } else {
            this.stopSimulation();
            document.getElementById('playBtn').disabled = true;
            document.getElementById('pauseBtn').disabled = true;
            document.getElementById('stopBtn').disabled = true;
            console.log('❌ 시뮬레이션 모드 비활성화');
        }
    }

    playSimulation() {
        if (!this.simulationActive) {
            alert('시뮬레이션 모드를 먼저 활성화해주세요.');
            return;
        }
        
        if (this.simulationPlaying) return;
        
        this.simulationPlaying = true;
        console.log('▶️ 시뮬레이션 재생 시작');
        
        this.simulationInterval = setInterval(() => {
            this.updateSimulation();
        }, 1000 / this.simulationSpeed);
    }

    pauseSimulation() {
        if (this.simulationInterval) {
            clearInterval(this.simulationInterval);
            this.simulationInterval = null;
        }
        this.simulationPlaying = false;
        console.log('⏸️ 시뮬레이션 일시정지');
    }

    stopSimulation() {
        if (this.simulationInterval) {
            clearInterval(this.simulationInterval);
            this.simulationInterval = null;
        }
        this.simulationPlaying = false;
        
        // 진행률 초기화
        document.getElementById('simulationProgress').style.width = '0%';
        document.getElementById('progressText').textContent = '0%';
        document.getElementById('currentSimulationTime').textContent = '00:00:00';
        
        console.log('⏹️ 시뮬레이션 정지');
    }

    setSimulationSpeed(speed) {
        this.simulationSpeed = speed;
        console.log(`⚡ 시뮬레이션 속도: ${speed}x`);
        
        // 재생 중이면 속도 변경 적용
        if (this.simulationPlaying && this.simulationInterval) {
            this.pauseSimulation();
            this.playSimulation();
        }
    }

    updateSimulation() {
        // 시뮬레이션 진행률 업데이트 (임시)
        const progress = Math.random() * 100;
        document.getElementById('simulationProgress').style.width = progress + '%';
        document.getElementById('progressText').textContent = Math.round(progress) + '%';
        
        // 시뮬레이션 시간 업데이트
        const elapsed = Math.floor(progress * 0.36); // 100% = 36초
        const hours = Math.floor(elapsed / 3600);
        const minutes = Math.floor((elapsed % 3600) / 60);
        const seconds = elapsed % 60;
        
        const timeString = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        document.getElementById('currentSimulationTime').textContent = timeString;
        
        // 센서 차트 업데이트 (임시 데이터)
        if (this.sensorChart) {
            const newData = Math.random() * 10;
            this.sensorChart.data.datasets[0].data.push(newData);
            this.sensorChart.data.datasets[0].data.shift();
            
            const newTime = new Date().toLocaleTimeString('ko-KR', {
                hour: '2-digit',
                minute: '2-digit'
            });
            this.sensorChart.data.labels.push(newTime);
            this.sensorChart.data.labels.shift();
            
            this.sensorChart.update();
        }
    }
}

// 페이지 로드 완료 시 대시보드 초기화
document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 IoT Care 대시보드 초기화 중...');
    window.dashboardManager = new DashboardManager();
    console.log('✅ 대시보드 초기화 완료');
});
