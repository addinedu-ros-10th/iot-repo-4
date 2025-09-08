import 'package:flutter/material.dart';

/// 앱 전체에서 사용하는 색상 시스템
class AppColors {
  // Private constructor to prevent instantiation
  AppColors._();
  
  // Primary Background Colors
  static const Color primaryBackground = Color(0xFF111827);    // 차콜 블랙
  static const Color secondaryBackground = Color(0xFF1F2937); // 다크 그레이
  
  // Surface Colors
  static const Color surface = Color(0xFFFFFFFF);             // 화이트
  static const Color cardBackground = Color(0xFF374151);      // 라이트 그레이
  
  // Text Colors
  static const Color neutralText = Color(0xFFE5E7EB);         // 화이트 톤
  static const Color secondaryText = Color(0xFF9CA3AF);       // 회색
  
  // Accent Colors
  static const Color accentCalm = Color(0xFF3B82F6);          // 블루
  static const Color chartAccent = Color(0xFF06B6D4);         // 시안
  
  // Alert Colors
  static const Color alertAttention = Color(0xFFF59E0B);      // 앰버
  static const Color alertWarning = Color(0xFFEF4444);        // 레드
  static const Color alertEmergency = Color(0xFFDC2626);      // 다크 레드
  
  // Success Colors
  static const Color highlightSuccess = Color(0xFF10B981);    // 그린
  
  // Additional Colors
  static const Color divider = Color(0xFF4B5563);             // 구분선
  static const Color overlay = Color(0x80000000);             // 오버레이
  
  /// 경보 레벨에 따른 색상 반환
  static Color getAlertColor(String alertLevel) {
    switch (alertLevel.toLowerCase()) {
      case 'emergency':
        return alertEmergency;
      case 'warning':
        return alertWarning;
      case 'attention':
        return alertAttention;
      case 'normal':
        return highlightSuccess;
      default:
        return neutralText;
    }
  }
  
  /// 경보 레벨에 따른 배경 색상 반환
  static Color getAlertBackgroundColor(String alertLevel) {
    switch (alertLevel.toLowerCase()) {
      case 'emergency':
        return alertEmergency.withOpacity(0.1);
      case 'warning':
        return alertWarning.withOpacity(0.1);
      case 'attention':
        return alertAttention.withOpacity(0.1);
      case 'normal':
        return highlightSuccess.withOpacity(0.1);
      default:
        return Colors.transparent;
    }
  }
  
  /// 그라데이션 색상 리스트
  static List<Color> get primaryGradient => [
    primaryBackground,
    secondaryBackground,
  ];
  
  static List<Color> get accentGradient => [
    accentCalm,
    chartAccent,
  ];
}
