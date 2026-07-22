"""코드 스타일 검사 헬퍼 스크립트 (Helper Script Example)

이 스크립트는 파이썬 소스 코드의 함수명(snake_case) 및 docstring 유무를 검사하는 스킬 헬퍼 도구입니다.
"""
import ast
import re

def analyze_code_style(code_content: str) -> dict:
    results = {"snake_case_violations": [], "missing_docstrings": []}
    try:
        tree = ast.parse(code_content)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # 1. snake_case 검사
                if not re.match(r"^[a-z_][a-z0-9_]*$", node.name):
                    results["snake_case_violations"].append(node.name)
                # 2. docstring 유무 검사
                if not ast.get_docstring(node):
                    results["missing_docstrings"].append(node.name)
    except Exception as e:
        results["parse_error"] = str(e)
    return results

if __name__ == "__main__":
    sample = "def badCamelCaseFunction(): pass"
    print("스킬 헬퍼 스크립트 검사 결과:", analyze_code_style(sample))
