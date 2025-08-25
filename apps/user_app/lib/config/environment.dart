/// 환경별 설정을 관리하는 클래스
class EnvironmentConfig {
  static const String _environment = String.fromEnvironment(
    'ENVIRONMENT',
    defaultValue: 'development',
  );

  /// 현재 환경
  static String get environment => _environment;

  /// 개발 환경 여부
  static bool get isDevelopment => _environment == 'development';

  /// 프로덕션 환경 여부
  static bool get isProduction => _environment == 'production';

  /// 테스트 환경 여부
  static bool get isTest => _environment == 'test';

  /// Mock 데이터 사용 여부
  static bool get useMockData => _environment == 'development' || _environment == 'test';

  /// API 기본 URL
  static String get apiBaseUrl {
    switch (_environment) {
      case 'production':
        return 'https://your-production-api.com';
      case 'development':
        return 'http://192.168.0.14:8000';
      case 'test':
        return 'http://localhost:8000';
      default:
        return 'http://192.168.0.14:8000';
    }
  }

  /// API 타임아웃 (초)
  static int get apiTimeout => _environment == 'production' ? 30 : 60;

  /// 로그 레벨
  static String get logLevel => _environment == 'production' ? 'error' : 'debug';
}
