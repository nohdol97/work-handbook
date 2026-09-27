---
id: data-platform-foundations
status: studied
last_updated: 2026-09-27
last_reviewed: 2026-09-27
knowledge_ids:
  - DPE-01-01
  - DPE-01-02
  - DPE-01-03
  - DPE-01-04
  - DPE-01-05
  - DPE-01-06
  - DPE-01-07
---

# Chapter 1 — Data Engineering Foundations

Page type: Learn. This page records concepts and design examples from the supplied study material. `studied` means conceptual study, not hands-on implementation or production validation. SQL and numbers are illustrative and were not run.

The body translates the latest supplied source without merging its headings, paragraphs, lists, or examples. Corrections, conditions on simplified statements, and previous additions appear separately under **Qualifications for real use**.

**Reading note:** The source core below keeps the original order and form. Read the section-specific corrections, conditions, and additions in the supplement after the source material; some original statements are simplified.

<!-- SOURCE CORE START -->

## 1.1 OLTP vs OLAP

### OLTP

OLTP stands for **Online Transaction Processing**.

Its main purpose is to process live service transactions.

Example:

- User registration
- Order creation
- Payment
- Inventory changes
- Creating a post

Characteristics:

- Frequently reads and writes a small set of rows.
- Many INSERT / UPDATE / DELETE operations.
- Fast responses to individual requests matter.
- Often uses normalized data models.

Typical systems:

- PostgreSQL
- MySQL

Example:

```text
users
orders
payments
```

Service applications commonly use these OLTP databases.

---

### OLAP

OLAP stands for **Online Analytical Processing**.

Its purpose is to analyze large amounts of data.

Example:

```text
Over the last year,
what was the LLM usage cost by team?

What was the average latency by model?

What were user behavior patterns over the last six months?
```

Characteristics:

- Reads very large numbers of rows.
- Many large scans, aggregations, and joins.
- Reads account for more work than writes.
- Works well with columnar storage.
- Often uses analytical models such as denormalized tables or star schemas.

---

### Why PostgreSQL can become less suitable for growing analytical history

PostgreSQL can run analytics.

However, as data accumulates:

```text
Hundreds of millions to billions of rows
+
Large scans
+
Large aggregations
+
Long-term history
```

these needs can cause analytical workloads to compete with service transactions in the database.

A common approach is:

```text
Application
   ↓
PostgreSQL
   ↓
CDC / Event Pipeline
   ↓
Lakehouse / Warehouse
```

to separate operational and analytical systems in this way.

Key point:

> **OLTP quickly handles the service's current state; OLAP analyzes large histories.**

---

## 1.2 Row-Oriented vs Column-Oriented Storage

### Row-Oriented

Row-oriented storage keeps the values of one row together.

Conceptually:

```text
Row 1: user_id, name, age, team
Row 2: user_id, name, age, team
```

This is useful for OLTP.

For example, row-oriented storage is a natural fit when reading all the information about one user.

---

### Column-Oriented

Column-oriented storage keeps values from the same column together.

Conceptually:

```text
user_id: 1, 2, 3, 4 ...
age:     20, 30, 40, 50 ...
team:    A, A, B, A ...
```

Analytical queries often read only certain columns.

Example:

```sql
SELECT AVG(latency_ms)
FROM llm_calls
```

This query does not need to read `prompt`, `response`, or `user_id`.

This is why columnar formats suit OLAP.

---

### Compression

Similar values often repeat within the same column.

Example:

```text
team_id:
A
A
A
A
B
B
B
```

Patterns like this compress well.

Columnar storage therefore helps with:

- Reading less data
- Improving compression efficiency
- Improving analytical query performance

These are useful benefits.

---

### Column Pruning

This optimization reads only the columns a query needs.

Example:

```sql
SELECT model_id, latency_ms
FROM fact_llm_call
```

Only the required columns need to be read for this query.

Key point:

> **Parquet is called a columnar file format because it stores data by column, letting analytical queries efficiently read only the columns they need.**

---

## 1.3 Parquet

Parquet is a widely used **Columnar File Format**.

Role:

> **A file format for efficiently storing large analytical datasets.**

Parquet itself is not a database.

```text
S3
├─ part-0001.parquet
├─ part-0002.parquet
└─ part-0003.parquet
```

