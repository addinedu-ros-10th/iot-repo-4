import 'package:flutter/foundation.dart';
import '../../data/services/user_service.dart';
import '../../data/dtos/user_dto.dart';
import '../../data/dtos/user_relationship_dto.dart';

/// 돌봄 대상자 데이터를 관리하는 Provider
class CareTargetsProvider extends ChangeNotifier {
  final UserService _userService;
  
  CareTargetsProvider(this._userService);
  
  // 상태 변수들
  List<UserDto> _careTargets = [];
  List<UserRelationshipDto> _relationships = [];
  bool _isLoading = false;
  String? _error;
  
  // Getters
  List<UserDto> get careTargets => _careTargets;
  List<UserRelationshipDto> get relationships => _relationships;
  bool get isLoading => _isLoading;
  String? get error => _error;
  
  /// 돌봄 대상자 목록 로드
  Future<void> loadCareTargets(String userId) async {
    _setLoading(true);
    _clearError();
    
    try {
      // 돌봄 대상자 목록 조회
      final targets = await _userService.getCareTargets(userId);
      
      // 사용자 관계 조회 (돌봄 제공자로서)
      final relationships = await _userService.getUserRelationshipsAsSubject(userId);
      
      _careTargets = targets;
      _relationships = relationships;
      
      if (kDebugMode) {
        print('✅ 돌봄 대상자 ${targets.length}명 로드 완료');
        print('✅ 사용자 관계 ${relationships.length}개 로드 완료');
      }
    } catch (e) {
      _setError('돌봄 대상자 목록 로드 실패: $e');
      if (kDebugMode) {
        print('❌ 돌봄 대상자 목록 로드 실패: $e');
      }
    } finally {
      _setLoading(false);
    }
  }
  
  /// 특정 돌봄 대상자 정보 로드
  Future<UserDto?> loadCareTarget(String targetId) async {
    try {
      final target = await _userService.getUserById(targetId);
      
      // 기존 목록에 없으면 추가
      if (!_careTargets.any((t) => t.userId == targetId)) {
        _careTargets.add(target);
        notifyListeners();
      }
      
      return target;
    } catch (e) {
      _setError('돌봄 대상자 정보 로드 실패: $e');
      return null;
    }
  }
  
  /// 돌봄 대상자 프로필 정보 로드
  Future<void> loadCareTargetProfile(String targetId) async {
    try {
      final profile = await _userService.getUserProfile(targetId);
      
      if (kDebugMode) {
        print('✅ 돌봄 대상자 프로필 로드 완료: ${profile.userId}');
      }
    } catch (e) {
      if (kDebugMode) {
        print('⚠️ 돌봄 대상자 프로필 로드 실패: $e');
      }
      // 프로필 로드 실패는 치명적이지 않으므로 에러로 처리하지 않음
    }
  }
  
  /// 돌봄 대상자 검색
  List<UserDto> searchCareTargets(String query) {
    if (query.isEmpty) return _careTargets;
    
    final lowercaseQuery = query.toLowerCase();
    return _careTargets.where((target) {
      return target.userName.toLowerCase().contains(lowercaseQuery) ||
             (target.email?.toLowerCase().contains(lowercaseQuery) ?? false) ||
             (target.phoneNumber?.contains(query) ?? false);
    }).toList();
  }
  
  /// 역할별 돌봄 대상자 필터링
  List<UserDto> getCareTargetsByRole(String role) {
    return _careTargets.where((target) => target.userRole == role).toList();
  }
  
  /// 활성 관계만 필터링
  List<UserRelationshipDto> getActiveRelationships() {
    return _relationships.where((rel) => rel.status == 'active').toList();
  }
  
  /// 특정 유형의 관계만 필터링
  List<UserRelationshipDto> getRelationshipsByType(String type) {
    return _relationships.where((rel) => rel.relationshipType == type).toList();
  }
  
  /// 돌봄 대상자 추가 (새로운 관계 생성 시)
  void addCareTarget(UserDto target) {
    if (!_careTargets.any((t) => t.userId == target.userId)) {
      _careTargets.add(target);
      notifyListeners();
    }
  }
  
  /// 돌봄 대상자 제거
  void removeCareTarget(String targetId) {
    _careTargets.removeWhere((target) => target.userId == targetId);
    _relationships.removeWhere((rel) => rel.targetUserId == targetId);
    notifyListeners();
  }
  
  /// 관계 상태 업데이트
  void updateRelationshipStatus(String relationshipId, String newStatus) {
    final index = _relationships.indexWhere((rel) => rel.relationshipId == relationshipId);
    if (index != -1) {
      // 새로운 상태로 관계 객체 생성 (불변성 유지)
      final oldRel = _relationships[index];
      final newRel = UserRelationshipDto(
        relationshipId: oldRel.relationshipId,
        subjectUserId: oldRel.subjectUserId,
        targetUserId: oldRel.targetUserId,
        relationshipType: oldRel.relationshipType,
        status: newStatus,
        createdAt: oldRel.createdAt,
        updatedAt: DateTime.now(),
      );
      
      _relationships[index] = newRel;
      notifyListeners();
    }
  }
  
  /// 데이터 새로고침
  Future<void> refresh(String userId) async {
    await loadCareTargets(userId);
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
