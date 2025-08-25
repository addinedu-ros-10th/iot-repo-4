/// 홈 상태 스냅샷 DTO
class HomeStateSnapshotDto {
  final DateTime time;
  final String userId;
  
  // 입구 센서
  final bool? entrancePirMotion;
  final String? entranceRfidStatus;
  final bool? entranceReedIsClosed;
  
  // 거실 센서
  final bool? livingroomPir1Motion;
  final bool? livingroomPir2Motion;
  final double? livingroomSoundDb;
  final double? livingroomMq7CoPpm;
  final String? livingroomButtonState;
  
  // 주방 센서
  final bool? kitchenPirMotion;
  final double? kitchenSoundDb;
  final double? kitchenMq5GasPpm;
  final double? kitchenLoadcell1Kg;
  final double? kitchenLoadcell2Kg;
  final String? kitchenButtonState;
  final bool? kitchenBuzzerIsOn;
  
  // 침실 센서
  final bool? bedroomPirMotion;
  final double? bedroomSoundDb;
  final double? bedroomMq7CoPpm;
  final double? bedroomLoadcellKg;
  final String? bedroomButtonState;
  
  // 화장실 센서
  final bool? bathroomPirMotion;
  final double? bathroomSoundDb;
  final double? bathroomTempCelsius;
  final String? bathroomButtonState;
  
  // 시스템 상태
  final String? detectedActivity;
  final String? alertLevel;
  final String? alertReason;
  final Map<String, dynamic>? actionLog;
  final Map<String, dynamic>? extraData;

  HomeStateSnapshotDto({
    required this.time,
    required this.userId,
    this.entrancePirMotion,
    this.entranceRfidStatus,
    this.entranceReedIsClosed,
    this.livingroomPir1Motion,
    this.livingroomPir2Motion,
    this.livingroomSoundDb,
    this.livingroomMq7CoPpm,
    this.livingroomButtonState,
    this.kitchenPirMotion,
    this.kitchenSoundDb,
    this.kitchenMq5GasPpm,
    this.kitchenLoadcell1Kg,
    this.kitchenLoadcell2Kg,
    this.kitchenButtonState,
    this.kitchenBuzzerIsOn,
    this.bedroomPirMotion,
    this.bedroomSoundDb,
    this.bedroomMq7CoPpm,
    this.bedroomLoadcellKg,
    this.bedroomButtonState,
    this.bathroomPirMotion,
    this.bathroomSoundDb,
    this.bathroomTempCelsius,
    this.bathroomButtonState,
    this.detectedActivity,
    this.alertLevel,
    this.alertReason,
    this.actionLog,
    this.extraData,
  });

  factory HomeStateSnapshotDto.fromJson(Map<String, dynamic> json) {
    return HomeStateSnapshotDto(
      time: DateTime.parse(json['time']),
      userId: json['user_id'] ?? '',
      entrancePirMotion: json['entrance_pir_motion'] as bool?,
      entranceRfidStatus: json['entrance_rfid_status'],
      entranceReedIsClosed: json['entrance_reed_is_closed'] as bool?,
      livingroomPir1Motion: json['livingroom_pir_1_motion'] as bool?,
      livingroomPir2Motion: json['livingroom_pir_2_motion'] as bool?,
      livingroomSoundDb: (json['livingroom_sound_db'] as num?)?.toDouble(),
      livingroomMq7CoPpm: (json['livingroom_mq7_co_ppm'] as num?)?.toDouble(),
      livingroomButtonState: json['livingroom_button_state'],
      kitchenPirMotion: json['kitchen_pir_motion'] as bool?,
      kitchenSoundDb: (json['kitchen_sound_db'] as num?)?.toDouble(),
      kitchenMq5GasPpm: (json['kitchen_mq5_gas_ppm'] as num?)?.toDouble(),
      kitchenLoadcell1Kg: (json['kitchen_loadcell_1_kg'] as num?)?.toDouble(),
      kitchenLoadcell2Kg: (json['kitchen_loadcell_2_kg'] as num?)?.toDouble(),
      kitchenButtonState: json['kitchen_button_state'],
      kitchenBuzzerIsOn: json['kitchen_buzzer_is_on'] as bool?,
      bedroomPirMotion: json['bedroom_pir_motion'] as bool?,
      bedroomSoundDb: (json['bedroom_sound_db'] as num?)?.toDouble(),
      bedroomMq7CoPpm: (json['bedroom_mq7_co_ppm'] as num?)?.toDouble(),
      bedroomLoadcellKg: (json['bedroom_loadcell_kg'] as num?)?.toDouble(),
      bedroomButtonState: json['bedroom_button_state'],
      bathroomPirMotion: json['bathroom_pir_motion'] as bool?,
      bathroomSoundDb: (json['bathroom_sound_db'] as num?)?.toDouble(),
      bathroomTempCelsius: (json['bathroom_temp_celsius'] as num?)?.toDouble(),
      bathroomButtonState: json['bathroom_button_state'],
      detectedActivity: json['detected_activity'],
      alertLevel: json['alert_level'],
      alertReason: json['alert_reason'],
      actionLog: json['action_log'] as Map<String, dynamic>?,
      extraData: json['extra_data'] as Map<String, dynamic>?,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'time': time.toIso8601String(),
      'user_id': userId,
      'entrance_pir_motion': entrancePirMotion,
      'entrance_rfid_status': entranceRfidStatus,
      'entrance_reed_is_closed': entranceReedIsClosed,
      'livingroom_pir_1_motion': livingroomPir1Motion,
      'livingroom_pir_2_motion': livingroomPir2Motion,
      'livingroom_sound_db': livingroomSoundDb,
      'livingroom_mq7_co_ppm': livingroomMq7CoPpm,
      'livingroom_button_state': livingroomButtonState,
      'kitchen_pir_motion': kitchenPirMotion,
      'kitchen_sound_db': kitchenSoundDb,
      'kitchen_mq5_gas_ppm': kitchenMq5GasPpm,
      'kitchen_loadcell_1_kg': kitchenLoadcell1Kg,
      'kitchen_loadcell_2_kg': kitchenLoadcell2Kg,
      'kitchen_button_state': kitchenButtonState,
      'kitchen_buzzer_is_on': kitchenBuzzerIsOn,
      'bedroom_pir_motion': bedroomPirMotion,
      'bedroom_sound_db': bedroomSoundDb,
      'bedroom_mq7_co_ppm': bedroomMq7CoPpm,
      'bedroom_loadcell_kg': bedroomLoadcellKg,
      'bedroom_button_state': bedroomButtonState,
      'bathroom_pir_motion': bathroomPirMotion,
      'bathroom_sound_db': bathroomSoundDb,
      'bathroom_temp_celsius': bathroomTempCelsius,
      'bathroom_button_state': bathroomButtonState,
      'detected_activity': detectedActivity,
      'alert_level': alertLevel,
      'alert_reason': alertReason,
      'action_log': actionLog,
      'extra_data': extraData,
    };
  }

