# 빠른 시작 가이드 (Quick Start Guide)

이 가이드는 프로젝트를 빠르게 시작하는 방법을 안내합니다.

## 사전 요구사항

### 필수 소프트웨어
- Python 3.9 이상
- pip (Python 패키지 관리자)
- Git

### 선택 사항
- Docker (컨테이너 배포 시)
- Visual Studio Code (권장 IDE)

## 5분 안에 시작하기

### 1단계: 프로젝트 클론 (30초)

```bash
# 저장소 클론
git clone https://github.com/your-org/flight-data-analyzer.git
cd flight-data-analyzer/sample
```

### 2단계: 가상 환경 설정 (1분)

```bash
# 가상 환경 생성
python -m venv venv

# 가상 환경 활성화
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate
```

### 3단계: 의존성 설치 (2분)

```bash
# 필수 패키지 설치
pip install -r requirements.txt
```

### 4단계: 애플리케이션 실행 (30초)

#### 옵션 A: 데이터 수집 실행
```bash
python -m src.data_collector
```

**출력 예시:**
```
Sample 1: Altitude=5432.12m, Speed=650.79km/h
Sample 2: Altitude=5234.56m, Speed=655.32km/h
...
Total collected samples: 10
```

#### 옵션 B: API 서버 실행
```bash
python -m src.api_server
```

**브라우저에서 확인:**
```
http://localhost:5000
```

### 5단계: API 테스트 (1분)

새 터미널을 열고:

```bash
# 헬스 체크
curl http://localhost:5000/health

# 데이터 수집
curl -X POST http://localhost:5000/api/collect \
  -H "Content-Type: application/json" \
  -d '{"samples": 5}'

# 데이터 조회
curl http://localhost:5000/api/data?limit=5

# 데이터 분석
curl -X POST http://localhost:5000/api/analyze

# 보고서 생성
curl http://localhost:5000/api/report?format=json
```

## 테스트 실행

```bash
# 전체 테스트 실행
pytest tests/ -v

# 커버리지 포함 테스트
pytest tests/ --cov=src --cov-report=html

# 특정 모듈 테스트
pytest tests/test_data_collector.py -v
```

**테스트 결과 확인:**
- 터미널에서 즉시 확인
- HTML 커버리지 리포트: `htmlcov/index.html`

## 코드 품질 검사

```bash
# 코드 포맷팅 확인
black --check src/ tests/

# 코드 자동 포맷팅
black src/ tests/

# Linting
flake8 src/ tests/ --max-line-length=120

# 타입 체킹
mypy src/ --ignore-missing-imports

# 보안 스캔
bandit -r src/
```

## Docker로 실행 (선택사항)

### 1. Docker 이미지 빌드
```bash
docker build -t flight-analyzer:latest .
```

### 2. 컨테이너 실행
```bash
docker run -d \
  -p 5000:5000 \
  --name flight-analyzer \
  flight-analyzer:latest
```

### 3. 로그 확인
```bash
docker logs -f flight-analyzer
```

### 4. 컨테이너 중지
```bash
docker stop flight-analyzer
docker rm flight-analyzer
```

## 일반적인 작업

### 새로운 데이터 수집 및 분석

```python
# Python 스크립트 예시
from src.data_collector import FlightDataCollector
from src.data_processor import DataProcessor
from src.analyzer import FlightAnalyzer
from src.report_generator import ReportGenerator

# 1. 데이터 수집
collector = FlightDataCollector("AIRCRAFT-001")
for _ in range(100):
    collector.collect_sensor_data()

# 2. 데이터 처리
processor = DataProcessor()
data = collector.get_buffer_data()
processed = processor.process_batch(data)

# 3. 데이터 분석
analyzer = FlightAnalyzer()
for item in processed:
    analyzer.detect_anomalies(item)

pattern = analyzer.analyze_flight_pattern(processed)
risk = analyzer.generate_risk_assessment(processed)
anomalies = analyzer.get_all_anomalies()

# 4. 보고서 생성
generator = ReportGenerator("AIRCRAFT-001")
generator.generate_html_report(pattern, risk, anomalies)
generator.generate_json_report(pattern, risk, anomalies)

print("Analysis complete! Check flight_report.html")
```

### API 클라이언트 예시

```python
import requests

base_url = "http://localhost:5000"

# 1. 데이터 수집
response = requests.post(f"{base_url}/api/collect", json={"samples": 50})
print(f"Collected: {response.json()['collected']} samples")

# 2. 데이터 분석
response = requests.post(f"{base_url}/api/analyze")
analysis = response.json()['analysis']
print(f"Risk Level: {analysis['risk_assessment']['risk_level']}")

# 3. 보고서 생성
response = requests.get(f"{base_url}/api/report?format=html")
print(f"Report: {response.json()['file']}")
```

## 문제 해결

### 포트가 이미 사용 중인 경우
```bash
# 포트 사용 확인
lsof -i :5000

# 프로세스 종료
kill -9 <PID>

# 또는 다른 포트 사용
python -m src.api_server --port 8080
```

### 의존성 오류
```bash
# 의존성 재설치
pip install --upgrade -r requirements.txt

# 또는 특정 패키지 재설치
pip install --upgrade flask
```

### 가상 환경 오류
```bash
# 가상 환경 삭제 후 재생성
rm -rf venv
python -m venv venv
source venv/bin/activate  # 또는 venv\Scripts\activate
pip install -r requirements.txt
```

## 다음 단계

### 프로젝트 이해하기
1. 📖 [README.md](../README.md) - 프로젝트 개요
2. 📐 [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - 프로젝트 구조
3. 📚 [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - API 문서

### CI/CD 설정하기
1. 🤖 [AI_AUTOMATION_GUIDE.md](AI_AUTOMATION_GUIDE.md) - AI 자동화
2. 🚀 [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - 배포 가이드

### 기여하기
1. 🤝 [CONTRIBUTING.md](../CONTRIBUTING.md) - 기여 가이드
2. 📝 [CHANGELOG.md](../CHANGELOG.md) - 변경 이력

## 유용한 명령어 모음

```bash
# 개발 환경 설정
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 테스트
pytest tests/ -v
pytest tests/ --cov=src --cov-report=html

# 코드 품질
black src/ tests/
flake8 src/ tests/ --max-line-length=120
pylint src/
mypy src/ --ignore-missing-imports

# 보안
bandit -r src/
safety check

# 실행
python -m src.data_collector
python -m src.api_server

# Docker
docker build -t flight-analyzer:latest .
docker run -d -p 5000:5000 --name flight-analyzer flight-analyzer:latest
docker logs -f flight-analyzer
docker stop flight-analyzer && docker rm flight-analyzer

# Git
git add .
git commit -m "Add: feature description"
git push origin feature-branch
```

## 지원

문제가 발생하거나 질문이 있으시면:

1. 📋 [GitHub Issues](https://github.com/your-org/flight-data-analyzer/issues)
2. 💬 [GitHub Discussions](https://github.com/your-org/flight-data-analyzer/discussions)
3. 📧 이메일: team@example.com

---

**축하합니다! 🎉**

프로젝트를 성공적으로 설정하고 실행했습니다. 이제 코드를 탐색하고 원하는 대로 수정할 수 있습니다.
