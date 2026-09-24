---
id: data-platform-foundations
status: studied
last_updated: 2026-09-24
last_reviewed: 2026-09-24
knowledge_ids:
  - DPE-01-01
  - DPE-01-02
  - DPE-01-03
  - DPE-01-04
  - DPE-01-05
  - DPE-01-06
  - DPE-01-07
---

# Data engineering foundations

Page type: Learn. This page records concepts and design examples from the supplied study material. `studied` means conceptual study, not hands-on implementation or production validation. SQL and numbers are illustrative and were not run.

## 1.1 OLTP vs OLAP

**Online Transaction Processing (OLTP)** handles live service transactions. Examples include user registration, order creation, payment, inventory changes, and posting a message. It reads or changes a small set of rows often. INSERT, UPDATE, and DELETE are common. Fast responses for individual requests matter. Normalized models are common. PostgreSQL and MySQL are typical examples. An application might use `users`, `orders`, and `payments` tables.

**Online Analytical Processing (OLAP)** answers questions across large datasets. For example: What was each team's LLM cost over the last year? What is the average latency by model? How did users behave over the last six months? Large scans, aggregations, and joins are common. Reads often dominate writes. Columnar storage and denormalized models such as star schemas suit these workloads.

PostgreSQL can run analytics. The concern is workload competition when hundreds of millions or billions of historical rows require large scans and aggregations. A common separation is:

```text
Application → PostgreSQL → CDC / Event Pipeline → Lakehouse / Warehouse
```

OLTP handles the service's current state quickly. OLAP analyzes large histories. Data size alone does not set a universal migration threshold.

## 1.2 Row-oriented vs column-oriented storage

Row-oriented storage keeps a row's values together:

```text
Row 1: user_id, name, age, team
Row 2: user_id, name, age, team
```

This suits a request for all details of one user. Column-oriented storage groups values from the same column:

```text
user_id: 1, 2, 3, 4 ...
age:     20, 30, 40, 50 ...
team:    A, A, B, A ...
```

An analytical query often needs only a few columns:

```sql
SELECT AVG(latency_ms)
FROM llm_calls;
```

It does not need `prompt`, `response`, or `user_id`. Similar values within one column also compress well. For example, `team_id = A, A, A, A, B, B, B` has repeated values. Less data and better compression can reduce I/O and improve analytical queries.

**Column pruning** reads only the columns the query needs:

```sql
SELECT model_id, latency_ms
FROM fact_llm_call;
```

Parquet is columnar because its layout lets readers access these columns efficiently.

## 1.3 Parquet

Parquet is a columnar file format for analytical data. It is not a database. Object storage may hold `part-0001.parquet`, `part-0002.parquet`, and `part-0003.parquet`.

Its main layout is:

```text
Parquet File → Row Group → Column Chunk → Page
```

A file has row groups. Each row group contains a chunk for each column. Column chunks contain pages. The useful mental model is a hierarchy of data units with metadata that can help skip work; this page does not cover the full binary format.

Encoding and compression reduce storage and I/O. Repeated values, numeric patterns, and string dictionaries can help. These are related but distinct steps.

Row-group statistics and optional page statistics or indexes can narrow a scan. Suppose a row group has `latency_ms min = 100, max = 500`. This condition cannot match that group:

```sql
WHERE latency_ms > 1000
```

Skipping it is min/max pruning. Predicate pushdown lets a lower layer use a filter. Pruning uses evidence to avoid reading units that cannot match. For example, `WHERE event_date = '2026-09-24'` may remove files or row groups where supported. Column pruning removes columns that the query does not use. Together these reduce both the data range and column set read. They do not promise arbitrary row access like a row index.

## 1.4 Object storage

Examples include Amazon S3, S3-compatible storage, Azure Blob Storage, and Google Cloud Storage. Lakehouses use object storage for large capacity, independent compute scaling, shared access by several engines, and often lower bulk-storage cost.

Object storage manages objects such as `s3://example-bucket/path/file.parquet`. Unlike block devices or a local file system, it is commonly used for large objects that are replaced rather than edited through frequent small random writes.

Storage and compute can have separate lifecycles:

```text
Storage: S3
Compute: Spark / Trino / Flink / Databricks
```

