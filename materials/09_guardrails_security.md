# 🛡️ Module 9: Enterprise Guardrails & AI Security

**Guardrails (가드레일)** 시스템은 AI 에이전트가 실제 상용 서비스(Production) 환경에 배포될 때, 사용자 악의적 공격(Prompt Injection), 시스템 프롬프트 유출(System Prompt Leakage), 개인정보(PII) 유출 및 비정상 출력을 실시간으로 차단하는 **필수 보안 레이어**입니다.

---

## 🔒 1. 3대 핵심 AI 보안 위험 요소 및 방어책

```text
┌─────────────────────────────────────────────────────────────┐
│                 엔터프라이즈 AI 보안 위협 매트릭스            │
├─────────────────┬─────────────────────────┬─────────────────┤
│ 1. Injection    │ 2. PII Leakage          │ 3. Schema Abuse │
│ (탈옥/명령 주입)│ (개인정보 무단 노출)    │ (출력 구조 파손)│
│ - 탈옥 프롬프트 │ - 전화번호, 이메일, 주민│ - JSON 파싱 실패│
│ ➔ Semantic Guard │ ➔ 정규식/NER 자동 마스킹│ ➔ Pydantic Guard│
└─────────────────┴─────────────────────────┴─────────────────┘
```

1. **Prompt Injection & Jailbreak (프롬프트 주입 및 탈옥)**:
   * "이전 모든 시스템 지침을 무시하라" 등의 명령을 차단하기 위해 입력 가드레일에서 시맨틱 유사도 및 위험 키워드 검사 수행.
2. **PII (Personally Identifiable Information) 보호**:
   * 모델의 출력에서 전화번호, 계좌번호, 이메일, 주민번호 등을 정규식 및 개체명 인식(NER)으로 감지하여 `***-****-****` 형태로 마스킹.
3. **Schema Violation & Safety Guard**:
   * 악의적 사용자가 모델에게 비정상적인 포맷을 유도할 때 Pydantic Validator가 즉시 차단.

---

## 🛡️ 2. 2중 가드레일 파이프라인 (Input & Output Dual Gate)

```text
[사용자 입력] ──► [1. Input Guardrail] ──► [2. Agent / LLM] ──► [3. Output Guardrail] ──► [안전한 응답]
                      (악의적 주입 감지)                             (PII 마스킹 및 스키마 검증)
```

---

## 🏋️ 실습 예제 따라하기

이 모듈과 연계되는 파이썬 실습 코드 파일은 [examples/09_guardrails_example.py](file:///c:/Coding/AI-Engineering/examples/09_guardrails_example.py)에 작성되어 있습니다.

```bash
python examples/09_guardrails_example.py
```
