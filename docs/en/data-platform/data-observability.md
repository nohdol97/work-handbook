---
id: data-platform-data-observability
status: studied
last_updated: 2026-10-18
last_reviewed: 2026-10-18
knowledge_ids:
  - DPE-12-01
  - DPE-12-02
  - DPE-12-03
  - DPE-12-04
  - DPE-12-05
  - DPE-12-06
  - DPE-12-07
---

# Chapter 12 — Data Observability

This chapter covers continuous measurement of data health. The numbers and incidents are learning examples, not measurements or hands-on experience. Data quality defines expected conditions. Observability helps show the current state and locate where a problem starts.

<!-- SOURCE CORE START -->

## 12.1 Data Freshness

Freshness asks whether data arrived by the time it is needed. A parcel has pickup, sorting, and delivery times. Data likewise has event, collection, processing, and dashboard refresh times. Define which clock makes data “late” before locating the delay.

### Source Freshness

Were source events created and collected by the needed time?

### Pipeline Freshness

Compare processing times from Kafka through Bronze, Silver, and Gold to locate a delay.

### Downstream Freshness

Do dashboards and BI actually show the newly processed data?

Comparing update times at each stage helps narrow down where delay began.

Event time, collection time, processing completion time, and screen refresh time are different measurements. Define which timestamps to compare before using them in operations.

---

## 12.2 Volume Monitoring

Volume monitoring checks whether counts are unusually low or high. A total order count can look normal while today’s partition is empty. Compare with baselines such as the same weekday or season to avoid treating a normal weekend drop as an incident.

Look for row counts that suddenly fall or rise compared with normal levels.

Possible causes of a decrease:

- Collection failure
- Producer problem
- Filter bug

Possible causes of an increase:

- Duplicates
- Replay
- Retry storm
- Traffic spike

A missing partition is another sign of a count problem.

Do not rely on one fixed number. Compare counts with:

- Recent averages
- The same weekday
- Seasonal patterns

Compare counts with baselines such as these.

An absolute threshold alone can flag a normal weekend decline. A total count can hide a missing partition.

The listed causes of decreases and increases are hypotheses. A volume change alone does not prove one. When the FAILED rate changes, check whether failures really increased or the way status is recorded changed.

Connect schema changes to [lineage](lineage-metadata.md) to help find affected consumers. If a job is late, check data health too. Find which datasets and users are affected.

---

## 12.3 Schema Monitoring

A schema is the agreement about columns, types, and required values. If a producer changes the type of `amount`, transformation SQL or dashboards may fail. After detecting the change, use [lineage](lineage-metadata.md) to find likely consumers.

Watch for these changes:

- Column addition
- Column removal
- Rename
- Type change
- Nullable change

A change that violates the expected structure can make downstream queries fail.

After detecting a schema change, use lineage to find likely datasets and consumers.

---

## 12.4 Distribution Drift

Distribution drift means the mix or range of values changes even when the row count does not. If the `FAILED` rate rises from 5% to 45%, investigate both real failures and changes in status recording. The change is a signal, not proof of its cause.

The total row count can stay normal while the mix or range of values changes.

Common signs of change:

- Null rate drift
- Cardinality drift
- Value distribution drift
- Numeric distribution drift

Example:

```text
Usual FAILED rate = 5%
Today's FAILED rate = 45%
```

A normal total count does not prove that the data contents are healthy.

---

## 12.5 Pipeline Health vs Data Health

Pipeline health asks whether a job ran; data health asks whether its output is usable. A delivery truck can arrive with an empty box. If a successful Gold job produces zero rows, check filters, source data, and partitions.

Pipeline health:

- Job status
- Kafka lag
- Runtime
- CPU and memory
- Failures

Data health:

- Freshness
- Volume
- Schema
- Nulls
- Duplicates
- Distributions

The key idea:

> **Green pipeline ≠ healthy data.**

A successful job can return zero rows because its query logic is wrong.

---

## 12.6 Data SLIs / SLOs

Compare the measured value and target over the same window. `Volume = 98M` alone cannot show whether a target is met. Define the period, partitions, and normal baseline. Use the same definitions when continuously measuring [quality rules](data-quality.md).

Data observability measures data health repeatedly over time.

Example SLIs:

```text
Freshness = 3 minutes
NULL rate = 0.5%
Volume = 98M
```

Example SLOs:

```text
Freshness < 5 minutes
NULL rate < 1%
Volume deviation < 20%
```

Check several signals together because one may look healthy while another does not.

Volume = 98M alone cannot show whether the deviation target is met. You need a baseline and a measurement window.

Define several signals for the dataset's business purpose. Share definitions with [quality SLOs](data-quality.md) so that measurement and response agree.

---

## 12.7 Alert Design

A useful alert says what failed, for how long, and where to look first. For example, “today’s `gold_orders` partition has been empty for 20 minutes” gives more direction than “low count.” Alerts that repeat near a threshold add work, so include duration and impact in the design.

The goal:

> **Report problems worth acting on, rather than maximizing alert count.**

### Noisy Alert

ALERT and RECOVERY repeat near the threshold.

### Actionable Alert

The alert makes it clear where to investigate.

A useful alert includes:

```text
Threshold
+
Duration
+
Severity
+
Context
```

Warning and Critical can use different levels.

Alert policies can also vary by dataset importance tier.

Keep repeated or low-value alerts from hiding important problems.

- **Threshold:** Which condition failed?
- **Duration:** How long has it lasted?
- **Severity:** How large is the impact?
- **Context:** Which dataset, partition, stage, owner, and related run should be checked?

Define duration and context to reduce alert fatigue. Check that this does not hide important signals.

---

<!-- SOURCE CORE END -->

## Chapter key points

- Freshness, counts, schemas, and distributions can reveal data problems even when jobs succeed.
- Define timestamps, windows, and baselines before treating a change as abnormal.
- Set SLIs and SLOs for the dataset's purpose. Include impact and next checks in alerts.

## LLM in Practice: investigate empty output from a successful job

**Prompt:**

=== "English"

    ```text {.prompt}
    The Gold job succeeded, but today's dashboard data has zero rows.
    Investigate this hypothetical incident before suggesting a redesign.
    Separate facts, assumptions, hypotheses, and missing evidence.
    Do not infer a root cause from correlation alone.
    Review the material; do not apply changes.
    ```

=== "한국어"

    ```text {.prompt}
    Gold 작업은 성공했는데 대시보드의 오늘 데이터가 0 rows다.
    재설계를 제안하기 전에 이 가상 장애를 조사하세요.
    사실·가정·가설·누락 근거를 구분하고 상관관계만으로 근본 원인을 단정하지 마세요.
    자료를 검토하되 실제 변경은 실행하지 마.
    ```

**Key point:** Checks that separate missing source data, missing partitions, filter errors, and delayed downstream refresh. It may treat a green job as evidence of healthy data. It may inspect only total counts and miss a missing partition. Check actual query results and timestamps at each stage, change history, and dashboard refresh state. Confirm the LLM's hypotheses with evidence before acting.

[Data quality](data-quality.md) · [Lineage and metadata](lineage-metadata.md) · [Handbook home](../index.md)

[More practical prompts](../prompts/data-observability.md)
