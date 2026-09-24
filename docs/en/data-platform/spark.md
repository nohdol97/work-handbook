---
id: data-platform-spark
status: studied
last_updated: 2026-09-24
last_reviewed: 2026-09-24
knowledge_ids:
  - DPE-04-01
  - DPE-04-02
  - DPE-04-03
  - DPE-04-04
  - DPE-04-05
  - DPE-04-06
  - DPE-04-07
  - DPE-04-08
  - DPE-04-09
  - DPE-04-10
  - DPE-04-11
  - DPE-04-12
  - DPE-04-13
  - DPE-04-14
---

# Apache Spark

Page type: Learn. This page records concepts and design examples from the supplied study material. `studied` means conceptual study, not hands-on implementation or production validation. Examples were not run.

## 4.1 Architecture

A Spark application has a driver and executors. The **driver** manages the application, plans jobs, schedules tasks, and coordinates executors. **Executors** run tasks, process data, and hold cached data.

A cluster manager allocates resources. Examples include Kubernetes, YARN, and Spark Standalone. With Spark on Kubernetes, Kubernetes manages resources for driver and executor pods.

```text
Application → Driver → Executors
```

## 4.2 Execution model

```text
Application → Job → Stage → Task
```

An **action** triggers work organized into jobs. **Stages** separate work at boundaries such as shuffles. A **task** processes a Spark partition within a stage. A **Spark partition** is a logical unit of parallel data processing. The **DAG** represents dependencies between transformations.

## 4.3 Lazy evaluation

Transformations such as filter, map, and join define a new dataset. Calling them does not immediately compute the full result. Actions such as `count`, `collect`, or a write trigger execution.

For Spark SQL and DataFrames, query planning can be understood as:

```text
User Code → Logical Plan → Optimized Logical Plan → Physical Plan → Execution
```

Catalyst optimizes query plans. Use `explain()` to inspect a plan. Plan inspection is part of understanding the work, not proof that the work will be fast.

## 4.4 Narrow and wide dependencies

A **narrow dependency** lets each output partition depend on a small set of input partitions. Map and filter are common examples. They may run without major movement between workers.

A **wide dependency** needs redistribution across partitions. GroupBy, repartition, and many joins can introduce a shuffle. A logical join is not proof that both inputs will shuffle: broadcast and compatible existing partitioning can change the physical plan.

## 4.5 Shuffle

Shuffle redistributes records between workers. Its cost can include network I/O, shuffle writes and reads, sorting, serialization, disk spill, and new stage boundaries.

```text
Worker A ─┐
Worker B ─┼→ Network Redistribution
Worker C ─┘
```

Large joins and aggregations are often expensive because data must move. Look at the physical plan and observed shuffle volume before treating this as the bottleneck.

## 4.6 Join strategies

| Strategy | Typical use and behavior | Risk |
| --- | --- | --- |
| Broadcast hash join | Send a small dimension to executors processing a large fact table | The broadcast side may be too large for memory |
| Sort-merge join | Partition large inputs by join key, sort, then merge | Network and sort cost |
| Shuffled hash join | Partition inputs, then build and probe a hash table | Per-partition memory pressure |

Fact-plus-dimension is a common analytical pattern. A large-to-large join may move much more data. A **semi join** checks existence; an **anti join** selects nonmatches. They can express the intent more clearly when columns from the other side are not needed.

Check **join cardinality**. Duplicate join keys on both sides can multiply result rows and cause a join explosion. A strategy change does not fix incorrect assumptions about key uniqueness.

## 4.7 Partition management

`repartition` redistributes data and normally introduces a shuffle. Use it to increase parallelism, redistribute by key, or influence output layout. `coalesce` usually reduces partition count and can avoid a full shuffle.

Keyed repartitioning sends matching key values to the same partition. Partition count affects task count, memory pressure, and possible output-file count. Target partition size and target file size are related, but are not interchangeable settings. Fewer tasks can reduce overhead while also reducing parallelism.

## 4.8 Cache and persist

Cache or persist can keep an intermediate result in memory or on disk. This can avoid repeating an expensive transformation used by several later queries:

```text
Expensive Transform → Cache → Query A / Query B
```

Call `unpersist` when the result is no longer needed. Caching may be a poor choice for data used only once, a very large dataset, or a memory-constrained job.

For reuse across jobs or long periods, a durable intermediate Iceberg table may be more suitable than executor cache. Cache and durable storage solve different lifecycle problems.

## 4.9 Data skew

Skew means a partition gets much more data or work than others. If `team_id = A` holds 80% of rows and all other teams hold 20%, one task may dominate completion time.

A **hot key** can slow a join or aggregation. `NULL`, `UNKNOWN`, and `0` can become hot default keys. Possible responses include:

- **Salting:** split a hot key into several temporary keys, process them, then combine correctly.
- **Pre-aggregation:** aggregate locally before moving data.
- **Heavy-key path:** process known hot keys separately.
- **Adaptive Query Execution (AQE):** use runtime statistics for supported plan changes and skew optimizations.

Salting a batch aggregation is not a general solution for ordered event processing. Splitting one ordered key can change ordering guarantees. Distinguish Spark batch skew from Kafka key-ordering design.

## 4.10 Performance engineering

Possible bottlenecks include CPU, executor memory, heap pressure, garbage collection, disk spill, network, shuffle, S3 scans, small files, and slow tasks.

**Executor sizing** chooses cores and memory for the workload. **Spill** writes intermediate data to disk when it does not fit in memory. A **straggler** is a task that finishes much later than peers; skew is one possible cause. **Speculative execution** can run another attempt of a slow task and use the first successful result. It does not remove the underlying skew.

