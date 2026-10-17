---
id: prompts-cdc-debezium
status: overview
last_updated: 2026-10-18
last_reviewed: 2026-10-18
knowledge_ids: []
---

# CDC and Debezium practical prompts

Copy these examples with the relevant SQL, settings, logs, or proposed changes. Use sanitized material and check suggestions against real evidence and permissions. An example does not authorize system changes or data deletion. These are not measured usage or model-performance results.

[Concept guide](../data-platform/cdc-debezium.md) · [All prompts](index.md)

| # | Jump to a situation |
| --- | --- |
| 01 | [Decide how to resume an interrupted snapshot](#cdc-debezium-01) |
| 02 | [Define delete and tombstone handling](#cdc-debezium-02) |
| 03 | [Review downstream impact of a schema change](#cdc-debezium-03) |
| 04 | [Review a transaction across multiple tables](#cdc-debezium-04) |
| 05 | [Check missed deletes when moving from polling to CDC](#cdc-debezium-05) |
| 06 | [Design history and current-state reconciliation](#cdc-debezium-06) |

## Decide how to resume an interrupted snapshot {#cdc-debezium-01}

**Prompt:**

=== "English"

    ```text {.prompt}
    The connector stopped during initial loading. Decide whether a new snapshot is needed.
    Separate observed completion state from assumed recovery options.
    Compare resume and reinitialization options using offset and WAL evidence.
    List unconfirmed snapshot behavior as version-specific checks.
    Return a decision table and missing evidence for each condition.
    Review only; do not apply changes.
    ```

=== "한국어"

    ```text {.prompt}
    초기 적재 중 connector가 멈춰 snapshot을 다시 시작할지 판단한다.
    관찰한 완료 상태와 추정한 복구 가능성을 구분해 주세요.
    Offset과 WAL 근거별로 재개·재초기화 후보를 비교해 주세요.
    확인되지 않은 snapshot 동작은 버전별 확인 항목으로 남겨 주세요.
    조건별 판단표와 부족한 증거를 작성해 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

**Key point:** Evidence to check first: the stored offset, snapshot completion record, and required WAL availability. Keep source-to-target key mappings while consistently replacing identifiers. The LLM may assume that every restart skips the snapshot or restores lost history. Distinguish rebuilding current state from recovering intermediate changes.

## Define delete and tombstone handling {#cdc-debezium-02}

**Prompt:**

=== "English"

    ```text {.prompt}
    A row deleted at the source still appears in current-state queries.
    Separate a database delete from a Kafka compaction record.
    Review stored results and query conditions for physical and logical deletes.
    Identify required key evidence when before lacks the full old row.
    Return expected history and current-state results for each input event.
    Review only; do not apply changes.
    ```

=== "한국어"

    ```text {.prompt}
    소스에서 삭제한 행이 current-state 조회에 남아 있다.
    DB 삭제 사실과 Kafka compaction record를 구분해 주세요.
    Physical·logical delete별 저장 결과와 조회 조건을 검토해 주세요.
    before의 전체 행이 없을 때 필요한 key 근거를 찾아 주세요.
    입력 event별 history·current-state 기대 결과표를 만들어 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

**Key point:** Evidence to check first: real DELETE/tombstone samples and the sink delete policy. Keep source-to-target key mappings while consistently replacing identifiers. The LLM may treat a tombstone as a business delete or include logically deleted rows in queries. Require history and current state to meet their separate contracts after redelivery.

## Review downstream impact of a schema change {#cdc-debezium-03}

**Prompt:**

=== "English"

    ```text {.prompt}
    Review the path from CDC to BI before renaming a source column.
    Compare rename, type, and nullability changes with consumer expectations.
    Do not assume CDC emits every DDL event.
    Separate confirmed impact, compatibility assumptions, and missing consumers.
    Return a table of failure conditions, check owners, and evidence by component.
    Review only; do not apply changes.
    ```

=== "한국어"

    ```text {.prompt}
    원본 column을 rename하기 전에 CDC부터 BI까지 영향을 확인한다.
    Rename·type·nullable 변경을 각 소비자의 기대 schema와 비교해 주세요.
    CDC가 DDL event를 모두 보낸다고 가정하지 말아 주세요.
    확인된 영향과 호환성 가설, 누락된 소비자를 구분해 주세요.
    구성 요소별 실패 조건·확인 담당·검증 근거 표를 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

**Key point:** Evidence to check first: the schema diff to deploy and actual downstream consumers. Keep source-to-target key mappings while consistently replacing identifiers. The LLM may assume nullable additions are always safe or renames propagate automatically. Include schema changes not carried by CDC in consumer checks.

## Review a transaction across multiple tables {#cdc-debezium-04}

**Prompt:**

=== "English"

    ```text {.prompt}
    Orders and payments change in one DB transaction but reach consumers at different times.
    Separate DB transaction boundaries from Kafka partition ordering scope.
    Analyze same-key order and cross-table arrival differences separately.
    Mark unverified metadata support and settings as assumptions.
    Return a table of observable order and order that is not guaranteed.
    Review only; do not apply changes.
    ```

=== "한국어"

    ```text {.prompt}
    주문과 결제가 같은 DB transaction에서 바뀌지만 소비자가 다른 시점에 본다.
    DB transaction 경계와 Kafka partition 순서 범위를 나눠 주세요.
    같은 key의 순서와 테이블 사이 도착 차이를 따로 분석해 주세요.
    Metadata 지원·설정이 확인되지 않은 부분은 가정으로 표시해 주세요.
    관측 가능한 순서와 보장되지 않는 순서의 표를 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

**Key point:** Evidence to check first: source transaction identifiers and partition order by table. Keep source-to-target key mappings while consistently replacing identifiers. The LLM may assume DB atomicity guarantees simultaneous visibility downstream. Do not equate Kafka arrival order with source transaction atomicity.

## Check missed deletes when moving from polling to CDC {#cdc-debezium-05}

**Prompt:**

=== "English"

    ```text {.prompt}
    Deleted rows remain in a target table filled by updated_at polling. Review the collection limits.
    Mark whether the polling query can observe each change.
    Review snapshot, offset, and log-retention duties for the CDC option.
    Separate observations, assumptions, and missing requirements before a redesign.
    Return a requirements comparison for polling and log-based CDC.
    Review only; do not apply changes.
    ```

=== "한국어"

    ```text {.prompt}
    updated_at polling으로 채운 대상 테이블에 삭제된 행이 남아 수집 방식의 한계를 정리하려고 해.
    각 변경을 polling query가 관측할 수 있는지 표시해 주세요.
    CDC 후보의 snapshot·offset·로그 보존 책임을 함께 검토해 주세요.
    설계 변경 전에 관측 사실·가정·추가 요구를 분리해 주세요.
    Polling과 로그 기반 CDC의 요구 충족 비교표를 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

**Key point:** Evidence to check first: change samples including hard deletes and required history retention. Keep source-to-target key mappings while consistently replacing identifiers. The LLM may assume a shorter polling interval fixes delete detection and all missing history. Verify deletes, intermediate changes, and current state separately for the same keys across migration.

## Design history and current-state reconciliation {#cdc-debezium-06}

**Prompt:**

=== "English"

    ```text {.prompt}
    One ingestion flow needs separate checks for history and current-state tables.
    Do not treat history row count and current key count as the same measure.
    Derive expected state from order, duplicate, and delete rules within one source scope.
    Separate synchronization delay from true mismatch hypotheses.
    Return per-key checks for latest state, deletion, and retained history.
    Review only; do not apply changes.
    ```

=== "한국어"

    ```text {.prompt}
    동일 수집 흐름에서 이력 테이블과 현재 상태 테이블의 검증 기준이 필요하다.
    이력 행 수와 현재 존재하는 key 수를 같은 기준으로 보지 말아 주세요.
    동일 source 범위의 순서·중복·삭제 규칙으로 기대 상태를 구해 주세요.
    동기화 지연과 실제 불일치 가설을 구분해 주세요.
    Key별 최신 상태·삭제 여부·이력 보존 확인표를 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

**Key point:** Evidence to check first: a common comparison point and position-ordering scope for each source. Keep source-to-target key mappings while consistently replacing identifiers. The LLM may compare all history rows with current source rows or order positions across sources. Keep the check failing when counts match but per-key values or delete state differ.
