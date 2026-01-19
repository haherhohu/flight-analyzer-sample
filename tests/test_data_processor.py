"""
data_processor 모듈 테스트
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_processor import DataProcessor


class TestDataProcessor:
    """DataProcessor 테스트 클래스"""
    
    def setup_method(self):
        """각 테스트 전에 실행"""
        self.processor = DataProcessor()
        self.valid_data = {
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
        assert self.processor.processed_count == 0
    
    def test_validate_valid_data(self):
        """유효한 데이터 검증 테스트"""
        result = self.processor.validate_data(self.valid_data)
        assert result is True
    
    def test_validate_missing_field(self):
        """필수 필드 누락 테스트"""
        invalid_data = self.valid_data.copy()
        del invalid_data['altitude']
        
        result = self.processor.validate_data(invalid_data)
        assert result is False
    
    def test_validate_invalid_altitude(self):
        """유효하지 않은 고도 테스트"""
        invalid_data = self.valid_data.copy()
        invalid_data['altitude'] = 20000.0  # 범위 초과
        
        result = self.processor.validate_data(invalid_data)
        assert result is False
    
    def test_validate_invalid_speed(self):
        """유효하지 않은 속도 테스트"""
        invalid_data = self.valid_data.copy()
        invalid_data['speed'] = 1500.0  # 범위 초과
        
        result = self.processor.validate_data(invalid_data)
        assert result is False
    
    def test_validate_invalid_heading(self):
        """유효하지 않은 방향 테스트"""
        invalid_data = self.valid_data.copy()
        invalid_data['heading'] = 400.0  # 범위 초과
        
        result = self.processor.validate_data(invalid_data)
        assert result is False
    
    def test_validate_invalid_latitude(self):
        """유효하지 않은 위도 테스트"""
        invalid_data = self.valid_data.copy()
        invalid_data['latitude'] = 100.0  # 범위 초과
        
        result = self.processor.validate_data(invalid_data)
        assert result is False
    
    def test_validate_invalid_longitude(self):
        """유효하지 않은 경도 테스트"""
        invalid_data = self.valid_data.copy()
        invalid_data['longitude'] = 200.0  # 범위 초과
        
        result = self.processor.validate_data(invalid_data)
        assert result is False
    
    def test_validate_invalid_fuel_level(self):
        """유효하지 않은 연료량 테스트"""
        invalid_data = self.valid_data.copy()
        invalid_data['fuel_level'] = 150.0  # 범위 초과
        
        result = self.processor.validate_data(invalid_data)
        assert result is False
    
    def test_validate_invalid_engine_temp(self):
        """유효하지 않은 엔진 온도 테스트"""
        invalid_data = self.valid_data.copy()
        invalid_data['engine_temp'] = 1500.0  # 범위 초과
        
        result = self.processor.validate_data(invalid_data)
        assert result is False
    
    def test_normalize_data(self):
        """데이터 정규화 테스트"""
        data = {
            "timestamp": "2026-01-19T10:00:00",
            "aircraft_id": "TEST-001",
            "altitude": 5432.123456,
            "speed": 650.789123,
            "heading": 180.456789,
            "latitude": 37.123456789,
            "longitude": 127.123456789,
            "fuel_level": 75.5555,
            "engine_temp": 450.2222
        }
        
        normalized = self.processor.normalize_data(data)
        
        assert normalized['altitude'] == 5432.12
        assert normalized['speed'] == 650.79
        assert normalized['heading'] == 180.46
        assert normalized['latitude'] == 37.123457
        assert normalized['longitude'] == 127.123457
        assert normalized['fuel_level'] == 75.56
        assert normalized['engine_temp'] == 450.22
    
    def test_normalize_increments_count(self):
        """정규화 시 카운터 증가 테스트"""
        initial_count = self.processor.processed_count
        self.processor.normalize_data(self.valid_data)
        assert self.processor.processed_count == initial_count + 1
    
    def test_calculate_statistics(self):
        """통계 계산 테스트"""
        data_list = [
            {"altitude": 1000.0},
            {"altitude": 2000.0},
            {"altitude": 3000.0},
            {"altitude": 4000.0},
            {"altitude": 5000.0}
        ]
        
        stats = self.processor.calculate_statistics(data_list, 'altitude')
        
        assert stats['count'] == 5
        assert stats['mean'] == 3000.0
        assert stats['median'] == 3000.0
        assert stats['min'] == 1000.0
        assert stats['max'] == 5000.0
        assert 'stdev' in stats
    
    def test_calculate_statistics_empty_list(self):
        """빈 리스트 통계 테스트"""
        stats = self.processor.calculate_statistics([], 'altitude')
        assert stats == {}
    
    def test_calculate_statistics_single_value(self):
        """단일 값 통계 테스트"""
        data_list = [{"altitude": 1000.0}]
        stats = self.processor.calculate_statistics(data_list, 'altitude')
        
        assert stats['count'] == 1
        assert stats['mean'] == 1000.0
        assert 'stdev' not in stats  # 단일 값은 표준편차 없음
    
    def test_filter_outliers(self):
        """이상치 필터링 테스트"""
        data_list = [
            {"altitude": 5000.0},
            {"altitude": 5100.0},
            {"altitude": 5200.0},
            {"altitude": 5300.0},
            {"altitude": 5400.0},
            {"altitude": 10000.0}  # 이상치
        ]
        
        filtered = self.processor.filter_outliers(data_list, 'altitude')
        
        # 이상치가 제거되었는지 확인
        assert len(filtered) < len(data_list)
    
    def test_filter_outliers_small_list(self):
        """작은 리스트 필터링 테스트"""
        data_list = [
            {"altitude": 5000.0},
            {"altitude": 5100.0}
        ]
        
        filtered = self.processor.filter_outliers(data_list, 'altitude')
        
        # 작은 리스트는 필터링하지 않음
        assert len(filtered) == len(data_list)
    
    def test_process_batch(self):
        """배치 처리 테스트"""
        data_list = [
            self.valid_data.copy(),
            self.valid_data.copy(),
            self.valid_data.copy()
        ]
        
        processed = self.processor.process_batch(data_list)
        
        assert len(processed) == 3
        assert all(isinstance(d, dict) for d in processed)
    
    def test_process_batch_with_invalid_data(self):
        """유효하지 않은 데이터 포함 배치 처리 테스트"""
        invalid_data = self.valid_data.copy()
        invalid_data['altitude'] = 20000.0  # 유효하지 않음
        
        data_list = [
            self.valid_data.copy(),
            invalid_data,
            self.valid_data.copy()
        ]
        
        processed = self.processor.process_batch(data_list)
        
        # 유효한 데이터만 처리됨
        assert len(processed) == 2
    
    def test_get_processed_count(self):
        """처리 카운트 조회 테스트"""
        self.processor.normalize_data(self.valid_data)
        self.processor.normalize_data(self.valid_data)
        
        count = self.processor.get_processed_count()
        assert count == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
