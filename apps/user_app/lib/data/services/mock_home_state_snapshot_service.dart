import 'package:user_app/data/dtos/home_state_snapshot_dto.dart';
import 'package:user_app/data/services/mock_data_service.dart';
import 'package:user_app/data/services/interfaces/home_state_snapshot_service_interface.dart';

/// Mock 홈 상태 스냅샷 서비스 - 실제 API 호출 대신 샘플 데이터 제공
class MockHomeStateSnapshotService implements HomeStateSnapshotServiceInterface {
  final MockDataService _mockDataService = MockDataService();

  /// Mock 최근 스냅샷 조회 (모니터링용)
  Future<List<HomeStateSnapshotDto>> getRecentSnapshotsForMonitoring(String userId) async {
    await Future.delayed(const Duration(milliseconds: 600));
    
    return _mockDataService.getMockHomeStateSnapshots();
  }

  /// Mock 경보 수준별 스냅샷 조회
  @override
  Future<List<HomeStateSnapshotDto>> getSnapshotsByAlertLevel({
    required String userId,
    required String alertLevel,
    int limit = 50,
  }) async {
    await Future.delayed(const Duration(milliseconds: 400));
    
    final allSnapshots = _mockDataService.getMockHomeStateSnapshots();
    return allSnapshots.where((snapshot) => 
      snapshot.alertLevel?.toLowerCase() == alertLevel.toLowerCase()
    ).take(limit).toList();
  }

  /// Mock 최신 스냅샷 조회
  Future<HomeStateSnapshotDto?> getLatestSnapshot(String userId) async {
    await Future.delayed(const Duration(milliseconds: 300));
    
    final snapshots = _mockDataService.getMockHomeStateSnapshots();
    if (snapshots.isNotEmpty) {
      return snapshots.first; // 가장 최근 스냅샷
    }
    return null;
  }

  /// Mock 경보 통계 조회
  Future<Map<String, int>> getAlertStatistics(String userId) async {
    await Future.delayed(const Duration(milliseconds: 200));
    
    return _mockDataService.getMockAlertStatistics();
  }

  /// Mock 활동 피드 조회
  Future<List<Map<String, dynamic>>> getActivityFeed(String userId) async {
    await Future.delayed(const Duration(milliseconds: 350));
    
    return _mockDataService.getMockActivityFeed();
  }

  /// Mock KPI 데이터 조회
  Future<Map<String, dynamic>> getKPIData(String userId) async {
    await Future.delayed(const Duration(milliseconds: 250));
    
    return _mockDataService.getMockKPIData();
  }

  // Interface implementation methods
  
  @override
  Future<HomeStateSnapshotListResponseDto> getUserSnapshots({
    required String userId,
    int page = 1,
    int size = 100,
    DateTime? since,
    DateTime? until,
  }) async {
    await Future.delayed(const Duration(milliseconds: 500));
    
    final snapshots = _mockDataService.getMockHomeStateSnapshots();
    List<HomeStateSnapshotDto> filteredSnapshots = snapshots;
    
    if (since != null) {
      filteredSnapshots = filteredSnapshots.where((s) => s.time.isAfter(since)).toList();
    }
    if (until != null) {
      filteredSnapshots = filteredSnapshots.where((s) => s.time.isBefore(until)).toList();
    }
    
    return HomeStateSnapshotListResponseDto(
      snapshots: filteredSnapshots,
      total: filteredSnapshots.length,
      page: page,
      size: size,
    );
  }

  @override
  Future<List<HomeStateSnapshotDto>> getSnapshotsByTimeRange({
    required String userId,
    required DateTime startTime,
    required DateTime endTime,
    int limit = 1000,
  }) async {
    await Future.delayed(const Duration(milliseconds: 400));
    
    final snapshots = _mockDataService.getMockHomeStateSnapshots();
    return snapshots
        .where((s) => s.time.isAfter(startTime) && s.time.isBefore(endTime))
        .take(limit)
        .toList();
  }

  @override
  Future<List<HomeStateSnapshotDto>> getDangerSnapshots({
    required String userId,
    int limit = 20,
  }) async {
    await Future.delayed(const Duration(milliseconds: 350));
    
    final snapshots = _mockDataService.getMockHomeStateSnapshots();
    return snapshots
        .where((s) => s.isInDanger)
        .take(limit)
        .toList();
  }

  @override
  Future<List<HomeStateSnapshotDto>> getSnapshotsBySensor({
    required String userId,
    required String sensorType,
    int limit = 50,
  }) async {
    await Future.delayed(const Duration(milliseconds: 300));
    
    final snapshots = _mockDataService.getMockHomeStateSnapshots();
    // Mock에서는 모든 스냅샷을 반환 (실제로는 센서 타입별 필터링)
    return snapshots.take(limit).toList();
  }

  @override
  Future<Map<String, dynamic>> getActivityPattern({
    required String userId,
    required DateTime startTime,
    required DateTime endTime,
  }) async {
    await Future.delayed(const Duration(milliseconds: 400));
    
    // Mock 활동 패턴 데이터
    return {
      'total_activities': 15,
      'most_active_hour': 14,
      'most_active_location': '거실',
      'average_duration': 45,
      'pattern_type': 'regular',
      'anomalies': 2,
    };
  }
}

