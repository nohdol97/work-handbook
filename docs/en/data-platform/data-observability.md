---
id: data-platform-data-observability
status: studied
last_updated: 2026-09-24
last_reviewed: 2026-09-24
knowledge_ids:
  - DPE-12-01
  - DPE-12-02
  - DPE-12-03
  - DPE-12-04
  - DPE-12-05
  - DPE-12-06
  - DPE-12-07
---

# Data observability

This Learn page covers continuous measurement of data health. The numbers and incidents are learning examples, not measurements or hands-on experience. Data quality defines expected conditions. Observability helps show the current state and locate where a problem starts.

## Split freshness by stage

| Stage | Question | Scope |
| --- | --- | --- |
| Source freshness | Is the source created and collected on time? | Source creation and collection |
| Pipeline freshness | Where does processing delay grow? | Kafka → Bronze → Silver → Gold |
| Downstream freshness | Does the user see current data? | Dashboards and BI |

Compare timestamps by stage to find where delay starts. For operational use, distinguish event time, collection time, processing completion time, and screen refresh time. They are different measurements.

## Changes in volume

Unusually low or high counts and missing partitions are signals to investigate.

| Change | Possible causes |
| --- | --- |
| Sharp decrease | Collection failure, producer problem, filter bug |
| Sharp increase | Duplicates, replay, retry storm, real traffic spike |
| Missing partition | That scope may not have been created or processed |

Compare recent averages, the same weekday, and seasonal patterns. An absolute threshold alone can flag a normal weekend decline or hide a missing partition inside a total count. These causes are hypotheses. A volume change alone does not prove one.

## Monitor schema and distributions

Watch column additions, removals, renames, type changes, and nullable changes. A breaking change can break downstream consumers. Connect this information to [lineage](lineage-metadata.md) to help find affected consumers.

Volume can be normal while values change. Watch null rate drift, cardinality drift, category distributions, and numeric distributions.

```text
Usual FAILED rate = 5%
Today's FAILED rate = 45%
Total row count = within the usual range
```

This example shows why counts alone cannot prove data health. Use more evidence to tell a real failure increase from a change in how status is recorded.

## Pipeline health and data health

| Pipeline health | Data health |
| --- | --- |
| Job status | Freshness |
| Kafka lag | Volume |
| Runtime | Schema |
| CPU and memory | NULLs and duplicates |
| Execution failures | Distribution |

**Green pipeline ≠ healthy data.** A successful job can return zero rows because its query logic is wrong. If a job is late, check data health as well to learn which datasets and users are affected.

## SLIs and SLOs

Observability measures data state over time. These are hypothetical measurements and targets.

| SLI measurement | Example SLO target |
| --- | --- |
| Freshness = 3 minutes | Freshness < 5 minutes |
| NULL rate = 0.5% | NULL rate < 1% |
| Volume = 98M rows | Volume deviation from the baseline < 20% |

The value 98M alone cannot show whether the deviation target is met. You need a baseline and a measurement window. Use several signals and define them for the dataset's business purpose. Share definitions with [quality SLOs](data-quality.md) so that measurement and response agree.

## Actionable alerts

The aim is to report problems worth acting on, not to maximize alert count. Repeated ALERT and RECOVERY states near a threshold create a noisy alert. An actionable alert makes it clear where to investigate.

Include these elements:

- **Threshold:** Which condition failed?
- **Duration:** How long has it lasted?
- **Severity:** How large is the impact? Warning and Critical can use different levels.
- **Context:** Which dataset, partition, stage, owner, and related run should be checked?

Policies can vary by dataset importance tier. Define duration and context to reduce alert fatigue. Check that this does not hide important signals.

## LLM in Practice: investigate empty output from a successful job

**Situation:** The Gold job succeeded, but today's dashboard data has zero rows.

**Context to Give the LLM:** Provide sanitized row counts and freshness by stage, partition lists, recent schema and filter changes, run logs, a normal same-weekday baseline, and dataset SLOs.

**Example Prompt:**

```text
Investigate this hypothetical incident before suggesting a redesign.
The Gold job succeeded, but today's dashboard shows zero rows.
Use the supplied row counts, freshness by stage, partition list,
schema and filter changes, logs, weekday baseline, and SLOs.
Separate facts, assumptions, hypotheses, and missing evidence.
Rank the next checks and explain what each result would support.
Do not infer a root cause from correlation alone.
```

**Expected Output:** Checks that separate missing source data, missing partitions, filter errors, and delayed downstream refresh.

**What the LLM Can Get Wrong:** It may treat a green job as evidence of healthy data. It may inspect only total counts and miss a missing partition.

**How to Validate:** Check actual query results and timestamps at each stage, change history, and dashboard refresh state. Confirm the LLM's hypotheses with evidence before acting.

[Data quality](data-quality.md) · [Lineage and metadata](lineage-metadata.md) · [Handbook home](../index.md)
