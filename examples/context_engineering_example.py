"""Module 0: AI IDE Architecture & Context Engineering Simulation.

Prompt Caching(KV-Cache)과 Context Compaction(정적 스크립트 전처리 및 토큰 다이어트)
효과를 정량적으로 시뮬레이션하고 측정하는 예제입니다.
"""

import dataclasses
import json
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


@dataclasses.dataclass
class TokenBudgetStats:
    raw_tokens: int
    optimized_tokens: int
    cached_tokens: int
    cost_raw_usd: float
    cost_optimized_usd: float
    latency_raw_ms: float
    latency_optimized_ms: float


class ContextOptimizer:
    """정적 스크립트 전처리 및 Prompt Caching 시뮬레이터."""

    def __init__(self, price_per_1k_input: float = 0.0015, price_per_1k_cached: float = 0.0003):
        self.price_input = price_per_1k_input
        self.price_cached = price_per_1k_cached

    def simulate_pipeline(self, raw_codebase: str, user_query: str) -> TokenBudgetStats:
        raw_tokens = len(raw_codebase.split()) * 2
        raw_tokens += len(user_query.split()) * 2
        cost_raw = (raw_tokens / 1000) * self.price_input
        latency_raw = raw_tokens * 0.15

        static_system_tokens = 400
        cached_tokens = static_system_tokens

        condensed_summary = {
            "file": "main.py",
            "total_lines": 1500,
            "detected_issues": [
                {"line": 42, "type": "SyntaxWarning", "msg": "undefined variable 'target'"},
                {"line": 108, "type": "SecurityRisk", "msg": "hardcoded password detected"}
            ]
        }
        summary_tokens = len(json.dumps(condensed_summary).split()) * 2
        dynamic_tokens = summary_tokens + (len(user_query.split()) * 2)

        optimized_tokens = static_system_tokens + dynamic_tokens
        cost_optimized = ((cached_tokens / 1000) * self.price_cached) + ((dynamic_tokens / 1000) * self.price_input)
        latency_optimized = (cached_tokens * 0.01) + (dynamic_tokens * 0.15)

        return TokenBudgetStats(
            raw_tokens=raw_tokens,
            optimized_tokens=optimized_tokens,
            cached_tokens=cached_tokens,
            cost_raw_usd=cost_raw,
            cost_optimized_usd=cost_optimized,
            latency_raw_ms=latency_raw,
            latency_optimized_ms=latency_optimized
        )


def main():
    print("=" * 70)
    print("🧩 Module 0: Context Engineering & Prompt Caching Simulator")
    print("=" * 70)

    mock_large_codebase = "\n".join([f"def function_{i}(): return 'result_{i}'" for i in range(500)])
    user_query = "main.py에서 보안 결함 및 구문 오류가 발생하는 줄을 찾아 수정해줘."

    optimizer = ContextOptimizer()
    stats = optimizer.simulate_pipeline(mock_large_codebase, user_query)

    print("\n[📊 1. 토큰 사용량 비교]")
    print(f"  • 원본 전체 코드 주입 시:  {stats.raw_tokens:>6,} Tokens")
    print(f"  • 정적 압축 및 캐싱 적용 시: {stats.optimized_tokens:>6,} Tokens (캐시 히트: {stats.cached_tokens:,} tok)")
    reduction_pct = (1 - (stats.optimized_tokens / stats.raw_tokens)) * 100
    print(f"  🔥 토큰 절감율: {reduction_pct:.1f}% 절약 달성!")

    print("\n[💰 2. 1회 API 호출 비용 비교 (1M 쿼리 기준 추정)]")
    print(f"  • 원본 주입 1회 비용:      ${stats.cost_raw_usd:.5f} (100만 회: ${stats.cost_raw_usd * 1_000_000:,.2f})")
    print(f"  • 최적화 주입 1회 비용:    ${stats.cost_optimized_usd:.5f} (100만 회: ${stats.cost_optimized_usd * 1_000_000:,.2f})")

    print("\n[⚡ 3. 응답 대기 지연시간(Latency) 비교]")
    print(f"  • 원본 주입 예상 지연시간:  {stats.latency_raw_ms:>6.1f} ms")
    print(f"  • 최적화 주입 예상 지연시간: {stats.latency_optimized_ms:>6.1f} ms (KV-Cache 고속 로드)")

    print("\n" + "=" * 70)
    print("✅ 결론: 결정론적 scripts/ 전처리와 Prompt Caching 배치가 결합될 때")
    print("   비용 80%+ 절감, 지연시간 단축, Lost-in-the-Middle 문제 원천 차단.")
    print("=" * 70)


if __name__ == "__main__":
    main()
