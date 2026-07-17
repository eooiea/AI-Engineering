import os
import socket
import sys
import time

try:
    import ollama
    HAS_OLLAMA_LIB = True
except ImportError:
    HAS_OLLAMA_LIB = False

def check_ollama_running() -> bool:
    """로컬 11434 포트에 연결을 시도하여 Ollama 데몬이 떠 있는지 점검합니다."""
    try:
        socket.create_connection(("localhost", 11434), timeout=1.0)
        return True
    except OSError:
        return False

def check_model_installed(model_name: str) -> bool:
    """Ollama 서버 내에 원하는 모델이 다운로드되어 있는지 검사합니다."""
    if not HAS_OLLAMA_LIB:
        return False
    try:
        model_list = ollama.list()
        models = model_list.get("models", [])
        for m in models:
            name = m.get("model", "") or m.get("name", "")
            if model_name in name:
                return True
        return False
    except Exception:
        return False


class OllamaAgent:
    """Ollama 로컬 API를 호출하는 에이전트 클래스"""
    def __init__(self, role: str, system_instruction: str, model_name: str):
        self.role = role
        self.system_instruction = system_instruction
        self.model_name = model_name
        self.use_real_api = HAS_OLLAMA_LIB and check_ollama_running() and check_model_installed(model_name)

    def generate(self, user_prompt: str, chat_history=None) -> str:
        print(f"[{self.role}] 로컬 추론 작동 중...")
        time.sleep(1.2) # 로컬 실행 지연 묘사
        
        if self.use_real_api:
            try:
                messages = [{"role": "system", "content": self.system_instruction}]
                if chat_history:
                    messages.extend(chat_history)
                messages.append({"role": "user", "content": user_prompt})
                
                response = ollama.chat(model=self.model_name, messages=messages)
                return response["message"]["content"]
            except Exception as e:
                print(f"[{self.role}] API 호출 중 에러 발생: {e}. Mock 데이터로 대체합니다.")
                return self._get_mock_response(user_prompt)
        else:
            return self._get_mock_response(user_prompt)

    def _get_mock_response(self, prompt: str) -> str:
        """가상 응답 폴백 메서드 (자식 클래스에서 오버라이드)"""
        return ""


class CoderAgent(OllamaAgent):
    """지정된 요구사항에 맞춰 최적의 파이썬 코드를 작성하는 개발자 에이전트"""
    def __init__(self, model_name: str):
        super().__init__(
            role="Coder-Agent",
            system_instruction=(
                "You are an expert Python software developer. Write clean, PEP8 compliant code based on requirements. "
                "Output ONLY executable Python code blocks within ```python ... ```. Do not add conversational intro/outro text."
            ),
            model_name=model_name
        )

    def _get_mock_response(self, prompt: str) -> str:
        # 피드백 반영 유무에 따라 다른 Mock 코드 생성
        if "피드백" in prompt or "개선" in prompt or "수정" in prompt or "반영" in prompt:
            print(f"[{self.role}] (Mock) 피드백이 반영된 2차 코드 생성 완료")
            return (
                "```python\n"
                "from functools import lru_cache\n\n"
                "@lru_cache(maxsize=128)\n"
                "def fibonacci_cached(n: int) -> int:\n"
                "    \"\"\"피보나치 수열 캐싱 함수 (중복 계산 제거 및 음수 에러 핸들링 추가)\"\"\"\n"
                "    if not isinstance(n, int):\n"
                "        raise TypeError(\"인자는 반드시 정수여야 합니다.\")\n"
                "    if n < 0:\n"
                "        raise ValueError(\"음수 피보나치 수는 정의되지 않습니다.\")\n"
                "    if n == 0:\n"
                "        return 0\n"
                "    elif n == 1:\n"
                "        return 1\n"
                "    return fibonacci_cached(n - 1) + fibonacci_cached(n - 2)\n"
                "```"
            )
        else:
            print(f"[{self.role}] (Mock) 1차 초안 코드 작성 완료")
            return (
                "```python\n"
                "def fibonacci(n):\n"
                "    # 피보나치 기초 구현 (캐싱 및 예외 처리 누락)\n"
                "    if n <= 0:\n"
                "        return 0\n"
                "    elif n == 1:\n"
                "        return 1\n"
                "    return fibonacci(n - 1) + fibonacci(n - 2)\n"
                "```"
            )


