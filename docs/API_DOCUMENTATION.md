# API 문서

## 개요

Flight Data Analysis API는 비행 데이터를 수집, 처리, 분석하고 보고서를 생성하는 RESTful API를 제공합니다.

## Base URL

```
http://localhost:5000
```

## 인증

현재 버전에서는 인증이 필요하지 않습니다. 프로덕션 환경에서는 적절한 인증 메커니즘을 구현해야 합니다.

## 엔드포인트

### 1. API 정보 조회

기본 API 정보와 사용 가능한 엔드포인트 목록을 반환합니다.

**요청**

```http
GET /
```

**응답**

```json
{
  "name": "Flight Data Analysis API",
  "version": "1.0.0",
  "status": "running",
  "endpoints": {
    "/": "API 정보",
    "/health": "헬스 체크",
    "/api/collect": "POST - 데이터 수집",
    "/api/data": "GET - 수집된 데이터 조회",
    "/api/analyze": "POST - 데이터 분석",
    "/api/report": "GET - 보고서 생성"
  }
}
```

---

### 2. 헬스 체크

API 서버의 상태를 확인합니다.

**요청**

```http
GET /health
```

**응답**

```json
{
  "status": "healthy",
  "timestamp": "2026-01-19T10:00:00.000000"
}
```

---

### 3. 데이터 수집

센서로부터 비행 데이터를 수집합니다.

**요청**

```http
POST /api/collect
Content-Type: application/json

{
  "samples": 5
}
```

**파라미터**
| 이름 | 타입 | 필수 | 기본값 | 설명 |
|------|------|------|--------|------|
| samples | integer | X | 1 | 수집할 샘플 수 |

**응답**

```json
{
  "success": true,
  "collected": 5,
  "data": [
    {
      "timestamp": "2026-01-19T10:00:00.000000",
      "aircraft_id": "API-AIRCRAFT-001",
      "altitude": 5432.12,
      "speed": 650.79,
      "heading": 180.46,
      "latitude": 37.123457,
      "longitude": 127.123457,
      "fuel_level": 75.56,
      "engine_temp": 450.22
    },
    ...
  ]
}
```

---

### 4. 데이터 조회

버퍼에 저장된 수집된 데이터를 조회합니다.

**요청**

```http
GET /api/data?limit=100
```

**쿼리 파라미터**
| 이름 | 타입 | 필수 | 기본값 | 설명 |
|------|------|------|--------|------|
| limit | integer | X | 100 | 반환할 최대 데이터 수 |

**응답**

```json
{
  "success": true,
  "count": 10,
  "data": [
    {
      "timestamp": "2026-01-19T10:00:00.000000",
      "aircraft_id": "API-AIRCRAFT-001",
      "altitude": 5432.12,
      "speed": 650.79,
      "heading": 180.46,
      "latitude": 37.123457,
      "longitude": 127.123457,
      "fuel_level": 75.56,
      "engine_temp": 450.22
    },
    ...
  ]
}
```

---

### 5. 데이터 분석

수집된 데이터를 분석하여 패턴, 이상 탐지, 위험도 평가를 수행합니다.

**요청**

```http
POST /api/analyze
Content-Type: application/json

{
  "data": [...]
}
```

**파라미터**
| 이름 | 타입 | 필수 | 기본값 | 설명 |
|------|------|------|--------|------|
| data | array | X | 버퍼 데이터 | 분석할 데이터 배열 (생략 시 버퍼 데이터 사용) |

**응답**

```json
{
  "success": true,
  "analysis": {
    "pattern": {
      "total_samples": 100,
      "avg_altitude": 5000.0,
      "avg_speed": 650.0,
      "avg_fuel_level": 55.0,
      "flight_phase": "CRUISE",
      "fuel_consumption_rate": 5.2,
      "anomaly_count": 2
    },
    "risk_assessment": {
      "risk_score": 25,
      "risk_level": "MEDIUM",
      "risk_factors": ["2 anomalies detected"]
    },
    "anomalies": [
      {
        "timestamp": "2026-01-19T10:00:00.000000",
        "aircraft_id": "API-AIRCRAFT-001",
        "anomalies": ["WARNING: High engine temperature (720.00°C)"]
      }
    ],
    "processed_count": 98,
    "invalid_count": 2
  }
}
```

---

### 6. 보고서 생성

분석 결과를 바탕으로 보고서를 생성합니다.

**요청**

```http
GET /api/report?format=json
```

**쿼리 파라미터**
| 이름 | 타입 | 필수 | 기본값 | 설명 |
|------|------|------|--------|------|
| format | string | X | json | 보고서 형식 (json, html) |

**응답 (JSON 형식)**

```json
{
  "success": true,
  "format": "json",
  "report": {
    "aircraft_id": "API-AIRCRAFT-001",
    "generated_at": "2026-01-19T10:00:00.000000",
    "analysis": {
      "total_samples": 100,
      "avg_altitude": 5000.0,
      "avg_speed": 650.0,
      "avg_fuel_level": 55.0,
      "flight_phase": "CRUISE",
      "fuel_consumption_rate": 5.2,
      "anomaly_count": 2
    },
    "risk_assessment": {
      "risk_score": 25,
      "risk_level": "MEDIUM",
      "risk_factors": ["2 anomalies detected"]
    },
    "anomalies": []
  }
}
```

