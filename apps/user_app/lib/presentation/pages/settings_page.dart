import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../config/environment.dart';
import '../../data/services/service_factory.dart';

/// 개발 설정 페이지
class SettingsPage extends StatefulWidget {
  const SettingsPage({super.key});

  @override
  State<SettingsPage> createState() => _SettingsPageState();
}

class _SettingsPageState extends State<SettingsPage> {
  bool _useMockData = EnvironmentConfig.useMockData;
  String _currentEnvironment = EnvironmentConfig.environment;
  String _apiBaseUrl = EnvironmentConfig.apiBaseUrl;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('개발 설정'),
        backgroundColor: Colors.grey[900],
        foregroundColor: Colors.white,
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // 환경 정보 카드
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      '현재 환경',
                      style: Theme.of(context).textTheme.titleLarge,
                    ),
                    const SizedBox(height: 8),
                    Text('환경: $_currentEnvironment'),
                    Text('API URL: $_apiBaseUrl'),
                    Text('서비스 타입: ${ServiceFactory.getServiceType()}'),
                  ],
                ),
              ),
            ),
            
            const SizedBox(height: 16),
            
            // Mock 데이터 설정 카드
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Mock 데이터 설정',
                      style: Theme.of(context).textTheme.titleLarge,
                    ),
                    const SizedBox(height: 8),
                    SwitchListTile(
                      title: const Text('Mock 데이터 사용'),
                      subtitle: const Text('개발 중 실제 API 대신 Mock 데이터 사용'),
                      value: _useMockData,
                      onChanged: (value) {
                        setState(() {
                          _useMockData = value;
                        });
                      },
                    ),
                    const SizedBox(height: 8),
                    ElevatedButton(
                      onPressed: () {
                        // 서비스 재생성
                        ServiceFactory.resetServices();
                        ScaffoldMessenger.of(context).showSnackBar(
                          const SnackBar(
                            content: Text('서비스가 재생성되었습니다. 앱을 재시작하세요.'),
                          ),
                        );
                      },
                      child: const Text('서비스 재생성'),
                    ),
                  ],
                ),
              ),
            ),
            
            const SizedBox(height: 16),
            
            // 환경 전환 카드
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      '환경 전환',
                      style: Theme.of(context).textTheme.titleLarge,
                    ),
                    const SizedBox(height: 8),
                    ListTile(
                      title: const Text('개발 환경'),
                      subtitle: const Text('Mock 데이터 사용'),
                      trailing: _currentEnvironment == 'development' 
                          ? const Icon(Icons.check, color: Colors.green)
                          : null,
                      onTap: () => _switchEnvironment('development'),
                    ),
                    ListTile(
                      title: const Text('프로덕션 환경'),
                      subtitle: const Text('실제 API 사용'),
                      trailing: _currentEnvironment == 'production' 
                          ? const Icon(Icons.check, color: Colors.green)
                          : null,
                      onTap: () => _switchEnvironment('production'),
                    ),
                  ],
                ),
              ),
            ),
            
            const Spacer(),
            
            // 정보 카드
            Card(
              color: Colors.blue[50],
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      '💡 개발 팁',
                      style: Theme.of(context).textTheme.titleMedium?.copyWith(
                        color: Colors.blue[700],
                      ),
                    ),
                    const SizedBox(height: 8),
                    const Text(
                      '• Mock 데이터: UI 개발 및 테스트용\n'
                      '• 실제 API: 백엔드 연동 테스트용\n'
                      '• 환경 변경 후 앱 재시작 필요',
                      style: TextStyle(fontSize: 12),
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  void _switchEnvironment(String environment) {
    setState(() {
      _currentEnvironment = environment;
      _useMockData = environment == 'development';
    });
    
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text('환경이 $_currentEnvironment로 변경되었습니다. 앱을 재시작하세요.'),
      ),
    );
  }
}
