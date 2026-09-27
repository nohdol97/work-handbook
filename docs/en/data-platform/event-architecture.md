---
id: data-platform-event-architecture
status: studied
last_updated: 2026-09-27
last_reviewed: 2026-09-27
knowledge_ids:
  - DPE-02-01
  - DPE-02-02
  - DPE-02-03
  - DPE-02-04
  - DPE-02-05
  - DPE-02-06
---

# Chapter 2 — Event Data Architecture

Page type: Learn. This page records concepts and design examples from the supplied study material. `studied` means conceptual study, not hands-on implementation or production validation. Examples were not run. Kafka broker, ISR, and replica operations are outside this page. The focus is event meaning for data engineering.

The body translates the latest supplied source without merging its headings, paragraphs, lists, or examples. Corrections, conditions on simplified statements, and previous additions appear separately under **Qualifications for real use**.

**Reading note:** The source core below keeps the original order and form. Read the section-specific corrections, conditions, and additions in the supplement after the source material; some original statements are simplified.

<!-- SOURCE CORE START -->

> Infrastructure details such as Kafka broker operations, ISR, and replica operations belong to a separate Platform session.  
> This chapter focuses on event semantics from a data engineering perspective.

## 2.1 Event Modeling

An event is data that describes a fact that happened in the past.

Example:

```text
user clicked button
order created
agent executed
llm called
tool failed
```

Design good events to be immutable where possible.

Add a new event instead of editing a historical event.

---

### Main fields

#### Event ID

A unique identifier for the event.

```text
event_id
```

It matters for deduplication and tracing.

#### Event Time

The time when the action actually happened.

#### Ingestion Time

The time when the data platform received the event.

These times can differ.

```text
event_time     = 10:00:01
ingestion_time = 10:00:05
```

#### Producer Timestamp

The creation time recorded by the producer.

#### Trace / Session Identifier

Connect several events to one execution or user session.

Example:

```text
trace_id
session_id
execution_id
```

---

## 2.2 Event Contracts

An event contract is an agreement between producer and consumer about the meaning of an event.

Example:

```text
field: latency_ms
type: integer
unit: millisecond
required: true
owner: AI Platform Team
```

A contract can include:

- Required / Optional
- Data Type
- Unit
- Semantic Definition
- Ownership
- Version
- Compatibility Rule

Key point:

> **The same schema does not guarantee the same meaning.**

For example, `latency=5` could mean:

- 5ms
- 5 seconds

The contract must define which unit applies.

---

## 2.3 Schema Evolution

Event schemas change over time.

Example:

```text
v1:
event_id
user_id
event_time

v2:
event_id
user_id
event_time
device_type
```

---

### JSON vs Avro vs Protobuf

#### JSON

Advantages:
- Easy for people to read
- Flexible

Disadvantages:
- Schema enforcement can be weak
- Relatively large data size

#### Avro

Often used for schema-based serialization.

Common in Kafka environments with a schema registry.

#### Protobuf

Provides an explicit schema and a compact binary format.

---

### Schema Registry

Manages event schemas centrally.

Role:

```text
Manage schema versions
Check compatibility
Prevent breaking changes
```

---

### Backward Compatibility

Can a new consumer read old data?

### Forward Compatibility

Can an old consumer process new data?

### Breaking Change

A change that can break an existing consumer.

Example:

- Removing a required field
- An incompatible type change
- A semantic change

---

## 2.4 Delivery Semantics

### At-Most-Once

Deliver at most once.

Fewer duplicates, but loss is possible.

```text
Zero or one time
```

### At-Least-Once

Deliver at least once.

Helps prevent loss, but duplicates are possible.

```text
One or more times
```

### Exactly-Once

An important question:

> **From where to where is exactly-once guaranteed?**

The scope can differ across Kafka internals, stream-processor state, and the sink.

In data engineering, a common design uses:

```text
At-Least-Once
+
Idempotency
+
Deduplication
```

this combination so the final result reflects one effect.

---

### Idempotency

Running the same operation several times must leave the same final result.

```text
Process event A
Process event A again

Same final result
```

### Deduplication

Keep one event when the same event arrives several times.

Example:

```text
event_id
```

This can be used to find duplicates.

---

## 2.5 Replay

An important benefit of an event log such as Kafka is the ability to reread past events.

