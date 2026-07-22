# 📚 PEP 8 & 코드 스타일 참조 가이드 (Reference Guide)

이 문서는 review-code 스킬이 참조하는 세부 코딩 스타일 표준 가이드라인입니다. `SKILL.md` 본문이 500줄을 넘지 않도록 상세 명세를 별도 분리하여 관리합니다.

---

## 1. Naming Conventions (이름 규칙)
* **모듈 (Modules)**: 짧은 소문자, 언더스코어 가능 (예: `data_parser.py`)
* **클래스 (Classes)**: CapWords / PascalCase (예: `HttpResponseHandler`)
* **함수 및 변수 (Functions & Variables)**: snake_case (예: `calculate_tax_rate`)
* **상수 (Constants)**: ALL_CAPS (예: `MAX_RETRY_COUNT = 3`)

---

## 2. Docstring Conventions (PEP 257)
* 모든 모듈, 공개 클래스, 공개 함수에는 다중 행 docstring을 작성합니다.
* 요약 문장은 마침표로 끝나는 삼중 따옴표 삼중 따옴표 삼중 따옴표 형태를 유지합니다.

---

## 3. Exception Handling Best Practices
* 포괄적 예외 지칭(`except:`, `except Exception:`) 대신 구체적 예외 클래스 지정:
  * ❌ `except Exception:`
  * ⭕ `except (KeyError, ValueError) as err:`
