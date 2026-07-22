# 🌐 Module 2: Advanced MCP - LinkedIn & External API Integration

**Module 1**에서 배운 기본 MCP (Model Context Protocol) 개념을 바탕으로, 이번 모듈에서는 **외부 상용 REST API 및 소셜 플랫폼(LinkedIn)과 연동하는 고급 MCP 실전 아키텍처**를 다룹니다.

---

## 🏛️ 외부 API 연동 MCP 아키텍처 (OAuth 2.0 & Tool Invocation)

```text
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐       ┌──────────────────┐
│  User Request   │ ──►  │    MCP Host     │ ──►  │  LinkedIn MCP   │ ──►  │   LinkedIn API   │
│ ("포스팅 올리기") │       │ (Payload 합성)  │       │ (Tool Executer) │       │ (REST / ugcPost) │
└─────────────────┘       └─────────────────┘       └─────────────────┘       └──────────────────┘
```

1. **User Prompt**: 사용자가 *"현재 워크스페이스 소식을 LinkedIn에 올리고 싶어"*라고 지시.
2. **MCP Host (IDE)**: 사용자의 지시와 최신 커리큘럼 상태를 합성하여 MCP Tool (`linkedin_create_post`)을 호출.
3. **LinkedIn MCP Server**: OAuth 2.0 Access Token을 활용하여 요청을 검증하고 LinkedIn REST API 포맷으로 변환.
4. **LinkedIn API Server**: `/v2/ugcPosts` 또는 `/v2/posts` 엔드포인트를 호출하여 포스팅을 정상 게재.

---

## 🔑 보안 및 인증 수칙 (OAuth 2.0 & Token Safety)

* **Access Token 격리**: LinkedIn API 억세스 토큰은 소스 코드에 직접 하드코딩하지 않고, 환경 변수(`LINKEDIN_ACCESS_TOKEN`) 또는 `mcp_config.json` 내의 보안 `env` 블록으로 분리 관리합니다.
* **Rate Limit 방어**: 불필요한 연쇄 포스팅 방지를 위해 에이전트가 포스팅 전 최종 마크다운 프리뷰를 보여주고 사용자의 1차 확인(User Approval)을 거치도록 설계합니다.

---

## 🏋️ 실습 예제 따라하기

이 모듈과 연계되는 파이썬 실습 코드 파일은 [examples/linkedin_mcp_example.py](file:///c:/Coding/AI-Engineering/examples/linkedin_mcp_example.py)에 작성되어 있습니다.

### 실습 실행 방법
```bash
python examples/linkedin_mcp_example.py
```

### 코드 주요 포인트
* 마크다운 형식의 학습 노트/소식을 LinkedIn API 전용 JSON 페이로드 포맷으로 변환하는 변환기(Converter).
* MCP Tool을 가동하여 안전하게 외부 API를 호출하는 시뮬레이션 흐름 확인.
