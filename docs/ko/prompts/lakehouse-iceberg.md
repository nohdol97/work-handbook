---
id: prompts-lakehouse-iceberg
status: overview
last_updated: 2026-09-24
last_reviewed: 2026-09-24
knowledge_ids: []
---

# Lakehouse와 Iceberg 실무 프롬프트

문서 유형: Reference. [기존 학습 내용](../data-platform/lakehouse-iceberg.md)을 적용하도록 작성한 가상의 재사용 예시 6개다. 실제 업무 경험, 사용 빈도 조사, 모델 실행 결과를 뜻하지 않는다. 예시를 실행하지 않았다.

상황에 맞는 예시를 고르고 대괄호 입력을 익명화한 자료로 바꾼다. 각 예시는 한국어·English 탭에서 언어를 선택해 복사할 수 있다. LLM의 답은 가설이며 실제 설정·로그·공식 문서·제한된 검증으로 확인한다. 운영 실행이나 권한 변경을 허가하는 문서는 아니다.

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

- **상황:** 같은 테이블을 조회했지만 두 엔진의 결과가 다른 가상 사례다.
- **제공할 맥락:** 조회 근거: [엔진·쿼리·실행 시각·관찰한 snapshot ID]; 메타데이터: [catalog·현재 pointer·snapshot 이력·동시 write].

예시 프롬프트:

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

- **기대 결과:** 참조 불일치 가설과 고정 snapshot 비교의 읽기 전용 점검표.
- **오류 가능성:** 최신 metadata 파일 이름만으로 현재 상태를 확정하거나 snapshot이 데이터 전체 복사라고 할 수 있다.
- **검증 방법:** 양쪽이 같은 snapshot과 동일 조건을 읽는지 확인하고 결과 수·집계를 대조한다.

## Partition evolution 이후 과거 파일 영향 검토 {#lakehouse-iceberg-02}

- **상황:** Day에서 hour로 partition spec을 바꿨는데 과거 조회는 느린 가상 사례다.
- **제공할 맥락:** Spec 이력: [이전·현재 transform·적용 시점·spec ID]; 조회와 파일: [시간 필터·파일별 spec·scan bytes·통계].

예시 프롬프트:

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

- **기대 결과:** 최근·과거 조회 비교표와 선택적 rewrite 검토 조건.
- **오류 가능성:** Spec을 바꾸면 과거 파일도 자동 재배치되거나 모든 엔진의 SQL 문법이 같다고 할 수 있다.
- **검증 방법:** 파일별 spec과 실행 계획을 확인하고 같은 시간 범위의 scan bytes를 비교한다.

## Copy-on-write와 merge-on-read 선택 검토 {#lakehouse-iceberg-03}

- **상황:** 소량의 row 변경이 자주 발생하는 가상 테이블의 읽기·쓰기 비용을 검토한다.
- **제공할 맥락:** Workload: [변경률·쿼리 빈도·읽기 지연 목표·파일 크기]; 지원 범위: [엔진·connector·format 버전·현재 delete 표현].

예시 프롬프트:

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

- **기대 결과:** 조건별 선택표와 read/write amplification을 측정할 계획.
- **오류 가능성:** Merge-on-read가 항상 빠르거나 새 값도 delete file에만 저장된다고 설명할 수 있다.
- **검증 방법:** 실제 버전의 지원을 확인하고 동일 변경·조회에서 파일 수·쓰기량·읽기 지연을 비교한다.

## Maintenance 작업의 우선순위 정하기 {#lakehouse-iceberg-04}

- **상황:** 쿼리 planning과 scan이 모두 느려진 가상 Iceberg 테이블을 점검한다.
- **제공할 맥락:** 진단 지표: [파일 크기·manifest 수·delete file 수·planning time]; 운영 제약: [조회 패턴·write 일정·정비 예산·유지 snapshot].

예시 프롬프트:

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

- **기대 결과:** 작업별 근거·예상 비용·측정 지표·중단 조건의 검토표.
- **오류 가능성:** Data compaction이 metadata 문제까지 모두 해결하거나 maintenance 자체가 무료라고 볼 수 있다.
- **검증 방법:** 작은 검증 범위에서 한 작업씩 비교하고 planning·scan·총비용 변화를 확인한다.

## Snapshot 보존과 정리 계획의 안전성 검토 {#lakehouse-iceberg-05}

- **상황:** 스토리지 비용을 줄이기 위한 가상 snapshot 정리 계획을 검토한다.
- **제공할 맥락:** 보존 요구: [time travel·rollback 기간·유지 snapshot 목록]; Write 상태: [진행 중 작업·최대 실행 시간·파일 경로 규칙].

예시 프롬프트:

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

- **기대 결과:** 보존 기간 결정에 필요한 질문과 읽기 전용 사전 점검표.
- **오류 가능성:** 현재 snapshot에 없다는 이유만으로 삭제를 권하거나 짧은 보존 기간을 임의로 정할 수 있다.
- **검증 방법:** 삭제 명령을 만들지 말고 전체 참조·경로 일치·진행 중 write의 여유 기간을 확인한다.

## Catalog와 governance 책임 경계 검토 {#lakehouse-iceberg-06}

- **상황:** 여러 compute 엔진이 같은 테이블을 쓰는 가상 환경의 책임을 정리한다.
- **제공할 맥락:** 구성: [storage·table format·catalog·engine·정책 계층]; 요구: [테이블 발견·commit·접근 제어·lineage·audit 담당].

예시 프롬프트:

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

- **기대 결과:** 책임 행렬과 제품·버전별로 확인해야 할 질문.
- **오류 가능성:** Catalog 등록만으로 모든 접근이 통제되거나 Unity Catalog와 Iceberg catalog를 같다고 볼 수 있다.
- **검증 방법:** 문서·설정·승인된 접근 테스트로 각 경로의 책임을 대조하고 권한 변경은 제안 수준에 둔다.
