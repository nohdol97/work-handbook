---
id: data-platform-governance
status: studied
last_updated: 2026-10-18
last_reviewed: 2026-10-18
knowledge_ids:
  - DPE-14-01
  - DPE-14-02
  - DPE-14-03
  - DPE-14-04
  - DPE-14-05
  - DPE-14-06
  - DPE-14-07
  - DPE-14-08
  - DPE-14-09
---

# Chapter 14 — Data Governance

This chapter covers ownership, policy, access, and audit. Durations and datasets are hypothetical. It does not claim that security policies were deployed or legal duties were verified. Governance asks, “Who may use this data, and under which conditions?”

<!-- SOURCE CORE START -->

## 14.1 Dataset Ownership

Ownership names who decides and fixes things when a dataset fails or its meaning changes. The technical owner handles pipelines and schemas; the business owner handles metric meaning and use. If teams disagree about an order count, both the source processing and the aggregation definition need owners.

### Technical Owner

- Pipeline
- Schema
- Quality
- SLO

### Business Owner

- Meaning
- KPIs
- Business definitions

Without owners, it is unclear who fixes an error or approves a change in meaning.

---

## 14.2 Classification

Classification labels importance and sensitivity so access, masking, and retention rules can use them. Like library materials with different borrowing rules, email addresses and ordinary team codes need different handling. PII (personally identifiable information) is a data type, not one step on a universal importance scale; it can sit beside another classification.

Examples:

- Public
- Internal
- Confidential
- PII
- Sensitive

Classify sensitive columns as well as whole tables.

Example:

```text
email → PII
team_id → Internal
```

Use these classifications when setting access, masking, and retention policies.

Public, Internal, Confidential, PII, and Sensitive are not a single ordered scale shared by every organization. PII describes the kind of data and can be used alongside an importance level.

---

## 14.3 Retention Policies

Set a retention period by weighing reprocessing and analysis needs against cost and exposure. The periods below are teaching examples. Set actual periods after checking legal, contract, business, and deletion requirements.

Retention defines:

> **How long data is kept.**

Consider:

- Cost
- Legal and regulatory requirements
- Sensitivity
- Analytical value

Example:

```text
Debug log → 14 days
User event → 1 year
Aggregated metrics → Long-term storage
```

Storage may use fast, lower-cost, and archive tiers based on how often data is read.

Decide when old Iceberg snapshots expire as part of the retention policy.

---

## 14.4 Deletion Policies

Logical deletion marks records so queries can exclude them. Physical deletion also addresses removal of stored data. An order absent from the current screen may still have copies in old snapshots, Kafka logs, or backups. Define which copies a deletion request covers before judging completion.

Deletion defines:

> **When, where, and how data is actually removed.**

Deleting the source can leave copies in transport logs and derived tables.

```text
PostgreSQL
 ↓
Kafka
 ↓
Bronze
 ↓
Silver
 ↓
Gold
 ↓
Backup
```

Check every copy and derived dataset in the deletion scope.

### Logical Delete

Mark a record as deleted.

### Physical Delete

Actually remove it.

In Iceberg, an older snapshot may still reference files absent from the current snapshot.

Consider older snapshots and file cleanup too.

Distinguish snapshot retention from source-data retention requirements. Data absent from the current snapshot may still be referenced by older snapshots.

- Snapshot expiration relates to cleanup of files no longer needed by retained snapshots.
- Orphan cleanup handles files that metadata does not reference.
- Choose a retention interval that avoids mistaking files from active writes for orphans.

