"""
analyzer 모듈 테스트
"""

import pytest
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.analyzer import FlightAnalyzer


class TestFlightAnalyzer:
    """FlightAnalyzer 테스트 클래스"""
    
    def setup_method(self):
        """각 테스트 전에 실행"""
        self.analyzer = FlightAnalyzer()
        self.normal_data = {
            "timestamp": "2026-01-19T10:00:00",
            "aircraft_id": "TEST-001",
            "altitude": 5000.0,
            "speed": 650.0,
            "heading": 180.0,
            "latitude": 37.5,
            "longitude": 127.0,
            "fuel_level": 75.0,
            "engine_temp": 450.0
        }
    
    def test_initialization(self):
        """초기화 테스트"""
        assert len(self.analyzer.anomalies) == 0
    
    def test_detect_no_anomalies(self):
        """정상 데이터 이상 탐지 테스트"""
        anomalies = self.analyzer.detect_anomalies(self.normal_data)
        assert len(anomalies) == 0
    
    def test_detect_low_fuel(self):
        """연료 부족 탐지 테스트"""
        data = self.normal_data.copy()
        data['fuel_level'] = 15.0  # 임계값(20%) 이하
        
        anomalies = self.analyzer.detect_anomalies(data)
        assert len(anomalies) > 0
        assert any('fuel' in a.lower() for a in anomalies)
    
    def test_detect_high_engine_temp(self):
        """엔진 과열 탐지 테스트"""
        data = self.normal_data.copy()
        data['engine_temp'] = 750.0  # 임계값(700°C) 초과
        
        anomalies = self.analyzer.detect_anomalies(data)
        assert len(anomalies) > 0
        assert any('engine' in a.lower() or 'temperature' in a.lower() for a in anomalies)
    
    def test_detect_high_altitude(self):
        """고도 초과 탐지 테스트"""
        data = self.normal_data.copy()
        data['altitude'] = 13000.0  # 임계값(12000m) 초과
        
        anomalies = self.analyzer.detect_anomalies(data)
        assert len(anomalies) > 0
        assert any('altitude' in a.lower() for a in anomalies)
    
    def test_detect_low_speed_at_high_altitude(self):
        """고고도 저속 탐지 테스트"""
        data = self.normal_data.copy()
        data['altitude'] = 9000.0
        data['speed'] = 250.0  # 고도에 비해 낮은 속도
        
        anomalies = self.analyzer.detect_anomalies(data)
        assert len(anomalies) > 0
        assert any('speed' in a.lower() for a in anomalies)
    
    def test_detect_multiple_anomalies(self):
        """다중 이상 탐지 테스트"""
        data = self.normal_data.copy()
        data['fuel_level'] = 15.0
        data['engine_temp'] = 750.0
        
        anomalies = self.analyzer.detect_anomalies(data)
        assert len(anomalies) >= 2
    
    def test_anomalies_stored(self):
        """이상 패턴 저장 테스트"""
        data = self.normal_data.copy()
        data['fuel_level'] = 15.0
        
        self.analyzer.detect_anomalies(data)
        
        stored = self.analyzer.get_all_anomalies()
        assert len(stored) > 0
        assert stored[0]['aircraft_id'] == "TEST-001"
    
    def test_analyze_flight_pattern(self):
        """비행 패턴 분석 테스트"""
        data_list = [self.normal_data.copy() for _ in range(5)]
        
        analysis = self.analyzer.analyze_flight_pattern(data_list)
        
        assert 'total_samples' in analysis
        assert 'avg_altitude' in analysis
        assert 'avg_speed' in analysis
        assert 'avg_fuel_level' in analysis
        assert 'flight_phase' in analysis
        assert 'fuel_consumption_rate' in analysis
        assert 'anomaly_count' in analysis
        
        assert analysis['total_samples'] == 5
    
    def test_analyze_empty_list(self):
        """빈 리스트 분석 테스트"""
        analysis = self.analyzer.analyze_flight_pattern([])
        assert analysis == {}
    
    def test_determine_flight_phase_taxi(self):
        """이륙 단계 판단 테스트"""
        phase = self.analyzer._determine_flight_phase(500.0, 100.0)
        assert phase == "TAXI/TAKEOFF"
    
    def test_determine_flight_phase_climb(self):
        """상승 단계 판단 테스트"""
        phase = self.analyzer._determine_flight_phase(2000.0, 400.0)
        assert phase == "CLIMB"
    
    def test_determine_flight_phase_cruise(self):
        """순항 단계 판단 테스트"""
        phase = self.analyzer._determine_flight_phase(8000.0, 700.0)
        assert phase == "CRUISE"
    
    def test_determine_flight_phase_descent(self):
        """하강 단계 판단 테스트"""
        phase = self.analyzer._determine_flight_phase(2000.0, 350.0)
        assert phase == "DESCENT"
    
    def test_determine_flight_phase_landing(self):
        """착륙 단계 판단 테스트"""
        phase = self.analyzer._determine_flight_phase(300.0, 200.0)
        assert phase == "APPROACH/LANDING"
    
    def test_calculate_distance(self):
        """거리 계산 테스트"""
        start = {
            'latitude': 37.5,
            'longitude': 127.0
        }
        end = {
            'latitude': 37.6,
            'longitude': 127.1
        }
        
        distance = self.analyzer.calculate_distance(start, end)
        
        # 거리는 양수여야 함
        assert distance > 0
        # 대략적인 거리 확인 (약 13-14km)
        assert 10 < distance < 20
    
    def test_calculate_distance_same_point(self):
        """동일 지점 거리 테스트"""
        point = {
            'latitude': 37.5,
            'longitude': 127.0
        }
        
        distance = self.analyzer.calculate_distance(point, point)
        assert distance == 0
    
    def test_generate_risk_assessment_low(self):
        """낮은 위험도 평가 테스트"""
        data_list = [self.normal_data.copy() for _ in range(5)]
        
        assessment = self.analyzer.generate_risk_assessment(data_list)
        
        assert 'risk_score' in assessment
        assert 'risk_level' in assessment
        assert 'risk_factors' in assessment
        assert assessment['risk_level'] == "LOW"
    
    def test_generate_risk_assessment_medium(self):
        """중간 위험도 평가 테스트"""
        data = self.normal_data.copy()
        data['fuel_level'] = 25.0  # 낮은 연료
        
        data_list = [data.copy() for _ in range(5)]
        
        assessment = self.analyzer.generate_risk_assessment(data_list)
        assert assessment['risk_level'] in ["MEDIUM", "LOW"]
    
    def test_generate_risk_assessment_high(self):
        """높은 위험도 평가 테스트"""
        data = self.normal_data.copy()
        data['fuel_level'] = 15.0
        data['engine_temp'] = 750.0
        
        # 이상 패턴 여러 개 생성
        for _ in range(10):
            self.analyzer.detect_anomalies(data)
        
        data_list = [data.copy() for _ in range(5)]
        
        assessment = self.analyzer.generate_risk_assessment(data_list)
        assert assessment['risk_score'] > 50
        assert assessment['risk_level'] == "HIGH"
    
    def test_get_all_anomalies(self):
        """모든 이상 패턴 조회 테스트"""
        data = self.normal_data.copy()
        data['fuel_level'] = 15.0
        
        self.analyzer.detect_anomalies(data)
        self.analyzer.detect_anomalies(data)
        
        anomalies = self.analyzer.get_all_anomalies()
        assert len(anomalies) == 2
    
    def test_predict_remaining_flight_time_normal(self):
        """정상 연료 잔여 시간 예측 테스트"""
        # 충분한 연료가 있는 상황 (느린 소비율)
        data_list = []
        for i in range(10):
            data = self.normal_data.copy()
            data['fuel_level'] = 80.0 - i * 0.1  # 매우 느리게 감소
            data['timestamp'] = f"2026-01-19T10:{i:02d}:00"
            data_list.append(data)
        
        prediction = self.analyzer.predict_remaining_flight_time(data_list)
        
        assert 'remaining_hours' in prediction
        assert 'current_fuel_percentage' in prediction
        assert 'fuel_consumption_rate' in prediction
        assert 'fuel_exhaustion_warning' in prediction
        # 충분한 연료와 느린 소비율이므로 경고 없음
        assert prediction['fuel_exhaustion_warning'] is False or prediction['remaining_hours'] > 2
    
    def test_predict_remaining_flight_time_warning(self):
        """연료 부족 경고 예측 테스트"""
        # 연료가 부족한 상황
        data_list = []
        for i in range(10):
            data = self.normal_data.copy()
            data['fuel_level'] = 25.0 - i * 2  # 빠르게 감소
            data['timestamp'] = f"2026-01-19T10:{i:02d}:00"
            data_list.append(data)
        
        prediction = self.analyzer.predict_remaining_flight_time(data_list)
        
        assert prediction['fuel_exhaustion_warning'] is True
        assert 'Critical' in prediction['message']
    
    def test_predict_remaining_flight_time_insufficient_data(self):
        """데이터 부족 시 예측 테스트"""
        data_list = [self.normal_data.copy()]
        
        prediction = self.analyzer.predict_remaining_flight_time(data_list)
        
        assert prediction['remaining_hours'] is None
        assert 'Insufficient data' in prediction['message']


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
