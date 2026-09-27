---
id: data-platform-architecture
status: studied
last_updated: 2026-09-27
last_reviewed: 2026-09-27
knowledge_ids:
  - DPE-17-01
  - DPE-17-02
  - DPE-17-03
  - DPE-17-04
  - DPE-17-05
  - DPE-19-01
  - DPE2-21-01
  - DPE2-21-02
  - DPE2-21-03
  - DPE2-21-04
  - DPE2-21-05
  - DPE2-21-06
  - DPE2-21-07
  - DPE2-21-08
  - DPE2-21-09
  - DPE2-21-10
  - DPE2-21-11
  - DPE2-21-12
  - DPE2-21-13
  - DPE2-21-14
  - DPE2-21-15
  - DPE2-21-16
  - DPE2-21-17
  - DPE2-21-18
  - DPE2-21-19
  - DPE2-21-20
  - DPE2-21-21
  - DPE2-21-22
  - DPE2-21-23
  - DPE2-21-24
  - DPE2-21-25
  - DPE2-21-26
  - DPE2-21-27
  - DPE2-21-28
  - DPE2-21-29
  - DPE2-22-01
  - DPE2-22-02
  - DPE2-22-03
  - DPE2-22-04
  - DPE2-22-05
  - DPE2-22-06
  - DPE2-22-07
  - DPE2-22-08
---


# Chapter 21 — Final End-to-End Data Platform Architecture

This page preserves Chapter 21 of the supplied complete source in its original order and form. Examples and diagrams describe studied concepts, not completed implementation, production recovery, or tests.

**Reading note:** The source core below keeps the original order and form. Read the section-specific corrections, conditions, and additions in the supplement after the source material; some original statements are simplified.

<!-- SOURCE CORE START -->

This is the final integration of the entire curriculum.

---

## 21.1 Core Architecture

```text
                    Applications
                         │
              ┌──────────┴──────────┐
              │                     │
         Event Data             Operational Data
              │                     │
            Kafka              PostgreSQL
              │                     │
              │                  Debezium
              │                     │
              └──────────┬──────────┘
                         │
                  Stream Processing
                   Flink / Spark
                         │
                         ▼
                  Bronze Iceberg
                         │
                         ▼
                       Spark
                         │
                         ▼
                  Silver Iceberg
                         │
                    dbt / Spark
                         │
                         ▼
                     Gold / Mart
                         │
               ┌─────────┼──────────┐
               │         │          │
             Trino       BI      AI Evaluation
```

---

## 21.2 Why Kafka Exists

Kafka is not the analytical database.

Role:

```text
Durable Event Transport
+
Replayable Event Log
+
Decoupling Producers/Consumers
```

Use when:

- multiple consumers need events,
- replay is valuable,
- asynchronous processing is required,
- event-driven architecture matters.

Do not add Kafka only because "data platforms use Kafka."

At low scale:

```text
Application
 ↓
Database / Direct Batch Export
```

may be enough.

---

## 21.3 Why Flink Exists

Role:

```text
Stateful Real-Time Stream Processing
```

Use when:

- low latency matters,
- Event Time is important,
- Watermarks are needed,
- large stateful streaming exists,
- complex windows/sessions are required.

If latency requirements are relaxed:

```text
Kafka
 ↓
Spark Structured Streaming
 ↓
Iceberg
```

may be simpler.

---

## 21.4 Why Bronze Exists

Bronze preserves data near its source form.

Purpose:

```text
Replay
Audit
Debug
Reprocessing
New transformation
Historical source
```

Without durable raw history, transformation bugs can be harder to recover from.

---

## 21.5 Why Iceberg Exists

Object Storage alone provides files.

Iceberg adds the table abstraction:

```text
Schema
Snapshot
Metadata
Partition evolution
Atomic commits
Time travel
Update/Delete/Merge support
```

It allows multiple engines to work with a shared analytical table.

---

## 21.6 Why Spark Exists

Spark is the heavy data processing engine.

Use for:

```text
large ETL
large joins
aggregation
backfill
compaction
ML datasets
Silver/Gold transformations
```

It is compute, not storage.

---

## 21.7 Why dbt Exists

dbt manages SQL transformation logic.

Use for:

```text
staging
intermediate
marts
tests
documentation
lineage
metric-oriented modeling
```

Spark and dbt are complementary.

```text
Spark
→ heavy processing

dbt
→ SQL transformation management
```

---

## 21.8 Why Gold / Mart Exists

Gold is where data becomes business-consumption ready.

Examples:

```text
fact_agent_execution
fact_llm_call
dim_model
dim_team
mart_daily_ai_usage
```

BI users should not need to understand raw event internals.

---

## 21.9 Why Trino / SQL Warehouse Exists

Analytics users need interactive SQL.

```text
Iceberg Gold
 ↓
Trino
 ↓
Dashboard / Analyst
```

In managed platforms:

```text
Databricks SQL Warehouse
Snowflake Virtual Warehouse
```

can fill this role.

---

## 21.10 Why Airflow / Lakeflow Exists

Data processing is more than individual jobs.

Need:

```text
schedule
dependencies
retries
backfills
failure handling
parameters
alerts
```

