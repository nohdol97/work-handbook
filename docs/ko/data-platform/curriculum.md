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

# 학습 범위와 남은 커리큘럼

## 출처와 학습 깊이

이 문서는 제공된 Data Platform Engineering 학습 노트의 진행 상태를 보존한다. 원문은 기술의 필요성, 해결하는 문제, 핵심 기능, 기술 간 연결·차이, 전체 구조에서의 위치를 설명하는 수준을 목표로 한다. 내부 구현 심화나 실무 구축 완료를 뜻하지 않는다.

원문은 Chapter 1~4를 이전에 완료한 학습 범위에 맞춰 **복원한 노트**, Chapter 5 이후를 실제 이어서 학습한 흐름이라고 명시한다. 원래 대화나 복원 이전 자료는 제공되지 않아 복원의 정확성을 별도로 확인하지 못했다. 아래 “완료”는 제공 자료의 학습 상태다.

원문 목차의 Chapter 17은 보충 설명, Chapter 18은 진행 현황이다. 아래 **Phase 17~21**은 앞으로 학습할 과정이며 그 Chapter 번호와 구분한다.

## 완료: Phase 1~15

1. [기초](foundations.md) — 개념 학습 완료.
2. [이벤트 아키텍처](event-architecture.md) — 개념 학습 완료.
3. [Lakehouse / Iceberg](lakehouse-iceberg.md) — 개념 학습 완료.
4. [Spark](spark.md) — 개념 학습 완료.
5. [Flink](flink.md) — 개념 학습 완료.
6. [CDC / Debezium](cdc-debezium.md) — 개념 학습 완료.
7. [Orchestration](orchestration.md) — 개념 학습 완료.
8. [dbt](dbt.md) — 개념 학습 완료.
9. [분석 데이터 모델링](analytical-modeling.md) — 개념 학습 완료.
10. [Trino](trino.md) — 개념 학습 완료.
11. [데이터 품질](data-quality.md) — 개념 학습 완료.
12. [데이터 관측](data-observability.md) — 개념 학습 완료.
13. [계보와 메타데이터](lineage-metadata.md) — 개념 학습 완료.
14. [거버넌스](governance.md) — 개념 학습 완료.
15. [AI-ready 데이터](ai-ready-data.md) — 개념 학습 완료.

## 진행 중: Phase 16

[16.1 Online Evaluation Events](online-evaluation.md)만 학습 완료다. 아래 항목은 **not-started**이며, AI-ready 문서에서 일부 개념을 언급했더라도 별도 과정의 학습 완료를 뜻하지 않는다.

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

## 미학습: Phase 17 — Databricks Deep Dive

상태: **not-started**. 아래는 원문이 제시한 후속 학습 목차다. 제품 기능을 검증하거나 과정을 완료했다는 주장이 아니다.

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

## 미학습: Phase 18 — Snowflake Deep Dive

상태: **not-started**. 아래는 원문이 제시한 후속 학습 목차다. 제품 기능을 검증하거나 과정을 완료했다는 주장이 아니다.

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

## 미학습: Phase 19 — Databricks vs Snowflake vs Open Lakehouse

상태: **not-started**. 아래는 원문이 제시한 후속 학습 목차다. 제품 기능을 검증하거나 과정을 완료했다는 주장이 아니다.

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

## 미학습: Phase 20 — Production Data Platform Engineering

상태: **not-started**. 아래는 원문이 제시한 후속 학습 목차다. 제품 기능을 검증하거나 과정을 완료했다는 주장이 아니다.

- Backfills
- Reprocessing
- Incident Drills
- Capacity Planning
- Cost Engineering
- DR / Recovery
- Data Platform SLOs

## 미학습: Phase 21 — 최종 End-to-End 프로젝트

상태: **not-started**. 목표는 [전체 구조](architecture.md)의 Applications → Kafka → Flink/Spark Streaming → Bronze Iceberg → Spark/dbt → Silver → Gold → Trino/BI/AI Evaluation 흐름과 PostgreSQL → Debezium → Kafka 경로다.

주변 기능은 Airflow orchestration, data quality, OpenLineage, catalog/discovery/governance, data observability의 freshness/correctness, Langfuse AI telemetry/evaluation이다. 구현 전후 다음 질문에 근거를 붙일 수 있어야 한다.

1. 각 구성 요소는 왜 존재하는가?
2. 장애가 나면 어떻게 동작하는가?
3. Backfill은 어떻게 하는가?
4. Consistency model은 무엇인가?
5. 어떻게 확장하는가?
6. 비용은 어디서 발생하는가?
7. Data contract는 어떻게 적용하는가?
8. SLO는 어떻게 정의하는가?
9. Recovery는 어떻게 하는가?
10. 규모가 작으면 어떤 구성 요소를 제거할 수 있는가?

설계·구축·장애 실험·성능 측정 자료는 아직 없다. 다음 원문이 들어오면 해당 범위를 보완하고 학습 상태를 갱신한다.

[전체 구조](architecture.md) · [홈](../index.md)
