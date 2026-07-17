# 🔌 Module 1: Model Context Protocol (MCP)

Model Context Protocol (MCP)는 **AI 애플리케이션(Client/Host)**과 **외부 시스템/데이터 소스(Server)** 간의 안전하고 표준화된 연결을 제공하기 위해 Anthropic에 의해 제안된 오픈 소스 표준 프로토콜입니다.

AI 업계에서는 이를 **"AI 시대를 위한 USB-C 포트"**라고도 부릅니다. 과거에는 각 IDE나 챗봇마다 개별 데이터베이스나 API 연동 모듈을 별도로 짜야 했으나, MCP를 사용하면 표준 규격 하나로 다양한 AI 모델에 연결할 수 있습니다.

---

## 🏛️ MCP 아키텍처

MCP는 크게 세 가지 구성 요소로 작동합니다.

1. **MCP Host (Client)**: 사용자의 에이전트 인터페이스(예: Antigravity IDE, Claude Desktop, Cursor 등). 서버에 작업(도구 실행)을 요청하고 데이터를 수신합니다.
2. **MCP Server**: 실제로 비즈니스 로직을 수행하고 데이터를 노출하는 가볍고 격리된 프로세스. 데이터베이스, API, 파일 시스템 등을 캡슐화합니다.
3. **Transport (전송 계층)**: JSON-RPC 2.0 규격 메시지가 Host와 Server 사이에 오가는 통로.
   *   `stdio`: 로컬 컴퓨터의 표준 입출력을 활용한 서브프로세스 기반 통신 (대부분의 로컬 IDE 플러그인에 사용).
   *   `SSE (Server-Sent Events) / HTTP`: 웹 서비스나 원기기 통신을 위해 사용.

```
┌──────────────────┐               JSON-RPC 2.0               ┌──────────────────┐
│  MCP Host (IDE)  │  ◄─────────────────────────────────────►  │    MCP Server    │
└────────┬─────────┘              (stdio / SSE)               └────────┬─────────┘
         │                                                             │
         ▼                                                             ▼
┌──────────────────┐                                          ┌──────────────────┐
│   Gemini Model   │                                          │ PostgreSQL, Git, │
│  (Reasoning Loop)│                                          │  Local Terminal  │
└──────────────────┘                                          └──────────────────┘
```

---

## 🔑 MCP 서버의 3대 핵심 개념

MCP 서버는 Host에게 다음 세 가지 주요 자원을 제공할 수 있습니다.

| 자원 종류 | 설명 | 호출 주체 | 비유 |
| :--- | :--- | :--- | :--- |
| **Tools (도구)** | 에이전트가 직접 실행하여 부수 효과(Side Effect)를 일으키는 함수. | LLM (에이전트가 판단하여 호출) | 쓰기 권한이 있는 API |
| **Resources (리소스)** | 에이전트가 참고할 수 있는 정적/동적 데이터 (읽기 전용). | 에이전트 / 사용자 | 데이터베이스 조회, 파일 읽기 |
| **Prompts (프롬프트)** | 미리 설정된 템플릿화된 지시문 또는 대화 스타터. | 사용자 | 챗 템플릿 |

---

## 🐍 Python FastMCP로 구축하기

`fastmcp` 패키지를 이용하면 데코레이터 방식으로 단 몇 줄의 코드로 MCP 서버를 빌드할 수 있습니다.

### 1. 도구(Tool) 추가
```python
from fastmcp import FastMCP

mcp = FastMCP("My MCP Server")

@mcp.tool()
def add_numbers(a: int, b: int) -> int:
    """두 숫자를 더합니다."""
    return a + b
```

### 2. 리소스(Resource) 추가
```python
@mcp.resource("system://metrics")
def get_metrics() -> str:
    """시스템 리소스 지표를 조회합니다."""
    return "CPU: 23%, Memory: 45%"
```

### 3. 프롬프트(Prompt) 추가
```python
@mcp.prompt()
def code_refactor_template(code: str) -> str:
    """코드 리팩토링 지시 템플릿을 생성합니다."""
    return f"다음 코드를 PEP 8 표준에 맞게 리팩토링해줘:\n\n{code}"
```

---

## 🏋️ 실습 예제 따라하기

이 모듈과 연계되는 실습 파일은 [examples/mcp_server.py](file:///c:/Users/majun/Coding/anti/examples/mcp_server.py)에 생성되어 있습니다.

### 실습 절차
1. 로컬 환경에서 MCP 서버가 정상 작동하는지 python으로 실행하여 구문을 확인합니다.
2. `fastmcp dev` 도구를 사용하여 CLI 디버거 환경을 띄웁니다.
3. Antigravity IDE 설정 파일인 `mcp_config.json`에 해당 서버의 경로(`stdio` 전송 방식)를 설정해 봄으로써 실제로 에이전트의 도구 목록에 내가 만든 커스텀 도구가 노출되는 것을 확인합니다.
