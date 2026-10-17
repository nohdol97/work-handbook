---
id: prompts-spark
status: overview
last_updated: 2026-10-18
last_reviewed: 2026-10-18
knowledge_ids: []
---

# Apache Spark practical prompts

Copy these examples with the relevant SQL, settings, logs, or proposed changes. Use sanitized material and check suggestions against real evidence and permissions. An example does not authorize system changes or data deletion. These are not measured usage or model-performance results.

[All prompts](index.md) · [Concepts and sources](../data-platform/spark.md)

## Quick selection

| Purpose | Jump to |
| --- | --- |
| Find the cause of join row explosion | [01](#spark-01) |
| Review whether a broadcast join fits memory | [02](#spark-02) |
| Balance output files and task parallelism | [03](#spark-03) |
| Choose cache or a durable intermediate table | [04](#spark-04) |
| Review duplicate effects from foreachBatch retries | [05](#spark-05) |
| Review streaming output mode and late events | [06](#spark-06) |

## Find the cause of join row explosion {#spark-01}

Example prompt:

=== "English"

    ```text {.prompt}
    Review an ETL whose row count grows sharply after a join.
    First compare duplicate-key multiplication with the intended relationship.
    If only existence matters, review semi or anti join semantics; avoid arbitrary deduplication.
    Return expected counts by key and a draft change that preserves meaning.
    ```

=== "한국어"

    ```text {.prompt}
    Join 후 row 수가 크게 늘어난 ETL을 검토 중이야.
    키 중복으로 생기는 다대다 곱과 의도한 관계를 먼저 비교해 줘.
    존재 여부만 필요하다면 semi/anti join의 의미를 검토하고 임의 dedup은 피해 줘.
    키별 예상 row 수 계산과 의미를 보존하는 수정 초안을 작성해 줘.
    ```

**Key point:** Evidence to check first: both grains and expected matches per key. Use plans, task metrics, and sample results from the same run. The LLM may treat broadcast or repartition as a grain fix or remove duplicates without checking meaning. Check a DISTINCT-based count fix against the original aggregation meaning.

## Review whether a broadcast join fits memory {#spark-02}

Example prompt:

=== "English"

    ```text {.prompt}
    Review a proposal to broadcast a small dimension table.
    Assess fit using measured size and per-executor load, not the label small.
    Compare broadcast with the current strategy, including memory pressure and reduced shuffle.
    Return supporting and opposing evidence, missing measurements, and a bounded comparison.
    ```

=== "한국어"

    ```text {.prompt}
    작은 dimension을 broadcast하자는 성능 제안을 검토 중이야.
    작다는 이름 대신 실제 크기와 executor별 부담으로 적합성을 평가해 줘.
    Broadcast와 현 join 전략을 비교하고 메모리 압박과 shuffle 감소를 함께 다뤄 줘.
    찬성·반대 근거, 빠진 측정, 제한된 비교 실험을 작성해 줘.
    ```

**Key point:** Evidence to check first: measured memory for filtered build data and executor headroom. Use plans, task metrics, and sample results from the same run. The LLM may equate compressed size with memory size or assume both join inputs always shuffle. Do not substitute compressed file size for memory demand.

## Balance output files and task parallelism {#spark-03}

Example prompt:

=== "English"

    ```text {.prompt}
    This proposal sharply reduces Spark partitions to produce fewer small Iceberg files.
    Compare repartition shuffle cost with the parallelism loss from coalesce.
    Account for task and table-partition boundaries and compression; target file size is not guaranteed.
    Return a small candidate set and an evaluation table for task times, file distribution, and write cost.
    ```

=== "한국어"

    ```text {.prompt}
    작은 Iceberg 파일을 줄이려고 Spark partition 수를 크게 낮추는 제안이다.
    Repartition의 shuffle 비용과 coalesce의 병렬성 감소를 비교해 줘.
    Task·table partition 경계와 압축률 때문에 목표 파일 크기가 보장되지 않음을 반영해 줘.
    작은 후보 집합과 task 시간·파일 분포·쓰기 비용의 평가표를 작성해 줘.
    ```

**Key point:** Evidence to check first: output distribution by table partition and tail task duration. Use plans, task metrics, and sample results from the same run. The LLM may assume fewer partitions are always faster or equate one file with one task. Check for slower writes and skew introduced while reducing file count.

## Choose cache or a durable intermediate table {#spark-04}

Example prompt:

=== "English"

    ```text {.prompt}
    This workflow reuses an expensive result in several analyses and a later job.
    Find recomputation caused by lazy evaluation and identify the actions that trigger work.
    Compare cache/persist, recomputation, and an intermediate Iceberg table by lifetime and cost.
    Return the decision basis, when to release cache, and management needs for durable results.
    ```

=== "한국어"

    ```text {.prompt}
    비싼 변환 결과를 여러 분석과 다음 job에서도 쓰는 workflow다.
    Lazy evaluation으로 반복 계산되는 구간을 찾고 실제 action을 표시해 줘.
    Cache/persist, 재계산, Iceberg 중간 테이블을 수명과 비용으로 비교해 줘.
    선택 근거와 cache 해제 시점, durable 결과의 관리 항목을 작성해 줘.
    ```

**Key point:** Evidence to check first: whether reuse occurs within one application or across jobs. Use plans, task metrics, and sample results from the same run. The LLM may treat cache as durable across jobs or assume it always helps data used once. Do not rely on cache alone for results needed after restart.

## Review duplicate effects from foreachBatch retries {#spark-05}

Example prompt:

=== "English"

    ```text {.prompt}
    An external sink shows duplicates after a micro-batch failure.
    Review the logic by separating source recovery from sink effects.
    Check whether batch replay and partial success leave only one final effect.
    Return results by failure point and conditions for idempotency measures such as batchId.
    ```

=== "한국어"

    ```text {.prompt}
    Micro-batch 실패 후 외부 sink에 중복 결과가 보이는 상황이야.
    Source 복구와 sink 효과의 보장 범위를 분리해 현재 로직을 검토해 줘.
    Batch 재실행과 부분 성공에서 같은 효과가 한 번만 남는지 검토해 줘.
    실패 지점별 결과 표와 batchId 등 멱등성 수단의 조건을 작성해 줘.
    ```

**Key point:** Evidence to check first: partial-write evidence and the scope of batch identifiers. Use plans, task metrics, and sample results from the same run. The LLM may claim checkpoints or the presence of batchId alone guarantee end-to-end exactly-once. Distinguish retries of one batch from reprocessing with a new checkpoint.

## Review streaming output mode and late events {#spark-06}

Example prompt:

=== "English"

    ```text {.prompt}
    This Structured Streaming aggregate is delayed or omits late events.
    Explain watermark behavior as event-time progress and a state-cleanup basis.
    Separate checks for operator/sink output-mode support from late-event outcomes.
    Return expected aggregates, emission timing, and state-retention assumptions by arrival sequence.
    ```

=== "한국어"

    ```text {.prompt}
    집계 결과가 늦거나 늦은 이벤트가 빠지는 Structured Streaming 작업이다.
    Watermark를 event-time 진행과 state 정리 기준으로 설명해 줘.
    연산·sink의 output mode 지원을 확인할 항목과 late event 결과를 나눠 줘.
    입력 순서별 기대 집계·출력 시점·state 유지 가정을 표로 작성해 줘.
    ```

**Key point:** Evidence to check first: actual output-mode/sink support and the late-input contract. Use plans, task metrics, and sample results from the same run. The LLM may treat watermarks as wall-clock timers or assume every mode works with every sink. Include stalled-watermark samples and inputs beyond the boundary.
