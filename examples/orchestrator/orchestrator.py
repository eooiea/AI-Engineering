import os
import sys
import time

# google-genai 라이브러리 연동 시도
try:
    from google import genai
    from google.genai import types
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

class AgentWorker:
    """하위 에이전트들의 공통 인터페이스를 정의하는 베이스 클래스"""
    def __init__(self, role: str, system_instruction: str):
        self.role = role
        self.system_instruction = system_instruction
        self.client = None
        
        # GEMINI_API_KEY가 환경 변수에 지정된 경우 실시간 API 연동 준비
        if HAS_GENAI and os.environ.get("GEMINI_API_KEY"):
            try:
                # API Key는 genai.Client가 내부적으로 os.environ["GEMINI_API_KEY"]를 탐색합니다.
                self.client = genai.Client()
            except Exception as e:
                print(f"[Warning] API 클라이언트 초기화 실패 ({e}). Mock 모드로 대체 실행합니다.")
                self.client = None

    def execute(self, prompt: str) -> str:
        """프롬프트를 실행하고 답변을 리턴합니다 (실제 API 또는 모의 응답)"""
        print(f"[{self.role}] 작업 지시 수신 중...")
        time.sleep(1.0) # 생각하는 척 지연시간 부여
        
        if self.client:
            try:
                # Gemini 2.5 Flash 모델 사용 권장
                response = self.client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=self.system_instruction,
                        temperature=0.7,
                    )
                )
                return response.text
            except Exception as e:
                print(f"[Error] API 호출 오류 ({e}). Mock 데이터로 대체합니다.")
                return self._get_mock_response(prompt)
        else:
            return self._get_mock_response(prompt)

    def _get_mock_response(self, prompt: str) -> str:
        """API 연동이 불가능할 때 사용할 가상 응답 발전기 (자식 클래스에서 오버라이드)"""
        return "기본 에이전트 응답 코드"


class OutlineAgent(AgentWorker):
    """지정된 주제에 맞는 보고서 목차(Outline)를 구성하는 에이전트"""
    def __init__(self):
        super().__init__(
            role="Outline-Agent",
            system_instruction="당신은 보고서 기획 전문가입니다. 주어진 주제에 대하여 서론, 본론, 결론을 아우르는 마크다운 목차를 생성하십시오. 서브헤더는 기입하지 마십시오."
        )

    def _get_mock_response(self, prompt: str) -> str:
        print(f"[{self.role}] API 키 미검출 - 가상 목차 데이터 생성")
        return (
            "1. 서론: AI 에이전트 오케스트레이션의 부상\n"
            "2. 본론: 에이전트 협업 설계 패턴 및 프레임워크 비교\n"
            "3. 결론: 향후 완전 자율 소프트웨어 개발 전망"
        )


class ContentAgent(AgentWorker):
    """목차의 세부 섹션을 받아 상세 원고를 기술하는 에이전트"""
    def __init__(self):
        super().__init__(
            role="Content-Agent",
            system_instruction="당신은 전문 리포트 작성가입니다. 목차의 한 주제를 받으면 그에 대한 상세 내용(최소 2~3문단)을 정중한 한글 어조로 서술하십시오."
        )

    def _get_mock_response(self, prompt: str) -> str:
        print(f"[{self.role}] API 키 미검출 - 가상 섹션 본문 생성")
        if "서론" in prompt:
            return (
                "최근 AI 엔지니어링 업계에서는 단일 거대 모델의 일회성 응답 한계를 극복하기 위해 다중 에이전트 조율(Orchestration) 시스템이 대두되고 있습니다.\n"
                "과거 프롬프트 엔지니어링 수준에 머무르던 에이전트들은 이제 파일 읽기, 터미널 실행 등의 자율 도구를 장착하여 워크플로우를 스스로 전개해 나갑니다."
            )
        elif "본론" in prompt:
            return (
                "멀티 에이전트 협업 구조는 주로 라우터 패턴, 마스터-워커 패턴, 플래너-실행기 패턴으로 나누어 구현됩니다.\n"
                "LangGraph와 CrewAI 같은 프레임워크는 상태(State)와 규칙 기반 통제를 결합하여 에이전트 간 순환 구조와 안전성을 통제합니다."
            )
        else:
            return (
                "결론적으로 AI 에이전트 오케스트레이션은 인간 개발자를 완전히 대체하는 것이 아닌, 생산성을 극대화시키는 부조종사 역할을 넘어 자동화 파트너로 발전할 것입니다.\n"
                "향후에는 보안 및 평가 하네스의 내재화가 이러한 AI 파이프라인 상용화의 핵심 열쇠가 될 것입니다."
            )


class MasterOrchestrator:
    """하위 에이전트들을 관리 및 호출하여 완성된 하나의 보고서를 조율해 내는 컨트롤러"""
    def __init__(self):
        print("[Master] 오케스트레이션 엔진 가동 시작...")
        self.outline_agent = OutlineAgent()
        self.content_agent = ContentAgent()

    def run_pipeline(self, topic: str) -> str:
        print(f"\n[Master] 목표 주제 접수: '{topic}'")
        
        # Step 1: 목차 에이전트 소환하여 아웃라인 획득
        print("\n[Master Step 1] Outline-Agent를 호출하여 보고서 골격을 기획합니다.")
        outline = self.outline_agent.execute(f"주제: {topic}에 대한 목차를 작성해줘.")
        print(f"\n[Master] 기획된 목차 수신 완료:\n{outline}\n")
        
        # 목차 분리 (라인 단위)
        sections = [line.strip() for line in outline.strip().split("\n") if line.strip()]
        
        # Step 2: 각 목차별 본문 내용 생성 (루프 오케스트레이션)
        final_document = f"# [Report] {topic} 종합 보고서\n\n"
        
        print("[Master Step 2] Content-Agent를 순차 호출하여 세부 섹션 본문을 작성합니다.")
        for section in sections:
            print(f"\n[Master] 현재 작성 중인 섹션 -> {section}")
            section_content = self.content_agent.execute(f"섹션 제목: {section}\n위 섹션에 대한 상세한 본문을 작성해줘.")
            final_document += f"## {section}\n\n{section_content}\n\n"
            
        print("\n[Master Step 3] 모든 섹션이 완료되었습니다. 결과물을 합성합니다.")
        return final_document


if __name__ == "__main__":
    # 실행 시 인자로 주제를 주거나, 기본 주제 사용
    topic = sys.argv[1] if len(sys.argv) > 1 else "AI 에이전트 오케스트레이션 트렌드"
    
    # GEMINI_API_KEY 안내 문구
    if not os.environ.get("GEMINI_API_KEY"):
        print("*" * 80)
        print("[Info] 안내: 'GEMINI_API_KEY' 환경 변수가 설정되어 있지 않아 모의(Mock) 에이전트로 시뮬레이션합니다.")
        print("   실제 API 연동을 원하시면 환경 변수를 설정해 주세요.")
        print("   예: $env:GEMINI_API_KEY='your-key-here' (PowerShell)")
        print("*" * 80)
        
    orchestrator = MasterOrchestrator()
    report = orchestrator.run_pipeline(topic)
    
    print("\n" + "=" * 40 + " 최종 보고서 출력 " + "=" * 40)
    print(report)
    print("=" * 96)
