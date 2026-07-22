# 🚀 Antigravity와 함께하는 AI 엔지니어링 마스터 클래스

본 교육 과정은 **Antigravity IDE** 환경에서 최근 AI 엔지니어링의 핵심 트렌드인 **Model Context Protocol (MCP)**, **LinkedIn 소셜 외부 연동**, **커스텀 에이전트 스킬**, **멀티 에이전트 오케스트레이션**, **평가 하네스(Evaluation Harness)**, **Antigravity SDK**, **로컬 LLM (Ollama) 멀티 에이전트 협업**, **RAG (검색 증강 생성)**, **Guardrails (보안)**, 그리고 **Observability (관측 가능성 및 추적)**를 실습하며 마스터할 수 있도록 설계된 종합 커리큘럼입니다.

이 워크스페이스는 학습 자료와 이론, 그리고 바로 실행하고 테스트해 볼 수 있는 파이썬 코드 예제들로 구성되어 있습니다.

---

## 📅 커리큘럼 로드맵

```mermaid
graph TD
    M0[0. AI IDE Architecture & Context Eng] --> M1[1. Model Context Protocol]
    M1 --> M2[2. Advanced MCP: LinkedIn API]
    M2 --> M3[3. Customization & Slash Commands]
    M3 --> M4[4. Multi-Agent Orchestration]
    M4 --> M5[5. Evaluation & Harness]
    M5 --> M6[6. Antigravity SDK Mastery]
    M6 --> M7[7. Ollama Local Agent]
    M7 --> M8[8. RAG & Vector DB Pipeline]
    M8 --> M9[9. Guardrails & AI Security]
    M9 --> M10[10. LLM Observability & Tracing]
    
    style M0 fill:#ffd,stroke:#333,stroke-width:2px
    style M1 fill:#f9f,stroke:#333,stroke-width:2px
    style M2 fill:#bbf,stroke:#333,stroke-width:2px
    style M3 fill:#bfb,stroke:#333,stroke-width:2px
    style M4 fill:#fbb,stroke:#333,stroke-width:2px
    style M5 fill:#fdd,stroke:#333,stroke-width:2px
    style M6 fill:#dfd,stroke:#333,stroke-width:2px
    style M7 fill:#ddf,stroke:#333,stroke-width:2px
    style M8 fill:#fdf,stroke:#333,stroke-width:2px
    style M9 fill:#ffd,stroke:#333,stroke-width:2px
    style M10 fill:#dff,stroke:#333,stroke-width:2px
```

