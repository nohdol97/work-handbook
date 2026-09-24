---
id: data-platform-flink
status: studied
last_updated: 2026-09-24
last_reviewed: 2026-09-24
knowledge_ids:
  - DPE-05-01
  - DPE-05-02
  - DPE-05-03
  - DPE-05-04
  - DPE-05-05
  - DPE-05-06
  - DPE-05-07
  - DPE-05-08
  - DPE-05-09
  - DPE-05-10
  - DPE-05-11
  - DPE-05-12
  - DPE-05-13
  - DPE-05-14
---

# Apache Flink

Page type: Learn. This page records concepts and design examples from the supplied study material. `studied` means conceptual study, not hands-on implementation or production validation. Examples were not run.

## 5.1 Why Flink?

A useful historical mental model is that Spark grew from batch processing toward streaming, while Flink centers on continuous stream processing. Spark Structured Streaming commonly uses micro-batches. Flink commonly processes a continuous stream as records arrive.

Flink is useful for stateful streaming, event time, watermarks, windows, timers, low latency, and complex real-time rules. Example workloads include anomaly detection, session analysis, error rate over the last five minutes, and live feature calculation. Its short definition is **a stateful stream-processing engine**.

## 5.2 Architecture

The **JobManager** coordinates the job. It is roughly comparable to Spark's driver for this introductory mental model. **TaskManagers** execute tasks, roughly like Spark executors. The systems are not identical.

An **operator** is a processing step:

```text
Source → Filter → KeyBy → Window → Aggregate → Sink
```

**Parallelism** is the number of parallel instances of an operator. A **task slot** is a logical resource-allocation unit within a TaskManager. It is not simply a synonym for a CPU core.

## 5.3 DataStream model

```text
Source → Transformation → Sink
```

Sources can read Kafka, CDC, or files. Transformations include filter, map, keyBy, window, and aggregate. Sinks can write to Iceberg, Kafka, a database, or a search store.

`keyBy(user_id)` groups events by key for downstream keyed processing. It enables state for each key:

```text
Stream → KeyBy → Stateful Processing
```

## 5.4 Event time

Distinguish **event time**, when an action happened; **processing time**, when the operator processes it; and **ingestion time**, when it enters the system. Events can arrive late or out of order. Event-time processing lets analysis follow the real occurrence time instead of arrival order.

## 5.5 Watermarks

A watermark is an estimate of event-time progress. It means the system expects most earlier events to have arrived under its chosen strategy. It is not proof that every earlier event arrived.

```text
Latest observed event time = 10:01:10
Assumed out-of-order bound = 5 seconds
Illustrative watermark ≈ 10:01:05
```

An event behind the watermark is late for event-time progress. Operators decide what to do with it. Options include dropping it, allowing lateness, or routing it separately.

Waiting longer can include more late data, but increases result latency and state needs. Moving faster lowers latency but can omit more late events. Neither choice guarantees accuracy by itself. An idle input partition can hold back progress, so idle-source detection may be needed.

## 5.6 Windows

An unbounded stream needs a defined scope for aggregation.

| Window | Behavior | Example |
| --- | --- | --- |
| Tumbling | Fixed, non-overlapping ranges | 10:00–10:01, then 10:01–10:02 |
| Sliding | Overlapping ranges | Calculate the last five minutes every minute |
| Session | Groups activity separated by an inactivity gap | Close a session after ten minutes with no activity |

Windows and watermarks work together in event-time processing. A session's event-time completion depends on time progress, not merely waiting on a wall clock.

## 5.7 State

State is information remembered from earlier records. For example, user A may have `click_count = 3` and user B `click_count = 1`.

**Keyed state** stores values per key after `keyBy()`. `ValueState` holds one value, `ListState` holds a list, and `MapState` holds key-value entries. Windows also keep state internally.

**State TTL** can expire old state under configured rules. Do not assume that every state item is removed immediately after a fixed period of inactivity. Update rules, visibility, and cleanup behavior matter.

## 5.8 Checkpoints

A checkpoint stores consistent processing state and source positions for recovery:

```text
TaskManager failure → Restore checkpoint → Restore Kafka offsets → Resume
```

A distributed snapshot coordinates state across operators. Checkpoint barriers mark the stream boundary included in a checkpoint. **Aligned checkpoints** wait for the required input barriers to line up. **Unaligned checkpoints** also record in-flight data and can reduce waiting under backpressure.

A checkpoint is execution state for resuming a streaming job. It is not a general-purpose backup of all external systems.

## 5.9 Savepoints

A savepoint is a state snapshot intentionally created for an operational change. Uses include upgrades, migration, rescaling, and planned stop/restart.

Checkpoints are primarily automatic recovery points. Savepoints are primarily operator-controlled change points. For example, a job might resume with parallelism increased from four to eight. State schema compatibility, migration rules, and operator identity still need checking.

## 5.10 Exactly-once processing

Exactly-once means one committed effect within the promised scope. Flink's internal state guarantee is not automatically an end-to-end guarantee.

The complete path includes:

```text
Source positions + Flink state + Sink consistency
```

