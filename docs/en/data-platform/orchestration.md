---
id: data-platform-orchestration
status: studied
last_updated: 2026-09-24
last_reviewed: 2026-09-24
knowledge_ids:
  - DPE-07-01
  - DPE-07-02
  - DPE-07-03
  - DPE-07-04
  - DPE-07-05
  - DPE-07-06
  - DPE-07-07
  - DPE-07-08
---

# Data orchestration

This page records conceptual study of orchestration, with Airflow as the main example. It does not claim that a DAG was deployed or operated. Official documentation was checked on 2026-09-24.

## What a DAG manages

An orchestrator manages task order, timing, failures, and reruns. A DAG is the workflow. A task is a unit of work. A dependency sets a condition between tasks. A schedule defines when or how often a workflow runs.

```mermaid
flowchart LR
  E[Extract] --> S[Spark transform]
  S --> D[dbt]
  D --> Q[Quality check]
  Q --> P[Publish]
```

Airflow usually directs compute systems instead of processing large datasets itself. An operator defines how to run a task. Examples include Python, SQL, Bash, Spark job submission, and a dbt command. One possible split is Airflow for orchestration, Spark for batch compute, Flink for streaming, dbt for SQL transformation definitions, Trino for queries, and Iceberg for tables. This is a design example, not a required product stack.

## Retries and idempotency

Transient failures include network timeouts, database connection errors, and temporary cluster issues. A retry may help. Permanent failures include SQL syntax errors, wrong schemas, and code bugs. Repeating them will not fix the cause.

A retry-safe task produces the same final result when run more than once. Blind append can create duplicates. Overwriting a specific partition, MERGE, and replace are alternatives. They still need correct input intervals, keys, and transaction boundaries. The command name alone does not make a task safe. Official guidance also recommends avoiding duplicates on retries and reading and writing specific partitions. [Airflow best practices](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html)

## Backfills and explicit intervals

A backfill recalculates past data. Reasons include a pipeline failure, a fixed logic bug, missing data, a new column, or a business logic change. A full backfill processes the whole period. A partial or partition backfill processes only the needed dates or partitions. Both need idempotency.

Parameters such as `process_date`, `start_date`, `end_date`, `environment`, and `data_interval` help reuse a DAG. “Process 2026-09-24” is easier to rerun than “process today.” Define interval boundaries and the timezone too. Using `now()` or the latest data can change the result of a rerun for the same past interval. [Specific partitions and data intervals](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html)

## Schedule versus readiness

A sensor waits for a condition. It may wait for an S3 file, an upstream DAG, or data readiness. “Try at 02:00” and “the input is ready” are different conditions. A schedule does not resolve data dependencies. Conditions can be checked by polling or through events. Check sensor and event support for the Airflow and provider versions in use.

## Resume from a failure

This state may not require restarting the whole DAG:

```text
Extract: success
Spark: success
dbt: failed
Quality: not run
Publish: not run
```

Fix dbt, then rerun the failed task. First check that prior upstream results are valid and belong to the same interval. The usual `all_success` rule waits for successful upstream tasks. Other rules, such as `all_done`, may run after failures or skips. It is wrong to say that upstream failure always blocks downstream execution. Check the publish gate's actual trigger rule. [Airflow trigger rules](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html#trigger-rules)

An alert should include the DAG, task, failure time, retry count, and error. Identifying the run and data interval also helps investigation.

## Designs to avoid

- Large compute jobs inside an Airflow worker tie up orchestration resources.
- Do not pass large datasets through XCom. Pass small states or paths, and keep data in external storage.
- Too many dependencies between DAGs make failure impact and rerun scope hard to understand.
- Do not use Airflow as a streaming engine. Use a suitable engine for continuous event processing.

Using XCom for small messages and shared storage for large data follows official guidance. [Communication between tasks](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html)

## LLM in Practice: review a backfill plan

Situation: a logic bug is fixed and seven days need reprocessing. Give the LLM the DAG dependencies, explicit date interval, source retention, output partitions, write method, failure state, and acceptance checks.

=== "English"

    ```text {.prompt}
    [Context]
    DAG dependencies, seven-day interval, and source retention: [context]
    Output partitions, write method, failure state, and acceptance checks: [plan]

    [Task]
    Review this seven-day backfill plan before changing it.
    Separate known facts, assumptions, risks, and missing evidence.
    Check input intervals, retry safety, downstream gates, and validation.
    Return a bounded rerun plan and checks for duplicate or missing rows.

    [Output]
    Return the rerun scope and validation list.

    [Checks]
    Compare actual keys, trigger rules, and intervals with before-and-after results for a small partition.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    DAG dependency·7일 구간·source 보존 범위: [맥락]
    출력 partition·write 방식·실패 상태·기준: [계획]

    [요청]
    이 7일 backfill 계획을 바꾸기 전에 먼저 검토해 주세요.
    알려진 사실·가정·위험·부족한 근거를 구분해 주세요.
    입력 구간·retry 안전성·downstream gate·검증을 확인해 주세요.
    제한된 재실행 계획과 중복·누락 행 확인 항목을 주세요.

    [출력]
    재실행 범위와 검증 목록을 주세요.

    [검증]
    실제 key·trigger rule·구간과 작은 partition의 전후 결과를 대조해 주세요.
    ```

Expected output is a rerun scope and validation list. The LLM may assume MERGE is always safe or suggest rerunning the whole DAG. Check real keys, trigger rules, and intervals. Compare results before and after a rerun on a small partition. This page does not claim that these tests were run.

[dbt](dbt.md) · [CDC and Debezium](cdc-debezium.md) · [Handbook home](../index.md)

[Six related practical prompts](../prompts/orchestration.md)
