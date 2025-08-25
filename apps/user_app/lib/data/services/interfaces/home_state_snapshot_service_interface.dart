import '../../dtos/home_state_snapshot_dto.dart';

/// 홈 상태 스냅샷 서비스 인터페이스
abstract class HomeStateSnapshotServiceInterface {
  /// 특정 사용자의 홈 상태 스냅샷 목록 조회
  Future<HomeStateSnapshotListResponseDto> getUserSnapshots({
    required String userId,
    int page = 1,
    int size = 100,
    DateTime? since,
    DateTime? until,
  });

  /// 최신 홈 상태 스냅샷 조회
  Future<HomeStateSnapshotDto?> getLatestSnapshot(String userId);

  /// 경보 수준별 스냅샷 조회
  Future<List<HomeStateSnapshotDto>> getSnapshotsByAlertLevel({
    required String userId,
    required String alertLevel,
    int limit = 50,
  });

  /// 특정 시간 범위의 스냅샷 조회
  Future<List<HomeStateSnapshotDto>> getSnapshotsByTimeRange({
    required String userId,
    required DateTime startTime,
    required DateTime endTime,
    int limit = 1000,
  });

  /// 모니터링용 최근 스냅샷 조회
  Future<List<HomeStateSnapshotDto>> getRecentSnapshotsForMonitoring(String userId);

  /// 경보 통계 조회
  Future<Map<String, int>> getAlertStatistics(String userId);

  /// 활동 피드 조회
  Future<List<Map<String, dynamic>>> getActivityFeed(String userId);

  /// KPI 데이터 조회
  Future<Map<String, dynamic>> getKPIData(String userId);

  /// 위험 상태 스냅샷 조회
  Future<List<HomeStateSnapshotDto>> getDangerSnapshots({
    required String userId,
    int limit = 20,
  });

  /// 센서별 스냅샷 조회
  Future<List<HomeStateSnapshotDto>> getSnapshotsBySensor({
    required String userId,
    required String sensorType,
    int limit = 50,
  });

  /// 활동 패턴 조회
  Future<Map<String, dynamic>> getActivityPattern({
    required String userId,
    required DateTime startTime,
    required DateTime endTime,
  });
}
