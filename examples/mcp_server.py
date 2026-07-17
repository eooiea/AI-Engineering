import platform
from fastmcp import FastMCP

# FastMCP 인스턴스 생성
# 이 인스턴스명이 클라이언트(IDE)에 노출되는 서버 식별 영역의 기본이 됩니다.
mcp = FastMCP("System & Utility MCP Server")

@mcp.tool()
def get_system_info() -> str:
    """현재 서버가 작동하고 있는 로컬 OS 플랫폼 및 파이썬 버전을 조회합니다."""
    os_name = platform.system()
    os_release = platform.release()
    python_ver = platform.python_version()
    return f"OS: {os_name} {os_release} | Python: {python_ver}"

@mcp.tool()
def calculate_square(number: float) -> str:
    """입력받은 숫자의 제곱값을 계산하여 리턴합니다."""
    result = number ** 2
    return f"{number}의 제곱은 {result}입니다."

@mcp.tool()
def get_mock_weather(city: str) -> str:
    """요청받은 도시(city)의 가상 날씨 데이터를 조회합니다."""
    # 간단한 목업(Mock) 매핑
    weather_db = {
        "seoul": "맑음, 기온 25°C, 습도 40%",
        "tokyo": "흐림, 기온 22°C, 습도 65%",
        "new york": "비 옴, 기온 18°C, 습도 88%",
        "london": "가랑비, 기온 15°C, 습도 90%"
    }
    
    city_lower = city.strip().lower()
    weather_info = weather_db.get(city_lower, "알 수 없는 지역 (날씨 데이터 없음)")
    return f"[{city.upper()} 날씨 정보] -> {weather_info}"

@mcp.resource("data://system/greeting")
def welcome_resource() -> str:
    """에이전트가 호출할 수 있는 환영 메시지 정적 리소스를 제공합니다."""
    return "안녕하세요! MCP Server 가 보낸 웰컴 메시지 데이터 리소스입니다."

if __name__ == "__main__":
    # MCP stdio 통신을 활성화하여 서버를 구동합니다.
    mcp.run()
