import 'package:flutter/foundation.dart';
import '../../data/services/home_state_snapshot_service.dart';
import '../../data/dtos/home_state_snapshot_dto.dart';

/// 홈 상태 스냅샷 데이터를 관리하는 Provider
class HomeStateSnapshotsProvider extends ChangeNotifier {
  final HomeStateSnapshotService _snapshotService;
  
  HomeStateSnapshotsProvider(this._snapshotService);
  
  // 상태 변수들
  List<HomeStateSnapshotDto> _snapshots = [];
  Map<String, int> _alertStatistics = {};
  List<HomeStateSnapshotDto> _dangerSnapshots = [];
  bool _isLoading = false;
  String? _error;
  
  // Getters
  List<HomeStateSnapshotDto> get snapshots => _snapshots;
  Map<String, int> get alertStatistics => _alertStatistics;
  List<HomeStateSnapshotDto> get dangerSnapshots => _dangerSnapshots;
  bool get isLoading => _isLoading;
  String? get error => _error;
  
  /// 사용자의 홈 상태 스냅샷 로드
  Future<void> loadUserSnapshots(String userId) async {
    _setLoading(true);
    _clearError();
    
    try {
      // 최근 스냅샷들 로드
      final recentSnapshots = await _snapshotService.getRecentSnapshotsForMonitoring(
        userId: userId,
        limit: 100,
      );
      
      // 경보 통계 로드
      final alertStats = await _snapshotService.getAlertStatistics(userId);
      
      // 위험 상태 스냅샷 로드
      final dangerSnapshots = await _snapshotService.getDangerSnapshots(
        userId: userId,
        limit: 20,
      );
      
      _snapshots = recentSnapshots;
      _alertStatistics = alertStats;
      _dangerSnapshots = dangerSnapshots;
      
      if (kDebugMode) {
        print('✅ 홈 상태 스냅샷 ${recentSnapshots.length}개 로드 완료');
        print('✅ 경보 통계: $alertStats');
        print('✅ 위험 상태 스냅샷 ${dangerSnapshots.length}개 로드 완료');
      }
    } catch (e) {
      _setError('홈 상태 스냅샷 로드 실패: $e');
      if (kDebugMode) {
        print('❌ 홈 상태 스냅샷 로드 실패: $e');
      }
    } finally {
      _setLoading(false);
    }
  }
  
  /// 특정 시간 범위의 스냅샷 로드
  Future<void> loadSnapshotsByTimeRange({
    required String userId,
    required DateTime startTime,
    required DateTime endTime,
  }) async {
    _setLoading(true);
    _clearError();
    
    try {
      final snapshots = await _snapshotService.getSnapshotsByTimeRange(
        userId: userId,
        startTime: startTime,
        endTime: endTime,
      );
      
      _snapshots = snapshots;
      
      if (kDebugMode) {
        print('✅ 시간 범위별 스냅샷 ${snapshots.length}개 로드 완료');
      }
    } catch (e) {
      _setError('시간 범위별 스냅샷 로드 실패: $e');
    } finally {
      _setLoading(false);
    }
  }
  
  /// 경보 수준별 스냅샷 로드
  Future<void> loadSnapshotsByAlertLevel({
    required String userId,
    required String alertLevel,
  }) async {
    _setLoading(true);
    _clearError();
    
    try {
      final snapshots = await _snapshotService.getSnapshotsByAlertLevel(
        userId: userId,
        alertLevel: alertLevel,
      );
      
      _snapshots = snapshots;
      
      if (kDebugMode) {
        print('✅ $alertLevel 경보 스냅샷 ${snapshots.length}개 로드 완료');
      }
    } catch (e) {
      _setError('경보 수준별 스냅샷 로드 실패: $e');
    } finally {
      _setLoading(false);
    }
  }
  
  /// 센서별 데이터 로드
  Future<void> loadSnapshotsBySensor({
    required String userId,
    required String sensorType,
  }) async {
    _setLoading(true);
    _clearError();
    
    try {
      final snapshots = await _snapshotService.getSnapshotsBySensor(
        userId: userId,
        sensorType: sensorType,
      );
      
      _snapshots = snapshots;
      
      if (kDebugMode) {
        print('✅ $sensorType 센서 스냅샷 ${snapshots.length}개 로드 완료');
      }
    } catch (e) {
      _setError('센서별 스냅샷 로드 실패: $e');
    } finally {
      _setLoading(false);
    }
  }
  
