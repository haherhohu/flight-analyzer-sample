# Contributing to Flight Data Analyzer

감사합니다! 이 프로젝트에 기여하고자 하시는 것에 대해 감사드립니다.

## 기여 방법

### 이슈 제출

- 버그를 발견하셨나요? [GitHub Issues](https://github.com/your-org/flight-data-analyzer/issues)에 버그 리포트를 작성해주세요.
- 새로운 기능을 제안하고 싶으신가요? Feature Request 이슈를 생성해주세요.
- 질문이 있으신가요? Discussion을 시작해주세요.

### Pull Request 제출

1. **Fork the repository**

   ```bash
   # GitHub에서 Fork 버튼 클릭
   ```

2. **Clone your fork**

   ```bash
   git clone https://github.com/your-username/flight-data-analyzer.git
   cd flight-data-analyzer
   ```

3. **Create a branch**

   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

4. **Make your changes**
   - 코드 작성
   - 테스트 추가
   - 문서 업데이트

5. **Run tests**

   ```bash
   pytest tests/ -v
   ```

6. **Check code quality**

   ```bash
   # Format code
   black src/ tests/

   # Lint
   flake8 src/ tests/
   pylint src/

   # Type checking
   mypy src/

   # Security scan
   bandit -r src/
   ```

7. **Commit your changes**

   ```bash
   git add .
   git commit -m "Add: your feature description"
   ```

   커밋 메시지 형식:
   - `Add: 새로운 기능 추가`
   - `Fix: 버그 수정`
   - `Update: 기존 기능 개선`
   - `Docs: 문서 수정`
   - `Test: 테스트 추가/수정`
   - `Refactor: 코드 리팩토링`

8. **Push to your fork**

   ```bash
   git push origin feature/your-feature-name
   ```

9. **Create a Pull Request**
   - GitHub에서 Pull Request 생성
   - 변경 사항에 대한 명확한 설명 작성
   - 관련 이슈 번호 참조 (예: `Closes #123`)

## 코딩 가이드라인

### Python 코드 스타일

- [PEP 8](https://www.python.org/dev/peps/pep-0008/) 준수
- Line length: 120 characters
- Black 포매터 사용

### 네이밍 규칙

- 변수/함수: `snake_case`
- 클래스: `PascalCase`
- 상수: `UPPER_SNAKE_CASE`

### 문서화

- 모든 public 함수에 docstring 작성
- Docstring 형식:
  ```python
  def function_name(param1: str, param2: int) -> bool:
      """
      함수의 간단한 설명

      Args:
          param1: 파라미터 1 설명
          param2: 파라미터 2 설명

      Returns:
          반환값 설명

      Raises:
          ValueError: 발생 가능한 예외 설명
      """
  ```

### 테스트

- 모든 새로운 기능에는 테스트 추가
- 테스트 커버리지 80% 이상 유지
- pytest 사용
- 테스트 파일명: `test_*.py`

### 보안

- 비밀키를 코드에 하드코딩하지 않기
- 환경 변수 사용
- 입력 검증 필수
- SQL Injection, XSS 방지

## Pull Request 체크리스트

PR을 제출하기 전에 다음 항목을 확인해주세요:

- [ ] 코드가 프로젝트의 코딩 스타일을 따릅니다
- [ ] 모든 테스트가 통과합니다
- [ ] 새로운 기능에 대한 테스트를 추가했습니다
- [ ] 문서를 업데이트했습니다 (해당되는 경우)
- [ ] CHANGELOG.md를 업데이트했습니다
- [ ] 커밋 메시지가 명확합니다
- [ ] 보안 취약점을 확인했습니다

## 코드 리뷰 프로세스

1. 자동화된 CI/CD 파이프라인이 실행됩니다
   - 코드 품질 검사
   - 보안 스캔
   - 테스트 실행
   - AI 코드 리뷰

2. 프로젝트 관리자가 코드를 검토합니다

3. 피드백이 제공되면 수정 후 재제출

4. 승인되면 main 브랜치에 병합됩니다

## 질문이나 도움이 필요하신가요?

- GitHub Discussions에서 질문하기
- Issues에서 도움 요청하기
- 이메일로 문의: team@example.com

## 행동 강령

이 프로젝트에 참여하는 모든 분들은 다음을 준수해야 합니다:

- 존중과 배려
- 건설적인 피드백
- 다양성 존중
- 협력적인 태도

## 라이선스

기여하신 코드는 프로젝트의 라이선스(Public Domain)에 따라 배포됩니다.

---

감사합니다! 🎉
