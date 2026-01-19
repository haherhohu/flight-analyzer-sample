# 배포 가이드

## 개요

이 문서는 비행 데이터 분석 시스템의 배포 절차를 설명합니다.

## 배포 환경

### 1. 스테이징 환경

- **용도**: 테스트 및 검증
- **브랜치**: develop
- **URL**: https://staging.example.com
- **자동 배포**: develop 브랜치에 푸시 시

### 2. 프로덕션 환경

- **용도**: 실제 운영
- **브랜치**: main
- **URL**: https://production.example.com
- **자동 배포**: main 브랜치에 푸시 시

## 배포 전 체크리스트

### 코드 품질

- [ ] 모든 테스트 통과
- [ ] 코드 커버리지 80% 이상
- [ ] Linting 통과 (Pylint, Flake8)
- [ ] 타입 체킹 통과 (MyPy)

### 보안

- [ ] 보안 스캔 통과
- [ ] 의존성 취약점 없음
- [ ] 비밀키 누출 없음
- [ ] 코드 리뷰 완료

### 문서

- [ ] README 업데이트
- [ ] CHANGELOG 업데이트
- [ ] API 문서 업데이트

## 로컬 배포

### 1. 환경 설정

```bash
# 가상 환경 생성
python -m venv venv

# 가상 환경 활성화
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt
```

### 2. 환경 변수 설정

`.env` 파일 생성:

```bash
# Application
APP_ENV=development
DEBUG=True
LOG_LEVEL=INFO

# API Server
API_HOST=0.0.0.0
API_PORT=5000

# Database (if applicable)
DATABASE_URL=sqlite:///flight_data.db

# External APIs
OPENAI_API_KEY=your_api_key_here
```

### 3. 애플리케이션 실행

```bash
# API 서버 실행
python -m src.api_server

# 데이터 수집 실행
python -m src.data_collector
```

## Docker 배포

### 1. Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY src/ ./src/

# 포트 노출
EXPOSE 5000

# 헬스 체크
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:5000/health')"

# 애플리케이션 실행
CMD ["python", "-m", "src.api_server"]
```

### 2. Docker Compose

`docker-compose.yml`:

```yaml
version: "3.8"

services:
  api:
    build: .
    ports:
      - "5000:5000"
    environment:
      - APP_ENV=production
      - DEBUG=False
    volumes:
      - ./data:/app/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

### 3. 빌드 및 실행

```bash
# 이미지 빌드
docker build -t flight-data-analyzer:latest .

# 컨테이너 실행
docker run -d \
  -p 5000:5000 \
  --name flight-analyzer \
  flight-data-analyzer:latest

# Docker Compose 사용
docker-compose up -d
```

## 클라우드 배포

### AWS 배포

#### 1. EC2 배포

```bash
# EC2 인스턴스 접속
ssh -i your-key.pem ubuntu@your-instance-ip

# 프로젝트 클론
git clone https://github.com/your-org/flight-data-analyzer.git
cd flight-data-analyzer

# 설치 및 실행
./deploy/setup.sh
./deploy/start.sh
```

#### 2. ECS (Elastic Container Service) 배포

```bash
# ECR에 이미지 푸시
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin your-account-id.dkr.ecr.us-east-1.amazonaws.com

docker tag flight-data-analyzer:latest \
  your-account-id.dkr.ecr.us-east-1.amazonaws.com/flight-data-analyzer:latest

docker push your-account-id.dkr.ecr.us-east-1.amazonaws.com/flight-data-analyzer:latest

# ECS 서비스 업데이트
aws ecs update-service \
  --cluster your-cluster \
  --service flight-analyzer \
  --force-new-deployment
```

### Azure 배포

#### Azure App Service

```bash
# Azure CLI 로그인
az login

# 리소스 그룹 생성
az group create --name flight-analyzer-rg --location eastus

# App Service 플랜 생성
az appservice plan create \
  --name flight-analyzer-plan \
  --resource-group flight-analyzer-rg \
  --sku B1 \
  --is-linux

# Web App 생성
az webapp create \
  --resource-group flight-analyzer-rg \
  --plan flight-analyzer-plan \
  --name flight-analyzer-app \
  --runtime "PYTHON|3.9"

# 코드 배포
az webapp deployment source config-zip \
  --resource-group flight-analyzer-rg \
  --name flight-analyzer-app \
  --src deployment.zip
```

### Google Cloud Platform 배포

#### Cloud Run 배포

```bash
# gcloud 인증
gcloud auth login

# 프로젝트 설정
gcloud config set project your-project-id

# 이미지 빌드 및 푸시
gcloud builds submit --tag gcr.io/your-project-id/flight-analyzer

# Cloud Run 배포
gcloud run deploy flight-analyzer \
  --image gcr.io/your-project-id/flight-analyzer \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

## Kubernetes 배포

### 1. Deployment 설정

`k8s/deployment.yml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flight-analyzer
  labels:
    app: flight-analyzer
