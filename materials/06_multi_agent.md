# 🤖 Module 6: Multi-Agent Orchestration & StateGraph

단일 LLM에게 모든 복잡한 작업을 한꺼번에 맡기는 구조에서 벗어나, 특화된 전문 에이전트들(Workers)을 상태 그래프(StateGraph)로 결합하고 제어권을 넘기는 **멀티 에이전트 오케스트레이션 (Multi-Agent Orchestration)** 패턴을 학습합니다.

---

## 📐 1. 핵심 멀티 에이전트 아키텍처 패턴

이 3대 패턴은 앤트로픽(Anthropic)의 연구 보고서 *"Building Effective Agents"*와 OpenAI의 *Swarm*, 그리고 *LangGraph*가 정립한 **현재 AI 업계에서 가장 지배적이고 널리 쓰이는 최신 표준 멀티 에이전트 아키텍처**입니다.

```text
┌─────────────────────────────────────────────────────────────────────────┐
│                      3대 핵심 멀티 에이전트 아키텍처                      │
├────────────────────┬────────────────────────────┬───────────────────────┤
│ 1️⃣ Router          │ 2️⃣ Supervisor-Worker        │ 3️⃣ Handoff Swarm      │
│ (조건부 단일 분기)  │ (중앙 집권형 지휘 및 합성) │ (탈중앙 자율 바통터치)│
├────────────────────┼────────────────────────────┼───────────────────────┤
│ • 1층 안내 데스크  │ • 영화 감독과 스태프들     │ • 릴레이 이어달리기   │
│ • Intent 분류 1:1  │ • Fan-out 병렬 & Fan-in    │ • transfer_to_agent() │
│ • 저비용, 초고속   │ • 복잡한 대형 작업 총괄    │ • 유연한 상태 전이    │
└────────────────────┴────────────────────────────┴───────────────────────┘
```

---

### 1️⃣ Router (조건부 단일 분기 패턴)
* **현실 비유**: 종합병원 1층의 **"안내 데스크 접수처"**
* **작동 원리**:
  1. 가장 저렴하고 빠른 경량 모델(Gemini Flash, GPT-4o-mini)이 사용자의 질문 의도(Intent)를 0.1초 만에 분류합니다.
  2. 분류된 결과에 따라 딱 하나의 전문 에이전트에게 작업을 직배송(Dispatch)합니다.
  3. `[사용자 질문]` ──► `[Router]` ──► `(코딩 질문? ➔ 코딩봇)` / `(환불 질문? ➔ 고객지원봇)`
* **장점**:
  * 불필요한 에이전트를 깨우지 않으므로 **토큰 비용과 응답 지연시간(Latency)이 가장 적습니다.**
* **적합한 작업**: 고객센터 FAQ 분류, 단순 도메인별 1:1 라우팅.

---

### 2️⃣ Supervisor-Worker (중앙 집권형 지휘 및 합성 패턴)
* **현실 비유**: **"영화 감독(Supervisor)과 각 분야 전문 스태프(Workers)"**
* **작동 원리**:
  1. 중앙의 **감독관(Supervisor / Orchestrator)** 에이전트가 복잡한 사용자의 명령을 받습니다.
  2. 작업을 작은 단위로 쪼갠 뒤(Planning), 전문 워커들에게 비동기 병렬로 일감을 뿌립니다 (**Fan-out**).
     * `Worker A (리서처)`: 최신 기술 동향 검색
     * `Worker B (개발자)`: 관련 핵심 소스 코드 작성
     * `Worker C (보안관)`: 작성된 코드의 취약점 검사
  3. 모든 워커의 결과가 나오면, 감독관이 이를 하나의 완벽한 최종 보고서로 종합(**Fan-in Synthesis**)하여 사용자에게 전달합니다.
* **장점**:
  * 병렬 처리(`asyncio.gather`)로 작업 시간을 대폭 단축하며, 중앙 감독관이 전체 품질을 엄격히 통제할 수 있습니다.
* **적합한 작업**: 대규모 시장 조사 보고서 작성, 풀스택 앱 개발(기획+디자인+코딩+테스트).

---

### 3️⃣ Handoff / Swarm (탈중앙 자율 바통터치 패턴)
* **현실 비유**: **"릴레이 이어달리기"** 또는 **"전문 상담사 간 전화 호 전환"**
* **작동 원리**:
  1. 중앙의 보스(감독관)가 따로 존재하지 않습니다.
  2. 에이전트들이 공통의 대화 상태(`State`)를 공유하며, 각 에이전트가 **"내 역할이 끝났으니 다음 사람에게 제어권을 넘긴다"**는 도구(`transfer_to_xxx_agent`)를 스스로 호출합니다.
  3. `[접수 에이전트]` ──(전화 호 전환)──► `[환불 에이전트]` ──(승인 완료 후)──► `[배송 에이전트]`
