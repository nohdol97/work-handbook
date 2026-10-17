---
id: data-platform-event-architecture
status: studied
last_updated: 2026-10-18
last_reviewed: 2026-10-18
knowledge_ids:
  - DPE-02-01
  - DPE-02-02
  - DPE-02-03
  - DPE-02-04
  - DPE-02-05
  - DPE-02-06
---

# Chapter 2 — Event Data Architecture

An **event** records something that already happened, such as “an order was created.” Like a parcel label with a unique number and time, an event needs an identity and a clear time basis. Sections 2.1–2.6 show how to define its meaning and keep that meaning during replay and delivery to several destinations.

<!-- SOURCE CORE START -->

> Infrastructure details such as Kafka broker operations, ISR, and replica operations belong to a separate Platform session.  
> This chapter focuses on event semantics from a data engineering perspective.

## 2.1 Event Modeling

A stable ID and time on an order-created event help consumers identify repeat deliveries and analyze when it happened.

An event is a record of something that already happened, such as an order creation or button click, kept so it can be read later.

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

Producers and consumers must agree on field meaning as well as names. Even if `latency_ms` is an integer, a consumer can misread it unless the contract says the unit is milliseconds.

An event contract is a shared rule between the sender (producer) and reader (consumer) for field meaning, units, and required values.

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

Old events and current consumers coexist when fields are added or changed. Schema evolution manages these version differences and helps answer which consumer can read which version.

Event schemas gain versions as fields are added or formats change. Check compatibility when old and new events must be read together.

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

A Schema Registry keeps event schema versions in one place and checks the configured compatibility rules. It resembles checking a shared form before teams change its required fields. This check does not guarantee that field values have the right business meaning.

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

The owner in the example is fictional. Distinguish plain JSON from validation through JSON Schema. A registry cannot catch every semantic change, such as a unit change. Allowed changes depend on the format, field defaults, and compatibility mode. For full historical replay, check whether compatibility covers only the previous schema or all prior schemas through a transitive mode. [Confluent schema compatibility](https://docs.confluent.io/platform/current/schema-registry/fundamentals/schema-evolution.html)

---

## 2.4 Delivery Semantics

Delivery semantics describe how many times a message may arrive. A retried order event could create two stored orders, so define the guarantee boundary and how the consumer prevents duplicate effects.

### At-Most-Once

Deliver zero or one time within the stated boundary.

Delivery is not duplicated within that boundary, but an event can be lost.

```text
Zero or one time
```

### At-Least-Once

Deliver one or more times under the stated retention and recovery conditions.

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

The source's at-most-once phrase “fewer duplicates” is simplified. Within the guarantee's boundary, delivery happens at most once, so it does not duplicate delivery, but loss is possible. Exactly-once means one committed effect within a defined boundary. Distinguish Kafka transactions, processor state, and an external sink.

At-least-once guarantees rely on the system's retention and recovery assumptions. Deduplication needs an identity rule and a state-retention period. A longer replay needs separate verification. Kafka replay is limited to retained history. Check historical schema support and each serving or lakehouse path's lag, recovery, and result consistency.

---

## 2.5 Replay

Replay reads retained events again. It can rebuild a missing search index or apply new analysis logic, but first check retention and the risk of duplicate writes.

An event log such as Kafka can replay past events while they remain retained. This helps recover gaps or build a new consumer.

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

The same event can feed a serving store for quick reads and a lakehouse for long-term analysis. Their processing and recovery paths may differ, so do not assume their results are always in sync.

One event can be stored in several forms for different uses. This is materialization, useful when quick lookup and long-term analysis both need the event.

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

## Related reading

[Data foundations](foundations.md), [Flink](flink.md), [Iceberg](lakehouse-iceberg.md).

## Chapter takeaways

Define event identity, time, and field meaning first. Then check that delivery, replay, and each storage path preserve that contract.

## LLM in practice: Replay safety review

Expect duplicate and loss risks, compatibility checks, and testable results.
Replay a small range twice and compare final results by event ID and missing-event counts.

**Prompt:**

=== "English"

    ```text {.prompt}
    Rebuild a hypothetical search index from historical events.
    Assess the current replay design before redesigning it.
    State the delivery guarantee boundary.
    Separate facts, assumptions, duplicate risks, and missing evidence.
    Review the material; do not apply changes.
    ```

=== "한국어"

    ```text {.prompt}
    가상의 신규 search index를 과거 이벤트로 재구축한다.
    재설계 전에 현재 replay 설계를 검토해 줘.
    전달 보장 경계를 명시하고 사실·가정·중복 위험·누락 근거를 나눠 줘.
    자료를 검토하되 실제 변경은 실행하지 마.
    ```

**Key point:** The LLM may extend Kafka guarantees to an external sink without evidence.

[See six more practical prompts for this topic](../prompts/event-architecture.md)

LLM output is a working hypothesis. Check it against official docs and actual configuration, logs, and measurements. External documents reviewed: 2026-09-24. This does not mean an implementation version was tested.
