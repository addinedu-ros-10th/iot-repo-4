/// 사용자 기본 정보 DTO
class UserDto {
  final String userId;
  final String userName;
  final String? email;
  final String? phoneNumber;
  final String userRole;
  final DateTime? createdAt;

  UserDto({
    required this.userId,
    required this.userName,
    this.email,
    this.phoneNumber,
    required this.userRole,
    this.createdAt,
  });

  factory UserDto.fromJson(Map<String, dynamic> json) {
    return UserDto(
      userId: json['user_id'] ?? '',
      userName: json['user_name'] ?? '',
      email: json['email'],
      phoneNumber: json['phone_number'],
      userRole: json['user_role'] ?? 'user',
      createdAt: json['created_at'] != null 
          ? DateTime.parse(json['created_at']) 
          : null,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'user_id': userId,
      'user_name': userName,
      'email': email,
      'phone_number': phoneNumber,
      'user_role': userRole,
      'created_at': createdAt?.toIso8601String(),
    };
  }
}

/// 사용자 프로필 DTO
class UserProfileDto {
  final String userId;
  final DateTime dateOfBirth;
  final String gender;
  final String? address;
  final String? addressDetail;
  final String? medicalHistory;
  final String? significantNotes;
  final String? currentStatus;
  final DateTime? createdAt;
  final DateTime? updatedAt;

  UserProfileDto({
    required this.userId,
    required this.dateOfBirth,
    required this.gender,
    this.address,
    this.addressDetail,
    this.medicalHistory,
    this.significantNotes,
    this.currentStatus,
    this.createdAt,
    this.updatedAt,
  });

  factory UserProfileDto.fromJson(Map<String, dynamic> json) {
    return UserProfileDto(
      userId: json['user_id'] ?? '',
      dateOfBirth: DateTime.parse(json['date_of_birth']),
      gender: json['gender'] ?? 'other',
      address: json['address'],
      addressDetail: json['address_detail'],
      medicalHistory: json['medical_history'],
      significantNotes: json['significant_notes'],
      currentStatus: json['current_status'],
      createdAt: json['created_at'] != null 
          ? DateTime.parse(json['created_at']) 
          : null,
      updatedAt: json['updated_at'] != null 
          ? DateTime.parse(json['updated_at']) 
          : null,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'user_id': userId,
      'date_of_birth': dateOfBirth.toIso8601String().split('T')[0],
      'gender': gender,
      'address': address,
      'address_detail': addressDetail,
      'medical_history': medicalHistory,
      'significant_notes': significantNotes,
      'current_status': currentStatus,
      'created_at': createdAt?.toIso8601String(),
      'updated_at': updatedAt?.toIso8601String(),
    };
  }

  /// 나이 계산
  int get age {
    final now = DateTime.now();
    int age = now.year - dateOfBirth.year;
    if (now.month < dateOfBirth.month || 
        (now.month == dateOfBirth.month && now.day < dateOfBirth.day)) {
      age--;
    }
    return age;
  }
}



/// 사용자 목록 응답 DTO
class UserListResponseDto {
  final List<UserDto> users;
  final int total;
  final int page;
  final int size;

  UserListResponseDto({
    required this.users,
    required this.total,
    required this.page,
    required this.size,
  });

  factory UserListResponseDto.fromJson(Map<String, dynamic> json) {
    return UserListResponseDto(
      users: (json['users'] as List?)
          ?.map((user) => UserDto.fromJson(user))
          .toList() ?? [],
      total: json['total'] ?? 0,
      page: json['page'] ?? 1,
      size: json['size'] ?? 10,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'users': users.map((user) => user.toJson()).toList(),
      'total': total,
      'page': page,
      'size': size,
    };
  }
}

/// 사용자 관계 목록 응답 DTO
class UserRelationshipListResponseDto {
  final List<Map<String, dynamic>> relationships;
  final int total;
  final int page;
  final int size;

  UserRelationshipListResponseDto({
    required this.relationships,
    required this.total,
    required this.page,
    required this.size,
  });

  factory UserRelationshipListResponseDto.fromJson(Map<String, dynamic> json) {
    return UserRelationshipListResponseDto(
      relationships: (json['relationships'] as List?)
          ?.map((rel) => rel as Map<String, dynamic>)
          .toList() ?? [],
      total: json['total'] ?? 0,
      page: json['page'] ?? 1,
      size: json['size'] ?? 10,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'relationships': relationships,
      'total': total,
      'page': page,
      'size': size,
    };
  }
}
