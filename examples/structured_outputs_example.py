"""Module 3: Structured Outputs & Self-Correction (Self-Healing) Example.

Pydantic을 활용한 엄격한 스키마 강제와, 실행 시 런타임 버그나 스키마 위반이 발생했을 때
에러 트레이스를 피드백으로 주입하여 자가 수정하는 Reflection 루프 구현체입니다.
"""

import json
import sys
from typing import List, Optional
from pydantic import BaseModel, Field, ValidationError

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


class CodeRefactoringTask(BaseModel):
    target_file: str = Field(description="리팩토링 대상 파일명")
    complexity_score: int = Field(ge=1, le=10, description="코드 복잡도 (1~10)")
    identified_issues: List[str] = Field(min_length=1, description="식별된 코드 문제점 목록")
    suggested_code: str = Field(description="리팩토링된 파이썬 코드")
    approved_by_lead: bool = Field(default=False, description="테크리드 승인 여부")


class SelfHealingAgent:
    """에러 피드백을 수신하여 스스로 코드를 고치는 자가 치유 에이전트."""

    def __init__(self, max_retries: int = 3):
        self.max_retries = max_retries

    def mock_llm_generate(self, attempt: int, error_feedback: Optional[str] = None) -> str:
        if attempt == 1:
            return json.dumps({
                "target_file": "payment_service.py",
                "complexity_score": 15,
                "identified_issues": [],
                "suggested_code": "def process(): return 1 / 0",
                "approved_by_lead": False
            })
        elif attempt == 2:
            return json.dumps({
                "target_file": "payment_service.py",
                "complexity_score": 7,
                "identified_issues": ["잠재적인 0으로 나누기 런타임 오류 존재"],
                "suggested_code": "def process(): return 1 / 0",
                "approved_by_lead": False
            })
        else:
            return json.dumps({
                "target_file": "payment_service.py",
                "complexity_score": 3,
                "identified_issues": ["0으로 나누기 방어 로직 추가", "안전한 반환 타입 처리"],
                "suggested_code": "def process(amount: float, count: int) -> float:\n    return amount / count if count > 0 else 0.0",
                "approved_by_lead": True
            })

    def execute_and_heal(self) -> CodeRefactoringTask:
        error_trace: Optional[str] = None

        for attempt in range(1, self.max_retries + 1):
            print(f"\n🔄 [시도 #{attempt}] LLM 추론 및 코드 검증 시작...")
            raw_output = self.mock_llm_generate(attempt, error_trace)
            print(f"  • 수신된 Raw JSON: {raw_output}")

            try:
                data = json.loads(raw_output)
                task_obj = CodeRefactoringTask(**data)
                print("  ✅ 1단계 Pydantic 스키마 유효성 검사 통과!")
            except (json.JSONDecodeError, ValidationError) as e:
                error_trace = f"Schema ValidationError: {str(e)}"
                print(f"  ❌ 1단계 스키마 검증 실패: {error_trace}")
                continue

            try:
                local_scope = {}
                exec(task_obj.suggested_code, {}, local_scope)
                if "process" in local_scope:
                    fn = local_scope["process"]
                    if fn.__code__.co_argcount == 0:
                        fn()
                    else:
                        fn(100.0, 5)
                print("  ✅ 2단계 런타임 실행 테스트 통과 (버그 없음)!")
                return task_obj
            except Exception as e:
                error_trace = f"Runtime Execution Error: {type(e).__name__}: {str(e)}"
                print(f"  ❌ 2단계 런타임 테스트 실패: {error_trace}")
                print(f"  🔁 에러 피드백을 LLM에 주입하여 자가 수정(Self-Correction) 요청...")

        raise RuntimeError("최대 재시도 횟수 초과: 자가 치유 실패")


def main():
    print("=" * 70)
    print("📐 Module 3: Structured Outputs & Self-Healing Pipeline")
    print("=" * 70)

    agent = SelfHealingAgent(max_retries=3)
    final_result = agent.execute_and_heal()

    print("\n" + "=" * 70)
    print("🎉 [최종 자가 치유 완료된 구조화 결과]")
    print(f"  • 대상 파일:    {final_result.target_file}")
    print(f"  • 복잡도 점수:  {final_result.complexity_score} / 10")
    print(f"  • 조치 사항:    {final_result.identified_issues}")
    print(f"  • 리팩토링 코드:\n{final_result.suggested_code}")
    print(f"  • 테크리드 승인: {final_result.approved_by_lead}")
    print("=" * 70)


if __name__ == "__main__":
    main()
