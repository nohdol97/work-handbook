---
id: data-platform-databricks
status: studied
last_updated: 2026-09-27
last_reviewed: 2026-09-27
knowledge_ids:
  - DPE2-17-01
  - DPE2-17-02
  - DPE2-17-03
  - DPE2-17-04
  - DPE2-17-05
  - DPE2-17-06
  - DPE2-17-07
  - DPE2-17-08
  - DPE2-17-09
  - DPE2-17-10
  - DPE2-17-11
  - DPE2-17-12
---

# Chapter 17 — Databricks Deep Dive

Page type: Learn. This page records concept study from Chapter 17. `studied` does not mean hands-on implementation or production experience. Examples are hypothetical and were not run. Product scope was checked against official documentation on 2026-09-26. Availability depends on cloud, region, Runtime, access mode, and table features.

**Reading note:** The source core below keeps the original order and form. Read the section-specific corrections, conditions, and additions in the supplement after the source material; some original statements are simplified.

<!-- SOURCE CORE START -->

## 17.1 Lakehouse Architecture

Databricks can be understood as:

> **A managed Data + AI Platform that combines many components previously studied separately.**

Self-managed architecture might look like:

```text
Kafka
 ↓
Flink
 ↓
Iceberg
 ↓
Spark
 ↓
dbt
 ↓
Trino
 ↓
BI

Around:
Airflow
Catalog
Lineage
Governance
MLflow
```

Databricks integrates many of these responsibilities.

High-level structure:

```text
Sources
  ↓
Ingestion
  ↓
Lakehouse Storage
  ↓
Transformation / Streaming
  ↓
SQL / BI
  ↓
ML / AI

       ↕
  Unity Catalog
```

### Storage / Compute separation

```text
Storage
→ S3 / Cloud Object Storage

Compute
→ Databricks
```

### Table formats

Databricks historically centers on Delta Lake but now also supports Iceberg.

### Compute

Databricks Runtime is Spark-based and also integrates Photon.

### Medallion Architecture

```text
Bronze
→ raw

Silver
→ cleaned / validated / joined

Gold
→ business-ready / fact / dimension / mart
```

### Unified workload idea

Databricks combines:

```text
Data Engineering
+
SQL Warehouse
+
Governance
+
ML
+
AI
```

on the same data foundation.

---

## 17.2 Databricks Runtime and Photon

Databricks Runtime can be understood as:

> **Apache Spark packaged with Databricks optimizations, libraries, connectors, and platform integration.**

Self-managed Spark:

```text
Spark
+
JVM / Python
+
Libraries
+
Connectors
+
Cluster Config
+
Performance Tuning
```

Databricks:

```text
Databricks Runtime
=
Spark
+
Managed Environment
+
Optimization
+
Platform Integration
```

### Runtime versions

Runtime versions bundle:

- Spark version
- JDK
- libraries
- runtime features
- behavior changes

Production should manage runtime upgrades intentionally.

### Photon

Photon:

> **Databricks' native vectorized execution engine for supported SQL/DataFrame operations.**

Concept:

```text
SQL / DataFrame
     ↓
Catalyst Planning
     ↓
Photon
     ↓
Native Execution
```

Useful for:

- scan,
- filter,
- joins,
- aggregation,
- shuffle,
- Parquet operations.

Photon does not conceptually replace Spark.

```text
Spark
→ API / planner / distributed framework

Photon
→ optimized execution layer
```

---

## 17.3 SQL Warehouses

SQL Warehouse:

> **Managed SQL compute for interactive analytics, BI, and dashboard workloads.**

Architecture:

```text
Delta / Iceberg
     ↓
SQL Warehouse
     ↓
BI / Analyst / Dashboard
```

This is similar to the role Trino played in the open architecture.

Use cases:

- Ad-hoc SQL
- BI
- Dashboard
- Reporting
- Analyst exploration
- SQL transformation

Important:

```text
Storage
→ object storage / tables

SQL Warehouse
→ compute
```

### Serverless SQL

Serverless reduces cluster operations:

```text
Query Load ↑
→ Compute scale ↑

Query Load ↓
→ Compute scale ↓
```

### Concurrency

Designed for multiple concurrent SQL consumers.

### Governance

Queries pass through Unity Catalog governance.

### Semantic layer connection

