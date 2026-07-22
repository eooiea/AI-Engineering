# 🎯 Module 4: Evaluation and Harness (평가 하네스)

인공지능 모델이 생성하는 결과물은 항상 동일하지 않고 비결정적(Non-deterministic)입니다. 프롬프트를 조금 고치거나 모델의 버전을 업그레이드하면, 이전에는 잘 되던 답변이 엉뚱하게 깨지는 **회귀(Regression) 현상**이 빈번하게 발생합니다.

따라서 AI 엔지니어링의 신뢰성을 담보하기 위해 가장 중요한 프로세스가 바로 **평가 하네스 (Evaluation Harness)** 의 구축입니다. 코드 개발에서 단위 테스트(Unit Test)를 짜는 것처럼, 프롬프트나 에이전트 시스템의 출력값을 체계적으로 테스트하는 자동화 환경입니다.

---

## 📐 AI 평가의 주요 방법론

평가 하네스는 대개 세 가지 검증 모델을 혼합하여 동작합니다.

### 1. 규칙 기반 검증 (Rule-based Assertions)
*   프로그래밍 방식으로 결과물의 정량적 조건을 비교합니다.
*   예: 글자 수 범위 검증, 특정 필수 키워드 포함 여부(contains), 유효한 JSON 형식 검증, 이메일/URL 정규식(Regex) 부합 여부.
*   *장점*: 속도가 매우 빠르고 비용이 전혀 들지 않습니다.

### 2. 의미론적 유사도 검증 (Semantic Similarity)
*   생성된 문장과 모범 답안(Ground Truth)의 임베딩 벡터 간의 코사인 유사도를 계산하여 의미가 통하는지 검증합니다.
*   *장점*: 단어나 조사 수준이 달라도 핵심 의미가 비슷하면 성공 처리할 수 있습니다.

### 3. LLM 판사 기법 (LLM-as-a-Judge)
*   지능이 높은 상위 모델(예: Gemini Pro)에게 평가 대상 답변과 평가 기준 루브릭(Rubric)을 주고 채점(예: 1~5점)을 하게 만듭니다.
*   *장점*: 단순 규칙으로 잡기 힘든 가독성, 친절도, 환각(Hallucination) 여부, 안전성(Safety) 등 정성적 평가가 가능합니다.

---

## 🛠️ 주요 오픈소스 평가 프레임워크

1. **Promptfoo**:
   *   YAML 파일로 프롬프트, 입력 테스트 케이스, 어설션을 정의하고 CLI 창에서 여러 모델이나 프롬프트 버전을 매트릭스 형태로 비교 테스트할 수 있습니다.
   *   속도가 빠르고 경량화되어 있으며, CI/CD 배포 파이프라인에 탑재하기 좋습니다. (현재 OpenAI가 인수하여 오픈소스로 유지관리 중)
2. **DeepEval**:
   *   파이썬의 `pytest` 스타일을 채택하여 파이썬 엔지니어들에게 친숙한 단위 테스트 환경을 제공합니다.
3. **Ragas**:
   *   RAG(Retrieval-Augmented Generation) 시스템에 특화되어 검색된 문서와 최종 답변 간의 충실도(Faithfulness), 관련성(Answer Relevance) 등을 정밀하게 측정합니다.

---

## 🏋️ 실습 예제 따라하기

이 모듈과 연계되는 실습 파일은 [examples/harness/eval_harness.py](file:///c:/Coding/AI-Engineering/examples/harness/eval_harness.py)에 생성되어 있습니다.

### 실습 절차
1. [examples/harness/eval_harness.py](file:///c:/Coding/AI-Engineering/examples/harness/eval_harness.py) 파일을 열어 규칙 기반의 Assertion 테스터 작동 방식을 확인합니다.
2. 터미널 창을 열고 `python examples/harness/eval_harness.py` 명령을 실행합니다.
3. 테스트 러너가 복수의 모의 답변(예: JSON 형식 답변, 부적절한 글자 수의 답변 등)들을 상대로 지정된 규칙(JSON 검증, 정규식 검증, 단어 포함 여부)을 평가하고 테스트 성공/실패 여부를 리포트 형태로 상세히 출력하는 것을 직접 확인합니다.
