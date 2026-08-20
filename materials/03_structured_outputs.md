# 📐 Module 3: Structured Outputs & Self-Correction Loop

인공지능 모델이 생성하는 결과물을 엔터프라이즈 백엔드나 프론트엔드 API에 안정적으로 통합하려면, 자유 텍스트가 아닌 **엄격한 스키마(JSON Schema / Pydantic)**를 100% 강제하고, 런타임 오류 시 에이전트가 스스로 수정하는 **자가 치유(Self-Healing) 루프**가 필수적입니다.

---

## 🔒 1. Structured Outputs의 3대 통제 기술

```text
┌─────────────────────────────────────────────────────────────┐
│                 Structured Output 통제 레벨                 │
├─────────────────┬─────────────────────────┬─────────────────┤
│ 1. Prompting    │ 2. Tool / JSON Mode     │ 3. Grammars     │
│ (프롬프트 요청) │ (함수 호출 스키마 강제) │ (로짓 마스킹)   │
│ - "JSON으로 줘" │ - tool_choice, Pydantic │ - BNF Grammar   │
│ - 파싱 에러 잦음│ - 스키마 준수율 99%     │ - 100% 문법 보장│
└─────────────────┴─────────────────────────┴─────────────────┘
```

1. **Prompt-based (원시적 방식)**: 프롬프트에 "JSON 포맷으로 출력해줘"라고 지시. 사족(`Here is your JSON:`)이 붙거나 따옴표 누락 등 파싱 오류가 빈번합니다.
2. **Tool/Function Calling Mode**: OpenAI/Gemini의 스키마 선언(`tools=[schema]`)을 활용해 모델의 출력을 JSON Arguments로 직접 강제합니다.
3. **Grammar-based Decoding (Constrained Decoding)**: 로컬 엔진(Llama.cpp, SGLang, vLLM)에서 BNF 문법에 맞지 않는 다음 토큰 생성을 수학적으로 0% 차단하여 100% 스키마를 보장합니다.

---

## 🔁 2. Reflection & Self-Correction (자가 치유) 아키텍처

LLM이 생성한 코드가 실행 도중 `ZeroDivisionError`나 `KeyError`, 혹은 Pydantic `ValidationError`를 발생시켰을 때 전체 파이프라인을 중단하지 않고 자가 치유하는 패턴입니다.

```text
┌─────────────┐
│  작업 요청  │
└──────┬──────┘
       ▼
┌─────────────┐       실행 성공
│  코드 생성  │ ──────────────────────► [최종 완료]
└──────┬──────┘
       │ 실행 오류 / 스키마 불일치
       ▼
┌─────────────┐
│ 에러 트레이스│
│ 피드백 주입 │
└──────┬──────┘
       │ 수정 프롬프트 전송 (최대 N회 반복)
       └──────────────► [코드 재생성]
```

---

## 🏋️ 실습 예제 따라하기

이 모듈과 연계되는 파이썬 실습 코드 파일은 [examples/structured_outputs_example.py](file:///c:/Coding/AI-Engineering/examples/structured_outputs_example.py)에 작성되어 있습니다.

```bash
python examples/structured_outputs_example.py
```

### 핵심 실습 포인트
* Pydantic `BaseModel`을 통한 엄격한 데이터 필드 및 유효성 검사.
* 의도적인 파싱 실패/런타임 에러 발생 시 에러 트레이스를 피드백으로 주입하여 자가 수정하는 Self-Healing 루프 구동.
