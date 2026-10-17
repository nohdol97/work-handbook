---
id: prompts-trino
status: overview
last_updated: 2026-10-18
last_reviewed: 2026-10-18
knowledge_ids: []
---

# Trino practical prompts

Copy these examples with the relevant SQL, settings, logs, or proposed changes. Use sanitized material and check suggestions against real evidence and permissions. An example does not authorize system changes or data deletion. These are not measured usage or model-performance results.

[Concept guide](../data-platform/trino.md) · [All prompts](index.md)

| # | Jump to a situation |
| --- | --- |
| 01 | [Check predicate and projection pushdown](#trino-01) |
| 02 | [Check broadcast-join memory fit](#trino-02) |
| 03 | [Investigate slow tasks and key skew](#trino-03) |
| 04 | [Review spill and retry-execution options](#trino-04) |
| 05 | [Check Iceberg pruning and storage roles](#trino-05) |
| 06 | [Review workload placement between Trino and Spark](#trino-06) |

## Check predicate and projection pushdown {#trino-01}

**Prompt:**

=== "English"

    ```text {.prompt}
    Scan bytes do not fall after adding a filter. Check whether pushdown occurs.
    Separate work pushed to the source from work retained in the plan.
    Review predicate and projection support by query shape and connector.
    Separate observed scan differences, cause hypotheses, and needed evidence.
    Return plan evidence, support checks, and comparisons that can reject each hypothesis.
    ```

=== "한국어"

    ```text {.prompt}
    Filter를 추가해도 scan bytes가 줄지 않아 pushdown 여부를 확인한다.
    Plan에서 source로 내려간 조건과 남은 연산을 구분해 주세요.
    Predicate·projection 지원을 query 형태와 connector별로 검토해 주세요.
    Scan 차이의 관측과 원인 가설, 필요한 근거를 분리해 주세요.
    연산별 plan 근거·지원 확인·반증할 비교표를 주세요.
    ```

**Key point:** Evidence to check first: connector support evidence and operations retained in EXPLAIN. Group the plan and metrics for one query ID and include connector details. The LLM may infer pushdown from WHERE or confuse fewer output rows with less scanning. Measure fewer output rows separately from fewer bytes read.

## Check broadcast-join memory fit {#trino-02}

**Prompt:**

=== "English"

    ```text {.prompt}
    A broadcast join with a supposedly small dimension causes a worker memory error.
    Separate data copied to each worker from total input size.
    Compare memory and exchange costs for broadcast and partitioned options.
    Do not assume changing join distribution alone solves the problem.
    Return memory hypotheses, supporting evidence, and further checks.
    ```

=== "한국어"

    ```text {.prompt}
    작다고 생각한 dimension의 broadcast join에서 worker 메모리 오류가 난다.
    각 worker에 복제되는 데이터와 전체 입력 크기를 구분해 주세요.
    Broadcast와 partitioned 후보의 memory·exchange 비용을 비교해 주세요.
    증거 없이 join 방식만 바꾸는 해결책으로 단정하지 말아 주세요.
    메모리 원인 가설·지지 근거·추가 확인표를 주세요.
    ```

**Key point:** Evidence to check first: actual build-side size and concurrent query memory per worker. Group the plan and metrics for one query ID and include connector details. The LLM may infer small size from the word dimension or ignore partitioned-join costs. Check headroom against the most loaded worker rather than average memory.

## Investigate slow tasks and key skew {#trino-03}

**Prompt:**

=== "English"

    ```text {.prompt}
    Most tasks finish, but some workers spend much longer on a join or aggregation.
    Separate uneven scans from imbalance after key redistribution.
    Separate correlation between slow tasks and hot keys from confirmed cause.
    List missing statistics that could reject the skew hypothesis.
    Return bottleneck candidates, key evidence, and next checks by stage.
    ```

=== "한국어"

    ```text {.prompt}
    대부분 task는 끝났지만 일부 worker가 join 또는 집계를 오래 수행한다.
    Scan 불균형과 key 재분배 이후 불균형을 나눠 주세요.
    느린 task와 특정 key 집중의 연관을 원인 확정과 구분해 주세요.
    Skew 가설을 반박할 수 있는 누락 통계를 적어 주세요.
    Stage별 병목 후보·key 근거·다음 확인표를 주세요.
    ```

**Key point:** Evidence to check first: per-stage task input sizes and redistribution-key distribution. Group the plan and metrics for one query ID and include connector details. The LLM may confirm skew from long tasks alone or assume more workers solve it. Test I/O and load alternatives instead of confirming skew from slow tasks alone.

## Review spill and retry-execution options {#trino-04}

**Prompt:**

=== "English"

    ```text {.prompt}
    Review a proposal to enable spill in response to out-of-memory failures.
    Separate observed OOM locations from assumptions about spill coverage.
    List version-specific spill status and fault-tolerant execution conditions to check.
    Compare memory, disk, and retry costs without promising a fix.
    Return prerequisites, uncertainties, and stop conditions for each option.
    ```

=== "한국어"

    ```text {.prompt}
    OOM 대응안으로 spill을 켜자는 제안의 적용 범위를 검토 중이야.
    관측된 OOM 위치와 spill이 다룰 수 있다는 가정을 나눠 주세요.
    버전별 spill 상태와 fault-tolerant 실행 적용 조건을 확인 항목으로 적어 주세요.
    해결을 보장하지 말고 memory·disk·재시도 비용을 비교해 주세요.
    선택지별 사전 조건·불확실성·중단 기준 표를 주세요.
    ```

**Key point:** Evidence to check first: spill/retry support in the installed version and exchange-storage setup. Group the plan and metrics for one query ID and include connector details. The LLM may assume spill fixes every OOM or retries without an exchange manager provide the same behavior. Check disk I/O, duration, and retry cost as well as successful execution.

## Check Iceberg pruning and storage roles {#trino-05}

**Prompt:**

=== "English"

    ```text {.prompt}
    A query for a small date interval reads more Iceberg files than expected.
    Map S3, Parquet, Iceberg, and Trino roles to the read path.
    Assess evidence for partition, file, row-group, and column pruning separately.
    Do not equate these checks with remote DB aggregation pushdown.
    Return expected behavior, observations, and missing evidence at each pruning step.
    ```

=== "한국어"

    ```text {.prompt}
    작은 날짜 구간을 조회하는데 예상보다 많은 Iceberg file을 읽는다.
    S3·Parquet·Iceberg·Trino 역할을 읽기 경로에 맞춰 나눠 주세요.
    Partition·file·row group·column pruning 근거를 따로 평가해 주세요.
    Remote DB aggregation pushdown과 같은 동작으로 취급하지 말아 주세요.
    Pruning 단계별 기대·관측·누락 근거 표를 주세요.
    ```

**Key point:** Evidence to check first: file statistics and actual scan records for one snapshot. Group the plan and metrics for one query ID and include connector details. The LLM may assume a date filter enables pruning at every level or describe Trino as file storage. Do not collapse partition, file, row-group, and column effects into one measure.

## Review workload placement between Trino and Spark {#trino-06}

**Prompt:**

=== "English"

    ```text {.prompt}
    Interactive BI queries and large historical recalculations compete for resources.
    Assess contention evidence before comparing query-serving and transformation roles.
    Do not treat common Trino and Spark roles as absolute feature limits.
    State missing cost and performance evidence needed for a placement decision.
    Return requirements, placement candidates, trade-offs, and unknowns by job.
    ```

=== "한국어"

    ```text {.prompt}
    대화형 BI 조회와 대규모 과거 재계산이 같은 자원을 두고 경합한다.
    현재 경합 근거를 평가한 뒤 query serving과 변환 책임을 비교해 주세요.
    Trino·Spark의 일반적 역할을 절대적 기능 한계로 취급하지 말아 주세요.
    작업 배치 결정에 필요한 비용·성능 근거가 없으면 명시해 주세요.
    작업별 요구·배치 후보·trade-off·미확인 항목 표를 주세요.
    ```

**Key point:** Evidence to check first: BI latency targets, backfill deadlines, and concurrent-run evidence. Group the plan and metrics for one query ID and include connector details. The LLM may move every slow query to Spark or promise performance from product names alone. Check both workload targets instead of claiming speed from an engine name.
