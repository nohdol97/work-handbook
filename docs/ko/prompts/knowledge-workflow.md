---
id: prompts-knowledge-workflow
status: overview
last_updated: 2026-10-18
last_reviewed: 2026-10-18
knowledge_ids: []
---

# 지식 관리 실무 프롬프트

실제 SQL·설정·로그·변경안을 붙여 바로 요청할 수 있는 예시다. 비식별 자료만 사용하고, 제안은 실제 근거와 권한에 맞춰 검토한다. 이 예시만으로 시스템 변경이나 데이터 삭제를 승인하지 않는다. 사용 빈도나 모델 성능을 측정한 사례는 아니다.

[개념 문서](../methodologies/knowledge-workflow.md) · [프롬프트 모음](index.md)

| 상황 | 바로 가기 |
|---|---|
| 문서화 전 지식 추출 | [01](#knowledge-workflow-01) |
| 한영 경고 강도와 조건 대조 | [02](#knowledge-workflow-02) |
| 새 자료와 기존 문서의 중복 통합 | [03](#knowledge-workflow-03) |
| 수정 후 검토 범위와 증거 확인 | [04](#knowledge-workflow-04) |

## 문서화 전 지식 추출 {#knowledge-workflow-01}

=== "한국어"

    ```text {.prompt}
    회의·학습 노트에서 문서 초안을 만들기 전에 빠뜨리면 안 되는 항목을 찾는다.
    1. 개념·예시·제약·실패·반례·미해결 질문을 먼저 추출해 주세요.
    2. 각 항목에 원문 위치와 제안 목적지를 붙여 주세요.
    3. 중복은 표시하되 서로 다른 조건을 합쳐 없애지 마세요.
    항목 | 유형 | 원문 위치 | 목적지 | 보류 이유 표를 작성해 주세요.
    ```

=== "English"

    ```text {.prompt}
    Find what must be retained before turning meeting or study notes into documentation.
    1. Extract concepts, examples, constraints, failures, counterexamples, and open questions.
    2. Give each item a source location and a proposed destination.
    3. Mark duplicates without erasing different conditions.
    Return a table: item | type | source location | destination | reason to defer.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 원문 전체의 접근 범위와 기존 문서 목적. 원문 위치를 유지하고 접근하지 못한 구간을 먼저 표시한다. 짧게 요약하면서 제약이나 반례를 버릴 수 있다. 원문 절·예시·숫자·실패 조건이 표에서 추적되지 않으면 초안 작성으로 넘어가지 않는다.

## 한영 경고 강도와 조건 대조 {#knowledge-workflow-02}

=== "한국어"

    ```text {.prompt}
    번역 후 필수 조건·금지 사항·수치가 같은지 검토 중이야.
    1. 개념·예시·조건·경고·수치·도식을 항목별로 비교해 주세요.
    2. 필수와 권고, 가능성과 보장의 차이를 우선 확인해 주세요.
    3. 불일치한 부분만 최소 수정안을 제안해 주세요.
    한국어 위치 | 영어 위치 | 차이 | 근거 | 수정안 표를 주세요.
    ```

=== "English"

    ```text {.prompt}
    Check whether required conditions, prohibitions, and numbers survive translation.
    1. Compare concepts, examples, conditions, warnings, numbers, and diagrams.
    2. Prioritize required versus recommended and possible versus guaranteed behavior.
    3. Suggest minimal edits only where meaning differs.
    Return: Korean location | English location | difference | evidence | edit.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 비교할 양언어 전체 문서와 원문 근거. 원문 위치를 유지하고 접근하지 못한 구간을 먼저 표시한다. 자연스러운 번역을 만들면서 must와 may를 바꿀 수 있다. 문장이 자연스러워도 must·may·수치·경고 강도가 달라지면 수정한다.

## 새 자료와 기존 문서의 중복 통합 {#knowledge-workflow-03}

=== "한국어"

    ```text {.prompt}
    같은 주제의 새 자료가 들어왔고 기존의 올바른 지식을 유지해야 한다.
    1. 중복·추가·충돌·범위 밖 내용을 분리해 주세요.
    2. 올바른 기존 지식과 새 지식의 합집합을 보존해 주세요.
    3. 판단할 수 없는 충돌은 보류하고 필요한 근거를 적어 주세요.
    ID | 상태 | 목적지 | 보존한 조건 | 이유 표와 수정 계획을 주세요.
    ```

=== "English"

    ```text {.prompt}
    New material covers an existing topic whose correct knowledge must remain.
    1. Separate duplicates, additions, conflicts, and out-of-scope items.
    2. Preserve the union of correct existing and useful new knowledge.
    3. Defer unresolved conflicts and list the evidence needed.
    Return: ID | state | destination | preserved conditions | reason, plus an edit plan.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 기존·신규 지식 ID와 보존해야 할 원문 구역. 원문 위치를 유지하고 접근하지 못한 구간을 먼저 표시한다. 표현이 비슷하다는 이유로 적용 조건이 다른 내용을 삭제할 수 있다. 표현이 비슷해도 적용 조건이 다르면 하나를 없애지 않는다.

## 수정 후 검토 범위와 증거 확인 {#knowledge-workflow-04}

=== "한국어"

    ```text {.prompt}
    내용을 바꾼 뒤 어떤 번역·출처·검증 증거를 갱신해야 하는지 확인한다.
    1. 의미·예시·경고·링크·도식에 미친 영향을 구분해 주세요.
    2. 다시 읽어야 할 양쪽 페이지와 출처 구간을 지정해 주세요.
    3. 실행한 검사와 아직 실행하지 않은 검사를 분리해 주세요.
    검토 항목 | 근거 | 상태 | 다음 확인 표를 주세요.
    ```

=== "English"

    ```text {.prompt}
    Identify translations, source mappings, and evidence affected by an edit.
    1. Separate effects on meaning, examples, warnings, links, and diagrams.
    2. Identify both pages and source sections that need another full review.
    3. Distinguish completed checks from checks not yet run.
    Return: review item | evidence | status | next check.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 실제 검토한 페이지와 실행한 검사 로그. 원문 위치를 유지하고 접근하지 못한 구간을 먼저 표시한다. hash를 새로 계산한 것만으로 의미 검토가 끝났다고 할 수 있다. hash 갱신만 있고 의미 대조나 실제 검사 로그가 없으면 완료로 표시하지 않는다.
