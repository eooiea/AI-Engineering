"""Module 8: Evaluation Harness & LLM-as-a-Judge Example.

결정론적 어설션(JSON 구문 검증, Regex)과
LLM-as-a-Judge 정량 루브릭(Rubric 1~5점 척도)을 통합하여
프롬프트 회귀(Regression)를 테스트하는 자동화 하네스입니다.
"""

import dataclasses
import json
import sys
from typing import List

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


@dataclasses.dataclass
class TestCase:
    id: str
    prompt: str
    ground_truth: str
    generated_output: str


@dataclasses.dataclass
class EvalReport:
    test_id: str
    deterministic_pass: bool
    judge_score: int
    rubric_feedback: str


class LLMAsAJudgeHarness:
    """하이브리드 평가 하네스 러너."""

    def evaluate_deterministic(self, output: str) -> bool:
        try:
            parsed = json.loads(output)
            return isinstance(parsed, dict) and "status" in parsed
        except Exception:
            return False

    def evaluate_judge_rubric(self, prompt: str, ground_truth: str, generated: str) -> (int, str):
        if "hallucination_detected" in generated:
            return 1, "❌ [1점] 근거 없는 허위 사실이 포함되어 있어 탈락."
        elif "incomplete" in generated:
            return 3, "⚠️ [3점] 대체로 부합하나 필수 세부 항목 일부 누락."
        else:
            return 5, "✅ [5점] Ground Truth에 완벽히 부합하며 군더더기 없는 최상위 품질."

    def run_suite(self, test_cases: List[TestCase]) -> List[EvalReport]:
        reports = []
        for tc in test_cases:
            det_pass = self.evaluate_deterministic(tc.generated_output)
            score, feedback = self.evaluate_judge_rubric(tc.prompt, tc.ground_truth, tc.generated_output)
            reports.append(EvalReport(tc.id, det_pass, score, feedback))
        return reports


def main():
    print("=" * 70)
    print("🧪 Module 8: Evaluation Harness & LLM-as-a-Judge Suite")
    print("=" * 70)

    test_cases = [
        TestCase(
            id="TC-001-HEALTHY",
            prompt="시스템 상태를 JSON으로 보고해줘.",
            ground_truth="status: ok",
            generated_output=json.dumps({"status": "ok", "uptime_hours": 120, "healthy": True})
        ),
        TestCase(
            id="TC-002-SYNTAX-FAIL",
            prompt="에러 로그를 분석해줘.",
            ground_truth="status: error",
            generated_output="Sure! Here is your output: {status: invalid_json}"
        ),
        TestCase(
            id="TC-003-HALLUCINATION",
            prompt="MCP 프로토콜 작성자를 알려줘.",
            ground_truth="Anthropic",
            generated_output=json.dumps({"status": "ok", "note": "hallucination_detected: 작성자는 가상의 인물"})
        )
    ]

    harness = LLMAsAJudgeHarness()
    reports = harness.run_suite(test_cases)

    print("\n[📊 테스트 결과 리포트]")
    passed_count = 0
    total_score = 0

    for rep in reports:
        print(f"\n▶ 테스트 ID: {rep.test_id}")
        print(f"  • 결정론적 규칙 검증: {'PASS ✅' if rep.deterministic_pass else 'FAIL ❌'}")
        print(f"  • LLM Judge 점수:     {rep.judge_score} / 5 점")
        print(f"  • Judge 피드백:       {rep.rubric_feedback}")

        if rep.deterministic_pass and rep.judge_score >= 4:
            passed_count += 1
        total_score += rep.judge_score

    pass_rate = (passed_count / len(test_cases)) * 100
    avg_score = total_score / len(test_cases)

    print("\n" + "=" * 70)
    print(f"📈 최종 요약: 총 {len(test_cases)}개 중 {passed_count}개 통과 (Pass Rate: {pass_rate:.1f}%)")
    print(f"⭐ 전체 평균 Judge 점수: {avg_score:.2f} / 5.0 점")
    print("=" * 70)


if __name__ == "__main__":
    main()
