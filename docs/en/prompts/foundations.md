---
id: prompts-foundations
status: overview
last_updated: 2026-10-18
last_reviewed: 2026-10-18
knowledge_ids: []
---

# Data engineering foundations practical prompts

Copy these examples with the relevant SQL, settings, logs, or proposed changes. Use sanitized material and check suggestions against real evidence and permissions. An example does not authorize system changes or data deletion. These are not measured usage or model-performance results.

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

Example prompt:

=== "English"

    ```text {.prompt}
    Service responses slow down while analytical queries run.
    Classify the current workload as OLTP or OLAP and assess evidence of contention.
    Compare keeping the design with separating analytics; do not decide by row count alone.
    Return a table of latency, freshness, operating cost, and evidence needed for each option.
    ```

=== "한국어"

    ```text {.prompt}
    운영 DB의 응답이 분석 쿼리 실행 시간대에 느려지는 상황이야.
    현재 workload를 OLTP와 OLAP로 나누고 충돌 근거를 평가해 줘.
    현 구조 유지와 분석계 분리를 비교하고 row 수만으로 결론 내리지 마.
    선택지별 응답 시간·신선도·운영 비용·추가 근거 표를 작성해 줘.
    ```

**Key point:** Evidence to check first: latency and resource records for comparable periods with and without analytics. The LLM may confuse correlation with causation or claim that PostgreSQL cannot run analytics. Reject an option that improves average latency while worsening slow service requests.

## Review a query for column pruning {#foundations-02}

Example prompt:

=== "English"

    ```text {.prompt}
    An aggregate needs few columns but scans many bytes in a wide event table.
    Identify required and unused columns and review the projection.
    Separate column pruning from row filtering and draft an equivalent query.
    Return each column's purpose, a SQL draft, expected I/O change, and limits.
    ```

=== "한국어"

    ```text {.prompt}
    넓은 이벤트 테이블에서 소수 열만 필요한 집계의 scan bytes가 큰 상황이야.
    결과에 필요한 열과 불필요한 열을 구분하고 projection을 검토해 줘.
    Column pruning과 row 필터를 구분하고 동일 결과를 내는 쿼리 초안을 제안해 줘.
    열별 사용 이유, 변경 SQL 초안, 예상 I/O 변화와 한계를 작성해 줘.
    ```

**Key point:** Evidence to check first: columns actually used by consumers and the result contract. The LLM may promise the same benefit in every engine or confuse filtering with column pruning. Check that removed columns do not break downstream schema contracts.

## Find what Parquet statistics can skip {#foundations-03}

Example prompt:

=== "English"

    ```text {.prompt}
    Review a query that reads many row groups despite a selective filter.
    Classify each row group as skippable, needing a read, or lacking evidence.
    Distinguish predicate pushdown from pruning; do not describe either as arbitrary row lookup.
    Return a statistics evidence table and conditions for considering a sort-layout change.
    ```

=== "한국어"

    ```text {.prompt}
    조건이 선택적인데도 많은 row group을 읽는 분석 쿼리를 검토 중이야.
    각 row group을 제외 가능·읽기 필요·정보 부족으로 분류해 줘.
    Predicate pushdown과 pruning을 나누고 임의의 row lookup처럼 설명하지 마.
    통계 근거 표와 정렬 변경을 검토할 조건을 작성해 줘.
    ```

**Key point:** Evidence to check first: row-group statistics for the filter and evidence of reader support. The LLM may treat overlapping ranges as proof of matching rows or missing statistics as missing values. Include NULLs and missing statistics when checking that skipped ranges contain no required rows.

## Compare daily and hourly partitions {#foundations-04}

Example prompt:

=== "English"

    ```text {.prompt}
    Evaluate a proposal to change daily partitions to hourly partitions.
    Compare pruning benefits and small-file growth for daily and hourly partitions.
    Treat empty and busy hours separately, and distinguish a partition from a file.
    Return estimated partition counts, file overhead, query effects, and assumptions for each option.
    ```

=== "한국어"

    ```text {.prompt}
    날짜 partition을 시간 단위로 바꾸자는 제안을 평가한다.
    일·시간 partition에서 pruning 이득과 작은 파일 증가를 비교해 줘.
    빈 시간대와 유입이 몰리는 시간대를 따로 보고 partition과 파일을 구분해 줘.
    후보별 partition 수·파일 부담·쿼리 영향 추정과 가정을 적어 줘.
    ```

**Key point:** Evidence to check first: query frequency by representative time range and file distribution. The LLM may claim finer partitions are always faster or assume one file per partition. Compare query gains with write and maintenance costs over the same workload period.

## Choose bucketing or sorting for a high-cardinality key {#foundations-05}

Example prompt:

=== "English"

    ```text {.prompt}
    Review a design that partitions directly by user ID for user-level queries.
    Compare direct partitioning, fixed buckets, and sorting for the current queries.
    Include hot keys and broad overlapping min/max ranges; explain the difference from an OLTP index.
    Return trade-offs for file count, skew, and pruning, plus the statistics needed.
    ```

=== "한국어"

    ```text {.prompt}
    사용자별 조회를 위해 사용자 ID로 직접 partition하자는 설계를 검토 중이야.
    직접 partition, 고정 bucket, 정렬을 현재 쿼리에 맞춰 비교해 줘.
    Hot key와 넓게 겹치는 min/max를 포함하고 OLTP index와 차이를 설명해 줘.
    후보별 파일 수·skew·pruning의 trade-off와 필요한 통계를 적어 줘.
    ```

**Key point:** Evidence to check first: per-key distribution and actual filter selectivity. The LLM may assume hashing splits a hot key or sorting gives the same row access as a B-tree. Check the largest key and empty buckets as well as average file count.

## Separate the causes of object-storage read cost {#foundations-06}

Example prompt:

=== "English"

    ```text {.prompt}
    Remote read time and request cost rise after compute is separated.
    Assess storage, requests, transfer, and compute cost separately.
    Compare pruning, caching, and file-size changes, including rewrite cost.
    Use supplied prices, not invented prices; return cost formulas and measurement priorities.
    ```

=== "한국어"

    ```text {.prompt}
    Compute를 분리한 뒤 원격 읽기 시간과 요청 비용이 커진 상황이야.
    저장 용량, 요청, 전송, compute 비용을 분리해서 평가해 줘.
    Pruning, cache, 파일 크기 조정의 효과와 재작성 비용을 비교해 줘.
    단가를 꾸며내지 말고 입력 단가를 쓰는 비용식과 측정 우선순위를 작성해 줘.
    ```

**Key point:** Evidence to check first: request, transfer, and compute usage for one period and applicable prices. The LLM may judge total cost by storage price alone or invent cache hit rates and tasks per file. Reject savings estimates that omit scope, rewrite costs, or cache expiry.
