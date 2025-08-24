/// 사용자 관계 DTO
class UserRelationshipDto {
  final String relationshipId;
  final String subjectUserId;
  final String targetUserId;
  final String relationshipType;
  final String status;
  final DateTime? createdAt;
  final DateTime? updatedAt;

  UserRelationshipDto({
    required this.relationshipId,
    required this.subjectUserId,
    required this.targetUserId,
    required this.relationshipType,
    required this.status,
    this.createdAt,
    this.updatedAt,
  });

  factory UserRelationshipDto.fromJson(Map<String, dynamic> json) {
    return UserRelationshipDto(
      relationshipId: json['relationship_id'] ?? '',
      subjectUserId: json['subject_user_id'] ?? '',
      targetUserId: json['target_user_id'] ?? '',
      relationshipType: json['relationship_type'] ?? '',
      status: json['status'] ?? 'active',
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
      'relationship_id': relationshipId,
      'subject_user_id': subjectUserId,
      'target_user_id': targetUserId,
      'relationship_type': relationshipType,
      'status': status,
      'created_at': createdAt?.toIso8601String(),
      'updated_at': updatedAt?.toIso8601String(),
    };
  }

  /// 관계 유형 한글 표시
  String get relationshipTypeDisplay {
    switch (relationshipType) {
      case 'caregiver':
        return '돌봄 제공자';
      case 'family':
        return '가족';
      case 'admin':
        return '관리자';
      default:
        return relationshipType;
    }
  }

  /// 상태 한글 표시
  String get statusDisplay {
    switch (status) {
      case 'pending':
        return '대기 중';
      case 'active':
        return '활성';
      case 'inactive':
        return '비활성';
      default:
        return status;
    }
  }
}
