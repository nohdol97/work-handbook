---
id: prompt-library
status: overview
last_updated: 2026-10-05
last_reviewed: 2026-10-05
knowledge_ids: []
---

# Practical prompt library

Use these templates for SQL, schema, and configuration reviews, incident investigation, cost analysis, and deployment or recovery planning. Choose by **the decision you need to make**, then by technology. The cases were selected to organize evidence and find review gaps in recurring work. Their usage frequency and effectiveness have not been measured.

## Start with your task

| Task | Starting cases | Useful result |
|---|---|---|
| Review a SQL or model PR | [Join row explosion](spark.md#spark-01) · [Incremental first runs and keys](dbt.md#dbt-05) · [SCD join boundaries](analytical-modeling.md#analytical-modeling-02) | Evidence locations, counterexamples, and minimal changes |
| Change a schema or contract | [CDC downstream impact](cdc-debezium.md#cdc-debezium-03) · [Event units and meaning](event-architecture.md#event-architecture-01) · [Contract SLOs and owners](governance.md#governance-06) | Broken consumer assumptions, open agreements, and rollout blockers |
| Triage an incident | [Freshness lag](data-observability.md#data-observability-01) · [Results differ across paths](event-architecture.md#event-architecture-04) · [Wrong RAG answers](ai-ready-data.md#ai-ready-data-04) | Observations, hypotheses, impact, and first checks |
| Review performance or cost | [Read cost](foundations.md#foundations-06) · [Trino OOM](trino.md#trino-02) · [Flink backpressure](flink.md#flink-05) | Bottleneck evidence, one-variable comparisons, and acceptance criteria |
| Prepare a rollout or migration | [Savepoint upgrade](flink.md#flink-04) · [Polling to CDC](cdc-debezium.md#cdc-debezium-05) · [Embedding refresh](ai-ready-data.md#ai-ready-data-03) | Scope, restore conditions, and proceed/hold decisions |
| Check reprocessing or recovery | [Resume failed tasks](orchestration.md#orchestration-03) · [Replay quarantine](data-quality.md#data-quality-03) · [Resume downstream use](data-quality.md#data-quality-06) | Reuse evidence, stop conditions, and reconciliation |
| Review evaluations or docs | [Failure to regression case](ai-ready-data.md#ai-ready-data-02) · [Compare agent versions](online-evaluation.md#online-evaluation-05) · [Review a translation PR](knowledge-workflow.md#knowledge-workflow-02) | Regression checks, comparison limits, and evidence-based edits |

## How to use

1. Read **Input preparation** and collect sanitized SQL, settings, logs, and samples for the same run or period. Label synthetic samples when real evidence is unavailable.
2. Copy the prompt from the `한국어` or `English` tab and fill the brackets. Add line numbers, timestamps, or sample IDs to inputs. Mark unknown values as `unknown`.
3. Compare each finding with its cited input. Use **What the LLM can get wrong** and **Expected result / validation** to accept or hold findings. Answer requests for missing evidence before relying on a conclusion.

Each prompt can be copied on its own. The answer is a review draft and does not authorize execution or changes. After use, record accepted findings, incorrect findings, and review time to judge usefulness for your own work.

## All cases by topic

The library contains 100 cases with specific questions and checks. Concept guides contain another 45 cases with bilingual tabs. Authored examples do not establish study completion or actual production experience.

| Topic | Decisions covered |
|---|---|
| [Storage and analytics](foundations.md) | Workload isolation, partitions, pruning, and read cost |
| [Event architecture](event-architecture.md) | Contracts, schema, duplicates, replay, and time basis |
| [Lakehouse / Iceberg](lakehouse-iceberg.md) | Snapshots, write modes, maintenance, and retention |
| [Spark](spark.md) | Joins, memory, output files, and retries |
| [Flink](flink.md) | Windows, state, checkpoints, and upgrades |
| [CDC / Debezium](cdc-debezium.md) | Snapshot recovery, deletes, schema, and reconciliation |
| [Orchestration](orchestration.md) | Readiness, retries, resume points, and publication gates |
| [dbt](dbt.md) | Model PRs, dependencies, tests, incremental work, and recalculation |
| [Analytical modeling](analytical-modeling.md) | Grain, history joins, metrics, and dimensions |
| [Trino](trino.md) | Pushdown, memory, skew, and workload placement |
| [Data quality](data-quality.md) | Check placement, quarantine, SLOs, and recovery |
| [Data observability](data-observability.md) | Freshness, volume, distributions, and alerts |
| [Lineage and metadata](lineage-metadata.md) | Catalogs, conflicting definitions, tracing, and impact |
| [Governance](governance.md) | Ownership, access, masking, retention, and audit |
| [AI-ready data](ai-ready-data.md) | Telemetry, regression cases, embeddings, and RAG |
| [Online AI evaluation](online-evaluation.md) | Evaluation links, missing scores, rubrics, and version comparisons |
| [Knowledge workflow](knowledge-workflow.md) | Extraction, translation, merging, and review evidence |

## Work examples in concept guides

[Release evaluation](../data-platform/ai-evaluation.md), [platform choice](../data-platform/platform-comparison.md), [operations and recovery](../data-platform/production-operations.md), and [architecture](../data-platform/architecture.md) provide review examples with their conceptual context. Find infrastructure and AWS cases through the [platform and infrastructure index](../platform-infrastructure/index.md) and [AWS index](../aws-cloud/index.md).
