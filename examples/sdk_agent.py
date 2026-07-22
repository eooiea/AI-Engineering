"""Google Antigravity SDK Agent Execution Module.

google-antigravity SDK를 사용하여 현재 워크스페이스 컨텍스트에서 자율적으로 파일 탐색 및 요약을 수행하는 에이전트 예제입니다.
"""
import asyncio
import os
import sys

# google-antigravity 라이브러리가 제대로 임포트되는지 확인
try:
    from google.antigravity import Agent, LocalAgentConfig
    HAS_SDK = True
except ImportError as e:
    HAS_SDK = False
    IMPORT_ERROR = e

async def run_agent():
    """Antigravity Agent 세션을 가동하여 워크스페이스 내 문서 분석 태스크를 구동합니다."""
    print("[SDK-Agent] 에이전트 초기화 프로세스 시작...")
    
    # 1. SDK 존재 여부 체크
    if not HAS_SDK:
        print(f"[Error] google-antigravity SDK가 올바르게 설치되지 않았거나 임포트할 수 없습니다.")
        print(f"상세 에러: {IMPORT_ERROR}")
        print("설치 명령: pip install google-antigravity")
        return

    # 2. GEMINI_API_KEY 환경변수 유무 점검
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("*" * 80)
        print("[Info] 안내: 'GEMINI_API_KEY' 환경 변수가 설정되어 있지 않습니다.")
        print("   Antigravity SDK는 Gemini 3.5 모델을 호출하므로, 실행 시 API 키가 필요합니다.")
        print("   설정 방법:")
        print("   - PowerShell (Windows): $env:GEMINI_API_KEY='your_api_key_here'")
        print("   - Bash (Linux/Mac): export GEMINI_API_KEY='your_api_key_here'")
        print("*" * 80)
        
        # 가상(Mock) 코드로 SDK API 호출 구문 예시만 인쇄 후 강제 종료하지 않고 초기화 시도만 해봅니다.
        print("\n[구문 예시] API 키가 연동되었다면 아래 코드가 실행됩니다:")
        print("----------------------------------------------------------------")
        print("config = LocalAgentConfig()")
        print("async with Agent(config) as agent:")
        print("    response = await agent.chat('워크스페이스 내 python 파일 목록을 요약해줘.')")
        print("    print(await response.text())")
        print("----------------------------------------------------------------\n")
        
        # API 키가 없어도 인스턴스 생성이 되는지 시험 삼아 시도합니다.
        try:
            config = LocalAgentConfig()
            print("LocalAgentConfig 객체가 성공적으로 생성되었습니다.")
        except Exception as ex:
            print(f"설정 객체 생성 실패: {ex}")
        return

    # 3. 실제 자율 에이전트 구동
    try:
        # 현재 디렉토리 컨텍스트를 활용하도록 설정
        config = LocalAgentConfig()
        current_cwd = os.getcwd()
        
        print("[SDK-Agent] Agent 인스턴스를 생성하고 세션을 엽니다.")
        async with Agent(config) as agent:
            prompt = f"현재 워크스페이스({current_cwd})에 작성되어 있는 학습용 markdown 파일 목록을 확인하고, 각 파일이 어떤 모듈을 다루고 있는지 리포트로 요약해줘."
            print(f"\n[SDK-Agent] 에이전트 질문 전송:\n'{prompt}'\n")
            
            # 에이전트와 대화 수행
            response = await agent.chat(prompt)
            
            print("[SDK-Agent] 에이전트로부터 응답을 수신했습니다:\n")
            print("=" * 40 + " 에이전트 실행 결과 " + "=" * 40)
            print(await response.text())
            print("=" * 96)
            
    except Exception as e:
        print(f"\n[Error] 에이전트 세션 실행 중 오류가 발생했습니다: {e}")
        print("API 키 권한이 올바른지, 또는 네트워크 프록시 설정을 확인하십시오.")

if __name__ == "__main__":
    # 비동기 루프로 에이전트 태스크 구동
    asyncio.run(run_agent())
