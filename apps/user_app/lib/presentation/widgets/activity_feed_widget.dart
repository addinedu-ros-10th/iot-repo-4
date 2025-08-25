import 'package:flutter/material.dart';
import '../../config/app_colors.dart';
import '../../data/dtos/home_state_snapshot_dto.dart';

/// 실시간 활동 피드를 표시하는 위젯
class ActivityFeedWidget extends StatelessWidget {
  final List<HomeStateSnapshotDto> snapshots;
  final int maxItems;

  const ActivityFeedWidget({
    super.key,
    required this.snapshots,
    this.maxItems = 10,
  });

  @override
  Widget build(BuildContext context) {
    if (snapshots.isEmpty) {
      return _buildEmptyState();
    }

    final sortedSnapshots = List<HomeStateSnapshotDto>.from(snapshots)
      ..sort((a, b) => b.time.compareTo(a.time)); // 최신순 정렬

    final recentSnapshots = sortedSnapshots.take(maxItems).toList();

    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: AppColors.secondaryBackground,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(
          color: AppColors.surface.withOpacity(0.1),
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(
                Icons.timeline,
                color: AppColors.accentCalm,
                size: 20,
              ),
              const SizedBox(width: 8),
              const Text(
                '실시간 활동 피드',
                style: TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                  color: AppColors.neutralText,
                ),
              ),
              const Spacer(),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                decoration: BoxDecoration(
                  color: AppColors.accentCalm.withOpacity(0.2),
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Text(
                  '${recentSnapshots.length}개',
                  style: TextStyle(
                    fontSize: 12,
                    fontWeight: FontWeight.w500,
                    color: AppColors.accentCalm,
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: 20),
          
          // 활동 목록
          ListView.builder(
            shrinkWrap: true,
            physics: const NeverScrollableScrollPhysics(),
            itemCount: recentSnapshots.length,
            itemBuilder: (context, index) {
              final snapshot = recentSnapshots[index];
              final isLast = index == recentSnapshots.length - 1;
              
              return _buildActivityItem(snapshot, isLast);
            },
          ),
        ],
      ),
    );
  }

  Widget _buildEmptyState() {
    return Container(
      padding: const EdgeInsets.all(24),
      decoration: BoxDecoration(
        color: AppColors.secondaryBackground,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(
          color: AppColors.surface.withOpacity(0.1),
        ),
      ),
      child: Column(
        children: [
          Icon(
            Icons.timeline,
            size: 48,
            color: AppColors.secondaryText.withOpacity(0.5),
          ),
          const SizedBox(height: 16),
          Text(
            '활동 데이터가 없습니다',
            style: TextStyle(
              fontSize: 16,
              color: AppColors.secondaryText,
              fontWeight: FontWeight.w500,
            ),
          ),
          const SizedBox(height: 8),
          Text(
            '센서에서 활동을 감지 중입니다',
            style: TextStyle(
              fontSize: 14,
              color: AppColors.secondaryText.withOpacity(0.7),
            ),
            textAlign: TextAlign.center,
          ),
        ],
      ),
    );
  }

  Widget _buildActivityItem(HomeStateSnapshotDto snapshot, bool isLast) {
    final activities = _extractActivities(snapshot);
    
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        // 타임라인 표시
        Column(
          children: [
            Container(
              width: 12,
              height: 12,
              decoration: BoxDecoration(
                color: _getAlertLevelColor(snapshot.alertLevel),
                shape: BoxShape.circle,
              ),
            ),
            if (!isLast)
              Container(
                width: 2,
                height: 40,
                color: AppColors.surface.withOpacity(0.2),
              ),
          ],
        ),
        
        const SizedBox(width: 16),
        
        // 활동 내용
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // 시간
              Text(
                _formatTime(snapshot.time),
                style: TextStyle(
                  fontSize: 12,
                  color: AppColors.secondaryText,
                  fontWeight: FontWeight.w500,
                ),
              ),
              
              const SizedBox(height: 8),
              
              // 활동 카드
              Container(
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: _getAlertLevelColor(snapshot.alertLevel).withOpacity(0.1),
                  borderRadius: BorderRadius.circular(8),
                  border: Border.all(
                    color: _getAlertLevelColor(snapshot.alertLevel).withOpacity(0.3),
                  ),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    // 경보 수준
                    if (snapshot.alertLevel != null && snapshot.alertLevel != 'Normal')
                      Row(
                        children: [
                          Icon(
                            _getAlertIcon(snapshot.alertLevel),
                            color: _getAlertLevelColor(snapshot.alertLevel),
                            size: 16,
                          ),
                          const SizedBox(width: 6),
                          Text(
                            '${snapshot.alertLevel} 경보',
                            style: TextStyle(
                              fontSize: 12,
                              fontWeight: FontWeight.bold,
                              color: _getAlertLevelColor(snapshot.alertLevel),
                            ),
                          ),
                        ],
                      ),
                    
                    if (snapshot.alertLevel != null && snapshot.alertLevel != 'Normal')
                      const SizedBox(height: 8),
                    
                    // 활동 요약
                    if (activities.isNotEmpty) ...[
                      Text(
                        _getActivitySummary(activities),
                        style: const TextStyle(
                          fontSize: 14,
                          fontWeight: FontWeight.w500,
                          color: AppColors.neutralText,
                        ),
                      ),
                      const SizedBox(height: 8),
                    ],
                    
                    // 상세 활동
                    _buildActivityDetails(activities),
                    
                    // 추가 정보
                    if (snapshot.alertReason != null) ...[
                      const SizedBox(height: 8),
                      Container(
                        padding: const EdgeInsets.all(8),
                        decoration: BoxDecoration(
                          color: AppColors.alertWarning.withOpacity(0.1),
                          borderRadius: BorderRadius.circular(6),
                        ),
                        child: Row(
                          children: [
                            Icon(
                              Icons.info_outline,
                              color: AppColors.alertWarning,
                              size: 14,
                            ),
                            const SizedBox(width: 6),
                            Expanded(
                              child: Text(
                                snapshot.alertReason!,
                                style: TextStyle(
                                  fontSize: 12,
                                  color: AppColors.alertWarning,
                                ),
                              ),
                            ),
                          ],
                        ),
                      ),
                    ],
                  ],
                ),
              ),
            ],
          ),
        ),
      ],
    );
  }

  Widget _buildActivityDetails(List<Map<String, dynamic>> activities) {
    return Column(
      children: activities.map((activity) {
        return Padding(
          padding: const EdgeInsets.only(bottom: 4),
          child: Row(
            children: [
              Icon(
                activity['icon'] as IconData,
                color: activity['color'] as Color,
                size: 14,
              ),
              const SizedBox(width: 6),
              Expanded(
                child: Text(
                  activity['description'] as String,
                  style: TextStyle(
                    fontSize: 12,
                    color: activity['color'] as Color,
                  ),
                ),
              ),
            ],
          ),
        );
      }).toList(),
    );
  }

  // 활동 추출
  List<Map<String, dynamic>> _extractActivities(HomeStateSnapshotDto snapshot) {
    final activities = <Map<String, dynamic>>[];
    
    // 입구 활동
    if (snapshot.entrancePirMotion ?? false) {
      activities.add({
        'icon': Icons.door_front_door,
        'color': AppColors.highlightSuccess,
        'description': '입구에서 움직임 감지',
      });
    }
    
    if (snapshot.entranceRfidStatus != null) {
      activities.add({
        'icon': Icons.credit_card,
        'color': AppColors.accentCalm,
        'description': 'RFID 카드 인식: ${snapshot.entranceRfidStatus}',
      });
    }
    
    // 거실 활동
    if ((snapshot.livingroomPir1Motion ?? false) || (snapshot.livingroomPir2Motion ?? false)) {
      activities.add({
        'icon': Icons.living,
        'color': AppColors.highlightSuccess,
        'description': '거실에서 움직임 감지',
      });
    }
    
    if (snapshot.livingroomSoundDb != null && snapshot.livingroomSoundDb! > 60) {
      activities.add({
        'icon': Icons.volume_up,
        'color': AppColors.alertWarning,
        'description': '거실 소음: ${snapshot.livingroomSoundDb!.toStringAsFixed(1)}dB',
      });
    }
    
    // 주방 활동
    if (snapshot.kitchenPirMotion ?? false) {
      activities.add({
        'icon': Icons.kitchen,
        'color': AppColors.highlightSuccess,
        'description': '주방에서 움직임 감지',
      });
    }
    
    if (snapshot.kitchenMq5GasPpm != null && snapshot.kitchenMq5GasPpm! > 100) {
      activities.add({
        'icon': Icons.air,
        'color': AppColors.alertEmergency,
        'description': '가스 농도 높음: ${snapshot.kitchenMq5GasPpm!.toStringAsFixed(1)}ppm',
      });
    }
    
    // 침실 활동
    if (snapshot.bedroomPirMotion ?? false) {
      activities.add({
        'icon': Icons.bed,
        'color': AppColors.highlightSuccess,
        'description': '침실에서 움직임 감지',
      });
    }
    
    // 화장실 활동
    if (snapshot.bathroomPirMotion ?? false) {
      activities.add({
        'icon': Icons.bathroom,
        'color': AppColors.highlightSuccess,
        'description': '화장실에서 움직임 감지',
      });
    }
    
    if (snapshot.bathroomTempCelsius != null && snapshot.bathroomTempCelsius! > 30) {
      activities.add({
        'icon': Icons.thermostat,
        'color': AppColors.alertWarning,
        'description': '화장실 온도 높음: ${snapshot.bathroomTempCelsius!.toStringAsFixed(1)}°C',
      });
    }
    
    // 버튼 이벤트
    if (snapshot.livingroomButtonState != null && snapshot.livingroomButtonState != 'IDLE') {
      activities.add({
        'icon': Icons.touch_app,
        'color': AppColors.accentCalm,
        'description': '거실 버튼: ${snapshot.livingroomButtonState}',
      });
    }
    
    if (snapshot.kitchenButtonState != null && snapshot.kitchenButtonState != 'IDLE') {
      activities.add({
        'icon': Icons.touch_app,
        'color': AppColors.accentCalm,
        'description': '주방 버튼: ${snapshot.kitchenButtonState}',
      });
    }
    
    return activities;
  }

  String _getActivitySummary(List<Map<String, dynamic>> activities) {
    if (activities.isEmpty) return '활동 없음';
    
    final motionCount = activities.where((a) => a['description'].toString().contains('움직임')).length;
    final alertCount = activities.where((a) => a['color'] == AppColors.alertWarning || a['color'] == AppColors.alertEmergency).length;
    
    if (alertCount > 0) {
      return '$alertCount개 경보 상황 감지';
    } else if (motionCount > 0) {
      return '$motionCount개 구역에서 활동 감지';
    } else {
      return '정상 활동';
    }
  }

  // 유틸리티 메서드들
  String _formatTime(DateTime time) {
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

  IconData _getAlertIcon(String? alertLevel) {
    switch (alertLevel?.toLowerCase()) {
      case 'emergency':
        return Icons.emergency;
      case 'warning':
        return Icons.warning;
      case 'attention':
        return Icons.info;
      case 'normal':
        return Icons.check_circle;
      default:
        return Icons.info;
    }
  }
}
