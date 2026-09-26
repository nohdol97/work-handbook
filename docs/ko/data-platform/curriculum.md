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

# 학습 범위와 완료 현황

## 출처와 학습 깊이

이 문서는 제공된 Data Platform Engineering 학습 노트의 진행 상태를 보존한다. 원문은 기술의 필요성, 해결하는 문제, 핵심 기능, 기술 간 연결·차이, 전체 구조에서의 위치를 설명하는 수준을 목표로 한다. 내부 구현 심화나 실무 구축 완료를 뜻하지 않는다.

원문은 Chapter 1~4를 이전에 완료한 학습 범위에 맞춰 **복원한 노트**, Chapter 5 이후를 실제 이어서 학습한 흐름이라고 명시한다. 원래 대화나 복원 이전 자료는 제공되지 않아 복원의 정확성을 별도로 확인하지 못했다. 아래 “완료”는 제공 자료의 학습 상태다.

첫 자료의 Chapter 17은 보충 설명, Chapter 18은 당시 진행 현황이다. 2026-09-26 추가 자료의 Chapter 16~21은 아래 Phase 번호에 대응하며 **Phase 1~21의 개념 학습 완료**를 명시한다. 첫 자료의 미학습 표시는 당시 이력으로 보존하고 현재 상태는 이번 자료로 갱신했다.

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

## 완료: Phase 16 — AI 평가 데이터 플랫폼

[16.1 온라인 평가](online-evaluation.md)와 [16.2~16.12 AI 평가 플랫폼](ai-evaluation.md)을 개념 학습했다. 새 자료의 예시·숫자·버전 표는 학습용이며 실제 모델 평가 실행 결과가 아니다.

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
- 16.12 버전별 관리 위치와 bundle 연결

## 완료: Phase 17 — Databricks Deep Dive

상태: **studied — 개념 학습 완료**. [Databricks](databricks.md)에 제공된 내용을 정리했다. 제품별 공식 문서 확인은 실제 배포·성능 시험을 대신하지 않는다.

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

## 완료: Phase 18 — Snowflake Deep Dive

상태: **studied — 개념 학습 완료**. [Snowflake](snowflake.md)에 제공된 내용을 정리했다. 새 자료는 condensed 요약 범위이며 내부 구현 심화를 주장하지 않는다. 제품별 공식 문서 확인은 실제 배포·성능 시험을 대신하지 않는다.

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

## 완료: Phase 19 — Databricks vs Snowflake vs Open Lakehouse

상태: **studied — 개념 학습 완료**. [플랫폼 비교](platform-comparison.md)에 제공된 내용을 정리했다. 제품별 공식 문서 확인은 실제 배포·성능 시험을 대신하지 않는다.

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

## 완료: Phase 20 — Production Data Platform Engineering

상태: **studied — 개념 학습 완료**. [운영 엔지니어링](production-operations.md)에 제공된 내용을 정리했다. 장애 사례는 개념 시나리오이며 실제 drill 결과가 아니다. 제품별 공식 문서 확인은 실제 배포·성능 시험을 대신하지 않는다.

- Backfills
- Reprocessing
- Incident Drills
- Capacity Planning
- Cost Engineering
- DR / Recovery
- Data Platform SLOs

## 완료: Phase 21 — 최종 End-to-End 아키텍처

상태: **studied — 아키텍처 개념 통합 완료**. 학습 구조는 [전체 구조](architecture.md)의 Applications → Kafka → Flink/Spark Streaming → Bronze Iceberg → Spark/dbt → Silver → Gold → Trino/BI/AI Evaluation 흐름과 PostgreSQL → Debezium → Kafka 경로다.

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

새 자료는 구성 요소별 존재 이유, 실패 동작, 보장 경계, backfill, 확장·비용, 작은 규모의 생략 후보, open/managed 대안, 7개 설계 원칙을 제공한다. 모두 [전체 구조](architecture.md)에 통합했다.

구축·장애 실험·성능 측정 자료는 아직 없다. 완료는 overview curriculum의 개념 이해 범위이며 운영 숙련도를 인증하지 않는다. 학습자는 OLTP/OLAP·Parquet·object storage·Iceberg, Spark/Flink·Kafka/CDC, Airflow/dbt/Trino·분석 모델, 품질/관측·metadata/lineage/catalog/governance, AI-ready 데이터·telemetry/evaluation/versioning·Langfuse/MLflow, managed 통합과 open 대안, 복구·규모별 단순화의 역할을 설명하는 것을 목표로 한다.

## 제품 근거의 범위

후속 원문은 Unity Catalog, Lakeflow Jobs, managed Delta/Iceberg, Iceberg REST Catalog, Dynamic Tables, Horizon Catalog, Snowflake Iceberg 공식 문서를 참고했다고 기록하지만 URL·버전·조회일은 제공하지 않는다. 따라서 현재 공식 근거는 각 제품 정규 페이지에서 별도로 확인하고 날짜·제약을 표시했다. 실제 cloud·region·edition·버전·설정은 적용 전에 확인한다.

[전체 구조](architecture.md) · [홈](../index.md)