Databricks Metric Views occupy the same conceptual area studied earlier:

```text
central metric definitions
+
dimensions
+
consistent business semantics
```

---

## 17.4 Unity Catalog

Unity Catalog:

> **Databricks' unified governance layer for Data and AI assets.**

Hierarchy:

```text
Metastore
   ↓
Catalog
   ↓
Schema
   ↓
Object
```

Three-part names:

```text
catalog.schema.table
```

Example:

```text
production.ai.fact_llm_call
```

### Object types

Unity Catalog can govern:

```text
Tables
Views
Volumes
Functions
Models
AI-related objects
```

### Volumes

Useful for governed files:

```text
PDF
Image
JSON
Documents
Artifacts
```

RAG example:

```text
PDF / Document
→ Volume

Chunk / Embedding
→ Table
```

### Managed vs External

Managed Table:

```text
UC manages
→ metadata
→ storage location
→ lifecycle
→ optimization
```

External Table:

```text
Data lives at user-managed object path
UC manages
→ metadata
→ access/governance
```

### Access

Objects are securable.

Privileges may apply at:

```text
Catalog
Schema
Table
View
Volume
Model
...
```

Hierarchy enables inherited policy.

---

## 17.5 Lakeflow Jobs

Lakeflow Jobs:

> **Databricks workflow orchestration.**

Airflow mapping:

```text
Airflow DAG
≈ Lakeflow Job
```

Inside a job:

```text
Task
→ dependency
→ schedule / trigger
```

Task types may include:

- Notebook
- SQL
- dbt
- Pipeline
- Python/Spark
- ML

Triggers may include:

```text
time schedule
file arrival
table update
continuous execution
```

### Airflow vs Lakeflow Jobs

```text
Lakeflow Jobs
→ Databricks-centered orchestration

Airflow
→ broader cross-platform orchestration
```

If most workloads live inside Databricks, a separate Airflow may not be necessary.

If workflows span:

```text
Databricks
AWS Lambda
Kubernetes
Snowflake
SaaS APIs
internal systems
```

a general orchestrator can still be useful.

---

## 17.6 Lakeflow Pipelines

Lakeflow high-level view:

```text
Lakeflow
├─ Connect
│   → ingestion
├─ Pipelines
│   → transformation
└─ Jobs
    → orchestration
```

### Jobs vs Pipelines

Jobs:

> **Define task execution order.**

Pipelines:

> **Define dataset transformation relationships declaratively.**

Procedural style:

```text
1. Run Bronze notebook
2. Run Silver notebook
3. Run Gold SQL
```

Declarative style:

```text
bronze_events
      ↓
silver_events
      ↓
gold_metrics
```

The engine manages more of:

- dependencies,
- incremental updates,
- execution order,
- parallelization,
- monitoring.

### Batch + Streaming

Pipelines can process both.

They are conceptually connected to Spark Structured Streaming.

### Important objects

```text
Pipeline
Flow
Streaming Table
Materialized View
```

### DLT naming

Older:

```text
Delta Live Tables (DLT)
```

Current direction:

```text
Lakeflow Pipelines
```

---

## 17.7 Delta / Iceberg Interoperability

Delta and Iceberg solve similar problems:

```text
Object Storage
+
Parquet
+
Table Metadata
```

with:

- transactions,
- snapshots,
- schema evolution,
- time travel,
- table management.

### Databricks default

Delta is still the natural/native path for many Databricks-managed workloads.

### Managed Iceberg

Databricks also supports Unity Catalog managed Iceberg tables.

Concept:

```text
Unity Catalog
   ↓
Managed Iceberg
   ↓
Parquet
```

### UniForm

Core idea:

> **Keep the same Parquet data while exposing compatible Iceberg metadata so Iceberg clients can read the table.**

Conceptual diagram:

```text
           Parquet Files
           /          \
Delta Metadata    Iceberg Metadata
      ↓                 ↓
Databricks       External Iceberg clients
```

This reduces the need to duplicate table data.

### Iceberg REST Catalog

Unity Catalog can participate in Iceberg REST-based interoperability.

External engines such as:

```text
Spark
Flink
Trino
```

can interact through Iceberg-compatible interfaces.

### Important distinction

```text
Delta ≠ Iceberg
```

Interoperability layers do not mean both formats are identical.

