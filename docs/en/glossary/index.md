---
id: handbook-glossary
status: overview
last_updated: 2026-09-26
last_reviewed: 2026-09-26
knowledge_ids: []
---

# Glossary

| Term | Meaning |
|---|---|
| Canonical knowledge | A shared set of useful knowledge merged from several sources. |
| Canonical page ID | A stable page identifier that stays the same when a path changes. A Korean and English pair shares one ID. |
| Content manifest | A list of meaningful source items with stable IDs. |
| Coverage matrix | A table that tracks where each ID is included, merged, deferred, or excluded, and why. |
| Semantic audit | A review of whether both languages keep the same concepts, examples, constraints, and warnings. |
| Source of truth | The original used to guide changes and decisions. Here, it is Markdown in Git. |

## Data platform terms

| Term | Meaning | Canonical topic |
|---|---|---|
| OLTP | A workload for small service transactions. | [foundations](../data-platform/foundations.md) |
| OLAP | An analytical workload that scans, aggregates, and joins large histories. | [foundations](../data-platform/foundations.md) |
| Column pruning | Reading only the columns a query needs. | [foundations](../data-platform/foundations.md) |
| Partition / pruning | A rule that divides data / skipping regions that cannot match a query. | [foundations](../data-platform/foundations.md) |
| Cardinality | The number of distinct values. | [foundations](../data-platform/foundations.md) |
| Compaction | Maintenance that combines small files into suitable sizes. | [foundations](../data-platform/foundations.md) |
| Schema | A definition of data structure, such as fields and types. | [event-architecture](../data-platform/event-architecture.md) |
| Idempotency | Repeating an operation does not duplicate its intended effect. | [event-architecture](../data-platform/event-architecture.md) |
| Consumer lag | A measure of how far a consumer is behind, often a log-position gap. | [event-architecture](../data-platform/event-architecture.md) |
| Snapshot | A consistent view of table or processing state at a point in time; scope depends on the type. | [lakehouse-iceberg](../data-platform/lakehouse-iceberg.md) |
| Shuffle | Moving data between processing nodes for operations such as grouping by key. | [spark](../data-platform/spark.md) |
| Data skew | Uneven data or work across keys or tasks. | [spark](../data-platform/spark.md) |
| Watermark | An estimate of event-time progress used for late data and state handling. | [flink](../data-platform/flink.md) |
| Checkpoint / savepoint | A state snapshot for recovery / a state snapshot used for planned operational changes. | [flink](../data-platform/flink.md) |
| Backpressure | Pressure sent upstream when downstream processing cannot keep up. | [flink](../data-platform/flink.md) |
| CDC | Capturing source changes such as inserts, updates, and deletes. | [cdc-debezium](../data-platform/cdc-debezium.md) |
| WAL | A write-ahead log of database changes used for recovery and replication. | [cdc-debezium](../data-platform/cdc-debezium.md) |
| Tombstone | A null-value record marking key removal in a Kafka compacted topic. | [cdc-debezium](../data-platform/cdc-debezium.md) |
| Orchestration / DAG | Managing task dependencies and execution / a directed graph without cycles. | [orchestration](../data-platform/orchestration.md) |
| Backfill | Filling or recomputing data for a past range. | [orchestration](../data-platform/orchestration.md) |
| Grain | What one row in a table represents. | [analytical-modeling](../data-platform/analytical-modeling.md) |
| Fact / dimension | Measured events or values / attributes that describe them. | [analytical-modeling](../data-platform/analytical-modeling.md) |
| SCD Type 2 | A model that preserves attribute history with new rows and validity periods. | [analytical-modeling](../data-platform/analytical-modeling.md) |
| Semantic layer | A layer defining reusable meanings and calculations for metrics and dimensions. | [analytical-modeling](../data-platform/analytical-modeling.md) |
| Predicate pushdown | Passing filter processing closer to the data source. | [trino](../data-platform/trino.md) |
| Data quality | Whether data meets requirements such as accuracy, completeness, and validity. | [data-quality](../data-platform/data-quality.md) |
| Quarantine | Separating invalid data from the normal path for investigation and recovery. | [data-quality](../data-platform/data-quality.md) |
| SLI / SLO | A measured service-level indicator / its target. | [data-observability](../data-platform/data-observability.md) |
| Freshness | Whether data is recent enough for its use. | [data-observability](../data-platform/data-observability.md) |
| Observability | Understanding system or data state and change through observed signals. | [data-observability](../data-platform/data-observability.md) |
| Lineage | Relationships showing how data is created, moved, and transformed. | [lineage-metadata](../data-platform/lineage-metadata.md) |
| Metadata / catalog | Information about data / a system for finding and exploring that information. | [lineage-metadata](../data-platform/lineage-metadata.md) |
| Data contract | An agreement covering schema, meaning, quality, freshness, and ownership. | [governance](../data-platform/governance.md) |
| RBAC | Access control that grants permissions by role. | [governance](../data-platform/governance.md) |
| Retention | How long and under which conditions data and derived copies are kept. | [governance](../data-platform/governance.md) |
| Trace / observation / session | An execution flow / an individual step / a group of related executions. | [ai-ready-data](../data-platform/ai-ready-data.md) |
| Provenance | Information tracing the origin and production context of data or AI output. | [ai-ready-data](../data-platform/ai-ready-data.md) |
| Reproducibility | The ability to restore experiment conditions; it does not guarantee identical LLM wording. | [ai-ready-data](../data-platform/ai-ready-data.md) |
| Regression dataset | Evaluation cases used to check whether past failures return. | [ai-ready-data](../data-platform/ai-ready-data.md) |
| Online evaluation | Attaching feedback, rule checks, or judge signals to real AI executions. | [online-evaluation](../data-platform/online-evaluation.md) |