Compute can scale independently or stop while stored data remains. Several engines may read the same data. Remote file access adds network I/O, so pruning, sensible file sizes, caching, and avoiding unnecessary scans matter. Actual cost depends on requests, transfer, and the workload.

## 1.5 File layout engineering

Millions of tiny files, such as 1 MB, 2 MB, and 800 KB Parquet files, create a **small file problem**. They increase metadata, open requests, query planning work, object-store requests, and often task overhead.

Very large files also have trade-offs. Depending on scan splitting, they may reduce parallel work or create long tasks. They can increase the cost of rewriting data. Choose a target file size for the workload rather than one universal value.

**Compaction** combines small files into more useful sizes. For example, 5 MB, 10 MB, 8 MB, and 7 MB files can be rewritten into a larger file. It matters especially for streaming ingestion into a lakehouse.

**Write amplification** occurs when a small logical change requires much more physical writing. Rewriting a large file to change a few rows is one example. Layout and table-format choices affect this cost.

## 1.6 Partitioning fundamentals

Partitioning divides data by a physical or logical rule. For example:

```text
event_date=2026-09-23
event_date=2026-09-24
```

**Partition pruning** allows `WHERE event_date = '2026-09-24'` to select the relevant partition instead of scanning every date.

**Cardinality** is the number of distinct values. `country` and `status` are often lower-cardinality keys. `user_id` and `request_id` can have very high cardinality. Directly partitioning by each user can create too many partitions.

A useful key appears in common filters, creates a manageable number of partitions, and avoids severe imbalance. Day or hour is often useful. The right granularity still depends on volume and query patterns. Too many partitions cause small files, more metadata, and greater management work.

A partition is not one file. A date partition may contain `file1.parquet`, `file2.parquet`, and `file3.parquet`.

## 1.7 Bucketing, sorting, and indexing

**Bucketing** hashes values into a fixed number of groups. The conceptual example `bucket(user_id, 32)` means 32 buckets for users. This avoids a separate partition for every distinct user. Actual APIs use their own argument order, such as Iceberg's conceptual `bucket(32, user_id)` transform.

**Sorting** puts values in key order within the written layout. Sorting by `user_id` can narrow min/max ranges and make pruning more useful. **Clustering** places data commonly read together near each other to reduce scans.

OLTP systems often use row-level indexes such as B-trees. Lakehouse scans commonly depend on partitions, file statistics, sort order, data skipping, and clustering. These are ways to reduce scan work; they are not identical to an OLTP index.

## Qualifications for real use

These sections are starting models. Choose whether to separate PostgreSQL analytics by measured workload impact, cost, and response time, not a row-count threshold. Include request and transfer costs when comparing object storage.

Parquet column chunks live inside row groups. Pruning depends on available statistics or indexes and reader support. Pushdown sends a filter to a lower layer; pruning skips storage units that cannot match. Neither is arbitrary row lookup. Encoding and compression are distinct steps. [Apache Parquet file format](https://parquet.apache.org/docs/file-format/)

A large Parquet file can have several scan splits. One file is not always one task. Balance parallelism, rewrite cost, and request cost when setting file-size targets. Bucket notation is conceptual; check the engine's argument order and syntax.

## Related reading

[Event architecture](event-architecture.md), [Iceberg](lakehouse-iceberg.md), [Spark](spark.md).

## LLM in practice: File-layout review

- Situation: A hypothetical workload has many small files and slow date-filtered queries.
- Context to give the LLM: Give sample queries, file-size distribution, partition keys, scan bytes, and planning time. Remove real data and identifiers.
- Expected output: Expect candidate causes, trade-offs, and a measurement plan.
- What the LLM can get wrong: The LLM may blame only small files or invent a universal target size.
- How to validate: Compare planning time, scan bytes, and task distribution for the same query and input.

Example prompt:

```text
Review this file layout before suggesting changes. Separate observations, assumptions, and hypotheses. Compare compaction, partition changes, and sorting. List missing evidence and one measurable check for each option.
```

LLM output is a working hypothesis. Check it against official docs and actual configuration, logs, and measurements. External documents reviewed: 2026-09-24. This does not mean an implementation version was tested.