class ValidatorAgent(OllamaAgent):
    """코더가 작성한 파이썬 코드를 정밀 감사(Audit)하여 지적 사항을 전달하는 에이전트"""
    def __init__(self, model_name: str):
        super().__init__(
            role="Validator-Agent",
            system_instruction=(
                "당신은 구글 출신의 수석 QA 엔지니어이자 코드 감사관입니다. 전달받은 파이썬 소스코드를 검토하고, "
                "1. 에러/예외 처리 누락, 2. 비효율적 알고리즘(중복 재귀 등), 3. 문서화(docstring) 상태를 분석하여 "
                "피드백 지적 사항들을 한글 번역 목록으로 출력하십시오. 만약 완벽하다면 단어 'PASS'만을 리턴하십시오."
            ),
            model_name=model_name
        )

    def _get_mock_response(self, prompt: str) -> str:
        if "lru_cache" in prompt or "cached" in prompt:
            print(f"[{self.role}] (Mock) 최종 코드 검증 통과 완료 (PASS)")
            return "PASS"
        else:
            print(f"[{self.role}] (Mock) 코드 지적 사항 및 피드백 도출 완료")
            return (
                "1. [비효율적 재귀]: 중복 호출이 많아 O(2^n)의 시간이 걸립니다. lru_cache나 메모이제이션 캐시를 적용하십시오.\n"
                "2. [예외 처리 미흡]: n에 음수가 들어오거나 정수가 아닐 때에 대한 에러 처리가 부재합니다.\n"
                "3. [문서화]: 함수의 동작과 리턴 타입을 설명하는 docstring이 없습니다."
            )


class OllamaOrchestrationPipeline:
    """두 로컬 에이전트 간의 개발-검증 오케스트레이션 제어 루프"""
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.coder = CoderAgent(model_name)
        self.validator = ValidatorAgent(model_name)

    def run(self, request_mission: str):
        print(f"\n[Master] Ollama 협업 에이전트 파이프라인 기동 (모델: {self.model_name})")
        
        # 1. Ollama 연결 상태 요약 인쇄
        real_run = self.coder.use_real_api and self.validator.use_real_api
        if real_run:
            print("[Master] 로컬 Ollama 데몬 및 모델 연동 감지 완료. 실시간 API 추론으로 동작합니다.")
        else:
            print("[Master] [Info] 로컬 Ollama 데몬 미구동 혹은 qwen2.5-coder 모델 미검출.")
            print("[Master] 사전 준비된 Mock 데이터 기반 협업 시뮬레이션 모드로 전환합니다.")
            
        print(f"\n[Master Step 1] Coder-Agent에게 파이썬 코드 작성을 요청합니다.")
        code_draft = self.coder.generate(f"요구사항: {request_mission}")
        print("\n" + "-"*30 + " 1차 작성된 코드 초안 " + "-"*30)
        print(code_draft)
        print("-" * 80)

        # 2. 검증 루프 시작 (최대 2회 반복 피드백 수렴)
        max_turns = 2
        current_code = code_draft
        
        for turn in range(1, max_turns + 1):
            print(f"\n[Master Step 2-Turn {turn}] Validator-Agent에게 코드 감사를 요청합니다.")
            feedback = self.validator.generate(f"검토할 코드:\n{current_code}")
            
            print(f"\n[Master] Validator 피드백 수신:\n{feedback}\n")
            
            # PASS 신호 검출 시 즉각 종료
            if "PASS" in feedback.upper().strip():
                print(f"[Master] [Success] Validator-Agent 검증 최종 통과! 코드가 완성되었습니다.")
                break
                
            if turn == max_turns:
                print(f"[Master] [Warning] 최대 피드백 횟수({max_turns}회)에 도달하였습니다. 협업을 종료합니다.")
                break

            # 피드백을 기반으로 Coder 재호출
            print(f"\n[Master Step 3-Turn {turn}] Coder-Agent에게 피드백을 전달하여 수정을 요청합니다.")
            refactor_prompt = (
                f"이전에 작성한 코드:\n{current_code}\n\n"
                f"위 코드에 대한 검증 피드백:\n{feedback}\n\n"
                f"위 지적 사항들을 모두 충실하게 반영하여 리팩토링된 파이썬 코드 완본을 ```python ... ``` 안에 작성해줘."
            )
            current_code = self.coder.generate(refactor_prompt)
            print("\n" + "-"*30 + f" {turn}차 수정 완료된 코드 " + "-"*30)
            print(current_code)
            print("-" * 80)
            
        print("\n[Master] 모든 협업 단계가 정상 종료되었습니다.")
        return current_code


if __name__ == "__main__":
    # Ollama qwen2.5-coder 모델 연동 준비
    model = "qwen2.5-coder"
    mission = "중복 계산이 발생하지 않고 캐싱이 작동하며 예외 처리가 가미된 피보나치 수열 연산 함수 작성"
    
    pipeline = OllamaOrchestrationPipeline(model)
    final_code = pipeline.run(mission)
    
    print("\n" + "=" * 40 + " 최종 배포 소스코드 " + "=" * 40)
    print(final_code)
    print("=" * 96)
