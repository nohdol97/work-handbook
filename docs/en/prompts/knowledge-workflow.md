---
id: prompts-knowledge-workflow
status: overview
last_updated: 2026-09-24
last_reviewed: 2026-09-24
knowledge_ids: []
---

# Knowledge workflow prompts

These four authored examples apply the existing knowledge workflow. They are not model runs or measured work results. Replace bracketed inputs with sanitized material, choose a prompt language, and copy.

[Concept guide](../methodologies/knowledge-workflow.md) · [Prompt library](index.md)

| Situation | Jump to example |
|---|---|
| Extract knowledge before drafting | [01](#knowledge-workflow-01) |
| Compare bilingual constraints and warnings | [02](#knowledge-workflow-02) |
| Merge new material without losing conditions | [03](#knowledge-workflow-03) |
| Plan review after a documentation change | [04](#knowledge-workflow-04) |

## Extract knowledge before drafting {#knowledge-workflow-01}

**Situation:** Find what must be retained before turning meeting or study notes into documentation.

**Context to give:** The full sanitized source, scope, existing outline, and unavailable sections.

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

**Expected output:** An extraction table with source locations, types, destinations, and missing evidence.

**What can go wrong:** It may drop constraints or counterexamples while summarizing.

**How to validate:** Compare every source section, example, number, and failure condition with the table.

## Compare bilingual constraints and warnings {#knowledge-workflow-02}

**Situation:** Check whether required conditions, prohibitions, and numbers survive translation.

**Context to give:** Full Korean and English pages, the glossary, and changed source sections.

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

**Expected output:** Located semantic differences, minimal edits, and ambiguities needing review.

**What can go wrong:** It may change must to may while making a translation sound natural.

**How to validate:** Check examples, warnings, conditions, and numbers against the source in both languages. Have a person perform the final review.

## Merge new material without losing conditions {#knowledge-workflow-03}

**Situation:** New material covers an existing topic whose correct knowledge must remain.

**Context to give:** Existing bilingual pages, new source and IDs, canonical destinations, and conflicts.

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

**Expected output:** Per-item Included/Merged/Deferred/Excluded proposals with reasons and destinations.

**What can go wrong:** It may delete content with different conditions because wording looks similar.

**How to validate:** Check that every old and new ID is mapped and each deferred or excluded item has a specific reason.

## Plan review after a documentation change {#knowledge-workflow-04}

**Situation:** Identify translations, source mappings, and evidence affected by an edit.

**Context to give:** The diff, full bilingual pages, prior review records, and actual check results.

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

**Expected output:** Affected scope, review tasks, passing evidence, and unverified areas.

**What can go wrong:** It may treat new hashes as proof that semantic review happened.

**How to validate:** Check the full-page review and actual logs, then compare current file hashes with the record.
