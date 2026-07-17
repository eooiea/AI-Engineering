# 🧠 Module 2: Antigravity Custom Skills

Antigravity IDE의 **커스텀 스킬 (Custom Skills)** 시스템은 코딩 수정 없이 프롬프트 명령어와 지침(System Instructions)만을 정의하여 에이전트의 작동 방식을 로컬 혹은 프로젝트 단위로 확장할 수 있는 매우 강력한 기능입니다.

사용자가 지시한 개발 작업의 문맥과 일치하는 스킬이 자동 감지(Auto-Discovery)되면, 해당 스킬에 기술된 정교한 규칙과 가이드라인이 에이전트의 상황 인지 버퍼에 즉각 탑재됩니다.

---

## 📂 스킬의 폴더 구조와 위치

스킬은 다음 두 가지 **Customization Roots** 아래에 배치할 수 있습니다.

1. **Global Customizations Root** (모든 프로젝트에 범용 적용):
   *   경로: `C:\Users\<사용자이름>\.gemini\config\skills\`
2. **Workspace Customizations Root** (현재 프로젝트에만 적용):
   *   경로: 프로젝트 루트 밑의 `.agents/skills/`

### 개별 스킬 구조 예시
```
.agents/skills/review-code/
├── SKILL.md                 <-- 핵심 스킬 정의 파일 (YAML Frontmatter + 지침)
├── scripts/                 <-- (선택) 에이전트가 실행할 헬퍼 스크립트
├── examples/                <-- (선택) 모범 개발 코드 예제
└── references/              <-- (선택) 500줄을 초과하는 대형 참조용 명세나 API 문서
```

---

## 📝 SKILL.md의 작성 규격

스킬 정의 파일은 반드시 상단에 마크다운 **YAML Frontmatter** 형식을 갖추어 메타데이터를 기입해야 합니다. Antigravity 에이전트는 이 메타데이터를 사용하여 스킬을 동적으로 식별합니다.

```markdown
---
name: "파이썬 코드 리뷰어 스킬"
description: "파이썬 코드를 리뷰하고 PEP 8 규격을 준수하는지 점검하는 스킬"
---

# 스킬 작동 지침
에이전트가 파이썬 코드를 작성하거나 수정할 때 다음 사항을 강제하십시오:

1. 모든 클래스와 공개 함수에는 docstring을 필수로 포함해야 합니다.
2. 예외 처리는 `except Exception:`과 같은 포괄적 예외 지정을 금지하고 명확한 예외 타입을 지정합니다.
3. 변수명은 snake_case, 클래스명은 PascalCase를 따릅니다.
```

### ⚠️ 핵심 작성 규칙
*   **YAML Frontmatter**: `name`과 `description` 필드는 필수(Required) 항목이며, 에이전트가 이 내용을 기준으로 작업에 매칭할지 결정합니다.
*   **분량 제한**: `SKILL.md` 본문은 에이전트 컨텍스트 손실을 막기 위해 **500줄 이하**로 유지해야 합니다. 방대한 참고자료가 있다면 `references/` 하위 디렉토리에 분할하여 에이전트가 원할 때 읽어가도록 설계하십시오.
*   **자동 감지**: 표준 위치에 두면 즉시 탐색됩니다. 만약 외부 공유 드라이브 등 특수한 위치에 스킬을 두었다면, 최상위 customization root에 `skills.json`을 작성해 수동 등록해주어야 합니다.

---

## 🏋️ 실습 예제 따라하기

이 모듈과 연계되는 커스텀 스킬은 프로젝트 최상위의 [.agents/skills/review-code/SKILL.md](file:///c:/Users/majun/Coding/anti/.agents/skills/review-code/SKILL.md)에 생성되어 있습니다.

### 실습 절차
1. [.agents/skills/review-code/SKILL.md](file:///c:/Users/majun/Coding/anti/.agents/skills/review-code/SKILL.md)를 열어 메타데이터와 프롬프트 가이드라인을 확인해 봅니다.
2. 에이전트에게 "이 워크스페이스에 있는 python 코드에 대해 코드 리뷰를 해줘" 라고 지시합니다.
3. 에이전트가 해당 명령을 받고 `review-code` 스킬의 가이드를 자동으로 감지하여 코드 리뷰 가이드 지침대로 리뷰 보고서를 한글로 이쁘게 작성해 주는지 확인합니다.
