import 'package:flutter/material.dart';
import '../../config/app_colors.dart';
import '../../data/dtos/home_state_snapshot_dto.dart';

/// 홈 플로어 플랜을 표시하는 위젯
class FloorPlanWidget extends StatelessWidget {
  final HomeStateSnapshotDto? latestSnapshot;
  final VoidCallback? onRoomTap;

  const FloorPlanWidget({
    super.key,
    this.latestSnapshot,
    this.onRoomTap,
  });

  @override
  Widget build(BuildContext context) {
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
                Icons.home,
                color: AppColors.accentCalm,
                size: 20,
              ),
              const SizedBox(width: 8),
              const Text(
                '홈 플로어 플랜',
                style: TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                  color: AppColors.neutralText,
                ),
              ),
              const Spacer(),
              if (latestSnapshot != null)
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                  decoration: BoxDecoration(
                    color: _getAlertLevelColor(latestSnapshot!.alertLevel).withOpacity(0.2),
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: Text(
                    latestSnapshot!.alertLevel ?? 'Normal',
                    style: TextStyle(
                      fontSize: 12,
                      fontWeight: FontWeight.w500,
                      color: _getAlertLevelColor(latestSnapshot!.alertLevel),
                    ),
                  ),
                ),
            ],
          ),
          const SizedBox(height: 20),
          
          // 플로어 플랜 레이아웃
          AspectRatio(
            aspectRatio: 1.2,
            child: Container(
              decoration: BoxDecoration(
                color: AppColors.surface.withOpacity(0.05),
                borderRadius: BorderRadius.circular(12),
                border: Border.all(
                  color: AppColors.surface.withOpacity(0.1),
                ),
              ),
              child: Stack(
                children: [
                  // 입구
                  Positioned(
                    top: 20,
                    left: 50,
                    right: 50,
                    child: _buildRoom(
                      '입구',
                      Icons.door_front_door,
                      _getEntranceStatus(),
                      _getEntranceColor(),
                    ),
                  ),
                  
                  // 거실
                  Positioned(
                    top: 120,
                    left: 20,
                    right: 20,
                    child: _buildRoom(
                      '거실',
                      Icons.living,
                      _getLivingRoomStatus(),
                      _getLivingRoomColor(),
                    ),
                  ),
                  
                  // 주방
                  Positioned(
                    top: 220,
                    left: 20,
                    child: _buildRoom(
                      '주방',
                      Icons.kitchen,
                      _getKitchenStatus(),
                      _getKitchenColor(),
                      width: 80,
                      height: 60,
                    ),
                  ),
                  
                  // 침실
                  Positioned(
                    top: 220,
                    right: 20,
                    child: _buildRoom(
                      '침실',
                      Icons.bed,
                      _getBedroomStatus(),
                      _getBedroomColor(),
                      width: 80,
                      height: 60,
                    ),
                  ),
                  
                  // 화장실
                  Positioned(
                    bottom: 20,
                    left: 50,
                    right: 50,
                    child: _buildRoom(
                      '화장실',
                      Icons.bathroom,
                      _getBathroomStatus(),
                      _getBathroomColor(),
                    ),
                  ),
                  
                  // 센서 상태 표시
                  if (latestSnapshot != null) ...[
                    // 거실 센서
                    if ((latestSnapshot!.livingroomPir1Motion ?? false) || (latestSnapshot!.livingroomPir2Motion ?? false))
                      Positioned(
                        top: 140,
                        left: 40,
                        child: _buildSensorIndicator('PIR', true),
                      ),
                    if (latestSnapshot!.livingroomSoundDb != null && latestSnapshot!.livingroomSoundDb! > 60)
                      Positioned(
                        top: 140,
                        right: 40,
                        child: _buildSensorIndicator('소음', true, color: AppColors.alertWarning),
                      ),
                    
                    // 주방 센서
                    if (latestSnapshot!.kitchenPirMotion ?? false)
                      Positioned(
                        top: 240,
                        left: 30,
                        child: _buildSensorIndicator('PIR', true),
                      ),
                    if (latestSnapshot!.kitchenMq5GasPpm != null && latestSnapshot!.kitchenMq5GasPpm! > 100)
                      Positioned(
                        top: 240,
                        left: 50,
                        child: _buildSensorIndicator('가스', true, color: AppColors.alertEmergency),
                      ),
                    
                    // 침실 센서
                    if (latestSnapshot!.bedroomPirMotion ?? false)
                      Positioned(
                        top: 240,
                        right: 30,
                        child: _buildSensorIndicator('PIR', true),
                      ),
                    
                    // 화장실 센서
                    if (latestSnapshot!.bathroomPirMotion ?? false)
                      Positioned(
                        bottom: 30,
                        left: 60,
                        child: _buildSensorIndicator('PIR', true),
                      ),
                    if (latestSnapshot!.bathroomTempCelsius != null && latestSnapshot!.bathroomTempCelsius! > 30)
                      Positioned(
                        bottom: 30,
                        right: 60,
                        child: _buildSensorIndicator('온도', true, color: AppColors.alertWarning),
                      ),
                  ],
                ],
              ),
            ),
          ),
          
          const SizedBox(height: 16),
          
          // 범례
          _buildLegend(),
        ],
      ),
    );
  }

  Widget _buildRoom(
    String name,
    IconData icon,
    String status,
    Color color, {
    double? width,
    double? height,
  }) {
    return GestureDetector(
      onTap: onRoomTap,
      child: Container(
        width: width ?? 120,
        height: height ?? 80,
        decoration: BoxDecoration(
          color: color.withOpacity(0.1),
          borderRadius: BorderRadius.circular(8),
          border: Border.all(
            color: color.withOpacity(0.3),
            width: 2,
          ),
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              icon,
              color: color,
              size: 24,
            ),
            const SizedBox(height: 4),
            Text(
              name,
              style: TextStyle(
                fontSize: 12,
                fontWeight: FontWeight.w500,
                color: color,
              ),
            ),
            Text(
              status,
              style: TextStyle(
                fontSize: 10,
                color: color.withOpacity(0.8),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildSensorIndicator(String label, bool isActive, {Color? color}) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
      decoration: BoxDecoration(
        color: (color ?? AppColors.highlightSuccess).withOpacity(0.9),
        borderRadius: BorderRadius.circular(8),
        boxShadow: [
          BoxShadow(
            color: (color ?? AppColors.highlightSuccess).withOpacity(0.3),
            blurRadius: 4,
            spreadRadius: 1,
          ),
        ],
      ),
      child: Text(
        label,
        style: TextStyle(
          fontSize: 10,
          fontWeight: FontWeight.bold,
          color: AppColors.surface,
        ),
      ),
    );
  }

  Widget _buildLegend() {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceEvenly,
      children: [
        _buildLegendItem('정상', AppColors.highlightSuccess),
        _buildLegendItem('주의', AppColors.alertAttention),
        _buildLegendItem('경고', AppColors.alertWarning),
        _buildLegendItem('비상', AppColors.alertEmergency),
      ],
    );
  }

  Widget _buildLegendItem(String label, Color color) {
    return Row(
      children: [
        Container(
          width: 12,
          height: 12,
          decoration: BoxDecoration(
            color: color,
            shape: BoxShape.circle,
          ),
        ),
        const SizedBox(width: 4),
        Text(
          label,
          style: TextStyle(
            fontSize: 10,
            color: AppColors.secondaryText,
          ),
        ),
      ],
    );
  }

  // 상태 정보 메서드들
  String _getEntranceStatus() {
    if (latestSnapshot == null) return '대기';
    if (latestSnapshot!.entrancePirMotion ?? false) return '활성';
    if (latestSnapshot!.entranceRfidStatus != null) return 'RFID';
    return '대기';
  }

  Color _getEntranceColor() {
    if (latestSnapshot == null) return AppColors.secondaryText;
    if (latestSnapshot!.entrancePirMotion ?? false) return AppColors.highlightSuccess;
    if (latestSnapshot!.entranceRfidStatus != null) return AppColors.accentCalm;
    return AppColors.secondaryText;
  }

  String _getLivingRoomStatus() {
    if (latestSnapshot == null) return '대기';
    if ((latestSnapshot!.livingroomPir1Motion ?? false) || (latestSnapshot!.livingroomPir2Motion ?? false)) {
      return '활성';
    }
    if (latestSnapshot!.livingroomSoundDb != null && latestSnapshot!.livingroomSoundDb! > 60) {
      return '소음';
    }
    return '정상';
  }

  Color _getLivingRoomColor() {
    if (latestSnapshot == null) return AppColors.secondaryText;
    if ((latestSnapshot!.livingroomPir1Motion ?? false) || (latestSnapshot!.livingroomPir2Motion ?? false)) {
      return AppColors.highlightSuccess;
    }
    if (latestSnapshot!.livingroomSoundDb != null && latestSnapshot!.livingroomSoundDb! > 60) {
      return AppColors.alertWarning;
    }
    return AppColors.accentCalm;
  }

  String _getKitchenStatus() {
    if (latestSnapshot == null) return '대기';
    if (latestSnapshot!.kitchenMq5GasPpm != null && latestSnapshot!.kitchenMq5GasPpm! > 100) {
      return '가스';
    }
    if (latestSnapshot!.kitchenPirMotion ?? false) return '활성';
    return '정상';
  }

  Color _getKitchenColor() {
    if (latestSnapshot == null) return AppColors.secondaryText;
    if (latestSnapshot!.kitchenMq5GasPpm != null && latestSnapshot!.kitchenMq5GasPpm! > 100) {
      return AppColors.alertEmergency;
    }
    if (latestSnapshot!.kitchenPirMotion ?? false) return AppColors.highlightSuccess;
    return AppColors.accentCalm;
  }

  String _getBedroomStatus() {
    if (latestSnapshot == null) return '대기';
    if (latestSnapshot!.bedroomPirMotion ?? false) return '활성';
    return '정상';
  }

  Color _getBedroomColor() {
    if (latestSnapshot == null) return AppColors.secondaryText;
    if (latestSnapshot!.bedroomPirMotion ?? false) return AppColors.highlightSuccess;
    return AppColors.accentCalm;
  }

  String _getBathroomStatus() {
    if (latestSnapshot == null) return '대기';
    if (latestSnapshot!.bathroomTempCelsius != null && latestSnapshot!.bathroomTempCelsius! > 30) {
      return '고온';
    }
    if (latestSnapshot!.bathroomPirMotion ?? false) return '활성';
    return '정상';
  }

  Color _getBathroomColor() {
    if (latestSnapshot == null) return AppColors.secondaryText;
    if (latestSnapshot!.bathroomTempCelsius != null && latestSnapshot!.bathroomTempCelsius! > 30) {
      return AppColors.alertWarning;
    }
    if (latestSnapshot!.bathroomPirMotion ?? false) return AppColors.highlightSuccess;
    return AppColors.accentCalm;
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
}
