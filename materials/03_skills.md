# 🧠 Module 3: Customization System & Slash Commands

Antigravity IDE의 **Customization System**은 코드 수정 없이 마크다운 문서만으로 에이전트의 작동 방식, 코딩 컨벤션, 전문 수행 절차를 제어하는 강력한 프롬프트 오케스트레이션 기능입니다.

> 💡 **Module 1~2와의 대조**: 앞선 모듈 1~2(MCP & LinkedIn API)가 에이전트에게 외부 세상과 연결하는 **'손과 발(Tools)'**을 달아준 것이라면, 이번 모듈 3의 Customization은 에이전트가 지켜야 할 **'상시 규칙(AGENTS.md)'과 '전문 업무 지침(SKILL.md)'**을 뇌에 탑재하는 파트입니다.

Antigravity 시스템은 크게 **상시 전역 규칙(`AGENTS.md`)**과 **동적 커스텀 스킬(`SKILL.md`)**이라는 두 가지 축으로 에이전트를 통제합니다.

---

## 📌 Part 1: 전역 상시 규칙 (AGENTS.md)

### 1. `AGENTS.md` 란?
`AGENTS.md`는 에이전트가 작동할 때 **가장 먼저 읽어서 대화 내내 시스템 프롬프트(System Prompt) 버퍼에 고정(Pin)해 두고 들고 가는 '상시 행동 규칙서'**입니다.

### 2. 위치 및 적용 범위 (Customization Roots)
* **Global Rules (모든 프로젝트 범용 적용)**:
  * 경로: `C:\Users\<사용자명>\.gemini\config\AGENTS.md`
