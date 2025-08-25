import 'package:user_app/data/dtos/user_dto.dart';
import 'package:user_app/data/dtos/home_state_snapshot_dto.dart';

/// Mock 데이터 서비스 - 백엔드 API 없이 샘플 데이터 제공
class MockDataService {
  static final MockDataService _instance = MockDataService._internal();
  factory MockDataService() => _instance;
  MockDataService._internal();

  /// Mock 사용자 데이터
  List<UserDto> getMockUsers() {
    return [
      UserDto(
        userId: 'user-001',
        userName: '김철수',
        email: 'kim@example.com',
        phoneNumber: '010-1234-5678',
        userRole: 'caregiver',
        createdAt: DateTime.now().subtract(const Duration(days: 30)),
      ),
      UserDto(
        userId: 'user-002',
        userName: '이영희',
        email: 'lee@example.com',
        phoneNumber: '010-2345-6789',
        userRole: 'caregiver',
        createdAt: DateTime.now().subtract(const Duration(days: 25)),
      ),
      UserDto(
        userId: 'user-003',
        userName: '박민수',
        email: 'park@example.com',
        phoneNumber: '010-3456-7890',
        userRole: 'caregiver',
        createdAt: DateTime.now().subtract(const Duration(days: 20)),
      ),
    ];
  }

  /// Mock 사용자 관계 데이터
  List<Map<String, dynamic>> getMockUserRelationships() {
    return [
      {
        'relationship_id': 'rel-001',
        'subject_user_id': 'user-001',
        'target_user_id': 'user-002',
        'relationship_type': 'family',
        'relationship_name': '딸',
        'created_at': DateTime.now().subtract(const Duration(days: 30)).toIso8601String(),
        'target_user': {
          'user_id': 'user-002',
          'user_name': '이영희',
          'user_role': 'caregiver',
          'email': 'lee@example.com',
          'phone_number': '010-2345-6789',
        }
      },
      {
        'relationship_id': 'rel-002',
        'subject_user_id': 'user-001',
        'target_user_id': 'user-003',
        'relationship_type': 'professional',
        'relationship_name': '돌봄사',
        'created_at': DateTime.now().subtract(const Duration(days: 20)).toIso8601String(),
        'target_user': {
          'user_id': 'user-003',
          'user_name': '박민수',
          'user_role': 'caregiver',
          'email': 'park@example.com',
          'phone_number': '010-3456-7890',
        }
      },
    ];
  }

