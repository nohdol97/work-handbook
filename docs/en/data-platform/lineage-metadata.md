---
id: data-platform-lineage-metadata
status: studied
last_updated: 2026-09-27
last_reviewed: 2026-09-27
knowledge_ids:
  - DPE-13-01
  - DPE-13-01A
  - DPE-13-02
  - DPE-13-03
  - DPE-13-04
  - DPE-13-05
  - DPE-13-06
  - DPE-13-07
---

# Chapter 13 — Lineage & Metadata Platform

This Learn page covers the studied roles of metadata, lineage, and catalogs. The datasets are hypothetical. It does not claim that collectors or platforms were built and tested. Metadata describes data. Lineage describes how data is created and used.

**Reading note:** The source core below keeps the original order and form. Read the section-specific corrections, conditions, and additions in the supplement after the source material; some original statements are simplified.

<!-- SOURCE CORE START -->

## 13.1 Metadata Types

Metadata is:

> **Data that describes data.**

### Technical Metadata

- Table
- Column
- Type
- Schema
- Partition
- File format

The question it answers:

> What is the structure?

### Operational Metadata

- Last updated
- Job status
- Freshness
- Row count
- Processing time

The question it answers:

> Is it running normally now?

### Business Metadata

- Description
- Owner
- KPI definition
- Business term
- Classification

The question it answers:

> What does this data mean for the business?

---

## 13.1A Business Metadata vs Semantic Layer

A follow-up question from the source:

> Business metadata looks similar to a semantic layer.

The answer:

> **They overlap, but they are not the same.**

Business metadata:

> Explains the meaning of data.

Example:

```text
Revenue
→ Excludes VAT
→ Excludes refunds
→ Owner: Finance
```

A semantic layer:

> Provides that meaning as computable metric and dimension definitions.

Example:

```text
Revenue
=
SUM(order_amount)
- SUM(refund)
- SUM(vat)
```

The relationship:

```text
Business metadata
→ "What is Revenue?"

Semantic layer
→ "How do we calculate Revenue?"

BI / Dashboard / AI
→ Use the same definition
```

A semantic layer makes the **executable analytical definitions** within business metadata concrete.

---

## 13.2 Dataset Lineage

Dataset lineage describes:

> **Source → Job → Target relationships.**

Example:

```text
raw_user_events
 ↓
Spark Job
 ↓
silver_user_events
 ↓
dbt
 ↓
mart_daily_users
```

### Upstream

The sources and jobs that produce the current data.

### Downstream

The consumers that use the current data.

Uses:

- Root cause investigation
- Impact analysis
- Data trust

---

## 13.3 OpenLineage

OpenLineage is:

> **A standard for expressing lineage information in a common format across data tools.**

Its core entities:

### Job

The work to be done.

### Run

One execution of a specific job.

### Dataset

Input or output data.

Example:

```text
bronze.orders
 ↓
Job: transform_orders
 ↓
silver.orders
```

OpenLineage is a **lineage event standard**, rather than a UI itself.

---

## 13.4 Column-Level Lineage

Column-level lineage shows more detailed relationships than table-level lineage.

Example:

```text
raw_orders.amount ────┐
                      ├→ silver_orders.net_amount
raw_orders.discount ──┘
```

Uses:

- Find the cause of KPI errors
- Assess schema-change impact
- Track sensitive data

---

## 13.5 Impact Analysis

Use lineage to investigate the effects of changes and failures.

### Upstream Analysis

Trace backward to investigate the cause of a problem.

### Downstream Impact Analysis

Follow a change to find the consumers it can affect.

Example:

```text
Type change in raw_orders.amount
 ↓
stg_orders
 ↓
fact_sales
 ↓
mart_daily_sales
 ↓
Dashboard
```

---

## 13.6 Marquez

Marquez is:

> **A lineage system that stores OpenLineage events and supports queries and visualization.**

The relationship:

```text
OpenLineage
→ Standard

Marquez
→ Collection / storage / UI / API
```

Marquez focuses on lineage and run relationships more than the full scope of a catalog.

---

## 13.7 Catalog Integration

A catalog combines information from several sources.

```text
Iceberg
→ Technical metadata

dbt
→ Models / documentation / dependencies

Airflow
→ Pipelines / runs

OpenLineage
→ Lineage

Quality tool
→ Data quality
```

Information a catalog can show:

