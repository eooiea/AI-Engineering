"""Module 6: Multi-Agent StateGraph & Async Parallel Orchestrator.

이 예제는 앤트로픽과 LangGraph의 핵심 표준 패턴인:
1. Supervisor-Worker 병렬 분담 (Parallel Fan-out & Fan-in via asyncio.gather)
2. 공유 상태 객체 (WorkflowState)를 통한 데이터 통신
3. 검증자(Validator) 반려 시 특정 워커만 재호출하는 자가 치유 피드백 루프
를 완벽하게 시각화한 실전 오케스트레이션 엔진입니다.
"""

import asyncio
import dataclasses
import random
import sys
import time
from typing import Dict, List, Optional

# 윈도우 콘솔 한글 인코딩 방어
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


# ==============================================================================
# 1. State: 모든 에이전트가 공유하는 공용 작업 칠판
# ==============================================================================
@dataclasses.dataclass
class WorkflowState:
    task: str
    outline: List[str] = dataclasses.field(default_factory=list)
    draft_sections: Dict[str, str] = dataclasses.field(default_factory=dict)
    final_article: str = ""
    review_score: int = 0
    feedback: str = ""
    iteration: int = 0


# ==============================================================================
# 2. 전문 에이전트 군단 (Workers)
# ==============================================================================
class OutlinePlannerAgent:
    """1단계: 사용자 요구사항을 분석하여 세부 목차를 쪼개는 기획자 에이전트."""

    async def plan(self, state: WorkflowState) -> WorkflowState:
        print("\n" + "=" * 75)
        print(f"📋 [1단계: PlannerAgent] 대형 작업 분해 및 목차 기획 시작")
        print(f"   • 인입된 목표: '{state.task}'")
        print("=" * 75)
        await asyncio.sleep(0.3)  # 기획 추론 시뮬레이션

        state.outline = [
            "섹션 1. Modern AI IDE & Context Packaging 아키텍처",
            "섹션 2. Model Context Protocol (MCP) 표준 프로토콜",
            "섹션 3. Multi-Agent StateGraph & 병렬 오케스트레이션",
            "섹션 4. 프로덕션 보안 Guardrails & OpenTelemetry 관측성"
        ]
        print("  ✅ 목차 기획 완료! 총 4개의 세부 전문 집필 태스크로 분할되었습니다.")
        for idx, item in enumerate(state.outline, 1):
            print(f"     {idx}) {item}")
        return state


class SectionWriterWorker:
    """2단계: 개별 섹션 하나를 전담하여 깊이 있게 작성하는 전문 작가 워커."""

    def __init__(self, worker_id: int):
        self.worker_id = worker_id

    async def write_section(self, section_title: str, feedback: Optional[str] = None) -> tuple:
        start_time = time.perf_counter()
        
        # 병렬성 체감을 위한 비동기 딜레이 (각자 처리 속도가 다름)
        delay = random.uniform(0.3, 0.7)
        if feedback:
            print(f"  ✍️  [Worker #{self.worker_id}] 피드백을 반영하여 '{section_title}' 집중 재집필 중...")
            delay = 0.4
        else:
            print(f"  ⚡ [Worker #{self.worker_id}] 병렬 작업 착수: '{section_title}' 집필 중...")

        await asyncio.sleep(delay)

        # 집필 내용 생성
        if "보안" in section_title and feedback:
            content = (
                f"[{section_title}]\n"
                f"- [피드백 보강 완료] OpenTelemetry 분산 트레이싱을 연동하여 토큰 누수를 방지합니다.\n"
                f"- 개인정보(PII) 마스킹 정규식 필터를 적용하여 엔터프라이즈 보안 기준을 100% 충족합니다."
            )
        else:
            content = (
                f"[{section_title}]\n"
                f"- 해당 도메인의 핵심 설계 원리와 실제 파이썬 엔지니어링 구현 패턴을 설명합니다.\n"
                f"- 프로덕션 환경에서의 고가용성 및 비용 최적화(Caching) 방안을 포함합니다."
            )

        elapsed = time.perf_counter() - start_time
        print(f"  🏁 [Worker #{self.worker_id}] 집필 완료! (소요 시간: {elapsed:.2f}초)")
        return section_title, content


