# 🤖 Module 4: Multi-Agent Orchestration (멀티 에이전트 오케스트레이션)

하나의 거대한 LLM에게 복잡하고 긴 미션을 한 번에 던져주면 컨텍스트 오류, 환각(Hallucination), 비합리적인 로직 설계 등의 한계에 부딪히기 쉽습니다. 

이러한 문제를 극복하기 위해 제안된 것이 바로 **멀티 에이전트 오케스트레이션 (Multi-Agent Orchestration)** 입니다. 큰 문제를 논리적이고 작은 단위로 쪼개어 각각 특화된 에이전트들(Workers)에게 분담시키고, 이를 총괄하는 지휘자(Master/Orchestrator)가 최종 결과물을 취합 및 정제하는 방식입니다.

---

## 📐 핵심 오케스트레이션 디자인 패턴

AI 엔지니어링 업계에서 널리 활용되는 대표적인 에이전트 조율 패턴은 다음과 같습니다.

### 1. 라우터 (Router) 패턴
*   사용자의 질문이나 요구사항에 따라 가장 적합한 전담 에이전트나 도구(Tool)로 흐름을 분기합니다.
*   예: "결제 오류 문의" -> 결제 전담 봇 호출 / "서버 장애 제보" -> 인프라 모니터링 봇 호출.

### 2. 오케스트레이터-워커 (Orchestrator-Workers) 패턴
*   마스터 에이전트가 입력된 미션을 바탕으로 여러 개의 하위 작업을 정의합니다.
*   하위 에이전트들(Workers)은 자신에게 할당된 독립적인 영역을 구현하거나 조사합니다.
*   마스터는 이들의 산출물을 모아 일관성 있는 최종 결과로 합성(Synthesis)합니다.
*   이 교육 과정의 실습인 [orchestrator.py](file:///c:/Coding/AI-Engineering/examples/orchestrator/orchestrator.py)가 이 패턴을 재현합니다.

### 3. 플래너-실행기 (Planner-Executor) 패턴
*   먼저 전체 작업을 수행할 논리적 단계들의 '계획(Plan)'을 세웁니다.
*   실행기(Executor)가 순차적으로 단계를 수행하며, 수행 중 에러나 피드백을 받으면 플래너가 실시간으로 계획을 수정(Replanning)하며 진행합니다.
*   Antigravity IDE의 `Planning Mode`가 이 패턴의 훌륭한 예시입니다.

```
                  ┌───────────────────────┐
                  │    User Requirement   │
                  └───────────┬───────────┘
                              │
                              ▼
                  ┌───────────────────────┐
                  │ Orchestrator (Master) │
                  └──────┬─────────┬──────┘
                         │         │
            ┌────────────┘         └────────────┐
            ▼                                   ▼
┌───────────────────────┐           ┌───────────────────────┐
│     Worker Agent 1    │           │     Worker Agent 2    │
│   (Outline Designer)  │           │   (Content Developer) │
└───────────┬───────────┘           └───────────┬───────────┘
            │                                   │
            └────────────┐         ┌────────────┘
                         ▼         ▼
                  ┌───────────────────────┐
                  │      Synthesizer      │
                  └───────────────────────┘
```

---

## 🛠️ 에이전트 오케스트레이션 프레임워크 트렌드

실제 상용 시스템을 구현할 때는 다음과 같은 파이썬 라이브러리들을 주로 채택합니다.

*   **LangGraph (LangChain 생태계)**: 상태 전이(State), 순환 사이클(Cycles) 및 조건부 라우팅을 그래프 구조(DAG)로 완벽하게 제어할 수 있어 엔터프라이즈 환경에서 가장 널리 쓰입니다.
*   **CrewAI**: 역할(Role), 목표(Goal), 백스토리(Backstory)를 지닌 에이전트들이 크루(Crew)로 뭉쳐 협업하는 에이전트 중심의 고수준 프레임워크입니다.
*   **AutoGen (Microsoft)**: 대화 중심의 에이전트 프레임워크로, 에이전트 간의 자유로운 협업 및 채팅 기반의 토론 과정을 자동화하기 용이합니다.

---

## 🏋️ 실습 예제 따라하기

이 모듈과 연계되는 실습 파일은 [examples/orchestrator/orchestrator.py](file:///c:/Coding/AI-Engineering/examples/orchestrator/orchestrator.py)에 생성되어 있습니다.

### 실습 절차
1. [examples/orchestrator/orchestrator.py](file:///c:/Coding/AI-Engineering/examples/orchestrator/orchestrator.py)를 열어 전체적인 코드를 파악합니다.
2. 이 스크립트는 `Gemini` API 키 없이도 실행 흐름을 쉽게 파악할 수 있도록 모의(Mock) 에이전트 호출 루프를 포함하고 있습니다.
3. 터미널 창을 열고 `python examples/orchestrator/orchestrator.py` 명령을 실행하여 마스터 에이전트가 기획 에이전트와 작성 에이전트를 차례대로 소환하고 일련의 보고서를 오케스트레이션하여 산출하는 시뮬레이션을 눈으로 확인해 봅니다.
