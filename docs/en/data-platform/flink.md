---
id: data-platform-flink
status: studied
last_updated: 2026-10-18
last_reviewed: 2026-10-18
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

# Chapter 5 — Flink

**Flink** processes events as they continue to arrive and keeps state between them. Picture a clerk updating a ledger whenever an order comes in. Sections 5.1–5.14 connect event time, late arrivals, state recovery, and writing results to external stores.

<!-- SOURCE CORE START -->

## 5.1 Why Flink

Flink handles an ongoing stream and can remember earlier results. Updating an order count for the last five minutes as new orders arrive shows why stateful streaming is useful.

Key point:

> **Spark expanded from batch-first processing to streaming, while Flink was designed streaming-first.**

Spark Structured Streaming can mainly be understood as micro-batch processing.

Flink centers on a continuous streaming model that processes events as they arrive.

Areas where Flink is strong:

- Event Time
- Watermark
- Window
- State
- Timer
- Stateful Streaming
- Low latency
- Complex real-time processing

Common examples:

- Real-time anomaly detection
- Session analysis
- Error rate over the last five minutes
- Real-time feature calculation

Key point:

> **Flink = Stateful Stream Processing Engine**

Spark and Flink's historical starting points help explain their strengths; they are not full lists of current execution modes. A task slot is a logical resource unit, not simply one CPU core. Source and downstream parallelism can differ.

---

## 5.2 Flink Architecture

A Flink job separates coordination from data processing. The JobManager coordinates work and TaskManagers run operators, though their execution model is not identical to Spark's.

### JobManager

The JobManager coordinates the whole job.

Conceptually similar to a Spark driver.

### TaskManager

TaskManagers run the operators' actual tasks.

Conceptually similar to a Spark executor.

### Operator

A processing step.

Example:

```text
Source → Filter → KeyBy → Window → Aggregate → Sink
```

### Parallelism

Run several instances of the same operator in parallel.

### Task Slot

A logical execution space inside a TaskManager.

---

## 5.3 DataStream Model

A DataStream reads events from a source, transforms them, and writes to a sink. To aggregate events by customer, `keyBy` redistributes them and supports state for each key.

Basic flow:

```text
Source
 ↓
Transformation
 ↓
Sink
```

### Source

Kafka, CDC, files, and other sources.

### Transformation

filter / map / keyBy / window / aggregate.

### Sink

Iceberg / Kafka / DB / Search Store.

### KeyBy

`keyBy` sends events with the same key to one logical processing unit so later events can be computed together.

```text
keyBy(user_id)
```

Keyed state can then be maintained.

Key point:

```text
Stream
 ↓
KeyBy
 ↓
Stateful Processing
```

---

## 5.4 Event Time

Use event time when a late order should count in the interval when it occurred, rather than when it arrived.

Main time concepts:

- Event Time
- Processing Time
- Ingestion Time

Event time is when an event happened, rather than when the platform received it.

Streaming events can arrive late or in a different order.

This is called **out-of-order arrival**.

Event-time processing supports analysis based on the time events actually happened.

Processing time is when the operator processes an event. Ingestion time is when it enters the system. Distinguish both from event time.

---

## 5.5 Watermark

A watermark signals how far event time has likely progressed. It does not rule out late events; it helps decide when to emit results and how long to keep state.

Watermark:

> **A progress boundary that assumes most events before this time have arrived**

Example:

```text
Latest event time = 10:01:10
Allowed delay = 5 seconds

Watermark ≈ 10:01:05
```

A watermark does not guarantee that every event has arrived.

An event older than the watermark that arrives later is a **late event**.

Late-event handling:

- Drop it
- Allowed Lateness
- Handle it separately

Trade-off:

```text
Slow watermark
→ Accuracy ↑
→ Result latency ↑

Fast watermark
→ latency ↓
→ Late events may be omitted
```

An idle partition can block watermark progress, so idle detection may be needed.

The five-second watermark example is an out-of-order assumption, not a universal formula. Progress across inputs is generally limited by the slowest active input. Check idleness and late-event policy together. Waiting longer costs state and does not guarantee accuracy. Event-time session completion is not just wall-clock waiting. [Flink watermarks](https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/event-time/generating_watermarks/)

---

## 5.6 Window

A window divides an endless stream into time ranges that can be aggregated. Use fixed ranges for orders per minute, or overlapping ranges for a rolling five-minute count updated each minute.

A stream keeps arriving, so a window defines a time range whose events can be aggregated.

