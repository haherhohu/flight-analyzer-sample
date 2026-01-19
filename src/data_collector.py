"""
비행 데이터 수집 모듈
Flight Data Collector Module

이 모듈은 센서로부터 비행 데이터를 수집합니다.
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Optional
import random


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FlightDataCollector:
    """비행 데이터 수집 클래스"""
    
    def __init__(self, aircraft_id: str):
        """
        Args:
            aircraft_id: 항공기 식별자
        """
        self.aircraft_id = aircraft_id
        self.data_buffer: List[Dict] = []
        logger.info(f"FlightDataCollector initialized for aircraft: {aircraft_id}")
    
    def collect_sensor_data(self) -> Dict:
        """
        센서 데이터 수집
        
        Returns:
            센서 데이터 딕셔너리
        """
        try:
            data = {
                "timestamp": datetime.utcnow().isoformat(),
                "aircraft_id": self.aircraft_id,
                "altitude": self._read_altitude(),
                "speed": self._read_speed(),
                "heading": self._read_heading(),
                "latitude": self._read_latitude(),
                "longitude": self._read_longitude(),
                "fuel_level": self._read_fuel_level(),
                "engine_temp": self._read_engine_temp()
            }
            
            self.data_buffer.append(data)
            logger.debug(f"Collected data: {data}")
            return data
            
        except Exception as e:
            logger.error(f"Error collecting sensor data: {e}")
            raise
    
    def _read_altitude(self) -> float:
        """고도 센서 읽기 (미터)"""
        # 실제 구현에서는 센서 API를 호출
        return random.uniform(1000, 10000)
    
    def _read_speed(self) -> float:
        """속도 센서 읽기 (km/h)"""
        return random.uniform(200, 900)
    
    def _read_heading(self) -> float:
        """방향 센서 읽기 (도)"""
        return random.uniform(0, 360)
    
    def _read_latitude(self) -> float:
        """위도 센서 읽기"""
        return random.uniform(-90, 90)
    
    def _read_longitude(self) -> float:
        """경도 센서 읽기"""
        return random.uniform(-180, 180)
    
    def _read_fuel_level(self) -> float:
        """연료량 센서 읽기 (%)"""
        return random.uniform(0, 100)
    
    def _read_engine_temp(self) -> float:
        """엔진 온도 센서 읽기 (°C)"""
        return random.uniform(200, 800)
    
    def get_buffer_data(self) -> List[Dict]:
        """
        버퍼에 저장된 데이터 반환
        
        Returns:
            수집된 데이터 리스트
        """
        return self.data_buffer.copy()
    
    def clear_buffer(self):
        """데이터 버퍼 초기화"""
        self.data_buffer.clear()
        logger.info("Data buffer cleared")
    
    def save_to_file(self, filename: str):
        """
        수집된 데이터를 파일로 저장
        
        Args:
            filename: 저장할 파일 경로
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.data_buffer, f, indent=2, ensure_ascii=False)
            logger.info(f"Data saved to {filename}")
        except Exception as e:
            logger.error(f"Error saving data to file: {e}")
            raise


def main():
    """메인 함수"""
    collector = FlightDataCollector("AIRCRAFT-001")
    
    # 10회 데이터 수집 시뮬레이션
    for i in range(10):
        data = collector.collect_sensor_data()
        print(f"Sample {i+1}: Altitude={data['altitude']:.2f}m, Speed={data['speed']:.2f}km/h")
    
    # 파일로 저장
    collector.save_to_file("flight_data.json")
    print(f"Total collected samples: {len(collector.get_buffer_data())}")


if __name__ == "__main__":
    main()