* **장점**:
  * 중앙 오케스트레이터의 병목 없이, 에이전트들이 상황에 따라 유연하게 제어권을 주고받는 **분산형 네트워크**를 형성합니다 (OpenAI Swarm 및 LangGraph의 핵심 아키텍처).
* **적합한 작업**: 다단계 비즈니스 프로세스(예약 ➔ 결제 ➔ 알림 발송), 대화형 자율 트러블슈팅.

---

## 🔄 2. StateGraph & Checkpointer 원리

현대 멀티 에이전트 시스템(특히 **LangGraph**)은 에이전트들을 단순한 함수 호출이 아닌, **"상태 그래프(StateGraph)"**라는 정교한 상태 머신으로 조율합니다.

```text
               ┌───────────────────────┐
               │     Start Node        │ ──► [1] 사용자 요구사항 인입
               └───────────┬───────────┘
                           │
                           ▼
               ┌───────────────────────┐
               │    Planner Agent      │ ◄────┐ [5] 반려 시: 에러 피드백을 들고
               └───────────┬───────────┘      │     기획안 재작성 루프
                           │                  │
                           ▼ [2] 세부 태스크  │
               ┌───────────────────────┐      │
               │    Executor Agent     │      │
               └───────────┬───────────┘      │
                           │                  │
                           ▼ [3] 결과물 제출  │
               ┌───────────────────────┐      │
               │    Validator Agent    │ ─────┘ [4] 조건부 엣지(Conditional Edge):
               └───────────┬───────────┘            "기준 미달 시 반려, 통과 시 종료"
                           │ (통과 시)
                           ▼
               ┌───────────────────────┐
               │       End Node        │ ──► [6] 최종 결과 사용자 전달
               └───────────────────────┘
```

---

### 1️⃣ State (공유 상태 객체 - "공용 작업 칠판")
* 멀티 에이전트들이 귓속말로 대화하는 것이 아니라, 중앙에 놓인 **"공용 화이트보드(TypedDict 또는 Pydantic 객체)"**에 각자 작업한 내용을 적고 공유합니다.
```python
# 에이전트들이 공유하는 State 데이터 구조 예시
class AgentState(TypedDict):
    user_request: str        # 사용자의 원본 질문
    plan: List[str]          # Planner가 수립한 단계별 계획
    generated_code: str      # Executor가 작성한 코드
    review_feedback: str     # Validator가 지적한 문제점
    is_approved: bool        # 최종 검증 통과 여부
```
1. **Planner**: `user_request`를 읽고 `plan`에 계획을 적습니다.
2. **Executor**: `plan`을 보고 코드를 짜서 `generated_code`를 채웁니다.
3. **Validator**: `generated_code`를 테스트해보고 `is_approved`를 `True` 또는 `False`로 변경합니다.

---

### 2️⃣ Conditional Edge (조건부 엣지 - "갈림길 분기 판단")
그래프의 화살표(Edge) 중에는 결과에 따라 경로가 동적으로 바뀌는 **조건부 엣지**가 있습니다:
* Validator 노드가 끝났을 때 파이썬 함수가 상태를 검사합니다:
  ```python
  def route_after_validation(state: AgentState):
      if state["is_approved"]:
          return "End Node"        # 합격이면 완료 노드로 이동
      else:
          return "Planner Agent"   # 불합격이면 기획자에게 반려(Feedback Loop)
  ```
* 이 구조 덕분에 사람이 개입하지 않아도 **완벽한 품질이 나올 때까지 에이전트들끼리 "작성 ➔ 검사 ➔ 반려 ➔ 재작성"의 자체 피드백 루프**를 무한히 돌릴 수 있습니다.

---

### 3️⃣ Checkpointer (체크포인터 - "게임의 자동 세이브 포인트")
실무 대규모 엔터프라이즈 환경에서 StateGraph의 가장 강력한 무기는 바로 **체크포인터(Checkpointer)**입니다.

* **개념**: 에이전트가 각 노드(Planner, Executor 등)를 통과할 때마다, 그 순간의 전체 State 스냅샷을 **SQLite나 PostgreSQL 데이터베이스에 자동으로 세이브(Save)**합니다.
* **왜 필수적일까요? (실무 3대 효용)**:
  1. **장애 내결함성 (Fault Tolerance)**:
     * 3번째 단계(Executor)에서 네트워크가 끊기거나 LLM API 타임아웃이 발생해도, **처음부터 다시 시작할 필요 없이 마지막 저장된 체크포인트에서 즉시 재개(Resume)**할 수 있습니다 (비용/시간 절약).
  2. **시간 여행 디버깅 (Time Travel)**:
     * 10단계까지 실행된 작업 중 4번째 단계로 시간을 되돌려(Rollback), 다른 프롬프트나 다른 파라미터를 넣었을 때의 분기 결과를 테스트해볼 수 있습니다.
  3. **Human-in-the-Loop 결합 (일시 정지 & 재개)**:
     * 사람의 승인이 필요할 때 서버 메모리에 에이전트 프로세스를 계속 띄워둘 필요 없이, **상태를 DB에 얼려두고(Freeze) 서버를 종료**합니다.
     * 3일 뒤 관리자가 웹 브라우저에서 '승인' 버튼을 누르면, 체크포인터가 DB에서 당시 기억을 고스란히 복원해 다음 노드로 이어갑니다.