If a sink repeats an external write on recovery, the full system may still produce duplicates. A supported transactional or idempotent sink can help close the boundary. At-least-once processing with an idempotent sink is another design, with its own assumptions.

## 5.11 Backpressure

Backpressure occurs when a slow downstream stage reduces the rate of upstream stages:

```text
Kafka → Filter → Aggregate → Slow Database
```

A slow database backs up aggregation, then filtering, then Kafka consumption. Consumer lag may rise. Causes include a slow sink, an expensive operator, network limits, skew, or an external database/API bottleneck.

Possible responses include more useful parallelism, better sink performance, batched writes, external-system scaling, and skew reduction. Backpressure is also normal flow control that protects the system from overload. More parallelism is not a universal fix, especially when an external service is already saturated.

## 5.12 Flink and Kafka

Kafka stores and delivers events. Flink performs stateful processing.

Kafka partition count limits useful concurrent source readers in the usual source model. If a topic has four partitions and source parallelism is eight, only four readers can actively own those partitions at one time. Downstream operators may still have different parallelism.

Flink checkpoints source offsets for recovery. Kafka or payload timestamps can supply event time. Kafka preserves order within a partition, not a total global order across partitions.

Kafka partitioning and Flink `keyBy` are different:

| Mechanism | Main purpose |
| --- | --- |
| Kafka partition | Log placement and parallel consumption |
| Flink `keyBy` | Redistribution for keyed state processing |

## 5.13 Flink and Iceberg

```text
Application → Kafka → Flink → Iceberg
```

A streaming append path keeps adding events to a lakehouse table. Flink tasks write files, and coordinated Iceberg commits make snapshots visible. Frequent writes and commits can produce small files, so compaction remains important.

One possible division of work is Flink for live processing and ingestion, with Spark for batch transforms, historical backfills, and compaction.

Current-state tables may need updates, deletes, or upserts. Do not assume that every Spark SQL MERGE pattern is available in a Flink sink. Check the connector's supported changelog, keys, and Iceberg format requirements.

## 5.14 Flink vs Spark

| Requirement | Common starting choice |
| --- | --- |
| Low latency, long-lived keyed state, event time, watermarks, sessions, complex live rules | Flink |
| Large batch ETL, large joins, backfills, Silver/Gold transforms, ML datasets | Spark |

Both support batch and streaming. This is a guide to common strengths, not an exclusive boundary. At a smaller scale, Spark Structured Streaming may be enough without adding Flink. Decide from latency, state, workload, and operational requirements.

## Qualifications for real use

Spark and Flink's historical starting points help explain their strengths; they are not full lists of current execution modes. A task slot is a logical resource unit, not simply one CPU core. Source and downstream parallelism can differ.

The five-second watermark example is an out-of-order assumption, not a universal formula. Progress across inputs is generally limited by the slowest active input. Check idleness and late-event policy together. Waiting longer costs state and does not guarantee accuracy. Event-time session completion is not just wall-clock waiting. [Flink watermarks](https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/event-time/generating_watermarks/)

State TTL is not immediate automatic deletion. The reviewed DataStream documentation describes processing-time TTL. Check update rules, expired-value visibility, and cleanup behavior. [Flink state](https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/fault-tolerance/state/)

Checkpoints do not back up all external systems. Unaligned checkpoints include in-flight data; they are not the same as simply skipping alignment in at-least-once mode. Source replay and restored state still need sink transaction or idempotency support. Savepoint restores also need compatible state schemas and operator identity. [Flink stateful processing](https://nightlies.apache.org/flink/flink-docs-stable/docs/concepts/stateful-stream-processing/)

More parallelism may worsen an overloaded external sink. The reviewed Iceberg Flink upsert documentation requires v2, primary-key or identifier fields, and partition source columns in equality fields. Do not assume Spark SQL MERGE behavior applies to a Flink sink. [Iceberg Flink writes](https://iceberg.apache.org/docs/latest/flink-writes/)

## Related reading

[Event semantics](event-architecture.md), [Spark](spark.md), [Iceberg](lakehouse-iceberg.md).

## LLM in practice: Stalled-watermark diagnosis

- Situation: A hypothetical streaming job receives data but emits window results late.
- Context to give the LLM: Give per-input timestamps and watermarks, idle settings, lag, backpressure, checkpoint duration, and sink latency.
- Expected output: Expect a distinction between idle input and slow processing, late-event impact, and verification steps.
- What the LLM can get wrong: The LLM may treat watermarks as wall clocks or checkpoint success as proof of sink correctness.
- How to validate: Inspect the minimum input watermark and late-event output, then compare state and sink results in a bounded reproduction.

Example prompt:

```text
Assess why event-time progress is stalled. Separate observed facts, idle-input hypotheses, slow-sink hypotheses, and missing evidence. Explain late-data risks. Propose a bounded test without dropping state or changing production retention.
```

LLM output is a working hypothesis. Check it against official docs and actual configuration, logs, and measurements. External documents reviewed: 2026-09-24. This does not mean an implementation version was tested.
