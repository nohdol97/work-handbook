---
id: prompts-foundations
status: overview
last_updated: 2026-09-24
last_reviewed: 2026-09-24
knowledge_ids: []
---

# Data engineering foundations practical prompts

Page type: Reference. These six authored, hypothetical examples apply the [existing study material](../data-platform/foundations.md). They do not claim production experience, measured usage frequency, or model results. The examples were not run.

Choose a case and replace bracketed inputs with sanitized information. Each prompt has 한국어 and English tabs for language selection and copying. Treat LLM output as a hypothesis. Check actual settings, logs, official docs, and bounded tests. This page does not authorize production actions or permission changes.

[All prompts](index.md) · [Concepts and sources](../data-platform/foundations.md)

## Quick selection

| Purpose | Jump to |
| --- | --- |
| Decide whether to separate analytical workloads | [01](#foundations-01) |
| Review a query for column pruning | [02](#foundations-02) |
| Find what Parquet statistics can skip | [03](#foundations-03) |
| Compare daily and hourly partitions | [04](#foundations-04) |
| Choose bucketing or sorting for a high-cardinality key | [05](#foundations-05) |
| Separate the causes of object-storage read cost | [06](#foundations-06) |

## Decide whether to separate analytical workloads {#foundations-01}

- **Situation:** In this hypothetical case, service responses slow down while analytical queries run.
- **Context to give the LLM:** Queries and frequency: [sanitized SQL and schedule]; Impact and limits: [transaction latency, resources, cost, freshness target].

Example prompt:

=== "English"

    ```text {.prompt}
    [Context]
    Queries and frequency: [sanitized SQL and schedule]
    Impact and limits: [transaction latency, resources, cost, freshness target]

    [Task]
    Classify the current workload as OLTP or OLAP and assess evidence of contention.
    Compare keeping the design with separating analytics; do not decide by row count alone.
    Separate observations, assumptions, hypotheses, and missing evidence.

    [Output]
    Return a table of latency, freshness, operating cost, and evidence needed for each option.

    [Checks]
    Propose a bounded comparison of latency and resources with and without the analytical work.
    Provide review and test plans only; do not run or change production.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    쿼리와 실행 빈도: [익명화한 SQL·주기]
    영향과 제약: [트랜잭션 지연·자원·비용·신선도 목표]

    [요청]
    현재 workload를 OLTP와 OLAP로 나누고 충돌 근거를 평가해 줘.
    현 구조 유지와 분석계 분리를 비교하고 row 수만으로 결론 내리지 마.
    관찰, 가정, 가설, 부족한 근거를 구분해 줘.

    [출력]
    선택지별 응답 시간·신선도·운영 비용·추가 근거 표를 작성해 줘.

    [검증]
    동일 workload에서 분석 실행 유무별 지연과 자원 지표를 비교하는 제한된 실험을 제안해 줘.
    운영 실행·변경 없이 검토와 검증 계획만 제시해 줘.
    ```

- **Expected output:** A table of latency, freshness, operating cost, and evidence needed for each option.
- **What the LLM can get wrong:** The LLM may confuse correlation with causation or claim that PostgreSQL cannot run analytics.
- **How to validate:** Propose a bounded comparison of latency and resources with and without the analytical work.

## Review a query for column pruning {#foundations-02}

- **Situation:** In this hypothetical case, an aggregate needs few columns but scans many bytes in a wide event table.
- **Context to give the LLM:** Query and schema: [SQL, column list, required result]; Execution evidence: [reader version, plan, scan bytes, file format].

Example prompt:

=== "English"

    ```text {.prompt}
    [Context]
    Query and schema: [SQL, column list, required result]
    Execution evidence: [reader version, plan, scan bytes, file format]

    [Task]
    Identify required and unused columns and review the projection.
    Separate column pruning from row filtering and draft an equivalent query.
    Separate observations, assumptions, hypotheses, and missing evidence.

    [Output]
    Return each column's purpose, a SQL draft, expected I/O change, and limits.

    [Checks]
    Describe how to compare results, columns actually read, and scan bytes on the same input.
    Provide review and test plans only; do not run or change production.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    쿼리와 스키마: [SQL·열 목록·필요한 결과]
    실행 근거: [reader 버전·계획·scan bytes·파일 형식]

    [요청]
    결과에 필요한 열과 불필요한 열을 구분하고 projection을 검토해 줘.
    Column pruning과 row 필터를 구분하고 동일 결과를 내는 쿼리 초안을 제안해 줘.
    관찰, 가정, 가설, 부족한 근거를 구분해 줘.

    [출력]
    열별 사용 이유, 변경 SQL 초안, 예상 I/O 변화와 한계를 작성해 줘.

    [검증]
    같은 입력에서 결과 일치와 실제 읽은 열·scan bytes를 확인하는 방법을 적어 줘.
    운영 실행·변경 없이 검토와 검증 계획만 제시해 줘.
    ```

- **Expected output:** Each column's purpose, a SQL draft, expected I/O change, and limits.
- **What the LLM can get wrong:** The LLM may promise the same benefit in every engine or confuse filtering with column pruning.
- **How to validate:** Describe how to compare results, columns actually read, and scan bytes on the same input.

## Find what Parquet statistics can skip {#foundations-03}

- **Situation:** Review a hypothetical query that reads many row groups despite a selective filter.
- **Context to give the LLM:** Filters and statistics: [predicate, row-group min/max, null information]; Storage and reader details: [sort layout, page indexes, reader support].

Example prompt:

=== "English"

    ```text {.prompt}
    [Context]
    Filters and statistics: [predicate, row-group min/max, null information]
    Storage and reader details: [sort layout, page indexes, reader support]

    [Task]
    Classify each row group as skippable, needing a read, or lacking evidence.
    Distinguish predicate pushdown from pruning; do not describe either as arbitrary row lookup.
    Separate observations, assumptions, hypotheses, and missing evidence.

    [Output]
    Return a statistics evidence table and conditions for considering a sort-layout change.

    [Checks]
    Check the prediction with the plan and row groups read; include a case with missing statistics.
    Provide review and test plans only; do not run or change production.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    조건과 통계: [필터·row group별 min/max·null 정보]
    저장·읽기 설정: [정렬 상태·page index 유무·reader 지원]

    [요청]
    각 row group을 제외 가능·읽기 필요·정보 부족으로 분류해 줘.
    Predicate pushdown과 pruning을 나누고 임의의 row lookup처럼 설명하지 마.
    관찰, 가정, 가설, 부족한 근거를 구분해 줘.

    [출력]
    통계 근거 표와 정렬 변경을 검토할 조건을 작성해 줘.

    [검증]
    실행 계획과 읽은 row group 수로 예측을 확인하고 통계가 없는 경우도 포함해 줘.
    운영 실행·변경 없이 검토와 검증 계획만 제시해 줘.
    ```

- **Expected output:** A statistics evidence table and conditions for considering a sort-layout change.
- **What the LLM can get wrong:** The LLM may treat overlapping ranges as proof of matching rows or missing statistics as missing values.
- **How to validate:** Check the prediction with the plan and row groups read; include a case with missing statistics.

## Compare daily and hourly partitions {#foundations-04}

- **Situation:** Evaluate a hypothetical proposal to change daily partitions to hourly partitions.
- **Context to give the LLM:** Access patterns: [query time ranges, filter frequency, freshness needs]; Distribution: [hourly volume, files per partition, file sizes].

Example prompt:

=== "English"

    ```text {.prompt}
    [Context]
    Access patterns: [query time ranges, filter frequency, freshness needs]
    Distribution: [hourly volume, files per partition, file sizes]

    [Task]
    Compare pruning benefits and small-file growth for daily and hourly partitions.
    Treat empty and busy hours separately, and distinguish a partition from a file.
    Separate observations, assumptions, hypotheses, and missing evidence.

    [Output]
    Return estimated partition counts, file overhead, query effects, and assumptions for each option.

    [Checks]
    Plan a comparison of scan bytes, planning time, and file distribution for representative time ranges.
    Provide review and test plans only; do not run or change production.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    접근 패턴: [기간별 쿼리·필터 빈도·신선도 요구]
    분포: [시간별 유입량·partition별 파일 수·크기]

    [요청]
    일·시간 partition에서 pruning 이득과 작은 파일 증가를 비교해 줘.
    빈 시간대와 유입이 몰리는 시간대를 따로 보고 partition과 파일을 구분해 줘.
    관찰, 가정, 가설, 부족한 근거를 구분해 줘.

    [출력]
    후보별 partition 수·파일 부담·쿼리 영향 추정과 가정을 적어 줘.

    [검증]
    대표 시간 범위별 scan bytes·planning time·파일 분포를 비교하는 계획을 작성해 줘.
    운영 실행·변경 없이 검토와 검증 계획만 제시해 줘.
    ```

- **Expected output:** Estimated partition counts, file overhead, query effects, and assumptions for each option.
- **What the LLM can get wrong:** The LLM may claim finer partitions are always faster or assume one file per partition.
- **How to validate:** Plan a comparison of scan bytes, planning time, and file distribution for representative time ranges.

## Choose bucketing or sorting for a high-cardinality key {#foundations-05}

- **Situation:** Review a hypothetical design that partitions directly by user ID for user-level queries.
- **Context to give the LLM:** Keys and queries: [sanitized cardinality, key distribution, filter examples]; Layout details: [current partitions, file min/max, engine version].

Example prompt:

=== "English"

    ```text {.prompt}
    [Context]
    Keys and queries: [sanitized cardinality, key distribution, filter examples]
    Layout details: [current partitions, file min/max, engine version]

    [Task]
    Compare direct partitioning, fixed buckets, and sorting for the current queries.
    Include hot keys and broad overlapping min/max ranges; explain the difference from an OLTP index.
    Separate observations, assumptions, hypotheses, and missing evidence.

    [Output]
    Return trade-offs for file count, skew, and pruning, plus the statistics needed.

    [Checks]
    Check the engine's transform syntax and compare selected files and scan bytes for the same filters.
    Provide review and test plans only; do not run or change production.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    키와 조회: [익명화한 cardinality·키 분포·필터 예시]
    배치 정보: [현 partition·파일별 min/max·엔진 버전]

    [요청]
    직접 partition, 고정 bucket, 정렬을 현재 쿼리에 맞춰 비교해 줘.
    Hot key와 넓게 겹치는 min/max를 포함하고 OLTP index와 차이를 설명해 줘.
    관찰, 가정, 가설, 부족한 근거를 구분해 줘.

    [출력]
    후보별 파일 수·skew·pruning의 trade-off와 필요한 통계를 적어 줘.

    [검증]
    엔진의 transform 문법을 확인하고 동일 필터의 파일 선택 수와 scan bytes를 비교해 줘.
    운영 실행·변경 없이 검토와 검증 계획만 제시해 줘.
    ```

- **Expected output:** Trade-offs for file count, skew, and pruning, plus the statistics needed.
- **What the LLM can get wrong:** The LLM may assume hashing splits a hot key or sorting gives the same row access as a B-tree.
- **How to validate:** Check the engine's transform syntax and compare selected files and scan bytes for the same filters.

## Separate the causes of object-storage read cost {#foundations-06}

- **Situation:** In this hypothetical case, remote read time and request cost rise after compute is separated.
- **Context to give the LLM:** Usage: [file count, sizes, request count, transfer volume, scan bytes]; Limits: [price components, repeated queries, cache lifetime, latency target].

Example prompt:

=== "English"

    ```text {.prompt}
    [Context]
    Usage: [file count, sizes, request count, transfer volume, scan bytes]
    Limits: [price components, repeated queries, cache lifetime, latency target]

    [Task]
    Assess storage, requests, transfer, and compute cost separately.
    Compare pruning, caching, and file-size changes, including rewrite cost.
    Separate observations, assumptions, hypotheses, and missing evidence.

    [Output]
    Use supplied prices, not invented prices; return cost formulas and measurement priorities.

    [Checks]
    Propose cold and warm runs of the same query to compare requests, transfer, and elapsed time.
    Provide review and test plans only; do not run or change production.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    사용량: [파일 수·크기·요청 수·전송량·scan bytes]
    제약: [요금 항목·반복 조회 패턴·cache 수명·응답 목표]

    [요청]
    저장 용량, 요청, 전송, compute 비용을 분리해서 평가해 줘.
    Pruning, cache, 파일 크기 조정의 효과와 재작성 비용을 비교해 줘.
    관찰, 가정, 가설, 부족한 근거를 구분해 줘.

    [출력]
    단가를 꾸며내지 말고 입력 단가를 쓰는 비용식과 측정 우선순위를 작성해 줘.

    [검증]
    동일 쿼리의 cold·warm 실행에서 요청 수·전송량·시간을 비교하는 검증을 제안해 줘.
    운영 실행·변경 없이 검토와 검증 계획만 제시해 줘.
    ```

- **Expected output:** Cost formulas using supplied prices and measurement priorities.
- **What the LLM can get wrong:** The LLM may judge total cost by storage price alone or invent cache hit rates and tasks per file.
- **How to validate:** Propose cold and warm runs of the same query to compare requests, transfer, and elapsed time.
