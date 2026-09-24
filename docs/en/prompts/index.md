---
id: prompt-library
status: overview
last_updated: 2026-09-24
last_reviewed: 2026-09-24
knowledge_ids: []
---

# Practical prompt library

These **100 new examples** support design reviews, SQL reviews, incident investigation, data checks, and documentation. The 17 existing examples in concept guides also use bilingual tabs and multiple lines. Choose a topic, then use its scenario list.

## How to use

1. Choose an example that matches your situation.
2. Select `한국어` or `English`. Tabs with the same label switch together across examples.
3. Copy the prompt and replace `[input fields]` with sanitized material. Use the top language menu to change the surrounding page language.
4. Separate observations, hypotheses, and next checks in the answer. Follow the example's validation steps.

These are newly authored applications of existing handbook concepts. They do not claim measured work frequency, model performance, or executed production work. Source study status and unstudied future topics remain unchanged.

## Browse by topic

| Topic | When to use | New examples |
|---|---|---:|
| [Storage and analytics](foundations.md) | File layout, partitions, and scan cost | 6 |
| [Event architecture](event-architecture.md) | Contracts, schema, duplicates, and delivery | 6 |
| [Lakehouse / Iceberg](lakehouse-iceberg.md) | Snapshots, commits, and maintenance | 6 |
| [Spark](spark.md) | Plans, shuffle, and skew | 6 |
| [Flink](flink.md) | Watermarks, state, and checkpoints | 6 |
| [CDC / Debezium](cdc-debezium.md) | Change order, snapshots, deletes, and recovery | 6 |
| [Orchestration](orchestration.md) | Dependencies, retries, and backfills | 6 |
| [dbt](dbt.md) | Models, incremental processing, tests, and history | 6 |
| [Analytical modeling](analytical-modeling.md) | Grain, joins, dimensions, and metrics | 6 |
| [Trino](trino.md) | Query plans, pushdown, and memory | 6 |
| [Data quality](data-quality.md) | Rules, quarantine, SLOs, and reprocessing | 6 |
| [Data observability](data-observability.md) | Freshness, volume, drift, and alerts | 6 |
| [Lineage and metadata](lineage-metadata.md) | Impact analysis, catalogs, and business meaning | 6 |
| [Governance](governance.md) | Ownership, access, masking, retention, and audit | 6 |
| [AI-ready data](ai-ready-data.md) | Traces, versions, retrieval, and reproducibility | 6 |
| [Online AI evaluation](online-evaluation.md) | Feedback, scores, and trace links | 6 |
| [Knowledge workflow](knowledge-workflow.md) | Extraction, translation review, merging, and evidence | 4 |

## What makes useful context

Provide symptoms, expected behavior, product and connector versions, actual settings, comparison periods, sanitized samples, observed logs and metrics, and fixed constraints. Mark unknown values as unknown. These templates do not authorize production changes. Responsible owners check actual permissions and recovery procedures before acting on a proposal.

[Data platform architecture](../data-platform/architecture.md) · [Study scope](../data-platform/curriculum.md) · [Knowledge workflow](../methodologies/knowledge-workflow.md)
