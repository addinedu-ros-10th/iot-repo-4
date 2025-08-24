import '../sources/api_service.dart';
import '../dtos/home_state_snapshot_dto.dart';

/// 홈 상태 스냅샷 관련 API 호출을 담당하는 서비스 클래스
class HomeStateSnapshotService {
  final ApiService _apiService;
  
  HomeStateSnapshotService(this._apiService);
  
  /// 특정 사용자의 홈 상태 스냅샷 목록 조회
  Future<HomeStateSnapshotListResponseDto> getUserSnapshots({
    required String userId,
    int page = 1,
    int size = 100,
    DateTime? since,
    DateTime? until,
  }) async {
    try {
      final queryParams = <String, dynamic>{
        'user_id': userId,
        'page': page,
        'size': size,
      };
      
      if (since != null) {
        queryParams['since'] = since.toIso8601String();
      }
      
      if (until != null) {
        queryParams['until'] = until.toIso8601String();
      }
      
      final response = await _apiService.get<Map<String, dynamic>>(
        '/api/home-state-snapshots',
        queryParameters: queryParams,
      );
      
      return HomeStateSnapshotListResponseDto.fromJson(response.data!);
    } catch (e) {
      throw Exception('홈 상태 스냅샷 조회 실패: ${_apiService.handleError(e)}');
    }
  }
  
  /// 최신 홈 상태 스냅샷 조회
  Future<HomeStateSnapshotDto?> getLatestSnapshot(String userId) async {
    try {
      final response = await _apiService.get<Map<String, dynamic>>(
        '/api/home-state-snapshots/latest/$userId',
      );
      
      if (response.data == null) return null;
      return HomeStateSnapshotDto.fromJson(response.data!);
    } catch (e) {
      throw Exception('최신 스냅샷 조회 실패: ${_apiService.handleError(e)}');
    }
  }
  
  /// 경보 수준별 스냅샷 조회
  Future<List<HomeStateSnapshotDto>> getSnapshotsByAlertLevel({
    required String userId,
    required String alertLevel,
    int limit = 50,
  }) async {
    try {
      final response = await _apiService.get<List<dynamic>>(
        '/api/home-state-snapshots/alert-level/$alertLevel',
        queryParameters: {
          'user_id': userId,
          'limit': limit,
        },
      );
      
      return (response.data ?? [])
          .map((snapshot) => HomeStateSnapshotDto.fromJson(snapshot))
          .toList();
    } catch (e) {
      throw Exception('경보 수준별 스냅샷 조회 실패: ${_apiService.handleError(e)}');
    }
  }
  
  /// 특정 시간 범위의 스냅샷 조회
  Future<List<HomeStateSnapshotDto>> getSnapshotsByTimeRange({
    required String userId,
    required DateTime startTime,
    required DateTime endTime,
    int limit = 1000,
  }) async {
    try {
      final response = await _apiService.get<List<dynamic>>(
        '/api/home-state-snapshots/time-range',
        queryParameters: {
          'user_id': userId,
          'start_time': startTime.toIso8601String(),
          'end_time': endTime.toIso8601String(),
          'limit': limit,
        },
      );
      
      return (response.data ?? [])
          .map((snapshot) => HomeStateSnapshotDto.fromJson(snapshot))
          .toList();
    } catch (e) {
      throw Exception('시간 범위별 스냅샷 조회 실패: ${_apiService.handleError(e)}');
    }
  }
  
  /// 센서별 데이터 조회
  Future<List<HomeStateSnapshotDto>> getSnapshotsBySensor({
    required String userId,
    required String sensorType,
    int limit = 100,
  }) async {
    try {
      final response = await _apiService.get<List<dynamic>>(
        '/api/home-state-snapshots/sensor/$sensorType',
        queryParameters: {
          'user_id': userId,
          'limit': limit,
        },
      );
      
      return (response.data ?? [])
          .map((snapshot) => HomeStateSnapshotDto.fromJson(snapshot))
          .toList();
    } catch (e) {
      throw Exception('센서별 스냅샷 조회 실패: ${_apiService.handleError(e)}');
    }
  }
  
