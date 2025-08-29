/**
 * IoT Care Bootstrap Dashboard - Modern JavaScript
 * 현대적이고 세련된 대시보드 기능 구현
 */

class ModernDashboard {
    constructor() {
        this.sensorChart = null;
        this.users = [];
        this.relationships = [];
        this.timelineData = [];
        this.isLoading = false;
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.initializeCharts();
        this.loadDashboardData();
        this.startRealTimeUpdates();
        
        // 페이지 로드 시 초기화
        this.showLoadingStates();
    }

    setupEventListeners() {
        // 사용자 선택 이벤트
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('user-select-btn')) {
                const userId = e.target.dataset.userId;
                this.selectUser(userId);
            }
        });

        // 새로고침 버튼
        const refreshBtn = document.createElement('button');
        refreshBtn.className = 'btn btn-glass position-fixed';
        refreshBtn.style.cssText = 'bottom: 20px; right: 20px; z-index: 1000;';
        refreshBtn.innerHTML = '<i class="bi bi-arrow-clockwise"></i>';
        refreshBtn.onclick = () => this.refreshDashboard();
        document.body.appendChild(refreshBtn);
    }

    initializeCharts() {
        const ctx = document.getElementById('sensorChart');
        if (!ctx) return;

        this.sensorChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: '온도 센서',
                    data: [],
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    tension: 0.4,
                    fill: true
                }, {
                    label: '가스 센서',
                    data: [],
                    borderColor: '#f093fb',
                    backgroundColor: 'rgba(240, 147, 251, 0.1)',
                    tension: 0.4,
                    fill: true
                }, {
                    label: '소음 센서',
                    data: [],
                    borderColor: '#4facfe',
                    backgroundColor: 'rgba(79, 172, 254, 0.1)',
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: {
                            color: '#ffffff',
                            font: {
                                size: 12
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        ticks: {
                            color: '#ffffff',
                            maxTicksLimit: 8
                        },
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        }
                    },
                    y: {
                        ticks: {
                            color: '#ffffff'
                        },
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        }
                    }
                },
                animation: {
                    duration: 1000,
                    easing: 'easeInOutQuart'
                }
            }
        });
    }

    async loadDashboardData() {
        try {
            this.isLoading = true;
            
            // 대시보드 통계 로드
            await this.loadDashboardStats();
            
            // 사용자 목록 로드
            await this.loadUsers();
            
            // 센서 데이터 로드
            await this.loadSensorData();
            
            // 최근 활동 로드
            await this.loadRecentActivity();
            
        } catch (error) {
            console.error('대시보드 데이터 로드 실패:', error);
            this.showErrorMessage('데이터 로드 중 오류가 발생했습니다.');
        } finally {
            this.isLoading = false;
            this.hideLoadingStates();
        }
    }

    async loadDashboardStats() {
        try {
            const response = await fetch('/api/dashboard/stats');
            const data = await response.json();
            
            if (data.success) {
                this.updateStatsDisplay(data.data);
            }
        } catch (error) {
            console.error('통계 로드 실패:', error);
        }
    }

    async loadUsers() {
        try {
            const response = await fetch('/api/users');
            const data = await response.json();
            
            if (data.success) {
                this.users = data.data;
                this.renderUserList();
            }
        } catch (error) {
            console.error('사용자 로드 실패:', error);
        }
    }

    async loadSensorData() {
        try {
            // 시뮬레이션 데이터 생성 (실제 API 연동 시 교체)
            const mockData = this.generateMockSensorData();
            this.updateSensorChart(mockData);
        } catch (error) {
            console.error('센서 데이터 로드 실패:', error);
        }
    }

    async loadRecentActivity() {
        try {
            // 시뮬레이션 활동 데이터 생성
            const mockActivities = this.generateMockActivities();
            this.renderRecentActivity(mockActivities);
        } catch (error) {
            console.error('활동 데이터 로드 실패:', error);
        }
    }

    updateStatsDisplay(stats) {
        document.getElementById('total-users').textContent = stats.total_users || 0;
        document.getElementById('active-devices').textContent = stats.active_devices || 0;
        document.getElementById('today-alerts').textContent = stats.today_alerts || 0;
        document.getElementById('crisis-situations').textContent = stats.crisis_situations || 0;
    }

    renderUserList() {
        const userListContainer = document.getElementById('user-list');
        if (!userListContainer) return;

        if (this.users.length === 0) {
            userListContainer.innerHTML = '<p class="text-light text-center">사용자가 없습니다.</p>';
            return;
        }

        const userCards = this.users.slice(0, 5).map(user => `
            <div class="user-card" data-aos="fade-up" data-aos-delay="${Math.random() * 300}">
                <div class="d-flex align-items-center">
                    <div class="flex-shrink-0">
                        <div class="rounded-circle bg-primary d-flex align-items-center justify-content-center" 
                             style="width: 50px; height: 50px;">
                            <i class="bi bi-person text-white"></i>
                        </div>
                    </div>
                    <div class="flex-grow-1 ms-3">
                        <h6 class="text-white mb-1">${user.user_name || 'Unknown'}</h6>
                        <p class="text-light mb-1 small">${user.user_role_kr || user.user_role || 'Unknown'}</p>
                        <p class="text-muted mb-0 small">${user.email || 'No email'}</p>
                    </div>
                    <div class="flex-shrink-0">
                        <button class="btn btn-sm btn-glass user-select-btn" data-user-id="${user.user_id}">
                            <i class="bi bi-eye"></i>
                        </button>
                    </div>
                </div>
            </div>
        `).join('');

        userListContainer.innerHTML = userCards;
    }

    renderRecentActivity(activities) {
        const activityContainer = document.getElementById('recent-activity');
        if (!activityContainer) return;

        const activityItems = activities.map(activity => `
            <div class="d-flex align-items-start mb-3" data-aos="fade-left" data-aos-delay="${Math.random() * 200}">
                <div class="flex-shrink-0 me-3">
                    <div class="rounded-circle d-flex align-items-center justify-content-center" 
                         style="width: 40px; height: 40px; background: ${activity.color};">
                        <i class="bi ${activity.icon} text-white"></i>
                    </div>
                </div>
                <div class="flex-grow-1">
                    <p class="text-white mb-1 small">${activity.description}</p>
                    <p class="text-muted mb-0 small">${activity.time}</p>
                </div>
            </div>
        `).join('');

        activityContainer.innerHTML = activityItems;
    }

    updateSensorChart(data) {
        if (!this.sensorChart) return;

        this.sensorChart.data.labels = data.labels;
        this.sensorChart.data.datasets[0].data = data.temperature;
        this.sensorChart.data.datasets[1].data = data.gas;
        this.sensorChart.data.datasets[2].data = data.noise;

        this.sensorChart.update('active');
    }

    generateMockSensorData() {
        const labels = [];
        const temperature = [];
        const gas = [];
        const noise = [];

        for (let i = 0; i < 24; i++) {
            const hour = new Date(Date.now() - (23 - i) * 60 * 60 * 1000);
            labels.push(hour.getHours() + ':00');
            
            temperature.push(20 + Math.random() * 10);
            gas.push(100 + Math.random() * 200);
            noise.push(30 + Math.random() * 40);
        }

        return { labels, temperature, gas, noise };
    }

    generateMockActivities() {
        const activities = [
            {
                description: '온도 센서 이상 감지',
                time: '2분 전',
                icon: 'bi-thermometer-half',
                color: '#ff6b6b'
            },
            {
                description: '새로운 사용자 등록',
                time: '5분 전',
                icon: 'bi-person-plus',
                color: '#4ecdc4'
            },
            {
                description: '가스 센서 정상화',
                time: '8분 전',
                icon: 'bi-check-circle',
                color: '#45b7d1'
            },
            {
                description: '시스템 백업 완료',
                time: '15분 전',
                icon: 'bi-cloud-check',
                color: '#96ceb4'
            }
        ];

        return activities;
    }

    selectUser(userId) {
        // 사용자 선택 시 상세 정보 표시
        console.log('사용자 선택:', userId);
        
        // 토스트 알림 표시
        this.showToast(`사용자 ID: ${userId} 선택됨`, 'info');
    }

    refreshDashboard() {
        this.loadDashboardData();
        this.showToast('대시보드 새로고침 완료', 'success');
    }

    startRealTimeUpdates() {
        // 30초마다 데이터 업데이트
        setInterval(() => {
            if (!this.isLoading) {
                this.loadDashboardStats();
            }
        }, 30000);

        // 5분마다 센서 데이터 업데이트
        setInterval(() => {
            if (!this.isLoading) {
                this.loadSensorData();
            }
        }, 300000);
    }

    showLoadingStates() {
        // 로딩 상태 표시
        const loadingElements = document.querySelectorAll('.loading-skeleton');
        loadingElements.forEach(el => el.style.display = 'block');
    }

    hideLoadingStates() {
        // 로딩 상태 숨김
        const loadingElements = document.querySelectorAll('.loading-skeleton');
        loadingElements.forEach(el => el.style.display = 'none');
    }

    showToast(message, type = 'info') {
        // 토스트 알림 표시
        const toastContainer = document.getElementById('toast-container') || this.createToastContainer();
        
        const toast = document.createElement('div');
        toast.className = `toast align-items-center text-white bg-${type} border-0`;
        toast.setAttribute('role', 'alert');
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;
        
        toastContainer.appendChild(toast);
        
        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();
        
        // 자동 제거
        toast.addEventListener('hidden.bs.toast', () => {
            toast.remove();
        });
    }

    createToastContainer() {
        const container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'toast-container position-fixed top-0 end-0 p-3';
        container.style.cssText = 'z-index: 1055;';
        document.body.appendChild(container);
        return container;
    }

    showErrorMessage(message) {
        this.showToast(message, 'danger');
    }
}

// 대시보드 초기화
document.addEventListener('DOMContentLoaded', () => {
    new ModernDashboard();
});

// 페이지 가시성 변경 시 데이터 새로고침
document.addEventListener('visibilitychange', () => {
    if (!document.hidden) {
        // 페이지가 다시 보일 때 데이터 새로고침
        setTimeout(() => {
            if (window.dashboard) {
                window.dashboard.refreshDashboard();
            }
        }, 1000);
    }
});