spec:
  replicas: 3
  selector:
    matchLabels:
      app: flight-analyzer
  template:
    metadata:
      labels:
        app: flight-analyzer
    spec:
      containers:
        - name: flight-analyzer
          image: your-registry/flight-analyzer:latest
          ports:
            - containerPort: 5000
          env:
            - name: APP_ENV
              value: "production"
            - name: DEBUG
              value: "False"
          resources:
            requests:
              memory: "128Mi"
              cpu: "100m"
            limits:
              memory: "512Mi"
              cpu: "500m"
          livenessProbe:
            httpGet:
              path: /health
              port: 5000
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /health
              port: 5000
            initialDelaySeconds: 5
            periodSeconds: 5
```

### 2. Service 설정

`k8s/service.yml`:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: flight-analyzer-service
spec:
  type: LoadBalancer
  selector:
    app: flight-analyzer
  ports:
    - protocol: TCP
      port: 80
      targetPort: 5000
```

### 3. 배포 실행

```bash
# 배포
kubectl apply -f k8s/deployment.yml
kubectl apply -f k8s/service.yml

# 상태 확인
kubectl get deployments
kubectl get pods
kubectl get services

# 로그 확인
kubectl logs -f deployment/flight-analyzer
```

## CI/CD를 통한 자동 배포

### GitHub Actions 설정

워크플로우는 이미 `.github/workflows/ci-cd.yml`에 구성되어 있습니다.

#### 배포 트리거

- **Staging**: `develop` 브랜치에 푸시
- **Production**: `main` 브랜치에 푸시

#### 배포 프로세스

1. 코드 체크아웃
2. 테스트 실행
3. 보안 스캔
4. 이미지 빌드
5. 레지스트리에 푸시
6. 배포 환경에 배포
7. 헬스 체크

## 모니터링 및 로깅

### 헬스 체크

```bash
# API 헬스 체크
curl http://your-domain/health

# 응답 예시
{
  "status": "healthy",
  "timestamp": "2026-01-19T10:00:00Z"
}
```

### 로그 수집

```bash
# Docker 로그
docker logs -f flight-analyzer

# Kubernetes 로그
kubectl logs -f deployment/flight-analyzer

# 로그 파일
tail -f /var/log/flight-analyzer/app.log
```

### 메트릭 수집

- **Prometheus**: 메트릭 수집
- **Grafana**: 시각화
- **ELK Stack**: 로그 분석

## 롤백 절차

### Docker 롤백

```bash
# 이전 버전으로 롤백
docker stop flight-analyzer
docker rm flight-analyzer
docker run -d \
  -p 5000:5000 \
  --name flight-analyzer \
  flight-data-analyzer:previous-tag
```

### Kubernetes 롤백

```bash
# 이전 버전으로 롤백
kubectl rollout undo deployment/flight-analyzer

# 특정 리비전으로 롤백
kubectl rollout undo deployment/flight-analyzer --to-revision=2

# 롤백 상태 확인
kubectl rollout status deployment/flight-analyzer
```

### GitHub Actions 롤백

1. 이전 릴리즈 태그로 체크아웃
2. 수동으로 워크플로우 실행
3. 배포 확인

## 보안 고려사항

### 1. 비밀키 관리

- AWS Secrets Manager
- Azure Key Vault
- Google Secret Manager
- Kubernetes Secrets

### 2. 네트워크 보안

- HTTPS/TLS 사용
- 방화벽 규칙 설정
- VPC/서브넷 구성
- 보안 그룹 설정

### 3. 접근 제어

- IAM 역할 및 정책
- RBAC (Role-Based Access Control)
- 최소 권한 원칙
- MFA (Multi-Factor Authentication)

## 문제 해결

### 일반적인 문제

#### 1. 포트 충돌

```bash
# 포트 사용 확인
lsof -i :5000

# 프로세스 종료
kill -9 <PID>
```

#### 2. 의존성 오류

```bash
# 의존성 재설치
pip install --upgrade -r requirements.txt
```

#### 3. 환경 변수 누락

```bash
# .env 파일 확인
cat .env

# 환경 변수 설정 확인
env | grep APP_
```

## 성능 최적화

### 1. 애플리케이션 레벨

- 캐싱 구현
- 데이터베이스 쿼리 최적화
- 비동기 처리

### 2. 인프라 레벨

- 로드 밸런싱
- 오토 스케일링
- CDN 사용

### 3. 모니터링

- APM (Application Performance Monitoring)
- 리소스 사용률 모니터링
- 응답 시간 추적

## 참고 자료

- [Docker 공식 문서](https://docs.docker.com/)
- [Kubernetes 공식 문서](https://kubernetes.io/docs/)
- [AWS 배포 가이드](https://aws.amazon.com/getting-started/)
- [Azure 배포 가이드](https://docs.microsoft.com/azure/)
- [GCP 배포 가이드](https://cloud.google.com/docs)
