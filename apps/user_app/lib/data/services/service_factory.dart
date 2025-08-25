import 'package:user_app/config/environment.dart';
import 'package:user_app/data/services/interfaces/user_service_interface.dart';
import 'package:user_app/data/services/interfaces/home_state_snapshot_service_interface.dart';
import 'package:user_app/data/services/mock_user_service.dart';
import 'package:user_app/data/services/mock_home_state_snapshot_service.dart';
import 'package:user_app/data/services/user_service.dart';
import 'package:user_app/data/services/home_state_snapshot_service.dart';
import 'package:user_app/data/sources/api_service.dart';

/// 서비스 팩토리 - 환경에 따라 적절한 서비스 인스턴스 생성
class ServiceFactory {
  static UserServiceInterface? _userService;
  static HomeStateSnapshotServiceInterface? _homeStateSnapshotService;

  /// 사용자 서비스 인스턴스 생성
  static UserServiceInterface createUserService() {
    if (_userService != null) return _userService!;

    if (EnvironmentConfig.useMockData) {
      _userService = MockUserService();
      print('🔧 Mock 사용자 서비스 생성됨');
    } else {
      final apiService = ApiService();
      _userService = UserService(apiService);
      print('🔧 실제 API 사용자 서비스 생성됨');
    }

    return _userService!;
  }

  /// 홈 상태 스냅샷 서비스 인스턴스 생성
  static HomeStateSnapshotServiceInterface createHomeStateSnapshotService() {
    if (_homeStateSnapshotService != null) return _homeStateSnapshotService!;

    if (EnvironmentConfig.useMockData) {
      _homeStateSnapshotService = MockHomeStateSnapshotService();
      print('🔧 Mock 홈 상태 스냅샷 서비스 생성됨');
    } else {
      final apiService = ApiService();
      _homeStateSnapshotService = HomeStateSnapshotService(apiService);
      print('🔧 실제 API 홈 상태 스냅샷 서비스 생성됨');
    }

    return _homeStateSnapshotService!;
  }

  /// 서비스 인스턴스 초기화 (테스트용)
  static void resetServices() {
    _userService = null;
    _homeStateSnapshotService = null;
  }

  /// 현재 사용 중인 서비스 타입 확인
  static String getServiceType() {
    return EnvironmentConfig.useMockData ? 'Mock' : 'Real API';
  }
}
