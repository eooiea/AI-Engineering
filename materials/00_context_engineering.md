# 🧩 Module 0: AI IDE Architecture & Context Engineering

Modern Agentic IDE(Antigravity, Cursor 등)가 사용자의 단순한 질문 하나를 받아 어떻게 백그라운드에서 전체 컨텍스트 보따리를 조립하고, 외부 도구와 연동하며, **컨텍스트 윈도우(Context Window)**, **Prompt Caching(KV-Cache)**, 그리고 **Context Compaction**을 최적화하는지 다루는 **기초 아키텍처 및 컨텍스트 엔지니어링 교재**입니다.

---

## 🏛️ 1. AI IDE 3대 내부 구성 요소와 역할 분담

AI IDE는 단순한 챗봇이 아니라, 다음 세 가지 핵심 객체가 긴밀하게 협력하는 **복합 소프트웨어 아키텍처**입니다.

```text
┌─────────────────────────┐
│       Gemini LLM        │ ◄── 🧠 1. 추론 엔진 (100% 텍스트/JSON 입출력만 담당)
└────────────┬────────────┘
             │ (JSON-RPC / REST API)
             ▼
┌─────────────────────────┐
│     MCP Host (IDE)      │ ◄── 👔 2. 오케스트레이터/운영자 (컨텍스트 조립, 파이프라인 관리)
└────────────┬────────────┘
             │ (Subprocess stdio / Exec)
             ▼
┌─────────────────────────┐
│ Tools / Terminal / MCP  │ ◄── 🛠️ 3. 실행 환경 (실제 디스크, 파이썬, 터미널, DB 조작)
└─────────────────────────┘
```

1. **Gemini LLM (Reasoning Engine)**: 순수 신경망 추론 엔진입니다. 직접 파일을 열거나 터미널 명령을 수행할 수 있는 손발이 없으며, 오직 **텍스트(JSON)를 읽고 텍스트를 뱉는 역할**만 수행합니다.
2. **MCP Host (IDE - Antigravity)**: 전체 파이프라인의 **중계자이자 운영자**입니다. 사용자의 질문, 전역 규칙, 파일 상태, 터미널 로그를 긁어모아 LLM에 넘겨주고, LLM이 반환한 도구 실행 요청(Function Call)을 받아 **실제 컴퓨터 환경에 전달하는 핵심 주체**입니다.
3. **Tools & Execution Layer**: 실제 파이썬 스크립트, Git CLI, 파일 시스템, MCP 서버 등 **부수 효과(Side Effect)를 만드는 실질적인 작업 환경**입니다.

---

## 🧠 2. 컨텍스트 윈도우의 한계와 Prompt Caching

### 1) 대용량 컨텍스트 윈도우의 3대 치명적 한계
* **Lost in the Middle (중간 분실 현상)**: LLM의 Self-Attention 메커니즘 특성상 프롬프트의 맨 처음(Head)과 맨 끝(Tail)에 있는 정보는 잘 기억하지만, **중간에 위치한 대량의 코드는 무시하거나 놓치는 현상**이 발생합니다.
* **Context Rotting (컨텍스트 오염)**: 불필요한 로그나 전체 코드가 주입되면 어텐션 분포가 분산되어 **환각(Hallucination) 발현율이 급증**합니다.
* **비용 및 지연시간 폭증**: 토큰 수가 비례하여 증가할수록 API 호출 비용과 First-token Latency가 선형적으로 늘어납니다.

### 2) Prompt Caching (KV-Cache 최적화 원리)
최신 LLM Provider(Anthropic, Google Gemini, OpenAI)는 **프롬프트의 접두사(Prefix)가 일치할 경우 Key-Value Attention Tensor를 캐싱하여 재사용**합니다.
* **정적 컨텍스트(Static Context)**: `AGENTS.md`(시스템 규칙), API 스키마, 도구 정의 등 변경되지 않는 부분을 **프롬프트의 최상단(Prefix)**에 배치하여 90% 이상의 캐시 히트율(Cache Hit)을 달성하고 비용을 50~80% 절감합니다.
* **동적 컨텍스트(Dynamic Context)**: 사용자 입력, 직전 턴 실행 로그 등 매번 바뀌는 요소는 **프롬프트의 최하단**에 배치합니다.

---

## 📦 3. 컨텍스트 조립 파이프라인 (Context Packaging)

사용자가 대화창에 한 줄(예: *"깃에 push해줘"*)을 입력했을 때, Host(IDE)가 백그라운드에서 결합하는 **5대 컨텍스트 페이로드(Payload)** 구조입니다.

```text
┌──────────────────────────────────────────────────────────────────────────┐
│                         LLM 전송 컨텍스트 페이로드                        │
├──────────────────────────────────────────────────────────────────────────┤
│ 1️⃣ System Rules [Cacheable]                                              │
│    - AGENTS.md 내의 전역 개발 수칙 (한글 답변, PEP 8, 예외 처리 규칙 등)   │
├──────────────────────────────────────────────────────────────────────────┤
│ 2️⃣ Triggered Custom Skills [Cacheable]                                   │
│    - 사용자 지시어("push")로 자동 감지된 commit-msg/SKILL.md 가이드라인    │
├──────────────────────────────────────────────────────────────────────────┤
│ 3️⃣ Workspace State & Active Context                                      │
│    - 현재 열려 있는 활성 파일 내용, 커서 위치, 디렉토리 구조             │
├──────────────────────────────────────────────────────────────────────────┤
│ 4️⃣ Tool & Terminal Execution Logs                                        │
│    - 방금 실행한 `git status`, `git add .` 등의 터미널 실제 Output 로그  │
├──────────────────────────────────────────────────────────────────────────┤
│ 5️⃣ User Instruction (사용자 질문)                                         │
│    - "깃에 push해줘"                                                      │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ 4. `scripts/` 헬퍼 스크립트와 Context Compaction

컨텍스트 엔지니어링의 핵심 지혜는 **"LLM에게 원본 빅데이터 전체를 읽게 하지 않고, 결정론적(Deterministic) 파이썬 스크립트에게 전처리를 위임하는 것"**입니다.

### 1) 결정론적 전처리 (Deterministic Preprocessing)
```text
[나쁜 접근법 - 확률적 LLM에 전적으로 의존]
 소스 코드 2,000줄 주입 ──► LLM 추론 파싱 ──► 토큰 폭증 & 환각 위험 (Lost in the Middle!)

[우수한 컨텍스트 엔지니어링 - scripts/ 정적 헬퍼 결합]
 소스 코드 ──► scripts/check_style.py 실행 (0.01초 정적 파싱) ──► 10줄 요약 JSON ──► LLM 주입
```

### 2) Context Compaction (컨텍스트 압축 전략)
* **대화 히스토리 슬라이딩 윈도우**: 최근 N턴은 원문 유지, 오래된 대화는 중간 요약본(Summary Node)으로 치환.
* **도구 실행 로그 Truncation**: 수백 줄의 빌드/테스트 로그 중 에러 스택트레이스(Error Trace) 핵심 30줄만 추출하여 주입.

---

## 🏋️ 실습 예제 따라하기

이 모듈과 연계되는 파이썬 실습 코드 파일은 [examples/00_context_engineering_example.py](file:///c:/Coding/AI-Engineering/examples/00_context_engineering_example.py)에 작성되어 있습니다.

```bash
python examples/00_context_engineering_example.py
```