**응답 (HTML 형식)**

```json
{
  "success": true,
  "format": "html",
  "file": "flight_report.html",
  "message": "HTML report generated successfully"
}
```

---

### 7. 데이터 버퍼 초기화

버퍼에 저장된 모든 데이터를 삭제합니다.

**요청**

```http
POST /api/clear
```

**응답**

```json
{
  "success": true,
  "message": "Data buffer cleared"
}
```

---

## 데이터 모델

### FlightData

비행 데이터 객체

| 필드        | 타입   | 설명                       | 범위       |
| ----------- | ------ | -------------------------- | ---------- |
| timestamp   | string | ISO 8601 형식의 타임스탬프 | -          |
| aircraft_id | string | 항공기 식별자              | -          |
| altitude    | float  | 고도 (미터)                | 0 - 15000  |
| speed       | float  | 속도 (km/h)                | 0 - 1000   |
| heading     | float  | 방향 (도)                  | 0 - 360    |
| latitude    | float  | 위도                       | -90 - 90   |
| longitude   | float  | 경도                       | -180 - 180 |
| fuel_level  | float  | 연료량 (%)                 | 0 - 100    |
| engine_temp | float  | 엔진 온도 (°C)             | 0 - 1000   |

### AnalysisResult

분석 결과 객체

| 필드                  | 타입    | 설명         |
| --------------------- | ------- | ------------ |
| total_samples         | integer | 총 샘플 수   |
| avg_altitude          | float   | 평균 고도    |
| avg_speed             | float   | 평균 속도    |
| avg_fuel_level        | float   | 평균 연료량  |
| flight_phase          | string  | 비행 단계    |
| fuel_consumption_rate | float   | 연료 소비율  |
| anomaly_count         | integer | 이상 패턴 수 |

### RiskAssessment

위험도 평가 객체

| 필드         | 타입    | 설명                          |
| ------------ | ------- | ----------------------------- |
| risk_score   | integer | 위험도 점수                   |
| risk_level   | string  | 위험 등급 (LOW, MEDIUM, HIGH) |
| risk_factors | array   | 위험 요인 목록                |

---

## 에러 응답

### 일반 에러 형식

```json
{
  "success": false,
  "error": "Error message description"
}
```

### HTTP 상태 코드

| 코드 | 설명                      |
| ---- | ------------------------- |
| 200  | 성공                      |
| 400  | 잘못된 요청               |
| 404  | 엔드포인트를 찾을 수 없음 |
| 500  | 서버 내부 오류            |

---

## 사용 예제

### Python

```python
import requests

# API 베이스 URL
base_url = "http://localhost:5000"

# 데이터 수집
response = requests.post(f"{base_url}/api/collect", json={"samples": 10})
print(response.json())

# 데이터 조회
response = requests.get(f"{base_url}/api/data?limit=10")
data = response.json()
print(f"Collected {data['count']} samples")

# 데이터 분석
response = requests.post(f"{base_url}/api/analyze")
analysis = response.json()
print(f"Risk Level: {analysis['analysis']['risk_assessment']['risk_level']}")

# 보고서 생성
response = requests.get(f"{base_url}/api/report?format=json")
report = response.json()
print(report)
```

### JavaScript

```javascript
const baseUrl = "http://localhost:5000";

// 데이터 수집
fetch(`${baseUrl}/api/collect`, {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({ samples: 10 }),
})
  .then((response) => response.json())
  .then((data) => console.log(data));

// 데이터 조회
fetch(`${baseUrl}/api/data?limit=10`)
  .then((response) => response.json())
  .then((data) => console.log(`Collected ${data.count} samples`));

// 데이터 분석
fetch(`${baseUrl}/api/analyze`, {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
})
  .then((response) => response.json())
  .then((analysis) => {
    console.log(`Risk Level: ${analysis.analysis.risk_assessment.risk_level}`);
  });
```

### cURL

```bash
# 데이터 수집
curl -X POST http://localhost:5000/api/collect \
  -H "Content-Type: application/json" \
  -d '{"samples": 10}'

# 데이터 조회
curl http://localhost:5000/api/data?limit=10

# 데이터 분석
curl -X POST http://localhost:5000/api/analyze

# 보고서 생성
curl http://localhost:5000/api/report?format=json
```

---

## 레이트 리미팅

현재 버전에서는 레이트 리미팅이 구현되어 있지 않습니다. 프로덕션 환경에서는 API 남용을 방지하기 위해 레이트 리미팅을 구현해야 합니다.

**권장 설정**:

- 일반 사용자: 100 requests/minute
- 인증된 사용자: 1000 requests/minute

---

## 버전 관리

현재 API 버전: v1.0.0

향후 버전에서는 URL 기반 버전 관리를 구현할 예정입니다:

- v1: `/api/v1/...`
- v2: `/api/v2/...`

---

## 지원 및 문의

이슈나 질문이 있으시면 GitHub Issues를 통해 문의해주세요.
