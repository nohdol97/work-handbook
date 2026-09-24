# 제공 자료에서 추출한 커리큘럼

별도의 커리큘럼 파일은 제공되지 않았다. 아래는 원문 Chapter 18을 그대로 추출한 것으로, 복원된 Chapter 1~4의 한계는 source.md 도입부와 정규 curriculum 페이지에 남겼다.

Current Progress and Remaining Curriculum

## 완료

- Phase 1 — Data Engineering Foundations ✅
- Phase 2 — Event Data Architecture ✅
- Phase 3 — Lakehouse / Iceberg ✅
- Phase 4 — Spark ✅
- Phase 5 — Flink ✅
- Phase 6 — CDC / Debezium ✅
- Phase 7 — Orchestration ✅
- Phase 8 — dbt ✅
- Phase 9 — Analytical Data Modeling ✅
- Phase 10 — Trino ✅
- Phase 11 — Data Quality Engineering ✅
- Phase 12 — Data Observability ✅
- Phase 13 — Lineage & Metadata Platform ✅
- Phase 14 — Data Governance ✅
- Phase 15 — AI-Ready Data ✅

## 진행 중

### Phase 16 — AI Evaluation Data Platform

완료:

- 16.1 Online Evaluation Events ✅

남은 항목:

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

---

## 이후 남은 Phase

### Phase 17 — Databricks Deep Dive

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

### Phase 18 — Snowflake Deep Dive

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

### Phase 19 — Databricks vs Snowflake vs Open Lakehouse

Compare:

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

### Phase 20 — Production Data Platform Engineering

- Backfills
- Reprocessing
- Incident Drills
- Capacity Planning
- Cost Engineering
- DR / Recovery
- Data Platform SLOs

### Phase 21 — Final End-to-End Project

Target Architecture:

```text
Applications
    ↓
Kafka
    ↓
Flink / Spark Streaming
    ↓
Bronze Iceberg
    ↓
Spark / dbt
    ↓
Silver
    ↓
Gold
    ↓
Trino / BI / AI Evaluation

PostgreSQL
    ↓
Debezium
    ↓
Kafka
```

Around it:

```text
Airflow
→ Orchestration

Data Quality
→ Trust

OpenLineage
→ Lineage

Catalog
→ Discovery / Governance

Data Observability
→ Freshness / Correctness

Langfuse
→ AI Telemetry / Evaluation
```

최종적으로 설명할 수 있어야 할 질문:

- 왜 각 Component가 존재하는가?
- Failure 시 어떻게 동작하는가?
- Backfill은 어떻게 하는가?
- Consistency Model은 무엇인가?
- Scale은 어떻게 하는가?
- Cost는 어디서 발생하는가?
- Data Contract는 어떻게 적용하는가?
- SLO는 어떻게 정의하는가?
- Recovery는 어떻게 하는가?
- 규모가 작다면 어떤 Component를 제거할 수 있는가?

---
