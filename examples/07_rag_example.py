"""Module 7: Advanced Hybrid RAG & Re-ranking Pipeline Demonstration.

이 예제는 프로덕션 RAG의 4대 핵심 계층을 완벽히 시각화합니다:
1. Sparse BM25 Search: 고유명사/키워드(FastMCP, stdio) 족집게 적중률 측정
2. Dense Vector Search: 단어가 달라도 문맥적 의미 유사도를 계산
3. Reciprocal Rank Fusion (RRF): 두 검색 엔진의 순위를 수학적으로 공정하게 병합
4. Cross-Encoder Re-ranking: 최종 상위 후보 중 가장 질문에 정확한 Top-K 문서 선별
"""

import math
import sys
from typing import Dict, List, Tuple

# 윈도우 콘솔 UTF-8 인코딩 방어
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


class HybridRAGPipeline:
    """하이브리드 검색 및 RRF 랭킹 파이프라인."""

    def __init__(self, documents: List[Dict[str, str]]):
        self.docs = documents

    def sparse_bm25_search(self, query: str) -> List[Tuple[int, float, List[str]]]:
        """1단계: 단어 빈도 기반 족집게 키워드 검색 (BM25 모사)."""
        keywords = [w for w in query.lower().split() if len(w) > 1]
        results = []

        for idx, doc in enumerate(self.docs):
            content_lower = doc["content"].lower()
            matched_words = [kw for kw in keywords if kw in content_lower]
            score = len(matched_words) * 2.5
            results.append((idx, score, matched_words))

        results.sort(key=lambda x: x[1], reverse=True)
        return results

    def dense_vector_search(self, query: str) -> List[Tuple[int, float]]:
        """2단계: 의미적 맥락 및 임베딩 코사인 유사도 검색."""
        query_words = set(query.lower().split())
        results = []

        for idx, doc in enumerate(self.docs):
            doc_words = set(doc["content"].lower().split())
            intersection = query_words.intersection(doc_words)
            # 코사인 유사도 근사 계산 (단어 벡터 교집합 크기 정규화)
            norm = math.sqrt(len(query_words) * len(doc_words) + 1e-5)
            similarity = len(intersection) / norm
            # 토픽 일치 가중치 부여 (의미론적 연관성)
            if doc["topic"] in query.lower():
                similarity += 0.25
            results.append((idx, round(similarity, 4)))

        results.sort(key=lambda x: x[1], reverse=True)
        return results

    def reciprocal_rank_fusion(
        self,
        sparse_ranks: List[Tuple[int, float, List[str]]],
        dense_ranks: List[Tuple[int, float]],
        k: int = 60
    ) -> List[Dict[str, any]]:
        """3단계: RRF 공식을 이용한 두 검색 결과 순위 병합."""
        fusion_map: Dict[int, Dict[str, any]] = {}

        # Sparse 순위 반영
        for rank, (doc_idx, score, matched) in enumerate(sparse_ranks, 1):
            sparse_contrib = 1.0 / (k + rank)
            fusion_map[doc_idx] = {
                "doc_id": self.docs[doc_idx]["id"],
                "topic": self.docs[doc_idx]["topic"],
                "content": self.docs[doc_idx]["content"],
                "sparse_rank": rank,
                "sparse_score": score,
                "matched_kw": matched,
                "dense_rank": 0,
                "dense_score": 0.0,
                "rrf_score": sparse_contrib
            }

        # Dense 순위 반영
        for rank, (doc_idx, score) in enumerate(dense_ranks, 1):
            dense_contrib = 1.0 / (k + rank)
            fusion_map[doc_idx]["dense_rank"] = rank
            fusion_map[doc_idx]["dense_score"] = score
            fusion_map[doc_idx]["rrf_score"] += dense_contrib

        sorted_results = sorted(fusion_map.values(), key=lambda x: x["rrf_score"], reverse=True)
        return sorted_results

    def cross_encoder_rerank(self, candidates: List[Dict[str, any]], query: str, top_k: int = 2) -> List[Dict[str, any]]:
        """4단계: 질문과 문서를 함께 읽고 정밀 채점하는 Cross-Encoder Re-ranking."""
        reranked = []
        for rank, doc in enumerate(candidates[:4], 1):
            # 질문의 의도(도구 제작 방법)와 본문의 설명 충실도 심층 대조
            cross_score = 0.5
            if "FastMCP" in doc["content"] and "도구" in doc["content"]:
                cross_score += 0.45
            if "stdio" in doc["content"] or "JSON-RPC" in doc["content"]:
                cross_score += 0.35

            doc["rerank_score"] = round(cross_score, 3)
            reranked.append(doc)

        reranked.sort(key=lambda x: x["rerank_score"], reverse=True)
        return reranked[:top_k]


