"""Module 3: Structured Outputs & Self-Correction (자가 치유 파이프라인).

이 예제는 현대 AI 엔지니어링의 핵심인:
1. Pydantic을 활용한 엄격한 스키마(규격) 강제
2. LLM이 짠 코드를 샌드박스 환경에서 실제 실행해보는 런타임 테스트
3. 에러 발생 시 에러 메시지를 피드백으로 주입하여 스스로 고치게 하는 자가 치유(Self-Healing) 루프
의 전 과정을 단계별로 시각화하여 보여주는 교육용 시뮬레이터입니다.
"""

import json
import sys
import time
from typing import List, Optional
from pydantic import BaseModel, Field, ValidationError

# 윈도우 파워셸/CMD 콘솔 한글 깨짐 방지 설정
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


# ==============================================================================
# 1. Pydantic 스키마 정의 (LLM이 지켜야 할 엄격한 출력 서식)
# ==============================================================================
class CodeRefactoringTask(BaseModel):
    """LLM이 반드시 준수해야 하는 JSON 출력 데이터 규격."""

    target_file: str = Field(
        description="리팩토링 대상 파일명"
    )
    complexity_score: int = Field(
        ge=1, le=10, 
        description="코드 복잡도 점수 (반드시 1 이상 10 이하의 정수)"
    )
    identified_issues: List[str] = Field(
        min_length=1, 
        description="식별된 코드 문제점 목록 (최소 1개 이상 작성 필수)"
    )
    suggested_code: str = Field(
        description="수정된 파이썬 함수 코드"
    )
    approved_by_lead: bool = Field(
        default=False, 
        description="테크리드 승인 여부 (검증 통과 시 True)"
    )


