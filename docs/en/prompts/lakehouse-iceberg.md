---
id: prompts-lakehouse-iceberg
status: overview
last_updated: 2026-10-18
last_reviewed: 2026-10-18
knowledge_ids: []
---

# Lakehouse and Iceberg practical prompts

Copy these examples with the relevant SQL, settings, logs, or proposed changes. Use sanitized material and check suggestions against real evidence and permissions. An example does not authorize system changes or data deletion. These are not measured usage or model-performance results.

[All prompts](index.md) · [Concepts and sources](../data-platform/lakehouse-iceberg.md)

## Quick selection

| Purpose | Jump to |
| --- | --- |
| Check whether two queries read different snapshots | [01](#lakehouse-iceberg-01) |
| Review old files after partition evolution | [02](#lakehouse-iceberg-02) |
| Review copy-on-write versus merge-on-read | [03](#lakehouse-iceberg-03) |
| Prioritize maintenance work | [04](#lakehouse-iceberg-04) |
| Review snapshot retention and cleanup safety | [05](#lakehouse-iceberg-05) |
| Review catalog and governance responsibilities | [06](#lakehouse-iceberg-06) |

## Check whether two queries read different snapshots {#lakehouse-iceberg-01}

Example prompt:

=== "English"

    ```text {.prompt}
    Two engines return different results for the same table.
    Explain the references from catalog to metadata, snapshot, manifests, and files.
    Separate different-snapshot and same-snapshot differences; do not start with rollback.
    Return reference-mismatch hypotheses and a read-only checklist for a fixed-snapshot comparison.
    Review only; do not apply changes.
    ```

=== "한국어"

    ```text {.prompt}
    같은 테이블을 조회했지만 두 엔진의 결과가 다른 상황이야.
    Catalog에서 metadata, snapshot, manifest, 파일로 이어지는 참조를 설명해 줘.
    서로 다른 snapshot과 같은 snapshot 내 차이를 나누고 rollback부터 제안하지 마.
    참조 불일치 가설과 고정 snapshot 비교의 읽기 전용 점검표를 작성해 줘.
    검토만 하고 변경은 실행하지 마.
    ```

**Key point:** Evidence to check first: the snapshot ID and conditions actually used by each query. Align read-only metadata and query evidence to the same point in time. The LLM may infer current state from a metadata filename or treat a snapshot as a full data copy. Do not infer equal snapshots from metadata filenames or query times alone.

## Review old files after partition evolution {#lakehouse-iceberg-02}

Example prompt:

=== "English"

    ```text {.prompt}
    Old-data queries stay slow after changing the spec from day to hour.
    Explain the current state by separating a spec change from rewriting old files.
    Explain how filters can support pruning across mixed specs and mark missing evidence.
    Return a recent-versus-historical query table and criteria for considering a selective rewrite.
    Review only; do not apply changes.
    ```

=== "한국어"

    ```text {.prompt}
    Day에서 hour로 partition spec을 바꿨는데 과거 조회는 느린 상황이야.
    Spec 변경과 과거 파일 rewrite를 구분해서 현재 상태를 설명해 줘.
    혼합 spec에서 필터가 어떻게 pruning에 쓰이는지 근거와 미확인 부분을 나눠 줘.
    최근·과거 조회 비교표와 선택적 rewrite 검토 조건을 작성해 줘.
    검토만 하고 변경은 실행하지 마.
    ```

**Key point:** Evidence to check first: old and new spec IDs and the spec associated with historical files. Align read-only metadata and query evidence to the same point in time. The LLM may assume old files are rearranged automatically or all engines use identical SQL. Compare results and scan costs on samples containing both old and new files.

## Review copy-on-write versus merge-on-read {#lakehouse-iceberg-03}

Example prompt:

=== "English"

    ```text {.prompt}
    Review read and write cost for a table with frequent small row changes.
    Compare file-rewrite cost with the cost of applying deletes during reads.
    Include data files for replacement values and delete maintenance; do not assume support.
    Return a conditional decision table and a plan to measure read and write amplification.
    Review only; do not apply changes.
    ```

=== "한국어"

    ```text {.prompt}
    소량의 row 변경이 자주 발생하는 테이블의 읽기·쓰기 비용을 검토 중이야.
    파일 rewrite 비용과 읽을 때 delete를 적용하는 비용을 비교해 줘.
    새 값의 data file 기록과 delete maintenance도 포함하고 지원 여부를 가정하지 마.
    조건별 선택표와 read/write amplification을 측정할 계획을 작성해 줘.
    검토만 하고 변경은 실행하지 마.
    ```

**Key point:** Evidence to check first: row-change support for the engine and connector and the read-latency target. Align read-only metadata and query evidence to the same point in time. The LLM may claim merge-on-read is always faster or replacement values live only in delete files. Include delete application and maintenance costs rather than choosing only by write speed.

## Prioritize maintenance work {#lakehouse-iceberg-04}

Example prompt:

=== "English"

    ```text {.prompt}
    Inspect an Iceberg table with slow planning and scans.
    Separate the purposes of data compaction, delete rewrite, and manifest rewrite.
    Prioritize work by the observed bottleneck; do not recommend all tasks at once.
    Return evidence, expected cost, metrics, and stop conditions for each candidate task.
    Review only; do not apply changes.
    ```

=== "한국어"

    ```text {.prompt}
    쿼리 planning과 scan이 모두 느려진 Iceberg 테이블을 점검한다.
    Data compaction, delete rewrite, manifest rewrite의 목적을 각각 구분해 줘.
    관찰된 병목에 맞게 우선순위를 정하고 모든 작업을 한 번에 권하지 마.
    작업별 근거·예상 비용·측정 지표·중단 조건의 검토표를 작성해 줘.
    검토만 하고 변경은 실행하지 마.
    ```

**Key point:** Evidence to check first: separate observations of planning and scan time. Align read-only metadata and query evidence to the same point in time. The LLM may assume data compaction fixes all metadata issues or maintenance has no cost. Lower the priority of maintenance work not tied to the observed bottleneck.

## Review snapshot retention and cleanup safety {#lakehouse-iceberg-05}

Example prompt:

=== "English"

    ```text {.prompt}
    Review a snapshot cleanup plan intended to reduce storage cost.
    Separate snapshot expiration from orphan cleanup and identify possibly referenced files.
    Review whether files absent from the current snapshot belong to older snapshots or in-flight writes.
    Return only retention questions and a read-only preflight checklist.
    Review only; do not apply changes.
    ```

=== "한국어"

    ```text {.prompt}
    스토리지 비용을 줄이기 위한 snapshot 정리 계획을 검토 중이야.
    Snapshot expiration과 orphan cleanup을 구분하고 참조 중 파일을 찾아 줘.
    현재 snapshot에 없는 파일도 과거 snapshot이나 진행 중 write와 관련되는지 검토해 줘.
    보존 기간 결정에 필요한 질문과 읽기 전용 사전 점검표만 작성해 줘.
    검토만 하고 변경은 실행하지 마.
    ```

**Key point:** Evidence to check first: retained snapshot references and the longest in-flight write duration. Align read-only metadata and query evidence to the same point in time. The LLM may recommend deletion based only on the current snapshot or invent a short retention period. Hold files with unclear references out of any deletion candidate list.

## Review catalog and governance responsibilities {#lakehouse-iceberg-06}

Example prompt:

=== "English"

    ```text {.prompt}
    Map responsibilities in an environment where several compute engines use one table.
    Separate finding current metadata from broader governance responsibilities.
    Mark evidence of policy enforcement for each engine path and unverified integrations.
    Return a responsibility matrix and questions to check for each product and version.
    Review only; do not apply changes.
    ```

=== "한국어"

    ```text {.prompt}
    여러 compute 엔진이 같은 테이블을 쓰는 환경의 책임을 정리하려고 해.
    Table 이름에서 현재 metadata를 찾는 책임과 governance 책임을 구분해 줘.
    각 엔진 경로에 정책이 적용되는 근거와 아직 확인하지 못한 연동을 표시해 줘.
    책임 행렬과 제품·버전별로 확인해야 할 질문을 작성해 줘.
    검토만 하고 변경은 실행하지 마.
    ```

**Key point:** Evidence to check first: metadata lookup paths and policy enforcement points by engine. Align read-only metadata and query evidence to the same point in time. The LLM may equate catalog registration with complete access control or equate Unity Catalog with an Iceberg catalog. Record successful table discovery separately from verified access control.
