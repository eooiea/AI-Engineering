# 🧠 Module 4: Agent Memory & State Persistence

실무 프로덕션 AI 에이전트는 일회성 질의응답을 넘어, **세션 내 대화 흐름(Short-term Memory)**과 **세션 간 사용자 프로필 및 과거 작업 히스토리(Long-term / Entity Memory)**를 영속적으로 기억하고 관리해야 합니다.

---

## 🏛️ 1. 에이전트 메모리의 3대 계층 구조

```text
┌─────────────────────────────────────────────────────────────┐
│                     에이전트 메모리 시스템                   │
├─────────────────┬─────────────────────────┬─────────────────┤
│ 1️⃣ Short-term    │ 2️⃣ Long-term            │ 3️⃣ Entity Memory │
│ (세션 내 단기)  │ (세션 간 영속 저장)     │ (사용자/엔티티) │
│ - Sliding Window│ - Vector / DB 저장소    │ - 이름, 선호도, │
│ - Token Summary │ - 과거 작업 결과 회상   │   인프라 설정   │
└─────────────────┴─────────────────────────┴─────────────────┘
```

1. **Short-term Memory (단기 기억)**: 현재 활성 대화 세션의 메시지 버퍼. 토큰 한도를 초과하지 않도록 **Sliding Window(최근 N개 턴 유지)** 또는 **중간 요약(Summarizer)**을 적용합니다.
2. **Long-term Memory (장기 기억)**: 과거 세션에서 해결했던 문제, 프로젝트 히스토리, 코드 조각 등을 Vector DB나 SQLite에 저장하고 필요 시 유사도 검색으로 호출합니다.
3. **Entity Memory (엔티티 기억)**: 대화 속에서 특정 사용자(User), 프로젝트(Repository), 인프라 서버의 고유 속성(예: "사용자는 Python 3.11 환경을 선호함", "DB 포트는 5432")을 Key-Value 형태로 추출하여 고정 기억합니다.

---

## ⚙️ 2. 메모리 수명 주기 (Lifecycle)

```text
[사용자 입력] ──► [1. Memory Retrieve] ──► [2. LLM Reasoning] ──► [3. Memory Update]
                    (단기/장기 메모리 주입)      (결과 도출)          (엔티티 추출 & 저장)
```

1. **Retrieve (회상)**: 사용자의 질문이 들어오면 연관된 단기 대화 이력과 장기 엔티티 정보를 프롬프트에 합성.
2. **Reasoning (추론)**: 주입된 기억을 바탕으로 맞춤형 답변 또는 도구 실행.
3. **Update & Consolidate (압축 및 저장)**: 대화 종료 시 중요한 엔티티나 핵심 지식을 추출하여 영속 저장소에 동기화.

---

## 🏋️ 실습 예제 따라하기

이 모듈과 연계되는 파이썬 실습 코드 파일은 [examples/04_agent_memory_example.py](file:///c:/Coding/AI-Engineering/examples/04_agent_memory_example.py)에 작성되어 있습니다.

```bash
python examples/04_agent_memory_example.py
```

### 핵심 실습 포인트
* Sliding Window 기반의 단기 대화 버퍼 관리 및 초과 시 자동 요약(Compaction).
* 세션이 변경되어도 유지되는 Key-Value 기반 Entity Memory 저장 및 자동 회상.
