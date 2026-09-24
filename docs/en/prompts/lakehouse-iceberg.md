---
id: prompts-lakehouse-iceberg
status: overview
last_updated: 2026-09-24
last_reviewed: 2026-09-24
knowledge_ids: []
---

# Lakehouse and Iceberg practical prompts

Page type: Reference. These six authored, hypothetical examples apply the [existing study material](../data-platform/lakehouse-iceberg.md). They do not claim production experience, measured usage frequency, or model results. The examples were not run.

Choose a case and replace bracketed inputs with sanitized information. Each prompt has 한국어 and English tabs for language selection and copying. Treat LLM output as a hypothesis. Check actual settings, logs, official docs, and bounded tests. This page does not authorize production actions or permission changes.

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

- **Situation:** In this hypothetical case, two engines return different results for the same table.
- **Context to give the LLM:** Query evidence: [engines, queries, run times, observed snapshot IDs]; Metadata: [catalog, current pointer, snapshot history, concurrent writes].

Example prompt:

=== "English"

    ```text {.prompt}
    [Context]
    Query evidence: [engines, queries, run times, observed snapshot IDs]
    Metadata: [catalog, current pointer, snapshot history, concurrent writes]

    [Task]
    Explain the references from catalog to metadata, snapshot, manifests, and files.
    Separate different-snapshot and same-snapshot differences; do not start with rollback.
    Separate observations, assumptions, hypotheses, and missing evidence.

    [Output]
    Return reference-mismatch hypotheses and a read-only checklist for a fixed-snapshot comparison.

    [Checks]
    Verify that both read the same snapshot with the same conditions, then compare counts and aggregates.
    Provide review and test plans only; do not run or change production.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    조회 근거: [엔진·쿼리·실행 시각·관찰한 snapshot ID]
    메타데이터: [catalog·현재 pointer·snapshot 이력·동시 write]

    [요청]
    Catalog에서 metadata, snapshot, manifest, 파일로 이어지는 참조를 설명해 줘.
    서로 다른 snapshot과 같은 snapshot 내 차이를 나누고 rollback부터 제안하지 마.
    관찰, 가정, 가설, 부족한 근거를 구분해 줘.

    [출력]
    참조 불일치 가설과 고정 snapshot 비교의 읽기 전용 점검표를 작성해 줘.

    [검증]
    양쪽이 같은 snapshot과 동일 조건을 읽는지 확인하고 결과 수·집계를 대조해 줘.
    운영 실행·변경 없이 검토와 검증 계획만 제시해 줘.
    ```

- **Expected output:** Reference-mismatch hypotheses and a read-only checklist for a fixed-snapshot comparison.
- **What the LLM can get wrong:** The LLM may infer current state from a metadata filename or treat a snapshot as a full data copy.
- **How to validate:** Verify that both read the same snapshot with the same conditions, then compare counts and aggregates.

## Review old files after partition evolution {#lakehouse-iceberg-02}

- **Situation:** In this hypothetical case, old-data queries stay slow after changing the spec from day to hour.
- **Context to give the LLM:** Spec history: [old and current transforms, change time, spec IDs]; Queries and files: [time filters, spec per file, scan bytes, statistics].

Example prompt:

=== "English"

    ```text {.prompt}
    [Context]
    Spec history: [old and current transforms, change time, spec IDs]
    Queries and files: [time filters, spec per file, scan bytes, statistics]

    [Task]
    Explain the current state by separating a spec change from rewriting old files.
    Explain how filters can support pruning across mixed specs and mark missing evidence.
    Separate observations, assumptions, hypotheses, and missing evidence.

    [Output]
    Return a recent-versus-historical query table and criteria for considering a selective rewrite.

    [Checks]
    Inspect file specs and query plans, then compare scan bytes for the same time ranges.
    Provide review and test plans only; do not run or change production.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    Spec 이력: [이전·현재 transform·적용 시점·spec ID]
    조회와 파일: [시간 필터·파일별 spec·scan bytes·통계]

    [요청]
    Spec 변경과 과거 파일 rewrite를 구분해서 현재 상태를 설명해 줘.
    혼합 spec에서 필터가 어떻게 pruning에 쓰이는지 근거와 미확인 부분을 나눠 줘.
    관찰, 가정, 가설, 부족한 근거를 구분해 줘.

    [출력]
    최근·과거 조회 비교표와 선택적 rewrite 검토 조건을 작성해 줘.

    [검증]
    파일별 spec과 실행 계획을 확인하고 같은 시간 범위의 scan bytes를 비교해 줘.
    운영 실행·변경 없이 검토와 검증 계획만 제시해 줘.
    ```

