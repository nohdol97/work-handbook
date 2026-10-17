---
id: prompts-governance
status: overview
last_updated: 2026-10-18
last_reviewed: 2026-10-18
knowledge_ids: []
---

# Data governance practical prompts

Copy these examples with the relevant SQL, settings, logs, or proposed changes. Use sanitized material and check suggestions against real evidence and permissions. An example does not authorize system changes or data deletion. These are not measured usage or model-performance results.

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

**Prompt:**

=== "English"

    ```text {.prompt}
    Schema changes and KPI questions go to one team, so clarify responsibility.
    Separate technical-owner and business-owner responsibilities.
    Name roles to consult for quality incidents, meaning changes, and schema changes.
    Give a table of dataset, responsibility, role, unassigned scope, and questions.
    Review only; do not apply changes.
    ```

=== "한국어"

    ```text {.prompt}
    schema 변경과 KPI 문의가 같은 창구로 몰려 책임을 나눈다.
    Technical owner와 Business owner의 책임을 구분하세요.
    품질 장애·의미 변경·schema 변경별 협의 대상을 제시하세요.
    데이터셋 / 책임 / 담당 역할 / 미지정 범위 / 확인 질문 표를 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

**Key point:** Evidence to check first: agreed roles and unassigned responsibilities. Provide approved policies separately from proposals under review. It may assign final business-meaning decisions to a pipeline owner without agreement. Do not assign final business-meaning authority to technical owners without agreement.

## Connect classification to access and masking {#governance-02}

**Prompt:**

=== "English"

    ```text {.prompt}
    Identify the policy review needed for sensitive fields in a new schema.
    Assess importance levels separately from data types such as PII.
    Review policy links while separating column access from value masking.
    Give a table of column, classification evidence, access roles, masking, and retention questions.
    Review only; do not apply changes.
    ```

=== "한국어"

    ```text {.prompt}
    새 schema의 민감 필드에 어떤 검토가 필요한지 정리하려고 해.
    중요도 등급과 PII 같은 데이터 성격을 별도로 평가하세요.
    column 접근 제한과 값 마스킹을 구분해 정책 연결을 검토하세요.
    column / 분류 근거 / 접근 대상 / 마스킹 / 보관 질문 표를 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

**Key point:** Evidence to check first: the approved classification scheme and role-specific purposes. Provide approved policies separately from proposals under review. It may make PII the top of every classification scale or treat masking as encryption. Do not finalize sensitivity or allowed roles from field names alone.

## Plan policy checks for each access path {#governance-03}

**Prompt:**

=== "English"

    ```text {.prompt}
    Policies appear in the catalog, but enforcement across engines is unknown.
    Separate displayed policies from enforcement on real query paths.
    State allow, deny, and masking expectations for each path and mark unknown support.
    Give a role-by-path check matrix and required official-doc and configuration evidence.
    Review only; do not apply changes.
    ```

=== "한국어"

    ```text {.prompt}
    catalog에는 정책이 보이지만 여러 엔진에서 같은 제어가 적용되는지 모른다.
    표시된 정책과 실제 조회 경로의 강제 적용을 구분하세요.
    각 경로에 허용·거부·마스킹 기대 결과를 정하고 미확인 지원을 표시하세요.
    역할 × 경로 검증 표와 필요한 공식 문서·설정 증거를 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

**Key point:** Evidence to check first: actual API, engine, and storage access paths. Provide approved policies separately from proposals under review. It may generalize one engine's behavior to every storage and API path. Do not generalize one successful path check to all access paths.

## Separate retention needs from snapshot policies {#governance-04}

**Prompt:**

=== "English"

    ```text {.prompt}
    Storage cost needs review, but source, snapshot, and backup retention needs differ.
    Separate data retention requirements from snapshot retention periods.
    Review storage-tier choices and cleanup risks without executing deletion.
    Give a table of scope, approved need, current retention, reference/write risks, and questions.
    Review only; do not apply changes.
    ```

=== "한국어"

    ```text {.prompt}
    저장 비용을 줄이려는데 원본·snapshot·backup의 보관 요구가 다르다.
    데이터 보관 요구와 snapshot 보존 기간을 분리하세요.
    보관 계층 선택과 정리 위험을 검토하되 삭제 작업은 실행하지 마세요.
    대상 / 승인 요구 / 현재 보관 / 참조·쓰기 위험 / 확인 질문 표를 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

**Key point:** Evidence to check first: owner-confirmed retention needs for sources, snapshots, and backups. Provide approved policies separately from proposals under review. It may use an example 14 days as a legal default or mistake active files for orphans. Do not equate moving storage tiers with completed physical deletion.

## Reconstruct access and changes from audit records {#governance-05}

**Prompt:**

=== "English"

    ```text {.prompt}
    Review which roles accessed which data after a policy change.
    Separate access and change audits and connect them by time.
    Treat who did what and whether data was healthy as separate questions.
    Give a table of time, role, target, action, policy state, and unverified scope.
    Review only; do not apply changes.
    ```

=== "한국어"

    ```text {.prompt}
    정책 변경 뒤 어떤 역할이 어떤 데이터에 접근했는지 검토 중이야.
    접근 감사와 변경 감사를 구분해 시간순으로 연결하세요.
    누가 무엇을 했는지와 데이터가 정상인지를 서로 다른 질문으로 다루세요.
    시각 / 역할 / 대상 / 행위 / 정책 상태 / 확인되지 않은 구간 표를 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

**Key point:** Evidence to check first: audit collection scope and policy-change times. Provide approved policies separately from proposals under review. It may read missing logs as no access or expose sensitive values in raw queries. Do not use missing logs as evidence of no access or policy compliance.

## Review a producer-consumer data contract {#governance-06}

**Prompt:**

=== "English"

    ```text {.prompt}
    A schema is agreed, but units, quality, freshness, and ownership are missing.
    Review meanings, units, required values, uniqueness, and ranges as well as types.
    List questions for missing quality, freshness, ownership, and version agreements.
    Give a table of contract item, definition, ambiguity, synthetic violation, and parties to consult.
    Review only; do not apply changes.
    ```

=== "한국어"

    ```text {.prompt}
    schema는 합의했지만 단위·품질·최신성·owner가 빠져 해석이 다르다.
    타입뿐 아니라 의미·단위·필수·유일·범위 조건을 검토하세요.
    품질·최신성·소유권·버전의 빠진 약속을 질문으로 남기세요.
    계약 항목 / 현재 정의 / 모호함 / 가상 위반 예 / 합의 대상 표를 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

**Key point:** Evidence to check first: meanings, SLOs, and change ownership agreed by producer and consumer. Provide approved policies separately from proposals under review. It may assume an integer implies milliseconds or turn a proposed SLO into an approved promise. Finish the review with proposed targets clearly separate from approved commitments.
