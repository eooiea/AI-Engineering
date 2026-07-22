"""RAG & Vector DB Pipeline Simulation Module.

문서 청킹, 임베딩 벡터 생성 시뮬레이션, 코사인 유사도 검색 및 하이브리드 RAG 생성을 시연합니다.
"""
import math

class VectorStore:
    """간단한 메모리 기반 벡터 데이터베이스 시뮬레이터."""
    def __init__(self):
        self.documents = []
        self.embeddings = []

    def _simple_embedding(self, text: str) -> list[float]:
        """텍스트에서 키워드 빈도를 추출하여 5차원 가상 임베딩 벡터를 반환합니다."""
        keywords = ["mcp", "agent", "rag", "security", "eval"]
        text_lower = text.lower()
        vec = [float(text_lower.count(kw)) for kw in keywords]
        norm = math.sqrt(sum(x * x for x in vec)) or 1.0
        return [x / norm for x in vec]

    def add_document(self, doc_id: str, content: str):
        """문서를 청킹하고 벡터화하여 메모리에 저장합니다."""
        vec = self._simple_embedding(content)
        self.documents.append({"id": doc_id, "content": content})
        self.embeddings.append(vec)

    def search(self, query: str, top_k: int = 2) -> list[dict]:
        """쿼리 임베딩과 문서 임베딩 간 코사인 유사도를 계산하여 Top-K 반환."""
        query_vec = self._simple_embedding(query)
        scores = []
        for idx, doc_vec in enumerate(self.embeddings):
            # 코사인 유사도 (내적)
            sim = sum(q * d for q, d in zip(query_vec, doc_vec))
            scores.append((sim, self.documents[idx]))
        
        scores.sort(key=lambda x: x[0], reverse=True)
        return [doc for score, doc in scores[:top_k]]


class RAGPipeline:
    """검색 기반 합성 응답 생성기."""
    def __init__(self, vector_store: VectorStore):
        self.store = vector_store

    def query(self, user_question: str) -> str:
        print(f"[RAG] 쿼리 수신: '{user_question}'")
        retrieved_docs = self.store.search(user_question, top_k=2)
        
        print("\n[RAG Retrieval] 검색된 Top-K 문서 조각:")
        for idx, doc in enumerate(retrieved_docs, 1):
            print(f"  ({idx}) [{doc['id']}] {doc['content'][:60]}...")
            
        context_str = "\n".join([d["content"] for d in retrieved_docs])
        
        # LLM 프롬프트 합성
        prompt = f"다음 검색 문맥을 참조하여 질문에 답하세요:\n[문맥]\n{context_str}\n\n[질문]\n{user_question}"
        print(f"\n[RAG Prompt Synthesis] 합성된 프롬프트 전달 완료")
        
        return f"합성 답변: 검색된 문맥에 기반하여 질문 '{user_question}'에 대응하는 근거 중심 답변이 성공적으로 생성되었습니다."


if __name__ == "__main__":
    print("[Start] RAG & Vector DB Pipeline 시뮬레이션 가동\n")
    store = VectorStore()
    
    # 가상 사내 지식 문서 입력 (청킹 데이터)
    store.add_document("doc_1", "Model Context Protocol(MCP)은 AI 에이전트와 외부 도구를 연동하는 표준 전송 프로토콜입니다.")
    store.add_document("doc_2", "RAG 시스템은 임베딩 벡터와 키워드 하이브리드 검색을 결합하여 환각을 방지합니다.")
    store.add_document("doc_3", "Agentic Orchestration은 Master와 Worker 에이전트가 협업하여 고도화된 소프트웨어를 구축합니다.")
    
    pipeline = RAGPipeline(store)
    response = pipeline.query("MCP 및 RAG 시스템의 역할이 뭐야?")
    
    print("\n" + "=" * 40 + " 최종 RAG 답변 " + "=" * 40)
    print(response)
    print("=" * 96)
