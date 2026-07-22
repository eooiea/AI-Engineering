"""Context Engineering & Token Budgeting Simulation Module.

5대 컨텍스트 페이로드 조립, scripts/ 헬퍼 스크립트를 활용한 토큰 다이어트 및 컨텍스트 윈도우 최적화를 시연합니다.
"""
import sys
from pathlib import Path

# check_style 스크립트 경로 연동
sys.path.append(str(Path(__file__).parent.parent / ".agents" / "skills" / "review-code" / "scripts"))
try:
    from check_style import analyze_code_style
    HAS_CHECK_STYLE = True
except ImportError:
    HAS_CHECK_STYLE = False


class ContextPackager:
    """AI IDE 백그라운드 컨텍스트 페이로드 조립기."""
    def __init__(self):
        self.system_rules = "AGENTS.md: 모든 답변은 정중한 한글로 작성하고 PEP8 규격을 준수한다."
        self.skill_instructions = "SKILL.md(review-code): 스코어 테이블 및 세부 피드백을 제공한다."

    def build_naive_payload(self, raw_code: str, user_prompt: str) -> dict:
        """[나쁜 예시] 수천 줄 전체 코드를 통째로 주입하는 방식."""
        content = f"{self.system_rules}\n{self.skill_instructions}\n[전체 소스코드]\n{raw_code}\n[지시]\n{user_prompt}"
        token_estimate = len(content) // 4  # 대략적인 토큰 수 추정
        return {"type": "Naive (전체 코드 주입)", "content_length": len(content), "tokens": token_estimate}

    def build_optimized_payload(self, raw_code: str, user_prompt: str) -> dict:
        """[우수한 컨텍스트 엔지니어링] scripts/ 정적 파싱 결과 요약본만 주입하는 방식."""
        if HAS_CHECK_STYLE:
            script_result = analyze_code_style(raw_code)
            summary_str = f"check_style.py 정적 분석 결과: {script_result}"
        else:
            summary_str = "check_style.py 요약: snake_case 위반 없음, docstring 누락 2건"

        content = f"{self.system_rules}\n{self.skill_instructions}\n[scripts/ 헬퍼 정적 파싱 요약]\n{summary_str}\n[지시]\n{user_prompt}"
        token_estimate = len(content) // 4
        return {"type": "Optimized (scripts/ 요약 주입)", "content_length": len(content), "tokens": token_estimate}


if __name__ == "__main__":
    print("[Start] Module 0: Context Engineering & Token Budgeting 실습\n")
    
    # 500줄 분량의 샘플 대형 파이썬 소스 코드 가정
    sample_code = """
def badFunctionName(x, y):
    return x + y

class sampleClass:
    def processData(self, data):
        pass
""" * 50  # 50번 반복하여 250줄 이상의 코드 생성

    packager = ContextPackager()
    user_query = "이 코드 스타일 검사하고 리뷰 보고서 작성해 줘"

    naive_res = packager.build_naive_payload(sample_code, user_query)
    opt_res = packager.build_optimized_payload(sample_code, user_query)

    print("=" * 40 + " 컨텍스트 페이로드 비교 " + "=" * 40)
    print(f"1) {naive_res['type']}:")
    print(f"   - 글자 수: {naive_res['content_length']}자 | 추정 토큰: {naive_res['tokens']} tokens")
    print(f"\n2) {opt_res['type']}:")
    print(f"   - 글자 수: {opt_res['content_length']}자 | 추정 토큰: {opt_res['tokens']} tokens")
    
    saved_percent = (1 - opt_res['tokens'] / naive_res['tokens']) * 100
    print("-" * 96)
    print(f"[Result] scripts/ 헬퍼 스크립트 활용으로 [ {saved_percent:.1f}% ] 의 토큰 절감 및 컨텍스트 윈도우 최적화 달성!")
    print("=" * 96)
