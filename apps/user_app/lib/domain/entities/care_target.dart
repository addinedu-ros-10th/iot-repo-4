/// 돌봄 대상자 도메인 엔티티
class CareTarget {
  final String userId;
  final String name;
  final String? email;
  final String? phoneNumber;
  final String userRole;
  final DateTime createdAt;
  final DateTime? lastActivityTime;
  final String? currentAlertLevel;
  final String? currentAlertReason;
  
  CareTarget({
    required this.userId,
    required this.name,
    this.email,
    this.phoneNumber,
    required this.userRole,
    required this.createdAt,
    this.lastActivityTime,
    this.currentAlertLevel,
    this.currentAlertReason,
  });
  
  /// 경보 수준의 우선순위 반환
  int get alertPriority {
    switch (currentAlertLevel?.toLowerCase()) {
      case 'emergency':
        return 0;
      case 'warning':
        return 1;
      case 'attention':
        return 2;
      case 'normal':
        return 3;
      default:
        return 4;
    }
  }
  
  /// 위험 상황 여부
  bool get isInDanger {
    return currentAlertLevel?.toLowerCase() == 'emergency' ||
           currentAlertLevel?.toLowerCase() == 'warning';
  }
  
  /// 주의가 필요한 상황 여부
  bool get needsAttention {
    return currentAlertLevel?.toLowerCase() == 'attention';
  }
  
  /// 정상 상태 여부
  bool get isNormal {
    return currentAlertLevel?.toLowerCase() == 'normal';
  }
  
  /// 마지막 활동으로부터 경과 시간 (분)
  int get minutesSinceLastActivity {
    if (lastActivityTime == null) return 0;
    final now = DateTime.now();
    return now.difference(lastActivityTime!).inMinutes;
  }
  
  /// 오랫동안 활동이 없는지 확인 (1시간 이상)
  bool get isInactive {
    return minutesSinceLastActivity > 60;
  }
  
  /// 복사본 생성
  CareTarget copyWith({
    String? userId,
    String? name,
    String? email,
    String? phoneNumber,
    String? userRole,
    DateTime? createdAt,
    DateTime? lastActivityTime,
    String? currentAlertLevel,
    String? currentAlertReason,
  }) {
    return CareTarget(
      userId: userId ?? this.userId,
      name: name ?? this.name,
      email: email ?? this.email,
      phoneNumber: phoneNumber ?? this.phoneNumber,
      userRole: userRole ?? this.userRole,
      createdAt: createdAt ?? this.createdAt,
      lastActivityTime: lastActivityTime ?? this.lastActivityTime,
      currentAlertLevel: currentAlertLevel ?? this.currentAlertLevel,
      currentAlertReason: currentAlertReason ?? this.currentAlertReason,
    );
  }
  
  /// JSON에서 엔티티 생성
  factory CareTarget.fromJson(Map<String, dynamic> json) {
    return CareTarget(
      userId: json['user_id'] ?? '',
      name: json['name'] ?? '',
      email: json['email'],
      phoneNumber: json['phone_number'],
      userRole: json['user_role'] ?? '',
      createdAt: DateTime.parse(json['created_at']),
      lastActivityTime: json['last_activity_time'] != null 
          ? DateTime.parse(json['last_activity_time']) 
          : null,
      currentAlertLevel: json['current_alert_level'],
      currentAlertReason: json['current_alert_reason'],
    );
  }
  
  /// 엔티티를 JSON으로 변환
  Map<String, dynamic> toJson() {
    return {
      'user_id': userId,
      'name': name,
      'email': email,
      'phone_number': phoneNumber,
      'user_role': userRole,
      'created_at': createdAt.toIso8601String(),
      'last_activity_time': lastActivityTime?.toIso8601String(),
      'current_alert_level': currentAlertLevel,
      'current_alert_reason': currentAlertReason,
    };
  }
  
  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is CareTarget && other.userId == userId;
  }
  
  @override
  int get hashCode => userId.hashCode;
  
  @override
  String toString() {
    return 'CareTarget(userId: $userId, name: $name, alertLevel: $currentAlertLevel)';
  }
}
