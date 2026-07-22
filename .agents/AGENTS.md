# 🤖 Antigravity Workspace Global Rules

이 파일은 Antigravity IDE가 시작할 때 가장 먼저 읽어 컨텍스트 윈도우(System Prompt)에 상시 주입하는 전역 규칙 문서입니다.

## 📌 전역 개발 수칙
1. **언어 정책**: 모든 대화 답변, 주석, 문서화는 정중한 한글로 작성합니다.
2. **코드 스타일**: Python 코드는 PEP 8 표준(snake_case 변수/함수명, PascalCase 클래스명)을 엄격히 준수합니다.
3. **안전한 예외 처리**: 포괄적인 `except Exception:` 캐칭을 피하고 구체적인 예외 클래스를 사용합니다.
4. **자동화 검증**: 코드 수정 후에는 관련 검사 스크립트나 테스터를 실행하여 동작을 검증합니다.
