"""Module 10: OpenTelemetry LLM Observability & Tracing Example.

OpenTelemetry 표준 분산 추적(Distributed Tracing) 구조를 적용하여
각 에이전트 단계별 Span 지연시간(Latency ms)과 토큰 사용량/비용을 측정하는 예제입니다.
"""

import dataclasses
import sys
import time
import uuid
from typing import List, Dict, Any, Optional

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


@dataclasses.dataclass
class Span:
    name: str
    span_id: str
    parent_id: Optional[str]
    duration_ms: float
    input_tokens: int
    output_tokens: int
    attributes: Dict[str, Any]


class LLMTracer:
    """OpenTelemetry 스타일의 트레이서."""

    def __init__(self, trace_name: str):
        self.trace_id = str(uuid.uuid4())[:8]
        self.trace_name = trace_name
        self.spans: List[Span] = []

    def record_span(
        self,
        name: str,
        duration_ms: float,
        input_tokens: int = 0,
        output_tokens: int = 0,
        parent_id: Optional[str] = None,
        attributes: Optional[Dict[str, Any]] = None
    ) -> str:
        span_id = str(uuid.uuid4())[:6]
        span = Span(
            name=name,
            span_id=span_id,
            parent_id=parent_id,
            duration_ms=duration_ms,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            attributes=attributes or {}
        )
        self.spans.append(span)
        return span_id

    def generate_report(self, price_per_1k_input: float = 0.0015, price_per_1k_output: float = 0.002) -> Dict[str, Any]:
        total_duration = sum(s.duration_ms for s in self.spans)
        total_input_tok = sum(s.input_tokens for s in self.spans)
        total_output_tok = sum(s.output_tokens for s in self.spans)
        total_cost = ((total_input_tok / 1000) * price_per_1k_input) + ((total_output_tok / 1000) * price_per_1k_output)

        return {
            "trace_id": self.trace_id,
            "trace_name": self.trace_name,
            "total_duration_ms": total_duration,
            "total_tokens": total_input_tok + total_output_tok,
            "total_cost_usd": total_cost,
            "span_count": len(self.spans)
        }


def main():
    print("=" * 70)
    print("👁️ Module 10: OpenTelemetry LLM Observability & Tracing")
    print("=" * 70)

    tracer = LLMTracer("rag_agent_user_query_flow")

    print("\n[📡 분산 추적 파이프라인 가동...]")

    span1_id = tracer.record_span("input_guardrail", duration_ms=12.5, input_tokens=30, output_tokens=0, attributes={"passed": True})
    span2_id = tracer.record_span("hybrid_rag_search", duration_ms=145.0, input_tokens=80, output_tokens=0, attributes={"retrieved_docs": 3})
    span3_id = tracer.record_span(
        "gemini_inference",
        duration_ms=1050.2,
        input_tokens=650,
        output_tokens=180,
        parent_id=span2_id,
        attributes={"model": "gemini-2.5-flash", "temperature": 0.2}
    )
    span4_id = tracer.record_span("output_pii_masking", duration_ms=18.3, input_tokens=0, output_tokens=0, attributes={"masked_entities": 2})

    report = tracer.generate_report()

    print(f"\n[📊 Trace Summary - Trace ID: {report['trace_id']}]")
    print(f"  • 작업명:           {report['trace_name']}")
    print(f"  • 총 지연시간:      {report['total_duration_ms']:.2f} ms")
    print(f"  • 총 사용 토큰:     {report['total_tokens']:,} Tokens")
    print(f"  • 예상 청구 비용:   ${report['total_cost_usd']:.6f} USD")
    print(f"  • 기록된 Span 수:   {report['span_count']} 개")

    print("\n[🌲 계층적 Span Waterfall 구조]")
    for span in tracer.spans:
        parent_marker = f"(부모: {span.parent_id})" if span.parent_id else "(루트)"
        print(f"  ├── [{span.name:<20}] {span.duration_ms:>7.1f}ms | In:{span.input_tokens:>4}tok, Out:{span.output_tokens:>4}tok | {parent_marker}")

    print("\n" + "=" * 70)
    print("✅ 확인: OpenTelemetry 표준 Tracing을 통해 병목 구간 식별 및 비용 추적 완료.")
    print("=" * 70)


if __name__ == "__main__":
    main()
