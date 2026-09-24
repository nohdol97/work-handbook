---
id: prompts-governance
status: overview
last_updated: 2026-09-24
last_reviewed: 2026-09-24
knowledge_ids: []
---

# Data governance practical prompts

These reusable, hypothetical work examples were authored from existing study concepts. They are not records of model runs, production work, or experiments. Fill placeholders with sanitized information safe to share. Treat results as hypotheses and drafts.

[Concept guide](../data-platform/governance.md) · [Prompt library](index.md)

| Case | Jump to example |
| --- | --- |
| 01 | [Clarify ownership and change responsibility](#governance-01) |
| 02 | [Connect classification to access and masking](#governance-02) |
| 03 | [Plan policy checks for each access path](#governance-03) |
| 04 | [Separate retention needs from snapshot policies](#governance-04) |
| 05 | [Reconstruct access and changes from audit records](#governance-05) |
| 06 | [Review a producer-consumer data contract](#governance-06) |

## Clarify ownership and change responsibility {#governance-01}

**Situation:** Schema changes and KPI questions go to one team, so clarify responsibility.

**Context to Give the LLM:** Datasets, pipelines, schemas, SLOs, and KPI definitions: [sanitized list] / Current technical and business roles and unassigned items: [role list]

**Example Prompt:**

=== "English"

    ```text {.prompt}
    [Context]
    Datasets, pipelines, schemas, SLOs, and KPI definitions: [sanitized list]
    Current technical and business roles and unassigned items: [role list]
    [Task]
    Separate technical-owner and business-owner responsibilities.
    Name roles to consult for quality incidents, meaning changes, and schema changes.
    Separate observations, assumptions, hypotheses, and missing evidence.
    [Output]
    Give a table of dataset, responsibility, role, unassigned scope, and questions.
    List uncertainties and the order of checks for the owner.
    [Checks]
    Compare agreed roles with catalog owners and confirm unassigned responsibilities.
    These checks are a plan; do not claim they were run.
    Do not change systems, delete data, or send data externally.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    데이터셋·pipeline·schema·SLO·KPI 정의: [비식별 목록]
    현재 기술·업무 담당 역할과 미지정 항목: [역할 목록]
    [요청]
    Technical owner와 Business owner의 책임을 구분하세요.
    품질 장애·의미 변경·schema 변경별 협의 대상을 제시하세요.
    관찰·가정·가설·누락 근거를 구분하세요.
    [출력]
    데이터셋 / 책임 / 담당 역할 / 미지정 범위 / 확인 질문 표를 주세요.
    불확실한 항목과 담당자가 다음에 확인할 순서를 적으세요.
    [검증]
    실제 역할 합의와 catalog owner 정보를 대조하고 미지정 책임을 확인하세요.
    위 검증은 계획이며 실행했다고 주장하지 마세요.
    실제 시스템 변경·데이터 삭제·외부 전송은 실행하지 마세요.
    ```

**Expected Output:** Give a table of dataset, responsibility, role, unassigned scope, and questions.

**What the LLM Can Get Wrong:** It may assign final business-meaning decisions to a pipeline owner without agreement.

**How to Validate:** Compare agreed roles with catalog owners and confirm unassigned responsibilities.

## Connect classification to access and masking {#governance-02}

**Situation:** Identify the policy review needed for sensitive fields in a new schema.

**Context to Give the LLM:** Field names, meanings, synthetic value types, and classification scheme: [definitions] / Role purposes, access, masking, and retention rules: [approved policy]

**Example Prompt:**

=== "English"

    ```text {.prompt}
    [Context]
    Field names, meanings, synthetic value types, and classification scheme: [definitions]
    Role purposes, access, masking, and retention rules: [approved policy]
    [Task]
    Assess importance levels separately from data types such as PII.
    Review policy links while separating column access from value masking.
    Separate observations, assumptions, hypotheses, and missing evidence.
    [Output]
    Give a table of column, classification evidence, access roles, masking, and retention questions.
    List uncertainties and the order of checks for the owner.
    [Checks]
    Confirm classifications and expected role results with policy owners using synthetic values.
    These checks are a plan; do not claim they were run.
    Do not change systems, delete data, or send data externally.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    필드명·의미·가상 값 유형·기존 분류 체계: [정의]
    역할별 사용 목적·접근·마스킹·보관 규칙: [승인된 정책]
    [요청]
    중요도 등급과 PII 같은 데이터 성격을 별도로 평가하세요.
    column 접근 제한과 값 마스킹을 구분해 정책 연결을 검토하세요.
    관찰·가정·가설·누락 근거를 구분하세요.
    [출력]
    column / 분류 근거 / 접근 대상 / 마스킹 / 보관 질문 표를 주세요.
    불확실한 항목과 담당자가 다음에 확인할 순서를 적으세요.
    [검증]
    정책 담당자에게 분류·역할별 기대 결과를 확인하고 가상 값으로 검토하세요.
    위 검증은 계획이며 실행했다고 주장하지 마세요.
    실제 시스템 변경·데이터 삭제·외부 전송은 실행하지 마세요.
    ```

**Expected Output:** Give a table of column, classification evidence, access roles, masking, and retention questions.

**What the LLM Can Get Wrong:** It may make PII the top of every classification scale or treat masking as encryption.

**How to Validate:** Confirm classifications and expected role results with policy owners using synthetic values.

## Plan policy checks for each access path {#governance-03}

**Situation:** Policies appear in the catalog, but enforcement across engines is unknown.

**Context to Give the LLM:** Roles, row/column policies, and expected masking results: [definitions] / Engines, runtimes, APIs, storage paths, and support evidence: [list]

**Example Prompt:**

=== "English"

    ```text {.prompt}
    [Context]
    Roles, row/column policies, and expected masking results: [definitions]
    Engines, runtimes, APIs, storage paths, and support evidence: [list]
    [Task]
    Separate displayed policies from enforcement on real query paths.
    State allow, deny, and masking expectations for each path and mark unknown support.
    Separate observations, assumptions, hypotheses, and missing evidence.
    [Output]
    Give a role-by-path check matrix and required official-doc and configuration evidence.
    List uncertainties and the order of checks for the owner.
    [Checks]
    Check installed-version docs, configuration, and isolated queries against synthetic data.
    These checks are a plan; do not claim they were run.
    Do not change systems, delete data, or send data externally.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    역할·row/column 정책·마스킹 기대 결과: [정의]
    엔진·runtime·API·storage 경로와 지원 근거: [목록]
    [요청]
    표시된 정책과 실제 조회 경로의 강제 적용을 구분하세요.
    각 경로에 허용·거부·마스킹 기대 결과를 정하고 미확인 지원을 표시하세요.
    관찰·가정·가설·누락 근거를 구분하세요.
    [출력]
    역할 × 경로 검증 표와 필요한 공식 문서·설정 증거를 주세요.
    불확실한 항목과 담당자가 다음에 확인할 순서를 적으세요.
    [검증]
    설치된 버전의 문서·설정과 격리된 가상 데이터 조회 결과로 확인하세요.
    위 검증은 계획이며 실행했다고 주장하지 마세요.
    실제 시스템 변경·데이터 삭제·외부 전송은 실행하지 마세요.
    ```

**Expected Output:** Give a role-by-path check matrix and required official-doc and configuration evidence.

**What the LLM Can Get Wrong:** It may generalize one engine's behavior to every storage and API path.

**How to Validate:** Check installed-version docs, configuration, and isolated queries against synthetic data.

## Separate retention needs from snapshot policies {#governance-04}

**Situation:** Storage cost needs review, but source, snapshot, and backup retention needs differ.

**Context to Give the LLM:** Data types, analytical value, sensitivity, and approved retention needs: [list] / Snapshot references, backups, active writes, and Hot/Cold/Archive setup: [state]

**Example Prompt:**

=== "English"

    ```text {.prompt}
    [Context]
    Data types, analytical value, sensitivity, and approved retention needs: [list]
    Snapshot references, backups, active writes, and Hot/Cold/Archive setup: [state]
    [Task]
    Separate data retention requirements from snapshot retention periods.
    Review storage-tier choices and cleanup risks without executing deletion.
    Separate observations, assumptions, hypotheses, and missing evidence.
    [Output]
    Give a table of scope, approved need, current retention, reference/write risks, and questions.
    List uncertainties and the order of checks for the owner.
    [Checks]
    Have policy owners confirm requirements and compare snapshot, backup, and run state.
    These checks are a plan; do not claim they were run.
    Do not change systems, delete data, or send data externally.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    데이터 유형·분석 가치·민감도·승인된 보관 요구: [목록]
    snapshot 참조·backup·활성 쓰기·Hot/Cold/Archive 구성: [현황]
    [요청]
    데이터 보관 요구와 snapshot 보존 기간을 분리하세요.
    보관 계층 선택과 정리 위험을 검토하되 삭제 작업은 실행하지 마세요.
    관찰·가정·가설·누락 근거를 구분하세요.
    [출력]
    대상 / 승인 요구 / 현재 보관 / 참조·쓰기 위험 / 확인 질문 표를 주세요.
    불확실한 항목과 담당자가 다음에 확인할 순서를 적으세요.
    [검증]
    정책 owner가 요구를 확인하고 snapshot 참조·backup·실행 상태를 대조하세요.
    위 검증은 계획이며 실행했다고 주장하지 마세요.
    실제 시스템 변경·데이터 삭제·외부 전송은 실행하지 마세요.
    ```

**Expected Output:** Give a table of scope, approved need, current retention, reference/write risks, and questions.

**What the LLM Can Get Wrong:** It may use an example 14 days as a legal default or mistake active files for orphans.

**How to Validate:** Have policy owners confirm requirements and compare snapshot, backup, and run state.

## Reconstruct access and changes from audit records {#governance-05}

**Situation:** Review which roles accessed which data after a policy change.

**Context to Give the LLM:** Anonymous roles, datasets, times, actions, and query types: [sanitized audit summary] / Schema, policy, owner, and retention changes and logging gaps: [history]

**Example Prompt:**

=== "English"

    ```text {.prompt}
    [Context]
    Anonymous roles, datasets, times, actions, and query types: [sanitized audit summary]
    Schema, policy, owner, and retention changes and logging gaps: [history]
    [Task]
    Separate access and change audits and connect them by time.
    Treat who did what and whether data was healthy as separate questions.
    Separate observations, assumptions, hypotheses, and missing evidence.
    [Output]
    Give a table of time, role, target, action, policy state, and unverified scope.
    List uncertainties and the order of checks for the owner.
    [Checks]
    Compare audit coverage and policy-change records and review results without identifiers.
    These checks are a plan; do not claim they were run.
    Do not change systems, delete data, or send data externally.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    익명 역할·dataset·시각·action·query 유형: [비식별 감사 요약]
    schema·정책·owner·보관 변경과 수집 공백: [이력]
    [요청]
    접근 감사와 변경 감사를 구분해 시간순으로 연결하세요.
    누가 무엇을 했는지와 데이터가 정상인지를 서로 다른 질문으로 다루세요.
    관찰·가정·가설·누락 근거를 구분하세요.
    [출력]
    시각 / 역할 / 대상 / 행위 / 정책 상태 / 확인되지 않은 구간 표를 주세요.
    불확실한 항목과 담당자가 다음에 확인할 순서를 적으세요.
    [검증]
    감사 수집 범위와 정책 변경 기록을 대조하고 식별값 없이 결과를 검토하세요.
    위 검증은 계획이며 실행했다고 주장하지 마세요.
    실제 시스템 변경·데이터 삭제·외부 전송은 실행하지 마세요.
    ```

**Expected Output:** Give a table of time, role, target, action, policy state, and unverified scope.

**What the LLM Can Get Wrong:** It may read missing logs as no access or expose sensitive values in raw queries.

**How to Validate:** Compare audit coverage and policy-change records and review results without identifiers.

## Review a producer-consumer data contract {#governance-06}

**Situation:** A schema is agreed, but units, quality, freshness, and ownership are missing.

**Context to Give the LLM:** event_id, latency_ms, and status definitions: [draft contract] / Producer and consumer needs, SLO, owner, and version: [agreed and open items]

**Example Prompt:**

=== "English"

    ```text {.prompt}
    [Context]
    event_id, latency_ms, and status definitions: [draft contract]
    Producer and consumer needs, SLO, owner, and version: [agreed and open items]
    [Task]
    Review meanings, units, required values, uniqueness, and ranges as well as types.
    List questions for missing quality, freshness, ownership, and version agreements.
    Separate observations, assumptions, hypotheses, and missing evidence.
    [Output]
    Give a table of contract item, definition, ambiguity, synthetic violation, and parties to consult.
    List uncertainties and the order of checks for the owner.
    [Checks]
    Check interpretation with both owners' requirements and valid and invalid synthetic events.
    These checks are a plan; do not claim they were run.
    Do not change systems, delete data, or send data externally.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    event_id·latency_ms·상태 필드 정의: [계약 초안]
    producer·consumer 요구·SLO·owner·version: [합의와 미합의]
    [요청]
    타입뿐 아니라 의미·단위·필수·유일·범위 조건을 검토하세요.
    품질·최신성·소유권·버전의 빠진 약속을 질문으로 남기세요.
    관찰·가정·가설·누락 근거를 구분하세요.
    [출력]
    계약 항목 / 현재 정의 / 모호함 / 가상 위반 예 / 합의 대상 표를 주세요.
    불확실한 항목과 담당자가 다음에 확인할 순서를 적으세요.
    [검증]
    양측 담당자의 요구와 정상·위반 가상 이벤트로 계약 해석을 확인하세요.
    위 검증은 계획이며 실행했다고 주장하지 마세요.
    실제 시스템 변경·데이터 삭제·외부 전송은 실행하지 마세요.
    ```

**Expected Output:** Give a table of contract item, definition, ambiguity, synthetic violation, and parties to consult.

**What the LLM Can Get Wrong:** It may assume an integer implies milliseconds or turn a proposed SLO into an approved promise.

**How to Validate:** Check interpretation with both owners' requirements and valid and invalid synthetic events.
