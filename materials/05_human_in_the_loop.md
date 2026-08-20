# 🛑 Module 5: Human-in-the-Loop & Safety Governance

실무 프로덕션 환경의 AI 에이전트는 결제 승인, 데이터베이스 변경/삭제, 배포 스크립트 실행, 대량 이메일 발송 등 **부수 효과(Side-Effect)가 큰 위험 도구**를 실행할 때 무조건적인 자율 실행을 방지하고 사람의 승인을 받아야 합니다. 이를 **Human-in-the-Loop (HITL)** 또는 **중단점(Breakpoint & Resume)** 아키텍처라고 부릅니다.

---

## 🛡️ 1. 위험도 기반 도구 분류 체계 (Tool Risk Matrix)

```text
┌─────────────────────────────────────────────────────────────┐
│                     도구 위험도 등급 체계                    │
├──────────────────────────┬──────────────────────────────────┤
│ 🟢 Tier 1: Safe (Read)   │ 🔴 Tier 2: Dangerous (Write/Exec)│
├──────────────────────────┼──────────────────────────────────┤
│ • 자동 승인 (Auto-exec)  │ • 사람 승인 필수 (Interrupt)     │
│ • 파일 읽기, 웹 검색     │ • 파일 삭제/수정, 셸 명령어 실행 │
│ • DB SELECT 쿼리         │ • DB DROP/DELETE, 외부 결제 호출 │
└──────────────────────────┴──────────────────────────────────┘
```

---

## ⏸️ 2. Interrupt & Resume 상태 머신 아키텍처

LangGraph 및 Antigravity IDE의 승인 대화상자(Modal)는 다음과 같은 비동기 상태 머신(State Machine)으로 동작합니다.

```text
[에이전트 작업 수행] ──► [도구 호출 요청 (Tool Call)]
                                 │
                 ┌───────────────┴───────────────┐
                 ▼ (Safe Tool)                   ▼ (Dangerous Tool)
          [즉시 실행 (Auto)]              [실행 일시 정지 (Interrupt)]
                 │                               │
                 │                        [승인 대기 (Human Approval)]
                 │                               │
                 │                    ┌──────────┴──────────┐
                 │                    ▼ 승인됨 (Approve)    ▼ 거부됨 (Reject)
                 │             [도구 재개 (Resume)]  [오류 피드백 반환]
                 │                    │                     │
                 └────────────────────┴─────────────────────┘
                                      │
                                      ▼
                            [다음 에이전트 단계 진행]
```

1. **Interrupt (일시 정지)**: 위험 도구가 감지되면 현재 세션 상태(State Snapshot)를 저장하고 실행을 멈춥니다.
2. **Human Inspection**: 사용자나 관리자에게 호출할 도구명과 인자(Arguments)를 UI에 렌더링하고 `승인(Approve)` 또는 `거부(Reject)`를 요청합니다.
3. **Resume (재개)**: 승인 시 저장된 상태 스냅샷을 복원하여 도구를 안전하게 실행하고 다음 추론 루프로 복귀합니다.

---

## 🏋️ 실습 예제 따라하기

이 모듈과 연계되는 파이썬 실습 코드 파일은 [examples/hitl_example.py](file:///c:/Coding/AI-Engineering/examples/hitl_example.py)에 작성되어 있습니다.

```bash
python examples/hitl_example.py
```

### 핵심 실습 포인트
* 위험 도구(파일 삭제, DB 수정 등)와 안전 도구(조회)의 데코레이터 분류.
* 위험 도구 호출 시 상태를 일시 정지하고 대화형/시뮬레이션 승인 토큰을 받아 안전하게 재개(Resume)하는 워크플로우 확인.