The data can be stored as files in object storage, as shown above.

---

### Row Group

Data inside a Parquet file is divided into large units called **Row Groups**.

```text
Parquet File
├─ Row Group 1
├─ Row Group 2
└─ Row Group 3
```

Within each row group, data is stored by column.

---

### Page

Column data within a row group can be further divided into pages.

Big picture:

```text
Parquet File
  ↓
Row Group
  ↓
Column Chunk
  ↓
Page
```

This session does not need to go deeply into the binary format. The key idea is that **Parquet divides data into hierarchical units and uses statistics to reduce unnecessary scans**.

---

### Encoding / Compression

Parquet applies encoding and compression based on column characteristics.

Purpose:

```text
Less storage space
+
Less I/O
```

Example:

- Repeated values
- Numeric data
- String dictionaries

These can be compressed efficiently.

---

### Statistics

Parquet can store statistics for row groups or pages.

Example:

```text
latency_ms
min = 100
max = 500
```

If the query is:

```sql
WHERE latency_ms > 1000
```

there is no need to read this row group.

This optimization is **Min/Max Pruning**.

---

### Predicate Pushdown / Pruning

Use conditions to avoid reading unnecessary data.

Example:

```sql
WHERE event_date = '2026-09-24'
```

Where possible, read only the required row groups or files.

---

### Column Pruning

Read only the required columns.

An important benefit of Parquet is:

```text
Only the required row range
+
Only the required columns
```

the ability to limit reading in this way.

---

## 1.4 Object Storage

Typical object storage systems:

- Amazon S3
- S3-compatible storage
- Azure Blob Storage
- Google Cloud Storage

Reasons lakehouses commonly use object storage:

- Can store very large amounts of data
- Can separate compute and storage
- Relatively low-cost bulk storage
- Several compute engines can share the same data

---

### Object vs Block/File Storage

Object storage manages data as objects.

Example:

```text
s3://bucket/path/file.parquet
```

It suits large, mostly immutable objects better than frequent random writes like those on a traditional local file system.

---

### Storage / Compute Separation

Traditional databases often tightly couple compute and storage in one system.

A lakehouse can use:

```text
Storage
→ S3

Compute
→ Spark / Trino / Flink / Databricks
```

this separation of storage and compute.

Advantages:

- Scale compute independently
- Read the same data from several engines
- Keep storage when compute stops

---

### Remote I/O

Because compute and storage are separate, files must be read over the network.

Therefore:

- Reduce unnecessary scans
- Optimize file sizes
- pruning
- caching

these practices become important.

---

## 1.5 File Layout Engineering

The size of an individual file can affect lakehouse performance.

---

### Small File Problem

Example:

```text
file1.parquet  1MB
file2.parquet  2MB
file3.parquet  800KB
...
Millions of files
```

When files are too small:

- More metadata
- More file-open cost
- More query-planning cost
- Too many tasks
- More object-storage requests

these problems can occur.

---

### Too-Large File

Conversely, when files are too large:

- Fewer units of parallel work
- Some tasks may take a long time
- Higher rewrite cost

these problems can occur.

Choose a **Target File Size** that suits the workload.

---

### Compaction

Combine small files into larger files.

```text
5MB
10MB
8MB
7MB
  ↓
Compaction
  ↓
A suitably sized Parquet file
```

This is especially important for streaming into a lakehouse.

---

### Write Amplification

Rewriting an entire large file to change a small amount of data can cause far more physical writing than the logical change.

Account for this cost when designing file layout and choosing a table format.

---

## 1.6 Partitioning Fundamentals

Partitioning divides data physically or logically according to a rule.

Example:

```text
event_date=2026-09-23
event_date=2026-09-24
```

---

### Partition Pruning

Query:

```sql
WHERE event_date = '2026-09-24'
```

the query can read only the partition for that date.

In other words:

> **Read only the required partitions instead of scanning all the data.**

---

### Cardinality

Cardinality matters when choosing a partition key.

Low-cardinality examples:

```text
country
status
```

High-cardinality examples:

```text
user_id
request_id
```

Directly partitioning by a column with many distinct values, such as `user_id`, can create too many partitions.

---

### Good / Bad Partition Keys

