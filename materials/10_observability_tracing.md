# 👁️ Module 10: OpenTelemetry LLM Observability & Tracing

**LLM Observability (관측 가능성)**는 복잡하게 얽힌 멀티 에이전트, RAG 검색, 도구 호출 파이프라인에서 **어느 단계에서 병목(지연시간)이 발생하는지, 어느 에이전트가 토큰 비용을 폭증시키는지 분산 추적(Distributed Tracing)하고 디버깅**하는 필수 운영 인프라입니다.

---

## 📊 1. OpenTelemetry 표준과 3대 핵심 메트릭

```text
┌─────────────────────────────────────────────────────────────┐
│                 LLM 관측 가능성 3대 핵심 메트릭               │
├─────────────────┬─────────────────────────┬─────────────────┤
│ 1️⃣ Latency       │ 2️⃣ Token Cost           │ 3️⃣ Tool Errors   │
│ (지연시간 ms)   │ (입/출력 토큰 및 비용)  │ (도구 호출 실패)│
│ - TTFT 측정     │ - Prompt/Completion     │ - Schema 파싱 에러│
│ - 병목 단계 식별│ - 에이전트별 비용 기여도│ - Fallback 빈도 │
└─────────────────┴─────────────────────────┴─────────────────┘
```

---

## 🔍 2. Trace (트레이스)와 Span (스팬)의 계층 구조

* **Trace**: 사용자 요청 시작부터 최종 답변 반환까지의 전체 실행 흐름.
* **Span**: 그 하위의 개별 실행 단위 (예: Guardrail Span, RAG Retrieval Span, LLM Generation Span, Tool Call Span).

```text
Trace: [user_query -> final_response] (Total: 1420ms | Cost: $0.0012)
 ├── Span 1: Input Guardrail Check (15ms)
 ├── Span 2: Hybrid RAG Search (125ms)
 │    ├── Child Span: BM25 Sparse Search (20ms)
 │    └── Child Span: Dense Vector Search (105ms)
 ├── Span 3: LLM Generation (1250ms, Prompt Tok: 450, Comp Tok: 120)
 └── Span 4: Output PII Masking (30ms)
```

---

## 🏋️ 실습 예제 따라하기

이 모듈과 연계되는 파이썬 실습 코드 파일은 [examples/10_observability_example.py](file:///c:/Coding/AI-Engineering/examples/10_observability_example.py)에 작성되어 있습니다.

```bash
python examples/10_observability_example.py
```