  /// 경보 수준 우선순위 (높을수록 위험)
  int get alertPriority {
    switch (alertLevel?.toLowerCase()) {
      case 'emergency':
        return 4;
      case 'warning':
        return 3;
      case 'attention':
        return 2;
      case 'normal':
        return 1;
      default:
        return 0;
    }
  }

  /// 위험 상태 여부
  bool get isInDanger {
    return alertLevel?.toLowerCase() == 'emergency' || 
           alertLevel?.toLowerCase() == 'warning';
  }

  /// 주의가 필요한 상태 여부
  bool get needsAttention {
    return alertLevel?.toLowerCase() == 'attention';
  }

  /// 정상 상태 여부
  bool get isNormal {
    return alertLevel?.toLowerCase() == 'normal';
  }

  /// 마지막 활동으로부터 경과 시간 (분)
  int get minutesSinceLastActivity {
    final now = DateTime.now();
    return now.difference(time).inMinutes;
  }

  /// 비활성 상태 여부 (30분 이상)
  bool get isInactive {
    return minutesSinceLastActivity > 30;
  }

  /// 센서 데이터 요약
  String get sensorSummary {
    final activeSensors = <String>[];
    
    if (entrancePirMotion == true) activeSensors.add('입구 모션');
    if (livingroomPir1Motion == true || livingroomPir2Motion == true) activeSensors.add('거실 모션');
    if (kitchenPirMotion == true) activeSensors.add('주방 모션');
    if (bedroomPirMotion == true) activeSensors.add('침실 모션');
    if (bathroomPirMotion == true) activeSensors.add('화장실 모션');
    
    if (activeSensors.isEmpty) return '활성 센서 없음';
    return activeSensors.join(', ');
  }

  /// 환경 데이터 요약
  String get environmentSummary {
    final envData = <String>[];
    
    if (livingroomSoundDb != null) envData.add('거실 소음: ${livingroomSoundDb!.toStringAsFixed(1)}dB');
    if (kitchenMq5GasPpm != null) envData.add('주방 가스: ${kitchenMq5GasPpm!.toStringAsFixed(1)}ppm');
    if (bathroomTempCelsius != null) envData.add('화장실 온도: ${bathroomTempCelsius!.toStringAsFixed(1)}°C');
    
    if (envData.isEmpty) return '환경 데이터 없음';
    return envData.join(', ');
  }
}

/// 홈 상태 스냅샷 목록 응답 DTO
class HomeStateSnapshotListResponseDto {
  final List<HomeStateSnapshotDto> snapshots;
  final int total;
  final int page;
  final int size;

  HomeStateSnapshotListResponseDto({
    required this.snapshots,
    required this.total,
    required this.page,
    required this.size,
  });

  factory HomeStateSnapshotListResponseDto.fromJson(Map<String, dynamic> json) {
    return HomeStateSnapshotListResponseDto(
      snapshots: (json['snapshots'] as List?)
          ?.map((snapshot) => HomeStateSnapshotDto.fromJson(snapshot))
          .toList() ?? [],
      total: json['total'] ?? 0,
      page: json['page'] ?? 1,
      size: json['size'] ?? 10,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'snapshots': snapshots.map((snapshot) => snapshot.toJson()).toList(),
      'total': total,
      'page': page,
      'size': size,
    };
  }
}
