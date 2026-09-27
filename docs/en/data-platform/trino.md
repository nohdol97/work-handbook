---
id: data-platform-trino
status: studied
last_updated: 2026-09-27
last_reviewed: 2026-09-27
knowledge_ids:
  - DPE-10-01
  - DPE-10-02
  - DPE-10-03
  - DPE-10-04
  - DPE-10-05
  - DPE-10-06
  - DPE-10-07
  - DPE-10-08
---

# Chapter 10 — Trino

This page records conceptual study of Trino. It does not claim verified query performance or production results. Official documentation was checked on 2026-09-24.

**Reading note:** The source core below keeps the original order and form. Read the section-specific corrections, conditions, and additions in the supplement after the source material; some original statements are simplified.

<!-- SOURCE CORE START -->

## 10.1 Architecture

Trino:

> **A distributed SQL query engine for fast queries on external data stores.**

Trino itself is not the primary storage system.

### Coordinator

- Analyze SQL.
- Build query plans.
- Manage stages and tasks.

### Worker

- Scan data.
- Join data.
- Run aggregations.

Role comparison:

```text
Trino Coordinator ≈ Spark Driver
Trino Worker ≈ Spark Executor
```

---

## 10.2 Connector Model

A connector is an adapter between Trino and an external system.

Examples:

- Iceberg Connector
- PostgreSQL Connector
- Hive Connector

Trino table names use:

```text
catalog.schema.table
```

Examples:

```text
iceberg.analytics.fact_llm_call
postgres.public.users
```

A Trino catalog and an Iceberg catalog have different meanings.

Trino Catalog:

> Identify which connector and data source to use.

A federated query can join different systems in one SQL statement. It does not guarantee good performance.

---

## 10.3 Query Execution

Conceptual structure:

```text
SQL
 ↓
Query Plan
 ↓
Stage
 ↓
Task
 ↓
Split
```

### Stage

A large execution step.

### Task

Part of a stage running on a specific worker.

### Split

A small unit of scan work.

### Exchange

Data redistribution between workers.

It is a similar concept to Spark shuffle.

Joins and GROUP BY operations can require many exchanges.

---

## 10.4 Pushdown

Purpose:

> **Perform supported work near the data to reduce scans and data movement.**

### Predicate Pushdown

Send `WHERE` conditions to the source.

### Projection Pushdown

Read only the required columns.

### Aggregation Pushdown

Run operations such as COUNT and SUM at the source when possible.

Iceberg partition, file, row group, and column pruning serve a similar purpose.

---

## 10.5 Join Strategies

### Broadcast Join

Copy a small table to all workers.

```text
Huge Fact
+
Tiny Dimension
```

### Partitioned Join

Redistribute large tables by join key.

This adds exchange costs.

### Data Skew

Some keys may concentrate work on a particular worker.

---

## 10.6 Memory

Trino keeps intermediate data for joins, aggregations, and sorts in memory.

Key concepts:

- Worker Memory
- Query Memory
- Spill

Spill:

```text
Memory pressure
 ↓
Use disk
```

Spill can help avoid query failure, but it slows the query.

---

## 10.7 Trino vs Spark

Common roles:

```text
Trino
→ Interactive SQL / Query Serving

Spark
→ Large-scale Processing / Transformation
```

Trino:

- BI
- Ad-hoc queries
- SQL from many concurrent users

Spark:

- ETL
- Backfills
- Large joins
- ML datasets
- Batch transforms

Using both:

```text
Spark
→ Create data

Trino
→ Query the created data
```

---

## 10.8 Trino + Iceberg

Structure:

```text
S3
 ↓
Parquet
 +
Iceberg Metadata
 ↓
Trino
 ↓
BI / Analyst
```

Trino uses Iceberg metadata to find needed files. It uses Parquet's columnar structure to read the required columns.

Roles:

```text
S3
→ Actual files

Parquet
→ File format

Iceberg
→ Table metadata / Snapshot

Trino
→ SQL queries
```

---

<!-- SOURCE CORE END -->

## Appendix: existing application notes

The main text follows the supplied chapter’s headings, examples, and order. These existing explanations and caveats are separate from the source text.