### Simple selection intuition

```text
Databricks-centric ecosystem
→ Delta is natural

Multi-engine / open ecosystem
→ Iceberg is natural
```

Modern Databricks supports both far more than before.

---

## 17.8 Lineage / Governance

Unity Catalog combines:

```text
Lineage
Classification
Access Control
Masking
Row Filters
Audit
```

### Lineage

Example:

```text
bronze.llm_calls
      ↓
Spark
      ↓
silver.llm_calls
      ↓
SQL/dbt
      ↓
gold.ai_usage
      ↓
Dashboard
```

Column-level lineage supports impact analysis.

### Classification

Example:

```text
email
→ PII

employee_id
→ Sensitive Internal
```

### Tags

Classification/tagging can drive policies.

```text
PII Tag
   ↓
Masking Policy
```

### RBAC / ABAC

RBAC:

```text
role
→ privilege
```

ABAC:

```text
attribute/tag
→ policy
```

Example:

```text
Tag = PII

General Analyst
→ masked

Security Admin
→ clear text
```

### External lineage

Enterprise lineage may include assets outside Databricks.

### AI governance

Governance scope increasingly includes:

- models,
- model services,
- agents,
- AI services.

---

## 17.9 MLflow

MLflow now spans:

```text
Traditional ML
+
GenAI / Agents
```

### Traditional ML

Experiment Tracking:

```text
Run
├─ Parameters
├─ Metrics
├─ Code Version
└─ Artifacts
```

### Model Registry

Tracks:

```text
model_name
version
alias
tags
lineage
```

In Databricks this integrates with Unity Catalog.

### GenAI Tracing

Concept:

```text
User
 ↓
Agent
 ↓
Retriever
 ↓
LLM
 ↓
Tool
 ↓
Response
```

Trace can capture:

```text
input
output
latency
tokens
cost
tool calls
retrieval
```

### GenAI Evaluation

Supports:

```text
evaluation datasets
scorers
LLM judges
custom rules
```

### Prompt Registry

Prompts can be versioned and evaluated.

### Human Feedback

Review and labeling can be connected to traces/evaluation.

### Langfuse overlap

There is now significant overlap:

| Capability | Langfuse | MLflow 3 |
|---|---|---|
| LLM tracing | Yes | Yes |
| Tool/retrieval tracing | Yes | Yes |
| Prompt management | Yes | Yes |
| Evaluation | Yes | Yes |
| LLM judge | Yes | Yes |
| Human feedback | Yes | Yes |
| Experiments | Yes | Yes |
| Traditional ML | Limited focus | Strong |
| Model Registry | Not core | Core |
| Unity Catalog Integration | External | Native |

If Databricks becomes the main enterprise platform, MLflow may cover many functions that would otherwise require Langfuse.

---

## 17.10 AI / Vector Capabilities

Databricks connects Lakehouse data to AI application capabilities.

High-level:

```text
Lakehouse
   ↓
AI Search
   ↓
Model / Agent
   ↓
Serving
   ↓
Application
```

### AI Search

Role:

> **Retrieve relevant enterprise data for RAG/search.**

Typical flow:

```text
Documents
 ↓
Chunking
 ↓
Embeddings
 ↓
AI Search
 ↓
Retriever
 ↓
LLM
```

### Search index sync

Source tables can be incrementally synchronized into search indexes.

### Model Serving

Models can be exposed as managed endpoints.

Possible models:

```text
custom model
foundation model
external model provider
```

### Agents

Agents can combine:

```text
LLM
AI Search
SQL Tool
MCP
External API
```

### Governance

Unity Catalog permissions should apply before unauthorized data reaches retrieval.

Important principle:

> **Do not retrieve unauthorized documents and hide them later. Prevent unauthorized retrieval in the first place.**

### Integrated AI stack

```text
Unity Catalog
→ governance

MLflow
→ trace/evaluation

Lakehouse
→ data

AI Search
→ retrieval

Model Serving
→ inference
```

---

## 17.11 Databricks Cost Model

Main idea:

> **Compute is the largest controllable cost dimension, with storage/network and AI services added around it.**

### DBU

DBU:

> Databricks normalized billing unit for compute/service usage.

Do not interpret it as a fixed CPU count.

### Classic Compute

Conceptually:

