"""Module 1: Model Context Protocol (MCP) Server Example.

FastMCP 기반으로 Tools, Resources, Prompts 3대 핵심 프리미티브를 모두 구현한
표준 MCP 서버 모듈입니다.
"""

import json
import os
import platform
import sys
from typing import Dict, Any

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

try:
    from fastmcp import FastMCP
    mcp_available = True
except ImportError:
    mcp_available = False


if mcp_available:
    mcp = FastMCP("system-utility-server")

    @mcp.tool()
    def get_system_metrics() -> Dict[str, Any]:
        """로컬 호스트의 OS, CPU 아키텍처 및 파이썬 런타임 정보를 수집합니다."""
        return {
            "os_name": platform.system(),
            "os_release": platform.release(),
            "architecture": platform.machine(),
            "python_version": platform.python_version(),
            "cpu_count": os.cpu_count() or 1
        }

    @mcp.tool()
    def get_weather_forecast(city: str) -> Dict[str, Any]:
        """지정된 도시의 현재 날씨와 기온 정보를 조회합니다."""
        mock_data = {
            "seoul": {"temp_c": 22.5, "condition": "맑음 (Sunny)", "humidity": 45},
            "tokyo": {"temp_c": 24.0, "condition": "구름 조금 (Partly Cloudy)", "humidity": 55},
            "new york": {"temp_c": 18.2, "condition": "비 (Rain)", "humidity": 80}
        }
        return mock_data.get(city.lower(), {"temp_c": 20.0, "condition": "정보 없음 (Default)", "humidity": 50})

    @mcp.resource("config://server-info")
    def get_server_config() -> str:
        """서버 환경 설정 및 메타데이터 리소스를 반환합니다."""
        return json.dumps({
            "server_name": "system-utility-server",
            "protocol_version": "2024-11-05",
            "transport": "stdio / sse",
            "status": "healthy"
        }, indent=2, ensure_ascii=False)

    @mcp.prompt()
    def diagnose_system_prompt(user_issue: str) -> str:
        """시스템 문제 진단을 위한 가이드라인 프롬프트를 생성합니다."""
        return f"""
다음 시스템 문제를 진단하고 get_system_metrics 도구를 호출하여 인프라 호환성을 분석하십시오.
- 사용자 제보 증상: {user_issue}
- 분석 원칙: 근본 원인(Root Cause), 재현 단계, 권장 해결책을 3단계로 서술할 것.
"""


def main():
    print("=" * 70)
    print("🔌 Module 1: Model Context Protocol (MCP) Server")
    print("=" * 70)

    if mcp_available:
        print("[✅ FastMCP 패키지 감지 완료]")
        print("  • 등록된 Tools:     get_system_metrics, get_weather_forecast")
        print("  • 등록된 Resources: config://server-info")
        print("  • 등록된 Prompts:   diagnose_system_prompt")
        print("\n[🚀 서버 테스트 실행]")
        print("  1. System Metrics Tool Output:")
        print("    ", get_system_metrics())
        print("  2. Server Config Resource Output:")
        print("    ", get_server_config())
        
        if len(sys.argv) > 1 and sys.argv[1] == "--run":
            print("\n[📡 MCP stdio Transport 서빙 시작...]")
            mcp.run(transport="stdio")
    else:
        print("[ℹ️ FastMCP 미설치 환경: 표준 JSON-RPC 시뮬레이션 모드]")
        sample_rpc_request = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {"name": "get_system_metrics", "arguments": {}},
            "id": 1
        }
        sample_rpc_response = {
            "jsonrpc": "2.0",
            "result": {
                "content": [{"type": "text", "text": json.dumps({"os": platform.system(), "python": platform.python_version()})}]
            },
            "id": 1
        }
        print("  • Request JSON-RPC:", json.dumps(sample_rpc_request))
        print("  • Response JSON-RPC:", json.dumps(sample_rpc_response))
    print("=" * 70)


if __name__ == "__main__":
    main()