  /// 활동 패턴 분석 로드
  Future<Map<String, dynamic>?> loadActivityPattern({
    required String userId,
    required DateTime startDate,
    required DateTime endDate,
  }) async {
    try {
      final pattern = await _snapshotService.getActivityPattern(
        userId: userId,
        startDate: startDate,
        endDate: endDate,
      );
      
      if (kDebugMode) {
        print('✅ 활동 패턴 분석 완료');
      }
      
      return pattern;
    } catch (e) {
      _setError('활동 패턴 분석 실패: $e');
      return null;
    }
  }
  
  /// 최신 스냅샷 가져오기
  Future<HomeStateSnapshotDto?> getLatestSnapshot(String userId) async {
    try {
      final latest = await _snapshotService.getLatestSnapshot(userId);
      
      if (latest != null && _snapshots.isNotEmpty) {
        // 최신 스냅샷이 기존 목록에 없으면 맨 앞에 추가
        if (_snapshots.first.time != latest.time) {
          _snapshots.insert(0, latest);
          notifyListeners();
        }
      }
      
      return latest;
    } catch (e) {
      if (kDebugMode) {
        print('⚠️ 최신 스냅샷 조회 실패: $e');
      }
      return null;
    }
  }
  
  /// 스냅샷 검색
  List<HomeStateSnapshotDto> searchSnapshots(String query) {
    if (query.isEmpty) return _snapshots;
    
    final lowercaseQuery = query.toLowerCase();
    return _snapshots.where((snapshot) {
      return snapshot.detectedActivity?.toLowerCase().contains(lowercaseQuery) == true ||
             snapshot.alertReason?.toLowerCase().contains(lowercaseQuery) == true ||
             snapshot.sensorSummary.toLowerCase().contains(lowercaseQuery) ||
             snapshot.environmentSummary.toLowerCase().contains(lowercaseQuery);
    }).toList();
  }
  
  /// 경보 수준별 스냅샷 필터링
  List<HomeStateSnapshotDto> getSnapshotsByAlertLevel(String alertLevel) {
    return _snapshots.where((snapshot) => 
      snapshot.alertLevel?.toLowerCase() == alertLevel.toLowerCase()
    ).toList();
  }
  
  /// 위험 상태 스냅샷만 필터링
  List<HomeStateSnapshotDto> getDangerSnapshots() {
    return _snapshots.where((snapshot) => snapshot.isInDanger).toList();
  }
  
  /// 주의가 필요한 스냅샷만 필터링
  List<HomeStateSnapshotDto> getAttentionSnapshots() {
    return _snapshots.where((snapshot) => snapshot.needsAttention).toList();
  }
  
  /// 정상 상태 스냅샷만 필터링
  List<HomeStateSnapshotDto> getNormalSnapshots() {
    return _snapshots.where((snapshot) => snapshot.isNormal).toList();
  }
  
  /// 비활성 상태 스냅샷만 필터링
  List<HomeStateSnapshotDto> getInactiveSnapshots() {
    return _snapshots.where((snapshot) => snapshot.isInactive).toList();
  }
  
  /// 센서별 활성 상태 요약
  Map<String, bool> getSensorActivitySummary() {
    if (_snapshots.isEmpty) return {};
    
    final latest = _snapshots.first;
    return {
      'entrance': latest.entrancePirMotion ?? false,
      'livingroom': (latest.livingroomPir1Motion ?? false) || (latest.livingroomPir2Motion ?? false),
      'kitchen': latest.kitchenPirMotion ?? false,
      'bedroom': latest.bedroomPirMotion ?? false,
      'bathroom': latest.bathroomPirMotion ?? false,
    };
  }
  
  /// 환경 데이터 요약
  Map<String, double?> getEnvironmentSummary() {
    if (_snapshots.isEmpty) return {};
    
    final latest = _snapshots.first;
    return {
      'livingroom_sound': latest.livingroomSoundDb,
      'kitchen_gas': latest.kitchenMq5GasPpm,
      'bathroom_temp': latest.bathroomTempCelsius,
    };
  }
  
  /// 데이터 새로고침
  Future<void> refresh(String userId) async {
    await loadUserSnapshots(userId);
  }
  
  /// 에러 초기화
  void clearError() {
    _clearError();
  }
  
  // Private methods
  void _setLoading(bool loading) {
    _isLoading = loading;
    notifyListeners();
  }
  
  void _setError(String error) {
    _error = error;
    notifyListeners();
  }
  
  void _clearError() {
    _error = null;
  }
}