Use the Spark UI to locate the expensive stage and compare task metrics. Diagnose before changing several settings at once.

## 4.11 Spark and Iceberg

```text
Iceberg → Spark → Transform → Iceberg
```

Iceberg metadata helps Spark plan which files to scan. Filters and column selection can reduce files, row groups, and columns read. One Iceberg file is not necessarily one Spark task. Split planning and file layout both affect parallelism.

Writes need suitable distribution, target file sizes, and query-aware sort order. MERGE can build a CDC current-state table. Write skew can overload one partition or key. Tasks produce files; an Iceberg commit makes a new snapshot visible.

Streaming writes, MERGE operations, and small files can accumulate **maintenance debt**. Plan compaction and related maintenance with the write workload.

## 4.12 Structured Streaming

Structured Streaming treats an input stream as a growing table. Micro-batch execution is a useful starting model:

```text
Kafka → Micro-batch → Spark → Sink
```

| Concept | Role |
| --- | --- |
| Kafka source | Reads topic records |
| Checkpoint | Stores offsets and recovery information |
| State | Remembers data for aggregation, deduplication, and other stateful work |
| Event time | Time of the real event |
| Late event | Arrives after newer event-time data |
| Watermark | Tracks event-time progress for supported state and late-data handling |
| Window | Groups data into time ranges |
| Deduplication | Suppresses repeated logical events within its configured scope |
| Output mode | Controls how results are emitted |
| `foreachBatch` | Applies batch logic to each micro-batch |

Frequent streaming writes to Iceberg can lower ingestion delay while producing small files. Compaction may be necessary. Streaming suits ongoing data; batch Spark often suits large historical backfills.

## 4.13 Spark's role

Spark is a distributed data-processing engine. It supports large ETL, joins, aggregations, backfills, lakehouse transformations, ML dataset creation, batch jobs, and Structured Streaming.

Spark is compute. S3 supplies storage, and Iceberg supplies table management. Using Spark does not make Spark the durable storage layer.

## 4.14 Do you still need dbt?

Spark and dbt have different roles. Spark executes distributed computation. dbt manages SQL transformation projects. They can be used together:

```text
Raw → Spark → Silver → dbt → Gold / Mart
```

This is an example, not a mandatory layer boundary. Simple SQL transformations may instead use dbt with Trino or a warehouse, without Spark. Choose based on the required computation and transformation-management needs.

## Qualifications for real use

A logical join does not always shuffle both inputs. Broadcast or existing partition layout can change the physical plan. Use `explain()` and the Spark UI to inspect shuffle bytes, task time, spill, GC, and input size. AQE supports specific runtime plan changes; it does not fix all skew. For join explosion, check key duplication and grain first. [Spark performance guide](https://spark.apache.org/docs/latest/sql-performance-tuning.html)

Speculation repeats a slow task but does not remove skew. Cache and durable tables have different lifetimes. Repartition normally shuffles, and too much partition reduction lowers parallelism. The Spark-to-dbt path is an example, not a required architecture.

An Iceberg target file size is not a promised output size. A file cannot exceed its writing task or cross an Iceberg partition boundary. Compressed file size differs from Spark's in-memory size. [Iceberg Spark writes](https://iceberg.apache.org/docs/latest/spark-writes/)

A watermark tracks event-time progress and supports state cleanup; it is not just a waiting timer. Append, update, and complete output modes have operator and sink constraints. `foreachBatch` writes are at-least-once by default. Use an idempotent sink design, such as deduplication by `batchId`, and test retries before claiming end-to-end exactly-once. [Spark Structured Streaming](https://spark.apache.org/docs/latest/streaming/apis-on-dataframes-and-datasets.html)

## Related reading

[Iceberg](lakehouse-iceberg.md), [Flink](flink.md), [Event semantics](event-architecture.md).

## LLM in practice: Slow-stage diagnosis

- Situation: One task takes much longer than others in a hypothetical join stage.
- Context to give the LLM: Give the physical plan, per-task input, shuffle, spill, GC, duration, key counts, and executor resources.
- Expected output: Expect evidence and falsification checks for each cause, plus small experiments.
- What the LLM can get wrong: The LLM may assume all stragglers are skew or always recommend broadcast.
- How to validate: Compare the Spark UI and plan, then change one setting at a time with the same input.

Example prompt:

=== "English"

    ```text {.prompt}
    [Context]
    Plan and distribution: [physical plan, key counts, executor resources]
    Task metrics: [input, shuffle, spill, GC, duration]

    [Task]
    Diagnose the slow stage before proposing a redesign.
    Rank skew, memory-pressure, and slow-I/O hypotheses by evidence.

    [Output]
    Separate evidence from assumptions; request missing metrics and falsification checks.

    [Checks]
    Propose one controlled test per hypothesis, changing one condition on the same input.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    계획과 분포: [physical plan·key 빈도·executor 자원]
    Task 지표: [입력·shuffle·spill·GC·실행 시간]

    [요청]
    재설계 제안 전에 느린 stage를 진단해 줘.
    Skew·메모리 압박·느린 I/O 가설을 근거에 따라 순위로 정리해 줘.

    [출력]
    근거와 가정을 구분하고 누락된 측정 및 반증 조건을 작성해 줘.

    [검증]
    가설마다 동일 입력으로 한 조건만 바꾸는 통제된 실험을 제안해 줘.
    ```

[See six more practical prompts for this topic](../prompts/spark.md)

LLM output is a working hypothesis. Check it against official docs and actual configuration, logs, and measurements. External documents reviewed: 2026-09-24. This does not mean an implementation version was tested.