* **Workspace Rules (현재 프로젝트에만 적용)**:
  * 경로: 프로젝트 루트 아래 **[.agents/AGENTS.md](file:///c:/Coding/AI-Engineering/.agents/AGENTS.md)**

### 3. 실제 작성 예시 ([.agents/AGENTS.md](file:///c:/Coding/AI-Engineering/.agents/AGENTS.md))
```markdown
# 🤖 Antigravity Workspace Global Rules

## 📌 전역 개발 수칙
1. **언어 정책**: 모든 대화 답변, 주석, 문서화는 정중한 한글로 작성합니다.
2. **코드 스타일**: Python 코드는 PEP 8 표준(snake_case 변수/함수명, PascalCase 클래스명)을 엄격히 준수합니다.
3. **안전한 예외 처리**: 포괄적인 `except Exception:` 캐칭을 피하고 구체적인 예외 클래스를 사용합니다.
4. **자동화 검증**: 코드 수정 후에는 관련 검사 스크립트나 테스터를 실행하여 동작을 검증합니다.
```

---

## 🧠 Part 2: 동적 커스텀 스킬 (Custom Skills & SKILL.md)

### 1. `SKILL.md` 란?
특정 업무(예: 코드 리뷰, DB 마이그레이션, UI 테스트 등)를 수행할 때 필요한 **전문 작업 지침서**입니다.

### 2. 동적 탐색 (Auto-Discovery) & On-Demand 로딩
모든 지침을 `AGENTS.md`에 넣어두면 컨텍스트 메모리(토큰)가 낭비됩니다. 반면 `SKILL.md`는 평소에는 상단 메타데이터 요약(`name`, `description`)만 가볍게 들고 다니다가, 사용자가 관련 명령을 지시하면 **그 순간 필요한 스킬의 본문만을 컨텍스트 윈도우에 동적으로 불러옵니다.**

### 3. 스킬의 폴더 구조
```
.agents/skills/review-code/
├── SKILL.md                 <-- 메인 지침서 (YAML Frontmatter + 가이드라인)
├── scripts/                 <-- 🛠️ (선택) 에이전트가 실행할 헬퍼 스크립트
├── examples/                <-- 💡 (선택) 모범 개발 코드 예제
└── references/              <-- 📚 (선택) 500줄을 초과하는 대형 참조용 명세나 API 문서
```

### 4. 헬퍼 자원 3종 구성 요소
* **`scripts/` ([scripts/check_style.py](file:///c:/Coding/AI-Engineering/.agents/skills/review-code/scripts/check_style.py))**: LLM 추론 오차를 줄이고 정적 검사를 0.1초 만에 수행하는 유틸리티 파이썬/쉘 스크립트.
* **`examples/` ([examples/good_python_sample.py](file:///c:/Coding/AI-Engineering/.agents/skills/review-code/examples/good_python_sample.py))**: 에이전트에게 지향하는 모범 코드 구현 패턴을 보여주는 예시.
* **`references/` ([references/pep8_summary.md](file:///c:/Coding/AI-Engineering/.agents/skills/review-code/references/pep8_summary.md))**: `SKILL.md` 본문이 500줄을 넘어가는 것을 막기 위해 분리한 세부 명세서.

### 5. 🔍 스킬 동적 탐색(Auto-Discovery) & 4단계 매칭 알고리즘

AI IDE 백그라운드 오케스트레이터가 사용자의 질문을 받아 스킬을 주입하는 **4단계 내부 동작 파이프라인**입니다:

```text
[1단계: 인덱싱 (Indexing)]
  └─► IDE 시동 시 .agents/skills/ 하위 SKILL.md의 YAML Frontmatter(name, description)만 0.001초 만에 인덱싱 (본문 미포함, 토큰 0% 소모)

[2단계: 의도 매칭 (Intent Matching)]
  └─► 사용자 질문("로그인 기능 추가하고 커밋 메시지 짜줘") 수신
  └─► IDE Router가 질문 키워드/의도와 등록된 description("한국어 규칙 및 멀티라인 표준 준수 커밋 메시지 스킬") 간 유사도 분석 -> commit-msg 스킬 🎯 매칭!

[3단계: 동적 본문 주입 (Dynamic Injection)]
  └─► 매칭된 commit-msg/SKILL.md 본문 전문을 읽어서 LLM 'Triggered Custom Skills' 컨텍스트 영역으로 동적 주입!

[4단계: 서브 자원 지연 실행 (Deferred Execution)]
  └─► SKILL.md 지침에 따라 scripts/ 정적 파서를 실행하고, 필요 시 references/ 보조 문서를 추가 로드!
```

#### 💡 `SKILL.md` Frontmatter 작성 실전 꿀팁
스킬 발동률을 100%로 높이려면 `description`에 사용자의 **의도, 목적, 대상 키워드**를 구체적으로 작성해야 합니다:
* ❌ **모호한 작성**: `description: "코드 리뷰 스킬"` (매칭 실패 위험 높음)
* ⭕ **명확한 작성**: `description: "Python 코드 스타일, PEP 8 준수, docstring 누락 및 예외 처리를 검사하고 한글 코드 리뷰 보고서를 작성하는 가이드라인 스킬"`

---

## 🔄 Part 3: AGENTS.md vs SKILL.md 비교 & 메모리 전략

AI IDE의 5대 컨텍스트 조립 파이프라인([00_context_engineering.md](file:///c:/Coding/AI-Engineering/materials/00_context_engineering.md))에서 `AGENTS.md`와 `SKILL.md`는 토큰 예산 관리의 중심 축입니다.

| 구분 | **`AGENTS.md` (전역 규칙)** | **`SKILL.md` (커스텀 스킬)** |
| :--- | :--- | :--- |
| **주요 역할** | **모든 대화에 공통 적용되는 뼈대 수칙** | **특정 태스크 수행을 위한 전문 가이드라인** |
| **로딩 방식** | **상시 로딩 (Always Pinned in Memory)** | **동적 호출 (On-Demand Loaded)** |
| **컨텍스트 영향** | 상시 메모리를 차지하므로 핵심 규칙 위주 요약 | 필요 시만 불러오므로 토큰 효율성 극대화 |
| **비유** | 회사 사규 / 기본 근무 수칙 | 특수 업무 매뉴얼 / 장비 가이드 |

### 🛠️ 에이전트 실행 시 메모리 로딩 시퀀스

```text
[에이전트 구동]
       │
       ▼
 1. AGENTS.md 읽기 ──► (System Prompt 메모리에 상시 고정!)
       │
       ▼
 2. 사용자 질문 수신 ("이 코드 리뷰해줘")
       │
       ▼
 3. SKILL.md 요약 탐색 ──► review-code 스킬 매칭 감지!
       │
       ▼
 4. SKILL.md 본문 읽기 ──► (필요한 순간에만 컨텍스트에 동적 로드!)
       │
       ▼
 5. scripts/check_style.py 실행 후 최종 결과 보고서 작성
```

---

## ⚡ Part 4: Antigravity 생산성 슬래시 명령어 (Slash Commands)

Antigravity IDE 대화창에서 `/`를 입력하면 에이전트의 작동 모드를 즉시 전환하거나 특수 태스크를 수행할 수 있는 4가지 핵심 슬래시 명령어를 제공합니다.

| 명령어 | 기능명 | 설명 및 사용처 |
| :--- | :--- | :--- |
| **`/goal`** | **목표 자율 달성 모드** | 목표가 100% 완료될 때까지 에이전트가 멈추지 않고 생각-실행-테스트 루프를 자율 전개 (장시간 작업 시 사용) |
| **`/schedule`** | **타이머 & 크론 예약** | 일회성 알람 타이머 설정 또는 주기적인 정기 모니터링 태스크(Cron Job) 구동 |
| **`/grill-me`** | **인터뷰 조율 모드** | 에이전트가 개발자에게 1:1로 질의응답을 던지며 요구사항 및 아키텍처 결정을 점진적으로 정렬 |
| **`/learn`** | **노하우 자동 스킬화** | 해결된 버그 수정법이나 사용자의 교정 사항을 `SKILL.md` 또는 `AGENTS.md` 파일로 자동 추출하여 영구 기억 |

---

## 🏋️ 실습 예제 따라하기

이 모듈과 연계되는 전역 규칙 및 커스텀 스킬은 다음 위치에 생성되어 있습니다:
* 프로젝트 규칙: [.agents/AGENTS.md](file:///c:/Coding/AI-Engineering/.agents/AGENTS.md)
* 커스텀 스킬 1 (코드 리뷰): [.agents/skills/review-code/SKILL.md](file:///c:/Coding/AI-Engineering/.agents/skills/review-code/SKILL.md)
* 커스텀 스킬 2 (커밋 메시지): [.agents/skills/commit-msg/SKILL.md](file:///c:/Coding/AI-Engineering/.agents/skills/commit-msg/SKILL.md)

### 실습 절차
1. [.agents/AGENTS.md](file:///c:/Coding/AI-Engineering/.agents/AGENTS.md) 파일을 열어 상시 고정되는 전역 개발 수칙을 확인합니다.
2. [.agents/skills/review-code/SKILL.md](file:///c:/Coding/AI-Engineering/.agents/skills/review-code/SKILL.md) 및 [.agents/skills/commit-msg/SKILL.md](file:///c:/Coding/AI-Engineering/.agents/skills/commit-msg/SKILL.md)를 열어 스킬 메타데이터와 작성 규격을 살펴봅니다.
3. 에이전트 대화창에 다음과 같이 지시하여 커스텀 스킬의 반응을 테스트합니다:
   * 💬 *"이 워크스페이스에 있는 python 코드에 대해 코드 리뷰를 해줘"* ➔ `review-code` 스킬 자동 로드
   * 💬 *"로그인 기능 추가하고 문서 정리한 내용으로 커밋 메시지 작성해줘"* ➔ `commit-msg` 스킬 자동 로드 (멀티라인 `-m` 및 7대 Type 포맷 준수 확인)
