---
id: data-platform-curriculum
status: overview
last_updated: 2026-09-24
last_reviewed: 2026-09-24
knowledge_ids:
  - DPE-00-01
  - DPE-18-01
  - DPE-18-02
  - DPE-18-03
  - DPE-18-04
  - DPE-18-05
  - DPE-18-06
  - DPE-18-07
---

# Study scope and remaining curriculum

## Source and depth

This page preserves the progress recorded in the supplied Data Platform Engineering notes. The study aimed to explain why technologies exist, which problems they solve, their core functions, their connections and differences, and their place in the overall architecture. It does not claim deep implementation study or completed production work.

The source calls Chapters 1–4 **reconstructed notes** of earlier completed study. Chapter 5 onward follows the continued study session. The original conversation and earlier material were not supplied, so the reconstruction could not be independently verified. “Completed” below means the study status reported in the source.

Source Chapter 17 contains supplementary explanations, and Chapter 18 records progress. **Phases 17–21** below are future study topics, not those chapter numbers.

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

## In progress: Phase 16

Only [16.1 Online Evaluation Events](online-evaluation.md) is complete. The following topics are **not-started**. Brief mentions in the AI-ready data page do not count as completing these separate lessons.

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

## Not started: Phase 17 — Databricks Deep Dive

Status: **not-started**. These are future topics listed by the source, not verified product capabilities or completed lessons.

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

## Not started: Phase 18 — Snowflake Deep Dive

Status: **not-started**. These are future topics listed by the source, not verified product capabilities or completed lessons.

- Architecture
- Micro-partitions
- Pruning
- Clustering
- Streams
- Tasks
- Dynamic Tables
- Snowpipe
- Iceberg Tables
- Governance
- Cortex / AI capabilities
- Cost / Scaling Model

## Not started: Phase 19 — Databricks vs Snowflake vs Open Lakehouse

Status: **not-started**. These are future topics listed by the source, not verified product capabilities or completed lessons.

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

## Not started: Phase 20 — Production Data Platform Engineering

Status: **not-started**. These are future topics listed by the source, not verified product capabilities or completed lessons.

- Backfills
- Reprocessing
- Incident Drills
- Capacity Planning
- Cost Engineering
- DR / Recovery
- Data Platform SLOs

## Not started: Phase 21 — final end-to-end project

Status: **not-started**. The target follows the [architecture](architecture.md): Applications → Kafka → Flink/Spark Streaming → Bronze Iceberg → Spark/dbt → Silver → Gold → Trino/BI/AI Evaluation, with PostgreSQL → Debezium → Kafka.

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

No design implementation, failure experiment, or performance measurement is supplied yet. Update the scope and study status when further source material arrives.

[Architecture](architecture.md) · [Home](../index.md)
