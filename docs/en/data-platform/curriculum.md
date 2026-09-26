---
id: data-platform-curriculum
status: overview
last_updated: 2026-09-26
last_reviewed: 2026-09-26
knowledge_ids:
  - DPE-00-01
  - DPE-18-01
  - DPE-18-02
  - DPE-18-03
  - DPE-18-04
  - DPE-18-05
  - DPE-18-06
  - DPE-18-07
  - DPE2-00-01
  - DPE2-00-02
  - DPE2-23-01
  - DPE2-23-02
---

# Study scope and completion

## Source and depth

This page preserves the progress recorded in the supplied Data Platform Engineering notes. The study aimed to explain why technologies exist, which problems they solve, their core functions, their connections and differences, and their place in the overall architecture. It does not claim deep implementation study or completed production work.

The source calls Chapters 1–4 **reconstructed notes** of earlier completed study. Chapter 5 onward follows the continued study session. The original conversation and earlier material were not supplied, so the reconstruction could not be independently verified. “Completed” below means the study status reported in the source.

In the first source, Chapter 17 contains supplementary explanations and Chapter 18 records progress at that time. Chapters 16–21 in the source added on 2026-09-26 match the Phase numbers below and declare **conceptual study of Phases 1–21 complete**. The first source keeps its historical not-started record; this page reflects the new material.

## Completed: Phases 1–15

1. [Foundations](foundations.md) — conceptual study completed.
2. [Event architecture](event-architecture.md) — conceptual study completed.
3. [Lakehouse / Iceberg](lakehouse-iceberg.md) — conceptual study completed.
4. [Spark](spark.md) — conceptual study completed.
5. [Flink](flink.md) — conceptual study completed.
6. [CDC / Debezium](cdc-debezium.md) — conceptual study completed.
7. [Orchestration](orchestration.md) — conceptual study completed.
8. [dbt](dbt.md) — conceptual study completed.
9. [Analytical data modeling](analytical-modeling.md) — conceptual study completed.
10. [Trino](trino.md) — conceptual study completed.
11. [Data quality](data-quality.md) — conceptual study completed.
12. [Data observability](data-observability.md) — conceptual study completed.
13. [Lineage and metadata](lineage-metadata.md) — conceptual study completed.
14. [Governance](governance.md) — conceptual study completed.
15. [AI-ready data](ai-ready-data.md) — conceptual study completed.

## Completed: Phase 16 — AI evaluation data platform

Conceptual study now covers [16.1 online evaluation](online-evaluation.md) and [16.2–16.12 AI evaluation](ai-evaluation.md). Examples, numbers, and version tables are learning examples, not actual model evaluation results.

- 16.2 Offline Evaluation Datasets
- 16.3 Human Feedback
- 16.4 Model-as-Judge Outputs
- 16.5 Prompt Versions
- 16.6 Model Versions
- 16.7 Agent Versions
- 16.8 Experiment Tracking
- 16.9 Regression Datasets
- 16.10 Cost / Quality / Latency Analysis
- 16.11 Langfuse + Iceberg Integration
- 16.12 Version management locations and bundle links

## Completed: Phase 17 — Databricks Deep Dive

Status: **studied — conceptual study completed**. [Databricks](databricks.md) contains the supplied content. Official documentation checks do not replace deployment or performance tests.

- Lakehouse Architecture
- Spark Runtime
- SQL Warehouses
- Unity Catalog
- Workflows
- Lakeflow
- Delta / Iceberg interoperability
- Lineage / Governance
- MLflow
- AI / Vector capabilities
- Cost Model
- Which self-managed components Databricks replaces

## Completed: Phase 18 — Snowflake Deep Dive

Status: **studied — conceptual study completed**. [Snowflake](snowflake.md) contains the supplied content. The new source is condensed and does not claim deep internal implementation study. Official documentation checks do not replace deployment or performance tests.

- Architecture
- Micro-partitions
- Pruning
- Clustering
- Streams
- Tasks
- Dynamic Tables
- Snowpipe / Snowpipe Streaming
- Iceberg Tables
- Governance
- Cortex / AI capabilities
- Cost / Scaling Model
- Snowflake Mental Model

## Completed: Phase 19 — Databricks vs Snowflake vs Open Lakehouse

Status: **studied — conceptual study completed**. [Platform comparison](platform-comparison.md) contains the supplied content. Official documentation checks do not replace deployment or performance tests.

- Storage Ownership
- Iceberg Openness
- Compute Model
- Streaming
- Batch
- SQL
- Governance
- Lineage
- AI Ecosystem
- Portability
- Operational Complexity
- Vendor Lock-in
- Total Cost

## Completed: Phase 20 — Production Data Platform Engineering

Status: **studied — conceptual study completed**. [Production operations](production-operations.md) contains the supplied content. Incident examples are conceptual scenarios, not completed drills. Official documentation checks do not replace deployment or performance tests.

- Backfills
- Reprocessing
- Incident Drills
- Capacity Planning
- Cost Engineering
- DR / Recovery
- Data Platform SLOs

## Completed: Phase 21 — final end-to-end architecture

Status: **studied — architecture concepts integrated**. The learning design follows the [architecture](architecture.md): Applications → Kafka → Flink/Spark Streaming → Bronze Iceberg → Spark/dbt → Silver → Gold → Trino/BI/AI Evaluation, with PostgreSQL → Debezium → Kafka.

Supporting capabilities are Airflow orchestration, data quality, OpenLineage, catalog/discovery/governance, freshness/correctness observability, and Langfuse AI telemetry/evaluation. Before and after implementation, collect evidence for these questions:

1. Why does each component exist?
2. How does it behave during failure?
3. How are backfills performed?
4. What is the consistency model?
5. How does it scale?
6. Where do costs arise?
7. How are data contracts applied?
8. How are SLOs defined?
9. How does recovery work?
10. Which components could a smaller system remove?

The new source explains component purposes, failure behavior, guarantee boundaries, backfills, scaling, cost, smaller-scale omissions, open/managed alternatives, and seven engineering principles. These are integrated into the [architecture](architecture.md).

No implementation, failure experiment, or performance measurement is supplied. Completion describes conceptual understanding of an overview curriculum, not certified operational skill. The learning goal is to explain OLTP/OLAP, Parquet, object storage, Iceberg, Spark/Flink, Kafka/CDC, Airflow/dbt/Trino, analytical models, quality/observability, metadata/lineage/catalog/governance, AI-ready data, telemetry/evaluation/versioning, Langfuse/MLflow, managed integration, open alternatives, recovery, and simplification at smaller scale.

## Scope of product references

The new source names Unity Catalog, Lakeflow Jobs, managed Delta/Iceberg, the Iceberg REST Catalog, Dynamic Tables, Horizon Catalog, and Snowflake Iceberg documentation, but supplies no URLs, versions, or access dates. Current official evidence was therefore checked separately on each product page, with dates and limits. Confirm the actual cloud, region, edition, version, and settings before use.

[Architecture](architecture.md) · [Home](../index.md)