### Architecture and execution model

The Coordinator/Worker and Spark Driver/Executor comparison explains roles. It does not mean their execution models are identical. `SQL → Query Plan → Stage → Task → Split` is also a learning model, not a complete list of execution elements. [Trino concepts](https://trino.io/docs/current/overview/concepts.html)

A Trino catalog selects a configured connector and data source. An Iceberg catalog locates and manages table metadata. Assess remote scans, data movement, and source load for federated query performance.

### Check pushdown and joins

Pushdown support depends on the connector and query shape. A SQL filter does not guarantee pushdown. Check EXPLAIN and actual data read.

Iceberg pruning and aggregation pushdown to a remote database both aim to reduce reading and movement. They are not the same operation. [Trino pushdown](https://trino.io/docs/current/optimizer/pushdown.html)

Interpret the source’s “all workers” as workers participating in the join. Check that the small broadcast table fits each worker's memory. Skew can concentrate work and memory use on a few workers and make them finish later.

### Spill and role boundaries

Spill can reduce memory pressure, but it does not solve every out-of-memory failure. Disk I/O can slow the query.

The Trino documentation checked on 2026-09-24 called spill legacy functionality. It suggested considering fault-tolerant execution with an appropriate task retry policy and exchange manager. Check applicability against the workload, connectors, and settings. This edit did not recheck official documentation or run performance experiments. [Trino spill](https://trino.io/docs/current/admin/spill.html)

The Trino/Spark comparison describes common roles. It does not define absolute feature boundaries or guarantee performance.

Iceberg pruning also depends on layout, metadata, filters, and connector behavior. [Trino Iceberg connector](https://trino.io/docs/current/connector/iceberg.html)

### Existing conceptual diagram

This preserves the existing Mermaid diagram separately from the source’s text diagram.

```mermaid
flowchart LR
  S[S3 objects] --> P[Parquet data files]
  I[Iceberg metadata and snapshots] --> T[Trino]
  P --> T
  T --> B[BI and analysts]
```

## LLM in Practice: investigate a slow federated query

Situation: a query joining an Iceberg fact to a PostgreSQL dimension is slow. Give the LLM anonymized SQL, EXPLAIN, actual scan and output rows and bytes, table sizes, key distributions, memory errors, and connector settings.

=== "English"

    ```text {.prompt}
    [Context]
    Anonymized SQL, EXPLAIN, and scan and output rows and bytes: [samples]
    Table sizes, key distributions, memory errors, and connector settings: [context]

    [Task]
    Assess this federated query before redesigning it.
    Separate observations from assumptions and hypotheses.
    Check pushdown, join distribution, exchange volume, skew, and memory.
    List missing evidence and small checks that could reject each hypothesis.
    Do not assume spill or broadcast is always safe.

    [Output]
    Return possible bottlenecks, their evidence, and ordered checks.

    [Checks]
    Validate with actual plans, runtime statistics, connector documentation, and bounded query comparisons.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    익명화한 SQL·EXPLAIN·scan/output rows·bytes: [샘플]
    Table 크기·key 분포·memory 오류·connector 설정: [맥락]

    [요청]
    이 federated query를 재설계하기 전에 평가해 주세요.
    관찰·가정·가설을 구분해 주세요.
    Pushdown·join distribution·exchange volume·skew·memory를 확인해 주세요.
    부족한 근거와 각 가설을 반박할 수 있는 작은 확인 작업을 나열해 주세요.
    Spill이나 broadcast가 항상 안전하다고 가정하지 말아 주세요.

    [출력]
    근거별 병목 후보와 확인 순서를 주세요.

    [검증]
    실제 plan·runtime 통계·connector 문서와 제한된 query 비교로 검증해 주세요.
    ```

Expected output links possible bottlenecks to evidence and next checks. The LLM may assume pushdown support or only suggest switching to Spark. Check the actual plan, runtime statistics, and connector documentation. Use bounded query comparisons to test each hypothesis. No performance experiment was run here.

[Analytical modeling](analytical-modeling.md) · [dbt](dbt.md) · [Handbook home](../index.md)

[Six related practical prompts](../prompts/trino.md)