  /// 경보 통계 조회
  Future<Map<String, int>> getAlertStatistics(String userId) async {
    try {
      // 각 경보 수준별로 개별 조회하여 통계 생성
      final normalSnapshots = await _apiService.get<List<dynamic>>(
        '/api/home-state-snapshots/alert-level/$userId/Normal',
        queryParameters: {
          'limit': 1000, // 충분히 큰 값으로 설정
        },
      );
      
      final attentionSnapshots = await _apiService.get<List<dynamic>>(
        '/api/home-state-snapshots/alert-level/$userId/Attention',
        queryParameters: {
          'limit': 1000,
        },
      );
      
      final warningSnapshots = await _apiService.get<List<dynamic>>(
        '/api/home-state-snapshots/alert-level/$userId/Warning',
        queryParameters: {
          'limit': 1000,
        },
      );
      
      final emergencySnapshots = await _apiService.get<List<dynamic>>(
        '/api/home-state-snapshots/alert-level/$userId/Emergency',
        queryParameters: {
          'limit': 1000,
        },
      );
      
      return {
        'normal': normalSnapshots.data?.length ?? 0,
        'attention': attentionSnapshots.data?.length ?? 0,
        'warning': warningSnapshots.data?.length ?? 0,
        'emergency': emergencySnapshots.data?.length ?? 0,
      };
    } catch (e) {
      throw Exception('경보 통계 조회 실패: ${_apiService.handleError(e)}');
    }
  }
  
  /// 활동 패턴 분석
  Future<Map<String, dynamic>> getActivityPattern({
    required String userId,
    required DateTime startDate,
    required DateTime endDate,
  }) async {
    try {
      final response = await _apiService.get<Map<String, dynamic>>(
        '/api/home-state-snapshots/activity-pattern',
        queryParameters: {
          'user_id': userId,
          'start_date': startDate.toIso8601String().split('T')[0],
          'end_date': endDate.toIso8601String().split('T')[0],
        },
      );
      
      return response.data!;
    } catch (e) {
      throw Exception('활동 패턴 분석 실패: ${_apiService.handleError(e)}');
    }
  }
  
  /// 실시간 모니터링을 위한 최근 스냅샷들 조회
  Future<List<HomeStateSnapshotDto>> getRecentSnapshotsForMonitoring({
    required String userId,
    int limit = 10,
  }) async {
    try {
      // 경로 충돌 문제로 인해 /latest/{userId} 엔드포인트를 사용
      // 최신 스냅샷을 여러 번 조회하여 데이터 수집
      final snapshots = <HomeStateSnapshotDto>[];
      
      // 최신 스냅샷부터 시작하여 limit만큼 수집
      for (int i = 0; i < limit; i++) {
        try {
          final response = await _apiService.get<Map<String, dynamic>>(
            '/api/home-state-snapshots/latest/$userId',
          );
          
          if (response.data != null) {
            final snapshot = HomeStateSnapshotDto.fromJson(response.data!);
            snapshots.add(snapshot);
            
            // 다음 조회를 위해 시간을 조금 앞으로 이동
            // 실제로는 백엔드에서 페이지네이션을 제공해야 함
            if (snapshots.length >= limit) break;
          }
        } catch (e) {
          // 개별 조회 실패 시 로그만 남기고 계속 진행
          print('스냅샷 조회 실패: $e');
          break;
        }
      }
      
      // 시간순으로 정렬하고 limit만큼 반환
      snapshots.sort((a, b) => b.time.compareTo(a.time));
      return snapshots.take(limit).toList();
    } catch (e) {
      throw Exception('최근 스냅샷 조회 실패: ${_apiService.handleError(e)}');
    }
  }
  
  /// 위험 상태 스냅샷 조회 (Emergency, Warning)
  Future<List<HomeStateSnapshotDto>> getDangerSnapshots({
    required String userId,
    int limit = 20,
  }) async {
    try {
      // Warning과 Emergency 레벨의 스냅샷을 조회
      final warningSnapshots = await _apiService.get<List<dynamic>>(
        '/api/home-state-snapshots/alert-level/$userId/Warning',
        queryParameters: {
          'limit': limit ~/ 2,
        },
      );
      
      final emergencySnapshots = await _apiService.get<List<dynamic>>(
        '/api/home-state-snapshots/alert-level/$userId/Emergency',
        queryParameters: {
          'limit': limit ~/ 2,
        },
      );
      
      final allSnapshots = <HomeStateSnapshotDto>[];
      
      if (warningSnapshots.data != null) {
        allSnapshots.addAll(
          warningSnapshots.data!.map((snapshot) => HomeStateSnapshotDto.fromJson(snapshot))
        );
      }
      
      if (emergencySnapshots.data != null) {
        allSnapshots.addAll(
          emergencySnapshots.data!.map((snapshot) => HomeStateSnapshotDto.fromJson(snapshot))
        );
      }
      
      // 시간순으로 정렬하고 limit만큼 반환
      allSnapshots.sort((a, b) => b.time.compareTo(a.time));
      return allSnapshots.take(limit).toList();
    } catch (e) {
      throw Exception('위험 상태 스냅샷 조회 실패: ${_apiService.handleError(e)}');
    }
  }
}
