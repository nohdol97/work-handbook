---
id: prompts-spark
status: overview
last_updated: 2026-09-24
last_reviewed: 2026-09-24
knowledge_ids: []
---

# Apache Spark practical prompts

Page type: Reference. These six authored, hypothetical examples apply the [existing study material](../data-platform/spark.md). They do not claim production experience, measured usage frequency, or model results. The examples were not run.

Choose a case and replace bracketed inputs with sanitized information. Each prompt has 한국어 and English tabs for language selection and copying. Treat LLM output as a hypothesis. Check actual settings, logs, official docs, and bounded tests. This page does not authorize production actions or permission changes.

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

- **Situation:** Review a hypothetical ETL whose row count grows sharply after a join.
- **Context to give the LLM:** Input definitions: [grain on each side, join keys, counts per key, null handling]; Intent and execution: [required result, join condition, row counts, plan].

Example prompt:

=== "English"

    ```text {.prompt}
    [Context]
    Input definitions: [grain on each side, join keys, counts per key, null handling]
    Intent and execution: [required result, join condition, row counts, plan]

    [Task]
    First compare duplicate-key multiplication with the intended relationship.
    If only existence matters, review semi or anti join semantics; avoid arbitrary deduplication.
    Separate observations, assumptions, hypotheses, and missing evidence.

    [Output]
    Return expected counts by key and a draft change that preserves meaning.

    [Checks]
    Compare expected and actual rows for synthetic many-to-many, unmatched, and null-key cases.
    Provide review and test plans only; do not run or change production.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    입력 정의: [양쪽 grain·join key·키별 건수·null 처리]
    의도와 실행: [필요한 결과·join 조건·전후 row 수·계획]

    [요청]
    키 중복으로 생기는 다대다 곱과 의도한 관계를 먼저 비교해 줘.
    존재 여부만 필요하다면 semi/anti join의 의미를 검토하고 임의 dedup은 피해 줘.
    관찰, 가정, 가설, 부족한 근거를 구분해 줘.

    [출력]
    키별 예상 row 수 계산과 의미를 보존하는 수정 초안을 작성해 줘.

    [검증]
    합성 다대다·미일치·null 표본으로 기대 row와 결과를 대조해 줘.
    운영 실행·변경 없이 검토와 검증 계획만 제시해 줘.
    ```

- **Expected output:** Expected counts by key and a draft change that preserves meaning.
- **What the LLM can get wrong:** The LLM may treat broadcast or repartition as a grain fix or remove duplicates without checking meaning.
- **How to validate:** Compare expected and actual rows for synthetic many-to-many, unmatched, and null-key cases.

## Review whether a broadcast join fits memory {#spark-02}

- **Situation:** Review a hypothetical proposal to broadcast a small dimension table.
- **Context to give the LLM:** Plan and size: [current physical plan, size after filtering, observed memory]; Resources and cost: [executor resources, concurrent tasks, GC, spill, shuffle bytes].

Example prompt:

=== "English"

    ```text {.prompt}
    [Context]
    Plan and size: [current physical plan, size after filtering, observed memory]
    Resources and cost: [executor resources, concurrent tasks, GC, spill, shuffle bytes]

    [Task]
    Assess fit using measured size and per-executor load, not the label small.
    Compare broadcast with the current strategy, including memory pressure and reduced shuffle.
    Separate observations, assumptions, hypotheses, and missing evidence.

    [Output]
    Return supporting and opposing evidence, missing measurements, and a bounded comparison.

    [Checks]
    Check actual plans, peak memory, GC, shuffle, and result equality on the same input.
    Provide review and test plans only; do not run or change production.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    계획과 크기: [현재 physical plan·필터 후 크기·실측 메모리]
    자원과 비용: [executor 자원·동시 task·GC·spill·shuffle bytes]

    [요청]
    작다는 이름 대신 실제 크기와 executor별 부담으로 적합성을 평가해 줘.
    Broadcast와 현 join 전략을 비교하고 메모리 압박과 shuffle 감소를 함께 다뤄 줘.
    관찰, 가정, 가설, 부족한 근거를 구분해 줘.

    [출력]
    찬성·반대 근거, 빠진 측정, 제한된 비교 실험을 작성해 줘.

    [검증]
    동일 입력의 실제 계획·peak memory·GC·shuffle·결과 일치를 확인해 줘.
    운영 실행·변경 없이 검토와 검증 계획만 제시해 줘.
    ```