class QualityValidatorAgent:
    """3단계: 완성된 문서를 종합 채점하고 결함을 짚어내는 심사관 에이전트."""

    async def validate(self, state: WorkflowState) -> WorkflowState:
        state.iteration += 1
        print("\n" + "=" * 75)
        print(f"🔍 [3단계: ValidatorAgent] 문서 종합 품질 심사 (시도 #{state.iteration})")
        print("=" * 75)
        await asyncio.sleep(0.4)

        sec4_content = state.draft_sections.get("섹션 4. 프로덕션 보안 Guardrails & OpenTelemetry 관측성", "")

        # 1차 시도: 보안 섹션 본문에 'OpenTelemetry 분산 트레이싱' 언급이 없으면 반려
        if "분산 트레이싱" not in sec4_content:
            state.review_score = 3
            state.feedback = "섹션 4 본문에 'OpenTelemetry 분산 트레이싱' 및 'PII 마스킹' 내용이 누락되었습니다."
            print(f"  ❌ 심사 결과: {state.review_score}/5점 [반려 (Reject)]")
            print(f"     👉 사유: {state.feedback}")
            print("\n  🔁 [조건부 엣지 발동]: 기준 미달로 인해 섹션 4 워커에게 핀포인트 재작업 지시!")
        else:
            state.review_score = 5
            state.feedback = "모든 기술 요구사항과 보안 감사 기준을 완벽하게 만족합니다."
            print(f"  ✅ 심사 결과: {state.review_score}/5점 [승인 완료 (Approve)]!")
            print(f"     👉 총평: {state.feedback}")
            print("\n  🎯 [조건부 엣지 발동]: 만점 승인 통과! 최종 [End Node]로 이동합니다.")

        return state


# ==============================================================================
# 3. StateGraph 오케스트레이터 (총괄 지휘자 / Supervisor)
# ==============================================================================
class StateGraphOrchestrator:
    """에이전트들의 병렬 분담(Fan-out), 취합(Fan-in), 반려 루프를 총괄 조율하는 지휘자."""

    def __init__(self):
        self.planner = OutlinePlannerAgent()
        self.validator = QualityValidatorAgent()

    async def run(self, task: str) -> WorkflowState:
        state = WorkflowState(task=task)

        # Step 1. 기획 수립
        state = await self.planner.plan(state)

        # Step 2 & 3. 집필 및 검증 루프
        while True:
            # ------------------------------------------------------------------
            # 🚀 [핵심: Parallel Fan-out] 4명의 워커를 동시에 기동!
            # ------------------------------------------------------------------
            if not state.draft_sections:
                print("\n" + "=" * 75)
                print(f"🚀 [Supervisor] 4명의 전문 작가 워커에게 동시 병렬 집필 명령 하달 (Fan-out)!")
                print("=" * 75)

                # 4개의 비동기 태스크를 동시에 생성
                tasks = []
                for idx, sec_title in enumerate(state.outline, 1):
                    worker = SectionWriterWorker(worker_id=idx)
                    tasks.append(worker.write_section(sec_title))

                # 🔥 asyncio.gather: 4개의 작업을 병렬로 한꺼번에 실행하고 결과를 기다림 (Fan-in)
                results = await asyncio.gather(*tasks)

                # 결과 취합 (Fan-in Synthesis)
                for title, content in results:
                    state.draft_sections[title] = content

                print(f"\n📥 [Supervisor] 4개 섹션의 병렬 작성이 모두 완료되어 통합 취합(Fan-in) 완료!")

            elif state.review_score < 4:
                # 🎯 자가 치유: 전체를 다 다시 쓰는 게 아니라 문제 있는 섹션만 핀포인트 재작업!
                target_sec = "섹션 4. 프로덕션 보안 Guardrails & OpenTelemetry 관측성"
                worker = SectionWriterWorker(worker_id=4)
                title, content = await worker.write_section(target_sec, feedback=state.feedback)
                state.draft_sections[title] = content

            # Step 3. 품질 검증
            state = await self.validator.validate(state)

            # 승인 기준 통과 시 루프 탈출
            if state.review_score >= 4:
                break

        # 최종 문서 조립
        state.final_article = "\n\n".join([f"## {k}\n{v}" for k, v in state.draft_sections.items()])
        return state


# ==============================================================================
# 메인 실행부
# ==============================================================================
async def main():
    print("=" * 75)
    print("🤖 Module 6: Real-world Async Multi-Agent StateGraph Demonstration")
    print("=" * 75)

    orchestrator = StateGraphOrchestrator()
    final_state = await orchestrator.run("엔터프라이즈 AI 엔지니어링 마스터 백서 작성")

    print("\n" + "=" * 75)
    print("🎉 [최종 오케스트레이션 완성 산출물]")
    print("=" * 75)
    print(f"  • 최종 평점:       {final_state.review_score} / 5 점")
    print(f"  • 자가 치유 턴수:   {final_state.iteration} 회")
    print(f"  • 집필된 총 섹션:   {len(final_state.draft_sections)} 개")
    print("\n📄 [완성된 본문 미리보기]:")
    print("-" * 75)
    for title, content in final_state.draft_sections.items():
        print(f"▶ {title}")
        for line in content.splitlines()[1:]:
            print(f"   {line}")
    print("-" * 75)
    print("\n💡 [오케스트레이션 핵심 정리]")
    print("   1. Supervisor가 작업을 쪼개 4개 워커에게 병렬로 뿌림 (Fan-out).")
    print("   2. asyncio.gather로 4명이 동시에 작업하여 소요 시간 70% 단축 (Fan-in).")
    print("   3. Validator가 반려 시 결함이 있는 특정 워커만 호출하여 스스로 완성!")
    print("=" * 75)


if __name__ == "__main__":
    asyncio.run(main())
