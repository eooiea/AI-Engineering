# 🤖 Module 5: Antigravity SDK (google-antigravity)

**Google Antigravity SDK** (`google-antigravity`)는 에이전트형 개발 플랫폼인 Antigravity의 자율 추론 엔진 및 도구(Tool) 실행 프레임워크를 개발자가 자신의 Python 애플리케이션에 직접 임포트하여 제어할 수 있게 돕는 공식 라이브러리입니다.

IDE나 CLI 화면을 거치지 않고 백엔드 데몬, 스크립트, 혹은 자동화 파이프라인에서 파일 수정, 터미널 실행, 에이전트 대화를 백프로그래밍 방식으로 오케스트레이션할 수 있습니다.

---

## 🏛️ SDK 핵심 구성 요소

`google-antigravity` 라이브러리의 핵심 API는 다음과 같습니다.

### 1. `google.antigravity.Agent`
*   에이전트 인스턴스를 관리하며 실질적인 대화 루프(`chat`)를 처리합니다.
*   비동기 컨텍스트 매니저(`async with Agent(config) as agent:`) 방식을 사용해 리소스를 안전하게 해제합니다.

### 2. `google.antigravity.LocalAgentConfig`
*   에이전트가 로컬 환경에서 실행되는 방식을 지정합니다.
*   에이전트가 접근 가능한 기본 디렉토리(Workspace), 사용할 모델(Gemini 3.5), 권한 검증 수준 및 프롬프트 가이드라인을 세팅합니다.

### 3. Unified Tools & Safety Policies
*   에이전트는 기본적으로 파일 I/O(읽기/쓰기/찾기), CLI 명령 실행 등의 도구 집합을 가지고 있습니다.
*   이 도구들은 **"기본 거부(Deny-by-default)"**의 안전 정책을 따르며, 위험한 셸 명령이나 지정 폴더 외부 쓰기 등이 시도되면 사용자 승인을 요청하는 차단 제어 장치가 작동합니다.

---

## 💻 기본 코드 패턴

```python
import asyncio
from google.antigravity import Agent, LocalAgentConfig

async def main():
    # 1. 에이전트 설정 인스턴스 생성
    config = LocalAgentConfig()
    
    # 2. 에이전트 세션 오픈 (비동기)
    async with Agent(config) as agent:
        # 3. 에이전트에 자율적 작업 지시
        response = await agent.chat("현재 디렉토리에서 가장 큰 파일 이름을 찾아줘.")
        
        # 4. 결과 출력
        print("에이전트 답변:")
        print(await response.text())

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 🏋️ 실습 예제 따라하기

이 모듈과 연계되는 실습 파일은 [examples/sdk_agent.py](file:///c:/Users/majun/Coding/anti/examples/sdk_agent.py)에 생성되어 있습니다.

### 실습 절차
1. [examples/sdk_agent.py](file:///c:/Users/majun/Coding/anti/examples/sdk_agent.py) 파일을 열어 SDK 패키지를 임포트하여 에이전트를 생성하는 전체 소스코드를 살펴봅니다.
2. 터미널 창을 열고 `python examples/sdk_agent.py` 명령을 실행합니다.
3. 로컬 에이전트가 정상적으로 구동되고, 로컬 Workspace 컨텍스트를 파악해 응답하는 과정을 콘솔 화면에서 확인합니다.