# ==============================================================================
# 2. 자가 치유 에이전트 클래스 (Self-Healing Loop)
# ==============================================================================
class SelfHealingAgent:
    """에러가 발생할 때마다 에러 내용을 피드백으로 삼아 스스로 고치는 에이전트."""

    def __init__(self, max_retries: int = 3):
        self.max_retries = max_retries

    def mock_llm_generate(self, attempt: int, error_feedback: Optional[str] = None) -> str:
        """LLM의 추론 과정을 모방하는 Mock 생성기 (단계별 버그 시뮬레이션)."""
        if attempt == 1:
            # ❌ [시도 1의 LLM]: 규칙을 무시하고 점수를 15점으로 줌 + 문제점 목록을 빈 배열([])로 줌
            return json.dumps({
                "target_file": "payment_service.py",
                "complexity_score": 15,  # 10점 초과 (규격 위반!)
                "identified_issues": [],  # 최소 1개 필수인데 비어있음 (규격 위반!)
                "suggested_code": "def process():\n    return 1 / 0",  # 실행 시 버그
                "approved_by_lead": False
            }, ensure_ascii=False, indent=2)

        elif attempt == 2:
            # ⚠️ [시도 2의 LLM]: 시도 1의 Pydantic 에러를 보고 점수와 목록은 고쳤으나,
            # 코드는 여전히 0으로 나누는 치명적인 버그 코드를 제출함
            return json.dumps({
                "target_file": "payment_service.py",
                "complexity_score": 7,   # ✅ 규칙 통과 (1~10)
                "identified_issues": ["0으로 나누기 런타임 잠재 위험 감지"],  # ✅ 규칙 통과
                "suggested_code": "def process():\n    return 1 / 0",  # ❌ 실행 시 ZeroDivisionError!
                "approved_by_lead": False
            }, ensure_ascii=False, indent=2)

        else:
            # 🎉 [시도 3의 LLM]: 시도 2의 런타임 에러 피드백을 보고 완벽하게 방어 코드를 짜옴
            return json.dumps({
                "target_file": "payment_service.py",
                "complexity_score": 3,   # ✅ 안전한 점수
                "identified_issues": [
                    "0으로 나누기 예외 방어 로직 추가 (if count > 0)",
                    "안전한 float 반환 타입 힌팅 적용"
                ],
                "suggested_code": (
                    "def process(amount: float, count: int) -> float:\n"
                    "    # 분모(count)가 0보다 클 때만 나눗셈을 수행합니다.\n"
                    "    return amount / count if count > 0 else 0.0"
                ),
                "approved_by_lead": True
            }, ensure_ascii=False, indent=2)

    def execute_and_heal(self) -> CodeRefactoringTask:
        """자가 치유 메인 파이프라인: 생성 ──► Pydantic 검사 ──► 런타임 실행 테스트 ──► 재시도."""
        error_trace: Optional[str] = None

        for attempt in range(1, self.max_retries + 1):
            print("\n" + "=" * 75)
            print(f"🔄 [시도 #{attempt}] 에이전트 추론 및 2단계 검증 시작")
            print("=" * 75)

            if error_feedback := error_trace:
                print("\n📩 [이전 턴의 에러 피드백이 LLM 프롬프트에 주입됨]:")
                print(f"   \"{error_feedback}\"")
                print("   👉 LLM이 이 에러를 분석하여 수정을 시도합니다...")

            # 1. LLM 출력 수신
            raw_output = self.mock_llm_generate(attempt, error_trace)
            print(f"\n📥 [LLM이 반환한 응답 데이터]:\n{raw_output}\n")

            # ------------------------------------------------------------------
            # 1단계 검증: Pydantic 스키마 유효성 검사 (포맷/타입/범위 검증)
            # ------------------------------------------------------------------
            print("🔍 [1단계 검증: Pydantic 스키마 검사 진행 중...]")
            try:
                data = json.loads(raw_output)
                task_obj = CodeRefactoringTask(**data)
                print("  ✅ 1단계 통과: 모든 JSON 필드 타입과 범위 규격(1~10점, 리스트 길이)을 만족합니다.")
            except (json.JSONDecodeError, ValidationError) as e:
                # Pydantic 검증 실패 시: 에러 메시지를 추출하여 다음 시도의 프롬프트로 넘김
                error_trace = f"Pydantic ValidationError: {str(e).splitlines()[0]}"
                print(f"  ❌ 1단계 탈락! 규격 위반 발생:")
                print(f"     👉 {error_trace}")
                print("\n  🔁 [시스템 조치]: 에러 상세 내용을 LLM에게 피드백으로 되먹이고 재작성을 요구합니다.")
                continue

            # ------------------------------------------------------------------
            # 2단계 검증: 런타임 실행 테스트 (실제 컴퓨터에서 돌려보기)
            # ------------------------------------------------------------------
            print("\n🔍 [2단계 검증: 파이썬 실제 코드 실행(Sandboxed Exec) 테스트 중...]")
            try:
                local_scope = {}
                # LLM이 제안한 코드를 격리된 환경에서 컴파일 및 실행
                exec(task_obj.suggested_code, {}, local_scope)

                if "process" in local_scope:
                    fn = local_scope["process"]
                    # 파라미터가 없으면 fn(), 파라미터가 있으면 fn(100.0, 5)로 모의 테스트
                    if fn.__code__.co_argcount == 0:
                        fn()
                    else:
                        test_val = fn(100.0, 5)
                        # 0으로 나누는 극단적 케이스도 테스트
                        zero_val = fn(100.0, 0)
                        assert zero_val == 0.0, "0 나누기 방어 실패"

                print("  ✅ 2단계 통과: 코드가 에러 없이 정상 실행되었으며 0 나누기 엣지 케이스를 방어했습니다!")
                return task_obj

            except Exception as e:
                # 런타임 에러 발생 시: 스택트레이스를 추출하여 다음 시도로 주입
                error_trace = f"RuntimeError: {type(e).__name__} ({str(e)})"
                print(f"  ❌ 2단계 탈락! 코드는 문법상 맞으나 실행 중 프로그램이 뻗었습니다:")
                print(f"     👉 {error_trace}")
                print("\n  🔁 [시스템 조치]: '당신이 짠 코드를 돌렸더니 0으로 나누기 에러가 납니다'라고 LLM에 경고합니다.")

        raise RuntimeError("최대 재시도 횟수를 초과했습니다.")


# ==============================================================================
# 메인 실행부
# ==============================================================================
def main():
    print("=" * 75)
    print("📐 Module 3: Structured Outputs & Self-Healing Pipeline Demonstration")
    print("=" * 75)
    print("이 데모는 LLM이 실수하더라도 시스템이 [1단계 스키마 검증]과 [2단계 코드 실행 검증]을 거쳐")
    print("스스로 완벽한 답을 찾아내는 '자가 치유(Self-Correction)' 과정을 보여줍니다.")

    agent = SelfHealingAgent(max_retries=3)
    final_result = agent.execute_and_heal()

    print("\n" + "=" * 75)
    print("🎉 [최종 검증 완료: 2단계 관문을 모두 뚫고 자가 치유된 최종 결과물]")
    print("=" * 75)
    print(f"  • 대상 파일:      {final_result.target_file}")
    print(f"  • 복잡도 점수:    {final_result.complexity_score} / 10 (정상 범위)")
    print(f"  • 조치 사항 목록:  {final_result.identified_issues}")
    print(f"  • 테크리드 승인:  {final_result.approved_by_lead}")
    print(f"  • 리팩토링된 최종 코드:")
    print("    " + "-" * 60)
    for line in final_result.suggested_code.splitlines():
        print(f"    {line}")
    print("    " + "-" * 60)
    print("\n💡 [핵심 교훈]")
    print("   AI에게 '잘해줘'라고 기도하지 말고,")
    print("   Pydantic 스키마와 자동화 테스트로 에러를 잡아내어 AI에게 다시 먹여주면 100% 견고해집니다!")
    print("=" * 75)


if __name__ == "__main__":
    main()
