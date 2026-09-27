---
id: data-platform-spark
status: studied
last_updated: 2026-09-27
last_reviewed: 2026-09-27
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

# Chapter 4 — Spark

Page type: Learn. This page records concepts and design examples from the supplied study material. `studied` means conceptual study, not hands-on implementation or production validation. Examples were not run.

The source body keeps its numbering, order, and form. [Source qualifications](#source-notes) separate applicable corrections and conditions by source section number.

**Reading note:** The source core below keeps the original order and form. Read the section-specific corrections, conditions, and additions in the supplement after the source material; some original statements are simplified.

<!-- SOURCE CORE START -->

## 4.1 Spark Architecture

Basic parts of a Spark application:

```text
Application
   ↓
Driver
   ↓
Executors
```

### Driver

- Manage the whole application
- Job planning
- Task scheduling
- Executor coordination

### Executor

- Execute actual tasks
- Process data
- Keep cached data

### Cluster Manager

A system that allocates Spark resources.

Example:

- Kubernetes
- YARN
- Standalone

With Spark on Kubernetes, Kubernetes manages execution resources for driver/executor pods.

---

## 4.2 Execution Model

Spark execution units:

```text
Application
  ↓
Job
  ↓
Stage
  ↓
Task
```

### Job

A large unit of work created when an action runs.

### Stage

An execution phase divided by boundaries such as shuffles.

### Task

An execution unit that processes one Spark partition.

### Spark Partition

A logical unit of data that Spark processes in parallel.

### DAG

Represent transformation dependencies as a graph.

---

## 4.3 Lazy Evaluation

Spark transformations do not run as soon as they are called.

Example:

```text
filter
map
join
```

Defining these operations does not start the actual computation until an action is called.

### Transformation

Define a new dataset.

### Action

Trigger actual execution.

Example:

- count
- collect
- write

---

### Query Planning

Conceptually:

```text
User Code
  ↓
Logical Plan
  ↓
Optimized Logical Plan
  ↓
Physical Plan
  ↓
Execution
```

For Spark SQL/DataFrames, the Catalyst Optimizer optimizes the query plan.

Use `explain()` to inspect the plan.

---

## 4.4 Narrow vs Wide Dependencies

### Narrow Dependency

Each output partition depends on only a few input partitions.

Example:

```text
map
filter
```

Data may not need to move much between workers.

### Wide Dependency

Data must be redistributed across partitions.

Example:

```text
groupBy
join
repartition
```

This causes a shuffle.

---

## 4.5 Shuffle

Shuffle is a very important concept for Spark performance.

```text
Worker A ─┐
Worker B ─┼→ Network Redistribution
Worker C ─┘
```

Possible costs:

- Network I/O
- Shuffle Write
- Shuffle Read
- Sort
- Serialization
- Disk Spill
- Stage Boundary

Key point:

> **Large joins and GROUP BY operations are expensive because data moves between workers.**

---

## 4.6 Join Strategies

### Broadcast Hash Join

Large fact + small dimension.

```text
Large Fact
+
Small Dimension
```

Broadcast the small table to all executors.

Benefit:
- Reduce shuffling of the large table

Caution:
- An overly large broadcast input can cause memory problems

---

### Sort-Merge Join

A common strategy for joining two large tables.

Conceptually:

```text
Shuffle both sides by join key
↓
Sort
↓
Merge
```

---

### Shuffle Hash Join

Partition both inputs, then perform a hash join.

---

### Fact + Dimension

A common analytical join pattern.

### Large-Large Join

When both sides are large, shuffle costs can be very high.

### Semi / Anti Join

Used for existence checks or exclusion conditions.

### Join Cardinality / Join Explosion

Many duplicate join keys can produce far more result rows than expected.

---

## 4.7 Partition Management

### repartition

Redistribute partitions.

A shuffle may occur.

Uses:
- Increase parallelism
- Redistribute by a specific key
- Adjust output file count

### coalesce

Mainly used to reduce partition count.

A full shuffle is not always required.

---

### Keyed Repartitioning

Send the same key values to the same partition.

### Task Parallelism

Spark partition count is directly related to task parallelism.

### Target Partition Size / Output File Count

Partition count relates to:
- Task count
- File count
- Memory pressure

These are connected.

---

## 4.8 Cache / Persist

Spark can keep intermediate results in memory or on disk.

### Why use it?

Recomputing the same data many times can be expensive.

```text
Expensive Transform
  ↓
Cache
  ├─ Query A
  └─ Query B
```

### unpersist

Release cached data when it is no longer needed.

### Cache is not always helpful

- Data used only once
- A very large dataset
- An environment with limited memory

Caching can be a disadvantage in these cases.

### Durable Iceberg Intermediate Table

For results reused over a long period or across jobs, durable storage such as an intermediate Iceberg table may fit better than cache.

---

## 4.9 Data Skew

Data skew means data concentrates in particular partitions.

Example:

```text
team_id = A → 80%
Others → 20%
```

One task may then take much longer than the others.

### Hot Key

Data concentrates on a particular key.

### Skewed Join / Aggregation

One key becomes a bottleneck in a join or GROUP BY.

### Null / Default Key Skew

Data can concentrate on default values such as `NULL`, `UNKNOWN`, or `0`.

### Salting

Add a salt to a hot key, spread it across several keys, then combine the results later.

However, **this is difficult to apply directly to streaming/event processing where the original key order matters.**  
Distinguish Spark batch join/aggregation skew from Kafka ordering problems.

### Pre-Aggregation

Aggregate partially before the shuffle to reduce data movement.

### Heavy-Key Special Path

Process a specific hot key on a separate path.

### AQE

Adaptive Query Execution can use runtime statistics for some skew optimizations.

---

## 4.10 Spark Performance Engineering

Common bottlenecks:

- CPU
- Executor Memory
- Heap Pressure
- GC
- Disk Spill
- Network
- Shuffle
- S3 Scan
- Small Files
- Straggler

### Executor Sizing

Adjust executor memory/cores to the workload.

### Spill

Write intermediate data that does not fit in memory to disk.

### Straggler

One task finishes much later than the others.

Skew can be one cause.

### Speculative Execution

Run another copy of an unusually slow task on a different executor and use the first result to finish.

### Spark UI

Important for finding which stage/task is the bottleneck.

---

## 4.11 Spark + Iceberg

Spark is one of the main compute engines for batch processing of Iceberg data.

```text
Iceberg
  ↓
Spark
  ↓
Transform
  ↓
Iceberg
```

### Iceberg Scan Planning

Use Iceberg metadata to decide which files to read.

### Predicate Pushdown / Pruning

Avoid reading unnecessary files/row groups.

### Spark Tasks vs Iceberg Files

One file does not always map to one task, but file layout affects task parallelism and scan efficiency.

### Write Distribution

Distribute data appropriately when producing files.

### Target File Size

Avoid creating files that are too small.

### Sort Order

Optimize layout for query patterns.

### MERGE

Can be used to build CDC current-state tables.

### Write Skew

Writes may concentrate on a particular partition/key.

### Commit Behavior

Spark tasks create files, and an Iceberg commit publishes a new snapshot to the table.

### Maintenance Debt

Streaming writes, MERGE operations, and small files can build up and require maintenance such as compaction.

---

## 4.12 Structured Streaming

Spark Structured Streaming provides a model for treating streaming data as a table.

It can mainly be understood as a **micro-batch** model.

```text
Kafka
 ↓
Micro Batch
 ↓
Spark
 ↓
Sink
```

### Kafka Source

Use a Kafka topic as a streaming source.

### Checkpoint

Store processing state, offsets, and other recovery information.

### State

Keep state needed for streaming aggregation/deduplication.

### Event Time

The time when an event actually happened.

### Late Events

An event that arrives late.

### Watermark

A basis for deciding how late an event can be before the system stops waiting for it.

### Window

Aggregate data over time ranges.

### Deduplication

Remove duplicate events.

### Output Modes

Decide how to emit aggregation results.

### foreachBatch

Process each micro-batch with batch logic.

### Streaming → Iceberg

Ingest into Iceberg in near real time.

Caution:

```text
Frequent writes
→ Small files
→ Compaction needed
```

### Streaming vs Batch Backfill

Streaming fits ongoing processing; batch Spark fits large historical reprocessing.

---

## 4.13 Spark's Role

Question:

> What is Spark's role?

Key point:

> **Spark is a large-scale distributed data-processing engine.**

Main uses:

- Large-scale ETL
- Join
- Aggregation
- Backfill
- Lakehouse Transform
- ML dataset creation
- Batch Processing
- Structured Streaming

Spark is not storage.

```text
Iceberg / S3
→ Storage/Table

Spark
→ Compute
```

---

## 4.14 Do You Need dbt When Using Spark?

Their roles differ.

```text
Spark
→ Large-scale data-processing engine

dbt
→ SQL transformation management layer
```

They can be used together.

Example:

```text
Raw
 ↓
Spark
 ↓
Silver
 ↓
dbt
 ↓
Gold / Mart
```

For simple SQL transformations, dbt with Trino or a warehouse may work without Spark.

---

<!-- SOURCE CORE END -->

## Source qualifications {#source-notes}

### 4.4–4.6 and 4.9 Join plans and skew

A logical join does not always shuffle both inputs. Broadcast or existing partition layout can change the physical plan. Use `explain()` and the Spark UI to inspect shuffle bytes, task time, spill, GC, and input size. AQE supports specific runtime plan changes; it does not fix all skew. For join explosion, check key duplication and grain first. [Spark performance guide](https://spark.apache.org/docs/latest/sql-performance-tuning.html)

### 4.7–4.10 and 4.14 Execution and role boundaries

Speculation repeats a slow task but does not remove skew. Cache and durable tables have different lifetimes. Repartition normally shuffles, and too much partition reduction lowers parallelism. The Spark-to-dbt path is an example, not a required architecture.

### 4.11 Iceberg file size

An Iceberg target file size is not a promised output size. A file cannot exceed its writing task or cross an Iceberg partition boundary. Compressed file size differs from Spark's in-memory size. [Iceberg Spark writes](https://iceberg.apache.org/docs/latest/spark-writes/)

### 4.12 Watermarks and output guarantees

A watermark tracks event-time progress and supports state cleanup; it is not just a waiting timer. Append, update, and complete output modes have operator and sink constraints. `foreachBatch` writes are at-least-once by default. Use an idempotent sink design, such as deduplication by `batchId`, and test retries before claiming end-to-end exactly-once. [Spark Structured Streaming](https://spark.apache.org/docs/latest/streaming/apis-on-dataframes-and-datasets.html)

### 4.3–4.7 Additional plan, join, and partition distinctions

Reading a plan does not prove good performance. Check the physical plan and measured shuffle volume first. Sort-merge joins have network and sort costs. Shuffled hash joins partition the inputs, then build and probe a hash table. They can create memory pressure per partition. Changing join strategy does not fix a wrong assumption about key uniqueness.

A semi join selects matching rows; an anti join selects nonmatches. They express existence checks clearly when columns from the other table are not needed. Target partition size and target file size are related but are not the same setting. Fewer tasks can reduce both overhead and parallelism.

### 4.10–4.12 Additional processing, reading, and state distinctions

Compare task metrics in the Spark UI and diagnose the bottleneck before changing several settings at once. For Iceberg reads, column selection as well as filters can reduce data read. File split planning and layout both affect parallelism. Plan compaction with the write workload.

Structured Streaming can be understood as a growing-table model. A late event can arrive after newer event-time data. Deduplication suppresses repeated logical events within its configured scope.

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
