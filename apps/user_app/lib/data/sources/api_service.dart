import 'dart:convert';
import 'package:dio/dio.dart';
import '../../config/environment.dart';

/// Backend API와 통신하는 서비스 클래스
class ApiService {
  late final Dio _dio;
  
  ApiService() {
    _dio = Dio(BaseOptions(
      baseUrl: EnvironmentConfig.apiBaseUrl,
      connectTimeout: const Duration(seconds: 10),
      receiveTimeout: const Duration(seconds: 10),
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
    ));
    
    // 인터셉터 추가 (로깅, 에러 처리 등)
    _dio.interceptors.add(InterceptorsWrapper(
      onRequest: (options, handler) {
        if (EnvironmentConfig.enableLogging) {
          print('🌐 API Request: ${options.method} ${options.path}');
        }
        handler.next(options);
      },
      onResponse: (response, handler) {
        if (EnvironmentConfig.enableLogging) {
          print('✅ API Response: ${response.statusCode} ${response.requestOptions.path}');
        }
        handler.next(response);
      },
      onError: (error, handler) {
        if (EnvironmentConfig.enableLogging) {
          print('❌ API Error: ${error.response?.statusCode} ${error.requestOptions.path}');
          print('Error: ${error.message}');
        }
        handler.next(error);
      },
    ));
  }
  
  /// GET 요청
  Future<Response<T>> get<T>(
    String path, {
    Map<String, dynamic>? queryParameters,
    Options? options,
  }) async {
    try {
      return await _dio.get<T>(
        path,
        queryParameters: queryParameters,
        options: options,
      );
    } catch (e) {
      if (EnvironmentConfig.enableLogging) {
        print('❌ GET 요청 실패: $path');
        print('Error: $e');
      }
      rethrow;
    }
  }
  
  /// POST 요청
  Future<Response<T>> post<T>(
    String path, {
    dynamic data,
    Map<String, dynamic>? queryParameters,
    Options? options,
  }) async {
    try {
      return await _dio.post<T>(
        path,
        data: data,
        queryParameters: queryParameters,
        options: options,
      );
    } catch (e) {
      if (EnvironmentConfig.enableLogging) {
        print('❌ POST 요청 실패: $path');
        print('Error: $e');
      }
      rethrow;
    }
  }
  
  /// PUT 요청
  Future<Response<T>> put<T>(
    String path, {
    dynamic data,
    Map<String, dynamic>? queryParameters,
    Options? options,
  }) async {
    try {
      return await _dio.put<T>(
        path,
        data: data,
        queryParameters: queryParameters,
        options: options,
      );
    } catch (e) {
      if (EnvironmentConfig.enableLogging) {
        print('❌ PUT 요청 실패: $path');
        print('Error: $e');
      }
      rethrow;
    }
  }
  
  /// DELETE 요청
  Future<Response<T>> delete<T>(
    String path, {
    Map<String, dynamic>? queryParameters,
    Options? options,
  }) async {
    try {
      return await _dio.delete<T>(
        path,
        queryParameters: queryParameters,
        options: options,
      );
    } catch (e) {
      if (EnvironmentConfig.enableLogging) {
        print('❌ DELETE 요청 실패: $path');
        print('Error: $e');
      }
      rethrow;
    }
  }
  
  /// 에러 응답 처리
  String handleError(dynamic error) {
    if (error is DioException) {
      switch (error.type) {
        case DioExceptionType.connectionTimeout:
          return '연결 시간 초과';
        case DioExceptionType.sendTimeout:
          return '전송 시간 초과';
        case DioExceptionType.receiveTimeout:
          return '수신 시간 초과';
        case DioExceptionType.badResponse:
          final statusCode = error.response?.statusCode;
          final responseData = error.response?.data;
          
          if (responseData is Map<String, dynamic> && responseData['detail'] != null) {
            return responseData['detail'];
          }
          
          switch (statusCode) {
            case 400:
              return '잘못된 요청입니다';
            case 401:
              return '인증이 필요합니다';
            case 403:
              return '접근 권한이 없습니다';
            case 404:
              return '요청한 리소스를 찾을 수 없습니다';
            case 500:
              return '서버 내부 오류가 발생했습니다';
            default:
              return '알 수 없는 오류가 발생했습니다 (상태 코드: $statusCode)';
          }
        case DioExceptionType.cancel:
          return '요청이 취소되었습니다';
        case DioExceptionType.connectionError:
          return '네트워크 연결을 확인해주세요';
        default:
          return '네트워크 오류가 발생했습니다';
      }
    }
    return '알 수 없는 오류가 발생했습니다';
  }
}
