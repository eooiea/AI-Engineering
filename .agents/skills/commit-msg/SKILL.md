---
name: "commit-msg"
description: "한국어 규칙 및 멀티라인(-m) 표준을 준수하는 Git 커밋 메시지 작성 가이드라인 스킬"
---

# 📌 Git 커밋 메시지 작성 지침 (Commit Message Guidelines)

사용자가 커밋 메시지 생성, Git 커밋 문구 작성, 또는 `git commit` 명령 추천을 요청할 때 작동하는 시스템 지침입니다. 에이전트는 반드시 다음 규격을 준수하여 한국어 커밋 메시지를 추천하거나 명령어를 작성해야 합니다.

---

## 1. ⚙️ 커밋 메시지 기본 구조 (Strict Rule)

커밋 명령어는 각 본문 라인마다 별도의 `-m` 플래그를 사용하는 멀티라인 방식을 엄격히 준수합니다.

```bash
git commit -m "type: subject" -m "- type(scope): detail 1" -m "- type(scope): detail 2"
```

---

## 2. 🏷️ Type 키워드 정의

작업 성격에 따라 아래 7가지 키워드 중 가장 적절한 하나를 선택합니다:

| Type | 설명 |
| :--- | :--- |
| **`feat`** | 새로운 기능 추가 |
| **`fix`** | 버그 수정 |
| **`refactor`** | 코드 리팩토링 (기능 변경 없이 구조 개선) |
| **`docs`** | 문서 수정 (`README.md`, 주석, 교재 등) |
| **`style`** | 코드 포맷팅, 세미콜론 수정 등 (로직 변경 없음) |
| **`chore`** | 패키지 설치, 빌드 업무, 설정 파일 변경 등 |
| **`test`** | 테스트 코드 추가 및 수정 |

---

## 3. 📝 세부 작성 규칙

1. **언어**: 모든 제목과 본문 설명은 **한국어**로 작성합니다.
2. **Subject (제목)**:
   * `type: 주제 요약` 형식으로 작성합니다.
   * 대표 변경 사항을 한 줄로 명확하게 요약합니다.
3. **Body (본문)**:
   * 각 세부 변경 사항마다 별도의 `-m` 플래그를 사용합니다.
   * 각 세부 라인은 `- type(범위/대상): 구체적 변경 내용` 포맷을 따릅니다.
   * 구조 변경이나 리팩토링 시 이유(Why)를 간략히 덧붙입니다.

---

## 💻 쉘(Shell)별 실행 예시

### 1) PowerShell (윈도우 기본 쉘)
```powershell
git commit -m "feat: 커스텀 스킬 등록 및 교재 보강" `
           -m "- feat(Skills): commit-msg 커스텀 스킬 생성" `
           -m "- docs(Materials): Module 2 교재 내용 업그레이드"
```

### 2) Git Bash / Linux
```bash
git commit -m "feat: 커스텀 스킬 등록 및 교재 보강" \
           -m "- feat(Skills): commit-msg 커스텀 스킬 생성" \
           -m "- docs(Materials): Module 2 교재 내용 업그레이드"
```
