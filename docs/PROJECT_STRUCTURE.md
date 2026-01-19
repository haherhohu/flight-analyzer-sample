# 프로젝트 구조

```
sample/
│
├── .github/
│   └── workflows/
│       ├── ci-cd.yml              # 메인 CI/CD 파이프라인
│       ├── ai-code-review.yml     # AI 코드 리뷰 워크플로우
│       └── security-scan.yml      # 보안 스캔 워크플로우
│
├── src/                           # 소스 코드
│   ├── __init__.py
│   ├── data_collector.py          # 데이터 수집 모듈
│   ├── data_processor.py          # 데이터 처리 모듈
│   ├── analyzer.py                # 데이터 분석 모듈
│   ├── report_generator.py        # 보고서 생성 모듈
│   └── api_server.py              # API 서버
│
├── tests/                         # 테스트 코드
│   ├── __init__.py
│   ├── test_data_collector.py
│   ├── test_data_processor.py
│   ├── test_analyzer.py
│   └── test_report_generator.py
│
├── docs/                          # 문서
│   ├── AI_AUTOMATION_GUIDE.md     # AI 자동화 가이드
│   ├── API_DOCUMENTATION.md       # API 문서
│   └── DEPLOYMENT_GUIDE.md        # 배포 가이드
│
├── .gitignore                     # Git 무시 파일
├── requirements.txt               # Python 의존성
├── pyproject.toml                 # 프로젝트 설정
├── README.md                      # 프로젝트 소개
├── CHANGELOG.md                   # 변경 이력
└── CONTRIBUTING.md                # 기여 가이드
```

## 모듈 설명

### 데이터 수집 (data_collector.py)

- 센서 데이터 수집
- 데이터 버퍼 관리
- 파일 저장 기능

### 데이터 처리 (data_processor.py)

- 데이터 유효성 검증
- 데이터 정규화
- 이상치 필터링
- 통계 계산

### 데이터 분석 (analyzer.py)

- 이상 패턴 탐지
- 비행 패턴 분석
- 위험도 평가
- 거리 계산

### 보고서 생성 (report_generator.py)

- HTML 보고서 생성
- JSON 보고서 생성
- 요약 텍스트 생성

### API 서버 (api_server.py)

- RESTful API 엔드포인트
- CORS 지원
- 에러 핸들링

## CI/CD 파이프라인 구조

```
┌─────────────────────────────────────────────────────────────────┐
│                         GitHub Actions                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              CI/CD Pipeline (ci-cd.yml)                   │  │
│  ├──────────────────────────────────────────────────────────┤  │
│  │                                                            │  │
│  │  1. Code Quality Check                                    │  │
│  │     └─ Black, Flake8, Pylint, MyPy                       │  │
│  │                                                            │  │
│  │  2. Security Scan                                         │  │
│  │     └─ Bandit, Safety                                     │  │
│  │                                                            │  │
│  │  3. Unit Tests                                            │  │
│  │     └─ Pytest + Coverage                                  │  │
│  │                                                            │  │
│  │  4. AI Code Review (PR only)                             │  │
│  │     └─ Automated AI analysis                              │  │
│  │                                                            │  │
│  │  5. Build                                                  │  │
│  │     └─ Package creation                                   │  │
│  │                                                            │  │
│  │  6. Integration Tests                                     │  │
│  │                                                            │  │
│  │  7. Deploy                                                 │  │
│  │     ├─ Staging (develop branch)                          │  │
│  │     └─ Production (main branch)                          │  │
│  │                                                            │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │        AI Code Review (ai-code-review.yml)                │  │
│  ├──────────────────────────────────────────────────────────┤  │
│  │                                                            │  │
│  │  • Complexity analysis (Radon)                            │  │
│  │  • Code quality check (Pylint)                            │  │
│  │  • Security scan (Bandit)                                 │  │
│  │  • AI-based suggestions                                   │  │
│  │  • PR comment with recommendations                        │  │
│  │                                                            │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │        Security Scan (security-scan.yml)                  │  │
│  ├──────────────────────────────────────────────────────────┤  │
│  │                                                            │  │
│  │  • Dependency scan (Safety)                               │  │
│  │  • SAST (Bandit)                                          │  │
│  │  • Secret detection (TruffleHog)                          │  │
│  │  • Code scanning (CodeQL)                                 │  │
│  │  • Security summary generation                            │  │
│  │                                                            │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

## 데이터 플로우

```
┌─────────────┐
│   Sensors   │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│ Data Collector  │
│  (수집)          │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ Data Processor  │
│  (검증/정규화)   │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│   Analyzer      │
│  (분석/탐지)     │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ Report Generator│
│  (보고서 생성)   │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│  HTML/JSON      │
│   Reports       │
└─────────────────┘
```

## API 엔드포인트

```
API Server (Port 5000)
│
├── GET  /                # API 정보
├── GET  /health          # 헬스 체크
│
├── POST /api/collect     # 데이터 수집
├── GET  /api/data        # 데이터 조회
├── POST /api/analyze     # 데이터 분석
├── GET  /api/report      # 보고서 생성
└── POST /api/clear       # 버퍼 초기화
```

## 테스트 구조

```
tests/
│
├── test_data_collector.py
│   ├── TestFlightDataCollector
│   │   ├── test_initialization
│   │   ├── test_collect_sensor_data
│   │   ├── test_altitude_range
│   │   ├── test_speed_range
│   │   └── ...
│
├── test_data_processor.py
│   ├── TestDataProcessor
│   │   ├── test_validate_valid_data
│   │   ├── test_normalize_data
│   │   ├── test_filter_outliers
│   │   └── ...
│
├── test_analyzer.py
│   ├── TestFlightAnalyzer
│   │   ├── test_detect_anomalies
│   │   ├── test_analyze_flight_pattern
│   │   ├── test_generate_risk_assessment
│   │   └── ...
│
└── test_report_generator.py
    ├── TestReportGenerator
    │   ├── test_generate_html_report
    │   ├── test_generate_json_report
    │   └── ...
```

## 보안 계층

```
┌─────────────────────────────────────────────────────────┐
│                    Security Layers                       │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  Layer 1: Code Security                                  │
│  ├─ Static Analysis (Bandit)                            │
│  ├─ Secret Detection (TruffleHog)                       │
│  └─ Code Quality (CodeQL)                               │
│                                                           │
│  Layer 2: Dependency Security                            │
│  ├─ Vulnerability Scan (Safety)                         │
│  └─ Automated Updates (Dependabot)                      │
│                                                           │
│  Layer 3: Runtime Security                               │
│  ├─ Input Validation                                     │
│  ├─ Error Handling                                       │
│  └─ Environment Variables                                │
│                                                           │
│  Layer 4: Infrastructure Security                        │
│  ├─ HTTPS/TLS                                           │
│  ├─ Access Control                                       │
│  └─ Network Segmentation                                 │
│                                                           │
└─────────────────────────────────────────────────────────┘
```