- **Expected output:** A recent-versus-historical query table and criteria for considering a selective rewrite.
- **What the LLM can get wrong:** The LLM may assume old files are rearranged automatically or all engines use identical SQL.
- **How to validate:** Inspect file specs and query plans, then compare scan bytes for the same time ranges.

## Review copy-on-write versus merge-on-read {#lakehouse-iceberg-03}

- **Situation:** Review read and write cost for a hypothetical table with frequent small row changes.
- **Context to give the LLM:** Workload: [change rate, query frequency, read-latency target, file sizes]; Support: [engine, connector, format version, current delete representation].

Example prompt:

=== "English"

    ```text {.prompt}
    [Context]
    Workload: [change rate, query frequency, read-latency target, file sizes]
    Support: [engine, connector, format version, current delete representation]

    [Task]
    Compare file-rewrite cost with the cost of applying deletes during reads.
    Include data files for replacement values and delete maintenance; do not assume support.
    Separate observations, assumptions, hypotheses, and missing evidence.

    [Output]
    Return a conditional decision table and a plan to measure read and write amplification.

    [Checks]
    Check version support and compare file count, bytes written, and read latency for the same changes and queries.
    Provide review and test plans only; do not run or change production.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    Workload: [변경률·쿼리 빈도·읽기 지연 목표·파일 크기]
    지원 범위: [엔진·connector·format 버전·현재 delete 표현]

    [요청]
    파일 rewrite 비용과 읽을 때 delete를 적용하는 비용을 비교해 줘.
    새 값의 data file 기록과 delete maintenance도 포함하고 지원 여부를 가정하지 마.
    관찰, 가정, 가설, 부족한 근거를 구분해 줘.

    [출력]
    조건별 선택표와 read/write amplification을 측정할 계획을 작성해 줘.

    [검증]
    실제 버전의 지원을 확인하고 동일 변경·조회에서 파일 수·쓰기량·읽기 지연을 비교해 줘.
    운영 실행·변경 없이 검토와 검증 계획만 제시해 줘.
    ```

- **Expected output:** A conditional decision table and a plan to measure read and write amplification.
- **What the LLM can get wrong:** The LLM may claim merge-on-read is always faster or replacement values live only in delete files.
- **How to validate:** Check version support and compare file count, bytes written, and read latency for the same changes and queries.

## Prioritize maintenance work {#lakehouse-iceberg-04}

- **Situation:** Inspect a hypothetical Iceberg table with slow planning and scans.
- **Context to give the LLM:** Metrics: [file sizes, manifest count, delete-file count, planning time]; Operating limits: [query patterns, write schedule, maintenance budget, retained snapshots].

Example prompt:

=== "English"

    ```text {.prompt}
    [Context]
    Metrics: [file sizes, manifest count, delete-file count, planning time]
    Operating limits: [query patterns, write schedule, maintenance budget, retained snapshots]

    [Task]
    Separate the purposes of data compaction, delete rewrite, and manifest rewrite.
    Prioritize work by the observed bottleneck; do not recommend all tasks at once.
    Separate observations, assumptions, hypotheses, and missing evidence.

    [Output]
    Return evidence, expected cost, metrics, and stop conditions for each candidate task.

    [Checks]
    Compare one task at a time in a small test scope and check planning, scan, and total cost.
    Provide review and test plans only; do not run or change production.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    진단 지표: [파일 크기·manifest 수·delete file 수·planning time]
    운영 제약: [조회 패턴·write 일정·정비 예산·유지 snapshot]

    [요청]
    Data compaction, delete rewrite, manifest rewrite의 목적을 각각 구분해 줘.
    관찰된 병목에 맞게 우선순위를 정하고 모든 작업을 한 번에 권하지 마.
    관찰, 가정, 가설, 부족한 근거를 구분해 줘.

    [출력]
    작업별 근거·예상 비용·측정 지표·중단 조건의 검토표를 작성해 줘.

    [검증]
    작은 검증 범위에서 한 작업씩 비교하고 planning·scan·총비용 변화를 확인해 줘.
    운영 실행·변경 없이 검토와 검증 계획만 제시해 줘.
    ```

