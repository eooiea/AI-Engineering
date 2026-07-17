import json
import re

class AssertionTestRunner:
    """간단한 규칙 및 어설션(Assertion) 기반 평가 하네스 테스트 러너"""
    def __init__(self):
        self.tests_run = 0
        self.tests_passed = 0
        self.tests_failed = 0
        self.results = []

    def log_result(self, name: str, success: bool, message: str):
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            status = "PASS"
        else:
            self.tests_failed += 1
            status = "FAIL"
            
        print(f"[{status}] {name} - {message}")
        self.results.append({"name": name, "status": status, "message": message})

    # --- 기본 단언문 (Assertions) ---
    
    def assert_contains(self, test_name: str, text: str, substring: str):
        """특정 서브스트링이 결과물에 포함되어 있는지 검증"""
        success = substring in text
        msg = f"키워드 '{substring}' 포함 여부 검사"
        self.log_result(test_name, success, msg if success else f"{msg} 실패 (텍스트: '{text[:30]}...')")

    def assert_json(self, test_name: str, text: str):
        """결과물이 올바른 JSON 포맷인지 검증"""
        try:
            json.loads(text)
            success = True
            msg = "올바른 JSON 구문 구조 검증"
        except json.JSONDecodeError as e:
            success = False
            msg = f"JSON 파싱 실패 ({e})"
        self.log_result(test_name, success, msg)

    def assert_length_range(self, test_name: str, text: str, min_len: int, max_len: int):
        """텍스트 길이가 지정된 바운더리 내에 속하는지 검증"""
        length = len(text)
        success = min_len <= length <= max_len
        msg = f"텍스트 길이 ({length}자) -> 범위 ({min_len} ~ {max_len}자) 만족 여부"
        self.log_result(test_name, success, msg if success else f"{msg} 실패")

    def assert_regex(self, test_name: str, text: str, pattern: str):
        """정규표현식 매칭 검증"""
        success = bool(re.search(pattern, text))
        msg = f"정규식 패턴 '{pattern}' 매칭 여부"
        self.log_result(test_name, success, msg if success else f"{msg} 실패")

    def print_summary(self):
        """최종 평가 결과 요약 레포트 출력"""
        print("\n" + "=" * 40 + " 평가 요약 보고서 " + "=" * 40)
        print(f"총 테스트 수: {self.tests_run} | 성공: {self.tests_passed} | 실패: {self.tests_failed}")
        success_rate = (self.tests_passed / self.tests_run * 100) if self.tests_run > 0 else 0
        print(f"합격률 (Success Rate): {success_rate:.1f}%")
        print("=" * 96)


# --- 테스트 케이스 데이터셋 시뮬레이션 ---
# 실제 환경에서는 LLM API 호출 후 리턴된 response.text 값을 아래 output에 매핑합니다.

MOCK_LLM_OUTPUTS = {
    "case_1_json_formatter": {
        "description": "사용자 정보를 JSON 구조로 정리하라는 프롬프트의 결과물",
        "output": '{"name": "홍길동", "age": 30, "skills": ["Python", "AI Engineering"]}'
    },
    "case_2_short_summary": {
        "description": "본문을 50자 이내로 요약하고 핵심어 '에이전트'를 포함하라는 프롬프트의 결과물",
        "output": "에이전트 오케스트레이션은 멀티 에이전트들의 협업과 상태 전이를 관리하는 최근 핵심 기법입니다." # 53자 (요약 조건 오버)
    },
    "case_3_email_extractor": {
        "description": "텍스트에서 이메일 주소를 포맷에 맞춰 추출하라는 프롬프트의 결과물",
        "output": "추출된 이메일: support@antigravity.google"
    }
}

if __name__ == "__main__":
    runner = AssertionTestRunner()
    
    print("[Start] 평가 하네스 테스터 가동 (Assertion-based Testing Running...)\n")
    
    # Test 1: JSON 포맷 및 데이터 속성 검증
    print("--- Test Suite 1: JSON Formatter Output ---")
    data_1 = MOCK_LLM_OUTPUTS["case_1_json_formatter"]["output"]
    runner.assert_json("TS1_JSON_Syntax", data_1)
    runner.assert_contains("TS1_Contains_Name", data_1, '"name"')
    runner.assert_contains("TS1_Contains_Skills", data_1, '"skills"')
    
    # Test 2: 분량 한계 및 핵심 키워드 유무 검증
    print("\n--- Test Suite 2: Short Summary Restrictions ---")
    data_2 = MOCK_LLM_OUTPUTS["case_2_short_summary"]["output"]
    runner.assert_contains("TS2_Contains_Keyword", data_2, "에이전트")
    # 50자 이내 제한 조건 검증 (실패 유도 시뮬레이션)
    runner.assert_length_range("TS2_Length_Boundary", data_2, min_len=5, max_len=50)
    
    # Test 3: 정규식을 통한 이메일 주소 검출 검증
    print("\n--- Test Suite 3: Data Extraction Regex ---")
    data_3 = MOCK_LLM_OUTPUTS["case_3_email_extractor"]["output"]
    runner.assert_regex("TS3_Email_Regex_Match", data_3, r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")

    # 최종 보고서 요약
    runner.print_summary()
