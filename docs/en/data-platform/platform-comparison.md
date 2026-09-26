---
id: data-platform-platform-comparison
status: studied
last_updated: 2026-09-26
last_reviewed: 2026-09-26
knowledge_ids:
  - DPE2-19-01
  - DPE2-19-02
  - DPE2-19-03
  - DPE2-19-04
  - DPE2-19-05
  - DPE2-19-06
  - DPE2-19-07
  - DPE2-19-08
  - DPE2-19-09
  - DPE2-19-10
  - DPE2-19-11
  - DPE2-19-12
  - DPE2-19-13
  - DPE2-19-14
  - DPE2-19-15
---

# Databricks, Snowflake, and Open Lakehouse

Page type: Decision guide. This page records comparative concepts from Chapter 19. It is not an actual adoption decision, benchmark, or production report. Suitability statements are hypotheses to test with workloads. Product details were checked against official documentation on 2026-09-26.

The options are a Databricks-centered managed Lakehouse, a Snowflake-centered managed data platform, and an Open Lakehouse assembled from open components. An open stack might use `Object storage + Iceberg + Spark + Flink + Trino + Airflow + dbt + OpenLineage + DataHub/OpenMetadata + MLflow/Langfuse`. Compare requirements and operational ownership rather than choosing a universal winner.

## 19.1 Storage Ownership

A common Databricks model is cloud object storage + Delta/Iceberg + Unity Catalog. Snowflake combines its managed-storage history with Iceberg and external-storage options. An open stack offers direct control over S3/ADLS/GCS, Iceberg tables, and metadata architecture.

“Files are in my bucket” differs from “I control lifecycle, catalog, policies, and commits.” Open designs favor direct control. Managed platforms move more operational responsibility to a vendor. Check account, retention, deletion, and external access boundaries in contracts and settings. [Databricks](databricks.md), [Snowflake](snowflake.md).

## 19.2 Iceberg Openness

