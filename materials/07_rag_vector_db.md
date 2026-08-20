# 📚 Module 7: Advanced Hybrid RAG & Vector Pipeline

**RAG (Retrieval-Augmented Generation)**는 LLM이 최신 사내 지식이나 문서를 검색하여 환각(Hallucination) 없이 사실 기반 답변을 생성하도록 돕는 필수 아키텍처입니다. 본 단원에서는 단순 벡터 검색을 넘어 **하이브리드 검색(Hybrid Search)**과 **Re-ranking**, **Agentic RAG**를 다룹니다.

---

## 🏛️ 1. 고성능 RAG 파이프라인 4단계

```text
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│ 1. Advanced     │ ──►  │ 2. Hybrid       │ ──►  │ 3. Re-ranking   │ ──►  │ 4. Grounded     │
│    Chunking     │       │    Retrieval    │       │ (Cross-Encoder) │       │    Generation   │
│ (Semantic/Hier) │       │ (Dense + Sparse)│       │ (Top-N ➔ Top-K) │       │ (사실 기반 합성)│
└─────────────────┘       └─────────────────┘       └─────────────────┘       └─────────────────┘
```

1. **Advanced Chunking**: 고정 길이 분할 대신 의미론적 문단 경계(Semantic Chunking) 또는 부모-자식(Parent-Child) 계층 청킹 적용.
2. **Hybrid Retrieval**: 의미적 맥락을 찾는 **Dense Search (임베딩 벡터)**와 고유명사/코드명을 정확히 찾는 **Sparse Search (BM25)**를 결합.
3. **RRF (Reciprocal Rank Fusion)**: 두 검색 결과의 순위를 수학적으로 병합하여 최적의 검색 점수 산출:
   $$RRF\_Score(d) = \sum_{m \in M} \frac{1}{k + r_m(d)}$$
4. **Cross-Encoder Re-ranking**: 1차 검색된 Top-20개 문서를 정밀한 Re-ranker 모델로 재평가하여 최상위 Top-3만 최종 프롬프트에 주입.

---

## 🤖 2. 에이전틱 RAG (Agentic RAG)

단순 일회성 검색이 아니라, 에이전트가 검색기를 도구(Tool)로 쥐고 다음과 같은 지능형 결정을 내립니다:
* **Query Rewriting**: 질문이 모호하면 검색 쿼리를 명확하게 재작성.
* **Multi-hop Search**: 복잡한 질문에 대해 1차 검색 결과를 바탕으로 2차, 3차 추가 질의 수행.
* **Self-Reflection (답변 충분성 검증)**: 검색된 문서로 답변이 가능한지 스스로 검증하고 불충분하면 검색어 수정 후 재검색.

---

## 🏋️ 실습 예제 따라하기

이 모듈과 연계되는 파이썬 실습 코드 파일은 [examples/rag_example.py](file:///c:/Coding/AI-Engineering/examples/rag_example.py)에 작성되어 있습니다.

```bash
python examples/rag_example.py
```
