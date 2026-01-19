"""
data_collector 모듈 테스트
"""

import pytest
import sys
import os

# 상위 디렉토리를 경로에 추가
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_collector import FlightDataCollector


class TestFlightDataCollector:
    """FlightDataCollector 테스트 클래스"""
    
    def test_initialization(self):
        """초기화 테스트"""
        collector = FlightDataCollector("TEST-001")
        assert collector.aircraft_id == "TEST-001"
        assert len(collector.data_buffer) == 0
    
    def test_collect_sensor_data(self):
        """센서 데이터 수집 테스트"""
        collector = FlightDataCollector("TEST-001")
        data = collector.collect_sensor_data()
        
        # 필수 필드 확인
        assert 'timestamp' in data
        assert 'aircraft_id' in data
        assert 'altitude' in data
        assert 'speed' in data
        assert 'heading' in data
        assert 'latitude' in data
        assert 'longitude' in data
        assert 'fuel_level' in data
        assert 'engine_temp' in data
        
        # 항공기 ID 확인
        assert data['aircraft_id'] == "TEST-001"
        
        # 버퍼 확인
        assert len(collector.data_buffer) == 1
    
    def test_altitude_range(self):
        """고도 범위 테스트"""
        collector = FlightDataCollector("TEST-001")
        data = collector.collect_sensor_data()
        
        assert 1000 <= data['altitude'] <= 10000
    
    def test_speed_range(self):
        """속도 범위 테스트"""
        collector = FlightDataCollector("TEST-001")
        data = collector.collect_sensor_data()
        
        assert 200 <= data['speed'] <= 900
    
    def test_heading_range(self):
        """방향 범위 테스트"""
        collector = FlightDataCollector("TEST-001")
        data = collector.collect_sensor_data()
        
        assert 0 <= data['heading'] <= 360
    
    def test_latitude_range(self):
        """위도 범위 테스트"""
        collector = FlightDataCollector("TEST-001")
        data = collector.collect_sensor_data()
        
        assert -90 <= data['latitude'] <= 90
    
    def test_longitude_range(self):
        """경도 범위 테스트"""
        collector = FlightDataCollector("TEST-001")
        data = collector.collect_sensor_data()
        
        assert -180 <= data['longitude'] <= 180
    
    def test_fuel_level_range(self):
        """연료량 범위 테스트"""
        collector = FlightDataCollector("TEST-001")
        data = collector.collect_sensor_data()
        
        assert 0 <= data['fuel_level'] <= 100
    
    def test_engine_temp_range(self):
        """엔진 온도 범위 테스트"""
        collector = FlightDataCollector("TEST-001")
        data = collector.collect_sensor_data()
        
        assert 200 <= data['engine_temp'] <= 800
    
    def test_multiple_collections(self):
        """다중 수집 테스트"""
        collector = FlightDataCollector("TEST-001")
        
        for i in range(5):
            collector.collect_sensor_data()
        
        assert len(collector.data_buffer) == 5
    
    def test_get_buffer_data(self):
        """버퍼 데이터 조회 테스트"""
        collector = FlightDataCollector("TEST-001")
        collector.collect_sensor_data()
        collector.collect_sensor_data()
        
        buffer = collector.get_buffer_data()
        assert len(buffer) == 2
        assert isinstance(buffer, list)
    
    def test_clear_buffer(self):
        """버퍼 초기화 테스트"""
        collector = FlightDataCollector("TEST-001")
        collector.collect_sensor_data()
        collector.collect_sensor_data()
        
        assert len(collector.data_buffer) == 2
        
        collector.clear_buffer()
        assert len(collector.data_buffer) == 0
    
    def test_save_to_file(self, tmp_path):
        """파일 저장 테스트"""
        collector = FlightDataCollector("TEST-001")
        collector.collect_sensor_data()
        
        # 임시 파일 경로
        file_path = tmp_path / "test_data.json"
        
        collector.save_to_file(str(file_path))
        
        # 파일 존재 확인
        assert file_path.exists()
        
        # 파일 내용 확인
        import json
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        assert len(data) == 1
        assert data[0]['aircraft_id'] == "TEST-001"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
