import 'package:user_app/data/dtos/user_dto.dart';
import 'package:user_app/data/dtos/user_relationship_dto.dart';
import 'package:user_app/data/services/mock_data_service.dart';
import 'package:user_app/data/services/interfaces/user_service_interface.dart';

/// Mock 사용자 서비스 - 실제 API 호출 대신 샘플 데이터 제공
class MockUserService implements UserServiceInterface {
  final MockDataService _mockDataService = MockDataService();

  /// Mock 사용자 관계 조회 (돌봄 대상자 목록)
  @override
  Future<List<UserRelationshipDto>> getUserRelationshipsAsSubject(String userId) async {
    // 실제 API 호출을 시뮬레이션하기 위한 지연
    await Future.delayed(const Duration(milliseconds: 500));
    
    // Mock 데이터를 UserRelationshipDto로 변환
    final mockData = _mockDataService.getMockUserRelationships();
    return mockData.map((data) => UserRelationshipDto(
      relationshipId: data['relationship_id'] ?? '',
      subjectUserId: data['subject_user_id'] ?? '',
      targetUserId: data['target_user_id'] ?? '',
      relationshipType: data['relationship_type'] ?? '',
      status: 'active',
      createdAt: data['created_at'] != null 
          ? DateTime.parse(data['created_at']) 
          : null,
      updatedAt: null,
    )).toList();
  }



  /// Mock 사용자 목록 조회
  Future<List<UserDto>> getUserList() async {
    await Future.delayed(const Duration(milliseconds: 400));
    
    return _mockDataService.getMockUsers();
  }

  // Interface implementation methods
  
  @override
  Future<UserListResponseDto> getAllUsers({
    int page = 1,
    int size = 10,
    String? role,
  }) async {
    await Future.delayed(const Duration(milliseconds: 400));
    
    final users = _mockDataService.getMockUsers();
    final filteredUsers = role != null 
        ? users.where((user) => user.userRole == role).toList()
        : users;
    
    return UserListResponseDto(
      users: filteredUsers,
      total: filteredUsers.length,
      page: page,
      size: size,
    );
  }

  @override
  Future<UserDto> getUserById(String userId) async {
    await Future.delayed(const Duration(milliseconds: 300));
    
    final users = _mockDataService.getMockUsers();
    return users.firstWhere(
      (user) => user.userId == userId,
      orElse: () => users.first, // 기본값으로 첫 번째 사용자 반환
    );
  }

  @override
  Future<UserDto> createUser({
    required String userName,
    required String userRole,
    String? email,
    String? phoneNumber,
  }) async {
    await Future.delayed(const Duration(milliseconds: 500));
    
    // Mock 사용자 생성
    return UserDto(
      userId: 'user-${DateTime.now().millisecondsSinceEpoch}',
      userName: userName,
      email: email,
      phoneNumber: phoneNumber,
      userRole: userRole,
      createdAt: DateTime.now(),
    );
  }

  @override
  Future<UserDto> updateUser(
    String userId, {
    String? userName,
    String? userRole,
    String? email,
    String? phoneNumber,
  }) async {
    await Future.delayed(const Duration(milliseconds: 400));
    
    final users = _mockDataService.getMockUsers();
    final existingUser = users.firstWhere(
      (user) => user.userId == userId,
      orElse: () => users.first,
    );
    
    return UserDto(
      userId: existingUser.userId,
      userName: userName ?? existingUser.userName,
      email: email ?? existingUser.email,
      phoneNumber: phoneNumber ?? existingUser.phoneNumber,
      userRole: userRole ?? existingUser.userRole,
      createdAt: existingUser.createdAt,
    );
  }

  @override
  Future<void> deleteUser(String userId) async {
    await Future.delayed(const Duration(milliseconds: 300));
    // Mock에서는 아무것도 하지 않음
  }

  @override
  Future<Map<String, dynamic>> createUserRelationship({
    required String subjectUserId,
    required String targetUserId,
    required String relationshipType,
    required String relationshipName,
  }) async {
    await Future.delayed(const Duration(milliseconds: 500));
    
    return {
      'relationship_id': 'rel-${DateTime.now().millisecondsSinceEpoch}',
      'subject_user_id': subjectUserId,
      'target_user_id': targetUserId,
      'relationship_type': relationshipType,
      'relationship_name': relationshipName,
      'created_at': DateTime.now().toIso8601String(),
    };
  }

  @override
  Future<Map<String, dynamic>> updateUserRelationship(
    String relationshipId, {
    String? relationshipType,
    String? relationshipName,
  }) async {
    await Future.delayed(const Duration(milliseconds: 400));
    
    final relationships = _mockDataService.getMockUserRelationships();
    final existingRelationship = relationships.firstWhere(
      (rel) => rel['relationship_id'] == relationshipId,
      orElse: () => relationships.first,
    );
    
    return {
      ...existingRelationship,
      'relationship_type': relationshipType ?? existingRelationship['relationship_type'],
      'relationship_name': relationshipName ?? existingRelationship['relationship_name'],
    };
  }

  @override
  Future<void> deleteUserRelationship(String relationshipId) async {
    await Future.delayed(const Duration(milliseconds: 300));
    // Mock에서는 아무것도 하지 않음
  }

  @override
  Future<List<UserDto>> getCareTargets(String userId) async {
    await Future.delayed(const Duration(milliseconds: 400));
    
    // Mock에서는 모든 사용자를 돌봄 대상자로 반환
    return _mockDataService.getMockUsers();
  }

  @override
  Future<UserProfileDto?> getUserProfile(String userId) async {
    await Future.delayed(const Duration(milliseconds: 300));
    
    // Mock 프로필 데이터 반환
    return UserProfileDto(
      userId: userId,
      dateOfBirth: DateTime(1950, 1, 1),
      gender: 'female',
      address: '서울시 강남구',
      addressDetail: '123-45',
      medicalHistory: '고혈압, 당뇨',
      significantNotes: '특별한 주의사항 없음',
      currentStatus: '정상',
      createdAt: DateTime.now().subtract(const Duration(days: 30)),
      updatedAt: DateTime.now(),
    );
  }
}

