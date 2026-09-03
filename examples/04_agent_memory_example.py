"""Module 4: Agent Memory & State Persistence Example.

Short-term 대화 버퍼(Sliding Window & 요약 압축)와
세션이 변경되어도 유지되는 Long-term Entity Memory(Key-Value 영속화)를 결합한
에이전트 메모리 관리 시스템입니다.
"""

import sys
from typing import Dict, List, Any

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


class AgentMemoryManager:
    """단기 대화 버퍼와 장기 엔티티 메모리를 총괄하는 메모리 매니저."""

    def __init__(self, max_short_term_turns: int = 3):
        self.max_turns = max_short_term_turns
        self.short_term_history: List[Dict[str, str]] = []
        self.conversation_summary: str = ""
        self.entity_memory: Dict[str, Any] = {}

    def update_entity(self, key: str, value: Any):
        """사용자 선호도, 인프라 설정 등 핵심 엔티티를 장기 기억에 저장합니다."""
        self.entity_memory[key] = value

    def get_entity(self, key: str, default: Any = None) -> Any:
        """장기 기억에서 특정 엔티티 속성을 회상합니다."""
        return self.entity_memory.get(key, default)

    def add_message(self, role: str, content: str):
        """새 대화 메시지를 단기 메모리에 기록하고, 한도 초과 시 자동 요약 압축합니다."""
        self.short_term_history.append({"role": role, "content": content})

        if len(self.short_term_history) > self.max_turns * 2:
            oldest_pair = self.short_term_history[:2]
            self.short_term_history = self.short_term_history[2:]
            compaction_note = f"[과거 요약: {oldest_pair[0]['content']} -> {oldest_pair[1]['content'][:30]}...]"
            if self.conversation_summary:
                self.conversation_summary += f" | {compaction_note}"
            else:
                self.conversation_summary = compaction_note

    def assemble_context_window(self, current_prompt: str) -> Dict[str, Any]:
        """LLM에 주입할 완성된 컨텍스트 메모리 페이로드를 빌드합니다."""
        return {
            "entity_long_term_memory": self.entity_memory,
            "condensed_summary": self.conversation_summary or "없음",
            "active_short_term_dialogue": self.short_term_history,
            "current_user_instruction": current_prompt
        }


def main():
    print("=" * 70)
    print("🧠 Module 4: Agent Memory & State Persistence Simulator")
    print("=" * 70)

    memory = AgentMemoryManager(max_short_term_turns=2)

    print("\n[📌 1. Long-term Entity Memory 적재]")
    memory.update_entity("user_name", "김철수")
    memory.update_entity("tech_stack", ["FastAPI", "PostgreSQL", "Docker"])
    memory.update_entity("preferred_language", "Python 3.11")
    print("  • 기억된 엔티티:", memory.entity_memory)

    print("\n[💬 2. 다중 턴 대화 진행 및 슬라이딩 윈도우 요약]")
    turns = [
        ("user", "우리 프로젝트 DB 포트가 몇 번이었지?"),
        ("assistant", "PostgreSQL 기본 포트인 5432번으로 설정되어 있습니다."),
        ("user", "도커 컴포즈 파일에 볼륨 경로 추가해줘."),
        ("assistant", "./data:/var/lib/postgresql/data 볼륨 매핑을 추가했습니다."),
        ("user", "테스트 코드 실행해줘."),
        ("assistant", "pytest tests/ 실행 결과 12개 테스트 모두 통과했습니다.")
    ]

    for role, content in turns:
        memory.add_message(role, content)

    new_query = "지금까지 작업한 내용 바탕으로 배포 스크립트 작성해줘."
    payload = memory.assemble_context_window(new_query)

    print("\n[📦 3. LLM 전송 직전 완성된 메모리 패키지]")
    print(f"  • 장기 엔티티: {payload['entity_long_term_memory']}")
    print(f"  • 압축된 요약: {payload['condensed_summary']}")
    print(f"  • 활성 단기 턴 수: {len(payload['active_short_term_dialogue'])} 개 메시지")
    for msg in payload["active_short_term_dialogue"]:
        print(f"    - [{msg['role']}]: {msg['content']}")
    print(f"  • 현재 질문: {payload['current_user_instruction']}")

    print("\n" + "=" * 70)
    print("✅ 확인: 단기 대화는 슬라이딩 요약되어 토큰 폭증을 방지하고,")
    print("   장기 엔티티는 영속화되어 개인화된 컨텍스트를 완벽하게 유지합니다.")
    print("=" * 70)


if __name__ == "__main__":
    main()
