---
id: prompts-lakehouse-iceberg
status: overview
last_updated: 2026-10-18
last_reviewed: 2026-10-18
knowledge_ids: []
---

# Lakehouse와 Iceberg 실무 프롬프트

실제 SQL·설정·로그·변경안을 붙여 바로 요청할 수 있는 예시다. 비식별 자료만 사용하고, 제안은 실제 근거와 권한에 맞춰 검토한다. 이 예시만으로 시스템 변경이나 데이터 삭제를 승인하지 않는다. 사용 빈도나 모델 성능을 측정한 사례는 아니다.

[전체 프롬프트 모음](index.md) · [개념과 출처](../data-platform/lakehouse-iceberg.md)

## 빠르게 고르기

| 목적 | 바로 가기 |
| --- | --- |
| 두 쿼리가 다른 snapshot을 읽는지 확인 | [01](#lakehouse-iceberg-01) |
| Partition evolution 이후 과거 파일 영향 검토 | [02](#lakehouse-iceberg-02) |
| Copy-on-write와 merge-on-read 선택 검토 | [03](#lakehouse-iceberg-03) |
| Maintenance 작업의 우선순위 정하기 | [04](#lakehouse-iceberg-04) |
| Snapshot 보존과 정리 계획의 안전성 검토 | [05](#lakehouse-iceberg-05) |
| Catalog와 governance 책임 경계 검토 | [06](#lakehouse-iceberg-06) |

## 두 쿼리가 다른 snapshot을 읽는지 확인 {#lakehouse-iceberg-01}

예시 프롬프트:

=== "한국어"

    ```text {.prompt}
    같은 테이블을 조회했지만 두 엔진의 결과가 다른 상황이야.
    Catalog에서 metadata, snapshot, manifest, 파일로 이어지는 참조를 설명해 줘.
    서로 다른 snapshot과 같은 snapshot 내 차이를 나누고 rollback부터 제안하지 마.
    참조 불일치 가설과 고정 snapshot 비교의 읽기 전용 점검표를 작성해 줘.
    검토만 하고 변경은 실행하지 마.
    ```

=== "English"

    ```text {.prompt}
    Two engines return different results for the same table.
    Explain the references from catalog to metadata, snapshot, manifests, and files.
    Separate different-snapshot and same-snapshot differences; do not start with rollback.
    Return reference-mismatch hypotheses and a read-only checklist for a fixed-snapshot comparison.
    Review only; do not apply changes.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 각 쿼리가 실제 읽은 snapshot ID와 조건. 읽기 전용 metadata와 쿼리 근거를 같은 시점으로 맞춘다. 최신 metadata 파일 이름만으로 현재 상태를 확정하거나 snapshot이 데이터 전체 복사라고 할 수 있다. metadata 파일 이름이나 실행 시각만으로 같은 snapshot이라고 판단하지 않는다.

## Partition evolution 이후 과거 파일 영향 검토 {#lakehouse-iceberg-02}

예시 프롬프트:

=== "한국어"

    ```text {.prompt}
    Day에서 hour로 partition spec을 바꿨는데 과거 조회는 느린 상황이야.
    Spec 변경과 과거 파일 rewrite를 구분해서 현재 상태를 설명해 줘.
    혼합 spec에서 필터가 어떻게 pruning에 쓰이는지 근거와 미확인 부분을 나눠 줘.
    최근·과거 조회 비교표와 선택적 rewrite 검토 조건을 작성해 줘.
    검토만 하고 변경은 실행하지 마.
    ```

=== "English"

    ```text {.prompt}
    Old-data queries stay slow after changing the spec from day to hour.
    Explain the current state by separating a spec change from rewriting old files.
    Explain how filters can support pruning across mixed specs and mark missing evidence.
    Return a recent-versus-historical query table and criteria for considering a selective rewrite.
    Review only; do not apply changes.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 변경 전후 spec ID와 과거 파일별 spec. 읽기 전용 metadata와 쿼리 근거를 같은 시점으로 맞춘다. Spec을 바꾸면 과거 파일도 자동 재배치되거나 모든 엔진의 SQL 문법이 같다고 할 수 있다. 과거·신규 파일을 섞은 표본에서도 결과와 scan 비용을 비교한다.

## Copy-on-write와 merge-on-read 선택 검토 {#lakehouse-iceberg-03}

예시 프롬프트:

=== "한국어"

    ```text {.prompt}
    소량의 row 변경이 자주 발생하는 테이블의 읽기·쓰기 비용을 검토 중이야.
    파일 rewrite 비용과 읽을 때 delete를 적용하는 비용을 비교해 줘.
    새 값의 data file 기록과 delete maintenance도 포함하고 지원 여부를 가정하지 마.
    조건별 선택표와 read/write amplification을 측정할 계획을 작성해 줘.
    검토만 하고 변경은 실행하지 마.
    ```

=== "English"

    ```text {.prompt}
    Review read and write cost for a table with frequent small row changes.
    Compare file-rewrite cost with the cost of applying deletes during reads.
    Include data files for replacement values and delete maintenance; do not assume support.
    Return a conditional decision table and a plan to measure read and write amplification.
    Review only; do not apply changes.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 해당 엔진·connector의 row 변경 지원과 읽기 지연 목표. 읽기 전용 metadata와 쿼리 근거를 같은 시점으로 맞춘다. Merge-on-read가 항상 빠르거나 새 값도 delete file에만 저장된다고 설명할 수 있다. 쓰기 단축만으로 선택하지 말고 delete 적용·정비 비용을 함께 본다.

## Maintenance 작업의 우선순위 정하기 {#lakehouse-iceberg-04}

예시 프롬프트:

=== "한국어"

    ```text {.prompt}
    쿼리 planning과 scan이 모두 느려진 Iceberg 테이블을 점검한다.
    Data compaction, delete rewrite, manifest rewrite의 목적을 각각 구분해 줘.
    관찰된 병목에 맞게 우선순위를 정하고 모든 작업을 한 번에 권하지 마.
    작업별 근거·예상 비용·측정 지표·중단 조건의 검토표를 작성해 줘.
    검토만 하고 변경은 실행하지 마.
    ```

=== "English"

    ```text {.prompt}
    Inspect an Iceberg table with slow planning and scans.
    Separate the purposes of data compaction, delete rewrite, and manifest rewrite.
    Prioritize work by the observed bottleneck; do not recommend all tasks at once.
    Return evidence, expected cost, metrics, and stop conditions for each candidate task.
    Review only; do not apply changes.
    ```

**핵심 사항:** 판단 전에 확인할 근거: planning과 scan 시간을 나눈 관측값. 읽기 전용 metadata와 쿼리 근거를 같은 시점으로 맞춘다. Data compaction이 metadata 문제까지 모두 해결하거나 maintenance 자체가 무료라고 볼 수 있다. 관측 병목과 연결되지 않는 정비 작업은 우선순위에서 내린다.

## Snapshot 보존과 정리 계획의 안전성 검토 {#lakehouse-iceberg-05}

예시 프롬프트:

=== "한국어"

    ```text {.prompt}
    스토리지 비용을 줄이기 위한 snapshot 정리 계획을 검토 중이야.
    Snapshot expiration과 orphan cleanup을 구분하고 참조 중 파일을 찾아 줘.
    현재 snapshot에 없는 파일도 과거 snapshot이나 진행 중 write와 관련되는지 검토해 줘.
    보존 기간 결정에 필요한 질문과 읽기 전용 사전 점검표만 작성해 줘.
    검토만 하고 변경은 실행하지 마.
    ```

=== "English"

    ```text {.prompt}
    Review a snapshot cleanup plan intended to reduce storage cost.
    Separate snapshot expiration from orphan cleanup and identify possibly referenced files.
    Review whether files absent from the current snapshot belong to older snapshots or in-flight writes.
    Return only retention questions and a read-only preflight checklist.
    Review only; do not apply changes.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 유지할 snapshot 참조와 진행 중 write의 최장 시간. 읽기 전용 metadata와 쿼리 근거를 같은 시점으로 맞춘다. 현재 snapshot에 없다는 이유만으로 삭제를 권하거나 짧은 보존 기간을 임의로 정할 수 있다. 참조가 불명확한 파일은 삭제 대상 목록에서 보류한다.

## Catalog와 governance 책임 경계 검토 {#lakehouse-iceberg-06}

예시 프롬프트:

=== "한국어"

    ```text {.prompt}
    여러 compute 엔진이 같은 테이블을 쓰는 환경의 책임을 정리하려고 해.
    Table 이름에서 현재 metadata를 찾는 책임과 governance 책임을 구분해 줘.
    각 엔진 경로에 정책이 적용되는 근거와 아직 확인하지 못한 연동을 표시해 줘.
    책임 행렬과 제품·버전별로 확인해야 할 질문을 작성해 줘.
    검토만 하고 변경은 실행하지 마.
    ```

=== "English"

    ```text {.prompt}
    Map responsibilities in an environment where several compute engines use one table.
    Separate finding current metadata from broader governance responsibilities.
    Mark evidence of policy enforcement for each engine path and unverified integrations.
    Return a responsibility matrix and questions to check for each product and version.
    Review only; do not apply changes.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 엔진별 metadata 탐색 경로와 정책 적용 위치. 읽기 전용 metadata와 쿼리 근거를 같은 시점으로 맞춘다. Catalog 등록만으로 모든 접근이 통제되거나 Unity Catalog와 Iceberg catalog를 같다고 볼 수 있다. table 발견 성공과 접근 제어 검증 성공을 별개 결과로 기록한다.