Use:

```text
Airflow
→ cross-platform

Lakeflow Jobs
→ Databricks-centric
```

---

## 21.11 Why Data Quality Exists

Question:

> **Can we trust the data?**

Checks include:

```text
Completeness
Uniqueness
Validity
Consistency
Freshness
Accuracy
Volume
```

Use quarantine for invalid data rather than silently dropping it.

---

## 21.12 Why Data Observability Exists

Question:

> **Is the data healthy right now, and where is it becoming unhealthy?**

Observe:

```text
Freshness
Volume
Schema
Distribution
Pipeline Health
Data Health
```

Important:

```text
Pipeline Healthy
≠
Data Healthy
```

---

## 21.13 Why Metadata / Catalog Exists

As data grows, users ask:

```text
What tables exist?
What does this column mean?
Who owns it?
Is it fresh?
Is it trustworthy?
```

Catalog unifies discovery and context.

---

## 21.14 Why Lineage Exists

Lineage answers:

```text
Where did this data come from?
Where does it go?
What breaks if I change it?
```

Useful for:

- root cause,
- impact analysis,
- governance,
- debugging,
- sensitive data tracking.

---

## 21.15 Why Governance Exists

Governance answers:

```text
Who owns it?
Who can access it?
Is it sensitive?
Should it be masked?
How long should it be retained?
Who accessed it?
```

Capabilities:

```text
Ownership
Classification
Retention
Deletion
Masking
Row/Column Access
Audit
Data Contracts
```

---

## 21.16 Why AI-Ready Data Exists

AI-ready data combines:

```text
Trust
Freshness
Versioning
Discovery
Governance
Provenance
```

AI should not consume unmanaged enterprise data blindly.

---

## 21.17 AI Evaluation Architecture

```text
Production Agent
      ↓
Trace / Telemetry
      ↓
Langfuse / MLflow
      ↓
Scores / Feedback / Judge
      ↓
Evaluation Dataset
      ↓
Experiments
      ↓
Regression Dataset
```

Long-term:

```text
Telemetry / Evaluation
      ↓
Iceberg
      ↓
Spark / dbt
      ↓
Enterprise AI Analytics
```

---

## 21.18 Version Chain for Reproducibility

A production/evaluation result should ideally be linkable to:

```text
Agent Version
Prompt Version
Model Version
Tool Version
Retrieval Config
Embedding Version
Dataset Version
Evaluator Version
Git Commit
```

Concept:

```text
result
 ↓
experiment_id / trace_id
 ↓
all relevant versions
```

This is the basis of reproducibility.

---

## 21.19 Failure Behavior

A good architecture explanation must include failures.

### Kafka Failure

Events remain durable according to configured replication/retention.

Consumers can resume/replay.

### Flink Failure

Restore:

```text
Checkpoint / Savepoint
+
Source Offset
```

### Spark Failure

Retry failed tasks/jobs.

Jobs must be idempotent.

### Iceberg Write Failure

Uncommitted files may become orphan files.

Atomic metadata commit protects table consistency.

### Airflow Failure

Resume from failed tasks rather than rebuilding everything.

### CDC Failure

Restart from offsets; snapshot/re-bootstrap when required.

### Data Quality Failure

Contain and quarantine before publishing downstream.

---

## 21.20 Consistency Model

Different parts of the platform have different guarantees.

Examples:

```text
Kafka
→ partition ordering
→ at-least-once / transactional features depending on usage

Flink
→ checkpointed state
→ end-to-end exactly-once depends on source + state + sink

Iceberg
→ snapshot-based consistent table reads
→ atomic commits

dbt / Batch
→ correctness depends heavily on idempotent transformations
```

Never say:

> "The entire platform is exactly-once"

without defining the boundary.

---

## 21.21 Backfill Strategy

Preferred hierarchy:

```text
1. Rebuild only affected partition/range
2. Use Bronze history
3. Kafka replay when within retention
4. Source re-extraction if necessary
```

Backfill requirements:

```text
parameterized time range
idempotency
resource limits
quality verification
lineage awareness
```

---

## 21.22 Scaling Model

### Kafka

Scale with:

```text
partitions
brokers
consumer parallelism
```

### Flink

Scale:

```text
operator parallelism
task managers
state backend/resources
```

### Spark

Scale:

```text
executors
tasks
partitions
cluster/serverless compute
```

### Iceberg

Scale through:

```text
object storage
metadata
file layout
partitioning
compaction
```

### Trino / SQL

Scale:

```text
workers / warehouse size
concurrency
query optimization
```

Scaling one component does not automatically remove bottlenecks in another.

---

## 21.23 Cost Model

Cost appears at different layers:

```text
Kafka
→ brokers/storage/network

Flink
→ always-on stream compute/state

Spark
→ batch compute

Iceberg
→ object storage + maintenance

Trino
→ query compute

BI
→ concurrency

AI
→ tokens/inference/search
```

Platform cost optimization is architecture-wide.

Examples:

```text
Reduce unnecessary raw retention
Reduce scans
Improve file layout
Use incremental transforms
Avoid duplicate materialization
Right-size compute
```

---

## 21.24 What to Remove at Smaller Scale

