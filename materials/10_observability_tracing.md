# 👁️ Module 10: LLM Observability & Tracing

**LLM Observability (관측 가능성)**는 복잡하게 호전되는 멀티 에이전트 및 도구 호출 루프에서 **어느 단계에서 병목(지연시간)이 발생하는지, 어느 에이전트가 토큰 비용을 폭증시키는지 분산 추적(Tracing)하고 디버깅**하는 필수 운영 메커니즘입니다.

---

## 📊 LLM 관측 가능성의 3대 핵심 메트릭

```text
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│ 1. Latency      │       │ 2. Token Cost   │       │ 3. Error Rate   │
│ (지연시간 ms)    │       │ (입/출력 토큰)  │       │ (도구 실패율)   │
└─────────────────┘       └─────────────────┘       └─────────────────┘
```

1. **Latency (지연시간)**: 각 에이전트 단계별 및 도구(MCP/RAG) 실행에 소요되는 정확한 밀리초(ms) 지연시간 측정.
2. **Token Cost (토큰 사용량)**: 프롬프트 입력 토큰(Input)과 모델 답변 토큰(Output)을 개별 추적하여 비용 계산.
3. **Tool Error Rate (도구 오류율)**: MCP 도구 호출 시 파싱 에러 및 예외 발생 빈도 추적.

---

## 🔍 OpenTelemetry & 분산 추적 (Distributed Tracing)

### Span (스팬)과 Trace (트레이스)의 개념
* **Trace**: 하나의 사용자 요청이 들어왔을 때부터 최종 답변이 나갈 때까지의 **전체 실행 경로 유니버스**.
* **Span**: 그 경로 내부의 **세부 단위 작업** (예: `Prompt Parsing Span`, `RAG Search Span`, `LLM Generation Span`).

```text
Trace: [사용자 질문 -> 최종 응답] (Total: 1200ms, Cost: 450 tokens)
 ├── Span 1: Input Guardrail Check (15ms)
 ├── Span 2: RAG Vector Search (120ms)
 └── Span 3: Gemini 2.5 Flash Generation (1065ms, Input: 350, Output: 100)
```

---

## 🏋️ 실습 예제 따라하기

이 모듈과 연계되는 파이썬 실습 코드 파일은 [examples/observability_example.py](file:///c:/Coding/AI-Engineering/examples/observability_example.py)에 작성되어 있습니다.

### 실습 실행 방법
```bash
python examples/observability_example.py
```

### 코드 주요 포인트
* 멀티 에이전트 호출 및 도구 실행 시 각 단계별 Span 지연시간(ms) 및 토큰 사용량 자동 측정.
* 전체 트레이스 요약 보고서 출력 확인.
