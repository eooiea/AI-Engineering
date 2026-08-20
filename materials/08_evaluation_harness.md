# 🧪 Module 8: Evaluation Harness & LLM-as-a-Judge

인공지능 모델은 비결정적(Non-deterministic)이므로, 프롬프트나 모델을 조금만 수정해도 이전 기능이 오작동하는 **회귀(Regression) 현상**이 자주 발생합니다. 이를 통제하기 위해 코드의 단위 테스트처럼 자동화된 **평가 하네스(Evaluation Harness)**와 **LLM 판사(LLM-as-a-Judge)** 시스템을 구축해야 합니다.

---

## 📐 1. 3단계 다계층 평가 방법론

```text
┌─────────────────────────────────────────────────────────────┐
│                     3단계 AI 평가 프레임워크                  │
├─────────────────┬─────────────────────────┬─────────────────┤
│ 1️⃣ Deterministic│ 2️⃣ Semantic Similarity  │ 3️⃣ LLM-as-a-Judge│
│ (결정론적 규칙) │ (임베딩 코사인 유사도)  │ (상위 모델 채점)│
│ - JSON 파싱 성공│ - 모범 답안과 벡터 비교 │ - 1~5점 Rubric  │
│ - Regex, 단어수 │ - 조사/어미 차이 포용   │ - 환각/충실도   │
│ - 0.001초 소요  │ - 0.05초 소요           │ - 정밀 정성 평가│
└─────────────────┴─────────────────────────┴─────────────────┘
```

---

## ⚖️ 2. LLM-as-a-Judge 정량 루브릭 (Rubric) 설계

LLM 판사에게 모호하게 "평가해줘"라고 요청하면 판사 모델조차 일관성을 잃습니다. 실무에서는 다음과 같이 **구체적인 채점 루브릭**을 프롬프트에 제공합니다.

| 점수 | 판정 기준 (Rubric) |
| :--- | :--- |
| **5점 (Exceptional)** | 제공된 Context의 사실만을 100% 인용하며, 논리적 결함이나 불필요한 사족이 없음 |
| **3점 (Moderate)** | 대체로 맞으나 사소한 환각이 섞여 있거나 필수 요구 항목 중 일부가 누락됨 |
| **1점 (Failed)** | 명백한 허위 사실(Hallucination)을 생성하거나 지시사항을 정면으로 위반함 |

---

## 🔁 3. CI/CD 파이프라인 통합 및 회귀 방지

* Git PR(Pull Request) 생성 시 GitHub Actions에서 평가 하네스(`eval_harness.py`)를 자동 실행.
* 이전 프롬프트 버전(Baseline) 대비 Pass Rate가 하락하거나 평균 점수가 떨어지면 병합(Merge)을 차단.

---

## 🏋️ 실습 예제 따라하기

이 모듈과 연계되는 파이썬 실습 코드 파일은 [examples/harness/eval_harness.py](file:///c:/Coding/AI-Engineering/examples/harness/eval_harness.py)에 작성되어 있습니다.

```bash
python examples/harness/eval_harness.py
```
