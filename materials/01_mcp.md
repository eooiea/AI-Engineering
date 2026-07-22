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
   *   `SSE (Server-Sent Events) / HTTP`: 웹 서비스나 원격 통신을 위해 사용.

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

## 🧠 딥다이브: LLM과 Host의 정체 및 본질

### Q1. Host도 AI인가요? LLM은 정말 글(텍스트)만 뱉나요?
* **LLM (GenAI 모델)**: **100% 텍스트(글)만 주고받는 신경망 모델**입니다. LLM은 스스로 내 컴퓨터에 파일을 생성하거나 파이썬 코드를 실행할 수 있는 손발이 전혀 없습니다.
* **MCP Host (Antigravity/Cursor)**: **AI가 아니라 일반적인 소프트웨어(프로그램)**입니다. 스스로 판단하는 지능이 없기 때문에 LLM을 '뇌'로 빌려 써서 사용자의 요청을 처리하는 **손과 발(운영자)** 역할을 합니다.

```
┌─────────────────────────┐
│     LLM (Gemini 등)     │ ◄── 🧠 100% 글자만 쓰는 천재 작전 참모 (타자기만 보유)
└────────────┬────────────┘     
             │ (텍스트 대화)
             ▼
┌─────────────────────────┐
│  MCP Host (Antigravity) │ ◄── 👔 일반 소프트웨어 (작전 장교: 참모 글 읽고 실제 장비 조작)
└────────────┬────────────┘     
             │ (JSON-RPC 통신)
             ▼
┌─────────────────────────┐
│       MCP Server        │ ◄── 🛠️ 실제 장비 / 도구 (연장통: DB, 파일 시스템, 터미널)
└─────────────────────────┘     
```

### Q2. LLM의 출력을 100% 통제하는 3가지 기술
과거에는 LLM이 JSON을 뱉으면서 `Sure! Here is the JSON:` 같은 사족을 붙여 파싱 오류가 자주 발생했습니다. 최신 AI 시스템은 이를 다음 3가지 기술로 통제합니다:

1. **로짓 마스킹 (Grammar-based Decoding)**: LLM이 단어를 생성하는 엔진 단에서 JSON 규격에 맞지 않는 모든 단어의 생성 확률을 0%로 마스킹하여 사족 출력을 물리적으로 차단합니다.
2. **Native Function Calling (API 채널 분리)**: 응답 객체 내에서 일반 대화 텍스트와 도구 호출 객체(`tool_calls`)가 아예 다른 API 채널로 분리되어 전달됩니다.
3. **방어적 검증 및 Self-Correction (자가 수정)**: Pydantic/Zod 검증 실패 시, Host가 에러 메시지를 LLM에 다시 보냄으로써 LLM이 자가 수정을 거쳐 올바른 인자를 다시 제출하도록 합니다.

---

## 🔑 MCP 서버의 3대 핵심 개념

MCP 서버는 Host에게 다음 세 가지 주요 자원을 제공할 수 있습니다.

| 자원 종류 | 설명 | 호출 주체 | 비유 |
| :--- | :--- | :--- | :--- |
| **Tools (도구)** | 에이전트가 직접 실행하여 부수 효과(Side Effect)를 일으키는 함수. | LLM (에이전트가 판단하여 호출) | 쓰기 권한이 있는 API |
| **Resources (리소스)** | 에이전트가 참고할 수 있는 정적/동적 데이터 (읽기 전용). | 에이전트 / 사용자 | 데이터베이스 조회, 파일 읽기 |
| **Prompts (프롬프트)** | 미리 설정된 템플릿화된 지시문 또는 대화 스타터. | 사용자 | 챗 템플릿 |

### 📝 도구 설명서(Docstring)와 LLM의 선택 메커니즘
개발자가 파이썬 코드 안의 **독스트링(`"""..."""`)**에 함수의 역할을 작성하면, FastMCP가 이를 긁어와 JSON Schema의 `description` 필드로 만듭니다. LLM은 사용자의 질문을 받았을 때 이 `description`을 읽고 도구 호출 여부를 스스로 판단합니다.

---

## ⚙️ `mcp_config.json` vs `AGENTS.md` (설정 파일 비교)

| 구분 | **`mcp_config.json`** | **`AGENTS.md` / `CLAUDE.md`** |
| :--- | :--- | :--- |
| **목적** | **외부 도구(Tool) 연결 및 백그라운드 구동** | **AI 에이전트 작업 규칙 및 코딩 컨벤션 지정** |
| **읽는 주체** | **IDE (컴퓨터 프로그램)** | **AI (LLM 모델)** |
| **포맷** | JSON 구조체 (`"command": "python" ...`) | 마크다운 텍스트 (`# 규칙 ...`) |
| **비유** | 외부 장비 연결 설정 / 자동 등록증 | 업무 수칙 / 회사 사규 문서 |

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

이 모듈과 연계되는 실습 파일은 [examples/mcp_server.py](file:///c:/Coding/AI-Engineering/examples/mcp_server.py) 및 [mcp_config.json](file:///c:/Coding/AI-Engineering/mcp_config.json)에 생성되어 있습니다.

### 🚀 상세 실습 단계별 가이드

#### 1단계: 패키지 설치
MCP 서버를 빠르게 빌드하기 위해 `fastmcp` 패키지를 설치합니다.
```bash
pip install fastmcp
```

#### 2단계: Python 서버 코드 가동 검증
작성한 [mcp_server.py](file:///c:/Coding/AI-Engineering/examples/mcp_server.py) 코드에 문법 오류가 없는지 실행해 봅니다.
```bash
python examples/mcp_server.py
```
* `stdio` 전송 방식이므로 실행 후 대기 상태가 되는 것이 정상입니다. (`Ctrl + C`로 종료)

#### 3단계: FastMCP Dev 디버거로 도구 사전 테스트 (선택 사항)
`fastmcp dev inspector` 명령을 사용하면 IDE에 연동하기 전에 브라우저 인스펙터 화면에서 등록된 도구들을 직접 클릭하여 테스트할 수 있습니다.
```bash
fastmcp dev inspector examples/mcp_server.py
```
* 터미널의 `Ok to proceed?` 물음에 `y`를 누르고 엔터를 칩니다.
* 브라우저 웹 화면(`localhost:6274`)에서 좌측 하단 **`▷ Connect`** 버튼을 누른 후 `Tools` 탭에서 함수들을 호출해 봅니다.

#### 4단계: IDE (Antigravity) 설정 파일 연동 (`mcp_config.json`)
Antigravity IDE 프로젝트 최상위 루트에 `mcp_config.json` 파일을 작성하여 서버를 `stdio` 방식으로 등록합니다.

**`mcp_config.json` 예시:**
```json
{
  "mcpServers": {
    "system-utility-server": {
      "command": "python",
      "args": [
        "c:/Coding/AI-Engineering/examples/mcp_server.py"
      ]
    }
  }
}
```

#### 5단계: 에이전트 도구 자동 감지 및 대화 테스트
IDE 대화창에서 아래와 같이 질문하여 커스텀 MCP 도구가 자동으로 호출되는지 확인합니다:
* **질문 1**: *"현재 내 PC의 OS 정보와 파이썬 버전을 알려줘"* ➔ `get_system_info()` 도구 자동 실행
* **질문 2**: *"서울 날씨 어때?"* ➔ `get_mock_weather(city="seoul")` 도구 자동 실행
