/// 환경별 설정을 관리하는 클래스
enum Environment { local, development, staging, production }

class EnvironmentConfig {
  static Environment _environment = Environment.local;
  
  /// 환경 설정
  static void setEnvironment(Environment env) {
    _environment = env;
  }
  
  /// 현재 환경
  static Environment get current => _environment;
  
  /// API 기본 URL
  static String get apiBaseUrl {
    switch (_environment) {
      case Environment.local:
        return 'http://localhost';
      case Environment.development:
        return 'http://localhost';
      case Environment.staging:
        return 'http://staging-api.care.app';
      case Environment.production:
        return 'http://ec2-43-201-96-23.ap-northeast-2.compute.amazonaws.com';
    }
  }
  
  /// 로깅 활성화 여부
  static bool get enableLogging {
    return _environment != Environment.production;
  }
  
  /// 분석 도구 활성화 여부
  static bool get enableAnalytics {
    return _environment == Environment.production;
  }
  
  /// 디버그 모드 여부
  static bool get isDebug {
    return _environment == Environment.local || _environment == Environment.development;
  }
  
  /// 환경별 앱 제목
  static String get appTitle {
    switch (_environment) {
      case Environment.local:
        return 'IoT Care App (Local)';
      case Environment.development:
        return 'IoT Care App (Dev)';
      case Environment.staging:
        return 'IoT Care App (Staging)';
      case Environment.production:
        return 'IoT Care App';
    }
  }
}