- **Expected output:** Evidence, expected cost, metrics, and stop conditions for each candidate task.
- **What the LLM can get wrong:** The LLM may assume data compaction fixes all metadata issues or maintenance has no cost.
- **How to validate:** Compare one task at a time in a small test scope and check planning, scan, and total cost.

## Review snapshot retention and cleanup safety {#lakehouse-iceberg-05}

- **Situation:** Review a hypothetical snapshot cleanup plan intended to reduce storage cost.
- **Context to give the LLM:** Retention needs: [time-travel and rollback windows, retained snapshot list]; Write state: [in-flight jobs, longest run time, file-path rules].

Example prompt:

=== "English"

    ```text {.prompt}
    [Context]
    Retention needs: [time-travel and rollback windows, retained snapshot list]
    Write state: [in-flight jobs, longest run time, file-path rules]

    [Task]
    Separate snapshot expiration from orphan cleanup and identify possibly referenced files.
    Review whether files absent from the current snapshot belong to older snapshots or in-flight writes.
    Separate observations, assumptions, hypotheses, and missing evidence.

    [Output]
    Return only retention questions and a read-only preflight checklist.

    [Checks]
    Do not produce deletion commands; check all references, path matching, and a margin for in-flight writes.
    Provide review and test plans only; do not run or change production.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    보존 요구: [time travel·rollback 기간·유지 snapshot 목록]
    Write 상태: [진행 중 작업·최대 실행 시간·파일 경로 규칙]

    [요청]
    Snapshot expiration과 orphan cleanup을 구분하고 참조 중 파일을 찾아 줘.
    현재 snapshot에 없는 파일도 과거 snapshot이나 진행 중 write와 관련되는지 검토해 줘.
    관찰, 가정, 가설, 부족한 근거를 구분해 줘.

    [출력]
    보존 기간 결정에 필요한 질문과 읽기 전용 사전 점검표만 작성해 줘.

    [검증]
    삭제 명령을 만들지 말고 전체 참조·경로 일치·진행 중 write의 여유 기간을 확인해 줘.
    운영 실행·변경 없이 검토와 검증 계획만 제시해 줘.
    ```

- **Expected output:** Only retention questions and a read-only preflight checklist.
- **What the LLM can get wrong:** The LLM may recommend deletion based only on the current snapshot or invent a short retention period.
- **How to validate:** Do not produce deletion commands; check all references, path matching, and a margin for in-flight writes.

## Review catalog and governance responsibilities {#lakehouse-iceberg-06}

- **Situation:** Map responsibilities in a hypothetical environment where several compute engines use one table.
- **Context to give the LLM:** Components: [storage, table format, catalog, engines, policy layer]; Needs: [table discovery, commits, access control, lineage, audit owners].

Example prompt:

=== "English"

    ```text {.prompt}
    [Context]
    Components: [storage, table format, catalog, engines, policy layer]
    Needs: [table discovery, commits, access control, lineage, audit owners]

    [Task]
    Separate finding current metadata from broader governance responsibilities.
    Mark evidence of policy enforcement for each engine path and unverified integrations.
    Separate observations, assumptions, hypotheses, and missing evidence.

    [Output]
    Return a responsibility matrix and questions to check for each product and version.

    [Checks]
    Compare responsibilities with docs, settings, and approved access tests; keep permission changes as proposals.
    Provide review and test plans only; do not run or change production.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    구성: [storage·table format·catalog·engine·정책 계층]
    요구: [테이블 발견·commit·접근 제어·lineage·audit 담당]

    [요청]
    Table 이름에서 현재 metadata를 찾는 책임과 governance 책임을 구분해 줘.
    각 엔진 경로에 정책이 적용되는 근거와 아직 확인하지 못한 연동을 표시해 줘.
    관찰, 가정, 가설, 부족한 근거를 구분해 줘.

    [출력]
    책임 행렬과 제품·버전별로 확인해야 할 질문을 작성해 줘.

    [검증]
    문서·설정·승인된 접근 테스트로 각 경로의 책임을 대조하고 권한 변경은 제안 수준에 둬.
    운영 실행·변경 없이 검토와 검증 계획만 제시해 줘.
    ```

- **Expected output:** A responsibility matrix and questions to check for each product and version.
- **What the LLM can get wrong:** The LLM may equate catalog registration with complete access control or equate Unity Catalog with an Iceberg catalog.
- **How to validate:** Compare responsibilities with docs, settings, and approved access tests; keep permission changes as proposals.
