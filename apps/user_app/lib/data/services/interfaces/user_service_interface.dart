import '../../dtos/user_dto.dart';
import '../../dtos/user_relationship_dto.dart';

/// 사용자 서비스 인터페이스
abstract class UserServiceInterface {
  /// 모든 사용자 목록 조회
  Future<UserListResponseDto> getAllUsers({
    int page = 1,
    int size = 10,
    String? role,
  });

  /// 특정 사용자 조회
  Future<UserDto> getUserById(String userId);

  /// 사용자 생성
  Future<UserDto> createUser({
    required String userName,
    required String userRole,
    String? email,
    String? phoneNumber,
  });

  /// 사용자 정보 수정
  Future<UserDto> updateUser(
    String userId, {
    String? userName,
    String? userRole,
    String? email,
    String? phoneNumber,
  });

  /// 사용자 삭제
  Future<void> deleteUser(String userId);

  /// 사용자 관계 조회 (돌봄 대상자 목록)
  Future<List<UserRelationshipDto>> getUserRelationshipsAsSubject(String userId);

  /// 사용자 관계 생성
  Future<Map<String, dynamic>> createUserRelationship({
    required String subjectUserId,
    required String targetUserId,
    required String relationshipType,
    required String relationshipName,
  });

  /// 사용자 관계 수정
  Future<Map<String, dynamic>> updateUserRelationship(
    String relationshipId, {
    String? relationshipType,
    String? relationshipName,
  });

  /// 사용자 관계 삭제
  Future<void> deleteUserRelationship(String relationshipId);

  /// 돌봄 대상자 목록 조회
  Future<List<UserDto>> getCareTargets(String userId);

  /// 사용자 프로필 조회
  Future<UserProfileDto?> getUserProfile(String userId);
}
