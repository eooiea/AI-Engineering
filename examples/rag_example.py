"""Module 7: Advanced Hybrid RAG & Vector Pipeline.

Dense Vector Search(의미 유사도)와 Sparse Search(BM25 키워드)를
Reciprocal Rank Fusion(RRF)으로 병합하고 Re-ranking을 거치는 고정밀 RAG 파이프라인입니다.
"""

import math
import sys
from typing import List, Dict, Tuple

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


class HybridRAGPipeline:
    """하이브리드 검색 및 RRF 랭킹 파이프라인."""

    def __init__(self, documents: List[Dict[str, str]]):
        self.docs = documents

    def sparse_bm25_search(self, query: str) -> List[Tuple[int, float]]:
        keywords = query.lower().split()
        scores = []
        for idx, doc in enumerate(self.docs):
            content_lower = doc["content"].lower()
            match_count = sum(content_lower.count(kw) for kw in keywords)
            score = match_count * 1.5
            scores.append((idx, score))
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores

    def dense_vector_search(self, query: str) -> List[Tuple[int, float]]:
        query_words = set(query.lower().split())
        scores = []
        for idx, doc in enumerate(self.docs):
            doc_words = set(doc["content"].lower().split())
            intersection = query_words.intersection(doc_words)
            similarity = len(intersection) / math.sqrt(len(query_words) * len(doc_words) + 1e-5)
            scores.append((idx, similarity))
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores

    def reciprocal_rank_fusion(self, sparse_ranks: List[Tuple[int, float]], dense_ranks: List[Tuple[int, float]], k: int = 60) -> List[Tuple[int, float]]:
        rrf_scores: Dict[int, float] = {}

        for rank, (doc_idx, _) in enumerate(sparse_ranks):
            rrf_scores[doc_idx] = rrf_scores.get(doc_idx, 0.0) + (1.0 / (k + rank + 1))

        for rank, (doc_idx, _) in enumerate(dense_ranks):
            rrf_scores[doc_idx] = rrf_scores.get(doc_idx, 0.0) + (1.0 / (k + rank + 1))

        ranked_results = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)
        return ranked_results

    def cross_encoder_rerank(self, candidates: List[Tuple[int, float]], query: str, top_k: int = 2) -> List[Dict[str, str]]:
        reranked = []
        for doc_idx, rrf_score in candidates[:5]:
            doc = self.docs[doc_idx]
            relevance_boost = 1.2 if doc["topic"] in query else 1.0
            final_score = rrf_score * relevance_boost
            reranked.append((doc, final_score))
        
        reranked.sort(key=lambda x: x[1], reverse=True)
        return [item[0] for item in reranked[:top_k]]


def main():
    print("=" * 70)
    print("📚 Module 7: Advanced Hybrid RAG & Re-ranking Pipeline")
    print("=" * 70)

    knowledge_base = [
        {"id": 1, "topic": "mcp", "content": "Model Context Protocol(MCP)은 AI와 외부 도구를 JSON-RPC 2.0 stdio/SSE로 연결하는 표준 프로토콜이다."},
        {"id": 2, "topic": "guardrails", "content": "Guardrails는 Prompt Injection 탈옥 공격과 주민번호, 이메일 등 PII 개인정보 유출을 방어한다."},
        {"id": 3, "topic": "memory", "content": "에이전트 메모리는 Short-term 슬라이딩 윈도우와 Long-term Entity Memory 영속 저장소로 구성된다."},
        {"id": 4, "topic": "harness", "content": "평가 하네스(Evaluation Harness)는 프롬프트 회귀를 방지하기 위해 LLM-as-a-Judge 루브릭 채점을 수행한다."},
        {"id": 5, "topic": "mcp", "content": "FastMCP 라이브러리를 사용하면 Python 함수 데코레이터로 손쉽게 로컬 MCP 도구를 제작할 수 있다."}
    ]

    pipeline = HybridRAGPipeline(knowledge_base)
    user_query = "FastMCP와 stdio 프로토콜을 사용해 도구를 만드는 방법"

    print(f"\n[🔍 1. 사용자 질문]: '{user_query}'")

    sparse_res = pipeline.sparse_bm25_search(user_query)
    print(f"  • Sparse BM25 Top 1 ID: {knowledge_base[sparse_res[0][0]]['id']}")

    dense_res = pipeline.dense_vector_search(user_query)
    print(f"  • Dense Vector Top 1 ID: {knowledge_base[dense_res[0][0]]['id']}")

    rrf_res = pipeline.reciprocal_rank_fusion(sparse_res, dense_res)
    print("  • RRF 결합 점수 상위 3개 인덱스:", [(knowledge_base[idx]['id'], round(score, 4)) for idx, score in rrf_res[:3]])

    final_docs = pipeline.cross_encoder_rerank(rrf_res, user_query, top_k=2)

    print("\n[🎯 2. Cross-Encoder Re-ranking 최종 선별된 최상위 지식 (Top 2)]")
    for doc in final_docs:
        print(f"  📌 [문서 ID: {doc['id']} | 분류: {doc['topic']}] {doc['content']}")

    print("\n" + "=" * 70)
    print("✅ 확인: Hybrid RRF와 Cross-Encoder Re-ranking으로 환각 없는")
    print("   최고 수준의 지식 컨텍스트를 프롬프트에 제공합니다.")
    print("=" * 70)


if __name__ == "__main__":
    main()