### Offset Replay

Start reading again from a particular offset.

```text
offset 100
→ 101
→ 102
...
```

### Downstream Rebuild

Example:

```text
Kafka
  ↓ replay
New Search Index
```

Or:

```text
Kafka
  ↓
New Lakehouse Table
```

These can be rebuilt in this way.

### Backfill from Kafka

Reprocess past events to fill missing data or apply new logic.

### Replay Safety

Because replay can produce duplicate events:

- Idempotency
- Deduplication
- Deterministic processing

these are important.

---

## 2.6 Event → Serving + Lakehouse Dual Path

One logical event can be materialized for several purposes.

```text
Application
   ↓
Kafka
   ├─→ Search Store
   ├─→ Operational Serving Store
   └─→ Lakehouse / Iceberg
```

For example, one user click event can support:

- A real-time dashboard
- Search or recommendations
- Long-term analytics
- AI Evaluation

these uses at the same time.

Key point:

> **An event stream is a delivery path. One event can be materialized into several stored forms for different purposes.**

---

<!-- SOURCE CORE END -->

## Qualifications for real use

The owner in the example is fictional. Distinguish plain JSON from validation through JSON Schema. A registry cannot catch every semantic change, such as a unit change. Allowed changes depend on the format, field defaults, and compatibility mode. For full historical replay, check whether compatibility covers only the previous schema or all prior schemas through a transitive mode. [Confluent schema compatibility](https://docs.confluent.io/platform/current/schema-registry/fundamentals/schema-evolution.html)

At-least-once guarantees rely on the system's retention and recovery assumptions. Deduplication needs an identity rule and a state-retention period. A longer replay needs separate verification. Kafka replay is limited to retained history. Check historical schema support and each serving or lakehouse path's lag, recovery, and result consistency.

### Section 2.4: the boundary of delivery guarantees

The source's at-most-once phrase “fewer duplicates” is simplified. Within the guarantee's boundary, delivery happens at most once, so it does not duplicate delivery, but loss is possible. Exactly-once means one committed effect within a defined boundary. Distinguish Kafka transactions, processor state, and an external sink.

### Existing supplementary flow diagram

```mermaid
flowchart TD
    A[Application] --> K[Kafka]
    K --> S[Search Store]
    K --> O[Operational Serving Store]
    K --> L[Lakehouse / Iceberg]
```

## Related reading

[Data foundations](foundations.md), [Flink](flink.md), [Iceberg](lakehouse-iceberg.md).

## LLM in practice: Replay safety review

- Situation: Rebuild a hypothetical search index from historical events.
- Context to give the LLM: Give schema versions, offset range, retention, event-ID rules, sink write behavior, and current consumer state.
- Expected output: Expect duplicate and loss risks, compatibility checks, and testable results.
- What the LLM can get wrong: The LLM may extend Kafka guarantees to an external sink without evidence.
- How to validate: Replay a small range twice and compare final results by event ID and missing-event counts.

Example prompt:

=== "English"

    ```text {.prompt}
    [Context]
    Schemas and scope: [schema versions, offset range, retention]
    Processing contract: [event-ID rules, sink writes, current consumer state]

    [Task]
    Assess the current replay design before redesigning it.
    State the delivery guarantee boundary.
    Separate facts, assumptions, duplicate risks, and missing evidence.

    [Output]
    List duplicate and loss risks, compatibility checks, and expected sink results.

    [Checks]
    Propose a bounded replay test and expected results by event ID.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    Schema와 범위: [schema 버전·offset 범위·보존 기간]
    처리 계약: [event ID 규칙·sink write·현재 consumer 상태]

    [요청]
    재설계 전에 현재 replay 설계를 검토해 줘.
    전달 보장 경계를 명시하고 사실·가정·중복 위험·누락 근거를 나눠 줘.

    [출력]
    중복·유실 위험과 호환성 점검, 예상 sink 결과를 작성해 줘.

    [검증]
    제한된 범위의 replay 테스트와 event ID별 기대 결과를 제안해 줘.
    ```

[See six more practical prompts for this topic](../prompts/event-architecture.md)

LLM output is a working hypothesis. Check it against official docs and actual configuration, logs, and measurements. External documents reviewed: 2026-09-24. This does not mean an implementation version was tested.
