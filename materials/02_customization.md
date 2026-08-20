# 🧠 Module 2: Customization & Agent Steering

Antigravity IDE의 **Customization System**은 코드 수정 없이 마크다운 문서만으로 에이전트의 작동 방식, 코딩 컨벤션, 전문 수행 절차, 그리고 **동적 도구 선택(Dynamic Tool Selection)**을 제어하는 프롬프트 오케스트레이션 메커니즘입니다.

---

## 📌 1. 상시 전역 규칙 (`AGENTS.md`) vs 동적 스킬 (`SKILL.md`)

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        에이전트 통제 이원화 구조                         │
├───────────────────────────────────┬────────────────────────────────────┤
│ 1️⃣ AGENTS.md (상시 고정 규칙)       │ 2️⃣ SKILL.md (동적 호출 매뉴얼)     │
├───────────────────────────────────┼────────────────────────────────────┤
│ • 365일 시스템 프롬프트에 상주    │ • 평소에는 메타 요약(Title)만 기억 │
│ • 핵심 사규, 코딩 스타일, 언어    │ • 사용자 키워드 트리거 시 본문 로드│
│ • "모든 답변은 한글 존댓말로"     │ • "commit-msg", "review-code"      │
│ • 고정 토큰 소비 최소화 (~500 tok)│ • 90% 이상의 토큰 절감 효과        │
└───────────────────────────────────┴────────────────────────────────────┘
```

---

## 🔍 2. Dynamic Tool Selection (메타 도구 검색 패턴)

실무 시스템에서 에이전트가 사용할 수 있는 도구가 50~100개 이상으로 늘어나면, **모든 도구 정의를 프롬프트에 한 번에 넣을 경우 Context Window 폭증과 툴 선택 혼란(Hallucination)**이 발생합니다.

### 2단계 도구 로딩 (Two-Stage Tool Retrieval)
1. **1단계 (Meta-Tool Index)**: 도구의 이름과 1줄 설명만 담긴 경량 인덱스에서 관련 도구 그룹 검색.
2. **2단계 (Detail On-Demand)**: 현재 작업에 반드시 필요한 3~5개의 정밀 도구 스키마만 컨텍스트에 동적 주입.

---

## ⚡ 3. 4대 핵심 생산성 슬래시 커맨드

* `/goal`: 자율 에이전트에게 장시간 실행(Overnight) 목표를 부여하고 중간에 멈추지 않도록 감사 루프 가동.
* `/schedule`: 일회성 타이머나 반복 크론(Cron) 백그라운드 작업을 에이전트에 예약.
* `/grill-me`: 구현 전 설계 결함이나 모호성을 해소하기 위해 에이전트가 사용자를 인터뷰하도록 지시.
* `/learn`: 해결된 모범 사례나 사용자 피드백을 영속적 커스텀 지식으로 저장.

---

## 🏋️ 실습 연동

이 모듈의 실습은 워크스페이스 내 [.agents/AGENTS.md](file:///c:/Coding/AI-Engineering/.agents/AGENTS.md) 및 커스텀 스킬 폴더([.agents/skills/review-code](file:///c:/Coding/AI-Engineering/.agents/skills/review-code/SKILL.md), [.agents/skills/commit-msg](file:///c:/Coding/AI-Engineering/.agents/skills/commit-msg/SKILL.md))와 연동됩니다.