```text
Databricks DBU
+
Cloud VM
+
Storage / Network
```

### Serverless

Infrastructure is managed by Databricks.

Operational burden decreases.

External storage/network costs can still exist.

### Cost sources

```text
Spark Jobs
SQL Warehouse
Lakeflow Pipelines
Serverless
Model Serving
AI Search
Storage
Network
Background optimization
```

### Performance optimization = cost optimization

```text
Partition Pruning
→ Scan ↓
→ Runtime ↓
→ Cost ↓
```

```text
Compaction
→ Query efficiency ↑
→ Cost ↓
```

```text
Incremental Processing
→ Full recompute avoided
→ Cost ↓
```

### Track by tags

Useful dimensions:

```text
team
project
environment
job
workspace
```

### Serverless is not automatically cheaper

It can improve:

- operational simplicity,
- startup time,
- scaling,
- idle reduction.

Actual cost still depends on workload.

---

## 17.12 Which Self-Managed Components Databricks Can Replace

Self-managed architecture:

```text
S3
+
Iceberg
+
Spark
+
Trino
+
Airflow
+
dbt
+
Catalog
+
OpenLineage
+
MLflow
+
Vector DB
+
AI Observability
```

Databricks can consolidate many responsibilities.

### High replacement potential

```text
Spark Cluster
→ Databricks Runtime / Serverless

Trino-like BI serving
→ SQL Warehouse

Custom Spark pipeline framework
→ Lakeflow Pipelines

Catalog / Governance
→ Unity Catalog

OpenLineage / Marquez-like internal lineage
→ Unity Catalog Lineage

Self-hosted MLflow
→ Managed MLflow

Vector DB for Databricks-centric RAG
→ AI Search
```

### Partial replacement

```text
Airflow
→ Lakeflow Jobs can replace it for Databricks-centric workflows

Langfuse
→ MLflow 3 overlaps substantially

dbt
→ Databricks SQL / Pipelines overlap, but dbt remains valid
```

### Usually not a full replacement

```text
Kafka
→ separate durable event log / event bus role

Flink
→ may remain for low-latency complex stateful streaming

Cross-platform orchestrator
→ may remain if the platform spans many systems
```

### Databricks' real value

Not simply:

> "Spark is faster."

But:

> **Reduce the number of platform components that must be installed, upgraded, integrated, secured, monitored, and operated independently.**

Trade-off:

```text
Operational Complexity ↓
Integration Speed ↑

but

Platform Dependency ↑
Vendor Lock-in ↑ possible
Cost ↑ possible
```

---

<!-- SOURCE CORE END -->

## Operational review and official documentation notes

The following notes are separate from the source. They retain the support conditions and cautions reviewed on 2026-09-26. This edit did not test new versions or recheck official documentation.

### Lakehouse Architecture

Databricks combines data engineering, SQL, governance, ML, and AI on a shared data foundation. A self-managed stack might use `Kafka → Flink → Iceberg → Spark → dbt → Trino → BI`, with Airflow, Catalog, Lineage, Governance, and MLflow around it. Databricks combines several of these responsibilities. It does not remove every role.

```mermaid
flowchart TD
    S[Sources] --> I[Ingestion]
    I --> L[Object storage and lakehouse tables]
    L --> T[Transformation and streaming]
    T --> Q[SQL and BI]
    T --> A[ML and AI]
    U[Unity Catalog] -.-> L
    U -.-> T
    U -.-> Q
    U -.-> A
```

Storage uses cloud object storage such as S3. Databricks supplies compute. The platform grew around Delta and also supports Iceberg. Runtime is Spark-based and can use Photon. Medallion layers separate **Bronze raw data → Silver cleaned, validated, joined data → Gold business facts, dimensions, and marts**. Turning on a tool does not guarantee layer quality. See [Lakehouse and Iceberg](lakehouse-iceberg.md).

### Databricks Runtime and Photon

Runtime bundles Spark with an execution environment, optimizations, libraries, connectors, and platform integration. It takes over some work needed to manage JVM/Python, libraries, connectors, cluster settings, and tuning in a self-managed Spark system. Runtime versions include Spark, JDK, libraries, and behavior changes. Plan production upgrades and test compatibility.