This was one of the original curriculum goals:

> **Explain what should be removed when scale is smaller.**

### Very small system

Possible:

```text
Application
 ↓
PostgreSQL
 ↓
dbt / SQL
 ↓
BI
```

No Kafka.

No Flink.

No Iceberg.

No Trino.

No separate metadata platform.

### Small analytics platform

```text
PostgreSQL / Files
 ↓
Object Storage
 ↓
Spark or managed SQL
 ↓
Warehouse / Lakehouse
 ↓
BI
```

Still possibly no Kafka/Flink.

### Medium event-driven platform

```text
Application
 ↓
Kafka
 ↓
Spark Structured Streaming
 ↓
Iceberg
 ↓
Spark/dbt
 ↓
Trino
```

Flink may still be unnecessary.

### Large real-time platform

```text
Kafka
 ↓
Flink
 ↓
Iceberg
 ↓
Spark
 ↓
Trino
```

Add:

```text
Catalog
Observability
Quality
Governance
```

when organizational/data complexity justifies them.

### Principle

> **Do not deploy technology because it exists in a reference architecture. Add it when its problem actually exists.**

---

## 21.25 What Changes if Databricks Is Adopted

Self-managed:

```text
Spark
Trino
Airflow
Catalog
Lineage
MLflow
Vector DB
```

may partially collapse into:

```text
Databricks Runtime
SQL Warehouse
Lakeflow
Unity Catalog
MLflow
AI Search
```

Possible remaining components:

```text
Kafka
Flink
External dbt
Cross-platform Airflow
Special-purpose stores
```

Architecture becomes simpler operationally.

Trade-off:

```text
less platform engineering
+
faster integration

vs

more vendor dependency
+
platform cost
```

---

## 21.26 What Changes if Snowflake Is Adopted

Possible consolidation:

```text
Warehouse
SQL compute
Transformation
Dynamic Tables
Governance
Iceberg access
AI services
```

may move into Snowflake.

Possible remaining components:

```text
Kafka
Flink
external Spark
Airflow
special-purpose operational systems
```

Snowflake is especially natural when the organization is SQL/analytics-centered.

---

## 21.27 Open Lakehouse Final Architecture

A fully open-oriented implementation could be:

```text
Applications
    ↓
Kafka
    ↓
Flink
    ↓
Iceberg on S3
    ↓
Spark
    ↓
dbt
    ↓
Trino
    ↓
BI
```

Surrounding components:

```text
Airflow
→ orchestration

OpenLineage
→ lineage event standard

DataHub / OpenMetadata
→ catalog

Soda / Great Expectations
→ quality

Prometheus / Grafana
→ system observability

Data observability layer
→ freshness / volume / drift

MLflow / Langfuse
→ AI lifecycle
```

Strength:

```text
flexibility
portability
control
```

Weakness:

```text
integration burden
operations
upgrades
security integration
on-call complexity
```

---

## 21.28 Managed Platform Final Architecture

Databricks-centered example:

```text
Sources
 ↓
Kafka / Lakeflow Connect
 ↓
Lakeflow Pipelines / Spark Streaming
 ↓
Delta / Iceberg
 ↓
Databricks Runtime / dbt
 ↓
Gold
 ↓
SQL Warehouse
 ↓
BI

Unity Catalog
→ governance + lineage

Lakeflow Jobs
→ orchestration

MLflow
→ ML/AI lifecycle

AI Search
→ retrieval

Model Serving
→ inference
```

Snowflake-centered example:

```text
Sources
 ↓
Snowpipe / Streaming / External ingestion
 ↓
Snowflake / Iceberg
 ↓
Dynamic Tables / SQL Transform
 ↓
Data Marts
 ↓
Virtual Warehouses
 ↓
BI

Horizon
→ governance

Cortex / Search / Agents
→ AI
```

---

## 21.29 Final Architecture Decision Checklist

Before adding any component ask:

### Kafka

```text
Do we need replayable event transport?
Do multiple consumers need the same event?
```

### Flink

```text
Do we really need stateful low-latency streaming?
```

### Iceberg

```text
Do we need open object-storage analytical tables,
snapshots, multi-engine access, and large history?
```

### Spark

```text
Do we have large-scale transformation/backfill workloads?
```

### dbt

```text
Do we need SQL transformation governance and reusable models?
```

### Trino

```text
Do we need interactive SQL over open lakehouse data?
```

### Airflow

```text
Do workflows span multiple systems and need orchestration?
```

### Catalog / Lineage

```text
Has the organization reached a point where users cannot
reliably find, understand, or assess impact on data?
```

### Data Quality / Observability

```text
Would wrong or stale data create meaningful business damage?
```

### Managed Platform

```text
Is reducing operations/integration work worth the vendor cost/dependency?
```

---

<!-- SOURCE CORE END -->

<!-- SOURCE FINAL START -->

# Final Mental Model

The entire study session can be compressed into this model:

```text
Sources
│
├─ Operational DB
│     ↓
│   CDC
│
└─ Events
      ↓
    Kafka
      ↓
Streaming Processing
      ↓
Raw / Bronze
      ↓
Lakehouse Table
      ↓
Batch Transformation
      ↓
Silver
      ↓
Modeling / dbt
      ↓
Gold / Marts
      ↓
SQL Serving
      ↓
BI / Analytics / AI
```