Engines such as Spark, Flink, Trino, Snowflake, and Databricks can connect to Iceberg tables. The REST Catalog specification defines a catalog interface across languages and engines. [Apache Iceberg REST specification](https://iceberg.apache.org/rest-catalog-spec/).

Move from “Does it support Iceberg?” to **“Which format versions, native features, external readers/writers, and policies remain available?”** Managed Iceberg, Iceberg reads of Delta, and external catalog registration are different configurations. Separate catalog credentials from direct object storage access. [Databricks external access](https://docs.databricks.com/aws/en/external-access), [Snowflake Iceberg](https://docs.snowflake.com/en/user-guide/tables-iceberg).

## 19.3 Compute Model

| Approach | Compute options | Design effect |
|---|---|---|
| Databricks | Spark Runtime, Photon, SQL Warehouse, Serverless Jobs, Model Serving | General data processing and AI integration |
| Snowflake | Virtual Warehouses and serverless services | SQL-centered managed compute |
| Open | Spark batch/ETL, Flink streaming, Trino interactive SQL, vLLM AI serving | Engine choice plus integration responsibility |

Set workload isolation, latency, throughput, and team requirements before adding engines.

## 19.4 Batch

Databricks is a natural candidate for Spark ETL, backfills, large joins, ML dataset creation, and Lakehouse transformation. Snowflake combines warehouse processing around SQL and Dynamic Tables. An open stack can choose Spark, Trino, dbt, and other tools, but must operate them. Treat “strong fit” as a hypothesis. Test actual data size, skew, and reprocessing.

## 19.5 Streaming

Databricks connects Structured Streaming, Lakeflow Pipelines, and Connect to the Lakehouse. Snowflake connects Snowpipe Streaming ingestion, Streams change tracking, and Dynamic Tables refresh. These are not interchangeable stateful streaming engines.

Flink in an open stack is a candidate for low latency, large state, complex event time, and detailed control. This adds checkpoint, state, scaling, and recovery work. Compare ingestion freshness separately from event-time correctness. [Flink](flink.md), [Spark](spark.md).

## 19.6 SQL / BI

Snowflake grew around `BI/Analyst → Virtual Warehouse → Data`. Databricks SQL Warehouse + Photon also serves interactive SQL and BI. An open stack can use `Iceberg → Trino → BI`, with SQL service operations owned by the organization. Compare concurrency, queues, p95 query latency, connectors, and semantic definitions under the same conditions.

## 19.7 Governance

Unity Catalog and Horizon Catalog integrate access, lineage, classification, audit, and Data/AI governance. An open stack can combine Catalog + IAM + OpenLineage + DataHub/OpenMetadata + Policy Engine + Audit. Choice increases, but policy enforcement and authentication integration become platform work.

A product's presence is not proof of security. Test allowed and denied access through queries, file paths, external engines, and AI retrieval. See the [AI Search boundary](databricks.md#1710-ai-vector-capabilities) for its row/column permission limitation.

## 19.8 Lineage

Managed platforms observe their own execution systems. This can help capture `Job → Table → Dashboard` lineage automatically. An open `Kafka → Flink → Spark → dbt → Trino → BI` flow needs standards and connector integration. [OpenLineage](lineage-metadata.md) helps connect these systems. Internal automatic capture does not promise complete coverage of external tools, every column, or all dynamic SQL.

## 19.9 AI Ecosystem

| Approach | Stack and suitability hypothesis |
|---|---|
| Databricks | Lakehouse + MLflow + AI Search + Model Serving + Agents + UC; close links between engineering assets and AI |
| Snowflake | Existing data + Cortex + Search/Analyst + Agents + Horizon; use enterprise data already in the warehouse |
| Open | Iceberg + Vector DB + vLLM + LiteLLM + Langfuse + MLflow + Agent Framework; direct composition and portability |

More freedom adds integration and operations work. Check migration of prompt, agent, retrieval, and evaluation versions, not only model replacement. [AI-ready data](ai-ready-data.md), [Online evaluation](online-evaluation.md).

## 19.10 Portability

Parquet, Iceberg, OpenLineage, and open APIs can make engine replacement easier. Managed platforms also offer open interfaces, especially around Iceberg. Managed workflow definitions, vendor-specific governance policies, serverless behavior, AI services, and proprietary optimizations remain separate dependencies.

**Portable data does not imply a portable operational system.** Separate file-read tests from migration tests for workflows, permissions, recovery, and evaluation history.

## 19.11 Operational Complexity

An open team may operate Kafka, Flink, Spark, Trino, Airflow, Catalog, Lineage, MLflow, Observability, and Security Integration. This needs strong platform skills.

Managed platforms reduce some installation, scaling, upgrades, compatibility management, cross-component authentication, monitoring, and governance integration. Incident response, correctness, and cost management remain. Their value often comes from less integration and operations work rather than one superior engine.

## 19.12 Vendor Lock-in

Do not judge lock-in by table format alone. Review **Data Format → Catalog → Pipeline Definitions → Orchestration → Security Policies → ML Registry → AI Evaluation → Serving → Operational Knowledge** separately.

An Iceberg table may move while vendor pipelines, governance, and AI features need rebuilding. For each layer, record export format, replacement, change cost, and validation. Open systems can also depend on engine-specific behavior and team knowledge.

## 19.13 Total Cost

TCO includes Compute + Storage + Network + Licenses + Platform Engineering Labor + Operations + Upgrades + Incident Response + Security Integration + Governance + Developer Productivity. Do not compare compute-hour prices alone.

Open software can have low direct cost and high labor cost. Managed services can charge more while reducing engineering work. Compare the same workload, SLO, recovery level, retention, and staff time. This page assumes no prices or savings rates.

## 19.14 Comparison table

These are **conditional design hypotheses** that preserve the source's direction. They are not benchmark rankings.

| Area | Databricks | Snowflake | Open Lakehouse |
|---|---|---|---|
| Historical center | Spark / Data / AI | SQL / DWH | Open data architecture |
| Storage | Object + Delta/Iceberg | Managed + Iceberg options | Direct object storage |
| Batch | Spark-centered large processing | SQL-centered processing | Choose Spark and other engines |
| Streaming | Lakehouse integration | Ingestion and incremental refresh | Detailed control with tools such as Flink |
| Interactive SQL | SQL Warehouse | Virtual Warehouse | Trino and other engines |
| Governance | Unity Catalog | Horizon Catalog | Integrate tools and policies |
| ML/AI | Integrated stack | Data-centered AI integration | Direct composition |
| Iceberg | Check table types and features | Check types and catalogs | Can be the base design |
| Portability | Depends on features used | Depends on features used | Can improve with open standards |
| Ops burden | Some work delegated | Some work delegated | More direct operations |
| Vendor dependency | Can grow with platform features | Can grow with platform features | Can decrease, but does not vanish |
| Engineering freedom | Choices within managed boundaries | Choices within managed boundaries | More direct control |

## 19.15 Practical decision heuristics

- Consider Databricks when large ETL, Spark skills, ML/AI, Lakehouse design, and data engineering/AI integration are central.
- Consider Snowflake when SQL analytics, an enterprise warehouse, BI, managed simplicity, and warehouse-centered teams are central.
- Consider Open when multiple engines, infrastructure control, open standards, portability, and custom platform skills matter strategically and the team can handle operations.

Hybrids are normal. Examples are `Kafka/Flink → Iceberg → Databricks + Trino`, or one Iceberg foundation used by Snowflake, Spark, and Trino. Validate catalogs, writers, and policies separately. Aim for **the fewest components that meet real workloads and organizational constraints**, not architectural purity.

## LLM in Practice

### Build evidence for a platform decision

**Situation:** A hypothetical team defines how to choose between managed and open platforms.

**Context to Give the LLM:** Provide sanitized workloads, SLOs, retention and recovery needs, staffing and operating skills, costs, required external engines and policies, and migration constraints.

**Example Prompt:**

=== "English"

    ```text {.prompt}
    [Context]
    Inputs: [workloads, SLOs, retention and recovery needs]
    Constraints: [staff, operating skills, budget evidence, required engines/policies, migration conditions]
    [Task]
    Assess the current problems and required responsibilities first.
    Compare Databricks, Snowflake, Open Lakehouse, and a minimal hybrid.
    Separate portability of storage, table format, catalog, pipelines, security, AI, and operating knowledge.
    [Output]
    Give a requirement table that separates observations, assumptions, and unknowns, plus trade-offs by option.
    List comparable TCO items, minimal proofs of concept, failure criteria, and exit criteria.
    [Checks]
    Do not invent prices, supported features, or benchmarks.
    Specify official docs, real read/write/denied-access tests, and cost/staff-time measurements.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    입력: [workload, SLO, 보존·복구 요구]
    제약: [인력, 운영역량, 예산자료, 필수 엔진·정책, 이관 조건]
    [요청]
    현재 문제와 필요한 책임부터 평가하라.
    Databricks, Snowflake, Open Lakehouse, 최소 hybrid를 비교하라.
    storage, table format, catalog, pipeline, security, AI, 운영 지식의 이식성을 나눠라.
    [출력]
    관찰·가정·미확인을 구분한 요구별 표와 대안별 trade-off를 작성하라.
    동일 조건 TCO 항목, 최소 PoC, 실패·철회 기준을 제시하라.
    [검증]
    단가·지원 기능·benchmark를 만들지 말라.
    공식 문서와 실제 읽기·쓰기·거부 테스트, 측정할 비용·인력시간을 지정하라.
    ```

**Expected Output:** A requirement fit/uncertainty table, lock-in by layer, a comparable TCO measurement plan, minimal proofs of concept, and exit criteria.

**What the LLM Can Get Wrong:** It may name a universal winner or claim full portability from an open table format alone.

**How to Validate:** Check official support tables and real reader/writer and access tests. Measure cost and staff time using the same data, SLOs, and recovery level. Have stakeholders review weights, trade-offs, and unknowns.
