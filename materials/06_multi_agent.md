# 🤖 Module 6: Multi-Agent Orchestration & StateGraph

단일 LLM에게 모든 복잡한 작업을 한꺼번에 맡기는 구조에서 벗어나, 특화된 전문 에이전트들(Workers)을 상태 그래프(StateGraph)로 결합하고 제어권을 넘기는 **멀티 에이전트 오케스트레이션 (Multi-Agent Orchestration)** 패턴을 학습합니다.

---

## 📐 1. 핵심 멀티 에이전트 아키텍처 패턴

```text
┌─────────────────────────────────────────────────────────────┐
│                 멀티 에이전트 오케스트레이션 패턴              │
├─────────────────┬─────────────────────────┬─────────────────┤
│ 1️⃣ Router        │ 2️⃣ Supervisor-Worker     │ 3️⃣ Handoff Swarm │
│ (조건부 단일분기)│ (중앙 집권형 지휘 조율) │ (자율 제어권 이전)│
│ - Intent 분류   │ - 작업 분담 및 합성     │ - 에이전트간 전이│
│ - if/else 분기  │ - Fan-out & Fan-in      │ - LangGraph DAG │
└─────────────────┴─────────────────────────┴─────────────────┘
```

1. **Router (라우터)**: 사용자 의도(Intent)에 따라 특정 도메인 에이전트(예: 코딩봇, 회계봇)로 단일 라우팅.
2. **Supervisor-Worker (감독자-워커)**: 마스터 에이전트가 서브태스크를 정의하고 여러 워커를 비동기 병렬(`asyncio.gather` / Fan-out) 실행한 뒤 결과를 취합(Fan-in Synthesis).
3. **Handoff / StateGraph (상태 전이망)**: LangGraph 스타일로 공통 `State` 객체를 공유하며 조건부 엣지(Conditional Edge)를 따라 에이전트 간 제어권을 자유롭게 전달.

---

## 🔄 2. StateGraph & Checkpointer 원리

```text
               ┌───────────────────────┐
               │     Start Node        │
               └───────────┬───────────┘
                           │
                           ▼
               ┌───────────────────────┐
               │    Planner Agent      │ ◄────┐ (재기획 루프)
               └───────────┬───────────┘      │
                           │                  │
                           ▼                  │
               ┌───────────────────────┐      │
               │    Executor Agent     │      │
               └───────────┬───────────┘      │
                           │                  │
                           ▼                  │
               ┌───────────────────────┐      │
               │    Validator Agent    │ ─────┘ (반려 시 재시도)
               └───────────┬───────────┘
                           │ (통과 시)
                           ▼
               ┌───────────────────────┐
               │       End Node        │
               └───────────────────────┘
```

---

## 🏋️ 실습 예제 따라하기

이 모듈과 연계되는 파이썬 실습 코드 파일은 [examples/orchestrator/orchestrator.py](file:///c:/Coding/AI-Engineering/examples/orchestrator/orchestrator.py)에 작성되어 있습니다.

```bash
python examples/orchestrator/orchestrator.py
```