Cross-cutting planes:

```text
Orchestration
→ when and in what order

Quality
→ can we trust the data

Observability
→ is the data healthy now

Metadata / Catalog
→ what data exists

Lineage
→ where did it come from and where does it go

Governance
→ who can use it and how

AI Evaluation
→ how good are model/agent outputs

Versioning
→ what exact system produced this result

Cost
→ what resources are consumed

Recovery
→ how do we restore correct state after failure
```

Technology role map:

```text
PostgreSQL
→ operational state

Kafka
→ event log / transport

Debezium
→ database changes → event stream

Flink
→ stateful real-time processing

Spark
→ large-scale distributed processing

Parquet
→ columnar analytical file format

Iceberg
→ open lakehouse table format

dbt
→ SQL transformation management

Trino
→ interactive distributed SQL

Airflow / Lakeflow Jobs
→ orchestration

Data Quality tools
→ validation

Data Observability
→ freshness / volume / drift

OpenLineage
→ lineage event standard

Catalog
→ discovery / metadata

Governance
→ access / classification / audit

Langfuse / MLflow
→ AI telemetry / evaluation / experiments

Databricks / Snowflake
→ managed platforms that consolidate many of the above roles
```

---

# Final Engineering Principles

## Principle 1 — Start from the problem, not the tool

Bad:

```text
"We should use Kafka because modern platforms use Kafka."
```

Better:

```text
"We need replayable events consumed independently by five systems."
→ Kafka may be justified.
```

---

## Principle 2 — Keep roles clear

Avoid confusing:

```text
Storage
Table Format
Compute
Transformation
Query Engine
Orchestrator
Catalog
```

Example:

```text
S3
→ storage

Parquet
→ file format

Iceberg
→ table format

Spark
→ compute

dbt
→ transformation management

Trino
→ query engine

Airflow
→ orchestration
```

---

## Principle 3 — Design for reprocessing

Production pipelines will eventually need:

```text
retry
replay
backfill
rollback
```

Therefore:

- keep raw history when justified,
- make tasks idempotent,
- parameterize time ranges,
- version transformations,
- define source of truth.

---

## Principle 4 — Data correctness is separate from system health

```text
Job Success
≠
Correct Data
```

Observe both.

---

## Principle 5 — Version AI systems as systems

An AI output is produced by more than a model.

Version:

```text
Data
Prompt
Model
Agent
Tools
Retrieval
Evaluator
Code
```

---

## Principle 6 — Managed platforms trade control for integration

Open:

```text
more control
more portability
more platform work
```

Managed:

```text
less integration work
faster delivery
more vendor dependency
```

Neither is universally correct.

---

## Principle 7 — Remove components when they are not earning their operational cost

A mature platform is not one with the most technologies.

A mature platform is one where:

> **Every component exists because a real requirement justifies its complexity.**

---

<!-- SOURCE FINAL END -->

## Appendix A — Supplementary Clarifications

<!-- SOURCE APPENDIX START -->

## 17.1 Overall Technology Role Map

The roles connected throughout this study session are as follows.

```text
Applications
   ↓
Kafka
   ↓
Flink / Spark Streaming
   ↓
Iceberg Bronze
   ↓
Spark / dbt
   ↓
Silver / Gold
   ↓
Trino
   ↓
BI / Analyst / AI Evaluation
```

PostgreSQL Operational Data:

```text
PostgreSQL
   ↓
Debezium
   ↓
Kafka
```

Supporting systems:

```text
Airflow
→ Orchestration

Data Quality
→ Trust

Data Observability
→ Freshness / Volume / Drift

OpenLineage
→ Lineage Standard

Catalog
→ Discovery / Metadata

Governance
→ Access / Classification / Audit

Langfuse
→ AI Telemetry / Evaluation
```

---

## 17.2 Storage / Table / Compute / Query / Transformation Boundaries

```text
S3
→ Object Storage

Parquet
→ Columnar File Format

Iceberg
→ Table Format / Metadata / Snapshot

Spark
→ Large-scale Compute

Flink
→ Stateful Streaming Compute

Trino
→ Distributed SQL Query Engine

dbt
→ SQL Transformation Management

Airflow
→ Orchestration
```

These role boundaries are key to understanding the whole data platform.

---

## 17.3 Data Quality vs Data Observability

### Data Quality

Question:

> Does the data satisfy the rules we defined?

Examples:

- not null
- unique
- accepted values
- accuracy

### Data Observability

Question:

> How is data health changing during operations, and where did problems appear?

Examples:

- freshness
- volume
- schema
- distribution
- anomaly
- alert

Observability can continuously monitor quality rules.

---

## 17.4 Metadata / Catalog / Semantic Layer Differences

### Metadata

Information that describes data.

### Catalog

A system for searching and exploring metadata.

### Business Metadata

The business meaning of data.

### Semantic Layer

Define metric/dimension meanings and calculations in a form that queries can reuse.

### Lineage

Relationships that describe how data is created and transformed.

### Governance

Policies that define who should use data and how.