  /// Mock 홈 상태 스냅샷 데이터
  List<HomeStateSnapshotDto> getMockHomeStateSnapshots() {
    final now = DateTime.now();
    
    return [
      // 최근 스냅샷 (정상 상태)
      HomeStateSnapshotDto(
        time: now.subtract(const Duration(minutes: 5)),
        userId: 'user-001',
        entrancePirMotion: false,
        entranceRfidStatus: 'registered',
        entranceReedIsClosed: true,
        livingroomPir1Motion: false,
        livingroomPir2Motion: false,
        livingroomSoundDb: 35.2,
        livingroomMq7CoPpm: 0.5,
        livingroomButtonState: 'idle',
        kitchenPirMotion: false,
        kitchenSoundDb: 28.7,
        kitchenMq5GasPpm: 0.3,
        kitchenLoadcell1Kg: 0.0,
        kitchenLoadcell2Kg: 0.0,
        kitchenButtonState: 'idle',
        kitchenBuzzerIsOn: false,
        bedroomPirMotion: false,
        bedroomSoundDb: 25.1,
        bedroomMq7CoPpm: 0.4,
        bedroomLoadcellKg: 0.0,
        bedroomButtonState: 'idle',
        bathroomPirMotion: false,
        bathroomSoundDb: 22.3,
        bathroomTempCelsius: 24.5,
        bathroomButtonState: 'idle',
        detectedActivity: 'sleeping',
        alertLevel: 'normal',
        alertReason: '모든 센서가 정상 상태입니다',
        actionLog: {
          'last_activity': '잠자기 시작',
          'last_movement': '침실에서 30분간 정적',
          'environment': '온도 24.5°C, 습도 45%',
        },
        extraData: {
          'battery_level': 85,
          'wifi_strength': 'strong',
          'last_maintenance': '2025-08-20',
        },
      ),
      
      // 주의가 필요한 상태
      HomeStateSnapshotDto(
        time: now.subtract(const Duration(minutes: 15)),
        userId: 'user-001',
        entrancePirMotion: false,
        entranceRfidStatus: 'registered',
        entranceReedIsClosed: true,
        livingroomPir1Motion: false,
        livingroomPir2Motion: false,
        livingroomSoundDb: 45.8,
        livingroomMq7CoPpm: 2.1,
        livingroomButtonState: 'idle',
        kitchenPirMotion: false,
        kitchenSoundDb: 38.2,
        kitchenMq5GasPpm: 1.8,
        kitchenLoadcell1Kg: 0.0,
        kitchenLoadcell2Kg: 0.0,
        kitchenButtonState: 'idle',
        kitchenBuzzerIsOn: false,
        bedroomPirMotion: false,
        bedroomSoundDb: 32.5,
        bedroomMq7CoPpm: 1.2,
        bedroomLoadcellKg: 0.0,
        bedroomButtonState: 'idle',
        bathroomPirMotion: false,
        bathroomSoundDb: 29.7,
        bathroomTempCelsius: 26.8,
        bathroomButtonState: 'idle',
        detectedActivity: 'resting',
        alertLevel: 'attention',
        alertReason: '거실 소음이 평소보다 높고, 일산화탄소 농도가 증가했습니다',
        actionLog: {
          'last_activity': '거실에서 휴식',
          'noise_alert': '소음 45.8dB (평소 35dB)',
          'co_alert': '일산화탄소 2.1ppm (평소 0.5ppm)',
        },
        extraData: {
          'battery_level': 82,
          'wifi_strength': 'strong',
          'ventilation_needed': true,
        },
      ),
      
      // 경고 상태
      HomeStateSnapshotDto(
        time: now.subtract(const Duration(minutes: 30)),
        userId: 'user-001',
        entrancePirMotion: false,
        entranceRfidStatus: 'registered',
        entranceReedIsClosed: true,
        livingroomPir1Motion: false,
        livingroomPir2Motion: false,
        livingroomSoundDb: 52.3,
        livingroomMq7CoPpm: 4.7,
        livingroomButtonState: 'idle',
        kitchenPirMotion: false,
        kitchenSoundDb: 48.9,
        kitchenMq5GasPpm: 3.2,
        kitchenLoadcell1Kg: 0.0,
        kitchenLoadcell2Kg: 0.0,
        kitchenButtonState: 'idle',
        kitchenBuzzerIsOn: false,
        bedroomPirMotion: false,
        bedroomSoundDb: 41.6,
        bedroomMq7CoPpm: 2.8,
        bedroomLoadcellKg: 0.0,
        bedroomButtonState: 'idle',
        bathroomPirMotion: false,
        bathroomSoundDb: 37.4,
        bathroomTempCelsius: 28.9,
        bathroomButtonState: 'idle',
        detectedActivity: 'unknown',
        alertLevel: 'warning',
        alertReason: '일산화탄소 농도가 위험 수준에 근접했습니다. 환기가 필요합니다',
        actionLog: {
          'last_activity': '활동 없음 (30분)',
          'co_warning': '일산화탄소 4.7ppm (위험 수준 5.0ppm)',
          'noise_warning': '소음 52.3dB (평소 35dB)',
          'action_required': '즉시 환기 필요',
        },
        extraData: {
          'battery_level': 78,
          'wifi_strength': 'medium',
          'emergency_contact': '010-1234-5678',
        },
      ),
      
      // 비상 상태
      HomeStateSnapshotDto(
        time: now.subtract(const Duration(minutes: 45)),
        userId: 'user-001',
        entrancePirMotion: false,
        entranceRfidStatus: 'registered',
        entranceReedIsClosed: true,
        livingroomPir1Motion: false,
        livingroomPir2Motion: false,
        livingroomSoundDb: 65.7,
        livingroomMq7CoPpm: 8.9,
        livingroomButtonState: 'idle',
        kitchenPirMotion: false,
        kitchenSoundDb: 58.2,
        kitchenMq5GasPpm: 6.4,
        kitchenLoadcell1Kg: 0.0,
        kitchenLoadcell2Kg: 0.0,
        kitchenButtonState: 'idle',
        kitchenBuzzerIsOn: true,
        bedroomPirMotion: false,
        bedroomSoundDb: 52.8,
        bedroomMq7CoPpm: 5.1,
        bedroomLoadcellKg: 0.0,
        bedroomButtonState: 'idle',
        bathroomPirMotion: false,
        bathroomSoundDb: 48.3,
        bathroomTempCelsius: 31.2,
        bathroomButtonState: 'idle',
        detectedActivity: 'emergency',
        alertLevel: 'emergency',
        alertReason: '일산화탄소 농도가 위험 수준을 초과했습니다. 즉시 대응이 필요합니다!',
        actionLog: {
          'last_activity': '비상 상황 감지',
          'co_emergency': '일산화탄소 8.9ppm (위험 수준 5.0ppm 초과)',
          'noise_emergency': '소음 65.7dB (비정상적으로 높음)',
          'buzzer_activated': '경보음 발생',
          'emergency_response': '비상 연락망에 자동 알림 발송',
        },
        extraData: {
          'battery_level': 75,
          'wifi_strength': 'weak',
          'emergency_contact': '010-1234-5678',
          'fire_department': '119',
          'last_reset': '2025-08-22 14:30:00',
        },
      ),
    ];
  }

