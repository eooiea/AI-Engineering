"""LLM Observability & Distributed Tracing Module.

에이전트 및 도구 실행 단계별 지연시간(Latency) 및 토큰 사용량을 수집/추적하는 트레이서 시뮬레이션입니다.
"""
import time
from typing import Optional

class Span:
    """단일 실행 단위 작업(Span)의 메트릭 수집기."""
    def __init__(self, name: str):
        self.name = name
        self.start_time = 0.0
        self.end_time = 0.0
        self.duration_ms = 0.0
        self.input_tokens = 0
        self.output_tokens = 0

    def __enter__(self):
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.perf_counter()
        self.duration_ms = (self.end_time - self.start_time) * 1000.0


class AgentTracer:
    """전체 트레이스(Trace) 세션 관리기."""
    def __init__(self, trace_id: str):
        self.trace_id = trace_id
        self.spans: list[Span] = []

    def start_span(self, name: str) -> Span:
        span = Span(name)
        self.spans.append(span)
        return span

    def print_trace_summary(self):
        total_duration = sum(s.duration_ms for s in self.spans)
        total_input_tokens = sum(s.input_tokens for s in self.spans)
        total_output_tokens = sum(s.output_tokens for s in self.spans)

        print("\n" + "=" * 40 + f" LLM Observability Summary [Trace: {self.trace_id}] " + "=" * 40)
        print(f"총 실행 시간 (Total Latency): {total_duration:.2f} ms")
        print(f"총 토큰 사용량 (Total Cost): {total_input_tokens + total_output_tokens} tokens (Input: {total_input_tokens}, Output: {total_output_tokens})")
        print("-" * 96)
        print(f"{'Span Name':<35} | {'Latency (ms)':<15} | {'Tokens (In/Out)':<20}")
        print("-" * 96)
        for s in self.spans:
            tokens_str = f"{s.input_tokens} / {s.output_tokens}" if s.input_tokens or s.output_tokens else "N/A"
            print(f"{s.name:<35} | {s.duration_ms:<15.2f} | {tokens_str:<20}")
        print("=" * 96)


if __name__ == "__main__":
    print("[Start] LLM Observability & Tracing 실습\n")
    tracer = AgentTracer(trace_id="tr_8f9a2b1c")

    # Step 1: Input Guardrail Check
    with tracer.start_span("Span_1: Input_Guardrail_Check") as s1:
        time.sleep(0.02)  # 20ms 작업 시뮬레이션

    # Step 2: RAG Vector Search
    with tracer.start_span("Span_2: RAG_Vector_Search") as s2:
        time.sleep(0.08)  # 80ms 작업 시뮬레이션
        s2.input_tokens = 50

    # Step 3: LLM Generation
    with tracer.start_span("Span_3: Gemini_Flash_Generation") as s3:
        time.sleep(0.35)  # 350ms 작업 시뮬레이션
        s3.input_tokens = 320
        s3.output_tokens = 110

    # Step 4: Output Guardrail PII Filter
    with tracer.start_span("Span_4: Output_Guardrail_Filter") as s4:
        time.sleep(0.01)  # 10ms 작업 시뮬레이션

    # 트레이스 보고서 출력
    tracer.print_trace_summary()