### Tumbling Window

Fixed, non-overlapping ranges.

```text
10:00~10:01
10:01~10:02
```

### Sliding Window

Overlapping moving ranges.

```text
Calculate the last five minutes of data every minute
```

### Session Window

Close a session after a defined period without events.

Example:

```text
User activity
→ 10 minutes of inactivity
→ Session close
```

Watermarks and windows work together.

---

## 5.7 State

State is information kept from earlier events. A per-customer click count needs keyed state so the next click can update the previous value.

State:

> **Information Flink remembers from earlier processing**

Example:

```text
user A → click_count = 3
user B → click_count = 1
```

### Keyed State

State per key after `keyBy()`.

### ValueState

One value.

### ListState

A list of values.

### MapState

Key-value entries.

### State TTL

Define when state expires and how it can be cleaned up. Physical removal may happen later, depending on the cleanup mode.

Windows can also be understood as using state internally.

State TTL is not immediate automatic deletion. The reviewed DataStream documentation describes processing-time TTL. Check update rules, expired-value visibility, and cleanup behavior. [Flink state](https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/fault-tolerance/state/)

---

## 5.8 Checkpoint

A checkpoint records state and input progress so a job can resume after failure. It resembles saving both a ledger page and its bookmark, but it is not an automatic backup of the external sink.

Checkpoint:

> **A recovery point that periodically stores Flink's execution state and processing position**

When a failure occurs:

```text
TaskManager failure
 ↓
Restore checkpoint
 ↓
Restore Kafka offsets
 ↓
Resume processing
```

### Distributed Snapshot

Store the state of multiple TaskManagers/operators in a consistent checkpoint.

### Checkpoint Barrier

Barriers flow through the stream to coordinate the boundary included in the snapshot.

### Aligned Checkpoint

Align barriers from multiple inputs before proceeding.

### Unaligned Checkpoint

Include in-flight data to take snapshots quickly in situations such as backpressure.

A checkpoint does not back up external stores. It records **job state and input progress for restoring streaming work**.

