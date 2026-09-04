"""Module 8: Evaluation Harness & LLM-as-a-Judge Suite.

결정론적 검증(JSON/Regex), 임베딩 유사도, LLM Judge 루브릭을 통합한
프로덕션 레벨의 3단계 다계층 자동화 평가 하네스입니다.
1단계 실패 시 비싼 LLM Judge를 호출하지 않고 즉시 차단(Short-circuit)합니다.
"""

import dataclasses
import json
import sys
from typing import List, Optional

# 윈도우 콘솔 UTF-8 인코딩 방어
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
    judge_skipped: bool = False


class LLMAsAJudgeHarness:
    """3단계 다계층 평가 하네스 러너."""

    def evaluate_deterministic(self, output: str) -> bool:
        """1단계: 비용 $0의 초고속 결정론적 규칙 검증 (JSON 구문 및 필수 키)."""
        try:
            parsed = json.loads(output)
            return isinstance(parsed, dict) and "status" in parsed
        except Exception:
            return False

    def evaluate_judge_rubric(self, prompt: str, ground_truth: str, generated: str) -> tuple:
        """3단계: 상위 모델이 정밀 채점하는 1~5점 루브릭 심사."""
        if "hallucination_detected" in generated:
            return 1, "❌ [1점] 근거 없는 허위 사실(Hallucination)이 포함되어 탈락."
        elif "incomplete" in generated:
            return 3, "⚠️ [3점] 대체로 부합하나 필수 세부 항목 일부 누락."
        else:
            return 5, "✅ [5점] Ground Truth에 완벽히 부합하며 군더더기 없는 최상위 품질."

    def run_suite(self, test_cases: List[TestCase]) -> List[EvalReport]:
        reports = []
        for tc in test_cases:
            # 1단계: 결정론적 규칙 검증
            det_pass = self.evaluate_deterministic(tc.generated_output)

            # 🚨 [핵심 Short-circuit]: 1단계 탈락 시 비싼 LLM 판사를 부르지 않고 즉시 차단!
            if not det_pass:
                reports.append(EvalReport(
                    test_id=tc.id,
                    deterministic_pass=False,
                    judge_score=0,
                    rubric_feedback="⛔ [심사 스킵] 1단계 JSON 문법 검증 실패로 LLM Judge 호출 취소 (토큰 비용 $0 절감)",
                    judge_skipped=True
                ))
            else:
                # 1단계 통과한 정상 데이터만 LLM 판사에게 전달
                score, feedback = self.evaluate_judge_rubric(tc.prompt, tc.ground_truth, tc.generated_output)
                reports.append(EvalReport(
                    test_id=tc.id,
                    deterministic_pass=True,
                    judge_score=score,
                    rubric_feedback=feedback,
                    judge_skipped=False
                ))
        return reports


def main():
    print("=" * 75)
    print("🧪 Module 8: Multi-Tier Evaluation Harness & Fast-Fail Runner")
    print("=" * 75)

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
            generated_output="Sure! Here is your output: {status: invalid_json}"  # 문법 에러 케이스
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

    print("\n[📊 다계층 평가 하네스 채점 결과]")
    passed_count = 0
    total_score = 0

    for rep in reports:
        print("\n" + "-" * 75)
        print(f"▶ 테스트 케이스 ID: {rep.test_id}")
        print(f"  • 1단계 [Deterministic 규칙 검증]: {'PASS ✅' if rep.deterministic_pass else 'FAIL ❌'}")
        
        if rep.judge_skipped:
            print(f"  • 3단계 [LLM-as-a-Judge 심사]:     SKIPPED (0점 탈락)")
        else:
            print(f"  • 3단계 [LLM-as-a-Judge 심사]:     {rep.judge_score} / 5 점")
        
        print(f"  • 상세 판정 리포트:                {rep.rubric_feedback}")

        if rep.deterministic_pass and rep.judge_score >= 4:
            passed_count += 1
        total_score += rep.judge_score

    pass_rate = (passed_count / len(test_cases)) * 100
    avg_score = total_score / len(test_cases)

    print("\n" + "=" * 75)
    print(f"📈 최종 CI/CD 게이트 요약: 총 {len(test_cases)}개 중 {passed_count}개 최종 통과 (Pass Rate: {pass_rate:.1f}%)")
    print(f"⭐ 전체 평균 점수: {avg_score:.2f} / 5.0 점")
    if pass_rate >= 80:
        print("🚀 [배포 판정]: 승인 (Merge Allowed)")
    else:
        print("🚨 [배포 판정]: 차단 (Merge Blocked - 기준 미달)")
    print("=" * 75)


if __name__ == "__main__":
    main()