A good partition key:

- Appears often in query filters
- Does not create too many partitions
- Avoids excessive concentration of data in one partition

Common time-based choices include:

```text
day
hour
```

These are often used.

---

### Over-Partitioning

When partitions become too fine-grained:

- More small files
- More metadata
- More management complexity

these effects occur.

---

### Partition vs File

A partition is a logical division of data. One partition can contain several files.

```text
date=2026-09-24
├─ file1.parquet
├─ file2.parquet
└─ file3.parquet
```

---

## 1.7 Bucketing / Sorting / Indexing

### Bucketing

Use a hash to divide data into a fixed number of buckets.

Example:

```text
bucket(user_id, 32)
```

This distributes high-cardinality keys across a fixed number of groups instead of creating a partition for each key.

---

### Sorting

Sort data within files by a particular key.

Example:

```text
sort by user_id
```

When similar values are close together, file min/max statistics can become more useful.

---

### Clustering

Place data that is often queried together physically close to reduce scan ranges.

---

### Lakehouse Indexing vs OLTP Index

OLTP databases often use row-level indexes such as B-trees.

Because lakehouses focus on large-scan workloads:

- Partition
- File Statistics
- Sort Order
- Data Skipping
- Clustering

these techniques are often used to reduce the amount read.

---

<!-- SOURCE CORE END -->

## Qualifications for real use

These sections are starting models. Choose whether to separate PostgreSQL analytics by measured workload impact, cost, and response time, not a row-count threshold. Include request and transfer costs when comparing object storage.

Parquet column chunks live inside row groups. Pruning depends on available statistics or indexes and reader support. Pushdown sends a filter to a lower layer; pruning skips storage units that cannot match. Neither is arbitrary row lookup. Encoding and compression are distinct steps. [Apache Parquet file format](https://parquet.apache.org/docs/file-format/)

A large Parquet file can have several scan splits. One file is not always one task. Balance parallelism, rewrite cost, and request cost when setting file-size targets. Bucket notation is conceptual; check the engine's argument order and syntax.

### Sections 1.3 and 1.6: statistics and cardinality

The source's phrase “only the required row range” means skipping units such as row groups when statistics allow it. It does not promise row-index access to only the exact matching rows.

Cardinality is the number of distinct values. Choose day or hour partition granularity based on actual data volume and query patterns. The Iceberg transform notation is conceptually `bucket(32, user_id)`.

## Related reading

[Event architecture](event-architecture.md), [Iceberg](lakehouse-iceberg.md), [Spark](spark.md).

## LLM in practice: File-layout review

- Situation: A hypothetical workload has many small files and slow date-filtered queries.
- Context to give the LLM: Give sample queries, file-size distribution, partition keys, scan bytes, and planning time. Remove real data and identifiers.
- Expected output: Expect candidate causes, trade-offs, and a measurement plan.
- What the LLM can get wrong: The LLM may blame only small files or invent a universal target size.
- How to validate: Compare planning time, scan bytes, and task distribution for the same query and input.

Example prompt:

=== "English"

    ```text {.prompt}
    [Context]
    Queries and layout: [SQL, partition keys, file-size distribution]
    Measurements: [scan bytes, planning time, task distribution]

    [Task]
    Review the current file layout before suggesting changes.
    Separate observations, assumptions, and hypotheses.
    Compare compaction, partition changes, and sorting.

    [Output]
    List cost drivers, trade-offs, and missing evidence for each option.

    [Checks]
    Propose one measurable check for each option.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    쿼리와 배치: [SQL·partition key·파일 크기 분포]
    측정: [scan bytes·planning time·task 분포]

    [요청]
    변경 제안 전에 현재 파일 배치를 검토해 줘.
    관찰, 가정, 가설을 나누고 compaction·partition 변경·정렬을 비교해 줘.

    [출력]
    선택지별 비용 원인·trade-off·누락 근거를 작성해 줘.

    [검증]
    선택지마다 하나의 측정 가능한 검증을 제안해 줘.
    ```

[See six more practical prompts for this topic](../prompts/foundations.md)

LLM output is a working hypothesis. Check it against official docs and actual configuration, logs, and measurements. External documents reviewed: 2026-09-24. This does not mean an implementation version was tested.
