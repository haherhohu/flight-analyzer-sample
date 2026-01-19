"""
데이터 분석 모듈
Data Analyzer Module

비행 데이터를 분석하고 이상 패턴을 탐지합니다.
"""

import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FlightAnalyzer:
    """비행 데이터 분석 클래스"""
    
    # 임계값 설정
    CRITICAL_FUEL_LEVEL = 20.0  # %
    HIGH_ENGINE_TEMP = 700.0    # °C
    MAX_SAFE_ALTITUDE = 12000.0 # m
    
    def __init__(self):
        self.anomalies: List[Dict] = []
        logger.info("FlightAnalyzer initialized")
    
    def detect_anomalies(self, data: Dict) -> List[str]:
        """
        이상 패턴 탐지
        
        Args:
            data: 분석할 데이터
            
        Returns:
            탐지된 이상 패턴 리스트
        """
        anomalies = []
        
        # 연료 부족 확인
        if data.get('fuel_level', 100) < self.CRITICAL_FUEL_LEVEL:
            anomaly = f"CRITICAL: Low fuel level ({data['fuel_level']:.2f}%)"
            anomalies.append(anomaly)
            logger.warning(anomaly)
        
        # 엔진 과열 확인
        if data.get('engine_temp', 0) > self.HIGH_ENGINE_TEMP:
            anomaly = f"WARNING: High engine temperature ({data['engine_temp']:.2f}°C)"
            anomalies.append(anomaly)
            logger.warning(anomaly)
        
        # 고도 초과 확인
        if data.get('altitude', 0) > self.MAX_SAFE_ALTITUDE:
            anomaly = f"WARNING: Altitude exceeds safe limit ({data['altitude']:.2f}m)"
            anomalies.append(anomaly)
            logger.warning(anomaly)
        
        # 속도 이상 확인
        altitude = data.get('altitude', 0)
        speed = data.get('speed', 0)
        if altitude > 8000 and speed < 300:
            anomaly = "WARNING: Unusually low speed at high altitude"
            anomalies.append(anomaly)
            logger.warning(anomaly)
        
        if anomalies:
            self.anomalies.append({
                'timestamp': data.get('timestamp'),
                'aircraft_id': data.get('aircraft_id'),
                'anomalies': anomalies
            })
        
        return anomalies
    
    def analyze_flight_pattern(self, data_list: List[Dict]) -> Dict:
        """
        비행 패턴 분석
        
        Args:
            data_list: 분석할 데이터 리스트
            
        Returns:
            분석 결과 딕셔너리
        """
        if not data_list:
            return {}
        
        # 평균값 계산
        avg_altitude = sum(d['altitude'] for d in data_list) / len(data_list)
        avg_speed = sum(d['speed'] for d in data_list) / len(data_list)
        avg_fuel = sum(d['fuel_level'] for d in data_list) / len(data_list)
        
        # 비행 상태 판단
        flight_phase = self._determine_flight_phase(avg_altitude, avg_speed)
        
        # 연료 소비율 계산
        fuel_consumption_rate = self._calculate_fuel_consumption(data_list)
        
        analysis = {
            'total_samples': len(data_list),
            'avg_altitude': round(avg_altitude, 2),
            'avg_speed': round(avg_speed, 2),
            'avg_fuel_level': round(avg_fuel, 2),
            'flight_phase': flight_phase,
            'fuel_consumption_rate': round(fuel_consumption_rate, 2),
            'anomaly_count': len(self.anomalies)
        }
        
        logger.info(f"Flight pattern analysis: {analysis}")
        return analysis
    
    def _determine_flight_phase(self, altitude: float, speed: float) -> str:
        """
        비행 단계 판단
        
        Args:
            altitude: 평균 고도
            speed: 평균 속도
            
        Returns:
            비행 단계
        """
        if altitude < 500:
            return "APPROACH/LANDING"
        elif altitude < 1000:
            return "TAXI/TAKEOFF"
        elif altitude < 3000 and speed < 400:
            return "DESCENT"
        elif altitude < 3000:
            return "CLIMB"
        elif altitude < 10000 and speed > 500:
            return "CRUISE"
        else:
            return "UNKNOWN"
    
    def _calculate_fuel_consumption(self, data_list: List[Dict]) -> float:
        """
        연료 소비율 계산
        
        Args:
            data_list: 데이터 리스트
            
        Returns:
            연료 소비율 (%/hour)
        """
        if len(data_list) < 2:
            return 0.0
        
        # 시간 경과 계산
        first = datetime.fromisoformat(data_list[0]['timestamp'].replace('Z', '+00:00'))
        last = datetime.fromisoformat(data_list[-1]['timestamp'].replace('Z', '+00:00'))
        time_diff = (last - first).total_seconds() / 3600.0  # hours
        
        if time_diff == 0:
            return 0.0
        
        # 연료 소비량
        fuel_diff = data_list[0]['fuel_level'] - data_list[-1]['fuel_level']
        
        # 시간당 소비율
        consumption_rate = fuel_diff / time_diff if time_diff > 0 else 0.0
        
        return consumption_rate
    
    def calculate_distance(self, start: Dict, end: Dict) -> float:
        """
        두 지점 간 거리 계산 (Haversine formula)
        
        Args:
            start: 시작 지점 데이터
            end: 종료 지점 데이터
            
        Returns:
            거리 (km)
        """
        import math
        
        lat1 = math.radians(start['latitude'])
        lon1 = math.radians(start['longitude'])
        lat2 = math.radians(end['latitude'])
        lon2 = math.radians(end['longitude'])
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        # Haversine formula
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        # 지구 반경 (km)
        r = 6371
        
        return c * r
    
    def generate_risk_assessment(self, data_list: List[Dict]) -> Dict:
        """
        위험도 평가
        
        Args:
            data_list: 분석할 데이터 리스트
            
        Returns:
            위험도 평가 결과
        """
        risk_score = 0
        risk_factors = []
        
        # 이상치 개수에 따른 위험도
        if len(self.anomalies) > 0:
            risk_score += len(self.anomalies) * 10
            risk_factors.append(f"{len(self.anomalies)} anomalies detected")
        
        # 평균 연료량에 따른 위험도
        avg_fuel = sum(d['fuel_level'] for d in data_list) / len(data_list) if data_list else 100
        if avg_fuel < 30:
            risk_score += 30
            risk_factors.append("Low average fuel level")
        
        # 평균 엔진 온도에 따른 위험도
        avg_temp = sum(d['engine_temp'] for d in data_list) / len(data_list) if data_list else 0
        if avg_temp > 650:
            risk_score += 20
            risk_factors.append("High average engine temperature")
        
        # 위험도 등급 결정
        if risk_score < 20:
            risk_level = "LOW"
        elif risk_score < 50:
            risk_level = "MEDIUM"
        else:
            risk_level = "HIGH"
        
        assessment = {
            'risk_score': risk_score,
            'risk_level': risk_level,
            'risk_factors': risk_factors
        }
        
        logger.info(f"Risk assessment: {assessment}")
        return assessment
    
    def get_all_anomalies(self) -> List[Dict]:
        """모든 탐지된 이상 패턴 반환"""
        return self.anomalies.copy()


def main():
    """메인 함수"""
    # 테스트 데이터
    test_data = [
        {
            "timestamp": "2026-01-19T10:00:00",
            "aircraft_id": "AIRCRAFT-001",
            "altitude": 5000.0,
            "speed": 650.0,
            "heading": 180.0,
            "latitude": 37.5,
            "longitude": 127.0,
            "fuel_level": 15.0,  # 임계값 이하
            "engine_temp": 450.0
        }
    ]
    
    analyzer = FlightAnalyzer()
    
    # 이상 탐지
    for data in test_data:
        anomalies = analyzer.detect_anomalies(data)
        print(f"Detected anomalies: {anomalies}")
    
    # 패턴 분석
    pattern = analyzer.analyze_flight_pattern(test_data)
    print(f"Flight pattern: {pattern}")
    
    # 위험도 평가
    risk = analyzer.generate_risk_assessment(test_data)
    print(f"Risk assessment: {risk}")


if __name__ == "__main__":
    main()