- **Expected output:** Supporting and opposing evidence, missing measurements, and a bounded comparison.
- **What the LLM can get wrong:** The LLM may equate compressed size with memory size or assume both join inputs always shuffle.
- **How to validate:** Check actual plans, peak memory, GC, shuffle, and result equality on the same input.

## Balance output files and task parallelism {#spark-03}

- **Situation:** This hypothetical proposal sharply reduces Spark partitions to produce fewer small Iceberg files.
- **Context to give the LLM:** Distribution: [Spark partition count, task times, file sizes, Iceberg partitions]; Write settings: [repartition/coalesce location, distribution keys, target file size].

Example prompt:

=== "English"

    ```text {.prompt}
    [Context]
    Distribution: [Spark partition count, task times, file sizes, Iceberg partitions]
    Write settings: [repartition/coalesce location, distribution keys, target file size]

    [Task]
    Compare repartition shuffle cost with the parallelism loss from coalesce.
    Account for task and table-partition boundaries and compression; target file size is not guaranteed.
    Separate observations, assumptions, hypotheses, and missing evidence.

    [Output]
    Return a small candidate set and an evaluation table for task times, file distribution, and write cost.

    [Checks]
    Change one setting at a time on the same data and compare slow-task duration, file counts, and sizes.
    Provide review and test plans only; do not run or change production.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    현재 분포: [Spark partition 수·task 시간·파일 크기·Iceberg partition]
    쓰기 설정: [repartition/coalesce 위치·분포 key·목표 파일 크기]

    [요청]
    Repartition의 shuffle 비용과 coalesce의 병렬성 감소를 비교해 줘.
    Task·table partition 경계와 압축률 때문에 목표 파일 크기가 보장되지 않음을 반영해 줘.
    관찰, 가정, 가설, 부족한 근거를 구분해 줘.

    [출력]
    작은 후보 집합과 task 시간·파일 분포·쓰기 비용의 평가표를 작성해 줘.

    [검증]
    동일 데이터에서 한 설정씩 바꾸고 tail task 시간·총 파일 수·크기를 비교해 줘.
    운영 실행·변경 없이 검토와 검증 계획만 제시해 줘.
    ```

- **Expected output:** A small candidate set and an evaluation table for task times, file distribution, and write cost.
- **What the LLM can get wrong:** The LLM may assume fewer partitions are always faster or equate one file with one task.
- **How to validate:** Change one setting at a time on the same data and compare slow-task duration, file counts, and sizes.

## Choose cache or a durable intermediate table {#spark-04}

- **Situation:** This hypothetical workflow reuses an expensive result in several analyses and a later job.
- **Context to give the LLM:** Reuse pattern: [actions, job boundaries, reuse count, lifetime]; Cost and resources: [compute time, result size, memory, restart needs].

Example prompt:

=== "English"

    ```text {.prompt}
    [Context]
    Reuse pattern: [actions, job boundaries, reuse count, lifetime]
    Cost and resources: [compute time, result size, memory, restart needs]

    [Task]
    Find recomputation caused by lazy evaluation and identify the actions that trigger work.
    Compare cache/persist, recomputation, and an intermediate Iceberg table by lifetime and cost.
    Separate observations, assumptions, hypotheses, and missing evidence.

    [Output]
    Return the decision basis, when to release cache, and management needs for durable results.

    [Checks]
    Measure recomputation, cache use, and write/read cost; check reuse needs after restart.
    Provide review and test plans only; do not run or change production.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    재사용 패턴: [action 목록·job 경계·재사용 횟수·수명]
    비용과 자원: [계산 시간·데이터 크기·메모리·재시작 요구]

    [요청]
    Lazy evaluation으로 반복 계산되는 구간을 찾고 실제 action을 표시해 줘.
    Cache/persist, 재계산, Iceberg 중간 테이블을 수명과 비용으로 비교해 줘.
    관찰, 가정, 가설, 부족한 근거를 구분해 줘.

    [출력]
    선택 근거와 cache 해제 시점, durable 결과의 관리 항목을 작성해 줘.

    [검증]
    실제 재계산 횟수·cache 사용·쓰기/읽기 비용을 측정하고 재시작 시 재사용 요구를 확인해 줘.
    운영 실행·변경 없이 검토와 검증 계획만 제시해 줘.
    ```

