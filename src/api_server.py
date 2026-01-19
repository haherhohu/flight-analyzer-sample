"""
API 서버 모듈
API Server Module

RESTful API를 통해 데이터에 접근할 수 있는 서버를 제공합니다.
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
import json
from datetime import datetime

from data_collector import FlightDataCollector
from data_processor import DataProcessor
from analyzer import FlightAnalyzer
from report_generator import ReportGenerator


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # CORS 활성화

# 전역 객체
collector = FlightDataCollector("API-AIRCRAFT-001")
processor = DataProcessor()
analyzer = FlightAnalyzer()
report_gen = ReportGenerator("API-AIRCRAFT-001")


@app.route('/')
def index():
    """API 정보"""
    return jsonify({
        'name': 'Flight Data Analysis API',
        'version': '1.0.0',
        'status': 'running',
        'endpoints': {
            '/': 'API 정보',
            '/health': '헬스 체크',
            '/api/collect': 'POST - 데이터 수집',
            '/api/data': 'GET - 수집된 데이터 조회',
            '/api/analyze': 'POST - 데이터 분석',
            '/api/report': 'GET - 보고서 생성'
        }
    })


@app.route('/health')
def health():
    """헬스 체크 엔드포인트"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat()
    })


@app.route('/api/collect', methods=['POST'])
def collect_data():
    """
    데이터 수집 엔드포인트
    
    Request Body (선택):
        {
            "samples": 1  // 수집할 샘플 수
        }
    """
    try:
        data = request.get_json() or {}
        samples = data.get('samples', 1)
        
        collected = []
        for _ in range(samples):
            sample = collector.collect_sensor_data()
            collected.append(sample)
        
        return jsonify({
            'success': True,
            'collected': len(collected),
            'data': collected
        })
    except Exception as e:
        logger.error(f"Error in collect_data: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/data', methods=['GET'])
def get_data():
    """
    수집된 데이터 조회 엔드포인트
    
    Query Parameters:
        limit: 반환할 최대 데이터 수 (기본값: 100)
    """
    try:
        limit = request.args.get('limit', 100, type=int)
        data = collector.get_buffer_data()
        
        # 제한 적용
        if limit > 0:
            data = data[-limit:]
        
        return jsonify({
            'success': True,
            'count': len(data),
            'data': data
        })
    except Exception as e:
        logger.error(f"Error in get_data: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/analyze', methods=['POST'])
def analyze_data():
    """
    데이터 분석 엔드포인트
    
    Request Body (선택):
        {
            "data": []  // 분석할 데이터 (없으면 버퍼의 데이터 사용)
        }
    """
    try:
        request_data = request.get_json() or {}
        data_list = request_data.get('data', collector.get_buffer_data())
        
        if not data_list:
            return jsonify({
                'success': False,
                'error': 'No data available for analysis'
            }), 400
        
        # 데이터 처리
        processed = processor.process_batch(data_list)
        
        # 이상 탐지
        for data in processed:
            analyzer.detect_anomalies(data)
        
        # 패턴 분석
        pattern = analyzer.analyze_flight_pattern(processed)
        
        # 위험도 평가
        risk = analyzer.generate_risk_assessment(processed)
        
        # 이상 패턴
        anomalies = analyzer.get_all_anomalies()
        
        return jsonify({
            'success': True,
            'analysis': {
                'pattern': pattern,
                'risk_assessment': risk,
                'anomalies': anomalies,
                'processed_count': len(processed),
                'invalid_count': len(data_list) - len(processed)
            }
        })
    except Exception as e:
        logger.error(f"Error in analyze_data: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/report', methods=['GET'])
def generate_report():
    """
    보고서 생성 엔드포인트
    
    Query Parameters:
        format: 보고서 형식 (json, html) 기본값: json
    """
    try:
        report_format = request.args.get('format', 'json')
        
        # 데이터 가져오기
        data_list = collector.get_buffer_data()
        
        if not data_list:
            return jsonify({
                'success': False,
                'error': 'No data available for report'
            }), 400
        
        # 데이터 처리 및 분석
        processed = processor.process_batch(data_list)
        
        for data in processed:
            analyzer.detect_anomalies(data)
        
        pattern = analyzer.analyze_flight_pattern(processed)
        risk = analyzer.generate_risk_assessment(processed)
        anomalies = analyzer.get_all_anomalies()
        
        # 보고서 생성
        if report_format == 'html':
            file_path = report_gen.generate_html_report(pattern, risk, anomalies)
            return jsonify({
                'success': True,
                'format': 'html',
                'file': file_path,
                'message': 'HTML report generated successfully'
            })
        else:
            file_path = report_gen.generate_json_report(pattern, risk, anomalies)
            
            # JSON 파일 내용 읽기
            with open(file_path, 'r', encoding='utf-8') as f:
                report_data = json.load(f)
            
            return jsonify({
                'success': True,
                'format': 'json',
                'report': report_data
            })
        
    except Exception as e:
        logger.error(f"Error in generate_report: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/clear', methods=['POST'])
def clear_data():
    """데이터 버퍼 초기화 엔드포인트"""
    try:
        collector.clear_buffer()
        return jsonify({
            'success': True,
            'message': 'Data buffer cleared'
        })
    except Exception as e:
        logger.error(f"Error in clear_data: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.errorhandler(404)
def not_found(error):
    """404 에러 핸들러"""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """500 에러 핸들러"""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500


def main():
    """메인 함수"""
    port = 5000
    logger.info(f"Starting Flight Data Analysis API on port {port}")
    app.run(host='0.0.0.0', port=port, debug=True)


if __name__ == "__main__":
    main()
