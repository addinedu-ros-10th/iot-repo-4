import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../widgets/kpi_card.dart';
import '../widgets/floor_plan_widget.dart';
import '../widgets/sensor_chart_widget.dart';
import '../widgets/activity_feed_widget.dart';
import '../state/care_targets_provider.dart';
import '../state/home_state_snapshots_provider.dart';
import '../../config/app_colors.dart';
import '../../data/dtos/user_dto.dart';
import '../../data/dtos/home_state_snapshot_dto.dart';

/// 전체 돌봄 대상자 대시보드 페이지
class GlobalDashboardPage extends StatefulWidget {
  const GlobalDashboardPage({super.key});

  @override
  State<GlobalDashboardPage> createState() => _GlobalDashboardPageState();
}

class _GlobalDashboardPageState extends State<GlobalDashboardPage> {
  // 개발용 테스트 사용자 ID (실제로는 로그인된 사용자 ID 사용)
  static const String _testUserId = '97928195-2dc7-46ba-b550-c11558d4b93d';
  
  @override
  void initState() {
    super.initState();
    // 페이지 로드 시 데이터 로드
    WidgetsBinding.instance.addPostFrameCallback((_) {
      final careTargetsProvider = context.read<CareTargetsProvider>();
      final snapshotsProvider = context.read<HomeStateSnapshotsProvider>();
      
      careTargetsProvider.loadCareTargets(_testUserId);
      snapshotsProvider.loadUserSnapshots(_testUserId);
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.primaryBackground,
      appBar: AppBar(
        title: const Text(
          'IoT Care 대시보드',
          style: TextStyle(
            color: AppColors.neutralText,
            fontWeight: FontWeight.bold,
          ),
        ),
        backgroundColor: AppColors.secondaryBackground,
        elevation: 0,
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh, color: AppColors.neutralText),
            onPressed: () => _refreshData(),
          ),
          IconButton(
            icon: const Icon(Icons.settings, color: AppColors.neutralText),
            onPressed: () => _navigateToAlertSettings(),
          ),
        ],
      ),
      body: RefreshIndicator(
        onRefresh: () => _refreshData(),
        child: SingleChildScrollView(
          physics: const AlwaysScrollableScrollPhysics(),
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              _buildWelcomeSection(),
              const SizedBox(height: 24),
              _buildKpiSection(),
              const SizedBox(height: 24),
              _buildQuickActionsSection(),
              const SizedBox(height: 24),
              _buildCareTargetsSection(),
              const SizedBox(height: 24),
              _buildVisualizationSection(),
              const SizedBox(height: 24),
              _buildHomeStateSnapshotsSection(),
              const SizedBox(height: 24),
              _buildRecentActivitySection(),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildWelcomeSection() {
    return Consumer2<CareTargetsProvider, HomeStateSnapshotsProvider>(
      builder: (context, careTargetsProvider, snapshotsProvider, child) {
        final careTargetsCount = careTargetsProvider.careTargets.length;
        final activeRelationships = careTargetsProvider.getActiveRelationships().length;
        
        return Container(
          padding: const EdgeInsets.all(20),
          decoration: BoxDecoration(
            gradient: LinearGradient(
              colors: AppColors.primaryGradient,
              begin: Alignment.topLeft,
              end: Alignment.bottomRight,
            ),
            borderRadius: BorderRadius.circular(16),
          ),
          child: Row(
            children: [
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      '안녕하세요! 👋',
                      style: TextStyle(
                        fontSize: 24,
                        fontWeight: FontWeight.bold,
                        color: AppColors.neutralText,
                      ),
                    ),
                    const SizedBox(height: 8),
                    const Text(
                      '오늘도 안전한 돌봄 서비스를 제공해주세요',
                      style: TextStyle(
                        fontSize: 16,
                        color: AppColors.secondaryText,
                      ),
                    ),
                    const SizedBox(height: 16),
                    Row(
                      children: [
                        _buildStatItem('총 대상자', '$careTargetsCount', Icons.people, AppColors.accentCalm),
                        const SizedBox(width: 24),
                        _buildStatItem('활성 관계', '$activeRelationships', Icons.link, AppColors.highlightSuccess),
                      ],
                    ),
                  ],
                ),
              ),
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: AppColors.surface.withOpacity(0.1),
                  borderRadius: BorderRadius.circular(12),
                ),
                child: const Icon(
                  Icons.dashboard,
                  size: 48,
                  color: AppColors.neutralText,
                ),
              ),
            ],
          ),
        );
      },
    );
  }

  Widget _buildStatItem(String label, String value, IconData icon, Color color) {
    return Row(
      children: [
        Container(
          padding: const EdgeInsets.all(8),
          decoration: BoxDecoration(
            color: color.withOpacity(0.2),
            borderRadius: BorderRadius.circular(8),
          ),
          child: Icon(icon, color: color, size: 20),
        ),
        const SizedBox(width: 8),
        Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              value,
              style: const TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
                color: AppColors.neutralText,
              ),
            ),
            Text(
              label,
              style: const TextStyle(
                fontSize: 12,
                color: AppColors.secondaryText,
              ),
            ),
          ],
        ),
      ],
    );
  }

  Widget _buildKpiSection() {
    return Consumer<HomeStateSnapshotsProvider>(
      builder: (context, snapshotsProvider, child) {
        final alertStats = snapshotsProvider.alertStatistics;
        
        return Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              '경보 현황',
              style: TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
                color: AppColors.neutralText,
              ),
            ),
            const SizedBox(height: 16),
            GridView.count(
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              crossAxisCount: 2,
              crossAxisSpacing: 16,
              mainAxisSpacing: 16,
              childAspectRatio: 1.5,
              children: [
                AlertLevelKpiCard(
                  alertLevel: 'Normal',
                  count: alertStats['normal'] ?? 0,
                  onTap: () => _showAlertDetails('Normal'),
                ),
                AlertLevelKpiCard(
                  alertLevel: 'Attention',
                  count: alertStats['attention'] ?? 0,
                  onTap: () => _showAlertDetails('Attention'),
                ),
                AlertLevelKpiCard(
                  alertLevel: 'Warning',
                  count: alertStats['warning'] ?? 0,
                  onTap: () => _showAlertDetails('Warning'),
                ),
                AlertLevelKpiCard(
                  alertLevel: 'Emergency',
                  count: alertStats['emergency'] ?? 0,
                  onTap: () => _showAlertDetails('Emergency'),
                ),
              ],
            ),
          ],
        );
      },
    );
  }

  Widget _buildQuickActionsSection() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text(
          '빠른 액션',
          style: TextStyle(
            fontSize: 20,
            fontWeight: FontWeight.bold,
            color: AppColors.neutralText,
          ),
        ),
        const SizedBox(height: 16),
        Row(
          children: [
            Expanded(
              child: _buildActionButton(
                '전체 대상자',
                Icons.people,
                AppColors.accentCalm,
                _navigateToAllTargets,
              ),
            ),
            const SizedBox(width: 16),
            Expanded(
              child: _buildActionButton(
                '경보 설정',
                Icons.notifications,
                AppColors.alertAttention,
                _navigateToAlertSettings,
              ),
            ),
          ],
        ),
        const SizedBox(height: 16),
        Row(
          children: [
            Expanded(
              child: _buildActionButton(
                '스케줄',
                Icons.calendar_today,
                AppColors.highlightSuccess,
                _navigateToSchedule,
              ),
            ),
            const SizedBox(width: 16),
            Expanded(
              child: _buildActionButton(
                '리포트',
                Icons.assessment,
                AppColors.chartAccent,
                _generateReport,
              ),
            ),
          ],
        ),
      ],
    );
  }

  Widget _buildVisualizationSection() {
    return Consumer<HomeStateSnapshotsProvider>(
      builder: (context, provider, child) {
        if (provider.isLoading) {
          return const Center(
            child: CircularProgressIndicator(
              color: AppColors.accentCalm,
            ),
          );
        }

        if (provider.error != null) {
          return Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: AppColors.alertWarning.withOpacity(0.1),
              borderRadius: BorderRadius.circular(12),
              border: Border.all(color: AppColors.alertWarning.withOpacity(0.3)),
            ),
            child: Column(
              children: [
                const Icon(
                  Icons.error_outline,
                  color: AppColors.alertWarning,
                  size: 32,
                ),
                const SizedBox(height: 8),
                Text(
                  '시각화 데이터 로드 실패',
                  style: TextStyle(
                    color: AppColors.alertWarning,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  provider.error!,
                  style: TextStyle(
                    color: AppColors.alertWarning.withOpacity(0.8),
                    fontSize: 12,
                  ),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 12),
                ElevatedButton(
                  onPressed: () => provider.loadUserSnapshots(_testUserId),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: AppColors.alertWarning,
                    foregroundColor: AppColors.surface,
                  ),
                  child: const Text('다시 시도'),
                ),
              ],
            ),
          );
        }

        final snapshots = provider.snapshots;
        final latestSnapshot = snapshots.isNotEmpty ? snapshots.last : null;
        
        return Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              '실시간 모니터링',
              style: TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.bold,
                color: AppColors.neutralText,
              ),
            ),
            const SizedBox(height: 20),
            
            // 플로어 플랜
            FloorPlanWidget(
              latestSnapshot: latestSnapshot,
              onRoomTap: () {
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(
                    content: Text('방 상세 정보 페이지로 이동'),
                    backgroundColor: AppColors.accentCalm,
                  ),
                );
              },
            ),
            
            const SizedBox(height: 24),
            
            // 센서 차트들
            Row(
              children: [
                Expanded(
                  child: SensorChartWidget(
                    snapshots: snapshots,
                    chartType: 'temperature',
                    maxDataPoints: 15,
                  ),
                ),
                const SizedBox(width: 16),
                Expanded(
                  child: SensorChartWidget(
                    snapshots: snapshots,
                    chartType: 'sound',
                    maxDataPoints: 15,
                  ),
                ),
              ],
            ),
            
            const SizedBox(height: 24),
            
            Row(
              children: [
                Expanded(
                  child: SensorChartWidget(
                    snapshots: snapshots,
                    chartType: 'gas',
                    maxDataPoints: 15,
                  ),
                ),
                const SizedBox(width: 16),
                Expanded(
                  child: SensorChartWidget(
                    snapshots: snapshots,
                    chartType: 'motion',
                    maxDataPoints: 15,
                  ),
                ),
              ],
            ),
            
            const SizedBox(height: 24),
            
            // 활동 피드
            ActivityFeedWidget(
              snapshots: snapshots,
              maxItems: 8,
            ),
          ],
        );
      },
    );
  }

  Widget _buildCareTargetsSection() {
    return Consumer<CareTargetsProvider>(
      builder: (context, provider, child) {
        if (provider.isLoading) {
          return const Center(
            child: CircularProgressIndicator(
              color: AppColors.accentCalm,
            ),
          );
        }

        if (provider.error != null) {
          return Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: AppColors.alertWarning.withOpacity(0.1),
              borderRadius: BorderRadius.circular(12),
              border: Border.all(color: AppColors.alertWarning.withOpacity(0.3)),
            ),
            child: Column(
              children: [
                const Icon(
                  Icons.error_outline,
                  color: AppColors.alertWarning,
                  size: 32,
                ),
                const SizedBox(height: 8),
                Text(
                  '데이터 로드 실패',
                  style: TextStyle(
                    color: AppColors.alertWarning,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  provider.error!,
                  style: TextStyle(
                    color: AppColors.alertWarning.withOpacity(0.8),
                    fontSize: 12,
                  ),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 12),
                ElevatedButton(
                  onPressed: () => provider.loadCareTargets(_testUserId),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: AppColors.alertWarning,
                    foregroundColor: AppColors.surface,
                  ),
                  child: const Text('다시 시도'),
                ),
              ],
            ),
          );
        }

        final careTargets = provider.careTargets;
        
        return Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                const Text(
                  '돌봄 대상자',
                  style: TextStyle(
                    fontSize: 20,
                    fontWeight: FontWeight.bold,
                    color: AppColors.neutralText,
                  ),
                ),
                Text(
                  '${careTargets.length}명',
                  style: const TextStyle(
                    fontSize: 16,
                    color: AppColors.secondaryText,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),
            if (careTargets.isEmpty)
              Container(
                padding: const EdgeInsets.all(24),
                decoration: BoxDecoration(
                  color: AppColors.secondaryBackground,
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Column(
                  children: [
                    Icon(
                      Icons.people_outline,
                      size: 48,
                      color: AppColors.secondaryText.withOpacity(0.5),
                    ),
                    const SizedBox(height: 16),
                    Text(
                      '돌봄 대상자가 없습니다',
                      style: TextStyle(
                        fontSize: 16,
                        color: AppColors.secondaryText,
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                    const SizedBox(height: 8),
                    Text(
                      '새로운 돌봄 관계를 설정해주세요',
                      style: TextStyle(
                        fontSize: 14,
                        color: AppColors.secondaryText.withOpacity(0.7),
                      ),
                      textAlign: TextAlign.center,
                    ),
                  ],
                ),
              )
            else
              ListView.builder(
                shrinkWrap: true,
                physics: const NeverScrollableScrollPhysics(),
                itemCount: careTargets.length,
                itemBuilder: (context, index) {
                  final target = careTargets[index];
                  return _buildCareTargetCard(target, provider);
                },
              ),
          ],
        );
      },
    );
  }

  Widget _buildHomeStateSnapshotsSection() {
    return Consumer<HomeStateSnapshotsProvider>(
      builder: (context, provider, child) {
        if (provider.isLoading) {
          return const Center(
            child: CircularProgressIndicator(
              color: AppColors.accentCalm,
            ),
          );
        }

        if (provider.error != null) {
          return Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: AppColors.alertWarning.withOpacity(0.1),
              borderRadius: BorderRadius.circular(12),
              border: Border.all(color: AppColors.alertWarning.withOpacity(0.3)),
            ),
            child: Column(
              children: [
                const Icon(
                  Icons.error_outline,
                  color: AppColors.alertWarning,
                  size: 32,
                ),
                const SizedBox(height: 8),
                Text(
                  '센서 데이터 로드 실패',
                  style: TextStyle(
                    color: AppColors.alertWarning,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  provider.error!,
                  style: TextStyle(
                    color: AppColors.alertWarning.withOpacity(0.8),
                    fontSize: 12,
                  ),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 12),
                ElevatedButton(
                  onPressed: () => provider.loadUserSnapshots(_testUserId),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: AppColors.alertWarning,
                    foregroundColor: AppColors.surface,
                  ),
                  child: const Text('다시 시도'),
                ),
              ],
            ),
          );
        }

        final snapshots = provider.snapshots;
        final dangerSnapshots = provider.dangerSnapshots;
        
        return Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                const Text(
                  '홈 상태 모니터링',
                  style: TextStyle(
                    fontSize: 20,
                    fontWeight: FontWeight.bold,
                    color: AppColors.neutralText,
                  ),
                ),
                Text(
                  '${snapshots.length}개 데이터',
                  style: const TextStyle(
                    fontSize: 16,
                    color: AppColors.secondaryText,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),
            
            // 센서 상태 요약
            if (snapshots.isNotEmpty) ...[
              _buildSensorStatusSummary(provider),
              const SizedBox(height: 16),
            ],
            
            // 위험 상태 스냅샷
            if (dangerSnapshots.isNotEmpty) ...[
              _buildDangerSnapshotsList(dangerSnapshots),
              const SizedBox(height: 16),
            ],
            
            // 최근 스냅샷 목록
            if (snapshots.isNotEmpty)
              _buildRecentSnapshotsList(snapshots.take(5).toList())
            else
              Container(
                padding: const EdgeInsets.all(24),
                decoration: BoxDecoration(
                  color: AppColors.secondaryBackground,
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Column(
                  children: [
                    Icon(
                      Icons.sensors_off,
                      size: 48,
                      color: AppColors.secondaryText.withOpacity(0.5),
                    ),
                    const SizedBox(height: 16),
                    Text(
                      '센서 데이터가 없습니다',
                      style: TextStyle(
                        fontSize: 16,
                        color: AppColors.secondaryText,
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                    const SizedBox(height: 8),
                    Text(
                      'IoT 센서에서 데이터를 수집 중입니다',
                      style: TextStyle(
                        fontSize: 14,
                        color: AppColors.secondaryText.withOpacity(0.7),
                      ),
                      textAlign: TextAlign.center,
                    ),
                  ],
                ),
              ),
          ],
        );
      },
    );
  }

  Widget _buildSensorStatusSummary(HomeStateSnapshotsProvider provider) {
    final sensorActivity = provider.getSensorActivitySummary();
    final environmentData = provider.getEnvironmentSummary();
    
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: AppColors.secondaryBackground,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(
          color: AppColors.surface.withOpacity(0.1),
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            '센서 상태 요약',
            style: TextStyle(
              fontSize: 16,
              fontWeight: FontWeight.bold,
              color: AppColors.neutralText,
            ),
          ),
          const SizedBox(height: 16),
          Row(
            children: [
              Expanded(
                child: _buildSensorStatusItem(
                  '입구',
                  sensorActivity['entrance'] ?? false,
                  Icons.door_front_door,
                ),
              ),
              Expanded(
                child: _buildSensorStatusItem(
                  '거실',
                  sensorActivity['livingroom'] ?? false,
                  Icons.living,
                ),
              ),
              Expanded(
                child: _buildSensorStatusItem(
                  '주방',
                  sensorActivity['kitchen'] ?? false,
                  Icons.kitchen,
                ),
              ),
              Expanded(
                child: _buildSensorStatusItem(
                  '침실',
                  sensorActivity['bedroom'] ?? false,
                  Icons.bed,
                ),
              ),
              Expanded(
                child: _buildSensorStatusItem(
                  '화장실',
                  sensorActivity['bathroom'] ?? false,
                  Icons.bathroom,
                ),
              ),
            ],
          ),
          if (environmentData.values.any((v) => v != null)) ...[
            const SizedBox(height: 16),
            const Divider(color: AppColors.surface),
            const SizedBox(height: 16),
            Row(
              children: [
                if (environmentData['livingroom_sound'] != null)
                  Expanded(
                    child: _buildEnvironmentDataItem(
                      '거실 소음',
                      '${environmentData['livingroom_sound']!.toStringAsFixed(1)}dB',
                      Icons.volume_up,
                      AppColors.accentCalm,
                    ),
                  ),
                if (environmentData['kitchen_gas'] != null)
                  Expanded(
                    child: _buildEnvironmentDataItem(
                      '주방 가스',
                      '${environmentData['kitchen_gas']!.toStringAsFixed(1)}ppm',
                      Icons.air,
                      AppColors.alertWarning,
                    ),
                  ),
                if (environmentData['bathroom_temp'] != null)
                  Expanded(
                    child: _buildEnvironmentDataItem(
                      '화장실 온도',
                      '${environmentData['bathroom_temp']!.toStringAsFixed(1)}°C',
                      Icons.thermostat,
                      AppColors.alertAttention,
                    ),
                  ),
              ],
            ),
          ],
        ],
      ),
    );
  }

  Widget _buildSensorStatusItem(String label, bool isActive, IconData icon) {
    return Column(
      children: [
        Container(
          width: 40,
          height: 40,
          decoration: BoxDecoration(
            color: isActive 
                ? AppColors.highlightSuccess.withOpacity(0.2)
                : AppColors.secondaryText.withOpacity(0.2),
            borderRadius: BorderRadius.circular(20),
          ),
          child: Icon(
            icon,
            color: isActive ? AppColors.highlightSuccess : AppColors.secondaryText,
            size: 20,
          ),
        ),
        const SizedBox(height: 8),
        Text(
          label,
          style: TextStyle(
            fontSize: 12,
            color: isActive ? AppColors.highlightSuccess : AppColors.secondaryText,
            fontWeight: FontWeight.w500,
          ),
        ),
        Text(
          isActive ? '활성' : '비활성',
          style: TextStyle(
            fontSize: 10,
            color: isActive ? AppColors.highlightSuccess : AppColors.secondaryText,
          ),
        ),
      ],
    );
  }

  Widget _buildEnvironmentDataItem(String label, String value, IconData icon, Color color) {
    return Column(
      children: [
        Container(
          width: 40,
          height: 40,
          decoration: BoxDecoration(
            color: color.withOpacity(0.2),
            borderRadius: BorderRadius.circular(20),
          ),
          child: Icon(icon, color: color, size: 20),
        ),
        const SizedBox(height: 8),
        Text(
          label,
          style: TextStyle(
            fontSize: 12,
            color: color,
            fontWeight: FontWeight.w500,
          ),
        ),
        Text(
          value,
          style: TextStyle(
            fontSize: 12,
            color: color,
            fontWeight: FontWeight.bold,
          ),
        ),
      ],
    );
  }

  Widget _buildDangerSnapshotsList(List<HomeStateSnapshotDto> dangerSnapshots) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: AppColors.alertWarning.withOpacity(0.1),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(
          color: AppColors.alertWarning.withOpacity(0.3),
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(
                Icons.warning,
                color: AppColors.alertWarning,
                size: 20,
              ),
              const SizedBox(width: 8),
              Text(
                '위험 상태 감지',
                style: TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.bold,
                  color: AppColors.alertWarning,
                ),
              ),
              const Spacer(),
              Text(
                '${dangerSnapshots.length}건',
                style: TextStyle(
                  fontSize: 14,
                  color: AppColors.alertWarning,
                  fontWeight: FontWeight.w500,
                ),
              ),
            ],
          ),
          const SizedBox(height: 12),
          ListView.builder(
            shrinkWrap: true,
            physics: const NeverScrollableScrollPhysics(),
            itemCount: dangerSnapshots.take(3).length,
            itemBuilder: (context, index) {
              final snapshot = dangerSnapshots[index];
              return _buildDangerSnapshotItem(snapshot);
            },
          ),
        ],
      ),
    );
  }

  Widget _buildDangerSnapshotItem(HomeStateSnapshotDto snapshot) {
    return Container(
      margin: const EdgeInsets.only(bottom: 8),
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: AppColors.alertWarning.withOpacity(0.1),
        borderRadius: BorderRadius.circular(8),
      ),
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.all(6),
            decoration: BoxDecoration(
              color: AppColors.alertWarning.withOpacity(0.2),
              borderRadius: BorderRadius.circular(12),
            ),
            child: Text(
              snapshot.alertLevel ?? 'Unknown',
              style: TextStyle(
                fontSize: 10,
                color: AppColors.alertWarning,
                fontWeight: FontWeight.bold,
              ),
            ),
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  snapshot.alertReason ?? '경보 사유 없음',
                  style: const TextStyle(
                    fontSize: 14,
                    fontWeight: FontWeight.w500,
                    color: AppColors.neutralText,
                  ),
                ),
                if (snapshot.detectedActivity != null) ...[
                  const SizedBox(height: 4),
                  Text(
                    '활동: ${snapshot.detectedActivity}',
                    style: const TextStyle(
                      fontSize: 12,
                      color: AppColors.secondaryText,
                    ),
                  ),
                ],
              ],
            ),
          ),
          Text(
            _formatTimeAgo(snapshot.time),
            style: const TextStyle(
              fontSize: 12,
              color: AppColors.secondaryText,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildRecentSnapshotsList(List<HomeStateSnapshotDto> snapshots) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: AppColors.secondaryBackground,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(
          color: AppColors.surface.withOpacity(0.1),
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            '최근 센서 데이터',
            style: TextStyle(
              fontSize: 16,
              fontWeight: FontWeight.bold,
              color: AppColors.neutralText,
            ),
          ),
          const SizedBox(height: 16),
          ListView.builder(
            shrinkWrap: true,
            physics: const NeverScrollableScrollPhysics(),
            itemCount: snapshots.length,
            itemBuilder: (context, index) {
              final snapshot = snapshots[index];
              return _buildRecentSnapshotItem(snapshot);
            },
          ),
        ],
      ),
    );
  }

  Widget _buildRecentSnapshotItem(HomeStateSnapshotDto snapshot) {
    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: AppColors.surface.withOpacity(0.05),
        borderRadius: BorderRadius.circular(8),
        border: Border.all(
          color: AppColors.surface.withOpacity(0.1),
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Container(
                padding: const EdgeInsets.all(4),
                decoration: BoxDecoration(
                  color: _getAlertLevelColor(snapshot.alertLevel).withOpacity(0.2),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Text(
                  snapshot.alertLevel ?? 'Unknown',
                  style: TextStyle(
                    fontSize: 10,
                    color: _getAlertLevelColor(snapshot.alertLevel),
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
              const Spacer(),
              Text(
                _formatTimeAgo(snapshot.time),
                style: const TextStyle(
                  fontSize: 12,
                  color: AppColors.secondaryText,
                ),
              ),
            ],
          ),
          const SizedBox(height: 8),
          if (snapshot.sensorSummary.isNotEmpty) ...[
            Text(
              '센서: ${snapshot.sensorSummary}',
              style: const TextStyle(
                fontSize: 12,
                color: AppColors.neutralText,
              ),
            ),
            const SizedBox(height: 4),
          ],
          if (snapshot.environmentSummary.isNotEmpty) ...[
            Text(
              '환경: ${snapshot.environmentSummary}',
              style: const TextStyle(
                fontSize: 12,
                color: AppColors.secondaryText,
              ),
            ),
            const SizedBox(height: 4),
          ],
          if (snapshot.detectedActivity != null) ...[
            Text(
              '활동: ${snapshot.detectedActivity}',
              style: const TextStyle(
                fontSize: 12,
                color: AppColors.accentCalm,
                fontWeight: FontWeight.w500,
              ),
            ),
          ],
        ],
      ),
    );
  }

  Widget _buildCareTargetCard(UserDto target, CareTargetsProvider provider) {
    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: AppColors.secondaryBackground,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(
          color: AppColors.surface.withOpacity(0.1),
        ),
      ),
      child: Row(
        children: [
          Container(
            width: 48,
            height: 48,
            decoration: BoxDecoration(
              color: AppColors.accentCalm.withOpacity(0.2),
              borderRadius: BorderRadius.circular(24),
            ),
            child: Icon(
              Icons.person,
              color: AppColors.accentCalm,
              size: 24,
            ),
          ),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  target.userName,
                  style: const TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.bold,
                    color: AppColors.neutralText,
                  ),
                ),
                const SizedBox(height: 4),
                Row(
                  children: [
                    Container(
                      padding: const EdgeInsets.symmetric(
                        horizontal: 8,
                        vertical: 4,
                      ),
                      decoration: BoxDecoration(
                        color: _getRoleColor(target.userRole).withOpacity(0.2),
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: Text(
                        _getRoleDisplayName(target.userRole),
                        style: TextStyle(
                          fontSize: 12,
                          color: _getRoleColor(target.userRole),
                          fontWeight: FontWeight.w500,
                        ),
                      ),
                    ),
                    if (target.email != null) ...[
                      const SizedBox(width: 8),
                      Icon(
                        Icons.email,
                        size: 14,
                        color: AppColors.secondaryText,
                      ),
                      const SizedBox(width: 4),
                      Expanded(
                        child: Text(
                          target.email!,
                          style: const TextStyle(
                            fontSize: 12,
                            color: AppColors.secondaryText,
                          ),
                          overflow: TextOverflow.ellipsis,
                        ),
                      ),
                    ],
                  ],
                ),
              ],
            ),
          ),
          IconButton(
            icon: const Icon(
              Icons.arrow_forward_ios,
              color: AppColors.secondaryText,
              size: 16,
            ),
            onPressed: () => _navigateToTargetDetail(target),
          ),
        ],
      ),
    );
  }

  Widget _buildRecentActivitySection() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text(
          '최근 활동',
          style: TextStyle(
            fontSize: 20,
            fontWeight: FontWeight.bold,
            color: AppColors.neutralText,
          ),
        ),
        const SizedBox(height: 16),
        Container(
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            color: AppColors.secondaryBackground,
            borderRadius: BorderRadius.circular(12),
          ),
          child: Column(
            children: [
              _buildActivityItem(
                '시스템 시작',
                '방금 전',
                Icons.power_settings_new,
                AppColors.highlightSuccess,
              ),
              _buildActivityItem(
                '데이터 동기화 완료',
                '1분 전',
                Icons.sync,
                AppColors.accentCalm,
              ),
              _buildActivityItem(
                '경보 설정 업데이트',
                '5분 전',
                Icons.settings,
                AppColors.alertAttention,
              ),
            ],
          ),
        ),
      ],
    );
  }

  Widget _buildActionButton(
    String label,
    IconData icon,
    Color color,
    VoidCallback onPressed,
  ) {
    return ElevatedButton(
      onPressed: onPressed,
      style: ElevatedButton.styleFrom(
        backgroundColor: color,
        foregroundColor: AppColors.surface,
        padding: const EdgeInsets.symmetric(vertical: 16),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(12),
        ),
      ),
      child: Column(
        children: [
          Icon(icon, size: 24),
          const SizedBox(height: 8),
          Text(
            label,
            style: const TextStyle(
              fontSize: 14,
              fontWeight: FontWeight.w500,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildActivityItem(
    String title,
    String time,
    IconData icon,
    Color color,
  ) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8),
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.all(8),
            decoration: BoxDecoration(
              color: color.withOpacity(0.2),
              borderRadius: BorderRadius.circular(8),
            ),
            child: Icon(icon, color: color, size: 16),
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Text(
              title,
              style: const TextStyle(
                color: AppColors.neutralText,
                fontWeight: FontWeight.w500,
              ),
            ),
          ),
          Text(
            time,
            style: const TextStyle(
              color: AppColors.secondaryText,
              fontSize: 12,
            ),
          ),
        ],
      ),
    );
  }

  // Helper methods
  Color _getRoleColor(String role) {
    switch (role) {
      case 'admin':
        return AppColors.alertEmergency;
      case 'caregiver':
        return AppColors.alertWarning;
      case 'family':
        return AppColors.alertAttention;
      case 'user':
        return AppColors.highlightSuccess;
      default:
        return AppColors.secondaryText;
    }
  }

  String _getRoleDisplayName(String role) {
    switch (role) {
      case 'admin':
        return '관리자';
      case 'caregiver':
        return '돌봄 제공자';
      case 'family':
        return '가족';
      case 'user':
        return '사용자';
      default:
        return role;
    }
  }

  Color _getAlertLevelColor(String? alertLevel) {
    switch (alertLevel?.toLowerCase()) {
      case 'emergency':
        return AppColors.alertEmergency;
      case 'warning':
        return AppColors.alertWarning;
      case 'attention':
        return AppColors.alertAttention;
      case 'normal':
        return AppColors.highlightSuccess;
      default:
        return AppColors.secondaryText;
    }
  }

  String _formatTimeAgo(DateTime time) {
    final now = DateTime.now();
    final difference = now.difference(time);
    
    if (difference.inMinutes < 1) {
      return '방금 전';
    } else if (difference.inMinutes < 60) {
      return '${difference.inMinutes}분 전';
    } else if (difference.inHours < 24) {
      return '${difference.inHours}시간 전';
    } else {
      return '${difference.inDays}일 전';
    }
  }

  // Action methods
  Future<void> _refreshData() async {
    final careTargetsProvider = context.read<CareTargetsProvider>();
    final snapshotsProvider = context.read<HomeStateSnapshotsProvider>();
    
    await Future.wait([
      careTargetsProvider.refresh(_testUserId),
      snapshotsProvider.refresh(_testUserId),
    ]);
  }

  void _showAlertDetails(String alertLevel) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text('$alertLevel 경보 상세 정보'),
        backgroundColor: AppColors.alertWarning,
      ),
    );
  }

  void _navigateToAllTargets() {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(
        content: Text('전체 대상자 페이지로 이동'),
        backgroundColor: AppColors.accentCalm,
      ),
    );
  }

  void _navigateToAlertSettings() {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(
        content: Text('경보 설정 페이지로 이동'),
        backgroundColor: AppColors.alertAttention,
      ),
    );
  }

  void _navigateToSchedule() {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(
        content: Text('스케줄 페이지로 이동'),
        backgroundColor: AppColors.highlightSuccess,
      ),
    );
  }

  void _generateReport() {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(
        content: Text('리포트 생성 중...'),
        backgroundColor: AppColors.chartAccent,
      ),
    );
  }

  void _navigateToTargetDetail(UserDto target) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text('${target.userName} 상세 정보 페이지로 이동'),
        backgroundColor: AppColors.accentCalm,
      ),
    );
  }
}