Current query results alone do not prove physical deletion. [Iceberg maintenance](https://iceberg.apache.org/docs/latest/maintenance/)

---

## 14.5 Masking

Masking hides sensitive values when users see data. For example, an analyst may see only part of an `email` value. Static masking stores a separately masked copy; dynamic masking changes query output by user or role. Encryption protects data in a different way and at different points.

### Static Masking

Store masked values in a separate copy.

### Dynamic Masking

Show different values based on the querying user or role.

The link to classification:

```text
PII
 ↓
Masking policy
```

AI prompts and responses can contain personal data, so check whether masking is needed on those paths too.

Masking hides displayed values; encryption protects data in storage or transit. They serve different purposes.

---

## 14.6 Row / Column Access

Row access asks “which records may this user see?” Column access asks “which fields?” A user might see orders for their team while the email column is blocked or masked. RBAC (Role-Based Access Control) groups permissions by role. Test allowed and denied behavior across real access paths.

### Row-Level Access

Limit which rows a user or team can see.

### Column-Level Access

Restrict access to a sensitive column itself.

The difference from masking:

```text
Column access
→ The column cannot be read

Masking
→ The column is visible, but its values are hidden
```

### RBAC

Group privileges by role instead of granting each user permission one by one.

A policy shown in a catalog does not prove protection across every external engine and storage path.

Databricks row filters and column masks have runtime, compute, and API limits. The checked documentation describes unsupported path-based and certain REST API access to tables with these policies. [Databricks filters and masks](https://docs.databricks.com/aws/en/data-governance/unity-catalog/filters-and-masks)

---

## 14.7 Auditability

Audit records who used or changed data and policies, and when. Observability asks whether data is healthy; audit asks who did what. For example, investigating denied access may require both the user privilege and the policy change record at that time. Audit logs can themselves be sensitive.

Access audit:

```text
user
dataset
time
action
query
```

Change audit:

- Schema changes
- Policy changes
- Owner changes
- Retention changes

The difference from observability:

```text
Observability
→ Are the system and data healthy?

Audit
→ Who did what?
```

Real users and queries in audit logs can be sensitive. Do not copy them directly into public learning material.

---

## 14.8 Data Contracts

A data contract is an agreement between producers and consumers about format, meaning, quality, and ownership. A delivery slip that lists only box size but omits the contents, quantity, and owner leaves the recipient guessing. Calling `latency_ms` an integer does not say which unit it uses or whether negative values are valid. Check the contract before changes so consumers are less likely to receive unexpected results.

It can include:

- Schema
- Semantics
- Quality
- SLO
- Ownership
- Version

Example:

```text
event_id
→ required + unique

latency_ms
→ integer
→ millisecond
→ >= 0

Freshness
→ < 5 min

Owner
→ AI Platform Team
```

It covers business meaning and quality responsibility as well as schema shape.

`email` and `team_id` are example field names, with no real organizational identifiers. The data contract's owner is a hypothetical team. Five minutes is not an approved operational SLO.

An integer type alone does not define a unit. The contract also states milliseconds and the non-negative rule.


---

## 14.9 Governance Platforms

Governance platforms combine catalogs, permissions, lineage, and audits to help operate policies. The products below address similar questions, but they do not promise identical behavior across engines, access paths, or editions. Test policy enforcement through actual query and storage paths before choosing one.

### Databricks Unity Catalog

The broad scope:

- Catalog / discovery
- Access control
- Row / column control
- Masking
- Classification
- Lineage
- Audit
- Data / AI governance

Think of it as the central governance layer for the Databricks lakehouse.

### AWS Lake Formation

Governance centered on AWS S3 data lakes.

- Glue Data Catalog
- Table / column / row permissions
- Integration with AWS analytics services

### Snowflake Horizon Catalog

Governance centered on Snowflake.

- Catalog
- Classification
- Tags
- Masking
- Row access
- Access history
- Lineage
- Data quality / AI governance

The three products help answer these questions:

```text
What is this data?
Who owns it?
Who may see it?
Is it sensitive?
Where did it come from?
Where is it used?
Who accessed it?
Is it healthy?
```

Product descriptions are a category-level comparison checked against official docs on 2026-09-24. No platform was deployed, and not every feature was tested.

- **Unity Catalog:** Separate broad capabilities from detailed runtime and access-path limits. [Official overview](https://docs.databricks.com/aws/en/data-governance/unity-catalog/)
- **Lake Formation:** Check data-filter support by integrated engine and service. [Data filtering](https://docs.aws.amazon.com/lake-formation/latest/dg/data-filtering.html)
- **Horizon Catalog:** Check edition and individual feature requirements. For example, Access History requires Enterprise Edition or higher. [Horizon Catalog](https://docs.snowflake.com/en/user-guide/snowflake-horizon), [Access History](https://docs.snowflake.com/en/user-guide/access-history)

The three products do not enforce every policy in the same way or scope.

---

<!-- SOURCE CORE END -->

## Chapter key points

- Owners, classifications, and retention periods define responsibility for access and deletion.
- Masking, row and column permissions, and audits serve different needs: limit exposure, decide access, and trace use.
- Distinguish logical from physical deletion. Check real copies and access paths, including snapshots and exports.

## LLM in Practice: review copies covered by deletion

**Prompt:**

=== "English"

    ```text {.prompt}
    Review a deletion policy for a hypothetical dataset to avoid missing source and derived copies.
    Review this deletion policy; do not execute deletion.
    Separate logical deletion, physical cleanup, and unverified scope.
    Inspect copies across PostgreSQL, Kafka, Bronze, Silver, Gold, and backups.
    Separate facts, assumptions, risks, and missing evidence.
    Review the material; do not apply changes.
    ```

=== "한국어"

    ```text {.prompt}
    가상 데이터셋에 삭제 정책을 설계하며 원본과 파생 사본을 빠뜨리지 않는지 확인한다.
    삭제 정책을 검토하되 삭제는 실행하지 마세요.
    논리 삭제·물리 정리·미검증 범위를 구분하세요.
    PostgreSQL·Kafka·Bronze·Silver·Gold·backup의 사본을 조사하세요.
    사실·가정·위험·누락 근거를 구분하세요.
    자료를 검토하되 실제 변경은 실행하지 마.
    ```

**Key point:** A list of copies to trace, questions for owners, a distinction between logical deletion and physical cleanup, and scope without completion evidence. It may assume that data is deleted because current queries cannot see it. It may mistake hypothetical retention periods for legal rules. Check actual storage, snapshot references, backup policies, consumer state, and approved retention and deletion policies. The responsible owners verify legal requirements. The LLM helps review; it does not replace policy approval or evidence of deletion.

[Lineage and metadata](lineage-metadata.md) · [Data quality](data-quality.md) · [Data observability](data-observability.md) · [Handbook home](../index.md)

[More practical prompts](../prompts/governance.md)
