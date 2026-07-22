# 📚 Module 8: RAG & Vector DB Pipeline

**RAG (Retrieval-Augmented Generation, 검색 증강 생성)**는 거대 언어 모델(LLM)이 최신 정보나 외부 사내 문서 데이터베이스를 실시간으로 검색하여 답변을 생성하도록 돕는 필수 엔터프라이즈 AI 아키텍처입니다.

---

## 🏛️ RAG의 3단계 핵심 파이프라인

```text
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│ 1. Indexing     │ ──►  │ 2. Retrieval    │ ──►  │ 3. Generation   │
│ (청킹 & 임베딩)  │       │ (검색 & 재순위) │       │ (프롬프트 합성) │
└─────────────────┘       └─────────────────┘       └─────────────────┘
```

1. **Indexing (색인)**: 문서를 작게 나누고(Chunking), 임베딩(Embedding) 벡터로 변환하여 벡터 DB에 저장.
2. **Retrieval (검색)**: 질문과 가장 연관성이 높은 문서 조각(Top-K)을 벡터 검색 및 하이브리드 검색으로 탐색.
3. **Generation (생성)**: 추출한 문서 내용을 프롬프트 컨텍스트에 덧붙여 LLM이 사실 기반으로 답변 작성.

---

## 🔍 고성능 RAG를 위한 3가지 고급 기술

### ① 하이브리드 검색 (Hybrid Search)
* **Dense Search (임베딩 벡터 검색)**: 의미적 유사도(Semantic Similarity) 탐색에 우수함.
* **Sparse Search (BM25 키워드 검색)**: 고유 명사, 제품 번호, 이메일 주소 등 정확한 단어 매칭에 우수함.
* ➔ 두 검색 결과를 가중치로 병합(Reciprocal Rank Fusion)하여 최상의 검색 정확도 달성.

### ② Re-ranking (Cross-Encoder 재순위화)
* 1차 검색된 Top-N개 문서를 속도는 조금 늦지만 훨씬 더 정밀한 **Cross-Encoder 모델**로 재평가하여 최상위 Top-K만 필터링하는 기술.

### ③ 에이전틱 RAG (Agentic RAG)
* 단순한 일회성 검색이 아니라, 에이전트가 도구(Tool)로서 RAG 검색기를 소지하고 필요 시 스스로 쿼리를 재작성(Query Rewriting)하며 멀티 턴 검색 수행.

---

## 🏋️ 실습 예제 따라하기

이 모듈과 연계되는 파이썬 실습 코드 파일은 [examples/rag_example.py](file:///c:/Coding/AI-Engineering/examples/rag_example.py)에 작성되어 있습니다.

### 실습 실행 방법
```bash
python examples/rag_example.py
```

### 코드 주요 포인트
* 문서 데이터 청킹 및 코사인 유사도(Cosine Similarity) 기반 벡터 검색 시뮬레이션.
* 검색된 문서 지식(Context)을 바탕으로 사실 기반 답변을 합성하는 파이프라인 흐름 확인.
