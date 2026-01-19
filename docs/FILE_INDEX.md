# 프로젝트 파일 목록

## 📂 전체 프로젝트 구조

```
sample/
│
├── 📄 README.md                              # 프로젝트 소개
├── 📄 PROJECT_SUMMARY.md                     # 프로젝트 완료 보고서
├── 📄 CHANGELOG.md                           # 변경 이력
├── 📄 CONTRIBUTING.md                        # 기여 가이드
├── 📄 .gitignore                             # Git 무시 파일
├── 📄 requirements.txt                       # Python 의존성
├── 📄 pyproject.toml                         # 프로젝트 설정
│
├── 📁 .github/                               # GitHub 설정
│   └── 📁 workflows/
│       ├── ci-cd.yml                         # 메인 CI/CD 파이프라인
│       ├── ai-code-review.yml                # AI 코드 리뷰
│       └── security-scan.yml                 # 보안 스캔
│
├── 📁 src/                                   # 소스 코드 (2,098 라인)
│   ├── __init__.py                           # 패키지 초기화
│   ├── data_collector.py        (158 라인)  # 데이터 수집
│   ├── data_processor.py        (190 라인)  # 데이터 처리
│   ├── analyzer.py              (267 라인)  # 데이터 분석
│   ├── report_generator.py      (297 라인)  # 보고서 생성
│   └── api_server.py            (233 라인)  # API 서버
│
├── 📁 tests/                                 # 테스트 코드
│   ├── __init__.py                           # 테스트 패키지 초기화
│   ├── test_data_collector.py   (123 라인)  # 데이터 수집 테스트
│   ├── test_data_processor.py   (240 라인)  # 데이터 처리 테스트
│   ├── test_analyzer.py         (285 라인)  # 분석 테스트
│   └── test_report_generator.py (205 라인)  # 보고서 생성 테스트
│
└── 📁 docs/                                  # 문서
    ├── QUICK_START.md                        # 빠른 시작 가이드
    ├── PROJECT_STRUCTURE.md                  # 프로젝트 구조
    ├── API_DOCUMENTATION.md                  # API 문서
    ├── AI_AUTOMATION_GUIDE.md                # AI 자동화 가이드
    └── DEPLOYMENT_GUIDE.md                   # 배포 가이드
```

---

## 📊 파일 통계

### 코드 파일

| 파일                | 라인 수   | 설명                     |
| ------------------- | --------- | ------------------------ |
| data_collector.py   | 158       | 센서 데이터 수집 및 저장 |
| data_processor.py   | 190       | 데이터 검증 및 처리      |
| analyzer.py         | 267       | 이상 탐지 및 분석        |
| report_generator.py | 297       | HTML/JSON 보고서 생성    |
| api_server.py       | 233       | RESTful API 서버         |
| **총 소스 코드**    | **1,145** | -                        |

### 테스트 파일

| 파일                     | 라인 수 | 테스트 수 |
| ------------------------ | ------- | --------- |
| test_data_collector.py   | 123     | 13        |
| test_data_processor.py   | 240     | 20        |
| test_analyzer.py         | 285     | 25        |
| test_report_generator.py | 205     | 12        |
| **총 테스트 코드**       | **853** | **70+**   |

### 문서 파일

| 파일                   | 설명                       |
| ---------------------- | -------------------------- |
| README.md              | 프로젝트 개요 및 주요 기능 |
| PROJECT_SUMMARY.md     | 완료 보고서                |
| QUICK_START.md         | 5분 시작 가이드            |
| PROJECT_STRUCTURE.md   | 프로젝트 구조 및 아키텍처  |
| API_DOCUMENTATION.md   | API 엔드포인트 상세 문서   |
| AI_AUTOMATION_GUIDE.md | AI 자동화 설정 가이드      |
| DEPLOYMENT_GUIDE.md    | 배포 방법 및 절차          |
| CONTRIBUTING.md        | 기여 가이드라인            |
| CHANGELOG.md           | 버전 변경 이력             |

### CI/CD 워크플로우

| 파일               | 설명                                 |
| ------------------ | ------------------------------------ |
| ci-cd.yml          | 메인 파이프라인 (빌드, 테스트, 배포) |
| ai-code-review.yml | AI 기반 코드 리뷰                    |
| security-scan.yml  | 보안 취약점 스캔                     |

---

## 🎯 핵심 파일 설명

### 1. 소스 코드 (src/)

#### data_collector.py

**목적**: 비행 센서 데이터 수집
**주요 기능**:

- FlightDataCollector 클래스
- 10가지 센서 데이터 수집
- 버퍼 관리
- JSON 파일 저장

**주요 메서드**:

```python
- collect_sensor_data()
- get_buffer_data()
- clear_buffer()
- save_to_file()
```

#### data_processor.py

**목적**: 수집된 데이터 검증 및 처리
**주요 기능**:

- 데이터 유효성 검증
- 값 정규화
- 이상치 필터링
- 통계 계산

**주요 메서드**:

```python
- validate_data()
- normalize_data()
- filter_outliers()
- calculate_statistics()
- process_batch()
```

#### analyzer.py

**목적**: 비행 데이터 분석 및 이상 탐지
**주요 기능**:

- 이상 패턴 탐지
- 비행 단계 판단
- 위험도 평가
- 거리 계산

**주요 메서드**:

```python
- detect_anomalies()
- analyze_flight_pattern()
- generate_risk_assessment()
- calculate_distance()
```

