import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'config/environment.dart';
import 'config/app_colors.dart';
import 'presentation/pages/global_dashboard_page.dart';
import 'data/sources/api_service.dart';
import 'data/services/user_service.dart';
import 'data/services/home_state_snapshot_service.dart';
import 'presentation/state/care_targets_provider.dart';
import 'presentation/state/home_state_snapshots_provider.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        // API 서비스 제공
        Provider<ApiService>(
          create: (_) => ApiService(),
        ),
        
        // 사용자 서비스 제공
        Provider<UserService>(
          create: (context) => UserService(
            context.read<ApiService>(),
          ),
        ),
        
        // 홈 상태 스냅샷 서비스 제공
        Provider<HomeStateSnapshotService>(
          create: (context) => HomeStateSnapshotService(
            context.read<ApiService>(),
          ),
        ),
        
        // 돌봄 대상자 Provider 제공
        ChangeNotifierProvider<CareTargetsProvider>(
          create: (context) => CareTargetsProvider(
            context.read<UserService>(),
          ),
        ),
        
        // 홈 상태 스냅샷 Provider 제공
        ChangeNotifierProvider<HomeStateSnapshotsProvider>(
          create: (context) => HomeStateSnapshotsProvider(
            context.read<HomeStateSnapshotService>(),
          ),
        ),
      ],
      child: MaterialApp(
        title: EnvironmentConfig.appTitle,
        debugShowCheckedModeBanner: EnvironmentConfig.isDebug,
        theme: ThemeData(
          useMaterial3: true,
          colorScheme: ColorScheme.dark(
            primary: AppColors.accentCalm,
            secondary: AppColors.chartAccent,
            surface: AppColors.surface,
            background: AppColors.primaryBackground,
            error: AppColors.alertWarning,
            onPrimary: AppColors.surface,
            onSecondary: AppColors.surface,
            onSurface: AppColors.neutralText,
            onBackground: AppColors.neutralText,
            onError: AppColors.surface,
          ),
          scaffoldBackgroundColor: AppColors.primaryBackground,
          appBarTheme: const AppBarTheme(
            backgroundColor: AppColors.secondaryBackground,
            foregroundColor: AppColors.neutralText,
            elevation: 0,
          ),
          cardTheme: CardTheme(
            color: AppColors.secondaryBackground,
            elevation: 2,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(12),
            ),
          ),
          elevatedButtonTheme: ElevatedButtonThemeData(
            style: ElevatedButton.styleFrom(
              backgroundColor: AppColors.accentCalm,
              foregroundColor: AppColors.surface,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(12),
              ),
              padding: const EdgeInsets.symmetric(
                horizontal: 24,
                vertical: 12,
              ),
            ),
          ),
          inputDecorationTheme: InputDecorationTheme(
            filled: true,
            fillColor: AppColors.secondaryBackground,
            border: OutlineInputBorder(
              borderRadius: BorderRadius.circular(12),
              borderSide: BorderSide.none,
            ),
            enabledBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(12),
              borderSide: BorderSide(
                color: AppColors.surface.withOpacity(0.1),
              ),
            ),
            focusedBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(12),
              borderSide: const BorderSide(
                color: AppColors.accentCalm,
                width: 2,
              ),
            ),
            labelStyle: const TextStyle(
              color: AppColors.secondaryText,
            ),
            hintStyle: const TextStyle(
              color: AppColors.secondaryText,
            ),
          ),
        ),
        home: const GlobalDashboardPage(),
      ),
    );
  }
}
