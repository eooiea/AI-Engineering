"""Module 6: Multi-Agent Orchestration & StateGraph.

LangGraph 스타일의 공유 상태(State) 기반 상태 전이 그래프와
Supervisor-Worker 병렬 분담 및 검증자(Validator) 반려 피드백 루프를 구현한 예제입니다.
"""

import dataclasses
import sys
from typing import List, Dict, Any, Optional

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


@dataclasses.dataclass
class WorkflowState:
    task: str
    outline: List[str] = dataclasses.field(default_factory=list)
    draft_sections: Dict[str, str] = dataclasses.field(default_factory=dict)
    final_article: str = ""
    review_score: int = 0
    feedback: str = ""
    iteration_count: int = 0


class OutlinePlannerAgent:
    def run(self, state: WorkflowState) -> WorkflowState:
        print(f"\n📋 [1. PlannerAgent] 작업 개요 및 목차 설계 중: '{state.task}'")
        state.outline = [
            "1. AI IDE 및 Context Engineering 개요",
            "2. Model Context Protocol (MCP) 표준 아키텍처",
            "3. Multi-Agent StateGraph 오케스트레이션",
            "4. 프로덕션 보안 Guardrails 및 관측 가능성"
        ]
        return state


class SectionWriterAgent:
    def run(self, state: WorkflowState) -> WorkflowState:
        print(f"\n✍️ [2. WriterAgent] {len(state.outline)}개 섹션 본문 작성 중...")
        for sec in state.outline:
            state.draft_sections[sec] = f"[{sec}]에 대한 심층 기술 설명 및 프로덕션 모범 사례 내용."
        state.final_article = "\n\n".join([f"### {k}\n{v}" for k, v in state.draft_sections.items()])
        return state


class QualityValidatorAgent:
    def run(self, state: WorkflowState) -> WorkflowState:
        state.iteration_count += 1
        print(f"\n🔍 [3. ValidatorAgent] 품질 및 누락 사항 심사 (시도 #{state.iteration_count})...")
        
        if state.iteration_count == 1:
            state.review_score = 3
            state.feedback = "보안 및 관측 가능성 섹션에 OpenTelemetry 및 PII 마스킹 언급 보강 필요"
            print(f"  ⚠️ 심사 결과: {state.review_score}/5점 (반려) -> 피드백: {state.feedback}")
        else:
            state.review_score = 5
            state.feedback = "모든 필수 아키텍처 항목이 완벽하게 반영됨."
            print(f"  ✅ 심사 결과: {state.review_score}/5점 (승인 완료)!")
        return state


class StateGraphOrchestrator:
    def __init__(self):
        self.planner = OutlinePlannerAgent()
        self.writer = SectionWriterAgent()
        self.validator = QualityValidatorAgent()

    def run_pipeline(self, task: str) -> WorkflowState:
        state = WorkflowState(task=task)
        state = self.planner.run(state)

        while True:
            state = self.writer.run(state)
            state = self.validator.run(state)

            if state.review_score >= 4:
                print("\n🎯 조건부 라우팅 통과: [End Node]로 전이.")
                break
            else:
                print(f"\n🔄 피드백 반영을 위해 [WriterAgent Node]로 회귀...")
                state.draft_sections["4. 프로덕션 보안 Guardrails 및 관측 가능성"] += (
                    "\n-> [보강] OpenTelemetry Tracing 및 PII 정규식 마스킹 파이프라인 완비."
                )

        return state


def main():
    print("=" * 70)
    print("🤖 Module 6: Multi-Agent StateGraph & Orchestrator")
    print("=" * 70)

    task_desc = "엔터프라이즈 AI 엔지니어링 마스터 백서 작성"
    orchestrator = StateGraphOrchestrator()
    final_state = orchestrator.run_pipeline(task_desc)

    print("\n" + "=" * 70)
    print("🎉 [최종 완성된 멀티 에이전트 산출물]")
    print(f"  • 최종 점수: {final_state.review_score} / 5")
    print(f"  • 반복 횟수: {final_state.iteration_count} 회")
    print(f"  • 본문 요약:\n{final_state.final_article[:250]}...")
    print("=" * 70)


if __name__ == "__main__":
    main()
