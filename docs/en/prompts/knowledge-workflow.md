---
id: prompts-knowledge-workflow
status: overview
last_updated: 2026-10-18
last_reviewed: 2026-10-18
knowledge_ids: []
---

# Knowledge workflow prompts

Copy these examples with the relevant SQL, settings, logs, or proposed changes. Use sanitized material and check suggestions against real evidence and permissions. An example does not authorize system changes or data deletion. These are not measured usage or model-performance results.

[Concept guide](../methodologies/knowledge-workflow.md) · [Prompt library](index.md)

| Situation | Jump to example |
|---|---|
| Extract knowledge before drafting | [01](#knowledge-workflow-01) |
| Compare bilingual constraints and warnings | [02](#knowledge-workflow-02) |
| Merge new material without losing conditions | [03](#knowledge-workflow-03) |
| Plan review after a documentation change | [04](#knowledge-workflow-04) |

## Extract knowledge before drafting {#knowledge-workflow-01}

=== "English"

    ```text {.prompt}
    Find what must be retained before turning meeting or study notes into documentation.
    1. Extract concepts, examples, constraints, failures, counterexamples, and open questions.
    2. Give each item a source location and a proposed destination.
    3. Mark duplicates without erasing different conditions.
    Return a table: item | type | source location | destination | reason to defer.
    ```

=== "한국어"

    ```text {.prompt}
    회의·학습 노트에서 문서 초안을 만들기 전에 빠뜨리면 안 되는 항목을 찾는다.
    1. 개념·예시·제약·실패·반례·미해결 질문을 먼저 추출해 주세요.
    2. 각 항목에 원문 위치와 제안 목적지를 붙여 주세요.
    3. 중복은 표시하되 서로 다른 조건을 합쳐 없애지 마세요.
    항목 | 유형 | 원문 위치 | 목적지 | 보류 이유 표를 작성해 주세요.
    ```

**Key point:** Evidence to check first: access coverage of the full source and the document's purpose. Keep source locations and mark unavailable sections before review. It may drop constraints or counterexamples while summarizing. Do not start drafting until source sections, examples, numbers, and failure conditions are traceable in the table.

## Compare bilingual constraints and warnings {#knowledge-workflow-02}

=== "English"

    ```text {.prompt}
    Check whether required conditions, prohibitions, and numbers survive translation.
    1. Compare concepts, examples, conditions, warnings, numbers, and diagrams.
    2. Prioritize required versus recommended and possible versus guaranteed behavior.
    3. Suggest minimal edits only where meaning differs.
    Return: Korean location | English location | difference | evidence | edit.
    ```

=== "한국어"

    ```text {.prompt}
    번역 후 필수 조건·금지 사항·수치가 같은지 검토 중이야.
    1. 개념·예시·조건·경고·수치·도식을 항목별로 비교해 주세요.
    2. 필수와 권고, 가능성과 보장의 차이를 우선 확인해 주세요.
    3. 불일치한 부분만 최소 수정안을 제안해 주세요.
    한국어 위치 | 영어 위치 | 차이 | 근거 | 수정안 표를 주세요.
    ```

**Key point:** Evidence to check first: complete pages in both languages and source evidence. Keep source locations and mark unavailable sections before review. It may change must to may while making a translation sound natural. Fix changed must/may meanings, numbers, or warning strength even when the prose reads naturally.

## Merge new material without losing conditions {#knowledge-workflow-03}

=== "English"

    ```text {.prompt}
    New material covers an existing topic whose correct knowledge must remain.
    1. Separate duplicates, additions, conflicts, and out-of-scope items.
    2. Preserve the union of correct existing and useful new knowledge.
    3. Defer unresolved conflicts and list the evidence needed.
    Return: ID | state | destination | preserved conditions | reason, plus an edit plan.
    ```

=== "한국어"

    ```text {.prompt}
    같은 주제의 새 자료가 들어왔고 기존의 올바른 지식을 유지해야 한다.
    1. 중복·추가·충돌·범위 밖 내용을 분리해 주세요.
    2. 올바른 기존 지식과 새 지식의 합집합을 보존해 주세요.
    3. 판단할 수 없는 충돌은 보류하고 필요한 근거를 적어 주세요.
    ID | 상태 | 목적지 | 보존한 조건 | 이유 표와 수정 계획을 주세요.
    ```

**Key point:** Evidence to check first: old/new knowledge IDs and source sections that must remain intact. Keep source locations and mark unavailable sections before review. It may delete content with different conditions because wording looks similar. Keep differing conditions even when the wording is similar.

## Plan review after a documentation change {#knowledge-workflow-04}

=== "English"

    ```text {.prompt}
    Identify translations, source mappings, and evidence affected by an edit.
    1. Separate effects on meaning, examples, warnings, links, and diagrams.
    2. Identify both pages and source sections that need another full review.
    3. Distinguish completed checks from checks not yet run.
    Return: review item | evidence | status | next check.
    ```

=== "한국어"

    ```text {.prompt}
    내용을 바꾼 뒤 어떤 번역·출처·검증 증거를 갱신해야 하는지 확인한다.
    1. 의미·예시·경고·링크·도식에 미친 영향을 구분해 주세요.
    2. 다시 읽어야 할 양쪽 페이지와 출처 구간을 지정해 주세요.
    3. 실행한 검사와 아직 실행하지 않은 검사를 분리해 주세요.
    검토 항목 | 근거 | 상태 | 다음 확인 표를 주세요.
    ```

**Key point:** Evidence to check first: pages actually reviewed and logs of checks actually run. Keep source locations and mark unavailable sections before review. It may treat new hashes as proof that semantic review happened. Do not claim completion from updated hashes without semantic comparison or actual check logs.