[Knowledge workflow](../methodologies/knowledge-workflow.md) · [Home](../index.md)

## Evaluation, managed platforms, and recovery

| Term | Meaning | Canonical topic |
|---|---|---|
| Rubric | Scoring and decision criteria for each evaluation dimension. | [ai-evaluation](../data-platform/ai-evaluation.md) |
| Groundedness | How well a response is supported by the supplied evidence. | [ai-evaluation](../data-platform/ai-evaluation.md) |
| Inter-rater agreement | Agreement among people evaluating the same cases. | [ai-evaluation](../data-platform/ai-evaluation.md) |
| Bundle version | A version of the combined agent, prompt, tool, model, and retrieval configuration. | [ai-evaluation](../data-platform/ai-evaluation.md) |
| TTFT | Time to first token: the delay from a request to its first output token. | [ai-evaluation](../data-platform/ai-evaluation.md) |
| Cost per success | Total cost divided by successful executions, with explicit success criteria and measurement scope. | [ai-evaluation](../data-platform/ai-evaluation.md) |
| DBU | A Databricks usage unit. Check compute type, contract, and other factors for actual charges. | [databricks](../data-platform/databricks.md) |
| Photon | A vectorized query execution engine in Databricks. | [databricks](../data-platform/databricks.md) |
| UniForm | Provides metadata for Iceberg readers of Delta tables; it does not imply equal writer support. | [databricks](../data-platform/databricks.md) |
| Micro-partition | A Snowflake-managed columnar storage unit with metadata used for pruning. | [snowflake](../data-platform/snowflake.md) |
| Dynamic Table | A Snowflake object that refreshes a declared query result toward a target lag. | [snowflake](../data-platform/snowflake.md) |
| RTO | Recovery time objective: the target time allowed for recovery. | [production-operations](../data-platform/production-operations.md) |
| RPO | Recovery point objective: acceptable data loss expressed as a time window. | [production-operations](../data-platform/production-operations.md) |
