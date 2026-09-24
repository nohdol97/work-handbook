---
id: prompts-knowledge-workflow
status: overview
last_updated: 2026-09-24
last_reviewed: 2026-09-24
knowledge_ids: []
---

# 지식 관리 실무 프롬프트

기존 지식 관리 원칙에서 파생한 작성 예시 4개다. 모델 실행이나 실제 업무 성과를 검증한 기록이 아니다. 대괄호 입력을 비식별 자료로 바꾸고 prompt의 언어 탭을 선택해 복사한다.

[개념 문서](../methodologies/knowledge-workflow.md) · [프롬프트 모음](index.md)

| 상황 | 바로 가기 |
|---|---|
| 문서화 전 지식 추출 | [01](#knowledge-workflow-01) |
| 한영 경고 강도와 조건 대조 | [02](#knowledge-workflow-02) |
| 새 자료와 기존 문서의 중복 통합 | [03](#knowledge-workflow-03) |
| 수정 후 검토 범위와 증거 확인 | [04](#knowledge-workflow-04) |

## 문서화 전 지식 추출 {#knowledge-workflow-01}

**상황:** 회의·학습 노트에서 문서 초안을 만들기 전에 빠뜨리면 안 되는 항목을 찾는다.

**제공 맥락:** 비식별 원문 전체, 범위, 기존 목차, 접근하지 못한 구간.

=== "한국어"

    ```text {.prompt}
    [맥락]
    원문: [비식별 노트 전체]
    범위와 기존 목차: [범위 / 목차]
    접근하지 못한 부분: [구간 또는 없음]
    [요청]
    1. 개념·예시·제약·실패·반례·미해결 질문을 먼저 추출해 주세요.
    2. 각 항목에 원문 위치와 제안 목적지를 붙여 주세요.
    3. 중복은 표시하되 서로 다른 조건을 합쳐 없애지 마세요.
    [출력]
    항목 | 유형 | 원문 위치 | 목적지 | 보류 이유 표를 작성해 주세요.
    [검증]
    원문에 없는 내용을 만들지 말고 접근 불가 범위를 명시해 주세요.
    추출이 끝나기 전에는 최종 문서 초안을 쓰지 마세요.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    Source: [full sanitized notes]
    Scope and current outline: [scope / outline]
    Unavailable sections: [sections or none]
    [Task]
    1. Extract concepts, examples, constraints, failures, counterexamples, and open questions.
    2. Give each item a source location and a proposed destination.
    3. Mark duplicates without erasing different conditions.
    [Output]
    Return a table: item | type | source location | destination | reason to defer.
    [Checks]
    Do not invent source content. State any unavailable scope.
    Do not draft the final document before extraction is complete.
    ```

**기대 결과:** 원문 위치·유형·목적지를 가진 추출표와 누락 근거 목록.

**오류 가능성:** 짧게 요약하면서 제약이나 반례를 버릴 수 있다.

**검증 방법:** 각 원문 절과 예시·숫자·실패 조건이 추출표에 있는지 직접 대조한다.

## 한영 경고 강도와 조건 대조 {#knowledge-workflow-02}

**상황:** 번역 후 필수 조건·금지 사항·수치가 같은지 검토한다.

**제공 맥락:** 한국어·영어 전체 페이지, 공통 용어집, 변경한 원문 구간.

=== "한국어"

    ```text {.prompt}
    [맥락]
    한국어 페이지: [전체 본문]
    영어 페이지: [전체 본문]
    용어집과 원문: [정의 / 근거]
    [요청]
    1. 개념·예시·조건·경고·수치·도식을 항목별로 비교해 주세요.
    2. 필수와 권고, 가능성과 보장의 차이를 우선 확인해 주세요.
    3. 불일치한 부분만 최소 수정안을 제안해 주세요.
    [출력]
    한국어 위치 | 영어 위치 | 차이 | 근거 | 수정안 표를 주세요.
    [검증]
    문장 수가 같다는 이유로 의미가 같다고 판단하지 마세요.
    불명확한 원문은 추측하지 말고 확인 질문으로 남겨 주세요.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    Korean page: [full text]
    English page: [full text]
    Glossary and source: [definitions / evidence]
    [Task]
    1. Compare concepts, examples, conditions, warnings, numbers, and diagrams.
    2. Prioritize required versus recommended and possible versus guaranteed behavior.
    3. Suggest minimal edits only where meaning differs.
    [Output]
    Return: Korean location | English location | difference | evidence | edit.
    [Checks]
    Equal sentence counts do not prove equal meaning.
    Turn unclear source statements into questions instead of guessing.
    ```

**기대 결과:** 문장 위치와 의미 차이, 최소 수정안, 검토가 필요한 모호함.

**오류 가능성:** 자연스러운 번역을 만들면서 must와 may를 바꿀 수 있다.

**검증 방법:** 두 언어의 예시·경고·조건·숫자를 원문과 대조하고 사람이 최종 검토한다.

## 새 자료와 기존 문서의 중복 통합 {#knowledge-workflow-03}

**상황:** 같은 주제의 새 자료가 들어왔고 기존의 올바른 지식을 유지해야 한다.

**제공 맥락:** 기존 한영 페이지, 신규 원문과 ID 목록, canonical 목적지와 충돌 항목.

=== "한국어"

    ```text {.prompt}
    [맥락]
    기존 문서와 지식 ID: [전체 본문 / ID]
    새 원문과 추출 ID: [원문 / 목록]
    정규 주제 위치: [목적지]
    [요청]
    1. 중복·추가·충돌·범위 밖 내용을 분리해 주세요.
    2. 올바른 기존 지식과 새 지식의 합집합을 보존해 주세요.
    3. 판단할 수 없는 충돌은 보류하고 필요한 근거를 적어 주세요.
    [출력]
    ID | 상태 | 목적지 | 보존한 조건 | 이유 표와 수정 계획을 주세요.
    [검증]
    짧게 만들기 위해 기술 범위를 줄이지 마세요.
    모든 ID를 추적하되 보류를 공개 완료로 계산하지 마세요.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    Existing pages and knowledge IDs: [full text / IDs]
    New source and extracted IDs: [source / list]
    Canonical topic locations: [destinations]
    [Task]
    1. Separate duplicates, additions, conflicts, and out-of-scope items.
    2. Preserve the union of correct existing and useful new knowledge.
    3. Defer unresolved conflicts and list the evidence needed.
    [Output]
    Return: ID | state | destination | preserved conditions | reason, plus an edit plan.
    [Checks]
    Do not reduce technical scope merely to shorten the document.
    Track every ID without counting deferred items as published.
    ```

**기대 결과:** 항목별 Included/Merged/Deferred/Excluded 제안과 이유·목적지.

**오류 가능성:** 표현이 비슷하다는 이유로 적용 조건이 다른 내용을 삭제할 수 있다.

**검증 방법:** 기존·신규 ID가 모두 대응되고 보류·제외 이유가 구체적인지 대조한다.

## 수정 후 검토 범위와 증거 확인 {#knowledge-workflow-04}

**상황:** 내용을 바꾼 뒤 어떤 번역·출처·검증 증거를 갱신해야 하는지 확인한다.

**제공 맥락:** 변경 diff, 한영 전체 본문, 기존 검토 기록, 실제 실행한 검사 결과.

=== "한국어"

    ```text {.prompt}
    [맥락]
    변경 diff와 한영 본문: [diff / 전체 페이지]
    출처 반영표와 이전 검토: [ID 대응 / 기록]
    실제 검사 결과: [명령 / 종료 상태 / 로그]
    [요청]
    1. 의미·예시·경고·링크·도식에 미친 영향을 구분해 주세요.
    2. 다시 읽어야 할 양쪽 페이지와 출처 구간을 지정해 주세요.
    3. 실행한 검사와 아직 실행하지 않은 검사를 분리해 주세요.
    [출력]
    검토 항목 | 근거 | 상태 | 다음 확인 표를 주세요.
    [검증]
    hash 갱신을 실제 의미 검토의 대체물로 취급하지 마세요.
    실행하지 않은 검사나 vault 복사를 성공했다고 쓰지 마세요.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    Diff and bilingual text: [diff / complete pages]
    Source mapping and prior review: [ID mapping / records]
    Actual check results: [command / exit status / logs]
    [Task]
    1. Separate effects on meaning, examples, warnings, links, and diagrams.
    2. Identify both pages and source sections that need another full review.
    3. Distinguish completed checks from checks not yet run.
    [Output]
    Return: review item | evidence | status | next check.
    [Checks]
    A new hash does not replace an actual semantic review.
    Do not claim success for checks or vault copies that were not run.
    ```

**기대 결과:** 영향 범위, 재검토 목록, 통과 근거와 미검증 범위.

**오류 가능성:** hash를 새로 계산한 것만으로 의미 검토가 끝났다고 할 수 있다.

**검증 방법:** 실제 전체 문서 검토와 검사 로그를 대조하고 현재 파일 hash가 기록과 같은지 확인한다.
