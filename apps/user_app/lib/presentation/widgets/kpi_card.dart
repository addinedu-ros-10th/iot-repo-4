import 'package:flutter/material.dart';
import '../../config/app_colors.dart';

/// KPI (Key Performance Indicator) 카드 위젯
class KpiCard extends StatelessWidget {
  final String title;
  final String value;
  final String? subtitle;
  final IconData icon;
  final Color? color;
  final VoidCallback? onTap;
  final bool isLoading;
  
  const KpiCard({
    super.key,
    required this.title,
    required this.value,
    this.subtitle,
    required this.icon,
    this.color,
    this.onTap,
    this.isLoading = false,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      color: AppColors.cardBackground,
      elevation: 4,
      margin: const EdgeInsets.all(8),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(12),
        child: Container(
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(12),
            gradient: LinearGradient(
              begin: Alignment.topLeft,
              end: Alignment.bottomRight,
              colors: [
                AppColors.cardBackground,
                AppColors.cardBackground.withOpacity(0.8),
              ],
            ),
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  Icon(
                    icon,
                    color: color ?? AppColors.accentCalm,
                    size: 24,
                  ),
                  const SizedBox(width: 8),
                  Expanded(
                    child: Text(
                      title,
                      style: TextStyle(
                        color: AppColors.secondaryText,
                        fontSize: 14,
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 12),
              if (isLoading)
                const SizedBox(
                  height: 32,
                  child: Center(
                    child: CircularProgressIndicator(
                      strokeWidth: 2,
                      valueColor: AlwaysStoppedAnimation<Color>(AppColors.accentCalm),
                    ),
                  ),
                )
              else
                Text(
                  value,
                  style: TextStyle(
                    color: AppColors.neutralText,
                    fontSize: 28,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              if (subtitle != null) ...[
                const SizedBox(height: 4),
                Text(
                  subtitle!,
                  style: TextStyle(
                    color: AppColors.secondaryText,
                    fontSize: 12,
                  ),
                ),
              ],
            ],
          ),
        ),
      ),
    );
  }
}

/// 경보 수준별 KPI 카드
class AlertLevelKpiCard extends StatelessWidget {
  final String alertLevel;
  final int count;
  final VoidCallback? onTap;
  final bool isLoading;
  
  const AlertLevelKpiCard({
    super.key,
    required this.alertLevel,
    required this.count,
    this.onTap,
    this.isLoading = false,
  });

  @override
  Widget build(BuildContext context) {
    final color = AppColors.getAlertColor(alertLevel);
    final icon = _getIconForAlertLevel(alertLevel);
    
    return KpiCard(
      title: _getTitleForAlertLevel(alertLevel),
      value: count.toString(),
      subtitle: '건',
      icon: icon,
      color: color,
      onTap: onTap,
      isLoading: isLoading,
    );
  }
  
  IconData _getIconForAlertLevel(String level) {
    switch (level.toLowerCase()) {
      case 'emergency':
        return Icons.warning_rounded;
      case 'warning':
        return Icons.error_outline;
      case 'attention':
        return Icons.info_outline;
      case 'normal':
        return Icons.check_circle_outline;
      default:
        return Icons.help_outline;
    }
  }
  
  String _getTitleForAlertLevel(String level) {
    switch (level.toLowerCase()) {
      case 'emergency':
        return '긴급';
      case 'warning':
        return '경고';
      case 'attention':
        return '주의';
      case 'normal':
        return '정상';
      default:
        return '알 수 없음';
    }
  }
}
