# AI 자동화 기능 가이드

## 개요

이 문서는 프로젝트에 통합된 AI 자동화 기능에 대해 설명합니다.

## 1. AI 기반 코드 리뷰

### 기능

- Pull Request 생성 시 자동으로 코드 분석
- 코드 품질, 보안, 성능 측면에서 개선점 제안
- 복잡도 분석 및 유지보수성 평가

### 사용 방법

1. Pull Request 생성
2. GitHub Actions가 자동으로 AI 코드 리뷰 워크플로우 실행
3. PR에 자동으로 리뷰 코멘트가 추가됨

### 구성 요소

- **Radon**: 코드 복잡도 및 유지보수성 지수 계산
- **Pylint**: 코드 품질 검사
- **Bandit**: 보안 취약점 검사
- **AI 분석**: 종합적인 개선 제안

### 워크플로우 파일

`.github/workflows/ai-code-review.yml`

## 2. 자동 보안 스캔

### 기능

- 의존성 취약점 검사
- 정적 애플리케이션 보안 테스팅 (SAST)
- 비밀키 누출 검사
- CodeQL을 통한 고급 보안 분석

### 스캔 유형

#### 2.1 의존성 취약점 스캔

- **도구**: Safety
- **대상**: requirements.txt의 모든 패키지
- **실행**: Push, PR, 매일 자동 실행
- **결과**: 알려진 보안 취약점이 있는 패키지 식별

#### 2.2 정적 보안 분석

- **도구**: Bandit
- **대상**: 모든 Python 소스 코드
- **검사 항목**:
  - SQL Injection
  - 하드코딩된 비밀키
  - 안전하지 않은 함수 사용
  - 입력 검증 누락

#### 2.3 비밀키 검사

- **도구**: TruffleHog
- **대상**: 전체 저장소
- **검사 항목**:
  - API 키
  - 액세스 토큰
  - 비밀번호
  - 인증서

#### 2.4 CodeQL 분석

- **도구**: GitHub CodeQL
- **대상**: Python 코드베이스
- **검사 항목**:
  - 보안 취약점
  - 코드 품질 이슈
  - 잠재적 버그

### 워크플로우 파일

`.github/workflows/security-scan.yml`

## 3. CI/CD 파이프라인

### 파이프라인 단계

#### 3.1 코드 품질 검사

```yaml
Jobs:
  - Black: 코드 포맷팅 확인
  - Flake8: PEP 8 준수 확인
  - Pylint: 코드 품질 검사
  - MyPy: 타입 힌트 검증
```

#### 3.2 보안 스캔

```yaml
Jobs:
  - Bandit: SAST 보안 스캔
  - Safety: 의존성 취약점 검사
```

#### 3.3 테스트 실행

```yaml
Jobs:
  - Pytest: 단위 테스트 실행
  - Coverage: 코드 커버리지 측정
  - Upload: 커버리지 보고서 업로드
```

#### 3.4 AI 코드 리뷰 (PR만)

```yaml
Jobs:
  - AI Review: 자동 코드 리뷰 생성
  - Comment: PR에 리뷰 코멘트 추가
```

#### 3.5 빌드

```yaml
Jobs:
  - Build: 패키지 빌드
  - Upload: 빌드 아티팩트 업로드
```

#### 3.6 배포

```yaml
Jobs:
  - Staging: develop 브랜치 → 스테이징 환경
  - Production: main 브랜치 → 프로덕션 환경
```

## 4. 설정 방법

### 4.1 GitHub Secrets 설정

프로젝트에서 다음 Secrets을 설정해야 합니다:

```
OPENAI_API_KEY (선택)
  - AI 코드 리뷰에 OpenAI API 사용 시 필요
  - 설정 경로: Repository Settings → Secrets → Actions
```

### 4.2 워크플로우 권한 설정

```yaml
Settings → Actions → General → Workflow permissions
- Read and write permissions 활성화
- Allow GitHub Actions to create and approve pull requests 활성화
```

### 4.3 브랜치 보호 규칙 (권장)

