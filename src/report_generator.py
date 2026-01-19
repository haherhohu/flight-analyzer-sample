"""
보고서 생성 모듈
Report Generator Module

분석 결과를 바탕으로 자동 보고서를 생성합니다.
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Optional


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ReportGenerator:
    """보고서 생성 클래스"""
    
    def __init__(self, aircraft_id: str):
        self.aircraft_id = aircraft_id
        logger.info(f"ReportGenerator initialized for aircraft: {aircraft_id}")
    
    def generate_html_report(
        self, 
        analysis: Dict, 
        risk_assessment: Dict, 
        anomalies: List[Dict],
        output_file: str = "flight_report.html"
    ) -> str:
        """
        HTML 형식의 보고서 생성
        
        Args:
            analysis: 분석 결과
            risk_assessment: 위험도 평가
            anomalies: 이상 패턴 리스트
            output_file: 출력 파일명
            
        Returns:
            생성된 보고서 파일 경로
        """
        html_content = f"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>비행 데이터 분석 보고서</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .header {{
            background-color: #2c3e50;
            color: white;
            padding: 20px;
            border-radius: 5px;
            margin-bottom: 20px;
        }}
        .section {{
            background-color: white;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .metric {{
            display: inline-block;
            margin: 10px 20px 10px 0;
        }}
        .metric-label {{
            font-weight: bold;
            color: #555;
        }}
        .metric-value {{
            font-size: 1.2em;
            color: #2c3e50;
        }}
        .risk-low {{ color: #27ae60; }}
        .risk-medium {{ color: #f39c12; }}
        .risk-high {{ color: #e74c3c; }}
        .anomaly {{
            background-color: #fff3cd;
            border-left: 4px solid #f39c12;
            padding: 10px;
            margin: 10px 0;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background-color: #34495e;
            color: white;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>비행 데이터 분석 보고서</h1>
        <p>항공기 ID: {self.aircraft_id}</p>
        <p>생성 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    
    <div class="section">
        <h2>비행 패턴 분석</h2>
        <div class="metric">
            <span class="metric-label">총 샘플 수:</span>
            <span class="metric-value">{analysis.get('total_samples', 0)}</span>
        </div>
        <div class="metric">
            <span class="metric-label">평균 고도:</span>
            <span class="metric-value">{analysis.get('avg_altitude', 0):.2f} m</span>
        </div>
        <div class="metric">
            <span class="metric-label">평균 속도:</span>
            <span class="metric-value">{analysis.get('avg_speed', 0):.2f} km/h</span>
        </div>
        <div class="metric">
            <span class="metric-label">평균 연료량:</span>
            <span class="metric-value">{analysis.get('avg_fuel_level', 0):.2f} %</span>
        </div>
        <div class="metric">
            <span class="metric-label">비행 단계:</span>
            <span class="metric-value">{analysis.get('flight_phase', 'UNKNOWN')}</span>
        </div>
        <div class="metric">
            <span class="metric-label">연료 소비율:</span>
            <span class="metric-value">{analysis.get('fuel_consumption_rate', 0):.2f} %/h</span>
        </div>
    </div>
    
    <div class="section">
        <h2>위험도 평가</h2>
        <div class="metric">
            <span class="metric-label">위험도 점수:</span>
            <span class="metric-value">{risk_assessment.get('risk_score', 0)}</span>
        </div>
        <div class="metric">
            <span class="metric-label">위험 등급:</span>
            <span class="metric-value risk-{risk_assessment.get('risk_level', 'low').lower()}">
                {risk_assessment.get('risk_level', 'UNKNOWN')}
            </span>
        </div>
        <h3>위험 요인</h3>
        <ul>
            {''.join(f'<li>{factor}</li>' for factor in risk_assessment.get('risk_factors', []))}
        </ul>
    </div>
    
    <div class="section">
        <h2>탐지된 이상 패턴</h2>
        {self._generate_anomaly_section(anomalies)}
    </div>
    
    <div class="section">
        <h2>권장 사항</h2>
        {self._generate_recommendations(analysis, risk_assessment, anomalies)}
    </div>
</body>
</html>
"""
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            logger.info(f"HTML report generated: {output_file}")
            return output_file
        except Exception as e:
            logger.error(f"Error generating HTML report: {e}")
            raise
    
    def _generate_anomaly_section(self, anomalies: List[Dict]) -> str:
        """이상 패턴 섹션 생성"""
        if not anomalies:
            return '<p>탐지된 이상 패턴이 없습니다.</p>'
        
        html = f'<p>총 {len(anomalies)}개의 이상 패턴이 탐지되었습니다.</p>'
        
        for anomaly in anomalies:
            html += f'''
            <div class="anomaly">
                <strong>시각:</strong> {anomaly.get('timestamp', 'N/A')}<br>
                <strong>항공기:</strong> {anomaly.get('aircraft_id', 'N/A')}<br>
                <strong>이상 내용:</strong>
                <ul>
                    {''.join(f'<li>{a}</li>' for a in anomaly.get('anomalies', []))}
                </ul>
            </div>
            '''
        
        return html
    
    def _generate_recommendations(
        self, 
        analysis: Dict, 
        risk_assessment: Dict, 
        anomalies: List[Dict]
    ) -> str:
        """권장 사항 생성"""
        recommendations = []
        
        # 위험도에 따른 권장사항
        if risk_assessment.get('risk_level') == 'HIGH':
            recommendations.append('즉시 비행 상태를 점검하고 필요시 비상 착륙을 준비하십시오.')
        elif risk_assessment.get('risk_level') == 'MEDIUM':
            recommendations.append('비행 파라미터를 주의 깊게 모니터링하십시오.')
        
        # 연료 관련 권장사항
        if analysis.get('avg_fuel_level', 100) < 30:
            recommendations.append('연료량이 낮습니다. 가장 가까운 공항으로 회항을 고려하십시오.')
        
        # 이상 패턴 관련 권장사항
        if len(anomalies) > 5:
            recommendations.append('다수의 이상 패턴이 탐지되었습니다. 시스템 점검이 필요합니다.')
        
        # 기본 권장사항
        if not recommendations:
            recommendations.append('현재 비행 상태는 정상입니다. 계속 모니터링을 유지하십시오.')
        
        html = '<ul>'
        for rec in recommendations:
            html += f'<li>{rec}</li>'
        html += '</ul>'
        
        return html
    
    def generate_json_report(
        self,
        analysis: Dict,
        risk_assessment: Dict,
        anomalies: List[Dict],
        output_file: str = "flight_report.json"
    ) -> str:
        """
        JSON 형식의 보고서 생성
        
        Args:
            analysis: 분석 결과
            risk_assessment: 위험도 평가
            anomalies: 이상 패턴 리스트
            output_file: 출력 파일명
            
        Returns:
            생성된 보고서 파일 경로
        """
        report = {
            'aircraft_id': self.aircraft_id,
            'generated_at': datetime.now().isoformat(),
            'analysis': analysis,
            'risk_assessment': risk_assessment,
            'anomalies': anomalies
        }
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            logger.info(f"JSON report generated: {output_file}")
            return output_file
        except Exception as e:
            logger.error(f"Error generating JSON report: {e}")
            raise
    
    def generate_summary(self, analysis: Dict, risk_assessment: Dict) -> str:
        """
        요약 텍스트 생성
        
        Args:
            analysis: 분석 결과
            risk_assessment: 위험도 평가
            
        Returns:
            요약 텍스트
        """
        summary = f"""
=== 비행 데이터 분석 요약 ===
항공기: {self.aircraft_id}
시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

[비행 패턴]
- 총 샘플: {analysis.get('total_samples', 0)}개
- 평균 고도: {analysis.get('avg_altitude', 0):.2f}m
- 평균 속도: {analysis.get('avg_speed', 0):.2f}km/h
- 비행 단계: {analysis.get('flight_phase', 'UNKNOWN')}

[위험도 평가]
- 위험 등급: {risk_assessment.get('risk_level', 'UNKNOWN')}
- 위험 점수: {risk_assessment.get('risk_score', 0)}
- 탐지된 이상: {analysis.get('anomaly_count', 0)}건
"""
        return summary


