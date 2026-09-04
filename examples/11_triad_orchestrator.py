"""Module 11: The Modern Agentic Triad Orchestrator (Harness, Loop, & Graph).

2026 현대 AI 엔지니어링 3대 핵심 기둥인
1) 🕸️ Graph Engineering (StateGraph 상태 머신 및 조건부 전이)
2) 🔄 Loop Engineering (자가 치유 루프, 서킷 브레이커, 진동 방지 및 스냅샷 롤백)
3) 🛡️ Harness Engineering (다계층 자동 채점 하네스 및 게이트)
의 유기적 결합을 완벽히 시뮬레이션하는 통합 오케스트레이터입니다.
"""

import dataclasses
import enum
import json
import sys
import time
from typing import Dict, List, Optional

# 윈도우 콘솔 UTF-8 인코딩 방어
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


class CircuitState(enum.Enum):
    CLOSED = "CLOSED"      # 정상 동작: 에이전트 자율 루프 허용
    OPEN = "OPEN"          # 장애 감지: 루프 차단, 스냅샷 롤백, HITL 에스컬레이션
    HALF_OPEN = "HALF_OPEN"  # 카나리아 시험 실행


@dataclasses.dataclass
class TriadState:
    task: str
    plan: Optional[str] = None
    generated_code: Optional[str] = None
    retry_count: int = 0
    failure_history: List[str] = dataclasses.field(default_factory=list)
    last_safe_snapshot: Optional[str] = None
    circuit_state: CircuitState = CircuitState.CLOSED
    is_completed: bool = False
    final_output: Optional[str] = None


class CircuitBreaker:
    """에이전트 무한 진동 및 발산(Divergence) 방지 서킷 브레이커."""

    def __init__(self, failure_threshold: int = 3):
        self.failure_threshold = failure_threshold
        self.consecutive_failures = 0
        self.state = CircuitState.CLOSED

    def record_success(self) -> None:
        self.consecutive_failures = 0
        self.state = CircuitState.CLOSED

    def record_failure(self, reason: str) -> CircuitState:
        self.consecutive_failures += 1
        if self.consecutive_failures >= self.failure_threshold:
            self.state = CircuitState.OPEN
        return self.state


class EvaluationHarness:
    """하네스 계층: 결정론적 린트 + 채점 기준 검증."""

    def verify_code(self, code: str) -> (bool, str):
        # 1. 결정론적 규칙 검증 (기본 문법 및 필수 함수 선언)
        if "def solution(" not in code:
            return False, "결정론적 검증 실패: 'def solution(' 선언이 누락되었습니다."
        if "return" not in code:
            return False, "결정론적 검증 실패: 'return' 문이 없습니다."
        
        # 2. 실행 안정성 (0으로 나누기, 구문 오류 시뮬레이션)
        if "1 / 0" in code or "ZeroDivisionError" in code:
            return False, "런타임 검증 실패: 0으로 나누기 예외 발생."

        return True, "하네스 통과: 모든 결정론적 테스트 및 루브릭 100점 달성."


class TriadOrchestrator:
    """Graph, Loop, Harness를 통합한 현대적 트라이어드 러너."""

    def __init__(self):
        self.circuit_breaker = CircuitBreaker(failure_threshold=3)
        self.harness = EvaluationHarness()

    # --- Graph Nodes ---
    def node_planner(self, state: TriadState) -> TriadState:
        print(f"\n[🕸️ Graph Node: Planner] '{state.task}' 계획 수립 중...")
        state.plan = "1. 입력 검증 2. 로직 구현 3. 반환값 포맷팅"
        state.last_safe_snapshot = "def solution(x):\n    # 초기 안전 스냅샷\n    return x"
        return state

    def node_generator(self, state: TriadState) -> TriadState:
        print(f"[🔄 Loop Node: Act/Generator] 시도 횟수 #{state.retry_count + 1}")
        
        # 시뮬레이션: 첫 2번은 일부러 결함 있는 코드를 생성하여 자가 치유 루프 검증
        if state.retry_count == 0:
            state.generated_code = "def solve_bad(x):\n    # 잘못된 함수명\n    return x * 2"
        elif state.retry_count == 1:
            state.generated_code = "def solution(x):\n    # 런타임 결함 주입\n    y = 1 / 0\n    return y"
        else:
            state.generated_code = "def solution(x):\n    # 완전한 자가 치유 코드\n    return x * 10"
            
        return state

    def node_verifier(self, state: TriadState) -> TriadState:
        print(f"[🛡️ Harness Node: Verify] 생성된 코드 하네스 검증 실행...")
        passed, message = self.harness.verify_code(state.generated_code or "")
        
        if passed:
            print(f"  --> ✅ {message}")
            self.circuit_breaker.record_success()
            state.circuit_state = CircuitState.CLOSED
            state.is_completed = True
            state.final_output = state.generated_code
        else:
            print(f"  --> ❌ {message}")
            state.failure_history.append(message)
            c_state = self.circuit_breaker.record_failure(message)
            state.circuit_state = c_state
            state.retry_count += 1
            
        return state

    # --- Graph Conditional Edge ---
    def route_next_step(self, state: TriadState) -> str:
        if state.is_completed:
            return "SUCCESS"
        if state.circuit_state == CircuitState.OPEN:
            return "CIRCUIT_TRIPPED"
        return "RETRY_LOOP"

    def run(self, task: str) -> TriadState:
        state = TriadState(task=task)
        
        # 1. StateGraph 시작: 계획 노드
        state = self.node_planner(state)

        # 2. Loop & Harness 사이클
        while not state.is_completed:
            state = self.node_generator(state)
            state = self.node_verifier(state)
            
            next_step = self.route_next_step(state)
            
            if next_step == "SUCCESS":
                print("\n🎉 [Triad 완료] 자가 치유 루프 성공 및 하네스 전수 통과!")
                break
            elif next_step == "CIRCUIT_TRIPPED":
                print("\n🚨 [Circuit Breaker 발동!] 루프 발산 감지 -> 서킷 차단(OPEN)")
                print(f"  * 마지막 안전 스냅샷으로 롤백 실행:\n{state.last_safe_snapshot}")
                print("  * 인간 승인자(HITL) 호출 및 Slack 에스컬레이션 트리거.")
                break
            else:
                print(f"  -> [지수 백오프] 0.5초 대기 후 자가 치유 재시도...\n")
                time.sleep(0.5)

        return state


if __name__ == "__main__":
    print("=" * 70)
    print("🚀 Module 11: The Modern Agentic Triad (Harness-Loop-Graph) 시뮬레이터")
    print("=" * 70)

    orchestrator = TriadOrchestrator()
    final_state = orchestrator.run("배열 요소를 10배로 스케일링하는 최적화 솔루션 작성")

    print("\n[최종 상태 점검]")
    print(f"- 완료 여부: {final_state.is_completed}")
    print(f"- 총 시도 횟수: {final_state.retry_count + (1 if final_state.is_completed else 0)}회")
    print(f"- 최종 서킷 상태: {final_state.circuit_state.value}")
    print(f"- 최종 생성 코드:\n{final_state.final_output}")