  /// Mock 경보 통계 데이터
  Map<String, int> getMockAlertStatistics() {
    return {
      'normal': 12,
      'attention': 3,
      'warning': 2,
      'emergency': 1,
    };
  }

  /// Mock 활동 피드 데이터
  List<Map<String, dynamic>> getMockActivityFeed() {
    final now = DateTime.now();
    
    return [
      {
        'id': 'activity-001',
        'timestamp': now.subtract(const Duration(minutes: 5)),
        'type': 'sensor_alert',
        'title': '정상 상태 확인',
        'description': '모든 센서가 정상 범위 내에서 작동 중입니다',
        'severity': 'info',
        'location': '전체',
      },
      {
        'id': 'activity-002',
        'timestamp': now.subtract(const Duration(minutes: 15)),
        'title': '소음 수준 증가',
        'description': '거실 소음이 평소보다 높게 감지되었습니다 (45.8dB)',
        'severity': 'warning',
        'location': '거실',
      },
      {
        'id': 'activity-003',
        'timestamp': now.subtract(const Duration(minutes: 30)),
        'title': '일산화탄소 농도 경고',
        'description': '일산화탄소 농도가 위험 수준에 근접했습니다 (4.7ppm)',
        'severity': 'warning',
        'location': '거실',
      },
      {
        'id': 'activity-004',
        'timestamp': now.subtract(const Duration(minutes: 45)),
        'title': '비상 상황 발생',
        'description': '일산화탄소 농도가 위험 수준을 초과했습니다 (8.9ppm)',
        'severity': 'critical',
        'location': '거실',
      },
      {
        'id': 'activity-005',
        'timestamp': now.subtract(const Duration(hours: 1)),
        'title': '침실 활동 감지',
        'description': '침실에서 움직임이 감지되었습니다',
        'severity': 'info',
        'location': '침실',
      },
      {
        'id': 'activity-006',
        'timestamp': now.subtract(const Duration(hours: 2)),
        'title': '주방 센서 활성화',
        'description': '주방 모션 센서가 활성화되었습니다',
        'severity': 'info',
        'location': '주방',
      },
    ];
  }

  /// Mock KPI 데이터
  Map<String, dynamic> getMockKPIData() {
    return {
      'total_snapshots': 156,
      'active_sensors': 8,
      'alert_count': 6,
      'last_update': DateTime.now().subtract(const Duration(minutes: 5)),
      'system_health': 'excellent',
      'battery_level': 85,
      'wifi_strength': 'strong',
      'uptime_hours': 720,
    };
  }
}


