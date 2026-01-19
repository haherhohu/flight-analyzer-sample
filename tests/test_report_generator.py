"""
report_generator 모듈 테스트
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.report_generator import ReportGenerator


class TestReportGenerator:
    """ReportGenerator 테스트 클래스"""
    
    def setup_method(self):
        """각 테스트 전에 실행"""
        self.generator = ReportGenerator("TEST-001")
        self.test_analysis = {
            'total_samples': 100,
            'avg_altitude': 5000.0,
            'avg_speed': 650.0,
            'avg_fuel_level': 55.0,
            'flight_phase': 'CRUISE',
            'fuel_consumption_rate': 5.2,
            'anomaly_count': 2
        }
        self.test_risk = {
            'risk_score': 25,
            'risk_level': 'MEDIUM',
            'risk_factors': ['2 anomalies detected']
        }
        self.test_anomalies = [
            {
                'timestamp': '2026-01-19T10:00:00',
                'aircraft_id': 'TEST-001',
                'anomalies': ['WARNING: High engine temperature (720.00°C)']
            }
        ]
    
    def test_initialization(self):
        """초기화 테스트"""
        assert self.generator.aircraft_id == "TEST-001"
    
    def test_generate_html_report(self, tmp_path):
        """HTML 보고서 생성 테스트"""
        output_file = str(tmp_path / "test_report.html")
        
        result = self.generator.generate_html_report(
            self.test_analysis,
            self.test_risk,
            self.test_anomalies,
            output_file
        )
        
        assert result == output_file
        assert os.path.exists(output_file)
        
        # 파일 내용 확인
        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        assert 'TEST-001' in content
        assert 'CRUISE' in content
        assert 'MEDIUM' in content
    
    def test_generate_html_report_no_anomalies(self, tmp_path):
        """이상 패턴 없는 HTML 보고서 생성 테스트"""
        output_file = str(tmp_path / "test_report_no_anomalies.html")
        
        result = self.generator.generate_html_report(
            self.test_analysis,
            self.test_risk,
            [],
            output_file
        )
        
        assert os.path.exists(output_file)
        
        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        assert '탐지된 이상 패턴이 없습니다' in content
    
    def test_generate_json_report(self, tmp_path):
        """JSON 보고서 생성 테스트"""
        import json
        
        output_file = str(tmp_path / "test_report.json")
        
        result = self.generator.generate_json_report(
            self.test_analysis,
            self.test_risk,
            self.test_anomalies,
            output_file
        )
        
        assert result == output_file
        assert os.path.exists(output_file)
        
        # JSON 파일 읽기
        with open(output_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        assert data['aircraft_id'] == 'TEST-001'
        assert 'analysis' in data
        assert 'risk_assessment' in data
        assert 'anomalies' in data
        assert 'generated_at' in data
    
    def test_generate_summary(self):
        """요약 생성 테스트"""
        summary = self.generator.generate_summary(
            self.test_analysis,
            self.test_risk
        )
        
        assert isinstance(summary, str)
        assert 'TEST-001' in summary
        assert 'CRUISE' in summary
        assert 'MEDIUM' in summary
        assert '100' in summary  # total_samples
    
    def test_generate_summary_format(self):
        """요약 형식 테스트"""
        summary = self.generator.generate_summary(
            self.test_analysis,
            self.test_risk
        )
        
        # 필수 섹션 확인
        assert '비행 패턴' in summary
        assert '위험도 평가' in summary
        assert '평균 고도' in summary
        assert '평균 속도' in summary
    
    def test_generate_anomaly_section_empty(self):
        """빈 이상 패턴 섹션 생성 테스트"""
        section = self.generator._generate_anomaly_section([])
        assert '탐지된 이상 패턴이 없습니다' in section
    
    def test_generate_anomaly_section_with_data(self):
        """데이터 있는 이상 패턴 섹션 생성 테스트"""
        section = self.generator._generate_anomaly_section(self.test_anomalies)
        
        assert '1개의 이상 패턴이 탐지되었습니다' in section
        assert 'TEST-001' in section
        assert 'High engine temperature' in section
    
    def test_generate_recommendations_high_risk(self):
        """높은 위험도 권장사항 테스트"""
        high_risk = {
            'risk_level': 'HIGH',
            'risk_score': 80,
            'risk_factors': ['Multiple issues']
        }
        
        recommendations = self.generator._generate_recommendations(
            self.test_analysis,
            high_risk,
            self.test_anomalies
        )
        
        assert '즉시' in recommendations or '비상' in recommendations
    
    def test_generate_recommendations_medium_risk(self):
        """중간 위험도 권장사항 테스트"""
        recommendations = self.generator._generate_recommendations(
            self.test_analysis,
            self.test_risk,
            self.test_anomalies
        )
        
        assert '모니터링' in recommendations or '주의' in recommendations
    
    def test_generate_recommendations_low_fuel(self):
        """낮은 연료 권장사항 테스트"""
        low_fuel_analysis = self.test_analysis.copy()
        low_fuel_analysis['avg_fuel_level'] = 25.0
        
        recommendations = self.generator._generate_recommendations(
            low_fuel_analysis,
            self.test_risk,
            self.test_anomalies
        )
        
        assert '연료' in recommendations
    
    def test_generate_recommendations_many_anomalies(self):
        """다수 이상 패턴 권장사항 테스트"""
        many_anomalies = [self.test_anomalies[0] for _ in range(10)]
        
        recommendations = self.generator._generate_recommendations(
            self.test_analysis,
            self.test_risk,
            many_anomalies
        )
        
        assert '시스템 점검' in recommendations or '다수' in recommendations
    
    def test_generate_recommendations_normal(self):
        """정상 상태 권장사항 테스트"""
        low_risk = {
            'risk_level': 'LOW',
            'risk_score': 10,
            'risk_factors': []
        }
        normal_analysis = self.test_analysis.copy()
        normal_analysis['avg_fuel_level'] = 80.0
        
        recommendations = self.generator._generate_recommendations(
            normal_analysis,
            low_risk,
            []
        )
        
        assert '정상' in recommendations


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