---

## 🛠️ 3. 실전: Antigravity IDE 에이전트 정의 및 오케스트레이션 실행

Antigravity IDE에서는 단일 대화창 안에서도 워크스페이스 내 **`.agents/agents/` 디렉토리에 각 분야별 전문 에이전트를 선언**하여, 최신 AI 엔지니어링 프로젝트를 자율적으로 분담하고 지휘할 수 있습니다.

### 1) 3대 최신 트렌드 전담 에이전트 스펙 (`.agents/agents/`)

우리는 **"최신 AI 엔지니어링 트렌드(GraphRAG, Event-Driven, Observability) 심층 리서치 및 아키텍처 수립"**을 위해 3마리의 전문 에이전트를 정의했습니다.

```text
c:\Coding\AI-Engineering\.agents\agents\
  ├── trend-researcher.json  <-- 1. 최신 AI 트렌드/논문 웹 심층 조사관
  ├── tech-architect.json    <-- 2. 엔터프라이즈 솔루션 설계 및 코드 작성관
  └── audit-reviewer.json    <-- 3. 보안/관측성 결함 심사 및 반려/승인 감사관
```

* **[TrendResearcherAgent](file:///c:/Coding/AI-Engineering/.agents/agents/trend-researcher.json)**:
  * **역할**: GraphRAG, Event-Driven Streaming, Test-Time Compute 등 최신 아키텍처 기술 명세 수집.
  * **도구 격리(최소 권한)**: `search_web`, `read_url_content`, `view_file` (파일 쓰기나 터미널 권한 없음).
* **[TechArchitectAgent](file:///c:/Coding/AI-Engineering/.agents/agents/tech-architect.json)**:
  * **역할**: 수집된 트렌드를 바탕으로 실제 동작하는 파이썬 StateGraph 및 다이어그램 설계.
  * **도구 격리**: `write_to_file`, `replace_file_content` (웹 서핑 도구 제외로 집중도 극대화).
* **[AuditReviewerAgent](file:///c:/Coding/AI-Engineering/.agents/agents/audit-reviewer.json)**:
  * **역할**: 작성된 결과물을 비판적으로 감사하여, OpenTelemetry 분산 추적 누락 시 3점 이하로 엄격히 반려.
  * **도구 격리**: `run_command`, `view_file` (코드 실행 및 검증 전담).

---

### 2) IDE 환경에서의 실전 오케스트레이션 실행 (How to Run)

사용자가 IDE 대화창에서 복합 지시를 내리면, IDE 오케스트레이터(Supervisor)가 백그라운드에서 이 에이전트들을 순차적/병렬로 지휘합니다:

```text
[사용자 명령 인입]
"최신 AI 엔지니어링 트렌드를 조사하고, 이를 반영한 엔터프라이즈 파이프라인 백서를 작성해줘."
      │
      ▼
1️⃣ [TrendResearcherAgent 출동]
   • 웹 검색 도구로 2025~2026 GraphRAG, OTel, Test-Time Scaling 최신 스펙 크롤링
   • 10줄 핵심 팩트 리포트를 공유 State 칠판에 기록
      │
      ▼
2️⃣ [TechArchitectAgent 바통터치 (Handoff)]
   • 리서치 리포트를 이어받아 [examples/06_orchestrator.py] 실전 아키텍처 및 파이썬 파이프라인 작성
      │
      ▼
3️⃣ [AuditReviewerAgent 엄격 감사 (Review)]
   • 터미널에서 코드를 돌려보고 OpenTelemetry 누락 발견 ──► 3점 부여 후 2번 아키텍트에게 반려!
   • 2번 아키텍트가 피드백을 반영해 재수정 ──► 5점 만점 획득 후 최종 완료 보고!
```

---

## 🏋️ 실습 예제 따라하기

이 모듈과 연계되는 파이썬 실습 코드 파일은 [examples/06_orchestrator.py](file:///c:/Coding/AI-Engineering/examples/06_orchestrator.py)에 작성되어 있습니다.

```bash
python examples/06_orchestrator.py
```