A useful model is `SQL/DataFrame → Catalyst planning → Photon for supported operations`. Photon is a native vectorized execution layer for supported scans, filters, joins, aggregations, shuffles, and Parquet operations. It does not replace Spark's APIs, planning, and distributed framework. Inspect execution plans to see which operations use it. [Photon scope](https://docs.databricks.com/aws/en/compute/photon).

### SQL Warehouses

A SQL Warehouse supplies compute for ad-hoc SQL, BI, dashboards, reporting, analyst exploration, and SQL transformations. It is not table storage. The flow is `Delta/Iceberg tables → SQL Warehouse → analyst/BI`. Compare its role with [Trino](trino.md) in an open stack.

Serverless SQL reduces cluster operations and adjusts compute to load. Measure concurrency and queue time when choosing capacity and settings. Queries connect to Unity Catalog governance. Metric Views cover central metric definitions, dimensions, and shared business semantics. Check feature requirements in [Databricks SQL](https://docs.databricks.com/aws/en/sql/) and [Metric Views](https://docs.databricks.com/aws/en/metric-views/).

### Unity Catalog

Unity Catalog is a governance layer for data and AI assets. Its hierarchy is `Metastore → Catalog → Schema → Object`. Table names use `catalog.schema.table`. The hypothetical name `production.ai.fact_llm_call` does not identify a real organization.

| Object or type | Responsibility and example |
|---|---|
| Tables, Views, Functions, Models | Tabular data, query definitions, functions, and models |
| Volumes | Files such as PDFs, images, JSON, documents, and artifacts |
| RAG layout example | Source PDFs in a Volume; chunks and embeddings in a Table |
| Managed Table | UC manages metadata, storage location, lifecycle, and supported optimizations |
| External Table | Data uses a user-managed object path; UC manages registered metadata and access |

Catalogs, schemas, tables, views, volumes, and models are securable objects. Some privileges are inherited through the hierarchy. Do not assume every privilege or policy has the same inheritance rules. **UC policies alone do not govern direct external reads and writes to object paths.** Check cloud IAM and external engine access too. [Unity Catalog](https://docs.databricks.com/aws/en/data-governance/unity-catalog/), [external access boundaries](https://docs.databricks.com/aws/en/external-access).

### Lakeflow Jobs

A Lakeflow Job defines tasks, dependencies, and schedules or triggers, much like an Airflow DAG. Tasks can include notebooks, SQL, dbt, pipelines, Python/Spark, and ML work. Time schedules, file arrival, table updates, and continuous execution have task-specific requirements. [Lakeflow Jobs](https://docs.databricks.com/aws/en/jobs/).

A separate Airflow system may add less value when most work runs inside Databricks. A [general orchestrator](orchestration.md) may still help coordinate Databricks, AWS Lambda, Kubernetes, Snowflake, SaaS APIs, and internal systems. Similar names do not imply identical DAG, retry, or backfill behavior.

### Lakeflow Pipelines

Separate **Connect for ingestion / Pipelines for transformation / Jobs for execution order**. The source's Lakeflow Pipelines and older Delta Live Tables (DLT) names connect to the current Spark Declarative Pipelines documentation. Some documentation and environments also use Lakeflow Spark Declarative Pipelines. [Current Pipelines documentation](https://docs.databricks.com/aws/en/ldp/), [Lakeflow Connect](https://docs.databricks.com/aws/en/ingestion/lakeflow-connect).

An imperative workflow says “run the Bronze notebook, run the Silver notebook, then run Gold SQL.” A declarative pipeline defines `bronze_events → silver_events → gold_metrics`. The engine manages more dependency, incremental update, execution order, parallelization, and monitoring work. Key objects are Pipeline, Flow, Streaming Table, and Materialized View. Pipelines handle batch and streaming and connect to Spark Structured Streaming. A declarative query is not automatically incremental in every case. It also needs suitable settings to meet freshness goals.

### Delta / Iceberg interoperability

Delta and Iceberg add table metadata to object storage and Parquet. Both address transactions, snapshots, schema evolution, time travel, and table management. **Delta and Iceberg are different formats.** Delta can be a natural choice for Databricks-centered work. Iceberg can suit multiple engines. Test the actual reader and writer combination.

| Approach | Meaning | Boundary to check |
|---|---|---|
| UC managed Iceberg | UC manages Iceberg tables and Parquet | Features, table version, external writers |
| Delta UniForm / Iceberg reads | One set of Parquet files with Delta and compatible Iceberg metadata | Delta remains the source format; read compatibility does not allow arbitrary Iceberg writes |
| Iceberg REST Catalog | Catalog interface for engines such as Spark, Flink, and Trino | Client, authentication, privileges, reads/writes, and table features |

UniForm generates Iceberg metadata asynchronously. Do not assume a Delta commit is immediately visible as the same Iceberg version. Check metadata generation status and external read freshness. Table format, storage, catalog, and governance integration are separate dimensions. [Iceberg reads](https://docs.databricks.com/aws/en/delta/iceberg-reads), [external system access](https://docs.databricks.com/aws/en/external-access), [Iceberg REST specification](https://iceberg.apache.org/rest-catalog-spec/).

### Lineage and Governance

An example lineage is `bronze.llm_calls → Spark → silver.llm_calls → SQL/dbt → gold.ai_usage → Dashboard`. Column lineage helps assess change impact. Example classifications are `email → PII` and `employee_id → Sensitive Internal`. No real values are collected or published here.

UC connects lineage, classification, access control, masking, row filters, and audit. RBAC connects roles to privileges. ABAC connects attributes or tags to policies. For example, a policy can mask PII-tagged data for general analysts and allow clear text only for a separately approved security role. **Adding a tag alone does not create masking.** Configure policies and test both allowed and denied access for each role.

Governance can extend to external lineage, models, model services, agents, and AI services. Check the collection and enforcement boundary of each integration. [UC governance scope](https://docs.databricks.com/aws/en/data-governance/unity-catalog/). See [Governance](governance.md) and [Lineage and Metadata](lineage-metadata.md).

### MLflow

MLflow covers traditional ML and GenAI/agents. An experiment Run links parameters, metrics, code versions, and artifacts. Model Registry tracks model names, versions, aliases, tags, and lineage. It integrates with UC on Databricks.

A `User → Agent → Retriever → LLM → Tool → Response` trace can link inputs, outputs, latency, tokens, cost, tool calls, and retrieval. Evaluation datasets, scorers, LLM judges, custom rules, Prompt Registry versions, and human feedback or review can support evaluation. Verify captured fields, cost availability, and sensitive-data handling in the actual instrumentation. [MLflow on Databricks](https://docs.databricks.com/aws/en/mlflow/).

The source compares MLflow 3 and Langfuse because their **capability areas overlap** in tracing, tool/retrieval tracking, prompt management, evaluation, judges, human feedback, and experiments. This does not promise equal behavior, UI, retention, or operations. MLflow has a strong traditional ML and Model Registry focus and native Databricks UC integration. Langfuse focuses on LLM work; a traditional ML registry is not its main purpose. The source describes its UC connection as an external integration. A Databricks-centered team can consider reducing duplicate systems after checking required features.

### AI / Vector capabilities

The integrated flow is `Lakehouse → AI Search → Model/Agent → Serving → Application`. A RAG flow is `documents → chunking → embeddings → AI Search → retriever → LLM`. AI Search is the current name for Vector Search. Distinguish indexes that sync supported source tables from indexes updated directly. Not every index updates automatically. Supported sync indexes can apply source changes incrementally, but some endpoint types need partial index rebuilds. [AI Search](https://docs.databricks.com/aws/en/ai-search/ai-search).

Model Serving can expose custom models, foundation models, and external providers through managed endpoints. Agents can combine an LLM, AI Search, SQL tools, MCP, and external APIs. UC covers governance, MLflow covers traces and evaluation, Lakehouse holds data, AI Search retrieves it, and Serving runs inference.

**Retrieving unauthorized documents and hiding them later is unsafe.** Restrict access before retrieval. The checked AI Search documentation says row and column permissions are unsupported and application ACLs can use the filter API. Do not assume UC integration automatically carries source row policies to an index. Build filters from trusted server-side user and permission data. Test bypass attempts, unauthorized documents, and permission changes. [AI Search limitations](https://docs.databricks.com/aws/en/ai-search/ai-search#limitations).

### Databricks cost model

A DBU is a normalized compute/service billing unit, not a fixed CPU count. Classic compute is conceptually **DBU + cloud VM + storage/network**. Serverless moves infrastructure operations to the vendor but can leave external storage/network charges. Include Spark Jobs, SQL Warehouses, Pipelines, Serverless, Model Serving, AI Search, storage, network, and background optimization.

Pruning can reduce scans. Compaction can improve reads. Incremental processing can avoid full recomputation. Check billing units, always-on resources, and maintenance cost before equating shorter runtime with lower bills. Allocate costs by `team / project / environment / job / workspace`. Serverless can improve operations, startup, scaling, and idle use without always being cheaper. Use real workloads and current [cost management documentation](https://docs.databricks.com/aws/en/admin/account-settings/usage), not a fixed assumed price.

### Which self-managed components can it replace?

| Existing responsibility | Integration candidate | Decision boundary |
|---|---|---|
| Spark cluster | Runtime / Serverless | High consolidation potential |
| Trino-like BI serving | SQL Warehouse | Check SQL, concurrency, and connector needs |
| Custom Spark pipeline framework | Pipelines | Check transformations and recovery |
| Catalog / Governance | Unity Catalog | Check external policy boundaries |
| OpenLineage / Marquez-like internal lineage | UC Lineage | Review external lineage separately |
| Self-hosted MLflow | Managed MLflow | Compare storage, auth, and features |
| Vector DB for Databricks-centered RAG | AI Search | Check quality, permissions, and sync |
| Airflow | Partial replacement by Jobs | Cross-platform orchestration may remain |
| Langfuse | MLflow feature overlap | Compare required trace/evaluation features |
| dbt | Some overlap with SQL / Pipelines | dbt remains a valid choice |
| Kafka | Usually remains separate | Durable event log / event bus |
| Flink | Keep when needed | Low-latency complex stateful streaming |

The value is less installation, upgrade, integration, security, and monitoring work across S3, tables, engines, orchestration, catalogs, lineage, MLflow, search, and AI observability. Balance simpler operations and faster integration against platform dependency, lock-in, and possible higher cost. See [Platform comparison](platform-comparison.md).

## LLM in Practice

### Review the scope of a managed migration

**Situation:** Assess whether to consolidate a hypothetical Spark, Trino, Airflow, and RAG search stack on Databricks.

**Context to Give the LLM:** Provide sanitized workloads, latency/freshness SLOs, external DAG dependencies, table formats and reader/writer versions, per-user retrieval permissions, costs, and operating hours.

**Example Prompt:**

=== "English"

    ```text {.prompt}
    [Context]
    Stack: [workloads and external dependencies]
    Constraints: [SLOs, reader/writer versions, retrieval permissions, costs and operating hours]
    [Task]
    Assess current responsibilities and observed problems first.
    Compare which responsibilities to keep or move to Databricks with evidence.
    Review remaining Kafka/Flink needs, external catalog access, and pre-retrieval ACLs separately.
    [Output]
    Separate observations, assumptions, and unknown support requirements.
    Give a responsibility table, phased experiments, failure criteria, and a rollback plan.
    [Checks]
    Do not promise product equivalence or cost savings.
    Link claims to official docs, real settings, denied-access tests, and metrics to measure.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    구성: [workload 목록과 외부 의존성]
    제약: [SLO, reader/writer 버전, 검색 권한, 비용과 운영시간]
    [요청]
    먼저 현 구조의 책임과 실제 문제를 평가하라.
    Databricks로 유지 또는 이관할 범위를 근거와 함께 비교하라.
    Kafka/Flink 잔존, 외부 catalog 접근, 검색 전 ACL을 별도로 검토하라.
    [출력]
    관찰 사실, 가정, 미확인 지원 조건을 분리하라.
    책임별 후보표와 단계적 실험, 실패 기준, rollback 계획을 작성하라.
    [검증]
    제품 동등성이나 비용 절감을 단정하지 말라.
    공식 문서, 실제 설정, 권한 거부 테스트, 측정해야 할 지표를 연결하라.
    ```

**Expected Output:** A keep/migrate table by responsibility, unknown requirements, phased experiments, access tests, and a rollback plan.

**What the LLM Can Get Wrong:** It may assume UC protects every external access and retrieval row, or that Kafka and Flink always disappear.

**How to Validate:** Compare current official support tables with real settings. Test external reads/writes, denied retrieval, retries, and recovery in isolation. Measure actual bills and operating hours. Have a person approve the decision.