### [Module 0: AI IDE Architecture & Context Engineering](file:///c:/Coding/AI-Engineering/materials/00_context_engineering.md)
*   **이론**: AI IDE의 3대 구동 객체(Host, Model, Execution Layer), Context Window 한계(Lost in the Middle), 5대 컨텍스트 페이로드 및 `scripts/` 정적 파서의 토큰 다이어프트 원리 이해.
*   **실습**: 5대 페이로드 조립 및 `scripts/` 헬퍼 스크립트를 통한 80% 토큰 절감 효과를 직접 측정하는 [context_engineering_example.py](file:///c:/Coding/AI-Engineering/examples/context_engineering_example.py) 구동.

### [Module 1: Model Context Protocol (MCP)](file:///c:/Coding/AI-Engineering/materials/01_mcp.md)
*   **이론**: AI 모델이 외부 도구, 데이터베이스, API 등과 소통하는 오픈 표준 프로토콜(MCP)의 개념과 아키텍처(Host vs. Server) 이해.
*   **실습**: Python `fastmcp` 패키지를 사용해 간단한 시스템 성능 메트릭 및 날씨 정보를 제공하는 [mcp_server.py](file:///c:/Coding/AI-Engineering/examples/mcp_server.py) 개발 및 호스트 등록 실습.

### [Module 2: Advanced MCP - LinkedIn & External API Integration](file:///c:/Coding/AI-Engineering/materials/02_mcp_linkedin.md)
*   **이론**: MCP 프로토콜을 외부 상용 SNS 플랫폼(LinkedIn REST API / OAuth 2.0)과 연동하는 고급 도구 호출 시퀀스 및 토큰 보안 수칙 이해.
*   **실습**: 에이전트 소식글을 LinkedIn ugcPosts REST API JSON 페이로드로 변환하고 게재하는 [linkedin_mcp_example.py](file:///c:/Coding/AI-Engineering/examples/linkedin_mcp_example.py) 시뮬레이션 가동.

### [Module 3: Customization System & Slash Commands](file:///c:/Coding/AI-Engineering/materials/03_skills.md)
*   **이론**: 에이전트의 상시 전역 규칙(`AGENTS.md`), 동적 커스텀 스킬(`SKILL.md`), 그리고 4대 생산성 슬래시 명령어(`/goal`, `/schedule`, `/grill-me`, `/learn`)를 활용한 완벽한 에이전트 행동 통제 구조 이해.
*   **실습**: 프로젝트 전역 규칙 파일([.agents/AGENTS.md](file:///c:/Coding/AI-Engineering/.agents/AGENTS.md)) 작성, 코드 리뷰어 스킬([SKILL.md](file:///c:/Coding/AI-Engineering/.agents/skills/review-code/SKILL.md)) 및 커밋 스킬([commit-msg/SKILL.md](file:///c:/Coding/AI-Engineering/.agents/skills/commit-msg/SKILL.md)) 연동.

### [Module 4: Multi-Agent Orchestration](file:///c:/Coding/AI-Engineering/materials/04_orchestration.md)
*   **이론**: 복잡한 소프트웨어 문제를 해결하기 위해 여러 하위 에이전트를 생성, 라우팅, 오케스트레이션하는 주류 아키텍처 패턴.
*   **실습**: Master 에이전트가 Outline 에이전트와 Content 작성 에이전트를 소환해 글을 연계 작성하도록 조율하는 [orchestrator.py](file:///c:/Coding/AI-Engineering/examples/orchestrator/orchestrator.py) 구현.

### [Module 5: Evaluation & Harness](file:///c:/Coding/AI-Engineering/materials/05_harness.md)
*   **이론**: AI 애플리케이션의 신뢰성을 담보하기 위한 정량 평가, 프롬프트 회귀 테스트 및 LLM-as-a-Judge 개요.
*   **실습**: 어설션 검증 기법을 구현하여 프롬프트 결과물들의 응답 품질을 등급별로 자동 평가하는 [eval_harness.py](file:///c:/Coding/AI-Engineering/examples/harness/eval_harness.py) 구동.

### [Module 6: Antigravity SDK Mastery](file:///c:/Coding/AI-Engineering/materials/06_antigravity_sdk.md)
*   **이론**: Antigravity 2.0 플랫폼의 백엔드 실행 런타임을 Python 코드로 직접 호출하여 자동화 에이전트 루프를 구현하는 방법.
*   **실습**: `google-antigravity` 라이브러리를 이용하여 로컬 파일을 읽고 분석하여 작업을 처리하는 자율 에이전트 스크립트 [sdk_agent.py](file:///c:/Coding/AI-Engineering/examples/sdk_agent.py) 작성 및 검증.

### [Module 7: Ollama Local Agent Collaboration](file:///c:/Coding/AI-Engineering/materials/07_ollama_orchestration.md)
*   **이론**: 로컬 LLM 환경(Ollama)에 탑재된 `qwen2.5-coder` 모델을 사용하여 코드 빌더(Coder)와 검증기(Validator) 간의 피드백 기반 협업 조율 설계.
*   **실습**: 공식 `ollama` SDK를 기반으로 두 에이전트가 코딩 과제를 완성하기 위해 상호 작용하는 [ollama_orchestrator.py](file:///c:/Coding/AI-Engineering/examples/ollama_orchestrator.py) 예제 실행.

### [Module 8: RAG & Vector DB Pipeline](file:///c:/Coding/AI-Engineering/materials/08_rag_vector_db.md)
*   **이론**: 청킹(Chunking), 임베딩 벡터 코사인 유사도 검색, 하이브리드 검색(Dense+Sparse) 및 Cross-Encoder Re-ranking 원리 이해.
*   **실습**: 메모리 기반 벡터 스토어를 구축하여 쿼리 검색 및 근거 기반 합성 응답을 생성하는 [rag_example.py](file:///c:/Coding/AI-Engineering/examples/rag_example.py) 테스트.

### [Module 9: Guardrails & AI Security](file:///c:/Coding/AI-Engineering/materials/09_guardrails_security.md)
*   **이론**: Prompt Injection / Jailbreak 탈옥 방어, 개인정보(PII) 자동 마스킹 및 입출력 가드레일 통제 레이어 이해.
*   **실습**: 악의적 프롬프트를 필터링하고 전화번호/이메일을 마스킹하는 안전한 필터 파이프라인 [guardrails_example.py](file:///c:/Coding/AI-Engineering/examples/guardrails_example.py) 구동.

### [Module 10: LLM Observability & Tracing](file:///c:/Coding/AI-Engineering/materials/10_observability_tracing.md)
*   **이론**: OpenTelemetry 표준 기반의 분산 추적(Distributed Tracing), Span/Trace 계층 구조, 지연시간(Latency ms) 및 토큰 사용량(Cost) 모니터링 이해.
*   **실습**: 멀티 에이전트 및 도구 실행 단계별 지연시간과 입력/출력 토큰 카운트를 자동 집계하는 [observability_example.py](file:///c:/Coding/AI-Engineering/examples/observability_example.py) 구동.

---

## 📂 폴더 구조 안내

```
c:\Coding\AI-Engineering\
├── curriculum.md                <-- 현재 문서 (Syllabus)
├── materials/                   <-- 상세 이론 학습 교재 폴더 (Module 0~10)
│   ├── 00_context_engineering.md
│   ├── 01_mcp.md
│   ├── 02_mcp_linkedin.md       <-- Advanced MCP (LinkedIn 연동)
│   ├── 03_skills.md
│   ├── 04_orchestration.md
│   ├── 05_harness.md
│   ├── 06_antigravity_sdk.md
│   ├── 07_ollama_orchestration.md
│   ├── 08_rag_vector_db.md
│   ├── 09_guardrails_security.md
│   └── 10_observability_tracing.md
├── examples/                    <-- 직접 돌려보는 실습 파이썬 코드
│   ├── context_engineering_example.py <-- Module 0: 토큰 다이어트 시뮬레이터
│   ├── mcp_server.py
│   ├── linkedin_mcp_example.py   <-- LinkedIn MCP 시뮬레이터
│   ├── sdk_agent.py
│   ├── ollama_orchestrator.py
│   ├── rag_example.py
│   ├── guardrails_example.py
│   ├── observability_example.py
│   ├── orchestrator/
│   │   └── orchestrator.py
│   └── harness/
│       └── eval_harness.py
└── .agents/
    ├── AGENTS.md                <-- 상시 전역 규칙
    └── skills/
        ├── review-code/         <-- 코드 리뷰 커스텀 스킬
        └── commit-msg/          <-- 커밋 메시지 커스텀 스킬
```