def main():
    """메인 함수"""
    # 테스트 데이터
    test_analysis = {
        'total_samples': 100,
        'avg_altitude': 5000.0,
        'avg_speed': 650.0,
        'avg_fuel_level': 55.0,
        'flight_phase': 'CRUISE',
        'fuel_consumption_rate': 5.2,
        'anomaly_count': 2
    }
    
    test_risk = {
        'risk_score': 25,
        'risk_level': 'MEDIUM',
        'risk_factors': ['2 anomalies detected']
    }
    
    test_anomalies = [
        {
            'timestamp': '2026-01-19T10:00:00',
            'aircraft_id': 'AIRCRAFT-001',
            'anomalies': ['WARNING: High engine temperature (720.00°C)']
        }
    ]
    
    generator = ReportGenerator('AIRCRAFT-001')
    
    # HTML 보고서 생성
    html_file = generator.generate_html_report(test_analysis, test_risk, test_anomalies)
    print(f"HTML report generated: {html_file}")
    
    # JSON 보고서 생성
    json_file = generator.generate_json_report(test_analysis, test_risk, test_anomalies)
    print(f"JSON report generated: {json_file}")
    
    # 요약 출력
    summary = generator.generate_summary(test_analysis, test_risk)
    print(summary)


if __name__ == "__main__":
    main()