Checkpoints do not back up all external systems. Unaligned checkpoints include in-flight data; they are not the same as simply skipping alignment in at-least-once mode. Source replay and restored state still need sink transaction or idempotency support. Savepoint restores also need compatible state schemas and operator identity. [Flink stateful processing](https://nightlies.apache.org/flink/flink-docs-stable/docs/concepts/stateful-stream-processing/)

---

## 5.9 Savepoint

A savepoint is a managed state record made before a planned change. It can support a job upgrade or rescaling, but the new code must be able to read the old state.

Savepoint:

> **A job-state snapshot deliberately created by an operator**

Main uses:

- Job Upgrade
- Migration
- Rescaling
- Planned Stop/Restart

Difference:

```text
Checkpoint
→ Automatic
→ Focused on failure recovery

Savepoint
→ Deliberate
→ Focused on operational changes
```

It can also support rescaling, such as changing parallelism from 4 to 8.

When changing the state structure, consider state migration and compatibility.

---

## 5.10 Exactly-Once Processing

Exactly-once means an event has one committed effect within a stated boundary. Even if Flink restores state correctly, an external store that accepts duplicate writes needs separate validation.

Exactly-once:

> **Each event's effect appears once in the final result**

Important:

> **Flink's internal exactly-once and end-to-end exactly-once are different.**

Required scope:

```text
Source Offset
+
Flink State
+
Sink Consistency
```

If the sink allows duplicate writes, the whole system is not exactly-once.

Alternative:

```text
At-Least-Once
+
Idempotent Sink
```

Exactly-once means one committed effect within the promised scope. A supported transactional or idempotent sink can help close the full boundary. At-least-once processing with an idempotent sink is another design with its own assumptions.


---

## 5.11 Backpressure

Backpressure happens when a slow downstream step holds up upstream processing. Like a blocked checkout line, it calls for finding whether the sink or an intermediate operator is the bottleneck.

Backpressure:

> **A slow downstream stage slows processing in upstream stages too**

Example:

```text
Kafka
 ↓
Filter
 ↓
Aggregate
 ↓
Slow Database

Slow database
→ Aggregation backs up
→ Filtering backs up
→ Kafka consumption slows
```

Kafka consumer lag may increase as a result.

Causes:

- Slow sink
- Heavy operator
- Network
- Skew
- External database/API bottleneck

Responses:

- Increase parallelism
- Improve the sink
- Batch Write
- Scale the external system
- Reduce skew

Backpressure is also natural flow control: a slow downstream step limits upstream input. Find the actual bottleneck before trying to remove it.

More parallelism may worsen an overloaded external sink. The reviewed Iceberg Flink upsert documentation requires v2, primary-key or identifier fields, and partition source columns in equality fields. Do not assume Spark SQL MERGE behavior applies to a Flink sink. [Iceberg Flink writes](https://iceberg.apache.org/docs/latest/flink-writes/)

---

## 5.12 Flink + Kafka

Kafka stores and delivers events; Flink computes over them. Kafka partitions affect source read parallelism, while Flink `keyBy` groups state, so they are not the same partitioning decision.

Roles:

```text
Kafka
→ Event storage/delivery

Flink
→ Stateful Stream Processing
```

### Kafka Partitions and Flink Parallelism

Kafka partition count affects the upper limit of parallel source consumption.

```text
Kafka Partitions = 4
Source Parallelism = 8
```

Even then, only four partitions can be actively read at the same time.

### Offset

Manage Kafka offsets with Flink checkpoints for recovery.

### Timestamp

Kafka/event timestamps can be used as event time.

### Ordering

Kafka preserves order inside one partition, but not one global order across several partitions.

### Kafka Partitioning vs Flink keyBy

Their purposes differ.

```text
Kafka Partition
→ Event storage and parallel consumption placement

Flink keyBy
→ Redistribution for state processing
```

---

## 5.13 Flink + Iceberg

Flink can keep writing results to Iceberg, but frequent commits can create many small files. Plan ongoing ingestion together with later compaction and large recomputations.

Purpose:

> **Continuously store streaming results in a lakehouse**

```text
Application
 ↓
Kafka
 ↓
Flink
 ↓
Iceberg
```

### Streaming Append

Keep appending new events.

### Commit Coordination

Flink tasks create files, and Iceberg commits publish snapshots.

### Small File Problem

Frequent commits can produce many small files.

### Compaction

Combine small files into larger files.

### Flink + Spark Role Split

```text
Flink
→ Real-time processing/ingestion

Spark
→ Batch Transform / Backfill / Compaction
```

### Update / Upsert

Current-state tables may need UPDATE / DELETE / MERGE.

---

## 5.14 Flink vs Spark

Flink and Spark both process data, but latency and state needs change which fits best. Compare complex low-latency event processing with large historical batch work before choosing.

### When Flink fits well

- Low latency
- Stateful Streaming
- Event Time
- Watermark
- Session
- Complex real-time rules

### When Spark fits well

- Large-scale batch processing
- ETL
- Large Join
- Backfill
- Silver/Gold creation
- ML Dataset

Both support batch and streaming, but their strengths differ.

At a small scale, Spark Structured Streaming may be enough without adding Flink.

Key point:

```text
Spark
→ Large-scale processing

Flink
→ Stateful real-time streaming
```

The batch/streaming comparison is not an exclusive feature boundary. Choose based on latency, state, workload, and operational requirements.

---

<!-- SOURCE CORE END -->

## Related reading

[Event semantics](event-architecture.md), [Spark](spark.md), [Iceberg](lakehouse-iceberg.md).

## Chapter takeaways

Treat time, state, recovery, and sink writes as one flow. Check late events and backpressure when defining the actual guarantee.

## LLM in practice: Stalled-watermark diagnosis

Expect a distinction between idle input and slow processing, late-event impact, and verification steps.
Inspect the minimum input watermark and late-event output, then compare state and sink results in a bounded reproduction.

**Prompt:**

=== "English"

    ```text {.prompt}
    A hypothetical streaming job receives data but emits window results late.
    Assess why event-time progress is stalled.
    Separate observed facts, idle-input hypotheses, slow-sink hypotheses, and missing evidence.
    Review the material; do not apply changes.
    ```

=== "한국어"

    ```text {.prompt}
    가상 streaming job에서 입력은 오는데 window 결과가 늦다.
    Event-time 진행이 막힌 이유를 검토해 줘.
    관찰 사실·idle input 가설·느린 sink 가설·누락 근거를 구분해 줘.
    자료를 검토하되 실제 변경은 실행하지 마.
    ```

**Key point:** The LLM may treat watermarks as wall clocks or checkpoint success as proof of sink correctness.

[See six more practical prompts for this topic](../prompts/flink.md)

LLM output is a working hypothesis. Check it against official docs and actual configuration, logs, and measurements. External documents reviewed: 2026-09-24. This does not mean an implementation version was tested.
