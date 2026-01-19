"""
데이터 처리 모듈
Data Processor Module

수집된 비행 데이터를 처리하고 정제합니다.
"""

import logging
from typing import Dict, List, Optional
import statistics


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataProcessor:
    """데이터 처리 클래스"""
    
    def __init__(self):
        self.processed_count = 0
        logger.info("DataProcessor initialized")
    
    def validate_data(self, data: Dict) -> bool:
        """
        데이터 유효성 검증
        
        Args:
            data: 검증할 데이터
            
        Returns:
            유효 여부
        """
        required_fields = [
            'timestamp', 'aircraft_id', 'altitude', 'speed',
            'heading', 'latitude', 'longitude', 'fuel_level', 'engine_temp'
        ]
        
        # 필수 필드 확인
        for field in required_fields:
            if field not in data:
                logger.warning(f"Missing required field: {field}")
                return False
        
        # 범위 검증
        if not (0 <= data['altitude'] <= 15000):
            logger.warning(f"Invalid altitude: {data['altitude']}")
            return False
        
        if not (0 <= data['speed'] <= 1000):
            logger.warning(f"Invalid speed: {data['speed']}")
            return False
        
        if not (0 <= data['heading'] <= 360):
            logger.warning(f"Invalid heading: {data['heading']}")
            return False
        
        if not (-90 <= data['latitude'] <= 90):
            logger.warning(f"Invalid latitude: {data['latitude']}")
            return False
        
        if not (-180 <= data['longitude'] <= 180):
            logger.warning(f"Invalid longitude: {data['longitude']}")
            return False
        
        if not (0 <= data['fuel_level'] <= 100):
            logger.warning(f"Invalid fuel level: {data['fuel_level']}")
            return False
        
        if not (0 <= data['engine_temp'] <= 1000):
            logger.warning(f"Invalid engine temperature: {data['engine_temp']}")
            return False
        
        return True
    
    def normalize_data(self, data: Dict) -> Dict:
        """
        데이터 정규화
        
        Args:
            data: 정규화할 데이터
            
        Returns:
            정규화된 데이터
        """
        normalized = data.copy()
        
        # 값 반올림
        normalized['altitude'] = round(data['altitude'], 2)
        normalized['speed'] = round(data['speed'], 2)
        normalized['heading'] = round(data['heading'], 2)
        normalized['latitude'] = round(data['latitude'], 6)
        normalized['longitude'] = round(data['longitude'], 6)
        normalized['fuel_level'] = round(data['fuel_level'], 2)
        normalized['engine_temp'] = round(data['engine_temp'], 2)
        
        self.processed_count += 1
        logger.debug(f"Data normalized: {normalized}")
        
        return normalized
    
    def filter_outliers(self, data_list: List[Dict], field: str) -> List[Dict]:
        """
        이상치 필터링 (IQR 방식)
        
        Args:
            data_list: 데이터 리스트
            field: 필터링할 필드명
            
        Returns:
            필터링된 데이터 리스트
        """
        if len(data_list) < 4:
            return data_list
        
        values = [d[field] for d in data_list if field in d]
        
        if not values:
            return data_list
        
        # Q1, Q3 계산
        sorted_values = sorted(values)
        n = len(sorted_values)
        q1 = sorted_values[n // 4]
        q3 = sorted_values[(3 * n) // 4]
        iqr = q3 - q1
        
        # 이상치 범위
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        
        # 필터링
        filtered = [
            d for d in data_list
            if field in d and lower_bound <= d[field] <= upper_bound
        ]
        
        removed = len(data_list) - len(filtered)
        if removed > 0:
            logger.info(f"Removed {removed} outliers from field '{field}'")
        
        return filtered
    
    def calculate_statistics(self, data_list: List[Dict], field: str) -> Dict:
        """
        통계 계산
        
        Args:
            data_list: 데이터 리스트
            field: 통계를 계산할 필드명
            
        Returns:
            통계 딕셔너리
        """
        values = [d[field] for d in data_list if field in d]
        
        if not values:
            return {}
        
        stats = {
            'count': len(values),
            'mean': statistics.mean(values),
            'median': statistics.median(values),
            'min': min(values),
            'max': max(values)
        }
        
        if len(values) > 1:
            stats['stdev'] = statistics.stdev(values)
        
        logger.info(f"Statistics for {field}: {stats}")
        return stats
    
    def process_batch(self, data_list: List[Dict]) -> List[Dict]:
        """
        배치 데이터 처리
        
        Args:
            data_list: 처리할 데이터 리스트
            
        Returns:
            처리된 데이터 리스트
        """
        processed = []
        
        for data in data_list:
            if self.validate_data(data):
                normalized = self.normalize_data(data)
                processed.append(normalized)
            else:
                logger.warning(f"Skipping invalid data: {data.get('timestamp', 'unknown')}")
        
        logger.info(f"Processed {len(processed)}/{len(data_list)} records")
        return processed
    
    def get_processed_count(self) -> int:
        """처리된 데이터 개수 반환"""
        return self.processed_count


def main():
    """메인 함수"""
    # 테스트 데이터
    test_data = [
        {
            "timestamp": "2026-01-19T10:00:00",
            "aircraft_id": "AIRCRAFT-001",
            "altitude": 5432.123456,
            "speed": 650.789,
            "heading": 180.456,
            "latitude": 37.123456789,
            "longitude": 127.123456789,
            "fuel_level": 75.5,
            "engine_temp": 450.2
        }
    ]
    
    processor = DataProcessor()
    processed = processor.process_batch(test_data)
    
    print(f"Processed {len(processed)} records")
    if processed:
        print(f"Sample: {processed[0]}")


if __name__ == "__main__":
    main()