---

## 17.5 AI Observability vs General Data Platform

AI observability/evaluation tools such as Langfuse handle the following well.

- Trace
- LLM Call
- Tool Call
- Prompt
- Response
- Token
- Cost
- Latency
- Score
- Dataset
- Experiment

But they do not fully replace long-term:

- Enterprise Analytics
- Lakehouse Storage
- Cross-domain Join
- Data Governance
- Long-term History
- Unified Catalog

They do not replace all of these.

Suggested role separation:

```text
Langfuse
→ AI execution-level telemetry/evaluation

Data Platform
→ durable analytical data asset
```

---

<!-- SOURCE APPENDIX END -->

## Appendix: existing study notes and application conditions

The following preserves the prior explanations, caveats, links, Mermaid diagrams, and practical prompts. They are separate from the source body. No existing correct content was deleted or inserted into the middle of the source. Official-document review dates retain their prior values.

This page merges the source's supplementary explanations and final mental model. The architecture explains relationships. It is not a completed system or a required design for every organization. Linked topic pages provide evidence and qualifications for product behavior.

### Data paths

In this example, application events go to Kafka. PostgreSQL changes reach Kafka through Debezium. Flink or Spark Streaming writes Bronze data. Spark and dbt transformations build Silver and Gold, which Trino queries. dbt SQL runs on a connected execution engine.

```mermaid
flowchart TD
  Apps[Applications] --> Kafka[Kafka]
  Apps --> PG[PostgreSQL]
  PG --> CDC[Debezium]
  CDC --> Kafka
  Kafka --> Stream[Flink / Spark Streaming]
  Stream --> Bronze[Iceberg Bronze]
  Bronze --> Transform[Spark / dbt with an execution engine]
  Transform --> Silver[Iceberg Silver]
  Silver --> Marts[dbt / Spark]
  Marts --> Gold[Gold / Data Mart]
  Gold --> Trino[Trino]
  Trino --> Consumers[BI / Analyst / AI Evaluation]
```

The source's simpler diagram emphasizes Spark from Bronze to Silver and dbt from Silver to Gold/Data Mart. This diagram shows tool combinations within the same learning architecture. Connections require compatible connectors, catalogs, and execution engines. No end-to-end integration was tested for this material.

### Component boundaries

| Component | Main role | Details |
|---|---|---|
| Kafka | Event transport / durable log | [Kafka](event-architecture.md) |
| S3 | Object storage | [S3](foundations.md) |
| Parquet | Columnar analytical file format | [Parquet](foundations.md) |
| Iceberg | Table format, metadata, snapshots | [Iceberg](lakehouse-iceberg.md) |
| Spark | Large-scale compute and batch processing | [Spark](spark.md) |
| Flink | Stateful real-time processing | [Flink](flink.md) |
| Debezium | Capture database changes | [Debezium](cdc-debezium.md) |
| dbt | SQL transformation management | [dbt](dbt.md) |
| Trino | Distributed, interactive SQL queries | [Trino](trino.md) |
| Airflow | Workflow orchestration | [Airflow](orchestration.md) |
| OpenLineage | A standard for lineage events | [OpenLineage](lineage-metadata.md) |
| Catalog | Metadata search and discovery | [Catalog](lineage-metadata.md) |
| Governance | Policy, access, and audit | [Governance](governance.md) |
| Langfuse | AI telemetry, observability, and evaluation | [Langfuse](ai-ready-data.md) |


Storage, file format, table format, compute, query, transformation management, and orchestration have different roles. S3 holds objects; Parquet describes files; Iceberg manages table state; Spark/Flink process data; Trino runs SQL queries; dbt manages SQL models; Airflow manages task dependencies and execution order.

### Cross-cutting capabilities

| Capability | Question |
|---|---|
| Airflow | In what order and with which dependencies should tasks run? |
| Data quality | Does data satisfy the rules, and can we trust it? |
| Data observability | Are freshness, volume, distribution, or correctness abnormal now? |
| Metadata / catalog | What data exists, and what does it mean? |
| Lineage / OpenLineage | Where did it come from, and where does it go? |
| Governance | Who may use it, and under which policy? |
| Langfuse | What happened inside AI execution, and how good was it? |
| AI-ready data | Can AI reuse data under controlled conditions and restore experiment conditions? |

### Quality and observability

[Data quality](data-quality.md) checks rules such as not null, unique, accepted values, and accuracy. [Data observability](data-observability.md) studies changes and anomalies through freshness, volume, schema, distribution, anomaly detection, and alerts. Observability can monitor quality rules continuously. A successful pipeline does not prove correct data.

### Metadata, catalogs, and semantic layers

Metadata describes data. A catalog makes metadata searchable. Business metadata explains business meaning. A semantic layer defines reusable metric and dimension meanings and calculations for queries. Lineage describes creation and transformation relationships. Governance covers use policies and their enforcement. See [lineage and metadata](lineage-metadata.md), [analytical modeling](analytical-modeling.md), and [governance](governance.md).

### AI observability and the general data platform

