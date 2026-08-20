"""Module 5: Human-in-the-Loop (HITL) & Safety Governance Example.

부수 효과(Side-Effect)가 큰 위험 도구 실행 시
시스템을 일시 정지(Interrupt)하고 관리자 승인(Approval)을 받아 재개(Resume)하는
상태 머신 제어 구현체입니다.
"""

import dataclasses
import enum
import sys
import time
from typing import Dict, Any, Callable, Optional

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


class ToolRiskLevel(enum.Enum):
    SAFE_READ = "SAFE_READ"
    DANGEROUS_WRITE = "DANGEROUS"


@dataclasses.dataclass
class ToolDefinition:
    name: str
    risk_level: ToolRiskLevel
    func: Callable[..., Any]
    description: str


class ExecutionState(enum.Enum):
    RUNNING = "RUNNING"
    INTERRUPTED_WAITING_APPROVAL = "INTERRUPTED_WAITING_APPROVAL"
    COMPLETED = "COMPLETED"
    REJECTED = "REJECTED"


class HumanInTheLoopExecutor:
    """도구 위험도를 감지하고 중단점을 제어하는 오케스트레이터."""

    def __init__(self):
        self.tool_registry: Dict[str, ToolDefinition] = {}
        self.state = ExecutionState.RUNNING
        self.pending_tool_call: Optional[Dict[str, Any]] = None

    def register_tool(self, name: str, risk_level: ToolRiskLevel, description: str):
        def decorator(func: Callable):
            self.tool_registry[name] = ToolDefinition(name, risk_level, func, description)
            return func
        return decorator

    def request_tool_execution(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        tool_def = self.tool_registry.get(tool_name)
        if not tool_def:
            return {"status": "error", "message": f"도구 '{tool_name}'를 찾을 수 없습니다."}

        print(f"\n[🛠️ 도구 호출 인입] '{tool_name}' (인자: {arguments})")

        if tool_def.risk_level == ToolRiskLevel.SAFE_READ:
            print(f"  🟢 [안전 등급: {tool_def.risk_level.value}] 자동 승인 및 즉시 실행")
            result = tool_def.func(**arguments)
            return {"status": "success", "executed": True, "result": result}

        print(f"  🔴 [위험 등급: {tool_def.risk_level.value}] Side-Effect 감지 -> 즉시 일시 정지 (Interrupt)!")
        self.state = ExecutionState.INTERRUPTED_WAITING_APPROVAL
        self.pending_tool_call = {
            "tool_name": tool_name,
            "arguments": arguments,
            "description": tool_def.description
        }
        return {
            "status": "interrupted",
            "executed": False,
            "message": f"승인 대기 중: 관리자(Human)의 승인이 필요합니다. (도구: {tool_name})"
        }

    def resume_with_approval(self, approved: bool, reason: str = "") -> Dict[str, Any]:
        if self.state != ExecutionState.INTERRUPTED_WAITING_APPROVAL or not self.pending_tool_call:
            return {"status": "error", "message": "대기 중인 중단점(Interrupt)이 없습니다."}

        tool_name = self.pending_tool_call["tool_name"]
        arguments = self.pending_tool_call["arguments"]
        tool_def = self.tool_registry[tool_name]

        if approved:
            print(f"\n✅ [관리자 승인 접수] 사유: '{reason or '정상 작업 승인'}' -> 실행 재개(Resume)...")
            result = tool_def.func(**arguments)
            self.state = ExecutionState.COMPLETED
            self.pending_tool_call = None
            return {"status": "success", "executed": True, "result": result}
        else:
            print(f"\n❌ [관리자 거부 접수] 사유: '{reason}' -> 작업 취소 및 에이전트에 반려 피드백 반환")
            self.state = ExecutionState.REJECTED
            self.pending_tool_call = None
            return {"status": "rejected", "executed": False, "message": f"사용자에 의해 실행이 거부됨: {reason}"}


def main():
    print("=" * 70)
    print("🛑 Module 5: Human-in-the-Loop & Breakpoint Executor")
    print("=" * 70)

    executor = HumanInTheLoopExecutor()

    @executor.register_tool("read_database_schema", ToolRiskLevel.SAFE_READ, "DB 스키마 조회 (안전)")
    def read_schema(table: str):
        return f"Table '{table}': [id INT, email VARCHAR, created_at TIMESTAMP]"

    @executor.register_tool("drop_database_table", ToolRiskLevel.DANGEROUS_WRITE, "DB 테이블 삭제 (매우 위험)")
    def drop_table(table: str):
        return f"CRITICAL: Table '{table}' dropped successfully!"

    print("\n--- [시나리오 1: 안전한 읽기 작업 요청] ---")
    res1 = executor.request_tool_execution("read_database_schema", {"table": "users"})
    print("결과:", res1)

    print("\n--- [시나리오 2: 위험한 쓰기/삭제 작업 요청] ---")
    res2 = executor.request_tool_execution("drop_database_table", {"table": "legacy_logs"})
    print("결과:", res2)

    print("\n--- [시나리오 3: 관리자 승인 대화상자 인터랙션] ---")
    print(f"현재 시스템 상태: {executor.state.value}")
    time.sleep(0.5)
    resume_res = executor.resume_with_approval(approved=True, reason="분기 정기 데이터 정리 작업 확인됨")
    print("재개 실행 결과:", resume_res)

    print("\n" + "=" * 70)
    print("✅ 확인: 파괴적 작업 전 Human-in-the-Loop 중단점을 완벽하게 제어합니다.")
    print("=" * 70)


if __name__ == "__main__":
    main()