- **Expected output:** The decision basis, when to release cache, and management needs for durable results.
- **What the LLM can get wrong:** The LLM may treat cache as durable across jobs or assume it always helps data used once.
- **How to validate:** Measure recomputation, cache use, and write/read cost; check reuse needs after restart.

## Review duplicate effects from foreachBatch retries {#spark-05}

- **Situation:** In this hypothetical case, an external sink shows duplicates after a micro-batch failure.
- **Context to give the LLM:** Processing details: [foreachBatch logic, batchId, checkpoint, retry logs]; Sink contract: [write mode, idempotency keys, commit boundary, partial success].

Example prompt:

=== "English"

    ```text {.prompt}
    [Context]
    Processing details: [foreachBatch logic, batchId, checkpoint, retry logs]
    Sink contract: [write mode, idempotency keys, commit boundary, partial success]

    [Task]
    Review the logic by separating source recovery from sink effects.
    Check whether batch replay and partial success leave only one final effect.
    Separate observations, assumptions, hypotheses, and missing evidence.

    [Output]
    Return results by failure point and conditions for idempotency measures such as batchId.

    [Checks]
    Plan applying the same batch twice in an isolated sink and checking results after partial success.
    Provide review and test plans only; do not run or change production.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    처리 정보: [foreachBatch 로직·batchId·checkpoint·재시도 로그]
    Sink 계약: [write 방식·멱등 key·commit 경계·부분 성공 처리]

    [요청]
    Source 복구와 sink 효과의 보장 범위를 분리해 현재 로직을 검토해 줘.
    Batch 재실행과 부분 성공에서 같은 효과가 한 번만 남는지 검토해 줘.
    관찰, 가정, 가설, 부족한 근거를 구분해 줘.

    [출력]
    실패 지점별 결과 표와 batchId 등 멱등성 수단의 조건을 작성해 줘.

    [검증]
    격리된 sink에서 같은 batch를 두 번 적용하고 부분 성공 후 결과도 대조하는 계획을 적어 줘.
    운영 실행·변경 없이 검토와 검증 계획만 제시해 줘.
    ```

- **Expected output:** Results by failure point and conditions for idempotency measures such as batchId.
- **What the LLM can get wrong:** The LLM may claim checkpoints or the presence of batchId alone guarantee end-to-end exactly-once.
- **How to validate:** Plan applying the same batch twice in an isolated sink and checking results after partial success.

## Review streaming output mode and late events {#spark-06}

- **Situation:** This hypothetical Structured Streaming aggregate is delayed or omits late events.
- **Context to give the LLM:** Aggregate definition: [event time, window, watermark, deduplication rules]; Execution details: [output mode, sink, Spark version, synthetic arrival order].

Example prompt:

=== "English"

    ```text {.prompt}
    [Context]
    Aggregate definition: [event time, window, watermark, deduplication rules]
    Execution details: [output mode, sink, Spark version, synthetic arrival order]

    [Task]
    Explain watermark behavior as event-time progress and a state-cleanup basis.
    Separate checks for operator/sink output-mode support from late-event outcomes.
    Separate observations, assumptions, hypotheses, and missing evidence.

    [Output]
    Return expected aggregates, emission timing, and state-retention assumptions by arrival sequence.

    [Checks]
    Compare version docs with bounded out-of-order and late-data tests, including output and state size.
    Provide review and test plans only; do not run or change production.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    집계 정의: [event time·window·watermark·중복 제거 규칙]
    실행 정보: [output mode·sink·Spark 버전·합성 도착 순서]

    [요청]
    Watermark를 event-time 진행과 state 정리 기준으로 설명해 줘.
    연산·sink의 output mode 지원을 확인할 항목과 late event 결과를 나눠 줘.
    관찰, 가정, 가설, 부족한 근거를 구분해 줘.

    [출력]
    입력 순서별 기대 집계·출력 시점·state 유지 가정을 표로 작성해 줘.

    [검증]
    버전 문서와 제한된 순서 변경·늦은 표본 실험에서 출력과 state 크기를 대조해 줘.
    운영 실행·변경 없이 검토와 검증 계획만 제시해 줘.
    ```

- **Expected output:** Expected aggregates, emission timing, and state-retention assumptions by arrival sequence.
- **What the LLM can get wrong:** The LLM may treat watermarks as wall-clock timers or assume every mode works with every sink.
- **How to validate:** Compare version docs with bounded out-of-order and late-data tests, including output and state size.