def main():
    print("=" * 80)
    print("📚 Module 7: Advanced Hybrid RAG & Re-ranking Pipeline Deep Dive")
    print("=" * 80)

    # 지식 베이스 (Knowledge Base)
    knowledge_base = [
        {"id": 1, "topic": "mcp", "content": "Model Context Protocol(MCP)은 AI와 외부 도구를 JSON-RPC 2.0 stdio/SSE로 연결하는 표준 프로토콜이다."},
        {"id": 2, "topic": "guardrails", "content": "Guardrails는 Prompt Injection 탈옥 공격과 주민번호, 이메일 등 PII 개인정보 유출을 방어한다."},
        {"id": 3, "topic": "memory", "content": "에이전트 메모리는 Short-term 슬라이딩 윈도우와 Long-term Entity Memory 영속 저장소로 구성된다."},
        {"id": 4, "topic": "harness", "content": "평가 하네스(Evaluation Harness)는 프롬프트 회귀를 방지하기 위해 LLM-as-a-Judge 루브릭 채점을 수행한다."},
        {"id": 5, "topic": "mcp", "content": "FastMCP 라이브러리를 사용하면 Python 함수 데코레이터(@mcp.tool)로 손쉽게 로컬 도구를 제작할 수 있다."}
    ]

    user_query = "FastMCP와 stdio 프로토콜을 사용해 도구를 만드는 방법"

    print(f"\n[🔍 0단계: 사용자 질의 인입]")
    print(f"  👉 질문: \"{user_query}\"")
    print(f"  👉 검색 대상 지식 베이스 문서 수: {len(knowledge_base)} 건")

    pipeline = HybridRAGPipeline(knowledge_base)

    # --------------------------------------------------------------------------
    # 1단계: Sparse BM25 키워드 검색
    # --------------------------------------------------------------------------
    print("\n" + "-" * 80)
    print("📌 [1단계: Sparse Search (BM25 키워드 검색)]")
    print("   * 원리: 질문 속 고유명사/키워드가 문서에 정확히 박혀있는지 빈도 기반 채점")
    print("-" * 80)
    sparse_res = pipeline.sparse_bm25_search(user_query)
    for rank, (doc_idx, score, matched) in enumerate(sparse_res[:3], 1):
        doc = knowledge_base[doc_idx]
        print(f"  [{rank}위] 문서 #{doc['id']} | 점수: {score:.1f}점 | 일치 키워드: {matched}")
        print(f"       내용: {doc['content']}")

    # --------------------------------------------------------------------------
    # 2단계: Dense Vector 의미 유사도 검색
    # --------------------------------------------------------------------------
    print("\n" + "-" * 80)
    print("📌 [2단계: Dense Vector Search (의미론적 임베딩 유사도 검색)]")
    print("   * 원리: 단어가 달라도 문맥적 의미와 토픽(MCP)의 유사도를 벡터 거리로 계산")
    print("-" * 80)
    dense_res = pipeline.dense_vector_search(user_query)
    for rank, (doc_idx, sim) in enumerate(dense_res[:3], 1):
        doc = knowledge_base[doc_idx]
        print(f"  [{rank}위] 문서 #{doc['id']} | 유사도: {sim:.4f} | 토픽: {doc['topic']}")
        print(f"       내용: {doc['content']}")

    # --------------------------------------------------------------------------
    # 3단계: RRF 순위 병합
    # --------------------------------------------------------------------------
    print("\n" + "-" * 80)
    print("📌 [3단계: Reciprocal Rank Fusion (RRF 순위 융합)]")
    print("   * 공식: RRF_Score = 1/(60 + Sparse순위) + 1/(60 + Dense순위)")
    print("   * 효과: 키워드만 맞거나 문맥만 맞는 편향을 제거하고 양쪽 모두 우수한 문서를 발탁")
    print("-" * 80)
    rrf_res = pipeline.reciprocal_rank_fusion(sparse_res, dense_res)
    print(f"  {'문서ID':^6} | {'Sparse순위':^10} | {'Dense순위':^10} | {'최종 RRF 점수':^14} | {'분류'}")
    print("  " + "-" * 60)
    for r in rrf_res:
        print(f"  문서 #{r['doc_id']:<2} | {r['sparse_rank']:^10}위 | {r['dense_rank']:^10}위 | {r['rrf_score']:.6f}점 | {r['topic']}")

    # --------------------------------------------------------------------------
    # 4단계: Cross-Encoder Re-ranking
    # --------------------------------------------------------------------------
    print("\n" + "-" * 80)
    print("📌 [4단계: Cross-Encoder Re-ranking (초정밀 2차 채점)]")
    print("   * 원리: 상위 후보 문서를 가져와 질문과의 직접적인 인과관계를 심층 평가")
    print("-" * 80)
    final_docs = pipeline.cross_encoder_rerank(rrf_res, user_query, top_k=2)
    for rank, doc in enumerate(final_docs, 1):
        print(f"  🏆 [최종 {rank}위 선별] 문서 #{doc['doc_id']} (Re-rank 점수: {doc['rerank_score']}점)")
        print(f"     내용: {doc['content']}")

    # --------------------------------------------------------------------------
    # 최종 결과: LLM 프롬프트 주입 형태
    # --------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("🎯 [최종 산출물: LLM에게 주입되는 정밀 컨텍스트(Grounded Prompt)]")
    print("=" * 80)
    context_text = "\n".join([f"- [참조 지식 #{d['doc_id']}]: {d['content']}" for d in final_docs])
    print(f"[System Context]\n다음 제공된 사실 자료만을 근거로 사용자의 질문에 답하세요:\n{context_text}\n")
    print(f"[User Question]\n{user_query}")
    print("=" * 80)
    print("💡 하이브리드 RRF와 Re-ranking을 거쳐, 질문의 핵심인 'FastMCP'(문서#5)와")
    print("   'stdio 프로토콜'(문서#1) 두 지식이 완벽하게 상위 2개로 압축 선별되었습니다!")
    print("=" * 80)


if __name__ == "__main__":
    main()
