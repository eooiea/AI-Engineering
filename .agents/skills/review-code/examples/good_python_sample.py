"""모범 코드 예시 (Good Code Example)

이 파일은 review-code 스킬이 지향하는 모범적인 파이썬 코드 구조 예시입니다.
- 모듈 최상단 docstring 포함
- 함수 및 클래스 명확한 Naming (snake_case / PascalCase)
- 구체적인 예외 처리 (Specific Exception Handling)
- 타입 힌팅 (Type Hinting) 적용
"""
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class UserDataProcessor:
    """사용자 데이터 전처리 및 검증을 담당하는 클래스."""

    def __init__(self, api_endpoint: str):
        self.api_endpoint = api_endpoint

    def parse_user_age(self, age_str: str) -> Optional[int]:
        """문자열 형태의 나이 데이터를 정수형으로 변환합니다.

        :param age_str: 나이 문자열
        :return: 정수로 변환된 나이 또는 None
        """
        try:
            age = int(age_str)
            if age < 0:
                raise ValueError("나이는 0보다 작을 수 없습니다.")
            return age
        except ValueError as exc:
            logger.warning(f"나이 파싱 오류 발생: {exc}")
            return None
