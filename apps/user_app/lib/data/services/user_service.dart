import '../sources/api_service.dart';
import '../dtos/user_dto.dart';
import '../dtos/user_relationship_dto.dart';

/// 사용자 관련 API 호출을 담당하는 서비스 클래스
class UserService {
  final ApiService _apiService;
  
  UserService(this._apiService);
  
  /// 모든 사용자 목록 조회
  Future<UserListResponseDto> getAllUsers({
    int page = 1,
    int size = 10,
    String? role,
  }) async {
    try {
      final queryParams = <String, dynamic>{
        'page': page,
        'size': size,
      };
      
      if (role != null) {
        queryParams['role'] = role;
      }
      
      final response = await _apiService.get<Map<String, dynamic>>(
        '/api/users/list',
        queryParameters: queryParams,
      );
      
      return UserListResponseDto.fromJson(response.data!);
    } catch (e) {
      throw Exception('사용자 목록 조회 실패: ${_apiService.handleError(e)}');
    }
  }
  
  /// 특정 사용자 조회
  Future<UserDto> getUserById(String userId) async {
    try {
      final response = await _apiService.get<Map<String, dynamic>>(
        '/api/users/$userId',
      );
      
      return UserDto.fromJson(response.data!);
    } catch (e) {
      throw Exception('사용자 조회 실패: ${_apiService.handleError(e)}');
    }
  }
  
  /// 사용자 생성
  Future<UserDto> createUser({
    required String userName,
    required String userRole,
    String? email,
    String? phoneNumber,
  }) async {
    try {
      final userData = {
        'user_name': userName,
        'user_role': userRole,
        if (email != null) 'email': email,
        if (phoneNumber != null) 'phone_number': phoneNumber,
      };
      
      final response = await _apiService.post<Map<String, dynamic>>(
        '/api/users/create',
        data: userData,
      );
      
      return UserDto.fromJson(response.data!);
    } catch (e) {
      throw Exception('사용자 생성 실패: ${_apiService.handleError(e)}');
    }
  }
  
  /// 사용자 정보 수정
  Future<UserDto> updateUser(
    String userId, {
    String? userName,
    String? userRole,
    String? email,
    String? phoneNumber,
  }) async {
    try {
      final updateData = <String, dynamic>{};
      
      if (userName != null) updateData['user_name'] = userName;
      if (userRole != null) updateData['user_role'] = userRole;
      if (email != null) updateData['email'] = email;
      if (phoneNumber != null) updateData['phone_number'] = phoneNumber;
      
      final response = await _apiService.put<Map<String, dynamic>>(
        '/api/users/$userId',
        data: updateData,
      );
      
      return UserDto.fromJson(response.data!);
    } catch (e) {
      throw Exception('사용자 수정 실패: ${_apiService.handleError(e)}');
    }
  }
  
  /// 사용자 삭제
  Future<void> deleteUser(String userId) async {
    try {
      await _apiService.delete('/api/users/$userId');
    } catch (e) {
      throw Exception('사용자 삭제 실패: ${_apiService.handleError(e)}');
    }
  }
  
  /// 사용자 프로필 조회
  Future<UserProfileDto> getUserProfile(String userId) async {
    try {
      final response = await _apiService.get<Map<String, dynamic>>(
        '/api/user-profiles/$userId',
      );
      
      return UserProfileDto.fromJson(response.data!);
    } catch (e) {
      throw Exception('사용자 프로필 조회 실패: ${_apiService.handleError(e)}');
    }
  }
  
  /// 사용자 관계 조회 (사용자가 주체인 경우)
  Future<List<UserRelationshipDto>> getUserRelationshipsAsSubject(String userId) async {
    try {
      final response = await _apiService.get<List<dynamic>>(
        '/api/user-relationships/user/$userId/as-subject',
      );
      print(response.data);
      return (response.data ?? [])
          .map((rel) => UserRelationshipDto.fromJson(rel))
          .toList();
    } catch (e) {
      throw Exception('사용자 관계 조회 실패: ${_apiService.handleError(e)}');
    }
  }
  
  /// 사용자 관계 조회 (사용자가 대상인 경우)
  Future<List<UserRelationshipDto>> getUserRelationshipsAsTarget(String userId) async {
    try {
      final response = await _apiService.get<List<dynamic>>(
        '/api/user-relationships/user/$userId/as-target',
      );
      
      return (response.data ?? [])
          .map((rel) => UserRelationshipDto.fromJson(rel))
          .toList();
    } catch (e) {
      throw Exception('사용자 관계 조회 실패: ${_apiService.handleError(e)}');
    }
  }
  
  /// 특정 유형의 관계 조회
  Future<List<UserRelationshipDto>> getRelationshipsByType(String relationshipType) async {
    try {
      final response = await _apiService.get<List<dynamic>>(
        '/api/user-relationships/type/$relationshipType',
      );
      
      return (response.data ?? [])
          .map((rel) => UserRelationshipDto.fromJson(rel))
          .toList();
    } catch (e) {
      throw Exception('관계 유형별 조회 실패: ${_apiService.handleError(e)}');
    }
  }
  
  /// 돌봄 대상자 목록 조회 (관리자/돌봄 제공자용)
  Future<List<UserDto>> getCareTargets(String userId) async {
    try {
      // 사용자가 주체인 돌봄 관계들을 조회
      final relationships = await getUserRelationshipsAsSubject(userId);
      
      // 돌봄 대상자 ID들 추출
      final targetIds = relationships
          .where((rel) => rel.relationshipType == 'caregiver' && rel.status == 'active')
          .map((rel) => rel.targetUserId)
          .toList();
      
      // 돌봄 대상자 정보 조회
      final careTargets = <UserDto>[];
      for (final targetId in targetIds) {
        try {
          final target = await getUserById(targetId);
          careTargets.add(target);
        } catch (e) {
          // 개별 사용자 조회 실패 시 로그만 남기고 계속 진행
          print('돌봄 대상자 정보 조회 실패: $targetId - $e');
        }
      }
      
      return careTargets;
    } catch (e) {
      throw Exception('돌봄 대상자 목록 조회 실패: ${_apiService.handleError(e)}');
    }
  }
}
