# 🔌 Module 1: Model Context Protocol (MCP) Mastery

Model Context Protocol (MCP)는 **AI 애플리케이션(Client/Host)**과 **외부 시스템/데이터 소스(Server)** 간의 안전하고 표준화된 양방향 통신을 제공하기 위해 제안된 오픈 표준 프로토콜입니다.

> 💡 **AI 시대를 위한 USB-C 포트**: 각 AI 플랫폼마다 DB나 API 연동 모듈을 별도로 짜던 과거 방식에서 벗어나, 표준 JSON-RPC 2.0 규격 하나로 다양한 AI 모델과 엔터프라이즈 리소스를 연결합니다.

---

## 🏛️ 1. MCP 3대 핵심 프리미티브 (Primitives)

MCP 서버는 단순히 "함수(Function)"만 노출하는 것이 아니라, 다음 세 가지 표준 데이터 프리미티브를 제공합니다.

```text
┌─────────────────────────────────────────────────────────────┐
│                     MCP Server Primitives                   │
├─────────────────┬─────────────────────────┬─────────────────┤
│ 1️⃣ Tools         │ 2️⃣ Resources             │ 3️⃣ Prompts       │
│ (동적 실행 함수) │ (정적/실시간 데이터 소스)│ (사전 정의 템플릿)│
│ - side-effects  │ - read-only MIME data   │ - reusable UI   │
│ - run_query()   │ - file://, db:// schema │ - slash commands│
└─────────────────┴─────────────────────────┴─────────────────┘
```

1. **Tools (도구)**: 모델이 제어권을 가지고 호출하여 Side-Effect(파일 생성, DB 갱신, API 호출)를 일으키는 실행 함수입니다.
2. **Resources (리소스)**: 파일, 데이터베이스 스키마, 로그 스트림 등 모델이나 호스트가 **읽기 전용(Read-Only)**으로 컨텍스트에 부착할 수 있는 정적/동적 데이터입니다. (URI 기반 식별)
3. **Prompts (프롬프트)**: 서버 개발자가 사전에 설계한 재사용 가능한 대화 템플릿 또는 슬래시 커맨드 워크플로우입니다.

---

## 🚀 2. 전송 계층 비교: `stdio` vs `SSE (Server-Sent Events)`

```text
[1. Local Subprocess (stdio)]
Host (IDE) ── (stdin / stdout 파이프) ──► 로컬 MCP 프로세스 (Python / Node)
- 특징: 로컬 컴퓨터 내부 초고속 IPC 통신, 인증 불필요, 로컬 IDE 플러그인에 최적화.

[2. Remote Web Service (SSE / HTTP)]
Host (IDE) ── (HTTP POST / SSE Stream) ──► 클라우드 원격 MCP 마이크로서비스
- 특징: 사내 중앙 집중식 DB/API 게이트웨이 연동, 분산 환경 확장성, Bearer Token / OAuth 인증 필요.
```

---

## 🛡️ 3. 프로덕션 MCP 엔지니어링 수칙

1. **엄격한 에러 핸들링**: MCP Tool 실행 실패 시 스택트레이스를 그대로 터뜨리지 않고, LLM이 이해하고 대안을 찾을 수 있는 정형화된 JSON 에러 메시지 반환.
2. **타임아웃 및 재연결(Reconnection)**: 외부 API 지연 시 무한 블로킹을 방지하기 위한 타임아웃(예: 10초) 및 네트워크 순단 시 지수 백오프(Exponential Backoff) 재연결.
3. **Multi-Server Aggregation**: 호스트 환경에서 여러 개의 MCP 서버(`db-server`, `git-server`, `slack-server`)를 동시에 등록하고 네임스페이스(`server_name.tool_name`)로 격리 관리.

---

## 🏋️ 실습 예제 따라하기

이 모듈과 연계되는 파이썬 실습 코드 파일은 [examples/01_mcp_server.py](file:///c:/Coding/AI-Engineering/examples/01_mcp_server.py)에 작성되어 있습니다.

```bash
python examples/01_mcp_server.py
```
