import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';
import '../../config/app_colors.dart';
import '../../data/dtos/home_state_snapshot_dto.dart';

/// 센서 데이터 차트를 표시하는 위젯
class SensorChartWidget extends StatelessWidget {
  final List<HomeStateSnapshotDto> snapshots;
  final String chartType; // 'temperature', 'sound', 'gas', 'motion'
  final int maxDataPoints;

  const SensorChartWidget({
    super.key,
    required this.snapshots,
    required this.chartType,
    this.maxDataPoints = 20,
  });

  @override
  Widget build(BuildContext context) {
    if (snapshots.isEmpty) {
      return _buildEmptyState();
    }

    final chartData = _prepareChartData();
    
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: AppColors.secondaryBackground,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(
          color: AppColors.surface.withOpacity(0.1),
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(
                _getChartIcon(),
                color: _getChartColor(),
                size: 20,
              ),
              const SizedBox(width: 8),
              Text(
                _getChartTitle(),
                style: const TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                  color: AppColors.neutralText,
                ),
              ),
              const Spacer(),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                decoration: BoxDecoration(
                  color: _getChartColor().withOpacity(0.2),
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Text(
                  _getCurrentValue(),
                  style: TextStyle(
                    fontSize: 12,
                    fontWeight: FontWeight.w500,
                    color: _getChartColor(),
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: 20),
          
          // 차트
          AspectRatio(
            aspectRatio: 2,
            child: LineChart(
              LineChartData(
                gridData: FlGridData(
                  show: true,
                  drawVerticalLine: true,
                  horizontalInterval: _getGridInterval(),
                  verticalInterval: 1,
                  getDrawingHorizontalLine: (value) {
                    return FlLine(
                      color: AppColors.surface.withOpacity(0.2),
                      strokeWidth: 1,
                    );
                  },
                  getDrawingVerticalLine: (value) {
                    return FlLine(
                      color: AppColors.surface.withOpacity(0.2),
                      strokeWidth: 1,
                    );
                  },
                ),
                titlesData: FlTitlesData(
                  show: true,
                  rightTitles: const AxisTitles(
                    sideTitles: SideTitles(showTitles: false),
                  ),
                  topTitles: const AxisTitles(
                    sideTitles: SideTitles(showTitles: false),
                  ),
                  bottomTitles: AxisTitles(
                    sideTitles: SideTitles(
                      showTitles: true,
                      reservedSize: 30,
                      interval: _getBottomTitleInterval(),
                      getTitlesWidget: (value, meta) {
                        if (value.toInt() >= 0 && value.toInt() < chartData.length) {
                          final snapshot = chartData[value.toInt()];
                          return Padding(
                            padding: const EdgeInsets.only(top: 8.0),
                            child: Text(
                              _formatTime(snapshot.time),
                              style: TextStyle(
                                color: AppColors.secondaryText,
                                fontWeight: FontWeight.bold,
                                fontSize: 10,
                              ),
                            ),
                          );
                        }
                        return const Text('');
                      },
                    ),
                  ),
                  leftTitles: AxisTitles(
                    sideTitles: SideTitles(
                      showTitles: true,
                      interval: _getLeftTitleInterval(),
                      reservedSize: 42,
                      getTitlesWidget: (value, meta) {
                        return Text(
                          _formatYAxisValue(value),
                          style: TextStyle(
                            color: AppColors.secondaryText,
                            fontWeight: FontWeight.bold,
                            fontSize: 10,
                          ),
                        );
                      },
                    ),
                  ),
                ),
                borderData: FlBorderData(
                  show: true,
                  border: Border.all(
                    color: AppColors.surface.withOpacity(0.2),
                    width: 1,
                  ),
                ),
                minX: 0,
                maxX: (chartData.length - 1).toDouble(),
                minY: _getMinY(),
                maxY: _getMaxY(),
                lineBarsData: [
                  LineChartBarData(
                    spots: _createSpots(chartData),
                    isCurved: true,
                    color: _getChartColor(),
                    barWidth: 3,
                    isStrokeCapRound: true,
                    dotData: FlDotData(
                      show: true,
                      getDotPainter: (spot, percent, barData, index) {
                        return FlDotCirclePainter(
                          radius: 4,
                          color: _getChartColor(),
                          strokeWidth: 2,
                          strokeColor: AppColors.surface,
                        );
                      },
                    ),
                    belowBarData: BarAreaData(
                      show: true,
                      color: _getChartColor().withOpacity(0.1),
                    ),
                  ),
                ],
                lineTouchData: LineTouchData(
                  touchTooltipData: LineTouchTooltipData(
                    tooltipBgColor: AppColors.surface,
                    tooltipRoundedRadius: 8,
                    tooltipPadding: const EdgeInsets.all(8),
                    getTooltipItems: (touchedSpots) {
                      return touchedSpots.map((touchedSpot) {
                        final snapshot = chartData[touchedSpot.x.toInt()];
                        return LineTooltipItem(
                          '${_getChartTitle()}: ${_formatTooltipValue(snapshot)}\n',
                          const TextStyle(
                            color: AppColors.neutralText,
                            fontWeight: FontWeight.bold,
                          ),
                          children: [
                            TextSpan(
                              text: _formatTime(snapshot.time),
                              style: TextStyle(
                                color: AppColors.secondaryText,
                                fontWeight: FontWeight.normal,
                              ),
                            ),
                          ],
                        );
                      }).toList();
                    },
                  ),
                ),
              ),
            ),
          ),
          
          const SizedBox(height: 16),
          
          // 통계 정보
          _buildStatistics(chartData),
        ],
      ),
    );
  }

  Widget _buildEmptyState() {
    return Container(
      padding: const EdgeInsets.all(24),
      decoration: BoxDecoration(
        color: AppColors.secondaryBackground,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(
          color: AppColors.surface.withOpacity(0.1),
        ),
      ),
      child: Column(
        children: [
          Icon(
            _getChartIcon(),
            size: 48,
            color: AppColors.secondaryText.withOpacity(0.5),
          ),
          const SizedBox(height: 16),
          Text(
            '${_getChartTitle()} 데이터가 없습니다',
            style: TextStyle(
              fontSize: 16,
              color: AppColors.secondaryText,
              fontWeight: FontWeight.w500,
            ),
          ),
          const SizedBox(height: 8),
          Text(
            '센서에서 데이터를 수집 중입니다',
            style: TextStyle(
              fontSize: 14,
              color: AppColors.secondaryText.withOpacity(0.7),
            ),
            textAlign: TextAlign.center,
          ),
        ],
      ),
    );
  }

  Widget _buildStatistics(List<HomeStateSnapshotDto> chartData) {
    if (chartData.isEmpty) return const SizedBox.shrink();

    final values = _extractValues(chartData);
    if (values.isEmpty) return const SizedBox.shrink();

    final avg = values.reduce((a, b) => a + b) / values.length;
    final max = values.reduce((a, b) => a > b ? a : b);
    final min = values.reduce((a, b) => a < b ? a : b);

    return Row(
      children: [
        Expanded(
          child: _buildStatItem('평균', _formatStatValue(avg)),
        ),
        Expanded(
          child: _buildStatItem('최대', _formatStatValue(max)),
        ),
        Expanded(
          child: _buildStatItem('최소', _formatStatValue(min)),
        ),
      ],
    );
  }

  Widget _buildStatItem(String label, String value) {
    return Column(
      children: [
        Text(
          label,
          style: TextStyle(
            fontSize: 12,
            color: AppColors.secondaryText,
          ),
        ),
        const SizedBox(height: 4),
        Text(
          value,
          style: TextStyle(
            fontSize: 16,
            fontWeight: FontWeight.bold,
            color: _getChartColor(),
          ),
        ),
      ],
    );
  }

  // 차트 데이터 준비
  List<HomeStateSnapshotDto> _prepareChartData() {
    final sortedSnapshots = List<HomeStateSnapshotDto>.from(snapshots)
      ..sort((a, b) => a.time.compareTo(b.time));
    
    return sortedSnapshots.take(maxDataPoints).toList();
  }

  List<FlSpot> _createSpots(List<HomeStateSnapshotDto> chartData) {
    final spots = <FlSpot>[];
    
    for (int i = 0; i < chartData.length; i++) {
      final value = _extractValue(chartData[i]);
      if (value != null) {
        spots.add(FlSpot(i.toDouble(), value));
      }
    }
    
    return spots;
  }

  // 차트 타입별 데이터 추출
  double? _extractValue(HomeStateSnapshotDto snapshot) {
    switch (chartType) {
      case 'temperature':
        return snapshot.bathroomTempCelsius?.toDouble();
      case 'sound':
        return snapshot.livingroomSoundDb?.toDouble();
      case 'gas':
        return snapshot.kitchenMq5GasPpm?.toDouble();
      case 'motion':
        return _getMotionValue(snapshot);
      default:
        return null;
    }
  }

  List<double> _extractValues(List<HomeStateSnapshotDto> chartData) {
    return chartData
        .map((snapshot) => _extractValue(snapshot))
        .where((value) => value != null)
        .map((value) => value!)
        .toList();
  }

  double _getMotionValue(HomeStateSnapshotDto snapshot) {
    int motionCount = 0;
    if (snapshot.entrancePirMotion ?? false) motionCount++;
    if (snapshot.livingroomPir1Motion ?? false) motionCount++;
    if (snapshot.livingroomPir2Motion ?? false) motionCount++;
    if (snapshot.kitchenPirMotion ?? false) motionCount++;
    if (snapshot.bedroomPirMotion ?? false) motionCount++;
    if (snapshot.bathroomPirMotion ?? false) motionCount++;
    return motionCount.toDouble();
  }

  // 차트 설정
  IconData _getChartIcon() {
    switch (chartType) {
      case 'temperature':
        return Icons.thermostat;
      case 'sound':
        return Icons.volume_up;
      case 'gas':
        return Icons.air;
      case 'motion':
        return Icons.sensors;
      default:
        return Icons.show_chart;
    }
  }

  String _getChartTitle() {
    switch (chartType) {
      case 'temperature':
        return '온도 모니터링';
      case 'sound':
        return '소음 모니터링';
      case 'gas':
        return '가스 모니터링';
      case 'motion':
        return '모션 감지';
      default:
        return '센서 데이터';
    }
  }

  Color _getChartColor() {
    switch (chartType) {
      case 'temperature':
        return AppColors.alertAttention;
      case 'sound':
        return AppColors.alertWarning;
      case 'gas':
        return AppColors.alertEmergency;
      case 'motion':
        return AppColors.highlightSuccess;
      default:
        return AppColors.accentCalm;
    }
  }

  String _getCurrentValue() {
    if (snapshots.isEmpty) return 'N/A';
    
    final latest = snapshots.last;
    final value = _extractValue(latest);
    
    if (value == null) return 'N/A';
    
    switch (chartType) {
      case 'temperature':
        return '${value.toStringAsFixed(1)}°C';
      case 'sound':
        return '${value.toStringAsFixed(1)}dB';
      case 'gas':
        return '${value.toStringAsFixed(1)}ppm';
      case 'motion':
        return '${value.toInt()}개';
      default:
        return value.toStringAsFixed(1);
    }
  }

  double _getGridInterval() {
    switch (chartType) {
      case 'temperature':
        return 5.0;
      case 'sound':
        return 10.0;
      case 'gas':
        return 50.0;
      case 'motion':
        return 1.0;
      default:
        return 10.0;
    }
  }

  double _getLeftTitleInterval() {
    switch (chartType) {
      case 'temperature':
        return 5.0;
      case 'sound':
        return 10.0;
      case 'gas':
        return 50.0;
      case 'motion':
        return 1.0;
      default:
        return 10.0;
    }
  }

  double _getBottomTitleInterval() {
    final interval = (maxDataPoints / 5).ceil().toDouble();
    return interval > 0 ? interval : 1.0;
  }

  double _getMinY() {
    final values = _extractValues(_prepareChartData());
    if (values.isEmpty) return 0.0;
    
    final min = values.reduce((a, b) => a < b ? a : b);
    return (min * 0.9).floorToDouble();
  }

  double _getMaxY() {
    final values = _extractValues(_prepareChartData());
    if (values.isEmpty) return 100.0;
    
    final max = values.reduce((a, b) => a > b ? a : b);
    return (max * 1.1).ceilToDouble();
  }

  // 포맷팅 메서드들
  String _formatTime(DateTime time) {
    final now = DateTime.now();
    final difference = now.difference(time);
    
    if (difference.inMinutes < 1) {
      return '방금';
    } else if (difference.inMinutes < 60) {
      return '${difference.inMinutes}분';
    } else if (difference.inHours < 24) {
      return '${difference.inHours}시간';
    } else {
      return '${difference.inDays}일';
    }
  }

  String _formatYAxisValue(double value) {
    switch (chartType) {
      case 'temperature':
        return '${value.toInt()}°C';
      case 'sound':
        return '${value.toInt()}dB';
      case 'gas':
        return '${value.toInt()}ppm';
      case 'motion':
        return '${value.toInt()}';
      default:
        return value.toStringAsFixed(0);
    }
  }

  String _formatTooltipValue(HomeStateSnapshotDto snapshot) {
    final value = _extractValue(snapshot);
    if (value == null) return 'N/A';
    
    switch (chartType) {
      case 'temperature':
        return '${value.toStringAsFixed(1)}°C';
      case 'sound':
        return '${value.toStringAsFixed(1)}dB';
      case 'gas':
        return '${value.toStringAsFixed(1)}ppm';
      case 'motion':
        return '${value.toInt()}개 센서';
      default:
        return value.toStringAsFixed(1);
    }
  }

  String _formatStatValue(double value) {
    switch (chartType) {
      case 'temperature':
        return '${value.toStringAsFixed(1)}°C';
      case 'sound':
        return '${value.toStringAsFixed(1)}dB';
      case 'gas':
        return '${value.toStringAsFixed(1)}ppm';
      case 'motion':
        return '${value.toStringAsFixed(1)}';
      default:
        return value.toStringAsFixed(1);
    }
  }
}