Tools such as Langfuse handle traces, LLM/tool calls, prompts/responses, tokens/cost/latency, scores, datasets, and experiments. Do not assume they replace enterprise analytics, lakehouse storage, cross-domain joins, governance, long-term history, or a unified catalog. In this learning design, Langfuse handles execution-level telemetry and evaluation; the data platform holds durable analytical assets. This is not a final product adoption decision.

[AI-ready data](ai-ready-data.md) · [Online evaluation](ai-evaluation.md#161-online-evaluation-events) · [Study scope and next steps](curriculum.md)

### Why each component exists

Chapter 21 adds role and selection criteria to the existing architecture. These are design review examples, not an adoption ADR or a running system.

| Component | Problem and role | Omission or alternative |
|---|---|---|
| Kafka | Durable event transport, replay within retention, and producer/consumer separation. Useful when several consumers independently read events and process them asynchronously. It is not the analytical database. | A small system may only need application → database or direct batch export. |
| Flink | Low latency, event time, watermarks, large state, and complex windows or sessions in stateful streams. | With relaxed latency needs, Kafka → Spark Structured Streaming → Iceberg may be a simpler candidate. |
| Bronze | Keeps history close to source form for replay, audit, debugging, reprocessing, new transformations, and historical source access. | Define retention, access, and deletion rules together. Without raw history, transformation errors can be harder to recover from. |
| Iceberg | Adds schema, snapshots, metadata, partition evolution, atomic commits, time travel, and support for updates/deletes/merges above object-storage files. | Check engine, catalog, and format-version compatibility for multi-engine reads, writes, and row changes. |
| Spark | Large ETL, joins, aggregation, backfills, compaction, ML datasets, and Silver/Gold transformations. | It is compute, not storage. A smaller SQL runtime may be enough for small workloads. |
| dbt | Manages staging, intermediate models, marts, tests, documentation, lineage, and metric-oriented SQL models. | Complements Spark's heavy processing. A connected engine executes the SQL. |
| Gold / marts | Makes business data usable without exposing raw event internals. | Examples: `fact_agent_execution`, `fact_llm_call`, `dim_model`, `dim_team`, `mart_daily_ai_usage`. Define grain and business meaning first. |
| Trino / SQL warehouse | Interactive SQL, such as Iceberg Gold → Trino → dashboard/analyst. | Databricks SQL Warehouse or Snowflake Virtual Warehouse can fill this role in a managed platform. |
| Airflow / Lakeflow Jobs | Connects schedules, dependencies, retries, backfills, failure handling, parameters, and alerts. | Consider Airflow for cross-platform work and Lakeflow Jobs for Databricks-centered work. |

### Questions about quality, context, and policy

Quality checks completeness, uniqueness, validity, consistency, freshness, accuracy, and volume. Quarantine invalid data with reasons and a reprocessing path instead of silently dropping it. Observability covers freshness, volume, schema, distribution, pipeline health, and data health. **Healthy execution and correct data are different.**

A catalog helps answer which tables exist, what columns mean, who owns them, and whether they are fresh and trustworthy. Lineage explains origins, destinations, and change impact. It supports root-cause analysis, debugging, governance, and sensitive-data tracking.

Governance covers ownership, access, sensitivity, masking, retention and deletion, and access history. Its controls include ownership, classification, retention, deletion, masking, row/column access, audit, and data contracts. AI-ready data combines trust, freshness, versioning, discovery, governance, and provenance. It does not mean giving AI uncontrolled access to enterprise data.

### AI evaluation and long-term analytics

```mermaid
flowchart TD
  Agent[Production Agent] --> Trace[Trace / Telemetry]
  Trace --> Observe[Langfuse / MLflow]
  Observe --> Score[Scores / Human Feedback / Judge]
  Score --> Dataset[Evaluation Dataset]
  Dataset --> Experiment[Experiments]
  Experiment --> Regression[Regression Dataset]
  Observe --> Export[Validated export / ingestion]
  Score --> Export
  Export --> Iceberg[Iceberg history]
  Iceberg --> Transform[Spark / dbt with an engine]
  Transform --> Analytics[Enterprise AI Analytics]
```

The new source branches from Gold/marts to Trino, BI, and AI evaluation. The existing diagram routes consumers through Trino as one example; not every consumer must use Trino.

Arrows represent logical data movement. They do not promise automatic integration or equal product capabilities. See the [AI evaluation platform](ai-evaluation.md) for trace/evaluation IDs, normalization, versions, and Langfuse export/API paths. Separate long-term analytics from execution-level observability.

A result should link through `experiment_id` or `trace_id` to these versions:

```text
Agent version → Prompt version → Model version → Tool version
Retrieval config → Embedding version → Dataset version
Evaluator version → Git commit
```

The arrows show the order of a dependency list, not a required linear execution chain. Preserve the combination of data, prompt, model, agent, tools, retrieval, evaluator, and code. These links support reconstruction of conditions. They do not guarantee identical output when external data changes or models are nondeterministic.

### Failure behavior and consistency boundaries

| Failure | Recovery decision and boundary |
|---|---|
| Kafka | Check replication, acknowledgements, retention, and available replicas. Consumers can resume or replay retained logs. Do not assume lossless recovery from every failure. |
| Flink | Check the availability and consistency of checkpoints/savepoints and source offsets before restoring state. |
| Spark | Retry failed tasks/jobs. Check job and output idempotency and writes that already succeeded. |
| Iceberg write | An atomic metadata commit protects consistent table state. Uncommitted files may be orphaned. Do not remove them without checking active writers and retention. |
| Airflow | Verify successful upstream output remains valid, then resume failed tasks. Do not default to rebuilding everything. |
| CDC | Resume from retained offset/log state; consider snapshots or re-bootstrap when required. |
| Data quality | Contain the problem and quarantine data before downstream publication; check cause, impact, and reprocessing. |

| Boundary | Guarantee and checks |
|---|---|
| Kafka | Ordering within a partition. Delivery semantics such as at-least-once and transaction features depend on producer and consumer use. |
| Flink | Checkpointed state. End-to-end exactly-once depends on source + state + sink conditions. |
| Iceberg | Snapshot-based consistent table reads and atomic commits. This does not automatically provide a business transaction across independent tables. |
| dbt / batch | Correctness depends strongly on bounded input and idempotent transformation/write rules. |

Define input, state, output, side effects, and failure boundaries before saying the whole platform is exactly-once. Use [operations and recovery](production-operations.md) and official engine documentation to check recovery positions and duplicate handling.

### Backfill and recovery design

An example priority is **rebuild the affected partition/range → use Bronze history → replay Kafka within retention → re-extract the source if needed**. This is not a mandatory command sequence. Choose according to available source data and the failure type.

Parameterize time ranges and design idempotency, resource limits, quality checks, and lineage impact analysis together. Expect retries, replay, backfills, and rollbacks. Keep justified raw history, transformation versions, and a defined source of truth. Actual procedures also need an owner, SLO, data contract, recovery input, and publication criteria.

### Scaling units and cost

| Component | Scaling units | Main costs |
|---|---|---|
| Kafka | Partitions, brokers, consumer parallelism | Brokers, storage, network |
| Flink | Operator parallelism, TaskManagers, state backend/resources | Always-on stream compute and state |
| Spark | Executors, tasks, partitions, cluster/serverless compute | Batch compute |
| Iceberg | Object storage, metadata, file layout, partitioning, compaction | Object storage and maintenance |
| Trino / SQL | Workers/warehouse size, concurrency, query optimization | Query compute |
| BI / AI | Concurrent users/workloads, inference and search paths | BI concurrency; AI tokens, inference, search |

Scaling one component does not remove another component's bottleneck. Before reducing unnecessary raw retention, check replay, audit, and retention requirements. Compare reduced scans, better file layout, incremental transforms, fewer duplicate materializations, and right-sized compute across the architecture. The total cost in [platform comparison](platform-comparison.md) also includes integration, upgrades, and on-call work.

### What to remove at smaller scale

| Example scale and need | Possible architecture | Omission candidates |
|---|---|---|
| Very small system | Application → PostgreSQL → dbt/SQL → BI | Kafka, Flink, Iceberg, Trino, separate metadata platform |
| Small analytics platform | PostgreSQL/files → object storage → Spark or managed SQL → warehouse/lakehouse → BI | Kafka and Flink may still be unnecessary |
| Medium event-driven platform | Application → Kafka → Spark Structured Streaming → Iceberg → Spark/dbt → Trino | Flink if stateful low-latency processing is not required |
| Large real-time platform | Kafka → Flink → Iceberg → Spark → Trino | Add catalog, observability, quality, and governance tools as organizational and data complexity justify them |

Removing a separate tool does not remove necessary quality, access-policy, or recovery responsibilities. Start with a real problem, not the presence of a component in a reference architecture.

### Open Lakehouse and managed options

An open-oriented example is **Applications → Kafka → Flink → Iceberg on S3 → Spark → dbt → Trino → BI**. The dbt step executes SQL through a compatible engine.

| Supporting role | Example tools |
|---|---|
| Orchestration | Airflow |
| Lineage event standard | OpenLineage |
| Catalog | DataHub / OpenMetadata |
| Quality | Soda / Great Expectations |
| System observability | Prometheus / Grafana |
| Data observability | A freshness, volume, and drift layer |
| AI lifecycle | MLflow / Langfuse |

Strengths are flexibility, portability, and control. Costs include integration, operations, upgrades, security integration, and on-call complexity. An open format does not by itself make SQL, catalogs, IAM, and operations portable.

A Databricks-centered candidate is:

```text
Sources → Kafka / Lakeflow Connect
→ Lakeflow Pipelines / Spark Streaming
→ Delta / Iceberg
→ Databricks Runtime / dbt → Gold
→ SQL Warehouse → BI

Unity Catalog: governance / lineage
Lakeflow Jobs: orchestration
MLflow: ML / AI lifecycle
AI Search: retrieval
Model Serving: inference
```

Some self-managed Spark, Trino, Airflow, catalog, lineage, MLflow, and vector-store responsibilities may combine into Runtime, SQL Warehouse, Lakeflow, Unity Catalog, MLflow, and AI Search. Kafka, Flink, external dbt, cross-platform Airflow, and special-purpose stores may remain. A matching feature name does not prove full replacement. Compare less platform engineering and faster integration with vendor dependency and platform cost.

A Snowflake-centered candidate is:

```text
Sources → Snowpipe / Streaming / external ingestion
→ Snowflake / Iceberg
→ Dynamic Tables / SQL transformation → Data marts
→ Virtual Warehouses → BI

Horizon: governance
Cortex / Search / Agents: AI
```

This can combine warehouse, SQL compute, transformation, Dynamic Tables, governance, Iceberg access, and AI services. Kafka, Flink, external Spark, Airflow, and special-purpose operational systems may remain. Treat its fit for SQL/analytics-centered organizations as a learning heuristic, not proof that it always performs better or costs less.

Check cloud, region, edition, runtime, table mode, and connector conditions. [Databricks](databricks.md) and [Snowflake](snowflake.md) document capabilities, limits, and official sources. Managed diagrams also describe untested integration candidates.

### Adoption questions and engineering principles

| Candidate | Question to answer |
|---|---|
| Kafka | Do we need replayable event transport? Do several consumers independently read the same event? |
| Flink | Do we actually need stateful low-latency streaming? |
| Iceberg | Do we need open analytical tables on object storage, snapshots, multiple engines, and large history? |
| Spark | Do we have large transformation or backfill workloads? |
| dbt | Do we need reusable SQL models and transformation management? |
| Trino | Do we need interactive SQL over an open lakehouse? |
| Airflow | Do workflows span systems that require orchestration? |
| Catalog / lineage | Is it difficult to find data, understand it, or assess change impact? |
| Quality / observability | Would incorrect or stale data cause real business harm? |
| Managed platform | Is reduced integration and operations work worth the vendor cost and dependency? |

Seven principles guide the choice:

1. Start with the problem. “Five systems need independent consumption of replayable events” is a reason; “modern platforms use Kafka” is not.
2. Separate storage, file format, table format, compute, transformation, query, orchestration, and catalog roles.
3. Design raw history, idempotency, time ranges, transformation versions, and source data for retries, replay, backfills, and rollback.
4. Observe job success and data correctness separately.
5. Version AI data, prompts, models, agents, tools, retrieval, evaluators, and code as one system.
6. Compare open control, portability, and platform work with managed integration, faster delivery, and vendor dependency. Neither is always correct.
7. Consider removing components whose complexity is not justified by actual requirements. Tool count does not measure maturity.

Read the final path as **operational DB → CDC / events → Kafka → streaming → raw/Bronze → lakehouse table → batch → Silver → modeling/dbt → Gold/marts → SQL serving → BI/analytics/AI**. Overlay orchestration order, quality and trust, current data health, metadata discovery, lineage origins and impact, governance policies, AI output quality, versioned execution conditions, resource costs, and recovery of correct state.

## LLM in Practice

**Situation:** Adapt a reference architecture to the needs of a small team.

**Context to give the LLM:** Sanitized workloads, latency and recovery targets, consumer count, current components, staffing, retention, and access constraints.

**Example prompt**

=== "English"

    ```text {.prompt}
    [Context]
    Current architecture, workload, and consumers: [sanitized description]
    Latency, recovery, retention, access, and staffing constraints: [requirements]

    [Task]
    First compare current component roles with actual requirements.
    List candidates to retain, remove, or combine in a managed platform, with reasons.
    Separate observations, assumptions, and missing evidence; do not assume end-to-end guarantees.

    [Output]
    Return requirements, options, failure impact, and trade-offs for each component.
    State who still owns source data, reprocessing, quality, and access policies.

    [Checks]
    List checks against actual version support and settings.
    Propose a bounded comparison of results, latency, and recovery on the same input.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    현재 구조·workload·consumer: [비식별 설명]
    지연·복구·보존·권한·운영 인력 조건: [요구]

    [요청]
    먼저 현재 구조의 역할과 실제 요구를 대조해 주세요.
    유지·생략·managed 통합 후보를 근거와 함께 나눠 주세요.
    관찰·가정·누락 근거를 구분하고 end-to-end 보장을 단정하지 마세요.

    [출력]
    구성 요소별 요구·대안·실패 영향·trade-off 표를 주세요.
    원본·재처리·품질·접근 정책의 책임이 남는지 명시해 주세요.

    [검증]
    실제 버전의 지원 범위와 설정을 대조할 항목을 주세요.
    같은 입력의 결과·지연·복구를 비교하는 제한된 검증 계획을 주세요.
    ```

**Expected output:** A component decision table and validation plan that expose unowned responsibilities.

**What the LLM can get wrong:** It may treat managed feature names as full replacement, automatic access-policy propagation, or consistency guarantees. It may remove necessary controls at small scale.

**How to validate:** An owner compares workloads, support documentation, settings, and result, latency, and recovery evidence on the same input. This example does not authorize actual changes.

## Evidence and verification scope

[Databricks data engineering](https://docs.databricks.com/aws/en/data-engineering) and [Snowflake architecture](https://docs.snowflake.com/en/user-guide/intro-key-concepts) were checked on 2026-09-26. Linked canonical topics contain detailed product evidence. This page combines source architecture concepts and principles; connector integration, SQL, failure recovery, and performance were not executed.
