# 🐏 Module 6: Ollama Local Agent Collaboration

최근 AI 엔지니어링 생태계의 주요 트렌드 중 하나는 **개인 정보 보호(Privacy)**, **무상 유지 비용(No token costs)**, 그리고 **인터넷 독립성(Offline operation)**을 위해 **로컬 LLM**을 구축하여 에이전트를 구동하는 것입니다.

**Ollama**는 로컬 PC에서 Llama 3, Qwen 2.5, Gemma 2 등 업계 최고 수준의 오픈 가중치 모델들을 손쉽게 띄우고 서빙할 수 있도록 돕는 대표적인 도구입니다.

---

## 🛠️ Ollama 설치 및 qwen2.5-coder 로드

### 1. Ollama 설치
*   공식 웹사이트([ollama.com](https://ollama.com))에서 본인의 운영체제(Windows, macOS, Linux)에 맞는 클라이언트를 다운로드하여 설치합니다.
*   설치가 끝나면 터미널(CMD, PowerShell)에서 `ollama` 명령어가 정상 동작하는지 확인합니다.

### 2. qwen2.5-coder 모델 다운로드 및 실행
*   코딩 및 구조적 추론에서 강점을 발휘하는 Alibaba의 **Qwen 2.5 Coder** 모델(주로 1.5B, 7B, 14B, 32B 중 가벼운 모델 권장)을 내려받습니다:
    ```bash
    ollama run qwen2.5-coder
    ```
*   명령어가 실행되면 모델 가중치가 백그라운드에 자동으로 적재되며 로컬 API 서빙 포트(`http://localhost:11434`)가 활성화됩니다.

---

## 🐍 공식 `ollama` Python SDK 활용

파이썬 환경에서 Ollama를 가장 간편하게 다루는 방법은 공식 `ollama` 패키지를 사용하는 것입니다:
```bash
pip install ollama
```

### 1. 기본적인 채팅 호출
```python
import ollama

response = ollama.chat(
    model='qwen2.5-coder',
    messages=[
        {'role': 'user', 'content': '파이썬으로 구구단 출력 함수 작성해줘.'}
    ]
)
print(response['message']['content'])
```

---

## 🎻 로컬 개발자 협업 (Coder + Validator) 아키텍처

Module 6의 실습 예제인 [ollama_orchestrator.py](file:///c:/Coding/AI-Engineering/examples/ollama_orchestrator.py)는 두 로컬 에이전트의 피드백 루프를 모방하여 완결성 높은 소스코드를 점진적으로 빌드해 냅니다.

```
                    ┌────────────────────────┐
                    │      사용자 미션       │
                    └───────────┬────────────┘
                                │
                                ▼
                    ┌────────────────────────┐
                    │       CoderAgent       │ ◄───────┐ (피드백 수신)
                    │  (1차 파이썬 코드 작성) │         │
                    └───────────┬────────────┘         │
                                │ (코드 전달)          │
                                ▼                      │
                    ┌────────────────────────┐         │
                    │     ValidatorAgent     │ ────────┘
                    │   (버그/예외 처리 검증) │
                    └───────────┬────────────┘
                                │ (완성 후 합성)
                                ▼
                    ┌────────────────────────┐
                    │  최종 검증된 파이썬 코드 │
                    └────────────────────────┘
```

### 1. `CoderAgent`
*   **지침**: 코드를 생성하는 전담 프로그래머. 오직 파이썬 구문과 임포트 모듈만 선언하며 다른 설명은 덧붙이지 않습니다.
*   **대응**: 1차 작성 후 Validator가 보낸 피드백 지적 사항들을 인지하여 코드를 한 단계 더 정교하게 리팩토링합니다.

### 2. `ValidatorAgent`
*   **지침**: 작성된 코드를 까다롭게 검증하는 QA 엔지니어. 코드 내 잠재적인 버그(예: ZeroDivision, 예외 캐싱 누락), 가독성, 하드코딩 여부를 검사하고 피드백 목록을 반환합니다.

---

## 🏋️ 실습 예제 따라하기

이 모듈과 연계되는 실습 파일은 [examples/ollama_orchestrator.py](file:///c:/Coding/AI-Engineering/examples/ollama_orchestrator.py)에 구성되어 있습니다.

### 실습 절차
1. 로컬 환경에 Ollama를 켜고 `ollama run qwen2.5-coder` 명령어로 모델을 준비합니다.
2. 터미널 창을 열고 `python examples/ollama_orchestrator.py`를 실행합니다.
3. **만약 로컬에 Ollama가 설치되어 있지 않거나 qwen2.5-coder가 로드되지 않은 상태라면**, 스크립트가 자동으로 예외를 감지하여 내장된 가상(Mock) 협업 대화 리포트를 터미널에 출력합니다.
4. 로컬 모델이 구동 중이라면, 실제로 두 개의 에이전트가 Ollama 모델을 교대로 호출하며 대화하고 피드백을 전달하여 코드가 스스로 개선되는 과정을 직접 모니터링할 수 있습니다.