```yaml
Settings → Branches → Branch protection rules
main 브랜치:
  - Require pull request reviews before merging
  - Require status checks to pass before merging:
    ✓ Code Quality Check
    ✓ Security Scan
    ✓ Unit Tests
```

## 5. 워크플로우 트리거

### 자동 트리거

- **Push**: main, develop 브랜치에 푸시 시
- **Pull Request**: main, develop 브랜치로 PR 생성/업데이트 시
- **Schedule**: 보안 스캔은 매일 02:00 UTC에 자동 실행

### 수동 트리거

- GitHub Actions 탭에서 "Run workflow" 버튼 클릭

## 6. 결과 확인

### 6.1 GitHub Actions 탭

1. Repository → Actions 탭
2. 실행 중인 워크플로우 확인
3. 완료된 워크플로우의 로그 및 아티팩트 다운로드

### 6.2 Pull Request

- AI 코드 리뷰 코멘트 확인
- 보안 스캔 요약 확인
- 테스트 결과 확인

### 6.3 아티팩트

각 워크플로우 실행 후 다음 아티팩트를 다운로드할 수 있습니다:

- `security-reports`: 보안 스캔 결과
- `coverage-report`: 테스트 커버리지 보고서
- `ai-review-artifacts`: AI 리뷰 상세 분석
- `dist-package`: 빌드된 패키지

## 7. AI 기능 커스터마이징

### 7.1 AI 코드 리뷰 규칙 수정

`ai-code-review.yml`에서 분석 규칙을 수정할 수 있습니다:

```yaml
- name: AI-based review suggestions
  env:
    OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
  run: |
    # 여기에 커스텀 AI 분석 로직 추가
```

### 7.2 보안 스캔 임계값 조정

`security-scan.yml`에서 보안 스캔 설정을 조정할 수 있습니다:

```yaml
- name: Run Bandit SAST scan
  run: |
    # -ll: Low severity 이상만 표시
    # -lll: Medium severity 이상만 표시
    bandit -r src/ -lll
```

## 8. 통합 가능한 추가 AI 도구

### 8.1 Snyk (의존성 보안)

```yaml
- name: Run Snyk
  uses: snyk/actions/python@master
  with:
    args: --severity-threshold=high
```

### 8.2 SonarCloud (코드 품질)

```yaml
- name: SonarCloud Scan
  uses: SonarSource/sonarcloud-github-action@master
  env:
    SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
```

### 8.3 Dependabot (자동 의존성 업데이트)

`.github/dependabot.yml` 파일 생성:

```yaml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
```

## 9. 모범 사례

### 9.1 코드 작성

- 타입 힌트 사용
- 포괄적인 docstring 작성
- 단위 테스트 작성
- 에러 처리 구현

### 9.2 보안

- 환경 변수로 민감한 정보 관리
- 정기적인 의존성 업데이트
- 코드 리뷰 필수화
- 보안 스캔 결과 즉시 대응

### 9.3 CI/CD

- 작은 단위로 자주 커밋
- PR 단위로 작업
- 모든 테스트 통과 후 병합
- 자동 배포 전 수동 승인 단계 추가

## 10. 문제 해결

### 10.1 워크플로우 실패 시

1. GitHub Actions 로그 확인
2. 실패한 단계의 에러 메시지 분석
3. 로컬에서 동일한 명령어 실행하여 재현
4. 필요시 워크플로우 수정

### 10.2 보안 경고 대응

1. 경고의 심각도 확인 (Critical, High, Medium, Low)
2. 영향받는 코드/패키지 식별
3. 수정 또는 업데이트 적용
4. 재스캔하여 해결 확인

### 10.3 성능 이슈

- 워크플로우 실행 시간이 너무 길 경우:
  - 병렬 실행 활용
  - 캐시 활용
  - 불필요한 단계 제거

## 11. 참고 자료

- [GitHub Actions 공식 문서](https://docs.github.com/en/actions)
- [Python 보안 베스트 프랙티스](https://python.readthedocs.io/en/stable/library/security_warnings.html)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Bandit 문서](https://bandit.readthedocs.io/)
- [Safety 문서](https://pyup.io/safety/)