#### report_generator.py

**목적**: 분석 결과 보고서 생성
**주요 기능**:

- HTML 보고서 생성
- JSON 보고서 생성
- 요약 텍스트 생성

**주요 메서드**:

```python
- generate_html_report()
- generate_json_report()
- generate_summary()
```

#### api_server.py

**목적**: RESTful API 제공
**주요 기능**:

- 7개 API 엔드포인트
- CORS 지원
- 에러 핸들링

**엔드포인트**:

```
GET  /               - API 정보
GET  /health         - 헬스 체크
POST /api/collect    - 데이터 수집
GET  /api/data       - 데이터 조회
POST /api/analyze    - 데이터 분석
GET  /api/report     - 보고서 생성
POST /api/clear      - 버퍼 초기화
```

---

### 2. 테스트 코드 (tests/)

#### test_data_collector.py

- 초기화 테스트
- 데이터 수집 테스트
- 센서 범위 검증 (고도, 속도, 방향 등)
- 버퍼 관리 테스트
- 파일 저장 테스트

#### test_data_processor.py

- 유효성 검증 테스트
- 정규화 테스트
- 이상치 필터링 테스트
- 통계 계산 테스트
- 배치 처리 테스트

#### test_analyzer.py

- 이상 탐지 테스트 (연료, 온도, 고도)
- 비행 단계 판단 테스트
- 위험도 평가 테스트
- 거리 계산 테스트

#### test_report_generator.py

- HTML 보고서 생성 테스트
- JSON 보고서 생성 테스트
- 요약 생성 테스트
- 권장사항 생성 테스트

---

### 3. GitHub Actions 워크플로우

#### ci-cd.yml (메인 파이프라인)

**트리거**: Push, Pull Request
**단계**:

1. lint-and-format (코드 품질)
2. security-scan (보안 스캔)
3. unit-tests (단위 테스트)
4. ai-code-review (AI 리뷰, PR만)
5. build (빌드)
6. integration-tests (통합 테스트)
7. deploy-staging (스테이징 배포)
8. deploy-production (프로덕션 배포)

#### ai-code-review.yml (AI 코드 리뷰)

**트리거**: Pull Request
**기능**:

- 변경 파일 분석
- 복잡도 계산 (Radon)
- 코드 패턴 검사
- AI 리뷰 제안
- PR 자동 코멘트

#### security-scan.yml (보안 스캔)

**트리거**: Push, Pull Request, 일일 자동 (cron)
**기능**:

- 의존성 취약점 (Safety)
- SAST (Bandit)
- 비밀키 검출 (TruffleHog)
- CodeQL 분석
- 보안 요약 생성

---

### 4. 문서 (docs/)

#### QUICK_START.md (2,100 단어)

- 5분 시작 가이드
- 설치 방법
- 기본 사용법
- 문제 해결

#### PROJECT_STRUCTURE.md (1,800 단어)

- 프로젝트 구조
- 모듈 설명
- 데이터 플로우
- 아키텍처 다이어그램

#### API_DOCUMENTATION.md (3,200 단어)

- 전체 API 레퍼런스
- 엔드포인트 상세
- 요청/응답 예시
- 에러 코드

#### AI_AUTOMATION_GUIDE.md (2,800 단어)

- AI 기능 설명
- 설정 방법
- 커스터마이징
- 통합 가이드

#### DEPLOYMENT_GUIDE.md (3,500 단어)

- 로컬 배포
- Docker 배포
- 클라우드 배포
- Kubernetes 배포

---

## 💻 코드 품질 지표

### 테스트 커버리지

- 목표: 80%+
- 단위 테스트: 70+ 케이스
- 통합 테스트: 포함

### 코드 스타일

- PEP 8 준수
- Black 포맷팅
- Type hints 사용
- Docstring 완비

### 보안

- Bandit 스캔 통과
- Safety 체크 통과
- 비밀키 없음
- 입력 검증 구현

---

## 🚀 사용 가능한 명령어

### 개발

```bash
# 테스트 실행
pytest tests/ -v

# 커버리지 포함
pytest tests/ --cov=src --cov-report=html

# 코드 포맷팅
black src/ tests/

# Lint
flake8 src/ tests/
pylint src/

# 타입 체킹
mypy src/

# 보안 스캔
bandit -r src/
```

### 실행

```bash
# 데이터 수집
python -m src.data_collector

# API 서버
python -m src.api_server

# 특정 모듈
python -m src.analyzer
```

---

## 📦 의존성

### 필수 패키지

- Flask 3.0.0
- flask-cors 4.0.0
- numpy 1.26.2
- pandas 2.1.4
- pytest 7.4.3
- pytest-cov 4.1.0

### 개발 패키지

- pylint 3.0.3
- flake8 7.0.0
- black 23.12.1
- mypy 1.8.0
- bandit 1.7.6
- safety 3.0.1

---

## 🎓 학습 가치

이 프로젝트를 통해 학습할 수 있는 내용:

1. **Python 개발**: 모듈화, 테스팅, API 개발
2. **DevOps**: CI/CD, 자동화, 배포
3. **보안**: 취약점 스캔, 코드 분석
4. **AI 통합**: 자동 리뷰, 분석
5. **문서화**: 기술 문서 작성

---

**생성일**: 2026년 1월 19일
**총 파일 수**: 25개
**총 코드 라인**: 2,098 라인
**문서 페이지**: 60+ 페이지
