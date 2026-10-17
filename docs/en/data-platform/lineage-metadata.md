---
id: data-platform-lineage-metadata
status: studied
last_updated: 2026-10-18
last_reviewed: 2026-10-18
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

This chapter covers the roles of metadata, lineage, and catalogs. The datasets are hypothetical. It does not claim that collectors or platforms were built and tested. Metadata describes data. Lineage describes how data is created and used.

<!-- SOURCE CORE START -->

## 13.1 Metadata Types

Metadata describes data much like a book’s title, author, and category describe a book. Data structure, recent runs, and business meaning are different kinds of metadata. Check them together before use. For `orders.amount`, knowing the type is not enough; also check its last update and whether it contributes to revenue.

Metadata is:

> **Data that describes data.**

### Technical Metadata

- Table
- Column
- Type
- Schema
- Partition
- File format

Technical metadata answers:

> What is the structure?

### Operational Metadata

- Last updated
- Job status
- Freshness
- Row count
- Processing time

Operational metadata answers:

> Is it running normally now?

### Business Metadata

- Description
- Owner
- KPI definition
- Business term
- Classification

Business metadata answers:

> What does this data mean for the business?

---

## 13.1A Business Metadata vs Semantic Layer

Business metadata says what a metric means. A semantic layer helps queries reuse the same calculation definition. It is like the difference between describing “revenue” on a recipe card and specifying the ingredients and calculation steps. The formula below is conceptual, not an accounting rule or ready-to-run SQL.

A question raised during study:

> Business metadata looks similar to a semantic layer.

Both concepts describe meaning, but they serve different uses:

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

A semantic layer turns business meaning into **calculation definitions** that queries can reuse.

The Revenue formula is conceptual. It is not an accounting rule or runnable syntax for a specific product.

Before using it, agree on grain, time period, currency, and whether any amount would be subtracted twice. Do not infer an executable calculation from a description alone.

---

## 13.2 Dataset Lineage

Lineage records the route from source data through jobs to the outputs that use it. If water from a tap looks wrong, trace the pipes backward; before changing a pipe, check which taps it serves. If daily user counts look wrong on a dashboard, trace that route backward to source events and transformations. Before a change, follow it forward to likely consumers.

Dataset lineage shows:

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

The source data and jobs that produced this dataset.

### Downstream

The jobs and users that read or depend on this dataset.

Uses:

- Root cause investigation
- Impact analysis
- Data trust

---

## 13.3 OpenLineage

OpenLineage is a standard for sharing lineage information between tools. A job defines work, a run is one execution, and a dataset is an input or output. Some job and dataset metadata events do not belong to one run. Even with the standard, check what each integration actually collects.

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

OpenLineage defines a **lineage event format**; it is not the screen used to view results.

OpenLineage defines events and metadata. The object model checked in the official docs also supports job and dataset metadata events that are not tied to a run. Do not assume every lineage event represents one execution. [OpenLineage object model](https://openlineage.io/docs/spec/object-model/)

OpenLineage and [Marquez](https://marquezproject.ai/) descriptions were checked against official docs on 2026-09-24. Installing an integration does not prove that all runs and column lineage are collected. Check actual coverage separately.

---

## 13.4 Column-Level Lineage

Column-level lineage goes beyond “which table was read?” to “which input columns produced this output column?” If `net_amount` uses `amount` and `discount`, review changes to both source columns. Uncollected SQL or dynamic transformations can leave gaps in the graph.

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

Impact analysis checks where a change or incident began and which consumers it might reach. Upstream means tracing back toward a cause; downstream means following results to consumers. Before approving a type change, check actual SQL and expected consumer types as well as the graph.

### Upstream Analysis

Trace backward through sources and transformations to investigate a cause.

### Downstream Impact Analysis

Follow changed data through transformations to find likely consumers.

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

An edge in a graph does not prove that a specific run was correct. Lineage can have gaps. Absence from the graph is not proof of no impact.

In the `raw_orders.amount` type-change example, check the expected types in each downstream transformation and consumer.

---

## 13.6 Marquez

Marquez collects OpenLineage information so users can explore the links between runs and datasets. Like a road standard and a map, OpenLineage defines an event format while Marquez is one collection and viewing tool. Installing it does not prove that every run or column link was captured.

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

A catalog is a searchable guide to metadata from several sources. Before using a new metric, check its description, owner, quality, and upstream and downstream paths together. A policy displayed in the catalog is not automatically enforced by every query engine or direct storage path.

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

The integration flow in 13.7 explains the roles of information sources. It is not a product configuration that guarantees automatic connections.

Displaying a policy and enforcing data access are different capabilities. [Governance](governance.md) also requires checking query engines and storage access paths.

---

<!-- SOURCE CORE END -->

## Chapter key points

- Metadata describes meaning and state. Lineage traces how data is produced and used.
- Before changing a type or metric, check upstream evidence and downstream consumers.
- A catalog graph alone cannot prove complete collection, correct execution, or policy enforcement.

## LLM in Practice: review a type change

**Prompt:**

=== "English"

    ```text {.prompt}
    Review a proposed type change to hypothetical `raw_orders.amount`.
    Assess this proposed type change before suggesting a redesign.
    List likely downstream impacts and upstream evidence to inspect.
    Separate facts, assumptions, hypotheses, and missing dependencies.
    Review the material; do not apply changes.
    ```

=== "한국어"

    ```text {.prompt}
    가상의 `raw_orders.amount` 타입 변경을 검토한다.
    재설계를 제안하기 전에 이 타입 변경안을 평가하세요.
    downstream 영향 후보와 확인할 upstream 근거를 나열하고, 사실·가정·누락 의존성을 구분하세요.
    자료를 검토하되 실제 변경은 실행하지 마.
    ```

**Key point:** A review of affected transformations, KPIs, and dashboards. It should list evidence to check and uncertainty caused by missing lineage. It may treat observed lineage as the full dependency graph. It may infer a calculation from a business description alone. Compare real SQL, run configuration, collected events, catalog entries, and sample results. Do not treat an LLM's estimate as change approval or a complete impact analysis.

[Data observability](data-observability.md) · [Governance](governance.md) · [Handbook home](../index.md)

[More practical prompts](../prompts/lineage-metadata.md)