- Description
- Owner
- Freshness
- Quality
- Upstream / downstream
- Classification
- Access policy

A modern catalog is more than a simple table list:

```text
Discovery
+
Metadata
+
Lineage
+
Governance
```

It is developing into this combination.

---

<!-- SOURCE CORE END -->

## Details to check in practice

### Calculation boundaries in a semantic layer

The Revenue formula is conceptual. It is not an accounting rule or runnable syntax for a specific product.

Before using it, agree on grain, time period, currency, and whether any amount would be subtracted twice. Do not infer an executable calculation from a description alone.

### OpenLineage and collection coverage

OpenLineage defines events and metadata. The object model checked in the official docs also supports job and dataset metadata events that are not tied to a run. Do not assume every lineage event represents one execution. [OpenLineage object model](https://openlineage.io/docs/spec/object-model/)

OpenLineage and [Marquez](https://marquezproject.ai/) descriptions were checked against official docs on 2026-09-24. Installing an integration does not prove that all runs and column lineage are collected. Check actual coverage separately.

### What lineage can prove

An edge in a graph does not prove that a specific run was correct. Lineage can have gaps. Absence from the graph is not proof of no impact.

In the `raw_orders.amount` type-change example, check the expected types in each downstream transformation and consumer.

### Catalog display and policy enforcement

The integration flow in 13.7 explains the roles of information sources. It is not a product configuration that guarantees automatic connections.

Displaying a policy and enforcing data access are different capabilities. [Governance](governance.md) also requires checking query engines and storage access paths.

### Supplemental diagrams of the source flows

```mermaid
flowchart LR
    Raw[raw_user_events] --> Spark[Spark Job]
    Spark --> Silver[silver_user_events]
    Silver --> Dbt[dbt]
    Dbt --> Mart[mart_daily_users]
```

```mermaid
flowchart LR
    Amount[raw_orders.amount] --> Net[silver_orders.net_amount]
    Discount[raw_orders.discount] --> Net
```

## LLM in Practice: review a type change

**Situation:** Review a proposed type change to hypothetical `raw_orders.amount`.

**Context to Give the LLM:** Provide sanitized before-and-after schemas, collected table and column lineage, transformations, job/run history, KPI definitions, and unknown collection coverage.

**Example Prompt:**

=== "English"

    ```text {.prompt}
    [Context]
    Before/after schemas for raw_orders.amount: [proposed type change]
    Table/column lineage and transformations: [sanitized definitions]
    Job/run history, KPI definitions, and known collection gaps: [material]
    [Task]
    Assess this proposed type change before suggesting a redesign.
    List likely downstream impacts and upstream evidence to inspect.
    Separate facts, assumptions, hypotheses, and missing dependencies.
    [Output]
    Give validation checks for stg_orders and fact_sales.
    Include checks for mart_daily_sales and its dashboard.
    [Checks]
    Compare actual SQL, configuration, events, catalog entries, and sample results.
    Do not treat this review as approval or a complete impact analysis.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    raw_orders.amount 전후 schema: [타입 변경안]
    table·column lineage와 변환식: [비식별 정의]
    job/run 이력·KPI 정의·알려진 수집 누락: [자료]
    [요청]
    재설계를 제안하기 전에 이 타입 변경안을 평가하세요.
    downstream 영향 후보와 확인할 upstream 근거를 나열하세요.
    사실·가정·가설·누락 의존성을 구분하세요.
    [출력]
    stg_orders·fact_sales의 검증 항목을 주세요.
    mart_daily_sales와 해당 대시보드의 검증 항목도 주세요.
    [검증]
    실제 SQL·설정·수집 이벤트·catalog·샘플 결과를 대조하세요.
    검토를 변경 승인이나 완전한 영향 분석으로 취급하지 마세요.
    ```

**Expected Output:** A review of affected transformations, KPIs, and dashboards. It should list evidence to check and uncertainty caused by missing lineage.

**What the LLM Can Get Wrong:** It may treat observed lineage as the full dependency graph. It may infer a calculation from a business description alone.

**How to Validate:** Compare real SQL, run configuration, collected events, catalog entries, and sample results. Do not treat an LLM's estimate as change approval or a complete impact analysis.

[Data observability](data-observability.md) · [Governance](governance.md) · [Handbook home](../index.md)

[More practical prompts](../prompts/lineage-metadata.md)
